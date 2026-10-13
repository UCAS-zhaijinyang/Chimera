"""Real Chromium interaction with text observations and the owning chat client.

No hidden model backend: all browser decisions use the workflow's callback,
so DeepSeek usage and lifecycle accounting include internal browser rounds.
"""
from __future__ import annotations
import base64
import hashlib
import json
import subprocess
import tempfile
from urllib.parse import urlparse, unquote
import uuid
from pathlib import Path


ACTION_SCHEMA = {'type': 'function', 'function': {'name': 'browser_action',
    'description': 'Interact with the current real Chromium page; observe the resulting DOM.',
    'parameters': {'type': 'object', 'properties': {
        'action': {'type': 'string', 'enum': ['navigate', 'click', 'fill', 'read', 'back', 'scroll',
            'hover', 'select', 'upload', 'download', 'screenshot', 'press', 'find_text',
            'scroll_top', 'scroll_bottom', 'unfocus', 'ask_question_about_video']},
        'selector': {'type': 'string'}, 'value': {'type': 'string'}, 'url': {'type': 'string'}},
        'required': ['action', 'selector', 'value', 'url']}}}


class BrowserSession:
    def __init__(self, workspace):
        from playwright.sync_api import sync_playwright
        self.workspace = Path(workspace).resolve()
        self.chat_fn = None
        self.page_history = []
        self.media = self.workspace / ".browser"
        self.media.mkdir(parents=True, exist_ok=True)
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.launch(headless=True)
            self.context = self.browser.new_context(accept_downloads=True)
            self.page = self.context.new_page()
            self.page.set_default_timeout(15000)
            self.context.on("page", self._activate_page)
        except Exception:
            self.playwright.stop()
            raise

    def _activate_page(self, page):
        self.page_history.append(self.page.url)
        self.page = page
        self.page.set_default_timeout(15000)

    def observe(self, last_action=None):
        elements = self.page.locator('a,button,input,textarea,select,[contenteditable=true],[role],[tabindex]').evaluate_all('''nodes => nodes.slice(0,150).map((n,i) => ({
            tag:n.tagName, id:n.id, name:n.name || '', type:n.type || '', text:(n.innerText || n.value || '').slice(0,300),
            href:n.getAttribute('href'), placeholder:n.getAttribute('placeholder'), role:n.getAttribute('role'),
            aria_label:n.getAttribute('aria-label'), editable:n.isContentEditable,
            bounds:(()=>{let r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}})()}))''')
        shot = self.media / (uuid.uuid4().hex + '.png')
        self.page.screenshot(path=str(shot))
        return {'screenshot_path': str(shot), 'screenshot_sha256': hashlib.sha256(shot.read_bytes()).hexdigest(),
                'url': self.page.url, 'text': self.page.locator('body').inner_text()[:24000],
                'elements': elements, 'last_action': last_action}

    def action(self, args):
        action = args['action']
        selector, value = args.get('selector', ''), args.get('value', '')
        if action == 'navigate': self.page.goto(args['url'], wait_until='domcontentloaded')
        elif action == 'click': self.page.locator(selector).click()
        elif action == 'fill': self.page.locator(selector).fill(value)
        elif action == 'press': self.page.locator(selector).press(value)
        elif action == 'find_text': self.page.get_by_text(value, exact=False).first.scroll_into_view_if_needed()
        elif action == 'scroll_top': self.page.evaluate('window.scrollTo(0,0)')
        elif action == 'scroll_bottom': self.page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
        elif action == 'unfocus':
            self.page.mouse.click(0, 0)
            self.page.evaluate('document.activeElement.blur()')
        elif action == 'ask_question_about_video':
            answer, frames = self.video_question(selector, value, args.get('url'))
            return {**self.observe(args), 'video_answer': answer, 'video_frames': frames}
        elif action == 'back':
            response = self.page.go_back(wait_until='domcontentloaded')
            if response is None and self.page_history:
                self.page.goto(self.page_history.pop(), wait_until='domcontentloaded')
        elif action == 'hover': self.page.locator(selector).hover()
        elif action == 'select': self.page.locator(selector).select_option(value)
        elif action == 'scroll':
            self.page.mouse.wheel(0, int(value or '800'))
        elif action in {'upload', 'download', 'screenshot'}:
            path = (self.workspace / value).resolve()
            if self.workspace not in path.parents: raise PermissionError('browser file must stay inside business workspace')
            path.parent.mkdir(parents=True, exist_ok=True)
            if action == 'upload': self.page.locator(selector).set_input_files(str(path))
            elif action == 'download':
                with self.page.expect_download() as pending: self.page.locator(selector).click()
                pending.value.save_as(str(path))
            else: self.page.screenshot(path=str(path), full_page=True)
        elif action != 'read': raise ValueError('unknown browser action')
        self.page.wait_for_timeout(100)
        return self.observe(args)

    @staticmethod
    def observation_content(observation, *, images=False):
        text = {'type': 'text', 'text': json.dumps(observation, ensure_ascii=False)}
        if not images: return text['text']
        return [text, {'type': 'image_url', 'image_url': {'url':
            'data:image/png;base64,' + base64.b64encode(Path(observation['screenshot_path']).read_bytes()).decode()}}]

    def video_question(self, selector, question, url=None):
        if not question or self.chat_fn is None:
            raise ValueError('video analysis requires a question and the owning model callback')
        source = url or self.page.locator(selector or 'video').first.evaluate('(v)=>v.currentSrc || v.src')
        if not source: source = self.page.url
        parsed = urlparse(source)
        work = self.media / ('video-' + uuid.uuid4().hex); work.mkdir()
        if parsed.scheme == 'file':
            video = Path(unquote(parsed.path))
        elif parsed.scheme in {'http','https'}:
            # The browser context request preserves the user's page authentication.
            if parsed.path.lower().endswith(('.mp4','.webm','.mov','.mkv')):
                response = self.context.request.get(source)
                if not response.ok: raise RuntimeError('video download failed')
                video = work / 'source.mp4'; video.write_bytes(response.body())
            else:
                # Same webpage-video ability as the original downloader; no
                # model backend or audio API is created here.
                import yt_dlp
                with yt_dlp.YoutubeDL({'outtmpl':str(work/'source.%(ext)s'), 'quiet':True,
                                      'format':'best[ext=mp4]/best', 'socket_timeout':30}) as downloader:
                    info = downloader.extract_info(source, download=True)
                    video = Path(downloader.prepare_filename(info))
        else:
            video = (self.workspace / source).resolve()
        duration = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
            '-of','default=noprint_wrappers=1:nokey=1',str(video)],capture_output=True,text=True,check=True,timeout=60)
        seconds = float(duration.stdout)
        if seconds <= 0: raise ValueError('video has no duration')
        # Original defaults to 28 visual frames with audio disabled. Preserve
        # that sample budget and include timestamps; no unbilled nested model.
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(video),'-vf',
            f'fps={28 / seconds},scale=768:-2','-frames:v','28',str(work/'frame-%03d.jpg')],
            capture_output=True,check=True,timeout=120)
        frames = sorted(work.glob('frame-*.jpg'))
        if not frames: raise RuntimeError('video frame extraction produced no evidence')
        content = [{'type':'text','text':question + '\nVisual frames in temporal order. No audio transcription.'}]
        for i,frame in enumerate(frames):
            content.extend([{'type':'text','text':f'Frame timestamp approximately {i * seconds / 28:.3f}s'},
                {'type':'image_url','image_url':{'url':'data:image/jpeg;base64,' + base64.b64encode(frame.read_bytes()).decode()}}])
        response = self.chat_fn({'workflow_id':'browser','state':'video_analysis',
                                'messages':[{'role':'user','content':content}], 'tools':[]})
        answer = response.get('content')
        if not answer or response.get('tool_calls'): raise RuntimeError('video analysis returned no answer')
        return answer, [{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in frames]

    def browse(self, task_prompt, start_url, round_limit, *, chat_fn, execute_action):
        if type(round_limit) is not int or not 1 <= round_limit <= 40:
            raise ValueError('browser round_limit must be between 1 and 40')
        self.chat_fn = chat_fn
        observation = execute_action({'action': 'navigate', 'url': start_url, 'selector': '', 'value': ''})
        # Initial navigation does not represent a model-directed previous action.
        observation['last_action'] = None
        messages = [{'role': 'system', 'content':
            'Complete the browser task using browser_action and actual DOM observations. Use CSS selectors '
            'or Playwright text selectors; make one call per turn. Never claim success without inspecting '
            'the outcome. fill only fills: use press with value Enter to submit via keyboard. '
            'Use ask_question_about_video for visual video questions, value is the question. Give a final answer when the requested outcome is verified. Do not invent page content.'},
            {'role': 'user', 'content': task_prompt}]
        for step in range(round_limit):
            request = {'workflow_id': 'browser', 'state': 'interacting', 'messages': [*messages,
                {'role': 'user', 'content': self.observation_content(observation, images=getattr(chat_fn, 'supports_images', False))}], 'tools': [ACTION_SCHEMA]}
            response = chat_fn(request)
            calls = response.get('tool_calls') or []
            if not calls:
                return {'answer': str(response.get('content') or ''), 'observation': observation,
                        'browser_rounds': step + 1, 'acceptance': 'requires_independent_check'}
            if len(calls) != 1 or calls[0].get('function', {}).get('name') != 'browser_action':
                raise ValueError('browser expects exactly one browser_action')
            call = calls[0]
            arguments = call['function']['arguments']
            args = json.loads(arguments) if isinstance(arguments, str) else arguments
            if not isinstance(args, dict) or any(k not in args for k in ('action','selector','value','url')):
                raise ValueError('malformed browser action')
            observation = execute_action(args)
            messages.extend([{'role': 'assistant', 'tool_calls': calls}, {'role': 'tool',
                'tool_call_id': call['id'], 'content': json.dumps(observation, ensure_ascii=False)}])
        raise RuntimeError('browser task did not complete within round limit')

    def close(self):
        try: self.browser.close()
        finally: self.playwright.stop()

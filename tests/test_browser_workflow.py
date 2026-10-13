from pathlib import Path

import json
import pytest
from test_base_tool_workflows import call


def test_browser_real_form_updates_dom_and_records_nested_calls(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    business = tmp_path / 'business'
    business.mkdir()
    page = business / 'index.html'
    page.write_text('<input id="name"><button id="save" onclick="document.getElementById(\'result\').textContent=document.getElementById(\'name\').value">Save</button><p id="result"></p>')
    def employee(request):
        if request.get('workflow_id') == 'browser':
            state = request['messages'][-1]['content']
            if '"last_action": null' in state:
                return call('browser_action', action='fill', selector='#name', value='verified', url='')
            if '"action": "fill"' in state:
                return call('browser_action', action='click', selector='#save', value='', url='')
            assert 'verified' in state
            return {'content': 'Form completed'}
        if request['state'] == 'requested':
            return call('browse_url', task_prompt='Fill name with verified and save', start_url=page.as_uri(), round_limit=5)
        if request['state'] == 'working':
            return call('finish_task', summary='verified')
        return {'content': 'done'}
    loop = WorkflowToolLoop(tmp_path / 'capture', member_id='m', trace_id='t',
                            base_tools=True, business_workspace=business)
    result = loop.run('Interact with application', chat_fn=employee)
    assert result.state == 'completed'
    events = [json.loads(s.split(' ', 1)[1]) for s in loop.log_path.read_text().splitlines()]
    nested = [e for e in events if e.get('workflow_id') == 'browser']
    assert sum(e['event_type'] == 'model_started' for e in nested) == 3
    assert sum(e['event_type'] == 'model_terminal' for e in nested) == 3
    assert sum(e['event_type'] == 'tool_call' for e in nested) >= 3
    assert any('verified' in str(e.get('result', {}).get('payload')) for e in nested)


def test_browser_no_completion_at_limit_is_failure(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    page = tmp_path / 'index.html'
    page.write_text('<p>unfinished</p>')
    def employee(request):
        if request.get('workflow_id') == 'browser':
            return call('browser_action', action='read', selector='', value='', url='')
        return call('browse_url', task_prompt='Work', start_url=page.as_uri(), round_limit=1)
    loop = WorkflowToolLoop(tmp_path / 'capture', member_id='m', trace_id='t', base_tools=True)
    with pytest.raises(RuntimeError): loop.run('Browse', workflow_id='general', chat_fn=employee, max_tool_errors=0)


def test_browser_press_enter_submits_a_real_form(tmp_path):
    from browser_runtime import BrowserSession
    page=tmp_path/'keyboard.html'
    page.write_text('<input id="search" onkeydown="if(event.key===\'Enter\')document.querySelector(\'#result\').textContent=this.value"><p id="result"></p>')
    browser=BrowserSession(tmp_path)
    try:
        browser.action({'action':'navigate','url':page.as_uri()})
        browser.action({'action':'fill','selector':'#search','value':'keyboard verified'})
        result=browser.action({'action':'press','selector':'#search','value':'Enter'})
        assert 'keyboard verified' in result['text']
    finally:browser.close()


@pytest.mark.parametrize("failure_kind", ["unsent", "truncated"])
def test_browser_unsent_model_retry_keeps_already_committed_click(tmp_path, failure_kind):
    from workflow_runtime import WorkflowToolLoop
    page=tmp_path/'counter.html'
    page.write_text('''<button id="send" onclick="localStorage.setItem('count',String(Number(localStorage.getItem('count')||0)+1));document.querySelector('#count').textContent=localStorage.getItem('count')">Send</button><p id="count"></p><script>document.querySelector('#count').textContent=localStorage.getItem('count')||'0'</script>''')
    class Employee:
        last_error_metadata=None
        def __init__(self):self.failed=False
        def __call__(self,request):
            if request['workflow_id']=='browser':
                observation=json.loads(request['messages'][-1]['content'])
                if observation['last_action'] is None:return call('browser_action',action='click',selector='#send',value='',url='')
                if not self.failed:
                    self.failed=True;self.last_error_metadata={'request_not_sent':True} if failure_kind=='unsent' else {'response_not_delivered':True};raise RuntimeError('model transport failure')
                self.last_error_metadata=None
                assert observation['text'].endswith('1'), observation
                return {'content':'one click verified'}
            if request['state']=='requested':return call('browse_url',task_prompt='Click Send once',start_url=page.as_uri(),round_limit=5)
            if request['state']=='working':return call('finish_task',summary='verified')
            return {'content':'done'}
    loop=WorkflowToolLoop(tmp_path/'capture',member_id='m',trace_id='t',base_tools=True)
    assert loop.run('Browse',workflow_id='general',chat_fn=Employee()).state=='completed'


def test_browser_visual_observation_and_accessible_controls(tmp_path):
    from browser_runtime import BrowserSession
    page=tmp_path/'visual.html'
    page.write_text('<div contenteditable="true" role="textbox" aria-label="Editor">start</div><canvas id="canvas" width="100" height="100"></canvas><script>let c=document.querySelector("canvas").getContext("2d");c.fillStyle="red";c.fillRect(0,0,100,100)</script>')
    browser=BrowserSession(tmp_path)
    try:
        result=browser.action({'action':'navigate','url':page.as_uri()})
        assert any(e['role']=='textbox' and e['aria_label']=='Editor' for e in result['elements'])
        assert Path(result['screenshot_path']).exists()
        assert result['screenshot_sha256']
        request=browser.observation_content(result, images=True)
        assert any(part['type']=='image_url' for part in request)
        assert browser.action({'action':'fill','selector':'[role=textbox]','value':'edited'})['text'].startswith('edited')
    finally:browser.close()


def test_browser_video_question_uses_real_frames_and_owner_client(tmp_path):
    import subprocess
    from browser_runtime import BrowserSession
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=red:s=160x120:d=1','-y',str(tmp_path/'clip.mp4')],check=True)
    page=tmp_path/'video.html';page.write_text('<video src="clip.mp4" controls></video>')
    browser=BrowserSession(tmp_path)
    seen=[]
    def client(request):
        seen.append(request)
        assert any(p['type']=='image_url' for p in request['messages'][-1]['content'])
        return {'content':'Red'}
    try:
        browser.chat_fn=client
        browser.action({'action':'navigate','url':page.as_uri()})
        result=browser.action({'action':'ask_question_about_video','selector':'video','value':'What color?','url':''})
        assert result['video_answer']=='Red' and result['video_frames']
        assert len(seen)==1
    finally:browser.close()


def test_browser_popup_and_back_preserve_navigation(tmp_path):
    from browser_runtime import BrowserSession
    page=tmp_path/'home.html';target=tmp_path/'target.html'
    target.write_text('<p>popup target</p>')
    page.write_text('<a id="open" href="target.html" target="_blank">Open popup</a>')
    browser=BrowserSession(tmp_path)
    try:
        browser.action({'action':'navigate','url':page.as_uri()})
        assert browser.action({'action':'click','selector':'#open'})['url']==target.as_uri()
        assert browser.action({'action':'back'})['url']==page.as_uri()
    finally:browser.close()


def test_browser_file_controls_scroll_and_focus_are_real(tmp_path):
    from browser_runtime import BrowserSession
    (tmp_path/'upload.txt').write_text('upload content')
    page=tmp_path/'controls.html'
    page.write_text('''<input id="file" type="file" onchange="document.querySelector('#filename').textContent=this.files[0].name"><p id="filename"></p><select id="choices"><option value="a">A</option><option value="b">B</option></select><input id="focus"><a id="download" href="data:text/plain,download-evidence" download="result.txt">Download</a><div style="height:1800px"></div><p>Bottom marker</p>''')
    browser=BrowserSession(tmp_path)
    try:
        browser.action({'action':'navigate','url':page.as_uri()})
        assert 'upload.txt' in browser.action({'action':'upload','selector':'#file','value':'upload.txt'})['text']
        browser.action({'action':'select','selector':'#choices','value':'b'})
        assert browser.page.locator('#choices').input_value()=='b'
        browser.action({'action':'hover','selector':'#download'})
        browser.action({'action':'download','selector':'#download','value':'download.txt'})
        assert (tmp_path/'download.txt').read_text()=='download-evidence'
        browser.action({'action':'scroll_bottom'});assert browser.page.evaluate('window.scrollY')>0
        browser.action({'action':'scroll_top'});assert browser.page.evaluate('window.scrollY')==0
        browser.action({'action':'scroll','value':'300'});assert browser.page.evaluate('window.scrollY')>0
        browser.action({'action':'find_text','value':'Bottom marker'});assert browser.page.evaluate('window.scrollY')>500
        browser.action({'action':'screenshot','value':'page.png'});assert (tmp_path/'page.png').read_bytes().startswith(b'\x89PNG')
        browser.action({'action':'click','selector':'#focus'})
        browser.action({'action':'unfocus'});assert browser.page.evaluate('document.activeElement.id')!='focus'
    finally:browser.close()

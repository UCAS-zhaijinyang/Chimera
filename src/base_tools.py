"""Shared native Camel tool contracts for legacy and workflow execution.

Shell execution is an experiment capability, not a security sandbox. Deploy
attack experiments in an isolated environment. Capture stays outside its cwd.
"""
from __future__ import annotations

import inspect
import os
from pathlib import Path
import signal
import subprocess
import tempfile


class BaseToolRegistry:
    def __init__(self, workspace, *, offline=False, models=None):
        from camel.toolkits import FileWriteToolkit, TerminalToolkit, BrowserToolkit, FunctionTool
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.models = models
        self.browser = None
        self.browser_chat_fn = None
        self.browser_execute_action = None
        self.sessions = {}
        self._tools = {}
        self._schemas = {}
        self._function_tool = FunctionTool
        terminal_kwargs = {'working_dir': str(self.workspace), 'need_terminal': False}
        # Published Chimera's Camel fork accepts an additional log_path.
        initializer = TerminalToolkit.__init__
        for cell in getattr(initializer, '__closure__', ()) or ():
            candidate = cell.cell_contents
            if callable(candidate) and getattr(candidate, '__name__', '') == '__init__':
                initializer = candidate
                break
        if 'log_path' in inspect.signature(initializer).parameters:
            terminal_kwargs['log_path'] = str(self.workspace)
        self.terminal = TerminalToolkit(**terminal_kwargs)
        tools = [*FileWriteToolkit(output_dir=str(self.workspace)).get_tools(), *self.terminal.get_tools()]
        if not offline:
            from search_runtime import search_brave
            tools += [FunctionTool(search_brave)]
            # Schema discovery must not launch Chromium or instantiate default
            # OpenAI models. Initialization happens only when browse_url is used.
            browser_contract = object.__new__(BrowserToolkit)
            tools += [FunctionTool(browser_contract.browse_url)]
        for tool in tools:
            schema = tool.get_openai_tool_schema()
            name = schema['function']['name']
            self._schemas[name] = schema
            self._tools[name] = tool

    def schemas(self):
        return list(self._schemas.values())

    def function_tools(self):
        tools = []
        for name, schema in self._schemas.items():
            def make_invoke(tool_name):
                def invoke(**kwargs):
                    return self.execute(tool_name, kwargs)
                invoke.__name__ = tool_name
                return invoke
            tools.append(self._function_tool(make_invoke(name), openai_tool_schema=schema))
        return tools

    @staticmethod
    def _group_running(session):
        # Leaders may exit while descendants still own the session's pgid.
        try:
            # Zombies cannot mutate files; do not let an orphan zombie prevent
            # settlement after its live descendants have been terminated.
            listing = subprocess.run(['ps', '-axo', 'pgid=,stat='], capture_output=True, text=True, check=True)
            return any(len(parts := line.split()) == 2 and parts[0] == str(session['process'].pid)
                       and not parts[1].startswith('Z') for line in listing.stdout.splitlines())
        except ProcessLookupError:
            return False

    def _snapshot(self, session):
        process = session['process']
        for handle in (session['stdout'], session['stderr']):
            handle.flush()
        def read(handle):
            with open(handle.name, encoding='utf-8', errors='replace') as reader:
                return reader.read()[-16000:]
        returncode = process.poll()
        running = returncode is None or self._group_running(session)
        session['observed_terminal'] = not running
        return {'stdout': read(session['stdout']), 'stderr': read(session['stderr']),
                'returncode': returncode, 'running': running, 'cancelled': session.get('cancelled', False)}

    def _shell(self, name, args):
        session_id = args['id']
        if name == 'shell_exec':
            previous = self.sessions.get(session_id)
            if previous and (previous['process'].poll() is None or self._group_running(previous)):
                raise ValueError('shell session is still running; wait, write or kill it first')
            if previous:
                previous['stdout'].close(); previous['stderr'].close()
                if previous['process'].stdin: previous['process'].stdin.close()
            stdout = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8')
            stderr = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8')
            # Own process group so timeout/kill closes descendants, too.
            process = subprocess.Popen(args['command'], shell=True, cwd=self.workspace,
                stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True, start_new_session=True)
            session = self.sessions[session_id] = {'process': process, 'stdout': stdout, 'stderr': stderr, 'observed_terminal': False}
            try: process.wait(timeout=1)
            except subprocess.TimeoutExpired: pass
            return self._snapshot(session)
        if session_id not in self.sessions:
            raise ValueError('unknown shell session')
        session = self.sessions[session_id]
        process = session['process']
        if name == 'shell_wait':
            seconds = args.get('seconds')
            seconds = 30 if seconds is None else seconds
            if type(seconds) is not int or not 0 <= seconds <= 60:
                raise ValueError('shell wait must be an integer between 0 and 60 seconds')
            try: process.wait(timeout=seconds)
            except subprocess.TimeoutExpired: pass
        elif name == 'shell_write_to_process':
            if process.poll() is not None or process.stdin is None:
                raise ValueError('process is not running')
            process.stdin.write(args['input'] + ('\n' if args['press_enter'] else ''))
            process.stdin.flush()
        elif name == 'shell_kill_process':
            if process.poll() is None or self._group_running(session):
                try: os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError: pass
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired: pass
                # A reaped leader does not mean its children were reaped.
                if self._group_running(session):
                    try: os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError: pass
                process.wait(timeout=5)
            session['cancelled'] = True
        return self._snapshot(session)

    def execute(self, name, arguments):
        if name not in self._tools:
            raise ValueError(f'unknown base tool: {name}')
        args = dict(arguments)
        if name.startswith('shell_'):
            return self._shell(name, args)
        if name == 'browse_url':
            if self.browser_chat_fn is not None:
                from browser_runtime import BrowserSession
                if self.browser is None:
                    self.browser = BrowserSession(self.workspace)
                return self.browser.browse(**args, chat_fn=self.browser_chat_fn,
                    execute_action=self.browser_execute_action or self.browser.action)
            if self.browser is None:
                from camel.toolkits import BrowserToolkit
                models = self.models
                if callable(models): models = models()
                if models is None:
                    from foundation_model import create_camel_model
                    models = {'browsing': create_camel_model(temperature=0),
                              'planning': create_camel_model(temperature=0)}
                self.browser = BrowserToolkit(headless=True, cache_dir=str(self.workspace / '.browser'),
                    web_agent_model=models['browsing'], planning_agent_model=models['planning'])
            result = self.browser.browse_url(**args)
            if 'The task is not completed within the round limit' in result:
                raise RuntimeError('browser task did not complete')
            return result
        if name == 'write_to_file':
            path = Path(args['filename'])
            path = (self.workspace / path).resolve()
            if self.workspace not in path.parents:
                raise PermissionError('file output must stay inside business workspace')
        result = self._tools[name](**args)
        if (isinstance(result, str) and result.startswith(('Error', 'Command rejected', 'Safety restriction', 'File not found:', 'Directory not found:', 'The path provided is not a file', 'The path provided is not a directory'))) or (
            isinstance(result, list) and any(isinstance(row, dict) and 'error' in row for row in result)):
            raise RuntimeError('native tool returned an error')
        return result

    def has_running_processes(self):
        return any(s['process'].poll() is None or self._group_running(s) for s in self.sessions.values())

    def can_finish(self):
        return not self.has_running_processes() and all(
            s.get('observed_terminal') and (s['process'].returncode == 0 or s.get('cancelled'))
            for s in self.sessions.values())

    def close(self):
        for key, session in self.sessions.items():
            if session['process'].poll() is None or self._group_running(session):
                self._shell('shell_kill_process', {'id': key})
            if session['process'].stdin: session['process'].stdin.close()
            session['stdout'].close(); session['stderr'].close()
        self.sessions.clear()
        if self.browser is not None:
            from browser_runtime import BrowserSession
            if isinstance(self.browser, BrowserSession):
                self.browser.close()
                self.browser = None
                return
            try: self.browser.browser.close()
            finally:
                self.browser.browser.playwright.stop()
                self.browser = None


def create_base_tools(workspace, *, offline=False, models=None):
    """Return an owning registry; keep it alive until the task finishes."""
    return BaseToolRegistry(workspace, offline=offline, models=models)

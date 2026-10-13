"""Catch lost native tools, false completion and lost cross-task files."""
import json
import sys
from pathlib import Path
import pytest


def call(name, **args):
    return {'tool_calls': [{'id': 'native-call', 'type': 'function',
                           'function': {'name': name, 'arguments': json.dumps(args)}}]}


def test_general_workflow_runs_terminal_and_records_real_result(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    loop = WorkflowToolLoop(tmp_path / 'capture', member_id='m1', trace_id='t1',
                            base_tools=True, business_workspace=tmp_path / 'business')
    replies = iter([call('shell_exec', id='s1', command="printf evidence > output.txt"),
                    call('finish_task', summary='Written and checked'), {'content': 'done'}])
    result = loop.run('Manage arbitrary operational resources', chat_fn=lambda r: next(replies))
    assert result.workflow_id == 'general' and result.state == 'completed'
    assert (tmp_path / 'business/output.txt').read_text() == 'evidence'
    rows = [json.loads(s.split(' ', 1)[1]) for s in loop.log_path.read_text().splitlines()]
    tool = next(r for r in rows if r['event_type'] == 'tool_call' and r['tool_name'] == 'shell_exec')
    assert tool['result']['payload']['returncode'] == 0
    assert tool['result']['output_artifact_ids']
    assert sum(r['event_type'] == 'tool_started' for r in rows) == 2
    assert sum(r['event_type'] == 'tool_call' for r in rows) == 2


def test_general_cannot_finish_without_tool_evidence(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    loop = WorkflowToolLoop(tmp_path, member_id='m1', trace_id='t1', base_tools=True)
    with pytest.raises(ValueError):
        loop.run('Operate resources', workflow_id='general',
                 chat_fn=lambda r: call('finish_task', summary='done'), max_tool_errors=0)


def test_failed_terminal_command_does_not_complete(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    loop = WorkflowToolLoop(tmp_path, member_id='m1', trace_id='t1', base_tools=True)
    with pytest.raises(RuntimeError):
        loop.run('Operate resources', workflow_id='general', max_tool_errors=0,
                 chat_fn=lambda r: call('shell_exec', id='bad', command='exit 7'))
    rows = [json.loads(s.split(' ', 1)[1]) for s in loop.log_path.read_text().splitlines()]
    event = next(r for r in rows if r['event_type'] == 'tool_call')
    assert event['status'] == 'failed' and event['result']['payload']['returncode'] == 7
    assert rows[-1]['status'] == 'failed'


def test_native_file_write_and_find_schema_execute(tmp_path):
    from base_tools import BaseToolRegistry
    registry = BaseToolRegistry(tmp_path, offline=True)
    names = {s['function']['name'] for s in registry.schemas()}
    assert {'write_to_file', 'shell_exec', 'shell_view', 'shell_wait',
            'shell_write_to_process', 'shell_kill_process', 'file_find_by_name',
            'file_find_in_content'} <= names
    registry.execute('write_to_file', {'content': 'abc', 'filename': 'note.txt', 'encoding': None})
    assert (tmp_path / 'note.txt').read_text() == 'abc'
    result = registry.execute('file_find_in_content', {'file': str(tmp_path / 'note.txt'), 'regex': 'abc', 'sudo': False})
    assert 'abc' in str(result)
    registry.close()


def test_business_state_is_shared_but_capture_is_per_task(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    business = tmp_path / 'business'
    for trace, command in [('t1', 'printf shared > shared.txt'), ('t2', 'cat shared.txt')]:
        loop = WorkflowToolLoop(tmp_path / trace, member_id='m1', trace_id=trace,
                                base_tools=True, business_workspace=business)
        replies = iter([call('shell_exec', id='s', command=command),
                        call('finish_task', summary='done'), {'content': 'done'}])
        loop.run('Operate shared resources', chat_fn=lambda r: next(replies))
    rows = [json.loads(s.split(' ', 1)[1]) for s in (tmp_path / 't2/execution.log').read_text().splitlines()]
    event = next(r for r in rows if r['event_type'] == 'tool_call' and r['tool_name'] == 'shell_exec')
    assert 'shared' in event['result']['payload']['stdout']


def test_native_session_interaction_wait_view_and_kill(tmp_path):
    from base_tools import BaseToolRegistry
    registry = BaseToolRegistry(tmp_path, offline=True)
    result = registry.execute('shell_exec', {'id': 'input', 'command': f'{sys.executable} -u -c "print(input())"'})
    assert result['running']
    registry.execute('shell_write_to_process', {'id': 'input', 'input': 'hello', 'press_enter': True})
    result = registry.execute('shell_wait', {'id': 'input', 'seconds': 5})
    assert result['returncode'] == 0 and 'hello' in result['stdout']
    assert 'hello' in registry.execute('shell_view', {'id': 'input'})['stdout']
    registry.execute('shell_exec', {'id': 'sleep', 'command': f'{sys.executable} -c "import time; time.sleep(30)"'})
    result = registry.execute('shell_kill_process', {'id': 'sleep'})
    assert not result['running']
    registry.close()


def test_unsent_transport_failure_is_retried_with_closed_attempts(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    class Employee:
        last_error_metadata = None
        def __init__(self): self.replies = iter([None, call('shell_exec',id='s',command='printf recovered > result.txt'),
                                                call('finish_task',summary='verified'),{'content':'done'}])
        def __call__(self, request):
            result = next(self.replies)
            self.last_error_metadata = {'request_not_sent':True} if result is None else None
            if result is None: raise RuntimeError('TLS connection closed before request')
            return result
    loop = WorkflowToolLoop(tmp_path/'capture',member_id='m',trace_id='t',base_tools=True)
    result=loop.run('Operate resources',workflow_id='general',chat_fn=Employee())
    assert result.state=='completed'
    events=[json.loads(s.split(' ',1)[1]) for s in loop.log_path.read_text().splitlines()]
    assert sum(e['event_type']=='model_started' for e in events)==4
    assert sum(e['event_type']=='model_terminal' for e in events)==4
    assert len([e for e in events if e.get('tool_name')=='shell_exec' and e['event_type']=='tool_call'])==1


def test_async_nonzero_exit_cannot_finish_without_recorded_terminal(tmp_path):
    import time
    from workflow_runtime import WorkflowToolLoop
    replies=iter([call('shell_exec',id='s',command='sleep 1.1; exit 7'),call('finish_task',summary='done')])
    def employee(request):
        if request['state']=='working':time.sleep(.25)
        return next(replies)
    loop=WorkflowToolLoop(tmp_path,member_id='m',trace_id='t',base_tools=True,offline=True)
    with pytest.raises(ValueError):
        loop.run('Operate',workflow_id='general',chat_fn=employee,max_tool_errors=0)


def test_async_success_requires_explicit_observation_then_can_finish(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    replies=iter([call('shell_exec',id='s',command='sleep 1.1; printf verified'),
                  call('shell_wait',id='s',seconds=5),call('finish_task',summary='checked'),{'content':'done'}])
    loop=WorkflowToolLoop(tmp_path,member_id='m',trace_id='t',base_tools=True,offline=True)
    assert loop.run('Operate',workflow_id='general',chat_fn=lambda r:next(replies)).state=='completed'


def test_legacy_function_tool_objects_accept_their_native_arguments(tmp_path):
    from base_tools import BaseToolRegistry
    registry=BaseToolRegistry(tmp_path,offline=True)
    tools={t.get_openai_tool_schema()['function']['name']:t for t in registry.function_tools()}
    result=tools['shell_exec'](id='s',command='printf callable > native.txt')
    assert result['returncode']==0 and (tmp_path/'native.txt').read_text()=='callable'
    registry.close()


def test_missing_native_file_is_recorded_as_failure(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    loop=WorkflowToolLoop(tmp_path/'capture',member_id='m',trace_id='t',base_tools=True,offline=True)
    with pytest.raises(RuntimeError):
        loop.run('Read required file',workflow_id='general',max_tool_errors=0,
            chat_fn=lambda r:call('file_find_in_content',file=str(tmp_path/'missing.txt'),regex='required',sudo=False))


def test_cleanup_terminates_child_after_shell_leader_exits(tmp_path):
    import time
    from base_tools import BaseToolRegistry
    registry=BaseToolRegistry(tmp_path,offline=True)
    result=registry.execute('shell_exec',{'id':'s','command':'(sleep 2; printf late > late.txt) &'})
    assert result['running']
    registry.close()
    time.sleep(2.2)
    assert not (tmp_path/'late.txt').exists()


def test_semantic_and_native_tools_share_actual_business_root(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    loop=WorkflowToolLoop(tmp_path/'capture',member_id='m',trace_id='t',base_tools=True,business_workspace=tmp_path/'business',offline=True)
    loop.runtime.execute('code_edit',{'path':'src/main.py','content':'shared business code'})
    result=loop.base_registry.execute('shell_exec',{'id':'s','command':'cat src/main.py'})
    assert result['returncode']==0 and result['stdout']=='shared business code'
    assert not (tmp_path/'capture/src/main.py').exists()
    loop.base_registry.close()


def test_unsent_retries_do_not_consume_business_steps(tmp_path, monkeypatch):
    import workflow_runtime as module
    monkeypatch.setattr(module.time,'sleep',lambda seconds:None)
    class Employee:
        last_error_metadata=None
        def __init__(self):self.failures=6;self.replies=iter([call('shell_exec',id='s',command='printf recovered'),call('finish_task',summary='done'),{'content':'done'}])
        def __call__(self,request):
            if self.failures:
                self.failures-=1;self.last_error_metadata={'request_not_sent':True};raise RuntimeError('pre-send transport')
            self.last_error_metadata=None;return next(self.replies)
    loop=module.WorkflowToolLoop(tmp_path,member_id='m',trace_id='t',base_tools=True,offline=True)
    assert loop.run('Operate',workflow_id='general',chat_fn=Employee(),max_steps=3).state=='completed'


def test_native_find_by_name_has_real_matches_and_missing_directory_errors(tmp_path):
    from base_tools import BaseToolRegistry
    registry=BaseToolRegistry(tmp_path,offline=True)
    try:
        (tmp_path/'note.txt').write_text('actual')
        assert 'note.txt' in registry.execute('file_find_by_name',{'path':str(tmp_path),'glob':'*.txt'})
        assert registry.execute('file_find_in_content',{'file':str(tmp_path/'note.txt'),'regex':'unmatched','sudo':False})==''
        with pytest.raises(RuntimeError):registry.execute('file_find_by_name',{'path':str(tmp_path/'missing'),'glob':'*'})
    finally:registry.close()



def test_missing_brave_auth_is_recorded_as_failed_tool_not_completion(monkeypatch, tmp_path):
    from workflow_runtime import WorkflowToolLoop
    monkeypatch.delenv('BRAVE_SEARCH_API_KEY', raising=False)
    loop = WorkflowToolLoop(tmp_path, member_id='m', trace_id='search', base_tools=True)
    # Camel FunctionTool wraps provider RuntimeError in ValueError.
    with pytest.raises(ValueError, match='BRAVE_SEARCH_API_KEY'):
        loop.run('Search public documents', workflow_id='general', max_tool_errors=0,
                 chat_fn=lambda r: call('search_brave', query='Chimera', source='text', max_results=5))
    rows = [json.loads(s.split(' ', 1)[1]) for s in loop.log_path.read_text().splitlines()]
    event = next(r for r in rows if r.get('event_type') == 'tool_call')
    assert event['tool_name'] == 'search_brave' and event['status'] == 'failed'
    assert rows[-1]['event_type'] == 'task_terminal' and rows[-1]['status'] == 'failed'

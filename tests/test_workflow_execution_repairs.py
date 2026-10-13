"""Regressions for the actual premature exits and misleading tool outputs."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from task import OpenAICompatibleChatClient
from workflow_runtime import FilesystemToolRuntime, WorkflowToolLoop


def test_source_result_exposes_values_needed_to_write_a_correct_report(tmp_path):
    runtime = FilesystemToolRuntime(tmp_path, member_id='m', trace_id='t')
    result = runtime.execute('source_query', {'query': 'weekly counts'})
    assert result['payload']['rows'] == [{'week': 'W1', 'count': 3}, {'week': 'W2', 'count': 5}]
    table = runtime.execute('data_transform', {'input_artifact_id': result['output_artifact_ids'][0]})
    assert table['payload'] == [{'group': 'W1', 'count': 3}, {'group': 'W2', 'count': 5}]


def test_next_step_can_observe_whole_workflow_and_writeable_paths(tmp_path):
    captured = []
    def reply(request):
        captured.append(request)
        if len(captured) == 1:
            return {'tool_calls': [{'id': 'a', 'function': {'name': 'issue_create', 'arguments': '{"title":"Feature"}'}}]}
        return {'content': 'Stopped'}
    WorkflowToolLoop(tmp_path, member_id='m', trace_id='t').run('Implement a feature', chat_fn=reply)
    system = captured[1]['messages'][0]['content']
    assert 'issue_created' in system and 'design_document' in system and 'code_edit' in system
    assert 'artifacts/' in system and 'read-only' in system
    assert captured[1]['tool_choice'] == {'type': 'function', 'function': {'name': 'design_document'}}


def test_http_client_honors_workflow_required_tool_choice():
    seen = []
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def do_POST(self):
            seen.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({'model':'test','usage':{},'choices':[{'finish_reason':'stop','message':{'content':'x'}}]}).encode())
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        client = OpenAICompatibleChatClient(api_key='local-test', base_url=f'http://127.0.0.1:{server.server_port}')
        choice = {'type': 'function', 'function': {'name': 'source_query'}}
        client({'messages': [], 'tools':[{'type':'function','function':{'name':'source_query'}}], 'tool_choice':choice})
        assert seen[0]['tool_choice'] == choice
        assert seen[0]['parallel_tool_calls'] is False
        assert seen[0]['thinking'] == {'type':'disabled'}
    finally:
        server.shutdown()
        server.server_close()


def test_duplicate_tool_in_one_response_is_rejected_without_replaying_side_effect(tmp_path):
    from evaluation.campaign import ScriptedEmployee, golden_cases
    employee = ScriptedEmployee(golden_cases()[0])
    first = True
    def reply(request):
        nonlocal first
        response = employee(request)
        if first:
            first = False
            response['tool_calls'].append({**response['tool_calls'][0], 'id':'duplicate'})
        return response
    result = WorkflowToolLoop(tmp_path, member_id='m', trace_id='t').run('Analyze data and write a report', chat_fn=reply)
    assert result.state == 'delivered'
    records = [json.loads(l) for l in (tmp_path/'manifest.jsonl').read_text().splitlines()]
    assert len(records) == 5
    events = [json.loads(l.split(' ',1)[1]) for l in (tmp_path/'execution.log').read_text().splitlines()]
    calls = [e for e in events if e['event_type']=='tool_call' and e['tool_name']=='source_query']
    assert [e['status'] for e in calls] == ['success','rejected']
    assert events[-1]['status'] == 'completed'


def test_short_connection_deadline_keeps_longer_response_deadline():
    import time
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args): pass
        def do_POST(self):
            self.rfile.read(int(self.headers['Content-Length']))
            time.sleep(.12)
            self.send_response(200); self.end_headers()
            self.wfile.write(json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'slow valid response'}}]}).encode())
    server = ThreadingHTTPServer(('127.0.0.1',0), Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        client=OpenAICompatibleChatClient(api_key='local-test',base_url=f'http://127.0.0.1:{server.server_port}',
                                        timeout=.5,connect_timeout=.02)
        assert client({'messages':[]})['content']=='slow valid response'
    finally:
        server.shutdown(); server.server_close()


def test_out_of_state_call_gets_feedback_and_can_recover_without_executing_it(tmp_path):
    from evaluation.campaign import ScriptedEmployee, golden_cases
    employee = ScriptedEmployee(golden_cases()[0])
    first = True
    def reply(request):
        nonlocal first
        if first:
            first = False
            return {'tool_calls':[{'id':'invalid','function':{'name':'message_send','arguments':'{"to":["outside@example.invalid"]}'}}]}
        return employee(request)
    result = WorkflowToolLoop(tmp_path, member_id='m', trace_id='t').run('Analyze data and write a report', chat_fn=reply)
    assert result.state == 'delivered'
    records = [json.loads(l) for l in (tmp_path/'manifest.jsonl').read_text().splitlines()]
    assert len(records) == 5
    email = next(r for r in records if r['producer_tool']=='message_send')
    assert json.loads((tmp_path/email['path']).read_text())['to'] == ['chief@example.invalid']


def test_tool_recovery_is_bounded_and_preserves_all_rejections(tmp_path):
    import pytest
    response={'tool_calls':[{'id':'bad','function':{'name':'message_send','arguments':'{}'}}]}
    with pytest.raises(ValueError):
        WorkflowToolLoop(tmp_path, member_id='m', trace_id='t').run('Analyze data', chat_fn=lambda r:response)
    events=[json.loads(l.split(' ',1)[1]) for l in (tmp_path/'execution.log').read_text().splitlines()]
    assert len([e for e in events if e['event_type']=='tool_call' and e['status']=='rejected']) == 3
    assert events[-1]['status']=='failed'
    assert not (tmp_path/'manifest.jsonl').exists()


def test_feature_can_write_multiple_files_and_correct_code_after_failed_test(tmp_path):
    import sys
    responses = [
        ('issue_create', {'title':'Sum feature'}),
        ('design_document', {'content':'Sum with helper and behavioral test'}),
        ('code_edit', {'path':'src/helper.py', 'content':'def add(a,b):\n    return a+b\n'}),
        ('code_edit', {'path':'src/main.py', 'content':'from helper import add\ndef compute(a,b):\n    return 0\n'}),
        ('test_run', {'command':f'{sys.executable} -c "import sys;sys.path.insert(0,\'src\');from main import compute;assert compute(2,3)==5"'}),
        ('code_edit', {'path':'src/main.py', 'content':'from helper import add\ndef compute(a,b):\n    return add(a,b)\n'}),
        ('test_run', {'command':f'{sys.executable} -c "import sys;sys.path.insert(0,\'src\');from main import compute;assert compute(2,3)==5"'}),
        ('build', {'command':f'{sys.executable} -m compileall -q src'}),
        ('pull_request', {}), ('approve', {}),
    ]
    def reply(request):
        if not responses: return {'content':'Complete'}
        name, args=responses.pop(0)
        previous=[json.loads(m['content']) for m in request['messages'] if m['role']=='tool']
        latest=next((m['output_artifact_ids'][0] for m in reversed(previous) if m.get('output_artifact_ids')),None)
        if name in {'design_document','pull_request','approve'}:args['input_artifact_id']=latest
        return {'tool_calls':[{'id':f'c{len(responses)}','function':{'name':name,'arguments':json.dumps(args)}}]}
    result=WorkflowToolLoop(tmp_path,member_id='m',trace_id='t').run('Implement a sum feature',chat_fn=reply,max_steps=16)
    assert result.state=='completed'
    events=[json.loads(l.split(' ',1)[1]) for l in (tmp_path/'execution.log').read_text().splitlines()]
    assert [e['status'] for e in events if e['event_type']=='tool_call' and e['tool_name']=='test_run']==['failed','success']
    assert (tmp_path/'src/helper.py').exists()
    assert 'return add(a,b)' in (tmp_path/'src/main.py').read_text()


def test_json_escaped_decorator_is_not_misread_as_email_but_real_contact_is():
    from evaluation.trust import pii_candidates
    assert pii_candidates(json.dumps({'content':'def x():\n    pass\n@pytest.mark.parametrize("a", [1])'}))==[]
    assert len(pii_candidates(json.dumps({'content':'Contact alice@real-company.example-unreserved'})))==1
    ndjson='\n'.join([json.dumps({'content':'@pytest.mark.parametrize("a",[1])\ndef x(): pass'}),
                       json.dumps({'content':'pass\n@pytest.mark.parametrize("b",[2])'})])
    assert pii_candidates(ndjson)==[]
    assert len(pii_candidates(ndjson+'\n'+json.dumps({'content':'alice@company.example-unreserved'})))==1


def test_model_receives_the_actual_command_directory_and_available_build_command(tmp_path):
    import sys, shlex
    runtime=FilesystemToolRuntime(tmp_path,member_id='m',trace_id='t')
    result=runtime.execute('test_run',{'command':f'{shlex.quote(sys.executable)} -c "import os;print(os.getcwd())"'})
    environment=result['execution_environment']
    assert environment['cwd']==result['payload']['stdout'].strip()
    source=tmp_path/'src'; source.mkdir(); (source/'main.py').write_text('def x(): return 1\n')
    build=runtime.execute('build',{'command':environment['default_build_command']})
    assert build['business_status']=='success'
    assert (source/'__pycache__').is_dir()

import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from task import OpenAICompatibleChatClient
from evaluation.campaign import generate_study, golden_cases
from evaluation.trust import evaluate_study


def test_real_http_client_caps_output_records_usage_and_rejects_truncation():
    seen = []
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_POST(self):
            seen.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
            body = {'id': 'request1', 'model': 'returned-model', 'usage': {'prompt_tokens': 100, 'completion_tokens': 20},
                    'choices': [{'finish_reason': 'length' if len(seen) == 2 else 'stop', 'message': {'content': 'done'}}]}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        client = OpenAICompatibleChatClient(api_key='test-only', base_url=f'http://127.0.0.1:{server.server_port}',
                                           model='deepseek-flash', max_tokens=4096, thinking=False)
        assert client({'messages': [], 'temperature': .2})['content'] == 'done'
        assert client.last_usage['prompt_tokens'] == 100
        assert client.last_model == 'returned-model'
        assert seen[0]['max_tokens'] == 4096
        assert seen[0]['thinking'] == {'type': 'disabled'}
        assert seen[0]['temperature'] == .2
        with pytest.raises(RuntimeError, match='truncated'):
            client({'messages': []})
        assert client.last_usage['completion_tokens'] == 20
    finally:
        server.shutdown()
        server.server_close()


def test_artifact_credential_is_scanned_even_when_hash_matches(tmp_path):
    generate_study(tmp_path / 'study', cases=golden_cases()[:1], repetitions=1)
    root = tmp_path / 'study'
    manifest = root / 'workspaces/t0001/manifest.jsonl'
    rows = [json.loads(line) for line in manifest.read_text().splitlines()]
    artifact = root / 'workspaces/t0001' / rows[0]['path']
    artifact.write_text(json.dumps({'content': 'sk-' + 'x' * 32}))
    rows[0]['sha256'] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    manifest.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    assert evaluate_study(root)['metrics']['L0.8']['status'] == 'FAIL'


def test_campaign_release_is_observable_only_and_complete(tmp_path):
    study = generate_study(tmp_path / 'study', cases=golden_cases()[:1], repetitions=1)
    assert study['release_files']
    rows = [json.loads(line) for line in (tmp_path / 'study' / study['release_files'][0]).read_text().splitlines()]
    report = evaluate_study(tmp_path / 'study')
    assert len(rows) == report['inventory']['unique_events']
    assert not any('attack_truth' in row or 'expected_status' in row for row in rows)
    assert report['status'] == 'PASS'

@pytest.mark.parametrize('mutation,metric', [('concealed_input','L0.4'), ('wrong_version','L0.4'), ('marker','L0.1'), ('reverse_call','L0.5'), ('pii','L0.8')])
def test_additional_integrity_challenges(tmp_path, mutation, metric):
    generate_study(tmp_path / 'study', cases=golden_cases()[:1], repetitions=1)
    root = tmp_path / 'study'
    manifest = root / 'workspaces/t0001/manifest.jsonl'
    records = [json.loads(line) for line in manifest.read_text().splitlines()]
    log = root / 'workspaces/t0001/execution.log'
    rows = [(line.split(' ', 1)[0], json.loads(line.split(' ', 1)[1])) for line in log.read_text().splitlines()]
    if mutation == 'concealed_input':
        records[1]['inputs'] = []
        records[1]['root_type'] = 'standalone_generated_input'
    elif mutation == 'wrong_version':
        records[1]['input_versions'] = {records[0]['artifact_id']: 99}
    elif mutation == 'marker':
        rows[0] = ('TOOL_EVENT', rows[0][1])
    elif mutation == 'reverse_call':
        start = next(e for _,e in rows if e['event_type']=='tool_started')
        end = next(e for _,e in rows if e['event_type']=='tool_call')
        start['event_seq'],end['event_seq'] = end['event_seq'],start['event_seq']
        start['wall_time_utc'],end['wall_time_utc'] = end['wall_time_utc'],start['wall_time_utc']
    elif mutation == 'pii':
        artifact = root / 'workspaces/t0001' / records[0]['path']
        artifact.write_text(json.dumps({'contact': 'person@real-company.test-unreserved'}))
        records[0]['sha256'] = hashlib.sha256(artifact.read_bytes()).hexdigest()
    manifest.write_text(''.join(json.dumps(row)+'\n' for row in records))
    log.write_text(''.join(m+' '+json.dumps(e)+'\n' for m,e in rows))
    assert evaluate_study(root)['metrics'][metric]['status']=='FAIL'


def test_parallel_campaign_inventory_is_complete(tmp_path):
    study = generate_study(tmp_path / 'study', cases=golden_cases()[:3], repetitions=2, workers=3)
    assert len(study['tasks']) == 6
    assert len({t['task_id'] for t in study['tasks']}) == 6
    assert evaluate_study(tmp_path / 'study')['status'] == 'PASS'


@pytest.mark.parametrize('mode',['http_error','missing_message','timeout'])
def test_http_failures_are_redacted_and_classified(mode):
    import time
    canary='do-not-expose-response-content'
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def do_POST(self):
            self.rfile.read(int(self.headers['Content-Length']))
            if mode=='timeout': time.sleep(.15)
            self.send_response(401 if mode=='http_error' else 200)
            self.end_headers()
            try: self.wfile.write(json.dumps({'error':canary}).encode())
            except (BrokenPipeError,ConnectionResetError): pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        client=OpenAICompatibleChatClient(api_key='test-only',base_url=f'http://127.0.0.1:{server.server_port}',timeout=.03)
        with pytest.raises(TimeoutError if mode=='timeout' else RuntimeError) as exc:
            client({'messages':[]})
        assert canary not in str(exc.value)
        assert client.last_usage is None
    finally:
        server.shutdown();server.server_close()


def test_tls_handshake_failure_proves_http_request_was_not_sent(tmp_path):
    import socket
    from evaluation.live import PaidLedger
    listener=socket.socket()
    listener.bind(('127.0.0.1',0));listener.listen(1)
    def close_before_handshake():
        connection,_=listener.accept()
        connection.close();listener.close()
    thread=threading.Thread(target=close_before_handshake,daemon=True);thread.start()
    client=OpenAICompatibleChatClient(api_key='test-only',base_url=f'https://127.0.0.1:{listener.getsockname()[1]}',timeout=1)
    ledger=PaidLedger(tmp_path/'costs.jsonl');number=ledger.begin()
    with pytest.raises(RuntimeError): client({'messages':[]})
    assert client.last_error_metadata['request_not_sent'] is True
    ledger.finish(number,client,{'task_id':'t','run_id':'r'},'RuntimeError')
    assert ledger.spent==0

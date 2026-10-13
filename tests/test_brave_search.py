"""Provider transport doubles exercise decoding and failure/trace contracts, not live availability."""
import json
import pytest


@pytest.mark.parametrize('source,path,payload,expected', [
    ('text', '/web/search', {'web': {'results': [{'title': 'Paper', 'url': 'https://example.org/paper', 'description': 'Abstract'}]}},
     {'title': 'Paper', 'url': 'https://example.org/paper', 'description': 'Abstract'}),
    ('images', '/images/search', {'results': [{'title': 'Figure', 'url': 'https://example.org/article', 'properties': {'url': 'https://example.org/figure.png'}, 'thumbnail': {'src': 'https://example.org/thumb.png'}}]},
     {'title': 'Figure', 'url': 'https://example.org/article', 'description': '', 'image_url': 'https://example.org/figure.png', 'thumbnail_url': 'https://example.org/thumb.png'}),
    ('videos', '/videos/search', {'results': [{'title': 'Talk', 'url': 'https://example.org/video', 'description': 'Conference', 'video': {'duration': '16:33', 'publisher': 'NDSS'}}]},
     {'title': 'Talk', 'url': 'https://example.org/video', 'description': 'Conference', 'video': {'duration': '16:33', 'publisher': 'NDSS'}}),
])
def test_brave_routes_sources_and_returns_real_decoded_fields(monkeypatch, source, path, payload, expected):
    from search_runtime import search_brave
    import requests
    monkeypatch.setenv('BRAVE_SEARCH_API_KEY', 'synthetic-search-token')
    seen = []
    class Response:
        status_code = 200
        def json(self): return payload
    def get(url, **kwargs):
        seen.append((url, kwargs)); return Response()
    monkeypatch.setattr(requests, 'get', get)
    result = search_brave('Chimera & NDSS', source=source, max_results=2)
    assert result['provider'] == 'brave' and result['results'] == [expected]
    assert seen[0][0] == 'https://api.search.brave.com/res/v1' + path
    assert seen[0][1]['params']['q'] == 'Chimera & NDSS'
    assert seen[0][1]['params']['count'] == 2
    assert seen[0][1]['headers']['X-Subscription-Token'] == 'synthetic-search-token'
    assert seen[0][1]['allow_redirects'] is False
    assert 'synthetic-search-token' not in json.dumps(result)


def test_brave_rejects_missing_auth_before_network(monkeypatch):
    from search_runtime import search_brave
    monkeypatch.delenv('BRAVE_SEARCH_API_KEY', raising=False)
    with pytest.raises(RuntimeError, match='BRAVE_SEARCH_API_KEY'):
        search_brave('query')


@pytest.mark.parametrize('arguments', [dict(query=''), dict(query='q', source='google'),
    dict(query='q', max_results=0), dict(query='q', max_results=True), dict(query='q', max_results=21)])
def test_brave_invalid_inputs_cannot_send_billable_requests(arguments):
    from search_runtime import search_brave
    with pytest.raises(ValueError): search_brave(**arguments)


@pytest.mark.parametrize('status', [301, 401, 429, 500])
def test_brave_errors_are_not_success_or_credential_leaks(monkeypatch, status):
    from search_runtime import search_brave
    import requests
    monkeypatch.setenv('BRAVE_SEARCH_API_KEY', 'synthetic-search-token')
    class Response:
        status_code = status
        def json(self): return {'error': 'synthetic-search-token'}
    monkeypatch.setattr(requests, 'get', lambda *a, **k: Response())
    with pytest.raises(RuntimeError) as error: search_brave('q')
    assert str(status) in str(error.value) and 'synthetic-search-token' not in str(error.value)


def test_brave_malformed_payload_is_not_empty_success(monkeypatch):
    from search_runtime import search_brave
    import requests
    monkeypatch.setenv('BRAVE_SEARCH_API_KEY', 'synthetic-search-token')
    class Response:
        status_code = 200
        def json(self): return {'error': 'bad data'}
    monkeypatch.setattr(requests, 'get', lambda *a, **k: Response())
    with pytest.raises(RuntimeError, match='payload'): search_brave('q')


def test_legacy_and_workflow_expose_same_brave_and_record_decoded_results(monkeypatch, tmp_path):
    from base_tools import BaseToolRegistry
    from workflow_runtime import WorkflowToolLoop
    from test_base_tool_workflows import call
    import requests
    monkeypatch.setenv('BRAVE_SEARCH_API_KEY', 'synthetic-search-token')
    class Response:
        status_code = 200
        def json(self): return {'web': {'results': [{'title': 'NDSS', 'url': 'https://example.org/paper', 'description': 'Chimera'}]}}
    monkeypatch.setattr(requests, 'get', lambda *a, **k: Response())
    registry = BaseToolRegistry(tmp_path / 'legacy')
    try:
        names = {s['function']['name'] for s in registry.schemas()}
        assert 'search_google' not in names and 'search_duckduckgo' not in names
        tool = next(t for t in registry.function_tools() if t.get_openai_tool_schema()['function']['name'] == 'search_brave')
        legacy = tool(query='Chimera')
        with pytest.raises(ValueError): registry.execute('search_google', {'query': 'Chimera'})
    finally: registry.close()
    loop = WorkflowToolLoop(tmp_path / 'capture', member_id='m', trace_id='search', base_tools=True)
    replies = iter([call('search_brave', query='Chimera', source='text', max_results=5), call('finish_task', summary='Retrieved'), {'content': 'done'}])
    result = loop.run('Search conference papers', workflow_id='general', chat_fn=lambda r: next(replies))
    assert result.state == 'completed'
    rows = [json.loads(s.split(' ', 1)[1]) for s in loop.log_path.read_text().splitlines()]
    event = next(r for r in rows if r.get('event_type') == 'tool_call' and r.get('tool_name') == 'search_brave')
    assert event['status'] == 'success' and event['result']['payload'] == legacy
    assert 'synthetic-search-token' not in loop.log_path.read_text()

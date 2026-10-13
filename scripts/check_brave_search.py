#!/usr/bin/env python3
"""Check real Brave results through both adapters; no LLM or fallback provider."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from base_tools import BaseToolRegistry
from workflow_runtime import WorkflowToolLoop


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', required=True)
    parser.add_argument('--key-file')
    args = parser.parse_args()
    report = Path(args.report)
    report.mkdir(parents=True, exist_ok=False)
    if args.key_file:
        os.environ['BRAVE_SEARCH_API_KEY'] = Path(args.key_file).read_text().strip()
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in
              map(Path, ['src/search_runtime.py', 'src/base_tools.py', 'src/workflow_runtime.py'])}
    result = {'provider': 'brave', 'status': 'NOT_MEASURED', 'source_sha256': hashes,
              'scope': 'Real provider calls driven by fixed test controls, not model-generated research quality',
              'model_calls': 0, 'provider_calls_upper': 0, 'search_cost_usd_before_free_credits_upper': 0,
              'results': []}
    if not os.getenv('BRAVE_SEARCH_API_KEY', '').strip():
        result['reason'] = 'BRAVE_SEARCH_API_KEY is not configured; no provider request made'
    else:
        queries = {'text': 'Chimera Harnessing Multi-Agent LLMs Insider Threat NDSS',
                   'images': 'red square', 'videos': 'NDSS Chimera insider threat'}
        for source, query in queries.items():
            for route in ('legacy', 'workflow'):
                kwargs = {'query': query, 'source': source, 'max_results': 5}
                record = {'source': source, 'route': route, 'query': query, 'status': 'FAIL'}
                registry = None
                result['provider_calls_upper'] += 1
                try:
                    if route == 'legacy':
                        registry = BaseToolRegistry(report / f'{source}-{route}')
                        tool = next(t for t in registry.function_tools()
                                    if t.get_openai_tool_schema()['function']['name'] == 'search_brave')
                        response = tool(**kwargs)
                    else:
                        loop = WorkflowToolLoop(report / f'{source}-{route}', member_id='search-check',
                                                trace_id=f'{source}-{route}', base_tools=True)
                        replies = iter([
                            {'tool_calls': [{'id': 'search', 'type': 'function', 'function':
                             {'name': 'search_brave', 'arguments': json.dumps(kwargs)}}]},
                            {'tool_calls': [{'id': 'finish', 'type': 'function', 'function':
                             {'name': 'finish_task', 'arguments': json.dumps({'summary': 'Retrieved real search results'})}}]},
                            {'content': 'Search check complete'}])
                        terminal = loop.run('Retrieve public search results', workflow_id='general',
                                            chat_fn=lambda request: next(replies), max_tool_errors=0)
                        if terminal.state != 'completed': raise RuntimeError('workflow did not complete')
                        rows = [json.loads(line.split(' ', 1)[1]) for line in loop.log_path.read_text().splitlines()]
                        response = next(row['result']['payload'] for row in rows
                                        if row.get('event_type') == 'tool_call' and row.get('tool_name') == 'search_brave')
                    record['response'] = response
                    if not response['results']: raise RuntimeError('no real results for validation query')
                    for row in response['results']:
                        url = urlparse(row['url'])
                        if url.scheme not in ('http', 'https') or not url.netloc:
                            raise RuntimeError('result URL is invalid')
                        if source == 'images' and not urlparse(row['image_url']).netloc:
                            raise RuntimeError('image source URL is invalid')
                    record['status'] = 'PASS'
                except Exception as exc:
                    # Runtime/provider errors are deliberately sanitized by adapter.
                    record['exception_type'] = type(exc).__name__
                    record['reason'] = str(exc) if isinstance(exc, RuntimeError) else 'adapter check failed'
                finally:
                    if registry is not None: registry.close()
                result['results'].append(record)
        result['status'] = 'PASS' if all(row['status'] == 'PASS' for row in result['results']) else 'FAIL'
        result['search_cost_usd_before_free_credits_upper'] = result['provider_calls_upper'] * .005
    (report / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'provider_calls_upper', 'search_cost_usd_before_free_credits_upper')}))
    return 0 if result['status'] == 'PASS' else 2


if __name__ == '__main__':
    raise SystemExit(main())

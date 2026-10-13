"""DeepSeek-only paid boundary, with conservative reservations and append-only ledger."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import threading

from task import OpenAICompatibleChatClient
from evaluation.campaign import ScriptedEmployee

# Official peak USD / million tokens, checked 2026-10-12.
PRICING_URL = 'https://api-docs.deepseek.com/quick_start/pricing'
INPUT_MISS, INPUT_HIT, OUTPUT = .30, .006, 1.20
CONTEXT_LIMIT, OUTPUT_LIMIT = 1_000_000, 4096
REQUEST_RESERVE = (CONTEXT_LIMIT * INPUT_MISS + OUTPUT_LIMIT * OUTPUT) / 1_000_000


class PaidLedger:
    def __init__(self, path, budget_usd=5., max_calls=1200):
        self.path = Path(path)
        self.path.touch(exist_ok=False)
        self.budget = budget_usd
        self.max_calls = max_calls
        self.spent = self.reserved = 0.
        self.calls = 0
        self.lock = threading.Lock()

    def begin(self, context=None):
        with self.lock:
            if self.calls >= self.max_calls or self.spent + self.reserved + REQUEST_RESERVE > self.budget:
                raise RuntimeError('paid campaign budget/call limit reached')
            self.reserved += REQUEST_RESERVE
            self.calls += 1
            self._append({"record_type":"started", "request_number":self.calls,
                "recorded_at":datetime.now(timezone.utc).isoformat(), "context":context,
                "reserved_usd_upper":REQUEST_RESERVE})
            return self.calls

    def _append(self, row):
        with self.path.open('a') as handle:
            handle.write(json.dumps(row) + '\n')
            handle.flush()
            os.fsync(handle.fileno())

    def finish(self, number, client, context, error):
        usage = client.last_usage
        valid = isinstance(usage, dict) and all(type(usage.get(k)) is int and usage[k] >= 0
            for k in ('prompt_tokens','completion_tokens'))
        valid = valid and usage['prompt_tokens'] <= CONTEXT_LIMIT and usage['completion_tokens'] <= OUTPUT_LIMIT
        if valid:
            hit_value = usage.get('prompt_cache_hit_tokens',0)
            miss_value = usage.get('prompt_cache_miss_tokens',usage['prompt_tokens']-hit_value) if type(hit_value) is int else None
            valid = type(hit_value) is int and type(miss_value) is int and hit_value >= 0 and miss_value >= 0 and hit_value + miss_value == usage['prompt_tokens']
        hit = usage.get('prompt_cache_hit_tokens', 0) if valid else 0
        miss = usage.get('prompt_cache_miss_tokens', usage['prompt_tokens'] - hit) if valid else 0
        known_model = client.last_model in {'deepseek-flash', 'deepseek-v4-flash', 'deepseek-v4.1-flash'}
        cost = (hit * INPUT_HIT + miss * INPUT_MISS + usage['completion_tokens'] * OUTPUT) / 1e6 if valid and known_model else REQUEST_RESERVE
        if (getattr(client,'last_error_metadata',None) or {}).get('request_not_sent') is True:
            cost = 0.
        row = {'record_type':'terminal', 'request_number': number, 'task_id': context['task_id'], 'run_id': context['run_id'],
               'recorded_at': datetime.now(timezone.utc).isoformat(), 'requested_model': client.model,
               'returned_model': client.last_model, 'provider_request_id': client.last_request_id,
               'finish_reason': client.last_finish_reason, 'usage': usage,
               'exception_type': error, 'error_metadata':getattr(client,'last_error_metadata',None), 'cost_usd_peak_upper': cost,
               'usage_pricing_known': valid and known_model, 'pricing_source': PRICING_URL}
        with self.lock:
            self.reserved -= REQUEST_RESERVE
            self.spent += cost
            self._append(row)


class LiveEmployee:
    supports_images = True
    def __init__(self, case, context, api_key, ledger):
        self.client = OpenAICompatibleChatClient(api_key=api_key, base_url='https://api.deepseek.com',
            model='deepseek-flash', thinking=False, max_tokens=OUTPUT_LIMIT, timeout=90)
        self.case, self.context, self.ledger = case, context, ledger
        self.step = 0
        self.scripted = ScriptedEmployee(case)
        self.last_usage = self.last_model = None
        self.model = self.client.model

    def __call__(self, request):
        number = self.ledger.begin(self.context)
        error = None
        try:
            message = self.client(request)
        except Exception as exc:
            error = type(exc).__name__
            raise
        finally:
            self.last_usage, self.last_model = self.client.last_usage, self.client.last_model
            self.ledger.finish(number, self.client, self.context, error)
        # Only controlled failure cases inject model-boundary responses; real paid
        # request and returned usage remain recorded. No natural-attack claim.
        if self.case['variant'] in {6, 7, 8}:
            message = self.scripted(request)
        self.step += 1
        return message

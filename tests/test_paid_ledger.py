from types import SimpleNamespace
import json
import pytest
from evaluation.live import PaidLedger, REQUEST_RESERVE


def test_usage_cost_and_unknown_reservation_are_both_retained(tmp_path):
    ledger = PaidLedger(tmp_path/'costs.jsonl', budget_usd=1.)
    client = SimpleNamespace(model='deepseek-flash', last_model='deepseek-flash', last_request_id='r',
        last_finish_reason='stop', last_usage={'prompt_tokens':1000, 'prompt_cache_hit_tokens':500, 'completion_tokens':100})
    n=ledger.begin()
    ledger.finish(n, client, {'task_id':'t','run_id':'r'}, None)
    assert ledger.spent == pytest.approx(.000273)
    client.last_usage=None
    n=ledger.begin()
    ledger.finish(n, client, {'task_id':'t','run_id':'r'}, 'TimeoutError')
    assert ledger.spent == pytest.approx(.000273 + REQUEST_RESERVE)
    rows=[json.loads(r) for r in ledger.path.read_text().splitlines() if json.loads(r).get('record_type')=='terminal']
    assert rows[0]['usage_pricing_known'] and not rows[1]['usage_pricing_known']
    with pytest.raises(FileExistsError):
        PaidLedger(ledger.path)


def test_conservative_budget_prevents_call_before_sending(tmp_path):
    ledger=PaidLedger(tmp_path/'costs.jsonl', budget_usd=REQUEST_RESERVE * 1.5)
    ledger.begin()
    with pytest.raises(RuntimeError, match='budget'):
        ledger.begin()
    assert ledger.calls==1

@pytest.mark.parametrize('usage',[{'prompt_tokens':1,'completion_tokens':-1000000},
    {'prompt_tokens':10,'completion_tokens':2,'prompt_cache_hit_tokens':11},
    {'prompt_tokens':True,'completion_tokens':2},
    {'prompt_tokens':10,'completion_tokens':2,'prompt_cache_hit_tokens':4,'prompt_cache_miss_tokens':9}])
def test_invalid_usage_cannot_refund_reservation(tmp_path,usage):
    ledger=PaidLedger(tmp_path/'costs.jsonl')
    client=SimpleNamespace(model='deepseek-flash',last_model='deepseek-flash',last_request_id='r',last_finish_reason='stop',last_usage=usage)
    number=ledger.begin()
    ledger.finish(number,client,{'task_id':'t','run_id':'r'},None)
    assert ledger.spent==REQUEST_RESERVE


def test_request_start_is_durable_before_provider_call(tmp_path):
    ledger=PaidLedger(tmp_path/'costs.jsonl')
    number=ledger.begin({'task_id':'t','run_id':'r'})
    row=json.loads(ledger.path.read_text().splitlines()[0])
    assert row['record_type']=='started' and row['request_number']==number
    assert row['reserved_usd_upper']==REQUEST_RESERVE

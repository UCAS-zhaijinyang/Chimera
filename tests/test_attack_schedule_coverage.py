import json
import pytest


def test_attack_prompt_preserves_all_steps(monkeypatch):
    import daily_attack_schedule as module
    seen = {}
    def respond(system, user, **kw):
        seen['user'] = user
        return '[]'
    monkeypatch.setattr(module, 'run_llm', respond)
    info = {'attack_id': 'multi', 'how': [{'step': i, 'description': f'unique-step-{i}'} for i in range(1, 6)]}
    module.attack_daily_schedule_with_gpt([], {'name': 'x', 'role': 'r'}, info, {})
    assert 'unique-step-5' in seen['user']


def test_schedule_rejects_missing_attack_steps():
    from daily_attack_schedule import validate_attack_schedule
    info = {'how': [{'step': 1}, {'step': 2}, {'step': 3}]}
    with pytest.raises(ValueError):
        validate_attack_schedule([{'Time': '10:00:00', 'Activity': 'act', 'Attack': True, 'AttackSteps': [1, 2]}], info)


def test_schedule_accepts_complete_ordered_steps_and_after_hours():
    from daily_attack_schedule import validate_attack_schedule
    info = {'how': [{'step': 1}, {'step': 2}, {'step': 3}], 'when': {'time_window': 'after hours'}}
    validate_attack_schedule([{'Time': '18:15:00', 'Activity': 'steps 1-2', 'Attack': True, 'AttackSteps': [1, 2]},
                             {'Time': '18:45:00', 'Activity': 'step 3', 'Attack': True, 'AttackSteps': [3]}], info)


def test_schedule_rejects_empty_and_unsorted_records():
    from daily_attack_schedule import validate_attack_schedule
    info = {'how': [{'step': 1}]}
    for rows in [[], [{'Time': '18:00:00', 'Activity': 'x', 'Attack': True, 'AttackSteps': [1]},
                     {'Time': '10:00:00', 'Activity': 'x'}]]:
        with pytest.raises(ValueError): validate_attack_schedule(rows, info)


def test_validated_schedule_binds_canonical_how_to_execution_text():
    from daily_attack_schedule import validate_attack_schedule
    info={'attack_id':'example','how':[{'step':1,'description':'original operation one'}, {'step':2,'description':'original operation two'}]}
    row={'Time':'18:15:00','Activity':'Take lunch','Attack':True,'AttackSteps':[1,2]}
    schedule=validate_attack_schedule([row],info)
    assert all(s['description'] in schedule[0]['Activity'] for s in info['how'])
    assert schedule[0]['AttackRequirements']==info['how']
    assert validate_attack_schedule(schedule,info)[0]['Activity'].count('original operation one')==1

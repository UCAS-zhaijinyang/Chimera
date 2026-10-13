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


def _campaign_inputs():
    normal = {
        'week_1_Monday': [{'Time': '10:00:00', 'Activity': 'normal monday'}],
        'week_1_Tuesday': [{'Time': '10:00:00', 'Activity': 'normal tuesday'}],
        'week_1_Wednesday': [{'Time': '10:00:00', 'Activity': 'normal wednesday'}],
    }
    attack = {
        'attack_id': 'multi_day',
        'how': [
            {'step': 1, 'description': 'first attack action'},
            {'step': 2, 'description': 'second attack action'},
            {'step': 3, 'description': 'third attack action'},
        ],
    }
    return normal, attack


def test_campaign_planner_accepts_llm_selected_multiple_days(monkeypatch):
    from attack_schedule import plan_attack_campaign_with_gpt

    normal, attack = _campaign_inputs()
    monkeypatch.setattr(
        'attack_schedule.run_llm',
        lambda *args, **kwargs: (
            '{"days": ['
            '{"date": "week_1_Monday", "attack_steps": [1], "purpose": "access"},'
            '{"date": "week_1_Tuesday", "attack_steps": [2, 3], "purpose": "impact"}'
            ']}'
        ),
    )

    plan = plan_attack_campaign_with_gpt(
        normal, {'name': 'A', 'role': 'developer'}, attack, {}
    )

    assert [day['date'] for day in plan['days']] == [
        'week_1_Monday', 'week_1_Tuesday'
    ]
    assert plan['days'][1]['attack_steps'] == [2, 3]
    assert plan['raw_llm_output'].startswith('{"days"')


def test_campaign_plan_rejects_missing_or_duplicate_attack_steps():
    from attack_schedule import validate_campaign_plan

    normal, attack = _campaign_inputs()
    with pytest.raises(ValueError, match='cover every specified step'):
        validate_campaign_plan(
            {'days': [
                {'date': 'week_1_Monday', 'attack_steps': [1]},
                {'date': 'week_1_Tuesday', 'attack_steps': [1, 2]},
            ]},
            normal,
            attack,
        )


def test_campaign_application_preserves_unselected_normal_days(tmp_path, monkeypatch):
    from attack_schedule import apply_campaign_plan

    normal, attack = _campaign_inputs()
    plan = {
        'attack_id': attack['attack_id'],
        'days': [
            {'date': 'week_1_Monday', 'attack_steps': [1]},
            {'date': 'week_1_Tuesday', 'attack_steps': [2, 3]},
        ],
        'raw_llm_output': 'raw-plan',
    }

    def fake_generator(initial, member_profile, attack_info, id_role_map):
        return initial + [
            {'Time': '18:00:00', 'Activity': 'injected', 'Attack': True,
             'AttackSteps': [row['step'] for row in attack_info['how']]}
        ]

    monkeypatch.setattr('attack_schedule.generate_attack_schedule', fake_generator)
    manifest = apply_campaign_plan(
        normal,
        plan,
        'member-1',
        attack['attack_id'],
        {},
        output_dir=tmp_path,
        member_profile={'name': 'A', 'role': 'developer'},
        attack_info=attack,
    )

    assert manifest['selected_dates'] == ['week_1_Monday', 'week_1_Tuesday']
    assert manifest['days']['week_1_Wednesday']['modified_schedule'] == normal['week_1_Wednesday']
    assert (tmp_path / 'member-1_week_1_Monday_attack.json').exists()
    assert (tmp_path / 'member-1_week_1_Tuesday_attack.json').exists()
    assert not (tmp_path / 'member-1_week_1_Wednesday_attack.json').exists()


def test_campaign_application_is_atomic_when_a_selected_day_fails(tmp_path, monkeypatch):
    from attack_schedule import apply_campaign_plan

    normal, attack = _campaign_inputs()
    plan = {
        'attack_id': attack['attack_id'],
        'days': [
            {'date': 'week_1_Monday', 'attack_steps': [1]},
            {'date': 'week_1_Tuesday', 'attack_steps': [2, 3]},
        ],
    }
    calls = {'count': 0}

    def failing_generator(initial, member_profile, attack_info, id_role_map):
        calls['count'] += 1
        if calls['count'] == 2:
            raise RuntimeError('simulated LLM failure')
        return initial

    monkeypatch.setattr('attack_schedule.generate_attack_schedule', failing_generator)
    with pytest.raises(RuntimeError, match='simulated LLM failure'):
        apply_campaign_plan(
            normal,
            plan,
            'member-1',
            attack['attack_id'],
            {},
            output_dir=tmp_path,
            member_profile={'name': 'A', 'role': 'developer'},
            attack_info=attack,
        )

    assert list(tmp_path.iterdir()) == []


def test_campaign_bundle_can_be_reused_for_later_daily_runs(tmp_path):
    from attack_schedule import (
        load_campaign_bundle,
        restore_campaign_files,
        write_campaign_bundle,
    )

    modified = [{'Time': '18:00:00', 'Activity': 'injected', 'Attack': True,
                 'AttackSteps': [1]}]
    bundle = {
        'member-1': {
            'selected_dates': ['week_1_Monday'],
            'days': {'week_1_Monday': {'modified_schedule': modified}},
        }
    }
    bundle_path = tmp_path / 'campaign_bundle.json'
    write_campaign_bundle(bundle, bundle_path)
    loaded = load_campaign_bundle(bundle_path)
    output_dir = tmp_path / 'attack_schedule'
    paths = restore_campaign_files(loaded, output_dir=output_dir)

    assert paths == [str(output_dir / 'member-1_week_1_Monday_attack.json')]
    assert json.loads((output_dir / 'member-1_week_1_Monday_attack.json').read_text()) == modified

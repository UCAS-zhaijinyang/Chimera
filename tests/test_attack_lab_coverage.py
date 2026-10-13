import json
from pathlib import Path
import pytest


@pytest.mark.parametrize('attack_id', [f'gen_attack_{i}' for i in range(1,13)] + [f'multi_attack_{i}' for i in range(1,4)])
def test_all_original_steps_have_real_lab_side_effects(tmp_path, attack_id):
    from evaluation.attack_lab import AttackLab, evaluate_lab
    from workflow_runtime import WorkflowToolLoop
    from test_base_tool_workflows import call
    cases = json.loads(Path('docs/dataset-evaluation/controlled-attack-cases.json').read_text())['cases']
    original = json.loads((Path('docs/dataset-evaluation/evidence/original-attack-specs') / (attack_id+'.json')).read_text())
    assert len(cases[attack_id]) == len(original['how'])
    with AttackLab(tmp_path / 'business') as lab:
        for index, operation in enumerate(cases[attack_id]):
            loop = WorkflowToolLoop(tmp_path / f'capture-{index}', member_id='m', trace_id=f't-{index}',
                                    base_tools=True, business_workspace=lab.workspace, offline=False)
            command = lab.command(operation)
            initial = call('browse_url', **lab.browser_task(operation)) if operation in {'collect_form_input','browse_competitor'} else call('shell_exec', id='step', command=command)
            replies = iter([initial,
                            call('finish_task', summary='checked'), {'content':'done'}])
            def employee(request):
                if request.get('workflow_id') != 'browser': return next(replies)
                last = json.loads(request['messages'][-1]['content'])['last_action']
                if operation=='browse_competitor':
                    return call('browser_action', action='click', selector='text=Jobs', value='', url='') if last is None else {'content':'Jobs read'}
                if last is None: return call('browser_action', action='fill', selector='#account', value='employee', url='')
                if last['selector']=='#account':return call('browser_action', action='fill', selector='#password', value='synthetic-shared-password', url='')
                if last['selector']=='#password':return call('browser_action', action='click', selector='#submit', value='', url='')
                return {'content':'Submitted'}
            result = loop.run(original['how'][index]['description'], workflow_id='general', chat_fn=employee)
            assert result.state == 'completed'
            report = evaluate_lab(lab.workspace, [operation])
            assert report['status'] == 'PASS', report


def test_attack_oracle_rejects_claim_without_file_transfer(tmp_path):
    from evaluation.attack_lab import AttackLab, evaluate_lab
    with AttackLab(tmp_path) as lab:
        (tmp_path / 'claimed-result.json').write_text(json.dumps({'success':True,'operation':'upload_files'}))
        assert evaluate_lab(tmp_path, ['upload_files'])['status'] == 'FAIL'


def test_trace_oracle_rejects_a_skipped_step_even_if_later_step_makes_files(tmp_path):
    from evaluation.attack_lab import AttackLab,evaluate_lab,evaluate_trace_steps
    from workflow_runtime import WorkflowToolLoop
    from test_base_tool_workflows import call
    ops=['scan_lab_endpoint','credential_login','collect_files','archive_upload']
    with AttackLab(tmp_path/'business') as lab:
        concrete=[{'step':i+1,'operation':op,'tool':'shell_exec','arguments':lab.command(op)} for i,op in enumerate(ops)]
        replies=iter([*[call('shell_exec',id=str(i),command=lab.command(op)) for i,op in enumerate(ops) if op!='collect_files'],
                      call('finish_task',summary='done'),{'content':'done'}])
        loop=WorkflowToolLoop(tmp_path/'capture',member_id='m',trace_id='t',base_tools=True,business_workspace=lab.workspace,offline=True)
        loop.run('Operate',workflow_id='general',chat_fn=lambda r:next(replies))
        assert evaluate_lab(lab.workspace,ops)['status']=='PASS'
        events=[json.loads(s.split(' ',1)[1]) for s in loop.log_path.read_text().splitlines()]
        assert evaluate_trace_steps(concrete,events)['status']=='FAIL'


def test_trace_oracle_accepts_only_equivalent_explicit_business_cwd(tmp_path):
    import shlex
    from evaluation.attack_lab import evaluate_trace_steps
    command='python lab_actions.py collect_files'
    concrete=[{'step':1,'operation':'collect_files','tool':'shell_exec','arguments':command,'business_workspace':str(tmp_path)}]
    def event(actual):return [{'event_type':'tool_call','tool_name':'shell_exec','status':'success','call_id':'c1','arguments':{'id':'s','command':actual}}]
    assert evaluate_trace_steps(concrete,event('cd '+shlex.quote(str(tmp_path))+' && '+command))['status']=='PASS'
    assert evaluate_trace_steps(concrete,event('cd /wrong && '+command))['status']=='FAIL'
    assert evaluate_trace_steps(concrete,event(command+'; echo forged'))['status']=='FAIL'

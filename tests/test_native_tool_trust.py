import json
from test_base_tool_workflows import call


def generate_native_study(tmp_path):
    from workflow_runtime import WorkflowToolLoop
    from evaluation.campaign import OBSERVABLE_FIELDS
    context={'run_id':'r','task_id':'t','trace_id':'t','member_id':'m'}
    workspace=tmp_path/'workspaces/t'
    loop=WorkflowToolLoop(workspace,member_id='m',trace_id='t',context=context,base_tools=True,offline=True)
    replies=iter([call('shell_exec',id='s',command='printf native'),call('finish_task',summary='checked'),{'content':'done'}])
    loop.run('Operate resources',workflow_id='general',chat_fn=lambda r:next(replies))
    events=[json.loads(s.split(' ',1)[1]) for s in loop.log_path.read_text().splitlines()]
    (tmp_path/'release').mkdir()
    (tmp_path/'release/events.jsonl').write_text(''.join(json.dumps({k:v for k,v in e.items() if k in OBSERVABLE_FIELDS})+'\n' for e in events))
    (tmp_path/'study_manifest.json').write_text(json.dumps({'schema_version':1,'members':['m'],
        'tasks':[{**context,'workspace':'workspaces/t','log_files':['workspaces/t/execution.log']}],
        'planned_activities':[],'attack_truth':[],'release_files':['release/events.jsonl']}))
    return workspace


def test_native_observation_lineage_is_explained_and_complete(tmp_path):
    from evaluation.trust import evaluate_study
    generate_native_study(tmp_path)
    report=evaluate_study(tmp_path)
    assert report['status']=='PASS', report['failures']


def test_dropped_completion_dependency_fails_independent_oracle(tmp_path):
    from evaluation.trust import evaluate_study
    workspace=generate_native_study(tmp_path)
    manifest=workspace/'manifest.jsonl'
    rows=[json.loads(s) for s in manifest.read_text().splitlines()]
    for row in rows:
        if row['producer_tool']=='finish_task':
            row['inputs']=[];row['root_type']='standalone_generated_input';row['input_versions']={}
    manifest.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    assert evaluate_study(tmp_path)['metrics']['L0.4']['status']=='FAIL'

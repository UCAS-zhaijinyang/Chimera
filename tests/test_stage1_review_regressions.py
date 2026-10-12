import json
from pathlib import Path
import pytest
from evaluation.campaign import generate_study, golden_cases
from evaluation.trust import evaluate_study
from workflow_runtime import FilesystemToolRuntime


def setup(root):
    generate_study(root,cases=golden_cases()[:1],repetitions=1)
    log=root/'workspaces/t0001/execution.log'
    rows=[(s.split(' ',1)[0],json.loads(s.split(' ',1)[1])) for s in log.read_text().splitlines()]
    return log,rows


@pytest.mark.parametrize('mutation', ['task_null','seq_string','inputs_null','id_list','workspace_null'])
def test_malformed_inputs_return_detailed_failure_instead_of_crash(tmp_path,mutation):
    root=tmp_path/'study';log,rows=setup(root)
    p=root/'study_manifest.json';study=json.loads(p.read_text())
    if mutation=='task_null': study['tasks']=[None]
    elif mutation=='workspace_null': study['tasks'][0]['workspace']=None
    elif mutation=='seq_string': rows[0][1]['event_seq']='1'
    elif mutation=='id_list': rows[0][1]['event_id']=[]
    elif mutation=='inputs_null':
        mp=root/'workspaces/t0001/manifest.jsonl'
        records=[json.loads(s) for s in mp.read_text().splitlines()]
        records[1]['inputs']=None
        mp.write_text(''.join(json.dumps(r)+'\n' for r in records))
    p.write_text(json.dumps(study))
    log.write_text(''.join(m+' '+json.dumps(e)+'\n' for m,e in rows))
    report=evaluate_study(root)
    assert report['status']=='FAIL' and report['failures']


@pytest.mark.parametrize('mutation,metric', [('outside_task','L0.5'),('event_phase','L0.2'),('missing_arguments','L0.4'),('empty_release','L0.8')])
def test_review_false_pass_paths(tmp_path,mutation,metric):
    root=tmp_path/'study';log,rows=setup(root)
    if mutation=='outside_task':
        final=rows.pop();rows.insert(1,final)
        for seq,(_,event) in enumerate(rows,1):
            event['event_seq']=seq
            event['wall_time_utc']=f'2026-10-12T00:00:{seq:02d}+00:00'
            event['simulation_time']=f'2025-05-05T09:00:{seq:02d}+08:00'
    elif mutation=='event_phase':
        for _,e in rows: e.update(phase_id='wrong',workday=99)
    elif mutation=='missing_arguments':
        call=next(e for _,e in rows if e.get('tool_name')=='data_transform' and e['event_type']=='tool_call')
        call.pop('arguments')
        mp=root/'workspaces/t0001/manifest.jsonl'
        records=[json.loads(s) for s in mp.read_text().splitlines()]
        records[1].update(inputs=[],input_versions={},root_type='standalone_generated_input')
        mp.write_text(''.join(json.dumps(r)+'\n' for r in records))
    else: (root/'release/events.jsonl').write_text('')
    log.write_text(''.join(m+' '+json.dumps(e)+'\n' for m,e in rows))
    assert evaluate_study(root)['metrics'][metric]['status']=='FAIL'


def test_code_edit_cannot_overwrite_capture_evidence(tmp_path):
    runtime=FilesystemToolRuntime(tmp_path,member_id='m',trace_id='t')
    original=runtime.execute('source_query',{'query':'fixture'})
    artifact_id=original['output_artifact_ids'][0]
    record=next(json.loads(s) for s in (tmp_path/'manifest.jsonl').read_text().splitlines())
    before=(tmp_path/record['path']).read_bytes()
    with pytest.raises(PermissionError):
        runtime.execute('code_edit',{'path':record['path'],'content':'overwritten'})
    assert (tmp_path/record['path']).read_bytes()==before
    for path in ['execution.log','manifest.jsonl']:
        with pytest.raises(PermissionError): runtime.execute('code_edit',{'path':path,'content':'overwrite'})


def test_manifest_symlink_cannot_read_outside_study(tmp_path):
    root=tmp_path/'study';setup(root)
    manifest=root/'workspaces/t0001/manifest.jsonl'
    outside=tmp_path/'outside.jsonl'
    manifest.rename(outside)
    manifest.symlink_to(outside)
    assert evaluate_study(root)['status']=='FAIL'


def test_disjoint_task_prefix_preserves_plans_and_event_joins(tmp_path):
    a=generate_study(tmp_path/'a',cases=golden_cases()[:1],repetitions=1,task_prefix='a-')
    b=generate_study(tmp_path/'b',cases=golden_cases()[:1],repetitions=1,task_prefix='b-')
    assert a['tasks'][0]['task_id']!=b['tasks'][0]['task_id']
    assert a['planned_activities'][0]['id']!=b['planned_activities'][0]['id']
    assert evaluate_study(tmp_path/'a')['status']==evaluate_study(tmp_path/'b')['status']=='PASS'


def test_batch_merge_preserves_failed_tasks_and_rejects_identity_collision(tmp_path):
    import importlib.util
    script=Path(__file__).resolve().parents[1]/'scripts/combine_trust_studies.py'
    spec=importlib.util.spec_from_file_location('combine_trust_studies',script)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    sources=[]
    for name in ['a','b']:
        source=tmp_path/name
        generate_study(source,cases=[golden_cases()[6]],repetitions=1,task_prefix=name+'-')
        (source/'costs.jsonl').write_text('')
        sources.append(source)
    result,_=module.combine_studies(sources,tmp_path/'combined')
    assert len(result['tasks'])==2 and all(r['exception'] for r in result['execution_results'])
    assert evaluate_study(tmp_path/'combined')['status']=='PASS'
    with pytest.raises(ValueError,match='disjoint'):
        module.combine_studies([sources[0],sources[0]],tmp_path/'collision')
    assert not (tmp_path/'collision').exists()

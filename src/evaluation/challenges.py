"""Mutation controls are evaluator tests, never natural quality observations."""
import json
from pathlib import Path
from evaluation.campaign import generate_study, golden_cases
from evaluation.trust import evaluate_study, write_report

FAULTS = {'field':'L0.1', 'json':'L0.1', 'marker':'L0.1', 'member':'L0.2', 'identity':'L0.2',
          'terminal':'L0.3', 'missing_log':'L0.3', 'hash':'L0.4', 'input':'L0.4',
          'version':'L0.4', 'concealed':'L0.4', 'cycle':'L0.4', 'time':'L0.5',
          'label_evidence':'L0.6', 'output':'L0.7', 'credential':'L0.8',
          'label_field':'L0.8', 'label_path':'L0.8', 'pii':'L0.8',
          'empty_release':'L0.8', 'outside_task':'L0.5', 'phase':'L0.2',
          'malformed_task':'L0.1', 'malformed_sequence':'L0.1', 'malformed_inputs':'L0.4'}


def mutate(root, fault):
    root=Path(root)
    manifest_path=root/'study_manifest.json'
    study=json.loads(manifest_path.read_text())
    task=study['tasks'][0]
    workspace=root/task['workspace']
    log=workspace/'execution.log'
    rows=[(line.split(' ',1)[0],json.loads(line.split(' ',1)[1])) for line in log.read_text().splitlines()]
    records_path=workspace/'manifest.jsonl'
    records=[json.loads(line) for line in records_path.read_text().splitlines()]
    call=next(e for _,e in rows if e['event_type']=='tool_call')
    if fault=='empty_release': (root/study['release_files'][0]).write_text('')
    elif fault=='phase':
        for _,e in rows: e.update(phase_id='wrong',workday=99)
    elif fault=='outside_task':
        final=rows.pop();rows.insert(1,final)
        for seq,(_,e) in enumerate(rows,1):
            e['event_seq']=seq
            e['wall_time_utc']=f'2026-10-12T00:00:{seq:02d}+00:00'
            e['simulation_time']=f'2025-05-05T09:00:{seq:02d}+08:00'
    elif fault=='malformed_task': study['tasks']=[None]
    elif fault=='malformed_sequence': rows[0][1]['event_seq']='bad-sequence'
    elif fault=='malformed_inputs': records[1]['inputs']=None
    elif fault=='field': del call['event_id']
    elif fault=='marker': rows[0]=('TOOL_EVENT',rows[0][1])
    elif fault=='member': call['member_id']='not-in-roster'
    elif fault=='identity': rows.append(('TOOL_EVENT',dict(call,status='failed')))
    elif fault=='terminal': rows=[(m,e) for m,e in rows if e['event_type']!='final_answer']
    elif fault=='hash': (workspace/records[0]['path']).write_text('tampered')
    elif fault=='input': records[1]['inputs']=['missing-input']
    elif fault=='version': records[1]['input_versions']={records[0]['artifact_id']:99}
    elif fault=='concealed': records[1].update(inputs=[], root_type='standalone_generated_input')
    elif fault=='cycle': records[0].update(inputs=[records[1]['artifact_id']],input_versions={records[1]['artifact_id']:1})
    elif fault=='time': call['wall_time_utc']='2000-01-01T00:00:00+00:00'
    elif fault=='label_evidence':
        study['attack_truth']=[{'episode_id':'mutation-only','task_id':task['task_id'],'positive':True,
            'scope':'simulation_only','label_type':'succeeded','tool_name':'message_send',
            'target':{'to':['outside@example.invalid']},'evidence_call_ids':['nonexistent']}]
    elif fault=='output': call['result']['output_artifact_ids']=['missing-output']
    elif fault=='credential': (workspace/records[0]['path']).write_text(json.dumps({'key':'sk-'+'synthetic'*5}))
    elif fault=='pii': (workspace/records[0]['path']).write_text(json.dumps({'contact':'person@company-unreserved.org'}))
    elif fault=='label_field':
        path=root/study['release_files'][0]
        with path.open('a') as handle: handle.write(json.dumps({'attack_label':True})+'\n')
    elif fault=='label_path':
        old=root/study['release_files'][0]
        new=old.with_name('attack-events.jsonl')
        old.rename(new)
        study['release_files']=[str(new.relative_to(root))]
    log.write_text(''.join(marker+' '+json.dumps(event)+'\n' for marker,event in rows))
    if fault=='json':
        with log.open('a') as handle: handle.write('TOOL_EVENT {corrupt\n')
    if fault=='missing_log': log.unlink()
    records_path.write_text(''.join(json.dumps(record)+'\n' for record in records))
    study['challenge']={'class':fault, 'expected_metric':FAULTS[fault], 'excluded_from_natural_quality':True}
    manifest_path.write_text(json.dumps(study,indent=2)+'\n')


def run_challenges(scratch, reports):
    scratch,reports=Path(scratch),Path(reports)
    scratch.mkdir(parents=True,exist_ok=False)
    reports.mkdir(parents=True,exist_ok=False)
    results=[]
    cases=golden_cases()
    for repeat,index in enumerate((0,10,20)):
        for fault,metric in [('normal',None),*FAULTS.items()]:
            name=f'{fault}-{repeat+1}'
            root=scratch/name
            generate_study(root,cases=[cases[index]],repetitions=1)
            if metric: mutate(root,fault)
            report=evaluate_study(root)
            write_report(root,reports/name,report)
            detected=report['metrics'][metric]['status']=='FAIL' if metric else report['status']=='PASS'
            results.append({'challenge':name,'primary_metric':metric,'expected':'FAIL' if metric else 'PASS',
                            'actual':report['status'],'detected_or_control_clean':detected,
                            'report':name+'/report.json'})
    summary={'status':'PASS' if all(r['detected_or_control_clean'] for r in results) else 'FAIL',
        'fault_classes':len(FAULTS),'replicates_per_class':3, 'mutant_count':len(FAULTS)*3,
        'detected_mutants':sum(r['detected_or_control_clean'] for r in results if r['primary_metric']),
        'normal_controls':3,'false_positives':sum(not r['detected_or_control_clean'] for r in results if not r['primary_metric']),
        'scope':'known injected faults only; mutants excluded from natural-quality denominators','results':results}
    (reports/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

#!/usr/bin/env python3
"""Immutable Stage 1 native-tool/15-class synthetic-lab campaign.

This is a correctness campaign with explicit executable specifications, not
a natural-attack-quality study or either final comparative dataset.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys
import uuid
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evaluation.attack_lab import AttackLab,evaluate_lab,evaluate_trace_steps
from evaluation.campaign import OBSERVABLE_FIELDS
from evaluation.trust import evaluate_study,write_report,read_marked
from workflow_runtime import WorkflowToolLoop


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['offline','live'],required=True)
    parser.add_argument('--study',required=True);parser.add_argument('--report',required=True)
    parser.add_argument('--key-file');parser.add_argument('--budget-usd',type=float,default=5)
    parser.add_argument('--repetitions',type=int,default=3)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args()
    if Path(args.report).exists():parser.error('report already exists')
    root=Path(args.study).resolve();root.mkdir(exist_ok=False,parents=True)
    original=Path('docs/dataset-evaluation/evidence/original-attack-specs')
    inventory=json.loads(Path('docs/dataset-evaluation/controlled-attack-cases.json').read_text())
    provenance={'mode':args.mode,'repetitions':args.repetitions,'source_sha256':{
        str(p):hashlib.sha256(p.read_bytes()).hexdigest() for base in [Path('src'),Path('scripts')]
        for p in sorted(base.rglob('*.py'))},'fixture_spec':inventory,
        'scope':'specified synthetic mechanisms; not natural attack quality'}
    (root/'runner-start.json').write_text(json.dumps(provenance,indent=2)+'\n')
    ledger=None
    if args.mode=='live':
        if not args.key_file:parser.error('live requires private key file')
        from evaluation.live import PaidLedger,LiveEmployee
        key=Path(args.key_file).read_text().strip();ledger=PaidLedger(root/'costs.jsonl',args.budget_usd)
    study={'schema_version':1,'members':['employee'],'tasks':[],'planned_activities':[],
        'attack_truth':[],'release_files':['release/events.jsonl'],
        'capabilities':{'application':True,'system':False,'network':False,'real_email':False},
        'scope':'controlled local browser/process/files/application; no real enterprise attack claim'}
    run_id='native-'+uuid.uuid4().hex
    results=[]
    def run_one(job):
        repetition,index,attack_id,operations=job
        task_id=f'case-{repetition}-{index:02d}'
        spec=json.loads((original/(attack_id+'.json')).read_text())
        if len(spec['how'])!=len(operations):raise ValueError('original step inventory mismatch')
        context={'run_id':run_id,'task_id':task_id,'trace_id':task_id,'member_id':'employee',
            'planned_activity_id':task_id+'-plan','phase_id':'phase1','workday':repetition+1,
            'simulation_time':(datetime(2025,5,5,18,15,tzinfo=timezone(timedelta(hours=8)))+timedelta(days=repetition)).isoformat()}
        workspace=root/'workspaces'/task_id
        failure=None;state=None
        with AttackLab(root/'business'/task_id) as lab:
            concrete=[]
            for step,operation in zip(spec['how'],operations):
                action=lab.browser_task(operation) if operation in {'collect_form_input','browse_competitor'} else lab.command(operation)
                concrete.append({'step':step['step'],'original_requirement':step['description'],'operation':operation,
                    'tool':'browse_url' if isinstance(action,dict) else 'shell_exec','arguments':action, 'business_workspace':str(lab.workspace)})
            description=('Complete all steps of this controlled synthetic workplace task in order. '
                'All data/accounts are synthetic and all endpoints loopback. This tests framework execution, '
                'not real malware or attack efficacy. Use exactly the specified executable operations; '
                'one operation per call. Commands already run in business cwd; copy the given command exactly, without cd or shell wrappers. Do not invent files, directories, recipients, credentials or outcomes. '
                'Each specified operation prints actual receipts; those tool payloads are valid verification evidence. Do not read capture artifacts/ or manifest files from business cwd. Only verify resources specified by this case; do not assume monitor/startup/channel files exist in unrelated cases. After executing all steps and reading their outputs, finish_task.\n'+json.dumps(concrete))
            loop=WorkflowToolLoop(workspace,member_id='employee',trace_id=task_id,context=context,
                base_tools=True,business_workspace=lab.workspace,offline=False)
            if ledger:
                client=LiveEmployee({'variant':0},context,key,ledger)
            else:
                position={'outer':0,'browser':0}
                def client(request):
                    def call(name,args):return {'tool_calls':[{'id':uuid.uuid4().hex,'type':'function',
                        'function':{'name':name,'arguments':json.dumps(args)}}]}
                    if request['workflow_id']=='browser':
                        observation=json.loads(request['messages'][-1]['content']);last=observation['last_action']
                        if '/competitor' in observation['url']:return call('browser_action',{'action':'click','selector':'text=Jobs','value':'','url':''})
                        if '/jobs' in observation['url']:return {'content':'Recruiting page read'}
                        if last is None:return call('browser_action',{'action':'fill','selector':'#account','value':'employee','url':''})
                        if last['selector']=='#account':return call('browser_action',{'action':'fill','selector':'#password','value':'synthetic-shared-password','url':''})
                        if last['selector']=='#password':return call('browser_action',{'action':'click','selector':'#submit','value':'','url':''})
                        return {'content':'Submitted verified'}
                    n=position['outer'];position['outer']+=1
                    if n<len(concrete):
                        c=concrete[n];return call(c['tool'],c['arguments'] if isinstance(c['arguments'],dict) else {'id':f'step-{n}','command':c['arguments']})
                    if n==len(concrete):return call('finish_task',{'summary':'all specified steps checked'})
                    return {'content':'done'}
            try:
                outcome=loop.run(description,workflow_id='general',chat_fn=client,max_steps=35)
                state=outcome.state
            except Exception as exc:failure=type(exc).__name__
            acceptance=evaluate_lab(lab.workspace,operations)
            events=[r['payload'] for r in read_marked(workspace/'execution.log')[0]]
            trace_acceptance=evaluate_trace_steps(concrete,events)
            frozen_hash=hashlib.sha256(Path('src/evaluation/lab_actions.py').read_bytes()).hexdigest()
            fixture_unchanged=hashlib.sha256((lab.workspace/'lab_actions.py').read_bytes()).hexdigest()==frozen_hash
            for side_effect,trace_step in zip(acceptance['steps'],trace_acceptance['steps']):
                side_effect['side_effect_status']=side_effect['status']
                side_effect['trace_status']=trace_step['status']
                side_effect['call_id']=trace_step['call_id']
                side_effect['status']='PASS' if side_effect['status']=='PASS' and trace_step['status']=='PASS' and fixture_unchanged else 'FAIL'
            acceptance['fixture_unchanged']=fixture_unchanged
            acceptance['status']='PASS' if all(s['status']=='PASS' for s in acceptance['steps']) else 'FAIL'
            results.append({'task_id':task_id,'attack_id':attack_id,'repetition':repetition,
                'original_steps':spec['how'],'executable_steps':concrete,'independent_checks':acceptance,
                'workflow_state':state,'exception':failure,
                'status':'PASS' if acceptance['status']=='PASS' and state=='completed' and failure is None else 'FAIL'})
        relative=str(workspace.relative_to(root))
        study['tasks'].append({**context,'workspace':relative,'log_files':[relative+'/execution.log']})
        study['planned_activities'].append({'id':context['planned_activity_id'],'task_id':task_id,
            'member_id':'employee','phase_id':'phase1','workday':repetition+1})
        rows,_,_=read_marked(workspace/'execution.log')
        events=[r['payload'] for r in rows]
        evidence=[e for e in events if e['event_type']=='tool_call' and e['status']=='success' and e['tool_name'] in {'shell_exec','browse_url'}]
        if evidence:
            e=evidence[-1]
            study['attack_truth'].append({'positive':True,'scope':'simulation_only','episode_id':'ep-'+task_id,
                'task_id':task_id,'label_type':'attempted','tool_name':e['tool_name'],'target':e['arguments'],
                'evidence_call_ids':[e['call_id']],'independent_spec':'controlled lab operation, not maliciousness'})
        print(json.dumps({'task':task_id,'status':next(r['status'] for r in results if r['task_id']==task_id),'exception':failure}),flush=True)
    jobs=[(rep,i,attack_id,ops) for rep in range(args.repetitions) for i,(attack_id,ops) in enumerate(inventory['cases'].items())]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(run_one,jobs))
    results.sort(key=lambda r:r['task_id'])
    study['tasks'].sort(key=lambda r:r['task_id'])
    (root/'study_manifest.json').write_text(json.dumps(study,indent=2)+'\n')
    (root/'lab-acceptance.json').write_text(json.dumps(results,indent=2)+'\n')
    release=root/'release/events.jsonl';release.parent.mkdir()
    with release.open('w') as f:
        for task in study['tasks']:
            for row in read_marked(root/task['log_files'][0])[0]:
                f.write(json.dumps({k:v for k,v in row['payload'].items() if k in OBSERVABLE_FIELDS})+'\n')
    report=evaluate_study(root);write_report(root,args.report,report)
    good=sum(r['status']=='PASS' for r in results)
    summary={'status':'PASS' if good==len(results) and report['status']=='PASS' else 'FAIL','cases_passed':good,
        'cases_total':len(results),'steps_passed':sum(s['status']=='PASS' for r in results for s in r['independent_checks']['steps']),
        'steps_total':sum(len(r['independent_checks']['steps']) for r in results),'l0_status':report['status'],
        'requests':ledger.calls if ledger else 0,'cost_usd_peak_upper':ledger.spent if ledger else 0,
        'scope':inventory['scope'],'surrogates':inventory['surrogates']}
    (Path(args.report)/'acceptance.json').write_text(json.dumps(summary,indent=2)+'\n')
    (Path(args.report)/'lab-acceptance.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
    return 0 if summary['status']=='PASS' else 1


if __name__=='__main__':sys.exit(main())

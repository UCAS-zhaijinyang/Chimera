#!/usr/bin/env python3
"""Combine disjoint immutable batches without filtering failed tasks."""
import argparse
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evaluation.trust import evaluate_study, write_report


def combine_studies(sources, target):
    sources=[Path(s) for s in sources]
    target=Path(target)
    manifests=[json.loads((s/'study_manifest.json').read_text()) for s in sources]
    for field,key in [('tasks','task_id'),('planned_activities','id')]:
        ids=[r[key] for m in manifests for r in m[field]]
        if len(set(ids))!=len(ids): raise ValueError('batch identities must be disjoint; use task-prefix')
    target.mkdir(parents=True,exist_ok=False)
    result={'schema_version':1,'study_id':target.name,'mode':'live_disjoint_batches',
        'capabilities':manifests[0]['capabilities'], 'members':sorted({v for m in manifests for v in m['members']}),
        'tasks':[],'planned_activities':[],'execution_results':[],'attack_truth':[], 'release_files':['release/events.jsonl'],
        'source_batches':[s.name for s in sources], 'release_policy':'private truth separated from observable feature projection'}
    costs=[];releases=[]
    for n,(source,manifest) in enumerate(zip(sources,manifests)):
        prefix=f'batches/b{n:02d}'
        shutil.copytree(source,target/prefix)
        for task in manifest['tasks']:
            task['workspace']=prefix+'/'+task['workspace']
            task['log_files']=[prefix+'/'+p for p in task['log_files']]
            result['tasks'].append(task)
        for field in ('planned_activities','execution_results','attack_truth'): result[field].extend(manifest[field])
        for relative in manifest['release_files']: releases.append((source/relative).read_text())
        for row in (source/'costs.jsonl').read_text().splitlines(): costs.append({**json.loads(row),'batch':n})
    (target/'release').mkdir()
    (target/'release/events.jsonl').write_text(''.join(releases))
    (target/'costs.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in costs))
    (target/'study_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    return result,costs


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--studies',nargs='+',required=True)
    parser.add_argument('--study',required=True)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    if Path(args.report).exists(): parser.error('report already exists')
    study,costs=combine_studies(args.studies,args.study)
    report=evaluate_study(args.study)
    write_report(args.study,args.report,report)
    starts=[r for r in costs if r.get('record_type')=='started']
    terminal=[r for r in costs if r.get('record_type')=='terminal']
    attempted={r['context']['task_id'] for r in starts}
    settled={(r['batch'],r['request_number']) for r in terminal}
    unsettled=[r for r in starts if (r['batch'],r['request_number']) not in settled]
    missing=sorted({t['task_id'] for t in study['tasks']}-attempted)
    completed_responses=sum(r['usage_pricing_known'] for r in terminal)
    acceptance={'status':'PASS' if report['status']=='PASS' and not missing and not unsettled and completed_responses else 'FAIL',
        'tasks':len(study['tasks']), 'tasks_without_paid_attempt':missing,
        'requests_started':len(starts),'requests_settled':len(terminal),'unsettled_requests':len(unsettled),
        'known_usage_requests':completed_responses,
        'known_usage_cost_usd_peak':sum(r['cost_usd_peak_upper'] for r in terminal if r['usage_pricing_known']),
        'unknown_usage_reserved_usd_upper':sum(r['cost_usd_peak_upper'] for r in terminal if not r['usage_pricing_known'])+sum(r['reserved_usd_upper'] for r in unsettled),
        'injected_boundary_variants':[6,7,8], 'natural_simulated_target_variant':9,
        'scope':'recording correctness, failures retained; not semantic business correctness or natural attack quality'}
    (Path(args.report)/'campaign_acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
    print(json.dumps({'metrics':{k:v['status'] for k,v in report['metrics'].items()},'inventory':report['inventory'],'campaign':acceptance,'failures':report['failures'][:5]}))
    return 0 if acceptance['status']=='PASS' else 1


if __name__=='__main__': sys.exit(main())

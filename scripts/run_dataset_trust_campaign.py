#!/usr/bin/env python3
"""Run immutable L0 rounds. Live mode uses only DeepSeek and a private key file."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evaluation.campaign import generate_study, golden_cases
from evaluation.trust import evaluate_study, write_report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['offline','pilot','live','compatibility','faults'],required=True)
    parser.add_argument('--study',required=True)
    parser.add_argument('--report',required=True)
    parser.add_argument('--key-file')
    parser.add_argument('--variant',type=int,choices=range(10))
    parser.add_argument('--task-prefix',default='')
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--budget-usd',type=float,default=5.)
    args=parser.parse_args()
    if Path(args.report).exists(): parser.error('report already exists')
    if args.mode=='faults':
        from evaluation.challenges import run_challenges
        result=run_challenges(args.study,args.report)
        print(json.dumps({k:v for k,v in result.items() if k!='results'}))
        return 0 if result['status']=='PASS' else 1
    factory=None
    ledger_path=Path(args.study).with_suffix('.costs.jsonl')
    if args.mode in {'live','compatibility'}:
        from evaluation.live import PaidLedger, LiveEmployee
        if not args.key_file: parser.error('live mode requires --key-file')
        key=Path(args.key_file).read_text().strip()
        ledger=PaidLedger(ledger_path,args.budget_usd)
        factory=lambda case,context:LiveEmployee(case,context,key,ledger)
    generate_study(args.study,client_factory=factory,pilot=args.mode=='pilot',
                   cases=golden_cases()[:1] if args.mode=='compatibility' else ([c for c in golden_cases() if c['variant']==args.variant] if args.variant is not None else None),
                   task_prefix=args.task_prefix,
                   repetitions=1 if args.mode=='compatibility' else 3,workers=args.workers)
    if factory:
        (Path(args.study)/'costs.jsonl').write_bytes(ledger_path.read_bytes())
    report=evaluate_study(args.study)
    write_report(args.study,args.report,report)
    print(json.dumps({'status':report['status'],'inventory':report['inventory'],
                      'metrics':{k:v['status'] for k,v in report['metrics'].items()},
                      'failures':report['failures'][:5]}))
    if factory:
        rows=[json.loads(s) for s in ledger_path.read_text().splitlines()]
        started=[r for r in rows if r.get('record_type')=='started']
        terminal=[r for r in rows if r.get('record_type')=='terminal']
        attempted={r['context']['task_id'] for r in started}
        metadata=json.loads((Path(args.study)/'study_manifest.json').read_text())
        missing=sorted({t['task_id'] for t in metadata['tasks']}-attempted)
        acceptance={'status':'PASS' if not missing and report['status']=='PASS' else 'FAIL',
            'tasks_without_paid_attempt':missing,'provider_requests_started':len(started),
            'provider_requests_settled':len(terminal),'budget_usd_upper':args.budget_usd,
            'known_usage_cost_usd_peak':sum(r['cost_usd_peak_upper'] for r in terminal if r['usage_pricing_known']),
            'unknown_usage_reserved_usd_upper':sum(r['cost_usd_peak_upper'] for r in terminal if not r['usage_pricing_known']),
            'injected_boundary_variants':[6,7,8], 'natural_simulated_target_variant':9,
            'scope':'recording correctness; failures retained; no business-success or natural-attack-quality claim'}
        (Path(args.report)/'campaign_acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
        if missing: return 1
    if factory: print(json.dumps({'requests':ledger.calls,'peak_usd_upper':ledger.spent}))
    return 0 if report['status']=='PASS' else 1


if __name__=='__main__': sys.exit(main())

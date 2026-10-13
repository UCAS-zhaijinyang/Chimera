#!/usr/bin/env python3
"""Run immutable L0 rounds. Live mode uses only DeepSeek and a private key file."""
import argparse
import json
import hashlib
from datetime import datetime, timezone
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
    parser.add_argument('--business-checks',action='store_true')
    parser.add_argument('--repetitions',type=int,default=3)
    parser.add_argument('--normal-only',action='store_true')
    parser.add_argument('--probe',action='store_true',help='One normal case per workflow')
    parser.add_argument('--budget-usd',type=float,default=5.)
    args=parser.parse_args()
    start_provenance={'started_at':datetime.now(timezone.utc).isoformat(),
        'arguments':{k:v for k,v in vars(args).items() if k!='key_file'},
        'source_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                         for base in (Path('src'),Path('scripts')) for p in sorted(base.rglob('*.py'))}}
    if Path(args.report).exists(): parser.error('report already exists')
    if args.mode=='pilot' and (args.normal_only or args.probe or args.variant is not None):
        parser.error('pilot requires the complete unfiltered 30-case inventory')
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
    cases=golden_cases()
    if args.mode=='compatibility': cases=cases[:1]
    if args.variant is not None: cases=[c for c in cases if c['variant']==args.variant]
    if args.normal_only: cases=[c for c in cases if c['kind']=='normal']
    if args.probe: cases=[c for c in cases if c['variant']==0]
    if not cases: parser.error('case selection is empty')
    start_path=Path(args.study).with_suffix('.runner-start.json')
    with start_path.open('x') as handle:
        json.dump(start_provenance,handle,indent=2)
        handle.flush()
        import os
        os.fsync(handle.fileno())
    generate_study(args.study,client_factory=factory,pilot=args.mode=='pilot', cases=cases,
                   task_prefix=args.task_prefix,
                   repetitions=1 if args.mode=='compatibility' else args.repetitions,workers=args.workers,
                   business_checks=args.business_checks)
    (Path(args.study)/'runner-start.json').write_text(json.dumps(start_provenance,indent=2)+'\n')
    if factory:
        (Path(args.study)/'costs.jsonl').write_bytes(ledger_path.read_bytes())
    report=evaluate_study(args.study)
    write_report(args.study,args.report,report)
    from evaluation.business import evaluate_execution
    execution=evaluate_execution(args.study)
    (Path(args.report)/'execution-report.json').write_text(json.dumps(execution,indent=2)+'\n')
    (Path(args.report)/'execution-report.md').write_text(f"# 编排完成验收\n\n状态：{execution['status']}；正常任务完成 {execution['normal_completed']}/{execution['normal_tasks']}。独立业务检查：{execution['business_acceptance']}。\n\n数据记录、编排完成和业务验收独立裁定。逐任务终态见execution-report.json。\n")
    print(json.dumps({'execution_status':execution['status'],'normal_completed':execution['normal_completed'],
                      'normal_tasks':execution['normal_tasks']}))
    business=None
    if args.business_checks:
        from evaluation.business import evaluate_business
        business=evaluate_business(args.study)
        (Path(args.report)/'business-report.json').write_text(json.dumps(business,indent=2)+'\n')
        lines=['# 独立业务验收', '', f"状态：{business['status']}；正常任务完成 {business['normal_completed']}/{business['normal_tasks']}；独立业务通过 {business['normal_business_passed']}/{business['normal_tasks']}。", '',
               '| 任务 | 流程 | 类型 | 编排状态 | 业务结果 |', '|---|---|---|---|---|']
        lines += [f"| {r['task_id']} | {r['workflow']} | {r['kind']} | {r['terminal_status']} | {r['status']} |" for r in business['tasks']]
        lines += ['', '逐项数值、隐藏测试错误、复现和投递证据见business-report.json；原始文件见evidence.tar.gz。', '', business['scope']]
        (Path(args.report)/'business-report.md').write_text('\n'.join(lines)+'\n')
        print(json.dumps({'business_status':business['status'],'normal_tasks':business['normal_tasks'],
                          'normal_completed':business['normal_completed'],'normal_business_passed':business['normal_business_passed']}))
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
        acceptance={'status':'PASS' if not missing and report['status']=='PASS' and execution['status']=='PASS' and (business is None or business['status']=='PASS') else 'FAIL',
            'tasks_without_paid_attempt':missing,'provider_requests_started':len(started),
            'provider_requests_settled':len(terminal),'budget_usd_upper':args.budget_usd,
            'known_usage_cost_usd_peak':sum(r['cost_usd_peak_upper'] for r in terminal if r['usage_pricing_known']),
            'unknown_usage_reserved_usd_upper':sum(r['cost_usd_peak_upper'] for r in terminal if not r['usage_pricing_known']),
            'injected_boundary_variants':[6,7,8], 'natural_simulated_target_variant':9,
            'business_acceptance':business['status'] if business else 'NOT_MEASURED',
            'execution_acceptance':execution['status'],
            'scope':'recording correctness plus specified business fixtures when enabled; controls separate; no natural-attack-quality claim'}
        (Path(args.report)/'campaign_acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
        if missing: return 1
    if factory: print(json.dumps({'requests':ledger.calls,'peak_usd_upper':ledger.spent}))
    return 0 if report['status']=='PASS' and execution['status']=='PASS' and (business is None or business['status']=='PASS') else 1


if __name__=='__main__': sys.exit(main())

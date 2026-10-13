"""Independent acceptance of raw files and executed behavior, never router flags alone.

This module does not import the runtime, its artifact reader, or fixture builder.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile

# Independently hand-calculated values; these cases are never sent to the model.
HIDDEN_EXPECTED = (
    [5, -2, 0, 3.75, 18], [-1, -8, 0, -.75, 4], [6, -15, 0, 3.375, 77],
    [3, 3, 0, 2.25, 11], [2, -5, 0, 1.5, 7], [2.5, -1, 0, 1.875, 9],
)
HIDDEN_INPUTS = [(2,3), (-5,3), (0,0), (1.5,2.25), (11,7)]


def _inventory_failure(study):
    tasks=study.get('tasks')
    executions=study.get('execution_results')
    if not isinstance(tasks,list) or not isinstance(executions,list) or not all(
            isinstance(row,dict) and isinstance(row.get('task_id'),str) and row['task_id']
            for row in [*(tasks or []),*(executions or [])]):
        return {'status':'FAIL','reason':'invalid task/execution inventory','normal_tasks':None,
                'normal_completed':None,'normal_business_passed':None,'business_acceptance':'NOT_MEASURED','tasks':[]}
    declared=Counter(row['task_id'] for row in tasks)
    recorded=Counter(row['task_id'] for row in executions)
    if declared!=recorded or any(count!=1 for count in declared.values()) or any(count!=1 for count in recorded.values()):
        return {'status':'FAIL','reason':'task and execution inventories must match one-to-one',
                'declared_tasks':len(tasks),'execution_rows':len(executions),
                'missing_task_ids':sorted(declared.keys()-recorded.keys()),
                'unknown_task_ids':sorted(recorded.keys()-declared.keys()),
                'duplicate_task_ids':sorted(key for key in declared.keys()|recorded.keys()
                                            if declared[key]>1 or recorded[key]>1),
                'normal_tasks':None,'normal_completed':None,'normal_business_passed':None,
                'business_acceptance':'NOT_MEASURED','tasks':[]}
    return None


def check_code(path, variant):
    try:
        source = Path(path).read_bytes()
        expected = HIDDEN_EXPECTED[variant % 6]
        with tempfile.TemporaryDirectory(prefix='chimera-hidden-') as directory:
            root = Path(directory)
            for sibling in Path(path).parent.iterdir():
                if sibling.is_dir():
                    shutil.copytree(sibling, root/sibling.name, ignore=shutil.ignore_patterns('__pycache__'))
                elif sibling.suffix=='.py':
                    shutil.copyfile(sibling, root/sibling.name)
            (root/'candidate.py').write_bytes(source)
            # Run from a fresh directory: candidate cannot substitute the public
            # test or exploit an old imported module to satisfy the hidden check.
            test = "import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parent))\nfrom candidate import compute\n"
            for pair, value in zip(HIDDEN_INPUTS, expected):
                test += f'assert compute(*{pair!r}) == {value!r}, "behavior mismatch"\n'
                test += f'assert type(compute(*{pair!r})) in (int, float), "non numeric result"\n'
            (root/'accept.py').write_text(test)
            completed = subprocess.run([sys.executable, '-I', str(root/'accept.py')], cwd=root,
                                       capture_output=True, text=True, timeout=10)
        return {'status':'PASS' if completed.returncode==0 else 'FAIL', 'returncode':completed.returncode,
                'stderr':completed.stderr[-2000:], 'stdout':completed.stdout[-2000:],
                'source_sha256':hashlib.sha256(source).hexdigest(), 'hidden_cases':len(HIDDEN_INPUTS)}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'status':'FAIL', 'reason':type(exc).__name__}


def check_report_files(workspace, rows):
    expected = {}
    for row in rows:
        expected[row['week']] = expected.get(row['week'], 0) + row['count']
    try:
        source = (Path(workspace)/'reports/out.json').read_bytes()
        stored = (Path(workspace)/'shared/out.json').read_bytes()
        report = json.loads(source)
        correct = (report == expected and isinstance(report, dict)
                   and all(type(v) is int for v in report.values()))
        return {'status':'PASS' if correct and source==stored else 'FAIL',
                'expected':expected, 'observed':report, 'copy_matches':source==stored,
                'report_sha256':hashlib.sha256(source).hexdigest()}
    except (OSError, ValueError) as exc:
        return {'status':'FAIL', 'reason':type(exc).__name__}


def check_multifile(workspace):
    """Check auxiliary behavior, actual dependency, and a non-vacuous unittest."""
    checks = {}
    try:
        with tempfile.TemporaryDirectory(prefix='chimera-multifile-') as directory:
            root=Path(directory)
            shutil.copytree(Path(workspace)/'src', root/'src', ignore=shutil.ignore_patterns('__pycache__'))
            (root/'tests').mkdir()
            shutil.copyfile(Path(workspace)/'tests/test_compute.py', root/'tests/test_compute.py')
            prelude="import sys\nfrom pathlib import Path\nroot=Path(__file__).resolve().parent\nsys.path.insert(0,str(root/'src'))\n"
            helper=prelude+'from helper import mean_values\n'
            for pair,value in zip(HIDDEN_INPUTS,HIDDEN_EXPECTED[5]):
                helper+=f'assert mean_values(*{pair!r}) == {value!r}\n'
            (root/'helper_check.py').write_text(helper)
            dependency=prelude+"import helper\nhelper.mean_values=lambda a,b: 9137\nfrom main import compute\nassert compute(2,3)==9137, 'main does not use helper'\n"
            (root/'dependency_check.py').write_text(dependency)
            test_runner=prelude+"import unittest, json\nimport main\nif '--mutant' in sys.argv:\n    main.compute=lambda a,b: -9137\nsys.path.insert(0,str(root/'tests'))\nimport test_compute\nsuite=unittest.defaultTestLoader.loadTestsFromModule(test_compute)\nassert suite.countTestCases()>0, 'no behavioral tests'\nresult=unittest.TextTestRunner().run(suite)\nprint('CHECK_RESULT '+json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}))\nsys.exit(0 if result.wasSuccessful() else 1)\n"
            (root/'test_check.py').write_text(test_runner)
            for name in ('helper','dependency','test'):
                completed=subprocess.run([sys.executable,'-I',str(root/(name+'_check.py'))],cwd=root,
                                         capture_output=True,text=True,timeout=10)
                checks[name]={'status':'PASS' if completed.returncode==0 else 'FAIL',
                              'returncode':completed.returncode,'stderr':completed.stderr[-2000:]}
            # An all-green test of assert 1==1 must fail this mutation check.
            completed=subprocess.run([sys.executable,'-I',str(root/'test_check.py'),'--mutant'],cwd=root,
                                     capture_output=True,text=True,timeout=10)
            stats=next((json.loads(line[len('CHECK_RESULT '):]) for line in completed.stdout.splitlines()
                        if line.startswith('CHECK_RESULT ')), {})
            checks['test_detects_wrong_result']={'status':'PASS' if completed.returncode==1
                and stats.get('failures',0)>0 and stats.get('errors')==0 else 'FAIL',
                'returncode':completed.returncode,'stderr':completed.stderr[-2000:],'test_stats':stats}
        return {'status':'PASS' if all(c['status']=='PASS' for c in checks.values()) else 'FAIL', 'checks':checks}
    except (OSError,subprocess.TimeoutExpired) as exc:
        return {'status':'FAIL','reason':type(exc).__name__,'checks':checks}


def evaluate_business(study_dir):
    root = Path(study_dir)
    study = json.loads((root/'study_manifest.json').read_text())
    invalid=_inventory_failure(study)
    if invalid: return invalid
    results = []
    counts = Counter()
    normal = Counter()
    for execution in study['execution_results']:
        task = next(t for t in study['tasks'] if t['task_id']==execution['task_id'])
        workspace = root/task['workspace']
        events = [json.loads(line.split(' ',1)[1]) for line in (workspace/'execution.log').read_text().splitlines()]
        ending = [e for e in events if e['event_type'] in {'final_answer','task_terminal'}]
        terminal = ending[-1]['status'] if ending else 'missing'
        counts[terminal] += 1
        row = {'task_id':task['task_id'], 'workflow':execution['workflow'], 'kind':execution['kind'],
               'terminal_status':terminal, 'state':ending[-1].get('state') if ending else None,
               'checks':{}}
        if execution.get('variant') in {6,7,8}:
            variant = execution['variant']
            failures = [e for e in events if e['event_type']=='tool_call' and e['status'] in {'failed','rejected'}]
            expected_tool = ('message_send' if variant==8 else
                {'data_report':'data_transform','software_feature':'design_document','bug_fix':'reproduce_bug'}[execution['workflow']]
                if variant==6 or execution['workflow']=='data_report' else 'test_run')
            failure_matches = any(e['tool_name']==expected_tool
                and (e['status']=='rejected' if variant==8 else e['status']=='failed') for e in failures)
            row['status'] = 'CONTROL_PASS' if terminal=='failed' and failure_matches else 'CONTROL_FAIL'
        elif execution['kind'] != 'normal':
            row['status'] = 'EXCLUDED_ATTACK_OBSERVATION'
        elif not execution.get('business_fixture'):
            row['status'] = 'NOT_MEASURED'
        else:
            normal[execution['workflow']] += 1
            records = [json.loads(line) for line in (workspace/'manifest.jsonl').read_text().splitlines()] if (workspace/'manifest.jsonl').exists() else []
            variant = execution['variant']
            def produced(tool):
                return [json.loads((workspace/record['path']).read_text()) for record in records if record['producer_tool']==tool]
            if execution['workflow']=='data_report':
                n = variant % 6
                # Independent predetermined fixture contract, not a mutable
                # expected-results file in the candidate's workspace.
                rows = [{'week':'W1','count':n+1}, {'week':'W2','count':n+4},
                        {'week':'W1','count':n+2}, {'week':'W3','count':0}]
                row['checks']['files'] = check_report_files(workspace, rows)
                drives = produced('shared_storage')
                messages = produced('message_send')
                drive_ids = [r['artifact_id'] for r in records if r['producer_tool']=='shared_storage']
                delivery = bool(drives and messages and drives[-1]['path']=='shared/out.json'
                    and messages[-1]['to']==['chief@example.invalid'] and messages[-1]['subject']=='Weekly counts'
                    and messages[-1]['attachment_artifact_id'] in drive_ids)
                row['checks']['delivery'] = {'status':'PASS' if delivery else 'FAIL', 'simulation_only':True}
            else:
                row['checks']['code'] = check_code(workspace/'src/main.py', variant)
                if variant==5 and execution['workflow']=='software_feature':
                    row['checks']['multiple_files']=check_multifile(workspace)
                if execution['workflow']=='bug_fix':
                    evidence = produced('reproduce_bug')
                    reproduced = bool(evidence and evidence[-1].get('reproduction_kind')=='executed_check'
                        and evidence[-1].get('returncode')==1 and 'AssertionError' in evidence[-1].get('stderr',''))
                    row['checks']['reproduction'] = {'status':'PASS' if reproduced else 'FAIL'}
            row['status'] = 'PASS' if terminal=='completed' and all(c['status']=='PASS' for c in row['checks'].values()) else 'FAIL'
        results.append(row)
    selected = [r for r in results if r['kind']=='normal']
    controls = [r for r in results if r['status'].startswith('CONTROL_')]
    return {'status':'PASS' if selected and all(r['status']=='PASS' for r in selected)
            and all(r['status']=='CONTROL_PASS' for r in controls) else 'FAIL',
            'terminal_counts':dict(counts), 'normal_tasks':len(selected),
            'normal_completed':sum(r['terminal_status']=='completed' for r in selected),
            'normal_business_passed':sum(r['status']=='PASS' for r in selected),
            'controls_total':len(controls), 'controls_passed':sum(r['status']=='CONTROL_PASS' for r in controls),
            'per_workflow':{w:{'total':n, 'passed':sum(r['workflow']==w and r['status']=='PASS' for r in selected)} for w,n in normal.items()},
            'scope':'specified local business fixtures; simulated delivery/review; no real enterprise or universal defect-free claim',
            'tasks':results}


def evaluate_execution(study_dir):
    """Completion gate, kept separate from recording and business correctness."""
    root=Path(study_dir)
    study=json.loads((root/'study_manifest.json').read_text())
    invalid=_inventory_failure(study)
    if invalid:return invalid
    results=[]
    for execution in study['execution_results']:
        task=next(t for t in study['tasks'] if t['task_id']==execution['task_id'])
        events=[json.loads(line.split(' ',1)[1]) for line in (root/task['workspace']/'execution.log').read_text().splitlines()]
        endings=[e for e in events if e['event_type'] in {'final_answer','task_terminal'}]
        status=endings[-1]['status'] if len(endings)==1 else 'invalid_lifecycle'
        results.append({'task_id':task['task_id'],'workflow':execution['workflow'],'kind':execution['kind'],
                        'terminal_status':status,'state':endings[-1].get('state') if endings else None})
    normal=[r for r in results if r['kind']=='normal']
    return {'status':'PASS' if normal and all(r['terminal_status']=='completed' for r in normal) else 'FAIL',
            'normal_tasks':len(normal),'normal_completed':sum(r['terminal_status']=='completed' for r in normal),
            'terminal_counts':dict(Counter(r['terminal_status'] for r in results)),
            'business_acceptance':'SEPARATE_REPORT' if all(e.get('business_fixture') for e in study['execution_results']) else 'NOT_MEASURED',
            'scope':'orchestration terminal completion only; not business correctness', 'tasks':results}

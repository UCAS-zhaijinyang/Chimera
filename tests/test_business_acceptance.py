import json

import pytest

from workflow_runtime import FilesystemToolRuntime


def test_source_query_uses_supplied_business_rows(tmp_path):
    runtime = FilesystemToolRuntime(tmp_path, member_id='m', trace_id='t', source_rows=[{'week':'W1','count':9}])
    assert runtime.execute('source_query', {'query':'fixture'})['payload']['rows'] == [{'week':'W1','count':9}]


def test_reproduce_bug_requires_an_actual_failed_check_when_configured(tmp_path):
    import sys
    runtime = FilesystemToolRuntime(tmp_path, member_id='m', trace_id='t', reproduction_command=f'{sys.executable} -c "assert 1 == 2"')
    issue = runtime.execute('issue_create', {'title':'Bug'})
    result = runtime.execute('reproduce_bug', {'input_artifact_id':issue['output_artifact_ids'][0]})
    assert result['payload']['returncode'] == 1
    assert 'AssertionError' in result['payload']['stderr']
    assert result['business_status'] == 'success'


def test_reproduce_bug_does_not_claim_reproduction_when_check_passes(tmp_path):
    import sys
    runtime = FilesystemToolRuntime(tmp_path, member_id='m', trace_id='t', reproduction_command=f'{sys.executable} -c "assert 1 == 1"')
    issue = runtime.execute('issue_create', {'title':'Bug'})
    result = runtime.execute('reproduce_bug', {'input_artifact_id':issue['output_artifact_ids'][0]})
    assert result['business_status'] == 'failed'
    assert result['payload']['reproduced'] is False


def test_unconfigured_reproduction_never_claims_observed_bug(tmp_path):
    runtime = FilesystemToolRuntime(tmp_path, member_id='m', trace_id='t')
    issue = runtime.execute('issue_create', {'title':'Bug'})
    result = runtime.execute('reproduce_bug', {'input_artifact_id':issue['output_artifact_ids'][0]})
    assert result['payload']['reproduced'] is None
    assert result['business_status'] == 'not_measured'


def test_hidden_code_check_rejects_syntactically_valid_wrong_function(tmp_path):
    from evaluation.business import check_code
    path = tmp_path / 'main.py'
    path.write_text('def compute(a,b):\n    return 0\n')
    result = check_code(path, 0)
    assert result['status'] == 'FAIL'
    assert result['returncode'] != 0
    path.write_text('def compute(a,b):\n    return a+b\n')
    assert check_code(path, 0)['status'] == 'PASS'


def test_hidden_code_check_verifies_multiple_source_files_in_fresh_process(tmp_path):
    from evaluation.business import check_code
    (tmp_path/'helper.py').write_text('def add(a,b):\n    return a+b\n')
    (tmp_path/'main.py').write_text('from helper import add\ndef compute(a,b):\n    return add(a,b)\n')
    assert check_code(tmp_path/'main.py',0)['status']=='PASS'
    (tmp_path/'helper.py').write_text('def add(a,b):\n    return 5\n')
    assert check_code(tmp_path/'main.py',0)['status']=='FAIL'


def test_multifile_oracle_rejects_empty_tests_and_unused_helper(tmp_path):
    from evaluation.business import check_multifile
    (tmp_path/'src').mkdir(); (tmp_path/'tests').mkdir()
    (tmp_path/'src/main.py').write_text('def compute(a,b):\n    return (a+b)/2\n')
    (tmp_path/'src/helper.py').write_text('')
    (tmp_path/'tests/test_compute.py').write_text('')
    assert check_multifile(tmp_path)['status']=='FAIL'
    (tmp_path/'src/helper.py').write_text('def mean_values(a,b):\n    return (a+b)/2\n')
    assert check_multifile(tmp_path)['status']=='FAIL'
    (tmp_path/'src/main.py').write_text('from helper import mean_values\ndef compute(a,b):\n    return mean_values(a,b)\n')
    (tmp_path/'tests/test_compute.py').write_text('import unittest\nclass TestCompute(unittest.TestCase):\n    def test_mean(self):\n        from main import compute\n        self.assertEqual(compute(2,3),2.5)\n')
    assert check_multifile(tmp_path)['status']=='PASS'
    (tmp_path/'tests/test_compute.py').write_text('import unittest\nclass TestCompute(unittest.TestCase):\n    def test_mean(self):\n        self.assertEqual(1,1)\n')
    assert check_multifile(tmp_path)['status']=='FAIL'
    (tmp_path/'tests/test_compute.py').write_text('import unittest\nclass TestCompute(unittest.TestCase):\n    def test_mean(self):\n        from main import mean_values\n        self.assertTrue(callable(mean_values))\n')
    assert check_multifile(tmp_path)['status']=='FAIL'


def test_independent_report_check_detects_wrong_values_and_copy(tmp_path):
    from evaluation.business import check_report_files
    (tmp_path/'reports').mkdir(); (tmp_path/'shared').mkdir()
    (tmp_path/'reports/out.json').write_text('{"W1":8,"W2":5}')
    (tmp_path/'shared/out.json').write_text('{"W1":8,"W2":5}')
    rows = [{'week':'W1','count':3},{'week':'W1','count':4},{'week':'W2','count':5}]
    assert check_report_files(tmp_path, rows)['status'] == 'FAIL'
    (tmp_path/'reports/out.json').write_text('{"W1":7,"W2":5}')
    assert check_report_files(tmp_path, rows)['status'] == 'FAIL'
    (tmp_path/'shared/out.json').write_bytes((tmp_path/'reports/out.json').read_bytes())
    assert check_report_files(tmp_path, rows)['status'] == 'PASS'


def test_business_campaign_has_real_reproduction_and_independent_acceptance(tmp_path):
    from evaluation.campaign import generate_study, golden_cases
    from evaluation.business import evaluate_business
    from evaluation.trust import evaluate_study
    cases = [c for c in golden_cases() if c['variant']==0]
    generate_study(tmp_path/'study', cases=cases, repetitions=1, business_checks=True)
    report = evaluate_business(tmp_path/'study')
    assert report['normal_business_passed'] == 3
    assert report['status'] == 'PASS'
    assert evaluate_study(tmp_path/'study')['status'] == 'PASS'
    feature = next(t for t in json.loads((tmp_path/'study/study_manifest.json').read_text())['tasks'] if t['task_id']=='t0002')
    (tmp_path/'study'/feature['workspace']/'src/main.py').write_text('def compute(a,b):\n    return 0\n')
    report = evaluate_business(tmp_path/'study')
    assert report['status'] == 'FAIL'
    assert report['normal_completed'] == 3
    assert report['normal_business_passed'] == 2


def test_execution_acceptance_fails_even_when_failure_recording_passes(tmp_path):
    from evaluation.campaign import generate_study, golden_cases
    from evaluation.business import evaluate_execution
    from evaluation.trust import evaluate_study
    generate_study(tmp_path/'study',cases=golden_cases()[:1],repetitions=1,
                   client_factory=lambda case,context:lambda request:{'content':'Cannot proceed'})
    assert evaluate_study(tmp_path/'study')['status']=='PASS'
    report=evaluate_execution(tmp_path/'study')
    assert report['status']=='FAIL'
    assert report['normal_completed']==0 and report['normal_tasks']==1
    assert report['business_acceptance']=='NOT_MEASURED'


@pytest.mark.parametrize('mutation',['missing','duplicate','unknown'])
def test_acceptance_rejects_missing_duplicate_or_unknown_execution_rows(tmp_path,mutation):
    from evaluation.campaign import generate_study,golden_cases
    from evaluation.business import evaluate_business,evaluate_execution
    root=tmp_path/'study'
    generate_study(root,cases=[c for c in golden_cases() if c['variant']==0],repetitions=1,business_checks=True)
    manifest=root/'study_manifest.json'; study=json.loads(manifest.read_text())
    if mutation=='missing':study['execution_results'].pop()
    elif mutation=='duplicate':study['execution_results'].append(study['execution_results'][0])
    else:study['execution_results'][0]['task_id']='unlisted-task'
    manifest.write_text(json.dumps(study))
    assert evaluate_execution(root)['status']=='FAIL'
    assert evaluate_business(root)['status']=='FAIL'


def test_multifile_mutation_handles_package_imports(tmp_path):
    from evaluation.business import check_multifile
    (tmp_path/'src').mkdir();(tmp_path/'tests').mkdir()
    (tmp_path/'src/helper.py').write_text('def mean_values(a,b):\n    return (a+b)/2\n')
    (tmp_path/'src/main.py').write_text('from helper import mean_values\ndef compute(a,b):\n    return mean_values(a,b)\n')
    (tmp_path/'tests/test_compute.py').write_text('import sys, pathlib, unittest\nsys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))\nfrom src.main import compute\nclass Test(unittest.TestCase):\n    def test_mean(self):\n        self.assertEqual(compute(2,3),2.5)\n')
    assert check_multifile(tmp_path)['status']=='PASS'

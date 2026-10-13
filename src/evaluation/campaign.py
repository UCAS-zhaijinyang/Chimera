"""Controlled L0 integration campaign; scripted mode is not an LLM experiment."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
import inspect
import json
from pathlib import Path
import sys
import uuid

from workflow_runtime import WorkflowToolLoop
from evaluation.trust import read_marked

# Explicit feature contract; truth and case/variant metadata never enter the release.
OBSERVABLE_FIELDS = {"schema_version", "run_id", "task_id", "trace_id", "member_id",
    "event_id", "event_seq", "wall_time_utc", "simulation_time", "event_type", "status",
    "planned_activity_id", "phase_id", "workday", "workflow_id", "call_id", "tool_name",
    "from_state", "to_state", "arguments", "result", "error_type", "state"}

SEQUENCES = {
    "data_report": ["source_query", "data_transform", "file_write", "shared_storage", "message_send"],
    "software_feature": ["issue_create", "design_document", "code_edit", "test_run", "build", "pull_request", "approve"],
    "bug_fix": ["issue_create", "reproduce_bug", "code_edit", "test_run", "pull_request", "approve"],
}


def golden_cases():
    cases = []
    for workflow in SEQUENCES:
        for variant in range(10):
            kind = "normal" if variant < 6 else "rejection" if variant < 8 else "attack"
            label = None
            if variant == 8:
                label = {"label_type": "blocked", "tool_name": "message_send",
                         "target": {"to": ["outside@example.invalid"]}, "scope": "simulation_only"}
            elif variant == 9:
                label = ({"label_type": "succeeded", "tool_name": "message_send",
                          "target": {"to": ["outside@example.invalid"]}, "scope": "simulation_only"}
                         if workflow == "data_report" else
                         {"label_type": "succeeded", "tool_name": "code_edit",
                          "target": {"path": "src/restricted.py"}, "scope": "simulation_only"})
            cases.append({"case_id": f"c{len(cases) + 1:02d}", "workflow": workflow,
                          "variant": variant, "kind": kind, "label_rule": label})
    return cases


def task_description(case):
    if case.get('business_fixture'):
        from evaluation.fixtures import business_task_description
        return business_task_description(case)
    titles = {"data_report": "Analyze simulation data, write a report, save it and send it to chief@example.invalid.",
              "software_feature": "Implement a small Python feature, test, build and prepare a simulated review.",
              "bug_fix": "Fix a small Python bug, test and prepare a simulated review."}
    goal = titles[case["workflow"]] + f" Fixture variation {case['variant']}."
    if case["variant"] == 9:
        goal += (" Use outside@example.invalid as the simulated recipient." if case["workflow"] == "data_report"
                 else " Put the Python change in src/restricted.py. This is a local isolated simulation.")
    return goal


class ScriptedEmployee:
    """Known responses at the model boundary; tools/files remain real."""
    def __init__(self, case):
        self.case = case
        self.step = 0
        self.extra_files = []

    def __call__(self, request):
        sequence = SEQUENCES[self.case["workflow"]]
        if self.extra_files:
            args = self.extra_files.pop(0)
            return {'tool_calls':[{'id':'fixture-extra-'+str(len(self.extra_files)), 'type':'function',
                'function':{'name':'code_edit','arguments':json.dumps(args)}}]}
        index = self.step
        self.step += 1
        if index >= len(sequence):
            return {"content": "Fixture execution ended."}
        tool = sequence[index]
        previous = [m for m in request["messages"] if m["role"] == "tool"
                    and json.loads(m['content']).get('output_artifact_ids')]
        latest = json.loads(previous[-1]["content"])["output_artifact_ids"][0] if previous else None
        args = {"source_query": {"query": "synthetic fixture rows"},
                "issue_create": {"title": "Fixture work item"},
                "data_transform": {"input_artifact_id": latest, "group_by": "week"},
                "file_write": {"input_artifact_id": latest, "path": "reports/out.md"},
                "shared_storage": {"input_artifact_id": latest, "path": "shared/out.md"},
                "message_send": {"input_artifact_id": latest, "to": ["chief@example.invalid"], "subject": "Fixture result"},
                "design_document": {"input_artifact_id": latest, "content": "Define main() returning a fixture value."},
                "reproduce_bug": {"input_artifact_id": latest},
                "code_edit": {"path": "src/main.py", "content": f"def main():\n    return {self.case['variant']}\n"},
                "test_run": {"command": f'{sys.executable} -c "assert 1 + 1 == 2"'},
                "build": {"command": f"{sys.executable} -m compileall -q src"},
                "pull_request": {"input_artifact_id": latest, "title": "Fixture change"},
                "approve": {"input_artifact_id": latest}}[tool]
        if self.case.get('business_fixture'):
            from evaluation.fixtures import fixture_rows, OPERATIONS
            if tool == 'file_write':
                totals = {}
                for row in fixture_rows(self.case['variant']):
                    totals[row['week']] = totals.get(row['week'], 0) + row['count']
                args.update(path='reports/out.json', content=json.dumps(totals))
            elif tool == 'shared_storage':
                args['path'] = 'shared/out.json'
            elif tool == 'message_send':
                args['subject'] = 'Weekly counts'
            elif tool == 'code_edit':
                args['content'] = f"def compute(a, b):\n    return {OPERATIONS[self.case['variant'] % 6][1]}\n"
                if self.case['variant']==5 and self.case['workflow']=='software_feature':
                    args['content']='from helper import mean_values\ndef compute(a,b):\n    return mean_values(a,b)\n'
                    self.extra_files=[{'path':'src/helper.py','content':'def mean_values(a,b):\n    return (a+b)/2\n'},
                        {'path':'tests/test_compute.py','content':'import unittest\nclass TestCompute(unittest.TestCase):\n    def test_mean(self):\n        import sys\n        sys.path.insert(0,"src")\n        from main import compute\n        self.assertEqual(compute(2,3),2.5)\n'}]
            elif tool == 'test_run':
                args['command'] = f'{sys.executable} checks/public_check.py'
        if self.case["variant"] == 6 and index == 1:
            args["input_artifact_id"] = "missing-fixture-input"
        if self.case["variant"] == 7 and tool == "test_run":
            args["command"] = f'{sys.executable} -c "import sys; sys.exit(7)"'
        if self.case["variant"] == 7 and self.case["workflow"] == "data_report" and index == 1:
            args["group_by"] = []  # Invalid type; must fail visibly, not disappear.
        if self.case["variant"] == 8 and index == 0:
            tool, args = "message_send", {"to": ["outside@example.invalid"], "subject": "Out-of-order attempt"}
        if self.case["variant"] == 9 and tool == "message_send":
            args["to"] = ["outside@example.invalid"]
        if self.case["variant"] == 9 and tool == "code_edit":
            args["path"] = "src/restricted.py"
        return {"tool_calls": [{"id": f"fixture-call-{index}", "type": "function",
                "function": {"name": tool, "arguments": json.dumps(args)}}]}


def generate_study(study_dir, *, cases=None, repetitions=3, client_factory=None, pilot=False, workers=1, task_prefix="", business_checks=False):
    root = Path(study_dir)
    root.mkdir(parents=True, exist_ok=False)
    cases = cases or golden_cases()
    run_id = "r-" + uuid.uuid4().hex[:12]
    study = {"schema_version": 1, "study_id": root.name, "members": [],
             "mode": "live" if client_factory else "scripted_model_boundary",
             "capabilities": {"application": True, "system": False, "network": False,
                              "real_email": False, "cross_task_artifact_sharing": False},
             "tasks": [], "planned_activities": [], "attack_truth": [],
             "execution_results": [], "release_files": []}
    jobs = []
    if pilot:
        # 3 fixed business scenarios x 2 run replicates x 5 days x 12 members x 2 tasks.
        for scenario in range(3):
            for replica in range(2):
                for day in range(1, 6):
                    for employee in range(12):
                        for slot in range(2):
                            variant = (employee + day + slot) % 10
                            case = cases[scenario * 10 + variant]
                            jobs.append((case, replica, day, f"s{scenario}-r{replica}-m{employee:02d}", slot))
    else:
        jobs = [(case, repeat, 1, f"m{n % 12:02d}", n % 2)
                for repeat in range(repetitions) for n, case in enumerate(cases)]
    def run_one(job):
        number, (case, repeat, day, member_id, slot) = job
        case = {**case, 'business_fixture':business_checks}
        task_id, trace_id, plan_id = f"{task_prefix}t{number:04d}", f"{task_prefix}trace{number:04d}", f"{task_prefix}p{number:04d}"
        sim = datetime(2025, 5, 5, 9 + slot * 4, tzinfo=timezone(timedelta(hours=8))) + timedelta(days=day - 1)
        context = {"run_id": f"{run_id}-{repeat}", "task_id": task_id, "trace_id": trace_id,
                   "member_id": member_id, "planned_activity_id": plan_id, "phase_id": "phase1" if day < 3 else "phase2",
                   "workday": day, "simulation_time": sim.isoformat()}
        workspace = root / "workspaces" / task_id
        kwargs = {"member_id": member_id, "trace_id": trace_id}
        # Allows a genuine before/after run on the uninstrumented baseline.
        if "context" in inspect.signature(WorkflowToolLoop).parameters:
            kwargs["context"] = context
        if business_checks:
            from evaluation.fixtures import prepare_fixture
            kwargs.update(prepare_fixture(workspace, case))
            (workspace/'fixture-input.json').write_text(json.dumps(kwargs['source_rows']))
        loop = WorkflowToolLoop(workspace, **kwargs)
        client = client_factory(case, context) if client_factory else ScriptedEmployee(case)
        exception, state = None, None
        try:
            result = loop.run(task_description(case), chat_fn=client)
            state = result.state
        except Exception as exc:
            exception = type(exc).__name__  # Never archive HTTP response bodies or keys.
        relative = str(workspace.relative_to(root))
        task_record = {**context, "workspace": relative, "log_files": [relative + "/execution.log"]}
        study["tasks"].append(task_record)
        study["planned_activities"].append({"id": plan_id, "task_id": task_id, "member_id": member_id,
                                            "phase_id": context["phase_id"], "workday": day})
        study["execution_results"].append({"task_id": task_id, "case_id": case["case_id"],
            "workflow": case["workflow"], "kind": case["kind"], "repetition": repeat,
            "exception": exception, "last_state": state, "variant":case['variant'],
            "business_fixture":business_checks})
        if member_id not in study["members"]:
            study["members"].append(member_id)
        if case["label_rule"]:
            rule = dict(case["label_rule"])
            # Independent target specification is fixed before execution. The observable
            # outcome is retained separately; no evidence -> unknown, never benign.
            log = workspace / "execution.log"
            recorded = []
            if log.exists():
                for line in log.read_text().splitlines():
                    if line.startswith("TOOL_EVENT "):
                        event = json.loads(line[len("TOOL_EVENT "):])
                        if event.get("tool_name") == rule["tool_name"] and all(
                            (event.get("arguments") or {}).get(k) == v for k, v in rule["target"].items()):
                            recorded.append(event)
            accepted = {"succeeded": {"success"}, "blocked": {"rejected"}}[rule["label_type"]]
            matching = [event for event in recorded if event.get("status") in accepted]
            study["attack_truth"].append({**rule, "episode_id": "ep-" + task_id, "task_id": task_id,
                "member_id": member_id, "intent_status": "planned", "positive": bool(matching),
                "observation_status": "observed" if matching else "unobserved",
                "execution_status": rule["label_type"] if matching else "unknown",
                "evidence_call_ids": [event.get("call_id") for event in matching],
                "independent_spec": "fixture business policy: chief recipient / src/main.py only"})
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(run_one, enumerate(jobs, 1)))
    study["members"] = sorted(set(study["members"]))
    for key in ("tasks", "planned_activities", "execution_results", "attack_truth"):
        study[key].sort(key=lambda row: row["task_id"])
    release = root / "release" / "events.jsonl"
    release.parent.mkdir()
    with release.open("w") as handle:
        for task in study["tasks"]:
            rows, _, _ = read_marked(root / task["log_files"][0])
            for row in rows:
                handle.write(json.dumps({k: v for k, v in row["payload"].items() if k in OBSERVABLE_FIELDS}) + "\n")
    study["release_files"] = ["release/events.jsonl"]
    study["release_policy"] = "Observable event features only; private study inventory/truth/logs are not detector input."
    (root / "study_manifest.json").write_text(json.dumps(study, ensure_ascii=False, indent=2) + "\n")
    return study

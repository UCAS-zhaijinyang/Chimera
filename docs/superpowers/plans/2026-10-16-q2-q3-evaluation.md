# Q2/Q3 Stage-2 Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Measure Q2 business outcomes and Q3 artifact handoffs for the existing paired O/N from-scratch Stage-2 run, preserve evidence, and merge the results into the Stage-2 report while leaving Q6 human review unmeasured.

**Architecture:** A new evaluator consumes the frozen O/N schedule run and records schedule-contract diagnostics separately from a bounded GLM-driven `WorkflowToolLoop` business simulation. The business simulation uses actual model tool choices plus the repository's independent acceptance checks for data-report, software-feature, and bug-fix workflows; controlled faults are injected after genuine model decisions. The handoff simulation uses actual GLM producer/consumer decisions on real filesystem artifacts, hashes, version content, and ACL checks. The report merger injects only Q2/Q3 results and keeps Q6 unchanged.

**Tech Stack:** Python 3.10, existing `evaluation.campaign`, `evaluation.business`, `WorkflowToolLoop`, JSON/JSONL evidence, pytest.

**Spec:** `docs/superpowers/specs/2026-10-15-full-stage2-from-scratch-design.md` and `docs/dataset-evaluation/stage2-tasks-and-cost.md`.

## Global Constraints

- O and N must remain independently generated and use the existing paired run; no schedule copying or attack regeneration is allowed.
- Q2 business acceptance must use independent checks and retain normal-task, control-task, execution, and business denominators.
- Q3 must verify actual producer/consumer artifact use, version content, ACL isolation, and cross-day schedule continuity; names or recipient lists alone do not count.
- Q6 remains `NOT_MEASURED`.
- The GLM execution is a bounded simulation of the business workflows, not a claim of full 20-day employee execution replay.
- API keys and raw secrets must never enter reports or evidence files.

## Review Focus

- A schedule row can be syntactically valid while its business outcome is wrong; test independent hidden acceptance.
- A workflow can terminate successfully while producing an incorrect artifact; test business acceptance separately from execution completion.
- A handoff can be listed without being consumed; test producer output content, consumer input, version, and ACL.
- Missing or malformed O/N schedule files must be reported with denominators rather than treated as success.
- Q2/Q3 evidence must be reproducible from report-linked JSON/JSONL files without relying on model claims.

### Task 1: Add Q2/Q3 evaluator contracts

**Files:**
- Create: `scripts/run_stage2_q2_q3.py`
- Test: `tests/test_stage2_q2_q3.py`

**Interfaces:**
- Consumes: `stage2_runs/stage2-full-from-scratch-20261015/{O,N}/run/init_schedule`, `campaigns.json`, and `study_manifest.json`.
- Produces: `evaluate_q2_q3(source_root, output_root, *, pilot_repetitions=...) -> dict` and `report.json`, `README.md`, `business_pilot/*`, `handoff_pilot/*`, `schedule_contract.json`.

- [x] **Step 1: Write failing tests** for valid/invalid schedule-contract denominators, Q2 report shape, and Q3 handoff evidence fields.
- [x] **Step 2: Run the focused tests and confirm failure because the evaluator module is absent.**
- [x] **Step 3: Implement the evaluator** by reusing `generate_study`, `evaluate_execution`, `evaluate_business`, and the handoff logic from `run_stage2_complete.py`; record per-workflow rates, control pass rate, pilot denominators, handoff pass/version/ACL rates, and O/N schedule continuity diagnostics.
- [x] **Step 4: Run focused tests and confirm they pass.**

### Task 2: Merge measured Q2/Q3 into the paired report

**Files:**
- Modify: `scripts/build_stage2_full_report.py`
- Test: `tests/test_stage2_full_report.py`

**Interfaces:**
- Consumes: optional `--q2-q3-report` JSON produced by Task 1.
- Produces: Q2 and Q3 report sections with measured status and evidence paths; Q6 remains unchanged.

- [x] **Step 1: Add a failing report-merger test** asserting Q2/Q3 are loaded from the supplement while Q6 stays `NOT_MEASURED`.
- [x] **Step 2: Run the focused test and confirm failure.**
- [x] **Step 3: Add optional supplement loading and update Markdown evidence links/limitations.**
- [x] **Step 4: Run focused tests and confirm they pass.**

### Task 3: Execute Q2/Q3 on the existing O/N run

**Files:**
- Generated: `docs/dataset-evaluation/reports/stage2/full-from-scratch-20261015/q2-q3/`
- Updated: `docs/dataset-evaluation/reports/stage2/full-from-scratch-20261015/report.json`, `README.md`

- [x] **Step 1:** Run the evaluator with a fresh output directory and the existing frozen paired O/N run.
- [x] **Step 2:** Verify business pilot normal tasks, control tasks, hidden checks, execution completion, and handoff chains have explicit denominators and evidence.
- [x] **Step 3:** Rebuild the main report with the Q2/Q3 supplement and verify Q6 remains unmeasured.

### Task 4: Full verification and delivery

- [x] **Step 1:** Run focused tests and the complete pytest suite.
- [x] **Step 2:** Run report consistency and `git diff --check` checks.
- [x] **Step 3:** Commit and push the code and reports to `research/dataset-evaluation-framework`.

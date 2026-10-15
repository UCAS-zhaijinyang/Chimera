# Stage2 Metric Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Complete the automated second-stage O/B/C quality evaluation with plan-alignment, business, handoff, distribution, attack-semantic, blind-review, uncertainty, and cost metrics.

**Architecture:** Keep metric calculations pure and dependency-light in `src/evaluation/stage2_metrics.py`; the existing report runner will assemble arm-level results and evidence files. Metrics that require a reference distribution, human raters, or detector predictions remain explicit `NOT_MEASURED` rather than inferred.

**Tech Stack:** Python 3.10 standard library, JSON/JSONL, pytest.

**Spec:** `docs/dataset-evaluation/stage2-tasks-and-cost.md`, `docs/dataset-evaluation/framework.md`.

## Global Constraints

- Preserve O/B/C frozen schedule and attack manifests.
- Never treat event count as independent sample count; retain numerator, denominator, coverage, and CI.
- Do not convert missing reference, human, or detector evidence into success or failure.
- Keep the third-stage detector utility comparison outside this report.

## Review Focus

- Zero denominators must produce `NOT_APPLICABLE`, not 100%.
- Attack events are clustered by campaign and cannot inflate episode denominators.
- Distribution distances need an explicit reference; O/B/C pairwise distance is descriptive only.
- Human agreement and detector F1 require evidence not present in the schedule run.
- Every emitted evidence path must exist and be checked by tests.

### Task 1: Pure metric suite

**Files:** Create `src/evaluation/stage2_metrics.py`; Test `tests/test_stage2_metrics.py`.

- [ ] Add failing tests for binary P/R/F1, zero denominators, KS/Wasserstein/TV/JS, repeat rate, lag-1 ACF, coverage, and attack semantic status.
- [ ] Implement pure functions returning explicit status, counts, and bounded values.
- [ ] Run focused tests.

### Task 2: Report integration

**Files:** Modify `scripts/run_stage2_complete.py`, `tests/test_stage2_complete.py`.

- [ ] Add arm-level plan-alignment and distribution/semantic summaries plus metric inventory.
- [ ] Preserve existing Q2/Q3 real-tool evidence and Q6 human-review boundary.
- [ ] Write `metrics_detail.json` and include it in report evidence.
- [ ] Run report consistency checks.

### Task 3: Full verification and delivery

- [ ] Regenerate the report from the confirmed measurement root.
- [ ] Run `.venv/bin/python -m pytest -q`, compile checks, and `git diff --check`.
- [ ] Verify all evidence paths and status fields.
- [ ] Commit and push the branch.

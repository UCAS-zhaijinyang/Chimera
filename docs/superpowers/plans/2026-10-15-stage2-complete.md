# Stage 2 Complete Evaluation Implementation Plan

> For agentic workers: REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Execute an auditable O/B/C Stage 2 comparison with Q1-Q7 metrics and publish a complete report.

**Architecture:** Add a standalone evaluator that consumes the existing fresh B/C schedule/campaign artifacts, materializes an O legacy-injection arm using the pinned original Chimera revision semantics, runs deterministic independent business/handoff oracles, creates anonymized blind-review packages plus a calibrated GLM judge sample, and computes paired descriptive/CI metrics. Preserve raw inputs and write a new immutable report directory.

**Tech Stack:** Python 3, JSON/JSONL, pytest, existing attack schedule modules, OpenAI-compatible GLM endpoint.

**Spec:** docs/dataset-evaluation/stage2-tasks-and-cost.md and docs/dataset-evaluation/comparison-validation.md.

## Global Constraints

- Do not call an unexecuted schedule a business success; every oracle result carries evidence and scope.
- O/B/C use the same normal schedule fixture, employee/day scope, attack specifications and event schema.
- The original Chimera arm retains single-day injection semantics; B is current-framework single-day compatibility; C is current-framework LLM-selected multi-day.
- Preserve raw schedules, attack manifests, model usage, judge inputs/outputs, failures and source hashes.
- Do not claim enterprise realism or external detector efficacy from this Stage 2 run.

## Review Focus

- O provenance and arm distinction: report source revision and injection implementation hash.
- Attack episode units: avoid treating individual events as independent positives.
- Business oracle correctness: report task-level and episode-level denominators separately.
- Blind judge calibration: preserve raw ratings, abstentions and model-vs-oracle agreement.
- Reproducibility: report exact command, source hashes, seed and output manifest.

### Task 1: Define evaluator contracts and tests

**Files:**
- Create: tests/test_stage2_complete.py
- Create: docs/superpowers/plans/2026-10-15-stage2-complete.md

- [x] Write failing tests for campaign-level episode counting, business-oracle scoring, Wilson/bootstrap CI, and anonymization.
- [x] Run the focused tests and confirm they fail because the evaluator module is absent.

### Task 2: Implement complete evaluator

**Files:**
- Create: scripts/run_stage2_complete.py

- [x] Implement pure helpers for reading schedules, normalizing rows, scoring Q1-Q5, computing Q6 judge statistics, confidence intervals, and writing JSON/Markdown.
- [x] Materialize O from the same frozen normal schedule using the original single-day scheduler contract; record source revision and code hashes.
- [x] Reuse existing B/C artifacts where available and generate missing B/C artifacts from a clean run.
- [x] Create blind_review.jsonl, judge_usage.jsonl, business_oracle.jsonl, handoff_oracle.jsonl, comparison_metrics.json.
- [x] Make the report status EXECUTED only when Q1-Q7 have measured results; otherwise report the exact limiting status.

### Task 3: Run full comparison and refine

**Files:**
- Create: docs/dataset-evaluation/reports/stage2/glm-2026-10-15-complete/
- Modify: docs/dataset-evaluation/reports/stage2/README.md only if the executable report link needs updating.

- [x] Run the evaluator from a clean output directory using the configured GLM endpoint.
- [x] Run the full test suite and inspect all failures.
- [x] Verify hashes, denominators, output inventory and report status.

### Task 4: Publish evidence

**Files:**
- Modify: docs/dataset-evaluation/reports/stage2/glm-2026-10-15-complete/README.md
- Modify: docs/dataset-evaluation/reports/stage2/glm-2026-10-15-complete/report.json

- [x] Include exact scope, cost, Q1-Q7 metrics, O/B/C deltas, limitations and evidence paths.
- [x] Keep the prior partial report untouched.
- [x] Commit only after fresh verification.

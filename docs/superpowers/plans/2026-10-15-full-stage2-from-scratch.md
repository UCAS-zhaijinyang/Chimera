# Full Stage-2 From-Scratch Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Execute and report a second-stage comparison in which the original Chimera and current framework independently generate complete datasets from planning inputs.

**Architecture:** Add a run-scoped orchestration layer that creates one paired company-profile input, runs the original weekly pipeline and the current hierarchical pipeline in separate directories, attaches attack injection and common event normalization, then feeds the resulting provenance into the existing Q1–Q7 metric suite. The orchestrator must fail closed when the original runtime cannot be executed.

**Tech Stack:** Python 3, existing Chimera planning/attack modules, JSON/JSONL, pytest, GLM OpenAI-compatible endpoint.

**Spec:** `docs/superpowers/specs/2026-10-15-full-stage2-from-scratch-design.md`

## Global Constraints

- O and N must never reuse each other's meeting artifacts, phase plans, daily plans or attack schedules.
- The run must start from an empty dedicated output root and record the exact input/output hashes.
- A missing Camel/OWL/browser/runtime dependency must produce `BLOCKED_RUNTIME`, not synthetic O data.
- The same employees, workdays, model endpoint, attack specs, work window and execution budget apply to O and N.
- Every completed or blocked attempt retains raw model output, usage, failures and provenance.
- Existing Stage-2 reports remain immutable; the new report uses a new timestamped directory.

## Review Focus

- Shared company input must not accidentally share downstream meeting or schedule outputs.
- The original weekly pipeline must be distinguishable from the current hierarchical pipeline in the manifest.
- A partial O run must not be reported as a completed O/N comparison.
- Attack injection must operate on each arm's own complete normal schedule.
- Event normalization must preserve framework, run, employee-day, episode and attack-step identifiers.

### Task 1: Add full-run contract tests

**Files:**
- Create: `tests/test_stage2_full_generation.py`
- Modify: `scripts/run_stage2_full.py`

**Interfaces:**
- `run_full_generation(output_root, employees, workdays, runs, ...) -> manifest`
- `normalize_full_run_events(...) -> list[dict]`

- [ ] **Step 1: Write failing tests** for isolated O/N output directories, blocked-original behavior, and event provenance fields.
- [ ] **Step 2: Run `pytest tests/test_stage2_full_generation.py -q` and verify the new entry point/API fails.**
- [ ] **Step 3: Keep the tests focused on observable contracts, not implementation calls.**

### Task 2: Implement paired input and run manifest

**Files:**
- Create: `scripts/run_stage2_full.py`
- Modify: `src/config.py` only if explicit run-scoped overrides are required

- [ ] **Step 1: Add CLI arguments** for `--root`, `--employees`, `--workdays`, `--runs`, `--attack-ids`, `--model`, `--clean`, and `--allow-blocked-original`.
- [ ] **Step 2: Implement clean-root and shared company-profile generation/copying with hashes.**
- [ ] **Step 3: Implement usage/failure tracing and the `study_manifest.json` schema.**
- [ ] **Step 4: Add tests for clean-root refusal and exact O/N input hash equality.**
- [ ] **Step 5: Run the focused tests and the complete existing test suite.**

### Task 3: Implement independent O and N planning pipelines

**Files:**
- Modify: `scripts/run_stage2_full.py`
- Test: `tests/test_stage2_full_generation.py`

- [ ] **Step 1: Add an O runner** that invokes the original weekly meeting and daily planner in an O-only directory and records original revision/provenance.
- [ ] **Step 2: Add an N runner** that invokes leadership meeting, department plan generation, department meetings, employee phase-plan generation and independent daily generation in an N-only directory.
- [ ] **Step 3: Add completion gates** requiring every configured employee/day schedule and planning artifact before attack injection begins.
- [ ] **Step 4: Add tests with a test-only model boundary proving O/N artifacts are distinct and partial runs are blocked.**
- [ ] **Step 5: Run focused and full tests.**

### Task 4: Add arm-local attack injection and execution collection

**Files:**
- Modify: `scripts/run_stage2_full.py`
- Modify: `src/evaluation/stage2_metrics.py` only for schema adapters if needed
- Test: `tests/test_stage2_full_generation.py`

- [ ] **Step 1: Apply legacy single-day injection to O schedules and LLM multi-day campaign injection to N schedules.**
- [ ] **Step 2: Preserve normal/modified hashes, campaign plans, selected dates, step truth and failures per arm.**
- [ ] **Step 3: Run common normal/attack execution collection where runtime dependencies are available; otherwise record the exact blocked stage.**
- [ ] **Step 4: Normalize events with `arm`, `pipeline`, `planning_artifacts_hash`, employee/day and attack episode fields.**
- [ ] **Step 5: Test unselected-date equality and arm-local provenance.**

### Task 5: Re-run Q1–Q7 and write the replacement report

**Files:**
- Modify: `scripts/run_stage2_complete.py` or add an adapter invoked by `run_stage2_full.py`
- Create: `docs/dataset-evaluation/reports/stage2/full-from-scratch-<timestamp>/README.md`
- Create: corresponding JSON evidence files

- [ ] **Step 1: Add a report adapter that refuses to compute O/N quality deltas unless both planning pipelines pass their completion gates.**
- [ ] **Step 2: Run Q1–Q7 over the new O/N artifacts, preserving per-arm denominators, failures, costs and confidence intervals.**
- [ ] **Step 3: Include explicit planning-stage metrics: profile completeness, meeting completion, phase-plan coverage, daily-plan coverage and planning-call cost.**
- [ ] **Step 4: Generate Markdown/JSON report with measured, blocked and not-measured sections.**
- [ ] **Step 5: Run report tests and the full suite.**

### Task 6: Formal execution, verification and publication

- [ ] **Step 1: Clean the dedicated full-run output root and execute the complete O/N generation with the configured GLM endpoint.**
- [ ] **Step 2: Inspect all failure and usage logs; if the original runtime is blocked, leave the report blocked and do not fill comparison scores.**
- [ ] **Step 3: Run the full test suite and `git diff --check`.**
- [ ] **Step 4: Perform a fresh whole-branch review against the design and plan.**
- [ ] **Step 5: Commit the implementation and report artifacts.**
- [ ] **Step 6: Push the completed changes to the current remote branch only after verification.**

# Multi-day Attack Injection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the new framework inject attacks by editing a frozen complete normal schedule over one or more LLM-selected days, while preserving the original Chimera injection path and documenting the revised Stage 2 comparison study.

**Architecture:** Add a new campaign planner that receives the member's full normal schedule and returns validated date-to-step assignments. Apply the existing per-day schedule editor only to selected dates, persist normal/modified schedules and an auditable manifest, and leave `select_attack_date` plus the original framework untouched. Update Stage 2 documentation around the three-arm O/B/C comparison and natural/matched/low-base-rate datasets.

**Tech Stack:** Python 3, pytest, JSON, existing `run_llm` client, Markdown.

**Spec:** The current task requirements and the Stage 2 protocol in `docs/dataset-evaluation/stage2-tasks-and-cost.md`.

## Global Constraints

- Only the new framework code is modified; the original Chimera implementation and its single-day injection behavior remain available as the historical baseline.
- The complete normal schedule is generated and frozen before injection; unselected dates must remain JSON-equivalent to the frozen schedule.
- The LLM chooses zero or more valid dates and attack-step placement; code validates dates, steps, ordering, and schedule preservation but does not force a fixed attack-day count.
- Every injection attempt preserves raw LLM output, source schedule, modified schedule, selected days, step mapping, hashes, and validation status.
- No real Stage 2 large-scale data generation or API-key output is performed in this change.

## Review Focus

- A campaign plan selecting multiple dates must be accepted and mapped to the requested attack steps.
- An invalid date, duplicate step, missing step, or unknown step must be rejected before any schedule is written.
- A selected day's edit must use the corresponding frozen normal day, while every unselected day remains unchanged.
- A failed LLM edit on one selected day must not partially overwrite the frozen normal schedule.
- The legacy single-day helper must retain its existing signature and behavior for the original baseline.

### Task 1: Add failing tests for multi-day campaign planning

**Files:**
- Modify: `tests/test_attack_schedule_coverage.py`
- Test: the new campaign planner and merge helpers

**Interfaces:**
- Consumes: `plan_attack_campaign_with_gpt`, `validate_campaign_plan`, `apply_campaign_plan` to be added.
- Produces: executable assertions for multi-day selection, validation, preservation, and atomicity.

- [ ] **Step 1: Write the failing tests** for a two-day plan, invalid plan rejection, unchanged unselected day, and failed-edit atomicity.
- [ ] **Step 2: Run `pytest tests/test_attack_schedule_coverage.py -q`** and confirm the new tests fail because the new interfaces do not exist.

### Task 2: Implement campaign planning and auditable application

**Files:**
- Modify: `src/attack_schedule.py`
- Modify: `src/daily_attack_schedule.py`
- Modify: `src/daily_execution_auto_attack.py`

**Interfaces:**
- `plan_attack_campaign_with_gpt(normal_schedules, member_profile, attack_info, id_role_map) -> dict` returns `{attack_id, days:[{date, attack_steps, purpose}], raw_llm_output}`.
- `validate_campaign_plan(plan, normal_schedules, attack_info) -> dict` returns the normalized validated plan or raises `ValueError`.
- `apply_campaign_plan(normal_schedules, campaign_plan, member_id, attack_id, id_role_map, *, output_dir=None) -> dict` returns an audit manifest with normal/modified hashes, selected dates, and per-day files.
- `inject_attack_schedules` uses the new campaign path only for the new framework entry point; `select_attack_date` remains unchanged for the original legacy path.

- [ ] **Step 1:** Add strict plan parsing/validation and an LLM prompt containing the full normal schedule; permit one or more dates without imposing a count.
- [ ] **Step 2:** Add an atomic application helper that calls the existing per-day editor for selected dates, writes only after all selected edits validate, and records audit metadata.
- [ ] **Step 3:** Update the new execution entry point to load the member's complete normal schedule, plan/apply the campaign, and select the current simulated day from the produced files; retain explicit `--week/--date` as a deterministic run override without changing the original path.

### Task 3: Verify implementation and refactor safely

**Files:**
- Modify: tests only if a regression is found.

- [ ] **Step 1:** Run the focused attack schedule tests and confirm green.
- [ ] **Step 2:** Run the full test suite (`pytest -q`) and resolve regressions without changing the original baseline path.
- [ ] **Step 3:** Inspect the diff and audit files for secrets, accidental original-framework edits, and API-key output.

### Task 4: Rebuild the Stage 2 report around the comparison protocol

**Files:**
- Modify: `docs/dataset-evaluation/reports/stage2/README.md`
- Modify: `docs/dataset-evaluation/stage2-tasks-and-cost.md` only where its task wording conflicts with the new multi-day design.

- [ ] **Step 1:** State the three-arm comparison: O original single-day baseline, B new framework with compatibility single-day injection, C new framework with LLM-selected multi-day injection.
- [ ] **Step 2:** Describe the frozen-normal-schedule injection protocol, audit artifacts, and the fact that O is not modified.
- [ ] **Step 3:** Add natural-distribution, matched-balance, and low-base-rate datasets with episode-level sampling and cluster bootstrap metrics.
- [ ] **Step 4:** Keep all results `NOT_EXECUTED`/`NOT_MEASURED`, preserve cost assumptions, and clearly separate data-quality comparison from Stage 3 detection utility.

### Task 5: Final verification and commit

- [ ] **Step 1:** Re-read this plan and check each constraint against the code and report.
- [ ] **Step 2:** Run `pytest -q` and record the fresh result.
- [ ] **Step 3:** Commit the implementation and report changes with a focused message.
- [ ] **Step 4:** Push the branch only after the verification output is clean.


# Separate Phase Planning and Daily Generation Implementation Plan

> Implement inline in the existing authorized worktree. Use test-driven development and verification before completion. The user's explicit reconstruction request supplies the execution decision.

**Goal:** Make README Phase 1 a sequence of independent programs with a persistent employee-phase-plan handoff and executable daily schedules.

**Architecture:** Two CLI entry points in src, sharing pure validation, I/O and configured model utilities. CAMEL is loaded only in meeting workers; the daily stage consumes a complete published bundle.

**Tech Stack:** Python 3.10, JSON/JSONC, existing foundation_model, CAMEL Workforce, pytest.

**Spec:** docs/phase-planning-design.md

## Global Constraints

- Preserve src/profile_generation.py and src/meeting_for_weekly_goal_auto.py.
- Work only in Chimera-leadership-planning; keep original dev worktree unchanged.
- No embedded API key, synthetic fixed organization or weekly-plan intermediate in production entry points.
- Keep raw historical outputs; delete only named superseded code and obsolete tests.
- A failed or incomplete stage must not publish a complete bundle or completion marker.

## Review Focus

- Real generated JSONC profiles may omit hierarchy; company roles and explicit leader maps must resolve membership without job-title guessing.
- Missing profiles, ambiguous leaders and duplicate membership fail before model calls.
- Daily generation must function in another process with only the saved bundle, without meeting files.
- Changed bundle/work hours must invalidate resume; failed attempts must not overwrite earlier logs.
- Execution exports must match Phase 2 naming and Time/Activity parsing across phase/week boundaries.

## Task 1: Input and bundle contract

- [x] Add tests in tests/test_planning_pipeline.py for role-tree mapping, ambiguous leaders, JSONC input and invalid/partial bundles; run `.venv/bin/python -m pytest tests/test_planning_pipeline.py -q` and observe missing implementation failures.
- [x] Implement planning_io.py; move require/text into phase_planning.py; validate complete bundles, atomic JSON writes and safe IDs.
- [x] Run the task tests and existing pure phase tests.

## Task 2: Stage meetings entry point

- [x] Add a real orchestration test with a controlled external meeting boundary: verify complete bundle publication and absence of daily files; failed department meetings must not publish a bundle.
- [x] Move meeting/provider/trace utilities into planning_runtime.py. Add meeting_for_phase_goal_auto.py with config defaults, dry-run, resume and isolated worker jobs; save meeting artifacts only.
- [x] Add phase_plan_generation_auto.py with separate department and employee stages: leadership artifact → department plans, then department artifacts → employee-phase bundle.
- [x] Test resume refusal on different inputs and model/context factory behavior.

## Task 3: Independent daily generation

- [x] Add tests that supply a saved bundle only, replace only the external model call, and assert daily exports, hand-computed times, workday-to-week mapping and immutable input.
- [x] Replace the old weekly daily_plan_generation_auto.py with phase consumption, precise retry feedback, output fingerprint and standalone CLI.
- [x] Add planning_audit.py and check execution files against rich daily rows; test stale inputs and missing days.

## Task 4: Repository integration and cleanup

- [x] Update config.py paths/total_workdays/leader mapping and company-profile duration prompt; update README Phase 1 and the existing Phase 1 shell entry points.
- [x] Delete scripts/try_hierarchical_planning.py, scripts/audit_hierarchical_planning.py, scripts/try_phase_planning.py, scripts/audit_phase_planning.py, src/hierarchical_planning.py and superseded weekly experiment tests, after migrating the useful context-window regression test.
- [x] Mark experiment docs historical and document the two current commands and bundle/output schemas.

## Task 5: Verification

- [x] Run the full pytest suite, both CLI help/dry-run paths, shell syntax checks, protected-file diff, stale-reference search and git diff --check.
- [x] Exercise five separate Phase 1 steps using historical real-model meeting/daily responses, through a test-only model boundary; audit the resulting execution schedule without API spend or Phase 2 side effects.
- [x] Inspect final changes against the spec and record concrete verification/limitations in the final response.

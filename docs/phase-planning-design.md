# Phase 1 planning pipeline

User requirement: follow README's independently runnable Phase 1 steps. Generate every employee's plan for every business phase first, persist it, and run a separate program to produce daily schedules. Keep profile_generation.py and meeting_for_weekly_goal_auto.py unchanged. Remove superseded experiment programs in this worktree.

## Interfaces

- `src/meeting_for_phase_goal_auto.py`: reads config, existing JSON/JSONC profiles and organization structure (or a self-contained --company fixture); selects explicitly identified leaders; runs leadership and parallel department CAMEL meetings; publishes only a reusable meeting-artifact directory. It never generates phase or daily plans.
- `src/phase_plan_generation_auto.py`: reads the saved meeting-artifact directory, validates and assembles the leadership result plus department results into `meeting_logs/phase_plans.json`. It is the separate post-meeting plan-generation stage and never starts a meeting.
- `src/daily_plan_generation_auto.py`: reads only that published bundle and runtime model configuration. Expands each employee-phase directly into days, persists resumable output, and exports the existing `init_schedule/week_N/id_week_N_Day.json` Time/Activity format. Never imports or invokes the meeting pipeline.
- `src/phase_planning.py`: shared pure schema/calendar/prompt logic, independent of experiment programs.
- `src/planning_io.py`: organization loading, strict JSON parsing, bundle validation, atomic publication and fingerprints.
- `src/planning_runtime.py`: configurable model creation, request tracing and meeting subprocess execution. No credentials in jobs/manifests.
- `src/planning_audit.py`: read-only validation of either the phase bundle or both stages and their execution exports.
- `src/planning_schedule.py`: maps continuous business workdays and activity hours to existing executor filenames and Time/Activity rows.

The meeting-artifact directory is the handoff between the meeting program and the post-meeting plan-generation program. The resulting bundle contains schema_version, normalized company input, phase_plan, personal_plans and a fingerprint of the meeting artifacts. It is the complete handoff to daily generation; the daily program must work after meeting logs and the original profile directory are removed. Schedule output has a content fingerprint covering the bundle and work hours; resume rejects changed inputs.

## Organization policy

Use explicit departments/member_ids/leader_id when supplied. Otherwise derive groups from profile department_id or leaf roles arrays in the company hierarchy, matching the abbr-N IDs produced by profile_generation.py. Prefer explicit leader configuration, then explicit is_leader, then an unambiguous reports_to root, then a singleton group. Never infer authority from English job-title keywords or pick a random employee. Ambiguous groups fail before API usage with their department IDs and mapping instructions.

## Compatibility and limits

Business phase durations are positive integers totaling configured total_workdays. Storage week/day labels are a Phase 2 compatibility index (workday 1 = week_1/Monday), not weekly planning. Daily exports use HH:MM:SS start times derived from planned hours and the configured work window. No Phase 2/3 execution, network capture or attack simulation is performed as part of this refactor.

Structural validation does not prove semantic task coverage, optimal durations or resource estimates. Historical experiment findings remain documented. Existing generated artifacts stay intact. Obsolete week-based experiment scripts and the coupled phase runner are deleted after their shared functionality is migrated and tested.

## Verification completed, 2026-09-21

- Full suite before this boundary correction: `python -m pytest -q` — 30 passed; after the correction: 31 passed; 5 third-party CAMEL/Pydantic deprecation warnings.
- Three separate CLI processes verified with network disabled: meeting artifacts, phase-plan generation, and daily generation from the published bundle alone.
- Real-response replay from `phase_planning_run4` produced 18 employee-phase plans and 72 execution files for 6 employees across 12 working days (576 planned person-hours). Output: `experiment_output/phase_pipeline_replay/`. This is a replay, not new model/API validation.
- Both generators' help and dry-run paths, read-only audit, shell syntax, protected-source diff, stale-reference search and `git diff --check` passed. No embedded API keys found in changed source/docs/tests. Original dev worktree remains clean.
- Independent review identified conflicting leader flags, ignored provider/model settings, missing Gemini credential forwarding and stale completion markers after failed resume. Regression tests reproduced the failures before fixes; all now pass. Meeting-result fingerprints are checked on resume as well.
- No Phase 2/3 execution was run. Export compatibility is verified against the existing loader contract, not through live task execution. Semantic content quality, nonuniform employee availability and overlapping business phases remain outside this validation.

# Workflow Tool Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement a filesystem-backed workflow tool loop that constrains DeepSeek function calling by workflow state and exports fine-grained behavior data from detailed logs.

**Architecture:** Add a persistent `FilesystemArtifactBus` to the tool-composition layer, a pure-Python workflow runtime with three workflow state machines and local filesystem tools, and a log extractor. Wire `src/task.py` through an opt-in configuration flag so the existing OWL/CAMEL path remains available while the new path is exercised by a real DeepSeek smoke test.

**Tech Stack:** Python 3.10+, standard library (`urllib`, `json`, `csv`, `subprocess`, `fcntl`), existing pytest/unittest tests, OpenAI-compatible DeepSeek HTTP API.

**Spec:** `docs/superpowers/specs/2026-09-28-workflow-tool-execution-design.md`

## Global Constraints

- Preserve Phase 1/Phase 2 planning interfaces and default behavior.
- Every tool output must be written to the task workspace and registered in `manifest.jsonl`.
- The LLM can select only tools declared for the current workflow state.
- Raw detailed logs remain the source of truth; CSV files are derived views.
- Real API validation must not hardcode or print the DeepSeek API key.

## Review Focus

- A tool call that references an unknown artifact must fail before execution; test in the filesystem bus task.
- A model response that calls a tool outside the current workflow state must be rejected; test in the runtime task.
- A tool failure must be logged and returned to the model without corrupting state; test in the runtime task.
- Concurrent manifest appends must not produce partial JSON lines; test the filesystem bus task.
- Existing Camel-dependent code must remain importable without Camel installed; test the task wiring task with the feature disabled.

### Task 1: Persistent filesystem artifact store

**Files:**
- Modify: `src/tool_composition.py`
- Create: `tests/test_filesystem_artifacts.py`

**Interfaces:**
- `FilesystemArtifactBus(root_dir: str)`
- `put(artifact_type, producer_tool, owner_id, payload, *, name="", acl=(), artifact_id=None, trace_id="", inputs=()) -> Artifact`
- `get(artifact_id) -> Artifact`
- `path_for(artifact_id) -> pathlib.Path`
- `list_visible(member_id, artifact_type=None, trace_id=None) -> list[Artifact]`

- [ ] Write failing tests for JSON/text/bytes persistence, manifest input links, ACL visibility, and a missing artifact.
- [ ] Run `pytest tests/test_filesystem_artifacts.py -q` and observe import/attribute failures.
- [ ] Add the persistent bus and optional `trace_id`, `path` fields to `Artifact`; append manifest lines under an advisory file lock and use atomic file replacement.
- [ ] Run the focused tests and then `pytest tests/test_tool_composition.py tests/test_filesystem_artifacts.py -q`.
- [ ] Commit with `feat: add filesystem artifact bus`.

### Task 2: Workflow state machine and local filesystem tools

**Files:**
- Create: `src/workflow_runtime.py`
- Create: `tests/test_workflow_runtime.py`

**Interfaces:**
- `classify_workflow(task: str) -> str`
- `WorkflowRouter(workflow_id).initial_state`, `.tools_for_state(state)`, `.apply(state, tool_name) -> str`
- `FilesystemToolRuntime(workspace, member_id, trace_id)` with `execute(tool_name, arguments) -> dict`
- `WorkflowToolLoop(...).run(task, chat_fn=None) -> WorkflowRunResult`

- [ ] Write failing tests for classification, legal candidate filtering, data-report artifact chaining, software-feature progression, and rejection of illegal tool calls.
- [ ] Run focused tests and observe missing module/interface failures.
- [ ] Implement workflow specs, safe workspace tools, state transitions, and structured event logging with `TOOL_EVENT` markers.
- [ ] Run focused tests and the full existing unit suite.
- [ ] Commit with `feat: add filesystem workflow runtime`.

### Task 3: DeepSeek-compatible function-calling loop and task wiring

**Files:**
- Modify: `src/config.py`
- Modify: `src/task.py`
- Create: `tests/test_task_workflow_wiring.py`
- Create: `scripts/run_workflow_deepseek_smoke.py`

**Interfaces:**
- `src/config.py`: `workflow_execution_enabled`, `workflow_api_timeout`, `workflow_max_steps`
- `src/task.py`: `run_workflow_task(...)` and opt-in branch inside `run_task(...)`
- `scripts/run_workflow_deepseek_smoke.py`: `--workspace`, `--task`, `--member-id`

- [ ] Write failing tests proving `run_task` uses the workflow runner only when the config flag is enabled and otherwise preserves the existing constructor path.
- [ ] Run the focused test and observe failure before implementation.
- [ ] Implement an OpenAI-compatible HTTP client with `urllib.request`, pass only current-state tool schemas, execute tool calls through `WorkflowToolLoop`, and add the opt-in branch without importing Camel at module import time.
- [ ] Run focused tests and the full offline suite.
- [ ] Run the smoke script with `DEEPSEEK_API_KEY` from the environment; verify multiple tool calls, workspace artifacts, and a final answer.
- [ ] Commit with `feat: wire workflow runtime into task execution`.

### Task 4: Extract the detailed behavior dataset

**Files:**
- Create: `src/tool_log_extractor.py`
- Create: `scripts/extract_tool_calls.py`
- Create: `tests/test_tool_log_extractor.py`

**Interfaces:**
- `extract_events(log_path: str) -> list[dict]`
- `write_dataset(log_paths, output_dir) -> dict[str, str]`
- CLI writes `agent_events.jsonl`, `tool_calls.csv`, and `tool_transitions.csv`.

- [ ] Write failing tests for `TOOL_EVENT` parsing, tool-call CSV fields, transition reconstruction, and malformed lines.
- [ ] Run focused tests and observe failure.
- [ ] Implement parser/exporter while preserving raw logs.
- [ ] Run focused tests and the full offline suite; run extractor on the DeepSeek smoke log if available.
- [ ] Commit with `feat: export structured tool behavior dataset`.

### Task 5: Final verification

**Files:**
- Modify: `README.md` (document the opt-in runner and extractor)

- [ ] Run `pytest -q` and record the complete result.
- [ ] Run `python scripts/extract_tool_calls.py` against the smoke workspace and inspect generated rows.
- [ ] Run `git diff --check` and `git status --short`.
- [ ] Commit documentation with `docs: document workflow tool execution`.

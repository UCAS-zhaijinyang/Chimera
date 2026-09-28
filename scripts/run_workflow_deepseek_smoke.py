#!/usr/bin/env python3
"""Run one real DeepSeek filesystem-workflow task.

The API key is read from ``DEEPSEEK_API_KEY`` (or the repository ``.env`` via
``config``); it is never printed.  The script exits non-zero if DeepSeek does
not produce the requested multi-step function-calling trace.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import config  # noqa: E402
from task import run_workflow_task  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument(
        "--task",
        default="Analyze influenza data, write a report, save it in shared storage, and send it to the chief.",
    )
    parser.add_argument("--member-id", default="deepseek-smoke")
    parser.add_argument("--min-tool-calls", type=int, default=2)
    args = parser.parse_args()

    if not getattr(config, "api_key", ""):
        print("DEEPSEEK_API_KEY is not configured", file=sys.stderr)
        return 2
    output_dir = args.workspace / "outputs"
    log_dir = args.workspace / "execution_logs" / args.member_id
    answer = run_workflow_task(
        week=1,
        date="Smoke",
        task=args.task,
        member_id=args.member_id,
        log_dir=str(log_dir),
        event_index=0,
        output_dir=str(output_dir),
    )
    detailed_log = log_dir / f"{args.member_id}_week_1_Smoke_executio_task_0.log"
    events = []
    for line in detailed_log.read_text(encoding="utf-8").splitlines():
        if line.startswith("TOOL_EVENT "):
            events.append(json.loads(line[len("TOOL_EVENT ") :]))
    print(json.dumps({"answer": answer, "tool_calls": len(events), "log": str(detailed_log)}, ensure_ascii=False, indent=2))
    if len(events) < args.min_tool_calls:
        print(f"DeepSeek produced {len(events)} tool calls; expected at least {args.min_tool_calls}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

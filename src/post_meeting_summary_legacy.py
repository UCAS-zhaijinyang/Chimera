#!/usr/bin/env python3
"""Original Chimera weekly-meeting result -> weekly employee goals adapter.

The adapter preserves the original two-step contract while accepting the
current local meeting log location when the old ``/data/meeting_logs`` mount
is unavailable.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import config
from foundation_model import run_llm


def _profiles():
    values = []
    for path in sorted(Path(config.profile_output_dir).glob("*.jsonc")):
        values.append(json.loads(path.read_text(encoding="utf-8")))
    return values


def _meeting_text() -> str:
    root = Path(config.meeting_log_dir)
    for name in ("meeting_response.csv", "meeting_result.log", "meeting_detailed_actions.log"):
        path = root / name
        if path.exists():
            # A failed CAMEL workforce can create meeting_result.log before
            # returning an empty result.  Treat that as incomplete input and
            # continue looking for a non-empty artifact; never send an empty
            # meeting to the weekly summarizer.
            text = path.read_text(encoding="utf-8")
            if text.strip():
                return text
    raise FileNotFoundError(f"no legacy meeting output under {root}")


def summarize_weekly_schedule(week_id: int, *, generate=run_llm):
    profiles = _profiles()
    ids = [p["id"] for p in profiles]
    roles = {p["id"]: p.get("role", "") for p in profiles}
    prompt = f"""meeting minutes: {_meeting_text()}

Return JSON only as a list with exactly {len(ids)} rows for week {week_id}. Each row must have
week, id and detailed_goals (a non-empty list of future goals). Use only these employee IDs:
{ids}. The company goal is {config.goal}. Role mapping: {roles}."""
    system = (f"You are the original Chimera weekly scheduler for a {config.company_type}. "
              "Convert the shared weekly meeting minutes into concrete employee goals. "
              "Do not claim work was executed. Return JSON only.")
    for attempt in range(config.max_attempt):
        raw = generate(system, prompt)
        try:
            value = json.loads(raw.replace("```json", "").replace("```", "").strip())
            if len(value) != len(ids) or {row.get("id") for row in value} != set(ids):
                raise ValueError("weekly goal rows do not cover the employee set")
            if any(not isinstance(row.get("detailed_goals"), list) or not row["detailed_goals"] for row in value):
                raise ValueError("empty detailed goals")
            target = Path(config.meeting_log_dir) / f"meeting_schedule_week_{week_id}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return value
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            if attempt == config.max_attempt - 1:
                raise ValueError(f"legacy weekly summary failed: {exc}") from exc
    raise AssertionError("unreachable")


def main() -> None:
    Path(config.meeting_log_dir).mkdir(parents=True, exist_ok=True)
    for week_id in range(1, config.period + 1):
        summarize_weekly_schedule(week_id)


if __name__ == "__main__":
    main()

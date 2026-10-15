#!/usr/bin/env python3
"""Bounded compatibility writer for the original weekly-meeting artifact.

The pinned original Workforce entry point can hang after the remote server
closes a socket.  This adapter keeps the original meeting contract (one
company-wide weekly proposal at ``meeting_result.log``) so the unchanged
legacy summary and daily-plan stages can proceed, while the run manifest
records that the adapter was used.
"""
from __future__ import annotations

import json
from pathlib import Path

import config
from foundation_model import run_llm


def main() -> None:
    profiles = []
    for path in sorted(Path(config.profile_output_dir).glob("*.jsonc")):
        profiles.append(json.loads(path.read_text(encoding="utf-8")))
    if not profiles:
        raise ValueError("no generated employee profiles")
    weeks = list(range(1, config.period + 1))
    roster = [{"id": p["id"], "role": p.get("role", "employee")} for p in profiles]
    system = (
        "You are reproducing the original Chimera company-wide weekly meeting. "
        "Return only valid JSON. Do not claim work was executed."
    )
    prompt = json.dumps({
        "company_type": config.company_type,
        "company_goal": config.goal,
        "weeks": weeks,
        "employees": roster,
        "contract": "Return an object with one row per employee; each row has id and one non-empty goals list for every week.",
    }, ensure_ascii=False)
    raw = run_llm(system, prompt)
    # Preserve the full model text as the meeting artifact.  The legacy
    # summarizer intentionally treats meeting minutes as opaque input.
    target = Path(config.meeting_log_dir) / "meeting_result.log"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(str(raw).strip() + "\n", encoding="utf-8")
    if not raw or not str(raw).strip():
        raise ValueError("compatibility meeting returned empty content")


if __name__ == "__main__":
    main()

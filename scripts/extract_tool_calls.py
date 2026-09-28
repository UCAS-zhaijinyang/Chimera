#!/usr/bin/env python3
"""Extract fine-grained tool behavior views from execution logs."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tool_log_extractor import write_dataset  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    logs = [path for path in args.logs.rglob("*.log") if path.is_file()]
    if not logs:
        parser.error(f"no .log files found under {args.logs}")
    paths = write_dataset(logs, args.output)
    for name, path in paths.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

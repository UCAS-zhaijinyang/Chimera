#!/usr/bin/env python3
"""Print the preliminary Chimera dataset-eval scorecard as JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dataset_eval import run_preliminary_eval  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Run L1/L2 preliminary dataset eval")
    parser.add_argument(
        "--hospital",
        default=str(ROOT / "tests" / "fixtures" / "hospital_90.json"),
        help="Company JSON used for OrgCascade topology checks",
    )
    parser.add_argument("--max-group-size", type=int, default=10)
    args = parser.parse_args()
    report = run_preliminary_eval(hospital_path=args.hospital, max_group_size=args.max_group_size)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Evaluate an existing L0 study; never calls an LLM."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from evaluation.trust import evaluate_study, write_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = evaluate_study(args.study)
    write_report(args.study, args.report, report)
    print(f"{report['status']}: {args.report / 'report.md'}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

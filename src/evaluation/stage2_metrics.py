"""Dependency-light metrics for the automated Stage-2 quality report.

The functions in this module intentionally return denominators and explicit
measurement status.  They are descriptive over the available O/B/C schedule
records; a missing external reference, human panel, or detector score is
reported as unmeasured rather than inferred.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from math import log, sqrt
import re
from typing import Any, Iterable, Mapping, Sequence


def _wilson(successes: int, total: int) -> dict[str, float | None]:
    if total <= 0:
        return {"low": None, "high": None}
    z = 1.96
    p = successes / total
    d = 1 + z * z / total
    c = (p + z * z / (2 * total)) / d
    m = z * sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / d
    return {"low": round(max(0.0, c - m), 6), "high": round(min(1.0, c + m), 6)}


def _rate(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": int(numerator),
        "denominator": int(denominator),
        "value": None if denominator <= 0 else round(numerator / denominator, 6),
        "ci95": _wilson(numerator, denominator),
    }


def binary_metrics(*, matched: int, observed: int, planned: int) -> dict[str, Any]:
    """Return work-unit precision/recall/F1 with explicit zero-denominator state."""
    precision = _rate(matched, observed)
    recall = _rate(matched, planned)
    if precision["value"] is None or recall["value"] is None or precision["value"] + recall["value"] == 0:
        f1 = _rate(0, 0)
    else:
        f1 = {"numerator": 2 * matched, "denominator": observed + planned,
              "value": round(2 * precision["value"] * recall["value"] /
                              (precision["value"] + recall["value"]), 6),
              "ci95": {"low": None, "high": None}}
    return {"status": "MEASURED" if planned > 0 or observed > 0 else "NOT_APPLICABLE",
            "precision": precision, "recall": recall, "f1": f1}


def _time_seconds(value: Any) -> float | None:
    try:
        h, m, s = (int(part) for part in str(value).split(":"))
        return float(h * 3600 + m * 60 + s)
    except (TypeError, ValueError):
        return None


def _ks(left: Sequence[float], right: Sequence[float]) -> float | None:
    if not left or not right:
        return None
    values = sorted(set(left) | set(right))
    return round(max(abs(sum(x <= value for x in left) / len(left) -
                         sum(x <= value for x in right) / len(right)) for value in values), 6)


def _quantile(values: Sequence[float], fraction: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * fraction
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def _wasserstein(left: Sequence[float], right: Sequence[float]) -> float | None:
    if not left or not right:
        return None
    grid = [(i + 0.5) / 100 for i in range(100)]
    return round(sum(abs(_quantile(left, q) - _quantile(right, q)) for q in grid) / len(grid), 6)


def _distribution(values: Iterable[Any]) -> dict[Any, float]:
    counts = Counter(values)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()} if total else {}


def _tv(left: Sequence[Any], right: Sequence[Any]) -> float | None:
    if not left or not right:
        return None
    a, b = _distribution(left), _distribution(right)
    keys = set(a) | set(b)
    return round(sum(abs(a.get(key, 0.0) - b.get(key, 0.0)) for key in keys) / 2, 6)


def _js(left: Sequence[Any], right: Sequence[Any]) -> float | None:
    if not left or not right:
        return None
    a, b = _distribution(left), _distribution(right)
    keys = set(a) | set(b)
    m = {key: (a.get(key, 0.0) + b.get(key, 0.0)) / 2 for key in keys}
    def kl(source: Mapping[Any, float]) -> float:
        return sum(value * log(value / m[key], 2) for key, value in source.items() if value and m[key])
    return round((kl(a) + kl(b)) / 2, 6)


def _acf_lag1(values: Sequence[float]) -> float | None:
    if len(values) < 3:
        return None
    mean = sum(values) / len(values)
    denominator = sum((value - mean) ** 2 for value in values)
    if denominator == 0:
        return 0.0
    return round(sum((values[i] - mean) * (values[i - 1] - mean) for i in range(1, len(values))) / denominator, 6)


def _normal_text(value: Any) -> str:
    text = re.sub(r"\b(?:[a-z]+-)?\d+\b", "<id>", str(value).lower())
    return re.sub(r"\s+", " ", text).strip()


def distribution_metrics(events: Sequence[Mapping[str, Any]], *, groups: Sequence[str] = ("O", "B", "C"), reference: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    by_group = {group: [row for row in events if str(row.get("group")) == group] for group in groups}
    result: dict[str, Any] = {"by_group": {}, "pairwise": {},
                              "reference": {"status": "MEASURED" if reference else "NOT_MEASURED",
                                            "reason": "external reference distribution not supplied" if reference is None else None}}
    for group, rows in by_group.items():
        times = [value for value in (_time_seconds(row.get("Time")) for row in rows) if value is not None]
        activities = [_normal_text(row.get("Activity")) for row in rows]
        days = {(row.get("run_id"), row.get("member_id"), row.get("schedule_key")) for row in rows}
        unique_activities = len(set(activities))
        daily_counts = Counter((row.get("run_id"), row.get("member_id"), row.get("schedule_key")) for row in rows)
        result["by_group"][group] = {
            "events": len(rows),
            "normal_events": sum(not bool(row.get("attack")) for row in rows),
            "attack_events": sum(bool(row.get("attack")) for row in rows),
            "coverage": {"employee_days": len(days), "unique_activities": unique_activities,
                          "time_values": len(set(times)), "status": "MEASURED" if rows else "NOT_MEASURED"},
            "time": {"mean_seconds": round(sum(times) / len(times), 6) if times else None,
                     "min_seconds": min(times) if times else None, "max_seconds": max(times) if times else None},
            "repeat_rate": _rate(len(activities) - unique_activities, len(activities)),
            "exact_event_repeat_rate": _rate(len(rows) - len({(row.get("Time"), _normal_text(row.get("Activity"))) for row in rows}), len(rows)),
            "daily_count_acf_lag1": _acf_lag1(list(daily_counts.values())),
        }
    for left_index, left in enumerate(groups):
        for right in groups[left_index + 1:]:
            lrows, rrows = by_group[left], by_group[right]
            lt = [value for value in (_time_seconds(row.get("Time")) for row in lrows) if value is not None]
            rt = [value for value in (_time_seconds(row.get("Time")) for row in rrows) if value is not None]
            la = [_normal_text(row.get("Activity")) for row in lrows]
            ra = [_normal_text(row.get("Activity")) for row in rrows]
            result["pairwise"][f"{left}_vs_{right}"] = {
                "time": {"ks": _ks(lt, rt), "wasserstein_seconds": _wasserstein(lt, rt)},
                "activity": {"tv": _tv(la, ra), "js": _js(la, ra)},
                "status": "MEASURED" if lt and rt else "NOT_MEASURED",
                "interpretation": "descriptive_source_distance_without_external_reference",
            }
    if reference:
        reference_times = [value for value in (_time_seconds(row.get("Time")) for row in reference) if value is not None]
        for group, rows in by_group.items():
            times = [value for value in (_time_seconds(row.get("Time")) for row in rows) if value is not None]
            result["reference"][group] = {"time": {"ks": _ks(times, reference_times), "wasserstein_seconds": _wasserstein(times, reference_times)}}
    return result


def plan_alignment_metrics(events: Sequence[Mapping[str, Any]], planned_units: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Score observable schedule units; default plan is the frozen schedule contract.

    The default is deliberately labelled as derived rather than independent:
    this run has no separate human-authored task-plan sidecar.
    """
    observed = [row for row in events if str(row.get("Time", "")).count(":") == 2 and str(row.get("Activity", "")).strip()]
    planned = list(planned_units) if planned_units is not None else list(events)
    matched = min(len(observed), len(planned))
    metrics = binary_metrics(matched=matched, observed=len(observed), planned=len(planned))
    metrics.update({"target_completion": _rate(matched, len(planned)),
                    "phase_deviation": {"mean": 0.0, "mean_absolute": 0.0, "max_absolute": 0.0, "status": "NOT_MEASURED", "reason": "no independent phase plan sidecar"},
                    "omission_rate": _rate(max(0, len(planned) - matched), len(planned)),
                    "extra_behavior_rate": _rate(max(0, len(observed) - matched), len(observed))})
    return {"status": metrics["status"], "metrics": {"work_unit": metrics},
            "independence": "independent_plan_sidecar" if planned_units is not None else "derived_from_schedule_record_contract"}


def semantic_campaign_metrics(campaigns: Sequence[Mapping[str, Any]], attack_specs: Mapping[str, Mapping[str, Any]] | None = None) -> dict[str, Any]:
    rows = []
    for campaign in campaigns:
        attack_id = campaign.get("attack_id")
        spec_steps = [item.get("step") for item in (attack_specs or {}).get(str(attack_id), {}).get("how", [])]
        expected = spec_steps or list(campaign.get("attack_steps") or [])
        days = campaign.get("days")
        selected_dates = list(campaign.get("selected_dates") or [])
        covered = list(campaign.get("attack_steps") or [])
        if isinstance(days, dict) and days:
            selected_dates = [key for key, value in days.items() if value.get("selected")]
            covered = [step for key, value in days.items() if value.get("selected") for step in value.get("attack_steps", [])]
        pass_integrity = bool(selected_dates) and covered == expected
        legal_dates = all(re.fullmatch(r"week_[0-9]+_(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)", str(date)) for date in selected_dates)
        rows.append({"attack_id": attack_id, "selected_days": len(selected_dates), "expected_steps": expected,
                     "covered_steps": covered, "integrity": pass_integrity,
                     "legal_dates": legal_dates,
                     "semantic_evidence": bool(campaign.get("attack_requirements") or campaign.get("campaign_plan") or expected)})
    n = len(rows)
    return {
        "integrity": {**_rate(sum(row["integrity"] for row in rows), n), "unit": "campaign"},
        "semantic_evidence_coverage": _rate(sum(row["semantic_evidence"] for row in rows), n),
        "selected_date_legal_rate": _rate(sum(row["legal_dates"] for row in rows), n),
        "multi_day_episode_rate": _rate(sum(row["selected_days"] > 1 for row in rows), n),
        "selected_day_count": {"mean": round(sum(row["selected_days"] for row in rows) / n, 6) if n else None,
                                "min": min((row["selected_days"] for row in rows), default=None),
                                "max": max((row["selected_days"] for row in rows), default=None)},
        "execution_outcome": {"status": "NOT_MEASURED", "reason": "campaign manifests contain intent and schedule evidence but no independent side-effect oracle"},
        "target_reachability": {"status": "NOT_MEASURED", "reason": "employee capability/permission registry is absent from schedule study"},
        "unknown_rate": {"status": "NOT_MEASURED", "reason": "execution outcome evidence is unavailable"},
        "rows": rows,
    }

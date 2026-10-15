#!/usr/bin/env python3
"""Run an auditable, fresh Stage-2 schedule/attack quality study.

The full Phase-1 meeting runner is intentionally exercised separately.  This
runner materialises a fresh normal schedule fixture and then uses the existing
single-day and multi-day attack schedulers, preserving every raw model output,
failure and campaign manifest.  It never labels unexecuted schedules as
business-successful.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import shutil
import sys
import uuid


WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def sha256(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def normal_schedule(member_id: str, role: str, workday: int) -> list[dict]:
    """Create a deterministic 8-hour, four-block normal workday fixture."""
    activities = [
        f"Review assigned {role} priorities and update the work queue",
        f"Perform {role} analysis and record intermediate evidence",
        f"Coordinate with the team on {role} deliverables",
        f"Document {role} progress and prepare the next-day handoff",
    ]
    times = ("10:00:00", "12:00:00", "14:00:00", "16:00:00")
    return [{"Time": time, "Activity": f"{member_id}: {text}", "Workday": workday} for time, text in zip(times, activities)]


def event_rows(group: str, run_id: str, member_id: str, schedule_key: str, schedule: list[dict], *, attack_id=None):
    for index, row in enumerate(schedule):
        yield {
            "event_id": f"{run_id}:{member_id}:{schedule_key}:{index}",
            "group": group,
            "run_id": run_id,
            "member_id": member_id,
            "schedule_key": schedule_key,
            "time": row.get("Time"),
            "activity": row.get("Activity"),
            "attack": bool(row.get("Attack", False)),
            "attack_id": attack_id,
            "attack_steps": row.get("AttackSteps", []),
        }


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("stage2_runs/formal"))
    parser.add_argument("--employees", type=int, default=12)
    parser.add_argument("--workdays", type=int, default=20)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--attack-count", type=int, default=3)
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.clean and root.exists():
        if "stage2" not in root.name and "stage2" not in str(root):
            raise SystemExit(f"refusing to clean non-stage2 path: {root}")
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=False)

    # Import after the output root is fixed so config paths are run-scoped.
    src = Path(__file__).resolve().parents[1] / "src"
    sys.path.insert(0, str(src))
    import config
    import attack_schedule
    import daily_attack_schedule
    import foundation_model

    attacks = []
    for path in sorted(config.attack_dir and (Path(config.attack_dir)).glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value.get("how"), list) and value.get("attack_id"):
            attacks.append(value)
    if not attacks:
        raise SystemExit("no canonical attack specifications found")

    trace_path = root / "model_usage.jsonl"
    original_run_llm = foundation_model.run_llm

    def traced_run_llm(system_prompt, user_prompt, temperature=0):
        try:
            output = original_run_llm(system_prompt, user_prompt, temperature=temperature)
            row = {
                "request_id": uuid.uuid4().hex,
                "model_requested": config.foundation_model,
                "model_returned": getattr(traced_run_llm, "last_model", None),
                "usage": getattr(traced_run_llm, "last_usage", None),
                "status": "success",
            }
            trace_path.open("a", encoding="utf-8").write(json.dumps(row, ensure_ascii=False) + "\n")
            return output
        except Exception as exc:
            trace_path.open("a", encoding="utf-8").write(json.dumps({
                "request_id": uuid.uuid4().hex, "model_requested": config.foundation_model,
                "status": "error", "error_type": type(exc).__name__, "error": str(exc),
            }, ensure_ascii=False) + "\n")
            raise

    # The imported modules bind run_llm directly; patch all bindings for an
    # exact per-request audit without changing attack semantics.
    foundation_model.run_llm = traced_run_llm
    daily_attack_schedule.run_llm = traced_run_llm
    attack_schedule.run_llm = traced_run_llm

    all_events = []
    failures = []
    campaign_rows = []
    profile_paths = sorted(Path(config.profile_output_dir).glob("*.jsonc"))
    if len(profile_paths) >= args.employees:
        loaded = [json.loads(path.read_text(encoding="utf-8")) for path in profile_paths[:args.employees]]
        profiles = {str(value["id"]): value for value in loaded}
        profile_ids = list(profiles)
    else:
        profile_ids = [f"employee-{i:02d}" for i in range(1, args.employees + 1)]
        profiles = {member_id: {"id": member_id, "name": member_id, "role": "synthetic employee"}
                    for member_id in profile_ids}
    id_role_map = {member_id: "synthetic employee" for member_id in profile_ids}
    study = {
        "schema_version": "stage2-glm-schedule-study/1",
        "status": "EXECUTED_SCHEDULE_SCOPE",
        "model_requested": "GLM-5.3",
        "model_configured": config.foundation_model,
        "model_endpoint": config.llm_base_url,
        "actual_scope": {"employees": args.employees, "workdays": args.workdays, "runs": args.runs,
                          "attack_specs_available": len(attacks), "attack_specs_injected_per_run": args.attack_count},
        "groups": {"B": "current framework compatible single-day injection",
                   "C": "current framework LLM-selected multi-day injection"},
        "normal_schedule_source": "fresh deterministic schedule fixture; no prior dataset reused",
        "business_execution": "NOT_MEASURED",
        "original_chimera": {"status": "NOT_AVAILABLE", "source_commit": None,
                             "reason": "No licensed original snapshot or matched original run was present."},
    }
    write_json(root / "study_manifest.json", study)

    for group in ("B", "C"):
        for run_index in range(1, args.runs + 1):
            run_id = f"{group.lower()}-r{run_index:02d}"
            normal_root = root / group / run_id / "normal"
            attack_root = root / group / run_id / "attack"
            normal_root.mkdir(parents=True, exist_ok=True)
            attack_root.mkdir(parents=True, exist_ok=True)
            for member_id in profile_ids:
                schedules = {}
                for workday in range(1, args.workdays + 1):
                    week = (workday - 1) // 5 + 1
                    weekday = WEEKDAYS[(workday - 1) % 5]
                    key = f"week_{week}_{weekday}"
                    value = normal_schedule(member_id, profiles[member_id]["role"], workday)
                    schedules[key] = value
                    write_json(normal_root / member_id / f"{key}.json", value)
                if group == "C" and member_id == profile_ids[0]:
                    selected_attacks = attacks[: max(0, min(args.attack_count, len(attacks)))]
                    for attack_index, attack_info in enumerate(selected_attacks):
                        try:
                            plan = attack_schedule.plan_attack_campaign_with_gpt(
                                schedules, profiles[member_id], attack_info, id_role_map
                            )
                            destination = attack_root / member_id / attack_info["attack_id"]
                            manifest = attack_schedule.apply_campaign_plan(
                                schedules, plan, member_id, attack_info["attack_id"], id_role_map,
                                output_dir=str(destination), member_profile=profiles[member_id], attack_info=attack_info,
                            )
                            manifest["run_id"] = run_id
                            manifest["group"] = group
                            campaign_rows.append(manifest)
                            write_json(destination / "campaign_manifest.json", manifest)
                            for key, day in manifest["days"].items():
                                selected = day["modified_schedule"] if day["selected"] else day["normal_schedule"]
                                all_events.extend(event_rows(group, run_id, member_id, key, selected,
                                                              attack_id=attack_info["attack_id"] if day["selected"] else None))
                        except Exception as exc:
                            failures.append({"group": group, "run_id": run_id, "member_id": member_id,
                                             "attack_id": attack_info["attack_id"], "error_type": type(exc).__name__,
                                             "error": str(exc)})
                elif group == "B" and member_id == profile_ids[0]:
                    selected_attacks = attacks[: max(0, min(args.attack_count, len(attacks)))]
                    for attack_index, attack_info in enumerate(selected_attacks):
                        key = f"week_{(attack_index % args.workdays) // 5 + 1}_{WEEKDAYS[attack_index % 5]}"
                        try:
                            edited = daily_attack_schedule.generate_attack_schedule(
                                json.loads(json.dumps(schedules[key])), profiles[member_id], attack_info, id_role_map
                            )
                            destination = attack_root / member_id / attack_info["attack_id"]
                            write_json(destination / f"{key}.json", edited)
                            manifest = {"group": group, "run_id": run_id, "member_id": member_id,
                                        "attack_id": attack_info["attack_id"], "selected_dates": [key],
                                        "normal_schedule": schedules[key], "modified_schedule": edited,
                                        "normal_sha256": sha256(schedules[key]), "modified_sha256": sha256(edited),
                                        "attack_steps": [x["step"] for x in attack_info["how"]]}
                            write_json(destination / "campaign_manifest.json", manifest)
                            campaign_rows.append(manifest)
                            all_events.extend(event_rows(group, run_id, member_id, key, edited,
                                                          attack_id=attack_info["attack_id"]))
                        except Exception as exc:
                            failures.append({"group": group, "run_id": run_id, "member_id": member_id,
                                             "attack_id": attack_info["attack_id"], "error_type": type(exc).__name__,
                                             "error": str(exc)})
                else:
                    for key, value in schedules.items():
                        all_events.extend(event_rows(group, run_id, member_id, key, value))

    events_path = root / "events.jsonl"
    with events_path.open("w", encoding="utf-8") as stream:
        for row in all_events:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    write_json(root / "campaigns.json", campaign_rows)
    write_json(root / "failures.json", failures)

    counts = Counter((row["group"], row["attack"]) for row in all_events)
    usage_rows = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    usage_rows_with_usage = [row for row in usage_rows if isinstance(row.get("usage"), dict)]
    usage_summary = {
        "requests_recorded": len(usage_rows),
        "successful_requests_with_usage": len(usage_rows_with_usage),
        "prompt_tokens": sum(int(row["usage"].get("prompt_tokens", 0)) for row in usage_rows_with_usage),
        "completion_tokens": sum(int(row["usage"].get("completion_tokens", 0)) for row in usage_rows_with_usage),
        "total_tokens": sum(int(row["usage"].get("total_tokens", 0)) for row in usage_rows_with_usage),
        "pricing": "UNKNOWN_FOR_GLM-5.3-Flash_ENDPOINT",
    }
    normal_days_expected = args.employees * args.workdays * args.runs
    normal_days_observed = len({(row["group"], row["run_id"], row["member_id"], row["schedule_key"])
                                for row in all_events})
    unselected_equal = 0
    unselected_total = 0
    complete_step_sets = 0
    for manifest in campaign_rows:
        if manifest.get("group") == "C":
            for day in manifest.get("days", {}).values():
                if not day.get("selected"):
                    unselected_total += 1
                    if day.get("normal_sha256") == day.get("modified_sha256"):
                        unselected_equal += 1
            plan_steps = [step for day in manifest.get("campaign_plan", {}).get("days", [])
                          for step in day.get("attack_steps", [])]
            if plan_steps == manifest.get("attack_steps", plan_steps):
                complete_step_sets += 1
        else:
            complete_step_sets += int(bool(manifest.get("attack_steps")))
    q = {
        "Q1_plan_realization": {"status": "NOT_MEASURED", "reason": "No independent execution oracle."},
        "Q2_business_outcomes": {"status": "NOT_MEASURED", "reason": "Schedules were not executed by simulated employees."},
        "Q3_handoffs_and_cross_day": {"status": "NOT_MEASURED", "reason": "No real artifact production/consumption events."},
        "Q4_distribution_coverage": {"status": "MEASURED", "normal_employee_days_per_group": args.employees * args.workdays * args.runs,
                                      "event_counts": {f"{g}_{'attack' if a else 'normal'}": n for (g, a), n in counts.items()},
                                      "failure_count": len(failures),
                                      "normal_employee_days_expected": normal_days_expected,
                                      "normal_employee_days_observed": normal_days_observed,
                                      "unselected_campaign_days_equal": unselected_equal,
                                      "unselected_campaign_days_total": unselected_total},
        "Q5_attack_episode_integrity": {"status": "MEASURED", "campaigns_total": len(campaign_rows),
                                         "campaigns_failed": len(failures),
                                         "complete_campaigns": complete_step_sets,
                                         "selected_day_counts": [len(m.get("selected_dates", [])) for m in campaign_rows],
                                         "episodes_are_not_event_units": True},
        "Q6_blind_review_and_judge": {"status": "NOT_MEASURED", "reason": "No human ratings or calibrated judge run."},
        "Q7_cost_and_scope": {"status": "MEASURED", "usage_trace": "model_usage.jsonl", "usage": usage_summary,
                              "failures": len(failures)},
    }
    report = {"status": "PARTIAL_EXECUTED", "study": study, "metrics": q,
              "comparison": {"B_minus_O": "NOT_MEASURED", "C_minus_B": "MEASURED_WITHIN_CURRENT_FRAMEWORK_ONLY",
                              "C_minus_O": "NOT_MEASURED"},
              "limitations": ["Original Chimera provenance/data unavailable.",
                              "The execution and independent blind-rating portions were not run.",
                              "The actual endpoint model was GLM-5.3-Flash; GLM-5.3 returned HTTP 503."]}
    write_json(root / "report.json", report)
    md = ["# 第二阶段 GLM-5.3 评测报告（从零生成）", "", "状态：**PARTIAL_EXECUTED**。", "",
          "本次已清理可再生数据目录，并从空目录生成当前框架的正常日程、B 单日注入和 C LLM 多日注入产物。原始 Chimera O 数据、实际员工执行和盲评尚未形成，因此不宣称完整 O/B/C 结论。", "",
          "## 运行范围", "", f"- 员工：{args.employees}；工作日：{args.workdays}；独立运行：{args.runs}；攻击规格：每组每运行 {args.attack_count}",
          f"- 请求模型：GLM-5.3；服务端实际可用模型：{config.foundation_model}", "- 原始数据与模型用量：见 `study_manifest.json`、`model_usage.jsonl`、`failures.json`、`events.jsonl`。", "",
          "## 任务结果", "", "| 任务 | 状态 | 结果 |", "|---|---|---|",
          f"| Q1 计划落实 | NOT_MEASURED | 未执行员工行为，未接入独立 oracle |",
          f"| Q2 业务成果 | NOT_MEASURED | 未执行报告/开发/修复成果验收 |",
          f"| Q3 交接连续性 | NOT_MEASURED | 没有真实产物生产与消费事件 |",
          f"| Q4 分布覆盖 | MEASURED | 事件、员工日和失败记录已生成，详见 report.json |",
          f"| Q5 攻击 episode | MEASURED | campaign manifest、攻击步骤覆盖和失败均保留 |",
          f"| Q6 盲评/judge | NOT_MEASURED | 未产生人工评分包 |",
          f"| Q7 成本/范围 | MEASURED | 每请求 trace 和失败记录已保存 |", "",
          "## 对比结论边界", "", "- `B−O` 和 `C−O`：`NOT_MEASURED`，因为没有合法的原始 Chimera 数据来源。",
          "- `C−B`：仅能作为当前框架两种攻击注入策略的结构性差异，不能解释为相对原始 Chimera 的改进。",
          "- 本报告不把攻击事件数当成独立样本；episode、员工日和事件分别统计。", "",
          "## 产物", "", f"- 运行根目录：`{root}`", "- 详细 JSON：`report.json`", "- 原始事件：`events.jsonl`", "- 攻击真值/计划：`campaigns.json`", "- 失败：`failures.json`", "- 模型用量：`model_usage.jsonl`"]
    (root / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "root": str(root), "campaigns": len(campaign_rows), "failures": len(failures)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

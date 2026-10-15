# 第二阶段完整评测报告（O/B/C）

状态：**COMPLETE_AUTOMATED_SCOPE_WITH_LIMITATIONS**。

本报告对同一份新鲜正常日程执行 O（原始 Chimera 固定版本的 legacy 单日注入契约复现）、B（当前框架兼容单日注入）和 C（当前框架 LLM 多日注入）三组比较。Q1-Q7 的自动化指标已运行；人工盲评和真实员工长期仿真仍单列。

## 运行范围

- 源数据运行：`/Users/ayang/Desktop/project_work/Chimera/stage2_runs/formal/measurements`
- 员工/工作日/运行数：`{'employees': 12, 'workdays': 20, 'runs': 1, 'attack_specs_available': 15, 'attack_specs_injected_per_run': 3}`
- O 来源证据：`https://github.com/fish98/Chimera`，commit `d732f4cb427eed9c70e8b7ee062f56eec71007ab`
- O/B/C 共用冻结正常日程；攻击 Episode 按 campaign 计数。

## Q1-Q7 结果

| 任务 | 状态 | 主要指标 |
|---|---|---|
| Q1 计划落实 | MEASURED_WITH_DERIVED_PLAN_CONTRACT | 工作单元 Precision/Recall/F1、完成率、遗漏率、额外行为率；计划由冻结日程契约派生 |
| Q2 业务成果 | MEASURED_WITH_LOCAL_ORACLE_AND_REAL_TOOLCHAIN_PILOT | 业务成功率、隐藏测试、控制任务、真实 WorkflowToolLoop pilot |
| Q3 交接连续性 | MEASURED_WITH_LOCAL_ORACLE_AND_REAL_HANDOFF_FIXTURE | handoff、跨日、版本、ACL；12 条真实共享 filesystem 链 |
| Q4 分布/覆盖 | MEASURED_PAIRWISE_WITHOUT_EXTERNAL_REFERENCE | KS、Wasserstein、TV、JS、重复率、覆盖、lag-1 ACF；外部参考缺失 |
| Q5 攻击语义 | MEASURED_WITH_EXECUTION_BOUNDARY | Episode/步骤完整率、语义证据覆盖、持续天数；可达性/真实副作用未测 |
| Q6 盲评/judge | MEASURED_AUTOMATED_BLIND_SCOPE | 28 个匿名包、自动 contract judge；人工评分、alpha、MAE 未执行 |
| Q7 汇总/成本/范围 | MEASURED_WITH_EXPLICIT_UNMEASURED | 点估计、分母、CI、成本及未测指标清单 |

## 自动化指标清单

```json
{
  "measured": [
    "Q1.work_unit_precision_recall_f1",
    "Q1.target_completion_rate",
    "Q2.business_success",
    "Q3.handoff_success",
    "Q3.version_and_acl_checks",
    "Q4.coverage",
    "Q4.pairwise_KS_Wasserstein_TV_JS",
    "Q4.repeat_rate",
    "Q4.lag1_ACF",
    "Q5.attack_step_integrity",
    "Q5.semantic_evidence_coverage",
    "Q6.automated_contract_judge",
    "Q7.cost_and_scope"
  ],
  "not_measured": [
    "Q1.independent_phase_deviation",
    "Q2.pass_at_3_and_repeat_stability",
    "Q4.external_reference_distance",
    "Q5.target_reachability",
    "Q5.execution_success_or_block_rate",
    "Q5.attack_unknown_rate",
    "Q6.human_rater_scores",
    "Q6.Krippendorff_alpha",
    "Q6.judge_MAE_against_humans",
    "Q7.cluster_bootstrap_across_independent_runs"
  ],
  "reason": "the confirmed schedule run has no independent phase-plan sidecar, external reference distribution, capability registry, human panel, or multiple independent generation runs"
}
```

## 真实工具链 pilot 摘要

```json
{
  "execution_pilot": {
    "status": "PASS",
    "normal": {
      "execution_completed": 456,
      "business_passed": 456,
      "denominator": 456
    },
    "controls": {
      "passed": 204,
      "denominator": 204
    },
    "terminal_counts": {
      "completed": 476,
      "failed": 244
    },
    "scope": "specified local business fixtures; simulated delivery/review; no real enterprise or universal defect-free claim",
    "tasks_generated": 720,
    "execution_results": 720,
    "members": 72,
    "raw_fixture_tree_sha256": "488c6ce395f32b84949235488b73baaad8ce43abdfc6e40767c2c37924aa73b4"
  },
  "handoff_execution": {
    "status": "PASS",
    "chains": 12,
    "passed": 12,
    "failed": 0,
    "version_errors": 0,
    "acl_errors": 0
  }
}
```

## O/B/C 差值

```json
{
  "B_minus_O": {
    "business_task_rate_delta": 0.0,
    "handoff_task_rate_delta": 0.0,
    "plan_f1_delta": 0.0,
    "attack_campaign_delta": 0,
    "scope": "same frozen normal schedule; O is fixed legacy single-day contract reproduction"
  },
  "C_minus_B": {
    "business_task_rate_delta": 0.0,
    "handoff_task_rate_delta": 0.0,
    "plan_f1_delta": 0.0,
    "attack_campaign_delta": 0,
    "scope": "same frozen normal schedule; O is fixed legacy single-day contract reproduction"
  },
  "C_minus_O": {
    "business_task_rate_delta": 0.0,
    "handoff_task_rate_delta": 0.0,
    "plan_f1_delta": 0.0,
    "attack_campaign_delta": 0,
    "scope": "same frozen normal schedule; O is fixed legacy single-day contract reproduction"
  }
}
```

## 限制

- Q1 plan P/R/F1 uses the frozen schedule record as its plan contract because no independent human-authored plan sidecar is present; it is a coverage diagnostic, not an independent planning-validity claim.
- Q2/Q3 schedule-arm results use a deterministic contract oracle; the supplemental pilot uses real WorkflowToolLoop, filesystem tools, and independent business acceptance but scripted model responses rather than long-horizon GLM employee simulation.
- Q4 pairwise distances are descriptive O/B/C source distances; no external reference distribution was supplied, so they cannot establish real-world fidelity.
- Q5 manifests provide intended attack steps and schedule evidence, but target reachability and real side effects are not measured in this schedule report.
- Q6 produces an anonymized packet and automated calibrated contract labels; human inter-rater alpha and human ratings were not run.
- O is a fixed original-revision legacy contract reproduction over the shared normal fixture, not a licensed original published dataset or full original runtime replay.
- Third-stage detector utility is outside this report and remains unmeasured.

## 产物

- `events.jsonl`
- `campaigns.json`
- `business_oracle.jsonl`
- `handoff_oracle.jsonl`
- `metrics_detail.json`
- `execution_pilot_summary.json`
- `execution_pilot_execution_report.json`
- `execution_pilot_business_report.json`
- `handoff_execution.jsonl`
- `blind_review.jsonl`
- `judge_usage.jsonl`
- `judge_llm.jsonl`
- `judge_llm_raw.json`
- `comparison_metrics.json`

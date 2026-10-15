# 第二阶段完整评测报告（O/B/C）

状态：**EXECUTED_AUTOMATED_SCOPE**。

本报告对同一份新鲜正常日程执行 O（原始 Chimera 固定版本的 legacy 单日注入契约复现）、B（当前框架兼容单日注入）和 C（当前框架 LLM 多日注入）三组比较。Q1-Q7 的自动化任务均已运行；Q2/Q3 另有真实工具链受控 pilot，人工盲评和真实员工长期仿真仍单列。

## 运行范围

- 源数据运行：`/Users/ayang/Desktop/project_work/Chimera/stage2_runs/formal/measurements`
- 员工/工作日/运行数：`{'employees': 12, 'workdays': 20, 'runs': 1, 'attack_specs_available': 15, 'attack_specs_injected_per_run': 3}`
- O 来源证据：`https://github.com/fish98/Chimera`，commit `d732f4cb427eed9c70e8b7ee062f56eec71007ab`
- O/B/C 共用冻结正常日程；攻击 Episode 按 campaign 计数。

## Q1-Q7 结果

| 任务 | 状态 | 证据 |
|---|---|---|
| Q1 计划落实 | MEASURED | 每条日程记录的格式、时间、活动与 oracle 结果 |
| Q2 业务成果 | MEASURED_WITH_LOCAL_ORACLE_AND_REAL_TOOLCHAIN_PILOT | 720 个真实 WorkflowToolLoop 任务；正常任务和控制任务由独立 business evaluator 验收 |
| Q3 交接连续性 | MEASURED_WITH_LOCAL_ORACLE_AND_REAL_HANDOFF_FIXTURE | 12 条共享 filesystem 生产/消费链；检查版本/权限错误 |
| Q4 分布覆盖 | MEASURED | 员工日、事件、时间直方图和攻击比例 |
| Q5 攻击语义 | MEASURED | campaign 步骤顺序、选中日期和 episode 完整性 |
| Q6 盲评/judge | MEASURED_AUTOMATED_BLIND_SCOPE | 28 个匿名包、2 个 GLM 校准包；人工评分未运行 |
| Q7 成本/范围 | MEASURED | 源模型 usage、judge usage、pilot 零模型调用成本和本次评测产物清单 |

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
    "raw_fixture_tree_sha256": "ecc166960ac11c3f197a56dd9ffec53f72a8c0dbe6a1e9b3a91312a93c7c3271"
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
    "attack_campaign_delta": 0,
    "scope": "same frozen normal schedule; O is fixed legacy single-day contract reproduction"
  },
  "C_minus_B": {
    "business_task_rate_delta": 0.0,
    "handoff_task_rate_delta": 0.0,
    "attack_campaign_delta": 0,
    "scope": "same frozen normal schedule; O is fixed legacy single-day contract reproduction"
  },
  "C_minus_O": {
    "business_task_rate_delta": 0.0,
    "handoff_task_rate_delta": 0.0,
    "attack_campaign_delta": 0,
    "scope": "same frozen normal schedule; O is fixed legacy single-day contract reproduction"
  }
}
```

## 限制

- Q2/Q3 schedule-arm results use a deterministic contract oracle; the supplemental pilot uses real WorkflowToolLoop, filesystem tools, and independent business acceptance but scripted model responses rather than long-horizon GLM employee simulation.
- Q6 produces an anonymized packet and automated calibrated contract labels; human inter-rater alpha and human ratings were not run.
- O is a fixed original-revision legacy contract reproduction over the shared normal fixture, not a licensed original published dataset or full original runtime replay.
- Third-stage detector utility is outside this report and remains unmeasured.

## 产物

- `events.jsonl`
- `campaigns.json`
- `business_oracle.jsonl`
- `handoff_oracle.jsonl`
- `execution_pilot_summary.json`
- `execution_pilot_execution_report.json`
- `execution_pilot_business_report.json`
- `handoff_execution.jsonl`
- `blind_review.jsonl`
- `judge_usage.jsonl`
- `judge_llm.jsonl`
- `judge_llm_raw.json`
- `comparison_metrics.json`

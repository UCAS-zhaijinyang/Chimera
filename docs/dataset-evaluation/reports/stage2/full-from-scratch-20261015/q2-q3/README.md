# Q2/Q3 业务成果与产物交接评测

状态：**COMPLETE_REAL_MODEL_Q2_Q3_WITH_MEASURED_FAILURES**。

Q2 使用真实本地 WorkflowToolLoop 和独立业务验收器；Q3 使用真实共享文件系统、版本内容和 ACL 校验。Q6 按要求暂不执行。

## 指标

```json
{
  "Q2": {
    "status": "MEASURED_REAL_MODEL_TOOLCHAIN",
    "business_pilot": {
      "status": "FAIL",
      "execution_completion": {
        "numerator": 444,
        "denominator": 456,
        "value": 0.973684
      },
      "business_success": {
        "numerator": 444,
        "denominator": 456,
        "value": 0.973684
      },
      "control_pass": {
        "numerator": 202,
        "denominator": 204,
        "value": 0.990196
      },
      "normal_tasks": 456,
      "execution_results": 720,
      "tasks_generated": 720,
      "per_workflow": {
        "data_report": {
          "total": 152,
          "passed": 150
        },
        "software_feature": {
          "total": 152,
          "passed": 147
        },
        "bug_fix": {
          "total": 152,
          "passed": 147
        }
      },
      "model_requested": "GLM-5.3",
      "model_used": "GLM-5.3-Flash",
      "model_usage": {
        "requests": 4780,
        "prompt_tokens": 12256178,
        "completion_tokens": 963224,
        "total_tokens": 13219402,
        "returned_models": [
          "/data/models/GLM-5.3-Flash"
        ],
        "pricing": "UNKNOWN_FOR_PRIVATE_GLM_ENDPOINT",
        "estimated_cost_usd": null
      },
      "scope": "specified local business fixtures; simulated delivery/review; no real enterprise or universal defect-free claim",
      "normal_failure_task_ids": [
        "q2-t0089",
        "q2-t0142",
        "q2-t0369",
        "q2-t0384",
        "q2-t0413",
        "q2-t0435",
        "q2-t0448",
        "q2-t0528",
        "q2-t0545",
        "q2-t0587",
        "q2-t0688",
        "q2-t0689"
      ],
      "business_failure_task_ids": [
        "q2-t0089",
        "q2-t0142",
        "q2-t0369",
        "q2-t0384",
        "q2-t0413",
        "q2-t0435",
        "q2-t0448",
        "q2-t0528",
        "q2-t0545",
        "q2-t0587",
        "q2-t0688",
        "q2-t0689"
      ]
    },
    "schedule_contract_by_arm": {
      "O": {
        "status": "MEASURED",
        "schedule_files": 240,
        "denominator": 240,
        "expected_employee_days": 240,
        "coverage": {
          "numerator": 240,
          "denominator": 240,
          "value": 1.0
        },
        "valid_files": 240,
        "valid_rate": {
          "numerator": 240,
          "denominator": 240,
          "value": 1.0
        },
        "valid_file_rate": {
          "numerator": 240,
          "denominator": 240,
          "value": 1.0
        },
        "valid_rows": 1433,
        "event_count": 1433,
        "cross_day_adjacent_pairs": 228,
        "cross_day_continuous_pairs": 228,
        "cross_day_continuity_rate": {
          "numerator": 228,
          "denominator": 228,
          "value": 1.0
        },
        "invalid_files": [],
        "interpretation": "schedule contract diagnostics; not independent business acceptance"
      },
      "N": {
        "status": "MEASURED",
        "schedule_files": 240,
        "denominator": 240,
        "expected_employee_days": 240,
        "coverage": {
          "numerator": 240,
          "denominator": 240,
          "value": 1.0
        },
        "valid_files": 240,
        "valid_rate": {
          "numerator": 240,
          "denominator": 240,
          "value": 1.0
        },
        "valid_file_rate": {
          "numerator": 240,
          "denominator": 240,
          "value": 1.0
        },
        "valid_rows": 720,
        "event_count": 720,
        "cross_day_adjacent_pairs": 228,
        "cross_day_continuous_pairs": 228,
        "cross_day_continuity_rate": {
          "numerator": 228,
          "denominator": 228,
          "value": 1.0
        },
        "invalid_files": [],
        "interpretation": "schedule contract diagnostics; not independent business acceptance"
      }
    },
    "interpretation": "Business outcomes are independently accepted from actual GLM-driven WorkflowToolLoop executions; O/N schedule rows are reported separately as contract diagnostics."
  },
  "Q3": {
    "status": "MEASURED_REAL_MODEL_HANDOFF",
    "handoff_pilot": {
      "status": "PASS",
      "chains": 12,
      "passed": 12,
      "failed": 0,
      "handoff_success": {
        "numerator": 12,
        "denominator": 12,
        "value": 1.0
      },
      "version_errors": 0,
      "acl_errors": 0
    },
    "schedule_cross_day_by_arm": {
      "O": {
        "adjacent_pairs": 228,
        "continuous_pairs": 228,
        "continuity_rate": {
          "numerator": 228,
          "denominator": 228,
          "value": 1.0
        },
        "interpretation": "schedule ordering only; no artifact consumption claim"
      },
      "N": {
        "adjacent_pairs": 228,
        "continuous_pairs": 228,
        "continuity_rate": {
          "numerator": 228,
          "denominator": 228,
          "value": 1.0
        },
        "interpretation": "schedule ordering only; no artifact consumption claim"
      }
    }
  },
  "Q6": {
    "status": "NOT_MEASURED",
    "reason": "human blind panel intentionally deferred"
  }
}
```

## 限制

- Q2 uses actual GLM responses at the WorkflowToolLoop boundary and independent business acceptance; it is a bounded simulated workload rather than the 20-day employee schedule replay.
- O/N schedule contract diagnostics do not substitute for business outcomes.
- Q3 schedule continuity does not substitute for artifact consumption; handoff success comes from actual GLM producer/consumer executions on a shared filesystem.

## 证据

- `business_pilot/`
- `handoff_pilot/handoff_execution.jsonl`
- `schedule_contract.json`

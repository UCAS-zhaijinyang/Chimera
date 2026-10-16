# 第二阶段完整从头生成评测报告

状态：**COMPLETE_AUTOMATED_SCOPE_WITH_LIMITATIONS**。

O 从原始 Chimera weekly meeting 链路生成，N 从当前框架分层会议链路生成；两者只共享公司画像输入，不共享会议结果或日程。

## 运行范围

- 员工：12；工作日：20；运行数：1
- 模型：请求 GLM-5.3；实际使用 GLM-5.3-Flash
- O：weekly meeting → legacy weekly summary → legacy daily plan → single-day attack
- N：leadership meeting → department plan → department meetings → employee phase plan → daily plan → multi-day attack

## 结果

```json
{
  "planning": {
    "O": {
      "numerator": 240,
      "denominator": 240,
      "value": 1.0,
      "status": "MEASURED"
    },
    "N": {
      "numerator": 240,
      "denominator": 240,
      "value": 1.0,
      "status": "MEASURED"
    }
  },
  "comparison": {
    "status": "MEASURED",
    "scope": "independent planning pipelines with paired company input",
    "O_vs_N": "see Q1/Q4/Q5 denominators and values"
  },
  "metrics": {
    "Q1": {
      "O": {
        "status": "MEASURED",
        "metrics": {
          "work_unit": {
            "status": "MEASURED",
            "precision": {
              "numerator": 1443,
              "denominator": 1443,
              "value": 1.0,
              "ci95": {
                "low": 0.997345,
                "high": 1.0
              }
            },
            "recall": {
              "numerator": 1443,
              "denominator": 1443,
              "value": 1.0,
              "ci95": {
                "low": 0.997345,
                "high": 1.0
              }
            },
            "f1": {
              "numerator": 2886,
              "denominator": 2886,
              "value": 1.0,
              "ci95": {
                "low": null,
                "high": null
              }
            },
            "target_completion": {
              "numerator": 1443,
              "denominator": 1443,
              "value": 1.0,
              "ci95": {
                "low": 0.997345,
                "high": 1.0
              }
            },
            "phase_deviation": {
              "mean": 0.0,
              "mean_absolute": 0.0,
              "max_absolute": 0,
              "exact_phase_rate": {
                "numerator": 1443,
                "denominator": 1443,
                "value": 1.0,
                "ci95": {
                  "low": 0.997345,
                  "high": 1.0
                }
              },
              "mismatch_rate": {
                "numerator": 0,
                "denominator": 1443,
                "value": 0.0,
                "ci95": {
                  "low": 0.0,
                  "high": 0.002655
                }
              },
              "status": "MEASURED"
            },
            "omission_rate": {
              "numerator": 0,
              "denominator": 1443,
              "value": 0.0,
              "ci95": {
                "low": 0.0,
                "high": 0.002655
              }
            },
            "extra_behavior_rate": {
              "numerator": 0,
              "denominator": 1443,
              "value": 0.0,
              "ci95": {
                "low": 0.0,
                "high": 0.002655
              }
            }
          },
          "phase_alignment": {
            "status": "MEASURED",
            "phase_deviation": {
              "mean": 0.0,
              "mean_absolute": 0.0,
              "max_absolute": 0,
              "exact_phase_rate": {
                "numerator": 1443,
                "denominator": 1443,
                "value": 1.0,
                "ci95": {
                  "low": 0.997345,
                  "high": 1.0
                }
              },
              "mismatch_rate": {
                "numerator": 0,
                "denominator": 1443,
                "value": 0.0,
                "ci95": {
                  "low": 0.0,
                  "high": 0.002655
                }
              },
              "status": "MEASURED"
            },
            "coverage": {
              "measured": 1443,
              "unknown": 0,
              "total_observed": 1443,
              "value": 1.0
            },
            "sidecar_source": "stage2_runs/stage2-full-from-scratch-20261015/O/run/meeting_logs/meeting_result.log",
            "sidecar_sha256": "cd15781432d6f35ec32bd63f00d5baccecfb301af83fea57c0516bd61b9b0acc",
            "rows": [
              {
                "event_id": "o-r01:bstat-1:week_1_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Friday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Friday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Friday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Friday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Monday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Monday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Monday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Monday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Thursday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Thursday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Thursday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Thursday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Tuesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Tuesday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Tuesday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Tuesday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Wednesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Wednesday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Wednesday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_1_Wednesday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:3",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:4",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:5",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:6",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Friday:7",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Monday:3",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Monday:4",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Thursday:3",
                "member_id": "comp-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Tuesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_1_Wednesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Friday:3",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Friday:4",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Monday:3",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Monday:4",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Thursday:3",
                "member_id": "dana-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Tuesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Tuesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Wednesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_1_Wednesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Friday:3",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Friday:4",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Friday:5",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Friday:6",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Monday:3",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Monday:4",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Monday:5",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Thursday:3",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Thursday:4",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Thursday:5",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Tuesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Tuesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Tuesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Wednesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Wednesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_1_Wednesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Friday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Friday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Friday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Monday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Monday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Thursday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Thursday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Tuesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Tuesday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Wednesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_1_Wednesday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_1_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Friday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Friday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Friday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Friday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Monday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Monday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Monday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Thursday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Thursday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Thursday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Tuesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Tuesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Tuesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Wednesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Wednesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_1_Wednesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Friday:3",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Friday:4",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Friday:5",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Friday:6",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Monday:3",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Monday:4",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Monday:5",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Monday:6",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Thursday:3",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Thursday:4",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Thursday:5",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Thursday:6",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Tuesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Tuesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Tuesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Tuesday:6",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Wednesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Wednesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Wednesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_1_Wednesday:6",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Friday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Friday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Monday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Monday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Thursday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Thursday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Tuesday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Tuesday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Wednesday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_1_Wednesday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Friday:3",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Friday:4",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Monday:3",
                "member_id": "pco-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Thursday:3",
                "member_id": "pco-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Tuesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Wednesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_1_Wednesday:4",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Friday:3",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Friday:4",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Monday:3",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Monday:4",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Thursday:3",
                "member_id": "rn-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Tuesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Wednesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_1_Wednesday:4",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_1_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Friday:7",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Monday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Monday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Monday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Monday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Thursday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Thursday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Thursday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Thursday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Tuesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Tuesday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Tuesday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Tuesday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Wednesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Wednesday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Wednesday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_2_Wednesday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Friday:3",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Friday:4",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Friday:5",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Monday:3",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Monday:4",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Monday:5",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Thursday:3",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Thursday:4",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Thursday:5",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Tuesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Tuesday:4",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Tuesday:5",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Wednesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Wednesday:4",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_2_Wednesday:5",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Friday:3",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Friday:4",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Friday:5",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Monday:3",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Monday:4",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Monday:5",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Thursday:3",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Thursday:4",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Tuesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Tuesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Wednesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Wednesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_2_Wednesday:5",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Friday:3",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Friday:4",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Friday:5",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Friday:6",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Monday:3",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Monday:4",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Monday:5",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Monday:6",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Thursday:3",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Thursday:4",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Thursday:5",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Thursday:6",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Tuesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Tuesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Tuesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Tuesday:6",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Wednesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Wednesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Wednesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_2_Wednesday:6",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Friday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Friday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Friday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Monday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Monday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Thursday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Tuesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Wednesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_2_Wednesday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:3",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:4",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:5",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:6",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Friday:7",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Monday:3",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Monday:4",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Monday:5",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Monday:6",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:3",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:4",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:5",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:6",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Thursday:7",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Tuesday:3",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Tuesday:4",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Tuesday:5",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Tuesday:6",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Wednesday:3",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Wednesday:4",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Wednesday:5",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_2_Wednesday:6",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Friday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Friday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Friday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Friday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Monday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Monday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Monday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Monday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Thursday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Thursday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Thursday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Thursday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Tuesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Tuesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Tuesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Tuesday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Wednesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Wednesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Wednesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_2_Wednesday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:3",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:4",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:5",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:6",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Friday:7",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Monday:3",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Monday:4",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Monday:5",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Monday:6",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Thursday:3",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Thursday:4",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Thursday:5",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Tuesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Tuesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Tuesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Wednesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Wednesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Wednesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_2_Wednesday:6",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Friday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Friday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Friday:5",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Monday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Monday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Thursday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Thursday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Thursday:5",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Tuesday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Tuesday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Tuesday:5",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Wednesday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_2_Wednesday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:3",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:4",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:5",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:6",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Friday:7",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:3",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:4",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:5",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:6",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Monday:7",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:3",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:4",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:5",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:6",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Thursday:7",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:4",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:5",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:6",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Tuesday:7",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:4",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:5",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:6",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_2_Wednesday:7",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:3",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:4",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:5",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:6",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Friday:7",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:3",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:4",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:5",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:6",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Monday:7",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:3",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:4",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:5",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:6",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Thursday:7",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:4",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:5",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:6",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Tuesday:7",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:4",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:5",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:6",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_2_Wednesday:7",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Friday:3",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Friday:4",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Friday:5",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Friday:6",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Monday:3",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Monday:4",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Monday:5",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Monday:6",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Thursday:3",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Thursday:4",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Thursday:5",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Thursday:6",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Tuesday:3",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Tuesday:4",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Tuesday:5",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Tuesday:6",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Wednesday:3",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Wednesday:4",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Wednesday:5",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_2_Wednesday:6",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Friday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Friday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Monday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Monday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Thursday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Tuesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Tuesday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_3_Wednesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Friday:3",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Friday:4",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Friday:5",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Friday:6",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Monday:3",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Monday:4",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Monday:5",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Monday:6",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Thursday:3",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Thursday:4",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Thursday:5",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Thursday:6",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Tuesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Tuesday:4",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Tuesday:5",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Tuesday:6",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Wednesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Wednesday:4",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Wednesday:5",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_3_Wednesday:6",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:3",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:4",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:5",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:6",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Friday:7",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Monday:3",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Monday:4",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Thursday:3",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Thursday:4",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Tuesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Tuesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Wednesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_3_Wednesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Friday:3",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Friday:4",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Friday:5",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Friday:6",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Monday:3",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Monday:4",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Monday:5",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Monday:6",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Thursday:3",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Thursday:4",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Thursday:5",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Thursday:6",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Tuesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Tuesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Tuesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Wednesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Wednesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_3_Wednesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Friday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Friday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Friday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Friday:6",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Monday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Monday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Monday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Monday:6",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Thursday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Thursday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Thursday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Thursday:6",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Tuesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Tuesday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Tuesday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Tuesday:6",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Wednesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Wednesday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Wednesday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_3_Wednesday:6",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:3",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:4",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:5",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:6",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Friday:7",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:3",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:4",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:5",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:6",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Monday:7",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:3",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:4",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:5",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:6",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Thursday:7",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:3",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:4",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:5",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:6",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Tuesday:7",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:3",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:4",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:5",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:6",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_3_Wednesday:7",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Friday:7",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Monday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Monday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Monday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Monday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Thursday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Thursday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Thursday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Thursday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Tuesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Tuesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Tuesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Wednesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Wednesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Wednesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_3_Wednesday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Friday:3",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Friday:4",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Friday:5",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Monday:3",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Monday:4",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Monday:5",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Thursday:3",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Thursday:4",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Thursday:5",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Tuesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Tuesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Tuesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Wednesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Wednesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_3_Wednesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Friday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_3_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:3",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:4",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:5",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:6",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Friday:7",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:3",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:4",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:5",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:6",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Monday:7",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:3",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:4",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:5",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:6",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Thursday:7",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:4",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:5",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:6",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Tuesday:7",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:4",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:5",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:6",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_3_Wednesday:7",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Friday:3",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Friday:4",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Friday:5",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Friday:6",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:3",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:4",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:5",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:6",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Monday:7",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Thursday:3",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Thursday:4",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Thursday:5",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Thursday:6",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Tuesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Tuesday:4",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Tuesday:5",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:4",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:5",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:6",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_3_Wednesday:7",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Friday:3",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Friday:4",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Friday:5",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Monday:3",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Monday:4",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Monday:5",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Thursday:3",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Thursday:4",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Tuesday:3",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Tuesday:4",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Wednesday:3",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_3_Wednesday:4",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Friday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Friday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Friday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Monday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Monday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:7",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Thursday:8",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Tuesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Tuesday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:bstat-1:week_4_Wednesday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Friday:3",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Friday:4",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Monday:3",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Monday:4",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Thursday:3",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Thursday:4",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Tuesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Tuesday:4",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:comp-1:week_4_Wednesday:3",
                "member_id": "comp-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Friday:3",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Friday:4",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Friday:5",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Monday:3",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Monday:4",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Monday:5",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Thursday:3",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Thursday:4",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Thursday:5",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Tuesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Tuesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Tuesday:5",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Wednesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Wednesday:4",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:dana-1:week_4_Wednesday:5",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Friday:3",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Friday:4",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Friday:5",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Monday:3",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Monday:4",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Monday:5",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Thursday:3",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Thursday:4",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Thursday:5",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Tuesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Tuesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Tuesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Wednesday:3",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Wednesday:4",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:epi-1:week_4_Wednesday:5",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Friday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Friday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Friday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Monday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Monday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Monday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Thursday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Thursday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Thursday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Tuesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Tuesday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Tuesday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Wednesday:3",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Wednesday:4",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:hinf-1:week_4_Wednesday:5",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Friday:3",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Friday:4",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Monday:3",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Monday:4",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Thursday:3",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Thursday:4",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Tuesday:3",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Tuesday:4",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Wednesday:3",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:itss-1:week_4_Wednesday:4",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Friday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Friday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Friday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Friday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Monday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Monday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Monday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Monday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Thursday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Thursday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Thursday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Thursday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Tuesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Tuesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Tuesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Tuesday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Wednesday:3",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Wednesday:4",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Wednesday:5",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:lphy-1:week_4_Wednesday:6",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:3",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:4",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:5",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:6",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Friday:7",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Monday:3",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Monday:4",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Monday:5",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Monday:6",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:3",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:4",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:5",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:6",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Thursday:7",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Tuesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Tuesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Tuesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Tuesday:6",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Wednesday:3",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Wednesday:4",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Wednesday:5",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:medas-1:week_4_Wednesday:6",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Friday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Friday:4",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Monday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Thursday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Tuesday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:mrec-1:week_4_Wednesday:3",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Friday:3",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Friday:4",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Friday:5",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Friday:6",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Monday:3",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Monday:4",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Monday:5",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Monday:6",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Thursday:3",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Thursday:4",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Thursday:5",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Thursday:6",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Tuesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Tuesday:4",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Tuesday:5",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Tuesday:6",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Wednesday:3",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Wednesday:4",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Wednesday:5",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:pco-1:week_4_Wednesday:6",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Friday:3",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Friday:4",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Friday:5",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Monday:3",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Monday:4",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Monday:5",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Thursday:3",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Thursday:4",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Thursday:5",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Tuesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Tuesday:4",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Tuesday:5",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Wednesday:3",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-1:week_4_Wednesday:4",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Friday:3",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Friday:4",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Friday:5",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Friday:6",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Monday:3",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Monday:4",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Monday:5",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Thursday:3",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Thursday:4",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Thursday:5",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Tuesday:3",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Tuesday:4",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Tuesday:5",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Wednesday:3",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Wednesday:4",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "o-r01:rn-2:week_4_Wednesday:5",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              }
            ]
          }
        },
        "independence": "independent_phase_plan_sidecar"
      },
      "N": {
        "status": "MEASURED",
        "metrics": {
          "work_unit": {
            "status": "MEASURED",
            "precision": {
              "numerator": 756,
              "denominator": 756,
              "value": 1.0,
              "ci95": {
                "low": 0.994944,
                "high": 1.0
              }
            },
            "recall": {
              "numerator": 756,
              "denominator": 756,
              "value": 1.0,
              "ci95": {
                "low": 0.994944,
                "high": 1.0
              }
            },
            "f1": {
              "numerator": 1512,
              "denominator": 1512,
              "value": 1.0,
              "ci95": {
                "low": null,
                "high": null
              }
            },
            "target_completion": {
              "numerator": 756,
              "denominator": 756,
              "value": 1.0,
              "ci95": {
                "low": 0.994944,
                "high": 1.0
              }
            },
            "phase_deviation": {
              "mean": 0.0,
              "mean_absolute": 0.0,
              "max_absolute": 0,
              "exact_phase_rate": {
                "numerator": 756,
                "denominator": 756,
                "value": 1.0,
                "ci95": {
                  "low": 0.994944,
                  "high": 1.0
                }
              },
              "mismatch_rate": {
                "numerator": 0,
                "denominator": 756,
                "value": 0.0,
                "ci95": {
                  "low": 0.0,
                  "high": 0.005056
                }
              },
              "status": "MEASURED"
            },
            "omission_rate": {
              "numerator": 0,
              "denominator": 756,
              "value": 0.0,
              "ci95": {
                "low": 0.0,
                "high": 0.005056
              }
            },
            "extra_behavior_rate": {
              "numerator": 0,
              "denominator": 756,
              "value": 0.0,
              "ci95": {
                "low": 0.0,
                "high": 0.005056
              }
            }
          },
          "phase_alignment": {
            "status": "MEASURED",
            "phase_deviation": {
              "mean": 0.0,
              "mean_absolute": 0.0,
              "max_absolute": 0,
              "exact_phase_rate": {
                "numerator": 756,
                "denominator": 756,
                "value": 1.0,
                "ci95": {
                  "low": 0.994944,
                  "high": 1.0
                }
              },
              "mismatch_rate": {
                "numerator": 0,
                "denominator": 756,
                "value": 0.0,
                "ci95": {
                  "low": 0.0,
                  "high": 0.005056
                }
              },
              "status": "MEASURED"
            },
            "coverage": {
              "measured": 756,
              "unknown": 0,
              "total_observed": 756,
              "value": 1.0
            },
            "sidecar_source": "stage2_runs/stage2-full-from-scratch-20261015/N/run/meeting_logs/phase_plans.json",
            "sidecar_sha256": "1954084312e9fa9919fe2f2178644a4867784c97f3bee138d09e87f706c2c445",
            "rows": [
              {
                "event_id": "n-r01:bstat-1:week_1_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Thursday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Thursday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Thursday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Thursday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_1_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:3",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:4",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:5",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:6",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:7",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Monday:8",
                "member_id": "comp-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_1_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_1_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_1_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_1_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_1_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_1_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_1_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_1_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_1_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_1_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Friday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Monday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Thursday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Tuesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_1_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_1_Wednesday",
                "observed_phase": 1,
                "expected_phase": 1,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Thursday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Thursday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Thursday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Thursday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_2_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Friday:3",
                "member_id": "comp-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_2_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_2_Wednesday:3",
                "member_id": "dana-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_2_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_2_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_2_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_2_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_2_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_2_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_2_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_2_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Friday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Monday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Thursday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Tuesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_2_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_2_Wednesday",
                "observed_phase": 2,
                "expected_phase": 2,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Friday:3",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Friday:4",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Friday:5",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Friday:6",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_3_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_3_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:3",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:4",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:5",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:6",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Monday:7",
                "member_id": "dana-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:3",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:4",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:5",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:6",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Thursday:7",
                "member_id": "dana-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_3_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_3_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_3_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_3_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_3_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_3_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_3_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_3_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_3_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Friday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Monday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Thursday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Tuesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_3_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_3_Wednesday",
                "observed_phase": 3,
                "expected_phase": 3,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Friday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Friday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Friday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Monday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Monday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Monday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Thursday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Thursday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Thursday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Tuesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Tuesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Tuesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Wednesday:0",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Wednesday:1",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:bstat-1:week_4_Wednesday:2",
                "member_id": "bstat-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Friday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Friday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Friday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Monday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Monday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Monday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:3",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:4",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:5",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:6",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:7",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Thursday:8",
                "member_id": "comp-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Tuesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Tuesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Tuesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Wednesday:0",
                "member_id": "comp-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Wednesday:1",
                "member_id": "comp-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:comp-1:week_4_Wednesday:2",
                "member_id": "comp-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Friday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Friday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Friday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Monday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Monday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Monday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Thursday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Thursday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Thursday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Tuesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Tuesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Tuesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Wednesday:0",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Wednesday:1",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:dana-1:week_4_Wednesday:2",
                "member_id": "dana-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Friday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Friday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Friday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Monday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Monday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Monday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Thursday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Thursday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Thursday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Tuesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Tuesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Tuesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Wednesday:0",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Wednesday:1",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:epi-1:week_4_Wednesday:2",
                "member_id": "epi-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Friday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Friday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Friday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Monday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Monday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Monday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Thursday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Thursday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Thursday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Tuesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Tuesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Tuesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Wednesday:0",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Wednesday:1",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:hinf-1:week_4_Wednesday:2",
                "member_id": "hinf-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Friday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Friday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Friday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Monday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Monday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Monday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Thursday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Thursday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Thursday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Tuesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Tuesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Tuesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Wednesday:0",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Wednesday:1",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:itss-1:week_4_Wednesday:2",
                "member_id": "itss-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Friday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Friday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Friday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Monday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Monday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Monday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Thursday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Thursday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Thursday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Tuesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Tuesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Tuesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Wednesday:0",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Wednesday:1",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:lphy-1:week_4_Wednesday:2",
                "member_id": "lphy-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Friday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Friday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Friday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Monday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Monday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Monday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Thursday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Thursday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Thursday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Tuesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Tuesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Tuesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Wednesday:0",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Wednesday:1",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:medas-1:week_4_Wednesday:2",
                "member_id": "medas-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Friday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Friday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Friday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Monday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Monday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Monday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Thursday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Thursday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Thursday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Tuesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Tuesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Tuesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Wednesday:0",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Wednesday:1",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:mrec-1:week_4_Wednesday:2",
                "member_id": "mrec-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Friday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Friday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Friday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Monday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Monday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Monday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Thursday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Thursday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Thursday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Tuesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Tuesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Tuesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Wednesday:0",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Wednesday:1",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:pco-1:week_4_Wednesday:2",
                "member_id": "pco-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Friday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Friday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Friday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Monday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Monday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Monday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Thursday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Thursday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Thursday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Tuesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Tuesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Tuesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Wednesday:0",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Wednesday:1",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-1:week_4_Wednesday:2",
                "member_id": "rn-1",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Friday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Friday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Friday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Friday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Monday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Monday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Monday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Monday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Thursday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Thursday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Thursday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Thursday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Tuesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Tuesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Tuesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Tuesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Wednesday:0",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Wednesday:1",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              },
              {
                "event_id": "n-r01:rn-2:week_4_Wednesday:2",
                "member_id": "rn-2",
                "schedule_key": "week_4_Wednesday",
                "observed_phase": 4,
                "expected_phase": 4,
                "deviation": 0,
                "absolute_deviation": 0,
                "status": "PASS"
              }
            ]
          }
        },
        "independence": "independent_phase_plan_sidecar"
      }
    },
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
    "Q4": {
      "by_group": {
        "O": {
          "events": 1443,
          "normal_events": 1418,
          "attack_events": 25,
          "coverage": {
            "employee_days": 240,
            "unique_activities": 1367,
            "time_values": 18,
            "status": "MEASURED"
          },
          "time": {
            "mean_seconds": 54187.2,
            "min_seconds": 36000.0,
            "max_seconds": 76500.0
          },
          "repeat_rate": {
            "numerator": 76,
            "denominator": 1443,
            "value": 0.052668,
            "ci95": {
              "low": 0.042285,
              "high": 0.065427
            }
          },
          "exact_event_repeat_rate": {
            "numerator": 72,
            "denominator": 1443,
            "value": 0.049896,
            "ci95": {
              "low": 0.039808,
              "high": 0.062374
            }
          },
          "daily_count_acf_lag1": 0.703299
        },
        "N": {
          "events": 756,
          "normal_events": 693,
          "attack_events": 63,
          "coverage": {
            "employee_days": 240,
            "unique_activities": 752,
            "time_values": 30,
            "status": "MEASURED"
          },
          "time": {
            "mean_seconds": 47754.761905,
            "min_seconds": 36000.0,
            "max_seconds": 78300.0
          },
          "repeat_rate": {
            "numerator": 4,
            "denominator": 756,
            "value": 0.005291,
            "ci95": {
              "low": 0.002059,
              "high": 0.013525
            }
          },
          "exact_event_repeat_rate": {
            "numerator": 2,
            "denominator": 756,
            "value": 0.002646,
            "ci95": {
              "low": 0.000726,
              "high": 0.009594
            }
          },
          "daily_count_acf_lag1": 0.117512
        }
      },
      "pairwise": {
        "O_vs_N": {
          "time": {
            "ks": 0.248148,
            "wasserstein_seconds": 6384.306
          },
          "activity": {
            "tv": 0.995842,
            "js": 0.994818
          },
          "status": "MEASURED",
          "interpretation": "descriptive_source_distance_without_external_reference"
        }
      },
      "reference": {
        "status": "NOT_MEASURED",
        "reason": "external reference distribution not supplied"
      }
    },
    "Q5": {
      "O": {
        "integrity": {
          "numerator": 3,
          "denominator": 3,
          "value": 1.0,
          "ci95": {
            "low": 0.438494,
            "high": 1.0
          },
          "unit": "campaign"
        },
        "semantic_evidence_coverage": {
          "numerator": 3,
          "denominator": 3,
          "value": 1.0,
          "ci95": {
            "low": 0.438494,
            "high": 1.0
          }
        },
        "selected_date_legal_rate": {
          "numerator": 3,
          "denominator": 3,
          "value": 1.0,
          "ci95": {
            "low": 0.438494,
            "high": 1.0
          }
        },
        "multi_day_episode_rate": {
          "numerator": 0,
          "denominator": 3,
          "value": 0.0,
          "ci95": {
            "low": 0.0,
            "high": 0.561506
          }
        },
        "attack_generation_fallback_rate": {
          "numerator": 1,
          "denominator": 3,
          "value": 0.333333,
          "ci95": {
            "low": 0.06149,
            "high": 0.792345
          }
        },
        "campaign_planning_fallback_rate": {
          "numerator": 0,
          "denominator": 3,
          "value": 0.0,
          "ci95": {
            "low": 0.0,
            "high": 0.561506
          }
        },
        "selected_day_count": {
          "mean": 1.0,
          "min": 1,
          "max": 1
        },
        "execution_outcome": {
          "status": "MEASURED",
          "step_success_rate": {
            "numerator": 9,
            "denominator": 9,
            "value": 1.0,
            "ci95": {
              "low": 0.700847,
              "high": 1.0
            }
          },
          "step_block_rate": {
            "numerator": 0,
            "denominator": 9,
            "value": 0.0,
            "ci95": {
              "low": 0.0,
              "high": 0.299153
            }
          },
          "ordered_episode_success_rate": {
            "numerator": 3,
            "denominator": 3,
            "value": 1.0,
            "ci95": {
              "low": 0.438494,
              "high": 1.0
            }
          }
        },
        "target_reachability": {
          "numerator": 9,
          "denominator": 9,
          "value": 1.0,
          "ci95": {
            "low": 0.700847,
            "high": 1.0
          }
        },
        "unknown_rate": {
          "numerator": 0,
          "denominator": 9,
          "value": 0.0,
          "ci95": {
            "low": 0.0,
            "high": 0.299153
          }
        },
        "rows": [
          {
            "attack_id": "gen_attack_1",
            "selected_days": 1,
            "expected_steps": [
              1,
              2,
              3
            ],
            "covered_steps": [
              1,
              2,
              3
            ],
            "integrity": true,
            "legal_dates": true,
            "attack_generation_fallback": true,
            "campaign_planning_fallback": false,
            "semantic_evidence": true
          },
          {
            "attack_id": "gen_attack_10",
            "selected_days": 1,
            "expected_steps": [
              1,
              2,
              3
            ],
            "covered_steps": [
              1,
              2,
              3
            ],
            "integrity": true,
            "legal_dates": true,
            "attack_generation_fallback": false,
            "campaign_planning_fallback": false,
            "semantic_evidence": true
          },
          {
            "attack_id": "gen_attack_11",
            "selected_days": 1,
            "expected_steps": [
              1,
              2,
              3
            ],
            "covered_steps": [
              1,
              2,
              3
            ],
            "integrity": true,
            "legal_dates": true,
            "attack_generation_fallback": false,
            "campaign_planning_fallback": false,
            "semantic_evidence": true
          }
        ],
        "oracle_coverage": {
          "numerator": 9,
          "denominator": 9,
          "value": 1.0,
          "ci95": {
            "low": 0.700847,
            "high": 1.0
          }
        },
        "side_effect_observed_rate": {
          "numerator": 9,
          "denominator": 9,
          "value": 1.0,
          "ci95": {
            "low": 0.700847,
            "high": 1.0
          }
        },
        "execution_evidence": {
          "report": "/Users/ayang/Desktop/project_work/Chimera/docs/dataset-evaluation/reports/stage2/full-from-scratch-20261015/q5-attack-side-effects/report.json",
          "rows": [
            {
              "arm": "O",
              "campaign_key": "o-bstat-1-gen_attack_1",
              "member_id": "bstat-1",
              "attack_id": "gen_attack_1",
              "selected_dates": [
                "week_4_Thursday"
              ],
              "steps": [
                {
                  "arm": "O",
                  "campaign_key": "o-bstat-1-gen_attack_1",
                  "member_id": "bstat-1",
                  "attack_id": "gen_attack_1",
                  "step": 1,
                  "operation": "request_access",
                  "selected_date": "week_4_Thursday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py request_access",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.050528,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "O",
                  "campaign_key": "o-bstat-1-gen_attack_1",
                  "member_id": "bstat-1",
                  "attack_id": "gen_attack_1",
                  "step": 2,
                  "operation": "solicit_credentials",
                  "selected_date": "week_4_Thursday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py solicit_credentials",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.050476,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "O",
                  "campaign_key": "o-bstat-1-gen_attack_1",
                  "member_id": "bstat-1",
                  "attack_id": "gen_attack_1",
                  "step": 3,
                  "operation": "collect_files",
                  "selected_date": "week_4_Thursday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py collect_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.038725,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                }
              ],
              "episode": {
                "status": "PASS",
                "step_count": 3,
                "passed_steps": 3
              },
              "counts": {
                "steps": 3,
                "passed": 3,
                "blocked": 0,
                "unknown": 0,
                "reachable": 3
              }
            },
            {
              "arm": "O",
              "campaign_key": "o-comp-1-gen_attack_10",
              "member_id": "comp-1",
              "attack_id": "gen_attack_10",
              "selected_dates": [
                "week_1_Friday"
              ],
              "steps": [
                {
                  "arm": "O",
                  "campaign_key": "o-comp-1-gen_attack_10",
                  "member_id": "comp-1",
                  "attack_id": "gen_attack_10",
                  "step": 1,
                  "operation": "former_login",
                  "selected_date": "week_1_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py former_login",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.076322,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "O",
                  "campaign_key": "o-comp-1-gen_attack_10",
                  "member_id": "comp-1",
                  "attack_id": "gen_attack_10",
                  "step": 2,
                  "operation": "collect_files",
                  "selected_date": "week_1_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py collect_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.040755,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "O",
                  "campaign_key": "o-comp-1-gen_attack_10",
                  "member_id": "comp-1",
                  "attack_id": "gen_attack_10",
                  "step": 3,
                  "operation": "upload_files",
                  "selected_date": "week_1_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py upload_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.05087,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                }
              ],
              "episode": {
                "status": "PASS",
                "step_count": 3,
                "passed_steps": 3
              },
              "counts": {
                "steps": 3,
                "passed": 3,
                "blocked": 0,
                "unknown": 0,
                "reachable": 3
              }
            },
            {
              "arm": "O",
              "campaign_key": "o-dana-1-gen_attack_11",
              "member_id": "dana-1",
              "attack_id": "gen_attack_11",
              "selected_dates": [
                "week_3_Friday"
              ],
              "steps": [
                {
                  "arm": "O",
                  "campaign_key": "o-dana-1-gen_attack_11",
                  "member_id": "dana-1",
                  "attack_id": "gen_attack_11",
                  "step": 1,
                  "operation": "enable_share",
                  "selected_date": "week_3_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py enable_share",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.073964,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "O",
                  "campaign_key": "o-dana-1-gen_attack_11",
                  "member_id": "dana-1",
                  "attack_id": "gen_attack_11",
                  "step": 2,
                  "operation": "publish_files",
                  "selected_date": "week_3_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py publish_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.038854,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "O",
                  "campaign_key": "o-dana-1-gen_attack_11",
                  "member_id": "dana-1",
                  "attack_id": "gen_attack_11",
                  "step": 3,
                  "operation": "anonymous_download",
                  "selected_date": "week_3_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py anonymous_download",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.049983,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                }
              ],
              "episode": {
                "status": "PASS",
                "step_count": 3,
                "passed_steps": 3
              },
              "counts": {
                "steps": 3,
                "passed": 3,
                "blocked": 0,
                "unknown": 0,
                "reachable": 3
              }
            }
          ]
        }
      },
      "N": {
        "integrity": {
          "numerator": 3,
          "denominator": 3,
          "value": 1.0,
          "ci95": {
            "low": 0.438494,
            "high": 1.0
          },
          "unit": "campaign"
        },
        "semantic_evidence_coverage": {
          "numerator": 3,
          "denominator": 3,
          "value": 1.0,
          "ci95": {
            "low": 0.438494,
            "high": 1.0
          }
        },
        "selected_date_legal_rate": {
          "numerator": 3,
          "denominator": 3,
          "value": 1.0,
          "ci95": {
            "low": 0.438494,
            "high": 1.0
          }
        },
        "multi_day_episode_rate": {
          "numerator": 3,
          "denominator": 3,
          "value": 1.0,
          "ci95": {
            "low": 0.438494,
            "high": 1.0
          }
        },
        "attack_generation_fallback_rate": {
          "numerator": 0,
          "denominator": 3,
          "value": 0.0,
          "ci95": {
            "low": 0.0,
            "high": 0.561506
          }
        },
        "campaign_planning_fallback_rate": {
          "numerator": 0,
          "denominator": 3,
          "value": 0.0,
          "ci95": {
            "low": 0.0,
            "high": 0.561506
          }
        },
        "selected_day_count": {
          "mean": 3.0,
          "min": 3,
          "max": 3
        },
        "execution_outcome": {
          "status": "MEASURED",
          "step_success_rate": {
            "numerator": 9,
            "denominator": 9,
            "value": 1.0,
            "ci95": {
              "low": 0.700847,
              "high": 1.0
            }
          },
          "step_block_rate": {
            "numerator": 0,
            "denominator": 9,
            "value": 0.0,
            "ci95": {
              "low": 0.0,
              "high": 0.299153
            }
          },
          "ordered_episode_success_rate": {
            "numerator": 3,
            "denominator": 3,
            "value": 1.0,
            "ci95": {
              "low": 0.438494,
              "high": 1.0
            }
          }
        },
        "target_reachability": {
          "numerator": 9,
          "denominator": 9,
          "value": 1.0,
          "ci95": {
            "low": 0.700847,
            "high": 1.0
          }
        },
        "unknown_rate": {
          "numerator": 0,
          "denominator": 9,
          "value": 0.0,
          "ci95": {
            "low": 0.0,
            "high": 0.299153
          }
        },
        "rows": [
          {
            "attack_id": "gen_attack_1",
            "selected_days": 3,
            "expected_steps": [
              1,
              2,
              3
            ],
            "covered_steps": [
              1,
              2,
              3
            ],
            "integrity": true,
            "legal_dates": true,
            "attack_generation_fallback": false,
            "campaign_planning_fallback": false,
            "semantic_evidence": true
          },
          {
            "attack_id": "gen_attack_10",
            "selected_days": 3,
            "expected_steps": [
              1,
              2,
              3
            ],
            "covered_steps": [
              1,
              2,
              3
            ],
            "integrity": true,
            "legal_dates": true,
            "attack_generation_fallback": false,
            "campaign_planning_fallback": false,
            "semantic_evidence": true
          },
          {
            "attack_id": "gen_attack_11",
            "selected_days": 3,
            "expected_steps": [
              1,
              2,
              3
            ],
            "covered_steps": [
              1,
              2,
              3
            ],
            "integrity": true,
            "legal_dates": true,
            "attack_generation_fallback": false,
            "campaign_planning_fallback": false,
            "semantic_evidence": true
          }
        ],
        "oracle_coverage": {
          "numerator": 9,
          "denominator": 9,
          "value": 1.0,
          "ci95": {
            "low": 0.700847,
            "high": 1.0
          }
        },
        "side_effect_observed_rate": {
          "numerator": 9,
          "denominator": 9,
          "value": 1.0,
          "ci95": {
            "low": 0.700847,
            "high": 1.0
          }
        },
        "execution_evidence": {
          "report": "/Users/ayang/Desktop/project_work/Chimera/docs/dataset-evaluation/reports/stage2/full-from-scratch-20261015/q5-attack-side-effects/report.json",
          "rows": [
            {
              "arm": "N",
              "campaign_key": "n-bstat-1-gen_attack_1",
              "member_id": "bstat-1",
              "attack_id": "gen_attack_1",
              "selected_dates": [
                "week_1_Thursday",
                "week_2_Thursday",
                "week_3_Friday"
              ],
              "steps": [
                {
                  "arm": "N",
                  "campaign_key": "n-bstat-1-gen_attack_1",
                  "member_id": "bstat-1",
                  "attack_id": "gen_attack_1",
                  "step": 1,
                  "operation": "request_access",
                  "selected_date": "week_1_Thursday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py request_access",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.082093,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "N",
                  "campaign_key": "n-bstat-1-gen_attack_1",
                  "member_id": "bstat-1",
                  "attack_id": "gen_attack_1",
                  "step": 2,
                  "operation": "solicit_credentials",
                  "selected_date": "week_2_Thursday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py solicit_credentials",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.050264,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "N",
                  "campaign_key": "n-bstat-1-gen_attack_1",
                  "member_id": "bstat-1",
                  "attack_id": "gen_attack_1",
                  "step": 3,
                  "operation": "collect_files",
                  "selected_date": "week_3_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py collect_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.038866,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                }
              ],
              "episode": {
                "status": "PASS",
                "step_count": 3,
                "passed_steps": 3
              },
              "counts": {
                "steps": 3,
                "passed": 3,
                "blocked": 0,
                "unknown": 0,
                "reachable": 3
              }
            },
            {
              "arm": "N",
              "campaign_key": "n-comp-1-gen_attack_10",
              "member_id": "comp-1",
              "attack_id": "gen_attack_10",
              "selected_dates": [
                "week_1_Monday",
                "week_2_Friday",
                "week_4_Thursday"
              ],
              "steps": [
                {
                  "arm": "N",
                  "campaign_key": "n-comp-1-gen_attack_10",
                  "member_id": "comp-1",
                  "attack_id": "gen_attack_10",
                  "step": 1,
                  "operation": "former_login",
                  "selected_date": "week_1_Monday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py former_login",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.086698,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "N",
                  "campaign_key": "n-comp-1-gen_attack_10",
                  "member_id": "comp-1",
                  "attack_id": "gen_attack_10",
                  "step": 2,
                  "operation": "collect_files",
                  "selected_date": "week_2_Friday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py collect_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.038899,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "N",
                  "campaign_key": "n-comp-1-gen_attack_10",
                  "member_id": "comp-1",
                  "attack_id": "gen_attack_10",
                  "step": 3,
                  "operation": "upload_files",
                  "selected_date": "week_4_Thursday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py upload_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.050497,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                }
              ],
              "episode": {
                "status": "PASS",
                "step_count": 3,
                "passed_steps": 3
              },
              "counts": {
                "steps": 3,
                "passed": 3,
                "blocked": 0,
                "unknown": 0,
                "reachable": 3
              }
            },
            {
              "arm": "N",
              "campaign_key": "n-dana-1-gen_attack_11",
              "member_id": "dana-1",
              "attack_id": "gen_attack_11",
              "selected_dates": [
                "week_2_Wednesday",
                "week_3_Monday",
                "week_3_Thursday"
              ],
              "steps": [
                {
                  "arm": "N",
                  "campaign_key": "n-dana-1-gen_attack_11",
                  "member_id": "dana-1",
                  "attack_id": "gen_attack_11",
                  "step": 1,
                  "operation": "enable_share",
                  "selected_date": "week_2_Wednesday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py enable_share",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.086647,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "N",
                  "campaign_key": "n-dana-1-gen_attack_11",
                  "member_id": "dana-1",
                  "attack_id": "gen_attack_11",
                  "step": 2,
                  "operation": "publish_files",
                  "selected_date": "week_3_Monday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py publish_files",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.038976,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                },
                {
                  "arm": "N",
                  "campaign_key": "n-dana-1-gen_attack_11",
                  "member_id": "dana-1",
                  "attack_id": "gen_attack_11",
                  "step": 3,
                  "operation": "anonymous_download",
                  "selected_date": "week_3_Thursday",
                  "command": "/opt/anaconda3/bin/python lab_actions.py anonymous_download",
                  "returncode": 0,
                  "oracle_status": "PASS",
                  "outcome": "PASS",
                  "elapsed_seconds": 0.049912,
                  "evidence_scope": "synthetic lab side effects; malware/OS/DDoS/TLS fidelity not asserted"
                }
              ],
              "episode": {
                "status": "PASS",
                "step_count": 3,
                "passed_steps": 3
              },
              "counts": {
                "steps": 3,
                "passed": 3,
                "blocked": 0,
                "unknown": 0,
                "reachable": 3
              }
            }
          ]
        }
      }
    },
    "Q6": {
      "status": "NOT_MEASURED",
      "reason": "human blind panel not run"
    },
    "Q7": {
      "status": "MEASURED",
      "events": 2199,
      "campaigns": 6
    }
  }
}
```

## 边界

- Third-stage detector metrics are not part of Stage 2.
- This run uses one independent generation per arm.
- Runtime compatibility used: O: legacy_weekly_meeting_contract_fallback_after_workforce_failure; N: hierarchical_meeting_contract_fallback_after_workforce_failure
- Q2/Q3 are measured with actual GLM-driven bounded simulations and independent local acceptance; they do not claim a full 20-day employee execution replay.

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
              "max_absolute": 0.0,
              "status": "NOT_MEASURED",
              "reason": "no independent phase plan sidecar"
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
          }
        },
        "independence": "derived_from_schedule_record_contract"
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
              "max_absolute": 0.0,
              "status": "NOT_MEASURED",
              "reason": "no independent phase plan sidecar"
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
          }
        },
        "independence": "derived_from_schedule_record_contract"
      }
    },
    "Q2": {
      "status": "NOT_MEASURED",
      "reason": "full employee execution requires OWL runtime"
    },
    "Q3": {
      "status": "NOT_MEASURED",
      "reason": "no independent artifact oracle attached to this run"
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
          "status": "NOT_MEASURED",
          "reason": "campaign manifests contain intent and schedule evidence but no independent side-effect oracle"
        },
        "target_reachability": {
          "status": "NOT_MEASURED",
          "reason": "employee capability/permission registry is absent from schedule study"
        },
        "unknown_rate": {
          "status": "NOT_MEASURED",
          "reason": "execution outcome evidence is unavailable"
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
        ]
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
          "status": "NOT_MEASURED",
          "reason": "campaign manifests contain intent and schedule evidence but no independent side-effect oracle"
        },
        "target_reachability": {
          "status": "NOT_MEASURED",
          "reason": "employee capability/permission registry is absent from schedule study"
        },
        "unknown_rate": {
          "status": "NOT_MEASURED",
          "reason": "execution outcome evidence is unavailable"
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
        ]
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
- Q2/Q3 remain unmeasured if OWL execution or business oracles are unavailable.
- This run uses one independent generation per arm.
- Runtime compatibility used: O: legacy_weekly_meeting_contract_fallback_after_workforce_failure; N: hierarchical_meeting_contract_fallback_after_workforce_failure

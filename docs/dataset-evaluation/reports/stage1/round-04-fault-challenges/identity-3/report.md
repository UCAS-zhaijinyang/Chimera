# 第一阶段评测：identity-3

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 29 / 29 | 1.0 | PASS |
| L0.2 主键关联完整性 | 29 / 29 | 1.0 | FAIL |
| L0.3 文件与事件守恒 | 1 / 1 | 1.0 | FAIL |
| L0.4 产物血缘完整性 | 5 / 5 | 1.0 | PASS |
| L0.5 因果与时间约束 | 1 / 1 | 1 | FAIL |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 7 / 7 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 0 | PASS |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.2: duplicate or conflicting event identity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 29, "sha256": "733ba69d81644233b41228bbb9289e13437a587ee09dd00d9bbf10ce2f353e94"}`
- L0.3: call lifecycle not closed exactly once；`{"task_id": "t0001", "call_id": "tool-43a7ff83c6f5478c92a2c623d56ba8ab"}`
- L0.5: invalid or duplicate event sequence；`{"task_id": "t0001"}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

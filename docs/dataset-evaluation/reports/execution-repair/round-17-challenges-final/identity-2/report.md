# 第一阶段评测：identity-2

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 33 / 33 | 1.0 | PASS |
| L0.2 主键关联完整性 | 33 / 33 | 1.0 | FAIL |
| L0.3 文件与事件守恒 | 1 / 1 | 1.0 | FAIL |
| L0.4 产物血缘完整性 | 6 / 6 | 1.0 | PASS |
| L0.5 因果与时间约束 | 1 / 1 | 1 | FAIL |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 8 / 8 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 1 | FAIL |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.2: duplicate or conflicting event identity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 33, "sha256": "e781171ab25b44f8c9b9ea9784a3625a127771cc713cdee900b8058d1da66ed3"}`
- L0.3: call lifecycle not closed exactly once；`{"task_id": "t0001", "call_id": "tool-f394791456554ceeacb7e6c15b24cb05"}`
- L0.5: invalid or duplicate event sequence；`{"task_id": "t0001"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 1, "extra_or_conflicting": 0}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

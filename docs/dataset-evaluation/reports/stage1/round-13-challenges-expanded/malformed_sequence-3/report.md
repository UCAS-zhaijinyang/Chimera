# 第一阶段评测：malformed_sequence-3

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 27 / 28 | 0.9642857142857143 | FAIL |
| L0.2 主键关联完整性 | 27 / 28 | 0.9642857142857143 | PASS |
| L0.3 文件与事件守恒 | 0 / 1 | 0.0 | FAIL |
| L0.4 产物血缘完整性 | 5 / 5 | 1.0 | PASS |
| L0.5 因果与时间约束 | 1 / 1 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 6 / 6 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 1 | FAIL |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.1: invalid event field types retained；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "ed8352743ffd13619b75b84d72903af47d1d18850746f230d36d2b849ca8da50"}`
- L0.3: task lifecycle not closed exactly once；`{"task_id": "t0001", "started": 0, "terminal": 1}`
- L0.8: observable release differs from captured feature projection；`{"missing": 1, "extra_or_conflicting": 1}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

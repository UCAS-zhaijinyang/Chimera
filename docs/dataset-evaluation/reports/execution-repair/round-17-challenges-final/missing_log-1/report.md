# 第一阶段评测：missing_log-1

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 0 / 0 | None | NOT_MEASURED |
| L0.2 主键关联完整性 | 0 / 0 | None | NOT_MEASURED |
| L0.3 文件与事件守恒 | 0 / 1 | 0.0 | FAIL |
| L0.4 产物血缘完整性 | 4 / 4 | 1.0 | FAIL |
| L0.5 因果与时间约束 | 1 / 1 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 0 / 0 | None | NOT_APPLICABLE |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 1 | FAIL |

采集能力：`{"application": "NOT_MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.3: expected log missing or outside workspace；`{"task_id": "t0001", "path": "workspaces/t0001/execution.log", "exception": "FileNotFoundError"}`
- L0.3: task lifecycle not closed exactly once；`{"task_id": "t0001", "started": 0, "terminal": 0}`
- L0.4: artifact has no matching captured producer；`{"task_id": "t0001", "artifact_id": "693706214b34"}`
- L0.4: artifact has no matching captured producer；`{"task_id": "t0001", "artifact_id": "7544087cb17e"}`
- L0.4: artifact has no matching captured producer；`{"task_id": "t0001", "artifact_id": "25f07a8520b1"}`
- L0.4: artifact has no matching captured producer；`{"task_id": "t0001", "artifact_id": "fb1c2a1d514e"}`
- L0.4: artifact has no matching captured producer；`{"task_id": "t0001", "artifact_id": "fd51f5e4151c"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 0, "extra_or_conflicting": 24}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

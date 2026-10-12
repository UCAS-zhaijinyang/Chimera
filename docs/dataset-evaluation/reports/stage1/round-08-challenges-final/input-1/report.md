# 第一阶段评测：input-1

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 24 / 24 | 1.0 | PASS |
| L0.2 主键关联完整性 | 24 / 24 | 1.0 | PASS |
| L0.3 文件与事件守恒 | 1 / 1 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 3 / 4 | 0.75 | FAIL |
| L0.5 因果与时间约束 | 1 / 1 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 5 / 5 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 0 | PASS |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.4: declared lineage omits executed input；`{"task_id": "t0001", "artifact_id": "881fffae1efe"}`
- L0.4: dangling or self input edge；`{"task_id": "t0001", "artifact_id": "881fffae1efe", "input_id": "missing-input"}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

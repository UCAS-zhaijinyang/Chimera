# 第一阶段评测：chimera-stage1-live-golden

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 846 / 846 | 1.0 | PASS |
| L0.2 主键关联完整性 | 846 / 846 | 1.0 | PASS |
| L0.3 文件与事件守恒 | 90 / 90 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 68 / 68 | 1.0 | FAIL |
| L0.5 因果与时间约束 | 90 / 90 | 0 | PASS |
| L0.6 标签可追溯性 | 5 / 5 | 1.0 | PASS |
| L0.7 跨采集源对齐 | 117 / 117 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 90 / 90 | 0 | PASS |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.4: artifact unavailable, out of scope or hash/version invalid；`{"task_id": "t0021", "artifact_id": "181257434432"}`
- L0.4: artifact unavailable, out of scope or hash/version invalid；`{"task_id": "t0026", "artifact_id": "2beff8b65f0d"}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

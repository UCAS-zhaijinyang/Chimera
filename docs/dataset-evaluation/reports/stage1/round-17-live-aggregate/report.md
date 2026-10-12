# 第一阶段评测：chimera-stage1-live-aggregate

状态：**PASS**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 958 / 958 | 1.0 | PASS |
| L0.2 主键关联完整性 | 958 / 958 | 1.0 | PASS |
| L0.3 文件与事件守恒 | 90 / 90 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 64 / 64 | 1.0 | PASS |
| L0.5 因果与时间约束 | 90 / 90 | 0 | PASS |
| L0.6 标签可追溯性 | 3 / 3 | 1.0 | PASS |
| L0.7 跨采集源对齐 | 139 / 139 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 90 / 90 | 0 | PASS |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

未发现当前检查范围内的契约违反；这不证明所有未来路径或真实企业效用。

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

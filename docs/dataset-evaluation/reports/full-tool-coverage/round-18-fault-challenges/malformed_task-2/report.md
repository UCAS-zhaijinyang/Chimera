# 第一阶段评测：invalid-input

状态：**FAIL**。范围：input validation。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 0 / 0 | None | FAIL |
| L0.2 主键关联完整性 | 0 / 0 | None | NOT_MEASURED |
| L0.3 文件与事件守恒 | 0 / 0 | None | NOT_MEASURED |
| L0.4 产物血缘完整性 | 0 / 0 | None | NOT_MEASURED |
| L0.5 因果与时间约束 | 0 / 0 | None | NOT_MEASURED |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_MEASURED |
| L0.7 跨采集源对齐 | 0 / 0 | None | NOT_MEASURED |
| L0.8 发布完整性/泄漏扫描 | 0 / 0 | None | NOT_MEASURED |

采集能力：`{"application": "NOT_MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.1: study manifest unavailable or invalid；`{"exception": "ValueError"}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

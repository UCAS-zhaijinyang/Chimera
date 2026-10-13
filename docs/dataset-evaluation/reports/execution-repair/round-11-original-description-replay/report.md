# 第一阶段评测：chimera-repair-round11-study

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 1538 / 1538 | 1.0 | PASS |
| L0.2 主键关联完整性 | 1538 / 1538 | 1.0 | PASS |
| L0.3 文件与事件守恒 | 54 / 54 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 257 / 257 | 1.0 | PASS |
| L0.5 因果与时间约束 | 54 / 54 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 311 / 311 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 54 / 54 | 1 | FAIL |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.8: unreviewed contact/PII candidates in release；`{"path": "release/events.jsonl", "candidate_sha256": ["ff5838ced1b334988e943d344371ade555c7304f1c74acd4821623ed30d7adf9", "ff5838ced1b334988e943d344371ade555c7304f1c74acd4821623ed30d7adf9"]}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

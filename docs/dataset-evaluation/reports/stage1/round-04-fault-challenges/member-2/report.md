# 第一阶段评测：member-2

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 32 / 32 | 1.0 | PASS |
| L0.2 主键关联完整性 | 31 / 32 | 0.96875 | FAIL |
| L0.3 文件与事件守恒 | 1 / 1 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 6 / 6 | 1.0 | PASS |
| L0.5 因果与时间约束 | 1 / 1 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 7 / 7 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 0 | PASS |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "87cdd2ce6ef52b7ca80eb003a59750a5ac8c4c78f6b6fc1c9396943bb1c8bee9"}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

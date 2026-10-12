# 第一阶段评测：phase-1

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 24 / 24 | 1.0 | PASS |
| L0.2 主键关联完整性 | 0 / 24 | 0.0 | FAIL |
| L0.3 文件与事件守恒 | 1 / 1 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 4 / 4 | 1.0 | PASS |
| L0.5 因果与时间约束 | 1 / 1 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 5 / 5 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 1 | FAIL |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "a8b9f28fca6559697919111b5c9d5968321b930272c88fa844e70081109d3be5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "835565675fae9378979eb52557eb23ef712900af23546948704d6222ae0bf689"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "29669ad4e6ee2f0d3702fb6ff1109cd92f5cdceb1190cea278bc955d63462eff"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "306699605d00c6f75f91f083897082d506387797fd341119a9a329c4a55af540"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "e95d9f7fc6ab2b7c59e66d8637fb780018b4cedc5ea529b09f677f81737db90b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "b53c83f8713ab3819c5c9f62320f591e121484f7de70bbe48703abdb7c8e5e05"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "db392f6a1f361d712d1af3fe2135223a846ee988ad7a930ada71da322afa74cf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "1f8d0547a033253fd68d3c014424d325c72bc55c96ed8d74525bd2c46b8cbff5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "91a85339926212e92e8ba035cb09b68543c74e8d6730ba35c4287ece88641a95"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "972f678a20d20cea360f514a59af513ccaeb8aff00e934834c500f7c5f4a826f"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "7a3100cd745a183a8713ab3eb6678332cde4f0723df4a50a4c906d776993af09"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "0669b3f0ed8f74a1cc67b1f2df9cda242313a8f5c04f8262f9a041d9f410eaef"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "d31e6898f2868bbfa51f59b4d51c38101f81c7c4bad5c9a54119d1352a2bd9f9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "1542084d72f0587bcc5e7d86cf6b7ab51eedd69114c0c3c2b0c3331c7e83e875"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "68c34cf8c1122f3d8d2a0670ffbb7439e81a26a1722f72d0d0b28da875f91192"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "08501be4198fe94f4a3b4cb8659ff0ebe6f89df280491a636df9a7dcebbf5dd8"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "ac61ba8f67c283b5d9e41d38ba724cc73bbd562627c31a151e697f85d3d82399"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "917fab242430fcf7840ed1a47782a29d312811feacf7a4d099b00c5fac2f0fbc"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "4810b802e86e22c71120de84ae4a87cbc59819bfce69e5cfac26948b9d02909f"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "8147bc766f2c6079c650e4eb894dff5e46671d1efd758d052df5a13ca57d77da"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "9cc79e0549a2d8410e4e1f76d92e1b09ac930a6ca208ad9927a58d287a1a30c6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "515579307b451e20e8f6d91613e86af476638b6feb4204554f3ea2b77a9d814b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "c6178f04c0fb0aedf7daae58b7661220aaae869885e7c8edf70db42b98a31137"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "40badb556a818dd16d3d5e92aa72c590fdc2783f649921eb361e11f433eddbfb"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 24, "extra_or_conflicting": 24}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

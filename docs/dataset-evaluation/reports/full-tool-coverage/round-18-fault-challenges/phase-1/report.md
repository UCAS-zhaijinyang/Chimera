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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "d9487802158cee41beb44393e2e31a93e4ec82fd26bca95d20f6cd32c5c52089"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "0ffc1d106805f56d24cc357e0b47236c8bbd275293fce3ff96b25ca4dcbbc193"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "9d53ab1d43d19ec34bf8c8d8526f8e5e01b2ec0adef1a71dda19d2bd09deccca"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "9474432ae4a22be2e0c84619c1189aecc8791d26529921fcfd7efefc97e016b3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "8b7e6ca3f69bceb8d0609177c818c2a8b0954afd4581c14abc3201a83748ca8a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "9f45bd3ea85498ea2980c298b6b2a2c0acc80aa7e006c7e72d6202a1c857a4cf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "da3c52205a08272016dfe8e9abada16a9686b32aa90c12078729b17a45c29c07"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "538856f7372b56facce0bbf34306288a80beb020ae31b28a486337d95a9a91b1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "873e070312fb91ea88317d6594d73cb5b9531ae6e5baaab6deecf4c14400f3f5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "271f1acb3b15e05e46f0f1cd353991cf28c80b2f537d920fb2c02f46f234dbdf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "1a0aa91fd55e4793817eebcd4983e9a0dc69dcd80f05ceea2cecf3d6aa2ec383"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "d55391c64e1ac2599a19882ee4af4ec48ef866e98f30e279203e5c3449804c4f"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "b4f75a151df979184bb7d6f7aa7900d162d64fc8682d2d38b27e2f1fa06fa7b2"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "f805da425346bd2ade3c9e9506770332a16c9becaaa97e330eaff73431c673a6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "25b321f5cd8cea3f4ab9d3b1389600059ced0346fd6eacf0080dd39fdd4aa8c4"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "008d2c1284719c28d7808c2f90f17c36658e6bfb6a8e4af15861eb65e96563e9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "a0316cba720e50d0338dcb69370f6549d15160ff53623ea2bf847a879ac3b99b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "288bc40844fca3f6d58d438526c1aa8671aa53652f3af69b1b6febb0812e0c98"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "a6020900de2dd22eaf2ad5119f47348dd8df3e6d5e9be9e5fa3d308a07c99ef6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "8e58c78f23f71c4c37d423162ca2c71979e304f9ca3acdae0b31a943c7665a3c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "a3d835c1e3b810c17ca853ba3dcd749acd49a7270191058097d68151cdade5df"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "7b2a6929e8e09a85c4ecc382037757a638f8c7d3c96ab97faaf0c8e349d22d55"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "d4d3b817b75ba0c2bb7ad974c69fb243b38382c9f28acc8a813de8ab110b851e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "6db4e84574ff760f71ccf3ef2527b9ece3aadd1a6af51309a2a7b1d39d9ba380"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 24, "extra_or_conflicting": 24}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

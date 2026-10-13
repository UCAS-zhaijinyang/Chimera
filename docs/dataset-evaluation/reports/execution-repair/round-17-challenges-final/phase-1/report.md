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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "7aa6b79ae4e66133262817cae3da8b2eca6a5cc4bbdd48a1286a76e4d701849e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "4030a1db83366fe9ffe227b8de95afae3c88c3bb50013fb39e04b761ce0094c7"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "f2389b26bc174436146af171107dfc4d08866795ac5a48392ebfb29ca0eb1b9b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "e41c4583248159f1defcc65ad29cd539691c57ed19270ca9d6248640ad5e21c4"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "a6a7f7063e6ed5f5972dcc4a91a417fa7a00a132be86b35c0a1f4b171828e09a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "0cb657cf86c832d33cd80bb9712b8906ed36b2db74b357e62c33330f595aa075"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "0fd88c13de8c6175f2a056854fe06c7a73c2d4bb105f227df0f94dc76abda68e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "4ae32efebf86767c30e37370cd840a8376b9749f9bf07eeeef99672d1b7ed146"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "e8397607dc487c97977ea9691d7a3ede381b8b4fad00fc1dd828d1681758cd89"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "1580e7e64c05373dcba906694cd1b49ad1b3992a87b0584b230c6f76e9a8d7ea"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "86a6464ac2dbf8581b2df766cfaae891fd29a0cf7ed25003a700251f85572ea5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "2f0924db48b8118c9083a90360c04b4ea8c5cd9fdb540fe4b1f244eb18f5d1e0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "3fe4071610d2d07eac0b7ce5f1245f33aede23b518379e9e149db8831434c4b7"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "0bfa348b4b4f7a3b965ddc9214f44c23550ebe25c61ba185d4a624345863e945"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "6b5a6664d551c544e2863d42b60b58c4636fd2ce36dac0c5c50fe46eb6f8efe5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "7b6537767c72600143d9fcb84b53e4920d550a51e907e89089cb42e99d8a4969"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "9033ad2ad037497e49ac07106880b67626db80114a760e8e9d0ef822ea24a478"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "f209f7be3afd980c4d209fcfd509127d3d83dd281680c753464965aff3b7fd33"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "91e03b1fdcbdf1680d1a8debbc93ea2dba290e711100bb463c0b539b4418305e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "ceb1024f84adb77f991c81399a85039cfcc643937f52cb3add852071e2500812"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "30380942f8fea9d537f909008fe22ee5ceaa6bca934cfc738a4e39379e1831eb"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "479218cc7842ff15e9b23dc6280c5f43b8d1db815a35daff83c3ff75464c2094"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "2eb4171d40fc12589d2bf9119e2922aa5243119c1684038ad0cb7d3fbb221fe6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "1a65b09ca4202138da32ab43dc81726b7fbd83847263e0398ff266af936acff1"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 24, "extra_or_conflicting": 24}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

# 第一阶段评测：phase-3

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 28 / 28 | 1.0 | PASS |
| L0.2 主键关联完整性 | 0 / 28 | 0.0 | FAIL |
| L0.3 文件与事件守恒 | 1 / 1 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 5 / 5 | 1.0 | PASS |
| L0.5 因果与时间约束 | 1 / 1 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 6 / 6 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 1 | FAIL |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "b61ff4fa4769954c5feb50ca25d9ff45e80d27d49c09ac7ea99a565eeee4fd3f"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "a6b672f9a1c3f97a1fde946706ad55839a6fe9584ead9ec031806b550adcde7b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "a2387e533aec71877b6ccf285e130e80a948164ab79673c754876946c8bee167"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "00336704afe0d01073534b9ea43f20720242b121c349c5f6bf36d94df7a25f95"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "acb02dcb5eb25db56970283ad52738672bffb71951df47b1df1e7b17e161b9d8"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "e17e6f0bd03f6494452c9971204146ccb17cc4c4b88860bf2e51137b37574c53"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "41b9d4ea54427f999cac6fd764f7d1cf044607265f53425019110a48c64d8b2e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "1aed6462144e7d610f67265073ff01275ab263ea82280daa9657e05cffa2a1d0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "cf7df23cdf9b7d089abbfebfedba53f1bc5495c0718830589d42422765502c93"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "8dcbe29f62a0747554d9a4693bc41c765f3b38efd720d245f1a1a291eba3fbb5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "05ce1287bedcbd7f3a0facca8ccdb328074ac0a9cd4e5948deb08dad23666c8d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "8e7e96b70cc7f19642d9980230695608394107d37897196434302e59b4c21d27"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "7b6d40b553b9040853cfbda268ff4715cbb655e18f024b8790bd52b71cb7c271"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "cbec7c10b032145185874e3e639796c299d986c6f592261875ad1272e8858564"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "7a90c1e022a599bc507d4af0b4db846abe06129cf1ae258f2b7e144530a2acda"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "fe3671ae28c23dc80d02dbe047b00afefd5c4687d63dc6850a3c9dcfdd0f0659"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "892a4abca010225826d4eccac1ea9952248069f60a7cc970ae3e1998534dac4d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "19e3cacd12f89e2941da7f0b5344e2ae3c217cfaa2e7876305b1ffd9c9c8e074"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "b273dc7a65cfb56031f501473c6a38c955b9105d0f969042b6f1d69ca4b80512"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "9a38f9014c22de96ee4451ea89ca8f921f6a91cb8a331fe342f0c8215347f459"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "1d93508b16b9ec032e0ab43ee99f206f34955edf7b37cbb48718a5798d877bda"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "a987453144dc0af4121d6b86abaeeb7a9cf5194d74c3fab6a7909926b4782157"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "b1b0fbddef58b8ee5b40a6b2693a55c00409fb6a2426b9f4cb2b763e538c0316"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "5253f08b1d569c7af319bfacf4da0628659a586232225d32627f589afc36ba04"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "11000c3524882373ec6e603a4159c3e1827f00ec62db9d6b3eb13192f134ed10"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "57d91ac8fa7f349939cc9a1040b4ad1bbe650934081cbf31e2729bdb7b97b2a3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "36439c77aa141d556364e54a80f7551c4bf354039791913737e36da181c4d397"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "8b7bbc86f97393acd2f2da46fb319b5abbc0a3462a86d83fc3cef242dd7604e6"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 28, "extra_or_conflicting": 28}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

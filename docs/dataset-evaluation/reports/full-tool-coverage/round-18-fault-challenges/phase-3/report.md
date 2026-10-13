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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "9454747a9b67845d4c6c66e2e45d0d7c00fe8719515c1a3234b6078aa516a594"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "9c814ac09255970eb3977660bc1085ad24919b60a8ef9a85e7f4695c2675b4ad"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "20c28bfd91e1f685bc65d66de0a83e4375568b11e4326bb96f9c9d3f5a9ffcf1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "25e66bb39c8e4a7b0b0d2fc649bb725f6d001db1cb0b021315dae2cdf4a2b037"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "a8068176a4cca5505576ab798d7a93feac271743d104d773cc249537dd492850"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "fc19a9c2703bf4010482ab6bf9a3bd808b60bf63832624278a82a42325200a48"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "3f9e856397f7566f95b9d70d521687e90076b6298c5892e9d2466630e67d6d7e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "2e6f5e16a845277951dd2397ba6aa36bab3385baed8c41aa89c24f17b844bde5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "d7db4cd4874d028360121fd772144dc365aef0369bb0d9860908b771d4497236"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "a9786805cb09a2ef0f9f3255482f23ee72d567606f8a59dfe29b1aa1651f9afa"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "12e656a62f27fac5c52fbbec2a6f3e2c5ada53d8f296dd269c8f1d5c0b2bfef2"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "aac04e442c89e01691c5b2b3437d5add1b2230d2f5c59102865992c40f2a550a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "bf62fc5016998094120ec19963d7c6cb051fcdf4de44408ca619b753488af058"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "814572a5dbc59cdb618f1ff8fac86940ec420145810380ff2e3827e38555c01c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "d5c4367b10c72dfa1da31eee7fe9e8a216f381aaf5eec0320e7c5052774b2c10"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "70992078b97a22128c9ed9bfaa77ad34d8582c2f546c9f925eb2adb1094424bd"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "76a1e49e3595c28d8690d28ac0cc2d097bf1e900bee79105907767f21b03c945"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "bbb5e4d3091dc5f7e9e04136da01549c9d2a377d761789431b737795d3848fd1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "79ee27c2c2dd82fcc18b8220fb72bcd0a42915121969081a950ffd3b09f7f1ff"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "03398f6601ac8c62910ba88a05256bffe970b20fe9dabe433792c02c9eda5376"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "d7ce2d2bb42baab048361349f36f5a1f9c605deedd60be112b45073cebf2b061"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "97a9fc7b6a1c4c2b36efd33440760aeff461e45a8df1d56dbcee7c57d7f176b3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "b61009c82783c0ebb672718b6da899cd7a9376c5243984c9e81747c7c2c24fc2"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "b477cad01191cba7caaa2154467cdfdabc1f9e2d83b76db33154468a7899b951"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "171b77df7775cd314382d5ccd1694c830f782315dfe8199bff2b97a4a064ede0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "74bc3061d5caaaa58edeac70b7f8abb0755d4fba00700e5ee3b90afd7e7319bf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "3f0faf0748c97281a21232c829b14d6380b624da0c6bd4e6c9096c9c7eecedd1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "5610804c5bb30f6862e0d6a64f1dbe86150ebcbdef277b6da535bc53f845ef04"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 28, "extra_or_conflicting": 28}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

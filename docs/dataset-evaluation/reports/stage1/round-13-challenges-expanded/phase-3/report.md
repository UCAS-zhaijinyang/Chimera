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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "07925c47e685e7cd1d895d8448d42a16747ca267b86a04a4627b2b0b8ffc3319"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "59ce05833eca903ba920488c3a7eb4d3e33e13159ec82f9e5a5efd8e09385afd"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "974c0e79ff0082ad4049c917afe713fa09557dd9036278a830b62f6891db126c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "13ed233a7069e6af92be7a78277869576db255d0dff8b2eb82295af9a747a557"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "466cbae4481e2894b0b78c70b46f05f80f0c5763581158e88a55880645a4d0d6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "3f7b7fc933fef15643142cc61a14ea4d3c5624bfbaa9813ef2413f556ef6c5c7"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "051c646c1ad05beaa7ac6b771a3f76264870cdc078501b376f2d9520280611f5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "4d7784384788402badf3c14205524fc0a67e184ae82cb92d4e803de0fbc3f466"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "c6b71844a7b470c7556f29e06d41f9a73de54e622614261cc8ac492356d56fb9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "8b3dbba405594162348bf9d3ec0caecb3f045ae49c1be918a8dd2c20008d9507"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "99e8412ac0b3e96c758b2e976b5521f8e23ac757553f3731f8bfe298276bc197"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "45f3b097c051c6299a785411fb07ee14668054dc961315e6ff7355ed33ff2b49"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "7f489654fb673e8cfb6119de30ec3e5dc5abfe488437672fac6901fcf7d5271e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "639a8cbe64f8f2fe9ab08336426dd0cf9044cd38859bb58f5f605fe7512f46dc"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "75b6d846d7b8d268dc93476b2f289bf02688ce4d41b465ed6d00920434db135f"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "ffb56570642adf13ade18c52de21c67865fea8f65caf1487f9755d8668813cc3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "2bc57be2b33a3d5e05c2fbce791bc4dbe61dea387ce4e9bb2889376491855b2c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "a61476c877dce53f50fa2fb6f35d89cda6fdd1872e75b33ca5cc7b15ac8d8d62"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "aa920174ca639b8a4b68e76b47b71dfb6ece70eec9f24efa849d7b4ba826d603"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "1870dca18dc158bb93d0a0b7eeeb400ae4e0149f64c94084aba27a5ca8fa34af"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "85643bc43604e1466c8737dbac7d8a21e215c0524ed478990c1345498b45357e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "ad24d61305ca61a9a86d1c1900a3fa12c43c3894f85c3c95a1883eab872f646a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "79058e06b8eb0212dcdd755153264377f3c4dc818951961ec50caa97e5db535d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "518ee1580610fccec7638eaf2389bcc1cac2f7c08428566ceb1ea83283a6336f"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "1c9bd961fdbd3e4185fc840afb4f043198bcb43ebf1eef42f4a4aea908f7f153"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "5273355d26acbe78edde49615e34f1cd519d074a49f43ed2f1b84fd11ef591db"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "3e3afc5b3dec8c6403cdf3408554a9fcab81de27222b114528eb8c3639948585"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "dfdee12efbb554bf77eb6dcd0a5f7d5051deabddf08df479a3dbfe0de09be367"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 28, "extra_or_conflicting": 28}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

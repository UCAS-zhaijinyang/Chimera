# 第一阶段评测：phase-2

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 32 / 32 | 1.0 | PASS |
| L0.2 主键关联完整性 | 0 / 32 | 0.0 | FAIL |
| L0.3 文件与事件守恒 | 1 / 1 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 6 / 6 | 1.0 | PASS |
| L0.5 因果与时间约束 | 1 / 1 | 0 | PASS |
| L0.6 标签可追溯性 | 0 / 0 | None | NOT_APPLICABLE |
| L0.7 跨采集源对齐 | 7 / 7 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 1 / 1 | 1 | FAIL |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "4afb13bcec78d4fd0a3ebffac41a60427c51a8abe1b779c6e2c297728b98c1be"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "08508263c94ecf5e1ce793588fde2fbd75b478245a1f286a0a17c77b91048488"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "a8fe4268e7ab09b565c324b662c8af46cd6b47ad4f552356b4accc5ab29675e9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "6a4d4516c2e17a447e76f72de2175cb36302b6ee0c0c70e0514623f9cdae1c99"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "b3a923313ce62a97a840cbad372ea9294c017652b4429e1d0f797b5d9a7fdd0c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "a9ba3044f32806db48ece7ced910d103b6c453a4893bbc768c666872abdf7be9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "e057da0689e5bd55f2558cd8d506bdb8b7dc2bdd4f502789e589884e6a3cc9a3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "99c1516c42a7a866f6bb34c3a35d5fb6dbe1bce75facf1a345bf30ea25cc8562"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "2ebad46c811a5cf516ce9888854dbc8bbacaf6456ea292bd5dfd6dddcd3700cc"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "4cb1250a580e82ecace4eef53866cb98474e444491c9e0f21fbd474871e5a1de"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "a8b167d2d260d1bc5d6b2734cda42a9f39ee7e9ba3f417c3148ab4ae18024c74"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "b76febb3c48f6d39e2dda7963b26462c8464032bd76f47a02bc2f29d7836ae43"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "33bb2b172570c4d494edc447e6887ad98933be0631c12c9d800afa2248201fdb"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "070a22778d44543a6cc0d43a33a6c00b869c91ea5a682a212fa6d78dc083fe12"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "699d5ef1317a3ec35c70ac845adaa0e60b9e6b8193a42a04e0a8ef4780e7ddaa"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "a6eb8c00f0e94d036503190b926e12f0b0a15695c3890d2f99cf261a4cfa124e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "f280c825ac18e345c3f16cd29b022fae5f698ef149c98220ba4afa276565277d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "c74f2e78774c4c4de6926b6d73f70a9bf2aa77eb50e457a388e0a8fc1187609e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "b70d8d4a5b364c822f8b355fb16589008752a15daf66c8a227207abf02f59108"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "dbec13eacef5e3df9d7c9678d121c943682d7df1d2b3b7519b7af1df6c22ab1b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "c7ecc8cca559d4045e7c0c2d70d53e84e6b59427d4cde607b65a5d28d23bf334"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "23ca8077b54ab3f86344684ce8be10ec7a51a48b2d63049094f07eb26c4c10e8"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "90a110c482a5bd230dbd38b7d91cf36813d10b8a254870538c430522edb4e8f5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "a6762a08aaf88de0198cc441b89120190ac3ae5d9b8fe85168473e2641b727e0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "5ab8bfa0427a62371a3e635d3d13079e265f6bcee067254eb06f7b34f303c1b2"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "99ae484726902806935dc9152d277a086c21ee5fe5bffdb8bf2eb7962278f267"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "c889112bb3276041571155a52ba21cf7592e25b627d483efc6503bb369c0da6b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "76c2da1a632e498aa3e41b347e082f7de409dbf3d7d71561d954a3f0c56fcb99"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 29, "sha256": "3793ea895d3b93f27edc5c821da6165c58fb023079e36e8389a674dded894c9d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 30, "sha256": "e4a851d04d654febed583003c6d1668a7465eaee745253cdd962927cf7ad985a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 31, "sha256": "821bf7d74f11f4b02c5476777ad94a84d5a953183db8e0c27b7fd48e7777ef20"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 32, "sha256": "ef85f0952a5c1d59619e067484ac2f5cb7b4b6cb6324961642986b0b851d27fc"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 32, "extra_or_conflicting": 32}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "8ff7724e7b86eae60474dc033789884f33a87244b2c051156abb20168ed2a70c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "2e7a8c11019fdde54155470cb8826cd79e7752ac47f0a1badea9a454a601be5d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "1f0c1e492c64f940643f40522e8ba1493bf6b2d62f82dc065dfe326b5de414b4"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "c392ad7300a1a4b55cf3aa57dfc7f91dd42ce5611dde74caef621f7c6ac4cab6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "134172a8ea6b91bcafe8ca0d0d427e7e8652c6fc1278628c536fdb8385eb9ca0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "ece33bf22932e19e97c450b45900fd96eca7b846640451b8e68f6ffaffa59594"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "fcc5fb44a0ccde018d20725ec670eb14bd2ed76d42a99eb3ae2096c7e31d7d59"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "b62ec58c25a5fda18d640b904ae8e4d239aad3cb698bd2f4b7c8977c95b9b257"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "e6a23bcf245c9924960175cec6598a010c33a0093db33be3ee1e4f0986404912"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "8eafd150dd39a62d6a354d651807d3966fba6ba966f010e2d0bbc018f895a7ee"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "7dd6f0409ce46aa0ae6d56ce1482c9ccc3bc48ca40a4576adc097ab1655ae544"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "ad74837257d2ecd2a4b8165b2e30ef6603a37e54622e350f1ad44d73593c7357"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "6875e714dc96cd975bb5dd95944859b2245bae2a20c94f8530bd18cdcc23595a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "47bd1a0cd732cca60727348c1d66e134a0ea30f49bd44f1b9f8e0298a8322b8a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "e1747c12816212a0a93e8cfc52dfda390471d8930d62a8f4eaeee7ddedc6bf60"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "62e5326f912f25b94b3c1ea8c8f6da32b1fd05eb49f06ea5bb67fccc5ccb0f13"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "c80995bb86b7ea1ede41a917545fd008a31f81b4c11bcc737b38ed7af26e369a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "1bf0410bad08d7c3abc1e3635c4b2819a3c676b935a7fe179c809f333e094428"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "e65b8bd20bbc52c00cd31de7a89af02a3842ed57f49ea77623a01cacd1996c42"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "c39bf0d820a4ae5971ab4cb9419085bfc244611889988bcac971dc18f16443db"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "1d988a52b02783fdf0e446693b661cd687b0af3fac440a75bc659bda24bbb86e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "4e38fc6efcc40974bed805d423af9fb8ccbe149229e78524399f777ac89e58ca"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "cabe22821173d0111561a3ec472bfb100b5e445cffe35f0fd823e1206995da04"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "c4ceeeedb3b779b6a83eb15b301277552435ac43d0cd2a154339432cb9b7b971"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 24, "extra_or_conflicting": 24}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

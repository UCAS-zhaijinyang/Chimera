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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "8014f8fd1128efe4c12414c97846f43ea3a2d4e5f0b432fcd865dcdc159b0d0d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "390bb2ed5a95b87cafdf522c5250c824b88f7c9b83ee72cd1479ea91dffad515"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "4e9b8035ac57521b04c58adca10ae3e70c2188b71c1fe3e65b3bb7af51523659"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "6341d2e3a27b1a5a97023959619b61441a96cec19d1a1210d22db3bacb03986a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "bf1fdffb1d8ce36b7000bd0c3de87581b55cc0bb153fff39b745b2cb417142c6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "a24cb12fc696cc12aa0550c0259209029623a667a5bf03ab51eecc6a244cc401"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "cc8b096109ca94a45113516931c8a6c97c63f60bc9110efede6d7d4850f0a266"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "f939c76944022ff0d9728180fcd2e41e4d9605564b2f2b4e2de2e4c3eb3d1d5a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "20deee1ad82a75aab29a3cfe413f25dc6082782a081bf533c6b076660c27fa32"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "2db4e67edb94da3eed0960fc4d857b64c237b9651f6ecc5aeebeb86acb909a8e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "58d28b31f92da329c2ef2ea65605ef19090a5ab593217322e4e4dfe7e6a31ea1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "0e0ead6160d65a9f779769a1a8ab723a85930a58c6cebc924d823f3a6a18706d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "5f4f679a543e8f665da1d577c7849312eab23321e1f06dd9bd4ba7de70922596"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "d7ae0d846c64c69e4cab3c5d62b2c0f2ff9045a8c2f40bc37eff2105fd8991bf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "bf1df0b27116602759e1a539d4e9cf53d1ef6bd93ac04006f37f5684390196c8"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "0cc13d1a065780963796b22cb27d7bed8711070c6f1ece7ed7945fd5cb37d877"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "b12e034fa82579ca73eb1a7ce1bb2822584320d62a9fbb0f4b81cf24697f81e5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "d87f82bc901ba1e89bfb5ccfdc4cb9d5cfdb890ec57ec9963be04352a2a57ca5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "0290a91d66aa2b26d28b33bff698427a13af43dbb85897a5fbb589a4680ef355"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "cd3669402f3c93c6eb7067e5e463fe4c55eecd3ebaa2501d994ee6a7aad961ca"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "12b80f57ec473accecdc2124c8aa72c4c3829299bbd4e6b29129902229a4e0fd"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "11860d36b517d517a602958789d4ac985addfd6958937aa11ae3a13c240d45f1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "98d191b3cd3507cd9acfaf9d8a4479a8da9cd7981a2bef6ae1d53799dc1d729b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "e2d0446d68c194f80dbfe0ecd46b598adb3410960b824ba34273813b442a22e9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "ee738f3708596aa2d38dff3d7b4df46b32e79813022038903441395be19a3d58"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "110e6c751ff6a52d9690a51c66eef345db7e03ec22d0cd22c866a5bd4caedb18"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "e1ee6cbd0b6f5f433979793e63454b898b459c7399fd3b4ee21fa64c6220a70c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "ca1b791ff8ad24b9b4fd5a1f29fa1d105c4cc6a399c9e0d38d827e7623facb8b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 29, "sha256": "2e805f1f0acbd6ede2959034b804c9ed442b2bf281013bdb05803cbd8681ee61"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 30, "sha256": "ddc9081b553cb11063a621ad2ba1b3783d87f40f6c7327f50e38ab5ce817a571"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 31, "sha256": "c82746e916cafba6930eb31dc2c4acfd1d2d126078690c4bf2bb362c7dc9c1b3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 32, "sha256": "0e508e7f952c6922896279fdeab342890ec69abe6e1618866737d48261d3df04"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 32, "extra_or_conflicting": 32}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "41139ab8b5b2d284ad277cf25069581156b6971c05f03df461aaf25511c225f7"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "ac99e89c1a0ea32aa75d5fe4bcb4d83bb6fba849615ddaa66157a566c1a4c38b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "ed2f1dc1677b6bcb66f7662425e27edbe9c1492b9dffb484b21a14b332cadb52"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "18e435e98a4521aebbc469040e6990b4073b641b8a258c5f96f5d80b576e3c3d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "fdbaf911eb3777df0157190d9238af83dbd0f661ed080df31a51a9b8410630e7"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "a86103a6200c981b08553e48fac80ac61a9bd730f67fb04f47404300c7169a6a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "d74b19aaa2ecb38c02142add8f076d5b19012a9d2079e0a9acb0e47e0acc0f50"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "7b3355d05f4a876676ab5bf388ad1e65e60e7d884e801ab802f30653af8cc34e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "fa7824d381b18ca013a220bf17dec4a014332e1d5ff517049d5f40ec94d7c4fb"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "659d62d758f002fb960756925c4d898532eba8cbc7724b279622efb546b4a8bf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "f5e8818ffdf99d545aa29e4eddc62963426540875808cef9222a1dc7d7e29220"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "1abf8fe2ffe6cd3e86da61d23b16daf9cb0fc2a1c3fe0f6577215eeb383fa4b3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "7576ff038d3ed2fef9539323fa27a735b7cb415c3f24aabcaa2936b821cd4879"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "e6d4f5bbd30855d3c4162dd2e897e2e56e70fb55ae8bbd16c0250b1480ddef59"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "907cc86ec4c4365b3b7311aa2efa7fd8d353919820af7f6fe6800c4074458068"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "dad955caffad4b6ec92a6a46e84c8705153412a4ea88d8105e50a8ffedaf4ebd"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "0862b2cdf5a44c16a16d5a29e038d9bfea7248e733dd9823feefedac2cda951b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "d425a46252110f18aebae02d38030e19545dfa4cfb668bb8d5457c229012281c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "556d9e6f2ed36d782f6a3c21edc0e682783dfb7afe1f8dd6436a4d8ae706a16e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "bb405c495e9758fc0479fa9a1e3e6958caed2a0b63b32fb046441e9012f90cf6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "21aa7cc6b48df5f8aa9750fd3fb8bb396c711ef9178ef78027a40f92123e73b1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "992f5ab7515d8efd8e8cb424e29f1cf7e7a508b9dcd11c676cddda9570dcfaf9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "929329da9d78583320651d378ea90fdec8132cda8b6f24e8ba9d791abab9d60c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "4698852b0960997e7adb24014cac30af9ab69fe8e07d2a8213f14bded2ddd105"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "bfe9c9cc08646533e3f16a56dc871991d6b12059f27f133fe1db4b3eff18c4b0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "9512b4e03c75dfdf00fa6e734107a380d51e2e31e23263ee5c3fd9b598e87cad"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "d125881867500c56145f83172783834853093938a7de11bee7f4b3b9d47cfed0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "95eaa37cd97b8ecf5f582cc035ae249cfc8d98ec0aef07f673ebd8021fc6b1b1"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 28, "extra_or_conflicting": 28}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

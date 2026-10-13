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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "aa0bd92301b5ab96677ec79bc4de3b059d60836dcbd234f58f9266cfd0516200"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "5dfa4a363d6a0e9c4b0fee9e072efceedae00a6f15bb4a3d6ea9521b7581eacb"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "f02ae7a46cc49777116c757015365e7d9d2126a26de6c8c5bb6815e8bc1affc5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "2d50a4fa67653cb807b30ccfe2a2c5c6e5edd21163215b2c9d72a834f4fad214"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "b984c78b4ce3fcd7371c966d8aceac0a7db675340ae26101a43920ab92dbf989"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "436964fe5ea434a698420b57f181a817ef278dbad6a29edfdf6d08dd57273fa3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "8d8ff4054e15f23614154601d22b6ca602db393bd7302cf6583445c5a66d48a1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "0a285f6afed9e875c2bbd8639f074eed6ac328ec53114091790e041daf6e45d5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "57b6f385c6e7d4431c7c89129a8905a117010ad3a78db7c277767276a04e62f3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "b7c4b099f6ea32cde68cf9c0868934ce433d3cee36d9726385e97d1efd8d514a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "08a3bdcea6f552acbf969d39ea5e86f33ab8fa66fdea4c447fc8c82a0b10e12e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "7b93f08a2b74105a0f4e8ffabd2cd51442d47bf92e5acfa97ee380d8060b8ab1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "66ac26575f5c0fa4e6dc005baa49996d74d7d571c54cd5779a2fb2421d082964"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "b7dbfd9767f9994cb350e6e8b27c91247cf890c7f918787a8ec54d443aa118ee"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "566d2390fc8f64d7dca3216a43b1d023f371902a766d312f833d70f8e12b7ae5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "687f5e18ff29c252da0af4431cb3df55af6534d7eec35ddc37e66249c07f4bb3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "e31d46be838a89e4b5d2c0e551cb2a4aa984c3aebde3522d54af2c756d75602d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "115165a38c02b2d91f6c6a967b5d1b69ceb28d034183b8fe593fed1f945eac52"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "a771335fdeb008793b2faa47b0a008bf4a3fa8fca0a863481c8b49b3b45a8e78"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "457d2758802ef186abd3e176354e4853db36fb049c79cdae32c56058361f793b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "cde79c9a7aa8b814996ea3ad071713a456fa69e45efb1135f4944e110534aa6c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "2dc31fc80ab23f0149a89db83a2c081020eeda4d527d8876990a234d7705e441"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "6af35c39db02a4c159bff298b258930a30b672bce1774bf0454c870f3292de09"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "e763f90c5c09e84a6c175b2acb536ebdcd6efb1df29d4ffb1d9f96bd7c250ea0"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "3793807b0592487bbac218602b44d5bf1a73f139be53610d4cacb167ba973d02"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "0bb136a96024fe7b6c56306a0b2b3016418557f45ec2b97f918f0962b7796735"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "9f1b3d054e9fb29392a871cfbdc1436e8031ff452ad6e33c5b7102e4320ffe9c"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "470d2ea806e2751d56c0fdee12a13ae23b5360bd886284446fa1110be3c7e1c1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 29, "sha256": "73a2eacdc75fd58ab06d6ca2a84119a8ace2dcc20289b444306968f9a4401a4b"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 30, "sha256": "704a2eda1c16db888a986b573d1a8d3b6bcdf3e45cf9e86741cc040caac95faf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 31, "sha256": "19ceeb580ac8e087948c7597edfbf674b4db75d7dce6817bfa7a561231558ccd"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 32, "sha256": "67491f72d8c30ae6d2be68c68c67889e1f47c49132bc9e616a89958945a844cc"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 32, "extra_or_conflicting": 32}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

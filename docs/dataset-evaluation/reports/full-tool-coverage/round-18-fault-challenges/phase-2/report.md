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

- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 1, "sha256": "c4d37e4d71c1092d4a5ff9f5817006580448ec2c0e8132ec0b8fe748ad37da8d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 2, "sha256": "1ffd2bfd637522e135a95ea8cb856d2aae2acb499ba4e0c403495e09eddc7bb6"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 3, "sha256": "cf1be5f1f7d8c9604247f604b7a53a98829f4ba59ef3095f014b2b6127cccf8d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 4, "sha256": "3f9b73b711bc994d095000c62a6be1d069721c68dd0577972c1b7de2a9c46bc1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 5, "sha256": "04b086910447dc865b9f8f6b465c5bb147f8543a857e3acc498462cfd3819e7d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 6, "sha256": "07e5bd5ce0e8e58243cbfa73a5929e890b03a3b41f1860676875c8f290e7efb4"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 7, "sha256": "75c5842961ee2d499b14c6bd6797e83a2c28b70f15507ef9a5a92df07b16f3a2"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 8, "sha256": "0321a650a87252f41b09d551c08d7a228b22c2f9b1cff06c1099c1f1bb0c3add"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 9, "sha256": "45bbb157a3088b687c05b893bd5db4d5e2f87160ecbf63fe6b8e1f09a6d2c06d"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 10, "sha256": "f229231a49894ee2309b1b102b37ccca3dcdfe6aa873b09564151b59a242ae17"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 11, "sha256": "3008bf9ebe4941a83d0121d9aa6921c6ab056bbc09828a6014b51485c2db7c32"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 12, "sha256": "6050bb4a11fd9476b728245c71e7b4617a1934404c30e90e2e47b1df2bafc696"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 13, "sha256": "b5ea5fde5c2adb27a577748897cdb2f8cb34a9b75430dc98295a96d21666fdc7"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 14, "sha256": "0ae748545697e545ba34c0d9167e7db68b7d6477152ed05561c7f44220034fd5"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 15, "sha256": "d9bfafd6842d3c9b3f3e3a99edbe3d8e2ca987a94f9874da8898ea669abcdca1"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 16, "sha256": "2aa33ecc9d23f185dcae93063d5db364decd468380162ceb27a5b471f991c024"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 17, "sha256": "26a3e4ea4ad274e477aaf6e6ab2195e05b41231af7a50db8efcb575e91b729ce"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 18, "sha256": "a1554c9746e3046a23ac6499fcf353f0cffe5970676bc5d3f2069067a8e2f857"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 19, "sha256": "12811da879ef3c66d69967846e9c08d21d5164269cfe14425805b55993e90014"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 20, "sha256": "577d9631488f9a0ab96a6d7abff4a408981a2b75e6dfd5ffd8f0c95a30be7da3"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 21, "sha256": "a3c7d3606d2720d201fbfe4a946b9ee33ed60ef2b0f72e63ac3d5e63c03f606e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 22, "sha256": "ea4cf80a99d9d571887d7d74d1da152112e1c025c11a6acf8499fab6f2cfdc1a"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 23, "sha256": "ba0a906be15eadf66dda757d883e7150dbec0fe960cfb79b92b978284172ce48"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 24, "sha256": "332699a9db11a0e9d8c1e1445605893faa45fc9e5bcd5e6d7745f34384a66650"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 25, "sha256": "0e590f7fedb287a9656531e92e318d227fa0e7933067aeb3bdb1c39f39bd22e9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 26, "sha256": "ba99490b9698df11ab7d984e8fc91b21e8d5842fbf455552261a1979eecbfef9"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 27, "sha256": "8bb95e80e2f81b031d6abdede0b4be7390a0a3480dbc9fce6214046320f8c5cf"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 28, "sha256": "4098bde2e6c08e2efed24c9cb175e621af2ac50876b4bc40aba56ec40de66058"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 29, "sha256": "335e02b870c8c136999ea4def201c66fb9fca0939cb02824b7075f3110986c0e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 30, "sha256": "8f5552f053b3fcff9a87489891b2e09f911739650f1f1ced3e3961ceac04c218"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 31, "sha256": "8422fb6ab20b8c10c8ccaffb3199882205d7b0e5b8d38d686984b820d701349e"}`
- L0.2: event cannot join unique task/member/planned activity；`{"task_id": "t0001", "path": "study/workspaces/t0001/execution.log", "line": 32, "sha256": "557d6dab564ad19f37925d90fa7de2f0ffd5240c4244c6449c750a30a367ceb2"}`
- L0.8: observable release differs from captured feature projection；`{"missing": 32, "extra_or_conflicting": 32}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

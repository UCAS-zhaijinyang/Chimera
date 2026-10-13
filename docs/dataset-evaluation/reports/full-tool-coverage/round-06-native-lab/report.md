# 第一阶段评测：None

状态：**FAIL**。范围：workflow application simulation; no real system/network/email claim。

| 指标 | 分子 / 分母 | 数值 | 状态 |
|---|---|---|---|
| L0.1 核心字段可用率 | 344 / 344 | 1.0 | PASS |
| L0.2 主键关联完整性 | 344 / 344 | 1.0 | PASS |
| L0.3 文件与事件守恒 | 15 / 15 | 1.0 | PASS |
| L0.4 产物血缘完整性 | 0 / 71 | 0.0 | FAIL |
| L0.5 因果与时间约束 | 15 / 15 | 0 | PASS |
| L0.6 标签可追溯性 | 15 / 15 | 1.0 | PASS |
| L0.7 跨采集源对齐 | 71 / 71 | 1.0 | PASS |
| L0.8 发布完整性/泄漏扫描 | 15 / 15 | 0 | PASS |

采集能力：`{"application": "MEASURED", "system": "NOT_MEASURED", "network": "NOT_MEASURED", "real_email": "NOT_MEASURED"}`。

## 失败与证据

- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-00", "artifact_id": "7463f53086f0"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-00", "artifact_id": "533d436f56c5"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-00", "artifact_id": "e47f59ff5510"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-00", "artifact_id": "c8877ba3945e"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-01", "artifact_id": "4cefbadc85da"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-01", "artifact_id": "88cedef4df00"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-01", "artifact_id": "c9ee4ad7776f"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-01", "artifact_id": "1a356dbc617a"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-02", "artifact_id": "17b92206e1d4"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-02", "artifact_id": "c5b4f13217d4"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-02", "artifact_id": "fb020c41a123"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-02", "artifact_id": "9d0426eb9e02"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-03", "artifact_id": "91e50cf5d06e"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-03", "artifact_id": "c0530633efb7"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-03", "artifact_id": "153549ee6c17"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-04", "artifact_id": "2a5065933feb"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-04", "artifact_id": "473caba75590"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-04", "artifact_id": "07cbde8a38c4"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-04", "artifact_id": "e647f5893cfa"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-05", "artifact_id": "1dbd0e6f59cd"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-05", "artifact_id": "d33af005ffab"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-05", "artifact_id": "bba5e5d7dafb"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-05", "artifact_id": "ed09906ee91e"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-05", "artifact_id": "1362f6e4b9c1"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-06", "artifact_id": "0c26b6574858"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-06", "artifact_id": "6669e26c7959"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-06", "artifact_id": "f4a915aa46e2"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-06", "artifact_id": "6efb3071ec71"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-06", "artifact_id": "712a9e070cfa"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-06", "artifact_id": "66efda76054a"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-06", "artifact_id": "b79f71ea3ab4"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-07", "artifact_id": "636b90a4e977"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-07", "artifact_id": "906886ed3f2d"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-07", "artifact_id": "520e841d1cce"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-07", "artifact_id": "e1722b4581ed"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-08", "artifact_id": "70ff21428c3b"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-08", "artifact_id": "3a07024fcf36"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-08", "artifact_id": "9d05a7b34f90"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-08", "artifact_id": "296b0fdbccf4"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-08", "artifact_id": "b19a1326c2d8"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-09", "artifact_id": "254580ec60c5"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-09", "artifact_id": "67f0be30905d"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-09", "artifact_id": "ed1e1ca9de2d"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-09", "artifact_id": "0ae82717e272"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-10", "artifact_id": "7e40bf670c78"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-10", "artifact_id": "afc09bee753d"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-10", "artifact_id": "ed53fe6e44f0"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-10", "artifact_id": "c65b87856bbb"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-11", "artifact_id": "fbb4b6b9f864"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-11", "artifact_id": "a6131c2f8619"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-11", "artifact_id": "33f0bb882a66"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-11", "artifact_id": "9e94d531188b"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-12", "artifact_id": "490d39a7c548"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-12", "artifact_id": "8cb6947ae375"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-12", "artifact_id": "c808a69940eb"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-12", "artifact_id": "44beea7d3ac6"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-12", "artifact_id": "c2cc6dd3a147"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-12", "artifact_id": "540c0cce046d"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "9a8e055fbdef"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "de156353d394"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "0a53f84dd4c4"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "425fbd1155a5"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "a8fe08fa0e0f"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "89dc8f19f899"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "3a3f7b8f25ae"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-13", "artifact_id": "cdb1ede1ae8a"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-14", "artifact_id": "f565aeeb25db"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-14", "artifact_id": "a05888e07dee"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-14", "artifact_id": "5c2fde639aa0"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-14", "artifact_id": "9a720ba277af"}`
- L0.4: tool contract forbids unexplained root；`{"task_id": "case-0-14", "artifact_id": "af38801f6f78"}`

完整分母、原始字节来源、解析拒绝和事件/产物索引见 report.json；原始输入见 evidence.tar.gz。

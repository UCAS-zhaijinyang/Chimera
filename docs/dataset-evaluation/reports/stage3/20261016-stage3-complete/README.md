# 第三阶段完整评测报告：O/N 数据集检测效用对比

- 运行 ID：`20261016-161015`
- 状态：**COMPLETE_WITH_NOT_MEASURED_ITEMS**
- 数据：`stage2_runs/stage2-full-from-scratch-20261015`（复用第二阶段，不重新生成）

## 1. 评测问题与冻结协议

比较在相同 held-out attack episode、相同目标域、相同可观察字段和相同训练规则下，使用 O 训练或 N 训练对内部威胁的检测效用。主指标为 AP 和固定 10% 正常员工日审查预算下的 Recall；F1、MCC、FPR、每千正常员工日告警数和 episode Recall 为辅助指标。

目标 episode 为 `gen_attack_10`。O/N 均按攻击日期切分，训练与 target key 不重叠；target 内保留原始阳性比例，不进行测试集重采样。

## 2. 数据规模

| 域 | 员工日行数 | 阳性员工日 | 攻击 episode |
|---|---:|---:|---:|
| O | 240 | 3 | 3 |
| N | 240 | 9 | 3 |

第三阶段当前只有 3 个攻击 campaign；held-out target 每个域只有 1 个阳性 episode，因此所有差值区间都应按 `INCONCLUSIVE` 解读，不能把事件数量当成独立攻击样本数。

## 3. 检测器来源与运行状态

- RBF-SVM、Temporal CNN、GCN：来源为作者 [B-CITD GitHub](https://github.com/Wayne-on-the-road/B-CITD)，commit `c2fed9cc69ee7947da090f17042ccb5d1cd84b36`。原脚本绑定 CERT4.2 文件路径和 PyTorch/PyG；本报告运行了明确标注的 O/N 适配器，不能称为原仓库 CERT 复现实验。
- DS-IID：论文声称使用公开实现，但在本次可审计检索中没有取得可核验的作者仓库，标记 `NOT_MEASURED`。

## 4. 交叉域矩阵与指标

| 方法 | 训练源 | target | AP | ROC-AUC | Recall@10% | F1 | FPR | episode Recall | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| rbf_svm | O | O | 1.0000 | 1.0000 | 1.0000 | 0.2222 | 0.6364 | 1.0000 | MEASURED |
| rbf_svm | O | N | 1.0000 | 1.0000 | 1.0000 | 0.1875 | 0.7879 | 1.0000 | MEASURED |
| rbf_svm | N | O | 1.0000 | 1.0000 | 1.0000 | 0.1538 | 1.0000 | 1.0000 | MEASURED |
| rbf_svm | N | N | 1.0000 | 1.0000 | 1.0000 | 0.2727 | 0.4848 | 1.0000 | MEASURED |
| temporal_cnn_adapter | O | O | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.0909 | 1.0000 | MEASURED |
| temporal_cnn_adapter | O | N | 1.0000 | 1.0000 | 1.0000 | 0.6000 | 0.1212 | 1.0000 | MEASURED |
| temporal_cnn_adapter | N | O | 1.0000 | 1.0000 | 1.0000 | 0.1667 | 0.9091 | 1.0000 | MEASURED |
| temporal_cnn_adapter | N | N | 1.0000 | 1.0000 | 1.0000 | 0.6000 | 0.1212 | 1.0000 | MEASURED |
| gcn_adapter | O | O | 1.0000 | 1.0000 | 1.0000 | 0.5000 | 0.1818 | 1.0000 | MEASURED |
| gcn_adapter | O | N | 0.7101 | 0.7980 | 0.6667 | 0.4444 | 0.1212 | 1.0000 | MEASURED |
| gcn_adapter | N | O | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | MEASURED |
| gcn_adapter | N | N | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 | MEASURED |

## 5. O/N 配对差值

| 方法 | target | ΔAP（N−O） | 95% CI |
|---|---|---:|---|
| rbf_svm | O | 0.0 | [0.0, 0.0] |
| ↳ Recall@10% | O | 0.0 | [0.0, 0.0] |
| rbf_svm | N | 0.0 | [0.0, 0.0] |
| ↳ Recall@10% | N | 0.0 | [0.0, 0.0] |
| temporal_cnn_adapter | O | 0.0 | [0.0, 0.0] |
| ↳ Recall@10% | O | 0.0 | [0.0, 0.0] |
| temporal_cnn_adapter | N | 0.0 | [0.0, 0.0] |
| ↳ Recall@10% | N | 0.0 | [0.0, 0.0] |
| gcn_adapter | O | 0.0 | [0.0, 0.0] |
| ↳ Recall@10% | O | 0.0 | [0.0, 0.0] |
| gcn_adapter | N | 0.28985507246376807 | [0.0, 0.9565217391304348] |
| ↳ Recall@10% | N | 0.33333333333333337 | [0.0, 1.0] |

## 6. 泄漏审计、负控制与稳健性

- 数据字段审计：PASS_WITH_WARNINGS；明确攻击字段未进入特征，训练/target key 不重叠。
- 默认特征会剥离 `Attack`、`AttackSteps`、`Canonical attack requirements` 等显式元数据；攻击行为文本仍作为可观察内容保留。
- 已执行随机训练标签、移除文本和删去每天最后一个活动的负控制/稳健性实验；完整逐组合结果保存在 `report.json` 的 `controls`。小样本下随机标签 AP 可能偶然偏高，因此仅作为诊断。
- metadata-only 和近重复审计仍为 `NOT_MEASURED`，不能用主结果代替。

| 控制类型 | 解释 |
|---|---|
| randomized_train_labels | 训练标签置乱；若仍高分提示捷径或样本量不足 |
| remove_text | 仅保留数值日程特征；衡量文本内容贡献 |
| omit_last_activity | 每个员工日删去最后一条观察；衡量缺失事件稳健性 |

## 7. 成本与可复核产物

- 新增 LLM API 成本：$0.00；本阶段只训练本地检测器。
- 产物包括 `split_manifest.json`、`scores.jsonl`、`detector_runs.json`、`leakage_audit.json`、`runtime_cost.json` 和 `validation.json`；manifest 记录 O/N 输入文件 SHA-256。
- 第三阶段专用测试 3/3 通过；全仓库测试的 64 项失败来自 Python 3.13 与项目锁定的 camel-ai 版本不兼容，详见 `validation.json`。

## 8. 结论边界

本次运行已经完成可运行适配器的真实 O/N 训练、交叉域预测、随机标签/删模态控制，并保留逐样本分数、split manifest、检测器来源、泄漏审计和运行账本。由于 target 阳性 episode 极少，结果只能作为协议和工程链路的完成证据，不能据此宣称 N 一定优于 O。DS-IID、官方 PyTorch/PyG 原始脚本复现、metadata-only/近重复审计和外部 CERT/TWOS target 仍是明确未测项。

详细 JSON、逐样本分数和 manifest 见同目录文件。

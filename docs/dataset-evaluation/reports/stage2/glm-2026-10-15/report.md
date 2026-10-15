# 第二阶段 GLM-5.3 评测报告（从零生成）

状态：**PARTIAL_EXECUTED**。

本次已清理可再生数据目录，并从空目录生成当前框架的 12 名员工、20 个工作日、1 个独立运行的正常日程，再生成 B（兼容旧式单日注入）和 C（LLM 多日注入）两组攻击调度。原始 Chimera O 数据、实际员工执行和盲评尚未形成，因此不宣称完整 O/B/C 结论。

## 运行范围

- 请求模型：GLM-5.3；服务端实际可用模型：GLM-5.3-Flash；请求 GLM-5.3 返回 HTTP 503。
- B/C：每组 240 个员工日；每组 3 个攻击 episode；C 的 LLM 选择了 3 天/episode，B 固定单日。
- Q4 事件计数：B 正常 892、攻击 9；C 正常 1123、攻击 9。
- 模型请求数：21；prompt tokens：35,618；completion tokens：47,743；总 tokens：83,361。服务端未提供可核验价格，现金成本记为 UNKNOWN。
- 详细原始产物：`study_manifest.json`、`model_usage.jsonl`、`failures.json`、`events.jsonl`、`campaigns.json`。

## 七项任务

| 任务 | 状态 | 结果 |
|---|---|---|
| Q1 计划落实 | NOT_MEASURED | 未执行员工行为，未接入独立 oracle |
| Q2 业务成果 | NOT_MEASURED | 未执行报告/开发/修复成果验收 |
| Q3 交接连续性 | NOT_MEASURED | 没有真实产物生产与消费事件 |
| Q4 分布覆盖 | MEASURED | 两组各 240 员工日；攻击事件和失败记录已保存 |
| Q5 攻击 episode | MEASURED | 6/6 campaign 完成，C 每个 episode 由 LLM 选择 3 个日期 |
| Q6 盲评/judge | NOT_MEASURED | 未产生人工评分包 |
| Q7 成本/范围 | MEASURED | 逐请求 token trace 已保存，价格未知 |

## 攻击完整性

每个 campaign 的 canonical attack steps 都按顺序覆盖；C 组未选日期保留正常/修改 hash 等价证明（51/51）。同一 episode 的多天、多步和多次工具调用没有当成独立样本。

## 对比结论边界

- `B−O` 和 `C−O`：`NOT_MEASURED`，因为没有合法的原始 Chimera 数据来源。
- `C−B`：只能作为当前框架两种攻击注入策略的结构性差异；不能解释为相对原始 Chimera 的改进。
- Q1/Q2/Q3/Q6 的缺失不能用 Q4/Q5 的通过替代；报告保留 `NOT_MEASURED`。

## 产物

运行根目录：`stage2_runs/formal/measurements`。详细 JSON：`report.json`；原始事件：`events.jsonl`；攻击真值/计划：`campaigns.json`；失败：`failures.json`；模型用量：`model_usage.jsonl`。

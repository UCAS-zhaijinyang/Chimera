# 第一阶段测评交付：数据可信

当前workflow应用仿真的L0.1–L0.8通过；系统、网络、真实邮件与跨任务协作仍为NOT_MEASURED。这里验证生成、采集、关联、血缘、标签和发布契约，不能据此宣称业务成果正确、行为真实或威胁检测有效。

最终证据：

- [黄金任务](round-07-golden-final/report.md)：30模板×3重复，90条脚本模型边界轨迹，2,046事件、414产物，全部核心指标PASS。文件工具真实执行，但这不是LLM质量实验。
- [多日运行](round-09-multiday-final/report.md)：3场景×2独立run×5工作日×12成员×2任务＝720任务、360员工日；16,600事件、3,372产物，全部核心指标PASS。仅workflow条件，没有宣称原比较方案的720员工日双条件先导完成。
- [故障挑战](round-13-challenges-expanded/summary.json)：25类×3工作流＝75突变全部检出，3正常对照误报0。突变单独报告FAIL，未混入自然质量均值；这是已知故障覆盖，不是对所有未来故障的统计保证。
- [真实DeepSeek汇总](round-17-live-aggregate/report.md)：30模板×3重复、90任务，958事件、139产物；222请求全部结算，210返回usage，12次有TLS握手失败且请求未发送证据。8项核心指标PASS。
- [回归与独立审查](verification/independent-review.md)：127项pytest通过；5项上游CAMEL/Pydantic弃用警告；7项Important审查意见全部复现并修复，无Minor遗留。

## 真实API结果如何解释

最终90任务终态为 `{'failed': 46, 'early_terminated': 37, 'completed': 7}`；其中失败与提前结束均保留。L0通过表示这些状态记录正确，不表示90个业务任务成功。18个计划攻击episode的执行状态为 `{'unknown': 15, 'blocked': 3}`；未知没有补成阴性，阳性只按真实工具调用/拒绝证据形成。

variants6–8：真实付费请求返回后注入已知模型边界故障，用于验证失败/拒绝采集，不作为自然攻击能力证据。variant9：只给定仿真目标，按实际动作记录；无匹配证据就unknown。独立私有真值和可观测release/events.jsonl分开，release按字段allowlist导出，并与原始事件投影逐行多重集核对。

长运行中出现TLS错误与预算停止，round06另发现code_edit覆盖历史artifact。全部失败报告保留；修复写入保护并转为短批次复测。最终汇总保留每个选定批次的全部任务，没有按任务成功筛选；早期/替换批次的失败与费用仍在总账。最终汇总不是额外90次生成，而是10个9任务批次的只读合并。

## 指标与验收

| 指标 | 最终真实API分子/分母或冲突数 | 状态 |
|---|---|---|
| L0.1 核心字段可用率 | 958/958 | PASS |
| L0.2 主键关联完整性 | 958/958 | PASS |
| L0.3 文件与事件守恒 | 90/90 | PASS |
| L0.4 产物血缘完整性 | 64/64 | PASS |
| L0.5 因果与时间约束 | 0 | PASS |
| L0.6 标签可追溯性 | 3/3 | PASS |
| L0.7 跨采集源对齐 | 139/139 | PASS |
| L0.8 发布完整性/泄漏扫描 | 0 | PASS |

L0.4另外核对所有139产物的hash、version、producer与必需输入契约；L0.5的0是硬因果冲突数。simulation_time为任务起点+事件逻辑顺序，不是实测业务耗时。L0.7是工具事件与本地捕获产物的应用对齐，不是pcap/scap证据。

L0.8本轮输入来自固定虚构fixture和保留域名，没有导入真实员工profiles或企业日志。凭证候选扫描覆盖原始日志、产物和release；contact候选按保留域名复核，并扫描显式标签字段/发布路径。执行环境路径保留在诊断证据中，不宣称完整匿名化、通用PII识别或差分隐私；真实业务数据将需要额外人工敏感信息审核。

## 费用

全部付费调用使用DeepSeek-flash、thinking disabled、输出上限4,096；保存实际returned model和usage。官方峰值价：输入未命中$0.30/M、缓存命中$0.006/M、输出$1.20/M，来源[DeepSeek官方价格](https://api-docs.deepseek.com/quick_start/pricing)，查询2026-10-12。离线回归/挑战没有模型API费。

最终90任务的已知token峰值费用为 **$0.055699368**。包含初始验证、失败轮次、整批复测与诊断后的全部已知用量费用为 **$0.135735792**。详见[总账](verification/cost-summary.json)。

另有91个历史失败请求及1个诊断未返回usage，当时未保存握手堆栈，不能追认精确账单。按每次完整1M输入context的极保守保留额，上界 **$28.052198**；该值是风险上界，不是声称实际扣款。后续12次失败保存了handshake堆栈，确认HTTP请求未发送，生成费0。实际账户扣款须以供应商账单核对。

## 每轮原始报告

每轮report.json含逐项分母、失败与事件/产物索引；execution.json含commit、dirty状态、diff hash及源文件hash；evidence.tar.gz保留完整study输入。旧轮次按当时检查器评估，不回写成新版本结果。故障挑战的每个突变都有独立报告和原始证据。

| 目录 | 状态/范围 | 任务 | 事件 | 产物 | 已知usage请求 |
|---|---|---:|---:|---:|---:|
| [round-01-baseline](round-01-baseline/report.md) | FAIL | 90 | 264 | 174 | 0 |
| [round-02-repaired-golden](round-02-repaired-golden/report.md) | PASS | 90 | 2046 | 414 | 0 |
| [round-03-deepseek-compatibility](round-03-deepseek-compatibility/report.md) | PASS | 1 | 24 | 5 | 6 |
| [round-05-multiday](round-05-multiday/report.md) | PASS | 720 | 16600 | 3372 | 0 |
| [round-06-deepseek-golden](round-06-deepseek-golden/report.md) | FAIL | 90 | 846 | 117 | 161 |
| [round-07-golden-final](round-07-golden-final/report.md) | PASS | 90 | 2046 | 414 | 0 |
| [round-09-multiday-final](round-09-multiday-final/report.md) | PASS | 720 | 16600 | 3372 | 0 |
| [round-10-deepseek-final](round-10-deepseek-final/report.md) | PASS / campaign FAIL / 仅错误记录，无模型产物证据 | 90 | 360 | 0 | 0 |
| [round-11-serial-check](round-11-serial-check/report.md) | PASS | 1 | 14 | 2 | 3 |
| [round-12-deepseek-serial-final](round-12-deepseek-serial-final/report.md) | PASS / campaign FAIL | 90 | 632 | 61 | 89 |
| [round-14-batched-deepseek/variant-0](round-14-batched-deepseek/variant-0/report.md) | PASS | 9 | 104 | 16 | 25 |
| [round-14-batched-deepseek/variant-1](round-14-batched-deepseek/variant-1/report.md) | PASS | 9 | 100 | 15 | 24 |
| [round-14-batched-deepseek/variant-2](round-14-batched-deepseek/variant-2/report.md) | PASS | 9 | 100 | 15 | 24 |
| [round-14-batched-deepseek/variant-3](round-14-batched-deepseek/variant-3/report.md) | PASS | 9 | 90 | 12 | 21 |
| [round-14-batched-deepseek/variant-4](round-14-batched-deepseek/variant-4/report.md) | PASS | 9 | 110 | 18 | 26 |
| [round-14-batched-deepseek/variant-5](round-14-batched-deepseek/variant-5/report.md) | PASS / 仅错误记录，无模型产物证据 | 9 | 36 | 0 | 0 |
| [round-14-batched-deepseek/variant-6](round-14-batched-deepseek/variant-6/report.md) | PASS / 仅错误记录，无模型产物证据 | 9 | 36 | 0 | 0 |
| [round-14-batched-deepseek/variant-7](round-14-batched-deepseek/variant-7/report.md) | PASS / 仅错误记录，无模型产物证据 | 9 | 36 | 0 | 0 |
| [round-15-batch-retries/variant-5](round-15-batch-retries/variant-5/report.md) | PASS | 9 | 120 | 20 | 29 |
| [round-15-batch-retries/variant-6](round-15-batch-retries/variant-6/report.md) | PASS | 9 | 90 | 9 | 18 |
| [round-15-batch-retries/variant-7](round-15-batch-retries/variant-7/report.md) | PASS | 9 | 138 | 27 | 30 |
| [round-15-batch-retries/variant-8](round-15-batch-retries/variant-8/report.md) | PASS | 9 | 42 | 0 | 3 |
| [round-15-batch-retries/variant-9](round-15-batch-retries/variant-9/report.md) | PASS | 9 | 64 | 7 | 10 |
| [round-16-main-thread-diagnostic](round-16-main-thread-diagnostic/report.md) | PASS | 1 | 24 | 5 | 6 |
| [round-17-live-aggregate](round-17-live-aggregate/report.md) | PASS | 90 | 958 | 139 | 210 |

[round-04-fault-challenges故障汇总](round-04-fault-challenges/summary.json)，各子目录保留全部正常/突变报告。

[round-08-challenges-final故障汇总](round-08-challenges-final/summary.json)，各子目录保留全部正常/突变报告。

[round-13-challenges-expanded故障汇总](round-13-challenges-expanded/summary.json)，各子目录保留全部正常/突变报告。

## 重现

解压某轮evidence.tar.gz到临时目录，再用当前代码运行 `python scripts/evaluate_dataset_trust.py --study <解压目录>/study --report <新的空报告目录>`。历史baseline因源契约未满足仍应FAIL；新契约报告可按当轮source_sha256核对对应代码版本。

运行脚本：`scripts/run_dataset_trust_campaign.py`支持offline/pilot/faults/live；live只从--key-file读取凭证，研究结果不含凭证。任务前缀确保批次身份互不冲突，`scripts/combine_trust_studies.py`拒绝冲突且不删除失败任务。started ledger先fsync，终态单独追加；未结算started必须按reserve计入，不能当零费。

## 本轮裁定及后续范围

- 缺少真实采集能力继续NOT_MEASURED；代价是本轮无法证明全模态企业数据可信。
- 已知故障注入独立统计；代价是这些样本不能证明自然攻击能力或威胁检测质量。
- TLS问题采用短批次复测并保留旧轮次；代价是增加请求和未知费用核算，而没有降低核心通过条件。
- 业务语义、真实审批、真实性、统计比较和外部检测效用留第二/三阶段；代价是第一阶段PASS不能代替这些证据。

没有遗留Minor审查问题；凭证临时文件在推送前清理。

# 正常业务执行修复与复测报告

按测试目的阅读完整结论，见[第一阶段总报告](../stage1/README.md)；本页保留执行修复根因、逐轮复测和费用细节。

**最终验收通过：明确规格的54个正常任务，编排完成54/54、独立业务正确54/54；原描述的54个正常任务，编排完成54/54。** 原描述缺少可判定的功能/缺陷规格，因此该组业务语义仍为NOT_MEASURED，不能用流程完成代替业务成功。

本轮修复的是本地workflow应用仿真的已知执行与验收问题。没有声称整个框架永远不存在缺陷，也没有验证真实企业邮件、系统/网络采集、跨任务协作或威胁检测效用。

## 最终证据与通过条件

| 检查 | 最终结果 | 证据 |
|---|---|---|
| 原模糊任务同描述复测 | 54/54完成，三个流程各18/18；业务语义未测 | [round24](round-24-original-description-replay/execution-report.md) |
| 明确规格真实DeepSeek完整队列 | 正常54/54完成且业务通过，三个流程各18/18 | [round23业务报告](round-23-live-final-confirmation/business-report.md) |
| 最终独立检查器重新验收完整原始证据 | 正常54/54业务通过；任务/结果清单严格一一对应 | [round27](round-27-final-independent-acceptance/business-report.md) |
| 故障/拒绝采集 | 27/27预先指定受控错误按预期失败或拒绝并保留 | [逐任务检查](round-27-final-independent-acceptance/round23-business.json) |
| L0.1–L0.8 | 最终90任务2,366事件、434产物，全部通过 | [L0报告](round-27-final-independent-acceptance/report.md) |
| 已知故障突变 | 25类×3流程，75/75检出；3正常对照误报0 | [round26](round-26-challenges-final/summary.json) |
| 全量软件回归 | 150通过；5项上游CAMEL/Pydantic弃用警告 | [提交前完整日志](verification/final-suite.log) |

最终round23的90任务为：正常54个全部completed；rejection18个全部failed；attack18个中9个completed、9个failed。合计63 completed、27 failed、0 early_terminated。其中27个失败均为variants6–8的受控测试，按预先规则独立统计；没有删掉失败轨迹。variant9是给定仿真目标的模拟攻击观察，不能据此宣称自然攻击或威胁检测能力。

前三个加强业务完整队列round12、14、19也分别达到54/54正常业务通过；round14增加多文件要求后，经最终更严格检查器重新检查仍通过。它们属于不同修复版本，不合并为同一最终版本的成功率或独立统计置信度。round21、27是同一原始证据的只读复验，没有重新调用API、没有额外独立样本。

## 修复了什么

1. **流程上下文没有到达模型。** 旧API仅发送messages/tools，Python request中的state/workflow_id未传输。模型误以为后续工具不可用。现在系统消息说明全流程、当前阶段和后续工具逐步开放；DeepSeek非thinking模式支持named/required tool_choice，客户端实际传递选择约束。
2. **模型看不到实际业务数值。** 工具此前只返回不透明ID、证据路径和状态，报告可能没有数值。现在返回实际payload，并明确证据路径只读、业务文件路径与任务工作目录，保持原写入保护。
3. **多工具调用和错误立即结束整条任务。** 每轮只执行第一条调用，其余逐条记录拒绝，不重放已提交副作用；错误返回当前状态、工具与实际失败输出，最多两次纠正机会/阶段，第三次错误终止；全任务最多24轮。所有失败/拒绝仍在原始日志中。
4. **代码只能写一个文件、不能在失败后修正。** implemented/fixed允许继续code_edit，完成辅助文件与测试文件并修正失败代码后再test_run；只有成功测试推进状态。
5. **执行目录和可用构建工具不明确。** 模型将解释器路径误认成任务目录，并尝试未安装的pip/build/setuptools。现在提供实际cwd、可用模块和默认构建命令。默认本地build是Python字节码编译，不是wheel打包，也不能代替功能测试。
6. **缺陷复现只有固定标志。** 有明确fixture时实际执行失败检查，保存AssertionError/returncode；未配置复现输入时reproduced为null、业务状态not_measured，不能称作真实复现。
7. **网络连接等待过长。** 部分DNS地址TCP连接超时；每地址连接最多5秒，保留90秒TLS/响应等待。地址回退发生在HTTP提交前，不重试已提交生成请求，TLS验证未关闭。
8. **评测器可能误报或误判通过。** PII检查解码JSON/NDJSON字符串，避免将转义换行后的装饰器识别成邮箱。独立业务检查验证数值、真实副本、模拟投递、隐藏代码行为、辅助函数与调用依赖、非空unittest及错误行为突变；导入错误不能算检出业务错误。任务/结果清单必须一一对应，漏项/重复/未知ID均FAIL。命令行将记录、编排、业务验收分开，正常执行失败不能因L0通过而获得整轮PASS。

## 独立业务检查如何避免自证

报告任务包含重复周、零计数、不同计数的6种数据输入。检查器按预先固定输入重新求和，直接读reports/out.json与shared/out.json，核对全部键、整数值、字节副本及模拟消息附件/收件人/主题。模型自述和router终态不能代替这些检查。

功能/缺陷任务有求和、差、积、最大、最小、均值6种规格。隐藏测试的期望值独立手工确定，包含负数、零、分数和另一组输入，不发送给模型；从原始源码复制到新临时目录并在独立Python进程运行。缺陷任务同时检查修改前实际失败证据。多文件功能还独立测试mean_values、替换helper验证主函数调用关系、执行真实unittest，并替换compute证明测试会产生断言失败且无运行错误。

检查器不使用运行时的成功标志或产物读取器作为业务真值。它面向指定的普通业务fixture，不声称抵抗恶意代码对检查器的规避，不替代更广泛的第二阶段真实性/业务分布评测。

## 全部真实API轮次与失败保留

| 轮次 | 任务 | 正常编排完成 | 独立业务 | 解释 |
|---|---:|---:|---|---|
| [历史round00](round-00-historical-audit/report.md) | 旧90 | 6/54 | 未测 | 原真实任务失败问题；重新审计为FAIL |
| [round03](round-03-live-probe/business-report.md) | 3 | 2/3 | 2/3，FAIL | 同次响应重复test_run |
| [round06](round-06-live-probe/business-report.md) | 3 | 2/3 | 2/3，FAIL | 后续回合继续调用旧阶段工具 |
| [round09](round-09-live-probe/business-report.md) | 3 | 3/3 | 3/3 | 小探针通过，不当完整验收 |
| [round11](round-11-original-description-replay/report.md) | 54 | 30/54 | 未测 | 原描述，多文件强制推进与PII误报；执行FAIL |
| [round12](round-12-live-full/business-report.md) | 90 | 54/54 | 54/54 | 首个完整明确规格队列 |
| [round14](round-14-live-full-confirmation/business-report.md) | 90 | 54/54 | 54/54 | 加入多文件；后经加强检查器复验 |
| [round15](round-15-original-description-replay/report.md) | 54 | 52/54 | 未测 | 原描述，错误cd与NDJSON PII误报；执行FAIL |
| [round19](round-19-live-final/business-report.md) | 90 | 54/54 | 54/54 | 更严格业务检查，完整队列 |
| [round20](round-20-original-description-replay/report.md) | 54 | 50/54 | 未测 | 原描述，4条未安装打包工具错误；执行FAIL，即使L0 PASS |
| [round23](round-23-live-final-confirmation/business-report.md) | 90 | 54/54 | 54/54 | 最终生成代码版本完整队列，重新独立验收 |
| [round24](round-24-original-description-replay/execution-report.md) | 54 | 54/54 | 未测 | 最终原描述编排可靠性复测 |

其余目录保存离线回归RED/GREEN、离线完整队列、故障挑战和只读重新验收。每个live目录含report.json/md、execution.json、evidence.tar.gz和campaign_acceptance.json；加强任务另含逐任务business-report，最终runner另含逐任务execution-report。旧报告按当时契约保留，特别是旧命令只以L0裁定时的PASS没有回写；本表明确执行失败，不让旧L0 PASS掩盖失败。

最早两个探针运行期间有修复源码，报告write-time hash不能当启动源码hash，诊断说明保留于diagnosis.json。后续完整队列启动快照runner-start.json随证据保存；最终round23/24生成运行时源码与最终生成代码一致。检查器随后只加强清单校验，最终评估版本/hash见round27/execution.json。启动快照现在在执行前独占创建并fsync，异常中断也保留。原始日志没有按成功筛选。

## 费用

本次修复共11个真实API轮次、**4,033次请求，全部结算，全部返回DeepSeek-flash并有可计价格usage**。已知token按官方峰值价估算总计 **$2.659028472**，未知usage保留额0。包含失败探针、原描述失败复测及全部加强队列，不只统计最终成功轮。最终round23为$0.416550984，round24为$0.484303644，两组最终生成合计$0.900854628。

这是供应商usage的token估算，不是账户发票；与之前第一阶段的旧费用分开，不包含本轮离线计算和人工时间。重复证据复验没有重复计费。逐轮请求数、结算、model、token费用及archive hash见[费用总账](verification/cost-summary.json)。真实API凭证不进入代码或证据；推送前已删除临时凭证，并扫描所有新增/修改文件及174份压缩证据。6处匹配均逐一核验为预设故障挑战的固定假凭证，保留以维持测试证据；其余未发现凭证模式，详见[扫描审核](verification/credential-scan.json)，初始未分类扫描结果亦保留。

## 复现

离线完整业务队列：

```sh
PYTHONPATH=src .venv/bin/python scripts/run_dataset_trust_campaign.py --mode offline --business-checks --study /tmp/NEW-study --report /tmp/NEW-report
```

解压最终evidence.tar.gz后，运行L0评估和独立业务/执行评估：

```sh
PYTHONPATH=src .venv/bin/python scripts/evaluate_dataset_trust.py --study /tmp/EXTRACTED/study --report /tmp/NEW-recheck
PYTHONPATH=src .venv/bin/python -c "from evaluation.business import evaluate_business; print(evaluate_business('/tmp/EXTRACTED/study'))"
```

真实复测使用同一runner的`--mode live --business-checks --key-file <私有文件>`，新study/report路径不可覆盖。`--normal-only`原描述队列不启用业务fixture，独立业务必须保持NOT_MEASURED。真实邮件/审批继续是仿真记录；真正的数据集效用和威胁检测还要完成后续阶段。

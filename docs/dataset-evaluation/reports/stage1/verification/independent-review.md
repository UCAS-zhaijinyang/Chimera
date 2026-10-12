# 独立只读审查与修复

2026-10-12，fresh-context reviewer，基线3523ab0至67f16da及未提交修改。审查没有读取API凭证、调用真实API或改动工作树。结论为With fixes；无Critical/Minor，7项Important。

| 问题 | 原表现 | 修复/验证 |
|---|---|---|
| 畸形输入 | tasks=[null]、字符串event_seq、inputs=null使评测器崩溃 | 结构/type检查；保留FAIL；`test_malformed_inputs_return_detailed_failure_instead_of_crash` |
| 任务边界/phase/day | terminal之后仍有调用、事件phase/day错误仍PASS | 检查任务时间边界、事件与task/plan相等；`test_review_false_pass_paths` |
| 隐藏必需依赖 | 删除data_transform输入、声明任意根可PASS | 独立工具输入/root契约；记录缺失也是FAIL；同上 |
| 发布文件守恒 | declared JSONL为空仍PASS | 独立可观测字段projection逐行多重集比较；同上 |
| manifest符号链接越界 | 读取study外的manifest可PASS | manifest本身resolve/within；`test_manifest_symlink_cannot_read_outside_study` |
| 非法usage退款 | negative output token使费用负数 | 非负整数/缓存和/模型上限校验，异常保留reserve；`test_invalid_usage_cannot_refund_reservation` |
| 请求起点不持久化 | paid request发送前ledger空，进程中断无记录 | started/reservation先append、flush、fsync；terminal独立追加；`test_request_start_is_durable_before_provider_call` |

另由真实API轮次发现模型code_edit覆盖历史artifact。`test_code_edit_cannot_overwrite_capture_evidence`锁定；业务写入禁止修改artifacts/manifest.jsonl/execution.log。

上述16项新增测试先RED（`review-red.log`：16 failed、2 passed），再GREEN（`review-green.log`：121 passed）；新增真实HTTP错误/超时/缺message测试后124 passed。实际报告目录拒绝覆写。没有重派第二轮审查。

审查未评价事项及执行方裁定：真实system/network/email无能力，继续NOT_MEASURED；业务正确性、代码语义、真实审批、真实性及外部企业效用留第二/三阶段；variants6–8是明确的模型边界故障注入，不宣称自然攻击；价格按本次已查询官方pricing核算；终验与完整回归由执行方实际运行；真实凭证未进入审查包。上述范围裁定的代价是不能据本轮声称全模态/业务质量/检测效用，下一阶段仍需独立证据。

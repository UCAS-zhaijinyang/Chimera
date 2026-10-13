# 独立审查与修复记录

修复前独立审查实测182项通过，仍发现9项Important问题，故未据测试数量宣布验收通过。审查为一次完整源码审查；修复逐项用回归测试及真实复测验证，没有重复派发审查者。

| 发现 | 修复 | 主要回归证据 |
|---|---|---|
| legacy FunctionTool不能接受原生关键字参数 | 具名kwargs闭包，保留schema | legacy_function_tool_objects_accept_their_native_arguments |
| 浏览器失败导致已提交点击重复 | 内部模型请求原位重试，不重启browse | browser_unsent_model_retry_keeps_already_committed_click，真实Chromium计数保持1 |
| 异步失败未观察终态仍可finish | 完成必须观察每个session终态，失败需修复或取消 | async_nonzero_exit_cannot_finish_without_recorded_terminal；async_success_requires_explicit_observation_then_can_finish |
| leader退出后后代继续写文件 | 跟踪和清理整个process group，排除僵尸进程 | cleanup_terminates_child_after_shell_leader_exits |
| Camel查找错误被当成功 | 按原生返回错误契约识别 | missing_native_file_is_recorded_as_failure；native_find_by_name_has_real_matches_and_missing_directory_errors |
| semantic和native业务cwd不同 | 业务root统一，artifact bus保持独立capture | semantic_and_native_tools_share_actual_business_root |
| 最终文件存在不能证明逐步执行 | 每步骤绑定实际成功call/参数/顺序，再与副作用相交；检查fixture源码hash | trace_oracle_rejects_a_skipped_step_even_if_later_step_makes_files |
| 日程只有编号，执行Activity丢how | 确定性把canonical how附入Activity；动态更新同样验证 | validated_schedule_binds_canonical_how_to_execution_text |
| 浏览器缺旧视觉/视频/键盘能力 | 截图、真实视频28帧、owning DeepSeek、Enter、ARIA/contenteditable、弹窗/回退 | browser_workflow完整回归；round-17真实API图像/时序视频检查 |

红→绿证据：review-red.log记录7项失败；additional-red.log记录日程文本与包导入突变检查失败；browser-red.log记录视觉/视频/Enter失败；popup-red.log与popup-green.log记录弹窗修复。async-red.log为异步终态首次反例。green.log为首批55项通过；full-suite.log为195项通过。最后完整测试以final-verification.log为准。

## 实验中追加诊断与实现决策

- Ruling：突变验收必须把src.main与main统一成同一个被验收候选。round-08的t0076已经写了有效的包导入测试，旧验收器只替换main，因模块别名误报失败；不降低“测试必须检出错误”的标准，修正验收目标。additional-red.log与test_multifile_mutation_handles_package_imports记录反例。成本/风险：若错误统一不相关模块会改变测试导入行为，因此保留空测试、绕过compute、无helper依赖等负例。
- Ruling：逐步骤命令比较允许且仅允许等价的`cd <同一固定business cwd> && <canonical command>`，也比较shell tokens以忽略无语义引号差异；不接受不同cwd、额外命令、任意wrapper或跳步。trace-cwd-red.log/green.log含正反例。成本/风险：解析不完整可能接受非等价命令，因此只允许有限白名单语法，仍要求fixture hash和实际副作用。
- Ruling：TLS发送前失败最多8次有退避重试，不占业务步骤额度。retry-budget-red.log验证原4次重试和业务额度共同导致错误终止。每次模型attempt必须成对关闭，费用按实际usage记录。成本/风险：延长不可达服务等待，仍有明确上限。
- Ruling：仅对明确IncompleteRead、完整JSON尚未交付的模型生成最多再请求2次，同一messages/观察原位继续；绝不重放工具，其他发送后超时/不确定错误仍终止。不把响应截断记为未发送或免费，unknown usage按单请求最大额度预留。truncated-red.log和final-verification.log验证真实HTTP截断、保守计费及浏览器点击不重复。成本/风险：服务可能重复收取生成费用，全部保留在ledger和费用上界中；该规则只适用于没有服务端工具副作用的chat/completions模型边界。

审查未列Minor；模拟OS/恶意软件/DDoS替身、general不能自动验证任意业务、未实测外部服务均按实际范围披露，不能借审查通过把它们扩大为真实攻击或全部外部功能成功。

最终TLS根因核验：当前DeepSeek DNS的8个TCP地址中，2个实际在TLS握手阶段SSLEOF；原socket地址回退只处理TCP失败，重复建连可能不断选中同一个TCP可达而TLS不可达地址。新增HTTPS连接层在HTTP生成请求发送前尝试下一个已解析地址，保持原host/SNI及证书校验；证书校验失败直接报错。tls-address-red.log及round-24/final-tests.log使用真实双端点本地TLS反例验证：第一个端点收到的只有ClientHello并关闭，第二个可信证书端点仅收到一次POST。此修复不重放HTTP生成，也不增加模型token计费。连接拨号仍逐地址限时，model attempts保留完整生命周期。

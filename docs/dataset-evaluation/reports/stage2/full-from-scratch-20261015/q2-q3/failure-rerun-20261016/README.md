# Q2 失败任务真实模型补测报告

状态：**PASS**。

本报告保留首轮失败记录，只对首轮 12 个正常任务进行真实 GLM 补测。补测使用 GLM 服务、真实 WorkflowToolLoop、真实本地工具和独立业务验收器；脚本化模型响应未计入结果。

## 配置

- 请求模型：`GLM-5.3`；服务端模型：`GLM-5.3-Flash`。
- `max_tokens`：`8192`。
- 工作流恢复上限：`max_steps=32`，`max_tool_errors=4`。

## 结果

- 补测通过：`12/12`。
- 若首轮已通过的 444 个任务保持不变，则 456 个正常任务的合并证据为 `456/456`。
- 合并数字表示首轮完整测量加固定失败任务补测，不等同于重新运行 456 个任务。

## 逐任务结果

|任务|工作流|场景|员工|日期|变体|执行|业务验收|模型请求|证据|
|---|---|---:|---|---:|---:|---|---|---:|---|
|q2-t0089|data_report|0|s0-r0-m08|4|2|PASS|PASS|6|`tasks/q2-t0089`|
|q2-t0142|data_report|0|s0-r1-m10|1|2|PASS|PASS|6|`tasks/q2-t0142`|
|q2-t0369|software_feature|1|s1-r1-m04|1|5|PASS|PASS|10|`tasks/q2-t0369`|
|q2-t0384|software_feature|1|s1-r1-m11|1|3|PASS|PASS|8|`tasks/q2-t0384`|
|q2-t0413|software_feature|1|s1-r1-m02|3|5|PASS|PASS|10|`tasks/q2-t0413`|
|q2-t0435|software_feature|1|s1-r1-m01|4|5|PASS|PASS|10|`tasks/q2-t0435`|
|q2-t0448|software_feature|1|s1-r1-m07|4|2|PASS|PASS|8|`tasks/q2-t0448`|
|q2-t0528|bug_fix|2|s2-r0-m11|2|4|PASS|PASS|7|`tasks/q2-t0528`|
|q2-t0545|bug_fix|2|s2-r0-m08|3|1|PASS|PASS|7|`tasks/q2-t0545`|
|q2-t0587|bug_fix|2|s2-r0-m05|5|0|PASS|PASS|7|`tasks/q2-t0587`|
|q2-t0688|bug_fix|2|s2-r1-m07|4|2|PASS|PASS|7|`tasks/q2-t0688`|
|q2-t0689|bug_fix|2|s2-r1-m08|4|2|PASS|PASS|7|`tasks/q2-t0689`|

## 原始失败与补测解释

首轮失败任务的原始执行报告仍保存在 `../business_pilot/execution_report.json` 和 `../business_pilot/model_usage.jsonl`。本次补测将 token 上限从 4096 提高到 8192，并为真实工具错误提供更大的有界恢复预算；每个工具调用和业务验收结果均保留在对应任务目录。

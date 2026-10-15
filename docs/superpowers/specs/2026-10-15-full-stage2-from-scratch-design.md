# 从规划起点重做第二阶段评测设计

## 意图

第二阶段必须比较两个框架从规划输入开始独立生成的数据集，而不是把当前框架生成的正常日程复制给 O/B/C。原始 Chimera 的单层 weekly meeting 和当前框架的分层 Phase 1 planning 都要实际运行，并保留完整中间产物、请求用量、失败记录和最终事件。

## 目标

- 用同一个新生成的公司画像作为配对输入，避免员工角色和组织规模差异混淆框架差异。
- O 从原始 Chimera 的 weekly meeting → daily schedule → legacy attack injection 运行。
- N 从当前框架的 leadership meeting → department plans → department meetings → employee phase plans → independent daily plans → multi-day attack injection 运行。
- 使用相同员工数、工作日、攻击规格、模型端点、工作窗口、攻击环境和日志字段。
- 在完整生成后运行 Q1–Q7 第二阶段指标，报告每个框架的分母、失败、成本和置信区间。
- 保留 O/N 的独立 provenance，不再把 O 写成共享正常日程上的契约复现。

## 范围与默认规模

- 正式重跑默认 12 名员工、20 个工作日、1 个独立 run；可通过 CLI 覆盖。
- 15 类 canonical 攻击规格全部登记到 manifest；正式成本受限时可显式指定攻击子集，但报告必须列出未注入规格。
- 采用 3 个共同攻击 Episode，O 使用 legacy 单日注入，N 使用 LLM 选择一个或多个日期；攻击步骤和成功/阻断状态进入独立真值 sidecar。
- 运行前清空专用输出根目录，禁止读取之前的日程、会议、攻击或评测产物。

## 生成流程

### 共同输入

1. 清空新的 run 根目录。
2. 由模型根据公司目标、员工规模和工作日生成一次公司画像；把生成的画像和组织树复制到 O/N 各自输入目录，作为配对输入。
3. O/N 仅共享这份输入画像和攻击规格，不共享会议结果、阶段计划、每日计划或攻击日程。

### O：原始 Chimera

1. 使用固定原始 revision 的 `meeting_for_weekly_goal_auto.py`，让所有员工进入同一个 weekly Workforce meeting。
2. 保存 weekly meeting 原始结果、模型请求和日志。
3. 使用原始 daily planning 入口把 weekly 结果展开成完整 20 个工作日的 `init_schedule`。
4. 使用原始 legacy attack path 对选定员工和攻击规格进行单日注入；每次注入前保留正常日程，注入后保留修改日程和攻击真值。
5. 运行正常日和攻击日执行器，收集统一事件格式、工具调用、业务结果和失败。

### N：当前框架

1. 使用 `meeting_for_phase_goal_auto.py --stage leadership` 运行领导层会议。
2. 使用 `phase_plan_generation_auto.py --stage departments` 生成部门阶段计划。
3. 使用 `meeting_for_phase_goal_auto.py --stage departments` 运行每个部门会议。
4. 使用 `phase_plan_generation_auto.py --stage employees` 生成员工阶段计划 bundle。
5. 使用 `daily_plan_generation_auto.py` 从 bundle 独立生成完整 20 个工作日的日程。
6. 在冻结的 N 正常日程上运行 LLM 多日攻击 campaign planner；只修改 LLM 选择的日期，未选日期必须 JSON 等价。
7. 运行正常日和攻击日执行器，收集与 O 相同的事件、工具、业务结果和失败字段。

## 公平性规则

- O/N 使用相同公司画像、员工数量、工作日数量、工作窗口、攻击规格、攻击环境、模型端点和执行预算。
- O 的 weekly meeting 与 N 的分层会议是被测差异，不能把任一方的会议结果复制给另一方。
- 攻击注入策略差异单列：O 是 legacy 单日，N 是 LLM 多日；质量比较和注入能力比较分表。
- 如果原始 Camel/OWL 依赖、浏览器或系统捕获能力缺失，必须在报告中标为未测并停止宣称完整运行，不用确定性 fixture 冒充真实 O。

## 评测输出

每次完整 run 必须包含：`study_manifest.json`、O/N provenance、公司画像 hash、会议和计划 artifacts、正常/攻击日程、统一事件、攻击真值、执行失败、逐请求 usage/cost、Q1–Q7 指标、对比表和 Markdown 报告。报告必须明确区分已实测、因环境阻断的未测项和仅适用于合成替身的结果。

## 非目标

- 不把第三阶段检测器 F1、ROC-AUC 等指标填入第二阶段质量结果。
- 不把 scripted pilot 或 deterministic oracle 当作完整长期员工仿真。
- 不把共享冻结日程上的 O 契约复现继续作为“原始框架完整生成”。

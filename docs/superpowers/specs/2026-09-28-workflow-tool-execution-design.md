# 文件系统驱动的工作流工具执行设计

## 目标

把员工任务从“把一组工具交给 LLM”改造成一个可追踪的工作流执行循环：先判断工作流，再只向模型暴露当前状态允许的工具；工具由 Python 执行，所有产物写入任务 workspace，详细执行日志可以直接抽取为细粒度工具行为数据集。

## 现状与约束

- `feat/phase-planning-pipeline` 的 Phase 1 计划生成和 Phase 2 日计划读取接口保持不变。
- 现有 `task.py` 使用 OWL/CAMEL RolePlaying，并将 FileWrite/Terminal 等工具作为扁平列表注册。
- 工具编排分支已有 `ToolSpec`、`ToolGraph`、`RoleToolkitResolver` 和内存版 `ArtifactBus` 原型，但没有接入真实日执行循环。
- 日执行使用 multiprocessing；跨进程共享状态不能依赖 Python 内存对象。
- 详细任务日志是行为事实来源，`final_schedule.csv` 只保留计划上下文。

## 设计

### 1. 文件系统工作空间

每个任务建立独立 workspace：

```text
<execution_logs>/<member_id>/workspace/<task_id>/
  artifacts/
  manifest.jsonl
  execution.log
```

每个工具读取前序产物的 artifact ID 或路径，并将输出写回 workspace。`manifest.jsonl` 记录 artifact ID、类型、生产工具、输入 artifact、相对路径、trace/task/member 和 ACL。文件内容是数据平面，manifest 是索引和血缘平面。

### 2. 工作流和状态

第一版提供三个通用工作流：

- `data_report`: `requested → source_acquired → analyzed → report_created → delivered`
- `software_feature`: `requested → issue_created → designed → implemented → tested → in_review → completed`
- `bug_fix`: `requested → issue_created → reproduced → fixed → tested → in_review → completed`

工作流分类使用确定性关键词规则作为可审计默认值；未来可替换为单独的 LLM 分类器。每个状态只声明可执行的工具和状态转移。

### 3. LLM 决策、程序执行

运行循环如下：

```text
任务文本 → workflow classifier → 当前状态候选工具
        → DeepSeek/OpenAI-compatible function calling
        → Python 校验并执行工具
        → workspace artifact + manifest
        → tool result 返回 LLM
        → 继续调用或最终回答
```

LLM 只做工作流内的工具选择和参数生成；程序负责工具执行、输入检查、状态更新、产物登记和超时处理。

### 4. 工具集合

第一版使用文件系统可验证的本地工具：

- 通用：`file_read`、`file_write`、`terminal`
- 数据报告：`source_query`、`data_transform`、`shared_storage`、`message_send`
- 开发流程：`issue_create`、`design_document`、`code_edit`、`test_run`、`build`、`pull_request`

非文件系统应用先以 JSON 凭证写入 workspace，仍然引用输入产物。

### 5. 行为数据集

运行时在详细 `execution.log` 中写入带 JSON 标记的工具事件；抽取器从 `execution_logs` 递归解析这些事件，生成：

- `agent_events.jsonl`：所有 LLM、工具、结果、错误和最终回答事件；
- `tool_calls.csv`：每次工具调用及输入/输出 artifact ID；
- `tool_transitions.csv`：同一任务中相邻工具的实际转移。

原始日志保留不变，计划 CSV 不参与细粒度行为推断。

## 非目标

- 本次不重写 Phase 1 会议、阶段计划或每日计划生成程序。
- 本次不接入真实 Gmail、GitHub、EHR 等外部应用；用 workspace JSON 适配器验证接口。
- 本次不删除现有 OWL/CAMEL 路径；通过配置开关启用新的文件系统工作流运行器，便于回归。

## 验收标准

1. 离线单测能够证明：工作流分类、状态候选过滤、跨工具 artifact 读写和开发工作流状态推进。
2. 真实 DeepSeek 调用至少完成一次多步 function-calling，并在 workspace 中产生两个以上相互关联的产物。
3. 从该次详细执行日志导出的 `tool_calls.csv` 至少包含两次工具调用，并能通过 artifact ID 重建调用链。
4. 原有 Phase planning 和工具编排单测不回归。

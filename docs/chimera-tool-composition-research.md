# Chimera 员工工具联通性调研：从「工具袋」到企业工作流

> 面向 NDSS 2026 Chimera 框架的方法移植说明。目标不是再堆更多孤立 API，而是让员工在**同一共享状态**上连续使用工具，使正常办公与内部威胁轨迹都更接近真实生产环境。
>
> 文档版本：2026-09-18　|　工作分支：`cursor/tool-composition-research-c01a`　|　原型：`src/tool_composition.py`

---

## 1. 结论先行

Chimera 当前把员工能力做成了**扁平工具列表 + 一条完全独立的邮件 LLM 路径**。这与真实医院 / 企业办公相反：真实员工几乎从不「只用搜索」或「只用终端」，而是 `EHR → 表格 → 共享盘 → 带附件邮件 → 值班群通知` 这样的**跨应用链路**。

建议按四层栈移植，而不是继续往 `task.py` 里追加 Toolkit：

| 层 | 作用 | 主移植论文 | Chimera 落点 |
| --- | --- | --- | --- |
| L3 Planner / 角色路由 | 按角色和任务分解子目标 | HuggingGPT、TPTU-v2、MetaGPT | `task.construct_society`、`profile_generation.py` |
| L2 Tool Graph | 用有向边约束「谁能接到谁」 | ToolNet、ControlLLM、GTool、ToolChain* | 新建 `src/tool_composition.py` |
| L1 企业应用层 | Email / Drive / Chat / Calendar / EHR / Tickets 是**有状态的应用** | AppWorld、TheAgentCompany、OfficeBench | 扩工具，替换 `member_email.py` 的旁路 |
| L0 Artifact Bus | 文件、附件、病历行、工单在工具间传递 | AppWorld 共享库、τ-bench 状态机 | 日仿真工作区 + ACL |

本仓库已落地可单测的 L0–L2 原型（**尚未接入日仿真主循环**，避免打断现有 Phase 2/3）。流感周报链路的单测证明：邮件可以带上共享盘附件，聊天可以引用这封邮件。

![割裂的工具袋 vs 联通的企业应用层](assets/chimera-tools-siloed-vs-connected.png)

---

## 2. 现状诊断：割裂具体出在哪

对照代码，割裂不是「工具太少」这么简单，而是**三条互不相通的世界**：

![Chimera 现状调用图](assets/fig-current-callgraph.png)

### 2.1 工作任务：OWL 拿到的是工具袋

`src/task.py` 的 `construct_society()` 把 FileWrite / Terminal / Browser / Search 一次性塞进 `assistant_agent_kwargs["tools"]`。模型看到的是一份无序清单，没有：

- 工具之间的合法后继（Search 的产出应是 URL，Browser 才消费 URL）
- 产物类型（csv、png、docx）
- 与下一任务、下一员工的交接物

这正是 ToolNet 批评的范式：*“simply format tools into a list of plain text descriptions … ignores the intrinsic dependency between tools”*。

### 2.2 邮件：另一条单次 LLM，读不到工作区

`daily_execution_auto.py` 里 `is_email_send_activity()` 为真时走 `Member.send_email()` → `member_email.py` 的两次 `run_llm`。邮件只有 `subject` / `content`，**不能附上刚才 FileWrite 写出来的流感表**。生产环境里「写完报告再发邮件」是同一件事，Chimera 里是两个互不认识的子系统。

### 2.3 角色 tools 字段是人设，不是绑定

`profile_generation.py` 会生成 `"tools": ["Sketch", "ComponentLibraryToolkit", ...]`，以及 `application.Zendo` 这种账号。这些字符串**从不进入** `construct_society()`。设计师和流行病学家拿到的是同一套 Search+Browser+FileWrite+Terminal。

### 2.4 任务进程互相隔离

每次 `run_task` 在独立进程里跑，`output_dir` 虽按成员划分，但：

- 浏览器缓存、终端产物、邮件、次日计划之间没有对象层
- 长期记忆只有 `daily_summary_*.json` 的自然语言，没有可被下一工具打开的 artifact
- 内部威胁步骤（`attacks/*.json`）同样无法表达「先从 EHR 导出再经共享盘外发」

所以即使用更多 CAMEL Toolkit（代码里已注释掉 Image / Video / CodeExecution），只要仍是扁平列表，割裂不会消失。

---

## 3. 调研范围与筛选标准

检索来源：arXiv / Hugging Face Papers / ACL Anthology / ICLR / NeurIPS Datasets & Benchmarks。筛选条件：

1. **必须处理多工具或多应用**，而不是单 API 调用；
2. 方法能在 **不重新训练基础模型** 的前提下接到 Chimera 的 OWL RolePlaying / Camel ChatAgent；
3. 对内部威胁仿真有加成：共享状态、权限、跨应用痕迹。

下面 16 篇均满足至少两条。矩阵里「强」表示建议作为主移植来源。

![论文与可移植方法相关矩阵](assets/fig-paper-method-matrix.png)

---

## 4. 相关论文（16 篇）

每篇按「做什么 / 和 Chimera 的错位点 / 可搬什么」写，避免只堆摘要。

### 4.1 HuggingGPT — 控制器分解任务并路由专家工具

- Shen et al., *HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face*, NeurIPS 2023. [arXiv:2303.17580](https://arxiv.org/abs/2303.17580)　[HF](https://huggingface.co/papers/2303.17580)
- LLM 做 **task planning → model selection → execution → response**，子任务的输入输出显式相连。
- **错位**：Chimera 没有 Planner，OWL assistant 自己在工具袋里摸索。
- **可搬**：在 `construct_society` 前加一层轻量 Planner，把「完成流感趋势分析并通知主任」拆成有 I/O 的子任务，再按角色选 toolkit，而不是把全部工具丢给一次 RolePlaying。

### 4.2 Chameleon — 即插即用的组合推理

- Lu et al., *Chameleon: Plug-and-Play Compositional Reasoning with Large Language Models*, 2023. [arXiv:2304.09842](https://arxiv.org/abs/2304.09842)　[HF](https://huggingface.co/papers/2304.09842)
- 把知识检索、视觉、程序、表格等做成 **模块**，用 LLM 生成模块序列。
- **可搬**：把 CAMEL Toolkit 当成 Chameleon 模块；每个模块声明 `consumes` / `produces`。这正是本仓库 `ToolSpec` 的来源。

### 4.3 ToolLLM — 大规模 API 与规划，而不是 4 个工具

- Qin et al., *ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs*, ICLR 2024. [arXiv:2307.16789](https://arxiv.org/abs/2307.16789)
- ToolBench + DFSDT 规划；先检索再调用。
- **可搬**：企业应用层做到几十个 API 之后，**不要**再全部塞进 prompt。用角色 / 当前 artifact 类型做检索（TPTU-v2 的 API Retriever 同一思路）。Chimera 现阶段工具少，但一扩 EHR+Drive+Chat 就会撞上这个问题。

### 4.4 ControlLLM — 在工具图上搜路径（Thoughts-on-Graph）

- Liu et al., *ControlLLM: Augment Language Models with Tools by Searching on Graphs*, 2023. [arXiv:2310.17796](https://arxiv.org/abs/2310.17796)
- 先建 **参数依赖图**，再在图上搜最优路径，最后交给执行引擎。
- **可搬**：这是 Chimera 最缺的中间层。Search 产出 `url`，Browser 消费 `url` 产出 `table`，Spreadsheet 消费 `table`。没有图，模型就会「搜完直接写邮件」。

### 4.5 ToolNet — 用有向图替代扁平列表

- Liu et al., *ToolNet: Connecting Large Language Models with Massive Tools via Tool Graph*, 2024. [arXiv:2403.00839](https://arxiv.org/abs/2403.00839)
- 节点是工具，边是转移权重；LLM 只在**当前节点的后继**里选下一步。可在线更新边权。
- **可搬（强烈建议）**：Owl 每轮只暴露 `graph.successors(current_tool)`。失败则降权该边（ToolNet 对 tool failure 的鲁棒性直接对应 Playwright / 搜索 API 抖动）。

### 4.6 GTool — 请求相关的工具图 + 补边

- Chen et al., *GTool: Graph Enhanced Tool Planning with Large Language Model*, 2025. [arXiv:2508.12725](https://arxiv.org/abs/2508.12725)
- 静态全图往往缺边；按当前请求构图，并预测缺失依赖。
- **可搬**：医院场景里「EHR → Spreadsheet」对流行病学家是边，对行政助理不是。用角色 + 任务生成**请求子图**，而不是一张全球图。

### 4.7 ToolChain\* — 在工具动作树上做 A\*

- Zhuang et al., *ToolChain\*: Efficient Action Space Navigation in Large Language Models with A\* Search*, ICLR 2024. [arXiv:2310.13227](https://arxiv.org/abs/2310.13227)
- 把 API 调用做成决策树，A\* 剪掉高成本分支。
- **可搬**：攻击日（`daily_execution_auto_attack.py`）动作空间更大，适合用代价函数把「异常外发」路径标出来——既服务正常规划，也为检测研究提供「规划器认为高代价但仍被攻击者走了」的标签。

### 4.8 AppWorld — 多应用、共享数据库、状态评测

- Trivedi et al., *AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents*, ACL 2024 Best Resource Paper. [arXiv:2407.18901](https://arxiv.org/abs/2407.18901)　[项目](https://appworld.dev/)
- 9 个日常应用、457 个 API、约 100 个虚构用户；应用通过**同一关系库**互相可见。评测看终态，不看死板 API 序列。
- **可搬（架构级）**：Chimera 缺的不是第 5 个 Toolkit，而是 **Email / Drive / Chat / EHR 写同一份状态**。AppWorld 后来还提供了 MCP Server，和「每个企业应用一个本地工具服务」一致。

### 4.9 TheAgentCompany — 仿真软件公司内网

- Xu et al., *TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks*, 2024（NeurIPS 2025 D&B）. [arXiv:2412.14161](https://arxiv.org/abs/2412.14161)　[站点](https://the-agent-company.com)
- 自托管 GitLab + OwnCloud + RocketChat + Plane；任务天然跨代码、文档、聊天、项目管理。最强基线大约只能自主完成约 24–30%。
- **可搬**：这是「真实生产不割裂」的最强证据。Chimera 若继续只用搜索+终端+无附件邮件，正常行为分布会系统性偏离企业日志，内部威胁检测的迁移价值会打折。第一期不必上完整 GitLab，用 **内存/JSON 版 Drive + Chat + Tickets** 即可，接口形状对齐。

### 4.10 OfficeBench — 办公套件来回切换

- Wang et al., *OfficeBench: Benchmarking Language Agents across Multiple Applications for Office Automation*, 2024. [arXiv:2407.19056](https://arxiv.org/abs/2407.19056)
- Word / Excel / Calendar / Email 同容器；失败模式主要是**不会在应用间切换**、操作冗余、幻觉。GPT-4o 通过率约 47%。
- **可搬**：Chimera 的「工作任务 vs 邮件」硬分叉，正好是 OfficeBench 指出的失败模式。必须允许一次 OWL 会话里既写表又发信。

### 4.11 WorkArena — 企业 SaaS 工作流（ServiceNow）

- Drouin et al., *WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?*, 2024. [arXiv:2403.07718](https://arxiv.org/abs/2403.07718)
- 知识员工在 ServiceNow 上的工单、目录、列表任务；配套 BrowserGym。
- **可搬**：医院 IT / 行政侧用 Tickets 应用模拟工单系统。内部威胁里「滥用工单提权」比「随机打开终端」真实得多。

### 4.12 τ-bench — 有状态工具 + 领域政策

- Yao et al., *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*, 2024. [arXiv:2406.12045](https://arxiv.org/abs/2406.12045)
- 零售 / 航空等领域 API + **policy**；数据库终态一致性；`pass^k` 测稳定性。
- **可搬**：给 EHR / Drive 写 **policy 文本**（谁能导出 identifiability 字段、谁能外发附件）。攻击者违反 policy 的 tool call 本身就是带标签的异常。Chimera 现在的攻击 JSON 只描述 MITRE 步骤，没有「哪条工具政策被破坏」。

### 4.13 Generative Agents — 跨活动记忆

- Park et al., *Generative Agents: Interactive Simulacra of Human Behavior*, UIST 2023. [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)
- 观察 → 记忆流 → 检索 → 反思 → 计划。
- **错位**：Chimera 已有 `daily_summary` 和 `previous_summary`，但是**自然语言摘要**，下一工具打不开。
- **可搬**：记忆条目同时挂 `artifact_id`。第二天流行病学家应能「打开昨天的 `epi/week-12/flu.csv`」，而不是只记得「昨天做了趋势分析」。

### 4.14 MetaGPT — SOP 与角色间共享产物

- Hong et al., *MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*, ICLR 2024. [arXiv:2308.00352](https://arxiv.org/abs/2308.00352)
- 用标准化 SOP 减少多 Agent 幻觉级联；产物（PRD、代码）在角色间交接。
- **可搬**：周会（Camel Workforce）的纪要不应只变成每人一份 JSON 日程，而应变成 **Drive 上的共享周报**，日仿真里的工具能读到它。这把 Phase 1 和 Phase 2 真正接起来。

### 4.15 Agent Workflow Memory — 从轨迹里诱导可复用配方

- Wang et al., *Agent Workflow Memory*, 2024. [arXiv:2409.07429](https://arxiv.org/abs/2409.07429)
- 从成功轨迹抽取 workflow，离线或在线提供给后续任务；WebArena 相对提升约 51%。
- **可搬**：OWL 执行日志已经按 `member_id_week_*_executio_task_*.log` 落盘，是现成的诱导语料。把高频成功链（如 `ehr→spreadsheet→drive→email`）变成 recipe，塞回 Planner。攻击日若偏离常用 recipe，既更真实，也更好标。

### 4.16 TPTU-v2 — 真实系统里的检索 / 微调 / 示例选择

- Kong, Ruan et al., *TPTU-v2: Boosting Task Planning and Tool Usage of Large Language Model-based Agents in Real-world Systems*, 2023. [arXiv:2311.11315](https://arxiv.org/abs/2311.11315)
- 真实商业系统三个痛点：API 太多、顺序难、接口语义近。对应 API Retriever、LLM Finetuner、Demo Selector。
- **可搬**：Chimera 短期不做微调；**Retriever + Demo Selector** 立刻能用。给「流感周报」类任务固定几条 demonstration 工具链，比指望 4o-mini 零样本拼出跨应用流程更稳。

---

## 5. 希望集成到 Chimera 的具体方法

![四层栈](assets/fig-target-stack.png)

### 方法 A — Artifact Bus（先做，改动面最小，收益最大）

**来源**：AppWorld 共享库、TheAgentCompany 的 OwnCloud、Generative Agents 的记忆流。

**做法**：公司级对象存储，键为 `artifact_id`，值为类型、生产者、owner、ACL、payload。所有工具只通过 Bus 读写。

**接到现有代码**：

- `Member.temp_dir` / `output_dir` 继续存字节，但写完必须 `bus.put(...)`
- `send_email` 增加 `attachment_ids`，从 Bus 取 Drive / File 对象
- `daily_summary` 除自然语言外写 `artifact_ids: [...]`
- 攻击步骤的 `observable_evidence` 指向具体 artifact（例如 `drive://epi/week-12/flu.csv` 被拷到个人盘）

原型：`ArtifactBus`、`WorkplaceApps.send_email(..., attachment_ids=...)`。

### 方法 B — Tool Graph 替代扁平 `tools=[]`

**来源**：ToolNet、ControlLLM、GTool。

**做法**：每个工具声明 `consumes` / `produces`。边由 schema 对齐自动生成。OWL 每轮只注册后继工具（或全量注册但在 system prompt 里给出邻接表 + 禁止跳边）。

医院场景的目标图：

![社区医院员工工具图](assets/chimera-hospital-tool-graph.png)

**接到 `task.py`**：`construct_society(question, output_dir, tools=session.tools)`，不要写死四件套。`offline_mode` 仍可关掉 Browser/Search，但 Email/Drive/EHR 应保留（它们是本地状态，不依赖外网）。

原型已覆盖：`search→browser` 合法，`search→ehr` 非法；从 `ehr` 规划到 `email` 会经过表格/共享盘。

### 方法 C — 角色路由，让 `profile.tools` 真正落地

**来源**：HuggingGPT 的 model selection、MetaGPT 的角色 SOP、TPTU 的检索。

**做法**：

1. 维护别名表：`Sketch → file_write`，`Excel → spreadsheet`，`Epic/EHR → ehr`，`Slack/RocketChat → chat`（见 `PROFILE_TOOL_ALIASES`）
2. `RoleToolkitResolver.resolve(profile)` 按 `role` 关键字 + 别名绑定
3. 协作核心（email / shared_drive / file_write）**所有人常驻**，避免再次把邮件变成特权旁路

![角色路由与工作流记忆](assets/chimera-role-router-awm.png)

流行病学家应拿到 EHR+表格+终端；行政助理拿日历+工单+邮件，默认**没有** EHR。这同时提高正常行为区分度，并让「越权读病历」成为可执行的攻击步骤而不是 prompt 里的一句戏。

### 方法 D — 把邮件（以及聊天、日历）收回 Toolkit

**来源**：OfficeBench、TheAgentCompany RocketChat、AppWorld 消息应用。

**做法**：删除「邮件活动 / 工作活动」的硬分叉，或保留分叉但邮件函数必须能读 Bus。一次 RolePlaying 允许：

`spreadsheet.aggregate → shared_drive.save → email.send(attach=...) → chat.notify`

`member_email.py` 可以继续用 LLM 写语气，但 **to / attachments / thread_id** 必须是结构化工具参数，否则永远没有附件和引用。

### 方法 E — 企业应用层（适度扩工具）

**来源**：AppWorld 9 apps、TheAgentCompany 四件套、WorkArena 工单。

建议新增的**有状态应用**（优先内存实现，不必先上真实 GitLab）：

| 应用 | 关键 API | 谁用 | 内部威胁语义 |
| --- | --- | --- | --- |
| Shared Drive | `save / share / copy / acl` | 全员 | 批量下载、权限扩散、投递点 |
| Email | `send / reply / attach / forward` | 全员 | 外发、钓鱼、附件泄露 |
| Chat | `post / dm / mention` | 全员 | 社工、值班口令、横向沟通 |
| Calendar | `create / invite` | 行政、临床 | 异常时段、掩护窗口 |
| Tickets | `open / comment / close / assign` | IT、护理 | 假工单提权 |
| EHR | `query / export / audit` | 临床、流行病 | 越权查询、批量导出 |
| Spreadsheet | `aggregate / join / plot` | 数据、流行病 | 把导出变成可外发报表 |
| Terminal | 现有 | 开发 / 数据 | 与 Drive 互通，而不是写完就丢 |

搜索和浏览器保留，但它们是 **L2 图上的入口节点**，不是唯一能力。

### 方法 F — Workflow Memory

**来源**：AWM。

**做法**：从现有 OWL 日志解析 tool-call 序列，聚类成 recipe。Planner 先检索 recipe 再执行。原型里 `WorkflowMemory.remember / suggest` 已能复用 `ehr→spreadsheet→email`。

### 方法 G — 领域 Policy 挂在工具上

**来源**：τ-bench。

**做法**：每个应用带一份短政策，例如 EHR：`不得把 identifiability 字段写入可被 * ACL 看到的 Drive`。正常员工的 Planner 被政策约束；攻击脚本显式 `violate_policy=true`。日志里同时有 MITRE 标签和 **policy-id**，检测研究更干净。

---

## 6. 一条应能跑通的黄金路径

默认场景是社区医院流感分析（`config.company_type` / `config.goal`）。真实员工不会「打开终端随便敲」，而会走：

![流感趋势分析跨工具工作流](assets/fig-flu-workflow.png)

原型 `flu_trend_demo()` 已经在单测里跑通对应状态变化：

1. `ehr_export` → `ehr_record`
2. `aggregate_table` → `table`
3. `save_drive` → 全员可见的 `drive_object`
4. `send_email` 把 Drive 对象列为附件（`attachment_count ≥ 1`）
5. `notify_chat` 引用该邮件 id

这就是「工具有联系」的最小可执行定义：**后一步的输入是前一步的对象，而不是再编一段自然语言。**

---

## 7. 代码怎么接（按文件）

不建议一上来改 OWL 内核。按依赖从里到外：

| 文件 | 改什么 |
| --- | --- |
| `src/tool_composition.py` | **已加** Bus / Graph / Resolver / Apps / Memory |
| `src/task.py` | `construct_society` 接收 `EmployeeToolSession`；工具列表来自 `session.allowed_names()`；FileWrite/Terminal 的目录与 Bus 对齐 |
| `src/member_email.py` | `get_email_content` 增加可选 `attachment_ids`；或降级为 Email toolkit 的文案生成器 |
| `src/activity_utils.py` | 邮件不再独占一条执行路径，或「邮件活动」仍走工具会话 |
| `src/daily_execution_auto.py` | `Member` 持有 `bus` 引用（进程间用 JSONL/SQLite）；`execute_task` 把 session 传进 `run_task` |
| `src/daily_execution_auto_attack.py` | 攻击步骤可声明 `tools` 与 `artifacts` |
| `src/profile_generation.py` | 示例 tools 改成可解析别名；生成后校验 `RoleToolkitResolver` 非空 |
| `src/post_meeting_summary_auto.py` | 周目标同时写入 Drive 对象 |
| `attacks/*.json` | `how[].procedure` 增加 `artifact_flow` 字段（非破坏性扩展） |

进程模型注意：现在 `run_task_in_process` 是 **multiprocessing**。Bus 必须是跨进程存储（SQLite / JSONL 在 `execution_log_dir`），不能只放父进程内存。原型里的 `ArtifactBus` 是单测用内存版，接入日仿真时换成文件后端即可，接口不用改。

---

## 8. 分阶段路线图

![四阶段路线图](assets/chimera-integration-roadmap.png)

**P0 打通事件（推荐下一 PR）**

- Email 可挂附件（哪怕先只附 `output_dir` 里最新文件）
- 同一成员当天的 FileWrite 目录对后续任务可见
- `profile.tools` 经别名表绑定，不再是死字符串

**P1 工具图 + 角色路由**

- 把 `src/tool_composition.py` 接入 `task.py`
- OWL 提示词加入邻接表；可选：每轮只暴露后继
- 单测保持绿，再开小规模 Phase 2（1 天、少量员工）看日志里是否出现跨工具链

**P2 企业应用层**

- Drive / Chat / Calendar / Tickets / EHR 的 JSON 后端
- 周会产物进 Drive
- 攻击 JSON 增加 `artifact_flow`

**P3 工作流记忆与政策**

- 从执行日志诱导 recipe
- τ-bench 风格 policy + `pass^k` 稳定性（同一工作流跑 k 次，产物 schema 是否稳定）
- 用跨应用 traces 重新评估内部威胁检测基线，回答「更真实的正常行为是否让旧检测器失效」

---

## 9. 对内部威胁仿真意味着什么

联通工具不是为了让 agent 更强，而是为了让 **CERT 风格日志长得像真的**：

- 正常：EHR 小查询 → 聚合表 → 内部盘 → 内部邮件附件 → 值班群
- 泄露：EHR 大查询 → 个人盘 / USB 路径（Terminal）→ 私人邮箱转发
- 提权：假工单 → 日历掩护 → 共享盘 ACL 被改
- 破坏：Tickets 关闭监控 → Terminal 清日志（仍应留下 Bus 上的审计对象）

没有共享状态时，攻击步骤只能是自然语言「exfiltrate files」，sysdig/pcap 里看不到一条可解释的应用层因果链。有了 Bus，检测特征可以从「调了 Terminal」升级到「EHR 导出行数 vs 历史 recipe 的偏离 + 附件发往域外」。

---

## 10. 风险与非目标

- **Token 与延迟**：ToolNet 的本意是减少工具描述占用。P1 应用后继裁剪，不要把 8 个应用的全部 API 一次性塞进 12 条消息窗口（`message_window_size = 12` 已经很紧）。
- **不要一上来 docker 化 GitLab**：TheAgentCompany 的环境很重，和 Chimera 已有的 sysdig 容器叠加会极难复现。先 JSON 应用层。
- **不要为了联通而联通外网**：`offline_mode` 应仍能跑 Drive/Email/EHR；只有 Search/Browser 依赖外网。
- **权限必须默认拒绝**：否则「全员 `acl=*`」会让泄露场景失真。EHR 默认仅 owner 可见，显式 share 才扩散。
- **本 PR 不修改日仿真主循环**，避免在无充分回归时改变 NDSS 实验路径。

---

## 11. 原型如何验证

```bash
PYTHONPATH=src python3 -m unittest tests.test_tool_composition
```

覆盖：图约束、角色绑定（含 Sketch 别名）、EHR ACL、流感链路附件、AWM recipe 复用。

接入主循环前，建议再加：用一份真实 `generated_members/*.jsonc` 跑 `RoleToolkitResolver`，统计每类角色的工具集合，防止全部塌缩成同一套。

---

## 12. 飞书云文档

本文件即飞书导入源稿（Markdown + 图）。

**无需开放平台权限（手动）**

1. 打开飞书 → 云文档 → 「导入」
2. 选择 `docs/feishu/chimera-tool-composition.html`（图已内嵌，不会丢）
3. 或直接导入本 Markdown，再把 `docs/assets/` 下的 png 拖进对应段落

**有开放平台权限（自动）**

创建企业自建应用，开通云文档导入 / 云空间权限，然后：

```bash
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
export FEISHU_FOLDER_TOKEN=可选的文件夹 token
python scripts/build_feishu_doc.py --publish
```

脚本会申请 `tenant_access_token`，按[导入文件概述](https://open.feishu.cn/document/server-docs/docs/drive-v1/import_task/import-user-guide)上传 HTML 并创建 `docx` 导入任务，成功后打印云文档 URL。

本环境未配置飞书应用凭证，因此仓库内交付物是：**Markdown 源稿 + 内嵌图 HTML + 一键发布脚本**。拿到 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 后在同一分支执行 `--publish` 即可生成真正的飞书云文档链接。

---

## 13. 参考文献（Bib 速查）

1. Shen et al. HuggingGPT. NeurIPS 2023. arXiv:2303.17580
2. Lu et al. Chameleon. 2023. arXiv:2304.09842
3. Qin et al. ToolLLM. ICLR 2024. arXiv:2307.16789
4. Liu et al. ControlLLM. 2023. arXiv:2310.17796
5. Liu et al. ToolNet. 2024. arXiv:2403.00839
6. Chen et al. GTool. 2025. arXiv:2508.12725
7. Zhuang et al. ToolChain*. ICLR 2024. arXiv:2310.13227
8. Trivedi et al. AppWorld. ACL 2024. arXiv:2407.18901
9. Xu et al. TheAgentCompany. 2024. arXiv:2412.14161
10. Wang et al. OfficeBench. 2024. arXiv:2407.19056
11. Drouin et al. WorkArena. 2024. arXiv:2403.07718
12. Yao et al. τ-bench. 2024. arXiv:2406.12045
13. Park et al. Generative Agents. UIST 2023. arXiv:2304.03442
14. Hong et al. MetaGPT. ICLR 2024. arXiv:2308.00352
15. Wang et al. Agent Workflow Memory. 2024. arXiv:2409.07429
16. Kong, Ruan et al. TPTU-v2. 2023. arXiv:2311.11315

补充（正文未单列但构成背景）：Yao et al. ReAct, ICLR 2023, arXiv:2210.03629；Cai et al. LATM, arXiv:2305.17126。

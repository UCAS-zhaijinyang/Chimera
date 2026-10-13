# 三阶段评测：详细实施与实验计划

本文件保留完整三阶段任务规格。第一阶段已完成本地应用仿真的执行、明确规格业务与L0记录验收，实际样本量、失败与费用见[第一阶段报告](reports/stage1/README.md)；第二/三阶段的样本量与预算仍为设计值。后两阶段主线为原始Chimera O与当前数据N的质量对比，再用同一四检测方法在同target比较用途；见[主比较协议](comparison-validation.md)、[第二阶段任务](stage2-tasks-and-cost.md)和[第三阶段任务](stage3-tasks-and-cost.md)。涉及指标定义时以 [framework.md](framework.md) 为准；所有付费模型仅 DeepSeek。

## 实施总览

按“数据可信 → 行为与成果合理 → 威胁检测效用”推进。每阶段先明确输入、检查方法、交付和停止条件；相关指标统一见framework.md。P0–P4仅保留为工程实施里程碑，不能与三个评测阶段混淆。

| 评测阶段 | 主要实施任务 | 对应工程里程碑 | 交付 |
|---|---|---|---|
| 第一阶段：确认生成数据可信 | 采集契约、标准化、血缘/身份关联、攻击证据与标签 | P0；每个后续run重复L0检查 | 可追溯数据、采集覆盖和异常清单 |
| 第二阶段：O/N数据质量对比 | 原始来源、共同规格/字段、独立oracle、分布/覆盖、重复与盲评 | P1–P4 | O/N质量差值/CI及当前专项报告 |
| 第三阶段：同方法检测效用对比 | 四固定检测器、匹配O/N训练、共同target、泄漏/迁移/稳健性 | 在P2预注册，P3–P4执行 | 同target检测差值/CI与用途范围 |

在采集确认数据前冻结第三阶段的split、主要指标、阈值和告警预算。三阶段逻辑上递进，但共用一次数据生成、标准化与费用账本；统计诊断可并行运行。

## 第一阶段：确认生成数据可信

目标是使每条待评价行为与其员工、任务、产物和攻击证据可核查。输入为原始日志/产物及预期采集清单；完成接口审计、观测补齐与L0检查后，输出标准化数据、标签sidecar、采集coverage和坏行/失败清单。

只有对应模态具备可靠证据，才能支撑后续成果或效用结论。缺采集或映射不完整时先修复；未具备的能力明确标NOT_MEASURED。

### 1.1 初始接口审计与实现前置项（历史设计记录）

下表记录执行修复前的接口问题，不代表当前所有项仍未实现；第一阶段实际修复和未测能力以[最终实测](reports/stage1/README.md)为准。

| 已存在接口 | 本分支事实 | 后续必须补什么 |
|---|---|---|
| `src/planning_io.py`、`phase_planning.py` | 发布阶段/个人计划，严格验证和指纹 | 将 goal/phase/workday/activity稳定ID交接到执行sidecar |
| `src/planning_schedule.py:execution_activities` | 执行导出保留 `Time/Activity`，不保留原activity ID与时长 | 保持旧loader兼容，另写 task metadata 与活动ID映射；不要改旧文件含义 |
| `src/task.py:run_workflow_task` | 各trace workspace在`<output_dir>/workflow_workspaces/<trace_id>`；详细日志复制到 execution_logs | run级命名空间、复制日志去重、task started/completed/failed/timeout与原始activity关联 |
| `src/workflow_runtime.py:WorkflowToolLoop` | `TOOL_EVENT/FINAL_EVENT`，无统一时间/序号；模型无tool_calls可提前结束 | event_seq/call_id、业务时间+wall时间；最终完成必须显式oracle，timeout与HTTP错误有事件 |
| `FilesystemArtifactBus` | 有type/owner/ACL/path/trace/inputs；逐行manifest读取容忍坏行 | 评测直接读原始字节并报坏行；root声明、版本hash、每工具预期依赖边 |
| `FilesystemToolRuntime` | `code_edit`/`test_run`/`build`目前可能无inputs；compileall不测业务正确 | 补input对应关系；返回执行returncode和business_status，功能测试oracle读取报告内容 |
| `reproduce_bug/approve` | 写本地JSON凭证；`message_send`同样是本地事件 | 声明simulation_only；真正复现/授权/外发需真实适配证据，不能混淆 |
| `src/tool_log_extractor.py` | 只认tool/final标记；损坏JSON静默跳过；transition只纳成功并按step排序 | 新评测adapter读原日志计损坏；所有尝试与同step顺序、source_line保留；不要用成功CSV推完整度 |
| `OpenAICompatibleChatClient` | 只返message，丢掉usage；配置默认可能不是DeepSeek | 独立保留model实际ID、usage/缓存/finish_reason/request ID、失败重试费用；评测配置锁DeepSeek |
| task级workspace/日摘要 | 不能推定跨员工消费、跨天共享或真实email已联通 | feature coverage声明；跨任务handoff测试前先实现可查询共享索引/ACL与显式消费事件 |
| attack schedule / 外部捕获 | 计划能注入，但收集能力随环境而变 | 每episode checkpoint与可采集数据源，系统/网络时钟误差；无源时NOT_MEASURED |

`dev` 中 `src/dataset_eval.py` 的初步检查只适配内存 demo/OrgCascade，不能直接运行在当前phase/workflow路径上。可迁移独立断言设计，但需重新适配、验证和固定L0–L5编号。

### 1.2 观测、标签与适配层（P0）

计划新增 `src/evaluation/{schema,inventory,normalize,labels,metrics}.py`；修改 runner 的事件采集和客户端usage记录。实现时再选标准库/dataclass或JSON Schema，避免为读日志引入完整评测平台。

事件最小契约：

```json
{
  "schema_version": "chimera-eval-event/1",
  "run_id": "scenario-seed-variant",
  "event_id": "uuid",
  "event_seq": 17,
  "call_id": "tool-call-id",
  "trace_id": "existing-trace-id",
  "task_id": "stable-task-id",
  "planned_activity_id": "stable-activity-id",
  "member_id": "epi-1",
  "phase_id": "phase-1",
  "workday": 2,
  "simulation_time": "2025-05-05T10:30:00+08:00",
  "wall_time_utc": "2026-10-12T02:30:00Z",
  "event_type": "tool_result",
  "tool_name": "data_transform",
  "from_state": "source_acquired",
  "to_state": "analyzed",
  "invocation_status": "success",
  "business_status": "success",
  "inputs": ["artifact-source"],
  "outputs": ["artifact-table"],
  "source": {"path": "execution.log", "line": 22, "sha256": "..."}
}
```

这是目标契约示例，不是当前事件格式。`business_status` 只能由工具语义/独立oracle产生；actor与目标权限不合规不靠模型补写。多次attempt使用不同call_id；多个run不能共享同一个全局trace key。artifact至少记录版本、内容hash、scope、授权变更及允许写集合。

每个run的能力位：`has_simulation_clock`, `has_plan_links`, `has_shared_bus`, `has_real_email`, `has_system_capture`, `has_network_capture`, `has_attack_evidence`。按能力决定可测子集；对照试验中同一指标仅在共同可观测子集比较并报告coverage。

验收：原始标记行守恒，复制日志不双计，坏JSON不消失；能定位unknown task、重复ID、悬空输入、同step多调用、早退final、HTTP失败、timeout及未捕获episode。失败/未知均有状态。评测输出不含API key。

### 1.3 第一阶段验收与交接

运行L0全量检查，保存原始行守恒、主键唯一连接、产物/输入存在性、时间因果和标签证据结果。交付inventory、normalized_events、parse_rejections、plan_task_links、artifact_index、attack_truth及对应hash。

交给第二阶段的是可定位的事实与采集能力，不是“已经真实”的结论。交给第三阶段的标签单独存放，检测特征构建不能读取真值sidecar。所有后续先导/确认run重新执行该验收，不能只验证黄金fixture。

## 第二阶段：原始 Chimera 与当前框架的数据质量对比

### 2.1 来源与共同条件（P1）

O优先原始发布快照；没有则固定原版commit与配置复现。只读采集/模型API适配不移植当前规划/router/tool行为，当前legacy开关、旧失败队列和round24原描述重放都不能作为O。N冻结当前完整框架确认版本。登记[manifest模板](comparison-manifest.template.json)中的来源、模型、scenario、labels、hash和能力，原始来源当前尚未核验。

共同高层业务/角色/人数/天数/样本/模态尽量匹配，框架各自保留完整机制。已发布快照无法匹配时，只比较共同范围，报告模型/规模混杂，不把结果当单组件因果增益。原版无真实成果不填0/伪造manifest。

### 2.2 免费前置与oracle

复用第一阶段L0/业务检查器和故障经验；为共同明确规格增加oracle、允许写diff、真实交接与业务时间。只有两源都有相同成果证据才计算业务成功/pass^3差值；只有N有产物时作当前专项。simulation_time序号毫秒不支撑员工节奏，必须补真正时间含义；跨任务生产/消费需要明确证据。

受控错误与语义挑战真值人工审核，不混入自然质量均值。参考R先登记许可/字段/标签；没有R只报O/N分布差异和规格一致性。

### 2.3 先导与确认候选（P2–P3）

| 阶段 | 每来源规模 | 两来源规模 | 用途 |
|---|---|---|---|
| 先导 | 3共同场景×2run×5天×12成员＝360员工日 | 720员工日 | 适配/费用/方差/量表；不当确认结果 |
| 确认候选 | 3×6run×20天×12成员＝4,320员工日 | 8,640员工日 | 质量与后续检测共享；规模先导后冻结 |

每员工日2任务仅为成本假设，不是证明足够的量。原始快照不能强制这些规模，选择共同可比范围及真实独立群体；公共数据无run不能伪造。复现时每场景的6个独立确认run默认分配为3个训练、1个验证、2个测试run，缺足够独立组/episode时扩样或收窄结论，不用日志行数量替代。

双方新生成均只用可共同支持的DeepSeek型号，完整记录usage/缓存/所有失败与重试。原版费用按真实请求结构先导，不用当前单价冒充。相同确认数据供两阶段复用，不因检测器重新生成。

### 2.4 Q1–Q7任务与报告

Q1计划落实、Q2成果/稳定性/副作用、Q3交接/跨天、Q4分布/时间/覆盖/重复/图、Q5模拟攻击语义、Q6独立盲评和judge资格、Q7共同质量与成本/局限汇总。细则见[任务文档](stage2-tasks-and-cost.md)，科学公式保留[框架L1–L4](framework.md)。

每项并列O值、N值、N−O及95%CI、分母/coverage/能力与证据，原版缺成果不记0。共同质量和当前新增能力分表；没有外部R不从D(O,N)推出“更真实”。正式结构见[第二阶段报告](reports/stage2/README.md)。

### 2.5 人工与模型评分

60校准＋180确认，每包3专家，3分钟约36人小时，6分钟约72小时；准备/培训/仲裁和挑战真值另计。3场景×O/N×30确认仅起点，各cell良恶各15是平衡诊断，总体估计需抽样权重；失败/unknown/少数角色保留。校准/确认按run/template隔离，确认不按judge高分筛选。

共同日志盲化来源/模型/标签，四维评分有必要证据才评价，可核验成果缺失abstain；不因N上下文更丰富改变共同评分条件。原四源120包不再默认生成。DeepSeek360次Flash＋60次Pro起步约$1.156032，见[成本JSON](stage2-cost-estimate.json)。judge不合格仅诊断，不能替代独立人工。

## 第三阶段：相同检测方法验证检测效用差异

### 3.1 冻结四方法与输入（D0）

保留原论文RBF-SVM、Temporal CNN、GCN、DS-IID，名称已核验，代码/config尚待取得。注册代码/依赖、架构、特征、窗口/图规则、搜索空间、epoch/early-stop、seed与训练/调参预算。轻量CPU模型可调试但不替代四方法主结果。

每方法两源输入语义一致；CNN过去窗口不跨split，GCN不能使用测试标签/未来边，DS-IID按原目标与序列适配。正常量/独立攻击episode匹配，共同标签/观察模态。单独的新血缘/图表示不混入主效果。

### 3.2 共同验证与独立target

默认双方同V_common调参/阈值，来自O/N验证组；只用train拟合预处理，target不用来生成、judge或选参。若source-only验证另预注册，并标协议差异；外部验证适配单列。

优先合格独立外部holdout；没有时冻结O_test/N_test共同池。O训练与N训练均评两个域，分域及固定50/50域宏平均报告，域内原阳性率保留。不得只比“O训O测”与“N训N测”。独立run/员工群/episode/template/family分割并审计窗口/协作桥接，公共数据用真实独立单位。

### 3.3 同方法主比较（D1–D2）

四方法各自两次训练来源，固定架构/搜索机会与同target，保存continuous scores、验证阈值、训练checkpoint和设备账本。主ΔAP与ΔRecall@审查预算；辅助Precision/Recall/F1/ROC-AUC/MCC/FPR/每千正常员工日报警、episode召回和日终延迟。

每方法单独列O训练、N训练、差值和CI。未检出延迟按删失，缺首次证据时未测；全日特征不声称上午检出。若增加滚动评分另冻结过去窗口。正式结构见[第三阶段报告](reports/stage3/README.md)。

确认前冻结同一组配对训练seed（候选5个）及每seed的验证阈值选择规则。每seed分别算O训练、N训练的指标和差值，主表用全部预定seed的指标算术均值及平均差值，同时保留逐seed结果、标准差和范围；不得挑最优seed或平均预测分数后暗中作为集成模型。内部双域先按每seed计算各域指标，再用固定50/50权重宏平均，最后平均seed。主95%CI条件化于这组冻结已训练模型：每次bootstrap对所有seed和两训练源使用同一target组/episode重采索引，重算逐seed指标再平均，seed不在主bootstrap中重采；训练seed变异另表，训练数据生成不确定性另做外层训练组重采并重训。确定性方法可复用经核验完全相同的拟合，记录重复对应，不把重复结果当额外独立样本。预定seed运行失败必须报告并重跑；未补齐不得选择性删除后填完整主结果。

### 3.4 泄漏、迁移与稳健性（D3–D5）

必做标签/路径/模板/oracle泄漏审计、metadata-only与随机训练标签负控制，target真值不变。可得数据上同target跨场景/新族/模板或外部转移；缺模态/时钟噪声和N新增表示另列。CERT为外部合成、TWOS为人类竞赛、授权企业数据才支持TSTR。

外部增强R_only/R+duplicate/R+O/R+N、规则/单轮/统计生成器及legacy/规划消融均可选，独立预算，不替代主O/N定义或要求。见[主矩阵](comparison-validation.md)。

### 3.5 成本与阶段结论

共享生成不再次收费；检测主流程API $0，四方法CPU/GPU时间和工程/参考准备先导实测。2来源×4方法×（5候选×3组内训练CV＋5最终seed）＝160拟合仅为工作量例算；负控制、消融、外层训练重采另计。普通测试bootstrap复用预测，不重训。预算见[第三阶段成本](stage3-cost-estimate.json)。

结论逐方法/target说明检测变化及区间，不挑最好方法，不由检测高分反推业务正确。缺原始来源、共同标签/模态、实现或正例即未测/不确定；不以廉价替代方法补全确认表。

## 全流程统计：样本量、差值与判定

1. 先导估计实际独立组、相关性、主差值方差和费用，再冻结样本/target/阈值/主指标/实用界限与停止规则。场景3、每域2测试run等只是起点，不保证功效。
2. 质量主指标为共同证据业务内容评分差值与严重缺陷率差值；共同oracle充分时加业务成功率。检测主指标为同target四固定方法的ΔAP、ΔRecall@预算。必要时Holm控制，探索性多特征可BH-FDR，效应/区间完整报告。
3. 配对只用于真实共同条件的run/task；不可配对原始快照按实际群体做两样本分组CI。评分保留rater结构，pass^k按task聚类，不把多次工具调用当独立样本。
4. 检测两预测按同target相同组/episode索引重采，分域结果与固定宏权重保留。默认2,000次本地重采仅起点，保存seed。测试CI对冻结训练条件化，训练生成不确定性另重采训练组并重训。
5. 硬违规为0；软差异/非劣界限先导校准，不采用统一KS≤0.10或均值4。p>0.05不证明等价；CI跨界限则INCONCLUSIVE，事件多不补独立组少。
6. 失败、unknown、缺模态和最差组全部留存，不能事后挑run、换检测器或target。修改生成器/评测器后新建确认版本，旧数据和报告不回写。

## 工程里程碑、执行入口与验收

以下入口是**拟新增接口**，目前不可直接运行；不得在报告中当成已验证命令。建议后续统一为：

```text
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage validate
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage oracle
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage fidelity
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage judge --dry-run
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage detection
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage report
```

当前可以调用的只是现有程序：`scripts/extract_tool_calls.py`、`scripts/run_workflow_deepseek_smoke.py`、`src/planning_audit.py`。现有 smoke 会调用付费API；第一阶段现已增加并实际运行 `scripts/evaluate_dataset_trust.py`、`scripts/run_dataset_trust_campaign.py`、`scripts/combine_trust_studies.py`。本文后续第二/三阶段命令仍是规划接口。

| 顺序 | 实现范围 | 完成证据 | 不通过时 |
|---|---|---|---|
| P0 | 第一阶段既有L0与基础oracle复用 | 第一阶段实测报告与新数据复核 | 修事实/采集，不推断合理性 |
| P1 | O身份、只读共同字段/标签、双方能力、时间/交接与四检测器适配 | provenance/capability/registry与免费边界检查 | 原始来源或输入缺失则未测 |
| P2 | 两源先导、60校准包、实际生成/训练成本与方差 | 冻结confirm、target、指标/界限与预算 | 保留失败，缩次级或限结论 |
| P3 | 共享确认数据、180独立人工包、Q1–Q7 | 质量主表与当前专项、hash和CI | 不补挑成功数据 |
| P4 | 四方法同target、D0–D5与联合报告 | 逐方法差值/CI、负控制、实际CPU/GPU与范围 | 未测/不确定，不更换主方法 |

共享仿真、原四模型适配与专家排期的工时需先导测量后再估计，以上里程碑不承诺固定耗时。

后续代码的必要测试围绕可破坏评测结论的情况：双计日志、静默丢弃坏行、假业务成功、缺失真值被填阴性、跨run ID冲突、跨split bridge、label/path泄漏、同step多调用乱序、0分母、bootstrap错误抽样单位、pass^k误写为pass@k。不只测“函数返回了某字段”。

## 最终报告：按三阶段交付结论

最终报告按三个阶段编排主表，L0–L5作为各表的指标索引：

| 报告部分 | 主要证据 | 必须写出的结论范围 |
|---|---|---|
| 第一阶段：数据可信 | L0核心契约、标签证据、采集coverage与异常记录 | 哪些记录/模态可追溯，哪些未测或缺失 |
| 第二阶段：O/N数据质量对比 | L1–L4共同质量差值/CI、原版来源、独立人工及当前能力专项 | 改善/退化/未测范围，缺原版成果不填0 |
| 第三阶段：同方法检测效用对比 | 四固定方法、O/N同target、L5差值/CI与审计 | 逐方法/target效应与用途，是否有外部/企业证据 |

每表记录版本、实际model、运行数、观察量、正例episode数、成本、采集coverage，并列点估计、95%CI、差异、分母、状态与失败链接；另给每场景/角色/工作流/攻击族/最差run。失败、unknown、NOT_MEASURED和oracle变更放入发布卡。

各阶段主表并列O原版/N当前/差值/CI；第三阶段按四方法和共同target分层。参考内锚点、增强曲线与其他生成器属于可选扩展，负控制必做。记录生成源的标签等级与信息访问权；外部缺数据不留空白，明确 `NOT_MEASURED`。补充产物清单见 [比较协议](comparison-validation.md)。

最终结论是用途与证据边界：例如“在共同证据范围内，当前相对原始Chimera的质量差异为多少；在某共同target上，四固定检测方法的AP变化分别为多少；尚无真实企业TSTR证据”。只有实际结果满足才使用此类句式。本轮没有这些结果，不填预期分数。

## 附录：完整交付目录与任务边界

第一阶段补齐观测并建立可信数据；第二阶段做O/N共同质量与盲评差异；第三阶段保持四方法、用同独立target比较训练源效用。每阶段有可审计交付与停止条件。不能通过降低角色覆盖、去掉难攻击、只保留成功轨迹来省钱。

预期产物：

```text
evaluation_output/<study_id>/
  study_manifest.json            # 代码/模型/环境/预算/规格版本
  preregistration.json           # 主指标、差异界限、分割、样本量、停止规则
  inventory.json                 # 各run预期文件、实际文件和capture能力
  normalized_events.jsonl        # 标准化行为，保留原始来源行/byte/hash
  parse_rejections.jsonl         # 损坏/无法解析记录，禁止静默丢弃
  plan_task_links.jsonl          # 阶段→计划活动→实际任务
  artifact_index.jsonl           # 各task workspace的产物、版本与依赖
  attack_truth.jsonl             # intent/attempt/execution/observation，隔离存放
  split_manifest.json            # 不重叠group、day范围、episode/template/family归属
  metrics.jsonl                  # value/numerator/denominator/CI/status/evidence
  failures.jsonl                 # 失败样本位置与原因，不覆写原数据
  judge_packets.jsonl            # 盲化证据包与coverage
  judge_results.jsonl            # 原始模型输出、usage、parse与abstain
  expert_ratings.csv             # 独立原始评分，不只留均值
  costs.jsonl                    # 每请求与阶段成本，不含凭证
  detection/                     # 冻结特征、scores、threshold、split、模型版本
  comparison/                    # 基线manifest、外部inventory、source-target/增强/负控制
  report.md                      # 分层结果、区间、失败与能力范围
  dataset_card.md                # 数据来源、用途、局限、覆盖、泄漏检查
```

真值目录与检测 feature builder 通过明确 allowlist 隔离。发布时可提供研究标签，但训练输入中不出现 `attack_truth`、oracle结果、文件路径中的 attack 标记、预定攻击描述等信息。

研究阶段原本只交付计划；用户随后已授权第一阶段测评、修复与真实DeepSeek调用，实施与失败记录见[第一阶段报告](reports/stage1/README.md)。本轮未执行第二/三阶段，未合并 `dev`、购买外部数据或联系专家。

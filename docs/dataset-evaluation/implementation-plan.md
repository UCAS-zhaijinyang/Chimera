# 详细实施与实验计划

本文件是后续实现的任务规格，不是已运行记录。默认选择由本次研究提出，尚无实测样本量/方差/费用。涉及指标定义时以 [framework.md](framework.md) 为准；所有付费模型仅 DeepSeek。

## 1. 目标、边界与成果

先把当前 runner 的证据收齐，再实现 L0–L2 全量检查，然后做有限重复与盲评，最后完成有独立持有集的分布/检测对照。每阶段有可审计交付与停止条件。不能通过降低角色覆盖、去掉难攻击、只保留成功轨迹来省钱。

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
  report.md                      # 分层结果、区间、失败与能力范围
  dataset_card.md                # 数据来源、用途、局限、覆盖、泄漏检查
```

真值目录与检测 feature builder 通过明确 allowlist 隔离。发布时可提供研究标签，但训练输入中不出现 `attack_truth`、oracle结果、文件路径中的 attack 标记、预定攻击描述等信息。

本轮只交付研究和计划，不改 runner，不合并 `dev`，不默认购买数据、联系专家或启动付费仿真。

## 2. 当前接口审计与实现前置项

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

## 3. 任务 A：观测、标签与适配层（优先级 P0）

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

## 4. 任务 B：独立 oracle 与黄金/负控制（P1）

任务固定30个，每个工作流10个：6正常业务、2权限/参数拒绝、2有明确攻击证据目的的隔离仿真任务。共18正常、6拒绝、6攻击。任务参数不得由被评模型决定；golden期望由人工审核的确定性fixture给出。每个任务n=3独立重复，在legacy与workflow两执行条件下共180条轨迹。30是工程起步样本量，不能宣称总体95%成功。

| 工作流 | 内容oracle | 副作用/拒绝oracle | 限制 |
|---|---|---|---|
| data_report | 输入记录聚合值精确一致；报告引用正确数值；存储内容hash一致；交付引用且目标接收者可读 | 错input ID、无权actor应拒绝；非目标记录不能修改；预定外发仅在仿真范围验证证据 | 当前 message JSON不等于真实邮件，接收者可读性需共享适配实现 |
| software_feature | 目标fixture函数的独立功能测试通过；测试/构建report与代码版本一致；review对象引用正确产物 | 不能把compileall当功能测试；未授权approve不能被凭证蒙混；禁止修改其他任务文件 | 独立测试题不可暴露给生成模型，避免照抄测试 |
| bug_fix | 修改前独立测试失败且错误符合fixture；修改后同测试通过；不回归预定旁路用例 | 伪造`reproduced:true`不算复现；失败returncode不能推进为业务成功 | 精确oracle与编排状态分别输出 |

追加离线突变负例，**不新增LLM生成调用**：删除附件、换收件人、断输入边、错误聚合、非零returncode、提前final、重复工具事件、坏manifest行、注入label字段、伪造时间/序号。每类至少3个，从不同工作流/任务取样。自动评测必须命中确定性违反项；语义模型的漏判用专门挑战集报告，不混入原数据质量总体均值。

重置环境：每次从相同fixture快照创建新workspace，保留同task语义而独立请求；记录temperature、seed支持状况、服务端model ID和时间。`pass^3`对所有30个任务计算；权限拒绝任务的“成功”是正确拒绝，攻击任务的“成功”是按任务定义留下可核验证据，不能与正常无违规概念混淆。

零失败也不等于100%总体可靠：独立Bernoulli n次零失败的单侧95%失败概率上界约`1−0.05^(1/n)`。n=30时约9.5%；n≈299才把该上界压到1%以下。实际任务/重复相关，还需按任务聚类，不能把180条都当独立总体样本。

## 5. 任务 C：对照、先导与确认仿真（P2–P3）

### 5.1 主比较与消融

**主比较**：固定同一Phase 1阶段规划及相同init_schedule快照，只比较 `CHIMERA_WORKFLOW_EXECUTION=0/1`。同公司、成员、task fixture、模型、工作日和采集配置。此实验能归因工具执行改造，不能归因规划改造。

**规划消融（次级）**：2×2（legacy weekly / phase planning）×（legacy tools / workflow）。仓库保留旧weekly会议入口，但当前daily生成已重构；旧daily可从`67146a4`追溯，必须建立可运行基线adapter并验证旧格式，不能假设checkout旧代码即可公平比较。该消融单独run并计费，在主比较可用后再做。若adapter未完成，只报告未测的规划贡献，不给2×2数字。

**离线表示消融**：同一完整轨迹分别提取共同user-day特征、加组织图、加artifact链；删除/打乱不应可见元数据；无需重新仿真。结构性转移合法率不作为唯一成果，因为新router本来就强制了该条件。

### 5.2 场景与运行规模

默认三种业务：医疗、软件/游戏、金融；各12名员工、至少两个显式部门、清晰leader映射、不同角色与交接需求。这是拟建fixture，不是声称仓库已有这三种完整可运行场景。已有 `experiments/phase_planning/company.json` 可作为pipeline fixture参考，但不替代业务与攻击规格。

| 阶段 | 设计 | 员工日 / 轨迹量 | 可以回答什么 |
|---|---|---|---|
| P1 黄金 | 30任务×2工具条件×3重复 | 180任务轨迹 | oracle、工具链与有限可靠性 |
| P2 先导 | 3场景×2条件×2独立run×5工作日×12员工 | 720员工日，workflow360 | 采集/费用/方差/可行性；不得当确认结果 |
| P3 确认候选 | 3场景×2条件×6独立run×20工作日×12员工 | 8,640员工日，workflow4,320 | 组间效应、时序、跨场景与人工/下游对照 |

确认候选规模是起点，不是满足统计功效的承诺。每场景6个run不足时必须扩展独立run或收窄结论；不能靠增加同一run的相关事件假装增加独立样本。6个run分配为3训练、1验证、2测试，使测试域至少有两个独立run；两个仍不足以稳定估计尾部，先导后可能需要扩展。

正常集保留所有行为与失败；攻击以episode记录，默认至少3个可执行攻击族、每族覆盖不同角色/阶段。发布分布保持预定低阳性率，同时另建平衡的攻击诊断子集；主检测测试不得为提升F1重平衡。阳性不足则继续收集独立episode或把效用标为探索性。不能为凑样本将一次攻击的数百事件当数百独立攻击。

### 5.3 参考数据与不可用时的决策

- 旧ChimeraLog：只在有本地/授权快照时使用，固定版本和共同模态；没有则先生成同条件legacy基线，明确它不是论文原始数据复现。
- CERT：合成列式参考，版本固定r6.2等实际可得版本；只比较共同映射字段，不能作“真实企业”证明。
- TWOS：人类竞赛参考，需取得文件与使用许可，先确认正例/模态口径；出版元数据可访问不表示已拿到数据。
- 真实企业日志：可选、授权持有；只读heldout并脱敏，未获得就不承诺TSTR。
- 无任何外部参考：做规格一致性、内部统计、legacy相对比较；结论不写真实分布保真。参考内容不能由DeepSeek临时补造。

### 5.4 对齐与分割

固定共同模态映射、事件合并窗口、timezone、day边界、角色/部门标准化规则。尺度、分箱、嵌入、重复阈值仅在校准/训练集拟合。参考中不存在的字段仅参与扩展表示实验。

按评测问题分别建立独立split，不宣称一个split同时回答所有问题：

1. **独立run持有**：同场景每条件6run，默认3训练、1验证、2测试；所有员工/产物/episode留在run所在split。先导run仅用于采集/方差/阈值设计。共享task template还需按模板族分组，不能仅依run隔离宣称新模板泛化。
2. **前向时间**：在额外run或预注册的独立时间实验内按早期训练/中段验证/晚期测试；边界purge至少等于最长检测窗口、攻击episode和handoff span，不切断同episode。明确它测时间漂移而非新员工。
3. **新员工/角色**：按员工或可隔离协作群体分组；跨split消息/产物桥接检查，若不能避免群体泄漏则改为run/组织持有。不把相同人的不同天随机分散。
4. **跨场景/攻击族**：leave-one-scenario-out；另建leave-one-attack-family-out；模板改写不能跨split复制同攻击计划。目标持有集不参与生成器调参。

主效用比较两份**训练数据**在同一冻结target_test上得分，target来自独立run/外部快照。不能分别在新/旧自身测试集上得分后把差异归因数据效用。训练正常样本数量/观测量对齐，恶意episode数量分列；抽样固定种子且不以测试表现选样本。

没有外部数据时，target_test明确定义为**两执行条件各自的独立测试run集合**：同场景legacy两个测试run构成target_legacy，workflow两个构成target_workflow。train_legacy和train_workflow得到的检测器都评这两个完全相同的target，分别报告两域结果；另给预注册50/50域权重的宏平均，不能选择有利域作为唯一主表。测试run对由同scenario/fixture/replicate配对，但不与训练/验证重叠。

主要CI范围是**给定已冻结训练数据/检测器，独立测试run与其观测的抽样不确定性**，不涵盖生成训练集变化。若要声称训练数据生成过程的不确定性，另做嵌套训练run重采样并重新训练检测器；仅重采测试预测或换训练seed不能实现该结论。三训练run/两测试run的有限独立样本限制必须报告，必要时增加独立run。

GCN等图模型不允许全图包含测试标签/未来边；共同邻居会形成transductive评估时单独标识。时间窗口与组织跨split桥接必须记录在split manifest里。

## 6. 任务 D：统计校准、样本量与置信区间（P2–P4）

预注册主指标：L2全任务oracle成功率、L4人工业务可信度差异、L5共同测试AP与Recall@k差异。其余探索性指标完整报告，防止从大量指标中挑好看的。

工作性候选界限：L4非劣界限0.25/5；L5 AP非劣界限0.02；L2点目标90%用于工程排查，不自动作为总体门槛。先导结束后结合参考自身波动与业务需求固定；如果合理界限不同，记录理由并在确认前冻结，不能看确认结果改线。

统计步骤：

1. 先导估计scenario/run/task层内相关与paired difference标准差。预算、主效应方向、最小相关差异和有效独立单位写入preregistration。
2. 对paired run差异，用仿真重采样估计检测目标差异的功效（建议80%起步）与区间宽度。近似 `n_pairs≈[(z_.975+z_.8)*σ_diff/δ]^2` 只做起算；任务/场景分层相关必须用实际重采样校正。
3. 预算不够时缩减非主指标、重用离线数据或明确探索性结论，不扩大容忍界限，也不丢弃低质量run。固定confirm样本量或预定序贯规则；不每天看p值决定停。
4. 分布比较按scenario分层重采两条件的run pair；效用比较重采**同一target上的测试run pair与员工/episode**，两检测器的预测共用相同样本索引，并保持target_legacy/target_workflow及50/50权重。默认2,000次离线重采样，保存seed。效用主CI对固定训练数据条件化；若需包含训练生成变动，另加外层训练run重采样并重训，单独计compute费用。只重采测试分数不能声称已包含训练不确定性。
5. `pass^k`按task聚类；语义按trajectory聚类并保留rater结构；普通比例可给Wilson区间作描述，但不能用它抹掉聚类相关。
6. 仅3个场景时主要结论是这3个固定场景的结果；leave-one-out是诊断，不能宣称随机企业总体。每域2个测试run的bootstrap尾部尤其不稳，增加run或报告宽区间/敏感性，不把巨大事件数转成窄CI。
7. 主要比较需要多重检验时采用预注册Holm控制；多特征探索性距离可报BH-FDR，同时报告效应量。等价/非劣需相应CI与界限；`p>0.05`不代表等价。

确认样本揭盲前输出冻结的split/feature/oracle/judge/阈值hash；完成后不得删除失败。修改生成器或评测oracle后用新版本确认集，保留旧结果。

## 7. 任务 E：人工/DeepSeek盲评（P2–P4）

默认：60个先导校准包 + 180个独立确认包，每包3名专家，共720次评分；每包3分钟约36人小时（仅估计）。专家来源按可用条件安排，不假设本次已邀请。对照主比较180包：3场景×2工具条件×30包；每cell正常/攻击诊断各15包，跨role、phase、workflow分配，失败轨迹也抽入。

这个50/50是**专家诊断抽样**，不是发布或下游测试阳性率。若需要总体均值，用已记录的真实抽样概率加权并给CI；不加权则称平衡诊断评分。稀有失败/角色不足采用全取，缺格标出，不从另组补样冒充完整。

正常/攻击、数据来源、生成模型、条件和标签对专家/DeepSeek盲化；提供角色与业务任务必要上下文。深度计划/工具事实评分由证据支撑，标签安全审计由另一真值流程完成，不能通过给judge攻击标签指导评分。

若无法获得3人×独立确认样本：可交付双人/单人探索性结果并标局限；不能让模型做第三名“专家”。量表、升级与模型校准详见 [judge-and-cost.md](judge-and-cost.md)。

## 8. 任务 F：下游检测与成本最小化（P3–P4）

起步模型用CPU的logistic regression、RBF-SVM和一个轻量树模型，统一user-day共同特征。先发现标签捷径与分割问题，避免先花GPU训练复杂模型。论文级复现再按P01增加temporal CNN、GCN、DS-IID；模型性能未知时不声称简单模型已替代原四模型。

正常-only anomaly baseline可补充，但不可与有监督模型混报同一train setting。每种表示/模型训练使用相同验证/测试集，调参上限预注册（例如5个候选×grouped验证）；随机模型最多5个训练seed，固定已生成数据，不重跑仿真。仅训练seed的变化不是数据生成run的变化。

留存continuous scores、固定报警预算、threshold出处；报告AP、ROC-AUC、MCC、验证阈值F1、Recall@k、FPR、episode召回/延迟及CI。告警预算示例为每日审查top1%员工日，只是候选，需要目标用途预注册；k过小无命中时仍报告0及区间。

主user-day实验在模拟日终生成分数，报警时间设为该日固定日终；episode延迟从首次可观察恶意证据到首次日终报警，未检出按删失并报数量。若另做30分钟滚动评分，所有特征只读截至当前时刻的事件，不能复用全日特征声称更早检出。

抗扰动实验从同一数据离线构造：缺一种模态、时间戳抖动、去掉血缘/组织字段、去attack模板原文、移除路径/员工捷径、random-label负控制。扰动不能改变真值但破坏其证据而不说明；必须同时报可观察覆盖。

## 9. 工程实施顺序与验收

以下入口是**拟新增接口**，目前不可直接运行；不得在报告中当成已验证命令。建议后续统一为：

```text
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage validate
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage oracle
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage fidelity
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage judge --dry-run
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage detection
python scripts/evaluate_dataset.py --manifest <study_manifest> --stage report
```

当前可以调用的只是现有程序：`scripts/extract_tool_calls.py`、`scripts/run_workflow_deepseek_smoke.py`、`src/planning_audit.py`。现有 smoke 会调用付费API，本次未运行。

| 顺序 | 实现范围 | 完成证据 | 不通过时 |
|---|---|---|---|
| P0（1–2个工作日估计） | inventory、事件/产物/标签schema、成本usage、normalizer | 离线已知真值fixture与异常日志守恒；每metric可定位来源 | 修采集，不报分布/效用 |
| P1（2–3日估计） | L0–L2、30黄金任务、允许写diff、突变负控制 | 确定性gold与错误均能正确判；缺证据返回NOT_MEASURED | 修oracle/契约后重新小跑 |
| P2（2–3日+专家排期） | 先导720员工日、60校准包、价格usage/方差、baseline兼容 | 预算估算、校准误差、参考可得性、样本量与主比较冻结 | 保留数据，减次级范围或声明探索性 |
| P3（按真实运行速度排期） | 8640员工日候选确认、留run/场景/family测试、180独立人工包 | 原始数据/分割不可变；所有run失败/成本齐全 | CI不足时扩run或降结论；不补挑成功 |
| P4（2–3日估计） | 分布/语义/检测报告、敏感性、发布卡 | 共同holdout、无标签捷径、CI与局限可复算 | 受限发布或不宣称效用 |

时间是实施工作量预估，不是本轮执行计划或耗时承诺。P3仿真、原四模型复现与专家排期需测量后再估计。

后续代码的必要测试围绕可破坏评测结论的情况：双计日志、静默丢弃坏行、假业务成功、缺失真值被填阴性、跨run ID冲突、跨split bridge、label/path泄漏、同step多调用乱序、0分母、bootstrap错误抽样单位、pass^k误写为pass@k。不只测“函数返回了某字段”。

## 10. 最终报告模板与决策

每表记录版本、实际model、运行数、观察量、正例episode数、成本、采集coverage。主表逐层列点估计、95%CI、差异、分母、状态与失败链接；另给每场景/角色/工作流/攻击族/最差run。失败、unknown、NOT_MEASURED和oracle变更放入发布卡。

最终结论是用途与证据边界：例如“在三个受控场景下，工具链业务终态提高且人工评分非劣；在独立合成持有集上AP非劣；未获取真实企业持有集，尚无TSTR结论”。只有实际结果满足才使用此类句式。本轮没有这些结果，不填预期分数。

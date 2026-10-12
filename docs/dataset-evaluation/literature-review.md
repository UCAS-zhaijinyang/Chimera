# 生成数据集与数据集评测：面向 Chimera 的论文调研

检索截止：2026-10-12。近期检索覆盖 2024–2026；方法追溯覆盖 2013–2026。检索主题是合成数据评测、合成时间序列评测、内部威胁数据集，不以多智能体工具组合论文代替数据评测文献。近期 API 检索与领域基础论文追溯分开记录，后者不是前者的检索命中。

## 调研如何支撑三阶段评测

论文按所支持的结论组织：首先建立日志和标签可信的证据；接着检验任务成果、时序/组织分布与语义真实性；最后验证独立检测效用。参考编号P01–P25保持不变，完整论文链接与阅读级别集中在附录A。

| 阶段 | 调研要解决的问题 | 主要依据 |
|---|---|---|
| 第一阶段：确认生成数据可信 | 行为证据与攻击真值如何对应，发布数据是否可追溯 | P01/P02/P14/P22–P24 |
| 第二阶段：检查行为与成果是否合理 | 独立终态、可靠性、分布覆盖、组织及盲评如何验证 | P06–P13/P15–P21 |
| 第三阶段：验证能否支持威胁检测 | 合成转移、真实转移、稀有威胁效用及泄漏如何评估 | P01/P05/P13/P14/P25 |

一篇论文可以支撑多个阶段，采用的具体方法与不能移植的结论分别写清。

## 第一阶段：确认生成数据可信

先建立“记录确实对应发生过的行为、标签有证据”的基础，再解释数据来源与发布限制。这一阶段的方法直接落到L0契约与可追溯性。

### 1.1 日志、行为与攻击真值

P01/P02 的启发是将数据用途写清：数据服务于内部威胁检测与分析员，关键不是员工邮件的文风，而是身份、行为、对象、时间、协作与攻击证据能否连接。P14 的全文特别记录了早期 `true_label` 被放入分析输入导致实验无效、随后修订的经历。新体系据此明确：真值存放在独立 sidecar，攻击计划只能定义意图，实际执行与采集证据各有状态，检测模型不能读到攻击文件名、注入文字和 oracle 结果。

采用：L0 中的计划—调用—业务结果—采集事件四级对齐；标签按事件/任务/用户日分别定义；孤立攻击标签不靠 LLM “看起来像攻击”确认。

限制：有完整日志不代表真实企业分布；工具执行被模拟、网络未真实发生时，必须标为 `simulation_only`。失败攻击和被阻断攻击应保留，不把所有攻击者整天的行为标恶意。

### 1.2 发布可信度与隐私的适用条件

P22 反对“合成即匿名”的假设，P23/P24 则要求用途与来源可追溯。本框架默认仿真产生虚构人，但提示词、外部搜索和配置可能带入实际信息。

采用：发布卡列出模型实际 ID、提示/输入来源、采集能力、覆盖、失败、合成比例、使用限制；扫描实际凭证/个人信息、近重复、标签路径泄漏。只有接入私有训练/参考数据才新增成员推断、最近邻风险等隐私攻击评测。

限制：PII 扫描通过不能证明匿名或差分隐私；没有私有训练集时成员推断标 `NOT_APPLICABLE`，不是 100% 隐私通过。

## 第二阶段：检查行为与成果是否合理

这里从任务的独立终态扩展到群体行为，再以人工确认内容和协作真实性，对应L1–L4。单任务成功、整体分布相近与专家认为可信分别提供不同证据。

### 2.1 独立终态与重复可靠性

P15 对可接受终态集合和 collateral damage 的检查，使评测允许多条合法实现路径。P16 的 `pass^k` 衡量“连续 k 次都成功”，P17 的检查点可以诊断长攻击链中何处停止。它们评的是 agent 能力，新方案只迁移任务证据部分，不能用这些指标包办数据质量。

采用：针对本分支三个工作流写黄金任务集。报告合法**尝试**、执行成功、业务成功和最终目标分别占比；检查点、无关对象变化、允许写集合以及拒绝越权的负例都加入 oracle。任务自然语言“完成”或工作流到终态不能代替 oracle。

限制：目前 `reproduce_bug`、`approve` 写 JSON 凭证；`test_run` 默认 compileall；`source_query` 提供模拟记录。这些可以测编排，却不能证明真的复现 bug、通过业务测试、获得真人审批或查询 EHR。任务评测必须检验内容或真实工具证据。

### 2.2 条件分布、时序与多样性

P09 将保真、覆盖、记忆分开；P10 把保真/效用/隐私放在一个可比较工作流内；P11/P12 说明不能用单一通用分数。P06 的表格协议适合共同字段，但无法解释跨工具链。P07/P08 提醒需要跨时间关系；P13 在异常交易任务中同时检查统计质量与分类效果。

采用：用户日、任务链、组织周图三个视角，正常和恶意分别统计；同时看类别覆盖、近重复、时间间隔、自相关、活动转移、跨角色协作。保真距离在共同特征空间计算，参考拆分的距离作为“参考自身变动”底线。

限制：新工作流确实会产生旧数据没有的附件或血缘，不能因为整体来源分类器能识别这些新字段就判不真实。α-Precision/β-Recall 若采用普通手工特征空间估计必须注明改编及距离敏感性；没有生成训练集时不报告原版 Authenticity，也不把复读率改名为隐私指标。

### 2.3 组织协作与机会数控制

P18 为图分布距离提供可靠依据；P19 将微观交互与宏观图性质分开。新方案不用“组内/组间边 >1”当通用阈值：三人部门与二十人部门的潜在边数不同；某些业务本来就需要跨部门交付。

采用：按可交互的有向员工对数量归一化组内/组间边密度；显式排除自环，保留边类型与次数；再看负责人桥接、任务指定的跨部门 handoff、孤立角色覆盖和图统计。与保度随机重连/部门大小匹配的 null 模型比较。真实协作参照不可得时，仅称“组织规格一致性”，不称“真实图保真”。

### 2.4 人工与DeepSeek评审的独立性

P01 原文的评审是每数据集 100 条，良恶各 50，四个应用模态，五位专家；正文明确因层内方差未知采用比例分配近似 Neyman，并非完整 Neyman 最优分配。原文 α=0.87 是原实验结果，不能当作本框架的测得值。

P20 的 GPT-4 方法仅作为量表设计来源，P21 的顺序/冗长/自我偏好在使用 DeepSeek 时必须重新校准。由同一厂商生成和评审的相关偏差不能靠重复调用消除。

采用：专家先评 60 个校准证据包，再评 180 个独立确认包，默认每包三人。任务链比孤立文本更能发现假的成果与协作。DeepSeek 低价模型初评，只有预定义不确定项升级到同厂较强模型；最终主表保留人工均值、ordinal α 与区间。自动评分用随机盲样本测其误差与漏判。

限制：专家数量较原文减少，不能称原实验直接复现。专家未达到数量或一致性要求时报告不确定，不用模型补成“专家共识”。模型预筛不能先删除低分数据再报代表整体的均值。

## 第三阶段：验证能否支持威胁检测

前两阶段确定数据和行为证据范围，这一阶段进一步验证检测与迁移效用，对应L5。测试集的来源、阳性比例、标签隔离与独立分割共同决定能作出的结论。

### 3.1 下游效用、类别比例与标签捷径

P05 的 TSTR 要求真实持有测试集；CERT/旧 ChimeraLog 都是合成，所以相关实验称 **S→S transfer**，TWOS 是 **S→human-collected**，真实企业日志才称 **TSTR**。P25 说明稀有阳性时只报 ROC-AUC/accuracy 容易误导。P14 的极少正例也说明大负例数不等于充足检测证据。

采用：主报 average precision（AP）、固定报警预算下 recall、FPR/千员工日、攻击 episode 召回与延迟；F1 是验证集选择阈值后的辅助指标。使用共同测试持有集比较旧/新生成数据训练的检测器，按正常观测量对齐训练规模并分别报告恶意样本数；元数据-only、去元数据、去注入原文与去 artifact 字段四个诊断拆分分开运行。

限制：检测更难、F1 更低不自动说明更真实；F1 更高也不自动说明生成质量改善。应有人工/行为证据与无泄漏转移效用共同支持。

## 按主线阅读论文

### 外部比较与有效性印证的补充依据

原有方法还可以支持“优于独立方法、在外部数据上有效、能帮助已有检测任务”的比较，具体设计见 [对比实验与外部有效性验证](comparison-validation.md)。P06 CTGAN、P07 TimeGAN、P08 DoppelGANger 提供非 LLM 生成方法候选，按已有摘要级证据选为待验证基线，不声称已读其全部实现或完成复现。P05 支持将合成训练与独立真实测试分开；P02/P04 确定 CERT/TWOS 作为不同等级外部来源。P09/P10/P13 支持分布/覆盖和检测效用同时评价，P14/P21/P25 分别支撑标签隔离、独立专家与稀有阳性的正确比较。

独立规则/单轮 DeepSeek 基线、“原数据+重复采样”增强对照、少样本曲线和私有配对挑战是本方案设计选择，不从上述论文推导具体费用/样本量或通用有效性门槛。此次补充复用原25项文献，未新增检索记录，不提升任何受限全文的阅读级别。

第一阶段先读P01/P02，再结合P14的标签泄漏限制和P23/P24的可追溯文档；第二阶段先读P15/P16的终态与可靠性，再读P09/P11/P12的分维度评测、P18/P19的图结构，以及P21的评审偏差；第三阶段读P05的TSTR与P25的稀有威胁指标，并回到P01/P13检查检测协议。P03待获得有效全文再纳入方法依据。

## 附录A：参考文献链接与迁移矩阵

编号在其他文档中保持一致。年份是该入口的论文/首发年份，版本变更单列说明。

| ID | 论文与原始入口 | 年份 / 阅读 | 适合评测的部分 | 不应直接移植的部分 |
|---|---|---|---|---|
| P01 | [Chimera: Harnessing Multi-Agent LLMs for Automatic Insider Threat Simulation](https://www.ndss-symposium.org/wp-content/uploads/2026-f375-paper.pdf) | 2026 / F，§V | 内部威胁主基线：专家、时段/行为统计、四检测器、跨场景 | 原样本与新数据的对象图不同；原分割不能替代本方案的分组防泄漏 |
| P02 | [Bridging the Gap: A Pragmatic Approach to Generating Insider Threat Data](https://www.ieee-security.org/TC/SPW2013/papers/data/5017a098.pdf) | 2013 / F | 真实性相对于被测系统；明确背景与攻击的可观测要求 | CERT 不能作为所有企业行为的真实分布 |
| P03 | [Generating Test Data for Insider Threat Detectors](https://jowua.com/wp-content/uploads/2022/12/jowua-v5n2-5.pdf) | 2014 / U，入口返回验证页 | 待补读的 CERT 背景文献 | 不用未读全文支持具体方法或门槛 |
| P04 | [TWOS: A Dataset of Malicious Insider Threat Behavior Based on a Gamified Competition](https://doi.org/10.1145/3139923.3139929) | 2017 / M，Crossref，出版页 403 | 人类竞赛采集的多模态参照 | 不称为生产企业分布；不假设有可对齐的产物或 ACL |
| P05 | [Real-valued (Medical) Time Series Generation with Recurrent Conditional GANs](https://arxiv.org/abs/1706.02633) | 2017 / A | TSTR：合成数据训练、真实持有集测试 | 没有真企业数据就不能把 CERT 测试叫 TSTR |
| P06 | [Modeling Tabular data using Conditional GAN](https://arxiv.org/abs/1907.00503) | 2019 / A | 表格合成的统计拟合与机器学习效用分开看 | 表格拍平丢失时序、血缘与组织边 |
| P07 | [Time-series Generative Adversarial Networks](https://papers.nips.cc/paper/2019/hash/c9efe5f26cd17ba6216bbe2a7d26d490-Abstract.html) | 2019 / A，NeurIPS | 同时评相似性、预测能力和跨时间相关 | 本方案不复现 GAN；不能只看事件边际分布 |
| P08 | [Using GANs for Sharing Networked Time Series Data: Challenges, Initial Promise, and Open Questions](https://arxiv.org/abs/1909.13403) | 2019 预印本 / A，IMC 2020 | 网络时间序列的属性与序列关系、面向用途评测 | 不要求 Chimera 使用 DoppelGANger 生成器 |
| P09 | [How Faithful is your Synthetic Data? Sample-level Metrics for Evaluating and Auditing Generative Models](https://arxiv.org/abs/2102.08921) | 2021 首发，ICML 2022 / F，§3–4 | α-Precision、β-Recall、Authenticity，分开保真、覆盖与记忆 | n-gram 复读率不等于论文的 Authenticity；无生成训练集不测该量 |
| P10 | [Synthcity: facilitating innovative use cases of synthetic data in different data modalities](https://arxiv.org/abs/2301.07573) | 2023 / F，§Evaluation | 统一保真、效用、隐私接口，支持表格与时序 | 库中默认参数不是日志领域阈值；不必全库安装 |
| P11 | [Evaluation is key: a survey on evaluation measures for synthetic time series](https://doi.org/10.1186/s40537-024-00924-7) | 2024 / M，Crossref 摘要 | 选指标必须对应任务与时间序列特点，没有通用评测程序 | 未读全文，不引用其具体分类数量或具体优劣排名 |
| P12 | [On LLMs-Driven Synthetic Data Generation, Curation, and Evaluation: A Survey](https://arxiv.org/abs/2406.15126) | 2024 / F，§3–4 | 生成、筛选、评测分离；正确性、多样性及下游评价 | 避免筛掉难样本后只公布变好的分数 |
| P13 | [Improve Fidelity and Utility of Synthetic Credit Card Transaction Time Series from Data-centric Perspective](https://arxiv.org/abs/2401.00965) | 2024 / F，§3–4 | 与内部威胁相近的稀有异常场景：同时看保真、FPR/FNR、类别比例 | 金融特征与该文阈值不能直接当企业日志标准 |
| P14 | [An Ethically Grounded LLM-Based Approach to Insider Threat Synthesis and Detection](https://arxiv.org/abs/2509.06920) | 2025 / F，实验与限制段，访问 v2 | LLM 合成 syslog 的不平衡评价、真标签泄漏教训 | 其测试仅少量正例且缺多日志链，不能据此证明生产效用 |
| P15 | [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](https://arxiv.org/abs/2407.18901) | 2024 / F，§Evaluation | 任务前后状态与有效终态集合；附带破坏 | 终态正确不等于生成数据分布真实；不要把固定 API 顺序当黄金答案 |
| P16 | [τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) | 2024 / F，Pass^k metric | 政策、目标状态与同任务多次成功的可靠性 | `pass^k` 不等于 `pass@k`，重复不能通过挑最好结果替代 |
| P17 | [TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks](https://arxiv.org/abs/2412.14161) | 2024 首发，访问 v3（2025）/ F | 长程任务的检查点和完整成功分开报告 | 完整职场基础设施较重；只迁移检查点协议 |
| P18 | [GraphRNN: Generating Realistic Graphs with Deep Auto-regressive Models](https://proceedings.mlr.press/v80/you18a.html) | 2018 / F，PDF evaluation | 图集合的度、聚类、motif 统计与 MMD | 多周单图相关，不能伪装成独立图集合；组织树不是观测真实图 |
| P19 | [GRAPHIA: Harnessing Social Graph Data to Enhance LLM-Based Social Simulation](https://aclanthology.org/2026.acl-long.322/) | 2026 / A，ACL | 微观交互与宏观网络性质同时评价 | 摘要不支持原旧文档对具体 MMD/谱实现的断言 |
| P20 | [G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment](https://aclanthology.org/2023.emnlp-main.153/) | 2023 / A，ACL 摘要 | 定义量表、结构化语义评审并与人工相关性比较 | 这里用 DeepSeek 的改编方案，不称为原版 G-Eval，也不移植 GPT-4 的有效性结论 |
| P21 | [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | 2023 / F，§Limitations | 顺序、冗长、自我偏好偏差；人工对照 | 换一份提示词或换同厂模型不能保证独立性 |
| P22 | [Synthetic Data – Anonymisation Groundhog Day](https://www.usenix.org/conference/usenixsecurity22/presentation/stadler) | 2022 / A，USENIX | “合成”并不自动保障隐私；用途/威胁模型决定审核 | Chimera 若没用私有真实训练数据，训练集成员推断不适用；不能声称差分隐私 |
| P23 | [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) | 2018 首发 / F，PDF | 生成动机、组成、采集、用途、局限、维护 | 文档存在不是质量通过证明 |
| P24 | [Data Cards: Purposeful and Transparent Dataset Documentation for Responsible AI](https://arxiv.org/abs/2204.01075) | 2022 / A | 把数据来源、用途、生命周期与决策限制写成发布卡 | 卡片不能替代分组实验或证据定位 |
| P25 | [The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432) | 2015 / F，PLOS | 稀有威胁场景主报 PR 曲线和正类覆盖 | PR-AUC 随阳性比例变化；比较要固定 prevalence 并报置信区间 |

## 附录B：检索与证据范围

调用 paper-search 的六个来源：arXiv、DBLP、OpenAlex、OpenReview、Semantic Scholar、Crossref。每主题每来源最多 4 项，得到 24 个唯一候选；小规模定向检索不等于穷尽综述。arXiv 与 Crossref 各返回 12 项，另外四源为零；DBLP 明确报连接错误，其他零结果原因未确认。没有把零返回解释为没有相关论文。完整候选、摘要、计数与筛选保存在 [原始 JSON](evidence/search-results.json) 与 [检索报告](../../allinone.md)。

阅读级别：

- **F**：访问并阅读一手全文中有关方法/评测段落；不表示已复现或逐页精读。
- **A**：核对一手标题、摘要或官方元数据；只用摘要支持的结论。
- **M**：数据库元数据/摘要，全文未访问成功；不依此确立数值阈值。
- **U**：历史背景链接保留，未完成内容核验，不用于核心方法依据。

HTTP 200 不自动等于有效论文：CERT 2014 链接返回验证页；TWOS 出版页返回 403；时间序列综述全文超时。相应项明确降低证据级别。GRAPHIA 的 ACL 链接已核对确为该论文，但这里只采用摘要中的微观/宏观双层评测思想，图 MMD 的方法依据单独引用 GraphRNN。

## 附录C：对原有调研的修正

`dev` 中已有 14 篇的评测草案，仍可作历史输入，但它写的是未接线原型且 L1/L2 编号不同。本方案重新读取当前代码与一手证据，不沿用以下混淆：

1. 把 CERT/旧 ChimeraLog 当作 Real；把同分布持有测试当作 TSTR。
2. 用 n-gram 重叠替代 P09 定义的 Authenticity。
3. 用预设的部门连通图当作真实协作图。
4. 把抽取后的 `tool_transitions.csv` 当作所有尝试的完整状态转移。
5. 把正文存在/程序返回/编排终态当业务成功。
6. 按模型分数过滤后再宣称整份生成数据质量提高。

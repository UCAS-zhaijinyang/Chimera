# 第一阶段实施与验收计划

> 执行方式：本会话直接实施，按 `superpowers:executing-plans` / TDD 执行；用户已授权评测、修复、保存每轮报告并推送当前分支，不再增加确认步骤。

**Goal:** 实现并执行 L0.1–L0.8，保留失败轮次，修复当前 workflow 采集/标注链，再进行真实 DeepSeek 验证并推送远端。

**Architecture:** 标准库实现独立评测器，以不可变 study manifest、原始日志、产物字节及独立标签fixture为依据。runtime 增加采集sidecar；现有工具接口保持兼容。报告写入新的轮次目录，不覆盖旧报告。

**Tech Stack:** Python 3.10+、pytest、现有FilesystemToolRuntime；DeepSeek官方API仅用于最后真实链路。

**Spec:** [framework.md](framework.md) 的 L0.1–L0.8、[implementation-plan.md](implementation-plan.md) 第一阶段与黄金任务定义。

## 全局约束

- 当前 `research/dataset-evaluation-framework` 是用户已选研究分支，工作树干净；在此分支实施与推送，不另建任务分支。
- 不改评测通过条件；坏行、丢失、拒绝、HTTP错误、timeout、提前结束和unknown均可追溯。
- 仿真邮件/审批与真实系统/网络证据分开；没有真实采集的模态标NOT_MEASURED，不冒充全模态通过。
- 凭证只在临时文件与请求内存中使用；报告、日志及提交不含凭证，不发送真实邮件。
- 使用 `.venv/bin/python`；现有55个pytest测试是回归基线。全套命令 `PYTHONPATH=src .venv/bin/python -m pytest -q`。
- 每次实际评测生成独立目录 `docs/dataset-evaluation/reports/stage1/<round>/`，包含manifest、指标/失败、故障注入结果、执行信息及压缩原始证据；不删除失败轮次。
- paid请求记录实际model/usage/失败；模型能力不影响确定性检查，不能将模型自报完成当真值。

## Review Focus

- 复制日志及跨run同trace：去重只合并相同源事件，不能合并身份冲突或重复执行。
- 不合法JSON、空输入、缺文件：进入分母/错误清单，不能因没读到记录而记100%。
- 工具或模型异常：started/terminal闭合，异常日志在finally中保留，unknown不能改正常。
- 文件被篡改、覆盖、路径越界：按不可变版本hash与输入边检查，不读工作区外文件。
- 攻击意图与实际动作：独立fixture指定可观察目标，依执行状态和证据验证标签，不由attack描述生成阳性。

## Task 1: 独立评测器与初始失败报告

Files: `src/evaluation/trust.py`, `src/evaluation/__init__.py`, `tests/test_dataset_trust.py`, `scripts/evaluate_dataset_trust.py`。

Interfaces: `evaluate_study(study_dir) -> dict` 返回8项metric及evidence/failures；`write_report(study_dir, report_dir, report)`拒绝覆写旧报告。CLI `--study PATH --report PATH`，核心失败退出1，输入错误仍保存报告。

- [x] 先写手工已知真值fixture测试：字段/关联/守恒/血缘/因果/标签/对齐/泄漏，以及损坏、重复、空/缺文件、越界和分母0。
- [x] 运行新测试观察RED，保存输出；实现评测器，运行GREEN与既有回归。
- [x] 用现有未改runtime生成90条黄金轨迹，运行评测器，保留第一轮FAIL报告及原始证据。
- [x] 提交独立评测器、测试与初始报告。

## Task 2: 修复runtime、产物及导出采集链

Files: `src/workflow_runtime.py`, `src/tool_composition.py`, `src/tool_log_extractor.py`, `src/task.py`, `src/planning_schedule.py`, `src/daily_plan_generation_auto.py` 与对应tests。

Interfaces: workflow接受可选 `context`（run/task/plan/member/phase/day/simulation_time），事件带唯一event/call和序号/时间；产物manifest带version/hash/created_at/root与input边；extractor提供lossless审计读取，原公共导出保持兼容；schedule写独立activity sidecar。

- [x] 用第一轮失败逐项写回归测试，先RED；按根因修复，每个模块GREEN后运行全套。
- [x] 保留提前final/拒绝/工具失败/HTTP错误/timeout/多调用的完整生命周期；失败任务仍复制日志。
- [x] 不允许损坏manifest静默读取或重复artifact ID覆盖；开发/test/build补真实输入链并记录returncode，不将失败命令算成功。
- [x] 保留计划导出旧Time/Activity，另写稳定planned_activity_id关联sidecar，执行入口读取该sidecar。
- [x] 完成90黄金轨迹、360员工日离线多日采集回归与至少每类3个独立故障挑战；记录每轮报告，修复至核心检查通过。
- [x] 提交修复和报告，运行全套回归。

## Task 3: 真实DeepSeek、终验与推送

Files: `src/task.py`, `scripts/run_dataset_trust_campaign.py`, tests及报告索引。

Interfaces: 客户端使用显式DeepSeek型号/输出限制、保存response usage而保持message返回接口；失败不记录响应中的敏感凭证；campaign `--mode offline/live --round ID` 不覆盖轮次，保留原始日志和收费账本。

- [x] 先测试真实HTTP边界（本地HTTP fixture覆盖usage/错误/超时/输出截断），RED→GREEN。
- [x] 真实DeepSeek执行三工作流30任务×3重复；所有失败保留，问题修复后新轮次复测。付费调用使用用户提供凭证，预算按stage1账本核算。
- [x] 保存逐项指标、原始证据、模型用量、故障检出/正常误报、全套测试输出；清楚列出系统/网络/真实邮件未测能力。
- [x] 进行一次独立代码审查，重要问题加回归测试修复，再运行全套及最终评测。
- [x] 检查提交无凭证、工作树与远端状态；提交全部修改与报告，`git push -u origin research/dataset-evaluation-framework`；核对远端commit。

## 执行记录

2026-10-12：系统python无pytest且不是项目环境；改用已存在的`.venv`。正确项目命令基线55 passed，5个依赖库弃用警告。远端可读，研究分支尚不存在。用户已提供真实API凭证，临时文件权限0600，未写入仓库。

Ruling: 报告中的通过范围限定当前workflow应用仿真采集；真实系统/网络/外发缺能力维持未测。这是已批准指标的能力边界，不能为凑全部PASS伪造pcap或真实发送。

2026-10-12 实施记录：Task 1已提交67f16da；round01失败1,341项记录保留。Task 2修复身份、schema、调用生命周期、hash/version、血缘、plan sidecar、无损抽取及Fixture误路由。round07黄金90轨迹、round09多日720任务/360员工日均PASS；round13扩展25类故障×3共75样本全部检出，3正常对照误报0。

Task 3：真实HTTP边界测试覆盖输出cap、thinking、usage、error redaction、timeout、缺message与截断。DeepSeek-flash真实轨迹按30模板×3重复运行；长运行受TLS中断与预算守卫影响，round06/10/12保留失败及未知，不将其用作完整90轨迹验收；改为按variant分批，全部原始失败仍在各批次报告。独立审查7项Important已经RED→GREEN修复，完整记录见reports/stage1/verification/independent-review.md。最终API汇总、完整回归、费用以及远端提交以reports/stage1/README.md为准。

Ruling: 实际API测试variants6–8在真实请求返回后注入已知故障，variant9按任务目标自然执行。这样测试的是记录契约，不据这些样本宣称模型自然攻击能力；如果误用于攻击能力比较会产生偏差，因此报告和账本明确记录。

Ruling: 出现TLS连接错误时采用分批/serial重跑以完成同样30模板×3次数，原轮次与未知收费保留，不挑选成功子轨迹。代价是增加重复请求；已按实际usage入账，未改变验收阈值。

Final review：fresh independent reviewer；7 Important已分别复现RED并修复GREEN，无Minor遗留。审查拒绝评价的真实采集、业务语义、真实性、检测效用已裁定留第二/三阶段；价格按实际官方信息核算，凭证隔离继续执行。

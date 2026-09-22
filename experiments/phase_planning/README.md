# 业务阶段计划：示例与历史实验

正式入口已迁入 `src/`，按根目录 README 的 Phase 1 分步运行。会议、会议产物整理和日计划是三个独立程序，分别通过文件交接，不经过周计划。

## 当前运行方法

`company.json` 是与行业无关的接口示例：软件公司的合成目标、3 个部门、6 名员工、12 个工作日，每人每天最多 8 小时。它没有预设阶段数量、名称或天数，这些由负责人会议讨论决定。换成其他公司的组织、画像、目标和工作日即可使用同一入口。

从仓库根目录运行（已激活 Python 环境，并在 `src/config.py` 配好模型）：

```bash
# 只检查输入和参会名单，不调用模型
python src/meeting_for_phase_goal_auto.py --company experiments/phase_planning/company.json --dry-run

# 程序一：负责人会议 → 并行部门会议 → 保存会议产物
python src/meeting_for_phase_goal_auto.py \
  --company experiments/phase_planning/company.json \
  --output experiment_output/phase_example/meeting_logs --key-stdin

# 程序二：从会议产物生成每人每阶段计划
python src/phase_plan_generation_auto.py \
  --meetings experiment_output/phase_example/meeting_logs \
  --output experiment_output/phase_example/meeting_logs/phase_plans.json

# 只读检查；也应人工检查阶段目标、责任和估计工时
python src/planning_audit.py --plans experiment_output/phase_example/meeting_logs/phase_plans.json

# 程序三：只读取已保存阶段计划，生成每日活动与执行文件
python src/daily_plan_generation_auto.py \
  --plans experiment_output/phase_example/meeting_logs/phase_plans.json \
  --output experiment_output/phase_example/init_schedule --key-stdin

python src/planning_audit.py \
  --plans experiment_output/phase_example/meeting_logs/phase_plans.json \
  --schedules experiment_output/phase_example/init_schedule
```

`--key-stdin` 隐藏读取凭据；也可设置 `CHIMERA_PLANNING_API_KEY` 或供应商环境变量。凭据不进入任务配置和调用日志。相同输入可加 `--resume` 继续，修改输入应使用新输出目录。日计划的 `--batch-days` 只限制单次输出规模，不规定业务阶段长度。

## 实现与产物

负责人会议使用 CAMEL Workforce，为每位部门代表建立独立智能体，依据公司目标、实际人数、可用工时和总工作日讨论阶段名称、持续天数、部门任务及交接。各部门随后在独立进程中并行开会，讨论每位员工在各阶段的目标。会议程序只保存 `company.json`、每场会议的输入和 `meeting_result.log`。

`phase_plan_generation_auto.py` 仅读取这些会议产物，验证负责人会议结果与所有部门会议结果，组装出完整的 `phase_plans.json`。它不重新开会，也不依赖原始员工画像目录；缺少或修改会议结果时不会静默生成旧计划。

每场会议的完整背景进入员工智能体上下文；日期或引用冲突会连同原提案退回参会者重新讨论，最多 `planning_meeting_rounds` 轮。JSON 解析不通过另一个模型改写决策。复用原周会议程序的画像加载及日志函数，原周计划入口和画像生成程序保持不变。

独立日计划程序读取完整 bundle 中的公司、画像、阶段和个人目标，按员工与阶段生成连续工作日的活动。长阶段分批生成，后续批次携带此前日计划。校验失败反馈原输出和具体错误，尝试记录保留。

| 当前产物 | 用途 |
|---|---|
| `meeting_logs/company.json` | 会议阶段使用的完整公司和画像快照 |
| `meeting_logs/meetings/<会议>/` | 参会画像、输入、原始输出和日志 |
| `meeting_logs/phase_plans.json` | 独立计划生成阶段发布的完整交接文件：`company`、`phase_plan`、`personal_plans`、`schema_version` |
| `init_schedule/daily/<阶段>/<员工>.json` | 个人整个阶段的逐日活动 |
| `init_schedule/chunks/` | 可续跑的批次及尝试记录 |
| `init_schedule/workdays/day_001/<员工>.json` | 全局工作日的活动与依赖 |
| `init_schedule/week_N/<员工>_week_N_Day.json` | 现有执行程序使用的 `Time` / `Activity` 数组 |
| `init_schedule/calendar.json` | 业务工作日与旧执行文件索引的映射 |
| `init_schedule/completed.json` | 全部产物通过结构审计后发布的标记 |

`week_N` 和星期名只是执行程序的存储索引：第 6 个工作日映射为 `week_2/Monday`。业务阶段由其持续天数决定，可以跨越该索引边界。

阶段天数必须覆盖总工作日；每人每阶段必须有目标；任务引用必须属于相应部门和阶段；日计划必须覆盖相应工作日且不超工时。交付发生在工作日结束，最终产物只能在之后的工作日使用。`requires_handoff_ids` 表示约定的输入交接，`uses_deliverable_ids` 表示额外读取的共享最终产物。

这些校验不证明目标语义完整、工时估计合理或计划最优。当前版本要求顺序阶段、每个部门每阶段有任务、每名员工每阶段有目标；休假、非全时员工、并行阶段尚未建模。

## 历史证据与本次重构验证

[RESULTS.md](RESULTS.md) 记录重构前的真实 DeepSeek 实验及内容问题，旧命令与旧文件布局只用于解释历史。`experiment_output/phase_planning_run1` 至 `phase_planning_run4` 保留不动，旧耦合实验脚本已删除。

重构回放结果在 `experiment_output/phase_pipeline_replay/`：三个程序分别在独立进程中运行，复用 run4 的原始会议与日计划响应。得到 3 个阶段、18 份个人阶段计划、72 份执行日文件、576 人时，结构审计通过。回放测试禁用网络，没有新增 API 调用；它验证新程序的编排与文件接口，不是新的模型质量实验。

可重复验证：

```bash
python -m pytest -q
python tests/support/replay_planning.py meetings experiment_output/phase_planning_run4 \
  --company experiments/phase_planning/company.json \
  --output experiment_output/phase_pipeline_replay/meeting_logs --resume
python tests/support/replay_planning.py phase_plans experiment_output/phase_planning_run4 \
  --meetings experiment_output/phase_pipeline_replay/meeting_logs \
  --output experiment_output/phase_pipeline_replay/meeting_logs/phase_plans.json --resume
python tests/support/replay_planning.py daily experiment_output/phase_planning_run4 \
  --plans experiment_output/phase_pipeline_replay/meeting_logs/phase_plans.json \
  --output experiment_output/phase_pipeline_replay/init_schedule --batch-days 2 --resume
```

历史环境依赖见 `../leadership_planning/requirements.txt` 和 `requirements.lock`。本机使用公开 PyPI `camel-ai==0.2.45`；仓库定制发行包此前下载返回 403，未验证其专有日志行为。未运行 Phase 2/3 模拟。

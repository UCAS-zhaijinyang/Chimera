# 已归档：负责人会议与部门周计划实验

本目录保留最初按周实验的输入、依赖版本和 [RESULTS.md](RESULTS.md)。它不满足后来明确的“负责人依据公司目标、人数和总工作日，决定阶段名称与持续天数”的需求。

对应的旧实验程序和周计划批量生成程序已删除。历史结果及原始模型响应仍保留在 `experiment_output/`，用于对照；历史报告中的命令不再是当前运行入口。

当前流程见 [业务阶段示例](../phase_planning/README.md) 和根目录 [README](../../README.md)：

1. `src/meeting_for_phase_goal_auto.py --stage leadership`：负责人会议，只保存会议产物。
2. `src/phase_plan_generation_auto.py --stage departments`：读取负责人会议产物，生成各部门阶段计划。
3. `src/meeting_for_phase_goal_auto.py --stage departments`：读取部门阶段计划，召开部门会议并保存会议产物。
4. `src/phase_plan_generation_auto.py --stage employees`：读取部门会议产物，生成每人每阶段计划。
5. `src/daily_plan_generation_auto.py`：读取员工阶段计划，生成日计划及现有执行程序可读的文件。
6. `src/planning_audit.py`：只读核验阶段计划及日计划产物。

`src/profile_generation.py` 与 `src/meeting_for_weekly_goal_auto.py` 保持原样；后者作为兼容入口和会议辅助函数来源保留，不作为新流程的周计划中间层。

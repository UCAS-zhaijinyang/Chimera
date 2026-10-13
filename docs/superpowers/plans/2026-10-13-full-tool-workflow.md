# 完整工具工作流修复计划

规格：../specs/2026-10-13-full-tool-workflow-design.md

1. `src/base_tools.py` 提供共用 `create_base_tools(workspace, offline, models=None)` 与 lazy registry；`src/task.py` 旧路径使用同一注册器。测试文件/终端真实操作、schema、错误返回。
2. `src/workflow_runtime.py` 添加显式 `workflow_id`、通用状态机、基础工具注册与产物日志；`src/task.py` 生产接线 general、共享业务目录，三业务评测维持严格路由。测试任意任务能操作真实文件并完成，非零命令不通过，结构化流程不提前完成，日志成对，跨任务文件可见。
3. `src/daily_attack_schedule.py` 保留全步骤与解析失败完整性。测试完整提示与无效日程不落盘。
4. 运行完整回归与独立业务队列；新增基础工具/15类原版步骤的隔离实工具检查，真实 DeepSeek 复测，保留每轮报告、原始证据及完整费用。独立代码审查与验收对照，修复未通过项再测，提交并推送。

每项先写行为测试，保存失败日志再修复，运行针对性与全量测试。验收不能降低或将未运行项标记为通过。

Review focus：关键词误分类、共享路径侵入采集证据、后台进程错误被吞掉、浏览器嵌套调用成本遗漏、旧工具补丁版本不能核验。

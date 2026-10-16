# Q1 阶段偏差旁证

每个员工的阶段计划从对应上游会议产物独立抽取：O 使用原始 weekly meeting 的 `meeting_result.log`，N 使用当前框架员工阶段计划 `phase_plans.json`。随后将日程事件的 `week_N` 与旁证中的员工阶段映射逐条比较。

主报告中的 `phase_deviation` 包括有符号平均偏差、平均绝对偏差、最大绝对偏差、精确阶段率、错配率、分母和 Wilson 95% CI。`UNKNOWN` 事件保留在 `coverage` 中，不能被当成通过。

两个 JSON 文件包含源文件 SHA-256、旁证内容哈希和每个员工的阶段映射；它们不读取生成后的日程作为计划来源。

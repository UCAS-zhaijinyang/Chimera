# Q5 攻击实际副作用评测

每个 O/N campaign 都在独立 AttackLab 中执行相同 canonical attack case。
`evaluate_lab` 读取文件、账号、日志、数据库和 HTTP 状态判定副作用；计划记录或命令返回码不构成成功证据。

## 指标

- `execution_success_rate`：步骤产生独立 oracle 预期副作用的比例。
- `execution_block_rate`：已执行但未产生预期副作用的比例。
- `target_reachability`：攻击步骤实际达到其 canonical 目标状态的比例。
- `oracle_coverage`：拥有可核验 oracle 状态的步骤比例；无 oracle 证据的步骤不会被计为成功。
- `unknown_rate`：无法由 oracle 判定的步骤比例。
- `ordered_episode_success_rate`：按 canonical 顺序全部通过的 campaign 比例。

这是受控合成实验室中的真实状态副作用测量，不声明真实企业系统或真实攻击能力。

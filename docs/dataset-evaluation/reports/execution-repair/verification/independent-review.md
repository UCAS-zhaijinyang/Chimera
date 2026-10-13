# 独立只读审查记录

审查基线：faf6b89ba464606a8366b12a2bac049f8aea3a4c；研究分支工作树。审查者只读，没有修改共享仓库或发起付费调用。审查与修复往返全部在同一任务完成。

## 发现与解决

| 级别 | 问题 | 证据及解决 |
|---|---|---|
| Important | 多文件存在检查允许空helper/空test和未调用helper的main通过 | 复现空文件反例；增加辅助函数隐藏行为、sentinel依赖检查与unittest执行 |
| Important | 覆盖整个main导致导入错误被误算为测试检出业务错误 | callable(mean_values)测试反例；仅替换原模块compute行为，必须断言失败且errors=0 |
| Important | 删除失败execution_result行可缩小分母获得PASS | 正常任务清单保留但result缺失反例；两套验收先严格一对一Counter验证，缺失/重复/未知全FAIL |
| Minor | pilot与过滤后case列表不兼容 | CLI提前拒绝pilot+probe/normal-only/variant，未写study |
| Minor | 启动快照在campaign结束后才落盘 | 执行前独占创建/fsync sibling snapshot，workers=0异常仍有可审计快照 |

## 最后独立验证

13项business测试通过；另外针对运行时/HTTP/流程的一组36项测试通过。协调者最后全量150项通过，完整日志留存。

从最终archive独立解压并使用最终检查器：round23正常54/54编排和业务通过、27/27控制通过；round24正常54/54编排通过，业务语义NOT_MEASURED。逐一验证11个live archive hash及账本，4,033条唯一started与4,033条terminal一一对应，已知峰值费用$2.659028472，未知usage0。

结论：没有未解决Critical/Important或延期Minor，适合交付当前声明的本地业务fixture/模拟应用范围。评测器最后增强分母检查后，对原证据独立复验，不能把复验算作新生成；原始任务模糊组业务语义必须保持NOT_MEASURED。

## 明确未裁定

真实企业数据/邮件/审批、任意缺陷输入、恶意代码规避检查器、系统/网络采集与跨任务协作、通用真实性和威胁检测效用、永久无缺陷。它们超出本轮指定应用fixture，不能把本轮通过作为这些能力的证据。

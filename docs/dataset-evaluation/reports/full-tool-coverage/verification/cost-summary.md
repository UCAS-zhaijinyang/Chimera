# 本轮完整工具修复费用

费用包括失败轮次和探针；按峰值 token 价估算，未知 usage 的发送后错误保留上界，不是供应商账单。每份唯一总账仅计一次。旧阶段一和旧 execution-repair 的费用另列，不能误读为项目累计费用。

| 轮次 | 请求 | 已知 usage 估算 USD | 未知 usage 保留 USD | 上界 USD |
|---|---:|---:|---:|---:|
| [round-04-live-business](../round-04-live-business/) | 524 | 0.373381668 | 0.000000000 | 0.373381668 |
| [round-08-live-business](../round-08-live-business/) | 584 | 0.415717812 | 0.000000000 | 0.415717812 |
| [round-09-live-native-lab](../round-09-live-native-lab/) | 377 | 0.228099840 | 0.000000000 | 0.228099840 |
| [round-12-vision-probe](../round-12-vision-probe/) | 1 | 0.000067500 | 0.000000000 | 0.000067500 |
| [round-15-live-business](../round-15-live-business/) | 590 | 0.319869708 | 0.304915200 | 0.624784908 |
| [round-16-live-native-lab](../round-16-live-native-lab/) | 283 | 0.112546632 | 0.000000000 | 0.112546632 |
| [round-17-browser-capabilities](../round-17-browser-capabilities/) | 10 | 0.009640008 | 0.000000000 | 0.009640008 |
| [round-19-live-native-lab](../round-19-live-native-lab/) | 276 | 0.163044900 | 0.304915200 | 0.467960100 |
| [round-20-live-business](../round-20-live-business/) | 591 | 0.409934316 | 0.304915200 | 0.714849516 |
| [round-22-live-final-native](../round-22-live-final-native/) | 314 | 0.161144688 | 0.609830400 | 0.770975088 |
| [round-23-live-final-business](../round-23-live-final-business/) | 625 | 0.399443256 | 0.609830400 | 1.009273656 |
| [round-26-live-final-business](../round-26-live-final-business/) | 581 | 0.415242444 | 0.000000000 | 0.415242444 |
| [round-27-live-final-native](../round-27-live-final-native/) | 269 | 0.170171976 | 0.000000000 | 0.170171976 |

总计 5025 次请求，已知 usage 估算 $3.178304748，未知 usage 保留 $2.134406400，合计上界 **$5.312711148**。

Brave 当前尚未发起真实请求，搜索费用 $0。后续验收最多6次搜索，按 $5/千次计，免费额度抵扣前上界 $0.03；与模型费用分账。

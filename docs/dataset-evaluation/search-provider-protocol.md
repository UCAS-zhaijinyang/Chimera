# 两套框架的统一搜索方案

2026-10-13，用户明确要求两套框架不再使用 Google，并选择 Brave Search API。此变更同时应用于原版执行路径和新工作流；比较对象应称为“原版 Chimera 编排＋共同搜索适配器”与“新框架＋共同搜索适配器”，不是声称完全不修改作者发布环境。

## 为什么选择 Brave

| 方案 | 能力与费用 | 本机核验 | 判断 |
|---|---|---|---|
| Brave Search API | 独立网页索引，网页/图片/视频搜索；官方当前 $5/千次请求，每月 $5 免费额度 | 官方文档可达；真实 API 尚缺 key | 用户选定，待真实验收 |
| DuckDuckGo | 无搜索 API 单次费用 | 旧库网页/图片失败，视频成功；HTML 页面真人挑战，未绕过 | 不作为正式默认 |
| Bing 网页 | 无正式搜索 API 接入 | HTTP 200，但无可解析结果 | 不能用响应码冒充可用 |
| Brave 公共网页 / Mojeek 网页 | 网页搜索 | 分别 HTTP 429 / 403 | 不采用网页抓取作为可靠接口 |
| 自建 SearXNG | 可禁用 Google，提供统一 JSON API；有部署成本 | 文档可达，未部署；仍依赖上游引擎 | 备选，不能声称已通过 |
| Tavily | 每月1000免费 credits，按量 $0.008/credit；搜索 basic 1 credit / advanced 2 credits | 官方文档核验，未调用 API | 有额度但并非独立索引对等替换，未选用 |

官方依据：

- [Brave 产品与价格](https://brave.com/search/api/)
- [Brave 网页搜索](https://api-dashboard.search.brave.com/documentation/services/web-search)
- [Brave 图片搜索](https://api-dashboard.search.brave.com/documentation/services/image-search)
- [Brave 视频搜索](https://api-dashboard.search.brave.com/documentation/services/video-search)
- [Tavily 价格与 credits](https://docs.tavily.com/documentation/api-credits)
- [SearXNG 搜索 API](https://docs.searxng.org/dev/search_api.html)

价格核验日期为2026-10-13，正式生成前再核验当前套餐。这里采用普通搜索端点，不调用 Brave Answers 或其他生成模型；所有模型推理继续使用 DeepSeek。

## 实际接入

`src/search_runtime.py::search_brave(query, source, max_results)` 是共同适配器。`source` 为 text/images/videos，`max_results` 为1–20。固定 country=us、search_lang=en、safesearch=strict、spellcheck=false；两源均不得单独改动这些参数。每调用至多一次 HTTP 请求，没有自动重试、Google 回退或其他引擎回退。

`BaseToolRegistry` 同时用于旧 OWL/Camel 路径和新工作流，统一注册 search_brave。随机浏览与周计划也使用该函数。原作者11工具的历史核验保留；当前把两项搜索注册合为一项，现有基础注册数为10，搜索类别仍有网页/图片/视频。原原生文件/终端/浏览器接口保留。

认证只从私有 `BRAVE_SEARCH_API_KEY` 环境读取，DeepSeek key 不能替代。认证缺失在网络提交前失败；HTTP限流/认证错误/服务错误、传输失败、畸形响应明确失败，不能当作搜索结果。成功结果含 provider/query/source/request_count 与真实来源 URL、摘要、图片来源或视频元数据；空结果明确为空，不代表检索任务完成。新流程将结果作为观察产物留档，搜索 token 不写入响应或日志。

## 公平对比和成本

正式两源使用同一模型、搜索适配器版本、参数、每任务搜索额度和每run总额度。框架生成的查询允许不同，因为查询策略本身属于方法差异；不得给一方更多额度或不同引擎。搜索调用单列费用，不能混入 DeepSeek token 账。

正式生成前还需实现并冻结共用搜索网关/缓存：以 provider、完整查询、类别、所有搜索参数及冻结时间段作为缓存键；同一查询返回同一份结果并记录内容 hash。公开轨迹须去除认证和直接标签泄漏。当前共享适配器已接入，但网关/缓存和正式两源采集联测尚未实现，不能声称已经排除所有动态索引差异。

设同一计费账户每月发起 Q 次实际搜索请求，按当前价格，免费抵扣前费用为 **$0.005×Q**；若该月 $5 免费额度完整可用且没有其他消费，则约为 **max(0, $0.005×Q−$5)**。例如1000次约$0，5000次约$20，10000次约$45。缓存命中不再发起请求；不同来源、重试或失败请求可能计费，按供应商账单核对。69,120模拟员工小时是工作容量，不能据此推算搜索请求数。

## 验收

离线测试覆盖三种端点的参数和解码、输入校验、认证缺失、301/401/429/500、畸形响应、旧FunctionTool与新workflow观察/终态。它们是 provider contract 测试，不是实际服务成功证据。

真实验收脚本 `scripts/check_brave_search.py` 对3类搜索分别走旧注册调用与新工作流，共至多6次搜索，免费抵扣前预算上界 **$0.03**，无需模型 API。控制调用是预写测试，不宣称模型自然检索质量；要求真实非空结果、合法来源 URL、工作流闭合及真实结果记录。报告目录独占创建，任何失败保留整轮，不覆盖旧报告。当前[round31](reports/full-tool-coverage/round-31-brave-provider-check/report.json)为 NOT_MEASURED：尚无 Brave key，0次搜索、$0。历史 Google 缺认证不再是当前验收条件；新 Brave 的真实验收仍是当前条件。

配置私有环境后运行：

```sh
PYTHONPATH=src .venv/bin/python scripts/check_brave_search.py --report /tmp/NEW-brave-report --key-file /path/to/private/brave-key
```

不把密钥放入命令行参数值、源码、报告或提交。正式原版隔离checkout还须接入同一适配器并完成端到端联测；本分支旧执行入口的接入不替代该验收。

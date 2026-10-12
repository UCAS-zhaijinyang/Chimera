# 生成数据集评测检索记录

检索日：2026-10-12；近期窗口2024–2026；每查询每来源最多4项。三个查询：`synthetic data evaluation`、`synthetic time series evaluation`、`insider threat dataset`。本报告完整列出保留结果；领域基础追溯见[25项参考文献](docs/dataset-evaluation/literature-review.md)。

来源计数：arXiv=12，Crossref=12，DBLP=0，OpenAlex=0，OpenReview=0，Semantic Scholar=0。24项唯一记录，0跨来源重复；5项按已读摘要判无关；19项保留（含摘要缺失/待核验项）。保留并不表示采纳为最终方法。引用数为API返回快照，arXiv的0不是已核实无引用。

## 保留结果（CLI lexical排序顺序）

| # | 论文链接 | 年份 | Venue | API引用数 | Score | 来源 | 语义筛选/使用范围 |
|---|---|---|---|---:|---:|---|---|
| 1 | [Evaluation of Machine Learning Techniques for ESP Diagnosis Using a Synthetic Time Series Dataset](https://doi.org/10.2523/iptc-24210-ms) | 2024 | International Petroleum Technology Conference | 2 | 6 | crossref | domain example of utility on synthetic fault data, secondary only |
| 2 | [Why Do Class-Dependent Evaluation Effects Occur with Time Series Feature Attributions? A Synthetic Data Investigation](http://arxiv.org/abs/2506.11790v2) | 2025 | arXiv | 0 | 6 | arxiv | known synthetic ground truth exposes invalid evaluation proxies |
| 4 | [Data-Efficient Sleep Staging with Synthetic Time Series Pretraining](http://arxiv.org/abs/2403.08592v2) | 2024 | arXiv | 0 | 5 | arxiv | synthetic-to-human task transfer example, secondary only |
| 5 | [Improve Fidelity and Utility of Synthetic Credit Card Transaction Time Series from Data-centric Perspective](http://arxiv.org/abs/2401.00965v1) | 2024 | arXiv | 0 | 5 | arxiv | fidelity and rare-event detection utility |
| 6 | [An Ethically Grounded LLM-Based Approach to Insider Threat Synthesis and Detection](http://arxiv.org/abs/2509.06920v2) | 2025 | arXiv | 0 | 5 | arxiv | direct insider-threat synthesis, imbalance and leakage |
| 7 | [Synthetic data improves survival model evaluation under distribution shifts](https://doi.org/10.2139/ssrn.6283638) | 未知 | 未知 | 0 | 5 | crossref | synthetic evaluation under distribution shift; clinical-domain secondary |
| 8 | [Dynamic Linear Coregionalization for Realistic Synthetic Multivariate Time Series](http://arxiv.org/abs/2604.05064v2) | 2026 | arXiv | 0 | 4 | arxiv | temporal cross-channel dynamics and transfer utility |
| 10 | [A Synthetic Data Generator for Cluster and Label Matching Evaluation](https://doi.org/10.2139/ssrn.7268626) | 未知 | 未知 | 0 | 4 | crossref | controlled label/cluster synthesis, secondary |
| 11 | [PPMI-Benchmark: A Dual Evaluation Framework for Imputation and Synthetic Data Generation in Longitudinal Parkinson's Disease Research](https://doi.org/10.5220/0013649700003967) | 2025 | Proceedings of the 14th International Conference on Data Science, Technology and Applications | 4 | 3 | crossref | abstract unavailable; retained pending verification |
| 12 | [AeroGen: Enhancing Remote Sensing Object Detection with Diffusion-Driven Data Generation](http://arxiv.org/abs/2411.15497v3) | 2024 | arXiv | 0 | 3 | arxiv | synthetic augmentation and independent downstream utility, vision-domain secondary |
| 13 | [TerraGen: A Unified Multi-Task Layout Generation Framework for Remote Sensing Data Augmentation](http://arxiv.org/abs/2510.21391v1) | 2025 | arXiv | 0 | 3 | arxiv | multitask generation and downstream utility, vision-domain secondary |
| 14 | [Synthetic Data in MR Spectroscopy: Current Practices, Applications, and Considerations](http://arxiv.org/abs/2602.23463v2) | 2026 | arXiv | 0 | 3 | arxiv | synthetic data evaluation practices; domain-specific secondary |
| 16 | [Towards Using Synthetic User Interaction Data in Digital Healthcare Usability Evaluation](https://doi.org/10.5220/0012427600003657) | 2024 | Proceedings of the 17th International Joint Conference on Biomedical Engineering Systems and Technologies | 0 | 3 | crossref | abstract unavailable; retained pending verification |
| 17 | [Gentle introduction to linear algebra – synthetic time series](https://doi.org/10.1016/b978-0-44-321857-6.00007-2) | 2024 | Synthetic Data and Generative AI | 0 | 3 | crossref | abstract unavailable; textbook chapter pending verification |
| 18 | [Insider Threat](https://doi.org/10.4324/9781003055716) | 2024 | 未知 | 1 | 2 | crossref | abstract unavailable; book/background not core paper |
| 21 | [Insider threat determinant: The MOCR Theory](https://doi.org/10.2139/ssrn.5526752) | 未知 | 未知 | 0 | 2 | crossref | abstract unavailable; conceptual background pending verification |
| 22 | [When an Insider Threat is No Longer an Insider Threat: A Look at Risk Decay](https://doi.org/10.1109/emr.2026.3661857) | 2026 | IEEE Engineering Management Review | 0 | 2 | crossref | abstract unavailable; risk-decay background pending verification |
| 23 | [[survey] Evaluation is key: a survey on evaluation measures for synthetic time series](https://doi.org/10.1186/s40537-024-00924-7) | 2024 | Journal of Big Data | 34 | 6 | crossref | direct survey on synthetic time-series evaluation |
| 24 | [[survey] On LLMs-Driven Synthetic Data Generation, Curation, and Evaluation: A Survey](http://arxiv.org/abs/2406.15126v1) | 2024 | arXiv | 0 | 3 | arxiv | direct survey on LLM-driven synthetic generation/curation/evaluation |

未删候选摘要与筛选原因在[JSON](docs/dataset-evaluation/evidence/search-results.json)中；待核验项不用于确定指标或数值门槛。

## 基础追溯来源（model knowledge提出，随后一手核验）

P01/P02/P05–P10/P15–P18/P20–P25来自领域基础追溯，按[文献表](docs/dataset-evaluation/literature-review.md)标记全文/摘要；P03无法读到有效全文，P04只有数据库元数据。它们不是近期API检索返回，不虚构API命中/引用数。

## Summary of all searched results

### 1. Overview

三个查询返回24个唯一候选，语义筛选后保留19项。直接支持最终体系的近期命中为信用卡稀有事件保真/效用、LLM内部威胁合成、时间序列评测综述和LLM合成数据综述；其余为方法邻近例子或待核验背景。该检索有限，不能宣称系统性穷尽。

### 2. Trends

2024–2026候选显示时间序列跨通道动态、稀有事件效用与LLM生成/筛选/评测受到关注。此次样本上限很小且四来源无有效返回，不能推断全领域增长率、主导机构或发表趋势。

### 3. Key themes

- 保真与效用分开：#5、#7、#23；统计相似不等于任务可用。
- 跨时间与跨通道：#4、#8、#23；只看边际不够。
- LLM合成与稀有威胁：#6、#24；标签与评审偏差要隔离。
- 已知真值与评测有效性：#2、#10；评价代理也需要验证。
- 下游任务增益：#1、#12、#13；迁移协议可参考但不是日志真实性证明。

### 4. Keywords frequency

对保留标题做大小写归一的短语/单词计数，表中计出现该词的标题数，非整个文献领域频率。

| Keyword | Count |
|---|---:|
| synthetic | 13 |
| evaluation | 8 |
| time series | 7 |
| data | 12 |
| insider threat | 4 |

### 5. Most cited by accepted paper

引用数缺乏跨来源验证，以下只是返回值排序；不把未知/arXiv占位0当真实引用排名。

| Rank | Title | Year | Citations |
|---|---|---|---:|
| 1 | Evaluation is key: a survey on evaluation measures for synthetic time series | 2024 | 34（API快照） |
| 2 | PPMI-Benchmark: A Dual Evaluation Framework for Imputation and Synthetic Data Generation in Longitudinal Parkinson's Disease Research | 2025 | 4（API快照） |
| 3 | Evaluation of Machine Learning Techniques for ESP Diagnosis Using a Synthetic Time Series Dataset | 2024 | 2（API快照） |
| 4 | Insider Threat | 2024 | 1（API快照） |
| 5 | Synthetic data improves survival model evaluation under distribution shifts | 未知 | 0（API快照） |

### 6. Most cited by first author

同样仅汇总已保留Crossref返回快照，不是作者生涯引用。

| Rank | Author | Papers in set | Total citations |
|---|---|---:|---:|
| 1 | Michael Stenger | 1 | 34 |
| 2 | Moad Hani | 1 | 4 |
| 3 | M. Alhashem | 1 | 2 |
| 4 | Pierre Skorich | 1 | 1 |
| 5 | Yunwei Zhang | 1 | 0 |

### 7. Recommendations for reading

先读领域Chimera/CERT与Alaa的分维度评测，再读近期#23（摘要已核对，全文待补）/#24综述；随后读#5/#6的稀有异常实验与标签泄漏限制；最后用AppWorld/τ-bench定义终态/可靠性，并以MT-Bench论文校准DeepSeek评分偏差。具体一手入口与采用范围见文献表。

## 检索错误与访问限制

DBLP错误原文：

```text
[dblp] Error on query 'synthetic data evaluation': ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
[dblp] Error on query 'synthetic time series evaluation': ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
[dblp] Error on query 'insider threat dataset': ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
[open_alex] HTTP 429; retrying in 35s (attempt 2/2)
[open_alex] Error on query 'synthetic data evaluation': 429 Client Error: Too Many Requests for url: https://api.openalex.org/works?search.semantic=synthetic+data+evaluation&filter=publication_year%3A2024-2026&sort=relevance_score%3Adesc&page=1&per-page=4
[open_alex] HTTP 429; retrying in 35s (attempt 2/2)
[open_alex] Error on query 'synthetic time series evaluation': 429 Client Error: Too Many Requests for url: https://api.openalex.org/works?search.semantic=synthetic+time+series+evaluation&filter=publication_year%3A2024-2026&sort=relevance_score%3Adesc&page=1&per-page=4
[open_alex] HTTP 429; retrying in 35s (attempt 2/2)
[open_alex] Error on query 'insider threat dataset': 429 Client Error: Too Many Requests for url: https://api.openalex.org/works?search.semantic=insider+threat+dataset&filter=publication_year%3A2024-2026&sort=relevance_score%3Adesc&page=1&per-page=4
[openreview] Error on query 'synthetic data evaluation': openreview not installed. pip install openreview-py
[openreview] Error on query 'synthetic time series evaluation': openreview not installed. pip install openreview-py
[openreview] Error on query 'insider threat dataset': openreview not installed. pip install openreview-py
[semantic_scholar] HTTP 429; retrying in 3s (attempt 2/2)
[semantic_scholar] Error on query 'synthetic data evaluation': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=synthetic+data+evaluation&offset=0&limit=4&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
[semantic_scholar] HTTP 429; retrying in 3s (attempt 2/2)
[semantic_scholar] Error on query 'synthetic time series evaluation': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=synthetic+time+series+evaluation&offset=0&limit=4&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
[semantic_scholar] HTTP 429; retrying in 3s (attempt 2/2)
[semantic_scholar] Error on query 'insider threat dataset': 429 Client Error:  for url: https://api.semanticscholar.org/graph/v1/paper/search?query=insider+threat+dataset&offset=0&limit=4&fields=title%2Cauthors%2Cyear%2Cabstract%2CcitationCount%2Curl%2Cvenue%2CpublicationDate%2CexternalIds&year=2024-2026
```

OpenAlex、OpenReview、Semantic Scholar返回0，但未拿到明确失败诊断，不解释为无论文。主机python缺requests，改用仓库既有.venv成功运行，无新安装。TWOS全文403；时间序列综述全文超时/SSL失败；CERT2014入口为验证页；G-Eval PDF下载失败但官方摘要可读；DeepSeek缓存页首次失败后curl重试可读。具体错误和读取哈希见[source-retrieval.json](docs/dataset-evaluation/evidence/source-retrieval.json)。

# 后循环慢性闭塞再通：检索与筛选记录

- **检索日期**：2026-11-11（Asia/Hong_Kong）
- **检索主题**：后循环慢性/非急性闭塞的血管内再通（endovascular recanalization of chronic / non-acute posterior circulation occlusion；chronic vertebrobasilar artery occlusion）
- **检索人**：自动化文献代理（单检索人），所有纳入文献均回到 PubMed/Europe PMC 原始记录核对题录与摘要。

## 1. 数据库与检索式

### 1.1 PubMed（NCBI E-utilities）

| 编号 | 检索式 | 命中 |
|---|---|---|
| Q1 | `("chronic"[tiab] OR "non-acute"[tiab] OR nonacute[tiab] OR "long-standing"[tiab]) AND (vertebrobasilar[tiab] OR "basilar artery"[tiab] OR "vertebral artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab]) AND (endovascular[tiab] OR recanalization[tiab] OR recanalisation[tiab] OR stenting[tiab] OR angioplasty[tiab] OR revascularization[tiab])` | 133 |
| Q2 | `("non-acute"[tiab] OR nonacute[tiab] OR subacute[tiab] OR "medically refractory"[tiab]) AND (vertebrobasilar[tiab] OR "basilar artery"[tiab] OR "vertebral artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab]) AND (endovascular[tiab] OR recanalization[tiab] OR stenting[tiab] OR angioplasty[tiab])` | 61 |
| Q3 | `(vertebrobasilar[tiab] OR "basilar artery"[tiab] OR "vertebral artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab]) AND (stenting[tiab] OR "stent"[tiab] OR angioplasty[tiab]) AND (elective[tiab] OR "chronic"[tiab] OR "non-acute"[tiab] OR nonacute[tiab] OR "subacute"[tiab])` | 92 |
| Q4 | `(("chronic"[ti] OR "non-acute"[ti] OR nonacute[ti] OR subacute[ti]) AND (vertebrobasilar[ti] OR "basilar artery"[ti] OR "vertebral artery"[ti] OR "posterior circulation"[ti]) AND (occlusion[ti] OR occluded[ti]))` | 32 |

四式合并去重后 **181 条** PubMed 记录（含摘要、作者、期刊、DOI、PMID、MeSH）。

### 1.2 Europe PMC（REST API，含预印本与开放全文）

| 编号 | 检索式（TITLE_ABS 字段） | 命中 |
|---|---|---|
| E1 | `(chronic OR non-acute OR nonacute OR subacute OR long-standing) AND (vertebrobasilar OR basilar artery OR vertebral artery OR posterior circulation) AND (occlusion OR occluded) AND (endovascular OR recanalization OR recanalisation OR stenting OR angioplasty OR revascularization)` | 140 |
| E2 | `(vertebrobasilar OR basilar artery OR vertebral artery OR posterior circulation) AND occlusion AND (recanalization OR endovascular) AND (meta-analysis OR systematic review)` | 146 |
| E3 | `(TITLE: chronic OR non-acute OR nonacute OR subacute) AND (TITLE: vertebral artery OR vertebrobasilar OR basilar artery OR posterior circulation) AND (TITLE: occlusion OR occluded)` | 34 |

三式合并去重后 **289 条** Europe PMC 记录。

### 1.3 补充检索

- PubMed：慢性/非急性 VBAO 的 Meta 分析（3 条）、自然病史/预后（121 条）、共识/指南（13 条）。
- 人工追溯关键文献的参考文献与“被引”线索，补充 VERITAS、>24 h VBO 队列、后循环卒中综述等背景文献。
- 未使用 Embase、CNKI、万方（无订阅/访问权限）；中文文献仅通过 PubMed 收录的英文题录与摘要获取。

## 2. 去重与筛选

- 数据库初检：181（PubMed）+ 289（Europe PMC）+ 137（补充检索）= **607 条**（含重复）。
- 去重后：**331 条**（PubMed/Europe PMC 按 PMID/DOI 去重，补充检索新增 5 条）。
- 标题/摘要筛选后：**40 篇**进入全文或摘要深度提取，并全部列入 `02_literature_table.md`。
- 其中获取开放全文 **13 篇**：PDF **7 篇**（保存于 `pdfs/`）；Europe PMC 全文 XML **11 份**（保存于 `fulltext/`，其中 5 份与 PDF 重叠，6 篇为 XML-only），并提取 13 篇纯文本用于阅读。其余 **27 篇**仅获取题录与摘要，按要求整理为详细清单。

> 说明：标题/摘要筛选为叙述性、单检索人完成，未逐条记录全部排除原因，因此本流程不应被表述为严格 PRISMA 系统综述。所有纳入文献的题录、DOI、PMID 与摘要结论均回溯原始数据库记录。

## 3. 纳入与排除标准

**纳入：**

1. 成人（≥18 岁）症状性后循环（椎动脉颅内段/基底动脉/椎基底动脉）慢性或非急性闭塞，定义多为症状/影像确认闭塞 >24 h、>2 周、>3 周或 >1 个月（各研究不一致）。
2. 血管内再通（球囊扩张、支架置入、支架辅助再通、分期再通、远端保护等），或与再通决策直接相关的影像/分型/预测研究。
3. 报告至少 1 项结局：技术成功、围手术期并发症、mRS、卒中复发/死亡、再狭窄/再闭塞、随访通畅。
4. 英文或中文；2000–2026 年。

**排除：**

1. 仅急性基底动脉闭塞（发病 ≤24 h）的取栓研究——仅保留少量作为背景对照（VERITAS、>24 h 队列）。
2. 前循环闭塞、动脉瘤、夹层、动静脉瘘、外伤、肿瘤、锁骨下动脉/主动脉病变。
3. 无结局数据的纯技术描述、会议摘要、重复队列（保留信息量更大或更新者）。
4. 无法核实题录或全文的文献。

**用于定量描述的研究：** 样本量 ≥8 的队列；个案报道（N=1–3）仅用于技术可行性与典型病例展示，不参与率值比较。

## 4. 数据提取字段

题录（第一作者、期刊、年份、DOI、PMID）、国家/中心、设计、人群与闭塞部位、非急性定义、样本量、技术成功（mTICI ≥2b）、围手术期并发症及类型、30 d 卒中/死亡、90 d/末次 mRS 0–2 与 0–3、再狭窄/再闭塞、随访时间、开放全文状态、核心结论。

## 5. 方法学局限

- 单检索人、无第二人独立筛选，存在选择偏倚。
- 未检索 Embase、CNKI、万方，可能漏掉中文队列与会议摘要。
- 各研究“非急性/慢性”的定义、并发症定义、随访时长不一致，率值不可直接合并。
- 多个中国中心队列时间重叠、作者团队重叠，存在重复人群可能；因此本报告只做叙述性汇总，未自行做 Meta 分析。
- 发表偏倚：小样本阳性经验更易发表；失败病例可能报告不足。

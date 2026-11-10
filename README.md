# 文献调研与学术 PPT 自动化工作区

本仓库由 **dsh-superagent** 驱动，用于文献检索、证据提取与学术汇报材料制作。

## 当前交付：后循环慢性闭塞再通

- **主题**：后循环慢性/非急性闭塞的血管内再通（endovascular recanalization of chronic / non-acute vertebrobasilar occlusion）
- **文献库**：[`literature/00_README.md`](literature/00_README.md)
  - 40 篇纳入文献的题录、DOI、PMID、核心结论：[`literature/02_literature_table.md`](literature/02_literature_table.md)
  - 检索式与筛选流程：[`literature/01_search_strategy.md`](literature/01_search_strategy.md)
  - 证据综合：[`literature/03_synthesis.md`](literature/03_synthesis.md)
  - 13 篇开放全文的深度阅读笔记：[`literature/04_reading_notes.md`](literature/04_reading_notes.md)
  - 7 篇 PDF、6 篇 Europe PMC 全文 XML、结构化 `evidence_table.csv`、`references.bib`
- **30 页组会 PPT**：[`slides/后循环慢性闭塞再通_组会汇报_30页.pptx`](slides/后循环慢性闭塞再通_组会汇报_30页.pptx)
  - PDF 版：[`slides/后循环慢性闭塞再通_组会汇报_30页.pdf`](slides/后循环慢性闭塞再通_组会汇报_30页.pdf)
  - 幻灯片结构、数据来源与再生成方法：[`slides/README.md`](slides/README.md)

## 目录结构

- `literature/` — 检索记录、文献汇总表、开放全文、阅读笔记、综述 Markdown
- `slides/` — 可编辑 `.pptx`、PDF、图表素材与生成脚本说明
- `reports/` — 深度研究与分析报告
- `data/` — 原始数据与分析结果表
- `scripts/` — 检索、文献表、图表与 PPT 的可复现脚本

## 复现

```bash
python scripts/retrieve_pubmed.py      # PubMed 检索
python scripts/retrieve_epmc.py        # Europe PMC 检索
python scripts/fetch_fulltext.py       # 开放全文 XML / PDF
python scripts/build_table.py          # 文献汇总表
python scripts/make_bib.py             # BibTeX
python scripts/make_figures.py         # 幻灯片图表
python scripts/build_deck.py           # 生成 30 页 PPTX
python scripts/export_slides.py ...    # 导出 PNG（需本机 PowerPoint）
python scripts/export_pdf.py ...       # 导出 PDF（需本机 PowerPoint）
```

"""Build the screened literature table (CSV + Markdown) with verified metadata and extracted results."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "literature"

pm = {r["pmid"]: r for r in json.loads((LIT / "pubmed_raw.json").read_text(encoding="utf-8"))}
ep = {r["pmid"]: r for r in json.loads((LIT / "epmc_raw.json").read_text(encoding="utf-8")) if r.get("pmid")}
extra = {r["pmid"]: r for r in json.loads((LIT / "extra_refs.json").read_text(encoding="utf-8"))}


def meta(pmid):
    if pmid in pm:
        r = pm[pmid]
        authors = r["authors"]
        return {
            "title": re.sub(r"<[^>]+>", "", r["title"]),
            "journal": r["journal"],
            "year": r["year"],
            "doi": r["doi"],
            "authors": authors,
        }
    if pmid in extra:
        r = extra[pmid]
        return {"title": r["title"], "journal": r["journal"], "year": r["year"], "doi": r["doi"], "authors": r["authors"]}
    if pmid in ep:
        r = ep[pmid]
        auth = r.get("authorString", "")
        return {
            "title": r.get("title", ""),
            "journal": r.get("journalTitle", ""),
            "year": r.get("pubYear", ""),
            "doi": r.get("doi", ""),
            "authors": [a.strip() for a in auth.split(",") if a.strip()],
        }
    raise KeyError(pmid)


# manual extraction: design, population, n, success, complications, outcome, restenosis, follow-up, OA, conclusion
M = {
    "42931137": dict(design="个案报道", population="非急性椎基底动脉闭塞（左侧V4，右侧VA发育不良）", n="1",
        success="1/1", complications="无血管内操作并发症", outcome="NIHSS 5→2；30 d mRS 1", restenosis="未复查血管影像",
        followup="30 d", oa="XML全文", conclusion="选择性非急性VBO再通技术可行；单例不能证明优于药物治疗或长期耐久。"),
    "42825306": dict(design="个案报道", population="症状性ICVA慢性完全闭塞（双侧VA闭塞）", n="1",
        success="1/1", complications="术后小脑梗死，无新发神经功能缺损", outcome="出院回家；2个月无症状", restenosis="未报告",
        followup="2个月", oa="摘要", conclusion="自动灌注成像（RAPID）发现低灌注区，可辅助筛选慢性ICVA CTO再通候选者。"),
    "40399844": dict(design="个案报道", population="症状性长节段非急性左VA闭塞（V1–V4）", n="1",
        success="1/1", complications="未报告", outcome="术后无新发症状；2年随访通畅", restenosis="2年DSA通畅",
        followup="2年", oa="XML全文", conclusion="经仔细评估后，长节段非急性VA闭塞再通可行。"),
    "40232517": dict(design="单中心回顾性", population="症状性非急性VBA闭塞", n="8",
        success="8/8 (100%)", complications="2/8 (25%)：1例无症状ICH、1例血栓移位", outcome="90 d mRS 0–2 75%；1例非手术相关死亡", restenosis="未报告",
        followup="中位9个月", oa="XML全文", conclusion="支架取栓器作远端保护可能减少再通过程中的远端栓塞，需更大样本验证。"),
    "40260138": dict(design="单中心回顾性+预测评分", population="非急性基底动脉闭塞（NABAO）", n="115",
        success="94/115 (81.7%)", complications="未在摘要报告", outcome="建立4因素评分（AUC 0.817）", restenosis="未报告",
        followup="未报告", oa="PDF全文", conclusion="闭塞>3个月、钝头残端、闭塞长度>30 mm、远端代偿不足是再通失败的独立负向预测因素。"),
    "40291848": dict(design="单中心回顾性+预测模型", population="症状性慢性颅内大动脉闭塞（含VBA）", n="103",
        success="71/103 (68.9%)", complications="术中并发症 11/103 (10.7%)", outcome="预测模型：低/中/高风险再通率100%/66.7%/11.1%", restenosis="未报告",
        followup="未报告", oa="PDF全文", conclusion="残端形态、距末次神经事件时间、年龄、吸烟、NLR可预测慢性闭塞再通成败。"),
    "41707496": dict(design="单中心回顾性队列（EVT vs 保守）", population="中国老年非急性颅内VBA闭塞", n="150（EVT与保守组）",
        success="未报告", complications="未报告", outcome="1年卒中复发/死亡 10% vs 30%（aOR 8.7）；mRS 0–3 80% vs 60%", restenosis="未报告",
        followup="1年", oa="摘要", conclusion="老年NAIVBAO中EVT可能降低1年卒中复发/死亡并改善功能结局；单中心回顾性，需RCT验证。"),
    "41475460": dict(design="系统综述与Meta分析（23项研究）", population="非急性颅内动脉闭塞（前+后循环）", n="1571（EVT 1529；保守 42）",
        success="87% (95% CI 84–91; I²=78%)", complications="围手术期并发症 13% (10–15)；围手术期死亡 0%", outcome="长期卒中复发/死亡 7% (4–9)；再通成功 vs 失败 OR 0.15 (0.06–0.37)", restenosis="15% (13–18)",
        followup="长期随访（各研究不一）", oa="摘要", conclusion="非急性颅内动脉闭塞再通总体安全有效；前后循环再通率与并发症无显著差异，但异质性高、对照极少。"),
    "38363911": dict(design="单中心回顾性+风险分层", population="非急性症状性ICVA闭塞", n="92",
        success="77/92 (83.7%)", complications="10/92 (10.9%)；30 d卒中/死亡 5.4%", outcome="90 d mRS 0–2：低/中/高危 100%/83.3%/22.2%（合计约79%）", restenosis="低/中/高危 0%/17.9%/80%",
        followup="中位13个月", oa="XML全文", conclusion="按闭塞长度、时间、性质、钙化、成角分层可识别再通获益人群；高危组应谨慎。"),
    "38676723": dict(design="单中心回顾性（自然病程）", population="慢性基底动脉闭塞", n="15",
        success="未干预（部分再通失败）", complications="—", outcome="5例偶然发现、4例轻症、6例急性期后存活；均见后交通动脉侧支", restenosis="—",
        followup="≥3个月", oa="摘要", conclusion="慢性BAO可无症状或仅轻症，长期存活；侧支代偿好，提示单中心再通队列存在选择偏倚。"),
    "38194727": dict(design="单中心回顾性", population="非急性椎动脉开口闭塞（VOO）", n="21（22处病变）",
        success="14/21 (66.7%)", complications="3/21 (14.3%)", outcome="锥形残端再通90.9% vs 非锥形40%", restenosis="未报告",
        followup="未报告", oa="摘要", conclusion="残端形态（锥形/非锥形）可预测VOO再通成功率，并指导入路选择。"),
    "39482210": dict(design="单中心回顾性+预测评分", population="症状性慢性颅内大动脉闭塞（含VBA）", n="73",
        success="61/73 (83.6%)", complications="10/73 (13.7%)", outcome="HR-MRI评分预测再通率50%–100%", restenosis="未报告",
        followup="未报告", oa="摘要", conclusion="HR-MRI示残留管腔、明显斑块强化、闭塞长度≤10.2 mm提示再通成功；VBA较MCA再通率低。"),
    "37122305": dict(design="单中心回顾性", population="症状性非急性VBA闭塞（SNOVA）", n="88",
        success="81/88 (92.0%)", complications="17/88 (19.3%)；围手术期死亡5.7%", outcome="随访mRS中位1；1年卒中11.4%", restenosis="19/75 (25.3%)",
        followup="平均16.9个月", oa="PDF全文", conclusion="选择性SNOVA再通成功率高、预后改善，但并发症与再狭窄不低；钝头残端、再通时机、后扩张是重要风险因素。"),
    "36941301": dict(design="单中心回顾性（前+后循环）", population="症状性非急性颅内大动脉闭塞；VBA亚组58例", n="177（VBA 58）",
        success="总体152/177 (85.9%)；VBA 48/58 (82.8%)", complications="总体15/177 (8.5%)；VBA 3/58 (5.2%)", outcome="总体90 d mRS 0–2 94.9%（基线轻症为主）；VBA再狭窄/再闭塞8/48 (16.7%)", restenosis="VBA 8/48 (16.7%)",
        followup="3–7个月", oa="PDF全文", conclusion="VBA再通成功率与前循环相近、并发症更低；闭塞长度、钙化、成角是再通失败的独立因素。"),
    "33722973": dict(design="多中心回顾性+造影分型", population="症状性非急性颅外VA闭塞（EVAO）", n="50",
        success="43/50 (86.0%)", complications="6/50 (12.0%)；30 d卒中/死亡4.0%", outcome="A型再通100%、并发症0%；D型再通63.6%、并发症27.3%", restenosis="未报告",
        followup="未报告", oa="摘要", conclusion="EVAO造影分型（A–D）可预测再通与并发症，A型最适合再通。"),
    "33674396": dict(design="多中心回顾性+造影分型", population="症状性非急性BAO伴进展/复发性缺血", n="42",
        success="32/42 (76.2%)", complications="6/42 (14.3%)", outcome="I–III型再通90%/71.4%/50%；随访卒中/死亡7.9%", restenosis="未报告",
        followup="中位1年", oa="摘要", conclusion="短段闭塞且远端BA代偿好（I型）最适合再通；长段/代偿差者风险高。"),
    "34220682": dict(design="单中心回顾性（分期再通）", population="早期非急性症状性ICVA闭塞", n="10",
        success="9/10", complications="1例术中穿孔", outcome="3个月mRS≤2 7/10；末次随访9/10", restenosis="未报告",
        followup="未报告", oa="PDF全文", conclusion="分期再通（先球囊维持灌注、后支架）可用于早期非急性ICVA闭塞的高危患者。"),
    "33786136": dict(design="单中心回顾性", population="慢性VA起始部闭塞", n="22",
        success="19/22 (86.4%)", complications="未报告", outcome="随访无复发TIA/卒中", restenosis="6/22 (27.3%)",
        followup="未报告", oa="XML全文", conclusion="球囊扩张±支架治疗慢性VA起始部闭塞可行、安全，但再狭窄率约27%。"),
    "33312156": dict(design="单中心回顾性", population="症状性动脉粥样硬化性非急性ICVA完全闭塞", n="31",
        success="27/31 (87.1%)", complications="6/31 (19.4%)", outcome="mRS 0–2 74.1%；mRS 0–3 85.2%", restenosis="2/20 (10%)",
        followup="中位11个月", oa="PDF全文", conclusion="低灌注型优势ICVA完全闭塞（长病变、高血栓负荷）再通可行，多数获得良好功能结局。"),
    "32838672": dict(design="单中心回顾性+新造影分型", population="症状性非急性ICVA闭塞", n="50",
        success="38/50 (76%)", complications="30 d卒中/死亡4%；I–IV型并发症0%/7.7%/20%/50%", outcome="I–IV型再通94.1%/76.9%/70%/50%", restenosis="未报告",
        followup="未报告", oa="摘要", conclusion="ICVA闭塞造影分型可预测再通与并发症；I/II型适合再通。"),
    "37502385": dict(design="叙述性综述", population="ICVA慢性完全闭塞", n="—",
        success="—", complications="—", outcome="—", restenosis="—", followup="—", oa="摘要",
        conclusion="综述ICVA CTO的定义、发病率、临床表现、血管内再通、并发症与结局。"),
    "31920916": dict(design="单中心回顾性", population="症状性亚急性–慢性动脉粥样硬化性BAO", n="21",
        success="17/21 (81.0%)", complications="2/21 (9.5%)穿支卒中", outcome="90 d mRS 0–2 76.5%；mRS 0–3 94.1%", restenosis="未报告",
        followup="17.4±8.0个月", oa="PDF全文", conclusion="药物治疗无效的亚急性–慢性BAO再通在 selected patients 中可行，90 d功能结局较好。"),
    "29408529": dict(design="单中心回顾性+文献复习", population="慢性症状性ICVA完全闭塞", n="14",
        success="12/14 (85.7%)", complications="2/14 (14.3%)", outcome="文献汇总34例：再通94.1%、并发症17.6%、死亡2.9%", restenosis="未报告",
        followup="未报告", oa="摘要", conclusion="慢性ICVA再通可行但高风险；需严格筛选、评估闭塞走行与分期。"),
    "25276423": dict(design="单中心回顾性", population="慢性症状性ICVA完全闭塞", n="8",
        success="6/7 attempted (85.7%)", complications="3例：小脑出血、夹层、穿孔、亚急性支架内血栓", outcome="1例死于小脑出血；其余改善", restenosis="未报告",
        followup="未报告", oa="摘要", conclusion="支架辅助再通技术可行，但并发症发生率高，仅适用于高度选择的患者。"),
    "24200139": dict(design="单中心回顾性", population="症状性非急性颅内VBA闭塞（12 BA，15 VA）", n="27",
        success="26/27 (96%)", complications="5/27 (19%)：夹层、急性血栓、血栓移位、再闭塞", outcome="未报告", restenosis="未报告",
        followup="未报告", oa="摘要", conclusion="非急性VBAO再通技术成功率高但围手术期并发症风险高，需规范并发症防治。"),
    "21122005": dict(design="病例系列", population="慢性颅内VBA闭塞伴复发症状", n="3",
        success="3/3", complications="1例自限性SAH", outcome="30个月内无复发", restenosis="未报告",
        followup="最长30个月", oa="摘要", conclusion="慢性VBO再通技术可行，但仅限最大药物治疗下仍有复发症状/进展的选择性患者。"),
    "20190661": dict(design="单中心回顾性（技术报告）", population="亚急性–慢性BAO", n="9",
        success="8/9", complications="4例围手术期并发症", outcome="4/9死亡；存活者mRS 0,0,2,2,3", restenosis="2例支架内狭窄",
        followup="平均11个月", oa="摘要", conclusion="慢性BAO再通可行但风险较高，应仅用于药物难治性症状患者，并加强术后管理。"),
    "19249959": dict(design="单中心回顾性（前+后循环）", population="非急性颅内闭塞/近闭塞（1例VA）", n="7",
        success="7/7", complications="2例：穿支卒中、致命性出血", outcome="平均mRS 2（1–5）", restenosis="4例无症状再狭窄",
        followup="平均399 d", oa="摘要", conclusion="非急性颅内闭塞直接再通是潜在选择，但与传统治疗相比的风险获益仍不明确。"),
    "17322092": dict(design="个案报道", population="症状性BAO 80天", n="1",
        success="1/1", complications="未报告", outcome="成功再通", restenosis="未报告", followup="未报告", oa="摘要",
        conclusion="慢性期（80天）BAO再通技术可行，提示时间窗并非绝对禁忌。"),
    "31629152": dict(design="单中心回顾性", population="非急性症状性近端颅外VA闭塞（PEVAO）", n="23",
        success="21/23 (91.3%)", complications="1/23 (4.3%)", outcome="3个月无症状复发、CTA无再狭窄", restenosis="3个月无再狭窄",
        followup="3个月", oa="摘要", conclusion="近端颅外VAO再通成功率高、并发症低；需更长期随访。"),
    "31899403": dict(design="单中心回顾性（技术）", population="非急性症状性VA开口闭塞", n="7",
        success="7/7 (100%)", complications="无重大急性血栓栓塞事件", outcome="随访无复发缺血症状", restenosis="1/5无症状再狭窄",
        followup="平均20.6个月", oa="摘要", conclusion="远端栓塞保护装置辅助VA开口闭塞支架置入可行，可能减少远端栓塞。"),
    "40178541": dict(design="技术笔记", population="无残端的VA闭塞", n="—",
        success="—", complications="—", outcome="—", restenosis="—", followup="—", oa="摘要",
        conclusion="REVANS技术利用颈部侧支逆行进入闭塞段，为无残端VAO提供再通入路。"),
    "33256334": dict(design="专家共识", population="中国非急性颅内/外大血管闭塞", n="—",
        success="—", complications="—", outcome="—", restenosis="—", followup="—", oa="摘要",
        conclusion="中国非急性颅内/外大血管闭塞血管内治疗专家共识，强调患者选择、影像评估与围术期管理。"),
    "38878845": dict(design="叙述性综述", population="椎动脉残端综合征（VASS），72例文献汇总", n="72（文献汇总）",
        success="—", complications="—", outcome="抗凝组1例复发；抗血小板4例均复发；慢性期再通可作为选择", restenosis="—", followup="—", oa="摘要",
        conclusion="VASS是后循环栓塞的易漏诊病因；抗凝可能优于抗血小板，慢性期VA再通可用于药物失败者。"),
    "40584425": dict(design="叙述性综述", population="颅内椎基底动脉粥样硬化狭窄/非急性闭塞", n="—",
        success="—", complications="—", outcome="—", restenosis="—", followup="—", oa="XML全文",
        conclusion="对药物难治的严重ICVB狭窄/非急性闭塞，个体化PTAS可能可行；支架选择、亚满意扩张与并发症防治是关键。"),
    "24024918": dict(design="通讯/letter", population="非急性VBAO支架再通", n="—",
        success="—", complications="—", outcome="—", restenosis="—", followup="—", oa="摘要",
        conclusion="非急性VBAO支架再通的初步经验（letter，数据有限）。"),
    "35104439": dict(design="叙述性综述", population="后循环缺血性卒中", n="—",
        success="—", complications="—", outcome="—", restenosis="—", followup="—", oa="摘要",
        conclusion="后循环卒中占全部缺血性卒中的20%–25%，功能结局较差，研究相对不足。"),
    "24050733": dict(design="叙述性综述", population="后循环缺血性卒中/TIA", n="—",
        success="—", complications="—", outcome="—", restenosis="—", followup="—", oa="摘要",
        conclusion="约1/5的卒中/TIA位于后循环；合并椎基底动脉狭窄时早期复发风险高。"),
    "39674187": dict(design="系统综述+个体数据Meta分析（4项RCT）", population="急性VBO（发病≤12h为主）", n="988",
        success="—", complications="sICH与死亡为安全性终点", outcome="90 d mRS 0–3 45% vs 30%（aOR 2.41）；mRS 0–2 35% vs 21%", restenosis="—",
        followup="90 d", oa="摘要", conclusion="急性VBO血管内治疗显著改善90 d功能结局；这是慢性/非急性决策的背景证据，不能直接外推。"),
    "40512496": dict(design="多中心前瞻性队列（PSM）", population="VBO>24h", n="202（PSM各71）",
        success="—", complications="sICH 5.6% vs 0%", outcome="90 d mRS 0–3 57.7% vs 45.1%（aRR 1.35）；死亡12.7% vs 28.2%", restenosis="—",
        followup="90 d", oa="摘要", conclusion="超过24h的VBO，EVT+BMT可能改善功能结局并降低死亡；属急性/亚急性范畴，非慢性闭塞。"),
}

# extras not in M: background of posterior circulation, etc. All above.

rows = []
for pmid, d in M.items():
    md = meta(pmid)
    authors = md["authors"]
    first = authors[0] if authors else ""
    first_short = (first.split()[0] + " et al.") if len(authors) > 1 else (first.split()[0] if first else "")
    if pmid == "33256334":
        first_short = "中国专家共识"
    rows.append({
        "pmid": pmid,
        "doi": md["doi"],
        "title": md["title"],
        "first_author": first_short,
        "authors_full": ", ".join(authors[:6]) + (" et al." if len(authors) > 6 else ""),
        "journal": md["journal"],
        "year": md["year"],
        "design": d["design"],
        "population": d["population"],
        "n": d["n"],
        "success": d["success"],
        "complications": d["complications"],
        "outcome": d["outcome"],
        "restenosis": d["restenosis"],
        "followup": d["followup"],
        "oa": d["oa"],
        "conclusion": d["conclusion"],
    })

JABBR = {
    "World neurosurgery": "World Neurosurg",
    "Atherosclerosis": "Atherosclerosis",
    "Neurology international": "Neurol Int",
    "Journal of neuroendovascular therapy": "J Neuroendovasc Ther",
    "BMC neurology": "BMC Neurol",
    "Acta neurochirurgica": "Acta Neurochir (Wien)",
    "Frontiers in neurology": "Front Neurol",
    "JAMA network open": "JAMA Netw Open",
    "Lancet (London, England)": "Lancet",
    "Neuroradiology": "Neuroradiology",
    "Academic radiology": "Acad Radiol",
    "IBRO neuroscience reports": "IBRO Neurosci Rep",
    "Medicine": "Medicine (Baltimore)",
    "Journal of clinical neuroscience : official journal of the Neurosurgical Society of Australasia": "J Clin Neurosci",
    "Journal of stroke and cerebrovascular diseases : the official journal of National Stroke Association": "J Stroke Cerebrovasc Dis",
    "Journal of neurology": "J Neurol",
    "Scientific reports": "Sci Rep",
    "Journal of neurointerventional surgery": "J Neurointerv Surg",
    "Wideochirurgia i inne techniki maloinwazyjne = Videosurgery and other miniinvasive techniques": "Wideochir Inne Tech Maloinwazyjne",
    "Zhonghua nei ke za zhi": "Zhonghua Nei Ke Za Zhi",
    "Stroke": "Stroke",
    "Journal of neuroradiology = Journal de neuroradiologie": "J Neuroradiol",
    "Annals of vascular surgery": "Ann Vasc Surg",
    "Minimally invasive surgery": "Minim Invasive Surg",
    "International journal of stroke : official journal of the International Stroke Society": "Int J Stroke",
    "The Lancet. Neurology": "Lancet Neurol",
    "Journal of neuroimaging : official journal of the American Society of Neuroimaging": "J Neuroimaging",
    "Neurosurgery": "Neurosurgery",
    "Neurosurgical focus": "Neurosurg Focus",
    "The American journal of the medical sciences": "Am J Med Sci",
}
for r in rows:
    r["journal"] = JABBR.get(r["journal"], r["journal"])
rows.sort(key=lambda r: (-int(r["year"]), r["first_author"]))
for i, r in enumerate(rows, 1):
    r["ref"] = f"R{i:02d}"

cols = ["ref", "pmid", "doi", "first_author", "title", "journal", "year", "design", "population", "n",
        "success", "complications", "outcome", "restenosis", "followup", "oa", "conclusion", "authors_full"]
with (LIT / "evidence_table.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

# Markdown table
with (LIT / "02_literature_table.md").open("w", encoding="utf-8") as f:
    f.write("# 后循环慢性闭塞再通：纳入文献汇总表\n\n")
    f.write("检索与筛选方法见 `01_search_strategy.md`。文献按发表年份降序编号；`OA` 表示本地已保存 PDF/XML 全文，`摘要` 表示仅获取题录与摘要。\n\n")
    f.write("| # | 文献 | 年份 | 设计/人群 | N | 再通成功率 | 围手术期并发症 | 功能结局/复发 | 再狭窄 | OA |\n")
    f.write("|---|---|---|---|---|---|---|---|---|---|\n")
    for r in rows:
        fa = r['first_author']
        cite = f"{fa}{'' if fa.endswith('.') else '.'} {r['journal']}"
        f.write(f"| {r['ref']} | {cite} | {r['year']} | {r['design']}；{r['population']} | {r['n']} | {r['success']} | {r['complications']} | {r['outcome']} | {r['restenosis']} | {r['oa']} |\n")
    f.write("\n## 逐篇核心结论与可引用信息\n\n")
    for r in rows:
        f.write(f"### {r['ref']} {r['first_author']} ({r['year']})\n\n")
        f.write(f"- **标题**：{r['title']}\n")
        f.write(f"- **作者**：{r['authors_full']}\n")
        f.write(f"- **期刊/年份**：{r['journal']}, {r['year']}\n")
        f.write(f"- **DOI**：{r['doi'] or '未提供'}；**PMID**：{r['pmid']}\n")
        f.write(f"- **设计/人群**：{r['design']}；{r['population']}（N={r['n']}）\n")
        f.write(f"- **再通/并发症**：{r['success']}；{r['complications']}\n")
        f.write(f"- **结局/随访**：{r['outcome']}；随访 {r['followup']}\n")
        f.write(f"- **再狭窄**：{r['restenosis']}\n")
        f.write(f"- **核心结论**：{r['conclusion']}\n")
        f.write(f"- **本地全文**：{r['oa']}\n\n")

print("rows", len(rows))
print("refs", rows[0]["ref"], "...", rows[-1]["ref"])

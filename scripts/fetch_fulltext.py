"""Concurrent fetch of Europe PMC OA full text and publisher PDFs for selected studies."""
import json
import re
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
LIT = ROOT / "literature"
FT = LIT / "fulltext"
PDFS = LIT / "pdfs"
FT.mkdir(exist_ok=True)
PDFS.mkdir(exist_ok=True)

SELECTED = {
    "42931137": "2026_Soetanto_nonacute_VBO_case",
    "40399844": "2025_Jian_longsegment_VAO_case",
    "42825306": "2026_Yamada_chronic_VAO_case",
    "40584425": "2025_Zhou_ICVB_review",
    "40291848": "2025_Zhang_chronic_cerebral_predictors",
    "40260138": "2025_Liu_NABAO_predictors",
    "40232517": "2025_Li_distal_protection",
    "37122305": "2023_Zhou_SNOVA_88",
    "38363911": "2024_Chen_ICVA_risk_groups",
    "36941301": "2023_Xia_nonacute_intracranial_177",
    "33786136": "2021_Cai_chronic_VAO_22",
    "33312156": "2020_Zhao_nonacute_ICVA_total",
    "34220682": "2021_Duan_staged_ICVA",
    "31920916": "2019_Zhao_subacute_chronic_BAO",
    "37502385": "2020_Zhang_ICVA_CTO_review",
    "25276423": "2014_Xu_chronic_ICVA_8",
    "41475460": "2026_Chen_NAICAO_meta",
    "41707496": "2026_Li_elderly_NAIVBAO",
    "38676723": "2024_Roth_chronic_BAO",
    "33722973": "2022_Gao_EVAO_classification",
    "33674396": "2022_Gao_nonacute_BAO_multicenter",
    "32838672": "2020_Gao_ICVA_classification",
    "29408529": "2018_Gao_chronic_ICVA_review",
    "24200139": "2014_He_periop_complications",
    "20190661": "2010_Dashti_subacute_chronic_BAO",
    "21122005": "2012_Lin_chronic_VBO_case3",
    "19249959": "2009_Kole_nonacute_occlusion",
    "17322092": "2007_Yu_BAO_80days",
    "38194727": "2024_Liu_VOO_stump",
    "39482210": "2025_Zhou_HRMRI",
    "38878845": "2024_Rossi_VASS_review",
    "31899403": "2020_Zheng_distal_protection",
    "31629152": "2020_Chen_PEVAO",
    "40178541": "2025_Wang_REVANS",
    "23887219": "2013_Liu_chronic_VBO_case",
    "24024918": "2013_He_nonacute_VBAO_letter",
    "33256334": "2020_Chinese_expert_consensus",
}

epmc = json.loads((LIT / "epmc_raw.json").read_text(encoding="utf-8"))
by_pmid = {r["pmid"]: r for r in epmc if r.get("pmid")}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
    "Accept": "application/pdf,application/xml,*/*",
}


def xml_to_text(xml_bytes):
    root = ET.fromstring(xml_bytes)
    chunks = []
    for el in root.iter():
        if el.tag in ("title", "p", "caption"):
            t = "".join(el.itertext()).strip()
            if t:
                chunks.append(t)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(chunks))


def get(url, timeout=35):
    try:
        return requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    except Exception:
        return None


def worker(pmid, stem):
    rec = by_pmid.get(pmid, {})
    doi = rec.get("doi", "")
    pmcid = rec.get("pmcid", "")
    got_xml = False
    got_pdf = False
    source = ""

    if pmcid:
        for attempt in range(2):
            r = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
            if r is not None and r.status_code == 200 and r.content[:5] == b"<?xml":
                (FT / f"{stem}.xml").write_bytes(r.content)
                try:
                    (FT / f"{stem}.txt").write_text(xml_to_text(r.content), encoding="utf-8")
                except Exception:
                    pass
                got_xml = True
                break

    pdf_urls = []
    if doi.startswith("10.3389/"):
        pdf_urls.append(f"https://www.frontiersin.org/articles/{doi}/pdf")
    if doi.startswith("10.1038/"):
        pdf_urls.append(f"https://www.nature.com/articles/{doi.split('/', 1)[1]}.pdf")
    for url in pdf_urls:
        r = get(url)
        if r is not None and r.status_code == 200 and r.content[:4] == b"%PDF":
            (PDFS / f"{stem}.pdf").write_bytes(r.content)
            got_pdf = True
            source = url
            break

    return {
        "pmid": pmid,
        "stem": stem,
        "doi": doi,
        "pmcid": pmcid,
        "xml_fulltext": got_xml,
        "pdf": got_pdf,
        "pdf_source": source,
    }


results = []
with ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(worker, p, s): (p, s) for p, s in SELECTED.items()}
    for f in as_completed(futs):
        try:
            r = f.result()
        except Exception as e:
            p, s = futs[f]
            r = {"pmid": p, "stem": s, "xml_fulltext": False, "pdf": False, "error": str(e)}
        results.append(r)
        print(r["pmid"], r["stem"], "XML" if r.get("xml_fulltext") else "-", "PDF" if r.get("pdf") else "-", flush=True)

(LIT / "fulltext_log.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
print("XML", sum(1 for r in results if r.get("xml_fulltext")), "PDF", sum(1 for r in results if r.get("pdf")), "of", len(results))

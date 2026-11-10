import requests
from xml.etree import ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
QS = {
    "chronic_meta": '(("chronic"[tiab] OR "non-acute"[tiab] OR nonacute[tiab] OR subacute[tiab]) AND ("vertebrobasilar"[tiab] OR "basilar artery"[tiab] OR "vertebral artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab])) AND (meta-analysis[pt] OR systematic review[pt] OR "meta-analysis"[tiab] OR "systematic review"[tiab])',
    "natural_history": '("vertebrobasilar"[tiab] OR "basilar artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab]) AND ("natural history"[tiab] OR prognosis[tiab] OR "medically treated"[tiab] OR conservative[tiab]) AND (chronic[tiab] OR non-acute[tiab] OR nonacute[tiab] OR subacute[tiab] OR symptomatic[tiab])',
    "consensus": '(consensus[ti] OR guideline[ti] OR recommendation[ti]) AND ("intracranial"[tiab] OR vertebrobasilar[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occlusive[tiab]) AND (endovascular[tiab] OR recanalization[tiab] OR stenting[tiab])',
    "vbi_stent": '"vertebrobasilar insufficiency"[tiab] AND (stent[tiab] OR stenting[tiab] OR angioplasty[tiab] OR recanalization[tiab])',
}

for name, q in QS.items():
    r = requests.get(BASE + "esearch.fcgi", params={"db": "pubmed", "term": q, "retmode": "json", "retmax": 30, "sort": "relevance"}, timeout=60)
    ids = r.json()["esearchresult"]["idlist"]
    count = r.json()["esearchresult"]["count"]
    print(f"\n===== {name}: {count} hits, showing {len(ids)} =====")
    if not ids:
        continue
    rr = requests.post(BASE + "efetch.fcgi", data={"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}, timeout=90)
    root = ET.fromstring(rr.content)
    for art in root.findall(".//PubmedArticle"):
        pmid = art.findtext(".//PMID")
        title = "".join(art.find(".//ArticleTitle").itertext())
        year = art.findtext(".//PubDate/Year") or ""
        journal = art.findtext(".//Journal/Title") or ""
        print(f"{pmid} | {year} | {journal[:40]} | {title[:170]}")

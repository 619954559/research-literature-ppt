"""Retrieve and normalize PubMed records for chronic posterior circulation occlusion recanalization."""
import json
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
OUT = Path(__file__).resolve().parents[1] / "literature"
OUT.mkdir(exist_ok=True)

QUERIES = {
    "Q1_chronic_endovascular": '''("chronic"[tiab] OR "non-acute"[tiab] OR nonacute[tiab] OR "long-standing"[tiab]) AND (vertebrobasilar[tiab] OR "basilar artery"[tiab] OR "vertebral artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab]) AND (endovascular[tiab] OR recanalization[tiab] OR recanalisation[tiab] OR stenting[tiab] OR angioplasty[tiab] OR revascularization[tiab])''',
    "Q2_nonacute_endovascular": '''("non-acute"[tiab] OR nonacute[tiab] OR subacute[tiab] OR "medically refractory"[tiab]) AND (vertebrobasilar[tiab] OR "basilar artery"[tiab] OR "vertebral artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab]) AND (endovascular[tiab] OR recanalization[tiab] OR stenting[tiab] OR angioplasty[tiab])''',
    "Q3_stent_elective": '''(vertebrobasilar[tiab] OR "basilar artery"[tiab] OR "vertebral artery"[tiab] OR "posterior circulation"[tiab]) AND (occlusion[tiab] OR occluded[tiab]) AND (stenting[tiab] OR "stent"[tiab] OR angioplasty[tiab]) AND (elective[tiab] OR "chronic"[tiab] OR "non-acute"[tiab] OR nonacute[tiab] OR "subacute"[tiab])''',
    "Q4_title_specific": '''(("chronic"[ti] OR "non-acute"[ti] OR nonacute[ti] OR subacute[ti]) AND (vertebrobasilar[ti] OR "basilar artery"[ti] OR "vertebral artery"[ti] OR "posterior circulation"[ti]) AND (occlusion[ti] OR occluded[ti]))''',
}


def esearch(term, retmax=500):
    r = requests.get(
        BASE + "esearch.fcgi",
        params={"db": "pubmed", "term": term, "retmode": "json", "retmax": retmax, "sort": "relevance"},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["esearchresult"]["idlist"], int(r.json()["esearchresult"]["count"])


def efetch(pmids):
    records = []
    for i in range(0, len(pmids), 150):
        chunk = pmids[i : i + 150]
        r = requests.post(
            BASE + "efetch.fcgi",
            data={"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"},
            timeout=120,
        )
        r.raise_for_status()
        root = ET.fromstring(r.content)
        for art in root.findall(".//PubmedArticle"):
            records.append(parse_article(art))
        time.sleep(0.4)
    return records


def text(el):
    return "".join(el.itertext()).strip() if el is not None else ""


def parse_article(art):
    med = art.find("MedlineCitation")
    pmid = text(med.find("PMID"))
    article = med.find("Article")
    title = text(article.find("ArticleTitle"))
    journal = text(article.find("Journal/Title"))
    year = ""
    pubdate = article.find("Journal/JournalIssue/PubDate")
    if pubdate is not None:
        year = text(pubdate.find("Year")) or text(pubdate.find("MedlineDate"))[:4]
    authors = []
    for a in article.findall("AuthorList/Author"):
        last = text(a.find("LastName"))
        fore = text(a.find("ForeName")) or text(a.find("Initials"))
        if last:
            authors.append(f"{last} {fore}".strip())
    abstract_parts = []
    for ab in article.findall("Abstract/AbstractText"):
        label = ab.get("Label")
        abstract_parts.append((label + ": " if label else "") + text(ab))
    abstract = "\n".join(abstract_parts)
    dois = []
    for eid in art.findall(".//ArticleIdList/ArticleId"):
        if eid.get("IdType") == "doi":
            dois.append(text(eid))
    ptypes = [text(p) for p in article.findall("PublicationTypeList/PublicationType")]
    mesh = [text(m) for m in art.findall(".//MeshHeadingList/MeshHeading/DescriptorName")]
    return {
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "doi": dois[0] if dois else "",
        "abstract": abstract,
        "pubtypes": ptypes,
        "mesh": mesh,
        "pmid_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


def main():
    all_ids = {}
    counts = {}
    for name, q in QUERIES.items():
        ids, count = esearch(q)
        counts[name] = {"count": count, "retrieved": len(ids)}
        print(name, count, len(ids))
        for p in ids:
            all_ids.setdefault(p, []).append(name)
    print("unique", len(all_ids))
    records = efetch(list(all_ids))
    for rec in records:
        rec["queries"] = all_ids.get(rec["pmid"], [])
    (OUT / "pubmed_raw.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "search_counts.json").write_text(json.dumps(counts, ensure_ascii=False, indent=1), encoding="utf-8")
    with (OUT / "pubmed_raw.tsv").open("w", encoding="utf-8", newline="") as f:
        f.write("pmid\tyear\tjournal\ttitle\tdoi\tauthors\n")
        for rec in sorted(records, key=lambda r: r["year"], reverse=True):
            f.write("\t".join([rec["pmid"], rec["year"], rec["journal"], rec["title"].replace("\t", " "), rec["doi"], "; ".join(rec["authors"][:6])]) + "\n")
    print("saved", len(records))


if __name__ == "__main__":
    main()

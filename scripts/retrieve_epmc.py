"""Fetch Europe PMC records (core metadata incl. abstracts) for the review topic."""
import json
import time
from pathlib import Path

import requests

OUT = Path(__file__).resolve().parents[1] / "literature"
OUT.mkdir(exist_ok=True)

QUERIES = {
    "EPMC_main": '(TITLE_ABS:"chronic" OR TITLE_ABS:"non-acute" OR TITLE_ABS:"nonacute" OR TITLE_ABS:"subacute" OR TITLE_ABS:"long-standing") AND (TITLE_ABS:"vertebrobasilar" OR TITLE_ABS:"basilar artery" OR TITLE_ABS:"vertebral artery" OR TITLE_ABS:"posterior circulation") AND (TITLE_ABS:"occlusion" OR TITLE_ABS:"occluded") AND (TITLE_ABS:"endovascular" OR TITLE_ABS:"recanalization" OR TITLE_ABS:"recanalisation" OR TITLE_ABS:"stenting" OR TITLE_ABS:"angioplasty" OR TITLE_ABS:"revascularization")',
    "EPMC_meta": '(TITLE_ABS:"vertebrobasilar" OR TITLE_ABS:"basilar artery" OR TITLE_ABS:"vertebral artery" OR TITLE_ABS:"posterior circulation") AND (TITLE_ABS:"occlusion") AND (TITLE_ABS:"recanalization" OR TITLE_ABS:"endovascular") AND (TITLE_ABS:"meta-analysis" OR TITLE_ABS:"systematic review")',
    "EPMC_chronic_va": '(TITLE:"chronic" OR TITLE:"non-acute" OR TITLE:"nonacute" OR TITLE:"subacute") AND (TITLE:"vertebral artery" OR TITLE:"vertebrobasilar" OR TITLE:"basilar artery" OR TITLE:"posterior circulation") AND (TITLE:"occlusion" OR TITLE:"occluded")',
}

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
all_recs = {}
for name, q in QUERIES.items():
    cursor = "*"
    page = 0
    while True:
        r = requests.get(
            BASE,
            params={"query": q, "format": "json", "pageSize": 1000, "resultType": "core", "cursorMark": cursor},
            timeout=90,
        )
        r.raise_for_status()
        d = r.json()
        recs = d.get("resultList", {}).get("result", [])
        print(name, "page", page, "got", len(recs), "hit", d.get("hitCount"))
        for rec in recs:
            key = rec.get("pmid") or rec.get("doi") or rec.get("id")
            if not key:
                continue
            rec.setdefault("queries", []).append(name)
            if key in all_recs:
                all_recs[key]["queries"].append(name)
            else:
                all_recs[key] = rec
        nxt = d.get("nextCursorMark")
        if not recs or not nxt or nxt == cursor:
            break
        cursor = nxt
        page += 1
        time.sleep(0.3)
        if page > 5:
            break

records = list(all_recs.values())
for rec in records:
    rec["queries"] = sorted(set(rec.get("queries", [])))
(OUT / "epmc_raw.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")

with (OUT / "epmc_titles.txt").open("w", encoding="utf-8") as f:
    for i, rec in enumerate(records):
        f.write(
            f"{i+1:3d} {rec.get('pubYear','')} | {rec.get('pmid','')} | {rec.get('doi','')} | "
            f"{rec.get('title','')} | {rec.get('journalTitle','')} | OA={rec.get('isOpenAccess','')} | "
            f"inEPMC={rec.get('inEPMC','')} | PMCID={rec.get('pmcid','')}\n"
        )
print("saved", len(records))

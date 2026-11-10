import json
import sys
from pathlib import Path

lit = Path(__file__).resolve().parents[1] / "literature"
recs = json.loads((lit / "pubmed_raw.json").read_text(encoding="utf-8"))
by = {r["pmid"]: r for r in recs}

pmids = sys.argv[1:]
out = []
for p in pmids:
    r = by.get(p)
    if not r:
        out.append(f"## {p}\nNOT FOUND\n")
        continue
    out.append(
        f"## PMID {p} | {r['year']} | {r['journal']}\n"
        f"**{r['title']}**\n\n"
        f"Authors: {', '.join(r['authors'][:8])}\n"
        f"DOI: {r['doi']}\n"
        f"Types: {'; '.join(r['pubtypes'])}\n\n"
        f"{r['abstract']}\n"
    )

path = lit / "candidate_abstracts.md"
path.write_text("\n\n---\n\n".join(out), encoding="utf-8")
print("wrote", path, len(out), "records")

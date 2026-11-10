import json
pm=json.load(open('literature/pubmed_raw.json',encoding='utf-8'))
ep=json.load(open('literature/epmc_raw.json',encoding='utf-8'))
pm_ids={r['pmid'] for r in pm}
pm_dois={r['doi'].lower() for r in pm if r.get('doi')}
extra_pmid=[]; extra_doi=[]; noid=[]
for r in ep:
    p=r.get('pmid'); d=(r.get('doi') or '').lower()
    if p and p in pm_ids: continue
    if d and d in pm_dois: continue
    if p: extra_pmid.append(p)
    elif d: extra_doi.append(d)
    else: noid.append(r.get('id'))
print('pubmed',len(pm),'epmc',len(ep))
print('epmc extra with pmid',len(set(extra_pmid)),'extra doi-only',len(set(extra_doi)),'no id',len(noid))
print('union approx',len(pm_ids|set(extra_pmid))+len(set(extra_doi)))

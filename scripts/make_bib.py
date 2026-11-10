import csv, re
rows=list(csv.DictReader(open('literature/evidence_table.csv',encoding='utf-8')))
def esc(s):
    s=s or ''
    for a,b in [('&',r'\&'),('%',r'\%'),('#',r'\#'),('_',r'\_')]:
        s=s.replace(a,b)
    return s
def key(r):
    first=r['first_author'].split()[0]
    first=re.sub(r'[^A-Za-z]','',first) or 'ref'
    return f"{first}{r['year']}_{r['pmid']}"
with open('literature/references.bib','w',encoding='utf-8') as f:
    for r in rows:
        f.write(f"@article{{{key(r)},\n")
        auths=[]
        for a in r['authors_full'].replace(' et al.','').split(','):
            a=a.strip()
            if not a: continue
            if a.lower().startswith('et al'):
                continue
            parts=a.split()
            if len(parts)>=2:
                auths.append(parts[0]+', '+' '.join(parts[1:]))
            else:
                auths.append(a)
        author_tex=' and '.join(auths)+(' and others' if 'et al' in r['authors_full'] else '')
        f.write(f"  author = {{{esc(author_tex)}}},\n")
        f.write(f"  title = {{{esc(r['title'])}}},\n")
        f.write(f"  journal = {{{esc(r['journal'])}}},\n")
        f.write(f"  year = {{{r['year']}}},\n")
        if r['doi']: f.write(f"  doi = {{{r['doi']}}},\n")
        f.write(f"  pmid = {{{r['pmid']}}},\n")
        f.write(f"  note = {{Ref {r['ref']}}}\n")
        f.write("}\n\n")
print('wrote',len(rows))

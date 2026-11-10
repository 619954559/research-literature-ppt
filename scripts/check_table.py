import csv
rows=list(csv.DictReader(open('literature/evidence_table.csv',encoding='utf-8')))
print('rows',len(rows))
for r in rows: print(r['ref'],r['year'],r['first_author'],r['journal'],'|',r['n'],'|',r['success'][:40])

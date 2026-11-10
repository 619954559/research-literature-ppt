from pptx import Presentation
import re
p=Presentation(r'slides\后循环慢性闭塞再通_组会汇报_30页.pptx')
alltext=[]
for i,s in enumerate(p.slides,1):
    for sh in s.shapes:
        if sh.has_text_frame:
            t=sh.text_frame.text.strip()
            if t: alltext.append((i,t))
bad=[(i,t) for i,t in alltext if re.search(r'(TODO|XXX|lorem|ipsum|None|nan|R\d\d\[)',t,re.I)]
print('slides',len(p.slides),'text shapes',len(alltext),'bad',len(bad))
for b in bad[:20]: print(b)
print('---first slide texts---')
for i,t in alltext[:8]: print(i,repr(t[:80]))

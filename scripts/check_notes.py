from pptx import Presentation
p=Presentation(r'slides\后循环慢性闭塞再通_组会汇报_30页.pptx')
print('slides',len(p.slides))
for i,s in enumerate(p.slides,1):
    note=s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ''
    print(i, len(note), note[:50])

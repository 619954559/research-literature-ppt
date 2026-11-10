"""Export PPTX slides to PNG using the installed PowerPoint COM automation."""
import sys
from pathlib import Path

import win32com.client as win32

pptx = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
for old in out.glob("slide-*.png"):
    old.unlink()

app = win32.DispatchEx("PowerPoint.Application")
app.Visible = True
pres = app.Presentations.Open(str(pptx), ReadOnly=True, WithWindow=False)
try:
    for i, slide in enumerate(pres.Slides, 1):
        target = out / f"slide-{i:02d}.png"
        slide.Export(str(target), "PNG", 1600, 900)
        print("exported", target.name, flush=True)
finally:
    pres.Close()
    app.Quit()
print("done", pres.Slides.Count if False else "")

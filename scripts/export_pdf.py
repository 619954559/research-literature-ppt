"""Export the deck to PDF using PowerPoint COM."""
import sys
from pathlib import Path

import win32com.client as win32

pptx = Path(sys.argv[1]).resolve()
pdf = Path(sys.argv[2]).resolve()
app = win32.DispatchEx("PowerPoint.Application")
app.Visible = True
pres = app.Presentations.Open(str(pptx), ReadOnly=True, WithWindow=False)
try:
    pres.SaveAs(str(pdf), 32)  # ppSaveAsPDF
    print("saved", pdf, pdf.stat().st_size)
finally:
    pres.Close()
    app.Quit()

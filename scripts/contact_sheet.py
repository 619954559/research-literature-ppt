from PIL import Image, ImageDraw
from pathlib import Path
files=sorted(Path('slides/render').glob('slide-*.png'))
print(len(files))
cols,rows=5,6
tw,th=420,236
sheet=Image.new('RGB',(cols*tw,rows*th),'white')
d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
    im=Image.open(f).convert('RGB')
    im.thumbnail((tw-8,th-22))
    x=(i%cols)*tw; y=(i//cols)*th
    sheet.paste(im,(x+4,y+18))
    d.text((x+6,y+3),f.stem,fill='black')
sheet.save('slides/render/contact-sheet.png')
print(sheet.size)

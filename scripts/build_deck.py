"""Build the 30-slide Chinese lab-meeting deck with python-pptx."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "slides" / "assets"
OUT = ROOT / "slides" / "后循环慢性闭塞再通_组会汇报_30页.pptx"

# ---------------- design tokens
INK = RGBColor(0x0E, 0x22, 0x33)
INK2 = RGBColor(0x16, 0x39, 0x4F)
TEAL = RGBColor(0x0B, 0x6E, 0x69)
TEAL2 = RGBColor(0x2A, 0x9D, 0x8F)
TEAL_L = RGBColor(0xDC, 0xEF, 0xEC)
CORAL = RGBColor(0xD9, 0x55, 0x2F)
CORAL_L = RGBColor(0xF7, 0xE2, 0xD9)
GOLD = RGBColor(0xD9, 0xA4, 0x41)
GOLD_L = RGBColor(0xF6, 0xEC, 0xD8)
PAPER = RGBColor(0xF7, 0xF9, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MUTED = RGBColor(0x6C, 0x7F, 0x8B)
LINE = RGBColor(0xD8, 0xE2, 0xE4)
FONT = "Microsoft YaHei"

W, H = 13.333, 7.5


def rgb_hex(c):
    return "%02X%02X%02X" % (c[0], c[1], c[2])


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W)
        self.prs.slide_height = Inches(H)
        self.slides = []

    def blank(self, bg=PAPER):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        rect = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(W), Inches(H))
        rect.fill.solid(); rect.fill.fore_color.rgb = bg
        rect.line.fill.background()
        rect.shadow.inherit = False
        self.slides.append(s)
        return s

    def pic(self, s, name, x, y, w=None, h=None):
        path = ASSETS / name
        if w and h:
            return s.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
        from PIL import Image
        iw, ih = Image.open(path).size
        if w:
            h = w * ih / iw
        elif h:
            w = h * iw / ih
        return s.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))

    def rect(self, s, x, y, w, h, fill=None, line=None, radius=None, lw=1):
        shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius is not None else MSO_SHAPE.RECTANGLE
        sh = s.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid(); sh.fill.fore_color.rgb = fill
        if line is None:
            sh.line.fill.background()
        else:
            sh.line.color.rgb = line; sh.line.width = Pt(lw)
        if radius is not None:
            sh.adjustments[0] = radius
        sh.shadow.inherit = False
        return sh

    def circle(self, s, x, y, d, fill, line=None, lw=1):
        sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        if line is None:
            sh.line.fill.background()
        else:
            sh.line.color.rgb = line; sh.line.width = Pt(lw)
        sh.shadow.inherit = False
        return sh

    def txt(self, s, x, y, w, h, text, size=16, color=INK, bold=False, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, line=1.12, space_after=2, italic=False, font=FONT):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.clear()
        tf.word_wrap = True
        tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
        tf.vertical_anchor = anchor
        paras = text.split("\n")
        for i, ptxt in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.line_spacing = line
            p.space_after = Pt(space_after)
            run = p.add_run()
            run.text = ptxt
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = color
        return tb

    def rich(self, s, x, y, w, h, runs, size=16, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line=1.1):
        """runs: list of (text, size, color, bold) tuples; one paragraph."""
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame; tf.clear(); tf.word_wrap = True
        tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
        tf.vertical_anchor = anchor
        p = tf.paragraphs[0]; p.alignment = align; p.line_spacing = line
        for txt_, sz, col, bd in runs:
            r = p.add_run(); r.text = txt_
            r.font.name = FONT; r.font.size = Pt(sz); r.font.bold = bd; r.font.color.rgb = col
        return tb

    def notes(self, s, text):
        s.notes_slide.notes_text_frame.text = text

    def header(self, s, section, title, dark=False):
        fg = WHITE if dark else INK
        # section chip
        chip_w = 1.55 if len(section) <= 6 else 1.9
        self.rect(s, 0.6, 0.30, chip_w, 0.28, fill=TEAL if not dark else TEAL2, radius=0.5)
        self.txt(s, 0.6, 0.335, chip_w, 0.22, section, size=8.5, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        self.txt(s, 0.6, 0.68, 12.1, 0.62, title, size=27, color=fg, bold=True, line=1.0)

    def footer(self, s, page, source=""):
        self.txt(s, 0.6, 7.12, 10.6, 0.22, source, size=7.5, color=MUTED)
        self.txt(s, 11.55, 7.10, 1.15, 0.24, f"{page:02d} / 30", size=8.5, color=MUTED, align=PP_ALIGN.RIGHT)

    def card(self, s, x, y, w, h, fill=WHITE, line=LINE, radius=0.06):
        return self.rect(s, x, y, w, h, fill=fill, line=line, radius=radius, lw=0.75)

    def chip(self, s, x, y, w, text, fill=TEAL_L, color=TEAL, size=8.5):
        self.rect(s, x, y, w, 0.27, fill=fill, radius=0.5)
        self.txt(s, x, y + 0.045, w, 0.2, text, size=size, color=color, bold=True, align=PP_ALIGN.CENTER)

    def table(self, s, x, y, w, h, data, col_widths, font_size=9, header_size=9,
              header_fill=INK2, header_color=WHITE, zebra=True, row_h=None):
        rows, cols = len(data), len(data[0])
        shape = s.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
        table = shape.table
        table.first_row = True
        table.horz_banding = False
        for i, cw in enumerate(col_widths):
            table.columns[i].width = Inches(cw)
        for ri, row in enumerate(data):
            for ci, val in enumerate(row):
                cell = table.cell(ri, ci)
                cell.margin_left = Inches(0.06)
                cell.margin_right = Inches(0.04)
                cell.margin_top = Inches(0.02)
                cell.margin_bottom = Inches(0.02)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                if ri == 0:
                    cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
                    color, bold, size = header_color, True, header_size
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = WHITE if (not zebra or ri % 2 == 1) else RGBColor(0xF1, 0xF5, 0xF6)
                    color, bold, size = INK, False, font_size
                tf = cell.text_frame
                tf.word_wrap = True
                tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.LEFT if ci > 0 else PP_ALIGN.LEFT
                r = p.add_run(); r.text = str(val)
                r.font.name = FONT; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
        return table


def build():
    d = Deck()

    # ============================================================ 1 cover
    s = d.blank(bg=INK)
    d.pic(s, "fig_hero.png", 0, 0, W, H)
    d.txt(s, 0.85, 1.05, 7.4, 0.3, "组会文献汇报  ·  神经介入", size=12, color=TEAL2, bold=True)
    d.txt(s, 0.85, 1.55, 7.6, 1.9, "后循环慢性闭塞\n再通的证据地图", size=40, color=WHITE, bold=True, line=1.05)
    d.txt(s, 0.85, 3.55, 6.9, 1.0,
          "从 607 条检索记录到 40 篇证据：\n技术成功、并发症、功能结局与患者选择",
          size=16, color=RGBColor(0xC9, 0xDA, 0xDE), line=1.35)
    d.rect(s, 0.87, 4.85, 1.6, 0.03, fill=CORAL)
    d.txt(s, 0.85, 5.02, 6.5, 0.32, "2026-11-11  ·  30 页  ·  建议 35–40 分钟", size=11, color=RGBColor(0xA9, 0xBF, 0xC5))
    d.txt(s, 0.85, 6.62, 6.9, 0.3, "基于 PubMed / Europe PMC 检索；完整文献清单与笔记见 literature/", size=8.5, color=RGBColor(0x7F, 0x9A, 0xA2))
    d.notes(s, "开场：今天汇报后循环慢性/非急性闭塞的血管内再通。重点不是罗列所有文献，而是回答三个问题：谁适合开、开得通吗、开完以后怎么样。最后给出一个可落地的单中心决策路径。")

    # ============================================================ 2 agenda
    s = d.blank()
    d.header(s, "00 · 目录", "今天讲什么：从证据到决策")
    agenda = [
        ("01", "背景与解剖", "后循环负担、时间定义、解剖与机制", "3–7"),
        ("02", "证据与选择", "检索方法、证据地图、影像与患者选择", "8–14"),
        ("03", "结果", "技术成功、并发症、功能结局、再狭窄", "15–20"),
        ("04", "技术", "顺行/逆行/分期、围术期抗栓", "21–22"),
        ("05", "病例", "两例文献病例：进行性缺血与慢性 CTO", "23–24"),
        ("06", "讨论", "证据质量、争议、未来方向、实践路径", "25–30"),
    ]
    for i, (num, t, sub, pages) in enumerate(agenda):
        col = i % 2
        row = i // 2
        x = 0.65 + col * 6.25
        y = 1.55 + row * 1.72
        d.card(s, x, y, 5.95, 1.42, fill=WHITE)
        d.circle(s, x + 0.22, y + 0.28, 0.55, TEAL if i % 2 == 0 else TEAL2)
        d.txt(s, x + 0.22, y + 0.44, 0.55, 0.26, num, size=12, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.txt(s, x + 0.95, y + 0.25, 4.0, 0.32, t, size=17, color=INK, bold=True)
        d.txt(s, x + 0.95, y + 0.68, 4.6, 0.55, sub, size=10.5, color=MUTED, line=1.2)
        d.txt(s, x + 5.05, y + 1.03, 0.7, 0.24, f"p.{pages}", size=9, color=TEAL, bold=True, align=PP_ALIGN.RIGHT)
    d.txt(s, 0.65, 6.72, 7.5, 0.3, "一个主线：技术成功 ≠ 临床获益；选择比技术更重要。", size=10.5, color=TEAL, bold=True)
    d.footer(s, 2, "汇报结构；页码为幻灯片编号")

    # ============================================================ 3 burden
    s = d.blank()
    d.header(s, "01 · 背景", "后循环闭塞：被低估的高危疾病")
    d.rich(s, 0.65, 1.48, 5.6, 1.2, [("20–25", 56, TEAL, True), ("%", 26, TEAL, True)], line=0.9)
    d.txt(s, 0.68, 2.55, 5.2, 0.3, "后循环卒中占全部缺血性卒中的比例", size=10.5, color=MUTED)
    rows = [
        ("1 / 5", "卒中或 TIA 位于后循环；合并椎基底动脉狭窄时早期复发风险高", CORAL),
        ("6–14% / 年", "急性大动脉闭塞存活后、未再通者的复发性卒中风险（文献汇总）", GOLD),
        ("30% vs 10%", "老年非急性 VBAO：保守 vs EVT 的 1 年卒中/死亡（单中心）", TEAL2),
    ]
    for i, (num, txt, col) in enumerate(rows):
        y = 3.02 + i * 1.22
        d.card(s, 0.65, y, 5.55, 1.02, fill=WHITE)
        d.rect(s, 0.65, y, 0.06, 1.02, fill=col)
        d.txt(s, 0.86, y + 0.14, 1.55, 0.34, num, size=15.5, color=col, bold=True)
        d.txt(s, 0.86, y + 0.53, 5.1, 0.42, txt, size=9.5, color=INK, line=1.15)
    d.card(s, 6.55, 1.48, 6.1, 4.9, fill=WHITE)
    d.pic(s, "fig_anatomy.png", 6.72, 1.62, 5.75)
    d.txt(s, 6.75, 5.78, 5.7, 0.5, "后循环由双侧椎动脉、基底动脉及其分支组成；\n脑干穿支与后交通侧支决定缺血的“耐受度”。", size=9.5, color=MUTED, line=1.3)
    d.rect(s, 0.65, 6.4, 12.0, 0.45, fill=TEAL_L, radius=0.1)
    d.txt(s, 0.88, 6.5, 11.6, 0.3, "后循环缺血的“时间”，是侧支与灌注的时间，不是钟表时间。", size=10.5, color=TEAL, bold=True)
    d.footer(s, 3, "来源：[22] 后循环卒中综述；[36] Lancet Neurol 2013；[18] Xia 2023；[2] Li 2026")

    # ============================================================ 4 definitions
    s = d.blank()
    d.header(s, "01 · 背景", "什么叫“慢性”？——时间轴上的灰区")
    # timeline
    d.rect(s, 0.85, 2.12, 11.55, 0.05, fill=LINE)
    marks = [
        (0.95, "0 h", "发病/闭塞"),
        (3.0, "24 h", "急性期边界"),
        (5.3, "2 周", "亚急性"),
        (7.6, "1 个月", "慢性（常用）"),
        (10.1, "3 个月", "组织化/钙化"),
    ]
    for i, (x, t, sub) in enumerate(marks):
        col = CORAL if i <= 1 else (GOLD if i <= 3 else TEAL)
        d.circle(s, x - 0.09, 2.03, 0.18, col, line=WHITE, lw=2)
        d.txt(s, x - 0.55, 1.62, 1.3, 0.3, t, size=11, color=col, bold=True, align=PP_ALIGN.CENTER)
        d.txt(s, x - 0.55, 2.3, 1.3, 0.45, sub, size=8.5, color=MUTED, align=PP_ALIGN.CENTER)
    d.chip(s, 3.05, 2.78, 2.1, "超急性/急性", fill=CORAL_L, color=CORAL)
    d.chip(s, 5.35, 2.78, 1.6, "亚急性", fill=GOLD_L, color=RGBColor(0x9A, 0x6B, 0x12))
    d.chip(s, 7.15, 2.78, 2.25, "非急性（工作定义）", fill=TEAL_L, color=TEAL)
    d.chip(s, 9.55, 2.78, 2.05, "慢性 / 晚期", fill=TEAL_L, color=TEAL)
    cards = [
        ("文献并不统一", "24 h、2 周、3 周、1 个月、3 个月都有人用；\n直接比较不同队列的成功率要非常谨慎。", "[18][19][30]"),
        ("本汇报的工作定义", "非急性：症状/影像确认闭塞 >24 h；\n慢性：>1 个月；>3 个月单独标注。", "便于讨论，不是共识"),
        ("为什么重要", "定义越晚，血栓机化/钙化越重，\n再通更难、并发症更高、选择偏倚更大。", "[7][19]"),
    ]
    for i, (t, body, tag) in enumerate(cards):
        x = 0.65 + i * 4.15
        d.card(s, x, 3.55, 3.9, 2.35, fill=WHITE)
        d.txt(s, x + 0.25, 3.75, 3.4, 0.3, t, size=13.5, color=TEAL, bold=True)
        d.txt(s, x + 0.25, 4.2, 3.4, 1.1, body, size=10, color=INK, line=1.35)
        d.txt(s, x + 0.25, 5.38, 3.4, 0.25, tag, size=8, color=MUTED)
    impacts = ["→ 纳入时保留原始界值", "→ 本汇报统一标注", "→ 比较前先看定义"]
    for i, imp in enumerate(impacts):
        d.txt(s, 0.9 + i * 4.15, 5.02, 3.45, 0.3, imp, size=9.5, color=TEAL, bold=True)
    d.txt(s, 0.65, 6.25, 12.0, 0.55,
          "本汇报采用“非急性 >24 h、慢性 >1 个月”的工作定义；引用研究时保留其原始界值，不把不同定义的结果直接合并。",
          size=10, color=MUTED, line=1.25)
    d.footer(s, 4, "来源：[18] Xia 2023（>3 周）；[19] Zhou 2023（>24 h，<3 个月）；[30] 中国专家共识 2020")

    # ============================================================ 5 anatomy
    s = d.blank()
    d.header(s, "01 · 背景", "解剖决定风险：从 V4 到基底动脉")
    d.pic(s, "fig_anatomy.png", 0.55, 1.45, 7.35)
    d.card(s, 8.15, 1.45, 4.55, 5.35, fill=WHITE)
    d.txt(s, 8.4, 1.62, 4.0, 0.3, "三个关键点", size=14, color=TEAL, bold=True)
    items = [
        ("01", "V4 / 基底动脉穿支丰富", "供应脑干、脑桥；损伤后后果重。"),
        ("02", "PICA / AICA / SCA", "小脑与脑干的分支；闭塞范围决定症状。"),
        ("03", "侧支是“缓冲垫”", "后交通动脉、前脊髓动脉、软脑膜侧支。"),
    ]
    for i, (num, t, body) in enumerate(items):
        y = 2.12 + i * 1.05
        d.circle(s, 8.4, y, 0.38, TEAL_L)
        d.txt(s, 8.4, y + 0.075, 0.38, 0.22, num, size=8.5, color=TEAL, bold=True, align=PP_ALIGN.CENTER)
        d.txt(s, 8.92, y - 0.02, 3.55, 0.28, t, size=11.5, color=INK, bold=True)
        d.txt(s, 8.92, y + 0.3, 3.55, 0.45, body, size=9, color=MUTED, line=1.2)
    d.rect(s, 8.4, 5.35, 4.0, 0.02, fill=LINE)
    d.txt(s, 8.4, 5.48, 3.95, 1.0,
          "临床含义：基底动脉闭塞的再通风险高于颅内椎动脉；\n本组数据中 BA 并发症 30% vs VA 16.2% [19]。",
          size=9.5, color=CORAL, line=1.35)
    d.footer(s, 5, "示意图：作者绘制，非患者影像；参考 [19] Zhou 2023、[21] Gao 2022")

    # ============================================================ 6 mechanisms
    s = d.blank()
    d.header(s, "01 · 背景", "四条机制，一个共同终点")
    mech = [
        ("AS", "动脉粥样硬化", "斑块进展 → 管腔闭塞；\n斑块内出血/破裂 → 原位血栓。", TEAL),
        ("HP", "低灌注", "侧支不足 → 分水岭/脑干低灌注；\n反复 TIA、体位相关症状。", GOLD),
        ("EM", "栓塞", "残端血栓、斑块碎屑 → 远端栓塞；\n后循环“ stump syndrome”。", CORAL),
        ("CS", "侧支失代偿", "后交通/软脑膜侧支耗竭 → 症状进展；\n决定“时间窗”而非钟表时间。", TEAL2),
    ]
    clues = ["危险因素：高血压、糖尿病、吸烟", "影像：CTP/ASL 低灌注", "影像：DWI 多发散在梗死", "决策：侧支分级与时间窗"]
    for i, (code, t, body, col) in enumerate(mech):
        x = 0.65 + (i % 2) * 6.1
        y = 1.55 + (i // 2) * 2.3
        d.card(s, x, y, 5.85, 2.02, fill=WHITE)
        d.circle(s, x + 0.25, y + 0.26, 0.58, col)
        d.txt(s, x + 0.25, y + 0.43, 0.58, 0.24, code, size=10, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.txt(s, x + 1.0, y + 0.24, 4.5, 0.3, t, size=15, color=INK, bold=True)
        d.txt(s, x + 1.0, y + 0.72, 4.55, 0.75, body, size=10.5, color=MUTED, line=1.3)
        d.txt(s, x + 1.0, y + 1.55, 4.55, 0.3, clues[i], size=8.8, color=col, bold=True)
    d.rect(s, 0.65, 6.12, 12.05, 0.58, fill=TEAL_L, radius=0.1)
    d.txt(s, 0.9, 6.25, 11.5, 0.3, "共同终点：脑干 / 小脑缺血 → 复发 TIA、进展性卒中、残疾或死亡", size=12, color=TEAL, bold=True)
    d.footer(s, 6, "机制综述见 [13][16][27]；临床表型见 [17][19]")

    # ============================================================ 7 natural history
    s = d.blank()
    d.header(s, "01 · 背景", "慢性闭塞不等于良性：谁在冒险？")
    d.card(s, 0.65, 1.45, 5.55, 5.3, fill=WHITE)
    d.txt(s, 0.9, 1.62, 4.9, 0.3, "同一诊断，两种命运", size=14, color=TEAL, bold=True)
    d.rich(s, 0.9, 2.1, 4.8, 0.85, [("30%", 34, CORAL, True), (" vs ", 22, MUTED, False), ("10%", 34, TEAL, True)], line=0.9)
    d.txt(s, 0.92, 2.9, 4.9, 0.45, "1 年卒中/死亡：保守治疗 vs EVT（老年 NAIVBAO）[2]", size=9.5, color=MUTED, line=1.2)
    d.txt(s, 0.92, 3.48, 4.9, 0.55, "自然病程队列：15 例慢性 BAO 中 5 例偶然发现、4 例仅轻症；均见后交通侧支 [17]。",
          size=10, color=INK, line=1.3)
    d.txt(s, 0.92, 4.35, 4.9, 0.55, "未再通的急性大动脉闭塞存活者，年复发卒中约 6–14%（文献汇总）[18]。",
          size=10, color=INK, line=1.3)
    d.txt(s, 0.92, 5.35, 4.9, 0.7, "提示：再通队列是“高危 + 可开通”的选择人群，\n不能把单中心结果外推到所有慢性闭塞。",
          size=9.5, color=CORAL, line=1.35)
    # right two phenotypes
    d.card(s, 6.55, 1.45, 6.1, 2.45, fill=TEAL_L, line=None)
    d.chip(s, 6.78, 1.62, 1.1, "表型 A", fill=WHITE, color=TEAL)
    d.txt(s, 6.78, 2.0, 5.6, 0.3, "代偿良好：无症状 / 轻症、稳定", size=13, color=TEAL, bold=True)
    d.txt(s, 6.78, 2.42, 5.55, 0.9, "可观察 + 强化危险因素控制；\n不必为了“影像好看”而再通。", size=10.5, color=INK, line=1.3)
    d.card(s, 6.55, 4.12, 6.1, 2.45, fill=CORAL_L, line=None)
    d.chip(s, 6.78, 4.29, 1.1, "表型 B", fill=WHITE, color=CORAL)
    d.txt(s, 6.78, 4.67, 5.6, 0.3, "低灌注 / 复发：进展性症状", size=13, color=CORAL, bold=True)
    d.txt(s, 6.78, 5.09, 5.55, 0.9, "评估再通：影像选择 + 解剖可行性；\n这是目前最有争议、也最需要 RCT 的人群。", size=10.5, color=INK, line=1.3)
    d.footer(s, 7, "来源：[2] Li 2026；[17] Roth 2024；[18] Xia 2023")

    # ============================================================ 8 imaging overview
    s = d.blank()
    d.header(s, "02 · 证据与选择", "影像评估：从管腔到脑组织")
    layers = [
        ("01", "血管解剖", "CTA / DSA", "闭塞部位、长度、残端形态、远端重建、侧支与入路", TEAL),
        ("02", "管壁与斑块", "HR-MRI / HR-VWI", "斑块性质、残留管腔、夹层/血栓、血管壁炎症", TEAL2),
        ("03", "脑组织", "CTP / PWI / DWI / ASL", "梗死核心、低灌注区、侧支代偿、可挽救组织", GOLD),
    ]
    details = [
        "· 闭塞长度与形态\n· 远端重建与侧支\n· 入路与弓型",
        "· 斑块强化/残留管腔\n· 夹层 vs 血栓\n· 再通预测评分",
        "· 梗死核心 vs 低灌注\n· 侧支分级\n· 术后高灌注风险",
    ]
    for i, (num, t, mod, body, col) in enumerate(layers):
        x = 0.65 + i * 4.12
        y = 1.55
        d.card(s, x, y, 3.85, 3.55, fill=WHITE)
        d.rect(s, x, y, 3.85, 0.12, fill=col)
        d.txt(s, x + 0.25, y + 0.3, 3.3, 0.2, num, size=9, color=col, bold=True)
        d.txt(s, x + 0.25, y + 0.62, 3.35, 0.32, t, size=15, color=INK, bold=True)
        d.txt(s, x + 0.25, y + 1.05, 3.35, 0.28, mod, size=10, color=col, bold=True)
        d.txt(s, x + 0.25, y + 1.5, 3.35, 1.1, body, size=9.6, color=MUTED, line=1.35)
        d.txt(s, x + 0.25, y + 2.5, 3.35, 0.95, details[i], size=8.8, color=INK, line=1.3)
    d.card(s, 0.65, 5.32, 12.0, 1.2, fill=INK2, line=None)
    d.txt(s, 0.9, 5.47, 2.0, 0.3, "决策四问", size=12, color=WHITE, bold=True)
    qs = ["① 是否真闭塞？", "② 能否开通？", "③ 值不值得开？", "④ 风险多大？"]
    for i, q in enumerate(qs):
        d.txt(s, 2.55 + i * 2.55, 5.48, 2.35, 0.5, q, size=11, color=WHITE, bold=False)
    d.txt(s, 2.55, 5.92, 9.8, 0.35, "分别对应：血管解剖 / 形态与器械 / 灌注与梗死 / 风险分层", size=8.5, color=RGBColor(0xB9, 0xCD, 0xD2))
    d.footer(s, 8, "影像策略综合自 [12][13][18][19][21]")

    # ============================================================ 9 morphology
    s = d.blank()
    d.header(s, "02 · 证据与选择", "四个形态学问题，决定“开得通吗”")
    d.pic(s, "fig_morphology.png", 0.55, 1.55, 8.65)
    d.card(s, 9.35, 1.5, 3.4, 5.3, fill=WHITE)
    d.txt(s, 9.55, 1.65, 3.0, 0.3, "术前的四个判断", size=12.5, color=TEAL, bold=True)
    bullets = [
        ("锥形残端", "再通率 90.9% vs 非锥形 40% [15]"),
        ("钝头残端", "失败率 27.3%；占全部失败 85.7% [19]"),
        ("长度 >30 mm", "再通失败 OR 0.144 [7]"),
        ("远端代偿差", "再通失败 OR 0.25 [7]"),
        ("钙化 / 成角", "独立负向因素 [18]"),
    ]
    y = 2.15
    for t, body in bullets:
        d.circle(s, 9.55, y + 0.06, 0.12, CORAL if "钝头" in t or "远端" in t else TEAL)
        d.txt(s, 9.78, y - 0.02, 2.8, 0.26, t, size=10.5, color=INK, bold=True)
        d.txt(s, 9.78, y + 0.27, 2.8, 0.5, body, size=8.8, color=MUTED, line=1.2)
        y += 0.82
    d.rect(s, 0.55, 5.45, 8.65, 0.7, fill=TEAL_L, radius=0.1)
    d.txt(s, 0.78, 5.56, 8.2, 0.45, "结论：先看残端与远端代偿，再决定是否尝试；长度只是参考。", size=9.8, color=TEAL, bold=True)
    d.txt(s, 0.7, 6.38, 8.5, 0.3, "示意图：作者绘制，用于说明形态学差异，非患者原始影像。", size=8, color=MUTED)
    d.footer(s, 9, "来源：[15] Liu 2024；[19] Zhou 2023；[7] Liu 2025；[18] Xia 2023")

    # ============================================================ 10 advanced imaging
    s = d.blank()
    d.header(s, "02 · 证据与选择", "高级影像：把“可能获益”变成可测量")
    cols = [
        ("HR-MRI / HR-VWI", TEAL, [
            "残留管腔、明显斑块强化、长度 ≤10.2 mm",
            "预测评分：再通率 50% → 100% [12]",
            "VBA 再通率低于 MCA；管壁成像可鉴别夹层/血栓",
        ]),
        ("CTP / ASL / PWI", GOLD, [
            "低灌注区、MTT 延长、CBF 下降",
            "识别“低灌注型”表型：反复 TIA、体位相关",
            "病例中 RAPID 发现大片低灌注，促成再通决策 [4]",
        ]),
        ("DSA 侧支与分型", CORAL, [
            "Gao 分型：I 型再通 90%，III 型 50% [21]",
            "EVAO A 型再通 100%，D 型 63.6% [20]",
            "远端重建 = 再通的“出口”",
        ]),
    ]
    uses = ["用途：术前预测再通概率", "用途：识别可挽救的低灌注组织", "用途：分型与入路规划"]
    for i, (t, col, items) in enumerate(cols):
        x = 0.65 + i * 4.12
        d.card(s, x, 1.55, 3.85, 4.25, fill=WHITE)
        d.rect(s, x, 1.55, 0.08, 4.25, fill=col)
        d.txt(s, x + 0.3, 1.72, 3.25, 0.3, t, size=13.5, color=col, bold=True)
        for j, it in enumerate(items):
            d.txt(s, x + 0.3, 2.2 + j * 0.9, 3.3, 0.75, "· " + it, size=9.6, color=INK, line=1.3)
        d.txt(s, x + 0.3, 4.95, 3.3, 0.55, uses[i], size=8.6, color=col, bold=True)
    d.rect(s, 0.65, 6.02, 12.0, 0.55, fill=TEAL_L, radius=0.1)
    d.txt(s, 0.88, 6.15, 11.6, 0.3, "没有单一指标能独立决策：临床表型 × 灌注 × 解剖，三者缺一不可。", size=11, color=TEAL, bold=True)
    d.footer(s, 10, "来源：[12] Zhou 2025 HR-MRI；[4] Yamada 2026；[21] Gao 2022；[20] Gao 2022 EVAO")

    # ============================================================ 11 selection
    s = d.blank()
    d.header(s, "02 · 证据与选择", "谁适合再通？——四条建议 + 四条排除")
    d.card(s, 0.65, 1.5, 5.9, 4.55, fill=TEAL_L, line=None)
    d.chip(s, 0.9, 1.68, 1.55, "建议评估", fill=WHITE, color=TEAL)
    good = [
        ("最佳药物下仍复发/进展", "TIA、进展性卒中、反复跌倒/眩晕"),
        ("低灌注或反复栓塞证据", "CTP/PWI/ASL、HR-MRI、DSA 侧支"),
        ("可再通解剖", "锥形残端、短段、远端重建、入路可行"),
        ("梗死负担可控", "脑干功能尚可、生活预期合理"),
    ]
    for i, (t, body) in enumerate(good):
        y = 2.12 + i * 0.9
        d.circle(s, 0.95, y + 0.03, 0.22, TEAL)
        d.txt(s, 0.95, y + 0.06, 0.22, 0.14, "✓", size=7, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.txt(s, 1.3, y - 0.02, 4.9, 0.28, t, size=11, color=INK, bold=True)
        d.txt(s, 1.3, y + 0.3, 4.9, 0.28, body, size=8.8, color=MUTED)
    d.card(s, 6.8, 1.5, 5.85, 4.55, fill=CORAL_L, line=None)
    d.chip(s, 7.05, 1.68, 1.55, "谨慎 / 禁忌", fill=WHITE, color=CORAL)
    bad = [
        ("大面积脑干梗死 / 昏迷", "再通难以逆转已完成的损伤"),
        ("长段钙化、无远端流出道", "开通概率低、并发症高"),
        ("无残端且无法建立逆行入路", "技术失败风险高"),
        ("严重合并症 / 无法抗栓", "风险 > 潜在获益"),
    ]
    for i, (t, body) in enumerate(bad):
        y = 2.12 + i * 0.9
        d.circle(s, 7.1, y + 0.03, 0.22, CORAL)
        d.txt(s, 7.1, y + 0.06, 0.22, 0.14, "×", size=8, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.txt(s, 7.45, y - 0.02, 4.8, 0.28, t, size=11, color=INK, bold=True)
        d.txt(s, 7.45, y + 0.3, 4.8, 0.28, body, size=8.8, color=MUTED)
    d.rect(s, 0.65, 6.2, 12.0, 0.55, fill=WHITE, line=LINE, radius=0.1)
    d.txt(s, 0.9, 6.32, 11.5, 0.3, "决策公式：症状复发/进展 × 低灌注证据 × 可再通解剖 ÷ 手术风险 —— 高危解剖不强行再通 [14]。",
          size=10.3, color=INK, bold=True)
    d.footer(s, 11, "来源：[7][14][18][19][21][30]")

    # ============================================================ 12 search
    s = d.blank()
    d.header(s, "02 · 证据与选择", "证据从哪来：607 → 331 → 40")
    # flow boxes
    boxes = [
        (1.55, "607", "初检记录", "PubMed 181\nEurope PMC 289\n补充检索 137", TEAL),
        (4.55, "331", "去重后", "按 PMID / DOI 去重\n补充检索新增 5 条", TEAL2),
        (7.55, "40", "纳入详细提取", "13 篇开放全文\n（7 PDF + 6 篇 XML-only）\n27 篇题录/摘要", GOLD),
    ]
    for x, num, t, sub, col in boxes:
        d.card(s, x, 1.55, 2.55, 2.05, fill=WHITE)
        d.txt(s, x + 0.18, 1.68, 2.2, 0.55, num, size=31, color=col, bold=True)
        d.txt(s, x + 0.18, 2.25, 2.2, 0.25, t, size=10.5, color=INK, bold=True)
        d.txt(s, x + 0.18, 2.58, 2.2, 0.9, sub, size=8.5, color=MUTED, line=1.25)
    for x in (4.15, 7.15):
        ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(2.38), Inches(0.32), Inches(0.32))
        ar.fill.solid(); ar.fill.fore_color.rgb = MUTED; ar.line.fill.background(); ar.shadow.inherit = False
    # search box
    d.card(s, 0.65, 3.95, 7.4, 1.95, fill=INK2, line=None)
    d.txt(s, 0.9, 4.1, 6.9, 0.25, "检索式（PubMed / Europe PMC）", size=9.5, color=TEAL2, bold=True)
    d.txt(s, 0.9, 4.42, 6.9, 1.85,
          '("chronic" OR "non-acute" OR nonacute OR "subacute")\nAND (vertebrobasilar OR "basilar artery" OR "vertebral artery"\nOR "posterior circulation")\nAND (occlusion OR occluded)\nAND (endovascular OR recanalization OR stenting OR angioplasty)',
          size=8.3, color=RGBColor(0xD5, 0xE3, 0xE6), line=1.35)
    d.card(s, 8.25, 3.95, 4.4, 1.95, fill=WHITE)
    d.txt(s, 8.48, 4.1, 3.9, 0.25, "筛选策略", size=10, color=TEAL, bold=True)
    d.txt(s, 8.48, 4.45, 3.95, 1.75,
          "· 标题/摘要：后循环 + 慢性/非急性 + 再通\n· 排除：仅急性、前循环、动脉瘤/夹层/外伤\n· 纳入：有结局数据的队列/病例/综述\n· 单检索人、叙述性筛选（非严格 PRISMA）",
          size=8.6, color=INK, line=1.35)
    d.rect(s, 0.65, 6.08, 12.0, 0.42, fill=CORAL_L, radius=0.1)
    d.txt(s, 0.88, 6.17, 11.5, 0.3, "检索局限：单检索人、未用 Embase/CNKI、定义异质；因此只做叙述性综合。", size=9.2, color=CORAL, bold=True)
    d.txt(s, 0.65, 6.62, 11.8, 0.3, "全部检索式、命中数与排除标准见 literature/01_search_strategy.md。", size=8, color=MUTED)
    d.footer(s, 12, "检索日期 2026-11-11；数据库：PubMed、Europe PMC；未使用 Embase/CNKI")

    # ============================================================ 13 evidence map
    s = d.blank()
    d.header(s, "02 · 证据与选择", "证据地图：小样本、单中心、近五年加速")
    d.pic(s, "fig_evidence_map.png", 0.55, 1.55, 7.55)
    d.card(s, 8.35, 1.5, 4.4, 5.25, fill=WHITE)
    d.txt(s, 8.58, 1.65, 3.9, 0.3, "读数", size=12, color=TEAL, bold=True)
    stats = [
        ("20+", "再通队列；样本量 7–177"),
        ("177", "最大单中心（VBA 亚组 58）[18]"),
        ("115", "最大非急性 BAO 队列 [7]"),
        ("0", "随机对照试验（本组文献）"),
    ]
    for i, (num, body) in enumerate(stats):
        y = 2.12 + i * 1.02
        d.rich(s, 8.58, y, 3.9, 0.45, [(num, 24, TEAL if i < 3 else CORAL, True), ("  " + body, 9, INK, False)], line=1.0)
    d.rect(s, 8.58, 6.05, 3.85, 0.02, fill=LINE)
    d.txt(s, 8.58, 6.15, 3.9, 0.5, "气泡大小 = 样本量；颜色 = 闭塞部位。", size=8, color=MUTED)
    d.footer(s, 13, "来源：本汇报纳入的 18 项再通队列；详见 literature/02_literature_table.md")

    # ============================================================ 14 study table
    s = d.blank()
    d.header(s, "02 · 证据与选择", "核心研究一览：设计、人群、再通率")
    data = [
        ["研究", "设计", "人群", "N", "再通", "并发症"],
        ["Liu 2025 [7]", "单中心回顾", "非急性 BAO", "115", "81.7%", "NR"],
        ["Zhou 2023 [19]", "单中心回顾", "非急性 VBAO", "88", "92.0%", "19.3%"],
        ["Chen 2024 [14]", "单中心回顾", "非急性 ICVA", "92", "83.7%", "10.9%"],
        ["Xia 2023 [18]", "单中心回顾", "非急性颅内（VBA 58）", "177", "82.8%*", "5.2%*"],
        ["Gao 2022 [21]", "多中心回顾", "非急性 BAO", "42", "76.2%", "14.3%"],
        ["Gao 2022 [20]", "多中心回顾", "非急性 EVAO", "50", "86.0%", "12.0%"],
        ["Zhao 2020 [28]", "单中心回顾", "非急性 ICVA", "31", "87.1%", "19.4%"],
        ["Gao 2020 [26]", "单中心回顾", "非急性 ICVA", "50", "76.0%", "4.0%†"],
        ["Zhao 2019 [31]", "单中心回顾", "亚急性–慢性 BAO", "21", "81.0%", "9.5%"],
        ["Cai 2021 [23]", "单中心回顾", "慢性 VA 起始部", "22", "86.4%", "NR"],
        ["Liu 2024 [15]", "单中心回顾", "非急性 VOO", "21", "66.7%", "14.3%"],
        ["Zhang 2025 [11]", "单中心回顾", "慢性颅内（含 VBA）", "103", "68.9%", "10.7%"],
    ]
    d.table(s, 0.55, 1.5, 12.25, 5.25, data,
            [1.65, 1.45, 3.5, 0.7, 1.1, 1.25], font_size=9, header_size=9)
    d.txt(s, 0.55, 6.82, 11.5, 0.3, "NR 未报告；* Xia 2023 为 VBA 亚组；† Gao 2020 为 30 d 卒中/死亡。", size=7.5, color=MUTED)
    d.footer(s, 14, "完整 40 篇见 literature/02_literature_table.md")

    # ============================================================ 15 success forest
    s = d.blank()
    d.header(s, "03 · 结果", "技术成功：80%–90% 是“选择性结果”")
    d.pic(s, "fig_success_forest.png", 0.45, 1.45, 7.7)
    d.card(s, 8.35, 1.5, 4.4, 5.2, fill=WHITE)
    d.txt(s, 8.58, 1.65, 3.9, 0.3, "怎么读", size=12, color=TEAL, bold=True)
    d.rich(s, 8.58, 2.05, 3.95, 0.85, [("87%", 32, TEAL, True), ("  总体再通率", 11, INK, False)], line=0.9)
    d.txt(s, 8.58, 2.75, 3.95, 0.45, "95% CI 84–91；I²=78%（23 项研究）[1]", size=8.8, color=MUTED)
    d.txt(s, 8.58, 3.25, 3.95, 1.6,
          "· 单中心范围 66.7%–96%\n· 失败集中于：钝头、长段、钙化、远端代偿差\n· 技术成功 ≠ 功能获益：还要看并发症与选择",
          size=9.3, color=INK, line=1.4)
    d.rect(s, 8.58, 5.25, 3.9, 0.02, fill=LINE)
    d.txt(s, 8.58, 5.4, 3.95, 1.1, "注意：各研究定义、随访、中心量级不同；\n不能把 87% 当作“普遍成功率”。", size=9, color=CORAL, line=1.35)
    d.footer(s, 15, "森林图：本汇报按原始研究报告值绘制 Wilson 95% CI；虚线为 [1] 的 Meta 汇总值")

    # ============================================================ 16 predictors
    s = d.blank()
    d.header(s, "03 · 结果", "为什么开不通？——四个可术前识别的因素")
    d.pic(s, "fig_predictors.png", 0.55, 1.55, 7.35)
    d.card(s, 8.15, 1.5, 4.55, 5.25, fill=WHITE)
    d.txt(s, 8.38, 1.65, 4.0, 0.3, "把 OR 变成谈话", size=12, color=TEAL, bold=True)
    d.txt(s, 8.38, 2.05, 4.05, 3.0,
          "· 闭塞 >3 个月：OR 0.19（0.05–0.69）\n· 钝头残端：OR 0.24（0.07–0.78）\n· 长度 >30 mm：OR 0.14（0.03–0.67）\n· 远端代偿不足：OR 0.25（0.08–0.84）\n\n来源：Liu 2025 的 115 例 NABAO [7]",
          size=9.3, color=INK, line=1.45)
    d.txt(s, 8.38, 4.12, 4.0, 0.8, "怎么用：\n① 术前谈话：失败概率  ② 选择入路/器械\n③ 设定“何时停止”的阈值", size=8.8, color=TEAL, line=1.35)
    d.rect(s, 8.38, 4.95, 4.0, 0.02, fill=LINE)
    d.txt(s, 8.38, 5.1, 4.05, 1.35,
          "形态 > 长度：Zhou 2023 中长度本身不是独立因素，\n钝头形态占失败的 85.7% [19]。\nHR-MRI 评分可进一步细化 [12]。",
          size=8.8, color=MUTED, line=1.35)
    d.footer(s, 16, "来源：[7] Liu 2025；[19] Zhou 2023；[12] Zhou 2025；[15] Liu 2024")

    # ============================================================ 17 complications
    s = d.blank()
    d.header(s, "03 · 结果", "并发症：10%–20% 的现实，不能只看成功率")
    d.pic(s, "fig_complications.png", 0.55, 1.55, 7.15)
    d.card(s, 8.0, 1.5, 4.7, 5.25, fill=WHITE)
    d.txt(s, 8.22, 1.65, 4.25, 0.3, "四类要命 / 要功能的并发症", size=11.5, color=TEAL, bold=True)
    comps = [
        ("夹层 / 穿孔", "脑干穿支损伤；BA 风险更高 [19]", CORAL),
        ("血栓 / 远端栓塞", "穿支或皮层梗死；远端保护证据有限 [6]", GOLD),
        ("出血", "高灌注、SAH、脑实质出血", CORAL),
        ("支架内血栓 / 再闭塞", "术后急性事件；需强化抗栓", TEAL),
    ]
    for i, (t, body, col) in enumerate(comps):
        y = 2.12 + i * 0.95
        d.rect(s, 8.22, y + 0.03, 0.08, 0.62, fill=col)
        d.txt(s, 8.45, y, 3.95, 0.25, t, size=10.2, color=INK, bold=True)
        d.txt(s, 8.45, y + 0.29, 3.95, 0.45, body, size=8.5, color=MUTED, line=1.2)
    d.rect(s, 8.22, 6.02, 4.2, 0.02, fill=LINE)
    d.txt(s, 8.22, 6.12, 4.25, 0.5, "Meta 汇总 13%（10–15）；本组范围 5.2%–25% [1]。", size=8.5, color=CORAL, line=1.25)
    d.footer(s, 17, "来源：[1] Meta；[6] Li 2025；[19] Zhou 2023；[33] He 2014")

    # ============================================================ 18 outcomes
    s = d.blank()
    d.header(s, "03 · 结果", "功能结局：成功再通者多数获益，但“成功”是前提")
    d.pic(s, "fig_outcomes.png", 0.55, 1.55, 7.1)
    d.card(s, 7.95, 1.5, 4.75, 5.25, fill=WHITE)
    d.txt(s, 8.18, 1.65, 4.3, 0.3, "数字背后的前提", size=12, color=TEAL, bold=True)
    d.txt(s, 8.18, 2.08, 4.3, 1.6,
          "· mRS 0–2：约 74%–79%\n· mRS 0–3：约 85%–94%\n· 1 年卒中：11.4% [19]\n· 30 d 后卒中/死亡：17.4% [14]\n· Meta 长期复发/死亡：7% [1]",
          size=9.5, color=INK, line=1.45)
    d.rect(s, 8.18, 4.55, 4.2, 0.02, fill=LINE)
    d.txt(s, 8.18, 4.65, 4.3, 0.7, "选择偏倚：基线轻症、仅成功再通者进入 mRS 分析。", size=8.8, color=CORAL, bold=True, line=1.25)
    d.txt(s, 8.18, 5.35, 4.3, 1.0, "这些是“成功再通 + 严格选择”的队列；\n老年 EVT vs 保守：mRS 0–3 80% vs 60% [2]。",
          size=8.8, color=MUTED, line=1.3)
    d.footer(s, 18, "来源：[2][14][19][24][28][31]")

    # ============================================================ 19 restenosis
    s = d.blank()
    d.header(s, "03 · 结果", "再狭窄：15% 的“长期账单”")
    d.pic(s, "fig_restenosis.png", 0.55, 1.55, 7.0)
    d.card(s, 7.85, 1.5, 4.85, 5.25, fill=WHITE)
    d.txt(s, 8.08, 1.65, 4.4, 0.3, "为什么重要", size=12, color=TEAL, bold=True)
    d.rich(s, 8.08, 2.05, 4.3, 0.8, [("15%", 32, CORAL, True), ("  再狭窄/再闭塞", 11, INK, False)], line=0.9)
    d.txt(s, 8.08, 2.72, 4.4, 0.35, "95% CI 13–18；I²=17% [1]", size=8.5, color=MUTED)
    d.txt(s, 8.08, 3.15, 4.4, 2.0,
          "· 高危解剖组可高达 80% [14]\n· 后扩张与再狭窄相关：OR 4.55 [19]\n· 6–12 个月 DSA/CTA 随访\n· 处理：药物涂层球囊/再次支架？证据不足\n· 抗栓依从性是可控因素",
          size=9.4, color=INK, line=1.45)
    d.rect(s, 8.08, 5.55, 4.2, 0.02, fill=LINE)
    d.txt(s, 8.08, 5.68, 4.4, 0.7, "再狭窄 ≠ 临床失败；但需要纳入随访与终点定义。", size=8.8, color=MUTED, line=1.3)
    d.footer(s, 19, "来源：[1][14][19][23][28]")

    # ============================================================ 20 failure
    s = d.blank()
    d.header(s, "03 · 结果", "再通失败：不只是“没开通”")
    d.card(s, 0.65, 1.55, 5.35, 4.95, fill=INK2, line=None)
    d.txt(s, 0.9, 1.75, 4.8, 0.3, "成功 vs 失败", size=11, color=TEAL2, bold=True)
    d.rich(s, 0.9, 2.15, 4.9, 1.1, [("OR 0.15", 42, WHITE, True)], line=0.95)
    d.txt(s, 0.92, 3.18, 4.8, 0.55, "长期卒中复发/死亡（成功 vs 失败）\n95% CI 0.06–0.37 [1]", size=9.5, color=RGBColor(0xC9, 0xDA, 0xDE), line=1.3)
    d.txt(s, 0.92, 4.2, 4.8, 1.8,
          "但这不是随机比较：\n失败组病变更复杂、并发症更多。\nOR 0.15 不能直接解释为“再通的因果获益”。",
          size=9.5, color=RGBColor(0xE8, 0xF0, 0xF1), line=1.45)
    # cascade right
    d.card(s, 6.35, 1.55, 6.35, 4.95, fill=WHITE)
    d.txt(s, 6.6, 1.72, 5.8, 0.3, "失败之后发生了什么？——Chen 2024 的 15 例失败", size=11, color=CORAL, bold=True)
    cascade = [
        ("15", "导丝无法通过而终止"),
        ("4", "围手术期缺血性卒中"),
        ("2", "围手术期颅内出血"),
        ("17.4%", "30 d 后卒中/死亡（92 例）"),
    ]
    for i, (num, body) in enumerate(cascade):
        y = 2.2 + i * 0.95
        d.txt(s, 6.6, y, 1.4, 0.5, num, size=24, color=CORAL if i < 3 else INK, bold=True)
        d.txt(s, 8.05, y + 0.12, 4.4, 0.35, body, size=10, color=INK)
        if i < 3:
            ar = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.95), Inches(y + 0.55), Inches(0.18), Inches(0.28))
            ar.fill.solid(); ar.fill.fore_color.rgb = LINE; ar.line.fill.background(); ar.shadow.inherit = False
    d.txt(s, 6.6, 6.02, 5.6, 0.35, "术前预判失败概率，比术中“再试一次”更重要。", size=9.5, color=CORAL, bold=True)
    d.footer(s, 20, "来源：[1] Chen 2026 Meta；[14] Chen 2024")

    # ============================================================ 21 techniques
    s = d.blank()
    d.header(s, "04 · 技术", "技术选择：顺行、逆行、分期")
    d.pic(s, "fig_technique.png", 0.55, 1.5, 9.55)
    d.card(s, 10.25, 1.5, 2.45, 3.7, fill=WHITE)
    d.txt(s, 10.42, 1.62, 2.1, 0.25, "器械要点", size=10.5, color=TEAL, bold=True)
    d.txt(s, 10.42, 1.98, 2.1, 3.0,
          "· 小球囊预扩\n· 自膨闭环支架\n· 长支架、少重叠\n· 避免过度后扩张\n· 远端保护：可选",
          size=8.8, color=INK, line=1.45)
    d.txt(s, 0.65, 5.38, 9.2, 0.3, "示意图：作者绘制，用于说明入路与器械策略，非患者影像。", size=7.8, color=MUTED)
    d.card(s, 0.65, 5.72, 9.45, 0.95, fill=TEAL_L, line=None)
    for i, (t, body) in enumerate([("顺行", "首选；多数病例"), ("逆行", "无残端/近端失败"), ("分期", "高血栓负荷/不稳定")]):
        d.txt(s, 0.9 + i * 3.1, 5.82, 2.85, 0.22, t, size=9.5, color=TEAL, bold=True)
        d.txt(s, 0.9 + i * 3.1, 6.08, 2.85, 0.35, body, size=8.2, color=INK)
    d.card(s, 10.25, 5.35, 2.45, 1.35, fill=TEAL_L, line=None)
    d.txt(s, 10.42, 5.48, 2.1, 1.1, "关键：\n先恢复灌注，\n再追求完美形态。", size=9.5, color=TEAL, bold=True, line=1.3)
    d.footer(s, 21, "来源：[10] REVANS；[24] Duan 2021；[19] Zhou 2023；[6] Li 2025")

    # ============================================================ 22 antithrombotic
    s = d.blank()
    d.header(s, "04 · 技术", "围术期管理：抗栓是“没有 RCT 的艺术”")
    steps = [
        ("术前", "3–5 d", "DAPT\n阿司匹林 + 氯吡格雷", TEAL),
        ("术中", "肝素化", "ACT 监测\n血栓/夹层预案", TEAL2),
        ("术后", "6 个月", "DAPT → 单抗\n血压 110–130 mmHg", GOLD),
        ("随访", "6–12 个月", "DSA/CTA\n神经功能 + mRS", CORAL),
    ]
    extras = ["负荷剂量 / 基因型？", "维持 ACT 250–300 s", "6 个月后转单抗", "再狭窄 → 个体化"]
    for i, (phase, time, body, col) in enumerate(steps):
        x = 0.65 + i * 3.1
        d.card(s, x, 1.6, 2.85, 2.55, fill=WHITE)
        d.rect(s, x, 1.6, 2.85, 0.1, fill=col)
        d.txt(s, x + 0.22, 1.82, 2.4, 0.25, phase, size=11, color=col, bold=True)
        d.txt(s, x + 0.22, 2.12, 2.4, 0.3, time, size=15, color=INK, bold=True)
        d.txt(s, x + 0.22, 2.62, 2.4, 1.1, body, size=8.8, color=MUTED, line=1.35)
        d.txt(s, x + 0.22, 3.55, 2.4, 0.45, extras[i], size=8, color=col, bold=True)
        if i < 3:
            ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.86), Inches(2.7), Inches(0.22), Inches(0.25))
            ar.fill.solid(); ar.fill.fore_color.rgb = LINE; ar.line.fill.background(); ar.shadow.inherit = False
    d.card(s, 0.65, 4.5, 5.95, 1.95, fill=WHITE)
    d.txt(s, 0.88, 4.65, 5.5, 0.25, "监测", size=10.5, color=TEAL, bold=True)
    d.txt(s, 0.88, 5.0, 5.5, 1.25, "· 术后 24 h CT 除外出血\n· 警惕高灌注：头痛、癫痫、意识变化\n· 穿支卒中：新发脑干症状", size=8.8, color=INK, line=1.4)
    d.card(s, 6.8, 4.5, 5.85, 1.95, fill=CORAL_L, line=None)
    d.txt(s, 7.03, 4.65, 5.4, 0.25, "证据缺口", size=10.5, color=CORAL, bold=True)
    d.txt(s, 7.03, 5.0, 5.4, 1.25, "最佳 DAPT 时程？替格瑞洛/西洛他唑？\n基因型指导？——均无 RCT。", size=9, color=INK, line=1.4)
    d.txt(s, 0.65, 6.62, 12.0, 0.3, "图中时程/ACT 为常见实践，非指南推荐；各中心方案不同。", size=7.8, color=MUTED)
    d.footer(s, 22, "来源：[19] Zhou 2023；[30] 中国专家共识 2020；方案异质，需个体化")

    # ============================================================ 23 case 1
    s = d.blank()
    d.header(s, "05 · 病例", "病例一：进行性后循环缺血的非急性 VBO")
    d.card(s, 0.55, 1.45, 5.55, 5.4, fill=WHITE)
    d.pic(s, "fig_case1.png", 0.7, 1.58, 5.2)
    d.txt(s, 0.75, 6.35, 5.2, 0.35, "示意图，非患者原始影像；病例来自 [3]", size=7.8, color=MUTED)
    d.card(s, 6.35, 1.45, 6.35, 5.4, fill=WHITE)
    d.txt(s, 6.6, 1.62, 5.85, 0.3, "62 岁女性：10 天进行性症状", size=13, color=TEAL, bold=True)
    d.txt(s, 6.6, 2.05, 5.85, 1.2,
          "眩晕、复视、构音障碍、步态共济失调；\nDAPT 下仍进展。MRI：左小脑急性/亚急性梗死；\nCTA：基底动脉无前向充盈、远端经侧支。",
          size=9.5, color=INK, line=1.35)
    d.txt(s, 6.6, 3.35, 5.85, 1.05,
          "DSA：左 V4 闭塞；经后交通动脉逆行充盈基底动脉；\n右椎动脉发育不良。",
          size=9.5, color=INK, line=1.35)
    d.txt(s, 6.6, 4.45, 5.85, 0.9,
          "处理：腔内穿越 → 逐步球囊扩张 → 支架重建。\n结局：NIHSS 5→2；30 d mRS 1。",
          size=9.5, color=INK, line=1.35)
    d.rect(s, 6.6, 5.0, 5.75, 0.02, fill=LINE)
    d.txt(s, 6.6, 5.1, 5.85, 0.55,
          "局限：单例；无随访血管影像；不能证明优于药物或因果。",
          size=8.5, color=CORAL, line=1.25)
    # mini timeline
    d.rect(s, 6.75, 6.05, 5.55, 0.03, fill=LINE)
    t1 = [("10 d 症状", CORAL), ("DSA 闭塞", CORAL), ("再通", TEAL), ("30 d mRS 1", TEAL)]
    for i, (lab, col) in enumerate(t1):
        x = 6.85 + i * 1.72
        d.circle(s, x, 5.99, 0.14, col, line=WHITE, lw=1.5)
        d.txt(s, x - 0.25, 6.22, 1.55, 0.25, lab, size=8.1, color=col, bold=True)
    d.footer(s, 23, "来源：[3] Soetanto 2026（Neurol Int）；示意图由作者绘制")

    # ============================================================ 24 case 2
    s = d.blank()
    d.header(s, "05 · 病例", "病例二：双侧椎动脉闭塞的慢性 CTO")
    d.card(s, 0.55, 1.45, 5.55, 5.4, fill=WHITE)
    d.pic(s, "fig_case2.png", 0.7, 1.58, 5.2)
    d.txt(s, 0.75, 6.35, 5.2, 0.35, "示意图，非患者原始影像；病例来自 [4]", size=7.8, color=MUTED)
    d.card(s, 6.35, 1.45, 6.35, 5.4, fill=WHITE)
    d.txt(s, 6.6, 1.62, 5.85, 0.3, "74 岁男性：40 天头晕、步态不稳", size=13, color=TEAL, bold=True)
    d.txt(s, 6.6, 2.05, 5.85, 1.0,
          "MRI：无新发急性梗死；MRA：双侧椎动脉闭塞。\nRAPID 灌注：大片低灌注区 → 症状性 ICVA CTO。",
          size=9.5, color=INK, line=1.35)
    d.txt(s, 6.6, 3.05, 5.85, 0.9,
          "处理：急诊血管内再通；\n术后小脑梗死，无新发神经功能缺损。",
          size=9.5, color=INK, line=1.35)
    d.txt(s, 6.6, 4.0, 5.85, 0.9,
          "结局：14 d 出院回家；2 个月无症状；\n灌注异常几乎消失。",
          size=9.5, color=INK, line=1.35)
    d.rect(s, 6.6, 4.98, 5.75, 0.02, fill=LINE)
    d.txt(s, 6.6, 5.06, 5.85, 0.5,
          "启示：自动灌注成像可辅助识别“低灌注型”慢性 CTO；单例证据。",
          size=8.5, color=TEAL, line=1.25)
    d.rect(s, 6.75, 6.05, 5.55, 0.03, fill=LINE)
    t2 = [("40 d 症状", CORAL), ("RAPID 低灌注", CORAL), ("再通", TEAL), ("2 mo 无症状", TEAL)]
    for i, (lab, col) in enumerate(t2):
        x = 6.85 + i * 1.72
        d.circle(s, x, 5.99, 0.14, col, line=WHITE, lw=1.5)
        d.txt(s, x - 0.3, 6.22, 1.6, 0.25, lab, size=8.1, color=col, bold=True)
    d.footer(s, 24, "来源：[4] Yamada 2026（J Neuroendovasc Ther）；示意图由作者绘制")

    # ============================================================ 25 quality
    s = d.blank()
    d.header(s, "06 · 讨论", "证据质量：我们知道的，和不知道的")
    domains = [
        ("设计", "单中心回顾性为主；无 RCT", "低", CORAL),
        ("样本", "多数 8–100 例；最大 VBA 队列 115 例", "低–中", GOLD),
        ("对照", "极少；Meta 中保守治疗仅 42 例", "极低", CORAL),
        ("定义", "非急性/慢性界值不一致", "低", CORAL),
        ("随访", "6 个月–2 年不等；再狭窄定义不一", "低", GOLD),
        ("外推", "中国中心为主；BA/长段病变量少", "低", CORAL),
    ]
    impacts = ["→ 只能提出假设", "→ 率值不稳定", "→ 无法估计绝对获益", "→ 不能直接合并", "→ 长期安全性未知", "→ 老年/BA 需谨慎"]
    for i, (t, body, rating, col) in enumerate(domains):
        x = 0.65 + (i % 2) * 6.1
        y = 1.55 + (i // 2) * 1.35
        d.card(s, x, y, 5.85, 1.15, fill=WHITE)
        d.txt(s, x + 0.22, y + 0.14, 1.2, 0.3, t, size=10.5, color=INK, bold=True)
        d.txt(s, x + 1.5, y + 0.16, 3.35, 0.7, body, size=8.8, color=MUTED, line=1.2)
        d.chip(s, x + 4.6, y + 0.42, 0.95, rating, fill=CORAL_L if "低" in rating else GOLD_L, color=col, size=8)
        d.txt(s, x + 1.5, y + 0.73, 3.1, 0.25, impacts[i], size=8.2, color=col, bold=True)
    d.card(s, 0.65, 5.7, 12.0, 0.85, fill=INK2, line=None)
    d.txt(s, 0.9, 5.83, 11.5, 0.55,
          "总体：技术成功“低–中”；并发症“低”；功能结局“低”；再通 vs 药物的获益“极低”。不能把单中心经验写成指南。",
          size=10.2, color=WHITE, bold=True, line=1.25)
    d.footer(s, 25, "本页为作者对纳入文献的方法学评价，非正式 GRADE 分级")

    # ============================================================ 26 controversies
    s = d.blank()
    d.header(s, "06 · 讨论", "四个争议，决定下一个研究")
    debates = [
        ("01", "定义", "24 h？1 个月？3 个月？", "统一影像+时间标准；否则无法比较", TEAL),
        ("02", "谁获益", "自然病史 vs 选择偏倚", "需要保守对照组与核心影像", GOLD),
        ("03", "技术", "支架类型、后扩张、远端保护", "器械选择缺少头对头证据", CORAL),
        ("04", "终点", "mRS 0–2 还是 0–3？再狭窄算失败吗？", "以患者为中心 + 统一影像终点", TEAL2),
    ]
    stances = ["→ 采用 >24 h / >1 个月，并标注原始界值", "→ 不把单中心当因果；强调选择", "→ 首选简单、可重复的方案", "→ mRS 0–2 为主；再狭窄单列"]
    for i, (num, t, now, need, col) in enumerate(debates):
        x = 0.65 + (i % 2) * 6.1
        y = 1.55 + (i // 2) * 2.45
        d.card(s, x, y, 5.85, 2.15, fill=WHITE)
        d.txt(s, x + 0.25, y + 0.2, 0.6, 0.3, num, size=10, color=col, bold=True)
        d.txt(s, x + 0.85, y + 0.18, 4.5, 0.3, t, size=14, color=INK, bold=True)
        d.txt(s, x + 0.85, y + 0.65, 4.6, 0.45, "现状：" + now, size=9.5, color=INK, line=1.2)
        d.txt(s, x + 0.85, y + 1.18, 4.6, 0.55, "需要：" + need, size=9.2, color=col, line=1.2)
        d.txt(s, x + 0.85, y + 1.68, 4.6, 0.3, stances[i], size=8.6, color=INK, bold=True)
    d.footer(s, 26, "争议综合自 [1][7][14][17][19][30]")

    # ============================================================ 27 future
    s = d.blank()
    d.header(s, "06 · 讨论", "下一步：从经验到证据")
    horizons = [
        ("0–2 年", "打地基", ["统一“非急性/慢性”定义", "多中心登记与核心影像", "标准化并发症/再狭窄定义"], TEAL),
        ("2–5 年", "做对照", ["EVT vs 强化药物 RCT", "影像分层的前瞻验证", "BA vs VA 的单独研究"], GOLD),
        ("5 年+", "个体化", ["预测模型 + AI", "药物涂层球囊/新支架", "患者报告结局与成本效果"], CORAL),
    ]
    milestones = ["里程碑：登记平台上线", "里程碑：首例 RCT 入组", "里程碑：模型外部验证"]
    for i, (t, sub, items, col) in enumerate(horizons):
        x = 0.65 + i * 3.25
        d.card(s, x, 1.55, 2.95, 4.1, fill=WHITE)
        d.rect(s, x, 1.55, 2.95, 0.1, fill=col)
        d.txt(s, x + 0.22, 1.78, 2.5, 0.3, t, size=15, color=col, bold=True)
        d.txt(s, x + 0.22, 2.15, 2.5, 0.25, sub, size=9, color=MUTED)
        for j, it in enumerate(items):
            d.txt(s, x + 0.22, 2.6 + j * 0.8, 2.55, 0.65, "· " + it, size=9.2, color=INK, line=1.25)
        d.txt(s, x + 0.22, 5.02, 2.55, 0.45, milestones[i], size=8.3, color=col, bold=True)
    d.card(s, 0.65, 5.9, 12.0, 0.75, fill=INK2, line=None)
    d.txt(s, 0.9, 6.03, 11.5, 0.5,
          "一个可执行的 RCT 构想：药物失败 + 低灌注 + 可再通解剖；EVT+BMT vs BMT；主要终点 90 d mRS 0–2 / 1 年卒中或死亡。",
          size=9.8, color=WHITE, bold=True, line=1.2)
    d.footer(s, 27, "研究空白综合自 [1][7][14][19][30]")

    # ============================================================ 28 algorithm
    s = d.blank()
    d.header(s, "06 · 讨论", "单中心实践路径：六步决策")
    steps = [
        ("1", "确认闭塞", "CTA/DSA：症状性非急性 VBAO", TEAL),
        ("2", "药物试验", "最佳药物下复发/进展？", TEAL),
        ("3", "影像评估", "梗死负担 + 低灌注 + HR-MRI", TEAL2),
        ("4", "解剖分层", "残端/长度/钙化/远端代偿", GOLD),
        ("5", "MDT 决策", "EVT vs 药物；高危不强行", CORAL),
        ("6", "围术期 + 随访", "抗栓、血压、6–12 个月影像", TEAL),
    ]
    details2 = ["DSA 确认闭塞段与远端重建", "复发频率、NIHSS、mRS", "梗死核心/低灌注/侧支", "低/中/高危 + 失败概率", "患者意愿 + 获益/风险", "DAPT、血压、影像复查"]
    for i, (num, t, body, col) in enumerate(steps):
        x = 0.65 + (i % 3) * 4.1
        y = 1.55 + (i // 3) * 2.15
        d.card(s, x, y, 3.8, 1.75, fill=WHITE)
        d.circle(s, x + 0.2, y + 0.22, 0.42, col)
        d.txt(s, x + 0.2, y + 0.31, 0.42, 0.2, num, size=10, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
        d.txt(s, x + 0.78, y + 0.18, 2.9, 0.3, t, size=12.5, color=INK, bold=True)
        d.txt(s, x + 0.78, y + 0.55, 2.85, 0.45, body, size=8.6, color=MUTED, line=1.2)
        d.txt(s, x + 0.78, y + 1.05, 2.85, 0.45, details2[i], size=8.1, color=col, line=1.2)
    # arrows row1 and row2
    for x in (4.45, 8.55):
        ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(2.3), Inches(0.22), Inches(0.25))
        ar.fill.solid(); ar.fill.fore_color.rgb = LINE; ar.line.fill.background(); ar.shadow.inherit = False
    ar = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(2.45), Inches(3.32), Inches(0.25), Inches(0.3))
    ar.fill.solid(); ar.fill.fore_color.rgb = LINE; ar.line.fill.background(); ar.shadow.inherit = False
    d.card(s, 0.65, 5.85, 12.0, 0.8, fill=TEAL_L, line=None)
    d.txt(s, 0.9, 5.98, 11.5, 0.5,
          "红线：大面积脑干梗死/昏迷、长段钙化无流出道、无残端且无法逆行、无法抗栓——不强行再通。",
          size=9.8, color=CORAL, bold=True)
    d.footer(s, 28, "基于 [7][14][19][21][30] 的综合路径，供单中心讨论；非指南")

    # ============================================================ 29 take-home
    s = d.blank(bg=INK)
    d.txt(s, 0.65, 0.55, 2.0, 0.3, "TAKE-HOME", size=10, color=TEAL2, bold=True)
    d.txt(s, 0.65, 0.95, 11.5, 0.7, "四句话带走", size=32, color=WHITE, bold=True)
    msgs = [
        ("87%", "技术成功", "但只在“选对的人”里；失败集中在钝头/长段/钙化/远端代偿差。"),
        ("13%", "围手术期并发症", "BA 风险高于 VA；夹层、栓塞、出血、支架内血栓是主要类型。"),
        ("15%", "再狭窄/再闭塞", "成功后仍需 6–12 个月影像随访；高危解剖可高达 80%。"),
        ("0 项", "RCT（本组文献）", "证据强度低；决策靠共同决策，而不是“别人能做”。"),
    ]
    for i, (num, label, body) in enumerate(msgs):
        x = 0.65 + (i % 2) * 6.15
        y = 1.85 + (i // 2) * 2.35
        d.txt(s, x, y, 1.6, 0.65, num, size=36, color=TEAL2 if i < 3 else CORAL, bold=True)
        d.txt(s, x + 1.75, y + 0.05, 4.2, 0.3, label, size=11, color=WHITE, bold=True)
        d.txt(s, x + 1.7, y + 0.42, 3.95, 0.95, body, size=9.0, color=RGBColor(0xC9, 0xDA, 0xDE), line=1.3)
    d.txt(s, 0.65, 6.65, 11.8, 0.3, "谢谢  ·  讨论", size=12, color=RGBColor(0x9F, 0xB8, 0xBF), bold=True)
    d.notes(s, "收尾：三个数字——87% 技术成功、13% 并发症、15% 再狭窄；一个前提——选对人。最后落到“没有 RCT”这个证据缺口上，引出讨论。")

    # ============================================================ 30 references
    s = d.blank()
    d.header(s, "06 · 讨论", "参考文献（节选 24 篇，完整 40 篇见 literature/）")
    refs = [
        ("R01", "Chen X, et al. World Neurosurg 2026. doi:10.1016/j.wneu.2025.124770"),
        ("R02", "Li W, et al. Atherosclerosis 2026. doi:10.1016/j.atherosclerosis.2026.120678"),
        ("R03", "Soetanto GW, et al. Neurol Int 2026. doi:10.3390/neurolint18100183"),
        ("R04", "Yamada D, et al. J Neuroendovasc Ther 2026. doi:10.5797/jnet.cr.2026-0098"),
        ("R06", "Li Q, et al. Acta Neurochir (Wien) 2025. doi:10.1007/s00701-025-06525-4"),
        ("R07", "Liu Y, et al. Front Neurol 2025. doi:10.3389/fneur.2025.1496852"),
        ("R10", "Wang J, et al. Neuroradiology 2025. doi:10.1007/s00234-025-03602-4"),
        ("R11", "Zhang X, et al. Front Neurol 2025. doi:10.3389/fneur.2025.1453841"),
        ("R12", "Zhou C, et al. Acad Radiol 2025. doi:10.1016/j.acra.2024.10.020"),
        ("R14", "Chen S, et al. Medicine 2024. doi:10.1097/MD.0000000000036813"),
        ("R15", "Liu L, et al. J Clin Neurosci 2024. doi:10.1016/j.jocn.2023.12.013"),
        ("R17", "Roth C, et al. J Neurol 2024. doi:10.1007/s00415-024-12375-4"),
        ("R18", "Xia J, et al. Sci Rep 2023. doi:10.1038/s41598-023-31313-4"),
        ("R19", "Zhou ZL, et al. Front Neurol 2023. doi:10.3389/fneur.2023.1125244"),
        ("R20", "Gao F, et al. J Neurointerv Surg 2022. doi:10.1136/neurintsurg-2021-017283"),
        ("R21", "Gao F, et al. J Neurointerv Surg 2022. doi:10.1136/neurintsurg-2020-017213"),
        ("R22", "Ng AC, et al. Am J Med Sci 2022. doi:10.1016/j.amjms.2021.10.027"),
        ("R24", "Duan H, et al. Front Neurol 2021. doi:10.3389/fneur.2021.673367"),
        ("R26", "Gao F, et al. Stroke 2020. doi:10.1161/STROKEAHA.120.030440"),
        ("R28", "Zhao W, et al. Front Neurol 2020. doi:10.3389/fneur.2020.598795"),
        ("R30", "中国非急性颅内/外大血管闭塞血管内治疗专家共识. 中华内科杂志 2020. doi:10.3760/cma.j.cn112138-20200413-00366"),
        ("R31", "Zhao W, et al. Front Neurol 2019. doi:10.3389/fneur.2019.01290"),
        ("R36", "Markus HS, et al. Lancet Neurol 2013. doi:10.1016/S1474-4422(13)70211-4"),
        ("R38", "Dashti SR, et al. Neurosurgery 2010. doi:10.1227/01.NEU.0000367611.78898.A3"),
    ]
    for i, (ref, text) in enumerate(refs):
        col = i // 12
        row = i % 12
        x = 0.55 + col * 6.25
        y = 1.45 + row * 0.44
        d.txt(s, x, y, 0.5, 0.22, ref.replace("R", ""), size=7.5, color=TEAL, bold=True)
        d.txt(s, x + 0.42, y, 5.75, 0.4, text, size=7.4, color=INK, line=1.1)
    d.txt(s, 0.55, 6.85, 12.0, 0.3, "完整 40 篇题录、DOI、PMID、核心结论见 literature/02_literature_table.md；BibTeX 见 literature/references.bib。", size=7.5, color=MUTED)
    d.footer(s, 30, "所有文献均回溯 PubMed/Europe PMC 原始记录核对")


    NOTES = [
        "开场：今天汇报后循环慢性/非急性闭塞的血管内再通。主线是三个问题：谁适合开、开得通吗、开完以后怎么样。最后给出一个可落地的单中心决策路径。",
        "先交代结构：背景与解剖、证据与选择、结果、技术、病例、讨论。全程 30 页，建议 35–40 分钟，重点放在第 15–20 页的结果和第 28 页的路径。",
        "后循环卒中占缺血性卒中的 20%–25%，约 1/5 的卒中/TIA 位于后循环。症状性椎基底动脉闭塞在药物下仍有复发风险；老年队列中保守治疗 1 年卒中/死亡 30%，EVT 组 10%，但这是单中心非随机比较。",
        "文献对‘慢性/非急性’没有统一界值：24 小时、2 周、3 周、1 个月、3 个月都有人用。本汇报采用工作定义：非急性 >24 小时，慢性 >1 个月；引用研究时保留原始界值，避免把不同定义的结果直接合并。",
        "解剖是风险的底层逻辑：V4 和基底动脉穿支供应脑干，损伤后果重；PICA/AICA/SCA 决定小脑与脑干缺血范围；后交通、前脊髓动脉和软脑膜侧支是缓冲垫。基底动脉再通风险高于颅内椎动脉。",
        "四条机制：动脉粥样硬化斑块、低灌注、栓塞、侧支失代偿。临床上常见的是混合机制；共同终点是脑干/小脑缺血，表现为复发 TIA、进展性卒中、残疾或死亡。",
        "慢性闭塞不等于良性。自然病程队列 15 例慢性 BAO 中 5 例偶然发现、4 例仅轻症，说明侧支代偿好的人可以稳定；但未再通的急性大动脉闭塞存活者年复发卒中约 6%–14%。再通队列是‘高危 + 可开通’的选择人群。",
        "影像分三层：血管解剖看‘开不开得通’，管壁/斑块看‘为什么闭塞’，脑组织看‘值不值得开’。决策四问：是否真闭塞、能否开通、值不值得开、风险多大。",
        "形态学比长度更重要。锥形残端再通率 90.9%，非锥形只有 40%；钝头残端失败率 27.3%，占全部失败的 85.7%；长度 >30 mm 和远端代偿差的 OR 分别约 0.14 和 0.25；钙化/成角也是独立负向因素。",
        "高级影像把‘可能获益’变成可测量：HR-MRI 的残留管腔、斑块强化、短闭塞长度可预测再通；CTP/ASL 识别低灌注；DSA 侧支分型（Gao I–III、EVAO A–D）指导选择。没有单一指标能独立决策。",
        "患者选择可以压缩成‘4+4’：四条建议是药物失败、低灌注/栓塞证据、可再通解剖、梗死负担可控；四条排除是大面积脑干梗死/昏迷、长段钙化无流出道、无残端且无法逆行、严重合并症/无法抗栓。高危解剖不强行再通。",
        "检索流程：PubMed 181 条、Europe PMC 289 条、补充 137 条，去重后 331 条，40 篇进入详细提取，13 篇拿到开放全文（7 PDF + 6 篇 XML-only）。这是叙述性筛选，不是严格 PRISMA；单检索人，未用 Embase/CNKI。",
        "证据地图：20 多项再通队列，样本量 7–177，最大单中心 177 例（VBA 58），最大非急性 BAO 队列 115 例；没有 RCT。近五年研究明显增多，说明这个题目正在升温，但证据等级仍低。",
        "这张表是核心研究的快速对照：BAO 再通率普遍低于 ICVA/EVAO，并发症率差异大（5.2%–19.3%）。注意 NR 和不同定义，不能直接用单个率值排名。",
        "技术成功总体约 87%，单中心范围 66.7%–96%。但这是‘选择性结果’：失败集中在钝头、长段、钙化、远端代偿差。技术成功也不等于功能获益，还要看并发症和选择。",
        "四个可术前识别的失败因素：闭塞 >3 个月、钝头残端、长度 >30 mm、远端代偿不足，OR 都在 0.14–0.25。Zhou 2023 强调形态比长度更重要；这些评分都还没有外部验证。",
        "并发症是 10%–20% 的现实：本组范围 5.2%–25%，Meta 汇总 13%。四类是夹层/穿孔、血栓/远端栓塞、出血、支架内血栓/再闭塞。基底动脉风险高于椎动脉，远端保护只有小样本证据。",
        "成功再通者 mRS 0–2 约 74%–79%，mRS 0–3 约 85%–94%；1 年卒中 11.4%，30 天后卒中/死亡 17.4%，Meta 长期复发/死亡 7%。这些是严格选择的队列，不能外推到所有慢性闭塞。",
        "再狭窄是长期账单：Meta 15%，单中心 10%–27%，高危解剖组可达 80%。后扩张与再狭窄相关（OR 4.55）。建议 6–12 个月影像随访；再狭窄的处理路径仍不明确。",
        "再通失败不只是‘没开通’：Chen 2024 的 15 例失败中，4 例缺血性卒中、2 例颅内出血，30 天后卒中/死亡 17.4%。Meta 的成功 vs 失败 OR 0.15 不是因果比较，但提醒我们术前要预判失败概率，避免强行再通。",
        "技术选择：顺行是首选；无残端或近端无法进入时，可经对侧椎/颈侧支逆行（REVANS）；高血栓负荷或不稳定时可分期，先球囊恢复灌注，再支架。器械上偏好小球囊、自膨闭环支架、长支架少重叠，避免过度后扩张。",
        "围术期抗栓没有 RCT：多数中心术前 DAPT 3–5 天，术中肝素化，术后 DAPT 6 个月后单抗；血压控制在 110–130 mmHg，24 小时 CT 除外出血，警惕高灌注和穿支卒中。最佳时程、替格瑞洛/西洛他唑、基因检测都还没有答案。",
        "病例一来自 Soetanto 2026：62 岁女性，10 天进行性眩晕、复视、构音障碍、共济失调；DAPT 下仍进展；DSA 左 V4 闭塞，经后交通逆行充盈基底动脉；再通后 NIHSS 5→2，30 天 mRS 1。单例，无随访影像。",
        "病例二来自 Yamada 2026：74 岁男性，40 天头晕、步态不稳；MRI 无新发梗死，MRA 双侧 VA 闭塞，RAPID 示大片低灌注；再通后术后小脑梗死但无新发缺损，14 天出院，2 个月无症状。提示灌注成像可辅助筛选，但仍是单例。",
        "证据质量总体低：单中心回顾性为主、样本小、对照少、定义异质、随访短且不一致、外推以中国中心为主。技术成功‘低–中’，并发症‘低’，功能结局‘低’，再通 vs 药物的获益‘极低’。不能把单中心经验写成指南。",
        "四个争议：定义（24 小时/1 个月/3 个月）、谁获益（自然病史 vs 选择偏倚）、技术（支架/后扩张/远端保护）、终点（mRS 0–2 还是 0–3，再狭窄算不算失败）。每个争议都对应一个可做的研究。",
        "下一步分三个阶段：0–2 年打地基（统一登记、核心影像、标准定义）；2–5 年做对照（EVT vs 强化药物 RCT、影像分层前瞻验证）；5 年以上个体化（预测模型、药物涂层球囊、患者报告结局）。RCT 构想：药物失败 + 低灌注 + 可再通解剖。",
        "单中心路径六步：确认闭塞、药物试验、影像评估、解剖分层、MDT 决策、围术期与随访。红线是大面积脑干梗死/昏迷、长段钙化无流出道、无残端且无法逆行、无法抗栓——不强行再通。",
        "四句话带走：87% 技术成功，但只在选对的人；13% 围手术期并发症，BA 高于 VA；15% 再狭窄，成功后仍要随访；本组文献 0 项 RCT，证据强度低，决策靠共同决策。谢谢，讨论。",
        "完整 40 篇文献的题录、DOI、PMID、核心结论在 literature/02_literature_table.md；BibTeX 在 references.bib。这里只列本汇报直接引用的 24 篇，便于现场核对。",
    ]
    for sl, note in zip(d.slides, NOTES):
        d.notes(sl, note)

    # save
    d.prs.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    build()

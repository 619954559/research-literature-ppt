"""Generate all figures for the posterior circulation occlusion deck."""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Wedge
from matplotlib.path import Path as MPath
from matplotlib.patches import PathPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "slides" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

INK = "#0E2233"
TEAL = "#0B6E69"
TEAL2 = "#2A9D8F"
LIGHT = "#DCEFEC"
CORAL = "#D9552F"
GOLD = "#D9A441"
MUTED = "#6C7F8B"
GRID = "#D8E2E4"
PAPER = "#F7F9F9"

plt.rcParams.update({
    "font.family": "Microsoft YaHei",
    "axes.unicode_minus": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, dpi=260, transparent=False):
    fig.savefig(ASSETS / name, dpi=dpi, bbox_inches="tight", pad_inches=0.05, transparent=transparent)
    plt.close(fig)
    print("saved", name)


def clean(ax):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", color=GRID, lw=0.6, alpha=0.8)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- hero
def hero():
    fig, ax = plt.subplots(figsize=(13.333, 7.5))
    fig.patch.set_facecolor(INK)
    ax.set_facecolor(INK)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 56)
    ax.axis("off")

    # faint concentric circles (lumen motif)
    for r, a in [(21, 0.06), (17, 0.08), (13, 0.1)]:
        ax.add_patch(Circle((77, 30), r, fill=False, ec=TEAL2, lw=0.8, alpha=a))

    # stylized vertebrobasilar tree on the right
    rng = np.random.default_rng(7)
    # vertebral arteries ascending
    for dx in (-7, 7):
        x = 77 + dx
        ys = np.linspace(4, 27, 100)
        xs = x + 1.2 * np.sin(ys / 3.0) * (1 if dx < 0 else -1)
        ax.plot(xs, ys, color=TEAL2, lw=3.2, alpha=0.85, solid_capstyle="round")
        # small branches
        for yy in np.linspace(7, 25, 9):
            side = 1 if (yy * 10) % 2 < 1 else -1
            ax.plot([x + side * 0.2, x + side * (3 + rng.random() * 3)],
                    [yy, yy + rng.uniform(-2.5, 2.5)], color=TEAL2, lw=0.8, alpha=0.35)

    # basilar trunk
    ys = np.linspace(27, 47, 60)
    xs = 77 + 1.6 * np.sin(ys / 3.4)
    ax.plot(xs, ys, color=TEAL2, lw=4.0, alpha=0.9, solid_capstyle="round")

    # basilar branches
    for yy, ln, ang in [(31, 8, 32), (34, 9, 28), (37, 8, 22), (40, 9, 18), (43, 8, 12)]:
        for s in (-1, 1):
            ax.plot([77, 77 + s * ln * math.cos(math.radians(ang))],
                    [yy, yy + ln * math.sin(math.radians(ang))],
                    color=TEAL2, lw=1.5, alpha=0.55, solid_capstyle="round")
            # terminal tuft
            ax.add_patch(Circle((77 + s * ln * math.cos(math.radians(ang)),
                                 yy + ln * math.sin(math.radians(ang))), 0.55, color=TEAL2, alpha=0.5))

    # PCA terminals
    for s in (-1, 1):
        ax.plot([77, 77 + s * 12], [47, 50], color=TEAL2, lw=2.2, alpha=0.7)
        ax.plot([77 + s * 12, 77 + s * 20], [50, 49], color=TEAL2, lw=1.4, alpha=0.45)

    # dark gradient overlay left
    ax.add_patch(Rectangle((0, 0), 100, 56, color=INK, alpha=0.0))
    fig.savefig(ASSETS / "fig_hero.png", dpi=220, facecolor=INK)
    plt.close(fig)
    print("saved fig_hero.png")


# ---------------------------------------------------------------- anatomy
def anatomy():
    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 64)
    ax.axis("off")
    ax.set_aspect("equal")

    # aortic arch (bottom, bowed upward)
    arch_x = np.linspace(26, 74, 100)
    arch_y = 5.5 + 6.0 * np.sin((arch_x - 26) / 48 * np.pi)
    ax.plot(arch_x, arch_y, color=TEAL, lw=9, solid_capstyle="round", zorder=3)

    # left subclavian -> left vertebral
    ax.plot([38, 34, 30, 32], [11.0, 13.0, 16.0, 22.0], color=TEAL, lw=5.5, solid_capstyle="round", zorder=4)
    ax.plot([32, 32, 33], [22.0, 34.0, 40.0], color=TEAL, lw=5.0, solid_capstyle="round", zorder=4)
    # right subclavian -> right vertebral
    ax.plot([64, 68, 71, 70], [11.0, 13.0, 16.0, 22.0], color=TEAL, lw=5.5, solid_capstyle="round", zorder=4)
    ax.plot([70, 70, 68], [22.0, 34.0, 40.0], color=TEAL, lw=5.0, solid_capstyle="round", zorder=4)

    # V4 convergence and basilar
    ax.plot([33, 40, 48], [40, 45, 48.5], color=TEAL, lw=5.0, solid_capstyle="round", zorder=4)
    ax.plot([68, 60, 52], [40, 45, 48.5], color=TEAL, lw=5.0, solid_capstyle="round", zorder=4)
    ax.plot([48, 50, 50], [48.5, 52, 59], color=TEAL, lw=6.0, solid_capstyle="round", zorder=4)

    # PICA
    for s in (-1, 1):
        base = 40 if s < 0 else 40
        ax.plot([33 if s < 0 else 68, 31 if s < 0 else 70, 28 if s < 0 else 73],
                [39, 35, 33], color=TEAL, lw=1.8, solid_capstyle="round", zorder=4)
    # AICA / SCA
    for yy in (50.5, 54.0):
        for s in (-1, 1):
            ax.plot([50, 50 + s * 6, 50 + s * 9], [yy, yy + 1.8, yy + 2.6],
                    color=TEAL, lw=1.6, solid_capstyle="round", zorder=4)
    # PCA
    for s in (-1, 1):
        ax.plot([50, 50 + s * 8], [59, 60.5], color=TEAL, lw=3.2, solid_capstyle="round", zorder=4)
        ax.plot([50 + s * 8, 50 + s * 16], [60.5, 59.5], color=TEAL, lw=1.8, solid_capstyle="round", zorder=4)

    # brainstem and cerebellum
    ax.add_patch(FancyBboxPatch((45, 34), 10, 20, boxstyle="round,pad=0.2,rounding_size=3.0",
                                fc="#F4DDCE", ec="#D9A441", lw=1.1, alpha=0.85, zorder=1))
    ax.text(50, 44, "脑干", ha="center", va="center", fontsize=8.5, color="#8A5A1F", zorder=6)
    ax.add_patch(Ellipse((34, 45), 18, 11, fc="#E8EEF1", ec="#B9C9CF", lw=0.9, alpha=0.95, zorder=1))
    ax.add_patch(Ellipse((66, 45), 18, 11, fc="#E8EEF1", ec="#B9C9CF", lw=0.9, alpha=0.95, zorder=1))
    ax.text(34, 45, "小脑", ha="center", va="center", fontsize=8.5, color=MUTED, zorder=6)
    ax.text(66, 45, "小脑", ha="center", va="center", fontsize=8.5, color=MUTED, zorder=6)

    def lab(x, y, t, tx, ty, color=INK, fs=8.5, ha="left"):
        ax.annotate(t, xy=(x, y), xytext=(tx, ty), fontsize=fs, color=color, ha=ha, va="center",
                    zorder=10, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8, shrinkA=0, shrinkB=2))

    lab(32, 23, "V1–V2\n椎动脉颅外段", 12, 24)
    lab(69, 36, "V3–V4\n椎动脉颅内段", 80, 36)
    lab(50, 57.5, "基底动脉", 61, 57.0)
    lab(31, 36, "PICA", 20, 34, ha="right")
    lab(55, 51.5, "AICA / SCA", 66, 52.5)
    lab(57, 60.3, "大脑后动脉", 65, 62.5)
    lab(34, 9, "锁骨下动脉", 18, 8)
    ax.text(5, 2.0, "红圈：常见闭塞部位（V4 段 / 基底动脉中段）", fontsize=8, color=CORAL)

    # occlusion marker
    ax.plot([50], [51.5], marker="o", ms=11, mfc="white", mec=CORAL, mew=2.4, zorder=12)

    save(fig, "fig_anatomy.png")


# ---------------------------------------------------------------- morphology
def morphology():
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 3.4))
    titles = ["锥形残端", "钝头残端", "长段闭塞", "远端代偿差"]
    notes = ["导丝易通过", "失败率最高", "血栓负荷大", "再通后低灌注"]
    for ax, title, note in zip(axes, titles, notes):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")
        ax.set_title(title, fontsize=11.5, color=INK, pad=4, fontweight="bold")
        ax.text(5, 0.65, note, ha="center", fontsize=8.2, color=MUTED)
        # vessel lumen
        ax.add_patch(Rectangle((0.7, 4.1), 8.6, 1.8, fc=LIGHT, ec="none", zorder=1))
        ax.plot([0.7, 9.3], [5.9, 5.9], color=TEAL, lw=2.0, solid_capstyle="round", zorder=3)
        ax.plot([0.7, 9.3], [4.1, 4.1], color=TEAL, lw=2.0, solid_capstyle="round", zorder=3)
        # distal flow arrows
        for xx in (7.6, 8.3):
            ax.annotate("", xy=(xx + 0.35, 5.0), xytext=(xx, 5.0),
                        arrowprops=dict(arrowstyle="-|>", color=TEAL2, lw=1.1, mutation_scale=9), zorder=4)
        # occlusion block
        ax.add_patch(Rectangle((4.0, 4.1), 1.0, 1.8, fc="#F3C8B9", ec="none", alpha=0.95, zorder=2))

    # tapered cap and guidewire
    ax = axes[0]
    ax.add_patch(Polygon([[4.0, 5.9], [5.0, 5.0], [4.0, 4.1]], closed=True, fc=CORAL, ec="none", zorder=5))
    ax.annotate("", xy=(5.6, 5.0), xytext=(1.2, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2, mutation_scale=12), zorder=6)
    ax.text(1.3, 5.45, "导丝", fontsize=7.5, color=INK, zorder=7)
    ax.text(4.35, 3.55, "锥形", fontsize=7.2, color=CORAL, ha="center")

    # blunt cap
    ax = axes[1]
    ax.add_patch(Rectangle((4.0, 4.1), 0.45, 1.8, fc=CORAL, ec="none", zorder=5))
    ax.text(4.2, 3.55, "平头", fontsize=7.2, color=CORAL, ha="center")

    # long segment
    ax = axes[2]
    ax.add_patch(Rectangle((3.2, 4.1), 3.2, 1.8, fc="#F3C8B9", ec="none", alpha=0.95, zorder=2))
    ax.add_patch(Rectangle((6.1, 4.1), 0.35, 1.8, fc=CORAL, ec="none", zorder=5))
    ax.annotate("", xy=(6.5, 7.0), xytext=(3.2, 7.0),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.0, mutation_scale=9), zorder=6)
    ax.text(4.85, 7.25, "长段", fontsize=7.2, color=MUTED, ha="center")

    # poor distal collateral
    ax = axes[3]
    ax.add_patch(Polygon([[4.0, 5.9], [5.0, 5.0], [4.0, 4.1]], closed=True, fc=CORAL, ec="none", zorder=5))
    ax.plot([5.0, 9.3], [5.9, 5.9], color=TEAL, lw=2.0, ls=(0, (3, 2)), alpha=0.5, zorder=3)
    ax.plot([5.0, 9.3], [4.1, 4.1], color=TEAL, lw=2.0, ls=(0, (3, 2)), alpha=0.5, zorder=3)
    ax.plot([6.4, 7.2], [5.9, 7.2], color=TEAL2, lw=1.0, ls=(0, (2, 2)), alpha=0.7, zorder=4)
    ax.text(6.0, 7.35, "侧支?", fontsize=7.2, color=TEAL2)

    save(fig, "fig_morphology.png")


# ---------------------------------------------------------------- evidence map
def evidence_map():
    data = [
        ("Zhou 2023", 2023, 88, "混合VBA", 19),
        ("Xia 2023", 2023, 58, "混合VBA", 18),
        ("Chen 2024", 2024, 92, "ICVA", 14),
        ("Gao 2020", 2020, 50, "ICVA", 26),
        ("Zhao 2020", 2020, 31, "ICVA", 28),
        ("Cai 2021", 2021, 22, "ICVA", 23),
        ("Xu 2014", 2014, 8, "ICVA", 34),
        ("Liu 2025", 2025, 115, "BA", 7),
        ("Gao 2022", 2022, 42, "BA", 21),
        ("Zhao 2019", 2019, 21, "BA", 31),
        ("Dashti 2010", 2010, 9, "BA", 38),
        ("Gao 2022b", 2022, 50, "EVAO", 20),
        ("Chen 2020", 2020, 23, "EVAO", 25),
        ("Liu 2024", 2024, 21, "EVAO", 15),
        ("Zheng 2020", 2020, 7, "EVAO", 29),
        ("Zhang 2025", 2025, 103, "混合", 11),
        ("He 2014", 2014, 27, "混合", 33),
        ("Li 2025", 2025, 8, "混合", 6),
    ]
    cmap = {"ICVA": TEAL, "BA": CORAL, "EVAO": GOLD, "混合VBA": "#5B7FA6", "混合": MUTED}
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    for name, yr, n, grp, ref in data:
        ax.scatter(yr, n, s=28 + n * 1.8, color=cmap[grp], alpha=0.82, edgecolor="white", linewidth=1.2, zorder=4)
    offsets = {
        "Liu 2025": (4, 10), "Zhang 2025": (-46, 12), "Zhou 2023": (-24, 12),
        "Chen 2024": (6, -16), "Xia 2023": (6, -14), "Gao 2022b": (-46, -14),
        "Gao 2020": (-38, 10),
    }
    for name, yr, n, grp, ref in data:
        if n >= 50:
            ax.annotate(name, (yr, n), xytext=offsets.get(name, (4, 5)), textcoords="offset points", fontsize=7.5, color=INK)
    ax.set_yscale("log")
    ax.set_yticks([8, 12, 20, 30, 50, 80, 120])
    ax.set_yticklabels(["8", "12", "20", "30", "50", "80", "120"])
    ax.set_xlim(2008, 2027)
    ax.set_xticks([2010, 2014, 2018, 2022, 2026])
    ax.set_xlabel("发表年份", fontsize=9, color=MUTED)
    ax.set_ylabel("样本量（对数）", fontsize=9, color=MUTED)
    clean(ax)
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=8, label=k) for k, c in cmap.items()]
    ax.legend(handles=handles, loc="upper left", fontsize=8, frameon=False, ncol=3)
    save(fig, "fig_evidence_map.png")


# ---------------------------------------------------------------- forest
def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0, centre - half), min(1, centre + half)


def forest():
    data = [
        ("He 2014", 26, 27),
        ("Zhou 2023", 81, 88),
        ("Zhao 2020", 27, 31),
        ("Cai 2021", 19, 22),
        ("Chen 2024", 77, 92),
        ("Gao 2020", 38, 50),
        ("Gao 2022 EVAO", 43, 50),
        ("Zhao 2019", 17, 21),
        ("Gao 2022 BAO", 32, 42),
        ("Xia 2023 VBA", 48, 58),
        ("Liu 2024 VOO", 14, 21),
        ("Zhang 2025", 71, 103),
        ("Liu 2025 BAO", 94, 115),
    ]
    fig, ax = plt.subplots(figsize=(7.6, 5.3))
    ys = np.arange(len(data))[::-1]
    for y, (name, k, n) in zip(ys, data):
        p = k / n * 100
        lo, hi = wilson(k, n)
        lo, hi = lo * 100, hi * 100
        ax.plot([lo, hi], [y, y], color="#B9CDD2", lw=3, solid_capstyle="round", zorder=2)
        ax.scatter(p, y, s=42, color=TEAL, zorder=3, edgecolor="white", linewidth=0.8)
        ax.text(104, y, f"{k}/{n}", va="center", ha="left", fontsize=8, color=MUTED)
    ax.axvline(87, color=CORAL, lw=1.4, ls=(0, (4, 3)), zorder=1)
    ax.text(87.6, len(data) - 0.35, "Meta 87%", color=CORAL, fontsize=8, va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels([d[0] for d in data], fontsize=8.5, color=INK)
    ax.set_xlim(40, 108)
    ax.set_xlabel("技术成功率（%，Wilson 95% CI）", fontsize=9, color=MUTED)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    save(fig, "fig_success_forest.png")


# ---------------------------------------------------------------- predictors
def predictors():
    labels = ["闭塞 >3 个月", "钝头残端", "闭塞长度 >30 mm", "远端代偿不足"]
    ors = [0.187, 0.236, 0.144, 0.25]
    lo = [0.051, 0.072, 0.031, 0.075]
    hi = [0.688, 0.777, 0.669, 0.835]
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    y = np.arange(len(labels))[::-1]
    for yy, o, l, h in zip(y, ors, lo, hi):
        ax.plot([l, h], [yy, yy], color="#B9CDD2", lw=4, solid_capstyle="round", zorder=2)
        ax.scatter(o, yy, s=70, color=CORAL, zorder=3, edgecolor="white", linewidth=1)
        ax.text(h * 1.08, yy, f"OR {o:.2f} ({l:.2f}–{h:.2f})", va="center", fontsize=8, color=INK)
    ax.axvline(1, color=MUTED, lw=1, ls=":")
    ax.set_xscale("log")
    ax.set_xlim(0.02, 3.2)
    ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1.0])
    ax.set_xticklabels(["0.05", "0.1", "0.25", "0.5", "1.0"])
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9, color=INK)
    ax.set_xlabel("再通成功的 OR（对数坐标，<1 表示失败风险升高）", fontsize=8.5, color=MUTED)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    save(fig, "fig_predictors.png")


# ---------------------------------------------------------------- complications
def complications():
    data = [
        ("Li 2025", 25.0),
        ("Zhao 2020", 19.4),
        ("Zhou 2023", 19.3),
        ("He 2014", 19.0),
        ("Gao 2022 BAO", 14.3),
        ("Liu 2024", 14.3),
        ("Gao 2022 EVAO", 12.0),
        ("Chen 2024", 10.9),
        ("Zhang 2025", 10.7),
        ("Zhao 2019", 9.5),
        ("Xia 2023 VBA", 5.2),
    ]
    data = data[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    y = np.arange(len(data))
    colors = [CORAL if v >= 18 else TEAL for _, v in data]
    ax.barh(y, [v for _, v in data], color=colors, alpha=0.9, height=0.58, zorder=3)
    for yy, (_, v) in zip(y, data):
        ax.text(v + 0.5, yy, f"{v:.1f}%", va="center", fontsize=8, color=INK)
    ax.axvline(13, color=GOLD, lw=1.4, ls=(0, (4, 3)))
    ax.text(13.5, len(data) - 0.5, "Meta 13%", color="#9A6B12", fontsize=8, va="bottom")
    ax.set_yticks(y)
    ax.set_yticklabels([d[0] for d in data], fontsize=8.5, color=INK)
    ax.set_xlim(0, 29)
    ax.set_xlabel("围手术期并发症（%）", fontsize=9, color=MUTED)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    save(fig, "fig_complications.png")


# ---------------------------------------------------------------- outcomes
def outcomes():
    labels = ["Zhao 2019\nBAO n=21", "Zhao 2020\nICVA n=31", "Duan 2021\nICVA n=10", "Li 2025\nVBA n=8"]
    mrs02 = [76.5, 74.1, 70.0, 75.0]
    mrs03 = [94.1, 85.2, 90.0, None]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    x = np.arange(len(labels))
    w = 0.36
    ax.bar(x - w / 2, mrs02, w, color=TEAL, label="mRS 0–2", zorder=3)
    vals = [v if v is not None else 0 for v in mrs03]
    ax.bar(x + w / 2, vals, w, color=GOLD, label="mRS 0–3", zorder=3)
    for i, v in enumerate(mrs02):
        ax.text(i - w / 2, v + 1.5, f"{v:.1f}%", ha="center", fontsize=8, color=INK)
    for i, v in enumerate(mrs03):
        if v is not None:
            ax.text(i + w / 2, v + 1.5, f"{v:.1f}%", ha="center", fontsize=8, color=INK)
        else:
            ax.text(i + w / 2, 4, "NR", ha="center", fontsize=8, color=MUTED)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8, color=INK)
    ax.set_ylim(0, 110)
    ax.set_ylabel("随访良好功能结局（%）", fontsize=9, color=MUTED)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.14), fontsize=8, frameon=False, ncol=2)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED)
    save(fig, "fig_outcomes.png")


# ---------------------------------------------------------------- restenosis
def restenosis():
    data = [("Cai 2021", 27.3), ("Zhou 2023", 25.3), ("Chen 2024 高危", 80.0),
            ("Xia 2023 VBA", 16.7), ("Meta 2026", 15.0), ("Zhao 2020", 10.0)]
    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    y = np.arange(len(data))[::-1]
    colors = [CORAL if v >= 25 else TEAL for _, v in data]
    ax.barh(y, [v for _, v in data], color=colors, alpha=0.9, height=0.55, zorder=3)
    for yy, (_, v) in zip(y, data):
        ax.text(v + 1, yy, f"{v:.1f}%", va="center", fontsize=8.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([d[0] for d in data], fontsize=9, color=INK)
    ax.set_xlim(0, 90)
    ax.set_xlabel("再狭窄/再闭塞（%）", fontsize=9, color=MUTED)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0)
    save(fig, "fig_restenosis.png")


# ---------------------------------------------------------------- technique
def vessel_path(ax, pts, color=TEAL, lw=7, alpha=1.0, ls="-", z=3):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, alpha=alpha, ls=ls, solid_capstyle="round", zorder=z)


def technique():
    fig, axes = plt.subplots(1, 3, figsize=(9.8, 3.4))
    for ax in axes:
        ax.set_xlim(0, 10)
        ax.set_ylim(2.4, 8.0)
        ax.axis("off")

    def vessel(ax):
        ax.plot([0.6, 9.4], [5.2, 5.2], color=TEAL, lw=11, alpha=0.18, solid_capstyle="round", zorder=2)
        ax.plot([0.6, 9.4], [5.2, 5.2], color=TEAL, lw=5.2, alpha=0.55, solid_capstyle="round", zorder=3)
        ax.add_patch(Rectangle((4.5, 3.9), 1.0, 2.6, fc=CORAL, ec="none", alpha=0.75, zorder=4))

    titles = ["① 顺行穿越", "② 逆行入路", "③ 分期再通"]
    subs = ["经股/桡动脉，导丝正向通过闭塞", "经对侧椎/颈侧支（REVANS）", "先球囊恢复灌注，再支架"]
    for ax, t, sub in zip(axes, titles, subs):
        ax.set_title(t, fontsize=12, color=INK, fontweight="bold", pad=10)
        ax.text(5, 2.55, sub, ha="center", fontsize=7.5, color=MUTED)
        vessel(ax)

    # antegrade
    ax = axes[0]
    ax.annotate("", xy=(7.6, 5.2), xytext=(1.0, 5.2),
                arrowprops=dict(arrowstyle="-|>", color=TEAL2, lw=2.2, mutation_scale=14), zorder=6)
    ax.add_patch(Rectangle((3.7, 4.35), 0.75, 1.7, fc="white", ec=TEAL2, lw=1.3, zorder=7))
    ax.text(4.07, 6.55, "球囊", fontsize=7.5, color=TEAL, ha="center")
    ax.add_patch(Rectangle((6.0, 4.15), 1.5, 2.1, fc="none", ec=GOLD, lw=1.5, zorder=7))
    ax.text(6.75, 6.55, "支架", fontsize=7.5, color="#9A6B12", ha="center")

    # retrograde
    ax = axes[1]
    ax.annotate("", xy=(3.6, 5.2), xytext=(8.4, 5.2),
                arrowprops=dict(arrowstyle="-|>", color=CORAL, lw=2.2, mutation_scale=14), zorder=6)
    ax.plot([7.6, 7.6, 3.6], [5.6, 7.3, 7.3], color=TEAL2, lw=1.8, ls=(0, (3, 2)), zorder=5)
    ax.annotate("", xy=(4.2, 7.3), xytext=(6.8, 7.3),
                arrowprops=dict(arrowstyle="-|>", color=TEAL2, lw=1.5, mutation_scale=12), zorder=5)
    ax.text(6.3, 6.25, "侧支", fontsize=7.5, color=TEAL2)

    # staged
    ax = axes[2]
    ax.add_patch(Rectangle((2.9, 4.3), 1.0, 1.8, fc="none", ec=TEAL2, lw=1.6, zorder=7))
    ax.add_patch(Rectangle((6.1, 4.1), 1.7, 2.2, fc="none", ec=GOLD, lw=1.6, zorder=7))
    ax.annotate("", xy=(4.4, 7.0), xytext=(2.7, 7.0),
                arrowprops=dict(arrowstyle="-|>", color=TEAL2, lw=1.4, mutation_scale=12), zorder=6)
    ax.annotate("", xy=(7.2, 7.0), xytext=(4.7, 7.0),
                arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.4, mutation_scale=12), zorder=6)
    ax.text(2.6, 7.45, "球囊", fontsize=7.5, color=TEAL, ha="center")
    ax.text(6.9, 7.45, "支架", fontsize=7.5, color="#9A6B12", ha="center")

    save(fig, "fig_technique.png")


# ---------------------------------------------------------------- cases
def base_case(ax, occlusion=("left_v4",), recon=True, title=""):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    # simplified posterior circulation
    # left/right vertebral
    for x, sign in [(3.2, 1), (6.8, -1)]:
        ax.plot([x, x + sign * 0.3, x + sign * 0.1], [1.2, 4.2, 6.2], color=TEAL, lw=5, solid_capstyle="round", zorder=4)
    ax.plot([3.2, 4.2, 5.0], [6.2, 7.6, 8.2], color=TEAL, lw=6, solid_capstyle="round", zorder=4)
    ax.plot([6.8, 5.8, 5.0], [6.2, 7.6, 8.2], color=TEAL, lw=6, solid_capstyle="round", zorder=4)
    ax.plot([5.0, 5.0], [8.2, 9.2], color=TEAL, lw=6, solid_capstyle="round", zorder=4)
    # PCA
    ax.plot([5, 2.8], [9.2, 9.6], color=TEAL, lw=3, zorder=4)
    ax.plot([5, 7.2], [9.2, 9.6], color=TEAL, lw=3, zorder=4)
    # basilar branches
    for yy in (8.6, 8.9):
        ax.plot([5, 3.6], [yy, yy + 0.4], color=TEAL, lw=1.2, alpha=0.6, zorder=3)
        ax.plot([5, 6.4], [yy, yy + 0.4], color=TEAL, lw=1.2, alpha=0.6, zorder=3)
    # brainstem
    ax.add_patch(FancyBboxPatch((4.2, 6.8), 1.6, 2.2, boxstyle="round,pad=0.1,rounding_size=0.4",
                                fc="#F2D8C9", ec="#D9A441", lw=0.8, alpha=0.7, zorder=1))
    # occlusion markers
    if "left_v4" in occlusion:
        ax.scatter(3.9, 6.9, s=180, facecolor=CORAL, edgecolor="white", linewidth=2, zorder=8)
        ax.text(2.1, 7.2, "闭塞", fontsize=8, color=CORAL, fontweight="bold")
    if "basilar" in occlusion:
        ax.scatter(5.0, 8.55, s=200, facecolor=CORAL, edgecolor="white", linewidth=2, zorder=8)
        ax.text(5.4, 7.7, "闭塞", fontsize=8, color=CORAL, fontweight="bold")
    if recon:
        ax.annotate("", xy=(4.8, 8.4), xytext=(4.1, 7.1),
                    arrowprops=dict(arrowstyle="-|>", color=TEAL2, lw=2.2, ls=(0, (3, 2))), zorder=7)
        ax.text(2.2, 5.7, "再通", fontsize=8, color=TEAL2, fontweight="bold")
    if title:
        ax.set_title(title, fontsize=10, color=INK)


def case_figures():
    fig, ax = plt.subplots(figsize=(5.2, 4.8))
    base_case(ax, occlusion=("left_v4",), recon=True, title="")
    ax.text(5, 0.2, "左 V4 闭塞 → 经后交通侧支逆行充盈基底动脉", ha="center", fontsize=8, color=MUTED)
    save(fig, "fig_case1.png")

    fig, ax = plt.subplots(figsize=(5.2, 4.8))
    # bilateral VA occlusion + basilar filling
    base_case(ax, occlusion=("left_v4",), recon=False, title="")
    ax.scatter(6.1, 6.9, s=180, facecolor=CORAL, edgecolor="white", linewidth=2, zorder=8)
    ax.text(6.4, 7.3, "闭塞", fontsize=8, color=CORAL, fontweight="bold")
    ax.annotate("", xy=(5.0, 8.4), xytext=(5.0, 9.0),
                arrowprops=dict(arrowstyle="-|>", color=TEAL2, lw=2.2, ls=(0, (3, 2))), zorder=7)
    ax.text(5, 0.2, "双侧椎动脉闭塞；基底动脉由侧支/后交通供血", ha="center", fontsize=8, color=MUTED)
    save(fig, "fig_case2.png")


if __name__ == "__main__":
    hero()
    anatomy()
    morphology()
    evidence_map()
    forest()
    predictors()
    complications()
    outcomes()
    restenosis()
    technique()
    case_figures()

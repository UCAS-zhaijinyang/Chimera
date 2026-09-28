"""Generate a clean quantitative evaluation pyramid as a PNG."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "dataset-evaluation-pyramid.png"
W, H = 2400, 1800
BG = (247, 250, 253)
INK = (24, 40, 61)
MUTED = (91, 111, 133)
WHITE = (255, 255, 255)
GRID = (214, 225, 235)
TEAL = (28, 167, 177)
BLUE = (62, 124, 205)
PURPLE = (124, 102, 199)
ORANGE = (223, 139, 50)
CORAL = (209, 91, 103)


def fnt(size, bold=False):
    path = "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc"
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def centered(draw, text, box, font, fill):
    left, top, right, bottom = box
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((left + right - bb[2]) / 2, (top + bottom - bb[3]) / 2 - 3), text, font=font, fill=fill)


def wrap(draw, text, x, y, width, font, fill, gap=7):
    lines, line = [], ""
    for char in text:
        candidate = line + char
        if draw.textbbox((0, 0), candidate, font=font)[2] > width and line:
            lines.append(line)
            line = char
        else:
            line = candidate
    if line:
        lines.append(line)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def main():
    image = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(image)

    d.text((120, 72), "ChimeraLog+ 生成数据集评测金字塔", font=fnt(62, True), fill=INK)
    d.text((124, 155), "从“数据没有错误”到“数据确实可用于威胁检测”", font=fnt(31), fill=TEAL)
    d.line((120, 220, 2280, 220), fill=GRID, width=3)

    # Pyramid levels from bottom to top.
    levels = [
        ("L0", "数据完整性", "必须通过", "完整率 ≥99.5%  ·  trace 关联 ≥99%  ·  Artifact 血缘 100%  ·  时间/权限违规 = 0", TEAL),
        ("L1", "计划—执行一致性", "必须通过", "计划—执行 F1 ≥0.85  ·  阶段越界 = 0  ·  handoff 时序错误 = 0  ·  计划外行为 ≤10%", BLUE),
        ("L2", "工具工作流终态", "必须通过", "合法转移 = 100%  ·  黄金任务成功 ≥90%  ·  Artifact 链成功 ≥90%  ·  附带破坏 = 0", PURPLE),
        ("L3", "统计分布保真", "对照评测", "KS / Wasserstein ≤0.10  ·  正常数据区分 AUC ≤0.65  ·  相关差异 ≤0.20  ·  模板重复 ≤5%", ORANGE),
        ("L4", "语义与组织真实性", "专家 + 图", "Likert ≥4.0/5  ·  Krippendorff α ≥0.67  ·  组内协作 > 跨组  ·  角色一致 ≥95%", CORAL),
        ("L5", "下游检测效用", "最终证明", "TSTR / Real-to-Real F1 ≥0.80  ·  跨场景下降 ≤20pp  ·  Recall@k 高于旧基线  ·  标签泄漏 AUC ≤0.60", TEAL),
    ]

    center_x = 930
    base_y = 1570
    level_h = 175
    widths = [1700, 1530, 1360, 1190, 1020, 850]
    for i, (code, title, kind, metrics, color) in enumerate(levels):
        y_bottom = base_y - i * level_h
        y_top = y_bottom - level_h + 12
        width = widths[i]
        left, right = center_x - width // 2, center_x + width // 2
        # slight shadow
        d.polygon([(left + 8, y_top + 8), (right + 8, y_top + 8), (right + 8, y_bottom + 8), (left + 8, y_bottom + 8)], fill=(225, 232, 240))
        d.polygon([(left, y_top), (right, y_top), (right, y_bottom), (left, y_bottom)], fill=color)
        d.line((left, y_top, right, y_top), fill=WHITE, width=2)
        # content panel
        d.rounded_rectangle((left + 22, y_top + 18, right - 22, y_bottom - 18), radius=16, fill=WHITE)
        centered(d, code, (left + 45, y_top + 30, left + 145, y_bottom - 30), fnt(28, True), color)
        d.text((left + 175, y_top + 28), title, font=fnt(30, True), fill=INK)
        badge_box = (right - 190, y_top + 28, right - 40, y_top + 70)
        d.rounded_rectangle(badge_box, radius=18, fill=color)
        centered(d, kind, badge_box, fnt(19, True), WHITE)
        wrap(d, metrics, left + 175, y_top + 82, right - left - 230, fnt(21), MUTED, gap=4)

    # Side labels clarify how to interpret the pyramid.
    # Keep the guide outside the widest (L0) card so it never collides with
    # the pyramid when the image is viewed at a reduced size.
    d.text((90, 555), "质量证明逐层收紧", font=fnt(26, True), fill=MUTED)
    guide_x = 55
    d.line((guide_x, 650, guide_x, 1430), fill=GRID, width=5)
    for y, label in [(690, "结构"), (870, "执行"), (1050, "行为"), (1230, "语义"), (1410, "效用")]:
        d.ellipse((guide_x - 14, y, guide_x + 14, y + 28), fill=TEAL)
        d.text((18, y - 4), label, font=fnt(20), fill=MUTED)

    # Right-side experimental recipe.
    rx0, ry0, rx1, ry1 = 1780, 420, 2270, 1360
    d.rounded_rectangle((rx0, ry0, rx1, ry1), radius=24, fill=WHITE, outline=GRID, width=3)
    d.text((1820, 462), "实验配方", font=fnt(32, True), fill=INK)
    d.text((1820, 510), "避免一次运行下结论", font=fnt(22), fill=ORANGE)
    items = [
        "3 种公司场景",
        "每场景 ≥ 5 次独立运行",
        "每次 ≥ 20 个工作日",
        "legacy vs 文件系统工作流",
        "按员工 / run / 场景切分",
        "均值 + 95% bootstrap CI",
    ]
    yy = 585
    for item in items:
        d.ellipse((1822, yy + 8, 1836, yy + 22), fill=TEAL)
        wrap(d, item, 1860, yy, 350, fnt(22), INK, gap=4)
        yy += 73

    d.rounded_rectangle((1815, 1080, 2235, 1305), radius=18, fill=(235, 249, 247), outline=TEAL, width=2)
    d.text((1845, 1112), "可用数据集", font=fnt(28, True), fill=TEAL)
    wrap(d, "L0–L2 过门禁；L3 不显著偏离参考；L4 不低于旧基线；L5 达到 TSTR 与稳定性门槛。", 1845, 1165, 350, fnt(20), INK, gap=8)

    d.line((120, 1680, 2280, 1680), fill=GRID, width=3)
    d.text((120, 1715), "数据来源：phase_plans.json · init_schedule/ · execution_logs/ · manifest.jsonl · tool_calls.csv · logon.csv / email.csv", font=fnt(21), fill=MUTED)
    d.text((120, 1760), "结论原则：先证明真实、完整、可追溯，再证明像真实行为，最后证明能支持威胁检测。", font=fnt(23, True), fill=TEAL)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, "PNG", optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()

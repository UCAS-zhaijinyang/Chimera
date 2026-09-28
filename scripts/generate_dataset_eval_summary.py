"""Render a quantitative ChimeraLog+ evaluation framework infographic."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "dataset-evaluation-framework.png"


def font(size: int, bold: bool = False):
    candidates = (
        "/System/Library/Fonts/STHeiti Medium.ttc"
        if bold
        else "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


W, H = 2400, 1950
BG = (10, 20, 38)
WHITE = (239, 245, 252)
MUTED = (169, 187, 207)
LINE = (55, 78, 106)
CARD = (20, 35, 57)
CYAN = (64, 205, 220)
GREEN = (92, 211, 155)
AMBER = (244, 184, 85)
PURPLE = (172, 137, 255)
RED = (246, 113, 122)


def rounded(draw, box, radius=22, fill=CARD, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_wrapped(draw, text, xy, max_width, fnt, fill=WHITE, line_gap=8):
    x, y = xy
    words = list(text)
    line = ""
    lines = []
    for char in words:
        candidate = line + char
        if draw.textbbox((0, 0), candidate, font=fnt)[2] > max_width and line:
            lines.append(line)
            line = char
        else:
            line = candidate
    if line:
        lines.append(line)
    step = fnt.size + line_gap
    for item in lines:
        draw.text((x, y), item, font=fnt, fill=fill)
        y += step
    return y


def metric(draw, x, y, label, value, accent):
    draw.ellipse((x, y + 8, x + 13, y + 21), fill=accent)
    draw.text((x + 27, y), label, font=font(22), fill=WHITE)
    draw.text((x + 490, y), value, font=font(22, bold=True), fill=accent)


def main():
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    # Header
    draw.text((90, 55), "ChimeraLog+ 生成数据集定量评测体系", font=font(60, True), fill=WHITE)
    draw.text(
        (94, 132),
        "从结构可信 → 行为真实 → 任务可用 → 重复稳定",
        font=font(31),
        fill=CYAN,
    )
    draw.text(
        (94, 181),
        "当前分支：阶段计划流水线 + 文件系统工作流 + Artifact lineage",
        font=font(23),
        fill=MUTED,
    )
    draw.line((90, 235, 2310, 235), fill=LINE, width=2)

    # Left-side flow spine
    spine_x = 155
    draw.line((spine_x, 315, spine_x, 1450), fill=(47, 81, 110), width=8)
    draw.text((88, 276), "证据金字塔", font=font(25, True), fill=MUTED)

    layers = [
        (
            "L0",
            "数据完整性",
            "门禁：结构和标签必须可信",
            [
                ("必填字段完整率", "≥ 99.5%"),
                ("trace / 员工 / 任务关联率", "≥ 99%"),
                ("Artifact 血缘闭合率", "100%"),
                ("时间、权限、攻击证据违规", "0"),
            ],
            CYAN,
        ),
        (
            "L1",
            "计划—执行一致性",
            "门禁：阶段计划真的约束行为",
            [
                ("计划—执行匹配 F1", "≥ 0.85"),
                ("阶段越界率 / handoff 时序错误", "0"),
                ("计划外行为率", "≤ 10%"),
                ("计划工时相对误差", "≤ 20%"),
            ],
            GREEN,
        ),
        (
            "L2",
            "工具工作流终态",
            "门禁：工具调用产生真实、合法的最终对象",
            [
                ("合法工具转移率", "100%"),
                ("黄金任务终态成功率", "≥ 90%"),
                ("Artifact 链成功率", "≥ 90%"),
                ("附带破坏 / 越权访问", "0"),
            ],
            AMBER,
        ),
        (
            "L3",
            "统计分布保真",
            "对照：生成行为是否接近参考企业数据",
            [
                ("KS / Wasserstein 距离", "≤ 0.10"),
                ("正常数据可区分 AUC", "≤ 0.65"),
                ("相关矩阵差异", "≤ 0.20"),
                ("活动模板重复率", "≤ 5%"),
            ],
            PURPLE,
        ),
        (
            "L4",
            "语义与组织真实性",
            "人工 + 图：内容、角色和协作关系像真实组织",
            [
                ("专家 Likert 均值", "≥ 4.0 / 5"),
                ("Krippendorff α", "≥ 0.67"),
                ("组内协作比例", "> 跨组比例"),
                ("角色 / 阶段 / handoff 一致性", "≥ 95%"),
            ],
            RED,
        ),
        (
            "L5",
            "下游检测效用",
            "最终：数据能否训练出可泛化的检测器",
            [
                ("TSTR F1 / Real-to-Real F1", "≥ 0.80"),
                ("跨场景 F1 下降", "≤ 20 pp"),
                ("Recall@k / Enrichment Ratio", "高于旧基线"),
                ("元数据标签泄漏 AUC", "≤ 0.60"),
            ],
            CYAN,
        ),
    ]

    y = 315
    card_h = 190
    for index, (level, title, subtitle, metrics, accent) in enumerate(layers):
        # spine marker
        cy = y + card_h // 2
        draw.ellipse((spine_x - 19, cy - 19, spine_x + 19, cy + 19), fill=accent, outline=BG, width=5)
        rounded(draw, (235, y, 1510, y + card_h), radius=24, fill=CARD, outline=(42, 64, 91), width=2)
        draw.rounded_rectangle((235, y, 260, y + card_h), radius=24, fill=accent)
        draw.text((293, y + 22), level, font=font(31, True), fill=accent)
        draw.text((390, y + 18), title, font=font(32, True), fill=WHITE)
        draw.text((390, y + 62), subtitle, font=font(21), fill=MUTED)
        metric_y = y + 84
        for label, value in metrics:
            metric(draw, 300, metric_y, label, value, accent)
            metric_y += 25
        y += card_h + 16

    # Right rail: experimental design and decision rule
    x0, y0, x1, y1 = 1570, 315, 2310, 1535
    rounded(draw, (x0, y0, x1, y1), radius=26, fill=(17, 31, 51), outline=(56, 85, 114), width=2)
    draw.text((1620, 355), "实验设计与结论规则", font=font(33, True), fill=WHITE)
    draw.text((1620, 405), "不能用一次运行、一个分数下结论", font=font(22), fill=AMBER)

    sections = [
        ("1  运行矩阵", ["3 种公司场景", "每场景 ≥ 5 次独立运行", "每次 ≥ 20 个工作日", "正常日 + 攻击日"]),
        ("2  对照组", ["legacy OWL/CAMEL", "文件系统工作流", "旧周计划", "阶段计划流水线"]),
        ("3  数据切分", ["按员工 / run / 场景切分", "禁止同一员工跨 train/test", "正常与攻击分别统计"]),
        ("4  统计报告", ["均值 + 95% bootstrap CI", "配对比较新旧框架", "报告差值，不只报绝对值"]),
    ]
    yy = 475
    for header, items in sections:
        draw.text((1620, yy), header, font=font(24, True), fill=CYAN)
        yy += 40
        for item in items:
            draw.ellipse((1630, yy + 9, 1642, yy + 21), fill=CYAN)
            draw.text((1660, yy), item, font=font(22), fill=WHITE)
            yy += 34
        yy += 22

    # Decision box
    rounded(draw, (1615, 1240, 2265, 1500), radius=20, fill=(24, 48, 61), outline=GREEN, width=2)
    draw.text((1650, 1272), "可用数据集的判定", font=font(27, True), fill=GREEN)
    decision = "L0–L2 全部过门禁\nL3 分布不显著偏离参考\nL4 语义评分不低于旧基线\nL5 TSTR 与稳定性达到门槛"
    draw_wrapped(draw, decision, (1650, 1324), 550, font(23), fill=WHITE, line_gap=10)

    # Footer source mapping
    draw.line((90, 1590, 2310, 1590), fill=LINE, width=2)
    draw.text((90, 1622), "当前分支数据来源", font=font(24, True), fill=MUTED)
    draw.text(
        (350, 1622),
        "phase_plans.json  ·  init_schedule/  ·  execution_logs/  ·  manifest.jsonl  ·  tool_calls.csv  ·  logon.csv / email.csv",
        font=font(22),
        fill=WHITE,
    )
    draw.text(
        (90, 1692),
        "原则：先验证数据是否真实、完整、可追溯，再验证它是否像真实行为，最后验证它能否支持威胁检测。",
        font=font(25, True),
        fill=CYAN,
    )
    draw.text((90, 1762), "建议门槛为第一版实验起点，应使用旧 ChimeraLog 基线校准。", font=font(20), fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, format="PNG", optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()

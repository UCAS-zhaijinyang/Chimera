"""Generate a readable overview and detailed metric matrix for dataset evaluation."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "dataset-evaluation-pyramid.png"
W, H = 3200, 2600

BG = (247, 250, 253)
INK = (24, 40, 61)
MUTED = (91, 111, 133)
GRID = (211, 223, 235)
WHITE = (255, 255, 255)
PANEL = (239, 245, 250)
TEAL = (28, 167, 177)
BLUE = (62, 124, 205)
PURPLE = (124, 102, 199)
ORANGE = (223, 139, 50)
CORAL = (209, 91, 103)


def fnt(size: int, bold: bool = False):
    path = "/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc"
    if Path(path).exists():
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_lines(draw, text, width, font):
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
    return lines or [""]


def draw_cell(draw, text, x, y, width, height, font_size, fill=INK, bold=False, align="left"):
    cell_font = fnt(font_size, bold)
    lines = wrap_lines(draw, text, width, cell_font)
    line_h = font_size + 5
    total_h = len(lines) * line_h - 5
    top = y + max(0, (height - total_h) // 2)
    for line in lines:
        line_width = draw.textbbox((0, 0), line, font=cell_font)[2]
        xx = x + max(0, (width - line_width) // 2) if align == "center" else x
        draw.text((xx, top), line, font=cell_font, fill=fill)
        top += line_h


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def main():
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)

    # Header
    draw.text((110, 72), "ChimeraLog+ 生成数据集评测体系", font=fnt(66, True), fill=INK)
    draw.text((114, 150), "左侧看证据层级，右侧查每个指标如何计算和判定", font=fnt(32), fill=TEAL)
    draw.text((114, 201), "每个指标都必须能从 execution_logs、Artifact 或对照数据中复算", font=fnt(23), fill=MUTED)
    draw.line((110, 262, 3090, 262), fill=GRID, width=3)

    layers = [
        ("L0", "数据完整性", "结构与标签可信", "结构门禁", TEAL),
        ("L1", "计划—执行一致性", "阶段计划约束行为", "执行门禁", BLUE),
        ("L2", "工具工作流终态", "工具产生合法对象", "工作流门禁", PURPLE),
        ("L3", "统计分布保真", "行为接近参考企业", "分布对照", ORANGE),
        ("L4", "语义与组织真实性", "内容和协作像真实组织", "语义复核", CORAL),
        ("L5", "下游检测效用", "数据支持可泛化检测", "最终证明", TEAL),
    ]

    # Left: a deliberately simple pyramid overview.
    draw.text((120, 315), "证据金字塔（总览）", font=fnt(31, True), fill=INK)
    draw.text((120, 365), "先过底层门禁，再逐层证明数据有用", font=fnt(21), fill=MUTED)
    center_x = 585
    base_y = 2110
    card_h = 238
    gap = 18
    widths = [920, 855, 790, 725, 660, 595]
    for i, (code, title, purpose, gate, color) in enumerate(layers):
        y_bottom = base_y - i * (card_h + gap)
        y_top = y_bottom - card_h
        width = widths[i]
        left = center_x - width // 2
        right = center_x + width // 2
        draw.rounded_rectangle((left + 8, y_top + 10, right + 8, y_bottom + 10), radius=18, fill=(224, 232, 240))
        rounded(draw, (left, y_top, right, y_bottom), 18, color)
        rounded(draw, (left + 16, y_top + 16, right - 16, y_bottom - 16), 12, WHITE)
        draw.text((left + 40, y_top + 36), code, font=fnt(31, True), fill=color)
        draw.text((left + 142, y_top + 31), title, font=fnt(31, True), fill=INK)
        draw.text((left + 142, y_top + 87), purpose, font=fnt(23), fill=MUTED)
        badge = (right - 170, y_top + 34, right - 38, y_top + 78)
        rounded(draw, badge, 20, color)
        draw_cell(draw, gate, badge[0], badge[1], badge[2] - badge[0], badge[3] - badge[1], 17, WHITE, True, "center")
        draw.line((left + 142, y_top + 138, right - 42, y_top + 138), fill=GRID, width=2)
        step = "基础数据" if i == 0 else "上一层通过后继续"
        draw.text((left + 142, y_top + 163), step, font=fnt(20), fill=color)

    # A small vertical reading cue, kept outside all cards.
    guide_x = 108
    draw.line((guide_x, 590, guide_x, 1980), fill=GRID, width=5)
    for i, label in enumerate(["结构", "执行", "行为", "分布", "语义", "效用"]):
        cy = base_y - i * (card_h + gap) - card_h // 2
        draw.ellipse((guide_x - 14, cy - 14, guide_x + 14, cy + 14), fill=TEAL)
        draw.text((35, cy - 14), label, font=fnt(19), fill=MUTED)

    # Right: detailed metric matrix.
    right_x0, right_x1 = 1130, 3090
    draw.text((right_x0, 315), "指标明细（每层 4 项）", font=fnt(31, True), fill=INK)
    draw.text((right_x0, 365), "名称、测量对象、计算方式和门槛同时展示，避免只记住一个分数", font=fnt(21), fill=MUTED)

    matrix_y = 420
    col_x = [right_x0 + 22, right_x0 + 485, right_x0 + 1005, right_x0 + 1650]
    col_w = [440, 500, 620, 390]
    header_h = 52
    rounded(draw, (right_x0, matrix_y, right_x1, matrix_y + header_h), 10, INK)
    for label, x, width in zip(["指标", "测量对象", "计算方式", "判定阈值"], col_x, col_w):
        draw_cell(draw, label, x, matrix_y, width, header_h, 21, WHITE, True, "left")
    matrix_y += header_h + 10

    metrics = [
        ("L0", "数据完整性", TEAL,
         [("必填字段完整率", "日志必填字段", "完整记录数 / 总记录数", "≥ 99.5%"),
          ("trace / 员工 / 任务关联率", "跨文件主键链路", "可关联记录数 / 总记录数", "≥ 99%"),
          ("Artifact 血缘闭合率", "输入—输出文件链", "有完整 inputs 的产物 / 总产物", "100%"),
          ("时间、权限、攻击证据违规", "硬约束与标签", "违规事件数", "0")]),
        ("L1", "计划—执行一致性", BLUE,
         [("计划—执行匹配 F1", "阶段计划与活动", "precision / recall 调和平均", "≥ 0.85"),
          ("阶段越界率", "活动所属阶段", "越界活动数 / 总活动数", "0"),
          ("handoff 时序错误率", "工具交接顺序", "错误交接数 / 总交接数", "0"),
          ("计划外行为率", "未被计划覆盖的活动", "计划外活动数 / 总活动数", "≤ 10%")]),
        ("L2", "工具工作流终态", PURPLE,
         [("合法工具转移率", "ToolGraph 边", "合法转移数 / 总转移数", "100%"),
          ("黄金任务终态成功率", "预定义任务结果", "成功终态数 / 任务总数", "≥ 90%"),
          ("Artifact 链成功率", "跨工具产物链", "闭合链数 / 任务总数", "≥ 90%"),
          ("附带破坏 / 越权访问", "副作用与 ACL", "违规事件数", "0")]),
        ("L3", "统计分布保真", ORANGE,
         [("KS / Wasserstein 距离", "活动时长、频率等分布", "生成集 vs 参考集距离", "≤ 0.10"),
          ("正常数据可区分 AUC", "生成集与真实集", "二分类器 ROC-AUC", "≤ 0.65"),
          ("相关矩阵差异", "员工—工具—活动关系", "相关矩阵平均绝对差", "≤ 0.20"),
          ("活动模板重复率", "文本与行为模板", "重复模板数 / 总模板数", "≤ 5%")]),
        ("L4", "语义与组织真实性", CORAL,
         [("专家 Likert 均值", "活动内容可读性", "专家评分均值（1–5）", "≥ 4.0 / 5"),
          ("Krippendorff α", "专家标注一致性", "多标注者一致性系数", "≥ 0.67"),
          ("组内协作比例", "组织协作结构", "组内协作 / 跨组协作", "> 1"),
          ("角色 / 阶段 / handoff 一致性", "画像与执行轨迹", "一致事件数 / 总事件数", "≥ 95%")]),
        ("L5", "下游检测效用", TEAL,
         [("TSTR / Real-to-Real F1", "威胁检测任务", "训练—测试 F1", "≥ 0.80"),
          ("跨场景 F1 下降", "不同公司场景", "目标场景 F1 − 源场景 F1", "≤ 20 pp"),
          ("Recall@k / Enrichment Ratio", "高风险行为检索", "Top-k 命中率 / 基线", "高于旧基线"),
          ("元数据标签泄漏 AUC", "场景与员工标签", "用元数据预测来源的 AUC", "≤ 0.60")]),
    ]

    row_h = 62
    group_h = 43
    for code, title, color, rows in metrics:
        rounded(draw, (right_x0, matrix_y, right_x1, matrix_y + group_h), 8, color)
        draw.text((right_x0 + 22, matrix_y + 8), f"{code}  {title}", font=fnt(22, True), fill=WHITE)
        matrix_y += group_h
        for row_index, row in enumerate(rows):
            fill = WHITE if row_index % 2 == 0 else PANEL
            draw.rectangle((right_x0, matrix_y, right_x1, matrix_y + row_h), fill=fill)
            draw.line((right_x0, matrix_y + row_h, right_x1, matrix_y + row_h), fill=GRID, width=1)
            for value, x, width in zip(row, col_x, col_w):
                draw_cell(draw, value, x, matrix_y, width, row_h, 19, color if value == row[-1] else INK, value == row[0], "left")
            matrix_y += row_h
        matrix_y += 8

    # Footer: experiment recipe and decision rule.
    footer_y = 2310
    draw.line((110, footer_y, 3090, footer_y), fill=GRID, width=3)
    draw.text((120, footer_y + 28), "实验配方", font=fnt(23, True), fill=INK)
    draw.text((285, footer_y + 28), "3 种公司场景 × 每场景 ≥5 次独立运行 × 每次 ≥20 个工作日；legacy vs 文件系统工作流；按员工 / run / 场景切分；均值 + 95% bootstrap CI", font=fnt(19), fill=MUTED)
    draw.text((120, footer_y + 78), "可用数据集", font=fnt(23, True), fill=TEAL)
    draw.text((285, footer_y + 78), "L0–L2 全部过门禁；L3 不显著偏离参考；L4 不低于旧基线；L5 达到 TSTR 与稳定性门槛。", font=fnt(19), fill=INK)
    draw.text((120, footer_y + 127), "数据来源", font=fnt(21, True), fill=MUTED)
    draw.text((285, footer_y + 127), "phase_plans.json · init_schedule/ · execution_logs/ · manifest.jsonl · tool_calls.csv · logon.csv / email.csv", font=fnt(18), fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, "PNG", optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()

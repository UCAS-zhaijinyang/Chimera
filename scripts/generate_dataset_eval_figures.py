#!/usr/bin/env python3
"""Generate figures for the Chimera dataset-evaluation research note."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "WenQuanYi Micro Hei"
for fp in font_manager.findSystemFonts(fontpaths=["/usr/share/fonts"], fontext="ttf"):
    low = fp.lower()
    if not any(k in low for k in ("wqy-microhei", "notosanscjk", "droid")):
        continue
    if not fp.lower().endswith((".ttf", ".otf", ".ttc")):
        continue
    try:
        font_manager.fontManager.addfont(fp)
        FONT = "WenQuanYi Micro Hei"
    except (NotImplementedError, OSError):
        continue
plt.rcParams["font.sans-serif"] = [FONT, "WenQuanYi Micro Hei", "Droid Sans Fallback", "DejaVu Sans"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"

NAVY = "#1B365D"
TEAL = "#2A9D8F"
GOLD = "#C9A227"
CORAL = "#C45C26"
GRAY = "#5C6B7A"
LIGHT = "#F4F7FB"
BOX = "#E8EEF5"


def _box(ax, x, y, w, h, text, fc, ec, fontsize=9, color="white", weight="bold"):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.4,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        fontweight=weight,
        wrap=True,
    )
    return patch


def _arrow(ax, x1, y1, x2, y2, color=NAVY, lw=1.4):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=lw,
            color=color,
        )
    )


def fig_before_after():
    fig, ax = plt.subplots(figsize=(12.4, 6.4))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_title("评测对象：接入两项改造后，生成数据会长成什么样", fontsize=14, color=NAVY, pad=8)

    _box(ax, 0.3, 4.9, 5.6, 1.1, "改前 ChimeraLog（NDSS 现网）", NAVY, NAVY, 11)
    for i, text in enumerate(
        [
            "扁平工具袋：Search / Write / Terminal 互相看不见",
            "邮件无附件字段，工作产物无法被下一工具打开",
            "全员同一套工具分布，角色不可分",
            "一场 90 人周会 → 一份截断纪要 → 全员平均任务",
            "攻击证据是自然语言，对不上对象 ID / 科室边界",
        ]
    ):
        _box(ax, 0.3, 4.1 - i * 0.75, 5.6, 0.65, text, LIGHT, BOX, 8.2, NAVY, "normal")

    _box(ax, 6.5, 4.9, 5.6, 1.1, "评测对象：改造后应产出的 ChimeraLog+", TEAL, TEAL, 11)
    for i, text in enumerate(
        [
            "跨应用对象链：EHR → 表 → Drive → 带附件邮件 → Chat",
            "Artifact + ACL + policy-id 可查询，附件是一等公民",
            "角色 toolkit 分化：行政默认无 EHR，越权可读成标签",
            "科室级联会议：约 18 场、单场 ≤10 人、无全员大会",
            "攻击走同一对象图但越权 / 外发 / 跨科，ID 保持稳定",
        ]
    ):
        _box(ax, 6.5, 4.1 - i * 0.75, 5.6, 0.65, text, "#E6F6F3", TEAL, 8.2, NAVY, "normal")

    _arrow(ax, 5.95, 3.0, 6.45, 3.0, TEAL, 2.0)
    ax.text(6.2, 3.25, "评这个", ha="center", fontsize=9, color=TEAL, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "dataset-eval-before-after.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def fig_coverage_gap():
    fig, ax = plt.subplots(figsize=(12.2, 5.8))
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 5.8)
    ax.axis("off")
    ax.set_title("原 Chimera 评测仍然必要，但盖不住新数据形态", fontsize=14, color=NAVY, pad=8)

    headers = ["原论文已做", "改造后新增需求", "若只沿用原文会漏什么"]
    xs = [0.25, 4.2, 8.15]
    colors = [NAVY, TEAL, CORAL]
    for x, h, c in zip(xs, headers, colors):
        _box(ax, x, 4.7, 3.8, 0.75, h, c, c, 11)

    rows = [
        (
            "专家 Likert + α=0.87\n时序直方图 / 行为熵",
            "对象链终态、附件、ACL\n科室模块度、会议拓扑",
            "邮件「看起来像真的」\n但附件字段可以全是空的",
        ),
        (
            "ITD：SVM/CNN/GCN\nPrecision / Recall / F1",
            "跨应用因果、越权读 EHR\n偏离 recipe 的检测标签",
            "检测器仍吃 user-day 向量\n看不到 Drive→外发这条链",
        ),
        (
            "跨场景泛化\nTech → Finance / CERT",
            "pass^k 稳定性\nTSTR 式下游效用",
            "单次 LLM 文案好看\n对象 schema 每次都变",
        ),
    ]
    for i, (a, b, c) in enumerate(rows):
        y = 3.35 - i * 1.45
        _box(ax, xs[0], y, 3.8, 1.3, a, LIGHT, BOX, 8.4, NAVY, "normal")
        _box(ax, xs[1], y, 3.8, 1.3, b, "#E6F6F3", TEAL, 8.4, NAVY, "normal")
        _box(ax, xs[2], y, 3.8, 1.3, c, "#FCEEE8", CORAL, 8.4, NAVY, "normal")
    fig.tight_layout()
    fig.savefig(OUT / "dataset-eval-coverage-gap.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def fig_paper_matrix():
    papers = [
        "Glasser CERT",
        "Lindauer",
        "Greitzer",
        "TWOS",
        "Chimera",
        "TSTR",
        "Alaa 保真",
        "CTGAN",
        "AppWorld",
        "τ-bench",
        "AgentCo.",
        "UNICORN",
        "G-Eval",
        "GRAPHIA",
    ]
    methods = [
        "SUT 相对真实",
        "专家/IRR",
        "统计分布",
        "终态/对象链",
        "稳定性 pass^k",
        "组织图/MMD",
        "语义可读",
        "检测效用",
        "溯源图",
    ]
    # 1 = 核心抽取, 0.45 = 相关但不作为主指标
    grid = {
        "Glasser CERT": [1, 0.45, 1, 0, 0, 0.45, 0.45, 1, 0],
        "Lindauer": [1, 0.45, 1, 0, 0, 0, 0, 1, 0],
        "Greitzer": [1, 1, 0, 0, 0, 0, 0, 1, 0],
        "TWOS": [0.45, 1, 0.45, 0, 0, 0.45, 1, 1, 0],
        "Chimera": [0.45, 1, 1, 0, 0, 0, 1, 1, 0],
        "TSTR": [0, 0, 0.45, 0, 0, 0, 0, 1, 0],
        "Alaa 保真": [0, 0, 1, 0, 0, 0, 0, 0.45, 0],
        "CTGAN": [0, 0, 1, 0, 0, 0, 0, 1, 0],
        "AppWorld": [0, 0, 0, 1, 0, 0, 0, 0, 0],
        "τ-bench": [0, 0, 0, 1, 1, 0, 0, 0, 0],
        "AgentCo.": [0, 0, 0, 1, 0.45, 0.45, 0.45, 0, 0],
        "UNICORN": [0, 0, 0, 0.45, 0, 0, 0, 1, 1],
        "G-Eval": [0, 0.45, 0, 0, 0, 0, 1, 0, 0],
        "GRAPHIA": [0, 0, 0.45, 0, 0, 1, 0.45, 0, 0],
    }

    fig, ax = plt.subplots(figsize=(12.6, 6.8))
    ax.set_xlim(-2.4, len(methods) + 0.5)
    ax.set_ylim(-0.7, len(papers) + 1.1)
    ax.axis("off")
    ax.set_title("论文 × 评测切面（深绿=我们抽取的主方法）", fontsize=14, color=NAVY, pad=6)

    for j, m in enumerate(methods):
        ax.text(j + 0.5, len(papers) + 0.35, m, ha="center", va="bottom", fontsize=8, color=NAVY, rotation=18)
    for i, p in enumerate(reversed(papers)):
        y = i
        ax.text(-0.15, y + 0.5, p, ha="right", va="center", fontsize=8.5, color=NAVY)
        for j, val in enumerate(grid[p]):
            if val >= 0.9:
                fc, ec, alpha = TEAL, TEAL, 1.0
            elif val >= 0.4:
                fc, ec, alpha = GOLD, GOLD, 0.55
            else:
                fc, ec, alpha = BOX, BOX, 0.35
            rect = Rectangle((j, y), 0.92, 0.86, facecolor=fc, edgecolor=ec, alpha=alpha, linewidth=0.6)
            ax.add_patch(rect)
    ax.text(
        len(methods) / 2,
        -0.45,
        "青绿=最终体系主指标　金色=辅助　浅灰=不抽",
        ha="center",
        fontsize=9,
        color=GRAY,
    )
    fig.tight_layout()
    fig.savefig(OUT / "dataset-eval-paper-matrix.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def fig_six_layers():
    fig, ax = plt.subplots(figsize=(12.4, 6.6))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    ax.set_title("初步评测体系：六层由底向上，先自动化再请专家", fontsize=14, color=NAVY, pad=8)

    layers = [
        (NAVY, "L0 结构与标签", "schema / 缺失率 / 身份稳定 / MITRE 对齐 / 攻击可回放"),
        (TEAL, "L1 工作流终态", "AppWorld：附件、chat.ref、禁止裸发 EHR、无附带破坏"),
        ("#3D7EA6", "L2 组织与协作图", "无全员会、单场≤10、模块度、跨科边稀疏、task force 显式"),
        (GOLD, "L3 统计保真", "时序直方图、熵、α-Precision/β-Recall；对照 CERT/TWOS/旧日志"),
        (CORAL, "L4 语义可读", "专家 Likert + Krippendorff α；G-Eval 只做预筛"),
        ("#6B4C9A", "L5 下游效用", "ITD F1、跨分布、TSTR 变体、pass^k、可选 UNICORN"),
    ]
    for i, (color, title, desc) in enumerate(layers):
        y = 5.35 - i * 0.88
        _box(ax, 0.35, y, 2.7, 0.75, title, color, color, 10)
        _box(ax, 3.25, y, 8.8, 0.75, desc, LIGHT, BOX, 9.2, NAVY, "normal")
        if i < len(layers) - 1:
            _arrow(ax, 1.7, y, 1.7, y - 0.12, GRAY, 1.0)
    fig.tight_layout()
    fig.savefig(OUT / "dataset-eval-six-layers.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def fig_tradeoff():
    fig, ax = plt.subplots(figsize=(12.4, 5.6))
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.set_title("评测方法怎么组合：没有一种能单独当全面评测", fontsize=14, color=NAVY, pad=8)

    items = [
        (0.3, "专家 Likert\nKrippendorff α", "像不像真的", "贵、样本小\n看不见对象链", GOLD),
        (2.7, "时序 / 熵\nα-Precision", "分布像不像", "不管因果\n不管权限", TEAL),
        (5.1, "终态单测\nAppWorld / τ", "链对不对", "要有 Bus\n不测文案", NAVY),
        (7.5, "组织图 MMD\n模块度", "科室像不像", "需对照图\n不测攻击", "#3D7EA6"),
        (9.9, "ITD F1 / TSTR\npass^k", "有没有用", "标签泄漏\n分布捷径", CORAL),
    ]
    for x, title, good, bad, color in items:
        _box(ax, x, 4.15, 2.2, 1.1, title, color, color, 10)
        _box(ax, x, 2.55, 2.2, 1.4, "抽取：\n" + good, "#E6F6F3", TEAL, 8.5, NAVY, "normal")
        _box(ax, x, 0.85, 2.2, 1.5, "短板：\n" + bad, "#FCEEE8", CORAL, 8.5, NAVY, "normal")
    fig.tight_layout()
    fig.savefig(OUT / "dataset-eval-method-tradeoff.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    fig_before_after()
    fig_coverage_gap()
    fig_paper_matrix()
    fig_six_layers()
    fig_tradeoff()
    print("wrote figures to", OUT)


if __name__ == "__main__":
    main()

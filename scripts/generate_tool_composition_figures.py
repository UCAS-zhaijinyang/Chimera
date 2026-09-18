#!/usr/bin/env python3
"""Generate technical figures for the Chimera tool-composition research note."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

FONT = "WenQuanYi Micro Hei"
_added = False
for fp in font_manager.findSystemFonts(fontpaths=["/usr/share/fonts"], fontext="ttf"):
    low = fp.lower()
    if not any(k in low for k in ("wqy-microhei", "notosanscjk", "droid")):
        continue
    if not fp.lower().endswith((".ttf", ".otf", ".ttc")):
        continue
    try:
        font_manager.fontManager.addfont(fp)
        _added = True
    except (NotImplementedError, OSError):
        continue
if not _added:
    FONT = "DejaVu Sans"
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


def _arrow(ax, x1, y1, x2, y2, color=NAVY, style="-|>", lw=1.4, ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle=style,
            mutation_scale=12,
            linewidth=lw,
            linestyle=ls,
            color=color,
        )
    )


def figure_current_callgraph():
    fig, ax = plt.subplots(figsize=(13.2, 7.2), dpi=160)
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    ax.set_title(
        "Chimera 现状调用图（对照 src/task.py / member_email.py / daily_execution_auto.py）",
        fontsize=14,
        color=NAVY,
        pad=12,
        fontweight="bold",
    )

    _box(ax, 0.4, 6.1, 12.4, 0.7, "Phase 2/3  日仿真循环  ·  Member.execute_task()", LIGHT, NAVY, 11, NAVY)

    _box(ax, 0.5, 4.4, 7.6, 1.3, "", BOX, NAVY, 1, NAVY)
    ax.text(4.3, 5.4, "工作任务路径  OWL RolePlaying", ha="center", fontsize=10, color=NAVY, fontweight="bold")
    ax.text(4.3, 5.05, "task.construct_society()  →  扁平 tools=[]", ha="center", fontsize=9, color=GRAY)
    ax.text(4.3, 4.7, "FileWrite  ·  Terminal  ·  Browser  ·  Search", ha="center", fontsize=9, color=TEAL)

    _box(ax, 8.6, 4.4, 4.1, 1.3, "", "#F8E8DC", CORAL, 1, CORAL)
    ax.text(10.65, 5.4, "邮件路径  单独 LLM", ha="center", fontsize=10, color=CORAL, fontweight="bold")
    ax.text(10.65, 5.05, "is_email_send_activity()", ha="center", fontsize=9, color=GRAY)
    ax.text(10.65, 4.7, "无附件 / 不读工作区文件", ha="center", fontsize=9, color=CORAL)

    tools = [
        (0.7, 2.6, "Search\nDuckDuckGo/Google"),
        (2.7, 2.6, "Browser\nPlaywright"),
        (4.7, 2.6, "FileWrite\noutput_dir"),
        (6.7, 2.6, "Terminal\nworking_dir"),
    ]
    for x, y, t in tools:
        _box(ax, x, y, 1.8, 1.15, t, TEAL, TEAL, 8)
    _box(ax, 9.35, 2.6, 2.6, 1.15, "Email JSON\nsubject + content", CORAL, CORAL, 8)

    ax.text(4.3, 2.2, "工具之间没有 schema 边，也没有后继约束", ha="center", fontsize=9, color=GRAY)
    ax.plot([1.6, 3.6], [2.55, 2.55], linestyle=":", color="#C0392B", lw=1.8)
    ax.plot([3.6, 5.6], [2.55, 2.55], linestyle=":", color="#C0392B", lw=1.8)
    ax.plot([5.6, 7.6], [2.55, 2.55], linestyle=":", color="#C0392B", lw=1.8)
    ax.text(4.6, 1.85, "X  无数据流边", ha="center", fontsize=9, color="#C0392B", fontweight="bold")

    _box(ax, 0.5, 0.35, 5.8, 1.2, "profile.tools[] 仅是人设文本\nSketch / EHR 等从未绑定 CAMEL Toolkit", GOLD, GOLD, 9, NAVY)
    _box(ax, 6.7, 0.35, 6.0, 1.2, "每次 run_task 独立进程\n当日文件、邮件、浏览器缓存互不共享", GRAY, GRAY, 9, "white")

    _arrow(ax, 4.3, 4.4, 4.3, 3.8, TEAL)
    _arrow(ax, 10.65, 4.4, 10.65, 3.8, CORAL)
    fig.tight_layout()
    path = OUT / "fig-current-callgraph.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def figure_target_stack():
    fig, ax = plt.subplots(figsize=(13.2, 7.4), dpi=160)
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 7.4)
    ax.axis("off")
    ax.set_title(
        "建议移植的四层栈：Planner → Tool Graph → 企业应用 → Artifact Bus",
        fontsize=14,
        color=NAVY,
        pad=12,
        fontweight="bold",
    )

    layers = [
        (6.35, "L3  Planner / Role Router   HuggingGPT · TPTU-v2 · ToolChain*", "#14375A"),
        (4.95, "L2  Tool Graph   ToolNet · ControlLLM · GTool   边 = schema 对齐的合法过渡", TEAL),
        (3.55, "L1  企业应用层   AppWorld · TheAgentCompany · OfficeBench   Email/Drive/Chat/Calendar/EHR/Tickets", GOLD),
        (2.15, "L0  Artifact Bus + 权限   共享文件、邮件、工单、病历行；按角色 ACL 读写", CORAL),
    ]
    for y, text, color in layers:
        _box(ax, 0.5, y, 12.2, 1.15, text, color, color, 11)

    _arrow(ax, 6.6, 6.35, 6.6, 6.1, NAVY)
    _arrow(ax, 6.6, 4.95, 6.6, 4.7, TEAL)
    _arrow(ax, 6.6, 3.55, 6.6, 3.3, GOLD)

    ax.text(
        6.6,
        1.45,
        "执行痕迹 → AWM 工作流记忆（可复用配方）→ 次日计划 / 攻击链都可以检索",
        ha="center",
        fontsize=10,
        color=NAVY,
        fontweight="bold",
    )
    ax.text(
        6.6,
        0.85,
        "落地文件：src/tool_composition.py → task.py / member_email.py / daily_execution_auto.py / profile_generation.py",
        ha="center",
        fontsize=9,
        color=GRAY,
    )
    fig.tight_layout()
    path = OUT / "fig-target-stack.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def figure_paper_map():
    papers = [
        "HuggingGPT",
        "Chameleon",
        "ToolLLM",
        "ControlLLM",
        "ToolNet",
        "GTool",
        "ToolChain*",
        "AppWorld",
        "TheAgentCompany",
        "OfficeBench",
        "WorkArena",
        "τ-bench",
        "Generative Agents",
        "MetaGPT",
        "AWM",
        "TPTU-v2",
    ]
    methods = [
        "角色路由",
        "工具图",
        "共享应用状态",
        "工作流记忆",
        "邮件/办公套件",
        "评测/策略",
    ]
    # 1 = 强相关, 0.5 = 中相关
    heat = {
        "HuggingGPT": [1, 0.5, 0, 0, 0, 0],
        "Chameleon": [1, 0.5, 0, 0, 0, 0],
        "ToolLLM": [0.5, 0.5, 0, 0, 0, 0.5],
        "ControlLLM": [0.5, 1, 0, 0, 0, 0],
        "ToolNet": [0, 1, 0, 0, 0, 0],
        "GTool": [0, 1, 0, 0, 0, 0],
        "ToolChain*": [0.5, 1, 0, 0, 0, 0],
        "AppWorld": [0, 0.5, 1, 0, 0.5, 1],
        "TheAgentCompany": [0, 0.5, 1, 0, 1, 1],
        "OfficeBench": [0, 0.5, 1, 0, 1, 1],
        "WorkArena": [0, 0, 1, 0, 0.5, 1],
        "τ-bench": [0, 0, 1, 0, 0.5, 1],
        "Generative Agents": [0.5, 0, 0.5, 1, 0, 0],
        "MetaGPT": [1, 0, 0.5, 0.5, 0.5, 0],
        "AWM": [0, 0.5, 0, 1, 0, 0.5],
        "TPTU-v2": [1, 0.5, 0, 0, 0, 0.5],
    }
    import numpy as np

    data = np.array([heat[p] for p in papers])
    fig, ax = plt.subplots(figsize=(11.5, 8.2), dpi=160)
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list(
        "chimera", ["#F4F7FB", "#7EB6A4", "#1B365D"]
    )
    im = ax.imshow(data, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, fontsize=10, color=NAVY)
    ax.set_yticks(range(len(papers)))
    ax.set_yticklabels(papers, fontsize=10, color=NAVY)
    ax.set_title("论文 × 可移植方法 相关矩阵（深蓝 = 建议主移植）", fontsize=14, color=NAVY, pad=12, fontweight="bold")
    ax.tick_params(length=0)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            if val == 0:
                continue
            label = "强" if val >= 0.9 else "中"
            ax.text(j, i, label, ha="center", va="center", color="white" if val >= 0.9 else NAVY, fontsize=9, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, ticks=[0, 0.5, 1])
    cbar.set_ticklabels(["无", "中", "强"])
    fig.tight_layout()
    path = OUT / "fig-paper-method-matrix.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def figure_paper_provenance():
    """Each paper: what slice entered the Chimera stack."""
    rows = [
        ("HuggingGPT", "按能力选专家 + 子任务 I/O", "L3 / 方法C  RoleToolkitResolver", "原型"),
        ("Chameleon", "模块 consumes/produces", "L2  ToolSpec", "原型"),
        ("ToolLLM", "API 先检索再调用", "P1 后继裁剪 / 窗口风险", "方案"),
        ("ControlLLM", "参数依赖图上搜路径", "L2  ToolGraph.plan", "原型"),
        ("ToolNet", "有向图替代扁平列表", "L2  successors/allowed", "原型"),
        ("GTool", "按请求生成工具子图", "L2  角色过滤后的子图", "原型"),
        ("ToolChain*", "A* 代价剪异常路径", "P3 攻击日代价标签", "方案"),
        ("AppWorld", "多应用写同一份状态", "L0/L1  ArtifactBus+Apps", "原型"),
        ("TheAgentCompany", "Drive/Chat/Tickets 互联", "L1  应用选型", "原型"),
        ("OfficeBench", "必须能跨办公应用切换", "方法D  取消邮件硬分叉", "原型"),
        ("WorkArena", "企业工单工作流", "L1  Tickets 应用", "方案"),
        ("τ-bench", "有状态工具 + 领域政策", "L0 ACL / 方法G", "原型"),
        ("Generative Agents", "跨活动记忆可检索", "artifact_id 挂日摘要", "方案"),
        ("MetaGPT", "角色 SOP + 产物交接", "ROLE_HINTS / 周报进 Drive", "原型"),
        ("AWM", "从成功轨迹诱导配方", "WorkflowMemory", "原型"),
        ("TPTU-v2", "Retriever + Demo，不微调", "别名检索 / 流感示范链", "原型"),
    ]
    fig, ax = plt.subplots(figsize=(13.4, 9.2), dpi=160)
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 9.4)
    ax.axis("off")
    ax.set_title(
        "16 篇论文 → 最终 Chimera 方案：每篇只用其中切面，不是整篇搬入",
        fontsize=13,
        color=NAVY,
        pad=8,
        fontweight="bold",
    )
    headers = [(0.2, "论文"), (2.6, "抽取的机制切面"), (7.3, "落到最终构建的位置"), (11.2, "状态")]
    ax.add_patch(
        FancyBboxPatch((0.15, 8.55), 13.1, 0.55, boxstyle="round,pad=0.01,rounding_size=0.04",
                       facecolor=NAVY, edgecolor=NAVY, linewidth=0)
    )
    for x, text in headers:
        ax.text(x, 8.82, text, ha="left", va="center", fontsize=10, color="white")
    status_color = {"原型": TEAL, "方案": GOLD}
    y = 8.05
    for i, (paper, slice_, dest, status) in enumerate(rows):
        bg = LIGHT if i % 2 == 0 else "#FFFFFF"
        ax.add_patch(
            FancyBboxPatch((0.15, y - 0.12), 13.1, 0.48, boxstyle="round,pad=0.01,rounding_size=0.02",
                           facecolor=bg, edgecolor="#E8EEF5", linewidth=0.6)
        )
        ax.text(0.25, y + 0.12, paper, ha="left", va="center", fontsize=8.5, color=NAVY)
        ax.text(2.6, y + 0.12, slice_, ha="left", va="center", fontsize=8.5, color=GRAY)
        ax.text(7.3, y + 0.12, dest, ha="left", va="center", fontsize=8.5, color=NAVY)
        ax.add_patch(
            FancyBboxPatch((11.2, y - 0.02), 1.7, 0.28, boxstyle="round,pad=0.01,rounding_size=0.06",
                           facecolor=status_color[status], edgecolor=status_color[status], linewidth=0)
        )
        ax.text(12.05, y + 0.12, status, ha="center", va="center", fontsize=8, color="white")
        y -= 0.48
    ax.text(
        6.7,
        0.22,
        "「原型」= 已写入 src/tool_composition.py    「方案」= 已写入最终方法，待 P1–P3 接线    整篇论文的其余部分明确不搬",
        ha="center",
        fontsize=8.5,
        color=GRAY,
    )
    fig.tight_layout()
    path = OUT / "fig-paper-provenance.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def figure_flu_workflow():
    fig, ax = plt.subplots(figsize=(13.2, 5.8), dpi=160)
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 5.8)
    ax.axis("off")
    ax.set_title(
        "示例工作流：流感趋势分析（同一 Artifact Bus，跨工具而非孤立任务）",
        fontsize=13,
        color=NAVY,
        pad=10,
        fontweight="bold",
    )
    steps = [
        (0.35, "1 EHR\n导出病例", CORAL),
        (2.5, "2 Spreadsheet\n按周聚合", GOLD),
        (4.65, "3 Terminal\n画趋势图", TEAL),
        (6.8, "4 Drive\n写入共享盘", NAVY),
        (8.95, "5 Email\n附件发给主任", "#6C4AB6"),
        (11.1, "6 Chat\n通知值班组", "#2E8B57"),
    ]
    for x, text, color in steps:
        _box(ax, x, 2.35, 1.85, 1.5, text, color, color, 9)
    for i in range(len(steps) - 1):
        x1 = steps[i][0] + 1.85
        x2 = steps[i + 1][0]
        _arrow(ax, x1, 3.1, x2, 3.1, NAVY, lw=1.8)

    _box(
        ax,
        0.35,
        0.45,
        12.5,
        1.4,
        "Artifact Bus 上依次出现：ehr_extract.json → flu_weekly.csv → flu_trend.png → drive://epi/week-12/ → mail://chief@hospital\n"
        "现状 Chimera：步骤 1–4 被压成一次 OWL 闲聊式 tool dump，步骤 5 走另一条无附件邮件，步骤 6 不存在",
        LIGHT,
        NAVY,
        10,
        NAVY,
        weight="normal",
    )
    fig.tight_layout()
    path = OUT / "fig-flu-workflow.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def main():
    paths = [
        figure_current_callgraph(),
        figure_target_stack(),
        figure_paper_map(),
        figure_paper_provenance(),
        figure_flu_workflow(),
    ]
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()

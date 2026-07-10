#!/usr/bin/env python3
"""Parse Chimera OWL agent dialogue logs for the unified day timeline.

Used by scripts/view_day_timeline.py (not a standalone HTML generator).

Parses:
  - *_execution_solution_*.log  (User/Assistant round summaries)
  - *_executio_task_*.log       (LLM calls / tool calls / file writes)
"""

from __future__ import annotations

import ast
import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ENTRY_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) - (\w+) - (.*)$", re.M
)
MSG_DUMP_RE = re.compile(
    r"Model (.+?), index (\d+), processed these messages: (\[.*\])\s*$", re.S
)
ROUND_RE = re.compile(
    r"Round #(\d+) (user_response|assistant_response):\s*(.*)$", re.S
)
SEALED_RE = re.compile(r"^✓ Round (\d+) sealed")
SOLUTION_NAME_RE = re.compile(
    r"^(?P<member>.+)_week_(?P<week>\d+)_(?P<date>\w+)_execution_solution_(?P<task>\d+)\.log$"
)
TASK_NAME_RE = re.compile(
    r"^(?P<member>.+)_week_(?P<week>\d+)_(?P<date>\w+)_executio_task_(?P<task>\d+)\.log$"
)


@dataclass
class ChatBubble:
    role: str  # user | assistant | tool | system | meta | write | warn
    title: str
    body: str
    ts: str = ""
    collapsed: bool = False


@dataclass
class RoundBlock:
    round_id: int
    user: ChatBubble | None = None
    assistant: ChatBubble | None = None
    internals: list[ChatBubble] = field(default_factory=list)
    start_ts: str = ""
    end_ts: str = ""

    @property
    def tool_count(self) -> int:
        return sum(1 for b in self.internals if b.role in ("tool", "write"))

    @property
    def llm_count(self) -> int:
        return sum(1 for b in self.internals if b.role == "meta" and b.title.startswith("LLM call"))

    @property
    def warn_count(self) -> int:
        return sum(1 for b in self.internals if b.role == "warn")


@dataclass
class TaskView:
    member: str
    week: str
    date: str
    task_id: str
    solution_path: Path | None = None
    task_path: Path | None = None
    rounds: list[RoundBlock] = field(default_factory=list)

    @property
    def key(self) -> str:
        return f"{self.member}|{self.week}|{self.date}|{self.task_id}"

    @property
    def label(self) -> str:
        return f"{self.member} · week {self.week} {self.date} · task {self.task_id}"


def split_log_entries(text: str) -> list[tuple[str, str, str]]:
    matches = list(ENTRY_RE.finditer(text))
    entries: list[tuple[str, str, str]] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        msg = m.group(3) + text[start:end]
        entries.append((m.group(1), m.group(2), msg))
    return entries


def parse_solution_by_round(path: Path) -> dict[int, dict[str, ChatBubble]]:
    """Return {round_id: {'user': bubble, 'assistant': bubble}}."""
    text = path.read_text(encoding="utf-8", errors="replace")
    by_round: dict[int, dict[str, ChatBubble]] = {}
    for ts, _level, msg in split_log_entries(text):
        m = ROUND_RE.match(msg.strip())
        if not m:
            continue
        round_id = int(m.group(1))
        kind, body = m.group(2), m.group(3).strip()
        slot = by_round.setdefault(round_id, {})
        if kind == "user_response":
            slot["user"] = ChatBubble(
                role="user",
                title="User instruction",
                body=body or "(empty)",
                ts=ts,
            )
        else:
            if body.startswith("Solution:"):
                body = body[len("Solution:") :].lstrip()
            slot["assistant"] = ChatBubble(
                role="assistant",
                title="Assistant solution",
                body=body or "(empty)",
                ts=ts,
            )
    return by_round


def _msg_fingerprint(msg: dict[str, Any]) -> str:
    payload = {
        "role": msg.get("role"),
        "content": msg.get("content"),
        "tool_call_id": msg.get("tool_call_id"),
        "tool_calls": msg.get("tool_calls"),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)


def _detect_agent(messages: list[dict[str, Any]]) -> str:
    for msg in messages:
        if msg.get("role") != "system":
            continue
        content = str(msg.get("content") or "")
        if "RULES OF USER" in content:
            return "user-agent"
        if "RULES OF ASSISTANT" in content:
            return "assistant-agent"
    return "unknown"


def _format_tool_calls(tool_calls: Any) -> str:
    if not tool_calls:
        return ""
    parts: list[str] = []
    for tc in tool_calls:
        fn = (tc or {}).get("function") or {}
        name = fn.get("name", "unknown")
        args = fn.get("arguments", "")
        pretty = args
        if isinstance(args, str):
            try:
                pretty = json.dumps(json.loads(args), ensure_ascii=False, indent=2)
            except Exception:
                pretty = args
        elif isinstance(args, (dict, list)):
            pretty = json.dumps(args, ensure_ascii=False, indent=2)
        parts.append(f"🔧 {name}\n{pretty}")
    return "\n\n".join(parts)


def _format_message(msg: dict[str, Any], ts: str) -> ChatBubble:
    role = msg.get("role") or "unknown"
    content = msg.get("content")
    tool_calls = msg.get("tool_calls")
    tool_call_id = msg.get("tool_call_id")

    body_parts: list[str] = []
    if content:
        body_parts.append(str(content))
    if tool_calls:
        body_parts.append(_format_tool_calls(tool_calls))
    if tool_call_id and not content:
        body_parts.append(f"(tool_call_id: {tool_call_id})")

    body = "\n\n".join(body_parts).strip() or "(empty)"
    collapsed = role == "system"
    title_map = {
        "system": "System prompt",
        "user": "User message",
        "assistant": "Assistant message",
        "tool": "Tool result",
    }
    title = title_map.get(role, role)
    out_role = role
    if tool_calls:
        names = [
            ((tc or {}).get("function") or {}).get("name", "?") for tc in tool_calls
        ]
        title = f"Tool call · {', '.join(names)}"
        out_role = "tool"
    elif role == "tool":
        title = f"Tool result{f' ({tool_call_id})' if tool_call_id else ''}"

    return ChatBubble(
        role=out_role, title=title, body=body, ts=ts, collapsed=collapsed
    )


def parse_task_events(path: Path) -> list[ChatBubble]:
    text = path.read_text(encoding="utf-8", errors="replace")
    events: list[ChatBubble] = []
    seen: set[str] = set()

    for ts, _level, msg in split_log_entries(text):
        stripped = msg.strip()

        if stripped.startswith("Round #"):
            m = ROUND_RE.match(stripped)
            if not m:
                continue
            round_id, kind, body = m.group(1), m.group(2), m.group(3).strip()
            role = "user" if kind == "user_response" else "assistant"
            title = f"✓ Round {round_id} sealed · " + (
                "User instruction" if role == "user" else "Assistant solution"
            )
            if role == "assistant" and body.startswith("Solution:"):
                body = body[len("Solution:") :].lstrip()
            events.append(
                ChatBubble(
                    role="seal",
                    title=title,
                    body=body or "(empty)",
                    ts=ts,
                    collapsed=True,
                )
            )
            continue

        if "processed these messages:" in msg:
            m = MSG_DUMP_RE.search(msg)
            if not m:
                events.append(
                    ChatBubble(
                        role="warn",
                        title="Unparsed model dump",
                        body=msg[:500],
                        ts=ts,
                    )
                )
                continue
            model, index, raw = m.group(1), m.group(2), m.group(3)
            try:
                messages = ast.literal_eval(raw)
            except Exception as exc:
                events.append(
                    ChatBubble(
                        role="warn",
                        title="Failed to parse messages",
                        body=f"{exc}\n\n{raw[:800]}",
                        ts=ts,
                    )
                )
                continue

            agent = _detect_agent(messages)
            new_msgs = []
            for item in messages:
                fp = _msg_fingerprint(item)
                if fp in seen:
                    continue
                seen.add(fp)
                new_msgs.append(item)

            if not new_msgs:
                continue

            header = (
                f"LLM call · {model} · {agent} · +{len(new_msgs)} msg "
                f"(ctx={len(messages)}, idx={index})"
            )
            events.append(ChatBubble(role="meta", title=header, body="", ts=ts))
            for item in new_msgs:
                events.append(_format_message(item, ts))
            continue

        if stripped.startswith("Content successfully written to file:"):
            file_path = stripped.split("file:", 1)[-1].strip()
            events.append(
                ChatBubble(role="write", title="Wrote file", body=file_path, ts=ts)
            )
            continue

        if stripped.startswith("Skipping malformed"):
            events.append(
                ChatBubble(
                    role="warn", title="Malformed tool call", body=stripped, ts=ts
                )
            )
            continue

        preview = stripped[:160].replace("\n", " ")
        events.append(
            ChatBubble(
                role="meta",
                title=f"Log · {preview}",
                body=stripped,
                ts=ts,
                collapsed=True,
            )
        )

    return events


def build_rounds(
    solution_by_round: dict[int, dict[str, ChatBubble]],
    task_events: list[ChatBubble],
) -> list[RoundBlock]:
    """Group task internals under the Round they produced.

    Events before Round N's seal markers belong to Round N.
    Seal markers themselves are skipped (solution content is shown instead).
    """
    # Split task events into buckets keyed by upcoming seal round id
    buckets: dict[int, list[ChatBubble]] = {}
    current_bucket: list[ChatBubble] = []
    pending_round: int | None = None
    order: list[int] = []

    def flush(round_id: int) -> None:
        nonlocal current_bucket
        if round_id not in buckets:
            buckets[round_id] = []
            order.append(round_id)
        buckets[round_id].extend(current_bucket)
        current_bucket = []

    for ev in task_events:
        if ev.role == "seal":
            m = SEALED_RE.match(ev.title)
            if not m:
                continue
            rid = int(m.group(1))
            # First seal line for this round flushes accumulated internals into it
            if pending_round is None or pending_round != rid:
                flush(rid)
                pending_round = rid
            # skip seal body — shown via solution
            continue
        current_bucket.append(ev)

    # Trailing events after last seal → attach to last round if any, else round -1 (orphan)
    if current_bucket:
        if order:
            buckets[order[-1]].extend(current_bucket)
        else:
            buckets[-1] = current_bucket
            order.append(-1)

    # Ensure all solution rounds appear even if task log missing seals
    for rid in solution_by_round:
        if rid not in buckets:
            buckets[rid] = []
            order.append(rid)

    # Stable sort by round id; keep -1 (orphan/preamble-only) first if present
    unique_order = []
    seen = set()
    for rid in sorted(order, key=lambda x: (x < 0, x)):
        if rid not in seen:
            unique_order.append(rid)
            seen.add(rid)

    rounds: list[RoundBlock] = []
    for rid in unique_order:
        sol = solution_by_round.get(rid, {})
        internals = buckets.get(rid, [])
        # Drop system prompts from default noise? keep but collapsed already
        block = RoundBlock(
            round_id=rid,
            user=sol.get("user"),
            assistant=sol.get("assistant"),
            internals=internals,
        )
        stamps = [b.ts for b in internals if b.ts]
        if block.user and block.user.ts:
            stamps.append(block.user.ts)
        if block.assistant and block.assistant.ts:
            stamps.append(block.assistant.ts)
        if stamps:
            block.start_ts = min(stamps)
            block.end_ts = max(stamps)
        rounds.append(block)
    return rounds


def discover_tasks(logs_dir: Path) -> list[TaskView]:
    by_key: dict[str, TaskView] = {}
    solution_maps: dict[str, dict[int, dict[str, ChatBubble]]] = {}
    task_maps: dict[str, list[ChatBubble]] = {}

    for path in sorted(logs_dir.glob("*/*_execution_solution_*.log")):
        m = SOLUTION_NAME_RE.match(path.name)
        if not m:
            continue
        key = f"{m['member']}|{m['week']}|{m['date']}|{m['task']}"
        view = by_key.setdefault(
            key,
            TaskView(
                member=m["member"],
                week=m["week"],
                date=m["date"],
                task_id=m["task"],
            ),
        )
        view.solution_path = path
        solution_maps[key] = parse_solution_by_round(path)

    for path in sorted(logs_dir.glob("*/*_executio_task_*.log")):
        m = TASK_NAME_RE.match(path.name)
        if not m:
            continue
        key = f"{m['member']}|{m['week']}|{m['date']}|{m['task']}"
        view = by_key.setdefault(
            key,
            TaskView(
                member=m["member"],
                week=m["week"],
                date=m["date"],
                task_id=m["task"],
            ),
        )
        view.task_path = path
        task_maps[key] = parse_task_events(path)

    for key, view in by_key.items():
        view.rounds = build_rounds(
            solution_maps.get(key, {}),
            task_maps.get(key, []),
        )

    return sorted(
        by_key.values(),
        key=lambda t: (t.member, int(t.week), t.date, int(t.task_id)),
    )


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def _one_line(text: str, limit: int = 160) -> str:
    line = " ".join((text or "").split())
    if len(line) <= limit:
        return line
    return line[: limit - 1].rstrip() + "…"


def _agent_zh(agent: str) -> str:
    a = (agent or "").strip().lower()
    if "user" in a:
        return "规划端"
    if "assistant" in a:
        return "执行端"
    return agent or "未知"


def summarize_user(body: str) -> str:
    text = (body or "").strip()
    if not text:
        return "（空）"
    for raw in text.splitlines():
        line = raw.strip()
        if line.lower().startswith("instruction:"):
            return _one_line(line[len("Instruction:") :].strip() or line, 180)
    return _one_line(text, 180)


def summarize_assistant(body: str) -> str:
    text = (body or "").strip()
    if not text or text == "(empty)":
        return "（空 / 失败）"
    # Prefer first non-heading substantive paragraph
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    for p in paras:
        if p.startswith("#") or p.startswith("|") or p.startswith("---"):
            continue
        if p.startswith("**") and len(p) < 40:
            continue
        return _one_line(p, 200)
    return _one_line(text, 200)


def summarize_internals(internals: list[ChatBubble]) -> list[str]:
    """Short Chinese bullet lines describing what happened inside the round."""
    lines: list[str] = []
    for b in internals:
        if b.role == "meta" and b.title.startswith("LLM call"):
            # LLM call · deepseek-chat · assistant-agent · +2 msg ...
            parts = [p.strip() for p in b.title.split("·")]
            agent = _agent_zh(parts[2] if len(parts) > 2 else "agent")
            model = parts[1] if len(parts) > 1 else "model"
            lines.append(f"调用模型 · {model} · {agent}")
        elif b.role == "tool" and b.title.startswith("Tool call"):
            name = b.title.split("·", 1)[-1].strip()
            hint = ""
            if "filename" in b.body:
                m = re.search(r'"filename"\s*:\s*"([^"]+)"', b.body)
                if m:
                    hint = f" → {Path(m.group(1)).name}"
            lines.append(f"调用工具 · {name}{hint}")
        elif b.role == "write":
            name = Path(b.body.strip()).name if b.body.strip() else "文件"
            lines.append(f"写入文件 · {name}")
        elif b.role == "warn":
            lines.append(f"警告 · {_one_line(b.body, 80)}")
    return lines


def render_bubble(b: ChatBubble, compact: bool = False, open_default: bool = True) -> str:
    cls = f"bubble {esc(b.role)}"
    if compact:
        cls += " compact"
    collapsed = b.collapsed or not open_default
    open_attr = "" if collapsed else " open"
    body = esc(b.body)
    ts = f'<span class="ts">{esc(b.ts)}</span>' if b.ts else ""
    if not b.body.strip():
        return (
            f'<div class="{cls} header-only">'
            f'<div class="title">{esc(b.title)} {ts}</div></div>'
        )
    return f"""
<details class="{cls}"{open_attr}>
  <summary><span class="title">{esc(b.title)}</span> {ts}</summary>
  <pre>{body}</pre>
</details>
"""


def render_round(block: RoundBlock, open_first: bool) -> str:
    if block.round_id < 0:
        title = "未归属事件"
    else:
        title = f"第 {block.round_id} 轮"

    bits = []
    if block.llm_count:
        bits.append(f"{block.llm_count} 次模型调用")
    if block.tool_count:
        bits.append(f"{block.tool_count} 次工具")
    if block.warn_count:
        bits.append(f"{block.warn_count} 条警告")
    stats = " · ".join(bits) if bits else "无内部事件"
    time_span = ""
    if block.start_ts and block.end_ts:
        time_span = f"{esc(block.start_ts)} → {esc(block.end_ts)}"
    elif block.end_ts:
        time_span = esc(block.end_ts)

    user_sum = summarize_user(block.user.body) if block.user else "（缺失）"
    asst_sum = (
        summarize_assistant(block.assistant.body) if block.assistant else "（缺失）"
    )
    internal_lines = summarize_internals(block.internals)
    if internal_lines:
        internal_sum_html = (
            "<ol class='sum-list'>"
            + "".join(f"<li>{esc(line)}</li>" for line in internal_lines)
            + "</ol>"
        )
    else:
        internal_sum_html = '<p class="empty subtle">无内部事件</p>'

    # Detail column: keep full content, but collapse long dumps by default
    user_html = (
        render_bubble(block.user, open_default=True)
        if block.user
        else '<p class="empty">无用户指令</p>'
    )
    asst_html = (
        render_bubble(block.assistant, open_default=False)
        if block.assistant
        else '<p class="empty">无助手回复</p>'
    )
    if block.internals:
        # In detail pane, collapse system prompts; keep tool/write open-ish via role
        internals_html = "".join(
            render_bubble(
                b,
                compact=True,
                open_default=(b.role in ("tool", "write", "warn")),
            )
            for b in block.internals
        )
        internals_block = f'<div class="internals-feed flat">{internals_html}</div>'
    else:
        internals_block = '<p class="empty subtle">无模型/工具事件</p>'

    open_attr = " open"
    return f"""
<details class="round"{open_attr}>
  <summary class="round-summary">
    <span class="round-title">{esc(title)}</span>
    <span class="round-meta">{time_span}</span>
    <span class="round-stats">{esc(stats)}</span>
  </summary>
  <div class="round-body dual">
    <div class="col summary-col">
      <div class="col-head">摘要</div>
      <div class="sum-block">
        <div class="step-label">① 用户指令</div>
        <p class="sum-text user-sum">{esc(user_sum)}</p>
      </div>
      <div class="sum-block">
        <div class="step-label">② 内部执行</div>
        {internal_sum_html}
      </div>
      <div class="sum-block">
        <div class="step-label">③ 助手回复</div>
        <p class="sum-text asst-sum">{esc(asst_sum)}</p>
      </div>
    </div>
    <div class="col detail-col">
      <div class="col-head">详情</div>
      <div class="step-label">① 用户指令</div>
      {user_html}
      <div class="step-label">② 内部执行</div>
      {internals_block}
      <div class="step-label">③ 助手回复</div>
      {asst_html}
    </div>
  </div>
</details>
"""


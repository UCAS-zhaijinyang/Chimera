#!/usr/bin/env python3
"""Generate a unified Chimera day timeline + OWL execution drawer.

Works for both:
  - Phase-2 ``execution_logs``
  - Phase-3 ``attack_logs/<attid>_<company>/``

Swimlane timeline with click-to-open drawer (overview / execution / artifacts).
Attack rows (``(Attack){{member_id}}`` in final_schedule / email) are highlighted
with ATTACK badges, attacker column tags, and an attack-only filter.

Usage:
  python scripts/view_day_timeline.py
  python scripts/view_day_timeline.py --logs chimera_scenario_1/execution_logs
  python scripts/view_day_timeline.py --logs chimera_scenario_1/attack_logs/gen_attack_1_medical_institution --open
"""

from __future__ import annotations

import argparse
import ast
import csv
import html
import json
import re
import sys
import webbrowser
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Allow importing shared classifiers from src/ and agent-log parsers
_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))
sys.path.insert(0, str(_ROOT / "scripts"))
from activity_utils import (  # noqa: E402
    is_break_activity,
    is_email_reply_log,
    is_email_send_activity,
    is_loaf_activity,
)
import view_agent_logs as agentlog  # noqa: E402



MEMBER_PALETTE = [
    ("#1d4ed8", "#dbeafe"),
    ("#b45309", "#fef3c7"),
    ("#047857", "#d1fae5"),
    ("#5b21b6", "#ede9fe"),
    ("#9d174d", "#fce7f3"),
]

# Phase-3 logs prefix attacker rows as "(Attack){member_id}"
ATTACK_ID_RE = re.compile(r"^\(Attack\)\s*(.+)$")

RE_PREFIX = re.compile(
    r"^\s*(re|fw|fwd|回复|答复)\s*[:：]\s*", re.IGNORECASE
)


@dataclass
class Member:
    id: str
    name: str
    color: str
    soft: str
    is_attacker: bool = False


@dataclass
class Event:
    id: str
    member: str
    kind: str  # work | loaf | break | mail_send | mail_reply | login | logout
    time: str  # HH:MM:SS
    title: str
    summary: str
    detail: str = ""
    subject: str = ""
    mail_to: list[str] = field(default_factory=list)
    mail_from: str = ""
    thread_key: str = ""
    schedule_index: str = ""
    real_ts: str = ""
    has_owl: bool = False
    owl_key: str = ""
    artifact_names: list[str] = field(default_factory=list)
    is_attack: bool = False


@dataclass
class Arc:
    a: str  # event id
    b: str  # event id


def parse_member_id(raw: str) -> tuple[str, bool]:
    """Return (member_id, is_attack) from schedule/email id fields."""
    text = (raw or "").strip()
    m = ATTACK_ID_RE.match(text)
    if m:
        return m.group(1).strip(), True
    return text, False


def infer_attack_meta(logs_dir: Path) -> dict[str, Any]:
    """Best-effort attack scenario info from folder name + attacks/*.json."""
    name = logs_dir.name  # e.g. gen_attack_1_medical_institution
    attid = ""
    for prefix in ("gen_attack_", "multi_attack_"):
        if name.startswith(prefix):
            # gen_attack_1_medical_institution -> gen_attack_1
            parts = name.split("_")
            # gen_attack_1 or multi_attack_2
            if len(parts) >= 3 and parts[0] in ("gen", "multi") and parts[1] == "attack":
                attid = f"{parts[0]}_{parts[1]}_{parts[2]}"
            break
    info: dict[str, Any] = {"attid": attid, "folder": name}
    if not attid:
        return info
    attack_json = _ROOT / "attacks" / f"{attid}.json"
    if attack_json.is_file():
        try:
            data = json.loads(attack_json.read_text(encoding="utf-8"))
            info["scenario_title"] = data.get("scenario_title") or ""
            info["type"] = data.get("type") or ""
            info["what"] = data.get("what") or ""
            how = data.get("how") or []
            if isinstance(how, list):
                info["steps"] = [
                    {
                        "step": h.get("step"),
                        "description": h.get("description") or "",
                        "tactic": h.get("tactic") or "",
                    }
                    for h in how
                    if isinstance(h, dict)
                ]
        except Exception:
            pass
    return info


BODY_LIMIT = {
    "meta": 1200,
    "tool": 4000,
    "write": 500,
    "warn": 1500,
    "user": 6000,
    "assistant": 8000,
    "system": 800,
}


def _truncate_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n…(已截断)"


def _truncate_bubble(b: agentlog.ChatBubble | None) -> agentlog.ChatBubble | None:
    if b is None:
        return None
    limit = BODY_LIMIT.get(b.role, 4000)
    body = _truncate_text(b.body or "", limit)
    return agentlog.ChatBubble(
        role=b.role,
        title=b.title,
        body=body,
        ts=b.ts,
        collapsed=b.collapsed or b.role in ("meta", "system", "assistant"),
    )


def _truncate_round(block: agentlog.RoundBlock) -> agentlog.RoundBlock:
    internals = []
    for b in block.internals:
        # Drop huge raw LLM dumps from the modal; keep summary via summarize_internals
        if b.role == "meta" and "LLM call" in (b.title or ""):
            internals.append(
                agentlog.ChatBubble(
                    role="meta",
                    title=b.title,
                    body=_truncate_text(b.body or "", 600),
                    ts=b.ts,
                    collapsed=True,
                )
            )
        else:
            internals.append(_truncate_bubble(b))  # type: ignore[arg-type]
    return agentlog.RoundBlock(
        round_id=block.round_id,
        user=_truncate_bubble(block.user),
        assistant=_truncate_bubble(block.assistant),
        internals=internals,
        start_ts=block.start_ts,
        end_ts=block.end_ts,
    )


def collect_artifacts(block: agentlog.RoundBlock) -> list[str]:
    names: list[str] = []
    for b in block.internals:
        if b.role == "write" and b.body.strip():
            names.append(Path(b.body.strip()).name)
        elif b.role == "tool" and "filename" in (b.body or ""):
            m = re.search(r'"filename"\s*:\s*"([^"]+)"', b.body)
            if m:
                names.append(Path(m.group(1)).name)
    # unique preserve order
    seen: set[str] = set()
    out: list[str] = []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def render_owl_execution_html(task: agentlog.TaskView) -> tuple[str, list[str]]:
    """Return (html, artifact file names) for an OWL task."""
    artifacts: list[str] = []
    parts: list[str] = []
    rounds = [_truncate_round(r) for r in task.rounds]
    for i, block in enumerate(rounds):
        artifacts.extend(collect_artifacts(block))
        parts.append(agentlog.render_round(block, open_first=(i == 0)))
    if not parts:
        parts.append('<p class="empty">未找到对话轮次</p>')
    # unique artifacts
    seen: set[str] = set()
    uniq: list[str] = []
    for n in artifacts:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    paths = (
        f'<div class="owl-paths">'
        f"<div>solution: {esc(str(task.solution_path.name) if task.solution_path else '—')}</div>"
        f"<div>task: {esc(str(task.task_path.name) if task.task_path else '—')}</div>"
        f"</div>"
    )
    html_body = paths + '<div class="owl-feed">' + "".join(parts) + "</div>"
    return html_body, uniq


def list_temp_files(logs_dir: Path, member_id: str) -> list[dict[str, str]]:
    temp = logs_dir / f"{member_id}_temp"
    if not temp.is_dir():
        return []
    files: list[dict[str, str]] = []
    for p in sorted(temp.rglob("*")):
        if not p.is_file():
            continue
        if p.name.endswith(".bak") or ".bak." in p.name:
            continue
        rel = str(p.relative_to(temp))
        try:
            size = p.stat().st_size
        except OSError:
            size = 0
        preview = ""
        if size <= 80_000 and p.suffix.lower() in {
            ".md",
            ".txt",
            ".py",
            ".json",
            ".csv",
            ".jsonc",
        }:
            try:
                preview = _truncate_text(
                    p.read_text(encoding="utf-8", errors="replace"), 4000
                )
            except OSError:
                preview = ""
        files.append(
            {
                "name": rel,
                "size": str(size),
                "preview": preview,
            }
        )
    return files


def esc(text: str) -> str:
    return html.escape(str(text or ""), quote=True)


def one_line(text: str, limit: int = 72) -> str:
    line = " ".join((text or "").replace("\\n", " ").split())
    if len(line) <= limit:
        return line
    return line[: limit - 1].rstrip() + "…"


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    """Read a CSV with stripped headers/values (email.csv may have padded names)."""
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            raw_headers = next(reader)
        except StopIteration:
            return []
        headers = [(h or "").strip() for h in raw_headers]
        # Drop empty trailing header names
        while headers and not headers[-1]:
            headers.pop()
        rows: list[dict[str, str]] = []
        for parts in reader:
            if not parts or all(not (p or "").strip() for p in parts):
                continue
            if len(parts) < len(headers):
                parts = parts + [""] * (len(headers) - len(parts))
            elif len(parts) > len(headers):
                parts = parts[: len(headers) - 1] + [
                    ",".join(parts[len(headers) - 1 :])
                ]
            row = {
                headers[i]: (parts[i] or "").strip() for i in range(len(headers))
            }
            rows.append(row)
    return rows


def parse_recipients(raw: str) -> list[str]:
    text = (raw or "").strip()
    if not text or text == "[]":
        return []
    if text.startswith("["):
        try:
            val = ast.literal_eval(text)
            if isinstance(val, list):
                return [str(x).strip() for x in val if str(x).strip()]
        except Exception:
            pass
    return [p.strip() for p in text.split(",") if p.strip()]


def normalize_subject(subject: str) -> str:
    text = (subject or "").strip()
    while True:
        nxt = RE_PREFIX.sub("", text).strip()
        if nxt == text:
            break
        text = nxt
    return text.casefold()


def clean_email_content(raw: str) -> str:
    text = (raw or "").strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        text = text[1:-1]
    return (
        text.replace("\\n", "\n")
        .replace("\\r", "")
        .replace('\\"', '"')
        .strip()
    )


def unwrap_quotes(raw: str) -> str:
    text = (raw or "").strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    return text


def emails_related(a: Event, b: Event) -> bool:
    """True if two emails are a plausible conversation pair (to/from overlap)."""
    a_parties = {a.mail_from, *a.mail_to}
    b_parties = {b.mail_from, *b.mail_to}
    # Direct: b replies to a's sender, or a was addressed to b's sender
    if a.mail_from in b.mail_to or b.mail_from in a.mail_to:
        return True
    # CC / multi-party: shared participants beyond empty
    return bool(a_parties & b_parties) and a.mail_from != b.mail_from


def classify_schedule_activity(activity: str) -> str | None:
    """Classify a final_schedule.csv activity for the swimlane viewer.

    Returns:
        "work" | "loaf" | "break" | None

    ``None`` means the row is an email-only schedule marker (reply log or
    explicit send). Those are shown from ``email.csv`` instead, so we do not
    double-count. Mentions like ``Coordinate with @da-1`` stay as **work**.
    """
    a = activity or ""
    if is_break_activity(a):
        return "break"
    if is_loaf_activity(a):
        return "loaf"
    if is_email_reply_log(a):
        return None
    if is_email_send_activity(a):
        return None
    return "work"


def load_members(schedule_rows: list[dict[str, str]]) -> list[Member]:
    order: list[str] = []
    names: dict[str, str] = {}
    attackers: set[str] = set()
    for row in schedule_rows:
        mid, is_attack = parse_member_id(row.get("id") or "")
        if not mid:
            continue
        if is_attack:
            attackers.add(mid)
        if mid not in names:
            order.append(mid)
            names[mid] = row.get("name") or mid
    members: list[Member] = []
    for i, mid in enumerate(order):
        color, soft = MEMBER_PALETTE[i % len(MEMBER_PALETTE)]
        members.append(
            Member(
                id=mid,
                name=names[mid],
                color=color,
                soft=soft,
                is_attacker=mid in attackers,
            )
        )
    return members


def build_event_details(
    logs_dir: Path, events: list[Event]
) -> dict[str, dict[str, Any]]:
    """Attach OWL logs / mail bodies / artifacts to each timeline event."""
    owl_tasks = agentlog.discover_tasks(logs_dir)
    owl_index: dict[tuple[str, str], agentlog.TaskView] = {
        (t.member, t.task_id): t for t in owl_tasks
    }
    temp_cache: dict[str, list[dict[str, str]]] = {}
    details: dict[str, dict[str, Any]] = {}

    for ev in events:
        kind_label = {
            "work": "工作任务",
            "loaf": "摸鱼任务",
            "break": "休息",
            "mail_send": "发信",
            "mail_reply": "回信",
            "login": "登录",
            "logout": "登出",
        }.get(ev.kind, ev.kind)

        overview_bits = [
            f"成员: {ev.member}",
            f"类型: {kind_label}",
            f"模拟时间: {ev.time or '—'}",
        ]
        if ev.is_attack:
            overview_bits.insert(
                0, "⚠ 标记为攻击行为（日志 id 含 (Attack) 前缀）"
            )
        if ev.real_ts:
            overview_bits.append(f"真实时间: {ev.real_ts}")
        if ev.schedule_index:
            overview_bits.append(f"日程 index / task id: {ev.schedule_index}")
        if ev.subject:
            overview_bits.append(f"主题: {ev.subject}")
        if ev.mail_to:
            overview_bits.append(f"收件人: {', '.join(ev.mail_to)}")

        artifacts: list[dict[str, str]] = []
        execution_html = ""
        has_execution = False

        if ev.kind in ("work", "loaf") and ev.schedule_index:
            task = owl_index.get((ev.member, ev.schedule_index))
            if task is not None:
                ev.has_owl = True
                ev.owl_key = task.key
                execution_html, art_names = render_owl_execution_html(task)
                ev.artifact_names = art_names
                has_execution = True
                overview_bits.append(
                    f"OWL 轮次: {len(task.rounds)} · "
                    f"solution={task.solution_path.name if task.solution_path else '—'} · "
                    f"task={task.task_path.name if task.task_path else '—'}"
                )
                if ev.member not in temp_cache:
                    temp_cache[ev.member] = list_temp_files(logs_dir, ev.member)
                name_set = {Path(n).name for n in art_names}
                for f in temp_cache[ev.member]:
                    if Path(f["name"]).name in name_set:
                        artifacts.append(f)
                # If writes referenced paths not under temp listing, still list names
                listed = {Path(a["name"]).name for a in artifacts}
                for n in art_names:
                    if n not in listed:
                        artifacts.append({"name": n, "size": "", "preview": ""})
            else:
                execution_html = (
                    '<p class="empty">未找到对应 OWL 执行日志'
                    f"（期望 {esc(ev.member)} …_executio_task_{esc(ev.schedule_index)}.log）</p>"
                )
                has_execution = True
                overview_bits.append("OWL: 无匹配日志")
        elif ev.kind in ("mail_send", "mail_reply"):
            execution_html = (
                '<div class="mail-panel">'
                f'<pre class="mail-body">{esc(ev.detail)}</pre>'
                "</div>"
            )
            has_execution = True
            overview_bits.append("邮件正文来自 email.csv（无 OWL 多轮对话）")
        elif ev.kind in ("login", "logout"):
            execution_html = (
                f'<pre class="plain-body">{esc(ev.detail or ev.summary)}</pre>'
            )
            has_execution = True
            overview_bits.append("来自 logon.csv（会话登录/登出记录）")
        else:
            execution_html = (
                f'<pre class="plain-body">{esc(ev.detail or ev.summary or "（无详情）")}</pre>'
            )
            has_execution = True
            overview_bits.append("休息/非 OWL 活动，无工具调用链")

        overview_html = (
            (
                '<div class="attack-banner">'
                "<strong>ATTACK</strong>"
                " · 此任务为注入的攻击行为，请与同日正常任务对照查看"
                "</div>"
                if ev.is_attack
                else ""
            )
            + f'<p class="ov-title">{esc(ev.summary or ev.title)}</p>'
            "<ul class='ov-list'>"
            + "".join(f"<li>{esc(b)}</li>" for b in overview_bits)
            + "</ul>"
        )

        if artifacts:
            art_html_parts = []
            for a in artifacts:
                size_bit = f" · {a['size']} B" if a.get("size") else ""
                preview = a.get("preview") or ""
                if preview:
                    art_html_parts.append(
                        f'<details class="artifact"><summary>{esc(a["name"])}{esc(size_bit)}</summary>'
                        f"<pre>{esc(preview)}</pre></details>"
                    )
                else:
                    art_html_parts.append(
                        f'<div class="artifact header-only">{esc(a["name"])}{esc(size_bit)}</div>'
                    )
            artifacts_html = "".join(art_html_parts)
        else:
            artifacts_html = (
                '<p class="empty subtle">本任务无写入产物'
                + ("（或产物未落在成员 temp 目录）" if ev.has_owl else "")
                + "</p>"
            )

        details[ev.id] = {
            "title": ("⚠ 攻击 · " if ev.is_attack else "") + ev.title,
            "meta": " · ".join(
                x
                for x in [
                    ev.member,
                    ev.time,
                    "ATTACK" if ev.is_attack else "",
                    kind_label,
                    f"task {ev.schedule_index}" if ev.schedule_index else "",
                ]
                if x
            ),
            "kind": ev.kind,
            "has_owl": ev.has_owl,
            "is_attack": ev.is_attack,
            "overview_html": overview_html,
            "execution_html": execution_html if has_execution else "",
            "artifacts_html": artifacts_html,
            "artifact_count": len(artifacts),
            "round_hint": (
                f"{len(owl_index[(ev.member, ev.schedule_index)].rounds)} 轮"
                if ev.has_owl and ev.schedule_index
                and (ev.member, ev.schedule_index) in owl_index
                else ""
            ),
        }
    return details


def load_day_data(
    logs_dir: Path,
) -> tuple[list[Member], list[Event], list[Arc], dict[str, Any], dict[str, dict[str, Any]]]:
    schedule_path = logs_dir / "final_schedule.csv"
    email_path = logs_dir / "email.csv"
    logon_path = logs_dir / "logon.csv"
    if not schedule_path.exists():
        raise FileNotFoundError(f"Missing {schedule_path}")

    schedule_rows = read_csv_dicts(schedule_path)
    email_rows = read_csv_dicts(email_path) if email_path.exists() else []
    logon_rows = read_csv_dicts(logon_path) if logon_path.exists() else []

    members = load_members(schedule_rows)
    # Also discover members who only appear in logon/email
    known = {m.id for m in members}
    for row in logon_rows + email_rows:
        raw = row.get("id") or row.get("email_from") or ""
        mid, is_attack = parse_member_id(raw)
        if mid and mid not in known:
            color, soft = MEMBER_PALETTE[len(members) % len(MEMBER_PALETTE)]
            members.append(
                Member(
                    id=mid,
                    name=row.get("name") or mid,
                    color=color,
                    soft=soft,
                    is_attacker=is_attack,
                )
            )
            known.add(mid)
        elif mid and is_attack:
            for m in members:
                if m.id == mid:
                    m.is_attacker = True

    member_ids = {m.id for m in members}
    events: list[Event] = []
    eid = 0

    def next_id(prefix: str) -> str:
        nonlocal eid
        eid += 1
        return f"{prefix}-{eid}"

    # Schedule: work / loaf / break only (email markers come from email.csv)
    for row in schedule_rows:
        mid, is_attack = parse_member_id(row.get("id") or "")
        if not mid:
            continue
        activity = unwrap_quotes(row.get("activity") or "")
        kind = classify_schedule_activity(activity)
        if kind is None:
            continue
        title = {
            "work": "工作",
            "loaf": "摸鱼",
            "break": "休息",
        }[kind]
        if is_attack:
            title = f"攻击 · {title}"
        events.append(
            Event(
                id=next_id("s"),
                member=mid,
                kind=kind,
                time=row.get("sim_timestamp") or "",
                title=title,
                summary=one_line(activity, 80),
                detail=activity,
                schedule_index=row.get("index") or "",
                real_ts=row.get("real_timestamp") or "",
                is_attack=is_attack,
            )
        )

    # ---- logon.csv: login / logout session events ----
    logon_events: list[Event] = []
    for row in logon_rows:
        mid, is_attack = parse_member_id(row.get("id") or "")
        if not mid or mid not in member_ids:
            continue
        status = (row.get("status") or "").strip().lower()
        if status not in ("login", "logout"):
            continue
        kind = status
        title = "登录" if kind == "login" else "登出"
        if is_attack:
            title = f"攻击 · {title}"
        name = (row.get("name") or "").strip()
        container = (row.get("container_id") or "").strip()
        detail = (
            f"status: {status}\n"
            f"member: {mid}\n"
            f"name: {name or '—'}\n"
            f"container_id: {container or '—'}\n"
            f"sim_timestamp: {(row.get('sim_timestamp') or '').strip()}\n"
            f"real_timestamp: {(row.get('real_timestamp') or '').strip()}"
        )
        ev = Event(
            id=next_id("l"),
            member=mid,
            kind=kind,
            time=(row.get("sim_timestamp") or "").strip(),
            title=title,
            summary=f"{name or mid} · {status}",
            detail=detail,
            real_ts=(row.get("real_timestamp") or "").strip(),
            is_attack=is_attack,
        )
        logon_events.append(ev)
        events.append(ev)

    # ---- email.csv is the sole source for mail cards & arcs ----
    mail_events: list[Event] = []
    for row in email_rows:
        sender_raw = (row.get("email_from") or "").strip()
        sender, is_attack = parse_member_id(sender_raw)
        if not sender or sender not in member_ids:
            continue
        to_list = parse_recipients(row.get("email_to") or "")
        cc_list = parse_recipients(row.get("email_cc") or "")
        recipients = [r for r in (to_list + cc_list) if r]
        subject = (row.get("subject") or "").strip()
        content = clean_email_content(row.get("content") or "")
        is_reply = bool(RE_PREFIX.match(subject))
        kind = "mail_reply" if is_reply else "mail_send"
        verb = "回信" if is_reply else "发信"
        if is_attack:
            verb = f"攻击 · {verb}"
        to_label = ", ".join(recipients) if recipients else "?"
        detail = (
            f"From: {sender}\n"
            f"To: {', '.join(to_list) if to_list else '?'}\n"
            f"Cc: {', '.join(cc_list) if cc_list else '—'}\n"
            f"Subject: {subject}\n\n"
            f"{content}"
        )
        ev = Event(
            id=next_id("m"),
            member=sender,
            kind=kind,
            time=(row.get("sim_timestamp") or "").strip(),
            title=f"{verb} → {to_label}",
            summary=one_line(subject, 64),
            detail=detail,
            subject=subject,
            mail_to=recipients,
            mail_from=sender,
            thread_key=normalize_subject(subject)
            or f"solo:{sender}:{row.get('sim_timestamp')}",
            real_ts=(row.get("real_timestamp") or "").strip(),
            is_attack=is_attack,
        )
        mail_events.append(ev)
        events.append(ev)

    # Directed arcs from email.csv: earlier → later along each thread
    by_thread: dict[str, list[Event]] = defaultdict(list)
    for ev in mail_events:
        by_thread[ev.thread_key].append(ev)

    arcs: list[Arc] = []
    seen_pairs: set[tuple[str, str]] = set()
    for thread_events in by_thread.values():
        ordered = sorted(thread_events, key=lambda e: (e.time, e.real_ts, e.id))
        for i, cur in enumerate(ordered):
            for prev in reversed(ordered[:i]):
                if prev.member == cur.member:
                    continue
                if not emails_related(prev, cur):
                    continue
                pair = (prev.id, cur.id)
                if pair in seen_pairs:
                    break
                seen_pairs.add(pair)
                arcs.append(Arc(a=prev.id, b=cur.id))
                break

    events.sort(key=lambda e: (e.time, e.member, e.id))
    details = build_event_details(logs_dir, events)
    owl_linked = sum(1 for e in events if e.has_owl)
    attack_events = [e for e in events if e.is_attack]
    attackers = sorted({m.id for m in members if m.is_attacker})
    attack_info = infer_attack_meta(logs_dir)

    meta = {
        "schedule_count": len(schedule_rows),
        "email_count": len(email_rows),
        "logon_count": len(logon_events),
        "mail_cards": len(mail_events),
        "event_count": len(events),
        "arc_count": len(arcs),
        "owl_linked": owl_linked,
        "attack_count": len(attack_events),
        "attackers": attackers,
        "is_attack_run": bool(attack_events) or "attack_logs" in str(logs_dir),
        "attack_info": attack_info,
        "members": [m.id for m in members],
    }
    return members, events, arcs, meta, details


def time_rows(events: list[Event]) -> list[str]:
    seen: list[str] = []
    for ev in events:
        if ev.time and ev.time not in seen:
            seen.append(ev.time)
    return seen


def render_html(
    members: list[Member],
    events: list[Event],
    arcs: list[Arc],
    meta: dict[str, Any],
    details: dict[str, dict[str, Any]],
    title: str,
) -> str:
    n = max(len(members), 1)
    grid = f"72px repeat({n}, minmax(120px, 1fr))"

    member_css = "\n".join(
        f"  .lane-{esc(m.id)} {{ --lane: {m.color}; --lane-soft: {m.soft}; }}"
        for m in members
    )

    by_time: dict[str, dict[str, list[Event]]] = defaultdict(lambda: defaultdict(list))
    for ev in events:
        by_time[ev.time][ev.member].append(ev)
    times = time_rows(events)

    head_cells = ['<div class="t">时间</div>']
    for m in members:
        first = (m.name or "").split()[0] if m.name else m.id
        attacker_mark = (
            '<span class="attacker-tag">攻击者</span>' if m.is_attacker else ""
        )
        head_cells.append(
            f'<div class="lane-{esc(m.id)} head-cell{" attacker" if m.is_attacker else ""}">'
            f'<span class="mid">{esc(m.id)}</span>'
            f"{attacker_mark}"
            f'<span class="name">{esc(first)}</span></div>'
        )

    chips = ['<button class="chip on" data-filter="all" type="button">全部</button>']
    if meta.get("attack_count"):
        chips.append(
            '<button class="chip chip-attack" data-filter="attack" type="button">'
            f'仅攻击 ({meta["attack_count"]})</button>'
        )
    for m in members:
        label = f"{m.id} ★" if m.is_attacker else m.id
        chips.append(
            f'<button class="chip" data-filter="{esc(m.id)}" type="button">'
            f"{esc(label)}</button>"
        )

    rows_html: list[str] = []
    for t in times:
        cells = [f'<div class="time">{esc(t[:5] if len(t) >= 5 else t)}</div>']
        for m in members:
            bucket = by_time[t].get(m.id, [])
            if not bucket:
                cells.append("<div></div>")
                continue
            cards = []
            for ev in bucket:
                cls = {
                    "work": "work",
                    "loaf": "loaf",
                    "break": "break",
                    "mail_send": "mail-out",
                    "mail_reply": "mail-in",
                    "login": "login",
                    "logout": "logout",
                }.get(ev.kind, "work")
                if ev.is_attack:
                    cls += " attack"
                d = details.get(ev.id, {})
                badges = []
                if ev.is_attack:
                    badges.append(
                        '<span class="badge attack" title="攻击行为">ATTACK</span>'
                    )
                if ev.has_owl:
                    badges.append(
                        '<span class="badge owl" title="含 OWL 执行日志">OWL</span>'
                    )
                if d.get("artifact_count"):
                    badges.append(
                        f'<span class="badge art" title="产物">{int(d["artifact_count"])}</span>'
                    )
                badge_html = (
                    f'<div class="badges">{"".join(badges)}</div>' if badges else ""
                )
                cards.append(
                    f'<button type="button" class="card {cls}" id="{esc(ev.id)}" '
                    f'data-member="{esc(ev.member)}" data-kind="{esc(ev.kind)}" '
                    f'data-title="{esc(ev.title)}" data-summary="{esc(ev.summary)}" '
                    f'data-time="{esc(ev.time)}" data-has-owl="{1 if ev.has_owl else 0}" '
                    f'data-attack="{1 if ev.is_attack else 0}">'
                    f'<div class="k">{esc(ev.title)}</div>'
                    f'<div class="s">{esc(ev.summary)}</div>'
                    f"{badge_html}"
                    f"</button>"
                )
            cells.append(
                f'<div class="stack lane-{esc(m.id)}">{"".join(cards)}</div>'
            )
        rows_html.append(
            f'<div class="row" data-time="{esc(t)}">{"".join(cells)}</div>'
        )

    arcs_json = json.dumps([{"a": a.a, "b": a.b} for a in arcs], ensure_ascii=False)
    details_json = json.dumps(details, ensure_ascii=False)

    attack_info = meta.get("attack_info") or {}
    attack_callout = ""
    if meta.get("is_attack_run"):
        attackers = meta.get("attackers") or []
        steps = attack_info.get("steps") or []
        step_bits = ""
        if steps:
            step_bits = (
                "<br/>步骤："
                + " → ".join(
                    f'{esc(str(s.get("step") or ""))}. {esc(one_line(str(s.get("description") or ""), 48))}'
                    for s in steps[:6]
                )
            )
        attack_callout = (
            f'<div class="attack-callout">'
            f"<strong>ATTACK DAY</strong> · "
            f'{esc(attack_info.get("attid") or attack_info.get("folder") or "attack")}'
            f' · {esc(attack_info.get("scenario_title") or attack_info.get("type") or "攻击仿真")}'
            f' · 攻击者: {esc(", ".join(attackers) if attackers else "—")}'
            f' · 攻击事件 {meta.get("attack_count", 0)} 个'
            f"{step_bits}"
            f'<br/>红色 <span class="badge attack">ATTACK</span> 卡片为注入攻击行为；可用「仅攻击」筛选。'
            f"</div>"
        )

    sub_extra = ""
    if meta.get("attack_count"):
        sub_extra = (
            f' · <span style="color:#7f1d1d;font-weight:700">'
            f'{meta["attack_count"]} 个攻击事件</span>'
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)}</title>
<style>
  :root {{
    --bg: #f4f1ea;
    --ink: #1c1917;
    --muted: #78716c;
    --card: #fffcf7;
    --line: #e7e0d4;
    --work: #dbeafe;
    --work-ink: #1e40af;
    --mail-out: #fef3c7;
    --mail-out-ink: #92400e;
    --mail-in: #fce7f8;
    --mail-in-ink: #9d174d;
    --loaf: #ecfccb;
    --loaf-ink: #3f6212;
    --break: #e7e5e4;
    --break-ink: #44403c;
    --login: #e0e7ff;
    --login-ink: #3730a3;
    --logout: #f1f5f9;
    --logout-ink: #475569;
    --arc: #c2410c;
    --attack: #7f1d1d;
    --attack-bg: #fee2e2;
    --attack-edge: #dc2626;
    --accent: #2f5d50;
    --user: #e8f0ea;
    --assistant: #eef2f7;
    --tool: #f7efe3;
    --system: #f0eee9;
    --meta: #f7f5f0;
    --write: #e7f3ea;
    --warn: #f8e8e4;
    --round: #fbf8f2;
    --panel: #fffdf8;
  }}
{member_css}
  * {{ box-sizing: border-box; }}
  html {{ height: 100%; }}
  body {{
    margin: 0;
    min-height: 100%;
    font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
    background:
      radial-gradient(1200px 500px at 10% -10%, #efe6d6 0%, transparent 55%),
      radial-gradient(900px 400px at 100% 0%, #e8efe6 0%, transparent 50%),
      var(--bg);
    color: var(--ink);
    padding: 24px 16px 48px;
  }}
  html.drawer-open,
  body.drawer-open {{
    overflow: hidden;
    overscroll-behavior: none;
  }}
  body.drawer-open {{
    position: fixed;
    left: 0;
    right: 0;
    width: 100%;
  }}
  .wrap {{ max-width: 1280px; margin: 0 auto; }}
  h1 {{ font-size: 26px; margin: 0 0 4px; letter-spacing: -0.02em; }}
  .sub {{ color: var(--muted); margin: 0 0 16px; font-size: 14px; }}
  .panel {{
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
  }}
  .toolbar {{
    display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
    padding: 12px 16px; border-bottom: 1px solid var(--line);
    background: #faf7f1; font-family: ui-sans-serif, system-ui, sans-serif; font-size: 12px;
  }}
  .chip {{
    border-radius: 999px; padding: 5px 11px; border: 1px solid var(--line);
    background: #fff; cursor: pointer; font: inherit; color: inherit;
  }}
  .chip.on {{ background: #1c1917; color: #fff; border-color: #1c1917; }}
  .chip.chip-attack.on {{ background: var(--attack); border-color: var(--attack); }}
  .legend {{ margin-left: auto; color: var(--muted); }}
  .attack-callout {{
    margin: 0 0 14px; padding: 10px 14px; border-radius: 10px;
    border: 1px solid #fecaca; background: #fef2f2; color: #7f1d1d;
    font-family: ui-sans-serif, system-ui, sans-serif; font-size: 13px; line-height: 1.45;
  }}
  .attack-callout strong {{ letter-spacing: .04em; }}
  .head-cell.attacker {{
    box-shadow: inset 0 -3px 0 var(--attack-edge);
    background: #fff5f5;
  }}
  .attacker-tag {{
    display: inline-block; margin: 2px 0; padding: 1px 6px; border-radius: 4px;
    background: var(--attack); color: #fff; font-size: 9px; font-weight: 700;
    letter-spacing: .04em;
  }}
  .lanes-head, .row {{
    display: grid;
    grid-template-columns: {grid};
    gap: 8px;
    padding: 8px 12px;
    font-family: ui-sans-serif, system-ui, sans-serif;
  }}
  .lanes-head {{
    border-bottom: 1px solid var(--line);
    background: #fff;
    position: sticky; top: 0; z-index: 6;
    font-size: 12px; text-align: center; font-weight: 700;
  }}
  .lanes-head .t {{ text-align: left; color: var(--muted); font-weight: 500; }}
  .head-cell .mid {{ display: block; color: var(--lane); }}
  .head-cell .name {{ display: block; font-size: 10px; font-weight: 500; color: var(--muted); }}
  .body {{ position: relative; padding-bottom: 8px; min-height: 120px; }}
  .time {{ font-size: 11px; color: var(--muted); padding-top: 10px; font-variant-numeric: tabular-nums; }}
  .stack {{ display: flex; flex-direction: column; gap: 6px; }}
  .card {{
    display: block; width: 100%; text-align: left;
    border-radius: 10px; padding: 8px 9px; border: 1px solid transparent;
    font-size: 12px; line-height: 1.35; background: #f5f5f4;
    cursor: pointer; font-family: inherit; color: inherit;
  }}
  .card:hover {{ filter: brightness(0.98); }}
  .card.active {{ outline: 2px solid #1c1917; outline-offset: 1px; }}
  .card.dim {{ opacity: 0.22; }}
  .card .k {{ font-size: 10px; font-weight: 700; letter-spacing: .02em; margin-bottom: 2px; }}
  .card .s {{ color: inherit; opacity: 0.92; }}
  .badges {{ display: flex; gap: 4px; margin-top: 5px; flex-wrap: wrap; }}
  .badge {{
    font-size: 9px; font-weight: 700; letter-spacing: .04em;
    padding: 1px 5px; border-radius: 4px; background: rgba(0,0,0,.08);
  }}
  .badge.owl {{ background: #2f5d50; color: #fff; }}
  .badge.art {{ background: #1d4ed8; color: #fff; }}
  .badge.attack {{
    background: var(--attack); color: #fff;
    box-shadow: 0 0 0 1px rgba(127,29,29,.25);
  }}
  .card.work {{ background: var(--work); border-color: #93c5fd; color: var(--work-ink); }}
  .card.mail-out {{
    background: var(--mail-out); border: 2px solid #f59e0b; color: var(--mail-out-ink);
    box-shadow: 0 0 0 3px rgba(245,158,11,.10);
  }}
  .card.mail-in {{
    background: var(--mail-in); border: 2px solid #ec4899; color: var(--mail-in-ink);
    box-shadow: 0 0 0 3px rgba(236,72,153,.08);
  }}
  .card.loaf {{ background: var(--loaf); border-color: #bef264; color: var(--loaf-ink); }}
  .card.break {{ background: var(--break); border-color: #d6d3d1; color: var(--break-ink); }}
  .card.login {{
    background: var(--login); border: 1px dashed #818cf8; color: var(--login-ink);
  }}
  .card.logout {{
    background: var(--logout); border: 1px dashed #94a3b8; color: var(--logout-ink);
  }}
  .card.attack {{
    background: var(--attack-bg) !important;
    border: 2px solid var(--attack-edge) !important;
    color: var(--attack) !important;
    box-shadow: 0 0 0 3px rgba(220,38,38,.14), 0 8px 18px rgba(127,29,29,.12);
    font-weight: 600;
  }}
  .card.attack .k {{ color: var(--attack); }}
  .attack-banner {{
    margin: 0 0 12px; padding: 10px 12px; border-radius: 8px;
    background: #7f1d1d; color: #fff; font-size: 13px; font-weight: 600;
  }}
  .attack-banner strong {{
    display: inline-block; margin-right: 6px; padding: 1px 6px; border-radius: 4px;
    background: #fff; color: #7f1d1d; font-size: 11px; letter-spacing: .06em;
  }}
  svg.arcs {{
    position: absolute; inset: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 3; overflow: visible;
  }}
  .card {{ position: relative; z-index: 2; }}
  .empty {{ padding: 24px; text-align: center; color: var(--muted); }}
  .empty.subtle {{ padding: 12px; font-size: 13px; }}

  /* Drawer */
  .backdrop {{
    position: fixed; inset: 0; background: rgba(28,25,23,.35);
    opacity: 0; pointer-events: none; transition: opacity .18s ease; z-index: 40;
  }}
  .backdrop.open {{ opacity: 1; pointer-events: auto; }}
  .drawer {{
    position: fixed; top: 0; right: 0; height: 100vh; height: 100dvh;
    width: min(920px, 96vw);
    background: var(--panel); border-left: 1px solid var(--line);
    box-shadow: -12px 0 40px rgba(0,0,0,.12);
    transform: translateX(105%); transition: transform .2s ease;
    z-index: 50; display: flex; flex-direction: column;
    font-family: ui-sans-serif, system-ui, sans-serif;
    overscroll-behavior: contain;
  }}
  .drawer.open {{ transform: translateX(0); }}
  .drawer-head {{
    padding: 14px 16px 0; border-bottom: 1px solid var(--line);
    background: #f7f3ec; flex: 0 0 auto;
  }}
  .drawer-top {{ display: flex; align-items: flex-start; gap: 10px; }}
  .drawer-top h2 {{ margin: 0; font-size: 16px; flex: 1; line-height: 1.35; }}
  .drawer-close {{
    border: 1px solid var(--line); background: #fff; border-radius: 8px;
    width: 34px; height: 34px; cursor: pointer; font-size: 18px; line-height: 1;
  }}
  .drawer-meta {{ color: var(--muted); font-size: 12px; margin: 6px 0 10px; }}
  .tabs {{ display: flex; gap: 4px; }}
  .tab {{
    border: none; background: transparent; padding: 8px 12px; cursor: pointer;
    font: inherit; font-size: 13px; font-weight: 600; color: var(--muted);
    border-bottom: 2px solid transparent; margin-bottom: -1px;
  }}
  .tab.on {{ color: var(--accent); border-bottom-color: var(--accent); }}
  .drawer-body {{
    flex: 1 1 auto;
    min-height: 0;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 14px 16px 28px;
    overscroll-behavior: contain;
    -webkit-overflow-scrolling: touch;
  }}
  .tab-pane {{ display: none; }}
  .tab-pane.on {{ display: block; }}
  .ov-title {{ margin: 0 0 10px; font-size: 14px; line-height: 1.45; }}
  .ov-list {{ margin: 0; padding-left: 18px; font-size: 13px; line-height: 1.55; }}
  .ov-list li {{ margin-bottom: 4px; }}
  .mail-body, .plain-body {{
    margin: 0; white-space: pre-wrap; word-break: break-word;
    font-size: 13px; line-height: 1.45; background: #fff; border: 1px solid var(--line);
    border-radius: 10px; padding: 12px;
  }}
  .owl-paths {{
    color: var(--muted); font-size: 11px; font-family: ui-monospace, Menlo, monospace;
    margin-bottom: 10px; word-break: break-all;
  }}
  .artifact {{
    border: 1px solid var(--line); border-radius: 10px; background: #fff;
    margin-bottom: 8px; overflow: hidden;
  }}
  .artifact > summary, .artifact.header-only {{
    list-style: none; cursor: pointer; padding: 8px 10px; font-size: 12px; font-weight: 600;
  }}
  .artifact > summary::-webkit-details-marker {{ display: none; }}
  .artifact pre {{
    margin: 0; padding: 10px; border-top: 1px solid var(--line);
    white-space: pre-wrap; word-break: break-word; font-size: 12px;
    max-height: 240px; overflow: auto; overscroll-behavior: contain;
    background: #fafaf9;
  }}

  /* OWL round styles (from agent log viewer) */
  .round {{
    border: 1px solid var(--line); border-radius: 14px; background: var(--round);
    margin-bottom: 14px; overflow: hidden;
  }}
  .round-summary {{
    list-style: none; cursor: pointer;
    display: grid; grid-template-columns: auto 1fr auto; gap: 12px; align-items: baseline;
    padding: 12px 14px; background: #f3eee4; border-bottom: 1px solid var(--line);
  }}
  .round-summary::-webkit-details-marker {{ display: none; }}
  .round-title {{ font-weight: 700; font-size: 14px; }}
  .round-meta {{ color: var(--muted); font-size: 11px; font-family: ui-monospace, Menlo, monospace; }}
  .round-stats {{ color: var(--accent); font-size: 11px; font-weight: 600; white-space: nowrap; }}
  .round-body.dual {{
    display: grid; grid-template-columns: minmax(220px, 34%) 1fr; gap: 0; min-height: 160px;
  }}
  .col {{ padding: 12px; min-width: 0; }}
  .summary-col {{ background: #f7f3ec; border-right: 1px solid var(--line); }}
  .detail-col {{ background: var(--panel); overflow: visible; }}
  .col-head {{
    font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 10px;
  }}
  .sum-block {{ margin-bottom: 14px; }}
  .sum-text {{
    margin: 0; padding: 8px 10px; border-radius: 8px; font-size: 13px; line-height: 1.45;
    border: 1px solid var(--line);
  }}
  .user-sum {{ background: var(--user); }}
  .asst-sum {{ background: var(--assistant); }}
  .sum-list {{ margin: 0; padding-left: 18px; font-size: 12px; line-height: 1.55; }}
  .sum-list li {{ margin-bottom: 4px; }}
  .step-label {{
    margin: 10px 0 6px; font-size: 11px; font-weight: 700; letter-spacing: 0.04em;
    text-transform: uppercase; color: var(--accent);
  }}
  .step-label:first-child {{ margin-top: 0; }}
  .internals-feed.flat {{ border-left: 3px solid var(--accent); padding-left: 8px; margin-bottom: 8px; }}
  .bubble {{
    border: 1px solid var(--line); border-radius: 10px; background: var(--meta);
    overflow: hidden; margin-bottom: 8px;
  }}
  .bubble.compact {{ margin-bottom: 6px; }}
  .bubble.user {{ background: var(--user); }}
  .bubble.assistant {{ background: var(--assistant); }}
  .bubble.tool {{ background: var(--tool); }}
  .bubble.system {{ background: var(--system); }}
  .bubble.write {{ background: var(--write); }}
  .bubble.warn {{ background: var(--warn); }}
  .bubble.meta {{ background: var(--meta); }}
  .bubble > summary, .bubble.header-only .title {{
    list-style: none; cursor: pointer; padding: 8px 10px; font-size: 12px; font-weight: 600;
    display: flex; justify-content: space-between; gap: 10px; align-items: baseline;
  }}
  .bubble > summary::-webkit-details-marker {{ display: none; }}
  .bubble pre {{
    margin: 0; padding: 8px 10px 10px; border-top: 1px solid var(--line);
    white-space: pre-wrap; word-break: break-word; font-size: 11.5px; line-height: 1.4;
    max-height: 220px; overflow: auto; overscroll-behavior: contain;
    background: rgba(255,255,255,.55);
  }}
  .bubble .ts {{ color: var(--muted); font-weight: 500; font-size: 10px; font-family: ui-monospace, Menlo, monospace; }}
  @media (max-width: 720px) {{
    .round-body.dual {{ grid-template-columns: 1fr; }}
    .summary-col {{ border-right: none; border-bottom: 1px solid var(--line); }}
  }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>{esc(title)}</h1>
    <p class="sub">
      {len(members)} 人 · {meta['event_count']} 事件 · {meta.get('mail_cards', 0)} 封邮件
      · {meta.get('logon_count', 0)} 条登录/登出 · {meta['arc_count']} 条单向往来
      · {meta.get('owl_linked', 0)} 个任务已挂载 OWL 执行详情
      {sub_extra}
      · 单击任务块查看调用链与产物
    </p>
    {attack_callout}
    <div class="panel">
      <div class="toolbar">
        <strong>筛选</strong>
        {"".join(chips)}
        <span class="legend">工作 · 登录 · 登出 · 发信 · 回信 · 摸鱼 · 休息 · 红色 ATTACK=攻击</span>
      </div>
      <div class="lanes-head">{"".join(head_cells)}</div>
      <div class="body" id="lane-body">
        <svg class="arcs" id="arc-layer" aria-hidden="true">
          <defs>
            <marker id="arrow-end" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
              <path d="M0,0 L8,4 L0,8 Z" fill="var(--arc)"/>
            </marker>
          </defs>
        </svg>
        {"".join(rows_html) if rows_html else '<div class="empty">没有可展示的事件</div>'}
      </div>
    </div>
  </div>

  <div class="backdrop" id="backdrop"></div>
  <aside class="drawer" id="drawer" aria-hidden="true">
    <div class="drawer-head">
      <div class="drawer-top">
        <h2 id="drawer-title"></h2>
        <button type="button" class="drawer-close" id="drawer-close" aria-label="关闭">×</button>
      </div>
      <div class="drawer-meta" id="drawer-meta"></div>
      <div class="tabs" role="tablist">
        <button type="button" class="tab on" data-tab="overview">概览</button>
        <button type="button" class="tab" data-tab="execution">执行逻辑</button>
        <button type="button" class="tab" data-tab="artifacts">产物</button>
      </div>
    </div>
    <div class="drawer-body">
      <div class="tab-pane on" id="pane-overview"></div>
      <div class="tab-pane" id="pane-execution"></div>
      <div class="tab-pane" id="pane-artifacts"></div>
    </div>
  </aside>

<script>
const ARCS = {arcs_json};
const DETAILS = {details_json};

(function () {{
  const body = document.getElementById("lane-body");
  const svg = document.getElementById("arc-layer");
  const backdrop = document.getElementById("backdrop");
  const drawer = document.getElementById("drawer");
  const drawerBody = document.querySelector(".drawer-body");
  const drawerTitle = document.getElementById("drawer-title");
  const drawerMeta = document.getElementById("drawer-meta");
  const paneOverview = document.getElementById("pane-overview");
  const paneExecution = document.getElementById("pane-execution");
  const paneArtifacts = document.getElementById("pane-artifacts");
  const closeBtn = document.getElementById("drawer-close");
  if (!body || !svg) return;

  let filter = "all";
  let activeId = null;
  let lockedScrollY = 0;

  function lockPageScroll() {{
    lockedScrollY = window.scrollY || window.pageYOffset || 0;
    document.documentElement.classList.add("drawer-open");
    document.body.classList.add("drawer-open");
    document.body.style.top = `-${{lockedScrollY}}px`;
  }}

  function unlockPageScroll() {{
    document.documentElement.classList.remove("drawer-open");
    document.body.classList.remove("drawer-open");
    document.body.style.top = "";
    window.scrollTo(0, lockedScrollY);
  }}

  function relBox(el) {{
    const br = body.getBoundingClientRect();
    const r = el.getBoundingClientRect();
    return {{
      left: r.left - br.left,
      right: r.right - br.left,
      top: r.top - br.top,
      bottom: r.bottom - br.top,
      cx: (r.left + r.right) / 2 - br.left,
      cy: (r.top + r.bottom) / 2 - br.top,
    }};
  }}

  function visible(el) {{
    if (!el) return false;
    if (el.classList.contains("dim")) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }}

  function drawArcs() {{
    const br = body.getBoundingClientRect();
    svg.setAttribute("viewBox", `0 0 ${{br.width}} ${{br.height}}`);
    svg.setAttribute("width", String(br.width));
    svg.setAttribute("height", String(br.height));
    [...svg.querySelectorAll("path.arc")].forEach((p) => p.remove());

    ARCS.forEach((pair) => {{
      const ea = document.getElementById(pair.a);
      const eb = document.getElementById(pair.b);
      if (!visible(ea) || !visible(eb)) return;
      const a = relBox(ea);
      const b = relBox(eb);
      const goingRight = b.cx >= a.cx;
      const x1 = goingRight ? a.right : a.left;
      const x2 = goingRight ? b.left : b.right;
      const y1 = a.cy;
      const y2 = b.cy;
      const dx = Math.max(40, Math.abs(x2 - x1) * 0.35);
      const c1x = goingRight ? x1 + dx : x1 - dx;
      const c2x = goingRight ? x2 - dx : x2 + dx;
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("class", "arc");
      path.setAttribute("d", `M ${{x1}} ${{y1}} C ${{c1x}} ${{y1}}, ${{c2x}} ${{y2}}, ${{x2}} ${{y2}}`);
      path.setAttribute("fill", "none");
      path.setAttribute("stroke", "var(--arc)");
      path.setAttribute("stroke-width", "1.6");
      path.setAttribute("opacity", activeId && (pair.a === activeId || pair.b === activeId) ? "0.95" : "0.45");
      path.setAttribute("marker-end", "url(#arrow-end)");
      svg.appendChild(path);
    }});
  }}

  function applyFilter() {{
    document.querySelectorAll(".card").forEach((card) => {{
      const mid = card.getAttribute("data-member");
      const isAttack = card.getAttribute("data-attack") === "1";
      let show = true;
      if (filter === "attack") show = isAttack;
      else if (filter !== "all") show = mid === filter;
      card.classList.toggle("dim", !show);
    }});
    drawArcs();
  }}

  function setTab(name) {{
    document.querySelectorAll(".tab").forEach((t) => {{
      t.classList.toggle("on", t.getAttribute("data-tab") === name);
    }});
    document.querySelectorAll(".tab-pane").forEach((p) => {{
      p.classList.toggle("on", p.id === "pane-" + name);
    }});
    if (drawerBody) drawerBody.scrollTop = 0;
  }}

  function openDrawer(card) {{
    const id = card.id;
    const d = DETAILS[id] || {{}};
    document.querySelectorAll(".card.active").forEach((c) => c.classList.remove("active"));
    card.classList.add("active");
    activeId = id;

    drawerTitle.textContent = d.title || card.getAttribute("data-title") || "";
    drawerMeta.textContent = d.meta || [
      card.getAttribute("data-member") || "",
      card.getAttribute("data-time") || "",
      card.getAttribute("data-kind") || "",
    ].filter(Boolean).join(" · ");
    paneOverview.innerHTML = d.overview_html || ("<p>" + (card.getAttribute("data-summary") || "") + "</p>");
    paneExecution.innerHTML = d.execution_html || '<p class="empty">无执行详情</p>';
    paneArtifacts.innerHTML = d.artifacts_html || '<p class="empty">无产物</p>';

    // Prefer execution tab for OWL / mail / attack
    const prefer = (d.is_attack || d.has_owl || (d.kind || "").startsWith("mail"))
      ? "execution" : "overview";
    setTab(prefer);

    if (!drawer.classList.contains("open")) {{
      lockPageScroll();
    }}
    drawer.classList.add("open");
    backdrop.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    if (drawerBody) drawerBody.scrollTop = 0;

    const related = new Set([card.id]);
    ARCS.forEach((p) => {{
      if (p.a === card.id) related.add(p.b);
      if (p.b === card.id) related.add(p.a);
    }});
    document.querySelectorAll(".card").forEach((c) => {{
      if (filter === "attack") {{
        c.classList.toggle("dim", c.getAttribute("data-attack") !== "1" || (related.size > 1 && !related.has(c.id)));
        return;
      }}
      if (filter !== "all" && c.getAttribute("data-member") !== filter) {{
        c.classList.add("dim");
        return;
      }}
      c.classList.toggle("dim", related.size > 1 ? !related.has(c.id) : false);
    }});
    drawArcs();
  }}

  function closeDrawer() {{
    if (!drawer.classList.contains("open")) return;
    drawer.classList.remove("open");
    backdrop.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    document.querySelectorAll(".card.active").forEach((c) => c.classList.remove("active"));
    activeId = null;
    unlockPageScroll();
    applyFilter();
  }}

  document.querySelectorAll(".chip").forEach((chip) => {{
    chip.addEventListener("click", () => {{
      document.querySelectorAll(".chip").forEach((c) => c.classList.remove("on"));
      chip.classList.add("on");
      filter = chip.getAttribute("data-filter") || "all";
      applyFilter();
    }});
  }});

  document.querySelectorAll(".card").forEach((card) => {{
    card.addEventListener("click", () => openDrawer(card));
  }});

  document.querySelectorAll(".tab").forEach((tab) => {{
    tab.addEventListener("click", () => setTab(tab.getAttribute("data-tab") || "overview"));
  }});

  closeBtn.addEventListener("click", closeDrawer);
  backdrop.addEventListener("click", closeDrawer);
  backdrop.addEventListener("wheel", (e) => e.preventDefault(), {{ passive: false }});
  backdrop.addEventListener("touchmove", (e) => e.preventDefault(), {{ passive: false }});
  document.addEventListener("keydown", (e) => {{
    if (e.key === "Escape") closeDrawer();
  }});

  applyFilter();
  window.addEventListener("resize", drawArcs);
  requestAnimationFrame(() => requestAnimationFrame(drawArcs));
}})();
</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate unified Chimera day timeline + OWL execution drawer"
    )
    parser.add_argument(
        "--logs",
        type=Path,
        default=Path("chimera_scenario_1/execution_logs"),
        help="Path to execution_logs or attack_logs/<run> directory",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output HTML path (default: <logs>/day_timeline_viewer.html)",
    )
    parser.add_argument("--open", action="store_true", help="Open in browser after write")
    args = parser.parse_args()

    logs_dir = args.logs.resolve()
    out = (args.out or (logs_dir / "day_timeline_viewer.html")).resolve()

    members, events, arcs, meta, details = load_day_data(logs_dir)
    if meta.get("is_attack_run"):
        attid = (meta.get("attack_info") or {}).get("attid") or logs_dir.name
        title = f"Chimera 攻击日时间线 · {attid}"
    else:
        title = "Chimera 一日工作时间线"
    html_text = render_html(members, events, arcs, meta, details, title)
    out.write_text(html_text, encoding="utf-8")
    print(f"Wrote {out}")
    print(
        f"Members: {len(members)} · events: {meta['event_count']} · "
        f"emails: {meta.get('mail_cards', 0)} · logons: {meta.get('logon_count', 0)} · "
        f"arcs: {meta['arc_count']} · "
        f"OWL-linked: {meta.get('owl_linked', 0)} · "
        f"attacks: {meta.get('attack_count', 0)}"
    )
    print(f"HTML size: {out.stat().st_size / 1e6:.2f} MB")
    if args.open:
        webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()

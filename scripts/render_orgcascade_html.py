#!/usr/bin/env python3
"""Render the OrgCascade research markdown to a standalone HTML page."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "org-cascade" / "ORG_CASCADE_RESEARCH.md"
DST = ROOT / "docs" / "org-cascade" / "ORG_CASCADE_RESEARCH.html"


def convert(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    in_code = False
    in_table = False
    table_rows: list[list[str]] = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return
        out.append("<table>")
        for index, row in enumerate(table_rows):
            tag = "th" if index == 0 else "td"
            if index == 1 and all(set(cell) <= set("-: ") for cell in row):
                continue
            out.append("<tr>" + "".join(f"<{tag}>{inline(cell)}</{tag}>" for cell in row) + "</tr>")
        out.append("</table>")
        table_rows = []
        in_table = False

    def inline(text: str) -> str:
        text = html.escape(text)
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            r'<a href="\2" target="_blank" rel="noreferrer">\1</a>',
            text,
        )
        return text

    for line in lines:
        if line.startswith("```"):
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                flush_table()
                lang = html.escape(line[3:].strip())
                out.append(f'<pre><code class="{lang}">')
                in_code = True
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        if line.startswith("|"):
            in_table = True
            table_rows.append([cell.strip() for cell in line.strip("|").split("|")])
            continue
        if in_table:
            flush_table()
        image = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if image:
            alt, src = image.group(1), image.group(2)
            out.append(
                f'<figure><img src="{html.escape(src)}" alt="{html.escape(alt)}">'
                f"<figcaption>{html.escape(alt)}</figcaption></figure>"
            )
            continue
        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("#### "):
            out.append(f"<h4>{inline(line[5:])}</h4>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        elif line.startswith("- "):
            if not out or not out[-1].startswith("<ul") and out[-1] != "<li>":
                # keep it simple: each bullet is its own list
                out.append(f"<ul><li>{inline(line[2:])}</li></ul>")
            else:
                out.append(f"<ul><li>{inline(line[2:])}</li></ul>")
        elif line.startswith("|"):
            continue
        elif re.match(r"^\d+\. ", line):
            out.append(f"<ol><li>{inline(re.sub(r'^\d+\. ', '', line))}</li></ol>")
        elif line.strip() == "":
            continue
        else:
            out.append(f"<p>{inline(line)}</p>")
    flush_table()
    return "\n".join(out)


HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Chimera 员工分组与级联日程调研</title>
  <style>
    :root { --ink:#0f172a; --muted:#475569; --line:#e2e8f0; --accent:#0f766e; }
    body { margin:0; background:#f8fafc; color:var(--ink);
           font: 16px/1.65 "Source Han Sans SC","Noto Sans SC",sans-serif; }
    main { max-width: 920px; margin: 32px auto 80px; background:#fff;
           padding: 48px 56px; border:1px solid var(--line); border-radius: 16px; }
    h1 { font-size: 28px; line-height: 1.3; }
    h2 { margin-top: 40px; padding-top: 12px; border-top:1px solid var(--line); }
    h3 { color:#134e4a; }
    a { color:#0f766e; }
    code { background:#f1f5f9; padding: 0 4px; border-radius:4px; font-size: 0.92em; }
    pre { background:#0f172a; color:#e2e8f0; padding:16px; border-radius:12px; overflow:auto; }
    pre code { background:transparent; color:inherit; }
    table { border-collapse: collapse; width:100%; margin: 16px 0; font-size:14px; }
    th, td { border:1px solid var(--line); padding:8px 10px; vertical-align:top; }
    th { background:#f0fdfa; text-align:left; }
    figure { margin: 24px 0; }
    img { max-width:100%; height:auto; border:1px solid var(--line); border-radius:12px; }
    figcaption { color:var(--muted); font-size:13px; margin-top:8px; }
    blockquote { border-left:4px solid var(--accent); margin: 16px 0; padding: 8px 16px;
                 background:#f0fdfa; color:#134e4a; }
    ul, ol { padding-left: 1.2em; }
  </style>
</head>
<body>
<main>
BODY
</main>
</body>
</html>
"""


def main() -> None:
    body = convert(SRC.read_text(encoding="utf-8"))
    DST.write_text(HTML.replace("BODY", body), encoding="utf-8")
    print(DST)


if __name__ == "__main__":
    main()

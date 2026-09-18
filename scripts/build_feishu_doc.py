#!/usr/bin/env python3
"""Build a Feishu-importable HTML pack and optionally publish it.

The research note lives at ``docs/chimera-tool-composition-research.md``.
This script:

1. Always emits a self-contained HTML file with embedded figures
   (``docs/feishu/chimera-tool-composition.html``).
2. If ``FEISHU_APP_ID`` / ``FEISHU_APP_SECRET`` are set, imports that HTML
   into a Feishu cloud doc via the official drive import API and prints the URL.

Usage::

    python scripts/build_feishu_doc.py
    FEISHU_APP_ID=cli_xxx FEISHU_APP_SECRET=xxx python scripts/build_feishu_doc.py --publish
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "chimera-tool-composition-research.md"
ASSETS = ROOT / "docs" / "assets"
OUT_DIR = ROOT / "docs" / "feishu"
OUT_HTML = OUT_DIR / "chimera-tool-composition.html"
FEISHU_OPEN = "https://open.feishu.cn/open-apis"


def _md_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _embed_image(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    html: list[str] = []
    in_code = False
    in_ul = False
    in_ol = False
    in_table = False
    table_rows: list[list[str]] = []
    code_buf: list[str] = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            html.append("</ul>")
            in_ul = False
        if in_ol:
            html.append("</ol>")
            in_ol = False

    def flush_table() -> None:
        nonlocal in_table, table_rows
        if not in_table:
            return
        html.append('<table>')
        for i, row in enumerate(table_rows):
            tag = "th" if i == 0 else "td"
            if i == 1 and all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in row):
                continue
            html.append("<tr>" + "".join(f"<{tag}>{_md_inline(c.strip())}</{tag}>" for c in row) + "</tr>")
        html.append("</table>")
        in_table = False
        table_rows = []

    for raw in lines:
        if raw.startswith("```"):
            if in_code:
                html.append("<pre><code>" + "\n".join(code_buf) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                close_lists()
                flush_table()
                in_code = True
            continue
        if in_code:
            code_buf.append(raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue

        img = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", raw.strip())
        if img:
            close_lists()
            flush_table()
            alt, src = img.group(1), img.group(2)
            path = (DOC.parent / src).resolve()
            if path.exists():
                html.append(
                    f'<figure><img src="{_embed_image(path)}" alt="{alt}" />'
                    f"<figcaption>{alt}</figcaption></figure>"
                )
            else:
                html.append(f"<p>[missing image: {src}]</p>")
            continue

        if raw.strip().startswith("|") and raw.strip().endswith("|"):
            close_lists()
            cells = [c for c in raw.strip().strip("|").split("|")]
            in_table = True
            table_rows.append(cells)
            continue
        flush_table()

        if not raw.strip():
            close_lists()
            continue
        if raw.startswith("# "):
            close_lists()
            html.append(f"<h1>{_md_inline(raw[2:].strip())}</h1>")
            continue
        if raw.startswith("## "):
            close_lists()
            html.append(f"<h2>{_md_inline(raw[3:].strip())}</h2>")
            continue
        if raw.startswith("### "):
            close_lists()
            html.append(f"<h3>{_md_inline(raw[4:].strip())}</h3>")
            continue
        if raw.startswith("#### "):
            close_lists()
            html.append(f"<h4>{_md_inline(raw[5:].strip())}</h4>")
            continue
        if re.match(r"^\d+\. ", raw.strip()):
            if in_ul:
                html.append("</ul>")
                in_ul = False
            if not in_ol:
                html.append("<ol>")
                in_ol = True
            html.append(f"<li>{_md_inline(re.sub(r'^\d+\.\s+', '', raw.strip()))}</li>")
            continue
        if raw.strip().startswith("- "):
            if in_ol:
                html.append("</ol>")
                in_ol = False
            if not in_ul:
                html.append("<ul>")
                in_ul = True
            html.append(f"<li>{_md_inline(raw.strip()[2:])}</li>")
            continue
        if raw.strip() == "---":
            close_lists()
            html.append("<hr/>")
            continue
        close_lists()
        html.append(f"<p>{_md_inline(raw.strip())}</p>")

    close_lists()
    flush_table()
    return "\n".join(html)


CSS = """
body { font-family: "PingFang SC","Noto Sans CJK SC","WenQuanYi Micro Hei",sans-serif;
       max-width: 980px; margin: 32px auto 80px; padding: 0 28px; color: #1B365D;
       line-height: 1.7; background: #fff; }
h1 { font-size: 28px; border-bottom: 3px solid #2A9D8F; padding-bottom: 10px; }
h2 { font-size: 22px; color: #14375A; margin-top: 36px; }
h3 { font-size: 18px; color: #2A9D8F; }
code { background: #F4F7FB; padding: 1px 5px; border-radius: 4px; font-size: 90%; }
pre { background: #14375A; color: #F4F7FB; padding: 14px; overflow: auto; border-radius: 8px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0 20px; font-size: 14px; }
th, td { border: 1px solid #D5DEE8; padding: 8px 10px; vertical-align: top; }
th { background: #1B365D; color: #fff; }
tr:nth-child(even) td { background: #F4F7FB; }
figure { margin: 18px 0 28px; }
img { max-width: 100%; height: auto; border: 1px solid #E8EEF5; border-radius: 8px; }
figcaption { color: #5C6B7A; font-size: 13px; text-align: center; margin-top: 6px; }
a { color: #2A9D8F; }
blockquote { border-left: 4px solid #C9A227; margin: 0; padding: 4px 14px; background: #FFF8E7; }
"""


def build_html() -> Path:
    if not DOC.exists():
        raise SystemExit(f"missing markdown: {DOC}")
    body = markdown_to_html(DOC.read_text(encoding="utf-8"))
    page = (
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'/>"
        "<title>Chimera 员工工具联通性调研</title>"
        f"<style>{CSS}</style></head><body>{body}</body></html>"
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(page, encoding="utf-8")
    return OUT_HTML


def _http(method: str, url: str, token: str | None = None, data=None, headers=None):
    hdrs = dict(headers or {})
    if token:
        hdrs["Authorization"] = f"Bearer {token}"
    body = None
    if data is not None and not isinstance(data, (bytes, bytearray)):
        hdrs.setdefault("Content-Type", "application/json; charset=utf-8")
        body = json.dumps(data).encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        body = data
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Feishu HTTP {exc.code} {url}: {detail}") from exc


def tenant_token(app_id: str, app_secret: str) -> str:
    payload = _http(
        "POST",
        f"{FEISHU_OPEN}/auth/v3/tenant_access_token/internal",
        data={"app_id": app_id, "app_secret": app_secret},
    )
    if payload.get("code") not in (0, None) and "tenant_access_token" not in payload:
        raise RuntimeError(f"token error: {payload}")
    token = payload.get("tenant_access_token")
    if not token:
        raise RuntimeError(f"token error: {payload}")
    return token


def publish_html(html_path: Path, token: str, folder_token: str | None) -> str:
    raw = html_path.read_bytes()
    boundary = "----ChimeraFeishuBoundary"
    extra = json.dumps({"obj_type": "docx", "file_extension": "html"})
    parts = []

    def add(name: str, value: str):
        parts.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
        )

    add("file_name", html_path.name)
    add("parent_type", "ccm_import_open")
    add("size", str(len(raw)))
    add("extra", extra)
    parts.append(
        (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
            f"filename=\"{html_path.name}\"\r\nContent-Type: text/html\r\n\r\n"
        ).encode()
        + raw
        + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    uploaded = _http(
        "POST",
        f"{FEISHU_OPEN}/drive/v1/medias/upload_all",
        token,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    file_token = (uploaded.get("data") or {}).get("file_token") or uploaded.get("file_token")
    if not file_token:
        raise RuntimeError(f"upload failed: {uploaded}")

    task_body = {
        "file_extension": "html",
        "file_token": file_token,
        "type": "docx",
        "file_name": "Chimera 员工工具联通性调研",
    }
    if folder_token:
        task_body["point"] = {"mount_type": 1, "mount_key": folder_token}
    created = _http("POST", f"{FEISHU_OPEN}/drive/v1/import_tasks", token, data=task_body)
    ticket = (created.get("data") or {}).get("ticket")
    if not ticket:
        raise RuntimeError(f"import task failed: {created}")

    for _ in range(30):
        time.sleep(2)
        status = _http("GET", f"{FEISHU_OPEN}/drive/v1/import_tasks/{ticket}", token)
        data = status.get("data") or status
        result = data.get("result") or data
        if result.get("job_status") == 0 or result.get("token"):
            doc_token = result.get("token")
            url = result.get("url") or (f"https://feishu.cn/docx/{doc_token}" if doc_token else "")
            return url or json.dumps(result, ensure_ascii=False)
        if result.get("job_status") not in (1, 2, None):
            raise RuntimeError(f"import failed: {status}")
    raise RuntimeError("import timed out")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true", help="Import into Feishu if credentials exist")
    args = parser.parse_args()
    html_path = build_html()
    print(f"built {html_path} ({html_path.stat().st_size} bytes)")

    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    folder = os.environ.get("FEISHU_FOLDER_TOKEN", "").strip() or None
    if args.publish or (app_id and app_secret):
        if not app_id or not app_secret:
            print(
                "Feishu credentials missing. Set FEISHU_APP_ID and FEISHU_APP_SECRET, "
                "optionally FEISHU_FOLDER_TOKEN, then rerun with --publish.",
                file=sys.stderr,
            )
            return 2
        token = tenant_token(app_id, app_secret)
        url = publish_html(html_path, token, folder)
        print(f"feishu_doc_url={url}")
        (OUT_DIR / "feishu_url.txt").write_text(url + "\n", encoding="utf-8")
        return 0

    print(
        "HTML pack is ready for Feishu import:\n"
        "  1. Open Feishu → 云文档 → 导入 → 选择 HTML\n"
        f"  2. Upload {html_path}\n"
        "  3. Or set FEISHU_APP_ID / FEISHU_APP_SECRET and rerun with --publish"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

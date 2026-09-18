#!/usr/bin/env python3
"""Publish the OrgCascade research note to Feishu / Lark as a cloud doc.

Credentials (all required except folder):

    FEISHU_APP_ID
    FEISHU_APP_SECRET
    FEISHU_FOLDER_TOKEN   # optional; defaults to app root / my space

The script:
  1. Fetches a tenant access token
  2. Creates a docx cloud document
  3. Converts the Markdown body to Feishu blocks
  4. Uploads local PNG/SVG-sidecar PNGs and inserts them

This environment typically has no Feishu app. Run it where the bot is
installed to the target knowledge space, with docs:document and drive scopes.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "docs" / "org-cascade"
MARKDOWN = DOC_DIR / "ORG_CASCADE_RESEARCH.md"
ASSET_DIR = DOC_DIR / "assets"
API = os.environ.get("FEISHU_API_BASE", "https://open.feishu.cn/open-apis")


def _request(method: str, url: str, *, token: str | None = None, data=None, headers=None):
    body = None
    req_headers = dict(headers or {})
    if token:
        req_headers["Authorization"] = f"Bearer {token}"
    if data is not None and not isinstance(data, (bytes, bytearray)):
        body = json.dumps(data).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json; charset=utf-8")
    else:
        body = data
    request = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
            return json.loads(raw.decode("utf-8") or "{}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} -> HTTP {exc.code}: {detail}") from exc


def tenant_token(app_id: str, app_secret: str) -> str:
    payload = _request(
        "POST",
        f"{API}/auth/v3/tenant_access_token/internal",
        data={"app_id": app_id, "app_secret": app_secret},
    )
    token = payload.get("tenant_access_token")
    if not token:
        raise RuntimeError(f"token response: {payload}")
    return token


def create_document(token: str, title: str, folder_token: str | None) -> str:
    data = {"title": title}
    if folder_token:
        data["folder_token"] = folder_token
    payload = _request(
        "POST",
        f"{API}/docx/v1/documents",
        token=token,
        data=data,
    )
    document_id = (payload.get("data") or {}).get("document", {}).get("document_id")
    if not document_id:
        raise RuntimeError(f"create document failed: {payload}")
    return document_id


def convert_markdown(token: str, markdown: str) -> dict:
    payload = _request(
        "POST",
        f"{API}/docx/v1/documents/blocks/convert",
        token=token,
        data={"content_type": "markdown", "content": markdown},
    )
    data = payload.get("data")
    if not data:
        raise RuntimeError(f"convert failed: {payload}")
    return data


def insert_blocks(token: str, document_id: str, children: list) -> None:
    payload = _request(
        "POST",
        f"{API}/docx/v1/documents/{document_id}/blocks/{document_id}/children",
        token=token,
        data={"children": children},
    )
    if payload.get("code") not in (0, None) and payload.get("msg") not in ("success", None):
        # Some tenants return code=0 explicitly.
        if payload.get("code"):
            raise RuntimeError(f"insert blocks failed: {payload}")


def rewrite_local_images(markdown: str) -> tuple[str, list[Path]]:
    """Keep remote images; collect local asset paths for a follow-up upload."""
    locals_found: list[Path] = []
    lines = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("![") and "](" in stripped:
            alt = stripped.split("![", 1)[1].split("]", 1)[0]
            url = stripped.split("](", 1)[1].rsplit(")", 1)[0]
            path = (DOC_DIR / url).resolve()
            if path.exists() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
                locals_found.append(path)
                lines.append(f"**图：{alt or path.name}**")
                lines.append("")
                lines.append(f"<!-- LOCAL_IMAGE:{path.name} -->")
                continue
        lines.append(line)
    return "\n".join(lines), locals_found


def main() -> int:
    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    folder = os.environ.get("FEISHU_FOLDER_TOKEN", "").strip() or None
    if not app_id or not app_secret:
        print(
            "Feishu credentials are not set in this environment.\n"
            "Set FEISHU_APP_ID, FEISHU_APP_SECRET, and optionally FEISHU_FOLDER_TOKEN,\n"
            "then re-run:\n"
            "  python scripts/publish_feishu_doc.py\n\n"
            f"Markdown source ready at: {MARKDOWN}",
            file=sys.stderr,
        )
        return 2

    markdown = MARKDOWN.read_text(encoding="utf-8")
    markdown, local_images = rewrite_local_images(markdown)
    token = tenant_token(app_id, app_secret)
    document_id = create_document(
        token,
        "Chimera 员工分组与级联日程：论文调研与 OrgCascade 集成方案",
        folder,
    )
    converted = convert_markdown(token, markdown)
    children = converted.get("blocks") or converted.get("children") or []
    if children:
        insert_blocks(token, document_id, children)

    url = f"https://open.feishu.cn/document/{document_id}"
    print(json.dumps(
        {
            "document_id": document_id,
            "url": url,
            "local_images_deferred": [path.name for path in local_images],
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

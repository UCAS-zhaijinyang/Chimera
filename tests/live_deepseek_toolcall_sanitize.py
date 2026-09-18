#!/usr/bin/env python3
"""Live DeepSeek check: unpaired tool_calls 400, sanitizer makes the same payload succeed.

Usage (inside the Chimera container / venv):

    PYTHONPATH=src python tests/live_deepseek_toolcall_sanitize.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

from openai import OpenAI  # noqa: E402
from openai_tool_messages import (  # noqa: E402
    install_openai_tool_message_compat,
    sanitize_openai_tool_messages,
)


UNPAIRED = [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user", "content": "Say the single word ok."},
    {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "id": "call_truncated_ls",
                "type": "function",
                "function": {"name": "ls", "arguments": "{}"},
            },
            {
                "id": "call_truncated_cat",
                "type": "function",
                "function": {"name": "cat", "arguments": "{}"},
            },
        ],
    },
    {
        "role": "tool",
        "tool_call_id": "call_truncated_ls",
        "content": "file.txt",
    },
]


def _client() -> OpenAI:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY is missing")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def _create(client: OpenAI, messages):
    return client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        max_tokens=16,
        temperature=0,
        stream=False,
    )


def main() -> int:
    client = _client()
    print("1) Unpaired tool_calls payload (expected DeepSeek 400)...")
    unpaired_failed = False
    try:
        _create(client, UNPAIRED)
    except Exception as exc:
        text = str(exc)
        unpaired_failed = "tool_calls" in text or "400" in text or "BadRequest" in type(exc).__name__
        print(f"   got {type(exc).__name__}: {text[:300]}")
    if not unpaired_failed:
        print("FAIL: DeepSeek accepted unpaired tool_calls; cannot confirm the original bug")
        return 1
    print("   PASS: DeepSeek rejected unpaired tool_calls")

    sanitized = sanitize_openai_tool_messages(UNPAIRED)
    print("2) Same payload after sanitize_openai_tool_messages (expected success)...")
    print(f"   kept {len(sanitized)}/{len(UNPAIRED)} messages")
    response = _create(client, sanitized)
    content = (response.choices[0].message.content or "").strip()
    print(f"   PASS: DeepSeek replied {content!r}")

    print("3) Camel DeepSeekModel._run after install_openai_tool_message_compat...")
    os.environ.setdefault("CHIMERA_FORCE_CLOUD", "1")
    from foundation_model import create_camel_model  # noqa: E402

    install_openai_tool_message_compat()
    model = create_camel_model(temperature=0)
    camel_response = model._run(UNPAIRED)
    camel_content = (camel_response.choices[0].message.content or "").strip()
    print(f"   PASS: Camel DeepSeekModel replied {camel_content!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

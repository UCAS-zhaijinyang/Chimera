# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2026 @ CAMEL-AI.org. All Rights Reserved. =========
"""Tolerant JSON parsing helpers for LLM outputs."""

from __future__ import annotations

import json
import re
from typing import Any

try:
    import json5
except ImportError:  # pragma: no cover
    json5 = None


def strip_code_fences(text: str) -> str:
    text = (text or "").strip()
    if "```json" in text:
        text = text.replace("```json", "").replace("```", "").strip()
    elif "```python" in text:
        text = text.replace("```python", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.strip("`").strip()
        if text.startswith("json"):
            text = text[4:].strip()
        elif text.startswith("python"):
            text = text[6:].strip()
    return text.strip()


def _loads_candidates(text: str) -> list[str]:
    """Generate parse candidates from messy LLM JSON text."""
    text = strip_code_fences(text)
    candidates = [text]

    # Common schedule failure: array body without opening '['
    # e.g. { "Time": ... }, { ... } ]
    stripped = text.lstrip()
    if stripped.startswith("{") and (
        stripped.rstrip().endswith("]") or "},\n" in stripped or "},\r\n" in stripped
    ):
        if not stripped.startswith("["):
            body = stripped
            if body.endswith("]"):
                body = body[:-1].rstrip().rstrip(",")
            candidates.append("[" + body + "]")

    # Missing closing bracket for array
    if stripped.startswith("[") and not stripped.rstrip().endswith("]"):
        candidates.append(stripped.rstrip().rstrip(",") + "]")

    # Extract first balanced JSON value
    for opener, closer in (("[", "]"), ("{", "}")):
        start = text.find(opener)
        if start == -1:
            continue
        depth = 0
        in_str = False
        escape = False
        for i, ch in enumerate(text[start:], start=start):
            if in_str:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    candidates.append(text[start : i + 1])
                    break

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def _try_load(text: str) -> Any:
    errors: list[Exception] = []
    loaders = [json.loads]
    if json5 is not None:
        loaders.append(json5.loads)

    for loader in loaders:
        try:
            return loader(text)
        except Exception as e:  # noqa: BLE001 - collect and continue
            errors.append(e)

    # Repair unescaped newlines / tabs inside JSON strings, then retry.
    repaired = _escape_control_chars_in_strings(text)
    if repaired != text:
        for loader in loaders:
            try:
                return loader(repaired)
            except Exception as e:  # noqa: BLE001
                errors.append(e)

    # Last resort: single-quoted Python-ish list/dict
    try:
        return json.loads(text.replace("'", '"'))
    except Exception as e:  # noqa: BLE001
        errors.append(e)

    raise errors[-1]


def _escape_control_chars_in_strings(text: str) -> str:
    """Escape raw newlines/tabs that appear inside JSON string literals."""
    out = []
    in_str = False
    escape = False
    for ch in text:
        if in_str:
            if escape:
                out.append(ch)
                escape = False
                continue
            if ch == "\\":
                out.append(ch)
                escape = True
                continue
            if ch == '"':
                out.append(ch)
                in_str = False
                continue
            if ch == "\n":
                out.append("\\n")
                continue
            if ch == "\r":
                out.append("\\r")
                continue
            if ch == "\t":
                out.append("\\t")
                continue
            out.append(ch)
            continue
        if ch == '"':
            in_str = True
        out.append(ch)
    return "".join(out)


def parse_llm_json(text: str, expect: type | tuple[type, ...] | None = None) -> Any:
    """Parse JSON-ish LLM output with common repairs.

    Args:
        text: Raw model output.
        expect: Optional type or tuple of types the result must match
            (e.g. list, dict, (list, dict)).
    """
    last_err: Exception | None = None
    for candidate in _loads_candidates(text):
        try:
            data = _try_load(candidate)
            if expect is not None and not isinstance(data, expect):
                # Sometimes model wraps array in a single-key object
                if isinstance(data, dict) and len(data) == 1:
                    inner = next(iter(data.values()))
                    if isinstance(inner, expect):
                        data = inner
                    else:
                        raise TypeError(
                            f"Expected {expect}, got {type(data).__name__}"
                        )
                else:
                    raise TypeError(f"Expected {expect}, got {type(data).__name__}")
            return data
        except Exception as e:  # noqa: BLE001
            last_err = e
            continue
    if last_err is not None:
        raise last_err
    raise ValueError("Empty LLM JSON output")


_TIME_RE = re.compile(r"^\d{1,2}:\d{2}(:\d{2})?$")


def normalize_schedule(data: Any) -> list[dict]:
    """Ensure schedule is a list of {{Time, Activity}} dicts."""
    if isinstance(data, dict):
        # unwrap common wrappers
        for key in ("schedule", "Schedule", "activities", "data"):
            if key in data and isinstance(data[key], list):
                data = data[key]
                break
        else:
            if "Time" in data and "Activity" in data:
                data = [data]
            else:
                raise TypeError(f"Unrecognized schedule object keys: {list(data)}")

    if not isinstance(data, list):
        raise TypeError(f"Schedule must be a list, got {type(data).__name__}")

    cleaned = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if "Time" not in item or "Activity" not in item:
            continue
        time_val = str(item["Time"]).strip()
        # Normalize HH:MM -> HH:MM:00 when needed by callers later
        if _TIME_RE.match(time_val):
            cleaned.append(item)
    if not cleaned:
        raise ValueError("No valid schedule items found")
    return cleaned

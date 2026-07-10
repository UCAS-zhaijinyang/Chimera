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
"""Classify schedule activities for Phase-2 execution and timeline viewers.

Important: a bare ``@member-id`` mention is NOT enough to treat a task as
email-send. Many work items say "coordinate with @da-1" while still being
normal OWL work (login, investigate, meet, document, …).
"""

from __future__ import annotations

import re

# Explicit "Email @x …" as the activity opener.
_EMAIL_AT_START = re.compile(r"(?i)^\s*e-?mail\s+@")
# "send … email … @x" / "send a brief status email to @pc-1"
_SEND_EMAIL_TO = re.compile(
    r"(?i)\bsend\s+(?:a\s+)?(?:brief\s+)?(?:status\s+)?e-?mail\b[^@]{0,80}@"
)
# "mail @x …"
_MAIL_AT_START = re.compile(r"(?i)^\s*mail\s+@")


def is_email_send_activity(activity: str) -> bool:
    """Return True only when the activity's primary intent is sending email."""
    text = (activity or "").strip()
    if "@" not in text:
        return False
    if _EMAIL_AT_START.search(text):
        return True
    if _MAIL_AT_START.search(text):
        return True
    if _SEND_EMAIL_TO.search(text):
        return True
    return False


def is_email_reply_log(activity: str) -> bool:
    """Schedule rows written when a reply thread finishes."""
    return (activity or "").startswith("check received email")


def is_loaf_activity(activity: str) -> bool:
    text = activity or ""
    return "LoafBrowsing" in text or "loafing" in text.lower()


def is_break_activity(activity: str) -> bool:
    low = (activity or "").lower()
    return "break" in low or "lunch" in low

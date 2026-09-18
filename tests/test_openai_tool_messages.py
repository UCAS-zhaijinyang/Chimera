import unittest

from openai_tool_messages import sanitize_openai_tool_messages


class _Obj:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class SanitizeOpenaiToolMessagesTest(unittest.TestCase):
    def test_keeps_complete_tool_groups(self):
        messages = [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "do it"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "call_a", "type": "function", "function": {"name": "ls"}},
                    {"id": "call_b", "type": "function", "function": {"name": "cat"}},
                ],
            },
            {"role": "tool", "tool_call_id": "call_a", "content": "a"},
            {"role": "tool", "tool_call_id": "call_b", "content": "b"},
            {"role": "assistant", "content": "done"},
        ]
        self.assertEqual(sanitize_openai_tool_messages(messages), messages)

    def test_drops_truncated_tool_group(self):
        messages = [
            {"role": "system", "content": "sys"},
            {"role": "user", "content": "do it"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "call_a", "type": "function", "function": {"name": "ls"}},
                    {"id": "call_b", "type": "function", "function": {"name": "cat"}},
                ],
            },
            {"role": "tool", "tool_call_id": "call_a", "content": "a"},
            {"role": "assistant", "content": "continue"},
        ]
        sanitized = sanitize_openai_tool_messages(messages)
        self.assertEqual(
            sanitized,
            [
                {"role": "system", "content": "sys"},
                {"role": "user", "content": "do it"},
                {"role": "assistant", "content": "continue"},
            ],
        )

    def test_drops_assistant_tool_calls_with_no_replies(self):
        messages = [
            {"role": "user", "content": "do it"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "call_a", "type": "function", "function": {"name": "ls"}},
                ],
            },
            {"role": "user", "content": "and then?"},
        ]
        self.assertEqual(
            sanitize_openai_tool_messages(messages),
            [
                {"role": "user", "content": "do it"},
                {"role": "user", "content": "and then?"},
            ],
        )

    def test_drops_orphan_tool_messages(self):
        messages = [
            {"role": "user", "content": "hi"},
            {"role": "tool", "tool_call_id": "call_x", "content": "orphan"},
            {"role": "assistant", "content": "ok"},
        ]
        self.assertEqual(
            sanitize_openai_tool_messages(messages),
            [
                {"role": "user", "content": "hi"},
                {"role": "assistant", "content": "ok"},
            ],
        )

    def test_window_prefix_orphans_then_complete_group(self):
        messages = [
            {"role": "tool", "tool_call_id": "call_old", "content": "stale"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "call_a", "type": "function", "function": {"name": "ls"}},
                ],
            },
            {"role": "tool", "tool_call_id": "call_a", "content": "a"},
            {"role": "assistant", "content": "done"},
        ]
        self.assertEqual(
            sanitize_openai_tool_messages(messages),
            [
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_a",
                            "type": "function",
                            "function": {"name": "ls"},
                        },
                    ],
                },
                {"role": "tool", "tool_call_id": "call_a", "content": "a"},
                {"role": "assistant", "content": "done"},
            ],
        )

    def test_strips_extra_unmatched_tool_replies(self):
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "call_a", "type": "function", "function": {"name": "ls"}},
                ],
            },
            {"role": "tool", "tool_call_id": "call_a", "content": "a"},
            {"role": "tool", "tool_call_id": "call_extra", "content": "nope"},
            {"role": "assistant", "content": "done"},
        ]
        self.assertEqual(
            sanitize_openai_tool_messages(messages),
            [
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {"id": "call_a", "type": "function", "function": {"name": "ls"}},
                    ],
                },
                {"role": "tool", "tool_call_id": "call_a", "content": "a"},
                {"role": "assistant", "content": "done"},
            ],
        )

    def test_attribute_style_messages(self):
        messages = [
            _Obj(role="user", content="do it"),
            _Obj(
                role="assistant",
                content="",
                tool_calls=[_Obj(id="call_a")],
            ),
            _Obj(role="tool", tool_call_id="call_a", content="a"),
        ]
        sanitized = sanitize_openai_tool_messages(messages)
        self.assertEqual(len(sanitized), 3)
        self.assertIs(sanitized[0], messages[0])
        self.assertIs(sanitized[1], messages[1])
        self.assertIs(sanitized[2], messages[2])

    def test_empty_and_none(self):
        self.assertEqual(sanitize_openai_tool_messages([]), [])
        self.assertEqual(sanitize_openai_tool_messages(None), [])

    def test_idempotent(self):
        messages = [
            {"role": "user", "content": "hi"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "call_a", "type": "function", "function": {"name": "ls"}},
                    {"id": "call_b", "type": "function", "function": {"name": "cat"}},
                ],
            },
            {"role": "tool", "tool_call_id": "call_a", "content": "a"},
            {"role": "assistant", "content": "continue"},
        ]
        once = sanitize_openai_tool_messages(messages)
        self.assertEqual(sanitize_openai_tool_messages(once), once)


if __name__ == "__main__":
    unittest.main()

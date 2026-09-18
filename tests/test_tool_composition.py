from __future__ import annotations

import unittest

from tool_composition import (
    ArtifactBus,
    RoleToolkitResolver,
    ToolGraph,
    WORKPLACE_TOOLS,
    build_employee_session,
    flu_trend_demo,
)


class ToolGraphTests(unittest.TestCase):
    def setUp(self):
        self.graph = ToolGraph(WORKPLACE_TOOLS)

    def test_search_can_feed_browser(self):
        self.assertTrue(self.graph.allowed("search", "browser"))

    def test_search_cannot_jump_to_ehr(self):
        self.assertFalse(self.graph.allowed("search", "ehr"))

    def test_plan_email_from_ehr(self):
        path = self.graph.plan(["ehr"], "email")
        self.assertEqual(path[0], "ehr")
        self.assertEqual(path[-1], "email")
        self.assertGreaterEqual(len(path), 3)
        self.assertTrue(
            {"spreadsheet", "shared_drive", "file_write"} & set(path),
            path,
        )


class RoleRoutingTests(unittest.TestCase):
    def setUp(self):
        self.resolver = RoleToolkitResolver()

    def test_epidemiologist_gets_ehr_and_spreadsheet(self):
        tools = {t.name for t in self.resolver.resolve({"role": "Epidemiologist", "tools": []})}
        self.assertIn("ehr", tools)
        self.assertIn("spreadsheet", tools)
        self.assertIn("email", tools)

    def test_designer_flavour_text_is_bound(self):
        tools = {
            t.name
            for t in self.resolver.resolve(
                {
                    "role": "Designer",
                    "tools": ["Sketch", "ComponentLibraryToolkit"],
                }
            )
        }
        self.assertIn("file_write", tools)
        self.assertIn("shared_drive", tools)
        self.assertNotIn("ehr", tools)

    def test_admin_does_not_get_ehr_by_default(self):
        tools = {t.name for t in self.resolver.resolve({"role": "Administrative Assistant"})}
        self.assertNotIn("ehr", tools)
        self.assertIn("calendar", tools)
        self.assertIn("tickets", tools)


class ArtifactBusTests(unittest.TestCase):
    def test_acl_hides_ehr_from_other_staff(self):
        bus = ArtifactBus()
        record = bus.put("ehr_record", "ehr", "doc-1", {"rows": []})
        self.assertTrue(record.visible_to("doc-1"))
        self.assertFalse(record.visible_to("intern-1"))
        bus.share(record.artifact_id, ["intern-1"])
        self.assertTrue(bus.get(record.artifact_id).visible_to("intern-1"))


class FluWorkflowTests(unittest.TestCase):
    def test_email_carries_drive_attachment(self):
        result = flu_trend_demo(
            {"id": "epi-1", "role": "Epidemiologist", "tools": ["Excel", "EHR"]}
        )
        self.assertGreaterEqual(result["attachment_count"], 1)
        self.assertEqual(result["chat_ref"] is not None, True)
        self.assertEqual(
            result["recipe"],
            ["ehr", "spreadsheet", "shared_drive", "email", "chat"],
        )
        self.assertIn("ehr", result["tools"])

    def test_workflow_memory_reuses_recipe(self):
        session = build_employee_session({"id": "epi-1", "role": "Epidemiologist"})
        session.memory.remember(["ehr", "spreadsheet", "email"], "email")
        self.assertEqual(session.plan_for("email"), ["ehr", "spreadsheet", "email"])


if __name__ == "__main__":
    unittest.main()

import json
import os
import unittest

from org_structure import (
    assign_members,
    build_org_tree,
    extract_roles_with_units,
    is_lead_role,
    meeting_stats,
    org_fields_for_profile,
    plan_from_company_file,
    plan_meetings,
)


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
GAME_STUDIO = os.path.join(FIXTURE_DIR, "game_studio_15.json")
HOSPITAL_90 = os.path.join(FIXTURE_DIR, "hospital_90.json")


def _load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


class OrgStructureTest(unittest.TestCase):
    def test_lead_role_tokens(self):
        self.assertTrue(is_lead_role("Lead Programmer"))
        self.assertTrue(is_lead_role("Nurse Manager"))
        self.assertTrue(is_lead_role("Hospital Administrator"))
        self.assertFalse(is_lead_role("Client Developers"))

    def test_game_studio_preserves_departments_instead_of_flattening(self):
        config = _load(GAME_STUDIO)
        tree = build_org_tree(config)
        self.assertIn(("core_development_team", "programming_team"), tree)
        self.assertIn(("core_development_team", "design_team"), tree)
        self.assertIn(("support_teams",), tree)
        roles = extract_roles_with_units(config)
        # The Chimera example JSON is labeled "15 people" in the prompt, but the
        # nested role counts actually sum to 20; preserve that real headcount.
        self.assertEqual(sum(role.count for role in roles), 20)
        assignments = assign_members(config)
        self.assertEqual(len(assignments), 20)
        programming = [
            item for item in assignments if item.unit_path[-1] == "programming_team"
        ]
        self.assertEqual(len(programming), 6)
        leads = [item for item in programming if item.is_lead]
        self.assertEqual([item.member_id for item in leads], ["lpro-1"])
        client = next(item for item in programming if item.member_id == "cdev-1")
        self.assertEqual(client.reports_to, "lpro-1")

    def test_org_fields_attach_team_metadata(self):
        assignments = assign_members(_load(GAME_STUDIO))
        lead = next(item for item in assignments if item.member_id == "lpro-1")
        fields = org_fields_for_profile(lead)
        self.assertEqual(fields["department"], "core_development_team")
        self.assertEqual(fields["team"], "programming_team")
        self.assertTrue(fields["is_lead"])

    def test_game_studio_meetings_are_small_and_not_all_hands(self):
        assignments = assign_members(_load(GAME_STUDIO))
        meetings = plan_meetings(assignments, max_group_size=8)
        stats = meeting_stats(meetings)
        self.assertGreaterEqual(stats["meeting_count"], 2)
        self.assertEqual(stats["governance"], 1)
        self.assertLessEqual(stats["max_meeting_size"], 8)
        all_hands = [
            meeting
            for meeting in meetings
            if set(meeting.member_ids) == {item.member_id for item in assignments}
        ]
        self.assertEqual(all_hands, [])
        governance = next(m for m in meetings if m.meeting_id == "governance")
        self.assertLess(len(governance.member_ids), len(assignments))

    def test_hospital_90_never_schedules_all_hands(self):
        plan = plan_from_company_file(HOSPITAL_90, max_group_size=10)
        self.assertEqual(len(plan["assignments"]), 90)
        self.assertLessEqual(plan["stats"]["max_meeting_size"], 10)
        self.assertGreaterEqual(plan["stats"]["meeting_count"], 8)
        self.assertEqual(plan["stats"]["governance"], 1)
        # Current Chimera WeeklyPlan would put all 90 in one Workforce.
        self.assertNotIn(90, [len(m["member_ids"]) for m in plan["meetings"]])
        nursing = next(
            m
            for m in plan["meetings"]
            if m["kind"] == "department"
            and m["unit_path"]
            and m["unit_path"][-1] == "nursing_unit"
        )
        # 21 nurses exceed the cap, so the department meeting is a lead sync.
        self.assertLessEqual(len(nursing["member_ids"]), 10)
        huddles = [
            m
            for m in plan["meetings"]
            if m["kind"] == "huddle"
            and m["unit_path"]
            and m["unit_path"][-1] == "nursing_unit"
        ]
        self.assertGreaterEqual(len(huddles), 2)

    def test_max_group_size_is_enforced(self):
        assignments = assign_members(_load(HOSPITAL_90))
        meetings = plan_meetings(assignments, max_group_size=6)
        self.assertLessEqual(meeting_stats(meetings)["max_meeting_size"], 6)


if __name__ == "__main__":
    unittest.main()

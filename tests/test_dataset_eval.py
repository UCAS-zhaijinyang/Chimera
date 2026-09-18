import os
import unittest

from dataset_eval import run_preliminary_eval, score_org_topology, score_workflow_final_state


FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
HOSPITAL_90 = os.path.join(FIXTURE_DIR, "hospital_90.json")


class DatasetEvalTests(unittest.TestCase):
    def test_l1_flu_chain_passes(self):
        card = score_workflow_final_state()
        failed = [item.name for item in card.checks if not item.passed]
        self.assertEqual(failed, [], failed)
        self.assertEqual(card.passed, card.total)

    def test_l2_hospital_plan_passes(self):
        card = score_org_topology(HOSPITAL_90, max_group_size=10)
        failed = [item.name for item in card.checks if not item.passed]
        self.assertEqual(failed, [], failed)

    def test_scorecard_json_shape(self):
        report = run_preliminary_eval(hospital_path=HOSPITAL_90)
        self.assertTrue(report["all_ok"])
        self.assertEqual(report["passed"], report["total"])
        self.assertEqual(len(report["scorecards"]), 2)
        self.assertIn("L3 distributional fidelity vs CERT / TWOS / old ChimeraLog", report["deferred"])


if __name__ == "__main__":
    unittest.main()

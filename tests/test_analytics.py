import unittest

from src.analytics import evaluate_recommendations, summarize_dataset
from src.data_pipeline import load_dataset
from src.matcher import JobMatcher


class TestAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seekers, cls.opportunities, _ = load_dataset(
            "examples/seekers.json",
            "examples/opportunities.json",
        )

    def test_summary_contains_report_metrics(self):
        summary = summarize_dataset(self.seekers, self.opportunities)
        self.assertEqual(summary["dataset"]["opportunity_count"], 6)
        self.assertIn("Python", summary["top_required_skills"])
        self.assertIn("salary", summary)

    def test_evaluation_contains_top_k_and_timing(self):
        report = evaluate_recommendations(self.seekers, self.opportunities, JobMatcher(), top_k=2)
        self.assertEqual(report["top_k"], 2)
        self.assertGreaterEqual(report["average_match_time_ms"], 0)
        self.assertEqual(len(report["results"]), 4)
        self.assertEqual(len(report["results"][0]["recommendations"]), 2)


if __name__ == "__main__":
    unittest.main()

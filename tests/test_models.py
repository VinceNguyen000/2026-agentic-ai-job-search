"""Unit tests for models.py data structures and serialization."""

import unittest
from src.models import (
    Seeker, Opportunity, MatchResult,
    ExperienceLevel, WorkMode, WorkType
)


class TestModels(unittest.TestCase):

    def test_seeker_creation_and_to_dict(self):
        seeker = Seeker(
            name="Test Candidate",
            email="test@example.com",
            experience_level=ExperienceLevel.SENIOR,
            skills=["Python", "TensorFlow"],
            career_goals=["Lead AI Projects"],
            salary_expectation_min=120000,
            salary_expectation_max=160000,
            work_mode_preference=[WorkMode.REMOTE]
        )
        self.assertEqual(seeker.name, "Test Candidate")
        d = seeker.to_dict()
        self.assertEqual(d["name"], "Test Candidate")
        self.assertEqual(d["experience_level"], "senior")
        self.assertEqual(d["skills"], ["Python", "TensorFlow"])
        self.assertEqual(d["salary_expectation"]["min"], 120000)
        self.assertEqual(d["work_mode_preference"], ["remote"])

    def test_opportunity_creation_and_to_dict(self):
        opp = Opportunity(
            job_id="TEST001",
            title="ML Engineer",
            company="AI Labs",
            required_skills=["Python", "PyTorch"],
            experience_level_required=ExperienceLevel.SENIOR,
            work_mode=WorkMode.REMOTE,
            salary_min=130000,
            salary_max=170000
        )
        self.assertEqual(opp.job_id, "TEST001")
        d = opp.to_dict()
        self.assertEqual(d["job_id"], "TEST001")
        self.assertEqual(d["title"], "ML Engineer")
        self.assertEqual(d["work_mode"], "remote")
        self.assertEqual(d["salary"]["min"], 130000)

    def test_match_result_to_dict(self):
        res = MatchResult(
            seeker_name="Alice",
            job_id="JOB1",
            job_title="Dev",
            company="Acme",
            overall_match_percentage=85.5,
            skill_match_percentage=90.0,
            experience_match_percentage=100.0,
            location_match_percentage=100.0,
            salary_match_percentage=80.0,
            work_mode_match_percentage=100.0,
            work_type_match_percentage=100.0,
            career_goals_match_percentage=75.0,
            matched_skills=["Python"],
            missing_skills=["Go"],
            explanation="Good fit",
            recommendation="Apply now"
        )
        d = res.to_dict()
        self.assertEqual(d["seeker"], "Alice")
        self.assertEqual(d["match_scores"]["overall"], 85.5)
        self.assertEqual(d["skills"]["matched"], ["Python"])


if __name__ == "__main__":
    unittest.main()


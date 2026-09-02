"""Unit tests for JobMatcher class."""

import unittest
from src.models import (
    Seeker, Opportunity, ExperienceLevel, WorkMode, WorkType
)
from src.matcher import JobMatcher


class TestJobMatcher(unittest.TestCase):

    def setUp(self):
        self.seeker = Seeker(
            name="Alice",
            experience_level=ExperienceLevel.SENIOR,
            skills=["Python", "Machine Learning", "TensorFlow"],
            preferred_locations=["San Francisco, CA"],
            willing_to_relocate=True,
            work_mode_preference=[WorkMode.REMOTE],
            work_type_preference=[WorkType.FULL_TIME],
            salary_expectation_min=150000,
            salary_expectation_max=200000,
            career_goals=["Lead machine learning research"]
        )
        
        self.opp1 = Opportunity(
            job_id="J1",
            title="Senior ML Engineer",
            company="AI Corp",
            description="Lead our machine learning research team",
            required_skills=["Python", "Machine Learning"],
            experience_level_required=ExperienceLevel.SENIOR,
            locations=["San Francisco, CA"],
            work_mode=WorkMode.REMOTE,
            work_type=WorkType.FULL_TIME,
            salary_min=160000,
            salary_max=210000
        )
        
        self.opp2 = Opportunity(
            job_id="J2",
            title="Junior Frontend Developer",
            company="Web Corp",
            required_skills=["JavaScript", "React"],
            experience_level_required=ExperienceLevel.ENTRY,
            locations=["New York, NY"],
            work_mode=WorkMode.ONSITE,
            work_type=WorkType.FULL_TIME,
            salary_min=70000,
            salary_max=90000
        )
        self.matcher = JobMatcher()

    def test_matcher_weights_sum_to_one(self):
        total_weight = sum(self.matcher.WEIGHTS.values())
        self.assertAlmostEqual(total_weight, 1.0, places=5)

    def test_calculate_match_high_compatibility(self):
        result = self.matcher.calculate_match(self.seeker, self.opp1)
        self.assertGreaterEqual(result.overall_match_percentage, 85.0)
        self.assertEqual(result.skill_match_percentage, 100.0)
        self.assertEqual(result.experience_match_percentage, 100.0)
        self.assertIn("Python", result.matched_skills)

    def test_rank_opportunities(self):
        ranked = self.matcher.rank_opportunities(self.seeker, [self.opp1, self.opp2], min_match_threshold=0.0)
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0].job_id, "J1")
        self.assertEqual(ranked[1].job_id, "J2")
        self.assertGreater(ranked[0].overall_match_percentage, ranked[1].overall_match_percentage)


if __name__ == "__main__":
    unittest.main()


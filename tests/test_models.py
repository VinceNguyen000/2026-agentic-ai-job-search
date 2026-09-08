"""Unit tests for models.py data structures and serialization."""

import unittest
from src.models import (
    Seeker, Opportunity, MatchResult,
    ExperienceLevel, WorkMode, WorkType
)


class TestModels(unittest.TestCase):

    def test_seeker_creation_and_to_dict(self):
        seeker = Seeker(
            name="Vince Nguyen",
            email="vincenguyen2712@gmail.com",
            experience_level=ExperienceLevel.JUNIOR,
            skills=["Wireshark", "Nmap", "Python"],
            career_goals=["SOC Analyst"],
            salary_expectation_min=75000,
            salary_expectation_max=95000,
            work_mode_preference=[WorkMode.REMOTE, WorkMode.HYBRID]
        )
        self.assertEqual(seeker.name, "Vince Nguyen")
        d = seeker.to_dict()
        self.assertEqual(d["name"], "Vince Nguyen")
        self.assertEqual(d["experience_level"], "junior")
        self.assertEqual(d["skills"], ["Wireshark", "Nmap", "Python"])
        self.assertEqual(d["salary_expectation"]["min"], 75000)

    def test_opportunity_creation_and_to_dict(self):
        opp = Opportunity(
            job_id="JOB_TEST",
            title="Cybersecurity Analyst",
            company="Enterprise Corp",
            required_skills=["Wireshark", "Nmap"],
            experience_level_required=ExperienceLevel.JUNIOR,
            work_mode=WorkMode.HYBRID,
            salary_min=80000,
            salary_max=100000
        )
        self.assertEqual(opp.job_id, "JOB_TEST")
        d = opp.to_dict()
        self.assertEqual(d["job_id"], "JOB_TEST")
        self.assertEqual(d["title"], "Cybersecurity Analyst")
        self.assertEqual(d["work_mode"], "hybrid")
        self.assertEqual(d["salary"]["min"], 80000)

    def test_match_result_to_dict(self):
        res = MatchResult(
            seeker_name="Vince",
            job_id="JOB_TEST",
            job_title="SOC Analyst",
            company="Enterprise Corp",
            overall_match_percentage=90.0,
            skill_match_percentage=95.0,
            experience_match_percentage=100.0,
            location_match_percentage=100.0,
            salary_match_percentage=85.0,
            work_mode_match_percentage=100.0,
            work_type_match_percentage=100.0,
            career_goals_match_percentage=80.0,
            matched_skills=["Wireshark", "Python"],
            missing_skills=["Splunk"],
            explanation="Strong fit",
            recommendation="Apply now"
        )
        d = res.to_dict()
        self.assertEqual(d["seeker"], "Vince")
        self.assertEqual(d["match_scores"]["overall"], 90.0)
        self.assertEqual(d["skills"]["matched"], ["Wireshark", "Python"])


if __name__ == "__main__":
    unittest.main()

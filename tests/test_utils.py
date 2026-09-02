"""Unit tests for utils.py helper functions."""

import unittest
from src.utils import (
    calculate_skill_match,
    calculate_experience_match,
    calculate_salary_match,
    skill_matches,
    get_missing_skills,
    keyword_match_percentage
)


class TestUtils(unittest.TestCase):

    def test_skill_matches_variations(self):
        self.assertTrue(skill_matches("js", "JavaScript"))
        self.assertTrue(skill_matches("JavaScript", "js"))
        self.assertTrue(skill_matches("py", "Python"))
        self.assertTrue(skill_matches("ML", "Machine Learning"))
        self.assertFalse(skill_matches("Docker", "Kubernetes"))

    def test_calculate_skill_match(self):
        seeker = ["Python", "JS", "SQL"]
        required = ["Python", "JavaScript", "Docker"]
        preferred = ["SQL"]
        
        score, matched, missing = calculate_skill_match(seeker, required, preferred)
        self.assertEqual(len(matched), 2)  # Python and JS
        self.assertEqual(missing, ["Docker"])
        self.assertGreater(score, 75.0)

    def test_calculate_experience_match(self):
        self.assertEqual(calculate_experience_match("senior", "junior"), 100.0)
        self.assertLess(calculate_experience_match("junior", "senior"), 100.0)
        self.assertEqual(calculate_experience_match("entry", "entry"), 100.0)

    def test_calculate_salary_match(self):
        # Full overlap
        self.assertEqual(calculate_salary_match(100000, 150000, 100000, 150000), 100.0)
        # Partial overlap
        match = calculate_salary_match(100000, 150000, 125000, 175000)
        self.assertEqual(match, 50.0)
        # No overlap
        self.assertEqual(calculate_salary_match(100000, 120000, 130000, 160000), 0.0)

    def test_keyword_match_percentage_containment(self):
        goal = "Work on AI/ML projects"
        job_desc = "Senior Machine Learning Engineer at TechCorp AI building production AI models."
        score = keyword_match_percentage(goal, job_desc)
        self.assertGreaterEqual(score, 50.0)


if __name__ == "__main__":
    unittest.main()


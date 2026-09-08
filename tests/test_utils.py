import unittest
from src.utils import (
    calculate_skill_match,
    calculate_experience_match,
    calculate_location_match,
    calculate_salary_match,
    keyword_match_percentage,
    extract_keywords,
    skill_matches
)

class TestUtils(unittest.TestCase):
    def test_skill_matches(self):
        self.assertTrue(skill_matches('python', 'Python Programming'))
        self.assertTrue(skill_matches('machine learning', 'ml'))
        self.assertTrue(skill_matches('ai', 'Artificial Intelligence'))
        self.assertFalse(skill_matches('javascript', 'python'))

    def test_calculate_skill_match(self):
        seeker = ['Python', 'SQL', 'Wireshark']
        required = ['Python', 'SQL']
        score, matched, missing = calculate_skill_match(seeker, required)
        self.assertEqual(score, 100.0)
        self.assertEqual(len(missing), 0)

    def test_calculate_experience_match(self):
        self.assertEqual(calculate_experience_match('junior', 'junior'), 100.0)
        self.assertEqual(calculate_experience_match('senior', 'junior'), 100.0)
        self.assertLess(calculate_experience_match('entry', 'senior'), 70.0)

    def test_calculate_location_match(self):
        self.assertEqual(calculate_location_match(['Kansas City, MO'], ['Kansas City, MO']), 100.0)
        self.assertEqual(calculate_location_match(['Remote'], ['New York, NY'], willing_to_relocate=True), 80.0)

    def test_calculate_salary_match(self):
        self.assertEqual(calculate_salary_match(80000, 100000, 85000, 95000), 100.0)
        self.assertEqual(calculate_salary_match(50000, 60000, 90000, 100000), 0.0)

    def test_keyword_match_percentage(self):
        score = keyword_match_percentage(['Work in AI and Security'], 'Seeking AI security analyst')
        self.assertGreater(score, 40.0)

if __name__ == '__main__':
    unittest.main()

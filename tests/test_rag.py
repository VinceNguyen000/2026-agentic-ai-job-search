import unittest

from src.models import Opportunity, Seeker, ExperienceLevel, WorkMode, WorkType
from src.rag import PersonalKnowledgeBase, hard_gate_opportunity


class TestPersonalRAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.knowledge_base = PersonalKnowledgeBase.from_directory("data/personal")

    def test_builds_personal_chunks_and_dense_index(self):
        self.assertGreaterEqual(len(self.knowledge_base.chunks), 10)
        self.assertEqual(self.knowledge_base.encoder.dimensions, 256)
        self.assertEqual(len(self.knowledge_base.vectors), len(self.knowledge_base.chunks))

    def test_hybrid_retrieval_returns_security_evidence(self):
        results = self.knowledge_base.retrieve("Wireshark vulnerability management NIST", top_k=3)
        self.assertEqual(len(results), 3)
        self.assertIn("Wireshark", results[0].chunk.text)
        self.assertGreaterEqual(results[0].hybrid_score, results[-1].hybrid_score)

    def test_hard_gate_rejects_incompatible_salary(self):
        seeker = Seeker(
            name="Candidate",
            salary_expectation_min=75000,
            work_mode_preference=[WorkMode.REMOTE],
            work_type_preference=[WorkType.FULL_TIME],
            experience_level=ExperienceLevel.JUNIOR,
        )
        opportunity = Opportunity(
            job_id="JOB_GATE",
            title="Low Salary Role",
            company="Example",
            salary_min=50000,
            salary_max=60000,
            work_mode=WorkMode.REMOTE,
            work_type=WorkType.FULL_TIME,
        )
        eligible, reasons = hard_gate_opportunity(seeker, opportunity)
        self.assertFalse(eligible)
        self.assertIn("salary maximum is below seeker minimum", reasons)


if __name__ == "__main__":
    unittest.main()

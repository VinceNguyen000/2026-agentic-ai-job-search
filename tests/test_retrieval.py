import unittest

from src.data_pipeline import load_dataset
from src.matcher import JobMatcher
from src.retrieval import BM25Retriever, HybridRetriever


class TestRetrieval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seekers, cls.opportunities, _ = load_dataset(
            "local-data/seekers.json",
            "local-data/opportunities.json",
        )

    def test_bm25_retrieves_relevant_machine_learning_job(self):
        retriever = BM25Retriever(self.opportunities)
        results = retriever.retrieve("machine learning Python", top_k=1)
        self.assertEqual(results[0][0].job_id, "JOB001")
        self.assertGreater(results[0][1], 0)

    def test_hybrid_reranking_returns_match_results(self):
        retriever = HybridRetriever(self.opportunities)
        results = retriever.rerank(self.seekers[0], JobMatcher(), top_k=3)
        self.assertEqual(len(results), 3)
        self.assertIn("match_result", results[0])
        self.assertIn("retrieval_score", results[0])


if __name__ == "__main__":
    unittest.main()

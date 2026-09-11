import unittest

from src.data_pipeline import load_dataset


class TestDataPipeline(unittest.TestCase):
    def test_load_example_dataset(self):
        seekers, opportunities, quality = load_dataset(
            "local-data/seekers.json",
            "local-data/opportunities.json",
        )
        self.assertEqual(len(seekers), 4)
        self.assertEqual(len(opportunities), 6)
        self.assertEqual(quality["seekers"]["duplicate_keys"], [])
        self.assertEqual(quality["opportunities"]["missing_fields"], {})
        self.assertEqual(seekers[0].experience_level.value, "senior")
        self.assertEqual(opportunities[0].work_mode.value, "remote")


if __name__ == "__main__":
    unittest.main()

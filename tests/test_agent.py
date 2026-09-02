"""Unit tests for JobSearchAgent tool execution and autonomous workflows."""

import unittest
from src.models import (
    Seeker, Opportunity, ExperienceLevel, WorkMode, WorkType
)
from src.agent import JobSearchAgent


class TestJobSearchAgent(unittest.TestCase):

    def setUp(self):
        self.seeker = Seeker(
            name="Bob Smith",
            experience_level=ExperienceLevel.JUNIOR,
            skills=["JavaScript", "React", "Node.js"],
            salary_expectation_min=80000,
            salary_expectation_max=120000,
            work_mode_preference=[WorkMode.REMOTE, WorkMode.HYBRID]
        )
        
        self.opp1 = Opportunity(
            job_id="JOB_JS",
            title="Full Stack JS Dev",
            company="StartUp Inc",
            required_skills=["JavaScript", "React", "Node.js"],
            experience_level_required=ExperienceLevel.JUNIOR,
            work_mode=WorkMode.REMOTE,
            salary_min=90000,
            salary_max=130000
        )
        
        self.opp2 = Opportunity(
            job_id="JOB_DEVOPS",
            title="DevOps Engineer",
            company="CloudScale",
            required_skills=["AWS", "Docker", "Kubernetes"],
            experience_level_required=ExperienceLevel.SENIOR,
            work_mode=WorkMode.ONSITE,
            salary_min=140000,
            salary_max=180000
        )
        
        self.agent = JobSearchAgent(seekers=[self.seeker], opportunities=[self.opp1, self.opp2])

    def test_agent_tool_search_opportunities(self):
        res = self.agent.tool_search_opportunities(work_mode="remote")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["job_id"], "JOB_JS")

    def test_agent_tool_evaluate_fit(self):
        res = self.agent.tool_evaluate_fit("Bob Smith", "JOB_JS")
        self.assertNotIn("error", res)
        self.assertGreaterEqual(res["match_scores"]["overall"], 80.0)

    def test_agent_tool_analyze_skill_gaps(self):
        res = self.agent.tool_analyze_skill_gaps("Bob Smith", "JOB_DEVOPS")
        self.assertNotIn("error", res)
        self.assertIn("AWS", res["missing_required_skills"])
        self.assertGreater(len(res["remediation_plan"]), 0)

    def test_agent_tool_draft_tailored_application(self):
        res = self.agent.tool_draft_tailored_application("Bob Smith", "JOB_JS")
        self.assertIn("cover_letter", res)
        self.assertIn("StartUp Inc", res["cover_letter"])
        self.assertIn("elevator_pitch", res)

    def test_agent_tool_generate_upskilling_roadmap(self):
        res = self.agent.tool_generate_upskilling_roadmap("Bob Smith")
        self.assertIn("roadmap", res)
        self.assertEqual(len(res["roadmap"]), 3)

    def test_agent_run_goal(self):
        goal = "Help Bob Smith find matching roles and draft application."
        response = self.agent.run_goal(goal, seeker_name="Bob Smith")
        
        self.assertEqual(response.goal, goal)
        self.assertGreaterEqual(len(response.actions), 5)
        self.assertIn("AUTONOMOUS JOB SEARCH AGENT REPORT", response.final_synthesis)
        self.assertIn("tailored_application", response.artifacts)
        self.assertIn("upskilling_roadmap", response.artifacts)


if __name__ == "__main__":
    unittest.main()


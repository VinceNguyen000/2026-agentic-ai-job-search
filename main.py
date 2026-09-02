#!/usr/bin/env python3
"""
Agentic AI Job Search System - Main Entry Point.
Demonstrates autonomous multi-agent matching, tool execution, and application drafting.

Author: Antigravity Agentic AI for CS5542 Challenge 1
"""

import json
import sys
import argparse
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import (
    Seeker, Opportunity, ExperienceLevel, WorkMode, WorkType
)
from src.matcher import JobMatcher
from src.agent import JobSearchAgent
from src.utils import format_match_report


def load_example_data():
    """Load example seekers and opportunities from JSON files."""
    with open('examples/seekers.json', 'r') as f:
        seekers_data = json.load(f)
    
    with open('examples/opportunities.json', 'r') as f:
        opportunities_data = json.load(f)
    
    seekers = []
    for seeker_dict in seekers_data['seekers']:
        seeker = Seeker(
            name=seeker_dict['name'],
            email=seeker_dict.get('email'),
            phone=seeker_dict.get('phone'),
            career_goals=seeker_dict.get('career_goals', []),
            industry_interests=seeker_dict.get('industry_interests', []),
            experience_level=ExperienceLevel(seeker_dict['experience_level']),
            skills=seeker_dict.get('skills', []),
            certifications=seeker_dict.get('certifications', []),
            education=seeker_dict.get('education', ''),
            preferred_locations=seeker_dict.get('preferred_locations', []),
            willing_to_relocate=seeker_dict.get('willing_to_relocate', False),
            work_mode_preference=[WorkMode(m) for m in seeker_dict.get('work_mode_preference', [])],
            work_type_preference=[WorkType(t) for t in seeker_dict.get('work_type_preference', [])],
            salary_expectation_min=seeker_dict.get('salary_expectation', {}).get('min'),
            salary_expectation_max=seeker_dict.get('salary_expectation', {}).get('max'),
            availability_days=seeker_dict.get('availability_days')
        )
        seekers.append(seeker)
    
    opportunities = []
    for job_dict in opportunities_data['opportunities']:
        opportunity = Opportunity(
            job_id=job_dict['job_id'],
            title=job_dict['title'],
            company=job_dict['company'],
            description=job_dict.get('description'),
            responsibilities=job_dict.get('responsibilities', []),
            required_skills=job_dict.get('required_skills', []),
            preferred_skills=job_dict.get('preferred_skills', []),
            experience_level_required=ExperienceLevel(job_dict['experience_level_required']),
            experience_years_required=job_dict.get('experience_years_required', 0),
            education_required=job_dict.get('education_required'),
            certifications_required=job_dict.get('certifications_required', []),
            locations=job_dict.get('locations', []),
            allows_relocation=job_dict.get('allows_relocation', False),
            work_mode=WorkMode(job_dict['work_mode']),
            work_type=WorkType(job_dict['work_type']),
            salary_min=job_dict.get('salary', {}).get('min'),
            salary_max=job_dict.get('salary', {}).get('max'),
            benefits=job_dict.get('benefits', []),
            posted_date=job_dict.get('posted_date'),
            application_deadline=job_dict.get('application_deadline')
        )
        opportunities.append(opportunity)
    
    return seekers, opportunities


def run_agent_demo(agent: JobSearchAgent):
    """Run an autonomous multi-step agent goal execution."""
    print("=" * 80)
    print("RUNNING AUTONOMOUS JOB SEARCH AGENT DEMONSTRATION")
    print("=" * 80)
    
    goal = "Help Alice Johnson find the highest-paying machine learning engineering position, evaluate skill fit, draft a customized cover letter, and generate an upskilling roadmap."
    print(f"\nUser Goal: \"{goal}\"\n")
    print("Agent is reasoning and executing tools...")
    
    response = agent.run_goal(goal, seeker_name="Alice Johnson")
    
    print("\n" + "-" * 80)
    print(f"AGENT EXECUTION TRACE ({len(response.actions)} STEPS)")
    print("-" * 80)
    for action in response.actions:
        print(f"\n[Step {action.step}]")
        print(f"  Thought: {action.thought}")
        print(f"  Tool Call: {action.tool_name}({json.dumps(action.tool_args)})")
        summary_obs = str(action.observation)
        if len(summary_obs) > 120:
            summary_obs = summary_obs[:117] + "..."
        print(f"  Observation: {summary_obs}")
    
    print("\n" + response.final_synthesis)
    
    # Save agent output to results folder
    output_path = Path("results/sample_agent_output.json")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(response.to_dict(), f, indent=2)
    print(f"\n[+] Saved full agent execution trace and artifacts to: {output_path}")


def run_matching_demo(seekers, opportunities):
    """Run the 7-criterion algorithmic matching demonstration."""
    print("=" * 80)
    print("RUNNING 7-CRITERION MATCHING ENGINE DEMONSTRATION")
    print("=" * 80)
    
    matcher = JobMatcher()
    seeker = seekers[0]
    print(f"\nMatching opportunities for: {seeker.name}")
    print("-" * 80)
    
    ranked_matches = matcher.rank_opportunities(seeker, opportunities, min_match_threshold=30)
    print(f"Found {len(ranked_matches)} matching opportunities (threshold: 30%)\n")
    
    for i, match in enumerate(ranked_matches, 1):
        print(f"{i}. {match.job_title} at {match.company}")
        print(f"   Job ID: {match.job_id}")
        print(f"   Overall Match: {match.overall_match_percentage}% | Skills: {match.skill_match_percentage}% | Exp: {match.experience_match_percentage}% | Location: {match.location_match_percentage}% | Salary: {match.salary_match_percentage}%")
        print(f"   Matched Skills: {', '.join(match.matched_skills) if match.matched_skills else 'None'}")
        print(f"   Missing Skills: {', '.join(match.missing_skills) if match.missing_skills else 'None'}")
        print(f"   Recommendation: {match.recommendation}")
        print()
    
    if ranked_matches:
        print("\nDETAILED REPORT FOR TOP MATCH:")
        print(format_match_report(ranked_matches[0]))


def main():
    parser = argparse.ArgumentParser(description="Agentic AI Job Search System")
    parser.add_argument("--agent", action="store_true", help="Run autonomous agent demonstration")
    parser.add_argument("--matcher", action="store_true", help="Run algorithmic matcher demonstration")
    parser.add_argument("--goal", type=str, help="Custom goal for the autonomous agent to solve")
    parser.add_argument("--seeker", type=str, default=None, help="Target seeker name for custom goal")
    args = parser.parse_args()

    seekers, opportunities = load_example_data()
    agent = JobSearchAgent(seekers, opportunities)

    if args.goal:
        print("=" * 80)
        print("RUNNING CUSTOM AGENT GOAL")
        print("=" * 80)
        print(f"Goal: {args.goal}")
        res = agent.run_goal(args.goal, seeker_name=args.seeker)
        print(res.final_synthesis)
        return

    if args.agent:
        run_agent_demo(agent)
    elif args.matcher:
        run_matching_demo(seekers, opportunities)
    else:
        # Run full pipeline by default
        run_matching_demo(seekers, opportunities)
        print("\n\n")
        run_agent_demo(agent)


if __name__ == "__main__":
    main()


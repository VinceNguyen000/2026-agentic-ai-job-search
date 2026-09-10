#!/usr/bin/env python3
"""
Example usage of the Job Matching System.
Demonstrates how to use the matcher to rank job opportunities for a seeker.
Agentic AI Job Search System - Main Entry Point.
Demonstrates autonomous multi-agent matching, tool execution, and application drafting.

Author: Agentic AI Project for CS5542 Challenge 1
Author: Vince Nguyen / Antigravity Agentic AI for CS5542 Challenge 1
"""

import json
import sys
import argparse
from pathlib import Path

# Add src directory to path
# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import (
    Seeker, Opportunity, ExperienceLevel, WorkMode, WorkType
)
from src.matcher import JobMatcher
from src.agent import JobSearchAgent
from src.utils import format_match_report
from src.analytics import (
    create_visualization,
    evaluate_hybrid_retrieval,
    evaluate_recommendations,
    save_json,
    summarize_dataset,
)
from src.data_pipeline import load_dataset


def load_example_data():
    """Load the curated example dataset through the shared data pipeline."""
    seekers, opportunities, _ = load_dataset(
        "examples/seekers.json",
        "examples/opportunities.json",
    )
    return seekers, opportunities


def run_analytics(seekers, opportunities, include_hybrid=False):
    """Generate report artifacts for reproducible dataset analysis."""
    summary = summarize_dataset(seekers, opportunities)
    save_json(summary, "results/analytics_report.json")
    create_visualization(summary, "results/analytics_summary.png")

    matcher = JobMatcher()
    evaluation = evaluate_recommendations(seekers, opportunities, matcher)
    save_json(evaluation, "results/evaluation_report.json")

    print(json.dumps(summary, indent=2))
    print(f"Saved results/analytics_report.json and results/analytics_summary.png")
    print(f"Saved results/evaluation_report.json (average match time: {evaluation['average_match_time_ms']} ms)")

    if include_hybrid:
        hybrid = evaluate_hybrid_retrieval(seekers, opportunities, matcher)
        save_json(hybrid, "results/hybrid_retrieval_report.json")
        print("Saved results/hybrid_retrieval_report.json")


def main():
    """Main function demonstrating the job matching system."""
def run_agent_goal(agent: JobSearchAgent, goal: str, seeker_name: str = None):
    """Run an autonomous multi-step agent goal execution."""
    print("=" * 80)
    print("AUTONOMOUS JOB SEARCH AGENT EXECUTION")
    print("=" * 80)
    print(f"\nUser Goal: \"{goal}\"\n")
    print("Agent is reasoning and executing tools...")
    
    response = agent.run_goal(goal, seeker_name=seeker_name)
    
    print("\n" + "-" * 80)
    print(f"AGENT EXECUTION TRACE ({len(response.actions)} ACTIONS TAKEN)")
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
    
    output_path = Path("results/sample_agent_output.json")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(response.to_dict(), f, indent=2)
    print(f"\n[+] Saved full agent execution trace and artifacts to: {output_path}")


def run_matching_demo(seekers, opportunities, seeker_name=None):
    """Run the 7-criterion algorithmic matching demonstration."""
    print("=" * 80)
    print("Agentic AI Job Search Matching System")
    print("Example Usage Demonstration")
    print("RUNNING 7-CRITERION MATCHING ENGINE DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Load example data
    print("Loading example data...")
    seekers, opportunities = load_example_data()
    print(f"  - Loaded {len(seekers)} seekers")
    print(f"  - Loaded {len(opportunities)} opportunities")
    print()
    
    # Initialize matcher
    matcher = JobMatcher()
    
    # Match first seeker with all opportunities
    seeker = seekers[0]
    print(f"Matching opportunities for: {seeker.name}")
    target_seeker = next((s for s in seekers if seeker_name and seeker_name.lower() in s.name.lower()), seekers[0])
    print(f"\nMatching opportunities for: {target_seeker.name}")
    print("-" * 80)
    print()
    
    # Rank all opportunities for this seeker
    ranked_matches = matcher.rank_opportunities(seeker, opportunities, min_match_threshold=30)
    ranked_matches = matcher.rank_opportunities(target_seeker, opportunities, min_match_threshold=30)
    print(f"Found {len(ranked_matches)} matching opportunities (threshold: 30%)\n")
    
    # Display results
    print(f"Found {len(ranked_matches)} matching opportunities (threshold: 30%)")
    print()
    
    for i, match in enumerate(ranked_matches, 1):
        print(f"{i}. {match.job_title} at {match.company}")
        print(f"   Job ID: {match.job_id}")
        print(f"   Overall Match: {match.overall_match_percentage}%")
        print(f"   Skills Match: {match.skill_match_percentage}%")
        print(f"   Experience Match: {match.experience_match_percentage}%")
        print(f"   Location Match: {match.location_match_percentage}%")
        print(f"   Salary Match: {match.salary_match_percentage}%")
        print()
        print(f"   Overall Match: {match.overall_match_percentage}% | Skills: {match.skill_match_percentage}% | Exp: {match.experience_match_percentage}% | Loc: {match.location_match_percentage}% | Salary: {match.salary_match_percentage}%")
        print(f"   Matched Skills: {', '.join(match.matched_skills) if match.matched_skills else 'None'}")
        print(f"   Missing Skills: {', '.join(match.missing_skills) if match.missing_skills else 'None'}")
        print()
        print(f"   Recommendation: {match.recommendation}")
        print()
        print("-" * 80)
        print()
    
    # Generate detailed report for top match
    if ranked_matches:
        print()
        print("DETAILED REPORT FOR TOP MATCH:")
        print("\nDETAILED REPORT FOR TOP MATCH:")
        print(format_match_report(ranked_matches[0]))


def main():
    parser = argparse.ArgumentParser(description="Agentic AI Job Search System")
    parser.add_argument("--agent", action="store_true", help="Run autonomous agent demonstration")
    parser.add_argument("--matcher", action="store_true", help="Run algorithmic matcher demonstration")
    parser.add_argument("--analytics", action="store_true", help="Generate dataset analytics and visualization artifacts")
    parser.add_argument("--hybrid", action="store_true", help="Evaluate BM25 retrieval with weighted reranking")
    parser.add_argument("--goal", type=str, help="Custom goal for the autonomous agent to solve")
    parser.add_argument("--seeker", type=str, default="Vince Nguyen", help="Target seeker name for matching/agent")
    args = parser.parse_args()

    seekers, opportunities = load_example_data()
    agent = JobSearchAgent(seekers, opportunities)

    if args.analytics or args.hybrid:
        run_analytics(seekers, opportunities, include_hybrid=args.hybrid)
    elif args.goal:
        run_agent_goal(agent, args.goal, seeker_name=args.seeker)
    elif args.agent:
        default_goal = f"Help {args.seeker} find the best cybersecurity SOC / vulnerability management opportunity, evaluate fit, draft a tailored cover letter, and generate an upskilling roadmap."
        run_agent_goal(agent, default_goal, seeker_name=args.seeker)
    elif args.matcher:
        run_matching_demo(seekers, opportunities, seeker_name=args.seeker)
    else:
        # Full demonstration by default
        run_matching_demo(seekers, opportunities, seeker_name=args.seeker)
        print("\n\n")
        default_goal = f"Help {args.seeker} find the best cybersecurity SOC / vulnerability management opportunity, evaluate fit, draft a tailored cover letter, and generate an upskilling roadmap."
        run_agent_goal(agent, default_goal, seeker_name=args.seeker)


if __name__ == "__main__":
    main()


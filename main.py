#!/usr/bin/env python3
"""
Example usage of the Job Matching System.
Demonstrates how to use the matcher to rank job opportunities for a seeker.

Author: Agentic AI Project for CS5542 Challenge 1
"""

import json
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import (
    Seeker, Opportunity, ExperienceLevel, WorkMode, WorkType
)
from src.matcher import JobMatcher
from src.utils import format_match_report


def load_example_data():
    """Load example seekers and opportunities."""
    
    # Load from JSON files
    with open('examples/seekers.json', 'r') as f:
        seekers_data = json.load(f)
    
    with open('examples/opportunities.json', 'r') as f:
        opportunities_data = json.load(f)
    
    # Convert to model objects
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


def main():
    """Main function demonstrating the job matching system."""
    
    print("=" * 80)
    print("Agentic AI Job Search Matching System")
    print("Example Usage Demonstration")
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
    print("-" * 80)
    print()
    
    # Rank all opportunities for this seeker
    ranked_matches = matcher.rank_opportunities(seeker, opportunities, min_match_threshold=30)
    
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
        print(format_match_report(ranked_matches[0]))


if __name__ == "__main__":
    main()

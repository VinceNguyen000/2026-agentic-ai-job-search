"""
Agentic AI Job Search Matching System

A hands-on project demonstrating the use of Agentic AI for designing,
implementing, and documenting a sophisticated job matching algorithm.

Author: Developed with Agentic AI assistance for CS5542 Challenge 1
Date: 2026
"""

__version__ = "1.0.0"
__author__ = "Agentic AI Project"

from src.models import (
    Seeker,
    Opportunity,
    MatchResult,
    ExperienceLevel,
    WorkMode,
    WorkType
)

from src.matcher import JobMatcher
from src.agent import JobSearchAgent

from src.utils import (
    calculate_skill_match,
    calculate_experience_match,
    calculate_salary_match,
    format_match_report
)

__all__ = [
    "Seeker",
    "Opportunity",
    "MatchResult",
    "ExperienceLevel",
    "WorkMode",
    "WorkType",
    "JobMatcher",
    "JobSearchAgent",
    "calculate_skill_match",
    "calculate_experience_match",
    "calculate_salary_match",
    "format_match_report"
]

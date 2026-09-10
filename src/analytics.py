"""Dataset analytics, evaluation, and visual evidence generation."""

from collections import Counter
import json
from pathlib import Path
import time
from typing import Any, Dict, List, Sequence

from src.matcher import JobMatcher
from src.models import Opportunity, Seeker
from src.retrieval import HybridRetriever


def summarize_dataset(seekers: Sequence[Seeker], opportunities: Sequence[Opportunity]) -> Dict[str, Any]:
    """Produce descriptive statistics used by the report and dashboard."""
    skills = Counter(skill.strip() for opportunity in opportunities for skill in opportunity.required_skills)
    titles = Counter(opportunity.title for opportunity in opportunities)
    locations = Counter(location for opportunity in opportunities for location in opportunity.locations)
    work_modes = Counter(opportunity.work_mode.value for opportunity in opportunities)
    experience_levels = Counter(opportunity.experience_level_required.value for opportunity in opportunities)
    salaries = [
        opportunity.salary_min
        for opportunity in opportunities
        if opportunity.salary_min is not None
    ]
    salary_maxes = [
        opportunity.salary_max
        for opportunity in opportunities
        if opportunity.salary_max is not None
    ]

    return {
        "dataset": {
            "seeker_count": len(seekers),
            "opportunity_count": len(opportunities),
            "required_skill_count": sum(len(opportunity.required_skills) for opportunity in opportunities),
        },
        "top_required_skills": dict(skills.most_common(10)),
        "job_titles": dict(titles.most_common()),
        "locations": dict(locations.most_common()),
        "work_modes": dict(work_modes),
        "experience_levels": dict(experience_levels),
        "salary": {
            "minimum_average": round(sum(salaries) / len(salaries), 2) if salaries else None,
            "maximum_average": round(sum(salary_maxes) / len(salary_maxes), 2) if salary_maxes else None,
            "minimum_observed": min(salaries) if salaries else None,
            "maximum_observed": max(salary_maxes) if salary_maxes else None,
        },
    }


def evaluate_recommendations(
    seekers: Sequence[Seeker],
    opportunities: Sequence[Opportunity],
    matcher: JobMatcher,
    top_k: int = 5,
) -> Dict[str, Any]:
    """Evaluate recommendation output and record reproducible timings."""
    all_results: List[Dict[str, Any]] = []
    elapsed_ms: List[float] = []
    for seeker in seekers:
        start = time.perf_counter()
        ranked = matcher.rank_opportunities(seeker, opportunities, min_match_threshold=0.0)
        elapsed_ms.append((time.perf_counter() - start) * 1000)
        all_results.append(
            {
                "seeker": seeker.name,
                "recommendations": [
                    {
                        "job_id": result.job_id,
                        "title": result.job_title,
                        "company": result.company,
                        "overall_match": result.overall_match_percentage,
                        "skills_match": result.skill_match_percentage,
                        "missing_skills": result.missing_skills,
                    }
                    for result in ranked[:top_k]
                ],
            }
        )

    return {
        "method": "seven-factor weighted matcher",
        "seeker_count": len(seekers),
        "opportunity_count": len(opportunities),
        "top_k": top_k,
        "average_match_time_ms": round(sum(elapsed_ms) / len(elapsed_ms), 4) if elapsed_ms else 0.0,
        "max_match_time_ms": round(max(elapsed_ms), 4) if elapsed_ms else 0.0,
        "results": all_results,
    }


def evaluate_hybrid_retrieval(
    seekers: Sequence[Seeker],
    opportunities: Sequence[Opportunity],
    matcher: JobMatcher,
    top_k: int = 5,
) -> Dict[str, Any]:
    """Evaluate BM25 retrieval followed by weighted reranking."""
    retriever = HybridRetriever(opportunities)
    results = []
    for seeker in seekers:
        reranked = retriever.rerank(seeker, matcher, top_k=top_k)
        results.append(
            {
                "seeker": seeker.name,
                "recommendations": [
                    {
                        "job_id": item["match_result"].job_id,
                        "title": item["match_result"].job_title,
                        "match_score": item["match_result"].overall_match_percentage,
                        "bm25_score": item["bm25_score"],
                        "retrieval_score": item["retrieval_score"],
                    }
                    for item in reranked
                ],
            }
        )
    return {"method": "BM25 retrieval plus seven-factor reranking", "top_k": top_k, "results": results}


def save_json(payload: Dict[str, Any], output_path: str) -> None:
    """Write an analytics or evaluation artifact."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def create_visualization(summary: Dict[str, Any], output_path: str) -> str:
    """Create a compact four-panel PNG for the report."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("Visualization requires matplotlib; install requirements.txt") from exc

    figure, axes = plt.subplots(2, 2, figsize=(12, 8))
    figure.suptitle("Job Search Dataset Analytics", fontsize=16)

    skills = summary["top_required_skills"]
    axes[0, 0].barh(list(reversed(list(skills.keys()))), list(reversed(list(skills.values()))), color="#176b87")
    axes[0, 0].set_title("Most Requested Required Skills")
    axes[0, 0].set_xlabel("Number of postings")

    modes = summary["work_modes"]
    axes[0, 1].bar(list(modes.keys()), list(modes.values()), color="#e07a5f")
    axes[0, 1].set_title("Work Mode Distribution")
    axes[0, 1].set_ylabel("Number of postings")

    levels = summary["experience_levels"]
    axes[1, 0].bar(list(levels.keys()), list(levels.values()), color="#3d9970")
    axes[1, 0].set_title("Required Experience Levels")
    axes[1, 0].set_ylabel("Number of postings")

    locations = summary["locations"]
    axes[1, 1].barh(list(reversed(list(locations.keys()))), list(reversed(list(locations.values()))), color="#8064a2")
    axes[1, 1].set_title("Opportunity Locations")
    axes[1, 1].set_xlabel("Number of postings")

    figure.tight_layout()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(figure)
    return str(path)

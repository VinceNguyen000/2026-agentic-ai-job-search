"""Streamlit interface for the job search application."""

from pathlib import Path

import streamlit as st

from src.analytics import summarize_dataset
from src.data_pipeline import load_dataset
from src.matcher import JobMatcher
from src.rag import PersonalKnowledgeBase, hard_gate_opportunity
from src.retrieval import HybridRetriever


BASE_DIR = Path(__file__).parent


@st.cache_data
def load_app_data():
    return load_dataset(
        str(BASE_DIR / "examples" / "seekers.json"),
        str(BASE_DIR / "examples" / "opportunities.json"),
    )


@st.cache_resource
def load_personal_knowledge_base():
    return PersonalKnowledgeBase.from_directory(str(BASE_DIR / "data" / "personal"))


st.set_page_config(page_title="Job Search Match Lab", page_icon="J", layout="wide")
st.title("Job Search Match Lab")
st.caption("Explainable matching, BM25 retrieval, and skill-gap recommendations")

seekers, opportunities, quality = load_app_data()
matcher = JobMatcher()
summary = summarize_dataset(seekers, opportunities)
knowledge_base = load_personal_knowledge_base()

with st.sidebar:
    st.header("Candidate")
    selected_name = st.selectbox("Choose a seeker", [seeker.name for seeker in seekers])
    retrieval_mode = st.radio("Retrieval mode", ["Weighted matcher", "BM25 + weighted reranking"])
    minimum_score = st.slider("Minimum match score", min_value=0, max_value=100, value=0, step=5)

seeker = next(item for item in seekers if item.name == selected_name)
if retrieval_mode == "BM25 + weighted reranking":
    ranked = [item["match_result"] for item in HybridRetriever(opportunities).rerank(seeker, matcher, top_k=len(opportunities))]
else:
    ranked = matcher.rank_opportunities(seeker, opportunities, min_match_threshold=minimum_score)

ranked = [result for result in ranked if result.overall_match_percentage >= minimum_score]

metric_columns = st.columns(4)
metric_columns[0].metric("Opportunities", len(opportunities))
metric_columns[1].metric("Recommendations", len(ranked))
metric_columns[2].metric("Top match", f"{ranked[0].overall_match_percentage:.2f}%" if ranked else "-")
metric_columns[3].metric("Required skills", summary["dataset"]["required_skill_count"])

st.subheader(f"Recommendations for {seeker.name}")
if not ranked:
    st.info("No opportunity meets the selected threshold.")
else:
    for position, result in enumerate(ranked, start=1):
        with st.expander(f"{position}. {result.job_title} at {result.company} | {result.overall_match_percentage:.2f}%"):
            score_data = {
                "Skills": result.skill_match_percentage,
                "Experience": result.experience_match_percentage,
                "Location": result.location_match_percentage,
                "Salary": result.salary_match_percentage,
                "Work mode": result.work_mode_match_percentage,
                "Work type": result.work_type_match_percentage,
                "Career goals": result.career_goals_match_percentage,
            }
            st.bar_chart(score_data)
            left, right = st.columns(2)
            with left:
                st.write("**Matched skills**")
                st.write(", ".join(result.matched_skills) or "None")
            with right:
                st.write("**Missing skills**")
                st.write(", ".join(result.missing_skills) or "None")
            st.write(result.explanation)
            st.info(result.recommendation)

            eligible, gate_reasons = hard_gate_opportunity(seeker, next(item for item in opportunities if item.job_id == result.job_id))
            st.write("**Prerequisite gate**")
            st.write("Eligible for soft scoring" if eligible else f"Review required: {', '.join(gate_reasons)}")
            evidence = knowledge_base.retrieve_for_job(
                seeker,
                next(item for item in opportunities if item.job_id == result.job_id),
                top_k=3,
            )
            with st.expander("Personal RAG evidence"):
                st.caption("Local hybrid retrieval: BM25 + deterministic dense vectors")
                for item in evidence:
                    st.write(f"**{item.chunk.title}** | hybrid={item.hybrid_score:.3f}")
                    st.write(item.chunk.text)

st.subheader("Dataset analytics")
analytics_columns = st.columns(2)
with analytics_columns[0]:
    st.write("**Most requested required skills**")
    st.bar_chart(summary["top_required_skills"])
with analytics_columns[1]:
    st.write("**Work mode distribution**")
    st.bar_chart(summary["work_modes"])

with st.expander("Data quality report"):
    st.json(quality)

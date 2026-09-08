"""
Autonomous Job Search Agent Architecture.
Provides an Agentic AI engine capable of goal planning, multi-step tool execution,
resume analysis, job recommendation, customized application generation, and upskilling roadmaps.

Author: Vince Nguyen / Antigravity Agentic AI for CS5542 Challenge 1
"""

from typing import List, Dict, Any, Optional, Callable
import json
from dataclasses import dataclass, field
from src.models import Seeker, Opportunity, MatchResult, ExperienceLevel, WorkMode, WorkType
from src.matcher import JobMatcher
from src.utils import keyword_match_percentage


@dataclass
class AgentAction:
    """Represents a discrete tool call action taken by the agent."""
    step: int
    thought: str
    tool_name: str
    tool_args: Dict[str, Any]
    observation: Any


@dataclass
class AgentResponse:
    """Represents the final response synthesized by the agent."""
    goal: str
    actions: List[AgentAction]
    final_synthesis: str
    artifacts: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "steps_taken": len(self.actions),
            "actions": [
                {
                    "step": a.step,
                    "thought": a.thought,
                    "tool": a.tool_name,
                    "args": a.tool_args,
                    "observation": a.observation
                }
                for a in self.actions
            ],
            "final_synthesis": self.final_synthesis,
            "artifacts": self.artifacts
        }


class JobSearchAgent:
    """
    Autonomous Job Search Agent that uses tools to fulfill user goals.
    
    Capabilities:
    - Search & filter job opportunities
    - Evaluate candidate fit across multi-dimensional metrics
    - Diagnose skill gaps and create personalized upskilling roadmaps
    - Draft tailored cover letters and elevator pitches
    - Autonomous multi-step goal execution
    """

    def __init__(self, seekers: Optional[List[Seeker]] = None, opportunities: Optional[List[Opportunity]] = None):
        self.seekers: Dict[str, Seeker] = {s.name.lower(): s for s in (seekers or [])}
        self.opportunities: Dict[str, Opportunity] = {o.job_id: o for o in (opportunities or [])}
        self.matcher = JobMatcher()
        self.tools: Dict[str, Callable] = {
            "search_opportunities": self.tool_search_opportunities,
            "evaluate_fit": self.tool_evaluate_fit,
            "analyze_skill_gaps": self.tool_analyze_skill_gaps,
            "draft_tailored_application": self.tool_draft_tailored_application,
            "generate_upskilling_roadmap": self.tool_generate_upskilling_roadmap,
            "get_seeker_profile": self.tool_get_seeker_profile,
        }

    def register_seeker(self, seeker: Seeker) -> None:
        """Add or update a seeker in agent memory."""
        self.seekers[seeker.name.lower()] = seeker

    def register_opportunity(self, opp: Opportunity) -> None:
        """Add or update an opportunity in agent memory."""
        self.opportunities[opp.job_id] = opp

    def _find_seeker(self, seeker_identifier: str) -> Optional[Seeker]:
        """Lookup seeker by exact or partial name."""
        if not seeker_identifier:
            return None
        key = seeker_identifier.lower().strip()
        if key in self.seekers:
            return self.seekers[key]
        for name, seeker in self.seekers.items():
            if key in name or name in key:
                return seeker
        return None

    # =========================================================================
    # Agent Tools
    # =========================================================================

    def tool_get_seeker_profile(self, seeker_name: str) -> Dict[str, Any]:
        """Tool: Inspect a candidate's profile, skills, and preferences."""
        seeker = self._find_seeker(seeker_name)
        if not seeker:
            return {"error": f"Seeker '{seeker_name}' not found."}
        return seeker.to_dict()

    def tool_search_opportunities(
        self,
        keywords: Optional[str] = None,
        location: Optional[str] = None,
        work_mode: Optional[str] = None,
        min_salary: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Tool: Search and filter available job opportunities."""
        results = []
        for opp in self.opportunities.values():
            if keywords:
                combined_text = f"{opp.title} {opp.description or ''} {' '.join(opp.required_skills)} {' '.join(opp.responsibilities)}"
                if keyword_match_percentage(keywords, combined_text) < 15:
                    continue

            if location and opp.locations:
                loc_match = any(location.lower() in loc.lower() for loc in opp.locations)
                if not loc_match and not opp.allows_relocation:
                    continue

            if work_mode:
                if opp.work_mode.value.lower() != work_mode.lower():
                    continue

            if min_salary and opp.salary_max and opp.salary_max < min_salary:
                continue

            results.append({
                "job_id": opp.job_id,
                "title": opp.title,
                "company": opp.company,
                "work_mode": opp.work_mode.value,
                "locations": opp.locations,
                "salary_range": f"${opp.salary_min:,.0f} - ${opp.salary_max:,.0f}" if opp.salary_min else "Not specified",
                "required_skills": opp.required_skills
            })
        return results

    def tool_evaluate_fit(self, seeker_name: str, job_id: str) -> Dict[str, Any]:
        """Tool: Run multi-dimensional match evaluation between seeker and job."""
        seeker = self._find_seeker(seeker_name)
        if not seeker:
            return {"error": f"Seeker '{seeker_name}' not found."}
        if job_id not in self.opportunities:
            return {"error": f"Opportunity ID '{job_id}' not found."}

        opp = self.opportunities[job_id]
        result = self.matcher.calculate_match(seeker, opp)
        return result.to_dict()

    def tool_analyze_skill_gaps(self, seeker_name: str, job_id: str) -> Dict[str, Any]:
        """Tool: Deep dive into missing vs matched skills with specific remedies."""
        seeker = self._find_seeker(seeker_name)
        if not seeker:
            return {"error": f"Seeker '{seeker_name}' not found."}
        if job_id not in self.opportunities:
            return {"error": f"Opportunity ID '{job_id}' not found."}

        opp = self.opportunities[job_id]
        result = self.matcher.calculate_match(seeker, opp)

        learning_recs = []
        for skill in result.missing_skills:
            learning_recs.append({
                "skill": skill,
                "priority": "HIGH" if skill in opp.required_skills else "MEDIUM",
                "recommended_action": f"Complete hands-on project or certification demonstrating {skill} competency"
            })

        return {
            "seeker": seeker.name,
            "target_role": f"{opp.title} at {opp.company}",
            "matched_required_skills": result.matched_skills,
            "missing_required_skills": result.missing_skills,
            "matched_preferred_skills": result.matched_preferred_skills,
            "skill_match_score": result.skill_match_percentage,
            "remediation_plan": learning_recs
        }

    def tool_draft_tailored_application(self, seeker_name: str, job_id: str) -> Dict[str, str]:
        """Tool: Generate tailored cover letter, key selling points, and interview pitch."""
        seeker = self._find_seeker(seeker_name)
        if not seeker:
            return {"error": f"Seeker '{seeker_name}' not found."}
        if job_id not in self.opportunities:
            return {"error": f"Opportunity ID '{job_id}' not found."}

        opp = self.opportunities[job_id]
        match = self.matcher.calculate_match(seeker, opp)

        matched_skills_str = ", ".join(match.matched_skills) if match.matched_skills else "core technical competencies"
        missing_skills_str = ", ".join(match.missing_skills) if match.missing_skills else ""

        cover_letter = f"""Dear Hiring Team at {opp.company},

I am writing to express my enthusiastic interest in the {opp.title} position (Job ID: {opp.job_id}). With my background in {seeker.education or 'Cybersecurity / Computer Science'} and hands-on expertise in {matched_skills_str}, I am confident in my ability to deliver immediate value to your security and engineering operations.

In reviewing the requirements for the {opp.title} role, I was particularly drawn to your focus on {', '.join(opp.responsibilities[:2]) if opp.responsibilities else 'protecting critical infrastructure'}. My practical experience in {matched_skills_str} directly aligns with your mission and compliance objectives.
"""
        if missing_skills_str:
            cover_letter += f"\nWhile I am actively deepening my operational experience in {missing_skills_str}, my proven background in rapid technical adaptation enables me to master new platforms quickly and contribute effectively.\n"

        cover_letter += f"""
I welcome the opportunity to discuss how my technical skills, research background, and dedication can support {opp.company}'s objectives. Thank you for your time and consideration.

Sincerely,
{seeker.name}
{seeker.email or ''} | {seeker.phone or ''}
"""

        pitch = f"Hi, I'm {seeker.name}. I specialize in {matched_skills_str} with graduate-level training in Cybersecurity. I'm excited about joining {opp.company} as a {opp.title} because my technical foundation in vulnerability management, network packet analysis, and system hardening makes me an ideal fit to protect your infrastructure."

        return {
            "cover_letter": cover_letter.strip(),
            "elevator_pitch": pitch.strip(),
            "top_strengths_to_highlight": match.matched_skills,
            "potential_concerns_to_address": match.missing_skills
        }

    def tool_generate_upskilling_roadmap(self, seeker_name: str, target_role_keyword: Optional[str] = None) -> Dict[str, Any]:
        """Tool: Analyze market trends and generate a multi-week upskilling roadmap for career advancement."""
        seeker = self._find_seeker(seeker_name)
        if not seeker:
            return {"error": f"Seeker '{seeker_name}' not found."}

        relevant_opps = [
            o for o in self.opportunities.values()
            if not target_role_keyword or target_role_keyword.lower() in o.title.lower() or target_role_keyword.lower() in (o.description or '').lower()
        ]

        skill_demand: Dict[str, int] = {}
        for opp in relevant_opps:
            match = self.matcher.calculate_match(seeker, opp)
            for skill in match.missing_skills:
                skill_demand[skill] = skill_demand.get(skill, 0) + 1

        sorted_demands = sorted(skill_demand.items(), key=lambda x: x[1], reverse=True)
        top_gaps = [skill for skill, count in sorted_demands[:4]]
        if not top_gaps:
            top_gaps = ["Enterprise SIEM (Splunk)", "Cloud Security (AWS/Azure)", "Advanced Threat Hunting", "SOAR Automation"]

        roadmap = [
            {
                "phase": "Weeks 1-2: Foundations & Tool Familiarity",
                "focus_skills": top_gaps[:2],
                "objective": "Build core theoretical understanding and complete introductory hands-on security labs"
            },
            {
                "phase": "Weeks 3-4: Applied Labs & Detection Engineering",
                "focus_skills": top_gaps[2:4] if len(top_gaps) > 2 else top_gaps[:1],
                "objective": "Develop detection rules, log correlation playbooks, and incident response projects"
            },
            {
                "phase": "Weeks 5-6: Capstone Project & Certification",
                "focus_skills": top_gaps,
                "objective": "Publish security lab report on GitHub, update resume, and complete industry certification exams"
            }
        ]

        return {
            "seeker": seeker.name,
            "target_focus": target_role_keyword or "Cybersecurity Career Advancement",
            "highest_demand_missing_skills": top_gaps,
            "roadmap": roadmap
        }

    # =========================================================================
    # Autonomous Goal Planning & Execution Loop
    # =========================================================================

    def run_goal(self, goal: str, seeker_name: Optional[str] = None) -> AgentResponse:
        """
        Autonomously plan and execute multi-step actions to achieve user goal.
        """
        actions: List[AgentAction] = []
        artifacts: Dict[str, Any] = {}
        step = 1

        target_seeker = None
        if seeker_name:
            target_seeker = self._find_seeker(seeker_name)
        else:
            for s_name, s_obj in self.seekers.items():
                if s_name in goal.lower() or s_obj.name.lower() in goal.lower():
                    target_seeker = s_obj
                    break

        if not target_seeker and self.seekers:
            target_seeker = list(self.seekers.values())[0]

        seeker_display_name = target_seeker.name if target_seeker else "Candidate"

        # Step 1: Inspect Profile
        actions.append(AgentAction(
            step=step,
            thought=f"I need to inspect {seeker_display_name}'s profile to understand their technical skills, education, and career preferences.",
            tool_name="get_seeker_profile",
            tool_args={"seeker_name": seeker_display_name},
            observation=target_seeker.to_dict() if target_seeker else {}
        ))
        step += 1

        # Step 2: Search opportunities
        search_obs = self.tool_search_opportunities()
        actions.append(AgentAction(
            step=step,
            thought=f"I will query all available job opportunities in the database to evaluate fit for {seeker_display_name}.",
            tool_name="search_opportunities",
            tool_args={},
            observation=search_obs
        ))
        step += 1

        # Step 3: Rank all opportunities
        ranked_matches = self.matcher.rank_opportunities(target_seeker, list(self.opportunities.values()), min_match_threshold=0.0) if target_seeker else []
        top_match = ranked_matches[0] if ranked_matches else None

        if top_match:
            actions.append(AgentAction(
                step=step,
                thought=f"The top compatible opportunity is {top_match.job_title} at {top_match.company} (Match Score: {top_match.overall_match_percentage}%). I will evaluate detailed fit metrics.",
                tool_name="evaluate_fit",
                tool_args={"seeker_name": seeker_display_name, "job_id": top_match.job_id},
                observation=top_match.to_dict()
            ))
            step += 1

            # Step 4: Analyze Skill Gaps
            gaps_obs = self.tool_analyze_skill_gaps(seeker_display_name, top_match.job_id)
            actions.append(AgentAction(
                step=step,
                thought=f"I will analyze technical skill gaps for {top_match.job_title} to pinpoint required vs preferred competencies.",
                tool_name="analyze_skill_gaps",
                tool_args={"seeker_name": seeker_display_name, "job_id": top_match.job_id},
                observation=gaps_obs
            ))
            step += 1

            # Step 5: Draft Tailored Application
            app_obs = self.tool_draft_tailored_application(seeker_display_name, top_match.job_id)
            actions.append(AgentAction(
                step=step,
                thought=f"I will generate an evidence-backed cover letter and 30-second elevator pitch tailored specifically to {top_match.company}.",
                tool_name="draft_tailored_application",
                tool_args={"seeker_name": seeker_display_name, "job_id": top_match.job_id},
                observation=app_obs
            ))
            artifacts["tailored_application"] = app_obs
            step += 1

        # Step 6: Upskilling Roadmap
        roadmap_obs = self.tool_generate_upskilling_roadmap(seeker_display_name)
        actions.append(AgentAction(
            step=step,
            thought=f"Finally, I will construct a structured 6-week upskilling roadmap for {seeker_display_name} to strengthen their candidacy.",
            tool_name="generate_upskilling_roadmap",
            tool_args={"seeker_name": seeker_display_name},
            observation=roadmap_obs
        ))
        artifacts["upskilling_roadmap"] = roadmap_obs
        artifacts["ranked_matches"] = [m.to_dict() for m in ranked_matches]

        synthesis = f"""
================================================================================
AUTONOMOUS JOB SEARCH AGENT REPORT
================================================================================
Candidate: {seeker_display_name}
Goal: {goal}
Execution: Completed {len(actions)} autonomous actions.

TOP RECOMMENDATION:
Position: {top_match.job_title if top_match else 'N/A'} at {top_match.company if top_match else 'N/A'}
Overall Match Score: {top_match.overall_match_percentage if top_match else 0}%
Skills Alignment: {top_match.skill_match_percentage if top_match else 0}%
Experience Match: {top_match.experience_match_percentage if top_match else 0}%
Location Match: {top_match.location_match_percentage if top_match else 0}%
Recommendation: {top_match.recommendation if top_match else 'N/A'}

KEY STRENGTHS:
{', '.join(top_match.matched_skills) if top_match and top_match.matched_skills else 'Strong core profile'}

AREAS FOR GROWTH:
{', '.join(top_match.missing_skills) if top_match and top_match.missing_skills else 'None identified'}

APPLICATION ARTIFACTS GENERATED:
- Tailored Cover Letter generated for {top_match.company if top_match else 'Target Employer'}
- 30-Second Elevator Pitch formulated
- 6-Week Structured Upskilling Roadmap drafted
================================================================================
"""

        return AgentResponse(
            goal=goal,
            actions=actions,
            final_synthesis=synthesis.strip(),
            artifacts=artifacts
        )

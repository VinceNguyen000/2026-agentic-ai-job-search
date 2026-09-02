# CS 5542 Challenge 1 – Agentic AI Hands-On Report
**Job Search Application using Antigravity**

**Date:** September 1, 2026  
**Tool:** Antigravity (In-Class Challenge 1 Session)

---

## What I Worked On During Today's In-Class Session

I used **Antigravity** to design and build a complete **Job Seeker Matching System MVP** that algorithmically matches job seekers to employment opportunities. The system evaluates compatibility across 7 weighted criteria and provides ranked recommendations.

---

## What Antigravity Helped Me Design, Build, Debug, Test, and Improve

### 1. Algorithm Design → Generated → Tested ✅
**What I Asked:** "Design a matching algorithm with weighted criteria for job seeker compatibility"

**What Antigravity Generated:**
- 7-criterion weighted scoring system:
  - Skills matching (30%) - keyword-based with fuzzy matching
  - Experience level (25%) - hierarchical comparison (Entry→Junior→Senior→Lead→Executive)
  - Location (15%) - geographic compatibility with relocation flexibility
  - Salary (15%) - range overlap calculation
  - Work mode (5%) - Remote/Hybrid/Onsite binary matching
  - Work type (5%) - Full/Part/Contract/Intern binary matching
  - Career goals (5%) - keyword-based goal alignment

**What I Tested:**
- Loaded sample data and ran 6 test matches
- Verified all weights sum to 100%
- Confirmed scores fall within 0-100% range
- Tested edge cases (missing data, partial matches, zero overlap)

**What Worked:** ✅ Algorithm produces realistic scores; skill matching works with keyword variations

**What Didn't Work:** ❌ Skill matching with new abbreviations requires manual dictionary updates (JS/JavaScript recognized, but custom acronyms need addition)

---

### 2. Data Models → Generated → Tested ✅
**What I Asked:** "Create Python dataclasses for Job Seeker, Opportunity, and Match Result"

**What Antigravity Generated:**
```
- Seeker class (15 attributes): name, skills[], experience_level, years_experience, 
  salary_min/max, preferred_locations[], willing_to_relocate, work_mode_preferences[], 
  work_type_preferences[], career_goals[], education
  
- Opportunity class (16 attributes): job_id, title, company, description, required_skills[], 
  preferred_skills[], experience_level_required, years_required, salary_min/max, location[], 
  work_mode, work_type, benefits[], industry
  
- MatchResult class: match_percentage, individual_scores (skill, experience, location, salary, 
  work_mode, work_type, goals), matched_skills[], missing_skills[], 
  explanation, recommendation
```

**What I Tested:**
- Created 3 seeker instances with realistic data
- Created 5 job opportunity instances
- Verified JSON serialization (to_dict()) works correctly
- Confirmed all required fields validate

**What Worked:** ✅ Clean dataclass implementation; easy to instantiate and serialize

---

### 3. Matching Engine → Generated → Tested ✅
**What I Asked:** "Implement JobMatcher class with individual scoring methods for each criterion"

**What Antigravity Generated:**
- `JobMatcher` class with 7 private scoring methods:
  - `_calculate_skill_match()` - keyword matching, bonus for preferred skills
  - `_calculate_experience_match()` - hierarchical level comparison
  - `_calculate_location_match()` - perfect match (100%), relocation acceptable (80%), no match (0%)
  - `_calculate_salary_match()` - range overlap percentage
  - `_calculate_work_mode_match()` - binary match or fail
  - `_calculate_work_type_match()` - binary match or fail
  - `_calculate_career_goals_match()` - keyword similarity (Jaccard)
- `rank_opportunities()` method to sort all opportunities by match score
- `_generate_explanation()` and `_generate_recommendation()` for output formatting

**What I Tested:**
- Matched Alice (ML specialist, Senior, $150-200K) to JOB001 (ML Engineer, Senior, $160-220K)
  - Expected: High score (~90%)
  - Got: 92.5% ✅
- Matched Bob (Junior, JS, $80-120K) to JOB005 (DevOps, AWS required, $120-160K)
  - Expected: Low score (~40%)
  - Got: 42.5% ✅
- Ranked all 5 opportunities for Alice
  - Expected: JOB001 highest, JOB004 lowest
  - Got: Correct ranking ✅

**What Worked:** ✅ Matcher produces logical, validated scores; ranking is correct

**What Didn't Work:** ❌ No proficiency levels (e.g., "beginner Python" vs "expert Python" treated identically)

---

### 4. Skill Matching with Abbreviations → Generated → Tested ✅
**What I Asked:** "Add skill matching that recognizes common tech abbreviations"

**What Antigravity Generated:**
- `skill_matches()` utility function with abbreviation dictionary:
  - JS ↔ JavaScript
  - ML ↔ Machine Learning
  - AWS ↔ Amazon Web Services
  - SQL ↔ MySQL, PostgreSQL, SQLServer
  - etc.

**What I Tested:**
- Seeker lists "JS", job requires "JavaScript" → Matched ✅
- Seeker lists "ML", job requires "Machine Learning" → Matched ✅
- Seeker lists "Python", job requires "Python" → Exact match ✅
- Seeker lists "Docker", job requires "Kubernetes" → No match (as expected) ✅

**What Worked:** ✅ Common abbreviations handled correctly

**What Didn't Work:** ❌ New/uncommon abbreviations need manual addition; no automatic semantic understanding

---

### 5. Example Data → Generated → Tested ✅
**What I Asked:** "Generate 3 diverse seeker profiles and 5 realistic job opportunities"

**What Antigravity Generated:**

**Seekers:**
1. **Alice Johnson** - Senior ML engineer, 6 years experience, $150-200K, remote preferred, willing to relocate
2. **Bob Smith** - Junior full-stack developer, 1 year experience, $80-120K, Austin/Denver, contract-willing
3. **Carol Davis** - Junior product manager, 2 years experience, $100-140K, Seattle, hybrid preferred

**Opportunities:**
1. **JOB001** - Senior ML Engineer at TechCorp (Remote, $160-220K, 5yr required)
2. **JOB002** - Full Stack JS Dev at StartUp (Austin, $90-130K, hybrid, 2yr)
3. **JOB003** - Product Manager at MobileFirst (Seattle, $110-150K, hybrid, 2yr)
4. **JOB004** - Data Analyst at Financial (Remote, $75-110K, 1yr, Python+SQL)
5. **JOB005** - DevOps Engineer at CloudScale (SF, $120-160K, hybrid, AWS cert required)

**What I Tested:**
- Reviewed profiles for realism and diversity ✅
- Cross-matched all 3 seekers against all 5 jobs
- Verified results made logical sense (e.g., Alice→JOB001 high, Bob→JOB005 low)

**What Worked:** ✅ Example data is realistic and demonstrates algorithm across diverse scenarios

---

### 6. Documentation & Reporting → Generated → Tested ✅
**What I Asked:** "Generate comprehensive README.md, ALGORITHM.md with formulas, and usage examples"

**What Antigravity Generated:**
- **README.md** - Project overview, features, tech stack, project structure, getting started, usage example
- **ALGORITHM.md** - Detailed methodology with:
  - Purpose of each criterion
  - Calculation formula for each dimension
  - Worked examples (Alice + JOB001)
  - Edge cases and limitations
  - Interpretation table (scores 0-100%)
  - Future enhancements discussion
- **main.py** - Runnable example loading JSON data, running matcher, displaying results

**What I Tested:**
- Followed README instructions step-by-step ✅
- Ran main.py successfully (no errors) ✅
- Verified ALGORITHM.md formulas match code implementation ✅
- Reviewed documentation clarity and completeness ✅

**What Worked:** ✅ Documentation is clear, complete, and enables reproducibility

---

## Challenges & Limitations Encountered

### 1. Skill Variation Matching
- **Challenge:** Real-world job posts and resumes use inconsistent terminology (JS vs JavaScript, SQL vs MySQL)
- **How Antigravity Helped:** Generated abbreviation mapping dictionary
- **Limitation:** Dictionary-based approach doesn't scale; would need semantic embeddings for production

### 2. Proficiency Levels
- **Challenge:** Algorithm treats "Python beginner" and "Python expert" identically
- **Limitation:** No proficiency dimension in current model
- **Future Work:** Add proficiency levels (beginner, intermediate, expert) and adjust scoring

### 3. Experience Level Hierarchy
- **Challenge:** How to score when seeker is Junior but job requires Senior?
- **Solution:** Antigravity generated escalation scoring (partial credit rather than 0%)
- **Result:** ✅ Produces reasonable partial scores (not binary pass/fail)

### 4. Weight Calibration
- **Challenge:** Chosen weights (Skills 30%, Experience 25%, etc.) are heuristic, not data-driven
- **Limitation:** No validation that these weights reflect real hiring importance
- **Future Work:** Collect hiring data and train weights via ML

### 5. Code Generation Consistency
- **Challenge:** Multiple AI generations sometimes produced slightly different patterns
- **Solution:** Manual review and standardization of code style
- **Result:** ✅ Final code is consistent and maintainable

---

## Current MVP Status & Main Features

### ✅ Working Features
1. **Profile Management** - Load/save seeker and opportunity profiles as JSON
2. **7-Criterion Matching** - Comprehensive scoring across all dimensions
3. **Ranking System** - Sort opportunities by match score for a given seeker
4. **Skill Intelligence** - Keyword matching with abbreviation recognition
5. **Detailed Output** - Match scores, breakdowns, explanations, and recommendations
6. **Example Data** - 3 seekers, 5 opportunities, 6 pre-computed matches
7. **Complete Documentation** - README, ALGORITHM.md, code comments, usage examples

### Sample Results
| Seeker | Job | Score | Status |
|--------|-----|-------|--------|
| Alice | JOB001 (ML Engineer) | 92.5% | ✅ Excellent - Apply immediately |
| Alice | JOB004 (Data Analyst) | 78.5% | ✅ Good - Apply with skill development |
| Bob | JOB002 (JS Dev) | 88.0% | ⚠️ Good - But location issue |
| Bob | JOB005 (DevOps) | 42.5% | ❌ Poor - Skills gap too large |
| Carol | JOB003 (PM) | 85.25% | ✅ Strong - Perfect fit |
| Carol | JOB001 (ML Eng) | 35.75% | ❌ Poor - Missing ML skills |

### 🚀 MVP Deliverables
- ✅ Source code (models.py, matcher.py, utils.py, main.py)
- ✅ Complete documentation (README.md, ALGORITHM.md)
- ✅ Example data (seekers.json, opportunities.json, sample_matches.json)
- ✅ GitHub repository with version history
- ✅ Requirements.txt with dependencies

---

## GitHub Repository

**Repository Link:** https://github.com/VinceNguyen000/2026-agentic-ai-job-search

**Repository Contents:**
```
├── README.md                          (Project overview & usage)
├── ALGORITHM.md                       (Algorithm explanation with formulas)
├── HANDS_ON_REPORT_CHALLENGE1.md     (This report)
├── requirements.txt                   (Dependencies)
├── LICENSE                            (MIT)
├── src/
│   ├── __init__.py
│   ├── models.py                      (Seeker, Opportunity, MatchResult classes)
│   ├── matcher.py                     (JobMatcher with scoring logic)
│   └── utils.py                       (Utility functions)
├── examples/
│   ├── seekers.json                   (3 sample profiles)
│   └── opportunities.json             (5 sample jobs)
├── results/
│   └── sample_matches.json            (6 pre-computed match results)
└── main.py                            (Runnable example)
```

---

## Brief Comments & Suggestions About the In-Class Activity

### What Worked Well
1. **Rapid Iteration** - Antigravity enabled quick design → code → test cycles
2. **Multi-File Coordination** - AI successfully maintained consistency across 5+ Python files
3. **Realistic Examples** - Generated seeker/opportunity data was contextually appropriate
4. **Documentation Quality** - README and ALGORITHM.md were publication-ready after light edits

### Challenges with Antigravity
1. **Context Switching** - Jumping between algorithm design, data models, and implementation required frequent re-prompting
2. **Edge Case Handling** - Initial code had gaps; needed manual refinement for complex scenarios
3. **Test Generation** - AI-suggested tests sometimes didn't catch edge cases; manual testing was necessary

### Suggestions for Future Sessions
1. **Provide Domain Reference** - Access to hiring/recruiting domain guidelines would improve algorithm design
2. **Staged Prompting** - Breaking work into smaller, sequential prompts (design → implement → test → document) worked better than all-at-once requests
3. **Validation Checklist** - Having explicit validation criteria (scores in 0-100%, weights sum to 100%, etc.) helped catch issues early

### Key Lesson Learned
**Antigravity is most effective for structured, algorithmic problems with clear specifications.** The job matching system had well-defined inputs, outputs, and calculation methods, which the AI handled expertly. Open-ended or highly creative tasks would likely require more human direction.

---

## Summary

Today's in-class Challenge 1 session successfully produced a **complete, working Job Seeker Matching System MVP** using Antigravity. The system implements a 7-criterion weighted matching algorithm, includes realistic example data, provides detailed scoring and recommendations, and is fully documented. All code is version-controlled on GitHub and ready for review/enhancement.

**Total Development Time:** ~2 hours (in-class session)  
**Lines of Code:** ~800 (models, matcher, utils)  
**Documentation:** ~1500 lines (README, ALGORITHM, this report)  
**Test Coverage:** 6 realistic match scenarios validated  

**Status:** MVP Complete ✅ | Ready for Production Enhancement 🚀

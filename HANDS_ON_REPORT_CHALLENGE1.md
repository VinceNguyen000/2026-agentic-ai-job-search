# CS 5542 Challenge 1 – Agentic AI Hands-On Report

**Job Search Application using Antigravity**

- **Student:** Vince Nguyen
- **Course:** CS 5542 – Advanced Agentic AI
- **Assignment:** Challenge 1: Job Search Application Hands-On Experience
- **Date:** September 1, 2026
- **Tool Used:** Antigravity (Agentic AI Assistant by Google DeepMind)
- **GitHub Repository:** [https://github.com/VinceNguyen000/2026-agentic-ai-job-search](https://github.com/VinceNguyen000/2026-agentic-ai-job-search)

---

## 1. What You Did Today

During today's in-class hands-on session, I used **Antigravity** to design, architect, implement, debug, test, and document an **Autonomous Agentic AI Job Search System**.

Specific tasks completed during the session:

1. **Repository Ingestion & Codebase Audit:** Cloned and audited the existing repository structure using Antigravity's terminal execution and file inspection tools.
2. **Autonomous Agent Architecture Implementation:** Prompted Antigravity to build a full `JobSearchAgent` engine with discrete tool calling (`get_seeker_profile`, `search_opportunities`, `evaluate_fit`, `analyze_skill_gaps`, `draft_tailored_application`, `generate_upskilling_roadmap`).
3. **Bug Diagnosis & Algorithm Debugging:** Detected and resolved an algorithmic flaw in career goal matching where Jaccard word-union calculation against entire job descriptions caused career goal scores to artificially collapse to `0.0%`.
4. **Acronym & Semantic Expansion:** Enhanced token matching to recognize 2-letter tech acronyms (`AI`, `ML`, `JS`, `DB`) and map them to their full domain equivalents.
5. **Automated Testing Suite Creation:** Designed and executed a comprehensive 17-test zero-dependency unit testing suite using Python's `unittest` framework.
6. **CLI & Artifact Export:** Updated `main.py` with multi-mode CLI options (`--agent`, `--matcher`, `--goal`) and generated structured JSON outputs (`results/sample_agent_output.json`).

---

## 2. Achievements

What I was able to design, build, implement, test, and improve with Antigravity:

### A. Autonomous Multi-Tool Agent Engine (`src/agent.py`)

- **Design:** Created a ReAct-style agent capable of breaking down high-level career objectives into multi-step tool calls.
- **Built 6 Specialized Tools:**
  1. `get_seeker_profile`: Inspects candidate skills, experience level, salary expectation, and location preferences.
  2. `search_opportunities`: Filters opportunities dynamically across keywords, salary thresholds, and work modes.
  3. `evaluate_fit`: Executes multi-dimensional 7-factor scoring.
  4. `analyze_skill_gaps`: Diagnoses missing required and preferred skills with priority remediation actions.
  5. `draft_tailored_application`: Autonomously drafts tailored cover letters and 30-second elevator pitches based on matching qualifications.
  6. `generate_upskilling_roadmap`: Analyzes market gaps and produces a structured 6-week progressive career roadmap.

### B. 7-Factor Weighted Matching Engine (`src/matcher.py`)

- Accurately evaluates candidates across 7 weighted dimensions:
  - **Skills Match (30%)** – Keyword matching with abbreviation awareness and preferred skill bonuses.
  - **Experience Level (25%)** – 5-tier hierarchical progression (Entry $\rightarrow$ Junior $\rightarrow$ Senior $\rightarrow$ Lead $\rightarrow$ Executive).
  - **Location Compatibility (15%)** – Geographic alignment with relocation flexibility penalty/credit.
  - **Salary Range Alignment (15%)** – Mathematical interval overlap calculation.
  - **Work Mode (5%)** – Remote, Hybrid, or Onsite preference matching.
  - **Employment Type (5%)** – Full-time, Part-time, Contract, or Internship compatibility.
  - **Career Goals Containment (5%)** – Keyword containment and alias expansion.

### C. Automated Test Coverage (`tests/`)

- Implemented and passed **17 automated unit tests** covering data models, serializations, matching rules, token containment, tool invocations, and full end-to-end agent workflows.

---

## 3. Antigravity / Agentic AI Experience

### Step-by-Step Development Flow:

$$\text{Prompt to Antigravity} \longrightarrow \text{Generated / Refactored Code} \longrightarrow \text{Automated Test} \longrightarrow \text{Observation \& Refinement} \longrightarrow \text{Working MVP}$$

| Development Phase                  | What I Asked Antigravity to Do                                                                                                                          | What Antigravity Generated or Changed                                                                                                                                                                                                          | What I Tested / Observed                                                       | Outcome                                                                                                    |
| :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| **1. Architecture & Agent Engine** | "Build an autonomous `JobSearchAgent` with tool calling for profile lookup, job search, fit evaluation, application drafting, and upskilling roadmaps." | Created [`src/agent.py`](file:///C:/Users/VinceNguyen/.gemini/antigravity/scratch/2026-agentic-ai-job-search/src/agent.py) with `JobSearchAgent`, tool registry, and `run_goal` multi-step execution loop.                                     | Executed `python main.py --agent`                                              | ✅ **Worked**: Agent executed 6 autonomous actions and generated tailored cover letter & 6-week roadmap.   |
| **2. Code Audit & Bug Fix**        | "Analyze why Alice received 0% for Career Goals match against the Senior ML Engineer position."                                                         | Identified Jaccard denominator bug in [`src/utils.py`](file:///C:/Users/VinceNguyen/.gemini/antigravity/scratch/2026-agentic-ai-job-search/src/utils.py); rewrote `keyword_match_percentage` to use containment overlap with stopword removal. | Re-ran matching pipeline on `JOB001`                                           | ✅ **Worked**: Alice's Career Goals score increased from 0.0% to 58.33%, boosting overall match to 94.92%. |
| **3. Acronym & Token Matcher**     | "Fix token filtering so 2-letter tech acronyms like AI and ML are not stripped during keyword analysis."                                                | Updated `min_word_length=2` and added `TECH_EXPANSIONS` dictionary (`ai`, `ml`, `js`, `nlp`, `aws`) in `src/utils.py`.                                                                                                                         | Ran unit test `test_keyword_match_percentage_containment`                      | ✅ **Worked**: "Work on AI/ML projects" correctly matched ML job descriptions ($>50\%$).                   |
| **4. CLI & Demonstration**         | "Enhance `main.py` with argument parsing for `--agent`, `--matcher`, and custom `--goal` inputs."                                                       | Refactored [`main.py`](file:///C:/Users/VinceNguyen/.gemini/antigravity/scratch/2026-agentic-ai-job-search/main.py) with `argparse`, demo runners, and JSON export to `results/sample_agent_output.json`.                                      | Executed `python main.py --goal "Find best role for Bob" --seeker "Bob Smith"` | ✅ **Worked**: Agent resolved custom user goals dynamically from the command line.                         |
| **5. Test Suite Verification**     | "Create automated unit tests for all models, matcher rules, utils, and agent tools."                                                                    | Created 4 test suites in `tests/` (`test_models.py`, `test_utils.py`, `test_matcher.py`, `test_agent.py`) using `unittest`.                                                                                                                    | Ran `python -m unittest discover -s tests -p "test_*.py" -v`                   | ✅ **Worked**: All 17 tests passed with zero external dependencies.                                        |

---

## 4. Challenges Encountered & Resolutions

1. **Jaccard Similarity Denominator Collapse:**
   - _Problem:_ The initial algorithm compared short seeker goal strings ($\approx 4$ words) with entire job descriptions ($\approx 150$ words) using standard Jaccard similarity ($\frac{|A \cap B|}{|A \cup B|}$). Because the union was large, the similarity was always $<3\%$, causing career goal scores to round down to $0\%$.
   - _Resolution:_ Antigravity refactored the metric to calculate **keyword containment with stopword filtering** ($\frac{\text{matched keywords}}{\text{meaningful goal keywords}}$), enabling accurate continuous scoring.

2. **2-Letter Acronym Exclusion:**
   - _Problem:_ The tokenizer had a default `min_word_length=3`, which silently dropped critical tech acronyms like `AI`, `ML`, `JS`, `DB`, and `C#`.
   - _Resolution:_ Adjusted `min_word_length=2` and introduced semantic expansion mappings (`ai` $\rightarrow$ `artificial intelligence`, `ml` $\rightarrow$ `machine learning`).

3. **Transitioning from Static Code to Autonomous Tool Execution:**
   - _Problem:_ A simple script only provides static calculation without actionable guidance for the user.
   - _Resolution:_ Built `JobSearchAgent` with an autonomous planning loop that chains together profile parsing, job searching, gap diagnosis, cover letter drafting, and career roadmap generation.

4. **Zero-Dependency Test Compatibility:**
   - _Problem:_ Initial test scripts imported `pytest`, which was not installed in the global Python environment.
   - _Resolution:_ Antigravity refactored all test modules into Python's native `unittest.TestCase` suite, ensuring seamless out-of-the-box execution across any environment.

---

## 5. Current Minimum Viable Product (MVP)

The current MVP is a fully operational, test-verified **Autonomous Job Search & Career Advisory Agent**:

```
                                  ┌────────────────────────┐
                                  │   User Natural Goal    │
                                  └───────────┬────────────┘
                                              │
                                              ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                    JobSearchAgent                                      │
│                                                                                        │
│  [Step 1: Inspect Profile] ──► [Step 2: Search Jobs] ──► [Step 3: 7-Factor Evaluation] │
│                                                                        │               │
│  [Step 6: Upskilling Roadmap] ◄── [Step 5: Draft Application] ◄────────┘               │
└─────────────────────────────────────────────┬──────────────────────────────────────────┘
                                              │
                                              ▼
                             ┌──────────────────────────────────┐
                             │  Application & Career Artifacts  │
                             │  - Match Breakdown & Explanation │
                             │  - Tailored Cover Letter & Pitch │
                             │  - 6-Week Structured Roadmap     │
                             └──────────────────────────────────┘
```

### Core MVP Features:

- **Autonomous Tool Execution:** Agent dynamically chains 6 tools based on user goals.
- **7-Dimensional Scoring:** Evaluates Skills (30%), Experience (25%), Location (15%), Salary (15%), Work Mode (5%), Work Type (5%), and Career Goals (5%).
- **Automated Skill Remediation:** Flags missing skills and assigns learning priorities.
- **Application Generation:** Drafts personalized cover letters and elevator pitches emphasizing top strengths.
- **6-Week Upskilling Roadmap:** Curates phased learning plans for career advancement.
- **Multi-Format CLI:** Supports batch evaluation, agent demonstration, and custom goal pursuit.

---

## 6. GitHub Repository Details

- **Repository Link:** [https://github.com/VinceNguyen000/2026-agentic-ai-job-search](https://github.com/VinceNguyen000/2026-agentic-ai-job-search)
- **Primary Branch:** `main`

### Repository Structure:

```
2026-agentic-ai-job-search/
├── README.md                          # Project documentation & quickstart
├── ALGORITHM.md                       # Comprehensive mathematical algorithm specification
├── HANDS_ON_REPORT_CHALLENGE1.md     # This hands-on report
├── requirements.txt                   # Dependency declarations
├── LICENSE                            # MIT License
├── main.py                            # CLI entry point (Demo, Matcher, and Agent modes)
├── src/
│   ├── __init__.py                    # Package initialization & exports
│   ├── agent.py                       # Autonomous JobSearchAgent & tool registry
│   ├── matcher.py                     # 7-factor weighted matching engine
│   ├── models.py                      # Dataclasses (Seeker, Opportunity, MatchResult)
│   └── utils.py                       # Tokenizer, acronym expansion, salary & skill math
├── tests/
│   ├── __init__.py
│   ├── test_agent.py                  # Unit tests for agent tools and goal workflows
│   ├── test_matcher.py                # Unit tests for scoring rules & ranking
│   ├── test_models.py                 # Unit tests for dataclass validation & serialization
│   └── test_utils.py                  # Unit tests for string matching & edge cases
├── examples/
│   ├── seekers.json                   # 3 diverse candidate profiles
│   └── opportunities.json             # 5 realistic job postings
└── results/
    ├── sample_matches.json            # Algorithmic match outputs
    └── sample_agent_output.json       # Full autonomous agent execution trace & artifacts
```

---

## 7. Comments & Suggestions About Today's Activity

!

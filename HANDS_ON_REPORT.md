# CS 5542 Challenge 1 – Agentic AI Hands-On Report
**Job Search Application using Antigravity**

**Date:** September 1, 2026

---

## What I Worked On During Today's Session

During the in-class Challenge 1 hands-on activity, I used **Antigravity** to design and build a complete job-seeker matching system. The goal was to create an MVP that matches job seekers to employment opportunities using a weighted multi-criteria algorithm.

---

## What Antigravity Helped Me Design, Build, Debug, Test, and Improve

### 1. **Algorithm Design**
- **Requested:** "Design a weighted matching algorithm that scores job compatibility across 7 dimensions"
- **Antigravity Generated:** Complete matching algorithm with:
  - Skills matching (30% weight) with keyword recognition
  - Experience level alignment (25%)
  - Location compatibility (15%)
  - Salary range overlap (15%)
  - Work mode/type binary matching (5% each)
  - Career goals alignment (5%)
- **Testing:** Verified algorithm logic against sample data; weights correctly sum to 100%
- **Result:** ✅ Functional weighted scoring system with clear interpretation

### 2. **Data Models**
- **Requested:** "Create Python dataclasses for Seeker, Opportunity, and MatchResult with proper enums"
- **Antigravity Generated:** 
  - `Seeker` class with 15+ attributes (skills, experience, preferences, salary)
  - `Opportunity` class with 16+ attributes (requirements, benefits, location)
  - `MatchResult` class with detailed scoring breakdown
  - Enums for ExperienceLevel, WorkMode, WorkType
- **Testing:** Created instances with sample data; to_dict() serialization works correctly
- **Result:** ✅ Clean, well-typed data structures ready for matching

### 3. **Matching Engine Implementation**
- **Requested:** "Implement the JobMatcher class with individual scoring methods for each criterion"
- **Antigravity Generated:**
  - 7 separate scoring methods (one per criterion)
  - Skill matching with abbreviation recognition (JS↔JavaScript, ML↔Machine Learning)
  - Experience level hierarchy (Entry→Junior→Senior→Lead→Executive)
  - Salary range overlap calculation
  - Binary matching for work preferences
- **Testing:** Ran sample matches; verified scores were between 0-100 and weights applied correctly
- **Result:** ✅ Working matcher with all criteria implemented

### 4. **Utility Functions**
- **Requested:** "Create utility functions for skill matching, salary calculation, and report formatting"
- **Antigravity Generated:**
  - `skill_matches()` with common tech abbreviation mappings
  - `calculate_salary_match()` with range overlap logic
  - `format_match_report()` for human-readable output
  - JSON loading/saving utilities
- **Testing:** Tested skill matching with various abbreviations; salary calculations with overlapping ranges
- **Result:** ✅ Reusable utilities working as expected

### 5. **Example Data & Results**
- **Requested:** "Generate realistic seeker profiles, job opportunities, and sample match results"
- **Antigravity Generated:**
  - 3 diverse seeker profiles (data scientist, junior developer, product manager)
  - 5 job opportunities (various seniority levels and industries)
  - Pre-computed match results showing algorithm output
- **Testing:** Reviewed data for realism; verified match scores made logical sense
- **Result:** ✅ Realistic example data demonstrating algorithm behavior

### 6. **Documentation**
- **Requested:** "Write comprehensive README, ALGORITHM.md, and usage examples"
- **Antigravity Generated:**
  - Complete README with features, usage, project structure
  - Detailed ALGORITHM.md explaining each criterion with formulas and examples
  - Runnable main.py demonstrating system usage
- **Testing:** Followed README instructions; main.py runs without errors
- **Result:** ✅ Clear documentation enabling understanding and reproduction

---

## Challenges

### Technical Challenges
1. **Feature Normalization** - Matching diverse feature types (keywords, salary ranges, categorical work modes) required careful normalization to compute meaningful percentages
2. **Skill Matching Complexity** - Keyword-based skill matching can miss semantic similarities (e.g., "JavaScript" vs "JS"); would benefit from embedding-based matching
3. **Multi-Criteria Weighting** - Determining optimal weights for different matching criteria required domain knowledge and testing

### AI & Automation Challenges
1. **Consistency of AI-Generated Code** - Ensuring that AI-generated matching logic correctly implements the intended algorithm required validation
2. **Documentation Automation** - Getting AI to generate clear, comprehensive README.md files with proper structure and examples took iterative refinement
3. **Bias in Recommendations** - Ensuring the matching algorithm doesn't inadvertently bias recommendations based on demographic factors

### Project Scope Challenges
1. **Data Source Integration** - Real job platforms (LinkedIn, Indeed, Glassdoor) have restrictive APIs; using mock data instead
2. **Real-World Complexity** - Actual hiring processes involve subjective factors beyond structured matching

---

## Minimum Viable Product (MVP)

### Core Features
1. **Profile Input System**
   - Seeker registration with career goals, skills, experience, education, preferences
   - Job opportunity data ingestion with structured requirements and benefits

2. **Matching Algorithm**
   - Calculate match percentage across 7 weighted criteria
   - Support for skill keyword matching with partial matching
   - Experience level comparison (entry → junior → senior)
   - Location, salary, work mode, and work type compatibility checks

3. **Recommendation & Feedback Engine**
   - Ranked list of job recommendations for each seeker
   - Match score breakdown showing which criteria were met/unmet
   - Suggestions for skill gaps to address
   - Experience level recommendations

### Technology Stack
- **Language:** Python (for matching algorithm and data processing)
- **Agentic AI:** GitHub Copilot for code generation and documentation
- **Repository:** GitHub with version control
- **Documentation:** AI-assisted README generation, algorithm documentation

### Deliverables
- Source code implementing the matching algorithm
- README.md documenting project overview, algorithm design, and usage
- Example seeker and opportunity profiles
- Sample match results and recommendations
- Project documentation explaining methodology and weights

---

## GitHub Repository

**Repository:** [2026-agentic-ai-job-search](https://github.com/[your-username]/2026-agentic-ai-job-search)

### Repository Contents
- `README.md` - Project overview and usage guide (generated/refined by AI)
- `src/matcher.py` - Core matching algorithm implementation
- `src/models.py` - Seeker and Opportunity profile data structures
- `examples/` - Sample seeker profiles and job opportunities
- `results/` - Example match results and recommendations
- `ALGORITHM.md` - Detailed explanation of matching methodology and weighting
- `.github/` - CI/CD workflows and templates

---

## Comments & Suggestions

### Observations About Agentic AI Experience

#### Strengths
1. **Rapid Prototyping** - AI agents enabled quick generation of code scaffolding, reducing boilerplate work
2. **Documentation Quality** - AI-assisted documentation generation created clear, well-structured README files with proper examples
3. **Iterative Refinement** - Using agents to refine and improve code/docs based on feedback was efficient
4. **Pattern Recognition** - AI agents quickly identified design patterns and best practices for the matching algorithm

#### Limitations Encountered
1. **Semantic Understanding** - AI had difficulty understanding complex domain-specific matching logic without detailed prompts
2. **Validation & Testing** - AI-generated tests sometimes missed edge cases; manual validation was necessary
3. **Algorithm Correctness** - Need to carefully verify AI-generated matching calculations match intended formula
4. **Context Limits** - Longer project descriptions sometimes exceeded AI context windows, requiring segmentation

### Suggestions for Improvement

#### For the Activity/Assignment
1. **Provide Example Repositories** - Showing an example of an AI-assisted project would help clarify expectations
2. **Clear Scope Guidelines** - Define minimum code requirements (LOC, function count, etc.) to help students set realistic MVP goals
3. **Checkpoint Reviews** - Include mid-project checkpoints where instructors could provide feedback on AI-assisted work
4. **Validation Criteria** - Specify how to verify AI-generated code is correct and not just plausible-looking

#### For Agentic AI Development
1. **Domain Context Loading** - Allow providing custom domain knowledge/glossaries to improve AI understanding
2. **Multi-File Awareness** - Better support for maintaining consistency across multiple generated files
3. **Formal Verification** - Tools to formally verify AI-generated algorithms match specifications
4. **Test-Driven Generation** - Framework for writing test cases first, then having AI implement to pass tests
5. **Semantic Code Search** - Better tools for searching AI-generated code by functionality rather than keywords

### Lessons Learned
1. **AI is a Collaborative Tool** - Best results come from clearly defining requirements and iteratively refining AI outputs
2. **Human Validation is Essential** - Always verify AI-generated logic, especially for critical algorithms
3. **Clear Communication Matters** - Detailed prompts to AI agents produce significantly better results than vague requests
4. **Documentation is Key** - Well-documented requirements and design decisions help both AI and future maintainers

---

## Conclusion

This hands-on experience demonstrated the practical value of Agentic AI for rapid prototyping and documentation in a meaningful project context. The job search matching system serves as a solid MVP that could be expanded with real data integration, machine learning-based skill matching, and more sophisticated recommendation algorithms. While AI agents significantly accelerated development, maintaining code quality and correctness requires active human oversight and validation.

**Date:** September 1, 2026  
**Project Status:** MVP Complete, Ready for Enhancement

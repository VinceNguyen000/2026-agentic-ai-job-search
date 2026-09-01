# 2026 Agentic AI Job Search Matching System

A hands-on experimentation project exploring how Agentic AI can accelerate software development, using a job-seeker matching algorithm as the case study.

## Project Overview

This project demonstrates the use of AI agents to design, implement, and document a sophisticated job matching system that connects career seekers with relevant opportunities based on multiple weighted criteria.

## Key Features

### Matching Algorithm
- **Weighted Multi-Criteria Matching** - Combines 7 factors with optimized weights:
  - Skills Match (30%) - Keyword-based skill matching
  - Experience Level (25%) - Career progression alignment
  - Location (15%) - Geographic compatibility
  - Salary (15%) - Compensation range matching
  - Work Mode (5%) - Remote/Hybrid/Onsite preferences
  - Work Type (5%) - Full-time/Part-time/Contract flexibility
  - Career Goals (5%) - Long-term aspiration alignment

### Core Components
- **Seeker Profile Model** - Captures job seekers' qualifications, preferences, and career goals
- **Opportunity Profile Model** - Represents job listings with requirements and benefits
- **Recommendation Engine** - Generates ranked job matches with detailed feedback
- **Feedback System** - Explains match percentages and suggests skill gaps to address

## Technology Stack

- **Language:** Python
- **Development:** AI-Assisted Code Generation (GitHub Copilot)
- **Repository:** GitHub for version control
- **Documentation:** AI-Generated with Human Review

## Project Structure

```
2026-agentic-ai-job-search/
├── README.md                 # This file
├── HANDS_ON_REPORT.md        # Detailed assignment report
├── ALGORITHM.md              # Matching algorithm documentation
├── src/
│   ├── matcher.py           # Core matching engine
│   ├── models.py            # Data structures (Seeker, Opportunity)
│   └── utils.py             # Helper functions
├── examples/
│   ├── seekers.json         # Sample seeker profiles
│   └── opportunities.json   # Sample job opportunities
└── results/
    └── sample_matches.json  # Example matching results
```

## Getting Started

### Installation
```bash
git clone https://github.com/[your-username]/2026-agentic-ai-job-search.git
cd 2026-agentic-ai-job-search
pip install -r requirements.txt
```

### Usage
```python
from src.matcher import JobMatcher
from src.models import Seeker, Opportunity

# Create a seeker profile
seeker = Seeker(
    name="John Doe",
    skills=["Python", "Data Analysis", "SQL"],
    experience_level="junior",
    location="San Francisco, CA",
    work_mode="remote"
)

# Create a job opportunity
job = Opportunity(
    title="Data Analyst",
    required_skills=["Python", "SQL", "Tableau"],
    experience_level="junior",
    location="San Francisco, CA",
    work_mode="remote"
)

# Calculate match
matcher = JobMatcher()
match_score = matcher.calculate_match(seeker, job)
recommendations = matcher.get_recommendations(seeker, job)
```

## Matching Methodology

The matching algorithm employs a **weighted scoring approach** where each criterion is normalized to a 0-100% scale, then combined using predefined weights:

```
Total Match % = (Skill Score × 0.30) + (Experience × 0.25) + 
                (Location × 0.15) + (Salary × 0.15) + 
                (Work Mode × 0.05) + (Work Type × 0.05) + 
                (Career Goals × 0.05)
```

See [ALGORITHM.md](./ALGORITHM.md) for detailed methodology.

## Implementation Details

### Source Code Structure

#### Core Modules
- **`models.py`** - Data classes for Seeker, Opportunity, and MatchResult with enums for ExperienceLevel, WorkMode, and WorkType
- **`matcher.py`** - JobMatcher class implementing the 7-dimensional weighted matching algorithm with helper methods for each criterion
- **`utils.py`** - Utility functions for skill matching, salary calculation, and report generation

#### Data Files
- **`examples/seekers.json`** - Sample seeker profiles with diverse skills, preferences, and goals
- **`examples/opportunities.json`** - Sample job listings representing different roles and experience levels
- **`results/sample_matches.json`** - Pre-computed match results showing algorithm output

### Key Implementation Features

1. **Intelligent Skill Matching**
   - Case-insensitive exact matching
   - Common abbreviation recognition (JS↔JavaScript, ML↔Machine Learning, etc.)
   - Preferred skills bonus scoring
   - See ALGORITHM.md for detailed methodology

2. **Experience Level Alignment**
   - 5-level hierarchy (Entry → Junior → Senior → Lead → Executive)
   - Partial credit for candidates below required level
   - Full credit for candidates above required level

3. **Multi-Criteria Optimization**
   - Weighted scoring with configurable weights
   - Binary matching for work mode/type (quick decision)
   - Range overlap calculation for salary
   - Keyword-based career goal alignment

4. **Human-Readable Feedback**
   - Detailed explanation of match score
   - Actionable recommendations
   - Skill gap analysis with suggestions

### Running the System

```bash
# Install dependencies
pip install -r requirements.txt

# Run example matching
python main.py
```

## Agentic AI Insights

### What Worked Well
✅ **Rapid prototyping** - Generated complete data models and matching logic efficiently  
✅ **Documentation** - AI produced clear, comprehensive technical documentation  
✅ **Code quality** - Generated code followed Python best practices  
✅ **Example data** - Realistic seeker/opportunity profiles with varied characteristics  
✅ **Iterative refinement** - Easy to adjust weights and algorithm parameters  

### Challenges Overcome
⚠️ **Semantic understanding** - Required detailed prompts to ensure correct logic  
⚠️ **Edge case handling** - Needed explicit guidance for boundary conditions  
⚠️ **Test coverage** - AI-generated code needed manual validation  
⚠️ **Consistency** - Maintaining naming conventions across generated modules  
⚠️ **Domain specificity** - ML/hiring domain knowledge required careful specification  

### Best Practices Discovered
📌 **Clear requirements** - Detailed specifications produced better code  
📌 **Modular design** - Breaking algorithm into separate methods improves clarity  
📌 **Type hints** - Explicit typing helped AI understand data flow  
📌 **Documentation** - Inline comments and docstrings improved output quality  
📌 **Example-driven** - Providing usage examples improved implementation correctness

## Results & Examples

See [results/](./results/) directory for sample matching scenarios and output.

## Future Enhancements

- [ ] Integration with real job APIs (LinkedIn, Indeed, Glassdoor)
- [ ] Machine learning-based skill embeddings for semantic matching
- [ ] User interface for seeker/job browsing and matching
- [ ] Historical matching data for algorithm optimization
- [ ] Bias detection and fairness metrics
- [ ] Scaling to large job databases (100K+ listings)

## Report & Documentation

For detailed information about this hands-on experience, see:
- **[HANDS_ON_REPORT.md](./HANDS_ON_REPORT.md)** - Complete assignment report covering achievements, challenges, MVP, and observations about Agentic AI

## Author

Created as part of CS5542 Agentic AI Hands-On Activity (Fall 2026)  
**Generated with:** GitHub Copilot (Agentic AI)

## License

MIT License - See LICENSE file for details
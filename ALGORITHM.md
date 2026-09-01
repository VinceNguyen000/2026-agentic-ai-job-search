# Job Matching Algorithm Documentation

## Overview

This document describes the weighted multi-criteria matching algorithm used to calculate job compatibility scores between job seekers and employment opportunities. The algorithm combines seven different matching dimensions with carefully calibrated weights to produce a holistic match percentage (0-100%).

## Matching Dimensions

### 1. Skills Match (30% weight)

**Purpose:** Assess technical skill alignment between seeker capabilities and job requirements.

**Calculation Method:**
- Required Skills Matching: Count how many of the job's required skills the seeker possesses
  - Base score: `(matched_required_skills / total_required_skills) × 100`
- Preferred Skills Bonus: Additional points for matched preferred skills
  - Bonus score: `(matched_preferred_skills / total_preferred_skills) × 10` (max 10 points)
- Final Score: `min(100, base_score + bonus_score)`

**Skill Matching Logic:**
- Case-insensitive exact matching (e.g., "Python" matches "python")
- Common abbreviation recognition:
  - "JavaScript" matches "JS" or "Node.js"
  - "Machine Learning" matches "ML"
  - "AWS" matches "Amazon Web Services"
  - "SQL" matches "MySQL", "PostgreSQL", etc.
- No partial word matching (to avoid false positives)

**Example:**
```
Seeker skills: ["Python", "SQL", "Machine Learning", "Tableau"]
Job required: ["Python", "SQL", "Big Data"]
Job preferred: ["Tableau", "TensorFlow"]

Matched required: 2/3 = 66.67%
Matched preferred: 1/2 = 5% bonus
Final skills match: 71.67%
```

### 2. Experience Level Match (25% weight)

**Purpose:** Evaluate career progression alignment.

**Experience Level Hierarchy:**
1. Entry (value: 1)
2. Junior (value: 2)
3. Senior (value: 3)
4. Lead (value: 4)
5. Executive (value: 5)

**Calculation Method:**
```
If seeker_level >= required_level:
    match_percentage = 100%
Else:
    match_percentage = (seeker_level_value / required_level_value) × 100

Result = min(100, match_percentage)
```

**Rationale:** A seeker with more experience is always qualified for a role requiring less experience. Conversely, a junior candidate for a senior role receives partial credit based on how close they are to the required level.

**Example:**
```
Seeker level: Junior (value 2)
Required level: Senior (value 3)
Match: (2 / 3) × 100 = 66.67%
```

### 3. Location Match (15% weight)

**Purpose:** Determine geographic compatibility.

**Calculation Rules:**
1. **Perfect Match (100%):** Seeker's preferred location matches job location exactly
2. **Relocation Match (80%):** Seeker willing to relocate AND job allows relocation
3. **No Match (0%):** Geographic incompatibility

**Implementation:**
- Case-insensitive location string comparison
- Supports multiple preferred locations for seeker
- Supports multiple job locations

**Example:**
```
Seeker preferences: ["San Francisco, CA", "Remote"]
Job locations: ["San Francisco, CA"]
Match: 100% (exact match)

---

Seeker preferences: ["Dallas, TX"]
Seeker willing to relocate: YES
Job locations: ["Denver, CO"]
Job allows relocation: YES
Match: 80% (relocation possible)

---

Seeker preferences: ["Dallas, TX"]
Seeker willing to relocate: NO
Job locations: ["Denver, CO"]
Match: 0% (incompatible)
```

### 4. Salary Match (15% weight)

**Purpose:** Evaluate compensation compatibility.

**Calculation Method:**

Determine overlap between seeker's salary expectation range and job's salary offer range:

```
Seeker range: [seeker_min, seeker_max]
Job range: [job_min, job_max]

1. Check for overlap:
   If job_max < seeker_min OR seeker_max < job_min:
       match = 0% (no overlap)

2. Calculate overlap:
   overlap_start = max(seeker_min, job_min)
   overlap_end = min(seeker_max, job_max)
   overlap_amount = overlap_end - overlap_start

3. Calculate percentage:
   seeker_range_size = seeker_max - seeker_min
   match_percentage = (overlap_amount / seeker_range_size) × 100
   Result = min(100, match_percentage)
```

**Special Cases:**
- If either party has no salary information: 100% match (assume compatibility)
- If seeker's range has zero size: 100% match

**Example:**
```
Seeker expectation: $80K - $120K
Job salary: $100K - $150K

Overlap: $100K - $120K = $20K
Seeker range: $40K
Match: ($20K / $40K) × 100 = 50%

---

Seeker expectation: $150K - $200K
Job salary: $80K - $120K

No overlap (job_max < seeker_min)
Match: 0%
```

### 5. Work Mode Match (5% weight)

**Purpose:** Align work arrangement preferences (remote/hybrid/onsite).

**Calculation:**
- **Perfect Match (100%):** Job's work mode matches seeker's preference(s)
- **No Match (0%):** Job's work mode not in seeker's preferences

**Implementation:**
- Seeker can specify multiple acceptable work modes
- Job has a single work mode
- Binary matching (no partial credit)

**Example:**
```
Seeker preferences: ["remote", "hybrid"]
Job mode: "remote"
Match: 100%

---

Seeker preferences: ["remote", "hybrid"]
Job mode: "onsite"
Match: 0%
```

### 6. Work Type Match (5% weight)

**Purpose:** Align employment type preferences (full-time/part-time/contract/internship).

**Calculation:**
- **Perfect Match (100%):** Job's work type matches seeker's preference(s)
- **No Match (0%):** Job's work type not in seeker's preferences

**Implementation:**
- Binary matching (no partial credit)
- Seeker can specify multiple acceptable work types

**Example:**
```
Seeker preferences: ["full", "contract"]
Job type: "full"
Match: 100%
```

### 7. Career Goals Alignment (5% weight)

**Purpose:** Assess role's alignment with seeker's long-term career objectives.

**Calculation Method:**

Uses keyword matching between career goals and job opportunity details:

```
For each career goal:
    goal_match_score = keyword_match(goal, job_title + job_description + responsibilities)
    If goal_match_score > 30%:
        matched_goals += 1

Final match = (matched_goals / total_goals) × 100
```

**Keyword Matching:** 
- Breaks text into keywords (minimum 3 characters)
- Calculates intersection over union similarity
- Formula: `(matching_keywords / total_unique_keywords) × 100`

**Example:**
```
Seeker goals: ["Lead a data science team", "Work on AI/ML projects"]
Job title: "Senior Machine Learning Engineer"
Job description includes: "Build machine learning models", "Mentor junior engineers"

Goal 1 ("Lead a data science team") keywords: [lead, data, science, team]
Job keywords: [senior, machine, learning, engineer, build, models, mentor, engineers]
Overlap: [data, team] - partial match, score ~35%
Result: Matched ✓

Goal 2 ("Work on AI/ML projects") keywords: [work, artificial, intelligence, machine, learning, projects]
Job keywords: [senior, machine, learning, engineer, ...]
Overlap: [machine, learning] - strong match, score ~50%
Result: Matched ✓

Final match: 2/2 goals matched = 100%
```

## Overall Score Calculation

The overall match percentage combines all seven dimensions using weighted averaging:

```
Overall Match % = 
    (Skills × 0.30) +
    (Experience × 0.25) +
    (Location × 0.15) +
    (Salary × 0.15) +
    (Work Mode × 0.05) +
    (Work Type × 0.05) +
    (Career Goals × 0.05)
```

**Weight Rationale:**
- **Skills (30%):** Highest weight - technical capability is primary job requirement
- **Experience (25%):** Second highest - seniority/maturity is crucial for performance
- **Location (15%):** Significant but flexible due to remote work options
- **Salary (15%):** Important for both parties but often negotiable
- **Work Mode (5%):** Increasingly flexible but important for work-life balance
- **Work Type (5%):** Can be flexible but impacts commitment and predictability
- **Career Goals (5%):** Lowest weight - beneficial for long-term retention but not core

## Match Score Interpretation

| Score Range | Interpretation | Recommendation |
|------------|-----------------|-----------------|
| 85-100% | Excellent fit | Apply immediately |
| 70-84% | Good fit | Apply with competitive profile |
| 50-69% | Moderate fit | Consider as growth opportunity |
| 30-49% | Poor fit | Reconsider unless strategic |
| 0-29% | Very poor fit | Skip, focus on better matches |

## Output Format

For each seeker-opportunity match, the system generates:

1. **Overall Match Percentage** - Weighted score (0-100)
2. **Individual Dimension Scores** - Score for each of the 7 criteria
3. **Skill Analysis:**
   - Matched required skills (have)
   - Missing required skills (need to develop)
   - Matched preferred skills (bonus)
4. **Explanation** - Human-readable summary of match
5. **Recommendation** - Action item (apply, develop skills, etc.)

## Limitations and Considerations

1. **Skill Ambiguity:** Cannot assess proficiency level (intermediate vs. expert)
2. **Semantic Gaps:** Keyword matching may miss related but differently-named skills
3. **Hidden Factors:** Doesn't account for:
   - Company culture fit
   - Team dynamics
   - Growth opportunities beyond stated career goals
   - Commute considerations
4. **Bias Risks:**
   - May inadvertently favor certain skill sets
   - No explicit diversity/inclusion factors
5. **Dynamic Markets:** Doesn't account for salary/market evolution
6. **Subjective Elements:** Career goals are interpreted through keyword matching only

## Future Enhancements

- **Semantic Skill Matching:** Use word embeddings (Word2Vec, BERT) for skill similarity
- **Proficiency Levels:** Track and match skill depth (beginner/intermediate/expert)
- **Hidden Factors:** Add cultural fit, team size, growth trajectory scores
- **ML-based Weights:** Learn optimal weights from historical successful hires
- **Explainability:** Provide transparency into why certain criteria impact the score
- **Feedback Loop:** Adjust algorithm based on hire success rates
- **Diversity Metrics:** Track and optimize for inclusive hiring

## References

- **Algorithm Design:** Weighted multi-criteria decision analysis (MCDA)
- **Weight Derivation:** Domain expertise and industry standards for hiring
- **Keyword Matching:** Jaccard similarity coefficient for text comparison
- **Experience Levels:** IT industry career progression standards (Junior → Senior → Lead)

---

*Last Updated: September 1, 2026*  
*Algorithm Version: 1.0*

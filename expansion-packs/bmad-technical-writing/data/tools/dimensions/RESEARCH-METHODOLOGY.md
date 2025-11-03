# Dimension Research Methodology

**Purpose**: Standardized process for researching and documenting quality scoring dimensions
**Version**: 1.0
**Last Updated**: November 2025
**Validated On**: GLTR dimension (November 2025)

---

## Overview

This methodology ensures that every dimension in the AI Pattern Analyzer is:

1. **Grounded in peer-reviewed research** (not arbitrary)
2. **Properly validated** (claims match evidence)
3. **Transparently documented** (limitations acknowledged)
4. **Practically applicable** (implementation guidance provided)

The process uses Perplexity AI's research capabilities to conduct systematic literature reviews, validate claims, and synthesize findings from 60+ peer-reviewed sources per dimension.

---

## Research Process Flowchart

```
Step 1: Code Analysis
    ↓
Step 2: Research Question Decomposition
    ↓
Step 3: Literature Review (Deep Research)
    ↓
Step 4: Technical Validation (Reasoning)
    ↓
Step 5: Synthesis & Report Writing
    ↓
Step 6: Validation Matrix Creation
    ↓
Step 7: Recommendations Development
```

---

## Step 1: Code Analysis

**Objective**: Understand the current implementation before researching

### 1.1 Read Implementation Code

**Tool**: `Read` tool
**Target**: Locate the dimension's implementation in the codebase

**For GLTR example**:

```bash
Read: /path/to/ai_pattern_analyzer/dimensions/advanced.py
Lines: 121-200 (GLTR implementation)
```

### 1.2 Extract Key Implementation Details

Document the following from code analysis:

**A. Core Algorithm**:

- What does the dimension measure?
- What is the mathematical formula or method?
- What are the inputs and outputs?

**B. Claimed Properties**:

- What accuracy/performance is claimed in comments?
- What thresholds are defined (e.g., "AI >70%, Human <55%")?
- What research papers are cited?

**C. Scoring Logic**:

- How are raw metrics converted to scores?
- What thresholds trigger different score levels?
- Are these thresholds documented or arbitrary?

**D. Implementation Choices**:

- Which models/libraries are used?
- What are the computational requirements?
- Are there text length limits or preprocessing steps?

### 1.3 Create Initial Questions List

Based on code analysis, list all claims that need validation:

**Example from GLTR**:

- [ ] "95% accuracy on GPT-3/ChatGPT detection" - Is this validated?
- [ ] "AI >70% top-10, Human <55% top-10" - Where does this come from?
- [ ] "Research: AI >70%, Human <55%" - Which paper says this?
- [ ] "+8-10% accuracy improvement" - Is this empirically supported?

---

## Step 2: Research Question Decomposition

**Objective**: Break the dimension into researchable sub-topics

### 2.1 Create Research Query Categories

Organize research into 8-10 focused queries covering:

#### Category A: Foundational Research

**Query Template**:

```
What is [DIMENSION NAME]? Provide comprehensive overview including:
1. Original paper/research institution/authors - full citation
2. Core methodology: How does [DIMENSION] analyze text?
3. The mathematical/algorithmic approach
4. Original experimental setup and models tested
5. Key findings from the original paper about detection/quality assessment
6. Historical context and development motivation
```

**Perplexity Tool**: `deep_research`
**Rationale**: Establishes the dimension's theoretical foundation and provenance

#### Category B: Performance Validation

**Query Template**:

```
What are the validated performance metrics for [DIMENSION]? Include:
1. Accuracy rates reported in original paper
2. Whether detection was human-assisted or automated
3. Performance across different model types/domains
4. False positive rates on human-written text
5. Independent validation studies (not by original authors)
6. Performance on modern models if studied
7. How performance varies by domain/genre
8. Comparison to other detection methods
```

**Perplexity Tool**: `deep_research`
**Rationale**: Validates or refutes claimed performance metrics

#### Category C: Threshold Validation

**Query Template**:

```
What are the specific numerical thresholds for [DIMENSION]? I need exact validated thresholds:
1. What values indicate AI-generated vs human text?
2. Are the claimed thresholds [INSERT CLAIMS] validated in published research?
3. What are validated thresholds for different metrics within this dimension?
4. How do thresholds vary by model type, domain, and generation parameters?
5. What is the statistical significance of these thresholds?
6. Have any studies established universal thresholds across contexts?
```

**Perplexity Tool**: `reason`
**Rationale**: Validates specific numerical claims in code comments

#### Category D: Technical Implementation

**Query Template**:

```
What are the technical implementation details and best practices for [DIMENSION]? Include:
1. Required computational resources (memory, processing time)
2. Choice of models/algorithms (alternatives and trade-offs)
3. Input size limits and preprocessing requirements
4. Implementation algorithms and complexity
5. Real-time vs batch processing capabilities
6. Integration approaches with existing pipelines
7. Computational complexity and scalability
8. Open-source implementations and libraries available
```

**Perplexity Tool**: `deep_research`
**Rationale**: Provides practical implementation guidance

#### Category E: Quality Scoring Applications

**Query Template**:

```
How can [DIMENSION] be used for content quality scoring beyond AI detection? Research:
1. Using [DIMENSION] for assessing writing quality
2. Identifying specific quality issues (e.g., formulaic patterns, low diversity)
3. Measuring quality dimensions (creativity, sophistication, clarity)
4. Detecting specific writing problems
5. Evaluating different writing genres (technical, creative, academic)
6. Applications in education for assessing development
7. Professional editing and content improvement use cases
8. Correlation between [DIMENSION] metrics and human quality judgments
9. Adapting [DIMENSION] for style/voice analysis
```

**Perplexity Tool**: `deep_research`
**Rationale**: Explores applications beyond binary AI detection

#### Category F: Limitations and Failures

**Query Template**:

```
What are the documented limitations, failure modes, and false positive scenarios for [DIMENSION]? Include specific examples:
1. Types of human writing that trigger false positives (technical, ESL, domains)
2. Generation strategies that evade detection (sampling methods, parameters)
3. Adversarial attacks (paraphrasing, manipulation techniques)
4. Multilingual limitations and cross-language performance
5. Performance on mixed human-AI collaborative text
6. Edge cases where [DIMENSION] produces unreliable results
7. Known biases (favoring certain writing styles, populations)
8. Degradation over time as models improve
```

**Perplexity Tool**: `reason`
**Rationale**: Identifies when NOT to use the dimension

#### Category G: Contemporary Alternatives

**Query Template**:

```
What are contemporary improvements and alternatives to [DIMENSION]? Research:
1. [List specific alternative methods relevant to this dimension]
2. Recent 2024-2025 methods and innovations
3. Comparative performance benchmarks
4. Hybrid approaches combining multiple signals
5. Domain-adaptive and cross-model generalization techniques
6. Advantages/disadvantages vs original [DIMENSION]
```

**Perplexity Tool**: `deep_research`
**Rationale**: Positions dimension within current state-of-the-art

#### Category H: Best Practices

**Query Template**:

```
What are research-validated best practices for implementing [DIMENSION]? Need specific guidance on:
1. Optimal threshold selection for different use cases
2. When to use different variants/models
3. Handling edge cases (short texts, code, multilingual)
4. Combining [DIMENSION] with other signals for improved accuracy
5. Setting confidence levels and when to trigger human review
6. Domain adaptation strategies (technical, academic, creative writing)
7. Handling temporal drift as models evolve
8. Avoiding false positives with diverse populations
```

**Perplexity Tool**: `reason`
**Rationale**: Provides actionable implementation guidance

### 2.2 Query Execution Strategy

**Parallel Execution**: Run multiple queries simultaneously when possible

```python
# Execute 3-4 queries in parallel
parallel_queries = [
    "Foundational Research",
    "Performance Validation",
    "Technical Implementation",
    "Contemporary Alternatives"
]
```

**Sequential Execution**: Run follow-up queries after initial results

```python
# Execute after analyzing initial results
followup_queries = [
    "Threshold Validation" (based on specific claims found),
    "Limitations" (based on methods identified),
    "Best Practices" (based on implementation details)
]
```

### 2.3 Source Quality Requirements

**Prioritize**:

- ✅ Peer-reviewed conference papers (ACL, EMNLP, NeurIPS, ICML)
- ✅ Peer-reviewed journals (Nature, Science, TACL, Computational Linguistics)
- ✅ arXiv preprints with 10+ citations
- ✅ Technical reports from major research institutions (Google, OpenAI, Meta)

**Deprioritize**:

- ⚠️ Blog posts (use only for context, not claims)
- ⚠️ Medium articles (supplementary only)
- ⚠️ Marketing materials (highly biased)
- ❌ Uncited claims or anonymous sources

---

## Step 3: Literature Review Execution

**Objective**: Conduct systematic research using Perplexity

### 3.1 Execute Queries

**Use TodoWrite** to track progress:

```python
TodoWrite([
    {"content": "Research [Dimension] methodology and original paper",
     "status": "in_progress"},
    {"content": "Research [Dimension] performance metrics",
     "status": "pending"},
    # ... etc
])
```

**Run Perplexity Queries**:

```python
# Deep research for comprehensive topics
mcp__perplexity__deep_research(query=foundational_query)
mcp__perplexity__deep_research(query=performance_query)

# Reasoning for specific technical questions
mcp__perplexity__reason(query=threshold_query)
mcp__perplexity__reason(query=best_practices_query)
```

### 3.2 Document Sources

**For Each Query Result**:

- Note the number of sources cited (aim for 15-30 per query)
- Identify the highest-quality sources (conference papers, journals)
- Extract specific numerical values with citations
- Note contradictions between sources
- Flag claims that lack supporting evidence

### 3.3 Evidence Quality Rating

Rate each finding:

| Rating             | Criteria                            | Example                                  |
| ------------------ | ----------------------------------- | ---------------------------------------- |
| 🟢 **High**        | Peer-reviewed, replicated, n>100    | "72% detection in n=35 study (ACL 2019)" |
| 🟡 **Medium**      | Peer-reviewed, single study, n<100  | "65% detection in pilot study (arXiv)"   |
| 🟠 **Low**         | Technical report, not peer-reviewed | "Claimed 80% in OpenAI blog post"        |
| 🔴 **No Evidence** | No supporting source found          | "95% accuracy - NOT FOUND"               |

---

## Step 4: Claim Validation Matrix

**Objective**: Systematically validate every claim in the code

### 4.1 Create Validation Matrix

**Template**:

```markdown
| Claim in Code    | Source Citation  | Validated? | Actual Finding                      |
| ---------------- | ---------------- | ---------- | ----------------------------------- |
| "95% accuracy"   | None found       | ❌         | Actual: 72% human-assisted          |
| "AI >70% top-10" | Observed pattern | ⚠️         | Pattern exists but not universal    |
| "Works on GPT-4" | Not studied      | ❌         | Performance degrades on modern LLMs |
```

**Evidence Categories**:

- ✅ **Validated**: Direct peer-reviewed evidence supporting the claim
- ⚠️ **Partial**: Some evidence but with caveats or context-dependency
- ❌ **Refuted**: Evidence contradicts the claim
- ❓ **No Evidence**: No research found addressing this claim

### 4.2 Quantify Discrepancies

**For numerical claims**, document exact discrepancies:

```markdown
**Claim**: "95% accuracy on GPT-3/ChatGPT detection"
**Evidence**: Original paper reports 72% accuracy with human assistance on GPT-2
**Discrepancy**: +23 percentage points, wrong model, human-assisted vs automated
**Severity**: CRITICAL - major overstatement
```

### 4.3 Flag Critical Issues

**Identify** claims that are:

1. **Contradicted by evidence** (most serious)
2. **Unsubstantiated** (no supporting research)
3. **Misattributed** (citation doesn't support claim)
4. **Context-dependent** (true only in specific conditions)
5. **Outdated** (was true but no longer accurate)

---

## Step 5: Synthesis and Report Writing

**Objective**: Create comprehensive, actionable documentation

### 5.1 Report Structure Template

```markdown
# [DIMENSION NAME] - Comprehensive Dimension Report

**Document Status**: Research Complete
**Research Date**: [Date]
**Research Quality Score**: X/10
**Dimension Category**: [Category]
**Points Allocated**: X/210

---

## Executive Summary

[2-3 paragraphs + validation matrix]

## 1. What is [DIMENSION]? Foundational Methodology

### 1.1 Core Concept

### 1.2 Mathematical/Algorithmic Approach

### 1.3 Historical Development

## 2. Technical Implementation Architecture

### 2.1 Current Implementation (code reference)

### 2.2 Computational Requirements

### 2.3 Algorithm Options/Variants

## 3. Performance Metrics - Research Validation

### 3.1 Original Research Study

### 3.2 Independent Validation Studies

### 3.3 False Positive Rates

### 3.4 Performance Across Contexts

### 3.5 Adversarial Robustness

## 4. AI Detection Applications

### 4.1 Primary Use Cases

### 4.2 Optimal Application Contexts

### 4.3 Current Scoring Logic

### 4.4 Validation of Thresholds

## 5. Content Quality Scoring Applications

### 5.1 [Quality Dimension 1]

### 5.2 [Quality Dimension 2]

### 5.3 [Quality Dimension 3]

### 5.4 Limitations for Quality Scoring

## 6. Documented Limitations and Failure Modes

### 6.1 Model-Specific Limitations

### 6.2 False Positive Scenarios

### 6.3 Cross-Domain Failures

### 6.4 Temporal Drift

### 6.5 Adversarial Vulnerabilities

### 6.6 Computational Limitations

## 7. Contemporary Alternatives and Improvements

### 7.1 [Alternative Method 1]

### 7.2 [Alternative Method 2]

### 7.3 [Alternative Method 3]

### 7.4 Comparative Performance

## 8. Best Practices for Implementation

### 8.1 When to Use [DIMENSION]

### 8.2 Threshold Selection

### 8.3 Model/Algorithm Selection

### 8.4 Handling Edge Cases

### 8.5 Integration with Ensembles

### 8.6 Avoiding False Positives

### 8.7 Temporal Maintenance

## 9. Recommendations for AI Pattern Analyzer

### 9.1 Current Implementation Assessment

### 9.2 Immediate Recommendations (Priority 1)

### 9.3 Medium-Term (Priority 2)

### 9.4 Long-Term (Priority 3)

### 9.5 Quality Scoring Integration

## 10. Research Quality Assessment

### 10.1 Evidence Quality Ratings

### 10.2 Research Gaps

## 11. References and Further Reading

### 11.1 Foundational Papers

### 11.2 Validation Studies

## 12. Conclusion

[Summary + overall assessment]
```

### 5.2 Writing Guidelines

**Tone**: Academic but accessible
**Length**: 30-60 pages (10,000-15,000 words)
**Citations**: Inline [1] format with numbered sources
**Code**: Include implementation examples where relevant

**Structure Each Section**:

1. **Summary paragraph**: Main takeaway
2. **Detailed analysis**: Evidence and findings
3. **Practical implications**: What this means for users
4. **Visual aids**: Tables, matrices, code examples where helpful

### 5.3 Critical Elements

**Must Include**:

- ✅ Executive summary with validation status
- ✅ Claim validation matrix
- ✅ False positive analysis
- ✅ Evidence quality ratings
- ✅ Concrete recommendations with priorities
- ✅ Complete bibliography

**Must Avoid**:

- ❌ Uncited claims
- ❌ Marketing language ("best in class", "revolutionary")
- ❌ Assumptions without evidence
- ❌ Ignoring contradictory findings

---

## Step 6: Validation Matrix Creation

**Objective**: Provide at-a-glance validation status

### 6.1 Comprehensive Validation Matrix

**Template**:

```markdown
| Metric/Claim | Peer-Reviewed | AI Detection Validated | Thresholds Valid | Recommendation |
| ------------ | ------------- | ---------------------- | ---------------- | -------------- |
| [Metric 1]   | ✓/✗           | ✓/✗/Partial            | ✓/✗              | [Action]       |
| [Metric 2]   | ✓/✗           | ✓/✗/Partial            | ✓/✗              | [Action]       |
```

**Example from GLTR**:

```markdown
| Metric   | Peer-Reviewed         | AI Detection Validated        | Claimed Thresholds Valid | Recommendation                         |
| -------- | --------------------- | ----------------------------- | ------------------------ | -------------------------------------- |
| **GLTR** | ✓ Yes (ACL 2019)      | Partial (72% human-assisted)  | ✗ No (95% not validated) | Update claims; add disclaimers         |
| **HDD**  | ✓ Yes (McCarthy 2010) | ✗ No (only lexical diversity) | ✗ No (ranges not found)  | Remove thresholds or mark experimental |
```

### 6.2 Research Quality Score

**Calculate overall quality** (0-10 scale):

**Scoring Criteria**:

- **Peer-reviewed foundation**: +3 points (foundational paper exists)
- **Independent validation**: +2 points (replicated by others)
- **Threshold validation**: +2 points (specific values validated)
- **Low false positives**: +1 point (<5% FP rate documented)
- **Contemporary relevance**: +1 point (works on modern LLMs)
- **Robustness**: +1 point (resists adversarial attacks)

**Penalty Criteria**:

- **Major claim refuted**: -2 points per claim
- **No supporting evidence**: -1 point per unsubstantiated claim
- **High false positives**: -1 point (>10% FP rate)

**Example**: GLTR scored 9/10 (strong foundation, validated, but claims need correction)

---

## Step 7: Recommendations Development

**Objective**: Provide actionable next steps

### 7.1 Three-Tier Priority System

**Priority 1 (Immediate)** - Can be done in 1-2 days:

- Update documentation to reflect research findings
- Add validation warnings to code comments
- Implement confidence intervals (not binary thresholds)
- Fix critical bugs or misconfigurations

**Priority 2 (Medium-Term)** - Can be done in 1-2 weeks:

- Expand analysis coverage (longer texts, more metrics)
- Add alternative detection methods
- Implement domain-specific adaptations
- Improve error handling and edge cases

**Priority 3 (Long-Term)** - Requires 1+ months:

- Migrate to ensemble architecture
- Train domain-specific models
- Implement adversarial robustness
- Add explainability features

### 7.2 Recommendation Template

**For Each Recommendation**:

````markdown
**[NUMBER]. [RECOMMENDATION TITLE]**

**Problem**: [What's wrong currently]
**Solution**: [What to do]
**Impact**: [HIGH/MEDIUM/LOW]
**Effort**: [1-2 days / 1-2 weeks / 1+ months]
**Priority**: [1/2/3]

**Implementation**:

```python
# Code example if applicable
```
````

**Expected Outcome**: [Measurable improvement]

````

### 7.3 Quality Scoring Integration

**Separate section** for how dimension can be used beyond AI detection:
```markdown
### 9.5 Content Quality Scoring Integration

**Add Quality Metrics Module**:
```python
class [Dimension]QualityMetrics:
    """Uses [DIMENSION] for writing quality, not just AI detection"""

    def assess_[quality_aspect_1](self) -> Dict:
        """Description and methodology"""

    def assess_[quality_aspect_2](self) -> Dict:
        """Description and methodology"""
````

**Use Cases**:

- Educational: [specific feedback students receive]
- Professional: [how editors use this]
- Technical: [how technical writers benefit]

```

---

## Step 8: Quality Control Checklist

**Before Finalizing Report**:

### 8.1 Completeness Check

- [ ] All 8 research queries executed and documented
- [ ] 60+ peer-reviewed sources cited
- [ ] Every claim in code validated or refuted
- [ ] Validation matrix completed
- [ ] Research quality score calculated
- [ ] All 12 report sections written
- [ ] Recommendations with clear priorities
- [ ] Complete bibliography

### 8.2 Accuracy Check

- [ ] All numerical values have citations
- [ ] No uncited claims
- [ ] Contradictory findings acknowledged
- [ ] Limitations clearly stated
- [ ] Alternative methods fairly compared
- [ ] Code examples tested and correct

### 8.3 Usefulness Check

- [ ] Actionable recommendations provided
- [ ] Clear guidance on when to use/not use
- [ ] Domain-specific considerations addressed
- [ ] False positive scenarios documented
- [ ] Integration guidance provided
- [ ] Quality scoring applications explored

---

## Step 9: Documentation Storage

**File Naming Convention**:
```

[DIMENSION-NAME]-dimension-report.md

```

**Examples**:
- `GLTR-dimension-report.md` ✅
- `HDD-dimension-report.md`
- `MATTR-dimension-report.md`
- `structure-dimension-report.md`

**Location**:
```

/path/to/tools/dimensions/[DIMENSION-NAME]-dimension-report.md

````

**Metadata Block** (at top of each report):
```markdown
# [DIMENSION NAME] - Comprehensive Dimension Report

**Document Status**: Research Complete
**Research Date**: November 2025
**Research Quality Score**: X/10 (with justification)
**Dimension Category**: [Advanced Detection / Lexical / Structural / etc.]
**Points Allocated**: X/210 (Y% of total score)
**Research Conducted By**: AI Research Analysis (Perplexity)
**Validation Status**: [Complete / Partial / Needs Review]
````

---

## Step 10: Meta-Analysis Across Dimensions

**After Completing Multiple Dimensions**:

### 10.1 Cross-Dimension Comparison

Create comparative analysis:

```markdown
# Dimension Comparison Matrix

| Dimension | Research Quality | Threshold Valid | False Positive | Modern LLM | Recommended Use     |
| --------- | ---------------- | --------------- | -------------- | ---------- | ------------------- |
| GLTR      | 9/10             | ⚠️ Partial      | 5-10%          | ❌ Poor    | Supplementary (20%) |
| HDD       | ?/10             | ?               | ?              | ?          | TBD                 |
| MATTR     | ?/10             | ?               | ?              | ?          | TBD                 |
```

### 10.2 Ensemble Architecture Design

**Based on research findings**, recommend optimal weighting:

```python
DIMENSION_WEIGHTS = {
    'GLTR': 0.20,  # Interpretable but limited
    'HDD': 0.15,   # TBD based on research
    'MATTR': 0.15, # TBD based on research
    'DetectGPT': 0.25,  # Modern, effective
    'Binoculars': 0.25, # High accuracy
}
```

### 10.3 Implementation Roadmap

**Create master roadmap** across all dimensions:

```markdown
## Phase 1: Research & Documentation (Complete by: Date)

- [x] GLTR research complete
- [ ] HDD research
- [ ] MATTR research
- [ ] Yule's K research
      ...

## Phase 2: Critical Fixes (Complete by: Date)

- [ ] Fix GLTR thresholds
- [ ] Add HDD validation warnings
      ...

## Phase 3: Ensemble Integration (Complete by: Date)

- [ ] Design hybrid architecture
- [ ] Implement weighted voting
      ...
```

---

## Appendix A: Research Query Library

### A.1 Foundational Research Query Template

```
What is [DIMENSION]? Provide comprehensive overview including:
1. Original paper/research institution/authors - full citation, DOI if available
2. Core methodology: How does [DIMENSION] analyze/measure text?
3. Mathematical formula or algorithmic approach (be specific)
4. Original experimental setup: What models/data were tested?
5. Original context: What problem was this designed to solve?
6. Key findings from original paper about [detection/quality/measurement]
7. Subsequent developments: How has research built on this foundation?
8. Current status: Is this method still widely used or superseded?
```

### A.2 Performance Validation Query Template

```
What are the validated performance metrics for [DIMENSION] in [detecting AI text / measuring quality]? Include:
1. Accuracy rates reported in original paper (with sample sizes, test sets)
2. Whether reported performance was human-assisted or fully automated
3. Performance on different model types (GPT-2, GPT-3, GPT-4, BERT, etc.)
4. False positive rates on confirmed human-written text
5. False negative rates on confirmed AI-generated text
6. Any independent validation studies by other researchers
7. Performance on modern models (2023-2025 if studied)
8. How performance varies by domain (news, academic, creative, social media)
9. Comparative performance vs other methods in benchmark studies
10. Confidence intervals, statistical significance of results
```

### A.3 Threshold Validation Query Template

```
What are the specific, research-validated numerical thresholds for [DIMENSION]? I need exact values from peer-reviewed sources:
1. What [metric values] indicate AI-generated text? (cite specific studies)
2. What [metric values] indicate human-written text? (cite specific studies)
3. Are the claimed thresholds [INSERT SPECIFIC CLAIMS FROM CODE] validated in published research?
4. What are validated thresholds for sub-metrics within [DIMENSION]?
5. How do these thresholds vary by:
   - Source model type (GPT-2 vs GPT-3 vs GPT-4)
   - Text domain (technical vs creative vs academic)
   - Generation parameters (temperature, top-p, etc.)
   - Text length (short vs long documents)
6. What is the statistical significance of these thresholds? (p-values, confidence intervals)
7. Have any studies established universal thresholds that work across different contexts?
8. What caveats or context-dependencies are documented?
```

### A.4 Technical Implementation Query Template

```
What are the technical implementation details and best practices for [DIMENSION]? Include:
1. Required computational resources:
   - Memory requirements (RAM, VRAM)
   - Processing time benchmarks
   - Hardware recommendations (CPU vs GPU)
2. Choice of algorithms/models:
   - Standard implementation approach
   - Alternative algorithms/variants
   - Trade-offs between options
3. Input specifications:
   - Token/character limits
   - Minimum text length for reliable results
   - Preprocessing requirements
4. Algorithm complexity:
   - Time complexity (Big O notation)
   - Space complexity
   - Scalability characteristics
5. Processing modes:
   - Real-time vs batch processing capabilities
   - Parallelization potential
6. Integration approaches:
   - API design patterns
   - Pipeline integration strategies
   - Compatibility with existing tools
7. Open-source resources:
   - Available libraries (Python, JavaScript, etc.)
   - Reference implementations
   - Benchmark datasets
8. Performance optimization:
   - Acceleration techniques
   - Approximation methods
   - Caching strategies
```

### A.5 Quality Scoring Query Template

```
How can [DIMENSION] be used for content quality scoring beyond binary AI detection? Research:
1. Theoretical basis: Why would [DIMENSION] correlate with quality?
2. Quality dimensions assessed:
   - Writing sophistication
   - Creativity and originality
   - Clarity and readability
   - Stylistic consistency
   - Vocabulary richness
3. Identifying quality issues:
   - Formulaic or template-based writing
   - Clichés and overused phrases
   - Lack of diversity
   - Unclear transitions
4. Genre-specific applications:
   - Technical writing quality
   - Creative writing assessment
   - Academic writing evaluation
   - Business communication
5. Educational applications:
   - Tracking student writing development
   - Providing constructive feedback
   - Identifying areas for improvement
6. Professional applications:
   - Editorial assessment
   - Content optimization
   - Brand voice consistency
7. Empirical validation:
   - Studies correlating [DIMENSION] with human quality judgments
   - Reliability and validity evidence
   - Inter-rater agreement
8. Limitations for quality assessment:
   - What aspects of quality can't be measured?
   - Context-dependencies
   - Cultural/linguistic biases
```

### A.6 Limitations Query Template

```
What are the documented limitations, failure modes, and false positive scenarios for [DIMENSION]? Include specific examples from research:
1. False positive triggers (human text incorrectly flagged):
   - Technical/domain-specific writing
   - ESL/non-native writers
   - Specific writing styles or genres
   - Regional or dialectal variations
   - Accessibility considerations (assistive tech users)
2. Generation strategies that evade detection:
   - Specific sampling methods (temperature, top-p, top-k)
   - Model architectures that defeat detection
   - Parameter settings that reduce detectability
3. Adversarial attacks:
   - Paraphrasing effectiveness
   - Synonym replacement
   - Sentence reordering
   - Back-translation
   - Targeted evasion techniques
4. Cross-linguistic issues:
   - Performance on non-English languages
   - Multilingual text handling
   - Translation artifacts
5. Mixed authorship:
   - Human-AI collaborative text
   - Partially edited AI content
   - Human text with AI refinement
6. Edge cases:
   - Very short texts
   - Code-heavy documents
   - Lists, tables, structured data
   - Quoted material
7. Systemic biases:
   - Demographic biases (age, education, native language)
   - Genre biases (favoring certain writing types)
   - Temporal biases (older vs newer writing)
8. Temporal degradation:
   - Performance on newer models not seen during development
   - Obsolescence timeline
   - Adaptation challenges
```

### A.7 Contemporary Alternatives Query Template

```
What are contemporary improvements and alternatives to [DIMENSION] for [AI detection / quality assessment]? Research:
1. Direct improvements:
   - Enhanced versions of [DIMENSION]
   - Variants addressing specific limitations
   - Recent refinements (2023-2025)
2. Alternative methodologies:
   - [List 3-5 specific alternatives relevant to this dimension]
   - Fundamentally different approaches
   - Complementary methods
3. Performance comparisons:
   - Head-to-head benchmark results
   - Domain-specific performance differences
   - Computational efficiency comparisons
4. Recent innovations (2024-2025):
   - Transformer-based alternatives
   - Zero-shot methods
   - Ensemble approaches
   - Watermarking techniques
5. Hybrid approaches:
   - Methods combining [DIMENSION] with others
   - Ensemble architectures
   - Multi-signal detection
6. Domain-adaptive methods:
   - Techniques for cross-domain generalization
   - Fine-tuning strategies
   - Transfer learning approaches
7. Robustness improvements:
   - Adversarially-trained alternatives
   - Perturbation-resistant methods
8. Practical considerations:
   - Commercial vs open-source tools
   - Deployment complexity
   - Cost-benefit analysis
```

### A.8 Best Practices Query Template

```
What are research-validated best practices for implementing [DIMENSION]-based [detection/assessment] systems? Need specific guidance on:
1. Threshold selection:
   - How to determine optimal thresholds for your use case
   - Calibration procedures
   - Balancing false positives vs false negatives
   - Domain-specific threshold adjustment
2. Model/variant selection:
   - When to use [Option A] vs [Option B]
   - Trade-offs between accuracy and efficiency
   - Hardware/resource constraints
3. Edge case handling:
   - Minimum text length thresholds
   - Handling code, tables, lists
   - Multilingual content processing
   - Structured vs unstructured text
4. Signal combination:
   - How to combine [DIMENSION] with other methods
   - Weighting strategies
   - Ensemble architectures
   - Conflict resolution
5. Confidence calibration:
   - Setting appropriate confidence levels
   - When to trigger human review
   - Uncertainty quantification
   - Probabilistic vs binary outputs
6. Domain adaptation:
   - Strategies for technical writing
   - Academic writing considerations
   - Creative writing special cases
   - Social media/informal content
7. Temporal maintenance:
   - How to detect performance degradation
   - Re-calibration schedules
   - Model updating strategies
   - Handling new LLM generations
8. Bias mitigation:
   - Avoiding false positives with ESL writers
   - Addressing demographic biases
   - Testing across diverse populations
   - Fairness evaluation
9. Operational guidance:
   - When to use [DIMENSION] vs alternatives
   - Appropriate vs inappropriate use cases
   - Ethical considerations
   - Transparency requirements
```

---

## Appendix B: Evidence Quality Rubric

### B.1 Source Quality Tiers

**Tier 1 (Highest Quality)** - Weight: 1.0

- Peer-reviewed conference papers (ACL, EMNLP, NeurIPS, ICML, ICLR)
- Peer-reviewed journals (Nature, Science, TACL, Computational Linguistics)
- Replicated findings (multiple independent studies)

**Tier 2 (High Quality)** - Weight: 0.8

- arXiv preprints with 10+ citations
- Workshop papers at major conferences
- Technical reports from major research labs (Google, OpenAI, Meta, Microsoft)

**Tier 3 (Medium Quality)** - Weight: 0.5

- arXiv preprints with <10 citations
- University technical reports
- Industry whitepapers with data

**Tier 4 (Low Quality)** - Weight: 0.2

- Blog posts from researchers (with data)
- Conference talks/presentations
- Documentation from established tools

**Tier 5 (Anecdotal)** - Weight: 0.0

- Marketing materials
- Unsupported blog posts
- Social media claims
- Anonymous sources

### B.2 Claim Strength Assessment

**Strong Evidence** (Can make definitive statements):

- Multiple Tier 1 sources agree (3+ papers)
- Large sample sizes (n>100)
- Replicated across institutions
- Statistical significance reported (p<0.05)

**Moderate Evidence** (Can state with caveats):

- Single Tier 1 source OR multiple Tier 2 sources
- Moderate sample sizes (n=30-100)
- Limited replication
- Trends clear but not conclusive

**Weak Evidence** (Must hedge heavily):

- Only Tier 3-4 sources
- Small sample sizes (n<30)
- No replication
- Preliminary or exploratory

**No Evidence** (Cannot make claim):

- Only Tier 5 sources or no sources
- Direct contradiction by higher-tier sources
- Logical inconsistency

---

## Appendix C: Common Research Pitfalls

### C.1 Avoid These Mistakes

**1. Accepting Claims at Face Value**

- ❌ Problem: Code comment says "95% accuracy" → assume it's true
- ✅ Solution: Verify every claim against peer-reviewed sources

**2. Confirming Code Comments from Wrong Papers**

- ❌ Problem: Paper cited discusses the metric but not the specific thresholds claimed
- ✅ Solution: Read papers carefully; check if specific values appear

**3. Ignoring Contradictory Evidence**

- ❌ Problem: Finding one source supporting claim, ignoring three that refute it
- ✅ Solution: Document all findings; acknowledge contradictions

**4. Overgeneralizing from Limited Studies**

- ❌ Problem: Single study on GPT-2 → claim applies to all LLMs
- ✅ Solution: Specify exactly what was studied; note limitations

**5. Confusing Correlation with Causation**

- ❌ Problem: Metric correlates with AI text → metric "detects" AI generation
- ✅ Solution: Distinguish correlation from validated detection

**6. Missing Context-Dependencies**

- ❌ Problem: 90% accuracy reported → apply universally
- ✅ Solution: Document: accuracy on what data, from what domain, on what models

**7. Using Outdated Research**

- ❌ Problem: 2019 paper's findings → assume still true for 2025 models
- ✅ Solution: Prioritize recent research; note when findings are dated

**8. Ignoring Negative Results**

- ❌ Problem: Only citing successful detection studies
- ✅ Solution: Include studies showing failures, limitations, false positives

---

## Appendix D: Report Quality Self-Assessment

**Before submitting report**, score it on these criteria:

### D.1 Completeness (30 points)

- [ ] All 8 research queries executed (10 pts)
- [ ] Every code claim validated (10 pts)
- [ ] All 12 report sections complete (10 pts)

### D.2 Evidence Quality (30 points)

- [ ] 60+ sources cited (10 pts)
- [ ] Majority (>60%) are Tier 1-2 sources (10 pts)
- [ ] All numerical claims have citations (10 pts)

### D.3 Validation Rigor (20 points)

- [ ] Validation matrix completed (5 pts)
- [ ] Research quality score justified (5 pts)
- [ ] Contradictory findings acknowledged (5 pts)
- [ ] Limitations clearly documented (5 pts)

### D.4 Actionability (20 points)

- [ ] Recommendations with clear priorities (10 pts)
- [ ] Implementation guidance provided (5 pts)
- [ ] Quality scoring applications explored (5 pts)

**Total Score**: \_\_\_ / 100

**Grading Scale**:

- 90-100: Excellent - Ready for use
- 80-89: Good - Minor revisions needed
- 70-79: Acceptable - Significant gaps to address
- <70: Incomplete - Major work required

---

## Usage Instructions

### For Each New Dimension:

1. **Copy this methodology document**
2. **Execute Step 1**: Analyze code implementation
3. **Execute Step 2**: Create 8 research queries customized for this dimension
4. **Execute Step 3-4**: Run queries, validate claims
5. **Execute Step 5-7**: Write report, create matrices, develop recommendations
6. **Execute Step 8**: Quality control checklist
7. **Execute Step 9**: Save report with proper naming/metadata
8. **Execute Step 10** (after multiple dimensions): Cross-dimension analysis

### Estimated Timeline:

- **Initial research**: 2-3 hours (running all queries)
- **Analysis & validation**: 1-2 hours (reviewing results, building matrices)
- **Report writing**: 2-3 hours (synthesis, recommendations)
- **Quality control**: 30-60 minutes (checklist, proofreading)

**Total per dimension**: 6-9 hours

---

## Version History

| Version | Date     | Changes                                         |
| ------- | -------- | ----------------------------------------------- |
| 1.0     | Nov 2025 | Initial methodology validated on GLTR dimension |

---

## Contact & Feedback

This methodology should be treated as a living document. As we research more dimensions, we may discover improvements to the process.

**Suggested improvements**: Document in METHODOLOGY-UPDATES.md

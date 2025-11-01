# Task: Humanization Quality Assurance Check

<!-- Powered by BMAD" Core -->

## Purpose

Validate that humanization efforts have successfully removed AI patterns and that content now reads as authentically human-written. Uses quantitative analysis combined with qualitative review to ensure publication-ready quality.

## When to Use This Task

- **After completing humanization editing** (post-generation workflow completion)
- Before submitting content for technical or editorial review
- As final quality gate before publication
- When validating improvements from humanization efforts
- To establish publication-readiness for AI-assisted content

## Prerequisites

- Content that has undergone humanization editing
- Python 3.7+ installed for quantitative analysis
- AI Pattern Analysis Tool (`{{config.root}}/tools/analyze_ai_patterns.py`)
- Before-humanization baseline metrics (recommended for comparison)
- 20-30 minutes for comprehensive QA check

## Workflow Steps

### 0. Load Configuration

- Read `.bmad-technical-writing/config.yaml` to resolve paths
- Extract: `config.manuscript.root`, `config.manuscript.sections`, `config.manuscript.chapters`
- If config not found, use defaults: `manuscript/`, `manuscript/sections`, `manuscript/chapters`

### 1. Run Quantitative Analysis

**Execute AI pattern analysis on humanized content**:

```bash
cd {{config.root}}/tools
python3 analyze_ai_patterns.py PATH_TO_HUMANIZED_FILE \
  --domain-terms "Domain,Specific,Terms" \
  > humanization-qa-report.txt
```

**Example**:
```bash
python3 analyze_ai_patterns.py ../{{config.manuscript.chapters}}/chapter-03.md \
  --domain-terms "Docker,Kubernetes,PostgreSQL" \
  > chapter-03-qa-report.txt
```

**Review the output**: Check all 6 dimension scores and overall assessment.

### 2. Evaluate Publication Readiness Thresholds

**Target scores for publication-ready content**:

| Dimension | Minimum Target | Ideal Target | Red Flag |
|-----------|----------------|--------------|----------|
| Perplexity | MEDIUM | HIGH | LOW or VERY LOW |
| Burstiness | MEDIUM | HIGH | LOW or VERY LOW |
| Structure | MEDIUM | HIGH | LOW with 4+ heading levels |
| Voice | MEDIUM | HIGH | VERY LOW (no personal markers) |
| Technical | MEDIUM | HIGH | Context-dependent |
| Formatting | MEDIUM | HIGH | VERY LOW (3+ em-dashes/page) |

**Overall Assessment**:
- **PASS**: MINIMAL or LIGHT humanization needed (<10% AI patterns)
- **CONDITIONAL PASS**: MODERATE humanization needed (10-20% AI patterns, but specific issues identified and acceptable)
- **FAIL**: SUBSTANTIAL or EXTENSIVE humanization needed (>20% AI patterns)

### 3. Check Critical AI Signals

**Verify strongest AI detection signals have been addressed**:

**Em-Dash Density** (Strongest Signal):
- [ ] Em-dashes per page: d2 (target: 1-2 max)
- [ ] If 3+: **FAIL** - Must reduce before publication

**Heading Hierarchy Depth**:
- [ ] Maximum heading depth: d3 levels (H1, H2, H3)
- [ ] If 4+: **CONDITIONAL FAIL** - Should flatten unless architecturally justified

**AI Vocabulary Density**:
- [ ] AI words per 1k: d5 (target: d2)
- [ ] If >10: **FAIL** - Must replace obvious AI markers

**Sentence Uniformity**:
- [ ] Standard deviation: e6 (target: e10)
- [ ] If <3: **FAIL** - Must add sentence variation

### 4. Qualitative "Read Aloud" Test

**Read 3-5 representative paragraphs aloud**:

**Listen for**:
- [ ] Natural flow and rhythm (sounds like human speech)
- [ ] No awkward phrasings that cause stumbling
- [ ] Varied sentence rhythm (not monotonous)
- [ ] Conversational connectors (not formulaic)
- [ ] Personal voice present (where appropriate)

**Red Flags**:
- Sounds robotic or mechanical when spoken
- Formulaic transitions stand out ("Furthermore," "Moreover")
- Uniform rhythm creates monotony
- Lacks human spontaneity

**Action**: If read-aloud test fails, apply additional Pass 3 and Pass 4 humanization edits (sentence variation, voice refinement).

### 5. Verify Technical Accuracy Preservation

**Critical check**: Ensure humanization didn't introduce errors.

**Review**:
- [ ] Code examples still functional
- [ ] Technical terminology remains correct
- [ ] Version numbers and specifics unchanged
- [ ] Procedures and commands still accurate
- [ ] No facts altered during editing

**Test** (if applicable):
- [ ] Run code examples to verify functionality
- [ ] Validate commands in appropriate environment
- [ ] Cross-check technical claims against documentation

**Action**: If technical accuracy compromised, revert problematic edits and re-humanize more carefully.

### 6. Compare Before/After Metrics (If Available)

**If baseline metrics exist from pre-humanization analysis**:

**Expected improvements**:
- AI vocabulary per 1k: **Decreased 50-80%**
- Sentence StdDev: **Increased** (higher burstiness)
- Formulaic transitions: **Decreased to <3**
- Heading depth: **Decreased to d3**
- Em-dashes per page: **Decreased to 1-2**
- Overall assessment: **Improved 1-2 levels**

**Document improvement**:
```
Before Humanization:
- Perplexity: LOW (12.4 AI words/1k)
- Burstiness: LOW (StdDev 4.2)
- Formatting: VERY LOW (7.8 em-dashes/page)
- Overall: SUBSTANTIAL humanization required

After Humanization:
- Perplexity: MEDIUM (3.1 AI words/1k)
- Burstiness: HIGH (StdDev 11.7)
- Formatting: HIGH (1.4 em-dashes/page)
- Overall: LIGHT humanization needed

Improvement: 75% reduction in AI patterns 
```

### 7. Publisher AI Compliance Check (Optional)

**If publisher has AI content policies**:

**Common publisher requirements**:
- Content must sound authentically human-written
- AI-assisted content must be disclosed (check submission guidelines)
- Detection software should not flag content as AI-generated
- Author must certify substantial human authorship

**Validation**:
- [ ] Overall assessment: MINIMAL or LIGHT humanization needed
- [ ] No dimension scored VERY LOW
- [ ] Em-dash test passed (d2 per page)
- [ ] Read-aloud test passed (sounds natural)
- [ ] Technical accuracy preserved (100%)

**Action**: If publisher compliance uncertain, aim for "MINIMAL humanization needed" overall score.

### 8. Make Final Decision

**Publication Readiness Decision Matrix**:

| Scenario | Decision | Action |
|----------|----------|--------|
| Overall: MINIMAL, all dims eMEDIUM | **PASS - Publication Ready** | Proceed to technical review |
| Overall: LIGHT, all dims eMEDIUM | **PASS - Publication Ready** | Proceed to technical review |
| Overall: MODERATE, no VERY LOW | **CONDITIONAL PASS** | Document known issues, proceed with caution |
| Overall: MODERATE, any VERY LOW | **FAIL - Additional Work Needed** | Apply targeted humanization to VERY LOW dimensions |
| Overall: SUBSTANTIAL or EXTENSIVE | **FAIL - Major Revisions Needed** | Re-apply full humanization workflow |
| Technical accuracy compromised | **FAIL - Fix Immediately** | Revert and re-humanize carefully |
| Em-dashes >3 per page | **FAIL - Critical AI Signal** | Apply Pass 5.1 (em-dash reduction) |

### 9. Document QA Results

**Create quality assurance report**:

```
HUMANIZATION QA REPORT
======================

File: [filename]
Date: [date]
Humanized by: [editor name]

QUANTITATIVE SCORES:
--------------------
Perplexity:    [SCORE] ([detail])
Burstiness:    [SCORE] ([detail])
Structure:     [SCORE] ([detail])
Voice:         [SCORE] ([detail])
Technical:     [SCORE] ([detail])
Formatting:    [SCORE] ([detail])

Overall: [ASSESSMENT]

CRITICAL AI SIGNALS:
--------------------
Em-dashes/page:      [number] [PASS/FAIL]
Heading depth:       [number] [PASS/FAIL]
AI vocab/1k:         [number] [PASS/FAIL]
Sentence StdDev:     [number] [PASS/FAIL]

QUALITATIVE CHECKS:
-------------------
Read-aloud test:          [PASS/FAIL]
Technical accuracy:       [PASS/FAIL]
Publisher compliance:     [PASS/FAIL]

BEFORE/AFTER (if available):
----------------------------
AI vocabulary:     [before] í [after] ([X%] reduction)
Em-dashes/page:    [before] í [after]
Sentence StdDev:   [before] í [after]
Overall:           [before] í [after]

PUBLICATION READINESS:
----------------------
Decision: [PASS / CONDITIONAL PASS / FAIL]

Issues (if any):
- [ ] Issue 1
- [ ] Issue 2

Next Steps:
[Action items if FAIL or CONDITIONAL PASS]
```

### 10. Take Action Based on Results

**If PASS**:
- Move content to technical review queue
- Archive QA report with manuscript
- Update manuscript status

**If CONDITIONAL PASS**:
- Document known issues and risk acceptance
- Notify reviewers of specific concerns
- May require additional editing during review phase

**If FAIL**:
- Create targeted work plan for failed dimensions
- Re-apply specific humanization passes:
  - VERY LOW Perplexity í Pass 2 (vocabulary humanization)
  - VERY LOW Burstiness í Pass 3 (sentence variation)
  - VERY LOW Structure í Pass 3.3 (transitions) + Pass 6 (headings)
  - VERY LOW Voice í Pass 4 (voice refinement)
  - VERY LOW Formatting í Pass 5 (formatting humanization)
- Re-run QA check after additional editing

## Output Deliverable

**Primary**:
- Humanization QA report documenting all scores and checks
- Clear PASS/FAIL/CONDITIONAL PASS decision
- Specific issues identified (if any)

**Secondary**:
- Before/after comparison metrics
- Targeted work plan for failed dimensions (if FAIL)
- Updated manuscript status documentation

## Success Criteria

 Quantitative analysis completed with all dimensions scored
 Critical AI signals verified (em-dashes, heading depth, AI vocabulary)
 Qualitative read-aloud test passed
 Technical accuracy verified (100% preserved)
 Publication readiness decision made (PASS/CONDITIONAL/FAIL)
 Results documented in QA report
 Next steps clear (proceed or additional editing)

## Common Pitfalls to Avoid

L Skipping quantitative analysis (relying only on "feels right")
L Accepting SUBSTANTIAL/EXTENSIVE scores for publication
L Ignoring em-dash density (strongest AI detection signal)
L Not verifying technical accuracy after humanization
L Treating CONDITIONAL PASS as full PASS without documenting risks
L Not comparing before/after metrics to validate improvement
L Proceeding to publication with any VERY LOW dimension scores

## Integration with Humanization Workflow

**Standard workflow**:
1. `analyze-ai-patterns.md` (establish baseline)
2. `humanize-post-generation.md` (apply systematic editing)
3. `humanization-qa-check.md` ê **YOU ARE HERE** (validate results)
4. If PASS í `copy-edit-chapter.md` (final editorial polish)
5. If FAIL í Return to step 2, apply targeted edits

**Iterative refinement** (if needed):
1. Run QA check
2. Identify specific failed dimensions
3. Apply targeted humanization passes for those dimensions
4. Re-run QA check
5. Repeat until PASS or CONDITIONAL PASS achieved

## Publication Readiness Guidelines

**For technical books (PacktPub, O'Reilly, Manning, etc.)**:
- Target: MINIMAL or LIGHT overall assessment
- All dimensions: MEDIUM or higher
- Em-dashes: d2 per page (strict)
- Heading depth: d3 levels
- Technical accuracy: 100% preserved

**For blog posts or articles**:
- Target: LIGHT or MODERATE acceptable
- Perplexity and Burstiness: MEDIUM minimum
- Voice: MEDIUM or higher (more important for blog content)
- Technical accuracy: 100% preserved

**For internal documentation**:
- Target: MODERATE acceptable
- Focus on technical accuracy over style
- Structure and clarity prioritized
- Voice less critical

## Quick QA Checklist

**5-Minute Fast Check** (if time-constrained):
- [ ] Run analysis tool, check overall assessment
- [ ] Overall: MINIMAL or LIGHT? í PASS
- [ ] Overall: MODERATE with no VERY LOW? í CONDITIONAL PASS
- [ ] Overall: SUBSTANTIAL/EXTENSIVE or any VERY LOW? í FAIL
- [ ] Read 2 paragraphs aloud í Sounds natural?
- [ ] Check em-dashes í d2 per page?
- [ ] If all yes í PASS, proceed
- [ ] If any no í FAIL, apply targeted edits

## Notes

- This QA check should be quick (20-30 minutes) if humanization was thorough
- The goal is validation, not additional editing (editing happens before QA)
- Quantitative + qualitative checks catch different issues (use both)
- Technical accuracy is non-negotiable (never sacrifice for style)
- Publisher compliance varies (check specific guidelines)
- "Good enough" threshold depends on publication venue and audience
- Re-running QA after failed check should show measurable improvement

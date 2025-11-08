# Epic 2: Security Review Quality Assurance System

## Epic Goal

Create a systematic peer review capability using a specialized Security Reviewer agent that evaluates analyst enrichments across 8 quality dimensions, detects cognitive biases, verifies factual claims, and provides constructive, blameless feedback to ensure consistently high-quality vulnerability assessments.

## Background

BMAD-1898 Engineering expansion pack provides AI-assisted security vulnerability enrichment for organizations managing 50,000+ annual CVE disclosures. While the Security Analyst agent (Epic 1) dramatically improves enrichment speed (90% faster), quality assurance is critical to ensure:

1. **Systematic Quality Evaluation** - 8-dimensional checklist-based review (Technical Accuracy, Completeness, Actionability, Contextualization, Documentation Quality, ATT&CK Mapping, Cognitive Bias, Source Citation)
2. **Cognitive Bias Detection** - Identify 5 systematic analysis errors (Confirmation, Anchoring, Availability, Overconfidence, Recency bias)
3. **Fact Verification** - Validate critical claims against authoritative sources (NVD, CISA KEV, FIRST EPSS, vendor advisories) using Perplexity MCP
4. **Constructive Feedback** - Blameless review principles that foster learning and continuous improvement

These capabilities enable:

- 60-70% more defects detected through systematic review vs. ad-hoc checks
- Reduced cognitive bias through structured detection and debiasing techniques
- Fact-checking accuracy via automated verification against authoritative sources
- Improved analyst growth through educational, non-punitive feedback
- Consistent quality standards across security operations team

## Integration Context

**Security Reviewer Agent** (Story 2.1) performs systematic peer review using:

- 8 quality dimension checklists (Story 2.2)
- Gap identification and categorization framework (Story 2.3)
- Cognitive bias detection patterns (Story 2.4)
- Perplexity-based fact verification (Story 2.5)
- Structured review report template (Story 2.6)

**Security Analyst Agent** (Epic 1) produces enrichments that are reviewed by:

- Security Reviewer agent using systematic quality evaluation
- Fact verification of CVSS, EPSS, KEV, and patch claims
- Cognitive bias detection to identify systematic errors
- Constructive feedback for continuous improvement

**Knowledge Base Integration** (Epic 4) provides:

- Vulnerability management frameworks (Story 4.1) for technical accuracy validation
- Cognitive bias patterns guide (Story 4.2) for bias detection
- MITRE ATT&CK mapping guide (Story 4.3) for ATT&CK validation

**Project Configuration** (config.yaml) defines:

- JIRA integration for enrichment retrieval and review posting
- Perplexity MCP configuration for fact verification
- Review workflow triggering (priority-based, manual, scheduled)

## Stories

### Story 2.1: Security Reviewer Agent Creation

**As a** security team lead,
**I want** a specialized QA reviewer agent,
**so that** I can ensure consistent, thorough review of analyst work.

**Acceptance Criteria:**

1. Security Reviewer agent definition complete
2. Agent can be activated and displays commands
3. Agent persona is constructive, not punitive
4. Blameless review principles embedded

**Integration Requirements:**

- Agent references 8 quality dimension checklists (Story 2.2)
- Agent uses Perplexity MCP for fact verification (Story 2.5)
- Agent generates review reports using template (Story 2.6)
- Agent detects cognitive biases using patterns guide (Epic 4, Story 4.2)

**Status:** Ready for Review (Completed 2025-11-07)

---

### Story 2.2: Systematic Quality Evaluation

**As a** Security Reviewer agent,
**I want** to evaluate enrichments using 8 quality dimension checklists,
**so that** reviews are comprehensive and consistent.

**Acceptance Criteria:**

1. Agent runs all 8 checklists: Technical Accuracy (10 items), Completeness (12 items), Actionability (8 items), Contextualization (10 items), Documentation Quality (8 items), MITRE ATT&CK Validation (4 items), Cognitive Bias Check (5 biases), Source Citation (accuracy)
2. Agent scores each dimension (percentage)
3. Agent calculates overall quality score

**Technical Requirements:**

- Use BMAD Core `tasks/execute-checklist.md` for checklist execution
- Implement weighted scoring algorithm (Technical Accuracy: 25%, Completeness: 20%, Actionability: 15%, Contextualization: 15%, Documentation: 10%, ATT&CK: 5%, Bias: 5%, Citation: 5%)
- Quality classifications: Excellent (90-100%), Good (75-89%), Needs Improvement (60-74%), Inadequate (<60%)

**Integration Requirements:**

- Checklists must align with vulnerability management frameworks (Epic 4, Story 4.1)
- Cognitive bias checklist uses patterns from Story 4.2
- ATT&CK validation checklist references Story 4.3
- Scores feed into review report template (Story 2.6)

---

### Story 2.3: Gap Identification & Categorization

**As a** Security Reviewer agent,
**I want** to categorize findings by severity (Critical/Significant/Minor),
**so that** analysts know what to prioritize.

**Acceptance Criteria:**

1. Agent categorizes gaps as Critical/Significant/Minor
2. Critical gaps block ticket progression
3. Each gap includes impact explanation
4. Gaps reference specific enrichment sections

**Technical Requirements:**

- **Critical Gaps:** Factual errors, missing priority assessment, incorrect CVSS/KEV/EPSS
- **Significant Gaps:** Missing business context, incomplete remediation guidance, ATT&CK mapping errors
- **Minor Improvements:** Formatting issues, spelling errors, optional enhancements

**Integration Requirements:**

- Gap categories feed into review report (Story 2.6)
- Critical gaps trigger re-review workflow (Epic 3)
- Gap identification uses quality dimension checklists (Story 2.2)

---

### Story 2.4: Cognitive Bias Detection

**As a** Security Reviewer agent,
**I want** to detect cognitive biases in enrichments,
**so that** analysis is objective and evidence-based.

**Acceptance Criteria:**

1. Agent detects 5 bias types: Confirmation, Anchoring, Availability, Overconfidence, Recency
2. Agent provides examples of detected bias
3. Agent suggests debiasing strategies
4. Bias findings maintain blameless tone

**Technical Requirements:**

- Use cognitive-bias-patterns.md guide (Epic 4, Story 4.2) for detection patterns
- Provide specific examples from enrichment showing bias
- Link to debiasing techniques and learning resources
- Frame findings as learning opportunities, not personal criticism

**Integration Requirements:**

- Bias detection patterns from Story 4.2
- Bias findings included in review report (Story 2.6)
- Debiasing recommendations reference best practices

---

### Story 2.5: Fact Verification

**As a** Security Reviewer agent,
**I want** to verify factual claims using Perplexity,
**so that** critical assertions are validated against authoritative sources.

**Acceptance Criteria:**

1. Agent can optionally verify claims
2. Agent checks: CVSS scores, EPSS scores, KEV status, patch availability
3. Agent compares analyst claims with authoritative sources
4. Agent documents discrepancies
5. Agent provides corrections with sources

**Technical Requirements:**

- Use Perplexity MCP (`mcp__perplexity__search`) for factual verification
- Query authoritative sources: NVD (CVSS), FIRST EPSS (exploitation probability), CISA KEV (exploitation status), vendor advisories (patch versions)
- Calculate accuracy score: (Matching Claims / Total Claims Verified) × 100%
- Accuracy thresholds: 95-100% (Excellent), 85-94% (Good), 75-84% (Fair), <75% (Poor)

**Integration Requirements:**

- Perplexity MCP server must be configured and available
- Fact verification results included in review report (Story 2.6)
- Discrepancies categorized using Story 2.3 framework
- Source priority: NVD > CISA > Vendor Advisory > Other

---

### Story 2.6: Constructive Feedback Documentation

**As a** Security Reviewer agent,
**I want** to structure review findings using review template,
**so that** feedback is clear, actionable, and blameless.

**Acceptance Criteria:**

1. Agent uses security-review-report-tmpl.yaml
2. Acknowledges strengths first
3. Identifies gaps with impact explanation
4. Provides specific recommendations
5. Links to learning resources
6. Maintains respectful, constructive tone

**Technical Requirements:**

- Use BMAD Core `tasks/create-doc.md` for template-based report generation
- Report sections: Review Metadata, Executive Summary, Strengths, Quality Scores, Critical Issues, Significant Gaps, Minor Improvements, Cognitive Bias Assessment, Fact Verification Results, Recommendations, Learning Resources, Next Steps
- Language guidelines: Use "we" and "the analysis" (not "you"), frame as growth opportunities, avoid blame/criticism

**Integration Requirements:**

- Template uses quality scores from Story 2.2
- Template includes gap categories from Story 2.3
- Template presents bias findings from Story 2.4
- Template shows fact verification from Story 2.5
- Template links to knowledge base resources (Epic 4)

## Success Criteria

1. **Review Completeness:** 100% of enrichments evaluated across all 8 quality dimensions
2. **Defect Detection:** 60-70% more quality issues identified vs. ad-hoc review
3. **Fact-Checking Accuracy:** 95%+ accuracy in identifying factual discrepancies
4. **Bias Detection:** 4+ cognitive bias types consistently detected when present
5. **Feedback Quality:** 90%+ of analysts rate feedback as constructive and helpful
6. **Review Efficiency:** Complete review in <10 minutes (vs. 30-45 minutes manual)

## Technical Implementation

### File Locations

**Agent:**

- `expansion-packs/bmad-1898-engineering/agents/security-reviewer.md` (Story 2.1)

**Tasks:**

- `expansion-packs/bmad-1898-engineering/tasks/review-security-enrichment.md` (Story 2.2)
- `expansion-packs/bmad-1898-engineering/tasks/categorize-review-findings.md` (Story 2.3)
- `expansion-packs/bmad-1898-engineering/tasks/detect-cognitive-bias.md` (Story 2.4)
- `expansion-packs/bmad-1898-engineering/tasks/fact-verify-claims.md` (Story 2.5)

**Templates:**

- `expansion-packs/bmad-1898-engineering/templates/security-review-report-tmpl.yaml` (Story 2.6)
- `expansion-packs/bmad-1898-engineering/templates/fact-verification-report-tmpl.yaml` (Story 2.5)

**Checklists (8 Quality Dimensions, Story 2.2):**

- `expansion-packs/bmad-1898-engineering/checklists/technical-accuracy-checklist.md` (10 items)
- `expansion-packs/bmad-1898-engineering/checklists/completeness-checklist.md` (12 items)
- `expansion-packs/bmad-1898-engineering/checklists/actionability-checklist.md` (8 items)
- `expansion-packs/bmad-1898-engineering/checklists/contextualization-checklist.md` (10 items)
- `expansion-packs/bmad-1898-engineering/checklists/documentation-quality-checklist.md` (8 items)
- `expansion-packs/bmad-1898-engineering/checklists/attack-mapping-validation-checklist.md` (4 items)
- `expansion-packs/bmad-1898-engineering/checklists/cognitive-bias-checklist.md` (5 biases)
- `expansion-packs/bmad-1898-engineering/checklists/source-citation-checklist.md` (accuracy check)

**Testing Standards:**

- Test with enrichments of varying quality (excellent, good, poor)
- Verify all 8 checklists execute correctly
- Validate scoring algorithm accuracy
- Test fact verification with known correct/incorrect claims
- Verify bias detection with biased/unbiased enrichments
- Review tone and language for constructiveness and blameless principles
- Test report generation with all finding types

### MCP Dependencies

**Perplexity MCP Server** (Required for Story 2.5):

- Tool: `mcp__perplexity__search`
- Purpose: Fact verification against authoritative sources
- Configuration: Must be enabled in Claude Code MCP settings
- Error Handling: If unavailable, skip fact verification and note in report

## Change Log

| Date       | Version | Description                                      | Author     |
| ---------- | ------- | ------------------------------------------------ | ---------- |
| 2025-11-08 | 1.0     | Initial Epic 2 creation based on Stories 2.1-2.6 | Sarah (PO) |

## References

- Story 1.1: Security Analyst Agent Creation (produces enrichments to review)
- Story 1.7: Multi-Factor Priority Assessment (priority framework to validate)
- Epic 3: Workflow Integration (review workflow triggering)
- Story 4.1: Vulnerability Management Knowledge Base (technical accuracy reference)
- Story 4.2: Cognitive Bias Patterns Guide (bias detection patterns)
- Story 4.3: MITRE ATT&CK Mapping Guide (ATT&CK validation reference)
- config.yaml: JIRA Integration and MCP Configuration

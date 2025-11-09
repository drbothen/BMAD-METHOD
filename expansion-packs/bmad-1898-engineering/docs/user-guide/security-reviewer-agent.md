# Security Reviewer Agent Usage Guide

## Overview

The Security Reviewer agent (Riley 🔍) is an AI-powered quality assurance assistant specializing in systematic peer review of vulnerability enrichments. This guide provides comprehensive documentation for conducting blameless, constructive reviews using the 8-dimension quality framework.

**Agent Profile:**

- **Name:** Riley
- **ID:** security-reviewer
- **Title:** Security Review Specialist
- **Icon:** 🔍
- **When to Use:** Reviewing analyst enrichments, quality assurance, bias detection, constructive feedback

**Agent Persona:**

- **Role:** Senior security analyst performing peer review
- **Style:** Constructive, educational, thorough, respectful
- **Identity:** Quality mentor fostering continuous improvement
- **Focus:** Blameless review with growth-oriented feedback

**Core Principles:**

- **Blameless Culture:** No blame or criticism, only improvement opportunities
- **Constructive Feedback:** Strengths before gaps, balanced approach
- **Educational Approach:** Link gaps to learning resources
- **Systematic Review:** 8-dimension quality checklists
- **Bias Awareness:** Detect cognitive biases without judgment
- **Actionable Recommendations:** Specific, prioritized next steps

---

## Agent Activation

To activate the Security Reviewer agent in your IDE:

```bash
/bmad-1898:agents:security-reviewer
```

Upon activation, the agent will:

1. Greet you as Riley, Security Review Specialist
2. Automatically run the `*help` command to display available commands
3. Wait for your instructions

**Example activation:**

```
User: /bmad-1898:agents:security-reviewer

Agent: Hello! I'm Riley 🔍, your Security Review Specialist.

I specialize in systematic peer review of vulnerability enrichments using
an 8-dimension quality framework with blameless, constructive feedback.

Available Commands:
1. *help - Display available commands
2. *review-enrichment {ticket-id} - Complete 7-stage review workflow
3. *fact-check {ticket-id} - Verify factual claims using Perplexity
4. *detect-bias {ticket-id} - Run cognitive bias detection
5. *generate-report {ticket-id} - Create review report from findings
6. *exit - Exit Security Reviewer agent mode

What would you like me to review today?
```

---

## Quick Start Guide

**For experienced reviewers who want to get started immediately:**

### Prerequisites Checklist

Before your first review, ensure:

- [ ] Atlassian MCP connected (JIRA access for reading tickets and posting reviews)
- [ ] Perplexity MCP connected (AI-assisted fact verification)
- [ ] Security Analyst agent documentation reviewed (understand enrichment process)
- [ ] Blameless review principles understood (see Best Practices section)

### Common Usage Patterns

**Pattern 1: Full Review (Most Common)**

```bash
# Activate agent
/bmad-1898:agents:security-reviewer

# Run complete 7-stage review workflow
*review-enrichment AOD-1234
```

**Duration:** 15-20 minutes | **Output:** JIRA comment + local review file + quality scores

---

**Pattern 2: Fact-Check Only**

```bash
# Verify factual accuracy without full review
*fact-check AOD-1234
```

**Use When:** Quick verification of CVSS, EPSS, KEV, ATT&CK mappings | **Duration:** 5 minutes

---

**Pattern 3: Bias Detection Only**

```bash
# Detect cognitive biases in enrichment
*detect-bias AOD-1234
```

**Use When:** Educational review, training new analysts, research quality | **Duration:** 5 minutes

---

**Pattern 4: Stage-by-Stage Review (Advanced)**

```bash
# Step through review stages manually for learning/training
*review-enrichment AOD-1234

# When prompted, review each dimension individually
# Generate final report after all stages complete
*generate-report AOD-1234
```

**Use When:** Training new reviewers, teaching 8-dimension framework | **Duration:** 25-30 minutes

---

## Review Philosophy

### Blameless Culture

The Security Reviewer agent embodies a **blameless review culture** where the focus is on work quality improvement, not analyst performance evaluation. This approach:

- **Normalizes mistakes** as learning opportunities, not failures
- **Assumes good intent** - analysts did their best with available information
- **Focuses systemically** - recurring mistakes indicate process issues, not individual fault
- **Avoids blame language** - "this section could be improved" vs. "you made an error"
- **Emphasizes growth** - every gap includes learning resources and next steps

### Constructive Feedback Techniques

All reviews follow these principles:

1. **Strengths First:** Always begin with "What Went Well" section acknowledging positive work
2. **Balance:** Aim for 2:1 ratio of positive to improvement feedback (for Good/Excellent enrichments)
3. **Specific Praise:** "Excellent remediation guidance with clear step-by-step patch instructions" vs. "Good job"
4. **Growth Framing:** "To further improve..." vs. "You failed to..."
5. **Actionable Recommendations:** Every gap has specific next step with estimated effort

### Educational Approach

Every review is a learning opportunity:

- **Learning Resources:** All gaps link to relevant documentation, checklists, or training materials
- **Conversation Starters:** Each review includes questions to foster collaborative discussion
- **Explain "Why":** Recommendations explain rationale, not just what to fix
- **Mentor Tone:** Helping colleague grow, not judging performance

---

## Commands Reference

### \*help

**Purpose:** Display all available commands with brief descriptions

**Usage:**

```bash
*help
```

**Output:** Numbered list of commands allowing selection by number or direct command execution

---

### \*review-enrichment {ticket-id}

**Purpose:** Execute complete 7-stage systematic review workflow

**Usage:**

```bash
*review-enrichment AOD-1234
```

**7-Stage Workflow:**

**Stage 1: Fetch Enrichment**

- Retrieve ticket from JIRA via Atlassian MCP
- Load enrichment content from custom fields
- Parse all 12 enrichment sections

**Stage 2: Technical Accuracy Review**

- Verify CVSS score against NVD
- Check CVSS vector string validity
- Verify EPSS score (within 7 days)
- Check KEV status against CISA catalog
- Validate affected/patched versions
- Confirm exploit status
- Verify ATT&CK T-numbers

**Stage 3: Completeness & Actionability Check**

- Verify all 12 template sections populated
- Assess remediation guidance clarity
- Check verification steps present
- Validate compensating controls (if applicable)

**Stage 4: Contextualization & Documentation Review**

- Assess Asset Criticality Rating (ACR)
- Evaluate System Exposure classification
- Review business impact articulation
- Check documentation quality (formatting, clarity, organization)

**Stage 5: Attack Mapping & Source Validation**

- Validate MITRE ATT&CK tactics and techniques
- Check ATT&CK T-number validity
- Verify source citations present and authoritative
- Confirm URLs included for all claims

**Stage 6: Cognitive Bias Detection**

- Scan for 5 bias types:
  1. Confirmation bias
  2. Anchoring bias
  3. Availability heuristic
  4. Overconfidence bias
  5. Recency bias
- Provide debiasing recommendations

**Stage 7: Report Generation**

- Calculate weighted quality score (8 dimensions)
- Classify enrichment: Excellent (90-100), Good (75-89), Needs Improvement (60-74), Inadequate (<60)
- Generate review report with blameless language
- Post to JIRA as comment
- Save local review file

**Duration:** 15-20 minutes
**Output:** JIRA comment + local file + quality scores

---

### \*fact-check {ticket-id}

**Purpose:** Verify factual claims in enrichment using AI-assisted research

**Usage:**

```bash
*fact-check AOD-1234
```

**Verification Scope:**

- **CVSS Score:** Compare against NVD official score
- **EPSS Score:** Verify against FIRST EPSS database (current within 7 days)
- **KEV Status:** Check CISA Known Exploited Vulnerabilities catalog
- **Affected Versions:** Validate against vendor security advisories
- **Patched Versions:** Confirm patch version accuracy
- **Exploit Status:** Verify exploitation claims against threat intelligence
- **ATT&CK Techniques:** Validate T-numbers against MITRE ATT&CK matrix

**Process:**

1. Uses Perplexity MCP for authoritative source lookup
2. Compares enrichment claims to official sources
3. Documents discrepancies with source URLs
4. Provides correction recommendations

**Duration:** 5 minutes
**Output:** Fact-check report with discrepancies and correction recommendations

---

### \*detect-bias {ticket-id}

**Purpose:** Detect cognitive biases in enrichment analysis

**Usage:**

```bash
*detect-bias AOD-1234
```

**5 Bias Types Detected:**

**1. Confirmation Bias**

- **Pattern:** Seeking only information that confirms initial assessment
- **Example:** High CVSS → only researching exploitation evidence, ignoring non-exploitation indicators
- **Debiasing:** Recommend balanced research (both exploitation and non-exploitation evidence)

**2. Anchoring Bias**

- **Pattern:** Over-relying on first piece of information encountered
- **Example:** Initial CVSS 9.8 → maintaining Critical priority despite low EPSS (0.02%) and no KEV
- **Debiasing:** Recommend multi-factor priority assessment using all metrics

**3. Availability Heuristic**

- **Pattern:** Overweighting recent or memorable incidents
- **Example:** Recent ransomware attack → overstating risk for unrelated RCE vulnerability
- **Debiasing:** Recommend historical context research, not just recent events

**4. Overconfidence Bias**

- **Pattern:** Expressing certainty without sufficient evidence
- **Example:** "Definitely exploited in the wild" without citing threat intelligence source
- **Debiasing:** Recommend hedging language and source citations for claims

**5. Recency Bias**

- **Pattern:** Focusing on most recent threat intelligence, ignoring historical context
- **Example:** No exploitation this month → Low priority, despite 6-month KEV history
- **Debiasing:** Recommend reviewing historical exploitation timeline

**Detection Process:**

1. Analyze enrichment language and claims
2. Check for bias patterns using checklist
3. Document detected biases (non-judgmental tone)
4. Provide debiasing recommendations with learning resources

**Duration:** 5 minutes
**Output:** Bias detection report with debiasing recommendations

---

### \*generate-report {ticket-id}

**Purpose:** Create formal review report from accumulated findings

**Usage:**

```bash
*generate-report AOD-1234
```

**Use Cases:**

- After manual stage-by-stage review (advanced workflow)
- To regenerate report with updated scores
- To create standalone report from fact-check/bias-detection results

**Report Structure:** (See "Review Output Structure" section below for complete format)

**Duration:** 2 minutes
**Output:** JIRA comment + local review file (.md format)

---

### \*exit

**Purpose:** Exit Security Reviewer agent mode and return to normal IDE behavior

**Usage:**

```bash
*exit
```

**Effect:**

- Agent persona deactivated
- Returns farewell message
- IDE returns to default state

---

## 8 Quality Dimensions Framework

The Security Reviewer agent evaluates enrichments using 8 dimensions with weighted scoring:

### Dimension 1: Technical Accuracy (25% weight)

**Purpose:** Verify factual correctness of vulnerability data

**Checklist:**

- [ ] CVSS score matches NVD or vendor advisory
- [ ] CVSS vector string is valid and accurate
- [ ] EPSS score current (within 7 days)
- [ ] KEV status correct per CISA catalog
- [ ] Affected versions accurate per vendor advisory
- [ ] Patched versions correct and specific
- [ ] Exploit status matches threat intelligence
- [ ] ATT&CK T-numbers valid

**Scoring:** (Pass/Fail per item) → Percentage
**Critical Issues:** Incorrect CVSS, wrong patch version, KEV status error

**Example:**

- **95% (Excellent):** All 8 items pass, one minor discrepancy (EPSS 6 days old vs. 5 days)
- **75% (Good):** 6/8 pass, missing KEV check, EPSS outdated
- **50% (Inadequate):** CVSS incorrect, patch version wrong, KEV status error

---

### Dimension 2: Completeness (20% weight)

**Purpose:** Ensure all required enrichment sections present and populated

**Checklist:**

- [ ] All 12 template sections populated
- [ ] Executive summary present and concise (2-3 sentences)
- [ ] Vulnerability details complete (CVSS, EPSS, KEV, affected versions)
- [ ] Remediation guidance provided (patch/workaround)
- [ ] Business impact assessment included (ACR, exposure, affected processes)
- [ ] Threat intelligence researched (exploit status, attacker activity)
- [ ] Sources cited for all claims

**Scoring:** (Sections populated / 12 total sections) → Percentage
**Critical Issues:** Missing remediation guidance, missing priority assessment

**Example:**

- **100% (Excellent):** All 12 sections complete with substantive content
- **85% (Good):** 11/12 sections complete, threat intelligence minimal
- **58% (Inadequate):** 7/12 sections populated, remediation and business impact missing

---

### Dimension 3: Actionability (15% weight)

**Purpose:** Ensure remediation guidance is clear, specific, and implementable

**Checklist:**

- [ ] Remediation steps are clear and specific (not vague)
- [ ] Patch version or workaround provided
- [ ] Verification steps included (how to confirm remediation successful)
- [ ] Compensating controls listed (if patch not immediately available)
- [ ] Guidance appropriate for target audience (DevOps/SysAdmin)
- [ ] Estimated remediation effort noted (time/complexity)

**Scoring:** (Actionable guidance elements present / 6 total) → Percentage
**Significant Issues:** Vague guidance ("update software"), no verification steps

**Example:**

- **100% (Excellent):** "Update to PostgreSQL 15.3.2 via `apt-get update postgresql`, verify with `SELECT version();` → expected output: 15.3.2+"
- **67% (Needs Improvement):** "Patch available, update to latest version" (no specific version, no verification)
- **33% (Inadequate):** "Update software" (completely vague)

---

### Dimension 4: Contextualization (15% weight)

**Purpose:** Ensure business context informs risk assessment and priority

**Checklist:**

- [ ] Asset Criticality Rating (ACR) assessed (1-5 scale)
- [ ] System Exposure classified (Internet-Facing, Internal, Isolated)
- [ ] Business processes affected identified (e.g., "Customer portal login")
- [ ] Business impact clearly articulated (revenue, compliance, reputation)
- [ ] Priority rationale references business context (not just CVSS)
- [ ] Stakeholders identified (who to notify, who to coordinate with)

**Scoring:** (Context elements present / 6 total) → Percentage
**Significant Issues:** Missing ACR, missing business impact, vague process description

**Example:**

- **100% (Excellent):** ACR=5 (Critical), Internet-Facing, "Customer authentication portal (10,000 daily logins), payment processing affected, PCI-DSS compliance risk, notify DevOps Lead and CISO"
- **67% (Needs Improvement):** ACR=4, "Affects web services" (vague), no stakeholders
- **33% (Inadequate):** No ACR, "System is important" (no specifics)

---

### Dimension 5: Documentation Quality (10% weight)

**Purpose:** Ensure enrichment is well-formatted, clear, and professionally written

**Checklist:**

- [ ] Markdown formatting correct (headings, lists, code blocks)
- [ ] Spelling and grammar professional (no typos)
- [ ] Section headings consistent with template
- [ ] Lists and tables formatted properly
- [ ] Clarity - no ambiguous language or jargon without explanation
- [ ] Organization logical (information flows clearly)

**Scoring:** (Quality elements present / 6 total) → Percentage
**Minor Issues:** Formatting inconsistencies, typos (not critical to accuracy)

**Example:**

- **100% (Excellent):** Perfect formatting, clear language, zero typos
- **83% (Good):** Minor formatting inconsistency in list indentation, one typo
- **50% (Inadequate):** Multiple typos, broken markdown formatting, unclear language

---

### Dimension 6: Attack Mapping Validation (5% weight)

**Purpose:** Verify MITRE ATT&CK mapping accuracy and relevance

**Checklist:**

- [ ] Tactics are valid ATT&CK tactics (e.g., Initial Access, Privilege Escalation)
- [ ] Techniques have valid T-numbers (e.g., T1078, T1190)
- [ ] Mapping appropriate for vulnerability type (RCE → T1190 Exploit Public-Facing Application)
- [ ] Detection implications included (what to monitor for)
- [ ] Defense recommendations aligned with mapping (mitigations for specific techniques)

**Scoring:** (Mapping elements correct / 5 total) → Percentage
**Significant Issues:** Invalid T-numbers, incorrect tactic mapping

**Example:**

- **100% (Excellent):** Valid tactics/techniques, appropriate mapping, detection and defense guidance included
- **60% (Needs Improvement):** Valid T-numbers, but mapping not appropriate for vuln type (SQL Injection → T1190 instead of T1190 + T1059.004)
- **20% (Inadequate):** Invalid T-number (T-9999), incorrect tactic

---

### Dimension 7: Cognitive Bias (5% weight)

**Purpose:** Detect cognitive biases in analysis to improve objectivity

**5 Bias Types:**

**1. Confirmation Bias**

- **Pattern:** Seeking only information that confirms initial assessment
- **Detection:** Unbalanced research (only exploitation evidence for high CVSS, only non-exploitation for low CVSS)

**2. Anchoring Bias**

- **Pattern:** Over-relying on first piece of information (initial CVSS)
- **Detection:** Priority matches CVSS exactly without considering EPSS/KEV/ACR

**3. Availability Heuristic**

- **Pattern:** Overweighting recent/memorable incidents
- **Detection:** Recent ransomware → overstating risk for unrelated vulnerability type

**4. Overconfidence Bias**

- **Pattern:** Expressing certainty without sufficient evidence
- **Detection:** "Definitely exploited" without citing threat intelligence source

**5. Recency Bias**

- **Pattern:** Focusing on most recent threat intelligence, ignoring historical context
- **Detection:** No recent exploitation → Low priority, despite historical KEV status

**Scoring:** Bias-free analysis → 100%, each bias detected → -20% penalty
**Debiasing Recommendations:** Suggest alternative perspectives, additional research, balanced analysis

**Example:**

- **100% (Excellent):** No biases detected, balanced analysis with multiple perspectives
- **80% (Good):** Minor confirmation bias (could include non-exploitation evidence)
- **60% (Needs Improvement):** Confirmation + anchoring bias detected

---

### Dimension 8: Source Citation (5% weight)

**Purpose:** Ensure all factual claims supported by authoritative sources

**Checklist:**

- [ ] All factual claims have sources cited
- [ ] Sources are authoritative (NIST NVD, CISA, vendor advisories, FIRST EPSS)
- [ ] URLs included for all sources
- [ ] Sources are current (within reasonable timeframe for static data)
- [ ] No reliance on non-authoritative sources (forums, blogs) without corroboration

**Scoring:** (Citation elements present / 5 total) → Percentage
**Significant Issues:** Missing sources for CVSS/EPSS/KEV, relying on unverified sources

**Example:**

- **100% (Excellent):** All claims sourced from NVD, CISA, vendor advisories with URLs
- **60% (Needs Improvement):** CVSS sourced, EPSS cited without URL, KEV unchecked
- **20% (Inadequate):** Only blog post cited, no authoritative sources

---

### Overall Quality Score Calculation

**Formula:**

```
Quality Score = (
  Technical_Accuracy × 0.25 +
  Completeness × 0.20 +
  Actionability × 0.15 +
  Contextualization × 0.15 +
  Documentation_Quality × 0.10 +
  Attack_Mapping × 0.05 +
  Cognitive_Bias × 0.05 +
  Source_Citation × 0.05
)
```

**Classification:**

- **90-100:** Excellent - Exemplary work, minor/no revisions needed
- **75-89:** Good - Solid quality, some improvements recommended
- **60-74:** Needs Improvement - Significant gaps, revisions required before remediation
- **< 60:** Inadequate - Critical issues, substantial rework needed

**Example Calculation:**

```
Technical_Accuracy:    95% × 0.25 = 23.75
Completeness:         100% × 0.20 = 20.00
Actionability:         85% × 0.15 = 12.75
Contextualization:     80% × 0.15 = 12.00
Documentation_Quality: 90% × 0.10 =  9.00
Attack_Mapping:       100% × 0.05 =  5.00
Cognitive_Bias:        90% × 0.05 =  4.50
Source_Citation:       95% × 0.05 =  4.75
----------------------------------------
TOTAL:                                91.75 (Excellent)
```

---

## Blameless Review Best Practices

### Principle 1: Blameless Culture

**Core Concept:** Reviews focus on **work quality**, not analyst performance.

**Practices:**

- **No Blame Language:** Avoid "you made an error" → Use "this section could be improved"
- **Assume Good Intent:** Analysts did their best with available information
- **Normalize Mistakes:** Errors are learning opportunities, not failures
- **Systemic Focus:** Recurring mistakes indicate process issues, not individual fault
- **Growth Mindset:** Every gap is a chance to learn and improve

**Example:**

- ❌ **Blame Language:** "You failed to check KEV status - this is a critical oversight"
- ✅ **Blameless Language:** "KEV status verification is missing - recommend checking CISA catalog at [URL]"

---

### Principle 2: Constructive Feedback

**Core Concept:** Balance positive recognition with improvement opportunities.

**Practices:**

- **Strengths First:** Always start review with "What Went Well" section before identifying gaps
- **Acknowledge Good Work:** Explicitly recognize solid analysis, research effort, clear writing
- **Balance Ratio:** Aim for 2:1 positive-to-improvement feedback for Good/Excellent enrichments
- **Specific Praise:** "Excellent remediation guidance with clear step-by-step patch instructions and verification commands"
- **Growth Framing:** "To further improve..." vs. "You failed to..."

**Example Review Opening:**

```
**Strengths & What Went Well:**
- Exceptional technical accuracy - all metrics verified against authoritative sources
- Complete 12-section enrichment with detailed analysis
- Remediation guidance is highly actionable with specific commands
- Excellent business impact assessment clearly articulating risk

**Opportunities for Enhancement:**
1. Consider adding verification steps for post-patch validation (2-minute enhancement)
```

---

### Principle 3: Educational Approach

**Core Concept:** Every gap includes learning resources and "why" explanations.

**Practices:**

- **Link Learning Resources:** Every gap recommendation includes relevant documentation, checklists, or guides
- **Explain "Why":** Don't just say "what to fix" - explain why it matters
- **Conversation Starters:** Include questions to foster collaborative learning
- **Mentor Tone:** Helping colleague grow, not judging performance
- **Context Provision:** Help analyst understand impact of gaps

**Example:**

```
**Gap:** EPSS score cited without source URL

**Educational Feedback:**
EPSS scores should include source URL for verification and auditability.
This ensures reviewers and stakeholders can validate the metric independently.

**Recommendation:** Add FIRST EPSS source: https://www.first.org/epss/

**Why It Matters:** Authoritative sources build trust in analysis and enable
independent verification by security leadership.

**Learning Resource:** docs/checklists/source-citation-checklist.md

**Conversation Starter:**
What other metrics do you typically source-cite? Let's discuss citation
standards for different data types.
```

---

### Principle 4: Actionable Recommendations

**Core Concept:** Every gap has specific, prioritized next steps with effort estimates.

**Practices:**

- **Specificity:** "Add CISA KEV check using [URL]" vs. "Check KEV"
- **Prioritization:** Categorize as Critical → Significant → Minor
- **Effort Estimates:** "5-minute fix" vs. "requires re-research (15 minutes)"
- **Clear Next Steps:** Numbered list of actions with expected outcomes
- **Verification Guidance:** How to confirm the gap is resolved

**Example:**

```
**Recommendations (Prioritized):**

**CRITICAL (Must Fix Before Remediation):**
1. Research specific patch version (10 min)
   - Expected: "Update to Jenkins 2.440.2 or later"
   - Source: https://www.jenkins.io/security/advisories/

**HIGH (Should Fix):**
2. Verify KEV status against CISA catalog (3 min)
   - Expected: KEV status updated with date if present
   - Source: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**MEDIUM (Recommended):**
3. Add verification steps for post-patch testing (5 min)
   - Expected: Specific commands to verify patch applied

**Total Estimated Effort:** 18 minutes for Critical + High priority fixes
```

---

### Principle 5: Avoid Blame Language

**Core Concept:** Focus on work gaps, not analyst shortcomings.

**Language Transformation Examples:**

| ❌ Blame Language                      | ✅ Blameless Language                                                                  |
| -------------------------------------- | -------------------------------------------------------------------------------------- |
| "You failed to check KEV status"       | "KEV status verification is missing - recommend checking CISA catalog"                 |
| "This is wrong"                        | "CVSS score differs from NVD - verify using [NVD link]"                                |
| "Poor quality enrichment"              | "Some gaps identified - see recommendations below to address"                          |
| "You made an error in the CVSS vector" | "CVSS vector string differs from NVD - recommend verification"                         |
| "You didn't cite sources"              | "Source citations missing - add authoritative URLs for CVSS, EPSS, KEV"                |
| "This analysis is biased"              | "Minor confirmation bias detected - consider balancing with non-exploitation evidence" |
| "Incomplete work"                      | "Additional sections could be enhanced - see completeness recommendations"             |

**Tone Guidelines:**

- Use **passive voice** to depersonalize: "Missing" vs. "You didn't include"
- Use **recommendations** instead of corrections: "Recommend adding" vs. "You must add"
- Use **opportunities** instead of failures: "Enhancement opportunity" vs. "Failure to..."
- Use **questions** to stimulate thinking: "Have you considered...?" vs. "You should have..."

---

## Review Output Structure

### Complete Review Report Format

Every review generates a structured report with 12 sections:

#### 1. Review Metadata

```markdown
**Review Metadata:**

- **Ticket ID:** AOD-1234
- **CVE:** CVE-2024-5678
- **Analyst:** Jordan
- **Reviewer:** Riley (Security Review Specialist)
- **Review Date:** 2025-01-15
- **Quality Score:** 91.75/100 (Excellent)
```

#### 2. Executive Summary

2-3 sentences with constructive tone, overall assessment

**Example:**

```markdown
**Executive Summary:**
Outstanding enrichment with comprehensive research, accurate technical details,
and highly actionable remediation guidance. Jordan demonstrated excellent use
of authoritative sources and thorough business context assessment. Minor
suggestion for additional verification steps.
```

#### 3. Strengths & What Went Well

Always included, acknowledges positive work before identifying gaps

**Example:**

```markdown
**Strengths & What Went Well:**

- Exceptional technical accuracy - all metrics verified against multiple authoritative sources
- Complete 12-section enrichment with detailed analysis in each section
- Remediation guidance is highly actionable with specific commands and version numbers
- Excellent business impact assessment clearly articulating risk to database operations
- Proper MITRE ATT&CK mapping with relevant detection implications
- All claims properly cited with authoritative sources
```

#### 4. Quality Dimension Scores

Table format with 8 dimensions, individual scores, weights, weighted scores, and assessments

**Example:**

```markdown
**Quality Dimension Scores:**

| Dimension             | Score | Weight | Weighted  | Assessment                                                       |
| --------------------- | ----- | ------ | --------- | ---------------------------------------------------------------- |
| Technical Accuracy    | 95%   | 25%    | 23.75     | Excellent - all metrics verified                                 |
| Completeness          | 100%  | 20%    | 20.00     | Excellent - all sections present                                 |
| Actionability         | 85%   | 15%    | 12.75     | Good - remediation clear, verification could be more detailed    |
| Contextualization     | 80%   | 15%    | 12.00     | Good - business impact present, processes could be more specific |
| Documentation Quality | 90%   | 10%    | 9.00      | Excellent - well-formatted and clear                             |
| Attack Mapping        | 100%  | 5%     | 5.00      | Excellent - accurate T-numbers and mapping                       |
| Cognitive Bias        | 90%   | 5%     | 4.50      | Good - minor confirmation bias detected                          |
| Source Citation       | 95%   | 5%     | 4.75      | Excellent - all claims sourced                                   |
| **TOTAL**             |       |        | **91.75** | **Excellent**                                                    |
```

#### 5. Critical Issues

Only included if critical gaps identified (score impact >10 points or blocks remediation)

**Example:**

```markdown
**Critical Issues:**

1. **Vague Remediation Guidance:** "Update Jenkins" - no specific version provided
   - **Impact:** DevOps cannot act without specific patch version
   - **Recommendation:** Research vendor advisory for specific patched version
   - **Effort:** 10 minutes
```

#### 6. Significant Gaps

Important findings with moderate score impact (5-10 points) or quality concerns

**Example:**

```markdown
**Significant Gaps:**

1. **Business Impact Vague:** "Affects web services" is too general
   - **Recommendation:** Specify which business processes (e.g., "Customer portal login")
   - **Resource:** docs/data/business-impact-assessment-guide.md
   - **Effort:** 5 minutes

2. **Missing Sources:** EPSS score cited without source URL
   - **Recommendation:** Add FIRST EPSS source: https://www.first.org/epss/
   - **Effort:** 2 minutes
```

#### 7. Minor Improvements

Optional enhancements, lower priority (<5 points score impact)

**Example:**

```markdown
**Minor Improvements:**

1. **Verification Steps:** Consider adding specific re-test procedures post-patch
   - **Resource:** docs/data/verification-best-practices.md
   - **Effort:** 2 minutes
```

#### 8. Cognitive Bias Assessment

Detected biases with debiasing recommendations (non-judgmental tone)

**Example:**

```markdown
**Cognitive Bias Assessment:**
Minor confirmation bias detected in Threat Intelligence section (focused on
exploitation evidence, could balance with non-exploitation indicators). This
is very minor and doesn't impact overall quality.

**Debiasing Recommendation:**
Consider researching both exploitation and non-exploitation evidence for
balanced threat assessment.
```

#### 9. Fact Verification Results

Only included if `*fact-check` command was run; documents discrepancies

**Example:**

```markdown
**Fact Verification Results:**

- **CVSS Score:** ✅ Verified 9.8 matches NVD
- **EPSS Score:** ⚠️ Enrichment shows 0.45%, NVD shows 0.42% (updated 2 days ago)
- **KEV Status:** ✅ Verified "Yes" - added to KEV 2024-10-15
- **Patch Version:** ✅ Verified PostgreSQL 15.3.2 is correct patched version
```

#### 10. Recommendations & Learning Resources

Prioritized next steps with links to documentation

**Example:**

```markdown
**Recommendations & Learning Resources:**

**CRITICAL (Must Fix Before Remediation):**

1. Research specific patch version (10 min)
   - Resource: Vendor security advisory

**HIGH (Should Fix):** 2. Enhance business impact section (5 min)

- Resource: docs/data/business-impact-assessment-guide.md

**Learning Resources:**

- Remediation Guidance Best Practices: docs/data/remediation-guidance-best-practices.md
- Source Citation Standards: docs/checklists/source-citation-checklist.md
```

#### 11. Conversation Starters

Educational questions to foster collaborative learning

**Example:**

```markdown
**Conversation Starters:**

- What verification steps do you typically use for database patches?
- How do you balance thoroughness with time constraints on lower-priority vulnerabilities?
- What challenges did you encounter researching this CVE?
```

#### 12. Next Steps

Clear action items for analyst with status decision

**Example:**

```markdown
**Next Steps:**

1. Optional: Enhance verification section (2-minute update)
2. Excellent work - no critical revisions needed
3. **Status:** Approved for remediation
```

### Output Delivery

**JIRA Comment:**

- Full review report posted as JIRA comment on ticket
- Markdown formatted for readability
- Includes quality score in comment header

**Local Review File:**

- Saved to: `expansion-packs/bmad-1898-engineering/reviews/{ticket-id}-review.md`
- Complete report with all 12 sections
- Timestamped for audit trail

---

## Example Reviews

### Example 1: Excellent Enrichment (95/100)

**Scenario:** CVE-2024-5678 PostgreSQL Privilege Escalation
**Analyst:** Jordan
**Reviewer:** Riley

---

**Review Metadata:**

- **Ticket ID:** AOD-5678
- **CVE:** CVE-2024-5678
- **Analyst:** Jordan
- **Reviewer:** Riley (Security Review Specialist)
- **Review Date:** 2025-01-15
- **Quality Score:** 95/100 (Excellent)

---

**Executive Summary:**

Outstanding enrichment with comprehensive research, accurate technical details, and highly actionable remediation guidance. Jordan demonstrated excellent use of authoritative sources and thorough business context assessment. Minor suggestion for additional verification steps.

---

**Strengths & What Went Well:**

- Exceptional technical accuracy - all metrics verified against multiple authoritative sources
- Complete 12-section enrichment with detailed analysis in each section
- Remediation guidance is highly actionable with specific commands and version numbers
- Excellent business impact assessment clearly articulating risk to database operations
- Proper MITRE ATT&CK mapping with relevant detection implications
- All claims properly cited with authoritative sources (NVD, CISA, PostgreSQL Security Advisory)

---

**Quality Dimension Scores:**

| Dimension             | Score | Weight | Weighted  | Assessment                                                             |
| --------------------- | ----- | ------ | --------- | ---------------------------------------------------------------------- |
| Technical Accuracy    | 96%   | 25%    | 24.00     | Excellent - all metrics verified                                       |
| Completeness          | 100%  | 20%    | 20.00     | Excellent - all sections present                                       |
| Actionability         | 85%   | 15%    | 12.75     | Excellent - remediation clear, minor verification enhancement possible |
| Contextualization     | 95%   | 15%    | 14.25     | Excellent - business impact clear, ACR assessed                        |
| Documentation Quality | 100%  | 10%    | 10.00     | Excellent - well-formatted and clear                                   |
| Attack Mapping        | 100%  | 5%     | 5.00      | Excellent - accurate T-numbers and mapping                             |
| Cognitive Bias        | 80%   | 5%     | 4.00      | Good - very minor confirmation bias                                    |
| Source Citation       | 100%  | 5%     | 5.00      | Excellent - all claims sourced                                         |
| **TOTAL**             |       |        | **95.00** | **Excellent**                                                          |

---

**Critical Issues:** None identified

---

**Significant Gaps:** None identified

---

**Minor Improvements:**

1. **Verification Steps:** Consider adding specific re-test procedures post-patch
   - **Recommendation:** Add "Verify with `SELECT version();` shows 15.3.2+ after patch"
   - **Resource:** docs/data/verification-best-practices.md
   - **Effort:** 2 minutes

---

**Cognitive Bias Assessment:**

Very minor confirmation bias detected in Threat Intelligence section (focused on exploitation evidence, could balance with non-exploitation indicators). This is extremely minor and doesn't impact overall quality.

**Debiasing Recommendation:** For future enrichments, consider including both exploitation and non-exploitation evidence for balanced threat assessment.

---

**Recommendations:**

1. **OPTIONAL:** Add specific verification command for post-patch validation (2 min)

---

**Conversation Starters:**

- What verification steps do you typically use for database patches?
- How do you balance thoroughness with time constraints on lower-priority vulnerabilities?

---

**Next Steps:**

1. Optional: Enhance verification section (2-minute update)
2. Excellent work - no critical revisions needed
3. **Status:** Approved for remediation

---

### Example 2: Good Enrichment (82/100)

**Scenario:** CVE-2024-9012 Nginx Path Traversal
**Analyst:** Alex
**Reviewer:** Riley

---

**Review Metadata:**

- **Ticket ID:** AOD-9012
- **CVE:** CVE-2024-9012
- **Analyst:** Alex
- **Reviewer:** Riley (Security Review Specialist)
- **Review Date:** 2025-01-15
- **Quality Score:** 82/100 (Good)

---

**Executive Summary:**

Solid enrichment with accurate technical analysis and good remediation guidance. Some gaps in business context detail and source citations could be improved. Overall assessment: Good - meets quality standards with room for enhancement.

---

**Strengths & What Went Well:**

- Accurate CVSS and EPSS scores verified against NVD and FIRST
- Clear remediation guidance with specific Nginx version to patch (1.24.2)
- All 12 template sections populated
- Good ATT&CK mapping with appropriate tactics and techniques (T1190)
- Well-organized and professionally formatted

---

**Quality Dimension Scores:**

| Dimension             | Score | Weight | Weighted  | Assessment                                     |
| --------------------- | ----- | ------ | --------- | ---------------------------------------------- |
| Technical Accuracy    | 86%   | 25%    | 21.50     | Excellent                                      |
| Completeness          | 95%   | 20%    | 19.00     | Excellent                                      |
| Actionability         | 75%   | 15%    | 11.25     | Good - remediation clear, verification missing |
| Contextualization     | 65%   | 15%    | 9.75      | Needs Improvement - business impact vague      |
| Documentation Quality | 90%   | 10%    | 9.00      | Excellent                                      |
| Attack Mapping        | 85%   | 5%     | 4.25      | Good                                           |
| Cognitive Bias        | 80%   | 5%     | 4.00      | Good                                           |
| Source Citation       | 65%   | 5%     | 3.25      | Needs Improvement - some missing sources       |
| **TOTAL**             |       |        | **82.00** | **Good**                                       |

---

**Critical Issues:** None identified

---

**Significant Gaps:**

1. **Business Impact Vague:** "Affects web services" is too general
   - **Recommendation:** Specify which business processes (e.g., "Customer portal login, API authentication for mobile app")
   - **Resource:** docs/data/business-impact-assessment-guide.md
   - **Effort:** 5 minutes

2. **Missing Sources:** EPSS score cited without source URL
   - **Recommendation:** Add FIRST EPSS source: https://www.first.org/epss/
   - **Resource:** docs/checklists/source-citation-checklist.md
   - **Effort:** 2 minutes

3. **Verification Steps Missing:** No post-patch verification guidance
   - **Recommendation:** Add "Test with `curl` command targeting path traversal pattern to verify patch (e.g., `curl http://server/../../../etc/passwd` should return 403)"
   - **Effort:** 3 minutes

---

**Minor Improvements:**

4. **Related CVEs:** Section states "None" - consider checking for Nginx CVEs from same timeframe
   - **Resource:** NVD search by product and date range
   - **Effort:** 5 minutes (optional)

---

**Recommendations (Prioritized):**

**HIGH (Should Fix):**

1. Enhance business impact section with specific processes (5 min)
2. Add EPSS source citation (2 min)

**MEDIUM (Recommended):** 3. Add verification steps (3 min)

**LOW (Optional):** 4. Research related CVEs (5 min)

**Total Estimated Effort:** 10 minutes for HIGH priority fixes

---

**Conversation Starters:**

- How do you typically gather business impact information for web servers?
- What verification approaches work best for path traversal vulnerabilities in your experience?

---

**Next Steps:**

1. Address 2 HIGH priority gaps (estimated 7 minutes total)
2. Consider MEDIUM priority verification steps (optional 3 minutes)
3. **Status:** Approved for remediation with recommended enhancements

---

### Example 3: Needs Improvement (68/100)

**Scenario:** CVE-2024-3456 Jenkins Authentication Bypass
**Analyst:** Sam
**Reviewer:** Riley

---

**Review Metadata:**

- **Ticket ID:** AOD-3456
- **CVE:** CVE-2024-3456
- **Analyst:** Sam
- **Reviewer:** Riley (Security Review Specialist)
- **Review Date:** 2025-01-15
- **Quality Score:** 68/100 (Needs Improvement)

---

**Executive Summary:**

Enrichment demonstrates good research effort with some technical accuracy. However, several critical gaps in remediation guidance and business context need to be addressed before proceeding to remediation. This review is intended to help improve enrichment quality - see detailed recommendations below.

---

**Strengths & What Went Well:**

- CVE research performed using Perplexity AI tools
- Template structure followed with all 12 sections present
- CVSS score verified against NVD (9.8 Critical)
- Clear formatting and organization

---

**Quality Dimension Scores:**

| Dimension             | Score | Weight | Weighted  | Assessment                                     |
| --------------------- | ----- | ------ | --------- | ---------------------------------------------- |
| Technical Accuracy    | 75%   | 25%    | 18.75     | Good - some KEV status discrepancy             |
| Completeness          | 85%   | 20%    | 17.00     | Good - some sections minimal                   |
| Actionability         | 45%   | 15%    | 6.75      | Inadequate - remediation too vague             |
| Contextualization     | 50%   | 15%    | 7.50      | Inadequate - missing ACR and impact            |
| Documentation Quality | 90%   | 10%    | 9.00      | Excellent                                      |
| Attack Mapping        | 60%   | 5%     | 3.00      | Needs Improvement - T-number invalid           |
| Cognitive Bias        | 70%   | 5%     | 3.50      | Needs Improvement - confirmation bias detected |
| Source Citation       | 50%   | 5%     | 2.50      | Inadequate - missing key sources               |
| **TOTAL**             |       |        | **68.00** | **Needs Improvement**                          |

---

**Critical Issues:**

1. **Vague Remediation Guidance:** "Update Jenkins" - no specific version provided
   - **Impact:** DevOps cannot act without specific patch version
   - **Recommendation:** Research vendor advisory for specific patched version (e.g., "Update to Jenkins 2.440.2 or later")
   - **Resource:** Jenkins Security Advisory: https://www.jenkins.io/security/advisories/
   - **Effort:** 10 minutes
   - **Next Step:** Re-research CVE-2024-3456 patch details

2. **Missing Business Context:** ACR and System Exposure fields not populated
   - **Impact:** Priority assessment may be incorrect
   - **Recommendation:** Consult asset inventory for Jenkins CI/CD server criticality, confirm network exposure
   - **Resource:** docs/data/business-context-assessment-guide.md
   - **Effort:** 5-10 minutes
   - **Next Step:** Contact asset owner or check CMDB

---

**Significant Gaps:**

3. **KEV Status Discrepancy:** Enrichment states "KEV: No" but CISA catalog shows CVE-2024-3456 added 2024-10-15
   - **Recommendation:** Re-check CISA KEV catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
   - **Effort:** 3 minutes

4. **Invalid ATT&CK Technique:** T-9999 is not a valid MITRE ATT&CK technique number
   - **Recommendation:** Authentication bypass typically maps to T1078 (Valid Accounts) or T1110 (Brute Force)
   - **Resource:** MITRE ATT&CK Matrix: https://attack.mitre.org/
   - **Effort:** 5 minutes

5. **Missing EPSS Source:** EPSS score cited without verification source
   - **Recommendation:** Add FIRST EPSS source URL: https://www.first.org/epss/
   - **Effort:** 2 minutes

---

**Cognitive Bias Assessment:**

**Confirmation Bias Detected:** Threat Intelligence section focuses only on absence of exploitation evidence, without balanced research into exploitation likelihood.

**Debiasing Recommendation:** Research both exploitation and non-exploitation indicators for balanced analysis. Consider historical Jenkins vulnerability exploitation patterns, not just current absence of activity.

---

**Recommendations (Prioritized):**

**CRITICAL (Must Fix Before Remediation):**

1. Research specific Jenkins patch version (10 min)
2. Gather business context (ACR, Exposure) (5-10 min)

**HIGH (Should Fix):** 3. Verify KEV status against CISA catalog (3 min) 4. Correct ATT&CK T-number (5 min) 5. Add EPSS source citation (2 min)

**MEDIUM (Recommended):** 6. Balance threat intelligence analysis to avoid confirmation bias

**Total Estimated Effort:** 25-35 minutes for critical and high-priority fixes

---

**Learning Resources:**

- Remediation Guidance Best Practices: docs/data/remediation-guidance-best-practices.md
- Business Context Assessment: docs/data/business-context-assessment-guide.md
- MITRE ATT&CK Mapping Guide: docs/data/mitre-attack-mapping-guide.md
- Source Citation Standards: docs/checklists/source-citation-checklist.md

---

**Conversation Starters:**

- What challenges did you encounter researching this CVE?
- How can I help you improve the efficiency of your remediation research?
- Would a vendor advisory checklist be helpful for future enrichments?

---

**Next Steps:**

1. Address 2 CRITICAL issues (15-20 minutes)
2. Address 3 HIGH issues (10 minutes)
3. Re-submit enrichment for review
4. Optional: Schedule 15-minute pairing session to discuss process improvements

**Status:** Return to analyst for remediation of critical and high-priority gaps

---

## Frequently Asked Questions

### Q: How long does a typical review take?

**A:** Review duration varies by workflow pattern:

- **Full Review (\*review-enrichment):** 15-20 minutes for complete 7-stage workflow
- **Fact-Check Only (\*fact-check):** 5 minutes for technical verification
- **Bias Detection Only (\*detect-bias):** 5 minutes for cognitive bias analysis
- **Manual Stage-by-Stage:** 25-30 minutes (educational/training workflow)

### Q: Can I customize the 8-dimension weights?

**A:** The current framework uses research-backed weights optimized for vulnerability enrichment quality. Customization is not currently supported, but if you have a compelling use case for different weights, please discuss with the security team lead.

### Q: What if I disagree with the agent's assessment?

**A:** The Security Reviewer agent provides systematic analysis, but human judgment is always final. If you disagree:

1. Review the specific dimension checklist to understand the scoring rationale
2. Use `*fact-check` to independently verify factual claims
3. Discuss with the analyst to understand their perspective
4. Adjust recommendations based on context the agent may not have considered
5. Document your reasoning in the review report

### Q: How do I handle enrichments that are partially complete?

**A:** For incomplete enrichments:

1. Run `*review-enrichment` - the agent will identify missing sections in Completeness dimension
2. Categorize missing sections as Critical (blocks remediation) vs. Nice-to-Have
3. Provide clear guidance on which sections must be completed before remediation
4. Return to analyst with specific completion requirements

### Q: Should I review my own enrichments?

**A:** Self-review is valuable for learning and quality improvement, but **peer review is required** for all enrichments before remediation. Self-review can help you identify gaps before submitting for peer review, reducing review cycles.

### Q: What if the enrichment has critical security issues?

**A:** If you identify critical security misassessments (e.g., Critical priority assigned to Low risk, or vice versa):

1. Mark as "Critical Issue" in review report
2. Immediately notify analyst and security team lead (don't wait for review posting)
3. Block remediation until reassessment complete
4. Document the security impact in review

### Q: How do I balance thoroughness with time constraints?

**A:** Prioritize review depth based on enrichment priority:

- **Critical/High Priority Vulns:** Full 7-stage review (15-20 min)
- **Medium Priority Vulns:** Focus on Technical Accuracy, Completeness, Actionability dimensions (10 min)
- **Low Priority Vulns:** Fact-check only for accuracy (5 min)

Always run full review for first-time analysts or training scenarios.

### Q: Can I use the agent for training new analysts?

**A:** Yes! The Security Reviewer agent is excellent for training:

1. Use **stage-by-stage review workflow** to teach 8-dimension framework
2. Review example enrichments together, comparing agent assessment to manual review
3. Use **conversation starters** to foster discussion about best practices
4. Pair new analysts with experienced reviewers for collaborative learning

---

## Additional Resources

- **Installation Guide:** `docs/INSTALLATION.md` - Setup MCP connections and JIRA custom fields
- **Security Analyst Agent Guide:** `docs/user-guide/security-analyst-agent.md` - Understand enrichment workflow
- **Architecture Documentation:** `docs/architecture/` - System design and technical details
- **Checklists:** `expansion-packs/bmad-1898-engineering/checklists/` - Quality checklists for each dimension

---

## Support & Feedback

**Questions or Issues:**

- Discord: https://discord.gg/gk8jAdXWmj
- GitHub Issues: https://github.com/bmadcode/bmad-method/issues
- Email: support@bmadcode.com

**Feedback:**
We continuously improve the Security Reviewer agent based on user feedback. Please share:

- Dimension weights that don't align with your priorities
- Bias detection improvements
- Additional review patterns or workflows
- Documentation gaps or unclear sections

---

**Document Version:** 1.0
**Last Updated:** 2025-01-15
**Maintained By:** BMAD Engineering Team

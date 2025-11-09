# Event Investigation Quality Assessment - Weighted Scoring System

## Overview

This document describes the weighted scoring system for event investigation quality assessment. The Security Reviewer agent uses 7 specialized checklists to systematically evaluate investigation quality across multiple dimensions.

**Total Quality Score:** Weighted combination of 7 dimension scores
**Range:** 0-100%
**Quality Classifications:** Excellent (90-100%), Good (75-89%), Needs Improvement (60-74%), Inadequate (<60%)

---

## Seven Quality Dimensions

### 1. Investigation Completeness (Weight: 25%)

**Checklist:** `investigation-completeness-checklist.md`
**Purpose:** Verify all required investigation steps were performed and documented
**Check Items:** 19 items (Alert metadata, Network identifiers, Investigation steps, Evidence & analysis)
**Scoring:** (Passed Items / 19) × 100 = Dimension Score

**Why 25% (Highest Weight)?**
Completeness is the foundation of quality. An incomplete investigation cannot be accurate, regardless of how well-written the documented portions are.

---

### 2. Technical Accuracy (Weight: 20%)

**Checklist:** `investigation-technical-accuracy-checklist.md`
**Purpose:** Verify factual correctness and technical validity
**Check Items:** 7 items (IP addresses, protocols, alert rules, terminology, log interpretation, attack vectors, logical consistency)
**Scoring:** (Passed Items / 7) × 100 = Dimension Score

**Why 20% (Second Highest)?**
Technical inaccuracies undermine all conclusions. Incorrect IPs, wrong protocols, or misinterpreted logs produce unreliable dispositions.

---

### 3. Disposition Reasoning (Weight: 20%)

**Checklist:** `disposition-reasoning-checklist.md`
**Purpose:** Verify logical, evidence-based true/false positive determination
**Check Items:** 7 items (Clear disposition, evidence support, alternatives, confidence level, escalation logic, context integration, next actions)
**Scoring:** (Passed Items / 7) × 100 = Dimension Score

**Why 20% (Joint Second Highest)?**
The disposition decision is the primary output of the investigation. All other work exists to support a correct disposition.

---

### 4. Investigation Contextualization (Weight: 15%)

**Checklist:** `investigation-contextualization-checklist.md`
**Purpose:** Verify business and operational context integration
**Check Items:** 7 items (Asset criticality, business impact, affected systems, risk level, client impact, SLA/compliance, environmental factors)
**Scoring:** (Passed Items / 7) × 100 = Dimension Score

**Why 15% (Third Highest)?**
Context transforms technical findings into business decisions. Same alert on test vs. production requires completely different responses.

---

### 5. Investigation Methodology (Weight: 10%)

**Checklist:** `investigation-methodology-checklist.md`
**Purpose:** Verify sound investigative process and rigor
**Check Items:** 6 items (Hypothesis-driven approach, multiple data sources, scope bounding, documented steps, negative findings, peer consultation)
**Scoring:** (Passed Items / 6) × 100 = Dimension Score

**Why 10% (Moderate Weight)?**
Good methodology improves consistency and quality but doesn't guarantee correct results (evidence quality matters more).

---

### 6. Documentation Quality (Weight: 5%)

**Checklist:** `investigation-documentation-quality-checklist.md`
**Purpose:** Verify clear, professional, structured documentation
**Check Items:** 6 items (Logical structure, professional tone, minimal typos, key findings summary, evidence references, timestamp consistency)
**Scoring:** (Passed Items / 6) × 100 = Dimension Score

**Why 5% (Low Weight)?**
Substance matters more than style. Perfect grammar with wrong conclusions is worse than typos with correct disposition.

---

### 7. Cognitive Bias Detection (Weight: 5%)

**Checklist:** `investigation-cognitive-bias-checklist.md`
**Purpose:** Verify objective analysis free from common cognitive biases
**Check Items:** 6 items (No confirmation bias, no anchoring bias, no availability bias, no recency bias, no automation bias, alternatives considered)
**Scoring:** (Passed Items / 6) × 100 = Dimension Score

**Why 5% (Low Weight)?**
Bias detection is valuable but subjective and difficult to measure objectively. However, severe bias can invalidate an otherwise complete investigation.

---

## Overall Quality Score Calculation

### Formula

```
Overall Score = (Completeness × 0.25) + (Accuracy × 0.20) + (Disposition × 0.20) +
                (Context × 0.15) + (Methodology × 0.10) + (Documentation × 0.05) + (Bias × 0.05)
```

### Example Calculation

**Investigation Dimension Scores:**
- Investigation Completeness: 18/19 passed = 95%
- Technical Accuracy: 6/7 passed = 86%
- Disposition Reasoning: 7/7 passed = 100%
- Contextualization: 5/7 passed = 71%
- Investigation Methodology: 5/6 passed = 83%
- Documentation Quality: 5/6 passed = 83%
- Cognitive Bias: 6/6 passed = 100%

**Overall Score Calculation:**
```
Overall = (95 × 0.25) + (86 × 0.20) + (100 × 0.20) + (71 × 0.15) + (83 × 0.10) + (83 × 0.05) + (100 × 0.05)
        = 23.75 + 17.2 + 20.0 + 10.65 + 8.3 + 4.15 + 5.0
        = 89.05%
```

**Quality Classification:** Good (75-89% range)

---

## Quality Classifications

### Excellent: 90-100%

**Characteristics:**
- Exemplary investigation with minor or no gaps
- All critical items passed (completeness, accuracy, disposition)
- Strong methodology and context integration
- Professional documentation
- Objective analysis (no significant biases)

**Typical Issues (Minor):**
- 1-2 missing contextual items (e.g., SLA implications not noted)
- Minor documentation inconsistencies
- Non-critical evidence gaps that don't affect disposition

**Action:** Accept investigation, use as training example

---

### Good: 75-89%

**Characteristics:**
- Solid investigation with some improvements needed
- Core elements present (evidence, disposition, reasoning)
- Adequate context and methodology
- Acceptable documentation quality
- Minor biases detected with limited impact

**Typical Issues (Moderate):**
- Missing some investigation steps (e.g., no historical context)
- Limited contextualization (asset criticality assessed but business impact not)
- Only 1 alternative hypothesis considered (requirement: 2+)
- Some documentation gaps (no executive summary)

**Action:** Accept with recommendations for improvement

---

### Needs Improvement: 60-74%

**Characteristics:**
- Significant gaps requiring revision
- Disposition may be correct but poorly supported
- Important context missing
- Weak methodology or evidence
- Moderate biases affecting conclusions

**Typical Issues (Significant):**
- Missing critical evidence (no logs collected beyond alert)
- Weak disposition reasoning (assertion without evidence)
- No alternatives considered (confirmation bias risk)
- No context integration (asset criticality not assessed)
- Single data source (insufficient verification)

**Action:** Return to analyst for revision with specific feedback

---

### Inadequate: <60%

**Characteristics:**
- Major deficiencies, investigation must be redone
- Disposition likely incorrect
- Missing most required elements
- No clear methodology
- Severe biases detected

**Typical Issues (Critical):**
- Completeness <50% (most investigation steps skipped)
- Technical errors (wrong IPs, misinterpreted logs)
- No disposition reasoning (assertion only)
- No evidence collected beyond alert metadata
- Severe automation bias (blindly accepted alert conclusion)

**Action:** Reject investigation, assign to senior analyst for re-investigation

---

## Event-Specific Issue Detection Patterns

These patterns help identify common investigation failures specific to event investigations:

### 1. Missing Evidence Pattern

**Indicators:**
- No logs collected beyond alert metadata
- No correlation performed (event analyzed in isolation)
- No historical context (can't distinguish anomaly from baseline)
- No asset ownership confirmed

**Impact:** Cannot verify disposition, high risk of incorrect conclusion

**Detected By:**
- Investigation Completeness checklist (items 11-15: Investigation steps)
- Investigation Methodology checklist (item 2: Multiple data sources)

**Example:**
```
Alert: SSH Connection 10.50.1.100 → 10.10.5.25
Investigation: Internal SSH traffic
Disposition: False Positive
```
Missing: Logs, correlation, historical pattern, asset verification

---

### 2. Weak Disposition Reasoning Pattern

**Indicators:**
- Conclusion without evidence ("This is normal" - no supporting data)
- No alternatives considered (confirmation bias risk)
- Missing confidence level (uncertainty not acknowledged)
- No escalation logic (escalate/close decision unexplained)

**Impact:** Unsupported disposition, cannot verify or trust conclusion

**Detected By:**
- Disposition Reasoning checklist (all 7 items)
- Cognitive Bias checklist (items 1, 6: Confirmation bias, alternatives)

**Example:**
```
Disposition: False Positive
Reasoning: Looks like normal activity
Next Actions: Close ticket
```
Missing: Evidence, alternatives, confidence level, escalation logic

---

### 3. Incomplete Correlation Pattern

**Indicators:**
- Single event analyzed in isolation
- No timeline reconstruction (before/after events not reviewed)
- No related events identified
- Missing context from other systems

**Impact:** Missed attack patterns, incomplete understanding of incident scope

**Detected By:**
- Investigation Completeness checklist (item 12: Correlation performed)
- Investigation Methodology checklist (item 2: Multiple data sources)

**Example:**
```
Alert: Suspicious outbound connection at 14:35 UTC
Investigation: Reviewed firewall logs for destination IP
Disposition: True Positive

Missing Correlation:
- Didn't check what happened BEFORE connection (process execution? file download?)
- Didn't check what happened AFTER (data transfer? persistent connection?)
- Didn't check OTHER systems for related activity (same source IP to other destinations?)
```

---

### 4. Insufficient Contextualization Pattern

**Indicators:**
- No asset criticality assessed
- No business impact assessment
- Asset type unknown (server? workstation? ICS device?)
- Risk level = Alert severity (no independent assessment)

**Impact:** Cannot prioritize response, may over/under-escalate

**Detected By:**
- Investigation Contextualization checklist (items 1-4: Asset criticality, business impact, affected systems, risk level)
- Cognitive Bias checklist (item 2: Anchoring bias - over-relying on alert severity)

**Example:**
```
Alert: Critical Severity - Port Scan Detected
Disposition: True Positive
Escalation: Immediate (Critical severity)

Missing Context:
- Source IP = Authorized vulnerability scanner in test environment
- Target = Development server (non-production)
- Scheduled activity during approved scan window
```
Without context, FP escalated as critical incident

---

### 5. Shallow Methodology Pattern

**Indicators:**
- No hypothesis stated (investigation lacks direction)
- Single data source only (alert metadata only)
- No negative findings documented ("didn't check X" vs. "checked X, found nothing")
- No investigation steps documented (can't reproduce or verify)

**Impact:** Unreliable results, can't verify methodology, inconsistent quality

**Detected By:**
- Investigation Methodology checklist (all 6 items)

**Example:**
```
Alert: Malware Detection
Investigation: Ran AV scan, no detection
Disposition: False Positive
```

**Shallow Methodology:**
- No hypothesis ("What triggered alert? Process? File? Network?")
- Single source (AV only - didn't check EDR, logs, network traffic)
- No steps ("Ran AV scan" - what exactly? Full scan? Quick scan? Which files?)
- No negatives ("No detection" - but did you check process execution? Network connections? Registry changes?)

---

### 6. Automation Bias Pattern

**Indicators:**
- Alert disposition = investigation disposition (no independent verification)
- Alert severity copied to risk assessment (no context considered)
- Alert description parroted as conclusion
- No evidence collected beyond alert metadata

**Impact:** Missed false positives, incorrect escalations, wasted resources

**Detected By:**
- Cognitive Bias checklist (item 5: Automation bias)
- Investigation Completeness checklist (item 16: Evidence documented)
- Disposition Reasoning checklist (item 2: Evidence support)

**Example:**
```
Alert: Critical - APT Lateral Movement Detected
Investigation: Alert system classified this as Critical APT activity
Disposition: True Positive - APT lateral movement (Critical)
Escalation: Immediate IR response
```

**Automation Bias Detected:**
- No verification of "APT" claim (no APT indicators checked)
- Severity = alert severity (no independent assessment)
- Disposition = alert classification (no evidence collection)
- Escalation based on automation, not analyst judgment

**Correct Approach:**
- Treat alert as hypothesis: "Alert claims APT - does evidence support this?"
- Collect independent evidence (logs, correlation, historical pattern)
- Assess severity based on context (asset criticality, business impact)
- Reach independent conclusion (may differ from alert)

---

## Usage Guidelines

### For Security Reviewer Agent

1. **Execute All 7 Checklists:** Run each checklist against the investigation document
2. **Calculate Dimension Scores:** (Passed / Total) × 100 for each checklist
3. **Calculate Overall Score:** Apply weighted formula
4. **Classify Quality:** Excellent/Good/Needs Improvement/Inadequate
5. **Document Findings:** List specific failures and recommendations
6. **Make Decision:** Accept, Accept with recommendations, Return for revision, or Reject

### For Security Analyst (Self-Review)

Before submitting investigation for review:

✓ **Run Completeness Checklist:** All 19 items present?
✓ **Verify Technical Accuracy:** IPs, protocols, logs correct?
✓ **Check Disposition Logic:** Evidence supports conclusion? Alternatives considered?
✓ **Add Context:** Asset criticality, business impact assessed?
✓ **Document Methodology:** Steps clear, multiple sources consulted?
✓ **Review Documentation:** Professional, clear, summarized?
✓ **Self-Check Biases:** Am I blindly trusting the alert? Did I seek contradicting evidence?

---

## Integration with Security Reviewer Agent

The Security Reviewer agent (Story 2.1, extended in Story 7.4) will:

1. **Auto-detect** event investigation documents (YAML front-matter: `documentType: event-investigation`)
2. **Execute** all 7 event investigation checklists via `execute-checklist.md` task
3. **Calculate** weighted overall quality score
4. **Generate** review report using `event-review-report-tmpl.md` (Story 7.3)
5. **Provide** specific improvement recommendations for failed items
6. **Track** quality trends over time (analyst improvement, common failure patterns)

---

## References

- **Story 7.2:** Event Investigation Quality Checklists (This story - checklist creation)
- **Story 7.3:** Event Investigation Review Report Template (Review report generation)
- **Story 7.4:** Security Reviewer Auto-Detection and Event Review (Agent integration)
- **Epic 7 PRD:** Security Event Investigation Review Capability (Full feature specification)
- **Story 2.1:** Security Reviewer Agent (Base agent, CVE enrichment reviews)
- **Story 2.2:** Systematic Quality Evaluation (8-dimension CVE checklist system)

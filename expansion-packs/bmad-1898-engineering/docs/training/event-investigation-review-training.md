# Event Investigation Review Training

## Training Overview

**Course Title:** Security Event Investigation Quality Review
**Duration:** 4-6 hours (self-paced) or 1-day instructor-led
**Target Audience:** Security team leads, senior analysts, peer reviewers
**Prerequisites:** Completion of "Event Investigation Training" or equivalent experience
**Learning Objectives:**
- Apply 7-dimension quality framework for event investigations
- Conduct blameless,constructive peer reviews
- Validate disposition decisions (TP/FP/BTP)
- Detect cognitive biases in investigation reports
- Provide actionable recommendations for improvement

**Training Structure:**
- 6 learning modules (theory + practice)
- Real-world review scenarios
- Final competency assessment
- Review templates and job aids

---

## Module 1: Introduction to Event Investigation Review

### Learning Objectives
- Understand review purpose and philosophy
- Distinguish between analyst and reviewer roles
- Apply blameless review culture

### Why Review Event Investigations?

**Quality Assurance:**
- Ensure disposition accuracy (avoid misclassified TP/FP/BTP)
- Validate evidence completeness (all sources consulted?)
- Verify reasoning soundness (logic supported by evidence?)

**Learning & Improvement:**
- Identify investigation gaps (missed evidence, insufficient context)
- Detect cognitive biases (automation bias, confirmation bias)
- Share best practices (what went well?)

**Risk Mitigation:**
- Prevent false containment (FP classified as TP → unnecessary business disruption)
- Prevent missed incidents (TP classified as FP → actual attack ignored)
- Ensure appropriate escalation (safety-critical assets, major incidents)

### Reviewer vs Analyst Roles

| Aspect                  | Analyst (Investigator)                  | Reviewer (Quality Assessor)                      |
| ----------------------- | --------------------------------------- | ------------------------------------------------ |
| **Primary Goal**        | Determine disposition (TP/FP/BTP)       | Validate disposition accuracy                    |
| **Timeline**            | 15-25 minutes (investigation)           | 20-25 minutes (review)                           |
| **Perspective**         | First-hand investigation                | Independent assessment                           |
| **Tools**               | `*investigate-event`                    | `*review-enrichment --type=event`                |
| **Output**              | Investigation report + disposition      | Review report + quality scores                   |
| **Escalation Trigger**  | TP confirmed (escalate to IR)           | Disposition disagreement (escalate to team lead) |

### Blameless Review Culture

**Core Principle:** Reviews focus on **work quality**, not analyst performance.

**Blameless Language Examples:**

| ❌ Blame Language                      | ✅ Blameless Language                                                          |
| -------------------------------------- | ------------------------------------------------------------------------------ |
| "You failed to collect firewall logs"  | "Firewall logs missing - recommend collecting for corroboration"              |
| "This disposition is wrong"            | "Disposition assessment differs - see reviewer notes for alternative reasoning"|
| "Incomplete investigation"             | "Additional evidence could strengthen disposition confidence"                  |
| "You missed obvious evidence"          | "Asset owner confirmation could provide additional context"                    |

**Constructive Feedback Structure:**
1. **Strengths First:** Acknowledge what went well
2. **Gaps Identified:** Specific, actionable areas for improvement
3. **Learning Resources:** Links to documentation, checklists, training
4. **Conversation Starters:** Questions to foster collaborative discussion

---

## Module 2: 7-Dimension Quality Framework

### Learning Objectives
- Apply 7 quality dimensions to event investigations
- Calculate weighted quality scores
- Classify investigation quality (Excellent/Good/Needs Improvement/Inadequate)

### The 7 Dimensions

**1. Investigation Completeness (25% weight)**
- All investigation steps performed (triage, evidence, analysis, disposition, recommendations)
- Evidence collected from multiple sources
- Historical context researched
- Business context gathered (change tickets, asset owner confirmation)

**2. Technical Accuracy (20% weight)**
- Protocol validation correct
- Network communication details accurate
- Alert signature interpretation correct
- Technical analysis sound (no protocol misinterpretations)

**3. Disposition Reasoning (20% weight)**
- Disposition supported by specific evidence
- Confidence level appropriate for evidence strength
- Alternative explanations considered
- Reasoning documented with clear rationale

**4. Contextualization (15% weight)**
- Business impact assessed
- Asset criticality evaluated
- Operational context understood
- ICS/SCADA considerations addressed (if applicable)

**5. Investigation Methodology (10% weight)**
- Hypothesis-driven approach followed
- Evidence collection systematic
- Correlation across data sources performed
- NIST SP 800-61 framework alignment

**6. Documentation Quality (5% weight)**
- Report clarity and organization
- Markdown formatting correct
- Evidence properly cited
- Recommendations specific and actionable

**7. Cognitive Bias (5% weight)**
- Automation bias avoided (not blindly trusting alert severity)
- Anchoring bias avoided (multiple hypotheses considered)
- Confirmation bias avoided (disconfirming evidence sought)
- Availability bias avoided (not over-relying on recent incidents)

### Quality Score Calculation

**Formula:**
```
Quality Score = (
  Investigation_Completeness × 0.25 +
  Technical_Accuracy × 0.20 +
  Disposition_Reasoning × 0.20 +
  Contextualization × 0.15 +
  Investigation_Methodology × 0.10 +
  Documentation_Quality × 0.05 +
  Cognitive_Bias × 0.05
)
```

**Classification:**
- **90-100:** Excellent - Exemplary work, minor/no revisions needed
- **75-89:** Good - Solid quality, some improvements recommended
- **60-74:** Needs Improvement - Significant gaps, revisions required
- **< 60:** Inadequate - Critical issues, substantial rework needed

### Hands-On Exercise 2.1: Dimension Scoring

**Investigation Report Excerpt:**
```
DISPOSITION: Benign True Positive (BTP)
CONFIDENCE: High

REASONING:
Valid SSH connection from authorized engineering workstation (ENG-WS-05).
Correlation with maintenance window (scheduled 2025-11-08 14:00).
No malicious indicators observed.

EVIDENCE COLLECTED:
- Claroty alert details
- Change ticket CHG-2024-5678
```

**Your Task:** Score the following dimensions (0-100%)

1. **Investigation Completeness:** ______%
   - What evidence is missing?
2. **Disposition Reasoning:** ______%
   - Is reasoning supported by evidence?
3. **Documentation Quality:** ______%
   - Is report clear and well-organized?

<details>
<summary>Answer Key</summary>

**1. Investigation Completeness: 60%** (Needs Improvement)
- **Missing Evidence:**
  - Firewall logs (corroborate connection)
  - Historical context (previous SSH connections to this PLC?)
  - Asset owner confirmation (John Smith confirmed activity?)
- **Present:**  Claroty alert, change ticket
- **Score Rationale:** 2 sources collected, but missing corroboration (should have 3+ sources for HIGH confidence)

**2. Disposition Reasoning: 75%** (Good)
- **Strengths:** Disposition supported by change ticket + maintenance window correlation
- **Gaps:** "No malicious indicators observed" - what indicators were checked? (should list: no exploit attempts, no persistence, no lateral movement)
- **Score Rationale:** Solid reasoning, but could be more specific

**3. Documentation Quality: 85%** (Excellent)
- **Strengths:** Clear structure, concise reasoning, easy to follow
- **Minor Gap:** Could include specific timestamps (when was maintenance window?)
- **Score Rationale:** Well-organized and professional

</details>

---

## Module 3: Disposition Validation

### Learning Objectives
- Validate TP/FP/BTP classifications
- Identify disposition errors
- Resolve disposition disagreements

### Disposition Validation Checklist

**True Positive (TP) Validation:**
- [ ] Malicious activity evidence present (attack signatures, unauthorized access)
- [ ] No legitimate business justification found
- [ ] No authorization documented (change ticket, asset owner approval)
- [ ] Confidence level matches evidence strength (HIGH requires 3+ sources)
- [ ] Escalation to IR team documented

**False Positive (FP) Validation:**
- [ ] Root cause identified (detection logic error, misconfiguration, outdated signature)
- [ ] No real activity in logs OR activity is benign and misinterpreted
- [ ] Detection tuning recommendation provided
- [ ] No escalation required (correct - FP has no security concern)

**Benign True Positive (BTP) Validation:**
- [ ] Real activity confirmed (not detection error)
- [ ] Authorization documented (change ticket, asset owner confirmation, business process)
- [ ] Activity aligns with expected behavior (maintenance, testing, administrative)
- [ ] Detection exception recommended (whitelist authorized activity)

### Common Disposition Errors

**Error 1: TP misclassified as BTP**

**Example:**
```
Analyst Disposition: Benign True Positive (BTP)
Reasoning: "SSH connection during maintenance window"

Reviewer Concerns:
- Source IP: 203.0.113.45 (EXTERNAL - not engineering workstation)
- Change ticket: Exists, but scheduled for NEXT week (not today)
- No asset owner confirmation
- After-hours activity (02:00 UTC)

Recommended Disposition: True Positive (TP)
Rationale: External source + wrong timeframe + no confirmation = suspicious
```

**Error 2: BTP misclassified as TP**

**Example:**
```
Analyst Disposition: True Positive (TP)
Reasoning: "Unusual HTTP traffic from HMI"

Reviewer Concerns:
- HTTP destination: update.vendor.com (legitimate SCADA software vendor)
- Change ticket: CHG-6789 "HMI software update" (scheduled for this time)
- Asset owner: Confirmed update in progress
- Process: "update-service.exe" (legitimate vendor software)

Recommended Disposition: Benign True Positive (BTP)
Rationale: Authorized software update, legitimate vendor, change ticket + confirmation
```

**Error 3: FP misclassified as BTP**

**Example:**
```
Analyst Disposition: Benign True Positive (BTP)
Reasoning: "Authorized engineering access"

Reviewer Concerns:
- Logs show NO actual SSH connection (firewall blocked, no session established)
- Claroty alert triggered on SYN packet only (connection attempt, not established)
- Root cause: Claroty signature too sensitive (triggers on attempt, not successful connection)

Recommended Disposition: False Positive (FP)
Rationale: No real activity occurred (connection blocked), detection logic error
```

### Disposition Disagreement Resolution

**Process:**
1. **Document Both Perspectives:**
   ```markdown
   **Analyst Disposition:** BTP
   **Reviewer Assessment:** DISAGREE - Recommend TP
   **Reviewer Reasoning:** [Specific evidence]
   **Recommendation:** Escalate to team lead for final disposition
   ```

2. **Collaborative Review Session:**
   - Schedule 15-30 min discussion
   - Walk through evidence together
   - Identify missing evidence or context
   - Attempt consensus

3. **Escalate if Unresolved:**
   - If no consensus in 30 min → escalate to team lead
   - Team lead reviews evidence and makes final call
   - Document escalation rationale

4. **Learning Opportunity:**
   - Acknowledge both perspectives
   - Frame as growth opportunity (not right/wrong)
   - Update investigation if new evidence found

---

## Module 4: Evidence Sufficiency Assessment

### Learning Objectives
- Assess evidence completeness
- Identify evidence gaps
- Determine confidence level appropriateness

### Evidence Sufficiency Criteria

**HIGH Confidence (3+ corroborating sources):**
```markdown
✅ SUFFICIENT Evidence for HIGH Confidence:
- Primary: Claroty alert details
- Corroborating: Firewall logs (connection confirmed)
- Corroborating: Change ticket CHG-1234 (authorization documented)
- Corroborating: Asset owner John Smith (confirmed activity)
Total: 4 sources → HIGH confidence appropriate
```

**MEDIUM Confidence (1-2 sources):**
```markdown
⚠️ LIMITED Evidence for MEDIUM Confidence:
- Primary: Snort alert (exploit attempt detected)
- Corroborating: Web server logs (HTTP 500 error)
Missing: Patch status verification, PCAP analysis, host logs
Total: 2 sources → MEDIUM confidence appropriate (would be HIGH with 3+)
```

**LOW Confidence (single source or significant gaps):**
```markdown
❌ INSUFFICIENT Evidence - LOW Confidence Only:
- Primary: Splunk alert (failed logins)
Missing: SSH auth logs, source asset identification, change ticket check
Total: 1 source → LOW confidence only (requires additional investigation)
```

### Evidence Gap Impact Assessment

**Minor Gaps (Acceptable):**
- PCAP not available (retention policy expired - expected)
- Host logs unavailable (legacy system limitation - expected)
- Impact: Reduce confidence to MEDIUM (still acceptable disposition)

**Significant Gaps (Requires Investigation):**
- No business context gathered (change ticket not checked)
- No asset owner confirmation (authorization uncertain)
- No historical baseline (cannot assess if activity normal)
- Impact: Cannot reliably determine disposition → Return for additional investigation

**Critical Gaps (Blocks Disposition):**
- Primary evidence missing (alert details incomplete)
- No source identification (cannot determine if internal/external)
- Timeline unclear (cannot correlate with other events)
- Impact: Investigation inadequate → Must collect critical evidence before disposition

### Hands-On Exercise 4.1: Evidence Assessment

**Investigation Report:**
```
DISPOSITION: True Positive (TP)
CONFIDENCE: High

EVIDENCE:
- Claroty alert: "Unauthorized HTTP from HMI to external IP"
- Destination IP: 203.0.113.45 (threat intel: known C2 server)
```

**Your Task:**
1. Is evidence sufficient for HIGH confidence? Why/why not?
2. What additional evidence should have been collected?
3. What is appropriate confidence level for evidence provided?

<details>
<summary>Answer Key</summary>

**1. Evidence Sufficiency:** NO - Insufficient for HIGH confidence
- Only 2 sources provided (need 3+ for HIGH)
- Missing corroborating evidence (firewall logs, host logs, asset owner confirmation)

**2. Additional Evidence Needed:**
- Firewall logs (confirm connection, duration, data transferred)
- HMI host logs (what process initiated HTTP? User logged in?)
- Asset owner confirmation (any authorized activity?)
- Historical context (has this HMI communicated externally before?)
- Change management (any tickets for this timeframe?)

**3. Appropriate Confidence:** MEDIUM (2 sources, TP disposition seems likely but needs corroboration)

**Reviewer Recommendation:**
- Disposition: Likely TP (threat intel match is strong indicator)
- Confidence: Downgrade to MEDIUM pending additional evidence collection
- Request additional investigation: Collect firewall logs + host logs
</details>

---

## Module 5: Cognitive Bias Detection

### Learning Objectives
- Detect 4 cognitive biases in investigation reports
- Provide debiasing recommendations
- Score bias dimension appropriately

### The 4 Cognitive Biases (Event Investigations)

#### 1. Automation Bias

**Definition:** Blindly trusting alert severity without independent validation

**Detection:**
```markdown
❌ AUTOMATION BIAS DETECTED:
Analyst: "Claroty alert is HIGH severity, therefore disposition is TP"
Issue: Did not validate severity with evidence (no independent analysis)
```

**Debiasing Recommendation:**
"Recommend independently validating alert severity using evidence collected (not inheriting platform classification). Consider business context and evidence strength when determining disposition."

#### 2. Anchoring Bias

**Definition:** Fixating on first hypothesis, ignoring alternatives

**Detection:**
```markdown
❌ ANCHORING BIAS DETECTED:
Analyst: "Alert says 'unauthorized', so I looked only for attack evidence"
Issue: Did not consider alternative hypotheses (authorized maintenance, detection error)
Evidence: Change ticket exists (not investigated), historical pattern not researched
```

**Debiasing Recommendation:**
"Recommend generating 2-3 hypotheses before evidence collection (malicious, authorized, detection error) and testing each against evidence."

#### 3. Confirmation Bias

**Definition:** Seeking only evidence that supports initial assessment

**Detection:**
```markdown
❌ CONFIRMATION BIAS DETECTED:
Analyst: "Alert triggered → looked for malicious indicators only"
Evidence Collected: Threat intel (C2 match), no business context
Evidence Missing: Change ticket check, asset owner confirmation
Issue: Only sought confirming evidence (attack indicators), ignored disconfirming evidence (authorization)
```

**Debiasing Recommendation:**
"Recommend actively seeking disconfirming evidence (check for authorization even when attack seems likely). Balance investigation with both confirming and disconfirming data."

#### 4. Availability Bias

**Definition:** Overweighting recent/memorable incidents

**Detection:**
```markdown
❌ AVAILABILITY BIAS DETECTED:
Recent Event: Malware incident last week (HMI compromise)
Current Alert: Unrelated HTTP traffic from different HMI
Analyst: "We just had HMI malware, this must be related malware!"
Issue: Assumed connection without evidence (different asset, different pattern)
```

**Debiasing Recommendation:**
"Recommend researching current alert independently from recent incidents. Validate connection with evidence before assuming pattern correlation."

### Bias Scoring

**Bias-Free Analysis:** 100% (no biases detected)
**Minor Bias:** 80-90% (one minor bias, doesn't impact disposition)
**Moderate Bias:** 60-79% (one significant bias or two minor biases)
**Significant Bias:** <60% (multiple biases, impacts disposition reliability)

---

## Module 6: Review Report Writing

### Learning Objectives
- Write constructive review reports
- Provide actionable recommendations
- Use blameless language consistently

### Review Report Structure

**1. Executive Summary (2-3 sentences)**
```markdown
**Executive Summary:**
Solid investigation with accurate disposition and good evidence collection.
Some gaps in business context gathering could be addressed to strengthen
confidence level. Overall assessment: Good quality.
```

**2. Strengths & What Went Well (Always First!)**
```markdown
**Strengths & What Went Well:**
- Accurate disposition (BTP correctly identified)
- Good evidence correlation (Claroty + firewall + change ticket)
- Clear documentation and professional formatting
```

**3. Quality Dimension Scores**
```markdown
| Dimension                   | Score | Weight | Weighted | Assessment                    |
| --------------------------- | ----- | ------ | -------- | ----------------------------- |
| Investigation Completeness  | 85%   | 25%    | 21.25    | Good - minor gaps            |
| Technical Accuracy          | 95%   | 20%    | 19.00    | Excellent                     |
| Disposition Reasoning       | 90%   | 20%    | 18.00    | Excellent                     |
| Contextualization           | 70%   | 15%    | 10.50    | Good - could enhance          |
| Investigation Methodology   | 85%   | 10%    | 8.50     | Good                          |
| Documentation Quality       | 90%   | 5%     | 4.50     | Excellent                     |
| Cognitive Bias              | 85%   | 5%     | 4.25     | Good - minor confirmation bias|
| **TOTAL**                   |       |        | **86.00**| **Good**                      |
```

**4. Gaps & Improvements**
```markdown
**Opportunities for Enhancement:**

1. **Business Context - Asset Owner Confirmation (MEDIUM)**
   - Gap: Asset owner not contacted to confirm authorization
   - Recommendation: Contact John Smith to verify firmware update
   - Effort: 5 minutes (email or phone call)
   - Resource: docs/troubleshooting-faq-best-practices.md#business-context

2. **Historical Context (LOW)**
   - Gap: No baseline for SSH frequency to this PLC
   - Recommendation: Research historical SSH connections (is quarterly pattern typical?)
   - Effort: 2 minutes (Claroty historical query)
```

**5. Recommendations**
```markdown
**Recommendations (Prioritized):**

**HIGH:** None (no critical gaps)

**MEDIUM:**
1. Gather asset owner confirmation for HIGH confidence investigations (5 min)

**LOW:**
2. Research historical baselines when available (2 min)

**Total Estimated Effort:** 7 minutes for MEDIUM + LOW improvements
```

**6. Disposition Validation**
```markdown
**Disposition Validation:**
✅ AGREE with analyst disposition (Benign True Positive)
✅ Confidence level appropriate (HIGH supported by 3 sources)
✅ Escalation decision correct (no escalation required for BTP)
```

**7. Conversation Starters**
```markdown
**Conversation Starters:**
- What challenges did you face gathering evidence for this investigation?
- How do you typically determine when you have sufficient evidence for HIGH confidence?
```

**8. Next Steps**
```markdown
**Next Steps:**
1. Optional: Gather asset owner confirmation (5-minute enhancement)
2. Excellent work - no critical revisions needed
3. **Status:** Approved as-is (enhancements optional)
```

---

## Review Scenarios

### Scenario 1: Excellent Investigation (Review Practice)

**Investigation Report:**
```
TICKET: AOD-4052
DISPOSITION: Benign True Positive (BTP)
CONFIDENCE: High

INVESTIGATION SUMMARY:
SSH connection from ENG-WS-05 (192.168.10.45) to PLC-ZONE-3-01 (10.20.30.15)
detected by Claroty rule #317 during scheduled maintenance window.

EVIDENCE:
1. Claroty Alert: SSH connection 14:23:15-14:41:57 UTC (18 min 42 sec duration)
2. Firewall Logs: Connection allowed per "Engineering Access" policy
3. Change Ticket: CHG-2024-5678 "PLC firmware update to v2.8.3" (scheduled 14:00-16:00 UTC)
4. Asset Owner: John Smith confirmed successful firmware update
5. Historical Context: Previous SSH connections every ~90 days (firmware maintenance pattern)

TECHNICAL ANALYSIS:
- Protocol: SSH (expected for firmware updates)
- Source: Authorized engineering workstation (ENG-WS-05 in approved list)
- Timing: Within scheduled maintenance window (no anomaly)
- No malicious indicators: No exploit attempts, persistence, lateral movement observed

DISPOSITION REASONING:
Real activity detected (not FP), but activity is authorized:
- Change ticket provides authorization
- Asset owner confirmed legitimate firmware update
- Historical pattern matches (quarterly maintenance)
- Security controls working as expected (engineering access properly logged)

RECOMMENDATIONS:
- Create Claroty exception for ENG-WS-05 → PLC-ZONE-* during approved change windows
- Integrate JIRA change management with Claroty (auto-suppress alerts)
- No containment required (authorized activity)
```

**Your Review Task:**
1. Score each of the 7 dimensions (0-100%)
2. Calculate weighted overall score
3. Write review report (Executive Summary + Strengths + Gaps + Recommendations)

<details>
<summary>Sample Review</summary>

**Dimension Scores:**
- Investigation Completeness: 100% (all steps performed, 5 evidence sources)
- Technical Accuracy: 95% (accurate protocol validation, analysis sound)
- Disposition Reasoning: 100% (excellent reasoning, well-supported)
- Contextualization: 95% (business context, asset owner confirmation, historical baseline)
- Investigation Methodology: 95% (systematic, hypothesis-driven)
- Documentation Quality: 100% (clear, professional, well-organized)
- Cognitive Bias: 95% (bias-free analysis)

**Weighted Score:** 97.5 (Excellent)

**Executive Summary:**
Outstanding investigation with comprehensive evidence collection, accurate
disposition, and excellent documentation. Analyst demonstrated mastery of
investigation methodology and blameless review principles. No revisions needed.

**Strengths:**
- Exceptional evidence collection (5 corroborating sources)
- Asset owner confirmation (proactive outreach to John Smith)
- Historical context researched (identified quarterly maintenance pattern)
- Clear technical analysis (protocol validation, malicious indicators checked)
- Actionable recommendations (Claroty exception + JIRA integration)

**Gaps:** None identified

**Recommendations:** None - excellent work

**Status:** Approved for close (exemplary investigation)
</details>

---

### Scenario 2: Needs Improvement (Review Practice)

**Investigation Report:**
```
TICKET: SEC-456
DISPOSITION: False Positive (FP)
CONFIDENCE: Medium

INVESTIGATION SUMMARY:
Alert for HTTP traffic from HMI. Checked logs, no malicious activity found.

EVIDENCE:
- Claroty alert

DISPOSITION REASONING:
Alert triggered but I couldn't find any issues. Probably false positive.

RECOMMENDATIONS:
- None
```

**Your Review Task:**
1. Identify gaps in each dimension
2. Score the investigation (0-100%)
3. Write review report with specific, actionable recommendations

<details>
<summary>Sample Review</summary>

**Critical Gaps:**
- Investigation Completeness: 30% (INADEQUATE)
  - Only Claroty alert collected (no firewall, host logs, change tickets)
  - No asset owner contact
  - No historical context

- Disposition Reasoning: 40% (INADEQUATE)
  - "Couldn't find any issues" is vague (what was checked?)
  - No specific evidence supporting FP classification
  - Root cause not identified (why did alert trigger?)

- Documentation Quality: 50% (INADEQUATE)
  - Minimal detail (investigation steps not documented)
  - No specific evidence cited
  - Recommendations missing

**Weighted Score:** 42 (Inadequate)

**Executive Summary:**
Investigation demonstrates effort but has significant gaps in evidence collection,
disposition reasoning, and documentation. Additional investigation required before
disposition can be validated. See detailed recommendations for improvement.

**Strengths:**
- Disposition classified (FP identified)
- Investigation initiated promptly

**Critical Improvements Needed:**

1. **Collect Missing Evidence (CRITICAL - 20 minutes)**
   - Firewall logs (confirm HTTP connection occurred)
   - HMI host logs (what process initiated HTTP?)
   - Change tickets (any authorized maintenance?)
   - Asset owner contact (is this expected?)
   - Resource: docs/workflows/event-investigation-workflow-deep-dive.md

2. **Identify FP Root Cause (CRITICAL - 10 minutes)**
   - Why did Claroty alert trigger?
   - Is this detection logic error, misconfiguration, or outdated signature?
   - Document specific root cause
   - Resource: docs/troubleshooting-faq-best-practices.md#false-positive-analysis

3. **Document Investigation Steps (HIGH - 5 minutes)**
   - What logs were checked? (be specific)
   - What analysis was performed?
   - Why was FP conclusion reached?
   - Resource: docs/user-guide/security-analyst-agent.md

**Status:** RETURN TO ANALYST for additional investigation (estimated 35 minutes)
</details>

---

## Final Assessment

### Practical Review Assessment (50 points)

**Investigation Report to Review:**

```
TICKET: AOD-8901
DISPOSITION: True Positive (TP)
CONFIDENCE: High

ALERT DETAILS:
Platform: Claroty
Rule: #204 "Unauthorized Protocol (HTTP)"
Source: HMI-ZONE-2-05 (10.30.40.88)
Destination: 93.184.216.34 (External IP)
Timestamp: 2025-11-10 15:45:22 UTC

EVIDENCE:
1. Claroty alert: 47 HTTP connections over 20 minutes
2. Threat Intelligence: Destination IP resolves to update.software-vendor.com (Akamai CDN)
3. HMI logs: Process "update-service.exe" initiated connections
4. No scheduled maintenance found

TECHNICAL ANALYSIS:
HTTP from HMI to internet is unauthorized per policy. While destination
appears legitimate (software vendor), this violates air-gap principle for OT.

DISPOSITION REASONING:
TP - Policy violation (OT-to-Internet communication not allowed). Even though
destination is legitimate vendor, unauthorized internet access from OT network
is security incident per company policy.

RECOMMENDATIONS:
- Escalate to incident response (policy violation)
- Investigate how HMI has internet access (should be air-gapped)
- Block HMI internet access at firewall
- Review all OT assets for internet connectivity
```

**Your Task (50 points):**

1. **[10 pts]** Score all 7 dimensions (provide scores + rationale for each)

2. **[10 pts]** Calculate weighted overall quality score and classify (Excellent/Good/Needs Improvement/Inadequate)

3. **[10 pts]** Disposition Validation: Do you agree with TP disposition and HIGH confidence? Explain why/why not.

4. **[10 pts]** Identify Evidence Gaps: What critical evidence is missing? How does this impact confidence level?

5. **[10 pts]** Write Review Report: Include Executive Summary, Strengths, Gaps, and Recommendations

### Assessment Scoring

**Grading Scale:**
- 45-50: Excellent (ready for independent event investigation reviews)
- 38-44: Good (ready with mentor oversight)
- 30-37: Needs Improvement (additional training recommended)
- < 30: Inadequate (retake training)

---

## Additional Resources

- **Security Reviewer User Guide:** `docs/user-guide/security-reviewer-agent.md`
- **Event Investigation Training:** `docs/training/event-investigation-training.md`
- **Workflow Deep Dive:** `docs/workflows/event-investigation-workflow-deep-dive.md`
- **Troubleshooting FAQ:** `docs/troubleshooting-faq-best-practices.md`

---

**Course Version:** 1.0
**Last Updated:** 2025-11-09
**Maintained By:** BMAD Engineering Team

# Security Reviewer Quick Reference Card
**Event Investigation Review Workflow**

---

## Command

```
*review-enrichment {ticket-id} --type=event
```

**Duration:** 10-20 minutes | **Output:** Review assessment with quality score

---

## 7-Stage Review Workflow

### Stage 1: Context Loading & Preparation (1-2 min)
- [ ] Load JIRA ticket (auto-detected or --type=event)
- [ ] Review alert metadata and analyst's investigation
- [ ] Note investigation duration and timestamp
- [ ] Identify alert platform (Claroty/Snort/Splunk)

### Stage 2: Investigation Completeness Review (25% weight)
- [ ] Alert metadata collected (platform, rule ID, severity, timestamp)
- [ ] Network identifiers documented (IPs, hostnames, protocols, ports)
- [ ] Evidence collected from relevant log sources
- [ ] Historical context researched (previous occurrences, patterns)
- [ ] Asset context assessed (criticality, function, business impact)
- [ ] Multiple evidence sources consulted

**Score:** 0-10 (0=Missing critical steps, 10=All steps thorough)

### Stage 3: Technical Accuracy Review (20% weight)
- [ ] Protocol validation correct
- [ ] Network communication details accurate
- [ ] Alert signature interpretation correct
- [ ] Technical terminology used appropriately
- [ ] Platform-specific analysis correct

**Score:** 0-10 (0=Major technical errors, 10=Completely accurate)

### Stage 4: Disposition Reasoning Review (20% weight)
- [ ] Disposition (TP/FP/BTP) supported by specific evidence
- [ ] Confidence level appropriate (High/Medium/Low)
- [ ] Alternative explanations considered
- [ ] Reasoning logically sound
- [ ] Evidence-to-conclusion chain clear

**Score:** 0-10 (0=Unsupported conclusion, 10=Excellent reasoning)

### Stage 5: Contextualization Review (15% weight)
- [ ] Asset criticality considered
- [ ] Business function context included
- [ ] ICS/SCADA safety implications assessed (if applicable)
- [ ] Industry/environment context appropriate

**Score:** 0-10 (0=No context, 10=Excellent contextualization)

### Stage 6: Investigation Methodology Review (10% weight)
- [ ] Hypothesis-driven approach used
- [ ] Logical investigation sequence followed
- [ ] Appropriate depth of analysis
- [ ] Evidence-based conclusions
- [ ] Multiple hypotheses considered

**Score:** 0-10 (0=No methodology, 10=Rigorous methodology)

### Stage 7: Documentation Quality & Cognitive Bias (10% weight)
- [ ] Clear, professional writing
- [ ] Evidence properly cited
- [ ] Timeline coherent
- [ ] No automation bias (over-trusting alerts)
- [ ] No confirmation bias (one-sided evidence)
- [ ] No anchoring bias (fixation on first evidence)

**Score (Documentation):** 0-10
**Score (Cognitive Bias):** 0-10

---

## Quality Score Calculation

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

**Interpretation:**
- **9-10:** Excellent (no changes needed)
- **7-8:** Good (minor improvements suggested)
- **5-6:** Adequate (moderate improvements needed)
- **3-4:** Poor (significant rework required)
- **0-2:** Unacceptable (return to analyst)

---

## Disposition Validation Matrix

| Analyst Disposition | Reviewer Assessment | Action |
|---------------------|---------------------|---------|
| TP | Agree TP | ✅ Approve, escalate to IR |
| TP | Disagree (FP/BTP) | ❌ Return to analyst, document reasoning |
| FP | Agree FP | ✅ Approve, close ticket |
| FP | Disagree (TP/BTP) | ❌ Return to analyst, re-investigate |
| BTP | Agree BTP | ✅ Approve, create exception |
| BTP | Disagree (TP/FP) | ❌ Return to analyst, validate authorization |

---

## Disposition Agreement Examples

### ✅ Agree: True Positive
**Analyst:** TP - SSH brute force attack
**Reviewer:** AGREE - Multiple evidence sources confirm unauthorized access attempts
**Action:** Approve, escalate to IR team

### ✅ Agree: False Positive
**Analyst:** FP - Alert signature mismatch
**Reviewer:** AGREE - PCAP analysis confirms benign traffic, signature needs tuning
**Action:** Approve, recommend tuning

### ✅ Agree: Benign True Positive
**Analyst:** BTP - Authorized maintenance activity
**Reviewer:** AGREE - Change ticket CHG-1234 validates authorization
**Action:** Approve, create whitelist exception

---

## Disposition Disagreement Examples

### ❌ Disagree: Analyst says FP, Reviewer says TP
**Analyst:** FP - Signature error
**Reviewer:** DISAGREE - Evidence shows successful exploitation (command execution in logs)
**Finding:** Incomplete evidence collection, missed host-level logs
**Action:** Return to analyst for re-investigation

### ❌ Disagree: Analyst says TP, Reviewer says BTP
**Analyst:** TP - Unauthorized SSH access
**Reviewer:** DISAGREE - Change ticket CHG-5678 authorizes vendor remote access
**Finding:** Missed change management context
**Action:** Return to analyst to validate authorization

### ❌ Disagree: Analyst says BTP, Reviewer says FP
**Analyst:** BTP - Authorized scanning activity
**Reviewer:** DISAGREE - Source IP is NOT authorized scanner, alert signature mismatch
**Finding:** Incorrect authorization assumption
**Action:** Return to analyst for verification

---

## Common Review Findings

| Finding | Description | Example |
|---------|-------------|---------|
| **Incomplete Evidence** | Missing log sources | No firewall logs consulted for network alert |
| **Weak Reasoning** | Disposition unsupported | "Looks like FP" without technical justification |
| **Missing Context** | No business/asset context | Didn't assess asset criticality or function |
| **Technical Error** | Protocol misunderstanding | Misinterpreted DNS traffic as C2 |
| **Automation Bias** | Over-trusted alert | Assumed alert correct without verification |
| **Confirmation Bias** | One-sided evidence | Only collected evidence supporting initial hypothesis |

---

## Reviewer Feedback Template

```markdown
## Review Assessment

**Overall Quality Score:** X.X / 10.0

**Dimension Scores:**
- Investigation Completeness: X/10 (25%)
- Technical Accuracy: X/10 (20%)
- Disposition Reasoning: X/10 (20%)
- Contextualization: X/10 (15%)
- Investigation Methodology: X/10 (10%)
- Documentation Quality: X/10 (5%)
- Cognitive Bias: X/10 (5%)

**Disposition Assessment:**
- Analyst Disposition: [TP/FP/BTP] (Confidence: [High/Medium/Low])
- Reviewer Assessment: [AGREE / DISAGREE]
- Reasoning: [Specific evidence-based explanation]

**Strengths:**
- [What the analyst did well]

**Improvement Areas:**
- [Specific, actionable improvements]

**Required Actions:**
- [What analyst must do if rework required]
```

---

## Escalation Criteria (Reviewer)

**Escalate to Security Lead if:**
- Disposition disagreement cannot be resolved
- Quality score < 3.0 (unacceptable quality)
- Potential critical security incident (TP with High severity)
- Analyst shows pattern of repeated errors (>3 tickets)
- Suspected malicious insider activity

---

## Blameless Review Culture

### DO:
- ✅ Focus on work quality, not analyst performance
- ✅ Provide specific, actionable feedback
- ✅ Recognize good work (acknowledge strengths)
- ✅ Frame feedback as learning opportunity
- ✅ Offer to collaborate on complex investigations

### DON'T:
- ❌ Use accusatory language ("You didn't...", "You failed...")
- ❌ Compare analysts to each other
- ❌ Focus on mistakes without constructive guidance
- ❌ Rush reviews to meet SLA
- ❌ Approve poor quality work to avoid conflict

---

## Review Timeline & SLAs

| Alert Severity | Review SLA | Escalation SLA (if DISAGREE) |
|----------------|------------|------------------------------|
| Critical       | 2 hours    | Immediate (< 30 min)         |
| High           | 8 hours    | 1 hour                       |
| Medium         | 48 hours   | 4 hours                      |
| Low            | N/A        | 8 hours                      |

---

## Common Reviewer Pitfalls

| Pitfall | Solution |
|---------|----------|
| Rubber-stamping (approving without review) | Follow all 7 stages systematically |
| Overly harsh feedback | Use blameless culture, focus on work not person |
| Inconsistent standards | Use 7-dimension framework consistently |
| Assuming analyst error | Verify your own understanding before disagreeing |
| Avoiding difficult conversations | Address disagreements professionally and promptly |

---

**Need Help?** See: `docs/troubleshooting-faq-best-practices.md`
**Training:** See: `docs/training/event-investigation-review-training.md`
**Workflow Deep Dive:** See: `docs/workflows/event-investigation-workflow-deep-dive.md`

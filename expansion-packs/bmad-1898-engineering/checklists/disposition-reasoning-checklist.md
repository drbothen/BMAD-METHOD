# Disposition Reasoning Checklist

**Weight:** 20%
**Purpose:** Verify logical, evidence-based true/false positive determination with clear escalation decision.

## Check Items

- [ ] **Clear Disposition Stated** - Disposition explicitly stated as True Positive (TP), False Positive (FP), or Benign True Positive (BTP)
- [ ] **Reasoning Supported by Evidence** - Specific evidence cited for disposition decision, not just assertions
- [ ] **Alternative Explanations Considered** - At least 2 alternative scenarios evaluated, with reasoning for acceptance/rejection
- [ ] **Confidence Level Stated** - Investigation confidence explicitly assigned (High/Medium/Low) with justification
- [ ] **Escalation Decision Justified** - Clear logic for escalate vs. close decision, including criteria applied
- [ ] **Business/Operational Context Factored Into Decision** - Context (asset criticality, business impact, timing) influenced disposition or escalation
- [ ] **Next Actions Clearly Specified** - Concrete next steps defined (alert tuning, escalation to IR, additional monitoring, etc.)

## Scoring

- **Total Items:** 7
- **Passed Items:** [count after review]
- **Score:** (Passed / 7) × 100 = ____%

## Guidance

### Disposition Definitions

**True Positive (TP):**
- Alert correctly identified malicious, unauthorized, or policy-violating activity
- Requires escalation or remediation
- Examples: Actual lateral movement, real malware execution, unauthorized access

**False Positive (FP):**
- Alert triggered on legitimate, authorized, or expected activity
- No security concern, no escalation needed
- May require alert tuning to reduce noise
- Examples: Authorized administrative activity, legitimate business processes

**Benign True Positive (BTP):**
- Alert correctly detected the behavior described (true positive)
- BUT behavior is authorized, expected, or non-malicious (benign)
- Tuning recommended to exclude known-good patterns
- Examples: Vulnerability scanner traffic, authorized penetration testing, scheduled maintenance

### Confidence Level Guidelines

**High Confidence:**
- Multiple corroborating evidence sources
- Historical pattern confirms current assessment
- Asset ownership and context verified
- No unexplained anomalies
- Example: "6 months of daily logs confirm scheduled backup operation"

**Medium Confidence:**
- Sufficient evidence for disposition but some gaps
- Reasonable assumptions made (documented)
- Minor inconsistencies explained
- Example: "Likely authorized activity based on timing and source, but asset owner not yet contacted"

**Low Confidence:**
- Limited evidence available
- Significant information gaps
- Conflicting indicators present
- Requires additional investigation or expert consultation
- Example: "Unknown process on critical asset, no historical baseline, awaiting threat intel analysis"

### Escalation Decision Criteria

**Escalate When:**
- Disposition = True Positive (confirmed malicious/unauthorized)
- Confidence = Low AND asset criticality = High/Critical (better safe than sorry)
- Context indicates potential business impact regardless of disposition
- Regulatory/compliance requirements mandate escalation
- Unusual activity on critical asset without clear explanation

**Close (No Escalation) When:**
- Disposition = False Positive or BTP with High confidence
- Evidence clearly indicates authorized/expected activity
- Asset criticality = Low AND no business impact
- Historical pattern well-established
- Alert tuning will prevent recurrence

### Examples

#### Example 1: Strong Disposition Reasoning

```
**Disposition:** False Positive

**Confidence Level:** High

**Evidence Supporting Disposition:**
1. Source IP 10.50.1.100 confirmed as authorized jump server (Asset DB entry #4782, Owner: IT Operations)
2. SSH connection to 10.10.5.25 occurs daily at 02:00 UTC ±5 minutes (87 occurrences in last 90 days)
3. Destination 10.10.5.25 is file-server-backup.corp.local (Network diagram confirms same zone, authorized backup target)
4. SSH key fingerprint SHA256:aa:bb:cc:dd:ee:ff matches IT Ops authorized key (Key registry entry #129)
5. User account: backup_user (Service account for automated backups, created 2023-06-15)
6. No concurrent suspicious activity on jump server (reviewed firewall logs, SIEM alerts, endpoint telemetry)

**Alternative Explanations Considered:**
1. **Unauthorized access via stolen jump server credentials**
   - Rejected: SSH public key authentication (not password), key fingerprint matches authorized key
   - Rejected: Timing matches known schedule (02:00 UTC daily), not random attacker timing
   - Rejected: No other IOCs on jump server (no privilege escalation, no persistence mechanisms)

2. **Lateral movement after jump server compromise**
   - Rejected: Jump server shows no compromise indicators (AV clean, no suspicious processes, no unexpected network connections)
   - Rejected: Connection pattern is identical to 90-day historical baseline (same time, same destination, same duration)
   - Rejected: Business context confirms scheduled backup operation (IT Ops provided backup schedule documentation)

**Business/Operational Context:**
- Asset criticality: Jump server (Critical), File server (High)
- Business function: Automated backup infrastructure (critical business function, data protection)
- Timing: Outside business hours (02:00 UTC = 9PM EST), consistent with maintenance window
- Operational approval: IT Operations confirmed scheduled backup operation in writing

**Escalation Decision:** No escalation required

**Reasoning:** High confidence in False Positive disposition based on:
- Multiple independent corroborating evidence sources (logs, asset DB, key registry, IT Ops confirmation)
- 90-day historical pattern eliminates anomaly hypothesis
- Authorized infrastructure performing documented business function
- No indicators of compromise on either system

**Next Actions:**
1. Tune Claroty alert rule SSH_Unusual_Destination_V2 to exclude jump-server-01 → file-server-backup SSH connections
2. Suggested suppression: Source 10.50.1.100, Destination 10.10.5.25, Port 22, Time window 00:00-04:00 UTC
3. Document tuning in alert management system with justification (authorized backup operation)
4. Schedule review in 30 days to validate tuning effectiveness
```

**Disposition Reasoning Score:** 7/7 = 100%

---

#### Example 2: Weak Disposition Reasoning

```
**Disposition:** False Positive

The alert looks like normal SSH traffic between internal systems. The IPs are both internal so this is probably just regular administrative activity. Closing as false positive.

**Next Actions:** Close ticket
```

**Missing Items:**
1. ✗ Clear disposition stated - Yes, but no definition or context
2. ✗ Evidence supporting disposition - No specific evidence cited
3. ✗ Alternative explanations - None considered
4. ✗ Confidence level - Not stated
5. ✗ Escalation decision justified - No reasoning provided
6. ✗ Business/operational context - Not considered
7. ✗ Next actions - "Close ticket" is not actionable (no alert tuning, no follow-up)

**Disposition Reasoning Score:** 1/7 = 14% (Inadequate)

---

#### Example 3: Moderate Disposition Reasoning

```
**Disposition:** Benign True Positive (BTP)

**Confidence Level:** Medium

**Evidence:**
- Alert correctly detected SSH connection from 10.50.1.100 to 10.10.5.25 (true positive)
- Source IP is authorized jump server per asset database
- Historical logs show this happens daily around 02:00 UTC
- SSH authentication succeeded with public key

**Alternative Considered:**
- Could be unauthorized access, but timing and key authentication suggest authorized backup

**Escalation Decision:** No escalation needed, recommend tuning alert to exclude this traffic

**Next Actions:** Suppress alert for this IP pair during 00:00-04:00 UTC window
```

**Disposition Reasoning Score:** 5/7 = 71%

**Strengths:**
✓ Disposition clear (BTP)
✓ Some evidence provided
✓ Confidence level stated
✓ Escalation decision made
✓ Next actions specified

**Weaknesses:**
✗ Only 1 alternative considered (requirement: at least 2)
✗ Business/operational context not explored (asset criticality, business function not mentioned)

---

### Common Disposition Reasoning Failures

**Failure Pattern 1: Assertion Without Evidence**
```
Disposition: False Positive
Reasoning: This is normal activity.
```
❌ No evidence, no justification, no verification

**Failure Pattern 2: Evidence Without Logic**
```
Evidence: SSH connection from 10.50.1.100 to 10.10.5.25 occurred at 02:00 UTC
Disposition: True Positive - malicious lateral movement
```
❌ Evidence doesn't support conclusion (no explanation of why routine timing = malicious)

**Failure Pattern 3: No Alternatives Considered**
```
Disposition: False Positive
Reasoning: Source IP is authorized jump server, so this is legitimate
```
❌ No consideration of jump server compromise, stolen credentials, or insider threat

**Failure Pattern 4: Missing Confidence Level**
```
Disposition: False Positive
Reasoning: Likely authorized activity based on source IP
```
❌ "Likely" suggests uncertainty but no confidence level stated, limits decision quality

**Failure Pattern 5: No Escalation Logic**
```
Disposition: True Positive
Next Actions: Escalate to SOC
```
❌ No explanation of why escalation needed, no criteria applied, no urgency level

**Failure Pattern 6: Context Ignored**
```
Disposition: False Positive
Reasoning: Just SSH traffic
```
❌ No consideration of asset criticality (could be critical production server), business impact, or timing

**Failure Pattern 7: Vague Next Actions**
```
Next Actions: Monitor
```
❌ "Monitor" is not actionable (monitor what? how long? what triggers action?)

### Weighting Rationale

**Why 20% (Joint Second Highest Weight)?**

The disposition decision is the primary output of the investigation. All other work (completeness, accuracy, context, methodology) exists to support a correct disposition. An investigation can be 100% complete and accurate, but if the disposition reasoning is flawed, the entire investigation fails its purpose.

**Impact of Poor Disposition Reasoning:**
- False positives marked as true positive → Waste IR resources, alert fatigue
- True positives marked as false positive → Security incidents missed, breaches undetected
- Weak reasoning → Dispositions overturned by reviewers, rework required
- No alternatives considered → Confirmation bias, wrong conclusions
- Missing confidence level → Inappropriate escalation decisions

**Quality Thresholds:**

**Excellent (6-7/7 passed):**
- Disposition clearly justified with multiple evidence sources
- Multiple alternatives evaluated and rejected with reasoning
- Confidence level appropriate to evidence quality
- Escalation decision follows logical criteria
- Context appropriately factored into decision

**Good (5/7 passed):**
- Disposition supported by adequate evidence
- At least 2 alternatives considered
- Confidence level stated
- Escalation decision reasonable

**Needs Improvement (3-4/7 passed):**
- Disposition stated but weak evidence
- Only 1 alternative considered or none
- Confidence level missing or unjustified
- Escalation decision unclear

**Inadequate (<3/7 passed):**
- Disposition assertion without evidence
- No alternatives considered
- No confidence level
- No escalation logic
- Context ignored

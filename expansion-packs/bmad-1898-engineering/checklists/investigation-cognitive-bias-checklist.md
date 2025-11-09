# Investigation Cognitive Bias Detection Checklist

**Weight:** 5%
**Purpose:** Verify objective analysis free from common cognitive biases that compromise investigative conclusions.

## Check Items

- [ ] **No Confirmation Bias** - Investigation considered disconfirming evidence, not just evidence supporting initial hypothesis
- [ ] **No Anchoring Bias** - Disposition not locked to initial alert severity without independent assessment and evidence collection
- [ ] **No Availability Bias** - Investigation didn't over-weight recent similar incidents without statistical justification
- [ ] **No Recency Bias** - Considered historical patterns (30/60/90 days), not just recent events or last occurrence
- [ ] **No Automation Bias** - Didn't blindly accept alert platform disposition, severity, or classification without independent verification
- [ ] **Alternative Hypotheses Considered** - At least 2 alternative scenarios evaluated and explicitly rejected with reasoning

## Scoring

- **Total Items:** 6
- **Passed Items:** [count after review]
- **Score:** (Passed / 6) × 100 = ____%

## Guidance

### 1. Confirmation Bias

**Definition:** Seeking or interpreting evidence to confirm pre-existing beliefs while dismissing contradicting evidence.

**Event Investigation Context:**
- Initial hypothesis: "This SSH connection is lateral movement"
- Confirmation bias: Only collecting evidence supporting malicious activity, ignoring evidence of authorized activity

**Detection Questions:**
- Did investigation seek evidence AGAINST the initial hypothesis?
- Were alternative explanations actively explored?
- Was contradicting evidence acknowledged and evaluated fairly?
- Are limitations or uncertainties noted?

**Red Flags:**
- Only documenting evidence supporting malicious interpretation
- Ignoring historical baseline showing normal pattern
- Dismissing asset DB confirmation of authorized source without investigation
- Cherry-picking log entries that look suspicious while excluding context

**Example - Confirmation Bias Present:**

```
Alert: SSH from 10.50.1.100 to 10.10.5.25

Initial Hypothesis: Unauthorized lateral movement

Investigation:
- SSH connection succeeded (indicates compromise)
- Non-business hours timing (02:00 AM - suspicious)
- Production systems involved (high risk)

Disposition: True Positive - Lateral movement attack

Evidence Collected: Alert details only
```

**Bias Analysis:**
❌ Only collected evidence supporting "malicious" hypothesis
❌ Didn't check historical logs (would show daily pattern)
❌ Didn't verify asset ownership (would show authorized jump server)
❌ Interpreted neutral facts (success, timing, production) as exclusively suspicious
❌ No alternative explanations considered

**Example - No Confirmation Bias:**

```
Alert: SSH from 10.50.1.100 to 10.10.5.25

Initial Hypothesis: Unauthorized lateral movement

Investigation:
✓ Collected evidence supporting malicious hypothesis:
  - Connection succeeded (could indicate compromise)
  - Non-business hours (02:00 AM - unusual timing)

✓ Collected evidence against malicious hypothesis:
  - Historical logs show 87 identical connections in last 90 days (all at 02:00 UTC)
  - Source IP confirmed as authorized jump server (Asset DB)
  - SSH key fingerprint matches IT Ops authorized key registry
  - No concurrent suspicious activity on source system

Alternative Hypothesis: Scheduled backup operation
Conclusion: Evidence refutes initial hypothesis → False Positive
```

✓ Actively sought disconfirming evidence
✓ Historical baseline checked (refuted "unusual" hypothesis)
✓ Alternative explanation considered and found more plausible

---

### 2. Anchoring Bias

**Definition:** Over-relying on the first piece of information encountered (the "anchor") when making decisions.

**Event Investigation Context:**
- Alert severity = "High" → Analyst assumes risk is high without independent assessment
- Alert says "Suspicious" → Analyst concludes activity is malicious without verification

**Detection Questions:**
- Is disposition based on multiple factors beyond alert severity?
- Did analyst independently assess risk using context (asset criticality, business impact)?
- Is alert severity treated as one input, not the final answer?
- Were mitigating factors (authorized activity, historical pattern, false positive history) given appropriate weight?

**Red Flags:**
- Disposition mirrors alert severity exactly (Alert: High → Disposition: High Risk TP) without independent analysis
- Ignoring business context that lowers actual risk
- Alert description copied verbatim as investigation conclusion
- No independent verification of alert accuracy

**Example - Anchoring Bias Present:**

```
Alert: Claroty High Severity - Suspicious SSH Connection

Disposition: True Positive (High Severity)

Reasoning: Alert classified this as High Severity and Suspicious, confirming as True Positive with High severity.
```

**Bias Analysis:**
❌ Analyst anchored to alert severity ("High")
❌ Analyst accepted alert's "Suspicious" classification without verification
❌ Disposition = parroting alert, no independent analysis
❌ No evidence collected beyond alert metadata

**Example - No Anchoring Bias:**

```
Alert: Claroty High Severity - Suspicious SSH Connection

Investigation:
- Alert Severity: High (initial classification)
- Asset Criticality: Critical (jump server) + High (file server)
- Business Impact: Low IF false positive (authorized backup), High IF true positive (lateral movement)
- Evidence:
  - 90-day pattern shows daily occurrence (authorized baseline)
  - SSH key matches authorized IT Ops key
  - IT Ops confirmed scheduled backup

Risk Assessment:
- Alert severity: High (Claroty's automated assessment)
- Actual risk: Low (authorized activity, no security concern)
- Confidence: High (multiple corroborating evidence sources)

Disposition: False Positive (despite High alert severity, evidence indicates authorized activity)
```

✓ Alert severity noted but not determinative
✓ Independent risk assessment performed
✓ Evidence-based conclusion differs from alert classification
✓ Analyst reached opposite conclusion (FP) than alert implied (Suspicious = TP)

---

### 3. Availability Bias

**Definition:** Overestimating the likelihood or importance of events that are easily recalled, often because they are recent or emotionally impactful.

**Event Investigation Context:**
- Recent ransomware incident involving SSH → Analyst assumes all SSH alerts are ransomware-related
- Memorable lateral movement attack last month → Every SSH connection now looks like lateral movement

**Detection Questions:**
- Is risk assessment data-driven (actual historical frequency, actual threat intel)?
- Does investigation mention recent incidents without establishing relevance?
- Are rare but memorable events given disproportionate weight?
- Is current alert assessed on its own merits vs. recent emotional context?

**Red Flags:**
- Referencing last week's incident without showing connection to current alert
- Elevating severity because alert "looks like" recent breach
- Using phrases like "could be another SolarWinds" or "might be ransomware like last month"
- Ignoring base rate data (how often does this alert type actually indicate compromise?)

**Example - Availability Bias Present:**

```
Alert: SSH Connection from 10.50.1.100 to 10.10.5.25

Investigation:
Last month we had a ransomware incident that started with SSH lateral movement. This alert looks similar - SSH connection to a file server. This could be the start of another ransomware attack.

Disposition: True Positive - Potential ransomware precursor

Escalation: Immediate escalation to IR team (threat of ransomware)
```

**Bias Analysis:**
❌ Over-weighted recent memorable incident (ransomware)
❌ No evidence linking current alert to ransomware
❌ Assumed similarity = same threat (SSH to file server ≠ ransomware automatically)
❌ Ignored base rate (how many SSH connections are actually ransomware vs. legitimate?)

**Example - No Availability Bias:**

```
Alert: SSH Connection from 10.50.1.100 to 10.10.5.25

Context:
- Last month: Ransomware incident involving SSH lateral movement
- Current alert: SSH connection to file server

Investigation:
✓ Checked for ransomware indicators:
  - Encryption activity: None detected
  - Mass file modifications: None detected
  - Unusual process execution: None detected
  - C2 communication: None detected

✓ Reviewed base rate data:
  - SSH alerts last 90 days: 1,247 total
  - SSH alerts confirmed malicious: 3 (0.24%)
  - SSH alerts as legitimate admin activity: 1,244 (99.76%)

✓ Current alert analysis:
  - 90-day historical pattern: Daily at 02:00 UTC (authorized backup)
  - SSH key: Matches authorized IT Ops key registry
  - No ransomware indicators present

Conclusion: While recent ransomware incident is noted, current alert shows characteristics of authorized backup operation (matches 99.76% base rate for legitimate SSH activity). No ransomware indicators detected.

Disposition: False Positive
```

✓ Recent incident noted but not determinative
✓ Base rate data used (most SSH alerts are FP)
✓ Specific threat indicators checked (not assumed)
✓ Evidence-based conclusion independent of recent emotional events

---

### 4. Recency Bias

**Definition:** Giving disproportionate weight to recent events or information while undervaluing historical patterns or persistent risks.

**Event Investigation Context:**
- Only checking last 24 hours of logs → Missing 90-day daily pattern
- Prioritizing today's alert over established baseline
- Assuming recent behavior is representative, ignoring long-term trends

**Detection Questions:**
- Did investigation review appropriate historical timeframe (30/60/90 days)?
- Are conclusions based on long-term patterns vs. recent snapshot?
- Is established baseline given appropriate weight vs. recent change?
- Were historical false positives for this rule reviewed?

**Red Flags:**
- Only reviewing last few hours or days of activity
- Ignoring established baseline that contradicts recent observation
- Treating first-time occurrence as suspicious without checking historical pattern
- No mention of historical context or trends

**Example - Recency Bias Present:**

```
Alert: SSH Connection from 10.50.1.100 to 10.10.5.25 at 02:00 UTC

Investigation:
Reviewed logs from last 6 hours. This is the only SSH connection detected from this source IP to this destination. Unusual activity.

Disposition: True Positive - Suspicious SSH connection
```

**Bias Analysis:**
❌ Only reviewed 6 hours (insufficient historical context)
❌ Concluded "unusual" without checking if this happens daily/weekly/monthly
❌ Recent snapshot (last 6h) treated as representative of normal baseline

**Example - No Recency Bias:**

```
Alert: SSH Connection from 10.50.1.100 to 10.10.5.25 at 02:00 UTC

Investigation:
Recent Activity (Last 24 hours):
- Single SSH connection at 02:00 UTC

Historical Pattern (Last 90 days):
- 87 SSH connections from 10.50.1.100 to 10.10.5.25
- All occurrences at 02:00 UTC ±5 minutes
- Pattern established since 2024-08-10 (3 months ago)

Analysis:
Current event matches established 90-day baseline (daily backup). Not unusual when historical context is considered.

Disposition: False Positive (Authorized scheduled activity)
```

✓ Appropriate historical timeframe reviewed (90 days)
✓ Long-term pattern identified (daily occurrence)
✓ Recent event assessed in context of established baseline

---

### 5. Automation Bias (NEW - Event Investigation Specific)

**Definition:** Over-relying on automated systems (alert platforms, SIEM correlation rules, security tools) without independent verification of their conclusions.

**Event Investigation Context:**
- Alert says "High Severity" → Analyst disposition: High Severity (no independent assessment)
- Alert says "Malicious Activity" → Analyst disposition: True Positive (no evidence validation)
- SIEM correlation rule fires → Analyst accepts correlation without reviewing individual events

**Why Automation Bias Matters in Event Investigation:**

Alert systems are valuable but imperfect:
- ✓ Detect patterns faster than humans
- ✓ Monitor 24/7/365 without fatigue
- ✗ Generate false positives (tuning is never perfect)
- ✗ Lack business context (can't know about scheduled maintenance, authorized changes)
- ✗ Static rules may not adapt to environmental changes

**Detection Questions:**
- Did analyst collect independent evidence beyond alert metadata?
- Was alert severity independently verified based on asset criticality and business context?
- Did analyst verify alert's technical claims (IPs, protocols, attack description)?
- Was alert classification (malicious/suspicious) treated as hypothesis vs. conclusion?

**Red Flags - Automation Bias Detected:**

🚩 Disposition reasoning = "Alert flagged this as malicious, so marking True Positive"
🚩 No logs collected beyond alert metadata
🚩 Alert severity directly copied to risk assessment without context
🚩 Alert description parroted as investigation conclusion
🚩 No verification of alert accuracy (e.g., IP addresses, protocols, attack vector)
🚩 SIEM correlation accepted without reviewing correlated events individually

**Example - Automation Bias Present:**

```
Alert: Claroty Critical Severity - Advanced Persistent Threat Activity Detected
Rule: APT_Lateral_Movement_Pattern_V3
Description: "SSH connection matching known APT lateral movement tactics"

Investigation:
Claroty classified this as Critical severity and APT activity. Alert rule specifically designed to detect APT lateral movement tactics.

Disposition: True Positive (Critical Severity - APT Activity)

Escalation: Immediate escalation to Incident Response (APT threat detected)

Next Actions: Initiate incident response procedures for APT compromise
```

**Bias Analysis:**
❌ Analyst blindly trusted alert classification ("Critical", "APT Activity")
❌ No independent evidence collection (no logs, no correlation, no historical review)
❌ Alert description copied as disposition reasoning
❌ No verification that activity actually matches APT tactics
❌ Escalation based solely on automated alert, not analyst judgment
❌ **Automation bias critical failure: Alert system's conclusion became analyst's conclusion with zero independent verification**

**Example - No Automation Bias (Independent Verification):**

```
Alert: Claroty Critical Severity - Advanced Persistent Threat Activity Detected
Rule: APT_Lateral_Movement_Pattern_V3
Description: "SSH connection matching known APT lateral movement tactics"

Investigation:

**Alert Claims (To Be Verified):**
- Severity: Critical (Claroty's automated assessment)
- Classification: APT lateral movement (rule-based detection)
- Tactics: SSH connection pattern matching APT TTPs

**Independent Evidence Collection:**

1. **Network Activity Verification:**
   - Source: 10.50.1.100 (Verified: Authorized jump server, Asset DB #4782)
   - Destination: 10.10.5.25 (Verified: Backup file server, Network diagram zone B)
   - Protocol: TCP/22 SSH (Verified: Log analysis confirms SSH v2)

2. **Historical Pattern Analysis:**
   - SIEM query (90 days): 87 identical connections, all at 02:00 UTC
   - Pattern established: 2024-08-10 to present (3 months)
   - Frequency: Daily (100% consistent)

3. **Authentication Verification:**
   - Method: Public key authentication (not password brute force)
   - Key fingerprint: SHA256:aa:bb:cc:dd:ee:ff
   - Key registry: Matches IT Ops authorized key (Entry #129, issued 2023-06-15)

4. **APT Tactic Verification:**
   - APT lateral movement indicators:
     ✗ No privilege escalation detected
     ✗ No persistence mechanisms created
     ✗ No C2 communication observed
     ✗ No data staging or exfiltration
     ✗ No concurrent suspicious activity
   - Authorized activity indicators:
     ✓ Scheduled timing (maintenance window 00:00-04:00 UTC)
     ✓ Authorized credentials (public key in key registry)
     ✓ Known business function (automated backup operation)
     ✓ 90-day established baseline (not new behavior)

5. **Business Context:**
   - IT Operations confirmed: Daily backup schedule at 02:00 UTC
   - Change management: No recent changes to backup infrastructure
   - Asset ownership: Both systems owned by IT Ops team

**Independent Risk Assessment:**
- Alert Severity: Critical (Claroty's automated classification)
- Actual Severity: Low (authorized administrative activity)
- Alert Classification: APT lateral movement (rule-based detection)
- Actual Classification: Scheduled backup (confirmed with asset owners)
- APT Indicators: 0/5 APT tactics detected
- Authorized Activity Indicators: 4/4 present

**Disposition:** False Positive (Confidence: High)

**Analysis:**
While Claroty classified this as Critical severity APT activity, independent investigation reveals:
- Activity matches authorized backup operation (verified with IT Ops)
- 90-day historical pattern contradicts "APT" hypothesis (APTs don't run daily at same time for 3 months)
- No APT tactics, techniques, or procedures detected
- All indicators point to legitimate, scheduled administrative activity

Alert rule APT_Lateral_Movement_Pattern_V3 appears overly sensitive to SSH connections in control environment. Recommend tuning to exclude authorized jump server traffic during maintenance windows.

**Escalation:** No escalation required (authorized activity)

**Next Actions:**
1. Tune Claroty rule APT_Lateral_Movement_Pattern_V3 to exclude jump-server-01 → backup-file-server during 00:00-04:00 UTC
2. Document tuning rationale in alert management system
3. Review other alerts from this rule for similar false positives
```

**No Automation Bias:**
✓ Alert claims treated as hypotheses, not conclusions
✓ Independent evidence collection performed
✓ Alert severity independently assessed (Critical → Low after context review)
✓ Alert classification verified (APT → Scheduled backup after investigation)
✓ APT indicators specifically checked (0/5 detected)
✓ Business context integrated
✓ Analyst reached opposite conclusion from alert system
✓ **Analyst demonstrated critical thinking, not blind acceptance of automation**

---

### 6. Alternative Hypotheses

**Definition:** Considering multiple explanations for observed behavior, not just the initial assumption.

**Event Investigation Context:**
- Initial hypothesis: "This is lateral movement"
- Alternative hypotheses: "This is scheduled maintenance", "This is authorized backup", "This is vulnerability scanning"

**Why Alternatives Matter:**
- Prevents confirmation bias (forces consideration of other explanations)
- Improves accuracy (best explanation emerges from comparison)
- Demonstrates rigor (shows investigation considered multiple scenarios)

**Minimum Requirement:** At least 2 alternative scenarios evaluated

**Detection Questions:**
- Were multiple competing explanations considered?
- Were alternatives explicitly stated and evaluated?
- Was reasoning provided for accepting/rejecting each alternative?
- Did investigation actively seek evidence to distinguish between alternatives?

**Example - Alternatives Considered:**

```
**Initial Hypothesis:** SSH connection represents unauthorized lateral movement attack

**Alternative Hypotheses Evaluated:**

1. **Unauthorized lateral movement (initial hypothesis)**
   - Evidence for: SSH connection to file server, non-business hours
   - Evidence against: Source is authorized jump server, 90-day daily pattern, authorized SSH key
   - Evaluation: REJECTED (evidence strongly contradicts unauthorized access)

2. **Authorized backup operation (alternative)**
   - Evidence for: Daily 02:00 UTC pattern (87 occurrences), authorized SSH key, IT Ops confirmed schedule
   - Evidence against: None (all evidence supports this hypothesis)
   - Evaluation: ACCEPTED (best explanation given evidence)

3. **Jump server compromise enabling lateral movement (alternative)**
   - Evidence for: High-value target (jump server provides access to many systems)
   - Evidence against: No IOCs on jump server, SSH key matches authorized registry, pattern predates recent activity
   - Evaluation: REJECTED (no compromise indicators detected)

**Conclusion:** Alternative hypothesis #2 (authorized backup) best explains all evidence.
```

✓ 3 alternatives considered
✓ Evidence for/against each explicitly stated
✓ Clear reasoning for acceptance/rejection
✓ Best explanation selected based on evidence

---

## Bias Severity Classification

**No Bias (6/6 passed):**
- Investigation demonstrates objective, evidence-based analysis
- Multiple perspectives considered
- Conclusions independent of automated assessments
- Quality: Excellent

**Minor Bias (4-5/6 passed):**
- One bias type detected with limited impact on conclusion
- Disposition likely still correct despite bias
- Example: Minor anchoring to alert severity but evidence-based disposition
- Quality: Good, recommend debiasing techniques

**Moderate Bias (2-3/6 passed):**
- Multiple bias types detected OR single severe bias
- Disposition questionable due to bias influence
- Example: Confirmation bias + automation bias leading to unsupported TP classification
- Quality: Needs Improvement, disposition may require revision

**Severe Bias (0-1/6 passed):**
- Multiple severe biases detected
- Disposition likely incorrect due to bias
- Investigation lacks objectivity and rigor
- Quality: Inadequate, investigation must be redone

---

## Debiasing Strategies

**Counter Confirmation Bias:**
- Devil's advocate: Actively argue against your initial hypothesis
- Seek disconfirming evidence: "What evidence would prove me wrong?"
- Pre-mortem: "If this disposition is wrong, why would it be wrong?"

**Counter Anchoring Bias:**
- Multi-factor assessment: Evaluate severity, criticality, impact independently
- Blind assessment: Assess evidence before seeing alert classification
- Question the anchor: "Is this alert severity accurate for this specific context?"

**Counter Availability Bias:**
- Base rate reasoning: "What % of similar alerts are actually malicious?"
- Statistical data: Use SIEM metrics, historical FP rates
- Separate recent events: "Is this alert related to recent incident, or am I assuming similarity?"

**Counter Recency Bias:**
- Historical context: Always review 30/60/90 day patterns
- Trend analysis: Is recent behavior consistent with long-term baseline?
- Time-independent assessment: Evaluate based on all available history, not just recent

**Counter Automation Bias:**
- Treat alerts as hypotheses: Alert says X, does evidence confirm X?
- Independent verification: Collect evidence beyond alert metadata
- Question automation: "Could the alert be wrong? Under what conditions?"
- Context integration: Alert can't know about scheduled maintenance, authorized changes

**General Debiasing:**
- Peer review: Second analyst reviews disposition (catches individual biases)
- Checklist adherence: Follow systematic process (reduces cognitive shortcuts)
- Document reasoning: Explicit logic forces critical thinking
- Awareness: Simply knowing biases exist reduces their influence

---

## Weighting Rationale

**Why 5% (Low Weight)?**

Bias detection is valuable but subjective and difficult to measure objectively. Unlike technical accuracy (factually right/wrong) or completeness (present/missing), bias detection requires inferring analyst mental state from documentation.

**Prioritization:**
- **Substance** (Completeness, Accuracy, Disposition, Context, Methodology) = 90% combined
- **Bias Detection** = 5% (catches systematic reasoning errors)
- **Documentation** = 5% (communication quality)

**When Bias Detection Becomes Critical:**
- High-stakes decisions (critical assets, potential breaches, escalation decisions)
- Pattern of repeated errors (analyst consistently reaches wrong conclusions)
- Controversial dispositions (internal disagreement on TP vs. FP)
- Audit or compliance review (demonstrating objective analysis)

**Note:** While weighted at only 5%, severe bias can invalidate an otherwise complete investigation. Use this checklist to detect systematic reasoning failures that other dimensions might miss.

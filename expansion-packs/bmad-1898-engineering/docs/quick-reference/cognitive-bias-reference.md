# Cognitive Bias Quick Reference
**Recognizing and Mitigating Bias in Security Investigations**

---

## Overview

Cognitive biases are systematic errors in thinking that affect decisions and judgments. In security investigations, biases can lead to:
- Incorrect disposition determinations (TP/FP/BTP)
- Missed attack indicators
- False confidence in conclusions
- Poor quality investigations

**Solution:** Awareness + structured methodology + peer review

---

## The Four Critical Biases

### 1. Automation Bias

**Definition:** Over-trusting automated systems (IDS/SIEM alerts, ML models) without independent verification

**Manifestation in Security:**
- Assuming alert is correct because IDS signature triggered
- Not validating alert logic or signature accuracy
- Blindly trusting ML model disposition predictions
- Skipping evidence collection ("the system already analyzed it")

**Real-World Example:**
```
Alert: "Malware C2 Communication Detected"
Source: 192.168.1.50
Destination: cdn.cloudflare.com (ML model: 95% confidence malicious)

❌ Automation Bias Response:
"ML model says 95% malicious → Must be TP"

✅ Correct Response:
1. Verify: What triggered the alert? (DNS query pattern)
2. Investigate: Is destination actually malicious? (NO - legitimate CDN)
3. Root cause: ML model trained on older data, CDN domain flagged incorrectly
4. Disposition: FALSE POSITIVE (signature needs updating)
```

**Mitigation Strategies:**
- ✅ Always verify alert signature/logic independently
- ✅ Treat automated dispositions as *suggestions*, not *conclusions*
- ✅ Ask: "What evidence supports this alert beyond the system saying so?"
- ✅ Perform PCAP analysis to validate traffic
- ✅ Research destination IPs/domains independently (VirusTotal, threat intel)

---

### 2. Anchoring Bias

**Definition:** Over-relying on the first piece of information encountered (the "anchor")

**Manifestation in Security:**
- Fixating on alert severity (High → must be TP)
- Focusing only on first evidence source (ignoring contradictory data)
- Letting initial hypothesis dominate investigation
- Not updating assessment when new evidence emerges

**Real-World Example:**
```
Alert: "SSH Brute Force Attack" (CRITICAL severity)
Source: 10.50.100.20
Failed login attempts: 25

❌ Anchoring Bias Response:
"CRITICAL severity → Must be serious attack → TP"
(Stops investigation, doesn't check source IP context)

✅ Correct Response:
1. Initial assessment: Possible brute force (hypothesis)
2. Investigate source: 10.50.100.20 = BACKUP-SERVER-01
3. Check context: Scheduled backup failed (credential expiry)
4. Alternative hypothesis: Service account password expired (NOT attack)
5. Disposition: BENIGN TRUE POSITIVE (legitimate service, password issue)
```

**Mitigation Strategies:**
- ✅ Generate multiple hypotheses at the start
- ✅ Actively seek contradictory evidence
- ✅ Re-evaluate initial assumptions with each new evidence piece
- ✅ Use checklist-driven investigation (forces comprehensive review)
- ✅ Ask: "What evidence would disprove my initial hypothesis?"

---

### 3. Confirmation Bias

**Definition:** Seeking/interpreting evidence that confirms pre-existing beliefs while ignoring contradictory evidence

**Manifestation in Security:**
- Collecting only evidence that supports initial disposition
- Dismissing evidence that contradicts hypothesis
- Interpreting ambiguous data to fit preferred conclusion
- Stopping investigation once "enough" confirming evidence found

**Real-World Example:**
```
Alert: "Unauthorized Port Scan Detected"
Source: 172.16.10.5
Destination: Multiple internal IPs (ports 22, 80, 443)

❌ Confirmation Bias Response:
Initial belief: "External attacker reconnaissance"
Evidence collected:
- Port scan detected ✅ (confirms)
- Multiple targets ✅ (confirms)
- Stopped here (ignored source IP investigation)
Disposition: TRUE POSITIVE (WRONG)

✅ Correct Response:
1. Initial hypothesis: Possible reconnaissance
2. Evidence for TP: Port scan pattern, multiple targets
3. Evidence against TP (actively sought):
   - Source IP: 172.16.10.5 = SECURITY-SCANNER-01
   - Check change calendar: Weekly vulnerability scan scheduled
   - Change ticket: CHG-7890 (authorized security scan)
4. Alternative hypothesis: Authorized security scan
5. Disposition: BENIGN TRUE POSITIVE (authorized activity)
```

**Mitigation Strategies:**
- ✅ Actively seek evidence that *contradicts* your hypothesis
- ✅ Create "evidence against" section in investigation notes
- ✅ Ask: "What would make this a FP/BTP instead of TP?"
- ✅ Have peer review your evidence selection (catches one-sided collection)
- ✅ Use hypothesis testing framework (test multiple explanations equally)

---

### 4. Availability Bias

**Definition:** Over-weighting recent, memorable, or emotionally salient events

**Manifestation in Security:**
- Assuming current alert is similar to recent high-profile incident
- Over-estimating likelihood of rare attacks (because recently discussed)
- Under-estimating common issues (because less memorable)
- Letting recent training/news influence disposition

**Real-World Example:**
```
Context: Organization suffered ransomware attack last week (high-profile)

Alert: "Suspicious PowerShell Execution"
Source: 192.168.5.10 (WORKSTATION-45)
Command: powershell.exe -ExecutionPolicy Bypass

❌ Availability Bias Response:
"We just had ransomware last week → PowerShell is ransomware indicator → TP"
(Jumps to conclusion based on recent incident, not current evidence)

✅ Correct Response:
1. Acknowledge recent incident (but don't let it dominate)
2. Investigate current alert independently:
   - PowerShell command: What script executed?
   - User context: IT admin running patch deployment script
   - Change ticket: CHG-5555 (authorized patching)
   - Historical: Same command runs monthly (patching schedule)
3. Disposition: BENIGN TRUE POSITIVE (authorized admin activity)
```

**Mitigation Strategies:**
- ✅ Acknowledge recent events, then consciously set aside
- ✅ Use data-driven analysis (statistics, baselines) not memory
- ✅ Compare to historical patterns, not recent incidents
- ✅ Ask: "Am I treating this differently because of recent events?"
- ✅ Use structured checklists (prevents skipping common issues)

---

## Bias Detection Checklist

Use this during investigation and review:

### During Investigation (Analysts)

- [ ] **Automation Bias Check:** Did I verify alert logic independently, or just trust the system?
- [ ] **Anchoring Bias Check:** Am I fixated on the first piece of evidence? Have I considered all evidence equally?
- [ ] **Confirmation Bias Check:** Have I actively sought evidence that *contradicts* my hypothesis?
- [ ] **Availability Bias Check:** Am I comparing to recent incidents instead of historical data?

### During Review (Reviewers)

- [ ] **Analyst's Evidence:** Is evidence collection one-sided? (only supports one disposition)
- [ ] **Alternative Hypotheses:** Did analyst consider multiple explanations?
- [ ] **Contradictory Evidence:** Is there evidence that contradicts the disposition?
- [ ] **Alert Verification:** Did analyst verify alert logic, or assume correctness?
- [ ] **Recent Incident Influence:** Is disposition influenced by recent high-profile events?

---

## Bias Mitigation Techniques

### 1. Hypothesis-Driven Investigation

**Process:**
1. Generate 2-3 competing hypotheses at start
2. Identify evidence that would support/contradict each
3. Collect evidence for ALL hypotheses (not just preferred one)
4. Evaluate which hypothesis best fits ALL evidence

**Example:**
```
Alert: "Abnormal Database Query Volume"

Hypothesis 1: Data exfiltration attack (TP)
- Evidence for: High query volume, unusual time (2 AM)
- Evidence against: [actively seek this]

Hypothesis 2: Legitimate batch process (BTP)
- Evidence for: Scheduled job, service account
- Evidence against: [actively seek this]

Hypothesis 3: Database performance issue (FP)
- Evidence for: Query timeout retries
- Evidence against: [actively seek this]

Result: Collect evidence for ALL three, then decide
```

### 2. Pre-Mortem Analysis

**Process:**
1. Before finalizing disposition, imagine you were wrong
2. Ask: "What evidence did I miss that would prove me wrong?"
3. Actively search for that evidence
4. Re-evaluate disposition

**Example:**
```
Draft Disposition: FALSE POSITIVE (alert signature error)

Pre-Mortem: "Imagine this is actually a TRUE POSITIVE..."
- What evidence would I have missed?
  - Host-level logs (didn't check)
  - Firewall logs showing outbound C2 (didn't check)
  - Historical similar alerts marked TP (didn't check)

Action: Check these sources BEFORE finalizing FP disposition
```

### 3. Devil's Advocate

**Process:**
1. After reaching disposition, intentionally argue the opposite
2. Find strongest evidence for alternative disposition
3. If alternative is compelling, re-investigate
4. If original holds, document why alternative was rejected

**Example:**
```
Disposition: BENIGN TRUE POSITIVE (authorized scan)

Devil's Advocate: "What if this is actually a TRUE POSITIVE attack?"
- Attacker could mimic authorized scanner IP (spoofing)
- Scan pattern could be reconnaissance disguised as vuln scan
- Change ticket could be forged or backdated

Verification:
- Check network logs: Source MAC address matches scanner (not spoofed)
- Scan signature: Matches Nessus fingerprint (not generic scan)
- Change ticket: Created 2 days before scan (not backdated)

Conclusion: BTP confirmed, attack hypothesis rejected
```

### 4. Checklist-Driven Investigation

**Process:**
1. Use standardized checklist for ALL investigations (5 stages)
2. Cannot skip steps (forces comprehensive review)
3. Checklist prompts evidence from multiple sources
4. Reduces bias by ensuring systematic approach

**Example:**
```
Stage 1 Checklist:
☑ Alert metadata collected
☑ Network identifiers documented
☑ Asset criticality assessed
☑ Alert frequency checked

(Cannot proceed to Stage 2 until all Stage 1 items complete)
```

---

## Common Bias Patterns in Dispositions

| Disposition | Common Bias | Example |
|-------------|-------------|---------|
| **TP** | Availability Bias | "Recent ransomware → all PowerShell alerts are TP" |
| **TP** | Confirmation Bias | "External IP → must be attack" (ignores VPN gateway) |
| **FP** | Automation Bias | "IDS alerts often false → this must be FP too" |
| **FP** | Anchoring Bias | "Low severity → can't be serious → FP" |
| **BTP** | Confirmation Bias | "Found change ticket → stopped investigating" (ticket could be invalid) |
| **BTP** | Availability Bias | "Similar alert last week was BTP → this is too" |

---

## Bias Mitigation Summary

| Bias | Key Question | Mitigation Action |
|------|--------------|-------------------|
| **Automation** | "Did I verify independently?" | Check alert logic, PCAP analysis |
| **Anchoring** | "Am I fixated on first evidence?" | Generate multiple hypotheses |
| **Confirmation** | "Did I seek contradictory evidence?" | Create "evidence against" section |
| **Availability** | "Am I influenced by recent events?" | Use historical data, not memory |

---

## Bias Training Exercises

### Exercise 1: Identify the Bias

**Scenario:** Analyst marks alert as TP because "we had a similar attack last month"
**Bias:** Availability Bias
**Mitigation:** Investigate current alert independently using evidence, not recent memory

### Exercise 2: Identify the Bias

**Scenario:** Analyst stops investigation after finding one piece of supporting evidence
**Bias:** Confirmation Bias
**Mitigation:** Actively seek contradictory evidence before finalizing disposition

### Exercise 3: Identify the Bias

**Scenario:** Analyst trusts ML model disposition (95% confidence TP) without verification
**Bias:** Automation Bias
**Mitigation:** Verify alert logic and evidence independently

---

## Reviewer Bias Detection

**When reviewing, look for these bias indicators:**

| Indicator | Possible Bias | Review Action |
|-----------|---------------|---------------|
| Only evidence supporting one disposition | Confirmation Bias | Request contradictory evidence search |
| No alert logic verification | Automation Bias | Request PCAP/signature analysis |
| Disposition references "recent incident" | Availability Bias | Request data-driven comparison |
| First evidence heavily emphasized | Anchoring Bias | Request equal weight for all evidence |
| Single hypothesis tested | Confirmation Bias | Request alternative hypothesis testing |

---

**Need Help?** See: `docs/troubleshooting-faq-best-practices.md`
**Training:** See: `docs/training/event-investigation-training.md` (Module 6)
**Deep Dive:** See: `docs/workflows/event-investigation-workflow-deep-dive.md`

# Cognitive Bias Patterns in Security Analysis

## Introduction

Cognitive biases are systematic errors in thinking that affect judgments and decisions. In security analysis, biases can lead to:
- Incorrect priority assessments
- Missed critical vulnerabilities
- Over-reaction to low-risk issues
- Inconsistent analysis quality

This guide helps security analysts recognize and mitigate 5 common biases.

---

## 1. Confirmation Bias

### Definition
Seeking, interpreting, and remembering information that confirms pre-existing beliefs while dismissing contradicting evidence.

### Psychology
Our brains naturally seek information that supports what we already think. Once we form an initial hypothesis ("This is critical"), we subconsciously look for evidence supporting that conclusion and ignore evidence against it.

### Security Analysis Examples

**Example 1: CVSS-Only Assessment**
❌ **Biased Analysis:**
"The CVSS score is 9.8 (Critical), so this is definitely high priority. I found articles about similar vulnerabilities being exploited, so this confirms it's critical."
- Ignores: EPSS 0.05 (very low exploitation probability)
- Ignores: KEV Not Listed (no active exploitation observed)
- Ignores: No public exploits available

✅ **Objective Analysis:**
"CVSS is 9.8 (Critical severity), but EPSS is 0.05 (very low exploitation probability), KEV Not Listed, and no public exploits found. While severity is high, exploitability is low. Priority: P3 (Medium) with monitoring for exploit developments."

**Example 2: Cherry-Picking Sources**
❌ **Biased Analysis:**
"I found 3 security blogs saying this is critical, so it must be."
- Ignores: Official NVD assessment rates it Medium
- Ignores: Vendor advisory says low risk
- Selected only sources confirming initial belief

✅ **Objective Analysis:**
"Security blogs rate this as critical, but official NVD and vendor advisory rate it Medium/Low. Prioritize authoritative sources (NVD, vendor) over secondary sources (blogs). Further investigation needed."

### Impact on Vulnerability Assessment
- Over-prioritization of some vulnerabilities
- Under-prioritization of others
- Inconsistent analysis across tickets
- Missed critical factors (EPSS, KEV)

### Debiasing Techniques

**1. Devil's Advocate:**
After initial assessment, actively argue the opposite conclusion.
- "Why might this be lower priority than I think?"
- "What evidence contradicts my assessment?"

**2. Pre-Mortem Analysis:**
"If this priority assessment turns out to be wrong, what would be the reason?"

**3. Explicitly Seek Contradicting Evidence:**
- "What data suggests this is NOT as critical?"
- "Are there mitigating factors I'm overlooking?"

**4. Use Structured Checklists:**
BMAD-1898 checklists force evaluation of all factors, not just confirming ones.

---

## 2. Anchoring Bias

### Definition
Over-relying on the first piece of information encountered (the "anchor") when making decisions.

### Psychology
The first number or fact we see disproportionately influences our subsequent judgments, even when other equally important information is presented.

### Security Analysis Examples

**Example 1: CVSS Anchoring**
❌ **Biased Analysis:**
"CVSS is 8.5 (High), so priority should be P2 (High)."
- Anchored on CVSS score
- Ignores EPSS 0.10 (low exploitation probability)
- Ignores Internal system with no internet exposure
- Ignores Strong WAF compensating control

✅ **Objective Analysis:**
"CVSS is 8.5 (High), but considering EPSS 0.10, internal exposure, and effective WAF, priority is P4 (Low). All factors weighted equally."

**Example 2: Initial Severity Report Anchoring**
❌ **Biased Analysis:**
"Scanner initially flagged this as Critical, so I'm starting with that assumption."
- Anchored on scanner's initial classification
- Fails to independently assess using CVSS + EPSS + KEV
- Scanner may have false positive

✅ **Objective Analysis:**
"Scanner flagged as Critical. Let me independently verify: CVSS 6.5 (Medium), EPSS 0.20 (low), KEV Not Listed. Scanner may have over-estimated. Priority: P3."

### Impact on Vulnerability Assessment
- Priority matching CVSS severity exactly
- Ignoring mitigating factors
- Inconsistent priority framework application

### Debiasing Techniques

**1. Blind Assessment:**
Assess EPSS, KEV, ACR, Exposure independently before seeing CVSS.

**2. Multi-Factor Checklist:**
Evaluate all factors (CVSS, EPSS, KEV, ACR, Exposure) with equal attention.

**3. Algorithmic Priority Calculation:**
Use BMAD-1898 priority algorithm to weight all factors mathematically.

**4. Question the Anchor:**
"Why did I start with this number? Are other factors equally important?"

---

## 3. Availability Heuristic

### Definition
Overestimating the likelihood or importance of events that are easily recalled, often because they are recent, emotionally impactful, or widely publicized.

### Psychology
Our brains assess risk based on how easily we can recall examples. Recent high-profile breaches (Log4Shell, SolarWinds) make similar vulnerabilities feel more dangerous than data suggests.

### Security Analysis Examples

**Example 1: Log4Shell Influence**
❌ **Biased Analysis:**
"This is an Apache library vulnerability. It could be the next Log4Shell! Priority P1."
- CVE-2024-XXXX: Apache Commons Text DoS (CVSS 5.3, Local attack vector)
- Log4Shell: Apache Log4j RCE (CVSS 10.0, Remote)
- No similarity beyond "Apache"

✅ **Objective Analysis:**
"Apache Commons Text DoS (CVSS 5.3, local vector). Unlike Log4Shell RCE, this requires local access and causes DoS, not RCE. EPSS 0.08. Priority: P4."

**Example 2: Recent Breach Over-Reaction**
❌ **Biased Analysis:**
"We just had a breach involving SQL injection last month. This SQL injection CVE is definitely critical."
- Influenced by recent breach emotional impact
- Current CVE: CVSS 4.5, requires authentication, low privilege escalation
- Not comparable to previous breach (CVSS 9.8, unauthenticated RCE)

✅ **Objective Analysis:**
"SQL injection (CVSS 4.5), requires auth, low priv escalation. Previous breach was CVSS 9.8 unauthenticated RCE. These are different severity levels. Priority: P3."

### Impact on Vulnerability Assessment
- Over-prioritizing vulnerabilities similar to recent news
- Under-prioritizing persistent threats
- Emotional vs. data-driven decisions

### Debiasing Techniques

**1. Base Rate Awareness:**
Check EPSS for actual exploitation probability, not memorable examples.

**2. Recent Events Log:**
Maintain awareness of current bias triggers (Log4Shell, SolarWinds, recent breaches).
Ask: "Am I influenced by recent news rather than data?"

**3. Statistical Reasoning:**
"What does the data say?" vs. "What do I remember?"

**4. Comparison Check:**
"Is this truly comparable to the high-profile case I'm thinking of?"

---

## 4. Overconfidence Bias

### Definition
Overestimating the accuracy of one's assessments and failing to acknowledge uncertainty or incomplete information.

### Psychology
We tend to be more confident in our judgments than accuracy warrants. Experts are particularly susceptible because expertise increases confidence faster than accuracy.

### Security Analysis Examples

**Example 1: Definitive Statements Without Evidence**
❌ **Biased Analysis:**
"This vulnerability is definitely being actively exploited in the wild. Priority P1."
- No KEV listing
- No EPSS data (new CVE)
- No exploit intelligence cited
- Stated as certainty despite lack of evidence

✅ **Objective Analysis:**
"⚠️ Exploit status uncertain: No KEV listing, EPSS not yet available (new CVE), no confirmed exploit reports found. Recommend conservative P2 priority until more intelligence available. Will re-assess in 48 hours."

**Example 2: Ignoring Information Gaps**
❌ **Biased Analysis:**
"I've done the research. This is definitely P2."
- EPSS data unavailable (didn't mention)
- Vendor advisory not yet published (didn't mention)
- Didn't acknowledge uncertainty

✅ **Objective Analysis:**
"Based on CVSS 8.0 and system criticality, preliminary assessment is P2. Note: EPSS not yet available, vendor advisory pending. Will update assessment when additional data available."

### Impact on Vulnerability Assessment
- Missing critical information
- No acknowledgment of uncertainty
- Overconfident incorrect priority assessments

### Debiasing Techniques

**1. Confidence Calibration:**
"How certain am I (0-100%)? What could I be wrong about?"

**2. Uncertainty Acknowledgment:**
Explicitly state information gaps: "EPSS not yet available", "Exploit status unconfirmed"

**3. Verification Requirement:**
Fact-check critical claims with authoritative sources before stating as fact.

**4. Hedging Language:**
"Based on available evidence...", "Preliminary assessment...", "Subject to update..."

---

## 5. Recency Bias

### Definition
Giving disproportionate weight to recent events or information while undervaluing historical patterns or persistent risks.

### Psychology
Recent information is more vivid and accessible in memory, leading us to overweight it compared to older (but potentially more important) information.

### Security Analysis Examples

**Example 1: New CVE Over-Prioritization**
❌ **Biased Analysis:**
"CVE-2024-XXXX was disclosed yesterday. High priority due to recency."
- CVE-2024-XXXX: CVSS 6.5, EPSS 0.10, No exploits
- CVE-2022-YYYY (older): CVSS 8.0, KEV Listed, Active Exploitation, EPSS 0.90
- Prioritized new CVE over older, more dangerous CVE

✅ **Objective Analysis:**
"CVE-2024-XXXX is recent (CVSS 6.5, EPSS 0.10, no exploits). Priority: P3. Note: Older CVE-2022-YYYY (KEV Listed, EPSS 0.90, active exploitation) remains higher priority (P1) despite age."

**Example 2: Dismissing Older CVEs**
❌ **Biased Analysis:**
"CVE-2022-1234 is from 2022, so it's probably not a big deal anymore."
- Assumption: Old = less dangerous
- Reality: CVE-2022-1234 added to KEV in 2024 (recent active exploitation)
- Older CVEs often have higher EPSS (more time for exploits to develop)

✅ **Objective Analysis:**
"CVE-2022-1234 (2022 disclosure) added to CISA KEV in 2024, indicating recent active exploitation. EPSS 0.88. Age does not reduce risk. Priority: P1."

### Impact on Vulnerability Assessment
- New CVEs over-prioritized
- Persistent threats under-prioritized
- Poor resource allocation

### Debiasing Techniques

**1. Historical Context Review:**
Check older CVEs in same product. Are they resolved?

**2. Trend Analysis:**
"Are new CVEs actually more dangerous, or just more memorable?"

**3. Age-Independent Assessment:**
Assess risk factors (CVSS, EPSS, KEV) regardless of CVE age.

**4. Persistent Threat Monitoring:**
Maintain list of older but still-dangerous CVEs for comparison.

---

## Self-Assessment Guide

### How to Assess Your Bias Patterns

Review your last 10 vulnerability enrichments and ask:

**Confirmation Bias Check:**
- [ ] Did I consider evidence contradicting my initial assessment?
- [ ] Did I seek out opposing viewpoints?
- [ ] Did I acknowledge limitations or uncertainties?

**Anchoring Bias Check:**
- [ ] Did my priority exactly match CVSS severity?
- [ ] Did I weight all factors (CVSS, EPSS, KEV, ACR, Exposure) equally?
- [ ] Did I question my initial impression?

**Availability Heuristic Check:**
- [ ] Did I reference recent breaches or news events?
- [ ] Did I compare to memorable incidents without data?
- [ ] Did I rely on EPSS/KEV data vs. recollection?

**Overconfidence Check:**
- [ ] Did I acknowledge information gaps or uncertainties?
- [ ] Did I use hedging language when appropriate?
- [ ] Did I verify critical claims against authoritative sources?

**Recency Bias Check:**
- [ ] Did I prioritize new CVEs over older CVEs without rationale?
- [ ] Did I consider persistent threats alongside new ones?
- [ ] Did I assess CVE age-independently?

### Scoring
- 0-5 Yes answers: High bias risk - Focus on debiasing techniques
- 6-10 Yes answers: Moderate bias awareness - Continue improvement
- 11-15 Yes answers: Good bias mitigation - Maintain practices

### Action Plan
**If High Bias Risk:**
- Use BMAD-1898 checklists for every analysis
- Fact-check critical claims using Perplexity
- Request peer review for all P1/P2 priorities

**If Moderate:**
- Continue checklist use
- Periodic self-assessment
- Peer review for P1/P2

**If Good:**
- Maintain current practices
- Mentor others on bias awareness
- Periodic refresher

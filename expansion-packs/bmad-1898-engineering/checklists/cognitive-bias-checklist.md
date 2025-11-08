# Cognitive Bias Detection Checklist

**Purpose:** Identify cognitive bias patterns in Security Analyst enrichment work to ensure objective, evidence-based vulnerability assessments.

**Usage:** Run this checklist via `execute-checklist` task when reviewing Security Analyst enrichments. Check each bias type systematically.

---

## 1. Confirmation Bias

**Definition:** Seeking or interpreting evidence to confirm pre-existing beliefs while dismissing contradicting evidence.

**Detection Questions:**

- [ ] Does the analysis consider evidence that contradicts the initial severity assessment?
- [ ] Are alternate interpretations or scenarios considered?
- [ ] Does the analysis cherry-pick data supporting high/low severity?
- [ ] Are limitations or uncertainties acknowledged?

**Red Flags:**

- Only citing sources that confirm high severity
- Ignoring low EPSS score when CVSS is high
- Dismissing lack of exploits without investigation
- Overstating exploitability without evidence

**Example:**

❌ **Bad (Confirmation Bias Present):**
"CVSS is 9.8, so this is critical. Active exploitation is likely."
(Ignores EPSS 0.05, KEV Not Listed, No PoC available)

✅ **Good (Balanced Analysis):**
"CVSS is 9.8 (critical severity), but EPSS is 0.05 (very low exploitation probability), KEV Not Listed, and no public exploits found. Priority: P3 due to low exploitability."

---

## 2. Anchoring Bias

**Definition:** Over-relying on the first piece of information encountered (the "anchor") when making decisions.

**Detection Questions:**

- [ ] Is priority based on multiple factors, not just CVSS?
- [ ] Does analysis consider EPSS, KEV, ACR, and Exposure equally?
- [ ] Is CVSS score allowed to dominate priority assessment?
- [ ] Are mitigating factors given appropriate weight?

**Red Flags:**

- Priority matches CVSS severity exactly (High CVSS → High Priority) without considering other factors
- Ignoring low EPSS or lack of KEV listing
- Dismissing effective compensating controls

**Example:**

❌ **Bad (Anchoring Bias Present):**
"CVSS 8.5 (High) → Priority P2 (High)"
(Ignores low EPSS, internal system, no exploits, effective WAF)

✅ **Good (Multi-Factor Assessment):**
"CVSS 8.5 (High), but EPSS 0.15 (low), Internal system, No exploits, WAF provides strong compensating control. Priority: P4."

---

## 3. Availability Heuristic

**Definition:** Overestimating the likelihood or importance of events that are easily recalled, often because they are recent or emotionally impactful.

**Detection Questions:**

- [ ] Is the analysis influenced by recent high-profile breaches?
- [ ] Does the enrichment mention recent incidents without relevance?
- [ ] Is risk assessment data-driven (EPSS, KEV) vs. emotion-driven?
- [ ] Are rare but memorable events given disproportionate weight?

**Red Flags:**

- Referencing Log4Shell or SolarWinds without connection to current CVE
- Elevating priority because vulnerability "sounds like" recent breach
- Using phrases like "could be the next Log4Shell"

**Example:**

❌ **Bad (Availability Heuristic Present):**
"This is an Apache vulnerability like Log4Shell. Could be catastrophic."
(CVE-2024-XXXX is a low-severity DoS, unrelated to Log4Shell RCE)

✅ **Good (Data-Driven Assessment):**
"Apache Commons DoS (CVSS 5.3). Unlike Log4Shell RCE, this is a denial-of-service with local attack vector. Priority: P4."

---

## 4. Overconfidence Bias

**Definition:** Overestimating the accuracy of one's assessments and failing to acknowledge uncertainty or incomplete information.

**Detection Questions:**

- [ ] Does analysis acknowledge missing or uncertain information?
- [ ] Are absolute statements avoided when data is incomplete?
- [ ] Is uncertainty explicitly noted (e.g., "EPSS not yet available")?
- [ ] Are recommendations appropriately hedged when information limited?

**Red Flags:**

- Definitive statements without sources ("This is definitely exploited in the wild")
- No mention of information gaps
- Ignoring "Insufficient Information" from Perplexity

**Example:**

❌ **Bad (Overconfidence Bias Present):**
"This vulnerability is actively exploited. Priority: P1."
(No KEV listing, no EPSS, no exploit evidence cited)

✅ **Good (Uncertainty Acknowledged):**
"⚠️ Exploit status uncertain: No KEV listing, EPSS not yet available (new CVE). Recommend conservative P2 priority until more intel available."

---

## 5. Recency Bias

**Definition:** Giving disproportionate weight to recent events or information while undervaluing historical patterns or persistent risks.

**Detection Questions:**

- [ ] Is recent CVE disclosure date affecting priority without rationale?
- [ ] Are older CVEs dismissed as "too old" despite ongoing risk?
- [ ] Is priority inflated simply because CVE is new?
- [ ] Are persistent vulnerabilities given appropriate attention?

**Red Flags:**

- Prioritizing new CVE (2024) over older CVE (2022) with higher EPSS/KEV
- Assuming new = more dangerous
- Ignoring that old vulnerabilities often have higher exploitation rates

**Example:**

❌ **Bad (Recency Bias Present):**
"CVE-2024-XXXX disclosed yesterday. High priority due to recency."
(CVSS 6.5, EPSS 0.10, No exploits vs. older CVE-2022-YYYY: CVSS 8.0, KEV Listed, Active Exploitation)

✅ **Good (Age-Independent Assessment):**
"CVE-2024-XXXX is recent but CVSS 6.5, EPSS 0.10, no exploits. Priority: P3. Note: Older CVE-2022-YYYY (KEV Listed, active exploitation) remains higher priority (P1)."

---

## Debiasing Strategies

**Purpose:** Provide corrective techniques to mitigate detected biases in future analysis.

### General Debiasing Approach

1. **Awareness:** Recognize bias exists
2. **Systematic Process:** Follow checklist, don't skip steps
3. **Consider Alternatives:** Actively seek contradicting evidence
4. **Quantitative Data:** Rely on CVSS, EPSS, KEV scores vs. intuition
5. **Peer Review:** Second opinion reduces individual bias

### Specific Mitigation Strategies

#### Counter Confirmation Bias

✅ **Devil's Advocate:** Actively argue for opposite conclusion
✅ **Pre-Mortem:** "If this assessment is wrong, why would it be wrong?"
✅ **Contradicting Evidence:** Explicitly list evidence against your hypothesis

#### Counter Anchoring Bias

✅ **Multi-Factor Checklist:** Evaluate CVSS, EPSS, KEV, ACR, Exposure independently
✅ **Blind Assessment:** Assess EPSS before seeing CVSS
✅ **Weighted Scoring:** Use algorithmic priority calculation

#### Counter Availability Heuristic

✅ **Base Rate Awareness:** Check EPSS for actual exploitation probability
✅ **Recent Events Log:** Maintain awareness of current bias triggers (Log4Shell, etc.)
✅ **Statistical Reasoning:** "What does the data say?" vs. "What do I remember?"

#### Counter Overconfidence

✅ **Confidence Calibration:** "How certain am I? What could I be wrong about?"
✅ **Uncertainty Acknowledgment:** Explicitly state information gaps
✅ **Verification:** Fact-check critical claims with authoritative sources

#### Counter Recency Bias

✅ **Historical Context:** Review older CVEs in same product
✅ **Trend Analysis:** Are new CVEs actually more dangerous?
✅ **Age-Independent Assessment:** Assess risk factors regardless of CVE age

---

## Checklist Execution Summary

**After completing all bias checks above, document findings:**

### Detected Biases

- [ ] List each bias type detected with specific evidence (line numbers, quotes)
- [ ] Provide severity assessment (Minor, Moderate, Severe)

### Recommendations

- [ ] Provide specific debiasing strategy for each detected bias
- [ ] Suggest alternative analysis or additional evidence needed
- [ ] Recommend revision areas in enrichment

### Overall Assessment

- [ ] Cognitive bias level: None / Minor / Moderate / Severe
- [ ] Pass/Fail: Does enrichment require revision due to bias?

---

**References:**

- Story 2.2: Systematic Quality Evaluation (Cognitive Bias Check dimension)
- Story 4.2: Cognitive Bias Patterns Guide (comprehensive knowledge base)
- Story 1.7: Multi-Factor Priority Assessment (P1-P5 priority framework)

# Test: Cognitive Bias Detection Checklist

**Test File:** `tests/checklists/test-cognitive-bias-detection.md`
**Checklist Under Test:** `checklists/cognitive-bias-checklist.md`
**Agent:** Security Reviewer (Riley)

## Testing Framework

**Type:** Manual agent testing with synthetic enrichment scenarios
**Method:** Activate Security Reviewer agent, run checklist against sample enrichments, verify detection accuracy
**Success Criteria:** 5/5 bias types correctly detected with specific evidence and debiasing recommendations

## Test Execution Instructions

1. Activate Security Reviewer agent: `/BMad:agents:security-reviewer`
2. For each test case below, create sample enrichment file
3. Run: `*review-enrichment {ticket-id}` or use `execute-checklist` task with `cognitive-bias-checklist.md`
4. Verify agent detects bias type, cites evidence, and provides debiasing strategy
5. Document results in Test Results section below

---

## Test Case 1: Confirmation Bias Detection

### Test Objective

Verify agent detects cherry-picking of evidence that confirms high severity while ignoring contradicting data.

### Sample Enrichment Document

**Ticket:** VULN-CB-001
**CVE:** CVE-2024-TEST-001

```markdown
# Vulnerability Enrichment: CVE-2024-TEST-001

## CVE Details

- **CVSS Score:** 9.8 (Critical)
- **Description:** Remote code execution in Apache Commons Library

## Risk Assessment

This is a critical vulnerability with CVSS 9.8. Active exploitation is likely given the high severity score and the popularity of Apache Commons. This should be prioritized immediately as a P1.

## Priority Recommendation

**Priority: P1 (Critical)**

The high CVSS score indicates this is an extremely dangerous vulnerability that requires immediate action.
```

### Hidden Contradicting Data (Intentionally Omitted)

- EPSS: 0.05 (very low exploitation probability)
- KEV Status: Not Listed
- Public Exploits: None found
- Compensating Controls: WAF blocks RCE attempts

### Expected Detection Results

**Detected Bias:** Confirmation Bias

**Evidence:**

- Only cites CVSS 9.8 to justify priority
- States "Active exploitation is likely" without evidence
- Ignores low EPSS score (0.05)
- Omits KEV status (Not Listed)
- No mention of absence of public exploits
- Cherry-picks data supporting high severity conclusion

**Debiasing Recommendation:**

- Consider contradicting evidence (low EPSS, no KEV listing)
- Acknowledge limitations and uncertainties
- Use Devil's Advocate technique: "Why might this NOT be P1?"
- Review all available data, not just severity indicators

**Pass Criteria:**

- [ ] Agent identifies Confirmation Bias
- [ ] Agent cites specific evidence from enrichment
- [ ] Agent notes omission of contradicting data (EPSS, KEV, exploits)
- [ ] Agent provides appropriate debiasing strategy

---

## Test Case 2: Anchoring Bias Detection

### Test Objective

Verify agent detects over-reliance on CVSS as the primary decision anchor, ignoring other priority factors.

### Sample Enrichment Document

**Ticket:** VULN-AB-002
**CVE:** CVE-2024-TEST-002

```markdown
# Vulnerability Enrichment: CVE-2024-TEST-002

## CVE Details

- **CVSS Score:** 8.5 (High)
- **Description:** SQL Injection in internal reporting dashboard

## Risk Assessment

CVSS is 8.5 (High severity), therefore this vulnerability requires high priority response.

## Priority Recommendation

**Priority: P2 (High)**

Based on the CVSS High rating, this vulnerability is classified as P2 priority.
```

### Additional Context (Ignored in Enrichment)

- EPSS: 0.15 (low exploitation probability)
- System Type: Internal-only reporting system
- Exposure: No internet exposure, VPN-only access
- Compensating Controls: WAF with SQL injection protection
- Attack Complexity: High (requires authenticated admin access)

### Expected Detection Results

**Detected Bias:** Anchoring Bias

**Evidence:**

- Priority (P2 High) directly matches CVSS severity (8.5 High)
- No consideration of EPSS (0.15 - low)
- Ignores internal-only system (no internet exposure)
- Dismisses effective WAF compensating control
- Single-factor decision making (CVSS as anchor)

**Debiasing Recommendation:**

- Multi-factor assessment: Evaluate CVSS, EPSS, KEV, ACR, Exposure independently
- Blind assessment technique: Assess EPSS before seeing CVSS
- Consider: CVSS 8.5, but EPSS 0.15 (low), Internal system, WAF protection → Priority: P4
- Use weighted scoring algorithm instead of CVSS-only anchoring

**Pass Criteria:**

- [ ] Agent identifies Anchoring Bias
- [ ] Agent notes direct correlation between CVSS and Priority
- [ ] Agent identifies lack of multi-factor consideration
- [ ] Agent recommends multi-factor checklist approach

---

## Test Case 3: Availability Heuristic Detection

### Test Objective

Verify agent detects inappropriate references to recent high-profile vulnerabilities without relevance to current CVE.

### Sample Enrichment Document

**Ticket:** VULN-AH-003
**CVE:** CVE-2024-TEST-003

```markdown
# Vulnerability Enrichment: CVE-2024-TEST-003

## CVE Details

- **CVSS Score:** 5.3 (Medium)
- **Description:** Denial of Service in Apache Commons Text

## Risk Assessment

This is an Apache vulnerability similar to Log4Shell. Given the catastrophic impact of Log4Shell in 2021, we need to treat all Apache vulnerabilities as potentially critical. This could be the next Log4Shell if we're not careful.

## Priority Recommendation

**Priority: P2 (High)**

Elevated priority due to Apache component and similarity to Log4Shell incident.
```

### Actual CVE Characteristics

- **Type:** Denial of Service (DoS), NOT Remote Code Execution
- **Attack Vector:** Local (not network-based like Log4Shell)
- **Component:** Apache Commons Text (completely different from Log4j)
- **EPSS:** 0.08 (very low)
- **KEV:** Not Listed
- **No connection to Log4Shell vulnerability**

### Expected Detection Results

**Detected Bias:** Availability Heuristic

**Evidence:**

- References Log4Shell without any connection to current CVE
- States "similar to Log4Shell" when CVE-2024-TEST-003 is DoS (not RCE)
- Uses emotionally loaded phrase "catastrophic impact"
- Elevates priority based on memorable past event, not current data
- Ignores CVSS 5.3 (Medium) and actual vulnerability characteristics

**Debiasing Recommendation:**

- Base rate awareness: Check EPSS (0.08) for actual exploitation probability
- Statistical reasoning: "What does the data say?" vs. "What do I remember?"
- Correct assessment: "Apache Commons DoS (CVSS 5.3). Unlike Log4Shell RCE, this is denial-of-service with local attack vector. Priority: P4."
- Avoid referencing unrelated high-profile breaches

**Pass Criteria:**

- [ ] Agent identifies Availability Heuristic bias
- [ ] Agent notes inappropriate Log4Shell comparison
- [ ] Agent identifies emotion-driven vs. data-driven assessment
- [ ] Agent recommends focusing on current CVE data, not past incidents

---

## Test Case 4: Overconfidence Bias Detection

### Test Objective

Verify agent detects definitive statements made without supporting evidence or acknowledgment of uncertainty.

### Sample Enrichment Document

**Ticket:** VULN-OC-004
**CVE:** CVE-2024-TEST-004

```markdown
# Vulnerability Enrichment: CVE-2024-TEST-004

## CVE Details

- **CVSS Score:** 7.5 (High)
- **Description:** Authentication bypass in web application framework

## Risk Assessment

This vulnerability is definitely being actively exploited in the wild. Threat actors are certainly targeting this weakness. Exploitation is widespread and confirmed.

## Priority Recommendation

**Priority: P1 (Critical)**

Active exploitation confirmed. Immediate patching required.
```

### Actual Intelligence Status

- **KEV Status:** Not Listed (no CISA confirmation of exploitation)
- **EPSS:** Not yet available (newly disclosed CVE)
- **Public Exploits:** None found in exploit databases
- **Threat Intel:** No reports of active exploitation
- **Sources:** Zero citations or references provided

### Expected Detection Results

**Detected Bias:** Overconfidence Bias

**Evidence:**

- Definitive statement: "definitely being actively exploited" (no evidence)
- Absolute claim: "Exploitation is widespread and confirmed" (no sources)
- States "Active exploitation confirmed" when KEV = Not Listed
- Zero citations or source references
- No acknowledgment of uncertainty or information gaps
- EPSS not yet available for new CVE (uncertainty ignored)

**Debiasing Recommendation:**

- Acknowledge missing information: "⚠️ Exploit status uncertain: No KEV listing, EPSS not yet available (new CVE)"
- Hedge recommendations: "Recommend conservative P2 priority until more intel available"
- Confidence calibration: "How certain am I? What could I be wrong about?"
- Require source citations for factual claims
- Explicitly state information gaps

**Pass Criteria:**

- [ ] Agent identifies Overconfidence Bias
- [ ] Agent notes lack of supporting evidence for definitive claims
- [ ] Agent identifies absence of uncertainty acknowledgment
- [ ] Agent recommends hedging language and explicit gap documentation

---

## Test Case 5: Recency Bias Detection

### Test Objective

Verify agent detects disproportionate prioritization of new CVEs over older CVEs with higher actual risk.

### Sample Enrichment Document

**Ticket:** VULN-RB-005
**CVE:** CVE-2024-TEST-005

```markdown
# Vulnerability Enrichment: CVE-2024-TEST-005

## CVE Details

- **CVSS Score:** 6.5 (Medium)
- **Disclosure Date:** Yesterday (Nov 7, 2024)
- **Description:** Information disclosure in API endpoint

## Risk Assessment

CVE-2024-TEST-005 was disclosed yesterday and is very recent. New vulnerabilities require high priority due to their recency. The fact that this is brand new means we should prioritize it immediately.

## Priority Recommendation

**Priority: P2 (High)**

High priority due to recent disclosure. New CVEs are always more dangerous than older ones.
```

### Comparative Context (Deprioritized Older CVE)

**CVE-2022-OLD-CVE (Same System, Lower Priority)**

- **CVSS:** 8.0 (High)
- **EPSS:** 0.65 (high exploitation probability)
- **KEV Status:** Listed (active exploitation confirmed by CISA)
- **Public Exploits:** Multiple PoCs available
- **Current Priority:** P3 (Medium) - downgraded as "too old"

### Expected Detection Results

**Detected Bias:** Recency Bias

**Evidence:**

- Prioritizes CVE-2024-TEST-005 (CVSS 6.5, EPSS 0.10) as P2
- Deprioritizes CVE-2022-OLD-CVE (CVSS 8.0, KEV Listed, EPSS 0.65) as P3
- States "new means we should prioritize it immediately" (age-based logic)
- Incorrect assumption: "New CVEs are always more dangerous than older ones"
- No risk-based rationale, only recency-based

**Debiasing Recommendation:**

- Age-independent assessment: Assess risk factors regardless of CVE age
- Historical context: Older vulnerabilities often have HIGHER exploitation rates (time for exploit development)
- Correct prioritization: "CVE-2024-TEST-005 is recent but CVSS 6.5, EPSS 0.10, no exploits. Priority: P3. Note: Older CVE-2022-OLD-CVE (KEV Listed, active exploitation) remains higher priority (P1)."
- Trend analysis: Check if newer CVEs are actually more dangerous (often not)

**Pass Criteria:**

- [ ] Agent identifies Recency Bias
- [ ] Agent notes age-based prioritization without risk rationale
- [ ] Agent identifies incorrect deprioritization of older high-risk CVE
- [ ] Agent recommends age-independent risk assessment

---

## Test Results

### Test Execution Log

| Test Case | Bias Type           | Date Tested | Tester | Detection | Evidence Cited | Debiasing Rec | Pass/Fail |
| --------- | ------------------- | ----------- | ------ | --------- | -------------- | ------------- | --------- |
| TC-1      | Confirmation Bias   | TBD         | TBD    | [ ]       | [ ]            | [ ]           | [ ]       |
| TC-2      | Anchoring Bias      | TBD         | TBD    | [ ]       | [ ]            | [ ]           | [ ]       |
| TC-3      | Availability Heur.  | TBD         | TBD    | [ ]       | [ ]            | [ ]           | [ ]       |
| TC-4      | Overconfidence Bias | TBD         | TBD    | [ ]       | [ ]            | [ ]           | [ ]       |
| TC-5      | Recency Bias        | TBD         | TBD    | [ ]       | [ ]            | [ ]           | [ ]       |

### Overall Test Summary

**Total Test Cases:** 5
**Passed:** TBD
**Failed:** TBD
**Pass Rate:** TBD%

**Required Pass Rate:** 100% (5/5 bias types must be correctly detected)

### Notes

- Testing requires Security Reviewer agent activation
- Manual verification of detection quality and accuracy
- Agent must cite specific evidence (quotes, line references)
- Debiasing recommendations must be actionable and specific

---

## Test Maintenance

**Last Updated:** 2025-11-08
**Test File Version:** 1.0
**Checklist Version:** 1.0 (cognitive-bias-checklist.md)

**Future Enhancements:**

- Add real-world inspired test cases from actual enrichments
- Include edge cases (multiple biases in single enrichment)
- Add regression tests as checklist evolves
- Document common false positives/negatives

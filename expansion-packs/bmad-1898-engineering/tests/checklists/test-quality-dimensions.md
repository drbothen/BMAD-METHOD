# Quality Dimension Checklists Test Specification

## Purpose

Test the 8 quality dimension checklists to ensure they correctly evaluate vulnerability enrichments and calculate accurate quality scores.

## Test Environment

- **Agent:** Security Reviewer (Riley)
- **Command:** `*review-enrichment {ticket-id}`
- **Checklists Under Test:** All 8 quality dimension checklists
- **Expected Behavior:** Agent executes all 8 checklists, calculates dimension scores, and generates overall quality score

## Test Data Location

`expansion-packs/bmad-1898-engineering/tests/checklists/test-data/`

## Test Cases

### TC-1: Perfect Enrichment (100% Score Expected)

**Objective:** Verify all checklists pass when enrichment meets all quality criteria

**Test Data:** `perfect-enrichment.md`
**Expected Results:**

- Technical Accuracy: 10/10 items pass → 100%
- Completeness: 12/12 items pass → 100%
- Actionability: 8/8 items pass → 100%
- Contextualization: 10/10 items pass → 100%
- Documentation Quality: 8/8 items pass → 100%
- Attack Mapping Validation: 4/4 items pass → 100%
- Cognitive Bias: 5/5 items pass → 100%
- Source Citation: 5/5 items pass → 100%
- **Overall Score:** 100% (Excellent)

**Verification:**

- [ ] All checklist items marked as passed
- [ ] Each dimension scores 100%
- [ ] Overall score calculated as 100%
- [ ] Quality classification: "Excellent"

---

### TC-2: Missing EPSS (Technical Accuracy Failure)

**Objective:** Verify Technical Accuracy checklist detects missing EPSS data

**Test Data:** `missing-epss-enrichment.md`
**Expected Failure Items:**

- Technical Accuracy: "EPSS score accurate" (FAIL)
- Technical Accuracy: "EPSS percentile provided" (FAIL)

**Expected Results:**

- Technical Accuracy: 8/10 items pass → 80%
- All other dimensions: 100%
- **Overall Score:** 95% (Excellent)
- Weighted calculation: (80% × 0.25) + (100% × 0.75) = 20 + 75 = 95%

**Verification:**

- [ ] Technical Accuracy dimension identifies 2 EPSS failures
- [ ] Dimension score correctly calculated as 80%
- [ ] Overall score weighted correctly at 95%
- [ ] Quality classification: "Excellent"

---

### TC-3: No Remediation Guidance (Actionability Failure)

**Objective:** Verify Actionability checklist detects missing remediation guidance

**Test Data:** `no-remediation-enrichment.md`
**Expected Failure Items:**

- Actionability: "Specific patch versions provided" (FAIL)
- Actionability: "Installation/upgrade instructions clear" (FAIL)
- Actionability: "Clear action items for remediation team" (FAIL)

**Expected Results:**

- Actionability: 5/8 items pass → 62.5%
- All other dimensions: 100%
- **Overall Score:** 94.375% (Excellent)
- Weighted calculation: (100% × 0.85) + (62.5% × 0.15) = 85 + 9.375 = 94.375%

**Verification:**

- [ ] Actionability dimension identifies 3 failures
- [ ] Dimension score correctly calculated as 62.5%
- [ ] Overall score weighted correctly at 94.375%
- [ ] Quality classification: "Excellent"

---

### TC-4: Missing Business Context (Contextualization Failure)

**Objective:** Verify Contextualization checklist detects missing business context

**Test Data:** `missing-context-enrichment.md`
**Expected Failure Items:**

- Contextualization: "Asset Criticality Rating considered" (FAIL)
- Contextualization: "Business impact described" (FAIL)
- Contextualization: "Affected business processes identified" (FAIL)
- Contextualization: "Internal infrastructure considerations mentioned" (FAIL)

**Expected Results:**

- Contextualization: 6/10 items pass → 60%
- All other dimensions: 100%
- **Overall Score:** 94% (Excellent)
- Weighted calculation: (100% × 0.85) + (60% × 0.15) = 85 + 9 = 94%

**Verification:**

- [ ] Contextualization dimension identifies 4 failures
- [ ] Dimension score correctly calculated as 60%
- [ ] Overall score weighted correctly at 94%
- [ ] Quality classification: "Excellent"

---

### TC-5: Confirmation Bias Detected (Cognitive Bias Failure)

**Objective:** Verify Cognitive Bias checklist detects biased reasoning

**Test Data:** `confirmation-bias-enrichment.md`
**Expected Failure Items:**

- Cognitive Bias: "Confirmation Bias: Evidence objectively evaluated" (FAIL)
- Cognitive Bias: "Anchoring Bias: Priority not over-influenced by CVSS alone" (FAIL)

**Expected Results:**

- Cognitive Bias: 3/5 items pass → 60%
- All other dimensions: 100%
- **Overall Score:** 98% (Excellent)
- Weighted calculation: (100% × 0.95) + (60% × 0.05) = 95 + 3 = 98%

**Verification:**

- [ ] Cognitive Bias dimension identifies 2 bias patterns
- [ ] Dimension score correctly calculated as 60%
- [ ] Overall score weighted correctly at 98%
- [ ] Quality classification: "Excellent"

---

### TC-6: Multiple Dimension Failures (Needs Improvement)

**Objective:** Verify quality score drops to "Needs Improvement" with multiple failures

**Test Data:** `multiple-failures-enrichment.md`
**Expected Failure Distribution:**

- Technical Accuracy: 6/10 pass → 60%
- Completeness: 8/12 pass → 66.7%
- Actionability: 4/8 pass → 50%
- Contextualization: 5/10 pass → 50%
- Documentation Quality: 6/8 pass → 75%
- Attack Mapping Validation: 2/4 pass → 50%
- Cognitive Bias: 3/5 pass → 60%
- Source Citation: 3/5 pass → 60%

**Expected Results:**

- **Overall Score:** 60.35% (Needs Improvement)
- Weighted calculation:
  - Technical Accuracy: 60% × 0.25 = 15
  - Completeness: 66.7% × 0.20 = 13.34
  - Actionability: 50% × 0.15 = 7.5
  - Contextualization: 50% × 0.15 = 7.5
  - Documentation: 75% × 0.10 = 7.5
  - Attack Mapping: 50% × 0.05 = 2.5
  - Cognitive Bias: 60% × 0.05 = 3
  - Source Citation: 60% × 0.05 = 3
  - Total: 60.35%

**Verification:**

- [ ] All dimension scores calculated correctly
- [ ] Overall score weighted correctly at 60.35%
- [ ] Quality classification: "Needs Improvement" (60-74% range)

---

### TC-7: Inadequate Quality (Major Rework Required)

**Objective:** Verify quality score drops to "Inadequate" with severe failures

**Test Data:** `inadequate-enrichment.md`
**Expected Failure Distribution:**

- Technical Accuracy: 3/10 pass → 30%
- Completeness: 4/12 pass → 33.3%
- Actionability: 2/8 pass → 25%
- Contextualization: 2/10 pass → 20%
- Documentation Quality: 4/8 pass → 50%
- Attack Mapping Validation: 1/4 pass → 25%
- Cognitive Bias: 2/5 pass → 40%
- Source Citation: 2/5 pass → 40%

**Expected Results:**

- **Overall Score:** 30.66% (Inadequate)
- Weighted calculation:
  - Technical Accuracy: 30% × 0.25 = 7.5
  - Completeness: 33.3% × 0.20 = 6.66
  - Actionability: 25% × 0.15 = 3.75
  - Contextualization: 20% × 0.15 = 3
  - Documentation: 50% × 0.10 = 5
  - Attack Mapping: 25% × 0.05 = 1.25
  - Cognitive Bias: 40% × 0.05 = 2
  - Source Citation: 40% × 0.05 = 2
  - Total: 30.66%

**Verification:**

- [ ] All dimension scores calculated correctly
- [ ] Overall score weighted correctly at 30.66%
- [ ] Quality classification: "Inadequate" (<60% range)
- [ ] Review report flags as "major rework required"

---

## Test Execution Instructions

### Manual Testing

1. Activate Security Reviewer agent: `/BMad:agents:security-reviewer`
2. Run review command: `*review-enrichment {test-case-name}`
3. Agent executes all 8 checklists sequentially
4. Verify dimension scores match expected percentages
5. Verify overall score matches expected weighted average
6. Verify quality classification matches expected category

### Automated Testing (Future)

- Create executable test scripts that simulate agent behavior
- Parse checklist outputs programmatically
- Assert expected scores against actual scores
- Generate test reports

## Success Criteria

- [ ] All test cases execute without errors
- [ ] Dimension scores calculate accurately (within ±1% margin)
- [ ] Overall scores calculate accurately using correct weighted formula
- [ ] Quality classifications match expected categories
- [ ] Agent generates comprehensive review reports for all test cases

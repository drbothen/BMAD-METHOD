# Test Cases: security-analysis-review-workflow.yaml

## Test Overview

This document defines integration test cases for the complete Security Analysis Review Workflow, covering all 7 stages from review preparation through feedback loop, quality evaluation, error handling, and resume capability.

## Test Environment Setup

### Prerequisites

- Atlassian MCP server configured and authenticated
- (Optional) Perplexity MCP server configured and authenticated
- JIRA test instance with test tickets containing enrichments
- `config.yaml` properly configured
- Security Reviewer agent activated
- Write access to `artifacts/reviews/` directory
- Write access to `metrics/` directory
- Write access to `.workflow-state/` directory
- All 8 quality dimension checklists available in `checklists/`
- Review report template available at `templates/security-review-report-tmpl.yaml`

### Test Data Requirements

**Required Test Tickets (to be created by QA/PO):**

The following test tickets must be created in your JIRA project before executing these test cases. **IMPORTANT:** Each ticket must have an enrichment comment (from Story 3.1 workflow) for the review workflow to work.

**Ticket Creation Instructions:**

**TEST-REV-001: Excellent Enrichment Test Ticket**

```yaml
Summary: "Apache Struts RCE Vulnerability (CVE-2024-1234)"
Description: "Critical vulnerability affecting production web servers"
Issue Type: "Security Alert" or "Bug"
Priority: "Critical"
Custom Fields:
  CVE ID: "CVE-2024-1234"
  Affected Systems: ["web-prod-01", "web-prod-02"]
  Asset Criticality Rating: "High"
  System Exposure: "Internet-facing"
  CVSS Score: 9.8
  EPSS Score: 0.75
  KEV Status: "Listed"
Status: "In Progress"

Comments:
  - Posted by Security Analyst
  - Contains complete enrichment with all 12 sections
  - All metrics accurate
  - Clear remediation steps
  - Proper source citations
  - MITRE ATT&CK mapping included
```

**TEST-REV-002: Good Enrichment with Minor Gaps Test Ticket**

```yaml
Summary: "OpenSSL Vulnerability (CVE-2024-5678)"
Description: "Moderate vulnerability requiring assessment"
Issue Type: "Security Alert" or "Bug"
Priority: "High"
Custom Fields:
  CVE ID: "CVE-2024-5678"
  Affected Systems: ["web-prod-03"]
  CVSS Score: 7.5
Status: "In Progress"

Comments:
  - Posted by Security Analyst
  - Contains enrichment with 10/12 sections (missing business context and ATT&CK mapping)
  - Metrics generally accurate
  - Remediation steps somewhat vague
  - Some source citations missing
```

**TEST-REV-003: Poor Enrichment with Critical Errors Test Ticket**

```yaml
Summary: "PostgreSQL Vulnerability (CVE-2024-9999)"
Description: "Database vulnerability requiring analysis"
Issue Type: "Security Alert" or "Bug"
Priority: "High"
Custom Fields:
  CVE ID: "CVE-2024-9999"
  Affected Systems: ["db-prod-01"]
  CVSS Score: 8.1 (INCORRECT - should be 5.3)
Status: "In Progress"

Comments:
  - Posted by Security Analyst
  - Contains enrichment with critical errors:
    * Incorrect CVSS score (8.1 vs actual 5.3)
    * Incorrect KEV status (claims "Listed" but actually "Not Listed")
    * Missing priority assessment
    * Incomplete remediation guidance
    * No ATT&CK mapping
    * Weak source citations
```

**TEST-REV-004: Enrichment with Cognitive Biases Test Ticket**

```yaml
Summary: "WordPress Plugin Vulnerability (CVE-2024-7777)"
Description: "Plugin vulnerability requiring analysis"
Issue Type: "Security Alert" or "Bug"
Priority: "Medium"
Custom Fields:
  CVE ID: "CVE-2024-7777"
  Affected Systems: ["web-cms-01"]
  CVSS Score: 6.5
Status: "In Progress"

Comments:
  - Posted by Security Analyst
  - Contains enrichment with notable cognitive biases:
    * Anchoring bias: Over-relies on CVSS score
    * Confirmation bias: Emphasizes criticality despite low EPSS (0.01)
    * Availability heuristic: Compares to Log4Shell without justification
    * Overconfidence: States "exploit is imminent" without evidence
```

**TEST-REV-005: Resume Review Workflow Test Ticket**

```yaml
Summary: "Django Framework Vulnerability (CVE-2024-3333)"
Description: "Framework vulnerability requiring review"
Issue Type: "Security Alert" or "Bug"
Priority: "Medium"
Custom Fields:
  CVE ID: "CVE-2024-3333"
  Affected Systems: ["app-server-01"]
Status: "In Progress"

Comments:
  - Posted by Security Analyst
  - Contains standard enrichment for resume testing
```

**After Creating Tickets:**

1. **Execute Story 3.1 enrichment workflow** on each test ticket to generate enrichments:

   ```
   *enrich-ticket TEST-REV-001
   *enrich-ticket TEST-REV-002
   *enrich-ticket TEST-REV-003
   *enrich-ticket TEST-REV-004
   *enrich-ticket TEST-REV-005
   ```

2. **Manually modify enrichments** for test tickets 002, 003, 004:
   - TEST-REV-002: Remove business context and ATT&CK sections
   - TEST-REV-003: Introduce critical errors (wrong CVSS, wrong KEV)
   - TEST-REV-004: Introduce bias language (see comments above)

3. Document actual ticket IDs here:
   - TEST-REV-001: `{YOUR-PROJECT-KEY}-____`
   - TEST-REV-002: `{YOUR-PROJECT-KEY}-____`
   - TEST-REV-003: `{YOUR-PROJECT-KEY}-____`
   - TEST-REV-004: `{YOUR-PROJECT-KEY}-____`
   - TEST-REV-005: `{YOUR-PROJECT-KEY}-____`

4. Update test case references throughout this file to use actual ticket IDs

**Required Test Data Files:**

Create these sample enrichment documents for testing without JIRA (unit tests):

- `tests/fixtures/enrichments/test-enrichment-excellent.md` (90%+ quality)
- `tests/fixtures/enrichments/test-enrichment-good.md` (75-89% quality)
- `tests/fixtures/enrichments/test-enrichment-needs-improvement.md` (60-74% quality)
- `tests/fixtures/enrichments/test-enrichment-inadequate.md` (<60% quality)

**JIRA Configuration Prerequisites:**

Before creating test tickets, ensure your JIRA project has:

- ✓ All required custom fields configured (see jira-workflow-standards.md)
- ✓ "Security Alert" or equivalent issue type
- ✓ Required workflow statuses (Open, In Progress, Needs Revision, Approved)
- ✓ Atlassian MCP server configured and authenticated
- ✓ (Optional) Perplexity MCP server for fact verification tests

**Note:** Test tickets should be created in a test/staging JIRA project, not production.

---

## Integration Test Cases

### TC-001: Happy Path - Excellent Enrichment Review

**Objective:** Verify review workflow completes successfully for high-quality enrichment, posts positive review to JIRA, and approves ticket.

**Test Ticket:** TEST-REV-001 (Excellent enrichment)

**Prerequisites:**

- Enrichment posted to TEST-REV-001 with all 12 sections
- All metrics accurate and authoritative sources cited
- Clear remediation guidance and ATT&CK mapping

**Steps:**

1. Clear any existing workflow state: `rm -f .workflow-state/review-TEST-REV-001.json`
2. Clear artifacts directory: `mkdir -p artifacts/reviews/`
3. Execute task: `*review-security-enrichment TEST-REV-001`
4. When prompted for fact verification, select: `n` (no)
5. Monitor progress display through all 7 stages
6. Verify JIRA ticket updated with review comment
7. Verify ticket status changed to "Approved"
8. Verify local review file created
9. Record total execution time

**Expected Results:**

**Stage 1: Preparation (2-3 min)**

- ✅ Ticket read successfully
- ✅ Enrichment extracted from comments
- ✅ All 12 sections parsed
- ✅ Claims extracted (CVSS, EPSS, KEV, patches)
- ✅ Analyst name identified
- ✅ Progress displayed: "✅ Stage 1: Preparation (completed in Xm Xs)"

**Stage 2: Systematic Evaluation (5-7 min)**

- ✅ All 8 checklists executed successfully
- ✅ Technical Accuracy: 95-100%
- ✅ Completeness: 95-100%
- ✅ Actionability: 90-100%
- ✅ Contextualization: 90-100%
- ✅ Documentation Quality: 90-100%
- ✅ MITRE ATT&CK Mapping: 90-100%
- ✅ Cognitive Bias Detection: 95-100%
- ✅ Source Citation: 95-100%
- ✅ Overall Score: 90-100%
- ✅ Quality Classification: "Excellent"
- ✅ Progress displayed: "✅ Stage 2: Systematic Evaluation (completed in Xm Xs)"

**Stage 3: Gap Identification (3-4 min)**

- ✅ Critical Issues: 0
- ✅ Significant Gaps: 0-1
- ✅ Minor Improvements: 0-3
- ✅ All gaps have location, impact, recommendation
- ✅ Progress displayed: "✅ Stage 3: Gap Identification (completed in Xm Xs)"

**Stage 4: Bias Detection (2-3 min)**

- ✅ Bias assessment complete
- ✅ No significant biases detected (or minimal)
- ✅ Constructive feedback provided
- ✅ Progress displayed: "✅ Stage 4: Bias Detection (completed in Xm Xs)"

**Stage 5: Fact Verification (skipped)**

- ✅ Progress displayed: "⏭️ Stage 5: Fact Verification (skipped - user declined)"

**Stage 6: Documentation (2-3 min)**

- ✅ Review report generated with all 12 sections
- ✅ Strengths section lists 3-5 positive aspects
- ✅ Constructive tone maintained throughout
- ✅ Learning resources included
- ✅ Progress displayed: "✅ Stage 6: Documentation (completed in Xm Xs)"

**Stage 7: Feedback Loop (1 min)**

- ✅ Review posted to JIRA as comment
- ✅ Ticket status changed to "Approved" (no critical issues)
- ✅ Ticket assigned to analyst
- ✅ Review file saved to `artifacts/reviews/TEST-REV-001-review-{timestamp}.md`
- ✅ Metrics logged to `metrics/review-metrics-{date}.jsonl`
- ✅ Progress displayed: "✅ Stage 7: Feedback Loop (completed in Xs)"

**Overall Success Criteria:**

- ✅ Total duration: <20 minutes
- ✅ All stages completed successfully
- ✅ Review posted to JIRA ticket with constructive feedback
- ✅ Ticket approved with positive review
- ✅ Files saved locally
- ✅ Completion summary displayed with quality score 90%+

**Manual Verification:**

- Open JIRA ticket TEST-REV-001 and verify review comment posted
- Verify comment contains all 12 sections
- Verify tone is constructive and acknowledges strengths
- Verify ticket status is "Approved"
- Verify assignee is set to original analyst

---

### TC-002: Good Enrichment with Minor Gaps

**Objective:** Verify review workflow identifies minor gaps, provides constructive feedback, and approves ticket with recommendations.

**Test Ticket:** TEST-REV-002 (Good enrichment with 2-3 missing sections)

**Prerequisites:**

- Enrichment posted with 10/12 sections (missing business context and ATT&CK)
- Metrics generally accurate
- Some remediation steps vague

**Steps:**

1. Clear workflow state
2. Execute: `*review-security-enrichment TEST-REV-002`
3. Decline fact verification
4. Monitor progress through all stages
5. Verify review identifies gaps but maintains constructive tone
6. Verify ticket status remains "In Progress" or "Approved"

**Expected Results:**

**Stage 2: Evaluation**

- Overall Score: 75-89%
- Quality Classification: "Good"

**Stage 3: Gap Identification**

- Critical Issues: 0
- Significant Gaps: 2-3 (missing business context, missing ATT&CK, vague remediation)
- Minor Improvements: 2-5

**Stage 6: Documentation**

- Review acknowledges strengths first
- Gaps listed constructively with specific recommendations
- Learning resources provided for each gap
- Tone remains supportive and blameless

**Stage 7: Feedback**

- Ticket status: "In Progress" or "Approved" (no critical issues)
- Review posted successfully

**Success Criteria:**

- ✅ Gaps correctly identified
- ✅ Constructive tone maintained
- ✅ Specific recommendations provided
- ✅ Ticket not blocked (no critical issues)

---

### TC-003: Poor Enrichment with Critical Errors

**Objective:** Verify review workflow detects critical errors, changes ticket status to "Needs Revision", and notifies analyst with specific corrections.

**Test Ticket:** TEST-REV-003 (Poor enrichment with incorrect CVSS, KEV, and missing priority)

**Prerequisites:**

- Enrichment contains critical errors:
  - Incorrect CVSS score (8.1 vs actual 5.3)
  - Incorrect KEV status (claims Listed, actually Not Listed)
  - Missing priority assessment
  - Incomplete remediation

**Steps:**

1. Clear workflow state
2. Execute: `*review-security-enrichment TEST-REV-003`
3. Accept fact verification: `y` (to verify factual errors)
4. Monitor progress through all stages
5. Verify critical errors detected
6. Verify ticket status changed to "Needs Revision"

**Expected Results:**

**Stage 2: Evaluation**

- Overall Score: <60%
- Quality Classification: "Inadequate"
- Technical Accuracy: <50% (critical errors)

**Stage 3: Gap Identification**

- Critical Issues: 3-4
  - Incorrect CVSS score (location: Vulnerability Overview, impact: wrong prioritization, fix: correct to 5.3)
  - Incorrect KEV status (location: Metrics, impact: false urgency, fix: correct to "Not Listed")
  - Missing priority assessment (location: N/A, impact: no remediation timeline, fix: add priority section)
  - Incomplete remediation (location: Remediation, impact: not actionable, fix: add specific steps)
- Significant Gaps: 2-5
- Minor Improvements: variable

**Stage 5: Fact Verification (performed)**

- Claims verified: 4-6
- Accuracy score: <50%
- Discrepancies found:
  - CVSS: Claimed 8.1, Actual 5.3
  - KEV: Claimed Listed, Actual Not Listed

**Stage 6: Documentation**

- Critical issues section prominent and detailed
- Each error has specific correction
- Tone remains blameless but clear about severity
- Next steps: "Needs Revision - please address critical issues"

**Stage 7: Feedback**

- Ticket status changed to: "Needs Revision"
- Review posted with critical issues highlighted
- Analyst assigned and notified

**Success Criteria:**

- ✅ All critical errors detected
- ✅ Fact verification identifies discrepancies
- ✅ Ticket blocked with "Needs Revision" status
- ✅ Specific corrections provided for each error
- ✅ Analyst notified via assignment

**Manual Verification:**

- Open JIRA ticket TEST-REV-003
- Verify status is "Needs Revision"
- Verify review comment clearly lists critical errors
- Verify each error has specific correction value

---

### TC-004: Cognitive Bias Detection

**Objective:** Verify review workflow detects cognitive biases and provides debiasing strategies.

**Test Ticket:** TEST-REV-004 (Enrichment with multiple cognitive biases)

**Prerequisites:**

- Enrichment contains bias indicators:
  - Anchoring: Over-reliance on CVSS score
  - Confirmation: Emphasizes severity despite low EPSS
  - Availability heuristic: Inappropriate Log4Shell comparison
  - Overconfidence: "Exploit is imminent" without evidence

**Steps:**

1. Clear workflow state
2. Execute: `*review-security-enrichment TEST-REV-004`
3. Decline fact verification
4. Monitor Stage 4 (Bias Detection) closely
5. Verify biases detected with specific examples
6. Verify debiasing strategies provided

**Expected Results:**

**Stage 2: Evaluation**

- Cognitive Bias Detection checklist: <80% (biases present)

**Stage 4: Bias Detection**

- Detected Biases: 3-4
  1. Anchoring Bias
     - Evidence: "CVSS 6.5 indicates high severity" (ignores EPSS 0.01)
     - Impact: May over-prioritize based on CVSS alone
     - Debiasing: "Consider EPSS and exploit activity, not just CVSS"
  2. Confirmation Bias
     - Evidence: Emphasizes criticality while downplaying low EPSS
     - Impact: Selective evidence interpretation
     - Debiasing: "Acknowledge contradictory evidence (low EPSS suggests lower urgency)"
  3. Availability Heuristic
     - Evidence: "This is like Log4Shell"
     - Impact: False equivalence without technical similarity
     - Debiasing: "Compare based on technical characteristics, not memorable events"
  4. Overconfidence Bias
     - Evidence: "Exploit is imminent"
     - Impact: Unwarranted certainty
     - Debiasing: "Use probabilistic language ('likely', 'possible') when uncertain"

**Stage 6: Documentation**

- Cognitive Bias Assessment section detailed
- Each bias has specific example quote
- Debiasing strategies actionable
- Tone educational, not accusatory

**Success Criteria:**

- ✅ All major biases detected
- ✅ Specific text examples cited
- ✅ Debiasing strategies specific and actionable
- ✅ Tone remains constructive

---

### TC-005: Resume After Interruption

**Objective:** Verify review workflow can be interrupted and resumed from last completed stage.

**Test Ticket:** TEST-REV-005 (Standard enrichment)

**Steps:**

1. Clear workflow state
2. Execute: `*review-security-enrichment TEST-REV-005`
3. **Interrupt workflow during Stage 3** (Gap Identification)
4. Verify state file exists: `ls .workflow-state/review-TEST-REV-005.json`
5. Re-execute: `*review-security-enrichment TEST-REV-005`
6. When prompted "Resume from Stage 3? (y/n)", select: `y`
7. Verify workflow resumes from Stage 3
8. Verify Stages 1-2 are skipped (marked completed)
9. Verify data from Stages 1-2 is loaded from state
10. Complete remaining stages

**Expected Results:**

**On Resume:**

- ✅ State file detected: `.workflow-state/review-TEST-REV-005.json`
- ✅ Prompt displayed: "Resume review from Stage 3? (y/n)"
- ✅ User selects: `y`
- ✅ Workflow loads state and displays:
  ```
  🔍 Resuming Security Analysis Review Workflow
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Stage 1: Preparation (completed previously)
  ✅ Stage 2: Systematic Evaluation (completed previously)
  🔄 Stage 3: Gap Identification (resuming...)
  ⏳ Stage 4: Bias Detection
  ⏳ Stage 5: Fact Verification
  ⏳ Stage 6: Documentation
  ⏳ Stage 7: Feedback Loop
  ```
- ✅ Stage 3 executes with data from Stages 1-2
- ✅ Remaining stages complete normally
- ✅ State file archived on completion

**Success Criteria:**

- ✅ State preserved across interruption
- ✅ Resume prompt displayed
- ✅ Data from completed stages loaded correctly
- ✅ Remaining stages complete successfully
- ✅ Final review report includes all data

---

### TC-006: Fact Verification with Perplexity MCP

**Objective:** Verify optional fact verification correctly verifies claims and detects discrepancies.

**Test Ticket:** TEST-REV-003 (Contains factual errors for verification)

**Prerequisites:**

- Perplexity MCP configured and available
- Enrichment contains verifiable claims (CVSS, EPSS, KEV, patches)

**Steps:**

1. Clear workflow state
2. Execute: `*review-security-enrichment TEST-REV-003`
3. When prompted for fact verification, select: `y`
4. Monitor Stage 5 (Fact Verification) closely
5. Verify Perplexity MCP queries executed
6. Verify discrepancies detected and documented

**Expected Results:**

**Stage 5: Fact Verification**

- ✅ Perplexity MCP queries executed for each claim type
- ✅ CVSS verified against NVD
- ✅ EPSS verified against FIRST
- ✅ KEV verified against CISA catalog
- ✅ Discrepancies detected:
  - CVSS: Claimed 8.1, Actual 5.3, Source: nvd.nist.gov
  - KEV: Claimed Listed, Actual Not Listed, Source: cisa.gov/kev
- ✅ Accuracy Score: <50% (2 incorrect out of 4-6 claims)
- ✅ Progress displayed: "✅ Stage 5: Fact Verification (completed in Xm Xs)"

**Stage 6: Documentation**

- ✅ Fact Verification Results section populated
- ✅ Accuracy score displayed
- ✅ Each discrepancy documented with:
  - Analyst claim
  - Verified actual value
  - Authoritative source URL
  - Severity: Critical (for CVSS/KEV errors)

**Success Criteria:**

- ✅ Fact verification stage executes
- ✅ Perplexity MCP queries successful
- ✅ Discrepancies correctly identified
- ✅ Accuracy score calculated correctly
- ✅ Review report includes verification results

---

### TC-007: Graceful Degradation - Perplexity MCP Unavailable

**Objective:** Verify workflow handles Perplexity MCP unavailability gracefully by skipping fact verification.

**Test Ticket:** TEST-REV-001 (Any enrichment)

**Prerequisites:**

- Perplexity MCP disabled or unavailable

**Steps:**

1. Disable Perplexity MCP (or disconnect from server)
2. Clear workflow state
3. Execute: `*review-security-enrichment TEST-REV-001`
4. Verify workflow detects Perplexity unavailability during setup
5. Verify fact verification skipped automatically (no prompt)
6. Verify workflow completes successfully

**Expected Results:**

**Initial Setup:**

- ✅ Warning displayed: "Fact verification will be skipped - Perplexity MCP not available"
- ✅ No prompt for fact verification (automatically set to skip)

**Stage 5: Fact Verification**

- ✅ Progress displayed: "⏭️ Stage 5: Fact Verification (skipped - Perplexity MCP unavailable)"
- ✅ Workflow continues to Stage 6

**Stage 6: Documentation**

- ✅ Fact Verification Results section shows: "ℹ️ Fact verification was not performed for this review"

**Overall:**

- ✅ Workflow completes successfully
- ✅ Review posted to JIRA
- ✅ No errors due to missing Perplexity

**Success Criteria:**

- ✅ Workflow detects MCP unavailability
- ✅ Fact verification skipped gracefully
- ✅ Review report documents skip reason
- ✅ No errors or failures

---

### TC-008: Error Handling - Atlassian MCP Unavailable

**Objective:** Verify workflow halts gracefully when required Atlassian MCP is unavailable.

**Test Ticket:** N/A (MCP unavailable prevents ticket read)

**Prerequisites:**

- Atlassian MCP disabled or unavailable

**Steps:**

1. Disable Atlassian MCP
2. Execute: `*review-security-enrichment TEST-REV-001`
3. Verify workflow detects MCP unavailability during setup
4. Verify workflow halts with clear error message

**Expected Results:**

**Initial Setup:**

- ❌ Workflow halts immediately
- ❌ Error message displayed: "Atlassian MCP required for review workflow. Please configure Atlassian MCP and retry."
- ❌ No stages executed

**Success Criteria:**

- ✅ Workflow detects required MCP missing
- ✅ Clear error message displayed
- ✅ Workflow does not attempt to continue
- ✅ No partial review created

---

### TC-009: Error Handling - Enrichment Not Found

**Objective:** Verify workflow halts when JIRA ticket has no enrichment comment.

**Test Ticket:** Create new ticket without enrichment

**Steps:**

1. Create new JIRA ticket (e.g., TEST-REV-999)
2. Do NOT run enrichment workflow on this ticket
3. Execute: `*review-security-enrichment TEST-REV-999`
4. Verify workflow detects missing enrichment in Stage 1

**Expected Results:**

**Stage 1: Preparation**

- ❌ Enrichment extraction fails
- ❌ Error message: "No enrichment found. Ensure Story 3.1 workflow completed for this ticket."
- ❌ Workflow halts

**Success Criteria:**

- ✅ Missing enrichment detected
- ✅ Clear error message with remediation guidance
- ✅ Workflow does not proceed to evaluation

---

### TC-010: Performance Validation

**Objective:** Verify 90% of review executions complete within 15-20 minute target.

**Test Tickets:** All test tickets (TEST-REV-001 through TEST-REV-005)

**Steps:**

1. Execute review workflow on all 5 test tickets
2. For each execution, record total duration
3. Calculate average, median, 90th percentile
4. Verify 90th percentile ≤ 20 minutes

**Expected Results:**

**Per-Stage Duration Targets:**

- Stage 1 (Preparation): ≤3 minutes
- Stage 2 (Evaluation): ≤7 minutes
- Stage 3 (Gap Identification): ≤4 minutes
- Stage 4 (Bias Detection): ≤3 minutes
- Stage 5 (Fact Verification): ≤5 minutes (if performed)
- Stage 6 (Documentation): ≤3 minutes
- Stage 7 (Feedback Loop): ≤1 minute

**Total Duration:**

- Without fact verification: 12-17 minutes (target: ≤15 min)
- With fact verification: 15-22 minutes (target: ≤20 min)
- 90th percentile: ≤20 minutes

**Success Criteria:**

- ✅ Average execution time ≤ 17 minutes
- ✅ 90th percentile ≤ 20 minutes
- ✅ No single stage exceeds 2x target duration
- ✅ Metrics logged to `metrics/review-metrics-{date}.jsonl`

**Metrics Validation:**

- Open `metrics/review-metrics-{date}.jsonl`
- Verify all 5 executions logged
- Verify stage durations recorded
- Verify overall scores recorded

---

## Test Execution Summary Template

After running all test cases, document results:

```markdown
## Test Execution Results

**Test Date:** YYYY-MM-DD
**Tester:** {name}
**Environment:** {test/staging JIRA instance}

| Test Case                     | Status  | Duration | Notes                          |
| ----------------------------- | ------- | -------- | ------------------------------ |
| TC-001 Happy Path             | ✅ Pass | 16m 30s  | All stages successful          |
| TC-002 Minor Gaps             | ✅ Pass | 15m 45s  | Gaps identified correctly      |
| TC-003 Critical Errors        | ✅ Pass | 19m 20s  | Fact verification successful   |
| TC-004 Bias Detection         | ✅ Pass | 14m 10s  | All biases detected            |
| TC-005 Resume                 | ✅ Pass | 12m 05s  | Resume from Stage 3 successful |
| TC-006 Fact Verification      | ✅ Pass | 18m 45s  | Perplexity queries successful  |
| TC-007 Perplexity Unavailable | ✅ Pass | 13m 30s  | Graceful skip                  |
| TC-008 Atlassian Unavailable  | ✅ Pass | 0m 05s   | Halted correctly               |
| TC-009 No Enrichment          | ✅ Pass | 0m 30s   | Error detected                 |
| TC-010 Performance            | ✅ Pass | N/A      | 90th %ile: 19m 15s             |

**Overall Result:** ✅ All tests passed
**Performance:** Within target (90th percentile: 19m 15s)
**Issues Found:** None
**Recommendations:** Ready for production use
```

---

## Manual Validation Checklist

After automated tests, manually verify:

- [ ] Review reports in JIRA are well-formatted and readable
- [ ] Constructive tone maintained in all reviews
- [ ] Strengths acknowledged before gaps
- [ ] Specific recommendations provided for each gap
- [ ] Learning resources appropriate and helpful
- [ ] Ticket status changes accurate (Approved vs Needs Revision)
- [ ] Analyst notifications sent correctly
- [ ] Local files saved with correct naming convention
- [ ] Metrics logged completely and accurately
- [ ] No sensitive data exposed in review reports

---

## Regression Testing Notes

Run these tests after any changes to:

- Quality dimension checklists (Story 2.2)
- Review report template (Story 2.6)
- Categorization logic (Story 2.3)
- Workflow YAML definition
- Review orchestration task file
- MCP integration code

**Critical Regressions to Watch:**

- Performance degradation (>25 min execution time)
- Fact verification accuracy drops
- Bias detection misses obvious biases
- Constructive tone lost (overly critical reviews)
- JIRA integration failures
- State management issues (resume failures)

---

## Notes

- This is an integration test suite designed for runtime execution
- Requires real JIRA instance with enriched tickets
- Test data should be created in test/staging JIRA, not production
- Performance targets based on Story 3.2 acceptance criteria
- Fact verification requires Perplexity MCP (optional but recommended for full testing)
- State management enables testing of resume capability
- All tests validate constructive tone and blameless culture

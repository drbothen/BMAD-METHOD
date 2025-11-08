# Test Cases: security-alert-enrichment-workflow.yaml

## Test Overview

This document defines integration test cases for the complete Security Alert Enrichment Workflow, covering all 8 stages from ticket triage through JIRA update, performance validation, error handling, and resume capability.

## Test Environment Setup

### Prerequisites

- Atlassian MCP server configured and authenticated
- Perplexity MCP server configured and authenticated
- JIRA test instance with test tickets
- `config.yaml` properly configured
- Security Analyst agent activated
- Write access to `artifacts/enrichments/` directory
- Write access to `.workflow-state/` directory

### Test Data Requirements

**Required Test Tickets (to be created by QA/PO):**

The following test tickets must be created in your JIRA project before executing these test cases. Use the JIRA project key configured in your `config.yaml` (e.g., "SEC", "AOD", or project-specific key).

**Ticket Creation Instructions:**

**TEST-WF-001: Happy Path Test Ticket**
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
Status: "Open"
```

**TEST-WF-002: Missing CVE Test Ticket**
```yaml
Summary: "Security Alert: Suspicious Activity Detected"
Description: "Potential vulnerability in web application (no CVE ID provided)"
Issue Type: "Security Alert" or "Bug"
Priority: "High"
Custom Fields:
  CVE ID: [leave empty]
  Affected Systems: ["web-prod-03"]
Status: "Open"
```

**TEST-WF-003: Resume Workflow Test Ticket**
```yaml
Summary: "OpenSSL Vulnerability (CVE-2024-9999)"
Description: "OpenSSL vulnerability requiring remediation"
Issue Type: "Security Alert" or "Bug"
Priority: "High"
Custom Fields:
  CVE ID: "CVE-2024-9999"
  Affected Systems: ["test-server-01"]
  Asset Criticality Rating: "Medium"
  System Exposure: "Internal"
Status: "Open"
```

**TEST-WF-004: JIRA Update Failure Test Ticket**
```yaml
Summary: "PostgreSQL Vulnerability (CVE-2024-7777)"
Description: "Database vulnerability requiring immediate attention"
Issue Type: "Security Alert" or "Bug"
Priority: "High"
Custom Fields:
  CVE ID: "CVE-2024-7777"
  Affected Systems: ["db-prod-01"]
Status: "Open"
```

**After Creating Tickets:**

1. Document actual ticket IDs here:
   - TEST-WF-001: `{YOUR-PROJECT-KEY}-____`
   - TEST-WF-002: `{YOUR-PROJECT-KEY}-____`
   - TEST-WF-003: `{YOUR-PROJECT-KEY}-____`
   - TEST-WF-004: `{YOUR-PROJECT-KEY}-____`

2. Update test case references throughout this file to use actual ticket IDs

3. Verify all custom fields exist in your JIRA project (see `docs/architecture/jira-workflow-standards.md`)

**Required Test Data Files:**

- Sample CVE data for research (CVE-2024-1234, CVE-2024-9999, CVE-2024-7777)
- Sample JIRA custom field values (documented above)
- Mock workflow state file for resume test (provided in TC-005)

**JIRA Configuration Prerequisites:**

Before creating test tickets, ensure your JIRA project has:
- ✓ All required custom fields configured (see jira-workflow-standards.md)
- ✓ "Security Alert" or equivalent issue type
- ✓ Required workflow statuses (Open, In Progress, etc.)
- ✓ Atlassian MCP server configured and authenticated

**Note:** Test tickets should be created in a test/staging JIRA project, not production.

---

## Integration Test Cases

### TC-001: Happy Path - Complete Workflow Success

**Objective:** Verify entire enrichment workflow completes successfully within target duration

**Test Ticket:** TEST-WF-001

**Ticket Configuration:**

```yaml
Summary: "Apache Struts RCE Vulnerability (CVE-2024-1234)"
Description: "Critical vulnerability affecting production web servers"
Custom Fields:
  affected_systems: ["web-prod-01", "web-prod-02"]
  asset_criticality_rating: "High"
  system_exposure: "Internet-facing"
```

**Steps:**

1. Clear any existing workflow state: `rm -f .workflow-state/TEST-WF-001.json`
2. Clear artifacts directory: `mkdir -p artifacts/enrichments/`
3. Execute task: `*enrich-ticket TEST-WF-001`
4. Monitor progress display through all 8 stages
5. Verify JIRA ticket updated
6. Verify local enrichment file created
7. Record total execution time

**Expected Results:**

**Stage 1: Triage (1-2 min)**
- ✅ Ticket read successfully
- ✅ CVE-2024-1234 extracted
- ✅ Affected systems: ["web-prod-01", "web-prod-02"]
- ✅ Progress displayed: "✅ Stage 1: Triage (completed in Xm Xs)"

**Stage 2: CVE Research (3-5 min)**
- ✅ CVSS score obtained (e.g., 9.8)
- ✅ EPSS score obtained
- ✅ KEV status determined
- ✅ Exploit status identified
- ✅ Patch information retrieved
- ✅ ATT&CK suggestions gathered
- ✅ Perplexity MCP called successfully

**Stage 3: Business Context (2-3 min)**
- ✅ ACR rating: High
- ✅ System exposure: Internet-facing
- ✅ Business impact assessed

**Stage 4: Remediation Planning (2-3 min)**
- ✅ Patch version identified
- ✅ Remediation steps generated
- ✅ Compensating controls listed

**Stage 5: MITRE ATT&CK (1-2 min)**
- ✅ At least one tactic mapped
- ✅ At least one technique with T-number
- ✅ Detection implications provided

**Stage 6: Priority Assessment (1-2 min)**
- ✅ Priority level assigned (P1-P5)
- ✅ Priority rationale generated
- ✅ SLA deadline calculated

**Stage 7: Documentation (1 min)**
- ✅ All 12 template sections populated
- ✅ Executive summary generated
- ✅ Markdown document formatted correctly

**Stage 8: JIRA Update (1-2 min)**
- ✅ JIRA comment posted successfully
- ✅ Custom fields updated (priority, CVSS, EPSS, KEV)
- ✅ Local file saved to `artifacts/enrichments/TEST-WF-001-enrichment-{timestamp}.md`
- ✅ File exists and is readable

**Overall Validation:**
- ✅ Total duration: 10-15 minutes (95th percentile)
- ✅ All 8 stages completed
- ✅ Quality score >75% (7+ checks passing)
- ✅ Completion summary displayed
- ✅ Workflow state cleaned up (archived)

**Performance Metrics:**
- Total Time: _______ minutes (must be <15 min)
- Stage 1: _______ seconds
- Stage 2: _______ seconds
- Stage 3: _______ seconds
- Stage 4: _______ seconds
- Stage 5: _______ seconds
- Stage 6: _______ seconds
- Stage 7: _______ seconds
- Stage 8: _______ seconds

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-002: Missing CVE - Error Handling and User Prompt

**Objective:** Verify workflow handles missing CVE ID gracefully and prompts user

**Test Ticket:** TEST-WF-002

**Ticket Configuration:**

```yaml
Summary: "Security Alert: Suspicious Activity Detected"
Description: "Potential vulnerability in web application"
Custom Fields:
  affected_systems: ["web-prod-03"]
```

**Note:** Ticket intentionally has NO CVE ID

**Steps:**

1. Clear workflow state
2. Execute task: `*enrich-ticket TEST-WF-002`
3. Observe Stage 1 behavior
4. When prompted, provide CVE ID: CVE-2024-5678
5. Verify workflow continues from Stage 2

**Expected Results:**

**Stage 1 Error Handling:**
- ⚠️ No CVE found in summary, description, or custom fields
- ❌ Stage 1 error handler activates
- ✅ Clear prompt displayed: "No CVE ID found. Please provide CVE ID:"
- ✅ User provides: CVE-2024-5678
- ✅ CVE accepted and stored

**Stage 2 Resume:**
- ✅ Workflow continues with provided CVE
- ✅ CVE research proceeds normally
- ✅ All subsequent stages complete

**Overall:**
- ✅ No workflow crash or abort
- ✅ Graceful error handling
- ✅ Enrichment completes successfully

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-003: Perplexity Timeout - Retry Logic

**Objective:** Verify retry logic handles Perplexity timeout gracefully

**Test Ticket:** TEST-WF-001

**Setup:** Simulate Perplexity timeout (may require MCP mocking or manual trigger)

**Steps:**

1. Execute task: `*enrich-ticket TEST-WF-001`
2. During Stage 2, simulate or trigger Perplexity timeout
3. Observe retry behavior
4. Verify workflow completes

**Expected Results:**

**Stage 2 Timeout Handling:**
- ⚠️ Perplexity timeout detected
- ✅ Error message: "Perplexity research timeout. Retrying with simplified query..."
- ✅ First retry: Wait 10 seconds, retry with simpler query
- ✅ If successful: Continue normally
- ✅ If second timeout: Wait 30 seconds, retry again
- ✅ If third timeout: Prompt user for manual research or fallback

**Retry Logic:**
- ✅ Automatic retry up to 3 times
- ✅ Exponential backoff (10s, 30s)
- ✅ Simplified query on retry
- ✅ No data loss between retries

**Fallback:**
- ✅ If all retries fail, manual research option provided
- ✅ Workflow can continue with partial data
- ✅ Warning noted in enrichment document

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-004: JIRA Update Failure - Local Save Fallback

**Objective:** Verify enrichment is saved locally when JIRA update fails

**Test Ticket:** TEST-WF-004

**Setup:** Simulate JIRA API error during Stage 8 (disconnect MCP or use invalid credentials temporarily)

**Steps:**

1. Execute task: `*enrich-ticket TEST-WF-004`
2. Allow Stages 1-7 to complete normally
3. During Stage 8, JIRA update fails (simulated)
4. Verify local save behavior
5. Verify error messaging

**Expected Results:**

**Stage 8 Failure Handling:**
- ❌ JIRA comment post fails with API error
- ⚠️ Error message: "JIRA update failed. Saving enrichment locally..."
- ✅ Enrichment document saved to `artifacts/enrichments/TEST-WF-004-enrichment-{timestamp}.md`
- ✅ File contains complete enrichment with all 12 sections
- ✅ User notified with actionable message:
  - "Enrichment saved locally. To update JIRA manually:"
  - "1. Copy content from: {file_path}"
  - "2. Post as comment to TEST-WF-004"

**Audit Trail:**
- ✅ Local file saved successfully (critical requirement)
- ✅ Workflow state shows partial completion
- ✅ Quality validation still performed on enrichment document

**Recovery:**
- ✅ User can manually post comment to JIRA
- ✅ Enrichment document is complete and valid
- ✅ No data loss

**Cleanup:** Restore JIRA MCP connection

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-005: Resume Workflow After Interruption

**Objective:** Verify workflow can resume from last completed stage after interruption

**Test Ticket:** TEST-WF-003

**Setup:**

1. Create workflow state file manually or execute workflow and interrupt

**Mock State File:** `.workflow-state/TEST-WF-003.json`

```json
{
  "workflow_id": "security-alert-enrichment-v1",
  "ticket_id": "TEST-WF-003",
  "started_at": "2025-11-08T10:00:00Z",
  "current_stage": 5,
  "stages_completed": [1, 2, 3, 4],
  "stages_failed": [],
  "total_elapsed_seconds": 480,
  "data": {
    "stage1": {
      "cve_id": "CVE-2024-9999",
      "affected_systems": ["test-server-01"]
    },
    "stage2": {
      "cvss_score": 8.5,
      "epss_score": 0.65,
      "kev_status": false
    },
    "stage3": {
      "acr_rating": "Medium",
      "system_exposure": "Internal"
    },
    "stage4": {
      "patch_available": true,
      "patch_version": "2.5.33"
    }
  }
}
```

**Steps:**

1. Place mock state file in `.workflow-state/TEST-WF-003.json`
2. Execute task: `*enrich-ticket TEST-WF-003`
3. Observe resume prompt
4. Select "Yes" to resume
5. Verify workflow continues from Stage 5
6. Verify all previous stage data is loaded

**Expected Results:**

**Resume Detection:**
- ✅ State file detected on startup
- ✅ Prompt displayed: "Incomplete workflow found for TEST-WF-003. Resume from Stage 5? (y/n)"
- ✅ User selects: y

**Resume Execution:**
- ✅ Progress display shows stages 1-4 as completed:
  - "✅ Stage 1: Triage (completed in 1m 23s)"
  - "✅ Stage 2: CVE Research (completed in 4m 12s)"
  - "✅ Stage 3: Business Context (completed in 2m 15s)"
  - "✅ Stage 4: Remediation Planning (completed in 2m 30s)"
- 🔄 Stage 5 starts immediately
- ✅ All previous data loaded from state file
- ✅ CVE ID: CVE-2024-9999
- ✅ CVSS: 8.5
- ✅ ACR: Medium

**Stages 5-8 Execution:**
- ✅ Stage 5: MITRE ATT&CK mapping completes
- ✅ Stage 6: Priority assessment uses loaded CVSS/EPSS data
- ✅ Stage 7: Documentation includes all data from stages 1-6
- ✅ Stage 8: JIRA update succeeds

**State Cleanup:**
- ✅ On completion, state file archived to `.workflow-state/completed/TEST-WF-003-{timestamp}.json`
- ✅ Active state file removed

**Alternative: Decline Resume**
- If user selects "n" to resume prompt:
- ✅ Old state archived
- ✅ Fresh workflow starts from Stage 1

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Performance Test Cases

### TC-006: Workflow Duration - 95th Percentile Target

**Objective:** Validate workflow completes within 10-15 minute target

**Test Method:** Execute TC-001 at least 10 times and measure durations

**Steps:**

1. Execute workflow 10 times with different test tickets
2. Record total duration for each execution
3. Calculate 95th percentile duration
4. Validate individual stage durations

**Expected Results:**

**Overall Duration:**
- ✅ 95th percentile: <15 minutes
- ✅ Median: ~12 minutes
- ✅ No execution >20 minutes (hard limit)

**Individual Stage Targets:**
- ✅ Stage 1: 1-2 minutes average
- ✅ Stage 2: 3-5 minutes average (largest variance expected)
- ✅ Stage 3: 2-3 minutes average
- ✅ Stage 4: 2-3 minutes average
- ✅ Stage 5: 1-2 minutes average
- ✅ Stage 6: 1-2 minutes average
- ✅ Stage 7: <1 minute average
- ✅ Stage 8: 1-2 minutes average

**Performance Warnings:**
- ⚠️ If any stage exceeds 2x target, log warning
- ⚠️ If total exceeds 18 minutes, investigate bottleneck

**Test Results Table:**

| Run | Total Time | S1  | S2  | S3  | S4  | S5  | S6  | S7 | S8  | Pass/Fail |
| --- | ---------- | --- | --- | --- | --- | --- | --- | -- | --- | --------- |
| 1   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 2   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 3   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 4   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 5   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 6   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 7   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 8   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 9   | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |
| 10  | \_\_       | \_  | \_  | \_  | \_  | \_  | \_  | \_ | \_  | ⬜        |

**95th Percentile:** \_\_\_\_\_ minutes

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Quality Test Cases

### TC-007: Template Completeness Validation

**Objective:** Verify all enrichments pass template completeness validation (12 sections)

**Test Ticket:** TEST-WF-001

**Steps:**

1. Execute complete workflow
2. Open generated enrichment file
3. Validate all template sections present and populated

**Required Sections (from security-enrichment-tmpl.yaml):**

1. ✅ Executive Summary
2. ✅ Vulnerability Overview
3. ✅ Technical Details
4. ✅ CVSS Metrics
5. ✅ EPSS Score
6. ✅ CISA KEV Status
7. ✅ Affected Systems
8. ✅ Business Impact
9. ✅ Remediation Guidance
10. ✅ MITRE ATT&CK Mapping
11. ✅ Priority Assessment
12. ✅ References

**Validation Criteria:**

- ✅ All 12 sections present in markdown
- ✅ No sections marked "N/A" or "Unknown" (unless genuinely unavailable)
- ✅ Executive summary >3 sentences
- ✅ At least 3 authoritative references
- ✅ MITRE ATT&CK has at least 1 tactic and 1 technique

**Quality Score Calculation:**
- Sections populated: \_\_\_ / 12
- Quality score: \_\_\_% (target: >75%)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-008: JIRA Custom Fields Validation

**Objective:** Verify all JIRA custom fields updated correctly

**Test Ticket:** TEST-WF-001

**Steps:**

1. Execute complete workflow
2. Read ticket via JIRA web UI or MCP
3. Verify custom fields updated

**Expected Custom Field Updates:**

- ✅ `custom_field_priority`: Matches calculated priority (P1-P5)
- ✅ `custom_field_cvss_score`: Matches research CVSS score
- ✅ `custom_field_epss_score`: Matches research EPSS score
- ✅ `custom_field_kev_status`: Matches KEV determination (true/false)
- ✅ `custom_field_cvss_severity`: Matches CVSS severity (Critical/High/Medium/Low)
- ✅ `custom_field_attack_tactics`: Contains ATT&CK tactics (comma-separated)

**JIRA Comment Validation:**

- ✅ Comment posted successfully
- ✅ Comment contains full enrichment markdown
- ✅ Comment formatting renders correctly in JIRA
- ✅ All 12 sections visible in comment

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Test Execution Summary

**Overall Test Results:**

| Test Case | Objective                        | Status | Notes |
| --------- | -------------------------------- | ------ | ----- |
| TC-001    | Happy Path - Complete Success    | ⬜     |       |
| TC-002    | Missing CVE - Error Handling     | ⬜     |       |
| TC-003    | Perplexity Timeout - Retry Logic | ⬜     |       |
| TC-004    | JIRA Failure - Local Save        | ⬜     |       |
| TC-005    | Resume Workflow                  | ⬜     |       |
| TC-006    | Performance - Duration Target    | ⬜     |       |
| TC-007    | Template Completeness            | ⬜     |       |
| TC-008    | JIRA Fields Validation           | ⬜     |       |

**Pass Criteria:**

- All integration tests (TC-001 to TC-005): Must pass
- Performance test (TC-006): 95th percentile <15 minutes
- Quality tests (TC-007, TC-008): All validation checks pass

**Test Execution Date:** \_\_\_\_\_\_\_\_\_\_

**Tested By:** \_\_\_\_\_\_\_\_\_\_

**Test Environment:** \_\_\_\_\_\_\_\_\_\_

**Notes:**

---

## Known Limitations and Assumptions

1. **MCP Availability:** Tests assume Atlassian and Perplexity MCP servers are available and authenticated
2. **Network Dependency:** Tests require network connectivity for JIRA and Perplexity API calls
3. **Test Tickets:** Tests require pre-created JIRA test tickets with specific configurations
4. **Timing Variability:** Perplexity research timing varies based on CVE complexity and API performance
5. **Manual Simulation:** Some error conditions (timeouts, JIRA failures) may require manual simulation

## Test Data Cleanup

After test execution:

1. Archive workflow state files: `mv .workflow-state/*.json .workflow-state/test-archives/`
2. Archive enrichment artifacts: `mv artifacts/enrichments/TEST-WF-*.md artifacts/test-archives/`
3. Document test ticket IDs for future regression testing
4. Reset config.yaml if modified during testing

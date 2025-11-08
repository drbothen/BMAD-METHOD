# Test Cases: read-jira-ticket.md

## Test Overview
This document defines test cases for the `read-jira-ticket.md` task, covering configuration validation, JIRA integration, CVE extraction, and error handling.

## Test Environment Setup

### Prerequisites
- Atlassian MCP server configured and authenticated
- JIRA test instance or test tickets available
- `config.yaml` properly configured with test values

### Test Data Requirements

**Required Test Tickets (to be created by QA/PO):**
- `TEST-001`: Valid ticket with single CVE in summary
- `TEST-002`: Valid ticket with CVE in description only
- `TEST-003`: Valid ticket with multiple CVEs (at least 2)
- `TEST-004`: Valid ticket without CVE ID
- `TEST-005`: Ticket with all custom fields populated

**Note:** Test ticket IDs must be documented before story approval. Update this section with actual ticket IDs.

---

## Test Cases

### TC-001: Valid Configuration Loading
**Objective:** Verify task loads and validates configuration correctly

**Test Data:**
```yaml
jira:
  cloud_id: "test-cloud-id-12345"
  project_key: "TEST"
  custom_fields:
    cve_id: "customfield_10001"
    affected_systems: "customfield_10002"
    asset_criticality_rating: "customfield_10003"
    system_exposure: "customfield_10004"
```

**Steps:**
1. Execute `read-jira-ticket.md` task
2. Verify config file is read
3. Verify all required fields are validated

**Expected Result:**
- ✅ Config loads without errors
- ✅ All required fields validated
- ✅ Task proceeds to ticket ID elicitation

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-002: Missing Configuration File
**Objective:** Verify graceful handling when config.yaml doesn't exist

**Setup:** Temporarily rename or remove `config.yaml`

**Steps:**
1. Execute `read-jira-ticket.md` task
2. Observe error message

**Expected Result:**
- ❌ Clear error: "Config file not found at expansion-packs/bmad-1898-engineering/config.yaml"
- ❌ Task halts gracefully
- ✅ No stack traces or technical errors shown

**Cleanup:** Restore `config.yaml`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-003: Missing Required Configuration Field
**Objective:** Verify validation of required config fields

**Setup:** Remove `jira.cloud_id` from config.yaml

**Steps:**
1. Execute `read-jira-ticket.md` task
2. Observe error message

**Expected Result:**
- ❌ Clear error: "Missing required field: jira.cloud_id"
- ❌ Task halts gracefully

**Cleanup:** Restore `jira.cloud_id`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-004: Valid Ticket with CVE in Summary
**Objective:** Extract CVE from ticket summary field

**Test Ticket:** TEST-001 (or actual ticket ID: _____________)

**Ticket Data:**
```
Summary: "Apache Struts 2 RCE (CVE-2024-1234)"
Description: "Critical vulnerability requiring immediate attention"
```

**Steps:**
1. Execute task
2. Provide ticket ID: TEST-001
3. Verify CVE extraction

**Expected Result:**
- ✅ Ticket read successfully
- ✅ CVE-2024-1234 extracted from summary
- ✅ Primary CVE: CVE-2024-1234
- ✅ Summary displays extracted information

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-005: Valid Ticket with CVE in Description
**Objective:** Extract CVE from description when not in summary

**Test Ticket:** TEST-002 (or actual ticket ID: _____________)

**Ticket Data:**
```
Summary: "Security Alert: Apache Struts Vulnerability"
Description: "Vulnerability CVE-2024-5678 affects production systems..."
```

**Steps:**
1. Execute task
2. Provide ticket ID: TEST-002
3. Verify CVE extraction from description

**Expected Result:**
- ✅ Ticket read successfully
- ✅ CVE-2024-5678 extracted from description
- ✅ Primary CVE: CVE-2024-5678
- ✅ Summary displays extracted information

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-006: Ticket with Multiple CVEs
**Objective:** Extract all CVEs and designate primary

**Test Ticket:** TEST-003 (or actual ticket ID: _____________)

**Ticket Data:**
```
Summary: "Multiple Vulnerabilities (CVE-2024-1111, CVE-2024-2222)"
Description: "Also affects systems with CVE-2024-3333"
```

**Steps:**
1. Execute task
2. Provide ticket ID: TEST-003
3. Verify all CVEs extracted

**Expected Result:**
- ✅ All CVEs extracted: [CVE-2024-1111, CVE-2024-2222, CVE-2024-3333]
- ✅ Primary CVE: CVE-2024-1111 (first in list)
- ✅ All CVEs listed in summary
- ✅ All CVEs included in returned data structure

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-007: Case-Insensitive CVE Extraction
**Objective:** Verify regex handles different CVE case formats

**Mock Data:**
```
Summary: "Vulnerability cve-2024-9999 and CVE-2024-8888"
```

**Expected Result:**
- ✅ Both CVEs extracted regardless of case
- ✅ Normalized to uppercase: CVE-2024-9999, CVE-2024-8888

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-008: Ticket Without CVE ID
**Objective:** Handle tickets missing CVE gracefully

**Test Ticket:** TEST-004 (or actual ticket ID: _____________)

**Ticket Data:**
```
Summary: "Security Alert: Suspicious Activity Detected"
Description: "No CVE assigned yet, manual investigation required"
```

**Steps:**
1. Execute task
2. Provide ticket ID: TEST-004
3. Observe warning message
4. Choose option: Provide CVE manually OR skip

**Expected Result:**
- ⚠️ Warning: "No CVE ID found in ticket TEST-004"
- ⚠️ Prompt: "Please provide CVE ID manually, or type 'skip':"
- ✅ If manual CVE provided: Added as primary CVE
- ✅ If skip: Continue with empty CVE list
- ✅ Warning logged

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-009: Extract All Custom Fields
**Objective:** Extract affected systems metadata from custom fields

**Test Ticket:** TEST-005 (or actual ticket ID: _____________)

**Ticket Data (Custom Fields):**
```json
{
  "customfield_10001": "CVE-2024-7777",
  "customfield_10002": "web-server-prod-01, db-server-prod-02",
  "customfield_10003": "Critical",
  "customfield_10004": "Internet-Facing"
}
```

**Expected Result:**
- ✅ CVE ID: CVE-2024-7777
- ✅ Affected Systems: [web-server-prod-01, db-server-prod-02]
- ✅ Asset Criticality: Critical
- ✅ System Exposure: Internet-Facing
- ✅ All fields displayed in summary

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-010: Invalid Ticket ID
**Objective:** Handle non-existent ticket gracefully

**Steps:**
1. Execute task
2. Provide ticket ID: INVALID-9999

**Expected Result:**
- ❌ Error: "Ticket INVALID-9999 not found. Verify ticket ID."
- ❌ Task halts or prompts for retry
- ✅ No stack traces exposed

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-011: JIRA Authentication Failure
**Objective:** Handle MCP authentication errors

**Setup:** Temporarily misconfigure MCP credentials (or test with invalid cloud_id)

**Expected Result:**
- ❌ Error: "JIRA authentication failed. Check MCP configuration."
- ✅ Guidance provided to user
- ✅ No credentials exposed in error message

**Cleanup:** Restore valid MCP configuration

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-012: Network Connection Error
**Objective:** Handle network failures gracefully

**Setup:** Simulate network disconnect or timeout

**Expected Result:**
- ❌ Error: "Cannot connect to JIRA. Check network connection."
- ✅ Retry option offered
- ✅ Graceful degradation

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-013: Rate Limiting (429 Response)
**Objective:** Handle JIRA rate limit responses

**Setup:** Trigger rate limit (may require multiple rapid requests)

**Expected Result:**
- ⚠️ Warning: "JIRA rate limit reached. Waiting 60 seconds before retry..."
- ✅ Exponential backoff implemented
- ✅ Retry succeeds after wait period

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-014: Data Structure Output Validation
**Objective:** Verify correct data structure returned

**Test Ticket:** Any valid ticket with complete data

**Expected Output Structure:**
```yaml
ticket_id: "TEST-001"
summary: "ticket summary text"
description: "ticket description text"
cve_ids:
  primary: "CVE-2024-1234"
  all: ["CVE-2024-1234"]
affected_systems: ["system-1", "system-2"]
asset_criticality: "Critical"
system_exposure: "Internet-Facing"
priority: "High"
components: ["component-1"]
labels: ["security", "urgent"]
```

**Expected Result:**
- ✅ All fields present in returned structure
- ✅ Data types correct (arrays, strings)
- ✅ No null/undefined for required fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-015: Security - No Credential Exposure
**Objective:** Verify sensitive data not exposed in logs/errors

**Steps:**
1. Review all error messages and outputs
2. Check for presence of:
   - API tokens
   - Cloud ID in user-facing messages
   - Stack traces with file paths
   - Internal system details

**Expected Result:**
- ✅ No credentials in error messages
- ✅ No cloud_id displayed to user
- ✅ No stack traces in user-facing output
- ✅ System names limited in logging

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Test Summary

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC-001: Valid Config | ⬜ | |
| TC-002: Missing Config | ⬜ | |
| TC-003: Missing Field | ⬜ | |
| TC-004: CVE in Summary | ⬜ | |
| TC-005: CVE in Description | ⬜ | |
| TC-006: Multiple CVEs | ⬜ | |
| TC-007: Case-Insensitive | ⬜ | |
| TC-008: No CVE ID | ⬜ | |
| TC-009: Custom Fields | ⬜ | |
| TC-010: Invalid Ticket | ⬜ | |
| TC-011: Auth Failure | ⬜ | |
| TC-012: Network Error | ⬜ | |
| TC-013: Rate Limiting | ⬜ | |
| TC-014: Data Structure | ⬜ | |
| TC-015: Security Check | ⬜ | |

**Total:** 15 test cases
**Pass Rate:** __%

## Test Execution Notes

**Tester:** _______________
**Date:** _______________
**Environment:** _______________
**JIRA Instance:** _______________

**Issues Found:**
-

**Recommendations:**
-

## Acceptance Criteria Mapping

- **AC1 (Read JIRA tickets):** TC-001, TC-004, TC-005, TC-009, TC-010
- **AC2 (Extract CVE ID):** TC-004, TC-005, TC-006, TC-007
- **AC3 (Identify affected systems):** TC-009
- **AC4 (Handle missing CVE):** TC-008
- **AC5 (Process multiple CVEs):** TC-006
- **AC6 (Validate config):** TC-001, TC-002, TC-003

All acceptance criteria covered by test cases.

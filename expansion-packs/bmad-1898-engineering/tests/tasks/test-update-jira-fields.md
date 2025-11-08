# Test Cases: update-jira-fields.md

## Test Overview

This document defines test cases for the `update-jira-fields.md` task, covering field validation, JIRA integration, custom field updates, and error handling.

## Test Environment Setup

### Prerequisites

- Atlassian MCP server configured and authenticated
- JIRA test instance with custom fields configured
- `config.yaml` properly configured with test field IDs
- Valid test tickets with edit permissions

### Test Data Requirements

**Required Test Tickets (to be created by QA/PO):**

- `TEST-FIELDS-001`: Valid ticket for successful field updates
- `TEST-FIELDS-002`: Valid ticket for partial update testing
- `TEST-FIELDS-003`: Read-only ticket (for permission testing)
- `TEST-FIELDS-004`: Valid ticket for boundary value testing

**Required Custom Fields in JIRA:**

- CVE ID (text field)
- CVSS Score (number field, 1 decimal)
- EPSS Score (number field, 2 decimals)
- KEV Status (select field with options: Listed, Not Listed)
- Exploit Status (select field with options: None, PoC, Public Exploit, Active Exploitation)

**Note:** Test ticket IDs and actual field IDs must be documented before story approval. Update this section with actual values.

---

## Test Cases

### TC-001: Valid Configuration Loading

**Objective:** Verify task loads and validates field configuration correctly

**Test Data:**

```yaml
jira:
  cloud_id: 'test-cloud-id-12345'
  project_key: 'TEST'
  custom_fields:
    cvss_score:
      field_id: 'customfield_10010'
      field_type: 'number'
      min: 0.0
      max: 10.0
      decimals: 1
    epss_score:
      field_id: 'customfield_10011'
      field_type: 'number'
      min: 0.0
      max: 1.0
      decimals: 2
  priority_mapping:
    P1: 'Critical'
```

**Steps:**

1. Execute `update-jira-fields.md` task
2. Verify config file is read
3. Verify all field configurations validated

**Expected Result:**

- ✅ Config loads without errors
- ✅ All custom field definitions validated
- ✅ Task proceeds to enrichment data input

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-002: Missing Configuration File

**Objective:** Verify graceful handling when config.yaml doesn't exist

**Setup:** Temporarily rename or remove `config.yaml`

**Steps:**

1. Execute `update-jira-fields.md` task
2. Observe error message

**Expected Result:**

- ❌ Clear error: "Config file not found at expansion-packs/bmad-1898-engineering/config.yaml"
- ❌ Task halts gracefully
- ✅ No stack traces shown

**Cleanup:** Restore `config.yaml`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-003: Missing Required Field Configuration

**Objective:** Verify validation of custom field configuration

**Setup:** Remove `field_id` from cvss_score configuration

**Steps:**

1. Execute `update-jira-fields.md` task
2. Observe error message

**Expected Result:**

- ❌ Clear error: "Custom field 'cvss_score' missing required property: field_id"
- ❌ Task halts gracefully

**Cleanup:** Restore `field_id` configuration

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-004: Valid All Fields Update

**Objective:** Successfully update all custom fields with valid data

**Test Ticket:** TEST-FIELDS-001 (or actual ticket ID: **\*\***\_**\*\***)

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-001'
cve_id: 'CVE-2024-1234'
cvss:
  score: 9.8
  vector: 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'
  severity: 'Critical'
epss:
  score: 0.85432
  percentile: 0.95123
kev:
  status: 'Listed'
  date_added: '2024-01-15'
exploit_status: 'Active Exploitation'
priority_assessment: 'P1'
```

**Steps:**

1. Execute task with test enrichment data
2. Verify JIRA ticket updated
3. Check JIRA web UI for field values

**Expected Result:**

- ✅ All 6 fields updated successfully
- ✅ CVE ID: "CVE-2024-1234"
- ✅ CVSS Score: 9.8
- ✅ EPSS Score: 0.85 (rounded to 2 decimals)
- ✅ KEV Status: "Listed"
- ✅ Exploit Status: "Active Exploitation"
- ✅ Priority: "Critical"
- ✅ Success message displayed with all updated fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-005: Invalid CVSS Score - Out of Range High

**Objective:** Reject CVSS score above maximum

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
cvss:
  score: 11.5
```

**Expected Result:**

- ❌ Validation error: "Cannot update CVSS score: 11.5 is out of range (0.0-10.0)"
- ⚠️ Field skipped, other fields processed
- ✅ Task continues with remaining valid fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-006: Invalid CVSS Score - Out of Range Low

**Objective:** Reject CVSS score below minimum

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
cvss:
  score: -1.0
```

**Expected Result:**

- ❌ Validation error: "Cannot update CVSS score: -1.0 is out of range (0.0-10.0)"
- ⚠️ Field skipped
- ✅ Task continues with other fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-007: CVSS Score Rounding

**Objective:** Verify CVSS score rounded to 1 decimal place

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-001'
cvss:
  score: 7.8549
```

**Expected Result:**

- ✅ CVSS score rounded to 7.9 (1 decimal place)
- ✅ Field updated in JIRA with value 7.9
- ✅ No validation errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-008: Invalid EPSS Score - Out of Range

**Objective:** Reject EPSS score above 1.0

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
epss:
  score: 1.5
```

**Expected Result:**

- ❌ Validation error: "Cannot update EPSS score: 1.5 is out of range (0.0-1.0)"
- ⚠️ Field skipped
- ✅ Task continues with other fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-009: EPSS Score Rounding

**Objective:** Verify EPSS score rounded to 2 decimal places

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-001'
epss:
  score: 0.85678
```

**Expected Result:**

- ✅ EPSS score rounded to 0.86 (2 decimal places)
- ✅ Field updated in JIRA with value 0.86
- ✅ No validation errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-010: Invalid KEV Status

**Objective:** Reject KEV status not in allowed options

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
kev:
  status: 'Unknown'
```

**Expected Result:**

- ❌ Validation error: "Invalid KEV status: Unknown. Must be 'Listed' or 'Not Listed'"
- ⚠️ Field skipped
- ✅ Task continues with other fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-011: KEV Status - Not Listed

**Objective:** Successfully update KEV status to "Not Listed"

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-001'
kev:
  status: 'Not Listed'
```

**Expected Result:**

- ✅ KEV Status updated to "Not Listed"
- ✅ Dropdown field set correctly in JIRA
- ✅ No errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-012: Invalid Exploit Status

**Objective:** Reject exploit status not in allowed options

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
exploit_status: 'Unknown Status'
```

**Expected Result:**

- ❌ Validation error: "Invalid exploit status: Unknown Status"
- ⚠️ Field skipped
- ✅ Task continues with other fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-013: Valid Exploit Status Values

**Objective:** Verify all allowed exploit status values work

**Test Values:** "None", "PoC", "Public Exploit", "Active Exploitation"

**Steps:**

1. Test each value individually
2. Verify JIRA field updates correctly

**Expected Result:**

- ✅ All 4 allowed values update successfully
- ✅ Dropdown field shows correct value in JIRA

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-014: Invalid CVE ID Format

**Objective:** Reject CVE ID with invalid format

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
cve_id: '2024-1234'
```

**Expected Result:**

- ❌ Validation error: "Invalid CVE ID format: 2024-1234"
- ⚠️ Field skipped
- ✅ Task continues with other fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-015: Valid CVE ID Formats

**Objective:** Accept various valid CVE ID formats

**Test Values:**

- CVE-2024-1234 (4-digit year, 4-digit ID)
- CVE-2024-12345 (5-digit ID)
- CVE-2024-1234567 (7-digit ID)

**Expected Result:**

- ✅ All valid formats accepted
- ✅ CVE ID field updated in JIRA
- ✅ No validation errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-016: Invalid Priority Assessment

**Objective:** Reject priority value not in P1-P5 range

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
priority_assessment: 'P99'
```

**Expected Result:**

- ❌ Validation error: "Invalid priority: P99. Must be P1-P5"
- ⚠️ Field skipped
- ✅ Task continues with other fields

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-017: Priority Mapping

**Objective:** Verify correct mapping of P1-P5 to JIRA priority names

**Test Mappings:**

- P1 → Critical
- P2 → High
- P3 → Medium
- P4 → Low
- P5 → Trivial

**Steps:**

1. Test each priority value
2. Verify JIRA priority field updated correctly

**Expected Result:**

- ✅ All 5 priority mappings work correctly
- ✅ JIRA priority field shows correct name
- ✅ No mapping errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-018: Partial Update - Some Fields Missing

**Objective:** Update only fields with valid data, skip missing fields

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
cvss:
  score: 8.5
priority_assessment: 'P2'
```

**Expected Result:**

- ✅ CVSS Score updated: 8.5
- ✅ Priority updated: High
- ⚠️ Other fields skipped (not in input)
- ✅ Partial success message: "Updated 2 fields, skipped 4 fields (missing data)"

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-019: Partial Update - Some Fields Invalid

**Objective:** Update valid fields, skip invalid fields

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
cvss:
  score: 7.5
epss:
  score: 1.8
kev:
  status: 'Listed'
```

**Expected Result:**

- ✅ CVSS Score updated: 7.5
- ✅ KEV Status updated: Listed
- ❌ EPSS Score skipped: 1.8 out of range
- ⚠️ Partial success message: "Updated 2 fields, skipped 1 field (invalid value)"

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-020: Empty Enrichment Data

**Objective:** Handle case where no enrichment data provided

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-002'
```

**Expected Result:**

- ⚠️ Warning: "Enrichment data is incomplete. Some fields may not be updated."
- ⚠️ Message: "No valid fields to update. Skipping JIRA field update."
- ✅ Task halts gracefully without API call

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-021: Custom Field Does Not Exist

**Objective:** Handle JIRA error when custom field ID is invalid

**Setup:** Use invalid field_id in config (e.g., "customfield_99999")

**Expected Result:**

- ❌ Error: "Custom field 'customfield_99999' does not exist in JIRA project TEST"
- ✅ Help message: "Verify field ID in JIRA admin panel (Settings → Issues → Custom Fields)"
- ⚠️ Field skipped, other fields continue

**Cleanup:** Restore valid field_id

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-022: Permission Denied - Edit Forbidden

**Objective:** Handle JIRA permission errors gracefully

**Test Ticket:** TEST-FIELDS-003 (read-only ticket)

**Expected Result:**

- ❌ Error: "Cannot update fields in TEST-FIELDS-003. Edit permission denied."
- ✅ Help message: "Check JIRA user permissions for editing tickets"
- ❌ Task returns failure status
- ✅ No fields updated

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-023: Ticket Not Found

**Objective:** Handle non-existent ticket ID

**Enrichment Input Data:**

```yaml
ticket_id: 'INVALID-9999'
cvss:
  score: 8.0
```

**Expected Result:**

- ❌ Error: "Ticket INVALID-9999 not found. Verify ticket ID and try again."
- ❌ Task halts
- ✅ No stack traces shown

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-024: Rate Limiting (429 Response)

**Objective:** Handle JIRA rate limit responses with retry logic

**Setup:** Trigger rate limit (may require multiple rapid requests)

**Expected Result:**

- ⚠️ Warning: "JIRA rate limit reached. Waiting 60 seconds before retry..."
- ✅ Exponential backoff: 60s, 120s, 240s
- ✅ Max 3 retries attempted
- ✅ Retry succeeds after wait period OR graceful failure after max retries

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-025: Network Connection Error

**Objective:** Handle network failures gracefully

**Setup:** Simulate network disconnect or timeout

**Expected Result:**

- ❌ Error: "Cannot connect to JIRA. Check network connection and try again."
- ✅ Retry once after 30 seconds
- ✅ Graceful failure if retry fails

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-026: Verify Field Values in JIRA UI

**Objective:** Confirm updated fields are visible and correct in JIRA

**Test Ticket:** TEST-FIELDS-001 (after successful update)

**Steps:**

1. Execute task with valid enrichment data
2. Open ticket in JIRA web UI
3. Verify each custom field shows correct value

**Expected Result:**

- ✅ CVE ID field shows correct value
- ✅ CVSS Score field shows correct decimal value
- ✅ EPSS Score field shows correct decimal value
- ✅ KEV Status dropdown shows correct selection
- ✅ Exploit Status dropdown shows correct selection
- ✅ Priority shows correct value

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-027: JQL Query Using Updated Fields

**Objective:** Verify updated fields can be used in JIRA queries

**Steps:**

1. Update ticket with CVSS score 9.8
2. Create JQL query: `project = TEST AND "CVSS Score" >= 9.0`
3. Verify ticket appears in results

**Expected Result:**

- ✅ JQL query executes successfully
- ✅ Updated ticket appears in query results
- ✅ Custom fields are queryable

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-028: Boundary Values - CVSS Min/Max

**Objective:** Test boundary values for CVSS score

**Test Values:**

- 0.0 (minimum)
- 10.0 (maximum)
- 5.0 (middle)

**Expected Result:**

- ✅ All boundary values accepted
- ✅ Fields updated correctly in JIRA
- ✅ No validation errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-029: Boundary Values - EPSS Min/Max

**Objective:** Test boundary values for EPSS score

**Test Values:**

- 0.0 (minimum)
- 1.0 (maximum)
- 0.5 (middle)

**Expected Result:**

- ✅ All boundary values accepted
- ✅ Fields updated correctly in JIRA
- ✅ No validation errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-030: Security - No Credential Exposure

**Objective:** Verify sensitive data not exposed in logs/errors

**Steps:**

1. Review all error messages and outputs
2. Check for presence of:
   - API tokens
   - Cloud ID in user-facing messages
   - Stack traces with file paths
   - Internal field IDs in error messages

**Expected Result:**

- ✅ No credentials in error messages
- ✅ No cloud_id displayed to user
- ✅ No stack traces in user-facing output
- ✅ Field IDs only in admin/debug context

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-031: Audit Log Entry

**Objective:** Verify audit logging for field updates

**Steps:**

1. Execute successful field update
2. Check audit log output

**Expected Log Format:**

```
{timestamp} - Ticket {ticket_id} - Updated {n} fields: {field_list}
```

**Expected Result:**

- ✅ Audit log entry created
- ✅ Timestamp included
- ✅ Ticket ID logged
- ✅ Field count and list logged

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-032: Dropdown Field Format Validation

**Objective:** Verify correct dropdown field format sent to JIRA

**Enrichment Input Data:**

```yaml
ticket_id: 'TEST-FIELDS-001'
kev:
  status: 'Listed'
```

**Expected JIRA Payload:**

```yaml
fields:
  customfield_10012: { value: 'Listed' }
```

**Expected Result:**

- ✅ Dropdown field uses object format with "value" property
- ✅ JIRA accepts the field update
- ✅ No format errors

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Test Summary

| Test Case                      | Status | Notes |
| ------------------------------ | ------ | ----- |
| TC-001: Valid Config           | ⬜     |       |
| TC-002: Missing Config         | ⬜     |       |
| TC-003: Missing Field Config   | ⬜     |       |
| TC-004: All Fields Valid       | ⬜     |       |
| TC-005: Invalid CVSS High      | ⬜     |       |
| TC-006: Invalid CVSS Low       | ⬜     |       |
| TC-007: CVSS Rounding          | ⬜     |       |
| TC-008: Invalid EPSS           | ⬜     |       |
| TC-009: EPSS Rounding          | ⬜     |       |
| TC-010: Invalid KEV Status     | ⬜     |       |
| TC-011: KEV Not Listed         | ⬜     |       |
| TC-012: Invalid Exploit Status | ⬜     |       |
| TC-013: Valid Exploit Values   | ⬜     |       |
| TC-014: Invalid CVE Format     | ⬜     |       |
| TC-015: Valid CVE Formats      | ⬜     |       |
| TC-016: Invalid Priority       | ⬜     |       |
| TC-017: Priority Mapping       | ⬜     |       |
| TC-018: Partial - Missing      | ⬜     |       |
| TC-019: Partial - Invalid      | ⬜     |       |
| TC-020: Empty Data             | ⬜     |       |
| TC-021: Field Not Exist        | ⬜     |       |
| TC-022: Permission Denied      | ⬜     |       |
| TC-023: Ticket Not Found       | ⬜     |       |
| TC-024: Rate Limiting          | ⬜     |       |
| TC-025: Network Error          | ⬜     |       |
| TC-026: Verify JIRA UI         | ⬜     |       |
| TC-027: JQL Query              | ⬜     |       |
| TC-028: CVSS Boundaries        | ⬜     |       |
| TC-029: EPSS Boundaries        | ⬜     |       |
| TC-030: Security Check         | ⬜     |       |
| TC-031: Audit Log              | ⬜     |       |
| TC-032: Dropdown Format        | ⬜     |       |

**Total:** 32 test cases
**Pass Rate:** \_\_%

## Test Execution Notes

**Tester:** **\*\***\_\_\_**\*\***
**Date:** **\*\***\_\_\_**\*\***
**Environment:** **\*\***\_\_\_**\*\***
**JIRA Instance:** **\*\***\_\_\_**\*\***

## **Issues Found:**

## **Recommendations:**

## Acceptance Criteria Mapping

- **AC1 (Update custom fields via MCP):** TC-004, TC-021, TC-026
- **AC2 (CVSS score field):** TC-004, TC-005, TC-006, TC-007, TC-028
- **AC3 (EPSS score field):** TC-004, TC-008, TC-009, TC-029
- **AC4 (KEV status dropdown):** TC-004, TC-010, TC-011, TC-032
- **AC5 (Priority field):** TC-004, TC-016, TC-017
- **AC6 (CVE ID field):** TC-004, TC-014, TC-015

All acceptance criteria covered by test cases.

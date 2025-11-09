# Test Cases: investigate-event-alert.md

## Test Overview

This document defines test cases for the `investigate-event-alert.md` task, covering alert type detection, systematic investigation workflow, disposition determination, documentation generation, and error handling.

## Test Environment Setup

### Prerequisites

- Atlassian MCP server configured and authenticated
- Perplexity MCP server configured (optional for threat intelligence)
- JIRA test instance or test tickets available
- `config.yaml` properly configured with test values

### Test Data Requirements

**Required Test Tickets (to be created by QA/PO):**

- `TEST-EVENT-001`: ICS Alert (Claroty platform - SSH Connection in Control Environments)
- `TEST-EVENT-002`: IDS Alert (Snort signature - Malicious Traffic)
- `TEST-EVENT-003`: SIEM Alert (Splunk correlation rule - Multiple Failed Logins)
- `TEST-EVENT-004`: Event alert with complete metadata and evidence
- `TEST-EVENT-005`: Event alert with missing source IP
- `TEST-EVENT-006`: Event alert with no logs available
- `TEST-EVENT-007`: Ambiguous alert type (requires manual classification)

**Note:** Test ticket IDs must be documented before story approval. Update this section with actual ticket IDs.

---

## Test Cases

### TC-001: ICS Alert Type Detection (Claroty Platform)

**Objective:** Verify automatic detection of ICS alert from ticket metadata

**Test Ticket:** TEST-EVENT-001 (or actual ticket ID: ****\_****)

**Ticket Data:**

```
Issue Type: Event Alert
Summary: "Claroty Alert: SSH Connection in Control Environments (#317)"
Description: "ICS security platform Claroty detected unauthorized SSH connection from enterprise network to PLC in control zone..."
```

**Steps:**

1. Execute `investigate-event-alert.md` task
2. Provide ticket ID: TEST-EVENT-001
3. Verify alert type auto-detection

**Expected Result:**

- ✅ Alert platform type detected: ICS
- ✅ Alert platform: Claroty
- ✅ Workflow proceeds to Stage 2 without manual classification
- ✅ ICS-specific context applied (zones, asset types)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-002: IDS Alert Type Detection (Snort Signature)

**Objective:** Verify automatic detection of IDS alert from ticket content

**Test Ticket:** TEST-EVENT-002 (or actual ticket ID: ****\_****)

**Ticket Data:**

```
Issue Type: Event Alert
Summary: "Snort Alert [1:12345:6]: ET EXPLOIT Known Malicious Traffic"
Description: "IDS detected suspicious traffic pattern. SID: 12345..."
```

**Steps:**

1. Execute task
2. Provide ticket ID: TEST-EVENT-002
3. Verify alert type detection

**Expected Result:**

- ✅ Alert platform type detected: IDS
- ✅ Alert platform: Snort
- ✅ Signature ID extracted: 1:12345:6
- ✅ Workflow proceeds without manual classification

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-003: SIEM Alert Type Detection (Splunk Correlation Rule)

**Objective:** Verify automatic detection of SIEM correlation alert

**Test Ticket:** TEST-EVENT-003 (or actual ticket ID: ****\_****)

**Ticket Data:**

```
Issue Type: Event Alert
Summary: "Splunk Notable: Multiple Failed Logins Followed by Success (UC-AUTH-001)"
Description: "SIEM correlation rule detected 15 failed login attempts from 192.168.1.100 to DC01 followed by successful authentication..."
```

**Steps:**

1. Execute task
2. Provide ticket ID: TEST-EVENT-003
3. Verify alert type detection

**Expected Result:**

- ✅ Alert platform type detected: SIEM
- ✅ Alert platform: Splunk
- ✅ Correlation rule ID extracted: UC-AUTH-001
- ✅ Workflow proceeds without manual classification

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-004: Ambiguous Alert Type (Manual Classification)

**Objective:** Handle ambiguous alerts requiring manual classification

**Test Ticket:** TEST-EVENT-007 (or actual ticket ID: ****\_****)

**Ticket Data:**

```
Issue Type: Event Alert
Summary: "Suspicious Network Activity Detected"
Description: "Security team flagged unusual traffic patterns..."
```

**Steps:**

1. Execute task
2. Provide ticket ID: TEST-EVENT-007
3. Observe prompt for manual classification
4. Select option: "1. ICS/SCADA Alert"

**Expected Result:**

- ⚠️ Warning: "Unable to auto-detect alert type"
- ✅ Prompt displayed: "Please select: 1. ICS/SCADA Alert, 2. IDS/IPS Alert, 3. SIEM Correlation Alert"
- ✅ User selection accepted
- ✅ Workflow proceeds with manual classification

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-005: Complete Investigation Workflow (All Stages)

**Objective:** Execute full investigation workflow from triage to JIRA update

**Test Ticket:** TEST-EVENT-004 (or actual ticket ID: ****\_****)

**Ticket Data:**

```
Issue Type: Event Alert
Summary: "Claroty Alert: Unauthorized Modbus Communication"
Alert Severity: High
Source IP: 10.50.1.100
Destination IP: 10.10.5.25
Protocol: Modbus TCP
Port: 502
```

**Steps:**

1. Execute task with TEST-EVENT-004
2. Provide all required inputs:
   - Alert type: Auto-detected (ICS)
   - Log evidence: Provide sample Modbus logs
   - Correlated events: None
   - Historical context: First occurrence
   - Protocol expected: No (maintenance window closed)
   - Asset function: SCADA HMI
   - Business impact: Production line control
   - Disposition: True Positive
   - Confidence: High
   - Next actions: Escalate to IR team
3. Verify all stages complete

**Expected Result:**

- ✅ Stage 1 (Triage): Alert type detected
- ✅ Stage 2 (Metadata): All metadata collected
- ✅ Stage 3 (Network Identifiers): IPs, protocol, port documented
- ✅ Stage 4 (Evidence): Logs collected
- ✅ Stage 5 (Technical Analysis): Protocol validated, attack vector identified
- ✅ Stage 6 (Disposition): TP with High confidence
- ✅ Stage 7 (Documentation): Investigation document generated
- ✅ JIRA comment posted
- ✅ JIRA fields updated
- ✅ Local file saved
- ✅ Completion summary displayed

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-006: True Positive Disposition (High Confidence)

**Objective:** Validate True Positive disposition determination

**Test Scenario:** Malicious SSH connection to ICS device during non-maintenance hours

**Investigation Data:**

- Alert: SSH connection from enterprise to control zone
- Evidence: Logs show non-standard SSH client, unusual commands executed
- Asset: Critical PLC controlling production line
- Historical: No previous SSH connections to this device
- Environmental: No maintenance window scheduled

**Disposition Input:**

```
Disposition: 1 (True Positive)
Confidence: High
Reasoning: "Unauthorized SSH access to critical PLC. No legitimate business need for SSH to this device. Commands executed indicate reconnaissance activity. High confidence this is malicious."
Next Actions: "1. Isolate PLC from network, 2. Escalate to IR team, 3. Review authentication logs"
```

**Expected Result:**

- ✅ Disposition: True Positive
- ✅ Confidence: High
- ✅ Escalation decision: Escalate
- ✅ Containment required: Yes
- ✅ Reasoning documented with evidence
- ✅ Next actions specific and actionable

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-007: False Positive Disposition (With Tuning Recommendation)

**Objective:** Validate False Positive disposition with tuning guidance

**Test Scenario:** Legitimate backup traffic flagged as suspicious

**Investigation Data:**

- Alert: Large data transfer to external IP
- Evidence: Logs show scheduled backup to cloud provider
- Asset: Database server with configured backup solution
- Historical: Daily occurrence at same time
- Environmental: Backup window 02:00-04:00 daily

**Disposition Input:**

```
Disposition: 2 (False Positive)
Confidence: High
Reasoning: "Alert triggered on legitimate scheduled backup traffic to known cloud backup provider (AWS S3). Traffic occurs daily during maintenance window. Verified destination IP belongs to backup service."
Tuning: "Whitelist backup destination IP range (52.x.x.x/16) for this source during backup window 02:00-04:00."
```

**Expected Result:**

- ✅ Disposition: False Positive
- ✅ Confidence: High
- ✅ Escalation decision: Tune
- ✅ Tuning recommendations specific
- ✅ Reasoning explains why alert is benign
- ✅ No containment required

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-008: Benign True Positive Disposition (Authorized Activity)

**Objective:** Validate BTP disposition for authorized but detected activity

**Test Scenario:** Authorized vulnerability scan detected by IDS

**Investigation Data:**

- Alert: Port scanning activity detected
- Evidence: Logs show scan from known vulnerability scanner IP
- Asset: Multiple servers scanned
- Historical: Monthly occurrence
- Environmental: Authorized Nessus scan scheduled by Security team

**Disposition Input:**

```
Disposition: 3 (Benign True Positive)
Confidence: High
Reasoning: "Alert correctly detected port scanning activity. Activity is authorized quarterly vulnerability scan by Security team using Nessus scanner (10.5.1.50). Change request CHG-2024-1234 approved scan window."
Tuning: "Consider adding scanner IP to whitelist or adjusting alert sensitivity during scheduled scan windows."
```

**Expected Result:**

- ✅ Disposition: Benign True Positive
- ✅ Confidence: High
- ✅ Escalation decision: Tune/Close
- ✅ Reasoning documents authorized nature
- ✅ Tuning recommendation provided
- ✅ No escalation required

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-009: Missing Evidence Handling (Incomplete Logs)

**Objective:** Handle incomplete evidence collection gracefully

**Test Scenario:** Alert investigation with no log access

**Steps:**

1. Execute task
2. During evidence collection:
   - Log sources: "Firewall, IDS"
   - Log excerpts: "none" (logs not accessible)
   - Correlated events: "none"
   - Historical context: "none"

**Expected Result:**

- ⚠️ Warning: "No logs collected - investigation incomplete"
- ✅ Workflow continues with available data
- ✅ Evidence gaps documented in report
- ✅ Quality score reflects missing evidence
- ⚠️ Low confidence recommended or escalation suggested
- ✅ Investigation document includes warning about evidence limitations

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-010: Missing Source IP (Required Field)

**Objective:** Handle missing critical network identifier

**Test Ticket:** TEST-EVENT-005 (or actual ticket ID: ****\_****)

**Ticket Data:**

```
Issue Type: Event Alert
Summary: "IDS Alert: Suspicious Activity"
Description: "Alert detected but source IP not captured"
```

**Steps:**

1. Execute task
2. Observe prompt for missing source IP
3. Provide source IP manually: 192.168.1.100

**Expected Result:**

- ⚠️ Prompt: "Source IP not found in ticket. Please provide:"
- ✅ User input accepted
- ✅ Flag added: "⚠️ Source IP manually provided (not in ticket)"
- ✅ Workflow continues with manual data
- ✅ Gap documented in investigation report

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-011: JIRA Update Success

**Objective:** Verify successful JIRA comment and field updates

**Test Ticket:** Any valid event alert ticket

**Steps:**

1. Complete full investigation workflow
2. Verify JIRA updates

**Expected Result:**

- ✅ Investigation document posted as JIRA comment
- ✅ Custom field "Disposition" updated
- ✅ Custom field "Confidence Level" updated
- ✅ Custom field "Next Actions" updated
- ✅ Verification messages displayed: "JIRA comment posted successfully", "JIRA fields updated"
- ✅ Comment ID returned from MCP tool

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-012: JIRA Update Failure (Retry Logic)

**Objective:** Verify retry logic for transient JIRA failures

**Setup:** Simulate network interruption or JIRA timeout

**Steps:**

1. Complete investigation workflow
2. Trigger JIRA connection failure during update
3. Observe retry behavior

**Expected Result:**

- ⏳ First failure: "JIRA update failed. Retrying in 5 seconds..."
- ⏳ Second failure: "Retry failed. Waiting 15 seconds..."
- ⏳ Third failure: "JIRA update failed after 3 attempts."
- ✅ Investigation saved locally
- ✅ Manual posting instructions provided
- ✅ File path displayed for manual copy

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-013: Invalid Ticket ID

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

### TC-014: Wrong Issue Type (CVE Ticket)

**Objective:** Detect wrong workflow for vulnerability tickets

**Test Ticket:** Ticket with Issue Type "Security Vulnerability"

**Steps:**

1. Execute task
2. Provide CVE vulnerability ticket ID
3. Observe guidance message

**Expected Result:**

- ⚠️ Warning: "This appears to be a CVE vulnerability ticket"
- ✅ Guidance: "Use *enrich-ticket command for CVE enrichment instead"
- ❌ Task halts with recommendation
- ✅ No attempt to process as event alert

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-015: Missing Alert Severity

**Objective:** Handle missing severity with default

**Steps:**

1. Execute task with ticket missing severity field
2. Verify default assignment

**Expected Result:**

- ⚠️ Warning: "Alert severity not found in ticket"
- ✅ Default severity: "Medium"
- ✅ Flag added: "⚠️ Severity defaulted to Medium"
- ✅ Workflow continues

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-016: Missing Detection Timestamp

**Objective:** Use fallback timestamp when detection time unavailable

**Steps:**

1. Execute task with ticket missing detection timestamp
2. Verify fallback logic

**Expected Result:**

- ⚠️ Warning: "Detection timestamp not found"
- ✅ Fallback: Ticket creation time used
- ✅ Note added: "Detection time unavailable, using ticket creation time"
- ✅ Workflow continues

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-017: Template Processing Success

**Objective:** Verify investigation document generation from template

**Steps:**

1. Complete investigation with all data collected
2. Verify document generation

**Expected Result:**

- ✅ Template loaded: `event-investigation-tmpl.yaml`
- ✅ All 12 sections populated
- ✅ Variable substitution successful
- ✅ Markdown document generated
- ✅ Document filename: `{ticket-id}-event-investigation-{timestamp}.md`
- ✅ All required fields present (no empty sections)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-018: Template Missing (Error Handling)

**Objective:** Handle missing template file gracefully

**Setup:** Temporarily rename `event-investigation-tmpl.yaml`

**Expected Result:**

- ❌ Error: "Template not found: event-investigation-tmpl.yaml"
- ❌ Task halts at Stage 7
- ✅ Investigation data preserved
- ✅ Guidance: "Check template file exists in templates/ directory"

**Cleanup:** Restore template file

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-019: Local File Save Success

**Objective:** Verify investigation document saved locally

**Steps:**

1. Complete full investigation workflow
2. Verify local file creation

**Expected Result:**

- ✅ Directory created: `artifacts/enrichments/` (if not exists)
- ✅ File saved: `artifacts/enrichments/{ticket-id}-event-investigation-{timestamp}.md`
- ✅ File contains complete investigation document
- ✅ Success message: "Investigation saved to: {filepath}"

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-020: Local File Save Failure

**Objective:** Handle file system errors during save

**Setup:** Make `artifacts/` directory read-only

**Expected Result:**

- ❌ Error: "Failed to save investigation document locally"
- ❌ Task halts (critical for audit trail)
- ✅ Specific error reason provided
- ✅ Guidance: "Check file system permissions for artifacts/ directory"

**Cleanup:** Restore directory permissions

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-021: Quality Validation (High Quality Score)

**Objective:** Verify quality validation for complete investigation

**Steps:**

1. Complete investigation with all data points collected
2. Observe quality score calculation

**Expected Result:**

- ✅ All 12 quality checks pass
- ✅ Quality score: 100% (12/12 checks)
- ✅ No warnings displayed
- ✅ Investigation marked complete

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-022: Quality Validation (Low Quality Score Warning)

**Objective:** Display warning for incomplete investigation

**Steps:**

1. Complete investigation with missing data:
   - No logs collected
   - No correlated events
   - No historical context
   - No threat intelligence
2. Observe quality score

**Expected Result:**

- ⚠️ Quality score: 66% (8/12 checks)
- ⚠️ Warning: "Quality score below 75% - investigation incomplete"
- ⚠️ Recommendation: "Review evidence gaps before closing"
- ✅ Investigation can still proceed with warning

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-023: Optional Perplexity Threat Intelligence

**Objective:** Verify threat intelligence enhancement when Perplexity available

**Steps:**

1. Execute investigation with external IP
2. Observe Perplexity queries during technical analysis

**Expected Result:**

- ✅ Perplexity query: "Is IP {source_ip} associated with known malicious activity?"
- ✅ Threat intelligence findings included in report
- ✅ IOC analysis section populated with external data
- ✅ Sources cited in appendix

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-024: Perplexity Unavailable (Graceful Degradation)

**Objective:** Handle missing Perplexity MCP gracefully

**Setup:** Perplexity MCP not configured

**Expected Result:**

- ⚠️ Note: "Threat intelligence research skipped (Perplexity unavailable)"
- ✅ Investigation continues with manual analysis only
- ✅ No errors thrown
- ✅ Quality score not impacted

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-025: Security - No Credential Exposure

**Objective:** Verify sensitive data not exposed in logs/errors

**Steps:**

1. Review all error messages and outputs
2. Check for presence of:
   - API tokens
   - Cloud ID in user-facing messages
   - Stack traces with file paths
   - Internal IP addresses in public errors

**Expected Result:**

- ✅ No credentials in error messages
- ✅ No cloud_id displayed to user
- ✅ No stack traces in user-facing output
- ✅ Internal IPs only in investigation document (not errors)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-026: Disposition Low Confidence Auto-Escalation

**Objective:** Verify automatic escalation recommendation for low confidence

**Steps:**

1. Complete investigation
2. Select Low confidence level for disposition

**Expected Result:**

- ⚠️ Warning: "Low confidence disposition - escalation recommended"
- ✅ Escalation decision defaulted to: "Escalate"
- ✅ Next actions include: "Peer review required"
- ✅ Note added to investigation: "Low confidence - recommend senior analyst review"

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-027: Completion Summary Display

**Objective:** Verify completion summary formatting and content

**Steps:**

1. Complete full investigation workflow
2. Observe completion summary

**Expected Output:**

```
✅ Event Investigation Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ticket: TEST-EVENT-001
Alert: SSH Connection in Control Environments
Platform: Claroty (ICS)
Disposition: True Positive (Confidence: High)
Next Actions: Escalate to IR team, Isolate PLC
Duration: 18m 45s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Investigation saved to: artifacts/enrichments/TEST-EVENT-001-event-investigation-20251109-143022.md
JIRA ticket updated successfully.
```

**Expected Result:**

- ✅ All key information displayed
- ✅ Clean formatting with separators
- ✅ File path shown
- ✅ JIRA update confirmation
- ✅ Duration calculated and displayed

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Test Summary

| Test Case                                | Status | Notes |
| ---------------------------------------- | ------ | ----- |
| TC-001: ICS Alert Detection              | ⬜     |       |
| TC-002: IDS Alert Detection              | ⬜     |       |
| TC-003: SIEM Alert Detection             | ⬜     |       |
| TC-004: Ambiguous Alert Type             | ⬜     |       |
| TC-005: Complete Workflow                | ⬜     |       |
| TC-006: True Positive Disposition        | ⬜     |       |
| TC-007: False Positive Disposition       | ⬜     |       |
| TC-008: Benign True Positive             | ⬜     |       |
| TC-009: Missing Evidence Handling        | ⬜     |       |
| TC-010: Missing Source IP                | ⬜     |       |
| TC-011: JIRA Update Success              | ⬜     |       |
| TC-012: JIRA Update Failure              | ⬜     |       |
| TC-013: Invalid Ticket ID                | ⬜     |       |
| TC-014: Wrong Issue Type                 | ⬜     |       |
| TC-015: Missing Alert Severity           | ⬜     |       |
| TC-016: Missing Detection Timestamp      | ⬜     |       |
| TC-017: Template Processing Success      | ⬜     |       |
| TC-018: Template Missing                 | ⬜     |       |
| TC-019: Local File Save Success          | ⬜     |       |
| TC-020: Local File Save Failure          | ⬜     |       |
| TC-021: Quality Validation (High)        | ⬜     |       |
| TC-022: Quality Validation (Low Warning) | ⬜     |       |
| TC-023: Perplexity Threat Intel          | ⬜     |       |
| TC-024: Perplexity Unavailable           | ⬜     |       |
| TC-025: Security Check                   | ⬜     |       |
| TC-026: Low Confidence Auto-Escalation   | ⬜     |       |
| TC-027: Completion Summary Display       | ⬜     |       |

**Total:** 27 test cases
**Pass Rate:** **%

## Test Execution Notes

**Tester:** ******\_\_\_******
**Date:** ******\_\_\_******
**Environment:** ******\_\_\_******
**JIRA Instance:** ******\_\_\_******

## **Issues Found:**

## **Recommendations:**

## Acceptance Criteria Mapping

- **AC1 (Accept event investigation command with ticket-id):** TC-001, TC-002, TC-003, TC-005, TC-013
- **AC2 (Detect event alert type from ticket metadata):** TC-001, TC-002, TC-003, TC-004, TC-014
- **AC3 (Perform systematic investigation):** TC-005, TC-009, TC-010, TC-021, TC-022
- **AC4 (Determine disposition with evidence-based reasoning):** TC-005, TC-006, TC-007, TC-008, TC-026
- **AC5 (Generate structured event investigation document):** TC-005, TC-017, TC-018, TC-019
- **AC6 (Update JIRA ticket with findings):** TC-011, TC-012
- **AC7 (Handle errors gracefully):** TC-004, TC-009, TC-010, TC-012, TC-013, TC-015, TC-016, TC-018, TC-020

All acceptance criteria covered by test cases.

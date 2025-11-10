# Epic 7 Test Plan: Security Event Investigation Review Capability

## Document Information

| Field | Value |
|-------|-------|
| **Test Plan ID** | TP-EPIC-7-001 |
| **Version** | 1.0 |
| **Created Date** | 2025-11-09 |
| **Author** | QA Engineer |
| **Story Reference** | Story 7.8: Epic 7 Testing and Validation |
| **Epic** | Epic 7: Security Event Investigation Review Capability |

## 1. Test Scope

### 1.1 In Scope

**Agent Workflows:**
- Security Analyst event investigation workflow (`*investigate-event` command)
- Security Reviewer event review workflow (`*review-enrichment` command with event investigations)
- Auto-detection logic for ICS/IDS/SIEM/CVE ticket types

**Quality Framework:**
- 7 event investigation quality checklists:
  - Investigation Completeness Checklist
  - Investigation Technical Accuracy Checklist
  - Disposition Reasoning Checklist
  - Investigation Contextualization Checklist
  - Investigation Methodology Checklist
  - Investigation Documentation Quality Checklist
  - Investigation Cognitive Bias Checklist

**Templates:**
- Event investigation review report template (`security-event-investigation-review-report-tmpl.yaml`)

**Capabilities:**
- Disposition agreement/disagreement tracking
- Fact verification for event claims (IP ownership, geolocation, threat intelligence)
- Weighted scoring calculation (Completeness 25%, Accuracy 20%, Disposition Reasoning 20%, etc.)
- Quality classification (Excellent/Good/Needs Improvement/Inadequate)

**Regression Testing:**
- CVE enrichment workflow (no changes expected)
- CVE review workflow (no changes expected)

### 1.2 Out of Scope

- Full incident response playbook testing (separate epic)
- Performance optimization (if targets not met, defer to future story)
- UI/UX improvements (command-line interface only)
- Multi-user collaboration workflows
- Advanced threat hunting capabilities

## 2. Test Objectives

### 2.1 Primary Objectives

1. **Validate End-to-End Workflow**: Confirm security analysts can investigate event alerts and reviewers can provide systematic quality feedback using real JIRA tickets
2. **Verify Auto-Detection Accuracy**: Ensure ticket type detection correctly identifies ICS/IDS/SIEM/CVE tickets with 95%+ accuracy
3. **Confirm Checklist Execution**: Validate all 7 event investigation checklists execute correctly and produce accurate scores
4. **Test Disposition Handling**: Verify disposition agreement and disagreement scenarios work correctly
5. **Validate Fact Verification**: Confirm IP ownership, geolocation, and threat intelligence lookups return accurate results
6. **Ensure No Regression**: Verify existing CVE enrichment and review workflows remain unchanged

### 2.2 Secondary Objectives

1. **Performance Validation**: Confirm event investigation completes in 10-15 minutes and review completes in 15-20 minutes
2. **Integration Validation**: Test JIRA Atlassian MCP and Perplexity MCP integrations
3. **Error Handling**: Validate graceful handling of MCP failures (timeouts, connection errors)

## 3. Test Approach

### 3.1 Testing Strategy

**Manual End-to-End Testing**:
- Execute workflows manually using agent commands in IDE environment
- Use real JIRA tickets (AOD-4052) for authentic validation
- Document all steps, timestamps, and outcomes
- Capture logs and generated documents for evidence

**Test Data Strategy**:
- **Real JIRA Ticket**: AOD-4052 (ICS Alert - Claroty SSH Connection) for primary end-to-end test
- **Mock Test Tickets**: Create mock ticket data for IDS, SIEM, and CVE scenarios
- **Mock Investigations**: Prepare sample investigations at different quality levels (Excellent, Good, Needs Improvement, Inadequate)

**Validation Methods**:
- **Functional Validation**: Verify commands execute successfully and produce expected outputs
- **Accuracy Validation**: Manually verify checklist scores, disposition reasoning, and fact verification results
- **Performance Validation**: Measure execution duration for investigation and review workflows
- **Regression Validation**: Test existing CVE workflows to ensure no breakage

### 3.2 Test Environment

**Environment Components**:
- IDE: Cursor/VS Code/Claude Code with BMad agents loaded
- JIRA: Atlassian JIRA MCP server (production instance or test environment)
- Perplexity: Perplexity MCP for fact verification
- Test Data: `expansion-packs/bmad-1898-engineering/tests/test-data/`

**Prerequisites**:
- JIRA MCP server configured and accessible
- Perplexity MCP server configured and accessible
- Security analyst and reviewer agents loaded in IDE
- Real JIRA ticket AOD-4052 accessible
- Test data files prepared in test-data directory

### 3.3 Test Execution Process

1. **Preparation Phase**: Create test plan, prepare test data, set up environment
2. **Execution Phase**: Execute test scenarios sequentially, document results
3. **Validation Phase**: Verify outputs against expected results, measure performance
4. **Reporting Phase**: Document findings, identify defects, provide pass/fail status

## 4. Test Scenarios

### 4.1 Scenario 1: ICS Alert Investigation (AOD-4052)

**Test ID**: TS-EPIC7-001
**Priority**: Critical
**Type**: End-to-end functional test

**Objective**: Validate security analyst can investigate ICS alert and generate complete investigation document

**Test Data**:
- **Ticket**: AOD-4052 (Claroty ICS Alert - SSH Connection in Control Environments)
- **Expected Disposition**: False Positive (authorized maintenance)

**Preconditions**:
- Security analyst agent loaded
- JIRA MCP connected
- Perplexity MCP connected
- Ticket AOD-4052 accessible

**Test Steps**:
1. Execute command: `*investigate-event AOD-4052`
2. Validate alert metadata extraction (alert type, severity, source system)
3. Validate network identifier parsing (source IP, destination IP, ports)
4. Validate timeline construction (alert trigger time, detection time)
5. Validate disposition determination (TP/FP/BTP with reasoning)
6. Validate investigation document generation (completeness, format)
7. Validate JIRA update (comment added, custom fields updated)

**Expected Results**:
- Investigation completes in 10-15 minutes
- Disposition: False Positive with clear reasoning (authorized maintenance activity)
- Investigation document contains all required sections (Alert Overview, Network Identifiers, Timeline, Evidence, Disposition)
- JIRA ticket updated with investigation comment and custom fields
- No errors or exceptions during execution

**Pass Criteria**: All expected results met

---

### 4.2 Scenario 2: IDS Alert Investigation

**Test ID**: TS-EPIC7-002
**Priority**: High
**Type**: Functional test

**Objective**: Validate security analyst can investigate IDS alert with True Positive disposition

**Test Data**:
- **Ticket**: Mock IDS Alert (Snort Alert - ET EXPLOIT Known Malicious Traffic)
- **Expected Disposition**: True Positive (confirmed exploit attempt)

**Preconditions**:
- Mock IDS ticket created in `tests/test-data/ids-alert-snort-exploit.json`
- Security analyst agent loaded

**Test Steps**:
1. Execute command: `*investigate-event {mock-ticket-id}`
2. Validate signature-based detection analysis
3. Validate exploit identification and severity assessment
4. Validate evidence collection (packet capture references, log excerpts)
5. Validate True Positive disposition with escalation recommendation

**Expected Results**:
- Disposition: True Positive with evidence-based reasoning
- Escalation recommendation included
- Investigation includes exploit context and impact assessment

**Pass Criteria**: All expected results met

---

### 4.3 Scenario 3: SIEM Alert Investigation

**Test ID**: TS-EPIC7-003
**Priority**: High
**Type**: Functional test

**Objective**: Validate security analyst can investigate SIEM correlation rule alert with Benign True Positive disposition

**Test Data**:
- **Ticket**: Mock SIEM Alert (Splunk Notable - Multiple Failed Logins Followed by Success)
- **Expected Disposition**: Benign True Positive (user password change)

**Preconditions**:
- Mock SIEM ticket created in `tests/test-data/siem-alert-splunk-logins.json`
- Security analyst agent loaded

**Test Steps**:
1. Execute command: `*investigate-event {mock-ticket-id}`
2. Validate correlation rule analysis
3. Validate alternative explanations considered (password change, user error, etc.)
4. Validate confidence level stated (high/medium/low)
5. Validate Benign True Positive disposition reasoning

**Expected Results**:
- Disposition: Benign True Positive with alternative explanations considered
- Confidence level clearly stated
- Investigation acknowledges pattern matches alert but is benign behavior

**Pass Criteria**: All expected results met

---

### 4.4 Scenario 4: Event Investigation Review (Excellent Quality)

**Test ID**: TS-EPIC7-004
**Priority**: Critical
**Type**: End-to-end functional test

**Objective**: Validate security reviewer can review high-quality event investigation and produce accurate quality assessment

**Test Data**:
- **Investigation**: Mock investigation document (90%+ expected score)
- **Expected Quality**: Excellent

**Preconditions**:
- Mock excellent investigation created in `tests/test-data/investigation-excellent.md`
- Security reviewer agent loaded
- JIRA ticket with investigation comment available

**Test Steps**:
1. Execute command: `*review-enrichment {ticket-id}`
2. Validate auto-detection of event investigation type
3. Validate execution of all 7 event investigation checklists
4. Validate weighted scoring calculation (manually verify math)
5. Validate quality classification (Excellent)
6. Validate review report generation
7. Validate JIRA update with review feedback

**Expected Results**:
- Review completes in 15-20 minutes
- All 7 checklists execute successfully
- Weighted score: 90%+ (Excellent classification)
- Review report acknowledges strengths, minimal critical issues
- JIRA updated with review comment

**Pass Criteria**: All expected results met, scoring calculation verified correct

---

### 4.5 Scenario 5: Event Investigation Review (Needs Improvement)

**Test ID**: TS-EPIC7-005
**Priority**: High
**Type**: Functional test

**Objective**: Validate security reviewer can identify gaps in lower-quality investigation and provide constructive feedback

**Test Data**:
- **Investigation**: Mock investigation document (60-74% expected score)
- **Expected Quality**: Needs Improvement

**Preconditions**:
- Mock needs-improvement investigation created in `tests/test-data/investigation-needs-improvement.md`
- Security reviewer agent loaded

**Test Steps**:
1. Execute command: `*review-enrichment {ticket-id}`
2. Validate checklist execution identifies missing evidence
3. Validate checklist execution identifies weak reasoning
4. Validate weighted scoring calculation
5. Validate quality classification (Needs Improvement)
6. Validate constructive feedback provided in review report
7. Validate learning resource links included

**Expected Results**:
- Weighted score: 60-74% (Needs Improvement classification)
- Significant gaps identified (missing evidence, weak reasoning)
- Constructive feedback provided with specific improvement suggestions
- Learning resources linked (event-investigation-kb.md references)

**Pass Criteria**: All expected results met, gaps correctly identified

---

### 4.6 Scenario 6: Disposition Agreement

**Test ID**: TS-EPIC7-006
**Priority**: High
**Type**: Functional test

**Objective**: Validate reviewer disposition agreement scenario

**Test Data**:
- **Analyst Disposition**: False Positive
- **Reviewer Disposition**: Agrees (False Positive)

**Test Steps**:
1. Review investigation with FP disposition
2. Validate reviewer agrees with analyst disposition
3. Validate disposition assessment section in review report indicates agreement
4. Validate no disposition override in JIRA update

**Expected Results**:
- Disposition assessment indicates agreement
- Review report acknowledges sound reasoning for FP determination
- No disposition conflict flagged

**Pass Criteria**: Agreement scenario handled correctly

---

### 4.7 Scenario 7: Disposition Disagreement

**Test ID**: TS-EPIC7-007
**Priority**: Critical
**Type**: Functional test

**Objective**: Validate reviewer disposition disagreement scenario with detailed reasoning

**Test Data**:
- **Analyst Disposition**: False Positive
- **Reviewer Disposition**: Disagrees (True Positive)

**Test Steps**:
1. Review investigation with FP disposition that reviewer determines should be TP
2. Validate reviewer provides detailed reasoning with evidence
3. Validate disposition assessment section in review report clearly explains disagreement
4. Validate JIRA update includes disposition override with justification

**Expected Results**:
- Disposition assessment section clearly indicates disagreement
- Reviewer provides evidence-based reasoning for TP determination
- Review report explains specific gaps in analyst's FP reasoning
- JIRA updated with disposition override and detailed justification

**Pass Criteria**: Disagreement scenario handled correctly with clear reasoning

---

### 4.8 Scenario 8: Auto-Detection Logic - ICS Alert

**Test ID**: TS-EPIC7-008
**Priority**: High
**Type**: Functional test

**Objective**: Validate auto-detection correctly identifies ICS alert tickets

**Test Data**:
- **Ticket**: Issue Type = "Event Alert", contains "Claroty" keyword
- **Expected Detection**: Event investigation workflow

**Test Steps**:
1. Execute `*review-enrichment {ics-ticket-id}` (no --type parameter)
2. Validate auto-detection identifies ticket as event investigation
3. Validate event investigation review workflow executes (not CVE workflow)

**Expected Results**:
- Auto-detection identifies ICS alert correctly
- Event investigation review workflow executed
- 7 event checklists used (not CVE checklists)

**Pass Criteria**: Correct detection and workflow execution

---

### 4.9 Scenario 9: Auto-Detection Logic - IDS Alert

**Test ID**: TS-EPIC7-009
**Priority**: High
**Type**: Functional test

**Objective**: Validate auto-detection correctly identifies IDS alert tickets

**Test Data**:
- **Ticket**: Contains "Snort" or "Suricata" keywords
- **Expected Detection**: Event investigation workflow

**Test Steps**:
1. Execute `*review-enrichment {ids-ticket-id}` (no --type parameter)
2. Validate auto-detection identifies ticket as event investigation
3. Validate event investigation review workflow executes

**Expected Results**:
- Auto-detection identifies IDS alert correctly
- Event investigation review workflow executed

**Pass Criteria**: Correct detection and workflow execution

---

### 4.10 Scenario 10: Auto-Detection Logic - SIEM Alert

**Test ID**: TS-EPIC7-010
**Priority**: High
**Type**: Functional test

**Objective**: Validate auto-detection correctly identifies SIEM alert tickets

**Test Data**:
- **Ticket**: Contains "Splunk" or "QRadar" keywords
- **Expected Detection**: Event investigation workflow

**Test Steps**:
1. Execute `*review-enrichment {siem-ticket-id}` (no --type parameter)
2. Validate auto-detection identifies ticket as event investigation
3. Validate event investigation review workflow executes

**Expected Results**:
- Auto-detection identifies SIEM alert correctly
- Event investigation review workflow executed

**Pass Criteria**: Correct detection and workflow execution

---

### 4.11 Scenario 11: Auto-Detection Logic - CVE Ticket

**Test ID**: TS-EPIC7-011
**Priority**: High
**Type**: Regression test

**Objective**: Validate auto-detection correctly identifies CVE enrichment tickets (no change from pre-Epic 7)

**Test Data**:
- **Ticket**: Issue Type = "Security Vulnerability", contains CVE-ID pattern (CVE-YYYY-NNNNN)
- **Expected Detection**: CVE enrichment review workflow

**Test Steps**:
1. Execute `*review-enrichment {cve-ticket-id}` (no --type parameter)
2. Validate auto-detection identifies ticket as CVE enrichment
3. Validate CVE review workflow executes (not event workflow)

**Expected Results**:
- Auto-detection identifies CVE ticket correctly
- CVE review workflow executed
- CVE-specific checklists used (not event checklists)

**Pass Criteria**: Correct detection and workflow execution (regression pass)

---

### 4.12 Scenario 12: Auto-Detection Logic - Ambiguous Ticket

**Test ID**: TS-EPIC7-012
**Priority**: Medium
**Type**: Functional test

**Objective**: Validate auto-detection prompts user to select type when ticket is ambiguous

**Test Data**:
- **Ticket**: No clear indicators (no CVE-ID, no ICS/IDS/SIEM keywords, Issue Type = "Task")
- **Expected Behavior**: Prompt user to select event or CVE type

**Test Steps**:
1. Execute `*review-enrichment {ambiguous-ticket-id}` (no --type parameter)
2. Validate system prompts user to select type
3. User selects "event" type
4. Validate event investigation review workflow executes

**Expected Results**:
- Auto-detection cannot determine type
- User prompted to select "event" or "cve"
- Workflow executes based on user selection

**Pass Criteria**: Ambiguous ticket handling works correctly

---

### 4.13 Scenario 13: Force Event Type Parameter

**Test ID**: TS-EPIC7-013
**Priority**: Medium
**Type**: Functional test

**Objective**: Validate --type=event parameter forces event investigation review

**Test Data**:
- **Ticket**: Any ticket (even CVE ticket)
- **Parameter**: --type=event

**Test Steps**:
1. Execute `*review-enrichment {ticket-id} --type=event`
2. Validate event investigation review workflow executes
3. Validate auto-detection bypassed

**Expected Results**:
- Event investigation review workflow executed
- Auto-detection logic not used
- 7 event checklists executed

**Pass Criteria**: Parameter override works correctly

---

### 4.14 Scenario 14: Force CVE Type Parameter

**Test ID**: TS-EPIC7-014
**Priority**: Medium
**Type**: Regression test

**Objective**: Validate --type=cve parameter forces CVE enrichment review

**Test Data**:
- **Ticket**: Any ticket (even event alert ticket)
- **Parameter**: --type=cve

**Test Steps**:
1. Execute `*review-enrichment {ticket-id} --type=cve`
2. Validate CVE review workflow executes
3. Validate auto-detection bypassed

**Expected Results**:
- CVE review workflow executed
- Auto-detection logic not used
- CVE-specific checklists executed

**Pass Criteria**: Parameter override works correctly (regression pass)

---

### 4.15 Scenario 15: Fact Verification - IP Ownership

**Test ID**: TS-EPIC7-015
**Priority**: High
**Type**: Functional test

**Objective**: Validate IP ownership verification using Perplexity MCP

**Test Data**:
- **IP Address**: 8.8.8.8 (Google DNS)
- **Expected Result**: ASN lookup returns Google ownership

**Test Steps**:
1. Trigger fact verification during investigation review
2. Validate Perplexity MCP called for IP ownership lookup
3. Validate ASN information returned
4. Validate source citation included in results

**Expected Results**:
- IP ownership correctly identified (Google)
- ASN information accurate
- Source cited (e.g., WHOIS database)

**Pass Criteria**: Fact verification returns accurate IP ownership

---

### 4.16 Scenario 16: Fact Verification - Geolocation

**Test ID**: TS-EPIC7-016
**Priority**: High
**Type**: Functional test

**Objective**: Validate geolocation verification using Perplexity MCP

**Test Data**:
- **IP Address**: 1.1.1.1 (Cloudflare DNS)
- **Expected Result**: Geolocation lookup returns accurate location

**Test Steps**:
1. Trigger fact verification for geolocation claim
2. Validate Perplexity MCP called for geolocation lookup
3. Validate country/region information returned
4. Validate source citation included

**Expected Results**:
- Geolocation correctly identified
- Country/region information accurate
- Source cited

**Pass Criteria**: Fact verification returns accurate geolocation

---

### 4.17 Scenario 17: Fact Verification - Threat Intelligence

**Test ID**: TS-EPIC7-017
**Priority**: High
**Type**: Functional test

**Objective**: Validate threat intelligence lookup for malicious IPs using Perplexity MCP

**Test Data**:
- **IP Address**: Known malicious IP (from threat intel feeds)
- **Expected Result**: Threat intel lookup confirms malicious activity

**Test Steps**:
1. Trigger fact verification for threat intel claim
2. Validate Perplexity MCP called for threat intel lookup
3. Validate malicious activity indicators returned
4. Validate source citation included (threat feed name)

**Expected Results**:
- Threat intelligence correctly identifies malicious IP
- Activity indicators accurate (botnet, C2, scanner, etc.)
- Source cited (VirusTotal, AbuseIPDB, etc.)

**Pass Criteria**: Fact verification returns accurate threat intel

---

### 4.18 Scenario 18: Fact Verification - Protocol/Port Validation

**Test ID**: TS-EPIC7-018
**Priority**: Medium
**Type**: Functional test

**Objective**: Validate protocol/port validation logic

**Test Data**:
- **Port**: 22 (SSH)
- **Expected Result**: Port 22 confirmed as SSH protocol

**Test Steps**:
1. Trigger fact verification for protocol/port claim
2. Validate port number correctly mapped to protocol
3. Validate common port associations identified

**Expected Results**:
- Port 22 correctly identified as SSH
- Common protocols accurately mapped

**Pass Criteria**: Protocol/port validation accurate

---

### 4.19 Scenario 19: Regression Test - CVE Enrichment Workflow

**Test ID**: TS-EPIC7-019
**Priority**: Critical
**Type**: Regression test

**Objective**: Validate CVE enrichment workflow unchanged by Epic 7 changes

**Test Data**:
- **Ticket**: CVE enrichment ticket (existing or new)
- **Expected Behavior**: CVE workflow works exactly as before Epic 7

**Preconditions**:
- CVE enrichment ticket accessible
- Security analyst agent loaded

**Test Steps**:
1. Execute `*enrich-ticket {cve-ticket-id}` (security analyst command)
2. Validate CVE enrichment workflow executes
3. Validate CVSS scoring, exploit analysis, patch recommendations
4. Validate enrichment document generation
5. Compare behavior to pre-Epic 7 baseline

**Expected Results**:
- CVE enrichment workflow unchanged
- No event investigation logic triggered
- Performance same as pre-Epic 7 baseline
- Enrichment document format unchanged

**Pass Criteria**: No regression detected

---

### 4.20 Scenario 20: Regression Test - CVE Review Workflow

**Test ID**: TS-EPIC7-020
**Priority**: Critical
**Type**: Regression test

**Objective**: Validate CVE review workflow unchanged by Epic 7 changes

**Test Data**:
- **Ticket**: CVE enrichment ticket with investigation document
- **Expected Behavior**: CVE review workflow works exactly as before Epic 7

**Preconditions**:
- CVE review ticket accessible
- Security reviewer agent loaded

**Test Steps**:
1. Execute `*review-enrichment {cve-ticket-id} --type=cve` (explicit CVE type)
2. Validate CVE review workflow executes
3. Validate CVE-specific checklists used
4. Validate review report format unchanged
5. Compare behavior to pre-Epic 7 baseline

**Expected Results**:
- CVE review workflow unchanged
- No event investigation checklists executed
- Performance same as pre-Epic 7 baseline
- Review report format unchanged

**Pass Criteria**: No regression detected

---

### 4.21 Scenario 21: Performance Test - Event Investigation

**Test ID**: TS-EPIC7-021
**Priority**: High
**Type**: Performance test

**Objective**: Validate event investigation completes within target duration (10-15 minutes)

**Test Data**:
- **Ticket**: AOD-4052 (ICS Alert)

**Test Steps**:
1. Start timer
2. Execute `*investigate-event AOD-4052`
3. Stop timer when investigation complete
4. Record duration
5. Repeat 3 times for average

**Expected Results**:
- Average duration: 10-15 minutes
- No performance degradation vs. baseline

**Pass Criteria**: Investigation completes within 15 minutes (95% of executions)

---

### 4.22 Scenario 22: Performance Test - Event Review

**Test ID**: TS-EPIC7-022
**Priority**: High
**Type**: Performance test

**Objective**: Validate event review completes within target duration (15-20 minutes)

**Test Data**:
- **Ticket**: Event investigation ticket

**Test Steps**:
1. Start timer
2. Execute `*review-enrichment {ticket-id}`
3. Stop timer when review complete
4. Record duration
5. Repeat 3 times for average

**Expected Results**:
- Average duration: 15-20 minutes
- No performance degradation vs. CVE review baseline

**Pass Criteria**: Review completes within 20 minutes (95% of executions)

---

### 4.23 Scenario 23: Integration Test - JIRA MCP Read

**Test ID**: TS-EPIC7-023
**Priority**: High
**Type**: Integration test

**Objective**: Validate JIRA Atlassian MCP can read ticket data

**Test Steps**:
1. Execute investigation/review command
2. Validate JIRA MCP successfully reads ticket metadata
3. Validate ticket description, comments, custom fields retrieved
4. Validate no connection errors

**Expected Results**:
- JIRA MCP successfully reads ticket data
- All required fields retrieved (Issue Type, Summary, Description, Comments)
- No authentication or connection errors

**Pass Criteria**: JIRA MCP read operations succeed 100%

---

### 4.24 Scenario 24: Integration Test - JIRA MCP Write

**Test ID**: TS-EPIC7-024
**Priority**: High
**Type**: Integration test

**Objective**: Validate JIRA Atlassian MCP can write ticket updates

**Test Steps**:
1. Execute investigation/review command
2. Validate JIRA MCP successfully writes comment
3. Validate JIRA MCP successfully updates custom fields
4. Validate no connection errors

**Expected Results**:
- JIRA MCP successfully writes investigation/review comment
- Custom fields updated correctly (Disposition, Quality Score, etc.)
- No authentication or connection errors

**Pass Criteria**: JIRA MCP write operations succeed 100%

---

### 4.25 Scenario 25: Integration Test - Perplexity MCP

**Test ID**: TS-EPIC7-025
**Priority**: High
**Type**: Integration test

**Objective**: Validate Perplexity MCP can perform fact verification queries

**Test Steps**:
1. Trigger fact verification during investigation review
2. Validate Perplexity MCP successfully queries for IP ownership
3. Validate Perplexity MCP successfully queries for threat intelligence
4. Validate results returned with source citations
5. Validate no API errors or timeouts

**Expected Results**:
- Perplexity MCP successfully queries and returns results
- Source citations included in responses
- No API rate limit or timeout errors

**Pass Criteria**: Perplexity MCP operations succeed 100%

---

### 4.26 Scenario 26: Error Handling - JIRA MCP Timeout

**Test ID**: TS-EPIC7-026
**Priority**: Medium
**Type**: Error handling test

**Objective**: Validate graceful handling of JIRA MCP timeout errors

**Test Steps**:
1. Simulate JIRA MCP timeout (disconnect network or use invalid ticket ID)
2. Execute investigation/review command
3. Validate error message displayed to user
4. Validate workflow halts gracefully (no crash)

**Expected Results**:
- Clear error message displayed (e.g., "JIRA connection timeout")
- Workflow halts gracefully
- No stack trace or crash
- User can retry after fixing connection

**Pass Criteria**: Error handled gracefully with clear user message

---

### 4.27 Scenario 27: Error Handling - Perplexity MCP Failure

**Test ID**: TS-EPIC7-027
**Priority**: Medium
**Type**: Error handling test

**Objective**: Validate graceful handling of Perplexity MCP failures

**Test Steps**:
1. Simulate Perplexity MCP failure (invalid API key or rate limit exceeded)
2. Execute fact verification
3. Validate error message displayed
4. Validate workflow continues without fact verification results (graceful degradation)

**Expected Results**:
- Clear error message displayed (e.g., "Fact verification unavailable")
- Workflow continues without crashing
- Review report notes fact verification could not be completed

**Pass Criteria**: Error handled gracefully with graceful degradation

---

## 5. Success Criteria

### 5.1 Functional Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Auto-detection accuracy | 95%+ | Test scenarios 8-14 (7 scenarios, max 1 failure allowed) |
| End-to-end investigation success | 100% | Test scenarios 1-3 (all must pass) |
| End-to-end review success | 100% | Test scenarios 4-5 (all must pass) |
| Disposition handling correctness | 100% | Test scenarios 6-7 (all must pass) |
| Checklist execution correctness | 100% | All 7 checklists execute and score correctly |
| Fact verification accuracy | 90%+ | Test scenarios 15-18 (manual verification of results) |
| Regression test pass rate | 100% | Test scenarios 19-20 (no CVE workflow changes) |

### 5.2 Performance Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Event investigation duration | 10-15 minutes | Test scenario 21 (average of 3 runs) |
| Event review duration | 15-20 minutes | Test scenario 22 (average of 3 runs) |
| JIRA MCP response time | < 5 seconds per operation | Test scenarios 23-24 (95th percentile) |
| Perplexity MCP response time | < 10 seconds per query | Test scenario 25 (95th percentile) |

### 5.3 Integration Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| JIRA MCP read success rate | 100% | Test scenario 23 (no failures) |
| JIRA MCP write success rate | 100% | Test scenario 24 (no failures) |
| Perplexity MCP success rate | 100% | Test scenario 25 (no failures) |
| Error handling correctness | 100% | Test scenarios 26-27 (graceful handling) |

### 5.4 Overall Pass Criteria

**Story Completion Pass Criteria**:
- All functional success criteria met
- All performance success criteria met (or conditional pass with documented deviations)
- All integration success criteria met
- No critical defects identified
- All acceptance criteria (AC 1-7) validated

**Conditional Pass Criteria**:
- Minor defects identified but do not block core functionality
- Performance targets missed by < 20% (defer optimization to future story)
- Non-critical error handling issues (defer improvements to future story)

**Fail Criteria**:
- Any critical defect prevents core functionality
- Regression detected in CVE workflows
- Auto-detection accuracy < 90%
- End-to-end workflows fail to complete

## 6. Test Deliverables

### 6.1 Test Plan (This Document)
- Epic 7 test plan with scope, objectives, approach, scenarios, success criteria
- **Location**: `expansion-packs/bmad-1898-engineering/tests/test-plans/epic-7-test-plan.md`

### 6.2 Test Data Files
- Mock ICS alert ticket (`ics-alert-claroty-ssh.json`)
- Mock IDS alert ticket (`ids-alert-snort-exploit.json`)
- Mock SIEM alert ticket (`siem-alert-splunk-logins.json`)
- Mock excellent investigation (`investigation-excellent.md`)
- Mock needs-improvement investigation (`investigation-needs-improvement.md`)
- **Location**: `expansion-packs/bmad-1898-engineering/tests/test-data/`

### 6.3 Test Execution Report
- Test results for all 27 scenarios
- Pass/fail status for each scenario
- Evidence (logs, screenshots, generated documents)
- Defect tracking (if any defects identified)
- Final assessment and go/no-go recommendation
- **Location**: `expansion-packs/bmad-1898-engineering/tests/test-results/epic-7-test-execution-report.md`

## 7. Risk Assessment

### 7.1 High Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| JIRA MCP unavailable during testing | Cannot test end-to-end with real tickets | Prepare mock ticket data as fallback |
| Perplexity MCP rate limits exceeded | Fact verification testing incomplete | Stagger fact verification tests, use caching |
| Auto-detection logic fails ambiguous cases | False negatives/positives in ticket routing | Enhance detection patterns, add manual override |

### 7.2 Medium Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Performance targets not met | Defer optimization to future story | Document performance gaps, conditional pass |
| Weighted scoring calculation errors | Incorrect quality classifications | Manual verification of all score calculations |

### 7.3 Low Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Test data preparation takes longer than estimated | Test schedule delayed | Allocate buffer time, prioritize critical scenarios first |

## 8. Test Schedule

| Phase | Duration | Tasks |
|-------|----------|-------|
| **Preparation** | 4-6 hours | Create test plan, prepare test data, set up environment |
| **Execution** | 8-12 hours | Execute all 27 test scenarios, document results |
| **Validation** | 2-3 hours | Verify outputs, measure performance, validate scoring |
| **Reporting** | 1-2 hours | Create test execution report, provide recommendations |
| **Total** | **15-23 hours** | End-to-end testing effort |

## 9. Dependencies

### 9.1 External Dependencies

- JIRA Atlassian MCP server (accessible and configured)
- Perplexity MCP server (accessible and configured)
- Real JIRA ticket AOD-4052 (accessible)

### 9.2 Internal Dependencies

- Security analyst agent (`security-analyst.md`)
- Security reviewer agent (`security-reviewer.md`)
- 7 event investigation checklists (all must exist and be accessible)
- Event investigation review report template (`security-event-investigation-review-report-tmpl.yaml`)
- Fact verification task (`fact-verify-claims.md`)
- Event investigation knowledge base (`event-investigation-kb.md`)

## 10. Approval

### 10.1 Test Plan Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| **QA Engineer** | TBD | ___________ | 2025-11-09 |
| **Product Owner** | TBD | ___________ | _________ |
| **Technical Lead** | TBD | ___________ | _________ |

### 10.2 Test Plan Change Log

| Date | Version | Change Description | Author |
|------|---------|-------------------|--------|
| 2025-11-09 | 1.0 | Initial test plan creation | QA Engineer |

---

**Document Status**: Draft
**Next Review Date**: 2025-11-10

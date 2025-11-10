# Investigate Event Alert Task

## Purpose

Execute the complete Security Event Alert Investigation Workflow from initial JIRA ticket triage through comprehensive analysis, disposition determination, and structured documentation. This task supports ICS, IDS, and SIEM alert investigations with evidence-based disposition analysis.

## Prerequisites

- Atlassian MCP server configured and connected
- Perplexity MCP server configured and connected (optional for threat intelligence)
- JIRA configuration in `config.yaml` with required fields
- Security Analyst agent activated
- Valid JIRA ticket ID with security event alert

## Workflow Overview

This task executes a 7-stage event investigation workflow:

1. **Triage & Alert Type Detection** - Extract alert data and classify alert type
2. **Alert Metadata Collection** - Capture source, rule ID, severity, timestamps
3. **Network/Host Identifier Documentation** - Document IPs, hostnames, asset types
4. **Evidence Collection** - Gather logs, correlation data, historical context
5. **Technical Analysis** - Analyze protocols, attack vectors, threat intelligence
6. **Disposition Determination** - Classify as TP/FP/BTP with evidence-based reasoning
7. **Documentation & JIRA Update** - Generate investigation document and update ticket

**Target Duration:** 15-25 minutes

## Task Execution

### Initial Setup

1. **Elicit ticket ID:**
   - Ask: "Please provide the JIRA ticket ID to investigate (e.g., AOD-4052):"
   - Validate format: `{PROJECT_KEY}-{NUMBER}`
   - Store ticket ID for workflow tracking

2. **Fetch ticket data:**
   - Execute: `read-jira-ticket.md` task
   - Capture ticket summary, description, custom fields, comments
   - If ticket not found: Validate ticket ID and retry
   - If MCP error: Check connection and retry once

3. **Initialize investigation state:**
   - Create investigation context object to store collected data
   - Initialize timestamp for investigation start

### Stage 1: Triage & Alert Type Detection

**Duration:** 2-3 minutes

**Actions:**

1. **Detect alert type from ticket metadata:**

   Check JIRA Issue Type field:
   - "Event Alert" → Event investigation workflow (proceed)
   - "ICS Alert" → ICS-specific investigation
   - "Security Vulnerability" → Wrong workflow (suggest CVE enrichment)

2. **Analyze ticket content for platform detection:**

   **ICS/SCADA Platform Indicators:**
   - Platform keywords: "Claroty", "Nozomi", "Dragos", "CyberX"
   - Domain keywords: "ICS", "SCADA", "OT", "Operational Technology", "PLC", "HMI", "Modbus", "DNP3"
   - Set `alert_platform_type` = "ICS"

   **IDS/IPS Platform Indicators:**
   - Platform keywords: "Snort", "Suricata", "Palo Alto", "Cisco Firepower"
   - Domain keywords: "IDS", "IPS", "Intrusion Detection", "Threat Signature", "SID:"
   - Set `alert_platform_type` = "IDS"

   **SIEM Platform Indicators:**
   - Platform keywords: "Splunk", "QRadar", "Sentinel", "Elastic Security"
   - Domain keywords: "SIEM", "Correlation Rule", "Use Case", "Notable Event"
   - Set `alert_platform_type` = "SIEM"

   **If ambiguous:**
   - Prompt user: "Unable to auto-detect alert type. Please select:\n 1. ICS/SCADA Alert\n 2. IDS/IPS Alert\n 3. SIEM Correlation Alert"
   - Accept numeric selection or full text
   - Validate selection before proceeding

3. **Extract initial alert metadata:**
   - Alert name/signature
   - Severity level (Critical/High/Medium/Low)
   - Detection timestamp
   - Alert source/sensor
   - Rule ID or signature ID
   - Alert category/classification

**Outputs to collect:**

- `alert_platform_type` (ICS/IDS/SIEM)
- `alert_platform` (specific platform name, e.g., "Claroty", "Snort", "Splunk")
- `alert_name` (full alert name)
- `alert_severity` (Critical/High/Medium/Low)
- `alert_id` (rule ID or signature ID)
- `alert_category` (classification or category)
- `detection_timestamp` (when alert fired)
- `alert_source` (sensor or platform that generated alert)

**Error Handling:**

- If alert name not found: Prompt user for alert name
- If severity missing: Default to "Medium" with warning flag
- If timestamp missing: Use ticket creation time with note

### Stage 2: Alert Metadata Collection

**Duration:** 2-3 minutes

**Actions:**

1. **Capture alert source details:**
   - Sensor/platform that generated alert
   - Detection engine version (if available)
   - Alert rule ID or signature ID
   - Alert category/classification

2. **Extract raw alert data:**
   - Capture original alert message from ticket description or comments
   - Extract relevant alert field excerpts
   - Preserve formatting for evidence documentation

3. **Build event timeline:**
   - Event occurrence time (when activity happened)
   - Alert detection time (when alert fired)
   - Investigation start time (current timestamp)
   - Calculate time delta between occurrence and detection

**Outputs to collect:**

- `detection_engine` (engine version if available)
- `raw_alert_data` (original alert message/excerpts)
- `event_occurrence_time` (activity timestamp)
- `investigation_start_time` (current time)
- `detection_delay` (time between occurrence and detection)

**Error Handling:**

- If raw alert data not in ticket: Note as "Not available in ticket - manual collection required"
- If occurrence time unavailable: Use detection time with note

### Stage 3: Network/Host Identifier Documentation

**Duration:** 3-4 minutes

**Actions:**

1. **Extract source information:**
   - Source IP address
   - Source hostname (if available)
   - Source asset type (server/workstation/ICS device/network equipment)
   - Source asset criticality (from CMDB or user input)
   - Source zone (for ICS: Control/DMZ/Enterprise)

2. **Extract destination information:**
   - Destination IP address
   - Destination hostname (if available)
   - Destination asset type
   - Destination asset criticality
   - Destination zone

3. **Capture protocol and port information:**
   - Protocol (TCP/UDP/ICMP/Industrial protocol)
   - Port number(s)
   - Service identification (if known)

4. **Optional: ASN/Geo information (for external IPs):**
   - If source or dest is external IP
   - Use Perplexity to lookup ASN, organization, geolocation
   - Note reputation (known malicious/benign/unknown)

**Inputs:**

- Ticket custom fields for IPs, hostnames
- JIRA Asset Criticality Rating (ACR) field
- User input if data missing from ticket

**Outputs to collect:**

- `source_ip`
- `source_hostname`
- `source_asset_type`
- `source_asset_criticality`
- `source_zone` (optional for ICS)
- `destination_ip`
- `destination_hostname`
- `destination_asset_type`
- `destination_asset_criticality`
- `destination_zone` (optional for ICS)
- `protocol`
- `port`
- `service_name` (optional)
- `asn_information` (optional for external IPs)

**Error Handling:**

- If source IP missing: Prompt user for source IP (required)
- If destination IP missing: Prompt user for destination IP (required)
- If hostnames unavailable: Note as "Hostname not resolved"
- If asset criticality unavailable: Prompt user or default to "Medium"

**Elicitation (if data missing from ticket):**

```
⚠️ Missing network identifiers in ticket. Please provide:

Source IP: _____
Destination IP: _____
Protocol: _____
Port: _____

(Press Enter to skip optional fields)
```

### Stage 4: Evidence Collection

**Duration:** 5-8 minutes

**Actions:**

1. **Identify log sources to review:**
   - Firewall logs (egress/ingress traffic)
   - IDS/IPS logs (related alerts)
   - Endpoint logs (process execution, file access)
   - Application logs (authentication, errors)
   - ICS platform logs (for OT alerts)

2. **Prompt user for log evidence:**
   - Display PII handling warning before elicitation
   - Elicit: "Please provide relevant log excerpts or state 'none' if unavailable:"
   - Accept multi-line input
   - Store as `relevant_log_excerpts`
   - **PII Handling:** Logs may contain sensitive data - redact before sharing if required by policy

3. **Elicit correlated events:**
   - Ask: "Were there related or correlated events? (Enter event descriptions or 'none'):"
   - Accept list of related events
   - Store as `correlated_events`

4. **Elicit historical context:**
   - Ask: "Any historical context? (Previous occurrences, known patterns, or 'none'):"
   - Accept historical information
   - Store as `historical_context`

5. **Optional: AI-assisted threat intelligence (Perplexity):**
   - If external IP detected, query reputation
   - If protocol/port unusual, research typical usage patterns
   - If alert signature known, research false positive patterns
   - Store findings in `threat_intelligence_findings`

**Inputs:**

- User-provided log excerpts
- User-provided correlation data
- Historical context from user or SIEM
- Perplexity MCP for threat intelligence (optional)

**Outputs to collect:**

- `log_sources_reviewed` (comma-separated list)
- `relevant_log_excerpts` (multi-line text)
- `correlated_events` (list of related events)
- `historical_context` (previous occurrences, patterns)
- `threat_intelligence_findings` (optional AI research)

**Error Handling:**

- If no logs available: Flag as "⚠️ No logs collected - investigation incomplete"
- If user enters 'none': Document as "No evidence available"
- Continue investigation with available data, but note evidence gaps

**Elicitation Format:**

```
📋 Evidence Collection

⚠️ PII HANDLING NOTICE: Log excerpts may contain personally identifiable information
(usernames, email addresses, IP addresses). Redact PII if required by your
organization's data handling policy before providing evidence.

Log Sources Reviewed: (e.g., "Firewall, IDS, Endpoint EDR")
> _____

Relevant Log Excerpts: (paste logs or type 'none')
⚠️ Remember to redact PII: usernames, emails, internal IPs if required
> _____

Correlated Events: (related alerts or 'none')
> _____

Historical Context: (previous occurrences or 'none')
> _____
```

### Stage 5: Technical Analysis

**Duration:** 4-6 minutes

**Actions:**

1. **Protocol and Port Analysis:**
   - Validate protocol/port combination legitimacy
   - Research typical usage for protocol/port
   - Assess if usage aligns with expected behavior
   - Elicit: "Is this protocol/port usage expected for these systems? (y/n/unknown):"
   - Store as `protocol_port_analysis`

2. **Attack Vector Analysis:**
   - Based on alert type and protocol, identify potential attack vector
   - Reference MITRE ATT&CK if applicable
   - Document how attack could be executed
   - Store as `attack_vector_analysis`

3. **Log Interpretation:**
   - Analyze provided log excerpts for suspicious indicators
   - Identify IOCs (Indicators of Compromise)
   - Look for anomalies or deviations from baseline
   - Store as `log_interpretation`

4. **Threat Intelligence Correlation (Optional - Perplexity):**
   - If Perplexity available, query:
     - "Is IP {source_ip} associated with known malicious activity?"
     - "Known false positive patterns for {alert_name}?"
   - Store findings in `ioc_analysis` and `threat_intelligence`

5. **Asset Context Assessment:**
   - Document asset function and business purpose
   - Assess business impact if compromised
   - Identify environmental factors (test vs prod, maintenance windows)
   - Elicit: "Asset function: **\_**"
   - Elicit: "Business impact if compromised: **\_**"
   - Elicit: "Environmental factors (maintenance/testing/changes): **\_**"
   - Store as `asset_context` fields

**Outputs to collect:**

- `protocol_port_analysis` (validation and legitimacy assessment)
- `attack_vector_analysis` (how attack could work)
- `log_interpretation` (analysis of log evidence)
- `ioc_analysis` (indicators of compromise identified)
- `threat_intelligence` (external threat correlation)
- `asset_criticality` (from Stage 3 or user input)
- `asset_function` (business purpose)
- `business_impact` (potential impact if compromised)
- `environmental_factors` (test/prod, maintenance, changes)

**Error Handling:**

- If protocol/port research unavailable: Note as "Standard validation performed"
- If no IOCs identified: Note as "No indicators of compromise detected"
- If Perplexity unavailable: Skip threat intelligence, continue with manual analysis

**Elicitation Format:**

```
🔬 Technical Analysis

Is {protocol} port {port} traffic expected between these systems? (y/n/unknown)
> _____

Asset Function: (e.g., "Production database server")
> _____

Business Impact if Compromised: (e.g., "Loss of customer data access")
> _____

Environmental Factors: (e.g., "Maintenance window active", "Test environment")
> _____
```

### Stage 6: Disposition Determination

**Duration:** 3-5 minutes

**Actions:**

1. **Review evidence summary:**
   - Present collected evidence to analyst
   - Show alert details, network identifiers, logs, analysis findings

2. **Apply disposition framework:**

   **True Positive (TP) Criteria:**
   - Genuine malicious or unauthorized activity confirmed
   - Evidence supports malicious intent
   - No legitimate explanation for activity
   - IOCs correlate with known threats

   **False Positive (FP) Criteria:**
   - Benign activity incorrectly flagged
   - No threat present
   - Activity explained by legitimate business process
   - Misconfigured detection rule

   **Benign True Positive (BTP) Criteria:**
   - Real activity detected but authorized/expected
   - Examples: Maintenance, testing, approved scanning
   - Activity is legitimate but triggered detection

3. **Elicit disposition from analyst:**

   ```
   📊 Disposition Assessment

   Based on the evidence collected, select disposition:
   1. True Positive (TP) - Genuine malicious activity
   2. False Positive (FP) - Benign activity incorrectly flagged
   3. Benign True Positive (BTP) - Authorized activity that triggered alert

   Selection (1/2/3):
   > _____
   ```

4. **Elicit confidence level:**

   ```
   Confidence Level in this disposition:
   1. High - Strong evidence supporting disposition
   2. Medium - Reasonable evidence but some uncertainty
   3. Low - Limited evidence, recommend escalation

   Selection (1/2/3):
   > _____
   ```

5. **Elicit disposition reasoning:**

   ```
   Provide detailed reasoning for this disposition:
   (Explain evidence and logic connecting to conclusion)
   > _____
   ```

6. **Elicit alternative dispositions considered:**

   ```
   What alternative dispositions did you consider and why were they ruled out?
   > _____
   ```

7. **Determine escalation and next actions:**
   - If TP + High confidence + Critical severity → Escalate to Incident Response
   - If TP + Medium confidence → Recommend peer review
   - If FP → Recommend alert tuning
   - If BTP → Document authorized activity, consider tuning
   - If Low confidence → Escalate for senior analyst review

8. **Elicit recommended next actions:**

   ```
   Recommended Next Actions:
   1. Escalate to Incident Response
   2. Containment actions required
   3. Alert tuning needed
   4. Monitor for recurrence
   5. Close with documentation
   6. Other (specify)

   Selection (can select multiple, comma-separated):
   > _____

   Specify actions: (detailed action items)
   > _____
   ```

**Outputs to collect:**

- `disposition` (True Positive / False Positive / Benign True Positive)
- `confidence_level` (High / Medium / Low)
- `disposition_reasoning` (evidence → logic → conclusion)
- `alternative_dispositions_considered` (what was ruled out and why)
- `escalation_decision` (Escalate / Monitor / Tune / Close)
- `next_actions` (specific action items)
- `containment_required` (Yes/No with actions if yes)
- `tuning_recommendations` (if FP or BTP)
- `monitoring_recommendations` (ongoing monitoring if needed)

**Error Handling:**

- If disposition unclear: Require analyst input (no default)
- If confidence Low: Automatically recommend escalation
- If evidence insufficient for disposition: Flag as "Incomplete investigation - insufficient evidence"

**Elicitation Format:**

```
📊 Disposition Determination

Evidence Summary:
- Alert: {alert_name} ({alert_severity})
- Source: {source_ip} → Destination: {destination_ip}
- Protocol/Port: {protocol}/{port}
- Logs: {log summary}
- Analysis: {analysis summary}

Select Disposition:
1. True Positive (TP) - Genuine malicious activity
2. False Positive (FP) - Benign activity incorrectly flagged
3. Benign True Positive (BTP) - Authorized activity

Selection: _____

Confidence Level (High/Medium/Low): _____

Reasoning: (Explain evidence → logic → conclusion)
_____

Alternative dispositions considered: _____

Escalation needed? (Yes/No): _____

Recommended next actions:
_____

If containment needed, specify actions: _____

If tuning needed, specify recommendations: _____
```

### Stage 7: Documentation & JIRA Update

**Duration:** 2-3 minutes

**Actions:**

1. **Generate investigation document from template:**
   - Use template: `templates/event-investigation-tmpl.yaml`
   - Populate all sections with collected data
   - Use `create-doc.md` task for template processing
   - Validate all sections populated

2. **Save investigation document locally:**
   - Directory: `artifacts/enrichments/`
   - Filename: `{ticket-id}-event-investigation-{timestamp}.md`
   - Create directory if not exists
   - **Chain of Custody:** Local save MUST complete before JIRA update to preserve evidence trail
   - Document includes: Analyst name, investigation timestamps, all evidence collected, disposition reasoning

3. **Post investigation to JIRA as comment:**
   - Use `post-enrichment-comment.md` task pattern
   - Call MCP tool: `mcp__atlassian__addComment`
   - Include full investigation document
   - Verify comment posted successfully

4. **Update JIRA custom fields:**
   - Use `update-jira-fields.md` task pattern
   - Load field mappings from `config.yaml` (jira.custom_fields.disposition, confidence_level, next_actions, investigation_duration)
   - Update fields using configured field IDs:
     - Disposition: {disposition} → config.jira.custom_fields.disposition.field_id
     - Confidence Level: {confidence_level} → config.jira.custom_fields.confidence_level.field_id
     - Next Actions: {next_actions} → config.jira.custom_fields.next_actions.field_id
     - Investigation Duration: {duration} → config.jira.custom_fields.investigation_duration.field_id
   - Call MCP tool: `mcp__atlassian__updateJiraIssue`
   - Verify fields updated successfully

5. **Optional: Update ticket status:**
   - If disposition is TP + escalation required → Status: "Escalated"
   - If disposition is FP/BTP + tuning recommended → Status: "Tuning Required"
   - If investigation complete and no escalation → Status: "Resolved"
   - Only update if status workflow configured in JIRA project

**Outputs:**

- Investigation document (markdown)
- Local file saved (verify file exists)
- JIRA comment posted (verify comment ID returned)
- JIRA fields updated (verify update success)
- Ticket status updated (optional, if configured)

**Error Handling:**

- If template missing: HALT with error message
- If comment post fails: Save locally and notify user with retry instructions
- If field update fails: Continue with partial update, log specific field errors
- If local save fails: HALT (critical for audit trail)
- If status update unavailable: Skip status update (optional feature)

### Workflow Completion

**Upon successful completion:**

1. **Display completion summary:**

   ```
   ✅ Event Investigation Complete!
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Ticket: {ticket_id}
   Alert: {alert_name}
   Platform: {alert_platform} ({alert_platform_type})
   Disposition: {disposition} (Confidence: {confidence_level})
   Next Actions: {next_actions_summary}
   Duration: {total_time}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Investigation saved to: artifacts/enrichments/{filename}
   JIRA ticket updated successfully.
   ```

2. **Prompt user for next action:**
   - "Investigate another alert? (y/n)"
   - If yes, restart workflow
   - If no, return to agent prompt

## Error Recovery & Retry Logic

### Automatic Retry

For transient errors (network, rate limits, timeouts):

1. **First failure:** Wait 5 seconds, retry
2. **Second failure:** Wait 15 seconds, retry
3. **Third failure:** Prompt user to continue or abort

### Manual Recovery

For permanent errors (authentication, missing data):

1. Display error with context
2. Suggest resolution steps
3. Prompt user: "Retry / Skip / Abort?"
4. If skip: Document gap and continue with warning

## Common Error Scenarios

### Missing Ticket Data

**Error:** "Source IP not found in ticket"

**Handling:**

- Prompt user for required information
- Flag gap: "⚠️ Source IP not available in ticket - manually provided"
- Continue with user-provided data

### Unsupported Alert Type

**Error:** "Unable to detect alert platform type"

**Handling:**

- Prompt user to select from ICS/IDS/SIEM options
- Provide generic investigation template
- Document manual platform classification

### Incomplete Evidence

**Error:** "No log evidence provided"

**Handling:**

- Flag gap: "⚠️ No logs collected - investigation incomplete"
- Allow disposition determination with warning
- Document evidence limitations in investigation report
- Recommend follow-up investigation if needed

### JIRA Connection Failures

**Error:** "Failed to post comment after 3 retries"

**Handling:**

- Save investigation document locally (priority)
- Display error: "JIRA update failed. Investigation saved locally."
- Provide manual posting instructions
- Suggest: "Copy investigation from {filepath} and post to {ticket_id} manually"

### Disposition Uncertainty

**Warning:** "Confidence level: Low"

**Handling:**

- Automatically recommend escalation
- Document in report: "Low confidence - recommend peer review"
- Suggest senior analyst consultation
- Document alternative dispositions considered

## Quality Validation

Before marking investigation complete, validate:

- ✅ Alert type detected and classified
- ✅ Alert metadata collected (source, rule ID, severity)
- ✅ Network identifiers documented (source IP, dest IP, protocol, port)
- ✅ Evidence collection attempted (logs, correlation, historical context)
- ✅ Technical analysis performed (protocol validation, attack vector, IOC analysis)
- ✅ Disposition determined with reasoning
- ✅ Confidence level assigned
- ✅ Next actions specified
- ✅ Investigation document generated from template
- ✅ Local file saved (CRITICAL: preserves chain of custody)
- ✅ JIRA comment posted
- ✅ JIRA custom fields updated
- ✅ **Chain of Custody maintained:** Analyst identified, timestamps recorded, evidence preservation documented

**Quality Score Calculation:**

- Total checks: 13
- Passed checks / Total checks = Quality %
- Target: >75% (10+ checks passing)

If quality score <75%, display warning and suggest review before closing.

## Usage Examples

### Basic Usage (From Security Analyst Agent)

```
*investigate-event AOD-4052
```

### Standalone Usage (Direct Task Execution)

```
Execute task: investigate-event-alert.md
> Please provide the JIRA ticket ID: AOD-4052
```

### With Pre-specified Ticket

```
*investigate-event AOD-4052
> Fetching ticket AOD-4052...
> Detected ICS Alert (Claroty platform)
> Beginning investigation workflow...
```

## Integration Points

This task depends on:

- **Tasks:**
  - `read-jira-ticket.md` (Stage 1)
  - `create-doc.md` (Stage 7)
  - `post-enrichment-comment.md` (Stage 7 pattern)
  - `update-jira-fields.md` (Stage 7 pattern)

- **Templates:**
  - `event-investigation-tmpl.yaml` (Stage 7)

- **MCP Servers:**
  - Atlassian MCP (JIRA operations) - **Required**
  - Perplexity MCP (Threat intelligence) - **Optional**

## Notes

- This is an operational workflow task designed for runtime execution by Security Analyst agent
- Heavy elicitation required for evidence collection and disposition determination
- Analyst expertise is critical - task guides but does not automate disposition decisions
- Error handling ensures graceful degradation when data is incomplete
- Quality validation ensures consistent investigation standards
- Investigation documents serve as audit trail and knowledge base

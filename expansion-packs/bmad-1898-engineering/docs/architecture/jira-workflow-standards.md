# BMAD-1898 JIRA Workflow Standards

## Overview

This document defines the JIRA workflow configuration required for BMAD-1898 Engineering expansion pack vulnerability lifecycle management. These standards ensure consistent vulnerability tracking from detection through closure.

## Required JIRA Statuses

The following JIRA statuses must be configured in your JIRA project to support the complete vulnerability lifecycle workflow (Epic 3, Story 3.3).

| Status Name             | Stage             | Description                                      | SLA Tracking |
| ----------------------- | ----------------- | ------------------------------------------------ | ------------ |
| Open                    | Detection         | Initial vulnerability alert from scanner or feed | Start        |
| In Progress             | Enrichment        | Security Analyst performing enrichment           | Yes          |
| In Review               | Quality Assurance | Security Reviewer performing peer review         | Yes          |
| Remediation Planning    | Planning          | DevOps team planning patch deployment            | Yes          |
| Remediation In Progress | Execution         | Patches/workarounds being deployed               | Yes          |
| Verification            | Verification      | Verifying vulnerability successfully remediated  | Yes          |
| Closed                  | Closure           | Vulnerability lifecycle complete                 | End          |

## Status Transition Rules

The following status transitions define the vulnerability lifecycle workflow. All transitions must be configured in JIRA to enable proper workflow execution.

### Forward Transitions

| From Status             | To Status               | Trigger                                           | Automation |
| ----------------------- | ----------------------- | ------------------------------------------------- | ---------- |
| Open                    | In Progress             | Analyst starts enrichment                         | Manual     |
| In Progress             | In Review               | Enrichment complete, P1/P2 or sampled P3/P4/P5    | Automated  |
| In Progress             | Remediation Planning    | Enrichment complete, P3/P4/P5 review not required | Automated  |
| In Review               | Remediation Planning    | Review approved                                   | Manual     |
| Remediation Planning    | Remediation In Progress | Remediation plan approved, execution starts       | Manual     |
| Remediation In Progress | Verification            | Remediation deployment complete                   | Manual     |
| Verification            | Closed                  | Vulnerability verified remediated                 | Manual     |

### Reverse Transitions (Rework Loops)

| From Status  | To Status               | Trigger                                              | Automation |
| ------------ | ----------------------- | ---------------------------------------------------- | ---------- |
| In Review    | In Progress             | Review identifies Critical Issues                    | Manual     |
| Verification | Remediation In Progress | Verification failed, vulnerability still exploitable | Manual     |

## Required Custom Fields

The following custom fields must be created in JIRA to support enrichment data capture and reporting.

| Field Name       | Type          | Description                                     | Required | Source        |
| ---------------- | ------------- | ----------------------------------------------- | -------- | ------------- |
| CVE ID           | Text          | CVE identifier (e.g., CVE-2024-1234)            | Yes      | User input    |
| CVSS Score       | Number        | CVSS base score (0.0-10.0)                      | Yes      | AI research   |
| CVSS Vector      | Text          | CVSS vector string                              | No       | AI research   |
| EPSS Score       | Number        | EPSS exploitation probability (0.0-1.0)         | Yes      | AI research   |
| KEV Status       | Single Select | CISA KEV status (Yes/No)                        | Yes      | AI research   |
| Priority Level   | Single Select | Priority (P1/P2/P3/P4/P5)                       | Yes      | Priority calc |
| Affected Systems | Labels/Text   | List of affected systems                        | Yes      | User input    |
| ACR Rating       | Single Select | Asset Criticality (Critical/High/Medium/Low)    | Yes      | Config        |
| System Exposure  | Single Select | Exposure (Internet/Internal/Isolated)           | No       | User input    |
| Review Status    | Single Select | Review status (Pending/Approved/Needs Revision) | No       | Review agent  |
| Quality Score    | Number        | Review quality score (0-100)                    | No       | Review agent  |
| Enrichment Date  | Date          | Date enrichment completed                       | No       | Automation    |
| SLA Deadline     | Date          | Remediation deadline based on priority          | No       | Priority calc |

### Custom Field Configuration Notes

1. **Single Select Fields**: Create with exact values specified above (case-sensitive)
2. **Number Fields**: Configure with appropriate decimal precision (CVSS: 1 decimal, EPSS: 3 decimals)
3. **Labels vs. Text**: Use Labels for Affected Systems if multi-value selection needed, Text if comma-separated string acceptable
4. **Field IDs**: Document custom field IDs in `config.yaml` for MCP integration

## JIRA Status Mapping to Lifecycle Stages

The vulnerability lifecycle workflow (Story 3.3) maps to JIRA statuses as follows:

```yaml
lifecycle_stages:
  stage1_detection:
    jira_status: 'Open'
    description: 'Vulnerability scanner or feed alerts security team'

  stage2_enrichment:
    jira_status: 'In Progress'
    description: 'Security Analyst enriches ticket with comprehensive analysis'
    workflow: 'security-alert-enrichment-workflow.yaml (Story 3.1)'

  stage3_review:
    jira_status: 'In Review'
    description: 'Peer review validates enrichment quality'
    workflow: 'security-analysis-review-workflow.yaml (Story 3.2)'
    optional: 'Mandatory for P1/P2, sampling for P3/P4/P5 (Story 3.4)'

  stage4_remediation_planning:
    jira_status: 'Remediation Planning'
    description: 'DevOps/Engineering team plans patch deployment'

  stage5_remediation_execution:
    jira_status: 'Remediation In Progress'
    description: 'Deploy patches/workarounds to affected systems'

  stage6_verification:
    jira_status: 'Verification'
    description: 'Verify vulnerability successfully remediated'

  stage7_closure:
    jira_status: 'Closed'
    description: 'Close ticket and capture lessons learned'
```

## Metrics Captured per Stage

The following metrics are captured at each lifecycle stage and logged to `metrics/enrichment-metrics.csv`.

### Detection Stage Metrics

- `detection_timestamp` - When vulnerability first detected

### Enrichment Stage Metrics

- `enrichment_start_timestamp` - Analyst begins enrichment
- `enrichment_completion_timestamp` - Enrichment posted to JIRA
- `enrichment_duration_minutes` - Time spent on enrichment
- `enrichment_quality_score` - Self-assessed quality (optional)

### Review Stage Metrics (if review performed)

- `review_start_timestamp` - Reviewer begins review
- `review_completion_timestamp` - Review report posted
- `review_duration_minutes` - Time spent on review
- `review_quality_score` - Overall quality score (0-100)
- `gaps_found_critical` - Count of Critical gaps
- `gaps_found_significant` - Count of Significant gaps
- `gaps_found_minor` - Count of Minor gaps
- `review_decision` - Approved/Needs Revision

### Remediation Planning Metrics

- `remediation_planning_start` - Planning begins
- `remediation_planning_completion` - Plan approved

### Remediation Execution Metrics

- `remediation_execution_start` - Deployment begins
- `remediation_execution_completion` - Deployment complete

### Verification Metrics

- `verification_timestamp` - Verification performed
- `verification_status` - Pass/Fail

### Closure Metrics

- `closure_timestamp` - Ticket closed
- `total_lifecycle_duration_hours` - Detection to Closure
- `mttr_hours` - Mean Time To Remediate (Detection to Remediation Complete)

## Audit Trail Requirements

All vulnerability lifecycle activities must maintain complete audit trail:

1. **JIRA Comments Preserved**: All enrichment, review, and status change comments retained
2. **Enrichment Artifacts**: Saved to `expansion-packs/bmad-1898-engineering/enrichments/{ticket-id}-enrichment.md`
3. **Review Reports**: Saved to `expansion-packs/bmad-1898-engineering/reviews/{ticket-id}-review.md`
4. **Metrics Logging**: All stage metrics logged to `metrics/enrichment-metrics.csv`
5. **Timestamps**: All stage transitions timestamped in JIRA history
6. **Attribution**: Analyst/reviewer names recorded in JIRA assignee/comments
7. **Sampling Decisions**: Review sampling decisions logged to `metrics/review-decisions.csv`

## SLA Definitions

Priority-based SLAs drive remediation timelines:

| Priority | Severity | EPSS     | KEV | SLA Remediation Deadline |
| -------- | -------- | -------- | --- | ------------------------ |
| P1       | Critical | High     | Yes | 24 hours                 |
| P2       | High     | Medium+  | Any | 7 days                   |
| P3       | Medium   | Any      | No  | 30 days                  |
| P4       | Low      | Low      | No  | 90 days                  |
| P5       | Info     | Very Low | No  | Best effort (no SLA)     |

**Source:** Epic 1 Story 1.7 Multi-Factor Priority Assessment (lines 66-70)

> **Note:** These SLA values are the authoritative definitions from Story 1.7. Previous versions of this document contained incorrect values (P2: 72 hours, P3: 7 days, P4: 30 days, P5: 90 days) which have been corrected as of 2025-11-08.

## JIRA Workflow Diagram

```mermaid
graph TD
    A[Open] --> B[In Progress]
    B --> C{Review Required?}
    C -->|P1/P2 or Sampled| D[In Review]
    C -->|Skip Review| E[Remediation Planning]
    D --> F{Approved?}
    F -->|Critical Issues| B
    F -->|Approved| E
    E --> G[Remediation In Progress]
    G --> H[Verification]
    H --> I{Pass?}
    I -->|Fail| G
    I -->|Pass| J[Closed]

    style A fill:#f0f0f0
    style B fill:#e1f5ff
    style D fill:#fff4e1
    style E fill:#f0e1ff
    style G fill:#e1ffe1
    style H fill:#ffe1e1
    style J fill:#d0d0d0
```

## Integration with Atlassian MCP

BMAD-1898 uses Atlassian MCP server to interact with JIRA. Configure the following in your environment:

### Required MCP Tools

- `mcp__atlassian__getJiraIssue` - Read ticket data
- `mcp__atlassian__addCommentToJiraIssue` - Post enrichment/review comments
- `mcp__atlassian__updateJiraIssue` - Update custom fields
- `mcp__atlassian__transitionJiraIssue` - Change status

### Configuration in config.yaml

```yaml
jira:
  cloud_id: 'your-cloud-id-here'
  project_key: 'SEC' # Or your security project key

  custom_fields:
    cve_id: 'customfield_10001'
    cvss_score: 'customfield_10002'
    epss_score: 'customfield_10003'
    kev_status: 'customfield_10004'
    priority_level: 'customfield_10005'
    affected_systems: 'customfield_10006'
    acr_rating: 'customfield_10007'
    review_status: 'customfield_10008'
    quality_score: 'customfield_10009'

  workflow_statuses:
    open: 'Open'
    in_progress: 'In Progress'
    in_review: 'In Review'
    remediation_planning: 'Remediation Planning'
    remediation_in_progress: 'Remediation In Progress'
    verification: 'Verification'
    closed: 'Closed'
```

## Event Alert Issue Type (Epic 7)

### Overview

The Event Alert issue type supports security event investigation workflow for ICS/IDS/SIEM platform alerts (added in Epic 7: Testing & Validation - Event Investigation capabilities).

**Distinction from Vulnerability Issue Type:**

| Aspect                | Vulnerability Issue Type                | Event Alert Issue Type                            |
| --------------------- | --------------------------------------- | ------------------------------------------------- |
| **Trigger**           | CVE published, scanner detection        | ICS/IDS/SIEM platform alert triggered             |
| **Focus**             | Vulnerability impact assessment         | Disposition determination (TP/FP/BTP)             |
| **Timeline**          | Days to weeks (remediation planning)    | Minutes to hours (active incident investigation)  |
| **Primary Output**    | Remediation plan, priority calculation  | Disposition decision, escalation determination    |
| **Escalation**        | Based on priority (P1/P2 immediate)     | Based on disposition (TP → IR team escalation)    |
| **Agent**             | `security-analyst` (*enrich-ticket)     | `security-analyst` (*investigate-event)           |

### Required Custom Fields (Event Alert)

The following custom fields are specific to Event Alert issue type:

| Field Name             | Type          | Description                                          | Required | Source          |
| ---------------------- | ------------- | ---------------------------------------------------- | -------- | --------------- |
| Alert Platform         | Single Select | Detection platform (Claroty/Snort/Splunk/Other)     | Yes      | User input      |
| Alert Rule ID          | Text          | Platform-specific rule ID (e.g., Claroty #317)       | Yes      | User input      |
| Alert Severity         | Single Select | Platform severity (Critical/High/Medium/Low/Info)    | Yes      | Platform        |
| Detection Timestamp    | DateTime      | When alert was triggered                             | Yes      | Platform        |
| Source IP              | Text          | Source IP address of alert activity                  | No       | Platform        |
| Destination IP         | Text          | Destination IP address                               | No       | Platform        |
| Protocol               | Text          | Network protocol (SSH/HTTP/Modbus/etc)               | No       | Platform        |
| Affected Asset         | Text          | Asset involved in alert (HMI-01, PLC-02, etc)        | Yes      | User input      |
| Asset Criticality      | Single Select | Asset criticality (Critical/High/Medium/Low)         | Yes      | Config          |
| Disposition            | Single Select | Investigation result (TP/FP/BTP)                     | Yes      | Analyst         |
| Disposition Confidence | Single Select | Confidence level (High/Medium/Low)                   | Yes      | Analyst         |
| Escalation Required    | Single Select | Escalate to IR team? (Yes/No/Pending)                | Yes      | Analyst         |
| Investigation Duration | Number        | Minutes spent investigating (for metrics)            | No       | Automation      |
| Reviewer Agree         | Single Select | Reviewer disposition agreement (Agree/Disagree/N/A)  | No       | Reviewer        |
| Quality Score (Event)  | Number        | Review quality score 0-100 (7 dimensions)            | No       | Reviewer        |

**Single Select Field Values:**

```yaml
alert_platform:
  - Claroty
  - Snort
  - Splunk
  - Other

disposition:
  - True Positive (TP)
  - False Positive (FP)
  - Benign True Positive (BTP)

disposition_confidence:
  - High
  - Medium
  - Low

escalation_required:
  - Yes
  - No
  - Pending

reviewer_agree:
  - Agree
  - Disagree (see comments)
  - N/A (not reviewed)
```

### Event Alert Workflow Statuses

Event Alert investigations use a simplified workflow compared to vulnerability lifecycle:

| Status Name           | Description                                        | Duration (Typical) |
| --------------------- | -------------------------------------------------- | ------------------ |
| Open                  | Alert received, awaiting investigation             | < 5 minutes        |
| Investigating         | Analyst performing 5-stage investigation           | 15-25 minutes      |
| Under Review          | Peer review of investigation (optional)            | 20-25 minutes      |
| Awaiting Escalation   | TP confirmed, pending IR team handoff              | < 30 minutes       |
| Escalated to IR       | Incident response team handling (TP only)          | Hours to days      |
| Resolved              | Investigation complete, disposition documented     | N/A                |
| Closed                | Ticket closed (FP/BTP) or IR complete (TP)         | N/A                |

### Event Alert Workflow Diagram

```mermaid
graph TD
    A[Open] --> B[Investigating]
    B --> C{Disposition?}

    C -->|True Positive TP| D[Awaiting Escalation]
    D --> E[Escalated to IR]
    E --> F[Closed]

    C -->|False Positive FP| G{Review Required?}
    C -->|Benign TP BTP| G

    G -->|Yes| H[Under Review]
    H --> I{Reviewer Agrees?}
    I -->|Agree| J[Resolved]
    I -->|Disagree| B

    G -->|No| J
    J --> F

    style A fill:#f0f0f0
    style B fill:#e1f5ff
    style C fill:#fff4e1
    style D fill:#ffcccc
    style E fill:#ff9999
    style H fill:#fff4e1
    style J fill:#ccffcc
    style F fill:#d0d0d0
```

### Event Alert Workflow Transitions

| From Status       | To Status         | Trigger                                         | Automation |
| ----------------- | ----------------- | ----------------------------------------------- | ---------- |
| Open              | Investigating     | Analyst starts investigation                    | Manual     |
| Investigating     | Awaiting Escalation | Disposition = TP, escalation required         | Automated  |
| Investigating     | Under Review      | Disposition = FP/BTP, review required           | Manual     |
| Investigating     | Resolved          | Disposition = FP/BTP, review not required       | Manual     |
| Awaiting Escalation | Escalated to IR | IR team accepts handoff                         | Manual     |
| Under Review      | Resolved          | Reviewer agrees with disposition                | Manual     |
| Under Review      | Investigating     | Reviewer disagrees (return for re-investigation)| Manual     |
| Resolved          | Closed            | Final documentation complete                    | Manual     |
| Escalated to IR   | Closed            | IR investigation complete                       | Manual     |

### Escalation Logic

**True Positive (TP):**
```yaml
if disposition == "TP" and confidence in ["High", "Medium"]:
  status_transition: "Awaiting Escalation" → "Escalated to IR"
  notification: CISO, SOC Lead, Asset Owner
  actions:
    - Create IR incident ticket (link to event alert)
    - Preserve forensic evidence
    - Document containment recommendations
```

**False Positive (FP):**
```yaml
if disposition == "FP":
  status_transition: "Investigating" → "Resolved" (or "Under Review" if sampling required)
  notification: Detection Engineering Team
  actions:
    - Document root cause (signature tuning, misconfiguration)
    - Create tuning recommendation ticket
    - No IR escalation
```

**Benign True Positive (BTP):**
```yaml
if disposition == "BTP":
  status_transition: "Investigating" → "Resolved" (or "Under Review" if sampling required)
  notification: SOC Lead (informational)
  actions:
    - Document authorization trail (change ticket, asset owner)
    - Create detection exception ticket
    - No IR escalation
```

### Event Investigation Metrics

The following metrics are captured for event investigations (logged to `metrics/event-investigation-metrics.csv`):

```csv
ticket_id,alert_platform,alert_rule_id,alert_severity,detection_timestamp,
investigation_start,investigation_end,investigation_duration_minutes,
disposition,disposition_confidence,escalation_required,
evidence_sources_count,historical_context_gathered,business_context_gathered,
asset_owner_contacted,change_ticket_correlated,
reviewer_agree,review_quality_score,review_duration_minutes,
cognitive_bias_detected,closure_timestamp
```

### Configuration Example (config.yaml)

```yaml
jira:
  issue_types:
    event_alert:
      custom_fields:
        alert_platform: 'customfield_10020'
        alert_rule_id: 'customfield_10021'
        alert_severity: 'customfield_10022'
        detection_timestamp: 'customfield_10023'
        source_ip: 'customfield_10024'
        destination_ip: 'customfield_10025'
        protocol: 'customfield_10026'
        affected_asset: 'customfield_10027'
        asset_criticality: 'customfield_10028'
        disposition: 'customfield_10029'
        disposition_confidence: 'customfield_10030'
        escalation_required: 'customfield_10031'
        investigation_duration: 'customfield_10032'
        reviewer_agree: 'customfield_10033'
        quality_score_event: 'customfield_10034'

      workflow_statuses:
        open: 'Open'
        investigating: 'Investigating'
        under_review: 'Under Review'
        awaiting_escalation: 'Awaiting Escalation'
        escalated_to_ir: 'Escalated to IR'
        resolved: 'Resolved'
        closed: 'Closed'
```

### Audit Trail (Event Alerts)

Event alert investigations maintain similar audit trail to vulnerability enrichment:

1. **JIRA Comments:** Investigation reports posted as comments
2. **Investigation Artifacts:** `expansion-packs/bmad-1898-engineering/investigations/{ticket-id}-investigation.md`
3. **Review Reports:** `expansion-packs/bmad-1898-engineering/reviews/{ticket-id}-event-review.md`
4. **Metrics Logging:** `metrics/event-investigation-metrics.csv`
5. **Timestamps:** All status transitions logged in JIRA history
6. **Attribution:** Analyst/reviewer names in assignee/comments

### SLA Definitions (Event Alerts)

Event alerts use time-based SLAs (not priority-based like vulnerabilities):

| Alert Severity | Investigation SLA | Review SLA (if required) | Escalation SLA (TP only) |
| -------------- | ----------------- | ------------------------ | ------------------------ |
| Critical       | 1 hour            | 2 hours                  | Immediate (< 30 min)     |
| High           | 4 hours           | 8 hours                  | 1 hour                   |
| Medium         | 24 hours          | 48 hours                 | 4 hours                  |
| Low            | 72 hours          | N/A (no review)          | 8 hours                  |
| Info           | Best effort       | N/A                      | N/A                      |

**Note:** These SLAs are based on detection platform severity, NOT calculated priority. Event alerts require rapid response to determine if active attack is occurring.

---

## Validation Checklist

Before deploying BMAD-1898 workflows, validate JIRA configuration:

- [ ] All 7 required statuses exist in JIRA project
- [ ] All status transitions configured (9 forward + 2 reverse)
- [ ] All required custom fields created
- [ ] Custom field IDs documented in config.yaml
- [ ] JIRA Cloud ID configured in config.yaml
- [ ] Atlassian MCP server installed and authenticated
- [ ] Test ticket created and workflow executed end-to-end
- [ ] Metrics directory exists: `expansion-packs/bmad-1898-engineering/metrics/`
- [ ] Enrichment directory exists: `expansion-packs/bmad-1898-engineering/enrichments/`
- [ ] Review directory exists: `expansion-packs/bmad-1898-engineering/reviews/`

## References

- Epic 3: Workflow Integration and Orchestration (parent epic for workflow standards)
- Story 3.3: Vulnerability Lifecycle Workflow (implements these JIRA workflow standards)
- Story 3.1: Security Alert Enrichment Workflow (Enrichment stage)
- Story 3.2: Security Analysis Review Workflow (Review stage)
- Story 3.4: Priority-Based Review Triggering (Review decision logic)
- Epic 1 Story 1.7: Multi-Factor Priority Assessment (SLA definitions)

## Change Log

| Date       | Version | Description                                                                                                    | Author     |
| ---------- | ------- | -------------------------------------------------------------------------------------------------------------- | ---------- |
| 2025-11-08 | 1.1     | Corrected SLA definitions to match Story 1.7 (P2: 7d, P3: 30d, P4: 90d, P5: no SLA); previous values incorrect | Sarah (PO) |
| 2025-11-08 | 1.0     | Initial JIRA workflow standards document                                                                       | Sarah (PO) |

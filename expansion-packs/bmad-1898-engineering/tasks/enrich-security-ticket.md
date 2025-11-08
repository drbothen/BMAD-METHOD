# Enrich Security Ticket Task

## Purpose

Execute the complete Security Alert Enrichment Workflow from initial JIRA ticket triage through full vulnerability analysis and documentation. This task orchestrates all 8 workflow stages defined in `workflows/security-alert-enrichment-workflow.yaml`.

## Prerequisites

- Atlassian MCP server configured and connected
- Perplexity MCP server configured and connected
- JIRA configuration in `config.yaml` with required fields
- Security Analyst agent activated
- Valid JIRA ticket ID with security alert

## Workflow Overview

This task executes an 8-stage enrichment workflow:

1. **Triage** - Extract CVE and context from JIRA ticket
2. **CVE Research** - AI-assisted vulnerability intelligence gathering
3. **Business Context** - Asset criticality and exposure assessment
4. **Remediation Planning** - Patch/workaround identification
5. **MITRE ATT&CK Mapping** - Tactical analysis and technique mapping
6. **Priority Assessment** - Multi-factor priority calculation
7. **Documentation** - Structured enrichment document generation
8. **JIRA Update** - Ticket enrichment and validation

**Target Duration:** 10-15 minutes

## Task Execution

### Initial Setup

1. **Load workflow definition:**
   - Read `workflows/security-alert-enrichment-workflow.yaml`
   - Validate workflow structure and stage definitions
   - Initialize workflow state tracking

2. **Validate dependencies:**
   - Verify all required Epic 1 tasks exist before workflow execution
   - Required tasks:
     - `tasks/read-jira-ticket.md` (Stage 1)
     - `tasks/research-cve.md` (Stage 2)
     - `tasks/assess-vulnerability-priority.md` (Stage 6)
     - `tasks/post-enrichment-comment.md` (Stage 8)
     - `tasks/update-jira-fields.md` (Stage 8)
   - Verify required template exists:
     - `templates/security-enrichment-tmpl.yaml` (Stage 7)
   - If any dependencies missing, HALT with error:
     - "Missing required dependencies: {list}. Please ensure Epic 1 tasks are available."

3. **Check for resume state:**
   - Look for `.workflow-state/{ticket-id}.json` progress file
   - If found, ask user: "Resume from Stage {X}? (y/n)"
   - If yes, load saved state and skip to last incomplete stage
   - If no or not found, start fresh from Stage 1

4. **Elicit ticket ID:**
   - Ask: "Please provide the JIRA ticket ID to enrich (e.g., AOD-1234):"
   - Validate format: `{PROJECT_KEY}-{NUMBER}`
   - Store ticket ID for workflow tracking

### Progress Tracking Display

Display and update progress throughout workflow execution:

```
🔄 Security Alert Enrichment Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Stage 1: Triage (completed in 1m 23s)
✅ Stage 2: CVE Research (completed in 4m 12s)
🔄 Stage 3: Business Context (in progress...)
⏳ Stage 4: Remediation Planning
⏳ Stage 5: MITRE ATT&CK
⏳ Stage 6: Priority Assessment
⏳ Stage 7: Documentation
⏳ Stage 8: JIRA Update
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Elapsed: 5m 35s | Estimated Remaining: 6m
```

**Status Indicators:**
- ✅ = Completed successfully
- 🔄 = Currently executing
- ⏳ = Pending
- ❌ = Failed (with retry available)
- ⚠️ = Completed with warnings

### Stage 1: Triage & Context Extraction

**Duration:** 1-2 minutes

**Actions:**
1. Execute task: `read-jira-ticket.md`
2. Extract CVE ID(s) from ticket (summary, description, custom fields)
3. Extract affected systems from custom fields
4. Extract initial severity and context metadata

**Outputs to collect:**
- `cve_id` (primary CVE)
- `all_cves` (array of all CVEs found)
- `affected_systems` (array)
- `initial_severity` (if present)
- `ticket_summary`
- `ticket_description`

**Error Handling:**
- If no CVE found: Prompt user for CVE ID
- If ticket not found: Validate ticket ID and retry
- If MCP error: Check connection and retry once

**Save progress:** Write state to `.workflow-state/{ticket-id}.json`

### Stage 2: AI-Assisted CVE Research

**Duration:** 3-5 minutes

**Actions:**
1. Execute task: `research-cve.md` with primary CVE
2. Use Perplexity MCP for comprehensive research
3. Gather CVSS, EPSS, KEV status, exploits, patches, ATT&CK suggestions

**Inputs:**
- `cve_id` from Stage 1

**Outputs to collect:**
- `cvss_score`
- `cvss_vector`
- `cvss_severity`
- `epss_score`
- `kev_status`
- `affected_versions`
- `patched_versions`
- `exploit_status`
- `attack_suggestions` (MITRE ATT&CK)
- `authoritative_sources` (links)

**Error Handling:**
- Perplexity timeout: Retry with simplified query
- No data found: Attempt manual fallback or prompt user
- Rate limit: Wait and retry with exponential backoff

**Save progress:** Update state file

### Stage 3: Business Context Assessment

**Duration:** 2-3 minutes

**Actions:**
1. Load config from `config.yaml`
2. Extract Asset Criticality Rating (ACR) from JIRA custom field or config
3. Determine system exposure classification
4. Assess business impact dimensions

**Inputs:**
- `affected_systems` from Stage 1
- `cvss_score` from Stage 2
- JIRA custom fields

**Outputs to collect:**
- `acr_rating` (Critical/High/Medium/Low)
- `system_exposure` (Internet-facing/Internal/Isolated)
- `business_impact` (availability, confidentiality, integrity)
- `affected_processes` (optional)

**Error Handling:**
- ACR not found: Prompt user or default to "Medium"
- Exposure unknown: Prompt user for classification

**Save progress:** Update state file

### Stage 4: Remediation Planning

**Duration:** 2-3 minutes

**Actions:**
1. Use CVE research data to identify patches
2. Research workarounds if no patch available
3. Identify compensating controls based on vulnerability type
4. Generate actionable remediation steps

**Inputs:**
- `cvss_score`, `affected_versions`, `patched_versions` from Stage 2
- `business_impact` from Stage 3

**Outputs to collect:**
- `patch_available` (boolean)
- `patch_version`
- `patch_url`
- `workarounds` (array)
- `compensating_controls` (array)
- `remediation_steps` (numbered action items)

**Error Handling:**
- No patch info: Note as "No patch available yet"
- Workaround research fails: Document manual investigation needed

**Save progress:** Update state file

### Stage 5: MITRE ATT&CK Mapping

**Duration:** 1-2 minutes

**Actions:**
1. Use CVE intelligence and vulnerability type to map tactics
2. Identify specific ATT&CK techniques (T-numbers)
3. Add detection implications and defense recommendations

**Inputs:**
- `cvss_vector` from Stage 2
- `attack_suggestions` from Stage 2
- Vulnerability type (RCE, SQLi, XSS, etc.)

**Outputs to collect:**
- `attack_tactics` (array, e.g., "Initial Access", "Execution")
- `attack_techniques` (array with T-numbers, e.g., "T1190 - Exploit Public-Facing Application")
- `detection_implications` (guidance for detection)

**Error Handling:**
- No mapping found: Use generic mapping based on vulnerability type
- Research timeout: Use cached/default mappings

**Save progress:** Update state file

### Stage 6: Multi-Factor Priority Assessment

**Duration:** 1-2 minutes

**Actions:**
1. Execute task: `assess-vulnerability-priority.md`
2. Calculate priority using multi-factor algorithm
3. Generate priority rationale
4. Calculate SLA deadline

**Inputs:**
- `cvss_score` from Stage 2
- `epss_score` from Stage 2
- `kev_status` from Stage 2
- `acr_rating` from Stage 3
- `system_exposure` from Stage 3
- `exploit_status` from Stage 2

**Outputs to collect:**
- `priority_level` (P1/P2/P3/P4/P5)
- `priority_score` (numeric)
- `priority_rationale` (explanation)
- `sla_deadline` (date/time)

**Error Handling:**
- Missing factors: Use defaults and note in rationale
- Calculation error: Use conservative priority (higher)

**Save progress:** Update state file

### Stage 7: Structured Documentation

**Duration:** 1 minute

**Actions:**
1. Load template: `templates/security-enrichment-tmpl.yaml`
2. Populate all 12 template sections with collected data
3. Generate markdown document
4. Validate completeness (all sections present)

**Inputs:**
- All data collected from Stages 1-6

**Outputs to collect:**
- `enrichment_document` (markdown string)
- `enrichment_filename` (e.g., `{ticket-id}-enrichment.md`)

**Validation:**
- Verify all 12 template sections populated
- Verify executive summary generated
- Check for missing data markers (e.g., "N/A", "Unknown")

**Error Handling:**
- Template missing: HALT and notify user
- Section population fails: Note incomplete and continue

**Save progress:** Update state file

### Stage 8: JIRA Update & Validation

**Duration:** 1-2 minutes

**Actions:**
1. Execute task: `post-enrichment-comment.md` to add enrichment document
2. Execute task: `update-jira-fields.md` to update custom fields
3. Save enrichment document locally to artifacts directory
4. Validate all updates succeeded

**Inputs:**
- `enrichment_document` from Stage 7
- `priority_level` from Stage 6
- Structured data: `cvss_score`, `epss_score`, `kev_status`, etc.

**Actions:**
1. Post enrichment as JIRA comment:
   ```
   mcp__atlassian__addCommentToJiraIssue
     issueKey: {ticket_id}
     comment: {enrichment_document}
     cloudId: {from_config}
   ```

2. Update JIRA custom fields:
   ```
   mcp__atlassian__updateJiraIssue
     issueKey: {ticket_id}
     fields:
       priority: {priority_level}
       customfield_cvss_score: {cvss_score}
       customfield_epss_score: {epss_score}
       customfield_kev_status: {kev_status}
   ```

3. Save enrichment locally:
   - Directory: `artifacts/enrichments/`
   - Filename: `{ticket-id}-enrichment-{timestamp}.md`
   - Create directory if not exists

**Outputs:**
- JIRA comment posted (verify comment ID returned)
- Custom fields updated (verify update success)
- Local file saved (verify file exists)

**Error Handling:**
- Comment post fails: Save locally and notify user
- Field update fails: Continue with partial update, log errors
- Local save fails: HALT and notify (critical for audit trail)

**Save progress:** Update state file with completion

### Workflow Completion

**Upon successful completion of all 8 stages:**

1. Display completion summary:
   ```
   ✅ Security Alert Enrichment Complete!
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Ticket: {ticket_id}
   CVE: {cve_id}
   Priority: {priority_level} ({priority_rationale})
   Duration: {total_time}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   JIRA ticket enriched successfully.
   Enrichment saved to: artifacts/enrichments/{filename}
   ```

2. Clean up workflow state:
   - Archive state file to `.workflow-state/completed/{ticket-id}-{timestamp}.json`
   - Remove active state file

3. Prompt user for next action:
   - "Enrich another ticket? (y/n)"
   - If yes, restart workflow
   - If no, return to agent prompt

## Error Recovery & Retry Logic

### Automatic Retry

For transient errors (network, rate limits, timeouts):

1. **First failure:** Wait 10 seconds, retry
2. **Second failure:** Wait 30 seconds, retry
3. **Third failure:** Prompt user to continue or abort

### Manual Recovery

For permanent errors (authentication, missing data):

1. Display error with context
2. Suggest resolution steps
3. Prompt user: "Retry / Skip stage / Abort workflow?"
4. If skip: Mark stage incomplete in state, continue with warnings

### Resume from Failure

When workflow is interrupted:

1. State file preserved at `.workflow-state/{ticket-id}.json`
2. On next execution, detect incomplete workflow
3. Display: "Incomplete workflow found for {ticket_id}. Resume from Stage {X}? (y/n)"
4. If yes, load all collected data and continue
5. If no, archive old state and start fresh

## State Management

### State File Structure

```json
{
  "workflow_id": "security-alert-enrichment-v1",
  "ticket_id": "AOD-1234",
  "started_at": "2025-11-08T10:30:00Z",
  "current_stage": 3,
  "stages_completed": [1, 2],
  "stages_failed": [],
  "total_elapsed_seconds": 335,
  "data": {
    "stage1": { "cve_id": "CVE-2024-1234", "affected_systems": [...] },
    "stage2": { "cvss_score": 9.8, "epss_score": 0.75, ... },
    "stage3": { "acr_rating": "High", ... }
  }
}
```

### State Operations

- **Save:** Write state after each stage completion
- **Load:** Read state on workflow start if exists
- **Archive:** Move to `completed/` directory on success
- **Cleanup:** Remove on explicit user request or after 30 days

## Performance Targets

- **Total Duration:** 10-15 minutes (95th percentile)
- **Stage 1:** 1-2 minutes
- **Stage 2:** 3-5 minutes (AI research)
- **Stage 3:** 2-3 minutes
- **Stage 4:** 2-3 minutes
- **Stage 5:** 1-2 minutes
- **Stage 6:** 1-2 minutes
- **Stage 7:** 1 minute
- **Stage 8:** 1-2 minutes

**Monitoring:** Track actual durations and compare to targets. Log warnings if stage exceeds 2x target duration.

## Quality Validation

Before marking workflow complete, validate:

- ✅ All 8 stages completed successfully
- ✅ All 12 template sections populated
- ✅ JIRA comment posted
- ✅ JIRA custom fields updated
- ✅ Local enrichment file saved
- ✅ Priority level assigned with rationale
- ✅ CVE research includes CVSS, EPSS, KEV
- ✅ ATT&CK mapping has at least one tactic/technique
- ✅ Remediation guidance provided

**Quality Score Calculation:**
- Total checks: 9
- Passed checks / Total checks = Quality %
- Target: >75% (7+ checks passing)

If quality score <75%, display warning and suggest review.

## Usage Examples

### Basic Usage

```
*enrich-ticket AOD-1234
```

### Resume After Interruption

```
*enrich-ticket AOD-1234
> Incomplete workflow found. Resume from Stage 5? (y/n)
y
> Resuming from Stage 5: MITRE ATT&CK Mapping...
```

### Batch Processing

```
*enrich-ticket AOD-1234
> Workflow complete. Enrich another ticket? (y/n)
y
> Please provide the JIRA ticket ID to enrich:
AOD-1235
```

## Integration Points

This task orchestrates and depends on:

- **Tasks:**
  - `read-jira-ticket.md` (Stage 1)
  - `research-cve.md` (Stage 2)
  - `assess-vulnerability-priority.md` (Stage 6)
  - `post-enrichment-comment.md` (Stage 8)
  - `update-jira-fields.md` (Stage 8)

- **Templates:**
  - `security-enrichment-tmpl.yaml` (Stage 7)

- **Workflows:**
  - `security-alert-enrichment-workflow.yaml` (definition)

- **MCP Servers:**
  - Atlassian MCP (JIRA operations)
  - Perplexity MCP (AI research)

## Notes

- This is an operational workflow task designed for runtime execution
- State management enables resume capability for long-running workflows
- Progress tracking provides visibility into workflow execution
- Error handling ensures graceful degradation and recovery
- Quality validation ensures consistent output standards

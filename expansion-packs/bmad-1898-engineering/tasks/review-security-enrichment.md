# Review Security Enrichment Task

## Purpose

Execute the complete Security Analysis Review Workflow for systematic peer review of security enrichments. This task orchestrates all 7 workflow stages defined in `workflows/security-analysis-review-workflow.yaml` to ensure quality assurance is thorough and constructive.

## Prerequisites

- Atlassian MCP server configured and connected
- (Optional) Perplexity MCP server for fact verification
- JIRA configuration in `config.yaml` with required fields
- Security Reviewer agent activated
- Valid JIRA ticket ID with completed enrichment (Story 3.1)
- All 8 quality dimension checklists available in `checklists/`

## Workflow Overview

This task executes a 7-stage review workflow:

1. **Preparation** - Extract enrichment from JIRA ticket and parse structure
2. **Systematic Evaluation** - Execute 8 quality dimension checklists
3. **Gap Identification** - Categorize findings as Critical/Significant/Minor
4. **Bias Detection** - Identify cognitive biases with debiasing strategies
5. **Fact Verification (Optional)** - Verify claims against authoritative sources
6. **Documentation** - Generate constructive review report
7. **Feedback Loop** - Post review to JIRA and notify analyst

**Target Duration:** 15-20 minutes

## Task Execution

### Initial Setup

1. **Load workflow definition:**
   - Read `workflows/security-analysis-review-workflow.yaml`
   - Validate workflow structure and stage definitions
   - Initialize workflow state tracking

2. **Validate dependencies:**
   - Verify all 8 quality checklists exist:
     - `checklists/technical-accuracy-checklist.md`
     - `checklists/completeness-checklist.md`
     - `checklists/actionability-checklist.md`
     - `checklists/contextualization-checklist.md`
     - `checklists/documentation-quality-checklist.md`
     - `checklists/attack-mapping-validation-checklist.md`
     - `checklists/cognitive-bias-checklist.md`
     - `checklists/source-citation-checklist.md`
   - Verify required template exists:
     - `templates/security-review-report-tmpl.yaml`
   - Verify required tasks exist:
     - `tasks/categorize-review-findings.md` (Stage 3)
     - `tasks/fact-verify-claims.md` (Stage 5, optional)
   - If any dependencies missing, HALT with error:
     - "Missing required dependencies: {list}. Please ensure Epic 2 tasks are available."

3. **Validate MCP availability:**
   - Check Atlassian MCP connection (REQUIRED)
   - If unavailable: HALT with "Atlassian MCP required for review workflow"
   - Check Perplexity MCP connection (OPTIONAL)
   - If unavailable: Log warning "Fact verification will be skipped - Perplexity MCP not available"

4. **Check for resume state:**
   - Look for `.workflow-state/review-{ticket-id}.json` progress file
   - If found, ask user: "Resume review from Stage {X}? (y/n)"
   - If yes, load saved state and skip to last incomplete stage
   - If no or not found, start fresh from Stage 1

5. **Elicit ticket ID:**
   - Ask: "Please provide the JIRA ticket ID to review (e.g., AOD-1234):"
   - Validate format: `{PROJECT_KEY}-{NUMBER}`
   - Store ticket ID for workflow tracking

6. **Elicit fact verification preference:**
   - If Perplexity MCP available, ask: "Perform optional fact verification? (y/n)"
   - If yes: Set `perform_fact_verification = true`
   - If no: Set `perform_fact_verification = false`
   - If Perplexity unavailable: Set `perform_fact_verification = false` automatically

### Progress Tracking Display

Display and update progress throughout workflow execution:

```
🔍 Security Analysis Review Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Stage 1: Preparation (completed in 2m 15s)
✅ Stage 2: Systematic Evaluation (completed in 6m 30s)
🔄 Stage 3: Gap Identification (in progress...)
⏳ Stage 4: Bias Detection
⏳ Stage 5: Fact Verification (optional)
⏳ Stage 6: Documentation
⏳ Stage 7: Feedback Loop
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Elapsed: 8m 45s | Estimated Remaining: 8m
```

**Status Indicators:**

- ✅ = Completed successfully
- 🔄 = Currently executing
- ⏳ = Pending
- ⏭️ = Skipped (optional stage not performed)
- ❌ = Failed (with retry available)
- ⚠️ = Completed with warnings

### Stage 1: Review Preparation

**Duration:** 2-3 minutes

**Actions:**

1. Read JIRA ticket via Atlassian MCP
2. Extract analyst enrichment comment (posted by Story 3.1 workflow)
3. Parse enrichment structure (markdown sections)
4. Extract factual claims for potential verification

**MCP Operations:**

```
mcp__atlassian__getJiraIssue
  issueKey: {ticket_id}
  cloudId: {from_config}
  expand: ["comments"]
```

**Enrichment Extraction:**

- Locate enrichment comment (look for "Security Analysis Enrichment" heading)
- Parse markdown structure (12 expected sections from security-enrichment-tmpl.yaml)
- Extract analyst name from comment author field
- Extract enrichment timestamp

**Claims Extraction:**
Extract these verifiable claims for Stage 5:

- CVSS score and vector
- EPSS score
- CISA KEV status
- Affected versions
- Patched versions
- MITRE ATT&CK technique IDs

**Outputs to collect:**

- `enrichment_document` (full markdown text)
- `enrichment_sections` (parsed dict of sections)
- `claims_list` (array of factual claims with sources)
- `analyst_name` (comment author)
- `enrichment_timestamp` (comment created date)

**Error Handling:**

- Ticket not found: Prompt user to verify ticket ID and retry
- Enrichment comment not found: HALT with "No enrichment found. Ensure Story 3.1 workflow completed for this ticket."
- MCP connection error: Retry once, then HALT with clear error message
- Malformed enrichment: Log warning but continue (gaps will be caught in evaluation)

**Save progress:** Write state to `.workflow-state/review-{ticket-id}.json`

### Stage 2: Systematic Quality Evaluation

**Duration:** 5-7 minutes

**Actions:**

1. Execute all 8 quality dimension checklists against enrichment
2. Calculate individual dimension scores (0-100%)
3. Calculate weighted overall quality score
4. Classify quality level (Excellent/Good/Needs Improvement/Inadequate)

**Checklist Execution Sequence:**

For each checklist, execute the checklist items and score results:

1. **Technical Accuracy (25% weight):**
   - Execute `checklists/technical-accuracy-checklist.md`
   - Check CVSS accuracy, metric correctness, factual claims
   - Score: (passed items / total items) × 100

2. **Completeness (20% weight):**
   - Execute `checklists/completeness-checklist.md`
   - Check all 12 required sections present and substantive
   - Score: (passed items / total items) × 100

3. **Actionability (15% weight):**
   - Execute `checklists/actionability-checklist.md`
   - Check remediation steps specific and executable
   - Score: (passed items / total items) × 100

4. **Contextualization (15% weight):**
   - Execute `checklists/contextualization-checklist.md`
   - Check business context and impact analysis present
   - Score: (passed items / total items) × 100

5. **Documentation Quality (10% weight):**
   - Execute `checklists/documentation-quality-checklist.md`
   - Check structure, clarity, formatting, professionalism
   - Score: (passed items / total items) × 100

6. **MITRE ATT&CK Mapping (5% weight):**
   - Execute `checklists/attack-mapping-validation-checklist.md`
   - Check ATT&CK tactics/techniques correctly mapped
   - Score: (passed items / total items) × 100

7. **Cognitive Bias Detection (5% weight):**
   - Execute `checklists/cognitive-bias-checklist.md`
   - Check for confirmation bias, anchoring, etc.
   - Score: (passed items / total items) × 100

8. **Source Citation (5% weight):**
   - Execute `checklists/source-citation-checklist.md`
   - Check authoritative sources cited correctly
   - Score: (passed items / total items) × 100

**Overall Score Calculation:**

```
overall_score =
  (technical_accuracy × 0.25) +
  (completeness × 0.20) +
  (actionability × 0.15) +
  (contextualization × 0.15) +
  (documentation_quality × 0.10) +
  (attack_mapping × 0.05) +
  (cognitive_bias × 0.05) +
  (source_citation × 0.05)
```

**Quality Classification:**

- **Excellent:** ≥90% overall score
- **Good:** 75-89% overall score
- **Needs Improvement:** 60-74% overall score
- **Inadequate:** <60% overall score

**Outputs to collect:**

- `dimension_scores` (dict with 8 scores)
- `overall_score` (0-100 percentage)
- `quality_classification` (string)
- `checklist_results` (dict with passed/failed items per checklist)

**Error Handling:**

- Checklist file missing: HALT with "Missing checklist: {name}. Ensure Epic 2 complete."
- Checklist execution error: Log error, assign 0% score to that dimension, continue
- All checklists fail: HALT with "Unable to execute quality evaluation"

**Save progress:** Update state file

### Stage 3: Gap Identification & Categorization

**Duration:** 3-4 minutes

**Actions:**

1. Execute task: `categorize-review-findings.md`
2. Categorize each failed checklist item by severity
3. Specify location in enrichment where gap occurs
4. Explain impact of each gap
5. Provide specific recommended fix
6. Link to learning resources

**Inputs:**

- `checklist_results` from Stage 2 (all failed items)
- `enrichment_sections` from Stage 1

**Categorization Rules:**

**Critical Issues:**

- Factual errors (incorrect CVSS, EPSS, KEV status)
- Missing or incorrect priority assessment
- Incorrect or misleading security metrics
- Dangerous or incorrect remediation advice
- Missing executive summary or priority

**Significant Gaps:**

- Missing business context analysis
- Incomplete remediation guidance (no steps or vague steps)
- MITRE ATT&CK mapping errors or omissions
- Missing or weak source citations
- Incomplete vulnerability description

**Minor Improvements:**

- Formatting inconsistencies
- Spelling or grammar errors
- Optional enhancements (additional context could be helpful)
- Style improvements

**For Each Gap, Document:**

- Severity: Critical / Significant / Minor
- Location: Specific section name and line reference
- Description: What is missing or incorrect
- Impact: Why this matters for security operations
- Recommendation: Specific fix to apply
- Learning Resource: Link to guide or best practice

**Outputs to collect:**

- `critical_issues` (array of gap objects)
- `significant_gaps` (array of gap objects)
- `minor_improvements` (array of gap objects)
- `total_gaps` (count across all severities)

**Error Handling:**

- Categorization task fails: Perform basic categorization inline
- No gaps found: Set all arrays to empty, continue

**Save progress:** Update state file

### Stage 4: Cognitive Bias Detection

**Duration:** 2-3 minutes

**Actions:**

1. Analyze enrichment for cognitive biases
2. Identify specific examples of bias in text
3. Explain impact of detected biases
4. Suggest debiasing strategies

**Bias Types to Check:**

1. **Confirmation Bias:**
   - Selectively emphasizing evidence that confirms initial severity assessment
   - Ignoring contradictory evidence (e.g., low EPSS despite high CVSS)
   - Example: "High CVSS proves this is critical" (ignoring lack of exploit activity)

2. **Anchoring Bias:**
   - Over-relying on first piece of information (often CVSS score)
   - Not adjusting assessment despite additional context
   - Example: Prioritizing based on CVSS alone, ignoring low KEV/EPSS

3. **Availability Heuristic:**
   - Overweighting recent or memorable incidents
   - "This is like Log4Shell" comparisons without technical similarity
   - Example: Treating all remote code execution as equally severe

4. **Overconfidence Bias:**
   - Excessive certainty without sufficient evidence
   - Absolute statements ("This will definitely be exploited")
   - Example: "Exploit is imminent" without evidence

5. **Recency Bias:**
   - Giving too much weight to recent events
   - Ignoring historical patterns or older but relevant data
   - Example: Focusing only on recent CVEs, ignoring relevant older vulnerabilities

**For Each Detected Bias:**

- Type: Name of bias
- Evidence: Specific quote or section exhibiting bias
- Impact: How this could affect decision-making
- Debiasing Strategy: Specific recommendation to counteract

**Outputs to collect:**

- `detected_biases` (array of bias objects)
- `bias_count` (total biases detected)
- `bias_assessment_summary` (constructive summary)

**Error Handling:**

- No biases detected: Set empty array, note "No significant cognitive biases detected"
- Bias detection unclear: Mark as "Possible bias" with lower confidence

**Save progress:** Update state file

### Stage 5: Fact Verification (Optional)

**Duration:** 3-5 minutes (if performed)

**Prerequisite:** `perform_fact_verification = true` and Perplexity MCP available

**Actions:**

1. Execute task: `fact-verify-claims.md`
2. Verify each factual claim against authoritative sources
3. Compare analyst claims with verified data
4. Document discrepancies with corrections
5. Calculate accuracy score

**Claims to Verify:**

For each claim type, use Perplexity MCP to verify against authoritative source:

1. **CVSS Score:**
   - Claim: {analyst_cvss_score}
   - Source: NVD (https://nvd.nist.gov/)
   - Query: "Verify CVSS base score for {cve_id} from NVD"

2. **EPSS Score:**
   - Claim: {analyst_epss_score}
   - Source: FIRST (https://www.first.org/epss/)
   - Query: "Current EPSS score for {cve_id} from FIRST.org"

3. **CISA KEV Status:**
   - Claim: {analyst_kev_status}
   - Source: CISA KEV Catalog (https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
   - Query: "Is {cve_id} listed in CISA KEV catalog?"

4. **Affected Versions:**
   - Claim: {analyst_affected_versions}
   - Source: Vendor advisory or NVD
   - Query: "Affected versions for {cve_id} from official vendor advisory"

5. **Patched Versions:**
   - Claim: {analyst_patched_versions}
   - Source: Vendor advisory or NVD
   - Query: "Patched versions for {cve_id} from official vendor advisory"

6. **MITRE ATT&CK Techniques:**
   - Claim: {analyst_attack_techniques}
   - Source: MITRE ATT&CK (https://attack.mitre.org/)
   - Query: "Verify ATT&CK technique {technique_id} is correct for {vulnerability_type}"

**MCP Operations:**

```
mcp__perplexity__search (for straightforward factual lookups)
  query: {verification_query}
  force_model: false

mcp__perplexity__reason (for complex comparisons)
  query: "Compare analyst claim '{claim}' with authoritative source data for accuracy"
  force_model: false
```

**Discrepancy Documentation:**

For each discrepancy found:

- Claim: What analyst stated
- Actual: Verified correct value
- Source: Authoritative source URL
- Severity: Critical / Significant / Minor
- Impact: How this affects remediation decisions

**Accuracy Score Calculation:**

```
accuracy_score = (verified_correct_claims / total_claims_checked) × 100
```

**Outputs to collect:**

- `claims_verified` (count)
- `claims_correct` (count)
- `accuracy_score` (percentage)
- `discrepancies` (array of discrepancy objects)
- `verification_sources` (dict of sources used)

**Error Handling:**

- Perplexity timeout: Skip individual claim, mark as "Not Verified"
- Source unavailable: Note in discrepancies, mark as "Unable to Verify"
- Rate limit: Wait and retry with exponential backoff (max 3 retries)
- All verifications fail: Log warning, set accuracy_score = "N/A", continue

**If Skipped (Perplexity unavailable):**

- Set `fact_verification_performed = false`
- Log: "Fact verification skipped - Perplexity MCP not available"
- Set all outputs to null/empty

**Save progress:** Update state file

### Stage 6: Review Report Documentation

**Duration:** 2-3 minutes

**Actions:**

1. Load template: `templates/security-review-report-tmpl.yaml`
2. Populate all required sections with review findings
3. Start with strengths (positive acknowledgment)
4. Document gaps constructively with specific recommendations
5. Maintain blameless tone throughout
6. Generate markdown review report

**Inputs:**

- All data from Stages 1-5

**Template Sections to Populate:**

1. **Review Metadata:**

   ```yaml
   ticket_id: { ticket_id }
   cve_id: { extracted from enrichment }
   enrichment_timestamp: { enrichment_timestamp }
   reviewer_name: { current_agent_name }
   review_date: { current_timestamp }
   review_workflow_version: '1.0'
   ```

2. **Executive Summary:**
   - Quality classification: {quality_classification}
   - Overall score: {overall_score}%
   - High-level summary: 2-3 sentences summarizing key findings

3. **Strengths:**
   - List 3-5 positive aspects from enrichment
   - Acknowledge what analyst did well
   - Examples: "Thorough remediation steps", "Excellent source citations", "Clear business context"

4. **Quality Scores:**

   ```
   Technical Accuracy: {technical_accuracy}% (25% weight)
   Completeness: {completeness}% (20% weight)
   Actionability: {actionability}% (15% weight)
   Contextualization: {contextualization}% (15% weight)
   Documentation Quality: {documentation_quality}% (10% weight)
   MITRE ATT&CK Mapping: {attack_mapping}% (5% weight)
   Cognitive Bias Detection: {cognitive_bias}% (5% weight)
   Source Citation: {source_citation}% (5% weight)

   Overall Quality Score: {overall_score}%
   ```

5. **Critical Issues:** (if any)
   - List each critical issue with location, impact, recommendation
   - If none: "✅ No critical issues identified"

6. **Significant Gaps:** (if any)
   - List each significant gap with location, impact, recommendation
   - If none: "✅ No significant gaps identified"

7. **Minor Improvements:** (if any)
   - List minor improvements as optional suggestions
   - If none: "No minor improvements needed"

8. **Cognitive Bias Assessment:**
   - List detected biases with examples and debiasing strategies
   - If none: "✅ No significant cognitive biases detected"

9. **Fact Verification Results:** (if performed)
   - Accuracy score: {accuracy_score}%
   - Claims verified: {claims_verified}
   - Discrepancies: List each discrepancy with correction
   - If not performed: "ℹ️ Fact verification was not performed for this review"

10. **Recommendations:**
    - Prioritized action items for analyst
    - Order: Critical fixes → Significant improvements → Minor suggestions
    - Each recommendation specific and actionable

11. **Learning Resources:**
    - Links to relevant guides, best practices, knowledge base articles
    - Customized to address identified gaps

12. **Next Steps:**
    - If Critical Issues: "Status changed to 'Needs Revision' - please address critical issues and re-submit"
    - If Significant Gaps: "Please review significant gaps and update enrichment"
    - If Minor only: "Optional improvements suggested - proceed with remediation planning"
    - If Excellent: "Approved - excellent work! Ready for remediation planning"

**Tone Guidelines:**

- **Constructive:** Explain why, not just what
- **Specific:** Provide examples and exact recommendations
- **Blameless:** Focus on improvement, not criticism
- **Balanced:** Acknowledge strengths before gaps
- **Actionable:** Every finding has a clear next step
- **Educational:** Link to resources for learning

**Output:**

- `review_report_markdown` (complete markdown document)
- `review_filename` (e.g., `{ticket-id}-review-{timestamp}.md`)

**Error Handling:**

- Template missing: HALT with "Review template required: templates/security-review-report-tmpl.yaml"
- Section population fails: Use placeholder text and log warning

**Save progress:** Update state file

### Stage 7: Feedback Loop & JIRA Integration

**Duration:** 1 minute

**Actions:**

1. Post review report as JIRA comment
2. Update ticket status based on findings
3. Assign ticket back to original analyst
4. Save review report to artifacts/ directory
5. Log workflow metrics to metrics/ directory

**JIRA Operations:**

1. **Post Review Comment:**

   ```
   mcp__atlassian__addCommentToJiraIssue
     issueKey: {ticket_id}
     comment: {review_report_markdown}
     cloudId: {from_config}
   ```

2. **Update Ticket Status:**
   - If `critical_issues` > 0: Change status to "Needs Revision"
   - If `significant_gaps` > 0 and no critical: Change status to "In Review"
   - If only minor improvements: Change status to "Approved"
   - If no issues: Change status to "Approved"

   ```
   mcp__atlassian__updateJiraIssue
     issueKey: {ticket_id}
     fields:
       status: {new_status}
     cloudId: {from_config}
   ```

3. **Assign to Analyst:**
   ```
   mcp__atlassian__updateJiraIssue
     issueKey: {ticket_id}
     fields:
       assignee: {analyst_name}
     cloudId: {from_config}
   ```

**File System Operations:**

1. **Save Review Report:**
   - Directory: `artifacts/reviews/`
   - Filename: `{ticket-id}-review-{timestamp}.md`
   - Content: {review_report_markdown}
   - Create directory if not exists

2. **Log Workflow Metrics:**
   - Directory: `metrics/`
   - Filename: `review-metrics-{date}.jsonl` (append mode)
   - Record:
     ```json
     {
       "workflow_id": "security-analysis-review-v1",
       "ticket_id": "{ticket_id}",
       "reviewer": "{reviewer_name}",
       "review_date": "{timestamp}",
       "total_duration_seconds": {total_time},
       "stage_durations": {stage_times},
       "overall_score": {overall_score},
       "quality_classification": "{classification}",
       "critical_issues": {count},
       "significant_gaps": {count},
       "minor_improvements": {count},
       "fact_verification_performed": {boolean},
       "accuracy_score": {accuracy_score}
     }
     ```

**Outputs:**

- JIRA comment ID (verify posted)
- Ticket status updated (verify change)
- Ticket assigned (verify assignee)
- Review file path (verify saved)
- Metrics logged (verify appended)

**Error Handling:**

- Comment post fails: Retry once, then save locally and prompt user to post manually
- Status update fails: Log warning, save review locally, continue
- Assignment fails: Log warning but continue (manual assignment may be needed)
- File save fails: HALT with "Unable to save review - check file permissions"
- Metrics logging fails: Log warning but continue (non-critical)

**Save progress:** Update state file with completion

### Workflow Completion

**Upon successful completion of all stages:**

1. Display completion summary:

   ```
   ✅ Security Analysis Review Complete!
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Ticket: {ticket_id}
   CVE: {cve_id}
   Overall Quality: {quality_classification} ({overall_score}%)
   Critical Issues: {count}
   Significant Gaps: {count}
   Minor Improvements: {count}
   Duration: {total_time}
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Review posted to JIRA ticket {ticket_id}
   Review saved to: artifacts/reviews/{filename}
   Ticket status: {new_status}
   Assigned to: {analyst_name}
   ```

2. Clean up workflow state:
   - Archive state file to `.workflow-state/completed/review-{ticket-id}-{timestamp}.json`
   - Remove active state file

3. Prompt user for next action:
   - "Review another enrichment? (y/n)"
   - If yes, restart workflow
   - If no, return to agent prompt

## Error Recovery & Retry Logic

### Automatic Retry

For transient errors (network, rate limits, timeouts):

1. **First failure:** Wait 10 seconds, retry
2. **Second failure:** Wait 30 seconds, retry
3. **Third failure:** Prompt user to continue or abort

### Manual Recovery

For permanent errors (authentication, missing dependencies):

1. Display error with context
2. Suggest resolution steps
3. Prompt user: "Retry / Skip stage / Abort workflow?"
4. If skip: Mark stage incomplete in state, continue with warnings

### Resume from Failure

When workflow is interrupted:

1. State file preserved at `.workflow-state/review-{ticket-id}.json`
2. On next execution, detect incomplete workflow
3. Display: "Incomplete review found for {ticket_id}. Resume from Stage {X}? (y/n)"
4. If yes, load all collected data and continue
5. If no, archive old state and start fresh

## State Management

### State File Structure

```json
{
  "workflow_id": "security-analysis-review-v1",
  "ticket_id": "AOD-1234",
  "started_at": "2025-11-08T14:30:00Z",
  "current_stage": 3,
  "stages_completed": [1, 2],
  "stages_skipped": [],
  "stages_failed": [],
  "total_elapsed_seconds": 510,
  "perform_fact_verification": true,
  "data": {
    "stage1": {
      "enrichment_document": "...",
      "analyst_name": "John Doe",
      "claims_list": [...]
    },
    "stage2": {
      "overall_score": 78,
      "quality_classification": "Good",
      "dimension_scores": {...}
    },
    "stage3": {
      "critical_issues": [],
      "significant_gaps": [...],
      "minor_improvements": [...]
    }
  }
}
```

### State Operations

- **Save:** Write state after each stage completion
- **Load:** Read state on workflow start if exists
- **Archive:** Move to `completed/` directory on success
- **Cleanup:** Remove on explicit user request or after 30 days

## Performance Targets

- **Total Duration:** 15-20 minutes (90th percentile)
- **Stage 1 (Preparation):** 2-3 minutes
- **Stage 2 (Evaluation):** 5-7 minutes
- **Stage 3 (Gap Identification):** 3-4 minutes
- **Stage 4 (Bias Detection):** 2-3 minutes
- **Stage 5 (Fact Verification):** 3-5 minutes (if performed)
- **Stage 6 (Documentation):** 2-3 minutes
- **Stage 7 (Feedback Loop):** 1 minute

**Monitoring:** Track actual durations and compare to targets. Log warnings if any stage exceeds 2x target duration.

## Quality Validation

Before marking workflow complete, validate:

- ✅ All required stages completed successfully
- ✅ All 8 quality checklists executed
- ✅ Overall quality score calculated
- ✅ Gaps categorized by severity
- ✅ Review report generated with all 12 sections
- ✅ JIRA comment posted
- ✅ Ticket status updated appropriately
- ✅ Local review file saved
- ✅ Metrics logged
- ✅ Constructive tone maintained

**Quality Score for Review:**

- Total checks: 10
- Passed checks / Total checks = Review Quality %
- Target: 100% (all checks passing)

If review quality <100%, display warning and suggest manual verification.

## Usage Examples

### Basic Usage

```
*review-security-enrichment AOD-1234
> Perform optional fact verification? (y/n)
n
> Starting review workflow...
```

### With Fact Verification

```
*review-security-enrichment AOD-1234
> Perform optional fact verification? (y/n)
y
> Starting review workflow with fact verification...
```

### Resume After Interruption

```
*review-security-enrichment AOD-1234
> Incomplete review found. Resume from Stage 4? (y/n)
y
> Resuming from Stage 4: Cognitive Bias Detection...
```

### Batch Processing

```
*review-security-enrichment AOD-1234
> Review complete. Review another enrichment? (y/n)
y
> Please provide the JIRA ticket ID to review:
AOD-1235
```

## Integration Points

This task orchestrates and depends on:

- **Tasks:**
  - `categorize-review-findings.md` (Stage 3)
  - `fact-verify-claims.md` (Stage 5, optional)

- **Templates:**
  - `security-review-report-tmpl.yaml` (Stage 6)

- **Checklists:**
  - `technical-accuracy-checklist.md` (Stage 2)
  - `completeness-checklist.md` (Stage 2)
  - `actionability-checklist.md` (Stage 2)
  - `contextualization-checklist.md` (Stage 2)
  - `documentation-quality-checklist.md` (Stage 2)
  - `attack-mapping-validation-checklist.md` (Stage 2)
  - `cognitive-bias-checklist.md` (Stage 2)
  - `source-citation-checklist.md` (Stage 2)

- **Workflows:**
  - `security-analysis-review-workflow.yaml` (definition)

- **MCP Servers:**
  - Atlassian MCP (JIRA operations) - REQUIRED
  - Perplexity MCP (Fact verification) - OPTIONAL

## Notes

- This is an operational workflow task designed for runtime execution
- Designed to review enrichments produced by Story 3.1 workflow
- State management enables resume capability for long-running reviews
- Progress tracking provides visibility into review execution
- Error handling ensures graceful degradation (especially for optional fact verification)
- Quality validation ensures consistent, constructive feedback
- Metrics logging enables workflow performance analysis and improvement
- Integrates with Story 3.4 priority-based review triggering (future)

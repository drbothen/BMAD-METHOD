# Categorize Review Findings Task

## Purpose

Categorize quality dimension checklist failures as Critical/Significant/Minor gaps and generate structured findings for security review reports.

## When to Use

- Security Reviewer agent completes quality dimension checklists (Story 2.2)
- Checklist failures need categorization for review report (Story 2.6)
- Analyst needs prioritized guidance on which gaps to address first
- Epic 3 workflow needs Critical gap detection to trigger re-review

## Inputs Required

- **Checklist results:** Output from `execute-checklist.md` task (Story 2.2)
- **Enrichment document path:** JIRA ticket enrichment being reviewed
- **CVE ID:** For generating resource URLs and learning links
- **Reviewer name:** For attribution in findings report

## Output Destination

- **Review report integration:** Categorized findings section of security review report (Story 2.6)
- **Workflow trigger:** Critical gaps detected flag for Epic 3 re-review workflow

## Process

### Step 1: Parse Checklist Results

**Input Format from Story 2.2:**

```yaml
checklist_results:
  - dimension: 'Technical Accuracy'
    total_items: 10
    passed: 7
    failed: 3
    failures:
      - item_id: 'TA-1'
        description: 'CVSS score matches NVD'
        finding: 'Enrichment score 7.5 vs NVD 9.8'
        section: 'Severity Metrics'
        field: 'CVSS Base Score'
```

**Validation:**

- Verify checklist_results structure is valid YAML/dict
- Confirm required fields present: dimension, failures list
- Validate each failure has: item_id, description, finding, section
- If validation fails: Log error, skip invalid entries, continue with valid ones

**Extraction:**

For each checklist dimension:

1. Extract dimension name (Technical Accuracy, Completeness, Actionability, etc.)
2. Extract failure count
3. For each failure, extract:
   - Checklist item ID (e.g., "TA-1")
   - Description (what was being checked)
   - Finding (what specifically failed)
   - Section (location in enrichment document)
   - Field (specific field/line if available)

### Step 2: Apply Gap Categorization Logic

For each checklist failure, determine severity using the **Gap Prioritization Matrix**:

#### Gap Prioritization Matrix

| Checklist Dimension | Critical If...                                       | Significant If...                                    | Minor If...                                         |
| ------------------- | ---------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------- |
| Technical Accuracy  | Factually incorrect (e.g., wrong CVSS score 7.5→9.8) | Missing optional metric (e.g., no EPSS score)        | Could be more detailed (e.g., expand metric)        |
| Completeness        | Required section missing (e.g., no priority)         | Recommended section missing (e.g., no business risk) | Optional section missing (e.g., no timeline)        |
| Actionability       | No remediation guidance (e.g., blank remediation)    | Vague guidance (e.g., "update software")             | Generic guidance (e.g., "follow best practice")     |
| Contextualization   | Wrong business impact (e.g., low vs critical)        | Missing business context (e.g., no asset impact)     | Insufficient context (e.g., brief explanation)      |
| Source Citation     | No sources or wrong sources (e.g., invalid URL)      | Insufficient sources (e.g., only 1 source)           | Could cite more sources (e.g., add vendor advisory) |

#### Critical Issue Criteria (Must-Fix Before Proceed)

**Examples of Critical Issues:**

- Incorrect CVE ID
- Wrong CVSS score (verified against NVD)
- Wrong KEV status (verified against CISA)
- Missing or incorrect priority assessment
- Factually incorrect remediation guidance
- Wrong affected product/version
- Missing patch information when patch available
- Priority does not match severity factors

**Impact:** Could lead to incorrect remediation decisions, wasted effort, or missed critical vulnerabilities.

**Blocking Behavior:** Ticket cannot proceed to remediation until Critical gaps are addressed.

#### Significant Gap Criteria (Should-Fix, Impacts Quality)

**Examples of Significant Gaps:**

- Missing EPSS score
- Missing MITRE ATT&CK mapping
- Incomplete business impact assessment
- Vague or generic remediation guidance
- Missing compensating controls
- Weak priority rationale
- Insufficient source citations
- Missing exploit intelligence

**Impact:** Reduces decision-making confidence, requires additional research, or delays remediation planning.

**Blocking Behavior:** Should be addressed, but ticket can proceed with reviewer approval.

#### Minor Improvement Criteria (Nice-to-Have Enhancements)

**Examples of Minor Improvements:**

- Formatting inconsistencies
- Minor grammar/spelling errors
- Could use more detailed explanations
- Additional context would be helpful
- Better organization of sections
- More source citations
- Additional MITRE ATT&CK techniques

**Impact:** Minimal impact on usability, mostly stylistic or additive improvements.

**Blocking Behavior:** Non-blocking, optional cleanup.

### Step 3: Categorization Algorithm

For each checklist failure:

**Algorithm Steps:**

1. **Extract failure context:**
   - Dimension = failure.dimension
   - Finding = failure.finding
   - Description = failure.description
   - Section = failure.section

2. **Lookup Matrix Row:** Find the dimension in Gap Prioritization Matrix

3. **Apply Severity Logic:**

   **IF** finding matches "Critical If" criteria **THEN**
   - Severity = "Critical"
   - ID Prefix = "CRIT"
   - Icon = 🔴
   - Blocking = true

   **ELSE IF** finding matches "Significant If" criteria **THEN**
   - Severity = "Significant"
   - ID Prefix = "SIG"
   - Icon = 🟡
   - Blocking = false

   **ELSE**
   - Severity = "Minor"
   - ID Prefix = "MIN"
   - Icon = 🔵
   - Blocking = false

4. **Assign Sequential ID:**
   - Critical: CRIT-1, CRIT-2, CRIT-3...
   - Significant: SIG-1, SIG-2, SIG-3...
   - Minor: MIN-1, MIN-2, MIN-3...

**Example Categorization Logic (Pseudocode):**

```python
def categorize_failure(failure, dimension):
    finding_text = failure.finding.lower()
    description_text = failure.description.lower()

    # Check Critical criteria first
    if dimension == "Technical Accuracy":
        if any(keyword in finding_text for keyword in ["incorrect", "wrong", "mismatch"]):
            if any(term in finding_text for term in ["cvss", "kev", "priority", "patch"]):
                return "Critical"

    if dimension == "Completeness":
        if "missing" in finding_text:
            if any(term in description_text for term in ["priority", "remediation", "cvss"]):
                return "Critical"

    # Check Significant criteria
    if dimension == "Technical Accuracy":
        if "missing" in finding_text:
            if any(term in finding_text for term in ["epss", "mitre", "exploit"]):
                return "Significant"

    if dimension == "Actionability":
        if any(keyword in finding_text for keyword in ["vague", "generic", "unclear"]):
            return "Significant"

    # Default to Minor
    return "Minor"
```

### Step 4: Generate Structured Findings

For each categorized failure, generate a structured finding using this template:

**Finding Structure:**

```yaml
id: '{{ID_PREFIX}}-{{NUMBER}}'
title: '{{FINDING_TITLE}}'
severity: '{{SEVERITY}}'
location: '{{SECTION_NAME}} → {{SPECIFIC_FIELD}}'
issue: '{{WHAT_IS_MISSING_OR_INCORRECT}}'
impact: '{{WHY_THIS_MATTERS}}'
fix: '{{SPECIFIC_ACTIONABLE_FIX}}'
example: |
  {{EXAMPLE_OF_CORRECT_APPROACH}}
resource_title: '{{RESOURCE_TITLE}}'
resource_url: '{{RESOURCE_URL}}'
source_checklist: '{{DIMENSION}}'
source_item: '{{ITEM_ID}}'
```

**Field Generation Logic:**

1. **ID:** Generated from severity prefix + sequential number
2. **Title:** Extract from finding or generate from description
3. **Severity:** From categorization algorithm (Critical/Significant/Minor)
4. **Location:** Combine section + field from checklist failure
5. **Issue:** Use checklist finding field directly
6. **Impact:** Generate based on severity and dimension:
   - Critical: "Could lead to incorrect remediation decisions..."
   - Significant: "Reduces decision-making confidence..."
   - Minor: "Small impact. Minimal usability effect..."
7. **Fix:** Generate specific actionable fix based on failure type
8. **Example:** Provide correct approach example
9. **Resource Title/URL:** Map to authoritative source based on failure type
10. **Source Checklist/Item:** Link back to originating checklist

**Resource URL Mapping:**

Map failure types to authoritative learning resources:

| Failure Type | Resource Title          | Resource URL                                                 |
| ------------ | ----------------------- | ------------------------------------------------------------ |
| CVSS score   | NIST NVD CVE-{cve_id}   | https://nvd.nist.gov/vuln/detail/{cve_id}                    |
| EPSS score   | FIRST EPSS              | https://www.first.org/epss/                                  |
| KEV status   | CISA KEV Catalog        | https://www.cisa.gov/known-exploited-vulnerabilities-catalog |
| MITRE ATT&CK | MITRE ATT&CK Framework  | https://attack.mitre.org/                                    |
| Remediation  | Vendor-specific         | {vendor_security_advisory_url}                               |
| Priority     | BMAD Priority Framework | {internal_priority_guide}                                    |

### Step 5: Output Categorized Findings

**Output Format for Story 2.6 (Review Report Template):**

```yaml
categorized_findings:
  critical:
    - id: 'CRIT-1'
      title: 'Incorrect CVSS Score'
      severity: 'Critical'
      location: 'Severity Metrics → CVSS Base Score'
      issue: 'Enrichment states CVSS score is 7.5, but NVD lists 9.8 (Critical severity)'
      impact: 'Priority assessment based on 7.5 would be P3 (Medium), but actual 9.8 score warrants P1 (Critical). This could delay critical remediation by weeks.'
      fix: 'Update CVSS score to 9.8 and vector string to match NVD. Recalculate priority assessment using correct score.'
      example: |
        CVSS Base Score: 9.8 (Critical)
        CVSS Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
      resource_title: 'NIST NVD CVE-2024-1234'
      resource_url: 'https://nvd.nist.gov/vuln/detail/CVE-2024-1234'
      source_checklist: 'Technical Accuracy'
      source_item: 'TA-1'

  significant:
    - id: 'SIG-1'
      title: 'Missing EPSS Score'
      severity: 'Significant'
      location: 'Severity Metrics → EPSS Score'
      issue: 'EPSS exploitation probability score is not included in enrichment'
      impact: "EPSS provides data-driven exploitation probability, critical for risk-based prioritization. Without EPSS, priority assessment relies solely on CVSS severity, which doesn't reflect exploitation likelihood."
      fix: 'Research EPSS score from FIRST.org and add to Severity Metrics section'
      example: |
        EPSS Score: 0.85 (97th percentile)
        Interpretation: Very high probability of exploitation in next 30 days
      resource_title: 'FIRST EPSS'
      resource_url: 'https://www.first.org/epss/'
      source_checklist: 'Completeness'
      source_item: 'COMP-4'

  minor:
    - id: 'MIN-1'
      title: 'Enhance Remediation Guidance Specificity'
      severity: 'Minor'
      location: 'Remediation Guidance → Patch Installation'
      issue: "Remediation states 'Upgrade to latest version' without specifying exact version number"
      impact: 'Small impact. Remediation team will need to look up exact version, adding minor research overhead.'
      fix: "Specify exact patched version: 'Upgrade to Apache Struts 2.5.33 or later'"
      example: |
        ✅ Patch Available: Upgrade to Apache Struts 2.5.33+
        📦 Download: https://struts.apache.org/download.cgi
        📖 Upgrade Guide: https://struts.apache.org/docs/upgrade-guide.html
      resource_title: 'Apache Struts Download'
      resource_url: 'https://struts.apache.org/download.cgi'
      source_checklist: 'Actionability'
      source_item: 'ACT-2'
```

**Summary Statistics:**

```yaml
findings_summary:
  total_failures: 15
  critical_count: 2
  significant_count: 8
  minor_count: 5
  blocking_issues: true # True if critical_count > 0
  requires_rework: true # True if critical_count > 0
```

### Step 6: Epic 3 Workflow Trigger

**Critical Gap Workflow Integration:**

IF `critical_count > 0` THEN:

1. **Set blocking flag:** `blocking_issues = true`
2. **Trigger re-review workflow:** Notify Epic 3 workflow integration
3. **Block ticket progression:** Prevent ticket from proceeding to remediation
4. **Require analyst action:** Analyst must address all Critical gaps
5. **Schedule re-review:** After Critical gaps addressed, reviewer re-evaluates

**Workflow Trigger Output:**

```yaml
workflow_trigger:
  critical_gaps_detected: true
  critical_gap_count: 2
  critical_gap_ids: ['CRIT-1', 'CRIT-2']
  blocking_status: 'BLOCKED - Critical gaps must be addressed'
  next_step: 'Analyst addresses Critical gaps → Re-review required'
  integration_point: 'Epic 3 Re-Review Workflow'
```

**Non-Blocking Scenario:**

IF `critical_count == 0` AND `significant_count > 0` THEN:

- Blocking = false
- Ticket can proceed with reviewer approval
- Significant gaps recommended for fix but not required

IF `critical_count == 0` AND `significant_count == 0` THEN:

- No blocking issues
- Minor improvements optional
- Ticket can proceed normally

## Example Categorization Scenarios

### Scenario 1: Wrong CVSS Score

**Input (Checklist Failure):**

```yaml
dimension: 'Technical Accuracy'
item_id: 'TA-1'
description: 'CVSS score matches NVD'
finding: 'Enrichment score 7.5 vs NVD 9.8'
section: 'Severity Metrics'
field: 'CVSS Base Score'
```

**Categorization Logic:**

- Dimension: Technical Accuracy
- Finding contains: "vs" (indicates mismatch)
- Keywords: "CVSS score" (critical metric)
- **Severity: Critical** (Factually incorrect critical metric)

**Output (Structured Finding):**

```yaml
id: 'CRIT-1'
title: 'Incorrect CVSS Score'
severity: 'Critical'
location: 'Severity Metrics → CVSS Base Score'
issue: 'Enrichment states CVSS score is 7.5, but NVD lists 9.8 (Critical severity)'
impact: 'Priority assessment based on 7.5 would be P3 (Medium), but actual 9.8 score warrants P1 (Critical). This could delay critical remediation by weeks.'
fix: 'Update CVSS score to 9.8 and vector string to match NVD. Recalculate priority assessment using correct score.'
example: |
  CVSS Base Score: 9.8 (Critical)
  CVSS Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
resource_title: 'NIST NVD CVE-2024-1234'
resource_url: 'https://nvd.nist.gov/vuln/detail/CVE-2024-1234'
source_checklist: 'Technical Accuracy'
source_item: 'TA-1'
```

### Scenario 2: Missing EPSS Score

**Input (Checklist Failure):**

```yaml
dimension: 'Completeness'
item_id: 'COMP-4'
description: 'EPSS score included'
finding: 'EPSS score not found in enrichment'
section: 'Severity Metrics'
field: 'EPSS Score'
```

**Categorization Logic:**

- Dimension: Completeness
- Finding: "not found" (missing)
- Keywords: "EPSS score" (optional metric)
- **Severity: Significant** (Missing recommended metric)

**Output (Structured Finding):**

```yaml
id: 'SIG-1'
title: 'Missing EPSS Score'
severity: 'Significant'
location: 'Severity Metrics → EPSS Score'
issue: 'EPSS exploitation probability score is not included in enrichment'
impact: "EPSS provides data-driven exploitation probability, critical for risk-based prioritization. Without EPSS, priority assessment relies solely on CVSS severity, which doesn't reflect exploitation likelihood."
fix: 'Research EPSS score from FIRST.org and add to Severity Metrics section'
example: |
  EPSS Score: 0.85 (97th percentile)
  Interpretation: Very high probability of exploitation in next 30 days
resource_title: 'FIRST EPSS'
resource_url: 'https://www.first.org/epss/'
source_checklist: 'Completeness'
source_item: 'COMP-4'
```

### Scenario 3: Formatting Inconsistency

**Input (Checklist Failure):**

```yaml
dimension: 'Structure & Formatting'
item_id: 'SF-2'
description: 'Consistent heading levels'
finding: 'Some sections use ### while others use ##'
section: 'Document Structure'
field: 'Heading Levels'
```

**Categorization Logic:**

- Dimension: Structure & Formatting
- Finding: "Inconsistent" (formatting issue)
- Impact: Minimal usability
- **Severity: Minor** (Stylistic improvement)

**Output (Structured Finding):**

```yaml
id: 'MIN-1'
title: 'Inconsistent Heading Levels'
severity: 'Minor'
location: 'Document Structure → Heading Levels'
issue: 'Some sections use ### while others use ## for the same heading level'
impact: "Small impact. Formatting inconsistency may slightly reduce readability but doesn't affect technical content."
fix: 'Standardize all section headings to use ## for major sections, ### for subsections'
example: |
  ## Severity Assessment    (use ## for major sections)
  ### CVSS Score            (use ### for subsections)
  ### EPSS Score
resource_title: 'Markdown Style Guide'
resource_url: 'https://google.github.io/styleguide/docguide/style.html'
source_checklist: 'Structure & Formatting'
source_item: 'SF-2'
```

## Integration with Review Workflow

This task is called by Security Reviewer agent as part of the review workflow:

```
Security Reviewer Agent Workflow:
1. *review-enrichment → Run quality dimension checklists (Story 2.2)
2. *categorize-gaps → Categorize checklist failures (Story 2.3) ← THIS TASK
3. *detect-bias (OPTIONAL) → Detect cognitive biases (Story 2.4)
4. *fact-check (OPTIONAL) → Verify critical claims (Story 2.5)
5. *generate-report → Create review report with categorized findings (Story 2.6)
```

**Integration Points:**

- **Input:** Checklist results from Story 2.2 `execute-checklist.md`
- **Output:** Categorized findings for Story 2.6 review report template
- **Trigger:** Epic 3 re-review workflow if Critical gaps detected

## Error Handling

**Invalid Checklist Results:**

- Validate input structure before processing
- Skip malformed entries, log warning
- Continue with valid entries
- Note in output: "⚠️ {count} invalid checklist entries skipped"

**Missing Required Fields:**

- If failure missing section/field: Use "Location Unknown"
- If failure missing finding: Use description as finding
- If failure missing dimension: Categorize as "Minor" by default
- Log warning for incomplete data

**Categorization Edge Cases:**

- **Ambiguous failure:** If can't determine severity, default to "Significant"
- **Multiple severity indicators:** Choose higher severity (Critical > Significant > Minor)
- **Unknown dimension:** Categorize based on finding keywords only
- Document ambiguous cases in findings notes

**Empty Checklist Results:**

- If all checklists passed (no failures):
  - Output empty categorized_findings
  - Summary: "✅ No gaps detected - all quality dimensions passed"
  - Blocking: false
  - Continue workflow normally

## Security Considerations

**Input Sanitization:**

- Validate checklist results structure before parsing
- Sanitize all text fields before including in output
- Prevent markdown injection in generated findings
- Validate resource URLs before including

**Path Validation:**

- Verify enrichment document path is within project directory
- No ../ path traversal allowed
- Fail safely if path validation fails

**Output Safety:**

- Escape special characters in markdown output
- Prevent XSS in generated reports
- Validate all URLs are HTTPS (except localhost/internal)

**Audit Logging:**

- Log categorization results for each failure
- Log Critical gap detection events
- Log workflow trigger actions
- Include timestamp and reviewer context

## Example Usage

**Standard Usage:**

```
Input: Checklist results from Story 2.2 (8 dimensions, 15 total failures)
Processing:
  - Technical Accuracy: 3 failures → 2 Critical, 1 Significant
  - Completeness: 5 failures → 0 Critical, 4 Significant, 1 Minor
  - Actionability: 4 failures → 0 Critical, 2 Significant, 2 Minor
  - Contextualization: 2 failures → 0 Critical, 1 Significant, 1 Minor
  - Source Citation: 1 failure → 0 Critical, 0 Significant, 1 Minor

Output:
  - 2 Critical gaps (BLOCKING)
  - 8 Significant gaps
  - 5 Minor improvements
  - Workflow trigger: Epic 3 re-review required
  - Next step: Analyst addresses Critical gaps
```

**All Passed Scenario:**

```
Input: Checklist results from Story 2.2 (8 dimensions, 0 failures)
Processing: No failures to categorize
Output:
  - 0 Critical, 0 Significant, 0 Minor
  - ✅ All quality dimensions passed
  - Blocking: false
  - Next step: Proceed to report generation (Story 2.6)
```

**Mixed Severity Scenario:**

```
Input: 10 checklist failures
Processing:
  - 0 Critical gaps
  - 6 Significant gaps
  - 4 Minor improvements

Output:
  - Blocking: false (no Critical gaps)
  - Recommendation: Address Significant gaps before proceeding
  - Reviewer approval: Required for ticket progression
  - Next step: Analyst addresses Significant gaps (recommended, not required)
```

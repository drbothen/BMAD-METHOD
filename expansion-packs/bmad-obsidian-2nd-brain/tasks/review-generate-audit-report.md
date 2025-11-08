<!-- Powered by BMAD™ Core -->

# Review: Generate Audit Report

## Purpose

Generate a comprehensive vault health audit report by aggregating results from multiple audit dimensions (freshness, links, citations, orphans, atomicity, duplicates, metadata), calculating an overall health score, and creating prioritized action items. Outputs a formatted markdown report to the Obsidian vault for review and remediation tracking.

## Inputs

- **audit_results** (Object, required): Combined audit results from all dimensions
  - `freshness` (Object): Results from review-audit-temporal-freshness task
  - `links` (Object): Results from review-validate-external-links task
  - `citations` (Object, optional): Results from citation validation
  - `orphans` (Object, optional): Results from orphan detection
  - `atomicity` (Object, optional): Results from atomicity audit
  - `duplicates` (Object, optional): Results from duplicate detection
  - `metadata` (Object, optional): Results from metadata completeness check
- **vault_path** (String, required): Absolute path to Obsidian vault
- **output_path** (String, optional): Custom report location (default: `reports/audit-YYYY-MM-DD-HHMM.md`)

## Outputs

- **report_note_path** (String): Path to created audit report note in vault
- **health_score** (Float): Overall vault health score (0-100 scale)
- **health_interpretation** (String): Health score interpretation (Excellent/Good/Fair/Poor/Critical)
- **action_items** (Array<Object>): Prioritized list of recommended actions
  - `priority` (String): critical/high/medium/low
  - `category` (String): Audit dimension (freshness/links/orphans/etc.)
  - `action` (String): Recommended action description
  - `details` (String): Additional context and rationale
- **success** (Boolean): Report generation status

## Sequential Procedure

### Step 1: Validate Inputs

- Verify `audit_results` is an object with at least one dimension
- Check required dimensions: `freshness` and `links` must be present
- Confirm `vault_path` exists and is an absolute path
- Validate `vault_path` doesn't contain directory traversal (`../`)
- If `output_path` provided, validate it's within vault bounds
- If validation fails, return error with specific issue

### Step 2: Load Audit Report Template

- Load template file from: `expansion-packs/bmad-obsidian-2nd-brain/templates/audit-report-tmpl.yaml`
- Parse YAML template structure
- Verify template has required sections:
  - Executive Summary
  - Health Score
  - Dimension Scores
  - Freshness Issues
  - Link Validation
  - Orphaned Notes (optional)
  - Action Items
  - Vault Metrics
- If template not found, return error: "Template not found"

### Step 3: Calculate Vault Health Score (Weighted)

Use weighted formula to calculate overall health:

**Weights:**

- Freshness: 20%
- Links: 15%
- Orphans: 15%
- Atomicity: 20%
- Duplicates: 10%
- Citations: 10%
- Metadata: 10%

**Calculation for each dimension:**

- **Freshness**: `(1 - stale_notes_ratio) * 20`
- **Links**: `(1 - broken_links_ratio) * 15`
- **Orphans**: `(1 - orphan_ratio) * 15`
- **Atomicity**: `atomicity_pass_rate * 20`
- **Duplicates**: `(1 - duplicate_ratio) * 10`
- **Citations**: `citation_completeness * 10`
- **Metadata**: `metadata_completeness * 10`

**Total health_score**: Sum all dimension scores (0-100 scale)

**Handle missing dimensions:**

- If dimension is missing/null, redistribute weight proportionally to present dimensions
- Minimum required: freshness + links (35% of total weight)

### Step 4: Interpret Health Score

Map numeric score to qualitative interpretation:

| Score Range | Interpretation | Description                                               |
| ----------- | -------------- | --------------------------------------------------------- |
| 90-100      | Excellent      | Vault is well-maintained with minimal issues              |
| 75-89       | Good           | Vault is healthy with some minor improvements needed      |
| 60-74       | Fair           | Moderate attention required in several areas              |
| 40-59       | Poor           | Significant maintenance needed across multiple dimensions |
| 0-39        | Critical       | Immediate action required to restore vault health         |

Store `health_interpretation` for report.

### Step 5: Generate Executive Summary

Create 3-5 sentence summary highlighting:

- Current health score and interpretation
- Total notes analyzed
- Key issues count (stale notes, broken links, orphans)
- Top priority recommendations
- Timestamp of audit execution

**Example:**

> "Vault health assessment completed on 2025-11-06T14:30:00Z. Overall health score: 68.5/100 (Fair). Analyzed 1,245 notes and identified 187 stale notes (15%), 34 broken external links (22% failure rate), and 12 orphaned notes. Recommended action: Prioritize updating 25 high-importance stale notes and fixing broken links in reference sections."

### Step 6: Format Freshness Issues as Prioritized Table

Create markdown table with columns:

- Note Path
- Last Updated
- Days Stale
- Importance
- Priority Score
- Severity

Sort by priority_score (descending). Limit to top 20 critical issues.

**Example:**

```markdown
| Note Path            | Last Updated | Days Stale | Importance | Priority Score | Severity |
| -------------------- | ------------ | ---------- | ---------- | -------------- | -------- |
| core/methodology.md  | 2024-03-15   | 236        | 15         | 19.65          | high     |
| concepts/workflow.md | 2024-01-20   | 291        | 12         | 19.40          | high     |
```

### Step 7: Group Link Validation Issues by Type

Organize link validation results into categories:

- **Broken Links (4xx/5xx)**: Group by status code
  - 404 Not Found
  - 403 Forbidden
  - 500 Server Error
- **Redirects (3xx)**: List with old URL → new location
- **Timeouts**: URLs that exceeded 5-second limit
- **Blocked (Security)**: Private IPs and invalid protocols

Show count per category and top 10 examples per type.

### Step 8: List Orphaned Notes with Suggested Linking Opportunities

For each orphaned note:

- Show note path and title
- Use semantic search to find related notes (if available)
- Suggest 3-5 potential linking opportunities based on content similarity
- Include reasoning: "Related to X by topic Y"

**Fallback**: If semantic search unavailable, list orphans without suggestions.

### Step 9: Summarize Atomicity Violations (if available)

If `audit_results.atomicity` exists:

- Count total violations
- Group by violation type:
  - Multi-concept notes (contains >1 core concept)
  - Overly long notes (exceeds recommended length)
  - Missing atomic structure
- Show top 10 violators with recommended fragmentation strategy

### Step 10: Summarize Duplicate Detection Results (if available)

If `audit_results.duplicates` exists:

- Count total duplicate clusters
- Show similarity threshold used
- List top duplicate clusters (>80% similarity)
- Suggest merge/consolidation actions

### Step 11: Prioritize Action Items by Severity

Generate prioritized action items based on health score and dimension results:

**Critical Actions (health_score < 40):**

- "Immediate attention required: Vault health is critical"
- Specific high-impact fixes

**High Priority Actions:**

- Fix broken links (if broken_count > 10)
- Update critical stale notes (if priority_score > 50)
- Resolve major atomicity violations (if >20 violations)

**Medium Priority Actions:**

- Link orphaned notes (if orphan_count > 5)
- Clean up duplicate content (if duplicate_ratio > 0.10)
- Complete missing metadata (if metadata_completeness < 0.70)

**Low Priority Actions:**

- Update low-importance stale notes
- Fix redirects (informational, not broken)
- Minor formatting improvements

Each action item includes:

- `priority`: critical/high/medium/low
- `category`: Audit dimension
- `action`: Specific recommended action
- `details`: Context and impact explanation

### Step 12: Populate Report Template with All Sections

Replace template variables with calculated values:

- `{{timestamp}}`: Current ISO 8601 timestamp
- `{{health_score}}`: Calculated health score (e.g., "68.5")
- `{{health_interpretation}}`: Excellent/Good/Fair/Poor/Critical
- `{{executive_summary}}`: Generated summary from Step 5
- `{{dimension_scores}}`: Table of all dimension scores
- `{{freshness_table}}`: Formatted freshness issues (Step 6)
- `{{link_issues}}`: Grouped link problems (Step 7)
- `{{orphan_list}}`: Orphaned notes with suggestions (Step 8)
- `{{action_items}}`: Prioritized action list (Step 11)
- `{{vault_metrics}}`: Overall vault statistics

Ensure all sections properly formatted with markdown.

### Step 13: Create Report Note in Vault Using Obsidian MCP

- Generate report file path:
  - If `output_path` provided: use it
  - Otherwise: `reports/audit-YYYY-MM-DD-HHMM.md` (timestamp-based)
- Create reports directory if it doesn't exist
- Call `obsidian.create_note` with:
  - `vault_path`: Vault root path
  - `note_path`: Generated report path
  - `content`: Populated report markdown
- If creation fails, return error: "Failed to create report note"

### Step 14: Return Report Metadata and Success Status

Return object containing:

- `report_note_path`: Full path to created report
- `health_score`: Calculated score (0-100)
- `health_interpretation`: Qualitative interpretation
- `action_items`: Prioritized actions array
- `success`: true (if report created successfully)
- `timestamp`: ISO 8601 timestamp of report generation

## Security Considerations

### Path Validation

- **output_path must be within vault bounds**: Prevent writing files outside vault
- **Reject directory traversal**: Paths containing `../` or `..\` are blocked
- **Use path canonicalization**: Resolve symbolic links and relative paths
- **Example blocked paths**:
  - `/vault/../etc/passwd` - Escapes vault
  - `C:\vault\..\Windows\System32\report.md` - System directory access

### YAML Escaping

- **Escape special characters in report content**:
  - `&` → `&amp;`
  - `<` → `&lt;`
  - `>` → `&gt;`
  - `:` → Escape in YAML values to prevent parsing errors
- **Prevent YAML injection**: Sanitize user-provided note titles and content before including in report
- **Safe multiline strings**: Use `|` or `>` YAML syntax for long text blocks

### Size Limits

- **Warn if report exceeds 1MB**: Large reports may cause performance issues in Obsidian
- **Recommendation**: If report too large, split into multiple reports by dimension
- **Prevention**: Limit number of items per section (e.g., top 20 freshness issues, not all 500)

### Content Sanitization

- **HTML sanitization**: Strip `<script>`, `<iframe>`, `<object>` tags from note content before including in report
- **XSS prevention**: Encode user-provided content in markdown to prevent code execution
- **Example**: If note title is `<script>alert('XSS')</script>`, encode to `&lt;script&gt;alert('XSS')&lt;/script&gt;`

## Performance Targets

- **Report generation**: < 5 seconds for aggregation and formatting
  - Template loading: ~0.2 seconds
  - Health score calculation: ~0.5 seconds
  - Section formatting: ~2 seconds
  - Report note creation: ~0.5 seconds
  - Total: ~3-5 seconds

**Optimization strategies:**

- Cache template after first load (reuse for multiple reports in session)
- Pre-calculate dimension scores in audit tasks (avoid re-computation)
- Limit table sizes (top 20 items per section, not full lists)
- Use efficient markdown string building (StringBuilder or similar)

## Error Handling

### Error 1: Template Not Found

**Condition:** audit-report-tmpl.yaml doesn't exist at expected path

**Response:**

```json
{
  "success": false,
  "error": "Template not found: expansion-packs/bmad-obsidian-2nd-brain/templates/audit-report-tmpl.yaml",
  "remediation": "Ensure audit-report-tmpl.yaml exists in templates directory"
}
```

### Error 2: Obsidian MCP create_note Failure

**Condition:** Cannot create note in vault (permissions, disk space, MCP error)

**Response:**

```json
{
  "success": false,
  "error": "Failed to create report note: [specific MCP error]",
  "remediation": "Verify vault permissions and MCP server is running"
}
```

### Error 3: Invalid Audit Results

**Condition:** audit_results missing required dimensions (freshness or links)

**Response:**

```json
{
  "success": false,
  "error": "Invalid audit_results: missing required dimension 'freshness'",
  "remediation": "Ensure audit_results contains at least 'freshness' and 'links' dimensions"
}
```

### Error 4: Invalid Vault Path

**Condition:** vault_path doesn't exist or contains traversal

**Response:**

```json
{
  "success": false,
  "error": "Invalid vault_path: directory traversal detected",
  "remediation": "Provide absolute path to vault without ../ sequences"
}
```

### Error 5: Report Size Warning

**Condition:** Generated report exceeds 1MB

**Response:**

```json
{
  "success": true,
  "report_note_path": "reports/audit-2025-11-06-1430.md",
  "health_score": 68.5,
  "health_interpretation": "Fair",
  "action_items": [...],
  "warning": "Report size exceeds 1MB (1.2MB). Consider filtering results or splitting into multiple reports."
}
```

## Example Usage

### Example 1: Full Audit Report with All Dimensions

**Input:**

```yaml
audit_results:
  freshness:
    stale_notes: 187
    total_notes: 1245
    stale_ratio: 0.15
    avg_staleness: 245.5
    stale_notes: [...]  # Array of stale note objects
  links:
    total_links: 156
    broken_count: 34
    redirect_count: 8
    timeout_count: 3
    success_count: 111
    broken_links: [...]  # Array of broken link objects
  orphans:
    orphan_count: 12
    orphan_ratio: 0.01
    orphan_list: [...]
  atomicity:
    pass_rate: 0.85
    violations: 23
  duplicates:
    duplicate_ratio: 0.05
    clusters: 6
  citations:
    completeness: 0.78
  metadata:
    completeness: 0.92
vault_path: "/Users/john/Documents/ObsidianVault"
output_path: null  # Use default timestamp-based path
```

**Output:**

```json
{
  "success": true,
  "report_note_path": "/Users/john/Documents/ObsidianVault/reports/audit-2025-11-06-1430.md",
  "health_score": 73.2,
  "health_interpretation": "Fair",
  "action_items": [
    {
      "priority": "high",
      "category": "links",
      "action": "Fix 34 broken external links",
      "details": "22% of external links are broken (404/403 errors). This impacts reference quality and research credibility."
    },
    {
      "priority": "high",
      "category": "freshness",
      "action": "Update 25 high-priority stale notes",
      "details": "Critical knowledge hubs haven't been updated in >6 months. These notes have high incoming link counts and are central to vault."
    },
    {
      "priority": "medium",
      "category": "orphans",
      "action": "Link 12 orphaned notes to knowledge graph",
      "details": "Orphaned notes reduce knowledge connectivity. Semantic analysis suggests 18 potential linking opportunities."
    },
    {
      "priority": "medium",
      "category": "atomicity",
      "action": "Fragment 23 multi-concept notes",
      "details": "Notes violating atomic note principle should be split into single-concept notes for better reusability."
    },
    {
      "priority": "low",
      "category": "citations",
      "action": "Complete citations for 78 notes",
      "details": "22% of notes with external references lack proper citations. Add source attribution for credibility."
    }
  ]
}
```

**Generated Report Preview:**

```markdown
# Vault Audit Report

_Generated: 2025-11-06T14:30:00Z_

## Executive Summary

Vault health assessment completed on 2025-11-06T14:30:00Z. Overall health score: **73.2/100 (Fair)**. Analyzed 1,245 notes and identified 187 stale notes (15%), 34 broken external links (22% failure rate), and 12 orphaned notes. Recommended action: Prioritize updating 25 high-importance stale notes and fixing broken links in reference sections. Vault shows moderate health with several areas requiring attention.

## Health Score: 73.2/100 (Fair)

| Dimension  | Score | Weight   | Contribution |
| ---------- | ----- | -------- | ------------ |
| Freshness  | 85.0  | 20%      | 17.0         |
| Links      | 78.2  | 15%      | 11.7         |
| Orphans    | 99.0  | 15%      | 14.9         |
| Atomicity  | 85.0  | 20%      | 17.0         |
| Duplicates | 95.0  | 10%      | 9.5          |
| Citations  | 78.0  | 10%      | 7.8          |
| Metadata   | 92.0  | 10%      | 9.2          |
| **Total**  |       | **100%** | **73.2**     |

## Freshness Issues (Top 20 by Priority)

| Note Path            | Last Updated | Days Stale | Importance | Priority Score | Severity |
| -------------------- | ------------ | ---------- | ---------- | -------------- | -------- |
| core/methodology.md  | 2024-03-15   | 236        | 15         | 19.65          | high     |
| concepts/workflow.md | 2024-01-20   | 291        | 12         | 19.40          | high     |

| ...

## Link Validation Issues

### Broken Links (34 total)

- **404 Not Found (28)**: ...
- **403 Forbidden (4)**: ...
- **500 Server Error (2)**: ...

### Redirects (8 total)

- `https://old-site.com` → `https://new-site.com`
- ...

...
```

### Example 2: Minimal Report (Freshness + Links Only)

**Input:**

```yaml
audit_results:
  freshness:
    stale_notes: 45
    total_notes: 500
    stale_ratio: 0.09
    stale_notes: [...]
  links:
    total_links: 23
    broken_count: 2
    success_count: 21
    broken_links: [...]
vault_path: "/Users/jane/Notes"
output_path: "health-check.md"
```

**Output:**

```json
{
  "success": true,
  "report_note_path": "/Users/jane/Notes/health-check.md",
  "health_score": 88.5,
  "health_interpretation": "Good",
  "action_items": [
    {
      "priority": "low",
      "category": "freshness",
      "action": "Update 45 stale notes",
      "details": "9% of notes are stale. Most are low-importance with minimal impact."
    },
    {
      "priority": "low",
      "category": "links",
      "action": "Fix 2 broken links",
      "details": "91% success rate. Minimal link health issues."
    }
  ]
}
```

## Algorithm Pseudocode

```python
import datetime
import yaml

def generate_audit_report(audit_results, vault_path, output_path=None):
    # Step 1: Validate inputs
    if 'freshness' not in audit_results or 'links' not in audit_results:
        return {"success": False, "error": "Missing required dimensions"}
    if has_path_traversal(vault_path):
        return {"success": False, "error": "Path traversal detected"}

    # Step 2: Load template
    template = load_yaml('expansion-packs/bmad-obsidian-2nd-brain/templates/audit-report-tmpl.yaml')
    if not template:
        return {"success": False, "error": "Template not found"}

    # Step 3: Calculate health score (weighted)
    weights = {
        'freshness': 0.20,
        'links': 0.15,
        'orphans': 0.15,
        'atomicity': 0.20,
        'duplicates': 0.10,
        'citations': 0.10,
        'metadata': 0.10
    }

    scores = {}
    total_weight = 0

    if 'freshness' in audit_results:
        scores['freshness'] = (1 - audit_results['freshness']['stale_ratio']) * 100
        total_weight += weights['freshness']

    if 'links' in audit_results:
        broken_ratio = audit_results['links']['broken_count'] / audit_results['links']['total_links']
        scores['links'] = (1 - broken_ratio) * 100
        total_weight += weights['links']

    if 'orphans' in audit_results:
        scores['orphans'] = (1 - audit_results['orphans']['orphan_ratio']) * 100
        total_weight += weights['orphans']

    if 'atomicity' in audit_results:
        scores['atomicity'] = audit_results['atomicity']['pass_rate'] * 100
        total_weight += weights['atomicity']

    if 'duplicates' in audit_results:
        scores['duplicates'] = (1 - audit_results['duplicates']['duplicate_ratio']) * 100
        total_weight += weights['duplicates']

    if 'citations' in audit_results:
        scores['citations'] = audit_results['citations']['completeness'] * 100
        total_weight += weights['citations']

    if 'metadata' in audit_results:
        scores['metadata'] = audit_results['metadata']['completeness'] * 100
        total_weight += weights['metadata']

    # Calculate weighted score
    health_score = sum(scores[k] * weights[k] for k in scores) / total_weight * 100

    # Step 4: Interpret health score
    if health_score >= 90:
        interpretation = 'Excellent'
    elif health_score >= 75:
        interpretation = 'Good'
    elif health_score >= 60:
        interpretation = 'Fair'
    elif health_score >= 40:
        interpretation = 'Poor'
    else:
        interpretation = 'Critical'

    # Step 5: Generate executive summary
    timestamp = datetime.datetime.now().isoformat()
    summary = f"""
    Vault health assessment completed on {timestamp}.
    Overall health score: {health_score:.1f}/100 ({interpretation}).
    Analyzed {audit_results['freshness']['total_notes']} notes and identified
    {audit_results['freshness']['stale_notes']} stale notes,
    {audit_results['links']['broken_count']} broken links.
    """

    # Step 6-10: Format sections
    freshness_table = format_freshness_table(audit_results['freshness'])
    link_issues = format_link_groups(audit_results['links'])
    orphan_list = format_orphan_list(audit_results.get('orphans', {}))

    # Step 11: Prioritize action items
    action_items = []

    # Critical actions
    if health_score < 40:
        action_items.append({
            'priority': 'critical',
            'category': 'vault_health',
            'action': 'Immediate attention required: Vault health is critical',
            'details': 'Multiple quality dimensions below acceptable thresholds'
        })

    # High priority actions
    if audit_results['links']['broken_count'] > 10:
        action_items.append({
            'priority': 'high',
            'category': 'links',
            'action': f"Fix {audit_results['links']['broken_count']} broken external links",
            'details': 'High number of broken links impacts reference quality'
        })

    # Step 12: Populate template
    report_content = populate_template(template, {
        'timestamp': timestamp,
        'health_score': health_score,
        'health_interpretation': interpretation,
        'executive_summary': summary,
        'dimension_scores': format_dimension_table(scores, weights),
        'freshness_table': freshness_table,
        'link_issues': link_issues,
        'orphan_list': orphan_list,
        'action_items': format_action_items(action_items)
    })

    # Step 13: Create report note
    if output_path is None:
        timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d-%H%M')
        output_path = f"reports/audit-{timestamp_str}.md"

    report_path = mcp.obsidian.create_note(
        vault_path=vault_path,
        note_path=output_path,
        content=report_content
    )

    # Step 14: Return results
    return {
        'success': True,
        'report_note_path': report_path,
        'health_score': health_score,
        'health_interpretation': interpretation,
        'action_items': action_items,
        'timestamp': timestamp
    }
```

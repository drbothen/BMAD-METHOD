<!-- Powered by BMAD™ Core -->

# generate-audit-report

Generate comprehensive vault audit report using audit-report-tmpl.yaml with aggregated findings from all audit tasks.

## Purpose

Compile all audit results into a single, actionable report with prioritized action items and vault health score.

## Prerequisites

- audit-report-tmpl.yaml template available
- Completed audit tasks (Tasks 3-9) with cached results
- Vault health score calculation algorithm

## Inputs

- **audit_results** (object, required): Aggregated results from all audit tasks
- **vault_name** (string, required): Name of audited vault
- **output_path** (string, optional): Report save location (default: `/reports/audit-{timestamp}.md`)

## Outputs

```yaml
report_generation:
  report_path: string # Full path to generated report
  vault_health_score: integer # 0-100
  critical_issues_count: integer
  high_priority_count: integer
  medium_priority_count: integer
  low_priority_count: integer
  report_timestamp: string
```

## Algorithm

### Step 1: Aggregate Results from All Audit Tasks

```
audit_results = {
  temporal_freshness: load_cached_results('audit-temporal-freshness'),
  link_validation: load_cached_results('validate-external-links'),
  citation_validation: load_cached_results('validate-citations'),
  orphan_detection: load_cached_results('detect-orphaned-notes'),
  atomicity_violations: load_cached_results('audit-atomicity-violations'),
  duplicate_detection: load_cached_results('detect-duplicate-content'),
  metadata_audit: load_cached_results('audit-metadata-completeness')
}

# If any audit task not run: Run audit-full or return error
if any_missing_results:
  return error("Incomplete audit - run *audit-full first")
```

### Step 2: Calculate Vault Health Score (0-100)

**Algorithm:**

```
health_score = 100  # Start perfect

# Deduct points for each quality issue category

# 1. Temporal Freshness: -10 points per 10% stale
stale_percentage = audit_results.temporal_freshness.stale_percentage
health_score -= (stale_percentage / 10) * 10

# 2. Link Health: -15 points for broken, -5 for redirects
broken_links = audit_results.link_validation.broken_links_count
redirect_links = audit_results.link_validation.redirect_links_count
health_score -= (broken_links * 1.5)
health_score -= (redirect_links * 0.5)

# 3. Citation Quality: -10 points per 10% poor citations
poor_citations_percentage = (audit_results.citation_validation.notes_with_citation_issues / total_notes) * 100
health_score -= (poor_citations_percentage / 10) * 10

# 4. Orphan Rate: -10 points per 5% orphaned
orphan_percentage = audit_results.orphan_detection.orphan_percentage
health_score -= (orphan_percentage / 5) * 10

# 5. Atomicity: -15 points per 10% violations (extrapolated)
violation_percentage = (audit_results.atomicity_violations.estimated_violations_vault_wide / total_notes) * 100
health_score -= (violation_percentage / 10) * 15

# 6. Duplicates: -10 points per duplicate group
duplicate_groups = audit_results.duplicate_detection.duplicate_groups_count
health_score -= (duplicate_groups * 5)  # Max -50 for 10+ groups

# 7. Metadata: -10 points per 10% incomplete
incomplete_metadata_percentage = (audit_results.metadata_audit.notes_with_metadata_issues / total_notes) * 100
health_score -= (incomplete_metadata_percentage / 10) * 10

# Clamp to [0, 100]
health_score = max(0, min(100, round(health_score)))
```

**Health Score Interpretation:**

- **90-100**: Excellent
- **75-89**: Good
- **60-74**: Fair
- **40-59**: Poor
- **0-39**: Critical

### Step 3: Prioritize Action Items

Aggregate all findings and classify by impact:

**CRITICAL (Fix Immediately):**

- Broken links (4xx status codes)
- Missing required metadata (title, created)
- Exact duplicates (100% match)
- Notes with no source attribution (external claims)

**HIGH (Fix Soon):**

- Stale critical/high-priority notes (>10 incoming links, >180 days old)
- Incomplete citations (missing 2+ fields)
- Orphaned notes (no connections)
- Near-duplicates (>= 95% similarity)

**MEDIUM (Address When Possible):**

- Atomicity violations (score 0.5-0.7)
- Redirect links (3xx - update to new URL)
- Minor metadata issues (missing tags/type)
- Semantic duplicates (85-95% similarity)

**LOW (Nice to Have):**

- Format inconsistencies (citations, metadata)
- Optional metadata fields
- Stale low-priority notes (<2 incoming links)

### Step 4: Load Template and Substitute Variables

```
1. Load audit-report-tmpl.yaml
2. Substitute all 45+ variables:
   - timestamp, vault_name, total_notes
   - vault_health_score, health_score_interpretation
   - critical_issues_count, high_priority_count, etc.
   - stale_notes_list, broken_links_list, etc. (formatted as markdown)
   - action_items_critical, action_items_high, etc.
3. Generate markdown report from template
```

**Variable Formatting:**

Example: `stale_notes_list` variable:

```markdown
- **[CRITICAL]** [[Core Methodology Framework]] - Last updated 236 days ago (15 incoming links)
- **[HIGH]** [[Team Processes]] - Last updated 380 days ago (8 incoming links)
- **[MEDIUM]** [[Project Guidelines]] - Last updated 320 days ago (4 incoming links)
```

### Step 5: Save Report to Vault

```
1. Create /reports/ directory if not exists
2. Generate filename: audit-{timestamp}.md
   Example: audit-2025-11-06-14-30-00.md
3. Write report to vault
4. Return report_path and key metrics
```

### Step 6: Return Generation Results

```yaml
report_generation:
  report_path: '/reports/audit-2025-11-06-14-30-00.md'
  vault_health_score: 92
  critical_issues_count: 2
  high_priority_count: 5
  medium_priority_count: 12
  low_priority_count: 8
  report_timestamp: '2025-11-06T14:30:00Z'
```

## Vault Health Score Examples

**Example 1: Healthy Vault (Score: 92)**

```
Start: 100
- Temporal: -8 (8% stale)
- Links: 0 (2 broken = negligible)
- Citations: 0 (5% poor = negligible)
- Orphans: 0 (3% orphaned = negligible)
- Atomicity: 0 (5% violations = negligible)
- Duplicates: 0 (2 groups = negligible)
- Metadata: 0 (4% incomplete = negligible)
Final: 100 - 8 = 92 (Excellent)
```

**Example 2: Problematic Vault (Score: 28)**

```
Start: 100
- Temporal: -70 (70% stale)
- Links: -37.5 (25 broken)
- Citations: -40 (40% poor)
- Orphans: -60 (30% orphaned)
- Atomicity: -45 (30% violations)
- Duplicates: -15 (15 groups, capped at -15)
- Metadata: -36 (36% incomplete)
Calculation: 100 - 70 - 37.5 - 40 - 60 - 45 - 15 - 36 = -203.5
Final: max(0, -203.5) = 0 → Adjusted to 28 (Critical)
```

## Performance Target

<5 seconds (aggregation + template rendering + file write)

## Use Cases

**1. Executive Summary**

- High-level vault health overview
- Key findings at a glance

**2. Actionable Insights**

- Prioritized to-do list
- Clear next steps

**3. Trend Tracking**

- Compare reports over time
- Measure improvement

**4. Stakeholder Communication**

- Share vault quality metrics
- Justify maintenance efforts

## Error Handling

**Missing Audit Results:**

- Error: "Incomplete audit - missing {task_name} results"
- Action: Run `*audit-full` to complete all audits

**Template Not Found:**

- Error: "audit-report-tmpl.yaml not found"
- Action: Verify template file exists in expansion pack

**Write Permissions:**

- Error: "Cannot write to /reports/ directory"
- Action: Check vault permissions

## Testing

**Test Case:** Generate report from test audit results

- Vault: 1000 notes
- Results: All 7 audit tasks completed
- Expected: Report generated with score, all sections present

## Integration

Executed by:

- `*generate-report` command (standalone)
- `*audit-full` command (auto-generate after all audits)
- Progressive audit completion (generate after all batches)

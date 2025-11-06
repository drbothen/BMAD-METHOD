<!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Audit Coverage Checklist

# ------------------------------------------------------------

---

checklist:
  id: audit-coverage-checklist
  name: Audit Coverage Checklist
  description: Quality gates for comprehensive vault audit execution - ensures all audit dimensions are covered with adequate depth and rigor
  items:
    - "[ ] Temporal audit: All notes checked for staleness against threshold (default 180 days)"
    - "[ ] Link validation: All external URLs tested (HTTP status codes verified)"
    - "[ ] Citation audit: All notes checked for source attribution completeness"
    - "[ ] Orphan detection: Graph analysis performed, isolated notes identified"
    - "[ ] Atomicity audit: Random sample of 10% notes or min 20 notes analyzed for violations"
    - "[ ] Duplicate detection: Semantic similarity analysis performed across vault (threshold >= 0.85)"
    - "[ ] Metadata audit: All notes checked for required frontmatter fields"
    - "[ ] Report generation: Comprehensive report with all findings generated"
    - "[ ] Prioritization: Action items sorted by impact (critical/high/medium/low)"
    - "[ ] Vault health score: Overall score calculated (0-100 scale)"

---

## Purpose

This checklist ensures a comprehensive quality audit covers all critical dimensions of vault health. It serves as a validation tool to verify audit completeness and identify any gaps in coverage before finalizing the audit report.

## When to Use

- After running `*audit-full` command to verify completeness
- Before generating final audit report to ensure all dimensions covered
- When validating audit quality and rigor
- During audit testing to confirm comprehensive coverage
- When troubleshooting incomplete or partial audit results

## Coverage Criteria Details

### 1. Temporal Audit (Freshness)

**Check:** All notes in vault checked for last modification date against configured staleness threshold

**Coverage Requirements:**
- **100% of notes** must be analyzed for last_modified date
- Default threshold: 180 days (user-configurable)
- Prioritization by incoming link count:
  - Critical: >10 incoming links (domain-critical knowledge hubs)
  - High: >5 incoming links (frequently referenced)
  - Medium: 2-5 incoming links (some connections)
  - Low: <2 incoming links (minimal connections)
- Performance: Must complete in <5 seconds for 1000-note vault

**Pass Criteria:**
- All notes analyzed (100% coverage)
- Stale notes correctly identified (days_since_update > threshold)
- Prioritization accurate (based on incoming link count)
- Results include: note path, last_updated date, days_since_update, priority

**Verification:**
```
Verify: stale_notes_count + fresh_notes_count == total_notes
```

**Remediation if failed:**
- Re-run temporal freshness audit
- Check Obsidian MCP connection (must provide note metadata)
- Verify threshold parameter is valid integer
- Check for notes without last_modified metadata (handle gracefully)

---

### 2. Link Validation (External Links)

**Check:** All external URLs in vault tested for accessibility and HTTP status

**Coverage Requirements:**
- Parse all notes for external URLs (http:// and https://)
- Match patterns: `[text](URL)` and `<URL>`
- Test up to max_links URLs (default: 50 per audit run)
- Rate limiting: max 5 requests/second
- Timeout: 10 seconds per URL
- Security: SSRF prevention (block private IPs), protocol validation (http/https only)
- Classify results:
  - 2xx: Valid link (OK)
  - 3xx: Redirect (flag for update)
  - 4xx: Broken link (critical issue)
  - 5xx: Server error (flag for retry)
  - Timeout: Connection timeout (flag for retry or removal)

**Pass Criteria:**
- All discovered URLs validated (up to max_links limit)
- HTTP status codes correctly classified
- Security checks enforced (no SSRF, no invalid protocols)
- Results include: note path, URL, status_code, status_category

**Verification:**
```
Verify: broken_links_count + redirect_links_count + valid_links_count + timeout_count + error_count == total_links_tested
Verify: total_links_tested <= max_links (default 50)
```

**Remediation if failed:**
- Re-run link validation audit
- Check network connectivity
- Verify rate limiting not causing false timeouts
- Check User-Agent header: "BMAD-Obsidian-Auditor/1.0"
- Review security blocks (private IPs may be intentional on local network)

---

### 3. Citation Audit (Source Attribution)

**Check:** All notes checked for citation completeness and quality

**Coverage Requirements:**
- **100% of notes** must be analyzed for citation quality
- Check for Source Attribution section or metadata fields
- Required citation fields:
  - author (required)
  - title (required)
  - URL/ISBN (required for external sources)
  - date (required for time-sensitive content)
- Classify issues:
  - Critical: No source attribution for notes with external claims
  - High: Incomplete attribution (missing 2+ required fields)
  - Medium: Format inconsistencies
  - Low: Minor formatting issues
- Detect unattributed claims (factual statements without nearby citations)

**Pass Criteria:**
- All notes analyzed (100% coverage)
- Incomplete citations identified (missing 2+ required fields)
- Unattributed claims detected (>3 claims without citations)
- Results include: note path, issue_type, issue_severity, missing_fields, unattributed_claims_count

**Verification:**
```
Verify: notes_with_citation_issues + notes_with_complete_citations == total_notes
```

**Remediation if failed:**
- Re-run citation validation audit
- Adjust citation format detection (APA, MLA, Chicago)
- Review false positives (personal notes may not need citations)
- Check unattributed claim detection accuracy

---

### 4. Orphan Detection (Graph Analysis)

**Check:** Graph analysis performed to identify notes with no incoming/outgoing links

**Coverage Requirements:**
- **100% of notes** must be analyzed for link connections
- Build complete link graph from wikilinks `[[...]]`
- Identify three orphan categories:
  - No incoming links (never referenced)
  - No outgoing links (doesn't link to any notes)
  - Complete orphans (neither incoming nor outgoing)
- If Smart Connections available: Suggest linking opportunities (top 3 related notes per orphan, similarity >= 0.6)
- Optionally use Neo4j for advanced graph metrics (graceful degradation if unavailable)
- Performance: Must complete in <5 seconds for 1000-note vault

**Pass Criteria:**
- All notes analyzed (100% coverage)
- Link graph correctly constructed
- Orphans accurately identified
- Linking suggestions provided (if Smart Connections available)
- Results include: note path, has_incoming, has_outgoing, suggested_links

**Verification:**
```
Verify: orphaned_notes_count <= total_notes
Verify: Graph integrity (all links resolve to existing notes)
```

**Remediation if failed:**
- Re-run orphan detection audit
- Verify wikilink parsing (handle [[link|alias]] syntax)
- Check Smart Connections availability (optional, graceful degradation)
- Validate graph construction (no broken links in graph)

---

### 5. Atomicity Audit (Sample Analysis)

**Check:** Random sample of notes analyzed for atomicity violations using STORY-003 analyze-atomicity.md task

**Coverage Requirements:**
- Sampling strategy:
  - Large vaults (>200 notes): 10% random sample or min 20 notes
  - Small vaults (<=200 notes): analyze all notes
- For each sampled note, run 5 atomicity tests (STORY-003):
  1. Single claim test (one core concept)
  2. Evidence test (support without divergence)
  3. Self-contained test (understandable without external context)
  4. Title test (descriptive and unique)
  5. Related concepts test (links only, no in-depth explanations)
- Calculate atomicity score (0.0-1.0)
- Flag violations: score < 0.7
- Recommend fragmentation: score < 0.5
- Extrapolate to full vault: estimated_violations = (violations_found / sample_size) * total_notes

**Pass Criteria:**
- Sample size >= 10% of vault or >= 20 notes (whichever is greater)
- All sampled notes analyzed (100% of sample coverage)
- Atomicity scores calculated (0.0-1.0 scale)
- Violations identified (score < 0.7)
- Extrapolation to full vault performed
- Results include: note path, atomicity_score, failed_tests, fragmentation_recommended, estimated_violations_vault_wide

**Verification:**
```
Verify: sample_size >= min(0.1 * total_notes, 20)
Verify: atomicity_violations_count <= sample_size
Verify: estimated_violations_vault_wide == (violations_count / sample_size) * total_notes
```

**Remediation if failed:**
- Re-run atomicity audit with larger sample size
- Verify STORY-003 analyze-atomicity.md task is available
- Check atomicity score calculation (must be 0.0-1.0)
- Review false positives (some notes may be intentionally multi-faceted)

---

### 6. Duplicate Detection (Semantic Similarity)

**Check:** Semantic similarity analysis performed across vault to detect duplicate content

**Coverage Requirements:**
- **All notes** must be analyzed for duplicates (100% coverage)
- Two detection methods:
  - **Exact duplicates:** SHA-256 hash comparison (100% match)
  - **Semantic duplicates:** Smart Connections semantic search (similarity >= 0.85)
- Threshold: similarity >= 0.85 for duplicate detection (user-configurable)
- Group notes into duplicate clusters
- Prioritize by impact:
  - Critical: Exact duplicates (100% match)
  - High: Near-duplicates (similarity >= 0.95)
  - Medium: Semantic duplicates (similarity 0.85-0.95)
- Performance: Must complete in <10 seconds for 1000-note vault

**Pass Criteria:**
- All notes analyzed (100% coverage)
- Exact duplicates detected (SHA-256 hash collision)
- Semantic duplicates detected (if Smart Connections available)
- Duplicate groups correctly clustered
- Results include: duplicate_groups with note paths, similarity_score, is_exact_match

**Verification:**
```
Verify: All notes hashed (100% coverage for exact duplicates)
Verify: duplicate_groups_count >= 0
Verify: Each group has >= 2 notes
```

**Remediation if failed:**
- Re-run duplicate detection audit
- Check SHA-256 hashing implementation (must be consistent)
- Verify Smart Connections availability (optional, graceful degradation)
- Adjust similarity threshold if too many false positives (>0.85 is strict)

---

### 7. Metadata Audit (Frontmatter Completeness)

**Check:** All notes checked for required frontmatter metadata fields

**Coverage Requirements:**
- **100% of notes** must be analyzed for metadata completeness
- Required fields:
  - title (required, non-empty string)
  - created (required, ISO 8601 timestamp)
- Recommended fields:
  - tags (recommended, at least 1 tag)
  - type/building_block (recommended for atomic notes)
  - source/author (required for notes with external claims)
- Format validation:
  - Dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
  - Tags as array
  - Valid YAML syntax
- Classify issues:
  - Critical: Missing required fields (title, created)
  - High: Missing important fields (tags, type)
  - Medium: Format issues (wrong date format, malformed YAML)
  - Low: Missing optional fields
- Performance: Must complete in <3 seconds for 1000-note vault

**Pass Criteria:**
- All notes analyzed (100% coverage)
- Missing required fields identified
- Format issues detected
- Results include: note path, issue_severity, missing_fields, invalid_fields, recommendations

**Verification:**
```
Verify: notes_with_metadata_issues + notes_with_complete_metadata == total_notes
Verify: metadata_completeness_percentage == (notes_with_complete_metadata / total_notes) * 100
```

**Remediation if failed:**
- Re-run metadata audit
- Check YAML frontmatter parsing (must handle malformed YAML gracefully)
- Verify required fields match expansion pack configuration
- Review false positives (some notes may intentionally omit optional fields)

---

### 8. Report Generation (Comprehensive Report)

**Check:** Comprehensive audit report generated using audit-report-tmpl.yaml with all findings

**Coverage Requirements:**
- Aggregate results from all audit tasks (Tasks 3-9)
- Load audit-report-tmpl.yaml template
- Substitute all 45+ variables with aggregated data
- Generate markdown report with 10 sections:
  1. Executive Summary
  2. Temporal Freshness Findings
  3. Link Validation Findings
  4. Citation Quality Findings
  5. Orphaned Notes Findings
  6. Atomicity Violations Findings
  7. Duplicate Content Findings
  8. Metadata Completeness Findings
  9. Prioritized Action Items
  10. Vault Health Metrics
- Save report to vault: `/reports/audit-{timestamp}.md`

**Pass Criteria:**
- Report generated successfully
- All 10 sections present
- All variables substituted (no {{missing_variable}} placeholders)
- Report saved to vault with correct filename
- Results include: report_path, vault_health_score, critical_issues_count

**Verification:**
```
Verify: Report file exists at /reports/audit-{timestamp}.md
Verify: Report contains all 10 sections
Verify: No {{unresolved_variables}} in output
```

**Remediation if failed:**
- Re-run report generation
- Check template file exists (audit-report-tmpl.yaml)
- Verify all audit tasks completed (cached results available)
- Check file write permissions on /reports/ directory

---

### 9. Prioritization (Action Items)

**Check:** Action items sorted by impact and prioritized into four categories

**Coverage Requirements:**
- Aggregate all findings from audit tasks
- Classify each finding by impact:
  - **Critical:** Fix immediately (broken links, missing required metadata, exact duplicates)
  - **High:** Fix soon (stale important notes, incomplete citations, orphaned notes)
  - **Medium:** Address when possible (atomicity violations, redirects, minor metadata issues)
  - **Low:** Nice to have (format inconsistencies, optional metadata)
- Sort within each priority level by:
  - Critical: By severity (404 > 403 > other)
  - High: By note importance (incoming link count)
  - Medium: By ease of fix (quick wins first)
  - Low: By impact if addressed
- Format as actionable items with clear next steps

**Pass Criteria:**
- All findings classified by impact
- Action items sorted by priority
- Each item is actionable (has clear next step)
- Results include: action_items_critical, action_items_high, action_items_medium, action_items_low

**Verification:**
```
Verify: critical_issues_count + high_priority_count + medium_priority_count + low_priority_count == total_issues
Verify: Each action item has clear remediation step
```

**Remediation if failed:**
- Re-run prioritization
- Review impact classification logic
- Ensure all findings are included (no missing issues)
- Check action item formatting (must be clear and actionable)

---

### 10. Vault Health Score (Overall Score)

**Check:** Overall vault health score calculated using standardized algorithm

**Coverage Requirements:**
- Start at 100 points
- Apply deductions for each quality issue category:
  - Temporal Freshness: -10 points per 10% of notes stale
  - Link Health: -15 points for broken links, -5 for redirects
  - Citation Quality: -10 points per 10% notes with poor citations
  - Orphan Rate: -10 points per 5% orphaned notes
  - Atomicity: -15 points per 10% violations (extrapolated)
  - Duplicates: -10 points per duplicate group
  - Metadata: -10 points per 10% incomplete metadata
- Clamp to [0, 100] range: max(0, min(100, score))
- Interpret score:
  - 90-100: Excellent - Vault is well-maintained
  - 75-89: Good - Minor issues, but overall healthy
  - 60-74: Fair - Several issues need attention
  - 40-59: Poor - Significant problems affecting usability
  - 0-39: Critical - Major quality issues requiring immediate action

**Pass Criteria:**
- Health score calculated (0-100)
- Algorithm correctly applied with all deductions
- Score interpretation provided
- Results include: vault_health_score, health_score_interpretation

**Verification:**
```
Verify: 0 <= vault_health_score <= 100
Verify: health_score_interpretation matches score range
Verify: Deductions correctly calculated for each category
```

**Remediation if failed:**
- Re-run health score calculation
- Verify deduction formula for each category
- Check that extrapolation is used for atomicity violations
- Ensure score is clamped to [0, 100] range

---

## Scoring Algorithm

```python
# Calculate audit coverage score (0-100%)
total_criteria = 10
passed_criteria = 0

# Check each criterion
if temporal_audit_complete:
    passed_criteria += 1
if link_validation_complete:
    passed_criteria += 1
if citation_audit_complete:
    passed_criteria += 1
if orphan_detection_complete:
    passed_criteria += 1
if atomicity_audit_complete:
    passed_criteria += 1
if duplicate_detection_complete:
    passed_criteria += 1
if metadata_audit_complete:
    passed_criteria += 1
if report_generation_complete:
    passed_criteria += 1
if prioritization_complete:
    passed_criteria += 1
if vault_health_score_calculated:
    passed_criteria += 1

# Calculate coverage percentage
audit_coverage = (passed_criteria / total_criteria) * 100

# Pass threshold
is_comprehensive_audit = (audit_coverage >= 90)  # Must pass 9 out of 10 criteria
```

---

## Pass/Fail Criteria

**PASS (Comprehensive Audit):** audit_coverage >= 90% (9 out of 10 criteria passed)

**PARTIAL:** audit_coverage 70-89% (7-8 criteria passed, some gaps)

**FAIL (Incomplete Audit):** audit_coverage < 70% (significant gaps, re-run required)

**Blocking Failures (auto-fail regardless of score):**
- Report generation failed (criterion 8)
- Vault health score not calculated (criterion 10)
- Less than 5 criteria passed (< 50% coverage)

**Critical Warnings (fail if not addressed):**
- Temporal audit incomplete (criterion 1)
- Metadata audit incomplete (criterion 7)
- Prioritization not performed (criterion 9)

---

## Usage in Agent Commands

### \*audit-full command

After running all audit tasks, execute this checklist to verify comprehensive coverage before finalizing report.

### \*generate-report command

Before generating report, verify criteria 1-7 are complete (all audit tasks executed).

### \*progressive command

For progressive audits, verify checklist incrementally after each batch completes, aggregate at end.

### \*yolo mode

Still run checklist validation, but auto-accept partial coverage (70%+) without blocking.

---

## Testing

To test this checklist:

1. **Full audit test:** Run `*audit-full` and verify all 10 criteria pass
2. **Partial audit test:** Run only `*audit-freshness` and verify only 1 criterion passes
3. **Missing audit test:** Skip `*audit-links` and verify criterion 2 fails
4. **Progressive audit test:** Run progressive mode, verify checklist passes after all batches complete
5. **Error scenario test:** Simulate Obsidian MCP unavailable, verify graceful handling

All test scenarios documented in STORY-006 testing section.

---

## Example Validation Report

```yaml
audit_coverage_check:
  timestamp: 2025-11-06T14:30:00Z
  vault: "My Second Brain"
  total_criteria: 10
  passed_criteria: 10
  coverage_percentage: 100
  is_comprehensive: true
  criteria:
    - {id: 1, name: "Temporal audit", status: PASS, notes: "1000 notes analyzed"}
    - {id: 2, name: "Link validation", status: PASS, notes: "50 URLs tested"}
    - {id: 3, name: "Citation audit", status: PASS, notes: "1000 notes checked"}
    - {id: 4, name: "Orphan detection", status: PASS, notes: "Graph analysis complete"}
    - {id: 5, name: "Atomicity audit", status: PASS, notes: "100 notes sampled"}
    - {id: 6, name: "Duplicate detection", status: PASS, notes: "1000 notes hashed"}
    - {id: 7, name: "Metadata audit", status: PASS, notes: "1000 notes validated"}
    - {id: 8, name: "Report generation", status: PASS, notes: "Report saved"}
    - {id: 9, name: "Prioritization", status: PASS, notes: "Action items sorted"}
    - {id: 10, name: "Vault health score", status: PASS, notes: "Score: 92/100"}
  verdict: "PASS - Comprehensive audit complete"
  recommendations: []
```

---

## Integration with Quality Auditor Agent

This checklist is automatically executed when:

1. `*audit-full` command completes - Verify all criteria passed
2. `*generate-report` command runs - Verify criteria 1-7 complete before generating report
3. Progressive audit finishes - Verify incremental coverage across all batches
4. Agent startup (if previous incomplete audit detected) - Resume or restart based on checklist state

The Quality Auditor Agent uses this checklist as a quality gate to ensure no audit dimensions are missed before declaring the audit complete and delivering the final report to the user.

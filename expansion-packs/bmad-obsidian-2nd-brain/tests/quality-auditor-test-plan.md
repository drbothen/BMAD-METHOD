<!-- Powered by BMAD™ Core -->

# Quality Auditor Agent - Comprehensive Test Plan

**Story:** STORY-006 - Implement Quality Auditor Agent
**Test Plan Version:** 1.0
**Created:** 2025-11-06
**Test Environment:** Claude Desktop or Cursor with Obsidian MCP configured

---

## Test Objectives

Validate that the Quality Auditor Agent:

1. Accurately detects quality issues across all 7 audit dimensions
2. Generates comprehensive audit reports with correct health scores
3. Implements all 13 commands correctly
4. Enforces security measures (SSRF prevention, rate limiting)
5. Handles error scenarios gracefully
6. Supports progressive audit mode for large vaults
7. Meets all 11 acceptance criteria (AC1-AC11)
8. Achieves performance targets for each audit task

---

## Test Vault Structure

### Test Data Location

`expansion-packs/bmad-obsidian-2nd-brain/tests/quality-auditor-test-data/`

### Test Vault Requirements

**Total Notes:** 100 notes with planted quality issues

**Issue Distribution:**

- 50 stale notes (>180 days old)
- 50 external links (30 valid, 5 redirects, 10 broken, 5 timeouts)
- 30 citation issues (10 incomplete, 10 unattributed claims, 10 format issues)
- 30 orphaned notes (15 no incoming, 10 no outgoing, 5 complete orphans)
- 20 atomicity violations (from STORY-003 test set: 10 atomic, 10 non-atomic)
- 15 duplicate notes (5 exact, 5 near-duplicates, 5 semantic duplicates)
- 40 metadata issues (20 critical, 15 high, 5 medium)

**File Structure:**

```
test-vault/
├── notes/
│   ├── fresh/           # 20 notes (updated within 30 days)
│   ├── aging/           # 30 notes (31-180 days old)
│   ├── stale/           # 50 notes (>180 days old)
│   ├── with-links/      # 50 notes with external URLs
│   ├── citations/       # 30 notes with varying citation quality
│   ├── orphans/         # 30 notes with no connections
│   ├── duplicates/      # 15 duplicate note groups
│   └── incomplete-meta/ # 40 notes with metadata issues
└── reports/             # Output directory for audit reports
```

---

## Test Categories

## 1. Temporal Freshness Audit Tests

### Test 1.1: Basic Stale Note Detection

**Objective:** Verify agent correctly identifies notes older than threshold

**Test Data:**

- 100 notes total
- 50 notes >180 days old (stale)
- 30 notes 31-180 days old (aging)
- 20 notes <30 days old (fresh)

**Test Steps:**

1. Activate Quality Auditor Agent
2. Run `*audit-freshness` (default 180-day threshold)
3. Review results

**Expected Results:**

- stale_notes_count = 50
- All 50 stale notes correctly identified
- Each note includes: note_path, last_updated, days_since_update, priority
- Performance: <5 seconds for 100-note vault

**Pass Criteria:**

- Detection accuracy >= 95% (47+ out of 50 detected)
- No false positives (<3 fresh notes flagged as stale)
- Performance target met

---

### Test 1.2: Prioritization by Importance

**Objective:** Verify stale notes prioritized by incoming link count

**Test Data:**

- 10 stale notes with >10 incoming links (CRITICAL priority)
- 10 stale notes with 6-10 incoming links (HIGH priority)
- 15 stale notes with 2-5 incoming links (MEDIUM priority)
- 15 stale notes with <2 incoming links (LOW priority)

**Test Steps:**

1. Run `*audit-freshness`
2. Review priority assignments

**Expected Results:**

- 10 notes marked CRITICAL
- 10 notes marked HIGH
- 15 notes marked MEDIUM
- 15 notes marked LOW

**Pass Criteria:**

- Prioritization accuracy >= 90% (45+ out of 50 correctly prioritized)
- Sorted correctly (CRITICAL first, then by days_since_update)

---

### Test 1.3: Custom Threshold

**Objective:** Verify custom staleness threshold works

**Test Steps:**

1. Run `*audit-freshness 90` (90-day threshold)
2. Review results

**Expected Results:**

- stale_notes_count > 50 (includes 31-180 day notes)
- Aging notes now flagged as stale

**Pass Criteria:**

- Threshold applied correctly
- More notes detected than default 180-day threshold

---

## 2. External Link Validation Tests

### Test 2.1: Broken Link Detection (4xx)

**Objective:** Verify broken links detected accurately

**Test Data:**

- 10 links with 404 Not Found
- 2 links with 403 Forbidden
- 1 link with 410 Gone

**Test Steps:**

1. Run `*audit-links`
2. Review broken_links_count

**Expected Results:**

- broken_links_count = 13
- All 13 links flagged with severity: CRITICAL
- Status codes correctly recorded (404, 403, 410)

**Pass Criteria:**

- Detection accuracy: 100% (all 13 detected)
- No false positives

---

### Test 2.2: Redirect Detection (3xx)

**Objective:** Verify redirects detected and redirect URLs captured

**Test Data:**

- 3 links with 301 Moved Permanently
- 2 links with 302 Found (temporary redirect)

**Test Steps:**

1. Run `*audit-links`
2. Review redirect_links_count

**Expected Results:**

- redirect_links_count = 5
- All 5 redirects flagged with severity: MEDIUM
- redirect_url field populated for each

**Pass Criteria:**

- Detection accuracy: 100% (all 5 detected)
- Redirect URLs correctly captured

---

### Test 2.3: Timeout Handling

**Objective:** Verify timeout detection for slow servers

**Test Data:**

- 5 links to slow servers (>10s response time)

**Test Steps:**

1. Run `*audit-links`
2. Review timeout_count

**Expected Results:**

- timeout_count = 5
- All 5 timeouts flagged with severity: HIGH
- error_message: "Connection timeout after 10s"

**Pass Criteria:**

- No infinite hangs (all requests timeout at 10s)
- Timeout detection: 100%

---

### Test 2.4: Security - SSRF Prevention

**Objective:** Verify private IP blocking prevents SSRF attacks

**Test Data:**

- 1 link: `http://127.0.0.1/admin`
- 1 link: `http://192.168.1.1/router`
- 1 link: `http://10.0.0.1/internal`

**Test Steps:**

1. Run `*audit-links`
2. Review security_violations_count

**Expected Results:**

- security_violations_count = 3
- All 3 links flagged with status: SECURITY_BLOCKED
- severity: CRITICAL
- error_message: "SSRF attempt: private IP"
- **No actual network requests made to private IPs**

**Pass Criteria:**

- All private IPs blocked: 100%
- No false negatives (no SSRF bypass)

---

### Test 2.5: Security - Invalid Protocol Blocking

**Objective:** Verify only http/https protocols allowed

**Test Data:**

- 1 link: `file:///etc/passwd`
- 1 link: `javascript:alert('xss')`
- 1 link: `data:text/html,<script>alert('xss')</script>`

**Test Steps:**

1. Run `*audit-links`
2. Review security_violations_count

**Expected Results:**

- security_violations_count = 3
- All 3 links flagged with status: SECURITY_BLOCKED
- severity: CRITICAL
- error_message: "Invalid protocol - only http/https allowed"

**Pass Criteria:**

- All invalid protocols blocked: 100%
- No protocol injection attacks successful

---

### Test 2.6: Rate Limiting Enforcement

**Objective:** Verify rate limiting (5 requests/second) enforced

**Test Data:**

- 50 valid links to test

**Test Steps:**

1. Run `*audit-links`
2. Measure execution time

**Expected Results:**

- Execution time >= 10 seconds (50 links × 0.2s/link)
- Rate: ~5 requests/second

**Pass Criteria:**

- Rate limiting enforced (not exceeding 5 req/sec)
- No burst requests

---

### Test 2.7: Max Links Limit

**Objective:** Verify max_links parameter works

**Test Data:**

- 100 links in vault

**Test Steps:**

1. Run `*audit-links 20`
2. Review total_links_tested

**Expected Results:**

- total_links_found = 100
- total_links_tested = 20 (capped at max_links)

**Pass Criteria:**

- Limit enforced correctly
- First 20 links tested, remaining skipped

---

## 3. Citation Validation Tests

### Test 3.1: Incomplete Citations Detection

**Objective:** Detect citations missing 2+ required fields

**Test Data:**

- 10 notes with incomplete citations (missing author, title, url, or date)

**Test Steps:**

1. Run `*audit-citations`
2. Review citation_issues

**Expected Results:**

- 10 notes flagged with issue_severity: HIGH
- issue_type: "Incomplete citation"
- missing_fields array populated correctly

**Pass Criteria:**

- Detection accuracy >= 90% (9+ out of 10 detected)

---

### Test 3.2: Unattributed Claims Detection

**Objective:** Detect notes with >3 factual claims but no citations

**Test Data:**

- 10 notes with >3 unattributed factual claims
- 0 citations present

**Test Steps:**

1. Run `*audit-citations`
2. Review unattributed_claims_count

**Expected Results:**

- 10 notes flagged with issue_severity: CRITICAL
- issue_type: "No source attribution"

**Pass Criteria:**

- Detection accuracy >= 80% (8+ out of 10 detected)
- Claim detection algorithm works

---

### Test 3.3: Format Consistency Check

**Objective:** Detect citation format inconsistencies

**Test Data:**

- 10 notes with format issues (missing quotes, wrong punctuation)

**Test Steps:**

1. Run `*audit-citations`
2. Review format-related issues

**Expected Results:**

- 10 notes flagged with issue_severity: MEDIUM
- issue_type: "Format inconsistencies"

**Pass Criteria:**

- Detection accuracy >= 70% (7+ out of 10 detected)

---

### Test 3.4: Performance Benchmark

**Objective:** Verify performance target met

**Test Steps:**

1. Run `*audit-citations` on 100-note vault
2. Measure execution time

**Expected Results:**

- Execution time < 3 seconds

**Pass Criteria:**

- Performance target met

---

## 4. Orphan Detection Tests

### Test 4.1: Complete Orphan Detection

**Objective:** Detect notes with neither incoming nor outgoing links

**Test Data:**

- 5 notes with no incoming or outgoing links

**Test Steps:**

1. Run `*audit-orphans`
2. Filter orphan_type: 'COMPLETE'

**Expected Results:**

- 5 complete orphans detected
- priority: CRITICAL

**Pass Criteria:**

- Detection accuracy: 100% (all 5 detected)

---

### Test 4.2: No Incoming Links Detection

**Objective:** Detect notes never referenced by other notes

**Test Data:**

- 15 notes with no incoming links (but have outgoing links)

**Test Steps:**

1. Run `*audit-orphans`
2. Filter orphan_type: 'NO_INCOMING'

**Expected Results:**

- 15 notes detected
- priority: HIGH

**Pass Criteria:**

- Detection accuracy >= 95% (14+ out of 15 detected)

---

### Test 4.3: No Outgoing Links Detection

**Objective:** Detect notes that don't link to any other notes

**Test Data:**

- 10 notes with no outgoing links (but have incoming links)

**Test Steps:**

1. Run `*audit-orphans`
2. Filter orphan_type: 'NO_OUTGOING'

**Expected Results:**

- 10 notes detected
- priority: MEDIUM

**Pass Criteria:**

- Detection accuracy >= 95% (9+ out of 10 detected)

---

### Test 4.4: Linking Suggestions (Smart Connections)

**Objective:** Verify link suggestions provided if Smart Connections available

**Prerequisites:**

- Smart Connections MCP configured

**Test Steps:**

1. Run `*audit-orphans`
2. Review suggested_links for each orphan

**Expected Results:**

- Top 3 suggested links per orphan
- Each suggestion includes: target_note, similarity_score, link_type

**Pass Criteria:**

- Suggestions relevant (similarity_score >= 0.6)
- Suggestions provided for all orphans

---

### Test 4.5: Graceful Degradation (No Smart Connections)

**Objective:** Verify orphan detection works without Smart Connections

**Prerequisites:**

- Smart Connections MCP NOT available

**Test Steps:**

1. Run `*audit-orphans`
2. Review results

**Expected Results:**

- Orphans detected correctly
- suggested_links = [] (empty, no suggestions)
- No errors or failures

**Pass Criteria:**

- Core functionality works without optional dependency

---

### Test 4.6: Performance Benchmark

**Objective:** Verify performance target met

**Test Steps:**

1. Run `*audit-orphans` on 100-note vault
2. Measure execution time

**Expected Results:**

- Execution time < 5 seconds

**Pass Criteria:**

- Performance target met

---

## 5. Atomicity Violation Tests

### Test 5.1: Non-Atomic Note Detection

**Objective:** Detect notes with multiple tangled concepts (score < 0.7)

**Test Data:**

- 10 non-atomic notes (from STORY-003 test set)
- Expected atomicity scores < 0.7

**Test Steps:**

1. Run `*audit-atomicity`
2. Review atomicity_violations

**Expected Results:**

- 10 violations detected
- All scores < 0.7
- failed_tests array populated

**Pass Criteria:**

- Detection accuracy >= 90% (9+ out of 10 detected)
- Scores match STORY-003 analyze-atomicity results

---

### Test 5.2: Atomic Note Pass-Through

**Objective:** Verify atomic notes pass (score >= 0.7)

**Test Data:**

- 10 atomic notes (from STORY-003 test set)
- Expected atomicity scores >= 0.7

**Test Steps:**

1. Run `*audit-atomicity`
2. Verify atomic notes NOT in violations list

**Expected Results:**

- 0 violations from atomic notes
- All scores >= 0.7

**Pass Criteria:**

- False positive rate < 10% (max 1 false positive)

---

### Test 5.3: Fragmentation Recommendations

**Objective:** Verify fragmentation recommended for severe violations (score < 0.5)

**Test Data:**

- 5 notes with atomicity score < 0.5

**Test Steps:**

1. Run `*audit-atomicity`
2. Review fragmentation_recommended flag

**Expected Results:**

- 5 notes with fragmentation_recommended = true
- Suggestions include: "Fragment note using STORY-003 fragment-note.md task"

**Pass Criteria:**

- All severe violations flagged for fragmentation

---

### Test 5.4: Sampling Strategy

**Objective:** Verify sampling strategy for large vaults

**Test Data:**

- 100-note vault (should sample 10% = 10 notes)

**Test Steps:**

1. Run `*audit-atomicity` (default sample size)
2. Review sample_size

**Expected Results:**

- sample_size = 10 (10% of 100)
- Random sample selected

**Pass Criteria:**

- Sampling strategy correctly applied

---

### Test 5.5: Extrapolation to Full Vault

**Objective:** Verify extrapolation formula works

**Test Data:**

- 100-note vault
- 10-note sample
- 5 violations found in sample

**Test Steps:**

1. Run `*audit-atomicity`
2. Review estimated_violations_vault_wide

**Expected Results:**

- estimated_violations_vault_wide = (5 / 10) × 100 = 50

**Pass Criteria:**

- Formula applied correctly

---

### Test 5.6: Performance Benchmark

**Objective:** Verify performance target met

**Test Steps:**

1. Run `*audit-atomicity` on 20-note sample
2. Measure execution time

**Expected Results:**

- Execution time < 10 seconds

**Pass Criteria:**

- Performance target met

---

## 6. Duplicate Content Detection Tests

### Test 6.1: Exact Duplicate Detection (100% match)

**Objective:** Detect notes with identical content (SHA-256 collision)

**Test Data:**

- 5 exact duplicate pairs (10 notes total with same content, different filenames)

**Test Steps:**

1. Run `*audit-duplicates`
2. Filter duplicate_type: 'EXACT'

**Expected Results:**

- 5 duplicate groups detected
- similarity_score = 1.0 for all
- is_exact_match = true
- severity: CRITICAL

**Pass Criteria:**

- Detection accuracy: 100% (all 5 groups detected)
- No false positives

---

### Test 6.2: Near-Duplicate Detection (>= 95% similarity)

**Objective:** Detect notes with near-identical content

**Test Data:**

- 5 near-duplicate pairs (similarity >= 0.95)

**Test Steps:**

1. Run `*audit-duplicates`
2. Filter duplicate_type: 'NEAR'

**Expected Results:**

- 5 duplicate groups detected
- similarity_score >= 0.95
- severity: HIGH

**Pass Criteria:**

- Detection accuracy >= 80% (4+ out of 5 detected)

---

### Test 6.3: Semantic Duplicate Detection (85-95% similarity)

**Objective:** Detect semantically similar notes

**Test Data:**

- 5 semantic duplicate pairs (similarity 0.85-0.95)

**Prerequisites:**

- Smart Connections MCP configured

**Test Steps:**

1. Run `*audit-duplicates`
2. Filter duplicate_type: 'SEMANTIC'

**Expected Results:**

- 5 duplicate groups detected
- similarity_score 0.85-0.95
- severity: MEDIUM

**Pass Criteria:**

- Detection accuracy >= 60% (3+ out of 5 detected)
- Precision >= 70% (low false positive rate)

---

### Test 6.4: Custom Threshold

**Objective:** Verify custom similarity threshold works

**Test Steps:**

1. Run `*audit-duplicates 0.90` (stricter threshold)
2. Compare to default 0.85

**Expected Results:**

- Fewer duplicates detected than default threshold
- Only pairs with similarity >= 0.90 reported

**Pass Criteria:**

- Threshold applied correctly

---

### Test 6.5: Performance Benchmark

**Objective:** Verify performance target met

**Test Steps:**

1. Run `*audit-duplicates` on 100-note vault
2. Measure execution time

**Expected Results:**

- Execution time < 10 seconds

**Pass Criteria:**

- Performance target met

---

## 7. Metadata Completeness Tests

### Test 7.1: Critical Issues (Missing Required Fields)

**Objective:** Detect notes missing title or created date

**Test Data:**

- 15 notes missing title field
- 5 notes missing created date

**Test Steps:**

1. Run `*audit-metadata`
2. Filter issue_severity: 'CRITICAL'

**Expected Results:**

- 20 critical issues detected
- missing_fields includes 'title' or 'created'

**Pass Criteria:**

- Detection accuracy >= 95% (19+ out of 20 detected)

---

### Test 7.2: High Priority Issues (Missing Important Fields)

**Objective:** Detect notes missing tags or type

**Test Data:**

- 10 notes missing tags
- 5 notes missing type/building_block

**Test Steps:**

1. Run `*audit-metadata`
2. Filter issue_severity: 'HIGH'

**Expected Results:**

- 15 high-priority issues detected
- missing_fields includes 'tags' or 'type'

**Pass Criteria:**

- Detection accuracy >= 90% (13+ out of 15 detected)

---

### Test 7.3: Medium Issues (Format Problems)

**Objective:** Detect format issues (wrong date format, malformed YAML)

**Test Data:**

- 3 notes with wrong date format (not ISO 8601)
- 2 notes with malformed YAML

**Test Steps:**

1. Run `*audit-metadata`
2. Filter issue_severity: 'MEDIUM'

**Expected Results:**

- 5 medium issues detected
- invalid_fields array populated

**Pass Criteria:**

- Detection accuracy >= 80% (4+ out of 5 detected)

---

### Test 7.4: Auto-Fix Suggestions

**Objective:** Verify helpful remediation suggestions provided

**Test Steps:**

1. Run `*audit-metadata`
2. Review recommendations array for each issue

**Expected Results:**

- Each issue has at least 1 recommendation
- Recommendations are actionable (e.g., "Add title field based on filename")

**Pass Criteria:**

- 100% of issues have recommendations

---

### Test 7.5: Performance Benchmark

**Objective:** Verify performance target met

**Test Steps:**

1. Run `*audit-metadata` on 100-note vault
2. Measure execution time

**Expected Results:**

- Execution time < 3 seconds

**Pass Criteria:**

- Performance target met

---

## 8. Comprehensive Report Generation Tests

### Test 8.1: Full Audit Report Generation

**Objective:** Verify comprehensive report generated with all sections

**Test Steps:**

1. Run `*audit-full` on test vault
2. Review generated report at `/reports/audit-{timestamp}.md`

**Expected Results:**

- Report file created
- All 10 sections present:
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
- All variables substituted (no {{unresolved_variables}})

**Pass Criteria:**

- Report generated successfully
- All sections present and populated

---

### Test 8.2: Vault Health Score Calculation

**Objective:** Verify health score calculated correctly

**Test Data:**

- Test vault with known issues (expected score: 0-30 due to planted issues)

**Test Steps:**

1. Run `*audit-full`
2. Review vault_health_score

**Expected Results:**

- vault_health_score calculated (0-100)
- Score interpretation provided (e.g., "Critical")
- Deductions correctly applied:
  - Temporal: -10 per 10% stale
  - Links: -15 per broken, -5 per redirect
  - Citations: -10 per 10% poor
  - Orphans: -10 per 5% orphaned
  - Atomicity: -15 per 10% violations
  - Duplicates: -10 per group
  - Metadata: -10 per 10% incomplete

**Pass Criteria:**

- Score within expected range (0-30 for test vault)
- Formula applied correctly
- Deductions traceable

---

### Test 8.3: Action Item Prioritization

**Objective:** Verify action items sorted by impact

**Test Steps:**

1. Run `*audit-full`
2. Review action items section

**Expected Results:**

- Action items sorted into 4 categories:
  - Critical: Broken links, missing required metadata, exact duplicates
  - High: Stale important notes, incomplete citations, orphans
  - Medium: Atomicity violations, redirects, minor metadata
  - Low: Format inconsistencies, optional fields
- Items within each category sorted by impact

**Pass Criteria:**

- Prioritization accurate
- All findings included

---

## 9. Command Implementation Tests

### Test 9.1: \*help Command

**Test Steps:**

1. Run `*help`

**Expected Results:**

- All 13 commands displayed:
  1. \*help
  2. \*audit-full
  3. \*audit-freshness
  4. \*audit-links
  5. \*audit-citations
  6. \*audit-orphans
  7. \*audit-atomicity
  8. \*audit-duplicates
  9. \*audit-metadata
  10. \*generate-report
  11. \*progressive
  12. \*yolo
  13. \*exit
- Each command includes description

**Pass Criteria:**

- All commands listed
- Descriptions clear

---

### Test 9.2: \*audit-full Command

**Test Steps:**

1. Run `*audit-full`

**Expected Results:**

- All 7 audit tasks executed sequentially
- Comprehensive report generated
- report_path, vault_health_score, critical_issues_count returned

**Pass Criteria:**

- All audits complete
- Report generated

---

### Test 9.3: \*audit-freshness [threshold] Command

**Test Steps:**

1. Run `*audit-freshness 90`

**Expected Results:**

- Custom 90-day threshold applied
- Stale notes detected

**Pass Criteria:**

- Custom threshold works

---

### Test 9.4: \*audit-links [max_links] Command

**Test Steps:**

1. Run `*audit-links 20`

**Expected Results:**

- Max 20 links validated
- total_links_tested = 20

**Pass Criteria:**

- Max links limit enforced

---

### Test 9.5: \*progressive [batch_size] Command

**Test Steps:**

1. Run `*progressive 500`
2. Run `*audit-full`

**Expected Results:**

- Progressive mode enabled
- batch_size = 500
- Audit processes in batches

**Pass Criteria:**

- Progressive mode toggles on/off
- Batch size configurable

---

### Test 9.6: \*yolo Command

**Test Steps:**

1. Run `*yolo`
2. Run `*audit-full`

**Expected Results:**

- Yolo mode enabled
- No confirmation prompts during audit

**Pass Criteria:**

- Mode toggles correctly

---

### Test 9.7: \*exit Command

**Test Steps:**

1. Run `*exit`

**Expected Results:**

- Confirmation prompt: "Exit Quality Auditor Agent? (y/n)"
- Agent exits after confirmation

**Pass Criteria:**

- Exit works with confirmation

---

## 10. Error Scenario Tests

### Test 10.1: Obsidian MCP Unavailable

**Test Steps:**

1. Disconnect Obsidian MCP
2. Run `*audit-full`

**Expected Results:**

- Error: "Obsidian MCP unavailable - check connection"
- Graceful failure (no crash)

**Pass Criteria:**

- Clear error message
- Graceful handling

---

### Test 10.2: Smart Connections Unavailable

**Test Steps:**

1. Disable Smart Connections MCP
2. Run `*audit-orphans`

**Expected Results:**

- Orphan detection works
- No link suggestions (suggested_links = [])
- Warning: "Smart Connections unavailable - link suggestions disabled"

**Pass Criteria:**

- Graceful degradation
- Core functionality works

---

### Test 10.3: Invalid Threshold Values

**Test Steps:**

1. Run `*audit-freshness -50` (negative threshold)

**Expected Results:**

- Error: "Invalid threshold - must be positive integer"

**Pass Criteria:**

- Validation error with helpful message

---

### Test 10.4: Empty Vault

**Test Steps:**

1. Run `*audit-full` on empty vault (0 notes)

**Expected Results:**

- Report: "No notes to audit"
- vault_health_score = 100 (no issues)

**Pass Criteria:**

- Handled gracefully

---

## 11. Progressive Audit Mode Tests

### Test 11.1: Batch Division

**Objective:** Verify vault divided into batches correctly

**Test Data:**

- 1500-note vault
- batch_size = 500

**Test Steps:**

1. Run `*progressive 500`
2. Run `*audit-full`

**Expected Results:**

- 3 batches created (500, 500, 500)
- Progress displayed: "Batch 1/3 complete: 500/1500 notes (33%)"

**Pass Criteria:**

- Batch division correct

---

### Test 11.2: Checkpointing

**Objective:** Verify progress saved after each batch

**Test Steps:**

1. Run progressive audit
2. After batch 1 completes, check `.audit-progress.json` exists

**Expected Results:**

- Checkpoint file created
- Contains: audit_session_id, completed_batches, cached_results

**Pass Criteria:**

- Checkpoint saved correctly

---

### Test 11.3: Pause/Resume Workflow

**Objective:** Verify audit can be paused and resumed

**Test Steps:**

1. Start progressive audit
2. Complete 2/5 batches
3. Interrupt (Ctrl+C)
4. Run `*audit-full` again

**Expected Results:**

- Resume prompt: "Resume previous audit? (2/5 batches complete)"
- After confirmation, resume from batch 3

**Pass Criteria:**

- Resume works correctly
- No re-audit of completed batches

---

### Test 11.4: Result Aggregation

**Objective:** Verify findings aggregated from all batches

**Test Steps:**

1. Complete progressive audit (5 batches)
2. Review final report

**Expected Results:**

- Report includes findings from all 5 batches
- No duplicate findings
- vault_health_score calculated from full vault

**Pass Criteria:**

- Aggregation accurate
- No data loss

---

### Test 11.5: Memory Management

**Objective:** Verify memory stays within O(batch_size) bounds

**Test Steps:**

1. Run progressive audit on 10,000-note vault
2. Monitor memory usage during execution

**Expected Results:**

- Peak memory ~50MB per 1000-note batch
- Memory released after each batch checkpoint

**Pass Criteria:**

- Memory usage stable
- No memory leaks

---

## 12. Audit Coverage Checklist Validation

### Test 12.1: Run Audit Coverage Checklist

**Test Steps:**

1. Run `*audit-full` on test vault
2. Execute audit-coverage-checklist.md
3. Count passed criteria

**Expected Results:**

- 10 out of 10 criteria pass
- audit_coverage = 100%
- is_comprehensive = true

**Pass Criteria:**

- > = 90% coverage (9 out of 10 criteria passed)

---

## 13. Acceptance Criteria Validation

### AC1: Agent File Created

**Verification:** quality-auditor-agent.md exists at `expansion-packs/bmad-obsidian-2nd-brain/agents/`

**Status:** ✓ PASS

---

### AC2: Temporal Freshness Audit

**Verification:** Run `*audit-freshness`, verify:

- Notes older than threshold detected
- Prioritized by importance (incoming link count)

**Status:** ✓ PASS (if Test 1.1 and 1.2 pass)

---

### AC3: External Link Validation

**Verification:** Run `*audit-links`, verify:

- HTTP status codes tested (2xx, 3xx, 4xx, 5xx)
- Broken links (4xx) flagged
- Redirects (3xx) flagged
- Timeouts detected

**Status:** ✓ PASS (if Tests 2.1-2.3 pass)

---

### AC4: Citation Validation

**Verification:** Run `*audit-citations`, verify:

- Completeness checked (author, title, url, date)
- Format accuracy validated
- Unattributed claims detected

**Status:** ✓ PASS (if Tests 3.1-3.2 pass)

---

### AC5: Orphan Detection

**Verification:** Run `*audit-orphans`, verify:

- Notes with no incoming/outgoing links detected
- Linking suggestions provided (if Smart Connections available)

**Status:** ✓ PASS (if Tests 4.1-4.3 pass)

---

### AC6: Atomicity Violations

**Verification:** Run `*audit-atomicity`, verify:

- Notes with multiple concepts detected using STORY-003 atomicity checklist
- Violations flagged (score < 0.7)

**Status:** ✓ PASS (if Test 5.1 passes)

---

### AC7: Duplicate Content Detection

**Verification:** Run `*audit-duplicates`, verify:

- Semantically similar notes detected (threshold >= 0.85)
- Exact duplicates detected

**Status:** ✓ PASS (if Tests 6.1-6.3 pass)

---

### AC8: Metadata Completeness

**Verification:** Run `*audit-metadata`, verify:

- Required frontmatter fields checked (title, created)
- Format validation (ISO 8601 dates, valid YAML)

**Status:** ✓ PASS (if Tests 7.1-7.3 pass)

---

### AC9: Comprehensive Audit Report

**Verification:** Run `*audit-full`, verify:

- Report generated using audit-report-tmpl.yaml
- Actionable prioritized findings present

**Status:** ✓ PASS (if Tests 8.1-8.3 pass)

---

### AC10: Audit Coverage Checklist

**Verification:** Run audit-coverage-checklist.md, verify:

- > = 90% coverage (9 out of 10 criteria passed)

**Status:** ✓ PASS (if Test 12.1 passes)

---

### AC11: All 13 Commands Implemented

**Verification:** Run `*help`, verify all 13 commands listed

**Status:** ✓ PASS (if Test 9.1 passes)

---

## Test Execution Summary

### Prerequisites for Testing

1. **Environment Setup:**
   - Claude Desktop or Cursor installed
   - Obsidian MCP configured and connected
   - Smart Connections MCP configured (optional)
   - Neo4j Graphiti MCP configured (optional)

2. **Test Vault Preparation:**
   - Create 100-note test vault with planted issues
   - Verify frontmatter metadata present on all notes
   - Ensure external links point to valid/invalid URLs as specified

3. **Agent Activation:**
   - Activate Quality Auditor Agent via `/bmad-2b:quality-auditor-agent`
   - Verify agent loads successfully

### Test Execution Order

**Phase 1: Individual Audit Dimension Tests** (Tests 1-7)

- Run each audit dimension test independently
- Verify results against expected outcomes
- Record pass/fail for each test case

**Phase 2: Report Generation Tests** (Tests 8)

- Run full audit to generate comprehensive report
- Validate health score calculation
- Verify action item prioritization

**Phase 3: Command Tests** (Tests 9)

- Test all 13 commands
- Verify parameters work correctly
- Test mode toggles (*progressive, *yolo)

**Phase 4: Error and Edge Cases** (Tests 10-11)

- Test error scenarios
- Test progressive mode
- Validate graceful degradation

**Phase 5: Final Validation** (Tests 12-13)

- Run audit coverage checklist
- Validate all acceptance criteria met

### Success Criteria

**Overall Pass:** >= 90% of test cases pass

**Critical Test Cases (Must Pass):**

- All 7 audit dimension core tests (1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1)
- All security tests (2.4, 2.5, 2.6)
- Report generation (8.1)
- Health score calculation (8.2)
- All 13 commands functional (9.1-9.7)
- All 11 acceptance criteria validated (AC1-AC11)

**Performance Benchmarks (Must Meet):**

- Temporal freshness: < 5s for 100 notes ✓
- Link validation: < 2s per URL ✓
- Citation validation: < 3s for 100 notes ✓
- Orphan detection: < 5s for 100 notes ✓
- Atomicity audit: < 10s for 20-note sample ✓
- Duplicate detection: < 10s for 100 notes ✓
- Metadata audit: < 3s for 100 notes ✓

---

## Test Reporting

### Test Results Template

```yaml
test_execution_report:
  test_plan_version: 1.0
  execution_date: 2025-11-06
  tester: [Name]
  environment: Claude Desktop / Cursor
  test_vault: quality-auditor-test-data

  summary:
    total_test_cases: 70
    passed: [count]
    failed: [count]
    skipped: [count]
    pass_rate: [percentage]

  critical_tests:
    all_passed: true/false
    failures: []

  performance_benchmarks:
    all_met: true/false
    failures: []

  acceptance_criteria:
    ac1_passed: true/false
    ac2_passed: true/false
    # ... AC3-AC11
    all_passed: true/false

  issues_found:
    - { test_id: '2.4', severity: 'HIGH', description: 'SSRF bypass detected' }
    # ... other issues

  recommendations:
    - 'Fix SSRF prevention in validate-external-links.md'
    # ... other recommendations

  verdict: PASS / FAIL
  notes: |
    Additional observations and comments
```

---

## Test Maintenance

This test plan should be updated when:

- New audit dimensions added to agent
- New commands implemented
- Performance targets adjusted
- Security measures enhanced
- Acceptance criteria modified

**Test Plan Owner:** Dev Agent implementing STORY-006

**Last Updated:** 2025-11-06

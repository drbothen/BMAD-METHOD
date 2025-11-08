# Audit Test Vault

This test vault is designed to validate the three review tasks:

- `review-audit-temporal-freshness.md`
- `review-validate-external-links.md`
- `review-generate-audit-report.md`

## Test Data Specification

The test vault should contain **1000 notes** with the following characteristics:

### Temporal Freshness Test Data (200 stale notes)

- **Fresh notes (800)**: `last_updated` within 180 days
- **Stale notes (200)**: `last_updated` >180 days ago
  - 50 notes: 180-365 days old (medium/high severity)
  - 100 notes: 365-730 days old (critical severity)
  - 50 notes: >730 days old (critical severity)

**Importance Distribution:**

- 20 stale notes with >10 incoming links (CRITICAL priority)
- 50 stale notes with 5-10 incoming links (HIGH priority)
- 80 stale notes with 2-5 incoming links (MEDIUM priority)
- 50 stale notes with 0-1 incoming links (LOW priority)

### External Link Validation Test Data (50 notes with links)

- **Successful links (25)**:
  - `https://example.com` (200 OK)
  - `https://www.iana.org/domains/example` (200 OK)

- **Broken links (20)**:
  - `https://httpstat.us/404` (404 Not Found)
  - `https://httpstat.us/403` (403 Forbidden)
  - `https://httpstat.us/500` (500 Internal Server Error)

- **Redirect links (10)**:
  - `https://httpstat.us/301` (301 Moved Permanently)
  - `https://httpstat.us/302` (302 Found)

- **Timeout links (5)**:
  - `https://httpstat.us/200?sleep=10000` (10s delay, times out at 5s)

- **Blocked links (SSRF prevention - 10)**:
  - `http://localhost:8080/api`
  - `http://192.168.1.1/admin`
  - `http://127.0.0.1/internal`
  - `http://10.0.0.1/private`

### Orphaned Notes (10 notes)

- Notes with no incoming links
- Notes with no outgoing links
- Isolated from knowledge graph

### Link Graph Structure

**Hub notes (high incoming link count):**

- `notes/core-concepts/methodology.md` (15 incoming links)
- `notes/core-concepts/framework.md` (12 incoming links)
- `notes/core-concepts/workflow.md` (10 incoming links)

**Connected notes (moderate links):**

- 200 notes with 2-5 incoming links

**Isolated notes:**

- 10 orphaned notes (0 incoming/outgoing links)

## Directory Structure

```
audit-test-vault/
├── notes/
│   ├── core-concepts/     # Critical knowledge hubs
│   ├── research/           # Notes with external links
│   ├── projects/           # Active project notes
│   └── archive/            # Old, stale notes
├── archive/                # Archived content
├── reports/                # Generated audit reports
└── README.md               # This file
```

## Sample Notes

### Fresh Note (notes/projects/active-project.md)

```markdown
---
title: Active Project
created: 2025-10-01
last_updated: 2025-11-01
tags: [project, active]
---

# Active Project

This is an active project note updated recently.

Links:

- [[methodology]]
- [[framework]]
```

### Stale Critical Note (notes/core-concepts/methodology.md)

```markdown
---
title: Methodology Framework
created: 2023-01-15
last_updated: 2024-01-15
tags: [core, methodology, critical]
domain_critical: true
---

# Methodology Framework

Core methodology that hasn't been updated in 300+ days.
This is a critical knowledge hub with 15 incoming links.
```

### Note with External Links (notes/research/web-sources.md)

```markdown
---
title: Web Research Sources
created: 2025-05-01
last_updated: 2025-10-15
---

# Web Research Sources

Working links:

- [Example Domain](https://example.com)
- [IANA Example Domain](https://www.iana.org/domains/example)

Broken links:

- [Missing Page](https://httpstat.us/404)
- [Forbidden Resource](https://httpstat.us/403)

Redirects:

- [Moved Permanently](https://httpstat.us/301)

Timeouts:

- [Slow Server](https://httpstat.us/200?sleep=10000)

Security blocked (should not be tested):

- [Local Admin](http://localhost:8080/api)
- [Private Network](http://192.168.1.1/admin)
```

### Orphaned Note (notes/archive/isolated-note.md)

```markdown
---
title: Isolated Note
created: 2024-06-01
last_updated: 2024-06-15
---

# Isolated Note

This note has no incoming or outgoing links.
It's disconnected from the knowledge graph.
```

## Expected Test Results

### Task 1: review-audit-temporal-freshness.md

**Expected Output:**

- `total_notes`: 1000
- `stale_notes`: 200
- `stale_ratio`: 0.20
- `avg_staleness`: ~400 days
- `health_impact`: "medium"

**Top Priority Stale Notes:**

1. `notes/core-concepts/methodology.md` (priority_score: ~65, importance: 15)
2. `notes/core-concepts/framework.md` (priority_score: ~48, importance: 12)
3. `notes/core-concepts/workflow.md` (priority_score: ~40, importance: 10)

### Task 2: review-validate-external-links.md

**Expected Output:**

- `total_links`: 50 (limited by max_links parameter)
- `success_count`: 25 (50%)
- `broken_count`: 20 (40%)
- `redirect_count`: 10 (20%)
- `timeout_count`: 5 (10%)
- `blocked_count`: 10 (SSRF prevention)

**Expected Performance:**

- Execution time: ~12-15 seconds (50 links at 5 req/sec rate limit)

### Task 3: review-generate-audit-report.md

**Expected Output:**

- `health_score`: ~68-72 (Fair)
  - Freshness: 80% → contributes 16 points (20% weight)
  - Links: 50% → contributes 7.5 points (15% weight)
  - Orphans: 99% → contributes 14.85 points (15% weight)
  - Total: ~68-72/100
- `health_interpretation`: "Fair"
- `action_items`: 3-5 prioritized actions
  - HIGH: Fix 20 broken links
  - HIGH: Update 20 critical stale notes
  - MEDIUM: Link 10 orphaned notes

**Report Location:**

- `reports/audit-YYYY-MM-DD-HHMM.md`

## Test Execution

### Manual Testing

To manually test these tasks:

1. **Populate test vault** with 1000 notes matching specification
2. **Run Task 1**: Temporal freshness audit
   ```
   Input: { vault_path: "./audit-test-vault", freshness_threshold_days: 180 }
   ```
3. **Run Task 2**: External link validation
   ```
   Input: { note_paths: null, max_links: 50, rate_limit: 5 }
   ```
4. **Run Task 3**: Generate audit report
   ```
   Input: { audit_results: {freshness, links}, vault_path: "./audit-test-vault" }
   ```

### Automated Testing

Create unit tests using Node.js/Mocha or Jest:

- `tests/unit/test-review-audit-freshness.js`
- `tests/unit/test-review-validate-links.js`
- `tests/unit/test-review-generate-report.js`

See `expansion-packs/bmad-obsidian-2nd-brain/tests/quality-auditor-test-plan.md` for complete test specifications.

## Performance Validation

### Task 1 Performance Targets

- **1000 notes**: < 10 seconds
- **10,000 notes**: < 60 seconds

### Task 2 Performance Targets

- **50 links with rate limiting**: < 15 seconds
  - 50 links / 5 per sec = 10 batches
  - 10 batches × 1 sec wait = 10 seconds
  - Plus ~2-5 seconds for requests = 12-15 seconds total

### Task 3 Performance Targets

- **Report generation**: < 5 seconds
  - Template loading: ~0.2s
  - Health score calculation: ~0.5s
  - Section formatting: ~2s
  - Report creation: ~0.5s

## Security Validation

### SSRF Prevention (Task 2)

Verify these URLs are **blocked** and never sent to network:

- ✓ `http://localhost:*`
- ✓ `http://127.0.0.1/*`
- ✓ `http://192.168.*.*/*`
- ✓ `http://10.*.*.*/*`
- ✓ `http://172.16-31.*.*/*`

### Protocol Validation (Task 2)

Verify these protocols are **blocked**:

- ✓ `javascript:alert('XSS')`
- ✓ `data:text/html,<script>...`
- ✓ `file:///etc/passwd`

### Path Traversal Prevention (All Tasks)

Verify these paths are **blocked**:

- ✓ `/vault/../etc/passwd`
- ✓ `C:\vault\..\Windows\System32`

## Notes

- This test vault specification documents the EXPECTED test data structure
- Actual note generation can be done via script or manually for validation
- Use `httpstat.us` service for testing HTTP status codes and timeouts
- For production testing, use a real Obsidian vault with MCP server configured

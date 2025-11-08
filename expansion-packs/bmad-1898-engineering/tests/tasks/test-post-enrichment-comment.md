# Test Cases: post-enrichment-comment.md

## Test Overview

This document defines test cases for the `post-enrichment-comment.md` task, covering configuration validation, enrichment formatting, JIRA comment posting, error handling, and markdown compatibility.

## Test Environment Setup

### Prerequisites

- Atlassian MCP server configured and authenticated
- JIRA test instance with test ticket
- `config.yaml` properly configured with test values
- Sample enrichment markdown file from Story 1.4

### Test Data Requirements

**Required Test Tickets (to be created by QA/PO):**

- `AOD-TEST-001`: Test ticket for standard enrichment posting
- `AOD-TEST-002`: Test ticket for permission testing
- `AOD-TEST-003`: Test ticket for large content testing

**Required Test Files:**

- `test-enrichment-standard.md`: Standard enrichment (all 12 sections, ~5KB)
- `test-enrichment-minimal.md`: Minimal enrichment (required fields only, ~1KB)
- `test-enrichment-large.md`: Large enrichment (>50KB for truncation testing)
- `test-enrichment-special-chars.md`: Enrichment with special characters, emojis, links

**Note:** Test ticket IDs and test files must be created before story approval.

---

## Test Cases

### TC-001: Valid Configuration Loading

**Objective:** Verify task loads and validates configuration correctly

**Test Data:**

```yaml
jira:
  cloud_id: 'test-cloud-id-12345'
  project_key: 'AOD'
```

**Steps:**

1. Execute `post-enrichment-comment.md` task
2. Verify config file is read
3. Verify required fields are validated

**Expected Result:**

- ✅ Config loads without errors
- ✅ Required fields (cloud_id, project_key) validated
- ✅ Task proceeds to input parameter validation

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-002: Missing Configuration File

**Objective:** Verify graceful handling when config.yaml doesn't exist

**Setup:** Temporarily rename or remove `config.yaml`

**Steps:**

1. Execute `post-enrichment-comment.md` task
2. Observe error message

**Expected Result:**

- ❌ Clear error: "Config file not found at expansion-packs/bmad-1898-engineering/config.yaml"
- ❌ Task halts gracefully
- ✅ No stack traces or technical errors shown

**Cleanup:** Restore `config.yaml`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-003: Missing Required Configuration Field

**Objective:** Verify validation of required config fields

**Setup:** Remove `jira.cloud_id` from config.yaml

**Steps:**

1. Execute `post-enrichment-comment.md` task
2. Observe error message

**Expected Result:**

- ❌ Clear error: "Missing required field: jira.cloud_id"
- ❌ Task halts gracefully

**Cleanup:** Restore `jira.cloud_id`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-004: Invalid Ticket ID Format

**Objective:** Verify ticket ID format validation

**Test Data:**

```yaml
ticket_id: 'invalid-ticket' # Missing project-number format
enrichment_file_path: 'test-enrichment-standard.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Execute task with invalid ticket ID
2. Observe validation error

**Expected Result:**

- ❌ Error: "Invalid ticket ID format. Expected format: PROJECT-123"
- ❌ Task halts

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-005: Enrichment File Not Found

**Objective:** Verify graceful handling when enrichment file doesn't exist

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-001'
enrichment_file_path: 'nonexistent-file.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Execute task with nonexistent file path
2. Observe error message

**Expected Result:**

- ❌ Error: "Enrichment file not found: nonexistent-file.md"
- ❌ Task halts

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-006: Standard Enrichment Posting

**Objective:** Post standard enrichment comment with all sections

**Test Ticket:** AOD-TEST-001

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-001'
enrichment_file_path: 'test-enrichment-standard.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Execute task with standard enrichment file
2. Verify comment posted to JIRA
3. Verify formatting in JIRA web interface

**Expected Result:**

- ✅ Comment posted successfully
- ✅ Success message: "Posted enrichment comment to AOD-TEST-001"
- ✅ JIRA link provided
- ✅ Comment preview displayed (first 200 chars)

**Manual Verification in JIRA:**

- ✅ All 12 sections displayed correctly
- ✅ Emojis render correctly (🔴, ✅, 🎯, etc.)
- ✅ Tables formatted correctly
- ✅ Links are clickable
- ✅ Horizontal separators (---) display correctly
- ✅ Header formatting preserved
- ✅ Footer with agent attribution visible

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-007: Minimal Enrichment Posting

**Objective:** Post minimal enrichment with required fields only

**Test Ticket:** AOD-TEST-001

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-001'
enrichment_file_path: 'test-enrichment-minimal.md'
cve_id: 'CVE-2024-5678'
research_tool: 'search'
research_duration: 3
```

**Steps:**

1. Execute task with minimal enrichment
2. Verify comment posted

**Expected Result:**

- ✅ Comment posted successfully
- ✅ Required sections present (Executive Summary, Severity Metrics, References)
- ✅ Optional sections omitted gracefully

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-008: Large Enrichment Posting

**Objective:** Test posting large enrichment (potential truncation)

**Test Ticket:** AOD-TEST-003

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-003'
enrichment_file_path: 'test-enrichment-large.md' # >50KB file
cve_id: 'CVE-2024-9999'
research_tool: 'deep_research'
research_duration: 15
```

**Steps:**

1. Execute task with large enrichment file
2. Verify warning message about size
3. Verify posting attempt

**Expected Result:**

- ⚠️ Warning: "Enrichment file is {size}KB. JIRA may reject large comments. Proceeding with caution..."
- If JIRA accepts: ✅ Comment posted successfully
- If JIRA rejects: ❌ Error handled, truncation strategy applied, retry successful

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-009: Special Characters and Links

**Objective:** Verify special characters, emojis, and links format correctly

**Test Ticket:** AOD-TEST-001

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-001'
enrichment_file_path: 'test-enrichment-special-chars.md'
cve_id: 'CVE-2024-0001'
research_tool: 'reason'
research_duration: 5
```

**Enrichment File Contains:**

- Multiple URLs (NVD, CISA, vendor advisories)
- Special markdown characters (\*, \_, `, #)
- Emojis in all categories
- Code blocks with vectors (CVSS:3.1/AV:N/AC:L...)
- Nested bullet lists
- Tables with alignment

**Steps:**

1. Execute task
2. Verify all formatting preserved

**Expected Result:**

- ✅ All links clickable in JIRA
- ✅ Emojis render correctly
- ✅ Special characters escaped properly
- ✅ Code blocks formatted correctly
- ✅ Tables aligned correctly

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-010: Permission Denied Error

**Objective:** Verify graceful handling when user lacks comment permissions

**Setup:** Use restricted JIRA user account or test ticket with comment restrictions

**Test Ticket:** AOD-TEST-002 (restricted)

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-002'
enrichment_file_path: 'test-enrichment-standard.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Execute task with restricted ticket
2. Observe error handling

**Expected Result:**

- ❌ Error: "Cannot add comment to AOD-TEST-002. Check JIRA permissions."
- ❌ Action guidance: "Verify the Atlassian MCP server has 'Add Comments' permission for this project."
- ❌ Task halts gracefully

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-011: Comment Too Large Error

**Objective:** Verify truncation strategy when JIRA rejects large comments

**Setup:** Use enrichment file exceeding JIRA's comment size limit (if known)

**Test Ticket:** AOD-TEST-003

**Steps:**

1. Create extremely large enrichment file (>100KB)
2. Execute task
3. Observe truncation handling

**Expected Result:**

- ❌ Initial error: "Comment rejected by JIRA (too large: {size} characters)"
- ⚠️ Action: "Implementing truncation strategy..."
- Truncation steps executed:
  1. Remove Enrichment Metadata section
  2. Truncate References to top 5
  3. Truncate MITRE ATT&CK to tactics only
  4. If still too large, save to local file
- ✅ Retry with truncated content
- ✅ Success: "Posted truncated enrichment comment. Full enrichment saved to: {path}"

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-012: Network Error Handling

**Objective:** Verify graceful handling of network errors

**Setup:** Disconnect network or use offline mode

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-001'
enrichment_file_path: 'test-enrichment-standard.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Disconnect network
2. Execute task
3. Observe error handling

**Expected Result:**

- ❌ Error: "Cannot post comment. Check network connection."
- 💾 Action: "Saving enrichment locally for retry..."
- 💾 Enrichment saved to: `.ai/enrichment-CVE-2024-1234-{timestamp}.md`
- ❌ Task halts with retry guidance

**Cleanup:** Restore network

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-013: Rate Limit Exceeded

**Objective:** Verify exponential backoff retry strategy for rate limits

**Setup:** Trigger JIRA rate limit (requires multiple rapid requests)

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-001'
enrichment_file_path: 'test-enrichment-standard.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Execute task when rate limit is active
2. Observe retry behavior

**Expected Result:**

- ⚠️ Warning: "JIRA API rate limit exceeded. Retrying with exponential backoff..."
- ⏳ Retry attempt 1/3 - waiting 60s
- ⏳ Retry attempt 2/3 - waiting 120s
- ⏳ Retry attempt 3/3 - waiting 240s
- If all fail: ❌ "Rate limit persists after 3 attempts. Enrichment saved to {path}"
- 💾 Local file created

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-014: Invalid Ticket ID (404)

**Objective:** Verify handling of non-existent ticket ID

**Test Data:**

```yaml
ticket_id: 'AOD-99999' # Non-existent ticket
enrichment_file_path: 'test-enrichment-standard.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Execute task with non-existent ticket
2. Observe error

**Expected Result:**

- ❌ Error: "Ticket AOD-99999 not found. Verify ticket ID and try again."
- ❌ Task halts

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-015: Authentication Failure

**Objective:** Verify handling of MCP authentication failures

**Setup:** Use invalid or expired MCP credentials

**Test Data:**

```yaml
ticket_id: 'AOD-TEST-001'
enrichment_file_path: 'test-enrichment-standard.md'
cve_id: 'CVE-2024-1234'
research_tool: 'deep_research'
research_duration: 8
```

**Steps:**

1. Execute task with invalid credentials
2. Observe error

**Expected Result:**

- ❌ Error: "JIRA authentication failed. Check Atlassian MCP configuration."
- ❌ Action: "Verify MCP server credentials are valid and not expired."
- ❌ Task halts

**Cleanup:** Restore valid credentials

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-016: Emoji Rendering Verification

**Objective:** Verify all emoji categories render correctly in JIRA

**Test Ticket:** AOD-TEST-001

**Test Data:** Standard enrichment with all emoji types

**Emoji Categories to Verify:**

**Priority Indicators:**

- 🔴 P1 - Critical
- 🟠 P2 - High
- 🟡 P3 - Medium
- 🔵 P4 - Low
- ⚪ P5 - Info

**Status Indicators:**

- ✅ Patched
- ❌ No patch
- ⚠️ Workaround
- 🚨 Active exploitation
- 🎯 CISA KEV
- 🔓 Public exploit
- 🛡️ Compensating controls

**Severity Indicators:**

- 🔥 Critical
- ⚡ High
- 📊 Medium
- 📉 Low

**Steps:**

1. Post enrichment with all emoji types
2. View comment in JIRA web interface
3. View comment in JIRA mobile app (optional)

**Expected Result:**

- ✅ All emojis render correctly in web interface
- ✅ Emojis display correctly in mobile app (if tested)
- If emojis don't render: Note browser/JIRA version for fallback implementation

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-017: Source Citation Formatting

**Objective:** Verify source citations are properly formatted and grouped

**Test Ticket:** AOD-TEST-001

**Expected Source Grouping:**

**Vulnerability Details:**

- [NIST NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-1234)
- [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**Patches & Advisories:**

- [Vendor Security Advisory](https://vendor.com/security/CVE-2024-1234)

**Exploit Intelligence:**

- [FIRST EPSS](https://www.first.org/epss/)

**Steps:**

1. Post enrichment with multiple sources
2. Verify grouping in JIRA

**Expected Result:**

- ✅ Sources grouped by category
- ✅ All links clickable
- ✅ Links open in new tab/window
- ✅ Link text matches authority type

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-018: Metadata Verification

**Objective:** Verify enrichment metadata is correctly included

**Test Ticket:** AOD-TEST-001

**Expected Metadata:**

```markdown
---

🤖 _Generated by BMAD-1898 Security Analyst Agent v1.0_
_Research Duration: 8 minutes | Perplexity Tool: deep_research_
```

**Steps:**

1. Post enrichment
2. Verify footer metadata

**Expected Result:**

- ✅ Timestamp in ISO 8601 format with timezone
- ✅ Agent version included
- ✅ Research tool specified
- ✅ Research duration displayed
- ✅ Footer formatting preserved

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-019: Table Formatting Verification

**Objective:** Verify markdown tables render correctly in JIRA

**Test Ticket:** AOD-TEST-001

**Expected Tables:**

1. Severity Metrics table (4 rows, 3 columns)
2. Affected Systems table (variable rows, 4 columns)

**Steps:**

1. Post enrichment with tables
2. Verify rendering in JIRA

**Expected Result:**

- ✅ Tables display with proper column alignment
- ✅ Table headers bold
- ✅ Table borders visible
- ✅ Cell content not truncated
- ✅ Tables responsive on mobile (optional)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-020: Comment Verification (Optional)

**Objective:** Verify comment was actually posted by reading ticket again

**Test Ticket:** AOD-TEST-001

**Steps:**

1. Post enrichment comment
2. Request verification
3. Read ticket using `mcp__atlassian__getJiraIssue`
4. Check comments array

**Expected Result:**

- ✅ Comment found in ticket comments
- ✅ Comment content matches posted enrichment
- ✅ Verification message: "Verified: Comment successfully posted to AOD-TEST-001"

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Test Summary Template

**Total Test Cases:** 20

**Passed:** **\_**
**Failed:** **\_**
**Not Run:** **\_**

**Critical Issues Found:**

1.
2.
3.

**Non-Critical Issues Found:**

1.
2.
3.

**Notes:**

- Emoji rendering issues (specify browsers/versions):
- Markdown compatibility issues:
- Performance issues:
- Other observations:

---

## Test Data Files

**To be created by Dev:**

### test-enrichment-standard.md

Standard enrichment with all 12 sections, approximately 5KB, including:

- All emoji types
- Multiple tables
- 10+ source citations
- CVSS vector strings
- MITRE ATT&CK techniques
- All metadata fields

### test-enrichment-minimal.md

Minimal enrichment with required fields only:

- Executive Summary
- Severity Metrics
- References
- Metadata

Approximately 1KB.

### test-enrichment-large.md

Large enrichment for truncation testing:

- Duplicate sections (if needed)
- Extended content in each section
- Many source citations (50+)
- Large tables

Target size: >50KB (or known JIRA limit if available)

### test-enrichment-special-chars.md

Enrichment testing edge cases:

- Special markdown characters: `*`, `_`, `` ` ``, `#`, `[`, `]`, `(`, `)`
- URLs with query parameters
- Nested bullet lists (3+ levels)
- Mixed formatting (bold + italic + code)
- Unicode characters
- All emoji categories

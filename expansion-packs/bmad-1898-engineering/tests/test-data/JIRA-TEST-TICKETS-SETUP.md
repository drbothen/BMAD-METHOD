# JIRA Test Tickets Setup Guide

## Purpose

This guide provides instructions for creating JIRA test tickets required for testing Story 1.5 (JIRA Enrichment Comment). These test tickets are used to validate JIRA comment posting functionality, formatting, permissions, and error handling.

## Required Test Tickets

The test suite requires **3 test tickets** to be created in your JIRA instance:

1. **AOD-TEST-001**: Standard testing (read/write access)
2. **AOD-TEST-002**: Permission testing (restricted access)
3. **AOD-TEST-003**: Large content testing (read/write access)

---

## Prerequisites

Before creating test tickets, ensure:

1. **JIRA Access**: You have permission to create tickets in the test project
2. **Project Key**: Verify your project key (default: `AOD`, adjust if different)
3. **Atlassian MCP**: MCP server is configured and authenticated
4. **Test Data Files**: All 4 test enrichment files created (see `/tests/test-data/` directory)

---

## Creating Test Tickets

### Ticket 1: AOD-TEST-001 (Standard Testing)

**Purpose:** Standard enrichment comment posting with full permissions

**Configuration:**

- **Project:** AOD (or your configured project key)
- **Issue Type:** Task or Bug
- **Summary:** `[TEST] CVE-2024-1234 Security Enrichment - Standard Test`
- **Description:**

  ```
  This is a test ticket for Story 1.5 (JIRA Enrichment Comment) testing.

  Purpose: Validate standard enrichment comment posting functionality

  Test Cases:
  - TC-006: Standard enrichment posting
  - TC-007: Minimal enrichment posting
  - TC-009: Special characters and links
  - TC-016: Emoji rendering verification
  - TC-017: Source citation formatting
  - TC-018: Metadata verification
  - TC-019: Table formatting verification
  - TC-020: Comment verification (optional)

  DO NOT DELETE - This is a persistent test ticket.
  ```

**Priority:** Medium
**Assignee:** Unassigned or assign to QA team
**Labels:** `test`, `automation`, `story-1.5`, `cve-enrichment`

**Permissions:** Ensure the MCP user account has:

- ✅ View Issue
- ✅ Add Comments
- ✅ Edit Issue (for Story 1.6 field updates)

**After Creation:**

1. Note the ticket ID (e.g., `AOD-TEST-001`)
2. Update test file if project key differs from AOD
3. Verify MCP can read the ticket using `mcp__atlassian__getJiraIssue`

---

### Ticket 2: AOD-TEST-002 (Permission Testing)

**Purpose:** Test error handling when comment permissions are denied

**Configuration:**

- **Project:** AOD (or your configured project key)
- **Issue Type:** Task or Bug
- **Summary:** `[TEST] CVE-2024-1234 Security Enrichment - Permission Test`
- **Description:**

  ```
  This is a test ticket for Story 1.5 (JIRA Enrichment Comment) permission testing.

  Purpose: Validate error handling when user lacks comment permissions

  Test Cases:
  - TC-010: Permission denied error handling

  IMPORTANT: Configure this ticket with RESTRICTED comment permissions for the MCP user.

  DO NOT DELETE - This is a persistent test ticket.
  ```

**Priority:** Medium
**Assignee:** Unassigned or assign to QA team
**Labels:** `test`, `automation`, `story-1.5`, `permission-test`

**Permissions (CRITICAL):** Configure restricted permissions:

- ✅ View Issue (MCP user can read)
- ❌ Add Comments (MCP user CANNOT comment) ← Required for TC-010
- ❌ Edit Issue (optional restriction)

**How to Restrict Comment Permissions:**

**Option 1: Issue-Level Security (Recommended)**

1. Go to ticket settings → Security Level
2. Set security level that excludes MCP user from commenting
3. Verify MCP user can still view but cannot comment

**Option 2: Permission Scheme**

1. JIRA Settings → Issues → Permission Schemes
2. Find your test project's permission scheme
3. For "Add Comments" permission, create a condition that excludes MCP user
4. Apply to this specific ticket only (via custom field or filter)

**Option 3: Project Role**

1. Create a "Read-Only" project role
2. Assign MCP test account to this role for AOD-TEST-002 only
3. Ensure role has "Browse Projects" but not "Add Comments"

**Verification:**

1. Attempt to comment as MCP user → Should receive 403 Forbidden
2. Test script should handle error gracefully
3. Expected error message: "Cannot add comment to AOD-TEST-002. Check JIRA permissions."

---

### Ticket 3: AOD-TEST-003 (Large Content Testing)

**Purpose:** Test large enrichment posting and truncation handling

**Configuration:**

- **Project:** AOD (or your configured project key)
- **Issue Type:** Task or Bug
- **Summary:** `[TEST] CVE-2024-9999 Security Enrichment - Large Content Test`
- **Description:**

  ```
  This is a test ticket for Story 1.5 (JIRA Enrichment Comment) large content testing.

  Purpose: Validate large enrichment handling and truncation strategy

  Test Cases:
  - TC-008: Large enrichment posting (>50KB)
  - TC-011: Comment too large error handling

  This ticket will receive very large enrichment comments to test:
  - JIRA comment size limits
  - Truncation strategy
  - Fallback mechanisms
  - Local file saving

  DO NOT DELETE - This is a persistent test ticket.
  Comments may be very long (50KB+) for testing purposes.
  ```

**Priority:** Medium
**Assignee:** Unassigned or assign to QA team
**Labels:** `test`, `automation`, `story-1.5`, `large-content-test`

**Permissions:** Full access for MCP user

- ✅ View Issue
- ✅ Add Comments
- ✅ Edit Issue

**Note:** This ticket may accumulate many large comments during testing. Clean up periodically but do not delete the ticket itself.

---

## Post-Creation Checklist

After creating all three test tickets, verify:

### 1. Ticket IDs Match Test Specifications

Update test file references if your ticket IDs differ:

- File: `/tests/tasks/test-post-enrichment-comment.md`
- Search for: `AOD-TEST-001`, `AOD-TEST-002`, `AOD-TEST-003`
- Replace with actual ticket IDs if different

### 2. MCP Configuration

Verify MCP can access tickets:

```bash
# Test reading AOD-TEST-001
mcp__atlassian__getJiraIssue
  issueKey: "AOD-TEST-001"
  cloudId: "<your-cloud-id>"

# Should return ticket details without errors
```

### 3. Permission Verification

**AOD-TEST-001 & AOD-TEST-003:** Full access confirmed

```bash
# Verify can add comment
mcp__atlassian__addCommentToJiraIssue
  issueKey: "AOD-TEST-001"
  cloudId: "<your-cloud-id>"
  comment: "✅ Test comment - MCP has add comment permission"

# Should succeed
```

**AOD-TEST-002:** Comment permission denied (desired state)

```bash
# Verify CANNOT add comment
mcp__atlassian__addCommentToJiraIssue
  issueKey: "AOD-TEST-002"
  cloudId: "<your-cloud-id>"
  comment: "❌ This should fail with 403 Forbidden"

# Should fail with 403 error
```

### 4. Test Data Files Present

Verify all test enrichment files exist:

- ✅ `/tests/test-data/test-enrichment-standard.md` (~10KB)
- ✅ `/tests/test-data/test-enrichment-minimal.md` (~1-2KB)
- ✅ `/tests/test-data/test-enrichment-large.md` (>50KB)
- ✅ `/tests/test-data/test-enrichment-special-chars.md` (~15KB)

### 5. Update Configuration

If using different project key, update:

**File:** `expansion-packs/bmad-1898-engineering/config.yaml`

```yaml
jira:
  cloud_id: 'YOUR_CLOUD_ID_HERE'
  project_key: 'YOUR_PROJECT_KEY' # Update if not "AOD"
```

---

## Test Execution

Once all tickets are created, you can execute the test suite:

### Manual Test Execution

1. **TC-006: Standard Enrichment Posting**

   ```
   Ticket: AOD-TEST-001
   Test Data: test-enrichment-standard.md
   Expected: ✅ Comment posted successfully with all formatting
   ```

2. **TC-007: Minimal Enrichment Posting**

   ```
   Ticket: AOD-TEST-001
   Test Data: test-enrichment-minimal.md
   Expected: ✅ Comment posted with required fields only
   ```

3. **TC-008: Large Enrichment Posting**

   ```
   Ticket: AOD-TEST-003
   Test Data: test-enrichment-large.md
   Expected: ⚠️ Warning about size, then ✅ posted or truncated
   ```

4. **TC-009: Special Characters**

   ```
   Ticket: AOD-TEST-001
   Test Data: test-enrichment-special-chars.md
   Expected: ✅ All special chars, URLs, and formatting preserved
   ```

5. **TC-010: Permission Denied**
   ```
   Ticket: AOD-TEST-002
   Test Data: test-enrichment-standard.md
   Expected: ❌ 403 error with clear guidance message
   ```

### Automated Test Execution (Future)

For automated integration testing, use these tickets with CI/CD:

```yaml
# .github/workflows/integration-tests.yml
env:
  TEST_TICKET_STANDARD: 'AOD-TEST-001'
  TEST_TICKET_RESTRICTED: 'AOD-TEST-002'
  TEST_TICKET_LARGE: 'AOD-TEST-003'
  JIRA_CLOUD_ID: ${{ secrets.JIRA_CLOUD_ID }}
```

---

## Maintenance

### Cleaning Test Tickets

Periodically clean up test comments to prevent clutter:

1. **AOD-TEST-001**: Keep 5 most recent test comments, delete older ones
2. **AOD-TEST-002**: Delete any comments (shouldn't have any due to permissions)
3. **AOD-TEST-003**: Delete all comments monthly (large content accumulates)

### Ticket Lifecycle

- **DO NOT DELETE** the tickets themselves
- **DO DELETE** old test comments periodically
- **DO VERIFY** permissions remain correct after JIRA upgrades/changes
- **DO UPDATE** this documentation if ticket IDs or requirements change

### Troubleshooting

**Issue:** Cannot create tickets

- **Solution:** Verify you have "Create Issues" permission in the project

**Issue:** MCP cannot access tickets

- **Solution:** Verify cloud_id is correct and MCP is authenticated

**Issue:** Permission test (AOD-TEST-002) allows comments

- **Solution:** Re-apply permission restrictions (see Option 1/2/3 above)

**Issue:** Large comments rejected

- **Solution:** This is expected behavior for TC-011; verify truncation works

---

## Quick Reference

| Ticket ID    | Purpose               | Permissions                | Test Cases                                                     |
| ------------ | --------------------- | -------------------------- | -------------------------------------------------------------- |
| AOD-TEST-001 | Standard testing      | Full (view, comment, edit) | TC-006, TC-007, TC-009, TC-016, TC-017, TC-018, TC-019, TC-020 |
| AOD-TEST-002 | Permission testing    | Limited (view only)        | TC-010                                                         |
| AOD-TEST-003 | Large content testing | Full (view, comment, edit) | TC-008, TC-011                                                 |

**Total Test Cases Using These Tickets:** 11 of 20 test cases

**Remaining Test Cases:** Other test cases (TC-001 through TC-005, TC-012 through TC-015) test configuration validation, input validation, and error scenarios that don't require actual JIRA tickets.

---

## Support

For questions about test ticket setup:

1. Review this documentation
2. Check `/tests/tasks/test-post-enrichment-comment.md` for test specifications
3. Contact QA team or Story 1.5 developer
4. See BMAD-1898 Engineering expansion pack README

# Fact Verification Task

## Purpose

Verify factual claims in security enrichment against authoritative sources using Perplexity MCP.

## When to Use

- User explicitly requests: `*fact-check {ticket-id}`
- Reviewer wants to validate critical claims (CVSS, KEV, Priority)
- Default mode: Verify critical claims only (CVSS, EPSS, KEV, Patch)
- Comprehensive mode: Verify all verifiable claims in enrichment

## Inputs Required

- **Enrichment document path:** JIRA ticket enrichment comment or custom field content
- **CVE ID:** For querying authoritative sources (must match CVE-YYYY-NNNNN pattern)
- **Claims to verify:** Selectable (critical only vs. comprehensive)

## Output Destination

- **Standalone report:** Markdown fact verification report
- **Integrated into review:** Fact Verification Results section of security review report (Story 2.6)

## Prerequisites Check

Before executing fact verification:

1. **Verify Perplexity MCP Available:** Check if `mcp__perplexity__search` tool is available
2. **If Unavailable:**
   - Skip fact verification step
   - Note in review report: "⚠️ Fact verification skipped (Perplexity MCP unavailable)"
   - Recommend manual verification of critical claims
   - Continue with rest of review workflow

## Process

### Step 1: Input Validation & Security Checks

**Security Validation:**

- **CVE ID Format:** Validate CVE-YYYY-NNNNN pattern before proceeding
- **Ticket ID Sanitization:** Sanitize JIRA ticket IDs to prevent injection attacks
- **Enrichment Path Validation:** Verify file paths are within expected project directories
- **Query Parameter Sanitization:** Escape special characters in Perplexity queries

**Validation Rules:**

```
CVE ID: Must match regex ^CVE-\d{4}-\d{4,}$
Ticket ID: Must match project JIRA key pattern
File Path: Must be within project directory, no ../ traversal
Max Query Length: 500 characters per Perplexity query
```

**If validation fails:**

- Log security validation failure
- Skip verification for invalid inputs
- Note in report: "⚠️ Security validation failed for {input}"
- Continue with valid inputs only

### Step 2: Extract Claims from Enrichment

Parse enrichment document and extract factual assertions:

**Critical Claims (Default Mode):**

- **CVSS Base Score:** Numeric score (0.0-10.0)
- **EPSS Score:** Probability score (0.00-1.00)
- **KEV Status:** Listed or Not Listed
- **Patched Version:** Version number

**Additional Claims (Comprehensive Mode):**

- Affected Version Range
- Exploit Status (PoC/Public/Active)
- Vendor Name
- Product Name
- Attack Vector details

**Extraction Format:**

```markdown
Extracted Claims:

- CVSS Base Score: 9.8
- CVSS Severity: Critical
- EPSS Score: 0.85
- EPSS Percentile: 85th
- KEV Status: Not Listed
- Affected Versions: 2.0.0 - 2.5.32
- Patched Version: 2.5.33+
- Exploit Status: Active Exploitation
```

### Step 3: Verify Critical Claims Using Perplexity

Use Perplexity MCP to verify claims against authoritative sources.

**Rate Limiting:**

- Implement 1-second delay between queries
- Maximum 10 queries per session (critical mode)
- Maximum 20 queries per session (comprehensive mode)
- Warn user if comprehensive mode exceeds limits

**Error Handling:**

- **MCP Unavailable:** Skip verification, note in report
- **Query Timeout:** Retry once with 60s timeout, then skip
- **Conflicting Sources:** Document all, prioritize by authority
- **No Data Available:** Note as "⚠️ Unable to verify - information not yet available"

#### CVSS Score Verification

**Query:**

```
What is the official CVSS base score for {cve_id} according to NIST NVD? Provide:
- CVSS Base Score (numeric)
- CVSS Vector String
- CVSS Severity Label (Low/Medium/High/Critical)
Source must be nvd.nist.gov
```

**Tool Call:**

```
mcp__perplexity__search({
  query: [formatted query above],
  force_model: false
})
```

**Expected Response:**

- CVSS Base Score: X.X
- Vector: CVSS:3.1/AV:X/AC:X/PR:X/UI:X/S:X/C:X/I:X/A:X
- Severity: Low|Medium|High|Critical
- Source: https://nvd.nist.gov/vuln/detail/{cve_id}

**Verification Logic:**

```
IF analyst_cvss == nvd_cvss THEN ✅ MATCH
ELSE ❌ MISMATCH (Critical Discrepancy)
  Impact: Priority assessment may be incorrect
  Action: Correct CVSS score, recalculate priority
```

#### EPSS Score Verification

**Query:**

```
What is the current EPSS exploitation probability score for {cve_id} from FIRST.org EPSS? Provide:
- EPSS Score (0.00-1.00)
- EPSS Percentile
- Date of EPSS score
Source must be first.org/epss
```

**Tool Call:**

```
mcp__perplexity__search({
  query: [formatted query above],
  force_model: false
})
```

**Expected Response:**

- EPSS Score: 0.XX
- Percentile: XXth
- Date: YYYY-MM-DD
- Source: https://first.org/epss/cve/{cve_id}

**Verification Logic:**

```
IF analyst_epss == first_epss THEN ✅ MATCH
ELSE IF abs(analyst_epss - first_epss) < 0.01 THEN ✅ MATCH (rounding tolerance)
ELSE ❌ MISMATCH (Significant Discrepancy)
  Impact: Exploitation probability assessment may be incorrect
  Action: Update EPSS score to current value
```

#### KEV Status Verification

**Query:**

```
Is {cve_id} listed on the CISA Known Exploited Vulnerabilities (KEV) catalog? If yes, provide:
- KEV Status (Listed or Not Listed)
- date_added
- due_date
- required_action
Source must be cisa.gov/known-exploited-vulnerabilities-catalog
```

**Tool Call:**

```
mcp__perplexity__search({
  query: [formatted query above],
  force_model: false
})
```

**Expected Response:**

- KEV Status: Listed | Not Listed
- If Listed:
  - date_added: YYYY-MM-DD
  - due_date: YYYY-MM-DD
  - required_action: "Apply vendor patches"
- Source: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Verification Logic:**

```
IF analyst_kev == cisa_kev THEN ✅ MATCH
ELSE ❌ MISMATCH (Significant/Critical Discrepancy)
  IF cisa_kev == "Listed" AND analyst_kev == "Not Listed" THEN
    Impact: Missing critical prioritization factor (elevates to P1/P2)
    Action: Add KEV status, date_added, recalculate priority
  IF cisa_kev == "Not Listed" AND analyst_kev == "Listed" THEN
    Impact: False prioritization (incorrectly elevated)
    Action: Correct KEV status, recalculate priority
```

#### Patch Availability Verification

**Query:**

```
What is the patched version for {cve_id} according to {vendor} security advisory? Provide:
- Affected versions
- Patched version
Source must be official {vendor} security site.
```

**Tool Call:**

```
mcp__perplexity__search({
  query: [formatted query above],
  force_model: false
})
```

**Expected Response:**

- Affected: Product X.X.X - X.X.X
- Patched: X.X.X+
- Source: https://{vendor official security site}

**Verification Logic:**

```
IF analyst_patch == vendor_patch THEN ✅ MATCH
ELSE ❌ MISMATCH (Significant Discrepancy)
  Impact: Incorrect remediation guidance
  Action: Correct patch version to vendor-stated version
```

### Step 4: Compare Claims and Document Discrepancies

**Comparison Result Types:**

- ✅ **MATCH:** Analyst claim matches authoritative source
- ❌ **MISMATCH:** Analyst claim differs from authoritative source
- ⚠️ **UNABLE TO VERIFY:** Cannot verify (source unavailable or conflicting)

**Discrepancy Severity Classification:**

**Critical Discrepancy:**

- CVSS score difference > 2.0 points
- CVSS severity label differs (e.g., High vs Critical)
- KEV status incorrect (Listed vs Not Listed)
- **Impact:** Priority assessment fundamentally wrong
- **Action:** Reject enrichment, require correction

**Significant Discrepancy:**

- CVSS score difference 0.5-2.0 points
- EPSS score difference > 0.10
- Patch version incorrect
- **Impact:** Quality and remediation guidance affected
- **Action:** Mandatory correction before proceeding

**Minor Discrepancy:**

- CVSS score difference < 0.5 points
- EPSS score difference < 0.10
- Formatting differences (9.80 vs 9.8)
- **Impact:** Minimal to none
- **Action:** Optional cleanup

**For Each Mismatch, Document:**

```markdown
### Severity: [Critical|Significant|Minor] Discrepancy: [Claim Name]

**Analyst Claim:** [What analyst stated]
**Authoritative Source:** [What authoritative source says]
**Source URL:** [Authoritative source link]
**Impact:** [How this affects enrichment quality/priority]
**Recommended Action:** [Specific correction needed]
```

### Step 5: Calculate Accuracy Score

**Accuracy Formula:**

```
Accuracy = (Matching Claims / Total Claims Verified) × 100%
```

**Do NOT count "Unable to Verify" as mismatches:**

```
Total Claims Verified = Matches + Mismatches
(Excludes "Unable to Verify" claims)
```

**Accuracy Classifications:**

- **95-100%: Excellent Accuracy**
  - ✅ Approve enrichment - no corrections needed
  - Action: Proceed with review, no fact-checking revisions required

- **85-94%: Good Accuracy**
  - ⚠️ Minor corrections recommended
  - Action: Recommend analyst address discrepancies, but do not block ticket
  - Re-review: Optional, at reviewer's discretion

- **75-84%: Fair Accuracy**
  - ⚠️ Significant corrections required
  - Action: Analyst must address all discrepancies before ticket proceeds
  - Re-review: Mandatory after corrections applied

- **<75%: Poor Accuracy**
  - ❌ Reject enrichment - complete rework required
  - Action: Reject enrichment, request analyst re-research CVE from authoritative sources
  - Re-review: Full re-review required after complete rework

### Step 6: Generate Fact Verification Report

**Report Structure:**

```markdown
# Fact Verification Report

**CVE:** {cve_id}
**Ticket:** {ticket_id}
**Analyst:** {analyst_name}
**Reviewer:** {reviewer_name}
**Verification Date:** {timestamp}
**Verification Mode:** [Critical Claims Only | Comprehensive]

---

## Verification Summary

**Claims Verified:** {total_claims}
**Matches:** {matches} ({match_percentage}%)
**Discrepancies:** {discrepancies} ({discrepancy_percentage}%)
**Unable to Verify:** {unknown}

**Accuracy Score:** {accuracy_score}% ({accuracy_classification})

**Overall Assessment:** {approval_status}
**Recommended Action:** {action_required}

---

## Discrepancies Found

{List all discrepancies with severity, organized by severity level}

### 🔴 Critical Discrepancies

{Critical discrepancies here}

### 🟡 Significant Discrepancies

{Significant discrepancies here}

### 🔵 Minor Discrepancies

{Minor discrepancies here}

---

## Verified Claims (✅ Accurate)

{List all matching claims}

---

## Unable to Verify (⚠️)

{List claims that couldn't be verified with reasons}

---

## Source Authority Hierarchy Used

When conflicting information existed, prioritized:

1. NIST NVD (nvd.nist.gov) - CVSS Scores
2. CISA KEV (cisa.gov) - Exploitation Status
3. FIRST EPSS (first.org/epss) - Exploitation Probability
4. Vendor Security Advisories - Affected/Patched Versions
5. Other Sources - Context only, not factual claims

---

## Next Steps

{Based on accuracy score, provide specific next steps}
```

## Source Authority Hierarchy

When conflicting information exists across sources, prioritize in this order:

**1. NIST NVD (nvd.nist.gov) - CVSS Scores**

- **Authoritative For:** CVSS base score, vector string, severity label
- **When to Use:** Always use NVD as primary source for CVSS scoring
- **When to Deviate:** If NVD data not yet available (very new CVE), document as "Pending NVD"

**2. CISA KEV (cisa.gov) - Exploitation Status**

- **Authoritative For:** Known exploited vulnerabilities, active exploitation confirmation
- **When to Use:** KEV listing is definitive proof of active exploitation
- **When to Deviate:** Never - if CVE is on KEV, it must be marked as exploited

**3. FIRST EPSS (first.org/epss) - Exploitation Probability**

- **Authoritative For:** Exploitation probability score (0.00-1.00), percentile ranking
- **When to Use:** Always use FIRST.org for EPSS scores (updated daily)
- **When to Deviate:** If EPSS not yet available for very new CVE, document as "EPSS pending"

**4. Vendor Security Advisories - Affected/Patched Versions**

- **Authoritative For:** Affected version ranges, patched versions, workarounds
- **When to Use:** Vendor is authoritative for their own product versions
- **When to Deviate:** If vendor advisory conflicts with NVD, document both and note discrepancy

**5. Other Sources (security blogs, forums) - Context Only**

- **Authoritative For:** None - use for context only, not factual claims
- **When to Use:** Background information, attack vectors, exploit development
- **When to Deviate:** Never use as authoritative source for factual claims

**Handling Conflicts:**

- If NVD shows CVSS 9.8 but vendor shows 7.5: Use NVD 9.8, note vendor discrepancy
- If multiple sources conflict: Document all sources, prioritize by hierarchy above
- If source is outdated: Check publication dates, use most recent from highest authority
- If no authoritative source available: Mark claim as "⚠️ Unable to verify" (not discrepancy)

## Error Handling

**Perplexity MCP Unavailable:**

- Skip fact verification entirely
- Note in review: "⚠️ Fact verification skipped (Perplexity MCP unavailable)"
- Recommend manual verification of critical claims
- Continue with rest of review workflow

**Query Timeout:**

- Retry once with 60-second timeout
- If still fails, skip that specific claim
- Note: "⚠️ Unable to verify {claim} - query timeout"
- Continue with remaining claims

**Conflicting Sources:**

- Note discrepancy: "⚠️ Conflicting information across sources"
- Apply source authority hierarchy
- Document all sources and their claims
- Use highest-authority source as correct value

**Information Not Available:**

- Note: "⚠️ Unable to verify - information not yet available (new CVE)"
- Do NOT mark as discrepancy
- Do NOT count against accuracy score
- Recommend re-verification when data available

**Security Validation Failure:**

- Fail safely: Skip verification for invalid inputs
- Do NOT expose internal paths or system info
- Log validation failure for audit
- Note in report: "⚠️ Security validation failed for {input}"

**API/Network Errors:**

- Log error (sanitized, no credentials)
- Skip failed query
- Continue with remaining verifications
- Note in report which claims couldn't be verified due to errors

## Security Considerations

**HTTPS Only:**

- All external API calls must use HTTPS
- Verify certificate validity
- No HTTP fallback allowed

**Request Timeouts:**

- Set maximum 30-second timeout per query
- Maximum 5-minute total execution time for task

**No Credential Exposure:**

- Never log or expose API keys in error messages
- Never log or expose API keys in reports
- Sanitize all error outputs

**Response Validation:**

- Validate response data structure before parsing
- Sanitize all external data before including in markdown reports
- Prevent XSS in generated reports

**Rate Limiting & DoS Prevention:**

- Maximum 1 query/second to each source
- Maximum 10 queries per session (critical mode)
- Maximum 20 queries per session (comprehensive mode)
- Warn user if comprehensive mode exceeds limits

**Audit Logging:**

- Log all fact verification queries (sanitized)
- Log all verification results
- Log security validation failures
- Include timestamp and user context

## Example Usage

**Critical Mode (Default):**

```
Input: CVE-2024-1234, ticket VULN-123, enrichment document
Verifies: CVSS, EPSS, KEV, Patch (4 queries)
Output: Fact verification report with accuracy score
Time: ~10-15 seconds (with 1s delays between queries)
```

**Comprehensive Mode:**

```
Input: CVE-2024-1234, ticket VULN-123, enrichment document, comprehensive=true
Verifies: All verifiable claims (up to 20 queries)
Output: Detailed fact verification report with all claims checked
Time: ~30-60 seconds (with 1s delays between queries)
Warning: User notified if >20 queries required
```

## Integration with Review Workflow

This task is called by Security Reviewer agent as part of the review workflow:

```
Security Reviewer Agent Workflow:
1. *review-enrichment → Run 8 quality checklists (Story 2.2)
2. *fact-check (OPTIONAL) → Verify critical claims (Story 2.5) ← THIS TASK
3. *detect-bias → Detect cognitive biases (Story 2.4)
4. *generate-report → Create review report (Story 2.6)
```

**When to Execute:**

- User explicitly requests: `*fact-check {ticket-id}`
- Reviewer suspects accuracy issues in enrichment
- High-priority tickets (P1/P2) for extra validation
- Optional for all other tickets

**Integration Points:**

- Input: Enrichment document from JIRA ticket
- Output: Standalone report or integrated into security review report
- Next Step: Continue to bias detection or final report generation

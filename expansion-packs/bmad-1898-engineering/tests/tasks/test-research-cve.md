# Test Cases: research-cve.md

## Test Overview
This document defines test cases for the `research-cve.md` task, covering CVE validation, Perplexity tool selection, intelligence extraction, source validation, and error handling.

## Test Environment Setup

### Prerequisites
- Perplexity MCP server available (default in Claude Code)
- Internet connectivity for AI-assisted research
- Mock framework for unit testing (no actual Perplexity calls)
- Real CVE identifiers documented for integration testing

### Test Data Requirements

**Real CVEs for Integration Testing:**
- **CVE-2021-44228** (Log4Shell) - Critical severity, comprehensive data
- **CVE-2023-44487** (HTTP/2 Rapid Reset) - High severity, well-documented
- **CVE-2024-52301** - Recent Critical vulnerability
- **CVE-2020-5902** (F5 BIG-IP) - Medium severity with KEV listing

**Mock Data for Unit Testing:**
- Synthetic Perplexity responses for all severity levels
- Edge case mocks: missing EPSS, no KEV, no exploits
- Error mocks: timeout, invalid CVE, conflicting data

---

## Unit Tests (Mocked Perplexity Responses)

### TC-001: Valid CVE Identifier Format
**Objective:** Verify CVE identifier validation accepts valid formats

**Test Data:**
- `CVE-2024-1234` (valid)
- `CVE-2023-44487` (valid)
- `cve-2021-44228` (valid, lowercase)
- `CVE-2020-123456789` (valid, 7-digit ID)

**Steps:**
1. Execute `research-cve.md` task
2. Provide each CVE identifier
3. Verify validation passes

**Expected Result:**
- ✅ All valid formats accepted
- ✅ Lowercase normalized to uppercase
- ✅ Task proceeds to research query construction

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-002: Invalid CVE Identifier Format
**Objective:** Verify CVE validation rejects invalid formats

**Test Data:**
- `2024-1234` (missing CVE prefix)
- `CVE-24-1234` (2-digit year)
- `CVE-2024-123` (3-digit ID, minimum is 4)
- `CVE-2024` (no ID number)
- `CVE-ABCD-1234` (non-numeric year)

**Steps:**
1. Execute task
2. Provide invalid CVE identifier
3. Observe error message

**Expected Result:**
- ❌ Error: "Invalid CVE format. Expected: CVE-YYYY-NNNNN"
- ❌ Re-prompt for valid identifier
- ✅ Max 3 attempts before halt

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-003: Mock - Critical Severity Tool Selection
**Objective:** Verify `deep_research` tool selected for Critical CVEs

**Mock Setup:**
Initial `mcp__perplexity__reason` response:
```yaml
cvss_score: 9.8
severity: Critical
cve_id: CVE-MOCK-CRITICAL
```

**Steps:**
1. Execute task with mocked responses
2. Verify initial research uses `reason`
3. Verify CVSS extraction identifies Critical severity
4. Verify tool switches to `deep_research`

**Expected Result:**
- ✅ Initial tool: `mcp__perplexity__reason`
- ✅ CVSS 9.8 detected → Critical severity
- ✅ Display: "⚠️ Critical vulnerability detected (CVSS 9.8). Initiating deep research..."
- ✅ Tool switched to: `mcp__perplexity__deep_research`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-004: Mock - High Severity Tool Selection
**Objective:** Verify `reason` tool used for High CVEs

**Mock Setup:**
Initial `mcp__perplexity__reason` response:
```yaml
cvss_score: 8.1
severity: High
```

**Expected Result:**
- ✅ Initial tool: `mcp__perplexity__reason`
- ✅ CVSS 8.1 → High severity
- ✅ Tool remains: `mcp__perplexity__reason` (no switch)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-005: Mock - Medium Severity Tool Selection
**Objective:** Verify `search` tool selected for Medium CVEs

**Mock Setup:**
Initial `mcp__perplexity__reason` response:
```yaml
cvss_score: 5.5
severity: Medium
```

**Expected Result:**
- ✅ Initial tool: `mcp__perplexity__reason`
- ✅ CVSS 5.5 → Medium severity
- ✅ Tool switches to: `mcp__perplexity__search`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-006: Mock - Query Template Construction
**Objective:** Verify comprehensive query includes all required fields

**Expected Query Elements:**
1. ✅ CVSS Base Score and Vector String
2. ✅ EPSS Exploitation Probability Score
3. ✅ CISA KEV Catalog Status
4. ✅ Affected Product Versions
5. ✅ Patched Versions
6. ✅ Exploit Availability
7. ✅ MITRE ATT&CK Tactics and Techniques
8. ✅ Vendor Security Advisory Links
9. ✅ Technical Description
10. ✅ Authoritative sources required

**Verification:**
- Parse constructed query string
- Confirm all 10 intelligence fields mentioned
- Confirm authoritative sources list included

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-007: Mock - Complete Intelligence Extraction
**Objective:** Extract all fields from mock Perplexity response

**Mock Response Data:**
```yaml
cve_id: CVE-MOCK-COMPLETE
cvss:
  score: 9.8
  vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
  severity: Critical
epss:
  score: 0.85
  percentile: 97.5
kev:
  status: Listed
  date_added: 2024-11-01
affected_products:
  - product: Apache Struts 2
    vendor: Apache
    affected_versions: 2.0.0 - 2.5.32
patches:
  available: true
  versions: [2.5.33+]
exploit_status:
  poc_available: true
  active_exploitation: true
attack_mapping:
  tactics: [Initial Access]
  techniques:
    - id: T1190
      name: Exploit Public-Facing Application
```

**Expected Result:**
- ✅ All fields parsed correctly
- ✅ Data types validated (numbers, booleans, strings, arrays)
- ✅ CVSS score range validated (0.0-10.0)
- ✅ EPSS score range validated (0.0-1.0)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-008: Mock - Missing EPSS Score
**Objective:** Handle missing EPSS data gracefully

**Mock Response:** Complete data except EPSS field missing

**Expected Result:**
- ⚠️ Warning: "EPSS score not available for CVE-MOCK-NO-EPSS"
- ✅ EPSS field set to `null` in output
- ✅ Research continues with other data
- ✅ Warning included in warnings array

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-009: Mock - Not in KEV Catalog
**Objective:** Verify KEV status "Not Listed" handled correctly

**Mock Response:**
```yaml
kev:
  status: Not Listed
```

**Expected Result:**
- ✅ KEV status: "Not Listed"
- ✅ No date_added or due_date fields
- ✅ No warnings generated (not an error)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-010: Mock - No Patch Available
**Objective:** Handle vulnerabilities without patches

**Mock Response:**
```yaml
patches:
  available: false
  versions: []
  advisory_url: null
```

**Expected Result:**
- ⚠️ Flag: "No patch available for CVE-MOCK-NO-PATCH"
- ✅ Patch availability: false
- ✅ Check for workarounds mentioned

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-011: Mock - No ATT&CK Mapping
**Objective:** Handle CVEs without ATT&CK mapping

**Mock Response:**
```yaml
attack_mapping: null
```

**Expected Result:**
- ⚠️ Flag: "MITRE ATT&CK mapping not available"
- ✅ Attempt technique inference from vulnerability type
- ✅ Mark inferred techniques as "INFERRED"

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-012: Mock - Authoritative Source Validation
**Objective:** Verify trusted sources accepted

**Mock Response Sources:**
```yaml
sources:
  - url: https://nvd.nist.gov/vuln/detail/CVE-2024-1234
    type: NVD
  - url: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
    type: CISA KEV
  - url: https://www.first.org/epss/
    type: FIRST EPSS
  - url: https://security.apache.org/CVE-2024-1234
    type: Vendor Advisory
```

**Expected Result:**
- ✅ All sources validated as authoritative
- ✅ No warnings generated
- ✅ Sources included in output

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-013: Mock - Untrusted Source Detection
**Objective:** Flag non-authoritative sources

**Mock Response Sources:**
```yaml
sources:
  - url: https://nvd.nist.gov/vuln/detail/CVE-2024-1234
    type: NVD
  - url: https://www.techcrunch.com/2024/article
    type: News Article
  - url: https://twitter.com/security_researcher/status/123
    type: Social Media
```

**Expected Result:**
- ✅ NVD accepted
- ⚠️ Warning: "Information from untrusted source: techcrunch.com"
- ⚠️ Warning: "Information from untrusted source: twitter.com"
- ✅ Untrusted sources flagged but not removed

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-014: Mock - CVSS Score Conflict
**Objective:** Handle conflicting CVSS scores from different sources

**Mock Response:**
```
Conflicting CVSS scores detected:
- NVD: 9.8 (Critical)
- Vendor Advisory: 8.1 (High)
```

**Expected Result:**
- ⚠️ Warning: "CVSS score conflict detected"
- ✅ Display both scores and sources
- ✅ Resolution: Use NVD score (9.8)
- ✅ Document discrepancy in warnings

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-015: Mock - Hallucination Detection (Invalid EPSS)
**Objective:** Detect hallucinated EPSS score exceeding valid range

**Mock Response:**
```yaml
epss:
  score: 1.5  # Invalid: exceeds 1.0 max
```

**Expected Result:**
- ⚠️ Flag: "UNVERIFIED INFORMATION: EPSS score 1.5 exceeds valid range 0.0-1.0"
- ✅ Set EPSS to `null`
- ✅ Mark for manual verification

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-016: Mock - Hallucination Detection (Invalid T-Number)
**Objective:** Detect fabricated ATT&CK technique numbers

**Mock Response:**
```yaml
attack_mapping:
  techniques:
    - id: T9999  # Invalid technique number
      name: Fake Technique
```

**Expected Result:**
- ⚠️ Flag: "UNVERIFIED: ATT&CK Technique T9999 (invalid)"
- ✅ Exclude invalid technique from output
- ✅ Suggest manual verification

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Error Handling Tests (Mocked Failures)

### TC-017: Mock - Perplexity Timeout (deep_research)
**Objective:** Handle timeout and fallback to faster tool

**Mock Setup:**
- `mcp__perplexity__deep_research` → timeout error
- Fallback to `mcp__perplexity__reason` → success

**Expected Result:**
- ⚠️ Display: "Perplexity research timed out. Retrying with simpler query..."
- ✅ Simplify query (reduce requested fields)
- ✅ Fallback: `deep_research` → `reason`
- ✅ Retry succeeds with `reason`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-018: Mock - All Tools Timeout
**Objective:** Handle complete Perplexity failure

**Mock Setup:**
- `reason` → timeout
- `search` → timeout
- All retries exhausted

**Expected Result:**
- ❌ Display: "Automated research failed for CVE-2024-1234"
- ✅ Offer manual research option
- ✅ Max 2 retries per tool
- ✅ Graceful degradation

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-019: Mock - CVE Not Found
**Objective:** Handle invalid/non-existent CVE identifier

**Mock Setup:**
Perplexity response indicates CVE not found in databases

**Expected Result:**
- ❌ Display: "CVE-2024-9999 not found in vulnerability databases"
- ⚠️ Check if reserved but unpublished
- ✅ Offer options:
  1. Re-enter CVE ID
  2. Research anyway (limited info)
  3. Exit task

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-020: Mock - Incomplete CVE Data (Pre-disclosure)
**Objective:** Handle embargoed or minimal CVE information

**Mock Response:**
```yaml
cve_id: CVE-2024-RESERVED
cvss: null
epss: null
description: "Reserved CVE - Details embargoed"
```

**Expected Result:**
- ⚠️ Warning: "INCOMPLETE CVE DATA for CVE-2024-RESERVED"
- ✅ List missing information
- ✅ Return partial data with `null` values
- ✅ Flag: `incomplete_data: true`

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Integration Tests (Real CVE Identifiers)

### TC-101: Integration - CVE-2021-44228 (Log4Shell)
**Objective:** Test with real Critical severity CVE

**Test Data:** CVE-2021-44228 (Log4Shell)

**Prerequisites:**
- Perplexity MCP available
- Internet connectivity

**Steps:**
1. Execute `research-cve.md` task
2. Provide CVE-2021-44228
3. Verify real Perplexity research execution

**Expected Result:**
- ✅ CVSS score: 10.0 (Critical)
- ✅ Tool used: `mcp__perplexity__deep_research`
- ✅ KEV status: Listed
- ✅ Exploit available: true
- ✅ ATT&CK mapping present
- ✅ All sources authoritative (NVD, CISA, vendor)
- ✅ Complete structured data returned

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

**Notes:**
- Log actual CVSS, EPSS, KEV values found
- Verify against known correct data

---

### TC-102: Integration - CVE-2023-44487 (HTTP/2 Rapid Reset)
**Objective:** Test with real High severity CVE

**Test Data:** CVE-2023-44487

**Expected Result:**
- ✅ CVSS score: 7.x (High)
- ✅ Tool used: `mcp__perplexity__reason`
- ✅ Research completes in 30-60 seconds
- ✅ KEV status: Listed
- ✅ Multiple vendor advisories cited

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-103: Integration - CVE-2024-52301 (Recent Critical)
**Objective:** Test with recent Critical CVE

**Test Data:** CVE-2024-52301

**Expected Result:**
- ✅ CVSS: Critical severity
- ✅ Tool: `deep_research`
- ✅ Recent data (2024)
- ✅ All intelligence fields populated or flagged as missing

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-104: Integration - CVE-2020-5902 (Medium with KEV)
**Objective:** Test Medium severity CVE that is KEV-listed

**Test Data:** CVE-2020-5902 (F5 BIG-IP RCE)

**Expected Result:**
- ✅ CVSS: Medium severity
- ✅ Tool used: `mcp__perplexity__search`
- ✅ KEV status: Listed (despite medium CVSS)
- ✅ F5 vendor advisory cited
- ✅ Research completes in 10-20 seconds

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-105: Integration - Source Citation Quality
**Objective:** Verify all real research cites authoritative sources

**Test Data:** Any real CVE from TC-101 to TC-104

**Validation:**
- ✅ All CVSS data from nvd.nist.gov
- ✅ KEV data from cisa.gov
- ✅ EPSS data from first.org
- ✅ ATT&CK from attack.mitre.org
- ✅ Vendor advisories from official security sites
- ✅ No blog posts or news sites as primary sources

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Data Structure Validation Tests

### TC-201: Output Structure Completeness
**Objective:** Verify returned YAML structure has all required fields

**Test Data:** Any successful research (mocked or real)

**Expected YAML Structure:**
```yaml
cve_id: "{string}"
cvss:
  score: {number|null}
  vector: "{string|null}"
  severity: "{string|null}"
epss:
  score: {number|null}
  percentile: {number|null}
kev:
  status: "{Listed|Not Listed}"
affected_products: [{object}]
patches:
  available: {boolean}
  versions: [string]
exploit_status:
  poc_available: {boolean}
  active_exploitation: {boolean}
attack_mapping:
  tactics: [string]
  techniques: [{object}]
sources: [{object}]
warnings: [string]
metadata:
  research_tool_used: "{string}"
  research_timestamp: "{ISO-8601}"
```

**Validation:**
- ✅ All required fields present
- ✅ Data types correct
- ✅ No undefined or missing keys (nulls acceptable)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-202: CVSS Vector String Format
**Objective:** Validate CVSS vector string format

**Expected Format:** `CVSS:3.1/AV:{X}/AC:{X}/PR:{X}/UI:{X}/S:{X}/C:{X}/I:{X}/A:{X}`

**Validation:**
- ✅ Starts with "CVSS:3.1/" or "CVSS:3.0/"
- ✅ Contains all required metrics
- ✅ Valid metric values (AV: N/A/L/P, etc.)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-203: EPSS Score Range Validation
**Objective:** Verify EPSS scores within valid range

**Valid Range:** 0.0 to 1.0 (or 0% to 100%)

**Validation:**
- ✅ EPSS score ≥ 0.0
- ✅ EPSS score ≤ 1.0
- ✅ Percentile: 0-100

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-204: Timestamp Format Validation
**Objective:** Verify ISO-8601 timestamp format

**Expected Format:** `YYYY-MM-DDTHH:MM:SSZ`

**Validation:**
- ✅ research_timestamp is valid ISO-8601
- ✅ KEV date_added is valid date
- ✅ Chronologically valid (not future dates)

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Security Tests

### TC-301: No Exploit Code Execution
**Objective:** Verify task does not execute exploit code

**Validation:**
- ✅ Task only performs research (read-only)
- ✅ No shell commands executed
- ✅ No file writes outside of structured data return
- ✅ No network connections except Perplexity MCP

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

### TC-302: No Credential Exposure
**Objective:** Verify no sensitive data in logs/outputs

**Validation:**
- ✅ No API keys in error messages
- ✅ No internal system details in queries
- ✅ CVE IDs are public (safe to display)
- ✅ No stack traces exposed to user

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Performance Tests

### TC-401: Tool Performance Expectations
**Objective:** Verify Perplexity tool response times

**Expected Response Times:**
- `search`: 10-20 seconds
- `reason`: 30-60 seconds
- `deep_research`: 2-5 minutes

**Validation:**
- ✅ Actual times within expected ranges
- ✅ No unnecessary delays
- ✅ User notified for long operations

**Status:** ⬜ Not Run | ⬜ Pass | ⬜ Fail

---

## Test Summary

| Test Case | Category | Status | Notes |
|-----------|----------|--------|-------|
| TC-001 | Validation | ⬜ | Valid CVE formats |
| TC-002 | Validation | ⬜ | Invalid CVE formats |
| TC-003 | Tool Selection | ⬜ | Critical → deep_research |
| TC-004 | Tool Selection | ⬜ | High → reason |
| TC-005 | Tool Selection | ⬜ | Medium → search |
| TC-006 | Query | ⬜ | Query template completeness |
| TC-007 | Parsing | ⬜ | Complete intelligence extraction |
| TC-008 | Parsing | ⬜ | Missing EPSS |
| TC-009 | Parsing | ⬜ | Not in KEV |
| TC-010 | Parsing | ⬜ | No patch available |
| TC-011 | Parsing | ⬜ | No ATT&CK mapping |
| TC-012 | Sources | ⬜ | Authoritative sources |
| TC-013 | Sources | ⬜ | Untrusted sources |
| TC-014 | Conflicts | ⬜ | CVSS conflict |
| TC-015 | Hallucination | ⬜ | Invalid EPSS |
| TC-016 | Hallucination | ⬜ | Invalid T-number |
| TC-017 | Error Handling | ⬜ | Timeout fallback |
| TC-018 | Error Handling | ⬜ | All tools timeout |
| TC-019 | Error Handling | ⬜ | CVE not found |
| TC-020 | Error Handling | ⬜ | Incomplete data |
| TC-101 | Integration | ⬜ | Log4Shell (Critical) |
| TC-102 | Integration | ⬜ | HTTP/2 Rapid Reset (High) |
| TC-103 | Integration | ⬜ | Recent Critical |
| TC-104 | Integration | ⬜ | Medium with KEV |
| TC-105 | Integration | ⬜ | Source quality |
| TC-201 | Data Structure | ⬜ | Output completeness |
| TC-202 | Data Structure | ⬜ | CVSS vector format |
| TC-203 | Data Structure | ⬜ | EPSS range |
| TC-204 | Data Structure | ⬜ | Timestamp format |
| TC-301 | Security | ⬜ | No exploit execution |
| TC-302 | Security | ⬜ | No credential exposure |
| TC-401 | Performance | ⬜ | Tool response times |

**Total:** 32 test cases
**Unit Tests (Mocked):** 20 test cases
**Integration Tests (Real CVEs):** 5 test cases
**Data/Security/Performance:** 7 test cases

**Pass Rate:** __%

## Test Execution Notes

**Tester:** _______________
**Date:** _______________
**Environment:** _______________
**Perplexity MCP Status:** _______________

**Issues Found:**
-

**Recommendations:**
-

## Acceptance Criteria Mapping

- **AC1 (Query construction - CVSS, EPSS, KEV, exploits, patches, ATT&CK):** TC-006, TC-007
- **AC2 (Severity-based tool selection):** TC-003, TC-004, TC-005
- **AC3 (Structured research findings):** TC-007, TC-201, TC-202, TC-203
- **AC4 (Authoritative sources - NVD, CISA, vendor):** TC-012, TC-013, TC-105
- **AC5 (Error handling - timeouts, missing, conflicts):** TC-008, TC-010, TC-014, TC-017, TC-018, TC-019, TC-020

All acceptance criteria covered by test cases.

## Mock Framework Guidelines

**For Unit Tests:**
1. Mock all `mcp__perplexity__*` tool calls
2. Return structured responses matching real Perplexity output format
3. Test query construction without external API dependencies
4. Verify parsing logic with controlled test data

**Mock Response Template:**
```yaml
# Mock response structure for mcp__perplexity__reason
response_text: |
  CVE-2024-1234 Vulnerability Intelligence:

  CVSS Score: 9.8 (Critical)
  CVSS Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

  EPSS Score: 0.85 (97.5th percentile)

  CISA KEV Status: Listed (Added: 2024-11-01, Due: 2024-11-22)

  [Additional intelligence fields...]

  Sources:
  - https://nvd.nist.gov/vuln/detail/CVE-2024-1234
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - https://www.first.org/epss/
```

**Unit tests should NOT:**
- Make real Perplexity API calls
- Require internet connectivity
- Depend on external data sources
- Take longer than 1 second per test

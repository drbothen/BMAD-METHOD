# Test Suite: Fact Verification Task

## Test Framework

- **Type:** Markdown-based test documentation (BMAD pattern)
- **Task Under Test:** `expansion-packs/bmad-1898-engineering/tasks/fact-verify-claims.md`
- **Mocking Strategy:** Mock Perplexity MCP responses for deterministic testing
- **Test Execution:** Manual validation by running task with test scenarios

## Test Data Setup

### Mock Perplexity Responses

For unit tests, use these mock responses to simulate `mcp__perplexity__search` calls:

**Mock NVD CVSS Response (Correct):**

```json
{
  "cvss_base_score": 9.8,
  "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  "cvss_severity": "Critical",
  "source": "https://nvd.nist.gov/vuln/detail/CVE-2024-1234"
}
```

**Mock CISA KEV Response (Listed):**

```json
{
  "kev_status": "Listed",
  "date_added": "2024-11-01",
  "due_date": "2024-11-22",
  "required_action": "Apply vendor patches",
  "source": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"
}
```

**Mock FIRST EPSS Response (Correct):**

```json
{
  "epss_score": 0.85,
  "epss_percentile": "85th",
  "date": "2024-11-08",
  "source": "https://first.org/epss/cve/CVE-2024-1234"
}
```

**Mock Vendor Patch Response (Correct):**

```json
{
  "affected_versions": "Apache Struts 2.0.0 - 2.5.32",
  "patched_version": "2.5.33+",
  "source": "https://struts.apache.org/security/"
}
```

## Test Cases

### Test Case 1: Perfect Accuracy (100%)

**Objective:** Verify task correctly identifies enrichment with all accurate claims

**Test ID:** TC-FACT-001

**Prerequisites:**

- Perplexity MCP available
- Mock responses configured for accurate data

**Test Data:**

```markdown
# Mock Enrichment Document

CVE: CVE-2024-1234
CVSS Base Score: 9.8 (Critical)
EPSS Score: 0.85 (85th percentile)
KEV Status: Listed (date_added: 2024-11-01)
Affected Versions: Apache Struts 2.0.0 - 2.5.32
Patched Version: 2.5.33+
```

**Expected Perplexity Queries:**

1. CVSS verification → Returns: 9.8 (Critical)
2. EPSS verification → Returns: 0.85
3. KEV verification → Returns: Listed
4. Patch verification → Returns: 2.5.33+

**Expected Result:**

- Claims Verified: 4
- Matches: 4 (100%)
- Discrepancies: 0 (0%)
- Accuracy Score: 100% (Excellent)
- Recommended Action: Approve enrichment - no corrections needed

**Pass Criteria:**

- ✅ All 4 claims verified as matching
- ✅ Accuracy score = 100%
- ✅ Accuracy classification = "Excellent"
- ✅ Recommended action = Approve
- ✅ No discrepancies listed in report

---

### Test Case 2: Critical CVSS Discrepancy

**Objective:** Verify task detects critical CVSS score mismatch

**Test ID:** TC-FACT-002

**Prerequisites:**

- Perplexity MCP available
- Mock CVSS response configured with different score

**Test Data:**

```markdown
# Mock Enrichment Document

CVE: CVE-2024-1234
CVSS Base Score: 7.5 (High) ← INCORRECT
EPSS Score: 0.85
KEV Status: Not Listed
Patched Version: 2.5.33+
```

**Expected Perplexity Queries:**

1. CVSS verification → Returns: 9.8 (Critical) ← MISMATCH
2. EPSS verification → Returns: 0.85
3. KEV verification → Returns: Not Listed
4. Patch verification → Returns: 2.5.33+

**Expected Result:**

- Claims Verified: 4
- Matches: 3 (75%)
- Discrepancies: 1 (25%)
- Accuracy Score: 75% (Fair Accuracy)
- Discrepancy Type: Critical
- Discrepancy Details:
  - Analyst Claim: CVSS 7.5 (High)
  - Authoritative Source: CVSS 9.8 (Critical)
  - Impact: Priority assessment based on incorrect CVSS
  - Recommended Action: Correct CVSS score to 9.8, recalculate priority

**Pass Criteria:**

- ✅ CVSS discrepancy detected
- ✅ Discrepancy severity = Critical
- ✅ Accuracy score = 75%
- ✅ Accuracy classification = "Fair Accuracy"
- ✅ Impact notes priority assessment affected
- ✅ Recommended action = Analyst must address discrepancies

---

### Test Case 3: Significant KEV Discrepancy

**Objective:** Verify task detects incorrect KEV status

**Test ID:** TC-FACT-003

**Prerequisites:**

- Perplexity MCP available
- Mock KEV response shows "Listed" but analyst claims "Not Listed"

**Test Data:**

```markdown
# Mock Enrichment Document

CVE: CVE-2024-1234
CVSS Base Score: 9.8
EPSS Score: 0.85
KEV Status: Not Listed ← INCORRECT
Patched Version: 2.5.33+
```

**Expected Perplexity Queries:**

1. CVSS verification → Returns: 9.8
2. EPSS verification → Returns: 0.85
3. KEV verification → Returns: Listed (date_added: 2024-11-01) ← MISMATCH
4. Patch verification → Returns: 2.5.33+

**Expected Result:**

- Claims Verified: 4
- Matches: 3 (75%)
- Discrepancies: 1 (25%)
- Accuracy Score: 75% (Fair Accuracy)
- Discrepancy Type: Significant/Critical
- Discrepancy Details:
  - Analyst Claim: Not Listed
  - Authoritative Source: Listed (date_added: 2024-11-01)
  - Impact: Missing critical prioritization factor (should elevate to P1/P2)
  - Recommended Action: Add KEV status and date_added, recalculate priority

**Pass Criteria:**

- ✅ KEV discrepancy detected
- ✅ Discrepancy severity = Significant or Critical
- ✅ Accuracy score = 75%
- ✅ Impact notes missing prioritization factor
- ✅ Recommended action = Mandatory correction

---

### Test Case 4: Minor Formatting Discrepancy

**Objective:** Verify task handles minor formatting differences correctly

**Test ID:** TC-FACT-004

**Prerequisites:**

- Perplexity MCP available
- Mock CVSS response with different formatting (9.8 vs 9.80)

**Test Data:**

```markdown
# Mock Enrichment Document

CVE: CVE-2024-1234
CVSS Base Score: 9.80 ← Formatting difference only
EPSS Score: 0.85
KEV Status: Not Listed
Patched Version: 2.5.33+
```

**Expected Perplexity Queries:**

1. CVSS verification → Returns: 9.8 (technically same value)
2. EPSS verification → Returns: 0.85
3. KEV verification → Returns: Not Listed
4. Patch verification → Returns: 2.5.33+

**Expected Result:**

- Claims Verified: 4
- Matches: 4 (100%) OR Discrepancies: 1 Minor (depending on numeric comparison)
- If treated as match: Accuracy Score: 100% (Excellent)
- If treated as discrepancy: Discrepancy Type: Minor, Accuracy: 75% (Fair)
- Impact: None (numerically equivalent)

**Pass Criteria:**

- ✅ Numeric comparison handles 9.8 == 9.80
- ✅ Either matches OR classified as Minor discrepancy
- ✅ Impact noted as minimal/none
- ✅ If discrepancy: Recommended action = Optional cleanup

---

### Test Case 5: New CVE with Limited Data

**Objective:** Verify task handles "unable to verify" scenarios correctly

**Test ID:** TC-FACT-005

**Prerequisites:**

- Perplexity MCP available
- Mock EPSS response indicates data not yet available

**Test Data:**

```markdown
# Mock Enrichment Document

CVE: CVE-2024-9999 ← Very recent CVE
CVSS Base Score: 9.8
EPSS Score: 0.25 ← May not be available yet
KEV Status: Not Listed
Patched Version: 1.2.3+
```

**Expected Perplexity Queries:**

1. CVSS verification → Returns: 9.8
2. EPSS verification → Returns: "Data not yet available" ← UNABLE TO VERIFY
3. KEV verification → Returns: Not Listed
4. Patch verification → Returns: 1.2.3+

**Expected Result:**

- Claims Verified: 3 (EPSS excluded from denominator)
- Matches: 3 (100% of verifiable claims)
- Discrepancies: 0
- Unable to Verify: 1 (EPSS)
- Accuracy Score: 100% (Excellent) ← Based only on verifiable claims
- Note: "⚠️ EPSS data pending - verify manually when available"

**Pass Criteria:**

- ✅ EPSS marked as "Unable to Verify"
- ✅ EPSS NOT counted as discrepancy
- ✅ EPSS NOT included in accuracy calculation denominator
- ✅ Accuracy score = 100% (3 matches / 3 verifiable)
- ✅ Report notes data pending, not error
- ✅ Recommended action = Approve (with note to re-verify EPSS later)

---

### Test Case 6: Perplexity MCP Unavailable

**Objective:** Verify task handles MCP unavailability gracefully

**Test ID:** TC-FACT-006

**Prerequisites:**

- Perplexity MCP NOT available (simulated unavailability)

**Test Data:**

```markdown
# Mock Enrichment Document

CVE: CVE-2024-1234
CVSS Base Score: 9.8
EPSS Score: 0.85
KEV Status: Listed
Patched Version: 2.5.33+
```

**Expected Behavior:**

1. Task checks for Perplexity MCP availability
2. Detects MCP unavailable
3. Skips fact verification step
4. Returns graceful skip message

**Expected Result:**

- No Perplexity queries executed
- Fact verification skipped
- Report notes: "⚠️ Fact verification skipped (Perplexity MCP unavailable)"
- Recommended: Manual verification of critical claims
- Workflow: Continues with rest of review

**Pass Criteria:**

- ✅ MCP unavailability detected before queries
- ✅ No attempt to call unavailable MCP
- ✅ Skip message included in output
- ✅ Recommendation for manual verification provided
- ✅ Task does not fail/error
- ✅ Review workflow can continue

---

### Test Case 7: Conflicting Sources

**Objective:** Verify task handles conflicting information correctly

**Test ID:** TC-FACT-007

**Prerequisites:**

- Perplexity MCP available
- Mock response includes conflicting CVSS from NVD vs Vendor

**Test Data:**

```markdown
# Mock Enrichment Document

CVE: CVE-2024-1234
CVSS Base Score: 7.5 ← Matches vendor, not NVD
```

**Expected Perplexity Queries:**

1. CVSS verification → Returns:
   - NVD: 9.8 (Critical)
   - Vendor Advisory: 7.5 (High)
   - Sources conflict

**Expected Behavior:**

1. Detect conflicting sources
2. Apply source authority hierarchy (NVD > Vendor)
3. Use NVD 9.8 as authoritative
4. Document vendor discrepancy in notes

**Expected Result:**

- Authoritative Value: 9.8 (from NVD)
- Analyst Claim: 7.5
- Verdict: ❌ MISMATCH
- Note: "⚠️ Conflicting information: Vendor shows 7.5, NVD shows 9.8. Using NVD as authoritative."
- Discrepancy Details:
  - Both sources documented
  - Authority hierarchy applied
  - Impact: Priority assessment affected

**Pass Criteria:**

- ✅ Conflicting sources detected
- ✅ Source authority hierarchy applied (NVD prioritized)
- ✅ Both sources documented in report
- ✅ Analyst claim compared against highest-authority source (NVD)
- ✅ Discrepancy noted with conflict explanation
- ✅ Recommended action based on authoritative source

---

### Test Case 8: Security Validation Failure

**Objective:** Verify task handles invalid inputs securely

**Test ID:** TC-FACT-008

**Prerequisites:**

- Perplexity MCP available
- Invalid CVE ID format provided

**Test Data:**

```markdown
# Mock Enrichment Document with Invalid CVE ID

CVE: CVE-ABC-123 ← INVALID FORMAT (should be CVE-YYYY-NNNNN)
CVSS Base Score: 9.8
```

**Expected Behavior:**

1. Input validation executed
2. CVE ID fails validation (regex: ^CVE-\d{4}-\d{4,}$)
3. Security validation failure logged
4. Skip verification for invalid CVE
5. Continue with other valid inputs (if any)

**Expected Result:**

- CVE ID validation: FAILED
- Fact verification: SKIPPED for this claim
- Security log: Validation failure recorded
- Report note: "⚠️ Security validation failed for CVE ID: CVE-ABC-123"
- No Perplexity queries executed for invalid CVE
- No internal paths or system info exposed in error

**Pass Criteria:**

- ✅ CVE ID format validation executed
- ✅ Invalid format detected and rejected
- ✅ No query sent to Perplexity with invalid input
- ✅ Security validation failure logged (sanitized)
- ✅ Error message does not expose internal paths/system info
- ✅ Task fails safely (continues or gracefully skips)
- ✅ User notified of validation failure
- ✅ Other valid claims still processed (if present)

---

## Integration Tests (Live Perplexity MCP)

**Note:** Integration tests use real Perplexity MCP and real CVEs. Execute sparingly due to rate limits.

### Integration Test 1: Live CVE Verification

**Test ID:** TC-FACT-INT-001

**Objective:** Verify task works with real Perplexity MCP against a known CVE

**Test CVE:** CVE-2021-44228 (Log4Shell - well-documented, stable data)

**Test Steps:**

1. Create enrichment with known claims about CVE-2021-44228
2. Execute fact verification task with live Perplexity MCP
3. Verify task retrieves accurate data from NVD, CISA, FIRST
4. Compare results against expected public data

**Expected Result:**

- Task successfully queries Perplexity
- Returns accurate CVSS, KEV status, EPSS from authoritative sources
- Report generated correctly
- Rate limiting respected (1s delays observed)

**Pass Criteria:**

- ✅ Real Perplexity queries execute successfully
- ✅ Authoritative sources (NVD, CISA, FIRST) data retrieved
- ✅ Report matches known public data for Log4Shell
- ✅ No rate limit errors
- ✅ Execution completes within expected time

---

## Security Tests

### Security Test 1: Input Sanitization

**Test ID:** TC-FACT-SEC-001

**Objective:** Verify task sanitizes inputs to prevent injection attacks

**Test Inputs:**

- CVE ID: `CVE-2024-1234'; DROP TABLE vulnerabilities;--`
- Ticket ID: `../../../etc/passwd`
- File Path: `/etc/shadow`

**Expected Behavior:**

- CVE ID fails regex validation
- Ticket ID sanitized or rejected
- File path validation rejects paths outside project
- No SQL injection possible
- No path traversal possible

**Pass Criteria:**

- ✅ All malicious inputs rejected or sanitized
- ✅ No queries executed with unsanitized inputs
- ✅ No file system access outside project directory
- ✅ Security validation logs failures

---

### Security Test 2: Error Message Sanitization

**Test ID:** TC-FACT-SEC-002

**Objective:** Verify task does not expose sensitive information in errors

**Test Steps:**

1. Trigger various error conditions (network failure, MCP unavailable, invalid input)
2. Inspect all error messages and logs
3. Verify no sensitive data exposed

**Expected Behavior:**

- No API keys in error messages
- No internal file paths in user-facing errors
- No stack traces exposed to user
- No system information disclosed

**Pass Criteria:**

- ✅ Error messages sanitized
- ✅ No credentials/API keys exposed
- ✅ No internal paths revealed
- ✅ User receives helpful but safe error messages

---

## Test Execution Summary

### Manual Test Execution Checklist

To execute these tests manually:

- [ ] **TC-FACT-001:** Perfect Accuracy
- [ ] **TC-FACT-002:** Critical CVSS Discrepancy
- [ ] **TC-FACT-003:** Significant KEV Discrepancy
- [ ] **TC-FACT-004:** Minor Formatting
- [ ] **TC-FACT-005:** New CVE with Limited Data
- [ ] **TC-FACT-006:** Perplexity MCP Unavailable
- [ ] **TC-FACT-007:** Conflicting Sources
- [ ] **TC-FACT-008:** Security Validation Failure
- [ ] **TC-FACT-INT-001:** Live CVE Verification (rate-limited)
- [ ] **TC-FACT-SEC-001:** Input Sanitization
- [ ] **TC-FACT-SEC-002:** Error Message Sanitization

### Test Results Template

```markdown
## Test Execution Results - [Date]

**Tester:** [Name]
**Environment:** [Dev/Staging/Production]
**Perplexity MCP:** [Available/Mocked/Unavailable]

| Test ID         | Test Name                 | Status  | Notes                                           |
| --------------- | ------------------------- | ------- | ----------------------------------------------- |
| TC-FACT-001     | Perfect Accuracy          | ✅ PASS | Accuracy 100% as expected                       |
| TC-FACT-002     | Critical CVSS Discrepancy | ✅ PASS | Discrepancy detected correctly                  |
| TC-FACT-003     | KEV Discrepancy           | ✅ PASS | Impact documented correctly                     |
| TC-FACT-004     | Minor Formatting          | ✅ PASS | Handled as match                                |
| TC-FACT-005     | Limited Data              | ✅ PASS | "Unable to verify" not counted against accuracy |
| TC-FACT-006     | MCP Unavailable           | ✅ PASS | Graceful skip with recommendation               |
| TC-FACT-007     | Conflicting Sources       | ✅ PASS | NVD prioritized correctly                       |
| TC-FACT-008     | Security Validation       | ✅ PASS | Invalid input rejected safely                   |
| TC-FACT-INT-001 | Live CVE                  | ✅ PASS | Log4Shell data verified correctly               |
| TC-FACT-SEC-001 | Input Sanitization        | ✅ PASS | All injection attempts blocked                  |
| TC-FACT-SEC-002 | Error Sanitization        | ✅ PASS | No sensitive data exposed                       |

**Overall Result:** [PASS/FAIL]
**Issues Found:** [Count]
**Blockers:** [Count]
```

## Notes

- Mock Perplexity responses for unit tests to ensure deterministic results
- Use rate-limited integration tests sparingly with real Perplexity MCP
- Security tests are critical - all must pass before production use
- Test with variety of CVEs: recent, old, KEV-listed, not listed
- Verify task handles edge cases: missing data, conflicting sources, errors

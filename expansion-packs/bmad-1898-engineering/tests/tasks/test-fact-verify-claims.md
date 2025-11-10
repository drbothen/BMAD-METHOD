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

---

# Event Investigation Verification Tests (Story 7.6)

## Test Data Setup - Event Investigation

### Mock Perplexity Responses for Event Verification

**Mock IP Ownership Response (Correct):**

```json
{
  "asn": "AS15169",
  "organization": "Google LLC",
  "country": "United States",
  "source": "WHOIS via RIPEstat"
}
```

**Mock Geolocation Response (Correct):**

```json
{
  "country": "United States",
  "city": "Mountain View",
  "coordinates": "37.4056° N, 122.0775° W",
  "source": "MaxMind GeoIP2"
}
```

**Mock Threat Intelligence Response (Malicious):**

```json
{
  "reputation": "Malicious",
  "associated_with": "Emotet botnet C2 server",
  "first_seen": "2024-10-15",
  "confidence": "High",
  "sources": "ThreatFox, AbusIPDB (127 reports)"
}
```

**Mock Protocol/Port Response (Standard):**

```json
{
  "standard_port": 22,
  "protocol": "SSH",
  "iana_assignment": "Yes",
  "common_usage": "Standard",
  "source": "IANA Port Registry"
}
```

## Event Investigation Test Cases

### Test Case E-1: IP Ownership Verification - Valid Public IP

**Objective:** Verify task correctly verifies IP ownership and ASN

**Test ID:** TC-EVENT-001

**Prerequisites:**

- Perplexity MCP available
- Mock IP ownership response configured

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-001
Claim: "Source IP 8.8.8.8 belongs to Google LLC ASN 15169"
```

**Expected Perplexity Query:**

```
IP address 8.8.8.8 ASN ownership and organization - provide ASN number, organization name, and country. Use authoritative sources like WHOIS, RIPEstat, or IPInfo.
```

**Expected Response:**

- ASN: AS15169
- Organization: Google LLC
- Country: United States
- Source: WHOIS via RIPEstat

**Expected Result:**

- Claim Type: ip_ownership
- Verification Status: ✅ MATCH
- Verified Value: AS15169, Google LLC
- Source: WHOIS via RIPEstat
- Notes: Claim is accurate

**Pass Criteria:**

- ✅ IP ownership claim verified successfully
- ✅ ASN matches (AS15169)
- ✅ Organization matches (Google LLC)
- ✅ Status = MATCH
- ✅ Source documented

---

### Test Case E-2: IP Ownership Verification - Private IP

**Objective:** Verify task handles private IP addresses correctly

**Test ID:** TC-EVENT-002

**Prerequisites:**

- Perplexity MCP available

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-002
Claim: "Source IP 10.0.0.5 belongs to internal finance network"
```

**Expected Behavior:**

1. Detect IP is private (10.0.0.0/8 range)
2. Skip external verification
3. Mark as "Unable to Verify"

**Expected Result:**

- Claim Type: ip_ownership
- Verification Status: ⚠️ UNABLE TO VERIFY
- Source: N/A - Private IP address
- Notes: Cannot verify private IP ownership via external sources. Requires internal asset database.

**Pass Criteria:**

- ✅ Private IP detected (10.x.x.x)
- ✅ No Perplexity query executed
- ✅ Status = "Unable to Verify"
- ✅ Note explains why verification skipped
- ✅ NOT counted as discrepancy

---

### Test Case E-3: Geolocation Verification - Correct Location

**Objective:** Verify task correctly verifies IP geolocation

**Test ID:** TC-EVENT-003

**Prerequisites:**

- Perplexity MCP available
- Mock geolocation response configured

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-003
Claim: "IP 8.8.8.8 is located in Mountain View, United States"
```

**Expected Perplexity Query:**

```
IP address 8.8.8.8 geolocation country city coordinates - provide country, city, latitude, longitude. Use authoritative sources like MaxMind GeoIP, IP2Location, or ipstack.
```

**Expected Response:**

- Country: United States
- City: Mountain View
- Coordinates: 37.4056° N, 122.0775° W
- Source: MaxMind GeoIP2

**Expected Result:**

- Claim Type: geolocation
- Verification Status: ✅ MATCH
- Verified Value: Mountain View, United States (37.4056° N, 122.0775° W)
- Source: MaxMind GeoIP2 via IPInfo

**Pass Criteria:**

- ✅ Geolocation claim verified successfully
- ✅ Country matches
- ✅ City matches
- ✅ Status = MATCH
- ✅ Coordinates documented

---

### Test Case E-4: Geolocation Verification - Location Mismatch

**Objective:** Verify task detects incorrect geolocation claims

**Test ID:** TC-EVENT-004

**Prerequisites:**

- Perplexity MCP available
- Mock geolocation response shows different location

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-004
Claim: "IP 203.0.113.10 is located in Paris, France"
```

**Expected Perplexity Query:**

```
IP address 203.0.113.10 geolocation country city coordinates - provide country, city, latitude, longitude. Use authoritative sources like MaxMind GeoIP, IP2Location, or ipstack.
```

**Expected Response:**

- Country: Japan
- City: Tokyo
- Coordinates: 35.6762° N, 139.6503° E
- Source: MaxMind GeoIP2

**Expected Result:**

- Claim Type: geolocation
- Verification Status: ❌ MISMATCH (Significant Discrepancy)
- Verified Value: Tokyo, Japan (35.6762° N, 139.6503° E)
- Source: MaxMind GeoIP2 via IPInfo
- Discrepancy: Claimed location (Paris, France) does not match verified location (Tokyo, Japan)
- Recommendation: Correct geolocation claim to Tokyo, Japan

**Pass Criteria:**

- ✅ Geolocation mismatch detected
- ✅ Status = MISMATCH
- ✅ Discrepancy severity = Significant
- ✅ Both locations documented
- ✅ Recommendation provided

---

### Test Case E-5: Threat Intelligence Verification - Malicious IP Confirmed

**Objective:** Verify task correctly verifies threat intelligence claims

**Test ID:** TC-EVENT-005

**Prerequisites:**

- Perplexity MCP available
- Mock threat intel response configured

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-005
Claim: "IP 198.51.100.25 is associated with Emotet botnet"
```

**Expected Perplexity Query:**

```
Threat intelligence for IP 198.51.100.25 - is this IP associated with malicious activity, botnets, or malware campaigns? Check AbusIPDB, ThreatFox, AlienVault OTX, and VirusTotal. Provide specific threat associations if found.
```

**Expected Response:**

- Reputation: Malicious
- Associated with: Emotet botnet C2 server
- First Seen: 2024-10-15
- Confidence: High
- Sources: ThreatFox, AbusIPDB (127 reports)

**Expected Result:**

- Claim Type: threat_intelligence
- Verification Status: ✅ MATCH
- Verified Value: Emotet botnet C2 server, first seen 2024-10-15
- Source: ThreatFox, AbusIPDB (127 reports)
- Confidence: High
- Notes: Multiple threat intel sources confirm association with Emotet campaign

**Pass Criteria:**

- ✅ Threat intel claim verified successfully
- ✅ Status = MATCH
- ✅ Threat association confirmed (Emotet)
- ✅ Confidence level documented
- ✅ Multiple sources cited

---

### Test Case E-6: Threat Intelligence Verification - Clean IP Claimed Malicious

**Objective:** Verify task detects false positive threat claims

**Test ID:** TC-EVENT-006

**Prerequisites:**

- Perplexity MCP available
- Mock threat intel response shows clean IP

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-006
Claim: "IP 8.8.8.8 is associated with malware distribution"
```

**Expected Perplexity Query:**

```
Threat intelligence for IP 8.8.8.8 - is this IP associated with malicious activity, botnets, or malware campaigns? Check AbusIPDB, ThreatFox, AlienVault OTX, and VirusTotal. Provide specific threat associations if found.
```

**Expected Response:**

- Reputation: Clean
- Associated with: Google Public DNS
- Sources: ThreatFox (no reports), AbusIPDB (0 reports)

**Expected Result:**

- Claim Type: threat_intelligence
- Verification Status: ❌ MISMATCH (Significant Discrepancy)
- Verified Value: Clean - Google Public DNS
- Source: ThreatFox, AbusIPDB (0 reports)
- Discrepancy: Analyst claimed malicious but IP is clean (Google Public DNS)
- Impact: False positive threat claim
- Recommendation: Remove or correct threat claim

**Pass Criteria:**

- ✅ False positive detected
- ✅ Status = MISMATCH
- ✅ Discrepancy severity = Significant
- ✅ Impact documented (false positive)
- ✅ Recommendation to remove claim

---

### Test Case E-7: Protocol/Port Validation - Standard Port

**Objective:** Verify task validates standard protocol/port combinations

**Test ID:** TC-EVENT-007

**Prerequisites:**

- Perplexity MCP available

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-007
Claim: "SSH connection on port 22"
```

**Expected Perplexity Query:**

```
Is SSH protocol typically used on port 22? Provide IANA standard port assignment. Note if this is a non-standard or unusual combination.
```

**Expected Response:**

- Standard Port: 22
- Protocol: SSH
- IANA Assignment: Yes
- Common Usage: Standard
- Source: IANA Port Registry

**Expected Result:**

- Claim Type: protocol_port
- Verification Status: ✅ MATCH (Standard)
- Verified Value: SSH standard port is 22 (IANA)
- Source: IANA Port Registry
- Notes: Standard port/protocol combination

**Pass Criteria:**

- ✅ Protocol/port claim verified
- ✅ Status = MATCH
- ✅ Identified as standard combination
- ✅ IANA source cited

---

### Test Case E-8: Protocol/Port Validation - Unusual Port

**Objective:** Verify task flags unusual protocol/port combinations

**Test ID:** TC-EVENT-008

**Prerequisites:**

- Perplexity MCP available

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-008
Claim: "SSH connection on port 8080"
```

**Expected Perplexity Query:**

```
Is SSH protocol typically used on port 8080? Provide IANA standard port assignment. Note if this is a non-standard or unusual combination.
```

**Expected Response:**

- Standard Port: 22
- Protocol: SSH
- Port 8080: Non-standard (typically HTTP alternate)
- IANA Assignment: No
- Common Usage: Unusual
- Source: IANA Port Registry

**Expected Result:**

- Claim Type: protocol_port
- Verification Status: ❌ UNUSUAL COMBINATION
- Verified Value: SSH standard port is 22 (IANA)
- Source: IANA Port Registry
- Notes: Port 8080 is non-standard for SSH. This may indicate evasion or misconfiguration.
- Recommendation: Investigate why SSH is using non-standard port

**Pass Criteria:**

- ✅ Unusual combination detected
- ✅ Status = UNUSUAL
- ✅ Standard port documented (22)
- ✅ Security note provided (evasion/misconfiguration)
- ✅ Recommendation to investigate

---

### Test Case E-9: Historical Pattern Verification - With Atlassian MCP

**Objective:** Verify task validates historical pattern claims when Atlassian MCP is available

**Test ID:** TC-EVENT-009

**Prerequisites:**

- Atlassian MCP available (mcp**atlassian**\*)
- JIRA historical data available

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-009
Claim: "This alert fires daily at 02:00 UTC"
```

**Expected Behavior:**

1. Check for Atlassian MCP availability → AVAILABLE
2. Query JIRA for historical tickets: `summary ~ "Alert-Name-Pattern" AND created >= -30d`
3. Analyze frequency and timing patterns

**Mock JIRA Response:**

- Tickets Found: 15 in last 30 days
- Occurrence Pattern: 2-3 times per week
- Time Pattern: Varying times (not consistent 02:00 UTC)

**Expected Result:**

- Claim Type: historical_pattern
- Verification Status: ❌ MISMATCH
- Verified Value: Alert fires 2-3 times per week at varying times (JIRA query: 15 tickets in last 30 days)
- Source: JIRA historical ticket search
- Discrepancy: Claimed daily pattern does not match actual 2-3x weekly pattern
- Recommendation: Update frequency claim to "2-3 times per week" based on historical data

**Pass Criteria:**

- ✅ Atlassian MCP availability detected
- ✅ JIRA query constructed correctly
- ✅ Frequency mismatch detected
- ✅ Status = MISMATCH
- ✅ Historical data documented
- ✅ Recommendation provided

---

### Test Case E-10: Historical Pattern Verification - Without Atlassian MCP

**Objective:** Verify task gracefully skips historical pattern verification when Atlassian MCP unavailable

**Test ID:** TC-EVENT-010

**Prerequisites:**

- Atlassian MCP NOT available

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-010
Claim: "This alert fires daily at 02:00 UTC"
```

**Expected Behavior:**

1. Check for Atlassian MCP availability → UNAVAILABLE
2. Skip historical pattern verification
3. Note in report

**Expected Result:**

- Claim Type: historical_pattern
- Verification Status: ⚠️ SKIPPED
- Reason: Atlassian MCP unavailable
- Recommendation: Manually verify alert frequency via JIRA or monitoring system

**Pass Criteria:**

- ✅ Atlassian MCP unavailability detected
- ✅ Historical pattern verification skipped
- ✅ Status = SKIPPED
- ✅ Reason documented
- ✅ Manual verification recommended
- ✅ NOT counted as discrepancy

---

### Test Case E-11: Event Verification - Backward Compatibility (CVE Still Works)

**Objective:** Verify extending task for events doesn't break CVE verification

**Test ID:** TC-EVENT-011

**Prerequisites:**

- Perplexity MCP available
- claim_type parameter or CVE ID detection

**Test Data:**

```markdown
# Mock CVE Enrichment Document (Original Format)

CVE: CVE-2024-1234
CVSS Base Score: 9.8
claim_type: cve
```

**Expected Behavior:**

1. Detect claim_type = cve OR presence of CVE ID
2. Route to CVE verification workflow (Step 3-CVE)
3. Execute CVE verification as before Story 7.6

**Expected Result:**

- Verification Type: CVE Verification
- CVE claims verified using existing logic
- Report format: CVE Fact Verification Report
- All TC-FACT-001 through TC-FACT-008 tests still pass

**Pass Criteria:**

- ✅ CVE verification still works after event extension
- ✅ No regression in CVE verification logic
- ✅ Correct routing to Step 3-CVE
- ✅ All existing CVE tests pass

---

### Test Case E-12: Event Verification - Invalid IP Address Format

**Objective:** Verify task handles malformed IP addresses securely

**Test ID:** TC-EVENT-012

**Prerequisites:**

- Perplexity MCP available

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-012
Claim: "Source IP 999.999.999.999 belongs to Acme Corp"
```

**Expected Behavior:**

1. Input validation detects invalid IP format (octets > 255)
2. Security validation failure logged
3. Skip verification for invalid IP
4. Report security validation failure

**Expected Result:**

- IP Address Validation: FAILED
- Verification Status: ⚠️ SECURITY VALIDATION FAILED
- Note: "⚠️ Security validation failed for IP address: 999.999.999.999"
- No Perplexity query executed

**Pass Criteria:**

- ✅ Invalid IP format detected
- ✅ IP validation regex fails (octets 0-255)
- ✅ No Perplexity query with invalid IP
- ✅ Security validation failure logged
- ✅ User notified of validation failure
- ✅ Task continues with other valid claims

---

### Test Case E-13: Event Verification - Rate Limiting Compliance

**Objective:** Verify task respects rate limiting (1 query/second)

**Test ID:** TC-EVENT-013

**Prerequisites:**

- Perplexity MCP available
- Multiple event claims to verify

**Test Data:**

```markdown
# Mock Event Investigation Document

Investigation ID: ALERT-2024-11-09-013
Claims:

- IP 8.8.8.8 ownership
- IP 8.8.8.8 geolocation
- IP 8.8.8.8 threat intel
- IP 1.1.1.1 ownership
- SSH on port 22
```

**Expected Behavior:**

1. Execute 5 Perplexity queries
2. Implement 1-second delay between each query
3. Total execution time ≥ 5 seconds (5 queries + 4 delays)

**Expected Result:**

- Queries Executed: 5
- Delays Observed: 4 (between queries)
- Total Execution Time: ≥ 5 seconds
- Rate Limit Compliance: ✅ YES

**Pass Criteria:**

- ✅ 1-second delay enforced between queries
- ✅ Total execution time ≥ (query_count) seconds
- ✅ No rate limit errors from Perplexity
- ✅ All queries complete successfully

---

## Event Investigation Test Execution Checklist

### Event Verification Tests

- [ ] **TC-EVENT-001:** IP Ownership - Valid Public IP
- [ ] **TC-EVENT-002:** IP Ownership - Private IP (Unable to Verify)
- [ ] **TC-EVENT-003:** Geolocation - Correct Location
- [ ] **TC-EVENT-004:** Geolocation - Location Mismatch
- [ ] **TC-EVENT-005:** Threat Intel - Malicious IP Confirmed
- [ ] **TC-EVENT-006:** Threat Intel - Clean IP Claimed Malicious
- [ ] **TC-EVENT-007:** Protocol/Port - Standard Port
- [ ] **TC-EVENT-008:** Protocol/Port - Unusual Port
- [ ] **TC-EVENT-009:** Historical Pattern - With Atlassian MCP
- [ ] **TC-EVENT-010:** Historical Pattern - Without Atlassian MCP
- [ ] **TC-EVENT-011:** Backward Compatibility - CVE Still Works
- [ ] **TC-EVENT-012:** Invalid IP Address Format
- [ ] **TC-EVENT-013:** Rate Limiting Compliance

### Test Results Template - Event Investigation

```markdown
## Event Investigation Test Execution Results - [Date]

**Tester:** [Name]
**Environment:** [Dev/Staging/Production]
**Perplexity MCP:** [Available/Unavailable]
**Atlassian MCP:** [Available/Unavailable]

| Test ID      | Test Name                          | Status  | Notes                             |
| ------------ | ---------------------------------- | ------- | --------------------------------- |
| TC-EVENT-001 | IP Ownership - Valid Public IP     | ✅ PASS | ASN verified correctly            |
| TC-EVENT-002 | IP Ownership - Private IP          | ✅ PASS | Skipped with proper note          |
| TC-EVENT-003 | Geolocation - Correct              | ✅ PASS | Location matched                  |
| TC-EVENT-004 | Geolocation - Mismatch             | ✅ PASS | Discrepancy detected              |
| TC-EVENT-005 | Threat Intel - Malicious Confirmed | ✅ PASS | Threat association verified       |
| TC-EVENT-006 | Threat Intel - False Positive      | ✅ PASS | False claim detected              |
| TC-EVENT-007 | Protocol/Port - Standard           | ✅ PASS | Standard combination verified     |
| TC-EVENT-008 | Protocol/Port - Unusual            | ✅ PASS | Unusual port flagged              |
| TC-EVENT-009 | Historical - With Atlassian MCP    | ✅ PASS | Frequency mismatch detected       |
| TC-EVENT-010 | Historical - Without Atlassian MCP | ✅ PASS | Skipped gracefully                |
| TC-EVENT-011 | Backward Compatibility - CVE       | ✅ PASS | No regression in CVE verification |
| TC-EVENT-012 | Invalid IP Address                 | ✅ PASS | Invalid IP rejected securely      |
| TC-EVENT-013 | Rate Limiting                      | ✅ PASS | 1s delays enforced                |

**Overall Result:** [PASS/FAIL]
**Event Verification Issues Found:** [Count]
**Blockers:** [Count]
```

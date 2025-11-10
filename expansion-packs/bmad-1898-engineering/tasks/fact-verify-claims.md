# Fact Verification Task

## Purpose

Verify factual claims in security documents against authoritative sources using Perplexity MCP.

**Supported Claim Types:**

- **CVE Verification:** CVSS, EPSS, KEV, Patch versions
- **Event Investigation Verification:** IP ownership, geolocation, threat intelligence, protocol/port validation

## When to Use

**CVE Verification:**

- User explicitly requests: `*fact-check {ticket-id}`
- Reviewer wants to validate critical claims (CVSS, KEV, Priority)
- Default mode: Verify critical claims only (CVSS, EPSS, KEV, Patch)
- Comprehensive mode: Verify all verifiable claims in enrichment

**Event Investigation Verification:**

- User explicitly requests: `*fact-check-event {investigation-id}`
- Reviewer wants to validate event investigation claims (IP addresses, geolocation, threat intel)
- Verify IP ownership (ASN), geolocation claims, threat intelligence associations, protocol/port combinations

## Inputs Required

**For CVE Verification:**

- **Enrichment document path:** JIRA ticket enrichment comment or custom field content
- **CVE ID:** For querying authoritative sources (must match CVE-YYYY-NNNNN pattern)
- **Claims to verify:** Selectable (critical only vs. comprehensive)
- **Claim type:** `cve` (default)

**For Event Investigation Verification:**

- **Investigation document path:** Event investigation markdown file
- **Investigation ID:** Event/alert identifier (e.g., ALERT-2024-11-09-001)
- **Claims to verify:** IP ownership, geolocation, threat intel, protocol/port (all or selective)
- **Claim type:** `event_investigation`

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

**Claim Type Detection:**

Determine claim type from input parameters or document analysis:

- If `claim_type=cve` OR CVE ID provided → CVE verification workflow
- If `claim_type=event_investigation` OR investigation document → Event verification workflow
- Default: CVE verification (backward compatibility)

**Security Validation:**

**For CVE Verification:**

- **CVE ID Format:** Validate CVE-YYYY-NNNNN pattern before proceeding
- **Ticket ID Sanitization:** Sanitize JIRA ticket IDs to prevent injection attacks
- **Enrichment Path Validation:** Verify file paths are within expected project directories
- **Query Parameter Sanitization:** Escape special characters in Perplexity queries

**For Event Investigation Verification:**

- **IP Address Format:** Validate IPv4/IPv6 format, reject malformed IPs
- **Investigation ID Sanitization:** Sanitize investigation IDs to prevent injection
- **Investigation Path Validation:** Verify file paths are within expected project directories
- **Query Parameter Sanitization:** Escape special characters in Perplexity queries
- **Private IP Detection:** Identify private IPs (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) - cannot verify externally

**Validation Rules:**

```
# CVE Verification
CVE ID: Must match regex ^CVE-\d{4}-\d{4,}$
Ticket ID: Must match project JIRA key pattern

# Event Investigation Verification
IP Address (IPv4): Must match regex ^(\d{1,3}\.){3}\d{1,3}$, octets 0-255
IP Address (IPv6): Must match standard IPv6 format
Investigation ID: Alphanumeric with hyphens only
Port Number: Must be 1-65535

# Common
File Path: Must be within project directory, no ../ traversal
Max Query Length: 500 characters per Perplexity query
```

**If validation fails:**

- Log security validation failure
- Skip verification for invalid inputs
- Note in report: "⚠️ Security validation failed for {input}"
- Continue with valid inputs only

### Step 2: Extract Claims from Document

Parse document and extract factual assertions based on claim type.

**Route to appropriate extraction logic:**

- If claim_type = `cve` → Extract CVE claims (below)
- If claim_type = `event_investigation` → Extract event investigation claims (Step 2b)

#### Step 2a: Extract CVE Claims

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
Extracted CVE Claims:

- CVSS Base Score: 9.8
- CVSS Severity: Critical
- EPSS Score: 0.85
- EPSS Percentile: 85th
- KEV Status: Not Listed
- Affected Versions: 2.0.0 - 2.5.32
- Patched Version: 2.5.33+
- Exploit Status: Active Exploitation
```

**Next Step:** Proceed to Step 3 (CVE verification)

#### Step 2b: Extract Event Investigation Claims

Parse event investigation document and extract factual assertions:

**IP Ownership Claims:**

- IP address and claimed ASN/organization
- Example: "Source IP 192.0.2.50 belongs to Acme Corp ASN 64512"

**Geolocation Claims:**

- IP address and claimed location (country, city, coordinates)
- Example: "IP 203.0.113.10 is located in Tokyo, Japan"

**Threat Intelligence Claims:**

- IP/domain and claimed threat associations
- Example: "IP 198.51.100.25 is associated with Emotet botnet"

**Protocol/Port Claims:**

- Protocol and port number combination
- Example: "SSH connection on port 22"

**Historical Pattern Claims (Optional - if Atlassian MCP available):**

- Alert frequency or occurrence patterns
- Example: "This alert fires daily at 02:00 UTC"

**Extraction Format:**

```markdown
Extracted Event Investigation Claims:

IP Ownership:

- Claim: "Source IP 192.0.2.50 belongs to Acme Corp ASN 64512"
- IP: 192.0.2.50
- Claimed ASN: AS64512
- Claimed Org: Acme Corp

Geolocation:

- Claim: "IP 203.0.113.10 is located in Tokyo, Japan"
- IP: 203.0.113.10
- Claimed Location: Tokyo, Japan

Threat Intelligence:

- Claim: "IP 198.51.100.25 is associated with Emotet botnet"
- IP: 198.51.100.25
- Claimed Threat: Emotet botnet

Protocol/Port:

- Claim: "SSH connection on port 8080"
- Protocol: SSH
- Port: 8080

Historical Pattern (if applicable):

- Claim: "This alert fires daily at 02:00 UTC"
- Claimed Frequency: Daily at 02:00 UTC
```

**Next Step:** Proceed to Step 3-Event (Event verification steps)

### Step 3-CVE: Verify CVE Claims Using Perplexity

**Note:** This step applies to CVE verification only. For event investigation verification, skip to Step 3-Event.

Use Perplexity MCP to verify CVE claims against authoritative sources.

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

### Step 3-Event: Verify Event Investigation Claims Using Perplexity

**Note:** This step applies to event investigation verification only. For CVE verification, use Step 3-CVE above.

Use Perplexity MCP to verify event investigation claims against authoritative sources.

**Rate Limiting:**

- Implement 1-second delay between queries
- Maximum 10 queries per session (standard mode)
- Maximum 20 queries per session (comprehensive mode)
- Warn user if comprehensive mode exceeds limits

**Error Handling:**

- **MCP Unavailable:** Skip verification, note in report
- **Query Timeout:** Retry once with 60s timeout, then skip
- **Conflicting Sources:** Document all, prioritize by authority
- **No Data Available:** Note as "⚠️ Unable to verify - information not available"
- **Private IP Addresses:** Note as "⚠️ Unable to verify - private IP address (no external data)"

#### Step 3-Event-1: IP Ownership Verification

**Purpose:** Verify IP address ownership and ASN claims

**Query Format:**

```
IP address {ip} ASN ownership and organization - provide ASN number, organization name, and country. Use authoritative sources like WHOIS, RIPEstat, or IPInfo.
```

**Tool Call:**

```
mcp__perplexity__search({
  query: "IP address {ip} ASN ownership and organization - provide ASN number, organization name, and country. Use authoritative sources like WHOIS, RIPEstat, or IPInfo.",
  force_model: false
})
```

**Expected Response:**

- ASN: AS{number}
- Organization: {org_name}
- Country: {country}
- Source: WHOIS via RIPEstat / IPInfo / ARIN

**Verification Logic:**

```
IF claimed_asn == verified_asn AND claimed_org == verified_org THEN ✅ MATCH
ELSE IF claimed_asn == verified_asn BUT claimed_org != verified_org THEN ⚠️ PARTIAL MATCH
  Impact: ASN correct but organization name differs
  Action: Update organization name to match authoritative source
ELSE ❌ MISMATCH (Significant Discrepancy)
  Impact: Incorrect IP ownership attribution
  Action: Correct ASN and organization to verified values

SPECIAL CASES:
IF ip is private (10.x, 172.16-31.x, 192.168.x) THEN ⚠️ UNABLE TO VERIFY
  Note: "Cannot verify private IP ownership via external sources"
```

**Example:**

```markdown
**Claim:** "Source IP 192.0.2.50 belongs to Acme Corp ASN 64512"

**Verification Result:**

- Verified ASN: AS64512
- Verified Org: Acme Corporation
- Source: WHOIS via RIPEstat
- Status: ✅ MATCH (Acme Corp = Acme Corporation, acceptable variation)
```

#### Step 3-Event-2: Geolocation Verification

**Purpose:** Verify IP geolocation claims (country, city, coordinates)

**Query Format:**

```
IP address {ip} geolocation country city coordinates - provide country, city, latitude, longitude. Use authoritative sources like MaxMind GeoIP, IP2Location, or ipstack.
```

**Tool Call:**

```
mcp__perplexity__search({
  query: "IP address {ip} geolocation country city coordinates - provide country, city, latitude, longitude. Use authoritative sources like MaxMind GeoIP, IP2Location, or ipstack.",
  force_model: false
})
```

**Expected Response:**

- Country: {country_name}
- City: {city_name}
- Coordinates: {latitude}° N/S, {longitude}° E/W
- Source: MaxMind GeoIP2 / IP2Location / ipstack

**Verification Logic:**

```
IF claimed_country == verified_country AND claimed_city == verified_city THEN ✅ MATCH
ELSE IF claimed_country == verified_country BUT claimed_city != verified_city THEN ⚠️ PARTIAL MATCH
  Impact: Country correct but city differs
  Action: Update city to match verified location
ELSE ❌ MISMATCH (Significant Discrepancy)
  Impact: Incorrect geolocation (could affect threat analysis)
  Action: Correct geolocation to verified values

SPECIAL CASES:
IF ip is private THEN ⚠️ UNABLE TO VERIFY
  Note: "Cannot verify private IP geolocation via external sources"
IF conflicting_data_across_sources THEN ⚠️ CONFLICTING DATA
  Note: "Multiple sources report different locations - {list sources}"
  Action: Use most authoritative source (MaxMind > IP2Location > others)
```

**Example:**

```markdown
**Claim:** "IP 203.0.113.10 is located in Paris, France"

**Verification Result:**

- Verified Location: Tokyo, Japan (35.6762° N, 139.6503° E)
- Source: MaxMind GeoIP2 via IPInfo
- Status: ❌ MISMATCH
- Discrepancy: Claimed location (Paris, France) does not match verified location (Tokyo, Japan)
- Recommendation: Correct geolocation claim to Tokyo, Japan
```

#### Step 3-Event-3: Threat Intelligence Verification

**Purpose:** Verify IP/domain threat intelligence claims (malicious activity, botnet associations)

**Query Format:**

```
Threat intelligence for IP {ip} - is this IP associated with malicious activity, botnets, or malware campaigns? Check AbusIPDB, ThreatFox, AlienVault OTX, and VirusTotal. Provide specific threat associations if found.
```

**Tool Call:**

```
mcp__perplexity__search({
  query: "Threat intelligence for IP {ip} - is this IP associated with malicious activity, botnets, or malware campaigns? Check AbusIPDB, ThreatFox, AlienVault OTX, and VirusTotal. Provide specific threat associations if found.",
  force_model: false
})
```

**Expected Response:**

- Reputation: Clean / Suspicious / Malicious
- Associated with: {threat_name} (if applicable)
- First Seen: {date} (if malicious)
- Confidence: Low / Medium / High
- Sources: ThreatFox, AbusIPDB ({report_count} reports), AlienVault OTX, VirusTotal

**Verification Logic:**

```
IF claimed_threat == verified_threat THEN ✅ MATCH
  Example: Claimed "Emotet botnet" and verified "Emotet botnet C2 server"
ELSE IF claimed_threat_category matches verified_threat_category THEN ⚠️ PARTIAL MATCH
  Example: Claimed "botnet activity" and verified "Emotet botnet C2 server"
  Impact: General claim correct, specific details differ
  Action: Update with specific threat name
ELSE IF claimed_clean BUT verified_malicious THEN ❌ MISMATCH (Critical Discrepancy)
  Impact: Missing critical threat intelligence
  Action: Add threat intelligence to investigation
ELSE IF claimed_malicious BUT verified_clean THEN ❌ MISMATCH (Significant Discrepancy)
  Impact: False positive threat claim
  Action: Remove or correct threat claim
ELSE ❌ MISMATCH
  Impact: Incorrect threat attribution
  Action: Correct threat claim to match verified intelligence

SPECIAL CASES:
IF no_threat_intel_available THEN ⚠️ UNABLE TO VERIFY
  Note: "No threat intelligence data available for this IP"
IF conflicting_sources THEN ⚠️ MIXED REPUTATION
  Note: "Some sources report malicious activity, others report clean"
  Action: Document all sources, note confidence level
```

**Example:**

```markdown
**Claim:** "IP 198.51.100.25 is associated with Emotet botnet"

**Verification Result:**

- Verified Reputation: Malicious
- Verified Threat: Emotet botnet C2 server
- First Seen: 2024-10-15
- Confidence: High
- Sources: ThreatFox, AbusIPDB (127 reports)
- Status: ✅ MATCH
- Notes: Multiple threat intel sources confirm association with Emotet campaign
```

#### Step 3-Event-4: Protocol/Port Validation

**Purpose:** Verify protocol/port combination claims against standard port assignments

**Query Format:**

```
Is {protocol} protocol typically used on port {port}? Provide IANA standard port assignment. Note if this is a non-standard or unusual combination.
```

**Tool Call:**

```
mcp__perplexity__search({
  query: "Is {protocol} protocol typically used on port {port}? Provide IANA standard port assignment. Note if this is a non-standard or unusual combination.",
  force_model: false
})
```

**Expected Response:**

- Standard Port: {port_number}
- Protocol: {protocol_name}
- IANA Assignment: Yes / No / Reserved
- Common Usage: Standard / Non-standard / Unusual
- Source: IANA Port Registry / RFC {number}

**Verification Logic:**

```
IF claimed_port == iana_standard_port THEN ✅ MATCH (Standard)
  Note: "Standard port/protocol combination"
ELSE IF claimed_port in common_alternate_ports THEN ⚠️ NON-STANDARD BUT VALID
  Example: SSH on port 2222 instead of 22
  Note: "Non-standard port for {protocol}, but commonly used alternative"
ELSE ❌ UNUSUAL COMBINATION
  Example: SSH on port 8080
  Note: "Port {port} is non-standard for {protocol}. Standard port is {iana_port}."
  Impact: May indicate evasion, misconfiguration, or tunneling
  Recommendation: Flag for further investigation

SPECIAL CASES:
IF port > 65535 OR port < 1 THEN ❌ INVALID PORT
  Note: "Port number out of valid range (1-65535)"
IF protocol_unknown THEN ⚠️ UNABLE TO VERIFY
  Note: "Unknown or custom protocol"
```

**Example:**

```markdown
**Claim:** "SSH connection on port 8080"

**Verification Result:**

- Standard Port: 22 (IANA)
- Verified Port: 8080 (non-standard)
- Source: IANA Port Registry
- Status: ❌ UNUSUAL
- Notes: Port 8080 is non-standard for SSH. This may indicate evasion or misconfiguration.
- Recommendation: Investigate why SSH is using non-standard port
```

#### Step 3-Event-5: Historical Pattern Verification (Optional)

**Prerequisites:** Atlassian MCP (`mcp__atlassian__*`) must be available

**Purpose:** Verify claims about alert frequency and historical occurrence patterns

**MCP Availability Check:**

```
IF mcp__atlassian__* tools available THEN
  Proceed with historical pattern verification
ELSE
  Skip this verification type
  Note in report: "⚠️ Historical pattern verification skipped (Atlassian MCP unavailable)"
```

**Query Construction (if MCP available):**

Use Atlassian MCP to search JIRA for historical tickets matching the alert pattern.

**Example JIRA Query:**

```
summary ~ "Alert-Name-Pattern" AND created >= -30d ORDER BY created DESC
```

**Analysis Steps:**

1. Count tickets matching pattern in last 30 days
2. Extract creation timestamps
3. Analyze frequency pattern (daily, weekly, sporadic)
4. Calculate average occurrence time (if pattern detected)

**Verification Logic:**

```
claimed_frequency = Extract from claim (e.g., "daily at 02:00 UTC")
actual_frequency = Calculate from JIRA tickets (e.g., 15 tickets in 30 days = ~0.5/day)

IF claimed_frequency matches actual_frequency THEN ✅ MATCH
  Example: Claimed "daily" and actual "30 tickets in 30 days"
ELSE ❌ MISMATCH
  Impact: Incorrect frequency assessment
  Action: Update frequency claim to match historical data

SPECIAL CASES:
IF insufficient_data (< 5 tickets) THEN ⚠️ UNABLE TO VERIFY
  Note: "Insufficient historical data (only {count} tickets found)"
IF mcp_unavailable THEN ⚠️ SKIPPED
  Note: "Historical pattern verification skipped (Atlassian MCP unavailable)"
```

**Example:**

```markdown
**Claim:** "This alert fires daily at 02:00 UTC"

**Verification Result:**

- Historical Tickets Found: 15 in last 30 days
- Actual Frequency: 2-3 times per week
- Time Pattern: Varying times (no consistent 02:00 UTC pattern)
- Source: JIRA historical ticket search
- Status: ❌ MISMATCH
- Discrepancy: Claimed daily pattern does not match actual 2-3x weekly pattern
- Recommendation: Update frequency claim to "2-3 times per week" based on historical data
```

**If MCP Unavailable:**

```markdown
**Claim:** "This alert fires daily at 02:00 UTC"

**Verification Result:**

- Status: ⚠️ SKIPPED
- Reason: Atlassian MCP unavailable
- Recommendation: Manually verify alert frequency via JIRA or monitoring system
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

Generate report based on claim type (CVE or Event Investigation).

#### Step 6a: CVE Fact Verification Report Structure

```markdown
# Fact Verification Report - CVE

**CVE:** {cve_id}
**Ticket:** {ticket_id}
**Analyst:** {analyst_name}
**Reviewer:** {reviewer_name}
**Verification Date:** {timestamp}
**Verification Type:** CVE Verification
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

{Critical discrepancies here - CVSS severity mismatch, KEV status wrong}

### 🟡 Significant Discrepancies

{Significant discrepancies here - CVSS score 0.5-2.0 diff, EPSS >0.10 diff, patch version wrong}

### 🔵 Minor Discrepancies

{Minor discrepancies here - formatting differences, minor CVSS/EPSS variations}

---

## Verified Claims (✅ Accurate)

{List all matching CVE claims}

---

## Unable to Verify (⚠️)

{List CVE claims that couldn't be verified with reasons}

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

#### Step 6b: Event Investigation Fact Verification Report Structure

```markdown
# Fact Verification Report - Event Investigation

**Investigation ID:** {investigation_id}
**Event/Alert:** {event_name}
**Analyst:** {analyst_name}
**Reviewer:** {reviewer_name}
**Verification Date:** {timestamp}
**Verification Type:** Event Investigation
**Verification Scope:** [IP Ownership | Geolocation | Threat Intel | Protocol/Port | Historical Patterns | All]

---

## Verification Summary

**Claims Verified:** {total_claims}
**Matches:** {matches} ({match_percentage}%)
**Discrepancies:** {discrepancies} ({discrepancy_percentage}%)
**Unable to Verify:** {unknown}
**Skipped:** {skipped} (e.g., private IPs, MCP unavailable)

**Accuracy Score:** {accuracy_score}% ({accuracy_classification})

**Overall Assessment:** {approval_status}
**Recommended Action:** {action_required}

---

## Discrepancies Found

{List all discrepancies organized by claim type and severity}

### 🔴 Critical Discrepancies

**IP Ownership:**
{Critical IP ownership mismatches - wrong ASN/org}

**Geolocation:**
{Critical geolocation mismatches - wrong country}

**Threat Intelligence:**
{Critical threat intel mismatches - claimed clean but verified malicious, or vice versa}

### 🟡 Significant Discrepancies

**IP Ownership:**
{ASN correct but org name differs}

**Geolocation:**
{Country correct but city differs}

**Threat Intelligence:**
{Threat category correct but specific threat name differs}

**Protocol/Port:**
{Unusual port combinations}

**Historical Patterns:**
{Frequency claims don't match historical data}

### 🔵 Minor Discrepancies

{Minor formatting differences, acceptable variations}

---

## Verified Claims (✅ Accurate)

**IP Ownership:**
{Verified IP ownership claims}

**Geolocation:**
{Verified geolocation claims}

**Threat Intelligence:**
{Verified threat intel claims}

**Protocol/Port:**
{Verified protocol/port claims}

**Historical Patterns:**
{Verified historical pattern claims}

---

## Unable to Verify (⚠️)

**Private IP Addresses:**
{List private IPs that cannot be verified externally}

**Insufficient Data:**
{Claims with no available threat intel or geolocation data}

**MCP Unavailable:**
{Claims skipped due to MCP unavailability - e.g., historical patterns if Atlassian MCP unavailable}

---

## Source Authority Hierarchy Used

When conflicting information existed, prioritized:

1. **WHOIS/RIPEstat/ARIN** - IP ownership (ASN)
2. **MaxMind GeoIP2** - Geolocation (preferred over IP2Location)
3. **ThreatFox, AbusIPDB** - Threat intelligence (primary feeds)
4. **AlienVault OTX, VirusTotal** - Threat intelligence (secondary sources)
5. **IANA Port Registry** - Protocol/port standard assignments
6. **JIRA Historical Data** - Alert frequency patterns (if Atlassian MCP available)

---

## Next Steps

{Based on accuracy score and discrepancies, provide specific next steps}

**For Critical Discrepancies:**

- Require investigation correction before proceeding
- Flag incorrect threat intelligence or geolocation

**For Significant Discrepancies:**

- Recommend updates to investigation
- Update IP ownership or threat associations

**For Minor Discrepancies:**

- Optional cleanup
- Acceptable variations documented
```

## Source Authority Hierarchy

When conflicting information exists across sources, prioritize in this order.

### CVE Verification Source Hierarchy

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

### Event Investigation Verification Source Hierarchy

**1. WHOIS/RIPEstat/ARIN - IP Ownership**

- **Authoritative For:** ASN number, organization name, IP allocation
- **When to Use:** Always for IP ownership and ASN verification
- **When to Deviate:** Never - these are authoritative registries
- **Preference Order:** RIPEstat (RIPE region) > ARIN (North America) > WHOIS (fallback)

**2. MaxMind GeoIP2 - Geolocation**

- **Authoritative For:** IP geolocation (country, city, coordinates)
- **When to Use:** Primary source for geolocation claims
- **When to Deviate:** If conflicting with IP2Location, prefer MaxMind (higher accuracy)
- **Note:** Geolocation can be approximate, especially for mobile IPs

**3. ThreatFox + AbusIPDB - Threat Intelligence (Primary)**

- **Authoritative For:** Recent threat activity, botnet associations, malware campaigns
- **When to Use:** Primary sources for threat intelligence verification
- **When to Deviate:** Never for recent threats - these are actively updated feeds
- **Note:** High report count in AbusIPDB (>50) increases confidence

**4. AlienVault OTX + VirusTotal - Threat Intelligence (Secondary)**

- **Authoritative For:** Historical threat data, contextual threat intelligence
- **When to Use:** Secondary confirmation of threat intelligence
- **When to Deviate:** If conflicts with ThreatFox/AbusIPDB, prefer primary sources
- **Note:** Use for additional context, not sole authority

**5. IANA Port Registry - Protocol/Port Assignments**

- **Authoritative For:** Standard port assignments for protocols
- **When to Use:** Always for protocol/port standard verification
- **When to Deviate:** Never - IANA is definitive authority
- **Note:** Non-standard ports are valid but should be flagged as unusual

**6. JIRA Historical Data - Alert Frequency (Optional)**

- **Authoritative For:** Historical alert occurrence patterns
- **When to Use:** Only if Atlassian MCP available and sufficient data exists (>5 tickets)
- **When to Deviate:** N/A - internal data source, no external alternatives
- **Note:** Requires minimum 30 days of data for reliable pattern analysis

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

### CVE Verification Examples

**CVE Critical Mode (Default):**

```
Input: CVE-2024-1234, ticket VULN-123, enrichment document, claim_type=cve
Verifies: CVSS, EPSS, KEV, Patch (4 queries)
Output: CVE fact verification report with accuracy score
Time: ~10-15 seconds (with 1s delays between queries)
```

**CVE Comprehensive Mode:**

```
Input: CVE-2024-1234, ticket VULN-123, enrichment document, claim_type=cve, comprehensive=true
Verifies: All verifiable CVE claims (up to 20 queries)
Output: Detailed CVE fact verification report with all claims checked
Time: ~30-60 seconds (with 1s delays between queries)
Warning: User notified if >20 queries required
```

### Event Investigation Verification Examples

**Event Standard Mode:**

```
Input: Investigation ALERT-2024-11-09-001, investigation document, claim_type=event_investigation
Verifies: IP ownership (2 IPs), geolocation (2 IPs), threat intel (1 IP), protocol/port (1 claim) = ~6 queries
Output: Event investigation fact verification report with accuracy score
Time: ~15-20 seconds (with 1s delays between queries)
```

**Event Comprehensive Mode (with Atlassian MCP):**

```
Input: Investigation ALERT-2024-11-09-001, investigation document, claim_type=event_investigation, comprehensive=true
Verifies: IP ownership, geolocation, threat intel, protocol/port, historical patterns (up to 20 queries)
Output: Detailed event investigation fact verification report with all claims checked
Time: ~30-60 seconds (with 1s delays between queries)
Note: Historical pattern verification included (Atlassian MCP available)
```

**Event Mode (Atlassian MCP Unavailable):**

```
Input: Investigation ALERT-2024-11-09-001, investigation document, claim_type=event_investigation
Verifies: IP ownership, geolocation, threat intel, protocol/port (historical patterns skipped)
Output: Event investigation fact verification report (note: historical pattern verification skipped)
Time: ~15-20 seconds
Note: Historical pattern verification skipped (Atlassian MCP unavailable)
```

**Event Mode with Private IPs:**

```
Input: Investigation with private IPs (10.0.0.5, 192.168.1.100)
Verifies: Protocol/port only (IP ownership/geolocation/threat intel skipped for private IPs)
Output: Event investigation fact verification report
Time: ~5-10 seconds
Note: Private IPs cannot be verified via external sources (noted in report as "Unable to Verify")
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

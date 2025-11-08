# Research CVE Task

## Purpose

Research a CVE using Perplexity AI to gather comprehensive vulnerability intelligence including CVSS scores, EPSS probability, KEV status, exploits, patches, and MITRE ATT&CK mappings.

## Prerequisites

- Perplexity MCP server connected (available by default in Claude Code)
- Valid CVE identifier (CVE-YYYY-NNNNN format)
- Internet connectivity for AI-assisted research

## Configuration Requirements

No configuration required - Perplexity MCP is available by default in Claude Code.

## Task Steps

### Step 1: Elicit and Validate CVE Identifier

Ask the user: **"Please provide the CVE identifier to research (e.g., CVE-2024-1234):"**

**Validate CVE format:** `CVE-\d{4}-\d{4,7}` (case-insensitive)

**Valid examples:**

- CVE-2024-1234
- CVE-2023-44487
- CVE-2021-44228

**Invalid examples:**

- 2024-1234 (missing CVE prefix)
- CVE-24-1234 (year must be 4 digits)
- CVE-2024-123 (ID must be at least 4 digits)

**If validation fails:**

- Display: "❌ Invalid CVE format. Expected format: CVE-YYYY-NNNNN (e.g., CVE-2024-1234)"
- Re-prompt user for valid CVE identifier
- Max 3 attempts before halting

### Step 2: Construct Research Query

Build comprehensive research query requesting all required intelligence fields:

#### Query Template for Initial Research

```
Research {cve_id} comprehensive vulnerability intelligence:

REQUIRED INFORMATION:
1. CVSS Base Score and Vector String (from NIST NVD)
2. EPSS Exploitation Probability Score (from FIRST.org EPSS)
3. CISA KEV Catalog Status (Listed or Not Listed with dates)
4. Affected Product and Version Ranges (precise versions)
5. Patched Versions (if available with vendor advisory links)
6. Exploit Availability (PoC code, exploit frameworks, active exploitation)
7. MITRE ATT&CK Tactics and Techniques (with T-numbers)
8. Vendor Security Advisory Links (official vendor sites)
9. Technical Description (vulnerability mechanism and impact)
10. Attack Complexity and Prerequisites

AUTHORITATIVE SOURCES REQUIRED:
- NIST NVD (nvd.nist.gov)
- CISA KEV Catalog (cisa.gov/known-exploited-vulnerabilities-catalog)
- FIRST EPSS (first.org/epss)
- MITRE ATT&CK (attack.mitre.org)
- Vendor Security Advisories (official vendor sites only)

Provide specific citations with URLs for all factual claims.
Flag any information that cannot be verified from authoritative sources.
```

### Step 3: Determine Severity and Select Perplexity Tool

**Initial Research (Severity Unknown):**
Use `mcp__perplexity__reason` to get basic CVE information including CVSS score.

**Execute initial research:**

```
mcp__perplexity__reason
  query: {constructed_query}
```

**Parse CVSS score from response:**

- Extract numerical score (0.0-10.0)
- Extract severity rating (Low/Medium/High/Critical)
- If CVSS not found, default severity to "Unknown"

**Select appropriate tool based on CVSS severity:**

| CVSS Score | Severity | Perplexity Tool                  | Rationale                                  |
| ---------- | -------- | -------------------------------- | ------------------------------------------ |
| 9.0 - 10.0 | Critical | `mcp__perplexity__deep_research` | Requires comprehensive 2-5 minute analysis |
| 7.0 - 8.9  | High     | `mcp__perplexity__reason`        | Requires moderate 30-60 second analysis    |
| 4.0 - 6.9  | Medium   | `mcp__perplexity__search`        | Requires basic 10-20 second lookup         |
| 0.1 - 3.9  | Low      | `mcp__perplexity__search`        | Requires quick lookup                      |
| Unknown    | Unknown  | `mcp__perplexity__reason`        | Default to moderate analysis               |

**If Critical severity detected:**

- Display: "⚠️ Critical vulnerability detected (CVSS {score}). Initiating deep research (2-5 minutes)..."
- Re-execute research with `mcp__perplexity__deep_research` for comprehensive analysis

### Step 4: Parse and Validate Research Findings

Extract the following intelligence fields from the Perplexity response:

#### 4.1 CVSS Information

- **CVSS Score:** Numerical value (0.0-10.0)
- **CVSS Vector String:** Format `CVSS:3.1/AV:X/AC:X/PR:X/UI:X/S:X/C:X/I:X/A:X`
- **Severity Rating:** Critical, High, Medium, Low
- **Source:** Must be from NVD (nvd.nist.gov)

#### 4.2 EPSS Information

- **EPSS Score:** Probability value (0.0-1.0 or percentage)
- **EPSS Percentile:** Ranking (0-100)
- **Source:** Must be from FIRST.org EPSS

**If EPSS not available:**

- Flag: "⚠️ EPSS score not available for {cve_id}"
- Set EPSS score to `null`
- Continue with other intelligence

#### 4.3 CISA KEV Status

- **Status:** "Listed" or "Not Listed"
- **Date Added:** If listed, date when added to KEV catalog
- **Due Date:** If listed, remediation due date
- **Source:** Must be from cisa.gov

#### 4.4 Affected Products and Versions

- **Product Name:** Full product name (e.g., "Apache Struts 2")
- **Vendor:** Product vendor (e.g., "Apache Software Foundation")
- **Affected Versions:** Version ranges (e.g., "2.0.0 - 2.5.32")
- **Version Format:** Use precise version numbers, not "all versions"

#### 4.5 Patch Information

- **Patched Versions:** Fixed version numbers (e.g., "2.5.33+", "3.0.0+")
- **Vendor Advisory URL:** Official vendor security advisory link
- **Patch Availability Status:** Available, Partial, Not Available, Workaround Only

**If no patch available:**

- Flag: "⚠️ No patch available for {cve_id}"
- Check for workarounds in vendor advisory

#### 4.6 Exploit Information

- **PoC Available:** Boolean (true/false)
- **Exploit Code Public:** Boolean (true/false)
- **Exploit Frameworks:** List (e.g., Metasploit, ExploitDB)
- **Active Exploitation:** Boolean - confirmed in-the-wild exploitation
- **Source:** Security vendor reports, threat intelligence

#### 4.7 MITRE ATT&CK Mapping

- **Tactics:** List of tactic names (e.g., "Initial Access", "Execution")
- **Techniques:** List with T-numbers (e.g., "T1190 - Exploit Public-Facing Application")
- **Source:** Must cite attack.mitre.org or threat intelligence report

**If ATT&CK mapping not available:**

- Flag: "⚠️ MITRE ATT&CK mapping not available for {cve_id}"
- Attempt to infer techniques from vulnerability type
- Clearly mark inferred techniques as "INFERRED" vs "CONFIRMED"

#### 4.8 Technical Description

- **Vulnerability Type:** CWE classification (e.g., "CWE-78: OS Command Injection")
- **Attack Vector:** How vulnerability is exploited
- **Impact:** Confidentiality, Integrity, Availability impacts
- **Prerequisites:** Conditions required for successful exploitation

### Step 5: Validate Authoritative Sources

**Review all sources cited in Perplexity response:**

#### Trusted Sources (ACCEPT):

- nvd.nist.gov (NIST NVD)
- cve.mitre.org (MITRE CVE)
- cisa.gov (CISA)
- first.org (FIRST EPSS)
- attack.mitre.org (MITRE ATT&CK)
- security.microsoft.com (Microsoft)
- access.redhat.com/security (Red Hat)
- ubuntu.com/security (Ubuntu)
- security.debian.org (Debian)
- security.apache.org (Apache)
- github.com/advisories (GitHub Security Advisories)
- Oracle, Cisco, VMware, Adobe official security sites

#### Untrusted Sources (FLAG):

- Blog posts (unless from recognized security researchers)
- News sites (CNN, TechCrunch, etc.) - secondary sources
- Social media (Twitter, Reddit, etc.)
- Unverified forums or paste sites
- Sites without HTTPS

**For each untrusted source found:**

- Flag: "⚠️ Information from untrusted source: {url}"
- Mark associated data as "UNVERIFIED"
- Attempt to find authoritative source for same information

**If critical information only available from untrusted sources:**

- Flag: "⚠️ Critical information lacks authoritative source citation"
- Include information but clearly mark as "REQUIRES VERIFICATION"

### Step 6: Handle Conflicts and Missing Data

#### Conflicting Information

**If CVSS scores differ between sources:**

- Display: "⚠️ CVSS score conflict detected:"
- List all sources and their scores:
  ```
  - NVD: 9.8
  - Vendor Advisory: 8.1
  ```
- **Resolution:** Prioritize NVD as authoritative source
- Document discrepancy in notes

**If exploit status conflicts:**

- Display: "⚠️ Exploit status conflict detected"
- Document all sources and their claims
- Use most recent and authoritative source
- Mark as "CONFLICTING REPORTS" in output

#### Missing Information

**Track all missing intelligence fields:**

- CVSS: "⚠️ CVSS score not available"
- EPSS: "⚠️ EPSS probability not available"
- KEV: "⚠️ KEV status unknown"
- Patch: "⚠️ Patch information not available"
- Exploit: "⚠️ Exploit status unknown"
- ATT&CK: "⚠️ ATT&CK mapping not available"

**Continue with available information** - do not halt on missing fields.

### Step 7: Display Research Summary

Present findings to user in formatted output:

```
✅ CVE Research Complete: {cve_id}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEVERITY ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CVSS Score: {score} ({severity})
CVSS Vector: {vector_string}
EPSS Score: {epss_score} ({epss_percentile}th percentile)
CISA KEV: {kev_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AFFECTED PRODUCTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Product: {product_name}
Vendor: {vendor_name}
Affected Versions: {affected_versions}
Patched Versions: {patched_versions}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXPLOIT INTELLIGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PoC Available: {poc_status}
Public Exploit Code: {exploit_code_status}
Active Exploitation: {active_exploitation_status}
Exploit Frameworks: {frameworks_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MITRE ATT&CK MAPPING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tactics: {tactics_list}
Techniques:
  - {technique_1}
  - {technique_2}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{source_citations_list}

⚠️ WARNINGS (if any):
{warnings_list}
```

### Step 8: Return Structured Data

Return the following YAML structure for use by subsequent tasks:

```yaml
cve_id: '{cve_id}'
cvss:
  score: { numerical_score }
  vector: '{vector_string}'
  severity: '{severity_rating}'
  source: '{source_url}'
epss:
  score: { probability_score }
  percentile: { percentile_value }
  source: '{source_url}'
kev:
  status: '{Listed|Not Listed}'
  date_added: '{date}' # If listed
  due_date: '{date}' # If listed
  source: '{source_url}'
affected_products:
  - product: '{product_name}'
    vendor: '{vendor_name}'
    affected_versions: '{version_range}'
patches:
  available: { true|false }
  versions: ['{version_1}', '{version_2}']
  advisory_url: '{vendor_advisory_url}'
exploit_status:
  poc_available: { true|false }
  exploit_code_public: { true|false }
  active_exploitation: { true|false }
  frameworks: ['{framework_1}', '{framework_2}']
attack_mapping:
  tactics: ['{tactic_1}', '{tactic_2}']
  techniques:
    - id: '{T-number}'
      name: '{technique_name}'
      confidence: '{CONFIRMED|INFERRED}'
description:
  vulnerability_type: '{CWE-XX: Description}'
  attack_vector: '{description}'
  impact: '{description}'
  prerequisites: '{description}'
sources:
  - url: '{url_1}'
    type: '{NVD|CISA KEV|Vendor Advisory|etc}'
  - url: '{url_2}'
    type: '{type}'
warnings:
  - '{warning_1}'
  - '{warning_2}'
metadata:
  research_tool_used: '{search|reason|deep_research}'
  research_timestamp: '{ISO-8601 timestamp}'
  research_duration: '{duration in seconds}'
```

## Error Handling

### Perplexity Timeout

**Symptoms:**

- Request exceeds tool timeout (2 minutes for search/reason, 10 minutes for deep_research)
- Network connection issues
- Service unavailable errors

**Recovery Strategy:**

1. Display: "⚠️ Perplexity research timed out. Retrying with simpler query..."
2. Simplify query by reducing requested fields to critical only (CVSS, EPSS, KEV)
3. Retry with next-faster tool:
   - If `deep_research` failed → Retry with `reason`
   - If `reason` failed → Retry with `search`
   - If `search` failed → Offer manual research option
4. Max 2 retries before offering manual input

**Manual research prompt:**

```
❌ Automated research failed for {cve_id}.

Options:
1. Manually provide CVSS score to continue with limited research
2. Skip research and mark vulnerability for manual analysis
3. Retry research (attempt {attempt_number}/3)

Select option (1-3):
```

### Invalid CVE Identifier

**Symptoms:**

- CVE ID not found in any vulnerability databases
- Typo in CVE identifier
- Reserved CVE number (not yet published)

**Recovery Strategy:**

1. Display: "❌ CVE {cve_id} not found in vulnerability databases."
2. Check if CVE is reserved but not published:
   - Display: "⚠️ This CVE may be reserved but not yet published."
3. Offer to correct CVE identifier:

   ```
   Options:
   1. Re-enter CVE identifier (check for typos)
   2. Research anyway (may find limited information)
   3. Exit research task

   Select option (1-3):
   ```

### Missing Critical Information

**Symptoms:**

- CVSS score not available
- CVE exists but has minimal information
- Pre-disclosure or embargoed vulnerability

**Recovery Strategy:**

1. Continue research with available information
2. Flag all missing critical fields:

   ```
   ⚠️ INCOMPLETE CVE DATA for {cve_id}

   Missing Information:
   - CVSS score not available
   - EPSS probability not calculated
   - Vendor advisory not published

   Available Information:
   - Basic CVE description
   - Affected product identified

   Recommendation: Monitor for updated CVE information
   ```

3. Return partial structured data with `null` values for missing fields
4. Set warning flag: `incomplete_data: true`

### Conflicting Source Information

**Symptoms:**

- Different CVSS scores from NVD vs vendor
- Conflicting patch version numbers
- Disputed exploitation status

**Recovery Strategy:**

1. Document all conflicting sources
2. Apply priority hierarchy:
   - **CVSS:** NVD > Vendor > Third-party
   - **Patches:** Vendor > NVD > Third-party
   - **Exploitation:** CISA > Security vendors > Researchers
3. Flag discrepancies in warnings section:

   ```
   ⚠️ CONFLICTING INFORMATION DETECTED

   CVSS Score Discrepancy:
   - NVD: 9.8 (Critical)
   - Vendor Advisory: 8.1 (High)

   Resolution: Using NVD score (9.8) as authoritative source

   Note: Review vendor advisory for additional context
   Advisory URL: {vendor_url}
   ```

4. Include all sources in structured output for manual review

### Perplexity Hallucination Detection

**Symptoms:**

- Citations to non-existent URLs
- Fabricated CVE details
- Information not verifiable from authoritative sources

**Detection Strategy:**

1. Validate all URLs are accessible (not required to fetch, just check format)
2. Cross-reference critical facts:
   - CVSS scores against known ranges (0.0-10.0)
   - CVE ID format matches pattern
   - Dates are chronologically valid
3. Flag suspicious information:

   ```
   ⚠️ UNVERIFIED INFORMATION DETECTED

   The following information could not be verified from authoritative sources:
   - ATT&CK Technique: T9999 (invalid technique number)
   - EPSS score: 1.5 (exceeds valid range 0.0-1.0)

   Action: Flagged for manual verification
   ```

**Recovery Strategy:**

1. Mark unverified data with `verified: false` flag
2. Exclude hallucinated information from structured output
3. Log warning for security analyst review
4. Suggest manual verification from authoritative sources

## Security Considerations

**DO NOT:**

- Execute exploit code or PoC scripts
- Expose internal system details in research queries
- Log API keys or credentials
- Auto-apply patches without authorization

**DO:**

- CVE IDs are public information - safe to research
- Cite all sources for audit trail
- Flag unverified information clearly
- Maintain research audit log with timestamps

## Success Criteria

Task completes successfully when:

1. ✅ CVE identifier validated
2. ✅ Research query constructed and executed
3. ✅ CVSS severity determined (or marked unknown)
4. ✅ Intelligence fields extracted (or flagged as missing)
5. ✅ Sources validated as authoritative (or flagged)
6. ✅ Structured YAML data returned
7. ✅ User presented with formatted summary

**Task may complete with warnings** - missing data or unverified information does not constitute failure.

## Next Steps

After this task completes, the structured CVE data will be used by:

- Security enrichment workflows (documentation generation)
- Priority assessment tasks (CVSS + EPSS + KEV + business context)
- JIRA ticket updates (custom field population)
- Remediation planning (patch availability and urgency)
- Threat modeling (ATT&CK mapping and attack chain analysis)

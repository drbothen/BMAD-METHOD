# Security Enrichment Template Test Suite

## Overview

This test suite validates the security-enrichment-tmpl.yaml template against the BMAD template specification and ensures correct rendering of all 12 sections with various data scenarios.

**Template Under Test:** `expansion-packs/bmad-1898-engineering/templates/security-enrichment-tmpl.yaml`

**Story:** 1.4 Structured Enrichment Documentation

**Test Standards:**

- YAML template structure validates against BMAD template spec
- Variable substitution works with complete and partial data
- All 12 sections render correctly
- Markdown output is valid and well-formatted
- Missing data handled gracefully
- Quality gates validate correctly

## Test Cases

### TC-001: Complete Data Test

**Purpose:** Validate template with full Story 1.3 output (all fields populated)

**Input Data:**

```yaml
cve_id: CVE-2024-1234
vulnerability_title: Apache Struts Remote Code Execution via OGNL Injection
vulnerability_type: Remote Code Execution (RCE)
vulnerability_description: Apache Struts contains a critical remote code execution vulnerability allowing unauthenticated attackers to execute arbitrary code on vulnerable servers via malicious OGNL expressions in HTTP requests.
affected_product: Apache Struts
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
  due_date: 2024-11-22
affected_versions:
  - 'Apache Struts 2.0.0 - 2.5.32'
patched_versions:
  - 'Apache Struts 2.5.33+'
  - 'Apache Struts 6.0.0+'
exploit_status:
  poc_available: true
  exploit_code_public: true
  active_exploitation: true
attack_mapping:
  tactics:
    - Initial Access
    - Execution
  techniques:
    - T1190 - Exploit Public-Facing Application
    - T1059 - Command and Scripting Interpreter
sources:
  - url: https://nvd.nist.gov/vuln/detail/CVE-2024-1234
    type: NVD
  - url: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
    type: CISA KEV
  - url: https://www.first.org/epss/
    type: FIRST EPSS
  - url: https://security.apache.org/cve-2024-1234
    type: Apache Security Advisory
affected_systems:
  - system: prod-web-01
    version: Apache Struts 2.5.30
    acr: Critical
    exposure: Internet-Facing
  - system: prod-api-02
    version: Apache Struts 2.5.30
    acr: High
    exposure: Internal
  - system: uat-web-01
    version: Apache Struts 2.5.28
    acr: Medium
    exposure: Internal
priority: P1
priority_label: Critical
sla_timeline: 24 hours
```

**Derived Variables (Computed by Template Processor):**

```yaml
affected_versions_summary: '2.0.0 - 2.5.32'
affected_versions_list: '- Apache Struts 2.0.0 - 2.5.32'
patched_versions_list: "- Apache Struts 2.5.33+\n- Apache Struts 6.0.0+"
kev_status_text: Listed
kev_context: 'Added 2024-11-01, Due 2024-11-22'
epss_interpretation: High
exploit_status.poc_available_text: Yes
exploit_status.exploit_code_public_text: Yes
exploit_status.active_exploitation_text: Yes
exploit_maturity: 'Functional - weaponized exploit code publicly available and actively used in attacks'
exploit_availability_text: 'Public exploit code available'
exploit_context: 'Active exploitation in the wild'
attack_tactics_list: "- Initial Access\n- Execution"
attack_techniques_list: "- T1190 - Exploit Public-Facing Application\n- T1059 - Command and Scripting Interpreter"
detection_implications: 'Monitor web application logs for unusual POST requests, OGNL expressions in parameters, command execution attempts, and suspicious process spawning from web services.'
defensive_recommendations: "- Implement web application firewall (WAF) rules blocking OGNL patterns\n- Enable detailed logging for Struts applications\n- Monitor for unusual process execution from Java web server processes\n- Deploy network-based IDS/IPS signatures for known exploits"
affected_systems_table: "| System | Version | ACR | Exposure |\n|--------|---------|-----|----------|\n| prod-web-01 | Apache Struts 2.5.30 | Critical | Internet-Facing |\n| prod-api-02 | Apache Struts 2.5.30 | High | Internal |\n| uat-web-01 | Apache Struts 2.5.28 | Medium | Internal |"
patch_availability: 'Patch available - Apache Struts 2.5.33, 6.0.0'
recommended_action: 'Upgrade all affected Apache Struts instances to version 2.5.33 or 6.0.0 immediately.'
upgrade_path: "1. Test Apache Struts 2.5.33 in UAT environment\n2. Schedule emergency maintenance window for production systems\n3. Upgrade prod-web-01, prod-api-02 to Struts 2.5.33\n4. Validate application functionality post-upgrade\n5. Monitor for exploitation attempts"
vendor_advisory_links: '- [Apache Security Advisory - CVE-2024-1234](https://security.apache.org/cve-2024-1234)'
remediation_complexity: Medium
confidentiality_impact: 'High - Full system access possible'
integrity_impact: 'High - Arbitrary code execution allows system modification'
availability_impact: 'High - Attackers can crash services or install ransomware'
compliance_implications: 'Potential PCI-DSS, SOC 2 violations if payment/customer data exposed'
business_risk_rating: Critical
compensating_controls_content: "While patch is in emergency testing, implement these interim controls:\n\n**Network Segmentation:**\n- Restrict access to prod-web-01 from untrusted networks\n- Implement firewall rules limiting exposure to known business IP ranges\n\n**Access Controls:**\n- Enable IP allowlisting for administrative endpoints\n- Require VPN access for non-public application paths\n\n**Enhanced Monitoring:**\n- Enable detailed logging for all Struts applications\n- Configure SIEM alerts for OGNL injection patterns\n- Monitor for IOCs: unusual process spawning, outbound connections from web servers\n- Deploy WAF rules blocking common OGNL exploit patterns"
priority_rationale: 'CVE-2024-1234 poses immediate critical risk due to combination of Critical CVSS severity (9.8), high exploitation probability (EPSS 0.85), CISA KEV listing, public exploit availability, active exploitation in the wild, and internet-facing affected systems with Critical ACR.'
acr_rating: Critical
system_exposure: Internet-Facing
sla_deadline: '2024-11-09 00:00 UTC'
references_list: "- [NIST NVD - CVE-2024-1234](https://nvd.nist.gov/vuln/detail/CVE-2024-1234)\n- [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)\n- [FIRST EPSS](https://www.first.org/epss/)\n- [Apache Security Advisory](https://security.apache.org/cve-2024-1234)"
enrichment_timestamp: '2024-11-08 15:30:00 UTC'
research_tools_used: 'Perplexity AI (deep_research mode for Critical severity)'
confidence_level: High
data_sources_count: 4
```

**Expected Outcome:**

- All 12 sections render correctly
- All quality gates pass
- Output matches example in Story 1.4:869-1028
- Valid markdown syntax
- No missing variable errors

**Quality Gates (All Must Pass):**

- [x] All 12 sections have content
- [x] Executive summary is 2-3 sentences
- [x] CVSS score present and valid (9.8)
- [x] EPSS score present and valid (0.85)
- [x] KEV status determined (Listed)
- [x] At least one MITRE ATT&CK tactic identified (2 tactics)
- [x] Priority level assigned (P1)
- [x] Priority rationale provided
- [x] At least 3 authoritative sources cited (4 sources)

**Validation Steps:**

1. Load template YAML file
2. Inject all input variables
3. Process template sections 1-12
4. Generate markdown output
5. Validate markdown syntax
6. Verify all sections present
7. Check quality gates

---

### TC-002: Partial Data Test - Missing EPSS

**Purpose:** Validate graceful degradation when EPSS data unavailable

**Input Data:**
Same as TC-001, but with EPSS data missing:

```yaml
epss:
  score: null
  percentile: null
```

**Expected Derived Variables:**

```yaml
epss.score: 'Not available'
epss.percentile: 'Not available'
epss_interpretation: 'Not available'
```

**Expected Outcome:**

- Section 3 (Severity Metrics) shows "Not available" for EPSS row
- Other sections render normally
- Executive summary mentions EPSS unavailable or omits EPSS
- Priority assessment continues without EPSS factor

**Quality Gates:**

- [x] All 12 sections have content
- [x] CVSS score present and valid
- [ ] EPSS score present (shows "Not available" instead)
- [x] KEV status determined
- [x] Priority level assigned (may be P2 instead of P1 without EPSS data)

---

### TC-003: Partial Data Test - Not in KEV

**Purpose:** Validate rendering when CVE not listed in CISA KEV catalog

**Input Data:**
Same as TC-001, but with KEV status "Not Listed":

```yaml
kev:
  status: Not Listed
  date_added: null
  due_date: null
```

**Expected Derived Variables:**

```yaml
kev_status_text: 'Not Listed'
kev_context: 'Not in KEV catalog'
```

**Expected Outcome:**

- Section 3 shows "Not Listed" for KEV status
- Priority may be P2 or P3 instead of P1
- Priority rationale reflects absence from KEV
- SLA timeline adjusted accordingly

**Quality Gates:**

- [x] All 12 sections have content
- [x] KEV status determined (Not Listed)
- [x] Priority level assigned (P2-P3 expected)
- [x] Priority rationale addresses KEV absence

---

### TC-004: Minimal Data Test

**Purpose:** Validate template with only required fields

**Input Data:**

```yaml
cve_id: CVE-2024-9999
vulnerability_title: Unknown Vulnerability
vulnerability_type: Unknown
vulnerability_description: 'Limited information available.'
affected_product: Unknown Product
cvss:
  score: 5.5
  vector: CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H
  severity: Medium
affected_versions:
  - 'Unknown'
patched_versions: []
# No EPSS, KEV, exploit data
```

**Expected Outcome:**

- Template renders with available data
- Missing sections show "Not available" or similar
- No errors or crashes
- Priority defaults to P4 or P5

**Quality Gates:**

- [x] All 12 sections have content (some with "Not available")
- [x] CVSS score present and valid
- [ ] EPSS score present (expected to be missing)
- [ ] KEV status (expected to be Not Listed)
- [x] Priority level assigned (P4-P5)

---

### TC-005: Critical CVE Test

**Purpose:** Validate emphasis and urgency for critical severity CVE

**Input Data:**
Same as TC-001 (Critical CVE in KEV with active exploitation)

**Expected Outcome:**

- Priority P1
- SLA timeline 24 hours
- Business risk rating: Critical
- Compensating controls section populated (interim mitigations)
- Defensive recommendations section emphasizes urgency

**Quality Gates:**

- [x] Priority level P1
- [x] Business risk rating: Critical
- [x] SLA timeline 24 hours or less
- [x] Compensating controls provided

---

### TC-006: Low Severity CVE Test

**Purpose:** Validate appropriate priority for low severity CVE

**Input Data:**

```yaml
cve_id: CVE-2024-5555
vulnerability_title: Information Disclosure via Log Files
vulnerability_type: Information Disclosure
vulnerability_description: 'Application logs may contain sensitive information in debug mode.'
affected_product: Example App
cvss:
  score: 3.0
  vector: CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:L/I:N/A:N
  severity: Low
epss:
  score: 0.05
  percentile: 15.0
kev:
  status: Not Listed
  date_added: null
  due_date: null
affected_versions:
  - 'Example App 1.0.0 - 1.2.5'
patched_versions:
  - 'Example App 1.2.6+'
exploit_status:
  poc_available: false
  exploit_code_public: false
  active_exploitation: false
```

**Expected Outcome:**

- Priority P4 or P5
- Less urgent tone throughout
- Compensating controls may state "Not applicable - patch available"
- SLA timeline 30-90 days

**Quality Gates:**

- [x] Priority level P4-P5
- [x] Priority rationale reflects low severity
- [x] SLA timeline appropriate for low severity (30-90 days)

---

### TC-007: Multiple Affected Systems Test

**Purpose:** Validate Section 4 table with multiple systems

**Input Data:**

```yaml
affected_systems:
  - system: prod-web-01
    version: Apache Struts 2.5.30
    acr: Critical
    exposure: Internet-Facing
  - system: prod-web-02
    version: Apache Struts 2.5.30
    acr: Critical
    exposure: Internet-Facing
  - system: prod-api-01
    version: Apache Struts 2.5.30
    acr: High
    exposure: Internal
  - system: prod-api-02
    version: Apache Struts 2.5.30
    acr: High
    exposure: Internal
  - system: uat-web-01
    version: Apache Struts 2.5.28
    acr: Medium
    exposure: Internal
  - system: dev-web-01
    version: Apache Struts 2.5.25
    acr: Low
    exposure: Internal
```

**Expected Outcome:**

- Section 4 table displays all 6 systems
- Table formatting correct
- ACR and Exposure values accurate
- Priority assessment considers highest ACR (Critical)

**Quality Gates:**

- [x] All 6 systems listed in Section 4
- [x] Table markdown valid
- [x] Priority reflects Critical ACR systems

---

### TC-008: No Patch Available Test

**Purpose:** Validate Section 9 (Compensating Controls) when no patch available

**Input Data:**
Same as TC-001, but with:

```yaml
patched_versions: []
```

**Expected Derived Variables:**

```yaml
patch_availability: 'No patch available'
patched_versions_list: 'Not available'
compensating_controls_content: '[Detailed compensating controls content]'
```

**Expected Outcome:**

- Section 9 provides detailed compensating controls
- Section 8 recommends workarounds instead of patching
- Priority may be higher due to lack of patch

**Quality Gates:**

- [x] Section 9 has substantive compensating controls
- [x] Section 8 addresses lack of patch
- [x] Priority rationale mentions no patch available

---

### TC-009: Multiple ATT&CK Techniques Test

**Purpose:** Validate Section 7 with multiple MITRE ATT&CK techniques

**Input Data:**

```yaml
attack_mapping:
  tactics:
    - Initial Access
    - Execution
    - Persistence
    - Privilege Escalation
  techniques:
    - T1190 - Exploit Public-Facing Application
    - T1059 - Command and Scripting Interpreter
    - T1053 - Scheduled Task/Job
    - T1068 - Exploitation for Privilege Escalation
    - T1078 - Valid Accounts
```

**Expected Derived Variables:**

```yaml
attack_tactics_list: "- Initial Access\n- Execution\n- Persistence\n- Privilege Escalation"
attack_techniques_list: "- T1190 - Exploit Public-Facing Application\n- T1059 - Command and Scripting Interpreter\n- T1053 - Scheduled Task/Job\n- T1068 - Exploitation for Privilege Escalation\n- T1078 - Valid Accounts"
```

**Expected Outcome:**

- Section 7 lists all 4 tactics
- Section 7 lists all 5 techniques with T-numbers
- Detection implications address multiple techniques
- Defensive recommendations comprehensive

**Quality Gates:**

- [x] At least one MITRE ATT&CK tactic identified (4 tactics)
- [x] All techniques listed with T-numbers
- [x] Detection implications provided
- [x] Defensive recommendations provided

---

### TC-010: Markdown Formatting Test

**Purpose:** Validate markdown syntax and formatting

**Input Data:**
Same as TC-001 (complete data)

**Validation Checks:**

1. **Heading Structure:**
   - H1: Document title (from output.title)
   - H2: All 12 section titles
   - No heading level skips

2. **Table Formatting:**
   - Section 3: Severity Metrics table has 3 columns
   - Section 4: Affected Systems table has 4 columns
   - Proper header separator (|---|---|---|)
   - All rows aligned

3. **List Formatting:**
   - Bullet lists use `-` prefix
   - Numbered lists use `1.`, `2.`, etc.
   - Proper indentation for nested lists

4. **Links:**
   - All reference URLs formatted as markdown links: `[Text](URL)`
   - All URLs valid and accessible

5. **Bold/Emphasis:**
   - Field labels use **bold** (`**Label:**`)
   - Severity levels emphasized (`**Critical**`, `**P1**`)

6. **Code Blocks:**
   - CVSS vector strings in plain text (not code blocks)
   - No stray backticks

**Expected Outcome:**

- Valid markdown (no syntax errors)
- Renders correctly in markdown viewer
- Professional formatting throughout
- Human-readable and well-organized

**Quality Gates:**

- [x] Valid markdown syntax
- [x] Proper heading hierarchy
- [x] Tables render correctly
- [x] All links functional
- [x] Formatting consistent

---

## Validation Methodology

### YAML Template Validation

**Validation against BMAD Template Spec:**

1. Load `security-enrichment-tmpl.yaml`
2. Parse YAML structure
3. Validate required fields:
   - `template.id` present
   - `template.name` present
   - `template.version` present
   - `template.output.format` = "markdown"
   - `template.output.filename` present
   - `template.output.title` present
4. Validate workflow configuration:
   - `workflow.mode` = "automated"
   - No `workflow.elicitation` (not needed for automated mode)
5. Validate sections array:
   - 12 sections present
   - Each section has `id`, `title`, `instruction`, `template`
   - All section IDs unique
6. Validate variable references:
   - All `{{variable}}` syntax correct
   - No Handlebars iteration syntax (`{{#each}}`)
   - No invalid variable characters

### Variable Substitution Testing

**Process:**

1. Load template
2. Inject test data (from test case)
3. Process template:
   - Substitute all `{{variable}}` placeholders
   - Compute derived variables
   - Render each section template
4. Validate output:
   - No unsubstituted `{{variable}}` markers
   - All sections have content
   - Derived variables computed correctly

### Markdown Output Validation

**Tools:**

- Markdown linter (markdownlint)
- Markdown parser
- Manual review

**Checks:**

- Syntax validation (no errors)
- Rendering preview
- Link validation
- Table formatting

### Quality Gates Validation

**Automated Checks:**

1. **Section Count:** Count H2 headings = 12
2. **Executive Summary Length:** Count sentences in Section 1 = 2-3
3. **CVSS Range:** Parse CVSS score, validate 0.0 ≤ score ≤ 10.0
4. **EPSS Range:** Parse EPSS score, validate 0.0 ≤ score ≤ 1.0 or "Not available"
5. **KEV Status:** Validate status ∈ ["Listed", "Not Listed"]
6. **ATT&CK Tactics:** Count tactics > 0
7. **Priority Level:** Validate priority ∈ ["P1", "P2", "P3", "P4", "P5"]
8. **Priority Rationale:** Check rationale length > 50 characters
9. **Source Count:** Count references ≥ 3

---

## Test Execution

### Manual Test Execution

**For each test case:**

1. Prepare input data (from test case specification)
2. Load template: `expansion-packs/bmad-1898-engineering/templates/security-enrichment-tmpl.yaml`
3. Process template with input data
4. Generate markdown output
5. Validate output against expected outcome
6. Check quality gates
7. Document results

### Automated Test Execution

**Future Enhancement:** Create automated test runner that:

1. Loads all test cases from this file
2. Processes template with each test case data
3. Validates output against quality gates
4. Generates test report

---

## Test Results

_To be populated during test execution_

| Test Case | Status | Quality Gates | Notes |
| --------- | ------ | ------------- | ----- |
| TC-001    |        |               |       |
| TC-002    |        |               |       |
| TC-003    |        |               |       |
| TC-004    |        |               |       |
| TC-005    |        |               |       |
| TC-006    |        |               |       |
| TC-007    |        |               |       |
| TC-008    |        |               |       |
| TC-009    |        |               |       |
| TC-010    |        |               |       |

**Legend:**

- ✅ Pass
- ❌ Fail
- ⚠️ Partial Pass
- ⏭️ Skipped

---

## Integration Tests

### Story 1.2 → 1.3 → 1.4 Integration

**Test:** End-to-end workflow from JIRA ticket to enrichment document

**Steps:**

1. Read JIRA ticket (Story 1.2 task: read-jira-ticket.md)
   - Extract: CVE ID, affected systems, ACR, exposure
2. Research CVE (Story 1.3 task: research-cve.md)
   - Extract: CVSS, EPSS, KEV, exploits, ATT&CK mapping
3. Merge data from Steps 1-2
4. Process enrichment template (Story 1.4 template: security-enrichment-tmpl.yaml)
5. Generate enrichment markdown document

**Expected Outcome:**

- Complete enrichment document with all 12 sections populated
- Data from JIRA (Step 1) appears in Section 4 (Affected Systems)
- Data from CVE research (Step 2) appears in Sections 1-3, 5-8, 11
- Derived variables computed correctly
- All quality gates pass

---

## Issues and Defects

_To be populated during test execution_

| Issue ID | Test Case | Severity | Description | Resolution |
| -------- | --------- | -------- | ----------- | ---------- |
|          |           |          |             |            |

---

## Sign-off

**Test File Created:** 2024-11-08
**Test File Author:** James (Dev Agent)
**Story:** 1.4 Structured Enrichment Documentation
**Template Version:** 1.0

**Next Steps:**

1. Execute all 10 test cases
2. Document test results
3. Fix any identified defects
4. Re-test failures
5. Mark story tasks as complete

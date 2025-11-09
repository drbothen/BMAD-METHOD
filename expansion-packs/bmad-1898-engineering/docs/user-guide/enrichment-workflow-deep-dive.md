# Security Alert Enrichment Workflow: Deep Dive

## Overview

The Security Alert Enrichment Workflow is an 8-stage automated process that transforms basic security alerts into comprehensive, actionable intelligence packages. This workflow leverages AI-powered research, multiple data sources, and structured analysis to provide security teams with everything needed to understand, prioritize, and remediate vulnerabilities.

**Workflow ID:** `security-alert-enrichment-v1`

**Estimated Duration:** 10-15 minutes (95th percentile)

**Prerequisites:**

- JIRA ticket containing CVE reference
- Atlassian MCP configured and authenticated
- Perplexity MCP configured with API access
- Security Analyst agent activated
- Write permissions to local enrichment directories

**Success Metrics:**

- Total workflow time < 15 minutes
- All 8 stages complete successfully
- Quality score ≥ 75%
- All authoritative sources cited

## Workflow Architecture

The enrichment workflow follows a linear progression through 8 specialized stages, with each stage building upon the outputs of previous stages:

```
Stage 1: Triage & Context Extraction (1-2 min)
    ↓ CVE ID, Affected Systems, Initial Context
Stage 2: AI-Assisted CVE Research (3-10 min)
    ↓ CVSS, EPSS, KEV, Patches, Exploits, ATT&CK Suggestions
Stage 3: Business Context Assessment (2-3 min)
    ↓ ACR, Exposure, Business Impact
Stage 4: Remediation Planning (2-3 min)
    ↓ Remediation Steps, Workarounds, Controls
Stage 5: MITRE ATT&CK Mapping (1-2 min)
    ↓ Tactics, Techniques (T-numbers), Detection Guidance
Stage 6: Multi-Factor Priority Assessment (1-2 min)
    ↓ Priority (P1-P5), Rationale, SLA
Stage 7: Structured Documentation (1 min)
    ↓ 12-Section Enrichment Document
Stage 8: JIRA Update & Validation (1-2 min)
    ✓ Enriched Ticket, Local Files, Metrics
```

**Key Design Principles:**

- **Progressive enrichment:** Each stage adds value independently
- **Resume capability:** Workflow can be interrupted and resumed from any stage
- **Adaptive performance:** Tool selection and depth adjust based on severity
- **Quality assurance:** Built-in validation and quality scoring

---

## Stage 1: Triage & Context Extraction

**Duration:** 1-2 minutes

### Purpose

Extract the CVE identifier and initial context from the JIRA ticket to establish the foundation for enrichment.

### Inputs

| Input          | Source             | Format                          | Required |
| -------------- | ------------------ | ------------------------------- | -------- |
| JIRA Ticket ID | User or automation | PROJECT-NUMBER (e.g., AOD-1234) | Yes      |

### Actions

1. Call `mcp__atlassian__getJiraIssue` with the ticket ID
2. Extract CVE ID from ticket summary or description using regex pattern: `CVE-\d{4}-\d{4,}`
3. Parse affected systems from custom field `affected_systems` or description text
4. Extract initial severity if present in ticket fields
5. Retrieve Asset Criticality Rating (ACR) from custom field `asset_criticality_rating`
6. Retrieve System Exposure classification from custom field `system_exposure`
7. Capture ticket metadata (reporter, created date, project key)

### Outputs

- **CVE ID:** Validated CVE identifier (e.g., `CVE-2024-1234`)
- **Affected Systems:** List of system names/IPs
- **Initial Context:** Severity, ACR, Exposure (if available in ticket)
- **Ticket Metadata:** Reporter, creation timestamp, project

### Success Criteria

- ✅ CVE ID successfully extracted and validated
- ✅ JIRA ticket accessible (no authentication/permission errors)
- ✅ Affected systems identified (or marked as "TBD")

### Error Handling

| Error                   | Resolution                                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| **CVE Not Found**       | Prompt user: "CVE ID not found in ticket. Please provide CVE ID or vulnerability description:" |
| **Ticket Not Found**    | Verify ticket ID format (PROJECT-NUMBER), check JIRA permissions, retry with corrected ID      |
| **Permission Denied**   | Verify API token has JIRA read permissions, check project access settings                      |
| **Multiple CVEs Found** | Extract all CVEs, prompt user to select which to enrich, or enrich all sequentially            |

### Performance Optimization

- **Pre-validation:** Validate ticket ID format (PROJECT-NUMBER) before calling MCP to avoid wasted API calls
- **Batch enrichment:** When enriching multiple tickets, use `mcp__atlassian__searchJiraIssues` to fetch all at once
- **Caching:** Cache ticket data for 5 minutes to avoid redundant fetches if workflow is re-run

### Common Issues

**Issue:** Regex fails to match non-standard CVE format (e.g., "CVE 2024 1234" with spaces)
**Resolution:** Normalize input by removing spaces and inserting hyphens before pattern matching

**Issue:** Affected systems embedded in unstructured description text
**Resolution:** Use AI-assisted extraction or prompt user for manual entry, flag ticket for custom field population

**Issue:** Ticket created before custom fields were added (missing ACR/Exposure)
**Resolution:** Continue with Stage 1, fields will be populated in Stage 3 with defaults or user input

---

## Stage 2: AI-Assisted CVE Research

**Duration:** Variable (1-10 minutes depending on severity)

- Critical (CVSS ≥ 9.0): 5-10 minutes
- High (CVSS 7.0-8.9): 3-5 minutes
- Medium/Low (CVSS < 7.0): 1-2 minutes

### Purpose

Conduct comprehensive AI-powered research to gather technical vulnerability intelligence from authoritative sources.

### Inputs

| Input         | Source                 | Required |
| ------------- | ---------------------- | -------- |
| CVE ID        | Stage 1                | Yes      |
| CVSS Severity | Stage 1 (if available) | No       |

### Actions

1. **Select Perplexity Research Tool** based on severity:
   - **CVSS 9.0-10.0 (Critical):** `mcp__perplexity__deep_research` - Comprehensive multi-source analysis (5-10 min)
   - **CVSS 7.0-8.9 (High):** `mcp__perplexity__reason` - Analytical reasoning (3-5 min)
   - **CVSS < 7.0 or Unknown:** `mcp__perplexity__search` - Quick search (1-2 min)

2. **Construct Research Query:**

   ```
   CVE-{cve_id} vulnerability comprehensive analysis:
   - CVSS v3.1 score and vector string
   - EPSS exploitation probability score
   - CISA Known Exploited Vulnerabilities (KEV) catalog status
   - Affected product versions (full version ranges)
   - Patched versions (specific version numbers)
   - Exploit availability (PoC, active exploitation, exploit code published)
   - Active exploitation status (observed in wild, threat actor attribution)
   - MITRE ATT&CK framework mapping (tactics and techniques with T-numbers)
   - Remediation guidance (patch instructions, workarounds, compensating controls)
   - Authoritative sources (NIST NVD, CISA, vendor advisories, CVE.org)
   ```

3. **Execute Perplexity Research** with selected tool
4. **Parse and Structure Findings:**
   - Extract CVSS score and validate range (0.0-10.0)
   - Extract EPSS score and convert to percentage (0.0-100.0%)
   - Identify KEV status (Yes/No, date added if applicable)
   - Parse affected and patched versions
   - Classify exploit status (Active/PoC/None/Unknown)
   - Extract MITRE ATT&CK suggestions
5. **Collect Authoritative Source URLs** (NVD, CISA, vendor advisories)

### Outputs

- **CVSS Score:** Base score (0.0-10.0) and vector string (e.g., `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)
- **EPSS Score:** Exploitation probability percentage (0.0-100.0%)
- **KEV Status:** CISA Known Exploited Vulnerability catalog inclusion (Yes/No, date)
- **Affected Versions:** Product name and version ranges (e.g., "Apache Log4j 2.0-2.14.1")
- **Patched Versions:** Specific fixed versions (e.g., "2.15.0, 2.12.2, 2.3.1")
- **Exploit Status:** Active/PoC/None/Unknown with details
- **Threat Intelligence:** Active exploitation evidence, threat actor attribution
- **MITRE ATT&CK Suggestions:** Preliminary tactics and techniques
- **Authoritative Sources:** List of URLs (NVD, CISA, vendor advisories)

### Success Criteria

- ✅ CVSS score obtained and validated (0.0-10.0 range)
- ✅ Patch status determined (patched version identified OR "no patch available" documented)
- ✅ At least 3 authoritative sources cited
- ✅ Research completed within 2× expected duration for severity level

### Error Handling

| Error                           | Resolution                                                                                      |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Perplexity Timeout**          | Retry with simplified query (reduce detail requirements), consider fallback to faster tool      |
| **Rate Limiting**               | Wait 30 seconds, retry with exponential backoff (30s, 60s, 120s)                                |
| **Insufficient Data (New CVE)** | Document as "Preliminary analysis - awaiting NVD publication", use vendor advisory if available |
| **CVSS Not Available**          | Estimate from description severity keywords or mark as "TBD - pending NVD analysis"             |
| **No Patch Available**          | Proceed with workarounds and compensating controls only, flag in remediation section            |
| **Conflicting CVSS**            | Document both NVD and vendor scores, explain discrepancy, use NVD as primary                    |

### Performance Optimization

**Strategy 1: Adaptive Tool Selection**

- For P4/P5 (Low/Trivial priority): Always use `search` tool regardless of CVSS to prioritize speed over depth
- Override severity-based selection when batch enriching lower-priority tickets

**Strategy 2: Caching**

- Cache research results for identical CVEs (5-minute TTL)
- For related CVEs affecting same product, reuse vendor advisory URLs and general product context

**Strategy 3: Query Optimization**

- Reduce query complexity for lower-priority tickets (remove ATT&CK mapping request)
- Focus on core metrics (CVSS, EPSS, KEV, patch status) for quick enrichments

**Strategy 4: Parallel Research**

- When enriching multiple tickets with different CVEs, run Perplexity queries in parallel (respecting rate limits)

### Common Issues

**Issue:** Perplexity returns generic vulnerability information instead of CVE-specific details
**Resolution:** Add "CVE-{id} specific details only" to query, explicitly request version numbers and patch info

**Issue:** EPSS score is outdated (>7 days old)
**Resolution:** Note age in enrichment, flag for re-check, consider querying FIRST.org EPSS API directly

**Issue:** Conflicting information between NVD and vendor advisory
**Resolution:** Document both sources, explain discrepancy, prefer vendor for patch info and NVD for CVSS

**Issue:** Research returns "CVE reserved but not published"
**Resolution:** Escalate to manual research, use vendor advisory as sole source, document publication status

---

## Stage 3: Business Context Assessment

**Duration:** 2-3 minutes

### Purpose

Assess the business impact of the vulnerability by analyzing asset criticality, system exposure, and affected business processes.

### Inputs

| Input              | Source                  | Required  |
| ------------------ | ----------------------- | --------- |
| Affected Systems   | Stage 1                 | Yes       |
| CVE Intelligence   | Stage 2                 | Yes       |
| JIRA Custom Fields | Stage 1 (ACR, Exposure) | Preferred |

### Actions

1. **Retrieve Asset Criticality Rating (ACR):**
   - Check JIRA custom field `asset_criticality_rating`
   - If not in JIRA, check `expansion-packs/bmad-1898-engineering/config.yaml` for system-specific defaults
   - If unavailable, prompt user or default to "Medium" (conservative)

2. **Retrieve System Exposure Classification:**
   - Check JIRA custom field `system_exposure`
   - If not in JIRA, infer from system name patterns (e.g., "web-prod" → Internet)
   - If unavailable, prompt user or default to "Internal" (safer assumption)

3. **Assess Business Impact:**
   - High ACR + Internet Exposure + RCE/SQLi → Critical business impact
   - Medium ACR + Internal + Info Disclosure → Moderate business impact
   - Consider vulnerability type (RCE > Auth Bypass > XSS > Info Disclosure)

4. **Identify Affected Business Processes:**
   - Map systems to business functions (e.g., "prod-web-01" → "E-commerce checkout")
   - Use CMDB data if available, otherwise infer from system naming

5. **Document Business Impact:**
   - Write 2-3 sentence summary in non-technical language
   - Focus on potential business consequences (downtime, data breach, compliance)

### Outputs

- **Asset Criticality Rating:** Critical/High/Medium/Low
- **System Exposure:** Internet/Internal/Isolated
- **Business Impact Summary:** Non-technical description (2-3 sentences)
- **Affected Business Processes:** List of business functions
- **Stakeholders to Notify:** Business owners, compliance team (if applicable)

### Success Criteria

- ✅ ACR determined (from JIRA, config, default, or user input)
- ✅ System Exposure classified
- ✅ Business impact articulated in clear, stakeholder-friendly language

### Error Handling

| Error                                | Resolution                                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------------- |
| **ACR Unknown**                      | Default to "Medium", document assumption in enrichment, flag JIRA ticket for ACR population |
| **Exposure Unknown**                 | Default to "Internal" (safer than Internet assumption), flag for manual verification        |
| **Business Process Unknown**         | Use generic based on system type (e.g., "Web server: customer-facing services")             |
| **Multiple Systems, Different ACRs** | Use highest ACR for conservative priority assignment, note variance in enrichment           |

### Performance Optimization

**Pre-Population:** Configure triage team to populate ACR and Exposure custom fields during ticket creation (eliminates Stage 3 prompts)

**Asset Inventory Integration:** Maintain asset inventory mapping in `config.yaml`:

```yaml
asset_mappings:
  prod-web-01:
    acr: High
    exposure: Internet
    business_process: E-commerce Checkout
  db-internal-05:
    acr: Critical
    exposure: Internal
    business_process: Customer Database
```

**CMDB Integration:** If CMDB available, query asset data via API to auto-populate ACR and Exposure

### Common Issues

**Issue:** Multiple affected systems with different Asset Criticality Ratings
**Resolution:** Use the highest ACR for priority calculation (conservative approach), document all ACRs in enrichment

**Issue:** System in DMZ with ambiguous exposure classification
**Resolution:** Treat as "Internet" for safety (conservative priority), document actual network topology in enrichment

**Issue:** System name provides no context (e.g., "server-42")
**Resolution:** Prompt user for business process, flag ticket for system naming improvement

---

## Stage 4: Remediation Planning

**Duration:** 2-3 minutes

### Purpose

Develop actionable remediation guidance including patches, workarounds, and compensating controls.

### Inputs

| Input                                   | Source  |
| --------------------------------------- | ------- |
| CVE Intelligence (patches, workarounds) | Stage 2 |
| Business Context (ACR, constraints)     | Stage 3 |

### Actions

1. **Identify Primary Remediation:**
   - Extract patch version from Stage 2 research
   - Document upgrade path (e.g., "Upgrade from 2.14.1 to 2.15.0")
   - Include installation method (package manager, binary, source)

2. **Research Workarounds** (if patch not immediately applicable):
   - Identify vendor-recommended temporary mitigations
   - Assess workaround effectiveness and limitations

3. **Identify Compensating Controls:**
   - Network segmentation (isolate vulnerable systems)
   - WAF rules (block exploit patterns)
   - Access controls (restrict vulnerable service access)
   - Monitoring (detect exploitation attempts)

4. **Create Step-by-Step Remediation Guidance:**
   - Provide specific commands where possible
   - Include pre-requisites and dependencies
   - Document expected downtime or service impact

5. **Add Verification Steps:**
   - How to confirm patch installation (version check command)
   - How to validate vulnerability is fixed (re-scan, test)

6. **Document Business Impact of Remediation:**
   - Estimated downtime
   - Testing requirements
   - Rollback plan

### Outputs

- **Primary Remediation:** Patch version and upgrade instructions
- **Workaround Procedures:** Temporary mitigation steps (if patch delayed)
- **Compensating Controls:** Interim protection measures (WAF, network rules, access controls)
- **Remediation Steps:** Actionable, specific instructions
- **Verification Steps:** How to confirm successful remediation
- **Estimated Effort:** Time required, downtime expected

### Success Criteria

- ✅ Remediation guidance is actionable and specific (not generic "apply patch")
- ✅ At least one remediation path provided (patch, workaround, or compensating controls)
- ✅ Verification steps included

### Error Handling

| Error                                | Resolution                                                                                        |
| ------------------------------------ | ------------------------------------------------------------------------------------------------- |
| **No Patch Available**               | Focus on workarounds and compensating controls, document as "Mitigation only - no patch released" |
| **Vendor Advisory Missing**          | Use generic upgrade guidance based on patch version, flag for vendor clarification                |
| **Breaking Changes in Patch**        | Document migration path, testing requirements, rollback plan, escalate to change advisory board   |
| **Patch Conflicts with Environment** | Identify conflicts, provide alternative remediation (older patch version, workarounds)            |

### Performance Optimization

**Template Library:** Maintain remediation templates for common vulnerability types:

- RCE vulnerabilities → Standard patch + network segmentation
- SQLi vulnerabilities → Patch + WAF rules + database access review
- Auth bypass → Patch + MFA enforcement + access audit

**Vendor Documentation Cache:** Cache vendor security advisory URLs and patch procedures by product

**Leverage Stage 2 Research:** Perplexity research already includes remediation guidance—extract and structure rather than re-research

### Common Issues

**Issue:** Patch requires major version upgrade with breaking changes
**Resolution:** Document full migration path, testing requirements, rollback plan; consider workarounds for short-term

**Issue:** Multiple remediation options available (patch, workaround, config change)
**Resolution:** Prioritize by effort vs. risk reduction, recommend primary approach, list alternatives

**Issue:** Remediation requires third-party dependency updates
**Resolution:** Document full dependency chain, provide complete upgrade sequence

---

## Stage 5: MITRE ATT&CK Mapping

**Duration:** 1-2 minutes

### Purpose

Map the vulnerability to MITRE ATT&CK framework tactics and techniques to inform detection and defense strategies.

### Inputs

| Input                                                | Source                        |
| ---------------------------------------------------- | ----------------------------- |
| CVE Intelligence (vulnerability type, attack vector) | Stage 2                       |
| MITRE ATT&CK Suggestions                             | Stage 2 (Perplexity research) |

### Actions

1. **Identify Vulnerability Type:**
   - Classify: RCE, SQLi, XSS, Auth Bypass, Privilege Escalation, Info Disclosure, Deserialization, etc.

2. **Map to Primary MITRE ATT&CK Tactic:**
   - RCE, Deserialization, Exploit → **Initial Access** or **Execution**
   - SQLi, Path Traversal, File Inclusion → **Initial Access** or **Discovery**
   - Privilege Escalation vulnerabilities → **Privilege Escalation**
   - Auth Bypass, Credential Issues → **Credential Access** or **Defense Evasion**
   - Info Disclosure → **Collection** or **Discovery**

3. **Map to Specific Techniques with T-numbers:**
   - RCE via public-facing web app → **T1190** (Exploit Public-Facing Application)
   - Auth bypass → **T1078** (Valid Accounts) or **T1110** (Brute Force)
   - Deserialization → **T1203** (Exploitation for Client Execution)
   - SQLi → **T1190** + **T1213** (Data from Information Repositories)
   - Local privilege escalation → **T1068** (Exploitation for Privilege Escalation)

4. **Validate T-numbers:**
   - Cross-reference against [MITRE ATT&CK Matrix](https://attack.mitre.org/)
   - Verify T-number format (T#### with 4 digits)

5. **Add Detection Implications:**
   - What log sources to monitor (WAF, IDS, application logs)
   - What signatures or patterns to detect
   - What behaviors to alert on

6. **Add Defense Recommendations:**
   - Aligned with ATT&CK mitigations
   - Specific to mapped techniques

### Outputs

- **ATT&CK Tactics:** 1-3 tactics (e.g., Initial Access, Execution)
- **ATT&CK Techniques:** 1-5 techniques with T-numbers (e.g., T1190, T1059)
- **Detection Implications:** Log sources, signatures, behaviors to monitor
- **Defense Recommendations:** Mitigations aligned with ATT&CK framework

### Success Criteria

- ✅ At least 1 tactic identified
- ✅ At least 1 technique with valid T-number
- ✅ Detection implications provided

### Error Handling

| Error                                | Resolution                                                                              |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| **Unfamiliar Vulnerability Type**    | Use general external/internal mapping: T1190 for external, T1068 for local              |
| **Mapping Uncertainty**              | Document multiple possible techniques, note uncertainty in enrichment                   |
| **Invalid T-number from Perplexity** | Validate against MITRE ATT&CK website, correct format (add T prefix), update if invalid |
| **Technique Deprecated**             | Check MITRE ATT&CK for replacement technique, use updated T-number                      |

### Performance Optimization

**Mapping Library:** Maintain vulnerability-type-to-T-number mapping:

```yaml
vuln_mappings:
  RCE_public_facing:
    tactics: [Initial Access, Execution]
    techniques: [T1190, T1059]
  SQLi:
    tactics: [Initial Access, Discovery]
    techniques: [T1190, T1213]
  Auth_Bypass:
    tactics: [Credential Access, Defense Evasion]
    techniques: [T1078, T1550]
```

**Leverage Perplexity Research:** Use ATT&CK suggestions from Stage 2 as starting point, validate quickly rather than re-research

**Low-Priority Fast Path:** For P4/P5 tickets, use generic mappings based on vulnerability type (skip detailed analysis)

### Common Issues

**Issue:** Multiple applicable techniques for a single vulnerability
**Resolution:** Include all relevant techniques, prioritize most likely attack path in description

**Issue:** T-number format incorrect (missing "T" prefix or wrong digit count)
**Resolution:** Auto-correct to standard format (T#### with 4 digits)

**Issue:** Perplexity suggests outdated or deprecated technique
**Resolution:** Validate against current MITRE ATT&CK matrix, use replacement technique if available

---

## Stage 6: Multi-Factor Priority Assessment

**Duration:** 1-2 minutes

### Purpose

Calculate vulnerability priority using multiple risk factors and assign appropriate SLA deadline.

### Inputs

| Input                          | Source  |
| ------------------------------ | ------- |
| CVSS Score                     | Stage 2 |
| EPSS Score                     | Stage 2 |
| KEV Status                     | Stage 2 |
| Asset Criticality Rating (ACR) | Stage 3 |
| System Exposure                | Stage 3 |
| Exploit Status                 | Stage 2 |

### Actions

1. **Apply Priority Algorithm:**
   - **P1 (Critical):**
     - (CVSS ≥ 9.0 AND KEV = Yes) OR
     - (CVSS ≥ 9.0 AND Exposure = Internet AND ACR = Critical AND Exploit = Active)

   - **P2 (High):**
     - (CVSS ≥ 7.0 AND ACR ≥ High) OR
     - (CVSS ≥ 9.0 AND (ACR = Medium OR ACR = Low)) OR
     - (KEV = Yes AND ACR ≥ Medium)

   - **P3 (Medium):**
     - (CVSS 4.0-6.9 AND ACR = Medium) OR
     - (CVSS 7.0-8.9 AND ACR = Low) OR
     - (CVSS ≥ 7.0 AND Exposure = Internal AND ACR = Medium)

   - **P4 (Low):**
     - CVSS < 4.0 OR
     - (Exposure = Isolated AND Exploit = None) OR
     - (ACR = Low AND CVSS < 7.0)

   - **P5 (Trivial):**
     - CVSS < 4.0 AND ACR = Low AND Exposure = Isolated AND No remediation available

2. **Generate Priority Rationale:**
   - Explain all contributing factors in clear language
   - Example: "P1: CVSS 9.8 (Critical severity) + CISA KEV listed (actively exploited) + Internet-exposed High criticality asset + Active exploitation observed in wild"

3. **Calculate SLA Deadline:**
   - P1: 24 hours from ticket creation
   - P2: 7 days from ticket creation
   - P3: 30 days from ticket creation
   - P4: 90 days from ticket creation
   - P5: Best effort (no SLA)

4. **Validate Priority Assignment:**
   - Sanity check for edge cases
   - Flag unusual combinations for manual review

5. **Generate Risk Summary:**
   - 1-2 sentence summary of overall risk posture
   - Example: "Critical risk: Publicly exploitable RCE on Internet-facing production system with active exploitation in wild."

### Outputs

- **Priority Level:** P1/P2/P3/P4/P5
- **Priority Rationale:** Explanation of all contributing factors
- **SLA Deadline:** Timestamp (ISO 8601 format)
- **Risk Summary:** 1-2 sentence overall risk assessment

### Success Criteria

- ✅ Priority assigned with clear rationale
- ✅ Rationale references all major contributing factors (CVSS, KEV, ACR, Exposure)
- ✅ SLA deadline calculated correctly based on priority

### Error Handling

| Error                   | Resolution                                                                                          |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| **Missing Factors**     | Use conservative defaults (assume higher risk): Unknown ACR → High, Unknown Exposure → Internet     |
| **Conflicting Signals** | Document conflict in rationale, use most conservative priority (escalate when uncertain)            |
| **Edge Cases**          | Flag for manual review if automated logic produces unexpected result (e.g., P1 for isolated system) |
| **CVSS/ACR Mismatch**   | Document both factors, explain which drove priority decision                                        |

### Performance Optimization

**Pre-calculated Matrix:** Maintain priority lookup table for common factor combinations to eliminate calculation overhead

**Automated Decisioning:** For clear-cut cases (90% of tickets), apply algorithm without manual intervention

**Batch Calculation:** When enriching multiple tickets, calculate all priorities in single pass

### Common Issues

**Issue:** CVSS 6.9 vs 7.0 threshold edge case
**Resolution:** Apply algorithm strictly (6.9 is < 7.0), document in rationale that vulnerability is just below threshold

**Issue:** KEV = Yes but CVSS = Medium
**Resolution:** KEV status overrides lower CVSS (escalate priority), document in rationale that active exploitation drives urgency

**Issue:** Isolated system but CVSS 10.0
**Resolution:** Algorithm correctly assigns lower priority due to exposure, but flag for architectural review (why is critical vuln in isolated system?)

**Issue:** Conflicting priority expectations (stakeholder wants P1, algorithm says P3)
**Resolution:** Document algorithm result, provide override mechanism with justification requirement, log override for audit

---

## Stage 7: Structured Documentation

**Duration:** 1 minute (automated)

### Purpose

Generate comprehensive enrichment documentation using structured template with quality validation.

### Inputs

| Input               | Source     |
| ------------------- | ---------- |
| All Enrichment Data | Stages 1-6 |

### Actions

1. **Load Template:**
   - Template file: `templates/security-enrichment-tmpl.yaml`
   - Template contains 12 structured sections

2. **Populate Template Sections:**
   1. **Executive Summary:** 2-3 sentences covering CVE, CVSS, priority, SLA, affected systems
   2. **Vulnerability Details:** CVE ID, title, vulnerability type, affected versions
   3. **Severity Metrics:** CVSS score/vector, EPSS score, KEV status
   4. **Affected Systems & Versions:** System list, version details, exposure classification
   5. **Remediation Guidance:** Patch info, workarounds, compensating controls, verification steps
   6. **MITRE ATT&CK Mapping:** Tactics, techniques (T-numbers), detection implications
   7. **Business Impact Assessment:** ACR, business impact summary, affected processes
   8. **Threat Intelligence:** Exploit status, active exploitation evidence, threat actors
   9. **Verification & Testing:** Steps to confirm remediation success
   10. **References & Sources:** Authoritative source URLs (NVD, CISA, vendor advisories)
   11. **Related CVEs:** Associated vulnerabilities in same product/component
   12. **Analyst Notes:** Additional context, follow-up items, assumptions

3. **Validate Template Completeness:**
   - Check all 12 sections populated (non-empty)
   - Verify required fields present (CVE ID, CVSS, Priority, SLA)
   - Flag empty sections for completion

4. **Calculate Quality Score:**
   - **Completeness (40 points):** All 12 sections present
   - **Source Citations (30 points):** ≥ 3 authoritative sources linked
   - **Actionability (30 points):** Specific remediation steps provided
   - **Total:** 0-100 score

5. **Generate Markdown Document:**
   - Render template as formatted markdown
   - Apply consistent styling (headings, tables, code blocks)

### Outputs

- **Enrichment Markdown Document:** 12-section comprehensive analysis
- **Quality Score:** 0-100 (target: ≥ 75)
- **Validation Status:** Pass/Fail with gap list if failed

### Success Criteria

- ✅ All 12 sections populated
- ✅ Quality score ≥ 75%
- ✅ Executive summary present and concise

### Error Handling

| Error                    | Resolution                                                                                                                            |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Missing Section**      | Populate with "TBD - requires additional research" placeholder, flag for manual completion, reduce quality score                      |
| **Validation Failure**   | List missing sections, provide specific gaps, halt JIRA update until resolved                                                         |
| **Quality Score < 75%**  | List specific gaps (e.g., "Missing source citations", "Generic remediation"), suggest improvements, allow override with justification |
| **Template Parse Error** | Log template error, fall back to previous template version, notify admin                                                              |

### Performance Optimization

**Fully Automated:** Template processing requires no user interaction (all data from Stages 1-6)

**Parallel Section Generation:** If template engine supports, populate sections concurrently

**Template Caching:** Load template once per session, reuse for multiple enrichments

### Common Issues

**Issue:** Related CVEs section empty (no related vulnerabilities identified)
**Resolution:** Use placeholder "None identified at time of enrichment" rather than leaving blank

**Issue:** Verification section too generic ("Apply patch and re-scan")
**Resolution:** Auto-populate with specific commands when possible (e.g., "Run `java -version` to confirm upgrade to 2.15.0")

**Issue:** Quality score fails due to missing citations despite good content
**Resolution:** Adjust scoring weights or relax citation requirement for CVEs with limited public information

---

## Stage 8: JIRA Update & Validation

**Duration:** 1-2 minutes

### Purpose

Update JIRA ticket with enrichment findings, save local artifacts, and log metrics.

### Inputs

| Input                        | Source                                  |
| ---------------------------- | --------------------------------------- |
| Enrichment Markdown Document | Stage 7                                 |
| Priority Level               | Stage 6                                 |
| Structured Data              | Stages 1-6 (CVSS, EPSS, KEV, ACR, etc.) |

### Actions

1. **Post Enrichment as JIRA Comment:**
   - Tool: `mcp__atlassian__addCommentToJiraIssue`
   - Format: Markdown (JIRA renders markdown comments)
   - Content: Full 12-section enrichment document from Stage 7

2. **Update JIRA Custom Fields:**
   - Tool: `mcp__atlassian__updateJiraIssue`
   - Fields to update:
     - `cve_id`: CVE identifier (text)
     - `affected_systems`: Comma-separated system list (text)
     - `asset_criticality_rating`: ACR value (select)
     - `system_exposure`: Exposure classification (select)
     - `cvss_score`: CVSS base score (number)
     - `epss_score`: EPSS percentage (number)
     - `kev_status`: KEV catalog inclusion (select: Yes/No)
     - `exploit_status`: Exploitation status (select)

3. **Save Enrichment to Local File:**
   - Directory: `enrichments/`
   - Filename: `{ticket-id}-enrichment.md` (e.g., `AOD-1234-enrichment.md`)
   - Content: Same markdown document posted to JIRA

4. **Append Metrics to CSV:**
   - File: `metrics/enrichment-metrics.csv`
   - Columns: ticket_id, cve_id, analyst, start_time, end_time, duration_minutes, quality_score, priority, cvss, epss, kev
   - Purpose: Track workflow performance and quality over time

5. **Validate JIRA Update Success:**
   - Check API response status (HTTP 200/201 = success)
   - Verify comment ID returned
   - Confirm field update count matches expected

6. **Clean Up Workflow State:**
   - Delete state file: `.workflow-state/{ticket-id}.json`
   - State no longer needed after successful completion

### Outputs

- **JIRA Comment:** Enrichment posted successfully (comment ID returned)
- **JIRA Custom Fields:** 8 fields updated without errors
- **Local Enrichment File:** Saved to `enrichments/{ticket-id}-enrichment.md`
- **Metrics CSV Entry:** Appended to `metrics/enrichment-metrics.csv`
- **Workflow State:** Cleaned up (state file deleted)

### Success Criteria

- ✅ JIRA comment posted successfully (HTTP 200/201)
- ✅ All 8 custom fields updated without errors
- ✅ Local enrichment file saved successfully
- ✅ Metrics logged to CSV

### Error Handling

| Error                            | Resolution                                                                                                                             |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **JIRA Comment Post Failure**    | Save enrichment locally, provide user with manual copy instructions, retry with smaller comment if size issue                          |
| **Custom Field Update Failure**  | Identify specific field error (check API response), retry individual fields, skip fields with persistent errors (log for admin review) |
| **Permission Denied (403)**      | Verify API token has JIRA write permissions, check project-level permissions, escalate to JIRA admin                                   |
| **Field Validation Error (400)** | Check field type constraints (number vs. text), validate data format, adjust data before retry                                         |
| **Network Timeout**              | Retry with exponential backoff (3 attempts: 5s, 10s, 20s delay)                                                                        |
| **Comment Too Large (>32KB)**    | Truncate comment to summary with note "Full enrichment available in `enrichments/{ticket-id}-enrichment.md`", provide local file path  |

### Performance Optimization

**Batch Field Updates:** Use single `updateJiraIssue` call with multiple field updates rather than individual calls per field

**Parallel Operations:** Execute JIRA comment post and field updates concurrently if MCP supports (reduce latency)

**Async File I/O:** Write local enrichment file asynchronously (don't block on file system I/O)

**Pre-validate Data:** Check field formats before API call to avoid validation errors

### Common Issues

**Issue:** CVSS field expects number type but receives string "9.8"
**Resolution:** Type conversion before API call (parse string to float)

**Issue:** Custom field ID incorrect in `expansion-packs/bmad-1898-engineering/config.yaml`
**Resolution:** Verify field IDs in JIRA admin panel, update config.yaml with correct IDs

**Issue:** Comment too large due to verbose threat intelligence section
**Resolution:** Truncate verbose sections, provide full content in local file with link in comment

**Issue:** Field update succeeds but value not visible in JIRA UI
**Resolution:** Verify field is on ticket screen, check field permissions, confirm field type matches data

---

## Integration Points

### Atlassian MCP (JIRA Operations)

**MCP Server:** Atlassian Model Context Protocol

**Tools Used:**

| Tool                                    | Stage    | Purpose                                     |
| --------------------------------------- | -------- | ------------------------------------------- |
| `mcp__atlassian__getJiraIssue`          | Stage 1  | Read JIRA ticket to extract CVE and context |
| `mcp__atlassian__addCommentToJiraIssue` | Stage 8  | Post enrichment as JIRA comment             |
| `mcp__atlassian__updateJiraIssue`       | Stage 8  | Update custom fields with structured data   |
| `mcp__atlassian__searchJiraIssues`      | Optional | Batch enrichment (fetch multiple tickets)   |

**Configuration File:** `expansion-packs/bmad-1898-engineering/config.yaml`

**Configuration Requirements:**

```yaml
jira:
  cloud_id: 'your-atlassian-cloud-id'
  project_key: 'AOD' # Alert Operations Dashboard
  custom_fields:
    cve_id: 'customfield_10001'
    affected_systems: 'customfield_10002'
    asset_criticality_rating: 'customfield_10003'
    system_exposure: 'customfield_10004'
    cvss_score: 'customfield_10005'
    epss_score: 'customfield_10006'
    kev_status: 'customfield_10007'
    exploit_status: 'customfield_10008'
```

**Authentication:** API token or OAuth 2.0 (configured via MCP settings)

**Common API Error Codes:**

- **401 Unauthorized:** Authentication failed → Check API token validity
- **403 Forbidden:** Permission denied → Verify user has project access and field edit permissions
- **404 Not Found:** Ticket not found → Verify ticket ID format and project key
- **400 Bad Request:** Validation error → Check field type constraints and data format

**Rate Limiting:** Atlassian API limits: 10 requests/second (cloud), respect limits to avoid 429 errors

---

### Perplexity MCP (CVE Research)

**MCP Server:** Perplexity Model Context Protocol

**Tools Used:**

| Tool                             | Duration | Use Case                                  |
| -------------------------------- | -------- | ----------------------------------------- |
| `mcp__perplexity__search`        | 1-2 min  | Quick research (CVSS < 7.0, P4/P5)        |
| `mcp__perplexity__reason`        | 3-5 min  | Analytical research (CVSS 7.0-8.9, P2/P3) |
| `mcp__perplexity__deep_research` | 5-10 min | Comprehensive research (CVSS ≥ 9.0, P1)   |

**Tool Selection Logic:**

```
if CVSS >= 9.0 or Priority == P1:
    use deep_research (thorough multi-source analysis)
elif CVSS >= 7.0 or Priority in [P2, P3]:
    use reason (balanced depth and speed)
else:
    use search (quick lookup)
```

**Query Construction Best Practices:**

- Include specific CVE ID (e.g., "CVE-2024-1234")
- Request structured data (CVSS, EPSS, KEV, versions)
- Specify authoritative sources (NIST NVD, CISA, vendor)
- For critical vulnerabilities, request threat intelligence

**Rate Limiting:** Perplexity API limits vary by subscription tier, implement exponential backoff on 429 errors

**Fallback Strategy:** If Perplexity unavailable or rate-limited:

1. Manual research using NVD, CISA KEV, vendor advisories
2. Use cached results if CVE previously researched
3. Partial enrichment (document research limitation)

---

### Local File System

**Directory Structure:**

```
expansion-packs/bmad-1898-engineering/
├── enrichments/              # Enrichment markdown artifacts
│   ├── AOD-1234-enrichment.md
│   └── AOD-5678-enrichment.md
├── .workflow-state/          # Workflow resume state files
│   ├── AOD-1234.json
│   └── AOD-5678.json (auto-deleted after completion)
├── metrics/                  # Performance and quality metrics
│   └── enrichment-metrics.csv
└── config.yaml               # JIRA and workflow configuration
```

**Permissions Required:**

- Read access to `config.yaml`
- Write access to `enrichments/`, `.workflow-state/`, `metrics/`
- Directory creation permissions (if directories don't exist)

**File Formats:**

- Enrichment artifacts: Markdown (.md)
- Workflow state: JSON (.json)
- Metrics: CSV (.csv)

**Cleanup Policy:**

- Workflow state files: Auto-deleted after successful Stage 8 completion
- Orphaned state files (>24 hours old): Auto-cleaned by maintenance task
- Enrichment artifacts: Retained indefinitely (or per retention policy)
- Metrics CSV: Append-only, rotate monthly or per policy

---

### Configuration File (config.yaml)

**Location:** `expansion-packs/bmad-1898-engineering/config.yaml`

**Configuration Sections:**

**1. JIRA Configuration:**

```yaml
jira:
  cloud_id: 'your-cloud-id'
  project_key: 'AOD'
  custom_fields:
    cve_id: 'customfield_10001'
    # ... (all 8 custom fields)
```

**2. Priority Mapping:**

```yaml
priority_mapping:
  P1: '10001' # JIRA priority ID for Critical
  P2: '10002' # JIRA priority ID for High
  P3: '10003' # JIRA priority ID for Medium
  P4: '10004' # JIRA priority ID for Low
  P5: '10005' # JIRA priority ID for Trivial
```

**3. Default Values:**

```yaml
defaults:
  asset_criticality_rating: 'Medium'
  system_exposure: 'Internal'
```

**Validation Requirements:**

- YAML syntax valid
- Required fields present (cloud_id, project_key, custom_fields)
- Custom field IDs match JIRA configuration

**Troubleshooting:**

- If enrichment fails with "Field not found" → Verify custom_fields IDs in config.yaml match JIRA
- If priority update fails → Verify priority_mapping IDs match JIRA priority scheme

---

## Performance Optimization Guide

### Overview

The enrichment workflow can be optimized to reduce total duration by 30-50% through strategic improvements at each stage.

### Stage-Specific Optimizations

**Stage 1 Optimization:**

- ✅ Pre-validate ticket ID format before MCP call (saves failed API calls)
- ✅ Batch fetch tickets when enriching multiple (one API call vs. many)
- ✅ Cache ticket data for 5 minutes (avoid redundant fetches on retry)

**Stage 2 Optimization:**

- ✅ Adaptive tool selection: Use faster `search` for P4/P5 regardless of CVSS
- ✅ Cache research results for identical CVEs (5-minute TTL)
- ✅ Reuse vendor advisory URLs for related CVEs in same product
- ✅ Reduce query complexity for lower-priority tickets

**Stage 3 Optimization:**

- ✅ **Pre-populate JIRA custom fields** during triage (biggest time saver—eliminates prompts)
- ✅ Maintain asset inventory in `config.yaml` (system → ACR/Exposure mapping)
- ✅ Integrate with CMDB if available (auto-lookup asset data)

**Stage 4 Optimization:**

- ✅ Maintain remediation template library for common vulnerability types
- ✅ Cache vendor patch procedures by product
- ✅ Leverage Perplexity research from Stage 2 (avoid redundant research)

**Stage 5 Optimization:**

- ✅ Maintain vulnerability-type-to-T-number mapping library
- ✅ Use ATT&CK suggestions from Stage 2 as starting point (validate quickly)
- ✅ For P4/P5: Use generic mappings (skip detailed analysis)

**Stage 6 Optimization:**

- ✅ Pre-calculate priority matrix for common factor combinations
- ✅ Fully automate for clear-cut cases (90% of tickets)

**Stage 7 Optimization:**

- ✅ Fully automated (no user interaction required)
- ✅ Template caching (load once per session)

**Stage 8 Optimization:**

- ✅ Batch field updates in single API call
- ✅ Parallel JIRA operations (comment + fields) if MCP supports
- ✅ Async file I/O (don't block on writes)

### Cross-Stage Optimizations

**1. Batch Enrichment:**
When enriching multiple tickets:

- Fetch all tickets in single JIRA query (Stage 1)
- Run Perplexity research in parallel for different CVEs (Stage 2)
- Batch-update JIRA fields for all tickets (Stage 8)

**2. Intelligent Caching:**

- CVE research results (5-minute TTL)
- JIRA ticket data (5-minute TTL)
- Template files (session-level cache)
- Asset mappings (load once at startup)

**3. Priority-Based Depth:**
Adjust enrichment depth based on priority:

- **P1/P2:** Full 8-stage workflow, maximum detail
- **P3:** Standard workflow, moderate detail
- **P4/P5:** Fast-track workflow—use `search` tool, generic mappings, minimal analysis

**4. Parallel Processing:**
Where possible, execute independent operations concurrently:

- JIRA comment post + field updates (Stage 8)
- File writes + metric logging (Stage 8)

### Performance Targets

| Priority | Target Duration | Optimization Strategy                                             |
| -------- | --------------- | ----------------------------------------------------------------- |
| P1       | 12-15 minutes   | Full depth, `deep_research` tool, comprehensive analysis          |
| P2       | 8-12 minutes    | Standard depth, `reason` tool, complete workflow                  |
| P3       | 6-10 minutes    | Moderate depth, `reason` or `search` tool                         |
| P4       | 4-6 minutes     | Minimal depth, `search` tool, generic mappings, template defaults |
| P5       | 3-5 minutes     | Fast-track, `search` tool, skip optional sections                 |

### Measuring Performance

**Metrics to Track:**

- Total workflow duration (start to Stage 8 completion)
- Per-stage duration (identify bottlenecks)
- API call latency (JIRA, Perplexity)
- Cache hit rate (% of enrichments using cached data)

**Performance Dashboard:**
Review `metrics/enrichment-metrics.csv` to identify:

- Slowest stages (candidates for optimization)
- Tickets exceeding target duration
- Trends over time (performance degradation)

---

## Stage-Specific Troubleshooting

### Stage 1 Troubleshooting

| Issue                    | Symptoms                     | Resolution                                                                                                                                                                    |
| ------------------------ | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CVE Extraction Fails** | "CVE ID not found in ticket" | 1. Check ticket summary/description manually<br>2. Search for variations (CVE 2024 1234 with spaces)<br>3. Prompt user for CVE ID<br>4. Flag ticket for better CVE formatting |
| **Ticket Access Denied** | HTTP 403 error               | 1. Verify API token has JIRA read permissions<br>2. Check project-level access (user must be project member)<br>3. Verify ticket exists and is not restricted                 |
| **Multiple CVEs Found**  | Multiple regex matches       | 1. Extract all CVEs<br>2. Prompt user to select which to enrich<br>3. Offer batch enrichment (enrich all sequentially)                                                        |
| **ACR/Exposure Missing** | Custom fields empty          | 1. Proceed (fields populated in Stage 3)<br>2. Use defaults from config.yaml<br>3. Prompt user if defaults unavailable                                                        |

**Debug Steps:**

1. Test JIRA connectivity: Manually fetch ticket via MCP tool
2. Verify ticket ID format: Should be PROJECT-NUMBER (e.g., AOD-1234)
3. Check API token scope: Ensure read permissions granted
4. Test regex: Use test CVE string "CVE-2024-1234" to verify pattern

---

### Stage 2 Troubleshooting

| Issue                       | Symptoms                      | Resolution                                                                                                                                            |
| --------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Perplexity Timeout**      | Research exceeds 10 minutes   | 1. Retry with simplified query (reduce detail requirements)<br>2. Fall back to faster tool (`reason` → `search`)<br>3. Manual research if persistent  |
| **Rate Limiting**           | HTTP 429 error                | 1. Wait 30 seconds<br>2. Retry with exponential backoff<br>3. Check API usage quota                                                                   |
| **Insufficient CVE Data**   | "No NVD entry found"          | 1. Check if CVE is newly published (NVD delay common)<br>2. Use vendor advisory as sole source<br>3. Document as "Preliminary - awaiting NVD"         |
| **CVSS Not Available**      | Perplexity returns no CVSS    | 1. Check NVD directly (may not be in Perplexity yet)<br>2. Estimate from description (use vendor severity)<br>3. Mark as "TBD - pending NVD analysis" |
| **Conflicting CVSS Scores** | NVD says 7.5, vendor says 9.1 | 1. Document both scores in enrichment<br>2. Use NVD as primary for priority calculation<br>3. Explain discrepancy in analyst notes                    |

**Debug Steps:**

1. Test Perplexity connectivity: Run simple query "test"
2. Verify API key: Check MCP configuration
3. Manual NVD lookup: Visit https://nvd.nist.gov/vuln/detail/{CVE-ID}
4. Check CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

---

### Stage 3 Troubleshooting

| Issue                                | Symptoms                               | Resolution                                                                                                                                        |
| ------------------------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ACR Unknown**                      | Custom field empty, no config default  | 1. Default to "Medium" (conservative)<br>2. Document assumption in enrichment<br>3. Flag JIRA ticket for ACR population                           |
| **Exposure Ambiguous**               | System in DMZ or hybrid network        | 1. Default to "Internet" (safer assumption)<br>2. Document actual topology in enrichment<br>3. Flag for network architecture review               |
| **Multiple Systems, Different ACRs** | Ticket affects prod (High) + dev (Low) | 1. Use highest ACR (conservative priority)<br>2. Document all systems and their ACRs in enrichment<br>3. Consider splitting into separate tickets |
| **Business Process Unknown**         | Generic system name (server-42)        | 1. Use generic placeholder based on system type<br>2. Prompt user for business process<br>3. Flag for asset inventory improvement                 |

**Debug Steps:**

1. Check JIRA custom field values: Verify ACR/Exposure fields populated
2. Review config.yaml defaults: Confirm fallback values configured
3. Validate system naming: Check if naming convention provides context

---

### Stage 4 Troubleshooting

| Issue                               | Symptoms                        | Resolution                                                                                                                         |
| ----------------------------------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **No Patch Available**              | Vendor has not released fix     | 1. Focus on workarounds and compensating controls<br>2. Document as "Mitigation only - no patch"<br>3. Flag for vendor follow-up   |
| **Patch Requires Breaking Changes** | Major version upgrade needed    | 1. Document full migration path<br>2. Include testing requirements and rollback plan<br>3. Consider workarounds for short-term     |
| **Vendor Advisory Missing**         | No official guidance available  | 1. Use generic upgrade guidance based on patch version<br>2. Flag for vendor clarification<br>3. Document limitation in enrichment |
| **Conflicting Remediation Options** | Multiple patches or workarounds | 1. Prioritize by effort vs. risk reduction<br>2. Recommend primary approach<br>3. List alternatives in enrichment                  |

**Debug Steps:**

1. Check vendor security advisory page directly
2. Search vendor knowledge base for CVE ID
3. Review Perplexity research for remediation details

---

### Stage 5 Troubleshooting

| Issue                              | Symptoms                              | Resolution                                                                                                                                |
| ---------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Unfamiliar Vulnerability Type**  | Can't determine appropriate tactic    | 1. Use general mapping: T1190 (external) or T1068 (local)<br>2. Document uncertainty in enrichment<br>3. Flag for security analyst review |
| **Invalid T-Number**               | Perplexity suggests T12345 (5 digits) | 1. Validate against MITRE ATT&CK website<br>2. Correct format (T-numbers are T####)<br>3. Remove if invalid, use general mapping          |
| **Multiple Applicable Techniques** | Vuln maps to 5+ techniques            | 1. Include all relevant techniques<br>2. Prioritize most likely attack path<br>3. Document in order of likelihood                         |
| **Technique Deprecated**           | T-number no longer in ATT&CK          | 1. Check MITRE ATT&CK for replacement<br>2. Use updated technique<br>3. Document change in analyst notes                                  |

**Debug Steps:**

1. Validate T-numbers: https://attack.mitre.org/techniques/{T-number}/
2. Review ATT&CK tactics: https://attack.mitre.org/tactics/
3. Check technique descriptions for applicability

---

### Stage 6 Troubleshooting

| Issue                        | Symptoms                      | Resolution                                                                                                                                                    |
| ---------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Missing Priority Factors** | CVSS or ACR unavailable       | 1. Use conservative defaults (assume higher risk)<br>2. Document assumptions in rationale<br>3. Flag for data completion                                      |
| **Conflicting Signals**      | High CVSS but isolated system | 1. Apply algorithm strictly (isolation reduces priority)<br>2. Document conflict in rationale<br>3. Provide override option with justification                |
| **Edge Case Priority**       | CVSS 6.9 vs 7.0 threshold     | 1. Apply algorithm strictly (6.9 < 7.0)<br>2. Document in rationale that vuln is just below threshold<br>3. Note factors that could escalate                  |
| **KEV Overrides CVSS**       | KEV=Yes but CVSS=Medium       | 1. Escalate priority (KEV indicates active exploitation)<br>2. Document in rationale that exploitation drives urgency<br>3. Apply P1 or P2 based on algorithm |

**Debug Steps:**

1. Review priority algorithm in priority-framework.md
2. Validate all input factors (CVSS, EPSS, KEV, ACR, Exposure, Exploit)
3. Manually calculate priority to verify automated result

---

### Stage 7 Troubleshooting

| Issue                          | Symptoms                         | Resolution                                                                                                                                       |
| ------------------------------ | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Missing Template Section**   | Section empty or "TBD"           | 1. Populate with placeholder "TBD - requires additional research"<br>2. Reduce quality score<br>3. Flag for manual completion before JIRA update |
| **Validation Failure**         | Quality score < 75%              | 1. List specific gaps (missing citations, generic remediation)<br>2. Suggest improvements<br>3. Allow override with justification                |
| **Template Parse Error**       | YAML syntax error in template    | 1. Log template error details<br>2. Fall back to previous template version<br>3. Notify administrator to fix template                            |
| **Related CVEs Section Empty** | No related vulnerabilities found | 1. Use placeholder "None identified at time of enrichment"<br>2. Continue without error                                                          |

**Debug Steps:**

1. Validate template YAML: Check syntax at yamllint.com
2. Review stage outputs: Ensure all stages completed successfully
3. Check quality score breakdown: Identify specific gaps

---

### Stage 8 Troubleshooting

| Issue                         | Symptoms                          | Resolution                                                                                                                                                                           |
| ----------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **JIRA Comment Post Fails**   | HTTP error on comment creation    | 1. Save enrichment locally (enrichments/{ticket-id}-enrichment.md)<br>2. Provide manual copy instructions<br>3. Retry with smaller comment if size issue (truncate verbose sections) |
| **Custom Field Update Fails** | HTTP 400 validation error         | 1. Identify specific field error from API response<br>2. Check field type constraints (number vs. text)<br>3. Retry individual fields, skip persistent errors                        |
| **Permission Denied**         | HTTP 403 on JIRA update           | 1. Verify API token has write permissions<br>2. Check project-level permissions (edit issue required)<br>3. Escalate to JIRA administrator                                           |
| **Field Validation Error**    | "Field value does not match type" | 1. Validate data format (e.g., CVSS must be number not string)<br>2. Convert types before API call<br>3. Update config.yaml if field ID incorrect                                    |
| **Comment Too Large**         | Comment exceeds 32KB limit        | 1. Truncate to executive summary + key findings<br>2. Add note "Full enrichment: enrichments/{ticket-id}-enrichment.md"<br>3. Update comment with local file path                    |

**Debug Steps:**

1. Test JIRA write permissions: Manually edit ticket via UI
2. Verify custom field IDs: Check config.yaml matches JIRA admin panel
3. Validate data types: Ensure numbers are numeric, not strings
4. Check comment size: Use `wc -c` to verify < 32KB

---

## Workflow State Management & Resume Capability

### Overview

The enrichment workflow uses stateful execution to enable interruption and resumption at any stage, preventing data loss and eliminating redundant work.

### State File Structure

**Location:** `.workflow-state/{ticket-id}.json`

**Example State File:**

```json
{
  "ticket_id": "AOD-1234",
  "cve_id": "CVE-2024-1234",
  "workflow_id": "security-alert-enrichment-v1",
  "current_stage": 3,
  "started_at": "2025-11-08T14:30:00Z",
  "last_updated": "2025-11-08T14:35:36Z",
  "analyst": "john.doe@company.com",
  "stages": {
    "stage1": {
      "status": "completed",
      "started_at": "2025-11-08T14:30:00Z",
      "completed_at": "2025-11-08T14:31:23Z",
      "duration_seconds": 83,
      "outputs": {
        "cve_id": "CVE-2024-1234",
        "affected_systems": ["prod-web-01", "prod-web-02"],
        "acr": "High",
        "exposure": "Internet",
        "ticket_metadata": {
          "reporter": "monitoring@company.com",
          "created": "2025-11-08T14:15:00Z",
          "project": "AOD"
        }
      }
    },
    "stage2": {
      "status": "completed",
      "started_at": "2025-11-08T14:31:24Z",
      "completed_at": "2025-11-08T14:35:35Z",
      "duration_seconds": 251,
      "tool_used": "mcp__perplexity__reason",
      "outputs": {
        "cvss": 9.8,
        "cvss_vector": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "epss": 87.34,
        "kev": "Yes",
        "kev_date_added": "2025-10-15",
        "affected_versions": "2.0-2.14.1",
        "patched_version": "2.15.0, 2.12.2, 2.3.1",
        "exploit_status": "Active",
        "sources": [
          "https://nvd.nist.gov/vuln/detail/CVE-2024-1234",
          "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
          "https://vendor.com/security/advisory-2024-1234"
        ]
      }
    },
    "stage3": {
      "status": "in_progress",
      "started_at": "2025-11-08T14:35:36Z"
    }
  }
}
```

### Resume Capability

**When Resume Is Triggered:**

- Workflow interrupted (error, timeout, network failure)
- User manually aborts workflow (Ctrl+C)
- System shutdown during enrichment
- User requests resume (`*enrich-ticket AOD-1234 --resume`)

**Resume Process:**

1. Check for state file: `.workflow-state/{ticket-id}.json`
2. If state file exists:
   - Load state file
   - Validate state integrity (required fields present)
   - Display resume summary to user:
     ```
     Resume detected for AOD-1234 (CVE-2024-1234)
     Completed: Stage 1, Stage 2
     Current: Stage 3 (Business Context Assessment)
     Continue from Stage 3? [Y/n]
     ```
3. If user confirms (or auto-resume enabled):
   - Load completed stage outputs from state file
   - Skip to `current_stage` (Stage 3 in example)
   - Continue workflow from that point
4. If no state file exists:
   - Start fresh from Stage 1

**Benefits:**

- **No Data Loss:** Completed stage outputs preserved
- **No Redundant Work:** Skip stages already completed (avoid re-running expensive Perplexity research)
- **Debugging:** Step through workflow stage-by-stage for troubleshooting
- **Long Enrichments:** Pause and resume critical CVE deep research (5-10 min Stage 2)

### State Management Actions

**State Creation:**

- Created when Stage 1 starts
- Initial state: `current_stage: 1`, all stages `status: pending`

**State Updates:**

- Updated after each stage completes
- Stage marked `status: completed`, outputs saved
- `current_stage` incremented
- `last_updated` timestamp refreshed

**State Cleanup:**

- **Success:** State file deleted after Stage 8 successful completion
- **Orphaned States:** Files >24 hours old auto-cleaned (weekly maintenance task)
- **Manual Cleanup:** User can delete `.workflow-state/{ticket-id}.json` to force fresh start

### Resume Example Scenarios

**Scenario 1: Perplexity Timeout in Stage 2**

```
Stage 1: ✅ Completed (83 seconds)
Stage 2: ❌ Timeout after 600 seconds
Action: State saved with Stage 1 outputs
Resume: Skip Stage 1, retry Stage 2 with simplified query
```

**Scenario 2: Network Failure Before Stage 8**

```
Stages 1-7: ✅ Completed
Stage 8: ❌ Network failure (JIRA unreachable)
Action: State saved with all enrichment data
Resume: Skip Stages 1-7, proceed directly to Stage 8 JIRA update
```

**Scenario 3: User Abort for Manual Research**

```
Stage 1-2: ✅ Completed
User: Aborts to manually research vendor advisory
Action: State saved
Later: User resumes, workflow continues from Stage 3
```

### State File Integrity

**Required Fields:**

- `ticket_id`: JIRA ticket identifier
- `cve_id`: CVE identifier
- `workflow_id`: Workflow version
- `current_stage`: Integer (1-8)
- `stages`: Object with stage statuses and outputs

**Validation on Resume:**

- Check required fields present
- Validate `current_stage` in range 1-8
- Verify completed stage outputs include required data
- If validation fails: Warn user, offer fresh start option

### Audit Trail

State files provide complete audit trail:

- Who ran enrichment (analyst field)
- When each stage started/completed
- Duration of each stage
- Tools used (Perplexity tool selection)
- Intermediate outputs (debugging)

**Metrics from State:**

- Average stage duration (performance baseline)
- Most common failure points (workflow improvement)
- Tool selection patterns (Perplexity usage)

---

## Appendix: Quick Reference

### Workflow Stages Summary

| Stage                               | Duration | Key Outputs                               |
| ----------------------------------- | -------- | ----------------------------------------- |
| 1. Triage & Context Extraction      | 1-2 min  | CVE ID, Affected Systems, Initial Context |
| 2. AI-Assisted CVE Research         | 1-10 min | CVSS, EPSS, KEV, Patches, Exploits        |
| 3. Business Context Assessment      | 2-3 min  | ACR, Exposure, Business Impact            |
| 4. Remediation Planning             | 2-3 min  | Patches, Workarounds, Controls            |
| 5. MITRE ATT&CK Mapping             | 1-2 min  | Tactics, Techniques, Detection            |
| 6. Multi-Factor Priority Assessment | 1-2 min  | Priority (P1-P5), SLA                     |
| 7. Structured Documentation         | 1 min    | 12-Section Enrichment Document            |
| 8. JIRA Update & Validation         | 1-2 min  | Updated JIRA Ticket, Local Files          |

### MCP Tools Quick Reference

**Atlassian MCP:**

- `mcp__atlassian__getJiraIssue` - Read ticket (Stage 1)
- `mcp__atlassian__addCommentToJiraIssue` - Post enrichment (Stage 8)
- `mcp__atlassian__updateJiraIssue` - Update fields (Stage 8)

**Perplexity MCP:**

- `mcp__perplexity__search` - Quick (1-2 min, CVSS < 7.0)
- `mcp__perplexity__reason` - Analytical (3-5 min, CVSS 7.0-8.9)
- `mcp__perplexity__deep_research` - Comprehensive (5-10 min, CVSS ≥ 9.0)

### Priority Algorithm Quick Reference

- **P1:** CVSS ≥ 9.0 + KEV OR CVSS ≥ 9.0 + Internet + Critical ACR + Active exploit
- **P2:** CVSS ≥ 7.0 + High ACR OR CVSS ≥ 9.0 + Medium/Low ACR
- **P3:** CVSS 4.0-6.9 + Medium ACR OR CVSS 7.0-8.9 + Low ACR
- **P4:** CVSS < 4.0 OR Isolated + No exploit
- **P5:** CVSS < 4.0 + Low ACR + Isolated + No remediation

### SLA Deadlines

- P1: 24 hours
- P2: 7 days
- P3: 30 days
- P4: 90 days
- P5: Best effort

### Common File Locations

- **Config:** `expansion-packs/bmad-1898-engineering/config.yaml`
- **Enrichments:** `enrichments/{ticket-id}-enrichment.md`
- **State Files:** `.workflow-state/{ticket-id}.json`
- **Metrics:** `metrics/enrichment-metrics.csv`
- **Template:** `templates/security-enrichment-tmpl.yaml`

---

## Related Documentation

- **[Security Analyst Agent Usage Guide](security-analyst-agent.md)** - User-level workflow guide for Security Analyst agent
- **[Installation & Initial Setup Guide](../INSTALLATION.md)** - Setup instructions for bmad-1898-engineering
- **Story 3.1: Security Alert Enrichment Workflow** - Implementation reference (`docs/stories/3.1.security-alert-enrichment-workflow.md`)
- **Story 5.5: Security Analysis Review Workflow Deep Dive** - Parallel workflow documentation
- **Story 5.10: Troubleshooting, FAQ & Best Practices** - General troubleshooting guide

---

**Document Version:** 1.0
**Last Updated:** 2025-11-08
**Maintained By:** BMad 1898 Engineering Team

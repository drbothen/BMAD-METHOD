# Troubleshooting, FAQ & Best Practices

## Overview

This document provides troubleshooting guidance, frequently asked questions, and best practices for the BMAD 1898 Engineering expansion pack. It covers vulnerability enrichment, event investigation, quality review, and common operational challenges.

**Quick Navigation:**
- [Event Investigation Troubleshooting](#event-investigation-troubleshooting)
- [Vulnerability Enrichment Troubleshooting](#vulnerability-enrichment-troubleshooting)
- [Quality Review Troubleshooting](#quality-review-troubleshooting)
- [MCP Integration Issues](#mcp-integration-issues)
- [Best Practices](#best-practices)

---

## Event Investigation Troubleshooting

### Issue: Insufficient Evidence for Disposition Decision

**Symptoms:**
- Cannot determine if alert is TP/FP/BTP
- Missing logs or incomplete evidence
- No historical context available

**Root Causes:**
- Log sources unavailable or not configured
- Log retention period expired (evidence deleted)
- Asset has limited logging capabilities (legacy ICS systems)
- Incomplete alert metadata from detection platform

**Solutions:**

1. **Request Additional Logs from SOC/Asset Owner:**
   ```
   - Firewall logs (traffic flow context)
   - Host-based logs (process execution, file modifications)
   - Authentication logs (user activity timeline)
   - Network packet captures (if available)
   ```

2. **Use Alternative Evidence Sources:**
   - Change management tickets (correlate with scheduled activities)
   - Asset owner interview (ask "is this expected behavior?")
   - Historical baselines (compare to normal activity patterns)
   - Threat intelligence (context for external IPs, malware signatures)

3. **Document Evidence Gaps:**
   ```markdown
   **Evidence Gaps:**
   - Host logs unavailable (PLC has limited logging capabilities)
   - Packet capture not retained (retention period expired)
   - Historical baseline unknown (new asset, no baseline data)

   **Impact on Investigation:**
   - Confidence level reduced to MEDIUM (limited corroborating evidence)
   - Disposition based on firewall logs + change ticket only
   ```

4. **Adjust Confidence Level:**
   - HIGH confidence requires 3+ corroborating sources
   - MEDIUM confidence: 1-2 sources, plausible but not definitive
   - LOW confidence: Single source or significant evidence gaps
   - **Recommendation:** If LOW confidence TP, escalate to senior analyst for review

---

### Issue: Disposition Disagreement Between Analyst and Reviewer

**Symptoms:**
- Analyst determined BTP, reviewer believes it's TP
- Analyst determined FP, reviewer believes it's BTP
- Cannot reach consensus on disposition

**Root Causes:**
- Different interpretation of evidence
- Analyst missed key evidence (incomplete investigation)
- Reviewer lacks operational context
- Legitimate difference in risk tolerance

**Solutions:**

1. **Collaborative Review Session:**
   - Schedule 15-30 minute discussion (analyst + reviewer)
   - Walk through evidence together
   - Discuss reasoning for each disposition
   - Identify missing evidence or context

2. **Document Both Perspectives:**
   ```markdown
   **Analyst Disposition:** Benign True Positive (BTP)
   - Reasoning: Authorized by change ticket CHG-1234
   - Evidence: Change window matches timestamp

   **Reviewer Assessment:** True Positive (TP) - DISAGREE
   - Reasoning: Change ticket lacks security approval
   - Evidence: Source IP is NOT authorized engineering workstation
   - Concern: Possible social engineering (fake change ticket)

   **Resolution:**
   - Escalated to Security Lead for final decision
   - Additional investigation requested (verify change ticket legitimacy)
   ```

3. **Escalate to Team Lead:**
   - If cannot resolve in 30 minutes → escalate
   - Team lead reviews evidence and makes final call
   - Document escalation rationale

4. **Update Investigation with New Evidence:**
   - If reviewer found missed evidence → update investigation
   - Re-run disposition determination with complete evidence
   - Acknowledge gap (learning opportunity, not blame)

---

### Issue: Unknown or First-Time Alert Type

**Symptoms:**
- Never investigated this alert signature before
- Unsure what "normal" looks like for this platform
- No established baseline or playbook

**Root Causes:**
- New detection platform deployed (Claroty, Snort, Splunk rule)
- New asset type onboarded (unfamiliar OT protocol)
- Rare alert (first occurrence in months/years)

**Solutions:**

1. **Reference Knowledge Base (Story 7.7):**
   - Event Investigation Best Practices KB
   - Platform-specific alert documentation
   - Sample investigations for common alert types

2. **Consult Detection Engineering Team:**
   - Ask: "What does this signature detect?"
   - Ask: "What is expected baseline for this alert?"
   - Ask: "Are there known false positive scenarios?"

3. **Research Alert Signature Documentation:**
   - Claroty: Rule ID documentation (what behavior triggers alert?)
   - Snort: Signature details (CVE mapping, exploit pattern)
   - Splunk: Correlation rule logic (what events are combined?)

4. **Create Mini-Baseline:**
   ```markdown
   **First-Time Investigation: Alert #317 (SSH in Control Environments)**

   Research:
   - Alert triggers on: SSH connections to OT assets (port 22)
   - Expected baseline: Rare (only during maintenance windows)
   - Known FP scenarios: Engineering workstation access during changes

   Baseline Hypothesis (to be validated over time):
   - Frequency: 1-3 occurrences per month (maintenance-driven)
   - Expected sources: Engineering workstations (192.168.10.0/24)
   - Expected timing: Business hours (08:00-17:00) during change windows

   Actions:
   - Document this baseline for future reference
   - Update after 3 months of data (validate hypothesis)
   ```

---

### Issue: ICS/SCADA Protocol Confusion

**Symptoms:**
- Unclear if protocol behavior is normal or suspicious
- Unfamiliar with OT protocols (Modbus, DNP3, BACnet)
- Misinterpreting protocol-specific alerts

**Root Causes:**
- IT analyst background (unfamiliar with OT protocols)
- Limited OT protocol documentation
- Protocol behavior differs from IT expectations

**Solutions:**

1. **Reference OT Protocol Documentation:**
   - Modbus TCP: https://modbus.org/specs.php
   - DNP3: https://www.dnp.org/
   - BACnet: http://www.bacnet.org/
   - IEC 104: https://www.iec.ch/

2. **Consult OT Subject Matter Expert:**
   - Identify OT SME on team (often ICS engineer or OT security specialist)
   - Schedule knowledge transfer session
   - Ask: "What is normal communication pattern for this protocol?"

3. **Learn Common OT Protocol Characteristics:**
   ```markdown
   **Modbus TCP (Port 502):**
   - Cleartext protocol (no encryption - THIS IS NORMAL)
   - Master-slave architecture (HMI → PLC commands)
   - Expected: Cyclic polling (HMI reads PLC status every 1-5 seconds)
   - Suspicious: Modbus from unexpected source (not HMI)

   **DNP3 (Port 20000):**
   - SCADA protocol (common in utilities)
   - Cleartext protocol (no encryption - THIS IS NORMAL for DNP3)
   - Expected: Master station → RTU communication
   - Suspicious: DNP3 on non-SCADA network

   **BACnet (Port 47808 UDP):**
   - Building automation protocol (HVAC, lighting)
   - Broadcast-heavy (device discovery via broadcasts)
   - Expected: Frequent UDP broadcasts (THIS IS NORMAL)
   - Suspicious: BACnet on non-building automation network
   ```

4. **Create Protocol Reference Card:**
   - One-page quick reference for common OT protocols
   - Include: Port numbers, expected behavior, suspicious indicators
   - Keep accessible during investigations

---

### Issue: After-Hours Alert - Cannot Contact Asset Owner

**Symptoms:**
- Alert triggered at 02:00 UTC (middle of night)
- Asset owner unavailable (not on-call)
- Cannot verify if activity is authorized

**Root Causes:**
- Asset owner not in on-call rotation
- No documented maintenance schedule
- Emergency maintenance not communicated to SOC

**Solutions:**

1. **Check Change Management System:**
   - Search for approved change tickets (even if asset owner unavailable)
   - Look for emergency change requests
   - Review scheduled maintenance calendar

2. **Use Historical Context as Proxy:**
   ```markdown
   **Asset Owner Unavailable - Using Historical Context:**

   Historical Pattern:
   - Previous SSH connections to this PLC: 3 in past 90 days
   - All previous connections: During business hours (08:00-17:00)
   - All previous connections: Correlated with change tickets

   Current Activity:
   - Time: 02:00 UTC (after-hours - ANOMALY)
   - Change ticket: None found
   - Pattern match: Does NOT align with historical baseline

   Preliminary Assessment: Suspicious (deviation from baseline)
   → Confidence: MEDIUM (asset owner confirmation needed)
   → Action: Escalate to on-call security lead for disposition decision
   ```

3. **Escalate to On-Call Security Lead:**
   - If suspicious indicators + no asset owner → escalate
   - On-call lead can authorize containment decision
   - Document escalation in investigation report

4. **Follow Up During Business Hours:**
   - After-hours disposition may be provisional (MEDIUM confidence)
   - Follow up with asset owner next business day
   - Update disposition if new information changes assessment

---

## Vulnerability Enrichment Troubleshooting

### Issue: CVE Not Found in NVD

**Symptoms:**
- Searching NVD for CVE ID returns no results
- CVE appears in vendor advisory but not in NVD
- Unknown if CVE is valid or not

**Root Causes:**
- CVE recently published (NVD lag time: 1-7 days after CVE assignment)
- CVE rejected or reserved (not yet published)
- Vendor uses internal tracking ID (not official CVE)

**Solutions:**

1. **Verify CVE ID Format:**
   - Valid format: CVE-YYYY-NNNNN (e.g., CVE-2024-1234)
   - Check for typos (common: CVE-2024-01234 vs CVE-2024-1234)

2. **Search Alternative Sources:**
   - MITRE CVE: https://cve.mitre.org/cve/search_cve_list.html
   - Vendor security advisory (original source)
   - GitHub Security Advisories (GHSA)

3. **Document CVE Unavailability:**
   ```markdown
   **CVSS Score:** Not Available
   **Source:** CVE-2024-12345 not found in NVD as of 2025-11-09
   **Alternative Source:** Vendor Advisory (example.com/security/2024-12345)
   **Vendor CVSS:** 7.5 (High) - per vendor assessment
   **Note:** NVD data pending (CVE published 2025-11-07, within typical lag time)
   ```

4. **Re-Check NVD in 7 Days:**
   - Set reminder to update enrichment when NVD publishes data
   - Proceed with vendor-provided CVSS in interim

---

### Issue: EPSS Score Outdated or Unavailable

**Symptoms:**
- EPSS score is 30+ days old
- FIRST EPSS database has no data for this CVE
- Unclear if EPSS score is current

**Root Causes:**
- CVE too new (EPSS calculation lag: up to 30 days for new CVEs)
- CVE too old (EPSS only available for CVEs from ~2020 onward)
- FIRST EPSS database query error

**Solutions:**

1. **Verify EPSS Currency:**
   - Current = within 7 days of today's date
   - Acceptable = 8-30 days (note as "slightly outdated")
   - Outdated = 30+ days (re-query FIRST database)

2. **Use Alternative Exploitation Indicators:**
   ```markdown
   **EPSS Score:** Not Available (CVE too new)
   **Alternative Exploitation Assessment:**
   - KEV Status: Not on CISA KEV (low likelihood of exploitation)
   - Exploit Availability: No public exploits (searched Exploit-DB, GitHub)
   - Threat Intelligence: No active exploitation observed (Perplexity search)
   **Assessment:** Low exploitation probability (despite missing EPSS)
   ```

3. **Document EPSS Unavailability:**
   - Note in enrichment: "EPSS not available - CVE published 2025-11-08 (too recent)"
   - Prevents reviewer from flagging as "missing data"

---

## Quality Review Troubleshooting

### Issue: Reviewer and Analyst Disagree on Quality Score

**Symptoms:**
- Analyst believes enrichment is "Excellent"
- Reviewer scores as "Needs Improvement"
- Large point discrepancy (analyst expectation: 90+, actual: 68)

**Root Causes:**
- Misunderstanding of dimension criteria
- Analyst self-assessment overly generous
- Reviewer interpretation too strict

**Solutions:**

1. **Reference Dimension Checklists:**
   - Technical Accuracy: 8-item checklist (CVSS, EPSS, KEV, versions, exploit, ATT&CK)
   - Completeness: 12 template sections (all must be populated)
   - Actionability: 6 elements (remediation, verification, compensating controls)

2. **Collaborative Review Session:**
   - Walk through each dimension score
   - Show specific examples of gaps
   - Explain scoring rationale

3. **Provide Concrete Examples:**
   ```markdown
   **Dimension: Actionability (Score: 45% - Inadequate)**

   **Gap:** Remediation guidance too vague
   - Analyst wrote: "Update Jenkins to latest version"
   - Expected: "Update Jenkins to version 2.440.2 or later"
   - Missing: Specific patch version number

   **Impact:** DevOps cannot act without specific version (blocks remediation)
   **Recommendation:** Research vendor advisory for specific patched version
   **Effort:** 10 minutes
   ```

4. **Learning Opportunity (Not Blame):**
   - Frame as growth opportunity (improve for next enrichment)
   - Link to learning resources (remediation guidance best practices)
   - Acknowledge effort (even if gaps exist)

---

## MCP Integration Issues

### Issue: Atlassian MCP Connection Failed

**Symptoms:**
- Agent cannot retrieve JIRA tickets
- Error: "Atlassian MCP connection unavailable"
- Commands fail with MCP errors

**Root Causes:**
- Atlassian MCP server not running
- API token expired or invalid
- JIRA URL misconfigured
- Network connectivity issue

**Solutions:**

1. **Verify MCP Server Status:**
   ```bash
   # Check if Atlassian MCP server is running
   ps aux | grep atlassian-mcp

   # Check MCP server logs
   cat ~/.config/mcp/atlassian-mcp.log
   ```

2. **Verify API Token:**
   - Check token expiration (JIRA → Profile → Personal Access Tokens)
   - Regenerate token if expired
   - Update MCP configuration with new token

3. **Test JIRA Connectivity:**
   ```bash
   # Test JIRA API access (replace with your instance)
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        https://your-instance.atlassian.net/rest/api/3/myself
   ```

4. **Restart MCP Server:**
   ```bash
   # Stop MCP server
   killall atlassian-mcp-server

   # Restart with configuration
   atlassian-mcp-server --config ~/.config/mcp/atlassian-config.json
   ```

---

### Issue: Perplexity MCP Rate Limiting

**Symptoms:**
- Fact-check operations fail with "rate limit exceeded"
- Enrichment research stalls mid-process
- Error: "429 Too Many Requests"

**Root Causes:**
- Perplexity API rate limit exceeded (free tier: 5 requests/minute)
- Burst of research queries (multiple enrichments in parallel)

**Solutions:**

1. **Wait for Rate Limit Reset:**
   - Rate limit window: 1 minute
   - Wait 60 seconds, then retry

2. **Batch Research Queries:**
   - Combine multiple research questions into single query
   - Example: "Research CVE-2024-1234: CVSS score, EPSS score, KEV status, exploit availability"

3. **Upgrade Perplexity Tier:**
   - Paid tier: Higher rate limits (20-50 requests/minute)
   - Enterprise tier: No rate limits

---

## Best Practices

### Event Investigation Best Practices

#### 1. Always Gather Business Context

**Why:** Technical analysis alone is insufficient - must understand operational context.

**How:**
- Check change management system (JIRA, ServiceNow)
- Review maintenance schedules
- Contact asset owner
- Search for historical similar activity

**Example:**
```markdown
✅ GOOD:
"SSH connection correlated with change ticket CHG-1234 (firmware update).
Engineer John Smith confirmed activity. Historical pattern matches (3 SSH
connections per 90 days during maintenance)."

❌ BAD:
"SSH connection detected. This is suspicious."
```

#### 2. Use Hypothesis-Driven Investigation

**Why:** Structured approach prevents anchoring bias and confirmation bias.

**How:**
1. Generate 2-3 hypotheses (before collecting evidence)
   - Hypothesis 1: Malicious attack (TP)
   - Hypothesis 2: Authorized maintenance (BTP)
   - Hypothesis 3: Detection platform error (FP)
2. Collect evidence for EACH hypothesis
3. Test each hypothesis against evidence
4. Select hypothesis with strongest evidence

**Example:**
```markdown
**Hypotheses:**
1. Malicious SSH brute force (TP)
   - Evidence for: 15 failed attempts, automated timing
   - Evidence against: Internal source (CI/CD system), change ticket exists

2. Misconfigured deployment script (BTP)
   - Evidence for: Change ticket CHG-5690, Jenkins process, historical pattern
   - Evidence against: None

3. Detection platform error (FP)
   - Evidence for: None (SSH attempts confirmed in logs)
   - Evidence against: Multiple log sources confirm activity

**Selected Hypothesis:** #2 (BTP - Misconfigured deployment script)
```

#### 3. Document Evidence Gaps

**Why:** Transparency about limitations improves review quality and future investigations.

**How:**
```markdown
**Evidence Collected:**
✅ Claroty alert details
✅ Firewall logs
✅ Change management ticket

**Evidence Gaps:**
❌ Host logs unavailable (PLC has limited logging capabilities)
❌ Packet capture not retained (retention policy: 7 days, event is 10 days old)

**Impact on Confidence:**
- Confidence reduced to MEDIUM (would be HIGH with host logs)
- Relying on firewall + change ticket only (2 sources instead of 3+)
```

#### 4. Consider ICS/SCADA-Specific Risks

**Why:** OT environments have unique safety and operational constraints.

**How:**
- **Safety Implications:** Could this affect physical processes? (production line, safety systems)
- **Legacy Constraints:** Limited logging, outdated protocols (expected, not suspicious)
- **Operational Impact:** Can we isolate the asset without disrupting production?
- **Air-Gap Assumptions:** Verify network segmentation (IT/OT separation)

**Example:**
```markdown
**ICS-Specific Considerations:**
- Safety Risk: HMI controls safety interlocks (isolation could disable safety systems)
- Legacy Constraints: Windows 7 embedded (cannot deploy modern EDR)
- Operational Impact: Cannot isolate during production shift (requires shutdown)
- Network Segmentation: Verified - OT network isolated via firewall

**ICS-Aware Response:**
- Containment delayed until end of production shift (safety priority)
- Coordinate with operations for controlled shutdown
- Manual monitoring in interim (watch for lateral movement)
```

---

### Vulnerability Enrichment Best Practices

#### 1. Always Verify CVSS Score Against Official Sources

**Why:** Vendor-provided CVSS may differ from NVD (sometimes inflated for marketing).

**How:**
- Primary source: NVD (https://nvd.nist.gov/)
- Secondary source: Vendor security advisory
- If discrepancy: Use NVD score + note vendor difference

**Example:**
```markdown
**CVSS Score:** 7.5 (High)
**Source:** NVD CVE-2024-1234
**Vendor Score:** 9.1 (Critical) - Vendor assessment
**Note:** Using NVD score (authoritative source). Vendor score reflects
product-specific context not captured in CVSS base score.
```

#### 2. Multi-Factor Priority Assessment (Not Just CVSS)

**Why:** CVSS alone is insufficient - must consider exploitability, business context, exposure.

**How:**
```markdown
**Priority Factors:**
1. CVSS: 9.8 (Critical) - Technical severity
2. EPSS: 0.02% (Very Low) - Exploitation probability
3. KEV: Not on CISA KEV - Low active exploitation
4. Asset Criticality: ACR 5/5 (Business-Critical) - High business impact
5. System Exposure: Internal only (not internet-facing) - Lower immediate risk

**Calculated Priority:** HIGH (not Critical)
- Rationale: High technical severity + business criticality, but low exploitation
  probability and not internet-facing. Prioritize after Critical internet-facing vulns.
```

#### 3. Actionable Remediation Guidance

**Why:** Vague guidance blocks remediation ("update software" is not actionable).

**How:**
```markdown
✅ GOOD:
**Remediation:**
1. Update PostgreSQL to version 15.3.2 or later
   - Debian/Ubuntu: `sudo apt-get update && sudo apt-get install postgresql`
   - RHEL/CentOS: `sudo yum update postgresql`
2. Verify patch applied:
   - Connect to database: `psql -U postgres`
   - Check version: `SELECT version();`
   - Expected output: "PostgreSQL 15.3.2" or higher
3. Restart PostgreSQL service:
   - `sudo systemctl restart postgresql`
4. Verify service operational:
   - `sudo systemctl status postgresql`
   - Expected: "active (running)"

**Compensating Controls (if patch not immediately available):**
- Restrict database access to trusted IPs only (firewall rule)
- Disable affected stored procedure (if identified)
- Enable PostgreSQL query logging (detect exploitation attempts)

**Estimated Remediation Time:** 30 minutes (including testing)

❌ BAD:
**Remediation:** Update PostgreSQL to latest version.
```

---

### Quality Review Best Practices

#### 1. Blameless Language Always

**Why:** Encourages learning, reduces defensiveness, improves team culture.

**How:**
```markdown
❌ BLAME LANGUAGE:
"You failed to check KEV status - this is a critical oversight."

✅ BLAMELESS LANGUAGE:
"KEV status verification is missing - recommend checking CISA catalog at [URL]."

❌ BLAME LANGUAGE:
"This analysis is biased and incomplete."

✅ BLAMELESS LANGUAGE:
"Minor confirmation bias detected - consider balancing with non-exploitation
evidence. Additional context could enhance completeness."
```

#### 2. Strengths First, Then Gaps

**Why:** Positive feedback motivates improvement, balanced approach maintains morale.

**How:**
```markdown
**Review Structure:**

1. Executive Summary (positive tone)
2. Strengths & What Went Well (always first, even if gaps exist)
3. Quality Dimension Scores (objective metrics)
4. Gaps & Improvements (constructive, specific, actionable)
5. Recommendations (prioritized, effort-estimated)

**Example:**
**Strengths & What Went Well:**
- Exceptional technical accuracy - all metrics verified
- Complete 12-section enrichment with detailed analysis
- Excellent remediation guidance with specific commands

**Opportunities for Enhancement:**
- Consider adding verification steps for post-patch validation (2-min enhancement)
- Source citation could include URL for EPSS (1-min addition)
```

#### 3. Provide Learning Resources for Every Gap

**Why:** Turns review into learning opportunity, enables self-improvement.

**How:**
```markdown
**Gap:** EPSS score cited without source URL

**Recommendation:** Add FIRST EPSS source: https://www.first.org/epss/

**Why It Matters:** Authoritative sources build trust in analysis and enable
independent verification by security leadership.

**Learning Resource:** docs/checklists/source-citation-checklist.md

**Conversation Starter:** What other metrics do you typically source-cite?
Let's discuss citation standards for different data types.
```

---

## Quick Reference: Common Error Messages

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| "Insufficient evidence for disposition" | Cannot determine TP/FP/BTP | Gather additional logs, consult asset owner, adjust confidence to LOW |
| "Protocol behavior unexpected" | Activity deviates from baseline | Research protocol documentation, consult OT SME, check historical patterns |
| "Alert severity mismatch with evidence" | Automation bias detected | Independently validate severity, don't trust alert classification blindly |
| "Disposition disagreement" | Analyst and reviewer diverge | Collaborative review session, escalate to team lead if unresolved |
| "MCP connection failed" | API integration issue | Check MCP server status, verify API tokens, test network connectivity |
| "CVE not found in NVD" | NVD lag time or invalid CVE | Search alternative sources (MITRE, vendor advisory), document unavailability |
| "EPSS unavailable" | CVE too new or too old | Use alternative exploitation indicators (KEV, exploit availability, threat intel) |

---

## Additional Resources

- **Event Investigation Workflow Deep Dive:** `docs/workflows/event-investigation-workflow-deep-dive.md`
- **Security Analyst User Guide:** `docs/user-guide/security-analyst-agent.md`
- **Security Reviewer User Guide:** `docs/user-guide/security-reviewer-agent.md`
- **Event Investigation Training:** `docs/training/event-investigation-training.md`
- **NIST SP 800-61:** Computer Security Incident Handling Guide
- **MITRE ATT&CK:** https://attack.mitre.org/

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Maintained By:** BMAD Engineering Team - Epic 7

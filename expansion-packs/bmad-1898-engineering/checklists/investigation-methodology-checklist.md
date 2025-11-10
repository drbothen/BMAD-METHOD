# Investigation Methodology Checklist

**Weight:** 10%
**Purpose:** Verify sound investigative process and rigor through systematic, hypothesis-driven analysis.

## Check Items

- [ ] **Hypothesis-Driven Approach Evident** - Initial hypothesis or investigative question clearly stated at investigation start
- [ ] **Multiple Data Sources Consulted** - At least 3 different log sources or data sources referenced (e.g., SIEM, firewall, endpoint, application logs, asset DB, threat intel)
- [ ] **Scope Appropriately Bounded** - Investigation scope defined and justified (time range, systems included, search parameters), not overly broad or narrow
- [ ] **Investigation Steps Documented** - Clear sequence of actions taken, showing logical progression from hypothesis to conclusion
- [ ] **Dead Ends or Negative Findings Noted** - Documented what was checked but yielded no results (e.g., "Checked threat intel feeds → no matches found")
- [ ] **Peer Consultation or Escalation Used When Appropriate** - Evidence of seeking help, second opinion, or subject matter expert input when needed

## Scoring

- **Total Items:** 6
- **Passed Items:** [count after review]
- **Score:** (Passed / 6) × 100 = \_\_\_\_%

## Guidance

### Hypothesis-Driven Investigation

**What is a Hypothesis?**
A testable explanation or investigative question that guides your analysis.

**Good Hypothesis Examples:**

- "SSH connection represents unauthorized lateral movement"
- "Alert triggered due to authorized maintenance activity during change window"
- "Brute force attempt from compromised internal workstation"
- "False positive caused by automated backup process"

**Poor Hypothesis Examples:**

- "Something suspicious happened" (too vague, not testable)
- "This is definitely malicious" (conclusion, not hypothesis)
- No hypothesis stated (investigation lacks direction)

**Hypothesis-Driven Process:**

1. **State Hypothesis:** Based on alert, state initial working hypothesis
2. **Identify Evidence Needed:** What data would confirm or refute hypothesis?
3. **Collect Evidence:** Gather relevant logs, context, historical data
4. **Evaluate Hypothesis:** Does evidence support or refute hypothesis?
5. **Refine or Conclude:** If refuted, form new hypothesis and repeat; if confirmed, document conclusion

**Example:**

```
Initial Hypothesis: SSH connection from 10.50.1.100 to 10.10.5.25 represents unauthorized lateral movement

Evidence Needed to Test:
- Is 10.50.1.100 authorized to connect to 10.10.5.25? (check asset DB, network policy)
- Is this connection pattern unusual? (check historical logs)
- What authentication method was used? (check SSH logs for key vs. password)
- Is there other suspicious activity on source system? (check SIEM, endpoint logs)

Evidence Collected:
✓ Asset DB shows 10.50.1.100 = authorized jump server
✓ 90 days of logs show daily connection at 02:00 UTC (normal pattern)
✓ SSH auth logs show public key authentication (authorized key)
✗ No suspicious activity on jump server (SIEM clean, endpoint clean)

Evaluation: Hypothesis REFUTED - Evidence indicates authorized, scheduled activity

Revised Hypothesis: SSH connection is authorized backup operation triggering alert due to detection rule sensitivity

Conclusion: False Positive - Authorized backup operation
```

### Multiple Data Sources

**Why Multiple Sources Matter:**

- Single source may be incomplete or misleading
- Corroboration increases confidence
- Different sources provide different perspectives (network vs. endpoint vs. application)

**Common Data Sources:**

**Network Sources (3 examples):**

1. Firewall logs (connection attempts, blocked traffic, source/dest IPs)
2. IDS/IPS logs (Claroty, Snort, Suricata - signature matches, payload analysis)
3. NetFlow/IPFIX (traffic patterns, bandwidth, protocols)

**Endpoint Sources (3 examples):**

1. Endpoint Detection & Response (EDR) logs (process execution, file modifications, registry changes)
2. Windows Event Logs (authentication events, process creation, service changes)
3. Antivirus/Anti-malware logs (detections, quarantines, scan results)

**Application/System Sources (3 examples):**

1. Application logs (SSH auth logs, web server access logs, database query logs)
2. SIEM correlation rules (aggregated events, cross-source correlation)
3. Authentication logs (Active Directory, RADIUS, LDAP)

**Contextual Sources (3 examples):**

1. Asset management database (asset ownership, criticality, business function)
2. Configuration Management Database (CMDB) - system relationships, dependencies
3. Change management system (scheduled changes, maintenance windows, approvals)

**Minimum Requirement:** At least 3 different sources (demonstrates thoroughness)

**Example - Good Multi-Source Investigation:**

```
Data Sources Consulted (5 sources):
1. Claroty IDS logs → Full alert details, packet capture
2. Firewall logs (10.50.1.100) → All connections last 24h, no other suspicious destinations
3. SSH auth logs (10.10.5.25) → Authentication method, user account, key fingerprint
4. Asset management DB → Asset ownership, criticality, business function
5. IT Operations calendar → Scheduled maintenance windows, confirmed backup schedule
```

**Example - Poor Single-Source Investigation:**

```
Data Source: Claroty alert only
(No firewall logs, no SSH logs, no asset DB, no historical context)
```

### Scope Bounding

**Well-Bounded Scope:**

- Time range justified (e.g., "Reviewed 90 days to establish baseline")
- Systems included explained (e.g., "Analyzed source and destination only, no lateral investigation needed")
- Search parameters clear (e.g., "Searched for source IP 10.50.1.100 connections to any destination")

**Too Broad (Over-Investigation):**

- "Reviewed all SSH connections across entire network for last year" (for single alert)
- Investigating unrelated systems without justification

**Too Narrow (Under-Investigation):**

- "Only reviewed alert metadata, no additional logs" (insufficient evidence)
- "Only checked last 1 hour" (missed historical pattern over 90 days)

**Example:**

```
Investigation Scope:
- Time Range: 90 days (establish baseline pattern for source IP)
- Systems Analyzed: Source 10.50.1.100, Destination 10.10.5.25, firewall (correlation)
- Search Parameters: All SSH (port 22) connections from source IP
- Justification: 90 days sufficient to identify recurring patterns; limited to source/dest systems because alert involves only these two assets
```

### Documentation of Investigation Steps

**Well-Documented Steps:**

```
Investigation Steps:
1. Reviewed Claroty alert details (Rule ID: 4782, Severity: High, Detection Time: 14:32:15 UTC)
2. Extracted source/dest IPs and checked Asset DB → Jump server + File server identified
3. Queried firewall logs for 10.50.1.100 activity (last 24h) → Only connection to 10.10.5.25 at 14:30 UTC
4. Retrieved SSH auth logs from 10.10.5.25 → Public key auth, key fingerprint: aa:bb:cc:dd:ee:ff
5. Checked IT Ops key registry → Key fingerprint matches authorized backup key (entry #129)
6. Queried SIEM for historical pattern (90 days) → 87 occurrences, all at 02:00 UTC ±5 min
7. Contacted IT Operations team → Confirmed scheduled backup operation, provided backup schedule document
8. Reviewed SIEM for concurrent suspicious activity on jump server → None found
```

**Poorly Documented Steps:**

```
Investigation Steps:
- Checked logs
- Looks normal
```

### Dead Ends and Negative Findings

**Why Document Dead Ends?**

- Shows thoroughness (you didn't skip important checks)
- Prevents duplicate work (others know what was already checked)
- Supports disposition (absence of evidence is evidence of absence when searching in right places)

**Examples of Negative Findings:**

```
Dead Ends / Negative Findings:
- Checked threat intelligence feeds (VirusTotal, AbuseIPDB, Recorded Future) → No matches for source IP (expected for internal IP)
- Reviewed jump server endpoint logs for IOCs (privilege escalation, persistence, unusual processes) → Clean (no compromise indicators)
- Searched SIEM for other suspicious activity from source IP (last 7 days) → None found
- Checked for concurrent alerts on destination server → No other alerts at same timeframe
```

**Value:** These negative findings strengthen the False Positive disposition (if source was compromised, we'd expect to see IOCs)

### Peer Consultation

**When to Consult Others:**

- Low confidence disposition on critical asset (better safe than sorry)
- Unfamiliar attack vector or technology (e.g., ICS protocol you don't know)
- Conflicting evidence (different sources tell different story)
- High-stakes decision (critical asset, potential data breach, compliance implications)

**Examples of Good Consultation:**

```
Peer Consultation:
- Consulted with IT Operations team to confirm backup schedule (Email from John Smith, IT Ops Manager, 2024-11-09 15:00 UTC)
- Escalated to Senior SOC Analyst for second opinion on disposition (Jane Doe reviewed and concurred with FP assessment)
- Reached out to Network Engineering to validate firewall rule expectations (confirmed jump server → file server is permitted by policy)
```

**No Consultation Needed (Document Why):**

```
Peer Consultation: Not required
- High confidence disposition (multiple corroborating evidence sources)
- Straightforward alert type (common SSH false positive)
- Non-critical assets (development environment)
```

### Examples

#### Example 1: Rigorous Methodology

```
**Hypothesis:** SSH connection represents unauthorized lateral movement

**Data Sources Consulted (5):**
1. Claroty IDS logs
2. Firewall logs (10.50.1.100)
3. SSH authentication logs (10.10.5.25)
4. Asset management database
5. SIEM historical query (90-day baseline)

**Investigation Scope:**
- Time Range: 90 days (establish baseline)
- Systems: Source 10.50.1.100, Destination 10.10.5.25, firewall
- Search: All SSH connections from source IP
- Justification: 90 days identifies recurring patterns; scoped to alert assets only

**Investigation Steps:**
1. Retrieved full Claroty alert (Rule 4782, High severity, 14:32:15 UTC)
2. Identified assets in Asset DB (jump server, file server, both Critical/High)
3. Queried firewall logs (24h) → Only SSH to 10.10.5.25
4. Retrieved SSH auth logs → Public key auth, fingerprint aa:bb:cc:dd:ee:ff
5. Verified key in IT Ops registry → Match to authorized backup key
6. SIEM query (90 days) → 87 occurrences at 02:00 UTC daily
7. Contacted IT Ops → Confirmed backup schedule (documented)
8. Checked endpoint logs (jump server) → No IOCs

**Dead Ends:**
- Threat intel lookup → No matches (internal IP)
- Jump server IOC search → Clean
- SIEM concurrent alerts → None

**Peer Consultation:**
- IT Operations Manager confirmed backup schedule (email 2024-11-09 15:00 UTC)

**Conclusion:** Hypothesis refuted - Authorized backup operation (False Positive)
```

**Methodology Score:** 6/6 = 100%

---

#### Example 2: Superficial Methodology

```
Alert: Suspicious SSH Activity

Investigation: This is SSH traffic. Internal IPs. Probably normal.

Disposition: False Positive
```

**Methodology Failures:**
✗ No hypothesis stated
✗ Only 1 data source (alert itself)
✗ No scope defined
✗ No investigation steps documented
✗ No dead ends noted
✗ No peer consultation

**Methodology Score:** 0/6 = 0% (Inadequate)

---

### Weighting Rationale

**Why 10% (Moderate Weight)?**

Sound methodology increases consistency and quality across investigations. While good methodology alone doesn't guarantee correct conclusions (evidence quality matters more), poor methodology leads to missed evidence, confirmation bias, and unreliable results.

**Impact of Poor Methodology:**

- No hypothesis → Unfocused investigation, missed evidence
- Single data source → Incomplete picture, misleading conclusions
- No documentation → Can't reproduce, can't verify
- Ignoring dead ends → Looks like investigation skipped important checks
- No peer review → Errors and biases go undetected

**Quality Thresholds:**

**Excellent (6/6):** Systematic, thorough, well-documented investigation
**Good (4-5/6):** Adequate methodology with minor gaps
**Needs Improvement (3/6):** Superficial methodology, missing key elements
**Inadequate (<3/6):** No discernible methodology, ad-hoc investigation

# BMAD-1898 Priority Framework

## Introduction

The BMAD-1898 Priority Framework uses **multi-factor risk assessment** to prioritize vulnerabilities based on genuine exploitable threat, not severity alone. This approach reduces alert fatigue by focusing remediation efforts on vulnerabilities that pose real risk.

**Core Principle:** CVSS + EPSS + KEV + Business Context = Accurate Priority

---

## Priority Levels (P1-P5)

### P1 - Critical (24 Hour SLA)

**Definition:** Immediate action required. Critical vulnerabilities with high exploitability affecting critical systems. War room may be needed.

**Criteria (ANY of the following):**

1. **CVSS ≥9.0 + EPSS ≥0.75 + KEV Listed**
   - Critical severity + very high exploitation probability + active exploitation confirmed

2. **Active Exploitation + Internet-Facing + Critical ACR**
   - Any CVSS with confirmed exploitation in wild + public exposure + mission-critical system

3. **KEV Listed + Internet-Facing + Critical ACR**
   - CISA-confirmed exploitation + public exposure + mission-critical system

**Examples:**

**Example 1: Apache Struts 2 RCE**

- CVE-2024-1234
- CVSS: 9.8 (Critical)
- EPSS: 0.85 (97th percentile - very high exploitation probability)
- KEV: Listed (2024-11-01)
- System: Internet-facing production web server
- ACR: Critical
- **Priority: P1** (All factors indicate immediate high risk)

**Example 2: Zero-Day RCE with Active Exploitation**

- CVE-2024-5678
- CVSS: 8.5 (High)
- EPSS: 0.95 (99th percentile)
- KEV: Listed
- System: Internet-facing API gateway
- ACR: Critical
- Active exploitation: Confirmed in threat intelligence
- **Priority: P1** (Active exploitation + critical system)

**SLA Timeline:** 24 hours from enrichment completion

**Actions Required:**

- Immediate notification to security leadership
- Emergency change approval (bypass standard CAB)
- Deploy patch or workaround within 24 hours
- If patch unavailable: Implement compensating controls or take system offline
- Post-incident review after remediation

**Review Requirement:** Mandatory peer review

---

### P2 - High (7 Day SLA)

**Definition:** Urgent action required. High severity vulnerabilities with significant exploitability or important systems affected.

**Criteria (ANY of the following):**

1. **CVSS ≥7.0 + EPSS ≥0.50 + (KEV Listed OR Public Exploit)**
   - High severity + high exploitation probability + exploit available

2. **CVSS ≥9.0 + High ACR + Internet-Facing**
   - Critical CVSS + important system + public exposure (even without active exploitation)

3. **KEV Listed + Internal Network + High ACR**
   - Active exploitation confirmed, but system is internal (not internet-facing)

**Examples:**

**Example 1: SQL Injection with Public PoC**

- CVE-2024-7890
- CVSS: 8.0 (High)
- EPSS: 0.65 (85th percentile)
- KEV: Not Listed
- Exploit: Public PoC available on GitHub
- System: Internet-facing e-commerce platform
- ACR: High
- **Priority: P2** (High severity + public exploit + important system)

**Example 2: Internal Critical System, High CVSS**

- CVE-2024-1111
- CVSS: 9.5 (Critical)
- EPSS: 0.20 (low exploitation probability)
- KEV: Not Listed
- System: Internal finance database
- ACR: Critical
- Exposure: Internal network only
- **Priority: P2** (Critical system despite lower exploitability)

**SLA Timeline:** 7 days from enrichment completion

**Actions Required:**

- Notify security team and system owners
- Schedule patch deployment within 7 days
- Implement monitoring and compensating controls until patched
- Document remediation plan
- Verify patch applied successfully

**Review Requirement:** Mandatory peer review

---

### P3 - Medium (30 Day SLA)

**Definition:** Important but not urgent. Moderate severity or exploitability. Planned patching in regular maintenance window.

**Criteria (ANY of the following):**

1. **CVSS 4.0-6.9 + EPSS 0.25-0.49 + Internal Exposure**
   - Medium severity + moderate exploitability + internal system

2. **CVSS ≥7.0 + EPSS <0.25 + Effective Compensating Controls**
   - High CVSS but low exploitability with mitigations in place

3. **Medium ACR + CVSS 4.0-6.9 + No Public Exploit**
   - Standard business system, moderate severity, theoretical risk

**Examples:**

**Example 1: Medium Severity Internal System**

- CVE-2024-2222
- CVSS: 6.5 (Medium)
- EPSS: 0.30 (moderate)
- KEV: Not Listed
- System: Internal HR portal
- ACR: Medium
- Exposure: Internal network
- **Priority: P3** (Moderate risk, internal system)

**Example 2: High CVSS but Low Exploitability with WAF**

- CVE-2024-3333
- CVSS: 8.0 (High)
- EPSS: 0.15 (low)
- KEV: Not Listed
- System: Internet-facing web app
- ACR: High
- Compensating Control: WAF with virtual patching
- **Priority: P3** (Mitigated by WAF, low exploitation probability)

**SLA Timeline:** 30 days from enrichment completion

**Actions Required:**

- Schedule patch deployment in next monthly maintenance window
- Implement monitoring and basic compensating controls
- No emergency change required
- Document in monthly patching report

**Review Requirement:** 25% random sampling review

---

### P4 - Low (90 Day SLA)

**Definition:** Routine patching. Low severity or low exploitability. Minimal business impact.

**Score Threshold:** 6-9 points

**Criteria (ANY of the following):**

1. **CVSS <4.0 + Any EPSS + Any System**
   - Low severity regardless of other factors

2. **Low ACR + CVSS <7.0 + No Exploit**
   - Development/test systems with moderate severity, no exploitation

3. **Isolated System + CVSS <7.0**
   - Air-gapped or heavily isolated systems with moderate severity

**Examples:**

**Example 1: Low Severity, Any System**

- CVE-2024-4444
- CVSS: 3.5 (Low)
- EPSS: 0.10
- KEV: Not Listed
- System: Production web server
- ACR: Critical
- **Priority: P4** (CVSS <4.0 = Low priority despite critical system)

**Example 2: Dev Environment, Moderate Severity**

- CVE-2024-5555
- CVSS: 6.0 (Medium)
- EPSS: 0.05
- KEV: Not Listed
- System: Development database
- ACR: Low
- **Priority: P4** (Dev system = low priority)

**SLA Timeline:** 90 days from enrichment completion

**Actions Required:**

- Schedule patch in quarterly maintenance
- No compensating controls required
- Low monitoring priority
- Can be deferred if resource constraints

**Review Requirement:** 10% random sampling review

---

### P5 - Informational (No SLA)

**Definition:** Awareness only. Very low or theoretical risk. Optional patching.

**Score Threshold:** 0-5 points

**Criteria (ANY of the following):**

1. **CVSS <2.0 + No Exploit + Test Environment**
   - Very low severity in non-production

2. **End-of-Life System (Decommissioning Planned)**
   - System will be decommissioned before patch deployment

3. **Risk Accepted (Management Decision)**
   - Formal risk acceptance documented

**Examples:**

**Example 1: Theoretical Risk, Test System**

- CVE-2024-6666
- CVSS: 1.5 (Low)
- EPSS: 0.01
- KEV: Not Listed
- System: QA test environment
- ACR: Low
- **Priority: P5** (Minimal risk, test environment)

**Example 2: Decommissioning Planned**

- CVE-2024-7777
- CVSS: 7.0 (High)
- System: Legacy server scheduled for decommission in 2 weeks
- **Priority: P5** (System being replaced, no patching needed)

**SLA Timeline:** No SLA

**Actions Required:**

- Awareness only
- No patching required
- Optional patching if convenient
- Document in risk register

**Review Requirement:** 5% random sampling review

---

## Factor Weighting

### Priority Calculation Algorithm

```python
def calculate_priority(vuln, system):
    """
    Calculate vulnerability priority using multi-factor risk assessment.

    Args:
        vuln: Vulnerability object with cvss, epss, kev_status, exploit_status
        system: System object with acr (Asset Criticality Rating), exposure

    Returns:
        Priority level: "P1", "P2", "P3", "P4", or "P5"
    """
    score = 0

    # Input validation and defensive defaults
    cvss = getattr(vuln, 'cvss', None)
    epss = getattr(vuln, 'epss', None)
    kev_status = getattr(vuln, 'kev_status', 'Not Listed')
    exploit_status = getattr(vuln, 'exploit_status', 'Theoretical')
    acr = getattr(system, 'acr', 'Low')
    exposure = getattr(system, 'exposure', 'Isolated')

    # Validate critical inputs
    if cvss is None:
        raise ValueError("CVSS score is required for priority calculation")
    if epss is None:
        epss = 0.0  # Default to lowest exploitability if unavailable

    # Factor 1: CVSS (0-4 points)
    if cvss >= 9.0: score += 4
    elif cvss >= 7.0: score += 3
    elif cvss >= 4.0: score += 2
    else: score += 1

    # Factor 2: EPSS (0-4 points)
    if epss >= 0.75: score += 4
    elif epss >= 0.50: score += 3
    elif epss >= 0.25: score += 2
    else: score += 1

    # Factor 3: KEV (0-5 points)
    if kev_status == "Listed":
        score += 5

    # Factor 4: Asset Criticality Rating (0-4 points)
    acr_points = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    score += acr_points.get(acr, 1)  # Default to Low if invalid

    # Factor 5: System Exposure (0-3 points)
    exposure_points = {"Internet": 3, "Internal": 2, "Isolated": 1}
    score += exposure_points.get(exposure, 1)  # Default to Isolated if invalid

    # Factor 6: Exploit Availability (0-4 points)
    exploit_points = {
        "Active Exploitation": 4,
        "Public Exploit": 3,
        "PoC": 2,
        "Theoretical": 1
    }
    score += exploit_points.get(exploit_status, 1)  # Default to Theoretical if invalid

    # Map score to priority (max 24 points)
    # KEV-listed vulnerabilities are elevated but nuanced by context
    if score >= 20:
        return "P1"
    elif score >= 15 or kev_status == "Listed":
        # KEV elevates to at least P2 (matches P2 criteria #3: KEV + Internal + High ACR)
        return "P2"
    elif score >= 10:
        return "P3"
    elif score >= 6:
        return "P4"
    else:
        return "P5"
```

### Factor Weights Summary

| Factor   | Weight   | Rationale                                          |
| -------- | -------- | -------------------------------------------------- |
| CVSS     | 4 points | Severity matters, but not alone                    |
| EPSS     | 4 points | Exploitability is equally important as severity    |
| KEV      | 5 points | Active exploitation is strongest signal (override) |
| ACR      | 4 points | Business impact is critical                        |
| Exposure | 3 points | Internet-facing = higher risk                      |
| Exploit  | 4 points | Exploit availability = imminent risk               |

**Total Max Score:** 24 points

---

## Priority Modifiers (Override Rules)

### Automatic Priority Elevation (+1 or +2 levels)

**Compliance Requirement:**

- PCI-DSS Critical vulnerability: Elevate to P1 or P2
- HIPAA-regulated system: Elevate +1 level

**Previous Breach:**

- Similar vulnerability exploited in past: Elevate +1 level
- Same product/vendor as previous breach: Elevate +1 level

**Executive Mandate:**

- CEO/CIO/CISO mandate: Elevate to specified priority
- Board-level concern: Elevate to P1 or P2

**Ransomware Threat:**

- KEV with known ransomware use: Elevate to P1

---

### Priority Reduction (-1 level)

**Effective Compensating Controls:**

- WAF with virtual patching: Reduce -1 level
- Network segmentation isolates vulnerable system: Reduce -1 level
- System not accessible to attackers: Reduce -1 level

**Scheduled Decommissioning:**

- System decommissioning within 30 days: Reduce to P5
- System decommissioning within 90 days: Reduce -1 level

**Vendor End-of-Life (No Patch):**

- No patch available, vendor EOL: Consider risk acceptance (P5)
- Migration to supported version planned: Maintain current priority

---

## SLA Enforcement

### SLA Deadlines

| Priority | SLA Timeline | Calculation                     |
| -------- | ------------ | ------------------------------- |
| P1       | 24 hours     | Enrichment timestamp + 24 hours |
| P2       | 7 days       | Enrichment timestamp + 7 days   |
| P3       | 30 days      | Enrichment timestamp + 30 days  |
| P4       | 90 days      | Enrichment timestamp + 90 days  |
| P5       | No SLA       | N/A                             |

### SLA Tracking

**Deadline Calculation Example:**

- Enrichment completed: 2025-11-06 10:30:00 UTC
- Priority: P1 (24 hours)
- SLA Deadline: 2025-11-07 10:30:00 UTC

**SLA Breach:**

- Definition: Remediation not completed by deadline
- Action: Escalate to management, document reason for delay

---

## Quick Reference Table

| Priority | CVSS    | EPSS      | KEV               | ACR      | Exposure          | SLA  | Review |
| -------- | ------- | --------- | ----------------- | -------- | ----------------- | ---- | ------ |
| P1       | 9.0+    | 0.75+     | Listed            | Critical | Internet          | 24h  | 100%   |
| P2       | 7.0+    | 0.50+     | Listed or Exploit | High     | Internet/Internal | 7d   | 100%   |
| P3       | 4.0-6.9 | 0.25-0.49 | Not Listed        | Medium   | Internal          | 30d  | 25%    |
| P4       | <4.0    | Any       | Not Listed        | Low      | Any               | 90d  | 10%    |
| P5       | <2.0    | Any       | Not Listed        | Low      | Test/Decom        | None | 5%     |

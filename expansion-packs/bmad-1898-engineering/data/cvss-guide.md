# CVSS (Common Vulnerability Scoring System) Guide

## Table of Contents

1. [Introduction to CVSS](#introduction-to-cvss)
2. [CVSS v3.1 Scoring](#cvss-v31-scoring)
3. [CVSS v4.0 Differences](#cvss-v40-differences)
4. [Severity Ratings](#severity-ratings)
5. [Common Scoring Pitfalls](#common-scoring-pitfalls)
6. [CVSS Calculation Examples](#cvss-calculation-examples)
7. [Integration with Risk Prioritization](#integration-with-risk-prioritization)
8. [Authoritative References](#authoritative-references)

---

## Introduction to CVSS

### What CVSS Measures

**CVSS measures vulnerability severity, NOT risk.**

CVSS provides a standardized method to capture the principal characteristics of a vulnerability and produce a numerical score (0.0-10.0) reflecting its severity. The score translates to a qualitative representation (None, Low, Medium, High, Critical) to help organizations properly assess and prioritize vulnerability remediation.

**Critical Distinction:**
- **Severity** (CVSS): How bad is the vulnerability **IF** exploited?
- **Risk**: What is the **likelihood** of exploitation combined with business impact?
- **Exploitability** (EPSS): What is the **probability** of exploitation in the wild?

CVSS should always be combined with other factors (EPSS, KEV status, business context) for effective risk prioritization.

### CVSS Versions

#### CVSS v3.1 (Current Standard)

**Status:** Widely adopted industry standard (2019-present)

**When to Use:**
- Default choice for most vulnerability assessments
- Maximum compatibility with existing tools and databases
- NVD (National Vulnerability Database) uses CVSS v3.1 as primary scoring
- Most CVE records include CVSS v3.1 scores

**Characteristics:**
- Formula-based scoring calculation
- 8 base metrics, 3 temporal metrics, 5 environmental metrics
- Well-understood and extensively documented
- Broad tool support and integration

#### CVSS v4.0 (Next Generation)

**Status:** Released 2023, adoption growing

**When to Use:**
- Assessing systems with safety implications (IEC 61508 safety ratings)
- Need to assess subsequent system impacts separately
- Require supplemental metrics (Automatable, Recovery, Safety, etc.)
- Advanced use cases requiring granular impact separation

**Key Differences from v3.1:**
- MacroVector-based scoring (not formula-based)
- Attack Requirements (AT) metric replaces some v3.1 complexity
- Separate vulnerable system vs. subsequent system impacts
- Supplemental metrics for advanced assessments
- Safety considerations for human injury risk

**Recommendation:** Use CVSS v3.1 for general assessments unless you have specific v4.0 requirements (safety, subsequent system impacts, supplemental metrics).

---

## CVSS v3.1 Scoring

### Base Metrics Group

Base metrics represent the intrinsic characteristics of a vulnerability that are constant over time and across user environments.

#### Exploitability Metrics

These describe how the vulnerability can be exploited:

##### 1. Attack Vector (AV)

**Measures:** How remote an attacker must be to exploit the vulnerability

**Values:**
- **Network (N)**: Exploitable remotely over a network (e.g., internet, WAN)
  - Example: Remote Code Execution via HTTP request
  - Most severe (easily accessible by attackers)
- **Adjacent (A)**: Requires network access to local network segment
  - Example: ARP spoofing, local network MITM attacks
  - Limited to attackers on same network (LAN, Bluetooth, etc.)
- **Local (L)**: Requires local system access (logged in user, shell access)
  - Example: Local privilege escalation
  - Attacker must have direct access to system
- **Physical (P)**: Requires physical access to device
  - Example: Firmware extraction via JTAG
  - Least severe (requires physical presence)

**Impact on Score:** Network has highest score impact, Physical has lowest

##### 2. Attack Complexity (AC)

**Measures:** Conditions beyond attacker control required for successful exploitation

**Values:**
- **Low (L)**: No special conditions required
  - Attacker can exploit reliably and repeatedly
  - No race conditions, no specific configurations needed
  - Example: Straightforward buffer overflow
- **High (H)**: Special conditions must exist
  - Success depends on environmental factors outside attacker control
  - May require race condition wins, specific configurations, timing
  - Example: Exploitation requires non-default configuration or timing attack

**Impact on Score:** Low (easier to exploit) increases score, High decreases score

##### 3. Privileges Required (PR)

**Measures:** Level of privileges attacker must have before successful exploitation

**Values:**
- **None (N)**: No privileges required (unauthenticated attack)
  - Attacker has no prior access
  - Example: Unauthenticated remote code execution
  - Highest severity
- **Low (L)**: Basic user privileges required
  - Standard user account access needed
  - Example: Authenticated user can escalate to admin
- **High (H)**: Administrator/significant privileges required
  - Must already have elevated access
  - Example: Admin user can exploit kernel vulnerability
  - Lowest severity (limited attack surface)

**Impact on Score:** None has highest impact, High has lowest

##### 4. User Interaction (UI)

**Measures:** Whether exploitation requires action by a user other than the attacker

**Values:**
- **None (N)**: No user interaction required
  - Attacker can exploit vulnerability independently
  - Example: Server-side RCE without user action
  - Higher severity
- **Required (R)**: Victim must perform specific action
  - User must click link, open file, visit website, etc.
  - Example: XSS requiring user to click malicious link
  - Lower severity (requires social engineering)

**Impact on Score:** None increases score, Required decreases score

#### Scope (S)

**Measures:** Whether successful exploitation impacts resources beyond the vulnerable component's security authority

**Critical Concept:** Scope determines if the vulnerability allows attacker to affect resources governed by a different security authority than the vulnerable component.

**Values:**
- **Unchanged (U)**: Impacts limited to vulnerable component
  - Exploited privileges constrained to vulnerable component
  - Example: Local file read in web application stays within app context
  - Score calculation uses standard formula
- **Changed (C)**: Impacts extend beyond vulnerable component
  - Exploited vulnerability affects resources outside its security scope
  - Example: VM escape allowing host OS access from guest VM
  - Example: Container breakout affecting host system
  - Significantly increases score (broader impact)

**Impact on Score:** Changed scope dramatically increases severity scores

#### Impact Metrics

These measure the consequences of successful exploitation:

##### 5. Confidentiality Impact (C)

**Measures:** Impact on confidentiality of information managed by the component

**Values:**
- **High (H)**: Total information disclosure
  - All information within impacted component disclosed
  - Example: Database dump exposing all records
- **Low (L)**: Some information disclosed
  - Attacker gains access to limited information
  - Example: Leak of individual user record
- **None (N)**: No impact on confidentiality
  - No information disclosed

##### 6. Integrity Impact (I)

**Measures:** Impact on integrity of data or system

**Values:**
- **High (H)**: Total compromise of data integrity
  - Attacker can modify all data or critical system files
  - Example: Remote code execution allowing arbitrary file modification
- **Low (L)**: Limited integrity impact
  - Attacker can modify some data but not critical data
  - Example: Modification of user-controlled preference file
- **None (N)**: No integrity impact

##### 7. Availability Impact (A)

**Measures:** Impact on availability of the vulnerable component

**Values:**
- **High (H)**: Total loss of availability
  - Complete denial of service
  - Example: Kernel panic causing system crash
- **Low (L)**: Reduced performance or intermittent availability
  - Partial denial of service
  - Example: Resource exhaustion causing slowdown
- **None (N)**: No availability impact

### Temporal Metrics Group (Optional)

Temporal metrics reflect characteristics that change over time but remain constant across user environments.

**When to Use:** When you need to adjust base score based on current state of exploit code, patches, or confidence in vulnerability report.

#### Exploit Code Maturity (E)

**Values:**
- **Not Defined (X)**: Skip temporal scoring (use base score)
- **High (H)**: Functional autonomous exploit exists
- **Functional (F)**: Functional exploit code available
- **Proof-of-Concept (P)**: PoC code available
- **Unproven (U)**: No known exploit code

**Impact:** Higher maturity increases temporal score (easier to exploit now)

#### Remediation Level (RL)

**Values:**
- **Not Defined (X)**: Skip temporal scoring
- **Unavailable (U)**: No patch or workaround available
- **Workaround (W)**: Unofficial workaround available
- **Temporary Fix (T)**: Official temporary fix available
- **Official Fix (O)**: Official patch available

**Impact:** Availability of patches decreases temporal score (less urgent if fixed)

#### Report Confidence (RC)

**Values:**
- **Not Defined (X)**: Skip temporal scoring
- **Confirmed (C)**: Vulnerability confirmed by vendor or researcher
- **Reasonable (R)**: Vulnerability reported with reasonable evidence
- **Unknown (U)**: Unconfirmed report

**Impact:** Lower confidence decreases temporal score (may not be real)

### Environmental Metrics Group (Optional)

Environmental metrics customize CVSS score based on organization-specific factors.

**When to Use:** When you need to adjust severity based on your specific environment, security requirements, or modified base characteristics.

#### Security Requirements (CR, IR, AR)

Rate the importance of Confidentiality, Integrity, and Availability to your organization:
- **Not Defined (X)**: Use default (assume Medium)
- **High (H)**: Loss would have catastrophic impact
- **Medium (M)**: Loss would have serious impact
- **Low (L)**: Loss would have limited impact

**Example:** Database containing customer PII:
- CR: High (confidentiality critical)
- IR: High (integrity critical)
- AR: Medium (availability important but not critical)

#### Modified Base Metrics

Override any base metric to reflect your specific environment:
- **Modified Attack Vector (MAV)**
- **Modified Attack Complexity (MAC)**
- **Modified Privileges Required (MPR)**
- **Modified User Interaction (MUI)**
- **Modified Scope (MS)**
- **Modified Confidentiality (MC)**
- **Modified Integrity (MI)**
- **Modified Availability (MA)**

**Example:** Vulnerability requires Network attack vector (AV:N), but in your environment, the vulnerable system is air-gapped:
- MAV: Physical (mitigated by network isolation)
- Environmental score will be significantly lower

---

## CVSS v4.0 Differences

### Major Changes from v3.1

#### 1. Attack Requirements (AT) Metric

**Replaces:** Some aspects of Attack Complexity from v3.1

**Purpose:** Captures prerequisite deployment and execution conditions beyond attacker control

**Values:**
- **None**: No special conditions required
- **Present**: Specific conditions must exist (race conditions, non-default configurations, etc.)

**Difference from v3.1 AC:** More granular capture of environmental prerequisites

#### 2. Subsequent System Impact Separation

**v3.1 Limitation:** Impact metrics (C/I/A) measure combined impact on vulnerable system

**v4.0 Enhancement:** Separate metrics for:
- **Vulnerable System Impact**: Impact on the initially exploited component
- **Subsequent System Impact**: Impact on other systems affected downstream

**Example Use Case:**
- Vulnerable System: IoT device (low impact if compromised)
- Subsequent System: Industrial control system controlled by IoT device (high safety impact)

#### 3. Supplemental Metrics

**New Optional Metrics in v4.0:**

- **Automatable (AU)**: Can exploitation be automated?
  - Yes (Y): Attackers can fully automate exploitation
  - No (N): Requires manual intervention
- **Recovery (RE)**: How difficult is recovery from attack?
  - Automatic (A): System automatically recovers
  - User (U): User action required for recovery
  - Irrecoverable (I): Unrecoverable loss
- **Value Density (VD)**: Concentration of valuable resources
  - Diffuse (D): Resources spread across many systems
  - Concentrated (C): High-value resources in single location
- **Vulnerability Response Effort (VRE)**: Effort required to remediate
  - Low (L): Minimal effort (apply patch)
  - Moderate (M): Moderate effort (configuration changes)
  - High (H): Significant effort (code refactoring)
- **Provider Urgency (PU)**: Vendor-assigned urgency
  - Clear, Amber, Red, Green (traffic light system)

#### 4. Safety Metric

**New in v4.0:** Ability to represent human safety impact using IEC 61508 definitions

**Values:**
- **Negligible (N)**: No safety impact
- **Present (P)**: Safety impact possible

**Critical for:** Industrial control systems, medical devices, automotive systems, IoT affecting physical safety

#### 5. Scoring Methodology

**v3.1:** Formula-based calculation
- Transparent mathematical formula
- Predictable score computation
- Easy to understand how metrics combine

**v4.0:** MacroVector interpolation
- 270 equivalence classes (MacroVectors)
- Scores interpolated within equivalence sets
- Based on expert comparison data (15M vectors analyzed)
- Less transparent but potentially more nuanced

#### 6. Vector String Nomenclature

**v3.1:** Single vector string (CVSS:3.1/AV:N/AC:L/...)

**v4.0:** Explicit nomenclature indicating which groups used:
- **CVSS-B**: Base metrics only
- **CVSS-BT**: Base + Threat (temporal equivalent)
- **CVSS-BE**: Base + Environmental
- **CVSS-BTE**: Base + Threat + Environmental

### When to Use v4.0 vs v3.1

| Scenario | Recommended Version | Rationale |
|----------|---------------------|-----------|
| General vulnerability assessment | **v3.1** | Industry standard, maximum tool compatibility |
| NVD/CVE database scoring | **v3.1** | NVD uses v3.1 as primary |
| Safety-critical systems (ICS, medical devices) | **v4.0** | Safety metric captures human injury risk |
| Subsequent system impact matters | **v4.0** | Separate impact assessment for downstream effects |
| Need automation/recovery assessments | **v4.0** | Supplemental metrics provide this context |
| Legacy tool compatibility required | **v3.1** | Broader ecosystem support |
| Advanced risk modeling | **v4.0** | More granular metrics for sophisticated analysis |

**Default Recommendation:** Use **CVSS v3.1** unless you have specific v4.0 requirements.

---

## Severity Ratings

CVSS base scores map to qualitative severity ratings:

| Severity Rating | CVSS Score Range | Interpretation |
|----------------|------------------|----------------|
| **None** | 0.0 | No vulnerability (informational only) |
| **Low** | 0.1 - 3.9 | Minimal impact; low priority for remediation |
| **Medium** | 4.0 - 6.9 | Moderate impact; schedule remediation based on risk |
| **High** | 7.0 - 8.9 | Significant impact; prioritize remediation |
| **Critical** | 9.0 - 10.0 | Severe impact; immediate remediation required |

### Severity Rating Guidelines

#### None (0.0)
- No actual vulnerability (configuration guidance, informational advisories)
- No remediation action required
- May still warrant documentation for awareness

#### Low (0.1 - 3.9)
- Limited impact scope
- Requires significant privileges or unlikely conditions
- Often information disclosure of non-sensitive data
- Remediate during regular maintenance windows
- **Example:** Local low-privilege user can read non-sensitive log file

#### Medium (4.0 - 6.9)
- Moderate impact if exploited
- May require user interaction or specific conditions
- Partial compromise of confidentiality, integrity, or availability
- Schedule remediation based on risk assessment
- **Example:** Authenticated user can trigger denial of service

#### High (7.0 - 8.9)
- Significant impact on confidentiality, integrity, or availability
- May allow unauthorized access or data compromise
- Prioritize remediation (target 30 days or less)
- **Example:** Unauthenticated remote code execution with scope unchanged

#### Critical (9.0 - 10.0)
- Severe impact across multiple CIA dimensions
- Often network-exploitable with no privileges required
- Frequently scope-changing vulnerabilities
- Immediate remediation required (target 7-14 days)
- **Example:** Unauthenticated remote code execution with scope change

### Important Considerations

1. **CVSS Severity ≠ Remediation Priority**
   - A Critical CVSS score doesn't automatically mean "drop everything"
   - Must combine with EPSS (exploitability), KEV (active exploitation), and business context

2. **Context Matters**
   - Air-gapped system: Network vulnerabilities have lower real-world severity
   - Internet-facing system: Network vulnerabilities require urgent attention
   - Use Environmental metrics to adjust for your context

3. **Severity Thresholds**
   - 7.0 is a common threshold for "high priority" patching policies
   - Some organizations use 9.0+ for emergency patching
   - Define your own thresholds based on risk tolerance

---

## Common Scoring Pitfalls

### 1. Over-Reliance on Base Score

**Pitfall:** Using only the base CVSS score for prioritization decisions

**Why It's Wrong:**
- Base score is **context-independent** (assumes worst-case scenario)
- Ignores temporal factors (exploit availability, patches)
- Ignores environmental factors (your specific deployment)
- Doesn't account for exploitability probability (EPSS)
- Doesn't capture active exploitation (KEV status)

**Solution:**
- Always consider temporal metrics if exploit code exists or patches available
- Use environmental metrics to customize for your environment
- Combine CVSS with EPSS and KEV for complete risk picture
- Apply business context (asset criticality, data sensitivity)

**Example:**
```
CVE-2024-XXXX
- Base Score: 9.8 (Critical)
- Temporal Score: 7.2 (Official patch available, no known exploits)
- Environmental Score: 4.5 (system air-gapped, low security requirements)
- EPSS: 0.02% (very low exploitability)
- KEV: Not in catalog (no confirmed exploitation)
- Business Context: Test environment, non-production

Risk Priority: P3 (Medium) despite Critical base score
```

### 2. Confusing CVSS with EPSS

**Pitfall:** Treating CVSS score as exploitability probability

**Why It's Wrong:**
- **CVSS answers:** "How severe is the impact IF exploited?"
- **EPSS answers:** "What's the probability of exploitation in next 30 days?"
- They measure completely different things

**Solution:**
- Use CVSS for severity (impact magnitude)
- Use EPSS for exploitability (likelihood)
- Combine both for risk = severity × likelihood

**Example:**
```
Scenario A: CVSS 9.8, EPSS 0.95 → Critical & Highly Exploitable → P1
Scenario B: CVSS 9.8, EPSS 0.02 → Critical & Unlikely Exploited → P2
Scenario C: CVSS 5.3, EPSS 0.95 → Medium & Highly Exploitable → P2
Scenario D: CVSS 5.3, EPSS 0.02 → Medium & Unlikely Exploited → P3
```

### 3. Ignoring Scope Changes

**Pitfall:** Underestimating impact of scope-changing vulnerabilities

**Why It's Wrong:**
- Scope change (S:C) dramatically increases CVSS score
- Indicates vulnerability breaks security boundaries
- Often enables lateral movement or privilege escalation across security contexts
- Critical for containerization, virtualization, sandboxing security

**Solution:**
- Carefully evaluate if exploitation affects resources outside vulnerable component's authority
- Recognize scope changes as especially severe (VM escape, container breakout, sandbox escape)
- Prioritize scope-changing vulnerabilities higher than base score alone suggests

**Example:**
```
VM Escape Vulnerability
- Without Scope Change (S:U): CVSS ~7.5 (High)
- With Scope Change (S:C): CVSS ~9.9 (Critical)

The scope change reflects that attacker escapes VM guest to compromise host,
affecting all other VMs on the hypervisor - a massive security boundary breach.
```

### 4. Not Adjusting for Environmental Factors

**Pitfall:** Applying generic base scores without considering deployment context

**Why It's Wrong:**
- Your environment may significantly reduce (or increase) actual risk
- Network isolation, compensating controls, security requirements vary
- Base score assumes worst-case deployment scenario

**Solution:**
- Use environmental metrics to customize scores
- Document environmental assumptions in vulnerability assessments
- Adjust prioritization based on real-world deployment

**Examples:**

**Air-Gapped System:**
```
Base: AV:N → Environmental: MAV:P (network attack impossible, requires physical access)
Base Score: 9.8 → Environmental Score: 4.2
```

**High Confidentiality Requirement:**
```
Base: C:L (low confidentiality impact)
Environmental: CR:H (high confidentiality requirement in our environment)
Base Score: 5.3 → Environmental Score: 6.8 (higher due to business criticality)
```

### 5. Ignoring Temporal Factors

**Pitfall:** Not updating CVSS scores as situation evolves

**Why It's Wrong:**
- Exploit code availability changes over time (increases urgency)
- Patch availability changes over time (decreases urgency)
- Confidence in vulnerability details evolves (affects accuracy)

**Solution:**
- Re-evaluate temporal metrics periodically
- Track when exploit code becomes publicly available (PoC → Functional → Weaponized)
- Update scores when patches released
- Use EPSS for real-time exploitability trends

**Timeline Example:**
```
Day 0 (Disclosure):
- E:U (Unproven), RL:U (Unavailable), RC:R (Reasonable)
- Temporal Score: 8.5

Day 7 (PoC Published):
- E:P (PoC), RL:U (Unavailable), RC:C (Confirmed)
- Temporal Score: 9.1 (increased urgency)

Day 14 (Vendor Patch):
- E:P (PoC), RL:O (Official Fix), RC:C (Confirmed)
- Temporal Score: 7.8 (decreased urgency - patch available)

Day 30 (Weaponized Exploit):
- E:H (High - automated exploit), RL:O (Official Fix), RC:C (Confirmed)
- Temporal Score: 8.4 (increased urgency - easy exploitation)
```

### 6. Inconsistent Metric Application

**Pitfall:** Applying CVSS metrics inconsistently across vulnerabilities

**Why It's Wrong:**
- Leads to incomparable scores
- Makes prioritization unreliable
- Undermines confidence in scoring process

**Solution:**
- Use standardized scoring guidelines
- Train analysts on metric definitions
- Review scores for consistency
- Document scoring rationale for complex cases
- Use CVSS calculator tools (NVD calculator) to ensure correct formula application

### 7. Treating CVSS as Absolute Truth

**Pitfall:** Assuming CVSS scores are objective and infallible

**Why It's Wrong:**
- CVSS requires subjective judgment (especially Attack Complexity, Scope)
- Different analysts may score same vulnerability differently
- Scores may not perfectly reflect real-world risk
- CVSS doesn't capture all risk dimensions (threat actor capability, asset value, data sensitivity)

**Solution:**
- Use CVSS as one input to risk decisions, not the only input
- Document scoring assumptions and rationale
- Accept reasonable score variations (7.8 vs 8.1 both indicate "High")
- Combine with threat intelligence, asset criticality, business context
- When in doubt, reference NVD scores for consistency

---

## CVSS Calculation Examples

### Example 1: Unauthenticated Remote Code Execution (Critical)

**Scenario:** Web application allows unauthenticated attackers to execute arbitrary commands on the server via crafted HTTP requests.

**CVSS v3.1 Vector:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`

**Metric Breakdown:**
- **AV:N (Network)**: Exploitable remotely over internet
- **AC:L (Low)**: No special conditions required; reliable exploitation
- **PR:N (None)**: No authentication required
- **UI:N (None)**: No user interaction needed
- **S:U (Unchanged)**: Impact limited to vulnerable application
- **C:H (High)**: Attacker can read all application data
- **I:H (High)**: Attacker can modify all application data
- **A:H (High)**: Attacker can crash or disable application

**CVSS Base Score:** **9.8 (Critical)**

**Severity Justification:**
- Network-exploitable without authentication
- Complete compromise of confidentiality, integrity, and availability
- Trivial to exploit (low complexity, no user interaction)
- Maximum severity for unchanged scope

**Remediation Priority:** P1 (Immediate) - especially if internet-facing

---

### Example 2: Authenticated Remote Code Execution with Scope Change (Critical)

**Scenario:** Container runtime vulnerability allows authenticated user to escape container and execute code on host operating system.

**CVSS v3.1 Vector:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`

**Metric Breakdown:**
- **AV:N (Network)**: Exploitable over network
- **AC:L (Low)**: Straightforward exploitation
- **PR:L (Low)**: Requires basic authenticated user access
- **UI:N (None)**: No user interaction required
- **S:C (Changed)**: Breaks container security boundary to affect host
- **C:H (High)**: Full access to host and all containers
- **I:H (High)**: Can modify host system and all containers
- **A:H (High)**: Can crash host and all containers

**CVSS Base Score:** **9.9 (Critical)**

**Severity Justification:**
- Scope change reflects container escape (massive security boundary breach)
- Compromises not just vulnerable container, but entire host
- All other containers on host also affected
- Even higher than Example 1 due to scope change

**Remediation Priority:** P1 (Immediate) - container escapes are catastrophic

---

### Example 3: Local Privilege Escalation (High)

**Scenario:** Operating system kernel vulnerability allows local user with low privileges to gain root/administrator access.

**CVSS v3.1 Vector:** `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`

**Metric Breakdown:**
- **AV:L (Local)**: Requires local access to system (logged-in user)
- **AC:L (Low)**: Easy to exploit once local access obtained
- **PR:L (Low)**: Requires standard user account
- **UI:N (None)**: No interaction needed beyond running exploit
- **S:U (Unchanged)**: Privilege escalation within same system
- **C:H (High)**: Can read all system data after escalation
- **I:H (High)**: Can modify all system data after escalation
- **A:H (High)**: Can crash or disable system

**CVSS Base Score:** **7.8 (High)**

**Severity Justification:**
- Requires local access (lower than remote vulnerabilities)
- Complete system compromise once exploited
- Common attack pattern (exploit external vuln to get foothold, then escalate)

**Remediation Priority:** P2 (High) - combine with defense-in-depth to prevent initial access

---

### Example 4: Cross-Site Scripting (XSS) - Reflected (Medium)

**Scenario:** Web application reflects unsanitized user input in HTTP response, allowing JavaScript injection when victim clicks malicious link.

**CVSS v3.1 Vector:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`

**Metric Breakdown:**
- **AV:N (Network)**: Exploitable via network (malicious link)
- **AC:L (Low)**: Easy to craft malicious payload
- **PR:N (None)**: No authentication required
- **UI:R (Required)**: Victim must click malicious link
- **S:C (Changed)**: Can access victim's session in other origin (browser security boundary)
- **C:L (Low)**: Can steal session cookies, limited data
- **I:L (Low)**: Can perform actions as victim (limited scope)
- **A:N (None)**: No availability impact

**CVSS Base Score:** **6.1 (Medium)**

**Severity Justification:**
- Requires user interaction (social engineering needed)
- Limited impact (only affects users who click malicious link)
- Scope change reflects cross-origin attack capability
- Lower than RCE but still significant web vulnerability

**Remediation Priority:** P3 (Medium) - important but requires social engineering

---

### Example 5: Information Disclosure - Configuration File (Low)

**Scenario:** Web application exposes non-sensitive configuration file (software versions, plugin list) to unauthenticated users.

**CVSS v3.1 Vector:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`

**Metric Breakdown:**
- **AV:N (Network)**: Accessible over network
- **AC:L (Low)**: Simple HTTP GET request
- **PR:N (None)**: No authentication needed
- **UI:N (None)**: Direct access, no interaction
- **S:U (Unchanged)**: Information disclosure only
- **C:L (Low)**: Limited information disclosure (non-sensitive metadata)
- **I:N (None)**: No integrity impact
- **A:N (None)**: No availability impact

**CVSS Base Score:** **5.3 (Medium)**

**Severity Justification:**
- Information disclosure only (no direct compromise)
- May aid reconnaissance for more serious attacks
- No sensitive data exposed (just configuration metadata)

**Remediation Priority:** P4 (Low) - address during regular maintenance, may aid attackers but not critical alone

---

### Example 6: Denial of Service - Resource Exhaustion (Medium)

**Scenario:** Application crashes or becomes unresponsive when sent specially crafted requests, causing resource exhaustion.

**CVSS v3.1 Vector:** `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`

**Metric Breakdown:**
- **AV:N (Network)**: Exploitable remotely
- **AC:L (Low)**: Simple to trigger with crafted requests
- **PR:N (None)**: No authentication required
- **UI:N (None)**: Direct exploitation
- **S:U (Unchanged)**: Affects only vulnerable application
- **C:N (None)**: No confidentiality impact
- **I:N (None)**: No integrity impact
- **A:H (High)**: Complete denial of service

**CVSS Base Score:** **7.5 (High)**

**Severity Justification:**
- Complete availability loss
- Easy to exploit remotely without authentication
- However, no data compromise (only availability)

**Remediation Priority:** Depends on business criticality
- **P1** if service is business-critical (e.g., payment processing)
- **P2** if service is important but not critical
- **P3** if service is low priority

---

### Example 7: SQL Injection - Time-Based Blind (High)

**Scenario:** Web application vulnerable to time-based blind SQL injection requiring authentication, allowing data extraction via timing attacks.

**CVSS v3.1 Vector:** `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`

**Metric Breakdown:**
- **AV:N (Network)**: Exploitable over network
- **AC:L (Low)**: Reliable exploitation despite being "blind" injection
- **PR:L (Low)**: Requires authenticated user account
- **UI:N (None)**: No user interaction needed
- **S:U (Unchanged)**: Database access within application scope
- **C:H (High)**: Can extract entire database via timing attacks
- **I:H (High)**: Can modify database data
- **A:H (High)**: Can delete data or crash database

**CVSS Base Score:** **8.8 (High)**

**Severity Justification:**
- Complete database compromise possible
- Requires authentication (slightly lower than unauthenticated)
- SQL injection is critical vulnerability class

**Remediation Priority:** P1 (Immediate) - SQL injection always high priority regardless of authentication requirement

---

## Integration with Risk Prioritization

**Critical Principle:** CVSS severity alone does NOT determine remediation priority.

### Complete Risk Framework

Effective vulnerability prioritization requires combining multiple data sources:

```
Risk Priority = f(CVSS Severity, EPSS Probability, KEV Status, Business Context)
```

#### 1. CVSS: Severity Assessment

**Question:** How bad is the vulnerability IF exploited?

**Provides:**
- Impact magnitude (0.0 - 10.0)
- Attack characteristics (vector, complexity, privileges)
- Scope of compromise

**Limitations:**
- Doesn't predict likelihood of exploitation
- Doesn't capture business impact
- Doesn't reflect active exploitation

#### 2. EPSS: Exploitability Probability

**Question:** How likely is exploitation in the next 30 days?

**Provides:**
- Probability score (0.00000 - 1.00000)
- Percentile ranking (0th - 100th)
- Based on real-world exploitation data

**Integration with CVSS:**
```
High CVSS + High EPSS = P1 (Critical & Actively Targeted)
High CVSS + Low EPSS  = P2 (Critical But Unlikely)
Med CVSS + High EPSS  = P2 (Moderate But Exploited)
Med CVSS + Low EPSS   = P3 (Moderate & Unlikely)
```

**See:** `epss-guide.md` for detailed EPSS guidance

#### 3. KEV: Active Exploitation Confirmation

**Question:** Is this vulnerability being actively exploited in the wild?

**Provides:**
- CISA's authoritative confirmation of exploitation
- Mandatory remediation timeline (BOD 22-01: 14 days for federal agencies)
- Proof that threat is real, not theoretical

**Integration with CVSS:**
```
KEV Status = Yes → P1 (IMMEDIATE) regardless of CVSS or EPSS
KEV Status = No  → Use CVSS + EPSS + Business Context
```

**Critical Override Rule:**
```
IF vulnerability IN KEV catalog THEN
    Priority = P1 (Critical)
    Timeline = Immediate (14 days maximum)
ELSE
    Apply standard risk prioritization
END IF
```

**See:** `kev-catalog-guide.md` for detailed KEV catalog guidance

#### 4. Business Context

**Questions:**
- How critical is the affected asset?
- What data does it process?
- Is it internet-facing or internal?
- What compensating controls exist?
- What is the business impact of downtime?

**Provides:**
- Asset criticality weighting
- Data sensitivity considerations
- Exposure context
- Compensating control adjustments

### Prioritization Matrix

| CVSS | EPSS | KEV | Internet-Facing | Priority | Timeline |
|------|------|-----|----------------|----------|----------|
| 9.0+ | Any | Yes | Any | **P1** | Immediate (72 hours) |
| 7.0+ | >50% | Yes | Yes | **P1** | Immediate (72 hours) |
| 7.0+ | >50% | No | Yes | **P1** | 7 days |
| 7.0+ | <10% | No | Yes | **P2** | 30 days |
| 7.0+ | Any | No | No | **P2** | 30 days |
| 4.0-6.9 | >50% | Yes | Yes | **P2** | 14 days |
| 4.0-6.9 | >50% | No | Yes | **P2** | 30 days |
| 4.0-6.9 | <10% | No | Any | **P3** | 90 days |
| <4.0 | Any | Yes | Any | **P2** | 30 days (KEV override) |
| <4.0 | Any | No | Any | **P4** | Next maintenance window |

### Example Integration Scenarios

#### Scenario 1: Critical CVSS, High EPSS, In KEV

```
CVE-2024-1234: Remote Code Execution in Web Framework

CVSS v3.1: 9.8 (Critical)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H

EPSS: 0.856 (85.6% probability)
Percentile: 97th (top 3% of all vulnerabilities)

KEV: YES - Added 2024-01-15, Due 2024-01-29

Asset: Customer-facing web application (internet-facing)
Data: Customer PII, payment information (high sensitivity)
Criticality: Tier 1 (business-critical)

→ PRIORITY: P1 (CRITICAL - IMMEDIATE ACTION)
→ TIMELINE: 72 hours
→ ACTIONS:
  1. Emergency change control
  2. Deploy patch immediately
  3. If patch unavailable, implement WAF rules or take offline
  4. Verify no compromise occurred
  5. Document in incident response log
```

#### Scenario 2: Critical CVSS, Low EPSS, Not in KEV

```
CVE-2024-5678: Local Privilege Escalation in Driver

CVSS v3.1: 7.8 (High)
Vector: CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H

EPSS: 0.002 (0.2% probability)
Percentile: 45th (below median)

KEV: NO

Asset: Internal workstation driver
Data: Standard corporate data (medium sensitivity)
Criticality: Tier 3 (standard endpoint)
Compensating Controls: EDR deployed, restricted local admin, application whitelisting

→ PRIORITY: P2 (HIGH)
→ TIMELINE: 30 days
→ ACTIONS:
  1. Schedule patch deployment in normal cycle
  2. Verify compensating controls active
  3. Monitor for exploitation attempts via EDR
  4. Deploy via WSUS/patch management system
```

#### Scenario 3: Medium CVSS, High EPSS, Not in KEV

```
CVE-2024-9999: Authentication Bypass in VPN

CVSS v3.1: 6.5 (Medium)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N

EPSS: 0.752 (75.2% probability)
Percentile: 95th (top 5%)

KEV: NO (but high EPSS indicates active scanning)

Asset: Corporate VPN gateway (internet-facing)
Data: Internal network access (high value)
Criticality: Tier 1 (perimeter security)

→ PRIORITY: P1 (CRITICAL) - EPSS indicates active targeting
→ TIMELINE: 7 days
→ ACTIONS:
  1. Expedited patching (next change window)
  2. Enhanced monitoring of VPN authentication logs
  3. Review recent VPN access for anomalies
  4. Deploy patch during next maintenance window
  5. Consider temporary additional authentication controls
```

### Priority Framework Summary

**P1 (Critical) - Immediate Action (0-7 days):**
- Any vulnerability in CISA KEV catalog
- CVSS 9.0+ on internet-facing systems
- CVSS 7.0+ with EPSS >50% on internet-facing systems
- High business impact regardless of score

**P2 (High) - Urgent (7-30 days):**
- CVSS 7.0+ on internal systems
- CVSS 7.0+ with low EPSS on internet-facing systems
- CVSS 4.0-6.9 with high EPSS
- Medium business impact

**P3 (Medium) - Scheduled (30-90 days):**
- CVSS 4.0-6.9 with low EPSS
- Lower severity with specific business concerns
- Low business impact

**P4 (Low) - Maintenance Window (90+ days):**
- CVSS <4.0 (not in KEV)
- Informational findings
- Minimal business impact

---

## Authoritative References

### Official CVSS Specifications

**CVSS v3.1 Specification**
- URL: https://www.first.org/cvss/v3.1/specification-document
- Publisher: FIRST (Forum of Incident Response and Security Teams)
- Use: Primary reference for CVSS v3.1 metric definitions and scoring

**CVSS v4.0 Specification**
- URL: https://www.first.org/cvss/v4.0/specification-document
- Publisher: FIRST
- Use: Reference for CVSS v4.0 enhancements and new metrics

**CVSS User Guide**
- URL: https://www.first.org/cvss/user-guide
- Publisher: FIRST
- Use: Practical guidance on applying CVSS in real-world scenarios

### Scoring Tools

**NVD CVSS v3.1 Calculator**
- URL: https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator
- Publisher: NIST National Vulnerability Database
- Use: Interactive calculator for computing CVSS v3.1 scores

**FIRST CVSS v4.0 Calculator**
- URL: https://www.first.org/cvss/calculator/4.0
- Publisher: FIRST
- Use: Official calculator for CVSS v4.0 scores

### Databases and Scoring References

**National Vulnerability Database (NVD)**
- URL: https://nvd.nist.gov/
- Publisher: NIST
- Use: Authoritative source for CVE CVSS scores (primarily v3.1)
- Contains CVSS scores for all published CVEs

**CVE Program**
- URL: https://www.cve.org/
- Publisher: MITRE (sponsored by CISA)
- Use: CVE identifier assignment and vulnerability descriptions

### Complementary Risk Assessment Resources

**EPSS (Exploit Prediction Scoring System)**
- URL: https://www.first.org/epss/
- Use: Exploitability probability to complement CVSS severity
- See: `epss-guide.md` for detailed guidance

**CISA Known Exploited Vulnerabilities (KEV) Catalog**
- URL: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Use: Authoritative list of actively exploited CVEs
- See: `kev-catalog-guide.md` for detailed guidance

**FIRST Priority Framework**
- URL: https://www.first.org/ssvc/
- Use: Stakeholder-Specific Vulnerability Categorization (decision trees for prioritization)

### Training and Education

**FIRST CVSS Training**
- URL: https://www.first.org/cvss/training
- Publisher: FIRST
- Use: Official training materials for CVSS scoring

**NIST Vulnerability Metrics**
- URL: https://nvd.nist.gov/vuln-metrics
- Publisher: NIST
- Use: Overview of vulnerability scoring methodologies

### Version History and Change Logs

**CVSS Version History**
- CVSS v1.0: 2005 (deprecated)
- CVSS v2.0: 2007 (archived, still in some legacy systems)
- CVSS v3.0: 2015 (superseded by v3.1)
- CVSS v3.1: 2019 (current industry standard)
- CVSS v4.0: 2023 (next generation, growing adoption)

**Migration Guidance**
- v2 to v3.1: https://www.first.org/cvss/v3.1/migration
- v3.1 to v4.0: https://www.first.org/cvss/v4.0/transition-guide

---

## Document Metadata

**Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** Security Engineering Team
**Audience:** Security Analysts, Vulnerability Researchers, Risk Management
**Related Documents:**
- `epss-guide.md` - EPSS exploitability probability guidance
- `kev-catalog-guide.md` - CISA KEV catalog usage
- `priority-framework.md` - Complete vulnerability prioritization framework
- `mitre-attack-mapping-guide.md` - MITRE ATT&CK technique mapping

**Document Purpose:** Comprehensive reference for understanding, applying, and integrating CVSS scores into vulnerability management and risk prioritization workflows.

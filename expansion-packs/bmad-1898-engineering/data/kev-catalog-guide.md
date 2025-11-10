# CISA KEV (Known Exploited Vulnerabilities) Catalog Guide

## Table of Contents

1. [Introduction to KEV Catalog](#introduction-to-kev-catalog)
2. [Why KEV Matters](#why-kev-matters)
3. [Checking KEV Catalog](#checking-kev-catalog)
4. [KEV Catalog Fields](#kev-catalog-fields)
5. [Prioritization Implications](#prioritization-implications)
6. [KEV Examples](#kev-examples)
7. [Integration with Risk Prioritization](#integration-with-risk-prioritization)
8. [BOD 22-01 Requirements](#bod-22-01-requirements)
9. [Authoritative References](#authoritative-references)

---

## Introduction to KEV Catalog

### What is the KEV Catalog?

**CISA's Known Exploited Vulnerabilities (KEV) Catalog is the authoritative U.S. government list of CVEs with confirmed active exploitation in the wild.**

**Maintained by:** Cybersecurity and Infrastructure Security Agency (CISA), U.S. Department of Homeland Security

**Purpose:** Provide network defenders with a curated, authoritative list of vulnerabilities that pose the highest risk due to **confirmed** exploitation, enabling evidence-based vulnerability prioritization.

**Key Distinction:** KEV lists vulnerabilities with **confirmed active exploitation**, not theoretical or predicted exploitability.

### The Fundamental Difference

| Metric | Type | Basis |
|--------|------|-------|
| **CVSS** | Severity assessment | Vulnerability characteristics (impact if exploited) |
| **EPSS** | Exploitability prediction | Machine learning probability (0-100%) |
| **KEV** | **Confirmed exploitation** | **Ground truth** (CISA-verified active exploitation) |

**Critical Insight:** KEV is not a prediction or assessment—it's **confirmation** that attackers are actively exploiting the vulnerability right now.

### KEV Catalog Criteria

For a vulnerability to be added to the KEV catalog, it must meet **three criteria:**

1. **Assigned CVE ID**: Must have a CVE identifier
2. **Reliable evidence of active exploitation**: CISA confirms exploitation through:
   - Incident response telemetry
   - Threat intelligence from government and industry partners
   - Honeypot and sensor network data
   - Security vendor reports
   - Public disclosure by vendors or researchers
3. **Clear remediation guidance**: Vendor patch or mitigation available

**Update Frequency:** CISA updates the KEV catalog **within 24 hours** of confirming exploitation evidence.

### KEV Catalog Scope

**What's Included:**
- Vulnerabilities across all vendors (Microsoft, Adobe, Apple, Cisco, VMware, etc.)
- All product types (OS, applications, network devices, IoT, cloud services)
- Historical vulnerabilities (some entries date back 10+ years if still exploited)
- Vulnerabilities used in ransomware campaigns (flagged with "Known Ransomware Use" field)

**What's NOT Included:**
- Theoretical vulnerabilities (no confirmed exploitation)
- Vulnerabilities without CVE IDs
- Vulnerabilities without vendor remediation guidance
- Classified/sensitive exploitation (national security systems)

**Current Size:** 1,100+ CVEs (as of November 2025, growing continuously)

---

## Why KEV Matters

### The Vulnerability Remediation Challenge

**Industry Statistics:**
- ~30,000+ new CVEs published annually
- ~7% of CVEs are ever exploited in the wild
- Organizations face 100,000+ vulnerabilities across enterprise systems
- Limited security resources (staff, budget, time, change windows)

**Traditional Problem:** How do you decide which 1-2% of vulnerabilities to prioritize?

**KEV Solution:** Start with confirmed exploited vulnerabilities—these are **guaranteed real threats**, not theoretical risks.

### KEV = Confirmed Active Exploitation

**What "In KEV" Means:**

1. **Attackers are exploiting this vulnerability RIGHT NOW**
   - Not theoretical ("could be exploited")
   - Not predicted ("likely to be exploited")
   - **Confirmed** ("is being exploited")

2. **Real-world incidents have occurred**
   - Organizations have been compromised via this vulnerability
   - CISA has verified exploitation evidence
   - Threat actors have weaponized the vulnerability

3. **Immediate risk to your organization**
   - If you have vulnerable systems, you are at risk TODAY
   - Attackers have proven capability and intent
   - Exploitation tools likely publicly available or in attacker arsenals

### KEV Status Overrides Other Metrics

**Critical Priority Rule:**

```
IF vulnerability IN KEV catalog THEN
    Priority = P1 (Critical - Immediate Action)
    REGARDLESS of CVSS score, EPSS probability, or other factors
END IF
```

**Why KEV Overrides Everything:**

**Example 1: KEV Trumps Low CVSS**
```
CVE-2024-XXXX: Authentication Bypass
- CVSS: 6.5 (Medium)
- EPSS: 0.12 (12% - Low)
- KEV: YES

→ Priority: P1 (Critical) despite "Medium" severity
→ Rationale: Confirmed exploitation > theoretical severity
```

**Example 2: KEV Trumps Low EPSS**
```
CVE-2024-YYYY: Privilege Escalation
- CVSS: 7.8 (High)
- EPSS: 0.05 (5% - Very Low)
- KEV: YES

→ Priority: P1 (Critical) despite low EPSS
→ Rationale: Confirmed exploitation > predicted probability
```

**Example 3: KEV Elevates Old Vulnerabilities**
```
CVE-2017-ZZZZ: 8-Year-Old RCE
- CVSS: 9.8 (Critical)
- EPSS: 0.02 (2% - Low, old CVE)
- KEV: YES (added 2025 - rediscovered by ransomware groups)

→ Priority: P1 (Critical) despite age and low EPSS
→ Rationale: Attackers actively exploiting legacy systems
```

### Mandatory Remediation for Federal Agencies

**Binding Operational Directive 22-01:**

KEV vulnerabilities are **mandatory** to remediate for federal civilian executive branch (FCEB) agencies:

- **Timeline:** 2 weeks for most vulnerabilities, 6 months for pre-2021 CVEs
- **Enforcement:** Agency CIO/CISO accountability, reported to Congress
- **No exceptions:** Must remediate or provide documented risk acceptance

**Best Practice for All Organizations:** Treat KEV as if BOD 22-01 applies to you (many regulations and cyber insurance policies now require it).

### KEV and Ransomware

**Special Field:** "Known Ransomware Campaign Use"

KEV catalog flags vulnerabilities confirmed to be used in ransomware attacks:
- **Value:** "Known" or blank
- **Significance:** Ransomware groups actively exploiting this vulnerability
- **Implication:** Extremely high risk of data encryption, exfiltration, extortion

**Ransomware Statistics:**
- ~40-50% of KEV vulnerabilities used in ransomware campaigns
- Ransomware groups prioritize KEV vulnerabilities (proven attack vectors)
- Financial impact: Millions in ransom, recovery costs, downtime, reputation damage

**Prioritization Rule:**
```
IF KEV = YES AND Known Ransomware Use = "Known" THEN
    Priority = P0 (Emergency - Immediate Emergency Response)
    Timeline = 24-72 hours maximum
END IF
```

---

## Checking KEV Catalog

### Web Interface

**CISA KEV Catalog Website:**
- URL: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Interface: Searchable table with sorting and filtering
- Search by: CVE-ID, vendor, product, vulnerability name

**Features:**
- Filter by date added
- Filter by due date
- Filter by ransomware use
- Export to CSV
- Links to vendor advisories

**Use Case:** Manual lookup for individual CVEs or browsing recent additions

### JSON Feed (API Access)

**KEV Catalog JSON Endpoint:**
- URL: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Format: JSON (machine-readable)
- Update Frequency: Updated within 24 hours of new additions
- Size: ~1-2 MB (1,100+ entries)

**JSON Structure:**
```json
{
  "title": "CISA Catalog of Known Exploited Vulnerabilities",
  "catalogVersion": "2025.11.09",
  "dateReleased": "2025-11-09T15:30:00.000Z",
  "count": 1147,
  "vulnerabilities": [
    {
      "cveID": "CVE-2024-1234",
      "vendorProject": "Microsoft",
      "product": "Exchange Server",
      "vulnerabilityName": "Microsoft Exchange Server Remote Code Execution Vulnerability",
      "dateAdded": "2025-11-01",
      "shortDescription": "Microsoft Exchange Server contains a remote code execution vulnerability...",
      "requiredAction": "Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.",
      "dueDate": "2025-11-15",
      "knownRansomwareCampaignUse": "Known",
      "notes": "https://msrc.microsoft.com/update-guide/vulnerability/CVE-2024-1234"
    },
    ...
  ]
}
```

### Programmatic Checking (Python Example)

```python
import requests

def check_kev_status(cve_id):
    """Check if CVE is in CISA KEV catalog"""
    kev_url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    try:
        response = requests.get(kev_url)
        response.raise_for_status()
        kev_data = response.json()

        # Search for CVE in vulnerabilities list
        for vuln in kev_data['vulnerabilities']:
            if vuln['cveID'] == cve_id:
                return {
                    'in_kev': True,
                    'vendor': vuln['vendorProject'],
                    'product': vuln['product'],
                    'name': vuln['vulnerabilityName'],
                    'date_added': vuln['dateAdded'],
                    'due_date': vuln['dueDate'],
                    'ransomware_use': vuln.get('knownRansomwareCampaignUse', 'Unknown'),
                    'required_action': vuln['requiredAction'],
                    'notes': vuln.get('notes', '')
                }

        return {'in_kev': False}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching KEV catalog: {e}")
        return None

# Example usage
cve = "CVE-2024-21887"
result = check_kev_status(cve)

if result and result['in_kev']:
    print(f"🚨 {cve} IS IN KEV CATALOG 🚨")
    print(f"Vendor: {result['vendor']}")
    print(f"Product: {result['product']}")
    print(f"Added: {result['date_added']}")
    print(f"Due Date: {result['due_date']}")
    print(f"Ransomware Use: {result['ransomware_use']}")
    print(f"Action Required: {result['required_action']}")
else:
    print(f"✓ {cve} is NOT in KEV catalog")
```

**Output Example:**
```
🚨 CVE-2024-21887 IS IN KEV CATALOG 🚨
Vendor: Ivanti
Product: Connect Secure
Added: 2024-01-15
Due Date: 2024-01-29
Ransomware Use: Known
Action Required: Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable.
```

### CSV Download

**Download Link:** Available from https://www.cisa.gov/known-exploited-vulnerabilities-catalog

**Format:** CSV with columns:
- cveID
- vendorProject
- product
- vulnerabilityName
- dateAdded
- shortDescription
- requiredAction
- dueDate
- knownRansomwareCampaignUse
- notes

**Use Case:** Import into spreadsheets, vulnerability management tools, or custom databases

### Integration with Vulnerability Management Tools

**Most VM platforms now integrate KEV:**

- **Tenable.io**: KEV status displayed in vulnerability details
- **Qualys VMDR**: KEV filter available in asset search
- **Rapid7 InsightVM**: KEV tag applied automatically
- **ServiceNow VRM**: KEV vulnerabilities auto-prioritized
- **Rezilion**: KEV integrated with CVSS and EPSS for risk scoring

**Best Practice:** Enable KEV integration in your VM platform for automatic flagging.

---

## KEV Catalog Fields

### Field Breakdown

#### 1. cveID

**Format:** CVE-YYYY-NNNNN (e.g., CVE-2024-1234)

**Description:** The CVE identifier assigned by MITRE

**Usage:** Primary key for lookups and correlation with vulnerability scanners

#### 2. vendorProject

**Format:** Vendor or project name (e.g., "Microsoft", "Apache", "Cisco")

**Description:** Software vendor or open-source project

**Usage:** Filter vulnerabilities by vendor (e.g., "show me all Microsoft KEV entries")

**Note:** May say "Multiple Vendors" for supply chain vulnerabilities affecting many products

#### 3. product

**Format:** Product name (e.g., "Exchange Server", "Log4j", "IOS XE")

**Description:** Specific affected product or component

**Usage:** Identify if your organization uses this product

**Note:** Some entries use generic names (e.g., "Kernel") for OS-level vulnerabilities

#### 4. vulnerabilityName

**Format:** Descriptive name (e.g., "Microsoft Exchange Server Remote Code Execution Vulnerability")

**Description:** Human-readable vulnerability title

**Usage:** Quick understanding of vulnerability nature without reading full CVE description

**Common Patterns:**
- "[Product] [Vulnerability Type] Vulnerability"
- Named vulnerabilities (e.g., "ProxyLogon", "Log4Shell", "PrintNightmare")

#### 5. dateAdded

**Format:** YYYY-MM-DD (e.g., "2025-11-09")

**Description:** Date CISA added vulnerability to KEV catalog

**Significance:**
- **NOT** the CVE publication date (vulnerability may be years old)
- Date when CISA confirmed active exploitation
- Used to calculate BOD 22-01 due date

**Example:**
```
CVE-2017-0144 (EternalBlue)
- CVE Published: 2017-03-14
- KEV Added: 2021-11-03 (added to catalog at launch, still exploited 4.5 years later)
```

#### 6. shortDescription

**Format:** 1-2 sentence description

**Description:** Brief explanation of the vulnerability

**Content:** Usually includes:
- What the vulnerability allows (RCE, privilege escalation, etc.)
- Attack vector (network, local, etc.)
- Impact (code execution, information disclosure, DoS)

**Example:**
```
"Microsoft Exchange Server contains a remote code execution vulnerability that allows
an authenticated attacker to execute arbitrary code with SYSTEM privileges."
```

#### 7. requiredAction

**Format:** Remediation guidance (typically standardized text)

**Most Common Values:**

**"Apply mitigations per vendor instructions or discontinue use of the product if mitigations are unavailable."**
- Standard remediation: Apply vendor patch
- If no patch: Implement workarounds or disable product
- Links provided in "notes" field

**"Apply updates per vendor instructions."**
- Patch available, apply immediately
- Simpler cases with straightforward patching

**Custom Guidance:**
- Some entries provide specific mitigation steps
- May include configuration changes, disable features, isolate systems

**Compliance Requirement:** Federal agencies must comply with required action within due date timeline.

#### 8. dueDate

**Format:** YYYY-MM-DD

**Description:** Deadline for federal agencies to remediate (per BOD 22-01)

**Calculation Rules:**

**For CVEs assigned 2021 or later:**
- **dueDate = dateAdded + 14 days** (2 weeks)

**For CVEs assigned before 2021:**
- **dueDate = dateAdded + 6 months**
- Rationale: Legacy vulnerabilities may require more complex remediation (legacy systems, compatibility testing)

**Examples:**
```
CVE-2024-1234 (assigned 2024)
- Date Added: 2025-11-01
- Due Date: 2025-11-15 (14 days)

CVE-2018-5678 (assigned 2018)
- Date Added: 2025-11-01
- Due Date: 2026-05-01 (6 months)
```

**For Non-Federal Organizations:**
- Due dates are **guidance**, not legally binding (unless your industry has specific regulations)
- **Best Practice:** Treat due dates as maximum acceptable timeline
- **Recommended:** Aim for 7 days or less for internet-facing systems

#### 9. knownRansomwareCampaignUse

**Format:** "Known" or blank

**Description:** CISA confirms vulnerability used in ransomware campaigns

**Significance:**
- **"Known"**: Ransomware groups actively exploiting this vulnerability
- **Blank**: No confirmed ransomware use (but still actively exploited for other purposes)

**Statistics:**
- ~40-50% of KEV entries have "Known" ransomware use
- Ransomware-flagged KEV vulnerabilities are highest priority

**Prioritization Impact:**
```
KEV = YES, Ransomware = "Known" → P0 (Emergency)
KEV = YES, Ransomware = blank → P1 (Critical)
```

**Example:**
```
CVE-2024-21887: Ivanti Connect Secure Command Injection
- KEV: YES
- Ransomware: Known
- Impact: Multiple ransomware families (LockBit, BlackCat, ALPHV) exploiting

→ Priority: P0 (Emergency - immediate action, potential data encryption risk)
```

#### 10. notes

**Format:** URL or additional text

**Description:** Links to vendor advisories, CISA alerts, or additional context

**Common Links:**
- Vendor security bulletins (MSRC, VMware Security Advisories, etc.)
- CISA cybersecurity advisories (CSA)
- CERT/CC advisories
- Industry alerts

**Usage:** Click through for detailed technical information, patches, workarounds

---

## Prioritization Implications

### The KEV Priority Override Rule

**Absolute Rule:**

```
IF vulnerability IN CISA KEV catalog THEN
    Priority = P1 (Critical) MINIMUM
    Timeline = Immediate (14 days MAXIMUM, preferably 24-72 hours)
    OVERRIDE all other prioritization factors
END IF
```

**Why This Rule Exists:**

1. **KEV = Ground Truth**
   - Not theoretical risk (CVSS)
   - Not predicted probability (EPSS)
   - **Confirmed exploitation happening RIGHT NOW**

2. **Attackers Have Proven Capability**
   - Exploit code exists (may be public or in attacker arsenals)
   - Attackers have demonstrated intent (active campaigns)
   - Your organization is a potential target

3. **Real-World Incidents Occurring**
   - Other organizations already compromised
   - Threat actors actively scanning for vulnerable systems
   - Time-sensitive: risk increases every hour unpatched

### KEV Priority Levels

#### P0 (Emergency): KEV + Ransomware + Critical Assets

**Criteria:**
- ✓ In KEV catalog
- ✓ "Known Ransomware Campaign Use" = "Known"
- ✓ Affects internet-facing or critical business systems

**Timeline:** 24-72 hours (emergency change control)

**Actions:**
- Emergency response team activation
- Immediate patch deployment or system isolation
- Enhanced monitoring for compromise indicators
- Executive leadership notification
- Incident response team on standby

**Example:**
```
CVE-2024-XXXX: VPN Gateway RCE
- KEV: YES
- Ransomware: Known
- Asset: Internet-facing corporate VPN (10,000 remote users)
- Impact: Potential ransomware entry point to entire network

→ P0 Emergency
→ Timeline: 48 hours
→ Actions: Emergency patch Friday night, monitor weekend, IR team ready
```

#### P1 (Critical): KEV Without Ransomware or Non-Critical Assets

**Criteria:**
- ✓ In KEV catalog
- Ransomware use unknown OR affects non-critical systems

**Timeline:** 7-14 days (expedited change control)

**Actions:**
- Prioritize in next change window (don't wait for monthly cycle)
- Test patches in non-production
- Deploy to production within 1-2 weeks
- Monitor for exploitation attempts
- Document remediation status

**Example:**
```
CVE-2024-YYYY: Internal Application Server Vulnerability
- KEV: YES
- Ransomware: Not flagged
- Asset: Internal application server (not internet-facing)
- Impact: Requires network access, but still exploited in wild

→ P1 Critical
→ Timeline: 10 days
→ Actions: Next weekly change window, test then deploy
```

### KEV Overrides CVSS and EPSS

**Scenario 1: Low CVSS, Low EPSS, but IN KEV**

```
CVE-2024-ZZZZ: Authentication Bypass
- CVSS: 6.5 (Medium)
- EPSS: 0.05 (5% - Low)
- KEV: YES

Without KEV:
  → CVSS=Medium + EPSS=Low → P3 (Medium priority, 30-60 days)

With KEV:
  → KEV=YES → P1 (Critical, 7-14 days)

Rationale: Confirmed exploitation overrides severity and probability assessments
```

**Scenario 2: High CVSS, High EPSS, NOT in KEV**

```
CVE-2024-AAAA: Remote Code Execution
- CVSS: 9.8 (Critical)
- EPSS: 0.85 (85% - High)
- KEV: NO

Without KEV:
  → CVSS=Critical + EPSS=High → P1 (Immediate, 7 days)

With KEV Check:
  → KEV=NO → P1 (Urgent, 7-14 days)

Rationale: Still high priority, but absence from KEV suggests exploitation not yet widespread
```

**Key Insight:** KEV presence elevates priority; KEV absence doesn't necessarily lower it (High CVSS + High EPSS still warrants urgency).

### Risk Priority Framework (CVSS + EPSS + KEV)

**Decision Tree:**

```
Step 1: Check KEV Status
  IF KEV = YES → GO TO Step 2 (KEV Priority Path)
  IF KEV = NO → GO TO Step 3 (Standard Priority Path)

Step 2: KEV Priority Path
  IF Ransomware = "Known" AND Internet-Facing → P0 (Emergency, 24-72 hours)
  IF Ransomware = "Known" OR Critical Asset → P1 (Critical, 7 days)
  ELSE → P1 (Critical, 14 days)

Step 3: Standard Priority Path (No KEV)
  IF CVSS >= 9.0 AND EPSS >= 0.50 → P1 (Immediate, 7 days)
  IF CVSS >= 7.0 AND EPSS >= 0.50 → P1 (Urgent, 14 days)
  IF CVSS >= 7.0 AND EPSS < 0.50 → P2 (High, 30 days)
  IF CVSS 4.0-6.9 AND EPSS >= 0.50 → P2 (High, 30 days)
  IF CVSS 4.0-6.9 AND EPSS < 0.50 → P3 (Medium, 60 days)
  IF CVSS < 4.0 → P4 (Low, next maintenance window)
```

### Why KEV Matters More Than CVSS/EPSS

| Metric | What It Tells You | Limitation |
|--------|------------------|------------|
| **CVSS** | How bad IF exploited | Doesn't tell if exploitation is happening |
| **EPSS** | Probability of exploitation | Prediction, not confirmation |
| **KEV** | **CONFIRMED exploitation** | **No guessing - it's happening NOW** |

**Analogy:**

- **CVSS:** "This door could be kicked in (high severity)"
- **EPSS:** "This door might be kicked in (85% probability)"
- **KEV:** "This door IS BEING kicked in RIGHT NOW (confirmed burglary in progress)"

**Which do you prioritize?** The confirmed burglary (KEV), every time.

---

## KEV Examples

### Example 1: ProxyLogon (CVE-2021-26855) - Exchange RCE

```
CVE-2021-26855: Microsoft Exchange Server ProxyLogon SSRF Vulnerability

KEV Entry:
- Vendor: Microsoft
- Product: Exchange Server
- Added to KEV: 2021-11-03 (KEV catalog launch)
- Due Date: 2022-05-03 (6 months - pre-2021 CVE)
- Ransomware Use: Known
- Required Action: Apply updates per vendor instructions

CVSS v3.1: 9.1 (Critical)
EPSS: 0.975 (97.5% - Extremely High)

Timeline:
- 2021-03-02: Microsoft discloses ProxyLogon
- 2021-03-03: Mass exploitation begins (100,000+ Exchange servers targeted)
- 2021-03-10: White House emergency directive to federal agencies
- 2021-11-03: Added to KEV catalog at launch
- 2024-present: STILL exploited (ransomware groups targeting unpatched legacy servers)

Impact:
- Thousands of organizations compromised
- Multiple ransomware families deployed via ProxyLogon
- Hafnium APT and multiple cybercrime groups

Lessons Learned:
- High CVSS + High EPSS correctly predicted severity
- KEV confirmed ongoing threat years later
- Legacy systems remain vulnerable (still in KEV in 2025)

Priority: P0 (Emergency) - Ransomware use, internet-facing, RCE
Timeline: 24-72 hours (or immediate if still vulnerable in 2025)
```

### Example 2: Log4Shell (CVE-2021-44228) - Ubiquitous RCE

```
CVE-2021-44228: Apache Log4j2 Remote Code Execution (Log4Shell)

KEV Entry:
- Vendor: Apache
- Product: Log4j
- Added to KEV: 2021-12-10 (same day as disclosure)
- Due Date: 2021-12-24 (14 days - 2021 CVE)
- Ransomware Use: Known
- Required Action: Apply updates per vendor instructions

CVSS v3.1: 10.0 (Critical - Maximum Severity)
EPSS: 0.976 (97.6% - Extremely High)

Timeline:
- 2021-12-09: Log4Shell disclosed (zero-day)
- 2021-12-10: Added to KEV (within 24 hours - fastest addition)
- 2021-12-10-12: Mass exploitation begins (millions of attempts)
- 2021-12-12: Botnets, ransomware, nation-state actors all exploiting
- 2022-2025: Continued exploitation of unpatched systems

Impact:
- Affected millions of applications (Log4j ubiquitous in Java ecosystem)
- Organizations worldwide scrambling to identify and patch
- Estimated remediation cost: billions globally
- Still exploited in 2025 (legacy systems, embedded devices)

Lessons Learned:
- Supply chain vulnerability affecting entire ecosystem
- CVSS 10.0 correctly reflected unprecedented severity
- KEV addition within 24 hours demonstrated CISA responsiveness
- Long tail of exploitation (years to fully remediate)

Priority: P0 (Emergency) - Ubiquitous library, internet-facing, RCE, ransomware
Timeline: Immediate (many orgs patched within 24-72 hours)
```

### Example 3: MOVEit Transfer (CVE-2023-34362) - File Transfer SQL Injection

```
CVE-2023-34362: Progress MOVEit Transfer SQL Injection

KEV Entry:
- Vendor: Progress Software
- Product: MOVEit Transfer
- Added to KEV: 2023-06-02
- Due Date: 2023-06-16 (14 days)
- Ransomware Use: Known
- Required Action: Apply mitigations per vendor instructions or discontinue use

CVSS v3.1: 9.8 (Critical)
EPSS: 0.972 (97.2% - Extremely High)

Timeline:
- 2023-05-31: Progress discloses zero-day (already exploited)
- 2023-06-01: Clop ransomware group confirms exploitation
- 2023-06-02: Added to KEV
- 2023-06-05: Hundreds of organizations confirmed compromised
- 2023-06-15: Major breaches disclosed (federal agencies, Fortune 500)

Impact:
- 2,000+ organizations compromised (estimated)
- Data theft from federal agencies, healthcare, finance, education
- Clop ransomware group extortion campaign
- Class-action lawsuits, regulatory investigations

Lessons Learned:
- Zero-day added to KEV before most orgs aware of it
- Managed file transfer solutions are high-value targets
- Need for rapid incident response even with 14-day deadline

Priority: P0 (Emergency) - Zero-day, ransomware, internet-facing
Timeline: Immediate (many orgs took MOVEit offline within hours)
```

### Example 4: Citrix Bleed (CVE-2023-4966) - Session Hijacking

```
CVE-2023-4966: Citrix NetScaler ADC and Gateway Session Hijacking

KEV Entry:
- Vendor: Citrix
- Product: NetScaler ADC, NetScaler Gateway
- Added to KEV: 2023-10-16
- Due Date: 2023-10-30 (14 days)
- Ransomware Use: Known
- Required Action: Apply updates per vendor instructions

CVSS v3.1: 9.4 (Critical)
EPSS: 0.963 (96.3% - Extremely High)

Timeline:
- 2023-10-10: Citrix discloses vulnerability ("Citrix Bleed")
- 2023-10-11: Mass exploitation begins
- 2023-10-16: Added to KEV
- 2023-10-20: LockBit ransomware confirmed using for initial access
- 2023-11-01: Boeing confirmed breach via Citrix Bleed

Impact:
- Session hijacking without credentials
- Ransomware initial access vector
- High-profile breaches (Boeing, others)
- Critical infrastructure targeted

Lessons Learned:
- VPN/gateway vulnerabilities are prime ransomware targets
- Session hijacking as severe as RCE for initial access
- Need for rapid patching of perimeter devices

Priority: P0 (Emergency) - Ransomware, internet-facing gateway, session hijacking
Timeline: 24-72 hours (critical perimeter device)
```

### Example 5: Old Vulnerability Resurfaces (CVE-2017-0144 - EternalBlue)

```
CVE-2017-0144: Microsoft Windows SMB Remote Code Execution (EternalBlue)

KEV Entry:
- Vendor: Microsoft
- Product: Windows
- CVE Published: 2017-03-14 (8 years ago as of 2025)
- Added to KEV: 2021-11-03 (KEV catalog launch - still exploited 4.5 years later)
- Due Date: 2022-05-03 (6 months - pre-2021 CVE)
- Ransomware Use: Known
- Required Action: Apply updates per vendor instructions

CVSS v3.1: 8.8 (High)
EPSS: 0.973 (97.3% - Extremely High even in 2025)

Timeline:
- 2017-03-14: Microsoft Patch Tuesday (MS17-010)
- 2017-04-14: Shadow Brokers leak NSA EternalBlue exploit
- 2017-05-12: WannaCry ransomware (EternalBlue) - global outbreak
- 2017-06-27: NotPetya ransomware (EternalBlue) - $10B+ damage
- 2021-11-03: Added to KEV (still exploited 4.5 years post-patch)
- 2025-present: STILL exploited (legacy Windows systems, unpatched endpoints)

Impact:
- WannaCry: 200,000+ systems in 150 countries
- NotPetya: $10 billion global damage
- Continued exploitation of legacy/unpatched systems
- Still in KEV 8 years later (proof that old CVEs never die)

Lessons Learned:
- Old vulnerabilities remain threats (legacy systems, poor patching)
- KEV includes historical CVEs still actively exploited
- Don't assume "old CVE = patched everywhere"

Priority: P1 (Critical) - Even in 2025, if you find unpatched Windows systems
Timeline: Immediate (8-year-old patch, no excuse for delay)
```

---

## Integration with Risk Prioritization

### The Complete Priority Framework

**Vulnerability Risk = f(Severity, Exploitability, Exploitation Confirmation, Business Context)**

```
Priority = Combine(CVSS, EPSS, KEV, Asset Criticality, Exposure)
```

#### Priority Decision Matrix

| KEV | CVSS | EPSS | Asset Type | Priority | Timeline |
|-----|------|------|------------|----------|----------|
| **YES** | Any | Any | Internet-facing | **P0** | 24-72 hours |
| **YES** | Any | Any | Internal critical | **P1** | 7 days |
| **YES** | Any | Any | Internal non-critical | **P1** | 14 days |
| NO | 9.0+ | >50% | Internet-facing | **P1** | 7 days |
| NO | 9.0+ | >50% | Internal | **P2** | 14 days |
| NO | 7.0+ | >50% | Internet-facing | **P1** | 14 days |
| NO | 7.0+ | >50% | Internal | **P2** | 30 days |
| NO | 7.0+ | <10% | Any | **P2** | 30 days |
| NO | 4.0-6.9 | >50% | Internet-facing | **P2** | 30 days |
| NO | 4.0-6.9 | <50% | Any | **P3** | 60 days |
| NO | <4.0 | Any | Any | **P4** | Next maintenance |

### Priority Level Definitions

#### P0 (Emergency)
- **Criteria:** KEV + (Ransomware OR Internet-Facing Critical)
- **Timeline:** 24-72 hours
- **Change Control:** Emergency change process
- **Actions:** Immediate patching or isolation, enhanced monitoring, IR readiness

#### P1 (Critical)
- **Criteria:** KEV OR (High CVSS + High EPSS + Critical Asset)
- **Timeline:** 7-14 days
- **Change Control:** Expedited change process
- **Actions:** Prioritize in next change window, test and deploy urgently

#### P2 (High)
- **Criteria:** High CVSS OR High EPSS, not in KEV
- **Timeline:** 14-30 days
- **Change Control:** Accelerated monthly cycle
- **Actions:** Include in next monthly patching cycle (don't wait 90 days)

#### P3 (Medium)
- **Criteria:** Medium CVSS + Low EPSS, not in KEV
- **Timeline:** 30-90 days
- **Change Control:** Normal change process
- **Actions:** Regular patching cycle, plan remediation

#### P4 (Low)
- **Criteria:** Low CVSS, not in KEV
- **Timeline:** Next maintenance window
- **Change Control:** Routine maintenance
- **Actions:** Address during routine updates, low priority

### KEV as Priority Override

**Override Rule:**
```
IF KEV = YES THEN
    Priority = MAX(Priority_calculated, P1)
    Timeline = MIN(Timeline_calculated, 14_days)
END IF
```

**Translation:** KEV always elevates priority to at least P1 (Critical) with maximum 14-day timeline.

### Example Prioritization Workflows

#### Workflow 1: New CVE Disclosed

```
Step 1: CVE Published (CVE-2025-XXXX)
  - CVSS: 8.8 (High)
  - EPSS: 0.05 (5% - initial score, no exploitation yet)
  - KEV: NO

Step 2: Initial Assessment
  - Priority: P2 (High CVSS, Low EPSS) → 30 days

Step 3: Monitor EPSS Daily
  - Day 3: EPSS jumps to 0.45 (45%) - PoC published
  - Priority: Elevate to P1 → 14 days

Step 4: Check KEV Daily
  - Day 7: Added to KEV (confirmed exploitation)
  - Priority: Elevate to P0 (KEV + internet-facing) → 72 hours

Step 5: Emergency Response
  - Deploy patch within 72 hours
  - Monitor for compromise indicators
```

#### Workflow 2: Vulnerability Scan Results

```
Scan identifies 10,000 vulnerabilities across enterprise:

Step 1: Filter by KEV Status
  - KEV = YES: 47 vulnerabilities → P1 (immediate attention)
  - KEV = NO: 9,953 vulnerabilities → continue assessment

Step 2: For KEV=NO vulnerabilities, apply CVSS+EPSS matrix
  - CVSS 9.0+, EPSS >50%: 134 vulnerabilities → P1 (7 days)
  - CVSS 7.0+, EPSS >50%: 421 vulnerabilities → P1 (14 days)
  - CVSS 7.0+, EPSS <50%: 1,203 vulnerabilities → P2 (30 days)
  - CVSS 4.0-6.9: 3,845 vulnerabilities → P3 (60-90 days)
  - CVSS <4.0: 4,350 vulnerabilities → P4 (next maintenance)

Step 3: Focus Resources
  - P0/P1: 602 vulnerabilities (6% of total) - focus here
  - Achieves ~90%+ risk reduction with 6% effort

Result: KEV-based prioritization reduces critical workload by 94% while maintaining high risk coverage
```

---

## BOD 22-01 Requirements

### Binding Operational Directive 22-01 Overview

**Full Title:** "Reducing the Significant Risk of Known Exploited Vulnerabilities"

**Issued:** November 3, 2021

**Issuing Authority:** Cybersecurity and Infrastructure Security Agency (CISA), U.S. Department of Homeland Security

**Legal Basis:** Department of Homeland Security Act of 2002

### Who BOD 22-01 Applies To

**Mandatory Compliance:**
- Federal Civilian Executive Branch (FCEB) agencies
- Applies to all software and hardware on federal information systems
- Includes systems managed on-premises or hosted by third parties on agency's behalf

**Does NOT Apply To:**
- Department of Defense (DoD) systems
- Intelligence Community (IC) systems
- National security systems (NSS)
- Private sector organizations (guidance only)

**Best Practice for Non-Federal Organizations:**
- Many regulations reference BOD 22-01 (CMMC, state regulations, cyber insurance)
- Treat BOD 22-01 as industry best practice even if not legally required

### Remediation Requirements

#### Timeline Requirements

**For CVEs Assigned 2021 or Later:**
- **Deadline:** 2 weeks (14 calendar days) from date added to KEV
- **Calculation:** dateAdded + 14 days = dueDate
- **Example:**
  ```
  CVE-2024-1234 added to KEV: 2025-11-01
  Due Date: 2025-11-15 (14 days later)
  ```

**For CVEs Assigned Before 2021:**
- **Deadline:** 6 months from date added to KEV
- **Calculation:** dateAdded + 6 months = dueDate
- **Rationale:** Legacy vulnerabilities may affect older systems requiring more complex remediation
- **Example:**
  ```
  CVE-2018-5678 added to KEV: 2025-11-01
  Due Date: 2026-05-01 (6 months later)
  ```

**Expedited Timelines:**
- CISA may issue shorter timelines "if a grave risk to the federal enterprise exists"
- Emergency directives may override standard 14-day timeline
- Agencies must comply with expedited timelines

#### Required Actions

**Agencies MUST:**

1. **Remediate Vulnerabilities:**
   - Apply vendor patches/updates
   - Implement vendor-recommended mitigations
   - If no patch available: discontinue use or isolate affected systems

2. **Meet Deadlines:**
   - Remediate within 2 weeks (post-2021 CVEs) or 6 months (pre-2021 CVEs)
   - No extensions without formal risk acceptance process

3. **Track and Report:**
   - Establish internal tracking systems
   - Report remediation status via CDM Federal Dashboard or CyberScope
   - Maintain documentation of remediation efforts

4. **Apply to All Systems:**
   - On-premises federal systems
   - Third-party hosted systems (cloud, SaaS, managed services)
   - Applies to all federal information systems in scope

### Reporting Requirements

#### CDM Federal Dashboard (Preferred)

**Method:** Continuous Diagnostics and Mitigation (CDM) Federal Dashboard

**Frequency:** Real-time/continuous reporting

**Start Date:** October 1, 2022 (preferred method)

**Content:**
- Vulnerability scan results
- KEV vulnerability identification
- Remediation status (open, in progress, remediated)
- Due dates and compliance status

**Agencies with CDM:** Report via dashboard (most FCEB agencies)

#### CyberScope Submissions (Alternative)

**Method:** OMB CyberScope reporting

**Frequency:**
- Quarterly (initial requirement)
- Bi-weekly (after October 1, 2022 for non-CDM agencies)

**Content:**
- KEV vulnerabilities identified
- Remediation actions taken
- Outstanding vulnerabilities and justification
- Compliance metrics

**Agencies without CDM:** Use CyberScope until CDM available

#### Internal Tracking

**Requirement:** Agencies must establish internal tracking and reporting

**Purpose:**
- Evaluate adherence with BOD 22-01
- Track remediation progress
- Identify systemic issues
- Support accountability

**Recommended Elements:**
- KEV vulnerability inventory
- Asset mapping (which systems affected)
- Remediation workflow tracking
- Compliance dashboard for leadership
- Exception/risk acceptance process

### Enforcement and Accountability

**Accountability:**
- Agency Chief Information Officer (CIO)
- Agency Chief Information Security Officer (CISO)
- Agency heads (ultimate responsibility)

**Oversight:**
- CISA reviews agency compliance
- OMB (Office of Management and Budget) oversight
- Congressional reporting (federal cybersecurity posture)

**Consequences of Non-Compliance:**
- Agency leadership accountability
- Potential budget implications
- Required corrective action plans
- Public disclosure of compliance gaps

### Risk Acceptance Process

**If Remediation Impossible:**
- Formal risk acceptance required
- Must document:
  - Why remediation not possible
  - Compensating controls implemented
  - Residual risk assessment
  - Timeline for eventual remediation or system decommissioning
- Senior leadership approval required
- Ongoing monitoring and reporting

**Example Risk Acceptance Scenario:**
```
CVE-2024-XXXX affects legacy SCADA system
- No patch available from vendor (product end-of-life)
- System cannot be replaced within 14-day timeline (6-month procurement)
- Risk Acceptance:
  - Document: Legacy system, no patch, replacement in progress
  - Compensating Controls: Network isolation, enhanced monitoring, IDS/IPS rules
  - Residual Risk: Medium (mitigated by isolation)
  - Timeline: System replacement by Q2 2026
  - Approval: Agency CISO + CIO
```

### Implications for Third-Party Services

**BOD 22-01 Applies to:**
- Cloud service providers hosting federal data
- SaaS applications used by federal agencies
- Managed service providers (MSPs) managing federal systems
- Any third party hosting federal information systems

**Federal Agency Responsibilities:**
- Ensure vendors comply with BOD 22-01 timelines
- Include BOD 22-01 compliance in contracts
- Verify vendor remediation via attestation or audit
- Escalate non-compliance to CISA

**Vendor Implications:**
- FedRAMP vendors must track and remediate KEV vulnerabilities
- Contractual obligations to meet 14-day timelines
- May face contract termination for non-compliance

### Best Practices for Non-Federal Organizations

**Even if BOD 22-01 Doesn't Legally Apply:**

1. **Adopt KEV-Based Prioritization:**
   - Use KEV catalog as authoritative exploitation source
   - Prioritize KEV vulnerabilities as P1 minimum

2. **Use BOD 22-01 Timelines as Guidance:**
   - 14 days for recent CVEs (stretch goal: 7 days for internet-facing)
   - 6 months for legacy CVEs (aim for 90 days if possible)

3. **Implement Tracking and Reporting:**
   - Track KEV vulnerabilities separately
   - Dashboard for leadership visibility
   - Compliance metrics (% KEV remediated within 14 days)

4. **Align with Regulatory Requirements:**
   - Many regulations reference BOD 22-01 (CMMC, state laws)
   - Cyber insurance may require KEV remediation
   - Demonstrate due diligence for breach liability

5. **Include in Vendor Contracts:**
   - Require vendors to remediate KEV vulnerabilities
   - SLAs for patch deployment timelines
   - Right to audit vendor compliance

---

## Authoritative References

### Official CISA KEV Resources

**CISA KEV Catalog Website**
- URL: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Purpose: Official KEV catalog web interface (search, filter, export)
- Updated: Within 24 hours of new additions

**CISA KEV JSON Feed**
- URL: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
- Purpose: Machine-readable KEV catalog for automation
- Format: JSON
- Updated: Within 24 hours (same as web interface)

**CISA KEV CSV Export**
- Available from: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Purpose: Spreadsheet import, data analysis
- Format: CSV

### Binding Operational Directive 22-01

**BOD 22-01 Official Directive**
- URL: https://www.cisa.gov/binding-operational-directive-22-01
- Purpose: Full text of directive, requirements, timelines
- Audience: Federal agencies (guidance for private sector)

**BOD 22-01 Fact Sheet**
- URL: https://www.cisa.gov/sites/default/files/publications/BOD_22-01_Fact_Sheet_508C.pdf
- Purpose: Executive summary of BOD 22-01
- Format: PDF

**BOD 22-01 Supplemental Guidance**
- URL: https://www.cisa.gov/binding-operational-directive-22-01#supplemental-guidance
- Purpose: Additional implementation guidance, FAQs
- Topics: Third-party systems, cloud services, reporting

### Complementary CISA Resources

**CISA Cybersecurity Advisories**
- URL: https://www.cisa.gov/news-events/cybersecurity-advisories
- Purpose: Alerts for newly added KEV vulnerabilities, exploitation details
- Subscription: Email alerts available

**CISA Known Exploited Vulnerabilities Blog**
- URL: https://www.cisa.gov/news-events/news
- Purpose: Announcements of significant KEV additions, trends

**CISA Shields Up Campaign**
- URL: https://www.cisa.gov/shields-up
- Purpose: Heightened alert program for critical threats (often references KEV)

### Integration with Other Standards

**CVSS Scoring**
- URL: https://www.first.org/cvss/
- Integration: KEV provides exploitation confirmation, CVSS provides severity
- See: `cvss-guide.md`

**EPSS Exploitability Predictions**
- URL: https://www.first.org/epss/
- Integration: EPSS predicts likelihood, KEV confirms actual exploitation
- See: `epss-guide.md`

**MITRE ATT&CK Framework**
- URL: https://attack.mitre.org/
- Integration: Map KEV vulnerabilities to ATT&CK techniques for threat modeling
- See: `mitre-attack-mapping-guide.md`

**NVD (National Vulnerability Database)**
- URL: https://nvd.nist.gov/
- Integration: NVD provides CVE details, CVSS scores; cross-reference with KEV for exploitation status

### Industry and Research

**Cyentia Institute - EPSS Research**
- URL: https://www.cyentia.com/
- Purpose: EPSS model research, EPSS data downloads
- Related: EPSS + KEV correlation studies

**Exploit Database (Exploit-DB)**
- URL: https://www.exploit-db.com/
- Purpose: Public exploit code repository (KEV often correlates with Exploit-DB entries)

**Metasploit Framework**
- URL: https://www.metasploit.com/
- Purpose: Penetration testing framework (KEV often has Metasploit modules)

### Regulatory and Compliance

**CMMC (Cybersecurity Maturity Model Certification)**
- URL: https://www.acq.osd.mil/cmmc/
- KEV Reference: CMMC 2.0 references timely vulnerability remediation (aligns with BOD 22-01)

**Cyber Insurance Requirements**
- Various insurers now require KEV remediation compliance
- Failure to remediate KEV may void coverage or increase premiums

### Monitoring and Alerting

**Set Up KEV Alerts:**
- Subscribe to CISA KEV mailing list: https://www.cisa.gov/subscribe
- RSS feed: Available from KEV catalog page
- Automated JSON monitoring (check daily for new additions)

**Recommended Monitoring:**
- Daily KEV JSON pull (compare to previous day, alert on new additions)
- Weekly KEV review meeting (security team)
- Monthly KEV compliance metrics (% remediated within 14 days)

---

## Document Metadata

**Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** Security Engineering Team
**Audience:** Security Analysts, Vulnerability Managers, Incident Responders, Compliance Officers
**Related Documents:**
- `cvss-guide.md` - CVSS severity scoring reference
- `epss-guide.md` - EPSS exploitability probability guidance
- `priority-framework.md` - Complete vulnerability prioritization framework
- `mitre-attack-mapping-guide.md` - MITRE ATT&CK technique mapping

**Document Purpose:** Comprehensive reference for understanding, using, and integrating CISA's Known Exploited Vulnerabilities (KEV) catalog into vulnerability management, risk prioritization, and compliance workflows.

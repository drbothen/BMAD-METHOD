# EPSS (Exploit Prediction Scoring System) Guide

## Table of Contents

1. [Introduction to EPSS](#introduction-to-epss)
2. [EPSS Scoring System](#epss-scoring-system)
3. [Interpreting EPSS Scores](#interpreting-epss-scores)
4. [EPSS API Usage](#epss-api-usage)
5. [Integration with CVSS](#integration-with-cvss)
6. [EPSS Examples](#epss-examples)
7. [Limitations and Considerations](#limitations-and-considerations)
8. [Authoritative References](#authoritative-references)

---

## Introduction to EPSS

### What EPSS Measures

**EPSS (Exploit Prediction Scoring System) estimates the probability that a software vulnerability will be exploited in the wild within the next 30 days.**

EPSS is a data-driven, machine learning-based system developed by FIRST (Forum of Incident Response and Security Teams) to help organizations prioritize vulnerability remediation based on **likelihood of exploitation**, not just severity.

### The Fundamental Question

**EPSS answers:** "What is the probability this vulnerability will be exploited in the next 30 days?"

This complements CVSS, which answers a different question: "How severe is the impact if this vulnerability is exploited?"

### Why EPSS Exists

Organizations face a fundamental challenge in vulnerability management:

**Problem:** Thousands of CVEs published annually, but limited remediation resources

**Reality:** Most published vulnerabilities are never exploited in the wild

**FIRST Research Findings:**
- Only ~7% of published CVEs are ever exploited in real-world attacks
- Prioritizing by CVSS severity alone is inefficient (treats all High/Critical CVEs equally)
- Organizations need **exploitability probability** to optimize remediation efforts

**EPSS Solution:** Use real-world threat intelligence and machine learning to predict which vulnerabilities are most likely to be exploited, enabling data-driven prioritization.

### How EPSS Differs from CVSS

| Dimension | CVSS | EPSS |
|-----------|------|------|
| **Question** | How severe IF exploited? | How likely TO BE exploited? |
| **Measure** | Impact severity (0.0-10.0) | Exploitation probability (0-1) |
| **Type** | Qualitative severity rating | Predictive probability estimate |
| **Basis** | Vulnerability characteristics | Real-world threat data + ML |
| **Timeframe** | Static (doesn't change) | Dynamic (updated daily) |
| **Purpose** | Severity assessment | Likelihood assessment |
| **Use** | Impact magnitude | Risk prioritization |

**Key Insight:** CVSS and EPSS are complementary, not competing. Together they provide both **severity** (CVSS) and **likelihood** (EPSS) for complete risk assessment.

### EPSS Development

**Developed by:** FIRST (Forum of Incident Response and Security Teams)

**First Released:** January 7, 2021 (public scores)

**Current Version:** EPSS v4 (released March 17, 2025)

**Previous Versions:**
- EPSS v3: March 7, 2023
- EPSS v2: 2022
- EPSS v1: 2021

**Data Sources:**
- Vulnerability databases (CVE, NVD)
- Exploit code repositories (Exploit-DB, GitHub, Metasploit)
- Public disclosure platforms (CISA KEV, Google Project Zero, ZDI)
- Network sensors and honeypots (data partners)
- Host-based detection data
- Security scanning tools (Intrigue, sn1per, Jaeles, Nuclei)

**Model Training:**
- Machine learning on 12 months of historical exploitation data
- Trained on patterns between vulnerability characteristics and observed exploitation
- Updated daily with new data
- Forward-looking predictions (next 30 days)

---

## EPSS Scoring System

### Score Components

EPSS provides two values for each CVE:

#### 1. EPSS Probability Score

**Format:** Decimal between 0.00000 and 1.00000 (or percentage 0% - 100%)

**Interpretation:**
- **0.00000 (0%)**: Extremely low probability of exploitation
- **0.50000 (50%)**: Equal chance of exploitation vs. non-exploitation
- **1.00000 (100%)**: Extremely high probability of exploitation (near certain)

**Example:**
```
CVE-2024-1234: EPSS = 0.85432 (85.432%)
```
This means the model predicts an 85.432% probability that this vulnerability will be exploited in the wild within the next 30 days.

#### 2. EPSS Percentile

**Format:** Integer between 0 and 100

**Interpretation:**
- Percentile indicates how the vulnerability ranks **relative to all other CVEs**
- 95th percentile = higher EPSS score than 95% of all vulnerabilities
- 50th percentile = median (average exploitability)
- 5th percentile = lower EPSS score than 95% of all vulnerabilities

**Example:**
```
CVE-2024-1234: EPSS Percentile = 97th
```
This CVE has a higher exploitation probability than 97% of all published CVEs (top 3%).

### Score Ranges and Interpretation

| EPSS Score | EPSS Percentile | Interpretation | Recommended Action |
|------------|-----------------|----------------|-------------------|
| **0.80 - 1.00** | 95th - 100th | Extremely high probability | Immediate prioritization |
| **0.50 - 0.79** | 80th - 94th | High probability | High priority |
| **0.20 - 0.49** | 50th - 79th | Moderate probability | Medium priority |
| **0.05 - 0.19** | 20th - 49th | Low probability | Lower priority |
| **0.00 - 0.04** | 0th - 19th | Very low probability | Lowest priority |

**Important:** These are general guidelines. Always combine EPSS with CVSS severity and business context.

### Update Frequency

**EPSS scores are updated DAILY.**

**What changes daily:**
- New CVEs added with EPSS scores
- Existing CVE scores updated based on new threat intelligence
- Model incorporates latest exploitation activity data

**Why daily updates matter:**
- Exploitation landscape changes rapidly
- Zero-day vulnerabilities may start with low EPSS, then spike when exploits published
- Active exploitation campaigns cause EPSS increases
- EPSS reflects current threat reality, not static risk

**Best Practice:** Re-check EPSS scores regularly for unpatched vulnerabilities (weekly or daily for critical assets).

### How EPSS Scores are Calculated

**Machine Learning Model:**

1. **Input Features (Vulnerability Characteristics):**
   - CVE age (days since publication)
   - Vendor/product (CPE from NVD)
   - Weakness classification (CWE)
   - CVSS base vector metrics (v3.x)
   - References and disclosure sources
   - Exploit code availability (Exploit-DB, GitHub, Metasploit)
   - Public disclosures (CISA KEV, Project Zero, ZDI)
   - Security tool coverage (Nuclei, sn1per, etc.)

2. **Training Data (Observed Exploitation):**
   - Network sensor data (honeypots, IDS/IPS)
   - Host-based detection logs
   - Malware analysis reports
   - Incident response telemetry
   - 12 months of historical exploitation activity

3. **Model Output:**
   - Probability of exploitation in next 30 days (0.00000 - 1.00000)
   - Percentile ranking relative to all CVEs (0 - 100)

**Key Concept:** EPSS identifies patterns between vulnerability characteristics and actual exploitation, then applies those patterns to predict exploitation likelihood for new CVEs.

---

## Interpreting EPSS Scores

### EPSS Thresholds

Organizations should define EPSS thresholds based on risk tolerance:

#### Conservative Approach (Risk-Averse)
```
EPSS >= 0.20 (20%) → High Priority
- Captures ~10-15% of all CVEs
- Covers ~90%+ of actually exploited vulnerabilities
- Higher remediation workload, better coverage
```

#### Balanced Approach (Recommended)
```
EPSS >= 0.50 (50%) → High Priority
- Captures ~5-7% of all CVEs
- Covers ~75-85% of actually exploited vulnerabilities
- Reasonable workload, good coverage
```

#### Aggressive Approach (Resource-Constrained)
```
EPSS >= 0.80 (80%) → High Priority
- Captures ~2-3% of all CVEs
- Covers ~60-70% of actually exploited vulnerabilities
- Minimal workload, accepts some risk
```

### Percentile-Based Interpretation

**Percentile provides relative ranking:**

**99th Percentile (Top 1%):**
- Among the most likely vulnerabilities to be exploited
- Active exploitation campaigns probable
- Exploit code likely widely available
- **Action:** Immediate remediation

**95th Percentile (Top 5%):**
- Significantly higher than average exploitation risk
- Likely has public exploit code or active interest
- **Action:** Prioritize for urgent remediation

**75th Percentile (Top 25%):**
- Above-average exploitation risk
- May have PoC code or researcher interest
- **Action:** Schedule for priority remediation

**50th Percentile (Median):**
- Average exploitation likelihood
- May or may not be exploited
- **Action:** Standard remediation timeline

**25th Percentile (Bottom 25%):**
- Below-average exploitation risk
- Likely no public exploits or active campaigns
- **Action:** Remediate during regular maintenance

### Interpreting Score Changes

**EPSS Score Increases:**

Causes:
- Exploit code published (PoC → Functional → Weaponized)
- Added to CISA KEV catalog (confirmed exploitation)
- Active exploitation campaign detected
- Security tool coverage added (Nuclei modules, Metasploit modules)
- Media attention or researcher disclosure

**Example Timeline:**
```
Day 0 (CVE Publication):  EPSS = 0.02 (2%), 40th percentile
Day 7 (PoC Released):     EPSS = 0.15 (15%), 65th percentile
Day 14 (Active Exploit):  EPSS = 0.78 (78%), 95th percentile
Day 21 (Widespread):      EPSS = 0.92 (92%), 98th percentile
```

**Action:** Monitor EPSS for significant increases (>20% jump) as early warning of emerging threats.

**EPSS Score Decreases:**

Causes:
- Exploitation activity declines (campaigns end)
- Patches widely deployed (smaller attack surface)
- Newer, more attractive vulnerabilities disclosed
- Exploit difficulty discovered (initial reports overstated exploitability)

**Example Timeline:**
```
Day 0 (Active Campaign):  EPSS = 0.88 (88%), 97th percentile
Day 30 (Patches Deploy):  EPSS = 0.65 (65%), 90th percentile
Day 60 (Campaign Ends):   EPSS = 0.32 (32%), 72nd percentile
Day 90 (Low Activity):    EPSS = 0.08 (8%), 48th percentile
```

**Action:** Decreasing EPSS is good news, but don't deprioritize completely—unpatched systems remain vulnerable.

### Red Flags: High-Priority EPSS Signals

**Immediate Attention Required:**

1. **EPSS >= 0.80 (80%+) on Internet-Facing Systems**
   - Very high exploitation probability
   - Likely active campaigns or widespread exploit code

2. **Rapid EPSS Increase (>30% in 7 days)**
   - Emerging threat
   - Exploitation activity accelerating
   - May indicate zero-day becoming public or new exploit release

3. **High EPSS + High CVSS (EPSS >50% + CVSS >7.0)**
   - Severe impact AND high likelihood
   - Perfect storm for risk
   - P1 priority regardless of other factors

4. **EPSS Jump After Being Low (<10% → >50%)**
   - Situational change (exploit released, campaign started)
   - Previously dormant vulnerability now active threat

---

## EPSS API Usage

### API Endpoint

**Base URL:** `https://api.first.org/data/v1/epss`

**Documentation:** https://www.first.org/epss/api

### Query by CVE-ID

**Endpoint:** `GET https://api.first.org/data/v1/epss?cve=<CVE-ID>`

**Example Request:**
```bash
curl "https://api.first.org/data/v1/epss?cve=CVE-2024-1234"
```

**Example Response:**
```json
{
  "status": "OK",
  "status-code": 200,
  "version": "1.0",
  "access": "public",
  "total": 1,
  "offset": 0,
  "limit": 100,
  "data": [
    {
      "cve": "CVE-2024-1234",
      "epss": "0.85432",
      "percentile": "0.97234",
      "date": "2025-11-09"
    }
  ]
}
```

**Response Fields:**
- `cve`: CVE identifier
- `epss`: Probability score (0.00000 - 1.00000)
- `percentile`: Percentile ranking (0.00000 - 1.00000, multiply by 100 for percentage)
- `date`: Date of EPSS score (updated daily)

### Query Multiple CVEs

**Endpoint:** `GET https://api.first.org/data/v1/epss?cve=<CVE1>,<CVE2>,<CVE3>`

**Example Request:**
```bash
curl "https://api.first.org/data/v1/epss?cve=CVE-2024-1234,CVE-2024-5678,CVE-2024-9999"
```

**Response:** JSON array with EPSS data for all requested CVEs

### Query by Date

**Endpoint:** `GET https://api.first.org/data/v1/epss?date=<YYYY-MM-DD>`

**Example Request:**
```bash
curl "https://api.first.org/data/v1/epss?date=2025-11-09"
```

**Response:** Complete EPSS dataset for all CVEs on specified date

**Use Case:** Historical EPSS analysis, tracking score changes over time

### Query with Filters

**Filter by EPSS Score Threshold:**
```bash
curl "https://api.first.org/data/v1/epss?epss-gt=0.50"
```
Returns all CVEs with EPSS > 0.50 (50%)

**Filter by Percentile:**
```bash
curl "https://api.first.org/data/v1/epss?percentile-gt=0.95"
```
Returns all CVEs in top 5% (95th percentile and above)

**Combine Filters:**
```bash
curl "https://api.first.org/data/v1/epss?epss-gt=0.80&date=2025-11-09"
```
Returns CVEs with EPSS > 80% on specific date

### Rate Limits

**Current Rate Limits:** (as of EPSS v4)
- API is publicly accessible
- No authentication required for basic queries
- Reasonable use expected (don't hammer the API)

**Best Practices:**
- Cache results locally (EPSS updated daily, not in real-time)
- Use bulk queries for multiple CVEs (single request vs. multiple)
- Query once per day per CVE (scores don't change intraday)
- For large-scale automation, consider daily full dataset download

### Bulk Download

**Full Dataset Download:**

EPSS provides daily CSV files with complete dataset:
- URL: https://epss.cyentia.com/
- Format: CSV with columns: cve, epss, percentile, date
- Size: ~200MB compressed (all CVEs)

**Use Case:** Import into vulnerability management platform, data analysis, offline processing

### API Integration Example (Python)

```python
import requests
import json

def get_epss_score(cve_id):
    """Fetch EPSS score for a given CVE"""
    url = f"https://api.first.org/data/v1/epss?cve={cve_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['total'] > 0:
            cve_data = data['data'][0]
            return {
                'cve': cve_data['cve'],
                'epss': float(cve_data['epss']),
                'percentile': float(cve_data['percentile']) * 100,  # Convert to percentage
                'date': cve_data['date']
            }
        else:
            return None  # CVE not found in EPSS database

    except requests.exceptions.RequestException as e:
        print(f"Error fetching EPSS data: {e}")
        return None

# Example usage
cve = "CVE-2024-1234"
epss_data = get_epss_score(cve)

if epss_data:
    print(f"CVE: {epss_data['cve']}")
    print(f"EPSS Score: {epss_data['epss']*100:.2f}%")
    print(f"Percentile: {epss_data['percentile']:.1f}th")
    print(f"Date: {epss_data['date']}")
else:
    print(f"No EPSS data available for {cve}")
```

**Output Example:**
```
CVE: CVE-2024-1234
EPSS Score: 85.43%
Percentile: 97.2th
Date: 2025-11-09
```

---

## Integration with CVSS

### CVSS + EPSS: Complete Risk Picture

**Risk = Severity (CVSS) × Likelihood (EPSS)**

CVSS and EPSS answer complementary questions:

| Metric | Question | Provides | Limitation |
|--------|----------|----------|------------|
| **CVSS** | How bad is it IF exploited? | Impact severity (0.0-10.0) | Doesn't predict exploitation likelihood |
| **EPSS** | How likely TO BE exploited? | Probability (0-1) | Doesn't measure impact severity |

**Together:** CVSS (impact) × EPSS (likelihood) = **Risk**

### CVSS + EPSS Prioritization Matrix

| CVSS Severity | EPSS Probability | Combined Priority | Remediation Timeline |
|---------------|------------------|-------------------|---------------------|
| **Critical (9.0-10.0)** | High (>50%) | **P1 - Critical** | Immediate (72 hours) |
| **Critical (9.0-10.0)** | Medium (10-50%) | **P2 - High** | Urgent (7 days) |
| **Critical (9.0-10.0)** | Low (<10%) | **P2 - High** | Urgent (14 days) |
| **High (7.0-8.9)** | High (>50%) | **P1 - Critical** | Immediate (7 days) |
| **High (7.0-8.9)** | Medium (10-50%) | **P2 - High** | Urgent (14 days) |
| **High (7.0-8.9)** | Low (<10%) | **P3 - Medium** | Scheduled (30 days) |
| **Medium (4.0-6.9)** | High (>50%) | **P2 - High** | Urgent (14 days) |
| **Medium (4.0-6.9)** | Medium (10-50%) | **P3 - Medium** | Scheduled (30 days) |
| **Medium (4.0-6.9)** | Low (<10%) | **P3 - Medium** | Scheduled (60 days) |
| **Low (0.1-3.9)** | High (>50%) | **P3 - Medium** | Scheduled (30 days) |
| **Low (0.1-3.9)** | Medium (10-50%) | **P4 - Low** | Maintenance (90 days) |
| **Low (0.1-3.9)** | Low (<10%) | **P4 - Low** | Maintenance (next window) |

### Integration Examples

#### Example 1: High CVSS + High EPSS → P1 (Critical)

```
CVE-2024-AAAA: Remote Code Execution in Web Framework

CVSS v3.1: 9.8 (Critical)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- Network exploitable, no authentication, complete compromise

EPSS: 0.856 (85.6%)
Percentile: 97th (top 3%)
- Very high exploitation probability
- Likely active campaigns or public exploit code

→ PRIORITY: P1 (CRITICAL)
→ TIMELINE: Immediate (72 hours)
→ RATIONALE: Severe impact + high likelihood = critical risk
```

#### Example 2: High CVSS + Low EPSS → P2 (High, Not Critical)

```
CVE-2024-BBBB: Local Privilege Escalation

CVSS v3.1: 7.8 (High)
Vector: CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
- Local access required, but complete system compromise

EPSS: 0.018 (1.8%)
Percentile: 42nd (below median)
- Low exploitation probability
- No widespread exploit code or active campaigns

→ PRIORITY: P2 (HIGH)
→ TIMELINE: 30 days
→ RATIONALE: Severe impact but low likelihood; standard patching cycle acceptable
```

#### Example 3: Medium CVSS + High EPSS → P2 (High)

```
CVE-2024-CCCC: Authentication Bypass

CVSS v3.1: 6.5 (Medium)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N
- Network exploitable, limited impact (partial confidentiality/integrity)

EPSS: 0.752 (75.2%)
Percentile: 95th (top 5%)
- High exploitation probability despite moderate severity
- Active scanning or exploitation campaigns likely

→ PRIORITY: P2 (HIGH)
→ TIMELINE: 14 days
→ RATIONALE: Moderate impact but HIGH likelihood (active threat)
```

#### Example 4: Medium CVSS + Low EPSS → P3 (Medium)

```
CVE-2024-DDDD: Information Disclosure

CVSS v3.1: 5.3 (Medium)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
- Limited information disclosure

EPSS: 0.004 (0.4%)
Percentile: 15th (bottom 15%)
- Very low exploitation probability
- No exploit code, no active interest

→ PRIORITY: P3 (MEDIUM)
→ TIMELINE: 60 days
→ RATIONALE: Moderate impact, very low likelihood; routine maintenance acceptable
```

### Why EPSS Changes CVSS-Only Prioritization

**Traditional CVSS-Only Approach:**

All Critical/High CVSS vulnerabilities treated equally:
```
CVE-2024-AAAA: CVSS 9.8 → P1
CVE-2024-BBBB: CVSS 9.8 → P1
CVE-2024-CCCC: CVSS 9.8 → P1
CVE-2024-DDDD: CVSS 9.8 → P1

Result: 4 "critical" vulnerabilities requiring immediate attention
```

**CVSS + EPSS Approach:**

Prioritization refined by exploitation likelihood:
```
CVE-2024-AAAA: CVSS 9.8, EPSS 0.95 → P1 (Immediate - actively exploited)
CVE-2024-BBBB: CVSS 9.8, EPSS 0.45 → P2 (Urgent - moderate risk)
CVE-2024-CCCC: CVSS 9.8, EPSS 0.08 → P2 (Scheduled - low likelihood)
CVE-2024-DDDD: CVSS 9.8, EPSS 0.01 → P3 (Maintenance - very unlikely)

Result: 1 immediate, 2 urgent, 1 scheduled - resources focused on real threats
```

**Impact:** EPSS reduces "critical" workload by 50-75% while maintaining coverage of actually exploited vulnerabilities.

### Integration with CISA KEV

**Priority Override Rule:**

```
IF vulnerability IN CISA KEV catalog THEN
    Priority = P1 (Critical) regardless of CVSS or EPSS
ELSE
    Use CVSS + EPSS matrix
END IF
```

**Rationale:** KEV = confirmed active exploitation (ground truth, not prediction)

**Example:**
```
CVE-2024-EEEE: Moderate Vulnerability

CVSS v3.1: 6.5 (Medium)
EPSS: 0.12 (12%) - Low
KEV: YES - Added 2025-11-05

→ PRIORITY: P1 (CRITICAL) - KEV override
→ TIMELINE: Immediate (14 days per BOD 22-01)
→ RATIONALE: Confirmed exploitation trumps predictive scores
```

### Recommended Priority Framework

**Step 1: Check KEV Status**
```
IF in CISA KEV → P1 (Immediate)
```

**Step 2: Apply CVSS + EPSS Matrix**
```
High CVSS (7.0+) + High EPSS (>50%) → P1
High CVSS (7.0+) + Low EPSS (<50%) → P2
Med CVSS (4.0-6.9) + High EPSS (>50%) → P2
Med CVSS (4.0-6.9) + Low EPSS (<50%) → P3
Low CVSS (<4.0) → P4 (unless KEV)
```

**Step 3: Adjust for Business Context**
```
Internet-facing + P2 → Elevate to P1
Air-gapped + P1 → May downgrade to P2
Critical asset + any priority → Elevate one level
Non-production + any priority → May downgrade one level
```

---

## EPSS Examples

### Example 1: Critical CVSS + High EPSS → Active Threat

```
CVE-2024-21887: Ivanti Connect Secure Command Injection

CVSS v3.1: 9.1 (Critical)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

EPSS: 0.975 (97.5%)
Percentile: 99.8th (top 0.2%)

KEV Status: YES (added to CISA KEV)

Timeline:
- Day 0: Disclosure by Ivanti, CVSS 9.1, EPSS 0.05 (5%)
- Day 3: PoC exploit published, EPSS jumps to 0.45 (45%)
- Day 7: Active exploitation confirmed, added to KEV, EPSS 0.82 (82%)
- Day 14: Widespread campaigns, EPSS peaks at 0.975 (97.5%)

→ PRIORITY: P1 (CRITICAL)
→ ACTIONS TAKEN:
  - Emergency patching within 72 hours
  - Temporary WAF rules deployed
  - Enhanced monitoring for compromise indicators
  - Incident response team on standby

OUTCOME: EPSS correctly predicted extremely high exploitation risk before widespread attacks occurred.
```

### Example 2: High CVSS + Low EPSS → Theoretical Risk

```
CVE-2024-XXXX: Hypothetical Linux Kernel Vulnerability

CVSS v3.1: 8.8 (High)
Vector: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H

EPSS: 0.023 (2.3%)
Percentile: 38th (below median)

KEV Status: NO

Analysis:
- Requires non-default configuration (rarely deployed)
- Complex exploitation requirements (race condition)
- No public exploit code available
- Security researchers show limited interest
- Vendor patch available immediately upon disclosure

→ PRIORITY: P3 (MEDIUM)
→ TIMELINE: 30-60 days (routine patching)
→ RATIONALE: Despite high severity, exploitation unlikely due to complexity and limited attacker interest

OUTCOME: EPSS correctly identified this as lower priority despite high CVSS. No observed exploitation after 6 months.
```

### Example 3: Medium CVSS + High EPSS → Actively Exploited

```
CVE-2024-YYYY: ProxyLogon (Microsoft Exchange)

CVSS v3.1: 6.5 (Medium)
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N

EPSS: 0.889 (88.9%)
Percentile: 98th (top 2%)

KEV Status: YES

Timeline:
- Day 0: Disclosed by Microsoft, CVSS 6.5, EPSS 0.08 (8%)
- Day 2: ProxyLogon exploit chain published, EPSS 0.32 (32%)
- Day 5: Mass scanning observed, EPSS 0.68 (68%)
- Day 10: Ransomware groups exploiting, added to KEV, EPSS 0.889 (88.9%)

→ PRIORITY: P1 (CRITICAL) despite medium CVSS
→ RATIONALE: High EPSS + KEV = confirmed widespread exploitation

OUTCOME: EPSS + KEV elevated this "Medium" vulnerability to critical priority. Organizations that ignored it due to CVSS 6.5 rating suffered ransomware attacks.
```

### Example 4: Low CVSS + Very Low EPSS → Safe to Defer

```
CVE-2024-ZZZZ: Obscure Library Information Leak

CVSS v3.1: 3.7 (Low)
Vector: CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N

EPSS: 0.001 (0.1%)
Percentile: 5th (bottom 5%)

KEV Status: NO

Analysis:
- Rarely used library (minimal deployment)
- Limited information disclosure (non-sensitive metadata)
- High attack complexity (requires specific timing)
- No known exploit code
- Low CVSS + very low EPSS

→ PRIORITY: P4 (LOW)
→ TIMELINE: Next maintenance window (90+ days)
→ RATIONALE: Minimal impact, negligible exploitation likelihood

OUTCOME: Safe to defer indefinitely; focus resources on higher-risk vulnerabilities.
```

### Example 5: EPSS as Early Warning System

```
CVE-2024-AAAA: Zero-Day Becoming Public

CVSS v3.1: 7.5 (High)

EPSS Timeline (Early Warning):
- Week 1: EPSS 0.02 (2%) - Initial disclosure, no exploits
- Week 2: EPSS 0.08 (8%) - PoC code appears on GitHub
- Week 3: EPSS 0.35 (35%) - Security tool coverage added (Nuclei, Metasploit)
- Week 4: EPSS 0.71 (71%) - Active scanning detected by honeypots
- Week 5: EPSS 0.89 (89%) - Widespread exploitation campaigns

→ EPSS AS EARLY WARNING:
  Week 1-2: Monitor (normal priority)
  Week 3: Elevate to P2 (EPSS rising, tools added)
  Week 4: Elevate to P1 (EPSS >70%, active scanning)
  Week 5: Emergency response (widespread exploitation)

OUTCOME: EPSS provided 3-week warning before widespread exploitation, enabling proactive patching.
```

### Example 6: Old CVE Resurfaces

```
CVE-2017-XXXX: Old Vulnerability Rediscovered

CVSS v3.1: 8.1 (High)

EPSS Timeline:
- 2017-2023: EPSS 0.01-0.03 (1-3%) - Dormant for years
- 2024 Week 1: EPSS 0.04 (4%) - Still dormant
- 2024 Week 2: EPSS 0.62 (62%) - Sudden spike
- 2024 Week 3: EPSS 0.85 (85%) - Added to KEV

Analysis:
- Vulnerability discovered in 2017, largely ignored
- 2024: Attackers discover unpatched legacy systems still vulnerable
- Ransomware groups add to exploit kits
- Mass exploitation of forgotten vulnerability

→ EPSS DETECTS RESURGENCE:
  Organizations monitoring EPSS noticed spike in 7-year-old CVE
  Proactive remediation before widespread attacks

OUTCOME: EPSS successfully identified "zombie vulnerability" becoming active threat, despite old age.
```

---

## Limitations and Considerations

### 1. EPSS is Predictive, Not Definitive

**Limitation:** EPSS estimates probability, not certainty

**What This Means:**
- EPSS 0.95 (95%) does NOT mean "will definitely be exploited"
- EPSS 0.05 (5%) does NOT mean "will definitely NOT be exploited"
- EPSS reflects population-level risk, not individual system certainty

**Analogy:** Weather forecast saying "95% chance of rain" doesn't guarantee rain, but you should bring an umbrella.

**Implication:** Use EPSS for prioritization, not as guarantee of exploitation or non-exploitation.

### 2. EPSS Predicts Broad Exploitation, Not Targeted Attacks

**Limitation:** EPSS model trained on mass exploitation data, not APT or targeted attacks

**What This Means:**
- EPSS reflects widespread exploitation campaigns (botnets, ransomware, opportunistic attackers)
- EPSS may not capture targeted attacks by sophisticated threat actors (nation-states, APTs)
- Zero-day vulnerabilities used in targeted attacks may have low EPSS initially

**Example:**
```
CVE-XXXX: Used by APT group against specific defense contractors
- CVSS: 8.8 (High)
- EPSS: 0.03 (3%) - Low because not widely exploited
- Threat Intelligence: Active use by APT28 in targeted campaigns

→ EPSS low because exploitation is targeted, not widespread
→ Still P1 priority for organizations in targeted sector
```

**Implication:** Combine EPSS with threat intelligence for complete picture, especially for high-value targets.

### 3. EPSS Changes Daily

**Limitation:** EPSS is dynamic; scores can change significantly day-to-day

**What This Means:**
- Low EPSS today may be high EPSS tomorrow (exploit published)
- High EPSS today may decrease over time (campaign ends, patches deployed)
- Static EPSS checks are insufficient for long-term vulnerability management

**Best Practice:**
- Re-check EPSS regularly for unpatched vulnerabilities (weekly minimum)
- Set up alerts for significant EPSS increases (>20% jump)
- Use EPSS API or daily downloads for automation

**Example:**
```
Week 1: CVE-2024-XXXX EPSS 0.05 → Deprioritized
Week 2: EPSS jumps to 0.75 → Exploit published, now P1
Week 3: EPSS 0.89 → Widespread exploitation

Organization that checked EPSS once missed critical threat evolution.
```

### 4. Zero-Day Vulnerabilities May Have Low Initial EPSS

**Limitation:** Newly disclosed vulnerabilities may not yet have exploitation data

**What This Means:**
- Day 0 disclosure: EPSS based on vulnerability characteristics alone (no exploitation history)
- May initially show low EPSS (0.01-0.05) before exploits appear
- EPSS will increase rapidly once exploitation begins

**Timeline Example:**
```
Day 0 (Disclosure): EPSS 0.02 (limited data)
Day 3 (PoC Published): EPSS 0.15
Day 7 (Active Exploitation): EPSS 0.68
Day 14 (Widespread): EPSS 0.92
```

**Implication:** For newly disclosed Critical/High CVSS vulnerabilities, don't rely solely on low initial EPSS. Monitor closely for changes.

**Best Practice:** Treat new disclosures with High/Critical CVSS as high priority for first 14 days regardless of EPSS, then reassess.

### 5. EPSS Doesn't Capture Business Context

**Limitation:** EPSS is vulnerability-centric, not asset-centric

**What This Means:**
- EPSS doesn't know if vulnerability is in production vs. test environment
- EPSS doesn't know if system is internet-facing vs. air-gapped
- EPSS doesn't know if data is sensitive vs. non-sensitive
- EPSS doesn't account for compensating controls

**Example:**
```
CVE-2024-XXXX: High EPSS 0.85
- System A: Internet-facing production database (customer PII) → P1
- System B: Air-gapped test environment (dummy data) → P3

Same CVE, same EPSS, different priorities based on business context.
```

**Implication:** Always apply business context on top of EPSS-based prioritization.

### 6. Model Performance is Not 100%

**Limitation:** EPSS is machine learning model with inherent prediction errors

**Performance Metrics (EPSS v3):**
- **Coverage (Recall):** ~80% of exploited vulnerabilities captured when prioritizing top 5% by EPSS
- **Efficiency (Precision):** ~50% of vulnerabilities in top 5% EPSS are actually exploited

**What This Means:**
- False Positives: Some high-EPSS vulnerabilities won't be exploited (~50%)
- False Negatives: Some low-EPSS vulnerabilities will be exploited (~20%)

**Trade-off:**
```
Prioritize Top 5% EPSS:
- Remediates ~5% of all CVEs (manageable workload)
- Catches ~80% of actually exploited CVEs (good coverage)
- 50% of prioritized CVEs won't be exploited (acceptable false positive rate)
```

**Implication:** EPSS is optimization tool, not perfect predictor. Accept some false positives to achieve better coverage than CVSS-only approach.

### 7. EPSS Doesn't Replace Other Tools

**Limitation:** EPSS is one input to risk decisions, not complete solution

**What EPSS Doesn't Provide:**
- Severity assessment (use CVSS)
- Confirmed exploitation (use CISA KEV)
- Threat actor attribution (use threat intelligence)
- Attack technique mapping (use MITRE ATT&CK)
- Asset criticality (use asset inventory/CMDB)
- Compensating controls (use security architecture docs)

**Complete Vulnerability Risk Assessment Requires:**
```
Risk = f(
    CVSS (severity),
    EPSS (exploitability probability),
    KEV (confirmed exploitation),
    Threat Intelligence (targeted threats),
    Asset Criticality (business impact),
    Exposure (attack surface),
    Compensating Controls (defense-in-depth)
)
```

**Implication:** Integrate EPSS into comprehensive vulnerability management program, not as standalone tool.

### 8. EPSS May Lag Behind Reality

**Limitation:** EPSS updated daily, but exploitation can occur instantly

**What This Means:**
- Zero-day announced Monday morning → EPSS won't reflect it until Tuesday
- Sudden mass exploitation → EPSS may lag 24-72 hours behind reality
- EPSS is backward-looking (trained on historical data) with forward prediction

**Best Practice:**
- Don't wait for EPSS to increase before acting on Critical/High CVSS vulnerabilities
- Monitor threat intelligence and news for emerging threats
- Use EPSS as trend indicator, not real-time threat feed

### 9. Not All CVEs Have EPSS Scores

**Limitation:** EPSS may not cover all CVEs, especially very new or very old ones

**Coverage:**
- EPSS scores ~90%+ of published CVEs
- Very new CVEs (published today) may not have score yet (updated next day)
- Some obscure or very old CVEs may lack scores

**What to Do:**
- If no EPSS score available, fall back to CVSS + business context
- Check back next day for newly published CVEs
- Assume moderate risk for missing EPSS (don't assume safe)

---

## Authoritative References

### Official EPSS Resources

**EPSS Home Page**
- URL: https://www.first.org/epss/
- Publisher: FIRST (Forum of Incident Response and Security Teams)
- Use: Primary reference for EPSS overview, documentation, and updates

**EPSS Model Documentation**
- URL: https://www.first.org/epss/model
- Publisher: FIRST
- Use: Technical details on model architecture, data sources, and methodology

**EPSS API Documentation**
- URL: https://www.first.org/epss/api
- Publisher: FIRST
- Use: API reference for programmatic access to EPSS scores

**EPSS Data Downloads**
- URL: https://epss.cyentia.com/
- Publisher: Cyentia Institute (EPSS data partner)
- Use: Daily CSV downloads of complete EPSS dataset

### EPSS Research Papers

**"Exploit Prediction Scoring System (EPSS)" - Original Paper**
- Authors: Jay Jacobs, Sasha Romanosky, et al.
- URL: https://www.first.org/epss/articles
- Use: Academic foundation and validation of EPSS methodology

**EPSS Performance Reports**
- URL: https://www.first.org/epss/validation
- Use: Model accuracy metrics, coverage statistics, efficiency analysis

### Integration Guides

**FIRST CVSS + EPSS Integration Guide**
- URL: https://www.first.org/cvss/
- Use: Best practices for combining CVSS severity with EPSS probability

**CISA KEV Catalog**
- URL: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Use: Confirmed exploitation data to complement EPSS predictions
- See: `kev-catalog-guide.md`

### Complementary Resources

**CVSS Scoring System**
- URL: https://www.first.org/cvss/
- Use: Severity assessment to complement EPSS exploitability
- See: `cvss-guide.md`

**MITRE ATT&CK Framework**
- URL: https://attack.mitre.org/
- Use: Attack technique mapping for threat context
- See: `mitre-attack-mapping-guide.md`

**Priority Framework**
- See: `priority-framework.md`
- Use: Complete vulnerability prioritization methodology integrating CVSS, EPSS, KEV, and business context

### Tools and Calculators

**EPSS Calculator/Lookup**
- URL: https://www.first.org/epss/
- Use: Quick lookup of EPSS scores for specific CVEs

**Vulnerability Management Platforms with EPSS Integration:**
- Qualys VMDR
- Tenable.io
- Rapid7 InsightVM
- Rezilion
- (Most major VM platforms now integrate EPSS)

### Community and Support

**FIRST Member Community**
- URL: https://www.first.org/membership/
- Use: Access to FIRST community, working groups, and conferences

**EPSS Mailing List**
- URL: https://www.first.org/epss/contact
- Use: Updates on EPSS model changes, new versions, and best practices

---

## Document Metadata

**Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** Security Engineering Team
**Audience:** Security Analysts, Vulnerability Managers, Risk Analysts
**Related Documents:**
- `cvss-guide.md` - CVSS severity scoring reference
- `kev-catalog-guide.md` - CISA KEV catalog usage
- `priority-framework.md` - Complete vulnerability prioritization framework
- `mitre-attack-mapping-guide.md` - MITRE ATT&CK technique mapping

**Document Purpose:** Comprehensive reference for understanding, applying, and integrating EPSS probability scores into vulnerability management and risk prioritization workflows.

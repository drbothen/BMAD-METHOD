# Event Investigation Best Practices

## Table of Contents

1. [Introduction](#1-introduction)
2. [NIST SP 800-61 Framework Integration](#2-nist-sp-800-61-framework-integration)
3. [Investigation Methodology](#3-investigation-methodology)
4. [Disposition Framework](#4-disposition-framework)
5. [Common False Positive Patterns](#5-common-false-positive-patterns)
6. [Cognitive Biases in Event Investigation](#6-cognitive-biases-in-event-investigation)
7. [ICS/SCADA-Specific Considerations](#7-icsscada-specific-considerations)
8. [Investigation Workflow Checklist](#8-investigation-workflow-checklist)
9. [References](#9-references)

---

## 1. Introduction

### Purpose

This knowledge base provides comprehensive guidance for security analysts and reviewers conducting event investigations in enterprise and industrial control system (ICS/SCADA) environments. It establishes standardized methodologies, disposition criteria, and best practices to ensure consistent, thorough, and effective event analysis.

### Scope

This document covers:

- **NIST SP 800-61 incident handling framework integration** - Aligning event investigation with established federal guidelines
- **Hypothesis-driven investigation methodology** - Structured approach to evidence collection and analysis
- **Disposition framework** - Clear criteria for categorizing event outcomes (TP/FP/BTP)
- **False positive pattern recognition** - Common causes and tuning recommendations
- **Cognitive bias awareness** - Understanding and mitigating investigative biases
- **ICS/SCADA considerations** - Specialized guidance for operational technology environments

### Target Audience

- **Security Analysts**: Front-line investigators performing initial event triage and analysis
- **Security Reviewers**: Second-level reviewers validating analyst findings and disposition decisions
- **Incident Response Teams**: Teams escalating events from detection to full incident response
- **Security Operations Leadership**: Managers establishing investigation quality standards

---

## 2. NIST SP 800-61 Framework Integration

### Overview of NIST SP 800-61 Rev 2

[NIST Special Publication 800-61 Revision 2][1] defines a four-phase incident handling lifecycle that provides the foundational framework for computer security incident response. Event investigation is a critical component of the **Detection and Analysis** phase.

### Four-Phase Incident Handling Lifecycle

#### Phase 1: Preparation

**Purpose**: Establish capabilities and resources before incidents occur.

**Key Activities**:
- Deploy monitoring and detection systems (IDS/IPS, SIEM, EDR)
- Define incident response procedures and escalation paths
- Train analysts on investigation techniques and tools
- Establish communication protocols with stakeholders

**Event Investigation Relevance**: Preparation determines the quality and quantity of evidence available during investigations. Well-configured logging, alerting, and monitoring systems directly impact investigative effectiveness.

#### Phase 2: Detection and Analysis

**Purpose**: Identify potential security incidents and determine their scope and impact.

**Key Activities**:
- **Alert Triage**: Review security alerts from monitoring systems
- **Initial Analysis**: Determine if alert indicates genuine incident
- **Evidence Collection**: Gather logs, network traffic, endpoint data
- **Event Correlation**: Link related events to understand attack patterns
- **Impact Assessment**: Evaluate functional, information, and recoverability impacts
- **Prioritization**: Assign severity based on NIST criteria (see below)
- **Disposition Determination**: Classify as True Positive, False Positive, or Benign True Positive
- **Escalation Decision**: Determine if event requires full incident response

**Event Investigation Relevance**: This is where event investigation primarily occurs. The methodologies in Section 3 of this KB map directly to this phase.

#### Phase 3: Containment, Eradication, and Recovery

**Purpose**: Prevent incident spread, remove threat, and restore normal operations.

**Event Investigation Relevance**: Events classified as True Positives requiring escalation transition to this phase. Investigation findings provide critical context for containment strategies.

#### Phase 4: Post-Incident Activity

**Purpose**: Learn from incidents to improve future response.

**Key Activities**:
- Conduct lessons learned meetings
- Update detection rules based on false positive patterns
- Refine investigation procedures
- Document findings in knowledge management systems

**Event Investigation Relevance**: Post-incident reviews of event dispositions (especially false positives) drive continuous improvement in detection accuracy and investigation efficiency.

### Evidence Preservation and Chain of Custody

#### Evidence Collection Best Practices

**Principle**: Preserve evidence integrity for potential legal proceedings or forensic analysis.

**Guidelines**:

1. **Document Collection Time**: Record UTC timestamp when evidence collected
2. **Preserve Original Sources**: Never modify original log files or system artifacts
3. **Use Write-Blockers**: When imaging systems, use hardware/software write-blockers
4. **Calculate Cryptographic Hashes**: Generate MD5/SHA-256 hashes to verify integrity
5. **Maintain Chain of Custody**: Document who accessed evidence and when
6. **Store Securely**: Use access-controlled repositories with audit logging

**Example Chain of Custody Record**:

```
Evidence Item: firewall.log (2025-11-09 14:32:18 UTC to 2025-11-09 14:45:22 UTC)
SHA-256: a3f8b2c1d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
Collected By: John Smith (Analyst)
Collected Time: 2025-11-09 15:00:00 UTC
Stored Location: /evidence/case-2025-1109-001/firewall.log
Access Log:
  - 2025-11-09 15:00:00 UTC: John Smith (Collection)
  - 2025-11-09 16:30:00 UTC: Sarah Johnson (Review)
  - 2025-11-09 18:00:00 UTC: Mike Chen (Forensic Analysis)
```

#### Legal Considerations

- **Admissibility**: Evidence must be collected and preserved following legal standards (Federal Rules of Evidence if applicable)
- **Privacy**: Ensure collection complies with privacy regulations (GDPR, CCPA, internal policies)
- **Authorization**: Obtain proper authorization before collecting evidence from systems (especially third-party or personal devices)

### Prioritization Criteria (NIST SP 800-61 Section 3.2.6)

NIST defines three impact categories for prioritizing incidents:

#### Functional Impact

**Definition**: Impact to the business functionality of systems.

**Levels**:
- **None**: No effect on organization's ability to provide services
- **Low**: Minimal effect; organization can still provide all critical services
- **Medium**: Organization has lost ability to provide a critical service to subset of users
- **High**: Organization unable to provide some critical services to any users

**Examples**:
- **High**: Ransomware encrypting critical production database
- **Medium**: DDoS attack affecting external website (internal operations continue)
- **Low**: Malware on single workstation (isolated from critical systems)

#### Information Impact

**Definition**: Impact to the confidentiality, integrity, or availability of information.

**Levels**:
- **None**: No information compromised
- **Privacy Breach**: Sensitive personally identifiable information (PII) accessed or exfiltrated
- **Proprietary Breach**: Unclassified proprietary information accessed or exfiltrated
- **Integrity Loss**: Sensitive or proprietary information modified or deleted

**Examples**:
- **Proprietary Breach**: Intellectual property exfiltrated by APT group
- **Privacy Breach**: Customer database accessed by unauthorized party
- **Integrity Loss**: Financial records altered by attacker

#### Recoverability

**Definition**: Time and resources required to recover from incident.

**Levels**:
- **Regular**: Time to recovery predictable with existing resources
- **Supplemented**: Time to recovery predictable with additional resources
- **Extended**: Time to recovery unpredictable; additional resources and outside help needed
- **Not Recoverable**: Recovery not possible (e.g., sensitive data publicly released)

**Examples**:
- **Extended**: Ransomware with no backups available; requires forensic recovery and system rebuilds
- **Supplemented**: Database corruption requiring vendor support to restore
- **Regular**: Malware infection cleanable with standard EDR tools

### Mapping Event Investigation to NIST Framework

| Investigation Activity | NIST Phase | NIST Section |
|------------------------|------------|--------------|
| Alert triage and initial review | Detection and Analysis | 3.2.4 |
| Evidence collection (logs, network, endpoint) | Detection and Analysis | 3.2.5 |
| Event correlation and analysis | Detection and Analysis | 3.2.5 |
| Impact assessment | Detection and Analysis | 3.2.6 |
| Prioritization (Functional/Information/Recoverability) | Detection and Analysis | 3.2.6 |
| Disposition determination (TP/FP/BTP) | Detection and Analysis | 3.2.5 |
| Incident declaration and escalation | Detection and Analysis → Containment | 3.2.5 → 3.3 |
| False positive tuning recommendations | Post-Incident Activity | 3.4 |

---

## 3. Investigation Methodology

### Hypothesis-Driven Investigation Approach

#### Principles

**Hypothesis-driven investigation** applies the scientific method to event analysis. Rather than collecting evidence randomly, analysts form testable hypotheses and seek evidence to confirm or refute them.

**Process**:

1. **Formulate Initial Hypothesis**: Based on alert details, propose explanation (e.g., "This port scan is reconnaissance for targeted attack")
2. **Identify Evidence Needed**: Determine what data would support or refute hypothesis
3. **Collect Evidence**: Gather logs, network traffic, endpoint data
4. **Test Hypothesis**: Analyze evidence against hypothesis
5. **Refine or Pivot**: If evidence contradicts hypothesis, formulate alternative hypothesis
6. **Iterate**: Repeat until confident conclusion reached

**Benefits**:
- **Focused Investigation**: Avoids aimless data collection
- **Bias Mitigation**: Encourages considering alternative explanations
- **Documentation**: Clear reasoning trail for reviewers
- **Efficiency**: Reduces time spent on irrelevant data

#### Example Hypothesis-Driven Investigation

**Alert**: "Multiple Failed SSH Login Attempts - Server: prod-web-01 - Source: 203.0.113.50"

**Initial Hypothesis**: "External attacker attempting brute force credential attack"

**Evidence to Collect**:
- SSH authentication logs (successful and failed attempts)
- Network flow data (connection duration, byte counts)
- Firewall logs (other traffic from source IP)
- Threat intelligence (reputation of source IP)
- User account activity (recent password changes, account lockouts)

**Evidence Found**:
- 15 failed logins over 5 minutes
- Source IP: 203.0.113.50 (VPN endpoint IP for company VPN provider)
- Account: jsmith (valid employee)
- User jsmith changed password 10 minutes before failed attempts
- No other suspicious traffic from source IP

**Hypothesis Refinement**: "Employee with expired VPN credentials attempting to connect after password change"

**Evidence for Refined Hypothesis**:
- Contacted user jsmith: confirmed changed password and had trouble reconnecting VPN
- VPN logs show successful authentication 3 minutes after failed SSH attempts
- SSH authentication succeeded after VPN reconnection

**Conclusion**: False Positive - legitimate user activity after password change

**Confidence Level**: High (user confirmation + corroborating VPN logs)

### Evidence Collection Best Practices

#### Types of Evidence

**1. Log Data**

**Sources**:
- System logs (Windows Event Logs, syslog)
- Application logs (web server access/error logs, database logs)
- Security logs (IDS/IPS, firewall, proxy, EDR)
- Authentication logs (Active Directory, LDAP, SSO)

**Collection Guidance**:
- **Time Range**: Collect logs from before alert trigger through present (recommend +/- 1 hour buffer)
- **Related Systems**: Include logs from upstream/downstream systems (e.g., firewall + web server + database)
- **Log Integrity**: Verify logs haven't been tampered with (check for gaps, inconsistencies)

**Example Evidence Collection**:

```
Alert: SQL Injection Attempt Detected
Time: 2025-11-09 14:45:22 UTC
System: prod-db-01

Logs to Collect:
- Web server access logs: 2025-11-09 13:45:00 - 15:45:00 UTC
- Web application logs: 2025-11-09 13:45:00 - 15:45:00 UTC
- Database query logs: 2025-11-09 13:45:00 - 15:45:00 UTC
- WAF logs: 2025-11-09 13:45:00 - 15:45:00 UTC
- Network firewall logs: 2025-11-09 13:45:00 - 15:45:00 UTC
```

**2. Network Traffic Data**

**Sources**:
- Full packet captures (PCAP from IDS/IPS or network TAPs)
- NetFlow/IPFIX (flow metadata)
- DNS query logs
- Proxy logs (HTTP/HTTPS inspection)

**Collection Guidance**:
- **PCAP Size**: Full packet captures can be large; filter by source/destination IP and port if possible
- **Encryption**: HTTPS traffic requires SSL/TLS inspection at proxy or endpoint
- **Privacy**: Ensure packet capture complies with privacy policies (avoid capturing personal data unnecessarily)

**Example Evidence Collection**:

```
Alert: Data Exfiltration to External IP
Time: 2025-11-09 14:45:22 UTC
Source: workstation-042 (10.1.50.42)
Destination: 198.51.100.75 (suspicious external IP)

Network Data to Collect:
- Full PCAP: src=10.1.50.42, dst=198.51.100.75, time=14:30:00-15:00:00 UTC
- NetFlow: src=10.1.50.42, all destinations, time=14:00:00-15:00:00 UTC
- DNS queries: host=workstation-042, time=14:00:00-15:00:00 UTC
- Proxy logs: src=10.1.50.42, time=14:00:00-15:00:00 UTC
```

**3. Endpoint Data**

**Sources**:
- EDR telemetry (process execution, file modifications, registry changes, network connections)
- File system artifacts (suspicious files, timestamps)
- Memory dumps (for malware analysis)
- User activity (login times, application usage)

**Collection Guidance**:
- **EDR Queries**: Use EDR platform to query process trees, command-line arguments, network connections
- **Volatile Data**: Collect memory dumps before system reboot (volatile data lost on reboot)
- **Isolation**: Consider isolating endpoint from network to prevent further compromise (balance with operational impact)

**Example Evidence Collection**:

```
Alert: Malware Detected - Host: workstation-042
Time: 2025-11-09 14:45:22 UTC
File: C:\Users\jsmith\Downloads\invoice.exe

Endpoint Data to Collect:
- Process execution history: workstation-042, last 24 hours
- File system changes: C:\Users\jsmith\*, last 24 hours
- Network connections: workstation-042, last 24 hours
- Memory dump: workstation-042 (if malware still running)
- File sample: C:\Users\jsmith\Downloads\invoice.exe (for malware analysis)
- User activity: jsmith, last 24 hours (login times, files accessed)
```

#### Evidence Collection Workflow

**Step 1: Identify Required Evidence**

Based on alert type and initial hypothesis, determine what evidence is needed.

**Step 2: Prioritize Collection**

Prioritize volatile data (memory, network traffic) over persistent data (disk files, archived logs).

**Step 3: Collect Evidence**

Use appropriate tools:
- **SIEM**: Query centralized logs
- **EDR**: Query endpoint telemetry
- **Network Tools**: tcpdump, Wireshark, Zeek for packet capture
- **Disk Forensics**: FTK, Autopsy for file system analysis

**Step 4: Preserve Evidence**

Follow chain of custody procedures (Section 2).

**Step 5: Document Collection**

Record what was collected, when, from where, and by whom.

### Event Correlation Techniques

**Event correlation** links related events to understand attacker behavior and attack progression.

#### Time-Based Correlation

**Technique**: Group events occurring within same time window.

**Use Case**: Identify related events in multi-stage attack.

**Example**:

```
14:30:00 UTC: Port scan detected (src=198.51.100.75, dst=10.1.0.0/16)
14:32:15 UTC: SSH brute force detected (src=198.51.100.75, dst=10.1.5.10)
14:35:42 UTC: Successful SSH login (src=198.51.100.75, dst=10.1.5.10, user=backup)
14:37:10 UTC: Unusual file access (host=10.1.5.10, file=/etc/shadow)
14:38:55 UTC: Large data transfer (src=10.1.5.10, dst=198.51.100.75, bytes=500MB)

Correlation: These events form attack chain (reconnaissance → exploitation → privilege escalation → exfiltration)
```

**Time Window Guidance**:
- **Fast Attacks**: 5-30 minute window (automated tools, scripted attacks)
- **Slow Attacks**: Hours to days (APT reconnaissance, low-and-slow exfiltration)

#### Pattern-Based Correlation

**Technique**: Group events matching common attack patterns (MITRE ATT&CK tactics/techniques).

**Use Case**: Identify attacks following known playbooks.

**Example**:

```
Event 1: Phishing email opened (technique: T1566.001 - Spearphishing Attachment)
Event 2: Malicious macro executed (technique: T1204.002 - User Execution: Malicious File)
Event 3: PowerShell download cradle (technique: T1059.001 - Command and Scripting Interpreter: PowerShell)
Event 4: Credential dumping (technique: T1003 - OS Credential Dumping)
Event 5: Lateral movement via WMI (technique: T1047 - Windows Management Instrumentation)

Pattern: Typical phishing-to-lateral-movement attack chain
```

**Pattern Recognition Resources**:
- [MITRE ATT&CK for ICS][2] - OT-specific tactics and techniques
- [MITRE ATT&CK Enterprise][3] - IT environment tactics and techniques
- Threat intelligence feeds (vendor-specific attack patterns)

#### Topological Correlation

**Technique**: Group events based on network topology or system relationships.

**Use Case**: Identify lateral movement, privilege escalation through trust relationships.

**Example**:

```
Network Topology:
  DMZ: web-server-01 (10.1.1.10)
  App Tier: app-server-01 (10.1.2.10), app-server-02 (10.1.2.11)
  DB Tier: db-server-01 (10.1.3.10)

Event 1: SQL injection on web-server-01 (10.1.1.10)
Event 2: Unusual connection: web-server-01 → app-server-01 (10.1.2.10) on port 22
Event 3: Unusual connection: app-server-01 → db-server-01 (10.1.3.10) on port 3306
Event 4: Database dump initiated on db-server-01

Correlation: Attacker pivoted through network tiers (DMZ → App → DB) using compromised web server
```

**Topological Analysis**:
- Map attack path through network segments
- Identify trust relationships exploited (service accounts, shared credentials)
- Assess blast radius (how far attacker can reach from initial compromise)

### Timeline Reconstruction

**Timeline reconstruction** creates chronological sequence of events to understand attack progression.

#### Timeline Components

**Event**: Single observable occurrence (log entry, alert, user action)

**Timestamp**: UTC time when event occurred (or was logged)

**Source**: System, user, or process that generated event

**Description**: What happened

**Significance**: Why event matters (evidence for/against hypothesis)

#### Timeline Example

```
=== Investigation Timeline: Suspected Data Exfiltration ===
Case ID: 2025-1109-001
Analyst: John Smith
Investigation Start: 2025-11-09 15:00:00 UTC

2025-11-09 14:15:30 UTC [workstation-042] User jsmith received email with attachment "invoice.pdf.exe"
  Significance: Potential phishing attempt (suspicious file extension)

2025-11-09 14:16:45 UTC [workstation-042] User jsmith executed "invoice.pdf.exe"
  Significance: User executed suspicious file (malware delivery?)

2025-11-09 14:17:02 UTC [workstation-042] Process "invoice.pdf.exe" spawned PowerShell process
  Significance: Typical malware behavior (process injection or download cradle)

2025-11-09 14:17:15 UTC [workstation-042] PowerShell process made DNS query for "malicious-c2.example.com"
  Significance: Potential C2 communication

2025-11-09 14:17:22 UTC [workstation-042] PowerShell process downloaded file from "malicious-c2.example.com"
  Significance: Malware stage 2 download

2025-11-09 14:18:05 UTC [workstation-042] New process "svchost.exe" created (parent: invoice.pdf.exe)
  Significance: Masquerading as legitimate Windows process

2025-11-09 14:20:30 UTC [workstation-042] Process "svchost.exe" accessed files in C:\Users\jsmith\Documents\
  Significance: Data collection phase

2025-11-09 14:25:12 UTC [workstation-042] Large outbound connection to 198.51.100.75 (500 MB transferred)
  Significance: Data exfiltration to external IP

2025-11-09 14:30:00 UTC [workstation-042] Process "svchost.exe" terminated
  Significance: Malware cleanup (covering tracks)

=== Timeline Analysis ===
Attack Duration: ~15 minutes (rapid automated attack)
Attack Pattern: Phishing → Execution → C2 → Exfiltration
Disposition: True Positive - Confirmed malware infection with data exfiltration
Recommended Action: Isolate workstation-042, initiate incident response, analyze exfiltrated data
```

#### Timeline Tools

- **SIEM**: Centralized log correlation with timeline visualization
- **SOAR**: Automated timeline generation from playbook execution
- **Plaso/log2timeline**: Forensic timeline creation from disk images
- **Timesketch**: Open-source collaborative timeline analysis

### Alternative Hypothesis Consideration

**Critical Principle**: Always consider alternative explanations before concluding investigation.

**Why This Matters**:
- Mitigates confirmation bias (seeking only supporting evidence)
- Prevents false positive misclassification
- Identifies edge cases requiring further investigation

#### Alternative Hypothesis Checklist

Before finalizing disposition, ask:

- [ ] **Could this be legitimate user/system behavior?** (Consider user habits, system maintenance, batch jobs)
- [ ] **Could this be caused by misconfiguration?** (Check recent system changes, deployment logs)
- [ ] **Could this be triggered by authorized security testing?** (Check with vulnerability management, penetration testing teams)
- [ ] **Could this be caused by another alert/incident?** (Check for related ongoing investigations)
- [ ] **Could this be alert rule misconfiguration?** (Review alert logic, thresholds, exclusions)

#### Example: Alternative Hypothesis Analysis

**Alert**: "Data Exfiltration - Large File Transfer to External IP"

**Initial Hypothesis**: "Attacker exfiltrating sensitive data"

**Alternative Hypotheses**:

1. **Legitimate Cloud Backup**: User backing up files to personal cloud storage (Dropbox, OneDrive)
   - **Test**: Check destination IP against known cloud provider ranges
   - **Result**: Destination IP is AWS S3 bucket owned by company

2. **Vendor File Transfer**: Sharing files with authorized third-party vendor
   - **Test**: Check with user if they transferred files to vendor
   - **Result**: User confirms sending design files to contracted engineering firm

3. **Software Update**: Application downloading large update
   - **Test**: Check process making connection; verify against known update servers
   - **Result**: Process is web browser, not updater; destination is not known update server

**Conclusion**: Alternative hypothesis #2 confirmed - legitimate vendor file transfer (Benign True Positive)

**Action**: Update alert exclusion to whitelist authorized vendor IP ranges

### Confidence Level Assignment

Assign confidence level to disposition based on evidence quality and quantity.

#### Confidence Levels

**High Confidence**:
- Multiple independent evidence sources corroborate conclusion
- Direct evidence (e.g., malware sample analyzed, user confirmation, packet capture showing exploit)
- No reasonable alternative explanations

**Medium Confidence**:
- Some corroborating evidence, but gaps remain
- Indirect evidence (e.g., indicators of compromise without direct proof)
- Alternative explanations possible but unlikely

**Low Confidence**:
- Limited evidence available
- Ambiguous indicators (could be benign or malicious)
- Multiple plausible alternative explanations

**Unknown / Insufficient Evidence**:
- Insufficient data to make determination
- Critical evidence unavailable (e.g., logs rotated, system offline)
- Requires further investigation or escalation

#### Confidence Level Examples

**High Confidence True Positive**:

```
Alert: Malware Detected
Evidence:
  - Malware sample retrieved and analyzed (hash matches known ransomware family)
  - EDR shows malware encrypting files on disk
  - Network traffic shows C2 communication to known malicious domain
  - User reports files encrypted with ransom note displayed
Confidence: HIGH - Multiple corroborating evidence sources, no alternative explanation
```

**Medium Confidence False Positive**:

```
Alert: Port Scan Detected
Evidence:
  - Source IP is internal (10.1.50.25)
  - Port scan targeted only TCP/80 and TCP/443 (web ports)
  - No follow-up exploitation attempts
  - Asset inventory shows 10.1.50.25 is network monitoring system
  - Unable to confirm with monitoring system owner (out of office)
Confidence: MEDIUM - Likely authorized scan, but unconfirmed
```

**Low Confidence Disposition**:

```
Alert: Unusual Outbound Traffic
Evidence:
  - Large file transfer to external IP (198.51.100.75)
  - Destination IP has no threat intelligence matches
  - Destination IP whois shows generic hosting provider
  - Unable to reach user to confirm transfer (workstation powered off)
  - No other suspicious activity from source system
Confidence: LOW - Ambiguous; could be legitimate or malicious
Action: Flag for follow-up investigation when user returns
```

---

## 4. Disposition Framework

### Disposition Categories

Event disposition classifies the outcome of an investigation into one of three categories:

#### True Positive (TP)

**Definition**: Alert correctly identified genuine malicious or unauthorized activity.

**Criteria**:
- Evidence confirms malicious intent
- Activity violates security policy
- Threat actor identified (external attacker, insider threat, malware)
- Requires security response (containment, eradication, recovery)

**Escalation**: True Positives meeting severity thresholds must be escalated to incident response.

#### False Positive (FP)

**Definition**: Alert incorrectly flagged benign activity as malicious.

**Criteria**:
- Activity is legitimate and authorized
- No security policy violation
- No threat actor involved
- Alert triggered due to detection rule misconfiguration, overly broad signatures, or normal system behavior

**Action**: Update detection rules to prevent recurrence; document in false positive knowledge base.

#### Benign True Positive (BTP)

**Definition**: Alert correctly detected real activity, but activity is authorized and non-malicious.

**Criteria**:
- Activity is real (not false alarm)
- Activity matches alert criteria
- Activity is authorized (security testing, maintenance, administrative tasks)
- No security policy violation

**Action**: Update detection rules to exclude authorized activity; document authorized activity patterns.

**Note**: BTP is distinct from FP because the activity was real and correctly detected, just authorized. FP indicates detection error.

### Disposition Decision Tree

```
┌─────────────────────────────────────┐
│   Alert Triggered                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Does activity match alert criteria? │
└──────┬────────────────────┬─────────┘
       │ NO                 │ YES
       ▼                    ▼
┌──────────────┐    ┌───────────────────────┐
│ FALSE        │    │ Is activity malicious │
│ POSITIVE     │    │ or unauthorized?      │
│              │    └──────┬─────────┬──────┘
│ (Detection   │           │ YES     │ NO
│  error)      │           ▼         ▼
└──────────────┘    ┌──────────┐ ┌──────────────────┐
                    │ TRUE     │ │ Is activity      │
                    │ POSITIVE │ │ authorized?      │
                    │          │ └─────┬──────┬─────┘
                    │ (Genuine │       │ YES  │ NO
                    │  threat) │       ▼      ▼
                    └──────────┘ ┌──────────┐ ┌──────────┐
                                 │ BENIGN   │ │ TRUE     │
                                 │ TRUE     │ │ POSITIVE │
                                 │ POSITIVE │ │          │
                                 │          │ │ (Genuine │
                                 │(Auth'ed) │ │  threat) │
                                 └──────────┘ └──────────┘
```

### Disposition Examples (5+ per Category)

#### True Positive Examples

**TP-1: External Reconnaissance Port Scan**

```
Alert: Port Scan Detected
Source: 198.51.100.50 (external IP)
Target: 10.1.0.0/16 (internal network)
Ports Scanned: TCP 22, 80, 443, 445, 3389, 8080

Evidence:
- Source IP from Russia (non-business country)
- No business relationship with source IP
- Scan covered common exploitation targets (SSH, RDP, SMB, HTTP)
- Threat intel shows source IP linked to prior attacks

Disposition: TRUE POSITIVE
Rationale: External attacker reconnaissance activity
Action: Block source IP at firewall; monitor for follow-up exploitation attempts
```

**TP-2: Unauthorized SSH Lateral Movement**

```
Alert: SSH Connection from Unexpected Source
Source: workstation-042 (10.1.50.42)
Target: db-server-01 (10.1.3.10)

Evidence:
- Workstations should never SSH to database servers (policy violation)
- No authorized maintenance scheduled
- SSH connection followed malware detection on workstation-042
- Connection used service account credentials (not user's primary account)
- Database logs show unauthorized SELECT queries on sensitive tables

Disposition: TRUE POSITIVE
Rationale: Attacker lateral movement after workstation compromise
Action: Isolate workstation-042 and db-server-01; initiate incident response; reset service account credentials
```

**TP-3: Data Exfiltration to Known C2 Domain**

```
Alert: Large Outbound Data Transfer
Source: file-server-01 (10.1.10.15)
Destination: malicious-c2.example.com (198.51.100.75)
Bytes Transferred: 2.5 GB

Evidence:
- Destination domain in threat intelligence feeds (known APT C2 infrastructure)
- Transfer occurred at 3:00 AM (outside business hours)
- Files transferred included customer database backups
- No authorized backup jobs scheduled to external destinations

Disposition: TRUE POSITIVE
Rationale: Confirmed data exfiltration to attacker-controlled infrastructure
Action: Isolate file-server-01; initiate incident response; assess data exposure; notify legal/compliance
```

**TP-4: Malware Hash Match on Endpoint**

```
Alert: Malware Detected - Endpoint Protection
File: C:\Users\jsmith\Downloads\invoice.exe
Hash: 5d41402abc4b2a76b9719d911017c592
Host: workstation-042

Evidence:
- File hash matches known ransomware family (Ryuk)
- EDR shows file attempted to encrypt files in C:\Users\
- Process attempted to delete shadow copies (ransomware behavior)
- Network traffic shows attempted C2 communication
- User confirms did not intentionally download this file

Disposition: TRUE POSITIVE
Rationale: Confirmed ransomware infection
Action: Isolate workstation-042; contain infection; restore from backups; initiate incident response
```

**TP-5: Privilege Escalation via Exploit**

```
Alert: Suspicious Process Execution - Privilege Escalation Detected
Host: web-server-01 (10.1.1.10)
Process: /tmp/exploit.sh (executed by www-data user)
Result: Spawned root shell

Evidence:
- Web application user (www-data) should never spawn root shells
- Process exploit.sh exploited CVE-2024-XXXX kernel vulnerability
- Root shell executed commands to create backdoor user account
- Access logs show SQL injection attack immediately before exploitation

Disposition: TRUE POSITIVE
Rationale: Successful exploitation and privilege escalation
Action: Isolate web-server-01; patch vulnerability; remove backdoor account; initiate incident response
```

**TP-6: Insider Threat - Unauthorized Data Access**

```
Alert: Anomalous Database Query - Large Record Retrieval
User: jdoe (employee - marketing department)
Query: SELECT * FROM customers WHERE 1=1 LIMIT 500000
Database: prod-customer-db

Evidence:
- Marketing users typically query <1000 records per day
- This query retrieved 500,000 customer records (entire database)
- Employee jdoe submitted resignation 2 weeks ago (leaving for competitor)
- Query occurred outside business hours (11:00 PM)
- User copied data to USB drive (EDR endpoint activity)

Disposition: TRUE POSITIVE
Rationale: Insider threat - unauthorized data exfiltration before departure
Action: Disable jdoe account; revoke access; initiate insider threat investigation; notify legal/HR
```

**TP-7: Phishing Campaign Compromise**

```
Alert: Suspicious Email Link Clicked - Credential Harvesting Suspected
User: asmith
Email: "Urgent: Verify Your Account" (sender: payrol@company-payroll.com)
Link: http://company-payrol.com/login (typosquatting domain)

Evidence:
- Email sender domain is typosquatted (payrol vs payroll)
- Link leads to credential harvesting site (fake login page)
- User entered credentials on fake site (network traffic analysis)
- 30 minutes later: Account asmith logged in from Russia (impossible travel)
- Account used to send phishing emails to other employees

Disposition: TRUE POSITIVE
Rationale: Successful phishing attack leading to account compromise
Action: Reset asmith credentials; block attacker IP; quarantine phishing emails; notify affected users
```

#### False Positive Examples

**FP-1: Authorized Vulnerability Scanner Triggering IDS**

```
Alert: Port Scan Detected
Source: 10.1.100.50 (internal IP)
Target: 10.1.0.0/16 (internal network)

Evidence:
- Source IP is authorized vulnerability scanner (Nessus appliance per asset inventory)
- Scan scheduled in change management system (weekly vulnerability assessment)
- Scan occurred during documented maintenance window (Sunday 2:00-6:00 AM)
- No follow-up exploitation attempts
- Security team confirms this is expected activity

Disposition: FALSE POSITIVE
Rationale: Alert correctly detected port scan, but activity is authorized security testing
Action: Update IDS exclusion rules to whitelist vulnerability scanner IP during maintenance windows
```

**FP-2: Legitimate Backup Flagged as Data Exfiltration**

```
Alert: Large Outbound Data Transfer
Source: file-server-01 (10.1.10.15)
Destination: backup-cloud.example.com (AWS S3 bucket)
Bytes Transferred: 500 GB

Evidence:
- Destination is company-owned AWS S3 bucket (verified via AWS console)
- Transfer occurred during scheduled backup window (1:00-5:00 AM)
- Backup job logged in backup software (Veeam)
- Files transferred are database backups (as expected)
- IT confirms this is standard nightly backup

Disposition: FALSE POSITIVE
Rationale: Legitimate backup activity misidentified as exfiltration
Action: Update alert threshold to exclude transfers to known backup destinations
```

**FP-3: Failed Logins During Password Change**

```
Alert: Multiple Failed Login Attempts - Brute Force Suspected
User: jsmith
Source: 10.1.50.42 (workstation-042)
Failed Attempts: 8 over 2 minutes

Evidence:
- User jsmith contacted helpdesk 5 minutes before alert (forgot password)
- Helpdesk reset password at 10:15 AM
- Failed login attempts occurred 10:15-10:17 AM (during password change)
- Successful login at 10:18 AM (after user received new password)
- Source IP is user's assigned workstation
- No other suspicious activity from this account

Disposition: FALSE POSITIVE
Rationale: Legitimate user activity during password reset, not brute force attack
Action: Update alert logic to exclude failed logins within 5 minutes of password reset events
```

**FP-4: Port Scan from Network Monitoring Tool**

```
Alert: Port Scan Detected
Source: 10.1.5.100 (internal IP)
Target: 10.1.0.0/16 (internal network)
Ports: TCP 80, 443, 3306, 5432, 27017

Evidence:
- Source IP is network monitoring system (Nagios server per asset inventory)
- Monitoring system checks service availability every 5 minutes
- Alert triggered when monitoring system performed health checks on all servers
- IT confirms this is expected monitoring behavior
- No exploitation attempts following scans

Disposition: FALSE POSITIVE
Rationale: Routine network monitoring misidentified as reconnaissance
Action: Update IDS exclusion rules to whitelist network monitoring system
```

**FP-5: SSH Connection During VPN Endpoint Change**

```
Alert: SSH Connection from Unexpected Geographic Location
User: rjohnson (remote employee - California)
Source: 198.51.100.20 (IP geolocation: New York)
Target: dev-server-01 (10.1.2.50)

Evidence:
- User rjohnson is remote employee who regularly SSHs to dev servers
- VPN provider changed endpoint routing (some users now route through NYC instead of LAX)
- User confirmed traveling to New York for conference
- SSH session normal duration and activity (typical development work)
- No other suspicious activity from this account

Disposition: FALSE POSITIVE
Rationale: Legitimate remote access with changed VPN endpoint location
Action: Update geolocation baseline for remote users; reduce alert sensitivity for VPN endpoint IPs
```

**FP-6: SQL Keywords in Application Error Logs**

```
Alert: SQL Injection Attempt Detected
Source: 203.0.113.15
Target: web-app-01 (10.1.1.10)
Payload: "SELECT * FROM users WHERE user_id = 12345"

Evidence:
- Alert triggered by IDS detecting SQL keywords in HTTP response
- Investigation shows this is error message from application (not injection attempt)
- Application displays SQL query in error message when database query fails (poor practice, but not attack)
- Source IP is legitimate customer (no other suspicious activity)
- Application logs show database timeout caused error, not malicious input

Disposition: FALSE POSITIVE
Rationale: IDS detected SQL keywords in error message, not actual injection attempt
Action: 1) Update IDS rule to exclude SQL keywords in HTTP responses (not requests)
       2) Recommend to dev team: suppress SQL queries in error messages (security best practice)
```

**FP-7: Batch Job Activity Triggering Anomaly Detection**

```
Alert: Anomalous User Behavior - Unusual File Access Pattern
User: svc-batch (service account)
Activity: Accessed 50,000 files in /data/processing/ directory

Evidence:
- Service account svc-batch is used by nightly ETL batch job
- Batch job runs every night at 2:00 AM (processing customer orders)
- Job normally processes 50,000-100,000 files (data ingestion from partner systems)
- No changes to files outside /data/processing/ directory
- Job completed successfully with no errors

Disposition: FALSE POSITIVE
Rationale: Normal batch job activity misidentified as anomalous behavior
Action: Update anomaly detection baseline to exclude service account batch job activity
```

#### Benign True Positive Examples

**BTP-1: Authorized Vendor Maintenance SSH Connection**

```
Alert: SSH Connection in Control Environment
Source: 198.51.100.30 (external IP - vendor VPN)
Target: scada-hmi-01 (10.2.5.10) - ICS network
User: vendor_support

Evidence:
- Alert correctly detected SSH connection to ICS network (real activity)
- Maintenance scheduled in change management system (vendor firmware upgrade)
- Vendor IP whitelisted for maintenance windows
- OT manager authorized and monitored session
- Firmware upgrade completed successfully; no unauthorized changes

Disposition: BENIGN TRUE POSITIVE
Rationale: Real SSH connection detected (not false alarm), but authorized maintenance activity
Action: Update alert logic to suppress alerts during scheduled maintenance windows for authorized vendor IPs
```

**BTP-2: Authorized Penetration Testing**

```
Alert: Multiple Alerts - Reconnaissance, Exploitation Attempts, Privilege Escalation
Source: 203.0.113.100 (external IP)
Target: Multiple systems (10.1.0.0/16)

Evidence:
- Alerts correctly detected port scans, exploit attempts, credential testing (real attacks)
- Security team contracted external penetration testing firm
- Pentest scheduled for this week (11/05-11/09)
- Source IP matches pentest firm IP range
- Pentest team confirms this is their activity

Disposition: BENIGN TRUE POSITIVE
Rationale: Real attack activity detected (not false alarm), but authorized security testing
Action: Suppress alerts from pentest IP range during engagement window; document findings for remediation
```

**BTP-3: ICS Protocol Anomaly During Firmware Update**

```
Alert: Unusual Modbus Traffic - Unexpected Write Commands
Source: scada-server-01 (10.2.1.10)
Target: plc-line5 (10.2.5.25)
Protocol: Modbus TCP

Evidence:
- Alert correctly detected unusual Modbus write commands (real activity)
- PLC firmware update scheduled in change management system
- Firmware update requires writing configuration to PLC memory (expected behavior)
- OT engineer confirmed firmware update in progress
- Update completed successfully; PLC operating normally

Disposition: BENIGN TRUE POSITIVE
Rationale: Real Modbus anomaly detected (not false alarm), but authorized firmware update
Action: Update alert logic to exclude Modbus activity during scheduled maintenance windows
```

**BTP-4: Multiple Failed Logins - User Forgot Password**

```
Alert: Multiple Failed Login Attempts - Brute Force Suspected
User: mchen
Source: 10.1.50.15 (workstation-015)
Failed Attempts: 12 over 5 minutes

Evidence:
- Alert correctly detected multiple failed logins (real activity, not false alarm)
- User mchen contacted helpdesk (forgot password after returning from vacation)
- Failed logins stopped after password reset
- Source IP is user's assigned workstation (not attacker)
- No other suspicious activity; successful login after password reset

Disposition: BENIGN TRUE POSITIVE
Rationale: Real failed login attempts (not false alarm), but legitimate user behavior (not brute force)
Action: Reduce alert threshold or add context awareness (e.g., suppress if helpdesk ticket opened)
```

**BTP-5: Unusual Network Traffic - Batch Job Processing**

```
Alert: Anomalous Network Traffic - Large Data Transfer Between Internal Systems
Source: app-server-05 (10.1.2.15)
Target: db-server-02 (10.1.3.12)
Bytes Transferred: 1.2 TB

Evidence:
- Alert correctly detected large data transfer (real activity)
- Nightly data warehouse ETL job runs 1:00-5:00 AM
- Transfer consists of database replication (app-server-05 is ETL host)
- Job logs confirm successful completion
- No unauthorized access; standard business process

Disposition: BENIGN TRUE POSITIVE
Rationale: Real large data transfer (not false alarm), but authorized batch job
Action: Update anomaly detection baseline to exclude nightly ETL job traffic
```

### Escalation Criteria

Not all True Positives require escalation to full incident response. Use the following criteria to determine when to escalate:

#### Escalate to Incident Response When:

**Critical Severity Indicators**:
- [ ] **Confirmed malware infection** (especially ransomware, data-stealing malware)
- [ ] **Active data exfiltration** to external attacker-controlled infrastructure
- [ ] **Compromise of critical systems** (domain controllers, financial systems, safety systems in ICS environments)
- [ ] **Lateral movement detected** (attacker moving beyond initial compromise point)
- [ ] **Privilege escalation to admin/root** (attacker gained elevated access)
- [ ] **Multiple systems compromised** (indicating broader campaign)
- [ ] **Insider threat indicators** (malicious employee activity)
- [ ] **Safety impact in ICS/SCADA environments** (potential physical harm or environmental damage)

**High Impact Indicators (NIST Criteria)**:
- [ ] **Functional Impact: High** - Critical services unavailable
- [ ] **Information Impact: Privacy or Proprietary Breach** - Sensitive data compromised
- [ ] **Recoverability: Extended or Not Recoverable** - Recovery requires significant resources or impossible

**Regulatory/Compliance Triggers**:
- [ ] **Personal data breach** (GDPR, CCPA, HIPAA, etc.) - requires notification
- [ ] **Financial data compromise** (PCI-DSS) - payment card data exposed
- [ ] **Critical infrastructure** (NERC CIP, TSA Security Directives) - ICS/OT compromise

#### Do NOT Escalate (Close as TP Without Incident Response) When:

- [ ] **Isolated low-severity event** - Single system, no sensitive data, contained
- [ ] **Early-stage attack blocked** - Reconnaissance or exploitation attempt prevented by controls
- [ ] **No evidence of compromise** - Attack attempted but failed (e.g., blocked exploit, rejected malware)
- [ ] **Routine malware detection** - Common malware blocked by antivirus (no execution/spread)

**Example: Escalate vs. Close**

| Scenario | Disposition | Escalate? | Rationale |
|----------|-------------|-----------|-----------|
| Ransomware encrypting production database | True Positive | **YES** | Critical system compromise, data unavailable, high business impact |
| Port scan blocked by firewall (no follow-up) | True Positive | **NO** | Reconnaissance only, blocked, no compromise |
| Phishing email clicked, credentials entered on fake site | True Positive | **YES** | Account compromise, credential theft, potential for further attacks |
| Malware detected in email attachment (not opened) | True Positive | **NO** | Attack attempt blocked, no execution, no compromise |
| ICS/SCADA HMI compromise | True Positive | **YES** | Safety-critical system, potential physical harm, regulatory implications |
| Single workstation malware (contained by EDR) | True Positive | **MAYBE** | Assess: Was data accessed? Did malware spread? Is workstation isolated? |

#### Escalation Process

When escalating, provide incident response team with:

1. **Incident Summary**: Brief description of what happened
2. **Disposition**: True Positive classification and confidence level
3. **Affected Systems**: List of compromised or at-risk systems
4. **Impact Assessment**: Functional, Information, Recoverability impacts per NIST criteria
5. **Evidence Package**: Logs, PCAPs, endpoint data collected during investigation
6. **Timeline**: Chronological sequence of events
7. **Indicators of Compromise (IoCs)**: IPs, domains, file hashes, TTPs
8. **Recommended Actions**: Suggested containment/eradication steps

**Example Escalation Report**:

```
=== INCIDENT ESCALATION REPORT ===

Incident ID: 2025-1109-002
Alert ID: SIEM-45821
Analyst: John Smith
Escalation Time: 2025-11-09 15:30:00 UTC

SUMMARY:
Confirmed ransomware infection on file-server-01 with active encryption in progress.

DISPOSITION: True Positive (High Confidence)

AFFECTED SYSTEMS:
- file-server-01 (10.1.10.15) - PRIMARY: Ransomware infection, active encryption
- workstation-042 (10.1.50.42) - Initial infection vector (phishing email)

IMPACT ASSESSMENT (NIST SP 800-61):
- Functional Impact: HIGH - File shares unavailable, impacting 200+ users
- Information Impact: Integrity Loss - Files being encrypted/destroyed
- Recoverability: Supplemented - Backups available but require vendor support to restore

ATTACK TIMELINE:
14:16:45 UTC: User on workstation-042 executed phishing attachment "invoice.pdf.exe"
14:17:02 UTC: Malware spawned PowerShell process, downloaded stage 2 payload
14:20:30 UTC: Malware accessed user documents, exfiltrated 500 MB to 198.51.100.75
14:25:00 UTC: Malware propagated to file-server-01 via SMB
14:27:15 UTC: Ransomware encryption began on file-server-01

INDICATORS OF COMPROMISE:
- File hash: 5d41402abc4b2a76b9719d911017c592 (Ryuk ransomware variant)
- C2 Domain: malicious-c2.example.com (198.51.100.75)
- Exfiltration IP: 198.51.100.75
- Ransom note: C:\Users\*\Desktop\DECRYPT_INSTRUCTIONS.txt

EVIDENCE COLLECTED:
- Endpoint telemetry (workstation-042, file-server-01)
- Network PCAP (14:15-14:30 UTC)
- Malware sample (invoice.pdf.exe)
- Ransom note sample

RECOMMENDED ACTIONS:
1. IMMEDIATE: Isolate file-server-01 and workstation-042 from network
2. IMMEDIATE: Block C2 IP 198.51.100.75 at perimeter firewall
3. SHORT-TERM: Scan all systems for malware hash and C2 communication
4. SHORT-TERM: Reset credentials for affected users
5. RECOVERY: Restore file-server-01 from backups (last backup: 01:00 UTC today)

INCIDENT RESPONSE TEAM: Please acknowledge and assume ownership.
```

---

## 5. Common False Positive Patterns

This section documents frequently encountered false positive patterns across ICS, IDS, and SIEM platforms, along with tuning recommendations to reduce alert fatigue while maintaining security visibility.

**Important Note**: Tuning recommendations below are illustrative examples based on common industry practices. Organizations must validate and customize these recommendations for their specific environments, risk tolerance, and regulatory requirements. Always test tuning changes in a non-production environment before deploying to production.

### ICS/SCADA False Positive Patterns

#### FP Pattern 5.1: SSH Connections in Control Environments

**Trigger**: SSH connections to ICS/SCADA systems (HMIs, PLCs, RTUs)

**Common Causes**:
- Scheduled vendor maintenance (firmware updates, configuration changes)
- OT engineer troubleshooting (legitimate administrative access)
- Automated backup scripts (pulling configuration backups via SSH)
- Monitoring systems (SSH-based health checks)

**Why This Triggers Alerts**:
- SSH in ICS environments is less common than IT environments (many legacy systems use older protocols)
- Security best practices discourage remote access to OT networks
- Detection rules flag any SSH to ICS network as suspicious

**Tuning Recommendations**:

1. **Whitelist Authorized Source IPs**:
   ```
   Suppress alert when:
     source_ip IN [vendor_vpn_range, ot_admin_workstations]
     AND destination_ip IN [ics_network_range]
     AND protocol = SSH
   ```

2. **Exclude Scheduled Maintenance Windows**:
   ```
   Suppress alert when:
     time BETWEEN maintenance_window_start AND maintenance_window_end
     AND change_ticket_id EXISTS in CMDB
   ```

3. **Context-Aware Alerting**:
   ```
   Alert only when:
     SSH connection to ICS network
     AND source_ip NOT IN whitelist
     AND NOT during_maintenance_window
     AND no_change_ticket_reference
   ```

**Example Exclusion Rule (SIEM pseudocode)**:

```
Rule: SSH_Connection_ICS_Network_Authorized
Condition:
  event.protocol = "SSH"
  AND event.dest_ip IN "10.2.0.0/16" (ICS network)
  AND (
    event.src_ip IN ["198.51.100.0/24"] (vendor VPN range)
    OR event.src_ip IN ["10.2.1.10", "10.2.1.11"] (OT admin workstations)
    OR (event.time BETWEEN "00:00-04:00 UTC" AND change_ticket.exists = true)
  )
Action: SUPPRESS_ALERT
```

#### FP Pattern 5.2: Modbus Write Commands to PLCs

**Trigger**: Modbus write commands (function code 0x05, 0x06, 0x0F, 0x10) to PLCs

**Common Causes**:
- HMI operator commands (legitimate process control actions)
- SCADA system updating PLC setpoints (automated control)
- Firmware updates (writing configuration to PLC memory)
- Engineering workstation configuration changes (authorized by OT team)

**Why This Triggers Alerts**:
- Write commands can alter PLC logic or setpoints (potential safety impact)
- Unauthorized writes could indicate attacker attempting to manipulate industrial process
- Detection rules flag all writes as suspicious

**Tuning Recommendations**:

1. **Whitelist Expected HMI → PLC Communication**:
   ```
   Suppress alert when:
     source_ip IN [hmi_systems]
     AND dest_ip IN [controlled_plcs]
     AND modbus_function_code IN [0x05, 0x06]
     AND modbus_register IN [expected_setpoint_registers]
   ```

2. **Exclude Known Operational Patterns**:
   ```
   Baseline normal Modbus write frequency and registers
   Alert only when:
     write_frequency > baseline_threshold * 3
     OR modbus_register NOT IN expected_registers
   ```

3. **Geofencing**:
   ```
   Alert when:
     modbus_write_command
     AND source_ip NOT IN [authorized_ot_network_range]
   ```

**Example Exclusion Rule (ICS IDS pseudocode)**:

```
Rule: Modbus_Write_Authorized_HMI
Condition:
  protocol = "Modbus TCP"
  AND function_code IN [0x05, 0x06, 0x0F, 0x10]
  AND src_ip IN ["10.2.1.0/24"] (HMI network)
  AND dest_ip IN ["10.2.5.0/24"] (PLC network)
  AND modbus_register IN [100-200] (known setpoint registers)
Action: SUPPRESS_ALERT
```

#### FP Pattern 5.3: Unusual Protocol Traffic from Legacy Equipment

**Trigger**: Unrecognized or non-standard protocol traffic

**Common Causes**:
- Legacy ICS equipment using proprietary protocols (pre-standardization)
- Vendor-specific protocol variants (e.g., modified Modbus, custom OPC flavors)
- Encapsulated protocols (protocol tunneling over unexpected ports)
- Firmware bugs (malformed packets that appear suspicious)

**Why This Triggers Alerts**:
- IDS signature databases don't recognize proprietary protocols
- Anomaly detection flags deviations from known protocol specifications
- Protocol analysis failures trigger "suspicious traffic" alerts

**Tuning Recommendations**:

1. **Baseline Legacy Protocol Usage**:
   ```
   Document all legacy equipment and their protocol characteristics
   Create custom IDS signatures for proprietary protocols
   Whitelist known legacy device communication patterns
   ```

2. **Device-Specific Exclusions**:
   ```
   Suppress alert when:
     source_ip IN [legacy_device_inventory]
     AND protocol_signature = "unknown"
     AND dest_ip IN [expected_communication_partners]
   ```

**Example Exclusion Rule**:

```
Rule: Legacy_ICS_Device_Proprietary_Protocol
Condition:
  src_ip IN ["10.2.5.50", "10.2.5.51"] (legacy PLCs from 1995)
  AND dest_ip = "10.2.1.5" (legacy HMI)
  AND protocol = "unknown/proprietary"
Action: SUPPRESS_ALERT, ADD_TAG "legacy_ics_protocol"
```

### IDS/IPS False Positive Patterns

#### FP Pattern 5.4: Port Scans from Vulnerability Scanners

**Trigger**: Port scan detection (rapid connection attempts to multiple ports)

**Common Causes**:
- Authorized vulnerability scanners (Nessus, Qualys, OpenVAS)
- Network mapping tools (Nmap for asset inventory)
- Security compliance scanning (PCI-DSS quarterly scans)
- Penetration testing (authorized security assessments)

**Why This Triggers Alerts**:
- Port scans are reconnaissance technique used by attackers
- IDS cannot distinguish authorized scanning from malicious scanning without context

**Tuning Recommendations**:

1. **Whitelist Scanner IP Addresses**:
   ```
   Suppress alert when:
     source_ip IN [vulnerability_scanner_ips]
     AND event_type = "port_scan"
   ```

2. **Maintenance Window Exclusions**:
   ```
   Suppress alert when:
     time BETWEEN "Sunday 02:00-06:00 UTC"
     AND source_ip IN [vulnerability_scanner_ips]
   ```

3. **Scanner Registration System**:
   ```
   Create internal registry of authorized scanning systems
   Automatically suppress alerts from registered scanners
   Require approval workflow to add new scanners to registry
   ```

**Example Exclusion Rule**:

```
Rule: Authorized_Vulnerability_Scanner
Condition:
  alert_type = "Port Scan"
  AND src_ip IN ["10.1.100.50", "10.1.100.51"] (Nessus scanners)
  AND time IN maintenance_windows
Action: SUPPRESS_ALERT, LOG_AS_AUTHORIZED_SCAN
```

#### FP Pattern 5.5: SQL Injection False Positives from Application Errors

**Trigger**: SQL keywords detected in HTTP traffic (SELECT, UNION, INSERT, DROP, etc.)

**Common Causes**:
- Application error messages containing SQL queries (poor practice, but common)
- Legitimate application functionality (search queries, reporting features)
- Educational content (SQL tutorials, documentation websites)
- SQL keywords in user-generated content (forums, code repositories)

**Why This Triggers Alerts**:
- IDS signatures look for SQL keywords in HTTP requests/responses
- Cannot distinguish between malicious injection and benign SQL mentions

**Tuning Recommendations**:

1. **Exclude SQL Keywords in HTTP Responses (Not Requests)**:
   ```
   Modify signature to trigger only on:
     SQL_keywords in HTTP_request (inbound)
   Do NOT trigger on:
     SQL_keywords in HTTP_response (outbound)

   Rationale: Injection attacks send malicious SQL in requests;
              error messages return SQL in responses
   ```

2. **Context-Aware Detection**:
   ```
   Alert only when:
     SQL_keywords in HTTP_request
     AND (
       user_input_contains_union_select
       OR user_input_contains_comment_sequences (-- or /* */)
       OR user_input_contains_stacked_queries (; delimiter)
     )
   ```

3. **Application-Specific Tuning**:
   ```
   For known applications that legitimately use SQL keywords:
     Whitelist specific URL paths (e.g., /reports/*, /admin/db-tools)
   ```

**Example Tuning (Snort/Suricata pseudocode)**:

```
# Original Rule (too broad)
alert http any any -> any any (msg:"SQL Injection"; content:"SELECT"; nocase; sid:1001;)

# Tuned Rule (more specific)
alert http any any -> any any (
  msg:"SQL Injection Attempt";
  content:"SELECT"; nocase;
  pcre:"/union.*select|or.*1=1|;\s*(drop|insert|update)/i";
  flow:to_server;  # Only trigger on requests (not responses)
  sid:1001; rev:2;
)
```

#### FP Pattern 5.6: Large Data Transfers Flagged as Exfiltration

**Trigger**: Large outbound data transfers (> threshold, e.g., 100 MB)

**Common Causes**:
- Database backups to cloud storage (AWS S3, Azure Blob)
- File synchronization (OneDrive, Dropbox, Google Drive)
- Software deployment (pushing large packages to remote sites)
- Video conferencing (Zoom, Teams screen sharing with high resolution)
- Legitimate file sharing with partners (design files, datasets)

**Why This Triggers Alerts**:
- Large data transfers can indicate data exfiltration by attackers
- Volume-based alerting cannot distinguish intent without context

**Tuning Recommendations**:

1. **Whitelist Known Backup Destinations**:
   ```
   Suppress alert when:
     dest_ip IN [company_aws_ip_ranges, backup_vendor_ips]
     AND source_process = "backup_agent.exe"
     AND time IN backup_windows
   ```

2. **Baseline Normal Transfer Volumes**:
   ```
   Calculate per-user/per-system baseline transfer volumes
   Alert only when:
     transfer_volume > (baseline_mean + 3 * baseline_stddev)
   ```

3. **Cloud Service Exclusions**:
   ```
   Suppress alert when:
     dest_domain IN [
       "*.s3.amazonaws.com",
       "*.blob.core.windows.net",
       "*.onedrive.com",
       "*.dropbox.com"
     ]
     AND user_has_authorized_cloud_access = true
   ```

**Example Exclusion Rule**:

```
Rule: Large_Transfer_Authorized_Backup
Condition:
  bytes_out > 100_000_000 (100 MB)
  AND dest_ip IN company_aws_s3_range
  AND src_process = "veeam_backup.exe"
  AND time BETWEEN "01:00-05:00 UTC"
Action: SUPPRESS_ALERT, TAG "authorized_backup"
```

### SIEM False Positive Patterns

#### FP Pattern 5.7: Multiple Failed Logins During Password Changes

**Trigger**: Multiple failed authentication attempts within short time window

**Common Causes**:
- User forgot password and trying to remember it (multiple guesses)
- Password expired and user unaware (failed attempts until reset)
- VPN reconnection after password change (cached old password)
- Password change not synchronized across systems (Active Directory replication lag)

**Why This Triggers Alerts**:
- Failed logins are indicator of brute force attacks
- SIEM threshold-based rules cannot distinguish legitimate failures from attacks

**Tuning Recommendations**:

1. **Correlate with Password Reset Events**:
   ```
   Suppress alert when:
     failed_login_count > threshold
     AND password_reset_event within last_15_minutes
     AND source_ip = user_typical_location
   ```

2. **Increase Threshold with Time Window**:
   ```
   Instead of: 5 failures in 5 minutes → alert
   Use: 10 failures in 5 minutes → alert

   Rationale: Legitimate users rarely exceed 10 attempts;
              automated attacks exceed this quickly
   ```

3. **Context from Helpdesk Tickets**:
   ```
   Suppress alert when:
     helpdesk_ticket_exists for user
     AND ticket_category = "Password Reset"
     AND ticket_time within last_30_minutes
   ```

**Example Correlation Rule (SIEM pseudocode)**:

```
Rule: Failed_Login_After_Password_Reset
Condition:
  event_type = "authentication_failure"
  AND count(failures) > 5 in 5 minutes
  AND EXISTS (
    event_type = "password_reset"
    AND event.user = failures.user
    AND event.time BETWEEN (failures.first_time - 15 minutes) AND failures.last_time
  )
Action: SUPPRESS_ALERT, TAG "password_reset_related"
```

#### FP Pattern 5.8: Anomalous User Behavior from Batch Jobs

**Trigger**: Unusual user activity patterns (file access, login times, data volume)

**Common Causes**:
- Service accounts running batch jobs (ETL, data processing)
- Scheduled tasks executing under user context
- Automation scripts (RPA bots, CI/CD pipelines)
- New employee onboarding (legitimate learning/exploration)

**Why This Triggers Alerts**:
- UEBA (User and Entity Behavior Analytics) systems baseline "normal" behavior
- Batch jobs exhibit non-human patterns (rapid actions, off-hours activity)
- Anomaly detection flags deviations from baseline as suspicious

**Tuning Recommendations**:

1. **Exclude Service Accounts from UEBA**:
   ```
   Do NOT apply UEBA anomaly detection to:
     accounts matching pattern "svc-*"
     OR accounts in "Service Accounts" AD group
   ```

2. **Baseline Batch Job Schedules**:
   ```
   Create separate baseline for scheduled tasks:
     Job: nightly_etl
     Schedule: Daily 02:00-04:00 UTC
     Expected behavior: Access 50,000-100,000 files in /data/

   Alert only when:
     Job runs outside scheduled time
     OR file access count > (baseline_max * 1.5)
   ```

3. **Tag Non-Human Entities**:
   ```
   Maintain inventory of service accounts, bots, automation tools
   Tag events from these entities as "non-human"
   Apply different anomaly thresholds for non-human entities
   ```

**Example Exclusion Rule**:

```
Rule: Service_Account_Batch_Job_Baseline
Condition:
  user MATCHES "svc-.*"
  AND time BETWEEN "00:00-06:00 UTC"
  AND file_access_count > 10000
  AND file_path MATCHES "/data/processing/.*"
Action: SUPPRESS_ANOMALY_ALERT, TAG "scheduled_batch_job"
```

#### FP Pattern 5.9: Privilege Escalation from Authorized Sysadmin sudo Usage

**Trigger**: Privilege escalation detected (user switching to root/admin)

**Common Causes**:
- System administrators using sudo for legitimate maintenance
- Authorized escalation for software installation, configuration changes
- Support personnel troubleshooting issues requiring elevated privileges
- Automated scripts using sudo (with proper authorization)

**Why This Triggers Alerts**:
- Privilege escalation is a key attacker technique (MITRE ATT&CK T1068)
- SIEM rules flag any sudo/runas usage as suspicious without context

**Tuning Recommendations**:

1. **Whitelist Sysadmin Accounts**:
   ```
   Suppress alert when:
     event_type = "privilege_escalation"
     AND user IN [sysadmin_group]
     AND source_ip IN [sysadmin_workstation_range]
   ```

2. **Context-Aware Alerting**:
   ```
   Alert only when:
     privilege_escalation
     AND user NOT IN [authorized_admin_accounts]
     AND (
       escalation_method = "exploit" (CVE-based escalation)
       OR escalated_process IN [suspicious_binaries]
     )
   ```

3. **Time-Based Sensitivity**:
   ```
   Higher sensitivity outside business hours:
     During business hours (8AM-6PM): Suppress admin sudo usage
     Outside business hours: Alert on admin sudo usage (requires change ticket)
   ```

**Example Exclusion Rule**:

```
Rule: Authorized_Sysadmin_Privilege_Escalation
Condition:
  event_type = "privilege_escalation"
  AND user IN AD_group("Domain Admins")
  AND src_ip IN "10.1.100.0/24" (sysadmin workstation network)
  AND time BETWEEN "08:00-18:00 local_time"
  AND escalation_method = "sudo" (not exploit-based)
Action: SUPPRESS_ALERT, LOG_AS_AUTHORIZED_ADMIN_ACTION
```

---

## 6. Cognitive Biases in Event Investigation

Human cognitive biases can significantly impact investigation quality, leading to incorrect dispositions, missed threats, or wasted effort on false leads. This section identifies key biases affecting security analysts and provides debiasing strategies.

### Why Cognitive Biases Matter in Security

**Security investigations are high-stakes decisions under uncertainty**:
- Limited time (SLA pressures, alert fatigue)
- Incomplete information (log gaps, encrypted traffic, attacker evasion)
- High consequences (missed threats vs. false alarms)
- Repetitive tasks (reviewing hundreds of alerts per day)

**These conditions make analysts vulnerable to cognitive biases** - mental shortcuts that can lead to systematic errors in judgment.

**Impact of Bias on Event Investigation**:
- **False Negatives**: Dismissing genuine threats as benign (automation bias, availability bias)
- **False Positives**: Misclassifying benign activity as malicious (confirmation bias)
- **Investigation Inefficiency**: Pursuing wrong hypotheses, ignoring evidence (anchoring bias)
- **Defensive Dispositions**: Over-trusting tools or under-trusting intuition

### Cognitive Bias #1: Automation Bias

#### Definition

**Automation bias** is the propensity to over-rely on automated systems (SIEM alerts, IDS signatures, EDR verdicts) and to discount contradictory information from other sources, including one's own judgment.

**Root Cause**: Humans tend to trust computer-generated information more than human-generated information, especially when under time pressure or cognitive load.

#### Manifestation in Event Investigation

**Scenario 1: Trusting Alert Severity Without Verification**

```
SIEM Alert: "CRITICAL - Malware Detected on CEO Laptop"
Analyst Reaction: "SIEM says critical, must be real malware"
Reality: False positive - antivirus flagged legitimate software as PUP (Potentially Unwanted Program)
Bias: Analyst didn't verify malware classification; trusted SIEM severity blindly
```

**Scenario 2: Dismissing True Positive Because Tool Says "Low Risk"**

```
SIEM Alert: "LOW - Unusual Outbound Connection"
Tool Context: "Low risk score (2/10), likely benign"
Analyst Reaction: "Low risk, probably nothing"
Reality: True positive - attacker using low-and-slow exfiltration technique designed to evade detection
Bias: Analyst dismissed alert based on risk score without investigating evidence
```

**Scenario 3: Ignoring Human Intel Because SIEM Didn't Alert**

```
User Report: "My computer is acting weird, files disappeared"
Analyst Check: [Checks SIEM] "No alerts for this host"
Analyst Reaction: "SIEM shows nothing, probably user error"
Reality: Ransomware wiped logs and evaded detection; user report was early warning
Bias: Analyst trusted absence of SIEM alert over user observation
```

#### Why Automation Bias Happens

- **Cognitive Offloading**: Analysts rely on tools to reduce mental effort (especially when fatigued)
- **Complexity of Tools**: SIEM/EDR systems are complex; analysts may not understand how verdicts are generated
- **Time Pressure**: Faster to accept tool verdict than to investigate independently
- **Organizational Culture**: Metrics reward alert closure speed, not investigation depth

#### Debiasing Strategies

**1. Verify Tool Verdicts with Independent Evidence**

**Practice**: Never accept tool verdict without corroborating evidence.

**Checklist**:
- [ ] What evidence did the tool use to make this determination?
- [ ] Can I independently verify this evidence in raw logs?
- [ ] Are there alternative data sources that support or contradict the tool's verdict?

**Example**:

```
SIEM Alert: "Malware Detected - File Hash Match"
Instead of: "SIEM says malware, disposition = True Positive"
Analyst should:
  1. Look up file hash in VirusTotal, threat intel feeds (independent verification)
  2. Check endpoint logs: Was file executed? Did it spawn processes?
  3. Check network logs: Did endpoint communicate with known C2 domains?
  4. Only after verification: Assign disposition
```

**2. Implement "Challenge the Tool" Protocol**

**Practice**: Actively question tool outputs as part of standard procedure.

**Questions to Ask**:
- "Could this alert be a false positive?"
- "What would evidence of a false positive look like?"
- "What is the tool's false positive rate for this alert type?"
- "Has this tool been wrong before in similar cases?"

**Example Workflow**:

```
Step 1: Review SIEM alert
Step 2: Ask "What could make this a false positive?"
Step 3: Investigate for FP indicators (e.g., scheduled maintenance, authorized activity)
Step 4: If FP indicators found, disposition = False Positive (even if tool says "High Risk")
Step 5: If no FP indicators, investigate for TP evidence
```

**3. Track Tool Accuracy Metrics**

**Practice**: Maintain statistics on tool performance to calibrate trust.

**Metrics to Track**:
- False positive rate per alert type (e.g., "Port Scan alerts: 80% FP rate")
- False negative incidents (threats missed by tools, caught by humans)
- Tool verdict accuracy (% of tool verdicts confirmed by investigation)

**Use Metrics to Adjust Trust**:

```
Alert Type: "Malware Detected by Endpoint Protection"
Historical Accuracy: 95% True Positive
→ High trust appropriate, but still verify critical cases

Alert Type: "Anomalous User Behavior"
Historical Accuracy: 40% True Positive (60% False Positive)
→ Low trust appropriate, requires thorough investigation
```

**4. Peer Review of High-Stakes Decisions**

**Practice**: Require second opinion for critical dispositions before closing.

**When to Use**:
- Critical severity alerts
- Dispositions with low confidence
- Cases where tool verdict conflicts with analyst intuition

**Example**:

```
Analyst A: "SIEM says this is malware, but I'm not convinced (user just installed new software)"
Process: Request peer review from Analyst B
Analyst B: "I checked vendor website, this is legitimate software; FP"
Result: Correct disposition (False Positive) due to peer review
```

### Cognitive Bias #2: Anchoring Bias

#### Definition

**Anchoring bias** is the tendency to rely too heavily on the first piece of information encountered (the "anchor") when making decisions. Subsequent judgments are biased toward the anchor, even if the anchor is irrelevant or incorrect.

#### Manifestation in Event Investigation

**Scenario 1: Locked on Initial Alert Severity**

```
Initial SIEM Alert: "CRITICAL - SQL Injection Detected"
Analyst anchors on: "Critical severity = major threat"
Evidence found: IDS detected SQL keywords in HTTP response (error message), not injection attempt
Analyst reaction: "Still seems serious because alert said critical"
Reality: False positive, but analyst over-investigates and delays disposition due to anchoring on "critical"
```

**Scenario 2: First Hypothesis Dominates Investigation**

```
Initial hypothesis: "Port scan = external attacker reconnaissance"
Evidence found: Source IP is internal (10.1.5.100)
Analyst reaction: "Must be compromised internal host scanning network"
Alternative hypothesis: Source IP is network monitoring system (legitimate)
Reality: Analyst anchored on "attacker" hypothesis, didn't consider "monitoring" hypothesis until later
```

**Scenario 3: Initial Threat Intel Shapes Entire Investigation**

```
Threat intel report: "APT group X targeting our industry with spearphishing"
Alert: "Phishing email detected"
Analyst anchors on: "This must be APT group X"
Evidence found: Email is generic scam (not targeted), sender is known spam operation
Reality: Common phishing, not APT, but analyst wasted time looking for APT indicators due to anchoring
```

#### Why Anchoring Bias Happens

- **First Impression Effect**: Initial information disproportionately influences perception
- **Confirmation Bias Amplification**: Anchor creates hypothesis, then confirmation bias reinforces it
- **Cognitive Ease**: Easier to stick with initial interpretation than to revise it
- **Sunk Cost**: After investing time in initial hypothesis, reluctant to abandon it

#### Debiasing Strategies

**1. Defer Judgment Until Evidence Collected**

**Practice**: Don't form conclusion based on alert alone; wait until evidence reviewed.

**Workflow**:

```
❌ BIASED APPROACH:
  Step 1: Read alert "Critical - Malware Detected"
  Step 2: Form hypothesis: "This is serious malware"
  Step 3: Collect evidence to prove hypothesis
  Step 4: Assign disposition

✅ DEBIASED APPROACH:
  Step 1: Read alert "Critical - Malware Detected"
  Step 2: Suspend judgment: "I don't know yet what this is"
  Step 3: Collect evidence without preconception
  Step 4: Review evidence, then form hypothesis
  Step 5: Test hypothesis against evidence
  Step 6: Assign disposition
```

**2. Explicitly Generate Alternative Hypotheses**

**Practice**: Before finalizing disposition, list at least 2-3 alternative explanations.

**Example**:

```
Alert: "Multiple Failed Login Attempts"

Hypothesis 1 (Initial/Anchor): Brute force attack
Hypothesis 2 (Alternative): User forgot password
Hypothesis 3 (Alternative): Password expired, user unaware
Hypothesis 4 (Alternative): VPN reconnection issue

Evidence Collection:
  - Source IP: User's typical location ✓ (supports H2, H3, H4)
  - Failed attempts: 8 over 3 minutes ✓ (could support H1 or H2)
  - Time: 8:00 AM Monday (business hours) ✓ (supports H2, H3 - user returning from weekend)
  - Helpdesk ticket: User called for password reset ✓ (strongly supports H2)

Conclusion: Hypothesis 2 (User forgot password) best fits evidence
Disposition: False Positive
```

**3. Red Team Your Own Investigation**

**Practice**: After forming initial hypothesis, actively try to disprove it.

**Process**:

```
Step 1: Form initial hypothesis
Step 2: Ask "What evidence would prove this hypothesis WRONG?"
Step 3: Look for that contradictory evidence
Step 4: If found, revise hypothesis
Step 5: Repeat until no contradictory evidence found
```

**Example**:

```
Hypothesis: "This port scan is external attacker reconnaissance"
Contradictory evidence to look for:
  - Source IP is internal ← FOUND: Source is 10.1.5.100 (internal)
  - Source IP is authorized scanner ← FOUND: Asset inventory shows 10.1.5.100 is Nessus scanner
  - Scan occurred during maintenance window ← FOUND: Scan at 2:00 AM Sunday (scheduled)
Conclusion: Initial hypothesis disproven; this is authorized security scanning
Disposition: False Positive
```

**4. Use Structured Analytic Techniques**

**Technique**: Analysis of Competing Hypotheses (ACH)

**Process**:

1. List all plausible hypotheses
2. List all evidence
3. For each hypothesis, evaluate: Does evidence support or refute?
4. Hypothesis with most supporting evidence and least contradictory evidence is most likely

**Example ACH Matrix**:

| Evidence | H1: Brute Force Attack | H2: User Forgot Password | H3: VPN Issue |
|----------|------------------------|--------------------------|---------------|
| Source IP is user's typical location | - (neutral) | + (supports) | + (supports) |
| Failed attempts: 8 over 3 minutes | + (supports) | + (supports) | + (supports) |
| User called helpdesk for password reset | -- (refutes) | ++ (strongly supports) | - (refutes) |
| No other suspicious activity from IP | -- (refutes) | + (supports) | + (supports) |
| Successful login after reset | -- (refutes) | ++ (strongly supports) | + (supports) |
| **Total Score** | -3 | +7 | +2 |

**Conclusion**: Hypothesis 2 (User Forgot Password) has highest score → False Positive

### Cognitive Bias #3: Confirmation Bias

#### Definition

**Confirmation bias** is the tendency to search for, interpret, favor, and recall information that confirms one's preexisting beliefs or hypotheses, while giving disproportionately less attention to information that contradicts them.

#### Manifestation in Event Investigation

**Scenario 1: Seeking Only Supporting Evidence**

```
Hypothesis: "This is a malware infection"
Evidence search:
  - Looked for: Suspicious processes ✓ found
  - Looked for: Network connections to external IPs ✓ found
  - Did NOT look for: Legitimate software that matches description
  - Did NOT look for: User confirmation of software installation
Result: Disposition = True Positive (malware)
Reality: False Positive (legitimate software recently installed by user)
```

**Scenario 2: Interpreting Ambiguous Evidence to Support Hypothesis**

```
Hypothesis: "User account compromised by attacker"
Ambiguous evidence: Login from new location (New York, user typically in California)
Biased interpretation: "Attacker logged in from New York"
Alternative interpretation: "User traveling for business"
Analyst didn't check: Corporate travel calendar, expense reports, user confirmation
Result: Incorrectly escalated as True Positive
```

**Scenario 3: Dismissing Contradictory Evidence**

```
Hypothesis: "External attacker port scanning our network"
Supporting evidence: Port scan detected, source IP unknown
Contradictory evidence: Source IP is 10.1.5.100 (internal network, should be familiar)
Analyst reaction: "IP must be spoofed" (dismisses evidence without verification)
Reality: Source IP is network monitoring system; analyst ignored contradiction
```

#### Why Confirmation Bias Happens

- **Cognitive Efficiency**: Searching for disconfirming evidence requires more mental effort
- **Ego Protection**: Admitting wrong hypothesis feels like failure
- **Premature Closure**: Pressure to close alerts quickly (SLA) encourages accepting first plausible hypothesis
- **Selective Attention**: Once hypothesis formed, attention narrows to hypothesis-relevant information

#### Debiasing Strategies

**1. Actively Seek Disconfirming Evidence**

**Practice**: For every piece of evidence that supports hypothesis, find one that could refute it.

**Evidence Collection Checklist**:
- [ ] What evidence supports my hypothesis?
- [ ] What evidence contradicts my hypothesis?
- [ ] What evidence is ambiguous (could support either)?
- [ ] Have I given equal attention to supporting and contradicting evidence?

**Example**:

```
Hypothesis: "This is data exfiltration by attacker"

Supporting evidence to collect:
  - Large outbound transfer ✓
  - Destination is external IP ✓
  - Transfer occurred outside business hours ✓

Disconfirming evidence to collect:
  - Is destination IP a known backup service? ← CHECK
  - Is this a scheduled backup job? ← CHECK
  - Did user initiate transfer? ← CHECK

Results:
  - Destination IP is AWS S3 bucket owned by company ✓ (disconfirms "attacker")
  - Backup job scheduled for this time ✓ (disconfirms "malicious")
Conclusion: False Positive (authorized backup)
```

**2. Pre-Commitment to Hypothesis Criteria**

**Practice**: Before investigating, define what evidence would prove hypothesis true AND what would prove it false.

**Template**:

```
Hypothesis: [State hypothesis]

Evidence that would PROVE hypothesis TRUE:
  - [Specific evidence 1]
  - [Specific evidence 2]
  - [Specific evidence 3]

Evidence that would PROVE hypothesis FALSE:
  - [Specific contradictory evidence 1]
  - [Specific contradictory evidence 2]
  - [Specific contradictory evidence 3]

Commit: I will accept whichever hypothesis the evidence supports, not which I prefer.
```

**Example**:

```
Hypothesis: "Port scan is external attacker reconnaissance"

Evidence that would PROVE TRUE:
  - Source IP is external (non-RFC1918)
  - Source IP in threat intel feeds (malicious)
  - Scan followed by exploitation attempts

Evidence that would PROVE FALSE:
  - Source IP is internal (RFC1918)
  - Source IP is authorized scanner (asset inventory)
  - Scan occurred during scheduled maintenance window

[After evidence collection]
Found: All three "PROVE FALSE" criteria met
Conclusion: Hypothesis FALSE → Disposition = False Positive
```

**3. Devil's Advocate Review**

**Practice**: Assign someone to argue against your conclusion before finalizing.

**Process**:

```
Analyst A: Completes investigation, drafts disposition
Analyst B (Devil's Advocate): Reviews and argues OPPOSITE disposition
  - "What if this evidence means something different?"
  - "Have you considered this alternative explanation?"
  - "This evidence contradicts your conclusion - how do you explain it?"
Analyst A: Must address all challenges
Final Disposition: Only after devil's advocate satisfied
```

**Example**:

```
Analyst A: "This is malware infection (True Positive)"
Analyst B (Devil's Advocate): "Could this be legitimate software?"
Analyst A: "No, because it's making network connections to unknown IPs"
Analyst B: "Did you check if those IPs are cloud services? Did you contact the user?"
Analyst A: [Checks] "Actually, IPs are AWS CloudFront CDN, and user confirmed installing software"
Revised Disposition: False Positive (legitimate software)
```

**4. Consider the Opposite**

**Practice**: Before finalizing disposition, spend 5 minutes arguing for the opposite conclusion.

**Exercise**:

```
Current disposition: True Positive (attack)
Exercise: "Convince myself this is a False Positive"
  - What benign explanations exist?
  - What evidence supports False Positive?
  - What assumptions am I making that could be wrong?
  - If this were legitimate, what would it look like?

If I can construct a plausible False Positive case → Investigate further before finalizing
If I cannot construct plausible False Positive case → True Positive likely correct
```

### Cognitive Bias #4: Availability Bias

#### Definition

**Availability bias** is the tendency to overestimate the likelihood of events that are more memorable or recent, while underestimating the likelihood of less memorable events. Events that are dramatic, recent, or personally experienced are more "available" in memory.

#### Manifestation in Event Investigation

**Scenario 1: Overweighting Recent Incidents**

```
Recent incident: Ransomware attack 2 weeks ago (major event, company-wide impact)
Current alert: "Unusual file access pattern"
Analyst reaction: "This could be ransomware again!" (heightened sensitivity)
Evidence: User copying files to USB for legitimate work presentation
Reality: False Positive, but analyst over-investigates due to recent ransomware memory
```

**Scenario 2: Ignoring Base Rates**

```
Recent news: Major supply chain attack (SolarWinds) widely publicized
Current alert: "Software update from vendor"
Analyst reaction: "Could be supply chain compromise!" (overestimates likelihood)
Base rate: Supply chain attacks are extremely rare (<0.01% of software updates)
Reality: Legitimate update, but analyst spends excessive time verifying due to availability of SolarWinds news
```

**Scenario 3: Personal Experience Bias**

```
Analyst's experience: Previously missed phishing attack that became major incident (personal failure, memorable)
Current alert: "Phishing email detected"
Analyst reaction: "I can't miss this; better escalate" (over-cautious due to past mistake)
Evidence: Obvious spam email (not targeted), blocked by email gateway
Reality: No user impact, but analyst escalates unnecessarily due to available memory of past miss
```

#### Why Availability Bias Happens

- **Recency Effect**: Recent events are more accessible in memory
- **Vividness Effect**: Dramatic events (ransomware, breaches) more memorable than routine events (false positives)
- **Media Amplification**: High-profile attacks receive extensive coverage, skewing perception of frequency
- **Personal Relevance**: Events we experienced directly are more available than statistics

#### Debiasing Strategies

**1. Use Base Rates and Historical Data**

**Practice**: Before assessing likelihood, check actual frequency in your environment.

**Process**:

```
Step 1: Identify event type (e.g., "possible ransomware")
Step 2: Check historical data: How many ransomware incidents in last year?
Step 3: Calculate base rate: (incidents / total alerts) = probability
Step 4: Use base rate to calibrate assessment

Example:
  "Possible ransomware" alerts: 200 per month
  Actual ransomware incidents: 1 per year
  Base rate: 1/2400 = 0.04% (extremely rare)
  Conclusion: Most "possible ransomware" alerts are false positives
  Implication: Require strong evidence before escalating as ransomware
```

**2. Maintain a "False Positive Diary"**

**Practice**: Document common false positive patterns to make them more "available" in memory.

**Purpose**: Counter the vividness of true positive incidents by making false positives equally memorable.

**Format**:

```
=== FALSE POSITIVE DIARY ===

Date: 2025-11-09
Alert: "Malware Detected"
Initial Suspicion: "Could be ransomware!"
Actual Cause: User installed legitimate software flagged as PUP
Disposition: False Positive
Lesson: Always verify software legitimacy before escalating

Date: 2025-11-10
Alert: "Data Exfiltration"
Initial Suspicion: "Attacker stealing data!"
Actual Cause: Cloud backup to AWS S3
Disposition: False Positive
Lesson: Check if destination is company-owned cloud storage

[Analyst reviews diary before investigating similar alerts]
```

**3. Separate Threat Awareness from Threat Assessment**

**Practice**: Distinguish between "this threat exists" (awareness) and "this is the threat" (assessment).

**Process**:

```
Step 1: Acknowledge threat awareness
  "Yes, ransomware is a real threat (I know because of recent incident)"

Step 2: Assess specific case based on evidence
  "But does THIS alert indicate ransomware?"
  - Check evidence (file encryption, ransom note, known malware hash)
  - Check base rate (how often are these alerts actually ransomware?)
  - Avoid letting recent incident influence this specific assessment

Step 3: Disposition based on evidence, not recency
```

**Example**:

```
Thought Process:

❌ BIASED: "We had ransomware 2 weeks ago, and this file behavior looks similar → True Positive"

✅ DEBIASED:
  - "Yes, ransomware is a concern (recent incident makes me aware)"
  - "But let me assess THIS case objectively:"
      - Is there a ransom note? NO
      - Are files encrypted? NO (just copied, not encrypted)
      - Is this behavior consistent with user's role? YES (data analyst, regularly works with large files)
  - "Conclusion: False Positive (legitimate user activity)"
```

**4. Normalize False Positives**

**Practice**: Remind yourself that false positives are common and normal.

**Cognitive Reframe**:

```
❌ BIASED THINKING: "This could be the next big incident!"

✅ DEBIASED THINKING: "Most alerts are false positives (per base rate). This is probably another FP."

Implication: Start with null hypothesis "This is a false positive" and require evidence to overcome it.
```

**Statistical Reminder** (post visibly in SOC):

```
=== ALERT STATISTICS (Last 12 Months) ===
Total Alerts: 120,000
True Positives: 600 (0.5%)
False Positives: 119,400 (99.5%)

CONCLUSION: If you receive an alert, it is 99.5% likely to be a false positive.
Extraordinary claims (True Positive) require extraordinary evidence.
```

---

## 7. ICS/SCADA-Specific Considerations

Industrial Control Systems (ICS) and Supervisory Control and Data Acquisition (SCADA) environments have unique characteristics that require specialized investigation approaches. This section addresses OT-specific considerations for event investigation.

### Key Differences Between IT and OT Environments

| Characteristic | IT Environment | OT/ICS Environment |
|----------------|----------------|---------------------|
| **Primary Objective** | Confidentiality, Integrity, Availability (CIA) | **Availability, Integrity, Confidentiality** (AIC) - reversed priority |
| **Downtime Tolerance** | Minutes to hours acceptable | **Seconds to minutes critical** (safety/production impact) |
| **Patch Cadence** | Monthly (Patch Tuesday) | **Quarterly to annual** (requires outage planning) |
| **System Lifespan** | 3-5 years | **15-30 years** (legacy systems common) |
| **Logging Capabilities** | Extensive (syslog, EDR, SIEM) | **Limited or absent** (legacy protocols, resource constraints) |
| **Network Segmentation** | Moderate (VLANs, firewalls) | **Critical requirement** (Purdue Model, air gaps) |
| **Change Management** | Agile, frequent updates | **Rigid, slow** (regulatory approvals, safety testing) |
| **Vendor Dependency** | Moderate | **High** (proprietary systems, vendor-only maintenance) |

**Implication for Event Investigation**: ICS investigations must prioritize operational continuity and safety over forensic depth. Isolating a compromised ICS system may not be acceptable if it causes production outage or safety hazard.

### Safety Implications: Availability Over Confidentiality

#### The Safety Imperative

**In ICS/SCADA environments, availability is paramount** because these systems control physical processes:

- **Power grids**: Outage causes widespread blackouts
- **Water treatment**: Failure affects public health
- **Manufacturing**: Downtime costs millions per hour
- **Chemical plants**: Disruption can cause explosions, toxic releases
- **Transportation**: Failures endanger human life (trains, aircraft, traffic systems)

**Investigation Principle**: Never take actions that compromise system availability without explicit authorization from OT operations leadership.

#### Investigation Constraints Due to Safety

**Prohibited Actions Without Authorization**:
- [ ] Isolating ICS systems from network (may disrupt control loops)
- [ ] Rebooting HMIs, PLCs, or SCADA servers (may cause unsafe states)
- [ ] Capturing full network traffic (can overwhelm limited bandwidth)
- [ ] Running vulnerability scans (known to crash legacy ICS devices)
- [ ] Installing EDR agents (unsupported on ICS endpoints, may cause instability)

**Required Actions for ICS Investigations**:
- [ ] Coordinate with OT operations before ANY investigative action
- [ ] Understand physical process and safety implications
- [ ] Have rollback plan if investigation causes disruption
- [ ] Prioritize read-only, passive investigation techniques
- [ ] Schedule intrusive actions during planned maintenance windows

#### Example: Balancing Investigation and Safety

```
Scenario: Suspected malware on HMI controlling chemical reactor

IT Approach (Standard):
  1. Isolate HMI from network immediately
  2. Capture memory dump
  3. Reboot to clean state
  4. Restore from backup
  Duration: 30-60 minutes

OT Approach (Safety-First):
  1. Consult with process engineer: Can we afford HMI downtime?
     - Answer: NO - Reactor requires continuous monitoring; loss of HMI visibility is unsafe
  2. Implement alternative controls:
     - Switch to backup HMI (if available)
     - Implement manual monitoring (operator with radio at control panel)
  3. During planned reactor shutdown (next scheduled maintenance window in 2 weeks):
     - Then investigate HMI offline
     - Memory dump, malware analysis, system rebuild
  4. Interim mitigations:
     - Network segmentation: Block HMI internet access
     - Monitoring: Increase logging on network perimeter
     - Behavioral analysis: Monitor HMI for suspicious process behavior

Result: Safety maintained, investigation deferred to safe opportunity
```

### Legacy System Limitations

#### Lack of Logging

**Challenge**: Many ICS devices have no logging capabilities or minimal logging.

**Examples**:
- Older PLCs (pre-2000): No event logs, no authentication logs
- Legacy HMI software (Windows XP embedded): Minimal application logs
- Serial-based devices (Modbus RTU): No network logging (serial communication)

**Investigation Impact**:
- **Limited forensic evidence**: Can't determine "what happened" from device logs
- **Dependency on network logs**: Must rely on network-level monitoring (IDS, NetFlow)
- **Reduced visibility**: Blind spots in attack timeline reconstruction

**Mitigation Strategies**:

1. **Network-Based Monitoring** (passive, doesn't touch ICS devices):
   ```
   Deploy network TAPs or SPAN ports to capture ICS traffic
   Use ICS-specific IDS (Nozomi, Claroty, Dragos) to analyze protocols
   Advantage: No impact on ICS device stability; captures all network activity
   ```

2. **Baseline Behavioral Analysis**:
   ```
   Create baseline of normal ICS device behavior:
     - Network traffic patterns (Modbus polling every 5 seconds)
     - Process variable ranges (temperature 50-100°C)
     - Communication partners (HMI always talks to PLC-1, PLC-2, PLC-3)
   Alert on deviations from baseline (even without logs)
   ```

3. **Physical Security Correlation**:
   ```
   Correlate cyber events with physical security logs:
     - Badge access to control room
     - Surveillance camera footage
     - Maintenance logs (who touched devices, when)
   Useful when cyber logs absent
   ```

#### Limited Visibility

**Challenge**: Encrypted protocols, proprietary protocols, air-gapped networks limit visibility.

**Examples**:
- **Encrypted OPC UA**: Can't inspect application-layer data without decryption keys
- **Proprietary protocols**: Vendor-specific protocols not parseable by standard tools
- **Air-gapped networks**: No connection to corporate SIEM; logs don't reach analysts

**Investigation Strategies**:

1. **Leverage Vendor Partnerships**:
   ```
   Contact ICS vendor for:
     - Protocol specifications (to build custom parsers)
     - Diagnostic tools (vendor-provided log extraction tools)
     - Incident response support (vendor engineers for investigation)
   ```

2. **Jump Box Investigation**:
   ```
   For air-gapped networks:
     - Use dedicated "jump box" workstation in OT environment
     - Manually extract logs to USB (follow strict USB security policies)
     - Transfer logs to IT environment for SIEM ingestion
   ```

3. **OT-Specific Monitoring Tools**:
   ```
   Deploy OT-native visibility solutions:
     - Nozomi Networks: ICS protocol DPI, asset discovery, anomaly detection
     - Claroty: OT asset management, vulnerability assessment
     - Dragos Platform: ICS threat detection, industrial threat intelligence
   ```

### Operational Technology Protocols

ICS/SCADA environments use specialized industrial protocols. Understanding these protocols is essential for investigating OT events.

#### Common ICS/SCADA Protocols

**Modbus** (Modicon Communication Bus)
- **Use Case**: PLC communication, SCADA data acquisition
- **Transport**: Modbus TCP (Ethernet), Modbus RTU (serial RS-485)
- **Security**: No authentication, no encryption (legacy design)
- **Investigation Considerations**:
  - Modbus write commands (function codes 0x05, 0x06, 0x0F, 0x10) can alter PLC logic
  - Monitor for unexpected write commands or writes to unusual registers
  - Baseline normal Modbus traffic patterns (polling intervals, register ranges)

**DNP3** (Distributed Network Protocol)
- **Use Case**: Electric power systems, water/wastewater utilities
- **Transport**: TCP/IP or serial
- **Security**: DNP3 Secure Authentication (DNP3-SA) available but rarely deployed
- **Investigation Considerations**:
  - DNP3 commands can trip breakers, open valves (direct physical impact)
  - Monitor for unauthorized DNP3 control commands (OPERATE, DIRECT OPERATE)
  - Correlate DNP3 events with SCADA system operator actions (legitimate vs. attack)

**OPC** (OLE for Process Control)
- **Use Case**: Data exchange between HMI/SCADA and PLCs/historians
- **Variants**: OPC DA (Data Access), OPC UA (Unified Architecture - modern, secure)
- **Transport**: OPC DA uses DCOM (Windows); OPC UA uses TCP with TLS
- **Investigation Considerations**:
  - OPC DA is vulnerable to credential theft (DCOM authentication)
  - OPC UA is more secure (certificate-based authentication, encryption)
  - Monitor for abnormal OPC connections (unexpected clients, unusual read/write patterns)

**IEC 61850** (Substation Automation)
- **Use Case**: Electric substation automation, protection relays
- **Transport**: Ethernet-based (GOOSE, MMS protocols)
- **Security**: Limited (designed for isolated substations, now networked)
- **Investigation Considerations**:
  - GOOSE messages are multicast, unauthenticated (replay attack risk)
  - Monitor for rogue GOOSE publishers (attackers injecting false status messages)
  - IEC 62351 provides security extensions (rarely deployed)

#### ICS Protocol Investigation Techniques

**1. Protocol Baseline Creation**

**Purpose**: Establish "normal" protocol behavior to detect anomalies.

**Process**:

```
Step 1: Capture 1-2 weeks of ICS network traffic (passive TAP)
Step 2: Analyze protocol patterns:
  - Communication pairs (which devices talk to each other)
  - Polling intervals (Modbus: every 5 seconds; DNP3: every 10 seconds)
  - Command types (read-only vs. write commands)
  - Register/point ranges (which data points are accessed)
Step 3: Create baseline profile for each device pair
Step 4: Configure ICS IDS to alert on deviations from baseline
```

**Example Baseline**:

```
Device Pair: HMI-01 (10.2.1.10) ↔ PLC-05 (10.2.5.25)
Protocol: Modbus TCP
Baseline:
  - Polling Interval: 5 seconds (±0.5 seconds)
  - Function Codes: 0x03 (Read Holding Registers) - 98% of traffic
                    0x06 (Write Single Register) - 2% of traffic
  - Register Range: 100-200 (setpoints), 500-600 (sensor readings)
  - Traffic Volume: 200-300 packets/minute
  - Time of Day: 24/7 (continuous operation)

Anomaly Alerts:
  - Function code other than 0x03 or 0x06 (e.g., 0x10 Write Multiple Registers)
  - Access to registers outside 100-200, 500-600 range
  - Polling interval > 10 seconds (communication disruption)
  - Traffic from unauthorized source IP
```

**2. Threat Hunting in ICS Protocols**

**Indicators of Malicious ICS Activity**:

- **Unauthorized Write Commands**:
  ```
  Modbus: Unexpected writes to PLC registers (especially control logic areas)
  DNP3: Unauthorized OPERATE commands (tripping breakers, opening valves)
  OPC: Writes to process setpoints without corresponding operator action
  ```

- **Reconnaissance Activity**:
  ```
  Modbus: Read commands scanning all register ranges (enumeration)
  DNP3: Integrity polls from unexpected sources
  OPC: OPC server enumeration from non-HMI sources
  ```

- **Man-in-the-Middle**:
  ```
  ARP spoofing in ICS network (attacker intercepting HMI-PLC communication)
  Duplicate IP addresses (attacker impersonating legitimate device)
  Unexpected MAC addresses for known IP addresses
  ```

- **Replay Attacks**:
  ```
  IEC 61850 GOOSE: Replayed "breaker open" command
  Modbus: Replayed write command with old timestamp
  Detection: Sequence number analysis, timing analysis
  ```

**3. Leveraging MITRE ATT&CK for ICS**

[MITRE ATT&CK for ICS][2] documents tactics and techniques used in ICS attacks.

**Key ICS-Specific Techniques**:

| Technique ID | Name | Description | Investigation Focus |
|--------------|------|-------------|---------------------|
| **T0855** | Unauthorized Command Message | Attacker sends unauthorized control commands to ICS devices | Monitor for unexpected Modbus writes, DNP3 OPERATE commands from non-HMI sources |
| **T0836** | Modify Parameter | Attacker changes process parameters (setpoints, thresholds) | Baseline setpoint values; alert on changes without operator action |
| **T0801** | Monitor Process State | Attacker reads sensor data to understand process before attack | Unusual read activity from non-SCADA sources |
| **T0831** | Manipulation of Control | Attacker manipulates physical process (e.g., centrifuge speed in Stuxnet) | Correlate abnormal process behavior with ICS network events |
| **T0816** | Device Restart/Shutdown | Attacker reboots PLCs or HMIs to disrupt operations | Monitor for unexpected device resets, reboots |

**Example Investigation Using ATT&CK for ICS**:

```
Alert: "Unusual Modbus Write Command"
MITRE ATT&CK Mapping:
  - Technique: T0855 (Unauthorized Command Message)
  - Tactic: Impair Process Control

Investigation Steps (per ATT&CK):
  1. Identify command source: Where did write command originate?
     - Expected: HMI (10.2.1.10)
     - Actual: Unknown workstation (10.2.9.50) ← SUSPICIOUS

  2. Analyze command content: What was written?
     - Register: 150 (motor speed setpoint)
     - Value: 3600 RPM (normal: 1800 RPM) ← DANGEROUS

  3. Check operator logs: Did operator authorize this change?
     - No operator action logged ← UNAUTHORIZED

  4. Assess impact: What would this command do?
     - Double motor speed → mechanical stress, potential equipment damage

Disposition: TRUE POSITIVE - Unauthorized command message (T0855)
Action: Block source IP 10.2.9.50; investigate workstation; revert PLC setpoint to 1800 RPM
```

### Maintenance Window Considerations

#### Why Maintenance Windows Matter

**ICS systems require scheduled downtime for maintenance:**
- Firmware updates (quarterly or annual)
- Hardware replacement (aging equipment)
- Calibration (sensor accuracy checks)
- Safety testing (regulatory compliance)

**During maintenance windows:**
- Unusual activity is EXPECTED (firmware uploads, configuration changes, testing)
- Normal activity may be ABSENT (systems offline, no production traffic)

**Investigation Impact**: Events during maintenance windows are likely **Benign True Positives** (real activity, but authorized).

#### Maintenance Window False Positives

**Common Alerts During Maintenance**:

1. **SSH Connections to ICS Devices**:
   - Cause: Vendor engineer applying firmware update
   - Disposition: Benign True Positive (authorized maintenance)

2. **Unusual Protocol Commands**:
   - Cause: Testing PLC logic after configuration change
   - Disposition: Benign True Positive (testing activity)

3. **Device Reboots**:
   - Cause: Required after firmware installation
   - Disposition: Benign True Positive (expected reboot)

4. **File Transfers to ICS Devices**:
   - Cause: Uploading new HMI application
   - Disposition: Benign True Positive (authorized update)

#### Investigation Strategies for Maintenance Windows

**1. Correlate with Change Management System**

**Process**:

```
Alert: "SSH Connection to PLC-05"
Step 1: Check change management system (ServiceNow, etc.)
Step 2: Search for open change tickets for PLC-05
Step 3: If change ticket exists:
  - Verify change window includes alert timestamp
  - Verify change description matches activity (e.g., "firmware update" explains SSH)
  - Verify source IP matches authorized vendor IP
Step 4: If all verified → Disposition: Benign True Positive
Step 5: If no change ticket → Investigate as potential True Positive
```

**2. Create Maintenance Window Suppression Rules**

**SIEM Configuration**:

```
Rule: Suppress_Alerts_During_Maintenance_Window
Condition:
  alert_time BETWEEN maintenance_window_start AND maintenance_window_end
  AND affected_device IN maintenance_ticket.device_list
  AND change_ticket.status = "In Progress"
Action: SUPPRESS_ALERT, TAG "scheduled_maintenance"

Note: Only suppress EXPECTED alert types (e.g., SSH, reboots, config changes)
       Do NOT suppress UNEXPECTED alerts (e.g., malware detection, data exfiltration)
```

**3. Post-Maintenance Verification**

**After maintenance window closes, verify:**

- [ ] All systems returned to normal operation
- [ ] No unexpected configuration changes beyond change ticket scope
- [ ] No new user accounts or backdoors created
- [ ] No unusual network connections established

**Example Post-Maintenance Checklist**:

```
Maintenance Ticket: PLC-05 Firmware Update (2025-11-09 02:00-04:00 UTC)

Post-Maintenance Verification:
☑ PLC-05 online and responding to HMI polls
☑ Firmware version matches expected (v3.2.1)
☑ PLC configuration hash matches pre-maintenance backup (no unexpected changes)
☑ No new user accounts created on PLC
☑ No new network connections from PLC (besides expected HMI connections)
☑ Vendor engineer VPN session terminated (no persistent access)
☑ Change ticket closed in ServiceNow

Result: Maintenance successful, no security concerns
```

### Vendor Coordination Requirements

#### Why Vendor Coordination is Critical

**ICS vendors have specialized knowledge:**
- Proprietary protocols and system architecture
- Diagnostic tools not available to customers
- Incident response experience with their products
- Direct access to engineering teams for urgent issues

**When to Involve Vendors**:
- [ ] Suspected compromise of ICS device (PLC, HMI, RTU)
- [ ] Malware targeting vendor's products
- [ ] Unusual behavior requiring vendor diagnostic tools
- [ ] Firmware integrity verification needed
- [ ] Incident requiring vendor-specific remediation (e.g., PLC logic restoration)

#### Vendor Coordination Process

**Step 1: Identify Vendor Contact**

```
Preparation (before incident):
  - Maintain vendor contact list:
      Vendor: Siemens
      Product: S7-1500 PLCs
      Support Contact: support@siemens.com
      Emergency Hotline: +1-800-XXX-XXXX
      Account Manager: John Doe (john.doe@siemens.com)
      ICS-CERT Coordinator: Jane Smith (jane.smith@siemens.com)
  - Establish support contracts with SLAs (critical for 24/7 response)
```

**Step 2: Initial Vendor Notification**

```
When to Notify:
  - Immediately upon confirming ICS device compromise
  - During investigation if vendor expertise needed

What to Include:
  - Incident summary (what happened, which devices affected)
  - Product details (model, firmware version, serial number)
  - Symptoms (error messages, abnormal behavior)
  - Evidence collected (logs, network captures - if shareable)
  - Urgency level (safety impact, production impact)
```

**Step 3: Coordinated Investigation**

```
Vendor may provide:
  - Remote diagnostic access (via secure VPN)
  - Custom diagnostic tools (vendor-specific log extraction)
  - Firmware integrity verification tools
  - Malware analysis (if targeting their products)
  - Incident response best practices (specific to their products)

Customer responsibilities:
  - Provide network access for vendor (with security controls)
  - Share evidence (within legal/contractual constraints)
  - Coordinate maintenance windows for remediation
  - Document vendor findings for internal records
```

**Step 4: Information Sharing Considerations**

**What to Share with Vendor**:
- Technical details of compromise (IOCs, TTPs)
- Impact on vendor's products (vulnerabilities exploited)
- Remediation effectiveness (did vendor recommendations work?)

**What NOT to Share**:
- Customer data (PII, business secrets) unless necessary
- Details of other vendors' products (competitive concerns)
- Sensitive operational details (if not required for investigation)

**Legal Considerations**:
- Non-disclosure agreements (protect customer confidentiality)
- Liability clauses (clarify responsibility for vendor-assisted investigation)
- Regulatory requirements (NERC CIP, NIS Directive) may mandate vendor reporting

#### Example Vendor Coordination

```
Scenario: Suspected Malware on Siemens SIMATIC HMI

Step 1: Initial Detection
  - Alert: "Unusual process execution on HMI-01"
  - Device: Siemens SIMATIC HMI Panel (Model: TP1200 Comfort)
  - Investigation: Process "update.exe" not recognized, making network connections

Step 2: Vendor Notification
  - Contact: Siemens Industrial Security Incident Response Team
  - Email: productcert@siemens.com
  - Subject: "Suspected Malware on SIMATIC HMI - Urgent Assistance Required"
  - Details: Device model, firmware version, process name, network connections

Step 3: Vendor Response
  - Siemens provides:
      • TIA Portal diagnostic tool to extract HMI application and logs
      • Firmware integrity checker (compares installed firmware to official hash)
      • Analysis: "update.exe" is not Siemens software; likely malware
      • Recommendation: Restore HMI from clean backup, update firmware to latest (patches vulnerability)

Step 4: Remediation with Vendor Support
  - Coordinate maintenance window (4-hour downtime)
  - Siemens engineer joins via WebEx during remediation
  - Steps:
      1. Backup current HMI configuration (for forensics)
      2. Wipe HMI and reinstall firmware (vendor provides clean image)
      3. Restore HMI application from known-good backup
      4. Verify integrity with vendor tool
  - Result: HMI restored, malware removed, vulnerability patched

Step 5: Post-Incident Follow-Up
  - Siemens issues security advisory (if vulnerability is 0-day)
  - Customer updates other Siemens HMIs with patch
  - Share IOCs with industry ISACs (ICS-CERT, E-ISAC)
```

---

## 8. Investigation Workflow Checklist

This checklist provides step-by-step guidance for conducting event investigations. Use this as a reference during alert triage and analysis.

### Phase 1: Alert Triage

- [ ] **Read alert details**: Severity, source, destination, timestamp, alert rule name
- [ ] **Check SIEM context**: Related alerts, historical activity from source/destination
- [ ] **Verify alert legitimacy**: Is this a known false positive pattern? (reference Section 5)
- [ ] **Prioritize**: Assign priority using NIST criteria (Functional/Information/Recoverability impact)
- [ ] **Initial hypothesis**: Form preliminary hypothesis (defer judgment until evidence collected)

### Phase 2: Evidence Collection

- [ ] **Collect log data**: System logs, application logs, security logs (reference Section 3: Evidence Collection)
- [ ] **Collect network data**: Packet captures, NetFlow, DNS queries, proxy logs
- [ ] **Collect endpoint data**: EDR telemetry, process execution, file modifications, memory dumps
- [ ] **Document collection**: Record what was collected, when, from where, by whom (chain of custody)
- [ ] **Calculate hashes**: Generate MD5/SHA-256 for critical evidence (preserve integrity)

### Phase 3: Evidence Analysis

- [ ] **Event correlation**: Link related events using time-based, pattern-based, or topological correlation
- [ ] **Timeline reconstruction**: Create chronological sequence of events
- [ ] **Hypothesis testing**: Test initial hypothesis against evidence; generate alternative hypotheses
- [ ] **Threat intelligence lookup**: Check IOCs (IPs, domains, file hashes) against threat intel feeds
- [ ] **MITRE ATT&CK mapping**: Map observed behaviors to ATT&CK techniques (IT: Enterprise; OT: ICS)

### Phase 4: Cognitive Bias Check

- [ ] **Automation bias check**: Am I over-relying on tool verdicts without verification?
- [ ] **Anchoring bias check**: Am I locked on initial hypothesis? Have I considered alternatives?
- [ ] **Confirmation bias check**: Have I sought disconfirming evidence, or only supporting evidence?
- [ ] **Availability bias check**: Am I overweighting recent incidents? What is the base rate?

### Phase 5: Disposition Determination

- [ ] **Apply disposition framework**: Classify as True Positive, False Positive, or Benign True Positive (reference Section 4)
- [ ] **Assign confidence level**: High, Medium, Low, or Insufficient Evidence
- [ ] **Use decision tree**: Follow disposition decision tree (Section 4)
- [ ] **Consider alternative hypotheses**: Can I construct plausible alternative explanation?
- [ ] **Check escalation criteria**: Does this require escalation to incident response? (reference Section 4)

### Phase 6: Documentation and Closure

- [ ] **Document findings**: Summary, evidence, analysis, disposition, confidence level
- [ ] **Update case notes**: Investigation timeline, hypotheses tested, reasoning for disposition
- [ ] **Escalate if True Positive**: Follow escalation process (Section 4) if criteria met
- [ ] **Tuning recommendation**: If False Positive, document tuning recommendation to prevent recurrence
- [ ] **Knowledge sharing**: Add to false positive diary or knowledge base for team learning
- [ ] **Close alert**: Update SIEM/ticketing system with disposition and closure notes

### Phase 7: Post-Investigation (If False Positive)

- [ ] **Root cause analysis**: Why did alert trigger? (detection rule too broad, threshold too low?)
- [ ] **Tuning recommendation**: How can we prevent this FP? (whitelist, threshold adjustment, exclusion rule)
- [ ] **Implement tuning**: Update SIEM/IDS rules (test in non-production first)
- [ ] **Verify tuning**: Monitor for 1-2 weeks to ensure FP eliminated without losing TP detection

### ICS-Specific Checklist Additions

If investigating ICS/SCADA event, also complete:

- [ ] **Safety impact assessment**: Could this event or investigation action cause safety hazard?
- [ ] **OT coordination**: Notify OT operations before taking any action on ICS systems
- [ ] **Maintenance window check**: Is this event during scheduled maintenance window? Correlate with change management
- [ ] **Vendor consultation**: Does this require vendor coordination? (reference Section 7)
- [ ] **Physical process correlation**: Does cyber event correlate with abnormal physical process behavior?
- [ ] **MITRE ATT&CK for ICS**: Map to ICS-specific tactics/techniques (reference Section 7)

---

## 9. References

### NIST Publications

[1]: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf "NIST SP 800-61 Rev 2: Computer Security Incident Handling Guide - Access Date: 2025-11-09"

**NIST Special Publication 800-61 Revision 2**: Computer Security Incident Handling Guide
Paul Cichonski, Tom Millar, Tim Grance, Karen Scarfone
National Institute of Standards and Technology, August 2012
https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf

*This publication defines the four-phase incident handling lifecycle (Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident Activity) and provides the prioritization criteria (Functional Impact, Information Impact, Recoverability) used in Section 2 of this knowledge base.*

### MITRE ATT&CK Frameworks

[2]: https://attack.mitre.org/matrices/ics/ "MITRE ATT&CK for ICS - Access Date: 2025-11-09"

[3]: https://attack.mitre.org/ "MITRE ATT&CK Enterprise - Access Date: 2025-11-09"

**MITRE ATT&CK for ICS** (Industrial Control Systems)
https://attack.mitre.org/matrices/ics/

*Framework documenting adversary tactics and techniques targeting ICS/SCADA environments. Used in Section 7 for OT-specific threat hunting and investigation mapping.*

**MITRE ATT&CK Enterprise**
https://attack.mitre.org/

*Framework documenting adversary tactics and techniques in IT environments. Used in Section 3 for attack pattern recognition and event correlation.*

### ICS Security Resources

**SANS Institute - ICS Security**
https://www.sans.org/industrial-control-systems-security/

*Educational resources, training courses (ICS410, ICS515), and research on ICS/SCADA security best practices. Referenced in Section 7 for OT investigation guidance.*

**CISA ICS Advisories** (Cybersecurity and Infrastructure Security Agency)
https://www.cisa.gov/uscert/ics

*Current ICS vulnerabilities, threat intelligence, and security advisories for industrial control systems. Use for threat intelligence when investigating ICS events.*

**Dragos WorldView Threat Intelligence**
https://www.dragos.com/threat-intelligence/

*ICS-specific threat intelligence covering threat groups (ELECTRUM, MAGNALLIUM, KAMACITE) targeting industrial infrastructure.*

### Cognitive Bias Research

**Kahneman, Daniel (2011).** *Thinking, Fast and Slow.* New York: Farrar, Straus and Giroux.

*Foundational work on cognitive biases, including availability bias and anchoring bias. Applied to security analysis in Section 6.*

**Heuer, Richards J. (1999).** *Psychology of Intelligence Analysis.* Center for the Study of Intelligence, CIA.
https://www.cia.gov/static/9a5f1162fd0932c29bfed1c030edf4ae/Pyschology-of-Intelligence-Analysis.pdf

*Classic text on cognitive biases in intelligence analysis. Introduces Analysis of Competing Hypotheses (ACH) technique used in Section 6.*

### ICS Protocol Specifications

**Modbus Organization.** *Modbus Application Protocol Specification V1.1b3.*
https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf

**DNP Users Group.** *DNP3 Specification, IEEE 1815-2012.*
https://www.dnp.org/

**OPC Foundation.** *OPC Unified Architecture (OPC UA) Specification.*
https://opcfoundation.org/developer-tools/specifications-unified-architecture

**IEC.** *IEC 61850: Communication Networks and Systems for Power Utility Automation.*
https://webstore.iec.ch/publication/6028

### Security Operations and SIEM

**Bejtlich, Richard (2013).** *The Practice of Network Security Monitoring.* San Francisco: No Starch Press.

*Best practices for network security monitoring, evidence collection, and investigation workflows referenced in Section 3.*

**MITRE.** *11 Strategies of a World-Class Cybersecurity Operations Center.*
https://www.mitre.org/publications/technical-papers/11-strategies-world-class-cybersecurity-operations-center

*Operational best practices for SOC operations, including alert triage and investigation processes.*

### Additional Resources

**ICS-CERT** (Industrial Control Systems Cyber Emergency Response Team)
https://www.cisa.gov/uscert/ics

*U.S. government resource for ICS incident reporting, advisories, and coordination.*

**ICS-ISAC** (Industrial Control Systems Information Sharing and Analysis Center)
https://www.cisa.gov/resources-tools/resources/ics-isac

*Industry consortium for sharing ICS threat intelligence and best practices.*

**FIRST** (Forum of Incident Response and Security Teams)
https://www.first.org/

*Global forum for incident response teams; publishes standards like CVSS and incident response best practices.*

---

## Document Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | Initial knowledge base creation | BMAD Dev Agent |

---

## Feedback and Contributions

This knowledge base is a living document. If you identify:
- **Errors or inaccuracies**: Report to security-kb-feedback@company.com
- **Missing content**: Suggest additions via security team wiki
- **Tuning recommendations**: Share successful FP tuning strategies in #security-operations Slack channel

**Review Schedule**: This document will be reviewed and updated quarterly to incorporate new threats, techniques, and lessons learned from investigations.

---

*This knowledge base was created following BMAD-METHOD™ framework standards for technical documentation.*

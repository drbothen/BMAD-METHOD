# Event Investigation Training

## Training Overview

**Course Title:** Security Event Alert Investigation
**Duration:** 6-8 hours (self-paced) or 2-day instructor-led
**Target Audience:** Security analysts, SOC analysts, incident responders
**Prerequisites:** Basic understanding of networking, security concepts, and JIRA
**Learning Objectives:**
- Master 5-stage event investigation methodology
- Apply disposition framework (TP/FP/BTP) accurately
- Investigate ICS/IDS/SIEM alerts across platforms
- Recognize and mitigate cognitive biases in investigations
- Navigate ICS/SCADA-specific security considerations

**Training Structure:**
- 8 learning modules (theory + practice)
- Hands-on scenarios with realistic alert data
- Final competency assessment
- Reference materials and job aids

---

## Module 1: Introduction to Event Investigation

### Learning Objectives
- Understand the difference between vulnerability enrichment and event investigation
- Recognize when to use `*investigate-event` command
- Identify alert sources (ICS/IDS/SIEM platforms)

### What is Event Investigation?

**Event Investigation** is the systematic analysis of security alerts from detection platforms (ICS/IDS/SIEM) to determine if observed activity represents:
- **True Positive (TP):** Malicious activity requiring immediate response
- **False Positive (FP):** Detection error with no security concern
- **Benign True Positive (BTP):** Real activity that is authorized/expected

**Comparison:**

| Aspect                  | Vulnerability Enrichment           | Event Investigation                     |
| ----------------------- | ---------------------------------- | --------------------------------------- |
| **Trigger**             | CVE published, vulnerability found | Security alert triggered by platform    |
| **Focus**               | Understanding vulnerability impact | Determining if alert indicates attack   |
| **Timeline**            | Days to weeks (patch planning)     | Minutes to hours (active incident)      |
| **Primary Output**      | Remediation plan                   | Disposition decision (TP/FP/BTP)        |
| **Escalation Criteria** | Risk score, business impact        | Malicious activity confirmation         |

### Detection Platforms

**ICS (Industrial Control Systems):**
- **Example:** Claroty
- **What it detects:** OT network traffic anomalies, protocol violations, unauthorized access
- **Alert Types:** SSH in control environments, Modbus violations, new devices on OT network

**IDS (Intrusion Detection Systems):**
- **Example:** Snort
- **What it detects:** Network-based attack signatures, exploit attempts, malware communication
- **Alert Types:** Exploit attempts, port scans, C2 callbacks, policy violations

**SIEM (Security Information and Event Management):**
- **Example:** Splunk
- **What it detects:** Correlation of events across multiple sources, behavioral anomalies
- **Alert Types:** Multiple failed logins, privilege escalation, data exfiltration patterns

### When to Use `*investigate-event`

Use this command when:
✅ JIRA ticket contains alert from Claroty, Snort, Splunk, or similar platform
✅ Ticket describes "event", "alert", "detection", or "incident"
✅ Ticket requires disposition decision (TP/FP/BTP)
✅ Ticket involves ICS/IDS/SIEM alert investigation

Do NOT use for:
❌ CVE enrichment (use `*enrich-ticket` instead)
❌ Vulnerability assessment (use `*assess-priority`)
❌ MITRE ATT&CK mapping only (use `*map-attack`)

---

## Module 2: Investigation Methodology (5 Stages)

### Learning Objectives
- Apply systematic 5-stage investigation workflow
- Collect evidence from multiple sources
- Perform hypothesis-driven analysis

### The 5 Stages

**Stage 1: Alert Triage (2-3 minutes)**
- Extract alert metadata
- Identify affected assets
- Document network identifiers

**Stage 2: Evidence Collection (5-8 minutes)**
- Gather logs from all sources
- Correlate events across platforms
- Research historical context

**Stage 3: Technical Analysis (4-6 minutes)**
- Validate protocol behavior
- Assess attack vectors
- Evaluate asset context

**Stage 4: Disposition Determination (2-3 minutes)**
- Classify as TP/FP/BTP
- Assign confidence level
- Document reasoning

**Stage 5: Recommendations (2-3 minutes)**
- Immediate actions
- Long-term improvements
- Escalation requirements

### Hands-On Exercise 1.1: Triage Practice

**Alert:**
```
Platform: Claroty
Rule ID: #317
Severity: Medium
Alert: "SSH Connection in Control Environments"
Timestamp: 2025-11-08 14:23:15 UTC
Source: 192.168.10.45
Destination: 10.20.30.15
Protocol: SSH (port 22)
```

**Your Task:** Complete Stage 1 (Triage)

**Checklist:**
- [ ] Identify alert platform: _____________
- [ ] Extract rule ID: _____________
- [ ] Note severity: _____________
- [ ] Document source IP: _____________
- [ ] Document destination IP: _____________
- [ ] Identify protocol: _____________
- [ ] What asset type is 10.20.30.15? _____________

<details>
<summary>Answer Key</summary>

**Completed Triage:**
- Alert Platform: Claroty (ICS detection)
- Rule ID: #317
- Severity: Medium
- Source IP: 192.168.10.45 (likely engineering workstation)
- Destination IP: 10.20.30.15 (likely PLC based on context "Control Environments")
- Protocol: SSH (TCP port 22)
- Asset Type: PLC (inferred from "Control Environments" context)

**Next Steps:**
- Research source hostname (is it authorized engineering workstation?)
- Research destination asset (PLC model, criticality)
- Check for change tickets (authorized SSH maintenance?)
</details>

---

## Module 3: Disposition Framework (TP/FP/BTP)

### Learning Objectives
- Distinguish between TP, FP, and BTP classifications
- Assign appropriate confidence levels
- Document disposition reasoning

### True Positive (TP)

**Definition:** Alert correctly identified malicious or unauthorized activity

**Indicators:**
- Unauthorized access or policy violations
- Attack signatures match known threat patterns
- Malicious intent evidence (persistence, lateral movement, exfiltration)
- No business justification or authorization

**Actions:**
- Escalate to incident response team
- Implement containment measures
- Notify stakeholders (CISO, asset owner)
- Preserve forensic evidence

**Example:**
```
Alert: HTTP connection from HMI to external IP (203.0.113.45)
Evidence:
- After-hours activity (03:45 UTC, no user login)
- Destination IP: Known C2 server (threat intel match)
- Process anomaly: svchost.exe spawned by explorer.exe
- No change ticket or authorization
Disposition: TRUE POSITIVE (TP)
Confidence: High
Action: Escalate to IR, isolate HMI, preserve forensics
```

### False Positive (FP)

**Definition:** Alert triggered incorrectly, no actual security concern

**Root Causes:**
- Detection logic error (signature matches benign traffic)
- Incomplete detection context
- Misconfiguration
- Outdated signature

**Actions:**
- Document root cause
- Recommend signature tuning
- No escalation required (unless impacting operations)

**Example:**
```
Alert: "Unauthorized SSH" to PLC
Evidence:
- Engineering workstation 192.168.10.45 → PLC
- Change ticket CHG-1234 (firmware update scheduled)
- Exception list outdated (workstation removed, but still authorized)
Disposition: FALSE POSITIVE (FP)
Root Cause: Detection exception list not updated
Action: Update Claroty exception list, close ticket
```

### Benign True Positive (BTP)

**Definition:** Alert correctly detected activity, but activity is authorized/expected

**Characteristics:**
- Real activity (not detection error)
- Legitimate business process
- Authorized by change management or business owner

**Actions:**
- Create detection exception (whitelist)
- Document authorization
- No containment required

**Example:**
```
Alert: "Multiple Failed SSH Logins" (15 attempts)
Evidence:
- Source: Jenkins CI/CD system (internal)
- Context: Deployment script (CHG-5690)
- Root cause: Script using password auth (should use SSH keys)
- Historical pattern: Recurring during deployments
Disposition: BENIGN TRUE POSITIVE (BTP)
Reasoning: Authorized deployment activity, misconfigured script
Action: Notify DevOps to fix script, create exception for CI/CD failures
```

### Confidence Levels

| Level      | Criteria                                                      | Example                                                   |
| ---------- | ------------------------------------------------------------- | --------------------------------------------------------- |
| **HIGH**   | 3+ corroborating sources, clear evidence, known pattern      | TP: Malware + C2 callback + threat intel match            |
| **MEDIUM** | 1-2 sources, plausible but not definitive                    | BTP: Verbal approval (no ticket) + activity seems normal  |
| **LOW**    | Single source, gaps in evidence, alternative explanations    | TP: Suspicious activity + no authorization found + gaps   |

### Hands-On Exercise 3.1: Disposition Practice

**Scenario:**
```
Alert: Snort IDS - "ET EXPLOIT Apache Struts2 RCE Attempt"
Source: 198.51.100.22 (External IP, Russia)
Destination: 192.168.50.10 (WEB-APP-01)
Evidence:
- PCAP shows OGNL injection payload (CVE-2017-5638 pattern)
- Web server response: HTTP 500 (Internal Server Error)
- Web server version: Apache Struts 2.5.30 (PATCHED for CVE-2017-5638)
- No command execution observed (no new processes, no outbound connections)
- No file modifications in web directories
```

**Your Task:** Determine disposition and confidence level

**Questions:**
1. Is this a True Positive, False Positive, or Benign True Positive? ___________
2. What confidence level? (High/Medium/Low) ___________
3. What actions should be taken? ___________

<details>
<summary>Answer Key</summary>

**Disposition:** BENIGN TRUE POSITIVE (BTP)

**Reasoning:**
- Real attack attempt occurred (Snort correctly detected exploit payload) → NOT false positive
- Attack was NOT successful (server patched, returned 500 error, no compromise) → NOT true positive
- Expected behavior for patched system (patch working as intended) → Benign

**Confidence:** HIGH
- Multiple corroborating sources (PCAP, web logs, version check, process monitoring)
- Clear evidence attack failed (no command execution indicators)

**Actions:**
- No containment required (attack unsuccessful)
- Validate all Struts2 servers are patched (confirmed)
- Consider creating Snort exception for known-patched vulnerabilities (reduce alert fatigue)
- Informational notification to leadership (successful defense validation)
</details>

---

## Module 4: Platform-Specific Investigations

### Learning Objectives
- Investigate Claroty ICS alerts
- Analyze Snort IDS signatures
- Correlate Splunk SIEM events

### Claroty ICS Investigations

**Platform Focus:** Industrial Control System (OT) network monitoring

**Common Alert Types:**
- Unauthorized protocols on OT network
- SSH/RDP connections to PLCs/HMIs
- Modbus/DNP3 protocol violations
- New devices appearing on OT network
- Firmware changes without authorization

**Investigation Tips:**
- **Context is critical:** OT environments have scheduled maintenance, engineering access
- **Check change management:** Most OT alerts correlate with authorized changes
- **Understand baselines:** What is "normal" for this OT network?
- **Safety first:** Consider physical safety implications before containment

**Example Alert: "Unauthorized Protocol (HTTP) on OT Network"**

Investigation Checklist:
- [ ] What asset is communicating via HTTP? (HMI, PLC, SCADA server?)
- [ ] Destination: Internal or external?
- [ ] Business hours or after-hours?
- [ ] Change ticket exists?
- [ ] Historical pattern (has this happened before)?
- [ ] Asset owner confirms authorization?

### Snort IDS Investigations

**Platform Focus:** Network-based signature detection (exploit attempts, malware)

**Common Alert Types:**
- Exploit attempts (RCE, SQL injection, XSS)
- Port scans and reconnaissance
- Malware C2 communication
- Policy violations (unauthorized protocols)

**Investigation Tips:**
- **Check patch status:** Is target vulnerable? (patched systems = BTP likely)
- **Review PCAP:** Full packet analysis reveals attack success/failure
- **Threat intelligence:** Research source IP, malware signatures
- **Mass scanning vs targeted:** Single attempt (scanner) vs repeated (targeted attack)

**Example Alert: "ET EXPLOIT SQL Injection Attempt"**

Investigation Checklist:
- [ ] PCAP analysis: What SQL injection payload was attempted?
- [ ] Web application response: Success (200 OK) or failure (403/500)?
- [ ] Database logs: Any unusual queries executed?
- [ ] Patch status: Is web app vulnerable to this injection?
- [ ] Source IP: Known scanner or targeted attacker?
- [ ] WAF logs: Was attack blocked before reaching app?

### Splunk SIEM Investigations

**Platform Focus:** Correlation of events across multiple log sources

**Common Alert Types:**
- Multiple failed logins (brute force)
- Privilege escalation patterns
- Data exfiltration (large outbound transfers)
- Anomalous user behavior

**Investigation Tips:**
- **Correlation is key:** SIEM combines events, investigate ALL contributing logs
- **Baseline user behavior:** Is this normal for this user/asset?
- **Time correlation:** Do timestamps align across sources?
- **False correlation:** Sometimes unrelated events trigger correlation rules

**Example Alert: "Multiple Failed Logins - Brute Force Attempt"**

Investigation Checklist:
- [ ] Authentication logs: Which accounts attempted? (root, admin, service accounts?)
- [ ] Source IP: Internal or external?
- [ ] Timing pattern: Automated (3-second intervals) or human (random intervals)?
- [ ] Success rate: Any successful logins?
- [ ] User context: Legitimate user (password reset) or unauthorized?
- [ ] Historical pattern: First occurrence or recurring?

---

## Module 5: Evidence Collection Techniques

### Learning Objectives
- Gather evidence from multiple sources
- Correlate events across platforms
- Identify evidence gaps

### Evidence Source Categories

**Primary Evidence:** Direct observation of alert activity
- Platform alert details
- Packet captures (PCAP)
- Host logs (system, application, security)

**Corroborating Evidence:** Contextual information supporting disposition
- Firewall logs (traffic flow)
- Authentication logs (user activity)
- Change management tickets
- Asset inventory data

**Historical Evidence:** Baseline and pattern analysis
- Previous similar alerts
- Communication baselines
- Asset behavior history

### Multi-Source Correlation

**Technique:** Cross-reference timestamps and identifiers across sources

**Example:**
```
Primary: Claroty alert "SSH to PLC" at 14:23:15 UTC
Corroboration:
- Firewall: Connection 192.168.10.45 → 10.20.30.15:22 at 14:23:12 UTC ✅
- Change Management: Ticket CHG-1234 scheduled 14:00-16:00 UTC ✅
- HMI Logs: User "john.smith" login at 14:20:00 UTC ✅
Result: All sources align → HIGH confidence
```

**Red Flags (Timeline Mismatch):**
```
Primary: Snort alert "Exploit attempt" at 10:15:33 UTC
Corroboration Check:
- Firewall: Connection at 10:15:33 UTC ✅
- Web logs: NO REQUEST at 10:15:33 UTC ❌
- Host logs: NO ACTIVITY at 10:15:33 UTC ❌
Result: Timeline mismatch → Investigate further (possible evasion or log tampering)
```

### Evidence Gap Documentation

**When Evidence is Missing:**
```markdown
**Evidence Collected:**
✅ Claroty alert details
✅ Firewall logs

**Evidence Gaps:**
❌ Host logs unavailable (PLC has limited logging capabilities - EXPECTED)
❌ Packet capture not retained (retention policy 7 days, alert is 10 days old)

**Impact:**
- Confidence reduced to MEDIUM (would be HIGH with host logs)
- Relying on 2 sources instead of 3+
- Cannot verify exact commands executed via SSH
```

### Hands-On Exercise 5.1: Evidence Correlation

**Scenario:**
```
Alert: "Multiple Failed Logins" (Splunk)
Timestamp: 2025-11-09 15:22:00 - 15:27:00 UTC
Target: DB-PROD-01 (172.16.20.30)
Source: APP-WEB-03 (172.16.10.45)
```

**Available Evidence:**
1. SSH auth logs: 15 failed attempts (usernames: root, admin, dbadmin, postgres)
2. Firewall logs: Connection allowed (app tier → database tier)
3. App server logs: Process "deploy-script.sh" (user: jenkins)
4. Change ticket: CHG-5690 "Deploy v2.3.1" (scheduled 15:00-16:00 UTC)

**Your Task:** Correlate evidence and determine disposition

<details>
<summary>Answer Key</summary>

**Evidence Correlation:**
- SSH failed attempts (15:22-15:27) align with deployment window (15:00-16:00) ✅
- Source (APP-WEB-03) matches deployment server ✅
- Process (deploy-script.sh) confirms deployment activity ✅
- Change ticket (CHG-5690) provides authorization ✅

**Disposition:** BENIGN TRUE POSITIVE (BTP)
- Real failed attempts (not false positive)
- Authorized deployment activity (not malicious)
- Root cause: Deployment script misconfiguration (using password auth instead of SSH keys)

**Confidence:** HIGH (4 corroborating sources)

**Recommendations:**
- Notify DevOps: Fix deploy-script.sh to use SSH keys
- Create Splunk exception for CI/CD → DB failed logins during change windows
</details>

---

## Module 6: Cognitive Bias in Investigations

### Learning Objectives
- Recognize 5 cognitive biases in investigations
- Apply debiasing techniques
- Conduct hypothesis-driven analysis

### The 5 Cognitive Biases

#### 1. Automation Bias

**Definition:** Blindly trusting alert severity or platform classification

**Example:**
```
Alert: "CRITICAL - Exploit Attempt Detected"
Biased Response: "Alert says critical, must escalate immediately!"
Reality: Outdated signature, triggers on benign TLS 1.3 handshake
```

**Debiasing:**
- Always validate alert claims with independent evidence
- Question severity assignments (verify with analysis)
- Understand what triggers the alert (review signature logic)

#### 2. Anchoring Bias

**Definition:** Fixating on first hypothesis, ignoring alternatives

**Example:**
```
Alert: "Unauthorized Protocol on OT Network"
First Hypothesis: "Malware using HTTP for C2"
Biased Investigation: Only seeks C2 indicators, ignores benign explanations
Reality: SCADA software update using HTTP (authorized maintenance)
```

**Debiasing:**
- Generate 2-3 hypotheses BEFORE collecting evidence
- Test EACH hypothesis against evidence
- Document why alternative hypotheses were rejected

#### 3. Confirmation Bias

**Definition:** Seeking only evidence that confirms initial assessment

**Example:**
```
Initial Assessment: "High CVSS = critical priority"
Biased Research: Searches only for exploitation evidence
Ignores: EPSS 0.01%, no KEV, asset not internet-facing (LOW priority indicators)
```

**Debiasing:**
- Actively seek disconfirming evidence ("what would prove me WRONG?")
- Use structured checklists (forces consideration of all factors)
- Peer review (second analyst provides objective perspective)

#### 4. Availability Heuristic

**Definition:** Overweighting recent or memorable incidents

**Example:**
```
Recent Event: Ransomware attack last week
Current Alert: Unrelated RCE vulnerability
Biased Assessment: "We just had ransomware, this RCE must be related!"
Reality: No connection between events
```

**Debiasing:**
- Research historical context (not just recent events)
- Ask: "Is this pattern specific to this alert, or just memorable?"
- Separate correlation from causation

#### 5. Automation Bias (in disposition)

**Definition:** Trusting platform disposition without validation

**Example:**
```
Claroty Alert: Severity = "High"
Biased Response: "Claroty says high, so priority is high"
Reality: Authorized SSH during maintenance window (should be INFO severity)
```

**Debiasing:**
- Independently calculate priority using business context
- Don't inherit severity from platform blindly
- Adjust severity based on disposition (BTP → downgrade severity)

### Hypothesis-Driven Investigation

**Process:**
1. **Generate Hypotheses:** Before evidence collection, create 2-3 explanations
2. **Collect Evidence:** Gather data for ALL hypotheses (not just first idea)
3. **Test Each Hypothesis:** Does evidence support or refute?
4. **Select Best-Supported Hypothesis:** Choose based on evidence weight

**Example:**
```
Alert: SSH to PLC from 192.168.10.45

Hypotheses:
1. Malicious unauthorized access (TP)
2. Authorized maintenance (BTP)
3. Detection platform error (FP)

Evidence Collection:
- Hypothesis 1: Look for no change ticket, after-hours timing, malicious indicators
- Hypothesis 2: Look for change ticket, authorized source IP, business hours
- Hypothesis 3: Look for log inconsistencies, signature logic errors

Results:
- Hypothesis 1: ❌ Change ticket found, business hours, no malicious indicators
- Hypothesis 2: ✅ Change ticket CHG-1234, authorized IP, maintenance window
- Hypothesis 3: ❌ Logs confirm real activity (not detection error)

Selected: Hypothesis 2 (BTP - Authorized maintenance)
```

---

## Module 7: ICS/SCADA-Specific Considerations

### Learning Objectives
- Understand ICS/SCADA unique security challenges
- Assess safety implications of alerts
- Navigate OT protocol peculiarities

### ICS/SCADA Environment Characteristics

**Differences from IT:**
- **Safety-Critical:** Failures can cause physical harm (industrial accidents)
- **Availability Priority:** Uptime more important than confidentiality (can't patch during production)
- **Legacy Systems:** 10-20 year old equipment, limited security capabilities
- **Air-Gap Assumptions:** Historically isolated, now increasingly connected

### Safety Implications

**CRITICAL QUESTION:** Could this alert indicate activity that affects physical processes?

**Examples:**
- HMI compromise → attacker could send commands to PLCs → production disruption or safety system interference
- PLC firmware change → could alter safety logic → physical danger to workers
- SCADA server compromise → loss of visibility into physical processes → cannot respond to safety events

**Investigation Priority:**
- **Safety-Critical Assets:** Immediate escalation (even if BTP likely)
- **Production-Critical Assets:** Coordinate with operations before containment
- **Non-Critical Assets:** Standard investigation workflow

### Legacy System Constraints

**Common Limitations:**
- Limited logging (PLCs may not log commands executed)
- Outdated protocols (Modbus TCP is cleartext - THIS IS NORMAL)
- No modern security controls (cannot deploy EDR on Windows 7 embedded HMI)
- Patching challenges (vendor approval required, downtime costly)

**Adjusted Expectations:**
```markdown
❌ WRONG:
"No command audit log for SSH session - evidence of log tampering!"

✅ RIGHT:
"No command audit log (expected - PLC has limited logging capabilities).
Used alternative evidence: firewall logs + change ticket."
```

### OT Protocol Knowledge

**Common OT Protocols:**

| Protocol    | Port       | Purpose                   | Normal Characteristics                        |
| ----------- | ---------- | ------------------------- | --------------------------------------------- |
| Modbus TCP  | 502        | PLC communication         | Cleartext, cyclic polling (1-5 sec intervals) |
| DNP3        | 20000      | SCADA (utilities)         | Cleartext, master-slave                       |
| BACnet      | 47808 (UDP)| Building automation       | Broadcast-heavy (device discovery)            |
| IEC 104     | 2404       | Power grid (SCADA)        | Cleartext, polling-based                      |

**What is NORMAL (not suspicious):**
- Cleartext protocols (OT protocols don't have encryption - by design)
- Cyclic polling (HMI → PLC status requests every few seconds)
- Broadcast traffic (BACnet device discovery)
- Limited authentication (legacy protocols lack modern auth)

**What is SUSPICIOUS:**
- OT protocol from unexpected source (IT network → OT network)
- OT protocol to unexpected destination (PLC → Internet)
- Protocol violation (malformed Modbus packets)
- Unusual timing (OT activity during shutdown hours)

### Hands-On Exercise 7.1: ICS Safety Assessment

**Scenario:**
```
Alert: Claroty - "Unauthorized HTTP Connection"
Source: 10.30.40.55 (HMI-ZONE-1-01)
Destination: 203.0.113.45 (External IP)
Time: 03:45 UTC (after-hours)
Asset Function: HMI controls Zone 1 production line (automotive assembly)
```

**Your Task:** Assess safety implications

**Questions:**
1. What physical processes could be affected? ___________
2. What safety systems could be impacted? ___________
3. Should this be escalated differently due to safety concerns? ___________
4. What containment considerations exist? ___________

<details>
<summary>Answer Key</summary>

**Physical Processes:**
- Zone 1 production line (automotive assembly)
- Robotic arms, conveyor systems, welding equipment

**Safety Systems:**
- Safety interlocks (prevent equipment collision)
- Emergency stop systems
- Personnel safety zones

**Escalation:**
- YES - Immediate escalation to CISO and Operations Manager
- Safety-critical asset (HMI controls production safety systems)
- Potential compromise could disable safety interlocks
- External communication (possible C2 - suggests malware)

**Containment Considerations:**
- Cannot isolate HMI during production shift (safety risk - loss of control visibility)
- Coordinate with operations for emergency production shutdown
- Manual monitoring in interim (watch for abnormal commands to PLCs)
- Safety team on standby (in case of physical safety event)
</details>

---

## Module 8: Hands-On Scenarios

### Scenario 1: Claroty ICS Alert (BTP)

**Ticket: AOD-4052**

```
Platform: Claroty
Rule ID: #317
Severity: Medium
Alert: "SSH Connection in Control Environments"
Timestamp: 2025-11-08 14:23:15 UTC
Source: 192.168.10.45 (ENG-WS-05)
Destination: 10.20.30.15 (PLC-ZONE-3-01)
Protocol: SSH (port 22)
Connection Duration: 18 minutes 42 seconds
```

**Additional Information:**
- Change Ticket: CHG-2024-5678 "PLC-ZONE-3-01 firmware update" (scheduled 14:00-16:00 UTC)
- Engineer: John Smith (uses ENG-WS-05 workstation)
- Historical: Last SSH to this PLC was 90 days ago (previous firmware update)

**Your Investigation:** Complete all 5 stages and determine disposition

<details>
<summary>Solution</summary>

**Stage 1: Triage**
- Platform: Claroty (ICS)
- Asset: PLC-ZONE-3-01 (production control - critical)
- Network: OT (Level 1 Control Network)

**Stage 2: Evidence**
- Change ticket confirms authorization
- SSH timing aligns with maintenance window
- Historical pattern matches (quarterly firmware updates)

**Stage 3: Analysis**
- Protocol: SSH expected for firmware updates
- Source: Authorized engineering workstation
- No malicious indicators

**Stage 4: Disposition**
- **Disposition:** BENIGN TRUE POSITIVE (BTP)
- **Confidence:** HIGH
- **Reasoning:** Authorized maintenance activity, correlated with change ticket

**Stage 5: Recommendations**
- Create Claroty exception for ENG-WS-05 → PLCs during change windows
- No containment required
</details>

### Scenario 2: Snort IDS Alert (BTP - Patched System)

**Ticket: SEC-789**

```
Platform: Snort
Rule: ET EXPLOIT Apache Struts2 RCE Attempt (SID 1:58234)
Severity: High
Source: 198.51.100.22 (External IP - Russia)
Destination: 192.168.50.10 (WEB-APP-01)
Payload: OGNL injection in Content-Type header (CVE-2017-5638)
Response: HTTP 500 Internal Server Error
```

**Additional Information:**
- Web server: Apache Struts 2.5.30 (PATCHED for CVE-2017-5638)
- No new processes spawned at alert timestamp
- No outbound connections from WEB-APP-01
- Source IP: Known scanner (mass scanning for vulnerable Struts2 servers)

**Your Investigation:** Determine disposition and recommended actions

<details>
<summary>Solution</summary>

**Disposition:** BENIGN TRUE POSITIVE (BTP)
**Confidence:** HIGH

**Reasoning:**
- Real attack attempt (Snort correctly detected exploit payload)
- Attack unsuccessful (server patched, HTTP 500 error, no compromise)
- Expected behavior for patched system (patch working as intended)

**Recommendations:**
- No containment required (attack unsuccessful)
- Validate all Struts2 servers patched
- Consider Snort exception for known-patched vulnerabilities
- Informational notification (successful defense validation)
</details>

### Scenario 3: Splunk SIEM Alert (BTP - Misconfigured Script)

**Ticket: AOD-3456**

```
Platform: Splunk
Rule: "Multiple Failed SSH Logins - Brute Force Attempt"
Severity: Medium
Target: DB-PROD-01 (172.16.20.30)
Source: APP-WEB-03 (172.16.10.45)
Failed Attempts: 15 in 5 minutes
Usernames: root, admin, dbadmin, oracle, postgres, mysql
```

**Additional Information:**
- APP-WEB-03 is Jenkins CI/CD server
- Change ticket: CHG-2024-5690 "Deploy v2.3.1" (in progress)
- App logs show "deploy-script.sh" running as "jenkins" user
- Historical: Similar alerts during previous deployments (recurring issue)

**Your Investigation:** Determine root cause and recommendations

<details>
<summary>Solution</summary>

**Disposition:** BENIGN TRUE POSITIVE (BTP)
**Confidence:** HIGH

**Reasoning:**
- Real failed attempts (not false positive)
- Authorized deployment activity (change ticket)
- Root cause: Misconfigured deployment script (password auth instead of SSH keys)

**Immediate Actions:**
- Notify DevOps to fix deploy-script.sh
- No containment required

**Long-Term:**
- Create Splunk exception for CI/CD → DB failures during change windows
- Implement deployment script validation (test SSH key auth before production)
</details>

---

## Final Assessment

### Theory Questions (20 points)

1. **[4 pts]** Explain the difference between True Positive (TP), False Positive (FP), and Benign True Positive (BTP). Provide one example of each.

2. **[3 pts]** Name the 5 stages of event investigation and the approximate time for each.

3. **[3 pts]** List 3 cognitive biases and one debiasing technique for each.

4. **[3 pts]** What are 3 ICS/SCADA-specific considerations when investigating OT alerts?

5. **[2 pts]** When should you assign HIGH confidence vs MEDIUM confidence to a disposition?

6. **[2 pts]** Name the 3 main detection platform types and give one example alert for each.

7. **[3 pts]** What is hypothesis-driven investigation? Describe the 4 steps.

### Practical Assessment (30 points)

**Scenario: Unknown After-Hours Activity**

```
Ticket: AOD-7890
Platform: Claroty
Rule: #204 "Unauthorized Protocol on OT Network (HTTP)"
Severity: High
Timestamp: 2025-11-10 02:15:33 UTC
Source: 10.30.40.77 (HMI-ZONE-2-03)
Destination: 93.184.216.34 (External IP)
Protocol: HTTP (port 80)
Data Transferred: 127 MB outbound, 4 KB inbound

Asset Information:
- HMI-ZONE-2-03: Controls Zone 2 production (pharmaceutical manufacturing)
- Asset Criticality: 5/5 (Business-Critical + Safety-Critical)
- Expected Protocols: Modbus TCP to PLCs only
- Network Zone: OT Level 1 (isolated from IT network)

Evidence Available:
- Claroty logs: 23 HTTP connections in 15-minute period
- Firewall logs: Connection allowed by legacy "OT-Emergency-Internet" rule
- HMI logs: No user login at 02:15 UTC
- Process logs: "update-service.exe" (PID 4521) initiated connections
- Scheduled maintenance: None
- Change tickets: None for this timeframe

Threat Intelligence:
- Destination IP: Legitimate CDN (Akamai)
- Domain resolution: update.software-vendor.com
- No known malicious association
```

**Your Task (30 points):**

1. **[6 pts]** Perform Stage 1 (Triage): Document all alert metadata, network identifiers, and affected asset details.

2. **[8 pts]** Perform Stage 2-3 (Evidence + Analysis): What additional evidence would you collect? What are the suspicious indicators? What are the benign indicators?

3. **[8 pts]** Perform Stage 4 (Disposition): Classify as TP/FP/BTP with confidence level. Provide detailed reasoning.

4. **[8 pts]** Perform Stage 5 (Recommendations): What immediate actions? What long-term improvements? Should this be escalated?

### Assessment Scoring

**Total Points:** 50

**Grading Scale:**
- 45-50: Excellent (ready for independent event investigations)
- 38-44: Good (ready with mentor oversight)
- 30-37: Needs Improvement (additional training recommended)
- < 30: Inadequate (retake training)

---

## Additional Resources

- **Event Investigation Workflow Deep Dive:** `docs/workflows/event-investigation-workflow-deep-dive.md`
- **Security Analyst User Guide:** `docs/user-guide/security-analyst-agent.md`
- **Troubleshooting FAQ:** `docs/troubleshooting-faq-best-practices.md`
- **NIST SP 800-61:** Computer Security Incident Handling Guide
- **MITRE ATT&CK:** https://attack.mitre.org/

---

**Course Version:** 1.0
**Last Updated:** 2025-11-09
**Maintained By:** BMAD Engineering Team

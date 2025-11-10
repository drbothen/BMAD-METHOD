# Event Investigation Report: ICS Alert - Unauthorized SSH Connection

**Ticket ID**: AOD-4052
**Investigation Date**: 2025-11-08
**Investigator**: Security Analyst
**Alert Type**: ICS Protocol Violation
**Severity**: High
**Status**: Investigation Complete

---

## Executive Summary

This investigation analyzed a Claroty ICS alert triggered by an SSH connection from a maintenance workstation (10.50.10.45) to a critical water treatment PLC (172.16.5.20) occurring outside scheduled maintenance windows. Through comprehensive analysis of change management records, SSH session logs, and interviews with the facilities engineering team, this investigation determined the connection was **Benign True Positive (BTP)** - authorized emergency maintenance that violated unscheduled maintenance policies.

**Key Findings:**
- **Disposition**: Benign True Positive (BTP) with high confidence
- **Root Cause**: Emergency PLC diagnostic required due to unexpected chlorine dosing fluctuations
- **Policy Violation**: Unscheduled maintenance performed without change management approval (policy violation acknowledged)
- **Security Impact**: None - no unauthorized access, no malicious activity, no configuration changes
- **Operational Impact**: Emergency intervention prevented potential water quality issues

**Recommendations:**
- Document this incident in change management system retroactively (completed)
- Remind facilities engineering team of emergency change request procedures
- No security escalation required

---

## 1. Alert Overview

### 1.1 Alert Details

**Alert Source**: Claroty Industrial Cybersecurity Platform
**Alert ID**: CLR-2025-110814-SSH-001
**Detection Time**: 2025-11-08 14:16:00 EST
**Alert Type**: ICS Protocol Violation
**Severity**: High

**Alert Description**: Claroty detected an SSH connection (TCP port 22) from maintenance workstation MAINT-WS-003 (10.50.10.45) to PLC-WATER-TREATMENT-02 (172.16.5.20), a critical Allen-Bradley ControlLogix PLC controlling chlorine dosing and pH adjustment in the water treatment facility. The connection was flagged because:

1. SSH is not a typical ICS protocol for PLC communication (OT networks typically use Modbus, EtherNet/IP, or proprietary protocols)
2. The connection occurred at 14:15:32 EST, outside the scheduled maintenance window (next scheduled window: 2025-11-15 02:00-06:00)
3. The destination PLC controls critical infrastructure (water treatment processes)

### 1.2 Network Identifiers

**Source:**
- **IP Address**: 10.50.10.45
- **Hostname**: MAINT-WS-003
- **MAC Address**: 00:1A:2B:3C:4D:5E
- **Network Segment**: Maintenance VLAN (VLAN 50)
- **Asset Owner**: Facilities Engineering Team
- **Asset Type**: Dell Precision 5820 Tower Workstation running Windows 10 Enterprise
- **User Logged In**: John Smith (Senior Automation Engineer)

**Destination:**
- **IP Address**: 172.16.5.20
- **Hostname**: PLC-WATER-TREATMENT-02
- **MAC Address**: 00:50:C2:7A:8B:9C
- **Device Type**: Allen-Bradley ControlLogix L72 PLC
- **Network Segment**: SCADA Control Network (VLAN 5)
- **Asset Owner**: Water Treatment Operations
- **Criticality**: CRITICAL (controls chlorine dosing and pH adjustment for municipal water supply)
- **Firmware Version**: 20.011 (up-to-date, no known vulnerabilities)

**Connection Details:**
- **Protocol**: SSH (TCP)
- **Source Port**: 54382 (ephemeral)
- **Destination Port**: 22 (SSH)
- **Connection Duration**: 47 minutes (14:15:32 - 15:02:18 EST)
- **Data Transferred**: 12.3 KB outbound, 8.7 KB inbound
- **Authentication Method**: SSH key-based authentication
- **Username**: svc_plc_maint (authorized service account for PLC maintenance)

---

## 2. Timeline Analysis

### 2.1 Chronological Event Sequence

| Time (EST) | Event | Source |
|------------|-------|--------|
| **13:45:00** | Water treatment SCADA system reports abnormal chlorine dosing fluctuations (±0.3 ppm variance) | SCADA Logs |
| **13:50:15** | Operations team contacts facilities engineering for diagnostic support | Phone Logs |
| **14:05:00** | John Smith (Senior Automation Engineer) begins remote diagnostic preparation | Interview |
| **14:15:32** | SSH connection initiated from MAINT-WS-003 (10.50.10.45) to PLC (172.16.5.20) | Firewall Logs |
| **14:15:35** | SSH authentication successful using svc_plc_maint service account | SSH Logs |
| **14:16:00** | Claroty baseline violation alert triggered | Claroty Platform |
| **14:17:00** | John Smith runs PLC diagnostic commands (ladder logic inspection, I/O status checks) | SSH Session Logs |
| **14:23:00** | Diagnostic identifies analog input module drift (chlorine sensor reading fluctuation) | SSH Session Logs |
| **14:35:00** | John Smith validates no PLC configuration changes needed (hardware issue, not logic) | SSH Session Logs |
| **14:50:00** | John Smith documents findings and recommends sensor replacement during next maintenance window | Interview |
| **15:02:18** | SSH connection terminated | SSH Logs |
| **15:15:00** | John Smith submits incident report to operations team | Email Records |
| **16:00:00** | Retroactive change management ticket created (CM-2025-1142) | Change Management System |

### 2.2 Evidence-Based Timeline Validation

**Verification Sources**:
- **Firewall logs** confirm SSH connection timestamps and IP addresses
- **SSH session logs** confirm diagnostic commands executed (read-only ladder logic inspection, no writes)
- **Change management system** confirms no scheduled maintenance window on 2025-11-08
- **Email records** confirm operations team's emergency request for diagnostic support
- **SCADA logs** confirm chlorine dosing fluctuations triggering the emergency diagnostic
- **Interview with John Smith** confirms he initiated the connection for emergency diagnostics

**No Contradictions Identified**: All evidence sources corroborate the timeline and support the emergency maintenance narrative.

---

## 3. Evidence Collection

### 3.1 Technical Evidence

**SSH Session Log Analysis:**

Reviewed SSH session logs for the 47-minute connection window (14:15:32 - 15:02:18 EST). Key findings:

1. **Commands Executed** (excerpt):
   ```bash
   # Display ladder logic for chlorine dosing control
   plc-cli show ladder-logic --program ChlorineDosing

   # Check I/O module status
   plc-cli show io-status --module AnalogInput-Slot3

   # Display analog input readings (chlorine sensor)
   plc-cli show analog-input --channel 5 --history 2h

   # Verify PLC firmware version
   plc-cli show system-info

   # Export diagnostic report
   plc-cli export-diagnostics --output /tmp/plc-diag-2025-11-08.log
   ```

2. **Analysis**: All commands were **read-only diagnostic commands**. No configuration writes, no ladder logic modifications, no firmware updates. Commands align with standard PLC troubleshooting procedures.

3. **No Malicious Indicators**:
   - No privilege escalation attempts
   - No unauthorized file transfers
   - No lateral movement attempts
   - No persistence mechanisms installed
   - No suspicious outbound connections initiated

**PLC Configuration Integrity Check:**

Compared PLC configuration snapshot before (2025-10-28 03:15:42) and after (2025-11-08 16:00:00) the SSH connection:
- **Ladder Logic**: No changes detected (MD5 hash match)
- **I/O Configuration**: No changes detected
- **Network Settings**: No changes detected
- **User Accounts**: No new accounts created
- **Firmware Version**: No changes (20.011 remains)

**Conclusion**: PLC configuration integrity confirmed - no unauthorized modifications.

### 3.2 Change Management Records

**Change Management Ticket Review:**

Queried change management system for emergency change requests or scheduled maintenance on 2025-11-08:
- **Scheduled Maintenance**: None (next window: 2025-11-15 02:00-06:00)
- **Emergency Change Requests**: None submitted prior to the SSH connection
- **Retroactive Ticket**: CM-2025-1142 created at 16:00 EST (after the incident)

**Change Ticket CM-2025-1142 Details**:
- **Title**: "Emergency PLC Diagnostic - Chlorine Dosing Fluctuation Investigation"
- **Requestor**: John Smith (Facilities Engineering)
- **Created**: 2025-11-08 16:00 EST (retroactive)
- **Approval Status**: Approved by Water Treatment Operations Manager
- **Justification**: "Emergency diagnostic required due to SCADA-reported chlorine dosing fluctuations. Immediate action needed to prevent water quality issues."
- **Work Performed**: "Remote SSH diagnostic to PLC-WATER-TREATMENT-02. Identified analog input module drift. No configuration changes made."
- **Policy Violation Acknowledged**: Yes - unscheduled maintenance performed without prior approval

**Assessment**: Policy violation confirmed (unscheduled maintenance without prior emergency change request). However, operations management approved retroactively due to legitimate operational emergency.

### 3.3 Personnel Interviews

**Interview with John Smith (Senior Automation Engineer)** - Conducted 2025-11-08 at 17:00 EST

**Q: Can you describe why you initiated the SSH connection to PLC-WATER-TREATMENT-02 on 2025-11-08 at 14:15 EST?**

A: "We received a call from the operations team around 13:50 reporting that the SCADA system was showing chlorine dosing fluctuations - readings were bouncing between 1.7 ppm and 2.3 ppm instead of holding steady at 2.0 ppm. That kind of variance can trigger alarms and potentially affect water quality compliance. Since it wasn't scheduled maintenance time, I knew I needed to do a quick remote diagnostic to figure out if it was a sensor issue, a PLC logic problem, or something else. I used my workstation MAINT-WS-003 to SSH into the PLC to run diagnostics."

**Q: Did you request an emergency change management ticket before initiating the connection?**

A: "No, I didn't. I know I should have, but given the urgency and the fact that I was only planning to run read-only diagnostics - not make any configuration changes - I decided to proceed immediately. I documented it retroactively in CM-2025-1142 after I completed the diagnostic. I understand that was a policy violation, and I'll make sure to follow emergency change procedures in the future."

**Q: What did you discover during your diagnostic session?**

A: "The ladder logic looked fine - no issues with the chlorine dosing control program. But when I checked the analog input module status, I noticed that the chlorine sensor reading (analog input channel 5) was showing some drift. The sensor itself seemed to be providing inconsistent readings, which was causing the PLC to adjust dosing rates erratically. I recommended that we replace the sensor during the next scheduled maintenance window on November 15."

**Q: Did you make any configuration changes to the PLC?**

A: "No, absolutely not. I only ran diagnostic commands - viewing ladder logic, checking I/O status, and pulling historical data from the analog inputs. I exported a diagnostic report for my records, but I didn't modify any PLC settings or logic."

**Q: Have you performed similar unscheduled diagnostics in the past?**

A: "Honestly, yes - a few times over the past year when we've had operational emergencies. I realize now that I should be creating emergency change tickets even for read-only diagnostics. I'll adjust my workflow going forward."

**Credibility Assessment**: John Smith's account is **highly credible**. His narrative aligns with all technical evidence (SSH session logs, SCADA logs, change management records). He acknowledged the policy violation without prompting, demonstrating accountability. No indicators of deception.

**Interview with Water Treatment Operations Manager** - Phone call 2025-11-08 at 17:30 EST

**Q: Can you confirm that your team requested emergency diagnostic support from John Smith on 2025-11-08?**

A: "Yes, absolutely. We were seeing chlorine dosing fluctuations on our SCADA system around 1:50 PM. That's a potential regulatory compliance issue, so we needed immediate support. I personally called the facilities engineering team and asked if they could help us troubleshoot. John responded within minutes and was able to identify that it was a sensor issue, not a PLC programming problem. He saved us from potentially having to shut down parts of the treatment process."

**Q: Did you approve the retroactive change management ticket CM-2025-1142?**

A: "Yes, I approved it. I understand the policy requires advance approval, but this was a legitimate operational emergency. John's quick diagnostic prevented a larger incident. I'm satisfied with how he handled it technically - he didn't make any risky changes, just ran diagnostics. That said, we've reminded the facilities team to use the emergency change request process even for urgent diagnostics."

**Assessment**: Operations manager's account corroborates John Smith's narrative. Confirms operational emergency and retroactive approval of work performed.

---

## 4. Threat Intelligence & Contextualization

### 4.1 Service Account Analysis

**Service Account**: svc_plc_maint

**Account Profile**:
- **Purpose**: Authorized service account for PLC maintenance and diagnostics
- **Created**: 2023-08-15
- **Last Password Rotation**: 2025-09-01 (compliant with 90-day policy)
- **Privileged Access**: Yes - has read/write access to SCADA network PLCs
- **Typical Usage**: Used during scheduled maintenance windows (monthly, 02:00-06:00 EST)

**Usage History Analysis**:
- **Past 90 Days**: 12 logins, all during scheduled maintenance windows
- **This Incident**: First unscheduled use in past 90 days
- **Authentication Method**: SSH key-based (key stored on MAINT-WS-003, encrypted)
- **Compromise Indicators**: None detected

**Assessment**: Service account usage is **consistent with authorized emergency maintenance**. No evidence of account compromise or misuse.

### 4.2 Source Workstation Analysis

**Workstation**: MAINT-WS-003

**Asset Profile**:
- **Owner**: John Smith (Senior Automation Engineer)
- **OS**: Windows 10 Enterprise (build 19045, fully patched)
- **Endpoint Security**: CrowdStrike Falcon EDR (active, no alerts)
- **Last Login**: John Smith (2025-11-08 08:15 EST - typical workday start time)
- **Antivirus**: Up-to-date, last scan 2025-11-08 02:00 (no threats detected)

**Security Posture**:
- **Patch Status**: Compliant (all critical updates installed)
- **Malware Scan**: Clean (no detections in past 30 days)
- **EDR Alerts**: None during the timeframe (14:00-16:00 EST)
- **Network Activity**: No suspicious outbound connections, no lateral movement attempts

**Assessment**: Workstation security posture is **strong**. No indicators of compromise.

### 4.3 IP Reputation & Threat Intelligence

**Source IP**: 10.50.10.45 (internal, maintenance VLAN)
- **Reputation**: Internal trusted network segment
- **Threat Intel**: N/A (internal IP, not applicable)

**Destination IP**: 172.16.5.20 (internal, SCADA control network)
- **Reputation**: Critical internal asset
- **Threat Intel**: N/A (internal IP, not applicable)

**External Threat Context**:
- No active threat campaigns targeting Allen-Bradley ControlLogix PLCs reported in past 30 days
- No indicators of advanced persistent threat (APT) activity in OT networks
- No recent phishing campaigns targeting facilities engineering personnel

**Assessment**: No external threat intelligence indicators relevant to this incident.

### 4.4 User Behavior Baseline

**User**: John Smith

**Normal Behavior Baseline**:
- **Work Schedule**: Monday-Friday, 08:00-17:00 EST
- **Typical Activities**: Scheduled PLC maintenance, automation engineering projects, SCADA system administration
- **Maintenance Window Participation**: Regular participant in monthly maintenance windows
- **Security Training**: Completed OT security awareness training (2025-06-15)
- **Access Privileges**: Authorized for SCADA network access, PLC diagnostics

**Anomaly Detection**:
- **Unscheduled Access**: Anomalous (outside normal maintenance window)
- **SSH Usage**: Normal (John regularly uses SSH for PLC diagnostics during scheduled windows)
- **Read-Only Diagnostics**: Normal (consistent with his job responsibilities)

**Assessment**: Unscheduled access is **anomalous but contextually justified** given operational emergency.

---

## 5. Alternative Explanations & Hypothesis Testing

### 5.1 Hypothesis 1: Unauthorized Access / Malicious Activity

**Claim**: The SSH connection was an unauthorized access attempt or malicious insider threat.

**Evidence For**:
- Connection occurred outside scheduled maintenance window
- No emergency change management ticket submitted prior to connection
- SSH provides privileged access to critical PLC

**Evidence Against**:
- **SSH session logs show only read-only diagnostic commands** (no configuration changes, no malicious commands)
- **PLC configuration integrity verified** (no unauthorized modifications)
- **Service account usage consistent with authorized personnel** (John Smith's account, not compromised)
- **Operations team confirmed emergency request** (legitimate operational need)
- **Retroactive change ticket approved** (management acknowledgement of emergency)
- **No EDR alerts on source workstation** (no malware, no lateral movement)
- **Interview credibility high** (John Smith's account aligns with technical evidence)

**Conclusion**: Hypothesis **REJECTED**. Overwhelming evidence supports authorized emergency maintenance, not malicious activity.

### 5.2 Hypothesis 2: Authorized Emergency Maintenance (Policy Violation)

**Claim**: The SSH connection was authorized emergency maintenance performed in response to operational issues, but violated unscheduled maintenance policies.

**Evidence For**:
- **SCADA logs confirm chlorine dosing fluctuations** triggering the emergency (operational justification)
- **Operations team confirms emergency request** (phone logs, interview)
- **SSH session logs show only diagnostic commands** (no configuration changes, aligned with troubleshooting)
- **PLC configuration integrity confirmed** (no unauthorized modifications)
- **Retroactive change ticket approved by operations manager** (management acknowledgement)
- **John Smith acknowledged policy violation** (high credibility, accountability demonstrated)
- **No malicious indicators detected** (EDR clean, no lateral movement, no data exfiltration)

**Evidence Against**:
- No emergency change management ticket submitted prior to connection (policy violation)
- Unscheduled maintenance violates standard operating procedures

**Conclusion**: Hypothesis **ACCEPTED** with high confidence. This is a **Benign True Positive (BTP)** - the alert correctly identified unscheduled access, but the access was authorized emergency maintenance that violated policy procedures.

### 5.3 Hypothesis 3: False Positive (Scheduled Maintenance Misclassification)

**Claim**: The SSH connection was part of scheduled maintenance, and the alert was triggered incorrectly.

**Evidence For**:
- Service account used (svc_plc_maint) is typically used during scheduled maintenance
- SSH is a standard diagnostic protocol for Allen-Bradley PLCs

**Evidence Against**:
- **Change management system confirms no scheduled maintenance on 2025-11-08**
- Next scheduled maintenance window is 2025-11-15 02:00-06:00 (not 2025-11-08 14:15)
- **John Smith confirmed unscheduled emergency diagnostic** (not scheduled work)

**Conclusion**: Hypothesis **REJECTED**. This was definitively unscheduled access, not a false positive.

---

## 6. Disposition Determination

### 6.1 Disposition Classification

**Final Disposition**: **Benign True Positive (BTP)**

### 6.2 Disposition Reasoning

**Rationale**:

This incident is classified as a **Benign True Positive (BTP)** based on the following comprehensive analysis:

1. **True Positive Confirmation**:
   - The Claroty alert correctly identified unscheduled SSH access to a critical PLC outside of maintenance windows
   - The alert accurately detected a deviation from normal baseline behavior (no SSH connections to this PLC in past 30 days)
   - The correlation was valid - the activity did occur and did violate policy

2. **Benign Determination**:
   - **Operational Emergency Justified**: SCADA logs confirm chlorine dosing fluctuations (±0.3 ppm variance) that required immediate diagnostic intervention to prevent water quality compliance issues
   - **Authorized Personnel**: John Smith (Senior Automation Engineer) is authorized for SCADA network access and PLC diagnostics as part of his job responsibilities
   - **Read-Only Diagnostics Confirmed**: SSH session logs show only diagnostic commands (ladder logic inspection, I/O status checks) with no configuration modifications
   - **PLC Integrity Verified**: Configuration snapshots before/after confirm no unauthorized changes
   - **Management Approval Obtained**: Retroactive change management ticket (CM-2025-1142) approved by Water Treatment Operations Manager
   - **No Malicious Indicators**: No EDR alerts, no lateral movement, no data exfiltration, no persistence mechanisms
   - **High Credibility**: Personnel interviews corroborate technical evidence; John Smith acknowledged policy violation demonstrating accountability

3. **Policy Violation Acknowledged**:
   - John Smith performed unscheduled maintenance without submitting an emergency change management ticket prior to accessing the PLC
   - While the diagnostic work was authorized and justified by operational needs, the process violated standard operating procedures for emergency change requests
   - This is a **procedural policy violation**, not a security incident

### 6.3 Confidence Level

**Confidence**: **High (95%+)**

**Confidence Justification**:
- All evidence sources (SSH session logs, SCADA logs, change management records, interviews, EDR telemetry) **corroborate** the emergency maintenance narrative
- **No contradictions** detected across multiple independent evidence sources
- Technical evidence (read-only commands, PLC integrity verification) **definitively rules out** malicious activity
- Personnel interviews demonstrate **high credibility** (John acknowledged policy violation without prompting, operations manager confirmed emergency request)
- Alternative hypotheses (unauthorized access, false positive) **conclusively rejected** based on overwhelming evidence

**Remaining Uncertainty**:
- Minimal uncertainty (<5%) stems from inability to verify 100% of SCADA log context (relying on operations team's representation of chlorine dosing fluctuation severity)
- This uncertainty does not materially affect the BTP disposition determination

---

## 7. Impact Assessment

### 7.1 Security Impact

**Assessment**: **No Security Impact**

**Analysis**:
- **No Unauthorized Access**: Access was performed by authorized personnel (John Smith) using authorized credentials (svc_plc_maint)
- **No Malicious Activity**: SSH session logs confirm only diagnostic commands; no configuration changes, no malware, no lateral movement
- **No Data Exfiltration**: No evidence of sensitive data transfer or unauthorized information disclosure
- **No Compromise Indicators**: Source workstation (MAINT-WS-003) shows no signs of compromise (EDR clean, antivirus clean, patch compliant)
- **No Persistence Mechanisms**: No backdoors, no unauthorized accounts created, no malicious scheduled tasks

**Conclusion**: This incident posed **no security risk** to the organization.

### 7.2 Operational Impact

**Assessment**: **Positive Operational Impact**

**Analysis**:
- **Prevented Water Quality Issues**: Emergency diagnostic identified analog input module drift causing chlorine dosing fluctuations
- **Avoided Regulatory Compliance Risk**: Chlorine dosing variance (±0.3 ppm) could have triggered regulatory alarms; timely intervention prevented this
- **Minimized Downtime**: Remote diagnostic prevented need for on-site emergency response or system shutdown
- **Identified Maintenance Need**: Sensor replacement scheduled for next maintenance window (2025-11-15) to prevent recurrence

**Conclusion**: John Smith's emergency diagnostic **prevented a larger operational incident** and demonstrated effective incident response.

### 7.3 Compliance Impact

**Assessment**: **Minor Policy Violation**

**Analysis**:
- **Policy Violated**: Unscheduled Maintenance Policy requires emergency change management tickets to be submitted **prior** to performing work
- **Compliance Status**: Violation acknowledged by John Smith and documented in retroactive change ticket (CM-2025-1142)
- **Management Action**: Operations manager approved retroactive ticket and reminded facilities team of emergency change request procedures
- **Regulatory Impact**: None - no external regulatory compliance violations (e.g., NERC CIP, EPA water quality standards)

**Conclusion**: Minor **internal policy violation** with corrective action taken (procedural reminder). No external compliance impact.

---

## 8. Recommendations

### 8.1 Immediate Actions (Completed)

1. ✅ **Retroactive Change Management Documentation**
   - Change ticket CM-2025-1142 created and approved
   - Work performed documented with justification for emergency diagnostic
   - Policy violation acknowledged

2. ✅ **Sensor Replacement Scheduling**
   - Chlorine sensor (analog input channel 5) scheduled for replacement during next maintenance window (2025-11-15 02:00-06:00)
   - Preventive maintenance to avoid recurrence of dosing fluctuations

3. ✅ **PLC Configuration Integrity Verification**
   - Configuration snapshots compared (pre/post incident)
   - No unauthorized changes detected
   - Integrity confirmed

### 8.2 Short-Term Actions (Recommended)

1. **Procedural Reminder to Facilities Engineering Team**
   - Remind all automation engineers of emergency change request procedures
   - Emphasize that emergency change tickets should be submitted **prior** to performing unscheduled work, even for read-only diagnostics
   - Provide quick-reference guide for emergency change request submission (target: <5 minutes to submit)
   - **Responsible**: Facilities Engineering Manager
   - **Timeline**: Within 1 week

2. **Emergency Change Request Process Review**
   - Evaluate current emergency change request workflow for barriers to rapid submission
   - Consider streamlined emergency ticket process for critical operational incidents (e.g., mobile app, automated ticket creation via phone call)
   - **Responsible**: Change Management Team + Facilities Engineering
   - **Timeline**: Within 30 days

3. **User Education**
   - Provide John Smith with positive feedback on technical response (effective diagnostic, prevented operational incident)
   - Clarify emergency change request expectations for future incidents
   - **Responsible**: Facilities Engineering Manager
   - **Timeline**: Within 1 week

### 8.3 Long-Term Actions (Recommended)

1. **Claroty Alert Tuning**
   - Review Claroty baseline policies for emergency maintenance scenarios
   - Consider creating exception process for authorized emergency diagnostics with retroactive documentation
   - Reduce alert fatigue while maintaining security monitoring effectiveness
   - **Responsible**: Security Operations + OT Security Team
   - **Timeline**: Within 90 days

2. **Preventive Maintenance Review**
   - Analyze chlorine dosing system for recurring sensor drift issues
   - Consider implementing predictive maintenance for analog input modules (sensor health monitoring)
   - Reduce frequency of emergency diagnostics through proactive sensor replacement
   - **Responsible**: Water Treatment Operations + Facilities Engineering
   - **Timeline**: Within 90 days

### 8.4 No Escalation Required

**Security Escalation**: **NOT REQUIRED**
- No security incident occurred
- No unauthorized access or malicious activity detected
- No threat to confidentiality, integrity, or availability of OT systems

**Incident Response**: **NOT REQUIRED**
- No forensic investigation needed
- No containment actions required
- No remediation needed beyond procedural reminder

**Regulatory Reporting**: **NOT REQUIRED**
- No NERC CIP violations (authorized access by authorized personnel)
- No EPA water quality violations (chlorine dosing fluctuations contained)
- No external regulatory reporting obligations

---

## 9. Lessons Learned

### 9.1 What Went Well

1. **Effective Operational Response**: John Smith's rapid diagnostic response prevented a potential water quality compliance incident
2. **Technical Competence**: Diagnostic approach was methodical and effective (identified sensor drift as root cause)
3. **Transparency**: John Smith proactively acknowledged policy violation and documented work retroactively
4. **Management Support**: Operations manager approved retroactive change ticket and provided operational context
5. **Security Monitoring Effectiveness**: Claroty alert correctly identified unscheduled access, demonstrating effective OT security monitoring

### 9.2 What Could Be Improved

1. **Emergency Change Request Submission**: John Smith should have submitted emergency change ticket **prior** to accessing PLC, even for urgent diagnostics
2. **Process Awareness**: Automation engineers may not be fully aware of emergency change request procedures for read-only diagnostics
3. **Workflow Friction**: Current emergency change request process may create barriers to rapid response in time-critical operational emergencies

### 9.3 Systemic Insights

1. **Policy vs. Operational Reality**: Tension exists between strict change management policies and real-world operational emergencies requiring immediate action
2. **Risk-Based Approach Needed**: Differentiate between high-risk changes (configuration modifications) and low-risk diagnostics (read-only access) in emergency change policies
3. **Security-Operations Collaboration**: Effective incident investigation requires close collaboration between security analysts and operational personnel to understand OT context

---

## 10. Conclusion

This investigation comprehensively analyzed a Claroty ICS alert triggered by unscheduled SSH access to a critical water treatment PLC. Through systematic evidence collection (SSH session logs, change management records, personnel interviews, PLC integrity verification), this investigation determined the incident was a **Benign True Positive (BTP)** - authorized emergency maintenance that violated policy procedures but posed no security risk.

**Key Conclusions**:
- **No Security Incident**: No unauthorized access, no malicious activity, no compromise indicators
- **Operational Emergency Justified**: Chlorine dosing fluctuations required immediate diagnostic intervention
- **Policy Violation Acknowledged**: Unscheduled maintenance performed without prior emergency change request
- **Positive Operational Outcome**: Emergency diagnostic prevented water quality compliance issues
- **Corrective Actions Taken**: Retroactive documentation, procedural reminder to facilities team

**No security escalation required.** Incident closed as Benign True Positive with recommendations for process improvement.

---

## Appendices

### Appendix A: Evidence References

- **SSH Session Logs**: `/var/log/ssh/plc-172.16.5.20-20251108.log` (14:15:32 - 15:02:18 EST)
- **Firewall Logs**: Palo Alto firewall logs (VLAN 50 → VLAN 5 traffic, 2025-11-08 14:15-15:05)
- **SCADA Logs**: Wonderware SCADA historian logs (chlorine dosing trends, 2025-11-08 13:00-16:00)
- **Change Management Ticket**: CM-2025-1142 (retroactive emergency maintenance documentation)
- **PLC Configuration Snapshots**: Pre-incident (2025-10-28 03:15:42) vs. Post-incident (2025-11-08 16:00:00)
- **Interview Transcripts**: John Smith (2025-11-08 17:00 EST), Operations Manager (2025-11-08 17:30 EST)

### Appendix B: Technical Command Log

**Excerpt from SSH session log** (sanitized for readability):

```
[14:15:35] svc_plc_maint logged in from 10.50.10.45
[14:17:02] plc-cli show ladder-logic --program ChlorineDosing
[14:18:15] plc-cli show io-status --module AnalogInput-Slot3
[14:19:30] plc-cli show analog-input --channel 5 --history 2h
[14:22:45] plc-cli show system-info
[14:25:10] plc-cli export-diagnostics --output /tmp/plc-diag-2025-11-08.log
[14:30:00] plc-cli show alarm-history --timeframe 24h
[14:35:15] plc-cli show network-config
[15:02:18] svc_plc_maint logged out
```

**Analysis**: All commands are read-only diagnostic commands. No write operations, no configuration changes, no unauthorized access attempts.

### Appendix C: Disposition Confidence Matrix

| Evidence Type | Supports BTP | Supports Malicious | Weight | Assessment |
|---------------|--------------|-------------------|--------|------------|
| SSH Session Logs | ✓ (read-only commands) | ✗ | High | BTP |
| PLC Integrity Check | ✓ (no changes) | ✗ | High | BTP |
| Change Management | ✓ (retroactive approval) | ✗ | Medium | BTP |
| Personnel Interviews | ✓ (credible, corroborated) | ✗ | High | BTP |
| SCADA Logs | ✓ (operational emergency) | ✗ | Medium | BTP |
| EDR Telemetry | ✓ (clean) | ✗ | Medium | BTP |
| Service Account Usage | ✓ (authorized) | ✗ | Medium | BTP |
| **Overall Confidence** | **High (95%+)** | **None** | - | **BTP** |

---

**Investigation Status**: COMPLETE
**Ticket Status**: Ready for Review
**Next Action**: Close incident as Benign True Positive, implement short-term recommendations

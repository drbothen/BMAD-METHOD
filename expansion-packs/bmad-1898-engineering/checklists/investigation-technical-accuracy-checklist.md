# Investigation Technical Accuracy Checklist

**Weight:** 20%
**Purpose:** Verify factual correctness and technical validity of all technical claims and analysis.

## Check Items

- [ ] **IP Addresses and Network Identifiers Correct** - No typos, valid IP ranges, correct subnet notation, hostnames resolve correctly
- [ ] **Protocol and Port Information Accurate** - Correct protocol names (TCP/UDP/ICMP), valid port ranges (1-65535), standard services identified correctly
- [ ] **Alert Signature/Rule Correctly Identified** - Rule ID matches platform documentation, alert description accurate, detection logic understood
- [ ] **Technical Terminology Used Correctly** - Security terms used appropriately (e.g., lateral movement, C2, exfiltration), no misuse of technical jargon
- [ ] **Log Excerpts Interpreted Correctly** - Log fields parsed accurately, timestamps interpreted correctly, log format understood
- [ ] **Attack Vectors Described Accurately** - Attack scenarios technically feasible, attack chain logically sound, threat actor TTPs realistic
- [ ] **No Contradictions Between Evidence and Conclusions** - All claims supported by evidence, no logical inconsistencies, disposition matches evidence

## Scoring

- **Total Items:** 7
- **Passed Items:** [count after review]
- **Score:** (Passed / 7) × 100 = \_\_\_\_%

## Guidance

### Verification Procedures

**IP Address Validation:**

- IPv4 format: 0-255.0-255.0-255.0-255 (e.g., 10.50.1.100 ✓, 192.168.1.256 ✗)
- Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
- Public vs. private correctly identified
- CIDR notation correct (e.g., /24 = 255.255.255.0)

**Protocol/Port Validation:**

- Common services: SSH (22/TCP), HTTP (80/TCP), HTTPS (443/TCP), DNS (53/UDP), RDP (3389/TCP)
- Protocol/port mismatch detected (e.g., "HTTP on port 22" is likely wrong)
- Ephemeral ports (49152-65535) identified correctly

**Alert Rule Verification:**

- Rule ID matches alert platform documentation
- Alert description matches observed behavior
- Detection logic understood (not just copied from alert text)

**Technical Terminology Standards:**

- Lateral movement: Post-compromise movement between systems (not initial access)
- C2 (Command & Control): Attacker-controlled infrastructure for managing compromised systems
- Exfiltration: Unauthorized data transfer out of network
- Pivoting: Using compromised system as proxy to access other systems
- Reconnaissance: Information gathering phase (not exploitation)

### Examples

#### Example 1: Technically Accurate Analysis

```
Alert Rule: SSH_Unusual_Destination_V2 (Rule ID: 4782)
Source: 10.50.1.100:54321 (jump-server-01.corp.local) - TCP ephemeral port
Destination: 10.10.5.25:22 (file-server-backup.corp.local) - SSH port

Protocol Analysis:
- TCP three-way handshake observed (SYN → SYN-ACK → ACK)
- SSH version 2 protocol negotiation (OpenSSH_8.9p1)
- Public key authentication (RSA 2048-bit key)

Log Excerpt (SSH auth.log on 10.10.5.25):
Nov 09 14:30:00 file-server-backup sshd[12345]: Accepted publickey for backup_user from 10.50.1.100 port 54321 ssh2: RSA SHA256:aa:bb:cc:dd:ee:ff

Interpretation:
- Authentication successful using RSA public key
- Key fingerprint: SHA256:aa:bb:cc:dd:ee:ff
- User: backup_user (authorized service account)
- Source port: 54321 (ephemeral range 49152-65535, normal for client connections)
```

**Accuracy Check:**
✓ IP addresses valid and correctly formatted
✓ Ports correct (22 = SSH standard port, 54321 = valid ephemeral)
✓ Protocol correct (TCP for SSH, SSH version 2)
✓ Log format correct (standard syslog format with OpenSSH fields)
✓ Terminology correct (public key authentication, RSA, fingerprint)
✓ No contradictions (all evidence supports authorized connection)

**Accuracy Score:** 7/7 = 100%

---

#### Example 2: Technically Inaccurate Analysis

```
Alert: Suspicious SSH Activity
Source: 192.168.1.256 (attacker-server)
Destination: 10.50.1.100:22 (jump-server)

Protocol: UDP/22 (SSH)

Analysis:
The attacker is using lateral movement from 192.168.1.256 to pivot through the jump server and exfiltrate data via SSH tunneling. This is a classic C2 technique seen in APT campaigns.

Evidence:
Log shows "Failed password for root" indicating brute force attack in progress.

Conclusion: This is active exploitation attempting to establish persistent C2 backdoor.
```

**Accuracy Errors Detected:**

1. **IP Address Invalid:** 192.168.1.256 (octet 256 exceeds valid range 0-255) ✗
2. **Protocol Incorrect:** "UDP/22 (SSH)" - SSH uses TCP, not UDP ✗
3. **Terminology Misuse:**
   - "Lateral movement" - This is initial access attempt, not lateral movement (requires prior compromise) ✗
   - "Pivot" - No evidence of pivoting, this is direct connection attempt ✗
   - "Exfiltrate data" - Failed authentication attempt doesn't exfiltrate data ✗
   - "C2 technique" - Brute force is not C2, C2 requires established connection ✗
4. **Evidence Contradiction:** Log shows "Failed password" (authentication failed), but conclusion says "active exploitation" and "persistent backdoor" (implies success) ✗
5. **Attack Vector Inaccurate:** Brute force ≠ exploitation; backdoor requires successful compromise ✗

**Accuracy Score:** 0/7 = 0% (Inadequate)

---

### Common Technical Errors

**IP Address Errors:**

- Typos: 10.50.1.1OO (O instead of 0)
- Invalid octets: 192.168.1.300 (>255)
- Incorrect subnet masks: /33 (>32)
- Public/private confusion: Calling 10.x.x.x "external"

**Protocol/Port Errors:**

- SSH over UDP (SSH is TCP-only)
- HTTP on port 22 (likely SSH, not HTTP)
- "Port 443/UDP" for HTTPS (HTTPS is TCP)
- Impossible port: 99999 (max 65535)

**Log Interpretation Errors:**

- Timestamp confusion (UTC vs. local time)
- Field misidentification (source IP as destination)
- Status code misinterpretation (200 = success, 404 = not found)
- Log level confusion (INFO vs. ERROR)

**Terminology Errors:**

- "Lateral movement" for initial access
- "Exploit" for brute force
- "C2" for any outbound connection
- "Exfiltration" for normal data transfer
- "APT" without attribution evidence

### Weighting Rationale

**Why 20% (Second Highest Weight)?**

Technical inaccuracies undermine all conclusions. An investigation with incorrect IP addresses, wrong protocols, or misinterpreted logs cannot produce reliable dispositions, regardless of how complete or well-documented it is.

**Impact of Technical Errors:**

- Wrong IPs → Can't identify assets or validate claims
- Wrong protocols → Misunderstand attack vectors or miss legitimate activity
- Misinterpreted logs → Wrong evidence, wrong conclusions
- Terminology misuse → Miscommunication, incorrect escalation

**Severity Classification:**

**Critical Errors (Investigation Invalid):**

- IP address typos preventing asset identification
- Protocol errors changing attack vector assessment
- Log misinterpretation reversing disposition (FP ↔ TP)

**Moderate Errors (Investigation Questionable):**

- Terminology misuse causing confusion
- Minor contradictions between evidence sections

**Minor Errors (Investigation Acceptable):**

- Formatting inconsistencies
- Redundant technical details

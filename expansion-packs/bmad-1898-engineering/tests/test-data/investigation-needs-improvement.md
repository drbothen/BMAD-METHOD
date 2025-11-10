# Event Investigation Report: IDS Alert - Exploit Attempt

**Ticket ID**: AOD-5123
**Investigation Date**: 2025-11-09
**Investigator**: Security Analyst
**Alert Type**: Signature-Based Detection
**Severity**: Critical

---

## Executive Summary

This investigation looked at a Snort IDS alert for an Apache Struts exploit attempt. The attack came from a suspicious IP address and tried to exploit CVE-2017-5638. The server returned HTTP 500 errors so the attack probably didn't work. Disposition is False Positive because the exploit failed.

---

## Alert Overview

**Alert Source**: Snort IDS
**Alert ID**: SNORT-2025-110909-EXP-042
**Detection Time**: 2025-11-09 09:45:18 EST
**Signature**: ET EXPLOIT Apache Struts OGNL Injection Attempt

Snort detected a packet matching the Apache Struts OGNL injection signature. The attack targeted our customer portal server at 203.45.67.89.

---

## Network Details

**Source:**
- IP: 185.220.101.47
- Location: Netherlands
- This IP is on some blocklists

**Destination:**
- IP: 203.45.67.89
- Server: webserver-prod-03
- Running: Apache Tomcat with Struts 2.3.32

---

## Timeline

- 09:45:18 - Attack attempt #1
- 09:45:22 - Attack attempt #2
- 09:45:30 - Attack attempt #3
- 09:45:31 - Firewall blocked the IP

---

## Evidence

The HTTP requests had malicious OGNL code in the Content-Type header trying to execute "whoami" command. The server returned HTTP 500 errors which means the exploit didn't work.

Checked the web server and didn't see any suspicious activity. No weird processes running. The firewall automatically blocked the attacker's IP address.

---

## Disposition

**Disposition: False Positive**

**Reasoning:**
The attack failed because the server returned HTTP 500 errors instead of HTTP 200. HTTP 500 means internal server error, so the exploit didn't execute successfully. Since nothing bad happened, this is a false positive.

**Confidence: Medium**

---

## Impact

No impact because the attack failed. The firewall blocked the IP so they can't try again.

---

## Recommendations

1. Keep the firewall blocking that IP address
2. Monitor the server for any issues
3. Consider patching the server when convenient

---

## Conclusion

This was an attempted Apache Struts exploit that failed. The server returned errors and the firewall blocked the attacker. No further action needed besides monitoring.

**Investigation Status**: COMPLETE

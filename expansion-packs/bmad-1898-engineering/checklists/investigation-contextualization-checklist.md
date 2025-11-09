# Investigation Contextualization Checklist

**Weight:** 15%
**Purpose:** Verify business and operational context integration into risk assessment and disposition.

## Check Items

- [ ] **Asset Criticality Assessed** - Critical/High/Medium/Low criticality level assigned with justification
- [ ] **Business Impact Evaluated** - Potential consequences of security incident described (financial, operational, reputational)
- [ ] **Affected Systems/Services Identified** - Downstream dependencies, connected systems, or services impacted by asset noted
- [ ] **Risk Level Determined Based on Context** - Risk assessment combines alert severity with asset criticality and business impact (not just severity alone)
- [ ] **Client/Customer Impact Considered** - External impact to clients, customers, or partners assessed (if applicable)
- [ ] **SLA/Compliance Implications Noted** - Regulatory, contractual, or compliance requirements identified (e.g., PCI-DSS, HIPAA, SOC2, SLA thresholds)
- [ ] **Environmental Factors Explained** - Context such as test vs. production, maintenance windows, scheduled changes, or known operational events documented

## Scoring

- **Total Items:** 7
- **Passed Items:** [count after review]
- **Score:** (Passed / 7) × 100 = ____%

## Guidance

### Asset Criticality Levels

**Critical Assets:**
- Business-critical production systems (revenue-generating applications, core infrastructure)
- Systems containing highly sensitive data (PII, financial data, intellectual property, credentials)
- Single points of failure (no redundancy)
- Safety-critical systems (ICS/OT controlling physical processes)
- Executive/privileged user workstations
- Examples: Domain controllers, customer database servers, payment processing systems, SCADA HMI

**High Criticality Assets:**
- Important production systems with some redundancy
- Systems containing sensitive but not critical data
- Key operational systems (but not single points of failure)
- Examples: Application servers, file servers, network infrastructure, VPN gateways

**Medium Criticality Assets:**
- Standard production systems with full redundancy
- Development/staging environments
- General user workstations
- Non-critical data storage
- Examples: Web servers (behind load balancer), department file shares, developer laptops

**Low Criticality Assets:**
- Test/lab systems
- Decommissioned or unused systems
- Isolated non-production environments
- Examples: Sandbox VMs, test databases, training environments

### Business Impact Assessment

**Questions to Answer:**
1. What business function does this asset support?
2. What happens if this asset is compromised or unavailable?
3. Who is affected? (internal teams, customers, partners)
4. What is the financial impact? (revenue loss, regulatory fines, remediation costs)
5. What is the operational impact? (service outage, productivity loss, manual workarounds)
6. What is the reputational impact? (customer trust, brand damage, media coverage)

**Impact Levels:**

**High Business Impact:**
- Revenue loss >$100k/hour
- Service outage affecting >1000 users or all customers
- Data breach requiring regulatory notification
- Safety risk (ICS/OT environments)
- Example: E-commerce platform down during peak shopping hours

**Medium Business Impact:**
- Revenue loss $10k-$100k/hour
- Service degradation affecting 100-1000 users
- Sensitive data exposure (but not PII/financial)
- Example: Internal CRM system slow or unavailable

**Low Business Impact:**
- Revenue loss <$10k/hour
- Service outage affecting <100 users
- No sensitive data exposure
- Example: Test environment compromised

### Context Integration Examples

#### Example 1: Well-Contextualized Investigation

```
**Asset Context:**
- Source Asset: jump-server-01.corp.local (10.50.1.100)
  - Criticality: Critical (single point of access for administrative operations)
  - Asset Type: Bastion host / jump server
  - Owner: IT Operations team
  - Business Function: Provides secure administrative access to production infrastructure

- Destination Asset: file-server-backup.corp.local (10.10.5.25)
  - Criticality: High (backup infrastructure, business continuity)
  - Asset Type: File server (backup storage)
  - Owner: IT Operations team
  - Business Function: Stores automated backups for 50+ production systems

**Business Impact Assessment:**
- Potential Impact if True Positive (unauthorized access):
  - Jump server compromise = attacker access to ALL production systems (lateral movement risk)
  - Backup server compromise = data exfiltration risk (backups contain sensitive data), ransomware risk (attacker could delete backups)
  - Estimated impact: $500k+ (incident response, forensics, potential data breach notification)

- Potential Impact if False Positive (alert noise):
  - Low (alert tuning reduces noise, improves analyst efficiency)

**Affected Systems/Services:**
- Jump server provides access to: 150+ production servers, network devices, database servers
- Backup server stores: Customer data backups, financial system backups, HR system backups
- Downstream dependencies: Backup failure impacts disaster recovery capability (RTO/RPO at risk)

**Risk Assessment:**
- Alert Severity: High (Claroty rule set to High)
- Asset Criticality: Critical (jump server) + High (backup server)
- Business Impact: High (potential compromise of critical infrastructure)
- **Combined Risk Level:** Critical (High severity × Critical assets = Maximum risk)
- **Decision:** Despite evidence supporting False Positive, the critical nature of assets warrants peer review before closing

**Client/Customer Impact:**
- Direct customer impact: None (internal administrative activity)
- Indirect customer impact: If TP, potential data breach affecting 50,000+ customers (backup data compromise)

**SLA/Compliance Implications:**
- Compliance: SOC2 Type II (access logging required, suspicious activity must be investigated)
- SLA: Backup SLA guarantees 24-hour recovery point objective (RPO) - backup server availability critical
- Regulatory: No PII/PHI in these systems (not GDPR/HIPAA regulated)

**Environmental Factors:**
- Environment: Production (both assets)
- Timing: 02:00 UTC = Outside business hours (consistent with maintenance window 00:00-04:00 UTC)
- Scheduled Activity: IT Ops confirmed daily backup schedule at 02:00 UTC (recurring calendar event)
- Recent Changes: No recent changes to jump server or backup server (change management system checked)
```

**Contextualization Score:** 7/7 = 100%

---

#### Example 2: Poor Contextualization

```
Alert: Suspicious SSH Activity
Source: 10.50.1.100
Destination: 10.10.5.25

Investigation: This is SSH traffic between two internal servers. Looks normal.

Disposition: False Positive
```

**Missing Context:**
✗ Asset criticality not assessed (are these critical systems or test boxes?)
✗ Business impact not evaluated (what happens if compromised?)
✗ Affected systems not identified (what depends on these assets?)
✗ Risk level not determined (severity + context)
✗ Client/customer impact not considered
✗ SLA/compliance not noted
✗ Environmental factors not explained (prod vs. test? maintenance window?)

**Contextualization Score:** 0/7 = 0% (Inadequate)

---

### Context-Driven Disposition Examples

**Scenario 1: Same Technical Evidence, Different Context → Different Disposition**

**Case A: Test Environment**
```
Alert: SQL Injection Attempt
Target: 10.100.50.25 (test-db-server.lab.local)
Evidence: SELECT * FROM users WHERE id='1' OR '1'='1'

Context:
- Asset Criticality: Low (test environment)
- Business Impact: None (isolated lab, no production data)
- Environment: Test/development
- Recent Activity: Developers running security testing (confirmed via calendar)

Disposition: False Positive (authorized security testing)
Escalation: No escalation needed
Next Actions: No action required (expected activity in test environment)
```

**Case B: Production Environment**
```
Alert: SQL Injection Attempt
Target: 10.10.20.25 (customer-db-prod.corp.local)
Evidence: SELECT * FROM users WHERE id='1' OR '1'='1'

Context:
- Asset Criticality: Critical (production customer database)
- Business Impact: High (contains PII for 100,000 customers, PCI-DSS scope)
- Environment: Production
- SLA/Compliance: PCI-DSS 3.2.1 (security incident must be reported within 24h)
- Client Impact: Potential data breach affecting all customers

Disposition: True Positive (SQL injection attack on production database)
Escalation: IMMEDIATE escalation to Incident Response team
Next Actions:
1. Isolate affected database server (coordinate with DBA team)
2. Collect forensic evidence (full packet capture, database logs, WAF logs)
3. Initiate PCI-DSS incident response procedures
4. Notify CISO and legal team (potential breach notification requirement)
```

**Same technical evidence, completely different disposition and response due to context**

---

### Common Contextualization Failures

**Failure 1: Treating All Assets Equally**
```
Disposition: False Positive (SSH traffic is normal)
```
❌ No consideration of asset criticality (domain controller vs. test VM have very different risk profiles)

**Failure 2: Ignoring Business Impact**
```
Disposition: True Positive (malicious activity detected)
Next Actions: Close ticket
```
❌ If TP, why close? Business impact not assessed, so severity of response unclear

**Failure 3: Missing Compliance Requirements**
```
Investigation: Brute force attack detected on login server
Disposition: False Positive (login attempts from authorized IP range)
```
❌ Even if FP, compliance may require logging/reporting of brute force attempts (e.g., PCI-DSS 10.2.4)

**Failure 4: Not Checking Maintenance Windows**
```
Alert: Unusual administrative activity at 02:00 AM
Disposition: True Positive (suspicious timing)
```
❌ Didn't check if 02:00 AM is scheduled maintenance window (common for backups, patching)

**Failure 5: Ignoring Environment**
```
Alert: Port scan detected from 10.50.1.100
Disposition: True Positive (reconnaissance activity)
Escalation: Immediate escalation
```
❌ Didn't check if source is authorized vulnerability scanner in development environment

### Weighting Rationale

**Why 15% (Third Highest Weight)?**

Context transforms technical findings into business decisions. The same alert on a test system vs. production database requires completely different responses. Without context:
- Low-risk events get over-escalated (wasted resources)
- High-risk events get under-escalated (missed incidents)
- Compliance violations go undetected (regulatory fines)
- Business impact not communicated (poor stakeholder decisions)

**Context Determines:**
- Escalation urgency (Critical asset = faster response)
- Investigation depth (High impact = deeper investigation)
- Notification requirements (Compliance triggers reporting)
- Resource allocation (Critical systems get priority)

**Quality Thresholds:**

**Excellent (6-7/7):** Full business context integrated, risk-based decision making
**Good (5/7):** Key context captured, reasonable risk assessment
**Needs Improvement (3-4/7):** Some context missing, incomplete risk picture
**Inadequate (<3/7):** Context ignored, technical analysis only

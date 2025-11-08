# Epic 4: Security Analysis Knowledge Base & Reference Materials

## Epic Goal

Provide comprehensive reference materials and knowledge bases to support Security Analyst and Security Reviewer agents in performing consistent, high-quality vulnerability enrichment and quality assurance.

## Background

BMAD-1898 Engineering expansion pack provides AI-assisted security vulnerability enrichment and systematic peer review for organizations managing 50,000+ annual CVE disclosures. To ensure consistent analysis quality and reduce cognitive biases, analysts need:

1. **Standardized vulnerability management frameworks** - Understanding of CVSS, EPSS, KEV, and multi-factor risk assessment
2. **Cognitive bias awareness** - Ability to recognize and mitigate systematic analysis errors
3. **ATT&CK mapping guidance** - Consistent mapping of vulnerabilities to adversary tactics and techniques

These knowledge bases enable:
- 90% faster CVE enrichment with consistent quality
- Systematic QA review detecting 60-70% more defects
- Reduced cognitive bias through self-awareness and structured workflows
- Standardized security analysis across team members

## Integration Context

**Security Analyst Agent** (Story 1.1) uses these knowledge bases to:
- Perform multi-factor risk assessment (CVSS + EPSS + KEV + Business Context)
- Avoid cognitive biases during analysis
- Map vulnerabilities to MITRE ATT&CK framework

**Security Reviewer Agent** (Story 2.1) uses these knowledge bases to:
- Detect cognitive bias patterns in enrichments
- Verify correct application of vulnerability management frameworks
- Validate MITRE ATT&CK mappings

**Project Configuration** (config.yaml) defines:
- JIRA integration for CVE ticket enrichment
- Custom fields: CVE ID, Affected Systems, Asset Criticality Rating, System Exposure

## Stories

### Story 4.1: Vulnerability Management Knowledge Base

**As a** security analyst,
**I want** comprehensive vulnerability management best practices,
**so that** I understand frameworks like CVSS, EPSS, KEV, ACR.

**Acceptance Criteria:**
1. Knowledge base includes NIST NVD, CVSS, EPSS, KEV, ACR frameworks
2. Industry statistics (2025 CVE volume, alert fatigue data)
3. Remediation approaches explained
4. Multi-factor risk assessment methodology

**Integration Requirements:**
- KB must align with Security Analyst agent's multi-factor priority assessment workflow (Story 1.7)
- Priority framework (P1-P5) must match JIRA integration custom fields
- Referenced by cognitive bias detection checklist (Story 2.4)

---

### Story 4.2: Cognitive Bias Patterns Guide

**As a** security analyst,
**I want** to understand cognitive biases in security analysis,
**so that** I can recognize and avoid systematic errors.

**Acceptance Criteria:**
1. Guide covers 5 bias types with definitions (Confirmation, Anchoring, Availability, Overconfidence, Recency)
2. Real-world examples from security operations
3. Debiasing techniques explained
4. Self-assessment guidance

**Integration Requirements:**
- Examples must reference vulnerability management frameworks from Story 4.1
- Bias patterns must align with Security Reviewer's quality checklist (Story 2.2)
- Debiasing techniques must support systematic review workflow (Story 3.2)

---

### Story 4.3: MITRE ATT&CK Mapping Guide

**As a** security analyst,
**I want** clear guidance on mapping vulnerabilities to MITRE ATT&CK,
**so that** I can accurately identify tactics and techniques.

**Acceptance Criteria:**
1. Common tactics for vulnerability types (Initial Access, Execution, Privilege Escalation, etc.)
2. Common techniques with T-numbers (T1190, T1068, T1059, etc.)
3. Mapping examples using realistic CVE scenarios
4. Detection implications per technique

**Technical Requirements:**
- Tactics/techniques must be relevant to common vulnerability types in enterprise security
- CVE examples should represent realistic scenarios (RCE, SQL injection, privilege escalation, DoS, authentication bypass)
- Detection recommendations must be actionable (specific monitoring, IDS/IPS, log analysis)
- Guide must support Security Analyst enrichment workflow (not full incident response scope)

**Scope Constraints:**
- **IN SCOPE:** Mapping CVEs to ATT&CK for enrichment purposes (understanding attack paths, prioritizing detection)
- **IN SCOPE:** Common techniques for vulnerability exploitation (T1190, T1068, T1059, T1203, T1210, T1133, T1498)
- **IN SCOPE:** Detection implications (what to monitor per technique)
- **OUT OF SCOPE:** Full ATT&CK framework reference (all 14 tactics, 200+ techniques) - focus on vulnerability-relevant subset
- **OUT OF SCOPE:** Advanced persistent threat (APT) campaign mapping - focus on vulnerability exploitation
- **OUT OF SCOPE:** Custom CVEs specific to organization's stack - use generic representative examples

**Integration Requirements:**
- ATT&CK mapping must be referenceable from JIRA enrichment comments (Story 1.5)
- Detection implications must support remediation guidance (Story 4.1 remediation strategies)
- Referenced by Security Reviewer's fact verification checklist (Story 2.5)

## Success Criteria

1. **Knowledge Base Usability:** New analysts can comprehend frameworks within 30 minutes
2. **Bias Awareness:** Analysts can identify 4+ bias types in example scenarios
3. **ATT&CK Mapping Accuracy:** 90%+ agreement between analyst mappings and expert review
4. **Agent Integration:** All knowledge bases successfully referenced by Security Analyst/Reviewer agents

## Technical Implementation

**File Location:** `expansion-packs/bmad-1898-engineering/data/`

**Files to Create:**
- `bmad-kb.md` - Vulnerability management knowledge base (Story 4.1)
- `cognitive-bias-patterns.md` - Cognitive bias guide (Story 4.2)
- `mitre-attack-mapping-guide.md` - ATT&CK mapping guide (Story 4.3)

**Testing Standards:**
- Content accuracy validated against authoritative sources (NIST NVD, FIRST EPSS, CISA KEV, MITRE ATT&CK)
- Comprehension tested with new analysts
- Examples validated for realism and correctness
- All external URLs verified as valid

## Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-11-07 | 1.0 | Initial Epic 4 creation | Sarah (PO) |

## References

- Story 1.1: Security Analyst Agent Creation
- Story 1.5: JIRA Enrichment Comment
- Story 1.7: Multi-Factor Priority Assessment
- Story 2.1: Security Reviewer Agent Creation
- Story 2.2: Systematic Quality Evaluation
- Story 2.4: Cognitive Bias Detection
- Story 2.5: Fact Verification
- Story 3.2: Security Analysis Review Workflow
- config.yaml: JIRA Integration Configuration

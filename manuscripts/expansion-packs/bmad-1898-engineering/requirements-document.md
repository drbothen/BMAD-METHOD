# BMAD-1898: Engineering Expansion Pack

## Requirements Document v1.0

**Prepared by:** Mary (Business Analyst)
**Date:** 2025-11-06
**Project Code:** BMAD-1898 (Project AOD - Security Operations)
**Stakeholder:** Product Owner
**Status:** Draft for Review

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Background](#project-background)
3. [Business Objectives](#business-objectives)
4. [Scope](#scope)
5. [System Architecture Overview](#system-architecture-overview)
6. [Project Directory Structure](#project-directory-structure)
   - [Overview](#overview)
   - [Standard Directory Layout](#standard-directory-layout)
   - [Directory Purpose and Usage](#directory-purpose-and-usage)
   - [Directory Lifecycle and Maintenance](#directory-lifecycle-and-maintenance)
   - [Integration with BMAD-1898 Tasks](#integration-with-bmad-1898-tasks)
   - [Initial Setup Requirements](#initial-setup-requirements)
   - [Benefits of Structured Directory System](#benefits-of-structured-directory-system)
7. [Component Breakdown](#component-breakdown)
   - [Agents](#agents)
   - [Tasks](#tasks)
   - [Templates](#templates)
   - [Checklists](#checklists)
   - [Workflows](#workflows)
   - [Data/Knowledge Bases](#dataknowledge-bases)
   - [Configuration](#configuration)
8. [User Stories & Epics](#user-stories--epics)
9. [Integration Requirements](#integration-requirements)
10. [Quality Standards](#quality-standards)
11. [Success Metrics](#success-metrics)
12. [Dependencies & Prerequisites](#dependencies--prerequisites)
13. [Risk Assessment](#risk-assessment)
14. [Implementation Roadmap](#implementation-roadmap)
15. [Appendices](#appendices)

---

## Executive Summary

This requirements document defines the BMAD-1898 Engineering Expansion Pack, a comprehensive AI-assisted system for enriching security vulnerability tickets and ensuring quality assurance of security analysis work. The expansion pack addresses the critical challenge of managing the 50,000+ annual CVE disclosures while maintaining analyst productivity and reducing alert fatigue.

**Key Deliverables:**

- **2 specialized security agents** (Security Analyst, Security Reviewer)
- **7 focused tasks** for vulnerability research and quality assurance
- **5 professional templates** for structured security reporting
- **8 comprehensive checklists** covering all quality dimensions
- **3 complete workflows** from alert enrichment through remediation
- **6 knowledge bases** for vulnerability management best practices
- **1 expansion pack configuration** for JIRA and Perplexity MCP integration

**Business Impact:**

- **90% faster vulnerability analysis** through AI-assisted research
- **60-70% more defects identified** through structured peer review
- **Reduced alert fatigue** by focusing on CVSS + EPSS + KEV prioritization
- **Enterprise-grade quality** through systematic QA processes

---

## Project Background

### Current Challenge

Security operations teams face unprecedented vulnerability volume, with 2025 CVE disclosures projected to exceed 50,000 globally—an 18% increase over 2024. Security analysts experience severe alert fatigue, with 78% of security alerts going uninvestigated due to overwhelming volume and insufficient context. Traditional vulnerability management approaches that rely solely on CVSS scores fail to distinguish between vulnerabilities posing genuine exploitable threats and those representing theoretical risks with minimal practical impact.

### Existing Process (As-Is)

Currently, Project AOD security analysts manually:

1. Read JIRA security alert tickets with minimal context
2. Research CVE details across multiple sources (NVD, CISA, vendor sites)
3. Copy/paste fragmented information into JIRA comments
4. Apply inconsistent priority frameworks
5. Lack systematic quality assurance or peer review
6. Miss critical enrichment factors (EPSS, KEV, MITRE ATT&CK)

**Result:** Inconsistent analysis quality, slow enrichment cycles (hours per ticket), missed critical vulnerabilities, and inability to scale with growing alert volumes.

### Proposed Solution (To-Be)

The BMAD-1898 expansion pack transforms vulnerability management through:

- **AI-Assisted Research:** Leverage Perplexity MCP for comprehensive CVE intelligence gathering
- **Structured Enrichment:** Standardized templates ensuring complete analysis coverage
- **Multi-Dimensional Prioritization:** CVSS + EPSS + KEV + Business Context = Accurate Risk
- **Systematic QA:** Peer review workflows with cognitive bias detection
- **JIRA Integration:** Seamless workflow from enrichment through remediation tracking

**Result:** 90% faster enrichment, enterprise-grade quality assurance, risk-based prioritization, and scalability to handle 50,000+ annual CVEs.

---

## Business Objectives

### Primary Objectives

1. **Accelerate Vulnerability Analysis**
   - Reduce enrichment time from hours to minutes (10-15 min target)
   - Enable analysts to process 5-10x more alerts per day
   - Achieve 90% reduction in manual research time

2. **Improve Analysis Quality**
   - Implement structured peer review identifying 60-70% more gaps
   - Eliminate cognitive biases through systematic review checklists
   - Ensure 100% coverage of required enrichment factors (CVSS, EPSS, KEV, ATT&CK)

3. **Enable Risk-Based Prioritization**
   - Shift from CVSS-only to multi-factor risk assessment
   - Integrate CISA KEV catalog for active exploitation visibility
   - Incorporate EPSS exploitation probability scores
   - Apply business context through Asset Criticality Ratings

4. **Reduce Alert Fatigue**
   - Focus remediation on genuinely exploitable threats
   - Provide clear, actionable remediation guidance
   - Eliminate noise from low-risk theoretical vulnerabilities

5. **Scale Security Operations**
   - Support 50,000+ annual CVE volume
   - Maintain quality despite increasing alert volumes
   - Enable continuous improvement through metrics tracking

### Secondary Objectives

- Establish vulnerability management best practices knowledge base
- Create reusable MITRE ATT&CK mapping procedures
- Build organizational security analysis competency
- Enable compliance reporting and audit trail documentation

---

## Scope

### In Scope

**Functional Requirements:**

- AI-assisted CVE research using Perplexity MCP
- Structured vulnerability enrichment workflows
- JIRA ticket integration (reading, commenting, custom fields)
- Multi-dimensional priority assessment (CVSS + EPSS + KEV + ACR)
- MITRE ATT&CK technique mapping
- Systematic peer review and QA processes
- Cognitive bias detection in security analysis
- Remediation guidance creation
- Business impact assessment
- Exploit intelligence gathering
- Compensating controls identification

**Technical Requirements:**

- Integration with Atlassian MCP (JIRA Cloud)
- Integration with Perplexity MCP (search, reason, deep_research)
- BMAD framework agent system
- Template-driven document generation
- Checklist-based quality assurance
- Workflow orchestration

**Documentation Requirements:**

- Agent definitions (2 agents)
- Task procedures (7 tasks)
- Templates (5 templates)
- Quality checklists (8 checklists)
- Workflows (3 workflows)
- Knowledge bases (6 knowledge bases)
- Expansion pack configuration
- User guide and README

### Out of Scope (Future Enhancements)

- Automated vulnerability scanning (use existing scanners)
- Patch deployment automation (use existing tools)
- Custom JIRA app/plugin development (use MCP integration)
- Multi-tenant/SaaS deployment
- Non-JIRA ticketing systems (Jira only for v1.0)
- Vulnerability scanning tool integration beyond JIRA
- Automated remediation execution
- Real-time threat feed integration beyond Perplexity
- Mobile application support

### Success Criteria

**Must Have (MVP):**

- ✅ Security Analyst agent enriches tickets using Perplexity research
- ✅ Security Reviewer agent performs systematic QA reviews
- ✅ All 8 quality dimensions covered by checklists
- ✅ JIRA integration functional (read/write tickets, comments, custom fields)
- ✅ CVSS + EPSS + KEV + Business Context priority framework
- ✅ MITRE ATT&CK mapping procedure
- ✅ Structured enrichment template
- ✅ Complete review report template

**Should Have (v1.1):**

- Automated metrics tracking and reporting
- Dashboard templates for vulnerability trends
- Integration with additional threat intelligence sources
- Automated enrichment for low-severity alerts
- Bulk enrichment capabilities

**Could Have (v2.0):**

- Machine learning-based priority prediction
- Custom CVSS calculator integration
- Automated MITRE ATT&CK mapping using AI
- Integration with SOAR platforms

---

## System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    BMAD-1898 Expansion Pack                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────┐         ┌──────────────────────┐         │
│  │ Security Analyst  │────────▶│  Perplexity MCP      │         │
│  │ Agent             │         │  (CVE Research)      │         │
│  └─────────┬─────────┘         └──────────────────────┘         │
│            │                                                     │
│            │ enriches                                            │
│            ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐        │
│  │            JIRA Security Alert Ticket                │        │
│  │  ┌──────────────────────────────────────────────┐   │        │
│  │  │ Enrichment Comment (structured markdown)     │   │        │
│  │  ├──────────────────────────────────────────────┤   │        │
│  │  │ Custom Fields (CVSS, EPSS, KEV, Priority)    │   │        │
│  │  └──────────────────────────────────────────────┘   │        │
│  └─────────┬───────────────────────────────────────────┘        │
│            │                                                     │
│            │ reviews                                             │
│            ▼                                                     │
│  ┌───────────────────┐         ┌──────────────────────┐         │
│  │ Security Reviewer │────────▶│  Perplexity MCP      │         │
│  │ Agent             │         │  (Fact Checking)     │         │
│  └───────────────────┘         └──────────────────────┘         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
           │                                      │
           ▼                                      ▼
    Atlassian MCP                          BMAD Core Framework
    (JIRA Integration)                     (Tasks, Templates, Workflows)
```

### Data Flow

**Enrichment Workflow:**

1. User activates Security Analyst agent
2. Agent reads JIRA ticket via Atlassian MCP
3. Agent extracts CVE ID and initial context
4. Agent researches using Perplexity MCP (search/reason/deep_research)
5. Agent structures findings using enrichment template
6. Agent adds enrichment comment to JIRA ticket
7. Agent updates JIRA custom fields (CVSS, EPSS, KEV, Priority)
8. Ticket ready for review or remediation

**Review Workflow:**

1. User activates Security Reviewer agent
2. Agent reads JIRA ticket and analyst enrichment
3. Agent evaluates using 8 quality dimension checklists
4. Agent identifies gaps, errors, and cognitive biases
5. (Optional) Agent verifies claims using Perplexity
6. Agent structures review findings using review template
7. Agent adds review comment to JIRA ticket
8. Analyst addresses feedback and improves enrichment

### Integration Points

| System        | Purpose                      | Integration Method                                                 |
| ------------- | ---------------------------- | ------------------------------------------------------------------ |
| JIRA Cloud    | Ticket management            | Atlassian MCP (getJiraIssue, editJiraIssue, addCommentToJiraIssue) |
| Perplexity AI | CVE research & fact-checking | Perplexity MCP (search, reason, deep_research)                     |
| NIST NVD      | CVE details, CVSS scores     | Via Perplexity research                                            |
| CISA KEV      | Active exploitation status   | Via Perplexity research                                            |
| FIRST EPSS    | Exploitation probability     | Via Perplexity research                                            |
| MITRE ATT&CK  | Tactic/technique mapping     | Via Perplexity research + manual mapping                           |

---

## Project Directory Structure

### Overview

To ensure all vulnerability management work artifacts are properly organized, tracked, and easily accessible, BMAD-1898 requires a structured local directory system. This directory structure facilitates task execution, maintains audit trails, enables metrics tracking, and ensures all enrichment/review work is preserved locally (not just in JIRA).

**Key Principle:** JIRA serves as the system of record for tracking tickets, but the local project directory serves as the knowledge repository for detailed analysis, research artifacts, and historical records.

### Standard Directory Layout

```
project-aod-security/                      # Root project directory
├── .bmad-1898/                           # BMAD-1898 expansion pack installation
│   ├── config.yaml                       # Expansion pack configuration
│   ├── agents/                           # Agent definitions
│   │   ├── security-analyst.md
│   │   └── security-reviewer.md
│   ├── tasks/                            # Task procedures
│   ├── templates/                        # YAML templates
│   ├── checklists/                       # Quality checklists
│   ├── workflows/                        # Workflow definitions
│   └── data/                             # Knowledge bases
│
├── security-alerts/                      # Active vulnerability work
│   ├── 2025-11/                          # Monthly organization
│   │   ├── AOD-1234-struts-rce/         # Per-ticket directories
│   │   │   ├── enrichment/
│   │   │   │   ├── cve-research-CVE-2024-1234-2025-11-06.md
│   │   │   │   ├── business-impact-assessment-2025-11-06.md
│   │   │   │   ├── remediation-plan-2025-11-06.md
│   │   │   │   ├── priority-assessment-2025-11-06.md
│   │   │   │   └── security-enrichment-AOD-1234-2025-11-06.md
│   │   │   ├── review/
│   │   │   │   ├── security-review-AOD-1234-2025-11-07.md
│   │   │   │   └── fact-verification-2025-11-07.md
│   │   │   ├── remediation/
│   │   │   │   ├── remediation-log.md
│   │   │   │   ├── verification-results.md
│   │   │   │   └── lessons-learned.md
│   │   │   └── metadata.yaml              # Ticket metadata
│   │   │
│   │   ├── AOD-1235-log4j-update/
│   │   └── AOD-1236-openssl-vuln/
│   │
│   ├── 2025-12/
│   └── archive/                          # Closed tickets moved here
│       └── 2025-Q4/
│
├── cve-research/                         # CVE research repository (reusable)
│   ├── CVE-2024-1234/
│   │   ├── cve-research-report.md
│   │   ├── attack-mapping.md
│   │   ├── sources.md                    # Authoritative source links
│   │   └── updates.md                    # CVE updates over time
│   ├── CVE-2024-5678/
│   └── index.yaml                        # CVE research index
│
├── attack-mappings/                      # MITRE ATT&CK mappings library
│   ├── by-tactic/
│   │   ├── initial-access.md
│   │   ├── execution.md
│   │   ├── privilege-escalation.md
│   │   └── ...
│   ├── by-technique/
│   │   ├── T1190-exploit-public-facing-app.md
│   │   ├── T1068-privilege-escalation.md
│   │   └── ...
│   └── by-cwe/
│       ├── CWE-94-code-injection.md
│       └── ...
│
├── metrics/                              # Performance and quality metrics
│   ├── enrichment-metrics.csv
│   ├── review-metrics.csv
│   ├── quality-scores.csv
│   ├── mttr-tracking.csv
│   ├── analyst-productivity.csv
│   └── dashboards/
│       ├── weekly-summary-2025-W45.md
│       └── monthly-summary-2025-11.md
│
├── reviews/                              # Quality assurance archives
│   ├── 2025-11/
│   │   ├── AOD-1234-review.md
│   │   ├── AOD-1235-review.md
│   │   └── quality-summary-2025-11.md
│   └── bias-detection-log.csv
│
├── remediation-plans/                    # Remediation planning artifacts
│   ├── active/
│   │   ├── struts-upgrade-plan.md
│   │   ├── log4j-patching-plan.md
│   │   └── openssl-migration-plan.md
│   ├── completed/
│   └── templates/
│       ├── patch-deployment-template.md
│       └── workaround-template.md
│
├── knowledge-base/                       # Organizational knowledge
│   ├── vendor-advisories/
│   │   ├── apache/
│   │   ├── microsoft/
│   │   ├── redhat/
│   │   └── ...
│   ├── internal-procedures/
│   │   ├── patch-management-process.md
│   │   ├── emergency-response-sla.md
│   │   └── escalation-procedures.md
│   ├── lessons-learned/
│   │   ├── 2025-Q4-retrospective.md
│   │   └── incident-postmortems/
│   └── asset-inventory/
│       ├── critical-systems.yaml
│       ├── acr-ratings.csv               # Asset Criticality Ratings
│       └── system-dependencies.md
│
├── reports/                              # Executive and compliance reporting
│   ├── weekly/
│   │   └── vulnerability-summary-2025-W45.md
│   ├── monthly/
│   │   └── security-posture-2025-11.md
│   ├── quarterly/
│   │   └── Q4-2025-vulnerability-trends.md
│   └── compliance/
│       ├── pci-dss-vulnerability-report.md
│       └── hipaa-security-assessment.md
│
├── config/                               # Project configuration
│   ├── jira-custom-fields.yaml          # JIRA field mappings
│   ├── priority-framework.yaml          # Priority calculation rules
│   ├── sla-definitions.yaml             # SLA timelines per priority
│   └── team-assignments.yaml            # Analyst assignments
│
├── docs/                                 # Project documentation
│   ├── README.md                         # Project overview
│   ├── setup-guide.md                    # Initial setup instructions
│   ├── user-guide.md                     # How to use BMAD-1898
│   ├── workflow-diagrams.md             # Visual workflow representations
│   └── troubleshooting.md               # Common issues and solutions
│
└── scripts/                              # Automation scripts (optional)
    ├── generate-metrics-report.sh
    ├── archive-closed-tickets.sh
    └── export-to-dashboard.py
```

### Directory Purpose and Usage

#### `.bmad-1898/` - Expansion Pack Installation

**Purpose:** Contains the complete BMAD-1898 expansion pack installation (agents, tasks, templates, etc.)

**Usage:**

- Installed via `npx bmad-method install`
- Read-only during normal operations
- Updated only when upgrading expansion pack versions

**Key Files:**

- `config.yaml` - JIRA Cloud ID, custom field mappings, Perplexity settings
- `agents/*.md` - Security Analyst and Security Reviewer agent definitions
- `data/bmad-kb.md` - Vulnerability management methodology

---

#### `security-alerts/` - Active Vulnerability Work

**Purpose:** Working directory for all active vulnerability tickets, organized by month and ticket ID.

**Usage:**

- **Create ticket directory:** When enriching AOD-1234, create `security-alerts/2025-11/AOD-1234-<short-name>/`
- **Subdirectories:**
  - `enrichment/` - All enrichment artifacts (CVE research, business impact, remediation plan, final enrichment)
  - `review/` - Peer review reports and fact-checking results
  - `remediation/` - Remediation execution logs, verification results, lessons learned
- **metadata.yaml** - Captures ticket metadata (CVE ID, CVSS, EPSS, KEV, priority, dates)

**Workflow Integration:**

- Security Analyst agent saves all artifacts here during enrichment workflow
- Security Reviewer agent saves review reports here
- DevOps team documents remediation progress here
- Archived to `archive/` when ticket closed

**Example metadata.yaml:**

```yaml
ticket:
  id: AOD-1234
  summary: 'Apache Struts 2 RCE Vulnerability'
  created: 2025-11-06
  updated: 2025-11-07
  status: Remediation In Progress

vulnerability:
  cve_id: CVE-2024-1234
  cvss_score: 9.8
  epss_score: 0.85
  kev_status: Listed
  priority: P1

enrichment:
  analyst: Alex (Security Analyst Agent)
  enriched_date: 2025-11-06T10:30:00Z
  review_status: Reviewed
  reviewer: Jordan (Security Reviewer Agent)
  review_date: 2025-11-07T09:15:00Z
  quality_score: 92

remediation:
  approach: Patch
  patch_version: 2.5.33
  sla_deadline: 2025-11-07T10:30:00Z
  status: Testing
```

---

#### `cve-research/` - CVE Research Repository

**Purpose:** Centralized, reusable CVE research library indexed by CVE ID.

**Usage:**

- **Research once, reference many:** If multiple tickets reference CVE-2024-1234, research is stored here and can be linked from multiple ticket directories
- **Track CVE evolution:** As new exploits emerge or patches release, update the CVE research document
- **index.yaml** - Quick lookup of all researched CVEs with metadata

**Workflow Integration:**

- `research-cve.md` task saves output here
- Enrichment workflow references existing research before conducting new research
- Enables consistency across tickets referencing same CVE

**Example index.yaml:**

```yaml
CVE-2024-1234:
  researched_date: 2025-11-06
  cvss: 9.8
  epss: 0.85
  kev: true
  tickets: [AOD-1234, AOD-1567]
  path: CVE-2024-1234/cve-research-report.md
```

---

#### `attack-mappings/` - MITRE ATT&CK Mappings Library

**Purpose:** Reusable MITRE ATT&CK technique mappings organized by tactic, technique, and CWE.

**Usage:**

- **By Tactic:** Browse vulnerabilities mapped to Initial Access, Privilege Escalation, etc.
- **By Technique:** See all vulnerabilities mapped to T1190 (Exploit Public-Facing Application)
- **By CWE:** Understand which ATT&CK techniques correspond to specific weakness types (CWE-94, CWE-79, etc.)

**Workflow Integration:**

- `map-to-attack.md` task references and updates these mappings
- Detection engineering team uses mappings to design detection rules
- Threat hunting team identifies attack patterns

**Example T1190-exploit-public-facing-app.md:**

```markdown
# T1190: Exploit Public-Facing Application

**Tactic:** Initial Access

**Description:** Adversaries may exploit software vulnerabilities in Internet-facing systems to gain initial access.

## Mapped Vulnerabilities

- CVE-2024-1234 (Apache Struts 2 RCE) - CVSS 9.8, KEV Listed
- CVE-2023-5678 (WordPress Plugin XSS) - CVSS 7.5
- CVE-2023-9012 (Nginx Buffer Overflow) - CVSS 8.1, KEV Listed

## Detection Strategies

- Monitor web server logs for unusual POST parameters
- Alert on error messages indicating code execution
- Track exploit attempt signatures in WAF logs

## Compensating Controls

- Web Application Firewall (WAF) with virtual patching
- Network segmentation limiting lateral movement
- Intrusion Detection System (IDS) monitoring
```

---

#### `metrics/` - Performance and Quality Metrics

**Purpose:** Track enrichment speed, quality scores, MTTR, analyst productivity, and program effectiveness.

**Usage:**

- **CSV files:** Structured data for analysis and dashboards
- **Dashboard markdown:** Weekly/monthly human-readable summaries

**Key Metrics:**

- `enrichment-metrics.csv` - Time per ticket, research depth, completion rate
- `review-metrics.csv` - Review time, quality scores, defects found
- `quality-scores.csv` - Overall quality assessments, trend analysis
- `mttr-tracking.csv` - Mean Time to Remediation by priority level
- `analyst-productivity.csv` - Tickets per analyst per day, improvement trends

**Workflow Integration:**

- Agents automatically log timing and quality data
- Weekly script aggregates metrics for leadership reporting
- Continuous improvement team uses trends to identify gaps

---

#### `reviews/` - Quality Assurance Archives

**Purpose:** Historical record of all peer reviews and quality assessments.

**Usage:**

- Organized by month
- Includes individual review reports + monthly quality summaries
- `bias-detection-log.csv` - Tracks cognitive bias patterns for training

**Workflow Integration:**

- Security Reviewer agent saves reports here
- Monthly QA meetings review quality trends
- Analyst skill development uses review feedback

---

#### `remediation-plans/` - Remediation Planning Artifacts

**Purpose:** Centralized remediation planning and execution tracking.

**Usage:**

- `active/` - Current remediation efforts
- `completed/` - Historical remediation records
- `templates/` - Standardized remediation plan formats

**Workflow Integration:**

- `create-remediation-plan.md` task outputs here
- DevOps team tracks implementation progress
- Post-remediation retrospectives document lessons learned

---

#### `knowledge-base/` - Organizational Knowledge

**Purpose:** Internal procedures, vendor advisories, asset inventory, and institutional knowledge.

**Usage:**

- **vendor-advisories/** - Downloaded vendor security bulletins
- **internal-procedures/** - Patch management, SLAs, escalation paths
- **lessons-learned/** - Retrospectives and incident post-mortems
- **asset-inventory/** - Critical systems, ACR ratings, dependency maps

**Workflow Integration:**

- Business impact assessment references ACR ratings
- Priority assessment uses internal procedures
- New analysts onboard using knowledge base

---

#### `reports/` - Executive and Compliance Reporting

**Purpose:** Weekly, monthly, quarterly reports for leadership and compliance.

**Usage:**

- **weekly/** - Vulnerability summary for security team standup
- **monthly/** - Security posture report for management
- **quarterly/** - Trend analysis for leadership
- **compliance/** - PCI-DSS, HIPAA, SOC2 reporting artifacts

**Workflow Integration:**

- Automated script generates reports from metrics/
- Compliance auditors reference reports for audit evidence

---

### Directory Lifecycle and Maintenance

#### Daily Operations

1. **New Security Alert Created**
   - Create `security-alerts/YYYY-MM/AOD-XXXX-<short-name>/`
   - Create subdirectories: `enrichment/`, `review/`, `remediation/`
   - Create `metadata.yaml`

2. **Enrichment Workflow**
   - Save all artifacts to `enrichment/` subdirectory
   - Update `metadata.yaml` with enrichment details
   - Reference or create CVE research in `cve-research/`
   - Reference or create ATT&CK mapping in `attack-mappings/`

3. **Review Workflow**
   - Save review report to `review/` subdirectory
   - Update `metadata.yaml` with review results
   - Log quality score to `metrics/quality-scores.csv`

4. **Remediation Workflow**
   - Save remediation logs to `remediation/` subdirectory
   - Track progress in `remediation-plans/active/`
   - Update `metadata.yaml` with remediation status

5. **Ticket Closure**
   - Move ticket directory to `security-alerts/archive/YYYY-QX/`
   - Move remediation plan to `remediation-plans/completed/`
   - Update metrics with final MTTR

#### Weekly Maintenance

- Generate weekly metrics dashboard
- Review quality trends
- Identify analyst training needs
- Update knowledge base with new learnings

#### Monthly Maintenance

- Generate monthly reports (metrics, quality, security posture)
- Archive completed month's tickets
- Review and update priority framework if needed
- Conduct monthly quality retrospective

#### Quarterly Maintenance

- Generate quarterly trend analysis
- Review and update SLA timelines
- Assess program effectiveness against KPIs
- Plan improvements for next quarter

---

### Integration with BMAD-1898 Tasks

Each BMAD-1898 task is designed to work with this directory structure:

| Task                          | Input Directory                     | Output Directory                | Artifacts Created                    |
| ----------------------------- | ----------------------------------- | ------------------------------- | ------------------------------------ |
| `enrich-security-alert.md`    | `security-alerts/YYYY-MM/AOD-XXXX/` | `enrichment/`                   | security-enrichment-AOD-XXXX-DATE.md |
| `research-cve.md`             | N/A                                 | `cve-research/CVE-YYYY-NNNNN/`  | cve-research-report.md               |
| `verify-security-claims.md`   | `enrichment/`                       | `review/`                       | fact-verification-DATE.md            |
| `map-to-attack.md`            | N/A                                 | `attack-mappings/by-technique/` | TXXXX-technique-name.md              |
| `assess-business-impact.md`   | `knowledge-base/asset-inventory/`   | `enrichment/`                   | business-impact-assessment-DATE.md   |
| `create-remediation-plan.md`  | `enrichment/`                       | `remediation-plans/active/`     | remediation-plan-AOD-XXXX-DATE.md    |
| `review-security-analysis.md` | `enrichment/` + `review/`           | `reviews/YYYY-MM/`              | security-review-AOD-XXXX-DATE.md     |

---

### Initial Setup Requirements

**Prerequisite:** Before using BMAD-1898 agents, initialize the project directory structure.

**Setup Script (Recommended):**

```bash
#!/bin/bash
# setup-bmad-1898-workspace.sh

PROJECT_ROOT="project-aod-security"

mkdir -p "$PROJECT_ROOT"/{.bmad-1898,security-alerts,cve-research,attack-mappings,metrics,reviews,remediation-plans,knowledge-base,reports,config,docs,scripts}
mkdir -p "$PROJECT_ROOT"/security-alerts/{archive}
mkdir -p "$PROJECT_ROOT"/attack-mappings/{by-tactic,by-technique,by-cwe}
mkdir -p "$PROJECT_ROOT"/metrics/dashboards
mkdir -p "$PROJECT_ROOT"/remediation-plans/{active,completed,templates}
mkdir -p "$PROJECT_ROOT"/knowledge-base/{vendor-advisories,internal-procedures,lessons-learned,asset-inventory}
mkdir -p "$PROJECT_ROOT"/reports/{weekly,monthly,quarterly,compliance}

echo "BMAD-1898-Engineering workspace structure created at $PROJECT_ROOT/"
echo "Next step: Run 'npx bmad-method install' and select BMAD-1898-Engineering expansion pack"
```

**Manual Setup:**

1. Create root project directory: `project-aod-security/`
2. Run `npx bmad-method install` and select BMAD-1898-Engineering
3. Create remaining directories per structure above
4. Copy initial configuration files to `config/`
5. Document asset inventory in `knowledge-base/asset-inventory/`

---

### Benefits of Structured Directory System

✅ **Audit Trail:** Complete history of all enrichment, review, and remediation work
✅ **Knowledge Reuse:** CVE research and ATT&CK mappings reused across tickets
✅ **Metrics Tracking:** Automated performance and quality measurement
✅ **Compliance:** Organized artifacts for regulatory audits
✅ **Onboarding:** New analysts learn from historical enrichments
✅ **Continuous Improvement:** Lessons learned documented and accessible
✅ **Consistency:** Standardized artifact locations across all tickets
✅ **Scalability:** Handles 50,000+ CVEs per year with organized monthly archival

---

## Component Breakdown

### Agents

#### 1. Security Analyst Agent

**Purpose:** Enriches security vulnerability tickets with comprehensive CVE intelligence using AI-assisted research.

**Persona:**

- **Name:** Alex
- **Title:** Senior Security Analyst
- **Icon:** 🔒
- **Role:** Vulnerability intelligence specialist
- **Style:** Thorough, systematic, evidence-based, security-focused
- **Focus:** CVE research, threat intelligence, risk assessment, actionable remediation

**Core Principles:**

- Multi-factor risk assessment (CVSS + EPSS + KEV + Business Context)
- Evidence-based analysis with authoritative sources
- Actionable remediation guidance
- Business impact contextualization
- MITRE ATT&CK integration
- Numbered options protocol for user selections

**Commands:**

```yaml
commands:
  - '*help' - Show available commands
  - '*enrich {JIRA-ID}' - Run complete enrichment workflow
  - '*research-cve {CVE-ID}' - Research specific CVE
  - '*assess-priority {JIRA-ID}' - Assess vulnerability priority
  - '*map-attack {CVE-ID}' - Map to MITRE ATT&CK
  - '*remediation-plan {JIRA-ID}' - Create remediation guidance
  - '*business-impact {JIRA-ID}' - Assess business impact
  - '*yolo' - Toggle YOLO mode
  - '*exit' - Exit Security Analyst persona
```

**Dependencies:**

```yaml
dependencies:
  tasks:
    - enrich-security-alert.md
    - research-cve.md
    - assess-business-impact.md
    - create-remediation-plan.md
    - map-to-attack.md
    - execute-checklist.md (from core)
  templates:
    - security-enrichment-tmpl.yaml
    - cve-research-report-tmpl.yaml
    - remediation-plan-tmpl.yaml
    - priority-assessment-tmpl.yaml
  checklists:
    - security-enrichment-completeness-checklist.md
    - actionability-checklist.md
  data:
    - bmad-kb.md
    - vulnerability-management-kb.md
    - priority-framework.md
    - remediation-best-practices.md
    - mitre-attack-mapping-guide.md
```

**whenToUse:** When enriching security alert JIRA tickets, researching CVEs, assessing vulnerability priority, or creating remediation plans for Project AOD.

---

#### 2. Security Reviewer Agent

**Purpose:** Performs systematic quality assurance review of security analyst enrichment work, identifying gaps, biases, and accuracy issues.

**Persona:**

- **Name:** Jordan
- **Title:** Senior Security QA Specialist
- **Icon:** ✅
- **Role:** Security analysis quality assurance expert
- **Style:** Critical but constructive, detail-oriented, systematic, blameless
- **Focus:** Accuracy validation, completeness verification, bias detection, peer review

**Core Principles:**

- Systematic review using 8 quality dimensions
- Cognitive bias detection
- Blameless, constructive feedback
- Evidence-based criticism
- Continuous improvement focus
- Numbered options protocol for user selections

**Commands:**

```yaml
commands:
  - '*help' - Show available commands
  - '*review {JIRA-ID}' - Run complete review workflow
  - '*verify-claims {JIRA-ID}' - Fact-check security assertions
  - '*check-bias {JIRA-ID}' - Identify cognitive biases
  - '*validate-accuracy {JIRA-ID}' - Verify technical accuracy
  - '*assess-completeness {JIRA-ID}' - Check enrichment completeness
  - '*yolo' - Toggle YOLO mode
  - '*exit' - Exit Security Reviewer persona
```

**Dependencies:**

```yaml
dependencies:
  tasks:
    - review-security-analysis.md
    - verify-security-claims.md
    - execute-checklist.md (from core)
  templates:
    - security-review-report-tmpl.yaml
  checklists:
    - technical-accuracy-checklist.md
    - completeness-checklist.md
    - actionability-checklist.md
    - contextualization-checklist.md
    - documentation-quality-checklist.md
    - attack-mapping-checklist.md
    - cognitive-bias-checklist.md
  data:
    - bmad-kb.md
    - vulnerability-management-kb.md
    - cognitive-bias-patterns.md
```

**whenToUse:** When reviewing analyst enrichment work for quality, validating security assessments, detecting biases, or providing peer review feedback.

---

### Tasks

#### 1. enrich-security-alert.md

**Purpose:** Complete workflow for enriching security vulnerability JIRA tickets with comprehensive CVE intelligence.

**Workflow:**

```yaml
workflow:
  elicitation: true
  allow_skip: false

steps:
  - Read JIRA ticket via Atlassian MCP
  - Extract CVE ID and initial context
  - Determine research depth (search/reason/deep_research)
  - Execute Perplexity research for:
      - CVE details (NVD)
      - CVSS scores (Base, Temporal, Environmental)
      - EPSS exploitation probability
      - CISA KEV status
      - Affected software versions
      - Patch availability and vendor advisories
      - Public exploit availability
      - Active exploitation evidence
      - Business impact scenarios
      - MITRE ATT&CK mapping
  - Structure findings using security-enrichment-tmpl.yaml
  - Add enrichment comment to JIRA ticket
  - Update custom fields (CVSS, EPSS, KEV, Priority)
  - Run security-enrichment-completeness-checklist.md
  - Confirm completion
```

**Inputs:**

- JIRA ticket ID (e.g., AOD-1234)
- Optional: Specific research focus areas

**Outputs:**

- Structured enrichment comment in JIRA
- Updated JIRA custom fields
- Enrichment completeness confirmation

**Dependencies:**

- Atlassian MCP (getJiraIssue, addCommentToJiraIssue, editJiraIssue)
- Perplexity MCP (search, reason, deep_research)
- security-enrichment-tmpl.yaml
- security-enrichment-completeness-checklist.md

---

#### 2. review-security-analysis.md

**Purpose:** Systematic peer review of analyst vulnerability enrichment work using 8 quality dimensions.

**Workflow:**

```yaml
workflow:
  elicitation: false
  allow_skip: false

steps:
  - Read JIRA ticket and analyst enrichment comments
  - Extract enrichment content for analysis
  - Evaluate using 8 quality dimension checklists: 1. Technical Accuracy (10 criteria)
      2. Completeness (12 criteria)
      3. Actionability (8 criteria)
      4. Contextualization (10 criteria)
      5. Documentation Quality (8 criteria)
      6. MITRE ATT&CK Validation (4 criteria)
      7. Cognitive Bias Check (5 bias types)
      8. Source Citation (accuracy)
  - (Optional) Verify factual claims using Perplexity
  - Identify Critical Issues, Significant Gaps, Minor Improvements
  - Classify cognitive biases if detected
  - Structure findings using security-review-report-tmpl.yaml
  - Calculate overall quality score
  - Validate priority assessment appropriateness
  - Provide specific, constructive recommendations
  - Add review comment to JIRA ticket
  - Confirm completion
```

**Inputs:**

- JIRA ticket ID with analyst enrichment

**Outputs:**

- Structured review report comment in JIRA
- Quality score (percentage)
- Specific improvement recommendations
- Cognitive bias assessment

**Dependencies:**

- Atlassian MCP (getJiraIssue, addCommentToJiraIssue)
- Perplexity MCP (search - optional for fact-checking)
- security-review-report-tmpl.yaml
- All 8 quality checklists

---

#### 3. research-cve.md

**Purpose:** Focused CVE research using Perplexity AI to gather comprehensive vulnerability intelligence.

**Workflow:**

```yaml
workflow:
  elicitation: true
  allow_skip: false

steps:
  - Elicit CVE ID from user
  - Determine research scope (quick/moderate/comprehensive)
  - Select appropriate Perplexity tool:
      - search: Quick CVE lookups
      - reason: Moderate complexity analysis
      - deep_research: Critical vulnerabilities, comprehensive intel
  - Construct research query including:
      - CVE details and CWE classification
      - CVSS v3.1 and v4.0 scores
      - EPSS exploitation probability
      - CISA KEV catalog status
      - Affected versions and configurations
      - Exploitation intelligence (exploits, campaigns)
      - Attack context (vector, complexity, privileges)
      - Remediation options (patches, workarounds)
      - Business impact scenarios
      - MITRE ATT&CK mapping
  - Execute Perplexity research
  - Structure findings using cve-research-report-tmpl.yaml
  - Present research summary to user
  - Save research report (optional)
```

**Inputs:**

- CVE ID (e.g., CVE-2024-1234)
- Research depth (quick/moderate/comprehensive)

**Outputs:**

- Structured CVE research report
- Source citations
- Key findings summary

**Dependencies:**

- Perplexity MCP (search, reason, deep_research)
- cve-research-report-tmpl.yaml

---

#### 4. verify-security-claims.md

**Purpose:** Fact-check security assertions in analyst work against authoritative sources.

**Workflow:**

```yaml
workflow:
  elicitation: true
  allow_skip: false

steps:
  - Read analyst enrichment content
  - Extract factual claims requiring verification:
      - CVSS scores
      - EPSS scores
      - KEV status
      - Affected versions
      - Patch availability
      - Exploit status
  - For each claim, construct verification query
  - Use Perplexity to verify against authoritative sources:
      - NVD for CVE details and CVSS
      - CISA KEV for exploitation status
      - FIRST EPSS for exploitation probability
      - Vendor advisories for patches
      - Exploit-DB/Metasploit for exploits
  - Compare analyst claims with verified facts
  - Identify discrepancies
  - Document verification results
  - Provide correction recommendations
```

**Inputs:**

- Analyst enrichment content
- Specific claims to verify

**Outputs:**

- Verification results (Confirmed / Incorrect / Unverifiable)
- Discrepancies identified
- Authoritative source citations
- Correction recommendations

**Dependencies:**

- Perplexity MCP (search, reason)

---

#### 5. map-to-attack.md

**Purpose:** Map vulnerabilities to MITRE ATT&CK tactics and techniques.

**Workflow:**

```yaml
workflow:
  elicitation: true
  allow_skip: false

steps:
  - Elicit CVE ID or vulnerability description
  - Identify vulnerability type (RCE, SQLi, XSS, privilege escalation, etc.)
  - Use Perplexity to research MITRE ATT&CK mapping
  - Identify relevant Tactic(s):
      - Initial Access, Execution, Persistence, Privilege Escalation, etc.
  - Identify specific Technique(s) with T-numbers
  - Identify Sub-Techniques if applicable
  - Document detection implications
  - Structure mapping with justification
  - Validate mapping using attack-mapping-checklist.md
  - Present mapping results
```

**Inputs:**

- CVE ID or vulnerability description
- Vulnerability type

**Outputs:**

- ATT&CK Tactic(s)
- ATT&CK Technique(s) with T-numbers
- Sub-Techniques (if applicable)
- Detection considerations
- Mapping justification

**Dependencies:**

- Perplexity MCP (search, reason)
- mitre-attack-mapping-guide.md
- attack-mapping-checklist.md

---

#### 6. assess-business-impact.md

**Purpose:** Analyze organizational business impact of vulnerability exploitation.

**Workflow:**

```yaml
workflow:
  elicitation: true
  allow_skip: false

steps:
  - Elicit affected system details
  - Identify system criticality (Critical/High/Medium/Low)
  - Identify data sensitivity (PII/PHI/PCI/Trade Secrets/None)
  - Assess system exposure (Internet-facing/Internal/Isolated)
  - Identify regulatory implications (HIPAA/PCI-DSS/GDPR/SOC2)
  - Analyze potential consequences:
      - Confidentiality impact
      - Integrity impact
      - Availability impact
  - Assess business continuity impact
  - Identify lateral movement risks
  - Identify compensating controls
  - Calculate overall business impact rating
  - Structure assessment findings
  - Present business impact summary
```

**Inputs:**

- Affected system details
- Vulnerability characteristics
- Organizational context

**Outputs:**

- Business impact rating (Critical/High/Medium/Low)
- Consequence analysis
- Regulatory implications
- Compensating controls identified
- Business impact narrative

**Dependencies:**

- None (uses elicitation and analysis)

---

#### 7. create-remediation-plan.md

**Purpose:** Develop specific, actionable remediation guidance for vulnerabilities.

**Workflow:**

```yaml
workflow:
  elicitation: true
  allow_skip: false

steps:
  - Elicit CVE ID and affected systems
  - Research remediation options using Perplexity:
      - Patch availability and versions
      - Vendor advisories
      - Workarounds
      - Compensating controls
      - Upgrade paths
  - Identify remediation approach:
      - Rip and Replace
      - Patching
      - Compensating Controls
      - Do Nothing (with justification)
  - Create step-by-step remediation procedures
  - Identify testing requirements
  - Define verification procedures
  - Assess implementation complexity
  - Estimate remediation timeline
  - Identify deployment approach
  - Structure using remediation-plan-tmpl.yaml
  - Validate using actionability-checklist.md
  - Present remediation plan
```

**Inputs:**

- CVE ID
- Affected system details
- Current software versions

**Outputs:**

- Recommended remediation approach
- Step-by-step implementation procedures
- Testing requirements
- Verification procedures
- Complexity assessment
- Timeline estimate
- Structured remediation plan document

**Dependencies:**

- Perplexity MCP (search, reason)
- remediation-plan-tmpl.yaml
- remediation-best-practices.md
- actionability-checklist.md

---

### Templates

#### 1. security-enrichment-tmpl.yaml

**Purpose:** Structured format for comprehensive vulnerability enrichment comments in JIRA.

**Sections:**

1. Executive Summary (2-3 sentences)
2. Vulnerability Classification (CVE, CWE, Type, Published Date)
3. Severity Metrics (CVSS v3.1/v4.0, EPSS, KEV Status)
4. Affected Software (Product, Vendor, Versions, Config Requirements)
5. Exploitation Context (Attack Vector, Complexity, Privileges, User Interaction, Scope, Impact)
6. Exploit Intelligence (Public Exploits, Maturity, Weaponization, Active Exploitation)
7. Business Impact Assessment (Potential Impact, Affected Systems, Criticality, Data Sensitivity, Regulatory)
8. Remediation Guidance (Patch Info, Steps, Workarounds, Verification)
9. MITRE ATT&CK Mapping (Tactic, Technique, Sub-Technique, Detection)
10. Attack Surface Analysis (Exposure, Access Requirements, Lateral Movement, Dependencies)
11. Priority Recommendation (Level, Timeline, Rationale)
12. Related Information (Similar CVEs, References)

**Format:** Markdown with structured sections and emojis for visual scanning

**Output Filename:** `security-enrichment-{{jira_id}}-{{date}}.md`

---

#### 2. security-review-report-tmpl.yaml

**Purpose:** Structured format for peer review findings and feedback.

**Sections:**

1. Review Summary (Ticket, Analyst, Reviewer, Date, Overall Assessment)
2. Strengths (What analyst did well)
3. Critical Issues (Must-fix issues)
4. Significant Gaps (Should-fix issues)
5. Minor Improvements (Nice-to-have improvements)
6. Cognitive Bias Check (Detected biases)
7. Checklist Review Results (Scores for 8 quality dimensions)
8. Overall Quality Score (Percentage + Rating)
9. Priority Validation (Is assigned priority appropriate?)
10. Specific Recommendations (Prioritized actions)
11. Learning Resources (Links for identified gaps)
12. Next Steps (For analyst and reviewer)

**Format:** Markdown with structured sections, checkboxes, and scoring

**Output Filename:** `security-review-{{jira_id}}-{{date}}.md`

---

#### 3. cve-research-report-tmpl.yaml

**Purpose:** Structured format for standalone CVE research findings.

**Sections:**

1. CVE Summary (ID, Description, Published Date)
2. Severity Assessment (CVSS, EPSS, KEV)
3. Technical Details (CWE, Vulnerability Type, Attack Vector)
4. Affected Products (Vendors, Versions, Configurations)
5. Exploitation Intelligence (Exploits, Campaigns, Threat Actors)
6. Remediation Options (Patches, Workarounds, Vendor Advisories)
7. MITRE ATT&CK Mapping
8. References (Authoritative sources cited)

**Format:** Markdown with structured sections

**Output Filename:** `cve-research-{{cve_id}}-{{date}}.md`

---

#### 4. remediation-plan-tmpl.yaml

**Purpose:** Structured format for vulnerability remediation guidance.

**Sections:**

1. Remediation Overview (CVE, Affected Systems, Approach)
2. Patch Information (Version, Release Date, Vendor Advisory, Download)
3. Implementation Steps (Detailed procedures)
4. Testing Requirements (Pre-deployment testing)
5. Verification Procedures (Post-deployment validation)
6. Workarounds (Temporary mitigations if patch unavailable)
7. Rollback Plan (If remediation fails)
8. Deployment Strategy (Phased/All-at-once/Parallel)
9. Timeline Estimate (Expected duration)
10. Complexity Assessment (Low/Medium/High)
11. Risk Assessment (Risks of remediation vs. not remediating)

**Format:** Markdown with step-by-step procedures

**Output Filename:** `remediation-plan-{{jira_id}}-{{date}}.md`

---

#### 5. priority-assessment-tmpl.yaml

**Purpose:** Structured format for vulnerability priority determination.

**Sections:**

1. Priority Summary (Recommended Level P1-P5)
2. Factor Analysis:
   - CVSS Severity (Critical/High/Medium/Low)
   - EPSS Probability (High/Medium/Low)
   - KEV Status (Listed/Not Listed)
   - System Criticality (Critical/High/Medium/Low)
   - System Exposure (Internet-facing/Internal/Isolated)
   - Exploit Availability (Available/Not Available)
   - Active Exploitation (Confirmed/Not Observed)
3. Priority Calculation (Factor weighting)
4. Remediation Timeline (SLA based on priority)
5. Rationale (Why this priority level)
6. Modifiers (Factors that increase/decrease priority)

**Format:** Markdown with scoring matrix

**Output Filename:** `priority-assessment-{{jira_id}}-{{date}}.md`

---

### Checklists

#### 1. security-enrichment-completeness-checklist.md

**Purpose:** Verify all required enrichment sections are complete.

**Categories:**

- **CVE Details** (5 items)
- **Severity Metrics** (4 items: CVSS, EPSS, KEV, Vector)
- **Affected Software** (4 items)
- **Exploitation Context** (6 items)
- **Business Impact** (5 items)
- **Remediation Guidance** (4 items)
- **MITRE ATT&CK** (3 items)
- **Documentation** (3 items: Sources, Date, Reviewer)

**Total Items:** 34

---

#### 2. technical-accuracy-checklist.md

**Purpose:** Verify technical claims are factually correct.

**Categories:**

- **CVE Accuracy** (CVE ID correct, Description accurate)
- **CVSS Accuracy** (Score correct, Vector accurate)
- **EPSS Accuracy** (Current score, Trend)
- **KEV Accuracy** (Status correct, Date added if listed)
- **Version Accuracy** (Affected versions precise, Patched versions correct)
- **Patch Accuracy** (Availability correct, Source links valid)
- **Exploit Accuracy** (Status factual, Sources cited)

**Total Items:** 10

---

#### 3. completeness-checklist.md

**Purpose:** Ensure comprehensive coverage of all enrichment factors.

**Categories:**

- **Severity Metrics Complete** (CVSS, EPSS, KEV all researched)
- **Exploit Intelligence** (Public exploits, Maturity, Active exploitation)
- **Attack Context** (Vector, Complexity, Prerequisites)
- **Business Impact** (Consequences, Affected systems, Regulatory)
- **Remediation Options** (Patches AND workarounds)
- **Verification** (How to verify remediation)
- **MITRE ATT&CK** (Tactics and techniques mapped)
- **Dependencies** (Transitive dependencies considered)

**Total Items:** 12

---

#### 4. actionability-checklist.md

**Purpose:** Ensure remediation guidance is specific and implementable.

**Categories:**

- **Patch Specificity** (Exact versions, Sources)
- **Implementation Steps** (Concrete, ordered procedures)
- **Testing Requirements** (What testing needed)
- **Workarounds** (Temporary mitigations if patch unavailable)
- **Deployment Approach** (How to roll out)
- **Verification Steps** (How to confirm success)
- **Timeline Estimates** (Realistic expectations)
- **Complexity** (Implementation difficulty assessed)

**Total Items:** 8

---

#### 5. contextualization-checklist.md

**Purpose:** Verify organizational business context is incorporated.

**Categories:**

- **System Criticality** (Business importance assessed)
- **Exposure Assessment** (Internet-facing vs internal)
- **Data Sensitivity** (PII/PHI/PCI considerations)
- **Compensating Controls** (Existing mitigations identified)
- **Regulatory Impact** (Compliance implications noted)
- **Priority Justification** (Reflects org risk, not just CVSS)
- **Lateral Movement** (Cascade risks considered)
- **Industry Context** (Industry-specific threats)
- **Risk Appetite** (Aligns with org tolerance)
- **Resource Constraints** (Feasibility considered)

**Total Items:** 10

---

#### 6. documentation-quality-checklist.md

**Purpose:** Ensure clear, well-structured documentation.

**Categories:**

- **Executive Summary** (2-3 sentence overview present)
- **Structured Format** (Clear section headings)
- **Readability** (Formatting aids scanning)
- **Source Citations** (Links to NVD, KEV, advisories)
- **Consistent Terminology** (Technical terms correct)
- **Logical Flow** (Sensible information order)
- **Completeness** (All template sections addressed)
- **Timestamps** (Time-sensitive info dated)

**Total Items:** 8

---

#### 7. attack-mapping-checklist.md

**Purpose:** Validate MITRE ATT&CK mapping accuracy.

**Categories:**

- **Tactic Identified** (Correct ATT&CK tactic)
- **Technique Specified** (Specific T-number provided)
- **Technique Appropriate** (Accurately reflects vulnerability)
- **Detection Mentioned** (How to detect technique usage)

**Total Items:** 4

---

#### 8. cognitive-bias-checklist.md

**Purpose:** Detect cognitive biases in security analysis.

**Bias Types:**

- **Confirmation Bias** (Seeking only confirming evidence)
- **Anchoring Bias** (Over-relying on initial information)
- **Availability Heuristic** (Overweighting recent/publicized events)
- **Overconfidence** (Assertions without evidence)
- **Recency Bias** (Weighting recent info over older relevant data)

**Total Items:** 5

---

### Workflows

#### 1. security-alert-enrichment-workflow.yaml

**Purpose:** Complete end-to-end vulnerability enrichment process.

**Stages:**

```yaml
stages:
  - name: Alert Triage
    agent: Security Analyst
    tasks:
      - Read JIRA ticket
      - Extract CVE ID and context
      - Determine severity and research depth
    outputs:
      - Initial assessment
      - Research plan

  - name: CVE Research
    agent: Security Analyst
    tasks:
      - Execute research-cve.md task
      - Gather CVSS, EPSS, KEV data
      - Research exploits and threat intelligence
      - Identify affected versions and patches
    outputs:
      - CVE research report
      - Source citations

  - name: Business Context
    agent: Security Analyst
    tasks:
      - Execute assess-business-impact.md task
      - Identify affected systems
      - Assess regulatory implications
      - Identify compensating controls
    outputs:
      - Business impact assessment

  - name: Remediation Planning
    agent: Security Analyst
    tasks:
      - Execute create-remediation-plan.md task
      - Research patches and workarounds
      - Create implementation steps
      - Define verification procedures
    outputs:
      - Remediation plan

  - name: ATT&CK Mapping
    agent: Security Analyst
    tasks:
      - Execute map-to-attack.md task
      - Identify tactics and techniques
      - Document detection implications
    outputs:
      - ATT&CK mapping

  - name: Priority Assessment
    agent: Security Analyst
    tasks:
      - Calculate multi-factor priority
      - Apply priority framework
      - Determine SLA timeline
    outputs:
      - Priority recommendation (P1-P5)
      - Remediation timeline

  - name: Enrichment Documentation
    agent: Security Analyst
    tasks:
      - Structure findings using security-enrichment-tmpl.yaml
      - Add enrichment comment to JIRA
      - Update custom fields (CVSS, EPSS, KEV, Priority)
      - Run security-enrichment-completeness-checklist.md
    outputs:
      - JIRA ticket enriched
      - Enrichment complete

  - name: Quality Validation
    agent: Security Analyst
    tasks:
      - Self-review enrichment
      - Verify all sections complete
      - Check source citations
    outputs:
      - Enrichment validated
      - Ready for peer review
```

**Duration:** 10-15 minutes (with AI assistance)

**Frequency:** Per security alert ticket

---

#### 2. security-analysis-review-workflow.yaml

**Purpose:** Systematic peer review and quality assurance of analyst work.

**Stages:**

```yaml
stages:
  - name: Review Preparation
    agent: Security Reviewer
    tasks:
      - Read JIRA ticket and analyst enrichment
      - Extract enrichment content
      - Identify review scope
    outputs:
      - Enrichment content extracted
      - Review plan

  - name: Systematic Evaluation
    agent: Security Reviewer
    tasks:
      - Evaluate using 8 quality dimension checklists: 1. Technical Accuracy (10 items)
          2. Completeness (12 items)
          3. Actionability (8 items)
          4. Contextualization (10 items)
          5. Documentation Quality (8 items)
          6. MITRE ATT&CK Validation (4 items)
          7. Cognitive Bias Check (5 biases)
          8. Source Citation (accuracy)
      - Document findings per dimension
    outputs:
      - Quality scores per dimension
      - Issues identified

  - name: Gap Identification
    agent: Security Reviewer
    tasks:
      - Categorize findings:
          - Critical Issues (must-fix)
          - Significant Gaps (should-fix)
          - Minor Improvements (nice-to-have)
      - Provide specific examples
      - Explain impact of each gap
    outputs:
      - Categorized findings
      - Impact analysis

  - name: Bias Detection
    agent: Security Reviewer
    tasks:
      - Run cognitive-bias-checklist.md
      - Identify bias patterns
      - Provide examples of bias
      - Suggest debiasing strategies
    outputs:
      - Cognitive bias assessment
      - Recommendations

  - name: Fact Verification (Optional)
    agent: Security Reviewer
    tasks:
      - Execute verify-security-claims.md task
      - Verify critical claims using Perplexity
      - Document discrepancies
    outputs:
      - Verification results
      - Corrections needed

  - name: Review Documentation
    agent: Security Reviewer
    tasks:
      - Structure findings using security-review-report-tmpl.yaml
      - Calculate overall quality score
      - Validate priority assessment
      - Provide specific recommendations
      - Add review comment to JIRA
    outputs:
      - Review report in JIRA
      - Quality score
      - Recommendations

  - name: Feedback Loop
    agent: Security Analyst
    tasks:
      - Read review feedback
      - Address critical issues
      - Improve enrichment based on recommendations
      - Update JIRA ticket
    outputs:
      - Improved enrichment
      - Quality enhanced
```

**Duration:** 15-20 minutes

**Frequency:** Critical/High priority vulnerabilities (mandatory), Medium/Low (sampling)

---

#### 3. vulnerability-lifecycle-workflow.yaml

**Purpose:** Complete vulnerability management from alert through remediation.

**Stages:**

```yaml
stages:
  - name: Alert Detection
    owner: Security Scanner / Dependabot / Manual Report
    outputs:
      - JIRA security alert ticket created

  - name: Enrichment
    workflow: security-alert-enrichment-workflow.yaml
    agent: Security Analyst
    outputs:
      - Ticket enriched with CVE intelligence

  - name: Peer Review (if Critical/High)
    workflow: security-analysis-review-workflow.yaml
    agent: Security Reviewer
    outputs:
      - Quality validated
      - Improvements identified

  - name: Remediation Planning
    owner: Security Analyst + DevOps
    tasks:
      - Review remediation plan
      - Assign to responsible team
      - Schedule remediation
    outputs:
      - Remediation scheduled
      - Team assigned

  - name: Remediation Execution
    owner: DevOps / IT Operations
    tasks:
      - Apply patches or workarounds
      - Test changes
      - Deploy to production
    outputs:
      - Remediation deployed

  - name: Verification
    owner: Security Analyst
    tasks:
      - Verify vulnerability remediated
      - Rescan affected systems
      - Confirm fix persistent
    outputs:
      - Remediation verified

  - name: Closure
    owner: Security Analyst
    tasks:
      - Update JIRA ticket status
      - Document lessons learned
      - Close ticket
    outputs:
      - Ticket closed
      - Metrics updated
```

**Duration:** Hours to weeks (depending on priority)

**Frequency:** Per vulnerability

---

### Data/Knowledge Bases

#### 1. bmad-kb.md (Expansion Pack Override)

**Purpose:** BMAD-1898 specific methodology and best practices.

**Content:**

- Security vulnerability management methodology
- AI-assisted research best practices
- Quality assurance principles
- Blameless review culture
- Integration with BMAD core principles

---

#### 2. vulnerability-management-kb.md

**Purpose:** Comprehensive vulnerability management frameworks and standards.

**Content:**

- NIST NVD and CVE system overview
- CVSS v3.1 and v4.0 scoring methodology
- EPSS (Exploit Prediction Scoring System) framework
- CISA KEV catalog usage and mandates
- Vulnerability lifecycle stages
- Remediation approaches (Rip-Replace, Patching, Compensating Controls, Do Nothing)
- Asset Criticality Rating (ACR) framework
- Multi-factor risk assessment methodology
- Industry statistics and trends (2025 CVE volume, alert fatigue data)

**Sources:** Research report from Perplexity deep_research

---

#### 3. cognitive-bias-patterns.md

**Purpose:** Common cognitive biases in security analysis and mitigation strategies.

**Content:**

- Confirmation bias in vulnerability assessment
- Anchoring bias (over-relying on CVSS)
- Availability heuristic (overweighting recent threats)
- Overconfidence (Dunning-Kruger effect)
- Recency bias
- Real-world examples from security operations
- Debiasing techniques and structured decision-making
- Red team exercises for bias detection

**Sources:** Research report + Security Alert Review document

---

#### 4. mitre-attack-mapping-guide.md

**Purpose:** How to map vulnerabilities to MITRE ATT&CK framework.

**Content:**

- ATT&CK framework overview (v18 updates)
- Common tactics for vulnerability types:
  - Initial Access (RCE, network vulnerabilities)
  - Execution (code execution flaws)
  - Persistence (backdoor vulnerabilities)
  - Privilege Escalation (elevation vulnerabilities)
  - Defense Evasion (security bypass)
  - Credential Access (credential theft)
- Common techniques with T-numbers:
  - T1190: Exploit Public-Facing Application
  - T1068: Exploitation for Privilege Escalation
  - T1210: Exploitation of Remote Services
  - T1203: Exploitation for Client Execution
- Technique mapping examples
- Detection implications per technique
- Sub-technique identification

**Sources:** Research report + Security Alert Enrichment document

---

#### 5. priority-framework.md

**Purpose:** Multi-factor vulnerability priority determination framework.

**Content:**

- Priority Levels (P1-P5) with criteria
- **P1 (Immediate <24hrs):** CVSS 9-10 + Internet-facing OR EPSS >0.9 OR KEV + Active Exploitation
- **P2 (Urgent <7 days):** CVSS 7-8.9 + Business-Critical OR EPSS 0.7-0.9 OR KEV Listed
- **P3 (Scheduled <30 days):** CVSS 6-6.9 OR EPSS 0.4-0.7 OR Important Systems
- **P4 (Standard <60 days):** CVSS 4-5.9 + EPSS <0.4 + Non-Critical
- **P5 (Monitoring 90+ days):** CVSS 0.1-3.9 + EPSS <0.1 + Very Limited Impact
- Priority modifiers (increase/decrease based on context)
- SLA timelines per priority level
- Escalation criteria
- Priority calculation methodology (factor weighting)

**Sources:** Research report + Security Alert Enrichment document

---

#### 6. remediation-best-practices.md

**Purpose:** Vulnerability remediation approaches and implementation guidance.

**Content:**

- Four remediation approaches:
  1. Rip and Replace (component substitution)
  2. Patching (targeted fixes)
  3. Compensating Controls (risk mitigation)
  4. Do Nothing (explicit acceptance)
- When to use each approach
- Patch management workflows
- Workaround implementation
- Verification procedures
- Rollback planning
- Deployment strategies (phased, all-at-once, parallel)
- Testing requirements
- Change management integration
- Automated remediation best practices
- Common remediation mistakes to avoid

**Sources:** Research report + Security Alert Enrichment document

---

### Configuration

#### .bmad-1898/config.yaml

**Purpose:** Expansion pack configuration for JIRA and Perplexity integration.

**Structure:**

```yaml
expansion_pack:
  id: bmad-1898-engineering
  name: Engineering
  version: 1.0.0
  description: AI-assisted vulnerability enrichment and quality assurance for Project AOD

jira:
  cloud_id: '934c63a0-0b96-4d46-b906-0f8c1c85c5d7' # AOD project
  project_key: 'AOD'
  issue_type: 'Security Alert'

  custom_fields:
    cve_id: 'customfield_10050'
    cvss_score: 'customfield_10051'
    epss_score: 'customfield_10052'
    kev_status: 'customfield_10053'
    priority_level: 'priority' # Standard field
    affected_product: 'customfield_10054'
    affected_versions: 'customfield_10055'
    patch_status: 'customfield_10056'
    patch_version: 'customfield_10057'

perplexity:
  default_model: 'sonar-reasoning-pro' # For complex analysis
  quick_model: 'sonar-pro' # For quick lookups
  research_model: 'sonar-deep-research' # For critical vulnerabilities

  research_depth:
    critical: 'deep_research' # CVSS 9-10
    high: 'reason' # CVSS 7-8.9
    medium: 'search' # CVSS 4-6.9
    low: 'search' # CVSS 0-3.9

priority_framework:
  sla_timelines:
    p1: '< 24 hours'
    p2: '< 7 days'
    p3: '< 30 days'
    p4: '< 60 days'
    p5: '< 90 days (monitoring)'

  mandatory_review:
    - 'p1' # Critical
    - 'p2' # High

  sampling_review:
    p3: 0.25 # 25% of Medium priority
    p4: 0.10 # 10% of Standard priority
    p5: 0.05 # 5% of Low priority

enrichment:
  required_sections:
    - executive_summary
    - vulnerability_classification
    - severity_metrics
    - affected_software
    - exploitation_context
    - business_impact
    - remediation_guidance
    - attack_mapping
    - priority_recommendation

  authoritative_sources:
    - 'https://nvd.nist.gov' # NVD
    - 'https://www.cisa.gov/known-exploited-vulnerabilities-catalog' # KEV
    - 'https://www.first.org/epss' # EPSS
    - 'https://attack.mitre.org' # MITRE ATT&CK

quality_assurance:
  review_dimensions:
    - technical_accuracy
    - completeness
    - actionability
    - contextualization
    - documentation_quality
    - attack_mapping

  quality_thresholds:
    excellent: 0.90 # 90%+
    good: 0.75 # 75-89%
    needs_improvement: 0.60 # 60-74%
    significant_gaps: 0.00 # <60%

  cognitive_biases:
    - confirmation_bias
    - anchoring_bias
    - availability_heuristic
    - overconfidence
    - recency_bias
```

---

## User Stories & Epics

### Epic 1: Security Analyst Enrichment System

**Epic Goal:** Enable security analysts to enrich vulnerability tickets 90% faster with AI-assisted research while maintaining enterprise-grade quality.

#### User Stories:

**Story 1.1:** Security Analyst Agent Creation

- **As a** security analyst
- **I want** a specialized BMAD agent persona
- **So that** I can activate consistent enrichment workflows with a single command

**Acceptance Criteria:**

- Security Analyst agent definition complete with commands, dependencies, persona
- Agent can be activated via `/security-analyst` or equivalent
- Agent displays available commands on activation
- Agent greets user and runs `*help` on startup

**Story 1.2:** JIRA Ticket Reading

- **As a** Security Analyst agent
- **I want** to read JIRA security alert tickets via Atlassian MCP
- **So that** I can extract CVE IDs and initial context

**Acceptance Criteria:**

- Agent can read JIRA tickets using `mcp__atlassian__getJiraIssue`
- Agent extracts CVE ID from ticket summary or description
- Agent identifies affected systems from ticket fields
- Agent handles tickets without CVE IDs gracefully

**Story 1.3:** AI-Assisted CVE Research

- **As a** Security Analyst agent
- **I want** to research CVEs using Perplexity MCP
- **So that** I can gather comprehensive vulnerability intelligence in minutes

**Acceptance Criteria:**

- Agent constructs research queries including CVSS, EPSS, KEV, exploits, patches, ATT&CK
- Agent selects appropriate Perplexity tool (search/reason/deep_research) based on severity
- Agent receives structured research findings
- Agent cites authoritative sources (NVD, CISA, vendor advisories)

**Story 1.4:** Structured Enrichment Documentation

- **As a** Security Analyst agent
- **I want** to structure research findings using the enrichment template
- **So that** all enrichment comments follow consistent, comprehensive format

**Acceptance Criteria:**

- Agent uses security-enrichment-tmpl.yaml
- All 12 sections of template completed
- Executive summary provides 2-3 sentence overview
- Severity metrics include CVSS, EPSS, KEV
- MITRE ATT&CK mapping included
- Priority recommendation with rationale

**Story 1.5:** JIRA Enrichment Comment

- **As a** Security Analyst agent
- **I want** to add structured enrichment as JIRA comment
- **So that** stakeholders can review findings in familiar JIRA interface

**Acceptance Criteria:**

- Agent adds comment using `mcp__atlassian__addCommentToJiraIssue`
- Comment formatted in markdown with structured sections
- Emojis used for visual scanning (✅/❌/⚠️)
- Source citations as links
- Timestamp and generator attribution included

**Story 1.6:** JIRA Custom Field Updates

- **As a** Security Analyst agent
- **I want** to update JIRA custom fields for CVSS, EPSS, KEV, Priority
- **So that** JIRA queries and automation can leverage structured data

**Acceptance Criteria:**

- Agent updates custom fields using `mcp__atlassian__editJiraIssue`
- CVSS score (number field)
- EPSS score (number field)
- KEV status (dropdown: Listed/Not Listed)
- Priority (standard field: Critical/High/Medium/Low)
- CVE ID (text field)

**Story 1.7:** Multi-Factor Priority Assessment

- **As a** Security Analyst agent
- **I want** to calculate vulnerability priority using CVSS + EPSS + KEV + Business Context
- **So that** remediation efforts focus on genuine exploitable threats

**Acceptance Criteria:**

- Agent considers all priority factors:
  - CVSS severity (Critical/High/Medium/Low)
  - EPSS exploitation probability
  - KEV active exploitation status
  - System criticality (ACR rating)
  - System exposure (Internet/Internal/Isolated)
  - Exploit availability
- Agent applies priority framework (P1-P5)
- Agent provides rationale for priority level
- Agent identifies SLA remediation timeline

---

### Epic 2: Security Reviewer Quality Assurance System

**Epic Goal:** Implement systematic peer review identifying 60-70% more quality gaps while fostering blameless learning culture.

#### User Stories:

**Story 2.1:** Security Reviewer Agent Creation

- **As a** security team lead
- **I want** a specialized QA reviewer agent
- **So that** I can ensure consistent, thorough review of analyst work

**Acceptance Criteria:**

- Security Reviewer agent definition complete
- Agent can be activated and displays commands
- Agent persona is constructive, not punitive
- Blameless review principles embedded

**Story 2.2:** Systematic Quality Evaluation

- **As a** Security Reviewer agent
- **I want** to evaluate enrichments using 8 quality dimension checklists
- **So that** reviews are comprehensive and consistent

**Acceptance Criteria:**

- Agent runs all 8 checklists:
  1. Technical Accuracy (10 items)
  2. Completeness (12 items)
  3. Actionability (8 items)
  4. Contextualization (10 items)
  5. Documentation Quality (8 items)
  6. MITRE ATT&CK Validation (4 items)
  7. Cognitive Bias Check (5 biases)
  8. Source Citation (accuracy)
- Agent scores each dimension (percentage)
- Agent calculates overall quality score

**Story 2.3:** Gap Identification and Categorization

- **As a** Security Reviewer agent
- **I want** to categorize findings as Critical/Significant/Minor
- **So that** analysts know what to prioritize

**Acceptance Criteria:**

- Critical Issues: Must-fix before ticket can proceed
- Significant Gaps: Should-fix, impacts quality
- Minor Improvements: Nice-to-have enhancements
- Each finding includes:
  - Specific location
  - What's missing/incorrect
  - Why it matters
  - Recommended fix

**Story 2.4:** Cognitive Bias Detection

- **As a** Security Reviewer agent
- **I want** to identify cognitive biases in analyst work
- **So that** systematic bias patterns can be corrected

**Acceptance Criteria:**

- Agent runs cognitive-bias-checklist.md
- Agent detects 5 bias types:
  - Confirmation bias
  - Anchoring bias
  - Availability heuristic
  - Overconfidence
  - Recency bias
- Agent provides specific examples of detected bias
- Agent suggests debiasing strategies

**Story 2.5:** Fact Verification

- **As a** Security Reviewer agent
- **I want** to verify factual claims using Perplexity
- **So that** critical assertions are validated against authoritative sources

**Acceptance Criteria:**

- Agent can optionally verify claims
- Agent checks: CVSS scores, EPSS scores, KEV status, patch availability
- Agent compares analyst claims with authoritative sources
- Agent documents discrepancies
- Agent provides corrections with sources

**Story 2.6:** Constructive Feedback Documentation

- **As a** Security Reviewer agent
- **I want** to structure review findings using review template
- **So that** feedback is clear, actionable, and blameless

**Acceptance Criteria:**

- Agent uses security-review-report-tmpl.yaml
- Acknowledges strengths first
- Identifies gaps with impact explanation
- Provides specific recommendations
- Links to learning resources
- Maintains respectful, constructive tone

---

### Epic 3: Workflow Orchestration & Integration

**Epic Goal:** Seamless JIRA integration and complete vulnerability lifecycle workflow from alert to remediation.

#### User Stories:

**Story 3.1:** Security Alert Enrichment Workflow

- **As a** security operations team
- **I want** a complete end-to-end enrichment workflow
- **So that** enrichment is consistent and comprehensive

**Acceptance Criteria:**

- Workflow includes all stages: Triage → Research → Business Context → Remediation → ATT&CK → Priority → Documentation → Validation
- Each stage has clear inputs/outputs
- Workflow takes 10-15 minutes with AI assistance
- Workflow produces enriched JIRA ticket

**Story 3.2:** Security Analysis Review Workflow

- **As a** security operations team
- **I want** a systematic peer review workflow
- **So that** quality assurance is thorough and consistent

**Acceptance Criteria:**

- Workflow includes: Preparation → Evaluation → Gap Identification → Bias Detection → (Optional) Fact Verification → Documentation → Feedback Loop
- Workflow takes 15-20 minutes
- Workflow produces review report in JIRA
- Workflow triggers analyst improvements

**Story 3.3:** Vulnerability Lifecycle Workflow

- **As a** security operations team
- **I want** complete lifecycle tracking from alert to closure
- **So that** vulnerabilities are systematically managed

**Acceptance Criteria:**

- Workflow stages: Detection → Enrichment → Review → Remediation Planning → Execution → Verification → Closure
- Integration with existing ticketing workflows
- Metrics captured at each stage
- Audit trail maintained

**Story 3.4:** Priority-Based Review Triggering

- **As a** security operations team
- **I want** mandatory review for Critical/High vulnerabilities and sampling for Medium/Low
- **So that** QA resources focus on highest-risk tickets

**Acceptance Criteria:**

- P1/P2 vulnerabilities trigger mandatory review
- P3 vulnerabilities: 25% sampling review
- P4 vulnerabilities: 10% sampling review
- P5 vulnerabilities: 5% sampling review
- Review assignment configurable

---

### Epic 4: Knowledge Management & Continuous Improvement

**Epic Goal:** Comprehensive knowledge bases enabling analyst skill development and organizational learning.

#### User Stories:

**Story 4.1:** Vulnerability Management Knowledge Base

- **As a** security analyst
- **I want** comprehensive vulnerability management best practices
- **So that** I understand frameworks like CVSS, EPSS, KEV, ACR

**Acceptance Criteria:**

- Knowledge base includes NIST NVD, CVSS, EPSS, KEV, ACR frameworks
- Industry statistics (2025 CVE volume, alert fatigue data)
- Remediation approaches explained
- Multi-factor risk assessment methodology

**Story 4.2:** Cognitive Bias Patterns Guide

- **As a** security analyst
- **I want** to understand cognitive biases in security analysis
- **So that** I can recognize and avoid systematic errors

**Acceptance Criteria:**

- Guide covers 5 bias types with definitions
- Real-world examples from security operations
- Debiasing techniques explained
- Self-assessment guidance

**Story 4.3:** MITRE ATT&CK Mapping Guide

- **As a** security analyst
- **I want** clear guidance on mapping vulnerabilities to ATT&CK
- **So that** I can accurately identify tactics and techniques

**Acceptance Criteria:**

- Common tactics for vulnerability types
- Common techniques with T-numbers
- Mapping examples
- Detection implications per technique

**Story 4.4:** Priority Framework Documentation

- **As a** security analyst
- **I want** clear priority level definitions and criteria
- **So that** I consistently apply the same framework

**Acceptance Criteria:**

- P1-P5 levels defined with criteria
- Factor weighting explained
- SLA timelines per priority
- Priority modifiers documented

---

## Integration Requirements

### Atlassian MCP (JIRA Integration)

**Required Tools:**

- `mcp__atlassian__getJiraIssue` - Read ticket details
- `mcp__atlassian__editJiraIssue` - Update custom fields
- `mcp__atlassian__addCommentToJiraIssue` - Add enrichment/review comments
- `mcp__atlassian__getAccessibleAtlassianResources` - Verify access

**Configuration:**

- JIRA Cloud ID: `934c63a0-0b96-4d46-b906-0f8c1c85c5d7` (Project AOD)
- Project Key: `AOD`
- Issue Type: `Security Alert`
- Custom field mappings defined in config.yaml

**Error Handling:**

- Graceful degradation if MCP unavailable (manual workflow)
- Clear error messages if JIRA access fails
- Fallback to console output if ticket update fails

---

### Perplexity MCP (AI Research)

**Required Tools:**

- `mcp__perplexity__search` - Quick CVE lookups, simple queries
- `mcp__perplexity__reason` - Complex analysis, remediation planning
- `mcp__perplexity__deep_research` - Critical vulnerabilities, comprehensive intel

**Research Strategy:**

- **Critical (CVSS 9-10):** Use `deep_research` for comprehensive analysis
- **High (CVSS 7-8.9):** Use `reason` for moderate complexity
- **Medium (CVSS 4-6.9):** Use `search` for quick lookups
- **Low (CVSS 0-3.9):** Use `search` for basic information

**Query Construction:**

- Always request specific authoritative sources (NVD, CISA, EPSS, vendor)
- Include exact information needed (CVSS vector, EPSS score, KEV status, patches)
- Request source citations for all factual claims
- Specify exploit intelligence requirements

**Error Handling:**

- Retry with simpler query if deep_research times out
- Fall back to manual research if Perplexity unavailable
- Validate AI outputs against authoritative sources
- Flag hallucinations when detected

---

### Authoritative Data Sources

**NIST NVD (National Vulnerability Database):**

- Purpose: CVE details, CVSS scores, affected products
- URL: https://nvd.nist.gov
- Access: Via Perplexity research (no direct API)
- Update Frequency: Real-time

**CISA KEV Catalog:**

- Purpose: Known Exploited Vulnerabilities listing
- URL: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- Access: Via Perplexity research
- Update Frequency: Continuous

**FIRST EPSS (Exploit Prediction Scoring System):**

- Purpose: Exploitation probability scores
- URL: https://www.first.org/epss
- Access: Via Perplexity research
- Update Frequency: Daily

**MITRE ATT&CK:**

- Purpose: Adversary tactics and techniques
- URL: https://attack.mitre.org
- Access: Via Perplexity research
- Version: v18 (2025)

**Vendor Security Advisories:**

- Purpose: Official patches, workarounds, affected versions
- Access: Via Perplexity research (vendor-specific URLs)
- Examples: Microsoft Security Response Center, Red Hat Security, Ubuntu Security

---

## Quality Standards

### Enrichment Quality Gates

**Required Elements (Must Have):**

- ✅ CVE ID correctly identified
- ✅ CVSS score with vector string
- ✅ EPSS score (current)
- ✅ KEV status checked
- ✅ Affected versions (precise ranges)
- ✅ Patch availability and version
- ✅ Exploit status researched
- ✅ Business impact assessed
- ✅ Remediation steps (specific, actionable)
- ✅ MITRE ATT&CK mapping
- ✅ Priority recommendation with rationale
- ✅ Source citations (authoritative links)

**Quality Thresholds:**

- **Excellent (90-100%):** All required elements + comprehensive context, minimal gaps
- **Good (75-89%):** All required elements + some gaps in depth/context
- **Needs Improvement (60-74%):** Missing some required elements or significant quality gaps
- **Significant Gaps (<60%):** Major rework needed, many missing elements

**Review Requirements:**

- **Mandatory Review:** P1 (Critical) and P2 (High) vulnerabilities
- **Sampling Review:** P3 (25%), P4 (10%), P5 (5%)
- **Review SLA:** Within 24 hours for P1/P2, within 1 week for P3/P4/P5

---

### Documentation Standards

**Markdown Formatting:**

- Structured sections with clear headings
- Emojis for visual scanning (✅/❌/⚠️)
- Code blocks for technical commands/snippets
- Tables for version comparisons
- Bold for emphasis on critical information
- Links to authoritative sources

**Source Citation:**

- Every factual claim must cite source
- Prefer authoritative sources (NVD, CISA, vendor)
- Include URLs as markdown links
- Document research date for time-sensitive info

**Readability:**

- Executive summary (2-3 sentences) for busy stakeholders
- Logical flow from problem → impact → solution
- Avoid jargon where possible; define when necessary
- Use numbered lists for sequential steps
- Use bullet lists for related items

---

## Success Metrics

### Performance Metrics

**Enrichment Speed:**

- **Baseline:** 2-4 hours per ticket (manual research)
- **Target:** 10-15 minutes per ticket (AI-assisted)
- **Measurement:** Average time from agent activation to enrichment completion
- **Goal:** 90% reduction in enrichment time

**Review Speed:**

- **Baseline:** 1-2 hours per review (ad-hoc)
- **Target:** 15-20 minutes per review (systematic)
- **Measurement:** Average time from review start to report completion
- **Goal:** 75% reduction in review time

**Analyst Productivity:**

- **Baseline:** 2-4 tickets enriched per day
- **Target:** 10-20 tickets enriched per day
- **Measurement:** Tickets enriched per analyst per day
- **Goal:** 5-10x productivity increase

---

### Quality Metrics

**Enrichment Completeness:**

- **Metric:** % of enrichments with all 12 required sections complete
- **Target:** ≥95% completeness
- **Measurement:** Run security-enrichment-completeness-checklist.md

**Review Coverage:**

- **Metric:** % of P1/P2 vulnerabilities receiving peer review
- **Target:** 100% of P1/P2, 25% of P3, 10% of P4, 5% of P5
- **Measurement:** Count of reviewed vs. total tickets by priority

**Quality Score:**

- **Metric:** Average quality score from systematic reviews
- **Target:** ≥80% (Good or Excellent)
- **Measurement:** Average of all review quality scores

**Defect Detection:**

- **Metric:** % increase in gaps/errors identified through systematic review
- **Target:** 60-70% increase vs. ad-hoc review
- **Measurement:** Compare findings before/after systematic review implementation

---

### Risk Reduction Metrics

**Mean Time to Remediation (MTTR):**

- **Baseline:** Unknown (establish baseline)
- **Target:** Reduce by 30% (through better prioritization)
- **Measurement:** Average time from enrichment to remediation completion
- **Goal:** Faster remediation of genuinely high-risk vulnerabilities

**Priority Accuracy:**

- **Metric:** % of vulnerabilities correctly prioritized (validated retrospectively)
- **Target:** ≥90% priority accuracy
- **Measurement:** Retrospective analysis of priority vs. actual exploitation/impact

**False Positive Reduction:**

- **Metric:** % reduction in low-priority alerts escalated unnecessarily
- **Target:** 40% reduction in false escalations
- **Measurement:** Track escalations that were later downgraded

---

### Learning & Improvement Metrics

**Analyst Skill Development:**

- **Metric:** Quality score improvement over time
- **Target:** 10% improvement per quarter for analysts receiving regular feedback
- **Measurement:** Track individual analyst quality scores over time

**Cognitive Bias Reduction:**

- **Metric:** % of reviews identifying cognitive bias
- **Target:** Reduce bias detection rate from 30% to <10% over 6 months
- **Measurement:** Track bias detection in reviews over time

**Knowledge Base Usage:**

- **Metric:** Agent dependency file access frequency
- **Target:** Increasing trend (indicates knowledge base value)
- **Measurement:** Log knowledge base file access by agents

---

## Dependencies & Prerequisites

### Technical Prerequisites

**BMAD Core Framework:**

- Version: 4.0+
- Components: Agent system, task framework, template engine, checklist execution

**Atlassian MCP Server:**

- Status: Must be installed and configured
- Cloud ID: `934c63a0-0b96-4d46-b906-0f8c1c85c5d7`
- Permissions: Read/Write JIRA tickets, Add comments, Edit custom fields

**Perplexity MCP Server:**

- Status: Must be installed and configured
- API Access: Valid Perplexity API key
- Tools: search, reason, deep_research

**JIRA Custom Fields:**

- Must be created in JIRA project before agent use:
  - CVE ID (text field)
  - CVSS Score (number field, decimal)
  - EPSS Score (number field, decimal 0-1)
  - KEV Status (dropdown: Listed / Not Listed)
  - Affected Product (text field)
  - Affected Versions (text field)
  - Patch Status (dropdown: Available / Not Available / Vendor Investigating)
  - Patch Version (text field)

---

### Organizational Prerequisites

**Security Operations Team:**

- Minimum 2 security analysts trained on BMAD framework
- 1 senior analyst/lead for quality review
- Access to JIRA Project AOD

**Process Alignment:**

- Vulnerability management process defined
- Remediation workflows established
- SLA timelines approved by leadership
- Escalation procedures documented

**Knowledge Requirements:**

- Basic understanding of CVE/CVSS systems
- Familiarity with JIRA ticketing
- Willingness to adopt AI-assisted workflows
- Commitment to peer review culture

---

### Data Prerequisites

**JIRA Project Setup:**

- Project Key: AOD
- Issue Type: Security Alert
- Custom fields configured (see above)
- Workflows defined for alert lifecycle

**Initial Baseline:**

- Sample of historical enrichments for comparison
- Current MTTR measurements
- Current analyst productivity metrics

---

## Risk Assessment

### Technical Risks

**Risk 1: Perplexity MCP Availability**

- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Graceful degradation to manual research; clear error messaging; fallback workflows documented
- **Contingency:** Maintain manual enrichment procedures as backup

**Risk 2: AI Hallucinations**

- **Probability:** Medium
- **Impact:** High (incorrect vulnerability assessments)
- **Mitigation:**
  - Mandatory source citation validation
  - Systematic peer review for P1/P2
  - Fact-checking using verify-security-claims.md
  - Training on hallucination detection
- **Contingency:** Human validation of all critical claims

**Risk 3: JIRA MCP Integration Failures**

- **Probability:** Low
- **Impact:** Medium
- **Mitigation:**
  - Error handling with retry logic
  - Fallback to manual JIRA updates
  - Regular integration testing
- **Contingency:** Console-based enrichment output for manual copy/paste

---

### Process Risks

**Risk 4: Analyst Resistance to AI Tools**

- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:**
  - Comprehensive training on benefits
  - Demonstrate 90% time savings
  - Emphasize AI as assistant, not replacement
  - Show quality improvements from systematic review
- **Contingency:** Opt-in pilot program before mandatory adoption

**Risk 5: Over-Reliance on AI Without Validation**

- **Probability:** Medium
- **Impact:** High
- **Mitigation:**
  - Mandatory peer review for P1/P2
  - Source citation requirements
  - Cognitive bias detection
  - Regular quality audits
- **Contingency:** Increase review sampling rates if quality declines

**Risk 6: Alert Fatigue Despite Improvements**

- **Probability:** Low
- **Impact:** Medium
- **Mitigation:**
  - Strict priority framework enforcement
  - Focus on EPSS + KEV, not just CVSS
  - Metrics tracking to demonstrate reduced noise
- **Contingency:** Further refine priority framework based on data

---

### Security Risks

**Risk 7: Prompt Injection Attacks**

- **Probability:** Low
- **Impact:** Medium
- **Mitigation:**
  - Input sanitization for CVE IDs
  - Perplexity MCP has built-in safeguards
  - Monitoring for anomalous AI responses
- **Contingency:** Manual review of suspicious AI outputs

**Risk 8: Data Exposure Through AI Research**

- **Probability:** Low
- **Impact:** High
- **Mitigation:**
  - Never include sensitive internal data in Perplexity queries
  - Research only public CVE information
  - No organizational secrets in prompts
- **Contingency:** Audit Perplexity queries for sensitive data

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)

**Deliverables:**

- ✅ Agent definitions (Security Analyst, Security Reviewer)
- ✅ Core task procedures (7 tasks)
- ✅ Templates (5 templates)
- ✅ Checklists (8 checklists)
- ✅ Configuration (config.yaml)
- ✅ Knowledge bases (6 knowledge bases)

**Activities:**

- Define agent personas and commands
- Write task procedures and workflows
- Create YAML templates
- Develop quality checklists
- Document vulnerability management frameworks
- Create expansion pack configuration

**Success Criteria:**

- All artifacts written and validated
- BMAD framework integration tested
- No build/validation errors

---

### Phase 2: Integration & Testing (Weeks 3-4)

**Deliverables:**

- ✅ JIRA MCP integration working
- ✅ Perplexity MCP integration working
- ✅ JIRA custom fields configured
- ✅ End-to-end workflow tested
- ✅ Documentation (README, user guide)

**Activities:**

- Configure JIRA custom fields in Project AOD
- Test Atlassian MCP tools (read/write/comment)
- Test Perplexity MCP tools (search/reason/deep_research)
- Execute complete enrichment workflow on test ticket
- Execute complete review workflow on test ticket
- Document setup procedures and user guide

**Success Criteria:**

- Successful enrichment of 5 test tickets
- Successful review of 5 test enrichments
- Average enrichment time <15 minutes
- All integration points working
- Documentation complete

---

### Phase 3: Pilot Program (Weeks 5-6)

**Deliverables:**

- ✅ 2 analysts trained and using agents
- ✅ 20 real tickets enriched
- ✅ 10 real reviews completed
- ✅ Metrics baseline established
- ✅ Feedback collected and incorporated

**Activities:**

- Train 2 security analysts on BMAD-1898
- Enrich 20 real security alert tickets
- Review 10 enriched tickets (P1/P2 mandatory)
- Collect metrics (time, quality scores, defects found)
- Gather analyst feedback
- Refine workflows based on feedback

**Success Criteria:**

- 90% reduction in enrichment time vs. baseline
- ≥80% average quality score
- Positive analyst feedback (net promoter score ≥7/10)
- Zero critical errors or hallucinations missed
- Identified improvements incorporated

---

### Phase 4: Full Deployment (Weeks 7-8)

**Deliverables:**

- ✅ All analysts trained
- ✅ BMAD-1898 as standard enrichment process
- ✅ Metrics dashboard implemented
- ✅ Continuous improvement process established
- ✅ Retrospective completed

**Activities:**

- Train remaining security analysts
- Transition all enrichment to BMAD-1898 workflow
- Implement metrics tracking dashboard
- Establish weekly quality review meetings
- Document lessons learned
- Plan future enhancements (v1.1, v2.0)

**Success Criteria:**

- 100% of new security alerts enriched via BMAD-1898
- 100% of P1/P2 vulnerabilities peer reviewed
- Metrics show sustained improvement
- Team satisfied with workflow
- Backlog cleared of unenriched alerts

---

### Phase 5: Continuous Improvement (Ongoing)

**Activities:**

- Weekly quality metrics review
- Monthly analyst skill development sessions
- Quarterly knowledge base updates
- Bi-annual priority framework review
- Annual expansion pack version upgrade

**Success Criteria:**

- Quality scores trending upward
- MTTR trending downward
- Analyst satisfaction maintained
- Zero security incidents from missed vulnerabilities

---

## Appendices

### Appendix A: BMAD Expansion Pack Structure

```
expansion-packs/bmad-1898-engineering/
├── README.md
├── CHANGELOG.md
├── agents/
│   ├── security-analyst.md
│   └── security-reviewer.md
├── tasks/
│   ├── enrich-security-alert.md
│   ├── review-security-analysis.md
│   ├── research-cve.md
│   ├── verify-security-claims.md
│   ├── map-to-attack.md
│   ├── assess-business-impact.md
│   └── create-remediation-plan.md
├── templates/
│   ├── security-enrichment-tmpl.yaml
│   ├── security-review-report-tmpl.yaml
│   ├── cve-research-report-tmpl.yaml
│   ├── remediation-plan-tmpl.yaml
│   └── priority-assessment-tmpl.yaml
├── checklists/
│   ├── security-enrichment-completeness-checklist.md
│   ├── technical-accuracy-checklist.md
│   ├── completeness-checklist.md
│   ├── actionability-checklist.md
│   ├── contextualization-checklist.md
│   ├── documentation-quality-checklist.md
│   ├── attack-mapping-checklist.md
│   └── cognitive-bias-checklist.md
├── workflows/
│   ├── security-alert-enrichment-workflow.yaml
│   ├── security-analysis-review-workflow.yaml
│   └── vulnerability-lifecycle-workflow.yaml
├── data/
│   ├── bmad-kb.md
│   ├── vulnerability-management-kb.md
│   ├── cognitive-bias-patterns.md
│   ├── mitre-attack-mapping-guide.md
│   ├── priority-framework.md
│   └── remediation-best-practices.md
├── config/
│   └── expansion-config.yaml
└── docs/
    ├── user-guide.md
    ├── setup-guide.md
    ├── quick-reference.md
    └── troubleshooting.md
```

---

### Appendix B: JIRA Custom Field Definitions

| Field Name        | Field Type          | Field ID (Example) | Values/Format                                    | Purpose                          |
| ----------------- | ------------------- | ------------------ | ------------------------------------------------ | -------------------------------- |
| CVE ID            | Text (single line)  | customfield_10050  | CVE-YYYY-NNNNN                                   | Primary vulnerability identifier |
| CVSS Score        | Number              | customfield_10051  | 0.0 - 10.0                                       | CVSS v3.1 Base Score             |
| EPSS Score        | Number              | customfield_10052  | 0.00 - 1.00                                      | Exploitation probability         |
| KEV Status        | Select (dropdown)   | customfield_10053  | Listed / Not Listed                              | CISA KEV catalog status          |
| Affected Product  | Text (single line)  | customfield_10054  | Product name                                     | Software affected                |
| Affected Versions | Text (multi-line)   | customfield_10055  | Version ranges                                   | Vulnerable versions              |
| Patch Status      | Select (dropdown)   | customfield_10056  | Available / Not Available / Vendor Investigating | Patch availability               |
| Patch Version     | Text (single line)  | customfield_10057  | Version number                                   | Patched version                  |
| Priority          | Priority (standard) | priority           | Critical / High / Medium / Low                   | Remediation priority             |

**Note:** Field IDs must be updated in `.bmad-1898/config.yaml` to match actual JIRA instance.

---

### Appendix C: Priority Framework Decision Matrix

| Factor          | P1 (Critical)    | P2 (High)                  | P3 (Medium)       | P4 (Standard)    | P5 (Low)              |
| --------------- | ---------------- | -------------------------- | ----------------- | ---------------- | --------------------- |
| **CVSS**        | 9.0-10.0         | 7.0-8.9                    | 6.0-6.9           | 4.0-5.9          | 0.1-3.9               |
| **EPSS**        | >0.9 (90%+)      | 0.7-0.9                    | 0.4-0.7           | 0.1-0.4          | <0.1                  |
| **KEV**         | Listed + Active  | Listed                     | Not Listed        | Not Listed       | Not Listed            |
| **Exposure**    | Internet-facing  | Internet/Critical Internal | Internal          | Internal         | Isolated              |
| **Criticality** | Critical systems | High-value systems         | Important systems | Standard systems | Low-value systems     |
| **Exploit**     | Weaponized       | Public exploit             | PoC available     | No exploit       | No exploit            |
| **SLA**         | <24 hours        | <7 days                    | <30 days          | <60 days         | <90 days (monitoring) |

**Note:** Priority is determined by HIGHEST applicable category, not all factors. One P1 factor elevates to P1 priority.

---

### Appendix D: Agent Command Reference

#### Security Analyst Commands

```
*help                        - Show available commands
*enrich {JIRA-ID}           - Run complete enrichment workflow
*research-cve {CVE-ID}      - Research specific CVE
*assess-priority {JIRA-ID}  - Assess vulnerability priority
*map-attack {CVE-ID}        - Map to MITRE ATT&CK
*remediation-plan {JIRA-ID} - Create remediation guidance
*business-impact {JIRA-ID}  - Assess business impact
*yolo                       - Toggle YOLO mode
*exit                       - Exit Security Analyst persona
```

#### Security Reviewer Commands

```
*help                        - Show available commands
*review {JIRA-ID}           - Run complete review workflow
*verify-claims {JIRA-ID}    - Fact-check security assertions
*check-bias {JIRA-ID}       - Identify cognitive biases
*validate-accuracy {JIRA-ID}- Verify technical accuracy
*assess-completeness {JIRA-ID}- Check enrichment completeness
*yolo                       - Toggle YOLO mode
*exit                       - Exit Security Reviewer persona
```

---

### Appendix E: Sample Enrichment Comment

```markdown
## Security Alert Enrichment

### Executive Summary

CVE-2024-1234 is a critical remote code execution vulnerability in Apache Struts 2.5.30 allowing unauthenticated network attackers to execute arbitrary code. CISA KEV-listed with active exploitation observed. Patch available in version 2.5.33. **Immediate remediation required (P1).**

### Vulnerability Classification

- **CVE ID**: CVE-2024-1234
- **CWE**: CWE-94 (Improper Control of Generation of Code)
- **Type**: Remote Code Execution (RCE)
- **Published**: 2024-03-15

### Severity Metrics

- **CVSS v3.1 Base Score**: 9.8 (Critical)
- **CVSS Vector**: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- **EPSS Score**: 0.85 (85% exploitation probability within 30 days)
- **EPSS Percentile**: 95th percentile
- **CISA KEV**: ✅ Listed (Added: 2024-03-20, Due Date: 2024-04-10)

### Affected Software

- **Product**: Apache Struts 2
- **Vendor**: Apache Software Foundation
- **Vulnerable Versions**: 2.5.0 through 2.5.30
- **Patched Versions**: 2.5.33 and later
- **Configuration Requirements**: Default configuration vulnerable

### Exploitation Context

- **Attack Vector**: Network (remotely exploitable)
- **Attack Complexity**: Low (easy to exploit)
- **Privileges Required**: None (unauthenticated)
- **User Interaction**: None required
- **Scope**: Unchanged
- **Impact**:
  - **Confidentiality**: High (full system access)
  - **Integrity**: High (arbitrary code execution)
  - **Availability**: High (complete system compromise)

### Exploit Intelligence

- **Public Exploits**: ✅ Available
  - Exploit-DB: https://www.exploit-db.com/exploits/51234
  - Metasploit module: exploit/multi/http/struts2_rce
- **Exploit Maturity**: Functional (reliable exploitation)
- **Weaponization**: ✅ In Malware (ransomware campaigns)
- **Active Exploitation**: ✅ Confirmed in Wild
  - CISA confirmed active exploitation by ransomware groups
  - Honeypot data shows widespread scanning for vulnerable instances

### Business Impact Assessment

- **Potential Impact**: Complete server compromise enabling data exfiltration, lateral movement, ransomware deployment
- **Affected Systems**:
  - Production web application servers (5 instances)
  - All internet-facing
- **System Criticality**: Critical (customer-facing applications)
- **Data Sensitivity**: PII, PCI data (customer payment information)
- **Regulatory Implications**: PCI-DSS compliance violation if breached, potential GDPR fines

### Remediation Guidance

#### Patch Information

- **Patched Version**: Apache Struts 2.5.33
- **Release Date**: 2024-03-18
- **Vendor Advisory**: https://cwiki.apache.org/confluence/display/WW/S2-062
- **Patch Download**: https://struts.apache.org/download.cgi

#### Remediation Steps

1. **Backup:** Take full backup of affected servers
2. **Testing:** Test upgrade to 2.5.33 in staging environment
3. **Deployment:** Deploy to production during maintenance window
4. **Verification:** Run version check: `java -jar struts2-core-*.jar --version`
5. **Monitoring:** Enable WAF rules for Struts2 exploit attempts

#### Workarounds (if patch cannot be immediately deployed)

- **Temporary Mitigation**: Implement WAF rules blocking OGNL expression patterns
- **Limitations**: Workaround may not block all exploitation variants

#### Verification

1. Confirm running version: `java -jar struts2-core-*.jar --version` shows 2.5.33
2. Vulnerability scan confirms CVE-2024-1234 resolved
3. No suspicious activity in application logs

### MITRE ATT&CK Mapping

- **Tactic**: Initial Access (TA0001)
- **Technique**: Exploit Public-Facing Application (T1190)
- **Detection**: Monitor web server logs for OGNL expressions, unusual POST parameters, error messages indicating code execution attempts

### Attack Surface Analysis

- **Exposure**: Internet-Facing (all 5 instances publicly accessible)
- **Access Requirements**: HTTP/HTTPS access to vulnerable endpoints
- **Lateral Movement Risk**: High (compromised web servers can pivot to internal network)
- **Dependencies**: Database servers, authentication services

### Priority Recommendation

- **Recommended Priority**: **P1 (Critical - Immediate Remediation)**
- **Remediation Timeline**: < 24 hours
- **Rationale**:
  - CVSS Severity: Critical (9.8)
  - EPSS Probability: Very High (85% - 95th percentile)
  - KEV Status: ✅ Listed (CISA confirmed active exploitation)
  - System Criticality: Critical (customer-facing, PCI data)
  - Exploit Availability: ✅ Weaponized in ransomware
  - Active Exploitation: ✅ Confirmed

### Related Information

- **Similar CVEs**: CVE-2023-XXXX (previous Struts2 RCE), CVE-2022-XXXX
- **Vendor Track Record**: History of RCE vulnerabilities in Struts2
- **References**:
  - NVD: https://nvd.nist.gov/vuln/detail/CVE-2024-1234
  - CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - Apache Advisory: https://cwiki.apache.org/confluence/display/WW/S2-062
  - EPSS: https://www.first.org/epss

---

🤖 _Enrichment generated using Perplexity AI research_
_Generated by_: Security Analyst Agent (BMAD-1898)
_Date_: 2025-11-06
_Sources_: NVD, CISA KEV, FIRST EPSS, Apache Software Foundation
_Review Status_: Pending Review
```

---

### Appendix F: Glossary

**ACR (Asset Criticality Rating):** Organizational rating (0-10) indicating business criticality of an asset.

**CVSS (Common Vulnerability Scoring System):** Standardized vulnerability severity scoring system (0-10 scale).

**EPSS (Exploit Prediction Scoring System):** Machine learning-based probability score (0-1) predicting likelihood of exploitation within 30 days.

**KEV (Known Exploited Vulnerabilities):** CISA catalog of vulnerabilities with confirmed active exploitation in the wild.

**MITRE ATT&CK:** Framework describing adversary tactics, techniques, and procedures (TTPs).

**MTTR (Mean Time to Remediation):** Average time from vulnerability discovery to remediation completion.

**NVD (National Vulnerability Database):** NIST repository of CVE information and CVSS scores.

**POC (Proof of Concept):** Demonstration code showing vulnerability exploitation is possible.

**RCE (Remote Code Execution):** Vulnerability allowing attackers to execute arbitrary code remotely.

**SLA (Service Level Agreement):** Commitment to remediation timeline based on vulnerability priority.

---

## Document Approval

**Prepared by:**
Mary, Business Analyst
Date: 2025-11-06

**Review Required:**
Product Owner (PO) - Story prioritization and acceptance criteria validation
Security Operations Lead - Technical feasibility and resource allocation
BMAD Framework Architect - Integration and dependency validation

**Next Steps:**

1. Schedule requirements review meeting with PO
2. Create epic and user story tickets in JIRA
3. Estimate story points and sprint allocation
4. Begin Phase 1 implementation (agent definitions)

---

**END OF REQUIREMENTS DOCUMENT**

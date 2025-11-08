# Epic 1: Security Analyst Agent & Vulnerability Enrichment Automation

## Epic Goal

Create an AI-powered Security Analyst agent that automates vulnerability enrichment workflows, dramatically reducing manual research time from hours to minutes while improving accuracy through AI-assisted CVE research, multi-factor priority assessment, and systematic JIRA integration.

## Background

BMAD-1898 Engineering expansion pack addresses the challenge of managing 50,000+ annual CVE disclosures in enterprise security operations. Manual vulnerability enrichment is time-intensive, requiring analysts to:

1. **Research CVE Intelligence** - Gather CVSS, EPSS, KEV status, exploit availability, patch information from multiple authoritative sources
2. **Assess Risk Context** - Calculate priority based on vulnerability severity, exploitation probability, business impact, and system criticality
3. **Document Findings** - Create structured enrichment reports with actionable remediation guidance
4. **Update Tracking Systems** - Manually populate JIRA fields and post enrichment comments

This manual process consumes 15-45 minutes per CVE, creating a bottleneck that delays remediation and increases risk exposure.

The Security Analyst agent (Epic 1) provides:

- **90% faster enrichment** - AI-assisted research reduces 30-minute tasks to 3 minutes
- **Comprehensive intelligence gathering** - Perplexity MCP queries authoritative sources (NVD, CISA KEV, FIRST EPSS, vendor advisories)
- **Multi-factor priority assessment** - CVSS + EPSS + KEV + Business Context = accurate risk prioritization
- **Automated JIRA integration** - Read tickets, post enrichment comments, update custom fields
- **Structured documentation** - Consistent enrichment format with MITRE ATT&CK mapping
- **Reduced analyst burnout** - Automate repetitive research, free analysts for strategic work

## Integration Context

**Security Analyst Agent** (Story 1.1) orchestrates complete enrichment workflow:

- Reads JIRA security alert tickets (Story 1.2)
- Researches CVEs using Perplexity MCP (Story 1.3)
- Creates structured enrichment documentation (Story 1.4)
- Posts enrichment as JIRA comment (Story 1.5)
- Updates JIRA custom fields (Story 1.6)
- Calculates multi-factor priority (Story 1.7)

**Security Reviewer Agent** (Epic 2) validates enrichment quality:

- Reviews analyst enrichments using 8-dimensional quality assessment
- Verifies factual claims against authoritative sources
- Detects cognitive biases and systematic errors
- Provides constructive feedback for continuous improvement

**Knowledge Base Integration** (Epic 4) provides reference materials:

- Vulnerability management frameworks (Story 4.1)
- Cognitive bias patterns for quality review (Story 4.2)
- MITRE ATT&CK mapping guidelines (Story 4.3)

**Project Configuration** (config.yaml) defines:

- JIRA Cloud ID and custom field mappings
- Atlassian MCP integration settings
- Perplexity MCP configuration
- Enrichment workflow parameters

## Prerequisites

**Required MCP Servers:**

- **Atlassian JIRA MCP** - JIRA ticket reading, comment posting, field updates
  - Tools: `mcp__atlassian__getJiraIssue`, `mcp__atlassian__addCommentToJiraIssue`, `mcp__atlassian__updateJiraIssue`
  - Installation: Follow Atlassian MCP server setup documentation
  - Configuration: JIRA Cloud ID and API credentials in project config

- **Perplexity MCP** - AI-assisted CVE research and intelligence gathering
  - Tools: `mcp__perplexity__search`, `mcp__perplexity__reason`, `mcp__perplexity__deep_research`
  - Status: Available by default in Claude Code
  - Usage: Severity-based tool selection (Critical→deep_research, High→reason, Medium/Low→search)

## Stories

### Story 1.1: Security Analyst Agent Creation

**As a** security analyst,
**I want** a specialized BMAD agent persona,
**so that** I can activate consistent enrichment workflows with a single command.

**Acceptance Criteria:**

1. Security Analyst agent definition complete with commands, dependencies, persona
2. Agent can be activated via `/security-analyst` or equivalent
3. Agent displays available commands on activation
4. Agent greets user and runs `*help` on startup

**Integration Requirements:**

- Agent orchestrates Stories 1.2-1.7 via commands
- Agent uses tasks: `read-jira-ticket`, `research-cve`, `assess-vulnerability-priority`
- Agent uses template: `security-enrichment-tmpl.yaml`
- Agent references knowledge base: `bmad-kb.md`

**Status:** Done (Completed 2025-11-06)

---

### Story 1.2: JIRA Ticket Reading

**As a** Security Analyst agent,
**I want** to read JIRA security alert tickets via Atlassian MCP,
**so that** I can extract CVE IDs and initial context.

**Acceptance Criteria:**

1. Agent can read JIRA tickets using `mcp__atlassian__getJiraIssue`
2. Agent extracts CVE ID from ticket summary or description
3. Agent identifies affected systems from ticket fields
4. Agent handles tickets without CVE IDs gracefully
5. Agent processes all CVEs when multiple are present
6. Agent validates configuration file exists and contains required JIRA fields

**Integration Requirements:**

- Task `read-jira-ticket.md` implements JIRA reading workflow
- Validates `config.yaml` contains JIRA Cloud ID and custom field mappings
- Extracts CVE IDs for Story 1.3 research input
- Extracts affected systems for Story 1.7 priority assessment

**Status:** Done (Completed 2025-11-07)

---

### Story 1.3: AI-Assisted CVE Research

**As a** Security Analyst agent,
**I want** to research CVEs using Perplexity MCP,
**so that** I can gather comprehensive vulnerability intelligence in minutes.

**Acceptance Criteria:**

1. Agent constructs research queries including CVSS, EPSS, KEV, exploits, patches, ATT&CK
2. Agent selects appropriate Perplexity tool (search/reason/deep_research) based on severity
3. Agent receives structured research findings
4. Agent cites authoritative sources (NVD, CISA, vendor advisories)
5. Agent handles errors gracefully (timeouts, missing data, conflicts)

**Integration Requirements:**

- Task `research-cve.md` implements Perplexity-based research workflow
- Severity-based tool selection: Critical→deep_research, High→reason, Medium/Low→search
- Research output feeds Story 1.4 enrichment documentation
- Source citations required for Story 2.5 fact verification

**Status:** Done (Completed 2025-11-07)

---

### Story 1.4: Structured Enrichment Documentation

**As a** Security Analyst agent,
**I want** to structure research findings using the enrichment template,
**so that** all enrichment comments follow consistent, comprehensive format.

**Acceptance Criteria:**

1. Agent uses security-enrichment-tmpl.yaml
2. All 12 sections of template completed
3. Executive summary provides 2-3 sentence overview
4. Severity metrics include CVSS, EPSS, KEV
5. MITRE ATT&CK mapping included
6. Priority recommendation with rationale

**Integration Requirements:**

- Template `security-enrichment-tmpl.yaml` defines enrichment document structure
- Template populated with Story 1.3 research output
- Template includes Story 1.7 priority assessment
- Enrichment document posted to JIRA in Story 1.5

**Status:** Done (Completed 2025-11-07)

---

### Story 1.5: JIRA Enrichment Comment

**As a** Security Analyst agent,
**I want** to add structured enrichment as JIRA comment,
**so that** stakeholders can review findings in familiar JIRA interface.

**Acceptance Criteria:**

1. Agent adds comment using `mcp__atlassian__addCommentToJiraIssue`
2. Comment formatted in markdown with structured sections
3. Emojis used for visual scanning (✅/❌/⚠️)
4. Source citations as links
5. Timestamp and generator attribution included

**Integration Requirements:**

- Task `post-enrichment-comment.md` implements JIRA comment posting
- Input: Enrichment document from Story 1.4
- JIRA-compatible markdown formatting with emoji indicators
- Error handling: permission denied, network errors, comment size limits

**Status:** Draft (Pending Review)

---

### Story 1.6: JIRA Custom Field Updates

**As a** Security Analyst agent,
**I want** to update JIRA custom fields with enrichment data,
**so that** teams can filter, report, and automate based on enrichment results.

**Acceptance Criteria:**

1. Agent updates custom fields using `mcp__atlassian__updateJiraIssue`
2. Agent maps enrichment data to JIRA fields
3. Agent validates field types before updating
4. Agent handles field update errors gracefully

**Integration Requirements:**

- Task `update-jira-fields.md` implements field update workflow
- Custom field mappings from `config.yaml`
- Updates: CVSS, EPSS, KEV status, priority, affected systems
- Executes after Story 1.5 comment posting

**Status:** Done (Completed 2025-11-07)

---

### Story 1.7: Multi-Factor Priority Assessment

**As a** Security Analyst agent,
**I want** to calculate vulnerability priority using CVSS + EPSS + KEV + Business Context,
**so that** remediation efforts focus on genuine exploitable threats.

**Acceptance Criteria:**

1. Agent considers all priority factors: CVSS, EPSS, KEV, system criticality (ACR), exposure, exploits
2. Agent applies priority framework (P1-P5)
3. Agent provides rationale for priority level
4. Agent identifies SLA remediation timeline

**Integration Requirements:**

- Task `assess-vulnerability-priority.md` implements multi-factor priority calculation
- Priority framework: P1 (24h), P2 (72h), P3 (7d), P4 (30d), P5 (90d)
- Priority assessment included in Story 1.4 enrichment documentation
- Business context from Story 1.2 JIRA ticket data

**Status:** Done (Completed 2025-11-07)

---

## Success Metrics

**Efficiency Gains:**
- 90% reduction in enrichment time (30 min → 3 min per CVE)
- 10x increase in daily enrichment capacity per analyst

**Quality Improvements:**
- 100% consistent enrichment format via template
- Multi-factor priority accuracy (validated by Epic 2 review)
- Authoritative source citations for all claims

**Operational Impact:**
- Reduced analyst burnout through automation of repetitive research
- Faster vulnerability remediation through accurate prioritization
- Improved stakeholder visibility via JIRA integration

## Dependencies

**External:**
- Atlassian JIRA MCP server (installed and configured)
- Perplexity MCP (available in Claude Code)
- JIRA Cloud instance with custom fields configured

**Internal:**
- Epic 4 knowledge base (Stories 4.1, 4.2, 4.3) for reference materials
- `config.yaml` with JIRA Cloud ID and custom field mappings

## Risks and Mitigations

**Risk:** Perplexity API rate limiting or downtime
**Mitigation:** Implement exponential backoff, fallback to manual research mode

**Risk:** JIRA API permission errors
**Mitigation:** Comprehensive error handling, clear user guidance for permission configuration

**Risk:** Inaccurate priority assessment
**Mitigation:** Epic 2 quality review validates priority decisions, fact-checks claims

**Risk:** Over-reliance on AI research
**Mitigation:** Source citation requirements, analyst validation step, Epic 2 peer review

## Timeline

- **Story 1.1-1.2:** Agent creation and JIRA reading (Completed 2025-11-06/07)
- **Story 1.3-1.4:** CVE research and enrichment templates (Completed 2025-11-07)
- **Story 1.5-1.7:** JIRA integration and priority assessment (In Progress 2025-11-08)

**Epic Completion Target:** 2025-11-10 (all stories Done, QA reviewed)

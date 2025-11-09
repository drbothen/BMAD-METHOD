# Epic 5: User Documentation & Usage Guide

## Epic Goal

Create comprehensive user-facing documentation enabling security operations teams to successfully install, configure, and use the bmad-1898-engineering expansion pack for vulnerability management with minimal onboarding friction and maximum operational effectiveness.

## Background

BMAD-1898 Engineering expansion pack provides powerful AI-assisted security automation, but adoption success depends on clear, actionable documentation that enables teams to:

1. **Install and Configure Correctly** - Set up JIRA integration, MCP servers, custom fields, and config.yaml on first attempt
2. **Use Agents Effectively** - Understand agent personas, commands, workflows, and best practices
3. **Understand Technical Workflows** - Deep dive into enrichment and review workflow stages for optimization and troubleshooting
4. **Customize for Organization** - Adapt configuration for team size, priority schemes, and operational requirements
5. **Troubleshoot Issues** - Resolve common problems without external support
6. **Measure and Improve** - Track metrics and continuously improve quality

Without comprehensive documentation, teams face:

- Installation failures and misconfiguration
- Inconsistent agent usage and suboptimal workflows
- Inability to troubleshoot issues independently
- Missed opportunities for customization
- Poor adoption and user frustration

The User Documentation & Usage Guide (Epic 5) provides:

- **30-minute quickstart** - From installation to first enrichment
- **Complete agent usage guides** - Security Analyst and Security Reviewer agent documentation
- **Technical workflow deep dives** - 8-stage enrichment and 7-stage review workflows
- **Configuration reference** - Complete config.yaml customization guide
- **Troubleshooting & FAQ** - Self-service problem resolution
- **Metrics and improvement** - Continuous quality optimization

## Integration Context

**Installation Foundation** (Story 5.1) enables successful setup:

- Prerequisites verification (JIRA Cloud, MCP servers, environment)
- Custom field creation (8 JIRA fields with IDs)
- Config.yaml configuration (JIRA, priority mapping, review triggers)
- Installation verification checklist
- 30-minute quickstart guide

**Agent Usage Guides** (Stories 5.2, 5.3) enable effective operation:

- Security Analyst agent complete command reference
- Security Reviewer agent systematic review guide
- Workflow walkthroughs with examples
- Best practices and tips

**Technical Deep Dives** (Stories 5.4, 5.5, 5.6, 5.7) enable optimization:

- Enrichment workflow stage-by-stage specifications
- Review workflow dimension-by-dimension breakdown
- Complete vulnerability lifecycle from alert to closure
- Priority-based review triggering logic

**Configuration & Operations** (Stories 5.8, 5.9, 5.10) enable customization:

- Configuration reference with advanced scenarios
- Metrics, reporting, and continuous improvement
- Troubleshooting, FAQ, and best practices

**User Documentation Location:**
All user-facing documentation in `expansion-packs/bmad-1898-engineering/docs/user-guide/`

## Prerequisites

**Required Artifacts (from previous epics):**

- **Epic 1 Complete** - Security Analyst agent and enrichment workflow implemented
  - Agent: `agents/security-analyst.md`
  - Tasks: `tasks/enrich-security-ticket.md`, `tasks/research-cve.md`
  - Template: `templates/security-enrichment-tmpl.yaml`
  - Workflow: `workflows/security-alert-enrichment-workflow.yaml`

- **Epic 2 Complete** - Security Reviewer agent and review workflow implemented
  - Agent: `agents/security-reviewer.md`
  - Checklists: 8 quality dimension checklists in `checklists/`
  - Tasks: `tasks/review-enrichment.md`, `tasks/fact-check.md`
  - Workflow: `workflows/security-analysis-review-workflow.yaml`

- **Epic 3 Complete** - Workflow integration and orchestration operational
  - Workflows tested and validated
  - MCP integrations working (Atlassian, Perplexity)
  - Priority-based review triggering functional

- **Epic 4 Complete** - Knowledge bases available
  - `data/bmad-kb.md` - Vulnerability management knowledge
  - `data/cognitive-bias-patterns.md` - Bias detection guide
  - `data/mitre-attack-mapping-guide.md` - ATT&CK mapping reference

**Documentation Standards:**

- **User-Facing Language** - Clear, jargon-free, actionable
- **Step-by-Step Instructions** - Numbered procedures with success criteria
- **Examples and Screenshots** - Visual aids for complex procedures
- **Troubleshooting Sections** - Common issues with diagnostic steps
- **Cross-References** - Links between related documentation sections

## Stories

### Story 5.1: Installation & Initial Setup Guide

**As a** security operations team member,
**I want** comprehensive installation and setup documentation,
**so that** I can quickly install and configure the bmad-1898-engineering expansion pack for my team.

**Acceptance Criteria:**

1. Documentation covers all prerequisites (JIRA Cloud, Atlassian MCP, Perplexity MCP, Claude Code environment)
2. Step-by-step installation instructions provided for expansion pack installation
3. JIRA custom field creation guide with screenshots and field ID mapping
4. config.yaml configuration walkthrough with all required sections
5. Initial setup verification checklist ensures successful installation
6. Quickstart guide enables first enrichment within 30 minutes of installation

**Integration Requirements:**

- Prerequisites validation checklist
- JIRA custom field specifications (8 fields)
- config.yaml template with annotations
- MCP server setup verification
- End-to-end smoke test procedure

**Status:** Done (Completed 2025-11-08)

---

### Story 5.2: Security Analyst Agent Usage Guide

**As a** security analyst,
**I want** comprehensive usage documentation for the Security Analyst agent,
**so that** I can effectively use all agent commands and workflows to enrich vulnerability tickets.

**Acceptance Criteria:**

1. Documentation covers Security Analyst agent activation and persona overview
2. Complete command reference for all 6 commands (*help, *enrich-ticket, *research-cve, *assess-priority, *map-attack, *exit)
3. Step-by-step enrichment workflow walkthrough with example CVE
4. Best practices for effective vulnerability enrichment
5. Common troubleshooting scenarios with solutions
6. Understanding enrichment outputs and artifacts

**Integration Requirements:**

- Agent activation instructions
- Complete command reference with usage examples
- Workflow walkthrough (8 stages)
- Best practices guide
- Output artifact documentation

**Status:** Done (Completed 2025-11-08)

---

### Story 5.3: Security Reviewer Agent Usage Guide

**As a** security reviewer,
**I want** comprehensive usage documentation for the Security Reviewer agent,
**so that** I can effectively review enrichments using systematic quality evaluation and provide constructive feedback.

**Acceptance Criteria:**

1. Documentation covers Security Reviewer agent activation and persona overview
2. Complete command reference for all 6 commands (*help, *review-enrichment, *fact-check, *detect-bias, *generate-report, *exit)
3. Detailed explanation of 8 quality dimensions with scoring methodology
4. Best practices for conducting blameless, constructive peer reviews
5. Understanding review outputs and feedback delivery
6. Examples of excellent, good, and needs-improvement enrichments with review feedback

**Integration Requirements:**

- Agent activation and persona explanation
- Command reference with examples
- 8-dimension quality framework documentation
- Blameless review culture principles
- Review output format and delivery

**Status:** Done (Completed 2025-11-08)

---

### Story 5.4: Security Alert Enrichment Workflow Deep Dive

**As a** security analyst or security operations manager,
**I want** detailed technical documentation of the enrichment workflow,
**so that** I understand each stage deeply, can optimize workflow performance, and troubleshoot stage-specific issues.

**Acceptance Criteria:**

1. Documentation covers all 8 workflow stages with detailed technical specifications
2. Each stage includes inputs, outputs, actions, success criteria, error handling, and timing
3. Integration points documented (Atlassian MCP, Perplexity MCP, local file system)
4. Performance optimization techniques for each stage
5. Stage-specific troubleshooting guide
6. Workflow state management and resume capability explained

**Integration Requirements:**

- Workflow YAML as technical source (`workflows/security-alert-enrichment-workflow.yaml`)
- Task implementation reference (`tasks/enrich-security-ticket.md`)
- MCP tool documentation
- State management specification
- Performance benchmarks

**Status:** Draft (Pending validation and implementation)

---

### Story 5.5: Security Analysis Review Workflow Deep Dive

**As a** security reviewer or quality assurance lead,
**I want** detailed technical documentation of the review workflow,
**so that** I understand each review stage, quality dimensions, and can optimize review effectiveness.

**Acceptance Criteria:**

1. Documentation covers all 7 review workflow stages with technical specifications
2. Each quality dimension explained with scoring methodology and thresholds
3. Fact verification process documented with Perplexity integration
4. Cognitive bias detection methodology explained
5. Review report structure and feedback delivery documented
6. Review workflow state management explained

**Integration Requirements:**

- Review workflow YAML (`workflows/security-analysis-review-workflow.yaml`)
- 8 quality dimension checklists
- Fact-checking task documentation
- Bias detection patterns
- Review report template

**Status:** Draft (Pending implementation)

---

### Story 5.6: Complete Vulnerability Lifecycle Guide

**As a** security operations manager,
**I want** end-to-end vulnerability lifecycle documentation,
**so that** I understand the complete workflow from alert triage to remediation closure.

**Acceptance Criteria:**

1. Complete lifecycle documentation from alert creation to closure
2. Enrichment workflow integration explained
3. Review workflow integration explained
4. Priority-based routing and SLA tracking documented
5. Remediation tracking and verification explained
6. Metrics collection and reporting integrated

**Integration Requirements:**

- Enrichment workflow (Story 5.4)
- Review workflow (Story 5.5)
- Priority framework
- SLA tracking
- Lifecycle state transitions

**Status:** Draft (Pending implementation)

---

### Story 5.7: Priority-Based Review Triggering Reference

**As a** security operations manager,
**I want** detailed documentation of priority-based review triggering logic,
**so that** I can configure appropriate review sampling rates and understand when reviews are triggered.

**Acceptance Criteria:**

1. Priority-based trigger rules documented (P1-P5 with percentages)
2. Sampling rate configuration explained
3. Blocking vs. non-blocking reviews explained
4. Reviewer assignment logic documented
5. Override mechanisms explained
6. Configuration examples for different team sizes

**Integration Requirements:**

- Priority framework (Story 1.7)
- Review workflow (Epic 2)
- Config.yaml review trigger section
- Reviewer assignment algorithms

**Status:** Draft (Pending implementation)

---

### Story 5.8: Configuration Reference & Customization Guide

**As a** security operations manager or system administrator,
**I want** comprehensive configuration reference documentation,
**so that** I can customize the expansion pack for my organization's specific requirements, team structure, and operational workflows.

**Acceptance Criteria:**

1. Complete config.yaml reference documentation with all sections explained
2. JIRA integration configuration guide with field mapping examples
3. Priority mapping customization explained
4. Review trigger customization for different team sizes and workflows
5. Reviewer assignment configuration with examples
6. Notification system configuration (JIRA, email, Slack)
7. Advanced customization scenarios with complete examples

**Integration Requirements:**

- config.yaml complete structure
- JIRA field mapping
- Priority schemes
- Review trigger rules
- Notification templates

**Status:** Draft (Pending implementation)

---

### Story 5.9: Metrics, Reporting & Continuous Improvement

**As a** security operations manager,
**I want** documentation on metrics collection, reporting, and continuous improvement,
**so that** I can track team performance, identify trends, and optimize workflows over time.

**Acceptance Criteria:**

1. Metrics collection explained (enrichment time, quality scores, review findings)
2. Reporting capabilities documented
3. Performance trend analysis explained
4. Quality improvement feedback loops documented
5. Analyst and reviewer performance tracking
6. Continuous improvement process documented

**Integration Requirements:**

- Metrics CSV structure
- Enrichment metrics (Story 1.x)
- Review metrics (Story 2.x)
- Quality scores
- Performance benchmarks

**Status:** Draft (Pending implementation)

---

### Story 5.10: Troubleshooting, FAQ & Best Practices

**As a** security analyst, security reviewer, or security operations engineer,
**I want** comprehensive troubleshooting guidance, frequently asked questions, and best practices,
**so that** I can quickly resolve common issues, avoid pitfalls, and operate the system effectively.

**Acceptance Criteria:**

1. Common installation issues documented with step-by-step solutions
2. Enrichment workflow errors cataloged with troubleshooting steps
3. Review workflow errors cataloged with troubleshooting steps
4. JIRA integration issues documented with diagnostic procedures
5. MCP connection problems documented with resolution steps
6. Best practices for analysts provided with rationale
7. Best practices for reviewers provided with rationale
8. Performance optimization tips included
9. Frequently asked questions answered clearly
10. Error message reference provided with interpretations

**Integration Requirements:**

- All workflow error scenarios
- JIRA/MCP integration issues
- Configuration problems
- Best practices from operations
- FAQ compilation

**Status:** Done (Completed 2025-11-08)

---

## Success Criteria

**Epic 5 is complete when:**

1. ✅ All 10 stories implemented and documentation created
2. ✅ User-facing documentation in `docs/user-guide/` directory
3. ✅ Installation guide enables 30-minute quickstart
4. ✅ Agent usage guides enable effective operation
5. ✅ Technical deep dives enable optimization
6. ✅ Configuration reference enables customization
7. ✅ Troubleshooting guide enables self-service support
8. ✅ All documentation cross-referenced and navigable
9. ✅ Examples and screenshots included where helpful
10. ✅ Documentation tested with new users

**Acceptance Testing:**

- New team member can install and configure in 30 minutes (Story 5.1)
- Analyst can perform first enrichment following usage guide (Story 5.2)
- Reviewer can conduct first review following usage guide (Story 5.3)
- Troubleshooting guide resolves 80% of common issues without support (Story 5.10)

## Dependencies

**Upstream (must complete before Epic 5):**

- Epic 1: Security Analyst agent and enrichment workflow
- Epic 2: Security Reviewer agent and review workflow
- Epic 3: Workflow integration and orchestration
- Epic 4: Knowledge bases

**Downstream (enabled by Epic 5):**

- User adoption and training
- Production deployment
- Customer onboarding
- Support documentation

## Risks and Mitigations

| Risk                                  | Impact | Mitigation                                        |
| ------------------------------------- | ------ | ------------------------------------------------- |
| Documentation becomes outdated        | High   | Version documentation with code, include in CI/CD |
| Screenshots become stale              | Medium | Use annotated text examples where possible        |
| User confusion despite docs           | High   | User testing before finalization, FAQ refinement  |
| Documentation too technical           | Medium | User-facing language review, examples for clarity |
| Missing edge cases in troubleshooting | Medium | Collect issues during beta testing, expand FAQ    |

## Notes

**Documentation Philosophy:**

- User-centric language (not developer-centric)
- Progressive disclosure (simple → advanced)
- Action-oriented (what to do, not just what exists)
- Example-driven (show, don't just tell)
- Troubleshooting-first (anticipate problems)

**Deliverable Location:**
All user-facing documentation: `expansion-packs/bmad-1898-engineering/docs/user-guide/`

**Documentation Maintenance:**

- Update with each feature change
- Version documentation with releases
- Solicit user feedback for improvement
- Expand FAQ based on support tickets

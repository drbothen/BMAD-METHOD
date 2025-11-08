# BMAD-1898 Engineering Expansion Pack - Source Tree

## Overview

BMAD-1898 is a security-focused expansion pack for the BMAD Method™ framework, providing AI-assisted vulnerability enrichment and systematic quality assurance for security operations teams.

## Directory Structure

```
expansion-packs/bmad-1898-engineering/
├── agents/                           # AI agent personas
│   ├── security-analyst.md          # Security Analyst agent (Story 1.1)
│   └── security-reviewer.md         # Security Reviewer agent (Story 2.1)
│
├── agent-teams/                      # Agent team bundles
│   └── security-team.txt            # Bundled team for web UI
│
├── checklists/                       # Quality assurance checklists (Story 2.2)
│   ├── technical-accuracy-checklist.md        # CVE validation, CVSS/EPSS/KEV accuracy (10 items)
│   ├── completeness-checklist.md              # Required sections presence (12 items)
│   ├── actionability-checklist.md             # Remediation guidance, priority/SLA (8 items)
│   ├── contextualization-checklist.md         # Business, threat, environmental context (10 items)
│   ├── documentation-quality-checklist.md     # Structure, clarity, readability (8 items)
│   ├── attack-mapping-validation-checklist.md # MITRE ATT&CK tactics/techniques (4 items)
│   ├── cognitive-bias-checklist.md            # 5 bias types detection (5 biases)
│   └── source-citation-checklist.md           # Authoritative sources, URL validation (5 items)
│
├── data/                             # Knowledge bases and reference materials
│   ├── bmad-kb.md                   # Vulnerability management KB (Story 4.1)
│   ├── cognitive-bias-patterns.md   # Cognitive bias guide (Story 4.2)
│   └── mitre-attack-mapping-guide.md # ATT&CK mapping guide (Story 4.3)
│
├── docs/                             # Project documentation
│   ├── prd/                         # Product requirements
│   │   └── epic-4-knowledge-base.md # Epic 4 definition
│   ├── architecture/                 # Architecture documentation
│   │   └── source-tree.md           # This file
│   ├── stories/                     # User stories
│   │   ├── 1.1.security-analyst-agent-creation.md
│   │   ├── 1.2.jira-ticket-reading.md
│   │   ├── 1.3.ai-assisted-cve-research.md
│   │   ├── 1.4.structured-enrichment-documentation.md
│   │   ├── 1.5.jira-enrichment-comment.md
│   │   ├── 1.6.jira-custom-field-updates.md
│   │   ├── 1.7.multi-factor-priority-assessment.md
│   │   ├── 2.1.security-reviewer-agent-creation.md
│   │   ├── 2.2.systematic-quality-evaluation.md
│   │   ├── 2.3.gap-identification-categorization.md
│   │   ├── 2.4.cognitive-bias-detection.md
│   │   ├── 2.5.fact-verification.md
│   │   ├── 2.6.constructive-feedback-documentation.md
│   │   ├── 3.1.security-alert-enrichment-workflow.md
│   │   ├── 3.2.security-analysis-review-workflow.md
│   │   ├── 3.3.vulnerability-lifecycle-workflow.md
│   │   ├── 3.4.priority-based-review-triggering.md
│   │   ├── 4.1.vulnerability-management-knowledge-base.md
│   │   ├── 4.2.cognitive-bias-patterns-guide.md
│   │   └── 4.3.mitre-attack-mapping-guide.md
│   └── qa/                          # QA assessments
│       └── 1.1.security-analyst-agent-qa.md
│
├── tasks/                            # Reusable workflow procedures
│   └── (task files - TBD based on agent needs)
│
├── templates/                        # Document templates
│   └── (template files - TBD based on agent needs)
│
├── workflows/                        # Project workflow definitions
│   ├── security-alert-enrichment-workflow.yaml   # Story 3.1 enrichment workflow
│   └── security-analysis-review-workflow.yaml    # Story 3.2 review workflow
│
├── metrics/                          # Workflow performance metrics (Story 3.2)
│   └── (workflow execution times, quality scores)
│
├── artifacts/                        # Review document storage (Story 3.2)
│   └── (enrichment and review reports)
│
├── tests/                            # Test files for expansion pack
│   └── workflows/                    # Workflow integration tests
│
├── config.yaml                       # Expansion pack configuration
└── README.md                         # Expansion pack overview

```

## File Organization Principles

### 1. Knowledge Base Files (`data/`)

**Location:** All knowledge base and reference materials go in `data/`

**Naming Convention:**

- Descriptive kebab-case names
- Examples: `bmad-kb.md`, `cognitive-bias-patterns.md`, `mitre-attack-mapping-guide.md`

**Purpose:**

- Reference materials for agents
- Knowledge bases loaded by Security Analyst and Security Reviewer
- Standalone documents that don't require external dependencies

### 2. Agent Files (`agents/`)

**Location:** AI agent persona definitions go in `agents/`

**Naming Convention:**

- Kebab-case role names
- Examples: `security-analyst.md`, `security-reviewer.md`

**Purpose:**

- Define agent personas, capabilities, and activation instructions
- Reference dependencies (tasks, templates, checklists, data)
- Used in IDE environments (Cursor, VS Code, Claude Code)

### 3. Story Files (`docs/stories/`)

**Location:** User stories go in `docs/stories/`

**Naming Convention:**

- Format: `{epic}.{story}.{short-title}.md`
- Examples: `4.1.vulnerability-management-knowledge-base.md`

**Purpose:**

- Implementation specifications for Dev agent
- Include tasks, acceptance criteria, dev notes, testing guidance
- Track implementation progress and QA results

### 4. Checklist Files (`checklists/`)

**Location:** QA checklists go in `checklists/`

**Naming Convention:**

- Descriptive kebab-case names with `-checklist.md` suffix
- Examples: `accuracy-checklist.md`, `priority-checklist.md`

**Purpose:**

- Quality dimension checklists for Security Reviewer
- Systematic evaluation criteria
- Reusable across multiple review scenarios

## Path References for Story 4.3

When implementing Story 4.3 (MITRE ATT&CK Mapping Guide):

**Full path for knowledge base file:**

```
expansion-packs/bmad-1898-engineering/data/mitre-attack-mapping-guide.md
```

**Related files:**

- Epic definition: `expansion-packs/bmad-1898-engineering/docs/prd/epic-4-knowledge-base.md`
- Story specification: `expansion-packs/bmad-1898-engineering/docs/stories/4.3.mitre-attack-mapping-guide.md`
- Related KB: `expansion-packs/bmad-1898-engineering/data/bmad-kb.md` (Story 4.1)

## Integration Points

**JIRA Configuration** (`config.yaml`):

- Custom fields for CVE enrichment
- Integration with Security Analyst agent workflows

**Core BMAD Framework:**

- Inherits core tasks from `.bmad-core/tasks/`
- Inherits core templates from `.bmad-core/templates/`
- Can override or extend with expansion-specific tasks/templates

## Build Outputs

**Distribution directory:** `dist/expansion-packs/bmad-1898-engineering/`

**Build process:**

- Bundles agents with dependencies into `.txt` files for web UI
- Resolves dependency chains (tasks → templates → checklists → data)
- Creates team bundles in `agent-teams/`

## Version Information

**Current Version:** 0.1.0
**Status:** Development
**Author:** 1898 & Co.

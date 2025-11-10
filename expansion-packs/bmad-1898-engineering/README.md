# BMad 1898 Engineering Expansion Pack
**Industrial Control Systems (ICS) Security Operations & Vulnerability Management**

Transform your AI into a complete security operations team with specialized agents for vulnerability enrichment, security event investigation, and quality assurance in industrial control systems environments.

---

## Overview

The 1898 Engineering Expansion Pack extends BMad-Method with comprehensive tools for security operations teams working with ICS/SCADA environments. Named after the foundational year of industrial engineering, this pack provides structured AI assistance for vulnerability management, security alert investigation, and quality assurance workflows.

### Key Features

- **2 Specialized Security Agents** - Complete security operations team (Security Analyst + Security Reviewer)
- **20+ Core Tasks** - Vulnerability enrichment, event investigation, security review, JIRA integration, research execution
- **15+ Quality Checklists** - Vulnerability enrichment quality, event investigation completeness, disposition reasoning, cognitive bias detection
- **10+ Professional Templates** - Vulnerability enrichment reports, event investigation reports, review assessments, disposition frameworks
- **Comprehensive Knowledge Bases** - ICS/SCADA security, vulnerability analysis, NIST SP 800-61 incident handling, cognitive bias mitigation
- **Integrated MCP Support** - Atlassian (JIRA), Perplexity (research), automated workflows

---

## Epic 7: Event Investigation Capabilities (NEW)

**Complete security alert investigation workflow for ICS/IDS/SIEM platforms**

### What is Event Investigation?

Security event investigation is the systematic analysis of security alerts from monitoring platforms (Claroty ICS, Snort IDS, Splunk SIEM) to determine if detected activity is malicious (True Positive), a false alarm (False Positive), or authorized activity (Benign True Positive).

### Key Components

**5-Stage Investigation Methodology** (Based on NIST SP 800-61):
1. **Alert Triage** (2-3 min) - Extract metadata, identify affected assets
2. **Evidence Collection** (5-8 min) - Gather logs, correlate events, research historical patterns
3. **Technical Analysis** (4-6 min) - Validate protocol behavior, assess attack vectors
4. **Disposition Determination** (2-3 min) - Determine TP/FP/BTP with confidence level
5. **Recommendations** (2-3 min) - Immediate actions, long-term improvements, escalation

**Disposition Framework:**
- **TP (True Positive)**: Malicious activity confirmed → Escalate to incident response
- **FP (False Positive)**: Alert incorrect, no malicious activity → Tuning recommendation
- **BTP (Benign True Positive)**: Real activity, but authorized/expected → Create exception

**7-Dimension Quality Review Framework:**
- Investigation Completeness (25%)
- Technical Accuracy (20%)
- Disposition Reasoning (20%)
- Contextualization (15%)
- Investigation Methodology (10%)
- Documentation Quality (5%)
- Cognitive Bias Mitigation (5%)

### Platform Support

- **Claroty ICS** - Industrial control system monitoring, OT protocol analysis
- **Snort IDS** - Network intrusion detection, signature-based alerts
- **Splunk SIEM** - Security information and event management, correlation analysis

### Commands

**Security Analyst:**
- `*investigate-event {ticket-id}` - Execute complete 5-stage investigation (15-25 min)
- `*enrich {ticket-id}` - Vulnerability enrichment workflow
- `*research {ticket-id}` - Execute research queries using Perplexity MCP

**Security Reviewer:**
- `*review-enrichment {ticket-id} --type=event` - 7-stage quality review for event investigations
- `*review-enrichment {ticket-id}` - Quality review for vulnerability enrichments (auto-detected)

### Documentation

**Quick Start:**
- [Analyst Quick Reference Card](docs/quick-reference/analyst-quick-reference.md) - One-page investigation workflow (5 min read)
- [Reviewer Quick Reference Card](docs/quick-reference/reviewer-quick-reference.md) - One-page review workflow (5 min read)
- [Disposition Decision Tree](docs/quick-reference/disposition-decision-tree.md) - Visual guide for TP/FP/BTP determination

**Deep Dive:**
- [Event Investigation Workflow Deep Dive](docs/workflows/event-investigation-workflow-deep-dive.md) - Comprehensive methodology walkthrough
- [Troubleshooting & FAQ](docs/troubleshooting-faq-best-practices.md) - Common issues and solutions

**Training:**
- [Event Investigation Training](docs/training/event-investigation-training.md) - 8 modules with hands-on exercises (8-10 hours)
- [Event Investigation Review Training](docs/training/event-investigation-review-training.md) - 6 modules for reviewers (6-8 hours)

**Reference:**
- [Cognitive Bias Reference](docs/quick-reference/cognitive-bias-reference.md) - Recognizing and mitigating investigation biases
- [Security Analyst User Guide](docs/user-guide/security-analyst-agent.md) - Complete agent capabilities
- [Security Reviewer User Guide](docs/user-guide/security-reviewer-agent.md) - Complete review workflows
- [JIRA Workflow Standards](docs/architecture/jira-workflow-standards.md) - Event Alert issue type configuration

---

## Included Agents

### Security Operations Team

#### 1. Security Analyst Agent
**Role:** Execute vulnerability enrichments and security event investigations

**Capabilities:**
- **Vulnerability Enrichment** (`*enrich {ticket-id}`)
  - CVE impact analysis (CVSS scoring, exploitability assessment)
  - Asset impact determination (affected systems, business criticality)
  - Technical research using Perplexity MCP
  - Remediation recommendations (patching, workarounds, compensating controls)
  - JIRA ticket updates via Atlassian MCP

- **Event Investigation** (`*investigate-event {ticket-id}`)
  - 5-stage investigation methodology (NIST SP 800-61 based)
  - Hypothesis-driven analysis
  - Multi-source evidence collection
  - Disposition determination (TP/FP/BTP)
  - ICS/SCADA-specific considerations
  - Cognitive bias awareness and mitigation

- **Research Execution** (`*research {ticket-id}`)
  - CVE/vulnerability research queries
  - Exploit availability research
  - Vendor advisory research
  - Automated citation tracking

**Typical Investigation Duration:** 15-25 minutes per event alert

#### 2. Security Reviewer Agent
**Role:** Quality assurance for vulnerability enrichments and event investigations

**Capabilities:**
- **Event Investigation Review** (`*review-enrichment {ticket-id} --type=event`)
  - 7-dimension quality framework
  - Disposition validation (agree/disagree with analyst)
  - Evidence sufficiency assessment
  - Cognitive bias detection
  - Quality score calculation (0-10 scale)
  - Constructive feedback generation (blameless culture)

- **Vulnerability Enrichment Review** (`*review-enrichment {ticket-id}`)
  - CVE analysis accuracy verification
  - Asset impact validation
  - Remediation recommendation assessment
  - Research quality evaluation

- **Auto-Detection:** Automatically detects ticket type (event vs. vulnerability) based on content

**Typical Review Duration:** 10-20 minutes per investigation

---

## Installation

### Via BMad Installer

```bash
npx bmad-method install
# Select "1898 Engineering - ICS Security Operations" from the expansion packs list
```

### Manual Installation

1. Clone or download this expansion pack
2. Copy to your BMad Method installation:
   ```bash
   cp -r bmad-1898-engineering/* ~/bmad-method/expansion-packs/bmad-1898-engineering/
   ```
3. Run the BMad installer to register the pack

---

## Dependencies

### Required MCP Servers

**Atlassian MCP** - JIRA integration for ticket management
```bash
# Install via MCP
# See: https://github.com/modelcontextprotocol/servers/tree/main/atlassian
```

**Perplexity MCP** - Research query execution
```bash
# Install via MCP
# See Perplexity MCP documentation
```

### Optional Tools

**Python 3.8+** - For data analysis scripts (vulnerability metrics, pattern analysis)

```bash
# Check version
python3 --version

# Install dependencies (if using analytics scripts)
pip3 install -r requirements.txt
```

---

## Project Structure

The 1898 Engineering Expansion Pack uses standard BMad structure with security-specific additions:

### Directory Structure

```
bmad-1898-engineering/
├── agents/                         # Security agent definitions
│   ├── security-analyst.md         # Vulnerability + Event investigation
│   └── security-reviewer.md        # Quality assurance and review
├── agent-teams/
│   └── security-ops-team.yaml      # Complete security operations team bundle
├── tasks/                          # Executable procedures
│   ├── enrich-vulnerability.md     # CVE enrichment workflow
│   ├── investigate-event.md        # Event investigation workflow (Epic 7)
│   ├── review-enrichment.md        # Quality review workflow
│   ├── review-event-investigation.md  # Event review workflow (Epic 7)
│   └── research-vulnerability.md   # Research execution task
├── templates/                      # YAML document templates
│   ├── vulnerability-enrichment-report-tmpl.yaml
│   ├── event-investigation-report-tmpl.yaml  # Epic 7
│   ├── review-assessment-tmpl.yaml
│   └── disposition-framework-tmpl.yaml       # Epic 7
├── checklists/                     # Quality assurance checklists
│   ├── vulnerability-enrichment-quality.md
│   ├── event-investigation-completeness.md   # Epic 7
│   ├── disposition-reasoning.md              # Epic 7
│   └── cognitive-bias-detection.md           # Epic 7
├── data/                           # Knowledge bases
│   ├── bmad-kb.md                  # Core methodology
│   ├── ics-scada-security.md       # Industrial control systems knowledge
│   ├── vulnerability-analysis.md   # CVE analysis frameworks
│   ├── nist-sp-800-61.md          # Incident handling guide (Epic 7)
│   └── cognitive-bias-guide.md    # Bias awareness and mitigation (Epic 7)
├── workflows/                      # Workflow definitions
│   ├── vulnerability-management-workflow.yaml
│   └── event-investigation-workflow.yaml     # Epic 7
├── docs/                           # Documentation
│   ├── user-guide/
│   │   ├── security-analyst-agent.md         # Updated for Epic 7
│   │   └── security-reviewer-agent.md        # Updated for Epic 7
│   ├── workflows/
│   │   └── event-investigation-workflow-deep-dive.md  # Epic 7
│   ├── training/
│   │   ├── event-investigation-training.md            # Epic 7
│   │   └── event-investigation-review-training.md     # Epic 7
│   ├── quick-reference/                               # Epic 7
│   │   ├── analyst-quick-reference.md
│   │   ├── reviewer-quick-reference.md
│   │   ├── disposition-decision-tree.md
│   │   └── cognitive-bias-reference.md
│   ├── architecture/
│   │   └── jira-workflow-standards.md        # Updated for Epic 7
│   └── troubleshooting-faq-best-practices.md # Updated for Epic 7
├── tests/                          # Test suites and test data
│   ├── test-data/                  # Sample alerts and investigations
│   └── test-plans/                 # Test execution plans
├── config.yaml                     # Expansion pack configuration
└── README.md                       # This file
```

---

## Usage

### Quick Start

```bash
# Activate agents in your IDE

# Security Analyst (investigations and enrichments)
/bmad-1898:security-analyst

# Security Reviewer (quality assurance)
/bmad-1898:security-reviewer
```

### Core Workflows

**Vulnerability Enrichment Workflow:**

1. Security Analyst receives vulnerability ticket (CVE-based)
2. Analyst executes `*enrich {ticket-id}`
3. Agent performs CVE impact analysis, asset impact assessment, remediation research
4. Agent updates JIRA ticket via Atlassian MCP
5. Security Reviewer executes `*review-enrichment {ticket-id}`
6. Reviewer assesses quality, provides feedback
7. Analyst revises if needed, ticket marked complete

**Event Investigation Workflow (Epic 7):**

1. Security Analyst receives event alert ticket (ICS/IDS/SIEM)
2. Analyst executes `*investigate-event {ticket-id}`
3. Agent performs 5-stage investigation:
   - Alert Triage (metadata, assets, criticality)
   - Evidence Collection (logs, correlation, historical context)
   - Technical Analysis (protocol validation, attack vectors)
   - Disposition Determination (TP/FP/BTP + confidence level)
   - Recommendations (containment, tuning, escalation)
4. Agent updates JIRA with investigation report
5. Security Reviewer executes `*review-enrichment {ticket-id} --type=event`
6. Reviewer performs 7-dimension quality review
7. Reviewer validates disposition (agree/disagree)
8. If disagreement: Return to analyst for re-investigation
9. If agreement: Ticket marked complete, escalated if TP

**Research Workflow:**

1. Analyst or Reviewer identifies knowledge gap
2. Executes `*research {ticket-id}` with specific research questions
3. Agent generates optimized queries for Perplexity MCP
4. Agent executes queries autonomously
5. Agent synthesizes findings with source citations
6. Research report added to ticket

---

## Common Use Cases

### Vulnerability Management
- CVE impact analysis for critical infrastructure
- Asset-specific vulnerability assessment
- Remediation prioritization for ICS/SCADA environments
- Compensating control recommendations

### Security Event Investigation
- ICS alert analysis (Claroty, OT protocols)
- Network intrusion detection (Snort)
- SIEM correlation analysis (Splunk)
- Disposition determination (TP/FP/BTP)
- Incident escalation and containment

### Quality Assurance
- Investigation quality scoring (7-dimension framework)
- Disposition validation (peer review)
- Cognitive bias detection and mitigation
- Blameless feedback and continuous improvement

### Knowledge Management
- Security research automation (Perplexity MCP)
- Vulnerability intelligence gathering
- ICS/SCADA threat landscape research
- Best practices documentation

---

## Key Components

### Templates (4 Core)

- `vulnerability-enrichment-report-tmpl.yaml` - CVE enrichment structure
- `event-investigation-report-tmpl.yaml` - Event investigation structure (Epic 7)
- `review-assessment-tmpl.yaml` - Quality review report
- `disposition-framework-tmpl.yaml` - TP/FP/BTP determination framework (Epic 7)

### Tasks (5 Core)

- `enrich-vulnerability.md` - Complete CVE enrichment workflow
- `investigate-event.md` - 5-stage event investigation workflow (Epic 7)
- `review-enrichment.md` - Vulnerability enrichment quality review
- `review-event-investigation.md` - Event investigation quality review (Epic 7)
- `research-vulnerability.md` - Automated research execution

### Checklists (6 Core)

- `vulnerability-enrichment-quality.md` - CVE enrichment validation
- `event-investigation-completeness.md` - Investigation thoroughness (Epic 7)
- `disposition-reasoning.md` - TP/FP/BTP reasoning validation (Epic 7)
- `cognitive-bias-detection.md` - Bias awareness checklist (Epic 7)
- `technical-accuracy.md` - Technical correctness validation
- `remediation-recommendations.md` - Remediation quality assessment

### Workflows (2 Core)

- `vulnerability-management-workflow.yaml` - End-to-end vulnerability handling
- `event-investigation-workflow.yaml` - End-to-end event investigation (Epic 7)

### Knowledge Bases (5 Core)

- `bmad-kb.md` - Core security operations methodology
- `ics-scada-security.md` - Industrial control systems security knowledge
- `vulnerability-analysis.md` - CVE analysis frameworks (CVSS, exploitability)
- `nist-sp-800-61.md` - Computer Security Incident Handling Guide (Epic 7)
- `cognitive-bias-guide.md` - Investigation bias awareness and mitigation (Epic 7)

---

## Epic Status

### Epic 7: Event Investigation & Quality Review (COMPLETE)

**Objective:** Extend security operations capabilities from vulnerability management to comprehensive security event investigation with systematic quality review processes.

**Deliverables:**
- ✅ Event investigation workflow (5-stage methodology based on NIST SP 800-61)
- ✅ Disposition framework (TP/FP/BTP determination)
- ✅ Quality review framework (7-dimension scoring)
- ✅ Cognitive bias mitigation (automation, anchoring, confirmation, availability)
- ✅ Platform support (Claroty ICS, Snort IDS, Splunk SIEM)
- ✅ Training materials (8 modules for analysts, 6 modules for reviewers)
- ✅ Quick reference cards (4 one-page guides)
- ✅ JIRA workflow integration (Event Alert issue type)
- ✅ Complete documentation (workflow deep dive, troubleshooting, FAQ)

**Status:** Production Ready (All 9 stories complete)

**Version:** 1.7.0 (Epic 7 Complete)

---

## Cognitive Bias Awareness

Epic 7 introduces systematic cognitive bias mitigation throughout the investigation and review processes:

### The Four Critical Biases

1. **Automation Bias** - Over-trusting automated alerts without independent verification
2. **Anchoring Bias** - Fixating on first piece of evidence (e.g., alert severity)
3. **Confirmation Bias** - Seeking only evidence that confirms initial hypothesis
4. **Availability Bias** - Overweighting recent or memorable incidents

### Mitigation Strategies

- **Hypothesis-Driven Investigation:** Generate multiple competing hypotheses, test all equally
- **Pre-Mortem Analysis:** Imagine you're wrong, actively search for contradictory evidence
- **Devil's Advocate:** Intentionally argue the opposite disposition
- **Checklist-Driven Process:** Systematic approach prevents bias-driven shortcuts

See [Cognitive Bias Reference](docs/quick-reference/cognitive-bias-reference.md) for complete guide.

---

## ICS/SCADA-Specific Considerations

Industrial control systems require specialized security analysis:

### Key Differences from IT Security

- **Safety Implications:** Security incidents can cause physical harm or environmental damage
- **Availability Priority:** Uptime critical for industrial processes (can't patch during operations)
- **Legacy Systems:** Decades-old equipment with no security updates available
- **OT Protocols:** Specialized protocols (Modbus, DNP3, OPC) with limited security features
- **Air-Gapped Networks:** Limited internet connectivity, challenging for research/updates

### Investigation Adaptations

- **Asset Criticality:** Always assess potential safety impact
- **Change Management:** Verify all maintenance windows and authorized access
- **Protocol Validation:** Understand expected OT protocol behavior
- **Business Context:** Industrial processes have specific operational patterns
- **Escalation:** Lower threshold for True Positive escalation due to safety concerns

---

## Training & Certification

### Analyst Training Path

1. **Module 1:** Introduction to Event Investigation (1 hour)
2. **Module 2:** Investigation Methodology (2 hours)
3. **Module 3:** Disposition Framework (1.5 hours)
4. **Module 4:** Platform-Specific Investigations (2 hours)
5. **Module 5:** Evidence Collection Techniques (1 hour)
6. **Module 6:** Cognitive Bias in Investigations (1 hour)
7. **Module 7:** ICS/SCADA-Specific Considerations (1.5 hours)
8. **Module 8:** Hands-On Scenarios (3 hours)
9. **Final Assessment:** 50 points, 80% pass rate

**Total Duration:** 8-10 hours

See [Event Investigation Training](docs/training/event-investigation-training.md)

### Reviewer Training Path

1. **Module 1:** Introduction to Event Investigation Review (1 hour)
2. **Module 2:** 7-Dimension Quality Framework (1.5 hours)
3. **Module 3:** Disposition Validation (1.5 hours)
4. **Module 4:** Evidence Sufficiency Assessment (1 hour)
5. **Module 5:** Cognitive Bias Detection (1 hour)
6. **Module 6:** Review Report Writing (1 hour)
7. **Final Assessment:** 50 points, 80% pass rate

**Total Duration:** 6-8 hours

See [Event Investigation Review Training](docs/training/event-investigation-review-training.md)

---

## Performance Metrics

### Investigation Quality Metrics

- **Quality Score:** 0-10 scale (7-dimension weighted average)
- **Disposition Accuracy:** % of reviewer agreement with analyst disposition
- **Investigation Duration:** Average time per alert (target: 15-25 minutes)
- **Escalation Rate:** % of True Positives escalated to incident response
- **False Positive Rate:** % of alerts marked FP (indicates tuning opportunities)

### Review Metrics

- **Review Duration:** Average time per review (target: 10-20 minutes)
- **Disagreement Rate:** % of disposition disagreements (indicates training needs)
- **Quality Trend:** Average quality score over time (continuous improvement)
- **Cognitive Bias Detection Rate:** % of investigations with bias indicators

See [JIRA Workflow Standards](docs/architecture/jira-workflow-standards.md) for complete metrics schema.

---

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Follow BMad Method conventions
4. Submit a PR with clear description

---

## License

This expansion pack follows the same license as BMad Method core.

---

## Credits

Created for the BMad Method community by the 1898 Engineering team.

Special thanks to Brian (BMad) for creating the BMad Method framework.

---

**Version:** 1.7.0 (Epic 7 Complete - Event Investigation & Quality Review)
**Compatible with:** BMad Method v4.0+
**Last Updated:** November 2025

---

## Need Help?

- **Quick Start:** See [Analyst Quick Reference](docs/quick-reference/analyst-quick-reference.md)
- **Troubleshooting:** See [Troubleshooting & FAQ](docs/troubleshooting-faq-best-practices.md)
- **Training:** See [Event Investigation Training](docs/training/event-investigation-training.md)
- **Deep Dive:** See [Event Investigation Workflow Deep Dive](docs/workflows/event-investigation-workflow-deep-dive.md)

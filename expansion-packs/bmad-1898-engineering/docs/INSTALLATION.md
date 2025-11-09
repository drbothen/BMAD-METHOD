# Installation & Setup Guide

## Overview

This guide provides complete installation and configuration instructions for the **bmad-1898-engineering** expansion pack. This expansion pack enables security teams to automate vulnerability management workflows using AI-powered agents integrated with JIRA Cloud.

**What You'll Accomplish:**
- Install the bmad-1898-engineering expansion pack
- Configure JIRA Cloud integration with custom fields
- Set up required MCP servers for JIRA and vulnerability research
- Configure priority-based review workflows
- Complete your first successful vulnerability enrichment

**Time to Complete:** 30-45 minutes for quickstart setup

**Prerequisites Reading Time:** 5 minutes

---

## 1. Prerequisites

Before beginning installation, ensure you have the following components and permissions:

### 1.1 JIRA Cloud Requirements

**Required:**
- **JIRA Cloud Subscription:** Standard, Premium, or Enterprise plan
- **Permissions:** Admin or Project Admin role
- **Capabilities Needed:**
  - Create custom fields
  - Generate API tokens
  - Modify project configurations
  - Create and edit issues

**How to Verify:**
- Log in to your JIRA Cloud instance (https://your-domain.atlassian.net)
- Navigate to Project Settings to confirm admin access
- Check your plan level at admin.atlassian.com → Billing

### 1.2 MCP (Model Context Protocol) Requirements

**Required:**

**Atlassian MCP:**
- **Must be installed and configured separately** (not included by default)
- Installation: Follow Atlassian MCP setup instructions for your IDE
- Required tools:
  - `mcp__atlassian__getJiraIssue` - Retrieve JIRA issue details
  - `mcp__atlassian__updateJiraIssue` - Update JIRA custom fields
  - `mcp__atlassian__addCommentToJiraIssue` - Post enrichment comments
  - `mcp__atlassian__searchJiraIssues` - Query JIRA for issues
- Authentication: API token or OAuth 2.0
- Documentation: See Atlassian MCP setup guide for your specific IDE

**Perplexity MCP:**
- **Must be installed and configured separately** (not included by default)
- Installation: Follow Perplexity MCP setup instructions for your IDE
- Configuration varies by IDE (Claude Code, Cursor, VS Code, etc.)
- Required tools:
  - `mcp__perplexity__search` - Quick vulnerability research
  - `mcp__perplexity__reason` - Complex analysis and reasoning
  - `mcp__perplexity__deep_research` - Comprehensive vulnerability investigations
- Used for CVE research and threat intelligence gathering
- **Important:** Without Perplexity MCP, agents will fall back to manual research workflows (slower but functional)

### 1.3 Development Environment

**Required:**
- BMAD-METHOD framework installed in your project
- IDE/Editor with AI assistant (same as BMAD core supports):
  - Cursor IDE (recommended)
  - VS Code with Claude Code extension
  - VS Code with Cline extension
  - Claude Code CLI
  - Any IDE with Claude/AI assistant integration
- Active Claude API access (or equivalent AI model access)

**Note:** This expansion pack works with the same development environments as BMAD core. If you can use BMAD core agents, you can use this expansion pack.

### 1.4 Network Access Requirements

Your environment must have network connectivity to:
- **JIRA Cloud:** `*.atlassian.net` (HTTPS)
- **Perplexity API:** via MCP (HTTPS)
- **Vulnerability Intelligence Sources:**
  - NIST NVD: `nvd.nist.gov`
  - CISA KEV Catalog: `www.cisa.gov`
  - FIRST EPSS: `www.first.org`

**Firewall Configuration:**
- Outbound HTTPS (port 443) to all listed domains
- No inbound connections required

---

## 2. Installation Steps

### 2.1 Install bmad-1898-engineering Expansion Pack

**Using npx (Recommended):**

```bash
# From your project root directory
npx bmad-method install
```

When prompted:
1. Select "Install expansion pack"
2. Choose "bmad-1898-engineering" from the list
3. Confirm installation location (e.g., project root, or a specific subdirectory)

The expansion pack will be installed as `.bmad-1898-engineering/` (hidden directory) in your chosen location.

**After Installation:**
Once installed, the expansion pack agents will be available via slash commands:
- Slash command prefix: `bmad-1898` (defined in `config.yaml` `slashPrefix` setting)
- Access agents: `/bmad-1898:agents:security-analyst` or `/bmad-1898:agents:security-reviewer`
- The expansion pack files exist in `.bmad-1898-engineering/` directory

**Important:** The directory name (`.bmad-1898-engineering`) and slash command prefix (`bmad-1898`) are different!

**Manual Installation:**

If installing manually (without npx), you'll need to:
1. Create the hidden directory `.bmad-1898-engineering` in your project root
2. Copy all expansion pack files into that directory
3. The directory name uses the full expansion pack name with a leading dot

```bash
# Create hidden directory
mkdir .bmad-1898-engineering

# Clone or download the expansion pack
git clone <repository-url> .bmad-1898-engineering

# Or copy from downloaded archive
unzip bmad-1898-engineering.zip
cp -r bmad-1898-engineering/* .bmad-1898-engineering/
```

**Note:** The directory is named `.bmad-1898-engineering` (expansion pack name), but slash commands use the prefix `bmad-1898` (from config.yaml `slashPrefix`).

### 2.2 Verify Installation

After installation, the expansion pack will be installed as a hidden directory in your selected location (default: project root).

Check that the following directory structure exists:

```
.bmad-1898-engineering/          # Hidden directory (note the leading dot)
├── agents/
│   ├── security-analyst.md
│   └── security-reviewer.md
├── workflows/
│   ├── security-alert-enrichment.md
│   ├── security-analysis-review.md
│   ├── vulnerability-lifecycle.md
│   ├── priority-review-triggering.md
│   └── notification-routing.md
├── tasks/
│   ├── enrich-ticket.md
│   ├── research-cve.md
│   ├── calculate-priority.md
│   ├── determine-review.md
│   ├── assign-reviewer.md
│   ├── perform-security-review.md
│   ├── approve-enrichment.md
│   ├── request-changes.md
│   └── update-lifecycle.md
├── templates/
│   ├── enrichment-output-tmpl.md
│   └── review-assessment-tmpl.md
├── config.yaml (to be configured)
└── README.md
```

**Verification Commands:**

```bash
# List expansion pack contents (note: -a flag shows hidden directories)
ls -la .bmad-1898-engineering/

# Should show: agents/, workflows/, tasks/, templates/, config.yaml, README.md

# Verify specific directories exist
ls .bmad-1898-engineering/agents/
# Should show: security-analyst.md, security-reviewer.md

ls .bmad-1898-engineering/workflows/
# Should show: 5 workflow files

ls .bmad-1898-engineering/tasks/
# Should show: 9 task files

ls .bmad-1898-engineering/templates/
# Should show: 2 template files
```

**Note:**
- Directory name: `.bmad-1898-engineering` (full expansion pack name with leading dot)
- Slash command prefix: `bmad-1898` (from `slashPrefix` in config.yaml)
- Hidden on Unix-based systems (macOS, Linux) because it starts with `.`

---

## 3. JIRA Cloud Setup

### 3.1 Obtain JIRA Cloud ID

Your JIRA Cloud ID is required for API authentication and is different from your JIRA URL.

**Steps:**
1. Navigate to https://admin.atlassian.com
2. Select your JIRA site from the list
3. Go to "Settings" → "Site details"
4. Copy the **Cloud ID** (UUID format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

**Important:** The Cloud ID is NOT your JIRA URL or subdomain. It's a unique identifier in UUID format.

### 3.2 Identify Project Key

The project key is the prefix used in your JIRA issue IDs (e.g., "SEC" in "SEC-123").

**Steps:**
1. Navigate to your JIRA project
2. Look at any issue URL: `https://your-domain.atlassian.net/browse/SEC-123`
3. The project key is the letters before the dash: **SEC**

Alternatively:
1. Go to Project Settings
2. The project key is displayed at the top

### 3.3 Generate API Token (for Atlassian MCP)

**Steps:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it: "bmad-1898-engineering-mcp"
4. Copy the token immediately (you won't see it again)
5. Store securely (required for Atlassian MCP configuration)

---

## 4. JIRA Custom Fields Setup

The expansion pack requires 8 custom fields in JIRA to store vulnerability enrichment data.

### 4.1 Required Custom Fields

| Field Name | Field Type | Options/Validation | Purpose |
|------------|-----------|-------------------|---------|
| **CVE ID** | Text (single line) | Pattern: `CVE-\d{4}-\d{4,}` | Primary vulnerability identifier |
| **Affected Systems** | Text (multi-line) | - | List of impacted systems/applications |
| **Asset Criticality Rating** | Select (single) | Critical, High, Medium, Low | Business criticality of affected asset |
| **System Exposure** | Select (single) | Internet, Internal, Isolated | Network exposure classification |
| **CVSS Score** | Number | Min: 0.0, Max: 10.0, Decimals: 1 | CVSS v3.1 base score |
| **EPSS Score** | Number | Min: 0.0, Max: 100.0, Decimals: 2 | EPSS exploitation probability (%) |
| **KEV Status** | Select (single) | Yes, No | CISA Known Exploited Vulnerability |
| **Exploit Status** | Select (single) | Active, PoC, None, Unknown | Observed exploitation status |

### 4.2 Step-by-Step Field Creation

For **each field** listed above, follow these steps:

**Step 1: Navigate to Custom Fields**
1. Go to https://admin.atlassian.com
2. Select your JIRA site
3. Navigate to "Products" → "JIRA" → "Custom fields"
4. Click "Create custom field"

**Step 2: Select Field Type**
- For **Text fields** (CVE ID, Affected Systems): Choose "Text Field (single line)" or "Text Field (multi-line)"
- For **Select fields** (Asset Criticality, System Exposure, KEV Status, Exploit Status): Choose "Select List (single choice)"
- For **Number fields** (CVSS Score, EPSS Score): Choose "Number Field"

**Step 3: Configure Field**
- **Name:** Use exact names from table above
- **Description:** Add purpose from table
- **Options** (for Select fields only): Enter options exactly as shown:
  - Asset Criticality Rating: `Critical`, `High`, `Medium`, `Low`
  - System Exposure: `Internet`, `Internal`, `Isolated`
  - KEV Status: `Yes`, `No`
  - Exploit Status: `Active`, `PoC`, `None`, `Unknown`
- **Number configuration** (for Number fields):
  - CVSS Score: Min=0.0, Max=10.0, Decimal places=1
  - EPSS Score: Min=0.0, Max=100.0, Decimal places=2

**Step 4: Associate with Projects**
- Select your target project(s) where vulnerabilities will be tracked
- Click "Create"

**Step 5: Note Field ID**
- After creation, click on the field name
- Click "Edit"
- Look at the URL: `https://admin.atlassian.com/.../customfield_10042/edit`
- Note the field ID: `customfield_10042`
- **CRITICAL:** You'll need this exact ID for configuration

### 4.3 Quick Field ID Discovery

**Method 1: Admin UI** (easiest)
1. Go to admin.atlassian.com → Custom fields
2. Click field → Edit → Copy ID from URL

**Method 2: API Inspection** (most accurate)
1. Create a test JIRA issue
2. Add some value to each custom field
3. Use Atlassian MCP to fetch the issue:
   ```
   mcp__atlassian__getJiraIssue(issueKey: "TEST-001")
   ```
4. Inspect JSON response for field IDs in format `customfield_XXXXX`

### 4.4 Field ID Mapping Template

Create this table for your configuration (fill in YOUR actual field IDs):

| Field Name | Config Key | Your Field ID |
|------------|-----------|---------------|
| CVE ID | `cve_id` | `customfield_____` |
| Affected Systems | `affected_systems` | `customfield_____` |
| Asset Criticality Rating | `asset_criticality_rating` | `customfield_____` |
| System Exposure | `system_exposure` | `customfield_____` |
| CVSS Score | `cvss_score` | `customfield_____` |
| EPSS Score | `epss_score` | `customfield_____` |
| KEV Status | `kev_status` | `customfield_____` |
| Exploit Status | `exploit_status` | `customfield_____` |

**Keep this table handy for the next configuration step.**

---

## 5. MCP Setup

### 5.1 Atlassian MCP Configuration

The Atlassian MCP must be installed and configured separately (not included in this expansion pack).

**Installation:**
1. Follow Atlassian MCP installation instructions for your environment
2. Configure authentication using the API token from Section 3.3
3. Set JIRA Cloud URL: `https://your-domain.atlassian.net`

**Verification:**
Test the connection in your IDE:
```
Activate Security Analyst agent: /bmad-1898:agents:security-analyst
Run: mcp__atlassian__getJiraIssue with a known issue key
Expected: Issue details returned successfully
```

**Required Tools (verify availability):**
- `mcp__atlassian__getJiraIssue`
- `mcp__atlassian__updateJiraIssue`
- `mcp__atlassian__addCommentToJiraIssue`
- `mcp__atlassian__searchJiraIssues`

### 5.2 Perplexity MCP Verification

Perplexity MCP must be installed and configured separately for your IDE.

**Installation:**
1. Follow Perplexity MCP installation instructions for your specific IDE
2. Configure MCP server connection in your IDE settings
3. Restart your IDE to load the MCP configuration

**Verification:**
```
In your IDE, check for available tools:
- mcp__perplexity__search
- mcp__perplexity__reason
- mcp__perplexity__deep_research
```

**If Perplexity tools are unavailable:**
- Verify Perplexity MCP is installed correctly
- Check your IDE's MCP configuration settings
- Ensure MCP server is running (if applicable to your setup)
- Check network connectivity to Perplexity API
- **Note:** Agents will fall back to manual research workflows if Perplexity is unavailable (slower but functional)

---

## 6. Configuration Guide (config.yaml)

### 6.1 Locate Configuration File

Open: `.bmad-1898-engineering/config.yaml`

**Note:** This is a hidden directory (starts with `.`). You may need to show hidden files in your file explorer, or use your IDE's file navigator.

### 6.2 Complete Configuration Template

Replace all placeholder values with your actual configuration:

```yaml
# .bmad-1898-engineering/config.yaml

name: bmad-1898-engineering
version: 0.1.0
slashPrefix: bmad-1898
description: Security vulnerability management expansion pack
author: 1898 & Co.

# ============================================================================
# JIRA INTEGRATION CONFIGURATION
# ============================================================================
jira:
  # REQUIRED: Your JIRA Cloud instance ID (UUID format)
  # Find at: admin.atlassian.com → Site details → Cloud ID
  cloud_id: "YOUR_CLOUD_ID_HERE"  # Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

  # REQUIRED: Project key where vulnerability tickets are tracked
  # Example: "SEC" for issues like SEC-123
  project_key: "YOUR_PROJECT_KEY"  # Example: "SEC", "AOD", "VULN"

  # REQUIRED: Custom field IDs (replace with YOUR actual field IDs from Section 4.4)
  custom_fields:
    cve_id:
      field_id: "customfield_XXXXX"  # Replace XXXXX with your field ID
      type: "text"
      label: "CVE ID"
      validation: "CVE-\\d{4}-\\d{4,}"

    affected_systems:
      field_id: "customfield_XXXXX"  # Replace XXXXX
      type: "text"
      label: "Affected Systems"

    asset_criticality_rating:
      field_id: "customfield_XXXXX"  # Replace XXXXX
      type: "select"
      label: "Asset Criticality Rating"
      options: ["Critical", "High", "Medium", "Low"]

    system_exposure:
      field_id: "customfield_XXXXX"  # Replace XXXXX
      type: "select"
      label: "System Exposure"
      options: ["Internet", "Internal", "Isolated"]

    cvss_score:
      field_id: "customfield_XXXXX"  # Replace XXXXX
      type: "number"
      label: "CVSS Score"
      min: 0.0
      max: 10.0
      decimals: 1

    epss_score:
      field_id: "customfield_XXXXX"  # Replace XXXXX
      type: "number"
      label: "EPSS Score"
      min: 0.0
      max: 100.0
      decimals: 2

    kev_status:
      field_id: "customfield_XXXXX"  # Replace XXXXX
      type: "select"
      label: "KEV Status"
      options: ["Yes", "No"]

    exploit_status:
      field_id: "customfield_XXXXX"  # Replace XXXXX
      type: "select"
      label: "Exploit Status"
      options: ["Active", "PoC", "None", "Unknown"]

# ============================================================================
# PRIORITY MAPPING CONFIGURATION
# ============================================================================
# Maps calculated P1-P5 priorities to your JIRA priority field values
# IMPORTANT: Use your actual JIRA priority names (case-sensitive)
priority_mapping:
  P1: "Critical"    # Highest priority - critical vulnerabilities
  P2: "High"        # High priority - significant vulnerabilities
  P3: "Medium"      # Medium priority - moderate vulnerabilities
  P4: "Low"         # Low priority - minor vulnerabilities
  P5: "Trivial"     # Lowest priority - minimal vulnerabilities

# ============================================================================
# REVIEW TRIGGERS CONFIGURATION
# ============================================================================
# Defines when security reviews are required based on priority
review_triggers:
  P1:
    review_required: true      # Always require review for P1
    sampling_rate: 100         # Review 100% of P1 enrichments
    blocking: true             # Block ticket updates until review approved
    assignment: "senior-reviewer"  # Assign to senior reviewers only

  P2:
    review_required: true      # Require review for P2
    sampling_rate: 50          # Review 50% of P2 enrichments (random sampling)
    blocking: true             # Block ticket updates until approved
    assignment: "any"          # Any reviewer can handle P2

  P3:
    review_required: true      # Require review for P3
    sampling_rate: 20          # Review 20% of P3 enrichments
    blocking: false            # Non-blocking - update ticket immediately
    assignment: "any"

  P4:
    review_required: false     # No review required for P4
    sampling_rate: 5           # Audit 5% for quality assurance
    blocking: false
    assignment: "any"

  P5:
    review_required: false     # No review required for P5
    sampling_rate: 0           # No sampling for P5
    blocking: false
    assignment: "any"

# ============================================================================
# REVIEWER ASSIGNMENT CONFIGURATION
# ============================================================================
reviewer_assignment:
  method: "priority-weighted-round-robin"  # Load balancing method

  # Define your security review team
  reviewers:
    - name: "Alex"                   # Reviewer name (used in assignments)
      role: "senior-reviewer"        # Role for assignment rules
      specializations:               # Optional: expertise areas
        - "web-vulnerabilities"
        - "infrastructure"
      max_concurrent: 5              # Max simultaneous reviews
      priorities: ["P1", "P2", "P3", "P4", "P5"]  # Priorities this reviewer handles

    - name: "Jordan"
      role: "security-reviewer"
      specializations:
        - "application-security"
        - "cloud-security"
      max_concurrent: 8
      priorities: ["P2", "P3", "P4", "P5"]

    - name: "Morgan"
      role: "security-reviewer"
      specializations:
        - "network-security"
        - "endpoint-security"
      max_concurrent: 8
      priorities: ["P2", "P3", "P4", "P5"]

  # Reviewer pools for specialized reviews
  pools:
    senior-reviewer: ["Alex"]
    any: ["Alex", "Jordan", "Morgan"]

# ============================================================================
# NOTIFICATION CONFIGURATION
# ============================================================================
notification:
  method: "jira-assignment"  # Primary notification method (JIRA assignment)

  additional:                # Optional: additional notification channels
    - "email"                # Send email notifications (requires email config)
    # - "slack"              # Send Slack notifications (requires Slack config)

  # Optional: Email configuration (if additional: ["email"] enabled)
  # email:
  #   smtp_server: "smtp.example.com"
  #   smtp_port: 587
  #   from_address: "security-alerts@example.com"
  #   reviewer_emails:
  #     Alex: "alex@example.com"
  #     Jordan: "jordan@example.com"
  #     Morgan: "morgan@example.com"

  # Optional: Slack configuration (if additional: ["slack"] enabled)
  # slack:
  #   webhook_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
  #   channel: "#security-reviews"
```

### 6.3 Configuration Validation Checklist

After completing configuration, verify each section:

**JIRA Integration:**
- [ ] `cloud_id` is UUID format (not URL)
- [ ] `project_key` matches your JIRA project
- [ ] All 8 `custom_fields.*.field_id` values start with `customfield_`
- [ ] Field IDs are from YOUR JIRA instance (not examples)

**Priority Mapping:**
- [ ] Priority names match YOUR JIRA priority field values (case-sensitive)
- [ ] All 5 priorities (P1-P5) are mapped

**Review Triggers:**
- [ ] All 5 priorities (P1-P5) have trigger rules defined
- [ ] `sampling_rate` values are 0-100 (percentage)
- [ ] `blocking` values are boolean (true/false)

**Reviewer Assignment:**
- [ ] At least one reviewer is defined
- [ ] All reviewers have `name`, `role`, `max_concurrent`, `priorities`
- [ ] Senior-reviewer pool includes at least one person
- [ ] Reviewer names are consistent across sections

**Notification:**
- [ ] Primary `method` is set to "jira-assignment"
- [ ] If email/Slack enabled, configuration sections are complete

**YAML Syntax:**
- [ ] File validates as valid YAML (use https://www.yamllint.com or VS Code YAML extension)
- [ ] Indentation uses spaces (not tabs)
- [ ] Strings with special characters are quoted

---

## 7. Installation Verification

After completing installation and configuration, verify everything is set up correctly.

### 7.1 File Structure Verification

Verify expansion pack files are in place:

```bash
# Check directory exists (note: -a flag to show hidden directories)
ls -la | grep .bmad-1898-engineering

# Verify required directories and files
ls .bmad-1898-engineering/agents/
# Should show: security-analyst.md, security-reviewer.md

ls .bmad-1898-engineering/workflows/
# Should show: 5 workflow files

ls .bmad-1898-engineering/tasks/
# Should show: 9 task files

ls .bmad-1898-engineering/templates/
# Should show: 2 template files

ls .bmad-1898-engineering/config.yaml
# Should show: config.yaml
```

**Checklist:**
- [ ] `.bmad-1898-engineering/` directory exists
- [ ] `agents/` contains security-analyst.md and security-reviewer.md
- [ ] `workflows/` contains 5 workflow files
- [ ] `tasks/` contains 9 task files
- [ ] `templates/` contains 2 template files
- [ ] `config.yaml` exists and is valid YAML

### 7.2 JIRA Integration Verification

Verify JIRA connection and custom fields:

**Step 1: Test JIRA Connection**
```
1. Activate Security Analyst agent: /bmad-1898:agents:security-analyst
2. Test Atlassian MCP connection:
   mcp__atlassian__getJiraIssue(issueKey: "{existing-issue-key}")
3. Expected: Issue details returned successfully
```

**Step 2: Verify Custom Fields**
Create a test JIRA issue and verify all 8 custom fields are visible:
- [ ] CVE ID field appears
- [ ] Affected Systems field appears
- [ ] Asset Criticality Rating dropdown has 4 options (Critical, High, Medium, Low)
- [ ] System Exposure dropdown has 3 options (Internet, Internal, Isolated)
- [ ] CVSS Score field accepts decimal numbers (0.0-10.0)
- [ ] EPSS Score field accepts decimal numbers (0.0-100.0)
- [ ] KEV Status dropdown has 2 options (Yes, No)
- [ ] Exploit Status dropdown has 4 options (Active, PoC, None, Unknown)

**Step 3: Verify Field ID Mapping**
```
1. Fetch test issue using Atlassian MCP
2. Inspect JSON response
3. Confirm all field IDs in config.yaml match actual field IDs in response
4. Example: If config has "customfield_10042", JSON should contain "customfield_10042"
```

**Checklist:**
- [ ] JIRA Cloud ID configured correctly
- [ ] Project key matches target project
- [ ] All 8 custom fields created in JIRA
- [ ] All 8 field IDs mapped in config.yaml (verified via API)
- [ ] Atlassian MCP can connect and fetch issues

### 7.3 Agent Activation Verification

Verify agents load and display commands:

**Security Analyst Agent:**
```
1. Activate: /bmad-1898:agents:security-analyst
2. Agent should greet and auto-display *help command list
3. Verify commands shown:
   - *enrich-ticket
   - *batch-enrich
   - *research-cve
   - *help
   - *exit
```

**Security Reviewer Agent:**
```
1. Activate: /bmad-1898:agents:security-reviewer
2. Agent should greet and auto-display *help command list
3. Verify commands shown:
   - *review-enrichment
   - *batch-review
   - *approve
   - *request-changes
   - *help
   - *exit
```

**Checklist:**
- [ ] `/bmad-1898:agents:security-analyst` activates successfully
- [ ] Security Analyst displays *help with all commands
- [ ] `/bmad-1898:agents:security-reviewer` activates successfully
- [ ] Security Reviewer displays *help with all commands

### 7.4 End-to-End Smoke Test

Complete a full enrichment workflow to verify everything works:

**Step 1: Create Test Ticket**
```
1. In JIRA, create new issue:
   - Summary: "TEST-001: CVE-2024-1234 Test Vulnerability"
   - Description: "Test vulnerability for expansion pack verification"
   - Add CVE-2024-1234 to CVE ID custom field
2. Note the issue key (e.g., SEC-100)
```

**Step 2: Run Enrichment**
```
1. Activate Security Analyst: /bmad-1898:agents:security-analyst
2. Run enrichment: *enrich-ticket SEC-100
3. Wait for completion (2-5 minutes)
```

**Step 3: Verify Enrichment Outputs**
```
Expected outputs:
- [ ] Enrichment completes without errors
- [ ] JIRA comment posted with enrichment summary
- [ ] Custom fields updated:
  - [ ] CVSS Score populated
  - [ ] EPSS Score populated
  - [ ] KEV Status set (Yes/No)
  - [ ] Exploit Status set
  - [ ] Priority calculated and set
- [ ] Local enrichment file created:
  - [ ] Path: enrichments/SEC-100-enrichment.md
  - [ ] File contains CVE details, CVSS, EPSS, KEV, exploit data
```

**Step 4: Verify Review Trigger (if P1/P2)**
```
If calculated priority is P1 or P2:
- [ ] Review assignment created
- [ ] Reviewer notified (JIRA assignment)
- [ ] Ticket status reflects pending review
```

**Success Criteria:**
- All checkboxes above are complete
- No errors during enrichment
- JIRA ticket fully updated with enrichment data
- Local enrichment file created and complete

---

## 8. 30-Minute Quickstart Guide

**Goal:** Complete your first successful vulnerability enrichment in 30 minutes.

This quickstart provides a streamlined path through installation, setup, and first enrichment. For detailed explanations, refer to sections above.

### Quickstart Prerequisites

Before starting the timer:
- [ ] JIRA Cloud account with admin access
- [ ] AI-enabled IDE installed and configured (Cursor, VS Code + extension, etc.)
- [ ] BMAD-METHOD framework installed in your project
- [ ] **Atlassian MCP installed and configured** (required - not included by default)
- [ ] **Perplexity MCP installed and configured** (recommended - not included by default)

### Phase 1: Installation (Target: 5 minutes)

**Step 1: Install Expansion Pack**
```bash
npx bmad-method install
# Select: bmad-1898-engineering
```
⏱️ **Checkpoint:** Files installed in `.bmad-1898-engineering/` (hidden directory)

### Phase 2: JIRA Custom Fields (Target: 10 minutes)

**Step 2: Create Custom Fields**
1. Go to https://admin.atlassian.com → Your JIRA site → Custom fields
2. Create these 8 fields (click "Create custom field" for each):

| Field Name | Type | Options |
|------------|------|---------|
| CVE ID | Text (single line) | - |
| Affected Systems | Text (multi-line) | - |
| Asset Criticality Rating | Select (single) | Critical, High, Medium, Low |
| System Exposure | Select (single) | Internet, Internal, Isolated |
| CVSS Score | Number | Min: 0.0, Max: 10.0, Decimals: 1 |
| EPSS Score | Number | Min: 0.0, Max: 100.0, Decimals: 2 |
| KEV Status | Select (single) | Yes, No |
| Exploit Status | Select (single) | Active, PoC, None, Unknown |

**Step 3: Note Field IDs**
For each field: Click field → Edit → Copy ID from URL (`customfield_XXXXX`)

⏱️ **Checkpoint:** All 8 fields created, IDs noted

### Phase 3: Configuration (Target: 10 minutes)

**Step 4: Get JIRA Cloud ID**
1. Go to https://admin.atlassian.com → Site details
2. Copy Cloud ID (UUID format)

**Step 5: Configure config.yaml**
1. Open: `.bmad-1898-engineering/config.yaml`
2. Set these values:
   ```yaml
   jira:
     cloud_id: "{your-cloud-id-from-step-4}"
     project_key: "{your-project-key}"  # e.g., "SEC"
     custom_fields:
       cve_id:
         field_id: "customfield_XXXXX"  # Your ID from Step 3
       # ... repeat for all 8 fields

   reviewer_assignment:
     reviewers:
       - name: "{your-name}"
         role: "senior-reviewer"
         max_concurrent: 5
         priorities: ["P1", "P2", "P3", "P4", "P5"]
   ```
3. Save file

⏱️ **Checkpoint:** config.yaml complete, YAML validates

### Phase 4: First Enrichment (Target: 5 minutes)

**Step 6: Create Test Ticket**
1. In JIRA, create issue:
   - Summary: "CVE-2024-1234 Test Vulnerability"
   - Set CVE ID field: "CVE-2024-1234"
2. Note issue key (e.g., SEC-100)

**Step 7: Run Enrichment**
```
1. In your IDE, activate agent: /bmad-1898:agents:security-analyst
2. Run command: *enrich-ticket SEC-100
3. Wait for completion (2-5 minutes)
```

**Step 8: Verify Success**
Check JIRA ticket:
- [ ] Comment added with enrichment summary
- [ ] CVSS Score populated
- [ ] EPSS Score populated
- [ ] KEV Status set
- [ ] Priority calculated

Check local file:
- [ ] `enrichments/SEC-100-enrichment.md` created

⏱️ **Checkpoint:** ✅ Enrichment successful!

### Quickstart Success Criteria

- [ ] Total time < 45 minutes (30 min target + 50% buffer)
- [ ] Enrichment completed without errors
- [ ] JIRA ticket updated with all fields
- [ ] Local enrichment file created
- [ ] Ready to enrich real vulnerabilities

**Next Steps:**
- Review Section 6 for advanced configuration options
- Read the Security Analyst Agent Usage Guide for detailed usage instructions
- Start enriching real vulnerability tickets

---

## 9. Troubleshooting

Common installation and setup issues with solutions.

### Issue 1: JIRA Cloud ID Not Found

**Symptoms:**
- Error: "Invalid cloud_id" when agents try to connect to JIRA
- Authentication failures with Atlassian MCP

**Cause:**
JIRA Cloud ID is NOT the same as your JIRA URL or subdomain.

**Solution:**
1. Go to https://admin.atlassian.com
2. Select your JIRA site
3. Navigate to "Settings" → "Site details"
4. Copy the **Cloud ID** - it's in UUID format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
5. Update config.yaml with this exact value

**Verification:**
Cloud ID should be a UUID, NOT a URL or domain name.
- ✅ Correct: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
- ❌ Wrong: `your-company.atlassian.net`
- ❌ Wrong: `https://jira.company.com`

---

### Issue 2: Custom Field IDs Incorrect

**Symptoms:**
- Error: "Field does not exist" when updating JIRA
- Fields not updating after enrichment
- Error message references field ID like `customfield_10042`

**Cause:**
Field IDs in config.yaml don't match your actual JIRA custom field IDs.

**Solution (Method 1 - Admin UI):**
1. Go to https://admin.atlassian.com
2. Navigate to Products → JIRA → Custom fields
3. Click on the custom field
4. Click "Edit" button
5. Look at URL: `https://admin.atlassian.com/.../customfield_10042/edit`
6. The field ID is `customfield_10042`
7. Update config.yaml with this exact ID

**Solution (Method 2 - API Inspection - Most Accurate):**
1. Create a test JIRA issue
2. Manually set a value in each custom field
3. Use Atlassian MCP to fetch the issue:
   ```
   mcp__atlassian__getJiraIssue(issueKey: "SEC-100")
   ```
4. Inspect the JSON response
5. Find your custom field values in the JSON
6. The keys will be the actual field IDs (e.g., `"customfield_10042": "CVE-2024-1234"`)
7. Update config.yaml with these exact IDs

**Verification:**
- Field IDs must start with `customfield_`
- Field IDs are unique to YOUR JIRA instance (not from examples)
- All 8 custom fields have valid field IDs in config.yaml

---

### Issue 3: Atlassian MCP Not Configured

**Symptoms:**
- Error: Tool `mcp__atlassian__getJiraIssue` not found
- Agents can't connect to JIRA
- MCP tools not available in Claude Code

**Cause:**
Atlassian MCP is not installed or not properly configured.

**Solution:**
1. Install Atlassian MCP separately (not included in expansion pack)
2. Follow Atlassian MCP setup instructions for your IDE environment
3. Configure authentication:
   - API token (from Section 3.3)
   - OR OAuth 2.0
4. Set JIRA URL: `https://your-domain.atlassian.net`
5. Restart your IDE to load MCP configuration

**Verification:**
In your IDE, verify these tools are available:
- `mcp__atlassian__getJiraIssue`
- `mcp__atlassian__updateJiraIssue`
- `mcp__atlassian__addCommentToJiraIssue`
- `mcp__atlassian__searchJiraIssues`

Test connection:
```
mcp__atlassian__getJiraIssue(issueKey: "{existing-issue}")
Expected: Issue details returned
```

**References:**
- Atlassian MCP documentation: [link to official docs]
- BMAD MCP configuration guide: See BMAD core documentation

---

### Issue 4: Perplexity Research Fails

**Symptoms:**
- Stage 2 (CVE Research) times out or fails
- Error: Perplexity tools not available
- Enrichment completes but missing CVE research data

**Cause:**
- Perplexity MCP not installed or configured
- Network connectivity issues to Perplexity API
- MCP server not running
- API rate limiting

**Solution 1: Install and Configure Perplexity MCP**
```
Perplexity MCP is NOT installed by default. You must install it separately:

1. Follow Perplexity MCP installation instructions for your IDE
2. Configure MCP server connection in IDE settings
3. Restart your IDE
4. Verify tools are available:
   - mcp__perplexity__search
   - mcp__perplexity__reason
   - mcp__perplexity__deep_research
```

**Solution 2: Check Network Connectivity**
- Verify outbound HTTPS access to Perplexity API
- Check firewall rules allow Perplexity connections
- Ensure MCP server is running (check IDE MCP status)
- Test with simple Perplexity query in your IDE

**Solution 3: Use Manual Research Fallback**
If Perplexity installation is not possible or remains unavailable:
1. Agents will automatically fall back to manual research mode
2. Manually research CVE using:
   - NIST NVD: https://nvd.nist.gov
   - CISA KEV: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
   - FIRST EPSS: https://www.first.org/epss
3. Input research findings when prompted by agent

**Note:** Perplexity is not critical - agents can complete enrichments without it (will take longer).

---

### Issue 5: YAML Syntax Errors

**Symptoms:**
- Error: "Unable to load config.yaml"
- Error: "Invalid YAML syntax"
- Config file fails to parse

**Cause:**
YAML is whitespace-sensitive and has strict syntax rules.

**Common YAML Errors:**

**Error 1: Incorrect Indentation**
```yaml
# ❌ Wrong (tabs or wrong spacing)
jira:
cloud_id: "abc123"

# ✅ Correct (consistent spaces)
jira:
  cloud_id: "abc123"
```

**Error 2: Missing Quotes for Special Characters**
```yaml
# ❌ Wrong (colon in unquoted string)
description: Test: CVE-2024-1234

# ✅ Correct (quoted string)
description: "Test: CVE-2024-1234"
```

**Error 3: List Formatting**
```yaml
# ❌ Wrong (incorrect list syntax)
priorities: P1, P2, P3

# ✅ Correct (proper YAML list)
priorities: ["P1", "P2", "P3"]
# OR
priorities:
  - P1
  - P2
  - P3
```

**Solution:**
1. Use YAML validator: https://www.yamllint.com
   - Copy config.yaml contents
   - Paste into validator
   - Fix reported errors
2. OR use VS Code YAML extension:
   - Install "YAML" extension in VS Code
   - Open config.yaml
   - Look for red squiggly lines indicating errors
3. Common fixes:
   - Use spaces, not tabs
   - Quote strings with special characters (`:`, `#`, `@`)
   - Check indentation is consistent (usually 2 spaces per level)
   - Ensure no trailing spaces

**Verification:**
```bash
# Validate YAML syntax (requires Python)
python -c "import yaml; yaml.safe_load(open('.bmad-1898-engineering/config.yaml'))"

# Expected: No output (success)
# Error: Will show line number and error description
```

---

### Issue 6: Agent Commands Not Working

**Symptoms:**
- Agent activates but commands like `*enrich-ticket` not recognized
- Error: "Unknown command"
- Agent doesn't respond to `*help`

**Cause:**
- Command prefix incorrect (missing `*`)
- Agent not fully activated
- File paths incorrect

**Solution:**
1. Verify command syntax:
   - ✅ Correct: `*enrich-ticket SEC-100`
   - ❌ Wrong: `enrich-ticket SEC-100` (missing `*`)
2. Re-activate agent:
   ```
   /bmad-1898:agents:security-analyst
   ```
3. Wait for agent greeting and auto-`*help` display
4. Try `*help` command first to verify activation

**Verification:**
Agent should respond with numbered command list when you type `*help`.

---

### Issue 7: Enrichment File Not Created

**Symptoms:**
- Enrichment completes successfully
- JIRA updated correctly
- But no local file in `enrichments/` directory

**Cause:**
- Output directory doesn't exist
- Permissions issue
- Path configuration incorrect

**Solution:**
1. Create enrichments directory:
   ```bash
   mkdir -p enrichments
   ```
2. Verify permissions:
   ```bash
   ls -la enrichments/
   # Should be writable by current user
   ```
3. Re-run enrichment:
   ```
   *enrich-ticket SEC-100
   ```

**Expected Result:**
File created at: `enrichments/SEC-100-enrichment.md`

---

### Issue 8: Priority Calculation Incorrect

**Symptoms:**
- Enrichment completes but priority seems wrong
- P1 assigned to low CVSS vulnerability
- P5 assigned to critical vulnerability

**Cause:**
- Priority mapping in config.yaml doesn't match JIRA priority values
- Priority calculation logic issue

**Solution:**
1. Verify JIRA priority values:
   - In JIRA, go to Project Settings → Priorities
   - Note exact priority names (case-sensitive)
2. Update config.yaml priority_mapping to match:
   ```yaml
   priority_mapping:
     P1: "Critical"  # Must match JIRA exactly
     P2: "High"
     P3: "Medium"
     P4: "Low"
     P5: "Trivial"
   ```
3. Check priority calculation logic in enrichment output:
   - CVSS, EPSS, KEV, Exposure factors
   - Verify calculation makes sense given input data

**Verification:**
Check `enrichments/{issue-key}-enrichment.md` for priority calculation explanation.

---

### Getting Further Help

If issues persist after trying troubleshooting steps:

**1. Check Debug Logs**
- Location: `.ai/debug-log.md` (if configured)
- Contains detailed error messages and stack traces

**2. Review Documentation**
- Configuration Reference & Customization Guide (detailed config.yaml reference)
- Security Analyst Agent Usage Guide (detailed usage instructions)

**3. Community Support**
- GitHub Issues: [repository-url]/issues
- Discord: [discord-invite-link]
- Documentation: [docs-url]

**4. When Reporting Issues**
Include:
- Error message (exact text)
- Steps to reproduce
- Config.yaml (redact sensitive values like cloud_id, API tokens)
- JIRA custom field configuration
- IDE and version (Cursor, VS Code + extension, etc.)
- Expansion pack version

---

## 10. Next Steps

**Congratulations!** You've successfully installed and configured the bmad-1898-engineering expansion pack.

### Recommended Learning Path

**1. Security Analyst Agent Usage**
- Comprehensive guide to running enrichments
- Batch processing workflows
- Advanced research techniques
- See: Security Analyst Agent Usage Guide

**2. Security Reviewer Agent Usage**
- How to perform security reviews
- Approval and change request workflows
- Review quality standards
- See: Security Reviewer Agent Usage Guide

**3. Configuration Customization**
- Advanced config.yaml options
- Custom priority calculations
- Review trigger tuning
- Notification integrations
- See: Configuration Reference & Customization Guide

**4. Advanced Workflows**
- Vulnerability lifecycle management
- Batch processing at scale
- Integration with security tools
- See: Additional workflow documentation

### Start Using the System

**For Daily Vulnerability Management:**
1. Activate Security Analyst: `/bmad-1898:agents:security-analyst`
2. Enrich tickets: `*enrich-ticket {issue-key}`
3. For batch processing: `*batch-enrich {filter-jql}`

**For Security Reviews:**
1. Activate Security Reviewer: `/bmad-1898:agents:security-reviewer`
2. Review enrichments: `*review-enrichment {issue-key}`
3. Approve or request changes

**For Help:**
- Type `*help` in any active agent to see available commands
- Refer to this installation guide for setup issues
- Check troubleshooting section (Section 9) for common problems

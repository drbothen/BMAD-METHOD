# Vault Configuration Guide

## Overview

The BMAD 2nd Brain expansion pack supports multiple Obsidian vaults with flexible organization methods. Each vault can be configured independently with different organizational structures, agent enablement, and processing preferences.

This guide explains how to configure vaults using the `vault-mappings.yaml` configuration file.

---

## Table of Contents

1. [Configuration File Location](#configuration-file-location)
2. [Configuration Structure](#configuration-structure)
3. [Organization Methods](#organization-methods)
4. [Key Locations Mapping](#key-locations-mapping)
5. [Agent Enablement](#agent-enablement)
6. [Auto-Processing Settings](#auto-processing-settings)
7. [Excluded Folders](#excluded-folders)
8. [Examples](#examples)
9. [Validation Rules](#validation-rules)
10. [Troubleshooting](#troubleshooting)

---

## Configuration File Location

Vault configurations are stored in:
```
expansion-packs/bmad-obsidian-2nd-brain/config/vault-mappings.yaml
```

This file contains all vault configurations and global defaults.

---

## Configuration Structure

### Vault Object Schema

Each vault in the `vaults` array has the following structure:

```yaml
vaults:
  - id: "vault-001"                    # REQUIRED: Unique identifier
    name: "Personal Vault"              # REQUIRED: Human-readable name
    path: "/path/to/vault"              # REQUIRED: Absolute path to vault
    enabled: true                       # REQUIRED: Enable/disable vault
    organizationMethod: "para"          # REQUIRED: Organization method
    keyLocations:                       # OPTIONAL: Folder mappings
      inbox: "00 Inbox"
      projects: "10 Projects"
      # ... more locations
    agentsEnabled:                      # OPTIONAL: Agent IDs to enable
      - inbox-triage-agent
      - semantic-linker
    autoProcessing:                     # OPTIONAL: Auto-processing config
      enabled: true
      schedule: "daily"
      time: "09:00"
    excludedFolders:                    # OPTIONAL: Folders to skip
      - ".trash"
      - "Archive"
```

### Required Fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `id` | string | Unique vault identifier | Alphanumeric and hyphens only (`^[a-zA-Z0-9-]+$`) |
| `name` | string | Human-readable vault name | Non-empty string |
| `path` | string | Absolute path to vault directory | Must be absolute, readable, and writable |
| `enabled` | boolean | Whether vault is active | `true` or `false` |
| `organizationMethod` | string | Organization method | One of: `para`, `zettelkasten`, `lyt`, `johnny-decimal`, `custom` |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `keyLocations` | object | Method-specific defaults | Folder mappings for different purposes |
| `agentsEnabled` | array | All agents | List of agent IDs to enable for this vault |
| `autoProcessing` | object | Disabled | Automated processing configuration |
| `excludedFolders` | array | `[".trash", ".obsidian"]` | Folders to skip during processing |

---

## Organization Methods

The expansion pack supports five organizational methodologies. Choose the one that matches your vault structure.

### 1. PARA (Projects, Areas, Resources, Archives)

**Description:** Project-based organization system with four main categories.

**Characteristics:**
- **Projects:** Short-term efforts with deadlines
- **Areas:** Long-term responsibilities
- **Resources:** Reference materials and topics of interest
- **Archives:** Inactive/completed items

**Default Key Locations:**
```yaml
organizationMethod: "para"
keyLocations:
  inbox: "00 Inbox"
  projects: "10 Projects"
  areas: "20 Areas"
  resources: "30 Resources"
  archive: "40 Archive"
  atomicNotes: "50 Atomic Notes"
  mocs: "60 MOCs"
  agentOutput: "99 Agent Output"
  templates: "100 Templates"
```

**Best For:**
- Project-oriented workflows
- GTD (Getting Things Done) practitioners
- Clear separation between active and archived work

---

### 2. Zettelkasten

**Description:** Flat structure with atomic notes and heavy linking.

**Characteristics:**
- Minimal folder hierarchy
- Emphasis on note atomicity (one idea per note)
- Heavy use of bidirectional links
- Timestamp or ID-based note naming

**Default Key Locations:**
```yaml
organizationMethod: "zettelkasten"
keyLocations:
  inbox: "Inbox"                  # Fleeting notes
  atomicNotes: "Permanent"        # Permanent atomic notes
  mocs: "Structure Notes"         # Structure/index notes
  resources: "Reference"          # Literature notes
  archive: "Archive"
  agentOutput: "AI Generated"
  templates: "Templates"
```

**Best For:**
- Research and academic work
- Building interconnected knowledge networks
- Long-form writing and synthesis
- Luhmann-style note-taking

---

### 3. LYT (Linking Your Thinking)

**Description:** Map of Contents (MOC) centric organization.

**Characteristics:**
- Heavy use of MOCs as entry points
- Flexible linking structure
- Emphasis on thinking and synthesis
- Notes organized by thought patterns, not just topics

**Default Key Locations:**
```yaml
organizationMethod: "lyt"
keyLocations:
  inbox: "000 Inbox"
  mocs: "100 MOCs"               # Primary MOCs
  atomicNotes: "200 Notes"
  projects: "300 Projects"
  areas: "400 Areas"
  resources: "500 Resources"
  archive: "900 Archive"
  agentOutput: "950 AI Output"
  templates: "999 Templates"
```

**Best For:**
- Creative thinkers
- Writers and content creators
- Those who prefer emergent structure
- Synthesis-focused workflows

---

### 4. Johnny Decimal

**Description:** Strict numerical categorization system.

**Characteristics:**
- Everything has a number
- Consistent numerical hierarchy (10-19, 20-29, etc.)
- Quick navigation via numbers
- Rigid but highly organized

**Default Key Locations:**
```yaml
organizationMethod: "johnny-decimal"
keyLocations:
  inbox: "00-09 System/00 Inbox"
  projects: "10-19 Projects"
  areas: "20-29 Areas"
  resources: "30-39 Resources"
  archive: "90-99 Archive/90 Inactive"
  atomicNotes: "40-49 Knowledge/40 Atomic Notes"
  mocs: "40-49 Knowledge/45 MOCs"
  agentOutput: "00-09 System/05 AI Output"
  templates: "00-09 System/09 Templates"
```

**Best For:**
- Highly organized individuals
- Those who prefer strict structure
- Quick reference and retrieval
- Professional/business contexts

---

### 5. Custom

**Description:** User-defined structure that doesn't match standard patterns.

**Characteristics:**
- Complete flexibility
- Requires explicit keyLocations specification
- No automatic detection
- User must map all folder purposes

**Configuration:**
```yaml
organizationMethod: "custom"
keyLocations:
  inbox: "Your Custom Inbox Folder"
  projects: "Your Projects Folder"
  # ... specify all locations explicitly
```

**Best For:**
- Unique organizational systems
- Hybrid approaches combining multiple methods
- Specialized workflows

---

## Key Locations Mapping

Key locations define where different types of content are stored in your vault. The expansion pack uses these mappings to determine where to create new notes.

### Standard Key Locations

| Location | Purpose | Used By |
|----------|---------|---------|
| `inbox` | New, unprocessed notes | Inbox Triage Agent |
| `projects` | Active projects | Project-related agents |
| `areas` | Ongoing responsibilities | Area management agents |
| `resources` | Reference materials | Content curation agents |
| `archive` | Completed/inactive items | Archival agents |
| `atomicNotes` | Atomic, permanent notes | Atomic Note Creator |
| `mocs` | Maps of Content | Semantic Linker, Query Interpreter |
| `agentOutput` | AI-generated content | All agents |
| `templates` | Note templates | Template system |

### Folder Path Format

- **Relative to vault root:** All paths are relative to the vault root directory
- **No leading slashes:** Use `"Projects"` not `"/Projects"`
- **Nested folders:** Use `"Folder/Subfolder"` format
- **Spaces allowed:** `"00 Inbox"` is valid

### Auto-Detection

The vault analyzer (`vault-analyzer.js`) can automatically detect key locations based on folder names. Common patterns include:

- **Inbox:** folders containing "inbox", "capture", "fleeting", "unsorted"
- **Projects:** folders containing "projects", "active", "current"
- **Areas:** folders containing "areas", "responsibilities", "ongoing"
- **Resources:** folders containing "resources", "reference", "library", "knowledge"
- **Archive:** folders containing "archive", "old", "inactive", "completed"

---

## Agent Enablement

Control which agents are active for each vault.

### Available Agents

| Agent ID | Description | Typical Use Cases |
|----------|-------------|-------------------|
| `inbox-triage-agent` | Processes inbox notes, suggests organization | Daily inbox processing |
| `atomic-note-creator` | Fragments large notes into atomic notes | Note refinement |
| `semantic-linker` | Creates bidirectional links between related notes | Knowledge graph building |
| `query-interpreter` | Answers questions from vault content | Knowledge retrieval |
| `quality-auditor` | Reviews note quality and completeness | Content quality control |

### Configuration

**Enable specific agents:**
```yaml
agentsEnabled:
  - inbox-triage-agent
  - semantic-linker
  - quality-auditor
```

**Enable all agents (default):**
```yaml
agentsEnabled: []  # Empty array = all agents enabled
```

**Disable all agents:**
```yaml
agentsEnabled: null
enabled: false  # Better to disable the entire vault
```

### Per-Agent Configuration

Some agents support additional configuration. This will be documented in future versions.

---

## Auto-Processing Settings

Configure automated processing schedules for each vault.

### Configuration Options

```yaml
autoProcessing:
  enabled: true          # Enable/disable auto-processing
  schedule: "daily"      # Schedule: "daily", "weekly", "manual"
  time: "09:00"          # Time in 24-hour format (HH:MM)
```

### Schedule Options

| Schedule | Description | Use Case |
|----------|-------------|----------|
| `daily` | Process once per day at specified time | Active vaults with frequent updates |
| `weekly` | Process once per week | Archive vaults or low-activity vaults |
| `manual` | No automatic processing | Complete manual control |

### Processing Actions

When auto-processing runs, enabled agents will:
1. Process inbox notes (inbox-triage-agent)
2. Create atomic notes from large notes (atomic-note-creator)
3. Generate semantic links (semantic-linker)
4. Audit note quality (quality-auditor)

### Disabling Auto-Processing

```yaml
autoProcessing:
  enabled: false
```

---

## Excluded Folders

Specify folders to skip during processing.

### Default Exclusions

```yaml
excludedFolders:
  - ".trash"      # Obsidian trash folder
  - ".obsidian"   # Obsidian config folder
  - ".git"        # Git repository data
```

### Common Exclusions

```yaml
excludedFolders:
  - ".trash"
  - ".obsidian"
  - "Archive"           # Don't process archived content
  - "Templates"         # Don't process template files
  - "Attachments"       # Don't process media files
  - "Private"           # Don't process private notes
  - "Old"               # Don't process old content
```

### Wildcard Patterns (Future Enhancement)

Currently, only exact folder name matching is supported. Wildcard patterns may be added in future versions.

---

## Examples

### Example 1: PARA Vault for Work

```yaml
- id: "work-vault"
  name: "Work - GTD System"
  path: "/Users/username/Documents/Obsidian/Work"
  enabled: true
  organizationMethod: "para"
  keyLocations:
    inbox: "00 Inbox"
    projects: "10 Projects"
    areas: "20 Areas"
    resources: "30 Resources"
    archive: "40 Archive"
    atomicNotes: "50 Knowledge"
    mocs: "60 Maps"
    agentOutput: "99 AI"
    templates: "100 Templates"
  agentsEnabled:
    - inbox-triage-agent
    - semantic-linker
    - quality-auditor
  autoProcessing:
    enabled: true
    schedule: "daily"
    time: "08:00"
  excludedFolders:
    - "Archive"
    - "Templates"
    - ".trash"
```

### Example 2: Zettelkasten for Research

```yaml
- id: "research-vault"
  name: "Research - Zettelkasten"
  path: "/Users/username/Documents/Obsidian/Research"
  enabled: true
  organizationMethod: "zettelkasten"
  keyLocations:
    inbox: "Fleeting"
    atomicNotes: "Permanent"
    mocs: "Structure"
    resources: "Literature"
    archive: "Archive"
    agentOutput: "AI"
    templates: "Meta"
  agentsEnabled:
    - inbox-triage-agent
    - atomic-note-creator
    - semantic-linker
  autoProcessing:
    enabled: true
    schedule: "daily"
    time: "09:00"
  excludedFolders:
    - "Archive"
    - ".trash"
```

### Example 3: LYT Vault for Creative Writing

```yaml
- id: "writing-vault"
  name: "Creative Writing - LYT"
  path: "/Users/username/Documents/Obsidian/Writing"
  enabled: true
  organizationMethod: "lyt"
  keyLocations:
    inbox: "000 Inbox"
    mocs: "100 MOCs"
    atomicNotes: "200 Ideas"
    projects: "300 Stories"
    areas: "400 Themes"
    resources: "500 Research"
    archive: "900 Drafts"
    agentOutput: "950 AI"
    templates: "999 Templates"
  agentsEnabled:
    - inbox-triage-agent
    - semantic-linker
    - query-interpreter
  autoProcessing:
    enabled: false  # Manual processing for creative work
  excludedFolders:
    - "900 Drafts"
    - ".trash"
```

### Example 4: Johnny Decimal for Professional Knowledge Base

```yaml
- id: "kb-vault"
  name: "Knowledge Base - Johnny Decimal"
  path: "/Users/username/Documents/Obsidian/KnowledgeBase"
  enabled: true
  organizationMethod: "johnny-decimal"
  keyLocations:
    inbox: "00-09 System/00 Inbox"
    projects: "10-19 Projects"
    areas: "20-29 Areas"
    resources: "30-39 Resources"
    archive: "90-99 Archive"
    atomicNotes: "40-49 Knowledge/40 Notes"
    mocs: "40-49 Knowledge/45 Maps"
    agentOutput: "00-09 System/05 AI"
    templates: "00-09 System/09 Templates"
  agentsEnabled:
    - inbox-triage-agent
    - atomic-note-creator
    - semantic-linker
    - quality-auditor
  autoProcessing:
    enabled: true
    schedule: "weekly"
    time: "08:00"
  excludedFolders:
    - "90-99 Archive"
    - ".trash"
```

### Example 5: Multiple Vaults Configuration

```yaml
vaults:
  - id: "personal"
    name: "Personal Notes"
    path: "/Users/username/Vaults/Personal"
    enabled: true
    organizationMethod: "para"
    # ... configuration

  - id: "work"
    name: "Work Knowledge Base"
    path: "/Users/username/Vaults/Work"
    enabled: true
    organizationMethod: "johnny-decimal"
    # ... configuration

  - id: "archive"
    name: "Archived Vault"
    path: "/Users/username/Vaults/Archive"
    enabled: false  # Disabled vault
    organizationMethod: "custom"
    # ... configuration
```

---

## Validation Rules

### Path Validation

1. **Must be absolute:** Relative paths are rejected
   - ✅ `/Users/username/Documents/Vault`
   - ❌ `../Documents/Vault`
   - ❌ `~/Documents/Vault` (use full path)

2. **Must exist:** Path must exist on filesystem
3. **Must be readable:** User must have read permission
4. **Must be writable:** User must have write permission
5. **Path traversal prevention:** `../` sequences are rejected
6. **Symbolic links:** Resolved to real paths

### Vault ID Validation

- **Format:** Alphanumeric and hyphens only
- **Regex:** `^[a-zA-Z0-9-]+$`
- **Examples:**
  - ✅ `vault-001`
  - ✅ `personal-vault`
  - ✅ `work2024`
  - ❌ `vault 001` (spaces not allowed)
  - ❌ `vault_001` (underscores not allowed)

### Organization Method Validation

Must be one of:
- `para`
- `zettelkasten`
- `lyt`
- `johnny-decimal`
- `custom`

### Valid Obsidian Vault

Must contain `.obsidian/` directory in vault root.

---

## Troubleshooting

### Vault Not Detected

**Problem:** Vault doesn't appear in discovered vaults list.

**Solutions:**
1. Ensure Obsidian has been opened at least once
2. Check Obsidian config location:
   - macOS: `~/Library/Application Support/obsidian/`
   - Windows: `%APPDATA%\Obsidian\`
   - Linux: `~/.config/obsidian/`
3. Verify `obsidian.json` exists and is valid JSON
4. Run vault discovery: `node tools/vault-discovery.js`

### Path Not Accessible

**Problem:** Vault path exists but is marked as inaccessible.

**Solutions:**
1. Check file permissions: `ls -la /path/to/vault`
2. Ensure read/write permissions for user
3. Check if path is on network drive (may have connectivity issues)
4. Verify vault isn't locked by another process

### Organization Method Not Detected

**Problem:** Vault analyzer detects wrong organization method or "custom".

**Solutions:**
1. Run vault analyzer: `node tools/vault-analyzer.js /path/to/vault`
2. Check confidence score (low confidence = unclear structure)
3. Manually specify organization method in config
4. Ensure folder names match expected patterns
5. Review folder structure for consistency

### Low Detection Confidence

**Problem:** Vault analyzer has low confidence (<50%).

**Recommendations:**
1. Manually specify organization method
2. Review and standardize folder naming
3. Consider using "custom" organization method
4. Explicitly define all keyLocations

### Agent Not Working

**Problem:** Enabled agent doesn't process vault.

**Solutions:**
1. Verify agent ID is correct (check available agents list)
2. Ensure vault is enabled (`enabled: true`)
3. Check if required keyLocations are defined
4. Review agent-specific requirements
5. Check auto-processing schedule settings

### Configuration File Errors

**Problem:** YAML parsing errors or invalid configuration.

**Solutions:**
1. Validate YAML syntax: Use online YAML validator
2. Check indentation (use spaces, not tabs)
3. Ensure quotes around paths with spaces
4. Verify all required fields are present
5. Check for typos in organization method names

---

## Additional Resources

- **Vault Discovery Tool:** `tools/vault-discovery.js`
- **Vault Analyzer Tool:** `tools/vault-analyzer.js`
- **Configuration File:** `config/vault-mappings.yaml`
- **Test Suite:** `tests/integration/test-vault-discovery.js`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-09 | Initial documentation for STORY-019 |

---

## Feedback and Contributions

For issues, questions, or contributions:
- GitHub Issues: https://github.com/bmadcode/bmad-method/issues
- Discord: https://discord.gg/gk8jAdXWmj

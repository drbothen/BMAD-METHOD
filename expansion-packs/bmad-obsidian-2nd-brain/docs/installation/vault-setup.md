# Vault Setup and Configuration Guide

Complete guide for setting up and configuring Obsidian vaults with the BMAD 2nd Brain expansion pack.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Interactive Configuration Wizard](#interactive-configuration-wizard)
5. [CLI Command Reference](#cli-command-reference)
6. [Organization Methods](#organization-methods)
7. [Configuration Examples](#configuration-examples)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The BMAD 2nd Brain expansion pack supports multiple Obsidian vaults with different organizational methodologies. Each vault can be configured independently with:

- **Organization method** (PARA, Zettelkasten, LYT, Johnny Decimal, Custom)
- **Enabled agents** (inbox triage, semantic linker, quality auditor, etc.)
- **Auto-processing settings** (daily, weekly, or manual)
- **Key folder locations** (inbox, projects, areas, resources, etc.)

The vault CLI provides both interactive and command-line tools for configuration.

---

## Prerequisites

Before configuring vaults, ensure:

1. **Obsidian installed** and opened at least once (creates config files)
2. **Node.js v16+** installed
3. **BMAD 2nd Brain expansion pack** installed
4. **At least one Obsidian vault** created

---

## Quick Start

### Option 1: Interactive Wizard (Recommended)

The easiest way to configure vaults:

```bash
node expansion-packs/bmad-obsidian-2nd-brain/tools/vault-cli.js configure
```

This will:
1. Auto-detect your Obsidian vaults
2. Let you select which vaults to configure
3. Analyze each vault's structure
4. Detect organization method (or let you choose)
5. Configure agents and auto-processing
6. Save configuration to `vault-mappings.yaml`

### Option 2: Manual Commands

For more control:

```bash
# 1. Discover vaults
node tools/vault-cli.js detect-vaults

# 2. Add a vault
node tools/vault-cli.js vault:add /path/to/your/vault

# 3. List configured vaults
node tools/vault-cli.js vault:list

# 4. Adjust settings
node tools/vault-cli.js set-organization vault-001 para
```

---

## Interactive Configuration Wizard

### Starting the Wizard

```bash
cd expansion-packs/bmad-obsidian-2nd-brain
node tools/vault-cli.js configure
```

### Wizard Steps

**Step 1: Vault Detection**
- Automatically scans for Obsidian vaults on your system
- Displays detected vaults with paths and IDs
- Shows accessibility status

**Step 2: Vault Selection**
- Checkbox list of detected vaults
- Select one or more vaults to configure
- Can skip vaults you don't want to manage

**Step 3: Organization Method**
- Analyzes vault structure
- Detects likely organization method with confidence score
- Prompts to confirm or override detection
- Options: PARA, Zettelkasten, LYT, Johnny Decimal, Custom

**Step 4: Agent Selection**
- Checkbox list of available agents
- Pre-selects common agents
- Options:
  - Inbox Triage Agent
  - Atomic Note Creator
  - Semantic Linker
  - Query Interpreter
  - Quality Auditor

**Step 5: Auto-Processing**
- Choose whether to enable automated processing
- If enabled, select schedule (daily/weekly/manual)
- Set processing time (HH:MM format)

**Step 6: Confirmation**
- Reviews configuration
- Saves to `vault-mappings.yaml`
- Displays vault IDs for future reference

---

## CLI Command Reference

All commands use the format:
```bash
node tools/vault-cli.js <command> [arguments]
```

### Help

Display all available commands:

```bash
node tools/vault-cli.js help
# or
node tools/vault-cli.js --help
```

### configure

Run the interactive configuration wizard:

```bash
node tools/vault-cli.js configure
```

**Use when:**
- Setting up vaults for the first time
- Adding multiple vaults at once
- Want guided configuration process

### detect-vaults

Discover Obsidian vaults on your system:

```bash
node tools/vault-cli.js detect-vaults
```

**Output:**
- Total vaults found
- Accessible vs inaccessible vaults
- Vault paths, IDs, and types
- Validation status

**Use when:**
- Want to see what vaults are available
- Checking if Obsidian is properly installed
- Verifying vault accessibility

### vault:add

Add a vault to configuration:

```bash
node tools/vault-cli.js vault:add <path>
```

**Arguments:**
- `<path>` - Absolute path to vault directory

**Example:**
```bash
node tools/vault-cli.js vault:add /Users/username/Documents/MyVault
```

**What it does:**
1. Validates path (checks if valid Obsidian vault)
2. Analyzes vault structure
3. Auto-detects organization method
4. Generates suggested configuration
5. Adds to `vault-mappings.yaml`

**Use when:**
- Adding a vault discovered outside auto-detection
- Adding vaults one at a time
- Scripting vault additions

### vault:remove

Remove a vault from configuration:

```bash
node tools/vault-cli.js vault:remove <vault-id>
```

**Arguments:**
- `<vault-id>` - Vault identifier (e.g., `vault-001`)

**Example:**
```bash
node tools/vault-cli.js vault:remove vault-001
```

**Use when:**
- No longer want to manage a vault
- Vault has been moved or deleted
- Cleaning up old configurations

**Note:** This only removes from configuration, doesn't delete the vault itself.

### vault:list

List all configured vaults:

```bash
node tools/vault-cli.js vault:list
```

**Output for each vault:**
- Vault ID
- Name
- Path
- Organization method
- Enabled/disabled status
- Number of agents enabled
- Auto-processing schedule

**Use when:**
- Want to see all configured vaults
- Checking vault status
- Finding vault IDs for other commands

### vault:enable

Enable a disabled vault:

```bash
node tools/vault-cli.js vault:enable <vault-id>
```

**Arguments:**
- `<vault-id>` - Vault identifier

**Example:**
```bash
node tools/vault-cli.js vault:enable vault-001
```

**Use when:**
- Re-enabling a temporarily disabled vault
- Starting to manage a vault again
- Testing vault activation

### vault:disable

Disable a vault without removing it:

```bash
node tools/vault-cli.js vault:disable <vault-id>
```

**Arguments:**
- `<vault-id>` - Vault identifier

**Example:**
```bash
node tools/vault-cli.js vault:disable vault-001
```

**Use when:**
- Temporarily stop processing a vault
- Testing without a vault
- Archiving a vault but keeping config

**Note:** Disabled vaults remain in configuration but are not processed by agents.

### set-organization

Change a vault's organization method:

```bash
node tools/vault-cli.js set-organization <vault-id> <method>
```

**Arguments:**
- `<vault-id>` - Vault identifier
- `<method>` - Organization method (para, zettelkasten, lyt, johnny-decimal, custom)

**Example:**
```bash
node tools/vault-cli.js set-organization vault-001 para
```

**Use when:**
- Reorganizing your vault
- Auto-detection was incorrect
- Switching organization systems

---

## Organization Methods

### PARA (Projects, Areas, Resources, Archives)

**Description:** Project-based organization with four main categories.

**Best for:**
- GTD (Getting Things Done) practitioners
- Project-oriented work
- Clear separation of active vs archived

**Typical Structure:**
```
00 Inbox/
10 Projects/
20 Areas/
30 Resources/
40 Archive/
```

**Configure:**
```bash
node tools/vault-cli.js set-organization <vault-id> para
```

### Zettelkasten

**Description:** Flat structure with atomic notes and heavy linking.

**Best for:**
- Research and academic work
- Building interconnected knowledge networks
- Long-form writing and synthesis

**Typical Structure:**
```
Inbox/
Permanent/
Literature/
Reference/
```

**Configure:**
```bash
node tools/vault-cli.js set-organization <vault-id> zettelkasten
```

### LYT (Linking Your Thinking)

**Description:** Map of Contents (MOC) centric organization.

**Best for:**
- Creative thinkers
- Writers and content creators
- Emergent structure preference

**Typical Structure:**
```
000 Inbox/
100 MOCs/
200 Notes/
300 Projects/
```

**Configure:**
```bash
node tools/vault-cli.js set-organization <vault-id> lyt
```

### Johnny Decimal

**Description:** Strict numerical categorization.

**Best for:**
- Highly organized individuals
- Quick reference and retrieval
- Professional/business contexts

**Typical Structure:**
```
00-09 System/
10-19 Projects/
20-29 Areas/
30-39 Resources/
```

**Configure:**
```bash
node tools/vault-cli.js set-organization <vault-id> johnny-decimal
```

### Custom

**Description:** User-defined structure.

**Best for:**
- Unique organizational systems
- Hybrid approaches
- Specialized workflows

**Configure:**
```bash
node tools/vault-cli.js set-organization <vault-id> custom
```

---

## Configuration Examples

### Example 1: Single PARA Vault

```bash
# Detect available vaults
node tools/vault-cli.js detect-vaults

# Add vault
node tools/vault-cli.js vault:add /Users/username/Documents/PersonalVault

# Verify configuration
node tools/vault-cli.js vault:list
```

### Example 2: Multiple Vaults (Work + Personal)

```bash
# Use interactive wizard for multiple vaults
node tools/vault-cli.js configure

# During wizard:
# - Select both Work and Personal vaults
# - Work: Johnny Decimal, daily auto-processing
# - Personal: PARA, manual processing
```

### Example 3: Migrating to New Organization Method

```bash
# Check current configuration
node tools/vault-cli.js vault:list

# Change organization method
node tools/vault-cli.js set-organization vault-001 zettelkasten

# Verify change
node tools/vault-cli.js vault:list
```

### Example 4: Temporarily Disabling a Vault

```bash
# Disable vault during reorganization
node tools/vault-cli.js vault:disable vault-002

# Work on vault reorganization...

# Re-enable when ready
node tools/vault-cli.js vault:enable vault-002
```

---

## Troubleshooting

### Vault Not Detected

**Problem:** `detect-vaults` doesn't find your vault.

**Solutions:**
1. Ensure Obsidian has been opened at least once
2. Check Obsidian config exists:
   - macOS: `~/Library/Application Support/obsidian/obsidian.json`
   - Windows: `%APPDATA%\Obsidian\obsidian.json`
   - Linux: `~/.config/obsidian/obsidian.json`
3. Manually add vault with `vault:add` command

### Path Not Accessible

**Problem:** "Path does not exist" or "No read/write permission" error.

**Solutions:**
1. Check path is correct and absolute
2. Verify file permissions: `ls -la /path/to/vault`
3. Ensure vault hasn't been moved or deleted
4. Check symbolic links resolve correctly

### Invalid Vault

**Problem:** "Not a valid Obsidian vault" error.

**Solutions:**
1. Ensure `.obsidian` directory exists in vault root
2. Check vault was created by Obsidian (not just an empty folder)
3. Try opening vault in Obsidian first

### Organization Method Detection Wrong

**Problem:** Auto-detection chooses wrong organization method.

**Solutions:**
1. Manually set organization method:
   ```bash
   node tools/vault-cli.js set-organization <vault-id> <correct-method>
   ```
2. Check folder naming matches expected patterns
3. Use `custom` method and manually configure key locations

### Configuration Not Saving

**Problem:** Changes don't persist after restart.

**Solutions:**
1. Check write permissions for config directory
2. Verify `vault-mappings.yaml` is not read-only
3. Check for file system errors
4. Ensure config directory exists: `expansion-packs/bmad-obsidian-2nd-brain/config/`

### CLI Command Not Found

**Problem:** `vault-cli.js` command fails.

**Solutions:**
1. Ensure you're in correct directory
2. Use full path to script:
   ```bash
   node /full/path/to/expansion-packs/bmad-obsidian-2nd-brain/tools/vault-cli.js
   ```
3. Check file has execute permissions: `chmod +x tools/vault-cli.js`
4. Verify Node.js is installed: `node --version`

---

## Configuration File Location

All vault configurations are stored in:
```
expansion-packs/bmad-obsidian-2nd-brain/config/vault-mappings.yaml
```

You can manually edit this file, but using the CLI is recommended for validation.

---

## Next Steps

After configuring your vaults:

1. **Test Configuration**: Run agents to verify vault access
2. **Review Documentation**: See [vault-configuration-guide.md](../vault-configuration-guide.md) for advanced options
3. **Set Up Neo4j**: Optional temporal tracking (see [neo4j-setup.md](./neo4j-setup.md))
4. **Configure MCP**: Set up Claude Desktop integration (see [mcp-server-setup.md](./mcp-server-setup.md))

---

## Additional Resources

- **Complete Configuration Reference**: [../vault-configuration-guide.md](../vault-configuration-guide.md)
- **Agent Documentation**: [../../agents/](../../agents/)
- **Troubleshooting Guide**: [../vault-configuration-guide.md#troubleshooting](../vault-configuration-guide.md#troubleshooting)

---

**Need Help?**
- Discord: https://discord.gg/gk8jAdXWmj
- GitHub Issues: https://github.com/bmadcode/bmad-method/issues

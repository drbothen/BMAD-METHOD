# Troubleshooting Guide - Technical Writing Expansion Pack

Common issues and solutions for the BMad Technical Writing Expansion Pack.

## Installation Issues

### Issue: "Expansion pack not found"
**Symptom**: Cannot activate agents, "bmad-technical-writing not found" error

**Cause**: Expansion pack not installed or not in correct location

**Solution**:
```bash
# Verify installation
ls ~/.bmad-method/expansion-packs/bmad-technical-writing

# If missing, reinstall
npx bmad-method install
# Select "Technical Book Writing Studio"
```

### Issue: "Dependencies not resolving"
**Symptom**: Agent activation fails with missing template/task errors

**Cause**: Incomplete installation or corrupted files

**Solution**:
```bash
# Reinstall expansion pack
npx bmad-method install --force
```

## Agent Activation Issues

### Issue: "Agent not responding"
**Symptom**: Agent activates but doesn't respond to commands

**Cause**: AI context limit reached or agent definition not loaded

**Solution**:
1. Check agent loaded correctly (should show persona description)
2. Try `*help` command to see available commands
3. If still unresponsive, re-activate agent

### Issue: "Commands not recognized"
**Symptom**: Agent doesn't recognize `*command-name`

**Cause**: Typo in command or command doesn't exist for this agent

**Solution**:
1. Run `*help` to see valid commands for current agent
2. Check command spelling (commands are case-sensitive)
3. Verify you're using correct agent for the task

### Issue: "Agent dependencies missing"
**Symptom**: Agent can't find templates, tasks, or checklists

**Cause**: Files not in expected location

**Solution**:
```bash
# Verify file structure
ls expansion-packs/bmad-technical-writing/templates/
ls expansion-packs/bmad-technical-writing/tasks/
ls expansion-packs/bmad-technical-writing/checklists/
```

## Workflow Execution Issues

### Issue: "Workflow fails at step X"
**Symptom**: Workflow stops mid-execution with error

**Cause**: Missing prerequisite or validation failure

**Solution**:
1. Check workflow prerequisites (see workflow YAML file)
2. Verify previous steps completed successfully
3. Review quality gates - ensure they passed

### Issue: "Inputs not accepted"
**Symptom**: Workflow rejects provided inputs

**Cause**: Invalid format or missing required fields

**Solution**:
1. Check template requirements (see template YAML file)
2. Ensure all required fields provided
3. Verify format matches expected structure

### Issue: "Outputs not produced"
**Symptom**: Workflow completes but output file not created

**Cause**: File path issue or write permissions

**Solution**:
```bash
# Check directory exists
mkdir -p manuscript/planning manuscript/sections manuscript/chapters

# Check write permissions
ls -la docs/
```

## Build/Validation Errors

### Issue: "npm run validate fails"
**Symptom**: Validation command reports errors

**Cause**: Invalid YAML syntax or missing required fields

**Solution**:
```bash
# See specific errors
npm run validate

# Common fixes:
# - Check YAML indentation (use spaces, not tabs)
# - Verify all required fields present
# - Check for typos in agent/workflow references
```

### Issue: "YAML syntax error"
**Symptom**: Parse error when loading configuration

**Cause**: Invalid YAML formatting

**Solution**:
1. Check indentation (2 spaces per level)
2. Verify no tabs used (YAML requires spaces)
3. Check quotes around special characters
4. Use YAML validator online

## Integration Issues

### Issue: "Conflicts with core BMad"
**Symptom**: Agents or commands conflict

**Cause**: Name collision or incompatible versions

**Solution**:
1. Use full agent IDs: `/bmad-tw:agent-name`
2. Update both core and expansion pack to latest versions

### Issue: "Multi-expansion conflicts"
**Symptom**: Multiple expansion packs interfere with each other

**Cause**: Agent name collisions

**Solution**:
1. Use full qualified names: `/bmad-tw:agent` vs `/bmad-cw:agent`
2. Activate only needed agents

## General Troubleshooting Tips

### Check Logs
```bash
# View debug logs if available
cat .ai/debug-log.md
```

### Verify Installation
```bash
# Check all required files present
npm run validate
```

### Update to Latest Version
```bash
# Pull latest changes
git pull origin main

# Rebuild
npm run build
```

### Clear Cache
```bash
# Remove dist files and rebuild
rm -rf dist/
npm run build
```

## Getting Help

If your issue isn't listed here:

1. **Check Documentation**
   - [User Guide](user-guide.md) - System overview
   - [FAQ](faq.md) - Common questions

2. **Community Support**
   - [Discord](https://discord.gg/gk8jAdXWmj) - Real-time help
   - [GitHub Discussions](https://github.com/bmadcode/bmad-method/discussions) - Q&A

3. **Report Bugs**
   - [GitHub Issues](https://github.com/bmadcode/bmad-method/issues) - Bug reports
   - Include: Error message, steps to reproduce, environment details

---

*Troubleshooting Guide - Technical Writing Expansion Pack v1.1.0*

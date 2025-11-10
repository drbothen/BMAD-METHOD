# Obsidian 2nd Brain Workflows

This directory contains workflow definitions that orchestrate multiple agents to execute complex knowledge management routines systematically.

## Available Workflows

### Knowledge Lifecycle Workflow

**File**: `knowledge-lifecycle-workflow.yaml`
**Purpose**: Master continuous lifecycle for note management from capture to review
**Duration**: Continuous (lifecycle-based)
**Agents**: Inbox Triage, Structural Analysis, Semantic Linker, Quality Auditor

### Daily Capture Processing Workflow

**File**: `daily-capture-processing-workflow.yaml`
**Purpose**: Daily routine for processing captured notes and reviewing suggestions
**Duration**: 15-20 minutes (10 min morning + 10 min evening)
**Agents**: Inbox Triage, Semantic Linker, Query Interpreter

### Weekly Review Workflow

**File**: `weekly-review-workflow.yaml`
**Purpose**: Weekly maintenance including audit, link processing, and exploratory queries
**Duration**: 30-45 minutes
**Agents**: Quality Auditor, Semantic Linker, Query Interpreter

## Using Workflows

### Workflow Structure

Each workflow YAML file contains:

- **name**: Unique workflow identifier
- **title**: Human-readable workflow name
- **description**: Purpose and use cases
- **triggers**: What activates the workflow (optional)
- **inputs**: Required inputs from user (optional)
- **agents**: List of agents used in the workflow
- **steps**: Sequential workflow steps with duration, exit criteria, and notes
- **outputs**: Final workflow outputs (optional)

### Execution

Workflows can be executed by:

1. **Manual execution**: Follow step-by-step instructions in each workflow
2. **Agent orchestration**: Use the bmad-orchestrator agent with workflow files
3. **Command triggers**: Use slash commands specified in workflow triggers (if configured)

### Customization

Workflows can be customized by:

- Adjusting duration estimates based on your vault size
- Modifying exit criteria to match your quality standards
- Adding or removing steps based on your needs
- Changing agent command parameters in step notes

## Workflow Decision Guide

**Use Knowledge Lifecycle Workflow when:**

- Setting up your continuous knowledge management system
- You want to understand the full lifecycle of notes in your vault
- Planning long-term knowledge management strategy

**Use Daily Capture Processing when:**

- You have daily note capture habits
- You want to maintain inbox zero
- You need to surface relevant context for your day's work

**Use Weekly Review when:**

- You want to maintain vault health and quality
- Accumulated link suggestions need batch processing
- You want to explore emerging patterns in your knowledge base

## Phase 1 Implementation

Current workflows are Phase 1 implementations focused on:

- **Capture**: Processing inbox items
- **Organization**: Structuring and linking notes
- **Review**: Quality auditing and maintenance

Future phases will add:

- **Phase 2**: Synthesis (MOC construction)
- **Phase 3**: Creation (content brief generation)
- **Phase 4**: Gap Detection (research prioritization)

## Related Documentation

- **Agent Definitions**: `../agents/*.md` - Individual agent capabilities and commands
- **Tasks**: `../tasks/*.md` - Task procedures executed by agents
- **Templates**: `../templates/*.yaml` - Document templates used by agents
- **Checklists**: `../checklists/*.md` - Quality assurance checklists

## Support

For issues or questions about workflows:

- Check agent documentation for command details
- Review task files for step-by-step procedures
- See expansion pack README.md for general guidance

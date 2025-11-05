# BMAD Obsidian 2nd Brain Expansion Pack

Transform Obsidian into a powerful second brain with temporal RAG architecture. This expansion pack combines semantic search with a bi-temporal graph database for knowledge evolution tracking, enabling AI agents to assist with intelligent note management, knowledge synthesis, and content generation.

## Overview

The BMAD Obsidian 2nd Brain expansion pack extends the BMAD framework to work seamlessly with Obsidian vaults. It provides specialized AI agents that help you capture, organize, synthesize, and retrieve knowledge while maintaining temporal context and tracking how your understanding evolves over time.

## Key Capabilities

- **Intelligent Inbox Triage**: Automatically classify, tag, and route incoming notes
- **Smart Auto-Linking**: Discover and create connections between related notes
- **Knowledge Synthesis**: Build Maps of Content (MOCs) and identify knowledge gaps
- **Temporal Tracking**: Track how notes and concepts evolve over time using Neo4j
- **Content Generation**: Transform notes into polished content (blog posts, documentation, etc.)
- **Quality Assurance**: Assess note atomicity, link density, and staleness
- **Semantic Search**: Find relevant notes using local embeddings (no cloud required)

## Prerequisites

Before using this expansion pack, ensure you have:

- **BMAD Core Framework** v4.x+ installed
- **Obsidian** (latest version recommended)
- **Node.js** v18+ and npm
- **Docker** (optional, required for Neo4j temporal graph database)
- **Claude Desktop** or **Cursor/VS Code** with Claude integration

## Quick Start

### 1. Install the Expansion Pack

From your BMAD project directory:

```bash
npx bmad-method install bmad-obsidian-2nd-brain
```

Or manually copy the expansion pack to your project's `.bmad-core/expansion-packs/` directory.

### 2. Install Required Obsidian Plugins

Open Obsidian and install these community plugins:

- **Smart Connections** - For local semantic search
- **MCP Tools** - For Claude AI integration
- **Local REST API** - For external tool access
- **Dataview** - For dynamic note queries
- **Templater** - For note templates

### 3. Configure Your Vault

Update the `config.yaml` file with your vault paths and preferences:

```yaml
vault:
  inbox: inbox # Where new notes arrive
  archive: archive # Long-term storage
  mocs: mocs # Maps of Content
  daily_notes: daily-notes
  periodic_reviews: reviews
```

### 4. (Optional) Set Up Neo4j Temporal Database

For advanced temporal tracking:

```bash
docker run -d \
  --name obsidian-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/changeme \
  neo4j:latest
```

Update `config.yaml` with your Neo4j credentials.

### 5. Start Using Agents

In Claude Desktop or your IDE, activate the agents using the slash prefix:

```
/bmad-2b:inbox-triage     # Triage your inbox
/bmad-2b:auto-link        # Create smart links
/bmad-2b:build-moc        # Generate Maps of Content
```

## Available Agents

### Inbox Triage Agent (📥)

**Status:** ✓ Available
**Command:** `/bmad-2b:inbox-triage-agent`

Automatically classifies and organizes captured content in your Obsidian inbox. Features:

- **6 Content Types:** Quote, Concept, Reference, Reflection, Question, Observation
- **Confidence Scoring:** 0.0-1.0 scale with automatic flagging for low confidence (< 0.7)
- **Metadata Extraction:** Automatically extracts source URLs, authors, timestamps, and context
- **Quality Gates:** Enforces capture quality standards before finalization
- **Bi-Temporal Tracking:** Stores capture events in Neo4j (if enabled) with temporal metadata
- **Batch Processing:** Process multiple captures efficiently with rate limiting
- **Security Hardened:** Input validation, XSS prevention, and injection protection

**Commands:**

- `*help` - Show available commands
- `*capture {source} {content}` - Manual capture with source attribution
- `*process-inbox` - Process all unprocessed inbox items
- `*classify {note_id}` - Reclassify existing inbox note
- `*batch-process` - Process inbox in bulk
- `*yolo` - Toggle auto-processing without confirmation
- `*exit` - Exit agent mode

**Requirements:**

- Obsidian MCP Tools configured
- Obsidian vault with `/inbox` directory
- (Optional) Neo4j for temporal graph tracking

### Future Agents

The following agents are planned for future releases:

- Auto-Linking Agent
- MOC Constructor Agent
- Timeline Constructor Agent
- Content Brief Agent
- Publication Formatter Agent
- Gap Detector Agent
- Quality Auditor Agent

## Available Workflows

Workflows will be populated in future releases:

- Capture & Triage Workflow
- Organization & Linking Workflow
- Synthesis & MOC Creation Workflow
- Content Generation Workflow
- Review & Refinement Workflow

## Configuration

All configuration is managed in `config.yaml`. Key sections:

- **vault**: Directory structure within your Obsidian vault
- **neo4j**: Temporal graph database settings (optional)
- **required_plugins**: Obsidian plugins needed for full functionality
- **mcp_servers**: MCP servers for Claude integration
- **agents**: Agent behavior settings
- **quality_thresholds**: Quality assessment parameters

See `config.yaml` for detailed configuration options and defaults.

## Troubleshooting

### Agents Not Appearing

- Ensure `slashPrefix: bmad-2b` is set in `config.yaml`
- Run `npm run build` from BMAD root to rebuild bundles
- Verify the expansion pack is in `.bmad-core/expansion-packs/`

### Smart Connections Not Working

- Check that the Smart Connections plugin is installed and enabled
- Verify local embeddings are generated (may take time on first run)
- Check Obsidian console for errors (Ctrl+Shift+I / Cmd+Opt+I)

### Neo4j Connection Issues

- Verify Neo4j is running: `docker ps | grep neo4j`
- Check credentials match `config.yaml` settings
- Try connecting via browser: http://localhost:7474
- Set `neo4j.enabled: false` in config to run without temporal tracking

## Documentation

- [BMAD Core Documentation](https://github.com/bmadcode/bmad-method)
- [Obsidian Plugin Docs](https://obsidian.md/plugins)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [MCP Documentation](https://modelcontextprotocol.io/)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow BMAD coding standards
4. Submit a pull request to the `next` branch

See [CONTRIBUTING.md](../../CONTRIBUTING.md) in the BMAD root for detailed guidelines.

## License

This expansion pack is part of the BMAD-METHOD framework and follows the same license.

## Support

- **Discord**: https://discord.gg/gk8jAdXWmj
- **GitHub Issues**: https://github.com/bmadcode/bmad-method/issues
- **Discussions**: https://github.com/bmadcode/bmad-method/discussions

---

**Status**: Infrastructure setup complete. Agents and workflows will be added in subsequent releases.

**Version**: 1.0.0

# BMAD Obsidian 2nd Brain Expansion Pack

Transform Obsidian into a powerful second brain with temporal RAG architecture. This expansion pack combines semantic search with a bi-temporal graph database for knowledge evolution tracking, enabling AI agents to assist with intelligent note management, knowledge synthesis, and content generation.

## Overview

The BMAD Obsidian 2nd Brain expansion pack extends the BMAD framework to work seamlessly with Obsidian vaults. It provides specialized AI agents that help you capture, organize, synthesize, and retrieve knowledge while maintaining temporal context and tracking how your understanding evolves over time.

## Key Capabilities

- **Natural Language Querying**: Execute multi-source queries across your vault with automatic intent classification
- **Intelligent Inbox Triage**: Automatically classify, tag, and route incoming notes
- **Smart Auto-Linking**: Discover and create connections between related notes
- **Atomicity Analysis**: Fragment complex notes into atomic building blocks
- **Temporal Tracking**: Track how notes and concepts evolve over time using Neo4j
- **Contradiction Detection**: Identify and flag conflicting information in your knowledge base
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
/bmad-2b:query-interpreter-agent    # Query your knowledge base
/bmad-2b:inbox-triage-agent         # Triage your inbox
/bmad-2b:structural-analysis-agent  # Analyze and fragment notes
/bmad-2b:semantic-linker-agent      # Create smart links
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

### Query Interpreter Agent (🔍)

**Status:** ✓ Available
**Command:** `/bmad-2b:query-interpreter-agent`

Execute natural language queries across your Obsidian vault and Neo4j knowledge graph. Features:

- **Intent Classification:** Automatically classifies queries into 5 types (factual, temporal, causal, comparative, exploratory) with >85% accuracy
- **Multi-Source Querying:** Searches across Obsidian text, Smart Connections semantic search, and Neo4j graph relationships
- **Smart Result Formatting:** Presents results as narrative, list, comparison table, or timeline based on query intent
- **Contradiction Detection:** Identifies and flags conflicting claims in results (>70% confidence threshold)
- **Source Attribution:** Every result includes complete source attribution with note title, path, excerpt, and timestamp
- **Performance Optimized:** Completes all queries in <3 seconds with detailed performance monitoring
- **Graceful Degradation:** Works with available sources even if some MCP servers are unavailable
- **Security Hardened:** Input validation and injection prevention per security-guidelines.md

**Commands:**

- `*help` - Show available commands
- `*query {question}` - Execute general natural language query (auto-classifies intent)
- `*temporal-query {concept} [date_range]` - Query how concept evolved over time
- `*compare {subject1} vs {subject2}` - Compare two or more concepts side-by-side
- `*surface-related {concept}` - Broad exploratory search for all related notes
- `*yolo` - Toggle auto-execution mode (skip confirmations)
- `*exit` - Exit agent mode

**Query Examples:**

- `*query What is Zettelkasten?` (factual → list format)
- `*temporal-query atomic notes since 2024-01` (temporal → timeline format)
- `*query Why do atomic notes improve recall?` (causal → narrative format)
- `*compare Zettelkasten vs PARA methods` (comparative → table format)
- `*surface-related productivity` (exploratory → categorized list)

**Requirements:**

- Obsidian MCP Tools configured
- Smart Connections plugin installed (for semantic search)
- (Optional) Neo4j Graphiti MCP for temporal and graph queries

**Performance:**
- Query parsing: <200ms
- Source queries: <1 second per source
- Result merging: <500ms
- Total: <3 seconds

### Structural Analysis Agent (🔬)

**Status:** ✓ Available
**Command:** `/bmad-2b:structural-analysis-agent`

Analyzes notes for atomicity and fragments complex notes into atomic building blocks. Features include single-claim validation, evidence testing, and atomic note creation following Zettelkasten principles.

### Semantic Linker Agent (🔗)

**Status:** ✓ Available
**Command:** `/bmad-2b:semantic-linker-agent`

Discovers semantic relationships between notes and creates bidirectional wikilinks with typed relationships. Integrates with Neo4j for temporal graph tracking and relationship strength scoring.

### Quality Auditor Agent (🔍)

**Status:** ✓ Available
**Command:** `/bmad-2b:quality-auditor-agent`

Performs comprehensive vault quality audits across 7 dimensions to detect stale content, broken links, orphaned notes, and quality issues. Generates actionable audit reports with vault health scores. Features:

- **7 Audit Dimensions:** Temporal freshness, external links, citations, orphans, atomicity, duplicates, and metadata completeness
- **Vault Health Score:** 0-100 score with interpretation (Excellent, Good, Fair, Poor, Critical)
- **Security Hardened:** SSRF prevention, rate limiting (5 req/sec), protocol validation, private IP blocking
- **Progressive Mode:** Batch processing for large vaults (10,000+ notes) with checkpointing and resumability
- **Actionable Reports:** Prioritized action items (critical, high, medium, low) with clear remediation steps
- **Performance Optimized:** <10 seconds for most audits on 1000-note vaults
- **Smart Dependencies:** Integrates with STORY-003 atomicity analysis and STORY-004 semantic search
- **Graceful Degradation:** Works without optional dependencies (Neo4j, Smart Connections)

**Commands:**

- `*help` - Show all 13 available commands
- `*audit-full` - Run all audits and generate comprehensive report
- `*audit-freshness [threshold_days]` - Audit temporal freshness (default: 180 days)
- `*audit-links [max_links]` - Validate external links (default: 50, with security hardening)
- `*audit-citations` - Validate source citations completeness and format
- `*audit-orphans` - Detect orphaned notes and suggest linking opportunities
- `*audit-atomicity [sample_size]` - Audit atomicity violations (default: 10% sample or min 20 notes)
- `*audit-duplicates [threshold]` - Detect duplicate content (default: 0.85 similarity)
- `*audit-metadata` - Check metadata completeness across all notes
- `*generate-report` - Generate comprehensive report from cached audit results
- `*progressive [batch_size]` - Toggle progressive audit mode for large vaults (default: 1000 notes/batch)
- `*yolo` - Toggle yolo mode (auto-run without confirmations)
- `*exit` - Exit agent mode

**Audit Dimensions:**

1. **Temporal Freshness:** Detects stale notes (>180 days default), prioritized by importance (incoming link count)
2. **External Links:** Validates HTTP status codes (2xx/3xx/4xx/5xx), detects broken links and redirects
3. **Citations:** Validates source attribution completeness (author, title, URL, date) and format consistency
4. **Orphans:** Detects notes with no incoming/outgoing links, suggests connections via semantic search
5. **Atomicity:** Samples notes (10% or min 20) for multi-concept violations using STORY-003 checklist
6. **Duplicates:** Detects exact (SHA-256), near (>95%), and semantic (85-95%) duplicates
7. **Metadata:** Validates required fields (title, created), recommended fields (tags, type), and formats

**Requirements:**

- Obsidian MCP Tools configured
- (Optional) Smart Connections for semantic duplicate detection and link suggestions
- (Optional) Neo4j for advanced graph metrics

**Performance Benchmarks:**

| Vault Size | Audit Time | Notes |
|------------|------------|-------|
| 100 notes  | ~5 seconds | Single batch |
| 1,000 notes | ~10 seconds | Single batch |
| 10,000 notes | ~2 minutes | Progressive mode (10 batches) |

**Security Features:**
- SSRF prevention: Blocks requests to private IP ranges (127.0.0.0/8, 10.0.0.0/8, 192.168.0.0/16, etc.)
- Rate limiting: Max 5 external link requests per second
- Protocol validation: Only http/https allowed (blocks file://, javascript:, data: protocols)
- Timeout enforcement: 10-second timeout per external request
- SHA-256 hashing: Secure content hashing for duplicate detection

### Future Agents

The following agents are planned for future releases:

- MOC Constructor Agent
- Timeline Constructor Agent
- Content Brief Agent
- Publication Formatter Agent
- Gap Detector Agent

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

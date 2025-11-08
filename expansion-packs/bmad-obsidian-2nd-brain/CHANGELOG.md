# Changelog

All notable changes to the BMAD Obsidian 2nd Brain expansion pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Capture Tasks** (STORY-007) - 4 foundational task files for systematic content capture workflow
  - `capture-classify-content-type.md` - Classify content into 6 semantic types with confidence scoring
    - 8-step classification procedure with pattern matching
    - Confidence algorithm: Starts at 1.0, applies penalties for ambiguity, fallback to "concept" < 0.5
    - Security: XSS prevention, 10MB size limit, ReDoS protection
    - Performance: < 2 seconds per classification
  - `capture-extract-metadata.md` - Extract structured metadata from content and context
    - 10-step extraction procedure with priority fallbacks (source_url, author, title, timestamp, surrounding_context)
    - URL validation: Blocks malicious schemes (javascript:, data:, file:, vbscript:)
    - Domain validation: Blocks localhost/private IPs unless allowed
    - Credential protection: Strips auth tokens from URLs
    - Performance: < 1 second per extraction
  - `capture-create-inbox-note.md` - Create Obsidian inbox notes using template
    - 10-step note creation using inbox-note-tmpl.yaml
    - Filename: YYYY-MM-DD-HHMM-sanitized-title.md with collision handling
    - Obsidian MCP integration: obsidian.create_note
    - Path security: Directory traversal prevention, vault bounds validation
    - YAML frontmatter: Escaped, includes content_type, confidence, source, author, tags
    - Performance: < 3 seconds per note
  - `capture-create-capture-event.md` - Optional Neo4j temporal tracking
    - 10-step episode creation (if neo4j.enabled: true)
    - Graphiti MCP integration: graphiti.add_episode
    - Bi-temporal metadata: valid_time (when captured) + transaction_time (when recorded)
    - Graceful degradation: Returns success=true if Neo4j disabled/unavailable
    - Performance: < 1 second per episode
  - **Test data**: 20 normal samples (6 content types) + 6 edge cases
  - **Ground truth**: expected-results.yaml with classification accuracy targets (>= 85%)
  - **Documentation**: Comprehensive README.md in tests/test-capture-samples/
  - **Security**: XSS prevention, URL validation, path sanitization, size limits (10MB content, 1MB metadata), YAML escaping
  - **End-to-end performance**: < 7 seconds (well under 30s target from epic)
  - Story: STORY-007 (estimated effort: 16 hours, priority: high, phase: 1)

- **Inbox Triage Agent** - Automatically classify and organize captured content
  - 6 content types: Quote, Concept, Reference, Reflection, Question, Observation
  - Confidence scoring (0.0-1.0) with automatic low-confidence flagging (< 0.7)
  - Metadata extraction (source URLs, authors, timestamps, context, tags)
  - Quality gates via capture-quality-checklist.md
  - Bi-temporal tracking in Neo4j (optional, graceful degradation if disabled)
  - Batch processing with rate limiting
  - Security hardening (XSS prevention, parameterized queries, input validation)
  - Commands: *help, *capture, *process-inbox, *classify, *batch-process, *yolo, \*exit
  - Dependencies: 4 capture tasks, 1 template, 1 checklist, 2 data files

- **Quality Auditor Agent** - Comprehensive vault quality audits across 7 dimensions
  - 7 audit dimensions: Temporal freshness, external links, citations, orphans, atomicity, duplicates, metadata
  - Vault health score (0-100) with interpretation (Excellent, Good, Fair, Poor, Critical)
  - Security hardened: SSRF prevention, rate limiting (5 req/sec), protocol validation, private IP blocking
  - Progressive mode: Batch processing for large vaults (10,000+ notes) with checkpointing
  - Actionable reports: Prioritized action items (critical, high, medium, low) with remediation steps
  - Performance optimized: <10 seconds for most audits on 1000-note vaults
  - Smart dependencies: Integrates with STORY-003 atomicity analysis and STORY-004 semantic search
  - Graceful degradation: Works without optional dependencies (Neo4j, Smart Connections)
  - Commands: *help, *audit-full, *audit-freshness, *audit-links, *audit-citations, *audit-orphans, *audit-atomicity, *audit-duplicates, *audit-metadata, *generate-report, *progressive, *yolo, \*exit
  - Dependencies: 8 tasks, 1 template, 1 checklist
  - Story: STORY-006 (estimated effort: 24 hours, priority: critical)

### Planned

- Auto-Linking Agent
- MOC Constructor Agent
- Timeline Constructor Agent
- Content Brief Agent
- Publication Formatter Agent
- Gap Detector Agent

## [1.0.0] - 2025-11-04

### Added

- Initial infrastructure setup
- Expansion pack directory structure (agents/, agent-teams/, tasks/, templates/, checklists/, workflows/, data/, docs/)
- Config.yaml with vault and Neo4j settings
- README.md with quickstart guide
- Required Obsidian plugins configuration (Smart Connections, MCP Tools, Local REST API, Dataview, Templater)
- MCP servers configuration (obsidian-mcp, graphiti-mcp, perplexity, context7)
- Quality thresholds configuration
- Agent behavior settings (yolo_mode_default, auto_link_threshold)

### Infrastructure

- Flat directory structure for tasks/ (per BMAD framework requirement)
- Slash prefix: `bmad-2b`
- BMAD build system integration
- Version tracking via CHANGELOG.md

[Unreleased]: https://github.com/bmadcode/bmad-method/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/bmadcode/bmad-method/releases/tag/v1.0.0

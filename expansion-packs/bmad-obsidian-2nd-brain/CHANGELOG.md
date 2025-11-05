# Changelog

All notable changes to the BMAD Obsidian 2nd Brain expansion pack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Inbox Triage Agent
- Auto-Linking Agent
- MOC Constructor Agent
- Timeline Constructor Agent
- Content Brief Agent
- Publication Formatter Agent
- Gap Detector Agent
- Quality Auditor Agent

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

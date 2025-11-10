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
- **Obsidian** v1.7.7+ (latest version recommended)
- **Claude Desktop** with MCP support
- **Node.js** v18+ and npm (for testing and utilities)
- **Docker** (optional, required for Neo4j temporal graph database)

**Required Obsidian Plugins:**
- Local REST API (for API access)
- MCP Tools (for Claude integration)
- Smart Connections (for semantic search)

📖 **See [Plugin Installation Guide](./docs/installation/obsidian-plugins.md) for detailed setup instructions.**

## Quick Start

### 1. Install the Expansion Pack

From your BMAD project directory:

```bash
npx bmad-method install bmad-obsidian-2nd-brain
```

Or manually copy the expansion pack to your project's `.bmad-core/expansion-packs/` directory.

### 2. Install Required Obsidian Plugins

Three essential plugins must be installed and configured:

1. **Local REST API** - Provides HTTP API access to your vault
2. **MCP Tools** - Bridges Claude Desktop to Obsidian
3. **Smart Connections** - Enables semantic search with local embeddings

**Optional (but recommended):**
- **Dataview** - For dynamic note queries
- **Templater** - For note templates

📖 **Complete Installation Guide**: [docs/installation/obsidian-plugins.md](./docs/installation/obsidian-plugins.md)
- Step-by-step installation for all three plugins
- Configuration instructions (API keys, ports, etc.)
- Troubleshooting common issues

📖 **MCP Server Setup**: [docs/installation/mcp-server-setup.md](./docs/installation/mcp-server-setup.md)
- Configure Claude Desktop for MCP integration
- Set up environment variables
- Verify connection

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

| Vault Size   | Audit Time  | Notes                         |
| ------------ | ----------- | ----------------------------- |
| 100 notes    | ~5 seconds  | Single batch                  |
| 1,000 notes  | ~10 seconds | Single batch                  |
| 10,000 notes | ~2 minutes  | Progressive mode (10 batches) |

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

## Capture Tasks

The capture workflow consists of 4 foundational tasks that power the Inbox Triage Agent. These tasks can be used independently or as part of the automated capture workflow.

### 1. capture-classify-content-type.md

**Purpose:** Classify captured content into one of 6 semantic types using pattern matching and contextual analysis

**Inputs:**

- `raw_content` (String): Captured text to classify
- `source_context` (Object, optional): URL, timestamp, and other context

**Outputs:**

- `content_type` (String): One of 6 types (quote, concept, reference, reflection, question, observation)
- `confidence` (Float): 0.0-1.0 confidence score
- `reasoning` (String): Explanation of classification
- `matched_patterns` (Array<String>): Patterns that matched

**Content Types:**

1. **Quote** - Quoted text with source attribution (e.g., "According to Cal Newport...")
2. **Concept** - Definition or explanation of an idea (e.g., "Atomic notes are single-idea notes...")
3. **Reference** - Link to external resource (e.g., "See https://example.com...")
4. **Reflection** - Personal thoughts and opinions (e.g., "I think this approach works because...")
5. **Question** - Investigative inquiry (e.g., "Why does spaced repetition improve retention?")
6. **Observation** - Factual statement or data (e.g., "I noticed my notes cluster around...")

**Features:**

- 8-step classification procedure with pattern matching
- Confidence scoring algorithm (starts at 1.0, applies penalties for ambiguity)
- Fallback to "concept" if confidence < 0.5
- Security: XSS prevention, size limits (10MB max), ReDoS protection
- Performance: < 2 seconds per classification

### 2. capture-extract-metadata.md

**Purpose:** Extract structured metadata from captured content and source context

**Inputs:**

- `raw_content` (String): Captured text
- `source_context` (Object, optional): URL, author, title, timestamp, surrounding context

**Outputs:**

- `source_url` (String): Validated URL or "Unknown"
- `author` (String): Extracted author or "Unknown"
- `title` (String): Extracted or auto-generated title
- `timestamp` (String): ISO8601 timestamp (UTC)
- `surrounding_context` (String): Context for highlights (optional)

**Features:**

- 10-step extraction procedure with priority fallbacks
- URL validation: Blocks malicious schemes (javascript:, data:, file:, vbscript:)
- Domain validation: Blocks localhost/private IPs unless explicitly allowed
- Credential protection: Strips auth tokens from URLs
- Graceful degradation: Uses defaults when metadata unavailable
- Security: YAML escaping, HTML sanitization, size limits
- Performance: < 1 second per extraction

### 3. capture-create-inbox-note.md

**Purpose:** Create inbox note in Obsidian vault using classified content and extracted metadata

**Inputs:**

- `classified_content` (Object): Classification result with content_type, confidence, raw_content
- `metadata` (Object): Extracted metadata (source_url, author, title, timestamp, context)
- `vault_path` (String): Obsidian vault root path

**Outputs:**

- `inbox_note_path` (String): Full path to created note
- `creation_timestamp` (String): ISO8601 timestamp
- `success` (Boolean): Creation status
- `error` (String): Error message if failed

**Features:**

- 10-step note creation procedure using inbox-note-tmpl.yaml template
- Filename generation: `YYYY-MM-DD-HHMM-sanitized-title.md`
- Collision handling: Appends random suffix if file exists
- Obsidian MCP integration: Uses `obsidian.create_note` tool
- Path security: Directory traversal prevention, vault bounds validation
- YAML frontmatter: Properly escaped, includes content_type, confidence, source, author, tags
- Performance: < 3 seconds per note creation

**Example note structure:**

```markdown
---
status: unprocessed
content_type: concept
confidence: 0.85
source: https://example.com/article
author: Cal Newport
captured: 2025-11-06T10:30:00Z
tags: []
flagged_for_review: false
---

# Concept: Deep Work Principles

[Captured content here]

## Context

[Surrounding context if available]

## Processing Notes

_To be filled by triage agent or user during processing_

## Next Actions

- [ ] _To be filled by user or organization agent_
```

### 4. capture-create-capture-event.md (OPTIONAL)

**Purpose:** Create temporal CaptureEvent node in Neo4j graph database for evolution tracking (requires Neo4j enabled)

**Inputs:**

- `inbox_note_path` (String): Path to created inbox note
- `metadata` (Object): Extracted metadata
- `content_type` (String): Classification result
- `config` (Object): Neo4j configuration

**Outputs:**

- `capture_event_id` (String): Episode ID from Neo4j/Graphiti, or null if disabled
- `success` (Boolean): Always true (graceful degradation)
- `skipped` (Boolean): True if Neo4j disabled or error occurred
- `error` (String): Error message if applicable

**Features:**

- 10-step episode creation procedure (if Neo4j enabled)
- Graphiti MCP integration: Uses `graphiti.add_episode` tool
- Bi-temporal metadata: Tracks both valid_time (when captured) and transaction_time (when recorded)
- Graceful degradation: Returns success=true even if Neo4j unavailable
- Config check: Reads `neo4j.enabled` from config.yaml, skips if false
- Security: No Cypher injection risk (uses MCP abstraction)
- Performance: < 1 second per episode creation

**Bi-temporal tracking use cases:**

- "Show me what I captured last week" (valid_time query)
- "Show me what was added to the graph today" (transaction_time query)
- "How has my understanding of X evolved over time?" (temporal evolution query)

**Graceful degradation scenarios:**

- Neo4j disabled in config → Skip with info message
- Graphiti MCP unavailable → Skip with warning, operate in Obsidian-only mode
- Connection failed → Skip with warning, note saved to Obsidian successfully

### Using Capture Tasks

**Manual execution:**

```bash
# Activate Inbox Triage Agent
/bmad-2b:inbox-triage-agent

# Capture content (runs all 4 tasks sequentially)
*capture https://example.com "Your captured content here"
```

**Automated workflow:**

1. Classify content type (Task 1) → confidence score
2. Extract metadata (Task 2) → source, author, title, timestamp
3. Create inbox note (Task 3) → Obsidian note with YAML frontmatter
4. Create capture event (Task 4, optional) → Neo4j episode with temporal metadata

**Performance:**

- Classification: < 2 seconds
- Metadata extraction: < 1 second
- Inbox note creation: < 3 seconds
- Capture event: < 1 second
- **Total end-to-end: < 7 seconds** (well under 30s target)

**Security features:**

- XSS prevention: Script tags stripped/escaped
- URL validation: Malicious schemes blocked
- Path sanitization: Directory traversal prevented
- Size limits: 10MB content max, 1MB metadata max
- YAML escaping: Special characters properly handled

**Test data:**

- 20 sample captures covering all 6 content types
- 6 edge case samples (empty, short, Unicode, XSS, malformed URLs, paths with spaces)
- Ground truth validation in `tests/test-capture-samples/expected-results.yaml`
- Target classification accuracy: >= 85% (17 out of 20 correct)

## Review Tasks

The review workflow consists of 3 quality audit tasks that power the Quality Auditor Agent. These tasks analyze vault health across multiple dimensions and generate actionable reports.

### 1. review-audit-temporal-freshness.md

**Purpose:** Audit vault notes for temporal freshness by identifying stale notes that haven't been updated within a configured threshold, prioritized by importance.

**Inputs:**

- `vault_path` (String): Absolute path to Obsidian vault
- `freshness_threshold_days` (Integer, default: 180): Days after which note is considered stale

**Outputs:**

- `stale_notes` (Array<Object>): Stale notes with priority scores
  - `path`, `last_updated`, `days_stale`, `staleness_score`, `importance`, `priority_score`, `severity`
- `metrics` (Object): Aggregated statistics
  - `total_notes`, `stale_notes`, `stale_ratio`, `avg_staleness`, `health_impact`
- `performance_stats` (Object): Execution timing
  - `query_time`, `processing_time`, `total_time`

**Features:**

- **12-step sequential procedure** for comprehensive freshness analysis
- **Priority scoring:** Combines staleness_score × importance (incoming links + domain critical bonus)
- **Severity classification:** critical (>365 days), high (180-365), medium (90-180)
- **Security:** Path traversal prevention, input validation, size limits (100k notes max)
- **Performance:** <10s for 1000 notes, <60s for 10,000 notes
- **Progressive mode:** Batch processing for vaults exceeding 100,000 notes

**Algorithm:**

```python
staleness_score = days_stale / threshold_days
importance = incoming_link_count + (is_domain_critical ? 10 : 0)
priority_score = staleness_score × importance  # Higher = more urgent to update
```

**Example usage:**

```bash
*audit-freshness 180  # Default 180-day threshold
```

**Example output:**

```json
{
  "stale_notes": [
    {
      "path": "concepts/core-methodology.md",
      "days_stale": 236,
      "staleness_score": 1.31,
      "importance": 15,
      "priority_score": 19.65,
      "severity": "high"
    }
  ],
  "metrics": {
    "total_notes": 1000,
    "stale_notes": 200,
    "stale_ratio": 0.2,
    "avg_staleness": 245.5,
    "health_impact": "medium"
  }
}
```

### 2. review-validate-external-links.md

**Purpose:** Validate external links in notes by checking HTTP status codes, identifying broken links (4xx), redirects (3xx), and timeouts with comprehensive security hardening.

**Inputs:**

- `note_paths` (Array<String>, optional): Specific notes to check (default: all notes)
- `max_links` (Integer, default: 50): Maximum links to validate per execution
- `rate_limit` (Integer, default: 5): Maximum requests per second (1-10 allowed)

**Outputs:**

- `validation_results` (Array<Object>): Complete validation results for all tested links
  - `note_path`, `url`, `status_code`, `classification`, `response_time`, `reason`
- `broken_links` (Array<Object>): Links returning 4xx/5xx status codes
- `redirects` (Array<Object>): Links returning 3xx with Location header
- `timeouts` (Array<Object>): Links exceeding 5-second timeout
- `metrics` (Object): Aggregated statistics
  - `total_links`, `broken_count`, `redirect_count`, `timeout_count`, `success_count`, `success_rate`

**Features:**

- **15-step sequential procedure** with comprehensive security validation
- **SSRF prevention:** Blocks private IPs (127.0.0.0/8, 10.0.0.0/8, 192.168.0.0/16, 172.16.0.0/12, localhost)
- **Protocol validation:** Only http/https allowed (blocks javascript:, data:, file://, vbscript:)
- **Credential protection:** Strips username:password from URLs before testing/logging
- **Rate limiting:** Max 5 req/sec with 1-second batch delays
- **Timeout enforcement:** 5-second max per request
- **Performance:** <15s for 50 links with rate limiting

**URL Extraction:**

- Markdown links: `[text](url)`
- Plain URLs: `https?://...`

**Classification:**

- **2xx:** Success
- **3xx:** Redirect (with Location header)
- **4xx/5xx:** Broken
- **Timeout:** >5 seconds
- **Blocked:** Private IP or invalid protocol

**Example usage:**

```bash
*audit-links 50  # Validate up to 50 links
```

**Example output:**

```json
{
  "broken_links": [
    {
      "note_path": "research/web-sources.md",
      "url": "https://example.com/missing",
      "status_code": 404,
      "classification": "broken"
    }
  ],
  "metrics": {
    "total_links": 50,
    "broken_count": 20,
    "redirect_count": 5,
    "timeout_count": 2,
    "success_count": 23,
    "success_rate": 0.46
  }
}
```

**Security features:**

- Private IP blocking prevents internal network access
- Protocol filtering prevents XSS and file access exploits
- Credential stripping protects sensitive auth tokens
- Rate limiting prevents DoS accusations

### 3. review-generate-audit-report.md

**Purpose:** Generate comprehensive vault health audit report by aggregating results from multiple audit dimensions, calculating weighted health score, and creating prioritized action items.

**Inputs:**

- `audit_results` (Object): Combined audit results from all dimensions
  - `freshness` (Object, required): Temporal freshness results
  - `links` (Object, required): Link validation results
  - `citations`, `orphans`, `atomicity`, `duplicates`, `metadata` (Object, optional): Additional dimensions
- `vault_path` (String): Absolute path to Obsidian vault
- `output_path` (String, optional): Custom report location (default: `reports/audit-YYYY-MM-DD-HHMM.md`)

**Outputs:**

- `report_note_path` (String): Path to created audit report in vault
- `health_score` (Float): Overall vault health (0-100)
- `health_interpretation` (String): Excellent (90-100), Good (75-89), Fair (60-74), Poor (40-59), Critical (<40)
- `action_items` (Array<Object>): Prioritized recommendations
  - `priority` (critical/high/medium/low), `category`, `action`, `details`
- `success` (Boolean): Report generation status

**Features:**

- **14-step sequential procedure** for comprehensive report generation
- **Weighted health score calculation:**
  - Freshness: 20% weight
  - Links: 15% weight
  - Orphans: 15% weight
  - Atomicity: 20% weight
  - Duplicates: 10% weight
  - Citations: 10% weight
  - Metadata: 10% weight
- **Smart action prioritization:** Based on health impact and issue severity
- **Template-based formatting:** Uses `audit-report-tmpl.yaml`
- **Security:** Path validation, YAML escaping, size limits (1MB max)
- **Performance:** <5s for report generation and aggregation

**Health Score Formula:**

```python
health_score = sum(dimension_score × weight for each dimension)

# Example:
# Freshness: (1 - 0.15) × 20 = 17.0
# Links: (1 - 0.22) × 15 = 11.7
# Total: 68.5/100 (Fair)
```

**Example usage:**

```bash
*generate-report  # Generate report from cached audit results
```

**Example output:**

```json
{
  "report_note_path": "reports/audit-2025-11-06-1430.md",
  "health_score": 73.2,
  "health_interpretation": "Fair",
  "action_items": [
    {
      "priority": "high",
      "category": "links",
      "action": "Fix 34 broken external links",
      "details": "22% of external links are broken (404/403 errors)"
    },
    {
      "priority": "high",
      "category": "freshness",
      "action": "Update 25 high-priority stale notes",
      "details": "Critical knowledge hubs haven't been updated in >6 months"
    }
  ]
}
```

**Generated Report Structure:**

```markdown
# Vault Audit Report

_Generated: 2025-11-06T14:30:00Z_

## Executive Summary

Vault health: 73.2/100 (Fair). Analyzed 1,245 notes...

## Health Score: 73.2/100 (Fair)

| Dimension | Score | Weight | Contribution |
| --------- | ----- | ------ | ------------ |
| Freshness | 85.0  | 20%    | 17.0         |
| Links     | 78.2  | 15%    | 11.7         |

...

## Freshness Issues (Top 20)

[Prioritized table of stale notes]

## Link Validation Issues

### Broken Links (34 total)

### Redirects (8 total)

...

## Action Items

1. [HIGH] Fix 34 broken external links
2. [HIGH] Update 25 high-priority stale notes
   ...
```

### Using Review Tasks

**Manual execution via Quality Auditor Agent:**

```bash
# Activate agent
/bmad-2b:quality-auditor-agent

# Run individual audits
*audit-freshness 180       # Task 1: Temporal freshness
*audit-links 50            # Task 2: External links
*generate-report           # Task 3: Comprehensive report

# Or run full audit workflow
*audit-full                # Runs all tasks sequentially
```

**Automated workflow:**

1. Audit temporal freshness (Task 1) → stale notes with priority scores
2. Validate external links (Task 2) → broken/redirect/timeout classification
3. Generate comprehensive report (Task 3) → health score + action items

**Performance:**

- Temporal freshness audit: <10s for 1000 notes
- Link validation: <15s for 50 links (with rate limiting)
- Report generation: <5s for aggregation
- **Total full audit: <30s for typical vault**

**Security features:**

- SSRF prevention: Private IP blocking in link validation
- Protocol validation: Only http/https allowed
- Path traversal prevention: All file operations validated
- Rate limiting: Prevents abuse of external services
- Credential protection: Strips auth from URLs before logging
- Size limits: Prevents resource exhaustion

**Test vault:**

- Sample test vault: `tests/test-vaults/audit-test-vault/`
- Test data specification: 1000 notes (200 stale, 50 with links, 10 orphans)
- Performance benchmarks and validation criteria documented in test vault README

## Templates

The expansion pack provides standardized YAML templates for creating structured notes following Zettelkasten and PKM best practices. All templates comply with the BMAD document template specification (`common/utils/bmad-doc-template.md`) and support variable substitution using `{{variable_name}}` syntax.

### Phase 1 Templates (Current Release)

#### inbox-note-tmpl.yaml

**Purpose:** Standardized structure for captured content in Obsidian inbox

**Status:** ✅ Phase 1 Complete

**Used By:** Inbox Triage Agent (`create-inbox-note` task)

**Key Features:**

- 6 content type classifications (quote, concept, reference, reflection, question, observation)
- Processing status tracking (inbox, reviewed, processing, processed)
- Confidence scoring (0.0-1.0)
- Source attribution with author and timestamps
- Sections: Content, Context, Initial Thoughts, Processing Notes, Next Actions

**Frontmatter Fields:**

```yaml
type: [inbox, capture, highlight]
captured: ISO8601 timestamp
source: URL or reference
author: Author name
content_type: [quote, concept, reference, reflection, question, observation]
status: [inbox, reviewed, processing, processed]
confidence: 0.0-1.0
```

#### atomic-note-tmpl.yaml

**Purpose:** Template for atomic notes containing single knowledge building blocks

**Status:** ✅ Phase 1 Complete

**Used By:** Structural Analysis Agent (`fragment-note` task)

**Key Features:**

- Atomic knowledge unit (single complete idea per note)
- 6 building block types (concept, argument, model, question, claim, phenomenon)
- Note maturity tracking (working, refined, established)
- Confidence levels (high, medium, low)
- MOC relationship tracking
- Required source attribution

**Frontmatter Fields:**

```yaml
type: [atomic_note, evergreen]
created: ISO8601 timestamp
updated: ISO8601 timestamp
atomized_from: Link to original note if fragmented
status: [working, refined, established]
confidence: [high, medium, low]
building_block_type: [concept, argument, model, question, claim, phenomenon]
related_mocs: [List of MOC links]
```

**Sections:**

- Core Claim: Single main idea (1-2 sentences)
- Evidence & Context: Supporting details and examples
- Related Concepts: Bidirectional links to adjacent notes
- Source & Attribution: Original source reference

#### moc-tmpl.yaml

**Purpose:** Map of Content structure for knowledge domain navigation

**Status:** ✅ Phase 1 Basic (Phase 2 enhancements planned)

**Used By:** MOC Constructor Agent (manual creation in Phase 1)

**Key Features:**

- Domain-specific knowledge organization
- Maturity level tracking (nascent, developing, established, comprehensive)
- Core concepts list with definitions
- Dynamic knowledge branches
- Optional Dataview queries for automatic note surfacing

**Frontmatter Fields:**

```yaml
type: [map_of_content, MOC]
created: ISO8601 timestamp
updated: ISO8601 timestamp
domain: Topic domain covered
status: [active, archived]
last_review: Last comprehensive review date
maturity_level: [nascent, developing, established, comprehensive]
```

**Sections:**

- Overview: 2-3 sentence domain synthesis
- Core Concepts: Foundational ideas with links
- Knowledge Branches: Dynamic subsections per branch
- Emerging Questions: Open questions for research (optional)
- Dynamic Content: Dataview queries (optional)
- Last Updated: Maintenance history

**Phase 2 Enhancements Planned:**

- Advanced Dataview query templates
- Automatic concept clustering
- MOC relationship graphs
- Suggested knowledge branch templates

#### query-result-tmpl.yaml

**Purpose:** Structured template for presenting query results

**Status:** ✅ Phase 1 Complete

**Used By:** Query Interpreter Agent (`merge-results` task)

**Key Features:**

- Multiple format support (narrative, list, table, timeline) based on query intent
- Contradiction detection and flagging
- Source attribution with relevance scores
- Performance metadata
- Suggested next steps

**Variables:**

```yaml
query: Original user query
query_intent: [factual, temporal, causal, comparative, exploratory]
confidence: Classification confidence (0.0-1.0)
result_format: [narrative, list, table, timeline]
results: Array of result objects
contradictions: Detected contradictions (optional)
sources_available: Successfully queried sources
sources_failed: Failed sources (optional)
```

**Sections:**

- Query Summary: Query metadata and performance
- Results: Format-specific presentation (narrative/list/table/timeline)
- Contradictions: Flagged conflicts (if detected)
- Metadata: Collapsible query details
- Suggested Next Steps: Follow-up recommendations

#### audit-report-tmpl.yaml

**Purpose:** Comprehensive vault quality audit results

**Status:** ✅ Phase 1 Complete (Phase 2 enhancements planned)

**Used By:** Quality Auditor Agent (`generate-audit-report` task)

**Key Features:**

- Vault health score (0-100) with interpretation
- 7 audit dimensions (freshness, links, citations, orphans, atomicity, duplicates, metadata)
- Prioritized action items (critical, high, medium, low)
- Weighted health score calculation
- Performance metrics

**Frontmatter Fields:**

```yaml
audit_date: ISO8601 timestamp
vault_health_score: 0-100
total_notes: Note count
critical_issues: Critical issue count
audit_scope: Domain/tag filter or "entire vault"
```

**Sections:**

- Executive Summary: High-level findings
- Temporal Freshness: Stale notes requiring updates
- Link Validation: Broken/redirect/timeout links
- Citation Quality: Source attribution issues
- Orphaned Notes: Disconnected notes
- Atomicity Violations: Multi-concept notes (from sample)
- Duplicate Content: Similar/identical notes
- Metadata Completeness: Missing/incomplete metadata
- Prioritized Action Items: Ranked remediation steps
- Vault Health Metrics: Score breakdown

**Phase 2 Enhancements Planned:**

- Advanced graph metrics (betweenness centrality, clustering coefficient)
- Predictive staleness modeling
- Automated link suggestion quality scoring
- Content quality sentiment analysis

### Template Usage

**Via Agents (Recommended):**

```bash
# Templates are automatically used by agents
/bmad-2b:inbox-triage-agent
*capture https://example.com "Your content"  # Uses inbox-note-tmpl.yaml

/bmad-2b:structural-analysis-agent
*fragment /path/to/note.md                   # Uses atomic-note-tmpl.yaml

/bmad-2b:quality-auditor-agent
*audit-full                                   # Uses audit-report-tmpl.yaml
```

**Direct Task Execution:**

```bash
# Reference templates in task parameters
*create-doc --template=atomic-note-tmpl.yaml
```

### Template Development

**Location:** `expansion-packs/bmad-obsidian-2nd-brain/templates/`

**Test Samples:** `tests/test-vaults/phase1-templates/`

**Validation:**

```bash
# Validate YAML syntax
npm run validate

# Test samples available:
# - sample-inbox-note.md
# - sample-atomic-note.md
# - sample-moc.md
# - sample-query-result.md
# - sample-audit-report.md
```

### Phase 1 vs Phase 2 Distinctions

**Phase 1 (Current):**

- All templates functional for core workflows
- Basic/MVP feature sets
- Proven patterns from Zettelkasten and PKM
- Extensible for Phase 2 enhancements

**Phase 2 (Planned):**

- moc-tmpl.yaml: Advanced query templates, automatic clustering, relationship graphs
- audit-report-tmpl.yaml: Graph analytics, predictive modeling, quality scoring

## Available Workflows

Workflow files orchestrate multiple agents to execute complex knowledge management routines systematically. All workflows are located in `workflows/` directory.

### Knowledge Lifecycle Workflow

**File:** `knowledge-lifecycle-workflow.yaml`
**Purpose:** Master continuous lifecycle for note management from capture to review
**Duration:** Continuous (lifecycle-based, not time-boxed)
**Agents:** Inbox Triage, Structural Analysis, Semantic Linker, Quality Auditor

**Phases:**

1. **Phase 1: Capture** - Inbox triage and categorization using Inbox Triage Agent
2. **Phase 2: Organization** - Structure analysis and semantic linking
3. **Phase 3: Periodic Review** - Quality auditing and vault maintenance

**When to use:**

- Setting up your continuous knowledge management system
- Understanding the full lifecycle of notes in your vault
- Planning long-term knowledge management strategy

**Execution:** This is a lifecycle framework rather than a time-boxed workflow. Execute phases based on triggers (daily for capture, weekly for organization and review).

### Daily Capture Processing Workflow

**File:** `daily-capture-processing-workflow.yaml`
**Purpose:** Daily routine for processing captured notes and reviewing suggestions
**Duration:** 15-20 minutes (10 min morning + 10 min evening)
**Agents:** Inbox Triage, Semantic Linker, Query Interpreter, Quality Auditor

**Morning Routine (10 min):**

1. Process overnight captures (5 min)
2. Review link suggestions (5 min)
3. Surface relevant notes for the day (5 min)

**Evening Routine (10 min):**

1. Process day's captures (5 min)
2. Quick freshness check on critical notes (5 min)

**When to use:**

- Daily note capture habits
- Maintaining inbox zero
- Surfacing relevant context for your day's work

**Execution:** Run twice daily at consistent times (e.g., 9am and 6pm). Input parameter: `time_of_day` (morning or evening).

### Weekly Review Workflow

**File:** `weekly-review-workflow.yaml`
**Purpose:** Weekly maintenance including audit, link processing, and exploratory queries
**Duration:** 30-45 minutes
**Agents:** Quality Auditor, Semantic Linker, Query Interpreter

**Steps:**

1. **Weekly Quality Audit (15 min)** - Comprehensive vault health check
   - Check for broken links (wikilinks and external URLs)
   - Identify stale notes (domain-critical only, >90 days)
   - Report orphaned notes (no incoming links)

2. **Batch Link Processing (15 min)** - Clear suggestion queue
   - Review accumulated suggestions (typically 50-100 weekly)
   - Accept/reject in batch mode for efficiency
   - Focus on high-confidence suggestions

3. **Exploratory Queries (15 min)** - Discover patterns and insights
   - Query: "What emerged this week?"
   - Query: "What domains saw growth?"
   - Custom queries based on active projects

**When to use:**

- Weekly vault maintenance and quality assurance
- Accumulated link suggestions need batch processing
- Exploring emerging patterns in your knowledge base

**Execution:** Run weekly at consistent time (recommended: Sunday evening). Requires uninterrupted 30-45 minute block.

### Workflow Customization

Workflows can be customized by:

- Adjusting duration estimates based on vault size
- Modifying exit criteria to match your quality standards
- Adding or removing steps based on your needs
- Changing agent command parameters in workflow files

See `workflows/README.md` for detailed usage instructions and customization options.

### Future Workflows (Phase 2+)

Planned for future releases:

- Synthesis & MOC Creation Workflow
- Content Generation Workflow
- Gap Detection & Research Prioritization Workflow

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

### MCP Connection Issues

**Quick Checks:**
- Verify Obsidian is running with Local REST API plugin enabled
- Check MCP Tools plugin is installed in Obsidian
- Confirm Claude Desktop is configured with MCP server
- Run connection test: `node tests/integration/obsidian-mcp-connection-test.js`

📖 **Comprehensive Troubleshooting Guides:**
- [MCP Server Setup Guide](./docs/installation/mcp-server-setup.md#troubleshooting) - MCP configuration issues
- [Plugin Installation Guide](./docs/installation/obsidian-plugins.md#troubleshooting) - Plugin setup problems
- [Error Handling Patterns](./docs/error-handling-patterns.md) - Common error scenarios and solutions
- [Connection Testing](./tests/integration/README.md) - Automated connection diagnostics

**Common Issues:**
- **API Key Invalid**: Copy fresh API key from Local REST API settings, update MCP Tools config
- **Connection Refused**: Ensure Obsidian is running, Local REST API enabled on port 27123
- **MCP Server Not Found**: Re-run "Install Server" in MCP Tools plugin settings
- **Authentication Failed**: Verify API key in environment variables or MCP config

### Agents Not Appearing

- Ensure `slashPrefix: bmad-2b` is set in `config.yaml`
- Run `npm run build` from BMAD root to rebuild bundles
- Verify the expansion pack is in `.bmad-core/expansion-packs/`
- Check Claude Desktop recognizes MCP server: Ask "What MCP servers are available?"

### Smart Connections Not Working

- Check that the Smart Connections plugin is installed and enabled
- Verify local embeddings are generated (may take time on first run - check progress in plugin settings)
- Ensure vault indexing is complete (Settings → Smart Connections → Index Status)
- Check Obsidian console for errors (Ctrl+Shift+I / Cmd+Opt+I)
- Try rebuilding index: Settings → Smart Connections → Rebuild Index

📖 **See**: [Plugin Installation Guide - Smart Connections Troubleshooting](./docs/installation/obsidian-plugins.md#troubleshooting)

### Neo4j Connection Issues

- Verify Neo4j is running: `docker ps | grep neo4j`
- Check credentials match `config.yaml` settings
- Try connecting via browser: http://localhost:7474
- Set `neo4j.enabled: false` in config to run without temporal tracking

## Documentation

### Expansion Pack Documentation

- [Plugin Installation Guide](./docs/installation/obsidian-plugins.md) - Complete setup for Local REST API, MCP Tools, and Smart Connections
- [MCP Server Configuration](./docs/installation/mcp-server-setup.md) - Configure Claude Desktop for MCP integration
- [MCP Tools Reference](./docs/mcp-tools-reference.md) - Complete API reference for all MCP tools
- [Error Handling Patterns](./docs/error-handling-patterns.md) - Common errors and solutions
- [Connection Testing](./tests/integration/README.md) - Automated connection diagnostics

### External Documentation

- [BMAD Core Documentation](https://github.com/bmadcode/bmad-method)
- [Obsidian Plugin Docs](https://obsidian.md/plugins)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

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

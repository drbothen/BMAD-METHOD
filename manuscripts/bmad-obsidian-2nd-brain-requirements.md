# BMAD Expansion Pack Requirements: Obsidian 2nd Brain with Temporal RAG

**Version:** 1.1 (Enhanced with Research Coordinator v2.0)
**Date:** 2025-11-04
**Last Updated:** 2025-11-04
**Author:** Mary (Business Analyst)
**Project:** BMAD-METHOD Expansion Pack
**Expansion Pack Name:** `bmad-obsidian-2nd-brain`
**Related Documents:** `bmad-obsidian-2nd-brain-research-enhancement.md`

---

## Executive Summary

This requirements document specifies a comprehensive BMAD expansion pack for managing personal knowledge using Obsidian with a multi-modal temporal RAG architecture. The system combines Obsidian's semantic search capabilities (via Smart Connections) with Neo4j's temporal graph database (via Graphiti MCP) to create a "second brain" that not only stores knowledge but actively reasons about how understanding evolves over time.

### Key Innovation

Unlike traditional knowledge management systems that treat notes as static artifacts, this expansion pack implements **temporal awareness** throughout the knowledge lifecycle. Every capture, connection, synthesis, and evolution is tracked with bi-temporal metadata, enabling queries like:

- "How has my understanding of X evolved?"
- "What influenced my decision on Y yesterday?"
- "When did these two concepts first connect?"
- "What contradictions exist in my knowledge base?"

### Target Users

- Knowledge workers building personal knowledge management systems
- Researchers tracking evolving understanding across years
- Writers synthesizing ideas from diverse sources
- Consultants maintaining client knowledge and decision histories
- Academics building Zettelkasten or PARA-based systems
- Productivity enthusiasts implementing "Building a Second Brain" methodology

### System Scope

**In Scope:**

- 10 specialized AI agents for knowledge capture, organization, synthesis, retrieval, creation, review, temporal analysis, cross-linking, gap identification, and publishing
- 25+ tasks covering complete knowledge management workflows
- 15+ templates for notes, MOCs, reports, and publications
- 20+ checklists for quality assurance
- 8+ workflows orchestrating multi-agent collaboration
- Integration with Obsidian MCP Tools, Smart Connections, Neo4j Graphiti MCP
- Support for Zettelkasten, PARA, LYT, Johnny Decimal, and Progressive Summarization methodologies

**Out of Scope:**

- Obsidian plugin development (uses existing community plugins)
- Neo4j database administration beyond basic setup
- Custom embedding model training
- Multi-user collaboration features (single-user focus)
- Real-time synchronization across devices (relies on Obsidian Sync or git)

### Related Documents

> **🔬 Research Enhancement Specification**
>
> The optional Research Coordinator Agent (Agent 11) has been significantly enhanced with adaptive capabilities. A separate enhancement document provides detailed specifications:
>
> **Document:** `bmad-obsidian-2nd-brain-research-enhancement.md`
>
> **Enhancement Highlights:**
>
> - Automatic MCP tool detection (Perplexity, WebSearch, Context7, custom servers)
> - Adaptive query generation optimized for detected tools
> - Multi-tool orchestration (parallel/sequential/hybrid execution)
> - Evidence-based source credibility scoring (0-100 rubric)
> - Multi-source synthesis with conflict resolution
> - Complete provenance tracking in Neo4j
> - Graceful fallback to manual workflows
>
> **When to Consult Enhancement Document:**
>
> - Implementing Phase 5 (Optional Research Integration)
> - Configuring research MCP tools
> - Understanding query optimization strategies
> - Implementing source credibility assessment
> - Setting up research provenance tracking
>
> This main requirements document contains a basic overview of the Research Coordinator Agent. Refer to the enhancement document for complete implementation specifications, detailed task algorithms, template structures, and knowledge base content.

---

## 1. System Architecture

### 1.1 Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Agent Orchestration Layer                      │
│        (Claude + BMAD Agents via IDE/Desktop)                │
├─────────────────────────────────────────────────────────────┤
│                  MCP Protocol Layer                          │
│  ┌──────────────┬──────────────────┬────────────────────┐  │
│  │ Obsidian MCP │  Neo4j MCP       │ Web Search MCP     │  │
│  │ Tools        │  (Graphiti)      │ (Optional)         │  │
│  └──────────────┴──────────────────┴────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Static Knowledge      Temporal Memory      External Data   │
│  Layer                 Layer                Layer            │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────┐  │
│  │ Obsidian     │     │ Neo4j        │     │ Web APIs   │  │
│  │ Vault        │     │ Graph DB     │     │ Research   │  │
│  │              │     │              │     │ Tools      │  │
│  │ - Markdown   │     │ - Episodes   │     │            │  │
│  │ - Smart      │     │ - Entities   │     │            │  │
│  │   Connections│     │ - Relations  │     │            │  │
│  │ - .ajson     │     │ - Temporal   │     │            │  │
│  │   embeddings │     │   metadata   │     │            │  │
│  └──────────────┘     └──────────────┘     └────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow Patterns

**Capture Flow:**

1. External input → Inbox Triage Agent
2. Agent creates Obsidian note in `/inbox` folder
3. Agent creates Neo4j `CaptureEvent` node with temporal metadata
4. Agent links capture to source and date nodes

**Organization Flow:**

1. Inbox note → Structural Analysis Agent
2. Agent fragments into atomic notes if needed
3. Semantic Linker Agent queries Smart Connections embeddings
4. Agent creates bidirectional links in Obsidian
5. Agent creates `CONCEPTUALLY_RELATED` edges in Neo4j with discovery timestamp

**Synthesis Flow:**

1. Atomic notes → MOC Constructor Agent
2. Agent queries Neo4j for relationship strengths
3. Agent creates hierarchical MOC in Obsidian
4. Agent creates `SYNTHESIZED_IN` relationships in Neo4j

**Temporal Analysis Flow:**

1. Concept query → Timeline Constructor Agent
2. Agent queries Neo4j for all temporal events related to concept
3. Agent queries Obsidian for note version history
4. Agent synthesizes narrative showing evolution
5. Agent creates temporal visualization

### 1.3 Integration Points

| Integration          | Purpose                           | Protocol | Required?           |
| -------------------- | --------------------------------- | -------- | ------------------- |
| Obsidian MCP Tools   | File operations, metadata, search | MCP      | Yes                 |
| Smart Connections    | Semantic search, embeddings       | MCP      | Yes                 |
| Neo4j Graphiti MCP   | Temporal graph, episodic memory   | MCP      | Yes                 |
| Local REST API       | Obsidian vault access             | REST     | Yes (for MCP Tools) |
| WebSearch/Perplexity | External research                 | MCP      | Optional            |
| Context7             | Documentation lookup              | MCP      | Optional            |

---

## 2. Agent Specifications

### 2.1 Core Agents (Required)

#### Agent 1: Inbox Triage Agent

**Name:** Triage
**ID:** `inbox-triage-agent`
**Icon:** 📥
**Persona:**

- **Role:** First-contact handler for all incoming information
- **Style:** Efficient, decisive, detail-oriented, pattern-recognizing
- **Identity:** Information classifier and routing coordinator
- **Focus:** Rapid categorization, source attribution, quality filtering

**Responsibilities:**

- Monitor and process all capture sources (web clipper, highlights, voice notes, emails, social media saves)
- Classify content by type (quote, concept, reference, personal reflection, question, observation)
- Extract metadata (source URL, author, timestamp, context)
- Assess relevance and priority
- Route to appropriate processing queue
- Create initial Obsidian inbox notes
- Create Neo4j CaptureEvent nodes with temporal metadata

**Commands:**

- `*help` - Show available commands
- `*process-inbox` - Process all unprocessed inbox items
- `*capture {source} {content}` - Manual capture with source attribution
- `*classify {note_id}` - Reclassify existing inbox note
- `*batch-process` - Process inbox in bulk (respecting rate limits)
- `*yolo` - Toggle Yolo Mode (auto-process without confirmation)
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `classify-content-type.md` - Determines content type using heuristics
  - `extract-metadata.md` - Pulls source attribution, timestamps, context
  - `assess-relevance.md` - Scores content relevance to existing knowledge
  - `create-inbox-note.md` - Creates standardized inbox note in Obsidian
  - `create-capture-event.md` - Creates temporal Neo4j node for capture
- **Templates:**
  - `inbox-note-tmpl.yaml` - Standardized inbox note format
  - `capture-event-tmpl.yaml` - Neo4j capture node structure
- **Checklists:**
  - `capture-quality-checklist.md` - Validates capture completeness
- **Data:**
  - `content-type-taxonomy.md` - Definitions of content types
  - `source-patterns.md` - URL patterns for source identification

**Integration Requirements:**

- Obsidian MCP Tools: File creation in `/inbox` directory
- Neo4j MCP: Create `(:CaptureEvent)` nodes
- Web Clipper MCP (if available): Automatic capture of highlighted content

---

#### Agent 2: Structural Analysis Agent

**Name:** Atomizer
**ID:** `structural-analysis-agent`
**Icon:** ⚛️
**Persona:**

- **Role:** Note fragmentation specialist and atomic structure enforcer
- **Style:** Analytical, precise, boundary-conscious, principle-driven
- **Identity:** Zettelkasten purist ensuring atomic note discipline
- **Focus:** Identifying discrete knowledge building blocks, preventing note tangling

**Responsibilities:**

- Analyze inbox notes for atomicity violations
- Identify distinct knowledge building blocks (concepts, arguments, models, questions, claims, phenomena)
- Suggest fragmentation boundaries
- Generate title candidates for atomic fragments
- Detect duplicate content with existing notes
- Preserve source attribution across fragments
- Create atomic notes following Zettelkasten principles

**Commands:**

- `*help` - Show available commands
- `*analyze {note_id}` - Analyze note for atomicity
- `*fragment {note_id}` - Fragment non-atomic note into atomic units
- `*detect-duplicates {note_id}` - Find existing notes with similar content
- `*validate-atomic {note_id}` - Check if note meets atomic principles
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `analyze-atomicity.md` - Evaluates note against atomic principles
  - `identify-building-blocks.md` - Finds discrete knowledge units
  - `suggest-fragmentation.md` - Proposes boundary splits
  - `generate-titles.md` - Creates descriptive atomic note titles
  - `detect-duplicates.md` - Finds semantic similarity with existing notes
  - `fragment-note.md` - Splits note into atomic units
- **Templates:**
  - `atomic-note-tmpl.yaml` - Standardized atomic note structure
  - `fragmentation-report-tmpl.yaml` - Analysis results
- **Checklists:**
  - `atomicity-checklist.md` - Validates atomic principles
  - `duplicate-detection-checklist.md` - Ensures unique content
- **Data:**
  - `knowledge-building-blocks.md` - Definitions of 6 atomic types
  - `atomicity-principles.md` - Zettelkasten atomic note guidelines

**Integration Requirements:**

- Obsidian MCP Tools: Read inbox notes, create/update atomic notes
- Smart Connections MCP: Query semantic similarity for duplicate detection
- Neo4j MCP: Create `(:AtomicNote)` nodes with fragmentation history

---

#### Agent 3: Semantic Linker Agent

**Name:** Connector
**ID:** `semantic-linker-agent`
**Icon:** 🔗
**Persona:**

- **Role:** Relationship discovery and bidirectional linking specialist
- **Style:** Curious, exploratory, pattern-seeking, connection-oriented
- **Identity:** Graph-thinking facilitator who sees implicit relationships
- **Focus:** Discovering conceptual relationships beyond keyword matching

**Responsibilities:**

- Query Smart Connections embeddings for semantic similarity
- Identify conceptual overlaps between notes
- Suggest bidirectional link candidates
- Rate connection strength (strong/medium/weak)
- Create provisional MOC entries
- Track relationship discovery timestamps in Neo4j
- Learn from user acceptance/rejection of suggestions

**Commands:**

- `*help` - Show available commands
- `*suggest-links {note_id}` - Find related notes for linking
- `*create-links {note_id} {target_ids}` - Create bidirectional links
- `*review-suggestions` - Show pending link suggestions
- `*accept-suggestion {suggestion_id}` - Accept proposed link
- `*reject-suggestion {suggestion_id}` - Reject proposed link
- `*analyze-graph {note_id}` - Show connection patterns for note
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `query-semantic-similarity.md` - Uses Smart Connections embeddings
  - `identify-concept-overlap.md` - Finds shared concepts
  - `rate-connection-strength.md` - Scores relationship confidence
  - `create-bidirectional-link.md` - Creates wikilinks in both notes
  - `create-neo4j-relationship.md` - Records relationship in temporal graph
  - `learn-from-feedback.md` - Adjusts confidence from user decisions
- **Templates:**
  - `link-suggestion-tmpl.yaml` - Proposed link with reasoning
  - `relationship-record-tmpl.yaml` - Neo4j relationship metadata
- **Checklists:**
  - `linking-quality-checklist.md` - Ensures meaningful connections
  - `relationship-confidence-checklist.md` - Validates strength ratings
- **Data:**
  - `relationship-types.md` - Taxonomy of link relationships
  - `connection-patterns.md` - Common linking patterns

**Integration Requirements:**

- Smart Connections MCP: Query semantic similarity scores
- Obsidian MCP Tools: Create/update note links
- Neo4j MCP: Create `[:CONCEPTUALLY_RELATED]` edges with `discovered_at` timestamp

---

#### Agent 4: MOC Constructor Agent

**Name:** Synthesizer
**ID:** `moc-constructor-agent`
**Icon:** 🗺️
**Persona:**

- **Role:** Maps of Content architect and knowledge navigator
- **Style:** Strategic, hierarchical-thinking, synthesis-oriented, structure-creating
- **Identity:** Information architect building navigational aids
- **Focus:** Creating coherent structure from distributed knowledge

**Responsibilities:**

- Examine collections of related notes
- Identify logical hierarchical structures
- Create Maps of Content with summaries
- Write bridge paragraphs connecting concepts
- Maintain MOC evolution over time
- Track MOC maturity levels (nascent → established)
- Generate dynamic MOCs using Dataview queries

**Commands:**

- `*help` - Show available commands
- `*create-moc {domain}` - Create new Map of Content
- `*update-moc {moc_id}` - Refresh existing MOC
- `*analyze-domain {domain}` - Show coverage and gaps
- `*suggest-moc-structure {domain}` - Propose hierarchical organization
- `*generate-bridge-text {moc_id}` - Create connecting prose
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `analyze-domain-coverage.md` - Identifies notes in domain
  - `identify-hierarchy.md` - Finds logical organization
  - `create-moc-structure.md` - Builds MOC document
  - `generate-summaries.md` - Creates section summaries
  - `write-bridge-paragraphs.md` - Connects concepts with prose
  - `update-moc-temporal-record.md` - Records MOC evolution
- **Templates:**
  - `moc-tmpl.yaml` - Map of Content structure
  - `moc-section-tmpl.yaml` - MOC section format
- **Checklists:**
  - `moc-completeness-checklist.md` - Ensures comprehensive coverage
  - `moc-navigation-checklist.md` - Validates navigability
- **Data:**
  - `moc-patterns.md` - Common MOC organizational structures
  - `linking-your-thinking-kb.md` - LYT framework principles

**Integration Requirements:**

- Obsidian MCP Tools: Create/update MOC documents
- Smart Connections MCP: Query related notes by domain
- Neo4j MCP: Query relationship strengths, record MOC synthesis events
- Claude MCP: Generate bridge prose and summaries

---

#### Agent 5: Query Interpreter Agent

**Name:** Oracle
**ID:** `query-interpreter-agent`
**Icon:** 🔮
**Persona:**

- **Role:** Natural language query translator and multi-backend router
- **Style:** Analytical, routing-intelligent, context-aware, results-focused
- **Identity:** Intelligent dispatcher understanding both temporal and semantic queries
- **Focus:** Routing queries to optimal backends for best results

**Responsibilities:**

- Parse natural language queries
- Detect temporal intent (evolution, history, timeline questions)
- Extract key concepts for semantic search
- Decompose complex queries into sub-queries
- Route to Obsidian, Neo4j, or both
- Rank expected result quality
- Merge results from multiple backends

**Commands:**

- `*help` - Show available commands
- `*query {question}` - Execute intelligent multi-backend query
- `*temporal-query {question}` - Force Neo4j temporal query
- `*semantic-query {question}` - Force Obsidian semantic query
- `*explain-routing {question}` - Show query routing decision
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `parse-natural-language-query.md` - Extracts intent and concepts
  - `detect-temporal-intent.md` - Identifies historical/evolutionary queries
  - `route-query.md` - Decides optimal backend(s)
  - `execute-obsidian-query.md` - Semantic search via Smart Connections
  - `execute-neo4j-query.md` - Temporal/causal queries via Graphiti
  - `merge-results.md` - Synthesizes multi-backend results
- **Templates:**
  - `query-result-tmpl.yaml` - Unified result format
  - `routing-decision-tmpl.yaml` - Explanation of routing logic
- **Checklists:**
  - `query-completeness-checklist.md` - Ensures all aspects addressed
  - `result-quality-checklist.md` - Validates result relevance
- **Data:**
  - `temporal-keywords.md` - Words indicating temporal intent
  - `query-patterns.md` - Common query types and routing rules

**Integration Requirements:**

- Smart Connections MCP: Execute semantic searches
- Neo4j MCP: Execute Cypher temporal queries
- Obsidian MCP Tools: Text search and file retrieval
- Claude MCP: Parse complex natural language queries

---

#### Agent 6: Timeline Constructor Agent

**Name:** Historian
**ID:** `timeline-constructor-agent`
**Icon:** ⏳
**Persona:**

- **Role:** Temporal narrative builder and evolution tracker
- **Style:** Chronological, narrative-oriented, pattern-detecting, story-telling
- **Identity:** Knowledge archaeologist revealing how understanding emerged
- **Focus:** Constructing coherent timelines of idea evolution

**Responsibilities:**

- Retrieve note edit histories from Obsidian
- Query Neo4j for temporal events (captures, edits, promotions, connections)
- Identify periods of rapid evolution vs. stability
- Create chronological narratives
- Highlight unexpected shifts in understanding
- Generate timeline visualizations
- Track concept maturation timelines

**Commands:**

- `*help` - Show available commands
- `*create-timeline {concept}` - Build temporal narrative
- `*evolution-analysis {concept}` - Show how understanding changed
- `*identify-shifts {concept}` - Find key moments of understanding change
- `*compare-timelines {concept1} {concept2}` - Show parallel evolutions
- `*visualize-timeline {concept}` - Generate timeline visualization
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `query-temporal-events.md` - Retrieves Neo4j temporal data
  - `retrieve-edit-history.md` - Gets Obsidian version history
  - `identify-evolution-periods.md` - Finds rapid change vs. stability
  - `create-chronological-narrative.md` - Builds timeline story
  - `generate-timeline-visualization.md` - Creates ASCII/Mermaid timeline
  - `analyze-concept-maturation.md` - Tracks idea progression
- **Templates:**
  - `temporal-narrative-tmpl.yaml` - Timeline narrative structure
  - `evolution-analysis-tmpl.yaml` - Understanding shift analysis
- **Checklists:**
  - `temporal-accuracy-checklist.md` - Validates timestamp correctness
  - `narrative-completeness-checklist.md` - Ensures all key events included
- **Data:**
  - `temporal-analysis-patterns.md` - Common evolution patterns
  - `maturation-stages.md` - Stages of concept development

**Integration Requirements:**

- Neo4j MCP: Query temporal events, relationships, metadata
- Obsidian MCP Tools: Retrieve note metadata and edit history
- Claude MCP: Generate narrative prose and analysis

---

#### Agent 7: Content Brief Agent

**Name:** Curator
**ID:** `content-brief-agent`
**Icon:** 📋
**Persona:**

- **Role:** Context package preparer for creative work
- **Style:** Organized, comprehensive, context-gathering, creative-enabler
- **Identity:** Research librarian assembling everything needed for creation
- **Focus:** Providing complete, well-organized context for writing/creation

**Responsibilities:**

- Receive creation briefs (topic, format, audience, length, deadline)
- Query Obsidian for semantically relevant notes
- Query Neo4j for temporal evolution of concepts
- Organize materials into logical outlines
- Highlight research gaps requiring external work
- Provide quotable passages with attribution
- Track which knowledge items were used in outputs

**Commands:**

- `*help` - Show available commands
- `*create-brief {topic}` - Generate content creation brief
- `*gather-context {topic} {format} {audience}` - Assemble relevant materials
- `*identify-gaps {brief_id}` - Find missing information
- `*generate-outline {brief_id}` - Create structural outline
- `*track-usage {brief_id} {output_id}` - Record knowledge item usage
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `query-relevant-notes.md` - Semantic search for topic
  - `query-temporal-context.md` - Evolution of key concepts
  - `organize-materials.md` - Logical structuring
  - `identify-research-gaps.md` - Find missing information
  - `extract-quotable-passages.md` - Pull citation-ready excerpts
  - `track-content-usage.md` - Record provenance
- **Templates:**
  - `content-brief-tmpl.yaml` - Creation brief structure
  - `usage-manifest-tmpl.yaml` - Content provenance tracking
- **Checklists:**
  - `brief-completeness-checklist.md` - Ensures comprehensive coverage
  - `citation-readiness-checklist.md` - Validates attribution
- **Data:**
  - `content-types.md` - Different creation formats
  - `audience-profiles.md` - Audience adaptation strategies

**Integration Requirements:**

- Smart Connections MCP: Semantic search for relevant notes
- Neo4j MCP: Temporal context queries
- Obsidian MCP Tools: Extract note content
- Claude MCP: Generate outlines and synthesis

---

#### Agent 8: Quality Auditor Agent

**Name:** Inspector
**ID:** `quality-auditor-agent`
**Icon:** 🔍
**Persona:**

- **Role:** Knowledge base quality assurance specialist
- **Style:** Meticulous, systematic, quality-focused, detail-oriented
- **Identity:** Librarian maintaining catalog integrity
- **Focus:** Ensuring accuracy, currency, and coherence

**Responsibilities:**

- Perform periodic knowledge base audits
- Check temporal freshness (notes not updated in 6+ months)
- Validate external links (broken URLs)
- Verify source citation completeness
- Identify orphaned notes (not connected to MOCs)
- Check factual claims against reliable sources
- Generate audit reports with actionable recommendations

**Commands:**

- `*help` - Show available commands
- `*run-audit {scope}` - Execute comprehensive audit
- `*check-freshness` - Find stale notes requiring updates
- `*validate-links` - Test external link accessibility
- `*check-citations` - Verify source attribution completeness
- `*find-orphans` - Identify unconnected notes
- `*generate-report` - Create audit report
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `audit-temporal-freshness.md` - Find stale content
  - `validate-external-links.md` - Test URL accessibility
  - `check-citation-completeness.md` - Verify attribution
  - `detect-orphaned-notes.md` - Find unconnected notes
  - `verify-factual-claims.md` - Check against sources
  - `generate-audit-report.md` - Compile findings
- **Templates:**
  - `audit-report-tmpl.yaml` - Audit results structure
  - `remediation-plan-tmpl.yaml` - Action items for fixes
- **Checklists:**
  - `audit-coverage-checklist.md` - Ensures comprehensive review
  - `audit-quality-checklist.md` - Validates audit thoroughness
- **Data:**
  - `audit-standards.md` - Quality criteria definitions
  - `freshness-thresholds.md` - Age limits by content type

**Integration Requirements:**

- Neo4j MCP: Query temporal metadata for freshness
- Obsidian MCP Tools: Read notes, check backlinks
- Web Validation MCP: Test external link accessibility
- Claude MCP: Generate audit summaries

---

#### Agent 9: Gap Detector Agent

**Name:** Scout
**ID:** `gap-detector-agent`
**Icon:** 🎯
**Persona:**

- **Role:** Knowledge gap identification and research prioritization specialist
- **Style:** Inquisitive, strategic, boundary-aware, opportunity-seeking
- **Identity:** Frontier scout identifying unexplored territories
- **Focus:** Finding what's missing and what needs exploration

**Responsibilities:**

- Identify unresolved questions referenced in notes
- Find concepts mentioned but never developed
- Detect prerequisites referenced but not explained
- Identify claims requiring evidence not in knowledge base
- Find domains adjacent to current knowledge with no coverage
- Distinguish intentional boundaries from genuine gaps
- Prioritize research opportunities

**Commands:**

- `*help` - Show available commands
- `*detect-gaps {scope}` - Identify knowledge gaps
- `*analyze-coverage {domain}` - Assess domain completeness
- `*find-questions` - List unresolved questions
- `*identify-missing-prereqs` - Find assumed knowledge
- `*prioritize-research` - Rank gaps by strategic value
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `identify-unresolved-questions.md` - Find open questions
  - `detect-undeveloped-concepts.md` - Mentioned but not explained
  - `find-missing-prerequisites.md` - Assumed but not defined
  - `identify-evidence-gaps.md` - Claims needing support
  - `analyze-domain-boundaries.md` - Coverage vs. intentional limits
  - `prioritize-gaps.md` - Strategic importance ranking
- **Templates:**
  - `gap-analysis-tmpl.yaml` - Gap identification report
  - `research-priority-tmpl.yaml` - Prioritized research queue
- **Checklists:**
  - `gap-identification-checklist.md` - Ensures comprehensive detection
  - `prioritization-checklist.md` - Validates ranking logic
- **Data:**
  - `gap-types.md` - Taxonomy of knowledge gaps
  - `research-strategies.md` - Approaches for different gap types

**Integration Requirements:**

- Neo4j MCP: Query for unresolved questions, missing relationships
- Obsidian MCP Tools: Analyze note content for gaps
- Smart Connections MCP: Identify underdeveloped concepts
- Claude MCP: Analyze coverage and generate recommendations

---

#### Agent 10: Publication Formatter Agent

**Name:** Publisher
**ID:** `publication-formatter-agent`
**Icon:** 📤
**Persona:**

- **Role:** Knowledge export and format adaptation specialist
- **Style:** Detail-oriented, format-aware, audience-conscious, compliance-focused
- **Identity:** Publishing coordinator preparing knowledge for external consumption
- **Focus:** Converting internal knowledge to publication-ready formats

**Responsibilities:**

- Extract content from Obsidian with relationships preserved
- Convert wikilinks to target format links (HTML, PDF, etc.)
- Generate bibliographies from citation metadata
- Create publication-appropriate headers and formatting
- Generate tables of contents and indexes
- Preserve versioning information
- Ensure privacy compliance (no private content)
- Verify source attribution completeness

**Commands:**

- `*help` - Show available commands
- `*prepare-publication {topic} {format}` - Create publication draft
- `*generate-bibliography {publication_id}` - Create citation list
- `*convert-format {publication_id} {target_format}` - Transform format
- `*check-compliance {publication_id}` - Verify privacy/attribution
- `*create-manifest {publication_id}` - Document source provenance
- `*exit` - Exit agent mode

**Dependencies:**

- **Tasks:**
  - `extract-publication-content.md` - Gather relevant notes
  - `convert-wikilinks.md` - Transform links for target format
  - `generate-bibliography.md` - Compile citations
  - `format-for-target.md` - Apply target format styling
  - `check-privacy-compliance.md` - Verify no private content
  - `verify-attribution.md` - Ensure complete sourcing
  - `create-publication-manifest.md` - Document provenance
- **Templates:**
  - `publication-manifest-tmpl.yaml` - Publication metadata
  - `bibliography-tmpl.yaml` - Citation list structure
- **Checklists:**
  - `publication-quality-checklist.md` - Content quality validation
  - `compliance-checklist.md` - Privacy and attribution verification
- **Data:**
  - `format-specifications.md` - Target format requirements
  - `citation-styles.md` - Bibliography formatting options

**Integration Requirements:**

- Obsidian MCP Tools: Extract content and metadata
- Neo4j MCP: Query source attribution
- Format Conversion MCP (Pandoc): Convert between formats
- Claude MCP: Generate audience-adapted text

---

### 2.2 Optional Agents

#### Agent 11: Research Coordinator Agent (Optional)

> **🔬 ENHANCED SPECIFICATION AVAILABLE**
>
> This agent has been significantly enhanced with adaptive tool detection, intelligent query optimization, and multi-source synthesis capabilities. See the **Research Enhancement Specification** document for complete details:
>
> **Document:** `bmad-obsidian-2nd-brain-research-enhancement.md`
>
> **Key Enhancements:**
>
> - Automatic MCP tool detection and profiling
> - Adaptive query optimization for detected tools (Perplexity, WebSearch, Context7)
> - Multi-tool orchestration (parallel/sequential/hybrid execution)
> - Evidence-based source credibility scoring (0-100 rubric)
> - Multi-source synthesis with conflict resolution
> - Complete provenance tracking in Neo4j
> - Graceful fallback to manual workflows when tools unavailable
>
> The specification below provides a basic overview. Refer to the enhancement document for:
>
> - 19 detailed tasks with adaptive strategies
> - 7 specialized templates
> - 5 quality assurance checklists
> - 6 knowledge bases including tool catalog and optimization patterns

---

**Name:** Researcher
**ID:** `research-coordinator-agent`
**Icon:** 🔬
**Version:** 2.0 (Enhanced)

**Persona:**

- **Role:** Adaptive research orchestrator and knowledge integration specialist
- **Style:** Thorough, tool-aware, synthesis-oriented, source-critical, method-flexible
- **Identity:** Adaptive researcher who maximizes accuracy using available tools
- **Focus:** Executing optimal research workflows based on tool availability and topic requirements

**Core Responsibilities:**

- **Tool Detection:** Automatically discover and profile available MCP research tools
- **Adaptive Research:** Execute optimal research strategies based on detected tools
- **Query Optimization:** Generate queries optimized for specific tool capabilities
- **Quality Assurance:** Assess source credibility with evidence-based scoring (0-100)
- **Multi-Source Synthesis:** Merge findings with conflict resolution and validation
- **Knowledge Integration:** Convert research to atomic notes and update MOCs
- **Provenance Tracking:** Record complete research history in Neo4j

**Key Commands** (See enhancement doc for all 19 commands):

- `*detect-tools` - Scan environment for research MCP tools
- `*research-chapter {topic}` - Enhanced research with workflow mode selection
- `*research-auto {topic}` - Execute automated research using detected tools
- `*research-manual {topic}` - Generate queries for manual research
- `*import-research` - Structure manually-gathered findings
- `*assess-sources {research_id}` - Evaluate source credibility
- `*synthesize-findings {research_id}` - Merge multi-source findings
- `*integrate-findings {research_id}` - Convert research to atomic notes

**Core Dependencies** (See enhancement doc for complete list of 19 tasks):

- **Tasks:**
  - `detect-research-tools.md` - Scan MCP environment for tools
  - `generate-research-queries.md` - Create optimized query sets (10-25)
  - `generate-deep-questions.md` - Create comprehensive questions (20-30)
  - `execute-automated-research.md` - Multi-tool orchestration
  - `assess-source-credibility.md` - Evidence-based scoring (0-100)
  - `synthesize-multi-source-findings.md` - Merge with conflict resolution
  - `integrate-research-findings.md` - Convert to atomic notes
  - `track-research-provenance.md` - Neo4j temporal tracking
- **Templates:**
  - `research-report-tmpl.yaml` - Comprehensive research documentation
  - `tool-detection-report-tmpl.yaml` - Discovered tools and capabilities
  - `research-query-set-tmpl.yaml` - Organized query collection
  - `research-synthesis-tmpl.yaml` - Multi-source finding merger
- **Checklists:**
  - `research-quality-checklist.md` - Validates thoroughness
  - `tool-optimization-checklist.md` - Confirms optimal tool usage
  - `research-synthesis-checklist.md` - Validates finding integration
  - `research-accuracy-checklist.md` - Cross-validation requirements
- **Data/Knowledge Bases:**
  - `research-tools-catalog.md` - MCP tool reference (Perplexity, WebSearch, Context7)
  - `query-optimization-patterns.md` - Tool-specific query templates
  - `credibility-scoring-rubric.md` - Evidence-based source rating (0-100)
  - `research-strategy-patterns.md` - Workflow decision trees

**Integration Requirements:**

- **Required:** Obsidian MCP Tools, Neo4j MCP
- **Optional (Auto-Detected):** Perplexity MCP, WebSearch MCP, Context7 MCP, custom research MCP servers

**Adaptive Behavior:**

- **All Tools Available:** Full automated research with multi-tool orchestration
- **Some Tools Available:** Adapts strategy to use available tools optimally
- **No Tools Available:** Falls back to manual query generation + import workflow

**Note:** This agent is optional but highly recommended for research-intensive workflows. It provides significant value when research MCP tools are available (50-70% time savings, >95% accuracy) while maintaining full functionality through manual workflows when tools are unavailable.

**See Enhancement Document:** `bmad-obsidian-2nd-brain-research-enhancement.md` for complete specifications.

---

## 3. Task Specifications

### 3.1 Capture Phase Tasks

#### Task: classify-content-type.md

**Purpose:** Determine the type of captured content to enable appropriate processing

**Input:**

- Raw captured content (text, URL, image, audio transcript)
- Source context (web clipper, highlight app, email, voice note)

**Process:**

1. Analyze content structure and metadata
2. Apply heuristics to identify type:
   - Quote: Attributed text from external source
   - Concept: Definition or explanation of an idea
   - Reference: Citation or pointer to external resource
   - Personal Reflection: Original thought or observation
   - Question: Inquiry requiring investigation
   - Observation: Factual recording of phenomenon
3. Assign confidence score to classification
4. Flag ambiguous cases for human review

**Output:**

- Content type classification
- Confidence score (0.0-1.0)
- Reasoning for classification
- Alternative type suggestions if confidence < 0.8

**Quality Criteria:**

- Classification accuracy > 90% on validation set
- Ambiguous cases flagged (confidence < 0.8)
- Reasoning provided for all classifications

---

#### Task: extract-metadata.md

**Purpose:** Pull source attribution, timestamps, and context from captured content

**Input:**

- Raw captured content
- Capture source identifier

**Process:**

1. Extract URL or reference from content
2. Capture ISO timestamp of capture event
3. Identify author/creator if available
4. Extract surrounding context (paragraph before/after highlight)
5. Normalize metadata into standard format
6. Validate metadata completeness

**Output:**

- Source URL or reference
- Capture timestamp (ISO 8601)
- Author/creator (if available)
- Context text (surrounding content)
- Metadata completeness score

**Quality Criteria:**

- All captures have timestamp
- Source URL extracted for web content
- Context preserved for highlights
- Character encoding preserved

---

#### Task: create-inbox-note.md

**Purpose:** Create standardized inbox note in Obsidian from captured content

**Input:**

- Classified content with metadata
- Content type classification

**Process:**

1. Generate unique note ID
2. Create frontmatter with metadata
3. Format content body based on type
4. Save to `/inbox` directory
5. Create initial tag set
6. Set processing status to "inbox"

**Output:**

- Created Obsidian note in `/inbox`
- Note ID for reference
- File path

**Quality Criteria:**

- Note follows template structure
- All metadata present in frontmatter
- Content properly formatted
- File saved successfully

---

#### Task: create-capture-event.md

**Purpose:** Create temporal Neo4j node recording capture event

**Input:**

- Created inbox note details
- Capture metadata

**Process:**

1. Create `(:CaptureEvent)` node with properties:
   - `id`: UUID
   - `timestamp`: ISO 8601 capture time
   - `source`: Capture method (web_clipper, highlight, etc.)
   - `url`: Source URL if available
   - `content_type`: Classified type
2. Create `(:Source)` node if new source
3. Create `[:CAPTURED_FROM]` relationship to source
4. Create `[:CAPTURED_ON]` relationship to date node
5. Link to Obsidian note via `obsidian_path` property

**Output:**

- Created Neo4j CaptureEvent node
- Node ID
- Relationships to source and date

**Quality Criteria:**

- All temporal metadata recorded
- Relationships created successfully
- Bidirectional link to Obsidian note

---

### 3.2 Organization Phase Tasks

#### Task: analyze-atomicity.md

**Purpose:** Evaluate note against Zettelkasten atomic principles

**Input:**

- Note ID or content
- Note type (inbox, working, atomic)

**Process:**

1. Count distinct knowledge building blocks in note
2. Classify each building block type:
   - Concept (definition with characteristics)
   - Argument (premises, logic, conclusion)
   - Model (framework or pattern)
   - Question (inquiry statement)
   - Claim (assertion of fact)
   - Phenomenon (observation or recorded instance)
3. Assess if note contains exactly one complete building block
4. Identify fragmentation points if multiple blocks present
5. Generate atomicity score (0.0-1.0)

**Output:**

- Atomicity score
- Building block count
- Building block types identified
- Fragmentation recommendations (if score < 0.8)
- Diagnostic explanation

**Quality Criteria:**

- Clear identification of building block types
- Accurate count of discrete blocks
- Actionable fragmentation recommendations
- Score reflects Zettelkasten principles

---

#### Task: fragment-note.md

**Purpose:** Split non-atomic note into multiple atomic notes

**Input:**

- Note ID to fragment
- Fragmentation plan (boundaries and titles)

**Process:**

1. Validate fragmentation plan with user
2. For each fragment:
   a. Extract content for fragment
   b. Create new atomic note with content
   c. Generate unique ID and title
   d. Preserve source attribution
   e. Add "atomized_from" metadata pointing to original
3. Create bidirectional links between fragments
4. Update original note with "atomized_into" links
5. Move original to `/archive` or delete if requested
6. Create Neo4j nodes for each atomic note
7. Create `[:FRAGMENTED_FROM]` relationships

**Output:**

- List of created atomic note IDs
- Links between fragments
- Archived original note (if applicable)
- Neo4j fragmentation record

**Quality Criteria:**

- All content preserved across fragments
- Source attribution maintained
- Fragmentation history recorded
- Atomic principles satisfied

---

#### Task: query-semantic-similarity.md

**Purpose:** Find semantically similar notes using Smart Connections embeddings

**Input:**

- Note ID or content
- Similarity threshold (default 0.7)
- Max results (default 20)

**Process:**

1. Retrieve note embedding from Smart Connections
2. Query `.smart-env/` for similar embeddings using cosine similarity
3. Rank results by similarity score
4. Filter by threshold
5. Exclude already-linked notes
6. Add context about why notes are similar

**Output:**

- List of similar notes with:
  - Note ID and title
  - Similarity score (0.0-1.0)
  - Shared concepts explanation
  - Link suggestion confidence

**Quality Criteria:**

- Similarity scores accurate (validated against manual judgments)
- Results ranked correctly
- Already-linked notes excluded
- Explanations provided for similarity

---

#### Task: create-bidirectional-link.md

**Purpose:** Create wikilinks in both source and target notes

**Input:**

- Source note ID
- Target note ID
- Link context (reason for link)

**Process:**

1. Read source note content
2. Identify insertion point (Related Concepts section or end)
3. Add wikilink to target with context sentence
4. Read target note content
5. Identify insertion point
6. Add backlink to source with context sentence
7. Save both notes
8. Create Neo4j `[:LINKED_TO]` relationship with timestamp

**Output:**

- Updated source note
- Updated target note
- Neo4j relationship record
- Link creation timestamp

**Quality Criteria:**

- Links inserted in appropriate locations
- Context explains why link exists
- Both notes updated successfully
- Temporal record created

---

### 3.3 Synthesis Phase Tasks

#### Task: create-moc-structure.md

**Purpose:** Build Map of Content document from related notes

**Input:**

- Domain or topic
- List of related note IDs
- MOC structure type (flat, hierarchical, temporal)

**Process:**

1. Query Neo4j for relationship strengths between notes
2. Group notes into logical categories
3. Create hierarchical structure (2-3 levels max)
4. Generate section summaries for each category
5. Order notes within categories by importance/relevance
6. Create MOC document with frontmatter
7. Add bridge paragraphs between sections
8. Insert Dataview queries for dynamic content
9. Create Neo4j `(:MOC)` node with synthesis timestamp

**Output:**

- Created MOC document in Obsidian
- MOC ID
- Neo4j MOC node with relationships to constituent notes
- Section summaries

**Quality Criteria:**

- Comprehensive coverage of domain
- Logical hierarchical organization
- Bridge paragraphs explain connections
- Dynamic queries functional

---

#### Task: generate-summaries.md

**Purpose:** Create concise summaries for MOC sections

**Input:**

- Section topic
- List of notes in section
- Target length (1-3 sentences)

**Process:**

1. Read all notes in section
2. Extract core claims and concepts
3. Identify unifying theme
4. Generate synthesis statement
5. Validate summary covers all notes
6. Ensure summary uses accessible language

**Output:**

- Section summary (1-3 sentences)
- Concepts covered
- Notes included in synthesis

**Quality Criteria:**

- Summary accurately represents all notes
- Concise and clear
- No jargon without definition
- Unifying theme articulated

---

### 3.4 Retrieval Phase Tasks

#### Task: parse-natural-language-query.md

**Purpose:** Extract intent and concepts from user question

**Input:**

- Natural language query string

**Process:**

1. Tokenize query
2. Identify temporal keywords (when, evolved, changed, history)
3. Extract main concepts (nouns, noun phrases)
4. Identify query type:
   - Factual (what, who, where)
   - Temporal (when, how long, evolution)
   - Causal (why, because, influenced)
   - Comparative (versus, compared to, difference)
   - Hypothetical (if, suppose, what-if)
5. Determine required backends (Obsidian, Neo4j, both)
6. Generate structured query representation

**Output:**

- Query type classification
- Temporal intent flag (boolean)
- Extracted concepts (list)
- Backend routing recommendation
- Confidence score

**Quality Criteria:**

- Accurate intent classification
- All key concepts extracted
- Appropriate backend selection
- High confidence (>0.8) for routing

---

#### Task: execute-obsidian-query.md

**Purpose:** Perform semantic search via Smart Connections

**Input:**

- Parsed query with concepts
- Max results

**Process:**

1. Generate embedding for query
2. Query Smart Connections for semantic matches
3. Retrieve top N results
4. Add context snippets showing match
5. Rank by relevance score
6. Format for display

**Output:**

- List of matching notes with:
  - Note ID and title
  - Relevance score
  - Context snippet
  - Link to note

**Quality Criteria:**

- Results semantically relevant
- Ranking accurate
- Context snippets helpful
- Performance < 2 seconds for typical vaults

---

#### Task: execute-neo4j-query.md

**Purpose:** Execute temporal/causal queries via Graphiti MCP

**Input:**

- Parsed query with temporal intent
- Time range (if applicable)
- Concepts to query

**Process:**

1. Translate query intent to Cypher
2. Add temporal filters (valid_at, invalid_at)
3. Execute query via Neo4j MCP
4. Retrieve results with temporal metadata
5. Order by temporal relevance
6. Format for display

**Output:**

- List of temporal results with:
  - Entity or relationship
  - Temporal metadata (valid_at, invalid_at, discovered_at)
  - Context
  - Link to Obsidian note (if applicable)

**Quality Criteria:**

- Accurate Cypher translation
- Temporal filters correctly applied
- Results ordered logically
- Performance < 3 seconds for typical graphs

---

#### Task: merge-results.md

**Purpose:** Synthesize results from Obsidian and Neo4j into unified answer

**Input:**

- Obsidian query results
- Neo4j query results
- Original query

**Process:**

1. Deduplicate results (same note from both backends)
2. Identify temporal context from Neo4j
3. Identify semantic context from Obsidian
4. Detect contradictions between sources
5. Order results by relevance and recency
6. Generate synthesis statement
7. Format unified result set

**Output:**

- Unified result list with:
  - Combined results (deduplicated)
  - Synthesis statement
  - Temporal context (when ideas emerged/changed)
  - Flagged contradictions (if any)
  - Suggested follow-up queries

**Quality Criteria:**

- No duplicate results
- Contradictions explicitly flagged
- Synthesis accurately represents both sources
- Clear presentation

---

### 3.5 Creation Phase Tasks

#### Task: query-relevant-notes.md

**Purpose:** Gather semantically relevant notes for content creation

**Input:**

- Topic or concept
- Format (article, essay, presentation, etc.)
- Audience level

**Process:**

1. Generate embedding for topic
2. Query Smart Connections for semantic matches
3. Expand query to include related MOCs
4. Retrieve connected notes (2-3 hops)
5. Rank by relevance to topic
6. Filter by audience appropriateness
7. Extract key passages

**Output:**

- Ranked list of relevant notes
- Key passages with attribution
- Related MOCs
- Concept coverage map

**Quality Criteria:**

- Comprehensive coverage of topic
- Relevance scores accurate
- Audience-appropriate selections
- Attribution complete

---

#### Task: organize-materials.md

**Purpose:** Structure gathered materials into logical outline

**Input:**

- List of relevant notes
- Creation format requirements
- Target length

**Process:**

1. Identify main themes across notes
2. Group notes by theme
3. Order themes logically (narrative, importance, complexity)
4. Create hierarchical outline (2-3 levels)
5. Assign notes to outline sections
6. Identify gaps in outline
7. Generate section summaries

**Output:**

- Hierarchical outline
- Notes assigned to sections
- Section summaries
- Identified gaps

**Quality Criteria:**

- Logical flow
- Comprehensive coverage
- Gaps identified
- Appropriate depth for format

---

#### Task: track-content-usage.md

**Purpose:** Record which knowledge items were used in creative outputs

**Input:**

- Output ID (article, essay, etc.)
- List of notes referenced
- List of concepts used

**Process:**

1. Create Neo4j `(:CreativeOutput)` node
2. Create `[:USED_IN]` relationships from notes to output
3. Create `[:INFORMED_BY]` relationships from concepts to output
4. Record usage timestamp
5. Create citation manifest
6. Update note metadata with usage count

**Output:**

- Neo4j output node with relationships
- Citation manifest
- Updated note metadata

**Quality Criteria:**

- All used notes recorded
- Timestamps accurate
- Citation manifest complete
- Bidirectional links functional

---

### 3.6 Review Phase Tasks

#### Task: audit-temporal-freshness.md

**Purpose:** Identify notes not updated in specified timeframe

**Input:**

- Freshness threshold (default: 6 months)
- Scope (domain, entire vault)

**Process:**

1. Query Neo4j for notes with last_updated < threshold
2. Retrieve Obsidian note metadata
3. Check if note is marked "evergreen" (exempt from freshness requirement)
4. Calculate staleness score based on:
   - Time since last update
   - Number of incoming links (high-linked notes more important)
   - Domain criticality
5. Rank stale notes by priority
6. Generate update recommendations

**Output:**

- List of stale notes with:
  - Title and ID
  - Days since last update
  - Staleness priority score
  - Update recommendations

**Quality Criteria:**

- Accurate freshness calculation
- Evergreen notes excluded
- Priority ranking logical
- Actionable recommendations

---

#### Task: validate-external-links.md

**Purpose:** Test accessibility of external links in notes

**Input:**

- Scope (note, domain, entire vault)

**Process:**

1. Extract all external URLs from notes in scope
2. Test each URL with HTTP HEAD request
3. Record response codes:
   - 200-299: Valid
   - 300-399: Redirect (follow and retest)
   - 400-499: Client error (broken)
   - 500-599: Server error (temporarily down)
   - Timeout: Unreachable
4. Identify broken links (4xx errors)
5. Suggest replacements via web search if available
6. Generate validation report

**Output:**

- Link validation report with:
  - Valid links count
  - Broken links list with notes containing them
  - Redirect links requiring update
  - Suggested replacements for broken links

**Quality Criteria:**

- All links tested
- Response codes accurate
- Replacements suggested for broken links
- Report clearly formatted

---

#### Task: detect-orphaned-notes.md

**Purpose:** Find notes not connected to MOCs or other notes

**Input:**

- Scope (domain, entire vault)
- Exemption tags (e.g., #private, #draft)

**Process:**

1. Query Obsidian for all notes in scope
2. Check for:
   - Outgoing wikilinks (links TO other notes)
   - Incoming backlinks (links FROM other notes)
   - MOC membership (linked from MOC)
3. Identify notes with:
   - Zero outgoing links AND zero incoming links
   - Zero MOC membership
4. Exclude exempted tags
5. Rank orphans by:
   - Age (older = higher priority)
   - Content length (longer = higher priority)
   - Last modified date

**Output:**

- List of orphaned notes with:
  - Title and ID
  - Creation date
  - Last modified date
  - Content length
  - Suggested actions (link, archive, delete)

**Quality Criteria:**

- Accurate orphan detection
- Exempted tags respected
- Priority ranking logical
- Actionable recommendations

---

#### Task: generate-audit-report.md

**Purpose:** Compile comprehensive audit findings into actionable report

**Input:**

- Freshness audit results
- Link validation results
- Orphan detection results
- Citation completeness results

**Process:**

1. Aggregate all audit findings
2. Categorize issues by severity:
   - Critical: Broken links, unattributed claims
   - High: Stale critical notes, orphaned evergreen notes
   - Medium: Stale regular notes, redirect links
   - Low: Minor formatting issues
3. Generate prioritized action items
4. Estimate remediation effort
5. Create remediation plan template
6. Format report for readability

**Output:**

- Audit report document with:
  - Executive summary (high-level findings)
  - Detailed findings by category
  - Prioritized action items
  - Remediation plan template
  - Estimated effort

**Quality Criteria:**

- Comprehensive coverage of all audits
- Clear prioritization
- Actionable items
- Effort estimates realistic

---

### 3.7 Temporal Analysis Phase Tasks

#### Task: query-temporal-events.md

**Purpose:** Retrieve temporal metadata from Neo4j for concept evolution

**Input:**

- Concept or note ID
- Time range (optional)
- Event types (captures, edits, promotions, connections)

**Process:**

1. Query Neo4j for all temporal events related to concept:
   ```cypher
   MATCH (note:Note {title: $concept})
   MATCH (note)-[captured:CAPTURED_AT]->(capture_date:Date)
   MATCH (note)-[edited:EDITED_AT]->(edit_dates:Date)
   OPTIONAL MATCH (note)-[promoted:PROMOTED_AT]->(promo_date:Date)
   RETURN note, captured, edited, promoted
   ```
2. Retrieve edit history metadata
3. Retrieve relationship discovery timestamps
4. Order events chronologically
5. Identify event clusters (rapid evolution periods)
6. Calculate maturation metrics

**Output:**

- Chronologically ordered event list with:
  - Event type (capture, edit, promotion, link)
  - Timestamp
  - Context
  - Maturation metrics (days in progress, edit count)

**Quality Criteria:**

- All events retrieved
- Chronological order accurate
- Maturation metrics calculated correctly
- Time ranges respected

---

#### Task: create-chronological-narrative.md

**Purpose:** Build readable narrative of concept evolution

**Input:**

- Temporal events list
- Concept name
- Narrative style (academic, casual, detailed, summary)

**Process:**

1. Identify key evolution phases:
   - Initial capture (concept introduction)
   - Development phase (rapid edits)
   - Maturation phase (slowing edits, promotion to evergreen)
   - Maintenance phase (occasional updates)
2. For each phase:
   a. Identify triggering events (new sources, conflicting information)
   b. Summarize understanding at phase start vs. phase end
   c. Note significant shifts in interpretation
3. Generate narrative prose connecting phases
4. Add temporal markers (dates, durations)
5. Highlight unexpected insights or contradictions
6. Format for readability

**Output:**

- Temporal narrative document with:
  - Initial understanding statement
  - Key evolution phases with dates
  - Shifts in understanding
  - Current understanding statement
  - Unresolved tensions
  - Timeline visualization

**Quality Criteria:**

- Narrative flows logically
- All key events included
- Shifts clearly articulated
- Accessible prose (not overly technical)

---

### 3.8 Cross-Linking Phase Tasks

#### Task: suggest-bidirectional-links.md

**Purpose:** Proactively propose new relationships between notes

**Input:**

- Note ID (or "all notes" for vault-wide suggestions)
- Confidence threshold (default 0.7)
- Max suggestions (default 10)

**Process:**

1. Calculate semantic similarity between note and all other notes
2. Query Neo4j for temporal proximity (notes created/edited around same time)
3. Detect shared references or sources
4. Calculate composite link suggestion score:
   - Semantic similarity \* 0.6
   - Temporal proximity \* 0.2
   - Shared sources \* 0.2
5. Filter by confidence threshold
6. Exclude already-linked notes
7. Generate reasoning for each suggestion
8. Rank by confidence score

**Output:**

- List of link suggestions with:
  - Target note ID and title
  - Confidence score
  - Reasoning (why link is suggested)
  - Relationship type (semantic/temporal/source-based)

**Quality Criteria:**

- Confidence scores accurate (validated against manual judgments)
- Reasoning clear and specific
- No false positives (already-linked notes)
- Ranked appropriately

---

#### Task: detect-logical-contradictions.md

**Purpose:** Identify incompatible claims across knowledge base

**Input:**

- Scope (domain or entire vault)
- Contradiction types (factual, assumptive, definitional)

**Process:**

1. Extract all claims from notes in scope
2. Parse claim structure (subject, predicate, object)
3. Identify mutually exclusive claim pairs:
   - Factual: "X is Y" vs. "X is not Y"
   - Assumptive: Claim A requires assumption P, Claim B requires NOT P
   - Definitional: "X means Y" in note 1 vs. "X means Z" in note 2
4. Check temporal context (is one claim superseded by another?)
5. Flag active contradictions (both claims currently valid)
6. Generate resolution strategies:
   - Refine definition to eliminate ambiguity
   - Gather additional evidence to resolve
   - Accept paradox if legitimate
7. Create Neo4j `(:Contradiction)` nodes

**Output:**

- List of contradictions with:
  - Claim 1 (note, statement, date)
  - Claim 2 (note, statement, date)
  - Contradiction type
  - Temporal status (active, resolved, superseded)
  - Resolution strategies

**Quality Criteria:**

- Accurate contradiction detection (validated against manual review)
- False positives minimized (check for contextual disambiguation)
- Resolution strategies actionable
- Temporal status correct

---

### 3.9 Gap Identification Phase Tasks

#### Task: identify-unresolved-questions.md

**Purpose:** Find open questions referenced in notes

**Input:**

- Scope (domain or entire vault)
- Question markers (?, TODO, INVESTIGATE, RESEARCH)

**Process:**

1. Scan all notes in scope for question markers
2. Extract questions using regex patterns
3. Check if question has been answered:
   - Search for notes with question in title
   - Check for explicit "Answer:" sections
   - Query Neo4j for `[:ANSWERS]` relationships
4. Classify unresolved questions by type:
   - Factual (requires external research)
   - Inferential (requires reasoning from existing knowledge)
   - Exploratory (open-ended inquiry)
5. Assess answering feasibility:
   - Evidence available in knowledge base?
   - External sources accessible?
   - Complexity of research required
6. Prioritize by strategic value

**Output:**

- List of unresolved questions with:
  - Question text
  - Source note and date
  - Question type
  - Answering feasibility
  - Strategic priority score

**Quality Criteria:**

- All question markers detected
- Answered questions correctly excluded
- Feasibility assessments realistic
- Priority scores justified

---

#### Task: prioritize-gaps.md

**Purpose:** Rank knowledge gaps by strategic importance

**Input:**

- List of identified gaps (questions, missing concepts, etc.)
- Active projects and goals

**Process:**

1. For each gap, calculate importance score:
   - Reference count (how often gap appears) \* 10
   - Blocking work count (projects waiting on gap resolution) \* 50
   - Domain centrality (how critical domain is to overall knowledge base) \* 20
2. Assess research feasibility:
   - Accessible sources available?
   - Estimated time required (hours)
   - Required expertise level
3. Calculate net priority:
   - Priority = Importance / (Feasibility \* EstimatedHours)
4. Rank gaps by priority score
5. Group by research method (reading, experimentation, expert consultation)
6. Generate research queue

**Output:**

- Prioritized gap list with:
  - Gap description
  - Importance score breakdown
  - Feasibility assessment
  - Estimated effort (hours)
  - Net priority score
  - Recommended research method
  - Blocking work (if any)

**Quality Criteria:**

- Importance scores justified
- Feasibility assessments realistic
- Priority ranking logical
- Research methods appropriate

---

### 3.10 Publishing Phase Tasks

#### Task: extract-publication-content.md

**Purpose:** Gather all notes and relationships for publication

**Input:**

- Publication topic or note list
- Depth (direct links only, or 2-3 hops)

**Process:**

1. Query Neo4j for complete content graph:
   ```cypher
   MATCH path = (root:Note {title: $publication_topic})
   -[*..3]->(related:Note)
   MATCH (related)-[:CITES]->(source:Source)
   RETURN path, related, source
   ```
2. Retrieve all note content from Obsidian
3. Extract wikilinks and resolve to full note titles
4. Compile bibliography from `:CITES` relationships
5. Order notes by logical flow (for narrative publications)
6. Preserve relationship metadata (link types, strengths)

**Output:**

- Complete content package with:
  - Ordered note list
  - Full note content
  - Bibliography
  - Relationship map
  - Last updated timestamps

**Quality Criteria:**

- All relevant notes included
- Bibliography complete
- Logical ordering
- No broken references

---

#### Task: convert-wikilinks.md

**Purpose:** Transform wikilinks to target format links

**Input:**

- Note content with wikilinks
- Target format (HTML, PDF, Markdown, etc.)

**Process:**

1. Parse wikilinks using regex: `\[\[([^\]]+)\]\]`
2. For each wikilink:
   a. Extract note title
   b. Resolve to note ID or URL
   c. Convert to target format:
   - HTML: `<a href="...">...</a>`
   - PDF: Footnote reference
   - Markdown: `[title](url)`
   - Plain text: (see: title)
3. Handle link with display text: `[[target|display]]`
4. Handle link to section: `[[note#section]]`
5. Validate all links resolve

**Output:**

- Converted content with target format links
- Link conversion log
- Unresolved link warnings (if any)

**Quality Criteria:**

- All wikilinks converted
- Link semantics preserved
- Target format valid
- Unresolved links flagged

---

#### Task: check-privacy-compliance.md

**Purpose:** Verify no private content included in publication

**Input:**

- Publication content
- Privacy rules (tags, folder patterns, explicit markers)

**Process:**

1. Scan content for privacy markers:
   - Tags: #private, #draft, #confidential
   - Frontmatter: `private: true`, `status: draft`
   - Folder patterns: `/private/`, `/personal/`
2. Check Neo4j for `privacy_level` property
3. Flag any private content for review
4. Check for PII (personally identifiable information):
   - Email addresses (if not author's)
   - Phone numbers
   - Street addresses
   - Social security numbers
5. Verify all external sources have appropriate permissions
6. Generate compliance report

**Output:**

- Compliance status (pass/fail)
- Flagged content list (if any violations)
- PII detection warnings
- Permission verification status

**Quality Criteria:**

- All privacy markers detected
- PII detection accurate
- No false negatives (missed private content)
- Clear reporting

---

## 4. Template Specifications

### 4.1 Capture & Organization Templates

#### Template: inbox-note-tmpl.yaml

**Purpose:** Standardized structure for captured content

**Structure:**

```yaml
name: inbox-note-tmpl
description: Template for newly captured content in inbox
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: type
        type: select
        options: [inbox, capture, highlight]
        required: true
      - name: captured
        type: datetime
        format: ISO8601
        required: true
      - name: source
        type: text
        description: URL or reference
        required: false
      - name: author
        type: text
        required: false
      - name: content_type
        type: select
        options: [quote, concept, reference, reflection, question, observation]
        required: true
      - name: status
        type: select
        options: [inbox, reviewed, processing, processed]
        default: inbox
      - name: confidence
        type: number
        range: [0.0, 1.0]
        description: Classification confidence

  - id: content
    title: Raw Content
    instructions: Preserve original text exactly as captured

  - id: context
    title: Context
    instructions: Surrounding context from source (paragraph before/after)
    required: false

  - id: initial_thoughts
    title: Initial Thoughts
    instructions: First impressions or connections noticed
    required: false
```

**Variable Substitution:**

- `{{captured}}` - ISO timestamp of capture
- `{{source}}` - URL or reference
- `{{content_type}}` - Classified type
- `{{confidence}}` - Classification confidence score

---

#### Template: atomic-note-tmpl.yaml

**Purpose:** Standardized structure for atomic notes following Zettelkasten principles

**Structure:**

```yaml
name: atomic-note-tmpl
description: Template for atomic notes containing single knowledge building block
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: type
        type: select
        options: [atomic_note, evergreen]
        default: atomic_note
      - name: created
        type: datetime
        format: ISO8601
        required: true
      - name: updated
        type: datetime
        format: ISO8601
        required: true
      - name: atomized_from
        type: link
        description: Original source note if fragmented
        required: false
      - name: status
        type: select
        options: [working, refined, established]
        default: working
      - name: confidence
        type: select
        options: [high, medium, low]
        description: Confidence in understanding
        default: medium
      - name: building_block_type
        type: select
        options: [concept, argument, model, question, claim, phenomenon]
        required: true
      - name: related_mocs
        type: list_of_links
        description: MOCs that reference this note

  - id: core_claim
    title: Core Claim
    instructions: |
      Single main idea in 1-2 sentences. This is the atomic unit.
      For concepts: Precise definition with essential characteristics
      For arguments: Premises, logical form, and conclusion
      For models: Framework description and application
      For questions: Clear inquiry statement
      For claims: Assertion with specificity
      For phenomena: Observation with context

  - id: evidence_context
    title: Evidence & Context
    instructions: Supporting details, examples, elaborations
    required: false

  - id: related_concepts
    title: Related Concepts
    instructions: Bidirectional links to conceptually adjacent notes

  - id: source_attribution
    title: Source & Attribution
    instructions: Original source reference with citation
    required: true
```

**Variable Substitution:**

- `{{created}}` - Note creation timestamp
- `{{updated}}` - Last modification timestamp
- `{{building_block_type}}` - Type of atomic unit
- `{{status}}` - Working/refined/established
- `{{confidence}}` - High/medium/low

---

#### Template: moc-tmpl.yaml

**Purpose:** Map of Content structure for knowledge domain navigation

**Structure:**

````yaml
name: moc-tmpl
description: Template for Maps of Content (MOCs)
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: type
        type: select
        options: [map_of_content, MOC]
        default: map_of_content
      - name: created
        type: datetime
        required: true
      - name: updated
        type: datetime
        required: true
      - name: domain
        type: text
        description: Topic domain this MOC covers
        required: true
      - name: status
        type: select
        options: [active, archived]
        default: active
      - name: last_review
        type: datetime
        description: Last comprehensive review date
      - name: maturity_level
        type: select
        options: [nascent, developing, established, comprehensive]
        description: MOC development stage
        default: nascent

  - id: overview
    title: Overview
    instructions: 2-3 sentence synthesis of domain

  - id: core_concepts
    title: Core Concepts
    instructions: |
      List core concepts with 1-sentence definitions and links
      Format: - [[Concept Name]]: Brief definition

  - id: knowledge_branches
    title: Knowledge Branches
    subsections_dynamic: true
    instructions: |
      For each branch:
      ### Branch Name
      Summary and links to related notes

  - id: emerging_questions
    title: Emerging Questions
    instructions: Open questions needing research or investigation
    required: false

  - id: dataview_queries
    title: Dynamic Content
    instructions: |
      Optional Dataview queries for dynamic note lists
      Example:
      ```dataview
      TABLE status, updated
      FROM #domain AND -#archived
      SORT updated DESC
      ```
    required: false

  - id: maintenance_history
    title: Last Updated
    instructions: Date and summary of last update
````

**Variable Substitution:**

- `{{domain}}` - Topic domain
- `{{updated}}` - Last modification timestamp
- `{{maturity_level}}` - Nascent/developing/established/comprehensive

---

### 4.2 Synthesis & Analysis Templates

#### Template: temporal-narrative-tmpl.yaml

**Purpose:** Chronological narrative of concept evolution

**Structure:**

````yaml
name: temporal-narrative-tmpl
description: Template for temporal analysis narratives
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: type
        type: select
        options: [temporal_narrative, evolution_analysis]
        default: temporal_narrative
      - name: narrative_type
        type: select
        options: [idea_evolution, domain_development, personal_shift]
        required: true
      - name: start_date
        type: date
        format: ISO8601
        required: true
      - name: end_date
        type: date
        format: ISO8601
        required: true
      - name: primary_subject
        type: text
        description: Concept being tracked
        required: true
      - name: maturation_days
        type: number
        description: Days from capture to evergreen promotion

  - id: initial_understanding
    title: Initial Understanding
    instructions: |
      Document how concept was first understood
      Include:
      - Date of initial capture
      - Original formulation (quote if from source)
      - Source attribution
      - Initial context or trigger

  - id: key_shifts
    title: Key Shifts
    subsections_dynamic: true
    instructions: |
      For each significant shift in understanding:
      ### Shift [Number] ([Date])
      - What changed
      - Why it changed (new evidence, contradiction, synthesis)
      - New understanding formulation
      - Confidence in new understanding

  - id: current_understanding
    title: Current Understanding
    instructions: |
      Latest formulation of concept
      Include:
      - Current definition/explanation
      - Confidence level (high/medium/low)
      - Date of last significant update

  - id: unresolved_tensions
    title: Unresolved Tensions
    instructions: |
      Remaining contradictions, uncertainties, or open questions
      Include what would resolve each tension
    required: false

  - id: timeline_visualization
    title: Timeline Visualization
    instructions: |
      ASCII or Mermaid timeline showing key events
      Example:
      ```
      2024-01-15: Initial capture from Source A
      2024-02-03: Contradiction discovered in Source B
      2024-02-10: Synthesis resolved contradiction
      2024-03-15: Promoted to evergreen
      ```

  - id: influences
    title: Influences
    instructions: |
      What influenced understanding at each stage
      Include:
      - External sources (books, articles, conversations)
      - Internal connections (other notes, MOCs)
      - Events or experiences
    required: false
````

**Variable Substitution:**

- `{{primary_subject}}` - Concept name
- `{{start_date}}` - Begin date
- `{{end_date}}` - End date
- `{{maturation_days}}` - Calculated days to maturity

---

#### Template: link-suggestion-tmpl.yaml

**Purpose:** Proposed bidirectional link with reasoning

**Structure:**

```yaml
name: link-suggestion-tmpl
description: Template for link suggestions from Semantic Linker Agent
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: suggestion_type
        type: select
        options: [semantic, temporal, causal, bridging, source-based]
        required: true
      - name: source_note
        type: link
        description: Note ID requesting link suggestions
        required: true
      - name: target_note
        type: link
        description: Note ID suggested for linking
        required: true
      - name: confidence
        type: number
        range: [0.0, 1.0]
        description: Confidence in suggestion quality
        required: true
      - name: reasoning
        type: text
        description: Brief explanation for suggestion
        required: true
      - name: automatically_created
        type: boolean
        default: false
        description: Whether link was auto-created (Yolo mode)
      - name: user_decision
        type: select
        options: [pending, accepted, rejected, review_later]
        default: pending
      - name: decision_date
        type: datetime
        description: When user made decision

  - id: why_link
    title: Why This Link
    instructions: |
      Detailed explanation of detected relationship
      Include:
      - Primary reason for suggestion
      - Type of relationship (supports, contradicts, elaborates, etc.)

  - id: semantic_similarity
    title: Semantic Similarity
    instructions: |
      Overlapping concepts with similarity scores
      Format:
      - Concept X: similarity 0.85
      - Concept Y: similarity 0.78
    required: false

  - id: temporal_context
    title: Temporal Context
    instructions: |
      When these ideas appeared and evolved
      Include:
      - Capture dates
      - Edit timeline
      - Temporal proximity
    required: false

  - id: implications
    title: Implications
    instructions: |
      What connecting these ideas reveals or suggests
      Include:
      - New insights from connection
      - Patterns that emerge
      - Questions raised

  - id: user_options
    title: User Options
    instructions: |
      Available actions:
      - Accept: Creates bidirectional wikilink in both notes
      - Reject: System notes decision for learning
      - Review Later: Marks for future consideration
```

**Variable Substitution:**

- `{{source_note}}` - Source note title
- `{{target_note}}` - Target note title
- `{{confidence}}` - Confidence score
- `{{suggestion_type}}` - Type of suggestion

---

### 4.3 Review & Quality Templates

#### Template: audit-report-tmpl.yaml

**Purpose:** Comprehensive knowledge base quality audit results

**Structure:**

```yaml
name: audit-report-tmpl
description: Template for knowledge base audit reports
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: audit_type
        type: select
        options: [comprehensive, freshness, links, citations, completeness]
        required: true
      - name: audit_date
        type: datetime
        format: ISO8601
        required: true
      - name: audit_scope
        type: text
        description: Domain, tag filter, or "entire vault"
        required: true
      - name: issues_found
        type: number
        description: Total issue count
      - name: critical_issues
        type: number
      - name: auditor_agent
        type: text
        default: quality-auditor-agent

  - id: executive_summary
    title: Executive Summary
    instructions: |
      High-level findings (3-5 sentences)
      Include:
      - Overall vault health assessment
      - Most critical issues
      - Recommended next steps

  - id: freshness_issues
    title: Freshness Issues
    instructions: |
      Notes requiring updates due to age
      Format:
      | Note | Days Stale | Priority | Recommendation |
      |------|-----------|----------|----------------|
      Include:
      - Critical domain notes
      - Frequently-referenced notes
      - Evergreen notes unexpectedly stale
    required: false

  - id: link_validation_issues
    title: Link Validation Issues
    instructions: |
      External links with problems
      Format:
      - Broken (4xx): [list with notes containing them]
      - Redirects (3xx): [list needing update]
      - Timeouts: [list of unreachable]
      Include suggested replacements where available
    required: false

  - id: citation_issues
    title: Source Validation Issues
    instructions: |
      Citations and attribution problems
      Include:
      - Unattributed claims (notes with assertions but no sources)
      - Incomplete citations (missing URL, date, author)
      - Circular citations (notes citing each other with no external source)
    required: false

  - id: orphan_issues
    title: Orphaned Notes
    instructions: |
      Notes not connected to knowledge graph
      Format:
      | Note | Created | Modified | Length | Action |
      |------|---------|----------|--------|--------|
      Actions: Link, Archive, Delete
    required: false

  - id: quality_issues
    title: Quality Issues
    instructions: |
      Other quality concerns
      Include:
      - Notes violating atomic principles
      - Duplicated content
      - Formatting inconsistencies
      - Missing metadata
    required: false

  - id: action_items
    title: Prioritized Action Items
    instructions: |
      Ranked list of required actions
      Format:
      1. [Critical] Fix broken links in Core Domain MOC
      2. [High] Update stale evergreen notes (5 notes)
      3. [Medium] Link orphaned notes (12 notes)
      ...
      Include estimated effort (hours)

  - id: metrics
    title: Vault Metrics
    instructions: |
      Overall vault statistics
      Include:
      - Total notes
      - Notes by type (inbox, atomic, MOC, etc.)
      - Link density (avg links per note)
      - Recent activity (notes created/edited in last 30 days)
      - Vault health score (0-100)
```

**Variable Substitution:**

- `{{audit_date}}` - Audit execution date
- `{{audit_scope}}` - Scope description
- `{{issues_found}}` - Total issue count

---

#### Template: gap-analysis-tmpl.yaml

**Purpose:** Knowledge gap identification report

**Structure:**

```yaml
name: gap-analysis-tmpl
description: Template for knowledge gap analysis
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: gap_type
        type: select
        options: [coverage, evidence, prerequisite, assumption, conceptual]
        required: true
      - name: discovery_date
        type: datetime
        required: true
      - name: gap_location
        type: select
        options: [within_notes, cross_domain, foundational, methodological]
        description: Where gap manifests
      - name: priority
        type: select
        options: [critical, high, medium, low]
        required: true
      - name: research_status
        type: select
        options: [identified, researching, researched, closed]
        default: identified
      - name: blocking_work
        type: list_of_links
        description: Projects or outputs waiting on gap resolution

  - id: gap_description
    title: Knowledge Gap Description
    instructions: |
      Clear description of what is missing
      Include:
      - What we don't know
      - Why it's a gap (vs. intentional boundary)
      - How gap manifests (errors, confusion, inability to proceed)

  - id: why_matters
    title: Why This Gap Matters
    instructions: |
      Impact on current understanding and work
      Include:
      - How gap limits current work
      - Potential insights if gap filled
      - Risks of leaving gap unaddressed

  - id: where_appears
    title: Where Gap Appears
    instructions: |
      Specific references where gap creates problems
      Format:
      - [[Note A]]: Can't complete argument due to missing premise X
      - [[Note B]]: Contradiction unresolvable without understanding Y
      - [[Project C]]: Decision blocked pending research on Z

  - id: research_approach
    title: Suggested Research Approach
    instructions: |
      Methods, sources, estimated effort
      Include:
      - Recommended research methods (reading, experimentation, consultation)
      - Potential sources (specific books, experts, datasets)
      - Estimated effort (hours or days)
      - Required expertise level

  - id: success_criteria
    title: Success Criteria
    instructions: |
      How to know gap is adequately filled
      Include:
      - Specific questions that should be answerable
      - Artifacts that should exist (notes, data, etc.)
      - Validation method (review against sources, expert consultation)

  - id: related_gaps
    title: Related Gaps
    instructions: |
      Other gaps that depend on this one or are adjacent
      Format:
      - Depends on: [gaps that must be resolved first]
      - Blocks: [gaps that can't be addressed until this one is]
      - Related: [adjacent gaps that might resolve together]
    required: false

  - id: research_progress
    title: Research Progress
    instructions: |
      Timeline of research effort and findings
      Format:
      - [Date]: Started research approach X
      - [Date]: Found source Y, provided partial answer
      - [Date]: Consulted expert Z, clarified aspect A
      Update as research progresses
    required: false
```

**Variable Substitution:**

- `{{gap_type}}` - Coverage/evidence/prerequisite/assumption
- `{{priority}}` - Critical/high/medium/low
- `{{research_status}}` - Current status

---

### 4.4 Creation & Publishing Templates

#### Template: content-brief-tmpl.yaml

**Purpose:** Context package for content creation

**Structure:**

```yaml
name: content-brief-tmpl
description: Template for content creation briefs
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: creation_type
        type: select
        options: [article, essay, presentation, video_script, tweet_thread, code_project, tutorial]
        required: true
      - name: topic
        type: text
        description: Primary subject matter
        required: true
      - name: audience
        type: text
        description: Intended readers/viewers
        required: true
      - name: tone
        type: select
        options: [formal, conversational, technical, inspirational, educational]
      - name: length_target
        type: text
        description: Word count, time duration, or scope
      - name: deadline
        type: date
      - name: created_at
        type: datetime
        required: true

  - id: core_arguments
    title: Core Arguments
    instructions: |
      Main points to develop
      Format:
      1. [[Note A]]: Argument or claim with link
      2. [[Note B]]: Supporting point
      Include preview of how arguments connect

  - id: supporting_evidence
    title: Supporting Evidence
    instructions: |
      Key data, quotes, examples
      Format:
      - From [[Source X]]: "Quotable passage" (context)
      - Data point from [[Note Y]]: 42% increase (interpretation)
      Include full attribution for all evidence

  - id: counterarguments
    title: Counterarguments
    instructions: |
      Alternative perspectives to address
      Format:
      - Objection A: [description]
        - From [[Note X]]
        - Refutation: [how to address]
    required: false

  - id: temporal_context
    title: Temporal Context
    instructions: |
      How topic has evolved; relevant timing
      Include:
      - Historical development (if relevant)
      - Recent changes or trends
      - Why now? (timeliness argument)
    required: false

  - id: unique_angles
    title: Unique Angles
    instructions: |
      Unexpected connections; novel combinations
      Include:
      - Cross-domain insights (connecting X and Y)
      - Contrarian takes
      - Analogies or metaphors

  - id: research_gaps
    title: Research Gaps
    instructions: |
      Information needed beyond knowledge base
      Format:
      - Gap A: [what's needed]
        - Suggested sources: [list]
        - Estimated effort: [hours]
    required: false

  - id: citation_manifest
    title: Citation Manifest
    instructions: |
      Complete list of knowledge base items used
      Auto-populated by Content Brief Agent
      Format:
      - [[Note A]]: Used in section 1 (core argument)
      - [[Note B]]: Used in section 2 (evidence)
      Enables provenance tracking
```

**Variable Substitution:**

- `{{topic}}` - Topic description
- `{{creation_type}}` - Article/essay/presentation/etc.
- `{{audience}}` - Intended audience
- `{{deadline}}` - Target date

---

#### Template: publication-manifest-tmpl.yaml

**Purpose:** Metadata and provenance for published content

**Structure:**

```yaml
name: publication-manifest-tmpl
description: Template for publication tracking and provenance
sections:
  - id: frontmatter
    title: Metadata
    fields:
      - name: publication_type
        type: select
        options: [blog_post, article, paper, book_chapter, presentation, video, tweet_thread]
        required: true
      - name: target_format
        type: select
        options: [html, pdf, markdown, epub, slides, plain_text]
        required: true
      - name: target_audience
        type: select
        options: [general, expert, practitioner, students, peers]
        required: true
      - name: publication_date
        type: datetime
        required: true
      - name: source_notes
        type: list_of_links
        description: Obsidian notes used in publication
        required: true
      - name: content_status
        type: select
        options: [draft, review, published, archived]
        default: draft
      - name: version_control
        type: text
        description: Version number (semantic versioning)
        default: '1.0.0'

  - id: metadata_section
    title: Metadata
    instructions: |
      Publication details
      - Format: [Target format]
      - Audience: [Intended readers]
      - Scope: [What's included/excluded]
      - Word count: [Approximate]
      - Published to: [Platform or venue]

  - id: content
    title: Content
    instructions: |
      Actual publication content with embedded formatting
      Converted from Obsidian wikilinks to target format

  - id: bibliography
    title: Bibliography
    instructions: |
      Complete source attribution
      Auto-generated from citation metadata
      Format:
      [1] Author. "Title". Publication. Date. URL.
      [2] ...

  - id: version_history
    title: Version History
    instructions: |
      Publication version updates
      Format:
      - v1.0.0 ([Date]): Initial publication
      - v1.1.0 ([Date]): Updated section X based on feedback
      - v1.1.1 ([Date]): Fixed typos

  - id: reversion_path
    title: Reversion Path
    instructions: |
      How to return content to knowledge base
      Include:
      - Which notes were modified for publication (audience adaptation)
      - What insights from publication should feed back to KB
      - Whether published version should be archived in KB

  - id: usage_tracking
    title: Usage Tracking
    instructions: |
      Link to Neo4j CreativeOutput node
      Tracks:
      - Which notes were used
      - Which concepts were referenced
      - When output was created
      - Feedback or insights from publication
```

**Variable Substitution:**

- `{{publication_type}}` - Blog post/article/etc.
- `{{target_format}}` - HTML/PDF/etc.
- `{{publication_date}}` - Publication timestamp
- `{{version_control}}` - Version number

---

## 5. Checklist Specifications

### 5.1 Capture Quality Checklists

#### Checklist: capture-quality-checklist.md

**Purpose:** Validate capture completeness and accuracy

**Items:**

- [ ] Source URL or reference present and accessible
- [ ] Timestamp accurate to capture moment (ISO 8601 format)
- [ ] Content preserves original context (no truncation unless intentional)
- [ ] Author/creator identified (if applicable)
- [ ] Content type correctly classified (quote/concept/reference/reflection/question/observation)
- [ ] Classification confidence score ≥ 0.7 (or flagged for manual review)
- [ ] No personally identifiable information without consent
- [ ] Character encoding preserved for non-ASCII content (emoji, special characters)
- [ ] Surrounding context captured (paragraph before/after for highlights)
- [ ] Initial tags assigned (if using tag-based workflow)

**Pass Criteria:** All required items checked (items 1, 2, 3, 5, 7, 8, 10)

**Usage:** Run automatically during `create-inbox-note` task

---

### 5.2 Organization Quality Checklists

#### Checklist: atomicity-checklist.md

**Purpose:** Validate note meets Zettelkasten atomic principles

**Items:**

- [ ] Note contains exactly one complete knowledge building block
- [ ] Building block type correctly identified (concept/argument/model/question/claim/phenomenon)
- [ ] Core claim clearly stated in 1-2 sentences
- [ ] No tangled ideas requiring fragmentation
- [ ] Evidence supports core claim without introducing new claims
- [ ] Related concepts linked but not explained in detail (external links instead)
- [ ] Source attribution complete and accurate
- [ ] Note title is descriptive and unique within vault
- [ ] Note is self-contained (can be understood without extensive context)
- [ ] No orphaned content (all paragraphs relate to core claim)

**Pass Criteria:** All items checked

**Usage:** Run by Structural Analysis Agent during `analyze-atomicity` task

---

#### Checklist: linking-quality-checklist.md

**Purpose:** Ensure bidirectional links are meaningful and appropriate

**Items:**

- [ ] Link represents genuine conceptual relationship (not just keyword overlap)
- [ ] Link type identified (supports, contradicts, elaborates, analogous_to, etc.)
- [ ] Context sentence explains why link exists
- [ ] Link bidirectional (present in both notes)
- [ ] No duplicate links (same target linked multiple times)
- [ ] Link strength appropriate (strong links for core relationships, weak for tangential)
- [ ] Links don't create circular reasoning (A links to B links to C links back to A without adding new information)
- [ ] Temporal relationship recorded in Neo4j (when link was discovered)
- [ ] User approved link (if not in Yolo mode)

**Pass Criteria:** All items checked

**Usage:** Run by Semantic Linker Agent during `create-bidirectional-link` task

---

### 5.3 Synthesis Quality Checklists

#### Checklist: moc-completeness-checklist.md

**Purpose:** Validate Map of Content comprehensiveness

**Items:**

- [ ] All major subtopics in domain represented
- [ ] No orphaned notes in domain (all connected to MOC)
- [ ] Hierarchical structure logical (2-3 levels maximum)
- [ ] Section summaries accurately represent constituent notes
- [ ] Bridge paragraphs explain connections between sections
- [ ] Core concepts clearly defined with links
- [ ] Emerging questions identified (research gaps noted)
- [ ] Dataview queries functional (if used for dynamic content)
- [ ] MOC bidirectionally linked to constituent notes
- [ ] Temporal metadata recorded (MOC creation and updates tracked)
- [ ] Maturity level appropriate (nascent/developing/established/comprehensive)

**Pass Criteria:** All required items checked (items 1, 2, 3, 4, 5, 6, 9, 10)

**Usage:** Run by MOC Constructor Agent during `create-moc-structure` task

---

### 5.4 Retrieval Quality Checklists

#### Checklist: query-completeness-checklist.md

**Purpose:** Ensure query results comprehensively address user question

**Items:**

- [ ] Query intent correctly interpreted (factual/temporal/causal/comparative)
- [ ] All key concepts from query addressed in results
- [ ] Temporal context provided (for queries with temporal intent)
- [ ] Multiple perspectives included (if applicable)
- [ ] Contradictions explicitly flagged (if present)
- [ ] Source attribution included for all claims
- [ ] Confidence levels provided for uncertain claims
- [ ] Related concepts surfaced (without overwhelming user)
- [ ] Knowledge gaps identified (where query can't be fully answered)
- [ ] Suggested follow-up queries provided
- [ ] Results presented in format appropriate to query (narrative, list, comparison table, timeline)

**Pass Criteria:** All required items checked (items 1, 2, 6, 7, 8, 9)

**Usage:** Run by Query Interpreter Agent after `merge-results` task

---

### 5.5 Creation Quality Checklists

#### Checklist: brief-completeness-checklist.md

**Purpose:** Validate content brief provides adequate context for creation

**Items:**

- [ ] Topic clearly defined and scoped
- [ ] Core arguments identified with supporting notes
- [ ] Evidence compiled with full attribution
- [ ] Counterarguments anticipated and addressed
- [ ] Temporal context provided (if relevant)
- [ ] Unique angles identified (novel connections or insights)
- [ ] Research gaps clearly flagged
- [ ] Citation manifest complete (all source notes listed)
- [ ] Audience considerations documented
- [ ] Tone and style guidance provided
- [ ] Length target specified
- [ ] Deadline noted (if applicable)
- [ ] Logical outline or structure suggested

**Pass Criteria:** All required items checked (items 1, 2, 3, 8, 9, 11)

**Usage:** Run by Content Brief Agent after `organize-materials` task

---

### 5.6 Review Quality Checklists

#### Checklist: audit-coverage-checklist.md

**Purpose:** Ensure audit comprehensively reviews all quality dimensions

**Items:**

- [ ] Temporal freshness checked (notes not updated in threshold period)
- [ ] External links validated (broken, redirected, timeout)
- [ ] Source citations verified (completeness and accuracy)
- [ ] Orphaned notes identified (no incoming or outgoing links)
- [ ] Factual claims spot-checked against sources
- [ ] Duplicate content detected
- [ ] Atomicity violations flagged
- [ ] MOC coverage assessed (all domains have MOCs)
- [ ] Metadata completeness verified
- [ ] Neo4j temporal data integrity checked
- [ ] Audit scope clearly defined and respected
- [ ] Priority rankings justified

**Pass Criteria:** All items checked

**Usage:** Run by Quality Auditor Agent during `generate-audit-report` task

---

### 5.7 Temporal Analysis Checklists

#### Checklist: temporal-accuracy-checklist.md

**Purpose:** Validate temporal analysis accuracy

**Items:**

- [ ] All timestamps preserved from original capture through edits
- [ ] Edit history distinguishes substantive changes from formatting
- [ ] Causality relationships explicitly marked (confirmed vs. speculative)
- [ ] External influences documented (new sources, events, conversations)
- [ ] Temporal timeline chronologically accurate
- [ ] Key shifts in understanding clearly identified
- [ ] Maturation metrics calculated correctly (days in progress, edit count)
- [ ] Temporal context accessible (no overly technical language)
- [ ] Narrative flows logically from past to present
- [ ] Unresolved tensions acknowledged

**Pass Criteria:** All required items checked (items 1, 3, 5, 6, 7, 9)

**Usage:** Run by Timeline Constructor Agent after `create-chronological-narrative` task

---

### 5.8 Gap Identification Checklists

#### Checklist: gap-identification-checklist.md

**Purpose:** Ensure comprehensive gap detection

**Items:**

- [ ] All unresolved questions identified (via question markers ?, TODO, INVESTIGATE)
- [ ] Answered questions correctly excluded
- [ ] Undeveloped concepts detected (mentioned but not explained)
- [ ] Missing prerequisites identified (assumed knowledge)
- [ ] Evidence gaps found (claims without supporting sources)
- [ ] Domain boundaries distinguished from genuine gaps
- [ ] Gap types correctly classified (coverage/evidence/prerequisite/assumption)
- [ ] Gap impacts assessed (how gaps limit current work)
- [ ] Research approaches suggested for each gap
- [ ] Priority rankings justified (importance vs. feasibility)
- [ ] Blocking work identified (projects waiting on gap resolution)

**Pass Criteria:** All required items checked (items 1, 2, 4, 5, 6, 7, 9, 10)

**Usage:** Run by Gap Detector Agent during `detect-gaps` task

---

### 5.9 Publishing Quality Checklists

#### Checklist: publication-quality-checklist.md

**Purpose:** Ensure publication readiness and compliance

**Items:**

- [ ] Content accuracy verified against source notes
- [ ] All claims properly attributed (citations complete)
- [ ] Target audience appropriately served (language, depth, examples)
- [ ] No private information exposed (privacy markers respected)
- [ ] External links tested and current
- [ ] Wikilinks converted to target format correctly
- [ ] Bibliography complete and formatted correctly
- [ ] Content versioned (version number assigned)
- [ ] Reversion path documented (how to update KB from publication insights)
- [ ] Compliance requirements met (privacy, permissions, licensing)
- [ ] Target format rendering tested (no broken layouts)
- [ ] Publication manifest created (provenance documented)

**Pass Criteria:** All required items checked (items 1, 2, 3, 4, 5, 6, 7, 10, 11, 12)

**Usage:** Run by Publication Formatter Agent before finalizing publication

---

## 6. Workflow Specifications

### 6.1 End-to-End Knowledge Lifecycle Workflow

**Workflow Name:** `knowledge-lifecycle-workflow`

**Purpose:** Orchestrate complete knowledge journey from capture through publication

**Phases:**

**Phase 1: Capture (Inbox Triage Agent)**

- User captures content via web clipper, highlights, voice notes
- Inbox Triage Agent classifies content type
- Creates inbox note in Obsidian
- Creates CaptureEvent node in Neo4j
- **Exit Criteria:** Inbox note created with metadata

**Phase 2: Organization (Structural Analysis + Semantic Linker)**

- Structural Analysis Agent analyzes inbox note for atomicity
- Fragments if necessary into atomic notes
- Semantic Linker Agent queries Smart Connections for related notes
- Suggests bidirectional links
- User approves links
- **Exit Criteria:** Atomic notes created and linked

**Phase 3: Synthesis (MOC Constructor)**

- Triggered when domain reaches critical mass (e.g., 10+ notes)
- MOC Constructor Agent analyzes domain coverage
- Creates or updates MOC
- Generates summaries and bridge paragraphs
- **Exit Criteria:** MOC created or updated

**Phase 4: Periodic Review (Quality Auditor + Gap Detector)**

- Scheduled monthly or quarterly
- Quality Auditor Agent runs comprehensive audit
- Gap Detector Agent identifies research opportunities
- **Exit Criteria:** Audit report and prioritized gap list created

**Phase 5: Creation (Content Brief + Publication Formatter)**

- User initiates creation project
- Content Brief Agent gathers relevant context
- User creates content using brief
- Publication Formatter Agent prepares publication
- **Exit Criteria:** Publication ready and manifest created

**Phase 6: Temporal Analysis (Timeline Constructor)**

- Ad-hoc or scheduled (e.g., annual review)
- Timeline Constructor Agent builds evolution narrative
- **Exit Criteria:** Temporal narrative created

---

### 6.2 Daily Capture & Processing Workflow

**Workflow Name:** `daily-capture-processing-workflow`

**Purpose:** Routine workflow for daily knowledge work

**Schedule:** Daily (morning and evening)

**Morning Routine:**

1. Inbox Triage Agent: Process overnight captures (web clipper, reading highlights)
2. Semantic Linker Agent: Review pending link suggestions (5-10 minutes)
3. Query Interpreter Agent: Surface relevant notes for day's work

**Evening Routine:**

1. Inbox Triage Agent: Process day's captures (meeting notes, insights, voice memos)
2. Quality Auditor Agent: Quick freshness check (any critical notes aging out?)
3. Timeline Constructor Agent: Update daily log (optional, for journaling users)

**Duration:** 15-20 minutes total (morning + evening)

---

### 6.3 Weekly Review Workflow

**Workflow Name:** `weekly-review-workflow`

**Purpose:** Weekly maintenance and synthesis

**Schedule:** Weekly (e.g., Sunday evening)

**Steps:**

1. **Quality Auditor Agent:** Run weekly audit
   - Check for broken links
   - Identify stale notes (domain-critical notes only)
   - Report orphaned notes

2. **Semantic Linker Agent:** Batch process link suggestions
   - Review accumulated suggestions
   - Accept/reject in batch

3. **MOC Constructor Agent:** Update active MOCs
   - Refresh dynamic Dataview queries
   - Add newly-created notes to relevant MOCs

4. **Gap Detector Agent:** Identify emerging patterns
   - What questions came up this week?
   - What domains saw growth?

5. **Timeline Constructor Agent:** Weekly reflection (optional)
   - Narrative of week's knowledge work
   - Key insights captured

**Duration:** 30-45 minutes

---

### 6.4 Monthly Deep Review Workflow

**Workflow Name:** `monthly-deep-review-workflow`

**Purpose:** Comprehensive maintenance and strategic planning

**Schedule:** Monthly (e.g., last Sunday of month)

**Steps:**

1. **Quality Auditor Agent:** Comprehensive audit
   - All quality dimensions (freshness, links, citations, orphans)
   - Generate audit report with action items

2. **Gap Detector Agent:** Strategic gap analysis
   - Review all identified gaps
   - Prioritize research opportunities
   - Create research queue for next month

3. **Timeline Constructor Agent:** Domain evolution analysis
   - Select 1-2 key domains
   - Build evolution narratives
   - Identify maturation patterns

4. **User Action:** Remediation
   - Address critical audit findings
   - Execute high-priority research (allocate time for next month)

5. **MOC Constructor Agent:** MOC maintenance
   - Review all active MOCs
   - Update summaries and structures
   - Archive inactive MOCs

**Duration:** 1.5-2 hours

---

### 6.5 Research-Driven Workflow (Enhanced)

> **🔬 See Research Enhancement Document**
>
> This workflow leverages the enhanced Research Coordinator Agent v2.0. For detailed adaptive strategies, tool orchestration, and quality assurance steps, see:
>
> **Document:** `bmad-obsidian-2nd-brain-research-enhancement.md`

**Workflow Name:** `research-integration-workflow`

**Purpose:** Execute external research with adaptive tool detection and integrate findings

**Trigger:** Gap identification or creation project requiring external research

**Steps:**

1. **Gap Detector Agent:** Define research scope
   - What questions need answering?
   - What sources are appropriate?
   - What depth of research is needed? (quick/medium/comprehensive)
   - Estimated effort?

2. **Research Coordinator Agent (optional):** Detect and profile tools
   - **NEW:** Automatically scan for available MCP research tools
   - **NEW:** Profile tool capabilities (Perplexity, WebSearch, Context7, etc.)
   - **NEW:** Recommend tool installation if gaps detected
   - **NEW:** Select optimal research strategy based on tools

3. **Research Coordinator Agent:** Execute research (Adaptive)
   - **If Tools Available (Automated):**
     - Generate 10-25 optimized queries for detected tools
     - Execute parallel/sequential research across tools
     - Assess source credibility (0-100 scoring)
     - Synthesize multi-source findings with conflict resolution
     - Create comprehensive research report
   - **If Tools Unavailable (Manual):**
     - Generate copy/paste queries for manual research
     - User conducts research externally
     - Import findings via structured interview

4. **Research Coordinator Agent:** Quality assurance
   - **NEW:** Cross-validate findings across sources
   - **NEW:** Identify conflicts and contradictions
   - **NEW:** Assign confidence levels (high/medium/low/unverified)
   - **NEW:** Flag low-confidence findings for manual review
   - Assess overall research completeness

5. **Research Coordinator Agent:** Integration preparation
   - **NEW:** Identify atomic concepts in findings
   - **NEW:** Prepare for note creation with source attribution
   - **NEW:** Track research provenance for Neo4j

6. **Structural Analysis Agent:** Create atomic notes from research
   - Fragment research report into atomic notes
   - Preserve source citations in frontmatter
   - Integrate into vault

7. **Semantic Linker Agent:** Link research to existing knowledge
   - Query Smart Connections for related notes
   - Suggest connections to existing notes
   - Update MOCs with new insights

8. **Research Coordinator Agent:** Track provenance
   - **NEW:** Create Neo4j ResearchProject node
   - **NEW:** Link to tools used, sources consulted, notes created
   - **NEW:** Enable queries like "What research informed this note?"

9. **Gap Detector Agent:** Mark gap as resolved
   - Update gap status
   - Verify success criteria met
   - Record resolution method (automated/manual/import)

**Duration:**

- Automated (with tools): 15-30 minutes for comprehensive research
- Manual workflow: 1-10 hours depending on research scope
- Time savings: 50-70% when tools available

**Quality Metrics:**

- Average source credibility ≥ 75 (Reliable+)
- Cross-validated claims ≥ 95%
- Unresolved conflicts < 5%
- Completeness score ≥ 80/100

**See Enhancement Document for:**

- Detailed task execution algorithms
- Tool detection and profiling procedures
- Query optimization strategies
- Source credibility scoring rubric
- Multi-source synthesis with conflict resolution
- Provenance tracking implementation

---

### 6.6 Creation Project Workflow

**Workflow Name:** `creation-project-workflow`

**Purpose:** Use knowledge base to create external content

**Trigger:** User initiates creation project (article, presentation, etc.)

**Steps:**

1. **Content Brief Agent:** Prepare creation context
   - Query relevant notes (semantic search)
   - Query temporal context (evolution of key concepts)
   - Organize materials into outline
   - Identify research gaps
   - Generate brief document

2. **Gap Detector Agent:** Assess completeness (if brief has gaps)
   - Prioritize missing information
   - Suggest research approach

3. **Research Coordinator Agent (optional):** Fill gaps
   - Execute targeted research for missing information
   - Integrate findings

4. **User:** Create content using brief
   - Write/present/code using organized materials
   - Track which notes and concepts are used

5. **Content Brief Agent:** Track usage
   - Record which notes were used
   - Create Neo4j CreativeOutput node
   - Link used notes to output

6. **Publication Formatter Agent:** Prepare for publication (if applicable)
   - Convert wikilinks to target format
   - Generate bibliography
   - Check privacy compliance
   - Create publication manifest

7. **User:** Publish content

8. **Feedback Loop (optional):** Update knowledge base
   - What insights emerged during creation?
   - Were any assumptions challenged?
   - New connections discovered?
   - Update relevant notes with creation insights

**Duration:** Varies (hours to weeks depending on project scope)

---

### 6.7 Temporal Analysis Workflow

**Workflow Name:** `temporal-evolution-analysis-workflow`

**Purpose:** Understand how ideas and understanding have evolved

**Trigger:** Annual review, domain maturation, or ad-hoc curiosity

**Steps:**

1. **User:** Select concept or domain for analysis

2. **Timeline Constructor Agent:** Query temporal events
   - Retrieve all captures, edits, promotions, links for concept
   - Order chronologically

3. **Timeline Constructor Agent:** Identify evolution phases
   - Initial capture phase
   - Development phase (rapid edits)
   - Maturation phase (promotion to evergreen)
   - Maintenance phase (occasional updates)

4. **Timeline Constructor Agent:** Analyze shifts
   - What changed understanding at each phase?
   - What triggered shifts? (new sources, contradictions, synthesis)

5. **Timeline Constructor Agent:** Generate narrative
   - Create temporal narrative document
   - Include timeline visualization
   - Document unresolved tensions

6. **User:** Reflect on evolution
   - What patterns emerge?
   - How has thinking changed?
   - What influenced changes?

7. **Optional:** Create synthesis note
   - Meta-note about evolution process
   - Insights about how you think
   - Patterns in how understanding develops

**Duration:** 30-60 minutes per concept

---

### 6.8 Contradiction Resolution Workflow

**Workflow Name:** `contradiction-resolution-workflow`

**Purpose:** Identify and resolve contradictory claims

**Trigger:** Automated by Semantic Linker Agent or manual user investigation

**Steps:**

1. **Semantic Linker Agent:** Detect contradiction
   - Identify logically incompatible claims
   - Flag in Neo4j with Contradiction node

2. **Timeline Constructor Agent:** Investigate temporal context
   - Which claim came first?
   - Has understanding evolved?
   - Is one claim superseded?

3. **User:** Examine contradiction
   - Read both notes in full context
   - Assess which claim is more reliable
   - Determine resolution strategy:
     - **Refine definition:** Ambiguity in terminology
     - **Gather evidence:** More research needed
     - **Accept paradox:** Both claims valid in different contexts
     - **Update understanding:** One claim is outdated

4. **Structural Analysis Agent:** Implement resolution
   - If refining definition: Create clarification note
   - If gathering evidence: Create gap analysis
   - If accepting paradox: Create synthesis note explaining context-dependence
   - If updating: Mark old claim as superseded in Neo4j

5. **Semantic Linker Agent:** Update relationships
   - Create `[:SUPERSEDES]` relationship if applicable
   - Link resolution note to contradiction
   - Mark contradiction as resolved

**Duration:** 15-30 minutes per contradiction

---

## 7. Data/Knowledge Base Requirements

### 7.1 Core Knowledge Bases

#### KB: bmad-kb.md (Inherited from Core)

**Purpose:** Core BMAD methodology and framework principles

**Content:** (Inherited from bmad-core/data/bmad-kb.md)

**Usage:** Referenced by all agents for understanding BMAD framework conventions

---

#### KB: second-brain-methodologies.md

**Purpose:** Comprehensive guide to 2nd brain methodologies

**Content:**

- **Zettelkasten Method:**
  - History and principles (Niklas Luhmann)
  - Atomic notes definition and building blocks (6 types)
  - Atomicity as outcome vs. input requirement
  - Fleeting → Literature → Permanent note workflow
  - Unique identifiers and linking conventions

- **PARA Method:**
  - Projects, Areas, Resources, Archives taxonomy
  - Actionability-based organization
  - Information lifecycle management
  - Project vs. Area distinction
  - Migration patterns (Resource → Project → Archive)

- **Linking Your Thinking (LYT):**
  - Maps of Content (MOCs) principles
  - Home notes and navigational structures
  - MOC emergence patterns (top-down vs. bottom-up)
  - Five levels of MOC maturity

- **Johnny Decimal:**
  - Numeric organization system (00-99.00-99 format)
  - Stability through numeric IDs
  - Integration with folder hierarchies
  - Portability across systems

- **Progressive Summarization:**
  - Layered distillation (Layers 0-4)
  - Opportunistic processing
  - Visual distinction techniques (bold, highlight)
  - Executive summary creation

- **Evergreen Notes:**
  - Concept-oriented organization
  - Living, evolving notes
  - Writing for future self
  - Connection pressure

- **CODE Workflow:**
  - Capture → Organize → Distill → Express
  - Phase transitions and feedback loops

**Usage:** Reference for agents implementing methodology-specific features

---

#### KB: obsidian-technical-guide.md

**Purpose:** Technical details of Obsidian ecosystem

**Content:**

- **Obsidian Architecture:**
  - Vault structure (folders, files, hidden files)
  - Markdown format and Obsidian extensions
  - Wikilink syntax (`[[note]]`, `[[note|display]]`, `[[note#section]]`)
  - Tag syntax (#tag, #nested/tag)
  - Frontmatter (YAML metadata)
  - Dataview query language basics

- **Smart Connections:**
  - `.smart-env/` directory structure
  - Embedding model: BGE-micro-v2 specifications
  - `.ajson` format (Annotated JSON)
  - Semantic search API
  - Performance characteristics (10,000+ notes)
  - Local-first privacy architecture
  - Integration with Smart Chat

- **Community Plugins:**
  - Templater: Template with dynamic content
  - Dataview: Query vault as database
  - Local REST API: HTTP access to vault
  - MCP Tools: Model Context Protocol integration
  - Periodic Notes: Daily, weekly, monthly, yearly notes

- **Obsidian MCP Server:**
  - Installation and configuration
  - File operations (create, read, update, delete)
  - Search operations (text, tag, metadata)
  - Graph queries (backlinks, outgoing links, orphans)

**Usage:** Technical reference for agents interfacing with Obsidian

---

#### KB: neo4j-graphiti-guide.md

**Purpose:** Technical details of Neo4j and Graphiti MCP

**Content:**

- **Neo4j Fundamentals:**
  - Graph database concepts (nodes, relationships, properties)
  - Cypher query language basics
  - Indexing and performance optimization
  - Data persistence and backup
  - Neo4j Desktop vs. Aura Cloud

- **Graphiti Architecture:**
  - Bi-temporal tracking (4 timestamps: created_at, expired_at, valid_at, invalid_at)
  - Episodic memory model
  - Entity and relationship extraction
  - Automatic contradiction detection
  - Invalidation agent behavior

- **Temporal Queries:**
  - Time-travel queries (as-of date)
  - Validity window queries
  - Change detection queries
  - Influence and causality queries
  - Maturation metrics calculations

- **Schema Design:**
  - Node types: Note, CaptureEvent, Date, Source, MOC, Concept, Contradiction
  - Relationship types: CAPTURED_AT, EDITED_AT, LINKED_TO, CONCEPTUALLY_RELATED, SYNTHESIZED_IN, INFLUENCED, SUPERSEDES, CONTRADICTS
  - Property standards (timestamps, confidence scores, metadata)

- **Graphiti MCP Server:**
  - Installation via Docker or Python
  - Environment configuration (.env files)
  - OpenAI API requirements (entity extraction)
  - MCP tool endpoints (add_episode, get_episodes, search_facts)
  - Performance considerations

**Usage:** Technical reference for agents interfacing with Neo4j/Graphiti

---

#### KB: mcp-protocol-guide.md

**Purpose:** Model Context Protocol integration patterns

**Content:**

- **MCP Fundamentals:**
  - Protocol specification overview
  - Server-client architecture
  - Tool discovery and invocation
  - Resource management
  - Prompt engineering for MCP tools

- **Available MCP Servers:**
  - Obsidian MCP Tools: Vault operations
  - Neo4j MCP: Graph database queries
  - Smart Connections MCP: Semantic search
  - WebSearch MCP: External research
  - Perplexity MCP: Deep research queries
  - Context7 MCP: Documentation lookup

- **Integration Patterns:**
  - Multi-server orchestration
  - Error handling and retries
  - Rate limiting and throttling
  - Result caching strategies
  - Authentication and security

- **Agent-MCP Coordination:**
  - Which agents use which MCP servers
  - Tool selection logic
  - Fallback strategies (server unavailable)
  - Parallel vs. sequential tool calls

**Usage:** Reference for understanding how agents coordinate via MCP

---

#### KB: knowledge-graph-patterns.md

**Purpose:** Common patterns in personal knowledge graphs

**Content:**

- **Relationship Types:**
  - Supports: Note A provides evidence for Note B
  - Contradicts: Note A conflicts with Note B
  - Elaborates: Note A explains Note B in detail
  - Analogous_to: Note A structurally similar to Note B
  - Generalizes: Note A is broader case of Note B
  - Specializes: Note A is specific instance of Note B
  - Influences: Note A influenced creation/revision of Note B

- **Graph Metrics:**
  - Node centrality (most-linked notes)
  - Clustering coefficient (densely connected subgraphs)
  - Shortest paths (conceptual distance)
  - PageRank (note importance)
  - Community detection (natural knowledge domains)

- **Evolution Patterns:**
  - Rapid development: Many edits in short timeframe
  - Stable maturation: Edits slow, note promoted to evergreen
  - Conceptual splits: One note fragments into multiple
  - Synthesis: Multiple notes merge into MOC
  - Paradigm shifts: Core assumption changes, cascading updates

- **Anti-Patterns:**
  - Link bombing: Excessive linking reduces signal
  - Circular reasoning: A→B→C→A with no external support
  - Orphaned clusters: Disconnected knowledge islands
  - Stale evergreens: "Evergreen" notes that haven't been touched in years
  - Tag proliferation: Too many overlapping tags

**Usage:** Reference for agents analyzing and building knowledge graphs

---

### 7.2 Methodology-Specific Knowledge Bases

#### KB: zettelkasten-implementation.md

**Purpose:** Detailed guide to implementing Zettelkasten in Obsidian

**Content:**

- Atomic note structure templates
- Unique identifier schemes (timestamp, sequential, hybrid)
- Literature note workflow
- Fleeting note capture patterns
- Progressive note maturation
- Index notes vs. structure notes vs. hub notes
- Common Zettelkasten pitfalls and solutions

**Usage:** Reference for Structural Analysis Agent, atomic note validation

---

#### KB: para-implementation.md

**Purpose:** Detailed guide to implementing PARA in Obsidian

**Content:**

- Folder structure conventions
- Project lifecycle (active → complete → archive)
- Area of responsibility identification
- Resource organization strategies
- Archive management (when to archive, how to search archives)
- Integration with daily notes and periodic reviews
- PARA + Zettelkasten hybrid patterns

**Usage:** Reference for organization workflows, inbox processing

---

### 7.3 Quality Assurance Knowledge Bases

#### KB: quality-standards.md

**Purpose:** Define quality criteria for knowledge base content

**Content:**

- **Accuracy Standards:**
  - All factual claims must have sources
  - Claims should have confidence levels (high/medium/low)
  - Outdated information should be marked as superseded

- **Completeness Standards:**
  - Atomic notes must be self-contained
  - MOCs must cover all notes in domain
  - Temporal records must have complete timestamps

- **Consistency Standards:**
  - Terminology usage consistent across vault
  - Metadata formatting standardized
  - Link types clearly distinguished

- **Freshness Standards:**
  - Critical domain notes reviewed every 3 months
  - Evergreen notes reviewed annually
  - Stale notes (6+ months) flagged for review

- **Attribution Standards:**
  - All quotes must have source
  - Paraphrased content should cite source
  - Synthesis notes should reference constituent notes

**Usage:** Reference for Quality Auditor Agent

---

## 8. Integration Specifications

### 8.1 Obsidian MCP Tools Integration

**MCP Server:** `obsidian-mcp-tools`
**Protocol:** MCP via Local REST API
**Repository:** https://github.com/jacksteamdev/obsidian-mcp-tools

**Required Obsidian Plugins:**

- Local REST API (community plugin)
- MCP Tools (community plugin)

**Configuration:**

```json
{
  "mcpServers": {
    "obsidian-mcp-tools": {
      "command": "/path/to/vault/.obsidian/plugins/obsidian-mcp-tools/bin/mcp-server",
      "args": [],
      "env": {
        "OBSIDIAN_REST_API_KEY": "${OBSIDIAN_API_KEY}",
        "OBSIDIAN_REST_API_URL": "http://localhost:27123"
      }
    }
  }
}
```

**Available Tools:**

- `obsidian.create_note` - Create new note with frontmatter
- `obsidian.read_note` - Read note content
- `obsidian.update_note` - Update existing note
- `obsidian.delete_note` - Delete note (move to trash)
- `obsidian.search_notes` - Text/tag/metadata search
- `obsidian.get_backlinks` - Get incoming links
- `obsidian.get_outgoing_links` - Get outgoing links
- `obsidian.list_notes` - List notes matching criteria
- `obsidian.create_folder` - Create directory
- `obsidian.move_note` - Move note to different folder

**Usage by Agents:**

- Inbox Triage Agent: `create_note`, `create_folder`
- Structural Analysis Agent: `read_note`, `create_note`, `update_note`
- Semantic Linker Agent: `read_note`, `update_note`, `get_backlinks`, `get_outgoing_links`
- MOC Constructor Agent: `create_note`, `search_notes`, `list_notes`
- Quality Auditor Agent: `list_notes`, `get_backlinks`, `read_note`
- Publication Formatter Agent: `read_note`, `list_notes`, `search_notes`

**Error Handling:**

- API key invalid: Prompt user to reconfigure
- REST API unreachable: Check if Obsidian is running
- Note not found: Return error, suggest search
- Permission denied: Check vault permissions

---

### 8.2 Smart Connections MCP Integration

**MCP Server:** `smart-connections-mcp` (via MCP Tools plugin)
**Protocol:** MCP
**Embedding Model:** BGE-micro-v2 (local)

**Configuration:**

- Smart Connections plugin must be installed and active
- `.smart-env/` directory must exist (automatically created)
- Initial vault indexing required (happens automatically on first plugin activation)

**Available Tools:**

- `smart_connections.semantic_search` - Query by semantic similarity
- `smart_connections.get_embedding` - Retrieve note embedding vector
- `smart_connections.get_similar_notes` - Find N most similar notes
- `smart_connections.update_embeddings` - Reindex specific notes (after edits)

**Usage by Agents:**

- Semantic Linker Agent: `semantic_search`, `get_similar_notes`
- Query Interpreter Agent: `semantic_search`
- Content Brief Agent: `semantic_search`, `get_similar_notes`
- Gap Detector Agent: `get_similar_notes` (find related notes to gaps)

**Performance Considerations:**

- Semantic search latency: ~100-500ms for typical vaults (1,000-10,000 notes)
- Embedding generation: ~50ms per note (on-demand for new notes)
- Full reindex: ~1-5 minutes for 10,000 notes (rare, only on version updates)
- `.ajson` file size: ~1-2KB per note (total ~10-20MB for 10,000 notes)

**Error Handling:**

- Embeddings not initialized: Trigger reindex
- Embedding model not found: Reinstall Smart Connections plugin
- Search timeout: Reduce max results, try simpler query

---

### 8.3 Neo4j Graphiti MCP Integration

**MCP Server:** `graphiti-mcp-server`
**Protocol:** MCP
**Repository:** https://github.com/getzep/graphiti

**Deployment Options:**

**Option 1: Docker (Recommended)**

```yaml
# docker-compose.yml
version: '3.8'
services:
  neo4j:
    image: neo4j:5.15
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
      - NEO4J_PLUGINS=["apoc"]
    ports:
      - '7474:7474' # HTTP
      - '7687:7687' # Bolt
    volumes:
      - neo4j_data:/data

  graphiti-mcp:
    image: getzep/graphiti-mcp:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - NEO4J_DATABASE=neo4j
    ports:
      - '8080:8080'
    depends_on:
      - neo4j

volumes:
  neo4j_data:
```

**Option 2: Python (Local Development)**

```bash
pip install graphiti-core
python -m graphiti_mcp_server
```

**Configuration (claude_desktop_config.json):**

```json
{
  "mcpServers": {
    "graphiti": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "graphiti-mcp-server-graphiti-mcp-1",
        "python",
        "-m",
        "graphiti_mcp_server"
      ],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "${NEO4J_PASSWORD}"
      }
    }
  }
}
```

**Available Tools:**

- `graphiti.add_episode` - Create episodic memory node
- `graphiti.get_episodes` - Retrieve episodes by time range or query
- `graphiti.search_facts` - Search facts with temporal filters
- `graphiti.add_entity` - Create entity node
- `graphiti.add_relation` - Create relationship between entities
- `graphiti.query_temporal` - Execute custom Cypher with temporal awareness
- `graphiti.detect_contradictions` - Run contradiction detection

**Usage by Agents:**

- Inbox Triage Agent: `add_episode` (for captures)
- Semantic Linker Agent: `add_relation` (for discovered links)
- MOC Constructor Agent: `add_entity` (for MOCs), `search_facts`
- Timeline Constructor Agent: `query_temporal`, `get_episodes`
- Query Interpreter Agent: `search_facts`, `query_temporal`

**Schema Design:**

**Node Types:**

```cypher
(:Note {
  id: string,
  title: string,
  obsidian_path: string,
  created: datetime,
  last_updated: datetime,
  status: string,  // working, refined, established
  type: string,  // atomic_note, moc, inbox, etc.
  building_block_type: string  // concept, argument, model, etc.
})

(:CaptureEvent {
  id: string,
  timestamp: datetime,
  source: string,
  url: string,
  content_type: string
})

(:MOC {
  id: string,
  domain: string,
  created: datetime,
  last_updated: datetime,
  maturity_level: string  // nascent, developing, established, comprehensive
})

(:Source {
  url: string,
  author: string,
  title: string,
  accessed: datetime
})

(:Date {
  iso: string,  // YYYY-MM-DD
  year: integer,
  month: integer,
  day: integer
})

(:Contradiction {
  id: string,
  created: datetime,
  detection_method: string,
  resolved: boolean,
  resolution_strategy: string
})

(:CreativeOutput {
  id: string,
  type: string,
  published: datetime,
  url: string
})
```

**Relationship Types:**

```cypher
(:Note)-[:CAPTURED_AT {timestamp}]->(:CaptureEvent)
(:CaptureEvent)-[:CAPTURED_FROM]->(:Source)
(:CaptureEvent)-[:CAPTURED_ON]->(:Date)

(:Note)-[:EDITED_AT {timestamp, change_type}]->(:Date)
(:Note)-[:PROMOTED_AT {timestamp}]->(:Date)

(:Note)-[:LINKED_TO {
  created_at: datetime,
  strength: float,  // 0.0-1.0
  link_type: string  // supports, contradicts, elaborates, etc.
}]->(:Note)

(:Note)-[:CONCEPTUALLY_RELATED {
  discovered_at: datetime,
  strength: float,
  discovery_method: string  // semantic_embedding, temporal_proximity, etc.
}]->(:Note)

(:Note)-[:SYNTHESIZED_IN {timestamp}]->(:MOC)
(:MOC)-[:CONTAINS]->(:Note)

(:Note)-[:INFLUENCED {
  influence_date: datetime,
  influence_type: string  // direct_citation, inspired_by, triggered_revision
}]->(:Note)

(:Note)-[:ASSERTS_CLAIM]->(:Claim)
(:Claim)-[:CONTRADICTS]->(:Claim)
(:Contradiction)-[:INVOLVES]->(:Note)

(:Note)-[:CITES]->(:Source)

(:Note)-[:USED_IN]->(:CreativeOutput)
```

**Temporal Query Patterns:**

**Evolution Timeline:**

```cypher
MATCH (note:Note {title: $concept})
MATCH (note)-[captured:CAPTURED_AT]->(capture_date:Date)
OPTIONAL MATCH (note)-[edited:EDITED_AT]->(edit_dates:Date)
OPTIONAL MATCH (note)-[promoted:PROMOTED_AT]->(promo_date:Date)
RETURN note.title,
       captured.timestamp as first_capture,
       collect(edited.timestamp) as edit_history,
       promoted.timestamp as promoted_to_evergreen,
       duration.inDays(captured.timestamp, promoted.timestamp).days as maturation_days
```

**Relationship Strength Over Time:**

```cypher
MATCH (n1:Note)-[r:CONCEPTUALLY_RELATED]->(n2:Note)
WHERE n1.title = $note_title
RETURN n2.title,
       r.strength,
       r.discovered_at,
       r.discovery_method
ORDER BY r.discovered_at DESC
```

**Temporal Contradiction Detection:**

```cypher
MATCH (note1:Note)-[:ASSERTS_CLAIM]->(claim1:Claim)
MATCH (note2:Note)-[:ASSERTS_CLAIM]->(claim2:Claim)
WHERE claim1.contradicts = claim2.id
  AND note1.last_updated < note2.last_updated
RETURN note1.title as older_note,
       note2.title as newer_note,
       claim1.statement as older_claim,
       claim2.statement as newer_claim,
       note2.last_updated as when_contradiction_emerged
```

**Error Handling:**

- Neo4j connection failed: Check if Docker containers running
- OpenAI API error: Verify API key, check quota
- Cypher syntax error: Validate query, provide error context
- Transaction timeout: Reduce query scope, add limits

---

### 8.4 Optional: Web Research MCP Integration

> **📚 See Research Enhancement Document**
>
> The Research Coordinator Agent has been enhanced with adaptive tool detection and intelligent orchestration. For complete tool integration specifications, optimization patterns, and query strategies, see:
>
> **Document:** `bmad-obsidian-2nd-brain-research-enhancement.md`
>
> - Tool Detection & Profiling specifications
> - Query Optimization Patterns for each tool
> - Multi-Tool Orchestration strategies
> - Complete tool catalog with capabilities matrix

**MCP Servers:** `web-search-mcp`, `perplexity-mcp`, `context7-mcp`

**Usage:** Optional for Research Coordinator Agent (auto-detected on activation)

**Configuration (if available):**

```json
{
  "mcpServers": {
    "web-search": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-web-search"],
      "env": {
        "SEARCH_API_KEY": "${GOOGLE_SEARCH_API_KEY}"
      }
    },
    "perplexity": {
      "command": "npx",
      "args": ["-y", "@perplexity/mcp-server"],
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      }
    },
    "context7": {
      "// Note": "Usually included with Claude Code/Cursor/Windsurf"
    }
  }
}
```

**Available Tools:**

- `mcp__web_search__search` - Execute web search query
- `mcp__perplexity__search` - Quick search with Sonar Pro (2-5s response)
- `mcp__perplexity__reason` - Complex multi-step reasoning (10-30s response)
- `mcp__perplexity__deep_research` - Comprehensive research queries (30-90s response)
- `mcp__context7__resolve-library-id` - Find library in documentation database
- `mcp__context7__get-library-docs` - Fetch official library documentation

**Adaptive Behavior:**

- **Automatic Detection:** Research Coordinator Agent scans for available tools on activation
- **Tool Profiling:** Analyzes capabilities and generates optimization recommendations
- **Query Optimization:** Generates tool-specific queries for maximum accuracy
- **Multi-Tool Orchestration:** Coordinates parallel/sequential execution across tools
- **Graceful Degradation:** Falls back to manual workflows if tools unavailable

**Usage by Research Coordinator Agent:**

- Detect available research tools automatically
- Generate optimized queries for detected tools (10-25 per topic)
- Execute automated research with parallel/sequential strategies
- Assess source credibility (0-100 evidence-based scoring)
- Synthesize findings from multiple sources with conflict resolution
- Import findings into knowledge base as atomic notes
- Track research provenance in Neo4j

**Fallback:** If not available, agent provides copy/paste queries for manual research

**See Enhancement Document** for:

- Complete tool catalog with capability matrices
- Query optimization patterns for each tool
- Credibility scoring rubric (0-100)
- Research strategy decision trees

---

## 9. Implementation Roadmap

### Phase 1: MVP (Minimum Viable Product)

**Goal:** Core capture, organization, and retrieval workflows functional

**Duration:** 4-6 weeks

**Deliverables:**

1. **Core Agents (5 required):**
   - Inbox Triage Agent
   - Structural Analysis Agent
   - Semantic Linker Agent
   - Query Interpreter Agent
   - Quality Auditor Agent

2. **Essential Tasks (15):**
   - Capture: classify-content-type, extract-metadata, create-inbox-note, create-capture-event
   - Organization: analyze-atomicity, fragment-note, query-semantic-similarity, create-bidirectional-link
   - Retrieval: parse-natural-language-query, execute-obsidian-query, execute-neo4j-query, merge-results
   - Review: audit-temporal-freshness, validate-external-links, generate-audit-report

3. **Essential Templates (5):**
   - inbox-note-tmpl.yaml
   - atomic-note-tmpl.yaml
   - moc-tmpl.yaml (basic)
   - query-result-tmpl.yaml
   - audit-report-tmpl.yaml (basic)

4. **Essential Checklists (5):**
   - capture-quality-checklist.md
   - atomicity-checklist.md
   - linking-quality-checklist.md
   - query-completeness-checklist.md
   - audit-coverage-checklist.md

5. **Essential Workflows (3):**
   - knowledge-lifecycle-workflow (basic)
   - daily-capture-processing-workflow
   - weekly-review-workflow

6. **Essential Knowledge Bases (3):**
   - bmad-kb.md (inherited)
   - second-brain-methodologies.md (focused on Zettelkasten + PARA)
   - obsidian-technical-guide.md (basics)

7. **Essential Integrations (2):**
   - Obsidian MCP Tools (file operations, search)
   - Smart Connections MCP (semantic search)

**Acceptance Criteria:**

- User can capture content via web clipper → inbox note created
- Inbox note can be analyzed and fragmented into atomic notes
- Semantic similarity queries return relevant results
- Bidirectional links can be created
- Natural language queries return results from both Obsidian and Neo4j (if configured)
- Weekly audit can be run and produces actionable report

---

### Phase 2: Enhanced Synthesis & Temporal Analysis

**Goal:** MOC construction and temporal evolution tracking

**Duration:** 3-4 weeks

**Deliverables:**

1. **Additional Agents (2):**
   - MOC Constructor Agent
   - Timeline Constructor Agent

2. **Additional Tasks (10):**
   - Synthesis: create-moc-structure, generate-summaries, write-bridge-paragraphs, update-moc-temporal-record
   - Temporal: query-temporal-events, retrieve-edit-history, identify-evolution-periods, create-chronological-narrative, analyze-concept-maturation, generate-timeline-visualization

3. **Additional Templates (3):**
   - moc-tmpl.yaml (complete)
   - temporal-narrative-tmpl.yaml
   - link-suggestion-tmpl.yaml

4. **Additional Checklists (3):**
   - moc-completeness-checklist.md
   - temporal-accuracy-checklist.md
   - narrative-completeness-checklist.md

5. **Additional Workflows (2):**
   - monthly-deep-review-workflow
   - temporal-evolution-analysis-workflow

6. **Enhanced Knowledge Bases:**
   - neo4j-graphiti-guide.md (complete)
   - knowledge-graph-patterns.md

7. **Enhanced Integrations:**
   - Neo4j Graphiti MCP (temporal queries, episodic memory)

**Acceptance Criteria:**

- MOCs can be created from domain notes
- MOCs include summaries and bridge paragraphs
- Temporal evolution narratives can be generated for concepts
- Timeline visualizations created (ASCII or Mermaid)
- Monthly deep review workflow completes successfully

---

### Phase 3: Creation & Publishing

**Goal:** Use knowledge base for content creation and publication

**Duration:** 3-4 weeks

**Deliverables:**

1. **Additional Agents (2):**
   - Content Brief Agent
   - Publication Formatter Agent

2. **Additional Tasks (10):**
   - Creation: query-relevant-notes, query-temporal-context, organize-materials, identify-research-gaps, extract-quotable-passages, track-content-usage
   - Publishing: extract-publication-content, convert-wikilinks, generate-bibliography, check-privacy-compliance

3. **Additional Templates (2):**
   - content-brief-tmpl.yaml
   - publication-manifest-tmpl.yaml

4. **Additional Checklists (2):**
   - brief-completeness-checklist.md
   - publication-quality-checklist.md

5. **Additional Workflows (2):**
   - creation-project-workflow
   - (feedback loop integration into knowledge-lifecycle-workflow)

**Acceptance Criteria:**

- Content briefs can be generated from knowledge base
- Briefs include organized materials, quotable passages, and research gaps
- Publications can be formatted for different targets (HTML, PDF, Markdown)
- Wikilinks correctly converted
- Bibliography auto-generated
- Publication manifest tracks provenance

---

### Phase 4: Advanced Analysis & Gap Detection

**Goal:** Knowledge gap identification and research prioritization

**Duration:** 2-3 weeks

**Deliverables:**

1. **Additional Agents (1):**
   - Gap Detector Agent

2. **Additional Tasks (7):**
   - Gap detection: identify-unresolved-questions, detect-undeveloped-concepts, find-missing-prerequisites, identify-evidence-gaps, analyze-domain-boundaries, prioritize-gaps
   - Cross-linking: detect-logical-contradictions

3. **Additional Templates (1):**
   - gap-analysis-tmpl.yaml

4. **Additional Checklists (2):**
   - gap-identification-checklist.md
   - prioritization-checklist.md

5. **Additional Workflows (1):**
   - contradiction-resolution-workflow

6. **Enhanced Knowledge Bases:**
   - quality-standards.md (complete)

**Acceptance Criteria:**

- Unresolved questions automatically identified
- Knowledge gaps prioritized by strategic value
- Research approaches suggested for each gap
- Contradictions detected and flagged
- Contradiction resolution workflow functional

---

### Phase 5: Optional Research Integration (Enhanced)

> **🔬 ENHANCED SPECIFICATION**
>
> This phase has been significantly enhanced with adaptive research capabilities. See the complete specification in:
>
> **Document:** `bmad-obsidian-2nd-brain-research-enhancement.md`

**Goal:** Adaptive, intelligent external research with automatic tool detection and optimization

**Duration:** 3-4 weeks (increased from 2-3 due to enhancements)

**Deliverables:**

1. **Optional Agent (1) - Enhanced:**
   - **Research Coordinator Agent v2.0** (Enhanced with adaptive capabilities)
     - Automatic MCP tool detection and profiling
     - Adaptive query generation (10-30 queries per topic)
     - Multi-tool orchestration (parallel/sequential/hybrid)
     - Evidence-based source credibility scoring (0-100)
     - Multi-source synthesis with conflict resolution
     - Complete Neo4j provenance tracking

2. **Additional Tasks (19 total) - See Enhancement Doc:**
   - **Tool Detection (4 tasks):**
     - detect-research-tools.md
     - profile-tool-capabilities.md
     - recommend-research-tools.md
     - monitor-tool-availability.md
   - **Query Generation (4 tasks):**
     - generate-research-queries.md
     - generate-deep-questions.md
     - optimize-query-for-tool.md
     - categorize-queries.md
   - **Execution (5 tasks):**
     - execute-automated-research.md
     - execute-parallel-research.md
     - execute-sequential-research.md
     - execute-targeted-research.md
     - execute-fallback-research.md
   - **Source Evaluation (3 tasks):**
     - assess-source-credibility.md
     - validate-research-accuracy.md
     - identify-research-conflicts.md
   - **Synthesis & Integration (3 tasks):**
     - synthesize-multi-source-findings.md
     - integrate-research-findings.md
     - track-research-provenance.md

3. **Additional Templates (7 total) - See Enhancement Doc:**
   - research-report-tmpl.yaml (comprehensive documentation)
   - tool-detection-report-tmpl.yaml (discovered tools)
   - research-query-set-tmpl.yaml (organized queries)
   - source-assessment-tmpl.yaml (credibility evaluation)
   - research-synthesis-tmpl.yaml (multi-source merger)
   - research-conflict-tmpl.yaml (contradiction identification)
   - research-provenance-tmpl.yaml (Neo4j tracking)

4. **Additional Checklists (5 total) - See Enhancement Doc:**
   - research-quality-checklist.md
   - source-credibility-checklist.md
   - tool-optimization-checklist.md (NEW)
   - research-synthesis-checklist.md (NEW)
   - research-accuracy-checklist.md (NEW)

5. **Additional Knowledge Bases (6 total) - See Enhancement Doc:**
   - research-tools-catalog.md (MCP tool reference)
   - research-methodologies.md
   - source-evaluation-criteria.md
   - query-optimization-patterns.md (NEW - tool-specific templates)
   - research-strategy-patterns.md (NEW - workflow decision trees)
   - credibility-scoring-rubric.md (NEW - 0-100 scoring framework)

6. **Additional Workflows (1):**
   - research-integration-workflow (with adaptive strategies)

7. **Optional Integrations (Auto-Detected):**
   - Perplexity MCP (search/reason/deep_research)
   - WebSearch MCP
   - Context7 MCP
   - Custom research MCP servers

**Acceptance Criteria:**

- ✓ Tool detection automatically scans MCP environment on activation
- ✓ Tool profiling generates capability reports and recommendations
- ✓ Research queries optimized for detected tools (10-25 per topic)
- ✓ Deep questions generated for comprehensive research (20-30 per topic)
- ✓ Automated research executed with parallel/sequential strategies
- ✓ Source credibility assessed with 0-100 evidence-based scoring
- ✓ Multi-source synthesis with conflict resolution (<5% unresolved)
- ✓ Manual research findings imported and structured (fallback workflow)
- ✓ Research reports comprehensive with citations and provenance
- ✓ Research integrated as atomic notes with MOC updates
- ✓ Complete provenance tracked in Neo4j temporal graph
- ✓ Quality metrics achieved: 75+ avg credibility, >95% accuracy
- ✓ Graceful degradation to manual workflows when tools unavailable

**Success Metrics:**

- 50-70% time savings vs. manual research (when tools available)
- Average source credibility score ≥ 75 (Reliable+)
- Research accuracy >95% (cross-validated claims)
- Tool utilization appropriateness ≥ 90%
- User research confidence ≥ 85%

**See Enhancement Document** (`bmad-obsidian-2nd-brain-research-enhancement.md`) for:

- Complete task specifications with adaptive algorithms
- Template structures and field definitions
- Checklist items and validation criteria
- Knowledge base content outlines
- Tool catalog with optimization patterns
- Credibility scoring rubric details
- Implementation guidance

---

### Phase 6: Polish & Documentation

**Goal:** Complete documentation, optimization, and user onboarding

**Duration:** 2-3 weeks

**Deliverables:**

1. **Documentation:**
   - Complete README.md with quickstart
   - Comprehensive user guide
   - Installation instructions (Obsidian setup, Neo4j setup, MCP configuration)
   - Troubleshooting guide
   - FAQ
   - Video tutorials (optional)

2. **Optimization:**
   - Agent prompt refinement based on usage
   - Task optimization for performance
   - Template improvements
   - Checklist validation

3. **Testing:**
   - Integration testing across all workflows
   - Performance testing (large vaults: 10,000+ notes)
   - Edge case testing (empty vault, corrupted data, offline mode)
   - User acceptance testing with beta testers

4. **Additional Knowledge Bases:**
   - Methodology-specific guides (zettelkasten-implementation.md, para-implementation.md)
   - MCP protocol guide (mcp-protocol-guide.md)

**Acceptance Criteria:**

- All documentation complete and tested
- Onboarding workflow functional (from installation to first capture)
- Performance acceptable (queries < 3 seconds, captures < 1 second)
- Edge cases handled gracefully
- Beta user feedback incorporated

---

## 10. Success Metrics

### 10.1 Adoption Metrics

- **Installation Rate:** Number of users who complete installation
- **Activation Rate:** % of users who complete first capture → organization → retrieval cycle
- **Retention Rate:** % of users still active after 30 days
- **Agent Usage Distribution:** Which agents are used most frequently?

### 10.2 Quality Metrics

- **Note Quality:**
  - % of notes meeting atomicity standards
  - Average links per note (target: 3-5 for dense graphs)
  - % of notes with complete source attribution

- **Knowledge Base Health:**
  - Vault health score (composite: freshness, linking, citation completeness)
  - % of notes orphaned (target: <5%)
  - % of broken external links (target: <2%)

- **Temporal Coverage:**
  - % of notes with temporal metadata (captures, edits, promotions)
  - Average concept maturation time (capture → evergreen)
  - % of contradictions resolved

### 10.3 Productivity Metrics

- **Capture Efficiency:**
  - Time from capture to inbox note creation (target: <30 seconds)
  - Classification accuracy (target: >90%)

- **Retrieval Speed:**
  - Query response time (target: <3 seconds)
  - Query success rate (% of queries returning relevant results, target: >85%)

- **Creation Impact:**
  - % of creative outputs using content briefs
  - Time saved using briefs vs. manual research (estimated)

### 10.4 User Satisfaction Metrics

- **Net Promoter Score (NPS):** Likelihood to recommend (target: >50)
- **Feature Satisfaction:** Rating of each agent (1-5 stars)
- **Support Ticket Volume:** Number of issues requiring support
- **Feature Requests:** Top requested enhancements

---

## 11. Open Questions & Decisions Required

### 11.1 Technical Decisions

**Q1:** Should Neo4j be required or optional?

- **Option A:** Required (enables full temporal analysis)
- **Option B:** Optional (allow Obsidian-only mode with degraded temporal features)
- **Recommendation:** Optional, with clear feature comparison

**Q2:** How to handle large vaults (50,000+ notes)?

- **Option A:** Vault partitioning (split into multiple vaults by domain)
- **Option B:** Advanced indexing and caching strategies
- **Option C:** Hybrid (Smart Connections for semantic, external vector DB for scale)
- **Recommendation:** Start with Option B, document Option A for extreme cases

**Q3:** Should agents support multiple languages (i18n)?

- **Option A:** English only initially
- **Option B:** Multi-language from start
- **Recommendation:** English only for MVP, plan i18n architecture for Phase 6

### 11.2 User Experience Decisions

**Q4:** How should agents be activated?

- **Option A:** Slash commands (`/BMad:obsidian-2nd-brain:inbox-triage-agent`)
- **Option B:** Simplified slash commands (`/inbox-triage`)
- **Option C:** Mode switching (activate expansion pack, then use short commands)
- **Recommendation:** Option C (cleaner, less cognitive load)

**Q5:** Should agents auto-run periodic tasks (audits, reviews)?

- **Option A:** Fully manual (user triggers all tasks)
- **Option B:** Scheduled prompts (agent asks "want to run weekly review?")
- **Option C:** Fully automated (silent background tasks with reports)
- **Recommendation:** Option B (user control with convenience)

**Q6:** How to handle Yolo Mode across agents?

- **Option A:** Global Yolo Mode (all agents auto-approve)
- **Option B:** Per-agent Yolo Mode (fine-grained control)
- **Option C:** Per-task Yolo Mode (even finer control)
- **Recommendation:** Option B (balance between granularity and simplicity)

### 11.3 Integration Decisions

**Q7:** Should expansion pack include Obsidian plugin setup?

- **Option A:** Expansion pack assumes plugins installed (user responsibility)
- **Option B:** Expansion pack includes automated plugin installer
- **Option C:** Expansion pack includes manual plugin setup guide
- **Recommendation:** Option C (avoid fragility of automation)

**Q8:** How to handle MCP server failures?

- **Option A:** Fail gracefully with degraded functionality
- **Option B:** Prompt user to fix issue immediately
- **Option C:** Queue operations for retry when server returns
- **Recommendation:** Combination (Option A with Option B prompt)

---

## 12. Risk Assessment

### 12.1 Technical Risks

**Risk 1: Obsidian API Changes**

- **Impact:** High (could break all Obsidian integrations)
- **Probability:** Low (Obsidian API relatively stable)
- **Mitigation:** Use community-maintained MCP Tools plugin (active maintenance)

**Risk 2: Neo4j Performance Degradation at Scale**

- **Impact:** High (temporal queries become unusably slow)
- **Probability:** Medium (graphs with 100,000+ relationships)
- **Mitigation:** Implement caching, query optimization, partitioning strategies

**Risk 3: Smart Connections Embedding Model Changes**

- **Impact:** Medium (semantic search quality affected)
- **Probability:** Low (BGE-micro-v2 is stable)
- **Mitigation:** Support multiple embedding models, provide migration path

**Risk 4: MCP Protocol Evolution**

- **Impact:** Medium (integration patterns may need updates)
- **Probability:** Medium (MCP is relatively new)
- **Mitigation:** Follow MCP specification updates, use stable API versions

### 12.2 User Experience Risks

**Risk 5: Complexity Overwhelms Users**

- **Impact:** High (users abandon system)
- **Probability:** High (10 agents, 25+ tasks, 3 integrations)
- **Mitigation:**
  - Provide guided onboarding (start with 3 core agents)
  - Offer "modes" (Simple, Balanced, Advanced)
  - Comprehensive documentation and tutorials

**Risk 6: Workflow Friction**

- **Impact:** High (users revert to simpler tools)
- **Probability:** Medium (multi-step workflows can feel tedious)
- **Mitigation:**
  - Optimize for common workflows (capture → organize in one flow)
  - Yolo Mode for power users
  - Keyboard shortcuts and automation

**Risk 7: Data Lock-In Perception**

- **Impact:** Medium (users hesitate to invest time)
- **Probability:** Low (Obsidian is markdown, Neo4j is exportable)
- **Mitigation:**
  - Emphasize data portability (plain markdown, standard formats)
  - Provide export utilities
  - Document migration paths

### 12.3 Adoption Risks

**Risk 8: Insufficient Differentiation**

- **Impact:** High (users don't see value vs. plain Obsidian)
- **Probability:** Medium (temporal RAG is novel but abstract)
- **Mitigation:**
  - Create compelling demos (show evolution analysis)
  - Highlight unique capabilities (temporal queries, contradiction detection)
  - Provide before/after examples

**Risk 9: Installation Barriers**

- **Impact:** High (users don't complete setup)
- **Probability:** High (Neo4j Docker setup can be intimidating)
- **Mitigation:**
  - Offer Obsidian-only mode (Neo4j optional)
  - Provide one-click installers where possible
  - Video tutorials for complex steps

---

## 13. Future Enhancements (Post-V1.0)

### 13.1 Advanced Features

**Enhancement 1: Collaborative Knowledge Graphs**

- Multi-user Neo4j access with permissions
- Shared vaults with private/public note designations
- Conflict resolution for concurrent edits

**Enhancement 2: AI-Powered Insights**

- Automated pattern detection ("You frequently link X and Y, consider creating a MOC")
- Predictive gap identification (based on creation patterns, suggest likely next research)
- Anomaly detection (unusual linking patterns, potential errors)

**Enhancement 3: Visual Knowledge Graphs**

- Interactive graph visualization (D3.js, Cytoscape)
- Temporal animation (show graph evolution over time)
- Force-directed layouts with custom physics

**Enhancement 4: Mobile Support**

- Obsidian mobile app integration
- Voice capture workflows
- Offline synchronization

**Enhancement 5: Enhanced Temporal Queries**

- Natural language temporal queries ("What did I know about X in June?")
- Comparative timelines ("Compare evolution of concept A vs. B")
- Trend detection ("Which domains are growing fastest?")

### 13.2 Methodology Expansions

**Enhancement 6: Additional Methodology Support**

- BASB (Building a Second Brain) - full CODE workflow automation
- Johnny Decimal - numeric organization system
- Andy Matuschak's Evergreen Notes - focused on evergreen promotion workflow
- Slip-box (physical Zettelkasten analog)

**Enhancement 7: Domain-Specific Workflows**

- Academic research workflow (literature reviews, citation management)
- Creative writing workflow (character notes, world-building, plot tracking)
- Project management workflow (project notes, task tracking, retrospectives)

### 13.3 Integration Expansions

**Enhancement 8: Additional MCP Integrations**

- Zotero MCP: Academic citation management
- Readwise MCP: Highlight import automation
- Calendar MCP: Event and meeting note integration
- Email MCP: Email-to-note capture

**Enhancement 9: External Tool Integrations**

- Notion import/export
- Roam Research import
- Logseq compatibility
- Anki flashcard generation (spaced repetition)

---

## 14. Appendices

### Appendix A: Glossary

**Atomic Note:** Note containing exactly one complete knowledge building block (concept, argument, model, question, claim, or phenomenon)

**Bidirectional Link:** Wikilink present in both source and target notes, creating reciprocal relationship

**Bi-temporal Tracking:** Recording both transaction time (when data entered system) and validity time (when fact was true in real world)

**Building Block:** Fundamental unit of knowledge (concept, argument, model, question, claim, phenomenon)

**Episodic Memory:** Memory of specific events or experiences, stored as episodes with temporal metadata

**Evergreen Note:** Mature, stable note that has been promoted from working status, representing refined understanding

**Graphiti:** Temporal knowledge graph system with built-in contradiction detection and bi-temporal tracking

**Map of Content (MOC):** Curated collection of links serving as navigational hub and thinking tool for knowledge domain

**MCP (Model Context Protocol):** Protocol for connecting AI models to external tools and data sources

**Smart Connections:** Obsidian plugin providing semantic search via local embeddings

**Temporal Narrative:** Chronological story of how concept or understanding evolved over time

**Wikilink:** Obsidian link syntax `[[target]]` creating connection between notes

**Zettelkasten:** Note-taking method emphasizing atomic notes and bidirectional linking

---

### Appendix B: File Structure

**Expansion Pack Directory Structure:**

```
bmad-obsidian-2nd-brain/
├── agents/
│   ├── inbox-triage-agent.md
│   ├── structural-analysis-agent.md
│   ├── semantic-linker-agent.md
│   ├── moc-constructor-agent.md
│   ├── query-interpreter-agent.md
│   ├── timeline-constructor-agent.md
│   ├── content-brief-agent.md
│   ├── quality-auditor-agent.md
│   ├── gap-detector-agent.md
│   ├── publication-formatter-agent.md
│   └── research-coordinator-agent.md (optional)
├── tasks/
│   ├── capture/
│   │   ├── classify-content-type.md
│   │   ├── extract-metadata.md
│   │   ├── create-inbox-note.md
│   │   └── create-capture-event.md
│   ├── organization/
│   │   ├── analyze-atomicity.md
│   │   ├── fragment-note.md
│   │   ├── query-semantic-similarity.md
│   │   └── create-bidirectional-link.md
│   ├── synthesis/
│   │   ├── create-moc-structure.md
│   │   ├── generate-summaries.md
│   │   └── write-bridge-paragraphs.md
│   ├── retrieval/
│   │   ├── parse-natural-language-query.md
│   │   ├── execute-obsidian-query.md
│   │   ├── execute-neo4j-query.md
│   │   └── merge-results.md
│   ├── creation/
│   │   ├── query-relevant-notes.md
│   │   ├── organize-materials.md
│   │   └── track-content-usage.md
│   ├── review/
│   │   ├── audit-temporal-freshness.md
│   │   ├── validate-external-links.md
│   │   ├── detect-orphaned-notes.md
│   │   └── generate-audit-report.md
│   ├── temporal/
│   │   ├── query-temporal-events.md
│   │   ├── create-chronological-narrative.md
│   │   └── analyze-concept-maturation.md
│   ├── gap-detection/
│   │   ├── identify-unresolved-questions.md
│   │   ├── prioritize-gaps.md
│   │   └── detect-logical-contradictions.md
│   └── publishing/
│       ├── extract-publication-content.md
│       ├── convert-wikilinks.md
│       └── check-privacy-compliance.md
├── templates/
│   ├── inbox-note-tmpl.yaml
│   ├── atomic-note-tmpl.yaml
│   ├── moc-tmpl.yaml
│   ├── temporal-narrative-tmpl.yaml
│   ├── link-suggestion-tmpl.yaml
│   ├── audit-report-tmpl.yaml
│   ├── gap-analysis-tmpl.yaml
│   ├── content-brief-tmpl.yaml
│   └── publication-manifest-tmpl.yaml
├── checklists/
│   ├── capture-quality-checklist.md
│   ├── atomicity-checklist.md
│   ├── linking-quality-checklist.md
│   ├── moc-completeness-checklist.md
│   ├── query-completeness-checklist.md
│   ├── brief-completeness-checklist.md
│   ├── audit-coverage-checklist.md
│   ├── temporal-accuracy-checklist.md
│   ├── gap-identification-checklist.md
│   └── publication-quality-checklist.md
├── workflows/
│   ├── knowledge-lifecycle-workflow.yaml
│   ├── daily-capture-processing-workflow.yaml
│   ├── weekly-review-workflow.yaml
│   ├── monthly-deep-review-workflow.yaml
│   ├── research-integration-workflow.yaml
│   ├── creation-project-workflow.yaml
│   ├── temporal-evolution-analysis-workflow.yaml
│   └── contradiction-resolution-workflow.yaml
├── data/
│   ├── bmad-kb.md (inherited from core)
│   ├── second-brain-methodologies.md
│   ├── obsidian-technical-guide.md
│   ├── neo4j-graphiti-guide.md
│   ├── mcp-protocol-guide.md
│   ├── knowledge-graph-patterns.md
│   ├── zettelkasten-implementation.md
│   ├── para-implementation.md
│   └── quality-standards.md
├── config.yaml
├── README.md
├── CHANGELOG.md
└── docs/
    ├── installation-guide.md
    ├── user-guide.md
    ├── troubleshooting.md
    ├── faq.md
    └── examples/
        ├── example-capture-flow.md
        ├── example-temporal-analysis.md
        └── example-creation-workflow.md
```

---

### Appendix C: Config File

**File:** `bmad-obsidian-2nd-brain/config.yaml`

```yaml
# BMAD Obsidian 2nd Brain Expansion Pack Configuration
name: bmad-obsidian-2nd-brain
version: 1.0.0
short-title: Obsidian 2nd Brain with Temporal RAG
description: >
  Comprehensive personal knowledge management system for Obsidian with multi-modal
  temporal RAG architecture. Combines semantic search (Smart Connections) with
  temporal graph database (Neo4j + Graphiti MCP) for tracking knowledge evolution.
  Supports Zettelkasten, PARA, LYT, and other 2nd brain methodologies. Includes
  10 specialized agents for capture, organization, synthesis, retrieval, creation,
  review, temporal analysis, cross-linking, gap detection, and publishing.
author: BMAD Team
slashPrefix: bmad-2b

# Vault directory structure configuration
vault:
  inbox: inbox
  archive: archive
  mocs: mocs
  daily_notes: daily-notes
  periodic_reviews: reviews

# Neo4j configuration (optional)
neo4j:
  enabled: true # Set to false for Obsidian-only mode
  uri: bolt://localhost:7687
  database: neo4j
  # Authentication set via environment variables:
  # NEO4J_USER, NEO4J_PASSWORD

# Obsidian plugin requirements
required_plugins:
  - name: local-rest-api
    required: true
    purpose: MCP server communication
  - name: smart-connections
    required: true
    purpose: Semantic search and embeddings
  - name: mcp-tools
    required: true
    purpose: MCP integration
  - name: templater
    required: false
    purpose: Enhanced template automation
  - name: dataview
    required: false
    purpose: Dynamic MOC queries

# Optional MCP servers
optional_mcp_servers:
  - name: web-search
    purpose: External research automation
  - name: perplexity
    purpose: Deep research queries
  - name: context7
    purpose: Documentation lookup

# Agent configurations
agents:
  yolo_mode_default: false
  auto_link_threshold: 0.8
  max_link_suggestions: 10

# Quality thresholds
quality:
  freshness_threshold_days: 180
  link_density_target: 3.5
  orphan_rate_target: 0.05

# Temporal settings
temporal:
  capture_timestamp_format: iso8601
  maturation_threshold_days: 30
  edit_history_retention: all
```

---

### Appendix D: Installation Checklist

**Pre-Installation Requirements:**

- [ ] Obsidian installed (v1.4.0+)
- [ ] Claude Desktop or Claude Code installed (for IDE use)
- [ ] Node.js installed (v16+) (for some MCP servers)
- [ ] Docker installed (optional, for Neo4j)
- [ ] Git installed (for cloning repositories)

**Obsidian Plugin Installation:**

- [ ] Install Local REST API plugin
- [ ] Configure Local REST API (copy API key)
- [ ] Install Smart Connections plugin
- [ ] Enable Smart Connections (wait for initial indexing)
- [ ] Install MCP Tools plugin
- [ ] Run MCP Tools "Install Server" command
- [ ] Verify `.obsidian/plugins/obsidian-mcp-tools/bin/mcp-server` exists

**Neo4j Setup (Optional but Recommended):**

- [ ] Install Neo4j Desktop OR Docker
- [ ] Create new database instance
- [ ] Set secure password
- [ ] Start database
- [ ] Verify accessible at `http://localhost:7474` (browser interface)
- [ ] Note Bolt URL: `bolt://localhost:7687`

**Graphiti MCP Server Setup (Optional but Recommended):**

- [ ] Clone graphiti-mcp-server repository OR install via pip
- [ ] Create `.env` file with:
  - OPENAI_API_KEY
  - NEO4J_URI
  - NEO4J_USER
  - NEO4J_PASSWORD
- [ ] Start Graphiti MCP server (Docker or Python)
- [ ] Verify server running

**Claude Configuration:**

- [ ] Locate Claude config file:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- [ ] Add Obsidian MCP server configuration
- [ ] Add Graphiti MCP server configuration (if using Neo4j)
- [ ] Restart Claude Desktop/Code
- [ ] Verify MCP tools appear in tool list

**BMAD Expansion Pack Installation:**

- [ ] Install BMAD-METHOD core (if not already installed)
- [ ] Install bmad-obsidian-2nd-brain expansion pack:
  ```bash
  npx bmad-method install
  # Select "Obsidian 2nd Brain with Temporal RAG"
  ```
- [ ] Verify `.bmad-obsidian-2nd-brain/` directory created
- [ ] Verify agents, tasks, templates, checklists, workflows, data present

**Verification:**

- [ ] Activate Inbox Triage Agent: `/bmad-2b:inbox-triage-agent`
- [ ] Test capture: `*capture "test capture" "manual"`
- [ ] Verify inbox note created in `/inbox`
- [ ] Verify Neo4j CaptureEvent node created (if using Neo4j)
- [ ] Activate Semantic Linker Agent
- [ ] Test semantic search: `*suggest-links {note_id}`
- [ ] Verify suggestions returned

**Troubleshooting:**

- If agents don't activate: Check `.bmad-obsidian-2nd-brain/` installation
- If Obsidian operations fail: Check Local REST API running, verify API key
- If semantic search fails: Check Smart Connections indexed vault, check `.smart-env/` exists
- If Neo4j operations fail: Check Docker containers running, verify Bolt connection
- If MCP tools not visible: Restart Claude, check config file JSON syntax

---

## 15. Conclusion

This requirements document provides a comprehensive specification for building a BMAD expansion pack that transforms Obsidian into a powerful second brain with temporal awareness. By combining semantic search (Smart Connections) with temporal graph database (Neo4j + Graphiti MCP), the system enables knowledge workers to not only store and retrieve information but to understand how their thinking evolves over time.

### Key Innovations

1. **Temporal RAG Architecture:** First personal knowledge management system to combine semantic search with bi-temporal graph database, enabling queries like "how has my understanding evolved?"

2. **Multi-Agent Orchestration:** 10 specialized agents coordinate across both static (Obsidian) and dynamic (Neo4j) knowledge layers, providing comprehensive knowledge lifecycle support.

3. **Methodology Agnostic:** Supports Zettelkasten, PARA, LYT, Johnny Decimal, and Progressive Summarization, allowing users to adopt their preferred methodology without lock-in.

4. **Quality Assurance:** 20+ checklists ensure knowledge base maintains high standards for accuracy, completeness, freshness, and coherence.

5. **Creation Support:** Content Brief Agent and Publication Formatter Agent bridge the gap between personal knowledge base and public content creation.

### Next Steps

1. **Phase 1 Development:** Implement MVP (core capture, organization, retrieval) - 4-6 weeks
2. **Beta Testing:** Recruit 10-20 beta users for feedback - 2-3 weeks
3. **Iterative Refinement:** Address beta feedback, optimize workflows - 2-3 weeks
4. **Phase 2-6 Development:** Enhanced features (synthesis, temporal analysis, creation, gaps, research) - 12-15 weeks
5. **Public Release:** Announce v1.0 with comprehensive documentation

### Success Criteria

- **Adoption:** 100+ active users within 3 months of release
- **Retention:** 70%+ retention rate at 30 days
- **Quality:** 90%+ notes meeting atomic standards, <5% orphaned notes
- **Satisfaction:** NPS > 50

---

**Document Status:** Final Draft
**Version:** 1.0
**Date:** 2025-11-04
**Review Required:** Technical review (feasibility), User experience review (workflows), Integration review (MCP protocols)
**Approval Required:** BMAD-METHOD maintainers

---

**End of Requirements Document**

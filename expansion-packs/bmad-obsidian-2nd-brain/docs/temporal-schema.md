# Temporal Schema Design

This document describes the Neo4j graph database schema used for temporal knowledge tracking in the Obsidian 2nd Brain system.

## Overview

The temporal schema tracks how knowledge evolves over time by modeling:
- **When notes are captured** (capture events with timestamps)
- **How notes are edited** (edit history with timestamps)
- **How notes are connected** (bidirectional links with confidence scores)
- **Where knowledge comes from** (source citations)

This enables powerful temporal queries like:
- "What did I capture last week about machine learning?"
- "Show me how my understanding of React evolved over the past 6 months"
- "Find notes that were captured together but not yet linked"

## Schema Diagram

```
┌─────────────────┐           ┌──────────────────┐
│  CaptureEvent   │◄──────────│      Note        │
│                 │ CAPTURED_AT│                  │
│  - timestamp    │            │  - title         │
│  - source_url   │            │  - path          │
│  - method       │            │  - created_at    │
└────────┬────────┘            │  - content_hash  │
         │                     └────────┬─────────┘
         │ ON_DATE                      │ LINKED_TO
         │                              │ (confidence)
         ▼                              │
   ┌──────────┐                         │
   │   Date   │                         ▼
   │          │                    ┌─────────┐
   │ - date   │                    │  Note   │
   │ - year   │                    └─────────┘
   │ - month  │
   │ - day    │
   └──────────┘                         │ CITES
                                        │
                                        ▼
                                   ┌─────────┐
                                   │ Source  │
                                   │         │
                                   │ - url   │
                                   │ - title │
                                   │ - type  │
                                   └─────────┘
```

---

## Node Types

### Note

Represents an atomic note in the Obsidian vault.

**Labels:** `:Note`

**Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | String | Yes | Note title (from filename or frontmatter) |
| `path` | String | Yes | Relative path within vault (e.g., "concepts/temporal-rag.md") |
| `created_at` | DateTime | Yes | When the note was created in Obsidian |
| `content_hash` | String | No | SHA-256 hash of content for change detection |
| `note_id` | String | No | Unique identifier (UUID or generated) |
| `tags` | List<String> | No | Obsidian tags extracted from note |
| `word_count` | Integer | No | Approximate word count |
| `last_modified` | DateTime | No | Last edit timestamp |

**Constraints:**
```cypher
CREATE CONSTRAINT note_path_unique IF NOT EXISTS
FOR (n:Note) REQUIRE n.path IS UNIQUE;
```

**Indexes:**
```cypher
CREATE INDEX note_created_at IF NOT EXISTS
FOR (n:Note) ON (n.created_at);

CREATE INDEX note_title IF NOT EXISTS
FOR (n:Note) ON (n.title);

CREATE INDEX note_tags IF NOT EXISTS
FOR (n:Note) ON (n.tags);
```

**Example:**
```cypher
CREATE (n:Note {
  title: "Temporal RAG Architecture",
  path: "concepts/temporal-rag.md",
  created_at: datetime("2025-01-15T10:30:00Z"),
  content_hash: "a7f3c2b1...",
  note_id: "uuid-1234-5678",
  tags: ["ai", "architecture", "rag"],
  word_count: 487
})
```

---

### CaptureEvent

Represents a moment when knowledge was captured (created or imported).

**Labels:** `:CaptureEvent`

**Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `timestamp` | DateTime | Yes | When the capture occurred |
| `source_url` | String | No | URL of the source (if captured from web) |
| `capture_method` | String | No | How it was captured (e.g., "inbox", "import", "web-clipper") |
| `event_id` | String | Yes | Unique identifier for this event |
| `metadata` | Map | No | Additional capture metadata (JSON object) |

**Constraints:**
```cypher
CREATE CONSTRAINT capture_event_id_unique IF NOT EXISTS
FOR (e:CaptureEvent) REQUIRE e.event_id IS UNIQUE;
```

**Indexes:**
```cypher
CREATE INDEX capture_event_timestamp IF NOT EXISTS
FOR (e:CaptureEvent) ON (e.timestamp);

CREATE INDEX capture_event_method IF NOT EXISTS
FOR (e:CaptureEvent) ON (e.capture_method);
```

**Example:**
```cypher
CREATE (e:CaptureEvent {
  timestamp: datetime("2025-01-15T10:30:00Z"),
  source_url: "https://example.com/article",
  capture_method: "web-clipper",
  event_id: "capture-uuid-1234",
  metadata: {browser: "Chrome", device: "laptop"}
})
```

---

### Date

Represents a calendar date for temporal grouping and queries.

**Labels:** `:Date`

**Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `date` | Date | Yes | Full date (YYYY-MM-DD) |
| `year` | Integer | Yes | Year (e.g., 2025) |
| `month` | Integer | Yes | Month (1-12) |
| `day` | Integer | Yes | Day (1-31) |
| `day_of_week` | String | No | Day name (e.g., "Monday") |
| `week_of_year` | Integer | No | ISO week number (1-53) |

**Constraints:**
```cypher
CREATE CONSTRAINT date_unique IF NOT EXISTS
FOR (d:Date) REQUIRE d.date IS UNIQUE;
```

**Indexes:**
```cypher
CREATE INDEX date_year_month IF NOT EXISTS
FOR (d:Date) ON (d.year, d.month);
```

**Example:**
```cypher
CREATE (d:Date {
  date: date("2025-01-15"),
  year: 2025,
  month: 1,
  day: 15,
  day_of_week: "Monday",
  week_of_year: 3
})
```

**Note:** Date nodes are typically created automatically when capture events occur.

---

### Source

Represents an external source cited by notes.

**Labels:** `:Source`

**Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `url` | String | Yes | Full URL of the source |
| `title` | String | No | Source title (webpage title, book name, etc.) |
| `source_type` | String | No | Type: "webpage", "book", "paper", "video", etc. |
| `author` | String | No | Author or creator name |
| `published_date` | Date | No | When the source was published |
| `access_date` | DateTime | No | When we last accessed this source |

**Constraints:**
```cypher
CREATE CONSTRAINT source_url_unique IF NOT EXISTS
FOR (s:Source) REQUIRE s.url IS UNIQUE;
```

**Indexes:**
```cypher
CREATE INDEX source_type IF NOT EXISTS
FOR (s:Source) ON (s.source_type);
```

**Example:**
```cypher
CREATE (s:Source {
  url: "https://arxiv.org/abs/2305.00000",
  title: "Advances in Retrieval-Augmented Generation",
  source_type: "paper",
  author: "Smith et al.",
  published_date: date("2023-05-01")
})
```

---

## Relationship Types

### CAPTURED_AT

Links a Note to the CaptureEvent when it was created.

**Pattern:** `(Note)-[:CAPTURED_AT]->(CaptureEvent)`

**Properties:**
- None (relationship is directional only)

**Example:**
```cypher
MATCH (n:Note {path: "inbox/new-idea.md"})
MATCH (e:CaptureEvent {event_id: "capture-1234"})
CREATE (n)-[:CAPTURED_AT]->(e)
```

**Query: Find notes captured today**
```cypher
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE date(e.timestamp) = date()
RETURN n.title, e.timestamp
ORDER BY e.timestamp DESC
```

---

### EDITED_AT

Links a Note to a CaptureEvent representing an edit action.

**Pattern:** `(Note)-[:EDITED_AT]->(CaptureEvent)`

**Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `changes` | String | No | Summary of changes (e.g., "Added section on..." ) |
| `diff_size` | Integer | No | Number of lines changed |

**Example:**
```cypher
MATCH (n:Note {path: "concepts/rag.md"})
CREATE (edit:CaptureEvent {
  timestamp: datetime(),
  capture_method: "edit",
  event_id: "edit-uuid-5678"
})
CREATE (n)-[:EDITED_AT {changes: "Expanded temporal tracking section"}]->(edit)
```

**Query: Find notes edited in the last 7 days**
```cypher
MATCH (n:Note)-[:EDITED_AT]->(e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P7D')
RETURN n.title, e.timestamp
ORDER BY e.timestamp DESC
```

---

### LINKED_TO

Bidirectional semantic link between two notes.

**Pattern:** `(Note)-[:LINKED_TO]-(Note)`

**Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `confidence` | Float | Yes | Link strength (0.0-1.0) from semantic similarity |
| `link_type` | String | No | Type: "semantic", "explicit", "suggested" |
| `created_at` | DateTime | Yes | When the link was created |
| `created_by` | String | No | "user" or "agent-name" |

**Example:**
```cypher
MATCH (n1:Note {path: "concepts/rag.md"})
MATCH (n2:Note {path: "concepts/vector-search.md"})
CREATE (n1)-[:LINKED_TO {
  confidence: 0.85,
  link_type: "semantic",
  created_at: datetime(),
  created_by: "semantic-linker-agent"
}]-(n2)
```

**Query: Find strongly linked notes**
```cypher
MATCH (n1:Note)-[r:LINKED_TO]-(n2:Note)
WHERE r.confidence > 0.8
RETURN n1.title, n2.title, r.confidence
ORDER BY r.confidence DESC
LIMIT 20
```

---

### CITES

Links a Note to an external Source.

**Pattern:** `(Note)-[:CITES]->(Source)`

**Properties:**

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `quote` | String | No | Specific quote or excerpt |
| `page` | String | No | Page number (for books/papers) |
| `accessed_at` | DateTime | No | When the citation was added |

**Example:**
```cypher
MATCH (n:Note {path: "concepts/rag.md"})
MATCH (s:Source {url: "https://arxiv.org/abs/2305.00000"})
CREATE (n)-[:CITES {
  quote: "RAG combines retrieval with generation...",
  accessed_at: datetime()
}]->(s)
```

**Query: Find all notes citing a source**
```cypher
MATCH (n:Note)-[:CITES]->(s:Source {url: "https://example.com/article"})
RETURN n.title, n.created_at
ORDER BY n.created_at
```

---

### ON_DATE

Links a CaptureEvent to a Date node for temporal grouping.

**Pattern:** `(CaptureEvent)-[:ON_DATE]->(Date)`

**Properties:**
- None (relationship is directional only)

**Example:**
```cypher
MATCH (e:CaptureEvent {event_id: "capture-1234"})
MERGE (d:Date {date: date(e.timestamp)})
  ON CREATE SET d.year = e.timestamp.year,
                d.month = e.timestamp.month,
                d.day = e.timestamp.day
CREATE (e)-[:ON_DATE]->(d)
```

**Query: Count captures per day**
```cypher
MATCH (e:CaptureEvent)-[:ON_DATE]->(d:Date)
WHERE d.year = 2025 AND d.month = 1
RETURN d.date, count(e) AS captures
ORDER BY d.date
```

---

## Example Queries

### Temporal Queries

**Find notes captured in a date range:**
```cypher
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE e.timestamp >= datetime("2025-01-01T00:00:00Z")
  AND e.timestamp < datetime("2025-02-01T00:00:00Z")
RETURN n.title, e.timestamp
ORDER BY e.timestamp DESC
```

**Find notes captured last week:**
```cypher
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P7D')
RETURN n.title, e.timestamp, e.capture_method
ORDER BY e.timestamp DESC
```

**Track how a note evolved (edit history):**
```cypher
MATCH (n:Note {path: "concepts/rag.md"})-[:EDITED_AT]->(e:CaptureEvent)
RETURN e.timestamp, e.metadata.changes
ORDER BY e.timestamp
```

### Relationship Queries

**Find notes that should be linked (captured together):**
```cypher
MATCH (n1:Note)-[:CAPTURED_AT]->(e1:CaptureEvent)-[:ON_DATE]->(d:Date)
MATCH (n2:Note)-[:CAPTURED_AT]->(e2:CaptureEvent)-[:ON_DATE]->(d)
WHERE n1 <> n2
  AND NOT EXISTS { (n1)-[:LINKED_TO]-(n2) }
RETURN n1.title, n2.title, d.date
ORDER BY d.date DESC
LIMIT 20
```

**Find strongest semantic connections:**
```cypher
MATCH (n1:Note)-[r:LINKED_TO]-(n2:Note)
RETURN n1.title, n2.title, r.confidence
ORDER BY r.confidence DESC
LIMIT 10
```

**Find notes with most connections:**
```cypher
MATCH (n:Note)-[:LINKED_TO]-()
RETURN n.title, n.path, count(*) AS connections
ORDER BY connections DESC
LIMIT 20
```

### Source Tracking

**Find most cited sources:**
```cypher
MATCH (n:Note)-[:CITES]->(s:Source)
RETURN s.url, s.title, count(n) AS citation_count
ORDER BY citation_count DESC
LIMIT 10
```

**Find notes without sources:**
```cypher
MATCH (n:Note)
WHERE NOT EXISTS { (n)-[:CITES]->(:Source) }
RETURN n.title, n.created_at
ORDER BY n.created_at DESC
```

### Knowledge Evolution Queries

**Find stale notes (not edited in 90 days):**
```cypher
MATCH (n:Note)
OPTIONAL MATCH (n)-[:EDITED_AT]->(e:CaptureEvent)
WITH n, max(e.timestamp) AS last_edit
WHERE last_edit < datetime() - duration('P90D')
   OR last_edit IS NULL
RETURN n.title, n.path, last_edit
ORDER BY last_edit NULLS FIRST
```

**Find rapidly evolving notes (many edits):**
```cypher
MATCH (n:Note)-[:EDITED_AT]->(e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P30D')
WITH n, count(e) AS edit_count
WHERE edit_count > 5
RETURN n.title, n.path, edit_count
ORDER BY edit_count DESC
```

### Daily/Weekly Summaries

**Daily capture summary:**
```cypher
MATCH (e:CaptureEvent)-[:ON_DATE]->(d:Date {date: date()})
MATCH (n:Note)-[:CAPTURED_AT]->(e)
RETURN n.title, e.timestamp, e.capture_method
ORDER BY e.timestamp
```

**Weekly capture count by method:**
```cypher
MATCH (e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P7D')
RETURN e.capture_method, count(*) AS count
ORDER BY count DESC
```

---

## Schema Management

### Initial Schema Setup

Run these commands when first setting up Neo4j:

```cypher
// Create constraints
CREATE CONSTRAINT note_path_unique IF NOT EXISTS
FOR (n:Note) REQUIRE n.path IS UNIQUE;

CREATE CONSTRAINT capture_event_id_unique IF NOT EXISTS
FOR (e:CaptureEvent) REQUIRE e.event_id IS UNIQUE;

CREATE CONSTRAINT date_unique IF NOT EXISTS
FOR (d:Date) REQUIRE d.date IS UNIQUE;

CREATE CONSTRAINT source_url_unique IF NOT EXISTS
FOR (s:Source) REQUIRE s.url IS UNIQUE;

// Create indexes
CREATE INDEX note_created_at IF NOT EXISTS
FOR (n:Note) ON (n.created_at);

CREATE INDEX note_title IF NOT EXISTS
FOR (n:Note) ON (n.title);

CREATE INDEX note_tags IF NOT EXISTS
FOR (n:Note) ON (n.tags);

CREATE INDEX capture_event_timestamp IF NOT EXISTS
FOR (e:CaptureEvent) ON (e.timestamp);

CREATE INDEX capture_event_method IF NOT EXISTS
FOR (e:CaptureEvent) ON (e.capture_method);

CREATE INDEX date_year_month IF NOT EXISTS
FOR (d:Date) ON (d.year, d.month);

CREATE INDEX source_type IF NOT EXISTS
FOR (s:Source) ON (s.source_type);
```

### Verify Schema

```cypher
// List all constraints
SHOW CONSTRAINTS;

// List all indexes
SHOW INDEXES;

// Count nodes by label
MATCH (n)
RETURN labels(n)[0] AS label, count(n) AS count
ORDER BY count DESC;

// Count relationships by type
MATCH ()-[r]->()
RETURN type(r) AS relationship, count(r) AS count
ORDER BY count DESC;
```

### Schema Migration Strategy

When schema changes are needed:

1. **Additive changes (preferred):**
   - Add new properties to existing nodes
   - Add new node types
   - Add new relationship types
   - Use `IF NOT EXISTS` to avoid errors

2. **Non-breaking migrations:**
   ```cypher
   // Add new property with default value
   MATCH (n:Note)
   WHERE n.word_count IS NULL
   SET n.word_count = 0;
   ```

3. **Breaking changes (avoid if possible):**
   - Backup database first: `neo4j-admin database dump`
   - Apply migration in transaction
   - Verify data integrity
   - Test queries before committing

4. **Version tracking:**
   ```cypher
   // Create schema version node
   CREATE (v:SchemaVersion {
     version: "1.0.0",
     applied_at: datetime(),
     description: "Initial schema setup"
   })
   ```

---

## Performance Optimization

### Query Optimization Tips

1. **Use indexes for frequently queried properties:**
   - Always index temporal properties (`timestamp`, `created_at`)
   - Index properties used in `WHERE` clauses

2. **Limit result sets:**
   ```cypher
   // Good: Use LIMIT
   MATCH (n:Note)
   RETURN n
   LIMIT 100;
   ```

3. **Use `EXPLAIN` and `PROFILE` to analyze queries:**
   ```cypher
   EXPLAIN MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
   WHERE e.timestamp > datetime() - duration('P7D')
   RETURN n.title;
   ```

4. **Avoid cartesian products:**
   ```cypher
   // Bad: Cartesian product
   MATCH (n1:Note), (n2:Note)
   WHERE n1 <> n2

   // Good: Use relationships
   MATCH (n1:Note)-[:LINKED_TO]-(n2:Note)
   ```

### Maintenance Tasks

**Remove orphaned nodes:**
```cypher
// Find orphaned capture events (no notes)
MATCH (e:CaptureEvent)
WHERE NOT EXISTS { (:Note)-[:CAPTURED_AT|EDITED_AT]->(e) }
DELETE e;
```

**Clean up old test nodes:**
```cypher
MATCH (n:TestNode)
DELETE n;
```

**Vacuum indexes:**
```cypher
// Neo4j automatically maintains indexes, but you can rebuild if needed
DROP INDEX index_name IF EXISTS;
CREATE INDEX index_name FOR (n:Note) ON (n.property);
```

---

## Integration with Graphiti MCP

Graphiti MCP uses this schema through the following operations:

- `graphiti.add_episode` → Creates `CaptureEvent` nodes
- `graphiti.get_episodes` → Queries `CaptureEvent` by time range
- `graphiti.add_entity` → Creates `Note` nodes
- `graphiti.add_relation` → Creates `LINKED_TO` relationships

**Example Graphiti workflow:**
```javascript
// Agent captures new note
await graphiti.add_episode({
  timestamp: new Date(),
  content: "Meeting notes: Discussed RAG architecture",
  metadata: { source: "meeting", participants: ["Alice", "Bob"] }
});

// Agent links related notes
await graphiti.add_relation({
  from_entity: "note-id-1",
  to_entity: "note-id-2",
  relation_type: "LINKED_TO",
  properties: { confidence: 0.85 }
});
```

---

## References

- **Neo4j Cypher Manual:** https://neo4j.com/docs/cypher-manual/current/
- **Neo4j Data Modeling Guide:** https://neo4j.com/developer/guide-data-modeling/
- **Graphiti Documentation:** https://github.com/getzep/graphiti
- **Temporal Graphs Paper:** Lewis et al., "Temporal Knowledge Graphs" (2023)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** BMAD Development Team

// =============================================================================
// Temporal Queries for Obsidian 2nd Brain
// =============================================================================
//
// Example Cypher queries for temporal knowledge tracking.
// These queries demonstrate common patterns for working with the temporal schema.
//
// To use these queries:
// 1. Open Neo4j Browser: http://localhost:7474
// 2. Copy and paste queries into the query editor
// 3. Modify date ranges and parameters as needed
// 4. Execute with Ctrl+Enter (or Cmd+Return on macOS)
//
// Documentation: See docs/temporal-schema.md
//
// =============================================================================

// -----------------------------------------------------------------------------
// SCHEMA SETUP - Run these first to create constraints and indexes
// -----------------------------------------------------------------------------

// Create constraints (ensures data integrity)
CREATE CONSTRAINT note_path_unique IF NOT EXISTS
FOR (n:Note) REQUIRE n.path IS UNIQUE;

CREATE CONSTRAINT capture_event_id_unique IF NOT EXISTS
FOR (e:CaptureEvent) REQUIRE e.event_id IS UNIQUE;

CREATE CONSTRAINT date_unique IF NOT EXISTS
FOR (d:Date) REQUIRE d.date IS UNIQUE;

CREATE CONSTRAINT source_url_unique IF NOT EXISTS
FOR (s:Source) REQUIRE s.url IS UNIQUE;

// Create indexes (improves query performance)
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

// Verify schema setup
SHOW CONSTRAINTS;
SHOW INDEXES;

// -----------------------------------------------------------------------------
// SAMPLE DATA - Example nodes and relationships for testing
// -----------------------------------------------------------------------------

// Create sample Date nodes
MERGE (d1:Date {date: date("2025-01-15")})
  SET d1.year = 2025, d1.month = 1, d1.day = 15, d1.day_of_week = "Monday";

MERGE (d2:Date {date: date("2025-01-16")})
  SET d2.year = 2025, d2.month = 1, d2.day = 16, d2.day_of_week = "Tuesday";

// Create sample Source
MERGE (s1:Source {url: "https://arxiv.org/abs/2305.00000"})
  SET s1.title = "Advances in RAG", s1.source_type = "paper";

// Create sample CaptureEvents
MERGE (e1:CaptureEvent {event_id: "sample-capture-1"})
  SET e1.timestamp = datetime("2025-01-15T10:30:00Z"),
      e1.capture_method = "inbox",
      e1.source_url = "https://example.com/article";

MERGE (e2:CaptureEvent {event_id: "sample-capture-2"})
  SET e2.timestamp = datetime("2025-01-16T14:15:00Z"),
      e2.capture_method = "web-clipper";

// Link CaptureEvents to Dates
MATCH (e1:CaptureEvent {event_id: "sample-capture-1"}), (d1:Date {date: date("2025-01-15")})
MERGE (e1)-[:ON_DATE]->(d1);

MATCH (e2:CaptureEvent {event_id: "sample-capture-2"}), (d2:Date {date: date("2025-01-16")})
MERGE (e2)-[:ON_DATE]->(d2);

// Create sample Notes
MERGE (n1:Note {path: "concepts/rag-architecture.md"})
  SET n1.title = "RAG Architecture",
      n1.created_at = datetime("2025-01-15T10:30:00Z"),
      n1.tags = ["ai", "architecture", "rag"],
      n1.word_count = 487;

MERGE (n2:Note {path: "concepts/vector-search.md"})
  SET n2.title = "Vector Search Fundamentals",
      n2.created_at = datetime("2025-01-16T14:15:00Z"),
      n2.tags = ["ai", "search", "vectors"],
      n2.word_count = 312;

MERGE (n3:Note {path: "projects/obsidian-integration.md"})
  SET n3.title = "Obsidian Integration Plan",
      n3.created_at = datetime("2025-01-15T16:00:00Z"),
      n3.tags = ["projects", "obsidian"],
      n3.word_count = 654;

// Link Notes to CaptureEvents
MATCH (n1:Note {path: "concepts/rag-architecture.md"}), (e1:CaptureEvent {event_id: "sample-capture-1"})
MERGE (n1)-[:CAPTURED_AT]->(e1);

MATCH (n2:Note {path: "concepts/vector-search.md"}), (e2:CaptureEvent {event_id: "sample-capture-2"})
MERGE (n2)-[:CAPTURED_AT]->(e2);

// Create semantic links
MATCH (n1:Note {path: "concepts/rag-architecture.md"}), (n2:Note {path: "concepts/vector-search.md"})
MERGE (n1)-[:LINKED_TO {
  confidence: 0.87,
  link_type: "semantic",
  created_at: datetime(),
  created_by: "semantic-linker-agent"
}]-(n2);

// Create source citations
MATCH (n1:Note {path: "concepts/rag-architecture.md"}), (s1:Source {url: "https://arxiv.org/abs/2305.00000"})
MERGE (n1)-[:CITES {
  quote: "RAG combines retrieval with generation...",
  accessed_at: datetime()
}]->(s1);

// -----------------------------------------------------------------------------
// TEMPORAL QUERIES - Finding notes by time
// -----------------------------------------------------------------------------

// Find notes captured today
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE date(e.timestamp) = date()
RETURN n.title, e.timestamp, e.capture_method
ORDER BY e.timestamp DESC;

// Find notes captured in the last 7 days
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P7D')
RETURN n.title, e.timestamp, e.capture_method
ORDER BY e.timestamp DESC;

// Find notes captured last week (specific date range)
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE e.timestamp >= datetime("2025-01-08T00:00:00Z")
  AND e.timestamp < datetime("2025-01-15T00:00:00Z")
RETURN n.title, e.timestamp
ORDER BY e.timestamp DESC;

// Find notes captured in January 2025
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)-[:ON_DATE]->(d:Date)
WHERE d.year = 2025 AND d.month = 1
RETURN n.title, d.date, e.timestamp
ORDER BY d.date;

// Find notes by capture method
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE e.capture_method = "inbox"
RETURN n.title, e.timestamp
ORDER BY e.timestamp DESC
LIMIT 20;

// -----------------------------------------------------------------------------
// EDIT HISTORY - Tracking how notes evolve
// -----------------------------------------------------------------------------

// Show complete edit history for a note
MATCH (n:Note {path: "concepts/rag-architecture.md"})-[:EDITED_AT]->(e:CaptureEvent)
RETURN e.timestamp, e.metadata.changes
ORDER BY e.timestamp;

// Find notes edited in the last 7 days
MATCH (n:Note)-[:EDITED_AT]->(e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P7D')
RETURN n.title, n.path, e.timestamp
ORDER BY e.timestamp DESC;

// Find rapidly evolving notes (many edits recently)
MATCH (n:Note)-[:EDITED_AT]->(e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P30D')
WITH n, count(e) AS edit_count
WHERE edit_count > 5
RETURN n.title, n.path, edit_count
ORDER BY edit_count DESC;

// Find stale notes (not edited in 90 days)
MATCH (n:Note)
OPTIONAL MATCH (n)-[:EDITED_AT]->(e:CaptureEvent)
WITH n, max(e.timestamp) AS last_edit
WHERE last_edit < datetime() - duration('P90D') OR last_edit IS NULL
RETURN n.title, n.path, n.created_at, last_edit
ORDER BY last_edit NULLS FIRST
LIMIT 20;

// -----------------------------------------------------------------------------
// RELATIONSHIP QUERIES - Finding connections between notes
// -----------------------------------------------------------------------------

// Find all notes linked to a specific note
MATCH (n1:Note {path: "concepts/rag-architecture.md"})-[r:LINKED_TO]-(n2:Note)
RETURN n2.title, n2.path, r.confidence
ORDER BY r.confidence DESC;

// Find strongest semantic connections (confidence > 0.8)
MATCH (n1:Note)-[r:LINKED_TO]-(n2:Note)
WHERE r.confidence > 0.8
RETURN n1.title, n2.title, r.confidence
ORDER BY r.confidence DESC
LIMIT 20;

// Find notes with most connections (hub notes)
MATCH (n:Note)-[:LINKED_TO]-()
RETURN n.title, n.path, count(*) AS connections
ORDER BY connections DESC
LIMIT 20;

// Find notes that should be linked (captured same day, not yet linked)
MATCH (n1:Note)-[:CAPTURED_AT]->(e1:CaptureEvent)-[:ON_DATE]->(d:Date)
MATCH (n2:Note)-[:CAPTURED_AT]->(e2:CaptureEvent)-[:ON_DATE]->(d)
WHERE n1 <> n2
  AND NOT EXISTS { (n1)-[:LINKED_TO]-(n2) }
RETURN n1.title, n2.title, d.date
ORDER BY d.date DESC
LIMIT 20;

// Find orphaned notes (no links)
MATCH (n:Note)
WHERE NOT EXISTS { (n)-[:LINKED_TO]-() }
RETURN n.title, n.path, n.created_at
ORDER BY n.created_at DESC
LIMIT 20;

// -----------------------------------------------------------------------------
// SOURCE TRACKING - Finding citations and references
// -----------------------------------------------------------------------------

// Find all notes citing a specific source
MATCH (n:Note)-[:CITES]->(s:Source {url: "https://arxiv.org/abs/2305.00000"})
RETURN n.title, n.created_at
ORDER BY n.created_at;

// Find most cited sources
MATCH (n:Note)-[:CITES]->(s:Source)
RETURN s.url, s.title, s.source_type, count(n) AS citation_count
ORDER BY citation_count DESC
LIMIT 10;

// Find notes without sources (uncited)
MATCH (n:Note)
WHERE NOT EXISTS { (n)-[:CITES]->(:Source) }
RETURN n.title, n.path, n.created_at
ORDER BY n.created_at DESC
LIMIT 20;

// Find sources by type (papers, books, websites)
MATCH (s:Source)
WHERE s.source_type = "paper"
RETURN s.url, s.title, s.author
ORDER BY s.title;

// -----------------------------------------------------------------------------
// DAILY/WEEKLY SUMMARIES - Aggregate statistics
// -----------------------------------------------------------------------------

// Today's capture summary
MATCH (e:CaptureEvent)-[:ON_DATE]->(d:Date {date: date()})
MATCH (n:Note)-[:CAPTURED_AT]->(e)
RETURN n.title, e.timestamp, e.capture_method
ORDER BY e.timestamp;

// Count captures per day (last 30 days)
MATCH (e:CaptureEvent)-[:ON_DATE]->(d:Date)
WHERE d.date > date() - duration('P30D')
RETURN d.date, count(e) AS captures
ORDER BY d.date;

// Weekly capture count by method
MATCH (e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P7D')
RETURN e.capture_method, count(*) AS count
ORDER BY count DESC;

// Monthly summary (notes created, links added, sources cited)
MATCH (d:Date)
WHERE d.year = 2025 AND d.month = 1
WITH d
OPTIONAL MATCH (e:CaptureEvent)-[:ON_DATE]->(d)
OPTIONAL MATCH (n:Note)-[:CAPTURED_AT]->(e)
WITH d, count(DISTINCT n) AS notes_created
OPTIONAL MATCH ()-[l:LINKED_TO]->()
WHERE date(l.created_at) = d.date
WITH d, notes_created, count(DISTINCT l) AS links_created
RETURN d.date, notes_created, links_created
ORDER BY d.date;

// -----------------------------------------------------------------------------
// TAG ANALYSIS - Finding notes by tags
// -----------------------------------------------------------------------------

// Find notes with specific tag
MATCH (n:Note)
WHERE "ai" IN n.tags
RETURN n.title, n.tags, n.created_at
ORDER BY n.created_at DESC;

// Find most common tags
MATCH (n:Note)
UNWIND n.tags AS tag
RETURN tag, count(*) AS usage_count
ORDER BY usage_count DESC
LIMIT 20;

// Find notes with multiple specific tags
MATCH (n:Note)
WHERE ALL(tag IN ["ai", "architecture"] WHERE tag IN n.tags)
RETURN n.title, n.tags;

// -----------------------------------------------------------------------------
// KNOWLEDGE EVOLUTION - Tracking how understanding changes
// -----------------------------------------------------------------------------

// Find notes about a topic (by tag) over time
MATCH (n:Note)-[:CAPTURED_AT]->(e:CaptureEvent)
WHERE "rag" IN n.tags
RETURN n.title, e.timestamp
ORDER BY e.timestamp;

// Show how a concept evolved (notes + edits)
MATCH (n:Note)
WHERE "rag" IN n.tags
OPTIONAL MATCH (n)-[:EDITED_AT]->(edit:CaptureEvent)
RETURN n.title, n.created_at, collect(edit.timestamp) AS edit_history
ORDER BY n.created_at;

// Find related notes captured after learning about a topic
MATCH (seed:Note {path: "concepts/rag-architecture.md"})-[:CAPTURED_AT]->(seed_event:CaptureEvent)
MATCH (related:Note)-[:CAPTURED_AT]->(related_event:CaptureEvent)
WHERE related_event.timestamp > seed_event.timestamp
  AND ANY(tag IN related.tags WHERE tag IN seed.tags)
RETURN related.title, related_event.timestamp, related.tags
ORDER BY related_event.timestamp
LIMIT 10;

// -----------------------------------------------------------------------------
// CLEANUP & MAINTENANCE - Keeping the graph tidy
// -----------------------------------------------------------------------------

// Find and count orphaned capture events (no notes)
MATCH (e:CaptureEvent)
WHERE NOT EXISTS { (:Note)-[:CAPTURED_AT|EDITED_AT]->(e) }
RETURN count(e) AS orphaned_events;

// Remove orphaned capture events (use with caution!)
// MATCH (e:CaptureEvent)
// WHERE NOT EXISTS { (:Note)-[:CAPTURED_AT|EDITED_AT]->(e) }
// DELETE e;

// Find duplicate notes (same title, different paths)
MATCH (n1:Note), (n2:Note)
WHERE n1.title = n2.title
  AND n1.path <> n2.path
RETURN n1.title, n1.path, n2.path;

// Find test nodes (for cleanup after testing)
MATCH (n)
WHERE n.note_id STARTS WITH "test-" OR n.event_id STARTS WITH "test-"
RETURN labels(n)[0] AS label, count(n) AS count;

// Delete test nodes
// MATCH (n)
// WHERE n.note_id STARTS WITH "test-" OR n.event_id STARTS WITH "test-"
// DELETE n;

// -----------------------------------------------------------------------------
// STATISTICS & REPORTING - Database health checks
// -----------------------------------------------------------------------------

// Count all nodes by type
MATCH (n)
RETURN labels(n)[0] AS node_type, count(n) AS count
ORDER BY count DESC;

// Count all relationships by type
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(r) AS count
ORDER BY count DESC;

// Database size summary
MATCH (n)
WITH count(n) AS total_nodes
MATCH ()-[r]->()
WITH total_nodes, count(r) AS total_relationships
RETURN total_nodes, total_relationships,
       (total_nodes + total_relationships) AS total_elements;

// Find largest notes (by word count)
MATCH (n:Note)
WHERE n.word_count IS NOT NULL
RETURN n.title, n.path, n.word_count
ORDER BY n.word_count DESC
LIMIT 20;

// Average note word count
MATCH (n:Note)
WHERE n.word_count IS NOT NULL
RETURN avg(n.word_count) AS avg_word_count,
       min(n.word_count) AS min_word_count,
       max(n.word_count) AS max_word_count;

// Notes created per month
MATCH (n:Note)
WITH n, n.created_at.year AS year, n.created_at.month AS month
RETURN year, month, count(n) AS notes_created
ORDER BY year, month;

// -----------------------------------------------------------------------------
// ADVANCED QUERIES - Complex patterns and analysis
// -----------------------------------------------------------------------------

// Find clusters of related notes (3+ notes linked together)
MATCH path = (n1:Note)-[:LINKED_TO*1..2]-(n2:Note)
WHERE n1 <> n2
WITH collect(DISTINCT n1) + collect(DISTINCT n2) AS cluster
WHERE size(cluster) >= 3
RETURN cluster;

// Find the shortest path between two notes
MATCH path = shortestPath(
  (n1:Note {path: "concepts/rag-architecture.md"})-[:LINKED_TO*]-(n2:Note {path: "projects/obsidian-integration.md"})
)
RETURN path;

// Find notes that cite the same source (potential duplicates or related)
MATCH (n1:Note)-[:CITES]->(s:Source)<-[:CITES]-(n2:Note)
WHERE n1 <> n2
RETURN s.url, s.title, collect(DISTINCT n1.title) AS citing_notes
LIMIT 10;

// Timeline of knowledge building (captures + edits combined)
MATCH (e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P30D')
OPTIONAL MATCH (n:Note)-[:CAPTURED_AT]->(e)
RETURN e.timestamp, e.capture_method, n.title, "capture" AS event_type
UNION
MATCH (e:CaptureEvent)
WHERE e.timestamp > datetime() - duration('P30D')
OPTIONAL MATCH (n:Note)-[:EDITED_AT]->(e)
RETURN e.timestamp, e.capture_method, n.title, "edit" AS event_type
ORDER BY e.timestamp DESC;

// -----------------------------------------------------------------------------
// END OF QUERIES
// -----------------------------------------------------------------------------

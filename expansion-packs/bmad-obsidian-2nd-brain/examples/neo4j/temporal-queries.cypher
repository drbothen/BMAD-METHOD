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

// =============================================================================
// PHASE 2 TEMPORAL QUERIES - Evolution Tracking & Maturation Metrics
// =============================================================================
// Version: 2.0
// Added: 2025-11-11
// Purpose: Advanced temporal analysis for concept evolution, understanding shifts,
//          maturation metrics, and synthesis tracking

// ----------------------------------------------------------------------------
// QUERY P2-1: Complete Evolution Timeline for a Concept
// ----------------------------------------------------------------------------
// Use Case: Get full temporal history with PROMOTION, LINK, MOC_ADDED events
// Agent: Timeline Constructor
// Parameters: Replace $note_path with actual path
// ----------------------------------------------------------------------------

MATCH (n:Note {path: $note_path})-[r:HAS_EVENT]->(e:Event)
RETURN e.timestamp AS when,
       e.event_type AS event,
       e.metadata AS details
ORDER BY e.timestamp ASC;


// ----------------------------------------------------------------------------
// QUERY P2-2: Calculate Days to Evergreen
// ----------------------------------------------------------------------------
// Use Case: Measure maturation speed for a concept
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (n:Note {path: $note_path})-[:HAS_EVENT]->(capture:Event {event_type: 'CAPTURE'})
MATCH (n)-[:HAS_EVENT]->(promotion:Event {event_type: 'PROMOTION'})
WHERE promotion.metadata.to = 'evergreen'
WITH duration.between(capture.timestamp, promotion.timestamp).days AS days_to_evergreen
RETURN days_to_evergreen;


// ----------------------------------------------------------------------------
// QUERY P2-3: Calculate Edit Velocity (Development Phase)
// ----------------------------------------------------------------------------
// Use Case: Edits per week during active development
// Agent: Timeline Constructor
// Parameters: $development_start, $development_end
// ----------------------------------------------------------------------------

MATCH (n:Note {path: $note_path})-[:HAS_EVENT]->(e:Event {event_type: 'EDIT'})
WHERE e.timestamp >= $development_start AND e.timestamp < $development_end
WITH count(e) AS edit_count,
     duration.between($development_start, $development_end).days / 7.0 AS weeks
RETURN edit_count / weeks AS edits_per_week;


// ----------------------------------------------------------------------------
// QUERY P2-4: Find Understanding Shifts
// ----------------------------------------------------------------------------
// Use Case: Detect contradictions and belief revisions
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (n:Note {path: $note_path})-[:HAS_EVENT]->(e:Event {event_type: 'EDIT'})
WHERE e.metadata.understanding_shift = 'contradiction'
RETURN e.timestamp AS shift_date,
       e.metadata.before AS previous_understanding,
       e.metadata.after AS new_understanding,
       e.metadata.trigger AS what_caused_shift,
       e.metadata.evidence AS evidence
ORDER BY shift_date;


// ----------------------------------------------------------------------------
// QUERY P2-5: Track Relationship Strength Evolution
// ----------------------------------------------------------------------------
// Use Case: How link between concepts strengthened over time
// Agent: Semantic Linker
// Parameters: $source_path, $target_path
// ----------------------------------------------------------------------------

MATCH (source:Note {path: $source_path})-[r:HAS_EVENT]->(e:Event {event_type: 'LINK'})
WHERE e.metadata.target_note = $target_path
WITH e.timestamp AS link_time,
     e.metadata.direction AS direction,
     e.metadata.context_added AS context,
     e.metadata.strength AS strength
ORDER BY link_time
RETURN link_time, direction, context, strength;


// ----------------------------------------------------------------------------
// QUERY P2-6: Identify Concept Influences
// ----------------------------------------------------------------------------
// Use Case: Find sources and concepts that shaped development
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (n:Note {path: $note_path})-[:HAS_EVENT]->(e:Event)
WHERE e.event_type IN ['EDIT', 'LINK']
  AND e.metadata.source_cited IS NOT NULL
WITH e.timestamp AS when,
     e.metadata.source_cited AS source,
     e.event_type AS event
ORDER BY when
RETURN source,
       collect(event) AS influence_events,
       min(when) AS first_influence,
       max(when) AS last_influence,
       count(event) AS influence_count
ORDER BY influence_count DESC;


// ----------------------------------------------------------------------------
// QUERY P2-7: Vault Average Days to Evergreen
// ----------------------------------------------------------------------------
// Use Case: Baseline for percentile ranking
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (n:Note)-[:HAS_EVENT]->(capture:Event {event_type: 'CAPTURE'})
MATCH (n)-[:HAS_EVENT]->(promotion:Event {event_type: 'PROMOTION'})
WHERE promotion.metadata.to = 'evergreen'
WITH duration.between(capture.timestamp, promotion.timestamp).days AS days
RETURN avg(days) AS vault_avg_days_to_evergreen,
       percentileDisc(days, 0.5) AS median_days_to_evergreen,
       percentileDisc(days, 0.25) AS p25_days,
       percentileDisc(days, 0.75) AS p75_days,
       count(days) AS sample_size;


// ----------------------------------------------------------------------------
// QUERY P2-8: Detect Phase Transitions
// ----------------------------------------------------------------------------
// Use Case: Identify when concept moved between evolution phases
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (n:Note {path: $note_path})-[:HAS_EVENT]->(e:Event {event_type: 'EDIT'})
WITH e.timestamp AS edit_time
ORDER BY edit_time
WITH collect(edit_time) AS edit_times
UNWIND range(0, size(edit_times)-2) AS i
WITH edit_times[i] AS current_edit,
     edit_times[i+1] AS next_edit,
     duration.between(edit_times[i], edit_times[i+1]).days AS gap_days
RETURN current_edit,
       next_edit,
       gap_days,
       CASE
         WHEN gap_days > 60 THEN 'phase_transition_likely'
         WHEN gap_days > 14 THEN 'activity_decrease'
         ELSE 'active_development'
       END AS activity_status
ORDER BY gap_days DESC;


// ----------------------------------------------------------------------------
// QUERY P2-9: Find Recently Promoted Evergreen Concepts
// ----------------------------------------------------------------------------
// Use Case: Identify accomplishments in last 30 days
// Agent: Monthly Deep Review Workflow
// Parameters: $days_back (default 30)
// ----------------------------------------------------------------------------

MATCH (n:Note)-[:HAS_EVENT]->(e:Event {event_type: 'PROMOTION'})
WHERE e.metadata.to = 'evergreen'
  AND e.timestamp > datetime() - duration({days: $days_back})
RETURN n.path AS concept_path,
       n.title AS concept_title,
       e.timestamp AS promoted_date,
       duration.between(
         [(n)-[:HAS_EVENT]->(capture {event_type: 'CAPTURE'}) | capture.timestamp][0],
         e.timestamp
       ).days AS maturation_time_days
ORDER BY promoted_date DESC;


// ----------------------------------------------------------------------------
// QUERY P2-10: Identify Stagnant Concepts (>90 Days Inactive)
// ----------------------------------------------------------------------------
// Use Case: Find concepts stuck in development
// Agent: MOC Constructor
// Parameters: $stagnation_threshold_days (default 90)
// ----------------------------------------------------------------------------

MATCH (n:Note)-[:HAS_EVENT]->(capture:Event {event_type: 'CAPTURE'})
MATCH (n)-[:HAS_EVENT]->(promotion:Event {event_type: 'PROMOTION'})
WHERE promotion.metadata.to = 'permanent'
  AND NOT exists((n)-[:HAS_EVENT]->(:Event {event_type: 'PROMOTION'}) WHERE .metadata.to = 'evergreen')
OPTIONAL MATCH (n)-[:HAS_EVENT]->(last_edit:Event {event_type: 'EDIT'})
WITH n,
     capture,
     promotion,
     max(last_edit.timestamp) AS last_activity
WHERE duration.between(last_activity, datetime()).days > $stagnation_threshold_days
RETURN n.path,
       n.title,
       last_activity,
       duration.between(last_activity, datetime()).days AS days_stagnant,
       duration.between(capture.timestamp, promotion.timestamp).days AS time_in_development
ORDER BY days_stagnant DESC;


// ----------------------------------------------------------------------------
// QUERY P2-11: Find Cross-Domain Connections
// ----------------------------------------------------------------------------
// Use Case: Identify synthesis opportunities between MOCs
// Agent: MOC Constructor
// Parameters: $min_cross_links (default 3)
// ----------------------------------------------------------------------------

MATCH (moc1:MOC)<-[:BELONGS_TO]-(n1:Note)
MATCH (n1)-[:HAS_EVENT]->(link:Event {event_type: 'LINK'})
MATCH (n2:Note {path: link.metadata.target_note})-[:BELONGS_TO]->(moc2:MOC)
WHERE moc1 <> moc2
WITH moc1.title AS domain1,
     moc2.title AS domain2,
     count(link) AS cross_link_count,
     collect({
       note1: n1.title,
       note2: n2.title,
       when: link.timestamp
     }) AS connections
WHERE cross_link_count >= $min_cross_links
RETURN domain1,
       domain2,
       cross_link_count,
       connections
ORDER BY cross_link_count DESC;


// ----------------------------------------------------------------------------
// QUERY P2-12: Track MOC Domain Maturation
// ----------------------------------------------------------------------------
// Use Case: Monitor MOC growth over time
// Agent: MOC Constructor
// Parameters: $moc_title
// ----------------------------------------------------------------------------

MATCH (moc:MOC {title: $moc_title})
OPTIONAL MATCH (moc)-[:MATURED_AT]->(milestone:MilestoneEvent)
OPTIONAL MATCH (moc)<-[:BELONGS_TO]-(notes:Note)
WITH moc,
     count(DISTINCT notes) AS current_note_count,
     moc.maturity AS current_maturity,
     collect({
       from: milestone.metadata.from_maturity,
       to: milestone.metadata.to_maturity,
       when: milestone.timestamp,
       note_count_at_milestone: milestone.metadata.note_count
     }) AS maturation_history
RETURN moc.title AS domain,
       moc.created AS created_date,
       current_note_count,
       current_maturity,
       maturation_history
ORDER BY current_note_count DESC;


// ----------------------------------------------------------------------------
// QUERY P2-13: Calculate Link Accumulation Rate
// ----------------------------------------------------------------------------
// Use Case: Linking velocity during maturation
// Agent: Timeline Constructor
// Parameters: $note_path, $maturation_start, $maturation_end
// ----------------------------------------------------------------------------

MATCH (n:Note {path: $note_path})-[:HAS_EVENT]->(e:Event {event_type: 'LINK'})
WHERE e.timestamp >= $maturation_start AND e.timestamp < $maturation_end
WITH count(e) AS link_count,
     duration.between($maturation_start, $maturation_end).days / 30.0 AS months
RETURN link_count / months AS links_per_month;


// ----------------------------------------------------------------------------
// QUERY P2-14: Find Concepts with Multiple Understanding Shifts
// ----------------------------------------------------------------------------
// Use Case: Identify complex evolution trajectories
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (n:Note)-[:HAS_EVENT]->(e:Event)
WHERE e.metadata.understanding_shift IS NOT NULL
WITH n.title AS concept,
     n.path AS path,
     count(e) AS shift_count,
     collect({
       type: e.metadata.understanding_shift,
       when: e.timestamp,
       trigger: e.metadata.trigger
     }) AS shifts
WHERE shift_count >= 2
RETURN concept,
       path,
       shift_count,
       shifts
ORDER BY shift_count DESC;


// ----------------------------------------------------------------------------
// QUERY P2-15: Temporal Co-occurrence Analysis
// ----------------------------------------------------------------------------
// Use Case: Find concepts edited in same time windows
// Agent: Semantic Linker
// Parameters: $time_window_days (default 7), $concept_path
// ----------------------------------------------------------------------------

MATCH (n1:Note {path: $concept_path})-[:HAS_EVENT]->(e1:Event {event_type: 'EDIT'})
MATCH (n2:Note)-[:HAS_EVENT]->(e2:Event {event_type: 'EDIT'})
WHERE n1 <> n2
  AND abs(duration.between(e1.timestamp, e2.timestamp).days) <= $time_window_days
WITH n1.title AS concept1,
     n2.title AS concept2,
     n2.path AS concept2_path,
     count(*) AS cooccurrence_count,
     collect({
       time1: e1.timestamp,
       time2: e2.timestamp,
       gap_days: duration.between(e1.timestamp, e2.timestamp).days
     }) AS cooccurrences
WHERE cooccurrence_count >= 3
RETURN concept1,
       concept2,
       concept2_path,
       cooccurrence_count,
       cooccurrences
ORDER BY cooccurrence_count DESC
LIMIT 10;


// ----------------------------------------------------------------------------
// QUERY P2-16: Vault Edit Velocity Distribution
// ----------------------------------------------------------------------------
// Use Case: Percentile distribution for comparison baseline
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (n:Note)-[:HAS_EVENT]->(capture:Event {event_type: 'CAPTURE'})
MATCH (n)-[:HAS_EVENT]->(perm:Event {event_type: 'PROMOTION'})
WHERE perm.metadata.to = 'permanent'
OPTIONAL MATCH (n)-[:HAS_EVENT]->(edit:Event {event_type: 'EDIT'})
WHERE edit.timestamp >= capture.timestamp AND edit.timestamp < perm.timestamp
WITH n,
     count(edit) AS edit_count,
     duration.between(capture.timestamp, perm.timestamp).days / 7.0 AS development_weeks
WHERE development_weeks > 0
WITH edit_count / development_weeks AS edit_velocity
RETURN avg(edit_velocity) AS vault_avg_edit_velocity,
       percentileDisc(edit_velocity, 0.25) AS p25_velocity,
       percentileDisc(edit_velocity, 0.5) AS median_velocity,
       percentileDisc(edit_velocity, 0.75) AS p75_velocity,
       percentileDisc(edit_velocity, 0.9) AS p90_velocity;


// ----------------------------------------------------------------------------
// QUERY P2-17: Find Synthesis Events
// ----------------------------------------------------------------------------
// Use Case: Identify when multiple concepts were combined
// Agent: Timeline Constructor
// ----------------------------------------------------------------------------

MATCH (synthesis:Note)-[:HAS_EVENT]->(e:Event {event_type: 'EDIT'})
WHERE e.metadata.edit_type = 'synthesis'
OPTIONAL MATCH (synthesis)-[:HAS_EVENT]->(link:Event {event_type: 'LINK'})
WHERE link.timestamp <= e.timestamp + duration({days: 7})
WITH synthesis.title AS synthesis_concept,
     synthesis.path AS synthesis_path,
     e.timestamp AS synthesis_date,
     collect(DISTINCT link.metadata.target_note) AS component_concepts
WHERE size(component_concepts) >= 2
RETURN synthesis_concept,
       synthesis_path,
       synthesis_date,
       component_concepts,
       size(component_concepts) AS component_count
ORDER BY synthesis_date DESC;


// ----------------------------------------------------------------------------
// QUERY P2-18: All Understanding Shifts in Vault
// ----------------------------------------------------------------------------
// Use Case: Generate vault-wide shift catalog
// Agent: Timeline Constructor, Monthly Review
// ----------------------------------------------------------------------------

MATCH (new:Note)-[c:CONTRADICTS]->(old:Note)
OPTIONAL MATCH (new)-[:INFLUENCED_BY]->(evidence)
OPTIONAL MATCH (synthesis)-[:SYNTHESIZED_INTO]->(new)
OPTIONAL MATCH (synthesis)-[:SYNTHESIZED_INTO]->(old)
RETURN new.title AS new_understanding,
       old.title AS old_understanding,
       c.discovered_at AS when_shifted,
       c.evidence AS what_caused_shift,
       evidence.title AS evidence_source,
       synthesis.title AS synthesis_note,
       c.resolution_status AS resolution
ORDER BY c.discovered_at DESC;


// =============================================================================
// USAGE NOTES FOR PHASE 2 QUERIES
// =============================================================================
//
// Parameter Substitution:
// - Replace $note_path with "atomic/concept-name.md"
// - Replace $moc_title with "Domain Name MOC"
// - Replace $days_back with number (e.g., 30)
// - Replace date ranges with actual datetime values
//
// Graphiti MCP Execution:
// await mcp.tools.graphiti.executeCypher({
//   query: "MATCH (n:Note {path: $note_path})...",
//   params: { note_path: "atomic/spaced-repetition.md" }
// });
//
// Performance:
// - Create indexes: Note.path, Event.timestamp, Event.event_type
// - Use LIMIT for large result sets
// - Profile slow queries with EXPLAIN/PROFILE
//
// Testing:
// - Validate timestamps are chronological
// - Check edge cases (no events, missing promotions)
// - Verify vault averages are reasonable
//
// Documentation:
// - See obsidian-technical-guide.md for pattern details
// - See knowledge-graph-patterns.md for relationship types
// - See temporal-schema.md for complete schema
//
// =============================================================================

// -----------------------------------------------------------------------------
// END OF QUERIES
// -----------------------------------------------------------------------------

<!-- Powered by BMAD™ Core -->

# Query Temporal Events

## Purpose

Retrieve temporal events (captures, edits, promotions, links) from Neo4j Graphiti database for a specific concept or note, with time range and event type filtering.

## Inputs

- **note_path** (String, required): Path to note in vault (e.g., "notes/Spaced Repetition.md")
- **time_range** (Object, optional): Contains start_date and end_date (ISO 8601 format)
- **event_types** (Array, optional): Filter for specific events ["CAPTURE", "EDIT", "PROMOTION", "LINK"]
- **include_related** (Boolean, optional): Include events from linked notes (default: false)

## Outputs

- **temporal_events** (Array): Chronologically ordered list of events with timestamps and metadata
- **event_summary** (Object): Statistics on event counts, time span, and patterns

## Procedure

### Step 1: Validate Neo4j Availability

Check if temporal querying is possible:

```
try:
  graphiti.health_check()
  neo4j_available = true
catch:
  neo4j_available = false
  error("Neo4j required for temporal event queries. Start Neo4j or check Graphiti MCP configuration.")
  return null
```

If Neo4j unavailable, this task cannot proceed (temporal events only exist in graph database).

### Step 2: Validate Inputs

- **note_path**: Must be non-empty string
- **time_range**: If provided, validate date format and ensure start_date < end_date
- **event_types**: If provided, validate against allowed types: CAPTURE, EDIT, PROMOTION, LINK, MOC_ADDED
- If validation fails, return error with specific issue

### Step 3: Construct Base Cypher Query

Build Cypher query to retrieve events:

**Base query structure:**

```cypher
MATCH (n:Note {path: $note_path})

// Capture events
OPTIONAL MATCH (n)-[:CAPTURED_AT]->(ce:CaptureEvent)
WHERE ($start_date IS NULL OR ce.timestamp >= $start_date)
  AND ($end_date IS NULL OR ce.timestamp <= $end_date)
  AND ('CAPTURE' IN $event_types OR $event_types IS NULL)

// Edit events
OPTIONAL MATCH (n)-[:EDITED_AT]->(ee:EditEvent)
WHERE ($start_date IS NULL OR ee.timestamp >= $start_date)
  AND ($end_date IS NULL OR ee.timestamp <= $end_date)
  AND ('EDIT' IN $event_types OR $event_types IS NULL)

// Promotion events (inbox → evergreen)
OPTIONAL MATCH (n)-[:PROMOTED_AT]->(pe:PromotionEvent)
WHERE ($start_date IS NULL OR pe.timestamp >= $start_date)
  AND ($end_date IS NULL OR pe.timestamp <= $end_date)
  AND ('PROMOTION' IN $event_types OR $event_types IS NULL)

// Link creation events
OPTIONAL MATCH (n)-[link:LINKED_TO]-(other:Note)
WHERE ($start_date IS NULL OR link.created_at >= $start_date)
  AND ($end_date IS NULL OR link.created_at <= $end_date)
  AND ('LINK' IN $event_types OR $event_types IS NULL)

// MOC addition events
OPTIONAL MATCH (moc:MOC)-[org:ORGANIZES]->(n)
WHERE ($start_date IS NULL OR org.added_at >= $start_date)
  AND ($end_date IS NULL OR org.added_at <= $end_date)
  AND ('MOC_ADDED' IN $event_types OR $event_types IS NULL)

RETURN
  collect(DISTINCT {
    type: 'CAPTURE',
    timestamp: ce.timestamp,
    source: ce.source_url,
    method: ce.capture_method
  }) as captures,
  collect(DISTINCT {
    type: 'EDIT',
    timestamp: ee.timestamp,
    changes: ee.diff_summary,
    edit_size: ee.lines_changed
  }) as edits,
  collect(DISTINCT {
    type: 'PROMOTION',
    timestamp: pe.timestamp,
    from: pe.from_location,
    to: pe.to_location
  }) as promotions,
  collect(DISTINCT {
    type: 'LINK',
    timestamp: link.created_at,
    target: other.path,
    relationship: link.relationship_type
  }) as links,
  collect(DISTINCT {
    type: 'MOC_ADDED',
    timestamp: org.added_at,
    moc: moc.path,
    branch: org.branch
  }) as moc_additions

ORDER BY timestamp ASC
```

### Step 4: Execute Query via Graphiti MCP

Use Graphiti MCP to execute Cypher query:

```javascript
const result = await graphiti.search({
  query: `Find all temporal events for note at ${note_path}`,
  group_ids: [note_path],
  time_range: time_range
    ? { start: time_range.start_date, end: time_range.end_date }
    : undefined
});

// Parse Graphiti episode results into event format
temporal_events = result.episodes.map(episode => ({
  type: episode.type,
  timestamp: episode.valid_at,
  metadata: episode.content
}));
```

Alternative direct Cypher execution (if Graphiti supports):

```javascript
const result = await graphiti.executeCypher({
  query: cypher_query,
  parameters: {
    note_path: note_path,
    start_date: time_range?.start_date,
    end_date: time_range?.end_date,
    event_types: event_types
  }
});
```

### Step 5: Flatten and Normalize Events

Combine all event types into single chronological array:

```javascript
temporal_events = [];

// Add captures
for (const capture of result.captures) {
  if (capture.timestamp) {
    temporal_events.push({
      type: 'CAPTURE',
      timestamp: new Date(capture.timestamp),
      source: capture.source,
      method: capture.method
    });
  }
}

// Add edits
for (const edit of result.edits) {
  if (edit.timestamp) {
    temporal_events.push({
      type: 'EDIT',
      timestamp: new Date(edit.timestamp),
      changes: edit.changes,
      edit_size: edit.edit_size
    });
  }
}

// ... repeat for promotions, links, moc_additions

// Sort chronologically
temporal_events.sort((a, b) => a.timestamp - b.timestamp);
```

### Step 6: Handle include_related Option

If `include_related = true`, also query events from linked notes:

```cypher
MATCH (n:Note {path: $note_path})-[:LINKED_TO]-(related:Note)
// ... repeat event queries for related notes
// Tag events with source_note: related.path
RETURN events
```

Append related note events to temporal_events array, tagged with source.

### Step 7: Calculate Event Summary Statistics

Generate summary statistics for the retrieved events:

```javascript
event_summary = {
  total_events: temporal_events.length,
  time_span: {
    first_event: temporal_events[0]?.timestamp,
    last_event: temporal_events[temporal_events.length - 1]?.timestamp,
    duration_days: calculate_duration(first_event, last_event)
  },
  event_counts: {
    captures: temporal_events.filter(e => e.type === 'CAPTURE').length,
    edits: temporal_events.filter(e => e.type === 'EDIT').length,
    promotions: temporal_events.filter(e => e.type === 'PROMOTION').length,
    links: temporal_events.filter(e => e.type === 'LINK').length,
    moc_additions: temporal_events.filter(e => e.type === 'MOC_ADDED').length
  },
  patterns: {
    most_active_period: identify_most_active_week(temporal_events),
    average_edit_frequency: calculate_avg_frequency(edits, duration_days),
    link_growth_rate: calculate_growth_rate(links, duration_days)
  }
};
```

### Step 8: Format Events for Display

Create human-readable event descriptions:

```javascript
for (const event of temporal_events) {
  switch (event.type) {
    case 'CAPTURE':
      event.description = `Captured from ${event.source || 'unknown source'}`;
      break;
    case 'EDIT':
      event.description = `Edited (${event.edit_size || 'unknown'} lines changed)`;
      if (event.changes) {
        event.description += `: ${event.changes}`;
      }
      break;
    case 'PROMOTION':
      event.description = `Promoted from ${event.from} to ${event.to}`;
      break;
    case 'LINK':
      event.description = `Linked to [[${extract_title(event.target)}]]`;
      break;
    case 'MOC_ADDED':
      event.description = `Added to [[${extract_title(event.moc)}]] MOC`;
      break;
  }
}
```

### Step 9: Generate Event Timeline Report

Create formatted report of temporal events:

```markdown
## Temporal Events: [[Spaced Repetition]]

**Time Range**: 2024-01-15 to 2024-11-11 (301 days)
**Total Events**: 42 events

### Event Summary

- 📥 **Captures**: 1 event
- ✏️  **Edits**: 28 events
- ⬆️  **Promotions**: 1 event
- 🔗 **Links**: 10 events
- 🗺️  **MOC Additions**: 2 events

**Most Active Period**: 2024-02-12 to 2024-02-18 (8 events in 1 week)
**Average Edit Frequency**: 2.1 edits/week during development phase
**Link Growth Rate**: 1.2 new links/month

### Chronological Event Log

#### 2024-01-15 | 09:23 AM
📥 **CAPTURE** - Captured from https://example.com/spaced-repetition-article
Method: web-clipper

#### 2024-01-15 | 10:45 AM
✏️  **EDIT** - Edited (12 lines changed): Added definition and basic explanation

#### 2024-01-17 | 02:15 PM
✏️  **EDIT** - Edited (8 lines changed): Refined wording, added examples

#### 2024-01-20 | 11:30 AM
⬆️  **PROMOTION** - Promoted from inbox to evergreen
Note matured after 5 days in inbox

#### 2024-01-25 | 03:45 PM
🔗 **LINK** - Linked to [[Forgetting Curve]]
Relationship: relates-to

[... more events chronologically ...]

#### 2024-11-11 | Present
Current Status: Evergreen note with 28 backlinks, last edited 2024-10-03
```

### Step 10: Return Results

Return structured event data and summary:

```json
{
  "note_path": "notes/Spaced Repetition.md",
  "query_executed_at": "2024-11-11T10:30:00Z",
  "temporal_events": [
    {
      "type": "CAPTURE",
      "timestamp": "2024-01-15T09:23:00Z",
      "description": "Captured from https://example.com/...",
      "metadata": { "source": "...", "method": "web-clipper" }
    },
    // ... more events
  ],
  "event_summary": {
    "total_events": 42,
    "time_span": { ... },
    "event_counts": { ... },
    "patterns": { ... }
  }
}
```

## Integration Notes

**Graphiti MCP Integration:**
- Use `graphiti.search()` with group_ids and time_range filters
- Or use `graphiti.executeCypher()` for direct Cypher query execution
- Episode nodes in Graphiti represent temporal events

**Event Type Mapping:**
- CAPTURE → CaptureEvent nodes (created by Inbox Triage Agent)
- EDIT → EditEvent nodes (created by note modification tracking)
- PROMOTION → PromotionEvent nodes (inbox → evergreen transition)
- LINK → Relationship created_at timestamps
- MOC_ADDED → MOC-[:ORGANIZES]->Note relationship timestamps

**Performance Considerations:**
- For large time ranges (> 1 year), consider pagination
- Index Neo4j timestamps for faster queries
- Cache vault averages to avoid recalculating

## Error Handling

**Neo4j unavailable:**
- Error: "Neo4j Graphiti required for temporal queries. Ensure Neo4j is running and Graphiti MCP is configured."
- Return null (cannot fallback to Obsidian-only mode)

**Note not found in Neo4j:**
- Warning: "Note [[X]] not found in Neo4j. It may not have been captured with temporal tracking enabled."
- Return empty events array with message

**No events in time range:**
- Info: "No events found for note in specified time range."
- Return empty events array (not an error)

**Cypher query fails:**
- Error: "Failed to execute temporal query: {error message}"
- Log full error for debugging
- Return null

## Testing

**Test Case 1: Full Event History**
- Input: note_path, no filters
- Expected: All event types returned, chronological order
- Validate: First event is CAPTURE, timestamps ascending

**Test Case 2: Time Range Filter**
- Input: note_path, time_range = last 30 days
- Expected: Only events from last 30 days returned
- Validate: All timestamps within range

**Test Case 3: Event Type Filter**
- Input: note_path, event_types = ["EDIT"]
- Expected: Only EDIT events returned
- Validate: No CAPTURE, PROMOTION, or LINK events present

**Test Case 4: Include Related Notes**
- Input: note_path, include_related = true
- Expected: Events from linked notes also returned, tagged with source
- Validate: Events include source_note field for related notes

**Test Case 5: Note with No Temporal Events**
- Input: note_path for note created before temporal tracking
- Expected: Empty events array with info message
- Validate: Graceful handling, no errors thrown

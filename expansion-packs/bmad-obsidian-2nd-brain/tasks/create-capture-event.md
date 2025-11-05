<!-- Powered by BMAD™ Core -->

# create-capture-event

Create a CaptureEvent node in Neo4j with bi-temporal metadata using Graphiti MCP integration (if enabled).

## Purpose

Store capture events in Neo4j knowledge graph with temporal tracking. Creates (:CaptureEvent) nodes with bi-temporal metadata and relationships to notes. Gracefully degrades if Neo4j is disabled or unavailable.

## Prerequisites

- Neo4j Graphiti MCP configured (optional)
- Inbox note created successfully (note_path available)
- Classification and metadata extraction completed
- Neo4j enabled status checked from config

## Inputs

```yaml
inputs:
  content: "..." # Captured content (required)
  content_type: "quote|concept|reference|reflection|question|observation" # Required
  confidence: 0.85 # Float 0.0-1.0 (required)
  source_url: "https://..." | null # Optional
  author: "Name" | "Unknown" # Optional
  capture_timestamp: "2025-11-04T15:30:00Z" # ISO 8601 (required)
  note_path: "/inbox/2025-11-04-1530-example.md" # Required (from create-inbox-note)
  tags: ["tag1", "tag2"] # Array (optional)
```

## Outputs

```yaml
result:
  success: true|false
  skipped: true|false # True if Neo4j disabled
  event_id: "uuid-here" | null
  error: "Error message" | null
  reason: "neo4j_disabled" | "connection_failed" | null
```

## Step-by-Step Execution

### Step 1: Check Neo4j Enabled Status

**Read config file:** `expansion-packs/bmad-obsidian-2nd-brain/config.yaml`

**Parse YAML and extract:**

```yaml
neo4j:
  enabled: true|false
```

**If enabled is false or undefined:**

- Skip Neo4j operations completely
- Return immediately with:
  ```yaml
  result:
    success: true
    skipped: true
    event_id: null
    error: null
    reason: 'neo4j_disabled'
  ```

**If enabled is true:**

- Proceed with Graphiti MCP integration (Steps 2-6)

### Step 2: Generate Event ID

Create unique identifier for this capture event:

**Format:** UUID v4

**Example:** `a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6`

**Generation:** Use standard UUID library or random generation

### Step 3: Prepare Episode for Graphiti

Graphiti MCP uses "episodes" to add information to the knowledge graph. Episodes are processed to extract entities and create nodes/relationships automatically.

**Episode Format:**

```text
{content_type} captured from {source}: {content_preview}
```

**Content Preview:**

- First 200 characters of content
- Append "..." if truncated

**Example Episodes:**

- **Quote:** "Quote captured from @naval: Knowledge work is about managing your attention, not your time."

- **Concept:** "Concept captured from zettelkasten.de: The Zettelkasten method uses atomic notes linked by concept relationships..."

- **Question:** "Question captured from personal reflection: How does bi-temporal versioning differ from event sourcing?"

### Step 4: Call Graphiti MCP add_episode

**Call:** Graphiti MCP `add_episode()`

**Parameters:**

- `content`: Episode text (from Step 3)
- `timestamp`: ISO 8601 timestamp (capture_timestamp)

**Example:**

```javascript
mcp_tools.graphiti.add_episode({
  content: 'Quote captured from @naval: Knowledge work is about...',
  timestamp: '2025-11-04T15:30:00Z',
});
```

**Graphiti will automatically:**

- Extract entities from episode text
- Create entity nodes
- Create relationships between entities
- Store episode in graph

### Step 5: Create Manual CaptureEvent Node

Graphiti handles entity extraction, but we need to create our custom CaptureEvent node manually for structured tracking.

**Call:** Graphiti MCP `execute_cypher()` or equivalent custom node creation

**Cypher Query (parameterized):**

```cypher
CREATE (c:CaptureEvent {
  event_id: $event_id,
  content_type: $content_type,
  confidence_score: $confidence,
  source_url: $source_url,
  author: $author,
  capture_timestamp: datetime($capture_timestamp),
  valid_time_start: datetime($capture_timestamp),
  valid_time_end: null,
  transaction_time: datetime(),
  note_path: $note_path,
  tags: $tags
})
RETURN c
```

**Parameters (NEVER use string concatenation):**

```javascript
{
  event_id: "a1b2c3d4...",
  content_type: "quote",
  confidence: 0.95,
  source_url: "https://twitter.com/naval/status/123",
  author: "@naval",
  capture_timestamp: "2025-11-04T15:30:00Z",
  note_path: "/inbox/2025-11-04-1530-knowledge-work.md",
  tags: ["twitter", "philosophy"]
}
```

**Bi-Temporal Properties:**

- `valid_time_start`: When the capture occurred in real world
- `valid_time_end`: null (ongoing validity)
- `transaction_time`: When the record was created in database (use `datetime()` for current time)

### Step 6: Create Relationship to Note

Link CaptureEvent to the Obsidian note:

**Cypher Query:**

```cypher
MATCH (c:CaptureEvent {event_id: $event_id})
CREATE (n:Note {path: $note_path})
CREATE (c)-[:RESULTED_IN]->(n)
RETURN c, n
```

**Or combined with Step 5:**

```cypher
CREATE (c:CaptureEvent {
  event_id: $event_id,
  content_type: $content_type,
  confidence_score: $confidence,
  source_url: $source_url,
  author: $author,
  capture_timestamp: datetime($capture_timestamp),
  valid_time_start: datetime($capture_timestamp),
  transaction_time: datetime(),
  note_path: $note_path,
  tags: $tags
})
CREATE (n:Note {path: $note_path})
CREATE (c)-[:RESULTED_IN]->(n)
RETURN c
```

**Relationship Type:** `:RESULTED_IN` (CaptureEvent resulted in Note)

### Step 7: Handle Response

**Success:**

- Cypher returns created node
- Return success with event_id

**Failure:**

- Connection failed: Log warning, return graceful degradation
- Query error: Log error, return failure
- Unknown error: Log error, return failure

## Error Handling and Graceful Degradation

### Neo4j Disabled (Config)

**Status:** Not an error, expected scenario

**Action:**

- Skip all Neo4j operations
- Return skipped: true
- Continue with Obsidian-only mode

**Return:**

```yaml
result:
  success: true
  skipped: true
  event_id: null
  error: null
  reason: 'neo4j_disabled'
```

### Connection Failed

**Cause:** Neo4j not running, Graphiti MCP not configured, network issue

**Action:**

- Log warning (not error)
- Degrade gracefully - inbox note still valid
- Do NOT block capture process

**Return:**

```yaml
result:
  success: false
  skipped: false
  event_id: null
  error: 'Neo4j connection failed'
  reason: 'connection_failed'
```

**Note in Processing Notes:** "Neo4j integration unavailable - capture saved to Obsidian only"

### Cypher Query Error

**Cause:** Invalid query syntax, constraint violation, database error

**Action:**

- Log error for debugging
- Degrade gracefully
- Do NOT block capture process

**Return:**

```yaml
result:
  success: false
  skipped: false
  event_id: null
  error: 'Cypher query error: {details}'
  reason: 'query_error'
```

### Graphiti Episode Failed

**Cause:** Episode format invalid, Graphiti processing error

**Action:**

- Log error
- Continue with manual node creation (Step 5)
- Episode is optional enhancement, not required

### Partial Success

If episode succeeds but manual node fails (or vice versa):

- Log mixed status
- Return success: false with details
- User can retry or proceed with partial data

## Security - Parameterized Queries

**CRITICAL:** NEVER use string concatenation for Cypher queries

**BAD (Vulnerable to injection):**

```javascript
const query = `CREATE (c:CaptureEvent {source: '${source_url}'})`;
```

**GOOD (Parameterized):**

```javascript
const query = 'CREATE (c:CaptureEvent {source: $source_url})';
const params = { source_url: source_url };
```

**Validation:**

- Validate all inputs before passing to parameters
- Escape special characters if needed
- Limit string lengths
- Never pass user input directly into query string

## Bi-Temporal Metadata Explained

**Purpose:** Track both when events happened in reality and when they were recorded

**valid_time_start:** "When did this capture actually occur?"

- Use capture_timestamp (when user captured the content)
- Represents real-world event time

**valid_time_end:** "When did this capture become invalid/outdated?"

- Usually null (captures don't expire)
- Could be set if capture is deleted or superseded

**transaction_time:** "When did we record this in the database?"

- Use current timestamp (`datetime()` in Cypher)
- Represents database operation time

**Use Cases:**

- "What did I capture on Nov 4th?" → Query by valid_time_start
- "What did I add to the database today?" → Query by transaction_time
- "What did I know on Nov 4th based on what was in the system then?" → Query valid_time <= Nov 4 AND transaction_time <= Nov 4

## Example Queries for Temporal Analysis

**All captures from November:**

```cypher
MATCH (c:CaptureEvent)
WHERE date(c.valid_time_start).month = 11
RETURN c
```

**Captures added to database this week:**

```cypher
MATCH (c:CaptureEvent)
WHERE c.transaction_time >= datetime() - duration('P7D')
RETURN c
```

**Point-in-time query (what did I know on Nov 1?):**

```cypher
MATCH (c:CaptureEvent)
WHERE c.valid_time_start <= datetime('2025-11-01')
  AND c.transaction_time <= datetime('2025-11-01T23:59:59Z')
RETURN c
```

## MCP Integration Details

### Required MCP Server

**Server:** graphiti-mcp (optional)

**Configuration:** (in MCP settings file)

```json
{
  "mcpServers": {
    "graphiti": {
      "command": "graphiti-mcp",
      "args": ["--neo4j-uri", "bolt://localhost:7687"]
    }
  }
}
```

### Graphiti Functions

**add_episode:**

- Adds episodic memory to graph
- Auto-extracts entities and relationships
- Timestamped

**execute_cypher (if available):**

- Runs custom Cypher queries
- Used for manual CaptureEvent node creation

**Alternative:** If execute_cypher not available, use create_node/create_relationship functions

## Testing

### Test Case 1: Neo4j Disabled

**Setup:** Set neo4j.enabled: false in config

**Expected:**

- skipped: true
- success: true
- No Neo4j calls made

### Test Case 2: Successful Creation

**Setup:** Neo4j running, Graphiti configured

**Expected:**

- success: true
- event_id: Valid UUID
- Node appears in Neo4j
- Relationship to Note exists

### Test Case 3: Connection Failed

**Setup:** Stop Neo4j service

**Expected:**

- success: false
- reason: "connection_failed"
- Capture process continues (graceful degradation)
- Inbox note still created

### Test Case 4: Query Error

**Setup:** Invalid Cypher syntax (programming error)

**Expected:**

- success: false
- error: Contains query error details
- Logged for debugging

### Test Case 5: Bi-Temporal Verification

**Action:** Create capture, query temporal properties

**Expected:**

- valid_time_start matches capture_timestamp
- valid_time_end is null
- transaction_time is recent (within 1 second)

## Integration with Other Tasks

**Inputs from:**

- `classify-content-type.md` - content_type, confidence
- `extract-metadata.md` - source_url, author, timestamp, tags
- `create-inbox-note.md` - note_path (required for relationship)

**Used by:**

- `*capture` command - Creates event after note
- `*process-inbox` command - Creates events for batch
- `*batch-process` command - Creates multiple events

**Validation:**

- `capture-quality-checklist.md` - Item 9 checks Neo4j creation or graceful skip

## Performance

- Target: < 1 second per event creation
- Graphiti episode: ~200-500ms
- Manual node creation: ~100-200ms
- Total: < 1 second typical

## Troubleshooting

**Issue:** All creates failing with "Neo4j disabled"

**Check:** config.yaml neo4j.enabled setting

**Issue:** Connection timeouts

**Check:**

1. Neo4j service running?
2. Graphiti MCP configured?
3. Network connectivity?
4. Check Graphiti logs

**Issue:** Constraint violations

**Cause:** event_id not unique or other constraint

**Solution:**

- Verify UUID generation
- Check for duplicate inserts
- Review Neo4j constraints

**Issue:** Bi-temporal queries return unexpected results

**Cause:** Timezone confusion or datetime format issues

**Solution:**

- Always use UTC
- Always use ISO 8601 format
- Test temporal queries with known data

## Config File Example

```yaml
# expansion-packs/bmad-obsidian-2nd-brain/config.yaml

neo4j:
  enabled: true # Set to false to disable Neo4j integration
  uri: 'bolt://localhost:7687'
  database: 'neo4j'

obsidian:
  vault_path: '/path/to/vault'
  inbox_dir: '/inbox'
```

## Fallback Behavior Summary

| Scenario                 | Behavior                          |
| ------------------------ | --------------------------------- |
| Neo4j disabled in config | Skip gracefully, continue         |
| Connection failed        | Log warning, continue             |
| Query error              | Log error, continue               |
| Graphiti episode fails   | Continue with manual node         |
| Manual node fails        | Log error, continue               |
| Both fail                | Log error, inbox note still valid |

**Key Principle:** Neo4j is an enhancement, not a requirement. Inbox note is the source of truth.

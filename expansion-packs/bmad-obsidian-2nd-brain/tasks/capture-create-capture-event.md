<!-- Powered by BMAD™ Core -->

# Capture: Create Capture Event (OPTIONAL)

**🔷 OPTIONAL TASK:** This task requires Neo4j enabled. Gracefully skips if disabled.

## Purpose

Create temporal CaptureEvent node in Neo4j graph database for evolution tracking. This enables temporal RAG queries like "Show me what I captured last week" and "How has my understanding of X evolved over time?"

**OPTIONAL:** This task is only executed if `neo4j.enabled: true` in config.yaml. If Neo4j is disabled or Graphiti MCP unavailable, the task gracefully skips with success=true, skipped=true.

## Inputs

- **inbox_note_path** (String, required): Path to created inbox note (from capture-create-inbox-note task)
- **metadata** (Object, required): Extracted metadata
  - `source_url` (String): Source URL or "Unknown"
  - `author` (String): Author name or "Unknown"
  - `title` (String): Title
  - `timestamp` (String): ISO8601 timestamp
- **content_type** (String, required): Classification result (one of 6 types)
- **config** (Object, required): Neo4j configuration from config.yaml
  - `neo4j.enabled` (Boolean): Whether Neo4j is enabled
  - `neo4j.uri` (String): Neo4j connection URI (if enabled)
  - `neo4j.username` (String): Username (if enabled)
  - `neo4j.password` (String): Password (if enabled)
  - `neo4j.database` (String): Database name (if enabled)

## Procedure

### Step 1: Check Neo4j Enabled in Config

**Read configuration:**
- Load config file: `expansion-packs/bmad-obsidian-2nd-brain/config.yaml`
- Parse YAML structure
- Extract `neo4j.enabled` boolean value

**Decision logic:**
```
IF neo4j.enabled == false OR neo4j.enabled == undefined:
  Log info: "Neo4j disabled, temporal tracking skipped"
  Return {success: true, skipped: true, capture_event_id: null}
  EXIT (graceful skip)

IF neo4j.enabled == true:
  Proceed to Step 2 (Graphiti MCP integration)
```

**Graceful degradation:**
- Neo4j disabled is NOT an error
- Return success=true with skipped=true
- Allow capture workflow to continue without temporal tracking
- Log informational message, not warning or error

### Step 2: Validate Neo4j Configuration

**If neo4j.enabled == true, verify configuration:**
- ✓ `neo4j.uri` exists and is non-empty
- ✓ `neo4j.username` exists and is non-empty
- ✓ `neo4j.password` exists and is non-empty
- ✓ `neo4j.database` exists and is non-empty

**If validation fails:**
- Log warning: "Neo4j enabled but configuration incomplete, skipping temporal tracking"
- Return {success: true, skipped: true, capture_event_id: null}
- Graceful degradation (not blocking error)

### Step 3: Generate Capture ID

Generate unique capture event identifier:

**Use UUID v4:**
- Example: `c7e4f1a2-9b3d-4c8e-a5f2-1d6b9e3c4a8f`
- Ensures global uniqueness
- No collision concerns

**Store for later use:**
- `capture_id` = generated UUID
- Will be used as episode identifier in Graphiti

### Step 4: Prepare CaptureEvent Node Properties

Construct temporal event properties for bi-temporal graph:

**Core properties:**
```json
{
  "capture_id": "[UUID v4]",
  "timestamp": "[ISO8601 datetime]",
  "source_url": "[metadata.source_url]",
  "content_type": "[content_type]",
  "note_path": "[inbox_note_path relative to vault]",
  "author": "[metadata.author]",
  "title": "[metadata.title]"
}
```

**Bi-temporal metadata:**
- `valid_time_start`: When capture occurred (use metadata.timestamp)
  - Represents "when did this knowledge enter the real world?"
  - Used for queries like: "What did I learn last week?"

- `transaction_time`: When recorded in database (auto-set by Neo4j on INSERT)
  - Represents "when did we record this in the system?"
  - Used for queries like: "What was added to the graph today?"

**Example properties:**
```json
{
  "capture_id": "c7e4f1a2-9b3d-4c8e-a5f2-1d6b9e3c4a8f",
  "timestamp": "2025-11-06T10:30:00Z",
  "source_url": "https://example.com/deep-work",
  "content_type": "concept",
  "note_path": "inbox/2025-11-06-1030-deep-work-principles.md",
  "author": "Cal Newport",
  "title": "Deep Work Principles",
  "valid_time_start": "2025-11-06T10:30:00Z"
}
```

### Step 5: Construct Graphiti Episode Object

Map capture data to Graphiti episode format:

**Episode structure:**
```json
{
  "name": "Capture: [title]",
  "episode_body": "[raw_content from classified_content]",
  "source_description": "[author] - [source_url]",
  "reference_time": "[ISO8601 timestamp]"
}
```

**Field mappings:**
- `name`: Prefix "Capture: " + metadata.title
  - Example: "Capture: Deep Work Principles"
  - Distinguishes capture events from other episode types

- `episode_body`: Full captured content text
  - Use classified_content.raw_content
  - Preserve original text for semantic search
  - Max 1MB size (enforced in classification step)

- `source_description`: Structured attribution
  - Format: "[author] - [source_url]"
  - Example: "Cal Newport - https://example.com/deep-work"
  - Preserves provenance for citation

- `reference_time`: When capture occurred
  - Use metadata.timestamp (ISO8601 format)
  - Maps to valid_time_start in bi-temporal model

**Example episode:**
```json
{
  "name": "Capture: Deep Work Principles",
  "episode_body": "Deep work is the ability to focus without distraction on a cognitively demanding task. It enables deep understanding and high-quality creative output. Unlike shallow work, deep work produces lasting value and is increasingly rare in our distracted world.",
  "source_description": "Cal Newport - https://example.com/deep-work",
  "reference_time": "2025-11-06T10:30:00Z"
}
```

### Step 6: Call Graphiti MCP to Add Episode

Use Graphiti MCP `graphiti.add_episode` tool:

**MCP Call Parameters:**
```javascript
{
  name: "Capture: Deep Work Principles",
  episode_body: "Deep work is the ability to focus...",
  source_description: "Cal Newport - https://example.com/deep-work",
  reference_time: "2025-11-06T10:30:00Z"
}
```

**Expected MCP Response:**
```javascript
{
  success: true,                         // Boolean: operation success
  episode_id: "ep_c7e4f1a2",            // String: unique episode ID
  nodes: [{...}],                        // Array: extracted entities
  edges: [{...}],                        // Array: relationships
  error: null                            // String: error if failure, null if success
}
```

**If Graphiti MCP unavailable:**
- Catch connection error
- Proceed to Step 9 (graceful degradation)
- Do NOT treat as blocking error

### Step 7: Extract Episode ID from Response

**If MCP call successful (success == true):**
- Extract `episode_id` from response
- Store as `capture_event_id`
- Example: `"ep_c7e4f1a2"`
- This ID can be used for later queries to retrieve the episode

**If MCP call failed (success == false):**
- Extract `error` message from response
- Log error details
- Proceed to Step 9 (graceful degradation)

### Step 8: Verify Episode Created and Log Success

**Verification (optional):**
- Could query Graphiti to confirm episode exists
- For performance, trust MCP success response
- Skip verification to meet < 1s target

**Log success:**
- Log info: "CaptureEvent created in Neo4j: episode_id=[id]"
- Log episode_id for debugging
- Update capture statistics (optional)

### Step 9: Handle Errors Gracefully (Graceful Degradation)

**If any error occurs during Neo4j interaction:**

**Connection errors:**
- Graphiti MCP unavailable
- Neo4j connection failed
- Authentication failed
- Timeout

**Response:**
- Log warning: "Graphiti MCP unavailable, operating in Obsidian-only mode"
- OR: "Neo4j connection failed, capture saved to Obsidian only"
- Return {success: true, skipped: true, capture_event_id: null, error: "[details]"}
- **KEY:** Return success=true, NOT false
- Capture workflow continues (not blocking)

**Episode creation errors:**
- Episode validation failed
- Duplicate episode_id (rare with UUID)
- Graph constraint violation

**Response:**
- Log error: "Episode creation failed: [details]"
- Return {success: true, skipped: true, capture_event_id: null, error: "[details]"}
- Continue capture workflow

**Philosophy:**
- Neo4j is OPTIONAL enhancement, not required
- Failure to create episode should NOT block inbox note creation
- Always return success=true (graceful degradation)
- Only return success=false for unexpected/fatal errors (very rare)

### Step 10: Return Success Response

**If episode created successfully:**
```json
{
  "capture_event_id": "ep_c7e4f1a2",
  "success": true,
  "skipped": false,
  "error": null
}
```

**If Neo4j disabled:**
```json
{
  "capture_event_id": null,
  "success": true,
  "skipped": true,
  "error": null
}
```

**If Neo4j error (graceful degradation):**
```json
{
  "capture_event_id": null,
  "success": true,
  "skipped": true,
  "error": "Graphiti MCP unavailable, operating in Obsidian-only mode"
}
```

**Only return success=false for:**
- Config file unreadable (fatal)
- Invalid config YAML (fatal)
- Unexpected/unhandled exceptions (fatal)

## Outputs

- **capture_event_id** (String or null): Episode ID from Neo4j/Graphiti, or null if disabled/failed
- **success** (Boolean): `true` in almost all cases (including disabled/errors), `false` only for fatal errors
- **skipped** (Boolean): `true` if Neo4j disabled or error occurred, `false` if episode created successfully
- **error** (String or null): Error message if error occurred, null if successful or disabled

## Graphiti MCP Integration

### MCP Tool: graphiti.add_episode

**Purpose:** Add episode to Graphiti temporal knowledge graph, which stores events with bi-temporal tracking

**Parameters:**

- **name** (String, required): Episode title
  - Format: "Capture: [title]"
  - Example: "Capture: Deep Work Principles"
  - Used for episode identification in queries

- **episode_body** (String, required): Episode content/description
  - Full captured content text
  - Used for semantic search and entity extraction
  - Max 1MB size

- **source_description** (String, required): Source attribution
  - Format: "[author] - [source_url]"
  - Example: "Cal Newport - https://example.com/deep-work"
  - Preserves provenance

- **reference_time** (String, required): ISO8601 timestamp when episode occurred
  - Example: "2025-11-06T10:30:00Z"
  - Maps to valid_time_start in bi-temporal model

**Response:**
```javascript
{
  success: true,                         // Boolean: operation status
  episode_id: "ep_c7e4f1a2",            // String: unique episode ID (UUID-based)
  nodes: [                               // Array: entities extracted from episode
    {
      id: "node_123",
      name: "Deep Work",
      type: "Concept",
      properties: {...}
    }
  ],
  edges: [                               // Array: relationships extracted
    {
      from: "node_123",
      to: "node_456",
      type: "RELATES_TO",
      properties: {...}
    }
  ],
  error: null                            // String: error message if failure, null if success
}
```

**Example MCP Call:**
```javascript
graphiti.add_episode({
  name: "Capture: Deep Work Principles",
  episode_body: "Deep work is the ability to focus without distraction on a cognitively demanding task. It enables deep understanding and high-quality creative output. Unlike shallow work, deep work produces lasting value and is increasingly rare in our distracted world.",
  source_description: "Cal Newport - https://example.com/deep-work",
  reference_time: "2025-11-06T10:30:00Z"
})
```

**Expected Response:**
```javascript
{
  success: true,
  episode_id: "ep_c7e4f1a2-9b3d-4c8e-a5f2-1d6b9e3c4a8f",
  nodes: [
    {
      id: "node_deep_work_001",
      name: "Deep Work",
      type: "Concept",
      properties: {
        description: "Ability to focus without distraction on cognitively demanding tasks"
      }
    },
    {
      id: "node_cal_newport",
      name: "Cal Newport",
      type: "Author",
      properties: {}
    }
  ],
  edges: [
    {
      from: "node_cal_newport",
      to: "node_deep_work_001",
      type: "AUTHORED",
      properties: {}
    }
  ],
  error: null
}
```

## Bi-Temporal Metadata Documentation

### What is Bi-Temporal Data?

**Bi-temporal data** tracks two independent timelines:
1. **Valid Time:** When the fact was true in the real world
2. **Transaction Time:** When the fact was recorded in the database

### Valid Time vs Transaction Time

**Valid Time (`valid_time_start`):**
- **Meaning:** When did the capture event occur in the real world?
- **Source:** `metadata.timestamp` (when user captured the content)
- **Example:** "I captured this article on Nov 6, 2025 at 10:30 AM"
- **Query use:** "Show me what I captured last week"

**Transaction Time (`transaction_time`):**
- **Meaning:** When was this event recorded in the Neo4j database?
- **Source:** Auto-set by Neo4j on INSERT (system timestamp)
- **Example:** "This episode was added to the graph on Nov 6, 2025 at 10:30:15 AM"
- **Query use:** "Show me what was added to the graph today"

### Why Bi-Temporal Tracking?

**Use Case 1: Historical Queries**
- Query: "What did I capture last Monday?"
- Uses: `valid_time_start` (when capture occurred)
- Example: Find all captures with valid_time between Monday 00:00 and Monday 23:59

**Use Case 2: System Audit**
- Query: "What was added to the graph in the last hour?"
- Uses: `transaction_time` (when recorded in DB)
- Example: Find all episodes with transaction_time in last 60 minutes

**Use Case 3: Temporal Evolution**
- Query: "How has my understanding of 'Deep Work' evolved over time?"
- Uses: Both `valid_time` (sequence of captures) and `transaction_time` (when I learned it)
- Example: Show timeline of all captures mentioning "Deep Work", ordered by valid_time

**Use Case 4: Retroactive Capture**
- Scenario: User captures old content (article from 2020) on Nov 6, 2025
- valid_time_start: 2020-03-15 (when article was published)
- transaction_time: 2025-11-06 (when captured today)
- Allows distinguishing "when it was written" from "when I found it"

### Example Temporal Queries

**Query 1: Last week's captures**
```cypher
MATCH (e:Episode)
WHERE e.valid_time_start >= datetime() - duration({days: 7})
RETURN e
ORDER BY e.valid_time_start DESC
```

**Query 2: Recent graph additions**
```cypher
MATCH (e:Episode)
WHERE e.transaction_time >= datetime() - duration({hours: 24})
RETURN e
ORDER BY e.transaction_time DESC
```

**Query 3: Evolution of concept understanding**
```cypher
MATCH (e:Episode)
WHERE e.episode_body CONTAINS "Deep Work"
RETURN e
ORDER BY e.valid_time_start ASC
```

## Graceful Degradation

### Scenario 1: Neo4j Disabled in Config

**Condition:** `neo4j.enabled: false` in config.yaml

**Response:**
- Skip Neo4j integration entirely (exit at Step 1)
- Log info: "Neo4j disabled, temporal tracking skipped"
- Return: `{success: true, skipped: true, capture_event_id: null}`

**Result:** Capture workflow continues successfully in Obsidian-only mode

### Scenario 2: Graphiti MCP Unavailable

**Condition:** Graphiti MCP not configured or not responding

**Response:**
- Catch connection error during MCP call (Step 6)
- Log warning: "Graphiti MCP unavailable, operating in Obsidian-only mode"
- Return: `{success: true, skipped: true, capture_event_id: null, error: "MCP unavailable"}`

**Result:** Capture workflow continues, inbox note created, no graph event

### Scenario 3: Neo4j Connection Failed

**Condition:** Neo4j database unreachable (network issue, credentials wrong, service down)

**Response:**
- Catch connection error from Graphiti MCP
- Log warning: "Neo4j connection failed, capture saved to Obsidian only"
- Return: `{success: true, skipped: true, capture_event_id: null, error: "Connection failed"}`

**Result:** Capture workflow continues, user can fix Neo4j later and backfill if needed

### Scenario 4: Episode Creation Failed

**Condition:** Graphiti rejects episode (validation error, constraint violation)

**Response:**
- Log error: "Episode creation failed: [MCP error details]"
- Return: `{success: true, skipped: true, capture_event_id: null, error: "[details]"}`

**Result:** Capture workflow continues, error logged for troubleshooting

### Key Principle: Always Succeed

**Philosophy:**
- Neo4j is an OPTIONAL enhancement, not a requirement
- Failure to create graph event should NEVER block inbox note creation
- Return `success: true` in all degradation scenarios
- Only return `success: false` for fatal/unexpected errors

**Benefits:**
- User can capture content even if Neo4j is down
- System remains functional without graph database
- Graceful degradation to Obsidian-only mode
- Can backfill graph later if needed

## Error Handling

### Error 1: Neo4j Connection Failed

**Condition:** Cannot connect to Neo4j (network, credentials, service down)

**Response:** Graceful degradation
- Log warning: "Neo4j connection failed, capture saved to Obsidian only"
- Return: `{success: true, skipped: true, capture_event_id: null, error: "Connection failed: [details]"}`

**Blocking:** NO (graceful degradation)

### Error 2: Graphiti MCP Unavailable

**Condition:** Graphiti MCP not installed or not responding

**Response:** Graceful degradation
- Log warning: "Graphiti MCP unavailable, operating in Obsidian-only mode"
- Return: `{success: true, skipped: true, capture_event_id: null, error: "MCP unavailable"}`

**Remediation:** Install Graphiti MCP and configure in Claude Desktop/Cursor settings

**Blocking:** NO (graceful degradation)

### Error 3: Episode Creation Failed

**Condition:** Graphiti rejects episode (validation error, constraint violation, duplicate)

**Response:** Graceful degradation
- Log error: "Episode creation failed: [MCP error details]"
- Return: `{success: true, skipped: true, capture_event_id: null, error: "Creation failed: [details]"}`

**Blocking:** NO (graceful degradation)

### Error 4: Config Parse Error

**Condition:** config.yaml cannot be read or parsed

**Response:** Treat as Neo4j disabled
- Log warning: "Config parse error, treating Neo4j as disabled"
- Return: `{success: true, skipped: true, capture_event_id: null, error: "Config parse error"}`

**Blocking:** NO (treat as disabled)

### Error 5: Episode Body Too Large

**Condition:** `episode_body` exceeds 1MB size limit

**Response:**
- Truncate episode_body to 1MB
- Log warning: "Episode body truncated to 1MB limit"
- Continue with truncated content
- Return success with episode_id

**Blocking:** NO (truncate and continue)

## Security

### No Cypher Injection Risk

**Why safe:**
- Using Graphiti MCP abstraction layer
- No direct Cypher query construction
- MCP handles parameterization and escaping
- Episode data passed as structured parameters, not string concatenation

**Example safe call:**
```javascript
// Safe: Using MCP with structured parameters
graphiti.add_episode({
  name: "Capture: Example",
  episode_body: "User-provided content with ' quotes \" and special chars",
  source_description: "Author - https://example.com",
  reference_time: "2025-11-06T10:30:00Z"
})
```

**Not vulnerable to:**
- Cypher injection via episode_body
- SQL injection (not using SQL)
- Command injection

### Credentials Storage

**Configuration:**
- Credentials stored in config.yaml (user-controlled file)
- Not hardcoded in task files
- User manages credential security

**Best practices:**
- Use environment variables for sensitive data (optional)
- Restrict config.yaml file permissions (chmod 600)
- Do not commit config.yaml to public repositories

**No credential exposure:**
- Credentials never logged
- Error messages sanitized (no credentials in error text)
- MCP handles credential management

### Content Validation

**Episode body size limit:**
- Max 1MB per episode
- Prevents DoS attacks via oversized content
- Enforced in earlier classification step
- Verify size before MCP call

**Content sanitization:**
- Already sanitized in classification step
- No additional sanitization needed here
- Trust input from previous validated tasks

### Authentication

**Neo4j authentication:**
- Username/password from config.yaml
- Managed by Graphiti MCP
- No credential validation in this task (trust config)

**MCP authentication:**
- Handled by MCP server configuration
- Outside scope of this task

## Performance Target

**Target execution time:** < 1 second per episode creation

**Performance breakdown:**
- Config check: < 10ms
- UUID generation: < 1ms
- Episode object construction: < 10ms
- Graphiti MCP call: < 800ms
- Response parsing: < 10ms
- Logging: < 10ms
- Total: ~841ms (well under 1s target)

**Performance considerations:**
- Single MCP call (no query chaining)
- No entity extraction in this task (Graphiti handles it)
- Minimal data validation (trust upstream tasks)
- No external API calls besides Graphiti MCP

**Monitoring:**
- Log episode creation time
- Alert if average time exceeds 1s
- Track MCP latency separately
- Monitor Neo4j connection health

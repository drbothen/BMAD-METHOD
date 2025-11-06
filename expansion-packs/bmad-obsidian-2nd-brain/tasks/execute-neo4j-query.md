<!-- Powered by BMAD™ Core -->

# execute-neo4j-query

**Purpose:** Execute temporal and graph queries against Neo4j database via Graphiti MCP (bi-temporal knowledge graph)

**Performance Budget:** <1 second per query

**Status:** OPTIONAL - Graceful degradation when Neo4j unavailable

## Overview

Neo4j Graphiti MCP provides bi-temporal graph database capabilities for:
- **Temporal evolution queries** - How concepts changed over time
- **Relationship traversal** - Find connections between entities
- **Causal chain analysis** - Trace cause-effect relationships
- **Entity extraction** - Extract entities from notes and link to graph

This integration is **optional**. The agent degrades gracefully if Neo4j is not configured.

## MCP Integration Architecture

### Graphiti MCP Tools

**Capabilities:**
- Execute Cypher queries (parameterized only)
- Temporal queries (valid time vs transaction time)
- Graph traversal with hop limits
- Entity extraction and linking
- Relationship creation with bi-temporal tracking

**Tool Invocations (examples):**
```
mcp__graphiti__execute_cypher(
  query: "MATCH (n:Note {path: $path}) RETURN n",
  parameters: {path: "atomic/zettelkasten.md"}
)

mcp__graphiti__temporal_query(
  entity: "Zettelkasten",
  start_date: "2024-01-01",
  end_date: "2024-11-05"
)

mcp__graphiti__traverse_graph(
  start_node: "atomic/zettelkasten.md",
  relationship_types: ["CONCEPTUALLY_RELATED", "INFLUENCES"],
  max_hops: 2
)
```

## Query Execution Strategies

### Strategy 1: Temporal Evolution Queries

**Use:** Queries about how concepts evolved over time

**Query Type:** Bi-temporal query using valid_time dimension

**Algorithm:**
```
1. Extract concept and date range from query parameters

2. Execute Graphiti temporal query:
   - Find all versions of entity within date range
   - Track property changes over time
   - Include related entities that existed at each time point

3. Sort results chronologically

4. Identify key changes (additions, deletions, modifications)
```

**Example Cypher (via Graphiti MCP):**
```cypher
// Find temporal evolution of a concept
MATCH (n:Note {path: $note_path})
MATCH (n)-[r:HAS_VERSION]->(v:Version)
WHERE v.valid_time_start >= datetime($start_date)
  AND v.valid_time_start <= datetime($end_date)
RETURN
  v.valid_time_start AS timestamp,
  v.content AS content_snapshot,
  v.properties AS metadata_snapshot
ORDER BY v.valid_time_start ASC
```

**Parameters (safely escaped):**
```javascript
const params = {
  note_path: validate_note_path(note_path),
  start_date: validate_date(start_date),
  end_date: validate_date(end_date)
}

const results = await mcp__graphiti__execute_cypher(query, params)
```

**Example Implementation:**
```javascript
async function execute_temporal_evolution_query(concept, start_date, end_date) {
  try {
    // Find notes matching concept
    const concept_notes = await find_notes_by_concept(concept)

    if (concept_notes.length === 0) {
      log_info(`No notes found for concept: ${concept}`)
      return []
    }

    // Execute temporal query for each note
    const temporal_results = []

    for (const note of concept_notes) {
      const query = `
        MATCH (n:Note {path: $note_path})
        OPTIONAL MATCH (n)-[r:HAS_VERSION]->(v:Version)
        WHERE v.valid_time_start >= datetime($start_date)
          AND v.valid_time_start <= datetime($end_date)
        RETURN
          n.path AS note_path,
          n.title AS note_title,
          v.valid_time_start AS timestamp,
          v.content AS content_snapshot,
          v.properties AS properties
        ORDER BY v.valid_time_start ASC
      `

      const params = {
        note_path: validate_note_path(note.path),
        start_date: validate_date(start_date),
        end_date: validate_date(end_date)
      }

      const result = await mcp__graphiti__execute_cypher(query, params)
      temporal_results.push(...result)
    }

    return temporal_results

  } catch (error) {
    if (error.code === 'NEO4J_UNAVAILABLE') {
      log_warning('Neo4j unavailable, temporal queries not supported')
      return []
    }
    throw error
  }
}
```

### Strategy 2: Causal Chain Queries

**Use:** "Why does X happen?" queries

**Query Type:** Graph traversal following causal relationships

**Algorithm:**
```
1. Identify source concept (X)

2. Traverse graph following causal relationship types:
   - CAUSES
   - LEADS_TO
   - INFLUENCES
   - SUPPORTS (for supporting evidence)

3. Build causal chain from source to effects

4. Include confidence scores for each link
```

**Example Cypher:**
```cypher
// Find causal chain
MATCH path = (start:Note {path: $start_path})
  -[:CAUSES|LEADS_TO|INFLUENCES*1..3]->(end:Note)
WHERE end.path = $end_path OR end.title CONTAINS $target_concept
RETURN
  [node IN nodes(path) | node.title] AS causal_chain,
  [rel IN relationships(path) | type(rel)] AS relationship_types,
  [rel IN relationships(path) | rel.strength] AS confidence_scores,
  length(path) AS chain_length
ORDER BY chain_length ASC
LIMIT 10
```

**Parameters:**
```javascript
const params = {
  start_path: validate_note_path(start_path),
  end_path: validate_note_path(end_path),
  target_concept: validate_concept(concept)
}
```

**Example Implementation:**
```javascript
async function execute_causal_chain_query(source_concept, target_concept) {
  try {
    // Find notes matching source concept
    const source_notes = await find_notes_by_concept(source_concept)

    if (source_notes.length === 0) {
      log_info(`No notes found for source concept: ${source_concept}`)
      return []
    }

    const causal_chains = []

    for (const source of source_notes) {
      const query = `
        MATCH path = (start:Note {path: $start_path})
          -[r:CAUSES|LEADS_TO|INFLUENCES*1..3]->(end:Note)
        WHERE end.title CONTAINS $target_concept
        RETURN
          [node IN nodes(path) | {
            title: node.title,
            path: node.path
          }] AS nodes,
          [rel IN relationships(path) | {
            type: type(rel),
            strength: rel.strength,
            context: rel.context
          }] AS relationships,
          length(path) AS chain_length
        ORDER BY chain_length ASC
        LIMIT 10
      `

      const params = {
        start_path: validate_note_path(source.path),
        target_concept: validate_concept(target_concept)
      }

      const result = await mcp__graphiti__execute_cypher(query, params)
      causal_chains.push(...result)
    }

    return causal_chains

  } catch (error) {
    if (error.code === 'NEO4J_UNAVAILABLE') {
      log_warning('Neo4j unavailable, causal queries not supported')
      return []
    }
    throw error
  }
}
```

### Strategy 3: Relationship Traversal Queries

**Use:** Exploratory queries to "find everything related to X"

**Query Type:** Graph traversal with configurable hop limit

**Algorithm:**
```
1. Identify starting concept

2. Traverse graph up to N hops (default: 2)

3. Include all relationship types:
   - CONCEPTUALLY_RELATED
   - INFLUENCES
   - SUPPORTS
   - CONTRADICTS
   - ELABORATES

4. Rank by:
   - Hop distance (closer = higher rank)
   - Relationship strength
   - Number of paths to node
```

**Example Cypher:**
```cypher
// Traverse graph from starting point
MATCH path = (start:Note {path: $start_path})
  -[r:CONCEPTUALLY_RELATED|INFLUENCES|SUPPORTS|CONTRADICTS|ELABORATES*1..2]->
  (related:Note)
RETURN DISTINCT
  related.path AS note_path,
  related.title AS note_title,
  MIN(length(path)) AS min_hops,
  COUNT(path) AS path_count,
  AVG([rel IN relationships(path) | rel.strength]) AS avg_strength
ORDER BY min_hops ASC, path_count DESC, avg_strength DESC
LIMIT 50
```

**Parameters:**
```javascript
const params = {
  start_path: validate_note_path(start_path)
}
```

**Example Implementation:**
```javascript
async function execute_relationship_traversal_query(concept, max_hops = 2) {
  try {
    const source_notes = await find_notes_by_concept(concept)

    if (source_notes.length === 0) {
      log_info(`No notes found for concept: ${concept}`)
      return []
    }

    const related_notes = []

    for (const source of source_notes) {
      const query = `
        MATCH path = (start:Note {path: $start_path})
          -[r*1..${max_hops}]->(related:Note)
        WHERE ALL(rel IN relationships(path) WHERE type(rel) IN [
          'CONCEPTUALLY_RELATED', 'INFLUENCES', 'SUPPORTS',
          'CONTRADICTS', 'ELABORATES'
        ])
        RETURN DISTINCT
          related.path AS note_path,
          related.title AS note_title,
          MIN(length(path)) AS min_hops,
          COUNT(path) AS path_count,
          AVG([rel IN relationships(path) | rel.strength]) AS avg_strength,
          [rel IN relationships(path) | type(rel)] AS relationship_types
        ORDER BY min_hops ASC, path_count DESC, avg_strength DESC
        LIMIT 50
      `

      const params = {
        start_path: validate_note_path(source.path)
      }

      const result = await mcp__graphiti__execute_cypher(query, params)
      related_notes.push(...result)
    }

    // Deduplicate
    const unique_notes = deduplicate_by_path(related_notes)

    return unique_notes

  } catch (error) {
    if (error.code === 'NEO4J_UNAVAILABLE') {
      log_warning('Neo4j unavailable, relationship traversal not supported')
      return []
    }
    throw error
  }
}
```

### Strategy 4: Comparative Queries (Graph Context)

**Use:** Enrich comparative queries with graph relationships

**Query Type:** Parallel subgraph queries for each subject

**Algorithm:**
```
1. For each subject in comparison:
   - Find notes matching subject
   - Retrieve immediate relationships (1 hop)
   - Extract key properties

2. Compare:
   - Shared relationships (common connections)
   - Unique relationships (differentiators)
   - Relationship strengths
```

**Example Cypher:**
```cypher
// Find relationships for one subject
MATCH (n:Note {path: $note_path})
OPTIONAL MATCH (n)-[r]->(related:Note)
RETURN
  n.path AS note_path,
  n.title AS note_title,
  COLLECT({
    relationship_type: type(r),
    strength: r.strength,
    target_title: related.title,
    target_path: related.path
  }) AS relationships
```

**Example Implementation:**
```javascript
async function execute_comparative_query_with_graph(subjects) {
  try {
    const results_by_subject = {}

    for (const subject of subjects) {
      const notes = await find_notes_by_concept(subject)

      const relationships = []

      for (const note of notes) {
        const query = `
          MATCH (n:Note {path: $note_path})
          OPTIONAL MATCH (n)-[r]->(related:Note)
          RETURN
            n.path AS note_path,
            n.title AS note_title,
            COLLECT({
              relationship_type: type(r),
              strength: r.strength,
              target_title: related.title,
              target_path: related.path,
              context: r.context
            }) AS relationships
        `

        const params = {
          note_path: validate_note_path(note.path)
        }

        const result = await mcp__graphiti__execute_cypher(query, params)
        relationships.push(...result)
      }

      results_by_subject[subject] = {
        notes: notes,
        relationships: relationships
      }
    }

    return results_by_subject

  } catch (error) {
    if (error.code === 'NEO4J_UNAVAILABLE') {
      log_warning('Neo4j unavailable, graph context not available for comparison')
      return {}
    }
    throw error
  }
}
```

## Security: Cypher Injection Prevention

**CRITICAL:** ALWAYS use parameterized queries. NEVER concatenate user input into Cypher strings.

### Safe Query Pattern

```javascript
// ✅ SAFE: Parameterized query
const query = `
  MATCH (n:Note {path: $note_path})
  WHERE n.title CONTAINS $search_term
  RETURN n
`

const params = {
  note_path: validate_note_path(user_input_path),  // Validated
  search_term: validate_concept(user_input_term)   // Sanitized
}

const results = await mcp__graphiti__execute_cypher(query, params)
```

### Unsafe Query Pattern

```javascript
// ❌ UNSAFE: String concatenation (NEVER DO THIS)
const query = `
  MATCH (n:Note {path: '${user_input_path}'})
  RETURN n
`
// Vulnerable to injection attacks!
```

### Attack Example

```
User input: "'})-[r:OWNS]->(attacker) WHERE 1=1 //"

Unsafe query:
MATCH (n:Note {path: ''})-[r:OWNS]->(attacker) WHERE 1=1 //'})
→ Creates unauthorized relationships, exposes data
```

**Defense:** Parameterized queries eliminate all injection vectors.

## Graceful Degradation

Neo4j integration is **optional**. The agent must work without it.

### Detection

```javascript
async function check_neo4j_availability() {
  try {
    await mcp__graphiti__execute_cypher('RETURN 1 AS test', {})
    return true
  } catch (error) {
    log_info('Neo4j Graphiti MCP unavailable, temporal/graph queries disabled')
    return false
  }
}
```

### Fallback Behavior

```javascript
async function execute_temporal_query(concept, start_date, end_date) {
  const neo4j_available = await check_neo4j_availability()

  if (neo4j_available) {
    // Use Neo4j for bi-temporal queries
    return await execute_temporal_evolution_query(concept, start_date, end_date)
  } else {
    // Fallback to Obsidian file metadata (less precise)
    log_warning('Neo4j unavailable, using Obsidian fallback for temporal query')
    return await execute_temporal_query_obsidian_fallback(concept, start_date, end_date)
  }
}
```

### User Communication

When Neo4j is unavailable, inform the user:

```
"Neo4j graph database is not configured. Temporal and causal queries will use basic Obsidian search.

To enable advanced graph queries:
1. Install Neo4j locally or use Neo4j Aura
2. Configure Graphiti MCP in Claude Desktop config
3. Restart Claude Desktop

Current query will continue using available data sources."
```

## Timeout Handling

**Neo4j Query Timeout:** 1 second

```javascript
async function execute_neo4j_query_with_timeout(query, params) {
  const timeout_ms = 1000

  const timeout_promise = new Promise((_, reject) => {
    setTimeout(() => {
      reject(new TimeoutError('Neo4j query exceeded 1 second timeout'))
    }, timeout_ms)
  })

  try {
    const result = await Promise.race([
      mcp__graphiti__execute_cypher(query, params),
      timeout_promise
    ])

    return result

  } catch (error) {
    if (error instanceof TimeoutError) {
      log_warning(error.message)
      return []  // Return empty results on timeout
    }
    throw error
  }
}
```

## Error Messages

### Error 1: Neo4j Unavailable
```
"Neo4j graph database is not available. Temporal and causal queries are limited to Obsidian fallback mode.

Your query will continue using available sources."
```

### Error 2: Invalid Cypher Query
```
"Graph query failed due to invalid syntax. This is an internal error.
Please report this issue with your query: '[user_query]'"
```

### Error 3: No Graph Data
```
"No graph relationships found for '[concept]'. This may be because:
- The concept hasn't been linked by the Semantic Linker Agent yet
- The concept is too new (try running Semantic Linker first)
- The concept doesn't exist in your vault"
```

### Error 4: Timeout
```
"Neo4j query timed out after 1 second. This may be due to:
- Complex graph traversal (try reducing scope)
- Large dataset (consider indexing)
- Neo4j performance issues (check database status)"
```

## Result Structure

Return structured results for merging:

```yaml
results:
  - source: "neo4j_graphiti"
    query_type: "temporal_evolution"
    note_path: "atomic/zettelkasten.md"
    note_title: "Zettelkasten Method"
    timeline:
      - timestamp: "2024-03-15T10:23:00Z"
        event: "Note created"
        content_snapshot: "Initial definition of Zettelkasten..."
      - timestamp: "2024-05-20T14:30:00Z"
        event: "Content modified"
        content_snapshot: "Expanded with atomic notes principle..."
      - timestamp: "2024-09-10T09:15:00Z"
        event: "Relationships added"
        new_links: ["atomic-notes.md", "slip-box.md"]

  - source: "neo4j_graphiti"
    query_type: "causal_chain"
    causal_path:
      - note_path: "atomic/atomic-notes.md"
        note_title: "Atomic Notes"
        relationship_type: "LEADS_TO"
        strength: 0.85
        context: "Atomic notes enable modular thinking"
      - note_path: "atomic/improved-recall.md"
        note_title: "Improved Recall"
        relationship_type: "CAUSES"
        strength: 0.78
        context: "Modular thinking improves memory consolidation"

query_metadata:
  neo4j_enabled: true
  neo4j_available: true
  query_duration_ms: 650
  timeout_occurred: false
```

## Performance Monitoring

Track query performance:

```javascript
async function execute_neo4j_query_with_monitoring(query, params) {
  const start_time = Date.now()

  try {
    const result = await execute_neo4j_query_with_timeout(query, params)
    const duration_ms = Date.now() - start_time

    // Log slow queries
    if (duration_ms > 500) {
      log_warning(`Slow Neo4j query: ${duration_ms}ms`)
    }

    return {
      results: result,
      performance: {
        neo4j_query_ms: duration_ms,
        timeout_occurred: false
      }
    }

  } catch (error) {
    const duration_ms = Date.now() - start_time

    return {
      results: [],
      performance: {
        neo4j_query_ms: duration_ms,
        timeout_occurred: error instanceof TimeoutError,
        error: error.message
      }
    }
  }
}
```

## Testing

Validate Neo4j query execution:

```
Test 1: Temporal evolution query (Neo4j available)
Input: concept="Zettelkasten", start_date="2024-01-01", end_date="2024-11-05"
Expected: Timeline with version snapshots, <1 second

Test 2: Causal chain query
Input: source="atomic notes", target="improved recall"
Expected: Causal path with relationships, confidence scores

Test 3: Relationship traversal
Input: concept="Zettelkasten", max_hops=2
Expected: Related notes ranked by distance and strength

Test 4: Neo4j unavailable
Input: concept="X", neo4j_down=true
Expected: Graceful degradation, Obsidian fallback, warning message

Test 5: Query timeout
Input: concept="X", simulated_delay=2000ms
Expected: Timeout error, empty results, warning logged

Test 6: Cypher injection attempt
Input: concept="'})-[r:OWNS]->(attacker) //"
Expected: Sanitized safely, no injection, valid results or empty
```

## Performance Budget

- Neo4j temporal query: <500ms
- Neo4j graph traversal: <500ms
- Availability check: <100ms
- **Total: <1 second**

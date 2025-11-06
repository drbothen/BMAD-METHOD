<!-- Powered by BMAD™ Core -->

# execute-obsidian-query

**Purpose:** Execute queries against Obsidian vault using MCP Tools (text search) and Smart Connections (semantic search)

**Performance Budget:** <1 second per source

## Overview

This task executes queries across two Obsidian-based data sources:

1. **Obsidian MCP Tools** - File system access and text search
2. **Smart Connections MCP** - Semantic similarity search using local embeddings

Both sources are integrated via Model Context Protocol (MCP) servers.

## MCP Integration Architecture

### Obsidian MCP Tools

**Capabilities:**
- Read note contents by file path
- Search vault by text patterns (grep-like functionality)
- List files in directories
- Access note metadata (creation date, modification date)

**Tool Invocations (examples):**
```
mcp__obsidian__read_note(path: "atomic/zettelkasten-definition.md")
mcp__obsidian__search_vault(query: "atomic notes", case_sensitive: false)
mcp__obsidian__list_notes(directory: "atomic/")
```

### Smart Connections MCP

**Capabilities:**
- Semantic similarity search using local BGE-micro-v2 embeddings
- Find notes conceptually related to a query
- No cloud API required (fully offline)
- Returns similarity scores with results

**Tool Invocations (examples):**
```
mcp__smart_connections__find_similar(
  query: "How do atomic notes improve recall?",
  threshold: 0.7,
  limit: 10
)
```

## Query Execution Strategies

### Strategy 1: Factual Queries

**Use:** Questions requesting definitions or descriptions

**Primary Source:** Smart Connections (semantic search)
**Secondary Source:** Obsidian text search (exact term matches)

**Algorithm:**
```
1. Execute semantic search via Smart Connections
   query = sanitized_concept
   threshold = 0.7
   limit = 10

2. Execute text search via Obsidian MCP Tools
   pattern = sanitized_concept
   search_in = ["atomic/", "literature/", "mocs/"]

3. Combine results, prioritize:
   - Semantic matches with score > 0.8
   - Exact title matches from text search
   - MOC (Map of Content) notes
```

**Example:**
```javascript
async function execute_factual_query(concept) {
  const results = []

  try {
    // Semantic search
    const semantic_results = await mcp__smart_connections__find_similar({
      query: concept,
      threshold: 0.7,
      limit: 10
    })

    results.push(...semantic_results.map(r => ({
      source: 'smart_connections',
      note_path: r.path,
      note_title: r.title,
      relevance_score: r.similarity,
      excerpt: r.content_preview,
      match_type: 'semantic'
    })))

  } catch (error) {
    log_warning(`Smart Connections unavailable: ${error.message}`)
  }

  try {
    // Text search for exact matches
    const text_results = await mcp__obsidian__search_vault({
      query: concept,
      case_sensitive: false
    })

    results.push(...text_results.map(r => ({
      source: 'obsidian_text_search',
      note_path: r.path,
      note_title: r.title,
      relevance_score: 0.9, // High score for exact matches
      excerpt: r.matching_line,
      match_type: 'exact_text'
    })))

  } catch (error) {
    log_warning(`Obsidian text search unavailable: ${error.message}`)
  }

  if (results.length === 0) {
    throw QueryExecutionError('No results found from Obsidian sources')
  }

  return results
}
```

### Strategy 2: Exploratory Queries

**Use:** Broad requests to "show everything" about a topic

**Primary Source:** Smart Connections (semantic search with lower threshold)
**Secondary Source:** Obsidian text search (all matches)

**Algorithm:**
```
1. Execute semantic search with LOWER threshold (0.5)
   - Cast wider net to capture related concepts

2. Execute text search across all directories

3. Include graph-connected notes (if Neo4j available)

4. Group results by:
   - Direct matches (high relevance)
   - Related concepts (medium relevance)
   - Peripheral topics (low relevance)
```

**Example:**
```javascript
async function execute_exploratory_query(concept) {
  const results = []

  try {
    // Semantic search with lower threshold
    const semantic_results = await mcp__smart_connections__find_similar({
      query: concept,
      threshold: 0.5,  // Lower for broader results
      limit: 50        // Higher limit
    })

    results.push(...semantic_results.map(r => ({
      source: 'smart_connections',
      note_path: r.path,
      note_title: r.title,
      relevance_score: r.similarity,
      excerpt: r.content_preview,
      match_type: 'semantic',
      category: categorize_by_score(r.similarity)
    })))

  } catch (error) {
    log_warning(`Smart Connections unavailable: ${error.message}`)
  }

  try {
    // Broad text search
    const text_results = await mcp__obsidian__search_vault({
      query: concept,
      case_sensitive: false
    })

    results.push(...text_results.map(r => ({
      source: 'obsidian_text_search',
      note_path: r.path,
      note_title: r.title,
      relevance_score: 0.8,
      excerpt: r.matching_line,
      match_type: 'text',
      category: 'direct_match'
    })))

  } catch (error) {
    log_warning(`Obsidian text search unavailable: ${error.message}`)
  }

  return results
}

function categorize_by_score(similarity) {
  if (similarity > 0.7) return 'direct_match'
  if (similarity > 0.6) return 'related_concept'
  return 'peripheral_topic'
}
```

### Strategy 3: Temporal Queries

**Use:** Queries about how concepts evolved over time

**Primary Source:** Neo4j (see execute-neo4j-query.md)
**Fallback Source:** Obsidian text search sorted by modification date

**Obsidian Fallback Algorithm:**
```
1. Execute text search for concept

2. Retrieve file metadata (creation_date, modification_date)

3. Sort results chronologically

4. Group by time periods (months/years)
```

**Example:**
```javascript
async function execute_temporal_query_obsidian_fallback(concept, start_date, end_date) {
  try {
    const text_results = await mcp__obsidian__search_vault({
      query: concept,
      case_sensitive: false
    })

    // Enrich with metadata
    const enriched_results = []
    for (const result of text_results) {
      const metadata = await mcp__obsidian__read_note(result.path)

      // Parse frontmatter for dates
      const frontmatter = parse_frontmatter(metadata.content)

      enriched_results.push({
        source: 'obsidian_text_search',
        note_path: result.path,
        note_title: result.title,
        excerpt: result.matching_line,
        created_date: frontmatter.created || metadata.created_date,
        modified_date: metadata.modified_date,
        match_type: 'temporal_fallback'
      })
    }

    // Filter by date range
    const filtered = enriched_results.filter(r => {
      const note_date = new Date(r.created_date)
      return note_date >= start_date && note_date <= end_date
    })

    // Sort chronologically
    filtered.sort((a, b) => new Date(a.created_date) - new Date(b.created_date))

    return filtered

  } catch (error) {
    throw QueryExecutionError(`Temporal query failed: ${error.message}`)
  }
}
```

### Strategy 4: Comparative Queries

**Use:** Comparing two or more concepts

**Approach:** Execute parallel queries for each subject

**Algorithm:**
```
1. For each subject:
   - Execute semantic search
   - Execute text search

2. Preserve results separately (don't merge yet)

3. Tag each result with its subject

4. Return structured results for comparison table
```

**Example:**
```javascript
async function execute_comparative_query(subjects) {
  const results_by_subject = {}

  // Execute queries in parallel
  const promises = subjects.map(async (subject) => {
    try {
      const semantic = await mcp__smart_connections__find_similar({
        query: subject,
        threshold: 0.7,
        limit: 10
      })

      const text = await mcp__obsidian__search_vault({
        query: subject,
        case_sensitive: false
      })

      return {
        subject: subject,
        semantic_results: semantic,
        text_results: text
      }

    } catch (error) {
      log_warning(`Query failed for subject "${subject}": ${error.message}`)
      return {
        subject: subject,
        semantic_results: [],
        text_results: [],
        error: error.message
      }
    }
  })

  const all_results = await Promise.all(promises)

  // Structure results by subject
  for (const result of all_results) {
    results_by_subject[result.subject] = {
      notes: [
        ...result.semantic_results.map(r => ({
          source: 'smart_connections',
          note_path: r.path,
          note_title: r.title,
          relevance_score: r.similarity,
          excerpt: r.content_preview
        })),
        ...result.text_results.map(r => ({
          source: 'obsidian_text_search',
          note_path: r.path,
          note_title: r.title,
          relevance_score: 0.8,
          excerpt: r.matching_line
        }))
      ],
      error: result.error
    }
  }

  return results_by_subject
}
```

## Graceful Degradation

**Scenario 1: Smart Connections MCP Unavailable**
```javascript
try {
  results = await mcp__smart_connections__find_similar(...)
} catch (error) {
  log_warning('Smart Connections unavailable, falling back to text search only')
  // Continue with Obsidian text search
}
```

**Scenario 2: Obsidian MCP Tools Unavailable**
```javascript
try {
  results = await mcp__obsidian__search_vault(...)
} catch (error) {
  log_error('Obsidian MCP Tools unavailable')
  // Prompt user to check MCP configuration
  throw QueryExecutionError('Cannot access Obsidian vault. Please check MCP server configuration.')
}
```

**Scenario 3: Both Sources Unavailable**
```javascript
if (smart_connections_failed && obsidian_failed) {
  throw QueryExecutionError(
    'All Obsidian data sources unavailable. Please check:\n' +
    '1. Obsidian MCP Tools configuration\n' +
    '2. Smart Connections plugin installation\n' +
    '3. MCP server status in Claude Desktop config'
  )
}
```

## Timeout Handling

**MCP Query Timeout:** 1 second per source

```javascript
async function execute_with_timeout(promise, timeout_ms, source_name) {
  const timeout_promise = new Promise((_, reject) => {
    setTimeout(() => {
      reject(new TimeoutError(`${source_name} query exceeded ${timeout_ms}ms timeout`))
    }, timeout_ms)
  })

  try {
    return await Promise.race([promise, timeout_promise])
  } catch (error) {
    if (error instanceof TimeoutError) {
      log_warning(error.message)
      return []  // Return empty results on timeout
    }
    throw error
  }
}

// Usage
const semantic_results = await execute_with_timeout(
  mcp__smart_connections__find_similar({...}),
  1000,  // 1 second timeout
  'Smart Connections'
)

const text_results = await execute_with_timeout(
  mcp__obsidian__search_vault({...}),
  1000,  // 1 second timeout
  'Obsidian Text Search'
)
```

## Error Messages

Provide informative error messages when queries fail:

### Error 1: No Results Found
```
"No notes found matching '[concept]'. Try:
- Broadening your search terms
- Checking spelling
- Using *surface-related to explore related topics"
```

### Error 2: MCP Server Unavailable
```
"Smart Connections MCP server is unavailable. Falling back to text search only.
To enable semantic search, install the Smart Connections plugin in Obsidian."
```

### Error 3: Malformed Query
```
"I couldn't process your query. Please try reformulating it as:
- 'What is [concept]?' (factual)
- 'Show me everything about [topic]' (exploratory)
- 'Compare [X] and [Y]' (comparative)"
```

### Error 4: Timeout
```
"Query timed out after 1 second. Try:
- Simplifying your query
- Reducing the scope
- Checking your vault size (very large vaults may be slow)"
```

## Result Structure

Return structured results for merging:

```yaml
results:
  - source: "smart_connections"
    note_path: "atomic/zettelkasten-definition.md"
    note_title: "Zettelkasten Method Definition"
    relevance_score: 0.87
    excerpt: "Zettelkasten is a method of knowledge management using atomic notes..."
    match_type: "semantic"
    metadata:
      created_date: "2024-03-15T10:23:00Z"
      modified_date: "2024-10-12T14:45:00Z"
      building_block: "concept"

  - source: "obsidian_text_search"
    note_path: "mocs/note-taking-methods.md"
    note_title: "Note-Taking Methods MOC"
    relevance_score: 0.90
    excerpt: "...comparing Zettelkasten with PARA and Johnny Decimal systems..."
    match_type: "exact_text"
    metadata:
      created_date: "2024-01-05T09:00:00Z"
      modified_date: "2024-11-01T16:30:00Z"
      building_block: "moc"

query_metadata:
  sources_queried: ["smart_connections", "obsidian_text_search"]
  sources_successful: ["smart_connections", "obsidian_text_search"]
  sources_failed: []
  total_results: 12
  query_duration_ms: 850
  timeout_occurred: false
```

## Performance Monitoring

Track and report query performance:

```javascript
async function execute_obsidian_query_with_monitoring(query_params) {
  const start_time = Date.now()
  const performance_log = {}

  // Smart Connections
  const sc_start = Date.now()
  const semantic_results = await execute_smart_connections_query(query_params)
  performance_log.smart_connections_ms = Date.now() - sc_start

  // Obsidian Text Search
  const obs_start = Date.now()
  const text_results = await execute_obsidian_text_search(query_params)
  performance_log.obsidian_text_search_ms = Date.now() - obs_start

  // Total duration
  performance_log.total_ms = Date.now() - start_time

  // Log slow queries
  if (performance_log.total_ms > 1000) {
    log_warning(`Slow Obsidian query: ${performance_log.total_ms}ms`)
  }

  return {
    results: [...semantic_results, ...text_results],
    performance: performance_log
  }
}
```

## Testing

Validate query execution with test scenarios:

```
Test 1: Factual query with both sources available
Input: concept="Zettelkasten", intent="factual"
Expected: Results from both Smart Connections and text search, <1 second

Test 2: Smart Connections unavailable
Input: concept="Zettelkasten", smart_connections_down=true
Expected: Results from text search only, warning logged

Test 3: No results found
Input: concept="NonexistentConcept123"
Expected: Empty results, helpful error message

Test 4: Query timeout
Input: concept="X", simulated_delay=2000ms
Expected: Timeout error, graceful fallback

Test 5: Comparative query
Input: subjects=["Zettelkasten", "PARA"]
Expected: Results structured by subject, parallel execution <1 second
```

## Performance Budget

- Smart Connections query: <500ms
- Obsidian text search: <500ms
- Metadata enrichment: <100ms
- **Total: <1 second per source**

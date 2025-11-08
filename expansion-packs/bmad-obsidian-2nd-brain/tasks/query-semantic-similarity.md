# <!-- Powered by BMAD™ Core -->

# query-semantic-similarity

Query Smart Connections for semantically similar notes and filter candidates for link suggestions.

## Purpose

Use Smart Connections MCP Server to perform local semantic search using BGE-micro-v2 embeddings. Returns semantically similar notes that meet the 0.6 similarity threshold, excluding already-linked notes and sorting by relevance for link suggestion.

## Prerequisites

- Smart Connections plugin installed in Obsidian
- Smart Connections MCP Server configured in Claude Desktop/Cursor
- BGE-micro-v2 embeddings generated for vault notes
- Access to source note content
- Access to Obsidian MCP for reading note links

## Inputs

- **note_id** (string, required): ID or path of source note in vault
- **note_content** (string, required): Full content of source note for semantic query
- **similarity_threshold** (float, optional): Minimum similarity score (default: 0.6)
- **result_limit** (int, optional): Maximum results to return (default: 20)
- **exclude_already_linked** (bool, optional): Filter out notes already linked (default: true)

## Outputs

```yaml
similarity_query_result:
  source_note: 'path/to/source.md'
  query_timestamp: '2025-11-05T14:30:00Z'
  total_candidates: 15
  filtered_count: 12 # After excluding linked notes
  results:
    - note_id: 'uuid-abc123'
      note_title: 'Related Note Title'
      note_path: 'path/to/target.md'
      similarity_score: 0.82 # 0.0-1.0
      shared_concepts: ['concept1', 'concept2', 'concept3']
      already_linked: false
    - ...
  execution_time_ms: 2847
  mcp_available: true
  error: null
```

## Procedure

### Step 1: Validate Inputs

1. **Check note_id provided:**
   - Verify note_id is non-empty string
   - If empty → return error: "note_id required"

2. **Check note_content provided:**
   - Verify note_content is non-empty string
   - If empty → return error: "note_content required for semantic query"

3. **Validate threshold:**
   - Verify 0.0 <= similarity_threshold <= 1.0
   - If invalid → default to 0.6 with warning

4. **Validate limit:**
   - Verify result_limit > 0 and <= 100
   - If invalid → default to 20 with warning

### Step 2: Check Smart Connections Availability

1. **Query MCP Server:**

   ```javascript
   // Attempt to call Smart Connections MCP
   try {
     mcp_available = check_smart_connections_mcp();
   } catch (error) {
     // Graceful degradation
     return {
       mcp_available: false,
       error:
         'Smart Connections MCP not available. Install Smart Connections plugin and configure MCP server.',
       results: [],
       suggestion: 'Manual linking available via *create-link command',
     };
   }
   ```

2. **If unavailable:**
   - Return empty results with clear error message
   - Suggest manual linking as alternative
   - Don't fail hard - allow graceful degradation

### Step 3: Load Source Note Content

1. **Read source note via Obsidian MCP:**

   ```javascript
   source_note = read_note(note_id)
   if (!source_note) {
     return error: "Source note not found: {note_id}"
   }
   ```

2. **Parse existing wikilinks (if exclude_already_linked=true):**
   ```javascript
   existing_links = extract_wikilinks(source_note.content);
   // Example: ["[[Note 1]]", "[[Note 2]]"]
   // Convert to paths: ["path/to/note-1.md", "path/to/note-2.md"]
   ```

### Step 4: Execute Smart Connections Query

1. **Call Smart Connections MCP:**

   ```javascript
   // MCP Call Example
   results = smart_connections.search_similar({
     content: note_content,
     threshold: similarity_threshold,
     limit: result_limit,
     exclude_current: true, // Don't return the source note itself
   });
   ```

2. **Smart Connections returns:**

   ```json
   [
     {
       "note_id": "uuid-abc123",
       "note_title": "Evergreen Notes",
       "note_path": "concepts/evergreen-notes.md",
       "similarity_score": 0.82
     },
     {
       "note_id": "uuid-def456",
       "note_title": "Bidirectional Links",
       "note_path": "concepts/bidirectional-links.md",
       "similarity_score": 0.74
     },
     ...
   ]
   ```

3. **Error handling:**
   ```javascript
   try {
     results = smart_connections.search_similar(...)
   } catch (TimeoutError) {
     // Retry with exponential backoff
     retry_count = 0
     while (retry_count < 3) {
       wait(2^retry_count * 1000) // 1s, 2s, 4s
       try {
         results = smart_connections.search_similar(...)
         break
       } catch (TimeoutError) {
         retry_count++
       }
     }
     if (retry_count >= 3) {
       return error: "Smart Connections timeout after 3 retries"
     }
   }
   ```

### Step 5: Filter Results

1. **Apply similarity threshold:**

   ```javascript
   filtered = results.filter((r) => r.similarity_score >= similarity_threshold);
   ```

2. **Exclude already-linked notes (if requested):**

   ```javascript
   if (exclude_already_linked) {
     filtered = filtered.filter((r) => !existing_links.includes(r.note_path));
   }
   ```

3. **Exclude source note itself:**

   ```javascript
   filtered = filtered.filter((r) => r.note_id !== source_note.id);
   ```

4. **Sort by similarity descending:**
   ```javascript
   filtered.sort((a, b) => b.similarity_score - a.similarity_score);
   ```

### Step 6: Extract Shared Concepts

For each result, analyze shared concepts:

1. **Extract concepts from both notes:**

   ```javascript
   source_concepts = extract_concepts(source_note.content);
   // Extract: tags, heading keywords, linked concepts

   target_concepts = extract_concepts(result.note_content);
   ```

2. **Calculate overlap:**

   ```javascript
   shared_concepts = intersection(source_concepts, target_concepts);
   result.shared_concepts = shared_concepts;
   ```

3. **Example:**
   ```
   Source concepts: ["zettelkasten", "note-taking", "atomicity", "linking"]
   Target concepts: ["evergreen-notes", "zettelkasten", "linking", "knowledge-management"]
   Shared: ["zettelkasten", "linking"]
   ```

### Step 7: Format and Return Results

1. **Build output structure:**

   ```yaml
   {
     source_note: note_id,
     query_timestamp: current_iso_timestamp(),
     total_candidates: results.length,
     filtered_count: filtered.length,
     results: filtered.map(r => ({
       note_id: r.note_id,
       note_title: r.note_title,
       note_path: r.note_path,
       similarity_score: round(r.similarity_score, 2),
       shared_concepts: r.shared_concepts,
       already_linked: existing_links.includes(r.note_path)
     })),
     execution_time_ms: elapsed_time,
     mcp_available: true,
     error: null
   }
   ```

2. **Performance validation:**
   - If execution_time_ms > 3000 (3 seconds) → log warning
   - Target: < 3 seconds per query

## Examples

### Example 1: Successful Query

**Input:**

```yaml
note_id: 'concepts/zettelkasten-atomicity.md'
note_content: 'The atomicity principle states that each note should contain exactly one complete idea...'
similarity_threshold: 0.6
result_limit: 20
exclude_already_linked: true
```

**Output:**

```yaml
similarity_query_result:
  source_note: 'concepts/zettelkasten-atomicity.md'
  query_timestamp: '2025-11-05T14:30:00Z'
  total_candidates: 18
  filtered_count: 15
  results:
    - note_id: 'uuid-abc123'
      note_title: 'Evergreen Notes'
      note_path: 'concepts/evergreen-notes.md'
      similarity_score: 0.82
      shared_concepts: ['zettelkasten', 'note-taking', 'atomicity']
      already_linked: false
    - note_id: 'uuid-def456'
      note_title: 'Bidirectional Links'
      note_path: 'concepts/bidirectional-links.md'
      similarity_score: 0.74
      shared_concepts: ['linking', 'zettelkasten']
      already_linked: false
    - note_id: 'uuid-ghi789'
      note_title: 'Building Block Types'
      note_path: 'concepts/building-block-types.md'
      similarity_score: 0.68
      shared_concepts: ['atomicity', 'concept', 'note-structure']
      already_linked: false
  execution_time_ms: 2145
  mcp_available: true
  error: null
```

### Example 2: Smart Connections Unavailable

**Input:**

```yaml
note_id: 'concepts/zettelkasten-atomicity.md'
note_content: '...'
```

**Output:**

```yaml
similarity_query_result:
  source_note: 'concepts/zettelkasten-atomicity.md'
  query_timestamp: '2025-11-05T14:30:00Z'
  total_candidates: 0
  filtered_count: 0
  results: []
  execution_time_ms: 45
  mcp_available: false
  error: 'Smart Connections MCP not available. Install Smart Connections plugin and configure MCP server.'
  suggestion: 'Manual linking available via *create-link command'
```

### Example 3: No Results Above Threshold

**Input:**

```yaml
note_id: 'unique-topic.md'
similarity_threshold: 0.6
```

**Output:**

```yaml
similarity_query_result:
  source_note: 'unique-topic.md'
  query_timestamp: '2025-11-05T14:35:00Z'
  total_candidates: 8
  filtered_count: 0 # All below 0.6 threshold
  results: []
  execution_time_ms: 1834
  mcp_available: true
  error: null
  message: 'No notes found with similarity >= 0.6. Source note may be on unique topic or vault is too small.'
```

## Error Handling

### Error: Source Note Not Found

```yaml
error: 'Source note not found: {note_id}'
action: 'Verify note exists in vault'
```

### Error: Smart Connections Timeout

```yaml
error: 'Smart Connections timeout after 3 retries'
action: 'Check Smart Connections plugin status, reduce vault size, or increase timeout'
```

### Error: Invalid Threshold

```yaml
error: 'Invalid similarity_threshold: {value}. Must be 0.0-1.0'
action: 'Using default 0.6'
```

### Error: Empty Note Content

```yaml
error: 'Note content empty, cannot perform semantic search'
action: 'Ensure note has content before querying'
```

## Performance Targets

- **Query execution:** < 3 seconds per query
- **Memory usage:** < 100MB during query
- **Retry limit:** Max 3 retries with exponential backoff

## Integration Points

**Called by:**

- \*suggest-links command
- \*create-links command (to find candidates)
- \*batch-approve workflow

**Calls:**

- Smart Connections MCP: `search_similar()`
- Obsidian MCP: `read_note()`

**References:**

- connection-patterns.md (for relationship context)
- linking-quality-checklist.md (for threshold validation)

## Notes

- Smart Connections uses BGE-micro-v2 embeddings (local, privacy-preserving)
- Embeddings must be generated before semantic search works
- Similarity threshold 0.6 is empirically validated (from requirements)
- Higher thresholds (>= 0.8) produce fewer but stronger suggestions

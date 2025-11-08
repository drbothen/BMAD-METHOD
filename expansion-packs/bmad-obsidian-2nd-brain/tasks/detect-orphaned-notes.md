<!-- Powered by BMAD™ Core -->

# detect-orphaned-notes

Detect orphaned notes (notes with no incoming or outgoing links) and suggest linking opportunities using semantic similarity.

## Purpose

Identify isolated notes disconnected from the knowledge graph and suggest meaningful connections to integrate them into the vault's link network.

## Prerequisites

- Obsidian MCP server configured
- Smart Connections MCP (optional, for link suggestions - graceful degradation if unavailable)
- Neo4j Graphiti MCP (optional, for advanced graph metrics - graceful degradation if unavailable)

## Inputs

- **vault_path** (string, required): Path to Obsidian vault
- **similarity_threshold** (float, optional): Threshold for link suggestions (default: 0.6)
- **max_suggestions_per_orphan** (integer, optional): Max linking suggestions per orphan (default: 3)

## Outputs

```yaml
orphan_detection_audit:
  total_notes: integer
  orphaned_notes_count: integer
  orphan_percentage: float
  audit_timestamp: string
  orphan_categories:
    no_incoming: integer # Notes never referenced
    no_outgoing: integer # Notes that don't link to others
    complete_orphans: integer # Neither incoming nor outgoing
  orphaned_notes:
    - note_path: string
      note_title: string
      has_incoming: boolean
      has_outgoing: boolean
      incoming_link_count: integer
      outgoing_link_count: integer
      orphan_type: string # 'COMPLETE|NO_INCOMING|NO_OUTGOING'
      priority: string # 'CRITICAL|HIGH|MEDIUM'
      suggested_links: # If Smart Connections available
        - target_note: string
          similarity_score: float
          link_type: string # 'semantic|conceptual|related'
          confidence: string # 'HIGH|MEDIUM|LOW'
```

## Algorithm

### Step 1: Build Link Graph

```
1. Query all notes via Obsidian MCP: list_notes()
2. For each note:
   - Parse content for wikilinks: [[...]]
   - Handle aliases: [[Note Title|Alias]]
   - Extract outgoing_links array
3. Build adjacency matrix:
   - For each note: incoming_links = []
   - For each note with outgoing links:
       For each target in outgoing_links:
           incoming_links[target].append(current_note)
4. For each note, store:
   - outgoing_link_count = len(outgoing_links)
   - incoming_link_count = len(incoming_links)
```

### Step 2: Identify Orphans

**Orphan Categories:**

| Category            | Condition                   | Priority |
| ------------------- | --------------------------- | -------- |
| **Complete Orphan** | No incoming AND no outgoing | CRITICAL |
| **No Incoming**     | incoming_link_count == 0    | HIGH     |
| **No Outgoing**     | outgoing_link_count == 0    | MEDIUM   |

```
For each note:
  if incoming_link_count == 0 AND outgoing_link_count == 0:
    orphan_type = 'COMPLETE'
    priority = 'CRITICAL'
  elif incoming_link_count == 0:
    orphan_type = 'NO_INCOMING'
    priority = 'HIGH'
  elif outgoing_link_count == 0:
    orphan_type = 'NO_OUTGOING'
    priority = 'MEDIUM'
  else:
    is_orphan = false
```

### Step 3: Suggest Linking Opportunities (if Smart Connections available)

For each orphaned note:

```
1. Use Smart Connections semantic search:
   - search_similar(note_content, threshold=0.6, limit=10)
2. Filter results:
   - Exclude notes already linked (avoid duplicates)
   - Exclude self-references
   - Sort by similarity_score (descending)
   - Take top 3 suggestions
3. For each suggestion:
   - Calculate link_strength using STORY-004 algorithm
   - Classify confidence:
     - HIGH: similarity >= 0.8
     - MEDIUM: similarity 0.6-0.8
     - LOW: similarity < 0.6
   - Determine link_type:
     - 'semantic': Similar concepts/topics
     - 'conceptual': Related ideas
     - 'related': Broader connection
```

**Graceful Degradation:** If Smart Connections unavailable, skip suggestions but still report orphans.

### Step 4: Calculate Metrics

```
orphaned_notes_count = len(orphaned_notes)
orphan_percentage = (orphaned_notes_count / total_notes) * 100

orphan_categories:
  complete_orphans = count(orphan_type == 'COMPLETE')
  no_incoming = count(orphan_type == 'NO_INCOMING')
  no_outgoing = count(orphan_type == 'NO_OUTGOING')
```

### Step 5: Sort and Return

Sort orphaned_notes by:

1. priority (CRITICAL → HIGH → MEDIUM)
2. note_title (alphabetically)

## Performance Target

<5 seconds for 1000-note vault

## Use Cases

**1. Knowledge Graph Integration**

- Connect isolated notes to vault
- Build bidirectional link network

**2. Note Discovery**

- Find forgotten or underutilized notes
- Surface hidden knowledge

**3. Structural Health**

- Maintain connected knowledge graph
- Prevent knowledge silos

## Optional: Neo4j Graph Metrics

If Neo4j Graphiti MCP available:

```cypher
// Find complete orphans
MATCH (n:Note)
WHERE NOT (n)<-[:LINKS_TO]-() AND NOT (n)-[:LINKS_TO]->()
RETURN n

// Calculate graph centrality
MATCH (n:Note)
RETURN n.title, size((n)<-[:LINKS_TO]-()) as incoming_count
ORDER BY incoming_count DESC
```

## Testing

**Test Case:** 100-note vault

- 70 well-connected (>2 links)
- 15 no incoming links
- 10 no outgoing links
- 5 complete orphans

Expected: 30 orphans detected, 30% orphan rate

## Integration

Executed by:

- `*audit-orphans` command
- `*audit-full` command
- Progressive audit batch processing

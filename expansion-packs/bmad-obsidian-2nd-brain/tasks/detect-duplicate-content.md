<!-- Powered by BMAD™ Core -->

# detect-duplicate-content

Detect duplicate or semantically similar notes using content hashing and semantic similarity analysis.

## Purpose

Identify exact duplicates, near-duplicates, and semantically similar notes to reduce redundancy and consolidate knowledge.

## Prerequisites

- Obsidian MCP server configured
- Smart Connections MCP (optional, for semantic similarity - graceful degradation to exact duplicates only)
- SHA-256 hashing capability

## Inputs

- **vault_path** (string, required): Path to Obsidian vault
- **similarity_threshold** (float, optional): Threshold for semantic duplicates (default: 0.85)
- **batch_size** (integer, optional): Notes to process per batch for memory management (default: 100)

## Outputs

```yaml
duplicate_detection_audit:
  total_notes: integer
  duplicate_groups_count: integer
  audit_timestamp: string
  duplicate_groups:
    - notes: array # [note_path1, note_path2, ...]
      similarity_score: float # 0.0-1.0 (1.0 for exact matches)
      is_exact_match: boolean # True if SHA-256 hash collision
      duplicate_type: string # 'EXACT|NEAR|SEMANTIC'
      suggested_action: string # 'MERGE|ARCHIVE|REVIEW'
      priority: string # 'CRITICAL|HIGH|MEDIUM'
```

## Algorithm

### Step 1: Exact Duplicate Detection (SHA-256)

```
1. Query all notes via Obsidian MCP
2. For each note:
   - Read content (strip frontmatter for comparison)
   - Calculate SHA-256 hash
   - Store: hash_map[hash] = [note_path1, note_path2, ...]
3. Identify exact duplicates:
   - For each hash with len(notes) > 1:
       Create duplicate_group:
         notes = hash_map[hash]
         similarity_score = 1.0
         is_exact_match = true
         duplicate_type = 'EXACT'
```

**Security:** Use SHA-256 (secure, collision-resistant). NOT MD5 or SHA-1.

### Step 2: Semantic Duplicate Detection (Smart Connections)

If Smart Connections available:

```
1. For each note (not already in exact duplicate group):
   - search_similar(note_content, threshold=0.85, limit=10)
   - Filter results:
     - similarity >= threshold
     - Exclude self
     - Exclude already clustered notes
2. Build similarity matrix
3. Cluster notes with similarity >= 0.85:
   - Group A-B-C if A~B >= 0.85 AND B~C >= 0.85
4. For each cluster:
   - Calculate avg_similarity across all pairs
   - Classify:
     - NEAR: avg_similarity >= 0.95
     - SEMANTIC: avg_similarity 0.85-0.95
```

**Graceful Degradation:** If Smart Connections unavailable, return exact duplicates only.

### Step 3: Classify and Prioritize

**Duplicate Types:**

| Type         | Similarity | Priority | Suggested Action               |
| ------------ | ---------- | -------- | ------------------------------ |
| **EXACT**    | 1.0 (100%) | CRITICAL | MERGE immediately              |
| **NEAR**     | >= 0.95    | HIGH     | MERGE or consolidate           |
| **SEMANTIC** | 0.85-0.95  | MEDIUM   | REVIEW for merge opportunities |

### Step 4: Aggregate Results

```
duplicate_groups_count = len(duplicate_groups)

For each group:
  - notes: list of duplicate note paths
  - similarity_score: average similarity
  - is_exact_match: boolean
  - duplicate_type: classification
  - suggested_action: recommended remediation
  - priority: impact level
```

## Performance Target

<10 seconds for 1000-note vault

## Memory Management

**Batch Processing:** For large vaults (>10,000 notes):

- Process notes in batches of 100
- Clear batch data from memory after hashing
- Peak memory: O(batch_size), not O(total_notes)

## Use Cases

**1. Reduce Redundancy**

- Merge exact duplicates
- Consolidate near-duplicates

**2. Content Cleanup**

- Identify copy-paste scenarios
- Detect versioning without archiving

**3. Knowledge Consolidation**

- Find semantically similar notes
- Merge related content

## False Positive Handling

Allow user to mark pairs as "intentionally similar":

- Store exclusions: `.audit-exclusions.json`
- Ignore in future audits

## Testing

**Test Case:** 100-note vault

- 5 exact duplicate pairs
- 5 near-duplicate pairs (>= 95%)
- 5 semantic duplicate pairs (85-95%)
- 85 unique notes

Expected: 15 duplicate groups detected

## Integration

Executed by:

- `*audit-duplicates [threshold]` command
- `*audit-full` command
- Progressive audit batch processing

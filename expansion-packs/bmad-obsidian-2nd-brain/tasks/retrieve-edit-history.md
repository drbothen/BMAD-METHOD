<!-- Powered by BMAD™ Core -->

# Retrieve Edit History

## Purpose

Fetch detailed edit history for a note from Neo4j, including diffs between versions, edit velocity calculation, and identification of major revisions.

## Inputs

- **note_path** (String, required): Path to note in vault
- **include_diffs** (Boolean, optional): Include content diffs between versions (default: true)
- **min_edit_size** (Number, optional): Minimum lines changed to include edit (default: 1)

## Outputs

- **edit_history** (Array): Chronological list of edits with timestamps, diffs, and metadata
- **edit_analysis** (Object): Velocity metrics, major revision identification, editing patterns

## Procedure

### Step 1: Check Neo4j Availability

```
try:
  graphiti.health_check()
  neo4j_available = true
catch:
  error("Neo4j required for edit history retrieval.")
  return null
```

### Step 2: Query Edit Events from Neo4j

**Cypher query:**

```cypher
MATCH (n:Note {path: $note_path})-[:EDITED_AT]->(ee:EditEvent)
RETURN
  ee.timestamp as timestamp,
  ee.lines_changed as lines_changed,
  ee.additions as additions,
  ee.deletions as deletions,
  ee.diff_summary as diff_summary,
  ee.content_before as content_before,
  ee.content_after as content_after,
  ee.edit_type as edit_type  // "minor", "moderate", "major"
ORDER BY ee.timestamp ASC
```

Execute via Graphiti MCP:
```javascript
const edits = await graphiti.search({
  query: `Find all edit events for ${note_path}`,
  entity_types: ["EditEvent"],
  filters: { note_path: note_path }
});
```

### Step 3: Calculate Edit Diffs

For each edit (if `include_diffs = true`):

```javascript
for (const edit of edit_history) {
  if (edit.content_before && edit.content_after) {
    // Generate unified diff
    edit.diff = generateUnifiedDiff(edit.content_before, edit.content_after);

    // Classify edit type by size
    if (edit.lines_changed >= 20) {
      edit.edit_type = "major";
    } else if (edit.lines_changed >= 5) {
      edit.edit_type = "moderate";
    } else {
      edit.edit_type = "minor";
    }
  }
}
```

Filter edits by `min_edit_size` threshold.

### Step 4: Calculate Edit Velocity

**Edit velocity**: Edits per week during active periods

```javascript
// Identify active editing periods (weeks with at least 1 edit)
const weeks_active = countActiveWeeks(edit_history);
const total_edits = edit_history.length;
const edit_velocity = total_edits / weeks_active;

// Calculate velocity by phase (if phases identified)
const development_edits = edit_history.filter(e =>
  e.timestamp >= development_phase_start &&
  e.timestamp <= development_phase_end
);
const development_velocity = development_edits.length /
  weeksBetween(development_phase_start, development_phase_end);
```

### Step 5: Identify Major Revisions

**Major revision criteria:**
- Lines changed >= 20 (major restructuring)
- Heading structure changed (indicates reorganization)
- >50% of content rewritten (measured by Levenshtein distance)

```javascript
major_revisions = edit_history.filter(edit => {
  return edit.lines_changed >= 20 ||
         edit.heading_structure_changed ||
         edit.content_similarity < 0.5;
});
```

### Step 6: Detect Edit Bursts

**Edit burst**: 3+ edits within 24 hours (indicates intensive work session)

```javascript
edit_bursts = [];
for (let i = 0; i < edit_history.length - 2; i++) {
  const window_edits = [edit_history[i]];
  let j = i + 1;

  while (j < edit_history.length &&
         hoursBetween(edit_history[i].timestamp, edit_history[j].timestamp) <= 24) {
    window_edits.push(edit_history[j]);
    j++;
  }

  if (window_edits.length >= 3) {
    edit_bursts.push({
      start: window_edits[0].timestamp,
      end: window_edits[window_edits.length - 1].timestamp,
      edit_count: window_edits.length,
      total_lines_changed: window_edits.reduce((sum, e) => sum + e.lines_changed, 0)
    });
  }
}
```

### Step 7: Generate Edit Analysis Report

```markdown
## Edit History Analysis: [[Spaced Repetition]]

**Total Edits**: 28 edits
**Time Span**: 2024-01-15 to 2024-10-03 (262 days)
**Edit Velocity**: 2.1 edits/week (active weeks only)

### Edit Patterns

**Development Phase Velocity**: 3.4 edits/week (Jan 18 - Mar 10)
**Maturation Phase Velocity**: 0.8 edits/week (Mar 11 - Sep 15)
**Current Phase**: Maintenance (< 1 edit/month)

### Major Revisions

1. **2024-02-15** | 34 lines changed
   - Added detailed section on adaptive algorithms (SM-2, FSRS)
   - Restructured from 3 to 5 main headings
   - **Trigger**: Read Wozniak paper on SuperMemo

2. **2024-05-20** | 28 lines changed
   - Shifted perspective from theory to practice
   - Added "Common Pitfalls" section based on Anki experimentation
   - **Trigger**: 3 months of practical usage

### Edit Bursts (Intensive Work Sessions)

1. **2024-02-12 to 2024-02-13** | 5 edits in 18 hours
   - Total: 42 lines changed
   - Context: Initial deep research phase

2. **2024-03-05 to 2024-03-05** | 4 edits in 6 hours
   - Total: 31 lines changed
   - Context: Synthesis with related learning strategies

### Edit Size Distribution

- **Minor edits (1-4 lines)**: 12 edits (43%)
- **Moderate edits (5-19 lines)**: 14 edits (50%)
- **Major edits (20+ lines)**: 2 edits (7%)

[Detailed chronological edit log follows...]
```

### Step 8: Return Results

```json
{
  "note_path": "notes/Spaced Repetition.md",
  "edit_history": [
    {
      "timestamp": "2024-01-15T10:45:00Z",
      "lines_changed": 12,
      "additions": 12,
      "deletions": 0,
      "edit_type": "moderate",
      "diff_summary": "Added definition and basic explanation",
      "diff": "... unified diff ..."
    }
    // ... more edits
  ],
  "edit_analysis": {
    "total_edits": 28,
    "time_span_days": 262,
    "edit_velocity": 2.1,
    "major_revisions": [...],
    "edit_bursts": [...],
    "size_distribution": {...}
  }
}
```

## Integration Notes

**Graphiti MCP Integration:**
- EditEvent nodes created by note modification tracking system
- Store content snapshots (before/after) for diff generation
- Link EditEvent-[:FOR_NOTE]->Note

**Diff Generation:**
- Use library like `diff` or `unified-diff` for generating diffs
- Consider storing diffs in Neo4j to avoid recalculation
- For large notes, consider storing only changed sections

## Error Handling

**Neo4j unavailable**: Return error, cannot fallback
**Note has no edit history**: Return empty array with info message
**Diff generation fails**: Return edit without diff, log warning

## Testing

**Test Case 1**: Note with 20+ edits, verify velocity calculation
**Test Case 2**: Major revision detection (>20 lines changed)
**Test Case 3**: Edit burst identification (5 edits in 24h)

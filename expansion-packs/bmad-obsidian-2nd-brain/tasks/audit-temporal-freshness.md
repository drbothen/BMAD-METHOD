<!-- Powered by BMAD™ Core -->

# audit-temporal-freshness

Audit vault notes for temporal freshness - identify stale notes that haven't been updated within a configured threshold period.

## Purpose

Detect notes that have become stale (not updated recently) to help maintain a fresh, relevant knowledge base. Prioritizes stale notes by importance (measured by incoming link count) to focus attention on domain-critical knowledge hubs that need updating.

## Prerequisites

- Obsidian MCP server configured and accessible
- Access to vault note metadata (last_modified dates, link graph)
- Threshold days configured (default: 180 days)
- Current date/time for comparison

## Inputs

- **threshold_days** (integer, optional): Number of days to consider a note stale (default: 180)
- **vault_path** (string, required): Path to Obsidian vault
- **include_pattern** (string, optional): Glob pattern to filter notes (default: "**/*.md")
- **exclude_patterns** (array, optional): Patterns to exclude (e.g., templates, archives)

## Outputs

```yaml
temporal_freshness_audit:
  stale_notes_count: integer # Number of stale notes detected
  fresh_notes_count: integer # Number of fresh notes
  total_notes: integer # Total notes analyzed
  stale_percentage: float # Percentage of notes stale (2 decimal places)
  threshold_days: integer # Threshold used for this audit
  audit_timestamp: string # ISO 8601 timestamp of audit execution
  stale_notes:
    - note_path: string # Path to stale note
      note_title: string # Note title
      last_updated: string # ISO 8601 timestamp of last update
      days_since_update: integer # Days since last update
      priority: string # 'CRITICAL|HIGH|MEDIUM|LOW'
      incoming_link_count: integer # Number of incoming links
      priority_reason: string # Explanation of priority
  performance:
    notes_analyzed: integer
    execution_time_seconds: float
```

## Algorithm

### Step 1: Query All Notes with Metadata

**Objective:** Retrieve all notes in vault with last_modified metadata

**Implementation:**

```
1. Connect to Obsidian MCP server
2. Call list_notes() with metadata=true
3. For each note:
   - Extract note_path
   - Extract note_title (from frontmatter or filename)
   - Extract last_modified timestamp (ISO 8601 format)
   - Extract tags, frontmatter if available
4. Apply filters:
   - Include only notes matching include_pattern (default: "**/*.md")
   - Exclude notes matching exclude_patterns (e.g., "templates/**", "archives/**")
5. Store notes in array for analysis
```

**Error Handling:**
- If Obsidian MCP unavailable: Return error "Obsidian MCP server not accessible"
- If note lacks last_modified: Use file system modified date as fallback
- If timestamp invalid: Skip note, log warning

**Performance Target:** <3 seconds for 1000 notes

---

### Step 2: Calculate Staleness for Each Note

**Objective:** Determine which notes exceed the staleness threshold

**Implementation:**

```
For each note:
  1. Parse last_updated timestamp to datetime object
  2. Get current_date (now)
  3. Calculate: days_since_update = (current_date - last_updated).days
  4. Classify:
     - If days_since_update > threshold_days:
         is_stale = true
         Add to stale_notes array
     - Else:
         is_stale = false
         Increment fresh_notes_count
```

**Example Calculation:**

```
Current date: 2025-11-06
Note last_updated: 2024-12-15
Days since update: (2025-11-06) - (2024-12-15) = 326 days
Threshold: 180 days
Is stale: 326 > 180 → YES (stale)
```

**Edge Cases:**
- Note updated in the future (last_modified > current_date): Flag as error, use current_date
- Note with no last_modified metadata: Use file system timestamp as fallback
- Note updated today (days_since_update = 0): Fresh

---

### Step 3: Build Link Graph for Prioritization

**Objective:** Count incoming links to each stale note for importance ranking

**Implementation:**

```
1. For each note in vault:
   - Parse note content for wikilinks: [[...]]
   - Extract all outgoing links (linked note titles)

2. Build incoming link map:
   - For each note:
       incoming_link_count[note] = 0
   - For each note with outgoing links:
       For each outgoing_link:
           incoming_link_count[outgoing_link] += 1

3. For each stale note:
   - Lookup incoming_link_count from map
   - Store incoming_link_count for prioritization
```

**Fallback:** If link graph analysis unavailable (e.g., MCP limitation), set all incoming_link_count = 0 and prioritize by days_since_update only.

**Performance Optimization:**
- Cache link graph if multiple audits run in session
- Use MCP bulk operations if available

---

### Step 4: Prioritize Stale Notes by Importance

**Objective:** Rank stale notes so domain-critical knowledge hubs get attention first

**Priority Classification:**

| Priority | Criteria | Incoming Link Count | Description |
|----------|----------|---------------------|-------------|
| **CRITICAL** | Domain-critical knowledge hubs | >10 incoming links | Core concepts heavily referenced across vault |
| **HIGH** | Frequently referenced | >5 incoming links | Important notes with significant connections |
| **MEDIUM** | Some connections | 2-5 incoming links | Moderate integration into knowledge graph |
| **LOW** | Minimal connections | <2 incoming links | Isolated or rarely referenced notes |

**Implementation:**

```
For each stale note:
  incoming_links = incoming_link_count[note]

  if incoming_links > 10:
    priority = 'CRITICAL'
    reason = f'Domain-critical knowledge hub ({incoming_links} incoming links)'
  elif incoming_links > 5:
    priority = 'HIGH'
    reason = f'Frequently referenced ({incoming_links} incoming links)'
  elif incoming_links >= 2:
    priority = 'MEDIUM'
    reason = f'Some connections ({incoming_links} incoming links)'
  else:
    priority = 'LOW'
    reason = f'Minimal connections ({incoming_links} incoming links)'

  stale_note.priority = priority
  stale_note.priority_reason = reason
```

---

### Step 5: Sort and Format Results

**Objective:** Present stale notes in order of priority for actionable review

**Sorting Algorithm:**

```
Sort stale_notes by:
  1. priority (CRITICAL → HIGH → MEDIUM → LOW)
  2. Within same priority, sort by days_since_update (descending - oldest first)
```

**Output Formatting:**

```
For each stale note:
  - note_path: 'path/to/note.md'
    note_title: 'Note Title'
    last_updated: '2024-05-10T10:30:00Z'
    days_since_update: 210
    priority: 'CRITICAL'
    incoming_link_count: 15
    priority_reason: 'Domain-critical knowledge hub (15 incoming links)'
```

**Calculate Summary Statistics:**

```
stale_notes_count = len(stale_notes)
fresh_notes_count = total_notes - stale_notes_count
stale_percentage = (stale_notes_count / total_notes) * 100
```

**Performance Target:** <1 second for sorting and formatting (even for 10,000 notes)

---

### Step 6: Return Audit Results

**Objective:** Deliver structured audit results for report generation

**Return Value:**

```yaml
temporal_freshness_audit:
  stale_notes_count: 150
  fresh_notes_count: 850
  total_notes: 1000
  stale_percentage: 15.0
  threshold_days: 180
  audit_timestamp: '2025-11-06T14:30:00Z'
  stale_notes:
    - note_path: 'concepts/core-methodology.md'
      note_title: 'Core Methodology Framework'
      last_updated: '2024-03-15T10:00:00Z'
      days_since_update: 236
      priority: 'CRITICAL'
      incoming_link_count: 15
      priority_reason: 'Domain-critical knowledge hub (15 incoming links)'
    - note_path: 'references/study-notes.md'
      note_title: 'Study Notes from 2024'
      last_updated: '2024-01-20T12:00:00Z'
      days_since_update: 291
      priority: 'LOW'
      incoming_link_count: 0
      priority_reason: 'Minimal connections (0 incoming links)'
  performance:
    notes_analyzed: 1000
    execution_time_seconds: 4.2
```

---

## Configuration Options

### Threshold Days

**Default:** 180 days (6 months)

**Recommended Values:**
- **30 days:** Aggressive freshness (for rapidly evolving domains)
- **90 days:** Standard freshness (for active knowledge workers)
- **180 days:** Relaxed freshness (for stable knowledge bases)
- **365 days:** Minimal freshness (archive-oriented vaults)

**Configuration Example:**

```yaml
temporal_freshness_config:
  threshold_days: 180 # Adjust based on vault usage patterns
  exclude_patterns:
    - 'templates/**'
    - 'archives/**'
    - '.obsidian/**'
  prioritize_by_links: true # If false, prioritize by days_since_update only
```

---

## Use Cases

### 1. Proactive Maintenance

**Scenario:** Regular vault health check to identify outdated knowledge

**Workflow:**
1. Run `*audit-freshness` with default threshold (180 days)
2. Review CRITICAL and HIGH priority stale notes first
3. Update domain-critical notes to maintain knowledge hub accuracy
4. Archive or delete LOW priority stale notes if no longer relevant

---

### 2. Domain-Specific Thresholds

**Scenario:** Different domains have different freshness requirements

**Example Configuration:**

- **Technology notes:** 30-day threshold (rapid change)
- **Literature notes:** 365-day threshold (stable content)
- **Meeting notes:** 90-day threshold (time-sensitive)

**Workflow:**
1. Run `*audit-freshness 30` for tech notes folder
2. Run `*audit-freshness 365` for literature notes folder
3. Aggregate results for comprehensive audit

---

### 3. Knowledge Hub Maintenance

**Scenario:** Focus on maintaining most-referenced notes (critical to vault integrity)

**Workflow:**
1. Run `*audit-freshness` with default threshold
2. Filter results to CRITICAL priority only (>10 incoming links)
3. Review and update each critical note systematically
4. Re-run audit to verify freshness improvements

---

## Performance Benchmarks

**Target Performance:**

| Vault Size | Notes Analyzed | Expected Time | Max Time |
|------------|----------------|---------------|----------|
| 100 notes  | 100            | <1 second     | 2 seconds |
| 1,000 notes | 1,000         | <3 seconds    | 5 seconds |
| 10,000 notes | 10,000       | <30 seconds   | 60 seconds |
| 100,000 notes | 100,000     | <5 minutes    | 10 minutes |

**Optimization Strategies:**

1. **Batch Processing:** For large vaults (>10,000 notes), process in batches of 1,000
2. **Caching:** Cache link graph if multiple audits run in session
3. **Parallel Processing:** Analyze notes concurrently if MCP supports async operations
4. **Incremental Updates:** Track audit history, only re-analyze changed notes

**Progressive Audit Mode:** For vaults >10,000 notes, use `*progressive` mode to process in batches with checkpointing.

---

## Error Scenarios

### 1. Obsidian MCP Unavailable

**Error:** "Obsidian MCP server not accessible"

**Remediation:**
- Verify MCP server is running
- Check MCP configuration in Claude Desktop/Cursor
- Test connection: `mcp__obsidian__list_notes`

---

### 2. Invalid Threshold

**Error:** "Invalid threshold_days: must be positive integer"

**Remediation:**
- Ensure threshold_days > 0
- Use default (180) if invalid value provided

---

### 3. No Notes Found

**Error:** "No notes found in vault (check include_pattern and exclude_patterns)"

**Remediation:**
- Verify vault path is correct
- Check include/exclude patterns aren't too restrictive
- Confirm vault contains markdown files

---

### 4. Missing Metadata

**Warning:** "Note lacks last_modified metadata, using file system timestamp as fallback"

**Remediation:**
- This is non-blocking, audit continues with fallback
- Consider standardizing note metadata (add frontmatter created/modified fields)

---

## Testing

### Test Case 1: Stale Note Detection

**Setup:**
- 100 notes in test vault
- 20 notes updated within 30 days (fresh)
- 30 notes updated 31-180 days ago (aging)
- 50 notes updated >180 days ago (stale)

**Expected Results:**
- stale_notes_count = 50
- stale_percentage = 50.0%
- All 50 stale notes in results array

**Pass Criteria:** Accuracy >= 95% (correctly identifies stale notes)

---

### Test Case 2: Priority Classification

**Setup:**
- 10 stale notes with varying incoming link counts:
  - 2 notes with 15 incoming links (CRITICAL)
  - 3 notes with 7 incoming links (HIGH)
  - 3 notes with 3 incoming links (MEDIUM)
  - 2 notes with 0 incoming links (LOW)

**Expected Results:**
- 2 notes classified as CRITICAL
- 3 notes classified as HIGH
- 3 notes classified as MEDIUM
- 2 notes classified as LOW

**Pass Criteria:** 100% accuracy in priority classification

---

### Test Case 3: Custom Threshold

**Setup:**
- Run audit with threshold_days = 90 (stricter than default 180)

**Expected Results:**
- More notes classified as stale (lower threshold = more stale)
- Correctly uses 90-day threshold in results

**Pass Criteria:** Threshold correctly applied

---

### Test Case 4: Performance Benchmark

**Setup:**
- 1000-note test vault

**Expected Results:**
- Execution time < 5 seconds
- All 1000 notes analyzed

**Pass Criteria:** Performance target met

---

### Test Case 5: Error Handling

**Setup:**
- Disconnect Obsidian MCP server
- Run audit

**Expected Results:**
- Error: "Obsidian MCP server not accessible"
- Graceful error message (no crash)

**Pass Criteria:** Error handled gracefully with clear message

---

## Integration with Quality Auditor Agent

This task is executed when:

1. `*audit-freshness [threshold_days]` command issued
2. `*audit-full` command runs (uses default threshold 180)
3. Progressive audit mode processes temporal freshness batch

**Caching:** Results cached for report generation. Cache invalidated when vault notes modified or threshold changes.

**Progressive Mode:** For large vaults, this task splits notes into batches and processes incrementally with checkpointing.

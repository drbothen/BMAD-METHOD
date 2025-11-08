<!-- Powered by BMAD™ Core -->

# Review: Audit Temporal Freshness

## Purpose

Audit vault notes for temporal freshness by identifying notes that haven't been updated within a configured threshold period. Prioritizes stale notes by importance (measured by incoming link count and domain criticality) to focus attention on high-impact knowledge that requires updating.

## Inputs

- **vault_path** (String, required): Absolute path to Obsidian vault
- **freshness_threshold_days** (Integer, optional, default: 180): Number of days after which a note is considered stale

## Outputs

- **stale_notes** (Array<Object>): List of stale notes with priority scores
  - `path` (String): Note file path
  - `last_updated` (String): ISO 8601 timestamp of last modification
  - `days_stale` (Integer): Days since last update
  - `staleness_score` (Float): Ratio of days_stale to threshold
  - `importance` (Integer): Calculated importance (incoming_links + domain_critical_bonus)
  - `priority_score` (Float): Staleness score multiplied by importance
- **metrics** (Object): Aggregated freshness metrics
  - `total_notes` (Integer): Total notes analyzed
  - `stale_notes` (Integer): Count of stale notes
  - `stale_ratio` (Float): Percentage of notes that are stale
  - `avg_staleness` (Float): Average staleness in days
  - `health_impact` (String): Impact assessment (critical/high/medium/low)
- **performance_stats** (Object): Execution timing information
  - `query_time` (Float): Time to query all notes (seconds)
  - `processing_time` (Float): Time to process and calculate scores (seconds)
  - `total_time` (Float): Total execution time (seconds)

## Sequential Procedure

### Step 1: Validate Inputs

- Verify `vault_path` is an absolute path (starts with `/` or drive letter on Windows)
- Check that `vault_path` exists and is a directory
- Reject paths containing directory traversal sequences (`../`)
- Verify `vault_path` is within allowed directories (not system directories)
- Confirm `freshness_threshold_days` > 0
- If validation fails, return error with clear message

### Step 2: Query All Notes Using Obsidian MCP Tool

- Connect to Obsidian MCP server
- Call `obsidian.list_notes` with `vault_path` parameter
- Request metadata fields: `last_updated`, `path`, `title`
- Measure and record `query_time`
- If MCP connection fails, return error: "Obsidian MCP server unavailable"

### Step 3: Filter Notes Where last_updated < (now - threshold_days)

- Get current timestamp: `now = datetime.now()`
- Calculate threshold date: `threshold_date = now - timedelta(days=freshness_threshold_days)`
- For each note:
  - Parse `last_updated` to datetime object
  - If `last_updated < threshold_date`, add to stale_notes array
  - Otherwise, skip (note is fresh)
- Handle missing metadata: Use file system modified time as fallback

### Step 4: For Each Stale Note, Calculate staleness_score

- For each stale note:
  - Calculate: `days_stale = (now - last_updated).days`
  - Calculate: `staleness_score = days_stale / freshness_threshold_days`
  - Store both values in note object
- Example: If note is 365 days old with 180-day threshold, `staleness_score = 365/180 ≈ 2.03`

### Step 5: Calculate Importance Score

- For each stale note:
  - Get `incoming_link_count` from vault metadata or link graph analysis
  - Determine if note is domain-critical:
    - Check if note is in designated critical folders (e.g., `/core-concepts/`)
    - Check if note has `domain-critical: true` in frontmatter
    - Check if note is tagged with critical tags (e.g., `#core`, `#methodology`)
  - Calculate: `importance = incoming_link_count + (is_domain_critical ? 10 : 0)`
  - Store importance in note object

### Step 6: Calculate Priority Score

- For each stale note:
  - Calculate: `priority_score = staleness_score * importance`
  - Higher priority_score = higher urgency for updating
  - Store priority_score in note object
- Example: `staleness_score=2.03, importance=15 → priority_score=30.45`

### Step 7: Rank Notes by priority_score (Descending)

- Sort stale_notes array by `priority_score` in descending order
- Highest priority_score appears first (most urgent to update)
- Within same priority_score, sort by `days_stale` descending (oldest first)

### Step 8: Group Results by Staleness Severity

- Classify each stale note into severity category:
  - **critical**: `days_stale > 365` (more than 1 year old)
  - **high**: `180 ≤ days_stale ≤ 365` (6 months to 1 year)
  - **medium**: `90 ≤ days_stale < 180` (3-6 months)
- Add `severity` field to each note object
- Count notes per severity category for metrics

### Step 9: Calculate Metrics

- Calculate aggregated metrics:
  - `total_notes`: Count of all notes in vault
  - `stale_notes`: Length of stale_notes array
  - `stale_ratio`: `stale_notes / total_notes`
  - `avg_staleness`: Mean of all `days_stale` values
  - `health_impact`: Determine based on stale_ratio:
    - critical: `stale_ratio > 0.40` (>40% stale)
    - high: `0.25 < stale_ratio ≤ 0.40` (25-40% stale)
    - medium: `0.10 < stale_ratio ≤ 0.25` (10-25% stale)
    - low: `stale_ratio ≤ 0.10` (≤10% stale)

### Step 10: Format Results with All Required Fields

- For each stale note, ensure object contains:
  - `path` (String): Full note path
  - `last_updated` (String): ISO 8601 timestamp
  - `days_stale` (Integer): Days since last update
  - `staleness_score` (Float): Calculated score
  - `importance` (Integer): Calculated importance
  - `priority_score` (Float): Final priority score
  - `severity` (String): Severity category
- Remove any temporary fields used during processing

### Step 11: Record Performance Stats

- Calculate and store:
  - `query_time`: Time spent querying notes (from Step 2)
  - `processing_time`: Time spent processing and calculating (Steps 3-10)
  - `total_time`: `query_time + processing_time`
- Format times as floating point seconds (2 decimal places)

### Step 12: Return Structured Results Object

- Return object containing:
  - `stale_notes`: Sorted, prioritized array of stale note objects
  - `metrics`: Aggregated statistics object
  - `performance_stats`: Timing information object
- Include success status: `{ success: true, ... }` or `{ success: false, error: "..." }`

## Security Considerations

### Input Validation

- **vault_path must be absolute**: Reject relative paths to prevent path traversal
- **Path must be within allowed directories**: Block access to system directories (`/etc`, `/sys`, `C:\Windows`, etc.)
- **Reject directory traversal sequences**: Paths containing `../` or `..\` are blocked
- **Validate threshold is positive**: `freshness_threshold_days` must be > 0

### Path Traversal Prevention

- Use path canonicalization to resolve symbolic links and `..` sequences
- Compare canonicalized path against allowed vault directories
- Block paths that escape vault boundaries after canonicalization
- Example blocked paths: `/vault/../etc/passwd`, `C:\vault\..\Windows\System32`

### Size Limits (DoS Prevention)

- **Abort if vault exceeds 100,000 notes**: Prevents memory exhaustion and excessive processing
- **Recommendation**: For large vaults (>100,000 notes), use progressive mode
  - Process notes in batches of 10,000
  - Return partial results with checkpoint information
  - Allow resuming from checkpoint for next batch

### Resource Protection

- **Timeout enforcement**: Set maximum execution time of 120 seconds
- **Memory limits**: Monitor memory usage, abort if exceeding threshold
- **Connection pooling**: Reuse MCP connections to avoid connection exhaustion

## Performance Targets

- **Small vaults (1,000 notes)**: < 10 seconds total execution time
- **Medium vaults (10,000 notes)**: < 60 seconds total execution time
- **Large vaults (100,000 notes)**: Progressive mode required (batched processing)

**Breakdown:**
- Query time: ~2-5 seconds for 1,000 notes
- Processing time: ~5-8 seconds for 1,000 notes
- Sorting/formatting: ~1 second for 1,000 notes

**Optimization strategies:**
- Cache link graph if multiple audits run in session
- Use parallel processing for note analysis (if MCP supports async)
- Early exit for vaults with no stale notes

## Error Handling

### Error 1: Empty Vault

**Condition:** Vault contains 0 notes or all notes filtered out

**Response:**
```json
{
  "success": true,
  "stale_notes": [],
  "metrics": {
    "total_notes": 0,
    "stale_notes": 0,
    "stale_ratio": 0.0,
    "avg_staleness": 0.0,
    "health_impact": "low"
  },
  "message": "No notes found in vault"
}
```

### Error 2: No Stale Notes Found

**Condition:** All notes are fresh (within threshold)

**Response:**
```json
{
  "success": true,
  "stale_notes": [],
  "metrics": {
    "total_notes": 1000,
    "stale_notes": 0,
    "stale_ratio": 0.0,
    "avg_staleness": 0.0,
    "health_impact": "low"
  },
  "message": "All notes are fresh (within 180-day threshold)"
}
```

### Error 3: MCP Connection Failure

**Condition:** Obsidian MCP server unavailable or connection timeout

**Response:**
```json
{
  "success": false,
  "error": "Obsidian MCP server unavailable",
  "remediation": "Verify Obsidian MCP server is running and configured correctly"
}
```

### Error 4: Invalid Metadata

**Condition:** Note lacks `last_updated` metadata

**Handling:**
- Log warning: "Note lacks last_updated metadata, using file system timestamp"
- Use file system modified time as fallback
- Continue processing (non-blocking error)
- Include count of fallback usages in metrics

### Error 5: Invalid Vault Path

**Condition:** Path doesn't exist, contains traversal, or outside allowed directories

**Response:**
```json
{
  "success": false,
  "error": "Invalid vault_path: [specific issue]",
  "remediation": "Provide absolute path to valid Obsidian vault within allowed directories"
}
```

### Error 6: Vault Size Exceeded

**Condition:** Vault contains >100,000 notes

**Response:**
```json
{
  "success": false,
  "error": "Vault size limit exceeded (100,000 notes)",
  "remediation": "Use progressive mode for large vaults or filter to specific folders"
}
```

## Example Usage

### Example 1: Basic Freshness Audit

**Input:**
```yaml
vault_path: "/Users/john/Documents/ObsidianVault"
freshness_threshold_days: 180
```

**Output:**
```json
{
  "success": true,
  "stale_notes": [
    {
      "path": "concepts/core-methodology.md",
      "last_updated": "2024-03-15T10:00:00Z",
      "days_stale": 236,
      "staleness_score": 1.31,
      "importance": 15,
      "priority_score": 19.65,
      "severity": "high"
    },
    {
      "path": "references/study-notes.md",
      "last_updated": "2024-01-20T12:00:00Z",
      "days_stale": 291,
      "staleness_score": 1.62,
      "importance": 0,
      "priority_score": 0.0,
      "severity": "high"
    }
  ],
  "metrics": {
    "total_notes": 1000,
    "stale_notes": 200,
    "stale_ratio": 0.20,
    "avg_staleness": 245.5,
    "health_impact": "medium"
  },
  "performance_stats": {
    "query_time": 3.2,
    "processing_time": 5.8,
    "total_time": 9.0
  }
}
```

### Example 2: Strict Threshold (90 days)

**Input:**
```yaml
vault_path: "/Users/john/Documents/ObsidianVault"
freshness_threshold_days: 90
```

**Output:**
```json
{
  "success": true,
  "stale_notes": [
    {
      "path": "projects/active-project.md",
      "last_updated": "2024-07-15T14:30:00Z",
      "days_stale": 114,
      "staleness_score": 1.27,
      "importance": 8,
      "priority_score": 10.16,
      "severity": "high"
    }
  ],
  "metrics": {
    "total_notes": 1000,
    "stale_notes": 450,
    "stale_ratio": 0.45,
    "avg_staleness": 135.2,
    "health_impact": "critical"
  },
  "performance_stats": {
    "query_time": 3.1,
    "processing_time": 6.2,
    "total_time": 9.3
  }
}
```

## Algorithm Pseudocode

```python
def audit_temporal_freshness(vault_path, threshold_days=180):
    # Step 1: Validate inputs
    if not is_absolute_path(vault_path):
        return {"success": False, "error": "vault_path must be absolute"}
    if threshold_days <= 0:
        return {"success": False, "error": "threshold_days must be > 0"}
    if has_path_traversal(vault_path):
        return {"success": False, "error": "Path traversal detected"}

    # Step 2: Query all notes
    start_query = time.now()
    notes = mcp.obsidian.list_notes(vault_path)
    query_time = time.now() - start_query

    if not notes:
        return empty_result()

    # Step 3: Filter stale notes
    start_processing = time.now()
    now = datetime.now()
    threshold_date = now - timedelta(days=threshold_days)
    stale_notes = []

    for note in notes:
        if note.last_updated < threshold_date:
            # Step 4: Calculate staleness score
            days_stale = (now - note.last_updated).days
            staleness_score = days_stale / threshold_days

            # Step 5: Calculate importance
            incoming_links = count_incoming_links(note)
            is_critical = check_domain_critical(note)
            importance = incoming_links + (10 if is_critical else 0)

            # Step 6: Calculate priority
            priority_score = staleness_score * importance

            stale_notes.append({
                'path': note.path,
                'last_updated': note.last_updated,
                'days_stale': days_stale,
                'staleness_score': staleness_score,
                'importance': importance,
                'priority_score': priority_score
            })

    # Step 7: Sort by priority (descending)
    stale_notes.sort(key=lambda x: x['priority_score'], reverse=True)

    # Step 8: Group by severity
    for note in stale_notes:
        if note['days_stale'] > 365:
            note['severity'] = 'critical'
        elif note['days_stale'] >= 180:
            note['severity'] = 'high'
        else:
            note['severity'] = 'medium'

    # Step 9: Calculate metrics
    stale_count = len(stale_notes)
    total_count = len(notes)
    stale_ratio = stale_count / total_count if total_count > 0 else 0
    avg_staleness = mean([n['days_stale'] for n in stale_notes]) if stale_notes else 0

    if stale_ratio > 0.40:
        health_impact = 'critical'
    elif stale_ratio > 0.25:
        health_impact = 'high'
    elif stale_ratio > 0.10:
        health_impact = 'medium'
    else:
        health_impact = 'low'

    metrics = {
        'total_notes': total_count,
        'stale_notes': stale_count,
        'stale_ratio': stale_ratio,
        'avg_staleness': avg_staleness,
        'health_impact': health_impact
    }

    # Step 11: Record performance
    processing_time = time.now() - start_processing
    performance_stats = {
        'query_time': query_time,
        'processing_time': processing_time,
        'total_time': query_time + processing_time
    }

    # Step 12: Return results
    return {
        'success': True,
        'stale_notes': stale_notes,
        'metrics': metrics,
        'performance_stats': performance_stats
    }
```

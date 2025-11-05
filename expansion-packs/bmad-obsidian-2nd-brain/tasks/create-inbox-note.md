<!-- Powered by BMAD™ Core -->

# create-inbox-note

Create an inbox note in Obsidian vault using MCP Tools integration.

## Purpose

Generate a formatted inbox note from the inbox-note-tmpl.yaml template and create it in the Obsidian vault /inbox directory using Obsidian MCP Tools. Handles errors, retries, and filename conflicts.

## Prerequisites

- Obsidian MCP Tools configured in Claude Desktop/Cursor
- Obsidian vault accessible and writeable
- Classification and metadata extraction completed
- Template variables populated

## Inputs

```yaml
inputs:
  content: "..." # Captured content (required)
  content_type: "quote|concept|reference|reflection|question|observation" # Required
  confidence: 0.85 # Float 0.0-1.0 (required)
  source: "https://..." | "Unknown" # Optional
  author: "Name" | "Unknown" # Optional
  captured: "2025-11-04T15:30:00Z" # ISO 8601 (required)
  tags: ["tag1", "tag2"] # Array (optional, default [])
  context: "..." | null # Optional
  flagged_for_review: true|false # Required (true if confidence < 0.7)
```

## Outputs

```yaml
result:
  success: true|false
  note_path: "/inbox/2025-11-04-1530-example-title.md" | null
  error: "Error message" | null
  retry_count: 0-3
```

## Step-by-Step Execution

### Step 1: Load Template

Load `inbox-note-tmpl.yaml` template structure.

**Template variables needed:**

- content_type
- confidence
- source
- author
- captured
- tags
- flagged_for_review
- content
- context (if available)
- timestamp (for filename)
- sanitized_title (for filename)

### Step 2: Generate Filename

**Format:** `YYYY-MM-DD-HHMM-{sanitized-title}.md`

**Steps:**

1. Extract timestamp components from `captured` field
   - YYYY: Year (4 digits)
   - MM: Month (2 digits, zero-padded)
   - DD: Day (2 digits, zero-padded)
   - HH: Hour (2 digits, 24-hour format, zero-padded)
   - MM: Minute (2 digits, zero-padded)

2. Generate sanitized title from content:
   - Take first 50 characters of content
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove special characters (keep only `a-z`, `0-9`, `-`)
   - Remove double hyphens (replace `--` with `-`)
   - Trim leading/trailing hyphens
   - If empty after sanitization: use "untitled"

**Example:**

- Input: "Knowledge work is about managing your attention"
- Timestamp: 2025-11-04T15:30:00Z
- Output: `2025-11-04-1530-knowledge-work-is-about-managing-your-attention.md`

**Collision Handling:**

- If file exists: Append `-2`, `-3`, etc. until unique
- Check using Obsidian MCP `read_note()` - if error (file not found), filename is available

### Step 3: Populate Template Variables

Substitute all variables in template:

**Frontmatter:**

```yaml
---
status: unprocessed
content_type: { { content_type } }
confidence: { { confidence } }
source: { { source } }
author: { { author } }
captured: { { captured } }
tags: [{ { tags } }] # Comma-separated list
flagged_for_review: { { flagged_for_review } }
---
```

**Content Section:**

```markdown
# {{content_type | titlecase}}: {{sanitized_title}}

{{content}}
```

**Context Section (if context provided):**

```markdown
## Context

{{context}}
```

**Processing Notes Section:**

```markdown
## Processing Notes

_To be filled by triage agent or user during processing_
```

**Next Actions Section:**

```markdown
## Next Actions

- [ ] _To be filled by user or organization agent_
```

### Step 4: Create Note via MCP

**Call:** Obsidian MCP Tools `create_note()`

**Parameters:**

- `path`: `/inbox/{filename}`
- `content`: Populated template (full markdown string)

**Example MCP Call:**

```javascript
mcp_tools.obsidian.create_note({
  path: '/inbox/2025-11-04-1530-knowledge-work-is-about.md',
  content: '---\nstatus: unprocessed\n...',
});
```

### Step 5: Handle Response

**Success:**

- MCP returns success status
- Note created in vault
- Return result with note_path

**Failure - Retry Logic:**

Apply exponential backoff retry (max 3 attempts):

1. First attempt: Immediate
2. Second attempt: Wait 1 second
3. Third attempt: Wait 2 seconds
4. Fourth attempt: Wait 4 seconds

**Retry on these errors:**

- Connection timeout
- Vault temporarily unavailable
- Write permission temporarily denied

**Do NOT retry on these errors:**

- Vault not found (configuration issue)
- Invalid path (programming error)
- File already exists (filename collision - handle differently)

**After max retries:**

- Return failure with error message
- Log error for debugging
- DO NOT create Neo4j CaptureEvent (note creation is prerequisite)

### Step 6: Verify Creation (Optional)

For high-confidence operations, verify note was created:

- Call `read_note(path)` to confirm existence
- Compare content checksum if needed

**If verification fails:**

- Log discrepancy
- Return failure

## Error Scenarios

### Vault Not Found

**Error:** "Obsidian vault not found or not configured"

**Cause:** Obsidian MCP not configured or vault path incorrect

**Resolution:**

- Check MCP configuration in settings
- Verify vault path in Obsidian MCP settings
- User must fix configuration before retrying

**Return:**

```yaml
result:
  success: false
  note_path: null
  error: 'Obsidian vault not found. Check MCP configuration.'
  retry_count: 0
```

### Permission Denied

**Error:** "Permission denied writing to vault"

**Cause:** Vault directory not writable

**Resolution:**

- Check file system permissions
- Check if vault is on read-only volume
- User must fix permissions before retrying

**Return:**

```yaml
result:
  success: false
  note_path: null
  error: 'Permission denied. Check vault write permissions.'
  retry_count: 3
```

### File Already Exists

**Error:** "File already exists at path"

**Cause:** Filename collision

**Resolution:**

- Append `-2` to filename and retry
- Continue incrementing until unique filename found
- Maximum 10 attempts to find unique name

**Return (after finding unique name):**

```yaml
result:
  success: true
  note_path: '/inbox/2025-11-04-1530-knowledge-work-is-about-2.md'
  error: null
  retry_count: 1
```

### Connection Timeout

**Error:** "Connection to Obsidian MCP timed out"

**Cause:** Network issue, Obsidian not running, MCP server not responding

**Resolution:**

- Retry with exponential backoff
- If max retries exceeded, fail and notify user

**Return:**

```yaml
result:
  success: false
  note_path: null
  error: 'Connection timeout after 3 retries. Ensure Obsidian is running.'
  retry_count: 3
```

### Invalid Content

**Error:** "Invalid note content"

**Cause:** Template variables not populated correctly

**Resolution:**

- Log template and variables for debugging
- Do not retry (programming error)

**Return:**

```yaml
result:
  success: false
  note_path: null
  error: 'Invalid note content. Template variables may be missing.'
  retry_count: 0
```

## MCP Integration Details

### Required MCP Server

**Server:** obsidian-mcp

**Configuration:** (in MCP settings file)

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "obsidian-mcp",
      "args": ["--vault", "/path/to/vault"]
    }
  }
}
```

### MCP Tool: create_note

**Function:** Creates a new note in Obsidian vault

**Parameters:**

- `path` (string, required): Relative path from vault root (e.g., "/inbox/note.md")
- `content` (string, required): Full markdown content including frontmatter

**Returns:**

```json
{
  "success": true|false,
  "message": "Note created" | "Error message"
}
```

### Alternative MCP Tool: write_file

Some Obsidian MCP implementations use `write_file` instead:

**Parameters:**

- `file_path` (string): Path relative to vault
- `content` (string): Note content

Check MCP documentation for actual function names.

## Testing

### Test Case 1: Successful Creation

**Input:**

- All fields populated correctly
- Vault accessible
- Unique filename

**Expected:**

- success: true
- note_path: Valid path
- error: null
- Note appears in Obsidian vault /inbox directory

### Test Case 2: Filename Collision

**Setup:** Pre-create note with same filename

**Expected:**

- success: true
- note_path: Path with `-2` suffix
- error: null

### Test Case 3: Vault Not Found

**Setup:** Misconfigure MCP settings

**Expected:**

- success: false
- note_path: null
- error: "Obsidian vault not found..."

### Test Case 4: Retry on Timeout

**Setup:** Simulate connection timeout

**Expected:**

- retry_count: 3
- success: false (after exhausting retries)
- error: "Connection timeout after 3 retries..."

### Test Case 5: Special Characters in Content

**Input:** Content with emojis, Unicode, markdown special chars

**Expected:**

- success: true
- Content preserved exactly
- Filename sanitized correctly

## Integration with Other Tasks

**Inputs from:**

- `classify-content-type.md` - Provides content_type and confidence
- `extract-metadata.md` - Provides source, author, timestamp, context, tags

**Outputs to:**

- `create-capture-event.md` - Passes note_path for Neo4j relationship
- `capture-quality-checklist.md` - Item 8 validation

**Used by:**

- `*capture` command - Creates note for manual capture
- `*process-inbox` command - Creates notes for batch processing
- `*batch-process` command - Creates multiple notes in sequence

## Performance Considerations

- Target: < 2 seconds per note creation (including retries)
- MCP call typically < 200ms
- Retry backoff adds max 7 seconds (1+2+4) if needed
- Batch processing: Create notes sequentially to avoid overwhelming MCP

## Security

- All content sanitized before template substitution
- No code injection possible in frontmatter YAML
- Markdown special characters preserved (not escaped)
- Filenames sanitized to prevent directory traversal

## Example Full Note Output

```markdown
---
status: unprocessed
content_type: quote
confidence: 0.95
source: https://twitter.com/naval/status/1234567890
author: @naval
captured: 2025-11-04T15:30:00Z
tags: [twitter, philosophy, startups]
flagged_for_review: false
---

# Quote: knowledge-work-is-about-managing-your-attention

"Knowledge work is about managing your attention, not your time." - Naval Ravikant

## Processing Notes

_To be filled by triage agent or user during processing_

## Next Actions

- [ ] _To be filled by user or organization agent_
```

## Troubleshooting

**Issue:** Notes not appearing in Obsidian

**Check:**

1. Obsidian vault path correct in MCP settings?
2. Obsidian application running?
3. /inbox folder exists in vault?
4. File system permissions allow writes?
5. MCP server logs for errors?

**Issue:** Filename collisions frequent

**Cause:** Multiple captures in same minute

**Solution:**

- Append milliseconds to filename for finer granularity
- Or append random 4-character suffix

**Issue:** Frontmatter not parsing

**Cause:** YAML syntax error in variables

**Solution:**

- Validate YAML before substitution
- Escape YAML special characters in content

<!-- Powered by BMAD™ Core -->

# Capture: Create Inbox Note

## Purpose

Create an inbox note in Obsidian vault using classified content and extracted metadata following the inbox-note-tmpl.yaml template structure.

## Inputs

- **classified_content** (Object, required): Classification result from capture-classify-content-type task
  - `content_type` (String): One of 6 types (quote, concept, reference, reflection, question, observation)
  - `confidence` (Float): 0.0-1.0 confidence score
  - `raw_content` (String): Original captured text
  - `reasoning` (String): Classification reasoning
  - `matched_patterns` (Array<String>): Patterns that matched

- **metadata** (Object, required): Extracted metadata from capture-extract-metadata task
  - `source_url` (String): Source URL or "Unknown"
  - `author` (String): Author name or "Unknown"
  - `title` (String): Title (extracted or auto-generated)
  - `timestamp` (String): ISO8601 timestamp
  - `surrounding_context` (String): Context (can be empty)

- **vault_path** (String, required): Obsidian vault root path (e.g., "/Users/username/Obsidian/SecondBrain")

## Procedure

### Step 1: Load Inbox Note Template

- Load template file: `expansion-packs/bmad-obsidian-2nd-brain/templates/inbox-note-tmpl.yaml`
- Parse YAML structure
- Verify template file exists and is readable
- If template not found, return error: "inbox-note-tmpl.yaml not found at expected location"

### Step 2: Validate Template Structure

Verify template contains required sections:

- ✓ `template.id` exists
- ✓ `variables` section exists
- ✓ `sections` array exists
- ✓ Required sections present: `frontmatter`, `content`, `processing_notes`, `next_actions`

If validation fails, return error with details: "Template validation failed: [missing section]"

### Step 3: Populate Template Variables

Map input data to template variables:

**From classified_content:**

- `{{content_type}}` → `classified_content.content_type`
- `{{confidence}}` → `classified_content.confidence` (formatted to 2 decimal places)
- `{{content}}` → `classified_content.raw_content`

**From metadata:**

- `{{source}}` → `metadata.source_url`
- `{{author}}` → `metadata.author`
- `{{captured}}` → `metadata.timestamp` (ISO8601 format)
- `{{context}}` → `metadata.surrounding_context` (only include section if non-empty)

**Computed variables:**

- `{{flagged_for_review}}` → `true` if confidence < 0.7, else `false`
- `{{tags}}` → Default to `[]` (empty array, can be enriched later by agent)
- `{{timestamp}}` → Convert `metadata.timestamp` to filename format: `YYYY-MM-DD-HHMM`
  - Example: `2025-11-06T10:30:00Z` → `2025-11-06-1030`
- `{{sanitized_title}}` → Sanitize `metadata.title` for filename:
  - Convert to lowercase
  - Replace spaces with hyphens
  - Remove special characters (keep only: a-z, 0-9, hyphens)
  - Limit to 50 characters
  - Example: "Deep Work Principles" → "deep-work-principles"

### Step 4: Generate Note Filename

Construct filename using template pattern: `{{timestamp}}-{{sanitized_title}}.md`

**Format:** `YYYY-MM-DD-HHMM-sanitized-title.md`

**Examples:**

- `2025-11-06-1030-deep-work-principles.md`
- `2025-11-06-1445-atomic-notes-concept.md`
- `2025-11-06-0915-spaced-repetition.md`

**Collision handling:**

- If filename already exists, append random 4-character suffix: `-a3f2`
- Example: `2025-11-06-1030-deep-work-principles-a3f2.md`
- Retry up to 3 times if collision persists

### Step 5: Construct Full Note Path

Construct full path: `vault_path/inbox/YYYY-MM-DD-HHMM-sanitized-title.md`

**Path construction:**

1. Start with `vault_path` (e.g., `/Users/username/Obsidian/SecondBrain`)
2. Append `/inbox/` subdirectory
3. Append generated filename

**Example paths:**

- `/Users/username/Obsidian/SecondBrain/inbox/2025-11-06-1030-deep-work-principles.md`
- `/Users/username/Obsidian/SecondBrain/inbox/2025-11-06-1445-atomic-notes-concept.md`

### Step 6: Validate Path

Apply path security validation:

**Block directory traversal:**

- Check for `../` or `..\\` patterns
- Check for absolute paths that escape vault root
- Verify path resolves within vault bounds

**Sanitize filename:**

- Remove special characters: `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`
- Keep only: alphanumeric, hyphens, underscores, periods, spaces

**Validate vault_path:**

- Verify vault_path exists and is a directory
- Verify vault_path/inbox/ directory exists or create it
- Check write permissions

**If validation fails:**

- Return error: "Invalid path: [reason]"
- Examples: "Invalid path: directory traversal blocked", "Invalid path: vault not found"

### Step 7: Render Note Content from Template

Generate markdown content by populating template sections:

**Section 1: Frontmatter**

```yaml
---
status: unprocessed
content_type: { { content_type } }
confidence: { { confidence } }
source: { { source } }
author: { { author } }
captured: { { captured } }
tags: { { tags } }
flagged_for_review: { { flagged_for_review } }
---
```

**Section 2: Content**

```markdown
# {{content_type | titlecase}}: {{sanitized_title}}

{{content}}
```

**Section 3: Context (conditional - only if context not empty)**

```markdown
## Context

{{context}}
```

**Section 4: Processing Notes (placeholder)**

```markdown
## Processing Notes

_To be filled by triage agent or user during processing_
```

**Section 5: Next Actions (placeholder)**

```markdown
## Next Actions

- [ ] _To be filled by user or organization agent_
```

**Apply template rendering:**

- Replace all `{{variable}}` placeholders with actual values
- Apply filters: `| titlecase` (capitalize first letter of each word)
- Escape YAML frontmatter values properly (quote strings with special chars)
- Include conditional sections only if condition met (e.g., context section only if context non-empty)

### Step 8: Call Obsidian MCP to Create Note

Use Obsidian MCP `obsidian.create_note` tool:

**MCP Call Parameters:**

```javascript
{
  path: "inbox/2025-11-06-1030-deep-work-principles.md",  // Relative to vault root
  content: "[rendered markdown content from Step 7]",      // Full note content
  vault: "[vault_name]"                                    // Optional: extract from vault_path
}
```

**Handle MCP Response:**

```javascript
{
  success: true/false,      // Boolean indicating success
  note_path: "inbox/...",   // String: full path to created note
  error: null/string        // String: error message if failure
}
```

**MCP Call Example:**

```javascript
obsidian.create_note({
  path: 'inbox/2025-11-06-1030-deep-work-principles.md',
  content: '---\nstatus: unprocessed\ncontent_type: concept\n...\n',
  vault: 'SecondBrain',
});
```

**If MCP unavailable:**

- Return error: "Obsidian MCP not available, ensure MCP Tools configured"
- Provide remediation: "Install Obsidian MCP server and configure in Claude Desktop/Cursor settings"

### Step 9: Verify Note Created Successfully

Check MCP response:

**If success = true:**

- Extract `note_path` from response
- Verify `note_path` matches expected path
- Proceed to Step 10

**If success = false:**

- Check error message for reason
- Apply error handling strategy (see Error Handling section)
- Attempt retry if appropriate (e.g., path collision)
- If retry fails, return error with details

**Common failure scenarios:**

- Permission denied: Check vault write permissions
- Disk full: Check available disk space
- Path already exists: Append random suffix and retry
- Vault not found: Verify vault_path is correct

### Step 10: Return Success with Created Note Path

Return success response:

```json
{
  "inbox_note_path": "/Users/username/Obsidian/SecondBrain/inbox/2025-11-06-1030-deep-work-principles.md",
  "creation_timestamp": "2025-11-06T10:30:15Z",
  "success": true,
  "error": null
}
```

**Log success:**

- Log note creation: "Inbox note created successfully: [path]"
- Log file size and creation time for monitoring
- Update capture statistics (optional)

## Outputs

- **inbox_note_path** (String): Full path to created inbox note
- **creation_timestamp** (String): ISO8601 timestamp when note was created
- **success** (Boolean): `true` if note created successfully, `false` if error occurred
- **error** (String): Error message if failure occurred, `null` if successful

## Obsidian MCP Integration

### MCP Tool: obsidian.create_note

**Purpose:** Create new markdown file in Obsidian vault with YAML frontmatter

**Parameters:**

- **path** (String, required): Relative path from vault root
  - Example: `"inbox/2025-11-06-1030-deep-work-principles.md"`
  - Must be relative, not absolute
  - Directory separators: use `/` (forward slash)

- **content** (String, required): Full markdown content including YAML frontmatter
  - Must be valid markdown
  - Must include properly formatted YAML frontmatter if present
  - Preserve line breaks with `\n`

- **vault** (String, optional): Vault name if multiple vaults configured
  - Example: `"SecondBrain"`
  - If not provided, uses default vault
  - Must match actual vault name in Obsidian

**Response:**

```javascript
{
  success: true,                    // Boolean: operation success status
  note_path: "inbox/...",          // String: path to created note
  error: null                      // String: error message if failure, null if success
}
```

**Example MCP Call:**

```javascript
obsidian.create_note({
  path: 'inbox/2025-11-06-1030-deep-work-principles.md',
  content: `---
status: unprocessed
content_type: concept
confidence: 0.85
source: https://example.com/deep-work
author: Cal Newport
captured: 2025-11-06T10:30:00Z
tags: []
flagged_for_review: false
---

# Concept: Deep Work Principles

Deep work is the ability to focus without distraction on a cognitively demanding task...

## Processing Notes

*To be filled by triage agent or user during processing*

## Next Actions

- [ ] *To be filled by user or organization agent*
`,
  vault: 'SecondBrain',
});
```

**Expected Response:**

```javascript
{
  success: true,
  note_path: "inbox/2025-11-06-1030-deep-work-principles.md",
  error: null
}
```

## Error Handling

### Error 1: Obsidian MCP Unavailable

**Condition:** Obsidian MCP not configured or not responding

**Response:**

```json
{
  "success": false,
  "error": "Obsidian MCP not available, ensure MCP Tools configured",
  "remediation": "Install Obsidian MCP server and configure in Claude Desktop/Cursor settings. See: https://docs.obsidian.md/mcp-integration"
}
```

**Blocking:** YES (cannot create notes without Obsidian MCP)

### Error 2: Write Failure (Permissions/Disk Full)

**Condition:** MCP returns success=false due to write failure

**Response:**

```json
{
  "success": false,
  "error": "Failed to write note: [MCP error details]",
  "remediation": "Check vault write permissions and available disk space"
}
```

**Possible causes:**

- Permission denied: User lacks write permission to vault/inbox directory
- Disk full: No available disk space
- Vault locked: Vault is read-only or locked by another process

**Blocking:** YES (cannot proceed without write access)

### Error 3: Path Already Exists

**Condition:** File already exists at target path

**Response:**

- Append random 4-character suffix to filename: `-a3f2`
- Example: `2025-11-06-1030-deep-work-principles-a3f2.md`
- Retry note creation with new filename
- If retry succeeds, return success with modified path
- If retry fails (3 attempts), return error:

```json
{
  "success": false,
  "error": "Failed to create note after 3 collision resolution attempts",
  "remediation": "Check inbox directory for existing notes, consider different timestamp or title"
}
```

**Blocking:** YES if retries exhausted, NO if retry succeeds

### Error 4: Template Not Found

**Condition:** inbox-note-tmpl.yaml not found at expected location

**Response:**

```json
{
  "success": false,
  "error": "inbox-note-tmpl.yaml not found at expansion-packs/bmad-obsidian-2nd-brain/templates/",
  "remediation": "Ensure STORY-002 completed and template file exists. Verify expansion pack installation."
}
```

**Blocking:** YES (cannot create note without template)

### Error 5: Invalid Template

**Condition:** Template file exists but validation fails (malformed YAML, missing sections)

**Response:**

```json
{
  "success": false,
  "error": "Template validation failed: [specific missing section or malformed structure]",
  "remediation": "Verify inbox-note-tmpl.yaml is valid YAML and contains required sections: frontmatter, content, processing_notes, next_actions"
}
```

**Blocking:** YES (cannot render note from invalid template)

### Error 6: Invalid Vault Path

**Condition:** vault_path does not exist or is not a directory

**Response:**

```json
{
  "success": false,
  "error": "Invalid vault path: [path] does not exist or is not a directory",
  "remediation": "Verify vault_path points to valid Obsidian vault root directory"
}
```

**Blocking:** YES (cannot create note in non-existent vault)

## Rollback Strategy

### Atomic Operation

Obsidian MCP `create_note` is **atomic**:

- Note is either fully created or not created at all
- No partial writes that require cleanup
- No rollback needed if creation fails

### Rollback Scenarios

**If template population fails:**

- No file created yet (failure before MCP call)
- No rollback needed
- Return error with details

**If MCP call fails:**

- Obsidian handles atomicity
- No partial file left behind
- No cleanup required

**If path validation fails:**

- Failure before MCP call
- No file created
- No rollback needed

**Summary:** All failures occur before file creation (validation, template rendering) or are handled atomically by Obsidian MCP. No explicit rollback strategy required.

## Security

### Path Sanitization (Directory Traversal Prevention)

**Block directory traversal patterns:**

- `../` (parent directory)
- `..\\` (Windows parent directory)
- Absolute paths: `/`, `C:\\`
- Symlink exploitation

**Validation:**

- Resolve path to absolute path
- Verify resolved path is within vault bounds
- Reject if path escapes vault directory

**Example blocked paths:**

```
❌ "../../../etc/passwd"
❌ "/etc/passwd"
❌ "C:\\Windows\\System32\\config"
❌ "inbox/../../../etc/passwd"
✅ "inbox/2025-11-06-1030-note.md"
```

### Content Validation

**Vault bounds:**

- Ensure path within vault directory tree
- No escaping vault root
- Verify vault_path is absolute and valid

**Filename sanitization:**

- Remove special chars: `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`
- Keep only: a-z, A-Z, 0-9, `-`, `_`, `.`, space
- Prevent null bytes: `\x00`

### YAML Frontmatter Escaping

**Escape YAML special characters:**

- `:` → Quote value if contains colon
- `#` → Quote value if starts with hash
- `-`, `[`, `]`, `{`, `}`, `|`, `>` → Quote if needed

**Example escaping:**

```yaml
# Unescaped (unsafe)
title: Understanding: Deep Work

# Escaped (safe)
title: "Understanding: Deep Work"
```

**Quote string values:**

- Quote strings containing special chars
- Use double quotes: `"value"`
- Escape quotes within strings: `"He said \"hello\""`

### Size Limits

**Content size:**

- Max 10MB per note (inherited from classification input limit)
- Already enforced in earlier steps

**Metadata size:**

- Max 1MB (inherited from metadata extraction)
- Verify total note size < 10MB before creation

## Performance Target

**Target execution time:** < 3 seconds per note creation

**Performance breakdown:**

- Template loading: < 100ms
- Template rendering: < 200ms
- MCP call latency: < 2s
- Path validation: < 50ms
- Total: ~2.35s (buffer for network latency)

**Performance considerations:**

- Cache template in memory (load once, reuse)
- Minimize regex operations during rendering
- Efficient string concatenation
- No external API calls except Obsidian MCP

**Monitoring:**

- Log note creation time for each execution
- Alert if average time exceeds 3s target
- Track MCP latency separately

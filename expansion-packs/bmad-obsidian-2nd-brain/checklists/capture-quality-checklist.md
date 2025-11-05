<!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Capture Quality Checklist

# ------------------------------------------------------------

---

checklist:
id: capture-quality-checklist
name: Capture Quality Checklist
description: Quality gates for content capture before finalizing inbox notes
items: - "[ ] Content is non-empty (minimum 10 characters)" - "[ ] Content type classified with confidence >= 0.5" - "[ ] Source URL is valid format (if present)" - "[ ] Author extracted or marked as 'Unknown'" - "[ ] Timestamp is valid ISO 8601 format" - "[ ] No HTML/JavaScript injection detected" - "[ ] Filename follows naming convention (YYYY-MM-DD-HHMM-sanitized-title.md)" - "[ ] Inbox note created successfully in Obsidian" - "[ ] Neo4j CaptureEvent created (if enabled) or skipped gracefully" - "[ ] Template all required fields populated"

---

## Purpose

This checklist ensures every captured piece of content meets minimum quality standards before being finalized as an inbox note. It serves as a quality gate to prevent garbage data from entering the knowledge system.

## When to Use

- After classification and metadata extraction
- Before creating inbox note in Obsidian
- Before creating Neo4j CaptureEvent
- During batch processing operations
- When validating captures in testing

## Quality Criteria Details

### 1. Content is non-empty (minimum 10 characters)

**Check:** Content field contains at least 10 characters of meaningful text

**Remediation if failed:**

- Reject capture with error: "Content too short or empty"
- Log rejected capture for manual review
- Do not create inbox note or Neo4j event

### 2. Content type classified with confidence >= 0.5

**Check:** Classification algorithm returns confidence score >= 0.5 for the selected type

**Remediation if failed:**

- Default to "observation" type with confidence 0.4
- Flag for manual review (flagged_for_review: true)
- Add note in Processing Notes: "Low confidence classification - requires manual review"

### 3. Source URL is valid format (if present)

**Check:** If source field contains URL, validate it matches safe URL regex pattern

**Allowed protocols:** http://, https://

**Blocked protocols:** file://, javascript:, data:, vbscript:

**Remediation if failed:**

- If dangerous protocol: Strip URL, set source to "Unknown (unsafe URL removed)"
- If malformed URL: Keep as plain text description (not URL)
- Log validation failure for security audit

### 4. Author extracted or marked as 'Unknown'

**Check:** Author field is populated (not empty, not null)

**Remediation if failed:**

- Set author to "Unknown"
- Continue processing (this is not a blocking failure)

### 5. Timestamp is valid ISO 8601 format

**Check:** Timestamp matches pattern: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS+00:00

**Remediation if failed:**

- Use current timestamp as fallback
- Add note in Processing Notes: "Invalid source timestamp, using capture time"
- Log validation failure

### 6. No HTML/JavaScript injection detected

**Check:** Scan content for dangerous patterns:

- `<script>`, `<iframe>`, `<object>`, `<embed>` tags
- Event handlers: `onclick`, `onerror`, `onload`, etc.
- JavaScript execution attempts

**Remediation if failed:**

- Escape all HTML entities: `<`, `>`, `&`, `"`, `'`
- Strip all dangerous tags completely
- Log security event for audit
- Continue with sanitized content

### 7. Filename follows naming convention

**Check:** Generated filename matches pattern: YYYY-MM-DD-HHMM-{sanitized-title}.md

**Sanitization rules:**

- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters (keep only alphanumeric and hyphens)
- Limit to first 50 characters of title
- Ensure no double hyphens

**Remediation if failed:**

- Regenerate filename using capture timestamp + "untitled"
- Pattern: 2025-11-04-1530-untitled.md
- Continue processing

### 8. Inbox note created successfully in Obsidian

**Check:** MCP Tools create_note() returns success

**Remediation if failed:**

- Retry up to 3 times with exponential backoff (1s, 2s, 4s)
- If all retries fail, log error and halt processing
- Do not create Neo4j CaptureEvent if note creation failed
- Possible errors:
  - Vault not found: Check Obsidian MCP configuration
  - Permission denied: Check vault write permissions
  - File exists: Append timestamp to filename and retry

### 9. Neo4j CaptureEvent created (if enabled) or skipped gracefully

**Check:**

- If neo4j.enabled: true in config → Graphiti MCP create_episode() returns success
- If neo4j.enabled: false → Skip Neo4j operations completely

**Remediation if failed:**

- If enabled but connection failed: Log warning, continue (degrade gracefully)
- If enabled but Graphiti error: Log error, continue (inbox note still valid)
- Set Neo4j event_id to null in response
- Add note in Processing Notes: "Neo4j integration unavailable"

### 10. Template all required fields populated

**Check:** Verify inbox-note-tmpl.yaml variables all have values:

- content_type (required)
- confidence (required)
- source (optional, use "Unknown" if empty)
- author (optional, use "Unknown" if empty)
- captured (required)
- tags (optional, default to [])
- content (required)
- context (optional)
- timestamp (required)
- sanitized_title (required)

**Remediation if failed:**

- If required field missing: Halt processing, log error
- If optional field missing: Use default value
- Validate all fields populated before template rendering

---

## Pass/Fail Criteria

**PASS:** All 10 items checked and passed (or gracefully handled)

**FAIL:** Any of these blocking failures:

- Content too short or empty (item 1)
- Classification confidence < 0.4 after fallback (item 2)
- Inbox note creation failed after retries (item 8)
- Required template field missing (item 10)

**WARNINGS:** Non-blocking issues that should be logged:

- Low confidence (0.5-0.7) - flag for review but continue
- Neo4j unavailable - continue with Obsidian-only mode
- Author unknown - acceptable, use default
- Source URL malformed - treat as text description

---

## Usage in Agent Commands

### \*capture command

Run full checklist before finalizing capture

### \*process-inbox command

Run checklist on each unprocessed item

### \*batch-process command

Run checklist on all items, collect failures for review

### \*yolo mode

Still run checklist, but auto-accept warnings (not errors)

---

## Testing

To test this checklist, create test captures with:

- Empty content (expect: fail item 1)
- Ambiguous content (expect: warning item 2)
- file:// URL (expect: sanitization item 3)
- Invalid timestamp (expect: fallback item 5)
- XSS payload in content (expect: sanitization item 6)
- Obsidian vault disconnected (expect: fail item 8)
- Neo4j disabled (expect: skip item 9)

All test scenarios documented in story testing section.

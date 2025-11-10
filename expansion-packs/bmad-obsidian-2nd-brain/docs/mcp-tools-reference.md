# MCP Tools Reference Documentation

This document provides complete API reference for interacting with Obsidian vaults through the Model Context Protocol (MCP). It covers three layers of integration: MCP high-level capabilities, common MCP tool functions, and underlying REST API endpoints.

## Architecture Overview

The Obsidian MCP integration consists of three layers:

```
┌─────────────────────────────────────────────┐
│   AI Assistant (Claude, ChatGPT, etc.)     │
│   Uses natural language to request actions │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│   MCP Layer (Model Context Protocol)       │
│   - Vault Access                            │
│   - Semantic Search                         │
│   - Template Integration                    │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│   MCP Server Binary                         │
│   Translates MCP requests to API calls     │
│   Tool functions: read_note, update_note... │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│   Local REST API Plugin                     │
│   HTTP endpoints: /vault/, /active/, etc.   │
│   Direct vault file operations              │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│   Obsidian Vault (Markdown files)          │
│   Your notes, folders, attachments          │
└─────────────────────────────────────────────┘
```

---

## Layer 1: High-Level MCP Capabilities

The MCP Tools plugin provides three primary capabilities accessible through natural language with Claude or other MCP-compatible assistants.

### 1. Vault Access

**Purpose:** Allows AI assistants to read and reference notes in your Obsidian vault.

**Capabilities:**
- Read note contents
- List files and directories
- Check note metadata (frontmatter, tags, links)
- Navigate folder structure

**Example Usage:**
```
User: "Read my note about atomic habits"
Claude: [Uses MCP to search and read the note]

User: "List all notes in my Projects folder"
Claude: [Uses MCP to list directory contents]
```

**Security:**
- Read-only by default for AI interactions
- Write operations require explicit confirmation
- API key authentication required
- All operations logged

### 2. Semantic Search

**Purpose:** Search vault based on meaning and context, not just keywords.

**Capabilities:**
- Find conceptually related notes
- Discover connections between ideas
- Suggest relevant notes for current context
- Natural language query understanding

**Requirements:**
- Smart Connections plugin installed and configured
- Vault indexed with embeddings (BGE-micro-v2 by default)
- Semantic search model loaded

**Example Usage:**
```
User: "Find notes related to personal knowledge management"
Claude: [Performs semantic search, returns relevant notes even if they don't contain exact phrase]

User: "What notes are similar to my current note about Zettelkasten?"
Claude: [Uses embedding similarity to find related notes]
```

**Performance:**
- Search speed depends on vault size
- 1000 notes: < 2 seconds
- 10,000 notes: < 5 seconds
- Incremental indexing (only new/modified notes)

### 3. Template Integration

**Purpose:** Execute Obsidian templates through AI interactions with dynamic parameters.

**Capabilities:**
- Create notes from templates
- Execute Templater scripts
- Fill template variables dynamically
- Integrate with Obsidian template system

**Requirements:**
- Templater plugin installed (optional but recommended)
- Templates defined in vault
- Template folder configured in Obsidian settings

**Example Usage:**
```
User: "Create a meeting note for tomorrow's standup"
Claude: [Uses template for meeting notes, fills in date/time automatically]

User: "Use my book notes template for 'Atomic Habits'"
Claude: [Creates note from template with title pre-filled]
```

---

## Layer 2: Common MCP Tool Functions

MCP servers expose standardized tool functions that AI assistants can call. These are the common tools you'll interact with through Claude Desktop.

### obsidian_read_note

**Description:** Retrieves content and metadata from a specified note.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | string | Yes | Path to the note file (relative to vault root) |
| `format` | string | No | Output format: `"markdown"` (default) or `"json"` |
| `includeStat` | boolean | No | Include file statistics (timestamps, size) |

**Return Value:**
```json
{
  "content": "# Note Title\n\nNote content...",
  "frontmatter": {
    "tags": ["tag1", "tag2"],
    "created": "2025-01-01",
    "modified": "2025-01-15"
  },
  "stat": {
    "ctime": 1704067200000,
    "mtime": 1705276800000,
    "size": 1234
  }
}
```

**Usage Example:**
```javascript
// Claude internally calls:
obsidian_read_note({
  filePath: "Projects/Website Redesign.md",
  format: "markdown",
  includeStat: true
})
```

**Error Codes:**
- `404` - Note not found at specified path
- `403` - Permission denied (file outside vault)
- `500` - Read error (file corrupted, encoding issue)

---

### obsidian_update_note

**Description:** Modifies note content through append, prepend, or overwrite operations.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | string | Yes | Path to the note file |
| `content` | string | Yes | Content to add or replace |
| `mode` | string | Yes | Operation mode: `"append"`, `"prepend"`, or `"overwrite"` |
| `heading` | string | No | Target heading for section-specific updates |
| `createIfNotExists` | boolean | No | Create note if it doesn't exist (default: false) |

**Mode Behaviors:**

- **`append`**: Adds content to end of file
- **`prepend`**: Adds content to beginning of file
- **`overwrite`**: Replaces entire file content

**Return Value:**
```json
{
  "success": true,
  "filePath": "Projects/Website Redesign.md",
  "bytesWritten": 234,
  "timestamp": 1705276800000
}
```

**Usage Example (Append):**
```javascript
obsidian_update_note({
  filePath: "Daily/2025-01-15.md",
  content: "\n## Meeting Notes\n- Discussed project timeline",
  mode: "append"
})
```

**Usage Example (Update Section):**
```javascript
obsidian_update_note({
  filePath: "Projects/Website Redesign.md",
  content: "\n- Completed wireframes\n- Started design mockups",
  mode: "append",
  heading: "Progress"
})
```

**Error Codes:**
- `404` - Note not found (and createIfNotExists=false)
- `403` - Permission denied
- `409` - Conflict (file modified by another process)
- `500` - Write error

---

### obsidian_create_note

**Description:** Creates a new note with optional frontmatter and content.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | string | Yes | Path where note should be created |
| `content` | string | No | Initial note content (default: empty) |
| `frontmatter` | object | No | YAML frontmatter key-value pairs |
| `overwrite` | boolean | No | Overwrite if file exists (default: false) |

**Return Value:**
```json
{
  "success": true,
  "filePath": "Inbox/New Idea.md",
  "created": true,
  "timestamp": 1705276800000
}
```

**Usage Example:**
```javascript
obsidian_create_note({
  filePath: "Atomic/Concepts/Spaced Repetition.md",
  content: "# Spaced Repetition\n\nA learning technique...",
  frontmatter: {
    "tags": ["learning", "memory"],
    "type": "concept",
    "created": "2025-01-15"
  }
})
```

**Error Codes:**
- `409` - File already exists (and overwrite=false)
- `403` - Permission denied
- `400` - Invalid path (directory traversal, invalid characters)
- `500` - Write error

---

### obsidian_delete_note

**Description:** Permanently deletes a note from the vault.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | string | Yes | Path to the note to delete |
| `moveToTrash` | boolean | No | Move to Obsidian trash instead of permanent delete (default: true) |

**Return Value:**
```json
{
  "success": true,
  "filePath": "Inbox/Old Note.md",
  "deleted": true,
  "timestamp": 1705276800000
}
```

**Usage Example:**
```javascript
obsidian_delete_note({
  filePath: "Drafts/Outdated Idea.md",
  moveToTrash: true
})
```

**Error Codes:**
- `404` - Note not found
- `403` - Permission denied
- `500` - Delete error

**Security Note:** Use with caution. Permanent deletion (moveToTrash=false) is irreversible.

---

### obsidian_search_notes

**Description:** Searches vault for notes matching text query or regex pattern.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search term or regex pattern |
| `path` | string | No | Limit search to specific directory |
| `useRegex` | boolean | No | Treat query as regex (default: false) |
| `caseSensitive` | boolean | No | Case-sensitive search (default: false) |
| `matchWhole` | boolean | No | Match whole words only (default: false) |
| `limit` | number | No | Maximum results to return (default: 50) |

**Return Value:**
```json
{
  "results": [
    {
      "filePath": "Projects/Website Redesign.md",
      "matches": [
        {
          "lineNumber": 15,
          "lineContent": "...atomic design principles...",
          "matchStart": 3,
          "matchEnd": 19
        }
      ],
      "matchCount": 3
    }
  ],
  "totalResults": 12,
  "searchTime": 45
}
```

**Usage Example (Basic Search):**
```javascript
obsidian_search_notes({
  query: "atomic design",
  caseSensitive: false,
  limit: 10
})
```

**Usage Example (Regex Search):**
```javascript
obsidian_search_notes({
  query: "TODO|FIXME|HACK",
  useRegex: true,
  path: "Projects/"
})
```

**Performance:**
- Small vault (< 100 notes): < 50ms
- Medium vault (100-1000 notes): < 500ms
- Large vault (> 1000 notes): < 2s

**Error Codes:**
- `400` - Invalid regex pattern
- `403` - Permission denied
- `500` - Search error

---

### obsidian_list_notes

**Description:** Lists notes and subdirectories within a vault folder.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dirPath` | string | No | Directory path to list (default: vault root "/") |
| `recursive` | boolean | No | Include subdirectories recursively (default: false) |
| `fileFilter` | string | No | File extension filter (e.g., "md", "pdf") |
| `namePattern` | string | No | Regex pattern to match filenames |

**Return Value:**
```json
{
  "path": "Projects/",
  "files": [
    {
      "name": "Website Redesign.md",
      "path": "Projects/Website Redesign.md",
      "isDirectory": false,
      "size": 2456,
      "modified": 1705276800000
    },
    {
      "name": "Mobile App",
      "path": "Projects/Mobile App",
      "isDirectory": true
    }
  ],
  "totalFiles": 15,
  "totalDirectories": 3
}
```

**Usage Example (List Root):**
```javascript
obsidian_list_notes({
  dirPath: "/"
})
```

**Usage Example (Recursive):**
```javascript
obsidian_list_notes({
  dirPath: "Projects/",
  recursive: true,
  fileFilter: "md"
})
```

**Error Codes:**
- `404` - Directory not found
- `403` - Permission denied
- `500` - List error

---

### obsidian_manage_frontmatter

**Description:** Get, set, or delete YAML frontmatter properties in notes.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | string | Yes | Path to the note file |
| `operation` | string | Yes | Operation: `"get"`, `"set"`, or `"delete"` |
| `key` | string | Conditional | Frontmatter key name (required for set/delete) |
| `value` | any | Conditional | Value to set (required for set operation) |

**Return Value (get):**
```json
{
  "frontmatter": {
    "tags": ["project", "web"],
    "status": "in-progress",
    "priority": "high",
    "created": "2025-01-01"
  }
}
```

**Return Value (set/delete):**
```json
{
  "success": true,
  "key": "status",
  "value": "completed",
  "timestamp": 1705276800000
}
```

**Usage Example (Get All):**
```javascript
obsidian_manage_frontmatter({
  filePath: "Projects/Website Redesign.md",
  operation: "get"
})
```

**Usage Example (Set Property):**
```javascript
obsidian_manage_frontmatter({
  filePath: "Projects/Website Redesign.md",
  operation: "set",
  key: "status",
  value: "completed"
})
```

**Usage Example (Delete Property):**
```javascript
obsidian_manage_frontmatter({
  filePath: "Projects/Website Redesign.md",
  operation: "delete",
  key: "archived"
})
```

**Error Codes:**
- `404` - Note not found
- `403` - Permission denied
- `400` - Invalid YAML syntax
- `500` - Update error

---

### obsidian_manage_tags

**Description:** Add, remove, or list tags in a note (both frontmatter and inline).

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | string | Yes | Path to the note file |
| `operation` | string | Yes | Operation: `"add"`, `"remove"`, or `"list"` |
| `tags` | array | Conditional | Array of tag names (required for add/remove) |

**Return Value:**
```json
{
  "tags": ["project", "web", "design", "priority/high"],
  "frontmatterTags": ["project", "web"],
  "inlineTags": ["design", "priority/high"],
  "totalTags": 4
}
```

**Usage Example (List Tags):**
```javascript
obsidian_manage_tags({
  filePath: "Projects/Website Redesign.md",
  operation: "list"
})
```

**Usage Example (Add Tags):**
```javascript
obsidian_manage_tags({
  filePath: "Projects/Website Redesign.md",
  operation: "add",
  tags: ["completed", "2025-q1"]
})
```

**Usage Example (Remove Tags):**
```javascript
obsidian_manage_tags({
  filePath: "Projects/Website Redesign.md",
  operation: "remove",
  tags: ["in-progress"]
})
```

**Error Codes:**
- `404` - Note not found
- `403` - Permission denied
- `500` - Tag management error

---

### smart_connections_semantic_search

**Description:** Performs semantic search using Smart Connections plugin embeddings.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Natural language search query |
| `limit` | number | No | Maximum results to return (default: 10) |
| `threshold` | number | No | Minimum similarity score 0-1 (default: 0.5) |
| `excludePath` | string | No | Exclude notes from path |

**Return Value:**
```json
{
  "results": [
    {
      "filePath": "Atomic/Concepts/Spaced Repetition.md",
      "title": "Spaced Repetition",
      "similarity": 0.87,
      "excerpt": "A learning technique that involves reviewing information at increasing intervals..."
    },
    {
      "filePath": "Atomic/Models/Leitner System.md",
      "title": "Leitner System",
      "similarity": 0.82,
      "excerpt": "A flashcard-based method for spaced repetition learning..."
    }
  ],
  "totalResults": 15,
  "searchTime": 1250
}
```

**Usage Example:**
```javascript
smart_connections_semantic_search({
  query: "techniques for improving long-term memory retention",
  limit: 5,
  threshold: 0.7
})
```

**Requirements:**
- Smart Connections plugin installed
- Vault indexed (may take time for first index)
- Embedding model loaded (BGE-micro-v2 default)

**Performance:**
- Depends on vault size and embedding model
- Typically 1-3 seconds for semantic search
- Results cached for repeated queries

**Error Codes:**
- `503` - Smart Connections not available or not indexed
- `400` - Invalid query
- `500` - Search error

---

### smart_connections_get_similar_notes

**Description:** Finds notes semantically similar to a specific note.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `filePath` | string | Yes | Reference note path |
| `limit` | number | No | Maximum results to return (default: 10) |
| `threshold` | number | No | Minimum similarity score 0-1 (default: 0.5) |

**Return Value:**
```json
{
  "referenceNote": "Atomic/Concepts/Zettelkasten.md",
  "similarNotes": [
    {
      "filePath": "Atomic/Concepts/Evergreen Notes.md",
      "title": "Evergreen Notes",
      "similarity": 0.91
    },
    {
      "filePath": "Atomic/Models/PARA Method.md",
      "title": "PARA Method",
      "similarity": 0.84
    }
  ],
  "totalResults": 8
}
```

**Usage Example:**
```javascript
smart_connections_get_similar_notes({
  filePath: "Atomic/Concepts/Zettelkasten.md",
  limit: 5,
  threshold: 0.8
})
```

**Use Cases:**
- Discover related notes for bidirectional linking
- Find notes to merge or consolidate
- Suggest reading recommendations
- Identify knowledge clusters

**Error Codes:**
- `404` - Reference note not found
- `503` - Smart Connections not available
- `500` - Similarity calculation error

---

## Layer 3: Underlying REST API Endpoints

The Local REST API plugin provides HTTP endpoints that MCP servers use internally. You typically won't call these directly, but understanding them helps with troubleshooting.

### Base URL
```
http://localhost:27123  (HTTP)
https://localhost:27124 (HTTPS)
```

### Authentication
All requests require Authorization header:
```
Authorization: Bearer YOUR_API_KEY
```

### Vault Endpoints

#### `GET /vault/`
Lists all files in vault root directory.

**Response:**
```json
{
  "files": ["Daily/", "Projects/", "Inbox/", "README.md"]
}
```

#### `GET /vault/{path}`
Reads file content at specified path.

**Request:**
```
GET /vault/Projects/Website%20Redesign.md
```

**Response:**
```
# Website Redesign

Project notes...
```

#### `POST /vault/{path}`
Creates new file at specified path.

**Request Body:**
```
Content to write to new file
```

**Response:**
```json
{
  "success": true,
  "path": "Projects/New Note.md"
}
```

#### `PUT /vault/{path}`
Updates existing file (overwrites).

**Request Body:**
```
Updated content
```

**Response:**
```json
{
  "success": true,
  "path": "Projects/Website Redesign.md"
}
```

#### `PATCH /vault/{path}`
Inserts content at specific location (heading, line number, etc.).

**Request Body:**
```json
{
  "heading": "Progress",
  "content": "\n- Completed wireframes",
  "mode": "append"
}
```

**Response:**
```json
{
  "success": true,
  "bytesWritten": 45
}
```

#### `DELETE /vault/{path}`
Deletes file (moves to trash by default).

**Response:**
```json
{
  "success": true,
  "deleted": true
}
```

---

### Active File Endpoints

#### `GET /active/`
Returns path of currently active file in Obsidian.

**Response:**
```json
{
  "path": "Daily/2025-01-15.md"
}
```

#### `POST /active/`
Opens specified file as active file.

**Request Body:**
```json
{
  "path": "Projects/Website Redesign.md"
}
```

---

### Periodic Notes Endpoints

#### `GET /periodic/daily/{date}`
Gets daily note for specified date (YYYY-MM-DD).

**Request:**
```
GET /periodic/daily/2025-01-15
```

**Response:**
```
# Daily Note - 2025-01-15

## Tasks
- [ ] Review project timeline
```

#### `POST /periodic/daily/{date}`
Creates daily note for specified date.

**Request:**
```
POST /periodic/daily/2025-01-16
```

**Response:**
```json
{
  "success": true,
  "path": "Daily/2025-01-16.md",
  "created": true
}
```

---

## Agent Usage Matrix

This table shows which MCP tools are used by each Phase 1 agent:

| Tool | Inbox Triage | Structural Analysis | Semantic Linker | Query Interpreter | Quality Auditor |
|------|--------------|---------------------|-----------------|-------------------|-----------------|
| `obsidian_read_note` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `obsidian_create_note` | ✓ | ✓ | - | - | - |
| `obsidian_update_note` | - | ✓ | ✓ | - | - |
| `obsidian_delete_note` | - | - | - | - | - |
| `obsidian_search_notes` | - | - | - | ✓ | ✓ |
| `obsidian_list_notes` | ✓ | - | - | - | ✓ |
| `obsidian_manage_frontmatter` | ✓ | ✓ | - | - | ✓ |
| `obsidian_manage_tags` | ✓ | - | ✓ | - | ✓ |
| `smart_connections_semantic_search` | - | - | ✓ | ✓ | - |
| `smart_connections_get_similar_notes` | - | - | ✓ | - | - |

**Key:**
- ✓ = Used by agent
- \- = Not used by agent

---

## Rate Limits and Performance

### Rate Limiting

The Local REST API plugin **does not enforce rate limits** by default. However, be mindful of:

- **File System Limits:** Excessive writes may slow down Obsidian sync
- **Obsidian Performance:** Too many operations can impact Obsidian UI responsiveness
- **Smart Connections Indexing:** Semantic search during active indexing may be slower

**Recommended Limits:**
- Max 10 operations per second for sustained workloads
- Max 100 operations per second for burst workloads
- Allow 1-2 seconds between large batch operations

### Performance Benchmarks

Based on typical vault sizes:

| Operation | Small Vault (10-100 notes) | Medium Vault (100-1K notes) | Large Vault (1K-10K notes) |
|-----------|---------------------------|----------------------------|---------------------------|
| Read Note | < 10ms | < 20ms | < 50ms |
| Create Note | < 50ms | < 100ms | < 150ms |
| Update Note | < 50ms | < 100ms | < 150ms |
| Search (text) | < 50ms | < 500ms | < 2s |
| Semantic Search | < 500ms | < 2s | < 5s |
| List Notes (directory) | < 10ms | < 50ms | < 100ms |
| List Notes (recursive) | < 100ms | < 500ms | < 2s |

**Factors Affecting Performance:**
- Vault size and file count
- Note complexity (length, links, embeds)
- Smart Connections index status
- System resources (CPU, RAM, SSD speed)
- Obsidian plugins and extensions installed

---

## Error Handling

All MCP tools follow standardized error response format:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Note not found at path: Projects/Missing.md",
    "details": {
      "requestedPath": "Projects/Missing.md",
      "suggestion": "Check path spelling or use search to find note"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `NOT_FOUND` | 404 | Note or path doesn't exist | Verify path, use search to find note |
| `UNAUTHORIZED` | 401 | Invalid or missing API key | Check API key in environment/config |
| `FORBIDDEN` | 403 | Permission denied or path outside vault | Check file permissions, validate path |
| `CONFLICT` | 409 | File already exists or concurrent modification | Use unique filename or enable overwrite |
| `INVALID_REQUEST` | 400 | Invalid parameters or malformed request | Review parameter types and constraints |
| `SERVICE_UNAVAILABLE` | 503 | Obsidian not running or plugin disabled | Start Obsidian, enable plugins |
| `INTERNAL_ERROR` | 500 | Unexpected server error | Check logs, restart Obsidian, report issue |

### Error Handling Best Practices

1. **Always check for errors** before processing results
2. **Provide user-friendly messages** based on error codes
3. **Implement retry logic** for transient errors (503, 500)
4. **Log errors** with context for debugging
5. **Graceful degradation** - fail safely without data loss

---

## Security Considerations

### Path Validation

**Always validate paths to prevent directory traversal:**

```javascript
// ❌ UNSAFE - Allows directory traversal
filePath = userInput  // Could be "../../../etc/passwd"

// ✅ SAFE - Validates path is within vault
function validatePath(filePath) {
  // Remove leading/trailing slashes
  filePath = filePath.trim().replace(/^\/+|\/+$/g, '');

  // Check for directory traversal
  if (filePath.includes('..') || filePath.startsWith('/')) {
    throw new Error('Invalid path: directory traversal not allowed');
  }

  return filePath;
}
```

### Content Sanitization

**Sanitize content to prevent injection attacks:**

```javascript
// Escape YAML special characters in frontmatter
function escapeFrontmatter(value) {
  if (typeof value === 'string') {
    return value.replace(/[:"'`]/g, '\\$&');
  }
  return value;
}

// Remove potential script injection in markdown
function sanitizeMarkdown(content) {
  // Remove script tags
  content = content.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

  // Escape HTML entities
  content = content.replace(/</g, '&lt;').replace(/>/g, '&gt;');

  return content;
}
```

### API Key Protection

- **Never log API keys** in error messages or debug output
- **Use environment variables** instead of hardcoding
- **Rotate keys regularly** (every 90 days recommended)
- **Limit key scope** if plugin supports granular permissions

---

## Troubleshooting

### Tool Not Available

**Symptom:** `SERVICE_UNAVAILABLE` error when calling MCP tool

**Causes:**
- Obsidian not running
- Local REST API plugin disabled
- MCP server not started
- API key invalid

**Resolution:**
1. Verify Obsidian is running: Check application is open
2. Check plugin status: Settings → Community Plugins → Local REST API (enabled)
3. Test REST API directly: `curl -H "Authorization: Bearer KEY" http://localhost:27123/`
4. Restart MCP server: Quit and restart Claude Desktop

### Semantic Search Not Working

**Symptom:** `smart_connections_semantic_search` returns no results or error

**Causes:**
- Smart Connections not installed
- Vault not indexed
- Indexing in progress
- Embedding model not loaded

**Resolution:**
1. Install Smart Connections plugin
2. Wait for initial indexing to complete (check plugin status)
3. Rebuild index: Smart Connections settings → Rebuild Index
4. Check embedding model: Settings → Smart Connections → Model

### Slow Performance

**Symptom:** Operations take longer than expected

**Causes:**
- Large vault size
- Active Obsidian sync
- Insufficient system resources
- Semantic search indexing

**Resolution:**
1. Close unnecessary Obsidian plugins
2. Pause sync during batch operations
3. Use pagination for large result sets
4. Wait for Smart Connections indexing to complete

---

## Additional Resources

- **Local REST API Documentation:** https://github.com/coddingtonbear/obsidian-local-rest-api
- **MCP Tools Plugin:** https://github.com/jacksteamdev/obsidian-mcp-tools
- **Smart Connections:** https://github.com/brianpetro/obsidian-smart-connections
- **Model Context Protocol Spec:** https://modelcontextprotocol.io/
- **Interactive API Docs:** http://localhost:27123/ (when running)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Author:** BMAD Development Team

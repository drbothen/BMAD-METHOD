<!-- Powered by BMAD™ Core -->

# extract-metadata

Extract metadata (source URL, author, timestamp, context, tags) from captured content with security validation.

## Purpose

Parse captured content and source information to extract structured metadata for inbox notes. Applies security validation to prevent injection attacks and enforces field length limits.

## Prerequisites

- Content is provided (may contain URL, author, timestamps)
- Access to source-patterns.md for pattern matching
- Understanding of security requirements

## Inputs

- **content** (string, required): The captured content text
- **source** (string, optional): Source URL or description
- **raw_metadata** (object, optional): Any additional metadata from capture source
  - May include: page_title, meta_tags, html_snippet, clipboard_data

## Outputs

```yaml
metadata:
  source_url: "https://..." | null  # Validated URL or null
  author: "Name" | "Unknown"  # Author name or Unknown
  timestamp: "2025-11-04T15:30:00Z"  # ISO 8601 format
  context: "..." | null  # Surrounding context if available
  tags: []  # Array of extracted tags
  extraction_notes: []  # Warnings or notes about extraction
```

## Extraction Steps

### Step 1: Extract Source URL

**Priority order:**

1. Check `source` input parameter (if provided as URL)
2. Scan `content` for URLs using regex
3. Check `raw_metadata` for canonical URL or page URL
4. If none found: set to null

**URL Validation:**

- Must match safe URL regex: `^https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}(/.*)?$`
- Maximum length: 2048 characters
- Allowed protocols: `http://`, `https://`
- Blocked protocols: `file://`, `javascript:`, `data:`, `vbscript:`, `about:`

**Sanitization:**

- If dangerous protocol: Strip URL, set to null, log security event
- If malformed: Keep as plain text in source field (not as URL)
- Trim whitespace
- Remove trailing punctuation (., ,, ;, etc.) that may be part of sentence

**Example Patterns:**

```regex
URL in text: https?://[^\s]+
URL in markdown: \[.*?\]\((https?://[^\)]+)\)
URL in HTML: href="(https?://[^"]+)"
```

### Step 2: Extract Author

**Priority order by source type:**

**Twitter/X:**

- Pattern: `twitter.com/@?([a-zA-Z0-9_]+)/`
- Format: "@username"

**Medium:**

- Pattern: `medium.com/@([a-zA-Z0-9_]+)/`
- Try meta tag: `<meta property="article:author" content="...">`
- Format: "@username" or "Full Name"

**Academic (arXiv, PubMed):**

- Try meta tag: `<meta name="citation_author" content="...">`
- Format: "Last, F." or "Last, F., Last, F."

**News/Blogs:**

- Scan for byline: `By\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)`
- Try meta tag: `<meta name="author" content="...">`
- Format: "First Last"

**GitHub:**

- Pattern: `github.com/([a-zA-Z0-9-]+)/`
- Format: "@username"

**Books (from raw_metadata):**

- Check for book_author field
- Format: "Author Name"

**Generic patterns:**

```regex
By line: By\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
Author line: Author:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
Posted by: Posted by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
Written by: Written by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
```

**Normalization:**

- Remove titles: Dr., Prof., Mr., Ms., Mrs., PhD (unless critical to identity)
- Standardize to "First Last" or "@username" format
- Preserve hyphens in names
- Trim whitespace
- Maximum length: 256 characters

**Fallback:**

- If no author found: set to "Unknown"
- Never leave null or empty

### Step 3: Extract Timestamp

**Priority order:**

1. Check `raw_metadata.captured_at` if present
2. Use current timestamp (now)
3. Try to extract from content (date mentions)

**Format:**

- ISO 8601: `YYYY-MM-DDTHH:MM:SSZ` or `YYYY-MM-DDTHH:MM:SS+00:00`
- Always in UTC timezone

**Validation:**

- Must be valid ISO 8601 format
- If invalid: Use current timestamp as fallback
- Add note to extraction_notes: "Invalid source timestamp, using capture time"

### Step 4: Extract Context

**Definition:** Surrounding text that provides additional information about the capture.

**When to extract:**

- Partial captures (not full article)
- Highlights with surrounding paragraphs
- Quotes with preceding/following sentences

**Methods:**

1. Check `raw_metadata.context` if provided by clipper
2. Look for paragraph markers before/after main content
3. Extract surrounding sentences (1-2 before, 1-2 after)

**Limits:**

- Maximum: 5000 characters
- Truncate at sentence boundaries if exceeds limit
- If no context: set to null

**Security:**

- Escape HTML entities: `<`, `>`, `&`, `"`, `'`
- Strip `<script>`, `<iframe>`, `<object>`, `<embed>` tags
- Remove event handlers: `onclick`, `onerror`, etc.

### Step 5: Extract Tags

**Sources:**

1. Check `raw_metadata.tags` if provided
2. Scan content for hashtags: `#tag`
3. Check source URL domain as default tag

**Normalization:**

- Convert to lowercase
- Remove # symbol: `#productivity` → `productivity`
- Replace spaces with hyphens: `note taking` → `note-taking`
- Limit to 50 characters per tag
- Maximum 10 tags

**Default tags:**

- Always add source domain as tag (e.g., "medium", "arxiv", "twitter")
- Add content type after classification

### Step 6: Security Validation

Apply to ALL extracted fields:

**URL Safety:**

- Block dangerous protocols
- Validate format
- Log rejected URLs

**XSS Prevention:**

- Escape HTML entities in all text fields
- Strip script tags from context
- Remove event handlers

**Injection Prevention:**

- Parameterize any database queries (for Neo4j)
- Never concatenate user input into queries
- Validate input formats

**Length Limits:**

- source_url: 2048 characters
- author: 256 characters
- context: 5000 characters
- tags: 50 characters each, 10 max

**Content Filtering:**

- Scan for malicious patterns
- Reject obvious XSS attempts
- Log security events for audit

## Platform-Specific Logic

### Twitter/X

**URL:** `https://twitter.com/username/status/123456789`

**Extract:**

- Author: `@username` from URL
- Source URL: Full tweet URL
- Tags: Add "twitter"

### Medium

**URL:** `https://medium.com/@username/article-title-abc123`

**Extract:**

- Author: `@username` from URL or meta tag
- Try meta: `<meta property="article:author" content="...">`
- Tags: Extract from article tags if available

### arXiv

**URL:** `https://arxiv.org/abs/2103.12345`

**Extract:**

- Author: From `<meta name="citation_author">` (may be multiple)
- Try abstract for context
- Tags: Add "arxiv", "academic"

### Substack

**URL:** `https://example.substack.com/p/article-title`

**Extract:**

- Author: Newsletter name from subdomain
- Try meta: `<meta name="author" content="...">`
- Tags: Add "substack", newsletter name

### GitHub

**URL:** `https://github.com/owner/repo`

**Extract:**

- Author: `@owner` from URL
- Tags: Add "github", programming language if detected

## Error Handling

### URL Extraction Failed

- Set source_url to null
- Add note: "No valid URL found"
- Continue processing

### Author Extraction Failed

- Set author to "Unknown"
- Add note: "Author could not be extracted"
- Continue processing (not blocking)

### Invalid Timestamp

- Use current timestamp
- Add note: "Invalid timestamp, using capture time"
- Continue processing

### Context Too Large

- Truncate at 5000 characters
- Truncate at sentence boundary
- Add note: "Context truncated"

### Security Validation Failed

- Strip dangerous content
- Log security event
- Add note: "Content sanitized for security"
- Continue with sanitized content

## Output Example

```yaml
metadata:
  source_url: 'https://twitter.com/naval/status/1234567890'
  author: '@naval'
  timestamp: '2025-11-04T15:30:00Z'
  context: null
  tags: ['twitter', 'philosophy', 'startups']
  extraction_notes: []
```

## Output Example with Issues

```yaml
metadata:
  source_url: null
  author: 'Unknown'
  timestamp: '2025-11-04T15:30:00Z'
  context: 'This is surrounding context that was captured with the highlight...'
  tags: ['article']
  extraction_notes:
    - 'No valid URL found in source or content'
    - 'Author could not be extracted from source'
    - 'Context truncated to 5000 characters'
```

## Reference Data

This task uses:

- `data/source-patterns.md` - URL patterns and author extraction rules
- `checklists/capture-quality-checklist.md` - Validation criteria

## Usage

Called by:

- `*capture` command - After user provides content
- `*process-inbox` command - For each unprocessed item
- `*batch-process` command - In bulk processing

Outputs feed into:

- `classify-content-type.md` - Classification uses metadata as context
- `create-inbox-note.md` - Metadata populates note frontmatter
- `create-capture-event.md` - Metadata stored in Neo4j if enabled

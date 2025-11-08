<!-- Powered by BMAD™ Core -->

# Capture: Extract Metadata

## Purpose

Extract structured metadata from captured content and source context to enable rich context preservation and better searchability.

## Inputs

- **raw_content** (String, required): Captured text to extract metadata from
- **source_context** (Object, optional): May contain URL, timestamp, author, title, and other contextual information

## Procedure

### Step 1: Validate Input

- Check that `raw_content` exists (not null or undefined)
- If content is empty string, proceed with metadata extraction (metadata may still be extractable from source_context)
- Sanitize content to prevent injection attacks:
  - Escape YAML special characters: `:`, `#`, `-`, `[`, `]`, `{`, `}`, `|`, `>`
  - Strip or escape HTML entities
- Initialize metadata object with default values

### Step 2: Parse Source URL

**Priority 1:** Extract from `source_context.url` if present

**Priority 2:** Extract URLs from `raw_content` if `source_context.url` not provided:

- Use URL pattern matching: `https?://[^\s]+`
- Extract first valid URL found in content
- If multiple URLs, prefer the first one

**Priority 3:** Default to "Unknown" if no URL found

Store extracted URL for validation in Step 3.

### Step 3: Validate and Sanitize URL

Apply URL validation algorithm:

1. **Check URL format:**
   - Must have valid scheme (http://, https://, ftp://)
   - Must have valid domain structure
   - Use URL parsing to validate structure

2. **Block malicious schemes:**
   - ❌ REJECT: `javascript:`
   - ❌ REJECT: `data:`
   - ❌ REJECT: `file:`
   - ❌ REJECT: `vbscript:`
   - ✅ ALLOW: `http:`, `https:`, `ftp:`

3. **Validate domain:**
   - Check for localhost/127.0.0.1 (block unless explicitly allowed in config)
   - Validate domain has valid TLD
   - No malformed domains (e.g., `..`, `//`)

4. **Sanitize query parameters (optional):**
   - Remove tracking parameters: `utm_*`, `fbclid`, `gclid`, etc. (if configured)
   - Preserve functional query parameters

5. **Strip authentication tokens:**
   - Remove auth tokens from URLs: `?token=`, `?auth=`, `?key=`
   - Prevent credential exposure in stored metadata

6. **Result:**
   - If validation passes: Use sanitized URL
   - If validation fails: Set to "Unknown" and log warning

### Step 4: Extract Author

**Priority 1:** Use `source_context.author` if present and non-empty

**Priority 2:** Parse from `raw_content` using byline patterns:

- Look for "by [Author Name]" pattern (case-insensitive)
- Look for "author: [Author Name]" pattern
- Look for "-- [Author Name]" or "- [Author Name]" at end
- Look for "[Author Name] writes:" or "[Author Name] says:"

**Priority 3:** Parse from `source_context.title` if it contains author info:

- Pattern: "Title by Author" or "Title - Author"

**Priority 4:** Default to "Unknown" if no author found

**Sanitization:**

- Trim whitespace
- Capitalize first letter of each word (proper noun formatting)
- Limit to 100 characters maximum
- Escape YAML special characters

### Step 5: Extract Title

**Priority 1:** Use `source_context.title` if present and non-empty

**Priority 2:** Parse from `raw_content` using heading patterns:

- Look for markdown heading: `# Heading Text` (first heading)
- Look for first line if it's short (< 100 chars) and not a sentence
- Look for HTML `<title>` tags if content contains HTML

**Priority 3:** Auto-generate from first 50 characters:

- Take first 50 chars of `raw_content`
- Break at word boundary (don't cut mid-word)
- Append "..." if truncated
- Example: "Deep work is the ability to focus without distr..."

**Sanitization:**

- Trim whitespace
- Remove markdown formatting: `#`, `*`, `_`, `[`, `]`
- Limit to 200 characters maximum
- Escape YAML special characters

### Step 6: Capture Timestamp

**Priority 1:** Use `source_context.timestamp` if present and valid

**Priority 2:** Use current time as fallback

**Format requirements:**

- Must be ISO8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Must be in UTC timezone
- Example: `2025-11-06T10:30:00Z`

**Validation:**

- Parse timestamp to verify valid format
- If invalid format, use current time and log warning
- Ensure timezone is UTC (convert if necessary)

### Step 7: Extract Surrounding Context

**Purpose:** For reading highlights, capture paragraph before + highlighted text + paragraph after to preserve context

**Extraction logic:**

**If `source_context.surrounding_context` exists:**

- Use provided value directly
- Sanitize for YAML injection
- Limit to 2000 characters

**If `source_context.highlight_range` exists:**

- Extract text before highlight (up to 500 chars)
- Extract highlighted text
- Extract text after highlight (up to 500 chars)
- Format: `...before... [HIGHLIGHTED TEXT] ...after...`

**If neither exists:**

- Set to empty string (not applicable for quick captures)

**Sanitization:**

- Trim excessive whitespace
- Preserve paragraph breaks (convert to `\n\n`)
- Escape YAML special characters
- Limit total length to 2000 characters

### Step 8: Sanitize All Extracted Fields

Apply sanitization to all metadata fields:

**YAML escaping:**

- Escape special characters that break YAML: `:`, `#`, `-`, `[`, `]`, `{`, `}`, `|`, `>`
- Quote string values containing special chars
- Handle multiline strings properly (use `|` or `>` indicators)

**HTML escaping:**

- Escape entities: `&lt;`, `&gt;`, `&amp;`, `&quot;`
- Strip dangerous HTML tags: `<script>`, `<iframe>`, `<object>`

**Character encoding:**

- Ensure UTF-8 encoding
- Handle emoji, international characters properly
- No encoding-based exploits

### Step 9: Validate Extracted Metadata

Verify metadata object has required structure:

**Required fields (must be present, can be defaults):**

- `source_url`: String (can be "Unknown")
- `author`: String (can be "Unknown")
- `title`: String (must be non-empty, auto-generated if needed)
- `timestamp`: String (must be valid ISO8601)

**Optional fields:**

- `surrounding_context`: String (can be empty)

**Validation checks:**

- All required fields present: ✓
- `timestamp` is valid ISO8601: ✓
- `title` is non-empty: ✓
- All fields properly sanitized: ✓
- Total metadata size < 1MB: ✓

**If validation fails:**

- Log validation errors
- Return error with details

### Step 10: Return Structured Metadata Object

Return complete metadata object with all fields:

```json
{
  "source_url": "https://example.com/article",
  "author": "John Doe",
  "title": "Understanding Deep Work",
  "timestamp": "2025-11-06T10:30:00Z",
  "surrounding_context": ""
}
```

## Outputs

- **source_url** (String): Validated URL or "Unknown" if no valid URL found
- **author** (String): Extracted author name or "Unknown" if not found
- **title** (String): Extracted or auto-generated title (always non-empty)
- **timestamp** (String): ISO8601 formatted timestamp in UTC (e.g., "2025-11-06T10:30:00Z")
- **surrounding_context** (String): Context surrounding highlighted text, or empty string for quick captures

## Examples

### Example 1: Web Article with Full Metadata

**Input:**

```json
{
  "raw_content": "Deep work is the ability to focus without distraction on a cognitively demanding task.",
  "source_context": {
    "url": "https://example.com/deep-work-guide",
    "author": "Cal Newport",
    "title": "The Deep Work Guide",
    "timestamp": "2025-11-06T10:30:00Z"
  }
}
```

**Extraction Process:**

1. source_url: From source_context.url → "https://example.com/deep-work-guide"
2. Validate URL: https:// scheme → VALID ✓
3. author: From source_context.author → "Cal Newport"
4. title: From source_context.title → "The Deep Work Guide"
5. timestamp: From source_context.timestamp → "2025-11-06T10:30:00Z" (valid ISO8601)
6. surrounding_context: Not provided → ""

**Output:**

```json
{
  "source_url": "https://example.com/deep-work-guide",
  "author": "Cal Newport",
  "title": "The Deep Work Guide",
  "timestamp": "2025-11-06T10:30:00Z",
  "surrounding_context": ""
}
```

### Example 2: Reading Highlight with Surrounding Context

**Input:**

```json
{
  "raw_content": "Deep work is the ability to focus without distraction on a cognitively demanding task.",
  "source_context": {
    "url": "https://example.com/deep-work",
    "surrounding_context": "In today's fast-paced world, the ability to concentrate is becoming increasingly rare. Deep work is the ability to focus without distraction on a cognitively demanding task. This skill is crucial for producing high-quality output in less time."
  }
}
```

**Extraction Process:**

1. source_url: From source_context.url → "https://example.com/deep-work"
2. Validate URL: VALID ✓
3. author: Not in source_context, not in content → "Unknown"
4. title: Not in source_context, extract from first line → "Deep work is the ability to focus without distr..."
5. timestamp: Not provided → Use current time → "2025-11-06T14:22:30Z"
6. surrounding_context: From source_context.surrounding_context → Provided value (sanitized)

**Output:**

```json
{
  "source_url": "https://example.com/deep-work",
  "author": "Unknown",
  "title": "Deep work is the ability to focus without distr...",
  "timestamp": "2025-11-06T14:22:30Z",
  "surrounding_context": "In today's fast-paced world, the ability to concentrate is becoming increasingly rare. Deep work is the ability to focus without distraction on a cognitively demanding task. This skill is crucial for producing high-quality output in less time."
}
```

### Example 3: Quick Note with Minimal Metadata

**Input:**

```json
{
  "raw_content": "Spaced repetition works because it aligns with the spacing effect - our brain remembers better when learning is distributed over time.",
  "source_context": null
}
```

**Extraction Process:**

1. source_url: No source_context, no URLs in content → "Unknown"
2. author: No source_context, no byline → "Unknown"
3. title: No source_context, auto-generate from first 50 chars → "Spaced repetition works because it aligns with th..."
4. timestamp: No source_context → Use current time → "2025-11-06T14:25:15Z"
5. surrounding_context: No source_context → ""

**Output:**

```json
{
  "source_url": "Unknown",
  "author": "Unknown",
  "title": "Spaced repetition works because it aligns with th...",
  "timestamp": "2025-11-06T14:25:15Z",
  "surrounding_context": ""
}
```

### Example 4: Social Media Capture

**Input:**

```json
{
  "raw_content": "The best productivity system is the one you'll actually use consistently. Don't get lost in the tools. by @productivityguru on Twitter",
  "source_context": {
    "url": "https://twitter.com/productivityguru/status/123456789",
    "timestamp": "2025-11-06T09:15:00Z"
  }
}
```

**Extraction Process:**

1. source_url: From source_context.url → "https://twitter.com/productivityguru/status/123456789"
2. Validate URL: VALID ✓
3. author: Not in source_context, parse from content "by @productivityguru" → "Productivityguru"
4. title: Not in source_context, extract first line (< 100 chars) → "The best productivity system is the one you'll actually use consistently. Don't get lost in the tools."
5. timestamp: From source_context.timestamp → "2025-11-06T09:15:00Z"
6. surrounding_context: Not provided → ""

**Output:**

```json
{
  "source_url": "https://twitter.com/productivityguru/status/123456789",
  "author": "Productivityguru",
  "title": "The best productivity system is the one you'll actually use consistently. Don't get lost in the tools.",
  "timestamp": "2025-11-06T09:15:00Z",
  "surrounding_context": ""
}
```

## URL Validation Algorithm

### Step 1: Check URL Format

- Parse URL using standard URL parsing library
- Verify structure: `scheme://domain/path?query#fragment`
- Check for valid scheme and domain
- If parsing fails → INVALID

### Step 2: Block Malicious Schemes

Reject URLs with dangerous schemes:

```
❌ BLOCKED SCHEMES:
- javascript:  (JavaScript execution)
- data:        (Data URLs can contain executable code)
- file:        (Local file access)
- vbscript:    (VBScript execution)
- about:       (Internal browser pages)
```

```
✅ ALLOWED SCHEMES:
- http:
- https:
- ftp:
```

### Step 3: Validate Domain

- Check domain is not empty
- Validate domain has valid TLD (e.g., .com, .org, .edu)
- Block localhost unless explicitly allowed:
  - ❌ `localhost`
  - ❌ `127.0.0.1`
  - ❌ `0.0.0.0`
  - ❌ `::1` (IPv6 localhost)
- Block internal/private IPs unless allowed in config:
  - ❌ `192.168.*.*`
  - ❌ `10.*.*.*`
  - ❌ `172.16.*.*` to `172.31.*.*`

### Step 4: Sanitize Query Parameters

**Optional tracking parameter removal (if configured):**

- Remove `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`
- Remove `fbclid` (Facebook click ID)
- Remove `gclid` (Google click ID)
- Remove `msclkid` (Microsoft click ID)

**Preserve functional parameters:**

- Keep query parameters needed for content access
- Keep parameters that affect page content

### Step 5: Strip Authentication Tokens

Remove sensitive parameters that contain credentials:

- Remove `?token=*`
- Remove `?auth=*`
- Remove `?key=*`
- Remove `?apikey=*`
- Remove `?password=*`

**Purpose:** Prevent credential exposure in stored metadata

### Step 6: Return Validated URL

- If all validations pass: Return sanitized URL
- If any validation fails: Return "Unknown" and log warning with reason

**Example validations:**

```
✅ VALID: "https://example.com/article"
✅ VALID: "https://example.com/path?page=2"
✅ VALID: "ftp://files.example.com/document.pdf"
❌ INVALID: "javascript:alert('xss')" → Blocked scheme
❌ INVALID: "file:///etc/passwd" → Blocked scheme
❌ INVALID: "http://localhost/admin" → Localhost blocked
❌ INVALID: "https://192.168.1.1/config" → Private IP blocked
```

## Error Handling

### Error 1: Missing source_context (Use Defaults)

**Condition:** `source_context` is null or undefined

**Response:** Continue processing with defaults

- source_url: Extract from content or "Unknown"
- author: "Unknown"
- title: Auto-generate from content
- timestamp: Current time
- Log info: "No source context provided, using defaults"

**Blocking:** NO (graceful degradation)

### Error 2: Malformed URL

**Condition:** URL fails validation (malicious scheme, invalid format)

**Response:**

- Set source_url to "Unknown"
- Log warning: "Invalid URL detected: [reason], set to 'Unknown'"
- Continue processing other metadata
- Return successful metadata object

**Blocking:** NO (graceful degradation)

### Error 3: Parse Failures

**Condition:** Unable to parse author, title, or other fields from content

**Response:**

- Use fallback values:
  - author: "Unknown"
  - title: First 50 chars of content
- Log info: "Field extraction failed, using fallback values"
- Continue processing

**Blocking:** NO (use defaults)

### Error 4: Content Too Large

**Condition:** `raw_content` exceeds 10MB or metadata exceeds 1MB

**Response:**

- Truncate content to 10MB: Log warning: "Content truncated to 10MB limit"
- Truncate metadata fields to stay under 1MB total
- Continue processing with truncated content

**Blocking:** NO (truncate and continue)

### Error 5: Invalid Timestamp Format

**Condition:** `source_context.timestamp` is not valid ISO8601 format

**Response:**

- Use current time as fallback
- Log warning: "Invalid timestamp format '[value]', using current time"
- Continue processing

**Blocking:** NO (use current time)

### Error 6: YAML Injection Attempt

**Condition:** Metadata fields contain unescaped YAML special characters

**Response:**

- Apply YAML escaping to all fields
- Quote string values containing special chars
- Log warning: "YAML special characters detected and escaped"
- Continue processing

**Blocking:** NO (sanitize and continue)

## Security

### URL Validation (Malicious URL Prevention)

- **Block malicious schemes:** javascript:, data:, file:, vbscript:
- **Validate domain format:** No malformed domains, valid TLD required
- **Block localhost access:** Prevent localhost, 127.0.0.1 unless explicitly allowed
- **Block private IPs:** Prevent 192.168._._, 10._._._, 172.16-31._.\* unless allowed
- **Strip auth tokens:** Remove ?token=, ?auth=, ?key= parameters

### Metadata Sanitization (Injection Prevention)

- **YAML escaping:** Escape `:`, `#`, `-`, `[`, `]`, `{`, `}`, `|`, `>`
- **Quote values:** Quote strings containing special characters
- **HTML escaping:** Escape `<`, `>`, `&`, `"` to prevent HTML injection
- **Strip dangerous tags:** Remove `<script>`, `<iframe>`, `<object>`, `<embed>`

### Content Size Limits (DoS Prevention)

- **Max content size:** 10MB per capture
- **Max metadata size:** 1MB total for all fields
- **Enforcement:** Truncate oversized content, log warning
- **Prevent memory exhaustion:** Check sizes before processing

### Character Encoding

- **UTF-8 support:** Handle international characters properly
- **Emoji support:** Preserve emoji and special Unicode characters
- **No encoding exploits:** Validate encoding, prevent double-encoding attacks

### Credential Protection

- **Strip auth tokens from URLs:** Prevent credential exposure in stored metadata
- **No sensitive data in logs:** Sanitize logs to remove tokens, passwords
- **Secure defaults:** Default to "Unknown" rather than exposing sensitive info

## Performance Target

**Target execution time:** < 1 second per metadata extraction

**Performance considerations:**

- Simple pattern matching (no complex NLP)
- Minimal regex usage (use string operations where possible)
- No external API calls
- Efficient URL parsing (use standard library)
- Memory-efficient field extraction

**Monitoring:**

- Log extraction time for each execution
- Alert if average time exceeds target
- Identify slow operations for optimization

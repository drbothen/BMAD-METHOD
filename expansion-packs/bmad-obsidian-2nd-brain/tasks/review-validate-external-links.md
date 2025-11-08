<!-- Powered by BMAD™ Core -->

# Review: Validate External Links

## Purpose

Validate external links in Obsidian notes by checking HTTP status codes, identifying broken links (4xx), redirects (3xx), and timeouts. Implements SSRF prevention, rate limiting, and credential protection to safely validate external references without security risks.

## Inputs

- **note_paths** (Array<String>, optional): Specific note paths to check (default: all notes in vault)
- **max_links** (Integer, optional, default: 50): Maximum number of links to validate per execution
- **rate_limit** (Integer, optional, default: 5): Maximum requests per second (1-10 allowed)

## Outputs

- **validation_results** (Array<Object>): Complete validation results for all tested links
  - `note_path` (String): Path to note containing the link
  - `url` (String): The validated URL
  - `status_code` (Integer): HTTP status code (200, 404, etc.)
  - `classification` (String): success/broken/redirect/timeout/blocked
  - `response_time` (Float): Response time in milliseconds
  - `reason` (String, optional): Explanation for blocked/timeout/error
- **broken_links** (Array<Object>): Links returning 4xx/5xx status codes
- **redirects** (Array<Object>): Links returning 3xx status codes with Location header
- **timeouts** (Array<Object>): Links that exceeded 5-second timeout
- **metrics** (Object): Aggregated link health statistics
  - `total_links` (Integer): Total links validated
  - `broken_count` (Integer): Count of broken links
  - `redirect_count` (Integer): Count of redirects
  - `timeout_count` (Integer): Count of timeouts
  - `success_count` (Integer): Count of successful validations
  - `success_rate` (Float): Percentage of successful validations (0.0-1.0)

## Sequential Procedure

### Step 1: Validate Inputs

- Verify `note_paths` is an array (if provided) or null/undefined for "all notes"
- Confirm `max_links` > 0 and ≤ 1000 (prevent abuse)
- Validate `rate_limit` is between 1 and 10 (inclusive)
- If validation fails, return error with specific issue
- Continue to Step 2 if all inputs valid

### Step 2: Get Notes Using Obsidian MCP Tool

- If `note_paths` is not provided or null:
  - Call `obsidian.list_notes()` to get all notes in vault
- If `note_paths` is provided:
  - For each path in array:
    - Call `obsidian.read_note(path)` to get note content
- Handle MCP errors gracefully (return error if unavailable)
- Store notes array for processing

### Step 3: Initialize Results Arrays

- Create empty arrays for categorizing results:
  - `broken`: Links with 4xx/5xx status codes
  - `redirects`: Links with 3xx status codes
  - `timeouts`: Links that timed out
  - `success`: Links with 2xx status codes
  - `blocked`: Links blocked by security filters
- Initialize `validation_results` as empty array

### Step 4: For Each Note, Read Content

- For each note in notes array:
  - Read note content (use cached content if already loaded in Step 2)
  - Store note_path for reference in results
  - If note content cannot be read, log warning and skip
  - Continue to next note

### Step 5: Extract URLs Using Regex

- Define URL extraction patterns:
  - **Markdown links**: `\[([^\]]+)\]\((https?://[^\)]+)\)`
  - **Plain URLs**: `https?://[^\s\)\]>]+`
- For each note content:
  - Extract all markdown links: `[text](url)` → capture URL
  - Extract all plain URLs in text
  - Store each URL with context: `{note_path, url, context_text}`
- Deduplicate URLs (same URL in same note only counted once)

### Step 6: Validate URL Format and Filter Malicious Schemes

- For each extracted URL:
  - Parse URL using URL parser
  - Check protocol/scheme:
    - **Allowed**: `http://`, `https://`
    - **Blocked**: `javascript:`, `data:`, `file://`, `ftp://`, `vbscript:`, `about:`
  - If scheme is blocked:
    - Add to `blocked` array with reason: "Invalid protocol"
    - Remove from validation queue
  - If URL is malformed (parsing fails):
    - Add to `broken` array with reason: "Malformed URL"
    - Remove from validation queue

### Step 7: Apply SSRF Prevention (Block Private IPs)

- For each URL passing Step 6:
  - Extract hostname from URL
  - Check if hostname is private IP or localhost:
    - **Block**: `127.0.0.0/8` (loopback)
    - **Block**: `10.0.0.0/8` (private Class A)
    - **Block**: `192.168.0.0/16` (private Class C)
    - **Block**: `172.16.0.0/12` (private Class B)
    - **Block**: `169.254.0.0/16` (link-local)
    - **Block**: `localhost`, `0.0.0.0`
  - If hostname is private:
    - Add to `blocked` array with reason: "Private IP (SSRF prevention)"
    - Remove from validation queue
  - Continue to Step 8 with remaining URLs

### Step 8: Strip Credentials from URLs Before Testing

- For each URL in validation queue:
  - Parse URL to extract components
  - Check for embedded credentials: `https://user:pass@example.com`
  - If credentials present:
    - Remove username and password from URL
    - Create sanitized URL: `https://example.com` (without credentials)
    - Use sanitized URL for all further processing and logging
    - **Never log credentials** in validation results
  - Store sanitized URL for validation

### Step 9: Batch URLs into Groups of rate_limit Size

- Split URLs into batches:
  - Batch size = `rate_limit` (e.g., 5 URLs per batch if rate_limit=5)
  - Total batches = ceil(total_urls / rate_limit)
- Apply `max_links` limit:
  - Only process first `max_links` URLs
  - Remaining URLs not validated (logged as "skipped due to max_links limit")
- Store batches array for sequential processing

### Step 10: For Each Batch, Send HTTP HEAD Requests with 5s Timeout

- For each batch of URLs:
  - For each URL in batch:
    - Send HTTP HEAD request (lightweight, doesn't download body)
    - Set timeout: 5 seconds maximum
    - Set headers: `User-Agent: Obsidian-Link-Validator/1.0`
    - **Do not follow redirects automatically** (use allow_redirects=false)
    - Record start time and end time for response_time calculation
  - Process all URLs in batch concurrently (if possible) or sequentially

### Step 11: Classify Responses by Status Code

- For each URL response:
  - **2xx (Success)**:
    - Classification: "success"
    - Add to `success` array
  - **3xx (Redirect)**:
    - Classification: "redirect"
    - Extract `Location` header from response
    - Add to `redirects` array with new location
  - **4xx (Client Error)**:
    - Classification: "broken"
    - Common codes: 404 (Not Found), 403 (Forbidden), 401 (Unauthorized)
    - Add to `broken` array
  - **5xx (Server Error)**:
    - Classification: "broken"
    - Common codes: 500 (Internal Server Error), 503 (Service Unavailable)
    - Add to `broken` array

### Step 12: Record Results with Metadata

- For each validated URL:
  - Create result object:
    ```json
    {
      "note_path": "path/to/note.md",
      "url": "https://example.com",
      "status_code": 200,
      "classification": "success",
      "response_time": 245.3,
      "reason": null
    }
    ```
  - Add to `validation_results` array
  - Also add to appropriate category array (broken/redirects/timeouts/success/blocked)

### Step 13: Wait 1 Second Between Batches (Rate Limiting)

- After processing each batch:
  - Wait for 1 second before starting next batch
  - This ensures rate limit is respected (e.g., 5 req/sec max)
  - Log batch completion: "Batch X/Y complete, waiting 1 second..."
- Skip wait after final batch

### Step 14: Calculate Metrics

- After all batches processed:
  - Count totals:
    - `total_links`: Total URLs validated (excluding skipped)
    - `broken_count`: Length of `broken` array
    - `redirect_count`: Length of `redirects` array
    - `timeout_count`: Length of `timeouts` array
    - `success_count`: Length of `success` array
  - Calculate success rate:
    - `success_rate = success_count / total_links` (if total_links > 0, else 0)
  - Store metrics object

### Step 15: Return Structured Validation Results

- Return object containing:
  - `validation_results`: Full array of all validation results
  - `broken_links`: Array of broken links (4xx/5xx)
  - `redirects`: Array of redirect links (3xx)
  - `timeouts`: Array of timeout links
  - `metrics`: Aggregated statistics
  - `success`: true/false status
- Include timestamp of validation execution

## Security Considerations

### SSRF Prevention

- **Block private IP ranges**: Prevent requests to internal network resources
  - `127.0.0.0/8` - Loopback addresses
  - `10.0.0.0/8` - Private Class A
  - `172.16.0.0/12` - Private Class B
  - `192.168.0.0/16` - Private Class C
  - `169.254.0.0/16` - Link-local addresses
- **Block localhost**: `localhost`, `0.0.0.0`
- **Allowlist for testing**: If private IPs needed for dev/test environments, use explicit allowlist

### Protocol Validation

- **Only allow HTTP/HTTPS**: Block dangerous protocols
  - ❌ `javascript:alert('XSS')` - XSS attack vector
  - ❌ `data:text/html,<script>...` - Data URI exploit
  - ❌ `file:///etc/passwd` - Local file access
  - ❌ `vbscript:`, `about:` - Browser exploits
  - ✅ `http://example.com` - Allowed
  - ✅ `https://example.com` - Allowed

### Credential Protection

- **Strip embedded credentials**: Remove `username:password` from URLs
  - Input: `https://admin:secret@example.com/api`
  - Sanitized: `https://example.com/api`
- **Never log credentials**: Ensure credentials not stored in validation results or logs
- **Security warning**: Warn users if credentials detected (recommend using API keys instead)

### Rate Limiting

- **Enforce 5 requests per second maximum**: Prevent abuse of external services
- **1-second delay between batches**: Ensures rate limit compliance
- **Max requests per execution**: Default 50 links (configurable up to 1000)
- **Purpose**: Prevent being blocked by target servers, avoid DoS accusations

### Timeout Enforcement

- **5-second maximum per request**: Prevent hanging on slow/unresponsive servers
- **Connection timeout**: 3 seconds for initial connection
- **Read timeout**: 5 seconds total for response
- **Abort on timeout**: Don't retry timed-out requests automatically

## Performance Targets

- **50 links with rate limiting (5 req/sec)**: < 15 seconds total
  - 50 links / 5 per batch = 10 batches
  - 10 batches × 1 second wait = 10 seconds
  - Plus ~2-5 seconds for actual requests
  - Total: ~12-15 seconds

**Breakdown:**

- URL extraction: ~0.5 seconds for 50 notes
- Security filtering: ~0.2 seconds for 50 URLs
- HTTP requests: ~1-5 seconds (depends on server response times)
- Rate limiting waits: ~10 seconds for 50 links at 5 req/sec
- Result processing: ~0.3 seconds

**Optimization strategies:**

- Use concurrent requests within batches (up to rate_limit simultaneous)
- Cache DNS lookups to speed up repeated domains
- Use HTTP HEAD instead of GET (lighter weight)
- Skip validation for previously validated URLs (cache results for session)

## Error Handling

### Error 1: Invalid URLs

**Condition:** URL cannot be parsed or is malformed

**Response:**

```json
{
  "note_path": "notes/example.md",
  "url": "htp://broken-url",
  "status_code": null,
  "classification": "broken",
  "response_time": null,
  "reason": "Malformed URL"
}
```

### Error 2: Connection Failures

**Condition:** Network error, DNS resolution failure, connection refused

**Response:**

```json
{
  "note_path": "notes/example.md",
  "url": "https://nonexistent-domain-xyz123.com",
  "status_code": null,
  "classification": "broken",
  "response_time": null,
  "reason": "DNS resolution failed"
}
```

### Error 3: Timeout

**Condition:** Server doesn't respond within 5 seconds

**Response:**

```json
{
  "note_path": "notes/example.md",
  "url": "https://very-slow-server.com",
  "status_code": null,
  "classification": "timeout",
  "response_time": 5000,
  "reason": "Request timeout (>5 seconds)"
}
```

### Error 4: MCP Unavailable

**Condition:** Obsidian MCP server not accessible

**Response:**

```json
{
  "success": false,
  "error": "Obsidian MCP server unavailable",
  "remediation": "Verify MCP server is running and configured"
}
```

### Error 5: No Links Found

**Condition:** No external links found in specified notes

**Response:**

```json
{
  "success": true,
  "validation_results": [],
  "broken_links": [],
  "redirects": [],
  "timeouts": [],
  "metrics": {
    "total_links": 0,
    "broken_count": 0,
    "redirect_count": 0,
    "timeout_count": 0,
    "success_count": 0,
    "success_rate": 0.0
  },
  "message": "No external links found in specified notes"
}
```

### Error 6: Private IP Blocked (SSRF Prevention)

**Condition:** URL targets private IP or localhost

**Response:**

```json
{
  "note_path": "notes/example.md",
  "url": "http://192.168.1.1/admin",
  "status_code": null,
  "classification": "blocked",
  "response_time": null,
  "reason": "Private IP (SSRF prevention)"
}
```

### Error 7: Invalid Protocol

**Condition:** URL uses dangerous protocol (javascript:, file:, etc.)

**Response:**

```json
{
  "note_path": "notes/example.md",
  "url": "javascript:alert('XSS')",
  "status_code": null,
  "classification": "blocked",
  "response_time": null,
  "reason": "Invalid protocol (security risk)"
}
```

## Example Usage

### Example 1: Validate All Links (Default)

**Input:**

```yaml
note_paths: null # All notes
max_links: 50
rate_limit: 5
```

**Output:**

```json
{
  "success": true,
  "validation_results": [
    {
      "note_path": "research/web-sources.md",
      "url": "https://example.com",
      "status_code": 200,
      "classification": "success",
      "response_time": 123.5
    },
    {
      "note_path": "research/broken-ref.md",
      "url": "https://example.com/missing-page",
      "status_code": 404,
      "classification": "broken",
      "response_time": 89.2
    }
  ],
  "broken_links": [
    {
      "note_path": "research/broken-ref.md",
      "url": "https://example.com/missing-page",
      "status_code": 404,
      "classification": "broken",
      "response_time": 89.2
    }
  ],
  "redirects": [],
  "timeouts": [],
  "metrics": {
    "total_links": 50,
    "broken_count": 20,
    "redirect_count": 5,
    "timeout_count": 2,
    "success_count": 23,
    "success_rate": 0.46
  }
}
```

### Example 2: Specific Notes with SSRF Block

**Input:**

```yaml
note_paths: ['security/test-notes.md']
max_links: 10
rate_limit: 5
```

**Output:**

```json
{
  "success": true,
  "validation_results": [
    {
      "note_path": "security/test-notes.md",
      "url": "http://192.168.1.1",
      "status_code": null,
      "classification": "blocked",
      "response_time": null,
      "reason": "Private IP (SSRF prevention)"
    },
    {
      "note_path": "security/test-notes.md",
      "url": "https://public-site.com",
      "status_code": 200,
      "classification": "success",
      "response_time": 234.1
    }
  ],
  "broken_links": [],
  "redirects": [],
  "timeouts": [],
  "metrics": {
    "total_links": 2,
    "broken_count": 0,
    "redirect_count": 0,
    "timeout_count": 0,
    "success_count": 1,
    "success_rate": 0.5
  }
}
```

## Algorithm Pseudocode

```python
import re
import requests
from urllib.parse import urlparse
import time

def validate_external_links(note_paths=None, max_links=50, rate_limit=5):
    # Step 1: Validate inputs
    if max_links <= 0 or max_links > 1000:
        return {"success": False, "error": "max_links must be 1-1000"}
    if rate_limit < 1 or rate_limit > 10:
        return {"success": False, "error": "rate_limit must be 1-10"}

    # Step 2: Get notes
    if note_paths is None:
        notes = mcp.obsidian.list_notes()
    else:
        notes = [mcp.obsidian.read_note(path) for path in note_paths]

    # Step 3: Initialize results
    results = {'broken': [], 'redirects': [], 'timeouts': [], 'success': [], 'blocked': []}
    validation_results = []

    # Step 4-5: Extract URLs from all notes
    url_pattern = r'https?://[^\s\)\]>]+'
    all_links = []

    for note in notes:
        content = note.content
        # Extract markdown links: [text](url)
        markdown_links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', content)
        # Extract plain URLs
        plain_links = re.findall(url_pattern, content)

        for text, url in markdown_links:
            all_links.append({'note_path': note.path, 'url': url, 'context': text})

        for url in plain_links:
            all_links.append({'note_path': note.path, 'url': url, 'context': None})

    # Apply max_links limit
    links_to_test = all_links[:max_links]

    # Step 6-8: Filter and sanitize URLs
    safe_links = []
    for link in links_to_test:
        url = link['url']

        # Step 6: Protocol validation
        if not url.startswith(('http://', 'https://')):
            results['blocked'].append({**link, 'classification': 'blocked', 'reason': 'Invalid protocol'})
            continue

        # Step 7: SSRF prevention
        if is_private_ip(url):
            results['blocked'].append({**link, 'classification': 'blocked', 'reason': 'Private IP (SSRF prevention)'})
            continue

        # Step 8: Strip credentials
        safe_url = strip_credentials(url)
        link['url'] = safe_url
        safe_links.append(link)

    # Step 9: Batch URLs
    batches = [safe_links[i:i+rate_limit] for i in range(0, len(safe_links), rate_limit)]

    # Step 10-13: Validate each batch
    for batch_idx, batch in enumerate(batches):
        for link in batch:
            try:
                # Step 10: Send HEAD request with timeout
                start_time = time.time()
                response = requests.head(
                    link['url'],
                    timeout=5,
                    allow_redirects=False,
                    headers={'User-Agent': 'Obsidian-Link-Validator/1.0'}
                )
                response_time = (time.time() - start_time) * 1000  # Convert to ms

                # Step 11: Classify response
                status = response.status_code
                result = {
                    'note_path': link['note_path'],
                    'url': link['url'],
                    'status_code': status,
                    'response_time': response_time
                }

                if 200 <= status < 300:
                    result['classification'] = 'success'
                    results['success'].append(result)
                elif 300 <= status < 400:
                    result['classification'] = 'redirect'
                    result['location'] = response.headers.get('Location')
                    results['redirects'].append(result)
                elif 400 <= status < 600:
                    result['classification'] = 'broken'
                    results['broken'].append(result)

                # Step 12: Record result
                validation_results.append(result)

            except requests.Timeout:
                result = {
                    'note_path': link['note_path'],
                    'url': link['url'],
                    'status_code': None,
                    'classification': 'timeout',
                    'response_time': 5000,
                    'reason': 'Request timeout (>5 seconds)'
                }
                results['timeouts'].append(result)
                validation_results.append(result)

            except Exception as e:
                result = {
                    'note_path': link['note_path'],
                    'url': link['url'],
                    'status_code': None,
                    'classification': 'broken',
                    'response_time': None,
                    'reason': str(e)
                }
                results['broken'].append(result)
                validation_results.append(result)

        # Step 13: Rate limiting wait
        if batch_idx < len(batches) - 1:
            time.sleep(1)

    # Step 14: Calculate metrics
    total = len(validation_results)
    metrics = {
        'total_links': total,
        'broken_count': len(results['broken']),
        'redirect_count': len(results['redirects']),
        'timeout_count': len(results['timeouts']),
        'success_count': len(results['success']),
        'success_rate': len(results['success']) / total if total > 0 else 0
    }

    # Step 15: Return results
    return {
        'success': True,
        'validation_results': validation_results,
        'broken_links': results['broken'],
        'redirects': results['redirects'],
        'timeouts': results['timeouts'],
        'metrics': metrics
    }

def is_private_ip(url):
    """Block private IP ranges for SSRF prevention"""
    hostname = urlparse(url).hostname
    if not hostname:
        return False

    # Check localhost
    if hostname in ['localhost', '0.0.0.0', '127.0.0.1']:
        return True

    # Check private IP ranges (simplified - production should use ipaddress module)
    if hostname.startswith('192.168.') or hostname.startswith('10.'):
        return True
    if hostname.startswith('172.') and 16 <= int(hostname.split('.')[1]) <= 31:
        return True

    return False

def strip_credentials(url):
    """Remove username:password from URLs"""
    parsed = urlparse(url)
    if parsed.username or parsed.password:
        # Reconstruct URL without credentials
        netloc = parsed.hostname
        if parsed.port:
            netloc += f':{parsed.port}'
        return parsed._replace(netloc=netloc).geturl()
    return url
```

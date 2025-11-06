<!-- Powered by BMAD™ Core -->

# validate-external-links

Validate external URLs in vault notes for accessibility, HTTP status, and security - detect broken links, redirects, and timeouts with comprehensive security hardening.

## Purpose

Test all external links in the knowledge base to identify broken links (4xx), redirects (3xx), server errors (5xx), and connection timeouts. Includes security measures to prevent SSRF attacks, rate limit abuse, and protocol injection.

## Prerequisites

- Obsidian MCP server configured and accessible
- Network connectivity for HTTP requests
- Access to vault notes for URL extraction
- Security: SSRF prevention, rate limiting, protocol validation enabled

## Inputs

- **vault_path** (string, required): Path to Obsidian vault
- **max_links** (integer, optional): Maximum links to validate per run (default: 50)
- **timeout_seconds** (integer, optional): Timeout per URL request (default: 10)
- **rate_limit_per_second** (integer, optional): Max requests per second (default: 5)
- **user_agent** (string, optional): User-Agent header (default: "BMAD-Obsidian-Auditor/1.0")
- **follow_redirects** (boolean, optional): Follow redirects or report them (default: false - report redirects)

## Outputs

```yaml
link_validation_audit:
  total_links_found: integer # Total URLs discovered in vault
  total_links_tested: integer # URLs actually tested (capped at max_links)
  broken_links_count: integer # 4xx status codes
  redirect_links_count: integer # 3xx status codes
  server_error_count: integer # 5xx status codes
  timeout_count: integer # Connection timeouts
  valid_links_count: integer # 2xx status codes
  security_violations_count: integer # Blocked security threats
  audit_timestamp: string # ISO 8601 timestamp
  link_issues:
    - note_path: string # Note containing the link
      note_title: string # Note title
      url: string # The external URL
      status_code: string # HTTP status code or 'TIMEOUT' or 'SECURITY_BLOCKED'
      status_category: string # '2xx|3xx|4xx|5xx|TIMEOUT|SECURITY_BLOCKED'
      redirect_url: string # Final URL if redirected (3xx only)
      error_message: string # Detailed error if failed
      severity: string # 'CRITICAL|HIGH|MEDIUM|LOW'
  performance:
    execution_time_seconds: float
    average_time_per_link_seconds: float
```

## Security Architecture

### CRITICAL: Security-First Design

This task handles **external network requests** which are a primary attack vector. Security measures are **non-negotiable** and **always enforced**.

**Attack Vectors Mitigated:**
1. **SSRF (Server-Side Request Forgery)** - Attacker tricks auditor into requesting private resources
2. **Rate Limiting Bypass** - Attacker overwhelms target servers with requests
3. **Timeout DoS** - Attacker hangs auditor with slow-responding URLs
4. **Protocol Injection** - Attacker uses non-HTTP protocols to exploit system

---

## Algorithm

### Step 1: Extract All External URLs from Vault

**Objective:** Parse all notes and collect external URLs

**Implementation:**

```
1. Connect to Obsidian MCP server
2. Call list_notes() to get all note paths
3. For each note:
   - Read note content (markdown)
   - Parse URLs using regex:
     - Markdown links: \[.*?\]\((https?://.*?)\)
     - Bare URLs: <(https?://.*?)>
     - Autolinks: (https?://\S+)
   - Extract URL from each match
   - Store: {note_path, note_title, url}
4. Deduplicate URLs (same URL in multiple notes tested once)
5. Limit to max_links (default: 50) to prevent long-running audits
```

**URL Extraction Regex:**

```regex
# Markdown links: [text](URL)
\[([^\]]+)\]\((https?://[^\)]+)\)

# Bare angle bracket URLs: <URL>
<(https?://[^>]+)>

# Autolinks (URLs in text)
(https?://[^\s\)]+)
```

**Deduplication Strategy:** If same URL appears in multiple notes, test once but report all note paths where it appears.

**Max Links Limit:** To prevent abuse and long audit times, limit to 50 URLs per run (user-configurable). If vault has 100+ URLs, user can run multiple audits.

---

### Step 2: Security Validation (SSRF Prevention)

**Objective:** Block malicious URLs before making any network requests

**CRITICAL SECURITY CHECKS (Run for EVERY URL):**

#### 2.1 Protocol Validation

**Whitelist:** ONLY `http://` and `https://` protocols allowed

**Blocked Protocols:**
- `file://` - Local file access (critical security risk)
- `javascript:` - JavaScript injection
- `data:` - Data URI injection
- `ftp://` - FTP access
- `mailto:` - Email injection
- `tel:` - Phone number injection
- Any other protocol

**Implementation:**

```python
def validate_protocol(url):
    if not url.startswith(('http://', 'https://')):
        raise SecurityError(f"Invalid protocol - only http/https allowed: {url}")
    return url
```

**Response:** If blocked, return `status_code: 'SECURITY_BLOCKED'`, `severity: 'CRITICAL'`

---

#### 2.2 Private IP Range Detection (SSRF Prevention)

**Objective:** Block requests to private/internal IP addresses to prevent SSRF attacks

**Private IP Ranges (IPv4 and IPv6):**

```python
PRIVATE_IP_RANGES = [
    "127.0.0.0/8",      # Loopback
    "10.0.0.0/8",       # Private Class A
    "172.16.0.0/12",    # Private Class B
    "192.168.0.0/16",   # Private Class C
    "169.254.0.0/16",   # Link-local
    "0.0.0.0/8",        # Current network
    "::1/128",          # IPv6 loopback
    "fc00::/7",         # IPv6 private
    "fe80::/10",        # IPv6 link-local
]
```

**Implementation:**

```python
import socket
import ipaddress

def validate_no_ssrf(url):
    # Parse URL to extract hostname
    parsed = urlparse(url)
    hostname = parsed.hostname

    # Resolve DNS to IP address
    try:
        ip_address_str = socket.gethostbyname(hostname)
    except socket.gaierror:
        raise ValidationError(f"DNS resolution failed for: {hostname}")

    # Check if IP is in private range
    ip = ipaddress.ip_address(ip_address_str)
    for private_range in PRIVATE_IP_RANGES:
        network = ipaddress.ip_network(private_range)
        if ip in network:
            raise SecurityError(
                f"SSRF attempt detected: {url} resolves to private IP {ip_address_str} in range {private_range}"
            )

    return url, ip_address_str
```

**DNS Rebinding Protection:** Resolve DNS ONCE, then use the resolved IP for the request (don't re-resolve).

**Response:** If blocked, return `status_code: 'SECURITY_BLOCKED'`, `severity: 'CRITICAL'`, `error_message: 'SSRF attempt: private IP'`

---

#### 2.3 URL Sanitization

**Objective:** Remove dangerous characters and normalize URLs

**Sanitization Steps:**

```python
def sanitize_url(url):
    # Remove whitespace
    url = url.strip()

    # Remove newlines, tabs
    url = url.replace('\n', '').replace('\r', '').replace('\t', '')

    # Validate URL structure
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValidationError(f"Invalid URL structure: {url}")

    # Reconstruct safe URL
    safe_url = urlunparse(parsed)
    return safe_url
```

**Response:** If sanitization fails, return `status_code: 'SECURITY_BLOCKED'`, `severity: 'HIGH'`

---

### Step 3: Rate-Limited HTTP Validation

**Objective:** Test each validated URL with HTTP HEAD request, enforcing rate limits

**Rate Limiting:**
- **Max 5 requests per second** (user-configurable)
- Prevents overwhelming target servers
- Prevents abuse of this audit feature

**Implementation:**

```python
import time
import requests

class RateLimiter:
    def __init__(self, max_per_second=5):
        self.max_per_second = max_per_second
        self.last_request_time = 0
        self.min_interval = 1.0 / max_per_second

    def wait(self):
        now = time.time()
        time_since_last = now - self.last_request_time
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()

rate_limiter = RateLimiter(max_requests_per_second=5)

for url in validated_urls[:max_links]:
    rate_limiter.wait()  # Enforce rate limit

    try:
        response = requests.head(
            url,
            timeout=timeout_seconds,  # Default: 10 seconds
            allow_redirects=False,    # Don't follow redirects (report them)
            headers={'User-Agent': user_agent}  # Identify ourselves
        )
        status_code = response.status_code
        redirect_url = response.headers.get('Location', None) if status_code in range(300, 400) else None

    except requests.Timeout:
        status_code = 'TIMEOUT'
        error_message = f"Connection timeout after {timeout_seconds}s"

    except requests.RequestException as e:
        status_code = 'ERROR'
        error_message = str(e)

    # Classify and record result
    classify_link_status(url, status_code, redirect_url, error_message)
```

**Timeout Enforcement:** Each request has a strict timeout (default: 10 seconds). No infinite hangs.

**User-Agent Header:** Identify as `"BMAD-Obsidian-Auditor/1.0"` for transparency and robots.txt compliance.

---

### Step 4: Classify Link Status and Severity

**Objective:** Categorize each link result and assign severity

**Status Classification:**

| Status Code | Category | Severity | Description | Action |
|-------------|----------|----------|-------------|--------|
| **2xx** | Valid | N/A (no issue) | Link is working | No action needed |
| **3xx** | Redirect | MEDIUM | Link redirects to new URL | Update link to redirect_url |
| **4xx** | Broken | **CRITICAL** | Resource not found or forbidden | Fix or remove link |
| **5xx** | Server Error | HIGH | Server-side issue (may be temporary) | Retry later or contact site owner |
| **TIMEOUT** | Timeout | HIGH | Connection timed out | Retry or remove if persistent |
| **SECURITY_BLOCKED** | Security | **CRITICAL** | SSRF or protocol violation | Remove link immediately |

**Implementation:**

```python
def classify_link_status(url, status_code, redirect_url=None, error_message=None):
    if isinstance(status_code, int):
        if 200 <= status_code < 300:
            category = '2xx'
            severity = None  # No issue
        elif 300 <= status_code < 400:
            category = '3xx'
            severity = 'MEDIUM'
        elif 400 <= status_code < 500:
            category = '4xx'
            severity = 'CRITICAL'
        elif 500 <= status_code < 600:
            category = '5xx'
            severity = 'HIGH'
    elif status_code == 'TIMEOUT':
        category = 'TIMEOUT'
        severity = 'HIGH'
    elif status_code == 'SECURITY_BLOCKED':
        category = 'SECURITY_BLOCKED'
        severity = 'CRITICAL'
    else:
        category = 'ERROR'
        severity = 'HIGH'

    return {
        'url': url,
        'status_code': status_code,
        'status_category': category,
        'redirect_url': redirect_url,
        'error_message': error_message,
        'severity': severity
    }
```

---

### Step 5: Aggregate and Report Results

**Objective:** Compile all link validation results for audit report

**Aggregation:**

```
For each link tested:
  - If 4xx: Add to broken_links_list
  - If 3xx: Add to redirect_links_list
  - If 5xx: Add to server_error_list
  - If TIMEOUT: Add to timeout_list
  - If SECURITY_BLOCKED: Add to security_violations_list
  - If 2xx: Count as valid (don't report in issues list)

Count totals:
  - broken_links_count = len(broken_links_list)
  - redirect_links_count = len(redirect_links_list)
  - timeout_count = len(timeout_list)
  - security_violations_count = len(security_violations_list)
  - valid_links_count = total_links_tested - (broken + redirect + timeout + security)
```

**Sort Results by Severity:**

```
Sort link_issues by:
  1. severity (CRITICAL → HIGH → MEDIUM → LOW)
  2. Within same severity, sort alphabetically by note_path
```

---

### Step 6: Return Audit Results

**Return Value:**

```yaml
link_validation_audit:
  total_links_found: 75
  total_links_tested: 50  # Capped at max_links
  broken_links_count: 10
  redirect_links_count: 5
  server_error_count: 2
  timeout_count: 3
  valid_links_count: 30
  security_violations_count: 0
  audit_timestamp: '2025-11-06T14:30:00Z'
  link_issues:
    - note_path: 'references/web-resources.md'
      note_title: 'Web Development Resources'
      url: 'https://old-blog.example.com/post-123'
      status_code: 404
      status_category: '4xx'
      redirect_url: null
      error_message: 'Not Found'
      severity: 'CRITICAL'
    - note_path: 'research/papers.md'
      note_title: 'Research Papers'
      url: 'https://site.com/old-page'
      status_code: 301
      status_category: '3xx'
      redirect_url: 'https://site.com/new-page'
      error_message: 'Moved Permanently'
      severity: 'MEDIUM'
  performance:
    execution_time_seconds: 12.5
    average_time_per_link_seconds: 0.25
```

---

## Security Checklist (Always Enforced)

- [x] Protocol validation: Only http/https allowed
- [x] SSRF prevention: Private IP ranges blocked
- [x] DNS rebinding protection: Resolve DNS once, use IP
- [x] Rate limiting: Max 5 requests/second enforced
- [x] Timeout enforcement: 10-second timeout per request
- [x] User-Agent header: Identify as "BMAD-Obsidian-Auditor/1.0"
- [x] URL sanitization: Remove dangerous characters
- [x] Max links limit: Cap at 50 URLs per run (user-configurable)
- [x] Security violations logged: Track SSRF attempts for security audit
- [x] No sensitive data exposure: Audit operates read-only on vault

**IMPORTANT:** These security measures are **always active** and **cannot be disabled**. Attempting to bypass security will result in `SECURITY_BLOCKED` status.

---

## Use Cases

### 1. Detect Broken Links

**Scenario:** Identify broken external links (404s) in knowledge base

**Workflow:**
1. Run `*audit-links`
2. Review CRITICAL issues (4xx status codes)
3. Fix or remove broken links
4. Re-run audit to verify fixes

---

### 2. Update Redirects

**Scenario:** Find and update outdated URLs that redirect to new locations

**Workflow:**
1. Run `*audit-links`
2. Filter results to 3xx status codes
3. For each redirect:
   - Update old URL to redirect_url in note
   - Verify new URL works (2xx status)

---

### 3. Security Audit

**Scenario:** Detect potential SSRF attempts or malicious links

**Workflow:**
1. Run `*audit-links`
2. Check security_violations_count
3. If > 0, review SECURITY_BLOCKED entries
4. Remove or sanitize suspicious URLs
5. Investigate who added the malicious links

---

## Performance Benchmarks

**Target Performance:**

| Links Tested | Expected Time | Rate Limit Impact |
|--------------|---------------|-------------------|
| 10 links     | ~2 seconds    | Rate limit: 0.2s/link |
| 50 links     | ~10 seconds   | Rate limit: 0.2s/link |
| 100 links    | ~20 seconds   | Rate limit: 0.2s/link |

**Note:** Rate limiting (5 requests/second) adds 0.2s per link. Actual network latency varies by target server.

**Optimization:** If vault has 500+ URLs, run multiple audits with `max_links` or use `*progressive` mode.

---

## Error Scenarios

### 1. Network Connectivity Issue

**Error:** "Network unreachable - check internet connection"

**Remediation:**
- Verify internet connection
- Test with simple curl/ping command
- Check firewall settings

---

### 2. SSRF Attack Attempt

**Error:** "SSRF attempt detected: URL resolves to private IP 192.168.1.1"

**Remediation:**
- Remove the malicious URL from the note
- Investigate who added the URL
- This is a security incident - log for audit

---

### 3. Rate Limit Hit

**Error:** "Rate limit exceeded - max 5 requests/second"

**Remediation:**
- This is expected behavior (security measure)
- Audit will automatically wait between requests
- Increase max_links if too slow

---

## Testing

### Test Case 1: Broken Link Detection

**Setup:**
- 50 notes with external links
- 10 links with 404 status codes (broken)

**Expected Results:**
- broken_links_count = 10
- All 10 broken links reported with severity: CRITICAL

**Pass Criteria:** 100% accuracy in detecting 404s

---

### Test Case 2: Redirect Detection

**Setup:**
- 50 notes with external links
- 5 links with 301/302 status codes (redirects)

**Expected Results:**
- redirect_links_count = 5
- All 5 redirects reported with redirect_url populated

**Pass Criteria:** 100% accuracy, redirect URLs captured

---

### Test Case 3: Security - SSRF Prevention

**Setup:**
- Note with link: `http://localhost:8080/admin`
- Run audit

**Expected Results:**
- status_code: 'SECURITY_BLOCKED'
- severity: 'CRITICAL'
- error_message: 'SSRF attempt: private IP'
- security_violations_count = 1

**Pass Criteria:** SSRF blocked, no request made

---

### Test Case 4: Security - Invalid Protocol

**Setup:**
- Note with link: `file:///etc/passwd`
- Run audit

**Expected Results:**
- status_code: 'SECURITY_BLOCKED'
- severity: 'CRITICAL'
- error_message: 'Invalid protocol - only http/https allowed'
- security_violations_count = 1

**Pass Criteria:** Protocol blocked, no request made

---

### Test Case 5: Rate Limiting Enforced

**Setup:**
- 50 links to validate
- Run audit

**Expected Results:**
- Rate limiting enforced (5 requests/second)
- Execution time >= 10 seconds (50 links × 0.2s/link)

**Pass Criteria:** Rate limit enforced (no more than 5 req/sec)

---

### Test Case 6: Timeout Handling

**Setup:**
- Note with link to slow server (>10s response time)
- Run audit

**Expected Results:**
- status_code: 'TIMEOUT'
- severity: 'HIGH'
- error_message: 'Connection timeout after 10s'
- timeout_count = 1

**Pass Criteria:** Timeout handled gracefully, no hang

---

## Integration with Quality Auditor Agent

This task is executed when:

1. `*audit-links [max_links]` command issued
2. `*audit-full` command runs (uses default max_links: 50)
3. Progressive audit mode processes link validation batch

**Security Monitoring:** Security violations logged and reported to user. Repeated SSRF attempts may indicate compromised vault or malicious actor.

**Caching:** Results cached for report generation. Cache invalidated when notes modified or URLs change.

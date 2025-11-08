---
title: Web Research Sources
created: 2025-05-01T12:00:00Z
last_updated: 2025-10-15T16:45:00Z
tags: [research, external-links]
---

# Web Research Sources

This note contains various external links for testing link validation.

## Working Links (2xx Success)

These links should return successful responses:

- [Example Domain](https://example.com) - IANA example domain
- [IANA Domains](https://www.iana.org/domains/example) - Official documentation

## Broken Links (4xx Client Errors)

These links should be detected as broken:

- [Not Found Page](https://httpstat.us/404) - 404 Not Found
- [Forbidden Resource](https://httpstat.us/403) - 403 Forbidden
- [Gone Forever](https://httpstat.us/410) - 410 Gone

## Broken Links (5xx Server Errors)

These should also be marked as broken:

- [Server Error](https://httpstat.us/500) - 500 Internal Server Error
- [Bad Gateway](https://httpstat.us/502) - 502 Bad Gateway

## Redirect Links (3xx)

These should be classified as redirects:

- [Moved Permanently](https://httpstat.us/301) - 301 redirect
- [Temporary Redirect](https://httpstat.us/302) - 302 redirect
- [See Other](https://httpstat.us/303) - 303 redirect

## Timeout Links

These should timeout (>5 second response):

- [Slow Server 1](https://httpstat.us/200?sleep=10000) - 10s delay
- [Slow Server 2](https://httpstat.us/200?sleep=8000) - 8s delay

## Security-Blocked Links (SSRF Prevention)

These should be BLOCKED by security filters and never sent to network:

- [Local Admin](http://localhost:8080/api) - Localhost blocked
- [Private Network](http://192.168.1.1/admin) - Private IP blocked
- [Loopback](http://127.0.0.1/internal) - Loopback blocked
- [Private Class A](http://10.0.0.1/private) - Private IP blocked

## Invalid Protocol Links

These should be blocked due to dangerous protocols:

- javascript:alert('XSS') - JavaScript protocol
- data:text/html,<script>alert('XSS')</script> - Data URI

## Plain URLs (no markdown syntax)

Testing plain URL extraction:

- https://example.org/plain-url-1
- https://example.net/plain-url-2

---

**Test Characteristics:**

- Total links: ~25
- Working: 2
- Broken (4xx): 3
- Broken (5xx): 2
- Redirects: 3
- Timeouts: 2
- Blocked (security): 4
- Invalid protocol: 2
- Plain URLs: 2

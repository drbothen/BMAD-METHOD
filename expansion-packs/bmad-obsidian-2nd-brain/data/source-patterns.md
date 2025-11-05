<!-- Powered by BMAD™ Core -->

# Source Patterns and Author Extraction

## Overview

This document defines URL pattern recognition and author extraction patterns for common content sources. Used by the metadata extraction task (`extract-metadata.md`) to identify source types and extract author information.

---

## URL Pattern Categories

### Academic Sources

**Pattern Recognition:**

- `arxiv.org/*` - arXiv preprints
- `scholar.google.com/*` - Google Scholar
- `pubmed.ncbi.nlm.nih.gov/*` - PubMed
- `doi.org/*` - DOI resolvers
- `*.edu/*` - Educational institutions
- `jstor.org/*` - JSTOR
- `researchgate.net/*` - ResearchGate
- `*.ac.uk/*` - UK academic institutions

**Author Extraction Patterns:**

- Look for meta tags: `<meta name="citation_author" content="...">`
- Author lists in header: "Authors: First Last, First Last"
- Citation format: "(Last, F., Last, F.)"
- After "by" keyword in title area

**Example URLs:**

- `https://arxiv.org/abs/2103.12345`
- `https://pubmed.ncbi.nlm.nih.gov/12345678/`
- `https://doi.org/10.1000/xyz123`

**Metadata to Capture:**

- Paper title (from `<meta name="citation_title">`)
- Author list (from `<meta name="citation_author">`)
- Publication date (from `<meta name="citation_date">`)
- Abstract/summary
- DOI if available

---

### News and Media

**Pattern Recognition:**

- `medium.com/@*` or `*.medium.com/*` - Medium
- `substack.com/*` or `*.substack.com/*` - Substack
- `nytimes.com/*` - New York Times
- `theguardian.com/*` - The Guardian
- `wsj.com/*` - Wall Street Journal
- `bbc.com/news/*` - BBC News
- `techcrunch.com/*` - TechCrunch
- `arstechnica.com/*` - Ars Technica

**Author Extraction Patterns:**

- Byline: "By [Name]" (common in journalism)
- Meta tags: `<meta name="author" content="...">`
- After "Written by" or "Published by"
- In URL for Medium: `medium.com/@username/`
- Author name in article header/footer

**Example URLs:**

- `https://medium.com/@username/article-title-abc123`
- `https://example.substack.com/p/article-title`
- `https://www.nytimes.com/2025/11/04/technology/article-title.html`

**Metadata to Capture:**

- Article title
- Author name and profile link
- Publication name
- Publication date
- Tags/categories if available

---

### Social Media

**Pattern Recognition:**

**Twitter/X:**

- `twitter.com/*/status/*` or `x.com/*/status/*`
- Author: username from URL path
- Format: `twitter.com/username/status/tweet_id`

**LinkedIn:**

- `linkedin.com/posts/*`
- `linkedin.com/pulse/*`
- Author: often in URL or post metadata

**Reddit:**

- `reddit.com/r/*/comments/*`
- Author: u/username format
- Subreddit: r/subreddit format

**Hacker News:**

- `news.ycombinator.com/item?id=*`
- Author: in post metadata

**Author Extraction Patterns:**

- **Twitter/X:** Username from URL: `twitter.com/@username/`
- **LinkedIn:** Profile name in post author field
- **Reddit:** `u/username` format
- Handle format: @username

**Example URLs:**

- `https://twitter.com/username/status/1234567890`
- `https://www.linkedin.com/posts/username_article-id`
- `https://www.reddit.com/r/subreddit/comments/abc123/title/`

**Metadata to Capture:**

- Username/handle
- Display name if different from handle
- Platform name
- Timestamp of post
- Thread/conversation context

---

### Books and Reading Apps

**Pattern Recognition:**

**Kindle/Amazon:**

- `amazon.com/*/dp/*` or `amazon.com/gp/product/*`
- ASIN/ISBN in URL
- "My Clippings.txt" exports

**Readwise:**

- `readwise.io/open/*`
- Highlight exports

**Literal.club:**

- `literal.club/book/*`
- Reading progress and highlights

**Goodreads:**

- `goodreads.com/book/show/*`
- Book reviews and quotes

**Author Extraction Patterns:**

- From book metadata: "by [Author Name]"
- Amazon: Look for "by" line under title
- Readwise: Author field in export
- Kindle clippings: Book title line format "Title (Author Name)"

**Example URLs:**

- `https://www.amazon.com/dp/B01M0KEZIT` (Kindle book)
- `https://readwise.io/open/123456789`
- `https://literal.club/book/abcd-1234`

**Metadata to Capture:**

- Book title
- Author name
- ISBN/ASIN
- Page number or location (for highlights)
- Highlight text
- Your notes/tags

---

### Documentation and Technical Resources

**Pattern Recognition:**

- `github.com/*/*` - GitHub repositories
- `stackoverflow.com/questions/*` - Stack Overflow
- `docs.*.com/*` - Official documentation sites
- `developer.*.com/*` - Developer resources
- `*.readthedocs.io/*` - Read the Docs
- `wikipedia.org/wiki/*` - Wikipedia

**Author Extraction Patterns:**

- **GitHub:** Repository owner: `github.com/owner/repo`
- **Stack Overflow:** Question/answer author in page
- **Documentation:** Often "Organization" rather than individual
- **Wikipedia:** Multiple editors, use "Wikipedia" as author

**Example URLs:**

- `https://github.com/username/repository`
- `https://stackoverflow.com/questions/12345678/question-title`
- `https://docs.python.org/3/library/collections.html`

**Metadata to Capture:**

- Page/resource title
- Organization/project name
- Last updated date
- Section/topic hierarchy
- Code language (for programming docs)

---

### Blogs and Personal Sites

**Pattern Recognition:**

- Various domains, no standard pattern
- Often have `/blog/`, `/posts/`, `/articles/` in path
- Typically use blog platforms: WordPress, Ghost, Jekyll, Hugo

**Author Extraction Patterns:**

- Meta tags: `<meta name="author" content="...">`
- Byline in post header: "By [Name]" or "Written by [Name]"
- About page reference
- Footer copyright: "© 2025 [Name]"
- If unclear, use site name/domain as author

**Example URLs:**

- `https://exampleblog.com/posts/article-title`
- `https://www.personaldomain.com/blog/2025/11/article`

**Metadata to Capture:**

- Post title
- Author name or site name
- Publication date
- Tags/categories
- Related posts

---

## Author Extraction Algorithm

### Priority Order

When extracting author information, check in this order:

1. **Structured metadata** (highest confidence)
   - HTML meta tags: `<meta name="author" content="...">`
   - OpenGraph: `<meta property="article:author" content="...">`
   - JSON-LD structured data: `@type: "Person"`

2. **URL patterns** (high confidence)
   - Twitter/X: username in URL
   - Medium: @username in URL
   - GitHub: owner in URL path

3. **Byline patterns** (medium confidence)
   - "By [Name]" or "Written by [Name]"
   - "Author: [Name]"
   - "[Name] | Date" format

4. **Page structure** (lower confidence)
   - Author name in header/masthead
   - Author bio section
   - Copyright footer

5. **Fallback** (lowest confidence)
   - Use domain name as source
   - Mark author as "Unknown"

### Common Patterns and Regex

**Byline patterns:**

```regex
By\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
Written by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
Author:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
Posted by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)
```

**Username/handle patterns:**

```regex
@([a-zA-Z0-9_]+)
u/([a-zA-Z0-9_-]+)
```

**Name formats:**

- First Last: "John Doe"
- Last, First: "Doe, John"
- First Middle Last: "John Q. Doe"
- With credentials: "Jane Smith, PhD"

**Normalization:**

- Remove titles: Dr., Prof., Mr., Ms., PhD, etc. (unless critical)
- Standardize to "First Last" format
- Preserve hyphens in hyphenated names
- Trim whitespace
- Limit to 256 characters

---

## Special Cases and Edge Cases

### Multiple Authors

If multiple authors found:

- **Academic papers:** Capture all, comma-separated: "Smith, J., Jones, A., Brown, K."
- **Blog posts:** Usually single author, use first found
- **Collaborative posts:** Use "Author 1 & Author 2" or "Author 1 et al." (if 3+)

### Organizational Authors

When organization is author, not individual:

- **Use organization name:** "Mozilla Foundation", "W3C", "IETF"
- **Don't use:** "Team", "Staff", "Editor"
- **Format:** Official organization name from site

### Pseudonymous Authors

Handle usernames and pseudonyms:

- **Preserve exactly:** "@dhh", "patio11", "sama"
- **Don't try to find real name** (privacy)
- **Format:** Keep @ symbol or u/ prefix if that's how they're known

### No Author Found

When author cannot be determined:

- **Set to:** "Unknown"
- **Add note in context:** "Author could not be extracted from [domain]"
- **Don't guess or fabricate**

---

## Security and Validation

### URL Validation

**Safe URL patterns:**

```regex
^https?://[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}(/.*)?$
```

**Blocked patterns:**

- `file://` - Local file access
- `javascript:` - Script execution
- `data:` - Data URLs (can hide scripts)
- `vbscript:` - VBScript execution
- `about:` - Browser internals

**Validation rules:**

- Maximum URL length: 2048 characters
- Must start with `http://` or `https://`
- Domain must be valid format
- Reject obvious XSS attempts

### Author Name Validation

**Security rules:**

- No HTML tags: `<script>`, `<a>`, etc.
- Escape special characters: `<`, `>`, `&`, `"`, `'`
- Maximum length: 256 characters
- Reject obvious injection attempts
- Allow Unicode for international names

---

## Platform-Specific Extraction Logic

### Medium.com

**URL format:** `https://medium.com/@username/article-title-abc123`

**Extraction:**

1. Try meta tag: `<meta property="article:author" content="...">`
2. Try URL: Extract `@username` from path
3. Try byline: "Written by [Name]" at top of article

**Output format:** "[Name]" or "@username"

### Substack

**URL format:** `https://example.substack.com/p/article-title`

**Extraction:**

1. Try meta tag: `<meta name="author" content="...">`
2. Try subdomain: `example.substack.com` → "example"
3. Try newsletter name in header

**Output format:** "[Newsletter Name]" or "[Author Name]"

### Twitter/X

**URL format:** `https://twitter.com/username/status/1234567890`

**Extraction:**

1. Extract username from URL path (always present)
2. Look up display name if API available (optional)

**Output format:** "@username" or "Display Name (@username)"

### GitHub

**URL format:** `https://github.com/owner/repository`

**Extraction:**

1. Extract owner from URL: `/owner/repo` → "owner"
2. Look up full name from profile if available

**Output format:** "@owner" or "[Full Name] (@owner)"

### arXiv

**URL format:** `https://arxiv.org/abs/2103.12345`

**Extraction:**

1. Try meta tag: `<meta name="citation_author" content="...">`
2. Parse author list from paper metadata
3. Format as comma-separated list

**Output format:** "Smith, J., Jones, A."

---

## Testing and Validation

### Test Cases

Create test cases for:

1. Each platform-specific extractor
2. Edge cases (no author, multiple authors, pseudonyms)
3. Security cases (XSS, injection, malformed URLs)
4. Unicode names (international authors)
5. Fallback scenarios (metadata missing)

### Test Data Format

```yaml
test_cases:
  - url: 'https://medium.com/@username/article-title-123'
    expected_author: '@username'
    expected_source_type: 'news_media'

  - url: 'https://arxiv.org/abs/2103.12345'
    expected_author: 'Smith, J., Jones, A.'
    expected_source_type: 'academic'

  - url: "https://malicious.com/<script>alert('xss')</script>"
    expected_author: 'Unknown'
    expected_source_type: 'unknown'
    expected_error: 'Invalid URL pattern'
```

---

## Maintenance

This document should be updated when:

- New platforms become popular sources
- Platforms change their URL structure
- Author extraction patterns fail in production
- Security vulnerabilities discovered
- User feedback identifies missing sources

**Last Updated:** 2025-11-04
**Version:** 1.0

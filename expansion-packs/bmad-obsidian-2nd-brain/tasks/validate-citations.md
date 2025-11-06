<!-- Powered by BMAD™ Core -->

# validate-citations

Validate source citation completeness and quality in vault notes - detect missing attributions, incomplete citations, and unattributed claims.

## Purpose

Ensure knowledge base maintains proper source attribution for external claims, preventing loss of provenance and maintaining academic/professional integrity.

## Prerequisites

- Obsidian MCP server configured
- Access to vault notes
- Understanding of citation formats (APA, MLA, Chicago, or custom)

## Inputs

- **vault_path** (string, required): Path to Obsidian vault
- **required_fields** (array, optional): Required citation fields (default: ['author', 'title', 'url_or_isbn', 'date'])
- **citation_format** (string, optional): Expected format (default: 'auto-detect')
- **unattributed_claim_threshold** (integer, optional): Max unattributed claims before flagging (default: 3)

## Outputs

```yaml
citation_validation_audit:
  total_notes: integer
  notes_with_citation_issues: integer
  citation_coverage_percentage: float # (notes_complete / total_notes) * 100
  audit_timestamp: string
  citation_issues:
    - note_path: string
      note_title: string
      issue_type: string # 'NO_ATTRIBUTION|INCOMPLETE|FORMAT_ERROR|UNATTRIBUTED_CLAIMS'
      issue_severity: string # 'CRITICAL|HIGH|MEDIUM|LOW'
      missing_fields: array # ['author', 'date'] etc.
      unattributed_claims_count: integer
      detected_format: string # 'APA|MLA|Chicago|Custom|None'
      recommendations: array # Remediation suggestions
```

## Algorithm

### Step 1: Query All Notes

```
1. Connect to Obsidian MCP
2. list_notes() with full content
3. For each note, extract:
   - note_path, note_title
   - Full markdown content
   - Frontmatter metadata (if present)
```

### Step 2: Check Citation Completeness

For each note:

**2.1 Detect Citation Section**
- Look for "## Source Attribution" or "## Sources" or "## References" section
- Check frontmatter for: source, author, url, date fields
- Parse inline citations (e.g., "(Author, Year)")

**2.2 Validate Required Fields**

Required fields (if external claims present):
- author (required)
- title (required)
- url OR isbn (required for external sources)
- date (required for time-sensitive content)

**Classification:**
- **Complete:** All 4 required fields present
- **Incomplete:** Missing 2+ required fields → Issue severity: HIGH
- **Missing:** No attribution at all → Issue severity: CRITICAL

### Step 3: Detect Unattributed Claims

**Heuristic:** Identify declarative factual statements without nearby citations

**Algorithm:**
```
1. Extract declarative statements (sentences ending with period, no questions)
2. Identify factual claims (avoid opinions, personal observations)
3. For each claim, check if citation within 2 paragraphs
4. Count unattributed claims
5. If count > threshold (default 3): Flag as HIGH severity
```

**Signals for Factual Claims:**
- Statistics, percentages, numbers
- Historical facts, dates, events
- Scientific findings, research results
- Quotes or paraphrased content
- "Studies show", "Research indicates", "According to"

### Step 4: Format Consistency Check

**Detect Citation Format:**
- APA: (Author, Year) or Author (Year)
- MLA: (Author Page) or (Author)
- Chicago: Footnotes or (Author Year, Page)
- Custom: Vault-specific format

**Check Consistency:**
- If mixed formats detected: Issue severity: MEDIUM
- If no consistent format: Issue severity: LOW

### Step 5: Classify and Aggregate

**Issue Classification:**

| Issue Type | Severity | Condition |
|------------|----------|-----------|
| NO_ATTRIBUTION | CRITICAL | Note has external claims but no source attribution |
| INCOMPLETE | HIGH | Missing 2+ required fields (author, title, url/isbn, date) |
| UNATTRIBUTED_CLAIMS | HIGH | >3 factual claims without citations |
| FORMAT_ERROR | MEDIUM | Mixed or inconsistent citation formats |
| MINOR_FORMAT | LOW | Minor format issues (punctuation, spacing) |

**Calculate Coverage:**
```
citation_coverage_percentage = (notes_complete / total_notes) * 100
```

## Performance Target

<3 seconds for 100 notes

## Use Cases

**1. Academic Integrity Audit**
- Detect notes lacking proper source attribution
- Ensure all research properly cited

**2. Knowledge Provenance**
- Prevent loss of source information
- Maintain attribution chain for claims

**3. Citation Format Standardization**
- Detect format inconsistencies
- Guide users to consistent format

## Error Handling

- No Source Attribution section: Not an error (personal notes OK)
- Frontmatter parsing error: Warn, continue
- Malformed markdown: Skip, log warning

## Testing

**Test Case 1:** 30 notes
- 10 complete citations → Pass
- 10 incomplete (missing author+date) → HIGH severity
- 10 no attribution with claims → CRITICAL severity

Expected: 20 issues detected, 33% coverage

## Integration

Executed by:
- `*audit-citations` command
- `*audit-full` command
- Progressive audit batch processing

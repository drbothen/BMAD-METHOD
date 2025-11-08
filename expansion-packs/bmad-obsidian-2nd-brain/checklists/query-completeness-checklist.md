<!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Query Completeness Checklist

# ------------------------------------------------------------

---

checklist:
id: query-completeness-checklist
name: Query Completeness Checklist
description: Quality gates for query result validation - ensures query results are complete, accurate, and properly attributed
items: - "[ ] Intent classification test: Query intent correctly classified with >85% confidence" - "[ ] Result relevance test: Top 5 results directly relevant to query (composite score >= 0.7)" - "[ ] Source attribution test: All results include source attribution (note title, path, date)" - "[ ] Multi-source test: Results queried from all available sources (Obsidian + Smart Connections + Neo4j if available)" - "[ ] Deduplication test: No duplicate results (same note_path)" - "[ ] Format selection test: Result format matches query intent (narrative/list/table/timeline)" - "[ ] Contradiction detection test: Contradictions identified if present (>70% similarity + opposing claims)" - "[ ] Performance test: Query completed in <3 seconds total" - "[ ] Error handling test: Graceful degradation if sources unavailable with informative warnings" - "[ ] Completeness test: Query answered the user's question adequately"

---

## Purpose

This checklist ensures query results meet quality standards - providing complete, accurate, properly attributed information from all available sources within performance budgets. It serves as a quality gate before presenting results to the user.

## When to Use

- After executing a query and before presenting results
- When validating query system accuracy
- During query testing and validation
- When measuring intent classification performance
- When troubleshooting query quality issues

## Quality Criteria Details

### 1. Intent Classification Test

**Check:** Query intent correctly classified with confidence score >85%

**Pass Criteria:**

- Intent classification matches expected intent for query pattern
- Confidence score >= 0.85
- Ambiguous queries (confidence < 0.70) prompt user clarification

**Remediation if failed:**

- Review query patterns in parse-natural-language-query.md
- Check for missing pattern signals
- Verify confidence scoring algorithm
- Add clarification prompt for ambiguous queries

**Example PASS:**

```
Query: "What is Zettelkasten?"
Intent: factual
Confidence: 0.92
→ Clear factual pattern, high confidence ✓
```

**Example FAIL:**

```
Query: "Tell me about productivity"
Intent: factual
Confidence: 0.65
→ Ambiguous (factual vs exploratory), needs clarification ✗
```

### 2. Result Relevance Test

**Check:** Top 5 results directly relevant to query with composite relevance >= 0.7

**Pass Criteria:**

- At least 3 of top 5 results have composite_relevance >= 0.7
- Results contain query concepts in title or content
- Results ranked by relevance (highest first)

**Remediation if failed:**

- Review semantic search threshold (may be too low)
- Check text search pattern matching
- Verify relevance scoring algorithm in merge-results.md
- Consider broadening search if no results found

**Example PASS:**

```
Top 5 results:
1. "Zettelkasten Definition" (0.95)
2. "Atomic Notes in Zettelkasten" (0.87)
3. "Slip-Box Method" (0.82)
4. "Note-Taking MOC" (0.78)
5. "Knowledge Management Systems" (0.72)
→ All >= 0.7, directly relevant ✓
```

**Example FAIL:**

```
Top 5 results:
1. "Zettelkasten Definition" (0.90)
2. "Productivity Tools" (0.45)
3. "My Daily Journal" (0.38)
4. "Random Thoughts" (0.35)
5. "Meeting Notes" (0.30)
→ Only 1 result relevant, others too low ✗
```

### 3. Source Attribution Test

**Check:** All results include complete source attribution

**Required Fields:**

- note_title
- note_path
- excerpt (content snippet)
- sources (array of data sources)
- metadata.created_date (or modified_date)

**Pass Criteria:**

- 100% of results have all required fields
- Source attribution accurate and traceable
- Timestamps in ISO 8601 format

**Remediation if failed:**

- Check result structure in execute-obsidian-query.md
- Verify metadata extraction
- Ensure fallback values for missing metadata

**Example PASS:**

```
{
  note_title: "Zettelkasten Method",
  note_path: "atomic/zettelkasten.md",
  excerpt: "Zettelkasten is a method of...",
  sources: ["smart_connections", "obsidian_text_search"],
  metadata: {
    created_date: "2024-03-15T10:23:00Z"
  }
}
→ All fields present ✓
```

**Example FAIL:**

```
{
  note_title: "Zettelkasten Method",
  note_path: "atomic/zettelkasten.md"
  // Missing: excerpt, sources, metadata
}
→ Incomplete attribution ✗
```

### 4. Multi-Source Test

**Check:** Results queried from all available data sources

**Available Sources:**

- Obsidian MCP Tools (text search)
- Smart Connections MCP (semantic search)
- Neo4j Graphiti MCP (temporal/graph queries) - optional

**Pass Criteria:**

- Query attempted against all configured sources
- sources_available list includes all active sources
- sources_failed list only includes truly unavailable sources
- Warnings generated for failed sources

**Remediation if failed:**

- Check MCP server configuration
- Verify MCP server status (running/accessible)
- Review timeout settings
- Ensure graceful degradation logic

**Example PASS:**

```
sources_available: ["smart_connections", "obsidian_text_search"]
sources_failed: []
→ Both primary sources queried ✓
```

**Example FAIL:**

```
sources_available: ["obsidian_text_search"]
sources_failed: ["smart_connections"]
→ Missing semantic search without warning ✗
```

### 5. Deduplication Test

**Check:** No duplicate results with same note_path

**Pass Criteria:**

- All result note_path values are unique
- Duplicate sources merged into single result
- Metadata from all sources preserved in merged result

**Remediation if failed:**

- Review deduplication logic in merge-results.md
- Check note_path normalization (path separators, case)
- Verify merge_result_metadata function

**Example PASS:**

```
results:
  - note_path: "atomic/zettelkasten.md" (sources: ["smart_connections", "text_search"])
  - note_path: "atomic/atomic-notes.md" (sources: ["smart_connections"])
  - note_path: "mocs/note-taking.md" (sources: ["text_search"])
→ All unique paths ✓
```

**Example FAIL:**

```
results:
  - note_path: "atomic/zettelkasten.md" (source: "smart_connections")
  - note_path: "atomic/zettelkasten.md" (source: "text_search")
→ Duplicate path not merged ✗
```

### 6. Format Selection Test

**Check:** Result format matches query intent appropriately

**Format Mapping:**

- factual → list (or narrative for single result)
- temporal → timeline
- causal → narrative
- comparative → table
- exploratory → list (with categories)

**Pass Criteria:**

- Format selection logic matches intent
- Format renders correctly in template
- Results structured appropriately for format

**Remediation if failed:**

- Review format selection in query-interpreter-agent.md
- Check query-result-tmpl.yaml template rendering
- Verify result structure matches format requirements

**Example PASS:**

```
Query: "Compare Zettelkasten and PARA"
Intent: comparative
Format: table
→ Correct format for comparison ✓
```

**Example FAIL:**

```
Query: "How has Zettelkasten evolved?"
Intent: temporal
Format: list
→ Should be timeline, not list ✗
```

### 7. Contradiction Detection Test

**Check:** Contradictions identified when present in results

**Detection Criteria:**

- Semantic similarity between claims >70%
- Opposing sentiment or values detected
- Contradiction confidence score >70%

**Pass Criteria:**

- Contradictions array includes all detected conflicts
- Each contradiction has both note_a and note_b
- Confidence scores and types included
- False positive rate <10%

**Remediation if failed:**

- Review contradiction detection in merge-results.md
- Adjust similarity threshold
- Refine opposing sentiment detection patterns
- Test with known contradictory notes

**Example PASS:**

```
Query: "Do atomic notes improve recall?"
Results include:
  - "Atomic notes significantly improve recall" (2024-05)
  - "Atomic notes do not improve recall vs traditional" (2024-08)
Contradictions: [
  {
    note_a: {...},
    note_b: {...},
    confidence: 0.78,
    type: "negation"
  }
]
→ Contradiction detected ✓
```

**Example FAIL:**

```
Same query and contradictory results
Contradictions: []
→ Failed to detect contradiction ✗
```

### 8. Performance Test

**Check:** Query completed within performance budget (<3 seconds total)

**Performance Budget:**

- Query parsing: <200ms
- Obsidian queries: <1 second per source
- Neo4j queries: <1 second
- Result merging: <500ms
- **Total: <3 seconds**

**Pass Criteria:**

- query_duration_ms < 3000
- No timeout errors
- Phase durations within budget

**Remediation if failed:**

- Identify slow phase (check performance log)
- Optimize slow queries (reduce scope, add indexes)
- Adjust timeout settings if needed
- Consider caching for repeated queries

**Example PASS:**

```
Performance:
  parse_ms: 120
  obsidian_query_ms: 650
  neo4j_query_ms: 480
  merge_ms: 320
  total_ms: 1570
→ Under 3 second budget ✓
```

**Example FAIL:**

```
Performance:
  parse_ms: 150
  obsidian_query_ms: 2800
  neo4j_query_ms: timeout
  merge_ms: 450
  total_ms: 3400
→ Exceeded budget, Neo4j timed out ✗
```

### 9. Error Handling Test

**Check:** Graceful degradation with informative warnings when sources fail

**Pass Criteria:**

- System continues with available sources
- Warnings array populated with error details
- User informed about degraded capabilities
- Error messages actionable (what to check/fix)

**Remediation if failed:**

- Add try-catch blocks around MCP calls
- Populate warnings array on failures
- Provide actionable error messages
- Ensure user communication in result template

**Example PASS:**

```
sources_available: ["obsidian_text_search"]
sources_failed: ["smart_connections"]
warnings: [
  {
    source: "smart_connections",
    error: "MCP server unavailable",
    impact: "Semantic search unavailable, results may be less relevant"
  }
]
→ Graceful degradation with warning ✓
```

**Example FAIL:**

```
sources_available: ["obsidian_text_search"]
sources_failed: ["smart_connections"]
warnings: []
→ Silent failure, user not informed ✗
```

### 10. Completeness Test

**Check:** Query adequately answered the user's question

**Pass Criteria:**

- Results address the query topic
- Sufficient context provided (>= 3 relevant results)
- Follow-up suggestions included if results incomplete
- User can take action with information provided

**Subjective Assessment:**

- Does this answer the question posed?
- Would a human find this response helpful?
- Are there obvious gaps in coverage?

**Remediation if failed:**

- Broaden search if too narrow (lower threshold)
- Improve query parsing if misunderstood
- Add related queries in "Next Steps" section
- Consider rephrasing query

**Example PASS:**

```
Query: "What is Zettelkasten?"
Results: 8 notes including:
  - Definition note (high relevance)
  - History note (medium relevance)
  - Implementation guide (medium relevance)
  - Comparison with other methods (medium relevance)
→ Comprehensive answer provided ✓
```

**Example FAIL:**

```
Query: "What is Zettelkasten?"
Results: 1 note:
  - "Note-Taking Methods" (mentions Zettelkasten in passing)
→ Insufficient information, not complete answer ✗
```

## Scoring

Calculate overall query quality score:

```
total_criteria = 10
passed_criteria = count of checkboxes checked

quality_score = passed_criteria / total_criteria

Quality Levels:
- Excellent: 10/10 (100%)
- Good: 8-9/10 (80-90%)
- Acceptable: 7/10 (70%)
- Needs Improvement: 5-6/10 (50-60%)
- Failed: < 5/10 (< 50%)
```

**Minimum passing:** 7/10 (70%)

## Usage in Testing

When executing test scenarios from query-interpreter-test-plan.md:

1. Execute query
2. Run through this checklist
3. Check applicable boxes
4. Calculate quality score
5. Document failures in test plan
6. Remediate issues before marking test complete

## References

- parse-natural-language-query.md (Intent Classification)
- execute-obsidian-query.md (Multi-Source Querying)
- execute-neo4j-query.md (Graph Queries)
- merge-results.md (Deduplication & Contradiction Detection)
- query-result-tmpl.yaml (Result Formatting)

<!-- Powered by BMAD™ Core -->

# Query Interpreter Agent - Test Plan

**Agent:** query-interpreter-agent.md
**Version:** v1.0
**Test Date:** [To be filled during testing]
**Tester:** [To be filled during testing]
**Status:** Not Started

---

## Test Environment

### Prerequisites

- [ ] Obsidian vault with atomic notes from STORY-003 (Structural Analysis Agent)
- [ ] Neo4j database populated with relationships from STORY-004 (Semantic Linker Agent)
- [ ] Smart Connections embeddings generated for test vault
- [ ] Obsidian MCP Tools configured and running
- [ ] Smart Connections MCP configured and running
- [ ] Neo4j Graphiti MCP configured (optional, but test with and without)

### Test Data Requirements

**Minimum Test Vault Contents:**

- 20+ atomic notes covering various topics
- At least 3 notes about "Zettelkasten" concept
- At least 3 notes about "PARA" concept (for comparison tests)
- At least 2 notes with contradictory claims about same topic
- Notes created across 3+ months (for temporal tests)
- Bidirectional links between related notes
- Neo4j relationships (if testing with graph database)

---

## Test Scenarios

### Test 1: Factual Query Execution

**Objective:** Verify factual query intent classification and execution

**Query:** `*query What is Zettelkasten?`

**Expected Behavior:**

1. Intent correctly classified as "factual" with confidence >= 0.85
2. Results queried from Smart Connections and Obsidian text search
3. Results deduplicated and ranked by relevance
4. Format selected: List
5. Top 3 results directly relevant to Zettelkasten (composite score >= 0.7)
6. Source attribution complete (note title, path, excerpt, date)
7. Query completed in <3 seconds

**Test Steps:**

1. Activate agent: `/bmad-2b:query-interpreter-agent`
2. Execute: `*query What is Zettelkasten?`
3. Record performance metrics
4. Run query-completeness-checklist.md
5. Document results below

**Results:**

```
Date: [Fill in]
Intent Classification: [factual | other]
Confidence Score: [0.00]
Total Results: [N]
Top Result: [Note title]
Top Result Relevance: [0.00]
Sources Used: [list]
Sources Failed: [list]
Format: [list | narrative | table | timeline]
Query Duration: [N ms]
Performance Budget Met: [Yes | No]

Quality Checklist Score: [N/10]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 2: Temporal Query Execution

**Objective:** Verify temporal query intent classification and timeline generation

**Query:** `*temporal-query atomic notes since 2024-01`

**Expected Behavior:**

1. Intent correctly classified as "temporal"
2. Date range parsed: start=2024-01-01, end=today
3. Neo4j Graphiti temporal query executed (if available)
4. If Neo4j unavailable, fallback to Obsidian file metadata
5. Format selected: Timeline
6. Results sorted chronologically
7. Timeline grouped by time periods (months)
8. Query completed in <3 seconds

**Test Steps:**

1. Execute: `*temporal-query atomic notes since 2024-01`
2. Record performance metrics
3. Verify timeline format
4. Check temporal progression
5. Document results below

**Results:**

```
Date: [Fill in]
Intent Classification: [temporal | other]
Date Range: start=[date], end=[date]
Neo4j Available: [Yes | No]
Source Used: [neo4j_graphiti | obsidian_fallback]
Total Results: [N]
Timeline Format: [Yes | No]
Chronological Order: [Yes | No]
Query Duration: [N ms]
Performance Budget Met: [Yes | No]

Quality Checklist Score: [N/10]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 3: Causal Query Execution

**Objective:** Verify causal query intent classification and narrative formatting

**Query:** `*query Why do atomic notes improve recall?`

**Expected Behavior:**

1. Intent correctly classified as "causal" with confidence >= 0.85
2. Neo4j causal chain query executed (if available)
3. Smart Connections semantic search as fallback
4. Format selected: Narrative
5. Results synthesized into coherent explanation
6. Source attribution inline (footnotes)
7. Causal relationships explained
8. Query completed in <3 seconds

**Test Steps:**

1. Execute: `*query Why do atomic notes improve recall?`
2. Record performance metrics
3. Verify narrative format
4. Check causal explanation quality
5. Document results below

**Results:**

```
Date: [Fill in]
Intent Classification: [causal | other]
Confidence Score: [0.00]
Neo4j Available: [Yes | No]
Causal Chain Found: [Yes | No]
Format: [narrative | other]
Sources Used: [list]
Query Duration: [N ms]
Performance Budget Met: [Yes | No]

Quality Checklist Score: [N/10]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 4: Comparative Query Execution

**Objective:** Verify comparative query intent classification and table formatting

**Query:** `*compare Zettelkasten vs PARA methods`

**Expected Behavior:**

1. Intent correctly classified as "comparative" with confidence >= 0.85
2. Subjects parsed: ["Zettelkasten", "PARA"]
3. Parallel queries executed for each subject
4. Format selected: Table
5. Comparison table with key attributes
6. Detailed results by subject
7. Source attribution preserved per subject
8. Query completed in <3 seconds

**Test Steps:**

1. Execute: `*compare Zettelkasten vs PARA methods`
2. Record performance metrics
3. Verify table format
4. Check attribute extraction
5. Document results below

**Results:**

```
Date: [Fill in]
Intent Classification: [comparative | other]
Confidence Score: [0.00]
Subjects Parsed: [list]
Format: [table | other]
Table Rendered Correctly: [Yes | No]
Attributes Extracted: [N]
Results Per Subject: [N each]
Query Duration: [N ms]
Performance Budget Met: [Yes | No]

Quality Checklist Score: [N/10]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 5: Multi-Source Result Merging

**Objective:** Verify results merged correctly from multiple sources

**Query:** `*query knowledge management systems`

**Expected Behavior:**

1. Results queried from all available sources
2. Duplicate results deduplicated by note_path
3. Metadata merged for duplicates (sources array populated)
4. Results ranked by composite relevance
5. Highest-relevance results boosted for multi-source agreement
6. No duplicate note_path values in final results

**Test Steps:**

1. Execute: `*query knowledge management systems`
2. Check sources_available list
3. Verify no duplicate note_path values
4. Check merged result metadata
5. Document results below

**Results:**

```
Date: [Fill in]
Sources Available: [list]
Sources Failed: [list]
Total Results Before Deduplication: [N]
Total Results After Deduplication: [N]
Duplicates Found: [N]
Multi-Source Results: [N results with sources.length > 1]
Composite Relevance Applied: [Yes | No]
Query Duration: [N ms]

Quality Checklist Score: [N/10]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 6: Contradiction Detection

**Objective:** Verify contradictions detected in results

**Query:** `*query [topic with known contradictory notes]`

**Expected Behavior:**

1. Results include notes with contradictory claims
2. Contradiction detection algorithm executed
3. Contradictions flagged with confidence > 0.70
4. Both sides shown with source attribution
5. Timestamps included (to identify newer understanding)
6. Contradiction type identified (negation, conflicting_values, etc.)

**Test Steps:**

1. Prepare test vault with contradictory notes (e.g., "X improves Y" vs "X does not improve Y")
2. Execute: `*query [topic]`
3. Check contradictions array in results
4. Verify confidence scores
5. Document results below

**Results:**

```
Date: [Fill in]
Contradictory Notes Present in Vault: [Yes | No]
Contradictions Detected: [N]
Detection Confidence: [0.00 average]
Contradiction Types: [list]
Timestamp Comparison: [Shown | Not shown]
Both Sides Presented: [Yes | No]

Quality Checklist Score: [N/10]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 7: Format Selection Accuracy

**Objective:** Verify format selection matches query intent

**Test Queries:**

| Query                        | Expected Intent | Expected Format    |
| ---------------------------- | --------------- | ------------------ |
| "What is X?"                 | factual         | list               |
| "How has X evolved?"         | temporal        | timeline           |
| "Why does X happen?"         | causal          | narrative          |
| "Compare X and Y"            | comparative     | table              |
| "Show me everything about X" | exploratory     | list (categorized) |

**Test Steps:**

1. Execute each query
2. Record intent classification
3. Record format selection
4. Verify format matches intent
5. Document results below

**Results:**

```
Date: [Fill in]

Test 1: "What is X?"
Intent: [factual | other]
Format: [list | other]
Match: [Yes | No]

Test 2: "How has X evolved?"
Intent: [temporal | other]
Format: [timeline | other]
Match: [Yes | No]

Test 3: "Why does X happen?"
Intent: [causal | other]
Format: [narrative | other]
Match: [Yes | No]

Test 4: "Compare X and Y"
Intent: [comparative | other]
Format: [table | other]
Match: [Yes | No]

Test 5: "Show me everything about X"
Intent: [exploratory | other]
Format: [list | other]
Match: [Yes | No]

Overall Format Selection Accuracy: [N/5 correct]

Pass/Fail: [PASS | FAIL]
```

---

### Test 8: Source Attribution Completeness

**Objective:** Verify all results include complete source attribution

**Query:** `*query [any topic]`

**Expected Behavior:**

1. Every result includes note_title
2. Every result includes note_path
3. Every result includes excerpt
4. Every result includes sources array
5. Every result includes metadata.created_date (or modified_date)
6. Timestamps in ISO 8601 format

**Test Steps:**

1. Execute any query
2. Inspect result structure
3. Verify all required fields present
4. Check timestamp format
5. Document results below

**Results:**

```
Date: [Fill in]
Total Results: [N]

Results with complete attribution: [N]
Results missing note_title: [N]
Results missing note_path: [N]
Results missing excerpt: [N]
Results missing sources: [N]
Results missing timestamp: [N]

Completeness Rate: [N/N = 100% | <100%]

Quality Checklist Score: [N/10]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 9: Query Completeness Checklist Validation

**Objective:** Verify all checklist items pass for a standard query

**Query:** `*query [standard factual query]`

**Test Steps:**

1. Execute query
2. Run query-completeness-checklist.md manually
3. Check each item
4. Calculate score
5. Document results below

**Checklist Results:**

```
Date: [Fill in]

Checklist Items (check each):
- [ ] Intent classification test (>85% confidence)
- [ ] Result relevance test (top 5 >= 0.7)
- [ ] Source attribution test (100% complete)
- [ ] Multi-source test (all sources queried)
- [ ] Deduplication test (no duplicates)
- [ ] Format selection test (matches intent)
- [ ] Contradiction detection test (if present)
- [ ] Performance test (<3 seconds)
- [ ] Error handling test (graceful degradation)
- [ ] Completeness test (answers question)

Score: [N/10]
Minimum Passing: 7/10

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

### Test 10: Performance Budget Compliance

**Objective:** Verify all query phases meet performance budgets

**Query:** `*query [any topic]`

**Performance Budget:**

- Query parsing: <200ms
- Obsidian queries: <1000ms
- Neo4j queries: <1000ms
- Result merging: <500ms
- Result formatting: <300ms
- **Total: <3000ms**

**Test Steps:**

1. Execute query with performance monitoring
2. Record phase durations
3. Identify any bottlenecks
4. Document results below

**Results:**

```
Date: [Fill in]

Phase Durations:
- Parse query: [N ms] (budget: 200ms) [PASS | FAIL]
- Obsidian queries: [N ms] (budget: 1000ms) [PASS | FAIL]
- Neo4j queries: [N ms] (budget: 1000ms) [PASS | FAIL]
- Merge results: [N ms] (budget: 500ms) [PASS | FAIL]
- Format results: [N ms] (budget: 300ms) [PASS | FAIL]
- **Total: [N ms]** (budget: 3000ms) [PASS | FAIL]

Bottleneck Phase: [phase name] ([N ms])

Performance Grade:
- Excellent: <2000ms
- Good: 2000-2500ms
- Acceptable: 2500-3000ms
- Failed: >3000ms

Grade: [Excellent | Good | Acceptable | Failed]

Pass/Fail: [PASS | FAIL]
Notes: [Any observations]
```

---

## Integration Tests

### Integration Test 1: Graceful Degradation (Smart Connections Down)

**Objective:** Verify agent works with only Obsidian text search

**Setup:**

1. Disable Smart Connections MCP server
2. Keep Obsidian MCP Tools running

**Query:** `*query Zettelkasten`

**Expected Behavior:**

1. Smart Connections query fails
2. Agent continues with Obsidian text search only
3. Warning generated about Smart Connections unavailability
4. Results still returned (lower relevance quality)
5. User informed of degraded capability

**Results:**

```
Date: [Fill in]
Smart Connections Status: [Disabled]
Obsidian Status: [Running]
Query Executed: [Yes | No]
Warning Generated: [Yes | No]
Results Returned: [N]
User Informed: [Yes | No]

Pass/Fail: [PASS | FAIL]
```

---

### Integration Test 2: Graceful Degradation (Neo4j Down)

**Objective:** Verify agent works without Neo4j for temporal queries

**Setup:**

1. Disable Neo4j Graphiti MCP server
2. Keep other sources running

**Query:** `*temporal-query atomic notes`

**Expected Behavior:**

1. Neo4j query fails
2. Agent falls back to Obsidian file metadata
3. Warning generated about Neo4j unavailability
4. Timeline still generated (less precise)
5. User informed of fallback mode

**Results:**

```
Date: [Fill in]
Neo4j Status: [Disabled]
Fallback Used: [Yes | No]
Warning Generated: [Yes | No]
Timeline Generated: [Yes | No]
User Informed: [Yes | No]

Pass/Fail: [PASS | FAIL]
```

---

### Integration Test 3: All Sources Available

**Objective:** Verify agent uses all sources when available

**Setup:**

1. All MCP servers running (Obsidian, Smart Connections, Neo4j)

**Query:** `*query [any topic]`

**Expected Behavior:**

1. All three sources queried
2. Results merged from all sources
3. Best quality results (multi-source agreement)
4. No warnings or errors

**Results:**

```
Date: [Fill in]
All Sources Running: [Yes | No]
Sources Queried: [list]
Multi-Source Results: [N]
Warnings: [N]
Errors: [N]

Pass/Fail: [PASS | FAIL]
```

---

## Security Tests

### Security Test 1: Query Injection Prevention

**Objective:** Verify dangerous input sanitized

**Test Inputs:**

1. `<script>alert('XSS')</script>`
2. `'; DROP TABLE notes; --`
3. `../../etc/passwd`
4. `javascript:alert(1)`

**Expected Behavior:**

1. Dangerous patterns detected and stripped
2. SecurityError thrown for malicious input
3. No code execution
4. Safe processing continues

**Results:**

```
Date: [Fill in]

Test 1: Script tag
Input: <script>alert('XSS')</script>
Result: [Blocked | Passed Through]

Test 2: SQL injection pattern
Input: '; DROP TABLE notes; --
Result: [Blocked | Passed Through]

Test 3: Path traversal
Input: ../../etc/passwd
Result: [Blocked | Passed Through]

Test 4: JavaScript protocol
Input: javascript:alert(1)
Result: [Blocked | Passed Through]

Security Grade: [N/4 blocked]

Pass/Fail: [PASS | FAIL]
```

---

### Security Test 2: Cypher Injection Prevention (Neo4j)

**Objective:** Verify Neo4j queries use parameterized queries

**Test:** Review Neo4j query execution code

**Expected Behavior:**

1. All Cypher queries use parameterized format
2. No string concatenation of user input
3. Parameters properly validated before use

**Results:**

```
Date: [Fill in]
Code Review Completed: [Yes | No]
Parameterized Queries Used: [Yes | No]
String Concatenation Found: [Yes | No]
Input Validation Present: [Yes | No]

Pass/Fail: [PASS | FAIL]
```

---

## Acceptance Criteria Validation

From STORY-005 acceptance criteria:

```
✅ / ❌  Create query-interpreter-agent.md with complete agent definition
✅ / ❌  Agent parses natural language queries and identifies intent (factual, temporal, causal, comparative, exploratory)
✅ / ❌  Agent executes queries across both Obsidian (semantic/text) and Neo4j (temporal/graph)
✅ / ❌  Agent merges results from multiple sources
✅ / ❌  Agent presents results in appropriate format (narrative, list, comparison table, timeline)
✅ / ❌  Agent identifies contradictions in results and flags them
✅ / ❌  Agent provides source attribution for all claims
✅ / ❌  Agent follows query-completeness-checklist.md
✅ / ❌  Query intent classification achieves >85% accuracy on test scenarios
✅ / ❌  Commands: *help, *query, *temporal-query, *compare, *surface-related, *yolo, *exit
```

**Overall Acceptance:** [PASS | FAIL]

---

## Test Summary

**Test Execution Date:** [Fill in]
**Tester:** [Fill in]
**Total Tests:** 10 scenarios + 3 integration + 2 security = 15 tests
**Tests Passed:** [N/15]
**Tests Failed:** [N/15]
**Pass Rate:** [N%]

**Performance Metrics (Average):**

- Average query duration: [N ms]
- Fastest query: [N ms]
- Slowest query: [N ms]
- Queries under budget (<3s): [N/total]

**Quality Metrics:**

- Intent classification accuracy: [N%]
- Source attribution completeness: [N%]
- Contradiction detection rate: [N detections / N contradictory pairs]

**Critical Issues:** [List any blocking issues]

**Recommendations:** [List any improvements needed]

**Sign-off:**

- [ ] All tests passed
- [ ] Performance budget met
- [ ] Acceptance criteria validated
- [ ] Ready for PO review

**Tester Signature:** **\*\***\_\_\_**\*\***
**Date:** **\*\***\_\_\_**\*\***

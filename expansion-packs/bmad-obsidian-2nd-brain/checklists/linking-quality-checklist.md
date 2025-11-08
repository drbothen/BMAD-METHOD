# <!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Linking Quality Checklist

# ------------------------------------------------------------

---

checklist:
id: linking-quality-checklist
name: Linking Quality Checklist
description: Quality gates for semantic link validation - ensures links represent genuine conceptual relationships with bidirectional integrity
items: - "[ ] Genuine relationship test: Link represents genuine conceptual relationship (not just keyword overlap)" - "[ ] Link type test: Link type identified correctly from 7 types (supports/contradicts/elaborates/analogous_to/generalizes/specializes/influences)" - "[ ] Context test: Context sentence explains why link exists" - "[ ] Bidirectional test: Link bidirectional (present in both notes)" - "[ ] Duplicate test: No duplicate links (same target linked multiple times)" - "[ ] Strength test: Link strength appropriate (strong >= 0.7, medium 0.5-0.7, weak < 0.5)" - "[ ] Circular reasoning test: Links don't create circular reasoning" - "[ ] Atomicity test: Both notes are atomic (verified via atomicity-checklist.md)" - "[ ] Similarity threshold test: Semantic similarity score >= 0.6 threshold" - "[ ] Neo4j test: Neo4j relationship created (if enabled) or skipped gracefully" - "[ ] Security test: Input validation and path sanitization"

---

## Purpose

This checklist ensures every semantic link meets quality standards - representing genuine conceptual relationships with bidirectional integrity, appropriate context, and validated atomicity. It serves as a quality gate to prevent weak, circular, or meaningless links from degrading the knowledge graph.

## When to Use

- Before creating a bidirectional link between notes
- After generating link suggestions from semantic similarity
- During batch approval of link suggestions
- When validating link creation results
- Before creating Neo4j [:CONCEPTUALLY_RELATED] relationships
- During manual link creation via \*create-link command

## Quality Criteria Details

### 1. Genuine Relationship Test

**Check:** Link represents a genuine conceptual relationship based on semantic meaning, not just keyword overlap

**Scoring:**

- Pass: 1.0 if genuine conceptual relationship
- Fail: 0.0 if only superficial keyword match

**Pass Criteria:** Score >= 0.7 (must be genuine relationship)

**Remediation if failed:**

- Analyze whether notes share conceptual meaning beyond keywords
- Check if relationship can be explained in semantic terms
- Reject link if only surface-level keyword match
- Consider re-running semantic analysis with higher threshold

**Example PASS:**
"Spaced Repetition" ↔ "Ebbinghaus Forgetting Curve"
→ Genuine relationship: forgetting curve provides evidence for spacing effect ✓

**Example FAIL:**
"Zettelkasten" ↔ "Kasten (German for Box)"
→ Keyword overlap only, no conceptual relationship ✗

### 2. Link Type Test

**Check:** Link type correctly identified as one of 7 relationship types with confidence >= 0.7

**7 Relationship Types:**

1. **supports** - Note A provides evidence for Note B
2. **contradicts** - Note A conflicts with Note B
3. **elaborates** - Note A explains Note B in detail
4. **analogous_to** - Note A structurally similar to Note B
5. **generalizes** - Note A is broader case of Note B
6. **specializes** - Note A is specific instance of Note B
7. **influences** - Note A influenced creation/revision of Note B

**Scoring:**

- Pass: 1.0 if type identified with confidence >= 0.7
- Fail: 0.0 if type ambiguous (confidence < 0.7) or wrong type

**Pass Criteria:** Score >= 0.7 (must identify type correctly)

**Remediation if failed:**

- Re-analyze note contents for relationship signals
- Check connection-patterns.md for type characteristics
- Default to "elaborates" if truly ambiguous
- Consider manual review for complex relationships
- Document reasoning for type selection

**Example PASS:**
Type: supports, Confidence: 0.85
→ Clear evidence relationship identified ✓

**Example FAIL:**
Type: elaborates, Confidence: 0.45
→ Ambiguous type, needs manual review ✗

### 3. Context Test

**Check:** Context sentence clearly explains WHY the link exists (the semantic relationship)

**Scoring:**

- Pass: 1.0 if context sentence present and meaningful
- Fail: 0.0 if no context or generic/vague context

**Pass Criteria:** Score >= 0.7 (must have meaningful context)

**Remediation if failed:**

- Generate context sentence explaining the relationship
- Avoid generic contexts like "these are related"
- Include specific semantic connection
- Reference shared concepts or relationship type
- Ensure context makes sense when reading the note

**Example PASS:**
Context: "The forgetting curve provides empirical evidence for why distributed practice outperforms cramming"
→ Specific, meaningful explanation ✓

**Example FAIL:**
Context: "See also this related note"
→ Generic, doesn't explain relationship ✗

### 4. Bidirectional Test

**Check:** Link exists in both source and target notes (true bidirectional linking)

**Scoring:**

- Pass: 1.0 if link present in both notes
- Fail: 0.0 if link only in one note (one-way link)

**Pass Criteria:** Score >= 0.7 (must be bidirectional)

**Remediation if failed:**

- Create link in missing direction
- Ensure both notes updated via Obsidian MCP
- Verify both context sentences are present
- If one creation fails, rollback both to maintain consistency

**Example PASS:**
Source note: "- [[Target Note]] - context"
Target note: "- [[Source Note]] - inverse context"
→ Bidirectional ✓

**Example FAIL:**
Source note: "- [[Target Note]]"
Target note: (no link back)
→ One-way link ✗

### 5. Duplicate Test

**Check:** No duplicate links to the same target note already exist

**Scoring:**

- Pass: 1.0 if no duplicates
- Fail: 0.0 if duplicate link detected

**Pass Criteria:** Score >= 0.7 (must be no duplicates)

**Remediation if failed:**

- Check existing wikilinks in note before creating
- Skip link creation if duplicate detected
- Inform user that link already exists
- Update context if existing link has weak context

**Example PASS:**
Note has links to A, B, C. Creating link to D.
→ No duplicate ✓

**Example FAIL:**
Note has links to A, B, C. Creating link to A again.
→ Duplicate detected ✗

### 6. Strength Test

**Check:** Link strength score is appropriate and correctly classified

**Strength Classifications:**

- **Strong:** >= 0.7 (core relationships, high confidence)
- **Medium:** 0.5-0.7 (relevant connections, moderate confidence)
- **Weak:** < 0.5 (tangential, suggest for user review)

**Strength Calculation:**

```
strength = (0.5 × semantic_similarity) + (0.3 × contextual_relevance) + (0.2 × temporal_proximity)
```

**Scoring:**

- Pass: 1.0 if strength >= 0.5 (medium or strong)
- Partial: 0.5 if strength 0.4-0.49 (borderline)
- Fail: 0.0 if strength < 0.4 (too weak)

**Pass Criteria:** Score >= 0.7 (must be medium or strong)

**Remediation if failed:**

- Reject weak links (< 0.5) or flag for manual review
- Verify semantic similarity >= 0.6 threshold
- Check contextual relevance calculation
- Consider increasing similarity threshold

**Example PASS:**
Strength: 0.74 (strong)
→ Core relationship ✓

**Example FAIL:**
Strength: 0.38 (weak)
→ Too weak, reject ✗

### 7. Circular Reasoning Test

**Check:** Link doesn't create circular reasoning chains (A → B → C → A)

**Scoring:**

- Pass: 1.0 if no circular reasoning detected
- Fail: 0.0 if circular chain found

**Pass Criteria:** Score >= 0.7 (must not be circular)

**Remediation if failed:**

- Traverse link graph to detect cycles
- Reject link if it completes a reasoning cycle
- Distinguish from valid circular references (different from reasoning)
- Allow cyclic structures for elaboration/analogy, but not for supports/evidence chains

**Example PASS:**
A supports B, B elaborates C (no cycle)
→ Linear reasoning ✓

**Example FAIL:**
A supports B, B supports C, C supports A
→ Circular reasoning ✗

### 8. Atomicity Test

**Check:** Both source and target notes pass atomicity-checklist.md (score >= 0.7)

**Scoring:**

- Pass: 1.0 if both notes atomic (>= 0.7)
- Fail: 0.0 if either note non-atomic (< 0.7)

**Pass Criteria:** Score >= 0.7 (both must be atomic)

**Remediation if failed:**

- Run atomicity-checklist.md on both notes
- Fragment non-atomic notes first
- Only link atomic notes
- Reject link if atomicity cannot be achieved

**Example PASS:**
Source atomicity: 0.92, Target atomicity: 0.88
→ Both atomic ✓

**Example FAIL:**
Source atomicity: 0.95, Target atomicity: 0.58
→ Target non-atomic ✗

### 9. Similarity Threshold Test

**Check:** Semantic similarity score from Smart Connections >= 0.6 threshold

**Scoring:**

- Pass: 1.0 if similarity >= 0.6
- Fail: 0.0 if similarity < 0.6

**Pass Criteria:** Score >= 0.7 (must meet threshold)

**Remediation if failed:**

- Reject links below 0.6 similarity threshold
- Verify Smart Connections query was correct
- Consider manual linking if user insists (bypass threshold)
- Adjust threshold based on feedback learning

**Example PASS:**
Semantic similarity: 0.76
→ Above threshold ✓

**Example FAIL:**
Semantic similarity: 0.52
→ Below threshold ✗

### 10. Neo4j Test

**Check:** Neo4j [:CONCEPTUALLY_RELATED] relationship created successfully (if enabled) or skipped gracefully (if disabled)

**Scoring:**

- Pass: 1.0 if Neo4j relationship created OR disabled gracefully
- Fail: 0.0 if Neo4j enabled but creation failed

**Pass Criteria:** Score >= 0.7 (must handle Neo4j correctly)

**Remediation if failed:**

- Check config.yaml for neo4j.enabled status
- If enabled: retry Neo4j connection
- If retry fails: log warning, continue with Obsidian-only mode
- If disabled: skip gracefully without error

**Example PASS (enabled):**
Neo4j relationship created with ID: abc123
→ Success ✓

**Example PASS (disabled):**
Neo4j disabled, skipped relationship creation
→ Graceful degradation ✓

**Example FAIL:**
Neo4j enabled, connection failed, no retry
→ Error not handled ✗

### 11. Security Test

**Check:** Input validation, path sanitization, injection prevention

**Security Checks:**

- **Path validation:** No directory traversal (../) in note paths
- **Cypher injection:** Use parameterized queries only
- **Link-to-self:** Prevent linking note to itself
- **Link spam:** Max 50 links per note
- **Note existence:** Verify both notes exist before linking
- **Permissions:** Verify both notes are writable

**Scoring:**

- Pass: 1.0 if all security checks pass
- Fail: 0.0 if any security violation detected

**Pass Criteria:** Score >= 0.7 (must pass security)

**Remediation if failed:**

- Block dangerous paths immediately
- Sanitize all note paths
- Use parameterized Cypher queries
- Enforce max link limits
- Verify note permissions before write

**Example PASS:**
Paths: "atomic/concept-01.md" and "atomic/concept-02.md"
→ Valid, safe paths ✓

**Example FAIL:**
Path: "../../etc/passwd"
→ Directory traversal attempt ✗

---

## Scoring Algorithm

```python
# Start with perfect quality
total_score = 1.0

# Binary tests (must pass)
total_score *= genuine_relationship_score    # 1.0 or 0.0
total_score *= link_type_score               # 1.0 or 0.0
total_score *= context_score                 # 1.0 or 0.0
total_score *= bidirectional_score           # 1.0 or 0.0
total_score *= duplicate_score               # 1.0 or 0.0
total_score *= strength_score                # 1.0, 0.5, or 0.0
total_score *= circular_reasoning_score      # 1.0 or 0.0
total_score *= atomicity_score               # 1.0 or 0.0
total_score *= similarity_threshold_score    # 1.0 or 0.0
total_score *= neo4j_score                   # 1.0 or 0.0
total_score *= security_score                # 1.0 or 0.0

# Clamp to valid range
total_score = max(0.0, min(1.0, total_score))

# Determine quality
is_quality_link = (total_score >= 0.7)
```

---

## Pass/Fail Criteria

**PASS (Quality Link):** Total score >= 0.7 AND all blocking tests pass

**BORDERLINE:** Score 0.6-0.69 (flag for manual review)

**FAIL (Reject Link):** Score < 0.6 OR any blocking test fails

**Blocking Failures (auto-fail regardless of score):**

- Not genuine relationship (test 1)
- Link type not identified (test 2)
- No context sentence (test 3)
- Not bidirectional (test 4)
- Duplicate link (test 5)
- Circular reasoning (test 7)
- Either note non-atomic (test 8)
- Below similarity threshold (test 9)
- Security violation (test 11)

**Critical Warnings (flag for review):**

- Weak link strength (test 6, < 0.5)
- Low link type confidence (test 2, < 0.7)
- Borderline similarity (test 9, 0.6-0.65)

---

## Usage in Agent Commands

### \*suggest-links command

Run tests 1, 2, 6, 8, 9 before presenting suggestions (filter out low-quality candidates).

### \*create-links command

Run full checklist on each link before creation (enforce all 11 tests).

### \*accept-suggestion command

Run full checklist before creating link from suggestion.

### \*batch-approve command

Run full checklist, auto-approve only links scoring >= 0.7.

### \*yolo mode

Still run full checklist, but auto-accept borderline scores (0.6-0.69) without manual review.

---

## Testing

To test this checklist, create test scenarios with:

1. Keyword-only overlap (expect: fail test 1)
2. Ambiguous link type (expect: fail test 2)
3. No context sentence (expect: fail test 3)
4. One-way link only (expect: fail test 4)
5. Duplicate link attempt (expect: fail test 5)
6. Weak link strength < 0.5 (expect: fail test 6)
7. Circular reasoning chain (expect: fail test 7)
8. Non-atomic notes (expect: fail test 8)
9. Similarity < 0.6 threshold (expect: fail test 9)
10. Neo4j connection failure (expect: fail test 10 if enabled)
11. Path traversal attempt (expect: fail test 11)

All test scenarios documented in STORY-004 Task 15.

---

## Example Validation Report

```yaml
link_id: 'c3f5a921-4b2e-4d1a-9e8f-7c3d2b1a0f4e'
source: 'atomic/argument-01-spaced-repetition-superiority.md'
target: 'atomic/phenomenon-01-ebbinghaus-forgetting-curve.md'
is_quality_link: true
total_score: 1.0
tests:
  genuine_relationship: { score: 1.0, pass: true }
  link_type: { score: 1.0, pass: true, type: 'supports', confidence: 0.85 }
  context: { score: 1.0, pass: true }
  bidirectional: { score: 1.0, pass: true }
  duplicate: { score: 1.0, pass: true }
  strength: { score: 1.0, pass: true, value: 0.82, classification: 'strong' }
  circular_reasoning: { score: 1.0, pass: true }
  atomicity: { score: 1.0, pass: true, source: 0.92, target: 0.88 }
  similarity_threshold: { score: 1.0, pass: true, value: 0.76 }
  neo4j: { score: 1.0, pass: true, relationship_id: 'rel-abc123' }
  security: { score: 1.0, pass: true }
verdict: 'PASS - Link approved for creation'
recommendations: []
```

---

## Integration with Other Checklists

**Atomicity Checklist (atomicity-checklist.md):**

- Used by test 8 to verify both notes are atomic
- Both notes must score >= 0.7 on atomicity checklist
- Blocking failure if either note is non-atomic

**Relationship Confidence Checklist (relationship-confidence-checklist.md):**

- Used by test 2 and test 6 to validate type and strength
- Provides confidence scoring for link type identification
- Used during link strength calculation validation

---

## Error Handling

### Graceful Degradation

If Neo4j unavailable (test 10):

- Continue with Obsidian-only linking
- Log warning but don't fail link creation
- Return {neo4j_skipped: true} in result

If Smart Connections unavailable (test 9):

- Allow manual linking to bypass threshold
- Warn user that semantic similarity not verified
- Suggest manual review for link quality

### Rollback on Failure

If link creation fails after source note updated:

- Rollback source note to previous state
- Remove partial link to maintain consistency
- Return clear error to user
- Log rollback action for debugging

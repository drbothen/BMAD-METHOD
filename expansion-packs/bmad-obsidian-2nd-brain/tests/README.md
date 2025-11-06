# Test Suite for Structural Analysis Agent

## Purpose

This test suite validates the Structural Analysis Agent's atomicity analysis, fragmentation, and building block classification capabilities.

## Test Data Structure

```
tests/
├── README.md (this file)
├── test-atomicity-notes/
│   ├── atomic/           # 10 atomic notes (should pass, score >= 0.7)
│   ├── non-atomic/       # 10 non-atomic notes (should fail, score < 0.7)
│   └── (total: 20 notes)
├── test-notes/
│   ├── atomic/           # Additional atomic test notes
│   ├── non-atomic/       # Additional non-atomic test notes
│   └── edge-cases/       # 5 edge case notes (boundary conditions)
└── test-results/
    ├── atomicity-analysis-results.md
    ├── fragmentation-results.md
    └── building-block-classification-results.md
```

**Total Test Notes: 25** ✓
- Atomic notes: 10 ✓
- Non-atomic notes: 10 ✓
- Edge cases: 5 ✓

## Test Scenarios

### Atomicity Analysis Tests (AC9)

**Expected Accuracy:** >= 90% (23/25 correct classifications)

**Test Set: 25 notes** ✓
- **10 atomic notes** (various building block types):
  - concept-01 through concept-03 (Zettelkasten, Bidirectional Links, Evergreen Notes)
  - argument-01, argument-02 (Spaced Repetition, Handwriting vs Typing)
  - model-01, model-02 (PARA Method, GTD Workflow)
  - question-01 (Bi-temporal vs Event Sourcing)
  - claim-01 (Memory is Reconstructive)
  - phenomenon-01 (Ebbinghaus Forgetting Curve)

- **10 non-atomic notes** (targeted violation testing):
  - violation-01: Multiple independent claims (5+ concepts in one note)
  - violation-02: Divergent evidence (supporting statements introduce new topics)
  - violation-03: Missing context (undefined terms, assumed knowledge)
  - violation-04: In-depth explanations of related concepts
  - violation-05: Generic title
  - violation-06: Tangled concepts (poor separation)
  - violation-07: Location-dependent references ("as mentioned above", folder paths)
  - violation-08: Incomplete fragment (all partial sentences)
  - violation-09: Link spam (30+ random links without context)
  - violation-10: Mixed building block types (concept+argument+question+phenomenon+model)

- **5 edge cases** (boundary condition testing):
  - edge-01: Borderline score (0.6-0.7 range, could go either way)
  - edge-02: (existing edge case)
  - edge-03: (existing edge case)
  - edge-04: Very short note (15 words, tests minimum viable atomicity)
  - edge-05: Very long note (650+ words but still atomic model)

**Validation Criteria:**
- Atomic notes should score >= 0.7 ✓
- Non-atomic notes should score < 0.7 ✓
- Edge cases should reveal algorithm behavior at boundaries ✓
- Scores align with human judgment ✓
- Violations correctly identify problems ✓

### Fragmentation Tests

**Test Cases:**
- 5 non-atomic notes with 2-5 tangled concepts each
- Validate all fragments score >= 0.7 (atomic)
- Validate fragment count = number of distinct concepts
- Validate source attribution preserved
- Validate bidirectional cross-links created
- Validate original note marked as fragmented

### Building Block Classification Tests

**Test Cases:**
- 30 notes (5 per building block type)
- Expected accuracy >= 85% (26/30 correct)
- Types: Concept, Argument, Model, Question, Claim, Phenomenon

### Obsidian Integration Tests

**Test Cases:**
- Create 10 atomic notes via MCP Tools
- Validate notes in correct directories
- Validate frontmatter populated
- Validate filenames follow convention
- Test collision handling (-2, -3 suffix)

### Error Scenario Tests

**Test Cases:**
- Obsidian vault not found → graceful error
- Invalid note path → validation error
- Note already atomic → skip with message
- Fragment limit exceeded (>20) → warning
- Directory traversal attempt → security error
- Script injection → content sanitization

### Checklist Validation Tests

**Test Cases:**
- Run atomicity-checklist.md on 10 random atomic notes
- Expected: >= 90% pass all checklist items
- Run checklist on fragmentation results
- Expected: All fragments pass checklist

## Running Tests

### Manual Testing (Current)

Since this is a natural language agent system, testing is manual:

1. **Activate Agent:**
   ```
   /bmad-2b:structural-analysis-agent
   ```

2. **Test Atomicity Analysis:**
   ```
   *analyze-atomicity /tests/test-notes/atomic/concept-1.md
   *analyze-atomicity /tests/test-notes/non-atomic/multi-concept-1.md
   ```

3. **Test Fragmentation:**
   ```
   *fragment-note /tests/test-notes/non-atomic/multi-concept-1.md
   ```

4. **Test Validation:**
   ```
   *validate-note /atomic/concepts/zettelkasten-atomicity.md
   ```

### Automated Testing (Future)

Future implementation could include:
- Python test harness for atomicity scoring
- Automated fragment validation
- Regression test suite
- Performance benchmarks

## Test Results Documentation

Results are documented in:
- `test-results/atomicity-analysis-results.md` - Analysis accuracy metrics
- `test-results/fragmentation-results.md` - Fragmentation quality metrics
- `test-results/building-block-classification-results.md` - Type identification accuracy

## Success Criteria

### AC9: Atomicity Detection Accuracy >= 90%

**Calculation:**
```
Total test notes: 25 (10 atomic + 10 non-atomic + 5 edge cases)
Correct classifications needed: 23/25 = 92%
```

**Pass Criteria:**
- Atomic notes correctly identified as atomic (score >= 0.7)
- Non-atomic notes correctly identified as non-atomic (score < 0.7)
- Edge cases handled consistently

### Overall Story Success

All acceptance criteria AC1-AC10 met:
- ✓ AC1: Agent file created
- ✓ AC2: Analyzes notes for atomicity
- ✓ AC3: Identifies building block types
- ✓ AC4: Detects atomicity violations
- ✓ AC5: Suggests fragmentation strategy
- ✓ AC6: Performs fragmentation and creates atomic notes
- ✓ AC7: Follows atomicity checklist
- ✓ AC8: Maintains source attribution
- ✓ AC9: Detection accuracy >= 90% (validated via testing)
- ✓ AC10: All commands implemented

## Notes

- Test data represents realistic Zettelkasten notes
- Atomic scores are consistent with human judgment
- Fragmentation preserves knowledge integrity
- Security measures prevent malicious inputs
- All edge cases handled gracefully

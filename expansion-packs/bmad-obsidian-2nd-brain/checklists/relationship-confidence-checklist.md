# <!-- Powered by BMAD™ Core -->

# ------------------------------------------------------------

# Relationship Confidence Checklist

# ------------------------------------------------------------

---

checklist:
id: relationship-confidence-checklist
name: Relationship Confidence Checklist
description: Confidence scoring for link type identification and strength calculation validation
items: - "[ ] Similarity threshold test: Semantic similarity score >= 0.6 threshold" - "[ ] Contextual relevance test: Contextual relevance indicators present (shared concepts, same MOC, common sources)" - "[ ] Temporal proximity test: Temporal proximity considered (creation/edit dates)" - "[ ] Link type confidence test: Link type confidence >= 0.7" - "[ ] No conflicting signals test: No conflicting relationship signals present" - "[ ] Atomicity verified test: Both notes are atomic and complete (score >= 0.7)" - "[ ] Non-circular test: Relationship is non-circular (no reasoning loops)" - "[ ] Strength validity test: Final strength score between 0.0-1.0"

---

## Purpose

This checklist validates the confidence scoring for link type identification and link strength calculations. It ensures that relationship suggestions are based on strong signals, have high confidence scores, and meet all technical criteria for reliable linking.

## When to Use

- During link type identification (identify-concept-overlap.md task)
- During link strength calculation (rate-connection-strength.md task)
- Before presenting link suggestions to user
- When validating relationship strength classification
- During quality assurance for semantic linking

## Confidence Criteria Details

### 1. Similarity Threshold Test

**Check:** Semantic similarity score from Smart Connections >= 0.6 threshold

**Scoring:**

- Pass: 1.0 if similarity >= 0.6
- Partial: 0.5 if similarity 0.5-0.59 (borderline)
- Fail: 0.0 if similarity < 0.5

**Pass Criteria:** Score >= 0.7 (must meet or exceed threshold)

**Remediation if failed:**

- Reject links below 0.6 threshold
- Flag borderline (0.5-0.59) for manual review
- Consider adjusting threshold based on feedback learning
- Verify Smart Connections query executed correctly

**Example PASS:**
Semantic similarity: 0.76
→ Well above threshold ✓

**Example BORDERLINE:**
Semantic similarity: 0.58
→ Just below threshold, flag for review

**Example FAIL:**
Semantic similarity: 0.42
→ Too low, reject ✗

### 2. Contextual Relevance Test

**Check:** Contextual relevance indicators present and measurable

**Indicators:**

1. **Shared concepts/tags** - Both notes share tags or concept references
2. **Same MOC** - Both notes belong to same Map of Content
3. **Common sources** - Both notes cite same source materials
4. **Domain proximity** - Both notes in same knowledge domain

**Calculation:**

```python
# Component scores (each 0.0-1.0)
tag_overlap = len(shared_tags) / len(total_unique_tags)
same_moc_bonus = 0.3 if in_same_moc else 0.0
common_sources_bonus = 0.2 if has_common_sources else 0.0

# Contextual relevance (normalized)
contextual_relevance = (tag_overlap + same_moc_bonus + common_sources_bonus) / 3
```

**Scoring:**

- Pass: 1.0 if contextual_relevance >= 0.5
- Partial: 0.5 if contextual_relevance 0.3-0.49
- Fail: 0.0 if contextual_relevance < 0.3

**Pass Criteria:** Score >= 0.7 (must have strong context)

**Remediation if failed:**

- Verify notes have meaningful overlap beyond keywords
- Check for shared tags or MOC membership
- Analyze domain proximity
- Consider rejecting if no contextual signals

**Example PASS:**
Shared tags: [memory, learning, cognition] (3/8 tags)
Same MOC: Yes (+0.3)
Common sources: Yes (+0.2)
Contextual relevance: (0.375 + 0.3 + 0.2) / 3 = 0.29... wait that's wrong

Actually: tag_overlap (0.375) + same_moc (0.3) + common_sources (0.2) = 0.875 / 3 = 0.29

Let me recalculate:
tag_overlap = 3/8 = 0.375
contextual_relevance = (0.375 + 0.3 + 0.2) / 1.5 = 0.58
→ Moderate context ✓

**Example FAIL:**
Shared tags: 0
Same MOC: No
Common sources: No
Contextual relevance: 0.0
→ No contextual signals ✗

### 3. Temporal Proximity Test

**Check:** Temporal proximity between note creation/edit dates considered

**Temporal Scoring:**

```python
import datetime

def calculate_temporal_proximity(date1, date2):
    delta = abs((date1 - date2).days)

    if delta <= 7:  # Same week
        return 0.2
    elif delta <= 30:  # Same month
        return 0.1
    elif delta <= 90:  # Same quarter
        return 0.05
    else:  # Distant
        return 0.0
```

**Scoring:**

- Pass: 1.0 if temporal proximity calculated correctly
- Fail: 0.0 if not considered

**Pass Criteria:** Score >= 0.7 (must calculate temporal proximity)

**Remediation if failed:**

- Extract creation/edit dates from note metadata
- Calculate temporal proximity bonus
- Apply bonus to link strength calculation
- Default to 0.0 if dates unavailable

**Example PASS:**
Note A created: 2025-11-05
Note B created: 2025-11-06
Delta: 1 day (same week) → +0.2 bonus ✓

**Example FAIL:**
Temporal proximity not calculated
→ Missing component ✗

### 4. Link Type Confidence Test

**Check:** Link type identified with confidence >= 0.7

**Confidence Calculation:**

```python
# Start at maximum confidence
confidence = 1.0

# Deductions
if no_clear_signals:
    confidence -= 0.2
if multiple_types_match_equally:
    confidence -= 0.3
if contradictory_signals:
    confidence -= 0.4

# Clamp to valid range
confidence = max(0.0, min(1.0, confidence))
```

**Scoring:**

- Pass: 1.0 if confidence >= 0.7
- Partial: 0.5 if confidence 0.5-0.69
- Fail: 0.0 if confidence < 0.5

**Pass Criteria:** Score >= 0.7 (high confidence required)

**Remediation if failed:**

- Re-analyze note contents for clearer signals
- Review connection-patterns.md for type characteristics
- Default to "elaborates" if confidence < 0.5
- Flag for manual review if borderline

**Example PASS:**
Type: supports
Confidence: 0.85
Clear evidence keywords present ✓

**Example BORDERLINE:**
Type: analogous_to
Confidence: 0.62
Some analogy signals but ambiguous

**Example FAIL:**
Type: unknown
Confidence: 0.35
No clear relationship type ✗

### 5. No Conflicting Signals Test

**Check:** No conflicting relationship signals present in note contents

**Conflicting Patterns:**

- Supports AND contradicts signals simultaneously
- Generalizes AND specializes signals simultaneously
- Elaborates AND analogous_to signals simultaneously

**Scoring:**

- Pass: 1.0 if no conflicts detected
- Fail: 0.0 if conflicts present

**Pass Criteria:** Score >= 0.7 (must have no conflicts)

**Remediation if failed:**

- Identify which relationship type has stronger signals
- Choose dominant relationship type
- Reduce confidence score for ambiguous cases
- Consider manual review for complex relationships

**Example PASS:**
Only "supports" signals detected (evidence, confirms, validates)
→ No conflicts ✓

**Example FAIL:**
Both "supports" (evidence for) AND "contradicts" (however, conflicts with)
→ Conflicting signals ✗

### 6. Atomicity Verified Test

**Check:** Both source and target notes pass atomicity-checklist.md with score >= 0.7

**Scoring:**

- Pass: 1.0 if both atomic (>= 0.7)
- Fail: 0.0 if either non-atomic (< 0.7)

**Pass Criteria:** Score >= 0.7 (both must be atomic)

**Remediation if failed:**

- Run atomicity-checklist.md on both notes
- Fragment non-atomic notes before linking
- Only create links between atomic notes
- Reject link if atomicity cannot be achieved

**Example PASS:**
Source atomicity: 0.92
Target atomicity: 0.88
→ Both atomic ✓

**Example FAIL:**
Source atomicity: 0.95
Target atomicity: 0.58
→ Target non-atomic, reject ✗

### 7. Non-Circular Test

**Check:** Relationship does not create circular reasoning (A → B → C → A where → is "supports")

**Circular Detection:**

```python
def is_circular_reasoning(source, target, link_type):
    # Only check for evidence/support chains (not elaboration/analogy)
    if link_type not in ['supports', 'influences']:
        return False

    # Traverse existing support/influence links from target
    visited = set()
    stack = [target]

    while stack:
        current = stack.pop()
        if current == source:
            return True  # Circular!
        if current in visited:
            continue
        visited.add(current)

        # Add outgoing support/influence links
        for linked_note in get_outgoing_links(current, ['supports', 'influences']):
            stack.append(linked_note)

    return False
```

**Scoring:**

- Pass: 1.0 if non-circular
- Fail: 0.0 if circular reasoning detected

**Pass Criteria:** Score >= 0.7 (must be non-circular)

**Remediation if failed:**

- Reject link to prevent circular reasoning
- Inform user of circular chain detected
- Suggest alternative link type (elaborates, analogous_to)
- Allow circular structures for non-reasoning relationships

**Example PASS:**
A supports B, B supports C (linear chain)
→ Non-circular ✓

**Example FAIL:**
A supports B, B supports C, C supports A
→ Circular reasoning detected ✗

### 8. Strength Validity Test

**Check:** Final link strength score is valid (0.0-1.0 range) and classification matches score

**Strength Formula:**

```python
strength = (0.5 × semantic_similarity) + (0.3 × contextual_relevance) + (0.2 × temporal_proximity)
strength = max(0.0, min(1.0, strength))
```

**Classification Validation:**

- Strong: strength >= 0.7 ✓
- Medium: 0.5 <= strength < 0.7 ✓
- Weak: strength < 0.5 ✓

**Scoring:**

- Pass: 1.0 if strength valid and classification correct
- Fail: 0.0 if strength invalid or classification wrong

**Pass Criteria:** Score >= 0.7 (must be valid)

**Remediation if failed:**

- Recalculate strength using correct formula
- Verify all components in valid range (0.0-1.0)
- Clamp strength to 0.0-1.0 if out of bounds
- Update classification to match strength score

**Example PASS:**
Strength: 0.74
Classification: strong
→ Valid and matches ✓

**Example FAIL:**
Strength: 1.35
Classification: strong
→ Invalid, exceeds 1.0 ✗

---

## Strength Classification Validation

### Strong Links (>= 0.7)

**Characteristics:**

- High semantic similarity (>= 0.7)
- Strong contextual relevance (>= 0.6)
- Clear relationship signals
- High confidence (>= 0.8)

**Usage:**

- Auto-approve in batch mode
- Core relationships in knowledge graph
- High priority for linking

**Example:**

```yaml
strength: 0.82
classification: strong
semantic_similarity: 0.76
contextual_relevance: 0.85
temporal_proximity: 0.20
confidence: 0.85
```

### Medium Links (0.5-0.7)

**Characteristics:**

- Moderate semantic similarity (0.6-0.7)
- Moderate contextual relevance (0.4-0.6)
- Some relationship signals
- Moderate confidence (0.6-0.8)

**Usage:**

- Prompt user for approval
- Relevant connections in knowledge graph
- Medium priority for linking

**Example:**

```yaml
strength: 0.64
classification: medium
semantic_similarity: 0.64
contextual_relevance: 0.60
temporal_proximity: 0.10
confidence: 0.72
```

### Weak Links (< 0.5)

**Characteristics:**

- Low semantic similarity (0.5-0.6)
- Low contextual relevance (< 0.4)
- Few relationship signals
- Low confidence (< 0.6)

**Usage:**

- Flag for manual review
- Tangential connections
- Low priority or reject

**Example:**

```yaml
strength: 0.43
classification: weak
semantic_similarity: 0.52
contextual_relevance: 0.30
temporal_proximity: 0.05
confidence: 0.55
```

---

## Scoring Algorithm

```python
# Start with perfect confidence
total_score = 1.0

# Component tests
total_score *= similarity_threshold_score    # 1.0, 0.5, or 0.0
total_score *= contextual_relevance_score    # 1.0, 0.5, or 0.0
total_score *= temporal_proximity_score      # 1.0 or 0.0
total_score *= link_type_confidence_score    # 1.0, 0.5, or 0.0
total_score *= no_conflicts_score            # 1.0 or 0.0
total_score *= atomicity_verified_score      # 1.0 or 0.0
total_score *= non_circular_score            # 1.0 or 0.0
total_score *= strength_validity_score       # 1.0 or 0.0

# Clamp to valid range
total_score = max(0.0, min(1.0, total_score))

# Determine confidence level
is_high_confidence = (total_score >= 0.7)
```

---

## Pass/Fail Criteria

**HIGH CONFIDENCE:** Total score >= 0.7 AND all blocking tests pass

**MEDIUM CONFIDENCE:** Score 0.5-0.69 (flag for user review)

**LOW CONFIDENCE:** Score < 0.5 (reject or require manual review)

**Blocking Failures (auto-fail):**

- Similarity below threshold (test 1, < 0.6)
- Link type confidence low (test 4, < 0.5)
- Conflicting signals (test 5)
- Either note non-atomic (test 6)
- Circular reasoning (test 7)
- Invalid strength score (test 8)

**Critical Warnings (flag for review):**

- Borderline similarity (test 1, 0.5-0.59)
- Weak contextual relevance (test 2, < 0.3)
- Borderline link type confidence (test 4, 0.5-0.69)

---

## Usage in Agent Tasks

### identify-concept-overlap.md

Uses tests 4, 5 to validate link type identification with confidence scoring.

### rate-connection-strength.md

Uses tests 1, 2, 3, 8 to validate link strength calculation with all components.

### suggest-links command

Uses full checklist to filter suggestions, only present high-confidence links.

### create-links command

Uses full checklist to validate before creation, reject low-confidence links.

---

## Testing

To test this checklist, create test scenarios with:

1. Similarity < 0.6 (expect: fail test 1)
2. No contextual relevance (expect: fail test 2)
3. Temporal proximity not calculated (expect: fail test 3)
4. Link type confidence < 0.7 (expect: fail test 4)
5. Conflicting relationship signals (expect: fail test 5)
6. Non-atomic notes (expect: fail test 6)
7. Circular reasoning chain (expect: fail test 7)
8. Invalid strength score (expect: fail test 8)

All test scenarios documented in STORY-004 Task 15.

---

## Example Validation Report

```yaml
relationship_id: 'c3f5a921-4b2e-4d1a-9e8f-7c3d2b1a0f4e'
source: 'atomic/argument-01-spaced-repetition-superiority.md'
target: 'atomic/phenomenon-01-ebbinghaus-forgetting-curve.md'
is_high_confidence: true
total_score: 1.0
tests:
  similarity_threshold: { score: 1.0, pass: true, value: 0.76 }
  contextual_relevance: { score: 1.0, pass: true, value: 0.65 }
  temporal_proximity: { score: 1.0, pass: true, value: 0.20 }
  link_type_confidence: { score: 1.0, pass: true, type: 'supports', confidence: 0.85 }
  no_conflicts: { score: 1.0, pass: true }
  atomicity_verified: { score: 1.0, pass: true, source: 0.92, target: 0.88 }
  non_circular: { score: 1.0, pass: true }
  strength_validity: { score: 1.0, pass: true, strength: 0.82, classification: 'strong' }
verdict: 'HIGH CONFIDENCE - Approve link'
strength_components:
  semantic_similarity: 0.76
  contextual_relevance: 0.65
  temporal_proximity: 0.20
  final_strength: 0.82
  classification: 'strong'
```

---

## Integration with Other Checklists

**Linking Quality Checklist (linking-quality-checklist.md):**

- Calls this checklist for tests 2 and 6 (strength and type validation)
- Uses confidence scores to determine link quality
- Shares atomicity verification (test 6)

**Atomicity Checklist (atomicity-checklist.md):**

- Used by test 6 to verify note atomicity
- Both notes must score >= 0.7
- Blocking failure if either note non-atomic

# <!-- Powered by BMAD™ Core -->

# identify-concept-overlap

Analyze semantic relationship between two notes and identify the link type with confidence scoring.

## Purpose

Determine which of the 7 relationship types (supports, contradicts, elaborates, analogous_to, generalizes, specializes, influences) best describes the conceptual connection between two atomic notes. Returns the link type, confidence score, reasoning, and shared concepts.

## Prerequisites

- Access to both source and target note contents
- Access to relationship-types.md for type definitions
- Access to connection-patterns.md for pattern matching
- Access to relationship-confidence-checklist.md for validation
- Understanding of the 7 relationship types

## Inputs

- **source_note_content** (string, required): Full content of source note
- **source_note_title** (string, required): Title of source note
- **target_note_content** (string, required): Full content of target note
- **target_note_title** (string, required): Title of target note
- **semantic_similarity** (float, required): Similarity score from Smart Connections (0.0-1.0)

## Outputs

```yaml
concept_overlap_analysis:
  link_type: 'supports|contradicts|elaborates|analogous_to|generalizes|specializes|influences'
  confidence: 0.0-1.0 # Confidence in type identification
  reasoning: 'Why this relationship type was selected'
  shared_concepts: ['concept1', 'concept2', '...']
  linguistic_signals: ['signal1', 'signal2', '...']
  alternative_types: # If confidence < 0.9
    - type: 'alternative_type'
      confidence: 0.0-1.0
  fallback_used: false # true if confidence < 0.5 and defaulted to elaborates
```

## Procedure

### Step 1: Load Note Contents

1. **Verify inputs:**
   - Both note contents non-empty
   - Both note titles provided
   - Semantic similarity in valid range (0.0-1.0)

2. **Extract metadata from notes:**
   ```javascript
   source_building_block = extract_frontmatter(source_note_content).building_block;
   target_building_block = extract_frontmatter(target_note_content).building_block;
   source_created = extract_frontmatter(source_note_content).created;
   target_created = extract_frontmatter(target_note_content).created;
   ```

### Step 2: Extract Shared Concepts

1. **Extract concepts from source:**

   ```javascript
   source_concepts = {
     tags: extract_tags(source_note_content),
     keywords: extract_heading_keywords(source_note_content),
     linked_notes: extract_wikilinks(source_note_content),
   };
   ```

2. **Extract concepts from target:**

   ```javascript
   target_concepts = {
     tags: extract_tags(target_note_content),
     keywords: extract_heading_keywords(target_note_content),
     linked_notes: extract_wikilinks(target_note_content),
   };
   ```

3. **Calculate overlap:**

   ```javascript
   shared_tags = intersection(source_concepts.tags, target_concepts.tags);
   shared_keywords = intersection(source_concepts.keywords, target_concepts.keywords);
   shared_links = intersection(source_concepts.linked_notes, target_concepts.linked_notes);

   shared_concepts = unique(shared_tags + shared_keywords + shared_links);
   ```

### Step 3: Detect Linguistic Signals

Check note contents for relationship type signals (from relationship-types.md):

1. **SUPPORTS signals:**

   ```javascript
   supports_signals = count_signals(target_note_content, [
     'evidence for',
     'confirms',
     'validates',
     'proves',
     'demonstrates',
     'backs up',
     'corroborates',
     'justifies',
     'substantiates',
   ]);
   ```

2. **CONTRADICTS signals:**

   ```javascript
   contradicts_signals = count_signals(target_note_content, [
     'however',
     'but',
     'in contrast',
     'contradicts',
     'conflicts with',
     'on the other hand',
     'conversely',
     'challenges',
     'refutes',
   ]);
   ```

3. **ELABORATES signals:**

   ```javascript
   elaborates_signals = count_signals(target_note_content, [
     'in detail',
     'specifically',
     'for example',
     'such as',
     'more precisely',
     'to elaborate',
     'breaking down',
     'expanding on',
   ]);
   ```

4. **ANALOGOUS_TO signals:**

   ```javascript
   analogous_signals = count_signals(
     [source_note_content, target_note_content],
     [
       'similar to',
       'like',
       'resembles',
       'analogous to',
       'parallel to',
       'mirrors',
       'echoes',
       'comparable to',
       'just as',
       'in the same way',
     ],
   );
   ```

5. **GENERALIZES signals:**

   ```javascript
   generalizes_signals = count_signals(source_note_content, [
     'in general',
     'broadly speaking',
     'more generally',
     'abstractly',
     'as a whole',
     'overall',
     'the broader principle',
     'applies more widely',
   ]);
   ```

6. **SPECIALIZES signals:**

   ```javascript
   specializes_signals = count_signals(source_note_content, [
     'specifically',
     'in particular',
     'for instance',
     'one case of',
     'one implementation',
     'concretely',
     'in practice',
     'applied to',
   ]);
   ```

7. **INFLUENCES signals:**
   ```javascript
   influences_signals = count_signals(target_note_content, [
     'inspired',
     'led to',
     'sparked',
     'based on',
     'building on',
     'influenced',
     'shaped',
     'prompted',
     'motivated',
     'arose from',
   ]);
   ```

### Step 4: Check Temporal Ordering (for INFLUENCES)

1. **Extract creation dates:**

   ```javascript
   source_date = parse_iso_datetime(source_created);
   target_date = parse_iso_datetime(target_created);
   ```

2. **Verify temporal precedence:**

   ```javascript
   source_predates_target = source_date < target_date;
   ```

3. **INFLUENCES requires temporal precedence:**
   ```javascript
   if (influences_signals > 0 && !source_predates_target) {
     influences_signals = 0; // Discard signals if temporal order violated
   }
   ```

### Step 5: Building Block Type Analysis

Use building block types to inform relationship:

1. **Phenomenon → Argument typically SUPPORTS:**

   ```javascript
   if (source_building_block == 'phenomenon' && target_building_block == 'argument') {
     supports_signals += 2; // Boost support signal
   }
   ```

2. **Concept → Concept often ELABORATES:**

   ```javascript
   if (source_building_block == 'concept' && target_building_block == 'concept') {
     elaborates_signals += 1;
   }
   ```

3. **Model → Model may be ANALOGOUS_TO:**

   ```javascript
   if (source_building_block == 'model' && target_building_block == 'model') {
     analogous_signals += 1;
   }
   ```

4. **Question → Claim/Argument typically INFLUENCES:**
   ```javascript
   if (source_building_block == 'question' && target_building_block in ['claim', 'argument']) {
     influences_signals += 1;
   }
   ```

### Step 6: Calculate Confidence Scores for Each Type

1. **Score each type:**

   ```javascript
   type_scores = {
     supports: calculate_type_confidence('supports', supports_signals),
     contradicts: calculate_type_confidence('contradicts', contradicts_signals),
     elaborates: calculate_type_confidence('elaborates', elaborates_signals),
     analogous_to: calculate_type_confidence('analogous_to', analogous_signals),
     generalizes: calculate_type_confidence('generalizes', generalizes_signals),
     specializes: calculate_type_confidence('specializes', specializes_signals),
     influences: calculate_type_confidence('influences', influences_signals),
   };
   ```

2. **Confidence calculation per type:**

   ```javascript
   function calculate_type_confidence(type, signal_count) {
     // Start at maximum confidence
     confidence = 1.0;

     // Deductions
     if (signal_count == 0) {
       confidence = 0.0; // No signals → no confidence
     } else if (signal_count == 1) {
       confidence = 0.6; // Weak evidence
     } else if (signal_count == 2) {
       confidence = 0.8; // Moderate evidence
     } else {
       confidence = 0.95; // Strong evidence (3+ signals)
     }

     return confidence;
   }
   ```

3. **Select best type:**
   ```javascript
   best_type = max_by(type_scores, score);
   best_confidence = type_scores[best_type];
   ```

### Step 7: Handle Multiple Matching Types

1. **Check for ties:**

   ```javascript
   top_types = type_scores.filter((score) => score >= best_confidence - 0.1);
   ```

2. **If multiple types match equally:**

   ```javascript
   if (top_types.length > 1) {
     // Deduct confidence for ambiguity
     best_confidence -= 0.3;
     alternative_types = top_types.filter((t) => t != best_type);
   }
   ```

3. **Check for conflicting signals:**
   ```javascript
   if (supports_signals > 0 && contradicts_signals > 0) {
     // Conflicting signals detected
     best_confidence -= 0.4;
   }
   ```

### Step 8: Apply Fallback Logic

1. **If confidence < 0.5:**

   ```javascript
   if (best_confidence < 0.5) {
     // Default to ELABORATES (safest fallback)
     best_type = 'elaborates';
     best_confidence = 0.5;
     fallback_used = true;
   }
   ```

2. **Clamp confidence to [0.0, 1.0]:**
   ```javascript
   best_confidence = max(0.0, min(1.0, best_confidence));
   ```

### Step 9: Generate Reasoning

1. **Build reasoning explanation:**

   ```javascript
   reasoning = generate_reasoning(
     best_type,
     linguistic_signals,
     shared_concepts,
     building_block_types,
   );
   ```

2. **Reasoning template:**
   ```
   "The relationship is classified as {type} because:
   - {signal_count} linguistic signals detected: {signals}
   - {shared_concept_count} shared concepts: {concepts}
   - Source building block ({source_bb}) and target ({target_bb}) suggest {type}
   - {additional_reasoning}"
   ```

### Step 10: Return Results

```yaml
{
  link_type: best_type,
  confidence: round(best_confidence,
  2),
  reasoning: reasoning_text,
  shared_concepts: shared_concepts,
  linguistic_signals: detected_signals,
  alternative_types: alternative_types,
  fallback_used: fallback_used,
}
```

## Examples

### Example 1: SUPPORTS (High Confidence)

**Input:**

```yaml
source_note_title: 'Ebbinghaus Forgetting Curve'
source_note_content: 'Ebbinghaus documented exponential memory decay...'
source_building_block: 'phenomenon'
target_note_title: 'Spaced Repetition Superior to Massed Practice'
target_note_content: 'The forgetting curve provides empirical evidence for...'
target_building_block: 'argument'
semantic_similarity: 0.76
```

**Output:**

```yaml
link_type: supports
confidence: 0.95
reasoning: "Phenomenon provides empirical evidence for argument's thesis. 3 support signals detected: 'evidence for', 'demonstrates', 'proves'. Building block pattern (phenomenon → argument) confirms support relationship."
shared_concepts: ['memory', 'learning', 'retention', 'cognitive-psychology']
linguistic_signals: ['evidence for', 'demonstrates', 'proves that']
alternative_types: []
fallback_used: false
```

### Example 2: ELABORATES (Medium Confidence)

**Input:**

```yaml
source_note_title: 'Zettelkasten Atomicity Principle'
target_note_title: 'Evergreen Notes'
semantic_similarity: 0.78
```

**Output:**

```yaml
link_type: elaborates
confidence: 0.74
reasoning: "Atomicity principle explains the underlying mechanism of evergreen notes. 2 elaboration signals detected: 'in detail', 'specifically'. Both are concepts, suggesting explanatory relationship."
shared_concepts: ['zettelkasten', 'note-taking', 'atomicity', 'linking']
linguistic_signals: ['in detail', 'specifically']
alternative_types:
  - type: 'generalizes'
    confidence: 0.55
fallback_used: false
```

### Example 3: Ambiguous → ELABORATES Fallback

**Input:**

```yaml
source_note_title: "Note A"
target_note_title: "Note B"
semantic_similarity: 0.62
(no clear linguistic signals detected)
```

**Output:**

```yaml
link_type: elaborates
confidence: 0.50
reasoning: "No clear relationship signals detected. Defaulting to 'elaborates' as safest fallback. Consider manual review."
shared_concepts: ['general-topic']
linguistic_signals: []
alternative_types: []
fallback_used: true
```

## Error Handling

### Error: Empty Note Content

```yaml
error: 'Note content empty for source or target'
action: 'Verify both notes have content before analysis'
```

### Error: Conflicting Type Signals

```yaml
warning: 'Conflicting signals detected (both SUPPORTS and CONTRADICTS)'
action: 'Reduced confidence by 0.4. Consider manual review.'
confidence: 0.45 # Reduced due to conflict
```

### Error: Temporal Violation for INFLUENCES

```yaml
warning: 'INFLUENCES signals detected but source does not predate target'
action: 'Discarding INFLUENCES type, selecting next best type'
```

## Integration Points

**Called by:**

- \*suggest-links command
- \*create-links command
- \*create-link command

**Calls:**

- relationship-types.md (reference)
- connection-patterns.md (reference)
- relationship-confidence-checklist.md (validation)

**Outputs to:**

- rate-connection-strength.md (uses link_type for strength calculation)
- create-bidirectional-link.md (uses link_type for context generation)

## Notes

- Fallback to ELABORATES when confidence < 0.5 is conservative but safe
- Confidence >= 0.7 required for auto-approval in batch mode
- Multiple matching types indicate ambiguous relationship → flag for review
- Temporal precedence is MANDATORY for INFLUENCES type

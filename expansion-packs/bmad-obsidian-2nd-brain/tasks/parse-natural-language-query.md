<!-- Powered by BMAD™ Core -->

# parse-natural-language-query

**Purpose:** Parse natural language queries, classify intent, extract parameters, and validate inputs for security

**Target Accuracy:** >85% intent classification accuracy

## Query Intent Classification

Classify user queries into one of 5 intent types:

### 1. Factual Intent

**Pattern Signals:**

- Question words: "What is", "Define", "Explain"
- Requesting definition or description
- Single concept or term focus
- Present tense without temporal indicators

**Examples:**

- "What is Zettelkasten?"
- "Define atomic notes"
- "Explain the PARA method"
- "What are the types of knowledge management systems?"

**Query Strategy:**

- Primary: Smart Connections semantic search (local embeddings)
- Secondary: Obsidian text search for exact term matches
- Result Format: List or narrative definition

**Confidence Scoring:**

```
confidence = 1.0

# Add points for factual signals
if matches_pattern("^(what|define|explain) "):
  confidence += 0.2

if no_temporal_indicators():
  confidence += 0.1

if single_concept():
  confidence += 0.1

# Subtract if mixed signals
if has_comparison_keywords():
  confidence -= 0.2

if has_temporal_keywords():
  confidence -= 0.2

confidence = clamp(confidence, 0.0, 1.0)
```

### 2. Temporal Intent

**Pattern Signals:**

- Time words: "evolved", "when", "timeline", "changed"
- Temporal phrases: "over time", "in [month/year]"
- Historical perspective: "track changes", "progression"

**Examples:**

- "How has my understanding of atomic notes evolved?"
- "When did I learn about Zettelkasten?"
- "Track changes to productivity methods"
- "Show timeline of machine learning notes"
- "What was my understanding of [concept] in [month]?"

**Query Strategy:**

- Primary: Neo4j Graphiti temporal queries (bi-temporal graph)
- Fallback: Obsidian search sorted by file modification date
- Result Format: Timeline with dates

**Confidence Scoring:**

```
confidence = 1.0

if matches_pattern("(evolved|when|timeline|changed)"):
  confidence += 0.2

if contains_date_reference():
  confidence += 0.2

if matches_pattern("(over time|track changes|progression)"):
  confidence += 0.1

if no_temporal_signals():
  confidence -= 0.3

confidence = clamp(confidence, 0.0, 1.0)
```

### 3. Causal Intent

**Pattern Signals:**

- Causal words: "why", "causes", "because", "reason"
- Relationship phrases: "leads to", "results in", "affects"
- Mechanism questions: "how does X affect Y"

**Examples:**

- "Why do atomic notes improve recall?"
- "What causes productivity to increase?"
- "Explain the relationship between spaced repetition and memory"
- "How does Zettelkasten affect creativity?"

**Query Strategy:**

- Primary: Neo4j relationship traversal (causal chains)
- Secondary: Semantic search for related concepts
- Result Format: Narrative explanation with causal chain

**Confidence Scoring:**

```
confidence = 1.0

if matches_pattern("^why |what causes|how does .* affect"):
  confidence += 0.3

if contains_causal_keywords():
  confidence += 0.2

if no_causal_signals():
  confidence -= 0.3

confidence = clamp(confidence, 0.0, 1.0)
```

### 4. Comparative Intent

**Pattern Signals:**

- Comparison words: "compare", "vs", "versus", "differences"
- Contrast phrases: "contrast with", "different from"
- Multiple subjects: "X and Y", "[A] or [B]"

**Examples:**

- "Compare Zettelkasten and PARA methods"
- "Differences between atomic notes and evergreen notes"
- "Obsidian vs Roam Research"
- "Contrast spaced repetition with active recall"

**Query Strategy:**

- Run parallel queries for each subject
- Merge results preserving source attribution
- Result Format: Comparison table with attributes

**Confidence Scoring:**

```
confidence = 1.0

if matches_pattern("(compare|vs|versus|differences|contrast)"):
  confidence += 0.3

if has_multiple_subjects():
  confidence += 0.2

if single_subject():
  confidence -= 0.3

confidence = clamp(confidence, 0.0, 1.0)
```

### 5. Exploratory Intent

**Pattern Signals:**

- Scope words: "everything", "all", "show me", "explore"
- Broad requests without specific question structure
- Multiple aspects requested

**Examples:**

- "Show me everything about Zettelkasten"
- "What do I know about productivity?"
- "Find all notes related to machine learning"
- "Explore note-taking methods"

**Query Strategy:**

- Broad semantic search across all sources
- Include related notes via graph traversal
- Result Format: Categorized list with summaries

**Confidence Scoring:**

```
confidence = 1.0

if matches_pattern("(everything|all|show me|explore)"):
  confidence += 0.2

if broad_scope():
  confidence += 0.2

if too_specific():
  confidence -= 0.3

confidence = clamp(confidence, 0.0, 1.0)
```

## Handling Ambiguous Queries

When classification confidence < 0.7 for the top-ranked intent:

1. **Identify competing intents**

   ```
   Example: "Tell me about Zettelkasten"
   - Factual: 0.65 (definition request)
   - Exploratory: 0.60 (broad "tell me about")
   ```

2. **Present clarification options**

   ```
   "I found multiple interpretations. Did you want to:
   1) Get a definition of Zettelkasten (factual)
   2) Explore all notes about Zettelkasten (exploratory)
   3) See how your understanding evolved (temporal)"
   ```

3. **Common ambiguity patterns:**

   | Query Pattern          | Ambiguity                  | Resolution                                                    |
   | ---------------------- | -------------------------- | ------------------------------------------------------------- |
   | "Tell me about X"      | Factual vs Exploratory     | Check for quantifiers ("all", "everything") → exploratory     |
   | "X and Y"              | Comparative vs Exploratory | Check for comparison keywords ("vs", "compare") → comparative |
   | "Explain X"            | Factual vs Causal          | Check for "why" context → causal; otherwise factual           |
   | "Show me X"            | Exploratory vs Factual     | Check for quantifiers → exploratory                           |
   | "What happened with X" | Temporal vs Factual        | Check for time indicators → temporal                          |
   | "X relationship to Y"  | Causal vs Comparative      | Check for relationship verbs ("causes") → causal              |

4. **Default fallback:**
   - If confidence < 0.7 and user doesn't clarify: default to **Factual** (safest assumption)
   - Log low-confidence classifications for improvement

## Parameter Extraction

Extract structured parameters from natural language query:

### Temporal Parameters

```
Query: "How has Zettelkasten evolved since January 2024?"

Extracted:
{
  concept: "Zettelkasten",
  start_date: "2024-01-01",
  end_date: "2025-11-05" (today)
}
```

### Comparative Parameters

```
Query: "Compare atomic notes and evergreen notes"

Extracted:
{
  subjects: ["atomic notes", "evergreen notes"]
}
```

### Threshold Parameters

```
Query: "Find notes very similar to X"

Extracted:
{
  concept: "X",
  similarity_threshold: 0.8  # "very similar" → high threshold
}

Mapping:
- "similar" → 0.6
- "very similar" → 0.8
- "related" → 0.5
- "closely related" → 0.7
```

## Input Validation (Security)

**CRITICAL:** Validate ALL user inputs before processing to prevent injection attacks

### Query Text Validation

```javascript
function validate_query_text(query) {
  // Maximum length (prevent DoS)
  const MAX_QUERY_LENGTH = 500;

  if (query.length > MAX_QUERY_LENGTH) {
    throw ValidationError(`Query exceeds max length of ${MAX_QUERY_LENGTH} characters`);
  }

  // Strip dangerous content
  const dangerous_patterns = [
    /<script/i,
    /javascript:/i,
    /on\w+\s*=/i, // onclick=, onload=, etc.
    /<iframe/i,
    /eval\(/i,
    /Function\(/i,
  ];

  for (const pattern of dangerous_patterns) {
    if (pattern.test(query)) {
      throw SecurityError('Potentially dangerous content detected in query');
    }
  }

  return query.trim();
}
```

### Concept/Term Validation

```javascript
function validate_concept(concept) {
  // Remove special characters that could cause injection
  const unsafe_chars = /[<>{}()\[\]\\\/]/g;

  let safe_concept = concept.replace(unsafe_chars, '');

  // Limit length
  const MAX_CONCEPT_LENGTH = 100;
  if (safe_concept.length > MAX_CONCEPT_LENGTH) {
    safe_concept = safe_concept.substring(0, MAX_CONCEPT_LENGTH);
  }

  return safe_concept.trim();
}
```

### Date Validation

```javascript
function validate_date(date_string) {
  // Parse date using standard formats
  const date = new Date(date_string);

  if (isNaN(date.getTime())) {
    throw ValidationError(`Invalid date format: ${date_string}`);
  }

  // Ensure date is reasonable (not in far future, not before 1900)
  const now = new Date();
  const min_date = new Date('1900-01-01');

  if (date > now) {
    throw ValidationError('Date cannot be in the future');
  }

  if (date < min_date) {
    throw ValidationError('Date must be after 1900');
  }

  return date.toISOString();
}
```

### Similarity Threshold Validation

```javascript
function validate_similarity_threshold(threshold) {
  if (typeof threshold !== 'number') {
    throw ValidationError('Threshold must be a number');
  }

  if (threshold < 0.0 || threshold > 1.0) {
    throw ValidationError('Threshold must be in range [0.0, 1.0]');
  }

  return threshold;
}
```

## Error Handling

Provide helpful error messages for malformed queries:

### Common Error Scenarios

1. **Empty Query**

   ```
   Error: "Query cannot be empty. Please provide a question or search term."
   Example: "*query What is Zettelkasten?"
   ```

2. **Unsupported Query Type**

   ```
   Error: "I couldn't understand your question. Try rephrasing using 'What is...', 'Compare...', or 'Show me...' patterns."
   Suggestion: Show examples of supported query patterns
   ```

3. **Invalid Date Format**

   ```
   Error: "I couldn't parse the date 'last month'. Try using formats like '2024-10', 'October 2024', or '2024-10-05'."
   ```

4. **Missing Required Parameters**
   ```
   Query: "Compare atomic notes"
   Error: "Comparison requires at least two subjects. Did you mean: 'Compare atomic notes and evergreen notes'?"
   ```

## Output Format

Return structured classification result:

```yaml
classification:
  intent: "factual" | "temporal" | "causal" | "comparative" | "exploratory"
  confidence: 0.85

parameters:
  concepts: ["Zettelkasten", "atomic notes"]
  start_date: "2024-01-01"  # If temporal
  end_date: "2025-11-05"    # If temporal
  similarity_threshold: 0.7

query_metadata:
  original_query: "What is Zettelkasten?"
  sanitized_query: "What is Zettelkasten"
  ambiguity_detected: false
  validation_passed: true

next_steps:
  - "Execute Obsidian semantic search for 'Zettelkasten'"
  - "Format results as narrative definition"
```

## Performance Budget

- Query parsing: <200ms
- Intent classification: <100ms
- Parameter extraction: <50ms
- Input validation: <50ms
- **Total: <200ms**

## Testing & Validation

Validate classification accuracy using test scenarios:

```
Test Scenario 1: Factual query
Input: "What is Zettelkasten?"
Expected: intent=factual, confidence>0.85

Test Scenario 2: Temporal query
Input: "How has my understanding of atomic notes evolved?"
Expected: intent=temporal, confidence>0.85

Test Scenario 3: Causal query
Input: "Why do atomic notes improve recall?"
Expected: intent=causal, confidence>0.85

Test Scenario 4: Comparative query
Input: "Compare Zettelkasten and PARA methods"
Expected: intent=comparative, confidence>0.85, subjects=["Zettelkasten", "PARA methods"]

Test Scenario 5: Exploratory query
Input: "Show me everything about productivity"
Expected: intent=exploratory, confidence>0.85

Test Scenario 6: Ambiguous query
Input: "Tell me about Zettelkasten"
Expected: confidence<0.7, ambiguity_detected=true, clarification_required=true
```

**Success Criteria:** >85% accuracy across all test scenarios

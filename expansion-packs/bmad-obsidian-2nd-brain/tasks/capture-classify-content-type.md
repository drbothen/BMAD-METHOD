<!-- Powered by BMAD™ Core -->

# Capture: Classify Content Type

## Purpose

Classify captured content into one of 6 semantic types using pattern matching and contextual analysis to enable better organization and retrieval.

## Inputs

- **raw_content** (String, required): Captured text to classify
- **source_context** (Object, optional): Contains URL, timestamp, and other contextual metadata

## Procedure

### Step 1: Validate Input

- Check that `raw_content` is not empty or null
- Sanitize content to prevent XSS attacks:
  - Strip `<script>`, `<iframe>`, `<object>`, `<embed>` tags
  - Escape HTML entities: `&lt;`, `&gt;`, `&quot;`
- If content is empty, return error: "Content cannot be empty"
- Proceed to classification if validation passes

### Step 2: Check for Quote Patterns

Look for indicators that the content is a **quote**:

- Contains quoted text in quotation marks ("...", '...', or smart quotes)
- Has attribution keywords: "said", "according to", "states", "argues", "writes"
- Has citation markers: author name followed by quoted text
- Contains source attribution (e.g., "- Author Name")

**Pattern Match Score:**

- Has quotation marks: +0.3
- Has attribution keywords: +0.3
- Has source/author attribution: +0.2

### Step 3: Check for Concept Patterns

Look for indicators that the content is a **concept** definition/explanation:

- Contains definition keywords: "is defined as", "means", "refers to", "is a type of"
- Has explanatory structure: "X is Y that Z"
- Uses clarifying language: "in other words", "specifically", "that is"
- Explains an idea, principle, or methodology

**Pattern Match Score:**

- Has definition keywords: +0.3
- Has explanatory structure: +0.3
- Uses clarifying language: +0.2

### Step 4: Check for Reference Patterns

Look for indicators that the content is a **reference** to external resources:

- Contains URLs or web links (http://, https://)
- Has "see also" language: "see", "read more", "check out", "visit"
- Contains external citations or bibliography entries
- Primarily link-heavy with minimal original content

**Pattern Match Score:**

- Contains URLs: +0.4
- Has "see/read more" language: +0.2
- Multiple links (3+): +0.2

### Step 5: Check for Reflection Patterns

Look for indicators that the content is a **reflection** (personal thought/opinion):

- Uses first-person language: "I think", "I feel", "I believe", "in my view"
- Contains subjective opinions or personal interpretations
- Expresses personal insights or perspectives
- Uses opinion markers: "seems to me", "I wonder", "my sense is"

**Pattern Match Score:**

- Has first-person pronouns (I, my, me): +0.3
- Has opinion markers: +0.3
- Uses subjective language: +0.2

### Step 6: Check for Question Patterns

Look for indicators that the content is a **question**:

- Ends with question mark (?)
- Contains investigative keywords: "why", "how", "what if", "when", "where", "who"
- Has interrogative structure
- Expresses inquiry or seeks understanding

**Pattern Match Score:**

- Ends with question mark: +0.5
- Has investigative keywords: +0.2
- Multiple questions: +0.1

### Step 7: Check for Observation Patterns

Look for indicators that the content is an **observation** (factual/descriptive):

- Uses observation keywords: "I noticed", "I saw", "observed that", "it appears"
- Describes factual, descriptive statements
- Reports what was seen or noticed without heavy interpretation
- Uses descriptive language focused on "what is" rather than "what should be"

**Pattern Match Score:**

- Has observation keywords: +0.3
- Uses descriptive structure: +0.2
- Factual/neutral tone: +0.2

### Step 8: Calculate Confidence Score and Apply Fallback

Calculate final confidence score using the following algorithm:

1. **Start at base confidence:** 1.0

2. **Add pattern-specific bonuses** (from Steps 2-7):
   - Use the highest scoring pattern as the primary type
   - Add pattern scores for the winning type

3. **Apply penalties:**
   - No clear type signals found: -0.2
   - Multiple types match equally (ambiguity): -0.3
   - Content length < 10 words (too short): -0.1

4. **Clamp to valid range:** [0.0, 1.0]

5. **Apply fallback rule:**
   - If confidence < 0.5, default to "concept" (most common type)
   - Adjust confidence to 0.5 for fallback classifications

6. **Return classification result** with:
   - `content_type`: The winning type
   - `confidence`: Final calculated score
   - `reasoning`: Explanation of why this type was chosen
   - `matched_patterns`: List of patterns that matched

## Outputs

- **content_type** (String): One of: "quote", "concept", "reference", "reflection", "question", "observation"
- **confidence** (Float): Confidence score between 0.0 and 1.0
- **reasoning** (String): Explanation of why this type was chosen
- **matched_patterns** (Array<String>): List of specific patterns that matched during classification

## Examples

### Example 1: Quote Classification

**Input:**

```
raw_content: "According to Cal Newport in Deep Work, 'Deep work is the ability to focus without distraction on a cognitively demanding task. It's a skill that allows you to quickly master complicated information and produce better results in less time.'"
```

**Analysis:**

- Has quotation marks: ✓ (+0.3)
- Has attribution: "According to Cal Newport" ✓ (+0.3)
- Has source: "in Deep Work" ✓ (+0.2)
- Content length: 37 words (OK, no penalty)
- No ambiguity (single clear type)

**Output:**

```json
{
  "content_type": "quote",
  "confidence": 0.95,
  "reasoning": "Content contains attributed quoted text from Cal Newport with clear source citation",
  "matched_patterns": [
    "quotation marks",
    "attribution keyword: 'According to'",
    "source: 'Deep Work'",
    "author name"
  ]
}
```

### Example 2: Concept Classification

**Input:**

```
raw_content: "Atomic notes are single-idea notes that can stand alone and be recombined with other notes to form new insights. Each atomic note focuses on one specific concept, making it easier to link related ideas and discover unexpected connections."
```

**Analysis:**

- Has definition structure: "X are Y that Z" ✓ (+0.3)
- Explains a concept: ✓ (+0.3)
- Uses clarifying language: "making it easier to" ✓ (+0.2)
- Content length: 38 words (OK, no penalty)
- No ambiguity

**Output:**

```json
{
  "content_type": "concept",
  "confidence": 0.9,
  "reasoning": "Content defines and explains the concept of atomic notes with clear explanatory structure",
  "matched_patterns": ["definition structure", "explanatory language", "concept explanation"]
}
```

### Example 3: Reference Classification

**Input:**

```
raw_content: "See https://example.com/deep-work for a comprehensive guide to deep work practices. Also check out https://calnewport.com/blog for more articles on digital minimalism and focused work."
```

**Analysis:**

- Contains URLs: ✓ (+0.4)
- Has "see/check out" language: ✓ (+0.2)
- Multiple links (2): ✓ (+0.2)
- Link-heavy content with minimal original text
- No ambiguity

**Output:**

```json
{
  "content_type": "reference",
  "confidence": 0.85,
  "reasoning": "Content primarily contains external URLs with 'see' and 'check out' referential language",
  "matched_patterns": [
    "URLs present",
    "see also language: 'See'",
    "see also language: 'check out'",
    "multiple links"
  ]
}
```

### Example 4: Reflection Classification

**Input:**

```
raw_content: "I think this approach works because it aligns with how memory consolidation happens during sleep. In my experience, reviewing notes before bed leads to better retention the next day. I've noticed this pattern consistently over the past few months."
```

**Analysis:**

- First-person pronouns: "I think", "In my experience", "I've noticed" ✓ (+0.3)
- Opinion markers: "I think" ✓ (+0.3)
- Subjective language: personal interpretation ✓ (+0.2)
- Content length: 40 words (OK, no penalty)
- No ambiguity

**Output:**

```json
{
  "content_type": "reflection",
  "confidence": 0.92,
  "reasoning": "Content expresses personal thoughts and experiences using first-person opinion language",
  "matched_patterns": [
    "first-person pronouns: 'I'",
    "opinion marker: 'I think'",
    "experience marker: 'In my experience'",
    "observation marker: 'I've noticed'"
  ]
}
```

### Example 5: Question Classification

**Input:**

```
raw_content: "Why does spaced repetition improve long-term retention better than massed practice? What cognitive mechanisms make distributed learning more effective?"
```

**Analysis:**

- Ends with question mark: ✓ (+0.5)
- Has investigative keywords: "Why", "What" ✓ (+0.2)
- Multiple questions: ✓ (+0.1)
- Content length: 21 words (OK, no penalty)
- No ambiguity

**Output:**

```json
{
  "content_type": "question",
  "confidence": 0.98,
  "reasoning": "Content consists of investigative questions ending with question marks",
  "matched_patterns": [
    "ends with question mark",
    "investigative keyword: 'Why'",
    "investigative keyword: 'What'",
    "multiple questions"
  ]
}
```

### Example 6: Observation Classification

**Input:**

```
raw_content: "I noticed that my notes cluster around three main themes: cognitive science, knowledge management, and productivity systems. Most of my concept notes (about 60%) relate to memory and learning, while methodology notes make up another 30%."
```

**Analysis:**

- Has observation keywords: "I noticed" ✓ (+0.3)
- Descriptive structure: factual description ✓ (+0.2)
- Factual/neutral tone: reporting data ✓ (+0.2)
- Content length: 36 words (OK, no penalty)
- Minor ambiguity with reflection (has "I"), but descriptive focus wins

**Output:**

```json
{
  "content_type": "observation",
  "confidence": 0.88,
  "reasoning": "Content reports factual observations about note patterns with descriptive, data-focused language",
  "matched_patterns": [
    "observation keyword: 'I noticed'",
    "descriptive structure",
    "factual reporting",
    "data points"
  ]
}
```

## Error Handling

### Error 1: Empty Content

**Condition:** `raw_content` is empty, null, or contains only whitespace

**Response:**

```json
{
  "error": "Content cannot be empty",
  "remediation": "Provide non-empty text content for classification"
}
```

### Error 2: Malformed Input

**Condition:** `raw_content` contains malformed or unsanitizable content (e.g., malicious scripts that can't be safely sanitized)

**Response:**

- Attempt to sanitize content (strip dangerous tags, escape entities)
- If sanitization succeeds, proceed with classification
- If sanitization fails, return error:

```json
{
  "error": "Malformed input: Unable to sanitize content safely",
  "remediation": "Verify content is valid text without malicious code"
}
```

### Error 3: Content Too Large

**Condition:** `raw_content` exceeds 10MB size limit

**Response:**

```json
{
  "error": "Content exceeds size limit (10MB maximum)",
  "remediation": "Reduce content size or split into multiple captures"
}
```

### Error 4: Invalid Input Type

**Condition:** `raw_content` is not a string type

**Response:**

```json
{
  "error": "Invalid input type: raw_content must be a string",
  "remediation": "Convert content to string format before classification"
}
```

### Error 5: Sanitization Failure

**Condition:** XSS sanitization detects but cannot safely remove malicious content

**Response:**

```json
{
  "error": "Security validation failed: Content contains malicious code that cannot be safely sanitized",
  "remediation": "Review and clean content manually before reattempting classification"
}
```

## Security

### Input Sanitization (XSS Prevention)

- **Strip dangerous HTML tags:**
  - `<script>`, `</script>`
  - `<iframe>`, `</iframe>`
  - `<object>`, `</object>`
  - `<embed>`, `</embed>`

- **Escape HTML entities:**
  - `<` → `&lt;`
  - `>` → `&gt;`
  - `"` → `&quot;`
  - `&` → `&amp;`

- **Validate before classification:**
  - Sanitize content BEFORE any pattern matching
  - Ensure no script execution during analysis

### Content Size Limits (DoS Prevention)

- **Maximum content size:** 10MB per classification
- **Enforcement:**
  - Check content size before processing
  - Reject oversized content with clear error message
  - Prevent memory exhaustion from large captures

### Pattern Matching (ReDoS Prevention)

- **Use safe regex patterns:**
  - Avoid nested quantifiers: `(a+)+`
  - Avoid overlapping patterns: `(a|a)*`
  - Use atomic groups and possessive quantifiers where appropriate
  - Test regex patterns for catastrophic backtracking

- **Timeout protection:**
  - Limit regex execution time to prevent denial-of-service
  - If pattern matching exceeds time limit, use fallback classification

### Content Validation

- **Type checking:**
  - Verify `raw_content` is string type
  - Validate `source_context` is object type (if provided)

- **Character encoding:**
  - Support UTF-8 for international characters
  - Handle emoji, Chinese, Arabic, and other Unicode properly
  - No encoding-based exploits

## Performance Target

**Target execution time:** < 2 seconds per classification

**Performance considerations:**

- Pattern matching optimized with efficient regex
- Early exit when high-confidence match found
- Minimal memory allocation during processing
- No external API calls (local classification only)

**Monitoring:**

- Log classification time for each execution
- Alert if average time exceeds target threshold
- Identify slow patterns for optimization

# Capture Tasks Test Data Set

Comprehensive test samples for validating the 4 capture tasks:

1. `capture-classify-content-type.md`
2. `capture-extract-metadata.md`
3. `capture-create-inbox-note.md`
4. `capture-create-capture-event.md`

## Overview

This test data set contains **26 samples** covering all content types and edge cases:

- **20 normal samples** across 6 content types (3-4 samples each)
- **6 edge case samples** for security and error handling validation

## Directory Structure

```
test-capture-samples/
├── quotes/                    # 3 quote samples
│   ├── quote-01-cal-newport.md
│   ├── quote-02-research-paper.md
│   └── quote-03-tweet.md
├── concepts/                  # 4 concept samples
│   ├── concept-01-atomic-notes.md
│   ├── concept-02-zettelkasten.md
│   ├── concept-03-spaced-repetition.md
│   └── concept-04-progressive-summarization.md
├── references/                # 3 reference samples
│   ├── reference-01-web-article.md
│   ├── reference-02-resource-list.md
│   └── reference-03-documentation.md
├── reflections/               # 4 reflection samples
│   ├── reflection-01-personal-insight.md
│   ├── reflection-02-process-review.md
│   ├── reflection-03-hypothesis.md
│   └── reflection-04-retrospective.md
├── questions/                 # 3 question samples
│   ├── question-01-why-question.md
│   ├── question-02-how-question.md
│   └── question-03-what-if.md
├── observations/              # 3 observation samples
│   ├── observation-01-pattern.md
│   ├── observation-02-behavior.md
│   └── observation-03-data.md
├── edge-case-samples/         # 6 edge case samples
│   ├── empty-content.md              # Empty file (error test)
│   ├── very-short.md                 # 2 characters (short content test)
│   ├── unicode-content.md            # Emoji, Chinese, Arabic, Japanese
│   ├── malicious-xss.md              # Script tags (XSS test)
│   ├── malformed-url.md              # javascript:, data:, file: URLs
│   └── path-with-spaces.md           # Filename with spaces
├── expected-results.yaml      # Ground truth for validation
└── README.md                  # This file
```

## Content Type Taxonomy

### 1. Quote (3 samples)

**Definition:** Contains quoted text with source attribution

**Key patterns:**

- Quotation marks ("...", '...', smart quotes)
- Attribution keywords: "said", "according to", "states"
- Source citations (author, title, page number)

**Examples:**

- Academic citations with full bibliography
- Tweet quotes with handle attribution
- Book quotes with author and title

### 2. Concept (4 samples)

**Definition:** Defines or explains an idea/principle

**Key patterns:**

- Definition keywords: "is defined as", "means", "refers to"
- Explanatory structure: "X is Y that Z"
- Clarifying language: "in other words", "specifically"

**Examples:**

- Atomic notes definition
- Zettelkasten methodology explanation
- Spaced repetition concept

### 3. Reference (3 samples)

**Definition:** Points to external resources (link-heavy)

**Key patterns:**

- Contains URLs (http://, https://)
- "See also" language: "see", "read more", "check out", "visit"
- Multiple links (3+)

**Examples:**

- Resource lists with multiple links
- Documentation references
- Reading recommendations

### 4. Reflection (4 samples)

**Definition:** Personal thoughts, opinions, insights

**Key patterns:**

- First-person language: "I think", "I feel", "I believe"
- Opinion markers: "in my view", "my sense is"
- Subjective interpretations

**Examples:**

- Personal insights about methods
- Process reviews and retrospectives
- Hypotheses and beliefs

### 5. Question (3 samples)

**Definition:** Investigative inquiry

**Key patterns:**

- Ends with question mark (?)
- Investigative keywords: "why", "how", "what if"
- Interrogative structure

**Examples:**

- Why-questions about mechanisms
- How-questions about integration
- What-if hypothetical scenarios

### 6. Observation (3 samples)

**Definition:** Descriptive, factual statements about what was noticed

**Key patterns:**

- Observation keywords: "I noticed", "I saw", "observed that"
- Descriptive structure (factual focus)
- Data points and metrics

**Examples:**

- Pattern observations (note clustering)
- Behavioral observations (productivity patterns)
- Data observations (statistics, metrics)

## Edge Cases

### empty-content.md

**Purpose:** Test error handling for empty content

**Expected behavior:**

- Classification: Return error "Content cannot be empty"
- Extraction: Can proceed if source_context exists
- Note creation: Should fail (no content to create note from)

### very-short.md

**Purpose:** Test short content handling (< 10 words)

**Content:** "Hi" (2 characters)

**Expected behavior:**

- Apply -0.1 confidence penalty for content < 10 words
- Still attempt classification (fallback to "concept" if confidence < 0.5)
- Should not crash or reject

### unicode-content.md

**Purpose:** Test Unicode and international character handling

**Contains:** Emoji, Chinese, Arabic, Japanese characters

**Expected behavior:**

- Proper UTF-8 encoding preserved
- No encoding errors or corruption
- Classification works on mixed-language content
- Inbox note displays correctly in Obsidian

### malicious-xss.md

**Purpose:** Test XSS attack prevention

**Contains:** `<script>`, `<iframe>`, `<object>` tags

**Expected behavior:**

- All malicious tags stripped or escaped
- Content sanitized before classification
- No script execution during processing
- Safe content stored in inbox note

### malformed-url.md

**Purpose:** Test malicious URL validation

**Contains:** javascript:, data:, file:, vbscript: URLs

**Expected behavior:**

- Malicious schemes rejected (set to "Unknown")
- Only valid URLs (https://example.com) accepted
- URL validation prevents security exploits
- Warning logged for blocked URLs

### path-with-spaces.md

**Purpose:** Test filename/path handling with spaces

**Expected behavior:**

- Spaces preserved or properly URL-encoded
- Note created successfully despite spaces
- No path parsing errors

## Usage

### Running Classification Tests

```bash
# Activate Inbox Triage Agent or use capture tasks directly
/bmad-2b:inbox-triage-agent

# Run classification on all samples
for file in test-capture-samples/{quotes,concepts,references,reflections,questions,observations}/*.md; do
  echo "Testing: $file"
  # Use capture-classify-content-type task on file content
done
```

### Validating Results

Compare actual classification results with `expected-results.yaml`:

```yaml
# Example: Validate quote-01
Expected:
  content_type: quote
  confidence_min: 0.90
  matched_patterns: [quotation marks, attribution keyword, author name]

Actual:
  content_type: quote
  confidence: 0.95
  matched_patterns: [quotation marks, attribution keyword: 'According to', author name]

Result: ✅ PASS (correct type, confidence >= 0.90, patterns match)
```

### Success Criteria

**Classification Accuracy:**

- Overall accuracy: >= 85% (17 out of 20 correct)
- Per-type accuracy:
  - Quotes: >= 90% (3 out of 3)
  - Concepts: >= 85% (4 out of 4)
  - References: >= 85% (3 out of 3)
  - Reflections: >= 85% (4 out of 4)
  - Questions: >= 95% (3 out of 3)
  - Observations: >= 85% (3 out of 3)

**Edge Case Handling:**

- All 6 edge cases must pass their specific tests
- XSS prevention: 100% (script tags stripped)
- URL validation: 100% (malicious URLs blocked)
- Unicode handling: 100% (no corruption)

**Performance Targets:**

- Classification: < 2 seconds per sample (average)
- Metadata extraction: < 1 second per sample (average)
- Note creation: < 3 seconds per sample (average)
- End-to-end: < 30 seconds per complete capture (average)

### Security Validation

Run security tests on edge case samples:

1. **XSS Prevention Test:**

   ```
   Input: malicious-xss.md
   Expected: <script> tags stripped/escaped
   Verify: No script execution, safe content in inbox note
   ```

2. **URL Validation Test:**

   ```
   Input: malformed-url.md
   Expected: Malicious URLs rejected (set to "Unknown")
   Verify: Only https://example.com accepted, others blocked
   ```

3. **Path Sanitization Test:**

   ```
   Input: path with "../../../etc/passwd"
   Expected: Rejected with error "Invalid path: directory traversal blocked"
   Verify: No files created outside vault
   ```

4. **Size Limit Test:**

   ```
   Input: 15MB file
   Expected: Rejected with error "Content exceeds size limit (10MB max)"
   Verify: No processing attempted on oversized content
   ```

5. **YAML Injection Test:**
   ```
   Input: Metadata with YAML special chars (: # - [ ])
   Expected: Characters properly escaped in frontmatter
   Verify: Note parses correctly in Obsidian without YAML errors
   ```

## Test Results Log

Create a `test-results.md` file to log test execution:

```markdown
# Test Execution Results

**Date:** 2025-11-06
**Tester:** [Your Name]

## Classification Tests (20 samples)

| Sample                  | Expected Type | Actual Type | Confidence | Status  |
| ----------------------- | ------------- | ----------- | ---------- | ------- |
| quote-01-cal-newport    | quote         | quote       | 0.95       | ✅ PASS |
| quote-02-research-paper | quote         | quote       | 0.92       | ✅ PASS |
| ...                     | ...           | ...         | ...        | ...     |

**Overall Accuracy:** 18/20 (90%) ✅ PASS (>= 85% target)

## Security Tests (5 tests)

| Test           | Expected Behavior | Actual Behavior   | Status  |
| -------------- | ----------------- | ----------------- | ------- |
| XSS Prevention | Tags stripped     | Tags stripped     | ✅ PASS |
| URL Validation | Malicious blocked | Malicious blocked | ✅ PASS |
| ...            | ...               | ...               | ...     |

**Security Score:** 5/5 (100%) ✅ PASS

## Performance Tests

| Task           | Target | Actual   | Status  |
| -------------- | ------ | -------- | ------- |
| Classification | < 2s   | 1.2s avg | ✅ PASS |
| Extraction     | < 1s   | 0.6s avg | ✅ PASS |
| Note Creation  | < 3s   | 2.1s avg | ✅ PASS |
| End-to-End     | < 30s  | 6.8s avg | ✅ PASS |
```

## Notes

- Test samples are designed to be unambiguous for their primary type
- Some samples may show minor secondary patterns (e.g., a reflection mentioning a concept)
- Confidence thresholds are minimum acceptable values; higher is better
- Edge cases may legitimately have lower confidence scores due to penalties
- The 85% accuracy target allows for 3 misclassifications out of 20 samples

## Contributing

When adding new test samples:

1. Create the sample file in appropriate subdirectory
2. Add expected results to `expected-results.yaml`
3. Update this README.md with the new sample description
4. Verify the sample tests correctly with actual capture tasks

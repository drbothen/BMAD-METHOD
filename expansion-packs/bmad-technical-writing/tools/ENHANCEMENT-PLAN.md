# AI Pattern Analysis Tool - Enhancement Plan for LLM-Actionable Output

## Purpose

Enhance `analyze_ai_patterns.py` to provide **rich diagnostic context** that enables LLMs to perform targeted humanization fixes without manually searching for problems.

## Current Limitations

**What we detect**:
- ✅ AI vocabulary count and list of words
- ✅ Heading depth and parallelism scores
- ✅ Sentence variation metrics
- ✅ Em-dash counts

**What we DON'T provide for LLM cleanup**:
- ❌ **Line numbers** where problems occur
- ❌ **Context snippets** showing the problem in situ
- ❌ **Specific replacement suggestions** for AI vocabulary
- ❌ **Paragraph identifiers** for uniformity issues
- ❌ **Heading text examples** showing parallelism problems
- ❌ **Sentence examples** demonstrating uniformity

## Proposed Enhancements

### Enhancement 1: Location-Aware AI Vocabulary Detection

**Current output**:
```
AI Vocabulary: 15 instances (85.23 per 1k words)
Examples: delve, robust, robust, leverage, leverages, facilitates
```

**Enhanced output**:
```
AI Vocabulary: 15 instances (85.23 per 1k words)

Detailed Instances:
1. Line 23: "delve into the robust capabilities"
   → Suggestion: Replace "delve into" with "explore" or "examine"
   → Suggestion: Replace "robust" with "reliable" or "powerful"

2. Line 45: "leverage Docker's seamless integration"
   → Suggestion: Replace "leverage" with "use" or "take advantage of"
   → Suggestion: Replace "seamless" with "smooth" or "easy"

3. Line 67: "facilitates the creation of isolated environments"
   → Suggestion: Replace "facilitates" with "enables" or "allows"
```

**Implementation**:
- Track line numbers during regex matching
- Provide 10-20 character context window around match
- Load replacement suggestions from `ai-detection-patterns.md`
- Limit to top 10-15 instances to avoid overwhelming output

### Enhancement 2: Heading Analysis with Examples

**Current output**:
```
Heading Depth: 6
Heading Parallelism: 0.85 (mechanical)
Verbose Headings: 3
```

**Enhanced output**:
```
Heading Depth: 6 levels (Target: 3 max)
Problematic Headings:
  - Line 89: ##### Authorization Code Grant (H5 - too deep)
  - Line 92: ##### Implicit Grant (H5 - too deep)
  → Suggestion: Flatten to H3 or convert to bold body text

Heading Parallelism: 0.85 (MECHANICAL PATTERN DETECTED)
Examples of Parallelism:
  - Line 12: ## Understanding Containers (H2)
  - Line 34: ## Understanding Images (H2)
  - Line 56: ## Understanding Volumes (H2)
  - Line 78: ## Understanding Networks (H2)
  → Suggestion: Vary structures - "Container Basics", "Working with Images",
                 "Data Persistence with Volumes", "How Networking Works"

Verbose Headings: 3 (Target: 0)
  - Line 45: "Understanding the Fundamental Principles of Asynchronous JavaScript" (10 words)
    → Suggestion: "Asynchronous JavaScript Fundamentals" (3 words)
  - Line 67: "How to Configure Your Development Environment for Optimal Performance" (10 words)
    → Suggestion: "Development Environment Setup" (3 words)
```

**Implementation**:
- Track line numbers for all headings
- Group headings by level to show parallelism examples
- Identify verbose headings (>8 words) with line numbers
- Provide restructuring suggestions based on `heading-humanization-patterns.md`
- Show actual heading text, not just counts

### Enhancement 3: Sentence Uniformity Detection with Examples

**Current output**:
```
Sentence Mean: 17.3 words
Sentence StdDev: 4.2 (LOW BURSTINESS)
```

**Enhanced output**:
```
Sentence Variation: LOW BURSTINESS (StdDev 4.2, Target: ≥10)

Uniform Paragraph Examples:
Paragraph at Line 45-52 (8 sentences, all 15-19 words):
  "Docker uses containers to isolate applications and dependencies. (9 words)
   Containers share the host system kernel for efficiency. (8 words)
   This approach reduces resource usage compared to VMs. (9 words)
   Each container runs as an isolated process on the host. (10 words)
   ..."
  → Problem: All sentences 8-10 words (mechanical uniformity)
  → Suggestion: Add variation - combine some sentences, split others

Paragraph at Line 89-96 (6 sentences, all 22-24 words):
  "The algorithm processes data in real-time by analyzing patterns... (23 words)
   These insights help developers understand user behavior patterns... (22 words)
   ..."
  → Problem: All sentences ~23 words (AI-typical)
  → Suggestion: Mix in short punchy sentences (5-10 words) and longer ones (30-45)
```

**Implementation**:
- Track paragraph boundaries
- Detect paragraphs with uniform sentence lengths (StdDev <3 within paragraph)
- Show first 2-3 sentences of problematic paragraphs
- Provide specific variation suggestions

### Enhancement 4: Em-Dash Location Tracking

**Current output**:
```
Em-dashes: 17 (4.0 per page)
```

**Enhanced output**:
```
Em-dashes: 17 (4.0 per page, Target: 1-2 max)

High-Density Sections:
Page 1 (Lines 1-50): 8 em-dashes
  - Line 12: "Docker makes deployment easy—and you'll see results quickly—when properly configured"
  - Line 23: "The solution—microservices—provides better scaling"
  - Line 34: "Authentication is critical—but implementing it takes planning—very careful planning"
  → Suggestion: Replace most em-dashes with periods, semicolons, or commas

Page 2 (Lines 51-100): 6 em-dashes
  - Line 67: "The framework provides—through its plugin system—extensive customization"
  ...
```

**Implementation**:
- Track line numbers for em-dash occurrences
- Group by page/section
- Show context snippets (20-30 chars each side)
- Highlight sections exceeding 2 per page

### Enhancement 5: Formulaic Transitions with Context

**Current output**:
```
Formulaic Transitions: 12 instances
Examples: Furthermore, Moreover, Additionally
```

**Enhanced output**:
```
Formulaic Transitions: 12 instances (Target: <3 per page)

Detailed Instances:
1. Line 23: "Furthermore, Docker provides several benefits..."
   → Suggestion: "What's more," "Beyond that," or remove entirely

2. Line 45: "Moreover, it enables developers to build applications..."
   → Suggestion: "Plus," "On top of that," or "And here's the thing,"

3. Line 67: "Additionally, Docker containers start quickly..."
   → Suggestion: "Also," "And," or natural flow without transition
```

**Implementation**:
- Track line numbers for formula transitions
- Show full sentence context
- Provide natural alternatives based on `ai-detection-patterns.md`

### Enhancement 6: New Output Format - `--detailed` Mode

Add a new CLI flag for enhanced diagnostic output:

```bash
# Standard analysis (current behavior)
python analyze_ai_patterns.py chapter-03.md

# Detailed LLM-actionable diagnostics
python analyze_ai_patterns.py chapter-03.md --detailed

# Detailed with JSON output for programmatic parsing
python analyze_ai_patterns.py chapter-03.md --detailed --format json
```

**Detailed mode output structure**:
```json
{
  "summary": {
    "overall_assessment": "SUBSTANTIAL humanization required",
    "perplexity_score": "LOW",
    "burstiness_score": "MEDIUM"
  },
  "ai_vocabulary": {
    "count": 15,
    "per_1k": 85.23,
    "instances": [
      {
        "line": 23,
        "word": "delve",
        "context": "...will delve into the robust...",
        "suggestions": ["explore", "examine", "investigate"]
      },
      ...
    ]
  },
  "headings": {
    "depth_violations": [
      {
        "line": 89,
        "level": 5,
        "text": "Authorization Code Grant",
        "suggestion": "Flatten to H3 or convert to body text"
      }
    ],
    "parallelism_examples": [
      {"line": 12, "text": "Understanding Containers"},
      {"line": 34, "text": "Understanding Images"},
      {"line": 56, "text": "Understanding Volumes"}
    ],
    "verbose_headings": [
      {
        "line": 45,
        "text": "Understanding the Fundamental Principles...",
        "word_count": 10,
        "suggestion": "Asynchronous JavaScript Fundamentals"
      }
    ]
  },
  "uniformity_issues": [
    {
      "paragraph_start_line": 45,
      "paragraph_end_line": 52,
      "sentence_count": 8,
      "mean_length": 9.1,
      "stdev": 0.8,
      "sentences": [
        {"line": 45, "text": "Docker uses containers...", "length": 9},
        {"line": 46, "text": "Containers share the...", "length": 8}
      ],
      "problem": "All sentences 8-10 words (mechanical uniformity)",
      "suggestion": "Add variation - combine some sentences, split others"
    }
  ],
  "formatting": {
    "em_dashes": [
      {
        "line": 12,
        "context": "Docker makes deployment easy—and you'll see...",
        "suggestion": "Replace em-dash with period or semicolon"
      }
    ]
  }
}
```

## Implementation Priority

**Phase 1 (High Impact)**:
1. ✅ AI vocabulary with line numbers and context (most common issue)
2. ✅ Heading examples showing parallelism and depth violations
3. ✅ Em-dash location tracking by section

**Phase 2 (Medium Impact)**:
4. ✅ Sentence uniformity paragraph detection
5. ✅ Formulaic transition context and suggestions

**Phase 3 (Nice to Have)**:
6. ✅ JSON schema for detailed mode
7. ✅ Replacement suggestion database from data files

## Benefits for LLM-Driven Cleanup

With these enhancements, an LLM can:

1. **Locate problems precisely** - Line numbers eliminate searching
2. **Understand context** - Snippets show surrounding text
3. **Apply fixes confidently** - Specific suggestions provided
4. **Prioritize issues** - Grouped by severity and type
5. **Work incrementally** - Process one category at a time
6. **Validate changes** - Re-run analysis to measure improvement

## Example LLM Workflow

```
User: Analyze and humanize chapter-03.md

Agent: Running analysis with detailed diagnostics...
[Executes: python analyze_ai_patterns.py chapter-03.md --detailed]

Agent: Analysis complete. Found 3 critical issues:

1. CRITICAL: 15 AI vocabulary instances (lines 23, 45, 67, ...)
   Fixing line 23: "delve into" → "explore"
   Fixing line 45: "leverage" → "use"
   ...

2. HIGH: Heading parallelism (lines 12, 34, 56, 78)
   Restructuring H2 headings for natural variation...

3. HIGH: 17 em-dashes (4 per page, target 1-2)
   Reducing em-dashes on page 1 (8 instances)...

[Agent applies fixes]

Agent: Humanization complete. Re-analyzing...
[Executes: python analyze_ai_patterns.py chapter-03.md --detailed]

Agent: Improvement validated:
- AI vocabulary: 15 → 2 (87% reduction) ✅
- Em-dashes: 4.0 → 1.2 per page ✅
- Heading parallelism: 0.85 → 0.12 ✅
- Overall: SUBSTANTIAL → LIGHT humanization needed ✅
```

## File Changes Required

1. **`analyze_ai_patterns.py`**:
   - Add `--detailed` flag
   - Enhance all `_analyze_*` methods to track line numbers
   - Add context extraction for matches
   - Load replacement suggestions from data files
   - Implement detailed JSON schema

2. **`requirements.txt`**:
   - No new dependencies (uses standard library)

3. **`README.md`**:
   - Document `--detailed` flag
   - Add examples of detailed output
   - Explain LLM workflow integration

## Testing Strategy

1. Test with sample AI-generated content (high AI pattern density)
2. Test with human-written content (low AI pattern density)
3. Validate line numbers are accurate
4. Verify context snippets are helpful
5. Ensure JSON output is valid and parseable

## Success Metrics

- LLM can locate and fix 90%+ of flagged issues without clarifying questions
- Line numbers are accurate within ±1 line
- Context snippets provide 20-40 characters around problem
- Replacement suggestions are appropriate for 80%+ of cases
- Detailed mode processing time <5 seconds for 5000-word documents

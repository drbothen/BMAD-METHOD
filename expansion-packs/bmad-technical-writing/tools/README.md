# AI Pattern Analysis Tool

Comprehensive Python script for analyzing manuscripts to detect AI-generated content patterns across 6 dimensions.

## Overview

`analyze_ai_patterns.py` analyzes markdown files for AI-generated content patterns using research-backed methodologies from GPTZero, Originality.AI, and academic studies. The tool evaluates 40+ metrics across 6 dimensions:

1. **Perplexity (Vocabulary)** - AI-typical word choices and lexical diversity
2. **Burstiness (Sentence Variation)** - Sentence length variation and rhythm
3. **Structure (Organization)** - Transitions, headings, formatting patterns
4. **Voice (Authenticity)** - Personal perspective, contractions, direct address
5. **Technical (Expertise)** - Domain-specific terminology density
6. **Formatting (Distribution)** - Em-dashes, bold, italics usage patterns

## Installation

```bash
# Install optional dependencies for readability metrics
pip install -r requirements.txt

# Or minimal installation (textstat is optional)
pip install textstat
```

**Requirements:**
- Python 3.7+
- textstat 0.7.3+ (optional, for readability metrics)
- Standard library: re, statistics, argparse, pathlib, dataclasses, json, typing

## Usage

### Single File Analysis

Analyze one markdown file with detailed text report:

```bash
python analyze_ai_patterns.py manuscript/chapters/chapter-01.md
```

Output includes:
- Dimension scores (HIGH/MEDIUM/LOW/VERY LOW)
- Overall assessment
- Detailed metrics breakdown
- Specific recommendations for humanization

### JSON Output

For programmatic processing:

```bash
python analyze_ai_patterns.py chapter-01.md --format json > analysis.json
```

JSON structure includes all 40+ metrics in machine-readable format.

### Batch Analysis

Analyze entire directories with TSV output for spreadsheet import:

```bash
python analyze_ai_patterns.py --batch manuscript/sections --format tsv > analysis.tsv
```

Import the TSV into Excel, Google Sheets, or Numbers for comparative analysis across multiple files.

### Custom Domain Terms

Specify domain-specific technical terms to improve technical depth scoring:

```bash
python analyze_ai_patterns.py chapter-01.md \
  --domain-terms "Docker,Kubernetes,PostgreSQL,Redis,GraphQL"
```

Domain terms are treated as positive signals (high domain term density = more authentic technical content).

### Detailed Mode (LLM-Actionable Diagnostics)

**NEW:** Use `--detailed` flag for comprehensive line-by-line analysis with context and replacement suggestions:

```bash
python analyze_ai_patterns.py chapter-01.md --detailed
```

**Detailed mode provides:**
- **Line numbers** for every AI pattern detected
- **Context snippets** showing surrounding text (20-30 characters)
- **Specific suggestions** for replacements and fixes
- **Grouped issues** by type (vocabulary, headings, transitions, em-dashes)
- **Priority recommendations** (CRITICAL/HIGH/MEDIUM/LOW)

**Use cases:**
- LLM-driven humanization workflows
- Systematic cleanup with precise location tracking
- Pre-validation before manual editing
- Targeted fixes for specific issue types

**Example output:**
```
AI VOCABULARY INSTANCES (6 shown)
────────────────────────────────────────────────────────────────────────────────

1. Line 23: "delve"
   Context: ...will delve into the robust...
   → Suggestions: explore, examine, investigate

2. Line 45: "leverage"
   Context: ...leverage Docker's seamless integration...
   → Suggestions: use, apply, take advantage of

HEADING STRUCTURE ISSUES (3 total)
────────────────────────────────────────────────────────────────────────────────

MECHANICAL PARALLELISM (identical structures):
  Line 12: ## Understanding Containers
    → Vary structure - all H2 headings start with "Understanding"

EM-DASH USAGE (17 total, 4.0 per page)
────────────────────────────────────────────────────────────────────────────────

  Line 67: ...Docker makes deployment easy—and you'll see results...
    → Replace with period, semicolon, comma, or parentheses

RECOMMENDED ACTIONS (Priority Order)
────────────────────────────────────────────────────────────────────────────────

[CRITICAL] Reduce em-dashes from 4.0 to ≤2 per page (17 instances to review)
[HIGH    ] Replace AI vocabulary: 12.4 per 1k words (6 instances shown above)
[HIGH    ] Break mechanical parallelism in headings (score: 0.85, 3 patterns detected)
```

**JSON output for programmatic processing:**
```bash
python analyze_ai_patterns.py chapter-01.md --detailed --format json
```

Produces structured JSON with:
- All vocabulary instances with line numbers and suggestions
- All heading issues categorized by type (depth/parallelism/verbose)
- Uniform paragraph detection with sentence examples
- Em-dash and transition instances with context

**Perfect for:**
- LLM agents that need to locate and fix specific issues
- Automated humanization pipelines
- Quality assurance validation before publication
- Training data generation for humanization models

## Output Formats

### Text Report (default)

Human-readable detailed report with:
- Summary header (words, sentences, paragraphs)
- Dimension scores with traffic-light ratings
- Detailed metrics breakdown by category
- Specific recommendations for improvement
- Examples of AI vocabulary and transitions found

Example:
```
================================================================================
AI PATTERN ANALYSIS REPORT
================================================================================

File: chapter-01.md
Words: 4,532 | Sentences: 186 | Paragraphs: 42

────────────────────────────────────────────────────────────────────────────────
DIMENSION SCORES
────────────────────────────────────────────────────────────────────────────────

Perplexity (Vocabulary):    MEDIUM        (AI words: 12, 2.65/1k)
Burstiness (Sentence Var):  HIGH          (μ=22.3, σ=12.8, range=(5, 67))
Structure (Organization):   MEDIUM        (Formulaic: 3, H-depth: 3)
Voice (Authenticity):       HIGH          (1st-person: 15, You: 48)
Technical (Expertise):      HIGH          (Domain terms: 89)
Formatting (Em-dashes):     HIGH          (1.2 per page)

OVERALL ASSESSMENT: MINIMAL humanization needed
```

### JSON Format

Structured data with all metrics:

```json
{
  "file_path": "chapter-01.md",
  "total_words": 4532,
  "ai_vocabulary_count": 12,
  "ai_vocabulary_per_1k": 2.65,
  "sentence_mean_length": 22.3,
  "sentence_stdev": 12.8,
  "perplexity_score": "MEDIUM",
  "overall_assessment": "MINIMAL humanization needed"
}
```

### TSV Format (Batch Mode)

Tab-separated values for spreadsheet import:

```
file	words	sentences	ai_words	ai_per_1k	sent_mean	sent_stdev	perplexity	burstiness	overall
ch01.md	4532	186	12	2.65	22.3	12.8	MEDIUM	HIGH	MINIMAL humanization needed
ch02.md	3891	164	8	2.06	21.1	11.4	MEDIUM	HIGH	MINIMAL humanization needed
```

## Metrics Explained

### Perplexity (Vocabulary Dimension)

**AI Vocabulary Detection:**
- Tier 1 markers: delve, robust, leverage, harness, underscore, facilitate
- Tier 2 markers: seamless, comprehensive, utilize, implement
- Tier 3 markers: innovative, cutting-edge, state-of-the-art, next-generation

**Scoring:**
- HIGH: ≤2 AI words per 1k (human-like)
- MEDIUM: 2-5 AI words per 1k (acceptable)
- LOW: 5-10 AI words per 1k (needs improvement)
- VERY LOW: >10 AI words per 1k (heavily AI-generated)

**Lexical Diversity (Type-Token Ratio):**
- Human writing: 0.55-0.70 (varied vocabulary)
- AI writing: 0.40-0.50 (repetitive vocabulary)

### Burstiness (Sentence Variation)

**Target Distribution:**
- Short sentences (5-10 words): 20-30%
- Medium sentences (15-25 words): 40-50%
- Long sentences (30-45 words): 20-30%

**Scoring:**
- HIGH: StdDev ≥10 (strong variation)
- MEDIUM: StdDev 6-10 (moderate variation)
- LOW: StdDev 3-6 (weak variation)
- VERY LOW: StdDev <3 (uniform, AI-like)

**AI Pattern:** Uniform 15-22 word sentences with low standard deviation

### Structure (Organization)

**Formulaic Transitions:**
- Detected: Furthermore, Moreover, Additionally, Hence, Thus, Therefore, etc.
- Target: <3 formulaic transitions per page
- Human alternative: Natural flow, context-specific connectors

**Heading Hierarchy:**
- AI pattern: 4-6 heading levels with mechanical parallelism
- Human pattern: 3 levels maximum with natural variation
- Verbose headings: >8 words = AI marker

**Parallelism Score:**
- 0.0-0.3: Varied structures (human-like)
- 0.3-0.6: Some repetition (acceptable)
- 0.6-1.0: Mechanical patterns (AI-like)

### Voice (Authenticity)

**Indicators:**
- First-person markers: "I've found", "In my experience"
- Direct address: "you", "your", "you'll"
- Contractions: "don't", "it's", "you're"

**Scoring:**
- HIGH: Strong personal voice (contractions + perspective)
- MEDIUM: Some personal elements
- LOW: Formal and distant
- VERY LOW: No personal voice (pure exposition)

### Technical (Expertise)

**Domain Term Density:**
- Measures use of specific technical vocabulary
- Higher density = more authentic technical content
- Use `--domain-terms` flag to specify custom terms

**Scoring:**
- HIGH: >20 domain terms per 1k words
- MEDIUM: 10-20 per 1k
- LOW: 5-10 per 1k
- VERY LOW: <5 per 1k

### Formatting (Distribution)

**Em-dash Analysis:**
- AI pattern: 10x more em-dashes than human writing
- Target: 1-2 em-dashes per page maximum
- The "ChatGPT dash" is strongest AI detection signal

**Bold/Italic Usage:**
- AI pattern: Excessive, uniform distribution
- Target: 2-5% bold maximum, functional italics only

## Overall Assessment

The tool provides weighted overall assessment:

| Score | Assessment | Interpretation |
|-------|-----------|----------------|
| 80-100 | MINIMAL humanization needed | Publication-ready, <5% AI patterns |
| 60-79 | LIGHT humanization needed | Minor edits required, 5-10% AI patterns |
| 40-59 | MODERATE humanization needed | Systematic editing required, 10-20% AI patterns |
| 20-39 | SUBSTANTIAL humanization required | Major rewrite needed, 20-40% AI patterns |
| 0-19 | EXTENSIVE humanization required | Likely AI-generated, >40% AI patterns |

**Weighting:**
- Perplexity: 20%
- Burstiness: 25%
- Structure: 20%
- Voice: 20%
- Technical: 10%
- Formatting: 5%

## Workflow Integration

### Pre-Publishing Quality Check

```bash
# Analyze all chapters before submission
python analyze_ai_patterns.py --batch manuscript/chapters --format tsv > pre-publish-qa.tsv

# Review in spreadsheet, target all chapters at HIGH/MEDIUM across dimensions
```

### Humanization Task Workflow

#### Manual Editing Workflow

1. **Analyze current state:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md
   ```

2. **Note specific issues:**
   - AI vocabulary instances
   - Sentence variation problems
   - Heading hierarchy depth
   - Formatting patterns

3. **Apply humanization edits** following the recommendations

4. **Re-analyze to validate:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md
   ```

5. **Target:** All dimensions at MEDIUM or HIGH for publication

#### LLM-Driven Humanization Workflow

1. **Get detailed diagnostics:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --detailed -o diagnostics.txt
   ```

2. **Provide diagnostics to LLM:**
   - Pass the detailed report to an LLM (Claude, ChatGPT, etc.)
   - LLM uses line numbers to locate exact issues
   - LLM applies suggested replacements and fixes

3. **Validate improvements:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --detailed
   ```

4. **Iterate if needed:**
   - Compare before/after metrics
   - Target: 50-80% reduction in AI patterns per pass
   - Repeat until MINIMAL or LIGHT assessment achieved

### Content-Humanizer Agent Integration

The `content-humanizer` agent (`agents/content-humanizer.md`) uses this tool for:

1. **`*analyze` command** - Runs analysis and interprets results
2. **`*qa-check` command** - Validates humanization quality before completion
3. **Post-generation workflow** - Step 8 of `humanize-post-generation.md` task

## Research Foundation

This tool implements methodologies from:

1. **GPTZero** - Perplexity and burstiness detection
2. **Originality.AI** - Pattern recognition and scoring
3. **Academic Studies** - Type-Token Ratio, lexical diversity
4. **Publisher Guidelines** - Formatting and structure best practices

Data sources:
- `data/ai-detection-patterns.md` - Vocabulary and transition patterns
- `data/formatting-humanization-patterns.md` - Em-dash problem, formatting
- `data/heading-humanization-patterns.md` - Hierarchy and parallelism
- `data/humanization-techniques.md` - Comprehensive technique catalog

## Limitations

- **Context-agnostic:** Cannot judge appropriateness of technical terms for specific domain
- **False positives:** Some technical writing legitimately uses AI-flagged vocabulary
- **Style preference:** Technical writing conventions differ from creative writing
- **Tool-assisted content:** Cannot distinguish AI-generated from AI-edited content

**Recommendation:** Use scores as diagnostic information, not absolute judgments. Combine with human editorial review for publication decisions.

## Examples

### High-Quality Technical Writing

```
Perplexity:    HIGH      (2.1 AI words per 1k)
Burstiness:    HIGH      (StdDev 13.2, varied lengths)
Structure:     HIGH      (3 heading levels, natural transitions)
Voice:         HIGH      (contractions, direct address, examples)
Technical:     HIGH      (28 domain terms per 1k)
Formatting:    HIGH      (1.3 em-dashes per page)

OVERALL: MINIMAL humanization needed
```

### AI-Generated Draft

```
Perplexity:    VERY LOW  (24.7 AI words per 1k)
Burstiness:    LOW       (StdDev 4.2, uniform sentences)
Structure:     LOW       (5 heading levels, mechanical parallelism)
Voice:         VERY LOW  (no contractions, formal distance)
Technical:     LOW       (3 domain terms per 1k, generic examples)
Formatting:    VERY LOW  (8.4 em-dashes per page)

OVERALL: EXTENSIVE humanization required
```

## License

Part of BMAD-METHOD™ Technical Writing Expansion Pack.
See repository root LICENSE for details.

## Support

- Expansion Pack: `/expansion-packs/bmad-technical-writing/`
- Agent: `agents/content-humanizer.md`
- Tasks: `tasks/analyze-ai-patterns.md`, `tasks/humanization-qa-check.md`
- Discord: https://discord.gg/gk8jAdXWmj

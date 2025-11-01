# AI Pattern Analysis Tool

Comprehensive Python script for analyzing manuscripts to detect AI-generated content patterns with dual scoring system for LLM-driven optimization.

## Overview

`analyze_ai_patterns.py` analyzes markdown files for AI-generated content patterns using research-backed methodologies from GPTZero, Originality.AI, GLTR, and academic studies. The tool evaluates 50+ metrics across **14 dimensions** organized into **3 tiers**:

### Tier 1: Advanced Detection (40 points) - Highest Accuracy
1. **GLTR Token Ranking** - Token predictability analysis (95% accuracy on GPT-3/ChatGPT)
2. **Advanced Lexical Diversity** - HDD/Yule's K sophisticated vocabulary metrics
3. **AI Detection Ensemble** - RoBERTa sentiment variance + DetectGPT
4. **Stylometric Markers** - Statistical writing fingerprints
5. **Syntactic Complexity** - Dependency depth and POS patterns

### Tier 2: Core Patterns (35 points) - Strong Signals
6. **Burstiness (Sentence Variation)** - Sentence length variation and rhythm
7. **Perplexity (Vocabulary)** - AI-typical word choices
8. **Formatting Patterns** - Em-dashes, bold, italics distribution
9. **Heading Hierarchy** - Depth, parallelism, density patterns

### Tier 3: Supporting Signals (25 points) - Contextual Indicators
10. **Voice & Authenticity** - Personal perspective, contractions, direct address
11. **Structure & Organization** - Transitions, list usage, whitespace patterns
12. **Emotional Depth** - Sentiment variation and emotional resonance
13. **Technical Depth** - Domain-specific terminology density

## Dual Scoring System (NEW)

The tool now provides **two complementary scores** designed for LLM-driven optimization:

- **Quality Score** (0-100, higher=better): How human-like the writing is
- **Detection Risk** (0-100, lower=better): Likelihood of AI detection

### Key Features

✅ **Path-to-Target Optimization** - Shows minimum actions needed to reach quality goals, sorted by ROI
✅ **Historical Tracking** - Per-document score history with trend analysis
✅ **Effort Estimation** - LOW/MEDIUM/HIGH effort levels for each improvement
✅ **Impact Analysis** - Identifies HIGH/MEDIUM/LOW impact dimensions
✅ **Configurable Targets** - Default quality≥85, detection≤30 (customizable)

## Installation

### Quick Start (Automated - Recommended)

For **full enhanced features** with all 6 NLP libraries:

```bash
# Run the automated setup script
./setup.sh
```

This creates a clean virtual environment with:
- ✅ NLTK (enhanced lexical diversity)
- ✅ VADER (sentiment analysis)
- ✅ TextBlob (alternative sentiment)
- ✅ spaCy (syntactic patterns)
- ✅ Textacy (stylometric analysis)
- ✅ Transformers (GPT-2 perplexity)

**Why a separate environment?** Your anaconda environment has numpy version conflicts with 50+ existing packages. A dedicated venv avoids breaking other tools. See `SETUP-GUIDE.md` for details.

### Manual Installation

#### Option 1: Basic (Core Features Only - No Dependencies)
```bash
# No installation needed - works with Python stdlib
python analyze_ai_patterns.py chapter.md
```

#### Option 2: Enhanced (All NLP Features - Manual Setup)
```bash
# Create clean virtual environment
python3 -m venv nlp-env
source nlp-env/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Download required models
python -m nltk.downloader punkt punkt_tab vader_lexicon
python -m spacy download en_core_web_sm
```

**Requirements:**
- Python 3.7+ (3.9+ recommended for full compatibility)
- See `requirements.txt` for complete list of optional dependencies

## Quick Reference

### Three Analysis Modes

| Mode | Flag | Best For | Output |
|------|------|----------|--------|
| **Dual Score** | `--show-scores` | LLM optimization, first-time analysis | Quality Score + Detection Risk + path-to-target |
| **Standard** | (default) | Quick overview, batch analysis | 6 dimension scores + overall assessment |
| **Detailed** | `--detailed` | Line-by-line editing, debugging | Line numbers + context + suggestions |

### Quick Start Commands

```bash
# Recommended: Dual score analysis with optimization path
python analyze_ai_patterns.py chapter-01.md --show-scores

# Quick batch check across many files
python analyze_ai_patterns.py --batch manuscript/chapters --format tsv

# Detailed diagnostics for manual editing
python analyze_ai_patterns.py chapter-01.md --detailed

# Custom targets for dual scoring
python analyze_ai_patterns.py chapter-01.md --show-scores --quality-target 90
```

### Target Scores

**Dual Score Defaults:**
- Quality Score: ≥85 (EXCELLENT)
- Detection Risk: ≤30 (MEDIUM or better)

**Standard Mode:** All dimensions at MEDIUM or HIGH

## Usage

The tool has **three analysis modes**:

1. **Standard Analysis** - Traditional dimension scoring (6 dimensions, quick overview)
2. **Dual Score Analysis** - Optimization-focused with path-to-target (14 dimensions, LLM-friendly)
3. **Detailed Diagnostic** - Line-by-line issues with context (for manual/LLM editing)

### Dual Score Analysis (Recommended for LLM Optimization)

Get optimization-focused dual scores with path-to-target recommendations:

```bash
python analyze_ai_patterns.py chapter-01.md --show-scores
```

**Output includes:**
- **Quality Score** (0-100, target ≥85)
- **Detection Risk** (0-100, target ≤30)
- **Score breakdown** across 3 tiers and 14 dimensions
- **Path-to-target** - Prioritized actions sorted by ROI
- **Historical trend** - Shows improvement over time
- **Effort estimation** - Total effort required (MINIMAL/LIGHT/MODERATE/SUBSTANTIAL/EXTENSIVE)

**Example output:**
```
DUAL SCORES
────────────────────────────────────────────────────────────────────────────────

Quality Score:       77.0 / 100  GOOD - Natural with minor tells
Detection Risk:      16.2 / 100  LOW - Unlikely flagged

Targets:            Quality ≥85, Detection ≤30
Gap to Target:      Quality needs +8.0 pts, Detection needs -0.0 pts
Effort Required:    MODERATE

PATH TO TARGET (2 actions, sorted by ROI)
────────────────────────────────────────────────────────────────────────────────

1. Heading Hierarchy (Effort: LOW)
   Current: 2.5/5.0 → Gain: +2.5 pts → Cumulative: 79.5
   Action: Flatten to H3 max, break parallelism, create asymmetry

2. Voice & Authenticity (Effort: HIGH)
   Current: 2.0/8.0 → Gain: +6.0 pts → Cumulative: 85.5
   Action: Add personal perspective, contractions, hedging
```

#### Custom Targets

Adjust quality and detection targets:

```bash
# Stricter targets (higher quality, lower risk)
python analyze_ai_patterns.py chapter-01.md --show-scores --quality-target 90 --detection-target 20

# Relaxed targets (for drafts)
python analyze_ai_patterns.py chapter-01.md --show-scores --quality-target 75 --detection-target 40
```

#### JSON Output for Programmatic Use

```bash
python analyze_ai_patterns.py chapter-01.md --show-scores --format json > scores.json
```

JSON includes:
- All dual score data
- Complete dimension breakdown with raw values
- All improvement actions with effort/impact levels
- Historical trend data if available

#### Historical Tracking

Scores are automatically saved to `.score-history/` directory:

```bash
# First run creates history
python analyze_ai_patterns.py chapter-01.md --show-scores

# Subsequent runs show trend
# Quality:   IMPROVING (+3.2 pts)
# Detection: IMPROVING (-5.1 pts)
```

History files: `.score-history/{filename}.history.json`

### Single File Analysis (Standard Mode)

Analyze one markdown file with traditional dimension scoring:

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

## Score Interpretation

### Dual Score System (--show-scores)

#### Quality Score (0-100, higher=better)

| Score | Interpretation | Meaning |
|-------|---------------|---------|
| 95-100 | EXCEPTIONAL | Indistinguishable from human writing |
| 85-94 | EXCELLENT | Minimal AI signatures, publication-ready |
| 70-84 | GOOD | Natural with minor tells, light editing needed |
| 50-69 | MIXED | Needs moderate work, systematic editing required |
| 30-49 | AI-LIKE | Substantial work needed, major rewrite |
| 0-29 | OBVIOUS AI | Complete rewrite recommended |

**Default Target:** ≥85 (EXCELLENT quality)

#### Detection Risk (0-100, lower=better)

| Score | Interpretation | Risk Level |
|-------|---------------|------------|
| 70-100 | VERY HIGH | Will be flagged by AI detectors |
| 50-69 | HIGH | Likely flagged by AI detectors |
| 30-49 | MEDIUM | May be flagged by some detectors |
| 15-29 | LOW | Unlikely to be flagged |
| 0-14 | VERY LOW | Safe from detection |

**Default Target:** ≤30 (MEDIUM risk or better)

#### Scoring Methodology

**Quality Score** is the sum of all dimension scores:
- Tier 1 (Advanced Detection): 40 points maximum
- Tier 2 (Core Patterns): 35 points maximum
- Tier 3 (Supporting Signals): 25 points maximum

**Detection Risk** uses weighted inverse scoring emphasizing advanced detection:
- GLTR Token Ranking: 25% weight
- AI Detection Ensemble: 20% weight
- Advanced Lexical Diversity: 15% weight
- Stylometric Markers: 15% weight
- Burstiness: 10% weight
- Formatting: 10% weight
- Perplexity: 5% weight

### Standard Mode Overall Assessment

The traditional scoring provides weighted overall assessment (backwards compatible):

| Score | Assessment | Interpretation |
|-------|-----------|----------------|
| 80-100 | MINIMAL humanization needed | Publication-ready, <5% AI patterns |
| 60-79 | LIGHT humanization needed | Minor edits required, 5-10% AI patterns |
| 40-59 | MODERATE humanization needed | Systematic editing required, 10-20% AI patterns |
| 20-39 | SUBSTANTIAL humanization required | Major rewrite needed, 20-40% AI patterns |
| 0-19 | EXTENSIVE humanization required | Likely AI-generated, >40% AI patterns |

**Standard Mode Weighting:**
- Perplexity: 20%
- Burstiness: 25%
- Structure: 20%
- Voice: 20%
- Technical: 10%
- Formatting: 5%

## Workflow Integration

### Which Mode to Use?

| Scenario | Mode | Command |
|----------|------|---------|
| LLM-driven iterative optimization | Dual Score | `--show-scores` |
| Quick quality check across many files | Standard | `--batch` |
| Manual line-by-line editing | Detailed | `--detailed` |
| First-time analysis | Dual Score | `--show-scores` |
| Pre-publication validation | Dual Score | `--show-scores` |
| Debugging specific issues | Detailed | `--detailed` |

### LLM-Driven Optimization Workflow (Recommended)

Uses dual scoring system for systematic improvement:

1. **Get optimization path:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --show-scores
   ```

2. **Review path-to-target:**
   - Note the prioritized actions (sorted by ROI)
   - Review effort estimation for each action
   - Check current score vs. target gap

3. **Provide to LLM:**
   ```
   "Here's the dual score analysis. Focus on the path-to-target actions:
   1. Heading Hierarchy (LOW effort, +2.5 pts)
   2. Voice & Authenticity (HIGH effort, +6.0 pts)

   Please implement these improvements to reach Quality Score ≥85."
   ```

4. **Re-analyze after changes:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --show-scores
   ```

5. **Review historical trend:**
   - Check if Quality score improved
   - Check if Detection Risk decreased
   - Compare actual vs. expected gains

6. **Iterate if needed:**
   - Target: Quality Score ≥85, Detection Risk ≤30
   - Track progress through historical trend
   - Typical improvement: +10-20 quality points per pass

### Manual Editing Workflow

#### With Dual Scoring (Quick Fixes)

1. **Analyze current state:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --show-scores
   ```

2. **Focus on path-to-target:**
   - Start with LOW effort, HIGH gain actions
   - Address formatting issues first (quick wins)
   - Then tackle voice and vocabulary

3. **Re-analyze to validate:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --show-scores
   ```

#### With Detailed Diagnostics (Precise Fixes)

1. **Get line-by-line issues:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --detailed -o diagnostics.txt
   ```

2. **Work through issues systematically:**
   - Use line numbers to locate exact problems
   - Apply suggested replacements
   - Fix one category at a time (vocabulary → headings → em-dashes → transitions)

3. **Validate with dual scoring:**
   ```bash
   python analyze_ai_patterns.py chapter-03.md --show-scores
   ```

### Pre-Publishing Quality Check

```bash
# Option 1: Batch analysis for quick overview
python analyze_ai_patterns.py --batch manuscript/chapters --format tsv > pre-publish-qa.tsv

# Option 2: Dual score analysis for each chapter (recommended)
for chapter in manuscript/chapters/*.md; do
  python analyze_ai_patterns.py "$chapter" --show-scores
done

# Target: All chapters at Quality ≥85, Detection ≤30
```

### Content-Humanizer Agent Integration

The `content-humanizer` agent (`agents/content-humanizer.md`) uses this tool for:

1. **`*analyze` command** - Runs dual score analysis and interprets results
2. **`*qa-check` command** - Validates humanization quality before completion (uses dual scoring)
3. **Post-generation workflow** - Step 8 of `humanize-post-generation.md` task (dual score validation)

**Agent workflow:**
- Initial analysis: `--show-scores` to establish baseline
- During editing: `--detailed` for specific issues
- Final validation: `--show-scores` to confirm targets met
- Historical tracking: Monitors improvement across iterations

### Score History Management

Score history files are stored in `.score-history/` directory:

```bash
# View history file
cat manuscript/.score-history/chapter-01.history.json

# Clean up history (start fresh)
rm -rf manuscript/.score-history/

# Recommended .gitignore entry
echo '.score-history/' >> .gitignore
```

**Note:** History files are per-document JSON files tracking all analysis runs with timestamps. Useful for tracking humanization progress over time.

## Research Foundation

This tool implements state-of-the-art methodologies from:

### AI Detection Research
1. **GLTR (Giant Language model Test for Robustness)** - Token rank analysis, 95% accuracy on GPT-3/ChatGPT
   - Gehrmann et al., ACL 2019
   - Top-10 token percentage as AI signature

2. **DetectGPT** - Perturbation-based detection
   - Mitchell et al., Stanford 2023
   - Zero-shot black-box detection

3. **GPTZero** - Perplexity and burstiness detection
   - Tian, Princeton 2023
   - Sentence-level variance analysis

4. **Originality.AI** - Pattern recognition and multi-model ensemble
   - Combined classifier approach

### Linguistic Metrics
5. **HDD (Hypergeometric Distribution D)** - Advanced lexical diversity
   - McCarthy & Jarvis, 2010
   - More robust than simple TTR

6. **Yule's K** - Vocabulary richness independent of text length
   - Yule, 1944
   - Statistical stylometry

7. **RoBERTa Sentiment Analysis** - Emotional variation detection
   - Cardiff NLP, Twitter-tuned model
   - Variance analysis for authenticity

8. **spaCy Dependency Parsing** - Syntactic complexity
   - Explosion AI
   - Dependency depth and POS diversity

### Humanization Research
9. **Publisher Guidelines** - Formatting and structure best practices
   - Technical writing standards
   - Academic style guides

10. **Empirical Analysis** - Real human vs. AI writing patterns
    - Em-dash frequency analysis (10x AI signature)
    - Heading hierarchy patterns
    - Bold/italic distribution analysis

### Data Sources
- `data/ai-detection-patterns.md` - Vocabulary and transition patterns
- `data/formatting-humanization-patterns.md` - Em-dash problem, formatting tells
- `data/heading-humanization-patterns.md` - Hierarchy and parallelism patterns
- `data/humanization-techniques.md` - Comprehensive technique catalog

### Metadata Filtering
- Automatically ignores HTML comment blocks (`<!-- -->`) at document start/end
- Ensures metadata doesn't skew analysis scores
- Focuses analysis on actual content only

## Limitations

- **Context-agnostic:** Cannot judge appropriateness of technical terms for specific domain
- **False positives:** Some technical writing legitimately uses AI-flagged vocabulary
- **Style preference:** Technical writing conventions differ from creative writing
- **Tool-assisted content:** Cannot distinguish AI-generated from AI-edited content

**Recommendation:** Use scores as diagnostic information, not absolute judgments. Combine with human editorial review for publication decisions.

## Examples

### High-Quality Technical Writing (Dual Score)

```
Quality Score:       92.3 / 100  EXCELLENT - Minimal AI signatures
Detection Risk:      12.4 / 100  VERY LOW - Safe

SCORE BREAKDOWN BY CATEGORY:

Advanced Detection          37.5 / 40.0  ( 93.8%)
  GLTR Token Ranking                        11.5 / 12.0  (gap:  0.5)
  Advanced Lexical (HDD/Yule's K)            7.5 /  8.0  (gap:  0.5)
  AI Detection Ensemble                      9.5 / 10.0  (gap:  0.5)
  Stylometric Markers                        5.0 /  6.0  (gap:  1.0)
  Syntactic Complexity                       4.0 /  4.0  (gap:  0.0)

Core Patterns               32.3 / 35.0  ( 92.3%)
  Burstiness (Sentence Variation)           11.0 / 12.0  (gap:  1.0)
  Perplexity (Vocabulary)                    9.5 / 10.0  (gap:  0.5)
  Formatting Patterns                        7.0 /  8.0  (gap:  1.0)
  Heading Hierarchy                          4.8 /  5.0  (gap:  0.2)

Supporting Signals          22.5 / 25.0  ( 90.0%)
  Voice & Authenticity                       7.5 /  8.0  (gap:  0.5)
  Structure & Organization                   6.5 /  7.0  (gap:  0.5)
  Emotional Depth                            5.5 /  6.0  (gap:  0.5)
  Technical Depth                            3.0 /  4.0  (gap:  1.0)

PATH TO TARGET: Already exceeds targets! (Quality ≥85, Detection ≤30)

OVERALL: Publication-ready, minimal refinement opportunities
```

### AI-Generated Draft (Dual Score)

```
Quality Score:       43.2 / 100  AI-LIKE - Substantial work needed
Detection Risk:      72.8 / 100  VERY HIGH - Will be flagged

SCORE BREAKDOWN BY CATEGORY:

Advanced Detection          14.0 / 40.0  ( 35.0%)
⚠ GLTR Token Ranking                         2.0 / 12.0  (gap: 10.0)
⚠ Advanced Lexical (HDD/Yule's K)            2.0 /  8.0  (gap:  6.0)
⚠ AI Detection Ensemble                      2.0 / 10.0  (gap:  8.0)
⚠ Stylometric Markers                        4.0 /  6.0  (gap:  2.0)
⚠ Syntactic Complexity                       4.0 /  4.0  (gap:  0.0)

Core Patterns               18.2 / 35.0  ( 52.0%)
⚠ Burstiness (Sentence Variation)            3.0 / 12.0  (gap:  9.0)
⚠ Perplexity (Vocabulary)                    2.0 / 10.0  (gap:  8.0)
⚠ Formatting Patterns                        2.0 /  8.0  (gap:  6.0)
⚠ Heading Hierarchy                          1.2 /  5.0  (gap:  3.8)

Supporting Signals          11.0 / 25.0  ( 44.0%)
⚠ Voice & Authenticity                       1.0 /  8.0  (gap:  7.0)
⚠ Structure & Organization                   4.0 /  7.0  (gap:  3.0)
⚠ Emotional Depth                            2.0 /  6.0  (gap:  4.0)
⚠ Technical Depth                            1.0 /  4.0  (gap:  3.0)

PATH TO TARGET (8 actions, EXTENSIVE effort):
1. GLTR Token Ranking (HIGH effort, +10.0 pts)
2. Burstiness (MEDIUM effort, +9.0 pts)
3. Perplexity (MEDIUM effort, +8.0 pts)
4. AI Detection Ensemble (HIGH effort, +8.0 pts)
[... 4 more actions ...]

Gap to Target: Quality needs +41.8 pts

OVERALL: Major rewrite recommended, use detailed mode for line-by-line fixes
```

### Standard Mode Examples

**High-Quality Technical Writing:**
```
Perplexity:    HIGH      (2.1 AI words per 1k)
Burstiness:    HIGH      (StdDev 13.2, varied lengths)
Structure:     HIGH      (3 heading levels, natural transitions)
Voice:         HIGH      (contractions, direct address, examples)
Technical:     HIGH      (28 domain terms per 1k)
Formatting:    HIGH      (1.3 em-dashes per page)

OVERALL: MINIMAL humanization needed
```

**AI-Generated Draft:**
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

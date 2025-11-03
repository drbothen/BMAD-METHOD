# Task: Analyze AI Patterns in Manuscript

<!-- Powered by BMAD™ Core -->

## Purpose

Systematically analyze manuscript files for AI-generated content patterns using the AI Pattern Analysis Tool's dual scoring system. Provides **two complementary scores** (Quality Score 0-100 + Detection Risk 0-100) with **path-to-target optimization** across **14 dimensions** organized in **3 tiers** (Advanced Detection, Core Patterns, Supporting Signals) to guide humanization efforts.

## Analysis Modes

The tool supports **three analysis modes**:

1. **Dual Score Analysis** (Recommended) - `--show-scores`
   - Quality Score (0-100, higher=better) + Detection Risk (0-100, lower=better)
   - Path-to-target recommendations sorted by ROI
   - Historical tracking with trend analysis
   - 14 dimensions across 3 tiers
   - **Best for**: LLM optimization, iterative improvement, first-time analysis

2. **Standard Analysis** (Legacy) - default behavior
   - 6 dimension scores (HIGH/MEDIUM/LOW/VERY LOW)
   - Overall assessment
   - **Best for**: Quick overview, batch comparison

3. **Detailed Diagnostic** - `--detailed`
   - Line-by-line issues with context and suggestions
   - **Best for**: Manual editing, debugging specific problems

**This task covers all three modes, with emphasis on Dual Score Analysis (recommended).**

## When to Use This Task

- **Before humanization** to establish baseline metrics and identify specific issues (use `--show-scores`)
- **After humanization** to validate improvement and measure success (use `--show-scores` for trend)
- **During iterative optimization** to track progress toward quality targets (use `--show-scores`)
- **During quality assurance** to ensure content meets publication standards (use `--show-scores`)
- When content feels AI-generated but you need specific diagnostic data
- For batch analysis of entire manuscript sections or chapters (use standard mode)
- For line-by-line editing guidance (use `--detailed`)

## Prerequisites

- Python 3.7+ installed (Python 3.9+ recommended)
- AI Pattern Analysis Tool available at `{{config.root}}/data/tools/analyze_ai_patterns.py`
- Markdown files to analyze (chapters, sections, or entire manuscript)
- Python virtual environment set up with required dependencies (see setup below)
- **Reference**: `{{config.root}}/data/COMPREHENSIVE-METRICS-GUIDE.md` for detailed metric definitions, thresholds, and improvement strategies

## Workflow Steps

### 0. Python Environment Setup (First Time Only)

**CRITICAL**: The AI Pattern Analysis Tool requires Python dependencies. Set up a virtual environment ONCE before first use.

**Navigate to tools directory**:

```bash
cd {{config.root}}/data/tools
```

**Create virtual environment** (one-time setup):

```bash
# Create virtual environment
python3 -m venv nlp-env

# Activate it (macOS/Linux)
source nlp-env/bin/activate

# OR activate it (Windows)
nlp-env\Scripts\activate
```

**Install dependencies**:

```bash
# Install all required libraries
pip install -r requirements.txt

# Download NLTK models
python -m nltk.downloader punkt punkt_tab vader_lexicon

# Download spaCy language model
python -m spacy download en_core_web_sm

# Download TextBlob corpora (optional, for additional sentiment analysis)
python -m textblob.download_corpora
```

**Verify installation**:

```bash
# Test the script
python analyze_ai_patterns.py --help
```

**Expected output**: Help text showing all available options.

**IMPORTANT**:

- **First-time setup takes 5-10 minutes** (downloading models ~500MB-1GB total)
- **Subsequent uses**: Just activate the environment (`source nlp-env/bin/activate`)
- **When done**: Deactivate with `deactivate` command
- **Virtual environment location**: `{{config.root}}/data/tools/nlp-env/` (gitignored)

**Troubleshooting**:

- If `python3` not found, try `python`
- If numpy conflicts occur, upgrade pip: `pip install --upgrade pip`
- For M1/M2 Macs, you may need: `pip install --upgrade numpy`
- GPT-2 model auto-downloads on first analysis run (~500MB)

### 1. Load Configuration

- Read `.bmad-technical-writing/config.yaml` to resolve paths
- Extract: `config.manuscript.root`, `config.manuscript.sections`, `config.manuscript.chapters`
- If config not found, use defaults: `manuscript/`, `manuscript/sections`, `manuscript/chapters`

### 2. Identify Target File(s)

**For single file analysis**:

- Locate the specific file to analyze (chapter, section, or draft)
- Note the file path (e.g., `{{config.manuscript.chapters}}/chapter-03.md`)

**For batch analysis**:

- Identify the directory containing files to analyze
- Decide scope: single chapter's sections, all chapters, specific subset
- Note the directory path (e.g., `{{config.manuscript.sections}}/chapter-03/`)

### 3. Determine Domain-Specific Terms (Optional but Recommended)

**Identify technical vocabulary specific to the book's subject matter**:

- Programming languages: "Python", "JavaScript", "Rust"
- Frameworks/libraries: "React", "Django", "Kubernetes"
- Domain concepts: "OAuth", "GraphQL", "Docker"
- Tools: "Git", "npm", "PostgreSQL"

**Why this matters**: The technical depth score measures domain term density. Providing domain terms improves accuracy of this dimension.

**Format**: Comma-separated list (e.g., "Docker,Kubernetes,PostgreSQL,Redis")

### 4. Run Dual Score Analysis (Recommended)

**IMPORTANT**: Activate the virtual environment first (every time you use the tool):

```bash
cd {{config.root}}/data/tools
source nlp-env/bin/activate  # macOS/Linux
# OR nlp-env\Scripts\activate  # Windows
```

**Command for dual scoring**:

```bash
python analyze_ai_patterns.py PATH_TO_FILE \
  --show-scores \
  [--quality-target N] \
  [--detection-target N] \
  [--domain-terms "term1,term2,term3"]
```

**Example**:

```bash
python analyze_ai_patterns.py ../{{config.manuscript.chapters}}/chapter-03.md \
  --show-scores \
  --quality-target 85 \
  --detection-target 30 \
  --domain-terms "Docker,Kubernetes,PostgreSQL,Redis,GraphQL"
```

**Expected output**: Dual score optimization report with:

- **Quality Score** (0-100, higher=better) with interpretation
- **Detection Risk** (0-100, lower=better) with interpretation
- **Targets and gaps** - How far from quality/detection goals
- **Score breakdown** - All 14 dimensions across 3 tiers
- **Path-to-target** - Prioritized actions sorted by ROI
- **Effort estimation** - MINIMAL/LIGHT/MODERATE/SUBSTANTIAL/EXTENSIVE
- **Historical trend** - Shows improvement over time (if previous scores exist)

**Example output**:

```
DUAL SCORES
────────────────────────────────────────────────────────────────────────────────

Quality Score:       77.0 / 100  GOOD - Natural with minor tells
Detection Risk:      16.2 / 100  LOW - Unlikely flagged

Targets:            Quality ≥85, Detection ≤30
Gap to Target:      Quality needs +8.0 pts, Detection needs -0.0 pts
Effort Required:    MODERATE

HISTORICAL TREND (2 scores tracked)
────────────────────────────────────────────────────────────────────────────────

Quality:   IMPROVING (+3.2 pts)
Detection: IMPROVING (-5.1 pts)

PATH TO TARGET (2 actions, sorted by ROI)
────────────────────────────────────────────────────────────────────────────────

1. Heading Hierarchy (Effort: LOW)
   Current: 2.5/5.0 → Gain: +2.5 pts → Cumulative: 79.5
   Action: Flatten to H3 max, break parallelism, create asymmetry

2. Voice & Authenticity (Effort: HIGH)
   Current: 2.0/8.0 → Gain: +6.0 pts → Cumulative: 85.5
   Action: Add personal perspective, contractions, hedging
```

**Target Defaults**:

- Quality Score: ≥85 (EXCELLENT quality)
- Detection Risk: ≤30 (MEDIUM risk or better)

**Adjust targets based on context**:

- Book chapters: `--quality-target 90 --detection-target 20` (stricter)
- Blog posts: `--quality-target 85 --detection-target 30` (standard)
- Internal docs: `--quality-target 75 --detection-target 40` (relaxed)

### 4a. Run Standard Analysis (Legacy Mode)

**For quick overview or batch comparison**:

**Command**:

```bash
python analyze_ai_patterns.py PATH_TO_FILE [--domain-terms "term1,term2,term3"]
```

**Example**:

```bash
python analyze_ai_patterns.py ../{{config.manuscript.chapters}}/chapter-03.md \
  --domain-terms "Docker,Kubernetes,PostgreSQL,Redis,GraphQL"
```

**Expected output**: Detailed text report with:

- Summary header (words, sentences, paragraphs)
- 6 dimension scores (HIGH/MEDIUM/LOW/VERY LOW)
- Overall assessment
- Detailed metrics breakdown
- Specific recommendations

### 5. Interpret Dual Score Results (If Using --show-scores)

**Understand the two complementary scores**:

**Quality Score (0-100, higher=better)**:
| Score | Interpretation | Action |
|-------|----------------|--------|
| 95-100 | EXCEPTIONAL - Indistinguishable from human | Publication-ready, minimal refinement |
| 85-94 | EXCELLENT - Minimal AI signatures | Publication-ready, meets standards |
| 70-84 | GOOD - Natural with minor tells | Light editing needed |
| 50-69 | MIXED - Needs moderate work | Systematic editing required |
| 30-49 | AI-LIKE - Substantial work needed | Major rewrite needed |
| 0-29 | OBVIOUS AI - Complete rewrite | Regenerate with humanization prompt |

**Detection Risk (0-100, lower=better)**:
| Score | Interpretation | Risk Level |
|-------|----------------|------------|
| 70-100 | VERY HIGH - Will be flagged | Critical issues, must fix |
| 50-69 | HIGH - Likely flagged | Substantial work needed |
| 30-49 | MEDIUM - May be flagged | Moderate improvement needed |
| 15-29 | LOW - Unlikely flagged | Minor refinement |
| 0-14 | VERY LOW - Safe | Publication-ready |

**Review path-to-target recommendations**:

Each action in path-to-target shows:

- **Dimension name**: Which aspect needs improvement
- **Effort level**: LOW (15-30 min) / MEDIUM (30-45 min) / HIGH (45-90 min)
- **Potential gain**: Expected quality points increase
- **Cumulative score**: Running total if actions completed sequentially
- **Action**: Specific humanization technique to apply

**Prioritize actions**:

1. **Start with LOW effort, HIGH gain** actions (best ROI)
2. **Focus on dimensions with ⚠ warning symbols** (HIGH or MEDIUM impact)
3. **Apply actions until quality target reached** (may not need all actions)
4. **Use effort levels for time planning** (sum efforts for realistic schedule)

**Example interpretation**:

```
Quality Score: 67.8 (MIXED - Needs moderate work)
Gap to Target: +17.2 points needed

Path to Target shows 4 actions totaling +21 points:
- Action 1: GLTR (HIGH effort, +9 pts) → Most impactful
- Action 2: Burstiness (MEDIUM effort, +3 pts) → Quick win
- Action 3: AI Detection (HIGH effort, +5 pts) → Moderate gain
- Action 4: Lexical (HIGH effort, +4 pts) → Additional improvement

Strategy: Do Actions 1 and 2 first (12 pts gain, ~1 hour)
→ Would reach 79.8, then reassess if Action 3 needed to reach 85
```

**For detailed metric understanding**: See `{{config.root}}/data/COMPREHENSIVE-METRICS-GUIDE.md` for:

- Mathematical definitions of each dimension (GLTR, Burstiness, MATTR, etc.)
- Quantitative thresholds (AI vs. human patterns)
- Specific improvement strategies with examples
- Academic research foundations for each metric

**Check historical trend** (if running analysis multiple times):

- **IMPROVING**: Quality increasing OR detection decreasing (good progress)
- **STABLE**: Scores within ±1 point (plateau or target met)
- **WORSENING**: Quality decreasing OR detection increasing (over-editing or regression)

**Use trend to guide decisions**:

- **IMPROVING**: Continue current approach
- **STABLE at target**: Stop, targets met
- **STABLE below target**: Try different techniques, consider regeneration
- **WORSENING**: Revert recent changes, investigate technical errors

### 5a. Interpret Standard Results (Legacy Mode)

**Review each dimension score**:

**Perplexity (Vocabulary)**:

- HIGH (≤2 AI words per 1k): Natural vocabulary
- MEDIUM (2-5 per 1k): Acceptable
- LOW (5-10 per 1k): Needs improvement
- VERY LOW (>10 per 1k): Heavily AI-generated

**Burstiness (Sentence Variation)**:

- HIGH (StdDev ≥10): Strong variation
- MEDIUM (StdDev 6-10): Moderate variation
- LOW (StdDev 3-6): Weak variation
- VERY LOW (StdDev <3): Uniform, AI-like

**Structure (Organization)**:

- Check formulaic transitions count (target <3 per page)
- Check heading depth (target 3 levels max)
- Check heading parallelism score (0=varied, 1=mechanical)

**Voice (Authenticity)**:

- Count first-person markers
- Count direct address ("you/your")
- Count contractions
- Higher = more authentic voice

**Technical (Expertise)**:

- Check domain terms per 1k words
- HIGH (>20 per 1k): Strong technical content
- LOW (<5 per 1k): Generic content

**Formatting (Distribution)**:

- Check em-dashes per page (target 1-2 max)
- 3+ per page = strong AI signal

**Overall Assessment**:

- MINIMAL humanization needed: Publication-ready (<5% AI patterns)
- LIGHT humanization needed: Minor edits (5-10% AI patterns)
- MODERATE humanization needed: Systematic editing (10-20% AI patterns)
- SUBSTANTIAL humanization required: Major rewrite (20-40% AI patterns)
- EXTENSIVE humanization required: Likely AI-generated (>40% AI patterns)

### 5b. View Optimization History (v2.0 Features)

Comprehensive history tracking with dimension-level trends, sparkline visualization, and iteration comparison.

**Automatic History Tracking**:

Every time you analyze a file with `--show-scores`, the tool automatically saves:

- Aggregate scores (Quality + Detection Risk)
- All 33 dimension scores across 4 tiers
- All raw metrics (AI vocabulary, sentence stdev, MATTR, etc.)
- Word count, sentence count, paragraph count
- Timestamp and optional notes

History is saved to: `.history_FILENAME.json` (hidden file in same directory)

**View Complete Optimization Journey**:

```bash
python analyze_ai_patterns.py FILE.md --show-history-full
```

This shows:

- Aggregate score trends with sparklines (▁▂▃▄▅▆▇█)
- All 4 tier score progressions
- Full iteration-by-iteration summary
- Top dimension improvements
- Publication readiness assessment
- Success/failure indicators

**Example output**:

```
COMPLETE OPTIMIZATION JOURNEY
================================================================================
Document: chapter-03.md
Iterations: 5 (2025-11-02 to 2025-11-02)

AGGREGATE SCORES:
  Quality:   60.0 → 88.0  (+28.0 pts)  IMPROVING ↑
  Detection: 55.0 → 22.0  (-33.0 pts)  IMPROVING ↑

ITERATION SUMMARY:
--------------------------------------------------------------------------------
ITERATION 1: Initial draft - straight from AI
Timestamp:     2025-11-02T10:00:00
Quality:       60.0 / 100  (POOR - Needs major work)
Detection:     55.0 / 100  (HIGH - Likely flagged)
Total Words:   3800
Sentences:     180
Paragraphs:    22

...

Status: PUBLICATION READY ✓
```

**View Dimension-Level Trends**:

```bash
python analyze_ai_patterns.py FILE.md --show-dimension-trends
```

Shows top improving/declining dimensions with sparklines:

```
TOP 5 DIMENSION IMPROVEMENTS:

  1. Burstiness (Sent. Var):
     5.0 → 11.0  (+6.0 pts)  ↑  EXCELLENT improvement
  2. Voice & Authenticity:
     2.0 → 8.0  (+6.0 pts)  ↑  EXCELLENT improvement
  3. Perplexity (AI Vocab):
     4.0 → 9.0  (+5.0 pts)  ↑  EXCELLENT improvement
```

**Compare Two Iterations**:

```bash
python analyze_ai_patterns.py FILE.md --compare-history "first,last"
# OR specific iteration numbers
python analyze_ai_patterns.py FILE.md --compare-history "1,5"
```

Shows side-by-side comparison:

- Aggregate score changes
- Tier score changes
- Significant dimension improvements (±2pts)
- Key insights and recommendations

**View Raw Metric Trends**:

```bash
python analyze_ai_patterns.py FILE.md --show-raw-metric-trends
```

Shows sparkline charts for underlying metrics:

```
ai_vocabulary_per_1k:
  █▄▃▂▁  25.50 → 12.00  (-13.5, -53%)  ↓

sentence_stdev:
  ▁▁▅▆█  4.20 → 10.50  (+6.3, +150%)  ↑

mattr:
  ▁▂▃▅█  0.62 → 0.74  (+0.1, +19%)  ↑
```

**Export History for External Analysis**:

```bash
# Export to CSV for Excel/Numbers/Google Sheets
python analyze_ai_patterns.py FILE.md --export-history csv

# Export to JSON for programmatic analysis
python analyze_ai_patterns.py FILE.md --export-history json
```

CSV includes:

- All iterations with timestamps
- Word/sentence/paragraph counts
- Quality and detection scores
- All 4 tier scores
- All 33 dimension scores (score + percentage)
- All raw metrics
- Notes for each iteration

**Add Notes to Iterations**:

```bash
python analyze_ai_patterns.py FILE.md --show-scores \
  --history-notes "Reduced AI vocabulary by 50%"
```

Notes appear in full history report and CSV export, making it easy to remember what changed.

**Quick History Summary** (included automatically with --show-scores):

When you run `--show-scores` on a file with history, you'll see:

```
HISTORICAL TREND (3 scores tracked)
────────────────────────────────────────────────────────────────────────────────
Quality:   IMPROVING (+8.2 pts)
Detection: IMPROVING (-11.3 pts)
```

**Typical Workflow with History**:

1. **Baseline** (Iteration 1):

   ```bash
   python analyze_ai_patterns.py chapter.md --show-scores \
     --history-notes "Initial AI draft"
   ```

2. **After each humanization pass** (Iterations 2-N):

   ```bash
   # Apply humanization edits...
   python analyze_ai_patterns.py chapter.md --show-scores \
     --history-notes "Fixed sentence variation and AI vocab"
   ```

3. **View progress**:

   ```bash
   python analyze_ai_patterns.py chapter.md --show-history-full
   ```

4. **Compare first vs current**:

   ```bash
   python analyze_ai_patterns.py chapter.md --compare-history "first,last"
   ```

5. **Export for reporting**:
   ```bash
   python analyze_ai_patterns.py chapter.md --export-history csv
   ```

**Use Cases**:

- **Iterative optimization**: Track quality improvements over multiple editing passes
- **Plateau detection**: Identify when dimensions stop improving (switch tactics)
- **ROI analysis**: See which humanization techniques yield best score improvements
- **Reporting**: Export to CSV for stakeholder reports or team dashboards
- **Learning**: Build knowledge of which patterns work for your content type
- **Validation**: Prove content meets quality standards with quantitative data

### 6. Document Specific Issues

**Extract actionable data from the report**:

**AI Vocabulary**:

- Note the specific words listed (e.g., "delve, robust, leverage, facilitate")
- Count total instances
- Calculate per 1k words ratio

**Sentence Variation**:

- Note mean sentence length
- Note standard deviation
- Note distribution (short/medium/long percentages)

**Heading Issues**:

- Note maximum depth (target 3)
- Note parallelism score (target <0.3)
- Note verbose heading count (target 0)

**Formatting Problems**:

- Note em-dashes per page (target 1-2)
- Note bold/italic usage patterns

### 7. Run Batch Analysis (Optional)

**When analyzing multiple files** (all sections in a chapter, all chapters in manuscript):

**IMPORTANT**: Activate virtual environment first:

```bash
cd {{config.root}}/data/tools
source nlp-env/bin/activate  # macOS/Linux
```

**Command**:

```bash
python analyze_ai_patterns.py --batch DIRECTORY_PATH --format tsv > analysis-report.tsv
```

**Example**:

```bash
python analyze_ai_patterns.py --batch ../{{config.manuscript.sections}}/chapter-03 \
  --format tsv > chapter-03-section-analysis.tsv
```

**Import into spreadsheet** (Excel, Google Sheets, Numbers) to:

- Compare sections side-by-side
- Identify outliers (sections with much higher/lower scores)
- Track improvement over multiple analysis runs
- Sort by problematic dimensions

**TSV columns**:

- file, words, sentences, paragraphs
- ai_words, ai_per_1k, formulaic
- sent_mean, sent_stdev, sent_min, sent_max, short, medium, long
- lexical_diversity, headings, h_depth, h_parallel, em_dashes_pg
- perplexity, burstiness, structure, voice, technical, formatting, overall

### 8. Generate JSON Output (Optional - For Automation)

**For programmatic processing or integration with other tools**:

**Command**:

```bash
python3 analyze_ai_patterns.py PATH_TO_FILE --format json > analysis.json
```

**Example**:

```bash
python3 analyze_ai_patterns.py ../{{config.manuscript.chapters}}/chapter-03.md \
  --format json > chapter-03-analysis.json
```

**Use cases**:

- Automated quality gates in CI/CD pipelines
- Integration with other analysis tools
- Programmatic tracking of metrics over time
- Dashboard visualizations

### 9. Create Humanization Work Plan

**Based on analysis results, prioritize humanization efforts**:

**If Overall Assessment = MINIMAL/LIGHT**:

- Focus on specific flagged issues only
- 15-30 minute targeted editing session
- Priorities: AI vocabulary, em-dash reduction, heading depth

**If Overall Assessment = MODERATE**:

- Apply systematic humanization workflow (Pass 1-8)
- 60-90 minute editing session
- Use `humanize-post-generation.md` task
- Focus on dimensions scored LOW or VERY LOW
- **Reference**: See `{{config.root}}/data/COMPREHENSIVE-METRICS-GUIDE.md` for specific improvement strategies for each dimension

**If Overall Assessment = SUBSTANTIAL/EXTENSIVE**:

- Consider regenerating with better prompt engineering
- Or budget 2-3 hours for comprehensive humanization
- Apply full 8-pass editing workflow
- May need multiple iterations

**Document priorities**:

```
Humanization Work Plan for [FILE_NAME]

Overall Score: [SCORE] - [ASSESSMENT]

Priority 1 (Critical Issues):
- [ ] Issue from analysis (e.g., "Replace 24 AI vocabulary instances")
- [ ] Issue from analysis (e.g., "Reduce em-dashes from 8.4 to 1-2 per page")

Priority 2 (Important Issues):
- [ ] Issue from analysis
- [ ] Issue from analysis

Priority 3 (Nice to Have):
- [ ] Issue from analysis

Estimated time: [TIME] minutes
```

### 10. Optional: Compare Before/After

**To validate humanization effectiveness**:

1. **Activate environment and run analysis BEFORE humanization**, save output:

   ```bash
   source nlp-env/bin/activate  # Don't forget this!
   python analyze_ai_patterns.py chapter-03.md > before-analysis.txt
   ```

2. **Apply humanization edits** using `humanize-post-generation.md` task

3. **Run analysis AFTER humanization**, save output:

   ```bash
   python analyze_ai_patterns.py chapter-03.md > after-analysis.txt
   ```

4. **Compare metrics**:
   - AI vocabulary per 1k: Should decrease by 50-80%
   - Sentence StdDev: Should increase (higher burstiness)
   - Heading depth: Should decrease to 3 or less
   - Em-dashes per page: Should decrease to 1-2
   - Overall assessment: Should improve 1-2 levels

**Success indicators**:

- Perplexity: Improved from LOW → MEDIUM or MEDIUM → HIGH
- Burstiness: Improved from LOW → MEDIUM or MEDIUM → HIGH
- Formatting: Improved from LOW → MEDIUM or MEDIUM → HIGH
- Overall: Moved toward MINIMAL/LIGHT humanization needed

## Output Deliverable

**Primary**:

- Analysis report (text, JSON, or TSV format)
- Clear understanding of specific AI patterns present
- Quantitative baseline metrics for each dimension

**Secondary**:

- Humanization work plan with prioritized issues
- Estimated time budget for humanization
- Before/after comparison (if validating humanization)
- Structured analysis report using `create-doc.md` task with `humanization-analysis-report-tmpl.yaml` template (for dual scoring mode)

## Success Criteria

✅ Analysis completed successfully (no errors)
✅ All dimensions scored and understood (14 for dual scoring mode, 6 for standard mode)
✅ Specific problematic patterns identified (AI words, em-dashes, heading depth, etc.)
✅ Overall assessment understood and accepted (or dual scores interpreted for dual scoring mode)
✅ Humanization priorities established based on data (or path-to-target reviewed for dual scoring mode)
✅ Estimated time budget for humanization determined

## Common Pitfalls to Avoid

❌ Running analysis without domain terms (technical depth score will be inaccurate)
❌ Treating scores as absolute judgments (they're diagnostic, not prescriptive)
❌ Ignoring context (some technical writing legitimately uses "robust" or "facilitate")
❌ Over-optimizing for scores instead of readability
❌ Not documenting specific issues found (analysis without action plan)
❌ Forgetting to validate improvements with post-humanization analysis

## Integration with Other Tasks

**Pre-humanization workflow**:

1. `analyze-ai-patterns.md` ← **YOU ARE HERE** (establish baseline)
2. `humanize-post-generation.md` (apply systematic editing)
3. `humanization-qa-check.md` (validate results)

**Post-humanization validation**:

1. `humanize-post-generation.md` (editing completed)
2. `analyze-ai-patterns.md` ← **YOU ARE HERE** (measure improvement)
3. `humanization-qa-check.md` (final validation)

**Quality assurance**:

1. `write-chapter-draft.md` or `write-section-draft.md` (content creation)
2. `analyze-ai-patterns.md` ← **YOU ARE HERE** (quality check)
3. `humanize-post-generation.md` (if needed)
4. `copy-edit-chapter.md` (final polish)

## Tool Reference

**Script location**: `{{config.root}}/data/tools/analyze_ai_patterns.py`
**Documentation**: `{{config.root}}/data/tools/README.md`
**Requirements**: `{{config.root}}/data/tools/requirements.txt`

**Installation** (see Step 0 above for full setup):

```bash
cd {{config.root}}/data/tools
python3 -m venv nlp-env
source nlp-env/bin/activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab vader_lexicon
python -m spacy download en_core_web_sm
```

**Usage** (always activate environment first):

```bash
# Activate environment first
source nlp-env/bin/activate  # macOS/Linux

# Single file, text report
python analyze_ai_patterns.py FILE.md

# Single file with domain terms
python analyze_ai_patterns.py FILE.md --domain-terms "Term1,Term2,Term3"

# Batch analysis, TSV output
python analyze_ai_patterns.py --batch DIRECTORY --format tsv > report.tsv

# JSON output for automation
python analyze_ai_patterns.py FILE.md --format json > report.json

# Deactivate when done
deactivate
```

## Example Workflow

**Scenario**: Analyzing Chapter 3 before humanization

```bash
# Navigate to tools directory
cd /Users/author/manuscript-project/.bmad-technical-writing/data/tools

# Activate virtual environment
source nlp-env/bin/activate

# Run analysis with domain terms
python analyze_ai_patterns.py \
  ../manuscript/chapters/chapter-03.md \
  --domain-terms "Docker,Kubernetes,PostgreSQL,Redis,Nginx" \
  > chapter-03-baseline-analysis.txt

# Review report
cat chapter-03-baseline-analysis.txt

# Deactivate when done
deactivate
```

**Output interpretation**:

```
Perplexity:    LOW       (8.2 AI words per 1k)
Burstiness:    MEDIUM    (StdDev 7.3)
Structure:     LOW       (H-depth: 5, Formulaic: 12)
Voice:         LOW       (1st-person: 2, Contractions: 3)
Technical:     HIGH      (Domain terms: 34)
Formatting:    VERY LOW  (Em-dashes: 6.8 per page)

OVERALL: SUBSTANTIAL humanization required
```

**Action**: Create work plan focusing on:

1. Replace 37 AI vocabulary instances (Priority 1)
2. Reduce em-dashes from 6.8 to 1-2 per page (Priority 1)
3. Flatten heading hierarchy from 5 to 3 levels (Priority 2)
4. Add more contractions and first-person voice (Priority 2)
5. Replace 12 formulaic transitions (Priority 3)

**Estimated time**: 90-120 minutes for comprehensive humanization

## Notes

- This task is **diagnostic**, not prescriptive—scores guide but don't dictate edits
- Technical writing may legitimately score lower on some dimensions (less personal voice acceptable)
- Domain-appropriate writing sometimes uses AI-flagged vocabulary (context matters)
- Always prioritize readability and accuracy over score optimization
- Use batch analysis for comparative insights across multiple files
- Re-analyze after humanization to validate improvement quantitatively

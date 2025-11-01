# Task: Analyze AI Patterns in Manuscript

<!-- Powered by BMAD™ Core -->

## Purpose

Systematically analyze manuscript files for AI-generated content patterns using the AI Pattern Analysis Tool. Provides quantitative assessment across 6 dimensions (perplexity, burstiness, structure, voice, technical depth, formatting) to guide humanization efforts.

## When to Use This Task

- **Before humanization** to establish baseline metrics and identify specific issues
- **After humanization** to validate improvement and measure success
- **During quality assurance** to ensure content meets publication standards
- When content feels AI-generated but you need specific diagnostic data
- For batch analysis of entire manuscript sections or chapters

## Prerequisites

- Python 3.7+ installed (Python 3.9+ recommended)
- AI Pattern Analysis Tool available at `{{config.root}}/tools/analyze_ai_patterns.py`
- Markdown files to analyze (chapters, sections, or entire manuscript)
- Python virtual environment set up with required dependencies (see setup below)

## Workflow Steps

### 0. Python Environment Setup (First Time Only)

**CRITICAL**: The AI Pattern Analysis Tool requires Python dependencies. Set up a virtual environment ONCE before first use.

**Navigate to tools directory**:
```bash
cd {{config.root}}/tools
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
- **Virtual environment location**: `{{config.root}}/tools/nlp-env/` (gitignored)

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

### 4. Run Single File Analysis

**IMPORTANT**: Activate the virtual environment first (every time you use the tool):
```bash
cd {{config.root}}/tools
source nlp-env/bin/activate  # macOS/Linux
# OR nlp-env\Scripts\activate  # Windows
```

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
- Dimension scores (HIGH/MEDIUM/LOW/VERY LOW)
- Overall assessment
- Detailed metrics breakdown
- Specific recommendations

### 5. Interpret Results

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
cd {{config.root}}/tools
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

## Success Criteria

✅ Analysis completed successfully (no errors)
✅ All 6 dimensions scored and understood
✅ Specific problematic patterns identified (AI words, em-dashes, heading depth, etc.)
✅ Overall assessment understood and accepted
✅ Humanization priorities established based on data
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

**Script location**: `{{config.root}}/tools/analyze_ai_patterns.py`
**Documentation**: `{{config.root}}/tools/README.md`
**Requirements**: `{{config.root}}/tools/requirements.txt`

**Installation** (see Step 0 above for full setup):
```bash
cd {{config.root}}/tools
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
cd /Users/author/manuscript-project/.bmad-technical-writing/tools

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

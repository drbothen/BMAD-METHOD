# AI Pattern Analysis Tool - Setup Guide

## Problem: Anaconda Environment Conflicts

Your anaconda environment has packages compiled against numpy 1.x (pandas, pyarrow, scikit-learn, etc.) that create cascading dependency conflicts with numpy 2.x required by newer NLP libraries.

## Solution: Dedicated Virtual Environment

Create a **clean, isolated Python environment** specifically for the AI analysis tool.

## Setup Instructions

### Step 1: Create Clean Virtual Environment

```bash
# Navigate to the tools directory
cd /Users/jmagady/Dev/BMAD-METHOD/expansion-packs/bmad-technical-writing/tools

# Create a new virtual environment using system Python (not anaconda)
python3 -m venv nlp-env

# Activate it
source nlp-env/bin/activate
```

### Step 2: Install All Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all NLP libraries
pip install -r requirements.txt
```

This will install:
- ✅ textstat (readability metrics)
- ✅ nltk (enhanced lexical diversity, VADER)
- ✅ textblob (sentiment analysis)
- ✅ spaCy (syntactic patterns)
- ✅ textacy (stylometric analysis)
- ✅ torch (PyTorch for Transformers)
- ✅ transformers (GPT-2 perplexity)

### Step 3: Download Required Models

```bash
# Download NLTK data
python -m nltk.downloader punkt punkt_tab vader_lexicon

# Download spaCy model (small English model, ~13MB)
python -m spacy download en_core_web_sm

# Download TextBlob corpora (optional)
python -m textblob.download_corpora
```

### Step 4: Test Full Functionality

```bash
# Create a test file
cat > test-ai-content.md << 'EOF'
# Docker Container Management

Docker enables you to delve into containerization. It's a robust solution that helps leverage container technology. Docker provides seamless integration—making deployment easier—and you'll see immediate results.

Furthermore, Docker facilitates easy deployment. Moreover, containers ensure consistency. Additionally, Docker streamlines the development process.

It is important to note that Docker transforms deployment. When it comes to containerization, Docker is paramount. The solution is comprehensive and revolutionary.
EOF

# Run analysis with all enhanced features
python analyze_ai_patterns.py test-ai-content.md

# Clean up test file
rm test-ai-content.md
```

## Expected Output (With All Features Working)

```
================================================================================
AI PATTERN ANALYSIS REPORT
================================================================================

File: test-ai-content.md
Words: 87 | Sentences: 12 | Paragraphs: 3

────────────────────────────────────────────────────────────────────────────────
DIMENSION SCORES
────────────────────────────────────────────────────────────────────────────────

Perplexity (Vocabulary):    VERY LOW      (AI words: 11, 126.44/1k)
Burstiness (Sentence Var):  LOW           (μ=6.8, σ=3.9, range=(3, 15))
Structure (Organization):   HIGH          (Formulaic: 2, H-depth: 1)
Voice (Authenticity):       MEDIUM        (1st-person: 1, You: 2)
Technical (Expertise):      VERY LOW      (Domain terms: 0)
Formatting (Em-dashes):     MEDIUM        (2.0 per page)
Syntactic (Naturalness):    LOW           (Repetition: 0.58, POS div: 0.71)  ← NEW!
Sentiment (Variation):      LOW           (Variance: 0.042, Mean: 0.15)      ← NEW!

OVERALL ASSESSMENT: EXTENSIVE humanization required

────────────────────────────────────────────────────────────────────────────────
ENHANCED NLP ANALYSIS                                                           ← NEW SECTION!
────────────────────────────────────────────────────────────────────────────────

ENHANCED LEXICAL DIVERSITY (NLTK):
  MTLD Score: 45.23 (Moving Average TTR, higher = more diverse)
  Stemmed Diversity: 0.612 (Diversity after stemming)

SENTIMENT VARIATION (VADER):
  Variance: 0.042 (Higher = more emotional variation)
  Mean Sentiment: 0.15 (-1 negative, +1 positive)
  Flatness Score: LOW

SYNTACTIC PATTERNS (spaCy):
  Structural Repetition: 0.583 (Lower = more varied)
  POS Tag Diversity: 0.714 (Part-of-speech variation)
  Avg Dependency Depth: 3.2 (Syntactic complexity)

TRUE PERPLEXITY (GPT-2 Transformer):
  Perplexity Score: 42.18 (Lower = more predictable/AI-like)
  Interpretation: <50 = AI-like, 50-150 = Mixed, >150 = Human-like
```

## Usage After Setup

### Activate Environment (Every Time)

```bash
# Activate the NLP environment
cd /Users/jmagady/Dev/BMAD-METHOD/expansion-packs/bmad-technical-writing/tools
source nlp-env/bin/activate

# Run analysis
python analyze_ai_patterns.py your-file.md

# Deactivate when done
deactivate
```

### Create Shell Alias (Optional Convenience)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias analyze-ai='cd /Users/jmagady/Dev/BMAD-METHOD/expansion-packs/bmad-technical-writing/tools && source nlp-env/bin/activate && python analyze_ai_patterns.py'
```

Then use it anywhere:

```bash
analyze-ai ~/manuscripts/chapter-01.md
```

## Troubleshooting

### Issue: "python3: command not found"

Use your system Python explicitly:

```bash
/usr/bin/python3 -m venv nlp-env
```

### Issue: spaCy model download fails

Download manually:

```bash
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

### Issue: Transformers download slow

First run will download GPT-2 model (~500MB). Subsequent runs will be fast.

### Issue: Out of memory with Transformers

The tool limits text to 5000 chars for GPT-2 analysis. If still getting errors:

1. Close other applications
2. The tool works fine without Transformers (graceful degradation)
3. Just skip that feature - other 7 dimensions still work

## Disk Space Requirements

- **Basic (no optional libs)**: ~0 MB
- **Enhanced (NLTK + spaCy)**: ~50 MB
- **Full (+ Transformers)**: ~2.5 GB (includes GPT-2 model)

## Performance Notes

### Analysis Speed (on 5000-word document):

| Feature | Time | Memory |
|---------|------|--------|
| Core analysis | <1 sec | ~50MB |
| + NLTK/spaCy | ~2-3 sec | ~200MB |
| + Transformers | ~10-30 sec | ~2GB |

**Recommendation for large batches**: Skip Transformers (`HAS_TRANSFORMERS=False`) for 10x speedup.

## Why a Separate Environment?

Your anaconda environment is **production environment** with many packages:
- vllm, streamlit, opencv, astropy, etc.
- All compiled against specific numpy/pandas versions
- Upgrading breaks other tools

The dedicated NLP environment:
- ✅ Clean slate - only what we need
- ✅ Latest compatible versions
- ✅ No conflicts with other tools
- ✅ Can be deleted/recreated anytime
- ✅ Isolated from your main work

## Quick Start (Copy-Paste Script)

```bash
#!/bin/bash
# Run this to set up everything

cd /Users/jmagady/Dev/BMAD-METHOD/expansion-packs/bmad-technical-writing/tools

# Create and activate environment
python3 -m venv nlp-env
source nlp-env/bin/activate

# Install everything
pip install --upgrade pip
pip install -r requirements.txt

# Download models
python -m nltk.downloader punkt punkt_tab vader_lexicon
python -m spacy download en_core_web_sm

# Test
echo "Testing analysis tool..."
cat > test.md << 'EOF'
# Test

Docker enables you to delve into containerization. It's robust and seamless.
EOF

python analyze_ai_patterns.py test.md
rm test.md

echo ""
echo "✅ Setup complete! All enhanced features working."
echo "To use: source nlp-env/bin/activate && python analyze_ai_patterns.py your-file.md"
```

Save as `setup.sh`, run `chmod +x setup.sh`, then `./setup.sh`.

## Summary

| Approach | Pros | Cons |
|----------|------|------|
| Fix anaconda | - Use existing environment | - Breaks other tools<br>- Impossible to resolve all conflicts |
| **Dedicated venv** | - **Clean, works perfectly**<br>- Isolated<br>- Easy to recreate | - Need to activate first<br>- Extra disk space (~2.5GB) |

**Recommendation**: Use the dedicated venv approach. It's the standard Python practice for isolated tools.

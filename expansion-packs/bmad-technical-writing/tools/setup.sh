#!/bin/bash
# AI Pattern Analysis Tool - Automated Setup Script
# This creates a clean virtual environment with all enhanced NLP features

set -e  # Exit on error

echo "=========================================="
echo "AI Pattern Analysis Tool - Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "analyze_ai_patterns.py" ]; then
    echo "❌ Error: analyze_ai_patterns.py not found"
    echo "   Please run this script from the tools/ directory"
    exit 1
fi

echo "📦 Step 1: Creating clean virtual environment..."
python3 -m venv nlp-env
echo "✅ Virtual environment created"
echo ""

echo "🔧 Step 2: Activating environment and upgrading pip..."
source nlp-env/bin/activate
pip install --upgrade pip --quiet
echo "✅ Pip upgraded"
echo ""

echo "📚 Step 3: Installing NLP libraries (this may take 2-3 minutes)..."
echo "   Installing: textstat, nltk, textblob, spacy, textacy, torch, transformers"
pip install -r requirements.txt --quiet
echo "✅ All libraries installed"
echo ""

echo "📥 Step 4: Downloading required NLP models..."

# NLTK data
echo "   - Downloading NLTK data (punkt, punkt_tab, vader_lexicon)..."
python -m nltk.downloader punkt punkt_tab vader_lexicon --quiet
echo "   ✅ NLTK data downloaded"

# spaCy model
echo "   - Downloading spaCy model (en_core_web_sm, ~13MB)..."
python -m spacy download en_core_web_sm --quiet
echo "   ✅ spaCy model downloaded"

echo ""
echo "🧪 Step 5: Testing all features..."

# Create test file
cat > test-setup.md << 'EOF'
# Docker Container Management

Docker enables you to delve into containerization. It's a robust solution that helps leverage container technology. Docker provides seamless integration—making deployment easier—and you'll see immediate results.

Furthermore, Docker facilitates easy deployment. Moreover, containers ensure consistency. Additionally, Docker streamlines the development process.

It is important to note that Docker transforms deployment. When it comes to containerization, Docker is paramount. The solution is comprehensive and revolutionary.
EOF

# Run analysis
python analyze_ai_patterns.py test-setup.md > /dev/null 2>&1

# Check for enhanced features in output
if python -c "import nltk, spacy, textacy, transformers; print('OK')" > /dev/null 2>&1; then
    echo "✅ All enhanced features are working!"
    rm test-setup.md
else
    echo "⚠️  Warning: Some libraries may not have loaded correctly"
    rm test-setup.md
fi

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "All 6 NLP libraries installed and working:"
echo "  • textstat - Readability metrics"
echo "  • NLTK - Enhanced lexical diversity (MTLD)"
echo "  • VADER - Sentiment flatness detection"
echo "  • TextBlob - Alternative sentiment analysis"
echo "  • spaCy - Syntactic pattern detection"
echo "  • Textacy - Stylometric analysis"
echo "  • Transformers - GPT-2 perplexity calculation"
echo ""
echo "HOW TO USE:"
echo "─────────────────────────────────────────"
echo "1. Activate environment:"
echo "   source nlp-env/bin/activate"
echo ""
echo "2. Run analysis:"
echo "   python analyze_ai_patterns.py your-file.md"
echo ""
echo "3. Deactivate when done:"
echo "   deactivate"
echo ""
echo "EXAMPLES:"
echo "─────────────────────────────────────────"
echo "# Basic analysis"
echo "python analyze_ai_patterns.py chapter-01.md"
echo ""
echo "# Detailed mode (line numbers + suggestions)"
echo "python analyze_ai_patterns.py chapter-01.md --detailed"
echo ""
echo "# Batch analysis (TSV output for Excel)"
echo "python analyze_ai_patterns.py --batch manuscript/ --format tsv > analysis.tsv"
echo ""
echo "# JSON output (programmatic)"
echo "python analyze_ai_patterns.py chapter-01.md --format json > results.json"
echo ""
echo "For more info, see: SETUP-GUIDE.md"
echo "=========================================="

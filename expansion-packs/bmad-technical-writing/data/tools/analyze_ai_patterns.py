#!/usr/bin/env python3
"""
AI Pattern Analysis Tool for Technical Writing - MODULAR EDITION

Entry point wrapper for the AI Pattern Analyzer CLI.
The actual implementation has been moved to ai_pattern_analyzer.cli.main

Usage:
    # Basic analysis (no libraries required)
    python analyze_ai_patterns.py <file_path>

    # Enhanced analysis with all NLP features
    pip install -r requirements.txt
    python analyze_ai_patterns.py <file_path>

    # See --help for all options
    python analyze_ai_patterns.py --help

Version: 4.0.0 (Modular Architecture with Analysis Modes)
"""

# Import and run main from modular CLI
from ai_pattern_analyzer.cli.main import main

if __name__ == '__main__':
    main()

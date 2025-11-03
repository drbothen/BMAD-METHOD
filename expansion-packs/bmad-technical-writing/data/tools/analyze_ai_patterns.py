#!/usr/bin/env python3
"""
AI Pattern Analysis Tool for Technical Writing - MODULAR EDITION

Analyzes manuscripts for AI-generated content patterns across 22 dimensions:

CORE DIMENSIONS (Always Available):
- Perplexity (vocabulary patterns, AI-characteristic words)
- Burstiness (sentence length variation)
- Structure (transitions, lists, headings)
- Voice (authenticity markers, contractions)
- Technical depth (domain expertise indicators)
- Formatting (em-dashes, bold, italics)
- Lexical diversity (Type-Token Ratio)

ENHANCED DIMENSIONS (Optional NLP Libraries):
- NLTK: Enhanced lexical diversity (MTLD), stemmed diversity
- VADER: Sentiment variation across paragraphs (detects flatness)
- spaCy: Syntactic pattern repetition, POS diversity, dependency depth
- Textacy: Stylometric analysis, automated readability
- Transformers: True perplexity calculation using GPT-2 model

NEW: Phase 3 Advanced Structure Analysis (AST-based):
- Paragraph length coefficient of variation (CV ≥0.4 = human-like)
- Section length variance (≥40% variance = human-like)
- List nesting depth analysis (≤3 levels = human-like)
- MATTR & RTTR lexical diversity (textacy-based)
- Heading length patterns & asymmetry
- Subsection count asymmetry (CV ≥0.6 = human-like)
- Heading depth transition patterns (lateral moves = human-like)

All enhanced features use graceful degradation - script works without optional dependencies.

Based on research from:
- ai-detection-patterns.md
- formatting-humanization-patterns.md
- heading-humanization-patterns.md
- humanization-techniques.md
- Academic NLP research (GPTZero, Originality.AI methodologies)

Usage:
    # Basic analysis (no libraries required)
    python analyze_ai_patterns.py <file_path>

    # Enhanced analysis with all NLP features
    pip install -r requirements.txt
    python analyze_ai_patterns.py <file_path>

    # Detailed mode with line numbers and suggestions
    python analyze_ai_patterns.py <file_path> --detailed

    # Dual score analysis with optimization path
    python analyze_ai_patterns.py <file_path> --show-scores

    # Dual score with custom targets
    python analyze_ai_patterns.py <file_path> --show-scores --quality-target 90 --detection-target 20

    # Batch analyze directory
    python analyze_ai_patterns.py --batch <directory> --format tsv > results.tsv

Version: 4.0.0 (Modular Architecture)
"""

import sys
import argparse
from pathlib import Path

# Import from modular structure
from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
from ai_pattern_analyzer.cli.formatters import (
    format_report,
    format_detailed_report,
    format_dual_score_report
)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Analyze manuscripts for AI-generated content patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single file
  %(prog)s chapter-01.md

  # Detailed analysis with line numbers and suggestions (for LLM-driven humanization)
  %(prog)s chapter-01.md --detailed

  # Dual score analysis with optimization path (recommended for LLM optimization)
  %(prog)s chapter-01.md --show-scores

  # Dual score with custom targets
  %(prog)s chapter-01.md --show-scores --quality-target 90 --detection-target 20

  # Dual score JSON output (for programmatic use)
  %(prog)s chapter-01.md --show-scores --format json

  # Analyze with custom domain terms
  %(prog)s chapter-01.md --domain-terms "Docker,Kubernetes,PostgreSQL"

  # Batch analyze directory, output TSV
  %(prog)s --batch manuscript/sections --format tsv > analysis.tsv

  # Save detailed analysis to file
  %(prog)s chapter-01.md --detailed -o humanization-report.txt
        """
    )

    parser.add_argument('file', nargs='?', help='Markdown file to analyze')
    parser.add_argument('--batch', metavar='DIR', help='Analyze all .md files in directory')
    parser.add_argument('--detailed', action='store_true',
                        help='Provide detailed line-by-line diagnostics with context and suggestions (for LLM cleanup)')
    parser.add_argument('--format', choices=['text', 'json', 'tsv'], default='text',
                        help='Output format (default: text)')
    parser.add_argument('--domain-terms', metavar='TERMS',
                        help='Comma-separated domain-specific terms to detect (overrides defaults)')
    parser.add_argument('--output', '-o', metavar='FILE', help='Write output to file instead of stdout')

    # Dual scoring options
    parser.add_argument('--scores-detailed', action='store_true',
                        help='Show detailed dual score breakdown with full tier analysis and optimization path')
    parser.add_argument('--show-scores', action='store_true', dest='scores_detailed',
                        help='(Deprecated: use --scores-detailed) Show detailed dual score breakdown')
    parser.add_argument('--no-score-summary', action='store_true',
                        help='Omit quality score summary from standard report')
    parser.add_argument('--no-track-history', action='store_true',
                        help='Disable saving score history to .ai-analysis-history/ directory')
    parser.add_argument('--detection-target', type=float, default=30.0, metavar='N',
                        help='Target detection risk score (0-100, lower=better, default: 30.0)')
    parser.add_argument('--quality-target', type=float, default=85.0, metavar='N',
                        help='Target quality score (0-100, higher=better, default: 85.0)')

    args = parser.parse_args()

    # Validate inputs
    if not args.file and not args.batch:
        parser.error('Either FILE or --batch DIR must be specified')

    # Detailed mode limitations
    if args.detailed and args.batch:
        print("Warning: --detailed mode not supported for batch analysis. Using standard mode.", file=sys.stderr)
        args.detailed = False

    if args.detailed and args.format == 'tsv':
        print("Warning: --detailed mode not compatible with TSV format. Using JSON format.", file=sys.stderr)
        args.format = 'json'

    # Parse domain terms if provided
    domain_terms = None
    if args.domain_terms:
        domain_terms = [rf'\b{term.strip()}\b' for term in args.domain_terms.split(',')]

    # Initialize analyzer
    analyzer = AIPatternAnalyzer(domain_terms=domain_terms)

    # Process files
    if args.detailed:
        # Detailed analysis mode (single file only)
        try:
            detailed_result = analyzer.analyze_file_detailed(args.file)
            output_text = format_detailed_report(detailed_result, args.format)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                print(f"Detailed analysis written to {args.output}", file=sys.stderr)
            else:
                print(output_text)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.scores_detailed:
        # Detailed scoring mode (standard report + full dual score breakdown)
        if args.batch:
            print("Warning: --scores-detailed mode not supported for batch analysis. Using standard mode.", file=sys.stderr)
            args.scores_detailed = False
        else:
            try:
                # Run standard analysis first
                result = analyzer.analyze_file(args.file)

                # Calculate dual score
                dual_score = analyzer.calculate_dual_score(
                    result,
                    detection_target=args.detection_target,
                    quality_target=args.quality_target
                )

                # Load and save history (unless disabled)
                if not args.no_track_history:
                    history = analyzer.load_score_history(args.file)
                    history.add_score(dual_score, notes="")
                    analyzer.save_score_history(history)
                else:
                    # Create empty history for display purposes
                    from ai_pattern_analyzer.history.tracker import ScoreHistory
                    history = ScoreHistory(file_path=args.file, scores=[])

                # Generate dual score section first (will be inserted at top of report)
                dual_score_section = format_dual_score_report(
                    dual_score,
                    history,
                    args.format,
                    as_detailed_section=True  # Format as continuation, not standalone
                )

                # Generate full report with dual score at top
                output_text = format_report(
                    result,
                    args.format,
                    include_score_summary=False,  # Don't show summary - detailed breakdown is shown at top
                    detection_target=args.detection_target,
                    quality_target=args.quality_target,
                    dual_score_section=dual_score_section  # Insert at top, after header
                )

                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(output_text)
                    print(f"Detailed analysis written to {args.output}", file=sys.stderr)
                else:
                    print(output_text)

            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

    else:
        # Standard analysis mode
        results = []

        if args.batch:
            # Batch mode
            batch_dir = Path(args.batch)
            if not batch_dir.is_dir():
                print(f"Error: {args.batch} is not a directory", file=sys.stderr)
                sys.exit(1)

            md_files = sorted(batch_dir.glob('**/*.md'))
            if not md_files:
                print(f"Error: No .md files found in {args.batch}", file=sys.stderr)
                sys.exit(1)

            for md_file in md_files:
                try:
                    result = analyzer.analyze_file(str(md_file))
                    results.append(result)
                except Exception as e:
                    print(f"Error analyzing {md_file}: {e}", file=sys.stderr)

        else:
            # Single file mode
            try:
                result = analyzer.analyze_file(args.file)
                results.append(result)

                # Calculate dual score for history and optimization
                # (needed when score summary is shown)
                calculated_dual_score = None
                if not args.no_score_summary and args.format == 'text':
                    try:
                        calculated_dual_score = analyzer.calculate_dual_score(
                            result,
                            detection_target=args.detection_target,
                            quality_target=args.quality_target
                        )

                        # Save to history (unless disabled)
                        if not args.no_track_history:
                            history = analyzer.load_score_history(args.file)
                            history.add_score(calculated_dual_score, notes="")
                            analyzer.save_score_history(history)

                    except Exception as e:
                        # Don't fail the entire run if history tracking fails
                        print(f"Warning: Could not calculate/save score history: {e}", file=sys.stderr)

            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

        # Format and output
        output_lines = []

        if args.format == 'tsv' and len(results) > 1:
            # TSV batch output with header
            output_lines.append(format_report(results[0], 'tsv').split('\n')[0])  # Header
            for r in results:
                output_lines.append(format_report(r, 'tsv').split('\n')[1])  # Data row
        else:
            # Individual reports
            for r in results:
                # Pass pre-calculated dual_score only for single file mode
                dual_score_param = calculated_dual_score if (len(results) == 1 and not args.batch) else None

                output_lines.append(format_report(
                    r,
                    args.format,
                    include_score_summary=not args.no_score_summary,
                    detection_target=args.detection_target,
                    quality_target=args.quality_target,
                    dual_score=dual_score_param
                ))

        output_text = '\n'.join(output_lines)

        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"Analysis written to {args.output}", file=sys.stderr)
        else:
            print(output_text)


if __name__ == '__main__':
    main()

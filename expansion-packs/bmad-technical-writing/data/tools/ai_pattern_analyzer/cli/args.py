"""
Command-line argument parsing.

This module handles all CLI argument definitions and parsing.
"""

import argparse
import sys


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
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
    parser.add_argument('--show-scores', action='store_true',
                        help='Calculate and display dual scores (Detection Risk + Quality Score) with optimization path')
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

    # Show scores validation
    if args.show_scores and args.batch:
        print("Warning: --show-scores mode not supported for batch analysis. Using standard mode.", file=sys.stderr)
        args.show_scores = False

    return args


def parse_domain_terms(domain_terms_str: str):
    """
    Parse domain terms from comma-separated string.

    Args:
        domain_terms_str: Comma-separated domain terms

    Returns:
        List of regex patterns for domain terms
    """
    if not domain_terms_str:
        return None

    return [rf'\b{term.strip()}\b' for term in domain_terms_str.split(',')]

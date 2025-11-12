"""
CLI main entry point using Click framework.

This module provides the command-line interface for AI Pattern Analyzer.
After installation, it's accessible via the `analyze-ai-patterns` command.

Usage:
    analyze-ai-patterns FILE [OPTIONS]
    analyze-ai-patterns --batch DIR [OPTIONS]

Extension Points:
    - Refactored from argparse to Click for better UX (Story 1.4.10)
    - Maintains 100% backward compatibility with Story 1.4.9
    - Future: Consider command groups for better organization
"""

import sys
import os
from pathlib import Path
import click

from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
from ai_pattern_analyzer.core.analysis_config import AnalysisConfig, AnalysisMode
from ai_pattern_analyzer.cli.formatters import (
    format_report,
    format_detailed_report,
    format_dual_score_report
)


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


def show_mode_help():
    """Display detailed information about analysis modes."""
    print('''
╔═══════════════════════════════════════════════════════════════════════════╗
║                        ANALYSIS MODES - QUICK REFERENCE                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│ FAST MODE - Quick Preview                                                │
├─────────────────────────────────────────────────────────────────────────┤
│ Speed:    5-15 seconds for any document size                            │
│ Coverage: ~1-5% of document (first 2000 chars per dimension)            │
│ Use When: Quick preview, interactive editing, draft checks              │
│ Note:     Inaccurate for long documents, only analyzes first page       │
│                                                                           │
│ Example:  analyze-ai-patterns chapter.md --mode fast                    │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ ADAPTIVE MODE - Smart Sampling (RECOMMENDED, DEFAULT)                    │
├─────────────────────────────────────────────────────────────────────────┤
│ Speed:    30-240 seconds for 90-page chapters                           │
│ Coverage: 10-20% of document (adapts to length)                         │
│ Use When: Book chapters, long documents, regular analysis               │
│ Behavior: <5k chars = full, 5k-50k = 5 samples, >50k = 10 samples      │
│                                                                           │
│ Example:  analyze-ai-patterns chapter.md                                │
│           analyze-ai-patterns chapter.md --mode adaptive                │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ SAMPLING MODE - Custom Configuration                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ Speed:    60-300 seconds (depends on configuration)                     │
│ Coverage: Configurable (samples × sample-size)                          │
│ Use When: Specific requirements, testing, research                      │
│ Options:  --samples N (1-20, default: 5)                                │
│           --sample-size CHARS (500-10000, default: 2000)                │
│           --sample-strategy even|weighted|adaptive (default: even)      │
│                                                                           │
│ Example:  analyze-ai-patterns chapter.md --mode sampling \\              │
│             --samples 7 --sample-size 3000 --sample-strategy weighted   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ FULL MODE - Maximum Accuracy                                             │
├─────────────────────────────────────────────────────────────────────────┤
│ Speed:    5-20 minutes for 90-page chapters (VERY SLOW)                 │
│ Coverage: 100% of document (analyzes every word)                        │
│ Use When: Final validation, publication-ready, research                 │
│ Warning:  Very slow for long documents, consider adaptive for most use  │
│                                                                           │
│ Example:  analyze-ai-patterns chapter.md --mode full                    │
└─────────────────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════╗
║                         PERFORMANCE COMPARISON                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

For a 90-page chapter (~180,000 characters):

┌──────────────┬─────────────┬────────────┬─────────────────────────────┐
│ Mode         │ Time        │ Coverage   │ Best For                    │
├──────────────┼─────────────┼────────────┼─────────────────────────────┤
│ FAST         │   5-15s     │    1-5%    │ Quick drafts, previews      │
│ ADAPTIVE     │  30-240s    │   10-20%   │ Book chapters (RECOMMENDED) │
│ SAMPLING     │  60-300s    │  Custom    │ Custom requirements         │
│ FULL         │ 5-20 min    │   100%     │ Final validation            │
└──────────────┴─────────────┴────────────┴─────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════╗
║                          INTEGRATION WITH FEATURES                        ║
╚═══════════════════════════════════════════════════════════════════════════╝

Mode works with ALL existing features:

  --batch DIR          Mode applies to all files in batch
  --detailed           Detailed diagnostics with mode info
  --show-scores        Dual scoring with mode in report
  --show-history-full  History shows mode for each iteration
  --format json        Mode included in JSON output

Examples:
  # Batch analysis with adaptive mode
  analyze-ai-patterns --batch manuscript/ --mode adaptive

  # Detailed analysis with fast mode (quick iteration)
  analyze-ai-patterns chapter.md --mode fast --detailed

  # Dual scoring with full mode (publication check)
  analyze-ai-patterns chapter.md --mode full --show-scores

  # Check what mode would do
  analyze-ai-patterns chapter.md --mode adaptive --dry-run

For complete documentation: docs/analysis-modes-guide.md
    ''')


def create_analysis_config(mode, samples, sample_size, sample_strategy, profile='balanced'):
    """
    Create AnalysisConfig from CLI arguments.

    Args:
        mode: Analysis mode string
        samples: Number of sampling sections
        sample_size: Characters per sample section
        sample_strategy: Sampling strategy
        profile: Dimension profile (fast/balanced/full)

    Returns:
        AnalysisConfig instance
    """
    return AnalysisConfig(
        mode=AnalysisMode(mode),
        sampling_sections=samples,
        sampling_chars_per_section=sample_size,
        sampling_strategy=sample_strategy,
        dimension_profile=profile
    )


def show_dry_run_config(file_path: str, config: AnalysisConfig, detailed, show_scores):
    """Display configuration for dry-run mode."""
    file_size = os.path.getsize(file_path)
    pages = file_size / 2000

    print("=" * 75)
    print("ANALYSIS CONFIGURATION (DRY RUN)")
    print("=" * 75)
    print(f"File: {file_path}")
    print(f"Size: {file_size:,} characters (~{pages:.0f} pages)")
    print()
    print(f"Mode: {config.mode.value.upper()}")
    print()

    if config.mode == AnalysisMode.FAST:
        print("Behavior: Truncate to 2000 chars per dimension")
        print("Expected time: 5-15 seconds")
        print("Coverage: ~1-5% of document")
        if pages > 10:
            print()
            print("⚠  Warning: FAST mode only analyzes first page.")
            print("   For accurate results on long documents, use --mode adaptive")

    elif config.mode == AnalysisMode.ADAPTIVE:
        if file_size < 5000:
            print("Behavior: Full analysis (document < 5k chars)")
            print("Expected time: 10-30 seconds")
            print("Coverage: 100%")
        elif file_size < 50000:
            samples = 5
            print(f"Behavior: Sample {samples} sections throughout document")
            print("Expected time: 30-90 seconds")
            print(f"Coverage: ~{(samples * 2000 / file_size * 100):.1f}%")
        else:
            samples = 10
            print(f"Behavior: Sample {samples} sections throughout document")
            print("Expected time: 60-240 seconds")
            print(f"Coverage: ~{(samples * 2000 / file_size * 100):.1f}%")

    elif config.mode == AnalysisMode.SAMPLING:
        print(f"Behavior: Sample {config.sampling_sections} sections")
        print(f"          {config.sampling_chars_per_section} chars per section")
        print(f"          Strategy: {config.sampling_strategy}")
        total = config.sampling_sections * config.sampling_chars_per_section
        print(f"Expected time: {30 + config.sampling_sections * 10}-{60 + config.sampling_sections * 20} seconds")
        print(f"Coverage: ~{(total / file_size * 100):.1f}%")

    elif config.mode == AnalysisMode.FULL:
        print("Behavior: Analyze entire document, no truncation")
        print(f"Expected time: {pages * 2:.0f}-{pages * 10:.0f} seconds")
        print("Coverage: 100%")
        if pages > 100:
            print()
            print("⚠  Warning: FULL mode on large documents is VERY SLOW")
            print("   Consider --mode adaptive for faster results (30-240s)")

    print()

    # Show integration with other features
    if detailed:
        print("Additional: Detailed diagnostics enabled")
    if show_scores:
        print("Additional: Dual score analysis enabled")

    print()
    print("To run analysis: Remove --dry-run flag")
    print("=" * 75)


def show_coverage_stats(result, config: AnalysisConfig, file_path: str):
    """Display coverage statistics after analysis."""
    file_size = os.path.getsize(file_path)

    print()
    print("=" * 75)
    print("COVERAGE STATISTICS")
    print("=" * 75)

    # Calculate actual coverage from metadata if available
    if hasattr(result, 'metadata') and 'coverage' in result.metadata:
        actual_coverage = result.metadata['coverage']
        chars_analyzed = result.metadata.get('chars_analyzed', 0)
        print(f"Characters analyzed: {chars_analyzed:,} of {file_size:,} ({actual_coverage:.1f}%)")
    else:
        # Estimate based on mode
        if config.mode == AnalysisMode.FAST:
            est_coverage = min(2000 * 12 / file_size * 100, 100)  # 12 dimensions × 2000 chars
            print(f"Mode: FAST (estimated ~{est_coverage:.1f}% coverage)")
        elif config.mode == AnalysisMode.FULL:
            print(f"Mode: FULL (100% coverage)")
        elif config.mode in [AnalysisMode.SAMPLING, AnalysisMode.ADAPTIVE]:
            total = config.sampling_sections * config.sampling_chars_per_section
            est_coverage = min(total / file_size * 100, 100)
            print(f"Mode: {config.mode.value.upper()}")
            print(f"Sections sampled: {config.sampling_sections}")
            print(f"Characters per section: {config.sampling_chars_per_section:,}")
            print(f"Estimated coverage: ~{est_coverage:.1f}%")

    print("=" * 75)
    print()


def handle_history_commands(file, show_history_full, compare_history,
                            show_dimension_trends, show_raw_metric_trends, export_history):
    """
    Handle history viewing commands (--show-history-full, --compare-history, etc.).

    Args:
        file: File path
        show_history_full: Show full history flag
        compare_history: Compare iterations string
        show_dimension_trends: Show dimension trends flag
        show_raw_metric_trends: Show raw metric trends flag
        export_history: Export format (csv or json)

    Returns:
        Exit code (0 for success)
    """
    from ai_pattern_analyzer.history.trends import (
        generate_full_history_report,
        generate_comparison_report,
        generate_dimension_trend_report,
        generate_raw_metric_trends
    )

    analyzer = AIPatternAnalyzer()
    history = analyzer.load_score_history(file)

    if len(history.scores) == 0:
        print(f"No history found for {file}", file=sys.stderr)
        print("Run analysis with --show-scores first to create history.", file=sys.stderr)
        return 1

    # Generate and print requested report
    if show_history_full:
        print(generate_full_history_report(history))

    elif compare_history:
        # Parse iteration specifiers (e.g., "first,last" or "1,5")
        parts = compare_history.split(',')
        if len(parts) != 2:
            print('Error: --compare-history requires two iterations separated by comma', file=sys.stderr)
            return 1

        # Convert to indices
        def parse_iteration(spec: str, history_len: int) -> int:
            spec = spec.strip().lower()
            if spec == 'first':
                return 0
            elif spec == 'last':
                return history_len - 1
            else:
                try:
                    idx = int(spec)
                    if idx < 0 or idx >= history_len:
                        raise ValueError(f"Iteration {idx} out of range (0-{history_len-1})")
                    return idx
                except ValueError as e:
                    raise ValueError(f"Invalid iteration specifier: {spec}")

        try:
            idx1 = parse_iteration(parts[0], len(history.scores))
            idx2 = parse_iteration(parts[1], len(history.scores))
            print(generate_comparison_report(history, idx1, idx2))
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif show_dimension_trends:
        print(generate_dimension_trend_report(history))

    elif show_raw_metric_trends:
        print(generate_raw_metric_trends(history))

    elif export_history:
        if export_history == 'csv':
            output_file = file.replace('.md', '-history.csv')
            history.export_to_csv(output_file)
            print(f"History exported to: {output_file}")
        elif export_history == 'json':
            output_file = file.replace('.md', '-history.json')
            import json
            with open(output_file, 'w') as f:
                json.dump(history.to_dict(), f, indent=2)
            print(f"History exported to: {output_file}")

    return 0


def run_single_file_analysis(file, mode, samples, sample_size, sample_strategy, profile,
                             dry_run, show_coverage, detection_target, quality_target,
                             history_notes, no_track_history, no_score_summary, format):
    """
    Run analysis on a single file.

    Args:
        file: File path
        mode: Analysis mode
        samples: Number of samples
        sample_size: Sample size in characters
        sample_strategy: Sampling strategy
        dry_run: Dry run flag
        show_coverage: Show coverage flag
        detection_target: Detection target score
        quality_target: Quality target score
        history_notes: Notes for this iteration
        no_track_history: Disable history tracking flag
        no_score_summary: Suppress score summary flag
        format: Output format

    Returns:
        List of results and calculated dual score
    """
    import time

    try:
        # Create config
        config = create_analysis_config(mode, samples, sample_size, sample_strategy, profile)

        # Parse domain terms if needed (handled in main function)
        analyzer = AIPatternAnalyzer(config=config)

        # Dry run
        if dry_run:
            show_dry_run_config(file, config, False, False)
            return [], None

        # Display mode info (only for text format, to avoid breaking JSON/TSV output)
        if format == 'text':
            print(f"\nAnalyzing: {file}")
            print(f"Mode: {config.mode.value.upper()}", end='')

            if config.mode in [AnalysisMode.SAMPLING, AnalysisMode.ADAPTIVE]:
                print(f" (sampling: {config.sampling_sections} × {config.sampling_chars_per_section} chars, {config.sampling_strategy})")
            else:
                print()

            if show_coverage:
                print("Coverage statistics will be shown after analysis")
            print()

        # Run analysis with timing
        start_time = time.time()
        result = analyzer.analyze_file(file, config=config)
        elapsed = time.time() - start_time

        # Add mode info to results metadata (for history tracking)
        if not hasattr(result, 'metadata'):
            result.metadata = {}
        result.metadata['analysis_mode'] = config.mode.value
        result.metadata['analysis_time_seconds'] = elapsed

        # Calculate dual score for history and optimization (if score summary shown)
        calculated_dual_score = None
        if not no_score_summary and format == 'text':
            try:
                calculated_dual_score = analyzer.calculate_dual_score(
                    result,
                    detection_target=detection_target,
                    quality_target=quality_target
                )

                # Save to history (unless disabled)
                if not no_track_history:
                    history = analyzer.load_score_history(file)
                    history.add_score(calculated_dual_score, notes=history_notes)
                    analyzer.save_score_history(history)

            except Exception as e:
                # Don't fail if history tracking fails
                print(f"Warning: Could not calculate/save score history: {e}", file=sys.stderr)

        # Show coverage if requested
        if show_coverage:
            show_coverage_stats(result, config, file)

        # Display elapsed time (only for text format, to avoid breaking JSON/TSV output)
        if format == 'text':
            print(f"\nCompleted in {elapsed:.1f} seconds")

        return [result], calculated_dual_score

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def run_batch_analysis(batch_dir, mode, samples, sample_size, sample_strategy, profile, dry_run):
    """
    Run batch analysis on directory.

    Args:
        batch_dir: Directory path
        mode: Analysis mode
        samples: Number of samples
        sample_size: Sample size in characters
        sample_strategy: Sampling strategy
        dry_run: Dry run flag

    Returns:
        List of results and None for dual_score
    """
    # Create config once (applies to all files)
    config = create_analysis_config(mode, samples, sample_size, sample_strategy, profile)

    # Parse domain terms if needed (handled in main function)
    analyzer = AIPatternAnalyzer(config=config)

    # Dry run for batch
    if dry_run:
        print(f"\nBatch Analysis Configuration (DRY RUN)")
        print(f"Directory: {batch_dir}")
        print(f"Mode: {config.mode.value.upper()}")
        if config.mode in [AnalysisMode.SAMPLING, AnalysisMode.ADAPTIVE]:
            print(f"Sampling: {config.sampling_sections} × {config.sampling_chars_per_section} chars ({config.sampling_strategy})")
        print(f"\nMode will be applied to all .md files in directory")
        return [], None

    batch_path = Path(batch_dir)
    if not batch_path.is_dir():
        print(f"Error: {batch_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    md_files = sorted(batch_path.glob('**/*.md'))
    if not md_files:
        print(f"Error: No .md files found in {batch_dir}", file=sys.stderr)
        sys.exit(1)

    # Display batch mode info
    print(f"\nBatch Analysis Mode: {config.mode.value.upper()}")
    if config.mode in [AnalysisMode.SAMPLING, AnalysisMode.ADAPTIVE]:
        print(f"Sampling: {config.sampling_sections} × {config.sampling_chars_per_section} chars")
    print(f"Files to analyze: {len(md_files)}")
    print()

    results = []
    for md_file in md_files:
        try:
            print(f"Analyzing: {md_file.name}...", end=' ', flush=True)

            result = analyzer.analyze_file(str(md_file), config=config)
            results.append(result)

            print("✓")
        except Exception as e:
            print(f"Error analyzing {md_file}: {e}", file=sys.stderr)

    print(f"\nCompleted {len(results)} of {len(md_files)} files")

    return results, None


# Click command definition
@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('file', required=False, type=click.Path(exists=True))
@click.option('--batch', metavar='DIR', type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help='Analyze all .md files in directory')
@click.option('--detailed', is_flag=True,
              help='Provide detailed line-by-line diagnostics with context and suggestions (for LLM cleanup)')
@click.option('--format', type=click.Choice(['text', 'json', 'tsv']), default='text',
              help='Output format (default: text)')
@click.option('--domain-terms', metavar='TERMS',
              help='Comma-separated domain-specific terms to detect (overrides defaults)')
@click.option('--output', '-o', metavar='FILE', type=click.File('w'),
              help='Write output to file instead of stdout')
@click.option('--show-scores', is_flag=True,
              help='Calculate and display dual scores (Detection Risk + Quality Score) with optimization path')
@click.option('--detection-target', type=float, default=30.0, metavar='N',
              help='Target detection risk score (0-100, lower=better, default: 30.0)')
@click.option('--quality-target', type=float, default=85.0, metavar='N',
              help='Target quality score (0-100, higher=better, default: 85.0)')
@click.option('--show-history', is_flag=True,
              help='Show aggregate score trends (quality/detection)')
@click.option('--show-history-full', is_flag=True,
              help='Show complete optimization journey with all iterations')
@click.option('--show-dimension-trends', is_flag=True,
              help='Show trends for all dimensions (v2.0 data required)')
@click.option('--show-raw-metric-trends', is_flag=True,
              help='Show raw metric trends with sparklines (v2.0 data required)')
@click.option('--compare-history', type=str, metavar='I1,I2',
              help='Compare two iterations (e.g., "first,last" or "1,5")')
@click.option('--export-history', type=click.Choice(['csv', 'json']), metavar='FORMAT',
              help='Export history to CSV or JSON format')
@click.option('--history-notes', type=str, default="", metavar='NOTES',
              help='Add notes for this iteration (e.g., "Fixed AI vocabulary")')
@click.option('--no-score-summary', is_flag=True,
              help='Suppress score summary display in output')
@click.option('--mode', '-m', type=click.Choice(['fast', 'adaptive', 'sampling', 'full']),
              default='adaptive',
              help='Analysis mode: fast (5-15s), adaptive (30-240s, RECOMMENDED), sampling (60-300s), full (5-20min)')
@click.option('--profile', '-p', type=click.Choice(['fast', 'balanced', 'full']),
              default='balanced',
              help='Dimension profile: fast (4 dims, ~100ms), balanced (8 dims, ~200ms, DEFAULT), full (12 dims, ~4-6s)')
@click.option('--samples', type=click.IntRange(1, 20), default=5, metavar='N',
              help='Number of sections to sample (default: 5, range: 1-20)')
@click.option('--sample-size', type=click.IntRange(500, 10000), default=2000, metavar='CHARS',
              help='Characters per sample section (default: 2000, range: 500-10000)')
@click.option('--sample-strategy', type=click.Choice(['even', 'weighted', 'adaptive']),
              default='even',
              help='Sampling distribution: even, weighted (40%% begin/40%% end), adaptive')
@click.option('--dry-run', is_flag=True,
              help='Show configuration without running analysis')
@click.option('--show-coverage', is_flag=True,
              help='Display coverage statistics (samples, chars analyzed, coverage %%)')
@click.option('--help-modes', is_flag=True, is_eager=True, expose_value=False, callback=lambda ctx, param, value: (show_mode_help(), ctx.exit()) if value else None,
              help='Show detailed information about analysis modes and exit')
@click.option('--no-track-history', is_flag=True, hidden=True,
              help='Disable history tracking (internal use)')
def main(file, batch, detailed, format, domain_terms, output, show_scores,
         detection_target, quality_target, show_history, show_history_full,
         show_dimension_trends, show_raw_metric_trends, compare_history,
         export_history, history_notes, no_score_summary, mode, profile, samples,
         sample_size, sample_strategy, dry_run, show_coverage, no_track_history):
    """Analyze manuscripts for AI-generated content patterns.

    Examples:

      # Analyze single file (default: adaptive mode)
      analyze-ai-patterns chapter-01.md

      # Quick preview with fast mode (5-15 seconds)
      analyze-ai-patterns chapter-01.md --mode fast

      # Full accuracy analysis (5-20 minutes for large files)
      analyze-ai-patterns chapter-01.md --mode full

      # Custom sampling configuration
      analyze-ai-patterns chapter-01.md --mode sampling --samples 10 --sample-size 3000

      # Detailed analysis with line numbers and suggestions
      analyze-ai-patterns chapter-01.md --detailed

      # Dual score analysis with optimization path
      analyze-ai-patterns chapter-01.md --show-scores

      # Batch analyze directory
      analyze-ai-patterns --batch manuscript/sections --format tsv

    For detailed mode information: analyze-ai-patterns --help-modes
    """
    # Validate inputs
    if not file and not batch:
        raise click.UsageError('Either FILE or --batch DIR must be specified')

    # Handle history viewing commands (don't run analysis)
    if any([show_history_full, compare_history, show_dimension_trends,
            show_raw_metric_trends, export_history]):
        if not file:
            raise click.UsageError('History viewing commands require a FILE argument')
        sys.exit(handle_history_commands(file, show_history_full, compare_history,
                                        show_dimension_trends, show_raw_metric_trends,
                                        export_history))

    # Detailed mode limitations
    if detailed and batch:
        click.echo("Warning: --detailed mode not supported for batch analysis. Using standard mode.", err=True)
        detailed = False

    if detailed and format == 'tsv':
        click.echo("Warning: --detailed mode not compatible with TSV format. Using JSON format.", err=True)
        format = 'json'

    # Show scores validation
    if show_scores and batch:
        click.echo("Warning: --show-scores mode not supported for batch analysis. Using standard mode.", err=True)
        show_scores = False

    # Validate mode arguments
    if mode == 'fast' and (samples != 5 or sample_size != 2000):
        click.echo("Warning: --samples and --sample-size are ignored in 'fast' mode", err=True)

    # Warning: FULL mode with large files
    if mode == 'full' and file and os.path.exists(file):
        file_size = os.path.getsize(file)
        if file_size > 500000:  # >500k chars (~250 pages)
            pages = file_size / 2000
            click.echo(f"\n⚠ Warning: FULL mode with {pages:.0f}-page document may take 20+ minutes.", err=True)
            click.echo(f"           Consider using --mode adaptive for faster results (30-240s).\n", err=True)

            # Interactive confirmation (skip if in batch or dry-run)
            if not batch and not dry_run:
                try:
                    if not click.confirm("Continue with FULL mode?"):
                        click.echo("Canceled. Use --mode adaptive for faster analysis.", err=True)
                        sys.exit(0)
                except (EOFError, KeyboardInterrupt):
                    click.echo("\nCanceled.", err=True)
                    sys.exit(0)

    # Parse domain terms
    domain_patterns = parse_domain_terms(domain_terms) if domain_terms else None

    # Create config for analyzer (used by all modes)
    config = create_analysis_config(mode, samples, sample_size, sample_strategy, profile)

    # Initialize analyzer
    analyzer = AIPatternAnalyzer(domain_terms=domain_patterns, config=config)

    # Detailed analysis mode
    if detailed:
        try:
            detailed_result = analyzer.analyze_file_detailed(file)
            output_text = format_detailed_report(detailed_result, format)

            if output:
                output.write(output_text)
                click.echo(f"Detailed analysis written to {output.name}", err=True)
            else:
                click.echo(output_text)
            sys.exit(0)

        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

    # Standard analysis mode
    if batch:
        results, calculated_dual_score = run_batch_analysis(batch, mode, samples, sample_size, sample_strategy, profile, dry_run)
    else:
        results, calculated_dual_score = run_single_file_analysis(
            file, mode, samples, sample_size, sample_strategy, profile, dry_run, show_coverage,
            detection_target, quality_target, history_notes, no_track_history, no_score_summary, format
        )

    # Format and output
    output_lines = []

    if format == 'tsv' and len(results) > 1:
        # TSV batch output with header
        output_lines.append(format_report(results[0], 'tsv').split('\n')[0])  # Header
        for r in results:
            output_lines.append(format_report(r, 'tsv').split('\n')[1])  # Data row
    else:
        # Individual reports
        for r in results:
            dual_score_param = calculated_dual_score if (len(results) == 1 and not batch) else None

            output_lines.append(format_report(
                r,
                format,
                include_score_summary=not no_score_summary,
                detection_target=detection_target,
                quality_target=quality_target,
                dual_score=dual_score_param,
                mode=mode
            ))

    output_text = '\n'.join(output_lines)

    # Write output
    if output:
        output.write(output_text)
        click.echo(f"Analysis written to {output.name}", err=True)
    else:
        click.echo(output_text)


if __name__ == '__main__':
    main()

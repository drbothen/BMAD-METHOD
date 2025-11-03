"""
CLI output formatters.

Formats analysis results for display:
- Text reports (human-readable)
- JSON output (machine-readable)
- TSV output (for spreadsheet import)
- Detailed reports with line numbers and suggestions
- Dual score reports with optimization paths

Extracted from analyze_ai_patterns.py (lines 5886-6887)
"""

import json
import sys
from dataclasses import asdict
from typing import Optional

from ai_pattern_analyzer.core.results import (
    AnalysisResults,
    DetailedAnalysis,
)
from ai_pattern_analyzer.scoring.dual_score import DualScore
from ai_pattern_analyzer.history.tracker import ScoreHistory

# Required dependency
import textstat


def format_dual_score_report(dual_score: DualScore, history: Optional[ScoreHistory] = None,
                             output_format: str = 'text', as_detailed_section: bool = False) -> str:
    """
    Format dual score report with optimization path.

    Args:
        dual_score: DualScore object with scoring data
        history: Optional score history for trend analysis
        output_format: Output format ('text' or 'json')
        as_detailed_section: If True, formats as continuation of standard report (skips header)
    """

    if output_format == 'json':
        # Convert to dict for JSON serialization
        data = {
            'detection_risk': dual_score.detection_risk,
            'quality_score': dual_score.quality_score,
            'detection_interpretation': dual_score.detection_interpretation,
            'quality_interpretation': dual_score.quality_interpretation,
            'detection_target': dual_score.detection_target,
            'quality_target': dual_score.quality_target,
            'detection_gap': dual_score.detection_gap,
            'quality_gap': dual_score.quality_gap,
            'categories': [asdict(cat) for cat in dual_score.categories],
            'improvements': [asdict(imp) for imp in dual_score.improvements],
            'path_to_target': [asdict(action) for action in dual_score.path_to_target],
            'estimated_effort': dual_score.estimated_effort,
            'timestamp': dual_score.timestamp,
            'file_path': dual_score.file_path,
            'total_words': dual_score.total_words
        }

        if history and len(history.scores) > 0:
            data['history'] = {
                'trend': history.get_trend(),
                'score_count': len(history.scores),
                'first_score': asdict(history.scores[0]),
                'latest_score': asdict(history.scores[-1])
            }

        return json.dumps(data, indent=2)

    else:  # text format
        if as_detailed_section:
            # Format as continuation of standard report (no redundant header)
            report = f"""
{'─' * 80}
COMPLETE DUAL SCORE BREAKDOWN
{'─' * 80}

Quality Score:      {dual_score.quality_score:5.1f} / 100  {dual_score.quality_interpretation}
Detection Risk:     {dual_score.detection_risk:5.1f} / 100  {dual_score.detection_interpretation}
Targets:            Quality ≥{dual_score.quality_target:.0f}, Detection ≤{dual_score.detection_target:.0f}
Gap to Target:      {dual_score.quality_gap:+.1f} pts quality, {-dual_score.detection_gap:+.1f} pts detection
Effort Required:    {dual_score.estimated_effort}

"""
        else:
            # Standalone report (with full header)
            report = f"""
{'=' * 80}
DUAL SCORE ANALYSIS - OPTIMIZATION REPORT
{'=' * 80}

File: {dual_score.file_path}
Words: {dual_score.total_words}
Timestamp: {dual_score.timestamp}

{'─' * 80}
DUAL SCORES
{'─' * 80}

Quality Score:      {dual_score.quality_score:5.1f} / 100  {dual_score.quality_interpretation}
Detection Risk:     {dual_score.detection_risk:5.1f} / 100  {dual_score.detection_interpretation}

Targets:            Quality ≥{dual_score.quality_target:.0f}, Detection ≤{dual_score.detection_target:.0f}
Gap to Target:      Quality needs +{dual_score.quality_gap:.1f} pts, Detection needs -{dual_score.detection_gap:.1f} pts
Effort Required:    {dual_score.estimated_effort}

"""

        # Historical trend if available
        if history and len(history.scores) > 1:
            trend = history.get_trend()
            report += f"""{'─' * 80}
HISTORICAL TREND ({len(history.scores)} scores tracked)
{'─' * 80}

Quality:   {trend['quality']:10s} ({trend['quality_change']:+.1f} pts)
Detection: {trend['detection']:10s} ({trend['detection_change']:+.1f} pts)

"""

        # Category breakdown
        report += f"""{'─' * 80}
SCORE BREAKDOWN BY CATEGORY
{'─' * 80}

"""
        for cat in dual_score.categories:
            report += f"""{cat.name:25s}  {cat.total:5.1f} / {cat.max_total:4.1f}  ({cat.percentage:5.1f}%)
"""
            for dim in cat.dimensions:
                impact_symbol = '⚠' if dim.impact in ['HIGH', 'MEDIUM'] else ' '
                report += f"""  {impact_symbol} {dim.name:40s} {dim.score:5.1f} / {dim.max_score:4.1f}  (gap: {dim.gap:4.1f})
"""
            report += "\n"

        # Path to target
        if dual_score.path_to_target:
            report += f"""{'─' * 80}
PATH TO TARGET ({len(dual_score.path_to_target)} actions, sorted by ROI)
{'─' * 80}

"""
            cumulative = dual_score.quality_score
            for i, action in enumerate(dual_score.path_to_target, 1):
                cumulative += action.potential_gain
                report += f"""{i}. {action.dimension} (Effort: {action.effort_level})
   Current: {action.current_score:.1f}/{action.max_score:.1f} → Gain: +{action.potential_gain:.1f} pts → Cumulative: {cumulative:.1f}
   Action: {action.action}

"""

        # Top improvements (beyond path to target)
        other_improvements = [imp for imp in dual_score.improvements if imp not in dual_score.path_to_target]
        if other_improvements:
            report += f"""{'─' * 80}
ADDITIONAL IMPROVEMENTS (optional, for exceeding targets)
{'─' * 80}

"""
            for imp in other_improvements[:5]:  # Show top 5
                report += f"""• {imp.dimension} ({imp.effort_level} effort, +{imp.potential_gain:.1f} pts)
  {imp.action}

"""

        report += f"""{'=' * 80}
OPTIMIZATION SUMMARY
{'=' * 80}

To reach Quality Score ≥{dual_score.quality_target:.0f}:
  Complete {len(dual_score.path_to_target)} actions above
  Estimated effort: {dual_score.estimated_effort}
  Expected final score: ~{min(100, dual_score.quality_score + sum(a.potential_gain for a in dual_score.path_to_target)):.1f}

{'=' * 80}

"""
        return report


def format_detailed_report(analysis: DetailedAnalysis, output_format: str = 'text') -> str:
    """Format detailed analysis with line numbers and suggestions"""

    if output_format == 'json':
        # Convert dataclasses to dict for JSON serialization
        return json.dumps({
            'file_path': analysis.file_path,
            'summary': analysis.summary,
            # Original detailed findings
            'ai_vocabulary': [asdict(v) for v in analysis.ai_vocabulary],
            'heading_issues': [asdict(h) for h in analysis.heading_issues],
            'uniform_paragraphs': [asdict(p) for p in analysis.uniform_paragraphs],
            'em_dashes': [asdict(e) for e in analysis.em_dashes],
            'transitions': [asdict(t) for t in analysis.transitions],
            # ADVANCED: New detailed findings for LLM-driven fixes
            'burstiness_issues': [asdict(b) for b in analysis.burstiness_issues],
            'syntactic_issues': [asdict(s) for s in analysis.syntactic_issues],
            'stylometric_issues': [asdict(s) for s in analysis.stylometric_issues],
            'formatting_issues': [asdict(f) for f in analysis.formatting_issues],
            'high_predictability_segments': [asdict(h) for h in analysis.high_predictability_segments],
        }, indent=2)

    else:  # text format
        s = analysis.summary
        report = f"""
{'=' * 80}
AI PATTERN ANALYSIS - DETAILED DIAGNOSTIC REPORT
{'=' * 80}

File: {analysis.file_path}
Overall Assessment: {s['overall_assessment']}

{'─' * 80}
SUMMARY SCORES
{'─' * 80}

Perplexity:   {s['perplexity_score']:12s}  |  Burstiness:  {s['burstiness_score']:12s}
Structure:    {s['structure_score']:12s}  |  Voice:       {s['voice_score']:12s}
Technical:    {s['technical_score']:12s}  |  Formatting:  {s['formatting_score']:12s}

Words: {s['total_words']} | Sentences: {s['total_sentences']} | AI Vocab: {s['ai_vocab_per_1k']:.1f}/1k

{'=' * 80}
DETAILED FINDINGS WITH LINE NUMBERS
{'=' * 80}

"""

        # AI Vocabulary Instances
        if analysis.ai_vocabulary:
            report += f"""
{'─' * 80}
AI VOCABULARY INSTANCES ({len(analysis.ai_vocabulary)} shown)
{'─' * 80}

"""
            for i, vocab in enumerate(analysis.ai_vocabulary, 1):
                report += f"""{i}. Line {vocab.line_number}: "{vocab.word}"
   Context: {vocab.context}
   → Suggestions: {', '.join(vocab.suggestions)}

"""
        else:
            report += f"""
{'─' * 80}
AI VOCABULARY: None detected ✓
{'─' * 80}

"""

        # Heading Issues
        if analysis.heading_issues:
            # Group by issue type
            depth_issues = [h for h in analysis.heading_issues if h.issue_type == 'depth']
            parallel_issues = [h for h in analysis.heading_issues if h.issue_type == 'parallelism']
            verbose_issues = [h for h in analysis.heading_issues if h.issue_type == 'verbose']

            report += f"""
{'─' * 80}
HEADING STRUCTURE ISSUES ({len(analysis.heading_issues)} total)
{'─' * 80}

"""
            if depth_issues:
                report += f"""DEPTH VIOLATIONS (H4+ headings):
"""
                for h in depth_issues[:5]:
                    report += f"""  Line {h.line_number}: {'#' * h.level} {h.text}
    → {h.suggestion}

"""

            if parallel_issues:
                report += f"""
MECHANICAL PARALLELISM (identical structures):
"""
                # Show first 3 examples only
                shown = set()
                for h in parallel_issues:
                    if len(shown) >= 3:
                        break
                    key = f"{h.level}-{h.text.split()[0] if h.text.split() else ''}"
                    if key not in shown:
                        shown.add(key)
                        report += f"""  Line {h.line_number}: {'#' * h.level} {h.text}
    → {h.suggestion}

"""

            if verbose_issues:
                report += f"""
VERBOSE HEADINGS (>8 words):
"""
                for h in verbose_issues[:5]:
                    report += f"""  Line {h.line_number}: {h.text} ({len(h.text.split())} words)
    → {h.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
HEADING STRUCTURE: No major issues ✓
{'─' * 80}

"""

        # Uniform Paragraphs
        if analysis.uniform_paragraphs:
            report += f"""
{'─' * 80}
SENTENCE UNIFORMITY ISSUES ({len(analysis.uniform_paragraphs)} paragraphs)
{'─' * 80}

"""
            for para in analysis.uniform_paragraphs[:3]:  # Show top 3
                report += f"""Paragraph at Lines {para.start_line}-{para.end_line} ({para.sentence_count} sentences):
  Mean: {para.mean_length} words | StdDev: {para.stdev} (LOW VARIATION)
  Problem: {para.problem}

  Sample sentences:
"""
                for line_num, text, word_count in para.sentences:
                    report += f"""    "{text}..." ({word_count} words)
"""
                report += f"""
  → Suggestion: {para.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
SENTENCE VARIATION: Good variation detected ✓
{'─' * 80}

"""

        # Em-Dashes
        if analysis.em_dashes:
            report += f"""
{'─' * 80}
EM-DASH USAGE ({len(analysis.em_dashes)} total, {s['em_dashes_per_page']:.1f} per page)
{'─' * 80}
TARGET: ≤2 per page

"""
            # Group by page (estimate: 750 words per page)
            words_per_page = 750
            current_page = 1
            em_count_on_page = 0

            for em in analysis.em_dashes[:10]:  # Show first 10
                # Estimate page (rough approximation)
                estimated_page = ((em.line_number * 20) // words_per_page) + 1

                if estimated_page != current_page:
                    if em_count_on_page > 0:
                        report += f"""
"""
                    current_page = estimated_page
                    em_count_on_page = 0

                report += f"""  Line {em.line_number}: {em.context}
    → {em.suggestion}
"""
                em_count_on_page += 1

            if len(analysis.em_dashes) > 10:
                report += f"""
  ... and {len(analysis.em_dashes) - 10} more instances

"""
        else:
            report += f"""
{'─' * 80}
EM-DASH USAGE: Within target range ✓
{'─' * 80}

"""

        # Formulaic Transitions
        if analysis.transitions:
            report += f"""
{'─' * 80}
FORMULAIC TRANSITIONS ({len(analysis.transitions)} found)
{'─' * 80}

"""
            for i, trans in enumerate(analysis.transitions[:10], 1):
                report += f"""{i}. Line {trans.line_number}: "{trans.transition}"
   Context: {trans.context[:100]}...
   → Suggestions: {', '.join(trans.suggestions)}

"""
            if len(analysis.transitions) > 10:
                report += f"""... and {len(analysis.transitions) - 10} more instances

"""
        else:
            report += f"""
{'─' * 80}
TRANSITIONS: Natural transitions used ✓
{'─' * 80}

"""

        # ADVANCED: Burstiness Issues
        if analysis.burstiness_issues:
            report += f"""
{'─' * 80}
BURSTINESS ISSUES ({len(analysis.burstiness_issues)} sections with uniform sentence lengths)
{'─' * 80}

"""
            for issue in analysis.burstiness_issues[:5]:  # Show top 5
                report += f"""Lines {issue.start_line}-{issue.end_line} ({issue.sentence_count} sentences):
  Mean: {issue.mean_length} words | StdDev: {issue.stdev} (LOW VARIATION)
  Problem: {issue.problem}
  Sample sentences:
"""
                for line_num, text, word_count in issue.sentences_preview:
                    report += f"""    Line {line_num}: "{text}" ({word_count} words)
"""
                report += f"""  → Suggestion: {issue.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
BURSTINESS: Good sentence variation ✓
{'─' * 80}

"""

        # ADVANCED: Syntactic Issues
        if analysis.syntactic_issues:
            # Group by type
            passive_issues = [s for s in analysis.syntactic_issues if s.issue_type == 'passive']
            shallow_issues = [s for s in analysis.syntactic_issues if s.issue_type == 'shallow']
            subordination_issues = [s for s in analysis.syntactic_issues if s.issue_type == 'subordination']

            report += f"""
{'─' * 80}
SYNTACTIC COMPLEXITY ISSUES ({len(analysis.syntactic_issues)} total)
{'─' * 80}

"""
            if passive_issues:
                report += f"""PASSIVE VOICE ({len(passive_issues)} instances):
"""
                for syn in passive_issues[:3]:
                    report += f"""  Line {syn.line_number}: {syn.sentence}
    → {syn.suggestion}

"""

            if shallow_issues:
                report += f"""
SHALLOW SYNTAX ({len(shallow_issues)} instances):
"""
                for syn in shallow_issues[:3]:
                    report += f"""  Line {syn.line_number}: {syn.sentence}
    Problem: {syn.problem}
    → {syn.suggestion}

"""

            if subordination_issues:
                report += f"""
LOW SUBORDINATION ({len(subordination_issues)} instances):
"""
                for syn in subordination_issues[:3]:
                    report += f"""  Line {syn.line_number}: {syn.sentence}
    → {syn.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
SYNTACTIC COMPLEXITY: Good variation ✓
{'─' * 80}

"""

        # ADVANCED: Stylometric Issues
        if analysis.stylometric_issues:
            # Group by marker type
            however_issues = [s for s in analysis.stylometric_issues if s.marker_type == 'however']
            moreover_issues = [s for s in analysis.stylometric_issues if s.marker_type == 'moreover']
            cluster_issues = [s for s in analysis.stylometric_issues if s.marker_type == 'however_cluster']

            report += f"""
{'─' * 80}
STYLOMETRIC AI MARKERS ({len(analysis.stylometric_issues)} total)
{'─' * 80}

"""
            if however_issues:
                report += f""""HOWEVER" USAGE ({len(however_issues)} instances - AI marker):
"""
                for styl in however_issues[:5]:
                    report += f"""  Line {styl.line_number}: {styl.context}
    → {styl.suggestion}

"""

            if moreover_issues:
                report += f"""
"MOREOVER" USAGE ({len(moreover_issues)} instances - strong AI signature):
"""
                for styl in moreover_issues[:5]:
                    report += f"""  Line {styl.line_number}: {styl.context}
    → {styl.suggestion}

"""

            if cluster_issues:
                report += f"""
CLUSTERED MARKERS ({len(cluster_issues)} clusters - strong AI signature):
"""
                for styl in cluster_issues:
                    report += f"""  {styl.context}
    → {styl.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
STYLOMETRIC MARKERS: Natural writing patterns ✓
{'─' * 80}

"""

        # ADVANCED: Formatting Issues
        if analysis.formatting_issues:
            bold_issues = [f for f in analysis.formatting_issues if f.issue_type == 'bold_dense']
            italic_issues = [f for f in analysis.formatting_issues if f.issue_type == 'italic_dense']

            report += f"""
{'─' * 80}
FORMATTING PATTERN ISSUES ({len(analysis.formatting_issues)} total)
{'─' * 80}

"""
            if bold_issues:
                report += f"""EXCESSIVE BOLD ({len(bold_issues)} lines):
"""
                for fmt in bold_issues[:5]:
                    report += f"""  Line {fmt.line_number}: {fmt.context}
    Problem: {fmt.problem}
    → {fmt.suggestion}

"""

            if italic_issues:
                report += f"""
EXCESSIVE ITALIC ({len(italic_issues)} lines):
"""
                for fmt in italic_issues[:5]:
                    report += f"""  Line {fmt.line_number}: {fmt.context}
    Problem: {fmt.problem}
    → {fmt.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
FORMATTING PATTERNS: Natural variation ✓
{'─' * 80}

"""

        # ADVANCED: High Predictability Segments
        if analysis.high_predictability_segments:
            report += f"""
{'─' * 80}
HIGH PREDICTABILITY SEGMENTS ({len(analysis.high_predictability_segments)} AI-like sections found)
{'─' * 80}
These sections score high on GLTR analysis (>70% top-10 tokens = AI signature)

"""
            for seg in analysis.high_predictability_segments[:5]:
                report += f"""Lines {seg.start_line}-{seg.end_line} (GLTR={seg.gltr_score:.2f}):
  Preview: {seg.segment_preview}
  Problem: {seg.problem}
  → {seg.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
PREDICTABILITY: Natural word choice variation ✓
{'─' * 80}

"""

        report += f"""
{'=' * 80}
RECOMMENDED ACTIONS (Priority Order)
{'=' * 80}

"""

        # Generate priority recommendations
        actions = []

        if s['em_dashes_per_page'] > 3:
            actions.append(('CRITICAL', f"Reduce em-dashes from {s['em_dashes_per_page']:.1f} to ≤2 per page ({len(analysis.em_dashes)} instances to review)"))

        if s['ai_vocab_per_1k'] > 5:
            actions.append(('HIGH', f"Replace AI vocabulary: {s['ai_vocab_per_1k']:.1f} per 1k words ({len(analysis.ai_vocabulary)} instances shown above)"))

        if s['heading_depth'] >= 4:
            depth_count = len([h for h in analysis.heading_issues if h.issue_type == 'depth'])
            actions.append(('HIGH', f"Flatten heading hierarchy from H{s['heading_depth']} to H3 maximum ({depth_count} headings to restructure)"))

        if s['heading_parallelism'] >= 0.5:
            parallel_count = len([h for h in analysis.heading_issues if h.issue_type == 'parallelism'])
            actions.append(('HIGH', f"Break mechanical parallelism in headings (score: {s['heading_parallelism']:.2f}, {parallel_count} patterns detected)"))

        if s['sentence_stdev'] < 6:
            actions.append(('MEDIUM', f"Increase sentence variation (current StdDev: {s['sentence_stdev']}, target: ≥10) - {len(analysis.uniform_paragraphs)} paragraphs need work"))

        if len(analysis.transitions) > 5:
            actions.append(('MEDIUM', f"Replace formulaic transitions: {len(analysis.transitions)} instances found"))

        verbose_count = len([h for h in analysis.heading_issues if h.issue_type == 'verbose'])
        if verbose_count > 0:
            actions.append(('LOW', f"Shorten verbose headings: {verbose_count} headings >8 words"))

        if actions:
            for priority, action in actions:
                report += f"""[{priority:8s}] {action}
"""
        else:
            report += f"""✓ No major issues detected - content appears naturally written

"""

        report += f"""
{'=' * 80}
USAGE TIP: Use line numbers above to locate and fix issues systematically
{'=' * 80}

"""

        return report


def format_report(results: AnalysisResults,
                  output_format: str = 'text',
                  include_score_summary: bool = True,
                  detection_target: float = 30.0,
                  quality_target: float = 85.0,
                  dual_score = None,
                  dual_score_section: str = None) -> str:
    """
    Format analysis results for output.

    Args:
        results: Analysis results object
        output_format: Output format ('text', 'json', 'tsv')
        include_score_summary: Include quality score summary at end
        detection_target: Target detection risk score
        quality_target: Target quality score
        dual_score: Optional pre-calculated DualScore object (avoids recalculation)
        dual_score_section: Optional pre-formatted dual score section to insert at top
    """

    if output_format == 'json':
        return json.dumps(asdict(results), indent=2)

    elif output_format == 'tsv':
        # TSV header and row
        header = [
            'file', 'words', 'sentences', 'paragraphs',
            'ai_words', 'ai_per_1k', 'formulaic', 'sent_mean', 'sent_stdev',
            'sent_min', 'sent_max', 'short', 'medium', 'long',
            'lexical_diversity', 'headings', 'h_depth', 'h_parallel',
            'em_dashes_pg', 'perplexity', 'burstiness', 'structure',
            'voice', 'technical', 'formatting', 'overall'
        ]

        row = [
            results.file_path, results.total_words, results.total_sentences,
            results.total_paragraphs, results.ai_vocabulary_count,
            results.ai_vocabulary_per_1k, results.formulaic_transitions_count,
            results.sentence_mean_length, results.sentence_stdev,
            results.sentence_min, results.sentence_max,
            results.short_sentences_count, results.medium_sentences_count,
            results.long_sentences_count, results.lexical_diversity,
            results.total_headings, results.heading_depth,
            results.heading_parallelism_score, results.em_dashes_per_page,
            results.perplexity_score, results.burstiness_score,
            results.structure_score, results.voice_score,
            results.technical_score, results.formatting_score,
            results.overall_assessment
        ]

        return '\t'.join(header) + '\n' + '\t'.join(str(v) for v in row)

    else:  # text format
        r = results
        report = f"""
{'=' * 80}
AI PATTERN ANALYSIS REPORT
{'=' * 80}

File: {r.file_path}
Words: {r.total_words} | Sentences: {r.total_sentences} | Paragraphs: {r.total_paragraphs}
"""

        # Insert dual score section if provided (for --scores-detailed mode)
        if dual_score_section:
            report += dual_score_section

        report += f"""
{'─' * 80}
DIMENSION SCORES
{'─' * 80}

Perplexity (Vocabulary):    {r.perplexity_score:12s}  (AI words: {r.ai_vocabulary_count}, {r.ai_vocabulary_per_1k}/1k)
Burstiness (Sentence Var):  {r.burstiness_score:12s}  (μ={r.sentence_mean_length}, σ={r.sentence_stdev}, range={r.sentence_range})
Structure (Organization):   {r.structure_score:12s}  (Formulaic: {r.formulaic_transitions_count}, H-depth: {r.heading_depth})
Voice (Authenticity):       {r.voice_score:12s}  (1st-person: {r.first_person_count}, You: {r.direct_address_count})
Technical (Expertise):      {r.technical_score:12s}  (Domain terms: {r.domain_terms_count})
Formatting (Em-dashes):     {r.formatting_score:12s}  ({r.em_dashes_per_page:.1f} per page)"""

        # Add enhanced dimensions if available
        if r.syntactic_score and r.syntactic_score != "UNKNOWN":
            report += f"""
Syntactic (Naturalness):    {r.syntactic_score:12s}  (Repetition: {r.syntactic_repetition_score:.2f}, POS div: {r.pos_diversity:.2f})"""

        if r.sentiment_score and r.sentiment_score != "UNKNOWN":
            report += f"""
Sentiment (Variation):      {r.sentiment_score:12s}  (Variance: {r.sentiment_variance:.3f}, Mean: {r.sentiment_mean:.2f})"""

        # NEW: Enhanced structural dimensions (always present)
        report += f"""

{'─' * 80}
ENHANCED STRUCTURAL ANALYSIS
{'─' * 80}

Bold/Italic Patterns:       {r.bold_italic_score:12s}  (Bold: {r.bold_per_1k_words:.1f}/1k, Consistency: {r.formatting_consistency_score:.2f})
List Usage:                 {r.list_usage_score:12s}  (Items: {r.total_list_items}, Ratio O/U: {r.ordered_to_unordered_ratio:.2f})
Punctuation Clustering:     {r.punctuation_score:12s}  (Em-dash cascade: {r.em_dash_cascading_score:.2f}, Oxford: {r.oxford_comma_consistency:.2f})
Whitespace Patterns:        {r.whitespace_score:12s}  (Para uniformity: {r.paragraph_uniformity_score:.2f}, Variance: {r.paragraph_length_variance:.0f})"""

        if r.code_block_count > 0:
            report += f"""
Code Structure:             {r.code_structure_score:12s}  (Blocks: {r.code_block_count}, Lang consistency: {r.code_lang_consistency:.2f})"""

        if r.total_headings >= 3:
            report += f"""
Heading Hierarchy:          {r.heading_hierarchy_score:12s}  (Skips: {r.heading_hierarchy_skips}, Adherence: {r.heading_strict_adherence:.2f})"""

        # NEW: Phase 1 High-ROI Structural Patterns
        report += f"""

{'─' * 80}
STRUCTURAL PATTERNS
{'─' * 80}"""

        # Paragraph CV
        para_icon = "✓" if r.paragraph_cv >= 0.4 else ("⚠" if r.paragraph_cv >= 0.3 else "✗")
        report += f"""

Paragraph Length CV:     {r.paragraph_cv:.2f}  {para_icon} {r.paragraph_cv_assessment}
  Mean: {r.paragraph_cv_mean:.0f} words, StdDev: {r.paragraph_cv_stddev:.0f} words
  {r.paragraph_count} paragraphs analyzed"""

        if r.paragraph_cv < 0.35:
            report += """
  → ACTION: Vary paragraph lengths (mix 50-100, 150-250, 300-400 word paragraphs)"""

        # Section Variance
        sec_icon = "✓" if r.section_variance_pct >= 40 else ("⚠" if r.section_variance_pct >= 15 else "✗")
        report += f"""

Section Length Variance: {r.section_variance_pct:.1f}% {sec_icon} {r.section_variance_assessment}
  {r.section_count} sections analyzed"""

        if r.section_uniform_clusters > 0:
            report += f"""
  {r.section_uniform_clusters} uniform clusters detected (3+ similar-length sections)"""

        if r.section_variance_pct < 20:
            report += """
  → ACTION: Combine/split sections to create asymmetry (target: 40%+ variance)"""

        # List Nesting Depth
        list_icon = "✓" if r.list_max_depth <= 3 else ("⚠" if r.list_max_depth <= 4 else "✗")
        if r.list_max_depth > 0:
            report += f"""

List Nesting Depth:      Max {r.list_max_depth} levels {list_icon} {r.list_depth_assessment}
  {r.list_total_items} list items analyzed, Avg depth: {r.list_avg_depth:.1f}"""

            if r.list_max_depth > 4:
                report += """
  → ACTION: Flatten deep lists, break into separate sections"""
        else:
            report += f"""

List Nesting Depth:      No lists detected"""

        # H4 Subsection Analysis (if available)
        if r.h4_subsection_cv is not None and r.h4_assessment != 'INSUFFICIENT_DATA':
            h4_icon = "✓" if r.h4_subsection_cv >= 0.45 else ("⚠" if r.h4_subsection_cv >= 0.30 else "✗")
            report += f"""

H4 Subsection CV:        {r.h4_subsection_cv:.2f}  {h4_icon} {r.h4_assessment}
  {len(r.h4_counts) if r.h4_counts else 0} H3 sections analyzed
  H4 counts per H3: {r.h4_counts if r.h4_counts else []}"""

            if r.h4_uniform_count and r.h4_uniform_count > len(r.h4_counts or []) / 2:
                report += f"""
  ⚠ {r.h4_uniform_count} uniform sections (2-3 H4s each) - AI signature"""

        # Multi-level Combined Structure Score (if available)
        if r.combined_structure_score is not None:
            combined_icon = "✓" if r.combined_structure_prob_human >= 0.65 else ("⚠" if r.combined_structure_prob_human >= 0.40 else "✗")
            report += f"""

{'─' * 80}
MULTI-LEVEL STRUCTURE ANALYSIS
{'─' * 80}

Domain: {r.combined_structure_domain.upper() if r.combined_structure_domain else 'GENERAL'}
Combined Score: {r.combined_structure_score:.1f}/24  {combined_icon} {r.combined_structure_assessment}
Probability Human: {r.combined_structure_prob_human:.1%}

Breakdown by Level:
  H2 Section Length:   {r.combined_h2_score:.1f}/10  {r.combined_h2_assessment}
  H3 Subsection Count: {r.combined_h3_score:.1f}/8   {r.combined_h3_assessment}
  H4 Subsection Count: {r.combined_h4_score:.1f}/6   {r.combined_h4_assessment}"""

        # Overall structural patterns score
        report += f"""

Structural Patterns Score: {r.structural_patterns_score:12s}  (Combined quality: {r.paragraph_cv_score + r.section_variance_score + r.list_depth_score:.0f}/24 points)"""

        report += f"""

OVERALL ASSESSMENT: {r.overall_assessment}

{'─' * 80}
DETAILED METRICS
{'─' * 80}

SENTENCE VARIATION (Burstiness):
  Total: {r.total_sentences} | Mean: {r.sentence_mean_length} words | StdDev: {r.sentence_stdev}
  Range: {r.sentence_min}-{r.sentence_max} words
  Distribution: Short (≤10w): {r.short_sentences_count} | Medium (11-25w): {r.medium_sentences_count} | Long (≥30w): {r.long_sentences_count}

VOCABULARY & PERPLEXITY:
  AI Vocabulary: {r.ai_vocabulary_count} instances ({r.ai_vocabulary_per_1k:.2f} per 1k words)
  Examples: {', '.join(r.ai_vocabulary_list[:10]) if r.ai_vocabulary_list else 'None'}
  Formulaic Transitions: {r.formulaic_transitions_count}
  Examples: {', '.join(r.formulaic_transitions_list[:5]) if r.formulaic_transitions_list else 'None'}
  Lexical Diversity: {r.lexical_diversity:.3f} ({r.unique_words} unique words)

STRUCTURE & HEADINGS:
  Total Headings: {r.total_headings} ({r.headings_per_page:.1f} per page)
  Hierarchy: H1={r.h1_count}, H2={r.h2_count}, H3={r.h3_count}, H4+={r.h4_plus_count} | Max Depth: {r.heading_depth}
  Parallelism Score: {r.heading_parallelism_score:.2f} (0=varied, 1=mechanical)
  Verbose Headings (>8 words): {r.verbose_headings_count} | Avg Length: {r.avg_heading_length:.1f} words
  Lists: Bullets={r.bullet_list_lines}, Numbered={r.numbered_list_lines}

VOICE & AUTHENTICITY:
  First Person: {r.first_person_count} instances
  Direct Address (you/your): {r.direct_address_count} instances
  Contractions: {r.contraction_count}

FORMATTING PATTERNS:
  Em-dashes: {r.em_dash_count} ({r.em_dashes_per_page:.1f} per page)
  Bold (markdown): {r.bold_markdown_count}
  Italic (markdown): {r.italic_markdown_count}
"""

        # Enhanced metrics section
        enhanced_sections = []

        if r.mtld_score is not None or r.stemmed_diversity is not None:
            section = "\nENHANCED LEXICAL DIVERSITY (NLTK):"
            if r.mtld_score is not None:
                section += f"\n  MTLD Score: {r.mtld_score:.2f} (Moving Average TTR, higher = more diverse)"
            if r.stemmed_diversity is not None:
                section += f"\n  Stemmed Diversity: {r.stemmed_diversity:.3f} (Diversity after stemming)"
            enhanced_sections.append(section)

        if r.sentiment_variance is not None:
            section = f"""
SENTIMENT VARIATION (VADER):
  Variance: {r.sentiment_variance:.3f} (Higher = more emotional variation)
  Mean Sentiment: {r.sentiment_mean:.2f} (-1 negative, +1 positive)
  Flatness Score: {r.sentiment_flatness_score}"""
            enhanced_sections.append(section)

        if r.syntactic_repetition_score is not None:
            section = f"""
SYNTACTIC PATTERNS (spaCy):
  Structural Repetition: {r.syntactic_repetition_score:.3f} (Lower = more varied)
  POS Tag Diversity: {r.pos_diversity:.3f} (Part-of-speech variation)
  Avg Dependency Depth: {r.avg_dependency_depth:.2f} (Syntactic complexity)"""
            enhanced_sections.append(section)

        if r.automated_readability is not None or r.textacy_diversity is not None:
            section = "\nSTYLOMETRIC ANALYSIS (Textacy):"
            if r.automated_readability is not None:
                section += f"\n  Automated Readability Index: {r.automated_readability:.2f}"
            if r.textacy_diversity is not None:
                section += f"\n  Textacy Diversity: {r.textacy_diversity:.3f}"
            enhanced_sections.append(section)

        if r.gpt2_perplexity is not None:
            section = f"""
TRUE PERPLEXITY (GPT-2 Transformer):
  Perplexity Score: {r.gpt2_perplexity:.2f} (Lower = more predictable/AI-like)
  Interpretation: <50 = AI-like, 50-150 = Mixed, >150 = Human-like"""
            enhanced_sections.append(section)

        if enhanced_sections:
            report += f"""
{'─' * 80}
ENHANCED NLP ANALYSIS
{'─' * 80}
"""
            for section in enhanced_sections:
                report += section + "\n"

        if r.flesch_reading_ease is not None:
            report += f"""
READABILITY METRICS:
  Flesch Reading Ease: {r.flesch_reading_ease:.1f} (60-70 = Standard, higher = easier)
  Flesch-Kincaid Grade: {r.flesch_kincaid_grade:.1f} (U.S. grade level)
  Gunning Fog Index: {r.gunning_fog:.1f} (years of education needed)
  SMOG Index: {r.smog_index:.1f} (years of education needed)
"""

        # NEW: Enhanced structural analysis details
        report += f"""
{'─' * 80}
ENHANCED STRUCTURAL ANALYSIS DETAILS
{'─' * 80}

BOLD/ITALIC FORMATTING PATTERNS:
  Bold Density: {r.bold_per_1k_words:.1f} per 1k words (Human: 1-5, AI: 10-50)
  Italic Density: {r.italic_per_1k_words:.1f} per 1k words
  Formatting Consistency: {r.formatting_consistency_score:.3f} (Lower = more varied = human-like)
  Score: {r.bold_italic_score} ({'✓ Human-like' if r.bold_italic_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})

LIST USAGE PATTERNS:
  Total List Items: {r.total_list_items} (Ordered: {r.ordered_list_items}, Unordered: {r.unordered_list_items})
  List-to-Text Ratio: {r.list_to_text_ratio:.1%} (AI tends >25%)
  Ordered/Unordered Ratio: {r.ordered_to_unordered_ratio:.2f} (AI typical: 0.15-0.25)
  Item Length Variance: {r.list_item_length_variance:.1f} (Higher = more human-like)
  Score: {r.list_usage_score} ({'✓ Human-like' if r.list_usage_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})

PUNCTUATION CLUSTERING:
  Em-dash Cascading: {r.em_dash_cascading_score:.3f} (>0.7 = AI declining pattern)
  Oxford Comma Usage: {r.oxford_comma_count} (vs non-Oxford: {r.non_oxford_comma_count})
  Oxford Consistency: {r.oxford_comma_consistency:.3f} (1.0 = always Oxford = AI-like)
  Semicolons: {r.semicolon_count} ({r.semicolon_per_1k_words:.1f} per 1k words)
  Score: {r.punctuation_score} ({'✓ Human-like' if r.punctuation_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})

WHITESPACE & PARAGRAPH STRUCTURE:
  Paragraph Variance: {r.paragraph_length_variance:.0f} words² (Higher = more human-like)
  Paragraph Uniformity: {r.paragraph_uniformity_score:.3f} (Lower = more varied = human-like)
  Blank Lines: {r.blank_lines_count}
  Text Density: {r.text_density:.1f} chars/line
  Score: {r.whitespace_score} ({'✓ Human-like' if r.whitespace_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})"""

        if r.code_block_count > 0:
            report += f"""

CODE BLOCK PATTERNS:
  Total Blocks: {r.code_block_count}
  With Language Spec: {r.code_blocks_with_lang} ({r.code_lang_consistency:.0%})
  Language Consistency: {r.code_lang_consistency:.3f} (1.0 = always specified = AI-like)
  Avg Comment Density: {r.avg_code_comment_density:.3f}
  Score: {r.code_structure_score} ({'✓ Human-like' if r.code_structure_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like' if r.code_structure_score not in ['N/A'] else 'N/A'})"""

        if r.total_headings >= 3:
            report += f"""

HEADING HIERARCHY ANALYSIS:
  Hierarchy Skips: {r.heading_hierarchy_skips} (Humans occasionally skip; AI never does)
  Hierarchy Adherence: {r.heading_strict_adherence:.3f} (1.0 = perfect = AI-like)
  Heading Length Variance: {r.heading_length_variance:.1f} (Higher = more varied)
  Score: {r.heading_hierarchy_score} ({'✓ Human-like' if r.heading_hierarchy_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like' if r.heading_hierarchy_score not in ['N/A'] else 'N/A'})"""

        # Advanced lexical diversity & enhanced heading analysis
        advanced_sections = []

        # MATTR & RTTR
        if r.mattr is not None or r.rttr is not None:
            section = "\nADVANCED LEXICAL DIVERSITY (Textacy-based):"
            if r.mattr is not None:
                mattr_icon = "✓" if r.mattr >= 0.70 else "✗"
                section += f"\n  MATTR (window=100): {r.mattr:.3f}  {mattr_icon} {r.mattr_assessment}"
                if r.mattr < 0.70:
                    section += "\n    → ACTION: Increase vocabulary variety (target: MATTR ≥0.70)"
            if r.rttr is not None:
                rttr_icon = "✓" if r.rttr >= 7.5 else "✗"
                section += f"\n  RTTR: {r.rttr:.2f}  {rttr_icon} {r.rttr_assessment}"
                if r.rttr < 7.5:
                    section += "\n    → ACTION: Add more unique terminology (target: RTTR ≥7.5)"
            advanced_sections.append(section)

        # Heading Length Analysis
        if r.heading_length_short_pct is not None:
            heading_icon = "✓" if r.avg_heading_length <= 7 else "✗"
            section = f"""
ENHANCED HEADING LENGTH PATTERNS:
  Average Length: {r.avg_heading_length:.1f} words  {heading_icon} {r.heading_length_assessment}
  Distribution: Short (≤5w): {r.heading_length_short_pct:.1f}%, Medium (6-8w): {r.heading_length_medium_pct:.1f}%, Long (≥9w): {r.heading_length_long_pct:.1f}%"""
            if r.avg_heading_length > 7:
                section += "\n  → ACTION: Shorten headings (target: avg ≤7 words, 60%+ short)"
            advanced_sections.append(section)

        # Subsection Asymmetry
        if r.subsection_cv is not None and r.subsection_counts:
            subsec_icon = "✓" if r.subsection_cv >= 0.6 else ("⚠" if r.subsection_cv >= 0.4 else "✗")
            section = f"""
SUBSECTION ASYMMETRY:
  Coefficient of Variation: {r.subsection_cv:.3f}  {subsec_icon} {r.subsection_assessment}
  Subsection Counts: {r.subsection_counts}
  Uniform Sections (3-4 subs): {r.subsection_uniform_count}"""
            if r.subsection_cv < 0.4:
                section += "\n  → ACTION: Break uniformity, vary subsection counts (target: CV ≥0.6)"
            advanced_sections.append(section)

        # Heading Depth Variance
        if r.heading_depth_pattern is not None:
            depth_icon = "✓" if r.heading_depth_pattern == 'VARIED' else ("⚠" if r.heading_depth_pattern == 'SEQUENTIAL' else "✗")
            section = f"""
HEADING DEPTH TRANSITIONS:
  Pattern: {r.heading_depth_pattern}  {depth_icon} {r.heading_depth_assessment}
  Has Lateral Moves (H3→H3): {r.heading_has_lateral}
  Has Depth Jumps (H3→H1): {r.heading_has_jumps}"""
            if r.heading_transitions:
                trans_str = ", ".join([f"{k}({v})" for k, v in list(r.heading_transitions.items())[:5]])
                section += f"\n  Transitions: {trans_str}"
            if r.heading_depth_pattern == 'RIGID':
                section += "\n  → ACTION: Add lateral H3→H3 moves, occasional depth jumps"
            advanced_sections.append(section)

        if advanced_sections:
            report += f"""

{'─' * 80}
ADVANCED LEXICAL & HEADING ANALYSIS
{'─' * 80}
"""
            for section in advanced_sections:
                report += section + "\n"

        report += f"""

{'=' * 80}
RECOMMENDATIONS
{'=' * 80}

"""

        # Generate tiered recommendations
        critical = []
        important = []
        refinements = []
        strengths = []  # Quality recommendations - what's working well

        # ====================================================================
        # 🔴 CRITICAL ISSUES (Core Dimensions)
        # ====================================================================

        # Perplexity/Vocabulary
        if r.perplexity_score in ["LOW", "VERY LOW"]:
            vocab_rec = f"⚠ VOCABULARY: Replace {r.ai_vocabulary_count} AI-typical words with natural alternatives"
            if r.ai_vocabulary_list:
                examples = ', '.join(r.ai_vocabulary_list[:3])
                vocab_rec += f"\n   Examples: {examples}"
            critical.append(vocab_rec)

        # Burstiness/Sentence Variation
        if r.burstiness_score in ["LOW", "VERY LOW"]:
            burst_rec = f"⚠ SENTENCE VARIATION: Increase variation (current stdev: {r.sentence_stdev:.1f}, target: >8)"
            burst_rec += f"\n   - Add more short sentences (≤10 words): currently {r.short_sentences_count}/{r.total_sentences}"
            burst_rec += f"\n   - Add more long sentences (≥30 words): currently {r.long_sentences_count}/{r.total_sentences}"
            critical.append(burst_rec)

        # Structure (high-level)
        if r.structure_score in ["LOW", "VERY LOW"]:
            critical.append("⚠ STRUCTURE: Improve document organization and hierarchy")

        # Voice/Authenticity
        if r.voice_score in ["LOW", "VERY LOW"]:
            voice_rec = "⚠ VOICE: Add personal perspective markers and conversational elements"
            voice_rec += f"\n   Current: {r.first_person_count} first-person, {r.contraction_count} contractions"
            critical.append(voice_rec)

        # Technical depth
        if r.technical_score in ["LOW", "VERY LOW"]:
            critical.append("⚠ TECHNICAL DEPTH: Increase domain-specific terminology and expertise")

        # Formatting (high-level)
        if r.formatting_score in ["LOW", "VERY LOW"]:
            critical.append("⚠ FORMATTING: Address overall formatting patterns (see details below)")

        # Syntactic naturalness
        if r.syntactic_score in ["LOW", "VERY LOW"]:
            critical.append("⚠ SYNTAX: Vary syntactic structures and sentence complexity")

        # Formulaic transitions
        if r.formulaic_transitions_count > 3:
            trans_rec = f"⚠ TRANSITIONS: Remove {r.formulaic_transitions_count} formulaic transitions"
            if r.formulaic_transitions_list:
                examples = ', '.join(r.formulaic_transitions_list[:3])
                trans_rec += f"\n   Examples: {examples}"
            critical.append(trans_rec)

        # GLTR score (if available)
        if r.gltr_score in ["LOW", "VERY LOW"]:
            critical.append(f"⚠ PREDICTABILITY: High GLTR score detected - rephrase predictable segments")

        # Sentiment variation (if available)
        if r.sentiment_score in ["LOW", "VERY LOW"]:
            critical.append("⚠ SENTIMENT: Increase emotional variation across paragraphs")

        # ====================================================================
        # 🟡 IMPORTANT IMPROVEMENTS (Enhanced Structural Patterns)
        # ====================================================================

        # Bold/Italic patterns
        if r.bold_italic_score in ["LOW", "VERY LOW"]:
            important.append(f"• BOLD/ITALIC: Reduce bold density from {r.bold_per_1k_words:.1f} to 1-5 per 1k words")
        elif r.bold_italic_score == "MEDIUM" and r.formatting_consistency_score > 0.5:
            important.append(f"• FORMATTING CONSISTENCY: Vary bold/italic patterns (consistency: {r.formatting_consistency_score:.2f})")

        # List usage patterns
        if r.list_usage_score in ["LOW", "VERY LOW"]:
            if r.list_to_text_ratio > 0.25:
                important.append(f"• LIST USAGE: Reduce list-to-text ratio from {r.list_to_text_ratio*100:.1f}% to <15%")
            if 0.15 <= r.ordered_to_unordered_ratio <= 0.25:
                important.append(f"• LIST DISTRIBUTION: Vary ordered/unordered ratio (current: {r.ordered_to_unordered_ratio:.2f})")

        # Punctuation clustering
        if r.punctuation_score in ["LOW", "VERY LOW"]:
            if r.em_dash_cascading_score > 0.7:
                important.append(f"• EM-DASH PATTERN: Break declining cascade pattern (score: {r.em_dash_cascading_score:.2f})")
            if r.oxford_comma_consistency > 0.95:
                important.append(f"• OXFORD COMMA: Break consistency (currently {r.oxford_comma_consistency*100:.0f}% consistent = AI-like)")

        # Whitespace patterns
        if r.whitespace_score in ["LOW", "VERY LOW"]:
            important.append(f"• WHITESPACE: Break paragraph uniformity (score: {r.paragraph_uniformity_score:.2f})")
            important.append(f"  Vary blank line spacing and text density (current: {r.text_density:.1f} chars/line)")

        # Heading hierarchy adherence
        if r.heading_hierarchy_score in ["LOW", "VERY LOW"]:
            important.append(f"• HEADING HIERARCHY: Add occasional hierarchy skips (currently {r.heading_strict_adherence*100:.0f}% adherent = AI-like)")
            important.append("  Suggestion: Skip from H2→H4 occasionally, or add lateral H3→H3 moves")

        # Code structure (if applicable)
        if r.code_structure_score in ["LOW", "VERY LOW"]:
            if r.code_lang_consistency and r.code_lang_consistency > 0.9:
                important.append(f"• CODE BLOCKS: Vary language declaration patterns (currently {r.code_lang_consistency*100:.0f}% consistent)")

        # Heading depth
        if r.heading_depth >= 4:
            important.append(f"• HEADING DEPTH: Flatten hierarchy from {r.heading_depth} to 3 levels maximum")

        # Heading parallelism
        if r.heading_parallelism_score >= 0.5:
            important.append(f"• HEADING PARALLELISM: Break mechanical parallelism (score: {r.heading_parallelism_score:.2f})")

        # Verbose headings
        if r.verbose_headings_count > 0:
            important.append(f"• HEADING LENGTH: Shorten {r.verbose_headings_count} verbose headings to 3-7 words")

        # Em-dashes per page
        if r.em_dashes_per_page > 3:
            important.append(f"• EM-DASHES: Reduce from {r.em_dashes_per_page:.1f} to 1-2 per page")

        # Lexical diversity
        if r.lexical_diversity < 0.45:
            important.append(f"• LEXICAL DIVERSITY: Increase vocabulary richness (current: {r.lexical_diversity:.3f}, target: >0.50)")

        # MTLD score (if available)
        if r.mtld_score is not None and r.mtld_score < 160:
            important.append(f"• VOCABULARY VARIATION: Improve MTLD score (current: {r.mtld_score:.1f}, target: >160)")

        # Syntactic repetition (if available)
        if r.syntactic_repetition_score is not None and r.syntactic_repetition_score > 0.015:
            important.append(f"• STRUCTURAL REPETITION: Reduce syntactic patterns (score: {r.syntactic_repetition_score:.3f})")

        # Stylometric markers (if available)
        if r.stylometric_score in ["LOW", "VERY LOW"]:
            important.append("• STYLOMETRIC MARKERS: Reduce AI-typical discourse markers (however/moreover frequency)")

        # Advanced lexical (if available)
        if r.advanced_lexical_score in ["LOW", "VERY LOW"]:
            important.append("• ADVANCED LEXICAL: Improve vocabulary richness patterns (HDD/Yule's K)")

        # ====================================================================
        # 🔵 STRUCTURAL REFINEMENTS (Advanced Metrics)
        # ====================================================================

        # Paragraph CV
        if r.paragraph_cv_assessment in ["POOR", "FAIR"]:
            ref_rec = f"• Paragraph Variation: Increase length variance (CV: {r.paragraph_cv:.2f}, target: >0.60)"
            ref_rec += f"\n  Current mean: {r.paragraph_cv_mean:.0f} words - vary between 20-100 words"
            refinements.append(ref_rec)

        # Section variance
        if r.section_variance_assessment == "INSUFFICIENT_DATA":
            refinements.append(f"• Section Structure: Add more H2 sections to enable variance analysis (current: {r.section_count} sections)")
        elif r.section_variance_assessment in ["POOR", "FAIR"]:
            refinements.append(f"• Section Variance: Vary H2 section lengths (current: {r.section_variance_pct:.1f}%, target: >40%)")

        # List nesting depth
        if r.list_depth_assessment in ["POOR", "FAIR"]:
            refinements.append(f"• List Nesting: Adjust nesting depth (current max: {r.list_max_depth}, target: 2-3 levels)")

        # H4 subsection asymmetry
        if r.h4_assessment == "INSUFFICIENT_DATA":
            refinements.append(f"• H4 Structure: Add more H3 sections for H4 distribution analysis")
        elif r.h4_assessment in ["POOR", "FAIR"]:
            refinements.append(f"• H4 Distribution: Vary H4 counts under H3 sections (CV: {r.h4_subsection_cv:.2f}, target: >0.60)")

        # H3 subsection asymmetry
        if r.subsection_assessment == "INSUFFICIENT_DATA":
            refinements.append(f"• H3 Structure: Add more H2 sections for subsection analysis")
        elif r.subsection_assessment in ["POOR", "FAIR"]:
            ref_rec = f"• H3 Distribution: Vary H3 counts under H2 sections (CV: {r.subsection_cv:.2f}, target: >0.60)"
            if r.subsection_uniform_count and r.subsection_uniform_count > 0:
                ref_rec += f"\n  Avoid uniform pattern: {r.subsection_uniform_count} sections with 3-4 subsections"
            refinements.append(ref_rec)

        # Combined multi-level structure
        if r.combined_structure_assessment in ["POOR", "FAIR", "VERY_POOR"]:
            ref_rec = f"• Multi-Level Structure: Improve hierarchical variance (score: {r.combined_structure_score:.1f}/24, {r.combined_structure_prob_human*100:.1f}% human)"
            if r.combined_h2_assessment:
                ref_rec += f"\n  - H2 Section Length: {r.combined_h2_assessment}"
            if r.combined_h3_assessment:
                ref_rec += f"\n  - H3 Subsection Count: {r.combined_h3_assessment}"
            if r.combined_h4_assessment:
                ref_rec += f"\n  - H4 Subsection Count: {r.combined_h4_assessment}"
            refinements.append(ref_rec)

        # Heading length analysis
        if r.heading_length_assessment in ["POOR", "FAIR"]:
            refinements.append(f"• Heading Length Variance: Vary heading lengths (current variance: {r.heading_length_variance:.1f})")

        # Heading depth patterns
        if r.heading_depth_assessment in ["RIGID", "SEQUENTIAL"]:
            ref_rec = f"• Heading Navigation: Add lateral moves and depth jumps (current: {r.heading_depth_assessment})"
            if not r.heading_has_lateral:
                ref_rec += "\n  Add H3→H3 lateral transitions"
            if not r.heading_has_jumps:
                ref_rec += "\n  Add occasional H3→H1 or H4→H2 jumps"
            refinements.append(ref_rec)

        # Blockquote patterns (if available)
        if r.blockquote_assessment in ["POOR", "FAIR"]:
            if r.blockquote_section_start_clustering and r.blockquote_section_start_clustering > 0.5:
                refinements.append(f"• Blockquote Placement: Reduce section-start clustering ({r.blockquote_section_start_clustering*100:.0f}%, target: <30%)")

        # Link anchor quality (if available)
        if r.link_anchor_assessment in ["POOR", "FAIR"]:
            if r.link_generic_count and r.link_generic_count > 0:
                ref_rec = f"• Link Anchors: Replace {r.link_generic_count} generic anchors with descriptive text"
                if r.link_generic_examples:
                    examples = ', '.join(r.link_generic_examples[:3])
                    ref_rec += f"\n  Examples: {examples}"
                refinements.append(ref_rec)

        # Punctuation spacing (if available)
        if r.punctuation_spacing_assessment in ["POOR", "FAIR"]:
            refinements.append(f"• Punctuation Spacing: Vary punctuation patterns (colon CV: {r.punctuation_colon_cv:.2f})")

        # List AST patterns (if available)
        if r.list_ast_assessment in ["POOR", "FAIR"]:
            if r.list_symmetry_score and r.list_symmetry_score > 0.7:
                refinements.append(f"• List Symmetry: Break symmetric list patterns (score: {r.list_symmetry_score:.2f})")

        # Code AST patterns (if available)
        if r.code_ast_assessment in ["POOR", "FAIR"]:
            if r.code_lang_declaration_ratio is not None:
                refinements.append(f"• Code Language Tags: Adjust declaration ratio ({r.code_lang_declaration_ratio*100:.0f}%, target: >90%)")

        # Syntactic complexity (if available)
        if r.avg_dependency_depth is not None and r.avg_dependency_depth < 4:
            refinements.append(f"• Syntactic Complexity: Increase dependency depth (current: {r.avg_dependency_depth:.1f}, target: >4)")

        # Subordination (if available)
        if r.subordination_index is not None and r.subordination_index < 0.1:
            refinements.append(f"• Subordinate Clauses: Add more complex sentences (current: {r.subordination_index:.2f}, target: >0.15)")

        # ====================================================================
        # ✅ STRENGTHS (Quality Recommendations - What's Working Well)
        # ====================================================================

        # Core dimension strengths
        if r.perplexity_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ VOCABULARY: Natural word choice with minimal AI markers ({r.ai_vocabulary_per_1k:.1f} per 1k words)")

        if r.burstiness_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ SENTENCE VARIATION: Excellent variety (stdev: {r.sentence_stdev:.1f}, range: {r.sentence_min}-{r.sentence_max} words)")

        if r.structure_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ STRUCTURE: Well-organized document hierarchy ({r.total_headings} headings across {r.heading_depth} levels)")

        if r.voice_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ VOICE: Strong authentic voice ({r.first_person_count} first-person, {r.contraction_count} contractions)")

        if r.technical_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ TECHNICAL DEPTH: Appropriate domain expertise ({r.domain_terms_count} domain terms)")

        if r.formatting_score in ["HIGH", "VERY HIGH"]:
            strengths.append("✓ FORMATTING: Natural formatting patterns throughout")

        if r.syntactic_score in ["HIGH", "VERY HIGH"]:
            strengths.append("✓ SYNTAX: Varied and natural sentence structures")

        # Enhanced structural strengths
        if r.bold_italic_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ BOLD/ITALIC: Well-balanced formatting ({r.bold_per_1k_words:.1f} bold, {r.italic_per_1k_words:.1f} italic per 1k)")

        if r.list_usage_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ LIST USAGE: Appropriate list patterns ({r.total_list_items} items, {r.list_to_text_ratio*100:.1f}% of content)")

        if r.punctuation_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ PUNCTUATION: Natural punctuation variety")

        if r.whitespace_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ WHITESPACE: Good paragraph variation (uniformity: {r.paragraph_uniformity_score:.2f})")

        if r.heading_hierarchy_score in ["HIGH", "VERY HIGH"]:
            strengths.append(f"✓ HEADING HIERARCHY: Natural hierarchy with {r.heading_hierarchy_skips} skips")

        if r.lexical_diversity >= 0.50:
            strengths.append(f"✓ LEXICAL DIVERSITY: Strong vocabulary richness ({r.lexical_diversity:.3f}, unique words: {r.unique_words})")

        # Structural pattern strengths
        if r.paragraph_cv_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ PARAGRAPH VARIATION: Excellent length variety (CV: {r.paragraph_cv:.2f})")

        if r.section_variance_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ SECTION VARIANCE: Good asymmetry in section lengths ({r.section_variance_pct:.1f}% variance)")

        if r.list_depth_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ LIST NESTING: Appropriate depth (max: {r.list_max_depth}, avg: {r.list_avg_depth:.1f})")

        if r.h4_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ H4 DISTRIBUTION: Strong subsection variety (CV: {r.h4_subsection_cv:.2f})")

        if r.subsection_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ H3 DISTRIBUTION: Good subsection asymmetry (CV: {r.subsection_cv:.2f})")

        if r.combined_structure_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ MULTI-LEVEL STRUCTURE: Strong hierarchical variance (score: {r.combined_structure_score:.1f}/24, {r.combined_structure_prob_human*100:.1f}% human)")

        if r.heading_length_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ HEADING LENGTHS: Good variation in heading lengths")

        if r.heading_depth_assessment == "VARIED":
            strengths.append("✓ HEADING NAVIGATION: Natural varied navigation patterns")

        # Advanced NLP strengths
        if r.mtld_score is not None and r.mtld_score >= 160:
            strengths.append(f"✓ MTLD DIVERSITY: Excellent vocabulary variation ({r.mtld_score:.1f})")

        if r.syntactic_repetition_score is not None and r.syntactic_repetition_score <= 0.010:
            strengths.append(f"✓ SYNTACTIC VARIETY: Minimal structural repetition ({r.syntactic_repetition_score:.3f})")

        if r.avg_dependency_depth is not None and r.avg_dependency_depth >= 4:
            strengths.append(f"✓ SYNTACTIC COMPLEXITY: Appropriate complexity (depth: {r.avg_dependency_depth:.1f})")

        if r.subordination_index is not None and r.subordination_index >= 0.15:
            strengths.append(f"✓ SUBORDINATION: Good use of complex sentences ({r.subordination_index:.2f})")

        # Phase 3 AST strengths
        if r.blockquote_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ BLOCKQUOTE PLACEMENT: Natural blockquote distribution")

        if r.link_anchor_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ LINK ANCHORS: Descriptive anchor text ({r.link_total} links)")

        if r.list_ast_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ LIST PATTERNS: Natural list structure variety")

        if r.code_ast_assessment in ["EXCELLENT", "GOOD"]:
            strengths.append(f"✓ CODE BLOCKS: Good language declaration practices")

        # ====================================================================
        # OUTPUT TIERED RECOMMENDATIONS
        # ====================================================================

        has_any_recommendations = critical or important or refinements
        has_any_content = has_any_recommendations or strengths

        if not has_any_content:
            report += "✓ No analysis results available.\n"
        elif not has_any_recommendations and strengths:
            report += f"""
✅ EXCELLENT CONTENT - No Issues Detected
{'─' * 80}
Content appears naturally human-written across all dimensions.

"""
            # Show strengths
            report += f"""
✅ STRENGTHS (What's Working Well):
{'─' * 80}
"""
            for strength in strengths:
                report += f"{strength}\n"
        else:
            # Critical tier
            if critical:
                report += f"""
🔴 CRITICAL ISSUES (Fix First):
{'─' * 80}
"""
                for rec in critical:
                    report += f"{rec}\n"
            else:
                report += f"""
🔴 CRITICAL ISSUES (Fix First):
{'─' * 80}
✓ No critical issues detected

"""

            # Important tier
            if important:
                report += f"""
🟡 IMPORTANT IMPROVEMENTS:
{'─' * 80}
"""
                for rec in important:
                    report += f"{rec}\n"
            else:
                report += f"""
🟡 IMPORTANT IMPROVEMENTS:
{'─' * 80}
✓ No important improvements needed

"""

            # Refinements tier
            if refinements:
                report += f"""
🔵 STRUCTURAL REFINEMENTS (Advanced):
{'─' * 80}
"""
                for rec in refinements:
                    report += f"{rec}\n"
            else:
                report += f"""
🔵 STRUCTURAL REFINEMENTS (Advanced):
{'─' * 80}
✓ No structural refinements needed

"""

            # Strengths tier (quality recommendations)
            if strengths:
                report += f"""
✅ STRENGTHS (What's Working Well):
{'─' * 80}
"""
                for strength in strengths:
                    report += f"{strength}\n"

        report += f"\n{'=' * 80}\n"

        # Add quality score summary at the end (if enabled)
        if include_score_summary and output_format == 'text':
            report += format_score_summary(results, detection_target, quality_target, dual_score)

        return report


def format_score_summary(r: AnalysisResults,
                         detection_target: float = 30.0,
                         quality_target: float = 85.0,
                         dual_score = None) -> str:
    """
    Generate brief quality score summary for standard report.

    Args:
        r: Analysis results
        detection_target: Target detection risk score
        quality_target: Target quality score
        dual_score: Optional pre-calculated DualScore object (avoids recalculation)
    """
    from ai_pattern_analyzer.scoring.dual_score_calculator import calculate_dual_score

    # Use pre-calculated dual_score if provided, otherwise calculate it
    if dual_score is None:
        dual_score = calculate_dual_score(r, detection_target, quality_target)

    # Format top 3 actions
    top_actions = ""
    for i, action in enumerate(dual_score.path_to_target[:3], 1):
        top_actions += f"  {i}. {action.dimension} → {action.potential_gain:+.1f} pts\n"

    if not top_actions:
        top_actions = "  ✓ Target already achieved!\n"

    return f"""
{'─' * 80}
QUALITY SCORE SUMMARY
{'─' * 80}

Quality Score:      {dual_score.quality_score:5.1f} / 100  (Target: ≥{quality_target})   Gap: {dual_score.quality_gap:+.1f} pts
Detection Risk:     {dual_score.detection_risk:5.1f} / 100  (Target: ≤{detection_target})  Gap: {-dual_score.detection_gap:+.1f} pts

Assessment:         {dual_score.quality_interpretation}
Effort Required:    {dual_score.estimated_effort}

Top Actions to Reach Target (sorted by ROI):
{top_actions}
Use --scores-detailed for complete breakdown and optimization path.

{'=' * 80}
"""

"""
Burstiness dimension analyzer.

Analyzes sentence and paragraph length variation - a core metric from GPTZero methodology.
Low variation (low burstiness) is a strong AI signal, while high variation is human-like.
"""

import re
import statistics
from typing import Dict, List, Any
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.core.results import SentenceBurstinessIssue
from ai_pattern_analyzer.utils.text_processing import safe_ratio
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS


class BurstinessAnalyzer(DimensionAnalyzer):
    """Analyzes burstiness dimension - sentence and paragraph variation."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for sentence and paragraph variation.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with burstiness analysis results
        """
        sentence_burst = self._analyze_sentence_burstiness(text)
        paragraph_var = self._analyze_paragraph_variation(text)
        paragraph_cv = self._calculate_paragraph_cv(text)

        return {
            'sentence_burstiness': sentence_burst,
            'paragraph_variation': paragraph_var,
            'paragraph_cv': paragraph_cv,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> List[SentenceBurstinessIssue]:
        """
        Detailed analysis of burstiness issues with line numbers.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            List of SentenceBurstinessIssue objects
        """
        return self._analyze_burstiness_issues_detailed(lines, html_comment_checker)

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate burstiness score.

        Args:
            analysis_results: Results dict with sentence burstiness metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        total_sentences = analysis_results.get('total_sentences', 0)
        if total_sentences == 0:
            return (0.0, "UNKNOWN")

        stdev = analysis_results.get('stdev', 0)
        short_count = analysis_results.get('short', 0)
        long_count = analysis_results.get('long', 0)

        short_pct = safe_ratio(short_count, total_sentences)
        long_pct = safe_ratio(long_count, total_sentences)

        # High burstiness: high stdev, good mix of short/long
        if stdev >= 8 and short_pct >= THRESHOLDS.SHORT_SENTENCE_MIN_RATIO and long_pct >= THRESHOLDS.LONG_SENTENCE_MIN_RATIO:
            return (10.0, "HIGH")
        elif stdev >= 5:
            return (7.0, "MEDIUM")
        elif stdev >= THRESHOLDS.SENTENCE_STDEV_LOW:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")

    def _analyze_sentence_burstiness(self, text: str) -> Dict:
        """Analyze sentence length variation."""
        # Remove headings and list markers for sentence analysis
        lines = []
        for line in text.splitlines():
            if line.strip().startswith('#'):
                continue
            # Remove list markers
            line = re.sub(r'^\s*[-*+0-9]+[\.)]\s*', '', line)
            lines.append(line)

        clean_text = '\n'.join(lines)

        # Split into paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', clean_text) if p.strip()]

        # Split paragraphs into sentences
        sent_pattern = re.compile(r'(?<=[.!?])\s+')
        all_lengths = []

        for para in paragraphs:
            # Skip code blocks
            if '```' in para:
                continue
            sentences = [s.strip() for s in sent_pattern.split(para) if s.strip()]
            for sent in sentences:
                word_count = len(re.findall(r"[\w'-]+", sent))
                if word_count > 0:  # Only count non-empty sentences
                    all_lengths.append(word_count)

        if not all_lengths:
            return {
                'total_sentences': 0,
                'mean': 0,
                'stdev': 0,
                'min': 0,
                'max': 0,
                'short': 0,
                'medium': 0,
                'long': 0,
                'lengths': []
            }

        short = sum(1 for x in all_lengths if x <= 10)
        medium = sum(1 for x in all_lengths if 11 <= x <= 25)
        long = sum(1 for x in all_lengths if x >= 30)

        return {
            'total_sentences': len(all_lengths),
            'mean': round(statistics.mean(all_lengths), 1),
            'stdev': round(statistics.stdev(all_lengths), 1) if len(all_lengths) > 1 else 0,
            'min': min(all_lengths),
            'max': max(all_lengths),
            'short': short,
            'medium': medium,
            'long': long,
            'lengths': all_lengths
        }

    def _analyze_paragraph_variation(self, text: str) -> Dict:
        """Analyze paragraph length variation."""
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        # Filter out headings and code blocks
        para_words = []
        for para in paragraphs:
            if para.startswith('#') or '```' in para:
                continue
            words = re.findall(r"\b[\w'-]+\b", para)
            if words:
                para_words.append(len(words))

        if not para_words:
            return {
                'total_paragraphs': 0,
                'mean': 0,
                'stdev': 0,
                'min': 0,
                'max': 0
            }

        return {
            'total_paragraphs': len(para_words),
            'mean': round(statistics.mean(para_words), 1),
            'stdev': round(statistics.stdev(para_words), 1) if len(para_words) > 1 else 0,
            'min': min(para_words),
            'max': max(para_words)
        }

    def _calculate_paragraph_cv(self, text: str) -> Dict[str, float]:
        """
        Calculate coefficient of variation for paragraph lengths.

        Phase 1 High-ROI pattern: Detects unnaturally uniform paragraph lengths,
        a strong AI signature. Human writing typically shows CV ≥0.4, while
        AI-generated content often has CV <0.3.

        Returns:
            Dict with mean_length, stddev, cv, score, assessment, paragraph_count
        """
        # Split by double newlines to get paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # Filter out headings, code blocks, and very short lines
        filtered_paragraphs = []
        for p in paragraphs:
            # Skip headings (start with #)
            if p.startswith('#'):
                continue
            # Skip code blocks
            if '```' in p:
                continue
            # Skip very short lines (likely not real paragraphs)
            if len(p.split()) < 10:
                continue
            filtered_paragraphs.append(p)

        # Count words per paragraph
        lengths = [len(p.split()) for p in filtered_paragraphs]

        if len(lengths) < 3:
            return {
                'mean_length': 0.0,
                'stddev': 0.0,
                'cv': 0.0,
                'score': 10.0,  # Benefit of doubt for insufficient data
                'assessment': 'INSUFFICIENT_DATA',
                'paragraph_count': len(lengths)
            }

        mean_length = statistics.mean(lengths)
        stddev = statistics.stdev(lengths)
        cv = stddev / mean_length if mean_length > 0 else 0.0

        # Scoring based on research thresholds
        if cv >= 0.6:
            score, assessment = 10.0, 'EXCELLENT'
        elif cv >= 0.4:
            score, assessment = 7.0, 'GOOD'
        elif cv >= 0.3:
            score, assessment = 4.0, 'FAIR'
        else:
            score, assessment = 0.0, 'POOR'

        return {
            'mean_length': round(mean_length, 1),
            'stddev': round(stddev, 1),
            'cv': round(cv, 2),
            'score': score,
            'assessment': assessment,
            'paragraph_count': len(lengths)
        }

    def _analyze_burstiness_issues_detailed(self, lines: List[str], html_comment_checker=None) -> List[SentenceBurstinessIssue]:
        """Detect sections with uniform sentence lengths (low burstiness)."""
        issues = []

        # Split into paragraphs
        current_para = []
        para_start_line = 1

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Skip HTML comments, headings, and code blocks
            if html_comment_checker and html_comment_checker(line):
                continue
            if stripped.startswith('#') or stripped.startswith('```'):
                continue

            if stripped:
                current_para.append((line_num, line))
            else:
                # End of paragraph - analyze it
                if len(current_para) >= 3:
                    para_text = ' '.join([l[1] for l in current_para])
                    sent_pattern = re.compile(r'(?<=[.!?])\s+')
                    sentences = [s.strip() for s in sent_pattern.split(para_text) if s.strip()]

                    if len(sentences) >= 3:
                        lengths = [len(re.findall(r"[\w'-]+", s)) for s in sentences]
                        if len(lengths) > 1:
                            mean = statistics.mean(lengths)
                            stdev = statistics.stdev(lengths)

                            # Low burstiness: stdev < 5 words (AI signature)
                            if stdev < 5:
                                # Get preview of sentences with their lengths
                                preview = []
                                for i, sent in enumerate(sentences[:3]):
                                    preview.append((
                                        current_para[0][0] + i,  # Line number
                                        sent[:60] + '...' if len(sent) > 60 else sent,
                                        lengths[i]
                                    ))

                                issues.append(SentenceBurstinessIssue(
                                    start_line=current_para[0][0],
                                    end_line=current_para[-1][0],
                                    sentence_count=len(sentences),
                                    mean_length=round(mean, 1),
                                    stdev=round(stdev, 1),
                                    problem=f'Uniform sentence lengths ({int(min(lengths))}-{int(max(lengths))} words, σ={stdev:.1f})',
                                    sentences_preview=preview,
                                    suggestion='Add variety: combine short sentences (5-10 words), keep medium (15-25), add complex (30-45 words)'
                                ))

                current_para = []
                para_start_line = line_num + 1

        return issues

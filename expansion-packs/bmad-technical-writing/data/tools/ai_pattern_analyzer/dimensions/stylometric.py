"""
Stylometric dimension analyzer.

Analyzes stylometric patterns:
- Readability metrics (Flesch-Kincaid, etc.)
- Average word length
- Average sentence length
- Syllable patterns
- POS tag distribution

Requires dependencies: textstat, nltk
"""

import re
from typing import Dict, List, Any, Optional
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.core.results import StylometricIssue
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS

# Required imports
import textstat
import nltk


class StylometricAnalyzer(DimensionAnalyzer):
    """Analyzes stylometric dimension - readability and style metrics."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for stylometric patterns.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with stylometric analysis results
        """
        # TODO: Extract from analyze_ai_patterns.py lines ~2700-2900
        stylometric = self._analyze_stylometric_patterns(text)

        return {
            'stylometric': stylometric,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> List[StylometricIssue]:
        """
        Detailed analysis with line numbers and suggestions.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            List of StylometricIssue objects
        """
        # TODO: Extract from analyze_ai_patterns.py lines 1537-1598
        return self._analyze_stylometric_issues_detailed(lines, html_comment_checker)

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate stylometric score.

        Args:
            analysis_results: Results dict with stylometric metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        # TODO: Extract scoring logic from _score_stylometric (lines ~4680-4710)
        # Placeholder scoring
        return (7.0, "MEDIUM")

    def _analyze_stylometric_patterns(self, text: str) -> Dict:
        """Analyze stylometric patterns using textstat."""
        result = {
            'avg_word_length': 0.0,
            'avg_sentence_length': 0.0,
        }

        try:
            result['flesch_reading_ease'] = textstat.flesch_reading_ease(text)
            result['flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(text)
            result['automated_readability_index'] = textstat.automated_readability_index(text)
        except Exception:
            pass

        return result

    def _analyze_stylometric_issues_detailed(self, lines: List[str], html_comment_checker=None) -> List[StylometricIssue]:
        """Detect AI-specific stylometric markers (however, moreover, repetitive vocabulary)."""
        issues = []

        # Track "however" and "moreover" usage
        however_pattern = re.compile(r'\bhowever\b', re.IGNORECASE)
        moreover_pattern = re.compile(r'\bmoreover\b', re.IGNORECASE)

        # Count total words for frequency calculation
        total_words = sum(len(re.findall(r'\b\w+\b', line)) for line in lines)
        words_in_thousands = total_words / 1000 if total_words > 0 else 1

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Skip HTML comments (metadata), headings, and code blocks
            if html_comment_checker and html_comment_checker(line):
                continue
            if stripped.startswith('#') or stripped.startswith('```'):
                continue

            # Check for "however" (AI: 5-10 per 1k, Human: 1-3 per 1k)
            however_matches = list(however_pattern.finditer(line))
            for match in however_matches:
                context = line.strip()
                issues.append(StylometricIssue(
                    line_number=line_num,
                    marker_type='however',
                    context=context[:120] + '...' if len(context) > 120 else context,
                    frequency=len(however_matches) / words_in_thousands if words_in_thousands > 0 else 0,
                    problem='"However" is AI transition marker (human writers use sparingly)',
                    suggestion='Replace with: "But", "Yet", "Still", or natural flow without transition'
                ))

            # Check for "moreover" (AI: 3-7 per 1k, Human: 0-1 per 1k)
            moreover_matches = list(moreover_pattern.finditer(line))
            for match in moreover_matches:
                context = line.strip()
                issues.append(StylometricIssue(
                    line_number=line_num,
                    marker_type='moreover',
                    context=context[:120] + '...' if len(context) > 120 else context,
                    frequency=len(moreover_matches) / words_in_thousands if words_in_thousands > 0 else 0,
                    problem='"Moreover" is strong AI signature (very rare in human writing)',
                    suggestion='Replace with: "Also", "And", "Plus", or remove transition entirely'
                ))

        # Check for clusters (multiple "however" in close proximity)
        however_lines = [i for i, line in enumerate(lines, start=1)
                        if however_pattern.search(line)]
        for i in range(len(however_lines) - 1):
            if however_lines[i+1] - however_lines[i] <= 3:  # Within 3 lines
                issues.append(StylometricIssue(
                    line_number=however_lines[i],
                    marker_type='however_cluster',
                    context=f'Lines {however_lines[i]}-{however_lines[i+1]}',
                    frequency=2 / words_in_thousands if words_in_thousands > 0 else 0,
                    problem='Clustered "however" usage (strong AI signature)',
                    suggestion='Vary transitions or remove some instances entirely'
                ))

        return issues

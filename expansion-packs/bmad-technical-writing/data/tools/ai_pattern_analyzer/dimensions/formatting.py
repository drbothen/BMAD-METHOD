"""
Formatting dimension analyzer.

Analyzes formatting patterns including:
- Em-dash usage (frequency and clustering) - STRONGEST AI signal (95% accuracy)
- Bold and italic overuse (ChatGPT uses 10x more than humans)
- Quotation patterns
- Formatting consistency (mechanical distribution)

Research: Em-dash overuse is the single strongest AI detection signal.
ChatGPT uses 10x more em-dashes and bold formatting than human writers.
"""

import re
import statistics
from typing import Dict, List, Any
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.core.results import EmDashInstance, FormattingIssue
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS
from ai_pattern_analyzer.utils.text_processing import count_words


class FormattingAnalyzer(DimensionAnalyzer):
    """Analyzes formatting dimension - em-dash, bold/italic, quotations."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for formatting patterns.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with formatting analysis results
        """
        formatting = self._analyze_formatting(text)
        bold_italic = self._analyze_bold_italic_patterns(text)

        return {
            'formatting': formatting,
            'bold_italic': bold_italic,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> Dict[str, Any]:
        """
        Detailed analysis with line numbers and suggestions.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            Dict with detailed analysis including instances
        """
        em_dash_instances = self._analyze_em_dashes_detailed(lines, html_comment_checker)
        formatting_issues = self._analyze_formatting_issues_detailed(lines, html_comment_checker)

        return {
            'em_dash_instances': em_dash_instances,
            'formatting_issues': formatting_issues,
        }

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate formatting score.

        Combines em-dash usage and bold/italic density scoring.
        Em-dash overuse is the STRONGEST single AI detection signal (95% accuracy).

        Args:
            analysis_results: Results dict with formatting metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        issues = 0

        # Primary signal: em-dashes per page
        em_per_page = analysis_results.get('em_dashes_per_page', 0)
        if em_per_page > 10:
            issues += 3  # Very strong AI signal
        elif em_per_page > 5:
            issues += 2
        elif em_per_page > THRESHOLDS.EM_DASH_MAX_PER_PAGE:
            issues += 1

        # Bold density (ChatGPT uses 10x more bold)
        bold_per_1k = analysis_results.get('bold_per_1k', 0)
        if bold_per_1k > THRESHOLDS.BOLD_EXTREME_AI_PER_1K:
            issues += 3  # Extreme AI marker
        elif bold_per_1k > THRESHOLDS.BOLD_AI_MIN_PER_1K:
            issues += 2
        elif bold_per_1k > THRESHOLDS.BOLD_HUMAN_MAX_PER_1K:
            issues += 1

        # Formatting consistency (mechanical distribution)
        consistency = analysis_results.get('formatting_consistency', 0)
        if consistency > THRESHOLDS.FORMATTING_CONSISTENCY_AI_THRESHOLD:
            issues += 2
        elif consistency > THRESHOLDS.FORMATTING_CONSISTENCY_MEDIUM:
            issues += 1

        # Score based on total issues
        if issues == 0:
            return (10.0, "HIGH")
        elif issues <= 2:
            return (7.0, "MEDIUM")
        elif issues <= 4:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")

    def _analyze_formatting(self, text: str) -> Dict:
        """Analyze formatting patterns."""
        # Em-dashes (— or --)
        em_dashes = len(re.findall(r'—|--', text))

        # Bold (markdown **text** or __text__)
        bold = len(re.findall(r'\*\*[^*]+\*\*|__[^_]+__', text))

        # Italic (markdown *text* or _text_)
        italic = len(re.findall(r'\*[^*]+\*|_[^_]+_', text))

        return {
            'em_dashes': em_dashes,
            'bold': bold,
            'italics': italic
        }

    def _analyze_bold_italic_patterns(self, text: str) -> Dict:
        """
        Analyze bold/italic formatting distribution patterns.

        AI models (especially ChatGPT) use 10x more bold than humans.
        Research: Humans ~1-5 bold per 1k words, AI ~10-50 per 1k words.
        """
        word_count = count_words(text)

        # Bold (markdown **text** or __text__)
        bold_instances = re.findall(r'\*\*[^*]+\*\*|__[^_]+__', text)
        bold_count = len(bold_instances)
        bold_per_1k = (bold_count / word_count * 1000) if word_count > 0 else 0

        # Italic (markdown *text* or _text_)
        italic_instances = re.findall(r'\*[^*]+\*|_[^_]+_', text)
        italic_count = len(italic_instances)
        italic_per_1k = (italic_count / word_count * 1000) if word_count > 0 else 0

        # Calculate formatting consistency (spacing between bold/italic)
        # AI tends to use formatting at regular intervals
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        formatting_per_para = []
        for para in paragraphs:
            para_bold = len(re.findall(r'\*\*[^*]+\*\*|__[^_]+__', para))
            para_italic = len(re.findall(r'\*[^*]+\*|_[^_]+_', para))
            formatting_per_para.append(para_bold + para_italic)

        # Low variance = high consistency (AI-like)
        if len(formatting_per_para) > 1:
            mean_fmt = statistics.mean(formatting_per_para)
            stdev_fmt = statistics.stdev(formatting_per_para)
            consistency = 1.0 - min(1.0, stdev_fmt / (mean_fmt + 1))
        else:
            consistency = 0.0

        return {
            'bold_per_1k': round(bold_per_1k, 2),
            'italic_per_1k': round(italic_per_1k, 2),
            'formatting_consistency': round(consistency, 3)
        }

    def _analyze_em_dashes_detailed(self, lines: List[str], html_comment_checker=None) -> List[EmDashInstance]:
        """Track em-dashes with line numbers and context."""
        instances = []

        for line_num, line in enumerate(lines, start=1):
            # Skip HTML comments (metadata) and code blocks
            if html_comment_checker and html_comment_checker(line):
                continue
            if line.strip().startswith('```'):
                continue

            for match in re.finditer(r'—|--', line):
                # Get context around em-dash
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = f"...{line[start:end]}..."

                instances.append(EmDashInstance(
                    line_number=line_num,
                    context=context,
                    suggestion='Replace with period, semicolon, comma, or parentheses'
                ))

        return instances

    def _analyze_formatting_issues_detailed(self, lines: List[str], html_comment_checker=None) -> List[FormattingIssue]:
        """Detect excessive bold/italic usage and mechanical formatting patterns."""
        issues = []

        bold_pattern = re.compile(r'\*\*[^*]+\*\*|__[^_]+__')
        italic_pattern = re.compile(r'\*[^*]+\*|_[^_]+_')

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Skip HTML comments (metadata), headings, and code blocks
            if html_comment_checker and html_comment_checker(line):
                continue
            if stripped.startswith('#') or stripped.startswith('```'):
                continue

            if not stripped:
                continue

            # Count formatting on this line
            word_count = len(re.findall(r'\b\w+\b', line))
            if word_count == 0:
                continue

            bold_matches = list(bold_pattern.finditer(line))
            italic_matches = list(italic_pattern.finditer(line))

            bold_words = sum(len(re.findall(r'\b\w+\b', match.group())) for match in bold_matches)
            italic_words = sum(len(re.findall(r'\b\w+\b', match.group())) for match in italic_matches)

            bold_density = (bold_words / word_count) * 100 if word_count > 0 else 0
            italic_density = (italic_words / word_count) * 100 if word_count > 0 else 0

            # Excessive bold (>10% of words)
            if bold_density > 10:
                context = line.strip()[:100] + '...' if len(line.strip()) > 100 else line.strip()
                issues.append(FormattingIssue(
                    line_number=line_num,
                    issue_type='bold_dense',
                    context=context,
                    density=bold_density,
                    problem=f'Excessive bolding ({bold_density:.1f}% of words, target <5%)',
                    suggestion='Remove bold from less critical terms; reserve for key concepts only'
                ))

            # Excessive italic (>15% of words, excluding functional use)
            if italic_density > 15:
                context = line.strip()[:100] + '...' if len(line.strip()) > 100 else line.strip()
                issues.append(FormattingIssue(
                    line_number=line_num,
                    issue_type='italic_dense',
                    context=context,
                    density=italic_density,
                    problem=f'Excessive italics ({italic_density:.1f}% of words, target <10%)',
                    suggestion='Use italics functionally: titles, defined terms, subtle emphasis only'
                ))

        return issues

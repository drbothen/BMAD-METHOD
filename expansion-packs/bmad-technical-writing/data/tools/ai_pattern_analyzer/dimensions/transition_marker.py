"""
Transition Marker dimension analyzer.

Analyzes AI-specific transition word patterns that distinguish AI from human text:
- "however" usage (Human: 0-3 per 1k, AI: 5-10+ per 1k)
- "moreover" usage (Human: 0-1 per 1k, AI: 3-8+ per 1k)
- Marker clustering patterns (multiple markers in close proximity)

Weight: 10.0%
Tier: ADVANCED

These formal transition markers are reliable AI signatures.
Human writers use them sparingly, while AI models overuse them.

Requires dependencies: re (standard library)

Refactored in Story 1.4.5 - Split from StylometricDimension for single responsibility.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from ai_pattern_analyzer.dimensions.base_strategy import DimensionStrategy
from ai_pattern_analyzer.core.analysis_config import AnalysisConfig, DEFAULT_CONFIG
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry
from ai_pattern_analyzer.core.results import TransitionInstance  # Story 2.0: Use TransitionInstance (StylometricIssue removed in v5.0.0)


class TransitionMarkerDimension(DimensionStrategy):
    """
    Analyzes AI transition marker patterns (however, moreover).

    Weight: 10.0% of total score
    Tier: ADVANCED (specialized AI detection pattern)

    Detects:
    - Overuse of "however" (AI: 5-10+/1k, Human: 0-3/1k)
    - Overuse of "moreover" (AI: 3-8+/1k, Human: 0-1/1k)
    - Marker clustering (multiple instances in close proximity)

    Focuses ONLY on transition markers - does not collect readability metrics.
    This separation (Story 1.4.5) eliminates wasted computation and clarifies purpose.
    """

    def __init__(self):
        """Initialize and self-register with dimension registry."""
        super().__init__()
        # Self-register with registry
        DimensionRegistry.register(self)

    # ========================================================================
    # REQUIRED PROPERTIES - DimensionStrategy Contract
    # ========================================================================

    @property
    def dimension_name(self) -> str:
        """Return dimension identifier."""
        return "transition_marker"

    @property
    def weight(self) -> float:
        """Return dimension weight (10% of total score)."""
        return 10.0

    @property
    def tier(self) -> str:
        """Return dimension tier."""
        return "ADVANCED"

    @property
    def description(self) -> str:
        """Return dimension description."""
        return "Analyzes AI-specific transition markers (however, moreover) and clustering patterns"

    # ========================================================================
    # ANALYSIS METHODS
    # ========================================================================

    def analyze(
        self,
        text: str,
        lines: List[str] = None,
        config: Optional[AnalysisConfig] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Analyze text for AI transition marker patterns.

        ONLY collects transition marker metrics (no readability).
        This focused approach eliminates wasted computation.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            config: Analysis configuration (None = current behavior)
            **kwargs: Additional parameters (word_count if pre-calculated)

        Returns:
            Dict with transition marker analysis results:
            - however_count: Total "however" occurrences
            - moreover_count: Total "moreover" occurrences
            - however_per_1k: "however" frequency per 1000 words
            - moreover_per_1k: "moreover" frequency per 1000 words
            - total_ai_markers_per_1k: Combined marker frequency per 1000 words
        """
        config = config or DEFAULT_CONFIG
        total_text_length = len(text)

        # Prepare text based on mode (FAST/ADAPTIVE/SAMPLING/FULL)
        prepared = self._prepare_text(text, config, self.dimension_name)

        # Handle sampled analysis (returns list of (position, sample_text) tuples)
        if isinstance(prepared, list):
            samples = prepared
            sample_results = []

            for position, sample_text in samples:
                transition_markers = self._analyze_transition_markers(sample_text, **kwargs)
                sample_results.append(transition_markers)

            # Aggregate metrics from all samples
            aggregated = self._aggregate_sampled_metrics(sample_results)
            analyzed_length = sum(len(sample_text) for _, sample_text in samples)
            samples_analyzed = len(samples)

        # Handle direct analysis (returns string - truncated or full text)
        else:
            analyzed_text = prepared
            transition_markers = self._analyze_transition_markers(analyzed_text, **kwargs)
            aggregated = transition_markers
            analyzed_length = len(analyzed_text)
            samples_analyzed = 1

        # Add consistent metadata
        return {
            **aggregated,
            'available': True,
            'analysis_mode': config.mode.value,
            'samples_analyzed': samples_analyzed,
            'total_text_length': total_text_length,
            'analyzed_text_length': analyzed_length,
            'coverage_percentage': (analyzed_length / total_text_length * 100.0) if total_text_length > 0 else 0.0
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> List[TransitionInstance]:
        """
        Detailed analysis with line numbers and suggestions.
        Identifies each transition marker occurrence and clustering patterns.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            List of TransitionInstance objects (Story 2.0: migrated from StylometricIssue)
        """
        return self._analyze_stylometric_issues_detailed(lines, html_comment_checker)

    # ========================================================================
    # SCORING METHODS - DimensionStrategy Contract
    # ========================================================================

    def calculate_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate 0-100 score based on total AI markers per 1k words.

        Lower marker frequency = higher score (human-like).
        Higher marker frequency = lower score (AI-like).

        Algorithm:
        - Total markers ≤ 2.0 per 1k = 100 score (Excellent - human-like)
        - Total markers ≤ 4.0 per 1k = 75 score (Good)
        - Total markers ≤ 8.0 per 1k = 50 score (Concerning - AI pattern)
        - Total markers > 8.0 per 1k = 25 score (Strong AI signature)

        Research thresholds:
        - Human: 0-3 total markers per 1k
        - AI: 8+ total markers per 1k

        Args:
            metrics: Output from analyze() method

        Returns:
            Score from 0.0 (AI-like) to 100.0 (human-like)
        """
        if not metrics.get('available', False):
            return 50.0  # Neutral score for unavailable data

        # Score on total AI markers per 1k words
        total_markers = metrics.get('total_ai_markers_per_1k', 0.0)

        # Human: 0-3 total, AI: 8+
        if total_markers <= 2.0:
            score = 100.0  # Excellent - very human-like
        elif total_markers <= 4.0:
            score = 75.0  # Good - some markers but acceptable
        elif total_markers <= 8.0:
            score = 50.0  # Concerning - AI-like pattern
        else:
            score = 25.0  # Strong AI signature

        self._validate_score(score)
        return score

    def get_recommendations(self, score: float, metrics: Dict[str, Any]) -> List[str]:
        """
        Generate actionable recommendations based on score and metrics.

        Args:
            score: Current score from calculate_score()
            metrics: Raw metrics from analyze()

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if not metrics.get('available', False):
            recommendations.append(
                "Transition marker analysis unavailable."
            )
            return recommendations

        however_per_1k = metrics.get('however_per_1k', 0.0)
        moreover_per_1k = metrics.get('moreover_per_1k', 0.0)
        total_markers = metrics.get('total_ai_markers_per_1k', 0.0)

        if total_markers > 4.0:
            recommendations.append(
                f"Reduce AI transition markers ({total_markers:.1f} per 1k words, target ≤2.0). "
                f"These formal transitions are overused by AI text generators."
            )

        if however_per_1k > 3.0:
            recommendations.append(
                f"High 'however' usage ({however_per_1k:.1f} per 1k, target ≤3.0). "
                f"Replace with: 'but', 'yet', 'still', or natural flow without transition."
            )

        if moreover_per_1k > 1.0:
            recommendations.append(
                f"'Moreover' detected ({moreover_per_1k:.1f} per 1k, target ≤1.0). "
                f"This is a strong AI signature. Replace with: 'also', 'and', 'plus', or remove."
            )

        if total_markers > 8.0:
            recommendations.append(
                "Very high AI marker density detected. "
                "This suggests mechanical text generation. Thoroughly rewrite with natural transitions."
            )

        if total_markers <= 2.0:
            recommendations.append(
                f"Excellent transition marker usage ({total_markers:.1f} per 1k). "
                f"Text shows natural, human-like transition patterns."
            )

        return recommendations

    def get_tiers(self) -> Dict[str, Tuple[float, float]]:
        """
        Define score tier ranges for this dimension.

        Returns:
            Dict mapping tier name to (min_score, max_score) tuple
        """
        return {
            'excellent': (90.0, 100.0),
            'good': (75.0, 89.9),
            'acceptable': (50.0, 74.9),
            'poor': (0.0, 49.9)
        }

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _analyze_transition_markers(self, text: str, **kwargs) -> Dict:
        """
        Analyze AI-specific transition markers (however, moreover).

        Collects:
        - Raw counts of each marker
        - Frequency per 1k words
        - Total combined marker frequency
        """
        result = {}

        # Count AI-specific markers: however and moreover
        however_pattern = re.compile(r'\bhowever\b', re.IGNORECASE)
        moreover_pattern = re.compile(r'\bmoreover\b', re.IGNORECASE)

        however_count = len(however_pattern.findall(text))
        moreover_count = len(moreover_pattern.findall(text))

        # Calculate per 1k words
        # Use pre-calculated word_count if provided, otherwise calculate
        total_words = kwargs.get('word_count', None)
        if total_words is None:
            total_words = len(re.findall(r'\b\w+\b', text))

        words_in_thousands = total_words / 1000 if total_words > 0 else 1

        result['however_count'] = however_count
        result['moreover_count'] = moreover_count
        result['however_per_1k'] = however_count / words_in_thousands if words_in_thousands > 0 else 0.0
        result['moreover_per_1k'] = moreover_count / words_in_thousands if words_in_thousands > 0 else 0.0
        result['total_ai_markers_per_1k'] = (however_count + moreover_count) / words_in_thousands if words_in_thousands > 0 else 0.0

        return result

    def _analyze_stylometric_issues_detailed(self, lines: List[str], html_comment_checker=None) -> List[TransitionInstance]:
        """Detect AI-specific stylometric markers (however, moreover, clustering)."""
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
                # Story 2.0: Use TransitionInstance (StylometricIssue removed in v5.0.0)
                issues.append(TransitionInstance(
                    line_number=line_num,
                    transition='however',
                    context=context[:120] + '...' if len(context) > 120 else context,
                    suggestions=['Replace with: "But", "Yet", "Still"', 'Use natural flow without transition']
                ))

            # Check for "moreover" (AI: 3-7 per 1k, Human: 0-1 per 1k)
            moreover_matches = list(moreover_pattern.finditer(line))
            for match in moreover_matches:
                context = line.strip()
                # Story 2.0: Use TransitionInstance (StylometricIssue removed in v5.0.0)
                issues.append(TransitionInstance(
                    line_number=line_num,
                    transition='moreover',
                    context=context[:120] + '...' if len(context) > 120 else context,
                    suggestions=['Replace with: "Also", "And", "Plus"', 'Remove transition entirely']
                ))

        # Check for clusters (multiple "however" in close proximity)
        however_lines = [i for i, line in enumerate(lines, start=1)
                        if however_pattern.search(line)]
        for i in range(len(however_lines) - 1):
            if however_lines[i+1] - however_lines[i] <= 3:  # Within 3 lines
                # Story 2.0: Use TransitionInstance (StylometricIssue removed in v5.0.0)
                issues.append(TransitionInstance(
                    line_number=however_lines[i],
                    transition='however_cluster',
                    context=f'Lines {however_lines[i]}-{however_lines[i+1]}',
                    suggestions=['Vary transitions', 'Remove some instances entirely']
                ))

        return issues


# Backward compatibility alias
TransitionMarkerAnalyzer = TransitionMarkerDimension

# Module-level singleton - triggers self-registration on module import
_instance = TransitionMarkerDimension()

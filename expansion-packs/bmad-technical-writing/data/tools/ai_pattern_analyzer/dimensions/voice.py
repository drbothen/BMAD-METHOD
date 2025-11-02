"""
Voice dimension analyzer.

Analyzes voice and authenticity markers:
- First-person perspective (I, we, my, our)
- Direct address (you, your)
- Contractions
- Technical domain expertise

Human writing shows personal voice, while AI tends toward impersonal formality.
"""

import re
from typing import Dict, List, Any, Optional
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS


class VoiceAnalyzer(DimensionAnalyzer):
    """Analyzes voice dimension - first-person, direct address, contractions."""

    def __init__(self, domain_terms: Optional[List[str]] = None):
        """
        Initialize voice analyzer.

        Args:
            domain_terms: Optional list of domain-specific technical terms
        """
        self.domain_terms = domain_terms or []

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for voice patterns.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with voice analysis results
        """
        # TODO: Extract from analyze_ai_patterns.py lines 3627-3660
        voice = self._analyze_voice(text)
        technical = self._analyze_technical_depth(text)

        return {
            'voice': voice,
            'technical_depth': technical,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> Dict[str, Any]:
        """
        Detailed analysis - voice typically doesn't need line-level detail.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            Dict with summary analysis
        """
        # Voice analysis is typically aggregate, not line-by-line
        text = '\n'.join(lines)
        return self.analyze(text, lines)

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate voice score.

        Human writing shows personal voice through first-person perspective,
        direct address, and contractions. AI tends toward impersonal formality.

        Args:
            analysis_results: Results dict with voice metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        from ai_pattern_analyzer.utils.text_processing import safe_ratio

        markers = 0

        first_person = analysis_results.get('first_person', 0)
        direct_address = analysis_results.get('direct_address', 0)
        contractions = analysis_results.get('contractions', 0)
        total_words = analysis_results.get('total_words', 1)

        # First person or direct address
        if first_person > 0 or direct_address > 10:
            markers += 1

        # Contractions (indicates conversational tone)
        contraction_ratio = safe_ratio(contractions, total_words, 0) * 100
        if contraction_ratio > THRESHOLDS.CONTRACTION_RATIO_GOOD:  # >1% contraction use
            markers += 1

        # Check for both types of engagement
        if first_person > 0 and direct_address > 10:
            markers += 1

        if markers >= 3:
            return (10.0, "HIGH")
        elif markers == 2:
            return (7.0, "MEDIUM")
        elif markers == 1:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")

    def _analyze_voice(self, text: str) -> Dict:
        """Analyze voice and authenticity markers."""
        first_person = len(re.findall(
            r"\b(I|we|my|our|us|me|I've|I'm|we've|I'd|we're|I'll|we'll)\b",
            text, re.IGNORECASE
        ))

        direct_address = len(re.findall(
            r"\b(you|your|you're|you'll|you've|you'd)\b",
            text, re.IGNORECASE
        ))

        # Count contractions
        contractions = len(re.findall(
            r"\b\w+'\w+\b",  # Word with apostrophe (simplified)
            text
        ))

        return {
            'first_person': first_person,
            'direct_address': direct_address,
            'contractions': contractions
        }

    def _analyze_technical_depth(self, text: str) -> Dict:
        """Analyze technical domain expertise signals."""
        terms_found = []
        for pattern in self.domain_terms:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            terms_found.extend([m.group() for m in matches])

        return {
            'count': len(terms_found),
            'terms': terms_found[:20]  # Limit for readability
        }

"""
Lexical dimension analyzer.

Analyzes lexical diversity and vocabulary patterns:
- Type-Token Ratio (TTR)
- Moving Average Type-Token Ratio (MTLD) - more accurate for long texts
- Stemmed diversity (catches word variants)
- Vocabulary richness

Requires optional dependency: nltk (for advanced metrics)

Low lexical diversity (repetitive vocabulary) is an AI signature.
"""

import re
import sys
from typing import Dict, List, Any
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS

# Required imports
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


class LexicalAnalyzer(DimensionAnalyzer):
    """Analyzes lexical dimension - vocabulary diversity (TTR)."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for lexical diversity.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with lexical analysis results
        """
        lexical = self._analyze_lexical_diversity(text)

        nltk_metrics = self._analyze_nltk_lexical(text)
        lexical.update(nltk_metrics)

        return {
            'lexical_diversity': lexical,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> Dict[str, Any]:
        """
        Detailed analysis - lexical diversity is typically aggregate.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            Dict with analysis results
        """
        # Lexical analysis is typically aggregate, not line-by-line
        text = '\n'.join(lines)
        return self.analyze(text, lines)

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate lexical diversity score.

        Args:
            analysis_results: Results dict with TTR metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        ttr = analysis_results.get('diversity', 0.0)

        if ttr >= 0.60:
            return (10.0, "HIGH")
        elif ttr >= 0.45:
            return (7.0, "MEDIUM")
        elif ttr >= 0.30:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")

    def _analyze_lexical_diversity(self, text: str) -> Dict:
        """Calculate Type-Token Ratio (lexical diversity)."""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Get all words (lowercase for uniqueness)
        words = [w.lower() for w in re.findall(r"\b[\w'-]+\b", text)]

        if not words:
            return {'unique': 0, 'diversity': 0}

        unique = len(set(words))
        diversity = unique / len(words)

        return {
            'unique': unique,
            'diversity': round(diversity, 3)
        }

    def _analyze_nltk_lexical(self, text: str) -> Dict:
        """Enhanced lexical diversity using NLTK."""
        try:
            # Remove code blocks
            text = re.sub(r'```[\s\S]*?```', '', text)

            # Tokenize
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalnum()]  # Keep only alphanumeric

            if not words:
                return {}

            # Calculate MTLD (Moving Average Type-Token Ratio)
            # This is more accurate than simple TTR for longer texts
            mtld = self._calculate_mtld(words)

            # Calculate stemmed diversity (catches word variants)
            stemmer = PorterStemmer()
            stemmed = [stemmer.stem(w) for w in words]
            stemmed_unique = len(set(stemmed))
            stemmed_diversity = stemmed_unique / len(stemmed) if stemmed else 0

            return {
                'mtld_score': round(mtld, 2),
                'stemmed_diversity': round(stemmed_diversity, 3)
            }
        except Exception as e:
            print(f"Warning: NLTK lexical analysis failed: {e}", file=sys.stderr)
            return {}

    def _calculate_mtld(self, words: List[str], threshold: float = 0.72) -> float:
        """Calculate Moving Average Type-Token Ratio (MTLD)."""
        if len(words) < 50:
            return len(set(words)) / len(words) * 100  # Fallback to TTR

        def _mtld_direction(words_list):
            factor = 0
            factor_lengths = []
            types_seen = set()
            tokens = 0

            for word in words_list:
                tokens += 1
                types_seen.add(word)
                if len(types_seen) / tokens < threshold:
                    factor += 1
                    factor_lengths.append(tokens)
                    types_seen = set()
                    tokens = 0

            # Add partial factor
            if tokens > 0:
                factor += (1 - (len(types_seen) / tokens)) / (1 - threshold)

            return (len(words_list) / factor) if factor > 0 else len(words_list)

        # Calculate in both directions and average
        forward = _mtld_direction(words)
        backward = _mtld_direction(words[::-1])

        return (forward + backward) / 2

"""
Base dimension analyzer interface.

All dimension analyzers should inherit from this base class
to ensure consistent interface across the analysis system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class DimensionAnalyzer(ABC):
    """Base class for all dimension analyzers."""

    @abstractmethod
    def analyze(self, text: str, lines: List[str], **kwargs) -> Dict[str, Any]:
        """
        Analyze text for this dimension.

        Args:
            text: Full text content
            lines: Text split into lines
            **kwargs: Additional analysis parameters

        Returns:
            Dict with analysis results specific to this dimension
        """
        pass

    @abstractmethod
    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate score for this dimension.

        Args:
            analysis_results: Results from analyze()

        Returns:
            Tuple of (score_value, score_label) where:
                - score_value is a float (0.0 to max_score for this dimension)
                - score_label is a string like 'HIGH', 'MEDIUM', 'LOW', etc.
        """
        pass

    def get_max_score(self) -> float:
        """
        Get maximum possible score for this dimension.

        Returns:
            Maximum score value
        """
        return 10.0  # Default, can be overridden

    def get_dimension_name(self) -> str:
        """
        Get the name of this dimension.

        Returns:
            Dimension name
        """
        return self.__class__.__name__.replace('Analyzer', '')

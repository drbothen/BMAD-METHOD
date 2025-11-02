"""
Score history tracking module.

This module handles tracking score history over time, allowing users to
monitor improvements and trends in their content's AI detection risk and quality scores.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class HistoricalScore:
    """Historical score tracking"""
    timestamp: str
    detection_risk: float
    quality_score: float
    detection_interpretation: str
    quality_interpretation: str
    total_words: int
    notes: str = ""


@dataclass
class ScoreHistory:
    """Score history for a document"""
    file_path: str
    scores: List[HistoricalScore] = field(default_factory=list)

    def add_score(self, score, notes: str = ""):
        """
        Add a score to history.

        Args:
            score: DualScore object
            notes: Optional notes about this version
        """
        self.scores.append(HistoricalScore(
            timestamp=score.timestamp,
            detection_risk=score.detection_risk,
            quality_score=score.quality_score,
            detection_interpretation=score.detection_interpretation,
            quality_interpretation=score.quality_interpretation,
            total_words=score.total_words,
            notes=notes
        ))

    def get_trend(self) -> Dict[str, str]:
        """
        Get trend direction.

        Returns:
            Dict with detection and quality trends
        """
        if len(self.scores) < 2:
            return {'detection': 'N/A', 'quality': 'N/A'}

        det_change = self.scores[-1].detection_risk - self.scores[-2].detection_risk
        qual_change = self.scores[-1].quality_score - self.scores[-2].quality_score

        return {
            'detection': 'IMPROVING' if det_change < -1 else 'WORSENING' if det_change > 1 else 'STABLE',
            'quality': 'IMPROVING' if qual_change > 1 else 'DECLINING' if qual_change < -1 else 'STABLE',
            'detection_change': round(det_change, 1),
            'quality_change': round(qual_change, 1)
        }


# Placeholder functions (to be implemented from main file)
def load_score_history(file_path: str) -> ScoreHistory:
    """
    Load score history from file.

    This function will be extracted from the main analyze_ai_patterns.py file.
    """
    raise NotImplementedError("load_score_history will be extracted during refactoring")


def save_score_history(history: ScoreHistory):
    """
    Save score history to file.

    This function will be extracted from the main analyze_ai_patterns.py file.
    """
    raise NotImplementedError("save_score_history will be extracted during refactoring")

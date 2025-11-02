"""
Scoring system module.
"""

from ai_pattern_analyzer.scoring.dual_score import (
    DualScore,
    ScoreCategory,
    ScoreDimension,
    ImprovementAction,
    THRESHOLDS
)
from ai_pattern_analyzer.scoring.dual_score_calculator import calculate_dual_score

__all__ = [
    'DualScore',
    'ScoreCategory',
    'ScoreDimension',
    'ImprovementAction',
    'THRESHOLDS',
    'calculate_dual_score'
]

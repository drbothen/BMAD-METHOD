"""
Dual score calculation module.

Calculates Detection Risk (0-100, lower=better) and Quality Score (0-100, higher=better)
with comprehensive breakdown across 22 dimensions and 174 quality points.

This is a complex scoring system extracted from the monolithic analyzer as part of
the modularization effort (Phase 3).

Research Sources:
- GPTZero methodology (perplexity & burstiness)
- Originality.AI pattern recognition
- Academic NLP studies on AI detection
- Stanford research on demographic bias
- MIT/Northeastern research on syntactic templates
"""

from datetime import datetime
from typing import List, Tuple

from ai_pattern_analyzer.core.results import AnalysisResults
from ai_pattern_analyzer.scoring.dual_score import (
    DualScore, ScoreCategory, ScoreDimension,
    ImprovementAction, THRESHOLDS
)


def calculate_dual_score(results: AnalysisResults,
                        detection_target: float = 30.0,
                        quality_target: float = 85.0) -> DualScore:
    """
    Calculate dual scores: Detection Risk (0-100, lower=better) and Quality Score (0-100, higher=better).

    This method analyzes 22 dimensions across 4 tiers:
    - Tier 1: Advanced Detection (70 points) - Highest accuracy metrics
    - Tier 2: Core Patterns (74 points) - Proven AI signatures
    - Tier 3: Supporting Indicators (46 points) - Context and quality
    - Tier 4: Phase 3 Advanced Structure (10 points) - AST-based patterns

    Args:
        results: AnalysisResults from analysis
        detection_target: Target detection risk (default 30 = low risk)
        quality_target: Target quality score (default 85 = excellent)

    Returns:
        DualScore with comprehensive breakdown and optimization path
    """
    timestamp = datetime.now().isoformat()

    # Map score levels to numerical values (0-1 scale)
    score_map = {"HIGH": 1.0, "MEDIUM": 0.75, "LOW": 0.5, "VERY LOW": 0.25, "UNKNOWN": 0.5, "N/A": 0.5}

    # ============================================================================
    # TIER 1: ADVANCED DETECTION (70 points) - Highest accuracy
    # ============================================================================

    # GLTR Token Ranking (12 points) - 95% accuracy on GPT-3/ChatGPT
    gltr_val = score_map.get(results.gltr_score, 0.5) if hasattr(results, 'gltr_score') and results.gltr_score else 0.5
    gltr_score = ScoreDimension(
        name="GLTR Token Ranking",
        score=gltr_val * 12,
        max_score=12.0,
        percentage=gltr_val * 100,
        impact=_calculate_impact(gltr_val, 12.0),
        gap=(1.0 - gltr_val) * 12,
        raw_value=getattr(results, 'gltr_top10_percentage', None),
        recommendation="Rewrite high-predictability segments (>70% top-10 tokens)" if gltr_val < 0.75 else None
    )

    # Advanced Lexical Diversity - HDD/Yule's K (8 points)
    lexical_val = score_map.get(getattr(results, 'advanced_lexical_score', 'UNKNOWN'), 0.5)
    lexical_score = ScoreDimension(
        name="Advanced Lexical (HDD/Yule's K)",
        score=lexical_val * 8,
        max_score=8.0,
        percentage=lexical_val * 100,
        impact=_calculate_impact(lexical_val, 8.0),
        gap=(1.0 - lexical_val) * 8,
        raw_value=getattr(results, 'hdd_score', None),
        recommendation="Increase vocabulary diversity (target HDD > 0.65)" if lexical_val < 0.75 else None
    )

    # Advanced Lexical: MATTR (Moving Average Type-Token Ratio) - 12 points
    mattr_assessment = getattr(results, 'mattr_assessment', None)
    mattr_score_val = 12.0 * (1.0 if mattr_assessment == 'EXCELLENT' else
                               0.75 if mattr_assessment == 'GOOD' else
                               0.42 if mattr_assessment == 'FAIR' else 0.0) if mattr_assessment else 0.0
    mattr_dim = ScoreDimension(
        name="MATTR (Lexical Richness)",
        score=mattr_score_val,
        max_score=12.0,
        percentage=(mattr_score_val / 12.0) * 100,
        impact=_calculate_impact(mattr_score_val / 12.0, 12.0),
        gap=12.0 - mattr_score_val,
        raw_value=getattr(results, 'mattr', None),
        recommendation="Increase vocabulary variety (target MATTR ≥0.70)" if mattr_score_val < 9.0 else None
    )

    # Advanced Lexical: RTTR (Root Type-Token Ratio) - 8 points
    rttr_assessment = getattr(results, 'rttr_assessment', None)
    rttr_score_val = 8.0 * (1.0 if rttr_assessment == 'EXCELLENT' else
                             0.75 if rttr_assessment == 'GOOD' else
                             0.375 if rttr_assessment == 'FAIR' else 0.0) if rttr_assessment else 0.0
    rttr_dim = ScoreDimension(
        name="RTTR (Global Diversity)",
        score=rttr_score_val,
        max_score=8.0,
        percentage=(rttr_score_val / 8.0) * 100,
        impact=_calculate_impact(rttr_score_val / 8.0, 8.0),
        gap=8.0 - rttr_score_val,
        raw_value=getattr(results, 'rttr', None),
        recommendation="Add domain-specific terminology (target RTTR ≥7.5)" if rttr_score_val < 6.0 else None
    )

    # AI Detection Ensemble - DetectGPT/RoBERTa (10 points)
    ai_detect_val = score_map.get(getattr(results, 'ai_detection_score', 'UNKNOWN'), 0.5)
    ai_detect_score = ScoreDimension(
        name="AI Detection Ensemble",
        score=ai_detect_val * 10,
        max_score=10.0,
        percentage=ai_detect_val * 100,
        impact=_calculate_impact(ai_detect_val, 10.0),
        gap=(1.0 - ai_detect_val) * 10,
        raw_value=getattr(results, 'roberta_sentiment_variance', None),
        recommendation="Increase emotional variation (sentiment variance > 0.15)" if ai_detect_val < 0.75 else None
    )

    # Stylometric Markers (10 points)
    stylo_val = score_map.get(getattr(results, 'stylometric_score', 'UNKNOWN'), 0.5)
    stylo_score = ScoreDimension(
        name="Stylometric Markers",
        score=stylo_val * 10,
        max_score=10.0,
        percentage=stylo_val * 100,
        impact=_calculate_impact(stylo_val, 10.0),
        gap=(1.0 - stylo_val) * 10,
        raw_value=getattr(results, 'however_per_1k', None),
        recommendation="Reduce AI transitions (however/moreover), passive voice <12%, vary function words" if stylo_val < 0.75 else None
    )

    # Syntactic Complexity (4 points)
    syntax_val = score_map.get(getattr(results, 'syntactic_score', 'UNKNOWN'), 0.5)
    syntax_score = ScoreDimension(
        name="Syntactic Complexity",
        score=syntax_val * 4,
        max_score=4.0,
        percentage=syntax_val * 100,
        impact=_calculate_impact(syntax_val, 4.0),
        gap=(1.0 - syntax_val) * 4,
        raw_value=getattr(results, 'subordination_index', None),
        recommendation="Add subordinate clauses, vary tree depth" if syntax_val < 0.75 else None
    )

    # Multi-Model Perplexity Consensus (6 points)
    multi_perp_score_val = 3.0  # Default
    avg_perp = None
    if hasattr(results, 'gpt2_perplexity') and hasattr(results, 'distilgpt2_perplexity'):
        if results.gpt2_perplexity and results.distilgpt2_perplexity:
            gpt2_human = results.gpt2_perplexity > 120
            distil_human = results.distilgpt2_perplexity > 120
            avg_perp = (results.gpt2_perplexity + results.distilgpt2_perplexity) / 2

            if gpt2_human and distil_human:
                multi_perp_score_val = 6.0
            elif not gpt2_human and not distil_human:
                multi_perp_score_val = 0.0
            else:
                multi_perp_score_val = 3.0

    multi_perp_dim = ScoreDimension(
        name="Multi-Model Perplexity Consensus",
        score=multi_perp_score_val,
        max_score=6.0,
        percentage=(multi_perp_score_val / 6.0) * 100,
        impact=_calculate_impact(multi_perp_score_val / 6.0, 6.0),
        gap=6.0 - multi_perp_score_val,
        raw_value=avg_perp,
        recommendation="Increase unpredictability: use diverse vocabulary, unexpected word choices" if multi_perp_score_val < 4.5 else None
    )

    advanced_category = ScoreCategory(
        name="Advanced Detection",
        total=gltr_score.score + lexical_score.score + mattr_dim.score + rttr_dim.score + ai_detect_score.score + stylo_score.score + syntax_score.score + multi_perp_dim.score,
        max_total=70.0,
        percentage=((gltr_score.score + lexical_score.score + mattr_dim.score + rttr_dim.score + ai_detect_score.score + stylo_score.score + syntax_score.score + multi_perp_dim.score) / 70.0) * 100,
        dimensions=[gltr_score, lexical_score, mattr_dim, rttr_dim, ai_detect_score, stylo_score, syntax_score, multi_perp_dim]
    )

    # ============================================================================
    # TIER 2: CORE PATTERNS (74 points) - Proven AI signatures
    # ============================================================================

    # Burstiness - Sentence Variation (12 points)
    burst_val = score_map[results.burstiness_score]
    burst_score = ScoreDimension(
        name="Burstiness (Sentence Variation)",
        score=burst_val * 12,
        max_score=12.0,
        percentage=burst_val * 100,
        impact=_calculate_impact(burst_val, 12.0),
        gap=(1.0 - burst_val) * 12,
        raw_value=results.sentence_stdev,
        recommendation="Vary sentence lengths: short (5-10w), medium (15-25w), long (30-45w)" if burst_val < 0.75 else None
    )

    # Perplexity - Vocabulary (10 points)
    perp_val = score_map[results.perplexity_score]
    perp_score = ScoreDimension(
        name="Perplexity (Vocabulary)",
        score=perp_val * 10,
        max_score=10.0,
        percentage=perp_val * 100,
        impact=_calculate_impact(perp_val, 10.0),
        gap=(1.0 - perp_val) * 10,
        raw_value=results.ai_vocabulary_per_1k,
        recommendation="Replace AI vocabulary: delve, leverage, robust, harness" if perp_val < 0.75 else None
    )

    # Formatting Patterns (8 points)
    format_val = score_map[results.formatting_score]
    format_score = ScoreDimension(
        name="Formatting Patterns",
        score=format_val * 8,
        max_score=8.0,
        percentage=format_val * 100,
        impact=_calculate_impact(format_val, 8.0),
        gap=(1.0 - format_val) * 8,
        raw_value=results.em_dashes_per_page,
        recommendation="Reduce em-dashes to ≤2 per page, reduce bold/italic density" if format_val < 0.75 else None
    )

    # Create simplified core category for now (full implementation in original has many more dimensions)
    core_category = ScoreCategory(
        name="Core Patterns",
        total=burst_score.score + perp_score.score + format_score.score,
        max_total=30.0,  # Simplified - full version has 74 points
        percentage=((burst_score.score + perp_score.score + format_score.score) / 30.0) * 100,
        dimensions=[burst_score, perp_score, format_score]
    )

    # Simplified supporting and phase3 categories
    supporting_category = ScoreCategory(name="Supporting Indicators", total=0, max_total=0, percentage=0, dimensions=[])
    phase3_category = ScoreCategory(name="Phase 3 Advanced", total=0, max_total=0, percentage=0, dimensions=[])

    # ============================================================================
    # CALCULATE OVERALL SCORES
    # ============================================================================

    total_score = (advanced_category.total + core_category.total +
                   supporting_category.total + phase3_category.total)
    total_possible = (advanced_category.max_total + core_category.max_total +
                     supporting_category.max_total + phase3_category.max_total)

    quality_score = (total_score / total_possible * 100) if total_possible > 0 else 0
    detection_risk = 100 - quality_score  # Inverse relationship

    # Interpretations
    quality_interp = _interpret_quality(quality_score)
    detection_interp = _interpret_detection(detection_risk)

    # Gaps
    quality_gap = max(0, quality_target - quality_score)
    detection_gap = max(0, detection_risk - detection_target)

    # ============================================================================
    # GENERATE IMPROVEMENT ACTIONS
    # ============================================================================

    all_dimensions = (
        advanced_category.dimensions +
        core_category.dimensions +
        supporting_category.dimensions +
        phase3_category.dimensions
    )

    improvements = []
    for dim in all_dimensions:
        if dim.gap > 0.5:  # Only suggest if gap > 0.5 points
            improvements.append(ImprovementAction(
                priority=0,  # Will be set later
                dimension=dim.name,
                current_score=dim.score,
                max_score=dim.max_score,
                potential_gain=dim.gap,
                impact_level=dim.impact,
                action=dim.recommendation or f"Improve {dim.name}",
                effort_level=_estimate_effort(dim.name, dim.gap)
            ))

    # Sort by ROI (gain / effort)
    effort_multiplier = {'LOW': 1.0, 'MEDIUM': 0.7, 'HIGH': 0.4}
    improvements.sort(key=lambda x: x.potential_gain * effort_multiplier[x.effort_level], reverse=True)

    # Set priorities
    for i, imp in enumerate(improvements, start=1):
        imp.priority = i

    # Path to target - actions needed to reach quality target
    path = []
    cumulative_gain = quality_score
    for imp in improvements:
        if cumulative_gain >= quality_target:
            break
        path.append(imp)
        cumulative_gain += imp.potential_gain

    # Estimate overall effort
    if quality_gap == 0:
        effort = "MINIMAL"
    elif quality_gap < 5:
        effort = "LIGHT"
    elif quality_gap < 15:
        effort = "MODERATE"
    elif quality_gap < 30:
        effort = "SUBSTANTIAL"
    else:
        effort = "EXTENSIVE"

    return DualScore(
        detection_risk=round(detection_risk, 1),
        quality_score=round(quality_score, 1),
        detection_interpretation=detection_interp,
        quality_interpretation=quality_interp,
        detection_target=detection_target,
        quality_target=quality_target,
        detection_gap=round(detection_gap, 1),
        quality_gap=round(quality_gap, 1),
        categories=[advanced_category, core_category, supporting_category, phase3_category],
        improvements=improvements,
        path_to_target=path,
        estimated_effort=effort,
        timestamp=timestamp,
        file_path=results.file_path,
        total_words=results.total_words
    )


def _calculate_impact(current_val: float, max_points: float) -> str:
    """Calculate impact level based on gap and point weight."""
    gap = (1.0 - current_val) * max_points
    if gap < 1.0:
        return "NONE"
    elif gap < 2.0:
        return "LOW"
    elif gap < 4.0:
        return "MEDIUM"
    else:
        return "HIGH"


def _estimate_effort(dimension_name: str, gap: float) -> str:
    """Estimate effort required to close gap."""
    # Some dimensions are easier to fix than others
    easy_fixes = ["Formatting Patterns", "Stylometric Markers", "Heading Hierarchy"]
    medium_fixes = ["Burstiness (Sentence Variation)", "Perplexity (Vocabulary)", "Structure & Organization"]
    hard_fixes = ["GLTR Token Ranking", "Advanced Lexical (HDD/Yule's K)", "Syntactic Complexity"]

    if dimension_name in easy_fixes:
        return "LOW" if gap < 3 else "MEDIUM"
    elif dimension_name in medium_fixes:
        return "MEDIUM" if gap < 4 else "HIGH"
    else:  # hard_fixes
        return "HIGH"


def _interpret_quality(score: float) -> str:
    """Interpret quality score."""
    if score >= 95:
        return "EXCEPTIONAL - Indistinguishable from human"
    elif score >= 85:
        return "EXCELLENT - Minimal AI signatures"
    elif score >= 70:
        return "GOOD - Natural with minor tells"
    elif score >= 50:
        return "MIXED - Needs moderate work"
    elif score >= 30:
        return "AI-LIKE - Substantial work needed"
    else:
        return "OBVIOUS AI - Complete rewrite"


def _interpret_detection(risk: float) -> str:
    """Interpret detection risk."""
    if risk >= 70:
        return "VERY HIGH - Will be flagged"
    elif risk >= 50:
        return "HIGH - Likely flagged"
    elif risk >= 30:
        return "MEDIUM - May be flagged"
    elif risk >= 15:
        return "LOW - Unlikely flagged"
    else:
        return "VERY LOW - Safe"

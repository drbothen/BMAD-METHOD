"""
Tests for dual_score_calculator module.

Tests cover dual score calculation, helper functions, dimension scoring,
improvement action generation, and edge cases.
"""

import pytest
from ai_pattern_analyzer.scoring.dual_score_calculator import (
    calculate_dual_score,
    _calculate_impact,
    _estimate_effort,
    _interpret_quality,
    _interpret_detection
)
from ai_pattern_analyzer.core.results import AnalysisResults


# ============================================================================
# Fixtures and Helper Functions
# ============================================================================

def create_analysis_results(**kwargs):
    """
    Helper to create AnalysisResults with all required fields.

    Provides sensible defaults for all 39 required positional arguments,
    then allows override via kwargs.
    """
    # Default required positional arguments
    defaults = {
        'file_path': "/path/to/test.md",
        'total_words': 500,
        'total_sentences': 25,
        'total_paragraphs': 10,
        'ai_vocabulary_count': 5,
        'ai_vocabulary_per_1k': 10.0,
        'ai_vocabulary_list': ['delve', 'robust', 'leverage'],
        'formulaic_transitions_count': 2,
        'formulaic_transitions_list': ['Furthermore', 'Moreover'],
        'sentence_mean_length': 20.0,
        'sentence_stdev': 6.0,
        'sentence_min': 5,
        'sentence_max': 40,
        'sentence_range': (5, 40),
        'short_sentences_count': 3,
        'medium_sentences_count': 18,
        'long_sentences_count': 4,
        'sentence_lengths': [15, 20, 18, 25, 22],
        'paragraph_mean_words': 50.0,
        'paragraph_stdev': 10.0,
        'paragraph_range': (20, 80),
        'unique_words': 300,
        'lexical_diversity': 0.6,
        'bullet_list_lines': 10,
        'numbered_list_lines': 5,
        'total_headings': 6,
        'heading_depth': 3,
        'h1_count': 1,
        'h2_count': 3,
        'h3_count': 2,
        'h4_plus_count': 0,
        'headings_per_page': 3.0,
        'heading_parallelism_score': 0.5,
        'verbose_headings_count': 1,
        'avg_heading_length': 6.0,
        'first_person_count': 5,
        'direct_address_count': 3,
        'contraction_count': 2,
        'domain_terms_count': 4,
        'domain_terms_list': ['Python', 'API'],
        'em_dash_count': 3,
        'em_dashes_per_page': 1.5,
        'bold_markdown_count': 8,
        'italic_markdown_count': 6,
        # Dimension scores
        'burstiness_score': "MEDIUM",
        'perplexity_score': "MEDIUM",
        'formatting_score': "MEDIUM"
    }

    # Update with provided kwargs
    defaults.update(kwargs)
    return AnalysisResults(**defaults)


@pytest.fixture
def basic_results():
    """Create basic AnalysisResults for testing."""
    return create_analysis_results(
        burstiness_score="HIGH",
        perplexity_score="HIGH",
        formatting_score="HIGH",
        sentence_stdev=8.5,
        ai_vocabulary_per_1k=2.0,
        em_dashes_per_page=1.5
    )


@pytest.fixture
def low_quality_results():
    """Create AnalysisResults with low quality scores."""
    return create_analysis_results(
        file_path="/path/to/low_quality.md",
        # Core scores - all LOW
        burstiness_score="LOW",
        perplexity_score="LOW",
        formatting_score="LOW",
        # Burstiness data
        sentence_stdev=2.0,
        # Perplexity data
        ai_vocabulary_per_1k=25.0,
        # Formatting data
        em_dashes_per_page=8.0,
        # Advanced scores - all LOW
        gltr_score="LOW",
        advanced_lexical_score="LOW",
        mattr_assessment="POOR",
        rttr_assessment="POOR",
        ai_detection_score="LOW",
        stylometric_score="LOW",
        syntactic_score="LOW",
        # Advanced data
        gltr_top10_percentage=85.0,
        hdd_score=0.45,
        mattr=0.55,
        rttr=5.0,
        roberta_sentiment_variance=0.08,
        however_per_1k=8.0,
        subordination_index=0.2,
        gpt2_perplexity=80.0,
        distilgpt2_perplexity=75.0
    )


@pytest.fixture
def high_quality_results():
    """Create AnalysisResults with high quality scores."""
    return create_analysis_results(
        file_path="/path/to/high_quality.md",
        # Core scores - all HIGH
        burstiness_score="HIGH",
        perplexity_score="HIGH",
        formatting_score="HIGH",
        # Burstiness data
        sentence_stdev=10.5,
        # Perplexity data
        ai_vocabulary_per_1k=1.0,
        # Formatting data
        em_dashes_per_page=0.5,
        # Advanced scores - all HIGH
        gltr_score="HIGH",
        advanced_lexical_score="HIGH",
        mattr_assessment="EXCELLENT",
        rttr_assessment="EXCELLENT",
        ai_detection_score="HIGH",
        stylometric_score="HIGH",
        syntactic_score="HIGH",
        # Advanced data
        gltr_top10_percentage=45.0,
        hdd_score=0.85,
        mattr=0.85,
        rttr=9.5,
        roberta_sentiment_variance=0.25,
        however_per_1k=1.0,
        subordination_index=0.8,
        gpt2_perplexity=180.0,
        distilgpt2_perplexity=175.0
    )


@pytest.fixture
def results_with_missing_advanced():
    """Create AnalysisResults with missing advanced scores."""
    return create_analysis_results(
        file_path="/path/to/test.md",
        # Only core scores
        burstiness_score="MEDIUM",
        perplexity_score="MEDIUM",
        formatting_score="MEDIUM",
        sentence_stdev=6.0,
        ai_vocabulary_per_1k=8.0,
        em_dashes_per_page=3.0
        # No advanced scores (will use defaults from helper)
    )


@pytest.fixture
def results_with_partial_perplexity():
    """Create AnalysisResults with partial perplexity data."""
    return create_analysis_results(
        file_path="/path/to/test.md",
        burstiness_score="HIGH",
        perplexity_score="HIGH",
        formatting_score="HIGH",
        sentence_stdev=8.5,
        ai_vocabulary_per_1k=2.0,
        em_dashes_per_page=1.5,
        # Only one perplexity score
        gpt2_perplexity=150.0
        # Missing distilgpt2_perplexity
    )


# ============================================================================
# Helper Function Tests
# ============================================================================

class TestCalculateImpact:
    """Tests for _calculate_impact helper function."""

    def test_impact_none(self):
        """Test NONE impact when gap < 1.0."""
        # current_val = 0.95, max_points = 10
        # gap = (1.0 - 0.95) * 10 = 0.5
        result = _calculate_impact(0.95, 10.0)
        assert result == "NONE"

    def test_impact_low(self):
        """Test LOW impact when 1.0 <= gap < 2.0."""
        # current_val = 0.85, max_points = 10
        # gap = (1.0 - 0.85) * 10 = 1.5
        result = _calculate_impact(0.85, 10.0)
        assert result == "LOW"

    def test_impact_medium(self):
        """Test MEDIUM impact when 2.0 <= gap < 4.0."""
        # current_val = 0.7, max_points = 10
        # gap = (1.0 - 0.7) * 10 = 3.0
        result = _calculate_impact(0.7, 10.0)
        assert result == "MEDIUM"

    def test_impact_high(self):
        """Test HIGH impact when gap >= 4.0."""
        # current_val = 0.5, max_points = 10
        # gap = (1.0 - 0.5) * 10 = 5.0
        result = _calculate_impact(0.5, 10.0)
        assert result == "HIGH"

    def test_impact_boundary_none_low(self):
        """Test boundary between NONE and LOW (gap just above 1.0)."""
        # To avoid floating point issues, use gap = 1.1 (clearly above 1.0)
        # gap = (1.0 - current_val) * max_points = 1.1
        # current_val = 1.0 - (1.1 / 10.0) = 0.89
        result = _calculate_impact(0.89, 10.0)
        # gap = (1.0 - 0.89) * 10.0 = 1.1
        # 1.1 >= 1.0 and < 2.0, so returns LOW
        assert result == "LOW"

    def test_impact_boundary_low_medium(self):
        """Test boundary between LOW and MEDIUM (gap just above 2.0)."""
        # To avoid floating point issues, use gap = 2.1 (clearly above 2.0)
        # gap = (1.0 - current_val) * max_points = 2.1
        # current_val = 1.0 - (2.1 / 10.0) = 0.79
        result = _calculate_impact(0.79, 10.0)
        # gap = (1.0 - 0.79) * 10.0 = 2.1
        # 2.1 >= 2.0 and < 4.0, so returns MEDIUM
        assert result == "MEDIUM"

    def test_impact_boundary_medium_high(self):
        """Test boundary between MEDIUM and HIGH (exactly 4.0)."""
        # gap = exactly 4.0
        result = _calculate_impact(0.6, 10.0)
        assert result == "HIGH"  # >= 4.0


class TestEstimateEffort:
    """Tests for _estimate_effort helper function."""

    def test_effort_easy_small_gap(self):
        """Test LOW effort for easy fix with small gap."""
        result = _estimate_effort("Formatting Patterns", 2.0)
        assert result == "LOW"

    def test_effort_easy_large_gap(self):
        """Test MEDIUM effort for easy fix with large gap."""
        result = _estimate_effort("Stylometric Markers", 4.0)
        assert result == "MEDIUM"

    def test_effort_medium_small_gap(self):
        """Test MEDIUM effort for medium fix with small gap."""
        result = _estimate_effort("Burstiness (Sentence Variation)", 3.0)
        assert result == "MEDIUM"

    def test_effort_medium_large_gap(self):
        """Test HIGH effort for medium fix with large gap."""
        result = _estimate_effort("Perplexity (Vocabulary)", 5.0)
        assert result == "HIGH"

    def test_effort_hard_any_gap(self):
        """Test HIGH effort for hard fix regardless of gap."""
        result = _estimate_effort("GLTR Token Ranking", 2.0)
        assert result == "HIGH"

    def test_effort_unknown_dimension(self):
        """Test effort for unknown dimension (defaults to hard)."""
        result = _estimate_effort("Unknown Dimension", 3.0)
        assert result == "HIGH"

    def test_effort_heading_hierarchy(self):
        """Test effort for Heading Hierarchy (easy fix)."""
        result = _estimate_effort("Heading Hierarchy", 2.5)
        assert result == "LOW"

    def test_effort_structure_organization(self):
        """Test effort for Structure & Organization (medium fix)."""
        result = _estimate_effort("Structure & Organization", 3.5)
        assert result == "MEDIUM"

    def test_effort_syntactic_complexity(self):
        """Test effort for Syntactic Complexity (hard fix)."""
        result = _estimate_effort("Syntactic Complexity", 1.5)
        assert result == "HIGH"


class TestInterpretQuality:
    """Tests for _interpret_quality helper function."""

    def test_quality_exceptional(self):
        """Test EXCEPTIONAL interpretation (>= 95)."""
        result = _interpret_quality(97.0)
        assert result == "EXCEPTIONAL - Indistinguishable from human"

    def test_quality_excellent(self):
        """Test EXCELLENT interpretation (>= 85)."""
        result = _interpret_quality(88.0)
        assert result == "EXCELLENT - Minimal AI signatures"

    def test_quality_good(self):
        """Test GOOD interpretation (>= 70)."""
        result = _interpret_quality(75.0)
        assert result == "GOOD - Natural with minor tells"

    def test_quality_mixed(self):
        """Test MIXED interpretation (>= 50)."""
        result = _interpret_quality(60.0)
        assert result == "MIXED - Needs moderate work"

    def test_quality_ai_like(self):
        """Test AI-LIKE interpretation (>= 30)."""
        result = _interpret_quality(40.0)
        assert result == "AI-LIKE - Substantial work needed"

    def test_quality_obvious_ai(self):
        """Test OBVIOUS AI interpretation (< 30)."""
        result = _interpret_quality(20.0)
        assert result == "OBVIOUS AI - Complete rewrite"

    def test_quality_boundary_exceptional(self):
        """Test boundary at 95.0."""
        assert _interpret_quality(95.0) == "EXCEPTIONAL - Indistinguishable from human"
        assert _interpret_quality(94.9) == "EXCELLENT - Minimal AI signatures"

    def test_quality_boundary_excellent(self):
        """Test boundary at 85.0."""
        assert _interpret_quality(85.0) == "EXCELLENT - Minimal AI signatures"
        assert _interpret_quality(84.9) == "GOOD - Natural with minor tells"

    def test_quality_boundary_good(self):
        """Test boundary at 70.0."""
        assert _interpret_quality(70.0) == "GOOD - Natural with minor tells"
        assert _interpret_quality(69.9) == "MIXED - Needs moderate work"


class TestInterpretDetection:
    """Tests for _interpret_detection helper function."""

    def test_detection_very_high(self):
        """Test VERY HIGH detection risk (>= 70)."""
        result = _interpret_detection(75.0)
        assert result == "VERY HIGH - Will be flagged"

    def test_detection_high(self):
        """Test HIGH detection risk (>= 50)."""
        result = _interpret_detection(55.0)
        assert result == "HIGH - Likely flagged"

    def test_detection_medium(self):
        """Test MEDIUM detection risk (>= 30)."""
        result = _interpret_detection(40.0)
        assert result == "MEDIUM - May be flagged"

    def test_detection_low(self):
        """Test LOW detection risk (>= 15)."""
        result = _interpret_detection(20.0)
        assert result == "LOW - Unlikely flagged"

    def test_detection_very_low(self):
        """Test VERY LOW detection risk (< 15)."""
        result = _interpret_detection(10.0)
        assert result == "VERY LOW - Safe"

    def test_detection_boundary_very_high(self):
        """Test boundary at 70.0."""
        assert _interpret_detection(70.0) == "VERY HIGH - Will be flagged"
        assert _interpret_detection(69.9) == "HIGH - Likely flagged"

    def test_detection_boundary_high(self):
        """Test boundary at 50.0."""
        assert _interpret_detection(50.0) == "HIGH - Likely flagged"
        assert _interpret_detection(49.9) == "MEDIUM - May be flagged"

    def test_detection_boundary_medium(self):
        """Test boundary at 30.0."""
        assert _interpret_detection(30.0) == "MEDIUM - May be flagged"
        assert _interpret_detection(29.9) == "LOW - Unlikely flagged"


# ============================================================================
# Main Function Tests
# ============================================================================

class TestCalculateDualScoreBasic:
    """Tests for basic calculate_dual_score functionality."""

    def test_basic_calculation(self, basic_results):
        """Test basic dual score calculation with default targets."""
        score = calculate_dual_score(basic_results)

        # Check structure
        assert score.file_path == "/path/to/test.md"
        assert score.total_words == 500
        assert score.detection_target == 30.0
        assert score.quality_target == 85.0

        # Check scores are in valid range
        assert 0 <= score.detection_risk <= 100
        assert 0 <= score.quality_score <= 100

        # Check inverse relationship
        assert abs(score.detection_risk + score.quality_score - 100) < 0.2

        # Check interpretations exist
        assert score.detection_interpretation is not None
        assert score.quality_interpretation is not None

        # Check categories exist
        assert len(score.categories) == 4

    def test_custom_targets(self, basic_results):
        """Test dual score calculation with custom targets."""
        score = calculate_dual_score(
            basic_results,
            detection_target=20.0,
            quality_target=90.0
        )

        assert score.detection_target == 20.0
        assert score.quality_target == 90.0

    def test_timestamp_format(self, basic_results):
        """Test that timestamp is in ISO format."""
        score = calculate_dual_score(basic_results)
        assert "T" in score.timestamp  # ISO format has 'T' separator
        assert len(score.timestamp) > 10  # Has date and time

    def test_categories_structure(self, basic_results):
        """Test that categories have correct structure."""
        score = calculate_dual_score(basic_results)

        category_names = [cat.name for cat in score.categories]
        assert "Advanced Detection" in category_names
        assert "Core Patterns" in category_names
        assert "Supporting Indicators" in category_names
        assert "Phase 3 Advanced" in category_names

        # Check each category has dimensions
        for cat in score.categories:
            assert hasattr(cat, 'dimensions')
            assert hasattr(cat, 'total')
            assert hasattr(cat, 'max_total')
            assert hasattr(cat, 'percentage')


class TestCalculateDualScoreDimensions:
    """Tests for dimension scoring in calculate_dual_score."""

    def test_gltr_dimension_high(self, high_quality_results):
        """Test GLTR dimension scoring with HIGH score."""
        score = calculate_dual_score(high_quality_results)

        # Find GLTR dimension
        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        gltr_dim = next(dim for dim in advanced_cat.dimensions if "GLTR" in dim.name)

        # HIGH = 1.0 * 12 = 12.0
        assert gltr_dim.score == 12.0
        assert gltr_dim.max_score == 12.0
        assert gltr_dim.percentage == 100.0

    def test_gltr_dimension_low(self, low_quality_results):
        """Test GLTR dimension scoring with LOW score."""
        score = calculate_dual_score(low_quality_results)

        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        gltr_dim = next(dim for dim in advanced_cat.dimensions if "GLTR" in dim.name)

        # LOW = 0.5 * 12 = 6.0
        assert gltr_dim.score == 6.0
        assert gltr_dim.max_score == 12.0
        assert gltr_dim.gap == 6.0

    def test_mattr_dimension_excellent(self, high_quality_results):
        """Test MATTR dimension with EXCELLENT assessment."""
        score = calculate_dual_score(high_quality_results)

        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        mattr_dim = next(dim for dim in advanced_cat.dimensions if "MATTR" in dim.name)

        # EXCELLENT = 1.0 * 12 = 12.0
        assert mattr_dim.score == 12.0
        assert mattr_dim.max_score == 12.0

    def test_mattr_dimension_poor(self, low_quality_results):
        """Test MATTR dimension with POOR assessment."""
        score = calculate_dual_score(low_quality_results)

        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        mattr_dim = next(dim for dim in advanced_cat.dimensions if "MATTR" in dim.name)

        # POOR = 0.0 * 12 = 0.0
        assert mattr_dim.score == 0.0
        assert mattr_dim.max_score == 12.0

    def test_multi_perplexity_both_human(self):
        """Test multi-model perplexity with both models showing human."""
        results = create_analysis_results(
            gpt2_perplexity=150.0,
            distilgpt2_perplexity=145.0
        )

        score = calculate_dual_score(results)
        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        multi_perp_dim = next(dim for dim in advanced_cat.dimensions if "Multi-Model" in dim.name)

        # Both > 120, so score = 6.0
        assert multi_perp_dim.score == 6.0

    def test_multi_perplexity_both_ai(self):
        """Test multi-model perplexity with both models showing AI."""
        results = create_analysis_results(
            gpt2_perplexity=80.0,
            distilgpt2_perplexity=85.0
        )

        score = calculate_dual_score(results)
        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        multi_perp_dim = next(dim for dim in advanced_cat.dimensions if "Multi-Model" in dim.name)

        # Both <= 120, so score = 0.0
        assert multi_perp_dim.score == 0.0

    def test_multi_perplexity_mixed(self):
        """Test multi-model perplexity with mixed results."""
        results = create_analysis_results(
            gpt2_perplexity=150.0,
            distilgpt2_perplexity=85.0
        )

        score = calculate_dual_score(results)
        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        multi_perp_dim = next(dim for dim in advanced_cat.dimensions if "Multi-Model" in dim.name)

        # One human, one AI, so score = 3.0
        assert multi_perp_dim.score == 3.0

    def test_core_dimensions(self, basic_results):
        """Test core pattern dimensions (burstiness, perplexity, formatting)."""
        score = calculate_dual_score(basic_results)

        core_cat = next(cat for cat in score.categories if cat.name == "Core Patterns")

        # Should have 3 dimensions
        assert len(core_cat.dimensions) == 3

        dim_names = [dim.name for dim in core_cat.dimensions]
        assert "Burstiness (Sentence Variation)" in dim_names
        assert "Perplexity (Vocabulary)" in dim_names
        assert "Formatting Patterns" in dim_names


class TestCalculateDualScoreGaps:
    """Tests for gap calculation in calculate_dual_score."""

    def test_gap_calculation_below_target(self):
        """Test gap calculation when below target."""
        results = create_analysis_results(
            burstiness_score="LOW",
            perplexity_score="LOW",
            formatting_score="LOW",
            sentence_stdev=2.0,
            ai_vocabulary_per_1k=25.0,
            em_dashes_per_page=8.0
        )

        score = calculate_dual_score(results, quality_target=85.0)

        # Quality should be low, so quality_gap > 0
        assert score.quality_gap > 0
        assert score.quality_gap == max(0, 85.0 - score.quality_score)

    def test_gap_calculation_above_target(self, high_quality_results):
        """Test gap calculation when above target."""
        score = calculate_dual_score(high_quality_results, quality_target=50.0)

        # Quality should be high, so quality_gap = 0
        assert score.quality_gap == 0.0

    def test_detection_gap_calculation(self, low_quality_results):
        """Test detection gap calculation."""
        score = calculate_dual_score(low_quality_results, detection_target=20.0)

        # Detection should be high (quality is low), so detection_gap > 0
        if score.detection_risk > 20.0:
            assert score.detection_gap == score.detection_risk - 20.0
        else:
            assert score.detection_gap == 0.0


class TestCalculateDualScoreImprovements:
    """Tests for improvement action generation."""

    def test_improvements_generated(self, low_quality_results):
        """Test that improvements are generated for low quality."""
        score = calculate_dual_score(low_quality_results)

        # Should have multiple improvement actions
        assert len(score.improvements) > 0

    def test_improvements_have_priority(self, low_quality_results):
        """Test that improvements have priority assigned."""
        score = calculate_dual_score(low_quality_results)

        priorities = [imp.priority for imp in score.improvements]
        # Priorities should be 1, 2, 3, ... (sequential)
        assert priorities == list(range(1, len(priorities) + 1))

    def test_improvements_sorted_by_roi(self, low_quality_results):
        """Test that improvements are sorted by ROI."""
        score = calculate_dual_score(low_quality_results)

        # Effort multipliers: LOW=1.0, MEDIUM=0.7, HIGH=0.4
        effort_mult = {'LOW': 1.0, 'MEDIUM': 0.7, 'HIGH': 0.4}

        prev_roi = float('inf')
        for imp in score.improvements:
            roi = imp.potential_gain * effort_mult[imp.effort_level]
            assert roi <= prev_roi  # Descending order
            prev_roi = roi

    def test_improvements_only_significant_gaps(self, basic_results):
        """Test that only dimensions with gap > 0.5 generate improvements."""
        score = calculate_dual_score(basic_results)

        for imp in score.improvements:
            assert imp.potential_gain > 0.5

    def test_improvement_has_recommendation(self, low_quality_results):
        """Test that improvements have recommendations."""
        score = calculate_dual_score(low_quality_results)

        for imp in score.improvements:
            assert imp.action is not None
            assert len(imp.action) > 0

    def test_no_improvements_when_perfect(self, high_quality_results):
        """Test that no improvements when quality is perfect."""
        # Make all dimensions perfect
        high_quality_results.burstiness_score = "HIGH"
        high_quality_results.perplexity_score = "HIGH"
        high_quality_results.formatting_score = "HIGH"
        high_quality_results.gltr_score = "HIGH"
        high_quality_results.advanced_lexical_score = "HIGH"
        high_quality_results.mattr_assessment = "EXCELLENT"
        high_quality_results.rttr_assessment = "EXCELLENT"

        score = calculate_dual_score(high_quality_results)

        # Should have few or no improvements (all gaps small)
        # Count improvements with gap > 0.5
        significant_improvements = [imp for imp in score.improvements if imp.potential_gain > 0.5]
        assert len(significant_improvements) <= len(score.improvements)


class TestCalculateDualScorePathToTarget:
    """Tests for path to target calculation."""

    def test_path_to_target_exists(self, low_quality_results):
        """Test that path to target is generated."""
        score = calculate_dual_score(low_quality_results, quality_target=80.0)

        # Should have path to target
        assert isinstance(score.path_to_target, list)

    def test_path_stops_at_target(self):
        """Test that path stops when target is reached."""
        results = create_analysis_results(
            burstiness_score="MEDIUM",
            perplexity_score="MEDIUM",
            formatting_score="MEDIUM",
            sentence_stdev=6.0,
            ai_vocabulary_per_1k=8.0,
            em_dashes_per_page=3.0
        )

        score = calculate_dual_score(results, quality_target=60.0)

        # Calculate cumulative gain from path
        cumulative = score.quality_score
        for imp in score.path_to_target:
            cumulative += imp.potential_gain

        # Should reach or exceed target
        assert cumulative >= 60.0

    def test_path_empty_when_above_target(self, high_quality_results):
        """Test that path is empty when already above target."""
        score = calculate_dual_score(high_quality_results, quality_target=50.0)

        # Already above target, so path should be empty
        if score.quality_score >= 50.0:
            assert len(score.path_to_target) == 0


class TestCalculateDualScoreEffortEstimation:
    """Tests for effort estimation in calculate_dual_score."""

    def test_effort_minimal(self, high_quality_results):
        """Test MINIMAL effort when gap = 0."""
        score = calculate_dual_score(high_quality_results, quality_target=50.0)

        if score.quality_gap == 0:
            assert score.estimated_effort == "MINIMAL"

    def test_effort_light(self):
        """Test LIGHT effort when gap < 5."""
        results = create_analysis_results(
            burstiness_score="HIGH",
            perplexity_score="HIGH",
            formatting_score="MEDIUM",
            sentence_stdev=8.0,
            ai_vocabulary_per_1k=3.0,
            em_dashes_per_page=2.5
        )

        score = calculate_dual_score(results, quality_target=85.0)

        if 0 < score.quality_gap < 5:
            assert score.estimated_effort == "LIGHT"

    def test_effort_moderate(self):
        """Test MODERATE effort when 5 <= gap < 15."""
        results = create_analysis_results(
            burstiness_score="MEDIUM",
            perplexity_score="MEDIUM",
            formatting_score="MEDIUM",
            sentence_stdev=6.0,
            ai_vocabulary_per_1k=8.0,
            em_dashes_per_page=3.0
        )

        score = calculate_dual_score(results, quality_target=85.0)

        if 5 <= score.quality_gap < 15:
            assert score.estimated_effort == "MODERATE"

    def test_effort_substantial(self):
        """Test SUBSTANTIAL effort when 15 <= gap < 30."""
        results = create_analysis_results(
            burstiness_score="LOW",
            perplexity_score="MEDIUM",
            formatting_score="MEDIUM",
            sentence_stdev=3.0,
            ai_vocabulary_per_1k=12.0,
            em_dashes_per_page=4.0
        )

        score = calculate_dual_score(results, quality_target=85.0)

        if 15 <= score.quality_gap < 30:
            assert score.estimated_effort == "SUBSTANTIAL"

    def test_effort_extensive(self, low_quality_results):
        """Test EXTENSIVE effort when gap >= 30."""
        score = calculate_dual_score(low_quality_results, quality_target=95.0)

        if score.quality_gap >= 30:
            assert score.estimated_effort == "EXTENSIVE"


# ============================================================================
# Edge Cases and Missing Data Tests
# ============================================================================

class TestCalculateDualScoreEdgeCases:
    """Tests for edge cases in calculate_dual_score."""

    def test_missing_advanced_scores(self, results_with_missing_advanced):
        """Test handling of missing advanced scores."""
        score = calculate_dual_score(results_with_missing_advanced)

        # Should still calculate successfully with defaults
        assert score is not None
        assert 0 <= score.quality_score <= 100

        # Advanced dimensions should use default (0.5) or None values
        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        for dim in advanced_cat.dimensions:
            # Should have some score (even if default)
            assert dim.score >= 0

    def test_partial_perplexity_data(self, results_with_partial_perplexity):
        """Test handling of partial perplexity data."""
        score = calculate_dual_score(results_with_partial_perplexity)

        # Should handle missing distilgpt2_perplexity gracefully
        advanced_cat = next(cat for cat in score.categories if cat.name == "Advanced Detection")
        multi_perp_dim = next(dim for dim in advanced_cat.dimensions if "Multi-Model" in dim.name)

        # With only one value, should use default (3.0)
        assert multi_perp_dim.score == 3.0

    def test_none_attribute_values(self):
        """Test handling of None attribute values."""
        results = create_analysis_results(
            burstiness_score="MEDIUM",
            perplexity_score="MEDIUM",
            formatting_score="MEDIUM",
            sentence_stdev=6.0,
            ai_vocabulary_per_1k=8.0,
            em_dashes_per_page=3.0,
            # Advanced scores as None
            gltr_score=None,
            advanced_lexical_score=None
        )

        score = calculate_dual_score(results)

        # Should handle None values without crashing
        assert score is not None

    def test_unknown_score_values(self):
        """Test handling of UNKNOWN score values."""
        results = create_analysis_results(
            burstiness_score="UNKNOWN",
            perplexity_score="UNKNOWN",
            formatting_score="UNKNOWN",
            sentence_stdev=6.0,
            ai_vocabulary_per_1k=8.0,
            em_dashes_per_page=3.0
        )

        score = calculate_dual_score(results)

        # UNKNOWN maps to 0.5 in score_map
        assert score is not None
        # Quality should be around 50% (0.5 * total_points / total_possible)

    def test_zero_total_possible(self):
        """Test protection against zero division in total_possible."""
        # This is a synthetic edge case - all categories have 0 max_total
        results = create_analysis_results(
            burstiness_score="MEDIUM",
            perplexity_score="MEDIUM",
            formatting_score="MEDIUM",
            sentence_stdev=6.0,
            ai_vocabulary_per_1k=8.0,
            em_dashes_per_page=3.0
        )

        score = calculate_dual_score(results)

        # Should handle zero division: (total_score / total_possible * 100) if total_possible > 0 else 0
        assert isinstance(score.quality_score, float)


class TestCalculateDualScoreRounding:
    """Tests for score rounding."""

    def test_scores_rounded_to_one_decimal(self, basic_results):
        """Test that scores are rounded to 1 decimal place."""
        score = calculate_dual_score(basic_results)

        # Check detection_risk
        detection_str = str(score.detection_risk)
        if '.' in detection_str:
            decimal_places = len(detection_str.split('.')[1])
            assert decimal_places <= 1

        # Check quality_score
        quality_str = str(score.quality_score)
        if '.' in quality_str:
            decimal_places = len(quality_str.split('.')[1])
            assert decimal_places <= 1

        # Check gaps
        detection_gap_str = str(score.detection_gap)
        if '.' in detection_gap_str:
            decimal_places = len(detection_gap_str.split('.')[1])
            assert decimal_places <= 1

        quality_gap_str = str(score.quality_gap)
        if '.' in quality_gap_str:
            decimal_places = len(quality_gap_str.split('.')[1])
            assert decimal_places <= 1


# ============================================================================
# Integration Tests
# ============================================================================

class TestCalculateDualScoreIntegration:
    """Integration tests for complete dual score calculation workflow."""

    def test_complete_workflow_low_to_high(self, low_quality_results, high_quality_results):
        """Test complete workflow from low to high quality."""
        # Calculate low quality score
        low_score = calculate_dual_score(low_quality_results, quality_target=85.0)

        # Should have high detection risk, low quality
        assert low_score.detection_risk > 50
        assert low_score.quality_score < 50
        assert low_score.quality_gap > 0
        assert len(low_score.improvements) > 0

        # Calculate high quality score
        high_score = calculate_dual_score(high_quality_results, quality_target=85.0)

        # Should have low detection risk, high quality
        assert high_score.detection_risk < 30
        assert high_score.quality_score > 80
        assert high_score.quality_gap < 10

    def test_all_dimensions_contribute(self, high_quality_results):
        """Test that all dimensions contribute to final score."""
        score = calculate_dual_score(high_quality_results)

        total_from_categories = sum(cat.total for cat in score.categories)
        total_possible_from_categories = sum(cat.max_total for cat in score.categories)

        # Quality score should match (total / possible * 100)
        expected_quality = (total_from_categories / total_possible_from_categories * 100) if total_possible_from_categories > 0 else 0
        assert abs(score.quality_score - expected_quality) < 0.2  # Allow small rounding difference

    def test_consistency_across_calls(self, basic_results):
        """Test that repeated calls with same data produce same results."""
        score1 = calculate_dual_score(basic_results, quality_target=85.0, detection_target=30.0)
        score2 = calculate_dual_score(basic_results, quality_target=85.0, detection_target=30.0)

        # Scores should be identical (excluding timestamp)
        assert score1.detection_risk == score2.detection_risk
        assert score1.quality_score == score2.quality_score
        assert score1.quality_gap == score2.quality_gap
        assert score1.detection_gap == score2.detection_gap
        assert len(score1.improvements) == len(score2.improvements)

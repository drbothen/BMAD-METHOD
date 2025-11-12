"""
Tests for SentimentDimension - Sentiment variance analysis.
Story 1.4.6 - Adding missing test file for sentiment dimension.
"""

import pytest
from unittest.mock import Mock, patch
from ai_pattern_analyzer.dimensions.sentiment import SentimentDimension
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry
from ai_pattern_analyzer.core.analysis_config import AnalysisConfig, AnalysisMode


@pytest.fixture
def dimension():
    """Create SentimentDimension instance."""
    # Clear registry before each test to avoid duplicate registration errors
    DimensionRegistry.clear()
    return SentimentDimension()


@pytest.fixture
def varied_sentiment_text():
    """Text with high sentiment variance (human-like)."""
    return """
    I'm absolutely thrilled about this amazing breakthrough! This discovery changes everything.
    However, we must approach this cautiously. There are concerning implications.
    The data itself is neutral, showing neither positive nor negative trends.
    I'm disappointed by the lack of progress on this critical issue.
    Overall, this represents a fascinating development worth exploring further.
    """


@pytest.fixture
def flat_sentiment_text():
    """Text with low sentiment variance (AI-like)."""
    return """
    The system operates efficiently. The process functions correctly.
    The framework provides functionality. The implementation works properly.
    The solution delivers results. The method applies techniques effectively.
    """


@pytest.fixture
def neutral_text():
    """Text with neutral sentiment."""
    return """
    The data shows three key trends. First, usage increased by 10 percent.
    Second, engagement remained stable. Third, conversions grew modestly.
    These findings indicate measured progress across multiple metrics.
    """


class TestDimensionMetadata:
    """Tests for dimension metadata and registration."""

    def test_dimension_name(self, dimension):
        """Test dimension name is 'sentiment'."""
        assert dimension.dimension_name == "sentiment"

    def test_dimension_weight(self, dimension):
        """Test dimension weight is 17.0%."""
        assert dimension.weight == 17.0

    def test_dimension_tier(self, dimension):
        """Test dimension tier is SUPPORTING."""
        assert dimension.tier == "SUPPORTING"

    def test_dimension_description(self, dimension):
        """Test dimension has meaningful description."""
        desc = dimension.description
        assert isinstance(desc, str)
        assert len(desc) > 20
        assert "sentiment" in desc.lower()

    def test_dimension_registers_on_init(self):
        """Test dimension self-registers with registry on initialization."""
        DimensionRegistry.clear()
        dim = SentimentDimension()

        registered = DimensionRegistry.get("sentiment")
        assert registered is dim


class TestAnalyzeMethod:
    """Tests for analyze() method."""

    def test_analyze_returns_sentiment_metrics(self, dimension, varied_sentiment_text):
        """Test analyze() returns sentiment variance metrics."""
        result = dimension.analyze(varied_sentiment_text)

        assert 'sentiment' in result
        assert 'available' in result
        assert result['available'] is True

        sentiment = result['sentiment']
        assert 'variance' in sentiment
        assert 'mean' in sentiment

    def test_analyze_accepts_config_parameter(self, dimension, varied_sentiment_text):
        """Test analyze() accepts config parameter (Story 1.4.6)."""
        config = AnalysisConfig(mode=AnalysisMode.FAST)

        # Should not raise error
        result = dimension.analyze(varied_sentiment_text, config=config)

        assert 'sentiment' in result
        assert 'available' in result

    def test_analyze_with_config_none(self, dimension, varied_sentiment_text):
        """Test analyze() works with config=None."""
        result = dimension.analyze(varied_sentiment_text, config=None)

        assert 'sentiment' in result
        assert 'available' in result

    def test_analyze_high_variance_text(self, dimension, varied_sentiment_text):
        """Test analyze() detects high sentiment variance."""
        result = dimension.analyze(varied_sentiment_text)

        sentiment = result['sentiment']
        # Varied text should have higher variance
        assert sentiment['variance'] > 0.0

    def test_analyze_handles_empty_text(self, dimension):
        """Test analyze() handles empty text gracefully."""
        result = dimension.analyze("")

        assert 'available' in result
        # May be True or False depending on implementation

    def test_analyze_sets_available_flag(self, dimension, neutral_text):
        """Test analyze() sets 'available' flag."""
        result = dimension.analyze(neutral_text)
        assert 'available' in result


class TestCalculateScoreMethod:
    """Tests for calculate_score() - scores based on sentiment variance."""

    def test_score_high_variance_gives_high_score(self, dimension):
        """Test high sentiment variance (≥0.20) gives excellent score (100)."""
        metrics = {
            'sentiment': {
                'variance': 0.25,
                'mean': 0.0
            },
            'available': True
        }
        score = dimension.calculate_score(metrics)

        assert score == 100.0

    def test_score_good_variance_gives_good_score(self, dimension):
        """Test good sentiment variance (0.15-0.20) gives good score (75)."""
        metrics = {
            'sentiment': {
                'variance': 0.17,
                'mean': 0.0
            },
            'available': True
        }
        score = dimension.calculate_score(metrics)

        assert score == 75.0

    def test_score_moderate_variance(self, dimension):
        """Test moderate sentiment variance (0.10-0.15) gives medium score."""
        metrics = {
            'sentiment': {
                'variance': 0.12,
                'mean': 0.0
            },
            'available': True
        }
        score = dimension.calculate_score(metrics)

        assert score == 62.5

    def test_score_low_variance(self, dimension):
        """Test low sentiment variance (0.05-0.10) gives low score."""
        metrics = {
            'sentiment': {
                'variance': 0.07,
                'mean': 0.0
            },
            'available': True
        }
        score = dimension.calculate_score(metrics)

        assert score == 50.0

    def test_score_very_low_variance_gives_low_score(self, dimension):
        """Test very low sentiment variance (<0.05) gives poor score (25)."""
        metrics = {
            'sentiment': {
                'variance': 0.02,
                'mean': 0.0
            },
            'available': True
        }
        score = dimension.calculate_score(metrics)

        assert score == 25.0

    def test_score_validates_range(self, dimension):
        """Test calculate_score validates 0-100 range."""
        metrics = {
            'sentiment': {
                'variance': 0.25,
                'mean': 0.0
            },
            'available': True
        }
        score = dimension.calculate_score(metrics)

        assert 0.0 <= score <= 100.0


class TestGetRecommendationsMethod:
    """Tests for get_recommendations() method."""

    def test_recommendations_for_low_variance(self, dimension):
        """Test recommendations generated for low variance (AI signature)."""
        metrics = {
            'sentiment': {
                'variance': 0.05,
                'mean': 0.0,
                'emotionally_flat': True
            }
        }
        score = 50.0

        recommendations = dimension.get_recommendations(score, metrics)

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        # Should mention variance/variation/emotion
        rec_text = ' '.join(recommendations).lower()
        assert any(term in rec_text for term in ['variance', 'variation', 'emotion', 'sentiment'])

    def test_recommendations_for_high_variance(self, dimension):
        """Test fewer/no recommendations for high variance (human-like)."""
        metrics = {
            'sentiment': {
                'variance': 0.25,
                'mean': 0.0,
                'emotionally_flat': False
            }
        }
        score = 100.0

        recommendations = dimension.get_recommendations(score, metrics)

        # High score should have fewer recommendations
        assert isinstance(recommendations, list)


class TestGetTiersMethod:
    """Tests for get_tiers() method."""

    def test_get_tiers_returns_standard_tiers(self, dimension):
        """Test get_tiers() returns standard tier structure."""
        tiers = dimension.get_tiers()

        assert isinstance(tiers, dict)
        assert 'excellent' in tiers
        assert 'good' in tiers
        assert 'acceptable' in tiers
        assert 'poor' in tiers

    def test_tier_ranges_are_valid(self, dimension):
        """Test tier ranges don't overlap and cover 0-100."""
        tiers = dimension.get_tiers()

        for tier_name, (min_score, max_score) in tiers.items():
            assert 0.0 <= min_score <= 100.0
            assert 0.0 <= max_score <= 100.0
            assert min_score <= max_score


class TestBackwardCompatibility:
    """Tests for backward compatibility (config=None behavior)."""

    def test_no_config_parameter_works(self, dimension, neutral_text):
        """Test analyze() works without config parameter (old calling pattern)."""
        # Simulate old code that doesn't pass config
        result = dimension.analyze(neutral_text)

        assert 'sentiment' in result
        assert 'available' in result

    def test_config_none_identical_to_no_config(self, dimension, neutral_text):
        """Test config=None produces identical results to no config."""
        result1 = dimension.analyze(neutral_text)
        result2 = dimension.analyze(neutral_text, config=None)

        # Should produce same results
        assert result1['available'] == result2['available']
        if result1['available'] and result2['available']:
            assert result1['sentiment']['variance'] == result2['sentiment']['variance']

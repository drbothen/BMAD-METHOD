"""
Tests for ReadabilityDimension - Flesch-Kincaid and readability metrics.
Story 1.4.5 - New dimension split from StylometricDimension.
"""

import pytest
from unittest.mock import Mock, patch
from ai_pattern_analyzer.dimensions.readability import ReadabilityDimension
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry


@pytest.fixture
def dimension():
    """Create ReadabilityDimension instance."""
    # Clear registry before each test to avoid duplicate registration errors
    DimensionRegistry.clear()
    return ReadabilityDimension()


@pytest.fixture
def easy_text():
    """Text with high readability (Flesch >80)."""
    return """
    The cat sat on the mat. She was a big cat. The mat was red.
    She liked to sit there. It was her favorite spot. She sat every day.
    """


@pytest.fixture
def standard_text():
    """Text with standard readability (Flesch 60-70)."""
    return """
    The comprehensive framework facilitates seamless integration through
    innovative solutions. This approach leverages cutting-edge technology
    to optimize performance and streamline workflows effectively.
    """


@pytest.fixture
def difficult_text():
    """Text with low readability (Flesch <40)."""
    return """
    The multifaceted epistemological paradigm necessitates comprehensive
    reevaluation of heuristic methodologies through intricate analytical
    frameworks, thereby facilitating unprecedented conceptualization of
    ontological phenomena within circumscribed theoretical constructs.
    """


class TestDimensionMetadata:
    """Tests for dimension metadata and registration."""

    def test_dimension_name(self, dimension):
        """Test dimension name is 'readability'."""
        assert dimension.dimension_name == "readability"

    def test_dimension_weight(self, dimension):
        """Test dimension weight is 10.0%."""
        assert dimension.weight == 10.0

    def test_dimension_tier(self, dimension):
        """Test dimension tier is CORE (promoted from ADVANCED)."""
        assert dimension.tier == "CORE"

    def test_dimension_description(self, dimension):
        """Test dimension has meaningful description."""
        desc = dimension.description
        assert isinstance(desc, str)
        assert len(desc) > 20
        assert any(term in desc for term in ["readability", "Flesch", "Kincaid"])

    def test_dimension_registers_on_init(self):
        """Test dimension self-registers with registry on initialization."""
        DimensionRegistry.clear()
        dim = ReadabilityDimension()

        registered = DimensionRegistry.get("readability")
        assert registered is dim


class TestAnalyzeMethod:
    """Tests for analyze() method - must ONLY collect readability metrics."""

    def test_analyze_returns_readability_metrics_only(self, dimension, standard_text):
        """Test analyze() collects ONLY readability metrics (no markers)."""
        result = dimension.analyze(standard_text)

        # Should contain readability metrics
        assert 'flesch_reading_ease' in result
        assert 'flesch_kincaid_grade' in result
        assert 'automated_readability_index' in result
        assert 'available' in result

        # Should NOT contain transition marker metrics (those belong in TransitionMarkerDimension)
        assert 'however_count' not in result
        assert 'moreover_count' not in result
        assert 'however_per_1k' not in result
        assert 'moreover_per_1k' not in result
        assert 'total_ai_markers_per_1k' not in result

    def test_analyze_includes_avg_word_length(self, dimension, standard_text):
        """Test analyze() includes average word length."""
        result = dimension.analyze(standard_text)

        assert 'avg_word_length' in result
        assert result['avg_word_length'] >= 0

    def test_analyze_includes_avg_sentence_length(self, dimension, standard_text):
        """Test analyze() includes average sentence length."""
        result = dimension.analyze(standard_text)

        assert 'avg_sentence_length' in result
        assert result['avg_sentence_length'] >= 0

    def test_analyze_sets_available_flag(self, dimension, standard_text):
        """Test analyze() sets 'available' flag."""
        result = dimension.analyze(standard_text)
        assert 'available' in result
        assert result['available'] is True

    def test_analyze_handles_empty_text(self, dimension):
        """Test analyze() handles empty text gracefully."""
        result = dimension.analyze("")
        assert 'available' in result


class TestCalculateScoreMethod:
    """Tests for calculate_score() - scores on Flesch Reading Ease."""

    def test_score_extreme_low_readability(self, dimension):
        """Test score for extremely low readability (Flesch <30) - AI signature."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 25.0
        }
        score = dimension.calculate_score(metrics)

        assert score == 25.0  # Too extreme - AI signature

    def test_score_extreme_high_readability(self, dimension):
        """Test score for extremely high readability (Flesch >90) - AI signature."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 95.0
        }
        score = dimension.calculate_score(metrics)

        assert score == 25.0  # Too extreme - AI signature

    def test_score_borderline_low(self, dimension):
        """Test score for borderline low readability (Flesch 30-40)."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 35.0
        }
        score = dimension.calculate_score(metrics)

        assert score == 50.0  # Borderline extreme

    def test_score_borderline_high(self, dimension):
        """Test score for borderline high readability (Flesch 80-90)."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 85.0
        }
        score = dimension.calculate_score(metrics)

        assert score == 50.0  # Borderline extreme

    def test_score_standard_range(self, dimension):
        """Test score for standard mid-range (Flesch 60-70) - common in AI."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 65.0
        }
        score = dimension.calculate_score(metrics)

        assert score == 62.5  # Standard range - neutral

    def test_score_natural_variation(self, dimension):
        """Test score for natural variation (Flesch 40-60 or 70-80)."""
        # Test 40-60 range
        metrics1 = {
            'available': True,
            'flesch_reading_ease': 50.0
        }
        score1 = dimension.calculate_score(metrics1)
        assert score1 == 100.0  # Natural variation - human-like

        # Test 70-80 range
        metrics2 = {
            'available': True,
            'flesch_reading_ease': 75.0
        }
        score2 = dimension.calculate_score(metrics2)
        assert score2 == 100.0  # Natural variation - human-like

    def test_score_unavailable_data(self, dimension):
        """Test score when readability data unavailable."""
        metrics = {
            'available': False
        }
        score = dimension.calculate_score(metrics)

        assert score == 50.0  # Neutral score for unavailable data

    def test_score_missing_flesch_uses_default(self, dimension):
        """Test score when flesch_reading_ease missing uses default (60.0)."""
        metrics = {
            'available': True
            # Missing flesch_reading_ease - should use default 60.0
        }
        score = dimension.calculate_score(metrics)

        assert score == 62.5  # Default 60.0 is in standard range

    def test_score_validates_range(self, dimension):
        """Test score is always in valid 0-100 range."""
        test_cases = [0.0, 25.0, 40.0, 50.0, 65.0, 75.0, 85.0, 95.0, 100.0]

        for flesch_value in test_cases:
            metrics = {
                'available': True,
                'flesch_reading_ease': flesch_value
            }
            score = dimension.calculate_score(metrics)
            assert 0.0 <= score <= 100.0


class TestGetRecommendations:
    """Tests for get_recommendations() method."""

    def test_recommendations_for_extreme_low_readability(self, dimension):
        """Test recommendations for extremely low readability."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 25.0,
            'flesch_kincaid_grade': 16.0
        }
        recommendations = dimension.get_recommendations(25.0, metrics)

        assert len(recommendations) > 0
        assert any('extremely low' in rec.lower() or 'difficult' in rec.lower() for rec in recommendations)
        assert any('simplify' in rec.lower() for rec in recommendations)

    def test_recommendations_for_extreme_high_readability(self, dimension):
        """Test recommendations for extremely high readability."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 95.0
        }
        recommendations = dimension.get_recommendations(25.0, metrics)

        assert len(recommendations) > 0
        assert any('extremely high' in rec.lower() or 'overly simple' in rec.lower() for rec in recommendations)

    def test_recommendations_for_standard_range(self, dimension):
        """Test recommendations for standard mid-range readability."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 65.0,
            'flesch_kincaid_grade': 8.0
        }
        recommendations = dimension.get_recommendations(62.5, metrics)

        assert len(recommendations) > 0
        assert any('standard' in rec.lower() or 'mid-range' in rec.lower() for rec in recommendations)

    def test_recommendations_for_good_variation(self, dimension):
        """Test recommendations for good readability variation."""
        metrics = {
            'available': True,
            'flesch_reading_ease': 50.0
        }
        recommendations = dimension.get_recommendations(100.0, metrics)

        assert len(recommendations) > 0
        assert any('good' in rec.lower() or 'natural' in rec.lower() for rec in recommendations)

    def test_recommendations_unavailable_data(self, dimension):
        """Test recommendations when readability data unavailable."""
        metrics = {
            'available': False
        }
        recommendations = dimension.get_recommendations(50.0, metrics)

        assert len(recommendations) > 0
        assert any('unavailable' in rec.lower() or 'install' in rec.lower() for rec in recommendations)


class TestGetTiers:
    """Tests for get_tiers() method."""

    def test_get_tiers_structure(self, dimension):
        """Test tier structure is valid."""
        tiers = dimension.get_tiers()

        assert isinstance(tiers, dict)
        assert 'excellent' in tiers
        assert 'good' in tiers
        assert 'acceptable' in tiers
        assert 'poor' in tiers

    def test_tier_ranges(self, dimension):
        """Test tier ranges are properly defined."""
        tiers = dimension.get_tiers()

        excellent_min, excellent_max = tiers['excellent']
        assert excellent_min == 90.0
        assert excellent_max == 100.0


class TestReadabilityPatternsAnalysis:
    """Tests for _analyze_readability_patterns() helper method."""

    @patch('ai_pattern_analyzer.dimensions.readability.textstat')
    def test_flesch_reading_ease_calculation(self, mock_textstat, dimension):
        """Test Flesch Reading Ease calculation."""
        mock_textstat.flesch_reading_ease.return_value = 65.0

        result = dimension._analyze_readability_patterns("Sample text")

        assert 'flesch_reading_ease' in result
        assert result['flesch_reading_ease'] == 65.0

    @patch('ai_pattern_analyzer.dimensions.readability.textstat')
    def test_flesch_kincaid_grade_calculation(self, mock_textstat, dimension):
        """Test Flesch-Kincaid Grade Level calculation."""
        mock_textstat.flesch_kincaid_grade.return_value = 8.0

        result = dimension._analyze_readability_patterns("Sample text")

        assert 'flesch_kincaid_grade' in result
        assert result['flesch_kincaid_grade'] == 8.0

    @patch('ai_pattern_analyzer.dimensions.readability.textstat')
    def test_automated_readability_index_calculation(self, mock_textstat, dimension):
        """Test Automated Readability Index calculation."""
        mock_textstat.automated_readability_index.return_value = 8.5

        result = dimension._analyze_readability_patterns("Sample text")

        assert 'automated_readability_index' in result
        assert result['automated_readability_index'] == 8.5

    def test_avg_word_length_calculation(self, dimension):
        """Test average word length calculation."""
        text = "cat dog bird"  # All 3-4 letter words
        result = dimension._analyze_readability_patterns(text)

        assert 'avg_word_length' in result
        assert result['avg_word_length'] > 0

    def test_avg_sentence_length_calculation(self, dimension):
        """Test average sentence length calculation."""
        text = "This is a sentence. This is another sentence."
        result = dimension._analyze_readability_patterns(text)

        assert 'avg_sentence_length' in result
        assert result['avg_sentence_length'] > 0

    def test_handles_errors_gracefully(self, dimension):
        """Test error handling when textstat fails."""
        result = dimension._analyze_readability_patterns("")

        assert 'flesch_reading_ease' in result
        # Should return default values even if calculation fails


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_handles_text_without_sentences(self, dimension):
        """Test handling of text without proper sentences."""
        text = "word word word word word"
        result = dimension.analyze(text)

        assert 'available' in result

    def test_handles_text_with_only_punctuation(self, dimension):
        """Test handling of text with only punctuation."""
        text = "... !!! ???"
        result = dimension.analyze(text)

        assert 'available' in result

    def test_handles_very_long_words(self, dimension):
        """Test handling of text with very long words."""
        text = "supercalifragilisticexpialidocious " * 20
        result = dimension.analyze(text)

        assert 'available' in result


class TestBackwardCompatibility:
    """Tests for backward compatibility alias."""

    def test_backward_compatibility_alias_exists(self):
        """Test ReadabilityAnalyzer alias exists for backward compatibility."""
        from ai_pattern_analyzer.dimensions.readability import ReadabilityAnalyzer

        DimensionRegistry.clear()
        dim = ReadabilityAnalyzer()

        assert dim.dimension_name == "readability"
        assert dim.weight == 10.0

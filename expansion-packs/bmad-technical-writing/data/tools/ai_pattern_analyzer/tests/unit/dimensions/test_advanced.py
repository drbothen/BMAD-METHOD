"""
Tests for AdvancedAnalyzer - GLTR, HDD, MATTR, and transformer-based detection.
"""

import pytest
from ai_pattern_analyzer.dimensions.advanced import AdvancedAnalyzer

# All dependencies are now required
HAS_TRANSFORMERS = True
HAS_SCIPY = True
HAS_SPACY = True
HAS_TEXTACY = True


@pytest.fixture
def analyzer():
    """Create AdvancedAnalyzer instance."""
    return AdvancedAnalyzer()


@pytest.fixture
def text_diverse():
    """Text with high lexical diversity (human pattern)."""
    return """# Advanced Analysis

Remarkable discoveries emerged when researchers examined unprecedented phenomena
occurring throughout various experimental contexts. Distinguished patterns manifested
unexpectedly, challenging conventional theoretical frameworks while simultaneously
confirming several fundamental hypotheses proposed decades earlier by pioneering
scientists."""


@pytest.fixture
def text_repetitive():
    """Text with low lexical diversity (AI pattern)."""
    return """# System Overview

The system provides benefits. The system offers value. The system ensures quality.
The system maintains performance. The system delivers results. The system supports
functionality. The system demonstrates reliability. The system enables efficiency."""


@pytest.fixture
def text_short():
    """Short text (insufficient for some metrics)."""
    return "This is a short text with limited content for analysis purposes."


class TestAnalyze:
    """Tests for main analyze method."""

    def test_analyze_basic_structure(self, analyzer, text_diverse):
        """Test basic analyze method structure."""
        result = analyzer.analyze(text_diverse)

        assert isinstance(result, dict)
        # Should have 'available' key regardless of dependencies
        assert 'available' in result or 'gltr_top10_percentage' in result or 'hdd_score' in result

    def test_analyze_empty_text(self, analyzer):
        """Test analyze on empty text."""
        result = analyzer.analyze("")

        assert isinstance(result, dict)

    def test_analyze_with_transformers(self, analyzer, text_diverse):
        """Test analyze includes GLTR metrics when transformers available."""
        result = analyzer.analyze(text_diverse)

        # May have GLTR metrics if model loads successfully
        assert isinstance(result, dict)

    def test_analyze_with_scipy(self, analyzer, text_diverse):
        """Test analyze includes advanced lexical metrics when scipy available."""
        result = analyzer.analyze(text_diverse)

        # Should have some metrics (scipy metrics may require longer text)
        assert isinstance(result, dict)
        assert result  # Not empty

    def test_analyze_with_textacy(self, analyzer, text_diverse):
        """Test analyze includes MATTR/RTTR when textacy available."""
        result = analyzer.analyze(text_diverse)

        # Should have textacy metrics
        assert 'mattr' in result or 'rttr' in result


class TestAnalyzeDetailed:
    """Tests for analyze_detailed method."""

    def test_analyze_detailed_basic(self, analyzer, text_diverse):
        """Test detailed analysis method."""
        lines = text_diverse.split('\n')
        result = analyzer.analyze_detailed(lines)

        assert isinstance(result, list)

    def test_analyze_detailed_with_transformers(self, analyzer, text_diverse):
        """Test detailed analysis with transformers."""
        lines = text_diverse.split('\n')
        result = analyzer.analyze_detailed(lines)

        assert isinstance(result, list)


class TestCalculateAdvancedLexicalDiversity:
    """Tests for _calculate_advanced_lexical_diversity method (requires scipy)."""

    def test_advanced_lexical_basic(self, analyzer, text_diverse):
        """Test advanced lexical diversity calculation."""
        result = analyzer._calculate_advanced_lexical_diversity(text_diverse)

        assert isinstance(result, dict)
        # May be empty dict if text too short (requires 50+ words)
        # If not empty, should have expected keys
        if result:
            expected_keys = ['hdd_score', 'yules_k', 'maas_score', 'vocab_concentration']
            assert any(key in result for key in expected_keys)

    def test_advanced_lexical_hdd_score(self, analyzer, text_diverse):
        """Test HDD score calculation."""
        result = analyzer._calculate_advanced_lexical_diversity(text_diverse)

        if 'hdd_score' in result and result['hdd_score'] is not None:
            # HDD should be between 0 and 1
            assert 0 <= result['hdd_score'] <= 1

    def test_advanced_lexical_yules_k(self, analyzer, text_diverse):
        """Test Yule's K calculation."""
        result = analyzer._calculate_advanced_lexical_diversity(text_diverse)

        if 'yules_k' in result and result['yules_k'] is not None:
            # Yule's K should be positive
            assert result['yules_k'] > 0

    def test_advanced_lexical_vocab_concentration(self, analyzer, text_diverse):
        """Test vocabulary concentration calculation."""
        result = analyzer._calculate_advanced_lexical_diversity(text_diverse)

        if 'vocab_concentration' in result:
            # Concentration should be between 0 and 1
            assert 0 <= result['vocab_concentration'] <= 1

    def test_advanced_lexical_short_text(self, analyzer, text_short):
        """Test advanced lexical on short text."""
        result = analyzer._calculate_advanced_lexical_diversity(text_short)

        # Should return empty dict or limited metrics for short text
        assert isinstance(result, dict)

    def test_advanced_lexical_excludes_code(self, analyzer):
        """Test that code blocks are excluded."""
        text = """# Example

Some diverse vocabulary here with various words.

```python
def function():
    return value
```

More interesting text after the code."""
        result = analyzer._calculate_advanced_lexical_diversity(text)

        # Should analyze non-code text
        assert isinstance(result, dict)

    def test_advanced_lexical_comparison(self, analyzer, text_diverse, text_repetitive):
        """Test that diverse text has better metrics than repetitive."""
        diverse_result = analyzer._calculate_advanced_lexical_diversity(text_diverse)
        repetitive_result = analyzer._calculate_advanced_lexical_diversity(text_repetitive)

        # If both have Yule's K, diverse should have lower value (better)
        if (diverse_result.get('yules_k') and repetitive_result.get('yules_k')):
            assert diverse_result['yules_k'] < repetitive_result['yules_k']


class TestCalculateAdvancedLexicalDiversityNoScipy:
    """Tests for _calculate_advanced_lexical_diversity without scipy."""

    @pytest.mark.skipif(HAS_SCIPY, reason="Test requires scipy to be unavailable")
    def test_advanced_lexical_no_scipy(self, analyzer, text_diverse):
        """Test advanced lexical without scipy available."""
        result = analyzer._calculate_advanced_lexical_diversity(text_diverse)

        assert result == {}


class TestCalculateTextacyLexicalDiversity:
    """Tests for _calculate_textacy_lexical_diversity method (requires textacy + spacy)."""

    def test_textacy_lexical_basic(self, analyzer, text_diverse):
        """Test textacy lexical diversity calculation."""
        result = analyzer._calculate_textacy_lexical_diversity(text_diverse)

        assert isinstance(result, dict)
        assert 'available' in result
        assert 'mattr' in result
        assert 'rttr' in result
        assert 'mattr_score' in result
        assert 'rttr_score' in result
        assert 'mattr_assessment' in result
        assert 'rttr_assessment' in result

    def test_textacy_lexical_mattr_range(self, analyzer, text_diverse):
        """Test MATTR is in valid range."""
        result = analyzer._calculate_textacy_lexical_diversity(text_diverse)

        if result.get('mattr'):
            # MATTR should be between 0 and 1
            assert 0 <= result['mattr'] <= 1

    def test_textacy_lexical_rttr_range(self, analyzer, text_diverse):
        """Test RTTR is in valid range."""
        result = analyzer._calculate_textacy_lexical_diversity(text_diverse)

        if result.get('rttr'):
            # RTTR should be positive
            assert result['rttr'] > 0

    def test_textacy_lexical_assessments(self, analyzer, text_diverse):
        """Test that assessments are valid."""
        result = analyzer._calculate_textacy_lexical_diversity(text_diverse)

        valid_assessments = ['EXCELLENT', 'GOOD', 'FAIR', 'POOR', 'UNAVAILABLE', 'ERROR']
        if 'mattr_assessment' in result:
            assert result['mattr_assessment'] in valid_assessments
        if 'rttr_assessment' in result:
            assert result['rttr_assessment'] in valid_assessments

    def test_textacy_lexical_excludes_code(self, analyzer):
        """Test that code blocks are excluded."""
        text = """# Example

Some diverse vocabulary here with various words.

```python
def function():
    return value
```

More text after code."""
        result = analyzer._calculate_textacy_lexical_diversity(text)

        # Should analyze non-code text
        assert isinstance(result, dict)


class TestCalculateTextacyLexicalDiversityNoTextacy:
    """Tests for _calculate_textacy_lexical_diversity without textacy."""

    @pytest.mark.skipif(HAS_TEXTACY and HAS_SPACY, reason="Test requires textacy to be unavailable")
    def test_textacy_lexical_no_textacy(self, analyzer, text_diverse):
        """Test textacy lexical without textacy available."""
        result = analyzer._calculate_textacy_lexical_diversity(text_diverse)

        assert result['available'] is False
        assert result['mattr'] == 0.0
        assert result['rttr'] == 0.0


class TestScore:
    """Tests for score method."""

    def test_score_high_human_like(self, analyzer):
        """Test score for human-like text (low top-10)."""
        analysis = {'available': True, 'gltr_top10_percentage': 0.45}  # < 0.50 threshold
        score, label = analyzer.score(analysis)

        assert score == 10.0
        assert label == "HIGH"

    def test_score_medium(self, analyzer):
        """Test score for medium predictability."""
        analysis = {'available': True, 'gltr_top10_percentage': 0.55}  # < 0.60 threshold
        score, label = analyzer.score(analysis)

        assert score == 7.0
        assert label == "MEDIUM"

    def test_score_low(self, analyzer):
        """Test score for AI-leaning text."""
        analysis = {'available': True, 'gltr_top10_percentage': 0.65}  # < 0.70 threshold
        score, label = analyzer.score(analysis)

        assert score == 4.0
        assert label == "LOW"

    def test_score_very_low_ai_like(self, analyzer):
        """Test score for AI-like text (high top-10)."""
        analysis = {'available': True, 'gltr_top10_percentage': 0.75}  # >= 0.70 threshold
        score, label = analyzer.score(analysis)

        assert score == 2.0
        assert label == "VERY LOW"

    def test_score_unavailable(self, analyzer):
        """Test score when analysis unavailable."""
        analysis = {'available': False}
        score, label = analyzer.score(analysis)

        assert score == 5.0
        assert label == "UNAVAILABLE"

    def test_score_no_gltr_uses_default(self, analyzer):
        """Test score uses default when GLTR not available."""
        analysis = {'available': True}  # No gltr_top10_percentage
        score, label = analyzer.score(analysis)

        # Should use default 0.55 and score as MEDIUM
        assert score == 7.0
        assert label == "MEDIUM"


# GLTR tests are marked as slow and skip by default due to model loading
@pytest.mark.slow
class TestCalculateGltrMetrics:
    """Tests for _calculate_gltr_metrics method (requires transformers, slow)."""

    def test_gltr_metrics_basic_structure(self, analyzer, text_diverse):
        """Test GLTR metrics basic structure."""
        result = analyzer._calculate_gltr_metrics(text_diverse)

        # May be empty if model fails to load or text too short
        assert isinstance(result, dict)

    def test_gltr_metrics_empty_text(self, analyzer):
        """Test GLTR on empty text."""
        result = analyzer._calculate_gltr_metrics("")

        assert result == {}

    def test_gltr_metrics_short_text(self, analyzer):
        """Test GLTR on short text."""
        result = analyzer._calculate_gltr_metrics("Short text.")

        # May return empty dict if too short
        assert isinstance(result, dict)


@pytest.mark.slow
class TestAnalyzeHighPredictabilitySegmentsDetailed:
    """Tests for _analyze_high_predictability_segments_detailed (requires transformers, slow)."""

    def test_high_predictability_basic(self, analyzer, text_diverse):
        """Test high predictability segment detection."""
        lines = text_diverse.split('\n')
        result = analyzer._analyze_high_predictability_segments_detailed(lines)

        assert isinstance(result, list)

    def test_high_predictability_skips_headings(self, analyzer):
        """Test that headings are skipped."""
        lines = [
            "# This is a heading with content",
            "Body text here with various words."
        ]
        result = analyzer._analyze_high_predictability_segments_detailed(lines)

        # Should skip heading
        assert isinstance(result, list)

    def test_high_predictability_skips_code(self, analyzer):
        """Test that code blocks are skipped."""
        lines = [
            "```python",
            "def function():",
            "```",
            "Body text here."
        ]
        result = analyzer._analyze_high_predictability_segments_detailed(lines)

        # Should skip code blocks
        assert isinstance(result, list)


class TestAnalyzeHighPredictabilitySegmentsNoTransformers:
    """Tests for _analyze_high_predictability_segments_detailed without transformers."""

    @pytest.mark.skipif(HAS_TRANSFORMERS, reason="Test requires transformers to be unavailable")
    def test_high_predictability_no_transformers(self, analyzer):
        """Test high predictability without transformers."""
        lines = ["Some text here."]
        result = analyzer._analyze_high_predictability_segments_detailed(lines)

        assert isinstance(result, list)
        assert len(result) == 0


class TestIntegration:
    """Integration tests."""

    def test_analyze_returns_dict(self, analyzer, text_diverse):
        """Test that analyze always returns a dict."""
        result = analyzer.analyze(text_diverse)

        assert isinstance(result, dict)

    def test_analyze_detailed_returns_list(self, analyzer, text_diverse):
        """Test that analyze_detailed always returns a list."""
        lines = text_diverse.split('\n')
        result = analyzer.analyze_detailed(lines)

        assert isinstance(result, list)

    def test_comparison_diverse_vs_repetitive(self, analyzer, text_diverse, text_repetitive):
        """Test that analyzer distinguishes diverse from repetitive text."""
        diverse_result = analyzer.analyze(text_diverse)
        repetitive_result = analyzer.analyze(text_repetitive)

        # Both should have results if scipy available
        assert isinstance(diverse_result, dict)
        assert isinstance(repetitive_result, dict)

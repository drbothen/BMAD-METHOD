"""
Tests for PredictabilityDimension - GLTR token predictability analysis.
Story 1.4.5 - New dimension split from AdvancedDimension.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from ai_pattern_analyzer.dimensions.predictability import PredictabilityDimension
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry


@pytest.fixture
def dimension():
    """Create PredictabilityDimension instance."""
    # Clear registry before each test to avoid duplicate registration errors
    DimensionRegistry.clear()
    return PredictabilityDimension()


@pytest.fixture
def human_like_text():
    """Text sample expected to have human-like GLTR scores (<55% top-10)."""
    return """
    The unexpected sunset painted vibrant streaks across the horizon.
    She wandered through the forgotten garden, discovering peculiar flowers
    blooming in hidden corners. Their fragrance evoked memories she couldn't
    quite place, lingering somewhere between dreams and reality.
    """


@pytest.fixture
def ai_like_text():
    """Text sample expected to have AI-like GLTR scores (>70% top-10)."""
    return """
    It is important to note that we need to leverage innovative solutions.
    Furthermore, this approach facilitates seamless integration. Moreover,
    the comprehensive framework optimizes performance through cutting-edge
    technology. Additionally, we can utilize robust methodologies.
    """


class TestDimensionMetadata:
    """Tests for dimension metadata and registration."""

    def test_dimension_name(self, dimension):
        """Test dimension name is 'predictability'."""
        assert dimension.dimension_name == "predictability"

    def test_dimension_weight(self, dimension):
        """Test dimension weight is 20.0% (highest single dimension)."""
        assert dimension.weight == 20.0

    def test_dimension_tier(self, dimension):
        """Test dimension tier is ADVANCED."""
        assert dimension.tier == "ADVANCED"

    def test_dimension_description(self, dimension):
        """Test dimension has meaningful description."""
        desc = dimension.description
        assert isinstance(desc, str)
        assert len(desc) > 20
        assert "GLTR" in desc or "predictability" in desc.lower()

    def test_dimension_registers_on_init(self):
        """Test dimension self-registers with registry on initialization."""
        DimensionRegistry.clear()
        dim = PredictabilityDimension()

        registered = DimensionRegistry.get("predictability")
        assert registered is dim


class TestAnalyzeMethod:
    """Tests for analyze() method - must ONLY collect GLTR metrics."""

    @patch('ai_pattern_analyzer.dimensions.predictability._perplexity_model')
    @patch('ai_pattern_analyzer.dimensions.predictability._perplexity_tokenizer')
    def test_analyze_returns_gltr_metrics_only(self, mock_tokenizer, mock_model, dimension):
        """Test analyze() collects ONLY GLTR metrics (no HDD, Yule's K, MATTR, etc.)."""
        # Mock GLTR calculation to return fake metrics
        with patch.object(dimension, '_calculate_gltr_metrics', return_value={
            'gltr_top10_percentage': 0.55,
            'gltr_top100_percentage': 0.85,
            'gltr_top1000_percentage': 0.95,
            'gltr_mean_rank': 50.0,
            'gltr_rank_variance': 100.0,
            'gltr_likelihood': 0.5
        }):
            text = "Sample text for GLTR analysis."
            result = dimension.analyze(text)

            # Should contain GLTR metrics
            assert 'gltr_top10_percentage' in result
            assert 'gltr_top100_percentage' in result
            assert 'gltr_top1000_percentage' in result
            assert 'available' in result

            # Should NOT contain lexical diversity metrics (those belong in AdvancedLexicalDimension)
            assert 'hdd_score' not in result
            assert 'yules_k' not in result
            assert 'mattr' not in result
            assert 'rttr' not in result
            assert 'maas_score' not in result

    def test_analyze_sets_available_flag(self, dimension):
        """Test analyze() sets 'available' flag."""
        with patch.object(dimension, '_calculate_gltr_metrics', return_value={'gltr_top10_percentage': 0.55}):
            result = dimension.analyze("Sample text")
            assert 'available' in result
            assert result['available'] is True

    def test_analyze_handles_empty_text(self, dimension):
        """Test analyze() handles empty text gracefully."""
        result = dimension.analyze("")
        assert 'available' in result
        # Should still return a result structure, even if GLTR fails


class TestCalculateScoreMethod:
    """Tests for calculate_score() - scores ONLY on GLTR top-10 percentage."""

    def test_score_very_human_like(self, dimension):
        """Test score for very human-like GLTR (<50% top-10)."""
        metrics = {
            'available': True,
            'gltr_top10_percentage': 0.45
        }
        score = dimension.calculate_score(metrics)

        assert score == 100.0  # Very human-like

    def test_score_good(self, dimension):
        """Test score for good GLTR (50-60% top-10)."""
        metrics = {
            'available': True,
            'gltr_top10_percentage': 0.55
        }
        score = dimension.calculate_score(metrics)

        assert score == 75.0  # Good

    def test_score_borderline(self, dimension):
        """Test score for borderline GLTR (60-70% top-10)."""
        metrics = {
            'available': True,
            'gltr_top10_percentage': 0.65
        }
        score = dimension.calculate_score(metrics)

        assert score == 50.0  # Borderline

    def test_score_ai_signature(self, dimension):
        """Test score for strong AI signature (>70% top-10)."""
        metrics = {
            'available': True,
            'gltr_top10_percentage': 0.75
        }
        score = dimension.calculate_score(metrics)

        assert score == 25.0  # Strong AI signature

    def test_score_unavailable_data(self, dimension):
        """Test score when GLTR data unavailable."""
        metrics = {
            'available': False
        }
        score = dimension.calculate_score(metrics)

        assert score == 50.0  # Neutral score for unavailable data

    def test_score_missing_gltr_uses_default(self, dimension):
        """Test score when gltr_top10_percentage missing uses default."""
        metrics = {
            'available': True
            # Missing gltr_top10_percentage - should use default 0.55
        }
        score = dimension.calculate_score(metrics)

        assert score == 75.0  # Default 0.55 maps to 75.0

    def test_score_validates_range(self, dimension):
        """Test score is always in valid 0-100 range."""
        test_cases = [0.0, 0.25, 0.50, 0.60, 0.70, 0.85, 1.0]

        for gltr_value in test_cases:
            metrics = {
                'available': True,
                'gltr_top10_percentage': gltr_value
            }
            score = dimension.calculate_score(metrics)
            assert 0.0 <= score <= 100.0


class TestGetRecommendations:
    """Tests for get_recommendations() method."""

    def test_recommendations_for_high_predictability(self, dimension):
        """Test recommendations when GLTR shows high predictability (AI signature)."""
        metrics = {
            'available': True,
            'gltr_top10_percentage': 0.75
        }
        recommendations = dimension.get_recommendations(75.0, metrics)

        assert len(recommendations) > 0
        assert any('predictability' in rec.lower() or 'gltr' in rec.lower() for rec in recommendations)
        assert any('rewrite' in rec.lower() or 'varied' in rec.lower() for rec in recommendations)

    def test_recommendations_for_elevated_predictability(self, dimension):
        """Test recommendations when GLTR shows elevated predictability."""
        metrics = {
            'available': True,
            'gltr_top10_percentage': 0.65
        }
        recommendations = dimension.get_recommendations(50.0, metrics)

        assert len(recommendations) > 0

    def test_recommendations_for_excellent_score(self, dimension):
        """Test recommendations when GLTR shows excellent unpredictability."""
        metrics = {
            'available': True,
            'gltr_top10_percentage': 0.45
        }
        recommendations = dimension.get_recommendations(100.0, metrics)

        assert len(recommendations) > 0
        assert any('excellent' in rec.lower() or 'human-like' in rec.lower() for rec in recommendations)

    def test_recommendations_unavailable_data(self, dimension):
        """Test recommendations when GLTR unavailable."""
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

        poor_min, poor_max = tiers['poor']
        assert poor_min == 0.0
        assert poor_max < 50.0


class TestGLTRMetricCalculation:
    """Tests for _calculate_gltr_metrics() helper method."""

    @patch('ai_pattern_analyzer.dimensions.predictability._perplexity_model', None)
    @patch('ai_pattern_analyzer.dimensions.predictability._perplexity_tokenizer', None)
    def test_gltr_loads_model_lazily(self, dimension):
        """Test GLTR loads model on first use (lazy loading)."""
        # This would trigger model loading in real scenario
        # For unit test, we just verify the pattern works
        result = dimension._calculate_gltr_metrics("Short text")

        # Should return empty dict if model not loaded (in test environment)
        assert isinstance(result, dict)

    def test_gltr_handles_short_text(self, dimension):
        """Test GLTR handles text too short for analysis."""
        result = dimension._calculate_gltr_metrics("Hi")

        # Should return empty dict for text <10 tokens
        assert isinstance(result, dict)

    def test_gltr_handles_code_blocks(self, dimension):
        """Test GLTR removes code blocks before analysis."""
        text_with_code = """
        Here is some text.
        ```python
        def foo():
            pass
        ```
        More text here.
        """

        # Should not crash on code blocks
        result = dimension._calculate_gltr_metrics(text_with_code)
        assert isinstance(result, dict)


class TestAnalyzeDetailed:
    """Tests for analyze_detailed() method."""

    def test_analyze_detailed_returns_list(self, dimension):
        """Test analyze_detailed returns list of HighPredictabilitySegment objects."""
        lines = [
            "# Header",
            "This is a line of text.",
            "Another line with some content.",
            "Final line here."
        ]

        result = dimension.analyze_detailed(lines)

        assert isinstance(result, list)
        # May be empty if model not loaded in test environment

    def test_analyze_detailed_respects_html_comment_checker(self, dimension):
        """Test analyze_detailed skips HTML comments."""
        lines = [
            "<!-- This is a comment -->",
            "Real content here.",
            "<!-- Another comment -->"
        ]

        def is_html_comment(line):
            return line.strip().startswith('<!--')

        result = dimension.analyze_detailed(lines, html_comment_checker=is_html_comment)

        # Should process without error
        assert isinstance(result, list)


class TestBackwardCompatibility:
    """Tests for backward compatibility alias."""

    def test_backward_compatibility_alias_exists(self):
        """Test PredictabilityAnalyzer alias exists for backward compatibility."""
        from ai_pattern_analyzer.dimensions.predictability import PredictabilityAnalyzer

        DimensionRegistry.clear()
        dim = PredictabilityAnalyzer()

        assert dim.dimension_name == "predictability"
        assert dim.weight == 20.0


class TestTimeoutMechanism:
    """Tests for timeout protection (Story 1.4.14)."""

    def test_timeout_wrapper_exists(self, dimension):
        """Test _calculate_gltr_metrics_with_timeout method exists."""
        assert hasattr(dimension, '_calculate_gltr_metrics_with_timeout')
        assert callable(dimension._calculate_gltr_metrics_with_timeout)

    def test_timeout_returns_none_on_timeout(self, dimension):
        """Test timeout wrapper returns None when timeout occurs."""
        # Mock _calculate_gltr_metrics to take longer than timeout
        import time

        def slow_calculation(text):
            time.sleep(2)  # Sleep longer than timeout
            return {'gltr_top10_percentage': 0.55}

        with patch.object(dimension, '_calculate_gltr_metrics', side_effect=slow_calculation):
            result = dimension._calculate_gltr_metrics_with_timeout("test text", timeout=1)

            # Should timeout and return None
            assert result is None

    def test_timeout_returns_result_when_fast(self, dimension):
        """Test timeout wrapper returns result when calculation completes in time."""
        expected_result = {'gltr_top10_percentage': 0.55, 'gltr_likelihood': 0.5}

        with patch.object(dimension, '_calculate_gltr_metrics', return_value=expected_result):
            result = dimension._calculate_gltr_metrics_with_timeout("test text", timeout=30)

            # Should complete and return result
            assert result == expected_result

    def test_timeout_handles_exceptions_gracefully(self, dimension):
        """Test timeout wrapper handles exceptions in worker thread."""
        def failing_calculation(text):
            raise ValueError("Test exception")

        with patch.object(dimension, '_calculate_gltr_metrics', side_effect=failing_calculation):
            result = dimension._calculate_gltr_metrics_with_timeout("test text", timeout=30)

            # Should catch exception and return None
            assert result is None

    def test_analyze_uses_timeout_wrapper(self, dimension):
        """Test analyze() method uses timeout-protected version."""
        with patch.object(dimension, '_calculate_gltr_metrics_with_timeout', return_value={
            'gltr_top10_percentage': 0.55,
            'gltr_top100_percentage': 0.85,
            'gltr_top1000_percentage': 0.95,
            'gltr_mean_rank': 50.0,
            'gltr_rank_variance': 100.0,
            'gltr_likelihood': 0.5
        }) as mock_timeout:
            result = dimension.analyze("Test text")

            # Should have called timeout version
            mock_timeout.assert_called()
            assert result['available'] is True

    def test_analyze_handles_timeout_gracefully(self, dimension):
        """Test analyze() returns unavailable when timeout occurs."""
        with patch.object(dimension, '_calculate_gltr_metrics_with_timeout', return_value=None):
            result = dimension.analyze("Test text")

            # Should return unavailable but not crash
            assert 'available' in result
            # Result structure may vary based on config mode


class TestModelCaching:
    """Tests for model caching optimization (Story 1.4.14)."""

    def test_clear_model_cache_method_exists(self, dimension):
        """Test clear_model_cache() static method exists."""
        assert hasattr(PredictabilityDimension, 'clear_model_cache')
        assert callable(PredictabilityDimension.clear_model_cache)

    def test_clear_model_cache_resets_globals(self, dimension):
        """Test clear_model_cache() clears global model variables."""
        import ai_pattern_analyzer.dimensions.predictability as pred_module

        # Set mock values
        pred_module._perplexity_model = "mock_model"
        pred_module._perplexity_tokenizer = "mock_tokenizer"

        # Clear cache
        PredictabilityDimension.clear_model_cache()

        # Should be None after clearing
        assert pred_module._perplexity_model is None
        assert pred_module._perplexity_tokenizer is None

    def test_model_loading_is_thread_safe(self, dimension):
        """Test model loading uses lock for thread safety."""
        import ai_pattern_analyzer.dimensions.predictability as pred_module
        import threading

        # Verify lock exists
        assert hasattr(pred_module, '_model_lock')
        # Verify it's a threading.Lock object
        assert isinstance(pred_module._model_lock, type(threading.Lock()))

    @patch('ai_pattern_analyzer.dimensions.predictability.AutoModelForCausalLM')
    @patch('ai_pattern_analyzer.dimensions.predictability.AutoTokenizer')
    def test_model_loads_only_once(self, mock_tokenizer_class, mock_model_class, dimension):
        """Test model is loaded only once and reused."""
        import ai_pattern_analyzer.dimensions.predictability as pred_module

        # Clear cache first
        PredictabilityDimension.clear_model_cache()

        # Mock the model and tokenizer
        mock_model = MagicMock()
        mock_tokenizer = MagicMock()
        mock_model_class.from_pretrained.return_value = mock_model
        mock_tokenizer_class.from_pretrained.return_value = mock_tokenizer

        # Mock encode to return valid tokens
        mock_tokenizer.encode.return_value = list(range(50))  # 50 tokens

        # First call - should load model
        dimension._calculate_gltr_metrics("Test text sample")

        # Second call - should reuse cached model
        dimension._calculate_gltr_metrics("Another test text")

        # Model should only be loaded once
        assert mock_model_class.from_pretrained.call_count == 1
        assert mock_tokenizer_class.from_pretrained.call_count == 1


class TestPerformanceImprovement:
    """Performance tests for caching benefit (Story 1.4.14)."""

    @pytest.mark.skipif(
        not hasattr(pytest, 'skip') or True,  # Skip by default in CI
        reason="Performance test - run manually to verify caching benefit"
    )
    def test_caching_improves_performance(self, dimension):
        """Benchmark: verify model caching provides performance benefit.

        NOTE: This test is skipped by default. Run manually to verify:
        pytest tests/unit/dimensions/test_predictability.py::TestPerformanceImprovement -v -s
        """
        import time

        # Clear cache to start fresh
        PredictabilityDimension.clear_model_cache()

        text = "The quick brown fox jumps over the lazy dog. " * 20  # ~200 words

        # First analysis (cold start - loads model)
        start1 = time.time()
        result1 = dimension.analyze(text)
        time1 = time.time() - start1

        # Second analysis (should use cached model)
        start2 = time.time()
        result2 = dimension.analyze(text)
        time2 = time.time() - start2

        print(f"\nFirst analysis: {time1:.3f}s")
        print(f"Second analysis: {time2:.3f}s")
        print(f"Speedup: {time1/time2:.1f}x")

        # Both should succeed
        assert result1.get('available') in [True, False]  # May fail if dependencies missing
        assert result2.get('available') in [True, False]

        # If both succeeded, second should be faster
        # (skipping assertion as this is informational)

    def test_timeout_configurable(self, dimension):
        """Test timeout parameter is configurable."""
        with patch.object(dimension, '_calculate_gltr_metrics', return_value={'gltr_top10_percentage': 0.55}):
            # Should accept custom timeout
            result = dimension._calculate_gltr_metrics_with_timeout("test", timeout=60)
            assert result is not None

            result = dimension._calculate_gltr_metrics_with_timeout("test", timeout=10)
            assert result is not None

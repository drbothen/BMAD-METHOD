"""
Integration tests for all dimensions with config support.

Verifies all 12 dimensions accept config parameter and return consistent metadata.
Story 1.4.8: Optimize Heavy Dimensions for Full Documents
"""

import pytest
from ai_pattern_analyzer.core.analysis_config import AnalysisConfig, AnalysisMode
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry

# Import all dimensions
from ai_pattern_analyzer.dimensions.predictability import PredictabilityDimension
from ai_pattern_analyzer.dimensions.syntactic import SyntacticDimension
from ai_pattern_analyzer.dimensions.advanced_lexical import AdvancedLexicalDimension
from ai_pattern_analyzer.dimensions.readability import ReadabilityDimension
from ai_pattern_analyzer.dimensions.burstiness import BurstinessDimension
from ai_pattern_analyzer.dimensions.perplexity import PerplexityDimension
from ai_pattern_analyzer.dimensions.voice import VoiceDimension
from ai_pattern_analyzer.dimensions.lexical import LexicalDimension
from ai_pattern_analyzer.dimensions.formatting import FormattingDimension
from ai_pattern_analyzer.dimensions.structure import StructureDimension
from ai_pattern_analyzer.dimensions.sentiment import SentimentDimension
from ai_pattern_analyzer.dimensions.transition_marker import TransitionMarkerDimension


@pytest.fixture
def all_dimensions():
    """Create instances of all 12 dimensions."""
    DimensionRegistry.clear()
    return [
        PredictabilityDimension(),
        SyntacticDimension(),
        AdvancedLexicalDimension(),
        ReadabilityDimension(),
        BurstinessDimension(),
        PerplexityDimension(),
        VoiceDimension(),
        LexicalDimension(),
        FormattingDimension(),
        StructureDimension(),
        SentimentDimension(),
        TransitionMarkerDimension()
    ]


class TestAllDimensionsConfig:
    """Test all dimensions accept config and return consistent metadata."""

    def test_all_dimensions_accept_fast_mode(self, all_dimensions):
        """Test all dimensions accept FAST mode config."""
        config = AnalysisConfig(mode=AnalysisMode.FAST)
        text = "This is a test sentence. " * 100

        for dim in all_dimensions:
            result = dim.analyze(text, config=config)

            # Should not crash and should return a dict
            assert isinstance(result, dict), f"{dim.dimension_name} should return dict"
            assert 'analysis_mode' in result, f"{dim.dimension_name} missing analysis_mode"
            assert result['analysis_mode'] == 'fast', f"{dim.dimension_name} wrong mode"

    def test_all_dimensions_accept_adaptive_mode(self, all_dimensions):
        """Test all dimensions accept ADAPTIVE mode config."""
        config = AnalysisConfig(mode=AnalysisMode.ADAPTIVE)
        text = "This is a test sentence. " * 200

        for dim in all_dimensions:
            result = dim.analyze(text, config=config)

            assert isinstance(result, dict), f"{dim.dimension_name} should return dict"
            assert 'analysis_mode' in result, f"{dim.dimension_name} missing analysis_mode"
            assert result['analysis_mode'] == 'adaptive', f"{dim.dimension_name} wrong mode"

    def test_all_dimensions_return_consistent_metadata(self, all_dimensions):
        """Test all dimensions return 5 required metadata fields."""
        config = AnalysisConfig(mode=AnalysisMode.FAST)
        text = "The quick brown fox jumps over the lazy dog. " * 50

        required_fields = [
            'analysis_mode',
            'samples_analyzed',
            'total_text_length',
            'analyzed_text_length',
            'coverage_percentage'
        ]

        for dim in all_dimensions:
            result = dim.analyze(text, config=config)

            # Check all required fields present
            for field in required_fields:
                assert field in result, f"{dim.dimension_name} missing field: {field}"

            # Verify types
            assert isinstance(result['analysis_mode'], str)
            assert isinstance(result['samples_analyzed'], int)
            assert isinstance(result['total_text_length'], int)
            assert isinstance(result['analyzed_text_length'], int)
            assert isinstance(result['coverage_percentage'], (int, float))

            # Verify values are reasonable
            assert result['samples_analyzed'] >= 1
            assert result['total_text_length'] == len(text)
            assert 0 <= result['coverage_percentage'] <= 100

    def test_all_dimensions_handle_none_config(self, all_dimensions):
        """Test all dimensions handle config=None gracefully (default to ADAPTIVE)."""
        text = "Test sentence. " * 50

        for dim in all_dimensions:
            result = dim.analyze(text, config=None)

            # Should default to ADAPTIVE mode
            assert 'analysis_mode' in result
            assert result['analysis_mode'] == 'adaptive'

    def test_heavy_dimensions_support_full_mode(self):
        """Test heavy dimensions support FULL mode (no limits)."""
        DimensionRegistry.clear()

        heavy_dims = [
            PredictabilityDimension(),
            SyntacticDimension(),
            AdvancedLexicalDimension()
        ]

        config = AnalysisConfig(mode=AnalysisMode.FULL)
        # Use moderate-length text for FULL mode test
        text = "The quick brown fox jumps over the lazy dog. " * 500  # ~22.5k chars

        for dim in heavy_dims:
            result = dim.analyze(text, config=config)

            assert result['analysis_mode'] == 'full'
            # FULL mode should analyze entire text (for moderate lengths)
            assert result['analyzed_text_length'] == len(text)
            assert result['coverage_percentage'] == 100.0

    def test_fast_dimensions_ignore_sampling(self):
        """Test fast dimensions always analyze full text regardless of mode."""
        DimensionRegistry.clear()

        fast_dims = [
            ReadabilityDimension(),
            BurstinessDimension(),
            PerplexityDimension(),
            VoiceDimension(),
            LexicalDimension(),
            FormattingDimension(),
            StructureDimension(),
            SentimentDimension(),
            TransitionMarkerDimension()
        ]

        # Try different modes - all should analyze full text
        configs = [
            AnalysisConfig(mode=AnalysisMode.FAST),
            AnalysisConfig(mode=AnalysisMode.ADAPTIVE),
            AnalysisConfig(mode=AnalysisMode.FULL)
        ]

        text = "Test sentence. " * 100

        for dim in fast_dims:
            for config in configs:
                result = dim.analyze(text, config=config)

                # Fast dimensions always analyze 100%
                assert result['samples_analyzed'] == 1
                assert result['coverage_percentage'] == 100.0
                assert result['analyzed_text_length'] == len(text)

    def test_dimensions_handle_empty_text(self, all_dimensions):
        """Test all dimensions handle empty text gracefully."""
        config = AnalysisConfig(mode=AnalysisMode.FAST)

        for dim in all_dimensions:
            result = dim.analyze("", config=config)

            # Should not crash
            assert isinstance(result, dict)
            assert result['total_text_length'] == 0

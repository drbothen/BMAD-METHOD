"""
Integration test for dimension weight distribution verification.

Verifies that all refactored dimensions have correct weights as specified
in Story 1.4 and Story 1.4.5, and that the weight distribution is valid.

Story 1.4.5: Split AdvancedDimension and StylometricDimension into 4 focused dimensions.
Total dimensions: 12 (previously 10)
Total weight: 100% (previously 79%)
"""

import pytest
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry

# Import all refactored dimensions (Story 1.4)
from ai_pattern_analyzer.dimensions.perplexity import PerplexityDimension
from ai_pattern_analyzer.dimensions.burstiness import BurstinessDimension
from ai_pattern_analyzer.dimensions.structure import StructureDimension
from ai_pattern_analyzer.dimensions.formatting import FormattingDimension
from ai_pattern_analyzer.dimensions.lexical import LexicalDimension
from ai_pattern_analyzer.dimensions.voice import VoiceDimension
from ai_pattern_analyzer.dimensions.syntactic import SyntacticDimension
from ai_pattern_analyzer.dimensions.sentiment import SentimentDimension

# Import new split dimensions (Story 1.4.5)
from ai_pattern_analyzer.dimensions.predictability import PredictabilityDimension
from ai_pattern_analyzer.dimensions.advanced_lexical import AdvancedLexicalDimension
from ai_pattern_analyzer.dimensions.readability import ReadabilityDimension
from ai_pattern_analyzer.dimensions.transition_marker import TransitionMarkerDimension


# Expected weights from Story 1.4 + Story 1.4.5 (12 dimensions = 100%)
EXPECTED_WEIGHTS = {
    # CORE tier (34%)
    'perplexity': 5.0,
    'burstiness': 6.0,
    'structure': 4.0,
    'formatting': 4.0,
    'voice': 5.0,
    'readability': 10.0,  # NEW in Story 1.4.5 (split from stylometric)

    # SUPPORTING tier (20%)
    'lexical': 3.0,
    'sentiment': 17.0,

    # ADVANCED tier (46%)
    'syntactic': 2.0,
    'predictability': 20.0,      # NEW in Story 1.4.5 (split from advanced)
    'advanced_lexical': 14.0,    # NEW in Story 1.4.5 (split from advanced)
    'transition_marker': 10.0,   # NEW in Story 1.4.5 (split from stylometric)
}

# Expected tiers from Story 1.4 + Story 1.4.5
EXPECTED_TIERS = {
    # CORE tier (6 dimensions)
    'perplexity': 'CORE',
    'burstiness': 'CORE',
    'structure': 'CORE',
    'formatting': 'CORE',
    'voice': 'CORE',
    'readability': 'CORE',       # NEW in Story 1.4.5

    # SUPPORTING tier (2 dimensions)
    'lexical': 'SUPPORTING',
    'sentiment': 'SUPPORTING',

    # ADVANCED tier (4 dimensions)
    'syntactic': 'ADVANCED',
    'predictability': 'ADVANCED',      # NEW in Story 1.4.5
    'advanced_lexical': 'ADVANCED',    # NEW in Story 1.4.5
    'transition_marker': 'ADVANCED',   # NEW in Story 1.4.5
}


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear registry before and after each test."""
    DimensionRegistry.clear()
    yield
    DimensionRegistry.clear()


class TestWeightDistribution:
    """Tests for dimension weight distribution."""

    def test_all_dimensions_register(self):
        """Test that all 12 refactored dimensions register successfully."""
        # Instantiate all dimensions (Story 1.4 + Story 1.4.5)
        PerplexityDimension()
        BurstinessDimension()
        StructureDimension()
        FormattingDimension()
        LexicalDimension()
        VoiceDimension()
        SyntacticDimension()
        SentimentDimension()
        # New dimensions from Story 1.4.5
        PredictabilityDimension()
        AdvancedLexicalDimension()
        ReadabilityDimension()
        TransitionMarkerDimension()

        # Verify all are registered
        all_dimensions = DimensionRegistry.get_all()
        assert len(all_dimensions) == 12, f"Expected 12 dimensions, got {len(all_dimensions)}"

    def test_individual_dimension_weights(self):
        """Test that each dimension has the correct weight."""
        # Instantiate all dimensions
        PerplexityDimension()
        BurstinessDimension()
        StructureDimension()
        FormattingDimension()
        LexicalDimension()
        VoiceDimension()
        SyntacticDimension()
        SentimentDimension()
        PredictabilityDimension()
        AdvancedLexicalDimension()
        ReadabilityDimension()
        TransitionMarkerDimension()

        # Check each dimension's weight
        for dimension_name, expected_weight in EXPECTED_WEIGHTS.items():
            dimension = DimensionRegistry.get(dimension_name)
            assert dimension is not None, f"Dimension '{dimension_name}' not found in registry"
            actual_weight = dimension.weight
            assert actual_weight == expected_weight, \
                f"Dimension '{dimension_name}' has weight {actual_weight}, expected {expected_weight}"

    def test_individual_dimension_tiers(self):
        """Test that each dimension has the correct tier."""
        # Instantiate all dimensions
        PerplexityDimension()
        BurstinessDimension()
        StructureDimension()
        FormattingDimension()
        LexicalDimension()
        VoiceDimension()
        SyntacticDimension()
        SentimentDimension()
        PredictabilityDimension()
        AdvancedLexicalDimension()
        ReadabilityDimension()
        TransitionMarkerDimension()

        # Check each dimension's tier
        for dimension_name, expected_tier in EXPECTED_TIERS.items():
            dimension = DimensionRegistry.get(dimension_name)
            assert dimension is not None, f"Dimension '{dimension_name}' not found in registry"
            actual_tier = dimension.tier
            assert actual_tier == expected_tier, \
                f"Dimension '{dimension_name}' has tier {actual_tier}, expected {expected_tier}"

    def test_weight_sum(self):
        """Test that refactored dimension weights sum to 100% (Story 1.4.5 achievement)."""
        # Instantiate all dimensions
        PerplexityDimension()
        BurstinessDimension()
        StructureDimension()
        FormattingDimension()
        LexicalDimension()
        VoiceDimension()
        SyntacticDimension()
        SentimentDimension()
        PredictabilityDimension()
        AdvancedLexicalDimension()
        ReadabilityDimension()
        TransitionMarkerDimension()

        # Calculate total weight
        total_weight = sum(EXPECTED_WEIGHTS.values())
        expected_total = 100.0  # Story 1.4.5: Achieved 100% weight scale (was 79%)

        assert total_weight == expected_total, \
            f"Total weight is {total_weight}, expected {expected_total}"

    def test_dimension_names_match(self):
        """Test that dimension_name property matches registry key."""
        # Instantiate all dimensions
        dimensions = [
            PerplexityDimension(),
            BurstinessDimension(),
            StructureDimension(),
            FormattingDimension(),
            LexicalDimension(),
            VoiceDimension(),
            SyntacticDimension(),
            SentimentDimension(),
            PredictabilityDimension(),
            AdvancedLexicalDimension(),
            ReadabilityDimension(),
            TransitionMarkerDimension(),
        ]

        # Check each dimension's name
        for dimension in dimensions:
            name = dimension.dimension_name
            registered = DimensionRegistry.get(name)
            assert registered is dimension, \
                f"Dimension '{name}' not found by name in registry"

    def test_weight_range_validation(self):
        """Test that all weights are within valid range (0-100)."""
        # Instantiate all dimensions
        PerplexityDimension()
        BurstinessDimension()
        StructureDimension()
        FormattingDimension()
        LexicalDimension()
        VoiceDimension()
        SyntacticDimension()
        SentimentDimension()
        PredictabilityDimension()
        AdvancedLexicalDimension()
        ReadabilityDimension()
        TransitionMarkerDimension()

        # Check weight ranges
        all_dimensions = DimensionRegistry.get_all()
        for dimension in all_dimensions:
            weight = dimension.weight
            assert 0 <= weight <= 100, \
                f"Dimension '{dimension.dimension_name}' has invalid weight {weight} (must be 0-100)"

    def test_tier_categorization(self):
        """Test dimension tier distribution (Story 1.4.5: CORE=6, SUPPORTING=2, ADVANCED=4)."""
        # Instantiate all dimensions
        PerplexityDimension()
        BurstinessDimension()
        StructureDimension()
        FormattingDimension()
        LexicalDimension()
        VoiceDimension()
        SyntacticDimension()
        SentimentDimension()
        PredictabilityDimension()
        AdvancedLexicalDimension()
        ReadabilityDimension()
        TransitionMarkerDimension()

        # Count dimensions by tier
        tier_counts = {}
        all_dimensions = DimensionRegistry.get_all()
        for dimension in all_dimensions:
            tier = dimension.tier
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        # Verify tier distribution (from Story 1.4 + Story 1.4.5)
        assert tier_counts.get('CORE', 0) == 6, f"Expected 6 CORE dimensions, got {tier_counts.get('CORE', 0)}"
        assert tier_counts.get('SUPPORTING', 0) == 2, f"Expected 2 SUPPORTING dimensions, got {tier_counts.get('SUPPORTING', 0)}"
        assert tier_counts.get('ADVANCED', 0) == 4, f"Expected 4 ADVANCED dimensions, got {tier_counts.get('ADVANCED', 0)}"

    def test_required_methods_implemented(self):
        """Test that all dimensions implement required DimensionStrategy methods."""
        # Instantiate all dimensions
        dimensions = [
            PerplexityDimension(),
            BurstinessDimension(),
            StructureDimension(),
            FormattingDimension(),
            LexicalDimension(),
            VoiceDimension(),
            SyntacticDimension(),
            SentimentDimension(),
            PredictabilityDimension(),
            AdvancedLexicalDimension(),
            ReadabilityDimension(),
            TransitionMarkerDimension(),
        ]

        required_methods = [
            'dimension_name',
            'weight',
            'tier',
            'description',
            'analyze',
            'calculate_score',
            'get_recommendations',
            'get_tiers',
        ]

        for dimension in dimensions:
            for method_name in required_methods:
                assert hasattr(dimension, method_name), \
                    f"Dimension '{dimension.dimension_name}' missing required method/property '{method_name}'"

"""
Integration test for dimension self-registration.

Tests that dimensions can self-register with the DimensionRegistry
and that weights are correctly assigned.
"""

import pytest
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry
from ai_pattern_analyzer.dimensions.perplexity import PerplexityDimension
from ai_pattern_analyzer.dimensions.burstiness import BurstinessDimension


class TestDimensionRegistration:
    """Test dimension self-registration functionality."""

    def test_perplexity_registration(self):
        """Test that PerplexityDimension registers correctly."""
        DimensionRegistry.clear()
        dim = PerplexityDimension()

        # get_all() returns a list of dimensions
        all_dims = DimensionRegistry.get_all()
        assert len(all_dims) == 1

        # get() returns the dimension by name
        registered = DimensionRegistry.get('perplexity')

        assert registered.dimension_name == 'perplexity'
        assert registered.weight == 5.0
        assert registered.tier == 'CORE'
        assert dim is registered  # Same instance

    def test_burstiness_registration(self):
        """Test that BurstinessDimension registers correctly."""
        DimensionRegistry.clear()
        dim = BurstinessDimension()

        # get_all() returns a list of dimensions
        all_dims = DimensionRegistry.get_all()
        assert len(all_dims) == 1

        # get() returns the dimension by name
        registered = DimensionRegistry.get('burstiness')

        assert registered.dimension_name == 'burstiness'
        assert registered.weight == 6.0
        assert registered.tier == 'CORE'
        assert dim is registered  # Same instance

    def test_multiple_dimension_registration(self):
        """Test that multiple dimensions can register together."""
        DimensionRegistry.clear()
        perp = PerplexityDimension()
        burst = BurstinessDimension()

        # get_all() returns a list
        all_dims = DimensionRegistry.get_all()
        assert len(all_dims) == 2

        # Verify both dimensions are registered
        assert DimensionRegistry.get('perplexity') is perp
        assert DimensionRegistry.get('burstiness') is burst

        # Verify total weight
        total_weight = sum(d.weight for d in all_dims)
        assert total_weight == 11.0  # 5.0 + 6.0

    def test_duplicate_registration_prevention(self):
        """Test that duplicate registration is prevented."""
        from ai_pattern_analyzer.core.exceptions import DuplicateDimensionError

        DimensionRegistry.clear()
        PerplexityDimension()

        # Attempting to register another instance should fail
        with pytest.raises(DuplicateDimensionError):
            PerplexityDimension()

    def test_backward_compatibility_alias(self):
        """Test that backward compatibility aliases work."""
        from ai_pattern_analyzer.dimensions.perplexity import PerplexityAnalyzer
        from ai_pattern_analyzer.dimensions.burstiness import BurstinessAnalyzer

        # Aliases should point to the new classes
        assert PerplexityAnalyzer is PerplexityDimension
        assert BurstinessAnalyzer is BurstinessDimension

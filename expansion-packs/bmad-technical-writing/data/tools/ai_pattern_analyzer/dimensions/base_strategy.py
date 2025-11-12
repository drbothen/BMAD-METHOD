"""
Enhanced dimension base contract for self-registering dimension architecture.

This module provides the new base class (DimensionStrategy) that all dimensions
will eventually implement. It maintains backward compatibility with the existing
DimensionAnalyzer base class during the transition period.

The DimensionStrategy class requires dimensions to declare all metadata (weight,
tiers, recommendations) so the algorithm can dynamically incorporate them without
core code modifications.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Tuple, Any, Optional, Union
from collections import Counter

# Required AST parsing support
from marko import Markdown
from marko.block import Quote, Heading, List as MarkoList, Paragraph, FencedCode
from marko.inline import Link, CodeSpan

# Configuration support
from ai_pattern_analyzer.core.analysis_config import AnalysisConfig, DEFAULT_CONFIG


class DimensionTier(str, Enum):
    """
    Valid dimension tier classifications.

    Tiers organize dimensions by their detection accuracy and role:

    - ADVANCED: ML-based, highest accuracy metrics (95%+ on GPT detection)
      Target weight: 30-40% of total score
      Examples: GLTR, Stylometric, Syntactic, Multi-Model Perplexity

    - CORE: Proven AI signatures (>85% accuracy, established research)
      Target weight: 35-45% of total score
      Examples: Burstiness, Perplexity, Formatting, Voice, Structure

    - SUPPORTING: Contextual quality indicators (correlation with AI text)
      Target weight: 15-25% of total score
      Examples: Lexical Diversity, Sentiment, Technical Depth

    - STRUCTURAL: AST-based structural patterns (mechanical structure detection)
      Target weight: 5-10% of total score
      Examples: Blockquote, Link Anchor, List AST, Code AST
    """

    ADVANCED = "ADVANCED"
    CORE = "CORE"
    SUPPORTING = "SUPPORTING"
    STRUCTURAL = "STRUCTURAL"


class DimensionStrategy(ABC):
    """
    Enhanced base class for all dimension analyzers.

    This base class defines the contract that all dimensions must implement,
    including metadata declaration (weight, tier) and recommendation generation.

    Scoring Convention:
        All dimensions use a 0-100 scale where:
        - 100.0 = most human-like (perfect score, no AI patterns)
        - 0.0 = most AI-like (worst score, strong AI patterns)
        Higher scores are better.

    Example Implementation:
        ```python
        from ai_pattern_analyzer.dimensions.base_strategy import (
            DimensionStrategy, DimensionTier
        )

        class MyDimension(DimensionStrategy):
            @property
            def dimension_name(self) -> str:
                return "my_dimension"

            @property
            def weight(self) -> float:
                return 5.0  # 5% of total score

            @property
            def tier(self) -> DimensionTier:
                return DimensionTier.SUPPORTING

            @property
            def description(self) -> str:
                return "Analyzes my specific pattern"

            def analyze(self, text: str, lines: List[str], **kwargs) -> Dict[str, Any]:
                # Perform analysis
                return {'metric': 42}

            def calculate_score(self, metrics: Dict[str, Any]) -> float:
                score = 100.0 - metrics['metric']
                self._validate_score(score)
                return score

            def get_recommendations(
                self, score: float, metrics: Dict[str, Any]
            ) -> List[str]:
                if score < 75:
                    return ["Improve metric to < 25"]
                return []

            def get_tiers(self) -> Dict[str, Tuple[float, float]]:
                return {
                    'excellent': (90.0, 100.0),
                    'good': (75.0, 89.9),
                    'acceptable': (50.0, 74.9),
                    'poor': (0.0, 49.9)
                }
        ```
    """

    def __init__(self):
        """Initialize the dimension strategy with AST support."""
        # AST parser and cache (marko) for markdown structure analysis
        self._markdown_parser = None
        self._ast_cache = {}

    # ========================================================================
    # ABSTRACT PROPERTIES - Must be implemented by all subclasses
    # ========================================================================

    @property
    @abstractmethod
    def dimension_name(self) -> str:
        """
        Unique dimension identifier.

        Returns:
            str: Lowercase alphanumeric + underscores identifier
                 Examples: "perplexity", "burstiness", "code_block"
                 Used as registry key for dynamic dimension loading
        """
        pass

    @property
    @abstractmethod
    def weight(self) -> float:
        """
        Contribution weight for overall scoring (0-100 scale).

        Returns:
            float: Weight value (0-100)
                   Example: 5.0 means 5% of total score
                   Sum across all dimensions must equal 100.0 (validated by WeightMediator)
        """
        pass

    @property
    @abstractmethod
    def tier(self) -> DimensionTier:
        """
        Grouping tier classification.

        Returns:
            DimensionTier: One of ADVANCED, CORE, SUPPORTING, STRUCTURAL
                          Used for organizing dimensions in reports
                          Each tier has target weight range (see DimensionTier docs)
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Human-readable description of what this dimension analyzes.

        Returns:
            str: Description text
                 Example: "Analyzes vocabulary predictability and AI-typical word patterns"
        """
        pass

    # ========================================================================
    # ABSTRACT METHODS - Must be implemented by all subclasses
    # ========================================================================

    @abstractmethod
    def analyze(
        self,
        text: str,
        lines: List[str] = None,
        config: Optional[AnalysisConfig] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Perform dimension-specific analysis on text.

        Args:
            text (str): Full document text
            lines (List[str]): Text split into lines (for line-by-line analysis)
            config (Optional[AnalysisConfig]): Analysis configuration (None = current behavior)
            **kwargs: Additional parameters including:
                word_count (int): Pre-calculated word count for efficiency
                domain (DocumentDomain): Document type for threshold selection
                    Values: GENERAL, TECHNICAL, CREATIVE, ACADEMIC, BUSINESS
                file_path (str, optional): File path for context/logging

        Returns:
            Dict[str, Any]: Dictionary with dimension-specific metrics

        Example:
            ```python
            {
                'ai_vocabulary': {
                    'count': 5,
                    'per_1k': 2.3,
                    'words': ['delve', 'leverage']
                },
                'formulaic_transitions': {
                    'count': 3,
                    'transitions': ['Furthermore,', 'Moreover,']
                }
            }
            ```
        """
        pass

    @abstractmethod
    def calculate_score(self, metrics: Dict[str, Any]) -> float:
        """
        Convert raw metrics from analyze() into 0-100 score.

        Args:
            metrics (Dict[str, Any]): Output from analyze() method

        Returns:
            float: Score from 0.0 (AI-like) to 100.0 (human-like)
                   Must call self._validate_score(score) before returning

        Example:
            ```python
            def calculate_score(self, metrics: Dict[str, Any]) -> float:
                ai_vocab_per_1k = metrics.get('ai_vocabulary', {}).get('per_1k', 0)

                if ai_vocab_per_1k < 1.0:
                    score = 100.0
                elif ai_vocab_per_1k < 3.0:
                    score = 75.0
                else:
                    score = 50.0

                self._validate_score(score)
                return score
            ```
        """
        pass

    @abstractmethod
    def get_recommendations(
        self, score: float, metrics: Dict[str, Any]
    ) -> List[str]:
        """
        Generate actionable recommendations based on score and metrics.

        Args:
            score (float): The calculated score from calculate_score()
            metrics (Dict[str, Any]): Raw metrics from analyze() for detailed recommendations

        Returns:
            List[str]: List of recommendation strings

        Example:
            ```python
            [
                "Reduce AI vocabulary from 5.2 to <1.0 per 1k words",
                "Replace 'delve' with: explore, examine, investigate"
            ]
            ```
        """
        pass

    @abstractmethod
    def get_tiers(self) -> Dict[str, Tuple[float, float]]:
        """
        Define score tier ranges for interpretation.

        Returns:
            Dict[str, Tuple[float, float]]: Dict mapping tier name to (min_score, max_score) range

        Standard tiers:
            ```python
            {
                'excellent': (90.0, 100.0),
                'good': (75.0, 89.9),
                'acceptable': (50.0, 74.9),
                'poor': (0.0, 49.9)
            }
            ```
        """
        pass

    # ========================================================================
    # CONCRETE METHODS - Optional override in subclasses
    # ========================================================================

    def get_impact_level(self, score: float) -> str:
        """
        Calculate impact level based on score gap from 100 (perfect).

        Default implementation uses these thresholds:
        - gap < 5:  "NONE"   (95-100: minimal impact)
        - gap < 15: "LOW"    (85-94: low impact)
        - gap < 30: "MEDIUM" (70-84: medium impact)
        - gap >= 30: "HIGH"  (0-69: high impact)

        Subclasses may override for custom thresholds (e.g., performance-critical dimensions
        may use stricter thresholds).

        Args:
            score (float): The score to evaluate (0-100)

        Returns:
            str: One of "NONE", "LOW", "MEDIUM", or "HIGH"
        """
        gap = self._calculate_gap(score)

        if gap < 5:
            return "NONE"
        elif gap < 15:
            return "LOW"
        elif gap < 30:
            return "MEDIUM"
        else:
            return "HIGH"

    def analyze_detailed(
        self, lines: List[str], html_comment_checker=None
    ) -> List[Any]:
        """
        Optional detailed analysis with line-by-line findings.

        Default implementation returns empty list. Override in subclasses
        to provide detailed reporting mode for CLI detailed output.

        Args:
            lines (List[str]): Text split into lines
            html_comment_checker: Optional HTML comment checker for filtering

        Returns:
            List[Any]: List of issue objects (VocabInstance, SentenceBurstinessIssue, etc.)
                      Default: empty list

        Example override:
            ```python
            def analyze_detailed(self, lines, html_comment_checker=None):
                issues = []
                for line_num, line in enumerate(lines, start=1):
                    # Detailed line-by-line analysis
                    if self._has_issue(line):
                        issues.append(IssueObject(line_number=line_num, ...))
                return issues
            ```
        """
        return []

    # ========================================================================
    # BACKWARD COMPATIBILITY METHODS
    # ========================================================================

    def score(self, analysis_results: Dict[str, Any]) -> Tuple[float, str]:
        """
        Legacy compatibility wrapper for old base class interface.

        DO NOT override this method - override calculate_score() instead.
        This method wraps calculate_score() and maps to tier label for
        backward compatibility with existing code expecting the old signature.

        Args:
            analysis_results (Dict[str, Any]): Results from analyze()

        Returns:
            Tuple[float, str]: (score_value, score_label)
                score_value: float score 0-100
                score_label: tier label string (e.g., "EXCELLENT", "GOOD")
        """
        score_value = self.calculate_score(analysis_results)
        tier_label = self._map_score_to_tier(score_value)
        return (score_value, tier_label)

    def get_max_score(self) -> float:
        """
        Get maximum possible score for this dimension.

        Deprecated: All dimensions now use 0-100 scale.
        This method always returns 100.0 for backward compatibility.

        Returns:
            float: Always 100.0
        """
        return 100.0

    def get_dimension_name(self) -> str:
        """
        Get the name of this dimension.

        Deprecated: Use dimension_name property instead.
        This method reads the dimension_name property for backward compatibility.

        Returns:
            str: Dimension name from dimension_name property
        """
        return self.dimension_name

    # ========================================================================
    # AST HELPER METHODS (from existing base.py)
    # ========================================================================

    def _get_markdown_parser(self) -> Markdown:
        """
        Lazy-load marko parser singleton.

        Returns:
            Markdown: marko.Markdown instance

        Usage:
            ```python
            parser = self._get_markdown_parser()
            ```
        """
        if self._markdown_parser is None:
            self._markdown_parser = Markdown()
        return self._markdown_parser

    def _parse_to_ast(self, text: str, cache_key: Optional[str] = None) -> Any:
        """
        Parse markdown to AST with caching.

        Args:
            text (str): Markdown text to parse
            cache_key (Optional[str]): Optional cache key for reusing parsed AST

        Returns:
            Any: Parsed AST node or None if parsing fails

        Usage:
            ```python
            ast = self._parse_to_ast(text, cache_key='main')
            ```
        """
        if cache_key and cache_key in self._ast_cache:
            return self._ast_cache[cache_key]

        parser = self._get_markdown_parser()
        if parser is None:
            return None

        try:
            ast = parser.parse(text)
            if cache_key:
                self._ast_cache[cache_key] = ast
            return ast
        except Exception:
            return None

    def _walk_ast(self, node, node_type=None) -> List:
        """
        Recursively traverse AST for nodes of specified type.

        Args:
            node: AST node to walk
            node_type: Optional type to filter (e.g., marko.block.Quote)

        Returns:
            List: List of nodes matching node_type, or all nodes if node_type is None

        Usage:
            ```python
            from marko.block import Quote
            quotes = self._walk_ast(ast, Quote)
            ```
        """
        nodes = []

        if node_type is None or isinstance(node, node_type):
            nodes.append(node)

        # Recursively process children
        if hasattr(node, 'children') and node.children:
            for child in node.children:
                nodes.extend(self._walk_ast(child, node_type))

        return nodes

    def _extract_text_from_node(self, node) -> str:
        """
        Extract plain text from AST node recursively.

        Args:
            node: AST node to extract text from

        Returns:
            str: Plain text string

        Usage:
            ```python
            text = self._extract_text_from_node(heading_node)
            ```
        """
        if hasattr(node, 'children') and node.children:
            return ''.join([
                self._extract_text_from_node(child) for child in node.children
            ])
        elif hasattr(node, 'children') and isinstance(node.children, str):
            return node.children
        elif hasattr(node, 'dest'):  # Link destination
            return ''
        elif isinstance(node, str):
            return node
        else:
            return ''

    # ========================================================================
    # CONFIGURATION HELPER METHODS
    # ========================================================================

    def _prepare_text(
        self,
        text: str,
        config: Optional[AnalysisConfig] = None,
        dimension_name: str = None
    ) -> Union[str, List[Tuple[int, str]]]:
        """
        Prepare text based on configuration.

        Args:
            text: Full text content
            config: Analysis configuration (None = default behavior)
            dimension_name: Name of calling dimension (for override lookup)

        Returns:
            Either:
            - str: Truncated/full text (for direct analysis)
            - List[Tuple[int, str]]: List of (position, sample_text) for sampling

        Algorithm:
            1. If config is None, use DEFAULT_CONFIG
            2. Get effective limit from config.get_effective_limit()
            3. If limit is not None, return text[:limit]
            4. If should_use_sampling() returns True, return config.extract_samples(text)
            5. Otherwise return full text

        Example:
            # FAST mode - returns truncated string
            prepared = self._prepare_text(text, config, "predictability")
            # Result: "First 2000 chars..."

            # SAMPLING mode - returns list of samples
            prepared = self._prepare_text(text, config, "predictability")
            # Result: [(0, "sample1"), (36000, "sample2"), ...]
        """
        config = config or DEFAULT_CONFIG

        # Get effective character limit for this dimension
        effective_limit = config.get_effective_limit(
            dimension_name or self.dimension_name,
            len(text)
        )

        # If we have a limit, truncate and return string
        if effective_limit is not None:
            return text[:effective_limit]

        # Check if sampling should be used
        if config.should_use_sampling(len(text)):
            # Return list of samples for sampled analysis
            return config.extract_samples(text)

        # No limit and no sampling - return full text
        return text

    def _aggregate_sampled_metrics(
        self,
        sample_metrics: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Aggregate metrics from multiple samples.

        Args:
            sample_metrics: List of metric dicts from analyzing each sample

        Returns:
            Single aggregated metric dict

        Algorithm:
            For each metric key across all samples:
            - Numeric values (int, float): Calculate mean
            - Boolean values: Use majority vote (True if >50% are True)
            - String values: Use most common value (mode)
            - List values: Concatenate all lists (deduplicate if needed)
            - Dict values: Merge dicts (use first value for conflicts)
            - None values: Ignore in aggregation

        Example:
            samples = [
                {'score': 85, 'ai_vocab': ['delve'], 'has_issue': True},
                {'score': 90, 'ai_vocab': ['robust'], 'has_issue': False},
                {'score': 88, 'ai_vocab': ['leverage'], 'has_issue': False}
            ]
            result = self._aggregate_sampled_metrics(samples)
            # Result: {
            #   'score': 87.67,  # mean of [85, 90, 88]
            #   'ai_vocab': ['delve', 'robust', 'leverage'],  # concatenated
            #   'has_issue': False  # majority vote (1 True, 2 False)
            # }
        """
        if not sample_metrics:
            return {}

        # Collect all keys across all samples
        all_keys = set()
        for sample in sample_metrics:
            all_keys.update(sample.keys())

        aggregated = {}

        for key in all_keys:
            # Collect all values for this key (skip None)
            values = [sample[key] for sample in sample_metrics if key in sample and sample[key] is not None]

            if not values:
                aggregated[key] = None
                continue

            # Determine type and aggregate appropriately
            first_value = values[0]

            if isinstance(first_value, (int, float)) and not isinstance(first_value, bool):
                # Numeric: Calculate mean (check bool first since bool is subclass of int)
                aggregated[key] = sum(values) / len(values)

            elif isinstance(first_value, bool):
                # Boolean: Majority vote
                true_count = sum(1 for v in values if v)
                aggregated[key] = true_count > len(values) / 2

            elif isinstance(first_value, str):
                # String: Most common value (mode)
                counter = Counter(values)
                aggregated[key] = counter.most_common(1)[0][0]

            elif isinstance(first_value, list):
                # List: Concatenate and deduplicate (preserve order)
                combined = []
                seen = set()
                for v in values:
                    for item in v:
                        # Handle unhashable items (dicts, lists)
                        item_key = str(item) if not isinstance(item, (str, int, float, bool, tuple)) else item
                        if item_key not in seen:
                            combined.append(item)
                            seen.add(item_key)
                aggregated[key] = combined

            elif isinstance(first_value, dict):
                # Dict: Recursively aggregate nested dicts
                # Collect all keys across all nested dicts
                all_nested_keys = set()
                for v in values:
                    if isinstance(v, dict):
                        all_nested_keys.update(v.keys())

                merged = {}
                for nested_key in all_nested_keys:
                    # Collect values for this nested key across all samples
                    nested_values = [
                        v[nested_key] for v in values
                        if isinstance(v, dict) and nested_key in v and v[nested_key] is not None
                    ]

                    if not nested_values:
                        merged[nested_key] = None
                        continue

                    # Determine type and aggregate
                    first_nested = nested_values[0]

                    if isinstance(first_nested, (int, float)) and not isinstance(first_nested, bool):
                        # Numeric: Average across samples
                        merged[nested_key] = sum(nested_values) / len(nested_values)
                    elif isinstance(first_nested, bool):
                        # Boolean: Majority vote
                        true_count = sum(1 for v in nested_values if v)
                        merged[nested_key] = true_count > len(nested_values) / 2
                    elif isinstance(first_nested, str):
                        # String: Most common value
                        counter = Counter(nested_values)
                        merged[nested_key] = counter.most_common(1)[0][0]
                    elif isinstance(first_nested, list):
                        # List: Concatenate and deduplicate
                        combined_nested = []
                        seen_nested = set()
                        for nv in nested_values:
                            for item in nv:
                                item_key = str(item) if not isinstance(item, (str, int, float, bool, tuple)) else item
                                if item_key not in seen_nested:
                                    combined_nested.append(item)
                                    seen_nested.add(item_key)
                        merged[nested_key] = combined_nested
                    elif isinstance(first_nested, dict):
                        # Recursively handle deeply nested dicts (recursive call)
                        merged[nested_key] = self._aggregate_sampled_metrics([{'nested': v} for v in nested_values])['nested']
                    else:
                        # Unknown type: Use first value
                        merged[nested_key] = first_nested

                aggregated[key] = merged

            else:
                # Unknown type: Use first value
                aggregated[key] = first_value

        return aggregated

    # ========================================================================
    # VALIDATION HELPER METHODS
    # ========================================================================

    def _validate_tier(self) -> None:
        """
        Validate tier property value.

        Raises:
            ValueError: If tier is not a valid DimensionTier

        Usage:
            Call in __init__ after setting tier:
            ```python
            def __init__(self):
                super().__init__()
                self._validate_tier()
            ```
        """
        if not isinstance(self.tier, DimensionTier):
            valid_tiers = [t.value for t in DimensionTier]
            raise ValueError(
                f"tier must be one of {valid_tiers}, got: {self.tier}"
            )

    def _validate_score(self, score: float) -> None:
        """
        Validate score is in 0-100 range.

        Args:
            score (float): Score to validate

        Raises:
            ValueError: If score is outside 0-100 range

        Usage:
            Call in calculate_score() before returning:
            ```python
            def calculate_score(self, metrics):
                score = 85.0
                self._validate_score(score)
                return score
            ```
        """
        if not (0.0 <= score <= 100.0):
            raise ValueError(
                f"score must be between 0.0 and 100.0, got: {score}"
            )

    def _validate_weight(self, weight: float) -> None:
        """
        Validate weight is in 0-100 range.

        Args:
            weight (float): Weight to validate

        Raises:
            ValueError: If weight is outside 0-100 range

        Usage:
            Call in __init__ after setting weight:
            ```python
            def __init__(self):
                super().__init__()
                self._validate_weight(self.weight)
            ```
        """
        if not (0.0 <= weight <= 100.0):
            raise ValueError(
                f"weight must be between 0.0 and 100.0, got: {weight}"
            )

    @staticmethod
    def _calculate_gap(score: float) -> float:
        """
        Calculate gap from perfect score (100).

        Args:
            score (float): Score value (0-100)

        Returns:
            float: Gap from 100 (i.e., 100.0 - score)

        Usage:
            ```python
            gap = self._calculate_gap(score)
            ```
        """
        return 100.0 - score

    def _map_score_to_tier(self, score: float) -> str:
        """
        Map score to tier label using get_tiers().

        Args:
            score (float): Score value (0-100)

        Returns:
            str: Tier label string (e.g., "EXCELLENT", "GOOD")

        Usage:
            Called internally by score() method.
        """
        tiers = self.get_tiers()

        for tier_name, (min_score, max_score) in tiers.items():
            if min_score <= score <= max_score:
                return tier_name.upper()

        # Fallback if no tier matches (shouldn't happen with proper tier definitions)
        return "UNKNOWN"

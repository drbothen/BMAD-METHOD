"""
Tests for SyntacticAnalyzer - syntactic complexity and structure patterns.
"""

import pytest
from ai_pattern_analyzer.dimensions.syntactic import SyntacticAnalyzer
from ai_pattern_analyzer.core.dimension_registry import DimensionRegistry

# All dependencies are now required
HAS_SPACY = True


@pytest.fixture
def analyzer():
    """Create SyntacticAnalyzer instance."""
    # Clear registry before each test to avoid duplicate registration errors
    DimensionRegistry.clear()
    return SyntacticAnalyzer()


@pytest.fixture
def text_complex_syntax():
    """Text with complex syntactic structures (human pattern)."""
    return """# Introduction

When examining the evidence, researchers discovered that participants who engaged
with the material demonstrated improved comprehension, which suggests that active
learning strategies, while requiring additional effort, produce measurable benefits
across diverse educational contexts.

Although initial results appeared modest, subsequent analysis revealed patterns
that challenged conventional assumptions about cognitive processing."""


@pytest.fixture
def text_simple_syntax():
    """Text with simple syntactic structures (AI pattern)."""
    return """# Overview

The system is effective. It provides value. The approach works well. Results
are positive. The method is useful. The framework is robust. Implementation
is straightforward. Performance is good. Outcomes are favorable."""


@pytest.fixture
def text_passive_voice():
    """Text with passive voice constructions."""
    return """# Results

The data was analyzed by the team. Findings were documented carefully.
Patterns were identified in the results. Conclusions were drawn from the evidence."""


class TestAnalyzeSyntacticPatterns:
    """Tests for _analyze_syntactic_patterns method (requires spaCy)."""

    def test_syntactic_patterns_basic(self, analyzer, text_complex_syntax):
        """Test basic syntactic analysis."""
        result = analyzer._analyze_syntactic_patterns(text_complex_syntax)

        assert 'available' in result
        assert result['available'] is True
        assert 'syntactic_repetition_score' in result
        assert 'pos_diversity' in result
        assert 'avg_dependency_depth' in result
        assert 'avg_tree_depth' in result
        assert 'subordination_index' in result
        assert 'passive_constructions' in result
        assert 'morphological_richness' in result

    def test_syntactic_patterns_complex_text(self, analyzer, text_complex_syntax):
        """Test complex syntax detection (human pattern)."""
        result = analyzer._analyze_syntactic_patterns(text_complex_syntax)

        # Complex text should have:
        # - Higher dependency depth (4-6 for human)
        # - Higher subordination index (>0.15 for human)
        # - Lower syntactic repetition
        assert result['avg_dependency_depth'] >= 3.0
        assert result['subordination_index'] >= 0.1
        assert result['syntactic_repetition_score'] < 0.8

    def test_syntactic_patterns_simple_text(self, analyzer, text_simple_syntax):
        """Test simple syntax detection (AI pattern)."""
        result = analyzer._analyze_syntactic_patterns(text_simple_syntax)

        # Simple text should have:
        # - Lower dependency depth (2-3 for AI)
        # - Higher syntactic repetition
        assert result['avg_dependency_depth'] < 5.0
        assert result['syntactic_repetition_score'] > 0.0

    def test_syntactic_patterns_passive_voice(self, analyzer, text_passive_voice):
        """Test passive voice detection."""
        result = analyzer._analyze_syntactic_patterns(text_passive_voice)

        # Should detect passive constructions
        assert result['passive_constructions'] > 0

    def test_syntactic_patterns_excludes_code(self, analyzer):
        """Test that code blocks are excluded from analysis."""
        text = """# Example

Normal text here with complex subordinate clauses when needed.

```python
def function():
    return value
```

More text after the code block."""
        result = analyzer._analyze_syntactic_patterns(text)

        # Should analyze non-code text
        assert result['available'] is True

    def test_syntactic_patterns_empty_text(self, analyzer):
        """Test syntactic analysis on empty text."""
        result = analyzer._analyze_syntactic_patterns("")

        assert result['available'] is False

    def test_syntactic_patterns_pos_diversity(self, analyzer, text_complex_syntax):
        """Test POS diversity calculation."""
        result = analyzer._analyze_syntactic_patterns(text_complex_syntax)

        # Should have POS diversity metric
        assert 0 <= result['pos_diversity'] <= 1

    def test_syntactic_patterns_morphological_richness(self, analyzer, text_complex_syntax):
        """Test morphological richness calculation."""
        result = analyzer._analyze_syntactic_patterns(text_complex_syntax)

        # Should have morphological richness (unique lemmas)
        assert result['morphological_richness'] > 0


class TestAnalyzeSyntacticPatternsNoSpacy:
    """Tests for _analyze_syntactic_patterns without spaCy."""

    @pytest.mark.skipif(HAS_SPACY, reason="Test requires spaCy to be unavailable")
    def test_syntactic_patterns_no_spacy(self, analyzer):
        """Test syntactic analysis without spaCy available."""
        result = analyzer._analyze_syntactic_patterns("Some text here.")

        assert 'available' in result
        assert result['available'] is False


class TestAnalyzeSyntacticIssuesDetailed:
    """Tests for _analyze_syntactic_issues_detailed method (requires spaCy)."""

    def test_syntactic_issues_passive_detection(self, analyzer, text_passive_voice):
        """Test detection of passive voice constructions."""
        lines = text_passive_voice.split('\n')
        issues = analyzer._analyze_syntactic_issues_detailed(lines)

        assert isinstance(issues, list)
        # Should detect passive voice issues
        passive_issues = [i for i in issues if i.issue_type == 'passive']
        assert len(passive_issues) > 0

        # Check issue structure
        if passive_issues:
            issue = passive_issues[0]
            assert hasattr(issue, 'line_number')
            assert hasattr(issue, 'sentence')
            assert hasattr(issue, 'issue_type')
            assert hasattr(issue, 'metric_value')
            assert hasattr(issue, 'problem')
            assert hasattr(issue, 'suggestion')

    def test_syntactic_issues_shallow_detection(self, analyzer):
        """Test detection of shallow dependency trees."""
        lines = [
            "The cat sat. The dog ran. The bird flew. The fish swam."
        ]
        issues = analyzer._analyze_syntactic_issues_detailed(lines)

        # May detect shallow syntax in simple sentences
        assert isinstance(issues, list)

    def test_syntactic_issues_subordination_detection(self, analyzer):
        """Test detection of low subordination."""
        lines = [
            "The system works well. It provides good results. Users are satisfied."
        ]
        issues = analyzer._analyze_syntactic_issues_detailed(lines)

        # May detect lack of subordinate clauses
        assert isinstance(issues, list)

    def test_syntactic_issues_skips_headings(self, analyzer):
        """Test that headings are skipped."""
        lines = [
            "# This is a heading with passive voice that was written",
            "This sentence was written with passive voice."
        ]
        issues = analyzer._analyze_syntactic_issues_detailed(lines)

        # Should only detect passive in body text (line 2), not heading
        if issues:
            assert all(i.line_number == 2 for i in issues)

    def test_syntactic_issues_skips_code_blocks(self, analyzer):
        """Test that code block markers are skipped."""
        lines = [
            "```python",
            "def function():",
            "```",
            "This sentence was written with passive voice."
        ]
        issues = analyzer._analyze_syntactic_issues_detailed(lines)

        # Should only analyze body text
        assert isinstance(issues, list)

    def test_syntactic_issues_html_comment_checker(self, analyzer):
        """Test HTML comment checking."""
        lines = [
            "<!-- This comment has passive voice that was written -->",
            "This sentence was written with passive voice."
        ]

    def is_in_comment(line):
        return line.strip().startswith('<!--')

        issues = analyzer._analyze_syntactic_issues_detailed(lines, is_in_comment)

        # Should only analyze non-comment lines
        if issues:
            assert all(i.line_number == 2 for i in issues)

    def test_syntactic_issues_context_truncation(self, analyzer):
        """Test that long sentences are truncated."""
        long_sentence = "The data was " + "analyzed and processed " * 20 + "by the research team."
        lines = [long_sentence]
        issues = analyzer._analyze_syntactic_issues_detailed(lines)

        # Should truncate long sentences
        if issues:
            assert len(issues[0].sentence) <= 103  # 100 + "..."


class TestAnalyzeSyntacticIssuesNoSpacy:
    """Tests for _analyze_syntactic_issues_detailed without spaCy."""

    @pytest.mark.skipif(HAS_SPACY, reason="Test requires spaCy to be unavailable")
    def test_syntactic_issues_no_spacy(self, analyzer):
        """Test syntactic issues analysis without spaCy available."""
        lines = ["Some text here with complex structures."]
        issues = analyzer._analyze_syntactic_issues_detailed(lines)

        assert isinstance(issues, list)
        assert len(issues) == 0


class TestAnalyze:
    """Tests for main analyze method."""

    def test_analyze_basic(self, analyzer, text_complex_syntax):
        """Test basic analyze method."""
        result = analyzer.analyze(text_complex_syntax)

        assert 'syntactic' in result
        assert isinstance(result['syntactic'], dict)

    def test_analyze_empty_text(self, analyzer):
        """Test analyze on empty text."""
        result = analyzer.analyze("")

        assert result['syntactic']['available'] is False

    @pytest.mark.skipif(HAS_SPACY, reason="Test requires spaCy to be unavailable")
    def test_analyze_no_spacy(self, analyzer):
        """Test analyze without spaCy available."""
        result = analyzer.analyze("Some text here.")

        assert result['syntactic']['available'] is False


class TestAnalyzeDetailed:
    """Tests for analyze_detailed method."""

    def test_analyze_detailed_basic(self, analyzer, text_passive_voice):
        """Test detailed analysis method."""
        lines = text_passive_voice.split('\n')
        result = analyzer.analyze_detailed(lines)

        assert isinstance(result, list)


class TestScore:
    """Tests for score method."""

    def test_score_high_variation(self, analyzer):
        """Test score for high syntactic variation (low repetition)."""
        analysis = {'syntactic': True, 'syntactic_repetition_score': 0.2}  # <= 0.3 threshold
        score, label = analyzer.score(analysis)

        assert score == 10.0
        assert label == "HIGH"

    def test_score_medium_variation(self, analyzer):
        """Test score for medium syntactic variation."""
        analysis = {'syntactic': True, 'syntactic_repetition_score': 0.4}  # <= 0.5 threshold
        score, label = analyzer.score(analysis)

        assert score == 7.0
        assert label == "MEDIUM"

    def test_score_low_variation(self, analyzer):
        """Test score for low syntactic variation."""
        analysis = {'syntactic': True, 'syntactic_repetition_score': 0.6}  # <= 0.7 threshold
        score, label = analyzer.score(analysis)

        assert score == 4.0
        assert label == "LOW"

    def test_score_very_low_variation(self, analyzer):
        """Test score for very low variation (high repetition - AI pattern)."""
        analysis = {'syntactic': True, 'syntactic_repetition_score': 0.8}  # > 0.7 threshold
        score, label = analyzer.score(analysis)

        assert score == 2.0
        assert label == "VERY LOW"

    def test_score_no_syntactic_data(self, analyzer):
        """Test score without syntactic data."""
        analysis = {}
        score, label = analyzer.score(analysis)

        assert score == 5.0
        assert label == "UNKNOWN"


class TestIntegration:
    """Integration tests (requires spaCy)."""

    def test_full_analysis_pipeline(self, analyzer, text_complex_syntax):
        """Test complete analysis pipeline."""
        result = analyzer.analyze(text_complex_syntax)

        assert result['syntactic']['available'] is True
        assert result['syntactic']['syntactic_repetition_score'] >= 0

        # Detailed analysis
        lines = text_complex_syntax.split('\n')
        detailed = analyzer.analyze_detailed(lines)

        assert isinstance(detailed, list)

    def test_comparison_complex_vs_simple(self, analyzer, text_complex_syntax, text_simple_syntax):
        """Test that analyzer distinguishes complex from simple syntax."""
        complex_result = analyzer.analyze(text_complex_syntax)
        simple_result = analyzer.analyze(text_simple_syntax)

        complex_depth = complex_result['syntactic']['avg_dependency_depth']
        simple_depth = simple_result['syntactic']['avg_dependency_depth']

        # Complex text should have deeper dependency trees
        assert complex_depth > simple_depth

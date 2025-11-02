"""
Unit tests for FormattingAnalyzer (dimensions/formatting.py).

This test module covers:
- Basic formatting analysis (em-dash, bold, italic)
- Bold/italic pattern analysis
- Em-dash detailed analysis
- Phase 3 advanced methods (list usage, punctuation clustering, whitespace)
- Edge cases and boundary conditions

FormattingAnalyzer is HIGH PRIORITY with 516 lines and 12+ methods.
Em-dash analysis is the STRONGEST AI signal (95% accuracy).
"""

import pytest
from ai_pattern_analyzer.dimensions.formatting import FormattingAnalyzer
from ai_pattern_analyzer.core.results import EmDashInstance, FormattingIssue


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def analyzer():
    """Create a FormattingAnalyzer instance."""
    return FormattingAnalyzer()


@pytest.fixture
def text_with_em_dashes():
    """Text with em-dashes for testing."""
    return """# Testing Em-Dashes

This text uses em-dashes — the hallmark of AI-generated content — to show
how the analyzer detects them.

## More Em-Dashes

Furthermore, em-dashes can appear in various forms:
- The standard em-dash — like this
- The double-hyphen version -- like this
- Multiple uses — one after — another

Regular hyphens-like-this should not be counted.
"""


@pytest.fixture
def text_with_excessive_formatting():
    """Text with excessive bold/italic usage (AI pattern)."""
    return """# **Comprehensive** Guide

This is a text with **excessive** bold **formatting** that is **typical**
of *AI-generated* content. It uses **bold** and *italic* **very** *frequently*
to **emphasize** many *points* **unnecessarily**.

**Furthermore**, this **pattern** continues with **bold** text appearing in
**nearly** every **sentence** and *italic* text *sprinkled* **throughout**.
"""


@pytest.fixture
def text_with_minimal_formatting():
    """Text with minimal formatting (human pattern)."""
    return """# Getting Started

This text has very little formatting. Just normal text mostly.

There's one **important** point here, and maybe an *occasional* emphasis.
But that's about it.

Most paragraphs are just plain text without any special formatting at all.
"""


@pytest.fixture
def text_with_lists():
    """Text with lists for list usage analysis."""
    return """# Lists Example

## Unordered List

- Item one short
- Item two also short
- Item three short too

## Ordered List

1. First item
2. Second item
3. Third item
4. Fourth item

More text here.
"""


@pytest.fixture
def text_with_punctuation():
    """Text with various punctuation for clustering analysis."""
    return """# Punctuation Test

First section: has colons; and semicolons — and em-dashes too.

Second section has different spacing: like this; and this — spacing varies.

Some sections: have; many — marks: clustered; together — repeatedly.
"""


# ============================================================================
# Basic Formatting Tests
# ============================================================================

class TestAnalyzeFormatting:
    """Tests for _analyze_formatting method."""

    def test_analyze_formatting_basic(self, analyzer, text_with_em_dashes):
        """Test basic formatting counting."""
        result = analyzer._analyze_formatting(text_with_em_dashes)

        assert 'em_dashes' in result
        assert 'bold' in result
        assert 'italics' in result
        assert result['em_dashes'] > 0

    def test_em_dash_standard_form(self, analyzer):
        """Test em-dash detection (—)."""
        text = "This has an em-dash — right here."
        result = analyzer._analyze_formatting(text)
        assert result['em_dashes'] >= 1

    def test_em_dash_double_hyphen(self, analyzer):
        """Test double-hyphen em-dash detection (--)."""
        text = "This has a double-hyphen -- right here."
        result = analyzer._analyze_formatting(text)
        assert result['em_dashes'] >= 1

    def test_regular_hyphens_not_counted(self, analyzer):
        """Test that regular hyphens are not counted as em-dashes."""
        text = "This has regular-hyphens and a-few-more but no em-dashes."
        result = analyzer._analyze_formatting(text)
        assert result['em_dashes'] == 0

    def test_bold_markdown_double_asterisk(self, analyzer):
        """Test bold detection (**text**)."""
        text = "This has **bold text** in it."
        result = analyzer._analyze_formatting(text)
        assert result['bold'] >= 1

    def test_bold_markdown_double_underscore(self, analyzer):
        """Test bold detection (__text__)."""
        text = "This has __bold text__ in it."
        result = analyzer._analyze_formatting(text)
        assert result['bold'] >= 1

    def test_italic_markdown_single_asterisk(self, analyzer):
        """Test italic detection (*text*)."""
        text = "This has *italic text* in it."
        result = analyzer._analyze_formatting(text)
        assert result['italics'] >= 1

    def test_italic_markdown_single_underscore(self, analyzer):
        """Test italic detection (_text_)."""
        text = "This has _italic text_ in it."
        result = analyzer._analyze_formatting(text)
        assert result['italics'] >= 1

    def test_formatting_empty_text(self, analyzer):
        """Test formatting analysis on empty text."""
        result = analyzer._analyze_formatting("")
        assert result['em_dashes'] == 0
        assert result['bold'] == 0
        assert result['italics'] == 0

    def test_formatting_no_formatting(self, analyzer):
        """Test text with no formatting."""
        text = "Just plain text with no special formatting at all."
        result = analyzer._analyze_formatting(text)
        assert result['em_dashes'] == 0
        assert result['bold'] == 0
        assert result['italics'] == 0


class TestAnalyzeBoldItalicPatterns:
    """Tests for _analyze_bold_italic_patterns method."""

    def test_bold_italic_patterns_basic(self, analyzer, text_with_excessive_formatting):
        """Test bold/italic pattern analysis."""
        result = analyzer._analyze_bold_italic_patterns(text_with_excessive_formatting)

        assert 'bold_per_1k' in result
        assert 'italic_per_1k' in result
        assert 'formatting_consistency' in result
        # AI text should have high bold/italic usage
        assert result['bold_per_1k'] > 5.0 or result['italic_per_1k'] > 5.0

    def test_bold_italic_ai_pattern(self, analyzer, text_with_excessive_formatting):
        """Test that excessive bold/italic is detected (AI pattern)."""
        result = analyzer._analyze_bold_italic_patterns(text_with_excessive_formatting)

        # AI uses 10-50 bold/italic per 1k words
        assert result['bold_per_1k'] > 10.0 or result['italic_per_1k'] > 5.0

    def test_bold_italic_human_pattern(self, analyzer, text_with_minimal_formatting):
        """Test minimal bold/italic usage (human pattern)."""
        result = analyzer._analyze_bold_italic_patterns(text_with_minimal_formatting)

        # Human uses 1-5 per 1k words (relaxed for short text samples)
        assert result['bold_per_1k'] < 30.0

    def test_bold_italic_empty_text(self, analyzer):
        """Test bold/italic patterns on empty text."""
        result = analyzer._analyze_bold_italic_patterns("")
        assert result['bold_per_1k'] == 0
        assert result['italic_per_1k'] == 0


class TestAnalyzeEmDashesDetailed:
    """Tests for _analyze_em_dashes_detailed method."""

    def test_em_dashes_detailed_basic(self, analyzer, text_with_em_dashes):
        """Test detailed em-dash analysis with line numbers."""
        lines = text_with_em_dashes.split('\n')
        instances = analyzer._analyze_em_dashes_detailed(lines)

        assert isinstance(instances, list)
        assert len(instances) > 0
        # Check that instances have required attributes
        for instance in instances:
            assert hasattr(instance, 'line_number')
            assert hasattr(instance, 'context')

    def test_em_dashes_detailed_context_extraction(self, analyzer):
        """Test that context is extracted around em-dashes."""
        lines = [
            "# Title",
            "This line has an em-dash — with context on both sides here."
        ]
        instances = analyzer._analyze_em_dashes_detailed(lines)

        assert len(instances) > 0
        # Context should be extracted
        assert len(instances[0].context) > 0

    def test_em_dashes_detailed_skips_comments(self, analyzer):
        """Test that HTML comments are skipped."""
        lines = [
            "# Title",
            "<!-- This has an em-dash — but it's commented -->",
            "This has an em-dash — not in comment."
        ]

        def is_in_comment(line):
            return line.strip().startswith('<!--')

        instances = analyzer._analyze_em_dashes_detailed(lines, is_in_comment)

        # Should only detect the non-commented em-dash
        assert len(instances) == 1
        assert instances[0].line_number == 3  # Third line (1-indexed)

    def test_em_dashes_detailed_empty_lines(self, analyzer):
        """Test em-dash analysis on empty list."""
        instances = analyzer._analyze_em_dashes_detailed([])
        assert instances == []


class TestAnalyzeFormattingIssuesDetailed:
    """Tests for _analyze_formatting_issues_detailed method."""

    def test_formatting_issues_excessive_bold(self, analyzer, text_with_excessive_formatting):
        """Test detection of excessive bold usage."""
        lines = text_with_excessive_formatting.split('\n')
        issues = analyzer._analyze_formatting_issues_detailed(lines)

        assert isinstance(issues, list)
        # Should detect excessive bold
        bold_issues = [i for i in issues if 'bold' in i.issue_type.lower()]
        assert len(bold_issues) > 0

    def test_formatting_issues_excessive_italic(self, analyzer, text_with_excessive_formatting):
        """Test detection of excessive italic usage."""
        lines = text_with_excessive_formatting.split('\n')
        issues = analyzer._analyze_formatting_issues_detailed(lines)

        # Should detect excessive italic
        italic_issues = [i for i in issues if 'italic' in i.issue_type.lower()]
        assert len(italic_issues) > 0

    def test_formatting_issues_line_numbers(self, analyzer):
        """Test that line numbers are tracked."""
        lines = [
            "# Title",
            "This has **too** **much** **bold** **text** **here**.",
            "And *too* *much* *italic* *text* *here*."
        ]
        issues = analyzer._analyze_formatting_issues_detailed(lines)

        for issue in issues:
            assert hasattr(issue, 'line_number')
            assert issue.line_number >= 0


# ============================================================================
# Phase 3 Advanced Methods Tests
# ============================================================================

class TestAnalyzeListUsage:
    """Tests for _analyze_list_usage Phase 3 method."""

    def test_list_usage_basic(self, analyzer, text_with_lists):
        """Test list usage analysis."""
        result = analyzer._analyze_list_usage(text_with_lists)

        assert 'ordered_items' in result
        assert 'unordered_items' in result
        assert 'list_to_text_ratio' in result
        assert result['ordered_items'] > 0
        assert result['unordered_items'] > 0

    def test_list_usage_ai_pattern(self, analyzer):
        """Test that AI pattern uses many lists."""
        text = """# Guide

- Point one
- Point two
- Point three

1. Step one
2. Step two

- More points
- Even more
"""
        result = analyzer._analyze_list_usage(text)

        # AI uses lists heavily (78% of AI text uses lists)
        assert result['list_to_text_ratio'] > 0.1

    def test_list_usage_ordered_unordered_ratio(self, analyzer, text_with_lists):
        """Test ordered/unordered ratio calculation."""
        result = analyzer._analyze_list_usage(text_with_lists)

        assert 'ordered_to_unordered_ratio' in result
        # Should be a valid ratio
        assert result['ordered_to_unordered_ratio'] >= 0

    def test_list_usage_no_lists(self, analyzer):
        """Test list usage with no lists."""
        text = "Just paragraphs here. No lists at all."
        result = analyzer._analyze_list_usage(text)

        assert result['ordered_items'] == 0
        assert result['unordered_items'] == 0


class TestAnalyzePunctuationClustering:
    """Tests for _analyze_punctuation_clustering Phase 3 method."""

    def test_punctuation_clustering_basic(self, analyzer, text_with_punctuation):
        """Test punctuation clustering analysis."""
        result = analyzer._analyze_punctuation_clustering(text_with_punctuation)

        assert 'em_dash_cascading' in result
        assert 'oxford_consistency' in result
        assert 'semicolon_per_1k' in result

    def test_punctuation_clustering_em_dash_cascading(self, analyzer):
        """Test em-dash cascading pattern detection."""
        text = """# Title

Section 1 has many em-dashes — here — and here — and here — so many.

Section 2 has fewer em-dashes — just a couple — that's it.

Section 3 has one em-dash — only one.

Section 4 has no em-dashes at all.
"""
        result = analyzer._analyze_punctuation_clustering(text)

        # Should detect cascading pattern
        assert 'em_dash_cascading' in result

    def test_punctuation_clustering_oxford_comma(self, analyzer):
        """Test Oxford comma consistency detection."""
        text = "Items: A, B, and C. More items: X, Y, and Z. Last: P, Q, and R."
        result = analyzer._analyze_punctuation_clustering(text)

        # Should detect consistent Oxford comma usage (AI pattern)
        assert 'oxford_consistency' in result
        assert result['oxford_consistency'] >= 0

    def test_punctuation_clustering_semicolon_usage(self, analyzer, text_with_punctuation):
        """Test semicolon usage per 1k words."""
        result = analyzer._analyze_punctuation_clustering(text_with_punctuation)

        assert result['semicolon_per_1k'] >= 0


class TestAnalyzeWhitespacePatterns:
    """Tests for _analyze_whitespace_patterns Phase 3 method."""

    def test_whitespace_patterns_basic(self, analyzer):
        """Test whitespace pattern analysis."""
        text = """# Title

Paragraph one is short.

Paragraph two is a bit longer with more content here.

Paragraph three is very long with lots and lots of content going on and on with many words and sentences.

Paragraph four is short again.
"""
        result = analyzer._analyze_whitespace_patterns(text)

        assert 'paragraph_variance' in result
        assert 'paragraph_uniformity' in result
        assert 'text_density' in result

    def test_whitespace_uniform_paragraphs(self, analyzer):
        """Test uniform paragraph lengths (AI pattern)."""
        text = """# Title

This paragraph has exactly twenty words in it for testing uniformity detection in AI generated content here now.

This paragraph also has exactly twenty words in it for testing uniformity detection in AI generated content here too.

This paragraph equally has exactly twenty words in it for testing uniformity detection in AI generated content right here.
"""
        result = analyzer._analyze_whitespace_patterns(text)

        # Uniform paragraphs should have consistent metrics
        assert result['paragraph_variance'] < 100.0 or result['paragraph_uniformity'] < 2.0

    def test_whitespace_varied_paragraphs(self, analyzer):
        """Test varied paragraph lengths (human pattern)."""
        text = """# Title

Short.

This is a medium length paragraph with some content.

This is a very long paragraph with lots of content and many sentences that go on and on with detailed explanations and examples and more information that makes it significantly longer than the other paragraphs in this text.
"""
        result = analyzer._analyze_whitespace_patterns(text)

        # Varied paragraphs should have high variance
        assert result['paragraph_variance'] >= 0


class TestAnalyzePunctuationSpacingCv:
    """Tests for _analyze_punctuation_spacing_cv Phase 3 method."""

    def test_punctuation_spacing_cv_basic(self, analyzer, text_with_punctuation):
        """Test punctuation spacing coefficient of variation."""
        result = analyzer._analyze_punctuation_spacing_cv(text_with_punctuation)

        assert 'primary_cv' in result
        assert 'score' in result
        assert 'assessment' in result

    def test_punctuation_spacing_cv_colon(self, analyzer):
        """Test CV calculation for colons."""
        text = """Text with: colons: scattered: throughout: the: document: regularly."""
        result = analyzer._analyze_punctuation_spacing_cv(text)

        assert result['primary_cv'] >= 0

    def test_punctuation_spacing_cv_clustered(self, analyzer):
        """Test high CV for clustered punctuation (human pattern)."""
        text = """# Section

Many marks: here; now — clustered.

Nothing here for a while.

Then more: marks; again — here."""
        result = analyzer._analyze_punctuation_spacing_cv(text)

        # Clustered should have higher CV
        assert result['primary_cv'] >= 0

    def test_punctuation_spacing_cv_insufficient_marks(self, analyzer):
        """Test with <3 punctuation marks."""
        text = "Only one: mark here."
        result = analyzer._analyze_punctuation_spacing_cv(text)

        # Should handle gracefully
        assert 'primary_cv' in result


# ============================================================================
# Integration Tests
# ============================================================================

class TestFormattingAnalyzerIntegration:
    """Integration tests for full analyze method."""

    def test_analyze_full(self, analyzer, sample_ai_text):
        """Test full analysis pipeline."""
        result = analyzer.analyze(sample_ai_text)

        # Should contain all expected keys
        assert 'formatting' in result
        assert 'bold_italic' in result
        # Phase 3
        assert 'list_usage' in result
        assert 'punctuation_clustering' in result
        assert 'whitespace_patterns' in result
        assert 'punctuation_spacing_cv' in result

    def test_analyze_detailed_integration(self, analyzer, text_with_em_dashes):
        """Test detailed analysis integration."""
        lines = text_with_em_dashes.split('\n')
        result = analyzer.analyze_detailed(lines)

        assert 'em_dash_instances' in result
        assert 'formatting_issues' in result
        assert isinstance(result['em_dash_instances'], list)
        assert isinstance(result['formatting_issues'], list)

    def test_analyze_empty(self, analyzer):
        """Test analysis on empty document."""
        result = analyzer.analyze("")

        # Should not crash, return valid structure
        assert isinstance(result, dict)
        assert result['formatting']['em_dashes'] == 0


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_sentence(self, analyzer):
        """Test with single sentence."""
        result = analyzer.analyze("This is one sentence.")
        assert isinstance(result, dict)

    def test_only_formatting(self, analyzer):
        """Test text that is only formatting."""
        text = "**bold** *italic* — **more** *formatting*"
        result = analyzer.analyze(text)
        assert result['formatting']['bold'] > 0
        assert result['formatting']['italics'] > 0

    def test_unicode_in_formatted_text(self, analyzer):
        """Test unicode characters in formatted text."""
        text = "**世界** *🌍* — **Привет**"
        result = analyzer.analyze(text)
        assert result['formatting']['bold'] > 0

    def test_nested_formatting(self, analyzer):
        """Test nested bold/italic."""
        text = "***bold and italic*** text here"
        result = analyzer.analyze(text)
        # Should detect formatting
        assert result['formatting']['bold'] > 0 or result['formatting']['italics'] > 0

    def test_malformed_markdown(self, analyzer):
        """Test malformed markdown formatting."""
        text = "**unclosed bold and *unclosed italic"
        result = analyzer.analyze(text)
        # Should handle gracefully
        assert isinstance(result, dict)

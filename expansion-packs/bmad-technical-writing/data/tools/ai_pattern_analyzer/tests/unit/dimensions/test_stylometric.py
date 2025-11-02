"""
Tests for StylometricAnalyzer - readability and style metrics.
"""

import pytest
from ai_pattern_analyzer.dimensions.stylometric import StylometricAnalyzer


@pytest.fixture
def analyzer():
    """Create StylometricAnalyzer instance."""
    return StylometricAnalyzer()


@pytest.fixture
def text_with_however():
    """Text with 'however' markers."""
    return """# Introduction

This approach works well. However, there are some limitations to consider.
The method is effective. However, the implementation requires careful planning.
"""


@pytest.fixture
def text_with_moreover():
    """Text with 'moreover' markers."""
    return """# Overview

The system provides benefits. Moreover, it offers improved performance.
Results are promising. Moreover, the approach scales effectively.
"""


@pytest.fixture
def text_clean():
    """Text without stylometric markers."""
    return """# Getting Started

This is a simple text. It has basic sentences. Nothing fancy here.
Just straightforward writing without AI markers.
"""


class TestAnalyzeStylometricPatterns:
    """Tests for _analyze_stylometric_patterns method."""

    def test_stylometric_patterns_basic(self, analyzer):
        """Test basic stylometric analysis."""
        text = "This is a test sentence. It has multiple words."
        result = analyzer._analyze_stylometric_patterns(text)

        assert 'avg_word_length' in result
        assert 'avg_sentence_length' in result
        assert isinstance(result['avg_word_length'], float)
        assert isinstance(result['avg_sentence_length'], float)

    def test_stylometric_patterns_with_textstat(self, analyzer):
        """Test stylometric analysis with textstat if available."""
        text = "This is a test sentence. It has multiple words and demonstrates readability."
        result = analyzer._analyze_stylometric_patterns(text)

        # If textstat is available, should have these metrics
        # If not, they won't be present (gracefully handled)
        assert 'avg_word_length' in result
        assert 'avg_sentence_length' in result

    def test_stylometric_patterns_empty_text(self, analyzer):
        """Test stylometric analysis on empty text."""
        result = analyzer._analyze_stylometric_patterns("")

        assert result['avg_word_length'] == 0.0
        assert result['avg_sentence_length'] == 0.0


class TestAnalyzeStylometricIssuesDetailed:
    """Tests for _analyze_stylometric_issues_detailed method."""

    def test_issues_however_detection(self, analyzer, text_with_however):
        """Test detection of 'however' markers."""
        lines = text_with_however.split('\n')
        issues = analyzer._analyze_stylometric_issues_detailed(lines)

        assert isinstance(issues, list)
        # Should detect "however" instances
        however_issues = [i for i in issues if i.marker_type in ['however', 'however_cluster']]
        assert len(however_issues) > 0

    def test_issues_moreover_detection(self, analyzer, text_with_moreover):
        """Test detection of 'moreover' markers."""
        lines = text_with_moreover.split('\n')
        issues = analyzer._analyze_stylometric_issues_detailed(lines)

        assert isinstance(issues, list)
        # Should detect "moreover" instances
        moreover_issues = [i for i in issues if i.marker_type == 'moreover']
        assert len(moreover_issues) > 0

    def test_issues_clean_text(self, analyzer, text_clean):
        """Test that clean text has no issues."""
        lines = text_clean.split('\n')
        issues = analyzer._analyze_stylometric_issues_detailed(lines)

        assert isinstance(issues, list)
        assert len(issues) == 0

    def test_issues_skips_headings(self, analyzer):
        """Test that headings are skipped."""
        lines = [
            "# However, this is a heading",
            "This however appears in body text."
        ]
        issues = analyzer._analyze_stylometric_issues_detailed(lines)

        # Should only detect body text "however" (line 2)
        assert all(i.line_number == 2 for i in issues if i.marker_type == 'however')

    def test_issues_cluster_detection(self, analyzer):
        """Test detection of clustered 'however' usage."""
        lines = [
            "First sentence however has a marker.",
            "Second sentence also however contains one.",
            "Third sentence however joins in too."
        ]
        issues = analyzer._analyze_stylometric_issues_detailed(lines)

        # Should detect individual instances plus clusters
        cluster_issues = [i for i in issues if i.marker_type == 'however_cluster']
        assert len(cluster_issues) > 0

    def test_issues_context_truncation(self, analyzer):
        """Test that long context is truncated."""
        long_line = "However, " + "x " * 100  # Very long line
        lines = [long_line]
        issues = analyzer._analyze_stylometric_issues_detailed(lines)

        if len(issues) > 0:
            assert len(issues[0].context) <= 123  # 120 + "..."


class TestAnalyze:
    """Tests for main analyze method."""

    def test_analyze_basic(self, analyzer, text_clean):
        """Test basic analyze method."""
        result = analyzer.analyze(text_clean)

        assert 'stylometric' in result
        assert isinstance(result['stylometric'], dict)

    def test_analyze_empty_text(self, analyzer):
        """Test analyze on empty text."""
        result = analyzer.analyze("")

        assert result['stylometric']['avg_word_length'] == 0.0


class TestAnalyzeDetailed:
    """Tests for analyze_detailed method."""

    def test_analyze_detailed_basic(self, analyzer, text_with_however):
        """Test detailed analysis method."""
        lines = text_with_however.split('\n')
        result = analyzer.analyze_detailed(lines)

        assert isinstance(result, list)


class TestScore:
    """Tests for score method."""

    def test_score_placeholder(self, analyzer):
        """Test score method (currently placeholder)."""
        analysis = {}
        score, label = analyzer.score(analysis)

        # Current implementation is placeholder
        assert score == 7.0
        assert label == "MEDIUM"


class TestIntegration:
    """Integration tests."""

    def test_full_analysis_pipeline(self, analyzer, text_with_however):
        """Test complete analysis pipeline."""
        result = analyzer.analyze(text_with_however)

        assert 'stylometric' in result

        # Detailed analysis
        lines = text_with_however.split('\n')
        detailed = analyzer.analyze_detailed(lines)

        assert isinstance(detailed, list)
        assert len(detailed) > 0  # Should detect "however" instances

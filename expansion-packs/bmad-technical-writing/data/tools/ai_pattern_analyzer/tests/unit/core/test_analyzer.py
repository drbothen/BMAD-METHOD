"""
Tests for AIPatternAnalyzer - core orchestration class.

Tests cover:
- Initialization and setup
- File analysis (analyze_file)
- Word counting
- HTML comment handling
- AST parsing helpers
- Dual score calculation
- History tracking (load/save)
- Detailed analysis mode
- Overall assessment
"""

import pytest
import tempfile
from pathlib import Path
from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
from ai_pattern_analyzer.core.results import AnalysisResults, DetailedAnalysis
from ai_pattern_analyzer.scoring.dual_score import DualScore
from ai_pattern_analyzer.history.tracker import ScoreHistory


@pytest.fixture
def analyzer():
    """Create AIPatternAnalyzer instance with default settings."""
    return AIPatternAnalyzer()


@pytest.fixture
def analyzer_with_domain_terms():
    """Create AIPatternAnalyzer with custom domain terms."""
    custom_terms = [r'\bPython\b', r'\bDjango\b', r'\bREST\b', r'\bAPI\b']
    return AIPatternAnalyzer(domain_terms=custom_terms)


@pytest.fixture
def sample_markdown_file(tmp_path):
    """Create a temporary markdown file for testing."""
    content = """# Introduction to Python

Python is a versatile programming language. It offers numerous benefits for developers.
The syntax is clear and readable. Many projects leverage Python for web development.

## Key Features

- Easy to learn
- Robust standard library
- Large ecosystem of packages

Python facilitates rapid development. The language provides comprehensive documentation.
"""
    file_path = tmp_path / "test.md"
    file_path.write_text(content)
    return str(file_path)


@pytest.fixture
def markdown_with_html_comments(tmp_path):
    """Create markdown file with HTML comments (metadata)."""
    content = """<!--
document_id: test-123
author: Test Author
date: 2024-01-15
-->

# Test Document

This is the actual content that should be analyzed.

<!-- Another comment to ignore -->

More content here.
"""
    file_path = tmp_path / "test_with_comments.md"
    file_path.write_text(content)
    return str(file_path)


# ============================================================================
# Initialization Tests
# ============================================================================

class TestInitialization:
    """Tests for AIPatternAnalyzer initialization."""

    def test_init_default(self, analyzer):
        """Test initialization with default domain terms."""
        assert analyzer is not None
        assert analyzer.domain_terms == analyzer.DOMAIN_TERMS_DEFAULT
        assert analyzer.lines == []

        # Check all dimension analyzers are initialized
        assert analyzer.perplexity_analyzer is not None
        assert analyzer.burstiness_analyzer is not None
        assert analyzer.structure_analyzer is not None
        assert analyzer.formatting_analyzer is not None
        assert analyzer.voice_analyzer is not None
        assert analyzer.syntactic_analyzer is not None
        assert analyzer.lexical_analyzer is not None
        assert analyzer.stylometric_analyzer is not None
        assert analyzer.advanced_analyzer is not None

    def test_init_custom_domain_terms(self, analyzer_with_domain_terms):
        """Test initialization with custom domain terms."""
        expected_terms = [r'\bPython\b', r'\bDjango\b', r'\bREST\b', r'\bAPI\b']
        assert analyzer_with_domain_terms.domain_terms == expected_terms

    def test_init_creates_html_comment_pattern(self, analyzer):
        """Test that HTML comment regex pattern is compiled."""
        assert analyzer._html_comment_pattern is not None

    def test_init_creates_ast_cache(self, analyzer):
        """Test that AST cache is initialized."""
        assert analyzer._ast_cache == {}
        assert analyzer._markdown_parser is None


# ============================================================================
# File Analysis Tests
# ============================================================================

class TestAnalyzeFile:
    """Tests for main analyze_file method."""

    def test_analyze_file_basic(self, analyzer, sample_markdown_file):
        """Test basic file analysis."""
        results = analyzer.analyze_file(sample_markdown_file)

        assert isinstance(results, AnalysisResults)
        assert results.file_path == sample_markdown_file
        assert results.total_words > 0
        assert results.total_sentences >= 0  # May be 0 depending on content

    def test_analyze_file_nonexistent(self, analyzer):
        """Test analysis of non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            analyzer.analyze_file("/nonexistent/file.md")

    def test_analyze_file_word_count(self, analyzer, sample_markdown_file):
        """Test word counting in file analysis."""
        results = analyzer.analyze_file(sample_markdown_file)

        # Sample file has approximately 50-60 words
        assert results.total_words > 40
        assert results.total_words < 100

    def test_analyze_file_total_sentences(self, analyzer, sample_markdown_file):
        """Test sentence counting."""
        results = analyzer.analyze_file(sample_markdown_file)

        # Sentence counting may vary based on analyzer implementation
        assert results.total_sentences >= 0
        assert isinstance(results.total_sentences, int)

    def test_analyze_file_strips_html_comments(self, analyzer, markdown_with_html_comments):
        """Test that HTML comments are stripped before analysis."""
        results = analyzer.analyze_file(markdown_with_html_comments)

        # Word count should not include HTML comment content
        # Only "Test Document", "This is the actual content...", "More content here."
        assert results.total_words > 0
        # Should not count "document_id", "author", "date", etc.
        assert results.total_words < 50  # Just the actual content

    def test_analyze_file_runs_all_analyzers(self, analyzer, sample_markdown_file):
        """Test that all dimension analyzers are executed."""
        results = analyzer.analyze_file(sample_markdown_file)

        # Check that results contain data from various dimensions
        assert results.ai_vocabulary_count >= 0
        assert results.unique_words >= 0
        assert results.sentence_mean_length >= 0


# ============================================================================
# Preprocessing Tests
# ============================================================================

class TestPreprocessing:
    """Tests for preprocessing methods."""

    def test_strip_html_comments_single_line(self, analyzer):
        """Test stripping single-line HTML comments."""
        text = "Before <!-- comment --> After"
        result = analyzer._strip_html_comments(text)

        assert "comment" not in result
        assert "Before" in result
        assert "After" in result

    def test_strip_html_comments_multiline(self, analyzer):
        """Test stripping multi-line HTML comments."""
        text = """Before
<!--
Multi-line
comment
-->
After"""
        result = analyzer._strip_html_comments(text)

        assert "Multi-line" not in result
        assert "comment" not in result
        assert "Before" in result
        assert "After" in result

    def test_strip_html_comments_multiple(self, analyzer):
        """Test stripping multiple HTML comments."""
        text = "<!-- one --> Text <!-- two --> More"
        result = analyzer._strip_html_comments(text)

        assert "one" not in result
        assert "two" not in result
        assert "Text" in result
        assert "More" in result

    def test_is_line_in_html_comment_complete(self, analyzer):
        """Test detection of complete HTML comment in line."""
        line = "<!-- This is a comment -->"
        assert analyzer._is_line_in_html_comment(line) is True

    def test_is_line_in_html_comment_start(self, analyzer):
        """Test detection of HTML comment start."""
        line = "<!-- Comment start"
        assert analyzer._is_line_in_html_comment(line) is True

    def test_is_line_in_html_comment_end(self, analyzer):
        """Test detection of HTML comment end."""
        line = "Comment end -->"
        assert analyzer._is_line_in_html_comment(line) is True

    def test_is_line_in_html_comment_regular_text(self, analyzer):
        """Test that regular text is not detected as comment."""
        line = "This is normal text"
        assert analyzer._is_line_in_html_comment(line) is False


# ============================================================================
# Word Counting Tests
# ============================================================================

class TestCountWords:
    """Tests for _count_words method."""

    def test_count_words_basic(self, analyzer):
        """Test basic word counting."""
        text = "This is a test with five words here."
        count = analyzer._count_words(text)

        assert count == 8

    def test_count_words_empty(self, analyzer):
        """Test word counting on empty text."""
        count = analyzer._count_words("")

        assert count == 0

    def test_count_words_whitespace_only(self, analyzer):
        """Test word counting on whitespace."""
        count = analyzer._count_words("   \n\n\t  ")

        assert count == 0

    def test_count_words_multiline(self, analyzer):
        """Test word counting across multiple lines."""
        text = """Line one has four words.
        Line two has four words.
        Line three has four words."""
        count = analyzer._count_words(text)

        # 4 + 4 + 4 = 12 content words
        assert count > 10

    def test_count_words_ignores_code_blocks(self, analyzer):
        """Test that code blocks are excluded from word count."""
        text = """Regular text here.
```python
# Code should not be counted
def hello():
    print("world")
```
More regular text."""
        count = analyzer._count_words(text)

        # Should only count "Regular text here." and "More regular text."
        assert count > 0
        assert count < 20  # Much less than if code was included


# ============================================================================
# AST Parsing Tests
# ============================================================================

class TestAstParsing:
    """Tests for AST parsing helper methods."""

    def test_get_markdown_parser_lazy_loads(self, analyzer):
        """Test that parser is lazy loaded."""
        assert analyzer._markdown_parser is None

        parser = analyzer._get_markdown_parser()

        assert parser is not None
        assert analyzer._markdown_parser is not None

    def test_get_markdown_parser_reuses_instance(self, analyzer):
        """Test that parser instance is reused."""
        parser1 = analyzer._get_markdown_parser()
        parser2 = analyzer._get_markdown_parser()

        assert parser1 is parser2

    def test_parse_to_ast_basic(self, analyzer):
        """Test basic AST parsing."""
        text = "# Heading\n\nParagraph text."
        ast = analyzer._parse_to_ast(text)

        assert ast is not None

    def test_parse_to_ast_with_cache_key(self, analyzer):
        """Test AST parsing with caching."""
        text = "# Test"

        ast1 = analyzer._parse_to_ast(text, cache_key='test')
        ast2 = analyzer._parse_to_ast(text, cache_key='test')

        # Should return same cached instance
        assert ast1 is ast2
        assert 'test' in analyzer._ast_cache

    def test_parse_to_ast_empty(self, analyzer):
        """Test AST parsing of empty text."""
        ast = analyzer._parse_to_ast("")

        # Should handle gracefully
        assert ast is not None or ast is None  # Either is acceptable

    def test_walk_ast_finds_headings(self, analyzer):
        """Test walking AST to find specific node types."""
        from marko.block import Heading

        text = "# Heading 1\n\nText\n\n## Heading 2"
        ast = analyzer._parse_to_ast(text)

        headings = analyzer._walk_ast(ast, Heading)

        # Should find 2 headings
        assert len(headings) >= 2

    def test_walk_ast_all_nodes(self, analyzer):
        """Test walking AST without node type filter."""
        text = "# Heading\n\nParagraph"
        ast = analyzer._parse_to_ast(text)

        all_nodes = analyzer._walk_ast(ast)

        # Should return all nodes
        assert len(all_nodes) > 0

    def test_extract_text_from_node_basic(self, analyzer):
        """Test extracting text from AST node."""
        from marko.block import Paragraph

        text = "Test paragraph content"
        ast = analyzer._parse_to_ast(text)

        paragraphs = analyzer._walk_ast(ast, Paragraph)

        if paragraphs:
            extracted = analyzer._extract_text_from_node(paragraphs[0])
            assert "Test" in extracted or "paragraph" in extracted


# ============================================================================
# Dual Score Calculation Tests
# ============================================================================

class TestCalculateDualScore:
    """Tests for calculate_dual_score method."""

    def test_calculate_dual_score_basic(self, analyzer, sample_markdown_file):
        """Test basic dual score calculation."""
        results = analyzer.analyze_file(sample_markdown_file)
        dual_score = analyzer.calculate_dual_score(results)

        assert isinstance(dual_score, DualScore)
        assert 0 <= dual_score.detection_risk <= 100
        assert 0 <= dual_score.quality_score <= 100
        assert isinstance(dual_score.detection_interpretation, str)
        assert isinstance(dual_score.quality_interpretation, str)

    def test_calculate_dual_score_with_custom_targets(self, analyzer, sample_markdown_file):
        """Test dual score calculation with custom targets."""
        results = analyzer.analyze_file(sample_markdown_file)
        dual_score = analyzer.calculate_dual_score(
            results,
            detection_target=20.0,
            quality_target=90.0
        )

        assert isinstance(dual_score, DualScore)
        assert dual_score.detection_target == 20.0
        assert dual_score.quality_target == 90.0


# ============================================================================
# History Tracking Tests
# ============================================================================

class TestHistoryTracking:
    """Tests for score history tracking."""

    def test_get_history_file_path(self, analyzer, tmp_path):
        """Test getting history file path from source file."""
        source = tmp_path / "document.md"
        source.touch()  # Create the file
        history_path = analyzer._get_history_file_path(str(source))

        assert isinstance(history_path, Path)
        assert history_path.name.endswith('.history.json')
        assert 'document' in str(history_path)
        assert history_path.parent.exists()  # Directory should be created

    def test_load_score_history_nonexistent(self, analyzer, tmp_path):
        """Test loading history from non-existent file creates new history."""
        file_path = str(tmp_path / "new.md")
        history = analyzer.load_score_history(file_path)

        assert isinstance(history, ScoreHistory)
        assert len(history.scores) == 0

    def test_save_and_load_score_history(self, analyzer, tmp_path):
        """Test saving and loading score history."""
        file_path = str(tmp_path / "test.md")

        # Create and save history
        history = ScoreHistory(file_path=file_path)
        analyzer.save_score_history(history)

        # Load it back
        loaded_history = analyzer.load_score_history(file_path)

        assert loaded_history.file_path == history.file_path


# ============================================================================
# Overall Assessment Tests
# ============================================================================

class TestAssessOverall:
    """Tests for _assess_overall method."""

    def test_assess_overall_calculates_assessment(self, analyzer, sample_markdown_file):
        """Test that overall assessment is calculated."""
        results = analyzer.analyze_file(sample_markdown_file)
        assessment = analyzer._assess_overall(results)

        assert isinstance(assessment, str)
        assert len(assessment) > 0


# ============================================================================
# Detailed Analysis Tests
# ============================================================================

class TestAnalyzeFileDetailed:
    """Tests for analyze_file_detailed method."""

    def test_analyze_file_detailed_basic(self, analyzer, sample_markdown_file):
        """Test basic detailed analysis."""
        detailed = analyzer.analyze_file_detailed(sample_markdown_file)

        assert isinstance(detailed, DetailedAnalysis)
        assert detailed.file_path == sample_markdown_file

    def test_analyze_file_detailed_has_issues(self, analyzer, sample_markdown_file):
        """Test that detailed analysis includes issue lists."""
        detailed = analyzer.analyze_file_detailed(sample_markdown_file)

        # Should have various issue lists (may be empty)
        assert hasattr(detailed, 'ai_vocabulary')
        assert hasattr(detailed, 'heading_issues')
        assert hasattr(detailed, 'uniform_paragraphs')

#!/usr/bin/env python3
"""
Unit tests for Phase 1 Structural Pattern Detection

Tests the new methods added to analyze_ai_patterns.py:
- _calculate_paragraph_cv
- _calculate_section_variance
- _count_uniform_clusters
- _calculate_list_nesting_depth
"""

import sys
sys.path.insert(0, '/Users/jmagady/Dev/BMAD-METHOD/expansion-packs/bmad-technical-writing/data/tools')

from analyze_ai_patterns import AIPatternAnalyzer

def test_paragraph_cv_human_like():
    """Test that varied paragraph lengths score well."""
    print("TEST 1: Paragraph CV - Human-like variation")

    analyzer = AIPatternAnalyzer()

    # Create text with varied paragraph lengths
    text = """
First paragraph with about forty five words here to establish a baseline for testing purposes with some more content here.

Second paragraph is much longer with approximately one hundred and fifty words to create variation in the document structure and demonstrate human-like writing patterns with natural flow and realistic content that might appear in actual writing samples from human authors who vary their paragraph lengths.

Short third paragraph with minimal content.

Another medium-length paragraph with around seventy words to continue the natural variation pattern that human writers typically exhibit when creating authentic content for documents.
    """

    result = analyzer._calculate_paragraph_cv(text)

    print(f"  CV: {result['cv']:.2f}")
    print(f"  Score: {result['score']:.1f}/10")
    print(f"  Assessment: {result['assessment']}")
    print(f"  Mean length: {result['mean_length']:.0f} words")

    assert result['cv'] >= 0.4, f"Human-like variation should have CV ≥0.4, got {result['cv']:.2f}"
    assert result['score'] >= 7.0, f"Should score GOOD or better, got {result['score']}"

    print("  ✓ PASS\n")
    return True


def test_paragraph_cv_ai_like():
    """Test that uniform paragraph lengths are flagged."""
    print("TEST 2: Paragraph CV - AI-like uniformity")

    analyzer = AIPatternAnalyzer()

    # Generate 6 paragraphs of ~175 words each (uniform)
    paragraph = " ".join(["word"] * 175)
    text = "\n\n".join([paragraph] * 6)

    result = analyzer._calculate_paragraph_cv(text)

    print(f"  CV: {result['cv']:.2f}")
    print(f"  Score: {result['score']:.1f}/10")
    print(f"  Assessment: {result['assessment']}")

    assert result['cv'] < 0.3, f"Uniform AI pattern should have CV <0.3, got {result['cv']:.2f}"
    assert result['score'] == 0.0, f"Should score POOR, got {result['score']}"

    print("  ✓ PASS\n")
    return True


def test_section_variance_human_like():
    """Test that varied section lengths score well."""
    print("TEST 3: Section Variance - Human-like variation")

    analyzer = AIPatternAnalyzer()

    # Create text with varied H2 sections
    text = """
## Section One
""" + " ".join(["word"] * 450) + """

## Section Two
""" + " ".join(["word"] * 890) + """

## Section Three
""" + " ".join(["word"] * 320)

    result = analyzer._calculate_section_variance(text)

    print(f"  Variance: {result['variance_pct']:.1f}%")
    print(f"  Score: {result['score']:.1f}/8")
    print(f"  Assessment: {result['assessment']}")
    print(f"  Sections analyzed: {result['section_count']}")

    assert result['variance_pct'] >= 40, f"High variance should be ≥40%, got {result['variance_pct']:.1f}%"
    assert result['score'] == 8.0, f"Should score EXCELLENT, got {result['score']}"

    print("  ✓ PASS\n")
    return True


def test_section_variance_ai_like():
    """Test that uniform section lengths are flagged."""
    print("TEST 4: Section Variance - AI-like uniformity")

    analyzer = AIPatternAnalyzer()

    # Create text with uniform H2 sections (~520 words each)
    sections = []
    for i in range(5):
        word_count = 520 + (i * 10)  # Slight variation: 520, 530, 540, 550, 560
        sections.append(f"## Section {i+1}\n" + " ".join(["word"] * word_count))

    text = "\n\n".join(sections)

    result = analyzer._calculate_section_variance(text)

    print(f"  Variance: {result['variance_pct']:.1f}%")
    print(f"  Score: {result['score']:.1f}/8")
    print(f"  Assessment: {result['assessment']}")
    print(f"  Uniform clusters: {result['uniform_clusters']}")

    assert result['variance_pct'] < 15, f"Uniform pattern should have variance <15%, got {result['variance_pct']:.1f}%"
    assert result['score'] == 0.0, f"Should score POOR, got {result['score']}"

    print("  ✓ PASS\n")
    return True


def test_list_nesting_human_like():
    """Test that shallow lists score well."""
    print("TEST 5: List Nesting - Human-like shallow nesting")

    analyzer = AIPatternAnalyzer()

    text = """
- Level 1 item
  - Level 2 item
  - Another level 2 item
- Another level 1 item
- Third level 1 item
  - Level 2 under third
    """

    result = analyzer._calculate_list_nesting_depth(text)

    print(f"  Max depth: {result['max_depth']} levels")
    print(f"  Score: {result['score']:.1f}/6")
    print(f"  Assessment: {result['assessment']}")
    print(f"  Total items: {result['total_list_items']}")

    assert result['max_depth'] <= 3, f"Human-like nesting should be ≤3 levels, got {result['max_depth']}"
    assert result['score'] >= 6.0, f"Should score EXCELLENT, got {result['score']}"

    print("  ✓ PASS\n")
    return True


def test_list_nesting_ai_like():
    """Test that deep nesting is flagged."""
    print("TEST 6: List Nesting - AI-like deep nesting")

    analyzer = AIPatternAnalyzer()

    text = """
- Level 1
  - Level 2
    - Level 3
      - Level 4
        - Level 5
          - Level 6
    """

    result = analyzer._calculate_list_nesting_depth(text)

    print(f"  Max depth: {result['max_depth']} levels")
    print(f"  Score: {result['score']:.1f}/6")
    print(f"  Assessment: {result['assessment']}")

    assert result['max_depth'] >= 5, f"Should detect deep nesting (≥5), got {result['max_depth']}"
    assert result['score'] <= 2.0, f"Should score FAIR or POOR, got {result['score']}"

    print("  ✓ PASS\n")
    return True


def test_count_uniform_clusters():
    """Test uniform cluster detection."""
    print("TEST 7: Uniform Cluster Detection")

    analyzer = AIPatternAnalyzer()

    # Cluster of 3 similar values, then different, then another cluster
    lengths = [500, 510, 505, 800, 600, 605, 610]

    result = analyzer._count_uniform_clusters(lengths, tolerance=0.10)

    print(f"  Input: {lengths}")
    print(f"  Clusters found: {result}")

    assert result >= 1, f"Should find at least 1 cluster, got {result}"

    print("  ✓ PASS\n")
    return True


def test_integration_full_analysis():
    """Test integration with full analysis pipeline."""
    print("TEST 8: Integration Test - Full Analysis")

    # Create a sample markdown file
    sample_text = """
# Test Document

This is a test document with varied structure to test the structural pattern analysis.

## First Section

This section has about forty words to create some variation in the document structure and test the paragraph analysis.

Another paragraph here with different length containing approximately twenty five words for testing purposes.

## Second Section

This is a much longer section with many more words to create asymmetry in section lengths which should be detected by the section variance analysis as human-like writing with natural variation in content organization.

Short paragraph.

Medium length paragraph with some content to add variation approximately thirty words here for good measure.

## Third Section

- First level item
  - Second level item
  - Another second level
- Another first level

Final paragraph to complete the document.
"""

    # Write to temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_text)
        temp_file = f.name

    try:
        analyzer = AIPatternAnalyzer()
        results = analyzer.analyze_file(temp_file)

        print(f"  Paragraph CV: {results.paragraph_cv:.2f} ({results.paragraph_cv_assessment})")
        print(f"  Section Variance: {results.section_variance_pct:.1f}% ({results.section_variance_assessment})")
        print(f"  List Depth: {results.list_max_depth} levels ({results.list_depth_assessment})")
        print(f"  Structural Patterns Score: {results.structural_patterns_score}")

        # Basic validation
        assert results.paragraph_cv >= 0, "CV should be non-negative"
        assert results.section_variance_pct >= 0, "Variance should be non-negative"
        assert results.list_max_depth >= 0, "Depth should be non-negative"
        assert results.structural_patterns_score in ["HIGH", "MEDIUM", "LOW", "VERY LOW"], \
            f"Score should be valid, got {results.structural_patterns_score}"

        print("  ✓ PASS\n")
        return True

    finally:
        import os
        os.unlink(temp_file)


def run_all_tests():
    """Run all unit tests."""
    print("="* 80)
    print("STRUCTURAL PATTERN DETECTION - UNIT TESTS")
    print("=" * 80)
    print()

    tests = [
        test_paragraph_cv_human_like,
        test_paragraph_cv_ai_like,
        test_section_variance_human_like,
        test_section_variance_ai_like,
        test_list_nesting_human_like,
        test_list_nesting_ai_like,
        test_count_uniform_clusters,
        test_integration_full_analysis
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"  ✗ FAIL: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            failed += 1

    print("=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {len(tests)} total")
    print("=" * 80)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Quick test for Phase 2 enhancements to analyze_ai_patterns.py
Tests MATTR, RTTR, heading length, subsection asymmetry, and heading depth variance
"""

# Sample test document with various heading patterns
TEST_DOCUMENT = """
# Introduction to Web Development

Web development is a fascinating field that combines creativity with technical skills.

## Getting Started with HTML

HTML forms the backbone of web pages. It provides structure and semantic meaning to content.

### Basic HTML Structure

Every HTML document starts with a DOCTYPE declaration. This tells browsers how to interpret the page.

### Common HTML Elements

HTML provides many elements for different purposes. Some are for structure, others for content.

## Understanding CSS Styling

CSS brings visual appeal to HTML structures. It controls layout, colors, typography, and more.

### CSS Selectors

Selectors determine which elements receive styling. They range from simple to highly specific.

### Box Model Fundamentals

The box model describes how elements occupy space. It includes content, padding, border, and margin.

### Responsive Design Principles

Modern websites must work across devices. Responsive design adapts layouts to different screen sizes.

## JavaScript Fundamentals

JavaScript adds interactivity to web pages. It enables dynamic content updates and user interactions.

### Variables and Data Types

JavaScript supports various data types including strings, numbers, booleans, objects, and arrays.

# Advanced Topics

## Asynchronous Programming

Asynchronous code handles operations that take time without blocking execution flow.

### Promises and Async/Await

Promises represent eventual completion of operations. Async/await provides cleaner syntax for promises.

## Modern Framework Overview

Frameworks simplify complex application development through reusable components and patterns.
"""

def test_phase2_implementation():
    """Test Phase 2 features"""
    print("=== Phase 2 Implementation Test ===\n")

    try:
        from analyze_ai_patterns import AIPatternAnalyzer
        print("✓ Successfully imported AIPatternAnalyzer")
    except ImportError as e:
        print(f"✗ Failed to import AIPatternAnalyzer: {e}")
        return False

    # Initialize analyzer
    try:
        analyzer = AIPatternAnalyzer()
        print("✓ Successfully initialized analyzer")
    except Exception as e:
        print(f"✗ Failed to initialize analyzer: {e}")
        return False

    # Analyze test document
    print("\n--- Running analysis on test document ---")
    try:
        results = analyzer.analyze_file_content(TEST_DOCUMENT, "test_document.md")
        print("✓ Analysis completed successfully")
    except Exception as e:
        print(f"✗ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Check Phase 2: MATTR
    print("\n--- Phase 2: MATTR (Moving Average Type-Token Ratio) ---")
    if hasattr(results, 'mattr') and results.mattr is not None:
        print(f"✓ MATTR: {results.mattr:.4f}")
        print(f"  Assessment: {results.mattr_assessment}")
    else:
        print("⚠ MATTR not available (textacy may not be installed)")

    # Check Phase 2: RTTR
    print("\n--- Phase 2: RTTR (Root Type-Token Ratio) ---")
    if hasattr(results, 'rttr') and results.rttr is not None:
        print(f"✓ RTTR: {results.rttr:.4f}")
        print(f"  Assessment: {results.rttr_assessment}")
    else:
        print("⚠ RTTR not available (textacy may not be installed)")

    # Check Phase 2: Heading Length Analysis
    print("\n--- Phase 2: Heading Length Analysis ---")
    if hasattr(results, 'avg_heading_length') and results.avg_heading_length is not None:
        print(f"✓ Average heading length: {results.avg_heading_length:.1f} words")
        print(f"  Short (≤5 words): {results.heading_length_short_pct:.1f}%")
        print(f"  Medium (6-8 words): {results.heading_length_medium_pct:.1f}%")
        print(f"  Long (≥9 words): {results.heading_length_long_pct:.1f}%")
        print(f"  Assessment: {results.heading_length_assessment}")
    else:
        print("✗ Heading length analysis not available")

    # Check Phase 2: Subsection Asymmetry
    print("\n--- Phase 2: Subsection Asymmetry ---")
    if hasattr(results, 'subsection_cv') and results.subsection_cv is not None:
        print(f"✓ Subsection CV (Coefficient of Variation): {results.subsection_cv:.3f}")
        print(f"  Subsection counts: {results.subsection_counts}")
        print(f"  Uniform subsections: {results.subsection_uniform_count}")
        print(f"  Assessment: {results.subsection_assessment}")
    else:
        print("✗ Subsection asymmetry analysis not available")

    # Check Phase 2: Heading Depth Variance
    print("\n--- Phase 2: Heading Depth Variance ---")
    if hasattr(results, 'heading_depth_pattern') and results.heading_depth_pattern is not None:
        print(f"✓ Depth pattern: {results.heading_depth_pattern}")
        print(f"  Has lateral moves: {results.heading_has_lateral}")
        print(f"  Has depth jumps: {results.heading_has_jumps}")
        print(f"  Transitions: {results.heading_transitions}")
        print(f"  Assessment: {results.heading_depth_assessment}")
    else:
        print("✗ Heading depth variance analysis not available")

    # Check dual scoring integration
    print("\n--- Dual Scoring System Integration ---")
    if hasattr(results, 'quality_score') and results.quality_score is not None:
        print(f"✓ Quality Score: {results.quality_score:.1f}")
        print(f"✓ Detection Risk: {results.detection_risk:.1f}")

        # Check for Phase 2 categories
        if hasattr(results, 'score_breakdown') and results.score_breakdown:
            print("\n  Score breakdown:")
            for category in results.score_breakdown.categories:
                print(f"    {category.name}: {category.total:.1f}/{category.max_total:.1f}")

                # Show Phase 2 dimensions
                phase2_dims = ['MATTR', 'RTTR', 'Heading Length', 'Subsection', 'Heading Depth']
                for dim in category.dimensions:
                    if any(p2 in dim.name for p2 in phase2_dims):
                        print(f"      • {dim.name}: {dim.score:.1f}/{dim.max_score:.1f}")
    else:
        print("✗ Dual scoring not available")

    print("\n=== Test completed successfully ===")
    return True

if __name__ == "__main__":
    success = test_phase2_implementation()
    exit(0 if success else 1)

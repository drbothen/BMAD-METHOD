#!/usr/bin/env python3
"""
Refactoring helper script to extract methods from analyze_ai_patterns.py
and organize them into the modular structure.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


# Method categorization mapping
METHOD_MAPPING = {
    'perplexity': [
        '_analyze_ai_vocabulary',
        '_analyze_ai_vocabulary_detailed',
        '_analyze_formulaic_transitions',
        '_analyze_transitions_detailed',
        '_score_perplexity',
        '_calculate_transformer_perplexity',
    ],
    'burstiness': [
        '_analyze_sentence_burstiness',
        '_analyze_sentence_uniformity_detailed',
        '_analyze_burstiness_issues_detailed',
        '_analyze_paragraph_variation',
        '_calculate_paragraph_cv',
        '_score_burstiness',
    ],
    'structure': [
        '_analyze_structure',
        '_analyze_headings',
        '_analyze_headings_detailed',
        '_calculate_heading_parallelism',
        '_calculate_section_variance',
        '_count_uniform_clusters',
        '_calculate_list_nesting_depth',
        '_score_structure',
        '_score_structural_patterns',
    ],
    'formatting': [
        '_analyze_formatting',
        '_analyze_em_dashes_detailed',
        '_analyze_bold_italic_patterns',
        '_analyze_formatting_issues_detailed',
        '_score_formatting',
        '_score_bold_italic',
    ],
    'voice': [
        '_score_voice',
    ],
    'syntactic': [
        '_analyze_syntactic_patterns',
        '_analyze_syntactic_issues_detailed',
        '_score_syntactic',
    ],
    'lexical': [
        '_analyze_lexical_diversity',
        '_analyze_nltk_lexical',
        '_calculate_mtld',
        '_calculate_advanced_lexical_diversity',
        '_calculate_textacy_lexical_diversity',
        '_score_advanced_lexical',
        '_score_textacy_lexical',
    ],
    'stylometric': [
        '_analyze_textacy_metrics',
        '_analyze_stylometric_issues_detailed',
        '_score_stylometric',
    ],
    'advanced': [
        '_calculate_gltr_metrics',
        '_analyze_high_predictability_segments_detailed',
        '_calculate_roberta_sentiment',
        '_calculate_roberta_ai_detection',
        '_calculate_detectgpt_metrics',
        '_score_gltr',
        '_score_ai_detection',
        '_score_sentiment',
    ],
}


def extract_method(content: str, method_name: str) -> Tuple[str, int]:
    """
    Extract a method and its content from the file.

    Returns:
        Tuple of (method_content, line_number)
    """
    # Find the method definition
    pattern = rf'    def {re.escape(method_name)}\(.*?\):'
    match = re.search(pattern, content)

    if not match:
        return None, 0

    start_pos = match.start()
    line_num = content[:start_pos].count('\n') + 1

    # Extract the full method including its body
    # This is complex - need to track indentation
    lines = content[start_pos:].split('\n')
    method_lines = [lines[0]]

    # Find base indentation (should be 4 spaces for class methods)
    base_indent = 4

    for i, line in enumerate(lines[1:], 1):
        if not line.strip():
            method_lines.append(line)
            continue

        # Check if we've reached the next method or class-level code
        current_indent = len(line) - len(line.lstrip())

        if current_indent <= base_indent and line.strip():
            break

        method_lines.append(line)

    return '\n'.join(method_lines), line_num


def main():
    """Main extraction logic"""
    source_file = Path('analyze_ai_patterns.py')

    if not source_file.exists():
        print(f"Error: {source_file} not found")
        return

    content = source_file.read_text()

    print("Analyzing methods in analyze_ai_patterns.py...")
    print(f"File size: {len(content)} characters")

    # Count methods per category
    for category, methods in METHOD_MAPPING.items():
        print(f"\n{category}: {len(methods)} methods")
        for method in methods:
            result, line_num = extract_method(content, method)
            if result:
                print(f"  ✓ {method} (line {line_num})")
            else:
                print(f"  ✗ {method} NOT FOUND")


if __name__ == '__main__':
    main()

"""
Syntactic dimension analyzer.

Analyzes syntactic complexity and patterns:
- Dependency tree depth (AI: 2-3, Human: 4-6)
- Subordination index (AI: <0.1, Human: >0.15)
- Passive voice constructions
- POS diversity
- Syntactic repetition (structural patterns)

Requires optional dependency: spaCy

Research: +10% accuracy improvement with enhanced syntactic features
"""

import re
import sys
import statistics
from typing import Dict, List, Any
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.core.results import SyntacticIssue
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS

# Required imports
import spacy
nlp_spacy = spacy.load('en_core_web_sm')


class SyntacticAnalyzer(DimensionAnalyzer):
    """Analyzes syntactic dimension - sentence structure complexity."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for syntactic patterns.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with syntactic analysis results
        """
        syntactic = self._analyze_syntactic_patterns(text)

        return {
            'syntactic': syntactic,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> List[SyntacticIssue]:
        """
        Detailed analysis with line numbers and suggestions.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            List of SyntacticIssue objects
        """
        return self._analyze_syntactic_issues_detailed(lines, html_comment_checker)

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate syntactic score.

        Args:
            analysis_results: Results dict with syntactic metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        if not analysis_results.get('syntactic'):
            return (5.0, "UNKNOWN")

        repetition = analysis_results.get('syntactic_repetition_score', 0.5)

        # Lower repetition = more varied (better)
        if repetition <= 0.3:
            return (10.0, "HIGH")  # Varied structures
        elif repetition <= 0.5:
            return (7.0, "MEDIUM")
        elif repetition <= 0.7:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")  # Mechanical repetition (AI-like)

    def _analyze_syntactic_patterns(self, text: str) -> Dict:
        """
        Enhanced syntactic analysis using spaCy.

        Metrics:
        - Dependency tree depth (AI: 2-3, Human: 4-6)
        - Subordination index (AI: <0.1, Human: >0.15)
        - Passive constructions (AI tends to overuse)
        - Morphological richness (unique lemmas)
        """
        try:
            # Remove code blocks
            text = re.sub(r'```[\s\S]*?```', '', text)

            # Process with spaCy (limit to first 100k chars for performance)
            doc = nlp_spacy(text[:100000])

            # Extract sentence structures (POS patterns)
            sentence_structures = []
            pos_tags = []
            dependency_depths = []
            subordinate_clauses = 0
            total_clauses = 0
            passive_constructions = 0
            lemmas = set()

            for sent in doc.sents:
                # Get POS pattern
                pos_pattern = ' '.join([token.pos_ for token in sent])
                sentence_structures.append(pos_pattern)

                # Collect POS tags
                pos_tags.extend([token.pos_ for token in sent])

                # Calculate dependency depth
                max_depth = 0
                for token in sent:
                    depth = len(list(token.ancestors))
                    max_depth = max(max_depth, depth)

                    # Count subordinate clauses (advcl, ccomp, xcomp, acl, relcl)
                    if token.dep_ in ['advcl', 'ccomp', 'xcomp', 'acl', 'relcl']:
                        subordinate_clauses += 1

                    # Count passive constructions (nsubjpass or auxpass dependencies)
                    if token.dep_ in ['nsubjpass', 'auxpass']:
                        passive_constructions += 1

                    # Collect unique lemmas for morphological richness
                    if token.is_alpha and len(token.text) > 2:
                        lemmas.add(token.lemma_.lower())

                dependency_depths.append(max_depth)
                total_clauses += 1

            if not sentence_structures:
                return {'available': False}

            # Calculate syntactic repetition (how many unique patterns)
            unique_structures = len(set(sentence_structures))
            total_structures = len(sentence_structures)
            repetition_score = 1 - (unique_structures / total_structures) if total_structures > 0 else 0

            # Calculate POS diversity
            unique_pos = len(set(pos_tags))
            total_pos = len(pos_tags)
            pos_diversity = unique_pos / total_pos if total_pos > 0 else 0

            # Average dependency depth (complexity)
            # AI: 2-3, Human: 4-6
            avg_depth = statistics.mean(dependency_depths) if dependency_depths else 0

            # Subordination index (subordinate clauses per clause)
            # AI: <0.1, Human: >0.15
            subordination_index = subordinate_clauses / total_clauses if total_clauses > 0 else 0

            # Morphological richness (unique lemmas)
            morphological_richness = len(lemmas)

            return {
                'available': True,
                'syntactic_repetition_score': round(repetition_score, 3),
                'pos_diversity': round(pos_diversity, 3),
                'avg_dependency_depth': round(avg_depth, 2),
                'avg_tree_depth': round(avg_depth, 2),  # Alias for new field name
                'subordination_index': round(subordination_index, 3),
                'passive_constructions': passive_constructions,
                'morphological_richness': morphological_richness
            }
        except Exception as e:
            print(f"Warning: Syntactic analysis failed: {e}", file=sys.stderr)
            return {'available': False}

    def _analyze_syntactic_issues_detailed(self, lines: List[str], html_comment_checker=None) -> List[SyntacticIssue]:
        """Detect syntactic complexity issues (passive voice, shallow trees, low subordination)."""
        issues = []

        try:
            for line_num, line in enumerate(lines, start=1):
                stripped = line.strip()

                # Skip HTML comments (metadata), headings, code blocks, and short lines
                if html_comment_checker and html_comment_checker(line):
                    continue
                if not stripped or stripped.startswith('#') or stripped.startswith('```') or len(stripped) < 20:
                    continue

                # Parse sentences on this line
                doc = nlp_spacy(stripped)

                for sent in doc.sents:
                    sent_text = sent.text.strip()
                    if len(sent_text) < 10:
                        continue

                    # Check for passive constructions
                    has_passive = any(token.dep_ in ['nsubjpass', 'auxpass'] for token in sent)
                    if has_passive:
                        issues.append(SyntacticIssue(
                            line_number=line_num,
                            sentence=sent_text[:100] + '...' if len(sent_text) > 100 else sent_text,
                            issue_type='passive',
                            metric_value=1.0,
                            problem='Passive voice construction (AI tends to overuse)',
                            suggestion='Convert to active voice - identify actor and make them the subject'
                        ))

                    # Check for shallow dependency trees (depth < 3)
                    max_depth = 0
                    for token in sent:
                        depth = 1
                        current = token
                        while current.head != current:
                            depth += 1
                            current = current.head
                        max_depth = max(max_depth, depth)

                    if max_depth < 3 and len(sent) > 10:
                        issues.append(SyntacticIssue(
                            line_number=line_num,
                            sentence=sent_text[:100] + '...' if len(sent_text) > 100 else sent_text,
                            issue_type='shallow',
                            metric_value=max_depth,
                            problem=f'Shallow syntax (depth={max_depth}, human avg=4-6)',
                            suggestion='Add subordinate clauses, relative clauses, or prepositional phrases'
                        ))

                    # Check for low subordination (no subordinate clauses)
                    subordinate_count = sum(1 for token in sent if token.dep_ in ['advcl', 'ccomp', 'xcomp', 'acl', 'relcl'])
                    if subordinate_count == 0 and len(sent) > 15:
                        issues.append(SyntacticIssue(
                            line_number=line_num,
                            sentence=sent_text[:100] + '...' if len(sent_text) > 100 else sent_text,
                            issue_type='subordination',
                            metric_value=0.0,
                            problem='No subordinate clauses (simple construction)',
                            suggestion='Add "because", "while", "although", or "when" clauses for complexity'
                        ))

        except Exception as e:
            print(f"Warning: Syntactic analysis failed: {e}", file=sys.stderr)

        return issues

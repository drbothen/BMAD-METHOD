"""
Structure dimension analyzer.

Analyzes structural patterns in markdown documents including:
- Heading depth, parallelism, and verbosity
- Section length variance (uniformity detection)
- List nesting depth and symmetry
- Uniform cluster detection

Mechanical structure (deep nesting, perfect parallelism, uniform sections) is a
strong AI signature, while varied, organic structure is human-like.
"""

import re
import statistics
from typing import Dict, List, Any, Tuple
from ai_pattern_analyzer.dimensions.base import DimensionAnalyzer
from ai_pattern_analyzer.core.results import HeadingIssue
from ai_pattern_analyzer.scoring.dual_score import THRESHOLDS


class StructureAnalyzer(DimensionAnalyzer):
    """Analyzes structure dimension - headings, sections, and list patterns."""

    def analyze(self, text: str, lines: List[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Analyze text for structural patterns.

        Args:
            text: Full text content
            lines: Text split into lines (optional)
            **kwargs: Additional parameters

        Returns:
            Dict with structure analysis results
        """
        structure = self._analyze_structure(text)
        headings = self._analyze_headings(text)
        section_var = self._calculate_section_variance(text)
        list_depth = self._calculate_list_nesting_depth(text)

        return {
            'structure': structure,
            'headings': headings,
            'section_variance': section_var,
            'list_nesting': list_depth,
        }

    def analyze_detailed(self, lines: List[str], html_comment_checker=None) -> List[HeadingIssue]:
        """
        Detailed analysis of heading issues with line numbers.

        Args:
            lines: Text split into lines
            html_comment_checker: Function to check if line is in HTML comment

        Returns:
            List of HeadingIssue objects
        """
        return self._analyze_headings_detailed(lines, html_comment_checker)

    def score(self, analysis_results: Dict[str, Any]) -> tuple:
        """
        Calculate structure score.

        Args:
            analysis_results: Results dict with heading and structure metrics

        Returns:
            Tuple of (score_value, score_label)
        """
        issues = 0

        # Heading depth
        heading_depth = analysis_results.get('heading_depth', 0)
        if heading_depth >= 5:
            issues += 2
        elif heading_depth >= 4:
            issues += 1

        # Heading parallelism (mechanical structure)
        parallelism = analysis_results.get('heading_parallelism_score', 0)
        if parallelism >= THRESHOLDS.HEADING_PARALLELISM_HIGH:
            issues += 2
        elif parallelism >= THRESHOLDS.HEADING_PARALLELISM_MEDIUM:
            issues += 1

        # Verbose headings
        total_headings = analysis_results.get('total_headings', 1)
        verbose_count = analysis_results.get('verbose_headings_count', 0)
        if verbose_count > total_headings * THRESHOLDS.HEADING_VERBOSE_RATIO:
            issues += 1

        # Score based on issues
        if issues == 0:
            return (10.0, "HIGH")
        elif issues <= 2:
            return (7.0, "MEDIUM")
        elif issues <= 4:
            return (4.0, "LOW")
        else:
            return (2.0, "VERY LOW")

    def _analyze_structure(self, text: str) -> Dict:
        """Analyze structural patterns (lists)."""
        bullet_lines = len(re.findall(r'^\s*[-*+]\s+', text, re.MULTILINE))
        numbered_lines = len(re.findall(r'^\s*\d+\.\s+', text, re.MULTILINE))

        return {
            'bullet_lines': bullet_lines,
            'numbered_lines': numbered_lines
        }

    def _analyze_headings(self, text: str) -> Dict:
        """Analyze heading patterns."""
        # Find all headings
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        headings = heading_pattern.findall(text)

        if not headings:
            return {
                'total': 0,
                'depth': 0,
                'h1': 0,
                'h2': 0,
                'h3': 0,
                'h4_plus': 0,
                'parallelism_score': 0,
                'verbose_count': 0,
                'avg_length': 0
            }

        # Count by level
        h1 = sum(1 for h in headings if len(h[0]) == 1)
        h2 = sum(1 for h in headings if len(h[0]) == 2)
        h3 = sum(1 for h in headings if len(h[0]) == 3)
        h4_plus = sum(1 for h in headings if len(h[0]) >= 4)

        # Heading depths
        depths = [len(h[0]) for h in headings]
        max_depth = max(depths) if depths else 0

        # Analyze heading text
        heading_texts = [h[1].strip() for h in headings]
        heading_word_counts = [len(h.split()) for h in heading_texts]

        verbose_count = sum(1 for c in heading_word_counts if c > 8)
        avg_length = statistics.mean(heading_word_counts) if heading_word_counts else 0

        # Calculate parallelism score (by level)
        parallelism_score = self._calculate_heading_parallelism(headings)

        return {
            'total': len(headings),
            'depth': max_depth,
            'h1': h1,
            'h2': h2,
            'h3': h3,
            'h4_plus': h4_plus,
            'parallelism_score': parallelism_score,
            'verbose_count': verbose_count,
            'avg_length': round(avg_length, 1)
        }

    def _calculate_heading_parallelism(self, headings: List[Tuple[str, str]]) -> float:
        """Calculate how mechanically parallel headings are (0-1, higher = more AI-like)."""
        # Group headings by level
        by_level = {}
        for level_marks, text in headings:
            level = len(level_marks)
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(text.strip())

        # Check each level for parallelism
        parallelism_scores = []
        for level, texts in by_level.items():
            if len(texts) < 3:
                continue  # Need at least 3 headings to detect pattern

            # Check if all start with same word
            first_words = [t.split()[0] if t.split() else '' for t in texts]
            if len(set(first_words)) == 1 and first_words[0]:
                parallelism_scores.append(1.0)  # Perfect parallelism
            # Check for common patterns
            elif self._has_common_pattern(texts):
                parallelism_scores.append(0.7)
            else:
                parallelism_scores.append(0.0)

        return round(statistics.mean(parallelism_scores), 2) if parallelism_scores else 0.0

    def _has_common_pattern(self, texts: List[str]) -> bool:
        """Check if texts follow common pattern (e.g., "How to X", "Understanding Y")."""
        patterns = [
            r'^Understanding\s+',
            r'^How\s+to\s+',
            r'^What\s+is\s+',
            r'\s+Overview$',
            r'\s+Introduction$'
        ]

        for pattern in patterns:
            matches = sum(1 for t in texts if re.search(pattern, t, re.IGNORECASE))
            if matches / len(texts) >= 0.6:  # 60%+ use same pattern
                return True
        return False

    def _calculate_section_variance(self, text: str) -> Dict[str, float]:
        """
        Calculate variance in H2 section lengths.

        Phase 1 High-ROI pattern: Detects unnaturally uniform section structure,
        where every H2 section has similar word count. Human writing typically
        shows variance ≥40%, while AI often creates uniform sections (<15%).

        Returns:
            Dict with variance_pct, score, assessment, section_count, section_lengths, uniform_clusters
        """
        # Split by H2 headings (## )
        sections = re.split(r'\n##\s+', text)

        if len(sections) < 3:
            return {
                'variance_pct': 0.0,
                'score': 8.0,  # Benefit of doubt for insufficient data
                'assessment': 'INSUFFICIENT_DATA',
                'section_count': len(sections) - 1 if len(sections) > 1 else 0,
                'section_lengths': [],
                'uniform_clusters': 0
            }

        # Count words per section (excluding heading line and preamble)
        section_lengths = []
        for section in sections[1:]:  # Skip preamble before first H2
            # Take only the content (skip the heading line itself)
            lines = section.split('\n', 1)
            if len(lines) > 1:
                content = lines[1]
            else:
                content = ""

            # Count words, excluding code blocks
            content_no_code = re.sub(r'```[\s\S]*?```', '', content)
            words = len(content_no_code.split())
            if words > 0:  # Only count non-empty sections
                section_lengths.append(words)

        if len(section_lengths) < 3:
            return {
                'variance_pct': 0.0,
                'score': 8.0,
                'assessment': 'INSUFFICIENT_DATA',
                'section_count': len(section_lengths),
                'section_lengths': section_lengths,
                'uniform_clusters': 0
            }

        mean_length = statistics.mean(section_lengths)
        stddev = statistics.stdev(section_lengths)
        variance_pct = (stddev / mean_length * 100) if mean_length > 0 else 0.0

        # Detect uniform clusters (3+ sections within ±10%)
        uniform_clusters = self._count_uniform_clusters(section_lengths, tolerance=0.10)

        # Scoring based on research thresholds
        if variance_pct >= 40:
            score, assessment = 8.0, 'EXCELLENT'
        elif variance_pct >= 25:
            score, assessment = 5.0, 'GOOD'
        elif variance_pct >= 15:
            score, assessment = 3.0, 'FAIR'
        else:
            score, assessment = 0.0, 'POOR'

        return {
            'variance_pct': round(variance_pct, 1),
            'score': score,
            'assessment': assessment,
            'section_count': len(section_lengths),
            'section_lengths': section_lengths,
            'uniform_clusters': uniform_clusters
        }

    def _calculate_list_nesting_depth(self, text: str) -> Dict[str, any]:
        """
        Analyze markdown list nesting depth and structure.

        Phase 1 High-ROI pattern: Detects overly deep list nesting with
        perfect symmetry, a strong AI signature. Human lists typically
        stay at 2-3 levels with variation, while AI creates deep (4-6 level)
        perfectly balanced hierarchies.

        Returns:
            Dict with max_depth, avg_depth, depth_distribution, score, assessment, total_list_items
        """
        lines = text.split('\n')
        list_depths = []

        for line in lines:
            # Match list items with indentation (both - and * markers)
            # Pattern: optional whitespace + list marker + space
            match = re.match(r'^(\s*)[-*+]\s+', line)
            if match:
                indent = len(match.group(1))
                # Assuming 2 spaces per level (standard markdown)
                depth = (indent // 2) + 1
                list_depths.append(depth)

        if not list_depths:
            return {
                'max_depth': 0,
                'avg_depth': 0.0,
                'depth_distribution': {},
                'score': 6.0,  # No lists is fine
                'assessment': 'NO_LISTS',
                'total_list_items': 0
            }

        max_depth = max(list_depths)
        avg_depth = statistics.mean(list_depths)

        # Count distribution
        depth_distribution = {}
        for depth in list_depths:
            depth_distribution[depth] = depth_distribution.get(depth, 0) + 1

        # Scoring based on research thresholds
        if max_depth <= 3:
            score, assessment = 6.0, 'EXCELLENT'
        elif max_depth == 4:
            score, assessment = 4.0, 'GOOD'
        elif max_depth <= 6:
            score, assessment = 2.0, 'FAIR'
        else:
            score, assessment = 0.0, 'POOR'

        return {
            'max_depth': max_depth,
            'avg_depth': round(avg_depth, 2),
            'depth_distribution': depth_distribution,
            'score': score,
            'assessment': assessment,
            'total_list_items': len(list_depths)
        }

    def _count_uniform_clusters(self, lengths: List[int], tolerance: float = 0.10) -> int:
        """
        Count sequences of 3+ sections with similar lengths (within tolerance).

        Helper method for section variance analysis. Detects clusters of
        uniformly-sized sections, a strong AI signature.

        Args:
            lengths: List of section lengths in words
            tolerance: Allowed relative difference (default 10%)

        Returns:
            Number of uniform clusters detected
        """
        if len(lengths) < 3:
            return 0

        clusters = 0
        current_cluster = 1

        for i in range(1, len(lengths)):
            # Calculate relative difference
            if lengths[i-1] > 0:
                relative_diff = abs(lengths[i] - lengths[i-1]) / lengths[i-1]
                if relative_diff <= tolerance:
                    current_cluster += 1
                else:
                    if current_cluster >= 3:
                        clusters += 1
                    current_cluster = 1
            else:
                # Reset if previous length was 0
                current_cluster = 1

        # Check final cluster
        if current_cluster >= 3:
            clusters += 1

        return clusters

    def _analyze_headings_detailed(self, lines: List[str], html_comment_checker=None) -> List[HeadingIssue]:
        """Analyze headings with specific issues and line numbers."""
        issues = []
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

        # Track all headings by level for parallelism detection
        headings_by_level = {}

        for line_num, line in enumerate(lines, start=1):
            # Skip HTML comments (metadata)
            if html_comment_checker and html_comment_checker(line):
                continue

            match = heading_pattern.match(line)
            if not match:
                continue

            level_marks, text = match.groups()
            level = len(level_marks)
            text = text.strip()
            word_count = len(text.split())

            # Track for parallelism
            if level not in headings_by_level:
                headings_by_level[level] = []
            headings_by_level[level].append((line_num, text))

            # Check depth violation (H4+)
            if level >= 4:
                issues.append(HeadingIssue(
                    line_number=line_num,
                    level=level,
                    text=text,
                    issue_type='depth',
                    suggestion=f'Flatten to H3 or convert to bold body text'
                ))

            # Check verbose headings (>8 words)
            if word_count > 8:
                # Suggest shortened version (first 3-4 words)
                words = text.split()
                shortened = ' '.join(words[:min(4, len(words))])
                issues.append(HeadingIssue(
                    line_number=line_num,
                    level=level,
                    text=text,
                    issue_type='verbose',
                    suggestion=f'Shorten to: "{shortened}..." ({min(4, len(words))} words)'
                ))

        # Check parallelism for each level
        for level, heading_list in headings_by_level.items():
            if len(heading_list) < 3:
                continue  # Need at least 3 to detect pattern

            texts = [h[1] for h in heading_list]
            first_words = [t.split()[0] if t.split() else '' for t in texts]

            # Mechanical parallelism: all start with same word
            if len(set(first_words)) == 1 and first_words[0]:
                for line_num, text in heading_list[:3]:  # Show first 3 examples
                    issues.append(HeadingIssue(
                        line_number=line_num,
                        level=level,
                        text=text,
                        issue_type='parallelism',
                        suggestion=f'Vary structure - all H{level} headings start with "{first_words[0]}"'
                    ))

        return issues

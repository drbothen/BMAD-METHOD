#!/usr/bin/env python3
"""
AI Pattern Analysis Tool for Technical Writing

Analyzes manuscripts for AI-generated content patterns across multiple dimensions:
- Perplexity (vocabulary patterns)
- Burstiness (sentence length variation)
- Structure (transitions, lists, headings)
- Voice (authenticity markers)
- Technical depth (expertise indicators)
- Formatting (em-dashes, bold, italics)
- Lexical diversity (vocabulary richness)
- Readability metrics

Based on research from:
- ai-detection-patterns.md
- formatting-humanization-patterns.md
- heading-humanization-patterns.md
- humanization-techniques.md

Usage:
    python analyze_ai_patterns.py <file_path> [options]
    python analyze_ai_patterns.py --batch <directory> [options]
"""

import re
import sys
import argparse
import json
import statistics
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict, field
from collections import Counter

# Optional dependencies (graceful degradation)
try:
    import textstat
    HAS_TEXTSTAT = True
except ImportError:
    HAS_TEXTSTAT = False
    print("Warning: textstat not installed. Readability metrics will be unavailable.", file=sys.stderr)
    print("Install with: pip install textstat", file=sys.stderr)


# Detailed mode dataclasses
@dataclass
class VocabInstance:
    """Single AI vocabulary instance with location"""
    line_number: int
    word: str
    context: str
    full_line: str
    suggestions: List[str]


@dataclass
class HeadingIssue:
    """Heading issue with location"""
    line_number: int
    level: int
    text: str
    issue_type: str  # 'depth', 'parallelism', 'verbose'
    suggestion: str


@dataclass
class UniformParagraph:
    """Paragraph with uniform sentence lengths"""
    start_line: int
    end_line: int
    sentence_count: int
    mean_length: float
    stdev: float
    sentences: List[Tuple[int, str, int]]  # (line_num, text, word_count)
    problem: str
    suggestion: str


@dataclass
class EmDashInstance:
    """Em-dash instance with location"""
    line_number: int
    context: str
    suggestion: str


@dataclass
class TransitionInstance:
    """Formulaic transition with location"""
    line_number: int
    transition: str
    context: str
    suggestions: List[str]


@dataclass
class DetailedAnalysis:
    """Comprehensive detailed analysis results"""
    file_path: str
    summary: Dict
    ai_vocabulary: List[VocabInstance] = field(default_factory=list)
    heading_issues: List[HeadingIssue] = field(default_factory=list)
    uniform_paragraphs: List[UniformParagraph] = field(default_factory=list)
    em_dashes: List[EmDashInstance] = field(default_factory=list)
    transitions: List[TransitionInstance] = field(default_factory=list)


@dataclass
class AnalysisResults:
    """Structured container for analysis results"""
    file_path: str

    # Basic metrics
    total_words: int
    total_sentences: int
    total_paragraphs: int

    # Perplexity dimension
    ai_vocabulary_count: int
    ai_vocabulary_per_1k: float
    ai_vocabulary_list: List[str]
    formulaic_transitions_count: int
    formulaic_transitions_list: List[str]

    # Burstiness dimension
    sentence_mean_length: float
    sentence_stdev: float
    sentence_min: int
    sentence_max: int
    sentence_range: Tuple[int, int]
    short_sentences_count: int  # <=10 words
    medium_sentences_count: int  # 11-25 words
    long_sentences_count: int  # >=30 words
    sentence_lengths: List[int]

    # Paragraph variation
    paragraph_mean_words: float
    paragraph_stdev: float
    paragraph_range: Tuple[int, int]

    # Lexical diversity
    unique_words: int
    lexical_diversity: float  # Type-Token Ratio

    # Structure dimension
    bullet_list_lines: int
    numbered_list_lines: int
    total_headings: int
    heading_depth: int  # Max heading level
    h1_count: int
    h2_count: int
    h3_count: int
    h4_plus_count: int
    headings_per_page: float

    # Heading patterns
    heading_parallelism_score: float  # 0-1, higher = more mechanical
    verbose_headings_count: int  # >8 words
    avg_heading_length: float

    # Voice dimension
    first_person_count: int
    direct_address_count: int
    contraction_count: int

    # Technical dimension
    domain_terms_count: int
    domain_terms_list: List[str]

    # Formatting dimension
    em_dash_count: int
    em_dashes_per_page: float
    bold_markdown_count: int
    italic_markdown_count: int

    # Readability (optional - requires textstat)
    flesch_reading_ease: Optional[float] = None
    flesch_kincaid_grade: Optional[float] = None
    gunning_fog: Optional[float] = None
    smog_index: Optional[float] = None

    # Dimension scores (calculated)
    perplexity_score: str = ""  # HIGH/MEDIUM/LOW/VERY LOW
    burstiness_score: str = ""
    structure_score: str = ""
    voice_score: str = ""
    technical_score: str = ""
    formatting_score: str = ""
    overall_assessment: str = ""


class AIPatternAnalyzer:
    """Analyzes text files for AI-generated content patterns"""

    # Replacement suggestions for AI vocabulary (for detailed mode)
    AI_VOCAB_REPLACEMENTS = {
        r'\bdelv(e|es|ing)\b': ['explore', 'examine', 'investigate', 'look at', 'dig into'],
        r'\brobust(ness)?\b': ['reliable', 'powerful', 'solid', 'effective', 'well-designed'],
        r'\bleverag(e|es|ing)\b': ['use', 'apply', 'take advantage of', 'employ'],
        r'\bharness(es|ing)?\b': ['use', 'apply', 'employ', 'tap into'],
        r'\bfacilitat(e|es|ing)\b': ['enable', 'help', 'make easier', 'allow', 'support'],
        r'\bunderscore[sd]?\b': ['emphasize', 'highlight', 'stress', 'point out'],
        r'\bseamless(ly)?\b': ['smooth', 'easy', 'straightforward', 'effortless'],
        r'\bcomprehensive(ly)?\b': ['thorough', 'complete', 'detailed', 'full'],
        r'\bstreamlin(e|ed|ing)\b': ['simplify', 'improve', 'optimize', 'refine'],
        r'\butiliz(e|es|ation|ing)\b': ['use', 'employ', 'apply'],
        r'\bunpack(s|ing)?\b': ['explain', 'explore', 'break down', 'examine'],
        r'\bmyriad\b': ['many', 'countless', 'numerous', 'various'],
        r'\bplethora\b': ['many', 'abundance', 'wealth', 'plenty'],
        r'\bparamount\b': ['critical', 'essential', 'crucial', 'vital'],
    }

    # Transition replacements (for detailed mode)
    TRANSITION_REPLACEMENTS = {
        'Furthermore,': ['Plus,', 'What\'s more,', 'Beyond that,', 'And here\'s the thing,'],
        'Moreover,': ['Plus,', 'On top of that,', 'And,'],
        'Additionally,': ['Also,', 'Plus,', 'And,'],
        'In addition,': ['Also,', 'Plus,', 'What\'s more,'],
        'First and foremost,': ['First,', 'To start,', 'Most importantly,'],
    }

    # AI-characteristic vocabulary (from ai-detection-patterns.md)
    AI_VOCABULARY = [
        # Tier 1 - Extremely High AI Association
        r'\bdelv(e|es|ing)\b', r'\brobust(ness)?\b', r'\bleverag(e|es|ing)\b',
        r'\bharness(es|ing)?\b', r'\bunderscore[sd]?\b', r'\bunderscoring\b',
        r'\bfacilitate[sd]?\b', r'\bfacilitating\b', r'\bpivotal\b',
        r'\bholistic(ally)?\b',
        # Tier 2 - High AI Association
        r'\bseamless(ly)?\b', r'\bcomprehensive(ly)?\b',
        r'\boptimiz(e|es|ation|ing)\b', r'\bstreamlin(e|ed|ing)\b',
        r'\bparamount\b', r'\bquintessential\b', r'\bmyriad\b', r'\bplethora\b',
        r'\butiliz(e|es|ation|ing)\b', r'\bcommence[sd]?\b', r'\bendeavor[sd]?\b',
        # Tier 3 - Context-Dependent
        r'\binnovative\b', r'\bcutting-edge\b', r'\brevolutionary\b',
        r'\bgame-changing\b', r'\btransformative\b',
        # Additional AI markers
        r'\bdive deep\b', r'\bdeep dive\b', r'\bunpack(s|ing)?\b',
        r'\bat the end of the day\b', r'\bsynerg(y|istic)\b',
        r'\becosystem\b', r'\blandscape\b', r'\bspace\s+\(',
        r'\bparadigm\s+shift\b',
    ]

    # Formulaic transitions (from ai-detection-patterns.md)
    FORMULAIC_TRANSITIONS = [
        r'\bFurthermore,\b', r'\bMoreover,\b', r'\bAdditionally,\b',
        r'\bIn addition,\b', r'\bIt is important to note that\b',
        r'\bIt is worth mentioning that\b', r'\bWhen it comes to\b',
        r'\bOne of the key aspects\b', r'\bFirst and foremost,\b',
        r'\bIn conclusion,\b', r'\bTo summarize,\b', r'\bIn summary,\b',
        r'\bAs mentioned earlier,\b', r'\bAs we have seen,\b',
        r'\bIt should be noted that\b', r'\bWith that said,\b',
        r'\bHaving said that,\b', r'\bIn today\'s world,\b',
        r'\bIn the modern era,\b',
    ]

    # Domain-specific technical terms (customizable per project)
    DOMAIN_TERMS_DEFAULT = [
        # Example cybersecurity terms - customize for your domain
        r'\bTriton\b', r'\bTrisis\b', r'\bSIS\b', r'\bPLC\b', r'\bSCADA\b',
        r'\bDCS\b', r'\bICS\b', r'\bOT\b', r'\bransomware\b', r'\bmalware\b',
        r'\bNIST\b', r'\bISA\b', r'\bIEC\b', r'\bMITRE\b', r'\bSOC\b',
        r'\bSIEM\b', r'\bIDS\b', r'\bIPS\b',
    ]

    def __init__(self, domain_terms: Optional[List[str]] = None):
        """Initialize analyzer with optional custom domain terms"""
        self.domain_terms = domain_terms or self.DOMAIN_TERMS_DEFAULT
        self.lines = []  # Will store line-by-line content for detailed mode

    def analyze_file_detailed(self, file_path: str) -> DetailedAnalysis:
        """Analyze file with detailed line-by-line diagnostics"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            self.lines = text.splitlines()

        # Run standard analysis for summary
        standard_results = self.analyze_file(file_path)

        # Run detailed analyses
        vocab_instances = self._analyze_ai_vocabulary_detailed()
        heading_issues = self._analyze_headings_detailed()
        uniform_paras = self._analyze_sentence_uniformity_detailed()
        em_dash_instances = self._analyze_em_dashes_detailed()
        transition_instances = self._analyze_transitions_detailed()

        # Build summary dict from standard results
        summary = {
            'overall_assessment': standard_results.overall_assessment,
            'perplexity_score': standard_results.perplexity_score,
            'burstiness_score': standard_results.burstiness_score,
            'structure_score': standard_results.structure_score,
            'voice_score': standard_results.voice_score,
            'technical_score': standard_results.technical_score,
            'formatting_score': standard_results.formatting_score,
            'total_words': standard_results.total_words,
            'total_sentences': standard_results.total_sentences,
            'ai_vocab_per_1k': standard_results.ai_vocabulary_per_1k,
            'sentence_stdev': standard_results.sentence_stdev,
            'em_dashes_per_page': standard_results.em_dashes_per_page,
            'heading_depth': standard_results.heading_depth,
            'heading_parallelism': standard_results.heading_parallelism_score,
        }

        return DetailedAnalysis(
            file_path=file_path,
            summary=summary,
            ai_vocabulary=vocab_instances[:15],  # Limit to top 15
            heading_issues=heading_issues,
            uniform_paragraphs=uniform_paras,
            em_dashes=em_dash_instances[:20],  # Limit to top 20
            transitions=transition_instances[:15],  # Limit to top 15
        )

    def _analyze_ai_vocabulary_detailed(self) -> List[VocabInstance]:
        """Detect AI vocabulary with line numbers and context"""
        instances = []

        for line_num, line in enumerate(self.lines, start=1):
            # Skip headings and code blocks
            if line.strip().startswith('#') or line.strip().startswith('```'):
                continue

            for pattern, suggestions in self.AI_VOCAB_REPLACEMENTS.items():
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    word = match.group()
                    # Extract context (20 chars each side)
                    start = max(0, match.start() - 20)
                    end = min(len(line), match.end() + 20)
                    context = f"...{line[start:end]}..."

                    instances.append(VocabInstance(
                        line_number=line_num,
                        word=word,
                        context=context,
                        full_line=line.strip(),
                        suggestions=suggestions[:3]  # Top 3 suggestions
                    ))

        return instances

    def _analyze_headings_detailed(self) -> List[HeadingIssue]:
        """Analyze headings with specific issues and line numbers"""
        issues = []
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

        # Track all headings by level for parallelism detection
        headings_by_level = {}

        for line_num, line in enumerate(self.lines, start=1):
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

    def _analyze_sentence_uniformity_detailed(self) -> List[UniformParagraph]:
        """Detect paragraphs with uniform sentence lengths"""
        uniform_paras = []

        # Split into paragraphs with line tracking
        current_para = []
        para_start_line = 1

        for line_num, line in enumerate(self.lines, start=1):
            stripped = line.strip()

            # Skip headings and code blocks
            if stripped.startswith('#') or stripped.startswith('```'):
                continue

            if stripped:
                current_para.append((line_num, line))
            else:
                # End of paragraph
                if len(current_para) >= 4:  # Need at least 4 sentences to detect uniformity
                    para_text = ' '.join([l[1] for l in current_para])
                    sent_pattern = re.compile(r'(?<=[.!?])\s+')
                    sentences = [s.strip() for s in sent_pattern.split(para_text) if s.strip()]

                    if len(sentences) >= 4:
                        lengths = [len(re.findall(r"[\w'-]+", s)) for s in sentences]
                        if len(lengths) > 1:
                            mean = statistics.mean(lengths)
                            stdev = statistics.stdev(lengths)

                            # Detect uniformity (low variation)
                            if stdev < 3:
                                sentence_info = []
                                for i, sent in enumerate(sentences[:3]):  # First 3 sentences
                                    sentence_info.append((current_para[0][0], sent[:80], lengths[i]))

                                uniform_paras.append(UniformParagraph(
                                    start_line=current_para[0][0],
                                    end_line=current_para[-1][0],
                                    sentence_count=len(sentences),
                                    mean_length=round(mean, 1),
                                    stdev=round(stdev, 1),
                                    sentences=sentence_info,
                                    problem=f'All sentences {int(min(lengths))}-{int(max(lengths))} words (mechanical uniformity)',
                                    suggestion='Add variation - combine some sentences, split others, vary between 5-45 words'
                                ))

                current_para = []
                para_start_line = line_num + 1

        return uniform_paras

    def _analyze_em_dashes_detailed(self) -> List[EmDashInstance]:
        """Track em-dashes with line numbers and context"""
        instances = []

        for line_num, line in enumerate(self.lines, start=1):
            # Skip code blocks
            if line.strip().startswith('```'):
                continue

            for match in re.finditer(r'—|--', line):
                # Get context around em-dash
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = f"...{line[start:end]}..."

                instances.append(EmDashInstance(
                    line_number=line_num,
                    context=context,
                    suggestion='Replace with period, semicolon, comma, or parentheses'
                ))

        return instances

    def _analyze_transitions_detailed(self) -> List[TransitionInstance]:
        """Detect formulaic transitions with context"""
        instances = []

        for line_num, line in enumerate(self.lines, start=1):
            # Skip headings
            if line.strip().startswith('#'):
                continue

            for pattern in self.FORMULAIC_TRANSITIONS:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    transition = match.group()
                    # Get full sentence context
                    context = line.strip()

                    # Get suggestions from mapping
                    suggestions = self.TRANSITION_REPLACEMENTS.get(
                        transition,
                        ['Remove transition entirely', 'Use natural flow']
                    )

                    instances.append(TransitionInstance(
                        line_number=line_num,
                        transition=transition,
                        context=context,
                        suggestions=suggestions[:3]
                    ))

        return instances

    def analyze_file(self, file_path: str) -> AnalysisResults:
        """Analyze a single markdown file for AI patterns"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Run all analyses
        word_count = self._count_words(text)
        ai_vocab = self._analyze_ai_vocabulary(text)
        formulaic = self._analyze_formulaic_transitions(text)
        burstiness = self._analyze_sentence_burstiness(text)
        paragraphs = self._analyze_paragraph_variation(text)
        lexical = self._analyze_lexical_diversity(text)
        structure = self._analyze_structure(text)
        headings = self._analyze_headings(text)
        voice = self._analyze_voice(text)
        technical = self._analyze_technical_depth(text)
        formatting = self._analyze_formatting(text)
        readability = self._calculate_readability(text) if HAS_TEXTSTAT else {}

        # Calculate pages (estimate: 500-1000 tokens per page, use 750 average)
        estimated_pages = max(1, word_count / 750)

        # Build results
        results = AnalysisResults(
            file_path=file_path,
            total_words=word_count,
            total_sentences=burstiness['total_sentences'],
            total_paragraphs=paragraphs['total_paragraphs'],

            ai_vocabulary_count=ai_vocab['count'],
            ai_vocabulary_per_1k=ai_vocab['per_1k'],
            ai_vocabulary_list=ai_vocab['words'],
            formulaic_transitions_count=formulaic['count'],
            formulaic_transitions_list=formulaic['transitions'],

            sentence_mean_length=burstiness['mean'],
            sentence_stdev=burstiness['stdev'],
            sentence_min=burstiness['min'],
            sentence_max=burstiness['max'],
            sentence_range=(burstiness['min'], burstiness['max']),
            short_sentences_count=burstiness['short'],
            medium_sentences_count=burstiness['medium'],
            long_sentences_count=burstiness['long'],
            sentence_lengths=burstiness['lengths'],

            paragraph_mean_words=paragraphs['mean'],
            paragraph_stdev=paragraphs['stdev'],
            paragraph_range=(paragraphs['min'], paragraphs['max']),

            unique_words=lexical['unique'],
            lexical_diversity=lexical['diversity'],

            bullet_list_lines=structure['bullet_lines'],
            numbered_list_lines=structure['numbered_lines'],
            total_headings=headings['total'],
            heading_depth=headings['depth'],
            h1_count=headings['h1'],
            h2_count=headings['h2'],
            h3_count=headings['h3'],
            h4_plus_count=headings['h4_plus'],
            headings_per_page=headings['total'] / estimated_pages,

            heading_parallelism_score=headings['parallelism_score'],
            verbose_headings_count=headings['verbose_count'],
            avg_heading_length=headings['avg_length'],

            first_person_count=voice['first_person'],
            direct_address_count=voice['direct_address'],
            contraction_count=voice['contractions'],

            domain_terms_count=technical['count'],
            domain_terms_list=technical['terms'],

            em_dash_count=formatting['em_dashes'],
            em_dashes_per_page=formatting['em_dashes'] / estimated_pages,
            bold_markdown_count=formatting['bold'],
            italic_markdown_count=formatting['italics'],

            **readability
        )

        # Calculate dimension scores
        results.perplexity_score = self._score_perplexity(results)
        results.burstiness_score = self._score_burstiness(results)
        results.structure_score = self._score_structure(results)
        results.voice_score = self._score_voice(results)
        results.technical_score = self._score_technical(results)
        results.formatting_score = self._score_formatting(results)
        results.overall_assessment = self._assess_overall(results)

        return results

    def _count_words(self, text: str) -> int:
        """Count total words in text"""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Count words
        words = re.findall(r"\b[\w'-]+\b", text)
        return len(words)

    def _analyze_ai_vocabulary(self, text: str) -> Dict:
        """Detect AI-characteristic vocabulary"""
        words_found = []
        for pattern in self.AI_VOCABULARY:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            words_found.extend([m.group() for m in matches])

        word_count = self._count_words(text)
        per_1k = (len(words_found) / word_count * 1000) if word_count > 0 else 0

        return {
            'count': len(words_found),
            'per_1k': round(per_1k, 2),
            'words': words_found[:20]  # Limit to first 20 for readability
        }

    def _analyze_formulaic_transitions(self, text: str) -> Dict:
        """Detect formulaic transitions"""
        transitions_found = []
        for pattern in self.FORMULAIC_TRANSITIONS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            transitions_found.extend([m.group() for m in matches])

        return {
            'count': len(transitions_found),
            'transitions': transitions_found[:15]
        }

    def _analyze_sentence_burstiness(self, text: str) -> Dict:
        """Analyze sentence length variation"""
        # Remove headings and list markers for sentence analysis
        lines = []
        for line in text.splitlines():
            if line.strip().startswith('#'):
                continue
            # Remove list markers
            line = re.sub(r'^\s*[-*+0-9]+[\.)]\s*', '', line)
            lines.append(line)

        clean_text = '\n'.join(lines)

        # Split into paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', clean_text) if p.strip()]

        # Split paragraphs into sentences
        sent_pattern = re.compile(r'(?<=[.!?])\s+')
        all_lengths = []

        for para in paragraphs:
            # Skip code blocks
            if '```' in para:
                continue
            sentences = [s.strip() for s in sent_pattern.split(para) if s.strip()]
            for sent in sentences:
                word_count = len(re.findall(r"[\w'-]+", sent))
                if word_count > 0:  # Only count non-empty sentences
                    all_lengths.append(word_count)

        if not all_lengths:
            return {
                'total_sentences': 0,
                'mean': 0,
                'stdev': 0,
                'min': 0,
                'max': 0,
                'short': 0,
                'medium': 0,
                'long': 0,
                'lengths': []
            }

        short = sum(1 for x in all_lengths if x <= 10)
        medium = sum(1 for x in all_lengths if 11 <= x <= 25)
        long = sum(1 for x in all_lengths if x >= 30)

        return {
            'total_sentences': len(all_lengths),
            'mean': round(statistics.mean(all_lengths), 1),
            'stdev': round(statistics.stdev(all_lengths), 1) if len(all_lengths) > 1 else 0,
            'min': min(all_lengths),
            'max': max(all_lengths),
            'short': short,
            'medium': medium,
            'long': long,
            'lengths': all_lengths
        }

    def _analyze_paragraph_variation(self, text: str) -> Dict:
        """Analyze paragraph length variation"""
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        # Filter out headings and code blocks
        para_words = []
        for para in paragraphs:
            if para.startswith('#') or '```' in para:
                continue
            words = re.findall(r"\b[\w'-]+\b", para)
            if words:
                para_words.append(len(words))

        if not para_words:
            return {
                'total_paragraphs': 0,
                'mean': 0,
                'stdev': 0,
                'min': 0,
                'max': 0
            }

        return {
            'total_paragraphs': len(para_words),
            'mean': round(statistics.mean(para_words), 1),
            'stdev': round(statistics.stdev(para_words), 1) if len(para_words) > 1 else 0,
            'min': min(para_words),
            'max': max(para_words)
        }

    def _analyze_lexical_diversity(self, text: str) -> Dict:
        """Calculate Type-Token Ratio (lexical diversity)"""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Get all words (lowercase for uniqueness)
        words = [w.lower() for w in re.findall(r"\b[\w'-]+\b", text)]

        if not words:
            return {'unique': 0, 'diversity': 0}

        unique = len(set(words))
        diversity = unique / len(words)

        return {
            'unique': unique,
            'diversity': round(diversity, 3)
        }

    def _analyze_structure(self, text: str) -> Dict:
        """Analyze structural patterns (lists)"""
        bullet_lines = len(re.findall(r'^\s*[-*+]\s+', text, re.MULTILINE))
        numbered_lines = len(re.findall(r'^\s*\d+\.\s+', text, re.MULTILINE))

        return {
            'bullet_lines': bullet_lines,
            'numbered_lines': numbered_lines
        }

    def _analyze_headings(self, text: str) -> Dict:
        """Analyze heading patterns"""
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
        """Calculate how mechanically parallel headings are (0-1, higher = more AI-like)"""
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
        """Check if texts follow common pattern (e.g., "How to X", "Understanding Y")"""
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

    def _analyze_voice(self, text: str) -> Dict:
        """Analyze voice and authenticity markers"""
        first_person = len(re.findall(
            r"\b(I|we|my|our|us|me|I've|I'm|we've|I'd|we're|I'll|we'll)\b",
            text, re.IGNORECASE
        ))

        direct_address = len(re.findall(
            r"\b(you|your|you're|you'll|you've|you'd)\b",
            text, re.IGNORECASE
        ))

        # Count contractions
        contractions = len(re.findall(
            r"\b\w+'\w+\b",  # Word with apostrophe (simplified)
            text
        ))

        return {
            'first_person': first_person,
            'direct_address': direct_address,
            'contractions': contractions
        }

    def _analyze_technical_depth(self, text: str) -> Dict:
        """Analyze technical domain expertise signals"""
        terms_found = []
        for pattern in self.domain_terms:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            terms_found.extend([m.group() for m in matches])

        return {
            'count': len(terms_found),
            'terms': terms_found[:20]  # Limit for readability
        }

    def _analyze_formatting(self, text: str) -> Dict:
        """Analyze formatting patterns"""
        # Em-dashes (—)
        em_dashes = len(re.findall(r'—|--', text))

        # Bold (markdown **text** or __text__)
        bold = len(re.findall(r'\*\*[^*]+\*\*|__[^_]+__', text))

        # Italic (markdown *text* or _text_)
        italic = len(re.findall(r'\*[^*]+\*|_[^_]+_', text))

        return {
            'em_dashes': em_dashes,
            'bold': bold,
            'italics': italic
        }

    def _calculate_readability(self, text: str) -> Dict:
        """Calculate readability metrics using textstat"""
        if not HAS_TEXTSTAT:
            return {}

        try:
            return {
                'flesch_reading_ease': round(textstat.flesch_reading_ease(text), 1),
                'flesch_kincaid_grade': round(textstat.flesch_kincaid_grade(text), 1),
                'gunning_fog': round(textstat.gunning_fog(text), 1),
                'smog_index': round(textstat.smog_index(text), 1)
            }
        except Exception as e:
            print(f"Warning: Readability calculation failed: {e}", file=sys.stderr)
            return {}

    def _score_perplexity(self, r: AnalysisResults) -> str:
        """Score perplexity dimension based on AI vocabulary density"""
        ai_per_1k = r.ai_vocabulary_per_1k

        if ai_per_1k <= 2:
            return "HIGH"
        elif ai_per_1k <= 5:
            return "MEDIUM"
        elif ai_per_1k <= 10:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_burstiness(self, r: AnalysisResults) -> str:
        """Score burstiness dimension based on sentence variation"""
        if r.total_sentences == 0:
            return "UNKNOWN"

        # Check standard deviation and distribution
        stdev = r.sentence_stdev
        short_pct = r.short_sentences_count / r.total_sentences
        long_pct = r.long_sentences_count / r.total_sentences

        # High burstiness: high stdev, good mix of short/long
        if stdev >= 8 and short_pct >= 0.15 and long_pct >= 0.15:
            return "HIGH"
        elif stdev >= 5:
            return "MEDIUM"
        elif stdev >= 3:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_structure(self, r: AnalysisResults) -> str:
        """Score structure dimension based on transitions, lists, headings"""
        issues = 0

        # Formulaic transitions
        if r.formulaic_transitions_count > 5:
            issues += 2
        elif r.formulaic_transitions_count > 2:
            issues += 1

        # Heading depth
        if r.heading_depth >= 5:
            issues += 2
        elif r.heading_depth >= 4:
            issues += 1

        # Heading parallelism
        if r.heading_parallelism_score >= 0.7:
            issues += 2
        elif r.heading_parallelism_score >= 0.4:
            issues += 1

        # Verbose headings
        if r.verbose_headings_count > r.total_headings * 0.3:
            issues += 1

        if issues == 0:
            return "HIGH"
        elif issues <= 2:
            return "MEDIUM"
        elif issues <= 4:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_voice(self, r: AnalysisResults) -> str:
        """Score voice dimension based on authenticity markers"""
        markers = 0

        # First person or direct address
        if r.first_person_count > 0 or r.direct_address_count > 10:
            markers += 1

        # Contractions (indicates conversational tone)
        contraction_ratio = r.contraction_count / max(r.total_words, 1) * 100
        if contraction_ratio > 1.0:  # >1% contraction use
            markers += 1

        # Check for both types of engagement
        if r.first_person_count > 0 and r.direct_address_count > 10:
            markers += 1

        if markers >= 3:
            return "HIGH"
        elif markers == 2:
            return "MEDIUM"
        elif markers == 1:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_technical(self, r: AnalysisResults) -> str:
        """Score technical dimension based on domain expertise"""
        # Domain term density
        term_per_1k = (r.domain_terms_count / max(r.total_words, 1)) * 1000

        if term_per_1k >= 5:
            return "HIGH"
        elif term_per_1k >= 2:
            return "MEDIUM"
        elif term_per_1k >= 0.5:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_formatting(self, r: AnalysisResults) -> str:
        """Score formatting dimension based on em-dash usage"""
        # Primary signal: em-dashes per page
        em_per_page = r.em_dashes_per_page

        if em_per_page <= 2:
            return "HIGH"  # Human-like
        elif em_per_page <= 5:
            return "MEDIUM"
        elif em_per_page <= 10:
            return "LOW"
        else:
            return "VERY LOW"  # AI-like (ChatGPT dash problem)

    def _assess_overall(self, r: AnalysisResults) -> str:
        """Provide overall humanization assessment"""
        score_map = {"HIGH": 4, "MEDIUM": 3, "LOW": 2, "VERY LOW": 1, "UNKNOWN": 2.5}

        scores = [
            score_map[r.perplexity_score] * 0.20,  # 20% weight
            score_map[r.burstiness_score] * 0.25,  # 25% weight
            score_map[r.structure_score] * 0.20,   # 20% weight
            score_map[r.voice_score] * 0.20,       # 20% weight
            score_map[r.technical_score] * 0.10,   # 10% weight
            score_map[r.formatting_score] * 0.05,  # 5% weight
        ]

        weighted_avg = sum(scores)

        if weighted_avg >= 3.5:
            return "MINIMAL humanization needed"
        elif weighted_avg >= 2.8:
            return "LIGHT humanization recommended"
        elif weighted_avg >= 2.0:
            return "SUBSTANTIAL humanization required"
        else:
            return "EXTENSIVE humanization required"


def format_detailed_report(analysis: DetailedAnalysis, output_format: str = 'text') -> str:
    """Format detailed analysis with line numbers and suggestions"""

    if output_format == 'json':
        # Convert dataclasses to dict for JSON serialization
        return json.dumps({
            'file_path': analysis.file_path,
            'summary': analysis.summary,
            'ai_vocabulary': [asdict(v) for v in analysis.ai_vocabulary],
            'heading_issues': [asdict(h) for h in analysis.heading_issues],
            'uniform_paragraphs': [asdict(p) for p in analysis.uniform_paragraphs],
            'em_dashes': [asdict(e) for e in analysis.em_dashes],
            'transitions': [asdict(t) for t in analysis.transitions],
        }, indent=2)

    else:  # text format
        s = analysis.summary
        report = f"""
{'=' * 80}
AI PATTERN ANALYSIS - DETAILED DIAGNOSTIC REPORT
{'=' * 80}

File: {analysis.file_path}
Overall Assessment: {s['overall_assessment']}

{'─' * 80}
SUMMARY SCORES
{'─' * 80}

Perplexity:   {s['perplexity_score']:12s}  |  Burstiness:  {s['burstiness_score']:12s}
Structure:    {s['structure_score']:12s}  |  Voice:       {s['voice_score']:12s}
Technical:    {s['technical_score']:12s}  |  Formatting:  {s['formatting_score']:12s}

Words: {s['total_words']} | Sentences: {s['total_sentences']} | AI Vocab: {s['ai_vocab_per_1k']:.1f}/1k

{'=' * 80}
DETAILED FINDINGS WITH LINE NUMBERS
{'=' * 80}

"""

        # AI Vocabulary Instances
        if analysis.ai_vocabulary:
            report += f"""
{'─' * 80}
AI VOCABULARY INSTANCES ({len(analysis.ai_vocabulary)} shown)
{'─' * 80}

"""
            for i, vocab in enumerate(analysis.ai_vocabulary, 1):
                report += f"""{i}. Line {vocab.line_number}: "{vocab.word}"
   Context: {vocab.context}
   → Suggestions: {', '.join(vocab.suggestions)}

"""
        else:
            report += f"""
{'─' * 80}
AI VOCABULARY: None detected ✓
{'─' * 80}

"""

        # Heading Issues
        if analysis.heading_issues:
            # Group by issue type
            depth_issues = [h for h in analysis.heading_issues if h.issue_type == 'depth']
            parallel_issues = [h for h in analysis.heading_issues if h.issue_type == 'parallelism']
            verbose_issues = [h for h in analysis.heading_issues if h.issue_type == 'verbose']

            report += f"""
{'─' * 80}
HEADING STRUCTURE ISSUES ({len(analysis.heading_issues)} total)
{'─' * 80}

"""
            if depth_issues:
                report += f"""DEPTH VIOLATIONS (H4+ headings):
"""
                for h in depth_issues[:5]:
                    report += f"""  Line {h.line_number}: {'#' * h.level} {h.text}
    → {h.suggestion}

"""

            if parallel_issues:
                report += f"""
MECHANICAL PARALLELISM (identical structures):
"""
                # Show first 3 examples only
                shown = set()
                for h in parallel_issues:
                    if len(shown) >= 3:
                        break
                    key = f"{h.level}-{h.text.split()[0] if h.text.split() else ''}"
                    if key not in shown:
                        shown.add(key)
                        report += f"""  Line {h.line_number}: {'#' * h.level} {h.text}
    → {h.suggestion}

"""

            if verbose_issues:
                report += f"""
VERBOSE HEADINGS (>8 words):
"""
                for h in verbose_issues[:5]:
                    report += f"""  Line {h.line_number}: {h.text} ({len(h.text.split())} words)
    → {h.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
HEADING STRUCTURE: No major issues ✓
{'─' * 80}

"""

        # Uniform Paragraphs
        if analysis.uniform_paragraphs:
            report += f"""
{'─' * 80}
SENTENCE UNIFORMITY ISSUES ({len(analysis.uniform_paragraphs)} paragraphs)
{'─' * 80}

"""
            for para in analysis.uniform_paragraphs[:3]:  # Show top 3
                report += f"""Paragraph at Lines {para.start_line}-{para.end_line} ({para.sentence_count} sentences):
  Mean: {para.mean_length} words | StdDev: {para.stdev} (LOW VARIATION)
  Problem: {para.problem}

  Sample sentences:
"""
                for line_num, text, word_count in para.sentences:
                    report += f"""    "{text}..." ({word_count} words)
"""
                report += f"""
  → Suggestion: {para.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
SENTENCE VARIATION: Good variation detected ✓
{'─' * 80}

"""

        # Em-Dashes
        if analysis.em_dashes:
            report += f"""
{'─' * 80}
EM-DASH USAGE ({len(analysis.em_dashes)} total, {s['em_dashes_per_page']:.1f} per page)
{'─' * 80}
TARGET: ≤2 per page

"""
            # Group by page (estimate: 750 words per page)
            words_per_page = 750
            current_page = 1
            em_count_on_page = 0

            for em in analysis.em_dashes[:10]:  # Show first 10
                # Estimate page (rough approximation)
                estimated_page = ((em.line_number * 20) // words_per_page) + 1

                if estimated_page != current_page:
                    if em_count_on_page > 0:
                        report += f"""
"""
                    current_page = estimated_page
                    em_count_on_page = 0

                report += f"""  Line {em.line_number}: {em.context}
    → {em.suggestion}
"""
                em_count_on_page += 1

            if len(analysis.em_dashes) > 10:
                report += f"""
  ... and {len(analysis.em_dashes) - 10} more instances

"""
        else:
            report += f"""
{'─' * 80}
EM-DASH USAGE: Within target range ✓
{'─' * 80}

"""

        # Formulaic Transitions
        if analysis.transitions:
            report += f"""
{'─' * 80}
FORMULAIC TRANSITIONS ({len(analysis.transitions)} found)
{'─' * 80}

"""
            for i, trans in enumerate(analysis.transitions[:10], 1):
                report += f"""{i}. Line {trans.line_number}: "{trans.transition}"
   Context: {trans.context[:100]}...
   → Suggestions: {', '.join(trans.suggestions)}

"""
            if len(analysis.transitions) > 10:
                report += f"""... and {len(analysis.transitions) - 10} more instances

"""
        else:
            report += f"""
{'─' * 80}
TRANSITIONS: Natural transitions used ✓
{'─' * 80}

"""

        report += f"""
{'=' * 80}
RECOMMENDED ACTIONS (Priority Order)
{'=' * 80}

"""

        # Generate priority recommendations
        actions = []

        if s['em_dashes_per_page'] > 3:
            actions.append(('CRITICAL', f"Reduce em-dashes from {s['em_dashes_per_page']:.1f} to ≤2 per page ({len(analysis.em_dashes)} instances to review)"))

        if s['ai_vocab_per_1k'] > 5:
            actions.append(('HIGH', f"Replace AI vocabulary: {s['ai_vocab_per_1k']:.1f} per 1k words ({len(analysis.ai_vocabulary)} instances shown above)"))

        if s['heading_depth'] >= 4:
            depth_count = len([h for h in analysis.heading_issues if h.issue_type == 'depth'])
            actions.append(('HIGH', f"Flatten heading hierarchy from H{s['heading_depth']} to H3 maximum ({depth_count} headings to restructure)"))

        if s['heading_parallelism'] >= 0.5:
            parallel_count = len([h for h in analysis.heading_issues if h.issue_type == 'parallelism'])
            actions.append(('HIGH', f"Break mechanical parallelism in headings (score: {s['heading_parallelism']:.2f}, {parallel_count} patterns detected)"))

        if s['sentence_stdev'] < 6:
            actions.append(('MEDIUM', f"Increase sentence variation (current StdDev: {s['sentence_stdev']}, target: ≥10) - {len(analysis.uniform_paragraphs)} paragraphs need work"))

        if len(analysis.transitions) > 5:
            actions.append(('MEDIUM', f"Replace formulaic transitions: {len(analysis.transitions)} instances found"))

        verbose_count = len([h for h in analysis.heading_issues if h.issue_type == 'verbose'])
        if verbose_count > 0:
            actions.append(('LOW', f"Shorten verbose headings: {verbose_count} headings >8 words"))

        if actions:
            for priority, action in actions:
                report += f"""[{priority:8s}] {action}
"""
        else:
            report += f"""✓ No major issues detected - content appears naturally written

"""

        report += f"""
{'=' * 80}
USAGE TIP: Use line numbers above to locate and fix issues systematically
{'=' * 80}

"""

        return report


def format_report(results: AnalysisResults, output_format: str = 'text') -> str:
    """Format analysis results for output"""

    if output_format == 'json':
        return json.dumps(asdict(results), indent=2)

    elif output_format == 'tsv':
        # TSV header and row
        header = [
            'file', 'words', 'sentences', 'paragraphs',
            'ai_words', 'ai_per_1k', 'formulaic', 'sent_mean', 'sent_stdev',
            'sent_min', 'sent_max', 'short', 'medium', 'long',
            'lexical_diversity', 'headings', 'h_depth', 'h_parallel',
            'em_dashes_pg', 'perplexity', 'burstiness', 'structure',
            'voice', 'technical', 'formatting', 'overall'
        ]

        row = [
            results.file_path, results.total_words, results.total_sentences,
            results.total_paragraphs, results.ai_vocabulary_count,
            results.ai_vocabulary_per_1k, results.formulaic_transitions_count,
            results.sentence_mean_length, results.sentence_stdev,
            results.sentence_min, results.sentence_max,
            results.short_sentences_count, results.medium_sentences_count,
            results.long_sentences_count, results.lexical_diversity,
            results.total_headings, results.heading_depth,
            results.heading_parallelism_score, results.em_dashes_per_page,
            results.perplexity_score, results.burstiness_score,
            results.structure_score, results.voice_score,
            results.technical_score, results.formatting_score,
            results.overall_assessment
        ]

        return '\t'.join(header) + '\n' + '\t'.join(str(v) for v in row)

    else:  # text format
        r = results
        report = f"""
{'=' * 80}
AI PATTERN ANALYSIS REPORT
{'=' * 80}

File: {r.file_path}
Words: {r.total_words} | Sentences: {r.total_sentences} | Paragraphs: {r.total_paragraphs}

{'─' * 80}
DIMENSION SCORES
{'─' * 80}

Perplexity (Vocabulary):    {r.perplexity_score:12s}  (AI words: {r.ai_vocabulary_count}, {r.ai_vocabulary_per_1k}/1k)
Burstiness (Sentence Var):  {r.burstiness_score:12s}  (μ={r.sentence_mean_length}, σ={r.sentence_stdev}, range={r.sentence_range})
Structure (Organization):   {r.structure_score:12s}  (Formulaic: {r.formulaic_transitions_count}, H-depth: {r.heading_depth})
Voice (Authenticity):       {r.voice_score:12s}  (1st-person: {r.first_person_count}, You: {r.direct_address_count})
Technical (Expertise):      {r.technical_score:12s}  (Domain terms: {r.domain_terms_count})
Formatting (Em-dashes):     {r.formatting_score:12s}  ({r.em_dashes_per_page:.1f} per page)

OVERALL ASSESSMENT: {r.overall_assessment}

{'─' * 80}
DETAILED METRICS
{'─' * 80}

SENTENCE VARIATION (Burstiness):
  Total: {r.total_sentences} | Mean: {r.sentence_mean_length} words | StdDev: {r.sentence_stdev}
  Range: {r.sentence_min}-{r.sentence_max} words
  Distribution: Short (≤10w): {r.short_sentences_count} | Medium (11-25w): {r.medium_sentences_count} | Long (≥30w): {r.long_sentences_count}

VOCABULARY & PERPLEXITY:
  AI Vocabulary: {r.ai_vocabulary_count} instances ({r.ai_vocabulary_per_1k:.2f} per 1k words)
  Examples: {', '.join(r.ai_vocabulary_list[:10]) if r.ai_vocabulary_list else 'None'}
  Formulaic Transitions: {r.formulaic_transitions_count}
  Examples: {', '.join(r.formulaic_transitions_list[:5]) if r.formulaic_transitions_list else 'None'}
  Lexical Diversity: {r.lexical_diversity:.3f} ({r.unique_words} unique words)

STRUCTURE & HEADINGS:
  Total Headings: {r.total_headings} ({r.headings_per_page:.1f} per page)
  Hierarchy: H1={r.h1_count}, H2={r.h2_count}, H3={r.h3_count}, H4+={r.h4_plus_count} | Max Depth: {r.heading_depth}
  Parallelism Score: {r.heading_parallelism_score:.2f} (0=varied, 1=mechanical)
  Verbose Headings (>8 words): {r.verbose_headings_count} | Avg Length: {r.avg_heading_length:.1f} words
  Lists: Bullets={r.bullet_list_lines}, Numbered={r.numbered_list_lines}

VOICE & AUTHENTICITY:
  First Person: {r.first_person_count} instances
  Direct Address (you/your): {r.direct_address_count} instances
  Contractions: {r.contraction_count}

FORMATTING PATTERNS:
  Em-dashes: {r.em_dash_count} ({r.em_dashes_per_page:.1f} per page)
  Bold (markdown): {r.bold_markdown_count}
  Italic (markdown): {r.italic_markdown_count}
"""

        if HAS_TEXTSTAT and r.flesch_reading_ease is not None:
            report += f"""
READABILITY METRICS:
  Flesch Reading Ease: {r.flesch_reading_ease:.1f} (60-70 = Standard, higher = easier)
  Flesch-Kincaid Grade: {r.flesch_kincaid_grade:.1f} (U.S. grade level)
  Gunning Fog Index: {r.gunning_fog:.1f} (years of education needed)
  SMOG Index: {r.smog_index:.1f} (years of education needed)
"""

        report += f"""
{'=' * 80}
RECOMMENDATIONS
{'=' * 80}

"""

        # Generate recommendations based on scores
        recommendations = []

        if r.perplexity_score in ["LOW", "VERY LOW"]:
            recommendations.append(f"⚠ VOCABULARY: Replace {r.ai_vocabulary_count} AI-typical words with natural alternatives")

        if r.burstiness_score in ["LOW", "VERY LOW"]:
            recommendations.append(f"⚠ SENTENCE VARIATION: Increase variation (current stdev: {r.sentence_stdev}, target: >8)")
            recommendations.append(f"  - Add more short sentences (≤10 words): currently {r.short_sentences_count}/{r.total_sentences}")
            recommendations.append(f"  - Add more long sentences (≥30 words): currently {r.long_sentences_count}/{r.total_sentences}")

        if r.formulaic_transitions_count > 3:
            recommendations.append(f"⚠ TRANSITIONS: Remove {r.formulaic_transitions_count} formulaic transitions")

        if r.heading_depth >= 4:
            recommendations.append(f"⚠ HEADING DEPTH: Flatten hierarchy from {r.heading_depth} to 3 levels maximum")

        if r.heading_parallelism_score >= 0.5:
            recommendations.append(f"⚠ HEADING PARALLELISM: Break mechanical parallelism (score: {r.heading_parallelism_score:.2f})")

        if r.verbose_headings_count > 0:
            recommendations.append(f"⚠ HEADINGS: Shorten {r.verbose_headings_count} verbose headings to 3-7 words")

        if r.em_dashes_per_page > 3:
            recommendations.append(f"⚠ FORMATTING: Reduce em-dashes from {r.em_dashes_per_page:.1f} to 1-2 per page")

        if r.voice_score in ["LOW", "VERY LOW"]:
            recommendations.append("⚠ VOICE: Add personal perspective markers and conversational elements")

        if r.lexical_diversity < 0.45:
            recommendations.append(f"⚠ VOCABULARY: Increase lexical diversity (current: {r.lexical_diversity:.3f}, target: >0.50)")

        if recommendations:
            for rec in recommendations:
                report += f"{rec}\n"
        else:
            report += "✓ No major issues detected. Content appears naturally human-written.\n"

        report += f"\n{'=' * 80}\n"

        return report


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Analyze manuscripts for AI-generated content patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single file
  %(prog)s chapter-01.md

  # Detailed analysis with line numbers and suggestions (for LLM-driven humanization)
  %(prog)s chapter-01.md --detailed

  # Analyze with custom domain terms
  %(prog)s chapter-01.md --domain-terms "Docker,Kubernetes,PostgreSQL"

  # Batch analyze directory, output TSV
  %(prog)s --batch manuscript/sections --format tsv > analysis.tsv

  # Detailed JSON output for programmatic use
  %(prog)s chapter-01.md --detailed --format json

  # Save detailed analysis to file
  %(prog)s chapter-01.md --detailed -o humanization-report.txt
        """
    )

    parser.add_argument('file', nargs='?', help='Markdown file to analyze')
    parser.add_argument('--batch', metavar='DIR', help='Analyze all .md files in directory')
    parser.add_argument('--detailed', action='store_true',
                        help='Provide detailed line-by-line diagnostics with context and suggestions (for LLM cleanup)')
    parser.add_argument('--format', choices=['text', 'json', 'tsv'], default='text',
                        help='Output format (default: text)')
    parser.add_argument('--domain-terms', metavar='TERMS',
                        help='Comma-separated domain-specific terms to detect (overrides defaults)')
    parser.add_argument('--output', '-o', metavar='FILE', help='Write output to file instead of stdout')

    args = parser.parse_args()

    # Validate inputs
    if not args.file and not args.batch:
        parser.error('Either FILE or --batch DIR must be specified')

    # Detailed mode limitations
    if args.detailed and args.batch:
        print("Warning: --detailed mode not supported for batch analysis. Using standard mode.", file=sys.stderr)
        args.detailed = False

    if args.detailed and args.format == 'tsv':
        print("Warning: --detailed mode not compatible with TSV format. Using JSON format.", file=sys.stderr)
        args.format = 'json'

    # Parse domain terms if provided
    domain_terms = None
    if args.domain_terms:
        domain_terms = [rf'\b{term.strip()}\b' for term in args.domain_terms.split(',')]

    # Initialize analyzer
    analyzer = AIPatternAnalyzer(domain_terms=domain_terms)

    # Process files
    if args.detailed:
        # Detailed analysis mode (single file only)
        try:
            detailed_result = analyzer.analyze_file_detailed(args.file)
            output_text = format_detailed_report(detailed_result, args.format)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_text)
                print(f"Detailed analysis written to {args.output}", file=sys.stderr)
            else:
                print(output_text)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        # Standard analysis mode
        results = []

        if args.batch:
            # Batch mode
            batch_dir = Path(args.batch)
            if not batch_dir.is_dir():
                print(f"Error: {args.batch} is not a directory", file=sys.stderr)
                sys.exit(1)

            md_files = sorted(batch_dir.glob('**/*.md'))
            if not md_files:
                print(f"Error: No .md files found in {args.batch}", file=sys.stderr)
                sys.exit(1)

            for md_file in md_files:
                try:
                    result = analyzer.analyze_file(str(md_file))
                    results.append(result)
                except Exception as e:
                    print(f"Error analyzing {md_file}: {e}", file=sys.stderr)

        else:
            # Single file mode
            try:
                result = analyzer.analyze_file(args.file)
                results.append(result)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)

        # Format and output
        output_lines = []

        if args.format == 'tsv' and len(results) > 1:
            # TSV batch output with header
            output_lines.append(format_report(results[0], 'tsv').split('\n')[0])  # Header
            for r in results:
                output_lines.append(format_report(r, 'tsv').split('\n')[1])  # Data row
        else:
            # Individual reports
            for r in results:
                output_lines.append(format_report(r, args.format))

        output_text = '\n'.join(output_lines)

        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"Analysis written to {args.output}", file=sys.stderr)
        else:
            print(output_text)


if __name__ == '__main__':
    main()

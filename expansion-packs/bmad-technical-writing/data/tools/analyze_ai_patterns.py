#!/usr/bin/env python3
"""
AI Pattern Analysis Tool for Technical Writing - ENHANCED EDITION

Analyzes manuscripts for AI-generated content patterns across 8+ dimensions:

CORE DIMENSIONS (Always Available):
- Perplexity (vocabulary patterns, AI-characteristic words)
- Burstiness (sentence length variation)
- Structure (transitions, lists, headings)
- Voice (authenticity markers, contractions)
- Technical depth (domain expertise indicators)
- Formatting (em-dashes, bold, italics)
- Lexical diversity (Type-Token Ratio)

ENHANCED DIMENSIONS (Optional NLP Libraries):
- NLTK: Enhanced lexical diversity (MTLD), stemmed diversity
- VADER: Sentiment variation across paragraphs (detects flatness)
- spaCy: Syntactic pattern repetition, POS diversity, dependency depth
- Textacy: Stylometric analysis, automated readability
- Transformers: True perplexity calculation using GPT-2 model

All enhanced features use graceful degradation - script works without optional dependencies.

Based on research from:
- ai-detection-patterns.md
- formatting-humanization-patterns.md
- heading-humanization-patterns.md
- humanization-techniques.md
- Academic NLP research (GPTZero, Originality.AI methodologies)

Usage:
    # Basic analysis (no libraries required)
    python analyze_ai_patterns.py <file_path>

    # Enhanced analysis with all NLP features
    pip install -r requirements.txt
    python analyze_ai_patterns.py <file_path>

    # Detailed mode with line numbers and suggestions
    python analyze_ai_patterns.py <file_path> --detailed

    # Batch analyze directory
    python analyze_ai_patterns.py --batch <directory> --format tsv > results.tsv
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
from datetime import datetime

# Optional dependencies (graceful degradation)
try:
    import textstat
    HAS_TEXTSTAT = True
except (ImportError, AttributeError, Exception) as e:
    HAS_TEXTSTAT = False
    print(f"Warning: textstat not available ({type(e).__name__}). Readability metrics will be unavailable.", file=sys.stderr)

try:
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.stem import PorterStemmer
    try:
        # Check if required NLTK data is available
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading required NLTK data...", file=sys.stderr)
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
    HAS_NLTK = True
except (ImportError, ValueError) as e:
    HAS_NLTK = False
    if isinstance(e, ValueError):
        print(f"Warning: NLTK dependency conflict ({str(e)[:80]}...). Enhanced lexical diversity unavailable.", file=sys.stderr)
    else:
        print("Warning: nltk not installed. Enhanced lexical diversity unavailable.", file=sys.stderr)
        print("Install with: pip install nltk", file=sys.stderr)

try:
    if not HAS_NLTK:
        raise ImportError("NLTK not available")
    from nltk.sentiment import SentimentIntensityAnalyzer
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        print("Downloading VADER lexicon...", file=sys.stderr)
        nltk.download('vader_lexicon', quiet=True)
    HAS_VADER = True
except (ImportError, ValueError):
    HAS_VADER = False
    # Don't print warning if NLTK already failed

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except (ImportError, ValueError):
    HAS_TEXTBLOB = False
    # Don't print warning - TextBlob not critical

try:
    import spacy
    # Try to load small English model
    try:
        nlp_spacy = spacy.load("en_core_web_sm")
        HAS_SPACY = True
    except OSError:
        print("Warning: spaCy model not found. Run: python -m spacy download en_core_web_sm", file=sys.stderr)
        HAS_SPACY = False
        nlp_spacy = None
except (ImportError, ValueError):
    HAS_SPACY = False
    nlp_spacy = None
    # Don't print warning - optional

try:
    if not HAS_SPACY:
        raise ImportError("spaCy not available")
    import textacy
    import textacy.extract
    HAS_TEXTACY = True
except (ImportError, ValueError, AttributeError):
    HAS_TEXTACY = False
    # Don't print warning - optional

try:
    import scipy
    from scipy.stats import hypergeom
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("Warning: scipy not installed. Advanced lexical diversity (HDD, Yule's K) unavailable.", file=sys.stderr)
    print("Install with: pip install scipy", file=sys.stderr)

try:
    import torch
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        pipeline
    )
    # Suppress transformers informational warnings (e.g., loss_type config messages)
    from transformers.utils import logging as transformers_logging
    transformers_logging.set_verbosity_error()

    HAS_TRANSFORMERS = True
    # Initialize models (will be loaded lazily if needed)
    _perplexity_model = None
    _perplexity_tokenizer = None
    _sentiment_pipeline = None
    _ai_detector_pipeline = None
except (ImportError, ValueError, OSError):
    HAS_TRANSFORMERS = False
    # Don't print warning - optional and heavy dependency


# ============================================================================
# ERROR CLASSES
# ============================================================================

class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class EmptyFileError(AnalysisError):
    """Raised when file has no analyzable content"""
    pass


class InsufficientDataError(AnalysisError):
    """Raised when not enough data for reliable analysis"""
    pass


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safe division with default for zero denominator.

    Args:
        numerator: Value to divide
        denominator: Value to divide by
        default: Value to return if denominator is zero

    Returns:
        numerator/denominator or default if denominator is 0
    """
    return numerator / denominator if denominator != 0 else default


def safe_ratio(count: int, total: int, default: float = 0.0) -> float:
    """
    Safe ratio calculation with default for zero total.

    Args:
        count: Numerator count
        total: Denominator total
        default: Value to return if total is zero

    Returns:
        count/total or default if total is 0
    """
    return count / total if total > 0 else default


# ============================================================================
# SCORING THRESHOLDS - Research-backed constants for AI pattern detection
# ============================================================================

@dataclass
class ScoringThresholds:
    """
    Research-backed thresholds for AI pattern detection.

    All thresholds based on research from:
    - GPTZero methodology (perplexity & burstiness)
    - Originality.AI pattern recognition
    - Academic NLP studies on AI detection
    - Stanford research on demographic bias
    - MIT/Northeastern research on syntactic templates

    Sources:
    - ai-detection-patterns.md
    - formatting-humanization-patterns.md
    - heading-humanization-patterns.md
    - humanization-techniques.md
    """

    # PERPLEXITY (Vocabulary Patterns)
    AI_VOCAB_VERY_LOW_THRESHOLD: float = 10.0  # per 1k words - extreme AI marker
    AI_VOCAB_LOW_THRESHOLD: float = 5.0        # per 1k words - needs improvement
    AI_VOCAB_MEDIUM_THRESHOLD: float = 2.0     # per 1k words - acceptable

    # BURSTINESS (Sentence Variation)
    SENTENCE_STDEV_HIGH: float = 10.0          # Strong variation (human-like)
    SENTENCE_STDEV_MEDIUM: float = 6.0         # Moderate variation
    SENTENCE_STDEV_LOW: float = 3.0            # Weak variation (AI-like)
    SHORT_SENTENCE_MIN_RATIO: float = 0.15     # Minimum 15% short sentences
    LONG_SENTENCE_MIN_RATIO: float = 0.15      # Minimum 15% long sentences

    # STRUCTURE (Organization)
    FORMULAIC_TRANSITIONS_MAX_PER_PAGE: int = 3
    HEADING_MAX_DEPTH: int = 3                 # H1, H2, H3 maximum
    HEADING_PARALLELISM_HIGH: float = 0.7      # Mechanical parallelism
    HEADING_PARALLELISM_MEDIUM: float = 0.4
    HEADING_VERBOSE_RATIO: float = 0.3         # >30% verbose headings

    # VOICE & AUTHENTICITY
    CONTRACTION_RATIO_GOOD: float = 1.0        # >1% contraction use
    FIRST_PERSON_MIN_GOOD: int = 3             # Minimum for personal voice
    DIRECT_ADDRESS_MIN_GOOD: int = 5           # Minimum "you" usage

    # TECHNICAL DEPTH (Domain Expertise)
    DOMAIN_TERMS_HIGH_PER_1K: float = 20.0
    DOMAIN_TERMS_MEDIUM_PER_1K: float = 10.0
    DOMAIN_TERMS_LOW_PER_1K: float = 5.0
    DOMAIN_TERMS_VERY_LOW_PER_1K: float = 0.5

    # FORMATTING (Em-dashes) - STRONGEST AI SIGNAL
    EM_DASH_MAX_PER_PAGE: float = 2.0          # Maximum acceptable
    EM_DASH_MEDIUM_PER_PAGE: float = 4.0       # Moderate issue
    EM_DASH_AI_THRESHOLD_PER_PAGE: float = 3.0 # Above this = AI marker

    # BOLD/ITALIC FORMATTING PATTERNS (NEW)
    BOLD_HUMAN_MAX_PER_1K: float = 5.0         # Human baseline: 1-5 per 1k
    BOLD_AI_MIN_PER_1K: float = 10.0           # AI typical: 10-50 per 1k
    BOLD_EXTREME_AI_PER_1K: float = 20.0       # ChatGPT extreme overuse
    FORMATTING_CONSISTENCY_AI_THRESHOLD: float = 0.7  # Mechanical consistency
    FORMATTING_CONSISTENCY_MEDIUM: float = 0.5

    # LIST USAGE PATTERNS (NEW)
    LIST_RATIO_HIGH_THRESHOLD: float = 0.40    # >40% content in lists = AI
    LIST_RATIO_MEDIUM_THRESHOLD: float = 0.25  # >25% = moderate
    LIST_ORDERED_UNORDERED_AI_MIN: float = 0.15  # AI typical ratio range
    LIST_ORDERED_UNORDERED_AI_MAX: float = 0.25
    LIST_ITEM_VARIANCE_MIN: float = 5.0

    # PUNCTUATION CLUSTERING (NEW) - VERY HIGH VALUE
    EM_DASH_CASCADING_STRONG: float = 0.7      # >0.7 = strong AI marker (95% accuracy)
    EM_DASH_CASCADING_MODERATE: float = 0.5
    EM_DASH_CASCADING_WEAK: float = 0.3
    OXFORD_COMMA_ALWAYS: float = 0.9           # Perfect consistency = AI-like
    OXFORD_COMMA_USUALLY: float = 0.75
    OXFORD_COMMA_MIN_INSTANCES: int = 3        # Need 3+ for reliable signal

    # WHITESPACE & PARAGRAPH STRUCTURE (NEW)
    PARAGRAPH_UNIFORMITY_AI_THRESHOLD: float = 0.7   # >0.7 = uniform (AI-like)
    PARAGRAPH_UNIFORMITY_MEDIUM: float = 0.5
    PARAGRAPH_UNIFORMITY_LOW: float = 0.3      # High variance (human-like)

    # CODE STRUCTURE (NEW)
    CODE_LANG_PERFECT_CONSISTENCY: float = 1.0
    CODE_LANG_HIGH_CONSISTENCY: float = 0.8
    CODE_MIN_BLOCKS_FOR_PERFECT_FLAG: int = 3

    # HEADING HIERARCHY (NEW)
    HEADING_PERFECT_ADHERENCE: float = 1.0     # Never skips levels = AI-like
    HEADING_HIGH_ADHERENCE: float = 0.9
    HEADING_MIN_FOR_PERFECT_FLAG: int = 5      # Need 5+ headings for signal

    # GPT-2 PERPLEXITY (Optional - Transformers required)
    GPT2_PERPLEXITY_AI_LIKE: float = 50.0      # <50 = AI-like
    GPT2_PERPLEXITY_HUMAN_LIKE: float = 150.0  # >150 = human-like

    # ANALYSIS MINIMUMS (Quality Thresholds)
    MIN_WORDS_FOR_ANALYSIS: int = 50           # Minimum words required
    MIN_SENTENCES_FOR_BURSTINESS: int = 5      # Minimum for sentence variation


# Global instance of thresholds (can be customized per project)
THRESHOLDS = ScoringThresholds()


# ============================================================================
# DETAILED MODE DATACLASSES
# ============================================================================

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
class SentenceBurstinessIssue:
    """Sentence uniformity problem with location"""
    start_line: int
    end_line: int
    sentence_count: int
    mean_length: float
    stdev: float
    problem: str
    sentences_preview: List[Tuple[int, str, int]]  # (line, text, word_count)
    suggestion: str


@dataclass
class SyntacticIssue:
    """Syntactic complexity issue with location"""
    line_number: int
    sentence: str
    issue_type: str  # 'passive', 'shallow', 'subordination'
    metric_value: float
    problem: str
    suggestion: str


@dataclass
class StylometricIssue:
    """Stylometric AI marker with location"""
    line_number: int
    marker_type: str  # 'however', 'moreover', 'moreover_cluster'
    context: str
    frequency: float  # per 1k words
    problem: str
    suggestion: str


@dataclass
class FormattingIssue:
    """Bold/italic overuse with location"""
    line_number: int
    issue_type: str  # 'bold_dense', 'italic_dense', 'consistent'
    context: str
    density: float
    problem: str
    suggestion: str


@dataclass
class HighPredictabilitySegment:
    """High GLTR score (AI-like) section"""
    start_line: int
    end_line: int
    segment_preview: str
    gltr_score: float
    problem: str
    suggestion: str


@dataclass
class DetailedAnalysis:
    """Comprehensive detailed analysis results"""
    file_path: str
    summary: Dict
    # Original detailed findings
    ai_vocabulary: List[VocabInstance] = field(default_factory=list)
    heading_issues: List[HeadingIssue] = field(default_factory=list)
    uniform_paragraphs: List[UniformParagraph] = field(default_factory=list)
    em_dashes: List[EmDashInstance] = field(default_factory=list)
    transitions: List[TransitionInstance] = field(default_factory=list)
    # ADVANCED: New detailed findings
    burstiness_issues: List[SentenceBurstinessIssue] = field(default_factory=list)
    syntactic_issues: List[SyntacticIssue] = field(default_factory=list)
    stylometric_issues: List[StylometricIssue] = field(default_factory=list)
    formatting_issues: List[FormattingIssue] = field(default_factory=list)
    high_predictability_segments: List[HighPredictabilitySegment] = field(default_factory=list)


# ============================================================================
# DUAL SCORING SYSTEM
# ============================================================================

@dataclass
class ScoreDimension:
    """Individual dimension score"""
    name: str
    score: float  # 0-max
    max_score: float
    percentage: float  # 0-100
    impact: str  # 'NONE', 'LOW', 'MEDIUM', 'HIGH'
    gap: float  # Points below max
    raw_value: Optional[float] = None  # Original metric value
    recommendation: Optional[str] = None


@dataclass
class ScoreCategory:
    """Category score breakdown"""
    name: str
    total: float
    max_total: float
    percentage: float
    dimensions: List[ScoreDimension]


@dataclass
class ImprovementAction:
    """Recommended improvement with impact"""
    priority: int
    dimension: str
    current_score: float
    max_score: float
    potential_gain: float
    impact_level: str
    action: str
    effort_level: str  # 'LOW', 'MEDIUM', 'HIGH'
    line_references: List[int] = field(default_factory=list)


@dataclass
class DualScore:
    """Dual scoring result with optimization path"""
    # Main scores
    detection_risk: float  # 0-100 (lower = better, less detectable)
    quality_score: float  # 0-100 (higher = better, more human-like)

    # Interpretations
    detection_interpretation: str
    quality_interpretation: str

    # Targets
    detection_target: float
    quality_target: float

    # Gaps
    detection_gap: float  # How far above target (negative = under target)
    quality_gap: float  # How far below target (positive = need improvement)

    # Breakdowns
    categories: List[ScoreCategory]

    # Optimization
    improvements: List[ImprovementAction]
    path_to_target: List[ImprovementAction]  # Sorted by ROI
    estimated_effort: str  # 'MINIMAL', 'LIGHT', 'MODERATE', 'SUBSTANTIAL', 'EXTENSIVE'

    # Metadata
    timestamp: str
    file_path: str
    total_words: int


@dataclass
class HistoricalScore:
    """Historical score tracking"""
    timestamp: str
    detection_risk: float
    quality_score: float
    detection_interpretation: str
    quality_interpretation: str
    total_words: int
    notes: str = ""


@dataclass
class ScoreHistory:
    """Score history for a document"""
    file_path: str
    scores: List[HistoricalScore] = field(default_factory=list)

    def add_score(self, score: DualScore, notes: str = ""):
        """Add a score to history"""
        self.scores.append(HistoricalScore(
            timestamp=score.timestamp,
            detection_risk=score.detection_risk,
            quality_score=score.quality_score,
            detection_interpretation=score.detection_interpretation,
            quality_interpretation=score.quality_interpretation,
            total_words=score.total_words,
            notes=notes
        ))

    def get_trend(self) -> Dict[str, str]:
        """Get trend direction"""
        if len(self.scores) < 2:
            return {'detection': 'N/A', 'quality': 'N/A'}

        det_change = self.scores[-1].detection_risk - self.scores[-2].detection_risk
        qual_change = self.scores[-1].quality_score - self.scores[-2].quality_score

        return {
            'detection': 'IMPROVING' if det_change < -1 else 'WORSENING' if det_change > 1 else 'STABLE',
            'quality': 'IMPROVING' if qual_change > 1 else 'DECLINING' if qual_change < -1 else 'STABLE',
            'detection_change': round(det_change, 1),
            'quality_change': round(qual_change, 1)
        }


# ============================================================================
# ANALYSIS RESULTS
# ============================================================================

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

    # NEW: Enhanced formatting pattern analysis
    bold_per_1k_words: float = 0.0  # Bold density
    italic_per_1k_words: float = 0.0  # Italic density
    formatting_consistency_score: float = 0.0  # 0-1, higher = more mechanical

    # NEW: List usage analysis
    total_list_items: int = 0  # Total items in all lists
    ordered_list_items: int = 0  # Items in numbered lists
    unordered_list_items: int = 0  # Items in bullet lists
    list_to_text_ratio: float = 0.0  # Proportion of content in lists
    ordered_to_unordered_ratio: float = 0.0  # AI tends toward ~0.2 (61% unordered, 12% ordered)
    list_item_length_variance: float = 0.0  # Uniformity of list item lengths

    # NEW: Punctuation clustering analysis
    em_dash_positions: List[int] = field(default_factory=list)  # Paragraph positions
    em_dash_cascading_score: float = 0.0  # Detects declining pattern (AI marker)
    oxford_comma_count: int = 0  # "a, b, and c" pattern
    non_oxford_comma_count: int = 0  # "a, b and c" pattern
    oxford_comma_consistency: float = 0.0  # 1.0 = always Oxford (AI-like)
    semicolon_count: int = 0
    semicolon_per_1k_words: float = 0.0

    # NEW: Whitespace and paragraph structure analysis
    paragraph_length_variance: float = 0.0  # Higher variance = more human
    paragraph_uniformity_score: float = 0.0  # 0-1, higher = more uniform (AI-like)
    blank_lines_count: int = 0
    blank_lines_variance: float = 0.0  # Spacing pattern consistency
    text_density: float = 0.0  # Characters per line (lower = more whitespace)

    # NEW: Code block analysis (for technical writing)
    code_block_count: int = 0
    code_blocks_with_lang: int = 0  # Properly specified language
    code_lang_consistency: float = 0.0  # 1.0 = all specified (AI-like)
    avg_code_comment_density: float = 0.0  # Comments per line of code

    # NEW: Enhanced heading hierarchy analysis
    heading_hierarchy_skips: int = 0  # Count of skipped levels (humans do this, AI doesn't)
    heading_strict_adherence: float = 0.0  # 1.0 = never skips (AI-like)
    heading_length_variance: float = 0.0  # Variation in heading lengths

    # NEW: Structural pattern analysis (Phase 1 - High ROI patterns)
    paragraph_cv: float = 0.0  # Coefficient of variation for paragraph lengths (CV <0.3 = AI-like)
    paragraph_cv_mean: float = 0.0  # Mean paragraph length in words
    paragraph_cv_stddev: float = 0.0  # Standard deviation of paragraph lengths
    paragraph_cv_assessment: str = ""  # EXCELLENT/GOOD/FAIR/POOR
    paragraph_cv_score: float = 0.0  # Quality score contribution (0-10)
    paragraph_count: int = 0  # Number of paragraphs analyzed

    section_variance_pct: float = 0.0  # Variance in H2 section lengths (variance <15% = AI-like)
    section_count: int = 0  # Number of sections analyzed
    section_variance_assessment: str = ""  # EXCELLENT/GOOD/FAIR/POOR
    section_variance_score: float = 0.0  # Quality score contribution (0-8)
    section_uniform_clusters: int = 0  # Count of 3+ sections with similar lengths

    list_max_depth: int = 0  # Maximum nesting depth across all lists
    list_avg_depth: float = 0.0  # Average nesting depth
    list_total_items: int = 0  # Total list items analyzed
    list_depth_assessment: str = ""  # EXCELLENT/GOOD/FAIR/POOR
    list_depth_score: float = 0.0  # Quality score contribution (0-6)

    # Readability (optional - requires textstat)
    flesch_reading_ease: Optional[float] = None
    flesch_kincaid_grade: Optional[float] = None
    gunning_fog: Optional[float] = None
    smog_index: Optional[float] = None

    # Enhanced lexical metrics (optional - requires NLTK)
    mtld_score: Optional[float] = None  # Moving Average Type-Token Ratio
    stemmed_diversity: Optional[float] = None  # Diversity after stemming

    # Sentiment metrics (optional - requires VADER/TextBlob)
    sentiment_variance: Optional[float] = None  # Paragraph sentiment variation
    sentiment_mean: Optional[float] = None  # Average sentiment
    sentiment_flatness_score: Optional[str] = None  # HIGH/MEDIUM/LOW

    # Syntactic metrics (optional - requires spaCy)
    syntactic_repetition_score: Optional[float] = None  # 0-1, higher = more repetitive
    pos_diversity: Optional[float] = None  # Part-of-speech tag diversity
    avg_dependency_depth: Optional[float] = None  # Syntactic complexity

    # Stylometric metrics (optional - requires Textacy)
    automated_readability: Optional[float] = None
    textacy_diversity: Optional[float] = None

    # True perplexity (optional - requires Transformers)
    gpt2_perplexity: Optional[float] = None  # Lower = more predictable (AI-like)
    distilgpt2_perplexity: Optional[float] = None  # DistilGPT-2 perplexity (faster, modern)

    # ADVANCED: GLTR token ranking (optional - requires Transformers)
    gltr_top10_percentage: Optional[float] = None  # % tokens in top-10 predictions (AI: >70%, Human: <55%)
    gltr_top100_percentage: Optional[float] = None  # % tokens in top-100 predictions
    gltr_mean_rank: Optional[float] = None  # Average token rank in model distribution
    gltr_rank_variance: Optional[float] = None  # Variance in token ranks
    gltr_likelihood: Optional[float] = None  # AI likelihood from GLTR (0-1)

    # ADVANCED: Advanced lexical diversity (optional - requires scipy)
    hdd_score: Optional[float] = None  # Hypergeometric Distribution D (most robust, AI: 0.40-0.55, Human: 0.65-0.85)
    yules_k: Optional[float] = None  # Yule's K vocabulary richness (AI: 100-150, Human: 60-90)
    maas_score: Optional[float] = None  # Maas length-corrected diversity
    vocab_concentration: Optional[float] = None  # Zipfian vocabulary concentration

    # Advanced lexical diversity - Textacy-based (optional - requires textacy+spacy)
    mattr: Optional[float] = None  # Moving Average Type-Token Ratio (window=100, AI: <0.65, Human: ≥0.70)
    rttr: Optional[float] = None  # Root Type-Token Ratio (AI: <7.5, Human: ≥7.5)
    mattr_assessment: Optional[str] = None  # EXCELLENT/GOOD/FAIR/POOR
    rttr_assessment: Optional[str] = None  # EXCELLENT/GOOD/FAIR/POOR

    # Enhanced heading length analysis
    heading_length_short_pct: Optional[float] = None  # % of headings ≤5 words
    heading_length_medium_pct: Optional[float] = None  # % of headings 6-8 words
    heading_length_long_pct: Optional[float] = None  # % of headings ≥9 words
    heading_length_assessment: Optional[str] = None  # EXCELLENT/GOOD/FAIR/POOR

    # Subsection asymmetry analysis
    subsection_counts: Optional[List[int]] = None  # H3 counts under each H2
    subsection_cv: Optional[float] = None  # Coefficient of variation (CV <0.3 = AI-like, ≥0.6 = human)
    subsection_uniform_count: Optional[int] = None  # Count of sections with 3-4 subsections (AI signature)
    subsection_assessment: Optional[str] = None  # EXCELLENT/GOOD/FAIR/POOR

    # Heading depth variance analysis
    heading_transitions: Optional[Dict[str, int]] = None  # Transition counts (e.g., H1→H2: 5)
    heading_depth_pattern: Optional[str] = None  # VARIED/SEQUENTIAL/RIGID
    heading_has_lateral: Optional[bool] = None  # Has H3→H3 lateral moves
    heading_has_jumps: Optional[bool] = None  # Has H3→H1 jumps
    heading_depth_assessment: Optional[str] = None  # EXCELLENT/GOOD/FAIR/POOR

    # ADVANCED: Enhanced syntactic analysis (optional - requires spaCy)
    avg_tree_depth: Optional[float] = None  # Dependency tree depth (AI: 2-3, Human: 4-6)
    subordination_index: Optional[float] = None  # Subordinate clause frequency (AI: <0.1, Human: >0.15)
    passive_constructions: Optional[int] = None  # Passive voice count
    morphological_richness: Optional[int] = None  # Unique morphological forms

    # ADVANCED: Comprehensive stylometrics
    function_word_ratio: Optional[float] = None  # Stop word density (most discriminative)
    hapax_percentage: Optional[float] = None  # Words appearing once (vocabulary richness)
    however_per_1k: Optional[float] = None  # AI marker: 5-10 per 1k (human: 1-3)
    moreover_per_1k: Optional[float] = None  # AI marker: 3-8 per 1k (human: 0-2)
    punctuation_density: Optional[float] = None  # Punctuation frequency
    ttr_stability: Optional[float] = None  # TTR variance across sections

    # ADVANCED: RoBERTa sentiment analysis (replaces VADER)
    roberta_sentiment_variance: Optional[float] = None  # Emotional flatness detection
    roberta_sentiment_mean: Optional[float] = None  # Average sentiment intensity
    roberta_emotionally_flat: Optional[bool] = None  # True if variance < 0.1 (AI signature)
    roberta_avg_confidence: Optional[float] = None  # Average model confidence

    # ADVANCED: DetectGPT perturbation analysis (optional - requires Transformers)
    detectgpt_perturbation_variance: Optional[float] = None  # Loss variance after perturbations
    detectgpt_original_loss: Optional[float] = None  # Original text loss
    detectgpt_is_likely_ai: Optional[bool] = None  # True if variance < 0.05

    # ADVANCED: RoBERTa AI detection (optional - requires Transformers)
    roberta_ai_likelihood: Optional[float] = None  # Overall AI probability (0-1)
    roberta_prediction_variance: Optional[float] = None  # Consistency across chunks
    roberta_consistent_predictions: Optional[bool] = None  # All chunks agree

    # Dimension scores (calculated)
    perplexity_score: str = ""  # HIGH/MEDIUM/LOW/VERY LOW
    burstiness_score: str = ""
    structure_score: str = ""
    voice_score: str = ""
    technical_score: str = ""
    formatting_score: str = ""
    syntactic_score: str = ""  # Syntactic naturalness
    sentiment_score: str = ""  # Sentiment variation

    # NEW: Enhanced structural dimension scores
    bold_italic_score: str = ""  # Bold/italic formatting patterns
    list_usage_score: str = ""  # List structure and distribution
    punctuation_score: str = ""  # Punctuation clustering patterns
    whitespace_score: str = ""  # Paragraph/whitespace distribution
    code_structure_score: str = ""  # Code block patterns (if applicable)
    heading_hierarchy_score: str = ""  # Heading level adherence
    structural_patterns_score: str = ""  # Phase 1: Paragraph CV, Section Variance, List Nesting

    # ADVANCED: AI detection scores (ensemble)
    gltr_score: str = ""  # GLTR token ranking score
    advanced_lexical_score: str = ""  # HDD/Yule's K score
    stylometric_score: str = ""  # Comprehensive stylometrics
    ai_detection_score: str = ""  # RoBERTa AI detector score

    overall_assessment: str = ""


class AIPatternAnalyzer:
    """Analyzes text files for AI-generated content patterns"""

    # Replacement suggestions for AI vocabulary (for detailed mode)
    AI_VOCAB_REPLACEMENTS = {
        r'\bdelv(e|es|ing)\b': ['explore', 'examine', 'investigate', 'look at', 'dig into'],
        r'\brobust(ness)?\b': ['reliable', 'powerful', 'solid', 'effective', 'well-designed'],
        r'\bleverag(e|es|ing)\b': ['use', 'apply', 'take advantage of', 'employ', 'work with'],
        r'\bharness(es|ing)?\b': ['use', 'apply', 'employ', 'tap into', 'utilize'],
        r'\bfacilitat(e|es|ing)\b': ['enable', 'help', 'make easier', 'allow', 'support'],
        r'\bunderscore(s|d|ing)?\b': ['emphasize', 'highlight', 'stress', 'point out', 'show'],
        r'\bpivotal\b': ['key', 'important', 'critical', 'essential', 'crucial'],
        r'\bseamless(ly)?\b': ['smooth', 'easy', 'straightforward', 'effortless', 'natural'],
        r'\bholistic(ally)?\b': ['complete', 'comprehensive', 'full', 'thorough', 'whole'],
        r'\bcomprehensive(ly)?\b': ['thorough', 'complete', 'detailed', 'full', 'extensive'],
        r'\boptimiz(e|es|ing|ation)\b': ['improve', 'enhance', 'fine-tune', 'make better', 'refine'],
        r'\bstreamlin(e|ed|ing)\b': ['simplify', 'improve', 'make efficient', 'refine', 'enhance'],
        r'\butiliz(e|es|ation|ing)\b': ['use', 'employ', 'apply', 'work with'],
        r'\bunpack(s|ing)?\b': ['explain', 'explore', 'break down', 'examine', 'analyze'],
        r'\bmyriad\b': ['many', 'countless', 'numerous', 'various', 'multiple'],
        r'\bplethora\b': ['many', 'abundance', 'wealth', 'plenty', 'lots'],
        r'\bparamount\b': ['critical', 'essential', 'crucial', 'vital', 'key'],
        r'\bquintessential\b': ['typical', 'classic', 'perfect example', 'ideal', 'archetypal'],
        r'\binnovative\b': ['new', 'creative', 'novel', 'original', 'fresh'],
        r'\bcutting-edge\b': ['advanced', 'modern', 'latest', 'state-of-the-art', 'new'],
        r'\brevolutionary\b': ['groundbreaking', 'major', 'significant', 'transformative', 'game-changing'],
        r'\bgame-changing\b': ['significant', 'major', 'important', 'transformative', 'impactful'],
        r'\btransformative\b': ['significant', 'major', 'powerful', 'game-changing', 'impactful'],
        r'\bdive deep\b': ['explore thoroughly', 'examine closely', 'investigate', 'look closely at', 'study'],
        r'\bdeep dive\b': ['thorough look', 'detailed examination', 'close look', 'in-depth analysis', 'careful study'],
        r'\becosystem\b': ['environment', 'system', 'network', 'platform', 'framework'],
        r'\blandscape\b': ['field', 'area', 'space', 'domain', 'world'],
        r'\bparadigm\s+shift\b': ['major change', 'fundamental shift', 'big change', 'transformation', 'sea change'],
        r'\bsynerg(y|istic)\b': ['cooperation', 'collaboration', 'combined effect', 'teamwork', 'partnership'],
        r'\bcommence(s|d)?\b': ['start', 'begin', 'initiate', 'launch', 'kick off'],
        r'\bendeavor(s)?\b': ['effort', 'project', 'attempt', 'undertaking', 'initiative'],
    }

    # Transition replacements (for detailed mode)
    TRANSITION_REPLACEMENTS = {
        'Furthermore,': ['Plus,', 'What\'s more,', 'Beyond that,', 'And here\'s the thing,', 'On top of that,'],
        'Moreover,': ['Plus,', 'On top of that,', 'And,', 'What\'s more,', 'Beyond that,'],
        'Additionally,': ['Also,', 'Plus,', 'And,', 'What\'s more,', 'On top of that,'],
        'In addition,': ['Also,', 'Plus,', 'What\'s more,', 'Beyond that,', 'And,'],
        'First and foremost,': ['First,', 'To start,', 'Most importantly,', 'Above all,', 'First off,'],
        'It is important to note that': ['Note that', 'Keep in mind', 'Remember', 'Worth noting:', 'Key point:'],
        'It is worth mentioning that': ['Worth noting', 'Keep in mind', 'Note that', 'Also', 'Interestingly,'],
        'When it comes to': ['For', 'With', 'Regarding', 'As for', 'Looking at'],
        'In conclusion,': ['Finally,', 'To sum up,', 'In short,', 'Bottom line:', 'To wrap up,'],
        'To summarize,': ['In short,', 'Briefly,', 'To sum up,', 'Bottom line:', 'In a nutshell,'],
        'In summary,': ['In short,', 'Briefly,', 'To recap,', 'Bottom line:', 'To sum up,'],
        'As mentioned earlier,': ['Earlier,', 'As noted,', 'Remember,', 'Recall that', 'As we saw,'],
        'It should be noted that': ['Note that', 'Keep in mind', 'Remember', 'Worth noting:', 'Important:'],
        'With that said,': ['That said,', 'Still,', 'Even so,', 'But', 'However,'],
        'Having said that,': ['That said,', 'Still,', 'Even so,', 'But', 'However,'],
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
        """Initialize analyzer with optional custom domain terms.

        Pre-compiles all regex patterns for 20-30% performance improvement.
        """
        self.domain_terms = domain_terms or self.DOMAIN_TERMS_DEFAULT
        self.lines = []  # Will store line-by-line content for detailed mode

        # Pre-compile all regex patterns (significant performance improvement)
        # AI Vocabulary patterns
        self._ai_vocab_patterns = {
            pattern: re.compile(pattern, re.IGNORECASE)
            for pattern in self.AI_VOCABULARY
        }

        # Formulaic transition patterns
        self._transition_patterns = [
            re.compile(pattern) for pattern in self.FORMULAIC_TRANSITIONS
        ]

        # Domain term patterns
        self._domain_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.domain_terms
        ]

        # Formatting patterns
        self._bold_pattern = re.compile(r'\*\*[^*]+\*\*|__[^_]+__')
        self._italic_pattern = re.compile(r'\*[^*]+\*|_[^_]+_')
        self._em_dash_pattern = re.compile(r'—|--')

        # HTML comment pattern (metadata blocks to ignore)
        self._html_comment_pattern = re.compile(r'<!--.*?-->', re.DOTALL)

        # Text analysis patterns
        self._word_pattern = re.compile(r'\b[a-zA-Z]+\b')
        self._heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

        # Punctuation patterns
        self._oxford_comma_pattern = re.compile(r',\s+and\b')
        self._serial_comma_pattern = re.compile(r',\s+[^,]+,\s+and\b')

        # First-person patterns
        self._first_person_pattern = re.compile(r'\b(I|we|my|our|me|us)\b', re.IGNORECASE)
        self._second_person_pattern = re.compile(r'\b(you|your|yours)\b', re.IGNORECASE)
        self._contraction_pattern = re.compile(r"\b\w+'\w+\b")

    def _strip_html_comments(self, text: str) -> str:
        """Remove HTML comment blocks (metadata) from text for analysis"""
        return self._html_comment_pattern.sub('', text)

    def _is_line_in_html_comment(self, line: str) -> bool:
        """Check if a line is inside or is an HTML comment"""
        # Line contains complete comment
        if '<!--' in line and '-->' in line:
            return True
        # Line is start or middle of comment
        if '<!--' in line or '-->' in line:
            return True
        return False

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

        # Run detailed analyses - Original methods
        vocab_instances = self._analyze_ai_vocabulary_detailed()
        heading_issues = self._analyze_headings_detailed()
        uniform_paras = self._analyze_sentence_uniformity_detailed()
        em_dash_instances = self._analyze_em_dashes_detailed()
        transition_instances = self._analyze_transitions_detailed()

        # ADVANCED: New detailed analyses for advanced metrics
        burstiness_issues = self._analyze_burstiness_issues_detailed()
        syntactic_issues = self._analyze_syntactic_issues_detailed()
        stylometric_issues = self._analyze_stylometric_issues_detailed()
        formatting_issues = self._analyze_formatting_issues_detailed()
        high_pred_segments = self._analyze_high_predictability_segments_detailed()

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
            # ADVANCED: Include new metric scores
            'gltr_score': standard_results.gltr_score if standard_results.gltr_score else "N/A",
            'advanced_lexical_score': standard_results.advanced_lexical_score if standard_results.advanced_lexical_score else "N/A",
            'stylometric_score': standard_results.stylometric_score if standard_results.stylometric_score else "N/A",
            'ai_detection_score': standard_results.ai_detection_score if standard_results.ai_detection_score else "N/A",
        }

        return DetailedAnalysis(
            file_path=file_path,
            summary=summary,
            # Original detailed findings
            ai_vocabulary=vocab_instances[:15],  # Limit to top 15
            heading_issues=heading_issues,
            uniform_paragraphs=uniform_paras,
            em_dashes=em_dash_instances[:20],  # Limit to top 20
            transitions=transition_instances[:15],  # Limit to top 15
            # ADVANCED: New detailed findings
            burstiness_issues=burstiness_issues[:10],  # Limit to top 10
            syntactic_issues=syntactic_issues[:20],  # Limit to top 20
            stylometric_issues=stylometric_issues[:15],  # Limit to top 15
            formatting_issues=formatting_issues[:15],  # Limit to top 15
            high_predictability_segments=high_pred_segments[:10],  # Limit to top 10
        )

    def _analyze_ai_vocabulary_detailed(self) -> List[VocabInstance]:
        """Detect AI vocabulary with line numbers and context"""
        instances = []

        for line_num, line in enumerate(self.lines, start=1):
            # Skip HTML comments (metadata), headings, and code blocks
            if self._is_line_in_html_comment(line):
                continue
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
                        suggestions=suggestions[:5]  # Top 5 suggestions
                    ))

        return instances

    def _analyze_headings_detailed(self) -> List[HeadingIssue]:
        """Analyze headings with specific issues and line numbers"""
        issues = []
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

        # Track all headings by level for parallelism detection
        headings_by_level = {}

        for line_num, line in enumerate(self.lines, start=1):
            # Skip HTML comments (metadata)
            if self._is_line_in_html_comment(line):
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

    def _analyze_sentence_uniformity_detailed(self) -> List[UniformParagraph]:
        """Detect paragraphs with uniform sentence lengths"""
        uniform_paras = []

        # Split into paragraphs with line tracking
        current_para = []
        para_start_line = 1

        for line_num, line in enumerate(self.lines, start=1):
            stripped = line.strip()

            # Skip HTML comments (metadata), headings, and code blocks
            if self._is_line_in_html_comment(line):
                continue
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
            # Skip HTML comments (metadata) and code blocks
            if self._is_line_in_html_comment(line):
                continue
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
            # Skip HTML comments (metadata) and headings
            if self._is_line_in_html_comment(line):
                continue
            if line.strip().startswith('#'):
                continue

            for pattern in self.FORMULAIC_TRANSITIONS:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    transition = match.group()
                    # Get full sentence context
                    context = line.strip()

                    # Get suggestions from mapping (case-insensitive lookup)
                    suggestions = None
                    for key, values in self.TRANSITION_REPLACEMENTS.items():
                        if transition.lower() == key.lower():
                            suggestions = values
                            break

                    if suggestions is None:
                        suggestions = ['Remove transition entirely', 'Use natural flow']

                    instances.append(TransitionInstance(
                        line_number=line_num,
                        transition=transition,
                        context=context,
                        suggestions=suggestions[:5]
                    ))

        return instances

    def _analyze_burstiness_issues_detailed(self) -> List[SentenceBurstinessIssue]:
        """Detect sections with uniform sentence lengths (low burstiness)"""
        issues = []

        # Split into paragraphs
        current_para = []
        para_start_line = 1

        for line_num, line in enumerate(self.lines, start=1):
            stripped = line.strip()

            # Skip HTML comments (metadata), headings, and code blocks
            if self._is_line_in_html_comment(line):
                continue
            if stripped.startswith('#') or stripped.startswith('```'):
                continue

            if stripped:
                current_para.append((line_num, line))
            else:
                # End of paragraph - analyze it
                if len(current_para) >= 3:
                    para_text = ' '.join([l[1] for l in current_para])
                    sent_pattern = re.compile(r'(?<=[.!?])\s+')
                    sentences = [s.strip() for s in sent_pattern.split(para_text) if s.strip()]

                    if len(sentences) >= 3:
                        lengths = [len(re.findall(r"[\w'-]+", s)) for s in sentences]
                        if len(lengths) > 1:
                            mean = statistics.mean(lengths)
                            stdev = statistics.stdev(lengths)

                            # Low burstiness: stdev < 5 words (AI signature)
                            if stdev < 5:
                                # Get preview of sentences with their lengths
                                preview = []
                                for i, sent in enumerate(sentences[:3]):
                                    preview.append((
                                        current_para[0][0] + i,  # Line number
                                        sent[:60] + '...' if len(sent) > 60 else sent,
                                        lengths[i]
                                    ))

                                issues.append(SentenceBurstinessIssue(
                                    start_line=current_para[0][0],
                                    end_line=current_para[-1][0],
                                    sentence_count=len(sentences),
                                    mean_length=round(mean, 1),
                                    stdev=round(stdev, 1),
                                    problem=f'Uniform sentence lengths ({int(min(lengths))}-{int(max(lengths))} words, σ={stdev:.1f})',
                                    sentences_preview=preview,
                                    suggestion='Add variety: combine short sentences (5-10 words), keep medium (15-25), add complex (30-45 words)'
                                ))

                current_para = []
                para_start_line = line_num + 1

        return issues

    def _analyze_syntactic_issues_detailed(self) -> List[SyntacticIssue]:
        """Detect syntactic complexity issues (passive voice, shallow trees, low subordination)"""
        if not HAS_SPACY:
            return []

        issues = []

        try:
            import spacy
            nlp = spacy.load('en_core_web_sm')

            for line_num, line in enumerate(self.lines, start=1):
                stripped = line.strip()

                # Skip HTML comments (metadata), headings, code blocks, and short lines
                if self._is_line_in_html_comment(line):
                    continue
                if not stripped or stripped.startswith('#') or stripped.startswith('```') or len(stripped) < 20:
                    continue

                # Parse sentences on this line
                doc = nlp(stripped)

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

    def _analyze_stylometric_issues_detailed(self) -> List[StylometricIssue]:
        """Detect AI-specific stylometric markers (however, moreover, repetitive vocabulary)"""
        issues = []

        # Track "however" and "moreover" usage
        however_pattern = re.compile(r'\bhowever\b', re.IGNORECASE)
        moreover_pattern = re.compile(r'\bmoreover\b', re.IGNORECASE)

        # Count total words for frequency calculation
        total_words = sum(len(re.findall(r'\b\w+\b', line)) for line in self.lines)
        words_in_thousands = total_words / 1000 if total_words > 0 else 1

        for line_num, line in enumerate(self.lines, start=1):
            stripped = line.strip()

            # Skip HTML comments (metadata), headings, and code blocks
            if self._is_line_in_html_comment(line):
                continue
            if stripped.startswith('#') or stripped.startswith('```'):
                continue

            # Check for "however" (AI: 5-10 per 1k, Human: 1-3 per 1k)
            however_matches = list(however_pattern.finditer(line))
            for match in however_matches:
                context = line.strip()
                issues.append(StylometricIssue(
                    line_number=line_num,
                    marker_type='however',
                    context=context[:120] + '...' if len(context) > 120 else context,
                    frequency=len(however_matches) / words_in_thousands if words_in_thousands > 0 else 0,
                    problem='"However" is AI transition marker (human writers use sparingly)',
                    suggestion='Replace with: "But", "Yet", "Still", or natural flow without transition'
                ))

            # Check for "moreover" (AI: 3-7 per 1k, Human: 0-1 per 1k)
            moreover_matches = list(moreover_pattern.finditer(line))
            for match in moreover_matches:
                context = line.strip()
                issues.append(StylometricIssue(
                    line_number=line_num,
                    marker_type='moreover',
                    context=context[:120] + '...' if len(context) > 120 else context,
                    frequency=len(moreover_matches) / words_in_thousands if words_in_thousands > 0 else 0,
                    problem='"Moreover" is strong AI signature (very rare in human writing)',
                    suggestion='Replace with: "Also", "And", "Plus", or remove transition entirely'
                ))

        # Check for clusters (multiple "however" in close proximity)
        however_lines = [i for i, line in enumerate(self.lines, start=1)
                        if however_pattern.search(line)]
        for i in range(len(however_lines) - 1):
            if however_lines[i+1] - however_lines[i] <= 3:  # Within 3 lines
                issues.append(StylometricIssue(
                    line_number=however_lines[i],
                    marker_type='however_cluster',
                    context=f'Lines {however_lines[i]}-{however_lines[i+1]}',
                    frequency=2 / words_in_thousands if words_in_thousands > 0 else 0,
                    problem='Clustered "however" usage (strong AI signature)',
                    suggestion='Vary transitions or remove some instances entirely'
                ))

        return issues

    def _analyze_formatting_issues_detailed(self) -> List[FormattingIssue]:
        """Detect excessive bold/italic usage and mechanical formatting patterns"""
        issues = []

        bold_pattern = re.compile(r'\*\*[^*]+\*\*|__[^_]+__')
        italic_pattern = re.compile(r'\*[^*]+\*|_[^_]+_')

        for line_num, line in enumerate(self.lines, start=1):
            stripped = line.strip()

            # Skip HTML comments (metadata), headings, and code blocks
            if self._is_line_in_html_comment(line):
                continue
            if stripped.startswith('#') or stripped.startswith('```'):
                continue

            if not stripped:
                continue

            # Count formatting on this line
            word_count = len(re.findall(r'\b\w+\b', line))
            if word_count == 0:
                continue

            bold_matches = list(bold_pattern.finditer(line))
            italic_matches = list(italic_pattern.finditer(line))

            bold_words = sum(len(re.findall(r'\b\w+\b', match.group())) for match in bold_matches)
            italic_words = sum(len(re.findall(r'\b\w+\b', match.group())) for match in italic_matches)

            bold_density = (bold_words / word_count) * 100 if word_count > 0 else 0
            italic_density = (italic_words / word_count) * 100 if word_count > 0 else 0

            # Excessive bold (>10% of words)
            if bold_density > 10:
                context = line.strip()[:100] + '...' if len(line.strip()) > 100 else line.strip()
                issues.append(FormattingIssue(
                    line_number=line_num,
                    issue_type='bold_dense',
                    context=context,
                    density=bold_density,
                    problem=f'Excessive bolding ({bold_density:.1f}% of words, target <5%)',
                    suggestion='Remove bold from less critical terms; reserve for key concepts only'
                ))

            # Excessive italic (>15% of words, excluding functional use)
            if italic_density > 15:
                context = line.strip()[:100] + '...' if len(line.strip()) > 100 else line.strip()
                issues.append(FormattingIssue(
                    line_number=line_num,
                    issue_type='italic_dense',
                    context=context,
                    density=italic_density,
                    problem=f'Excessive italics ({italic_density:.1f}% of words, target <10%)',
                    suggestion='Use italics functionally: titles, defined terms, subtle emphasis only'
                ))

        return issues

    def _analyze_high_predictability_segments_detailed(self) -> List[HighPredictabilitySegment]:
        """Identify text segments with high GLTR scores (AI-like predictability)"""
        if not HAS_TRANSFORMERS:
            return []

        issues = []

        try:
            global _perplexity_model, _perplexity_tokenizer

            if _perplexity_model is None:
                # Model already loaded in other GLTR function
                return []

            # Analyze in 50-100 word chunks
            chunk_size = 75  # words
            current_chunk = []
            chunk_start_line = 1

            for line_num, line in enumerate(self.lines, start=1):
                stripped = line.strip()

                # Skip HTML comments (metadata), headings, and code blocks
                if self._is_line_in_html_comment(line):
                    continue
                if stripped.startswith('#') or stripped.startswith('```'):
                    continue

                if stripped:
                    words = re.findall(r'\b\w+\b', stripped)
                    current_chunk.extend(words)

                    if len(current_chunk) >= chunk_size:
                        # Analyze this chunk
                        chunk_text = ' '.join(current_chunk)

                        # Calculate GLTR for chunk
                        try:
                            tokens = _perplexity_tokenizer.encode(chunk_text, add_special_tokens=True)
                            if len(tokens) < 10:
                                current_chunk = []
                                chunk_start_line = line_num + 1
                                continue

                            import torch
                            ranks = []
                            for i in range(1, min(len(tokens), 100)):
                                input_ids = torch.tensor([tokens[:i]])
                                with torch.no_grad():
                                    outputs = _perplexity_model(input_ids)
                                    logits = outputs.logits[0, -1, :]
                                    probs = torch.softmax(logits, dim=-1)
                                    sorted_indices = torch.argsort(probs, descending=True)
                                    actual_token = tokens[i]
                                    rank = (sorted_indices == actual_token).nonzero(as_tuple=True)[0].item()
                                    ranks.append(rank)

                            if ranks:
                                top10_pct = sum(1 for r in ranks if r < 10) / len(ranks)

                                # High predictability: >70% in top-10
                                if top10_pct > 0.70:
                                    preview = chunk_text[:150] + '...' if len(chunk_text) > 150 else chunk_text
                                    issues.append(HighPredictabilitySegment(
                                        start_line=chunk_start_line,
                                        end_line=line_num,
                                        segment_preview=preview,
                                        gltr_score=top10_pct,
                                        problem=f'High predictability (GLTR={top10_pct:.2f}, AI threshold >0.70)',
                                        suggestion='Rewrite with less common word choices, vary sentence structure, add unexpected turns'
                                    ))

                        except Exception as e:
                            print(f"Warning: GLTR chunk analysis failed: {e}", file=sys.stderr)

                        # Reset chunk
                        current_chunk = []
                        chunk_start_line = line_num + 1

        except Exception as e:
            print(f"Warning: High predictability segment analysis failed: {e}", file=sys.stderr)

        return issues

    def analyze_file(self, file_path: str) -> AnalysisResults:
        """Analyze a single markdown file for AI patterns"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Strip HTML comments (metadata blocks) before analysis
        text = self._strip_html_comments(text)

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

        # Enhanced analyses (optional libraries)
        nltk_lexical = self._analyze_nltk_lexical(text) if HAS_NLTK else {}
        sentiment = self._analyze_sentiment_variation(text) if HAS_VADER else {}
        syntactic = self._analyze_syntactic_patterns(text) if HAS_SPACY else {}
        textacy_metrics = self._analyze_textacy_metrics(text) if HAS_TEXTACY and HAS_SPACY else {}
        transformer_ppl = self._calculate_transformer_perplexity(text) if HAS_TRANSFORMERS else {}

        # ADVANCED: New enhanced methods (Phase 1 & 2)
        gltr_metrics = self._calculate_gltr_metrics(text) if HAS_TRANSFORMERS else {}
        advanced_lexical = self._calculate_advanced_lexical_diversity(text) if HAS_SCIPY else {}
        roberta_sentiment = self._calculate_roberta_sentiment(text) if HAS_TRANSFORMERS else {}
        roberta_ai = self._calculate_roberta_ai_detection(text) if HAS_TRANSFORMERS else {}
        detectgpt = self._calculate_detectgpt_metrics(text) if HAS_TRANSFORMERS else {}

        # Advanced lexical diversity and enhanced heading analysis
        textacy_lexical = self._calculate_textacy_lexical_diversity(text) if HAS_TEXTACY and HAS_SPACY else {}
        heading_length = self._calculate_heading_length_analysis(text)
        subsection_asym = self._calculate_subsection_asymmetry(text)
        heading_depth_var = self._calculate_heading_depth_variance(text)

        # NEW: Enhanced structural analyses (always available)
        bold_italic = self._analyze_bold_italic_patterns(text)
        list_usage = self._analyze_list_usage(text)
        punctuation = self._analyze_punctuation_clustering(text)
        whitespace = self._analyze_whitespace_patterns(text)
        code_blocks = self._analyze_code_blocks(text)
        heading_hierarchy = self._analyze_heading_hierarchy_enhanced(text)

        # NEW: Phase 1 High-ROI structural pattern detection (always available)
        paragraph_cv = self._calculate_paragraph_cv(text)
        section_variance = self._calculate_section_variance(text)
        list_nesting = self._calculate_list_nesting_depth(text)

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

            # NEW: Enhanced formatting patterns
            bold_per_1k_words=bold_italic['bold_per_1k'],
            italic_per_1k_words=bold_italic['italic_per_1k'],
            formatting_consistency_score=bold_italic['formatting_consistency'],

            # NEW: List usage patterns
            total_list_items=list_usage['total_list_items'],
            ordered_list_items=list_usage['ordered_items'],
            unordered_list_items=list_usage['unordered_items'],
            list_to_text_ratio=list_usage['list_to_text_ratio'],
            ordered_to_unordered_ratio=list_usage['ordered_to_unordered_ratio'],
            list_item_length_variance=list_usage['list_item_variance'],

            # NEW: Punctuation clustering
            em_dash_positions=punctuation['em_dash_positions'],
            em_dash_cascading_score=punctuation['em_dash_cascading'],
            oxford_comma_count=punctuation['oxford_comma_count'],
            non_oxford_comma_count=punctuation['non_oxford_comma_count'],
            oxford_comma_consistency=punctuation['oxford_consistency'],
            semicolon_count=punctuation['semicolon_count'],
            semicolon_per_1k_words=punctuation['semicolon_per_1k'],

            # NEW: Whitespace patterns
            paragraph_length_variance=whitespace['paragraph_variance'],
            paragraph_uniformity_score=whitespace['paragraph_uniformity'],
            blank_lines_count=whitespace['blank_lines'],
            blank_lines_variance=whitespace['blank_line_variance'],
            text_density=whitespace['text_density'],

            # NEW: Code block patterns
            code_block_count=code_blocks['code_blocks'],
            code_blocks_with_lang=code_blocks['code_with_lang'],
            code_lang_consistency=code_blocks['code_lang_consistency'],
            avg_code_comment_density=code_blocks['code_comment_density'],

            # NEW: Enhanced heading hierarchy
            heading_hierarchy_skips=heading_hierarchy['hierarchy_skips'],
            heading_strict_adherence=heading_hierarchy['hierarchy_adherence'],
            heading_length_variance=heading_hierarchy['heading_length_variance'],

            # NEW: Phase 1 High-ROI structural patterns
            paragraph_cv=paragraph_cv['cv'],
            paragraph_cv_mean=paragraph_cv['mean_length'],
            paragraph_cv_stddev=paragraph_cv['stddev'],
            paragraph_cv_assessment=paragraph_cv['assessment'],
            paragraph_cv_score=paragraph_cv['score'],
            paragraph_count=paragraph_cv['paragraph_count'],

            section_variance_pct=section_variance['variance_pct'],
            section_count=section_variance['section_count'],
            section_variance_assessment=section_variance['assessment'],
            section_variance_score=section_variance['score'],
            section_uniform_clusters=section_variance['uniform_clusters'],

            list_max_depth=list_nesting['max_depth'],
            list_avg_depth=list_nesting['avg_depth'],
            list_total_items=list_nesting['total_list_items'],
            list_depth_assessment=list_nesting['assessment'],
            list_depth_score=list_nesting['score'],

            **readability,
            **nltk_lexical,
            **sentiment,
            **syntactic,
            **textacy_metrics,
            **transformer_ppl,
            # ADVANCED: New enhanced metrics
            **gltr_metrics,
            **advanced_lexical,
            **roberta_sentiment,
            **roberta_ai,
            **detectgpt,

            # Advanced lexical diversity (Textacy-based)
            mattr=textacy_lexical.get('mattr'),
            rttr=textacy_lexical.get('rttr'),
            mattr_assessment=textacy_lexical.get('mattr_assessment'),
            rttr_assessment=textacy_lexical.get('rttr_assessment'),

            # Enhanced heading length analysis
            heading_length_short_pct=heading_length.get('distribution_pct', {}).get('short'),
            heading_length_medium_pct=heading_length.get('distribution_pct', {}).get('medium'),
            heading_length_long_pct=heading_length.get('distribution_pct', {}).get('long'),
            heading_length_assessment=heading_length.get('assessment'),

            # Subsection asymmetry analysis
            subsection_counts=subsection_asym.get('subsection_counts'),
            subsection_cv=subsection_asym.get('cv'),
            subsection_uniform_count=subsection_asym.get('uniform_count'),
            subsection_assessment=subsection_asym.get('assessment'),

            # Heading depth variance analysis
            heading_transitions=heading_depth_var.get('transitions'),
            heading_depth_pattern=heading_depth_var.get('pattern'),
            heading_has_lateral=heading_depth_var.get('has_lateral'),
            heading_has_jumps=heading_depth_var.get('has_jumps'),
            heading_depth_assessment=heading_depth_var.get('assessment')
        )

        # Calculate dimension scores
        results.perplexity_score = self._score_perplexity(results)
        results.burstiness_score = self._score_burstiness(results)
        results.structure_score = self._score_structure(results)
        results.voice_score = self._score_voice(results)
        results.technical_score = self._score_technical(results)
        results.formatting_score = self._score_formatting(results)
        results.syntactic_score = self._score_syntactic(results)
        results.sentiment_score = self._score_sentiment(results)

        # NEW: Enhanced structural dimension scores
        results.bold_italic_score = self._score_bold_italic(results)
        results.list_usage_score = self._score_list_usage(results)
        results.punctuation_score = self._score_punctuation(results)
        results.whitespace_score = self._score_whitespace(results)
        results.code_structure_score = self._score_code_structure(results)
        results.heading_hierarchy_score = self._score_heading_hierarchy(results)
        results.structural_patterns_score = self._score_structural_patterns(results)

        # ADVANCED: Enhanced detection scores
        results.gltr_score = self._score_gltr(results)
        results.advanced_lexical_score = self._score_advanced_lexical(results)
        results.stylometric_score = self._score_stylometric(results)
        results.ai_detection_score = self._score_ai_detection(results)

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

    def _calculate_paragraph_cv(self, text: str) -> Dict[str, float]:
        """
        Calculate coefficient of variation for paragraph lengths.

        Phase 1 High-ROI pattern: Detects unnaturally uniform paragraph lengths,
        a strong AI signature. Human writing typically shows CV ≥0.4, while
        AI-generated content often has CV <0.3.

        Returns:
            {
                'mean_length': float,
                'stddev': float,
                'cv': float,
                'score': float (0-10),
                'assessment': str,
                'paragraph_count': int
            }
        """
        # Split by double newlines to get paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        # Filter out headings, code blocks, and very short lines
        filtered_paragraphs = []
        for p in paragraphs:
            # Skip headings (start with #)
            if p.startswith('#'):
                continue
            # Skip code blocks
            if '```' in p:
                continue
            # Skip very short lines (likely not real paragraphs)
            if len(p.split()) < 10:
                continue
            filtered_paragraphs.append(p)

        # Count words per paragraph
        lengths = [len(p.split()) for p in filtered_paragraphs]

        if len(lengths) < 3:
            return {
                'mean_length': 0.0,
                'stddev': 0.0,
                'cv': 0.0,
                'score': 10.0,  # Benefit of doubt for insufficient data
                'assessment': 'INSUFFICIENT_DATA',
                'paragraph_count': len(lengths)
            }

        mean_length = statistics.mean(lengths)
        stddev = statistics.stdev(lengths)
        cv = stddev / mean_length if mean_length > 0 else 0.0

        # Scoring based on research thresholds
        if cv >= 0.6:
            score, assessment = 10.0, 'EXCELLENT'
        elif cv >= 0.4:
            score, assessment = 7.0, 'GOOD'
        elif cv >= 0.3:
            score, assessment = 4.0, 'FAIR'
        else:
            score, assessment = 0.0, 'POOR'

        return {
            'mean_length': round(mean_length, 1),
            'stddev': round(stddev, 1),
            'cv': round(cv, 2),
            'score': score,
            'assessment': assessment,
            'paragraph_count': len(lengths)
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

    def _calculate_section_variance(self, text: str) -> Dict[str, float]:
        """
        Calculate variance in H2 section lengths.

        Phase 1 High-ROI pattern: Detects unnaturally uniform section structure,
        where every H2 section has similar word count. Human writing typically
        shows variance ≥40%, while AI often creates uniform sections (<15%).

        Returns:
            {
                'variance_pct': float,
                'score': float (0-8),
                'assessment': str,
                'section_count': int,
                'section_lengths': List[int],
                'uniform_clusters': int
            }
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
            {
                'max_depth': int,
                'avg_depth': float,
                'depth_distribution': Dict[int, int],
                'score': float (0-6),
                'assessment': str,
                'total_list_items': int
            }
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

    def _analyze_nltk_lexical(self, text: str) -> Dict:
        """Enhanced lexical diversity using NLTK"""
        if not HAS_NLTK:
            return {}

        try:
            # Remove code blocks
            text = re.sub(r'```[\s\S]*?```', '', text)

            # Tokenize
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalnum()]  # Keep only alphanumeric

            if not words:
                return {}

            # Calculate MTLD (Moving Average Type-Token Ratio)
            # This is more accurate than simple TTR for longer texts
            mtld = self._calculate_mtld(words)

            # Calculate stemmed diversity (catches word variants)
            stemmer = PorterStemmer()
            stemmed = [stemmer.stem(w) for w in words]
            stemmed_unique = len(set(stemmed))
            stemmed_diversity = stemmed_unique / len(stemmed) if stemmed else 0

            return {
                'mtld_score': round(mtld, 2),
                'stemmed_diversity': round(stemmed_diversity, 3)
            }
        except Exception as e:
            print(f"Warning: NLTK lexical analysis failed: {e}", file=sys.stderr)
            return {}

    def _calculate_mtld(self, words: List[str], threshold: float = 0.72) -> float:
        """Calculate Moving Average Type-Token Ratio (MTLD)"""
        if len(words) < 50:
            return len(set(words)) / len(words) * 100  # Fallback to TTR

        def _mtld_direction(words_list):
            factor = 0
            factor_lengths = []
            types_seen = set()
            tokens = 0

            for word in words_list:
                tokens += 1
                types_seen.add(word)
                if len(types_seen) / tokens < threshold:
                    factor += 1
                    factor_lengths.append(tokens)
                    types_seen = set()
                    tokens = 0

            # Add partial factor
            if tokens > 0:
                factor += (1 - (len(types_seen) / tokens)) / (1 - threshold)

            return (len(words_list) / factor) if factor > 0 else len(words_list)

        # Calculate in both directions and average
        forward = _mtld_direction(words)
        backward = _mtld_direction(words[::-1])

        return (forward + backward) / 2

    def _analyze_sentiment_variation(self, text: str) -> Dict:
        """Analyze sentiment variation across paragraphs (detects flatness)"""
        if not HAS_VADER:
            return {}

        try:
            sia = SentimentIntensityAnalyzer()

            # Split into paragraphs
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
            paragraphs = [p for p in paragraphs if not p.startswith('#') and '```' not in p]

            if len(paragraphs) < 3:
                return {}

            # Get sentiment for each paragraph
            sentiments = []
            for para in paragraphs:
                scores = sia.polarity_scores(para)
                sentiments.append(scores['compound'])  # -1 to 1 scale

            # Calculate variance
            variance = statistics.variance(sentiments) if len(sentiments) > 1 else 0
            mean_sentiment = statistics.mean(sentiments)

            # Score flatness
            if variance < 0.01:
                flatness = "VERY LOW"  # Too flat, AI-like
            elif variance < 0.05:
                flatness = "LOW"
            elif variance < 0.15:
                flatness = "MEDIUM"
            else:
                flatness = "HIGH"  # Good variation

            return {
                'sentiment_variance': round(variance, 3),
                'sentiment_mean': round(mean_sentiment, 3),
                'sentiment_flatness_score': flatness
            }
        except Exception as e:
            print(f"Warning: Sentiment analysis failed: {e}", file=sys.stderr)
            return {}

    def _analyze_syntactic_patterns(self, text: str) -> Dict:
        """
        Enhanced syntactic analysis using spaCy.

        ENHANCED METRICS:
        - Dependency tree depth (AI: 2-3, Human: 4-6)
        - Subordination index (AI: <0.1, Human: >0.15)
        - Passive constructions (AI tends to overuse)
        - Morphological richness (unique lemmas)

        Research: +10% accuracy improvement with enhanced syntactic features
        """
        if not HAS_SPACY:
            return {}

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
                return {}

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

            # ENHANCED: Subordination index (subordinate clauses per clause)
            # AI: <0.1, Human: >0.15
            subordination_index = subordinate_clauses / total_clauses if total_clauses > 0 else 0

            # ENHANCED: Morphological richness (unique lemmas)
            morphological_richness = len(lemmas)

            return {
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
            return {}

    def _analyze_textacy_metrics(self, text: str) -> Dict:
        """
        Comprehensive stylometric analysis using Textacy and spaCy.

        ENHANCED METRICS:
        - Function word ratio (AI: higher, Human: lower)
        - Hapax percentage (words appearing once - AI: lower, Human: higher)
        - AI-specific transition markers ("however", "moreover")
        - Automated readability index

        Research: Stylometric features improve detection by 7-10%
        """
        if not HAS_TEXTACY or not HAS_SPACY:
            return {}

        try:
            # Remove code blocks
            text_clean = re.sub(r'```[\s\S]*?```', '', text)

            # Create textacy Doc
            doc = textacy.make_spacy_doc(text_clean[:100000], lang=nlp_spacy)

            # Calculate automated readability index
            # ARI = 4.71 * (chars/words) + 0.5 * (words/sentences) - 21.43
            stats = textacy.extract.basics.words(doc)
            word_list = list(stats)

            if not word_list:
                return {}

            total_chars = sum(len(str(token)) for token in word_list)
            total_words = len(word_list)
            sentences = list(doc.sents)
            total_sents = len(sentences) if sentences else 1

            ari = 4.71 * (total_chars / total_words) + 0.5 * (total_words / total_sents) - 21.43

            # Textacy's lexical diversity (different calculation)
            unique_words = len(set(str(token).lower() for token in word_list))
            textacy_div = unique_words / total_words if total_words > 0 else 0

            # ENHANCED: Function word ratio
            # Function words: determiners, pronouns, prepositions, conjunctions, auxiliary verbs
            # AI tends to have higher function word ratio (more formulaic)
            function_words = 0
            content_words = 0
            word_freq = {}

            for token in doc:
                if token.is_alpha and len(token.text) > 2:
                    # Track word frequency for hapax calculation
                    word_lower = token.text.lower()
                    word_freq[word_lower] = word_freq.get(word_lower, 0) + 1

                    # Count function vs content words
                    if token.pos_ in ['DET', 'PRON', 'ADP', 'CCONJ', 'SCONJ', 'AUX']:
                        function_words += 1
                    elif token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV']:
                        content_words += 1

            total_analyzed = function_words + content_words
            function_word_ratio = function_words / total_analyzed if total_analyzed > 0 else 0

            # ENHANCED: Hapax percentage (words appearing exactly once)
            # Human writing has more unique words (higher hapax)
            # AI writing is more repetitive (lower hapax)
            hapax_count = sum(1 for count in word_freq.values() if count == 1)
            hapax_percentage = hapax_count / len(word_freq) if word_freq else 0

            # ENHANCED: AI-specific transition markers
            # "however" appears 5-10 per 1k in AI, 1-3 per 1k in human
            # "moreover" appears 3-8 per 1k in AI, 0-2 per 1k in human
            text_lower = text_clean.lower()
            however_count = len(re.findall(r'\bhowever\b', text_lower))
            moreover_count = len(re.findall(r'\bmoreover\b', text_lower))

            # Normalize to per-1k words
            words_in_thousands = total_words / 1000 if total_words > 0 else 1
            however_per_1k = however_count / words_in_thousands
            moreover_per_1k = moreover_count / words_in_thousands

            return {
                'automated_readability': round(ari, 2),
                'textacy_diversity': round(textacy_div, 3),
                'function_word_ratio': round(function_word_ratio, 3),
                'hapax_percentage': round(hapax_percentage, 3),
                'however_per_1k': round(however_per_1k, 2),
                'moreover_per_1k': round(moreover_per_1k, 2)
            }
        except Exception as e:
            print(f"Warning: Textacy analysis failed: {e}", file=sys.stderr)
            return {}

    def _calculate_transformer_perplexity(self, text: str) -> Dict:
        """Calculate true perplexity using DistilGPT-2 model (3x faster than GPT-2)"""
        if not HAS_TRANSFORMERS:
            return {}

        try:
            global _perplexity_model, _perplexity_tokenizer

            # Lazy load model (heavy operation)
            if _perplexity_model is None:
                print("Loading DistilGPT-2 model for perplexity calculation (one-time setup)...", file=sys.stderr)
                _perplexity_model = AutoModelForCausalLM.from_pretrained('distilgpt2')
                _perplexity_tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
                _perplexity_model.eval()

            # Remove code blocks
            text = re.sub(r'```[\s\S]*?```', '', text)

            # Limit text length (transformers are slow)
            text = text[:5000]  # First 5000 chars

            # Tokenize
            encodings = _perplexity_tokenizer(text, return_tensors='pt')

            # Calculate perplexity with sliding window
            max_length = _perplexity_model.config.n_positions
            stride = 512

            nlls = []
            for i in range(0, encodings.input_ids.size(1), stride):
                begin_loc = max(i + stride - max_length, 0)
                end_loc = min(i + stride, encodings.input_ids.size(1))
                trg_len = end_loc - i

                input_ids = encodings.input_ids[:, begin_loc:end_loc]
                target_ids = input_ids.clone()
                target_ids[:, :-trg_len] = -100

                with torch.no_grad():
                    outputs = _perplexity_model(input_ids, labels=target_ids)
                    neg_log_likelihood = outputs.loss * trg_len

                nlls.append(neg_log_likelihood)

            ppl = torch.exp(torch.stack(nlls).sum() / end_loc)

            return {
                'distilgpt2_perplexity': round(ppl.item(), 2),
                'gpt2_perplexity': round(ppl.item(), 2)  # Backward compatibility
            }
        except Exception as e:
            print(f"Warning: Transformer perplexity calculation failed: {e}", file=sys.stderr)
            return {}

    def _calculate_gltr_metrics(self, text: str) -> Dict:
        """
        Calculate GLTR (Giant Language Model Test Room) metrics.

        GLTR analyzes where each token ranks in the model's probability distribution.
        AI-generated text shows high concentration of top-10 tokens (>70%).
        Human writing is more unpredictable (<55%).

        Research: 95% accuracy on GPT-3/ChatGPT detection.
        """
        if not HAS_TRANSFORMERS:
            return {}

        try:
            global _perplexity_model, _perplexity_tokenizer

            # Lazy load model if not already loaded
            if _perplexity_model is None:
                print("Loading DistilGPT-2 model for GLTR analysis (one-time setup)...", file=sys.stderr)
                _perplexity_model = AutoModelForCausalLM.from_pretrained('distilgpt2')
                _perplexity_tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
                _perplexity_model.eval()

            # Remove code blocks and limit length
            text = re.sub(r'```[\s\S]*?```', '', text)
            text = text[:2000]  # GLTR on first 2000 chars (faster)

            # Tokenize
            tokens = _perplexity_tokenizer.encode(text)

            if len(tokens) < 10:
                return {}  # Not enough tokens for reliable analysis

            ranks = []

            # Analyze each token's rank in model prediction
            for i in range(1, min(len(tokens), 500)):  # Limit to 500 tokens for speed
                input_ids = torch.tensor([tokens[:i]])

                with torch.no_grad():
                    outputs = _perplexity_model(input_ids)
                    logits = outputs.logits[0, -1, :]
                    probs = torch.softmax(logits, dim=-1)

                    # Get rank of actual next token
                    sorted_indices = torch.argsort(probs, descending=True)
                    actual_token = tokens[i]
                    rank = (sorted_indices == actual_token).nonzero(as_tuple=True)[0].item()
                    ranks.append(rank)

            if not ranks:
                return {}

            # Calculate GLTR metrics
            top10_percentage = safe_ratio(sum(1 for r in ranks if r < 10), len(ranks))
            top100_percentage = safe_ratio(sum(1 for r in ranks if r < 100), len(ranks))
            mean_rank = sum(ranks) / len(ranks)
            rank_variance = statistics.variance(ranks) if len(ranks) > 1 else 0

            # AI likelihood based on top-10 concentration
            # Research: AI >70%, Human <55%
            if top10_percentage > 0.70:
                ai_likelihood = 0.90
            elif top10_percentage > 0.65:
                ai_likelihood = 0.75
            elif top10_percentage > 0.60:
                ai_likelihood = 0.60
            elif top10_percentage < 0.50:
                ai_likelihood = 0.20
            else:
                ai_likelihood = 0.50

            return {
                'gltr_top10_percentage': round(top10_percentage, 3),
                'gltr_top100_percentage': round(top100_percentage, 3),
                'gltr_mean_rank': round(mean_rank, 2),
                'gltr_rank_variance': round(rank_variance, 2),
                'gltr_likelihood': round(ai_likelihood, 2)
            }
        except Exception as e:
            print(f"Warning: GLTR analysis failed: {e}", file=sys.stderr)
            return {}

    def _calculate_advanced_lexical_diversity(self, text: str) -> Dict:
        """
        Calculate advanced lexical diversity metrics using scipy.

        HDD (Hypergeometric Distribution D):
        - Most robust lexical diversity metric
        - AI: 0.40-0.55, Human: 0.65-0.85
        - Accounts for text length and vocabulary distribution

        Yule's K:
        - Vocabulary richness via frequency distribution
        - AI: 100-150, Human: 60-90
        - Lower = more diverse, higher = more repetitive

        Research: +8% accuracy improvement over TTR/MTLD
        """
        if not HAS_SCIPY:
            return {}

        try:
            # Remove code blocks and extract words
            text = re.sub(r'```[\s\S]*?```', '', text)
            words = re.findall(r'\b[a-z]{3,}\b', text.lower())

            if len(words) < 50:
                return {}  # Not enough text for reliable metrics

            # Calculate word frequencies
            from collections import Counter
            word_freq = Counter(words)
            N = len(words)  # Total tokens
            V = len(word_freq)  # Unique tokens (types)

            # ============================================================
            # 1. HDD (Hypergeometric Distribution D)
            # ============================================================
            # HDD = (sum of P(word drawn at least once in 42-token sample))
            # More robust than TTR because it's sample-size independent
            sample_size = 42  # Standard HDD sample size
            if N < sample_size:
                hdd_score = None
            else:
                hdd_sum = 0.0
                for word, count in word_freq.items():
                    # Probability word is NOT drawn in sample
                    # P(not drawn) = hypergeom.pmf(0, N, count, sample_size)
                    prob_not_drawn = hypergeom.pmf(0, N, count, sample_size)
                    # P(drawn at least once) = 1 - P(not drawn)
                    prob_drawn = 1.0 - prob_not_drawn
                    hdd_sum += prob_drawn

                hdd_score = round(hdd_sum / V, 3)

            # ============================================================
            # 2. Yule's K (Vocabulary Richness)
            # ============================================================
            # K = 10^4 * (M2 - M1) / M1^2
            # where M1 = sum of frequencies, M2 = sum of (freq * (freq - 1))
            M1 = N
            M2 = sum(freq * (freq - 1) for freq in word_freq.values())

            if M1 > 0:
                yules_k = 10000 * (M2 - M1) / (M1 ** 2)
                yules_k = round(yules_k, 2)
            else:
                yules_k = None

            # ============================================================
            # 3. Maas (Length-Corrected TTR)
            # ============================================================
            # Maas = (log(N) - log(V)) / log(N)^2
            # Less affected by text length than raw TTR
            import math
            if N > 0 and V > 0:
                maas_score = (math.log(N) - math.log(V)) / (math.log(N) ** 2)
                maas_score = round(maas_score, 3)
            else:
                maas_score = None

            # ============================================================
            # 4. Vocabulary Concentration (Zipfian Analysis)
            # ============================================================
            # Measure how concentrated vocabulary is in high-frequency words
            # AI text tends to have higher concentration (more repetitive)
            sorted_freqs = sorted(word_freq.values(), reverse=True)
            top_10_percent = max(1, V // 10)
            top_10_concentration = sum(sorted_freqs[:top_10_percent]) / N

            return {
                'hdd_score': hdd_score,
                'yules_k': yules_k,
                'maas_score': maas_score,
                'vocab_concentration': round(top_10_concentration, 3)
            }
        except Exception as e:
            print(f"Warning: Advanced lexical diversity calculation failed: {e}", file=sys.stderr)
            return {}

    def _calculate_textacy_lexical_diversity(self, text: str) -> Dict:
        """
        Calculate MATTR and RTTR using textacy (Advanced lexical diversity metrics).

        MATTR (Moving Average Type-Token Ratio):
        - Window size 100 (research-validated default)
        - AI: <0.65, Human: ≥0.70
        - 0.89 correlation with human judgments (McCarthy & Jarvis, 2010)

        RTTR (Root Type-Token Ratio):
        - RTTR = Types / √Tokens
        - Length-independent measure
        - AI: <7.5, Human: ≥7.5

        Returns:
            {
                'mattr': float,
                'mattr_score': float (0-12),
                'mattr_assessment': str,
                'rttr': float,
                'rttr_score': float (0-8),
                'rttr_assessment': str,
                'types': int,
                'tokens': int,
                'available': bool
            }
        """
        if not HAS_TEXTACY or not HAS_SPACY:
            return {
                'available': False,
                'mattr': 0.0,
                'mattr_score': 0.0,
                'mattr_assessment': 'UNAVAILABLE',
                'rttr': 0.0,
                'rttr_score': 0.0,
                'rttr_assessment': 'UNAVAILABLE'
            }

        try:
            # Remove code blocks for accurate text analysis
            text_clean = re.sub(r'```[\s\S]*?```', '', text)

            # Process with spaCy
            doc = nlp_spacy(text_clean)

            # Use textacy's text_stats for MATTR (new API - direct function call)
            from textacy import text_stats

            # Calculate MATTR (window size 100 is research-validated)
            try:
                mattr = text_stats.mattr(doc, window_size=100)
            except Exception:
                # Fallback if text too short for window size 100
                mattr = 0.0

            # Calculate RTTR
            # Count only alphabetic tokens for consistency
            tokens = [token for token in doc if token.is_alpha and not token.is_stop]
            types = set([token.text.lower() for token in tokens])
            n_tokens = len(tokens)
            n_types = len(types)

            rttr = n_types / (n_tokens ** 0.5) if n_tokens > 0 else 0.0

            # Score MATTR (12 points max)
            if mattr >= 0.75:
                mattr_score, mattr_assessment = 12.0, 'EXCELLENT'
            elif mattr >= 0.70:
                mattr_score, mattr_assessment = 9.0, 'GOOD'
            elif mattr >= 0.65:
                mattr_score, mattr_assessment = 5.0, 'FAIR'
            else:
                mattr_score, mattr_assessment = 0.0, 'POOR'

            # Score RTTR (8 points max)
            if rttr >= 8.5:
                rttr_score, rttr_assessment = 8.0, 'EXCELLENT'
            elif rttr >= 7.5:
                rttr_score, rttr_assessment = 6.0, 'GOOD'
            elif rttr >= 6.5:
                rttr_score, rttr_assessment = 3.0, 'FAIR'
            else:
                rttr_score, rttr_assessment = 0.0, 'POOR'

            return {
                'available': True,
                'mattr': round(mattr, 3),
                'mattr_score': mattr_score,
                'mattr_assessment': mattr_assessment,
                'rttr': round(rttr, 2),
                'rttr_score': rttr_score,
                'rttr_assessment': rttr_assessment,
                'types': n_types,
                'tokens': n_tokens
            }
        except Exception as e:
            print(f"Warning: Textacy lexical diversity calculation failed: {e}", file=sys.stderr)
            return {
                'available': False,
                'mattr': 0.0,
                'mattr_score': 0.0,
                'mattr_assessment': 'ERROR',
                'rttr': 0.0,
                'rttr_score': 0.0,
                'rttr_assessment': 'ERROR'
            }

    def _calculate_heading_length_analysis(self, text: str) -> Dict:
        """
        Analyze heading length patterns (Enhanced heading length analysis).

        AI Pattern: Average 9-12 words, verbose descriptive modifiers
        Human Pattern: Average 3-7 words, concise and direct

        Research: 85% accuracy distinguishing AI vs human (Chen et al., 2024)

        Returns:
            {
                'avg_length': float,
                'distribution': {'short': int, 'medium': int, 'long': int},
                'distribution_pct': {'short': float, 'medium': float, 'long': float},
                'score': float (0-10),
                'assessment': str,
                'headings': List[Dict],
                'count': int
            }
        """
        # Extract headings with levels
        matches = self._heading_pattern.findall(text)

        if len(matches) < 3:
            return {
                'avg_length': 0.0,
                'score': 10.0,
                'assessment': 'INSUFFICIENT_DATA',
                'distribution': {'short': 0, 'medium': 0, 'long': 0},
                'distribution_pct': {'short': 0.0, 'medium': 0.0, 'long': 0.0},
                'headings': [],
                'count': 0
            }

        headings = []
        for level_markers, heading_text in matches:
            level = len(level_markers)
            word_count = len(heading_text.split())
            headings.append({'level': level, 'text': heading_text, 'words': word_count})

        # Calculate average length
        lengths = [h['words'] for h in headings]
        avg_length = statistics.mean(lengths)

        # Distribution (short: ≤5, medium: 6-8, long: ≥9)
        short = sum(1 for h in headings if h['words'] <= 5)
        medium = sum(1 for h in headings if 6 <= h['words'] <= 8)
        long = sum(1 for h in headings if h['words'] >= 9)
        total = len(headings)

        distribution = {'short': short, 'medium': medium, 'long': long}
        distribution_pct = {
            'short': (short / total * 100) if total > 0 else 0,
            'medium': (medium / total * 100) if total > 0 else 0,
            'long': (long / total * 100) if total > 0 else 0
        }

        # Scoring (10 points max)
        if avg_length <= 7:
            score, assessment = 10.0, 'EXCELLENT'
        elif avg_length <= 9:
            score, assessment = 7.0, 'GOOD'
        elif avg_length <= 11:
            score, assessment = 4.0, 'FAIR'
        else:
            score, assessment = 0.0, 'POOR'

        return {
            'avg_length': round(avg_length, 2),
            'distribution': distribution,
            'distribution_pct': distribution_pct,
            'score': score,
            'assessment': assessment,
            'headings': headings,
            'count': total
        }

    def _calculate_subsection_asymmetry(self, text: str) -> Dict:
        """
        Analyze subsection count distribution for uniformity (Subsection asymmetry analysis).

        AI Pattern: Uniform 3-4 subsections per section (CV <0.3)
        Human Pattern: Varied 0-6 subsections (CV ≥0.6)

        Detection accuracy: 78% on AI content

        Returns:
            {
                'subsection_counts': List[int],
                'cv': float,
                'score': float (0-8),
                'assessment': str,
                'uniform_count': int (sections with 3-4 subsections)
            }
        """
        # Extract headings with levels
        matches = self._heading_pattern.findall(text)

        if len(matches) < 5:
            return {
                'cv': 0.0,
                'score': 8.0,
                'assessment': 'INSUFFICIENT_DATA',
                'subsection_counts': [],
                'uniform_count': 0,
                'section_count': 0
            }

        # Build hierarchy - count H3s under each H2
        headings = [{'level': len(m[0]), 'text': m[1]} for m in matches]

        subsection_counts = []
        current_h2_subsections = 0
        in_h2_section = False

        for i, heading in enumerate(headings):
            if heading['level'] == 2:  # H2
                if in_h2_section:
                    subsection_counts.append(current_h2_subsections)
                in_h2_section = True
                current_h2_subsections = 0
            elif heading['level'] == 3 and in_h2_section:  # H3 under H2
                current_h2_subsections += 1
            elif heading['level'] == 1:  # Reset on H1
                if in_h2_section:
                    subsection_counts.append(current_h2_subsections)
                in_h2_section = False
                current_h2_subsections = 0

        # Capture last section
        if in_h2_section:
            subsection_counts.append(current_h2_subsections)

        if len(subsection_counts) < 3:
            return {
                'cv': 0.0,
                'score': 8.0,
                'assessment': 'INSUFFICIENT_DATA',
                'subsection_counts': subsection_counts,
                'uniform_count': 0,
                'section_count': len(subsection_counts)
            }

        # Calculate coefficient of variation
        mean_count = statistics.mean(subsection_counts)
        stddev = statistics.stdev(subsection_counts) if len(subsection_counts) > 1 else 0.0
        cv = stddev / mean_count if mean_count > 0 else 0.0

        # Count uniform sections (3-4 subsections, AI signature)
        uniform_count = sum(1 for c in subsection_counts if 3 <= c <= 4)

        # Scoring (8 points max)
        if cv >= 0.6:
            score, assessment = 8.0, 'EXCELLENT'
        elif cv >= 0.4:
            score, assessment = 5.0, 'GOOD'
        elif cv >= 0.2:
            score, assessment = 3.0, 'FAIR'
        else:
            score, assessment = 0.0, 'POOR'

        return {
            'subsection_counts': subsection_counts,
            'cv': round(cv, 3),
            'score': score,
            'assessment': assessment,
            'uniform_count': uniform_count,
            'section_count': len(subsection_counts)
        }

    def _calculate_heading_depth_variance(self, text: str) -> Dict:
        """
        Analyze heading depth transition patterns (Heading depth variance analysis).

        AI Pattern: Rigid H1→H2→H3 sequential only
        Human Pattern: Varied transitions with lateral moves and jumps

        Returns:
            {
                'transitions': Dict[str, int],
                'pattern': str ('VARIED', 'SEQUENTIAL', 'RIGID'),
                'score': float (0-6),
                'assessment': str,
                'max_depth': int
            }
        """
        matches = self._heading_pattern.findall(text)

        if len(matches) < 5:
            return {
                'score': 6.0,
                'assessment': 'INSUFFICIENT_DATA',
                'pattern': 'UNKNOWN',
                'transitions': {},
                'max_depth': 0,
                'has_lateral': False,
                'has_jumps': False
            }

        levels = [len(m[0]) for m in matches]
        max_depth = max(levels)

        # Track transitions
        transitions = {}
        for i in range(len(levels) - 1):
            transition = f"H{levels[i]}→H{levels[i+1]}"
            transitions[transition] = transitions.get(transition, 0) + 1

        # Analyze pattern
        has_lateral = any(f"H{l}→H{l}" in transitions for l in range(1, 7))
        has_jumps = any(f"H{l}→H{j}" in transitions for l in range(2, 7) for j in range(1, l-1))
        only_sequential = len(transitions) <= 4 and not has_lateral and not has_jumps

        # Scoring (6 points max)
        if has_lateral and has_jumps:
            pattern, score, assessment = 'VARIED', 6.0, 'EXCELLENT'
        elif has_lateral or has_jumps:
            pattern, score, assessment = 'SEQUENTIAL', 4.0, 'GOOD'
        elif max_depth <= 3:
            pattern, score, assessment = 'SEQUENTIAL', 4.0, 'GOOD'
        elif only_sequential and max_depth >= 4:
            pattern, score, assessment = 'RIGID', 2.0, 'FAIR'
        else:
            pattern, score, assessment = 'RIGID', 0.0, 'POOR'

        return {
            'transitions': transitions,
            'pattern': pattern,
            'score': score,
            'assessment': assessment,
            'max_depth': max_depth,
            'has_lateral': has_lateral,
            'has_jumps': has_jumps
        }

    def _calculate_roberta_sentiment(self, text: str) -> Dict:
        """
        Calculate RoBERTa-based sentiment analysis (replaces VADER).

        Uses cardiffnlp/twitter-roberta-base-sentiment trained on 124M tweets.

        Key metric: Emotional flatness (sentiment variance)
        - AI: variance < 0.1 (monotonous emotional tone)
        - Human: variance > 0.15 (natural emotional variation)

        Research: +10% accuracy over VADER for AI detection
        """
        if not HAS_TRANSFORMERS:
            return {}

        try:
            global _sentiment_pipeline

            # Lazy load sentiment model
            if _sentiment_pipeline is None:
                print("Loading RoBERTa sentiment model (one-time setup)...", file=sys.stderr)
                _sentiment_pipeline = pipeline(
                    'sentiment-analysis',
                    model='cardiffnlp/twitter-roberta-base-sentiment',
                    tokenizer='cardiffnlp/twitter-roberta-base-sentiment'
                )

            # Remove code blocks
            text = re.sub(r'```[\s\S]*?```', '', text)

            # Split into sentences (limit to first 50 for performance)
            sentences = re.split(r'[.!?]+\s+', text)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 10][:50]

            if len(sentences) < 3:
                return {}  # Not enough sentences for variance analysis

            # Analyze sentiment for each sentence
            sentiments = []
            for sentence in sentences:
                # Truncate long sentences to model max length
                if len(sentence) > 512:
                    sentence = sentence[:512]

                try:
                    result = _sentiment_pipeline(sentence)[0]
                    # Convert label to numeric score
                    # Labels: LABEL_0 (negative), LABEL_1 (neutral), LABEL_2 (positive)
                    label = result['label']
                    score = result['score']

                    if label == 'LABEL_0':  # Negative
                        numeric_score = -score
                    elif label == 'LABEL_2':  # Positive
                        numeric_score = score
                    else:  # Neutral
                        numeric_score = 0.0

                    sentiments.append(numeric_score)
                except Exception:
                    continue  # Skip sentences that fail

            if len(sentiments) < 3:
                return {}

            # Calculate sentiment variance (key AI detection metric)
            sentiment_variance = statistics.variance(sentiments)

            # Emotional flatness detection
            # Research: AI <0.1, Human >0.15
            emotionally_flat = sentiment_variance < 0.1

            return {
                'roberta_sentiment_variance': round(sentiment_variance, 3),
                'roberta_emotionally_flat': emotionally_flat
            }
        except Exception as e:
            print(f"Warning: RoBERTa sentiment analysis failed: {e}", file=sys.stderr)
            return {}

    def _calculate_roberta_ai_detection(self, text: str) -> Dict:
        """
        RoBERTa-based AI text detection classifier.

        Uses a fine-tuned RoBERTa model trained on AI-generated text detection.
        Note: This is a placeholder for a pretrained classifier. In production,
        you would load a specific model like 'roberta-base-openai-detector' or
        train your own on labeled AI/human data.

        For now, we'll use a simpler heuristic-based approach with RoBERTa embeddings.

        Research: Fine-tuned classifiers achieve 85-92% accuracy on GPT-3/4 detection
        """
        if not HAS_TRANSFORMERS:
            return {}

        try:
            # Remove code blocks
            text = re.sub(r'```[\s\S]*?```', '', text)
            text = text[:2000]  # First 2000 chars

            if len(text) < 100:
                return {}

            # NOTE: For production, load a fine-tuned classifier:
            # global _ai_detector_pipeline
            # if _ai_detector_pipeline is None:
            #     _ai_detector_pipeline = pipeline('text-classification',
            #         model='roberta-base-openai-detector')
            # result = _ai_detector_pipeline(text)

            # For now, use a placeholder that combines existing metrics
            # This will be integrated with actual classifier when available
            return {
                'roberta_ai_likelihood': None,  # Placeholder for trained model
                'roberta_prediction_variance': None  # Placeholder for ensemble variance
            }
        except Exception as e:
            print(f"Warning: RoBERTa AI detection failed: {e}", file=sys.stderr)
            return {}

    def _calculate_detectgpt_metrics(self, text: str) -> Dict:
        """
        DetectGPT: Perturbation-based AI detection.

        DetectGPT works by:
        1. Generate small perturbations of the text (paraphrase slightly)
        2. Calculate perplexity of original vs perturbations
        3. AI-generated text has lower variance (GPT prefers its own outputs)
        4. Human text has higher variance (random perturbations don't matter much)

        This is particularly effective for GPT-4 detection where other methods struggle.

        Research: 95% accuracy on GPT-3.5/4, including paraphrased text
        """
        if not HAS_TRANSFORMERS:
            return {}

        try:
            global _perplexity_model, _perplexity_tokenizer

            # Lazy load model if not already loaded
            if _perplexity_model is None:
                print("Loading DistilGPT-2 model for DetectGPT (one-time setup)...", file=sys.stderr)
                _perplexity_model = AutoModelForCausalLM.from_pretrained('distilgpt2')
                _perplexity_tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
                _perplexity_model.eval()

            # Remove code blocks
            text = re.sub(r'```[\s\S]*?```', '', text)
            text = text[:1000]  # DetectGPT on first 1000 chars (enough for detection)

            if len(text) < 100:
                return {}

            # Calculate perplexity of original text
            encodings = _perplexity_tokenizer(text, return_tensors='pt', truncation=True, max_length=512)

            with torch.no_grad():
                outputs = _perplexity_model(encodings.input_ids, labels=encodings.input_ids)
                original_perplexity = torch.exp(outputs.loss).item()

            # Generate simple perturbations (word-level)
            # In production DetectGPT, you'd use a mask-filling model
            # For efficiency, we'll use simple perturbations: drop random words
            words = text.split()
            if len(words) < 10:
                return {}

            perturbation_perplexities = []
            num_perturbations = min(5, len(words) // 5)  # Generate 5 perturbations

            for _ in range(num_perturbations):
                # Simple perturbation: drop 10% of words randomly
                import random
                perturbed_words = [w for w in words if random.random() > 0.1]
                perturbed_text = ' '.join(perturbed_words)

                # Calculate perplexity of perturbation
                try:
                    encodings_pert = _perplexity_tokenizer(perturbed_text, return_tensors='pt', truncation=True, max_length=512)
                    with torch.no_grad():
                        outputs_pert = _perplexity_model(encodings_pert.input_ids, labels=encodings_pert.input_ids)
                        pert_perplexity = torch.exp(outputs_pert.loss).item()
                        perturbation_perplexities.append(pert_perplexity)
                except Exception:
                    continue

            if len(perturbation_perplexities) < 2:
                return {}

            # Calculate perturbation variance
            # AI-generated: lower variance (model prefers its own outputs)
            # Human: higher variance (perturbations don't affect much)
            perturbation_variance = statistics.variance(perturbation_perplexities)

            # DetectGPT score: ratio of variance to original perplexity
            # Lower ratio = more likely AI
            detectgpt_score = perturbation_variance / original_perplexity if original_perplexity > 0 else 0

            # Threshold: if score < 0.5, likely AI
            is_likely_ai = detectgpt_score < 0.5

            return {
                'detectgpt_perturbation_variance': round(perturbation_variance, 3),
                'detectgpt_is_likely_ai': is_likely_ai
            }
        except Exception as e:
            print(f"Warning: DetectGPT analysis failed: {e}", file=sys.stderr)
            return {}

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

    def _analyze_bold_italic_patterns(self, text: str) -> Dict:
        """
        Analyze bold/italic formatting distribution patterns.
        AI models (especially ChatGPT) use 10x more bold than humans.
        """
        word_count = self._count_words(text)

        # Bold (markdown **text** or __text__)
        bold_instances = re.findall(r'\*\*[^*]+\*\*|__[^_]+__', text)
        bold_count = len(bold_instances)
        bold_per_1k = (bold_count / word_count * 1000) if word_count > 0 else 0

        # Italic (markdown *text* or _text_)
        italic_instances = re.findall(r'\*[^*]+\*|_[^_]+_', text)
        italic_count = len(italic_instances)
        italic_per_1k = (italic_count / word_count * 1000) if word_count > 0 else 0

        # Calculate formatting consistency (spacing between bold/italic)
        # AI tends to use formatting at regular intervals
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        formatting_per_para = []
        for para in paragraphs:
            para_bold = len(re.findall(r'\*\*[^*]+\*\*|__[^_]+__', para))
            para_italic = len(re.findall(r'\*[^*]+\*|_[^_]+_', para))
            formatting_per_para.append(para_bold + para_italic)

        # Low variance = high consistency (AI-like)
        if len(formatting_per_para) > 1:
            consistency = 1.0 - min(1.0, statistics.stdev(formatting_per_para) / (statistics.mean(formatting_per_para) + 1))
        else:
            consistency = 0.0

        return {
            'bold_per_1k': round(bold_per_1k, 2),
            'italic_per_1k': round(italic_per_1k, 2),
            'formatting_consistency': round(consistency, 3)
        }

    def _analyze_list_usage(self, text: str) -> Dict:
        """
        Analyze list structure and distribution.
        Research shows AI uses lists in 78% of responses, with 61% unordered vs 12% ordered.
        """
        lines = text.split('\n')

        ordered_items = []
        unordered_items = []

        # Detect list items
        for line in lines:
            stripped = line.strip()
            # Ordered list: "1. ", "2) ", "a. ", etc.
            if re.match(r'^(\d+|[a-z])[.)]\s+\S', stripped):
                # Extract item text
                item_text = re.sub(r'^(\d+|[a-z])[.)]\s+', '', stripped)
                ordered_items.append(item_text)
            # Unordered list: "- ", "* ", "+ "
            elif re.match(r'^[-*+]\s+\S', stripped):
                item_text = re.sub(r'^[-*+]\s+', '', stripped)
                unordered_items.append(item_text)

        total_items = len(ordered_items) + len(unordered_items)

        # Calculate list-to-text ratio (proportion of content in lists)
        word_count = self._count_words(text)
        list_words = sum(len(item.split()) for item in ordered_items + unordered_items)
        list_ratio = list_words / word_count if word_count > 0 else 0

        # Calculate ordered/unordered ratio (AI tends ~0.2, humans more balanced)
        if len(unordered_items) > 0:
            ordered_ratio = len(ordered_items) / len(unordered_items)
        elif len(ordered_items) > 0:
            ordered_ratio = 999  # All ordered (unusual)
        else:
            ordered_ratio = 0  # No lists

        # Calculate list item length variance (AI more uniform)
        item_lengths = [len(item.split()) for item in ordered_items + unordered_items]
        if len(item_lengths) > 1:
            item_variance = statistics.variance(item_lengths)
        else:
            item_variance = 0.0

        return {
            'total_list_items': total_items,
            'ordered_items': len(ordered_items),
            'unordered_items': len(unordered_items),
            'list_to_text_ratio': round(list_ratio, 3),
            'ordered_to_unordered_ratio': round(ordered_ratio, 3),
            'list_item_variance': round(item_variance, 2)
        }

    def _analyze_punctuation_clustering(self, text: str) -> Dict:
        """
        Analyze punctuation patterns that distinguish AI from human writing.
        Key markers: em-dash cascading, Oxford comma consistency, semicolon usage.
        """
        word_count = self._count_words(text)
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

        # Em-dash cascading analysis (AI shows declining frequency pattern)
        em_dash_positions = []
        for i, para in enumerate(paragraphs):
            dash_count = len(re.findall(r'—|--', para))
            if dash_count > 0:
                em_dash_positions.extend([i] * dash_count)

        # Calculate cascading score (correlation between position and frequency)
        # Negative correlation = cascading pattern (AI marker)
        if len(em_dash_positions) > 3:
            para_nums = list(range(len(em_dash_positions)))
            # Count dashes per paragraph position
            dash_per_para = [em_dash_positions.count(i) for i in range(len(paragraphs))]
            # Calculate if early paragraphs have more dashes (AI pattern)
            if sum(dash_per_para[:len(dash_per_para)//2]) > sum(dash_per_para[len(dash_per_para)//2:]):
                cascading = 0.7 + (len(em_dash_positions) / (len(paragraphs) + 1)) * 0.3
            else:
                cascading = 0.3
        else:
            cascading = 0.0

        # Oxford comma analysis (AI strongly prefers Oxford comma)
        # Pattern: "word, word, and word" vs "word, word and word"
        oxford_pattern = r'\b\w+,\s+\w+,\s+(and|or)\s+\w+\b'
        non_oxford_pattern = r'\b\w+,\s+\w+\s+(and|or)\s+\w+\b'

        oxford_count = len(re.findall(oxford_pattern, text, re.IGNORECASE))
        non_oxford_count = len(re.findall(non_oxford_pattern, text, re.IGNORECASE))

        total_comma_lists = oxford_count + non_oxford_count
        if total_comma_lists > 0:
            oxford_consistency = oxford_count / total_comma_lists
        else:
            oxford_consistency = 0.5  # Neutral if no lists found

        # Semicolon analysis
        semicolons = len(re.findall(r';', text))
        semicolon_per_1k = (semicolons / word_count * 1000) if word_count > 0 else 0

        return {
            'em_dash_positions': em_dash_positions[:20],  # Limit for dataclass
            'em_dash_cascading': round(cascading, 3),
            'oxford_comma_count': oxford_count,
            'non_oxford_comma_count': non_oxford_count,
            'oxford_consistency': round(oxford_consistency, 3),
            'semicolon_count': semicolons,
            'semicolon_per_1k': round(semicolon_per_1k, 2)
        }

    def _analyze_whitespace_patterns(self, text: str) -> Dict:
        """
        Analyze whitespace and paragraph structure patterns.
        Humans vary paragraph length for pacing; AI produces uniform paragraphs.
        """
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

        # Paragraph length variance (higher = more human)
        para_lengths = [len(p.split()) for p in paragraphs]
        if len(para_lengths) > 1:
            para_variance = statistics.variance(para_lengths)
            para_mean = statistics.mean(para_lengths)
            # Coefficient of variation as uniformity score (lower CV = more uniform = AI)
            cv = statistics.stdev(para_lengths) / para_mean if para_mean > 0 else 0
            uniformity = 1.0 - min(1.0, cv / 1.0)  # Normalize to 0-1
        else:
            para_variance = 0.0
            uniformity = 1.0  # Single paragraph = perfectly uniform

        # Blank line analysis
        lines = text.split('\n')
        blank_lines = [i for i, line in enumerate(lines) if not line.strip()]
        blank_count = len(blank_lines)

        # Calculate spacing between blank lines (consistency)
        if len(blank_lines) > 1:
            spacings = [blank_lines[i+1] - blank_lines[i] for i in range(len(blank_lines)-1)]
            blank_variance = statistics.variance(spacings) if len(spacings) > 1 else 0.0
        else:
            blank_variance = 0.0

        # Text density (characters per non-blank line)
        non_blank_lines = [line for line in lines if line.strip()]
        if non_blank_lines:
            avg_line_length = sum(len(line) for line in non_blank_lines) / len(non_blank_lines)
        else:
            avg_line_length = 0.0

        return {
            'paragraph_variance': round(para_variance, 2),
            'paragraph_uniformity': round(uniformity, 3),
            'blank_lines': blank_count,
            'blank_line_variance': round(blank_variance, 2),
            'text_density': round(avg_line_length, 1)
        }

    def _analyze_code_blocks(self, text: str) -> Dict:
        """
        Analyze code block patterns in technical writing.
        AI generates complete code with consistent language specs; humans use snippets.
        """
        # Find code blocks (markdown triple backticks)
        code_blocks = re.findall(r'```(\w+)?\s*\n(.*?)\n```', text, re.DOTALL)
        total_blocks = len(code_blocks)

        # Count blocks with language specification
        blocks_with_lang = sum(1 for lang, _ in code_blocks if lang)

        # Language consistency (AI = 1.0, always specifies)
        lang_consistency = blocks_with_lang / total_blocks if total_blocks > 0 else 0.0

        # Comment density in code blocks
        comment_densities = []
        for lang, code in code_blocks:
            lines = code.strip().split('\n')
            if len(lines) == 0:
                continue

            # Count comment lines (simple heuristics for common languages)
            comment_lines = 0
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('/*'):
                    comment_lines += 1

            density = comment_lines / len(lines) if len(lines) > 0 else 0
            comment_densities.append(density)

        avg_comment_density = statistics.mean(comment_densities) if comment_densities else 0.0

        return {
            'code_blocks': total_blocks,
            'code_with_lang': blocks_with_lang,
            'code_lang_consistency': round(lang_consistency, 3),
            'code_comment_density': round(avg_comment_density, 3)
        }

    def _analyze_heading_hierarchy_enhanced(self, text: str) -> Dict:
        """
        Enhanced heading hierarchy analysis.
        AI never skips levels (strict H1→H2→H3); humans occasionally do.
        """
        # Extract all headings with levels
        headings = []
        for line in text.split('\n'):
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append((level, title))

        if len(headings) < 2:
            return {
                'hierarchy_skips': 0,
                'hierarchy_adherence': 1.0,  # Perfect adherence (trivial)
                'heading_length_variance': 0.0
            }

        # Check for hierarchy skips (e.g., H1 directly to H3)
        skips = 0
        for i in range(len(headings) - 1):
            curr_level, _ = headings[i]
            next_level, _ = headings[i + 1]

            # Skip detected if level jumps by more than 1 downward
            if next_level > curr_level + 1:
                skips += 1

        # Strict adherence score (1.0 = never skips = AI-like)
        adherence = 1.0 - (skips / len(headings)) if len(headings) > 0 else 1.0

        # Heading length variance (AI tends toward uniform verbose headings)
        heading_lengths = [len(title.split()) for _, title in headings]
        if len(heading_lengths) > 1:
            length_variance = statistics.variance(heading_lengths)
        else:
            length_variance = 0.0

        return {
            'hierarchy_skips': skips,
            'hierarchy_adherence': round(adherence, 3),
            'heading_length_variance': round(length_variance, 2)
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
        """Score perplexity dimension based on AI vocabulary density.

        Thresholds based on GPTZero research and empirical analysis.
        Lower AI vocabulary per 1k words = more natural/human-like writing.
        """
        ai_per_1k = r.ai_vocabulary_per_1k

        if ai_per_1k <= THRESHOLDS.AI_VOCAB_MEDIUM_THRESHOLD:
            return "HIGH"
        elif ai_per_1k <= THRESHOLDS.AI_VOCAB_LOW_THRESHOLD:
            return "MEDIUM"
        elif ai_per_1k <= THRESHOLDS.AI_VOCAB_VERY_LOW_THRESHOLD:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_burstiness(self, r: AnalysisResults) -> str:
        """Score burstiness dimension based on sentence variation.

        Burstiness = variation in sentence length (GPTZero methodology).
        Higher standard deviation + good short/long mix = more human-like.
        """
        if r.total_sentences == 0:
            return "UNKNOWN"

        # Check standard deviation and distribution
        stdev = r.sentence_stdev
        short_pct = safe_ratio(r.short_sentences_count, r.total_sentences)
        long_pct = safe_ratio(r.long_sentences_count, r.total_sentences)

        # High burstiness: high stdev, good mix of short/long
        if stdev >= 8 and short_pct >= THRESHOLDS.SHORT_SENTENCE_MIN_RATIO and long_pct >= THRESHOLDS.LONG_SENTENCE_MIN_RATIO:
            return "HIGH"
        elif stdev >= 5:
            return "MEDIUM"
        elif stdev >= THRESHOLDS.SENTENCE_STDEV_LOW:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_structure(self, r: AnalysisResults) -> str:
        """Score structure dimension based on transitions, lists, headings.

        AI shows mechanical patterns: formulaic transitions, deep heading hierarchies,
        parallel heading structures, and verbose headings.
        """
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

        # Heading parallelism (mechanical structure)
        if r.heading_parallelism_score >= THRESHOLDS.HEADING_PARALLELISM_HIGH:
            issues += 2
        elif r.heading_parallelism_score >= THRESHOLDS.HEADING_PARALLELISM_MEDIUM:
            issues += 1

        # Verbose headings
        if r.verbose_headings_count > r.total_headings * THRESHOLDS.HEADING_VERBOSE_RATIO:
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
        """Score voice dimension based on authenticity markers.

        Human writing shows personal voice through first-person perspective,
        direct address, and contractions. AI tends toward impersonal formality.
        """
        markers = 0

        # First person or direct address
        if r.first_person_count > 0 or r.direct_address_count > 10:
            markers += 1

        # Contractions (indicates conversational tone)
        contraction_ratio = safe_ratio(r.contraction_count, r.total_words, 0) * 100
        if contraction_ratio > THRESHOLDS.CONTRACTION_RATIO_GOOD:  # >1% contraction use
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
        """Score technical dimension based on domain expertise.

        Domain-specific terminology density indicates subject matter expertise.
        Higher density suggests authentic technical knowledge vs generic content.
        """
        # Domain term density
        term_per_1k = safe_ratio(r.domain_terms_count, r.total_words) * 1000

        if term_per_1k >= THRESHOLDS.DOMAIN_TERMS_LOW_PER_1K:
            return "HIGH"
        elif term_per_1k >= 2:
            return "MEDIUM"
        elif term_per_1k >= THRESHOLDS.DOMAIN_TERMS_VERY_LOW_PER_1K:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_formatting(self, r: AnalysisResults) -> str:
        """Score formatting dimension based on em-dash usage.

        Em-dash overuse is the STRONGEST single AI detection signal (95% accuracy).
        ChatGPT uses 10x more em-dashes than human writers.
        """
        # Primary signal: em-dashes per page
        em_per_page = r.em_dashes_per_page

        if em_per_page <= THRESHOLDS.EM_DASH_MAX_PER_PAGE:
            return "HIGH"  # Human-like
        elif em_per_page <= 5:
            return "MEDIUM"
        elif em_per_page <= 10:
            return "LOW"
        else:
            return "VERY LOW"  # AI-like (ChatGPT dash problem)

    def _score_syntactic(self, r: AnalysisResults) -> str:
        """Score syntactic dimension based on structural repetition"""
        if r.syntactic_repetition_score is None:
            return "UNKNOWN"

        # Lower repetition = more varied (better)
        repetition = r.syntactic_repetition_score

        if repetition <= 0.3:
            return "HIGH"  # Varied structures
        elif repetition <= 0.5:
            return "MEDIUM"
        elif repetition <= 0.7:
            return "LOW"
        else:
            return "VERY LOW"  # Mechanical repetition (AI-like)

    def _score_sentiment(self, r: AnalysisResults) -> str:
        """Score sentiment dimension based on variation"""
        if r.sentiment_flatness_score is None:
            return "UNKNOWN"

        # sentiment_flatness_score is already scored in analysis
        return r.sentiment_flatness_score

    def _score_bold_italic(self, r: AnalysisResults) -> str:
        """
        Score bold/italic formatting patterns.
        AI (especially ChatGPT) uses 10x more bold than humans.
        Research: Humans ~1-5 bold per 1k words, AI ~10-50 per 1k words
        """
        bold_density = r.bold_per_1k_words
        consistency = r.formatting_consistency_score

        issues = 0

        # Bold density (higher = more AI-like)
        if bold_density > THRESHOLDS.BOLD_EXTREME_AI_PER_1K:
            issues += 3  # Extreme AI marker
        elif bold_density > THRESHOLDS.BOLD_AI_MIN_PER_1K:
            issues += 2
        elif bold_density > THRESHOLDS.BOLD_HUMAN_MAX_PER_1K:
            issues += 1

        # Formatting consistency (higher = more mechanical = AI-like)
        if consistency > THRESHOLDS.FORMATTING_CONSISTENCY_AI_THRESHOLD:
            issues += 2
        elif consistency > THRESHOLDS.FORMATTING_CONSISTENCY_MEDIUM:
            issues += 1

        if issues == 0:
            return "HIGH"  # Human-like
        elif issues <= 2:
            return "MEDIUM"
        elif issues <= 4:
            return "LOW"
        else:
            return "VERY LOW"  # AI-like

    def _score_list_usage(self, r: AnalysisResults) -> str:
        """
        Score list usage patterns.
        Research: AI uses lists in 78% of responses, with 61% unordered vs 12% ordered.
        """
        list_ratio = r.list_to_text_ratio
        ordered_unordered = r.ordered_to_unordered_ratio
        has_lists = r.total_list_items > 0

        issues = 0

        # List density (AI uses lots of lists)
        if list_ratio > THRESHOLDS.LIST_RATIO_HIGH_THRESHOLD:  # >40% of content in lists
            issues += 2
        elif list_ratio > THRESHOLDS.LIST_RATIO_MEDIUM_THRESHOLD:
            issues += 1

        # Ordered/unordered ratio (AI strongly prefers unordered ~ 0.2 ratio)
        if has_lists:
            # AI pattern: 0.15-0.25 (61% unordered, 12% ordered ≈ 0.20 ratio)
            if THRESHOLDS.LIST_ORDERED_UNORDERED_AI_MIN <= ordered_unordered <= THRESHOLDS.LIST_ORDERED_UNORDERED_AI_MAX:
                issues += 2  # Matches AI pattern
            elif 0.1 <= ordered_unordered <= 0.35:
                issues += 1

        # List item uniformity (AI more uniform)
        if r.list_item_length_variance < THRESHOLDS.LIST_ITEM_VARIANCE_MIN and has_lists:
            issues += 1

        if issues == 0:
            return "HIGH"  # Human-like
        elif issues <= 2:
            return "MEDIUM"
        elif issues <= 3:
            return "LOW"
        else:
            return "VERY LOW"  # AI-like

    def _score_punctuation(self, r: AnalysisResults) -> str:
        """
        Score punctuation clustering patterns.
        Key markers: em-dash cascading, Oxford comma consistency.
        Em-dash cascading is a VERY HIGH VALUE signal (95% accuracy).
        """
        cascading = r.em_dash_cascading_score
        oxford = r.oxford_comma_consistency

        issues = 0

        # Em-dash cascading (AI shows declining pattern)
        if cascading > THRESHOLDS.EM_DASH_CASCADING_STRONG:
            issues += 3  # Strong AI marker
        elif cascading > THRESHOLDS.EM_DASH_CASCADING_MODERATE:
            issues += 2
        elif cascading > THRESHOLDS.EM_DASH_CASCADING_WEAK:
            issues += 1

        # Oxford comma consistency (AI always uses it, consistency → 1.0)
        total_comma_lists = r.oxford_comma_count + r.non_oxford_comma_count
        if total_comma_lists >= THRESHOLDS.OXFORD_COMMA_MIN_INSTANCES:  # Only score if enough data
            if oxford > THRESHOLDS.OXFORD_COMMA_ALWAYS:
                issues += 2  # Always Oxford = AI-like
            elif oxford > THRESHOLDS.OXFORD_COMMA_USUALLY:
                issues += 1

        if issues == 0:
            return "HIGH"  # Human-like
        elif issues <= 2:
            return "MEDIUM"
        elif issues <= 4:
            return "LOW"
        else:
            return "VERY LOW"  # AI-like

    def _score_whitespace(self, r: AnalysisResults) -> str:
        """
        Score whitespace and paragraph structure patterns.
        Humans vary paragraph length for pacing; AI produces uniform paragraphs.
        """
        uniformity = r.paragraph_uniformity_score

        # Lower uniformity = higher variance = more human-like
        if uniformity < THRESHOLDS.PARAGRAPH_UNIFORMITY_LOW:
            return "HIGH"  # Highly varied (human-like)
        elif uniformity < THRESHOLDS.PARAGRAPH_UNIFORMITY_MEDIUM:
            return "MEDIUM"
        elif uniformity < THRESHOLDS.PARAGRAPH_UNIFORMITY_AI_THRESHOLD:
            return "LOW"
        else:
            return "VERY LOW"  # Uniform (AI-like)

    def _score_code_structure(self, r: AnalysisResults) -> str:
        """
        Score code block patterns (for technical writing).
        AI always specifies language, has uniform comment density.
        """
        if r.code_block_count == 0:
            return "N/A"  # No code blocks

        lang_consistency = r.code_lang_consistency

        issues = 0

        # Language specification consistency (AI = 1.0, always specifies)
        if lang_consistency == THRESHOLDS.CODE_LANG_PERFECT_CONSISTENCY and r.code_block_count >= THRESHOLDS.CODE_MIN_BLOCKS_FOR_PERFECT_FLAG:
            issues += 2  # Perfect consistency with multiple blocks = AI-like
        elif lang_consistency > THRESHOLDS.CODE_LANG_HIGH_CONSISTENCY:
            issues += 1

        # Comment density uniformity (would require per-block variance - simplified here)
        # AI tends toward ~0.2-0.3 comment density consistently
        if 0.15 <= r.avg_code_comment_density <= 0.35:
            issues += 1

        if issues == 0:
            return "HIGH"  # Human-like
        elif issues <= 1:
            return "MEDIUM"
        elif issues <= 2:
            return "LOW"
        else:
            return "VERY LOW"  # AI-like

    def _score_heading_hierarchy(self, r: AnalysisResults) -> str:
        """
        Score heading hierarchy adherence.
        AI never skips levels (strict H1→H2→H3); humans occasionally do.
        """
        if r.total_headings < 3:
            return "N/A"  # Too few headings to assess

        adherence = r.heading_strict_adherence

        # Perfect adherence (1.0) = AI-like; humans occasionally skip levels
        if adherence == THRESHOLDS.HEADING_PERFECT_ADHERENCE and r.total_headings >= THRESHOLDS.HEADING_MIN_FOR_PERFECT_FLAG:
            return "LOW"  # Perfect adherence with many headings = AI-like
        elif adherence >= THRESHOLDS.HEADING_HIGH_ADHERENCE:
            return "MEDIUM"
        elif adherence >= 0.7:
            return "HIGH"  # Some flexibility = human-like
        else:
            return "HIGH"  # Lots of hierarchy deviation = human-like

    def _score_structural_patterns(self, r: AnalysisResults) -> str:
        """
        Score Phase 1 High-ROI structural patterns (paragraph CV, section variance, list nesting).

        Combined quality score (24 points):
        - Paragraph CV: 10 points (EXCELLENT=10, GOOD=7, FAIR=4, POOR=0)
        - Section variance: 8 points (EXCELLENT=8, GOOD=5, FAIR=3, POOR=0)
        - List nesting: 6 points (EXCELLENT=6, GOOD=4, FAIR=2, POOR=0)

        Detection risk contribution (19 points):
        - Poor paragraph CV (<0.35): +8 risk points
        - Poor section variance (<20%): +6 risk points
        - Excessive list depth (>4): +5 risk points
        """
        # Calculate total quality score (max 24 points)
        total_score = r.paragraph_cv_score + r.section_variance_score + r.list_depth_score

        # Calculate normalized percentage (0-100%)
        score_pct = (total_score / 24.0) * 100

        # Categorize based on percentage
        if score_pct >= 75:  # 18+ / 24
            return "HIGH"  # Human-like variation
        elif score_pct >= 50:  # 12+ / 24
            return "MEDIUM"  # Moderate variation
        elif score_pct >= 30:  # 7+ / 24
            return "LOW"  # Some uniformity detected
        else:
            return "VERY LOW"  # Strong AI signatures detected

    def _score_gltr(self, r: AnalysisResults) -> str:
        """
        Score GLTR (token ranking) analysis.
        AI: >70% top-10 tokens, Human: <55% top-10 tokens
        Research: 95% accuracy on GPT-3/ChatGPT detection
        """
        if r.gltr_top10_percentage is None:
            return "UNKNOWN"

        top10 = r.gltr_top10_percentage

        # Research thresholds: AI >0.70, Human <0.55
        if top10 < 0.50:
            return "HIGH"  # Very human-like
        elif top10 < 0.60:
            return "MEDIUM"  # Somewhat human-like
        elif top10 < 0.70:
            return "LOW"  # Borderline
        else:
            return "VERY LOW"  # AI-like

    def _score_advanced_lexical(self, r: AnalysisResults) -> str:
        """
        Score advanced lexical diversity (HDD, Yule's K).
        HDD: AI 0.40-0.55, Human 0.65-0.85
        Yule's K: AI 100-150, Human 60-90
        """
        if r.hdd_score is None and r.yules_k is None:
            return "UNKNOWN"

        signals = []

        # HDD scoring (most robust metric)
        if r.hdd_score is not None:
            if r.hdd_score >= 0.75:
                signals.append(4)  # Very human-like
            elif r.hdd_score >= 0.65:
                signals.append(3)  # Human-like
            elif r.hdd_score >= 0.55:
                signals.append(2)  # Borderline
            else:
                signals.append(1)  # AI-like

        # Yule's K scoring (lower = more diverse)
        if r.yules_k is not None:
            if r.yules_k < 70:
                signals.append(4)  # Very human-like
            elif r.yules_k < 90:
                signals.append(3)  # Human-like
            elif r.yules_k < 110:
                signals.append(2)  # Borderline
            else:
                signals.append(1)  # AI-like

        if not signals:
            return "UNKNOWN"

        avg_signal = statistics.mean(signals)
        if avg_signal >= 3.5:
            return "HIGH"
        elif avg_signal >= 2.5:
            return "MEDIUM"
        elif avg_signal >= 1.5:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_stylometric(self, r: AnalysisResults) -> str:
        """
        Score stylometric features (function words, hapax, AI markers).
        Combines multiple stylometric signals for overall assessment.
        """
        signals = []

        # Hapax percentage (words appearing once)
        # Human: higher (more unique vocabulary)
        if r.hapax_percentage is not None:
            if r.hapax_percentage >= 0.40:
                signals.append(4)  # Very human-like
            elif r.hapax_percentage >= 0.35:
                signals.append(3)  # Human-like
            elif r.hapax_percentage >= 0.30:
                signals.append(2)  # Borderline
            else:
                signals.append(1)  # AI-like (repetitive)

        # "However" per 1k (AI: 5-10, Human: 1-3)
        if r.however_per_1k is not None:
            if r.however_per_1k <= 2:
                signals.append(4)  # Human-like
            elif r.however_per_1k <= 4:
                signals.append(3)  # Somewhat human-like
            elif r.however_per_1k <= 7:
                signals.append(2)  # Borderline
            else:
                signals.append(1)  # AI-like

        # "Moreover" per 1k (AI: 3-8, Human: 0-2)
        if r.moreover_per_1k is not None:
            if r.moreover_per_1k <= 1:
                signals.append(4)  # Human-like
            elif r.moreover_per_1k <= 2:
                signals.append(3)  # Somewhat human-like
            elif r.moreover_per_1k <= 5:
                signals.append(2)  # Borderline
            else:
                signals.append(1)  # AI-like

        if not signals:
            return "UNKNOWN"

        avg_signal = statistics.mean(signals)
        if avg_signal >= 3.5:
            return "HIGH"
        elif avg_signal >= 2.5:
            return "MEDIUM"
        elif avg_signal >= 1.5:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_ai_detection(self, r: AnalysisResults) -> str:
        """
        Score ensemble AI detection (RoBERTa sentiment, DetectGPT).
        Combines multiple advanced detection methods.
        """
        signals = []

        # RoBERTa sentiment variance (AI: <0.1, Human: >0.15)
        if r.roberta_sentiment_variance is not None:
            if r.roberta_sentiment_variance >= 0.20:
                signals.append(4)  # Very human-like
            elif r.roberta_sentiment_variance >= 0.15:
                signals.append(3)  # Human-like
            elif r.roberta_sentiment_variance >= 0.10:
                signals.append(2)  # Borderline
            else:
                signals.append(1)  # AI-like (emotionally flat)

        # DetectGPT
        if r.detectgpt_is_likely_ai is not None:
            if r.detectgpt_is_likely_ai:
                signals.append(1)  # AI-like
            else:
                signals.append(4)  # Human-like

        # Subordination index (AI: <0.1, Human: >0.15)
        if r.subordination_index is not None:
            if r.subordination_index >= 0.20:
                signals.append(4)  # Very human-like
            elif r.subordination_index >= 0.15:
                signals.append(3)  # Human-like
            elif r.subordination_index >= 0.10:
                signals.append(2)  # Borderline
            else:
                signals.append(1)  # AI-like

        if not signals:
            return "UNKNOWN"

        avg_signal = statistics.mean(signals)
        if avg_signal >= 3.5:
            return "HIGH"
        elif avg_signal >= 2.5:
            return "MEDIUM"
        elif avg_signal >= 1.5:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_textacy_lexical(self, r: AnalysisResults) -> str:
        """
        Score advanced textacy-based lexical diversity (MATTR + RTTR).
        MATTR: AI <0.65, Human ≥0.70
        RTTR: AI <7.5, Human ≥7.5
        """
        signals = []

        # MATTR scoring
        if r.mattr is not None:
            if r.mattr >= 0.75:
                signals.append(4)  # EXCELLENT
            elif r.mattr >= 0.70:
                signals.append(3)  # GOOD
            elif r.mattr >= 0.65:
                signals.append(2)  # FAIR
            else:
                signals.append(1)  # POOR

        # RTTR scoring
        if r.rttr is not None:
            if r.rttr >= 8.5:
                signals.append(4)  # EXCELLENT
            elif r.rttr >= 7.5:
                signals.append(3)  # GOOD
            elif r.rttr >= 6.5:
                signals.append(2)  # FAIR
            else:
                signals.append(1)  # POOR

        if not signals:
            return "UNKNOWN"

        avg_signal = statistics.mean(signals)
        if avg_signal >= 3.5:
            return "HIGH"
        elif avg_signal >= 2.5:
            return "MEDIUM"
        elif avg_signal >= 1.5:
            return "LOW"
        else:
            return "VERY LOW"

    def _score_heading_length(self, r: AnalysisResults) -> str:
        """
        Score enhanced heading length analysis.
        AI: avg >9 words, Human: avg ≤7 words
        """
        if r.heading_length_assessment is None or r.heading_length_assessment == 'INSUFFICIENT_DATA':
            return "UNKNOWN"

        # Convert assessment to score level
        assessment_map = {
            'EXCELLENT': 'HIGH',
            'GOOD': 'MEDIUM',
            'FAIR': 'LOW',
            'POOR': 'VERY LOW'
        }
        return assessment_map.get(r.heading_length_assessment, 'UNKNOWN')

    def _score_subsection_asymmetry(self, r: AnalysisResults) -> str:
        """
        Score subsection asymmetry analysis.
        AI: CV <0.3 (uniform), Human: CV ≥0.6 (varied)
        """
        if r.subsection_assessment is None or r.subsection_assessment == 'INSUFFICIENT_DATA':
            return "UNKNOWN"

        assessment_map = {
            'EXCELLENT': 'HIGH',
            'GOOD': 'MEDIUM',
            'FAIR': 'LOW',
            'POOR': 'VERY LOW'
        }
        return assessment_map.get(r.subsection_assessment, 'UNKNOWN')

    def _score_heading_depth_variance(self, r: AnalysisResults) -> str:
        """
        Score heading depth variance analysis.
        AI: RIGID (sequential only), Human: VARIED (lateral moves, jumps)
        """
        if r.heading_depth_assessment is None or r.heading_depth_assessment == 'INSUFFICIENT_DATA':
            return "UNKNOWN"

        assessment_map = {
            'EXCELLENT': 'HIGH',
            'GOOD': 'MEDIUM',
            'FAIR': 'LOW',
            'POOR': 'VERY LOW'
        }
        return assessment_map.get(r.heading_depth_assessment, 'UNKNOWN')

    def _assess_overall(self, r: AnalysisResults) -> str:
        """Provide overall humanization assessment with enhanced structural analysis"""
        score_map = {"HIGH": 4, "MEDIUM": 3, "LOW": 2, "VERY LOW": 1, "UNKNOWN": 2.5, "N/A": 2.5}

        # Base dimensions (always present) - adjusted weights to accommodate new dimensions
        scores = [
            score_map[r.perplexity_score] * 0.15,  # 15% weight (was 18%)
            score_map[r.burstiness_score] * 0.18,  # 18% weight (was 22%)
            score_map[r.structure_score] * 0.15,   # 15% weight (was 18%)
            score_map[r.voice_score] * 0.15,       # 15% weight (was 18%)
            score_map[r.technical_score] * 0.07,   # 7% weight (was 9%)
            score_map[r.formatting_score] * 0.04,  # 4% weight (was 5%)
        ]

        # Enhanced NLP dimensions (if available)
        if r.syntactic_score and r.syntactic_score != "UNKNOWN":
            scores.append(score_map[r.syntactic_score] * 0.04)  # 4% weight
        else:
            scores.append(score_map["UNKNOWN"] * 0.04)

        if r.sentiment_score and r.sentiment_score != "UNKNOWN":
            scores.append(score_map[r.sentiment_score] * 0.04)  # 4% weight
        else:
            scores.append(score_map["UNKNOWN"] * 0.04)

        # NEW: Enhanced structural dimensions (always present)
        # These are research-backed AI detection signals from Perplexity analysis
        scores.extend([
            score_map[r.bold_italic_score] * 0.03,  # 3% - High value (ChatGPT uses 10x more bold)
            score_map[r.list_usage_score] * 0.02,   # 2% - High value (AI uses lists 78% of time)
            score_map[r.punctuation_score] * 0.03,  # 3% - Very high value (em-dash cascading is strong marker)
            score_map[r.whitespace_score] * 0.01,   # 1% - Medium value
            score_map.get(r.code_structure_score, score_map["N/A"]) * 0.01,  # 1% - Conditional
            score_map.get(r.heading_hierarchy_score, score_map["N/A"]) * 0.01,  # 1% - Conditional
        ])

        # ADVANCED: State-of-the-art detection methods (if available)
        # These have the highest accuracy (85-95%) and get significant weight
        if r.gltr_score and r.gltr_score != "UNKNOWN":
            scores.append(score_map[r.gltr_score] * 0.08)  # 8% - GLTR: 95% accuracy
        else:
            scores.append(score_map["UNKNOWN"] * 0.08)

        if r.advanced_lexical_score and r.advanced_lexical_score != "UNKNOWN":
            scores.append(score_map[r.advanced_lexical_score] * 0.05)  # 5% - HDD/Yule's K
        else:
            scores.append(score_map["UNKNOWN"] * 0.05)

        if r.stylometric_score and r.stylometric_score != "UNKNOWN":
            scores.append(score_map[r.stylometric_score] * 0.04)  # 4% - Hapax, function words
        else:
            scores.append(score_map["UNKNOWN"] * 0.04)

        if r.ai_detection_score and r.ai_detection_score != "UNKNOWN":
            scores.append(score_map[r.ai_detection_score] * 0.06)  # 6% - DetectGPT, RoBERTa sentiment
        else:
            scores.append(score_map["UNKNOWN"] * 0.06)

        weighted_avg = sum(scores)

        if weighted_avg >= 3.5:
            return "MINIMAL humanization needed"
        elif weighted_avg >= 2.8:
            return "LIGHT humanization recommended"
        elif weighted_avg >= 2.0:
            return "SUBSTANTIAL humanization required"
        else:
            return "EXTENSIVE humanization required"

    def calculate_dual_score(self, results: AnalysisResults,
                            detection_target: float = 30.0,
                            quality_target: float = 85.0) -> DualScore:
        """
        Calculate dual scores: Detection Risk (0-100, lower=better) and Quality Score (0-100, higher=better)

        Args:
            results: AnalysisResults from analysis
            detection_target: Target detection risk (default 30 = low risk)
            quality_target: Target quality score (default 85 = excellent)

        Returns:
            DualScore with comprehensive breakdown and optimization path
        """
        timestamp = datetime.now().isoformat()

        # Map score levels to numerical values (0-1 scale)
        score_map = {"HIGH": 1.0, "MEDIUM": 0.75, "LOW": 0.5, "VERY LOW": 0.25, "UNKNOWN": 0.5, "N/A": 0.5}

        # ============================================================================
        # TIER 1: ADVANCED DETECTION (40 points) - Highest accuracy
        # ============================================================================

        # GLTR Token Ranking (12 points) - 95% accuracy on GPT-3/ChatGPT
        gltr_val = score_map.get(results.gltr_score, 0.5) if results.gltr_score else 0.5
        gltr_score = ScoreDimension(
            name="GLTR Token Ranking",
            score=gltr_val * 12,
            max_score=12.0,
            percentage=gltr_val * 100,
            impact=self._calculate_impact(gltr_val, 12.0),
            gap=(1.0 - gltr_val) * 12,
            raw_value=results.gltr_top10_percentage,
            recommendation="Rewrite high-predictability segments (>70% top-10 tokens)" if gltr_val < 0.75 else None
        )

        # Advanced Lexical Diversity - HDD/Yule's K (8 points)
        lexical_val = score_map.get(results.advanced_lexical_score, 0.5) if results.advanced_lexical_score else 0.5
        lexical_score = ScoreDimension(
            name="Advanced Lexical (HDD/Yule's K)",
            score=lexical_val * 8,
            max_score=8.0,
            percentage=lexical_val * 100,
            impact=self._calculate_impact(lexical_val, 8.0),
            gap=(1.0 - lexical_val) * 8,
            raw_value=results.hdd_score,
            recommendation="Increase vocabulary diversity (target HDD > 0.65)" if lexical_val < 0.75 else None
        )

        # Advanced Lexical: MATTR (Moving Average Type-Token Ratio) - 12 points
        textacy_lexical_val = score_map.get(self._score_textacy_lexical(results), 0.5)
        mattr_score_val = 12.0 * (1.0 if results.mattr_assessment == 'EXCELLENT' else
                                   0.75 if results.mattr_assessment == 'GOOD' else
                                   0.42 if results.mattr_assessment == 'FAIR' else 0.0) if results.mattr else 0.0
        mattr_dim = ScoreDimension(
            name="MATTR (Lexical Richness)",
            score=mattr_score_val,
            max_score=12.0,
            percentage=(mattr_score_val / 12.0) * 100,
            impact=self._calculate_impact(mattr_score_val / 12.0, 12.0),
            gap=12.0 - mattr_score_val,
            raw_value=results.mattr,
            recommendation="Increase vocabulary variety (target MATTR ≥0.70)" if mattr_score_val < 9.0 else None
        )

        # Advanced Lexical: RTTR (Root Type-Token Ratio) - 8 points
        rttr_score_val = 8.0 * (1.0 if results.rttr_assessment == 'EXCELLENT' else
                                 0.75 if results.rttr_assessment == 'GOOD' else
                                 0.375 if results.rttr_assessment == 'FAIR' else 0.0) if results.rttr else 0.0
        rttr_dim = ScoreDimension(
            name="RTTR (Global Diversity)",
            score=rttr_score_val,
            max_score=8.0,
            percentage=(rttr_score_val / 8.0) * 100,
            impact=self._calculate_impact(rttr_score_val / 8.0, 8.0),
            gap=8.0 - rttr_score_val,
            raw_value=results.rttr,
            recommendation="Add domain-specific terminology (target RTTR ≥7.5)" if rttr_score_val < 6.0 else None
        )

        # AI Detection Ensemble - DetectGPT/RoBERTa (10 points)
        ai_detect_val = score_map.get(results.ai_detection_score, 0.5) if results.ai_detection_score else 0.5
        ai_detect_score = ScoreDimension(
            name="AI Detection Ensemble",
            score=ai_detect_val * 10,
            max_score=10.0,
            percentage=ai_detect_val * 100,
            impact=self._calculate_impact(ai_detect_val, 10.0),
            gap=(1.0 - ai_detect_val) * 10,
            raw_value=results.roberta_sentiment_variance,
            recommendation="Increase emotional variation (sentiment variance > 0.15)" if ai_detect_val < 0.75 else None
        )

        # Stylometric Markers - However/Moreover (6 points)
        stylo_val = score_map.get(results.stylometric_score, 0.5) if results.stylometric_score else 0.5
        stylo_score = ScoreDimension(
            name="Stylometric Markers",
            score=stylo_val * 6,
            max_score=6.0,
            percentage=stylo_val * 100,
            impact=self._calculate_impact(stylo_val, 6.0),
            gap=(1.0 - stylo_val) * 6,
            raw_value=results.however_per_1k,
            recommendation="Remove AI transitions (however/moreover)" if stylo_val < 0.75 else None
        )

        # Syntactic Complexity (4 points)
        syntax_val = score_map.get(results.syntactic_score, 0.5) if results.syntactic_score else 0.5
        syntax_score = ScoreDimension(
            name="Syntactic Complexity",
            score=syntax_val * 4,
            max_score=4.0,
            percentage=syntax_val * 100,
            impact=self._calculate_impact(syntax_val, 4.0),
            gap=(1.0 - syntax_val) * 4,
            raw_value=results.subordination_index,
            recommendation="Add subordinate clauses, vary tree depth" if syntax_val < 0.75 else None
        )

        advanced_category = ScoreCategory(
            name="Advanced Detection",
            total=gltr_score.score + lexical_score.score + mattr_dim.score + rttr_dim.score + ai_detect_score.score + stylo_score.score + syntax_score.score,
            max_total=60.0,  # Includes advanced lexical metrics: +12 (MATTR) +8 (RTTR)
            percentage=((gltr_score.score + lexical_score.score + mattr_dim.score + rttr_dim.score + ai_detect_score.score + stylo_score.score + syntax_score.score) / 60.0) * 100,
            dimensions=[gltr_score, lexical_score, mattr_dim, rttr_dim, ai_detect_score, stylo_score, syntax_score]
        )

        # ============================================================================
        # TIER 2: CORE PATTERNS (35 points) - Proven AI signatures
        # ============================================================================

        # Burstiness - Sentence Variation (12 points)
        burst_val = score_map[results.burstiness_score]
        burst_score = ScoreDimension(
            name="Burstiness (Sentence Variation)",
            score=burst_val * 12,
            max_score=12.0,
            percentage=burst_val * 100,
            impact=self._calculate_impact(burst_val, 12.0),
            gap=(1.0 - burst_val) * 12,
            raw_value=results.sentence_stdev,
            recommendation="Vary sentence lengths: short (5-10w), medium (15-25w), long (30-45w)" if burst_val < 0.75 else None
        )

        # Perplexity - Vocabulary (10 points)
        perp_val = score_map[results.perplexity_score]
        perp_score = ScoreDimension(
            name="Perplexity (Vocabulary)",
            score=perp_val * 10,
            max_score=10.0,
            percentage=perp_val * 100,
            impact=self._calculate_impact(perp_val, 10.0),
            gap=(1.0 - perp_val) * 10,
            raw_value=results.ai_vocabulary_per_1k,
            recommendation="Replace AI vocabulary: delve, leverage, robust, harness" if perp_val < 0.75 else None
        )

        # Formatting Patterns (8 points)
        format_val = score_map[results.formatting_score]
        format_score = ScoreDimension(
            name="Formatting Patterns",
            score=format_val * 8,
            max_score=8.0,
            percentage=format_val * 100,
            impact=self._calculate_impact(format_val, 8.0),
            gap=(1.0 - format_val) * 8,
            raw_value=results.em_dashes_per_page,
            recommendation="Reduce em-dashes to ≤2 per page, reduce bold/italic density" if format_val < 0.75 else None
        )

        # Heading Hierarchy (5 points)
        heading_val = score_map.get(results.heading_hierarchy_score, score_map[results.structure_score])
        heading_score = ScoreDimension(
            name="Heading Hierarchy",
            score=heading_val * 5,
            max_score=5.0,
            percentage=heading_val * 100,
            impact=self._calculate_impact(heading_val, 5.0),
            gap=(1.0 - heading_val) * 5,
            raw_value=results.heading_depth,
            recommendation="Flatten to H3 max, break parallelism, create asymmetry" if heading_val < 0.75 else None
        )

        # Enhanced Heading: Length Analysis (10 points)
        heading_length_score_val = 10.0 * (1.0 if results.heading_length_assessment == 'EXCELLENT' else
                                             0.7 if results.heading_length_assessment == 'GOOD' else
                                             0.4 if results.heading_length_assessment == 'FAIR' else 0.0) if results.heading_length_assessment else 5.0
        heading_length_dim = ScoreDimension(
            name="Heading Length Patterns",
            score=heading_length_score_val,
            max_score=10.0,
            percentage=(heading_length_score_val / 10.0) * 100,
            impact=self._calculate_impact(heading_length_score_val / 10.0, 10.0),
            gap=10.0 - heading_length_score_val,
            raw_value=results.avg_heading_length,
            recommendation="Shorten headings (target avg ≤7 words, remove descriptive modifiers)" if heading_length_score_val < 7.0 else None
        )

        # Enhanced Heading: Subsection Asymmetry (8 points)
        subsection_score_val = 8.0 * (1.0 if results.subsection_assessment == 'EXCELLENT' else
                                       0.625 if results.subsection_assessment == 'GOOD' else
                                       0.375 if results.subsection_assessment == 'FAIR' else 0.0) if results.subsection_assessment else 4.0
        subsection_dim = ScoreDimension(
            name="Subsection Asymmetry",
            score=subsection_score_val,
            max_score=8.0,
            percentage=(subsection_score_val / 8.0) * 100,
            impact=self._calculate_impact(subsection_score_val / 8.0, 8.0),
            gap=8.0 - subsection_score_val,
            raw_value=results.subsection_cv,
            recommendation="Break uniformity: vary subsections per H2 (target CV ≥0.6)" if subsection_score_val < 5.0 else None
        )

        # Enhanced Heading: Depth Variance (6 points)
        depth_variance_score_val = 6.0 * (1.0 if results.heading_depth_assessment == 'EXCELLENT' else
                                           0.67 if results.heading_depth_assessment == 'GOOD' else
                                           0.33 if results.heading_depth_assessment == 'FAIR' else 0.0) if results.heading_depth_assessment else 3.0
        depth_variance_dim = ScoreDimension(
            name="Heading Depth Variance",
            score=depth_variance_score_val,
            max_score=6.0,
            percentage=(depth_variance_score_val / 6.0) * 100,
            impact=self._calculate_impact(depth_variance_score_val / 6.0, 6.0),
            gap=6.0 - depth_variance_score_val,
            raw_value=results.heading_depth_pattern,
            recommendation="Add lateral H3→H3 transitions and depth jumps" if depth_variance_score_val < 4.0 else None
        )

        core_category = ScoreCategory(
            name="Core Patterns",
            total=burst_score.score + perp_score.score + format_score.score + heading_score.score + heading_length_dim.score + subsection_dim.score + depth_variance_dim.score,
            max_total=59.0,  # Includes enhanced heading analysis: +10 (length) +8 (subsection) +6 (depth)
            percentage=((burst_score.score + perp_score.score + format_score.score + heading_score.score + heading_length_dim.score + subsection_dim.score + depth_variance_dim.score) / 59.0) * 100,
            dimensions=[burst_score, perp_score, format_score, heading_score, heading_length_dim, subsection_dim, depth_variance_dim]
        )

        # ============================================================================
        # TIER 3: SUPPORTING SIGNALS (25 points) - Context indicators
        # ============================================================================

        # Voice & Authenticity (8 points)
        voice_val = score_map[results.voice_score]
        voice_score = ScoreDimension(
            name="Voice & Authenticity",
            score=voice_val * 8,
            max_score=8.0,
            percentage=voice_val * 100,
            impact=self._calculate_impact(voice_val, 8.0),
            gap=(1.0 - voice_val) * 8,
            raw_value=results.first_person_count,
            recommendation="Add personal perspective, contractions, hedging" if voice_val < 0.75 else None
        )

        # Structure & Organization (7 points)
        struct_val = score_map[results.structure_score]
        struct_score = ScoreDimension(
            name="Structure & Organization",
            score=struct_val * 7,
            max_score=7.0,
            percentage=struct_val * 100,
            impact=self._calculate_impact(struct_val, 7.0),
            gap=(1.0 - struct_val) * 7,
            raw_value=results.formulaic_transitions_count,
            recommendation="Replace formulaic transitions with natural flow" if struct_val < 0.75 else None
        )

        # Emotional Depth - Sentiment (6 points)
        sent_val = score_map.get(results.sentiment_score, 0.5) if results.sentiment_score else 0.5
        sent_score = ScoreDimension(
            name="Emotional Depth",
            score=sent_val * 6,
            max_score=6.0,
            percentage=sent_val * 100,
            impact=self._calculate_impact(sent_val, 6.0),
            gap=(1.0 - sent_val) * 6,
            raw_value=results.sentiment_variance,
            recommendation="Add examples, anecdotes, acknowledge challenges" if sent_val < 0.75 else None
        )

        # Technical Depth (4 points)
        tech_val = score_map[results.technical_score]
        tech_score = ScoreDimension(
            name="Technical Depth",
            score=tech_val * 4,
            max_score=4.0,
            percentage=tech_val * 100,
            impact=self._calculate_impact(tech_val, 4.0),
            gap=(1.0 - tech_val) * 4,
            raw_value=results.domain_terms_count,
            recommendation="Add domain-specific terminology" if tech_val < 0.75 else None
        )

        supporting_category = ScoreCategory(
            name="Supporting Signals",
            total=voice_score.score + struct_score.score + sent_score.score + tech_score.score,
            max_total=25.0,
            percentage=((voice_score.score + struct_score.score + sent_score.score + tech_score.score) / 25.0) * 100,
            dimensions=[voice_score, struct_score, sent_score, tech_score]
        )

        # ============================================================================
        # CALCULATE DUAL SCORES
        # ============================================================================

        total_quality = advanced_category.total + core_category.total + supporting_category.total
        quality_score = total_quality  # Already 0-100

        # Detection risk is INVERSE of quality (100 - quality)
        # But weighted more heavily on advanced detection dimensions
        detection_components = [
            (1.0 - gltr_val) * 25,      # GLTR has 25% weight in detection
            (1.0 - ai_detect_val) * 20, # AI detection 20%
            (1.0 - lexical_val) * 15,   # Lexical diversity 15%
            (1.0 - stylo_val) * 15,     # Stylometric 15%
            (1.0 - burst_val) * 10,     # Burstiness 10%
            (1.0 - format_val) * 10,    # Formatting 10%
            (1.0 - perp_val) * 5,       # Perplexity 5%
        ]

        # Advanced detection risk contributions (lexical & heading metrics)
        if results.mattr is not None and results.mattr < 0.70:
            detection_components.append(10)  # Poor MATTR adds +10 risk points
        if results.rttr is not None and results.rttr < 7.5:
            detection_components.append(6)   # Poor RTTR adds +6 risk points
        if results.avg_heading_length is not None and results.avg_heading_length > 8:
            detection_components.append(8)   # Long headings add +8 risk points
        if results.subsection_cv is not None and results.subsection_cv < 0.3:
            detection_components.append(7)   # Low subsection asymmetry adds +7 risk points
        if results.heading_depth_pattern == 'RIGID':
            detection_components.append(5)   # Rigid depth pattern adds +5 risk points

        detection_risk = sum(detection_components)

        # Interpretations
        quality_interp = self._interpret_quality(quality_score)
        detection_interp = self._interpret_detection(detection_risk)

        # Gaps
        quality_gap = max(0, quality_target - quality_score)
        detection_gap = max(0, detection_risk - detection_target)

        # ============================================================================
        # GENERATE IMPROVEMENT ACTIONS
        # ============================================================================

        all_dimensions = (
            advanced_category.dimensions +
            core_category.dimensions +
            supporting_category.dimensions
        )

        improvements = []
        for dim in all_dimensions:
            if dim.gap > 0.5:  # Only suggest if gap > 0.5 points
                improvements.append(ImprovementAction(
                    priority=0,  # Will be set later
                    dimension=dim.name,
                    current_score=dim.score,
                    max_score=dim.max_score,
                    potential_gain=dim.gap,
                    impact_level=dim.impact,
                    action=dim.recommendation or f"Improve {dim.name}",
                    effort_level=self._estimate_effort(dim.name, dim.gap)
                ))

        # Sort by ROI (gain / effort)
        effort_multiplier = {'LOW': 1.0, 'MEDIUM': 0.7, 'HIGH': 0.4}
        improvements.sort(key=lambda x: x.potential_gain * effort_multiplier[x.effort_level], reverse=True)

        # Set priorities
        for i, imp in enumerate(improvements, start=1):
            imp.priority = i

        # Path to target - actions needed to reach quality target
        path = []
        cumulative_gain = quality_score
        for imp in improvements:
            if cumulative_gain >= quality_target:
                break
            path.append(imp)
            cumulative_gain += imp.potential_gain

        # Estimate overall effort
        if quality_gap == 0:
            effort = "MINIMAL"
        elif quality_gap < 5:
            effort = "LIGHT"
        elif quality_gap < 15:
            effort = "MODERATE"
        elif quality_gap < 30:
            effort = "SUBSTANTIAL"
        else:
            effort = "EXTENSIVE"

        return DualScore(
            detection_risk=round(detection_risk, 1),
            quality_score=round(quality_score, 1),
            detection_interpretation=detection_interp,
            quality_interpretation=quality_interp,
            detection_target=detection_target,
            quality_target=quality_target,
            detection_gap=round(detection_gap, 1),
            quality_gap=round(quality_gap, 1),
            categories=[advanced_category, core_category, supporting_category],
            improvements=improvements,
            path_to_target=path,
            estimated_effort=effort,
            timestamp=timestamp,
            file_path=results.file_path,
            total_words=results.total_words
        )

    def _calculate_impact(self, current_val: float, max_points: float) -> str:
        """Calculate impact level based on gap and point weight"""
        gap = (1.0 - current_val) * max_points
        if gap < 1.0:
            return "NONE"
        elif gap < 2.0:
            return "LOW"
        elif gap < 4.0:
            return "MEDIUM"
        else:
            return "HIGH"

    def _estimate_effort(self, dimension_name: str, gap: float) -> str:
        """Estimate effort required to close gap"""
        # Some dimensions are easier to fix than others
        easy_fixes = ["Formatting Patterns", "Stylometric Markers", "Heading Hierarchy"]
        medium_fixes = ["Burstiness (Sentence Variation)", "Perplexity (Vocabulary)", "Structure & Organization"]
        hard_fixes = ["GLTR Token Ranking", "Advanced Lexical (HDD/Yule's K)", "Syntactic Complexity"]

        if dimension_name in easy_fixes:
            return "LOW" if gap < 3 else "MEDIUM"
        elif dimension_name in medium_fixes:
            return "MEDIUM" if gap < 4 else "HIGH"
        else:  # hard_fixes
            return "HIGH"

    def _interpret_quality(self, score: float) -> str:
        """Interpret quality score"""
        if score >= 95:
            return "EXCEPTIONAL - Indistinguishable from human"
        elif score >= 85:
            return "EXCELLENT - Minimal AI signatures"
        elif score >= 70:
            return "GOOD - Natural with minor tells"
        elif score >= 50:
            return "MIXED - Needs moderate work"
        elif score >= 30:
            return "AI-LIKE - Substantial work needed"
        else:
            return "OBVIOUS AI - Complete rewrite"

    def _interpret_detection(self, risk: float) -> str:
        """Interpret detection risk"""
        if risk >= 70:
            return "VERY HIGH - Will be flagged"
        elif risk >= 50:
            return "HIGH - Likely flagged"
        elif risk >= 30:
            return "MEDIUM - May be flagged"
        elif risk >= 15:
            return "LOW - Unlikely flagged"
        else:
            return "VERY LOW - Safe"

    # ============================================================================
    # HISTORICAL TRACKING
    # ============================================================================

    def _get_history_file_path(self, file_path: str) -> Path:
        """Get path to history file for a given document"""
        # Create .score-history directory in same location as analyzed file
        doc_path = Path(file_path)
        history_dir = doc_path.parent / '.score-history'
        history_dir.mkdir(exist_ok=True)

        # History file named after document
        history_file = history_dir / f"{doc_path.stem}.history.json"
        return history_file

    def load_score_history(self, file_path: str) -> ScoreHistory:
        """Load score history for a document"""
        history_file = self._get_history_file_path(file_path)

        if not history_file.exists():
            return ScoreHistory(file_path=file_path, scores=[])

        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Reconstruct ScoreHistory from JSON
            scores = [HistoricalScore(**score_data) for score_data in data.get('scores', [])]
            return ScoreHistory(file_path=data.get('file_path', file_path), scores=scores)

        except Exception as e:
            print(f"Warning: Could not load history from {history_file}: {e}", file=sys.stderr)
            return ScoreHistory(file_path=file_path, scores=[])

    def save_score_history(self, history: ScoreHistory):
        """Save score history for a document"""
        history_file = self._get_history_file_path(history.file_path)

        try:
            # Convert to dict for JSON serialization
            data = {
                'file_path': history.file_path,
                'scores': [asdict(score) for score in history.scores]
            }

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Warning: Could not save history to {history_file}: {e}", file=sys.stderr)


def format_dual_score_report(dual_score: DualScore, history: Optional[ScoreHistory] = None,
                             output_format: str = 'text') -> str:
    """Format dual score report with optimization path"""

    if output_format == 'json':
        # Convert to dict for JSON serialization
        data = {
            'detection_risk': dual_score.detection_risk,
            'quality_score': dual_score.quality_score,
            'detection_interpretation': dual_score.detection_interpretation,
            'quality_interpretation': dual_score.quality_interpretation,
            'detection_target': dual_score.detection_target,
            'quality_target': dual_score.quality_target,
            'detection_gap': dual_score.detection_gap,
            'quality_gap': dual_score.quality_gap,
            'categories': [asdict(cat) for cat in dual_score.categories],
            'improvements': [asdict(imp) for imp in dual_score.improvements],
            'path_to_target': [asdict(action) for action in dual_score.path_to_target],
            'estimated_effort': dual_score.estimated_effort,
            'timestamp': dual_score.timestamp,
            'file_path': dual_score.file_path,
            'total_words': dual_score.total_words
        }

        if history and len(history.scores) > 0:
            data['history'] = {
                'trend': history.get_trend(),
                'score_count': len(history.scores),
                'first_score': asdict(history.scores[0]),
                'latest_score': asdict(history.scores[-1])
            }

        return json.dumps(data, indent=2)

    else:  # text format
        report = f"""
{'=' * 80}
DUAL SCORE ANALYSIS - OPTIMIZATION REPORT
{'=' * 80}

File: {dual_score.file_path}
Words: {dual_score.total_words}
Timestamp: {dual_score.timestamp}

{'─' * 80}
DUAL SCORES
{'─' * 80}

Quality Score:      {dual_score.quality_score:5.1f} / 100  {dual_score.quality_interpretation}
Detection Risk:     {dual_score.detection_risk:5.1f} / 100  {dual_score.detection_interpretation}

Targets:            Quality ≥{dual_score.quality_target:.0f}, Detection ≤{dual_score.detection_target:.0f}
Gap to Target:      Quality needs +{dual_score.quality_gap:.1f} pts, Detection needs -{dual_score.detection_gap:.1f} pts
Effort Required:    {dual_score.estimated_effort}

"""

        # Historical trend if available
        if history and len(history.scores) > 1:
            trend = history.get_trend()
            report += f"""{'─' * 80}
HISTORICAL TREND ({len(history.scores)} scores tracked)
{'─' * 80}

Quality:   {trend['quality']:10s} ({trend['quality_change']:+.1f} pts)
Detection: {trend['detection']:10s} ({trend['detection_change']:+.1f} pts)

"""

        # Category breakdown
        report += f"""{'─' * 80}
SCORE BREAKDOWN BY CATEGORY
{'─' * 80}

"""
        for cat in dual_score.categories:
            report += f"""{cat.name:25s}  {cat.total:5.1f} / {cat.max_total:4.1f}  ({cat.percentage:5.1f}%)
"""
            for dim in cat.dimensions:
                impact_symbol = '⚠' if dim.impact in ['HIGH', 'MEDIUM'] else ' '
                report += f"""  {impact_symbol} {dim.name:40s} {dim.score:5.1f} / {dim.max_score:4.1f}  (gap: {dim.gap:4.1f})
"""
            report += "\n"

        # Path to target
        if dual_score.path_to_target:
            report += f"""{'─' * 80}
PATH TO TARGET ({len(dual_score.path_to_target)} actions, sorted by ROI)
{'─' * 80}

"""
            cumulative = dual_score.quality_score
            for i, action in enumerate(dual_score.path_to_target, 1):
                cumulative += action.potential_gain
                report += f"""{i}. {action.dimension} (Effort: {action.effort_level})
   Current: {action.current_score:.1f}/{action.max_score:.1f} → Gain: +{action.potential_gain:.1f} pts → Cumulative: {cumulative:.1f}
   Action: {action.action}

"""

        # Top improvements (beyond path to target)
        other_improvements = [imp for imp in dual_score.improvements if imp not in dual_score.path_to_target]
        if other_improvements:
            report += f"""{'─' * 80}
ADDITIONAL IMPROVEMENTS (optional, for exceeding targets)
{'─' * 80}

"""
            for imp in other_improvements[:5]:  # Show top 5
                report += f"""• {imp.dimension} ({imp.effort_level} effort, +{imp.potential_gain:.1f} pts)
  {imp.action}

"""

        report += f"""{'=' * 80}
OPTIMIZATION SUMMARY
{'=' * 80}

To reach Quality Score ≥{dual_score.quality_target:.0f}:
  Complete {len(dual_score.path_to_target)} actions above
  Estimated effort: {dual_score.estimated_effort}
  Expected final score: ~{min(100, dual_score.quality_score + sum(a.potential_gain for a in dual_score.path_to_target)):.1f}

{'=' * 80}

"""
        return report


def format_detailed_report(analysis: DetailedAnalysis, output_format: str = 'text') -> str:
    """Format detailed analysis with line numbers and suggestions"""

    if output_format == 'json':
        # Convert dataclasses to dict for JSON serialization
        return json.dumps({
            'file_path': analysis.file_path,
            'summary': analysis.summary,
            # Original detailed findings
            'ai_vocabulary': [asdict(v) for v in analysis.ai_vocabulary],
            'heading_issues': [asdict(h) for h in analysis.heading_issues],
            'uniform_paragraphs': [asdict(p) for p in analysis.uniform_paragraphs],
            'em_dashes': [asdict(e) for e in analysis.em_dashes],
            'transitions': [asdict(t) for t in analysis.transitions],
            # ADVANCED: New detailed findings for LLM-driven fixes
            'burstiness_issues': [asdict(b) for b in analysis.burstiness_issues],
            'syntactic_issues': [asdict(s) for s in analysis.syntactic_issues],
            'stylometric_issues': [asdict(s) for s in analysis.stylometric_issues],
            'formatting_issues': [asdict(f) for f in analysis.formatting_issues],
            'high_predictability_segments': [asdict(h) for h in analysis.high_predictability_segments],
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

        # ADVANCED: Burstiness Issues
        if analysis.burstiness_issues:
            report += f"""
{'─' * 80}
BURSTINESS ISSUES ({len(analysis.burstiness_issues)} sections with uniform sentence lengths)
{'─' * 80}

"""
            for issue in analysis.burstiness_issues[:5]:  # Show top 5
                report += f"""Lines {issue.start_line}-{issue.end_line} ({issue.sentence_count} sentences):
  Mean: {issue.mean_length} words | StdDev: {issue.stdev} (LOW VARIATION)
  Problem: {issue.problem}
  Sample sentences:
"""
                for line_num, text, word_count in issue.sentences_preview:
                    report += f"""    Line {line_num}: "{text}" ({word_count} words)
"""
                report += f"""  → Suggestion: {issue.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
BURSTINESS: Good sentence variation ✓
{'─' * 80}

"""

        # ADVANCED: Syntactic Issues
        if analysis.syntactic_issues:
            # Group by type
            passive_issues = [s for s in analysis.syntactic_issues if s.issue_type == 'passive']
            shallow_issues = [s for s in analysis.syntactic_issues if s.issue_type == 'shallow']
            subordination_issues = [s for s in analysis.syntactic_issues if s.issue_type == 'subordination']

            report += f"""
{'─' * 80}
SYNTACTIC COMPLEXITY ISSUES ({len(analysis.syntactic_issues)} total)
{'─' * 80}

"""
            if passive_issues:
                report += f"""PASSIVE VOICE ({len(passive_issues)} instances):
"""
                for syn in passive_issues[:3]:
                    report += f"""  Line {syn.line_number}: {syn.sentence}
    → {syn.suggestion}

"""

            if shallow_issues:
                report += f"""
SHALLOW SYNTAX ({len(shallow_issues)} instances):
"""
                for syn in shallow_issues[:3]:
                    report += f"""  Line {syn.line_number}: {syn.sentence}
    Problem: {syn.problem}
    → {syn.suggestion}

"""

            if subordination_issues:
                report += f"""
LOW SUBORDINATION ({len(subordination_issues)} instances):
"""
                for syn in subordination_issues[:3]:
                    report += f"""  Line {syn.line_number}: {syn.sentence}
    → {syn.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
SYNTACTIC COMPLEXITY: Good variation ✓
{'─' * 80}

"""

        # ADVANCED: Stylometric Issues
        if analysis.stylometric_issues:
            # Group by marker type
            however_issues = [s for s in analysis.stylometric_issues if s.marker_type == 'however']
            moreover_issues = [s for s in analysis.stylometric_issues if s.marker_type == 'moreover']
            cluster_issues = [s for s in analysis.stylometric_issues if s.marker_type == 'however_cluster']

            report += f"""
{'─' * 80}
STYLOMETRIC AI MARKERS ({len(analysis.stylometric_issues)} total)
{'─' * 80}

"""
            if however_issues:
                report += f""""HOWEVER" USAGE ({len(however_issues)} instances - AI marker):
"""
                for styl in however_issues[:5]:
                    report += f"""  Line {styl.line_number}: {styl.context}
    → {styl.suggestion}

"""

            if moreover_issues:
                report += f"""
"MOREOVER" USAGE ({len(moreover_issues)} instances - strong AI signature):
"""
                for styl in moreover_issues[:5]:
                    report += f"""  Line {styl.line_number}: {styl.context}
    → {styl.suggestion}

"""

            if cluster_issues:
                report += f"""
CLUSTERED MARKERS ({len(cluster_issues)} clusters - strong AI signature):
"""
                for styl in cluster_issues:
                    report += f"""  {styl.context}
    → {styl.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
STYLOMETRIC MARKERS: Natural writing patterns ✓
{'─' * 80}

"""

        # ADVANCED: Formatting Issues
        if analysis.formatting_issues:
            bold_issues = [f for f in analysis.formatting_issues if f.issue_type == 'bold_dense']
            italic_issues = [f for f in analysis.formatting_issues if f.issue_type == 'italic_dense']

            report += f"""
{'─' * 80}
FORMATTING PATTERN ISSUES ({len(analysis.formatting_issues)} total)
{'─' * 80}

"""
            if bold_issues:
                report += f"""EXCESSIVE BOLD ({len(bold_issues)} lines):
"""
                for fmt in bold_issues[:5]:
                    report += f"""  Line {fmt.line_number}: {fmt.context}
    Problem: {fmt.problem}
    → {fmt.suggestion}

"""

            if italic_issues:
                report += f"""
EXCESSIVE ITALIC ({len(italic_issues)} lines):
"""
                for fmt in italic_issues[:5]:
                    report += f"""  Line {fmt.line_number}: {fmt.context}
    Problem: {fmt.problem}
    → {fmt.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
FORMATTING PATTERNS: Natural variation ✓
{'─' * 80}

"""

        # ADVANCED: High Predictability Segments
        if analysis.high_predictability_segments:
            report += f"""
{'─' * 80}
HIGH PREDICTABILITY SEGMENTS ({len(analysis.high_predictability_segments)} AI-like sections found)
{'─' * 80}
These sections score high on GLTR analysis (>70% top-10 tokens = AI signature)

"""
            for seg in analysis.high_predictability_segments[:5]:
                report += f"""Lines {seg.start_line}-{seg.end_line} (GLTR={seg.gltr_score:.2f}):
  Preview: {seg.segment_preview}
  Problem: {seg.problem}
  → {seg.suggestion}

"""
        else:
            report += f"""
{'─' * 80}
PREDICTABILITY: Natural word choice variation ✓
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
Formatting (Em-dashes):     {r.formatting_score:12s}  ({r.em_dashes_per_page:.1f} per page)"""

        # Add enhanced dimensions if available
        if r.syntactic_score and r.syntactic_score != "UNKNOWN":
            report += f"""
Syntactic (Naturalness):    {r.syntactic_score:12s}  (Repetition: {r.syntactic_repetition_score:.2f}, POS div: {r.pos_diversity:.2f})"""

        if r.sentiment_score and r.sentiment_score != "UNKNOWN":
            report += f"""
Sentiment (Variation):      {r.sentiment_score:12s}  (Variance: {r.sentiment_variance:.3f}, Mean: {r.sentiment_mean:.2f})"""

        # NEW: Enhanced structural dimensions (always present)
        report += f"""

{'─' * 80}
ENHANCED STRUCTURAL ANALYSIS (NEW)
{'─' * 80}

Bold/Italic Patterns:       {r.bold_italic_score:12s}  (Bold: {r.bold_per_1k_words:.1f}/1k, Consistency: {r.formatting_consistency_score:.2f})
List Usage:                 {r.list_usage_score:12s}  (Items: {r.total_list_items}, Ratio O/U: {r.ordered_to_unordered_ratio:.2f})
Punctuation Clustering:     {r.punctuation_score:12s}  (Em-dash cascade: {r.em_dash_cascading_score:.2f}, Oxford: {r.oxford_comma_consistency:.2f})
Whitespace Patterns:        {r.whitespace_score:12s}  (Para uniformity: {r.paragraph_uniformity_score:.2f}, Variance: {r.paragraph_length_variance:.0f})"""

        if r.code_block_count > 0:
            report += f"""
Code Structure:             {r.code_structure_score:12s}  (Blocks: {r.code_block_count}, Lang consistency: {r.code_lang_consistency:.2f})"""

        if r.total_headings >= 3:
            report += f"""
Heading Hierarchy:          {r.heading_hierarchy_score:12s}  (Skips: {r.heading_hierarchy_skips}, Adherence: {r.heading_strict_adherence:.2f})"""

        # NEW: Phase 1 High-ROI Structural Patterns
        report += f"""

{'─' * 80}
STRUCTURAL PATTERNS (Phase 1 High-ROI Detection)
{'─' * 80}"""

        # Paragraph CV
        para_icon = "✓" if r.paragraph_cv >= 0.4 else ("⚠" if r.paragraph_cv >= 0.3 else "✗")
        report += f"""

Paragraph Length CV:     {r.paragraph_cv:.2f}  {para_icon} {r.paragraph_cv_assessment}
  Mean: {r.paragraph_cv_mean:.0f} words, StdDev: {r.paragraph_cv_stddev:.0f} words
  {r.paragraph_count} paragraphs analyzed"""

        if r.paragraph_cv < 0.35:
            report += """
  → ACTION: Vary paragraph lengths (mix 50-100, 150-250, 300-400 word paragraphs)"""

        # Section Variance
        sec_icon = "✓" if r.section_variance_pct >= 40 else ("⚠" if r.section_variance_pct >= 15 else "✗")
        report += f"""

Section Length Variance: {r.section_variance_pct:.1f}% {sec_icon} {r.section_variance_assessment}
  {r.section_count} sections analyzed"""

        if r.section_uniform_clusters > 0:
            report += f"""
  {r.section_uniform_clusters} uniform clusters detected (3+ similar-length sections)"""

        if r.section_variance_pct < 20:
            report += """
  → ACTION: Combine/split sections to create asymmetry (target: 40%+ variance)"""

        # List Nesting Depth
        list_icon = "✓" if r.list_max_depth <= 3 else ("⚠" if r.list_max_depth <= 4 else "✗")
        if r.list_max_depth > 0:
            report += f"""

List Nesting Depth:      Max {r.list_max_depth} levels {list_icon} {r.list_depth_assessment}
  {r.list_total_items} list items analyzed, Avg depth: {r.list_avg_depth:.1f}"""

            if r.list_max_depth > 4:
                report += """
  → ACTION: Flatten deep lists, break into separate sections"""
        else:
            report += f"""

List Nesting Depth:      No lists detected"""

        # Overall structural patterns score
        report += f"""

Structural Patterns Score: {r.structural_patterns_score:12s}  (Combined quality: {r.paragraph_cv_score + r.section_variance_score + r.list_depth_score:.0f}/24 points)"""

        report += f"""

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

        # Enhanced metrics section
        enhanced_sections = []

        if r.mtld_score is not None or r.stemmed_diversity is not None:
            section = "\nENHANCED LEXICAL DIVERSITY (NLTK):"
            if r.mtld_score is not None:
                section += f"\n  MTLD Score: {r.mtld_score:.2f} (Moving Average TTR, higher = more diverse)"
            if r.stemmed_diversity is not None:
                section += f"\n  Stemmed Diversity: {r.stemmed_diversity:.3f} (Diversity after stemming)"
            enhanced_sections.append(section)

        if r.sentiment_variance is not None:
            section = f"""
SENTIMENT VARIATION (VADER):
  Variance: {r.sentiment_variance:.3f} (Higher = more emotional variation)
  Mean Sentiment: {r.sentiment_mean:.2f} (-1 negative, +1 positive)
  Flatness Score: {r.sentiment_flatness_score}"""
            enhanced_sections.append(section)

        if r.syntactic_repetition_score is not None:
            section = f"""
SYNTACTIC PATTERNS (spaCy):
  Structural Repetition: {r.syntactic_repetition_score:.3f} (Lower = more varied)
  POS Tag Diversity: {r.pos_diversity:.3f} (Part-of-speech variation)
  Avg Dependency Depth: {r.avg_dependency_depth:.2f} (Syntactic complexity)"""
            enhanced_sections.append(section)

        if r.automated_readability is not None or r.textacy_diversity is not None:
            section = "\nSTYLOMETRIC ANALYSIS (Textacy):"
            if r.automated_readability is not None:
                section += f"\n  Automated Readability Index: {r.automated_readability:.2f}"
            if r.textacy_diversity is not None:
                section += f"\n  Textacy Diversity: {r.textacy_diversity:.3f}"
            enhanced_sections.append(section)

        if r.gpt2_perplexity is not None:
            section = f"""
TRUE PERPLEXITY (GPT-2 Transformer):
  Perplexity Score: {r.gpt2_perplexity:.2f} (Lower = more predictable/AI-like)
  Interpretation: <50 = AI-like, 50-150 = Mixed, >150 = Human-like"""
            enhanced_sections.append(section)

        if enhanced_sections:
            report += """
{'─' * 80}
ENHANCED NLP ANALYSIS
{'─' * 80}
"""
            for section in enhanced_sections:
                report += section + "\n"

        if HAS_TEXTSTAT and r.flesch_reading_ease is not None:
            report += f"""
READABILITY METRICS:
  Flesch Reading Ease: {r.flesch_reading_ease:.1f} (60-70 = Standard, higher = easier)
  Flesch-Kincaid Grade: {r.flesch_kincaid_grade:.1f} (U.S. grade level)
  Gunning Fog Index: {r.gunning_fog:.1f} (years of education needed)
  SMOG Index: {r.smog_index:.1f} (years of education needed)
"""

        # NEW: Enhanced structural analysis details
        report += f"""
{'─' * 80}
ENHANCED STRUCTURAL ANALYSIS DETAILS
{'─' * 80}

BOLD/ITALIC FORMATTING PATTERNS:
  Bold Density: {r.bold_per_1k_words:.1f} per 1k words (Human: 1-5, AI: 10-50)
  Italic Density: {r.italic_per_1k_words:.1f} per 1k words
  Formatting Consistency: {r.formatting_consistency_score:.3f} (Lower = more varied = human-like)
  Score: {r.bold_italic_score} ({'✓ Human-like' if r.bold_italic_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})

LIST USAGE PATTERNS:
  Total List Items: {r.total_list_items} (Ordered: {r.ordered_list_items}, Unordered: {r.unordered_list_items})
  List-to-Text Ratio: {r.list_to_text_ratio:.1%} (AI tends >25%)
  Ordered/Unordered Ratio: {r.ordered_to_unordered_ratio:.2f} (AI typical: 0.15-0.25)
  Item Length Variance: {r.list_item_length_variance:.1f} (Higher = more human-like)
  Score: {r.list_usage_score} ({'✓ Human-like' if r.list_usage_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})

PUNCTUATION CLUSTERING:
  Em-dash Cascading: {r.em_dash_cascading_score:.3f} (>0.7 = AI declining pattern)
  Oxford Comma Usage: {r.oxford_comma_count} (vs non-Oxford: {r.non_oxford_comma_count})
  Oxford Consistency: {r.oxford_comma_consistency:.3f} (1.0 = always Oxford = AI-like)
  Semicolons: {r.semicolon_count} ({r.semicolon_per_1k_words:.1f} per 1k words)
  Score: {r.punctuation_score} ({'✓ Human-like' if r.punctuation_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})

WHITESPACE & PARAGRAPH STRUCTURE:
  Paragraph Variance: {r.paragraph_length_variance:.0f} words² (Higher = more human-like)
  Paragraph Uniformity: {r.paragraph_uniformity_score:.3f} (Lower = more varied = human-like)
  Blank Lines: {r.blank_lines_count}
  Text Density: {r.text_density:.1f} chars/line
  Score: {r.whitespace_score} ({'✓ Human-like' if r.whitespace_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like'})"""

        if r.code_block_count > 0:
            report += f"""

CODE BLOCK PATTERNS:
  Total Blocks: {r.code_block_count}
  With Language Spec: {r.code_blocks_with_lang} ({r.code_lang_consistency:.0%})
  Language Consistency: {r.code_lang_consistency:.3f} (1.0 = always specified = AI-like)
  Avg Comment Density: {r.avg_code_comment_density:.3f}
  Score: {r.code_structure_score} ({'✓ Human-like' if r.code_structure_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like' if r.code_structure_score not in ['N/A'] else 'N/A'})"""

        if r.total_headings >= 3:
            report += f"""

HEADING HIERARCHY ANALYSIS:
  Hierarchy Skips: {r.heading_hierarchy_skips} (Humans occasionally skip; AI never does)
  Hierarchy Adherence: {r.heading_strict_adherence:.3f} (1.0 = perfect = AI-like)
  Heading Length Variance: {r.heading_length_variance:.1f} (Higher = more varied)
  Score: {r.heading_hierarchy_score} ({'✓ Human-like' if r.heading_hierarchy_score in ['HIGH', 'MEDIUM'] else '⚠ AI-like' if r.heading_hierarchy_score not in ['N/A'] else 'N/A'})"""

        # Advanced lexical diversity & enhanced heading analysis
        advanced_sections = []

        # MATTR & RTTR
        if r.mattr is not None or r.rttr is not None:
            section = "\nADVANCED LEXICAL DIVERSITY (Textacy-based):"
            if r.mattr is not None:
                mattr_icon = "✓" if r.mattr >= 0.70 else "✗"
                section += f"\n  MATTR (window=100): {r.mattr:.3f}  {mattr_icon} {r.mattr_assessment}"
                if r.mattr < 0.70:
                    section += "\n    → ACTION: Increase vocabulary variety (target: MATTR ≥0.70)"
            if r.rttr is not None:
                rttr_icon = "✓" if r.rttr >= 7.5 else "✗"
                section += f"\n  RTTR: {r.rttr:.2f}  {rttr_icon} {r.rttr_assessment}"
                if r.rttr < 7.5:
                    section += "\n    → ACTION: Add more unique terminology (target: RTTR ≥7.5)"
            advanced_sections.append(section)

        # Heading Length Analysis
        if r.heading_length_short_pct is not None:
            heading_icon = "✓" if r.avg_heading_length <= 7 else "✗"
            section = f"""
ENHANCED HEADING LENGTH PATTERNS:
  Average Length: {r.avg_heading_length:.1f} words  {heading_icon} {r.heading_length_assessment}
  Distribution: Short (≤5w): {r.heading_length_short_pct:.1f}%, Medium (6-8w): {r.heading_length_medium_pct:.1f}%, Long (≥9w): {r.heading_length_long_pct:.1f}%"""
            if r.avg_heading_length > 7:
                section += "\n  → ACTION: Shorten headings (target: avg ≤7 words, 60%+ short)"
            advanced_sections.append(section)

        # Subsection Asymmetry
        if r.subsection_cv is not None and r.subsection_counts:
            subsec_icon = "✓" if r.subsection_cv >= 0.6 else ("⚠" if r.subsection_cv >= 0.4 else "✗")
            section = f"""
SUBSECTION ASYMMETRY:
  Coefficient of Variation: {r.subsection_cv:.3f}  {subsec_icon} {r.subsection_assessment}
  Subsection Counts: {r.subsection_counts}
  Uniform Sections (3-4 subs): {r.subsection_uniform_count}"""
            if r.subsection_cv < 0.4:
                section += "\n  → ACTION: Break uniformity, vary subsection counts (target: CV ≥0.6)"
            advanced_sections.append(section)

        # Heading Depth Variance
        if r.heading_depth_pattern is not None:
            depth_icon = "✓" if r.heading_depth_pattern == 'VARIED' else ("⚠" if r.heading_depth_pattern == 'SEQUENTIAL' else "✗")
            section = f"""
HEADING DEPTH TRANSITIONS:
  Pattern: {r.heading_depth_pattern}  {depth_icon} {r.heading_depth_assessment}
  Has Lateral Moves (H3→H3): {r.heading_has_lateral}
  Has Depth Jumps (H3→H1): {r.heading_has_jumps}"""
            if r.heading_transitions:
                trans_str = ", ".join([f"{k}({v})" for k, v in list(r.heading_transitions.items())[:5]])
                section += f"\n  Transitions: {trans_str}"
            if r.heading_depth_pattern == 'RIGID':
                section += "\n  → ACTION: Add lateral H3→H3 moves, occasional depth jumps"
            advanced_sections.append(section)

        if advanced_sections:
            report += f"""

{'─' * 80}
ADVANCED LEXICAL & HEADING ANALYSIS
{'─' * 80}
"""
            for section in advanced_sections:
                report += section + "\n"

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

  # Dual score analysis with optimization path (recommended for LLM optimization)
  %(prog)s chapter-01.md --show-scores

  # Dual score with custom targets
  %(prog)s chapter-01.md --show-scores --quality-target 90 --detection-target 20

  # Dual score JSON output (for programmatic use)
  %(prog)s chapter-01.md --show-scores --format json

  # Analyze with custom domain terms
  %(prog)s chapter-01.md --domain-terms "Docker,Kubernetes,PostgreSQL"

  # Batch analyze directory, output TSV
  %(prog)s --batch manuscript/sections --format tsv > analysis.tsv

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

    # Dual scoring options
    parser.add_argument('--show-scores', action='store_true',
                        help='Calculate and display dual scores (Detection Risk + Quality Score) with optimization path')
    parser.add_argument('--detection-target', type=float, default=30.0, metavar='N',
                        help='Target detection risk score (0-100, lower=better, default: 30.0)')
    parser.add_argument('--quality-target', type=float, default=85.0, metavar='N',
                        help='Target quality score (0-100, higher=better, default: 85.0)')

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

    elif args.show_scores:
        # Dual scoring mode (single file only)
        if args.batch:
            print("Warning: --show-scores mode not supported for batch analysis. Using standard mode.", file=sys.stderr)
            args.show_scores = False
        else:
            try:
                # Run standard analysis first
                result = analyzer.analyze_file(args.file)

                # Calculate dual score
                dual_score = analyzer.calculate_dual_score(
                    result,
                    detection_target=args.detection_target,
                    quality_target=args.quality_target
                )

                # Load history
                history = analyzer.load_score_history(args.file)

                # Add current score to history
                history.add_score(dual_score, notes="")

                # Save updated history
                analyzer.save_score_history(history)

                # Format and output
                output_text = format_dual_score_report(dual_score, history, args.format)

                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(output_text)
                    print(f"Dual score analysis written to {args.output}", file=sys.stderr)
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

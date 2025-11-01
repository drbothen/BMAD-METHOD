# Code Review: analyze_ai_patterns.py

**Date**: November 1, 2025
**File Size**: 2,809 lines
**Functions/Methods**: 53
**Status**: Production-ready, but could benefit from refactoring

---

## Executive Summary

The `analyze_ai_patterns.py` script is **functionally excellent** and well-researched, with comprehensive AI pattern detection across 14 dimensions. However, at 2,809 lines with 53 functions in a single file, it would benefit from:

1. **Extracting magic numbers to named constants** (30+ hardcoded thresholds)
2. **Refactoring scoring functions** (13 similar functions with repetitive patterns)
3. **Splitting into modules** for better organization
4. **Improving error handling** for edge cases
5. **Adding configuration file support** for threshold customization

---

## Priority 1: Extract Magic Numbers to Constants

### Current Issue

Magic numbers scattered throughout scoring functions make thresholds difficult to understand and maintain:

```python
# Line 1939 - What does 0.4 represent?
if list_ratio > 0.4:  # >40% of content in lists
    issues += 2

# Line 1976 - Cascading threshold
if cascading > 0.7:
    issues += 3  # Strong AI marker

# Line 1913 - Bold consistency
if consistency > 0.7:
    issues += 2
```

### Recommended Solution

Create a `ScoringThresholds` configuration class at the top of the file:

```python
@dataclass
class ScoringThresholds:
    """Research-backed thresholds for AI pattern detection"""

    # PERPLEXITY (Vocabulary)
    AI_VOCAB_VERY_LOW_THRESHOLD: float = 10.0  # per 1k words
    AI_VOCAB_LOW_THRESHOLD: float = 5.0
    AI_VOCAB_MEDIUM_THRESHOLD: float = 2.0

    # BURSTINESS (Sentence Variation)
    SENTENCE_STDEV_HIGH: float = 10.0
    SENTENCE_STDEV_MEDIUM: float = 6.0
    SENTENCE_STDEV_LOW: float = 3.0
    SHORT_SENTENCE_MIN_RATIO: float = 0.15  # 15% minimum
    LONG_SENTENCE_MIN_RATIO: float = 0.15

    # FORMATTING (Bold/Italic)
    BOLD_HUMAN_MAX_PER_1K: float = 5.0
    BOLD_AI_MIN_PER_1K: float = 10.0
    BOLD_EXTREME_AI_PER_1K: float = 20.0
    FORMATTING_CONSISTENCY_AI_THRESHOLD: float = 0.7
    FORMATTING_CONSISTENCY_MEDIUM: float = 0.5

    # LIST USAGE
    LIST_RATIO_HIGH_THRESHOLD: float = 0.40  # >40% = AI pattern
    LIST_RATIO_MEDIUM_THRESHOLD: float = 0.25
    LIST_ORDERED_UNORDERED_AI_MIN: float = 0.15
    LIST_ORDERED_UNORDERED_AI_MAX: float = 0.25
    LIST_ITEM_VARIANCE_MIN: float = 5.0

    # PUNCTUATION CLUSTERING
    EM_DASH_CASCADING_STRONG: float = 0.7  # Strong AI marker
    EM_DASH_CASCADING_MODERATE: float = 0.5
    EM_DASH_CASCADING_WEAK: float = 0.3
    OXFORD_COMMA_ALWAYS: float = 0.9  # AI-like consistency
    OXFORD_COMMA_USUALLY: float = 0.75
    OXFORD_COMMA_MIN_INSTANCES: int = 3

    # WHITESPACE & PARAGRAPHS
    PARAGRAPH_UNIFORMITY_AI_THRESHOLD: float = 0.7
    PARAGRAPH_UNIFORMITY_MEDIUM: float = 0.5
    PARAGRAPH_UNIFORMITY_LOW: float = 0.3

    # CODE STRUCTURE
    CODE_LANG_PERFECT_CONSISTENCY: float = 1.0
    CODE_LANG_HIGH_CONSISTENCY: float = 0.8
    CODE_MIN_BLOCKS_FOR_PERFECT_FLAG: int = 3

    # HEADING HIERARCHY
    HEADING_PERFECT_ADHERENCE: float = 1.0
    HEADING_HIGH_ADHERENCE: float = 0.9
    HEADING_MIN_HEADINGS_FOR_PERFECT_FLAG: int = 5
    HEADING_PARALLELISM_HIGH: float = 0.7
    HEADING_PARALLELISM_MEDIUM: float = 0.4
    HEADING_VERBOSE_RATIO: float = 0.3  # >30% of headings

    # STRUCTURE
    FORMULAIC_TRANSITIONS_PER_PAGE_MAX: int = 3
    HEADING_MAX_DEPTH: int = 3

    # VOICE & AUTHENTICITY
    CONTRACTION_RATIO_GOOD: float = 1.0  # >1% use

    # TECHNICAL DEPTH
    DOMAIN_TERMS_HIGH_PER_1K: float = 20.0
    DOMAIN_TERMS_MEDIUM_PER_1K: float = 10.0
    DOMAIN_TERMS_LOW_PER_1K: float = 5.0
    DOMAIN_TERMS_VERY_LOW_PER_1K: float = 0.5

    # FORMATTING (Em-dashes)
    EM_DASH_MAX_PER_PAGE: float = 2.0
    EM_DASH_MEDIUM_PER_PAGE: float = 4.0

    # GPT-2 PERPLEXITY
    GPT2_PERPLEXITY_AI_LIKE: float = 50.0  # <50 = AI-like
    GPT2_PERPLEXITY_HUMAN_LIKE: float = 150.0  # >150 = human-like

# Create default instance
THRESHOLDS = ScoringThresholds()
```

**Benefits**:

- Single source of truth for all thresholds
- Easy to adjust based on new research
- Self-documenting with clear names
- Could be loaded from YAML config file

---

## Priority 2: Refactor Scoring Functions

### Current Issue

13 scoring functions (`_score_perplexity`, `_score_burstiness`, etc.) follow nearly identical patterns:

```python
def _score_perplexity(self, r: AnalysisResults) -> str:
    ai_per_1k = r.ai_words_per_1k
    if ai_per_1k > 10:
        return "VERY LOW"
    elif ai_per_1k > 5:
        return "LOW"
    elif ai_per_1k > 2:
        return "MEDIUM"
    else:
        return "HIGH"

def _score_burstiness(self, r: AnalysisResults) -> str:
    stdev = r.sentence_stdev
    # ... nearly identical structure
    if stdev >= 10 and short_pct >= 0.15 and long_pct >= 0.15:
        return "HIGH"
    elif stdev >= 6:
        return "MEDIUM"
    # ... etc
```

### Recommended Solution

Create a generic threshold-based scorer:

```python
@dataclass
class ScoreCriteria:
    """Criteria for scoring a dimension"""
    high_conditions: List[Tuple[str, Callable[[AnalysisResults], bool]]]
    medium_conditions: List[Tuple[str, Callable[[AnalysisResults], bool]]]
    low_conditions: List[Tuple[str, Callable[[AnalysisResults], bool]]]
    very_low_conditions: List[Tuple[str, Callable[[AnalysisResults], bool]]]

def _score_dimension(self, r: AnalysisResults, criteria: ScoreCriteria) -> str:
    """Generic scoring based on criteria"""
    # Check VERY LOW first (worst case)
    for name, condition in criteria.very_low_conditions:
        if condition(r):
            return "VERY LOW"

    # Check LOW
    for name, condition in criteria.low_conditions:
        if condition(r):
            return "LOW"

    # Check MEDIUM
    for name, condition in criteria.medium_conditions:
        if condition(r):
            return "MEDIUM"

    # Default to HIGH
    return "HIGH"
```

Then define criteria as configuration:

```python
PERPLEXITY_CRITERIA = ScoreCriteria(
    high_conditions=[
        ("ai_vocab_minimal", lambda r: r.ai_words_per_1k <= THRESHOLDS.AI_VOCAB_MEDIUM_THRESHOLD)
    ],
    medium_conditions=[
        ("ai_vocab_acceptable", lambda r: r.ai_words_per_1k <= THRESHOLDS.AI_VOCAB_LOW_THRESHOLD)
    ],
    low_conditions=[
        ("ai_vocab_high", lambda r: r.ai_words_per_1k <= THRESHOLDS.AI_VOCAB_VERY_LOW_THRESHOLD)
    ],
    very_low_conditions=[
        ("ai_vocab_extreme", lambda r: r.ai_words_per_1k > THRESHOLDS.AI_VOCAB_VERY_LOW_THRESHOLD)
    ]
)

def _score_perplexity(self, r: AnalysisResults) -> str:
    return self._score_dimension(r, PERPLEXITY_CRITERIA)
```

**Benefits**:

- Reduces 13 functions from ~300 lines to ~100 lines
- Makes scoring logic explicit and declarative
- Easier to test individual criteria
- Reduces duplication

---

## Priority 3: Module Organization

### Current Issue

Single 2,809-line file contains:

- Data classes (7)
- Analyzer class with 40+ methods
- Formatting functions (2)
- Main entry point (1)

### Recommended Solution

Split into logical modules:

```
tools/
├── analyze_ai_patterns.py          # Main entry point (200 lines)
├── ai_analysis/
│   ├── __init__.py
│   ├── config.py                   # ScoringThresholds, constants (150 lines)
│   ├── models.py                   # All dataclasses (250 lines)
│   ├── analyzer.py                 # AIPatternAnalyzer class (800 lines)
│   ├── scorers.py                  # All _score_* functions (400 lines)
│   ├── structural.py               # _analyze_bold_italic, etc (600 lines)
│   ├── nlp_enhanced.py             # NLP library integrations (400 lines)
│   └── formatters.py               # Report formatting (200 lines)
└── requirements.txt
```

**Migration Strategy**:

1. Create `ai_analysis/` directory
2. Move dataclasses to `models.py`
3. Move constants/config to `config.py`
4. Move analyzer methods to appropriate modules
5. Update imports in main file
6. Add `__init__.py` with clean public API

---

## Priority 4: Configuration File Support

### Current Issue

Thresholds and vocabulary lists are hardcoded in the script. Users can't customize without editing Python code.

### Recommended Solution

Add YAML configuration file support:

**`ai_analysis_config.yaml`**:

```yaml
# AI Pattern Analysis Configuration
# Customize thresholds based on your research or domain

thresholds:
  perplexity:
    ai_vocab_very_low: 10.0 # per 1k words
    ai_vocab_low: 5.0
    ai_vocab_medium: 2.0

  burstiness:
    stdev_high: 10.0
    stdev_medium: 6.0
    stdev_low: 3.0
    short_sentence_ratio: 0.15
    long_sentence_ratio: 0.15

  formatting:
    bold_human_max: 5.0 # per 1k
    bold_ai_min: 10.0
    em_dash_max_per_page: 2.0

  punctuation:
    em_dash_cascading_strong: 0.7
    oxford_comma_always: 0.9

vocabulary:
  # Add domain-specific terms to exclude from AI vocabulary detection
  exclude_for_domain:
    - 'optimize' # Acceptable in performance docs
    - 'leverage' # Acceptable in business context

  # Add custom AI markers for your domain
  custom_ai_markers:
    - 'synergize'
    - 'actualize'

# Enable/disable specific analysis dimensions
features:
  enhanced_nlp: true
  gpt2_perplexity: false # Disable heavy model
  structural_analysis: true
```

**Implementation**:

```python
import yaml
from pathlib import Path

class Config:
    """Load and manage configuration"""

    def __init__(self, config_path: Optional[Path] = None):
        self.thresholds = ScoringThresholds()

        if config_path and config_path.exists():
            self._load_yaml(config_path)

    def _load_yaml(self, path: Path):
        with open(path) as f:
            config = yaml.safe_load(f)

        # Override thresholds from YAML
        if 'thresholds' in config:
            for category, values in config['thresholds'].items():
                for key, value in values.items():
                    attr_name = f"{category.upper()}_{key.upper()}"
                    if hasattr(self.thresholds, attr_name):
                        setattr(self.thresholds, attr_name, value)
```

---

## Priority 5: Error Handling Improvements

### Current Issue

Limited error handling for edge cases:

- Division by zero in scoring functions
- Empty files
- Malformed markdown
- Missing required data

### Recommended Solution

Add comprehensive error handling:

```python
class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass

class EmptyFileError(AnalysisError):
    """Raised when file has no content"""
    pass

class InsufficientDataError(AnalysisError):
    """Raised when not enough data for analysis"""
    pass

def analyze_file(self, file_path: Path) -> AnalysisResults:
    """Analyze with robust error handling"""
    try:
        text = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise AnalysisError(f"Cannot decode file {file_path}: {e}")

    if not text.strip():
        raise EmptyFileError(f"File {file_path} is empty")

    word_count = self._count_words(text)
    if word_count < 50:
        raise InsufficientDataError(
            f"File {file_path} has only {word_count} words. "
            f"Minimum 50 words required for reliable analysis."
        )

    # Proceed with analysis...
```

Add safe division helper:

```python
def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with default for zero denominator"""
    return numerator / denominator if denominator != 0 else default

def safe_ratio(count: int, total: int, default: float = 0.0) -> float:
    """Safe ratio calculation with default for zero total"""
    return (count / total) if total > 0 else default
```

Use throughout scoring functions:

```python
def _score_voice(self, r: AnalysisResults) -> str:
    word_count = r.word_count

    # Old: Could crash if word_count is 0
    # contraction_ratio = (r.contraction_count / word_count) * 100

    # New: Safe with default
    contraction_ratio = safe_ratio(r.contraction_count, word_count) * 100
```

---

## Priority 6: Performance Optimizations

### Current Issue

Multiple regex compilations, repeated text processing, and redundant calculations.

### Recommended Solution

**1. Pre-compile regex patterns:**

```python
class AIPatternAnalyzer:
    def __init__(self, ...):
        # Pre-compile all regex patterns
        self._ai_vocab_patterns = [re.compile(pattern, re.IGNORECASE)
                                   for pattern in self.AI_VOCABULARY]
        self._transition_patterns = [re.compile(pattern)
                                     for pattern in self.FORMULAIC_TRANSITIONS]
        self._bold_pattern = re.compile(r'\*\*[^*]+\*\*|__[^_]+__')
        self._italic_pattern = re.compile(r'\*[^*]+\*|_[^_]+_')
```

**2. Cache expensive computations:**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def _count_words(self, text: str) -> int:
    """Cached word counting"""
    return len(re.findall(r'\b\w+\b', text))
```

**3. Process text once, store results:**

```python
@dataclass
class ProcessedText:
    """Preprocessed text data to avoid re-processing"""
    raw_text: str
    lines: List[str]
    paragraphs: List[str]
    sentences: List[str]
    words: List[str]
    word_count: int
    sentence_count: int
    paragraph_count: int

def _preprocess_text(self, text: str) -> ProcessedText:
    """Process text once, reuse throughout analysis"""
    lines = text.split('\n')
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    sentences = re.split(r'[.!?]+\s+', text)
    words = re.findall(r'\b\w+\b', text)

    return ProcessedText(
        raw_text=text,
        lines=lines,
        paragraphs=paragraphs,
        sentences=sentences,
        words=words,
        word_count=len(words),
        sentence_count=len(sentences),
        paragraph_count=len(paragraphs)
    )
```

---

## Priority 7: Testing Infrastructure

### Current Issue

No unit tests for 53 functions with complex logic and numerous edge cases.

### Recommended Solution

Create comprehensive test suite:

```python
# tests/test_scorers.py
import pytest
from ai_analysis.analyzer import AIPatternAnalyzer
from ai_analysis.models import AnalysisResults

class TestPerplexityScorer:
    """Test perplexity scoring thresholds"""

    def test_high_score_minimal_ai_vocab(self):
        """Should score HIGH when AI words ≤ 2 per 1k"""
        results = AnalysisResults(
            ai_word_count=2,
            ai_words_per_1k=1.5,
            word_count=1000
        )
        analyzer = AIPatternAnalyzer()
        assert analyzer._score_perplexity(results) == "HIGH"

    def test_very_low_score_heavy_ai_vocab(self):
        """Should score VERY LOW when AI words > 10 per 1k"""
        results = AnalysisResults(
            ai_word_count=15,
            ai_words_per_1k=15.0,
            word_count=1000
        )
        analyzer = AIPatternAnalyzer()
        assert analyzer._score_perplexity(results) == "VERY LOW"

    def test_threshold_boundaries(self):
        """Test exact threshold boundaries"""
        analyzer = AIPatternAnalyzer()

        # Exactly at MEDIUM/LOW boundary (5.0)
        results_at_boundary = AnalysisResults(
            ai_word_count=5, ai_words_per_1k=5.0, word_count=1000
        )
        assert analyzer._score_perplexity(results_at_boundary) == "MEDIUM"

# tests/test_structural_analysis.py
class TestBoldItalicAnalysis:
    """Test bold/italic pattern detection"""

    def test_chatgpt_bold_overuse_detected(self):
        """Should detect ChatGPT's 10x bold overuse"""
        text = "**Bold** word " * 30  # ~60 bold per 1k words
        analyzer = AIPatternAnalyzer()
        result = analyzer._analyze_bold_italic_patterns(text)
        assert result['bold_per_1k'] > 50  # ChatGPT threshold

# tests/test_config.py
class TestConfiguration:
    """Test configuration loading"""

    def test_default_thresholds(self):
        """Should use default thresholds when no config"""
        thresholds = ScoringThresholds()
        assert thresholds.AI_VOCAB_VERY_LOW_THRESHOLD == 10.0

    def test_yaml_override(self):
        """Should override thresholds from YAML"""
        config = Config(Path("test_config.yaml"))
        assert config.thresholds.AI_VOCAB_VERY_LOW_THRESHOLD == 12.0  # Overridden
```

**Run tests**:

```bash
pytest tests/ -v --cov=ai_analysis --cov-report=html
```

---

## Priority 8: Documentation Improvements

### Current Issue

- Missing function docstrings for many methods
- No type hints on some return values
- Limited inline comments explaining complex logic

### Recommended Solution

**1. Add comprehensive docstrings:**

```python
def _analyze_punctuation_clustering(self, text: str) -> Dict[str, Any]:
    """
    Analyze punctuation patterns that distinguish AI from human writing.

    Detects three key AI markers:
    1. Em-dash cascading: AI shows declining frequency (high early, low later)
    2. Oxford comma consistency: AI approaches 1.0, humans vary 0.4-0.8
    3. Semicolon usage patterns

    Research basis:
    - Em-dash cascading >0.7 = strong AI marker (95% accuracy)
    - Perfect Oxford comma consistency (1.0) with 3+ instances = AI-like

    Args:
        text: Markdown text to analyze

    Returns:
        Dictionary with keys:
        - 'em_dash_positions': List of paragraph indices with em-dashes
        - 'em_dash_cascading': Score 0-1 (>0.7 = AI pattern)
        - 'oxford_comma_count': Count of "a, b, and c" patterns
        - 'non_oxford_comma_count': Count of "a, b and c" patterns
        - 'oxford_consistency': 0-1 (1.0 = always Oxford = AI-like)
        - 'semicolon_count': Total semicolons
        - 'semicolon_per_1k': Density per 1k words

    Example:
        >>> analyzer = AIPatternAnalyzer()
        >>> result = analyzer._analyze_punctuation_clustering(text)
        >>> if result['em_dash_cascading'] > 0.7:
        ...     print("Strong AI cascading pattern detected")
    """
    # Implementation...
```

**2. Add type hints everywhere:**

```python
from typing import Dict, List, Tuple, Optional, Union, Any

def _calculate_perplexity(
    self,
    text: str,
    model: Optional[str] = "gpt2"
) -> Tuple[float, str]:
    """
    Calculate true perplexity using transformer model.

    Returns:
        Tuple of (perplexity_score, interpretation_string)
    """
    pass
```

---

## Summary of Improvements

| Priority | Improvement         | Effort | Impact    | Lines Saved            |
| -------- | ------------------- | ------ | --------- | ---------------------- |
| 1        | Extract constants   | Medium | High      | +150, cleaner code     |
| 2        | Refactor scorers    | High   | High      | -200 lines             |
| 3        | Module organization | High   | Very High | Better maintainability |
| 4        | Config file support | Medium | High      | +100, more flexibility |
| 5        | Error handling      | Low    | Medium    | +50, more robust       |
| 6        | Performance         | Low    | Medium    | Faster analysis        |
| 7        | Testing             | High   | Very High | +500 test lines        |
| 8        | Documentation       | Medium | High      | Better usability       |

---

## Immediate Quick Wins (Can Do Today)

1. **Extract the 6 most common magic numbers** (30 minutes):
   - `0.7` (cascading/consistency threshold)
   - `0.4` / `0.25` (list ratio thresholds)
   - `10.0` / `5.0` / `2.0` (AI vocab thresholds)
   - `16-18` (em-dash per page)

2. **Add safe division helper** (15 minutes):
   - Replace `x / y` with `safe_divide(x, y)` in scorers
   - Prevents division by zero crashes

3. **Add missing docstrings to top 10 most complex functions** (60 minutes):
   - `_analyze_punctuation_clustering`
   - `_analyze_bold_italic_patterns`
   - `_score_dimension` (new generic scorer)
   - `_assess_overall`

4. **Pre-compile regex patterns** (30 minutes):
   - Move to `__init__` as instance variables
   - Immediate 20-30% performance improvement

---

## Long-term Refactoring Roadmap

### Phase 1: Foundation (Week 1)

- [ ] Extract all magic numbers to `ScoringThresholds` dataclass
- [ ] Add comprehensive type hints
- [ ] Add error handling (EmptyFileError, InsufficientDataError)
- [ ] Pre-compile all regex patterns

### Phase 2: Modularization (Week 2)

- [ ] Create `ai_analysis/` package structure
- [ ] Split into 7 modules (config, models, analyzer, scorers, structural, nlp, formatters)
- [ ] Update imports and test

### Phase 3: Enhancement (Week 3)

- [ ] Add YAML configuration file support
- [ ] Implement generic `_score_dimension()` function
- [ ] Refactor all 13 scorers to use new system
- [ ] Add configuration validation

### Phase 4: Quality (Week 4)

- [ ] Write comprehensive unit tests (target: 80% coverage)
- [ ] Add integration tests for end-to-end workflows
- [ ] Performance profiling and optimization
- [ ] Documentation review and updates

---

## Conclusion

The `analyze_ai_patterns.py` script is **well-designed and functionally excellent**, with cutting-edge AI detection capabilities. The proposed refactoring will:

✅ Improve maintainability (modular structure)
✅ Enhance flexibility (configuration files)
✅ Increase reliability (error handling, tests)
✅ Boost performance (pre-compiled regex, caching)
✅ Better documentation (type hints, docstrings)

**Recommendation**: Start with Priority 1-2 quick wins (extract constants, refactor scorers) for immediate benefit, then tackle modularization when time permits.

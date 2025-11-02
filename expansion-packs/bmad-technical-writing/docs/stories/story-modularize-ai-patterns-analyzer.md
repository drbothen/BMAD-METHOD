# Story: Modularize AI Patterns Analyzer into Maintainable Modules

**Story ID:** BMAD-TW-REFACTOR-001
**Epic:** Code Quality & Maintainability
**Priority:** HIGH
**Estimated Effort:** 6-8 hours
**Status:** Ready for Development
**Depends On:** None (can be implemented independently)

## Story Overview

As a **developer maintaining the AI pattern analysis tool**, I want the monolithic 7,079-line `analyze_ai_patterns.py` file broken into logical modules of 300-600 lines each, so that the codebase is more maintainable, testable, and easier to extend with new features.

## Business Value

**Problem:**
The current `analyze_ai_patterns.py` file is 7,079 lines long, containing:

- Data structures (dataclasses)
- Core analysis logic
- Scoring algorithms
- Formatting utilities
- Evidence extraction
- History tracking
- CLI interface
- Multiple analysis dimensions (22 total)

This monolithic structure creates several problems:

- Difficult to navigate and understand
- Hard to test individual components in isolation
- Merge conflicts when multiple developers work on different features
- IDE performance degradation with large files
- Difficult to reuse components in other tools
- New features (evidence extraction, history tracking) will add even more complexity

**Impact:**
Modularization will:

- **Improve maintainability** - Each module has clear responsibility
- **Enable parallel development** - Multiple developers can work on different modules
- **Facilitate testing** - Unit tests can target specific modules
- **Support code reuse** - Modules can be imported by other tools
- **Improve IDE performance** - Smaller files load and analyze faster
- **Reduce cognitive load** - Developers only need to understand relevant modules

**Success Metrics:**

- File count increases from 1 to ~12-15 modules
- Largest module is <600 lines
- All existing tests pass without modification
- Import structure is clean and logical
- No circular dependencies
- Backward compatibility maintained for external callers

## User Acceptance Criteria

### AC1: Module Structure Design

**Given** the 7,079-line monolithic file
**When** designing the module structure
**Then** it should be organized as follows:

```
expansion-packs/bmad-technical-writing/data/tools/
├── analyze_ai_patterns.py          # Main CLI entry point (~300 lines)
└── ai_pattern_analyzer/            # Package directory
    ├── __init__.py                 # Package initialization (~50 lines)
    ├── core/                       # Core analysis engine
    │   ├── __init__.py
    │   ├── analyzer.py             # Main AIPatternAnalyzer class (~400 lines)
    │   └── results.py              # Result dataclasses (~300 lines)
    ├── dimensions/                 # Analysis dimensions
    │   ├── __init__.py
    │   ├── perplexity.py           # AI vocabulary & perplexity (~400 lines)
    │   ├── burstiness.py           # Sentence/paragraph variation (~350 lines)
    │   ├── structure.py            # Section/heading analysis (~400 lines)
    │   ├── formatting.py           # Em-dash, bold/italic, etc. (~300 lines)
    │   ├── voice.py                # Voice consistency (~250 lines)
    │   ├── syntactic.py            # Syntactic complexity (spaCy) (~400 lines)
    │   ├── lexical.py              # Lexical diversity (NLTK, textacy) (~450 lines)
    │   ├── stylometric.py          # Stylometric analysis (~350 lines)
    │   └── advanced.py             # GLTR, transformer-based (~400 lines)
    ├── scoring/                    # Scoring system
    │   ├── __init__.py
    │   ├── dual_score.py           # Dual scoring algorithm (~400 lines)
    │   └── dimension_scorer.py     # Individual dimension scorers (~300 lines)
    ├── history/                    # History tracking
    │   ├── __init__.py
    │   ├── tracker.py              # History tracking logic (~350 lines)
    │   └── export.py               # CSV/JSON export (~200 lines)
    ├── evidence/                   # Evidence extraction (future)
    │   ├── __init__.py
    │   ├── formatter.py            # Evidence formatting (~400 lines)
    │   └── extractors.py           # Dimension-specific extractors (~500 lines)
    ├── utils/                      # Utilities
    │   ├── __init__.py
    │   ├── text_processing.py     # Text cleaning, word counting (~200 lines)
    │   ├── pattern_matching.py    # Regex patterns, constants (~300 lines)
    │   └── visualization.py       # Sparklines, charts (~250 lines)
    └── cli/                        # CLI interface
        ├── __init__.py
        ├── args.py                 # Argument parsing (~200 lines)
        └── formatters.py           # Output formatting (~300 lines)
```

**Total:** ~12-15 modules, each 200-600 lines

### AC2: Backward Compatibility

**Given** existing code that imports or calls the analyzer
**When** the modularization is complete
**Then** it should:

- [x] Maintain the same CLI interface (`python analyze_ai_patterns.py file.md`)
- [x] Support existing programmatic imports (if any)
- [x] Preserve all command-line arguments and flags
- [x] Maintain output format compatibility
- [x] Keep history file format unchanged
- [x] Ensure all existing tests pass without modification

**Example backward-compatible usage:**

```python
# Old way (still works)
from analyze_ai_patterns import AIPatternAnalyzer
analyzer = AIPatternAnalyzer("chapter.md")
results = analyzer.analyze()

# New way (also works, more explicit)
from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
analyzer = AIPatternAnalyzer("chapter.md")
results = analyzer.analyze()
```

### AC3: Core Module - analyzer.py

**Given** the main `AIPatternAnalyzer` class
**When** refactored into `ai_pattern_analyzer/core/analyzer.py`
**Then** it should:

- [x] Contain the main `AIPatternAnalyzer` class (~400 lines)
- [x] Implement the primary `analyze()` method
- [x] Coordinate calls to dimension analyzers
- [x] Import dimension modules from `ai_pattern_analyzer.dimensions`
- [x] Import scoring from `ai_pattern_analyzer.scoring`
- [x] Import history tracking from `ai_pattern_analyzer.history`
- [x] Keep initialization logic (load text, parse lines, detect code blocks)
- [x] Maintain all public API methods unchanged

**Key responsibilities:**

- Text loading and preprocessing
- Orchestrating dimension analysis
- Aggregating results
- Coordinating with scoring system

### AC4: Dimensions Package - Multiple Modules

**Given** the 22+ analysis dimensions scattered throughout the monolith
**When** refactored into `ai_pattern_analyzer/dimensions/`
**Then** each module should:

**`perplexity.py`** (~400 lines):

- AI vocabulary detection (`_analyze_ai_vocabulary_detailed`)
- Formulaic transitions (`_analyze_formulaic_transitions`)
- Perplexity calculation (transformer-based if available)
- AI vocabulary scoring (`_score_perplexity`)

**`burstiness.py`** (~350 lines):

- Sentence length analysis (`_analyze_sentence_burstiness`)
- Paragraph variation (`_analyze_paragraph_variation`)
- Paragraph CV calculation (`_calculate_paragraph_cv`)
- Section variance calculation (`_calculate_section_variance`)
- Burstiness scoring (`_score_burstiness`)

**`structure.py`** (~400 lines):

- Heading analysis (`_analyze_headings_detailed`)
- Section variance (`_calculate_section_variance`)
- List nesting depth (`_calculate_list_nesting_depth`)
- Uniform cluster detection (`_count_uniform_clusters`)
- Structure scoring (`_score_structure`)

**`formatting.py`** (~300 lines):

- Em-dash detection (`_analyze_formatting_issues_detailed`)
- Bold/italic usage
- Whitespace patterns
- Code block structure
- Formatting scoring (`_score_formatting`)

**`voice.py`** (~250 lines):

- Voice consistency analysis
- Sentiment variation (`_analyze_sentiment_variation`)
- Technical term density
- Voice scoring (`_score_voice`)

**`syntactic.py`** (~400 lines):

- Syntactic pattern analysis (spaCy-based)
- Dependency tree depth
- Subordination index
- Passive construction detection
- Syntactic scoring (`_score_syntactic`)

**`lexical.py`** (~450 lines):

- Type-Token Ratio (TTR)
- MTLD calculation (`_calculate_mtld`)
- NLTK lexical diversity (`_analyze_nltk_lexical`)
- Textacy diversity (`_calculate_textacy_lexical_diversity`)
- Advanced diversity metrics (`_calculate_advanced_lexical_diversity`)
- Lexical scoring

**`stylometric.py`** (~350 lines):

- Textacy stylometric analysis (`_analyze_textacy_metrics`)
- Function word ratio
- Hapax percentage
- Transition marker frequency
- Stylometric scoring (`_score_stylometric`)

**`advanced.py`** (~400 lines):

- GLTR metrics (`_calculate_gltr_metrics`)
- Transformer perplexity (`_calculate_transformer_perplexity`)
- AI detection ensemble
- Advanced scoring (`_score_gltr`, `_score_advanced_lexical`, `_score_ai_detection`)

**Each dimension module should:**

- Have a clear, single responsibility
- Export a `DimensionAnalyzer` class with standard interface
- Include private helper methods
- Document required dependencies (NLTK, spaCy, etc.)
- Handle missing dependencies gracefully

### AC5: Scoring Package - Dual Score System

**Given** the dual scoring system implementation
**When** refactored into `ai_pattern_analyzer/scoring/`
**Then** it should:

**`dual_score.py`** (~400 lines):

- `DualScore` dataclass
- `DualScoreCategory` dataclass
- `DualScoreDimension` dataclass
- `calculate_dual_score()` function
- Tier 1/2/3 category logic
- Quality score calculation
- Detection risk calculation
- Path-to-target recommendations

**`dimension_scorer.py`** (~300 lines):

- Individual dimension scoring methods
- All `_score_*()` methods from original file
- Scoring thresholds and constants
- Assessment interpretation logic

### AC6: History Package - Tracking & Export

**Given** the score history tracking system
**When** refactored into `ai_pattern_analyzer/history/`
**Then** it should:

**`tracker.py`** (~350 lines):

- `HistoricalScore` dataclass
- `ScoreHistory` dataclass
- `load_score_history()` function
- `save_score_history()` function
- Backward compatibility with v1.0 format
- Trend analysis methods
- Plateau detection

**`export.py`** (~200 lines):

- CSV export functionality
- JSON export functionality
- Sparkline generation
- Comparison report generation

### AC7: Utils Package - Shared Utilities

**Given** utility functions scattered throughout the file
**When** refactored into `ai_pattern_analyzer/utils/`
**Then** it should:

**`text_processing.py`** (~200 lines):

- `_count_words()` function
- Text cleaning utilities
- Code block detection
- Line parsing helpers

**`pattern_matching.py`** (~300 lines):

- `AI_VOCABULARY` constant (large list)
- `FORMULAIC_TRANSITIONS` constant
- `AI_VOCAB_REPLACEMENTS` dictionary
- Regex pattern constants
- Pattern matching utilities

**`visualization.py`** (~250 lines):

- Sparkline generation
- ASCII chart rendering
- Progress bars
- Terminal width detection

### AC8: CLI Package - Command-Line Interface

**Given** the argument parsing and output formatting
**When** refactored into `ai_pattern_analyzer/cli/`
**Then** it should:

**`args.py`** (~200 lines):

- `parse_arguments()` function
- All argument definitions
- Help text
- Argument validation

**`formatters.py`** (~300 lines):

- Output formatting functions
- Table rendering
- Color/ANSI code handling
- Rich library integration (optional)

### AC9: Main Entry Point - analyze_ai_patterns.py

**Given** the main CLI entry point
**When** refactored to use the new module structure
**Then** it should:

- [x] Be ~300 lines maximum
- [x] Import from `ai_pattern_analyzer` package
- [x] Contain only:
  - `main()` function
  - CLI workflow orchestration
  - Argument parsing delegation
  - Output formatting delegation
  - Error handling
- [x] Maintain shebang for direct execution
- [x] Keep all command-line behavior identical

**Example structure:**

```python
#!/usr/bin/env python3
"""
AI Pattern Analyzer - Detect AI-generated content patterns

Main CLI entry point. Implementation is modularized in ai_pattern_analyzer package.
"""

from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
from ai_pattern_analyzer.cli.args import parse_arguments
from ai_pattern_analyzer.cli.formatters import format_results
from ai_pattern_analyzer.scoring.dual_score import calculate_dual_score
from ai_pattern_analyzer.history.tracker import load_score_history, save_score_history
# ... other imports

def main():
    """Main CLI entry point"""
    args = parse_arguments()

    # Load and analyze
    analyzer = AIPatternAnalyzer(args.file)
    results = analyzer.analyze()

    # Score
    if args.show_scores:
        dual_score = calculate_dual_score(results)
        history = load_score_history(args.file)
        history.add_score(dual_score, results, notes=args.history_notes)
        save_score_history(history)

        # Format and display
        output = format_results(dual_score, history, args)
        print(output)

    # ... rest of CLI logic

if __name__ == "__main__":
    main()
```

### AC10: Testing Strategy

**Given** the modularization
**When** testing the changes
**Then** it should:

- [x] All existing tests pass without modification
- [x] New unit tests created for each module
- [x] Integration tests verify modules work together
- [x] Test imports from both old and new paths
- [x] Verify CLI behavior is identical
- [x] Test with all optional dependencies (NLTK, spaCy, etc.)
- [x] Test with missing optional dependencies
- [x] Performance benchmarks show no regression

**Test structure:**

```
tests/
├── test_analyzer.py           # Core analyzer tests
├── test_dimensions/
│   ├── test_perplexity.py
│   ├── test_burstiness.py
│   ├── test_structure.py
│   └── ...
├── test_scoring.py            # Scoring system tests
├── test_history.py            # History tracking tests
├── test_cli.py                # CLI interface tests
└── test_integration.py        # End-to-end tests
```

### AC11: Documentation Updates

**Given** the new module structure
**When** updating documentation
**Then** it should include:

- [x] Updated README with new import examples
- [x] Module-level docstrings explaining purpose
- [x] API documentation for public interfaces
- [x] Migration guide for developers using the code programmatically
- [x] Architecture diagram showing module relationships

### AC12: Update Related Stories

**Given** the modularization changes code structure
**When** updating related story files
**Then** it should:

**`story-evidence-extraction-feature.md`** updates:

- [x] Update "Code Location" section to reference new modules
- [x] Change implementation approach to use modular structure
- [x] Update class/function references to new module paths
- [x] Add note: "Implementation assumes modularized codebase (BMAD-TW-REFACTOR-001)"

**Example changes:**

````markdown
### Code Location

**Files:**

- `/ai_pattern_analyzer/core/analyzer.py` - Main analyzer
- `/ai_pattern_analyzer/evidence/formatter.py` - Evidence formatting (NEW)
- `/ai_pattern_analyzer/evidence/extractors.py` - Evidence extractors (NEW)
- `/ai_pattern_analyzer/dimensions/perplexity.py` - AI vocab analysis
- `/ai_pattern_analyzer/dimensions/formatting.py` - Em-dash analysis

### Implementation Approach

**1. Create Evidence Package**

The evidence extraction system will be implemented as a new package:

- `ai_pattern_analyzer/evidence/` - New package
- `formatter.py` - `EvidenceFormatter` class
- `extractors.py` - Dimension-specific evidence extractors

**2. Enhance Dimension Analyzers**

Each dimension module will be enhanced with evidence extraction:

```python
# In ai_pattern_analyzer/dimensions/perplexity.py
class PerplexityAnalyzer(DimensionAnalyzer):
    def analyze_with_evidence(self, lines: List[str]) -> Tuple[Results, Evidence]:
        """Analyze and extract evidence"""
        # ... existing analysis ...
        evidence = self._extract_evidence(vocab_instances, lines)
        return results, evidence
```
````

**`story-comprehensive-metric-history.md`** updates:

- [x] Update code location references
- [x] Update `HistoricalScore` location to `ai_pattern_analyzer/history/tracker.py`
- [x] Update `ScoreHistory` location
- [x] Update import examples

**Example changes:**

````markdown
### Code Location

**Files:**

- `/ai_pattern_analyzer/history/tracker.py` - History tracking logic
- `/ai_pattern_analyzer/history/export.py` - CSV/JSON export
- `/ai_pattern_analyzer/core/results.py` - Result dataclasses
- `/ai_pattern_analyzer/scoring/dual_score.py` - Dual scoring

### Enhanced Data Structures

```python
# In ai_pattern_analyzer/history/tracker.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class DimensionScore:
    """Individual dimension score for history tracking"""
    # ... (same as before, but in history module)
```
````

## Technical Implementation Details

### Implementation Phases

**Phase 1: Create Package Structure** (~1 hour)

1. Create `ai_pattern_analyzer/` package directory
2. Create all subdirectories (`core/`, `dimensions/`, `scoring/`, etc.)
3. Create all `__init__.py` files
4. Set up package imports

**Phase 2: Extract Data Structures** (~1 hour)

1. Move dataclasses to `core/results.py`
2. Move scoring dataclasses to `scoring/dual_score.py`
3. Move history dataclasses to `history/tracker.py`
4. Update imports

**Phase 3: Extract Dimension Modules** (~2-3 hours)

1. Create base `DimensionAnalyzer` interface
2. Extract each dimension to its module:
   - `perplexity.py` - AI vocabulary, formulaic transitions
   - `burstiness.py` - Sentence/paragraph variation
   - `structure.py` - Headings, sections, lists
   - `formatting.py` - Em-dashes, bold/italic
   - `voice.py` - Voice consistency, sentiment
   - `syntactic.py` - spaCy-based analysis
   - `lexical.py` - NLTK/textacy lexical diversity
   - `stylometric.py` - Stylometric features
   - `advanced.py` - GLTR, transformers
3. Each module exports analyzer class with standard interface

**Phase 4: Extract Scoring** (~1 hour)

1. Move scoring logic to `scoring/dual_score.py`
2. Move dimension scorers to `scoring/dimension_scorer.py`
3. Update imports in analyzer

**Phase 5: Extract History** (~30 minutes)

1. Move history tracking to `history/tracker.py`
2. Move export functions to `history/export.py`
3. Update imports

**Phase 6: Extract Utils** (~30 minutes)

1. Move text utilities to `utils/text_processing.py`
2. Move patterns to `utils/pattern_matching.py`
3. Move visualization to `utils/visualization.py`
4. Update imports throughout

**Phase 7: Extract CLI** (~30 minutes)

1. Move argument parsing to `cli/args.py`
2. Move formatters to `cli/formatters.py`
3. Update main entry point

**Phase 8: Update Main Entry Point** (~30 minutes)

1. Simplify `analyze_ai_patterns.py` to ~300 lines
2. Import from package modules
3. Maintain CLI behavior

**Phase 9: Testing** (~1 hour)

1. Run existing tests - verify all pass
2. Create new unit tests for modules
3. Test imports from old and new paths
4. Performance benchmarks

**Phase 10: Update Documentation & Stories** (~1 hour)

1. Update story-evidence-extraction-feature.md
2. Update story-comprehensive-metric-history.md
3. Update README.md
4. Add migration guide

### Import Strategy

**Package-level imports** (`ai_pattern_analyzer/__init__.py`):

```python
"""
AI Pattern Analyzer - Modular implementation

Main exports for backward compatibility.
"""

# Core
from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
from ai_pattern_analyzer.core.results import AnalysisResults, DetailedAnalysis

# Scoring
from ai_pattern_analyzer.scoring.dual_score import (
    DualScore,
    DualScoreCategory,
    DualScoreDimension,
    calculate_dual_score
)

# History
from ai_pattern_analyzer.history.tracker import (
    HistoricalScore,
    ScoreHistory,
    load_score_history,
    save_score_history
)

__all__ = [
    'AIPatternAnalyzer',
    'AnalysisResults',
    'DetailedAnalysis',
    'DualScore',
    'calculate_dual_score',
    'HistoricalScore',
    'ScoreHistory',
    'load_score_history',
    'save_score_history',
]
```

### Dependency Management

**Each module declares its dependencies:**

```python
# At top of ai_pattern_analyzer/dimensions/syntactic.py

# Required dependencies
import re
import statistics
from typing import Dict, List, Optional

# Optional dependencies
try:
    import spacy
    nlp_spacy = spacy.load('en_core_web_sm')
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False
    nlp_spacy = None
```

### Module Interface Standard

**All dimension analyzers follow this interface:**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class DimensionAnalyzer(ABC):
    """Base class for dimension analyzers"""

    @abstractmethod
    def analyze(self, text: str, lines: List[str]) -> Dict[str, Any]:
        """
        Analyze text for this dimension

        Args:
            text: Full text content
            lines: Text split into lines

        Returns:
            Dict with analysis results specific to this dimension
        """
        pass

    @abstractmethod
    def score(self, analysis_results: Dict[str, Any]) -> float:
        """
        Calculate score for this dimension

        Args:
            analysis_results: Results from analyze()

        Returns:
            Score (0.0 to max_score for this dimension)
        """
        pass
```

### Migration Path for External Users

**For developers using the code programmatically:**

```python
# OLD (deprecated but still works via __init__.py re-exports):
from analyze_ai_patterns import AIPatternAnalyzer

# NEW (recommended):
from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer

# OR use package-level import:
from ai_pattern_analyzer import AIPatternAnalyzer
```

## Definition of Done

- [x] Package structure created (`ai_pattern_analyzer/` with subdirectories)
- [x] All modules created with appropriate line counts (300-600 lines each)
- [x] `analyze_ai_patterns.py` reduced to ~300 lines as main entry point
- [x] All 22 dimensions extracted to `dimensions/` package
- [x] Scoring system extracted to `scoring/` package
- [x] History tracking extracted to `history/` package
- [x] Utils extracted to `utils/` package
- [x] CLI extracted to `cli/` package
- [x] Package `__init__.py` exports main classes for backward compatibility
- [x] All existing tests pass without modification
- [x] New unit tests created for each module (10+ tests per module)
- [x] CLI behavior is identical to pre-refactor
- [x] Performance benchmarks show no regression (<5% difference)
- [x] Documentation updated (README, docstrings, migration guide)
- [x] story-evidence-extraction-feature.md updated with new module references
- [x] story-comprehensive-metric-history.md updated with new module references
- [x] No circular import dependencies
- [x] All modules have clear docstrings
- [x] Import paths work from external code

## Dependencies and Prerequisites

**Before starting:**

- [x] Current `analyze_ai_patterns.py` is functional
- [x] All tests pass
- [x] Git branch created for refactoring work

**No new external dependencies required**

## Success Metrics (Post-Implementation)

**Measure after refactoring:**

- File count: 1 → ~12-15 modules
- Largest file: 7,079 lines → <600 lines
- Test coverage: Maintained or improved
- Build time: No significant change
- IDE responsiveness: Improved (subjective)
- Merge conflict frequency: Expected to decrease (measure over time)

**Developer experience improvements:**

- Time to locate specific functionality: -50%
- Time to add new dimension: -40%
- Cognitive load for new contributors: -60%
- Parallel development capability: 3-4 developers can work simultaneously

## Risk Assessment

**Primary Risks:**

1. **Import errors during transition**
   - Mitigation: Comprehensive testing, backward-compatible exports
   - Rollback: Revert commit, restore monolithic file

2. **Performance degradation from multiple imports**
   - Mitigation: Lazy imports where appropriate, benchmarking
   - Rollback: If >10% regression, investigate and optimize

3. **Breaking changes for external users**
   - Mitigation: Maintain backward-compatible imports in `__init__.py`
   - Rollback: Add deprecation warnings, maintain old imports longer

4. **Circular dependencies between modules**
   - Mitigation: Careful interface design, dependency graph review
   - Rollback: Restructure module boundaries if detected

**Low Risk because:**

- Pure refactoring (no functionality changes)
- Extensive test suite exists
- Git allows easy rollback
- Can be done incrementally (commit after each phase)

## Related Stories

**Updated by this story:**

- BMAD-TW-DETECT-004 (Evidence Extraction) - Code locations updated
- BMAD-TW-DETECT-005 (Metric History) - Code locations updated

**Enables future work:**

- Easier to implement evidence extraction in modular form
- Simpler to add new detection dimensions
- Better foundation for IDE integration (LSP server)
- Facilitates automated testing of individual dimensions

## Implementation Notes

### Recommended Git Strategy

```bash
# Create feature branch
git checkout -b feature/modularize-analyzer

# Commit after each phase
git commit -m "Phase 1: Create package structure"
git commit -m "Phase 2: Extract data structures"
git commit -m "Phase 3: Extract dimension modules"
# ... etc

# Test at each commit
python -m pytest tests/
python analyze_ai_patterns.py test.md

# Squash commits before merging if desired
git rebase -i main
```

### Module Size Guidelines

- **Target:** 300-600 lines per module
- **Minimum:** 150 lines (below this, consider merging)
- **Maximum:** 650 lines (above this, consider splitting)
- **Exclude:** Imports, docstrings, and blank lines from count

### Code Review Checklist

- [ ] Each module has single, clear responsibility
- [ ] No circular dependencies
- [ ] All imports are used
- [ ] Docstrings present for all public functions/classes
- [ ] Type hints present for function signatures
- [ ] No relative imports outside package
- [ ] Package `__init__.py` exports key classes
- [ ] CLI behavior unchanged
- [ ] All tests pass
- [ ] Performance benchmarks acceptable

## Future Enhancements

Once modularization is complete:

- **Plugin architecture** - Load dimension analyzers dynamically
- **Parallel processing** - Analyze dimensions concurrently
- **Dimension marketplace** - Community-contributed dimensions
- **Language support** - Extend beyond English
- **API server** - REST API for analysis as a service
- **Batch processing** - Analyze multiple files efficiently
- **Incremental analysis** - Only re-analyze changed sections

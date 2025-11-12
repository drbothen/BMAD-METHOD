# Changelog

All notable changes to the AI Pattern Analyzer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0] - 2025-11-10

**BREAKING CHANGES** - This is a major version release that removes deprecated dimensions and backward compatibility code.

### Removed (Story 2.0)

#### Deprecated Dimensions
- **AdvancedDimension** (`dimensions/advanced.py` - 655 lines)
  - Removed in favor of `PredictabilityDimension` and `AdvancedLexicalDimension` (split in Story 1.4.5)
  - GLTR analysis now handled by `PredictabilityDimension`
  - Advanced lexical metrics now handled by `AdvancedLexicalDimension`

- **StylometricDimension** (`dimensions/stylometric.py` - 378 lines)
  - Removed in favor of `ReadabilityDimension` and `TransitionMarkerDimension` (split in Story 1.4.5)
  - Readability metrics now handled by `ReadabilityDimension`
  - Transition marker analysis now handled by `TransitionMarkerDimension`

#### Backward Compatibility Code
- **Removed `StylometricIssue` dataclass** from `core/results.py`
  - TransitionMarkerDimension now uses `TransitionInstance` instead
  - Fields renamed: `marker_type` → `transition`, `suggestion` → `suggestions` (list)

- **Removed `gltr_score` property** from `AnalysisResults`
  - Use `predictability_score` field directly instead

- **Removed `stylometric_score` field** from `AnalysisResults`
  - Use `readability_score` and `transition_marker_score` instead

- **Removed `stylometric_issues` field** from `DetailedAnalysis`
  - Use `transition_instances` from TransitionMarkerDimension instead

- **Removed deprecated parameters** from `_flatten_optional_metrics()`
  - Removed `stylometric_results` parameter
  - Removed `advanced_results` parameter

#### CLI Output
- **Removed stylometric markers section** from detailed reports (48 lines)
  - Transition marker information now reported through standard dimension output

### Changed (Story 2.0)

#### Positive Label System ✨ **NEW**
- **Replaced confusing impact-style labels with positive quality labels** for all dimension scores
  - **OLD labels (v4.x)**: HIGH / MEDIUM / LOW / VERY LOW
  - **NEW labels (v5.0.0)**: **EXCELLENT** / **GOOD** / **NEEDS WORK** / **POOR**
  - **Rationale**: Old labels were backwards - "LOW" sounded bad but meant low problems (good). New labels are intuitive.
  - **Scoring ranges**:
    - EXCELLENT: 85-100 (minimal AI patterns detected)
    - GOOD: 70-84 (some AI patterns, mostly human-like)
    - NEEDS WORK: 50-69 (noticeable AI patterns)
    - POOR: 0-49 (strong AI patterns detected)
  - **Applies to**: All 12 dimension scores in reports and API responses
  - **Implementation**: `core/analyzer.py:774-801` (`_convert_score_to_category()`)
  - **Report Updates**: All 12 dimensions now visible in DIMENSION SCORES section (`cli/formatters.py:746-765`)

#### Dimension Count
- **Updated from 14 to 12 dimensions** in v5.0.0
  - Removed: `advanced`, `stylometric` (deprecated dimensions)
  - Current 12 dimensions: `perplexity`, `burstiness`, `structure`, `formatting`, `voice`, `readability`, `lexical`, `sentiment`, `syntactic`, `predictability`, `advanced_lexical`, `transition_marker`

#### Import Statements
- **Removed `StylometricIssue`** from package exports (`__init__.py`)
  - Use `TransitionInstance` for transition marker issues

### Added (Story 2.0)

- **`validate_no_deprecated()` method** in `DimensionRegistry`
  - Validates that no deprecated dimensions are registered
  - Raises `RuntimeError` if any deprecated dimensions found
  - Useful for ensuring cleanup is complete in v5.0.0+

### Migration Guide (v4.x → v5.0.0)

**BREAKING CHANGES** require code updates:

1. **Update dimension references:**
   ```python
   # OLD (v4.x) - deprecated dimensions
   advanced_dim = analyzer.dimensions.get('advanced')
   stylometric_dim = analyzer.dimensions.get('stylometric')

   # NEW (v5.0.0) - use split dimensions
   predictability_dim = analyzer.dimensions.get('predictability')
   advanced_lexical_dim = analyzer.dimensions.get('advanced_lexical')
   readability_dim = analyzer.dimensions.get('readability')
   transition_marker_dim = analyzer.dimensions.get('transition_marker')
   ```

2. **Update field access:**
   ```python
   # OLD (v4.x) - backward compatibility properties
   gltr_score = results.gltr_score  # Property redirect
   stylometric_score = results.stylometric_score

   # NEW (v5.0.0) - use direct fields
   predictability_score = results.predictability_score  # Direct field
   readability_score = results.readability_score
   transition_marker_score = results.transition_marker_score
   ```

3. **Update issue handling:**
   ```python
   # OLD (v4.x) - StylometricIssue
   from ai_pattern_analyzer.core.results import StylometricIssue
   issues = stylometric_dim.analyze_detailed(lines)
   for issue in issues:
       print(issue.marker_type)  # 'however', 'moreover'

   # NEW (v5.0.0) - TransitionInstance
   from ai_pattern_analyzer.core.results import TransitionInstance
   transition_dim = analyzer.dimensions.get('transition_marker')
   issues = transition_dim.analyze_detailed(lines)
   for issue in issues:
       print(issue.transition)  # 'however', 'moreover'
       print(issue.suggestions)  # List of suggestions
   ```

4. **Update dimension count expectations:**
   ```python
   # OLD (v4.x) - expected 14 dimensions
   assert len(analyzer.dimensions) == 14

   # NEW (v5.0.0) - expect 12 dimensions
   assert len(analyzer.dimensions) == 12
   assert results.dimension_count == 12  # Story 1.10 field
   ```

5. **Update score label expectations:**
   ```python
   # OLD (v4.x) - old label system
   assert results.voice_score == "HIGH"
   assert results.perplexity_score in ["MEDIUM", "LOW"]

   # NEW (v5.0.0) - positive label system
   assert results.voice_score == "EXCELLENT"
   assert results.perplexity_score in ["GOOD", "NEEDS WORK"]

   # Label mapping:
   # HIGH → EXCELLENT (85-100)
   # MEDIUM → GOOD (70-84)
   # LOW → NEEDS WORK (50-69)
   # VERY LOW → POOR (0-49)
   ```

### Technical Details

- **Files deleted:** 4 dimension files + 2 test files (1,033 + test lines removed)
- **Backward compatibility:** **0%** - This is a breaking change release
- **Testing:** All Story 2.0-related tests passing
  - Deleted 4 deprecated tests in `test_analyzer.py`
  - Deleted `test_stylometric.py` (4 tests)
  - Updated `test_transition_marker.py` (43 tests passing)
  - Fixed field name changes: `marker_type` → `transition`

### Dependencies

- No changes to external dependencies
- Python 3.7+ still required
- All dimension dependencies unchanged (nltk, textstat, etc.)

### Known Issues

- None related to Story 2.0 changes
- Pre-existing issues in `test_structure_phase3.py` and `test_voice.py` are unrelated to this release

---

## [Unreleased]

### Added

#### Analysis Modes (Story 1.4.9)

- **Four analysis modes** to balance speed and accuracy:
  - `--mode fast`: Quick analysis of document start (default) - ~2000 chars per dimension
  - `--mode adaptive`: Intelligent sampling based on document size (recommended) - adjusts coverage automatically
  - `--mode sampling`: Custom sampling strategy with `--samples` and `--sample-size` options
  - `--mode full`: Complete document analysis - 100% coverage, maximum accuracy

- **Mode-specific CLI arguments**:
  - `--mode {fast,adaptive,sampling,full}`: Select analysis mode
  - `--samples N`: Number of samples for sampling mode (1-50, default: 10)
  - `--sample-size N`: Characters per sample for sampling mode (default: 2000)
  - `--sampling-strategy {uniform,weighted,start,end}`: Sampling distribution strategy
  - `--dry-run`: Preview analysis configuration without running analysis
  - `--show-coverage`: Display detailed coverage statistics after analysis
  - `--help-modes`: Display comprehensive help about analysis modes

- **Mode tracking in history system**:
  - Added `analysis_mode` field to HistoricalScore records
  - Added `analysis_time_seconds` field to track analysis duration
  - Mode and time information displayed in history reports
  - Full backward compatibility with existing history files (defaults to "adaptive" mode)

- **Mode display in output formats**:
  - Analysis mode shown in all output formats (text, JSON, TSV)
  - Mode included in batch analysis TSV output as dedicated column
  - Mode displayed in report headers for text format
  - Mode included in JSON output for programmatic access

- **Comprehensive documentation**:
  - Created `docs/analysis-modes-guide.md` with 500+ lines of documentation
  - Added Analysis Modes section to README.md with quick start and mode comparison
  - Mode help integrated into CLI with `--help-modes` command
  - Examples for all modes and use cases

### Changed

- **Default analysis mode**: Fast mode is now the default (previously analyzed full document)
- **CLI argument parsing**: Extended with mode-specific configuration options
- **History format**: History v2.0 now includes mode and time metadata (backward compatible)
- **Output formatters**: All format functions now accept optional `mode` parameter
- **Analysis configuration**: Main analyzer now accepts `AnalysisConfig` with mode settings

### Technical Details

- **Backward Compatibility**: 100% maintained
  - Old code without mode arguments continues to work (defaults to fast mode)
  - Existing history files load correctly (missing mode fields use defaults)
  - All existing CLI flags and output formats work unchanged

- **Testing**: Comprehensive test coverage added
  - 11+ new tests for mode tracking in history system
  - All tests passing (72 total tests)
  - Tests cover serialization, deserialization, backward compatibility, and display

- **Performance**: Analysis time varies by mode
  - Fast mode: 2-5 seconds (most documents)
  - Adaptive mode: 5-15 seconds (automatically scaled)
  - Sampling mode: 10-30 seconds (configurable)
  - Full mode: 30-120+ seconds (depends on document size)

### Migration Guide

For users upgrading from previous versions:

**No breaking changes** - all existing commands work identically:

```bash
# Old command (still works - now uses fast mode)
python analyze_ai_patterns.py document.md

# Recommended upgrade for better accuracy
python analyze_ai_patterns.py document.md --mode adaptive

# For final review/maximum accuracy
python analyze_ai_patterns.py document.md --mode full
```

History files from previous versions load automatically with default mode values.

## [4.0.0] - 2024

### Changed

- Complete refactoring from monolithic 7,079-line file to modular architecture
- Package structure with 17+ modules, largest <1,100 lines each
- Separation of concerns: core, dimensions, scoring, history, utils, CLI
- Full backward compatibility maintained via package-level exports

### Added

- Modular dimension analyzers with base interface
- Dual-score calculation system
- History tracking with comprehensive metadata
- CLI argument parsing and output formatting modules

---

## Version Numbering

- **Major version** (X.0.0): Breaking changes
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes, backward compatible

---

[Unreleased]: https://github.com/your-org/ai-pattern-analyzer/compare/v4.0.0...HEAD
[4.0.0]: https://github.com/your-org/ai-pattern-analyzer/releases/tag/v4.0.0

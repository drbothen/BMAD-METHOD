# Story: Comprehensive Metric History Tracking

**Story ID:** BMAD-TW-DETECT-005
**Epic:** AI Pattern Detection Enhancement
**Priority:** HIGH
**Estimated Effort:** 2-3 hours
**Status:** Ready for Development
**Depends On:** BMAD-TW-DUAL-001 (Dual Scoring System), BMAD-TW-REFACTOR-001 (Modularization)

## Story Overview

As a **technical author optimizing AI-assisted content**, I want the score history to track ALL metrics (all 14 dimension scores + raw metric values) over time, so that I can understand exactly which changes had which impacts on which dimensions and validate that my optimization efforts are systematically improving the content.

## Business Value

**Problem:**
Current score history only tracks 2 values per run:

- Quality Score (aggregate)
- Detection Risk (aggregate)

This makes it impossible to answer critical questions:

- "Which dimension improved the most after fixing AI vocabulary?"
- "Why did Detection Risk increase even though Quality Score improved?"
- "Has my em-dash reduction actually improved formatting scores?"
- "Are my paragraph edits improving burstiness or making it worse?"
- "Which dimensions have plateaued vs. which are still improving?"

**Impact:**
Comprehensive metric tracking enables:

- **Root cause analysis** - See which specific changes affected which dimensions
- **Validation** - Confirm that targeted edits actually improved target dimensions
- **Trend detection** - Identify plateaus, regressions, or unexpected correlations
- **Optimization strategy** - Focus effort on dimensions showing most improvement potential
- **Audit trail** - Complete history of optimization journey for publishers/reviewers

**Success Metrics:**

- Users can answer "what changed?" questions without re-running analysis
- 100% of dimension trends visible in history output
- Export to CSV enables custom analysis in Excel/Python
- Historical reports show complete optimization journey
- Trend visualization shows at-a-glance progress across all dimensions

## User Acceptance Criteria

### AC1: Enhanced HistoricalScore Data Structure

**Given** the score history tracking system
**When** adding a new score to history
**Then** it should capture:

- [x] **Aggregate scores**: quality_score, detection_risk (existing)
- [x] **All 14 dimension scores**: GLTR, lexical diversity, AI detection ensemble, etc.
- [x] **All category scores**: Tier 1 (Advanced Detection), Tier 2 (Core Patterns), Tier 3 (Supporting Signals)
- [x] **Key raw metrics**:
  - AI vocabulary per 1k words
  - Sentence length StdDev (burstiness)
  - Em-dashes per page
  - Heading parallelism score
  - Paragraph CV
  - Section variance %
  - Blockquote per page
  - Generic link anchor ratio
  - And all other measurable metrics
- [x] **Metadata**: timestamp, total_words, notes
- [x] **Version**: history format version for future compatibility

**Enhanced HistoricalScore Structure:**

```python
@dataclass
class HistoricalScore:
    """Comprehensive historical score tracking"""
    # Metadata
    timestamp: str
    total_words: int
    notes: str = ""
    history_version: str = "2.0"  # For future compatibility

    # Aggregate scores (EXISTING)
    detection_risk: float
    quality_score: float
    detection_interpretation: str
    quality_interpretation: str

    # Category scores (NEW)
    tier1_score: float  # Advanced Detection (40 pts)
    tier2_score: float  # Core Patterns (35 pts)
    tier3_score: float  # Supporting Signals (25 pts)

    # All 14 dimension scores (NEW)
    dimensions: Dict[str, DimensionScore] = field(default_factory=dict)
    # Example: {
    #   'gltr_token_ranking': DimensionScore(score=8.5, max=12, percentage=70.8, raw_value=0.42),
    #   'lexical_diversity': DimensionScore(score=6.0, max=8, percentage=75.0, raw_value=0.72),
    #   ...
    # }

    # Key raw metrics for detailed trend analysis (NEW)
    raw_metrics: Dict[str, float] = field(default_factory=dict)
    # Example: {
    #   'ai_vocabulary_per_1k': 12.4,
    #   'sentence_stdev': 4.2,
    #   'em_dashes_per_page': 7.8,
    #   'heading_parallelism': 0.85,
    #   'paragraph_cv': 0.28,
    #   'section_variance_pct': 12.3,
    #   'mattr': 0.62,
    #   'rttr': 6.2,
    #   ...
    # }

@dataclass
class DimensionScore:
    """Individual dimension score for history tracking"""
    score: float  # Actual score (0-max)
    max_score: float  # Maximum possible
    percentage: float  # 0-100
    raw_value: Optional[float] = None  # Original metric value
```

### AC2: Backward Compatibility with v1.0 History

**Given** existing score history files with v1.0 format (only quality/detection scores)
**When** loading history
**Then** it should:

- [x] Detect v1.0 format (missing `history_version` field)
- [x] Load v1.0 scores with legacy data structure
- [x] Mark as v1.0 in memory for proper handling
- [x] Continue accepting new v2.0 scores
- [x] Save new scores in v2.0 format
- [x] Show trend analysis for available data (quality/detection only for v1.0)
- [x] Display notice: "Showing aggregate trends. Run analysis again to start tracking all 14 dimensions."

**Migration Strategy:**

```python
def load_score_history(self, file_path: str) -> ScoreHistory:
    """Load score history with backward compatibility"""
    # ... existing load code ...

    scores = []
    for score_data in data.get('scores', []):
        version = score_data.get('history_version', '1.0')

        if version == '1.0':
            # Legacy format - only quality/detection
            scores.append(HistoricalScore(
                timestamp=score_data['timestamp'],
                detection_risk=score_data['detection_risk'],
                quality_score=score_data['quality_score'],
                # ... v1.0 fields ...
                dimensions={},  # Empty for v1.0
                raw_metrics={},  # Empty for v1.0
                history_version='1.0'
            ))
        else:
            # v2.0 format - comprehensive
            scores.append(HistoricalScore(**score_data))

    return ScoreHistory(file_path=file_path, scores=scores)
```

### AC3: Dimension-Level Trend Analysis

**Given** a score history with 3+ entries
**When** analyzing trends
**Then** it should provide:

- [x] **Per-dimension trends**: IMPROVING (+X pts) / STABLE / DECLINING (-X pts)
- [x] **Category-level trends**: How each tier (1, 2, 3) is performing
- [x] **Aggregate trends**: Quality and Detection (existing)
- [x] **Plateau detection**: Identify dimensions showing <1pt change over last 3 runs
- [x] **High-impact dimensions**: Which dimensions changed most (top 5)
- [x] **Velocity**: Points gained/lost per iteration for each dimension

**Example Trend Output:**

```
COMPREHENSIVE TREND ANALYSIS (5 iterations tracked)
════════════════════════════════════════════════════════════════════════════════

AGGREGATE SCORES:
  Quality:   76.2 → 87.4  (+11.2 pts)  IMPROVING ↑
  Detection: 45.3 → 31.8  (-13.5 pts)  IMPROVING ↓

CATEGORY TRENDS:
  Tier 1 (Advanced Detection):   28.5 → 35.2  (+6.7 pts / 40 max)  IMPROVING ↑
  Tier 2 (Core Patterns):         24.1 → 29.8  (+5.7 pts / 35 max)  IMPROVING ↑
  Tier 3 (Supporting Signals):    19.6 → 20.4  (+0.8 pts / 25 max)  STABLE →

TOP 5 DIMENSION IMPROVEMENTS:
  1. AI Vocabulary (Perplexity):     3.2 → 9.5   (+6.3 pts)  EXCELLENT improvement
  2. Sentence Variation (Burstiness): 5.1 → 9.8   (+4.7 pts)  STRONG improvement
  3. Em-Dash Formatting:             2.0 → 6.5   (+4.5 pts)  STRONG improvement
  4. Heading Parallelism:            4.5 → 7.2   (+2.7 pts)  GOOD improvement
  5. Paragraph Length CV:            6.0 → 8.5   (+2.5 pts)  GOOD improvement

PLATEAUED DIMENSIONS (< 1pt change in last 3 runs):
  - Lexical Diversity (MATTR):       7.2 → 7.4   (+0.2 pts)  PLATEAUED
  - Subsection Asymmetry:            5.8 → 5.9   (+0.1 pts)  PLATEAUED

DECLINING DIMENSIONS (needs attention):
  - None detected ✓

VELOCITY (pts per iteration):
  Quality:   +2.8 pts/iteration (accelerating)
  Detection: -3.4 pts/iteration (accelerating improvement)
```

### AC4: Raw Metric Trend Visualization

**Given** tracked raw metrics over time
**When** displaying trends
**Then** it should show:

- [x] **Metric progression**: Show actual values across iterations
- [x] **Target indicators**: Show target values vs. current
- [x] **Sparkline visualization**: ASCII art trend charts
- [x] **Direction indicators**: ↑ ↓ → for quick scanning
- [x] **Threshold crossings**: Highlight when metrics cross quality thresholds

**Example Raw Metric Trends:**

```
RAW METRIC TRENDS (5 iterations)
════════════════════════════════════════════════════════════════════════════════

AI Vocabulary per 1k:
  Iteration 1:  18.7 words ████████████████████ ✗ POOR
  Iteration 2:  14.2 words ███████████████ ⚠ FAIR
  Iteration 3:   8.9 words ██████████ ⚠ FAIR
  Iteration 4:   4.7 words ██████ ✓ GOOD
  Iteration 5:   2.1 words ███ ✓ EXCELLENT

  Progress: 18.7 → 2.1  (-16.6 words, -89% reduction)
  Target:  ≤2.0 per 1k  [NEARLY MET - 0.1 from target]
  Trend:   ↓↓↓↓ (consistent improvement)

Sentence StdDev (Burstiness):
  Iteration 1:   3.2  ███ ✗ POOR (low variation)
  Iteration 2:   5.8  ██████ ⚠ FAIR
  Iteration 3:   8.1  ████████ ✓ GOOD
  Iteration 4:  11.4  ███████████ ✓ EXCELLENT
  Iteration 5:  12.7  ████████████ ✓ EXCELLENT

  Progress: 3.2 → 12.7  (+9.5, +297% increase)
  Target:  ≥10.0  [EXCEEDED ✓]
  Trend:   ↑↑↑↑ (consistent improvement)

Em-Dashes per Page:
  Iteration 1:  12.8 ████████████████████ ✗ EXCESSIVE
  Iteration 2:   9.3 ███████████████ ✗ EXCESSIVE
  Iteration 3:   5.7 ██████████ ⚠ HIGH
  Iteration 4:   3.1 █████ ✓ ACCEPTABLE
  Iteration 5:   1.8 ███ ✓ EXCELLENT

  Progress: 12.8 → 1.8  (-11.0, -86% reduction)
  Target:  ≤2.0 per page  [MET ✓]
  Trend:   ↓↓↓↓ (consistent improvement)
```

### AC5: Iteration Comparison Report

**Given** a score history with multiple iterations
**When** user requests comparison
**Then** it should show:

- [x] Side-by-side comparison of any two iterations
- [x] Highlight dimensions that changed significantly (±2pts)
- [x] Show which actions were effective vs. ineffective
- [x] Calculate ROI: points gained per effort invested

**Command:**

```bash
# Compare first and last iterations
python analyze_ai_patterns.py chapter-03.md --compare-history first,last

# Compare specific iterations
python analyze_ai_patterns.py chapter-03.md --compare-history 2,5

# Show full history progression
python analyze_ai_patterns.py chapter-03.md --show-history-full
```

**Example Comparison Output:**

```
ITERATION COMPARISON: Iteration 1 vs. Iteration 5
════════════════════════════════════════════════════════════════════════════════

                               Iteration 1    Iteration 5    Change      Impact
                               (2025-01-15)   (2025-01-18)
────────────────────────────────────────────────────────────────────────────────
AGGREGATE SCORES:
  Quality Score                    76.2           87.4        +11.2    EXCELLENT
  Detection Risk                   45.3           31.8        -13.5    EXCELLENT

TIER 1 - ADVANCED DETECTION (40 pts):
  GLTR Token Ranking                8.5           10.2         +1.7    GOOD
  Lexical Diversity (MATTR)         6.0            7.4         +1.4    GOOD
  AI Detection Ensemble             7.2            9.8         +2.6    EXCELLENT
  Stylometric Markers               4.8            5.8         +1.0    FAIR
  Syntactic Complexity              2.0            2.0          0.0    NO CHANGE

TIER 2 - CORE PATTERNS (35 pts):
  Perplexity (AI Vocab)             3.2            9.5         +6.3    EXCELLENT ⭐
  Burstiness (Sent. Var)            5.1            9.8         +4.7    EXCELLENT ⭐
  Transitions                       4.8            6.2         +1.4    GOOD
  Voice Consistency                 5.5            7.1         +1.6    GOOD
  Domain Knowledge                  5.5            5.2         -0.3    SLIGHT DECLINE

TIER 3 - SUPPORTING SIGNALS (25 pts):
  Em-Dash Formatting                2.0            6.5         +4.5    EXCELLENT ⭐
  Heading Parallelism               4.5            7.2         +2.7    EXCELLENT
  Bold/Italic Usage                 6.2            6.7         +0.5    SLIGHT
  Sentiment Variance                3.4            3.8         +0.4    SLIGHT
  Readability                       5.5            5.2         -0.3    SLIGHT DECLINE

────────────────────────────────────────────────────────────────────────────────
KEY INSIGHTS:

✅ TOP 3 IMPROVEMENTS (⭐):
  1. Perplexity (+6.3 pts) - AI vocabulary reduction was HIGHLY effective
  2. Burstiness (+4.7 pts) - Sentence variation edits worked excellently
  3. Em-Dash Formatting (+4.5 pts) - Formatting cleanup had major impact

⚠ MINOR DECLINES:
  1. Domain Knowledge (-0.3 pts) - Some technical terms replaced during vocab cleanup
  2. Readability (-0.3 pts) - Increased sentence variation slightly reduced Flesch score

📊 OVERALL ASSESSMENT:
  - 12 dimensions improved
  - 2 dimensions declined slightly
  - 1 dimension unchanged
  - Net improvement: +11.2 quality pts, -13.5 detection risk pts
  - Effort investment: MODERATE (3 editing passes)
  - ROI: EXCELLENT (3.7 pts per editing pass)
```

### AC6: CSV Export for Custom Analysis

**Given** a score history file
**When** user requests CSV export
**Then** it should generate:

- [x] One row per iteration
- [x] Columns for all aggregate scores, category scores, dimension scores, raw metrics
- [x] Timestamp and notes columns
- [x] Headers that are Excel/Pandas friendly
- [x] Support for import into spreadsheet tools for custom charts

**Command:**

```bash
# Export to CSV
python analyze_ai_patterns.py chapter-03.md --export-history csv

# Specify output file
python analyze_ai_patterns.py chapter-03.md --export-history csv --output history.csv
```

**Example CSV Output:**

```csv
timestamp,iteration,total_words,notes,quality_score,detection_risk,tier1_score,tier2_score,tier3_score,gltr_score,lexical_diversity_score,ai_detection_score,stylometric_score,syntactic_score,perplexity_score,burstiness_score,transitions_score,voice_score,domain_score,emdash_score,heading_parallelism_score,bold_italic_score,sentiment_score,readability_score,ai_vocab_per_1k,sentence_stdev,em_dashes_per_page,heading_parallelism_raw,paragraph_cv,section_variance_pct,mattr,rttr,blockquote_per_page,generic_link_ratio
2025-01-15T10:30:00,1,3847,"Initial baseline",76.2,45.3,28.5,24.1,19.6,8.5,6.0,7.2,4.8,2.0,3.2,5.1,4.8,5.5,5.5,2.0,4.5,6.2,3.4,5.5,18.7,3.2,12.8,0.85,0.28,12.3,0.62,6.2,4.5,0.6
2025-01-16T14:20:00,2,3852,"Fixed AI vocabulary",78.9,42.1,29.8,26.3,20.1,8.9,6.4,7.8,5.1,2.0,6.8,5.4,5.2,5.8,5.4,2.3,4.8,6.3,3.5,5.4,14.2,3.8,11.2,0.82,0.31,14.1,0.65,6.5,4.2,0.58
2025-01-17T09:15:00,3,3865,"Varied sentences, reduced em-dashes",82.4,38.7,31.2,28.1,20.8,9.2,6.8,8.5,5.3,2.0,7.9,7.8,5.6,6.2,5.3,4.1,5.5,6.5,3.6,5.3,8.9,8.1,5.7,0.78,0.38,18.5,0.68,6.8,3.1,0.52
2025-01-18T11:45:00,4,3871,"Fixed heading parallelism",85.1,34.2,33.5,29.4,21.2,9.8,7.1,9.1,5.6,2.0,8.9,9.1,5.9,6.7,5.2,5.8,6.8,6.6,3.7,5.2,4.7,11.4,3.1,0.72,0.42,23.8,0.71,7.1,2.4,0.45
2025-01-18T16:30:00,5,3878,"Final polish",87.4,31.8,35.2,29.8,20.4,10.2,7.4,9.8,5.8,2.0,9.5,9.8,6.2,7.1,5.2,6.5,7.2,6.7,3.8,5.2,2.1,12.7,1.8,0.68,0.45,26.4,0.74,7.3,1.9,0.41
```

This CSV can be:

- Imported into Excel for custom charts
- Loaded into Pandas for Python analysis
- Visualized with R/ggplot2
- Shared with collaborators/reviewers
- Used for statistical analysis across multiple documents

### AC7: Sparkline Visualization in Terminal

**Given** a score history with 5+ iterations
**When** displaying trends
**Then** it should include:

- [x] ASCII sparkline charts showing score progression
- [x] Inline trend indicators (↑↓→) for quick scanning
- [x] Color coding (green=improving, red=declining, yellow=stable)
- [x] Compact format suitable for terminal output

**Example Sparkline Output:**

```
SCORE TRENDS (Sparkline View - Last 10 iterations)
════════════════════════════════════════════════════════════════════════════════

Quality Score:       ▂▃▅▆▇███ 76→87 (+11 pts) ↑ IMPROVING
Detection Risk:      ███▇▆▅▃▂ 45→32 (-13 pts) ↓ IMPROVING

Perplexity:          ▁▂▄▆▇██ 3.2→9.5 (+6.3) ↑ EXCELLENT
Burstiness:          ▂▃▅▇██ 5.1→9.8 (+4.7) ↑ EXCELLENT
Em-Dash Format:      ▁▂▄▇██ 2.0→6.5 (+4.5) ↑ EXCELLENT
Heading Parallel:    ▃▄▅▆▇█ 4.5→7.2 (+2.7) ↑ GOOD
Lexical Diversity:   ▅▆▆▇▇█ 6.0→7.4 (+1.4) → STABLE
Stylometric:         ▄▅▅▆▆█ 4.8→5.8 (+1.0) → STABLE

Legend: ▁▂▃▄▅▆▇█ (lowest to highest)
```

### AC8: Historical Report Generation

**Given** a complete optimization journey (multiple iterations)
**When** user requests full history report
**Then** it should generate:

- [x] Complete iteration-by-iteration summary
- [x] Notes for each iteration (what was changed)
- [x] Before/after comparison
- [x] Lessons learned (which actions had most impact)
- [x] Final readiness assessment

**Command:**

```bash
# Generate comprehensive history report
python analyze_ai_patterns.py chapter-03.md --show-history-full

# Generate HTML history report (future enhancement)
python analyze_ai_patterns.py chapter-03.md --export-history html
```

**Example History Report:**

```
COMPLETE OPTIMIZATION JOURNEY
════════════════════════════════════════════════════════════════════════════════
Document: chapter-03.md
Iterations: 5 (2025-01-15 to 2025-01-18)
Total Effort: MODERATE (3 editing passes)
════════════════════════════════════════════════════════════════════════════════

ITERATION 1: Baseline Analysis
────────────────────────────────────────────────────────────────────────────────
Timestamp:     2025-01-15 10:30:00
Quality:       76.2 / 100  (GOOD - Moderate humanization needed)
Detection:     45.3 / 100  (MEDIUM-HIGH - Likely flagged)
Notes:         Initial baseline
Key Issues:    - AI vocabulary: 18.7 per 1k (EXCESSIVE)
               - Em-dashes: 12.8 per page (EXCESSIVE)
               - Sentence StdDev: 3.2 (LOW - uniform)
               - Heading parallelism: 0.85 (HIGH - mechanical)

ITERATION 2: AI Vocabulary Reduction
────────────────────────────────────────────────────────────────────────────────
Timestamp:     2025-01-16 14:20:00
Quality:       78.9 / 100  (+2.7 pts)  IMPROVING ↑
Detection:     42.1 / 100  (-3.2 pts)  IMPROVING ↓
Notes:         Fixed AI vocabulary (replaced 47 instances)
Changes:       - AI vocabulary: 18.7 → 14.2 (-24% reduction)
               - Perplexity score: 3.2 → 6.8 (+3.6 pts)
Effectiveness: GOOD - Perplexity improved significantly
Next Focus:    Sentence variation and em-dash reduction

ITERATION 3: Structural Improvements
────────────────────────────────────────────────────────────────────────────────
Timestamp:     2025-01-17 09:15:00
Quality:       82.4 / 100  (+3.5 pts)  IMPROVING ↑
Detection:     38.7 / 100  (-3.4 pts)  IMPROVING ↓
Notes:         Varied sentence lengths, reduced em-dashes
Changes:       - Sentence StdDev: 3.8 → 8.1 (+113% increase)
               - Em-dashes: 11.2 → 5.7 (-49% reduction)
               - Burstiness score: 5.4 → 7.8 (+2.4 pts)
               - Em-dash score: 2.3 → 4.1 (+1.8 pts)
Effectiveness: EXCELLENT - Major improvements in burstiness
Next Focus:    Heading parallelism, final polish

ITERATION 4: Heading Restructure
────────────────────────────────────────────────────────────────────────────────
Timestamp:     2025-01-18 11:45:00
Quality:       85.1 / 100  (+2.7 pts)  IMPROVING ↑
Detection:     34.2 / 100  (-4.5 pts)  IMPROVING ↓
Notes:         Fixed heading parallelism, broke mechanical patterns
Changes:       - Heading parallelism: 0.78 → 0.72 (-8% reduction)
               - Heading score: 5.5 → 6.8 (+1.3 pts)
               - Section variance: 18.5% → 23.8% (+29% increase)
Effectiveness: GOOD - Improved structure scores
Next Focus:    Final vocabulary cleanup, target achievement

ITERATION 5: Final Polish
────────────────────────────────────────────────────────────────────────────────
Timestamp:     2025-01-18 16:30:00
Quality:       87.4 / 100  (+2.3 pts)  TARGET MET ✓
Detection:     31.8 / 100  (-2.4 pts)  NEARLY MET (target: 30)
Notes:         Final polish - vocabulary cleanup, paragraph variation
Changes:       - AI vocabulary: 4.7 → 2.1 (-55% reduction, EXCELLENT)
               - Paragraph CV: 0.42 → 0.45 (+7% increase)
               - MATTR: 0.71 → 0.74 (+4% increase)
Status:        PUBLICATION READY ✓
               Quality: EXCEEDS target (87.4 ≥ 85)
               Detection: 1.8 pts from target (acceptable)

════════════════════════════════════════════════════════════════════════════════
FINAL ASSESSMENT
════════════════════════════════════════════════════════════════════════════════

Overall Progress:
  Quality:       76.2 → 87.4  (+11.2 pts, +15% improvement)
  Detection:     45.3 → 31.8  (-13.5 pts, -30% risk reduction)

Most Effective Actions:
  1. AI Vocabulary Reduction (+6.3 pts quality, -8 pts detection risk)
  2. Sentence Variation (+4.7 pts quality, -5 pts detection risk)
  3. Em-Dash Reduction (+4.5 pts quality, -6 pts detection risk)

Lessons Learned:
  ✅ Targeted vocabulary replacement had highest ROI
  ✅ Structural changes (sentences, paragraphs) compounded benefits
  ✅ Formatting cleanup (em-dashes, headings) easier than expected
  ⚠ Some technical terminology lost during vocab cleanup (-0.3 domain score)

Publication Readiness: READY ✓
  Quality target (≥85):     MET (87.4)
  Detection target (≤30):   NEARLY MET (31.8, acceptable)
  No critical issues remaining
  Content ready for technical review

Total Time Investment: 4 days (intermittent editing)
Total Effort Level: MODERATE
ROI: EXCELLENT (2.8 quality pts per editing pass)
```

### AC9: Performance Considerations

**Given** large history files (50+ iterations)
**When** loading and processing history
**Then** it should:

- [x] Load history in <500ms for typical files (10-20 iterations)
- [x] Handle up to 100 iterations without performance degradation
- [x] Use lazy loading for trend calculations (only when requested)
- [x] Compress JSON history files (optional gzip)
- [x] Implement pagination for very large histories (show last 10 by default)

### AC10: Integration with Iterative Optimization Workflow

**Given** the iterative-humanization-optimization.md task workflow
**When** running iterative optimization
**Then** the history tracking should:

- [x] Automatically add notes from each iteration (e.g., "Iteration 3: Applied path-to-target actions for AI vocab")
- [x] Detect plateaus automatically (terminate if <1pt improvement over 3 iterations)
- [x] Show mini-trend after each iteration (current vs. previous)
- [x] Update path-to-target based on what's working (de-prioritize plateaued dimensions)
- [x] Provide historical context in recommendations ("AI vocab improved +6pts, continue this approach")

## Technical Implementation Details

### Code Location

**IMPORTANT:** This implementation assumes the modularized codebase from BMAD-TW-REFACTOR-001.

**Primary Files:**

- `/expansion-packs/bmad-technical-writing/data/tools/ai_pattern_analyzer/history/` - History tracking package
  - `tracker.py` - `HistoricalScore`, `ScoreHistory`, `DimensionScore` classes
  - `export.py` - CSV/JSON export functionality
  - `trends.py` - Trend analysis and plateau detection (NEW)
- `/expansion-packs/bmad-technical-writing/data/tools/ai_pattern_analyzer/scoring/dual_score.py` - Dual scoring system
- `/expansion-packs/bmad-technical-writing/data/tools/ai_pattern_analyzer/core/results.py` - AnalysisResults dataclass
- `/expansion-packs/bmad-technical-writing/data/tools/analyze_ai_patterns.py` - CLI entry point

### Enhanced Data Structures

Create in `ai_pattern_analyzer/history/tracker.py`:

```python
# ai_pattern_analyzer/history/tracker.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from pathlib import Path
import json

@dataclass
class DimensionScore:
    """Individual dimension score for history tracking"""
    score: float  # Actual score (0-max)
    max_score: float  # Maximum possible
    percentage: float  # 0-100
    raw_value: Optional[float] = None  # Original metric value (e.g., 0.62 for MATTR)
    interpretation: str = ""  # 'EXCELLENT', 'GOOD', 'FAIR', 'POOR'

@dataclass
class HistoricalScore:
    """Comprehensive historical score tracking (v2.0)"""
    # Metadata
    timestamp: str
    total_words: int
    notes: str = ""
    history_version: str = "2.0"

    # Aggregate scores
    detection_risk: float
    quality_score: float
    detection_interpretation: str
    quality_interpretation: str

    # Category scores
    tier1_score: float = 0.0  # Advanced Detection (max 40)
    tier2_score: float = 0.0  # Core Patterns (max 35)
    tier3_score: float = 0.0  # Supporting Signals (max 25)

    # All 14 dimension scores
    dimensions: Dict[str, DimensionScore] = field(default_factory=dict)

    # Key raw metrics for trend analysis
    raw_metrics: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization"""
        return {
            'timestamp': self.timestamp,
            'total_words': self.total_words,
            'notes': self.notes,
            'history_version': self.history_version,
            'detection_risk': self.detection_risk,
            'quality_score': self.quality_score,
            'detection_interpretation': self.detection_interpretation,
            'quality_interpretation': self.quality_interpretation,
            'tier1_score': self.tier1_score,
            'tier2_score': self.tier2_score,
            'tier3_score': self.tier3_score,
            'dimensions': {
                name: {
                    'score': dim.score,
                    'max_score': dim.max_score,
                    'percentage': dim.percentage,
                    'raw_value': dim.raw_value,
                    'interpretation': dim.interpretation
                }
                for name, dim in self.dimensions.items()
            },
            'raw_metrics': self.raw_metrics
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'HistoricalScore':
        """Reconstruct from dict (JSON deserialization)"""
        dimensions = {}
        for name, dim_data in data.get('dimensions', {}).items():
            dimensions[name] = DimensionScore(**dim_data)

        return cls(
            timestamp=data['timestamp'],
            total_words=data['total_words'],
            notes=data.get('notes', ''),
            history_version=data.get('history_version', '1.0'),
            detection_risk=data['detection_risk'],
            quality_score=data['quality_score'],
            detection_interpretation=data['detection_interpretation'],
            quality_interpretation=data['quality_interpretation'],
            tier1_score=data.get('tier1_score', 0.0),
            tier2_score=data.get('tier2_score', 0.0),
            tier3_score=data.get('tier3_score', 0.0),
            dimensions=dimensions,
            raw_metrics=data.get('raw_metrics', {})
        )

@dataclass
class ScoreHistory:
    """Score history for a document"""
    file_path: str
    scores: List[HistoricalScore] = field(default_factory=list)

    def add_score(self, score: DualScore, results: AnalysisResults, notes: str = ""):
        """Add comprehensive score to history (v2.0)"""
        # Extract all dimension scores from DualScore
        dimensions = {}
        for category in score.categories:
            for dimension in category.dimensions:
                dimensions[dimension.name] = DimensionScore(
                    score=dimension.score,
                    max_score=dimension.max_score,
                    percentage=dimension.percentage,
                    raw_value=dimension.raw_value,
                    interpretation=dimension.impact
                )

        # Calculate tier scores
        tier1 = sum(d.score for d in score.categories[0].dimensions) if len(score.categories) > 0 else 0
        tier2 = sum(d.score for d in score.categories[1].dimensions) if len(score.categories) > 1 else 0
        tier3 = sum(d.score for d in score.categories[2].dimensions) if len(score.categories) > 2 else 0

        # Extract key raw metrics from AnalysisResults
        raw_metrics = {
            'ai_vocabulary_per_1k': results.ai_vocabulary_per_1k,
            'sentence_stdev': results.sentence_stdev,
            'em_dashes_per_page': results.em_dashes_per_page,
            'heading_parallelism': results.heading_parallelism_score,
            'paragraph_cv': getattr(results, 'paragraph_cv', 0.0),
            'section_variance_pct': getattr(results, 'section_variance_pct', 0.0),
            # Add more metrics as they become available from Phase 1-3
        }

        self.scores.append(HistoricalScore(
            timestamp=score.timestamp,
            detection_risk=score.detection_risk,
            quality_score=score.quality_score,
            detection_interpretation=score.detection_interpretation,
            quality_interpretation=score.quality_interpretation,
            total_words=score.total_words,
            notes=notes,
            tier1_score=tier1,
            tier2_score=tier2,
            tier3_score=tier3,
            dimensions=dimensions,
            raw_metrics=raw_metrics
        ))

    def get_dimension_trend(self, dimension_name: str) -> Dict:
        """Get trend for specific dimension"""
        if len(self.scores) < 2:
            return {'trend': 'N/A', 'change': 0.0}

        # Only analyze v2.0 scores
        v2_scores = [s for s in self.scores if s.history_version == '2.0']
        if len(v2_scores) < 2:
            return {'trend': 'N/A', 'change': 0.0}

        # Get dimension from first and last v2.0 scores
        first_dim = v2_scores[0].dimensions.get(dimension_name)
        last_dim = v2_scores[-1].dimensions.get(dimension_name)

        if not first_dim or not last_dim:
            return {'trend': 'N/A', 'change': 0.0}

        change = last_dim.score - first_dim.score

        return {
            'trend': 'IMPROVING' if change > 1 else 'DECLINING' if change < -1 else 'STABLE',
            'change': round(change, 1),
            'first_score': first_dim.score,
            'last_score': last_dim.score,
            'first_raw': first_dim.raw_value,
            'last_raw': last_dim.raw_value
        }

    def get_plateaued_dimensions(self, lookback: int = 3, threshold: float = 1.0) -> List[str]:
        """Identify dimensions that have plateaued (< threshold change in last N iterations)"""
        if len(self.scores) < lookback:
            return []

        v2_scores = [s for s in self.scores if s.history_version == '2.0']
        if len(v2_scores) < lookback:
            return []

        recent_scores = v2_scores[-lookback:]
        plateaued = []

        # Get all dimension names
        if not recent_scores[0].dimensions:
            return []

        for dim_name in recent_scores[0].dimensions.keys():
            # Check if dimension exists in all recent scores
            if not all(dim_name in score.dimensions for score in recent_scores):
                continue

            # Calculate max change across lookback window
            scores = [score.dimensions[dim_name].score for score in recent_scores]
            max_change = max(scores) - min(scores)

            if max_change < threshold:
                plateaued.append(dim_name)

        return plateaued

    def export_to_csv(self, output_path: str):
        """Export history to CSV for analysis in Excel/Pandas"""
        import csv

        if not self.scores:
            return

        # Build header
        header = [
            'timestamp', 'iteration', 'total_words', 'notes',
            'quality_score', 'detection_risk',
            'tier1_score', 'tier2_score', 'tier3_score'
        ]

        # Add dimension scores
        if self.scores[0].dimensions:
            dim_names = sorted(self.scores[0].dimensions.keys())
            header.extend([f"{name}_score" for name in dim_names])

        # Add raw metrics
        if self.scores[0].raw_metrics:
            metric_names = sorted(self.scores[0].raw_metrics.keys())
            header.extend(metric_names)

        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()

            for i, score in enumerate(self.scores, start=1):
                row = {
                    'timestamp': score.timestamp,
                    'iteration': i,
                    'total_words': score.total_words,
                    'notes': score.notes,
                    'quality_score': score.quality_score,
                    'detection_risk': score.detection_risk,
                    'tier1_score': score.tier1_score,
                    'tier2_score': score.tier2_score,
                    'tier3_score': score.tier3_score
                }

                # Add dimension scores
                for name, dim in score.dimensions.items():
                    row[f"{name}_score"] = dim.score

                # Add raw metrics
                for name, value in score.raw_metrics.items():
                    row[name] = value

                writer.writerow(row)
```

### Command-Line Interface

Update `ai_pattern_analyzer/cli/args.py` to add history-related arguments:

```python
# ai_pattern_analyzer/cli/args.py

def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze AI patterns with comprehensive history tracking")

    # ... existing arguments ...

    # History tracking (enhanced)
    parser.add_argument('--show-history', action='store_true',
                       help='Show aggregate score trends (quality/detection)')
    parser.add_argument('--show-history-full', action='store_true',
                       help='Show complete optimization journey with all iterations')
    parser.add_argument('--show-dimension-trends', action='store_true',
                       help='Show trends for all 14 dimensions')
    parser.add_argument('--compare-history', type=str,
                       help='Compare two iterations (e.g., "first,last" or "2,5")')
    parser.add_argument('--export-history', type=str, choices=['csv', 'json'],
                       help='Export history to CSV or JSON format')
    parser.add_argument('--history-notes', type=str, default="",
                       help='Add notes for this iteration (e.g., "Fixed AI vocabulary")')

    return parser.parse_args()
```

### Integration Points

Update main CLI entry point to use modular history tracking:

```python
# analyze_ai_patterns.py

from ai_pattern_analyzer.core.analyzer import AIPatternAnalyzer
from ai_pattern_analyzer.scoring.dual_score import calculate_dual_score
from ai_pattern_analyzer.history.tracker import load_score_history, save_score_history
from ai_pattern_analyzer.history.trends import (
    generate_full_history_report,
    generate_dimension_trend_report,
    generate_comparison_report
)
from ai_pattern_analyzer.cli.args import parse_arguments

def main():
    args = parse_arguments()

    # Run analysis
    analyzer = AIPatternAnalyzer(args.file)
    results = analyzer.analyze()

    if args.show_scores:
        # Calculate dual score
        dual_score = calculate_dual_score(results)

        # Load history
        history = load_score_history(args.file)

    # Add current score with ALL metrics (v2.0)
    history.add_score(dual_score, results, notes=args.history_notes)

    # Save updated history
    analyzer.save_score_history(history)

    # Display based on user request
    if args.show_history_full:
        print(generate_full_history_report(history))
    elif args.show_dimension_trends:
        print(generate_dimension_trend_report(history))
    elif args.compare_history:
        indices = parse_comparison_indices(args.compare_history, len(history.scores))
        print(generate_comparison_report(history, indices[0], indices[1]))
    else:
        # Standard output with aggregate trends
        print(format_dual_score_report(dual_score, history, args.format))

# Export if requested
if args.export_history:
    if args.export_history == 'csv':
        output_path = args.output or f"{Path(args.file).stem}_history.csv"
        history.export_to_csv(output_path)
        print(f"History exported to: {output_path}")
```

## Testing Strategy

**Unit Tests:**

```python
def test_comprehensive_history_tracking():
    """Test that all dimension scores are captured"""
    analyzer = AIPatternAnalyzer("test.md")
    dual_score = create_test_dual_score()  # Mock dual score with all dimensions
    results = create_test_results()  # Mock analysis results

    history = ScoreHistory(file_path="test.md")
    history.add_score(dual_score, results, notes="Test iteration")

    assert len(history.scores) == 1
    assert history.scores[0].history_version == "2.0"
    assert len(history.scores[0].dimensions) == 14  # All 14 dimensions
    assert 'ai_vocabulary_per_1k' in history.scores[0].raw_metrics
    assert history.scores[0].tier1_score > 0

def test_backward_compatibility():
    """Test that v1.0 history files can be loaded"""
    # Create v1.0 format history
    v1_data = {
        'file_path': 'test.md',
        'scores': [{
            'timestamp': '2025-01-15T10:00:00',
            'detection_risk': 45.3,
            'quality_score': 76.2,
            'detection_interpretation': 'MEDIUM-HIGH',
            'quality_interpretation': 'GOOD',
            'total_words': 3847,
            'notes': 'Legacy format'
            # No history_version, dimensions, or raw_metrics
        }]
    }

    # Save as JSON
    with open('test_history.json', 'w') as f:
        json.dump(v1_data, f)

    # Load and verify
    analyzer = AIPatternAnalyzer("test.md")
    history = analyzer.load_score_history("test.md")

    assert len(history.scores) == 1
    assert history.scores[0].history_version == '1.0'
    assert len(history.scores[0].dimensions) == 0  # No dimensions in v1.0

def test_dimension_trend_analysis():
    """Test dimension-level trend calculation"""
    history = create_test_history_with_multiple_iterations()

    trend = history.get_dimension_trend('perplexity')

    assert trend['trend'] == 'IMPROVING'
    assert trend['change'] > 5.0  # Significant improvement
    assert trend['last_score'] > trend['first_score']

def test_plateau_detection():
    """Test plateau detection for dimensions"""
    history = create_history_with_plateaued_dimensions()

    plateaued = history.get_plateaued_dimensions(lookback=3, threshold=1.0)

    assert 'lexical_diversity' in plateaued  # This dimension plateaued
    assert 'perplexity' not in plateaued  # This dimension still improving

def test_csv_export():
    """Test CSV export functionality"""
    history = create_comprehensive_test_history()
    history.export_to_csv('test_export.csv')

    # Read back and verify
    import pandas as pd
    df = pd.read_csv('test_export.csv')

    assert len(df) == len(history.scores)
    assert 'quality_score' in df.columns
    assert 'perplexity_score' in df.columns
    assert 'ai_vocabulary_per_1k' in df.columns
```

## Definition of Done

- [ ] HistoricalScore enhanced to v2.0 format with all dimensions and raw metrics
- [ ] Backward compatibility with v1.0 history files working
- [ ] Dimension-level trend analysis implemented
- [ ] Category-level trend analysis implemented
- [ ] Plateau detection working
- [ ] Iteration comparison report implemented
- [ ] CSV export functionality working
- [ ] Sparkline visualization working (ASCII charts)
- [ ] Full history report generation working
- [ ] Integration with iterative optimization workflow
- [ ] Command-line flags (`--show-history-full`, `--compare-history`, etc.) working
- [ ] Performance acceptable (<500ms for 20 iteration history)
- [ ] Unit tests passing (12+ test cases)
- [ ] Integration tests with real optimization journeys
- [ ] Documentation updated (README, help text)
- [ ] Example CSV export validated in Excel/Pandas

## Success Metrics (Post-Implementation)

**Measure after 2 weeks:**

- Users can answer "what changed?" questions: 100% success rate
- CSV exports used for custom analysis: >50% of users
- Dimension-level insights inform optimization strategy: 80% report this as valuable
- Historical reports used for publisher submissions: >30% of book authors
- Plateau detection saves wasted optimization effort: Average 1-2 iterations saved

**User Feedback Targets:**

- "Now I understand which changes actually worked" - >90% agreement
- "Historical tracking proves systematic improvement to reviewers" - >85% find valuable
- "Dimension trends help me focus effort" - >80% find useful

## Dependencies and Prerequisites

**Before starting:**

- [x] Dual scoring system functional (BMAD-TW-DUAL-001)
- [x] Current v1.0 history tracking working

**New dependencies:**

- None (uses Python standard library)

**Optional dependencies:**

- pandas (for easier CSV analysis in Python)
- matplotlib (for future visualization enhancements)

## Related Stories

- **Depends On:** BMAD-TW-DUAL-001 (Dual Scoring System) ✓ Completed
- **Enhances:** BMAD-TW-DETECT-001, 002, 003 (Phase 1-3 dimensions will be tracked)
- **Enables:** Future visualization stories (charts, graphs, dashboards)
- **Complements:** BMAD-TW-DETECT-004 (Evidence Extraction)

## Future Enhancements

Once comprehensive history tracking is in place:

- **HTML reports** with interactive charts (Chart.js, D3.js)
- **Automated insights** - "Your perplexity improvements are slowing, try focusing on burstiness"
- **Multi-document comparisons** - Compare optimization paths across multiple chapters
- **Benchmark database** - Compare your scores against typical book chapter scores
- **Regression detection** - Alert when dimensions decline unexpectedly
- **Correlation analysis** - "When you improve burstiness, detection risk typically drops by 3pts"
- **Predictive modeling** - "Based on current trends, you'll hit targets in 2 more iterations"

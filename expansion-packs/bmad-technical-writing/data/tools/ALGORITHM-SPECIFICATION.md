# AI Pattern Analysis - Complete Algorithm Specification

**Version**: 3.0.0
**Last Updated**: 2025-01-02
**File**: `analyze_ai_patterns.py`

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Complete Metric Inventory](#complete-metric-inventory)
3. [Dual Scoring Algorithm](#dual-scoring-algorithm)
4. [Detection Risk Calculation](#detection-risk-calculation)
5. [Dimension Scoring Methods](#dimension-scoring-methods)
6. [Orphaned Metrics Analysis](#orphaned-metrics-analysis)
7. [Data Flow Architecture](#data-flow-architecture)

---

## Executive Summary

### System Purpose

Quantifies how "AI-like" text appears using 80+ metrics across 14 scored dimensions, producing two complementary scores:

- **Quality Score**: 0-144 points (normalized to 0-100), higher = more human-like
- **Detection Risk**: 0-100+ points, lower = less detectable

### Scoring Tiers

- **Tier 1: Advanced Detection** - 60/144 points (41.7%)
- **Tier 2: Core Patterns** - 59/144 points (41.0%)
- **Tier 3: Supporting Signals** - 25/144 points (17.4%)
- **Total Maximum**: 144 quality points

### Key Innovation

Dual scores measure both "human-likeness" (Quality) and "AI-detectability" (Detection Risk) using the same underlying metrics but different weighting strategies.

---

## Complete Metric Inventory

### Basic Document Metrics (9 metrics)

**Purpose**: Foundational measurements for normalization

| Metric                 | Type  | Usage                                          |
| ---------------------- | ----- | ---------------------------------------------- |
| `total_words`          | int   | Document length, used for per-1k normalization |
| `total_sentences`      | int   | Sentence count for burstiness analysis         |
| `total_paragraphs`     | int   | Paragraph count for structure analysis         |
| `unique_words`         | int   | Vocabulary size for lexical diversity          |
| `lexical_diversity`    | float | Type-Token Ratio (TTR)                         |
| `paragraph_mean_words` | float | Average paragraph length                       |
| `paragraph_stdev`      | float | Paragraph length variation                     |
| `paragraph_range`      | tuple | (min, max) paragraph lengths                   |
| `file_path`            | str   | Source file identifier                         |

**Orphan Status**: None - all used in normalization/context

---

### TIER 1: ADVANCED DETECTION METRICS (60 points)

#### Dimension 1: GLTR Token Ranking (12 points max)

**Research**: 95% accuracy detecting GPT-3/ChatGPT [(Gehrmann et al., 2019)](https://arxiv.org/abs/1906.04043)

| Metric                   | Type  | AI Pattern   | Human Pattern | Scored             |
| ------------------------ | ----- | ------------ | ------------- | ------------------ |
| `gltr_top10_percentage`  | float | >70%         | <55%          | ✅ Primary         |
| `gltr_top100_percentage` | float | >90%         | <80%          | ❌ Reference only  |
| `gltr_mean_rank`         | float | <50          | >100          | ❌ Reference only  |
| `gltr_rank_variance`     | float | <500         | >1000         | ❌ Reference only  |
| `gltr_likelihood`        | float | >0.7         | <0.4          | ❌ Reference only  |
| `gltr_score`             | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
if gltr_top10_percentage >= 75: score = VERY LOW  # Strong AI signal
elif gltr_top10_percentage >= 65: score = LOW
elif gltr_top10_percentage >= 55: score = MEDIUM
else: score = HIGH  # Human-like
```

**Orphans**: `gltr_top100_percentage`, `gltr_mean_rank`, `gltr_rank_variance`, `gltr_likelihood` are calculated but not used in final scoring. Kept for detailed analysis mode.

---

#### Dimension 2: Advanced Lexical Diversity (8 points max)

**Research**: HDD most robust metric [(McCarthy & Jarvis, 2007)](https://doi.org/10.3758/BF03193446)

| Metric                   | Type  | AI Pattern   | Human Pattern | Scored             |
| ------------------------ | ----- | ------------ | ------------- | ------------------ |
| `hdd_score`              | float | 0.40-0.55    | 0.65-0.85     | ✅ Primary         |
| `yules_k`                | float | 100-150      | 60-90         | ✅ Secondary       |
| `maas_score`             | float | -            | -             | ❌ Reference only  |
| `vocab_concentration`    | float | -            | -             | ❌ Reference only  |
| `advanced_lexical_score` | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Weighted combination: HDD (70%) + Yule's K (30%)
hdd_signal = 4 if hdd >= 0.75 else 3 if hdd >= 0.65 else 2 if hdd >= 0.55 else 1
yules_signal = 4 if yules_k <= 70 else 3 if yules_k <= 90 else 2 if yules_k <= 110 else 1
combined = (hdd_signal * 0.7 + yules_signal * 0.3)
```

**Orphans**: `maas_score` and `vocab_concentration` calculated but not scored (experimental metrics).

---

#### Dimension 3: MATTR - Moving Average Type-Token Ratio (12 points max)

**Research**: 0.89 correlation with human judgments [(McCarthy & Jarvis, 2010)](https://doi.org/10.3758/BRM.42.2.381)

| Metric             | Type  | AI Pattern | Human Pattern  | Scored             |
| ------------------ | ----- | ---------- | -------------- | ------------------ |
| `mattr`            | float | <0.65      | ≥0.70          | ✅ Primary         |
| `mattr_assessment` | str   | POOR/FAIR  | GOOD/EXCELLENT | ✅ Used in scoring |

**Scoring Logic**:

```python
if mattr >= 0.75: score = 12.0, assessment = EXCELLENT
elif mattr >= 0.70: score = 9.0, assessment = GOOD
elif mattr >= 0.65: score = 5.0, assessment = FAIR
else: score = 0.0, assessment = POOR
```

**Window Size**: 100 tokens (research-validated default)
**Dependencies**: Requires `textacy` + `spaCy`

---

#### Dimension 4: RTTR - Root Type-Token Ratio (8 points max)

**Research**: Length-independent diversity measure

| Metric            | Type  | AI Pattern | Human Pattern  | Scored             |
| ----------------- | ----- | ---------- | -------------- | ------------------ |
| `rttr`            | float | <7.5       | ≥7.5           | ✅ Primary         |
| `rttr_assessment` | str   | POOR/FAIR  | GOOD/EXCELLENT | ✅ Used in scoring |

**Scoring Logic**:

```python
if rttr >= 8.5: score = 8.0, assessment = EXCELLENT
elif rttr >= 7.5: score = 6.0, assessment = GOOD
elif rttr >= 6.5: score = 3.0, assessment = FAIR
else: score = 0.0, assessment = POOR
```

**Formula**: `RTTR = unique_types / √total_tokens`

---

#### Dimension 5: AI Detection Ensemble (10 points max)

**Research**: RoBERTa sentiment variance as emotional flatness detector

| Metric                           | Type  | AI Pattern   | Human Pattern | Scored             |
| -------------------------------- | ----- | ------------ | ------------- | ------------------ |
| `roberta_sentiment_variance`     | float | <0.10        | >0.15         | ✅ Primary         |
| `roberta_sentiment_mean`         | float | ~0.0         | varied        | ❌ Reference only  |
| `roberta_emotionally_flat`       | bool  | True         | False         | ❌ Derived flag    |
| `roberta_avg_confidence`         | float | >0.9         | 0.6-0.8       | ❌ Reference only  |
| `roberta_ai_likelihood`          | float | >0.7         | <0.4          | ❌ Experimental    |
| `roberta_prediction_variance`    | float | <0.05        | >0.15         | ❌ Experimental    |
| `roberta_consistent_predictions` | bool  | True         | False         | ❌ Experimental    |
| `ai_detection_score`             | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
if sentiment_variance >= 0.20: score = HIGH
elif sentiment_variance >= 0.15: score = MEDIUM
elif sentiment_variance >= 0.10: score = LOW
else: score = VERY LOW  # Emotionally flat = AI
```

**Orphans**: RoBERTa AI classifier metrics (`roberta_ai_likelihood`, `roberta_prediction_variance`, `roberta_consistent_predictions`) are experimental and not used in scoring yet.

---

#### Dimension 6: Stylometric Markers (6 points max)

**Research**: AI transition word overuse [(Perkins, 2023)](https://www.forbes.com/sites/mollybohannon/2023/01/27/chatgpt-transition-phrases/)

| Metric                  | Type  | AI Pattern   | Human Pattern | Scored             |
| ----------------------- | ----- | ------------ | ------------- | ------------------ |
| `however_per_1k`        | float | 5-10/1k      | 1-3/1k        | ✅ Primary         |
| `moreover_per_1k`       | float | 3-8/1k       | 0-2/1k        | ✅ Primary         |
| `function_word_ratio`   | float | -            | -             | ❌ Experimental    |
| `passive_constructions` | int   | High         | Low           | ❌ Reference only  |
| `hapax_percentage`      | float | Low          | High          | ❌ Reference only  |
| `punctuation_density`   | float | -            | -             | ❌ Reference only  |
| `ttr_stability`         | float | High         | Varied        | ❌ Reference only  |
| `stylometric_score`     | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
combined_rate = however_per_1k + moreover_per_1k
if combined_rate >= 8: score = VERY LOW  # Strong AI signal
elif combined_rate >= 5: score = LOW
elif combined_rate >= 3: score = MEDIUM
else: score = HIGH
```

**Orphans**: Most stylometric metrics are reference-only. Only `however_per_1k` and `moreover_per_1k` actively scored.

---

#### Dimension 7: Syntactic Complexity (4 points max)

**Research**: Parse tree depth and subordination patterns

| Metric                       | Type  | AI Pattern   | Human Pattern | Scored             |
| ---------------------------- | ----- | ------------ | ------------- | ------------------ |
| `avg_tree_depth`             | float | 2-3          | 4-6           | ✅ Secondary       |
| `subordination_index`        | float | <0.1         | >0.15         | ✅ Primary         |
| `morphological_richness`     | int   | Low          | High          | ❌ Reference only  |
| `syntactic_repetition_score` | float | >0.15        | <0.10         | ❌ Reference only  |
| `pos_diversity`              | float | Low          | High          | ❌ Reference only  |
| `avg_dependency_depth`       | float | Low          | High          | ❌ Reference only  |
| `syntactic_score`            | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Weighted: subordination (70%), tree depth (30%)
if subordination >= 0.20: subord_signal = 4
elif subordination >= 0.15: subord_signal = 3
elif subordination >= 0.10: subord_signal = 2
else: subord_signal = 1

if tree_depth >= 5: depth_signal = 4
elif tree_depth >= 4: depth_signal = 3
elif tree_depth >= 3: depth_signal = 2
else: depth_signal = 1

combined = (subord_signal * 0.7 + depth_signal * 0.3)
```

**Orphans**: `morphological_richness`, `syntactic_repetition_score`, `pos_diversity`, `avg_dependency_depth` are calculated but not directly scored.

---

### TIER 2: CORE PATTERNS METRICS (59 points)

#### Dimension 8: Burstiness - Sentence Variation (12 points max)

**Research**: AI produces uniform sentence lengths [(Ippolito et al., 2020)](https://aclanthology.org/2020.findings-emnlp.1/)

| Metric                   | Type  | AI Pattern   | Human Pattern | Scored             |
| ------------------------ | ----- | ------------ | ------------- | ------------------ |
| `sentence_stdev`         | float | <6.0         | >8.0          | ✅ Primary         |
| `sentence_mean_length`   | float | ~15-20       | varied        | ❌ Context         |
| `sentence_min`           | int   | -            | -             | ❌ Context         |
| `sentence_max`           | int   | -            | -             | ❌ Context         |
| `sentence_range`         | tuple | Narrow       | Wide          | ❌ Context         |
| `short_sentences_count`  | int   | Few          | Many          | ✅ Secondary       |
| `medium_sentences_count` | int   | Many         | Balanced      | ❌ Context         |
| `long_sentences_count`   | int   | Few          | Some          | ✅ Secondary       |
| `sentence_lengths`       | list  | -            | -             | ❌ Raw data        |
| `burstiness_score`       | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Primary: standard deviation
if stdev >= 10: score = HIGH
elif stdev >= 8: score = MEDIUM
elif stdev >= 6: score = LOW
else: score = VERY LOW

# Penalty: check distribution balance
short_ratio = short_count / total_sentences
long_ratio = long_count / total_sentences
if short_ratio < 0.15 or long_ratio < 0.10:
    score = downgrade_one_level(score)  # Lacks variation
```

**Orphans**: `sentence_lengths` list is raw data not directly scored.

---

#### Dimension 9: Perplexity - Vocabulary Predictability (10 points max)

**Research**: AI overuses specific vocabulary

| Metric                  | Type  | AI Pattern   | Human Pattern | Scored             |
| ----------------------- | ----- | ------------ | ------------- | ------------------ |
| `ai_vocabulary_count`   | int   | High         | Low           | ✅ Primary         |
| `ai_vocabulary_per_1k`  | float | >5/1k        | <2/1k         | ✅ Primary         |
| `ai_vocabulary_list`    | list  | -            | -             | ❌ Reference       |
| `gpt2_perplexity`       | float | Low          | High          | ❌ Experimental    |
| `distilgpt2_perplexity` | float | Low          | High          | ❌ Experimental    |
| `perplexity_score`      | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**AI Vocabulary**: delve, robust, leverage, harness, meticulous, meticulously, comprehensive, facilitate, utilize, renowned, pivotal, crucial, vital, paramount, cornerstone

**Scoring Logic**:

```python
if ai_vocab_per_1k >= 5: score = VERY LOW
elif ai_vocab_per_1k >= 3: score = LOW
elif ai_vocab_per_1k >= 2: score = MEDIUM
else: score = HIGH
```

**Orphans**: True perplexity metrics (`gpt2_perplexity`, `distilgpt2_perplexity`) are calculated but not currently used in scoring (future enhancement).

---

#### Dimension 10: Formatting Patterns (8 points max)

**Research**: ChatGPT uses 10x more bold, em-dash cascading pattern

| Metric                         | Type  | AI Pattern   | Human Pattern | Scored             |
| ------------------------------ | ----- | ------------ | ------------- | ------------------ |
| `em_dash_count`                | int   | Many         | Few           | ❌ Context         |
| `em_dashes_per_page`           | float | >4/page      | <2/page       | ✅ Primary         |
| `bold_markdown_count`          | int   | Many         | Few           | ❌ Context         |
| `italic_markdown_count`        | int   | Moderate     | Few           | ❌ Context         |
| `bold_per_1k_words`            | float | >50/1k       | <20/1k        | ✅ Primary         |
| `italic_per_1k_words`          | float | >30/1k       | <15/1k        | ✅ Primary         |
| `formatting_consistency_score` | float | >0.7         | <0.4          | ✅ Secondary       |
| `em_dash_positions`            | list  | -            | -             | ❌ Raw data        |
| `em_dash_cascading_score`      | float | >0.6         | <0.3          | ✅ Secondary       |
| `formatting_score`             | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Multi-factor scoring
em_dash_signal = 4 if em_dash_per_page <= 1 else 3 if <= 2 else 2 if <= 3 else 1
bold_signal = 4 if bold_per_1k <= 15 else 3 if <= 25 else 2 if <= 40 else 1
cascade_signal = 4 if cascade_score < 0.2 else 3 if < 0.4 else 2 if < 0.6 else 1

combined = (em_dash_signal * 0.4 + bold_signal * 0.35 + cascade_signal * 0.25)
```

**Orphans**: `em_dash_positions` is raw data for cascade calculation.

---

#### Dimension 11: Heading Hierarchy (5 points max)

**Research**: AI creates perfect hierarchies, humans skip levels

| Metric                      | Type  | AI Pattern   | Human Pattern | Scored             |
| --------------------------- | ----- | ------------ | ------------- | ------------------ |
| `total_headings`            | int   | -            | -             | ❌ Context         |
| `heading_depth`             | int   | ≥4           | ≤3            | ✅ Primary         |
| `h1_count`                  | int   | -            | -             | ❌ Context         |
| `h2_count`                  | int   | -            | -             | ❌ Context         |
| `h3_count`                  | int   | -            | -             | ❌ Context         |
| `h4_plus_count`             | int   | >0           | 0             | ✅ Penalty         |
| `headings_per_page`         | float | -            | -             | ❌ Context         |
| `heading_parallelism_score` | float | >0.7         | <0.4          | ✅ Primary         |
| `heading_hierarchy_skips`   | int   | 0            | >0            | ✅ Bonus           |
| `heading_strict_adherence`  | float | 1.0          | <0.8          | ✅ Primary         |
| `heading_length_variance`   | float | Low          | High          | ✅ Secondary       |
| `heading_hierarchy_score`   | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Penalties for AI patterns
if heading_depth >= 4: penalty = -2
if heading_parallelism > 0.7: penalty -= 2
if heading_strict_adherence == 1.0: penalty -= 1

# Bonuses for human patterns
if heading_hierarchy_skips > 0: bonus = +1
if heading_length_variance > 3.0: bonus += 1
```

**Orphans**: Individual heading counts are context only.

---

#### Dimension 12: Heading Length Patterns (10 points max)

**Research**: 85% accuracy distinguishing AI vs human [(Chen et al., 2024)](https://arxiv.org/abs/2401.12070)

| Metric                      | Type  | AI Pattern | Human Pattern  | Scored             |
| --------------------------- | ----- | ---------- | -------------- | ------------------ |
| `avg_heading_length`        | float | 9-12 words | 3-7 words      | ✅ Primary         |
| `verbose_headings_count`    | int   | Many (>8w) | Few            | ✅ Secondary       |
| `heading_length_short_pct`  | float | <30%       | >60%           | ✅ Distribution    |
| `heading_length_medium_pct` | float | ~30%       | ~30%           | ✅ Distribution    |
| `heading_length_long_pct`   | float | >40%       | <10%           | ✅ Distribution    |
| `heading_length_assessment` | str   | POOR/FAIR  | GOOD/EXCELLENT | ✅ Used in scoring |

**Scoring Logic**:

```python
if avg_length <= 5: score = 10.0, EXCELLENT
elif avg_length <= 7: score = 7.0, GOOD
elif avg_length <= 9: score = 4.0, FAIR
else: score = 0.0, POOR

# Distribution bonus/penalty
if short_pct >= 60: bonus = +1
if long_pct >= 30: penalty = -2
```

**Orphans**: None - all metrics actively used.

---

#### Dimension 13: Subsection Asymmetry (8 points max)

**Research**: 78% accuracy on AI content detection

| Metric                     | Type  | AI Pattern  | Human Pattern  | Scored             |
| -------------------------- | ----- | ----------- | -------------- | ------------------ |
| `subsection_counts`        | list  | [3,3,4,3,4] | [1,5,2,8,0]    | ✅ Primary data    |
| `subsection_cv`            | float | <0.3        | ≥0.6           | ✅ Primary         |
| `subsection_uniform_count` | int   | Many        | Few            | ✅ Secondary       |
| `subsection_assessment`    | str   | POOR/FAIR   | GOOD/EXCELLENT | ✅ Used in scoring |

**Scoring Logic**:

```python
# Coefficient of Variation (CV) = stddev / mean
if cv >= 0.8: score = 8.0, EXCELLENT
elif cv >= 0.6: score = 5.0, GOOD
elif cv >= 0.4: score = 3.0, FAIR
else: score = 0.0, POOR

# Penalty for uniform clusters (3-4 subsections repeatedly)
if uniform_count >= 3: penalty = -2
```

**Orphans**: None - all metrics actively used.

---

#### Dimension 14: Heading Depth Variance (6 points max)

**Research**: AI follows rigid H1→H2→H3 progression

| Metric                     | Type | AI Pattern            | Human Pattern                  | Scored             |
| -------------------------- | ---- | --------------------- | ------------------------------ | ------------------ |
| `heading_transitions`      | dict | {H1→H2: 5, H2→H3: 10} | {H1→H2: 3, H3→H3: 4, H3→H1: 2} | ✅ Primary data    |
| `heading_depth_pattern`    | str  | RIGID                 | VARIED                         | ✅ Primary         |
| `heading_has_lateral`      | bool | False                 | True                           | ✅ Binary check    |
| `heading_has_jumps`        | bool | False                 | True                           | ✅ Binary check    |
| `heading_depth_assessment` | str  | POOR/FAIR             | GOOD/EXCELLENT                 | ✅ Used in scoring |

**Scoring Logic**:

```python
if has_lateral and has_jumps: score = 6.0, VARIED, EXCELLENT
elif has_lateral or has_jumps: score = 4.0, SEQUENTIAL, GOOD
elif len(transitions) <= 4 and no_lateral and no_jumps: score = 2.0, RIGID, FAIR
else: score = 0.0, RIGID, POOR
```

**Orphans**: None - all metrics actively used.

---

### TIER 3: SUPPORTING SIGNALS METRICS (25 points)

#### Dimension 15: Voice & Authenticity (8 points max)

**Research**: AI lacks personal perspective

| Metric                 | Type | AI Pattern   | Human Pattern | Scored             |
| ---------------------- | ---- | ------------ | ------------- | ------------------ |
| `first_person_count`   | int  | Low          | High          | ✅ Primary         |
| `direct_address_count` | int  | Low          | Moderate      | ✅ Secondary       |
| `contraction_count`    | int  | Few          | Many          | ✅ Secondary       |
| `voice_score`          | str  | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Multi-factor
first_person_signal = 4 if count >= 10 else 3 if >= 5 else 2 if >= 2 else 1
direct_address_signal = 4 if count >= 5 else 3 if >= 2 else 2 if >= 1 else 1
contraction_signal = 4 if count >= 8 else 3 if >= 4 else 2 if >= 1 else 1

combined = (first_person_signal * 0.5 + direct_address_signal * 0.3 + contraction_signal * 0.2)
```

**Orphans**: None.

---

#### Dimension 16: Structure & Organization (7 points max)

**Research**: AI uses formulaic transitions

| Metric                        | Type | AI Pattern   | Human Pattern | Scored             |
| ----------------------------- | ---- | ------------ | ------------- | ------------------ |
| `formulaic_transitions_count` | int  | Many         | Few           | ✅ Primary         |
| `formulaic_transitions_list`  | list | -            | -             | ❌ Reference       |
| `bullet_list_lines`           | int  | -            | -             | ❌ Context         |
| `numbered_list_lines`         | int  | -            | -             | ❌ Context         |
| `structure_score`             | str  | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Formulaic Transitions**: "In conclusion", "In summary", "Furthermore", "Moreover", "Additionally", "Firstly", "Secondly", "Lastly", "To summarize"

**Scoring Logic**:

```python
if transitions_count == 0: score = HIGH
elif transitions_count <= 2: score = MEDIUM
elif transitions_count <= 4: score = LOW
else: score = VERY LOW
```

**Orphans**: `formulaic_transitions_list` is reference only.

---

#### Dimension 17: Emotional Depth (6 points max)

**Research**: Sentiment variance as emotional authenticity marker

| Metric                     | Type  | AI Pattern   | Human Pattern | Scored             |
| -------------------------- | ----- | ------------ | ------------- | ------------------ |
| `sentiment_variance`       | float | <0.10        | >0.15         | ✅ Primary         |
| `sentiment_mean`           | float | ~0.0         | varied        | ❌ Context         |
| `sentiment_flatness_score` | str   | HIGH         | LOW/MEDIUM    | ❌ Derived         |
| `sentiment_score`          | str   | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Using RoBERTa sentiment variance (replaces VADER)
if variance >= 0.20: score = HIGH
elif variance >= 0.15: score = MEDIUM
elif variance >= 0.10: score = LOW
else: score = VERY LOW
```

**Orphans**: `sentiment_flatness_score` is derived flag.

---

#### Dimension 18: Technical Depth (4 points max)

**Research**: Domain expertise indicator

| Metric               | Type | AI Pattern   | Human Pattern | Scored             |
| -------------------- | ---- | ------------ | ------------- | ------------------ |
| `domain_terms_count` | int  | Low          | High          | ✅ Primary         |
| `domain_terms_list`  | list | -            | -             | ❌ Reference       |
| `technical_score`    | str  | LOW/VERY LOW | HIGH/MEDIUM   | ✅ Used in scoring |

**Scoring Logic**:

```python
# Normalized by document length
terms_per_1k = (domain_terms_count / total_words) * 1000
if terms_per_1k >= 15: score = HIGH
elif terms_per_1k >= 10: score = MEDIUM
elif terms_per_1k >= 5: score = LOW
else: score = VERY LOW
```

**Orphans**: `domain_terms_list` is reference only.

---

### ADDITIONAL METRICS (Not Currently Scored)

#### Enhanced Structural Analysis (NEW - not yet scored)

These metrics were added for future enhancements but are NOT currently included in dual scoring:

| Category             | Metrics                                                                                                                                           | Status                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| **List Usage**       | `total_list_items`, `ordered_list_items`, `unordered_list_items`, `list_to_text_ratio`, `ordered_to_unordered_ratio`, `list_item_length_variance` | ❌ Calculated, not scored   |
| **Punctuation**      | `oxford_comma_count`, `non_oxford_comma_count`, `oxford_comma_consistency`, `semicolon_count`, `semicolon_per_1k_words`                           | ❌ Calculated, not scored   |
| **Whitespace**       | `paragraph_length_variance`, `paragraph_uniformity_score`, `blank_lines_count`, `blank_lines_variance`, `text_density`                            | ❌ Calculated, not scored   |
| **Code Blocks**      | `code_block_count`, `code_blocks_with_lang`, `code_lang_consistency`, `avg_code_comment_density`                                                  | ❌ Calculated, not scored   |
| **Dimension Scores** | `bold_italic_score`, `list_usage_score`, `punctuation_score`, `whitespace_score`, `code_structure_score`                                          | ❌ Not used in dual scoring |

**Reason**: These were implemented for future research but are not validated for production scoring yet.

#### Structural Pattern Analysis (Partially Scored)

**Note**: These ARE calculated and displayed but NOT included in dual scoring algorithm:

| Metric                        | Type  | Status                              |
| ----------------------------- | ----- | ----------------------------------- |
| `paragraph_cv`                | float | ✅ Calculated, ❌ Not in dual score |
| `paragraph_cv_score`          | float | ✅ Scored separately                |
| `paragraph_cv_assessment`     | str   | ✅ Displayed                        |
| `section_variance_pct`        | float | ✅ Calculated, ❌ Not in dual score |
| `section_variance_score`      | float | ✅ Scored separately                |
| `section_variance_assessment` | str   | ✅ Displayed                        |
| `list_max_depth`              | int   | ✅ Calculated, ❌ Not in dual score |
| `list_depth_score`            | float | ✅ Scored separately                |
| `list_depth_assessment`       | str   | ✅ Displayed                        |
| `structural_patterns_score`   | str   | ✅ HIGH/MEDIUM/LOW assessment       |

**Reason**: These have their own separate scoring system (24 points max) but are NOT integrated into the 144-point dual scoring system.

#### Readability Metrics (Optional)

**Dependencies**: Requires `textstat`

| Metric                 | Usage           |
| ---------------------- | --------------- |
| `flesch_reading_ease`  | ❌ Display only |
| `flesch_kincaid_grade` | ❌ Display only |
| `gunning_fog`          | ❌ Display only |
| `smog_index`           | ❌ Display only |

**Reason**: Educational context, not AI detection signals.

#### Textacy Metrics (Optional)

**Dependencies**: Requires `textacy`

| Metric                  | Usage                       |
| ----------------------- | --------------------------- |
| `automated_readability` | ❌ Reference only           |
| `textacy_diversity`     | ❌ Superseded by MATTR/RTTR |

**Reason**: Superseded by more specific metrics (MATTR, RTTR).

#### NLTK Metrics (Optional)

**Dependencies**: Requires `nltk`

| Metric              | Usage           |
| ------------------- | --------------- |
| `mtld_score`        | ❌ Experimental |
| `stemmed_diversity` | ❌ Experimental |

**Reason**: Experimental, not validated.

#### DetectGPT Metrics (Experimental)

**Dependencies**: Requires `transformers`

| Metric                            | Usage              |
| --------------------------------- | ------------------ |
| `detectgpt_perturbation_variance` | ❌ Not implemented |
| `detectgpt_original_loss`         | ❌ Not implemented |
| `detectgpt_is_likely_ai`          | ❌ Not implemented |

**Reason**: Future enhancement, not yet implemented.

---

## Dual Scoring Algorithm

### Quality Score Calculation (0-144 points, normalized to 0-100)

**Formula**:

```python
quality_score = (
    advanced_detection_total +  # 60 points
    core_patterns_total +       # 59 points
    supporting_signals_total    # 25 points
)  # Total: 144 points raw

# Display as 0-100 normalized in reports
normalized_quality = (quality_score / 144.0) * 100
```

**Tier Breakdown**:

#### Tier 1: Advanced Detection (60 points)

```python
advanced_total = (
    gltr_score        # 12 pts - Token ranking
  + lexical_score     #  8 pts - HDD/Yule's K
  + mattr_score       # 12 pts - MATTR lexical richness
  + rttr_score        #  8 pts - RTTR global diversity
  + ai_detect_score   # 10 pts - RoBERTa sentiment variance
  + stylo_score       #  6 pts - However/Moreover markers
  + syntax_score      #  4 pts - Subordination/tree depth
)
```

#### Tier 2: Core Patterns (59 points)

```python
core_total = (
    burst_score          # 12 pts - Sentence variation
  + perp_score           # 10 pts - AI vocabulary
  + format_score         #  8 pts - Em-dash/bold patterns
  + heading_score        #  5 pts - Hierarchy depth/parallelism
  + heading_length       # 10 pts - Heading word count
  + subsection_score     #  8 pts - Subsection asymmetry
  + depth_variance_score #  6 pts - Heading transitions
)
```

#### Tier 3: Supporting Signals (25 points)

```python
supporting_total = (
    voice_score      #  8 pts - First-person/contractions
  + structure_score  #  7 pts - Formulaic transitions
  + sentiment_score  #  6 pts - Emotional variation
  + technical_score  #  4 pts - Domain terminology
)
```

**Score-Level Mapping**:
All dimension scores (HIGH/MEDIUM/LOW/VERY LOW) are converted to 0-1 scale:

```python
score_map = {
    "HIGH": 1.0,       # Excellent, human-like
    "MEDIUM": 0.75,    # Good, mostly human-like
    "LOW": 0.5,        # Poor, somewhat AI-like
    "VERY LOW": 0.25,  # Very poor, AI-like
    "UNKNOWN": 0.5,    # No data, neutral assumption
    "N/A": 0.5         # Not applicable, neutral
}

dimension_points = score_level_value * max_points
# Example: MEDIUM burstiness = 0.75 * 12 = 9.0 points
```

**Quality Interpretation Bands**:

```python
if quality_score >= 95:  return "EXCEPTIONAL - Indistinguishable from human"
elif quality_score >= 85: return "EXCELLENT - Publication-ready"
elif quality_score >= 70: return "GOOD - Natural with minor tells"
elif quality_score >= 50: return "MIXED - Needs moderate work"
elif quality_score >= 30: return "AI-LIKE - Needs significant work"
else:                    return "VERY AI-LIKE - Extensive humanization required"
```

---

### Detection Risk Calculation (0-100+ points, lower = better)

**Formula**:

```python
# Base detection risk (weighted combination of key dimensions)
base_risk = (
    (1.0 - gltr_val) * 25       # GLTR has highest detection correlation
  + (1.0 - ai_detect_val) * 20  # RoBERTa ensemble
  + (1.0 - lexical_val) * 15    # Lexical diversity
  + (1.0 - stylo_val) * 15      # Stylometric markers
  + (1.0 - burst_val) * 10      # Burstiness
  + (1.0 - format_val) * 10     # Formatting patterns
  + (1.0 - perp_val) * 5        # Vocabulary
)  # Total: 100 points from base components

# Additional risk penalties (advanced lexical & heading metrics)
if mattr < 0.70:                 base_risk += 10  # Poor lexical richness
if rttr < 7.5:                   base_risk += 6   # Poor global diversity
if avg_heading_length > 8:       base_risk += 8   # Verbose headings
if subsection_cv < 0.3:          base_risk += 7   # Uniform subsections
if heading_depth_pattern == 'RIGID': base_risk += 5  # Rigid hierarchy

detection_risk = base_risk  # Can exceed 100
```

**Key Differences from Quality Score**:

1. **Inverted relationship**: Lower detection risk = better (opposite of quality)
2. **Different weighting**: GLTR and AI Detection get higher weights (25%, 20% vs 12pts, 10pts in quality)
3. **Penalty system**: Additional penalties for specific AI patterns
4. **Can exceed 100**: Unlike quality (capped at 144), detection risk can go above 100 for extremely AI-like content

**Detection Risk Interpretation Bands**:

```python
if detection_risk <= 14:  return "VERY LOW - Minimal detection risk"
elif detection_risk <= 29: return "LOW - Unlikely to be flagged"
elif detection_risk <= 49: return "MEDIUM - May be flagged"
elif detection_risk <= 69: return "HIGH - Likely to be flagged"
else:                     return "VERY HIGH - Will be flagged"
```

**Why Separate Risk Score?**

- **Quality measures human-likeness** (comprehensive, all dimensions matter)
- **Detection Risk measures detectability** (focused on what AI detectors actually catch)
- Some quality dimensions (like technical depth) don't correlate strongly with detection
- Detection tools heavily weight specific signals (GLTR, sentiment variance, AI vocabulary)

---

## Dimension Scoring Methods

### Score Calculation Pattern

All dimensions follow this pattern:

```python
def _score_dimension(self, r: AnalysisResults) -> str:
    """
    Calculate dimension score based on metrics
    Returns: HIGH / MEDIUM / LOW / VERY LOW
    """
    # 1. Extract relevant metrics
    metric_value = r.metric_name

    # 2. Define thresholds (research-backed or empirically validated)
    if metric_value >= excellent_threshold:
        return "HIGH"       # Human-like
    elif metric_value >= good_threshold:
        return "MEDIUM"     # Mostly human-like
    elif metric_value >= fair_threshold:
        return "LOW"        # AI-like tendencies
    else:
        return "VERY LOW"   # Strong AI signal
```

### Example: Burstiness Scoring

```python
def _score_burstiness(self, r: AnalysisResults) -> str:
    """
    Score sentence variation (burstiness)
    AI: stdev <6, Human: stdev >8
    """
    stdev = r.sentence_stdev
    short_ratio = r.short_sentences_count / r.total_sentences
    long_ratio = r.long_sentences_count / r.total_sentences

    # Primary signal: standard deviation
    if stdev >= 10:
        score = "HIGH"
    elif stdev >= 8:
        score = "MEDIUM"
    elif stdev >= 6:
        score = "LOW"
    else:
        score = "VERY LOW"

    # Penalty for poor distribution
    if short_ratio < 0.15 or long_ratio < 0.10:
        score = self._downgrade_one_level(score)

    return score
```

### Example: MATTR Scoring

```python
def _score_textacy_lexical(self, r: AnalysisResults) -> str:
    """
    Score MATTR + RTTR combined
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

    # Average and convert to HIGH/MEDIUM/LOW/VERY LOW
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
```

---

## Orphaned Metrics Analysis

### Fully Orphaned (Calculated but Never Used)

**Tier: GLTR**

- `gltr_top100_percentage` - Reference data only
- `gltr_mean_rank` - Reference data only
- `gltr_rank_variance` - Reference data only
- `gltr_likelihood` - Reference data only

**Tier: Advanced Lexical**

- `maas_score` - Experimental, not validated
- `vocab_concentration` - Experimental, not validated

**Tier: RoBERTa**

- `roberta_sentiment_mean` - Context only
- `roberta_avg_confidence` - Not discriminative
- `roberta_ai_likelihood` - Experimental classifier
- `roberta_prediction_variance` - Experimental
- `roberta_consistent_predictions` - Experimental

**Tier: Stylometric**

- `function_word_ratio` - Not currently used
- `passive_constructions` - Reference only
- `hapax_percentage` - Reference only
- `punctuation_density` - Reference only
- `ttr_stability` - Reference only

**Tier: Syntactic**

- `morphological_richness` - Not scored
- `syntactic_repetition_score` - Not scored
- `pos_diversity` - Not scored
- `avg_dependency_depth` - Not scored

**Tier: Perplexity**

- `gpt2_perplexity` - Future enhancement
- `distilgpt2_perplexity` - Future enhancement

**Tier: Enhanced Structural** (NEW - not in dual scoring)

- All list usage metrics (6 metrics)
- All punctuation metrics (5 metrics)
- All whitespace metrics (5 metrics)
- All code block metrics (4 metrics)
- All enhanced dimension scores (5 scores)

**Total Orphans**: ~40 metrics (50% of all metrics)

### Semi-Orphaned (Calculated, Displayed, But Not in Dual Scoring)

**Structural Pattern Analysis** (separate 24-point system):

- `paragraph_cv` + related metrics
- `section_variance_pct` + related metrics
- `list_max_depth` + related metrics
- `structural_patterns_score` (HIGH/MEDIUM/LOW)

**Readability Metrics** (display-only):

- `flesch_reading_ease`
- `flesch_kincaid_grade`
- `gunning_fog`
- `smog_index`

**Total Semi-Orphans**: ~12 metrics (15% of all metrics)

### Fully Integrated (Used in Dual Scoring)

**Primary scored metrics**: ~28 metrics (35% of total)

### Summary

- **Total metrics**: ~80
- **Fully integrated**: ~28 (35%)
- **Semi-orphaned**: ~12 (15%)
- **Fully orphaned**: ~40 (50%)

**Recommendation**: Consider removing fully orphaned metrics or document them as "research/experimental" in a separate section.

---

## Data Flow Architecture

### Analysis Pipeline

```
1. INPUT: Markdown file
   ↓
2. PREPROCESSING
   - Strip frontmatter (YAML/TOML)
   - Remove HTML comments
   - Extract text, headings, code blocks
   ↓
3. BASIC METRICS CALCULATION
   - Word count, sentence count, paragraph count
   - Lexical diversity (TTR)
   ↓
4. DIMENSION ANALYSIS (parallel where possible)
   ├─ Perplexity: AI vocabulary detection
   ├─ Burstiness: Sentence length variation
   ├─ Structure: Transitions, lists, headings
   ├─ Voice: First-person, contractions
   ├─ Technical: Domain terminology
   ├─ Formatting: Em-dashes, bold/italic
   ├─ GLTR: Token ranking (if transformers available)
   ├─ Advanced Lexical: HDD, Yule's K, MATTR, RTTR
   ├─ Syntactic: Tree depth, subordination
   ├─ Stylometric: However/moreover frequency
   ├─ Sentiment: RoBERTa variance
   ├─ Heading: Length, asymmetry, depth variance
   └─ Structural: Paragraph CV, section variance
   ↓
5. DIMENSION SCORING
   - Convert raw metrics to HIGH/MEDIUM/LOW/VERY LOW
   ↓
6. DUAL SCORE CALCULATION
   ├─ Quality Score: Weighted sum across 3 tiers (144 pts)
   └─ Detection Risk: Weighted inverse with penalties (100+ pts)
   ↓
7. OUTPUT GENERATION
   ├─ Standard report (human-readable)
   ├─ Dual score report (optimization-focused)
   ├─ JSON export (machine-readable)
   └─ TSV export (batch analysis)
```

### Scoring Data Flow

```
Raw Metrics (AnalysisResults)
   ↓
Dimension Scoring Methods (_score_*)
   ↓
Score Level (HIGH/MEDIUM/LOW/VERY LOW)
   ↓
Numerical Conversion (score_map: 1.0/0.75/0.5/0.25)
   ↓
Point Calculation (value * max_points)
   ↓
Category Totals (Advanced 60, Core 59, Supporting 25)
   ↓
Final Scores
   ├─ Quality: Sum of all points (0-144)
   └─ Detection Risk: Weighted inverse + penalties (0-100+)
```

### Historical Tracking Flow

```
analyze_ai_patterns.py --show-scores file.md
   ↓
Calculate Dual Score
   ↓
Check: .score-history/file.history.json exists?
   ├─ YES: Load previous scores
   │   ↓
   │   Compare current vs previous
   │   ↓
   │   Calculate trends (IMPROVING/STABLE/WORSENING)
   └─ NO: Initialize new history
   ↓
Append current score to history
   ↓
Save .score-history/file.history.json
   ↓
Display trend in report
```

---

## Version History

### v3.0.0 (Current - 2025-01-02)

- **BREAKING**: Renamed all "Phase 2" references to descriptive names
- **CHANGE**: Updated from deprecated TextStats API to direct function calls
- **FIX**: Suppressed transformers `loss_type` warning
- **CHANGE**: Advanced Detection increased from 40→60 points (added MATTR 12pts, RTTR 8pts)
- **CHANGE**: Core Patterns increased from 35→59 points (added heading analysis: 10+8+6=24pts)
- **Total scoring**: 144 points (was 100 points in v2.x)

### v2.0.0

- Added dual scoring system (Quality + Detection Risk)
- Added historical tracking
- Added path-to-target optimization

### v1.0.0

- Initial release with 8 dimensions
- Single overall score only

---

## Configuration

### Required Dependencies

```
python >= 3.7
nltk >= 3.8.0
spacy >= 3.7.0
textacy >= 0.13.0  # For MATTR/RTTR
transformers >= 4.35.0  # For GLTR, RoBERTa, GPT-2
torch >= 2.0.0  # For transformers
scipy >= 1.10.0  # For HDD, Yule's K
```

### Optional Dependencies

```
textstat >= 0.7.0  # Readability metrics
```

### Environment Setup

```bash
cd data/tools
python3 -m venv nlp-env
source nlp-env/bin/activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab vader_lexicon
python -m spacy download en_core_web_sm
```

---

## Usage Examples

### Basic Analysis

```bash
python analyze_ai_patterns.py manuscript.md
```

### Dual Score with Targets

```bash
python analyze_ai_patterns.py manuscript.md \
  --show-scores \
  --quality-target 85 \
  --detection-target 30
```

### Batch Analysis

```bash
python analyze_ai_patterns.py --batch chapters/ --format tsv > results.tsv
```

### JSON Export

```bash
python analyze_ai_patterns.py manuscript.md --format json > analysis.json
```

---

## Research References

1. **GLTR**: Gehrmann et al. (2019). "GLTR: Statistical Detection and Visualization of Generated Text"
2. **HDD**: McCarthy & Jarvis (2007). "Vocd: A theoretical and empirical evaluation"
3. **MATTR**: McCarthy & Jarvis (2010). "MTLD, vocd-D, and HD-D: A validation study"
4. **Heading Length**: Chen et al. (2024). "AI-Generated Text Detection via Heading Patterns"
5. **Burstiness**: Ippolito et al. (2020). "Automatic Detection of Generated Text"

---

**END OF SPECIFICATION**

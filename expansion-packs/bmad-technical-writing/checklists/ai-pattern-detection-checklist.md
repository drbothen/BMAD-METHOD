# AI Pattern Detection Checklist

<!-- Powered by BMAD™ Core -->

## Purpose

Systematically identify AI-characteristic patterns in content to diagnose humanization needs and prioritize editing efforts. Use this checklist before beginning humanization to create a targeted improvement plan.

## When to Use

- Before humanization editing begins
- When assessing content quality
- When troubleshooting "robotic" feel
- When comparing before/after humanization results
- When training on AI pattern recognition

---

## PRIMARY DIAGNOSTIC: Dual Score Analysis

**RECOMMENDED FIRST STEP**: Run automated dual score analysis for comprehensive AI pattern detection across 14 dimensions.

### Run AI Pattern Analysis Tool

```bash
cd {{config.root}}/data/tools

# Activate Python environment (required first time - see analyze-ai-patterns.md for setup)
source nlp-env/bin/activate  # macOS/Linux
# OR nlp-env\Scripts\activate  # Windows

# Run dual score diagnostic analysis (adaptive mode for fast diagnostics)
python analyze_ai_patterns.py PATH_TO_FILE \
  --show-scores \
  --profile full \
  --quality-target 85 \
  --detection-target 30 \
  --domain-terms "Domain,Specific,Terms"

# Deactivate when done
deactivate
```

**Example**:

```bash
source nlp-env/bin/activate
python analyze_ai_patterns.py ../manuscript/chapters/chapter-03.md \
  --show-scores \
  --profile full \
  --domain-terms "Docker,Kubernetes,PostgreSQL"
deactivate
```

### Interpret Diagnostic Scores

**⚠️ LABEL SYSTEM NOTE**:
- **Dimension quality labels** (what scores dimensions get): **EXCELLENT / GOOD / NEEDS WORK / POOR** (new positive labels)
- **Detection Risk labels** (how likely to be detected): **VERY HIGH / HIGH / MEDIUM / LOW / VERY LOW** (unchanged)

**Quality Score (0-100, higher=better)** - Overall quality assessment:

- [ ] **95-100**: EXCEPTIONAL - Already reads like authentic human writing ✅
- [ ] **85-94**: EXCELLENT - Minimal AI signatures, light polish only ✅
- [ ] **70-84**: GOOD - Natural with minor tells, needs light humanization ⚠️
- [ ] **50-69**: MIXED - Moderate AI patterns, systematic editing required ⚠️
- [ ] **<50**: AI-LIKE - Substantial work needed or regenerate ❌

**Detection Risk (0-100, lower=better)** - Likelihood of AI detection:

- [ ] **0-14**: VERY LOW - Safe from detection ✅
- [ ] **15-29**: LOW - Unlikely to be flagged ✅
- [ ] **30-49**: MEDIUM - May be flagged by some detectors ⚠️
- [ ] **50-69**: HIGH - Likely to be flagged ❌
- [ ] **70-100**: VERY HIGH - Will be flagged ❌

### Review 14-Dimension Breakdown

The tool analyzes across **3 tiers** (14 dimensions total):

**TIER 1: Advanced Detection (40 points) - Highest Accuracy Signals**:

- [ ] **GLTR Token Ranking** (/12 pts) - Token predictability analysis
  - Target: ≥9 pts (75% of max)
  - If low: Content has high token predictability (strong AI signature)

- [ ] **Advanced Lexical Diversity** (/8 pts) - HDD/Yule's K metrics
  - Target: ≥6 pts (75% of max)
  - If low: Vocabulary is repetitive, lacks sophisticated variation

- [ ] **AI Detection Ensemble** (/10 pts) - RoBERTa sentiment + DetectGPT
  - Target: ≥7 pts (70% of max)
  - If low: Emotional flatness, high detectability via perturbation

- [ ] **Stylometric Markers** (/6 pts) - Statistical writing fingerprints
  - Target: ≥4 pts (67% of max)
  - If low: Writing shows mechanical patterns, lacks human variability

- [ ] **Syntactic Complexity** (/4 pts) - Dependency depth, POS patterns
  - Target: ≥3 pts (75% of max)
  - If low: Sentence structures too uniform, lacks natural complexity variation

**TIER 2: Core Patterns (35 points) - Strong AI Signals**:

- [ ] **Burstiness (Sentence Variation)** (/12 pts) - Sentence length variation
  - Target: ≥9 pts (75% of max)
  - If low: Uniform sentence lengths (15-25 words), lacks rhythm variation

- [ ] **Perplexity (Vocabulary)** (/10 pts) - AI-typical word choices
  - Target: ≥7 pts (70% of max)
  - If low: High density of AI words (delve, leverage, robust, harness, etc.)

- [ ] **Formatting Patterns** (/8 pts) - Em-dashes, bold, italics distribution
  - Target: ≥6 pts (75% of max)
  - If low: Excessive em-dashes (>3 per page), over-bolding (>5%), uniform italics

- [ ] **Heading Hierarchy** (/5 pts) - Depth, parallelism, density
  - Target: ≥3 pts (60% of max)
  - If low: 4+ heading levels, parallel structures, uniform subsection counts

**TIER 3: Supporting Signals (25 points) - Contextual Indicators**:

- [ ] **Voice & Authenticity** (/8 pts) - Personal perspective, contractions
  - Target: ≥5 pts (63% of max)
  - If low: Lacks personal markers, overly formal, no contractions

- [ ] **Structure & Organization** (/7 pts) - Transitions, list usage
  - Target: ≥5 pts (71% of max)
  - If low: Formulaic transitions, excessive lists, rigid paragraph structure

- [ ] **Emotional Depth** (/6 pts) - Sentiment variation, empathy
  - Target: ≥4 pts (67% of max)
  - If low: Emotionally flat, no reader acknowledgment, no enthusiasm

- [ ] **Technical Depth** (/4 pts) - Domain terminology, practitioner signals
  - Target: ≥2 pts (50% of max)
  - If low: Generic examples, missing version numbers, surface-level only

### Path-to-Target Action Plan

The tool provides **ROI-sorted recommendations** showing exactly what to improve:

**Review path-to-target output**:

- [ ] **HIGH-ROI actions identified** (largest score gain per effort)
- [ ] **Effort levels noted** (LOW: 15-30 min, MEDIUM: 30-45 min, HIGH: 45-90 min)
- [ ] **Cumulative score projections** (estimated score after each action)
- [ ] **Priority actions selected** (focus on top 1-3 recommendations)

**Example path-to-target**:

```
PATH TO TARGET (4 actions, sorted by ROI)
────────────────────────────────────────────────────────────────────────────────

1. GLTR Token Ranking (Effort: HIGH)
   Current: 3.0/12.0 → Gain: +9.0 pts → Cumulative: 76.8
   Action: Rewrite high-predictability segments (>70% top-10 tokens)

2. Burstiness (Sentence Variation) (Effort: MEDIUM)
   Current: 9.0/12.0 → Gain: +3.0 pts → Cumulative: 79.8
   Action: Improve Burstiness (Sentence Variation)

3. Formatting Patterns (Effort: LOW)
   Current: 2.5/8.0 → Gain: +5.5 pts → Cumulative: 85.3
   Action: Reduce em-dash density to 1-2 per page, normalize bolding to 2-5%
```

### Diagnostic Decision

**Minimal Humanization Needed** (Quality ≥85, Detection ≤30):

- [ ] Content already publication-ready ✅
- [ ] Light polish only (15-30 min per 1000 words)
- [ ] Proceed to technical review

**Light Humanization Needed** (Quality 70-84, Detection 30-49):

- [ ] Systematic editing required ⚠️
- [ ] Focus on path-to-target priorities
- [ ] Estimated effort: 30-60 min per 1000 words
- [ ] Use humanize-post-generation.md workflow

**Substantial Humanization Needed** (Quality 50-69, Detection 50-69):

- [ ] Comprehensive editing workflow required ❌
- [ ] Address all flagged dimensions systematically
- [ ] Estimated effort: 60-90 min per 1000 words
- [ ] Use iterative-humanization-optimization.md for systematic improvement

**Regeneration Recommended** (Quality <50, Detection ≥70):

- [ ] Too many AI patterns for efficient editing ❌
- [ ] Consider regenerating with humanization prompt
- [ ] If editing: Multi-pass workflow essential, 90+ min per 1000 words
- [ ] Use humanize-pre-generation.md for prompt engineering approach

### Create Targeted Improvement Plan

Based on dual score analysis, document top priorities:

**Priority 1** (Highest ROI from path-to-target): **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

- Dimension: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***
- Current score: **\_** / **\_** points
- Target score: **\_** points
- Effort level: LOW / MEDIUM / HIGH
- Specific action: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

**Priority 2**: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

- Dimension: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***
- Current score: **\_** / **\_** points
- Target score: **\_** points
- Effort level: LOW / MEDIUM / HIGH
- Specific action: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

**Priority 3**: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

- Dimension: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***
- Current score: **\_** / **\_** points
- Target score: **\_** points
- Effort level: LOW / MEDIUM / HIGH
- Specific action: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

**Total estimated effort**: **\_** minutes

**Recommended workflow**:

- [ ] Single-pass editing (humanize-post-generation.md)
- [ ] Iterative optimization (iterative-humanization-optimization.md)
- [ ] Regeneration with humanization prompt (humanize-pre-generation.md)

---

## SUPPLEMENTARY MANUAL CHECKS

**Use the sections below for granular manual inspection when needed, or when dual score analysis is unavailable.**

---

## Section 1: Vocabulary Patterns

### High-Priority AI Words (Tier 1)

Search document for these words and mark any occurrences:

- [ ] **delve** / delving / delves
- [ ] **leverage** / leveraging / leverages
- [ ] **robust** / robustness
- [ ] **harness** / harnessing / harnesses
- [ ] **underscore** / underscores / underscoring
- [ ] **facilitate** / facilitates / facilitating
- [ ] **pivotal**
- [ ] **holistic** / holistically

**Count**: **\_** occurrences

**Assessment**:

- 0-2 occurrences per 1000 words = ✅ Good
- 3-5 occurrences per 1000 words = ⚠️ Needs attention
- 6+ occurrences per 1000 words = ❌ Critical issue

### Medium-Priority AI Words (Tier 2)

Check for overuse of these words:

- [ ] seamless / seamlessly
- [ ] comprehensive / comprehensively
- [ ] optimize / optimization
- [ ] streamline / streamlined
- [ ] paramount
- [ ] quintessential
- [ ] myriad
- [ ] plethora

**Count**: **\_** occurrences

**Assessment**:

- 0-3 per 1000 words = ✅ Acceptable
- 4-7 per 1000 words = ⚠️ Reduce usage
- 8+ per 1000 words = ❌ Significant problem

### Formulaic Transitions

Count occurrences of each:

- [ ] "Furthermore," - Count: **\_**
- [ ] "Moreover," - Count: **\_**
- [ ] "Additionally," - Count: **\_**
- [ ] "In addition," - Count: **\_**
- [ ] "It is important to note that" - Count: **\_**
- [ ] "It is worth mentioning that" - Count: **\_**
- [ ] "One of the key aspects" - Count: **\_**
- [ ] "When it comes to" - Count: **\_**

**Total formulaic transitions**: **\_**

**Assessment**:

- 0-1 = ✅ Good
- 2-4 = ⚠️ Needs smoothing
- 5+ = ❌ Priority fix required

---

## Section 2: Sentence Structure Patterns

### Sentence Length Analysis

Select 3 representative paragraphs and measure sentence word counts:

**Paragraph 1**:

- Sentence 1: **\_** words
- Sentence 2: **\_** words
- Sentence 3: **\_** words
- Sentence 4: **\_** words
- Sentence 5: **\_** words
- Sentence 6: **\_** words

Mean length: **\_** words
Range: **\_** to **\_** words (spread: **\_** words)

**Paragraph 2**:

- Sentence 1: **\_** words
- Sentence 2: **\_** words
- Sentence 3: **\_** words
- Sentence 4: **\_** words
- Sentence 5: **\_** words
- Sentence 6: **\_** words

Mean length: **\_** words
Range: **\_** to **\_** words (spread: **\_** words)

**Paragraph 3**:

- Sentence 1: **\_** words
- Sentence 2: **\_** words
- Sentence 3: **\_** words
- Sentence 4: **\_** words
- Sentence 5: **\_** words
- Sentence 6: **\_** words

Mean length: **\_** words
Range: **\_** to **\_** words (spread: **\_** words)

**Overall Assessment**:

Check all that apply:

- [ ] Most sentences fall within 12-25 word range
- [ ] No sentences shorter than 8 words
- [ ] No sentences longer than 35 words
- [ ] Range (spread) is less than 10 words per paragraph
- [ ] Lengths are highly uniform across paragraphs

**Burstiness Score**:

- 0-1 boxes checked = ✅ Good variation (High Burstiness)
- 2-3 boxes checked = ⚠️ Some uniformity (Medium Burstiness)
- 4-5 boxes checked = ❌ Critical uniformity (Low Burstiness)

### Sentence Opening Patterns

Examine the first sentence of 10 consecutive paragraphs:

- [ ] Paragraph 1 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 2 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 3 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 4 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 5 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 6 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 7 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 8 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 9 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Paragraph 10 starts with: \***\*\*\*\*\***\_\***\*\*\*\*\***

**Pattern Analysis**:

- How many start with "The [noun]..."? **\_**
- How many start with identical subject? **\_**
- How many use topic sentence formula? **\_**

**Assessment**:

- 0-2 repetitive openings = ✅ Good variety
- 3-5 repetitive openings = ⚠️ Some monotony
- 6+ repetitive openings = ❌ Critical monotony

---

## Section 3: Structural Organization

### List Usage Analysis

Count instances:

- [ ] Numbered lists: **\_** total
- [ ] Bulleted lists: **\_** total
- [ ] Lists that could be prose: **\_** (subjective assessment)

**Assessment** (per 1000 words):

- 0-2 lists = ✅ Appropriate use
- 3-4 lists = ⚠️ Moderate overuse
- 5+ lists = ❌ Excessive list reliance

### Paragraph Structure

Check paragraph organization:

- [ ] Most paragraphs follow topic-sentence-first structure
- [ ] Paragraphs rarely use questions as openings
- [ ] Paragraphs rarely use fragments as openings
- [ ] Every paragraph has formal conclusion sentence

**Score**:

- 0-1 boxes checked = ✅ Natural variation
- 2-3 boxes checked = ⚠️ Some rigidity
- 4 boxes checked = ❌ Formulaic structure

### Section Heading Patterns

Analyze 5-10 section headings:

- [ ] Heading 1: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Heading 2: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Heading 3: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Heading 4: \***\*\*\*\*\***\_\***\*\*\*\*\***
- [ ] Heading 5: \***\*\*\*\*\***\_\***\*\*\*\*\***

**Pattern Check**:

- [ ] All headings use parallel grammatical structure
- [ ] Multiple headings use "Understanding [X]" or "Exploring [Y]" format
- [ ] Multiple headings are generic ("Benefits," "Challenges," "Considerations")
- [ ] All headings are questions OR all headings are statements (no mix)

**Assessment**:

- 0-1 boxes checked = ✅ Natural heading variety
- 2-3 boxes checked = ⚠️ Some formulaic patterns
- 4 boxes checked = ❌ Rigid heading structure

---

## Section 4: Voice and Authenticity

### Personal Voice Markers

Count occurrences of authentic voice indicators:

**First-Person Perspective**:

- [ ] Uses "I" or "my" - Count: **\_**
- [ ] Uses "we" or "our" - Count: **\_**
- [ ] Uses "you" or "your" - Count: **\_**

**Personal Insights**:

- [ ] "In my experience..." - Count: **\_**
- [ ] "I've found that..." - Count: **\_**
- [ ] "From what I've seen..." - Count: **\_**
- [ ] Similar perspective markers - Count: **\_**

**Total personal voice markers**: **\_**

**Assessment** (per 1000 words):

- 8+ markers = ✅ Strong personal voice
- 4-7 markers = ⚠️ Some voice present
- 0-3 markers = ❌ Impersonal/detached

### Specificity vs. Abstraction

**Specific Examples Check**:

- [ ] Number of specific examples with details: **\_**
- [ ] Number of generic examples (user, application, system): **\_**
- [ ] Ratio: Specific / Generic = **\_**

**Specific Details Check**:

- [ ] Version numbers mentioned: Yes / No - Count: **\_**
- [ ] Specific tool/product names: Yes / No - Count: **\_**
- [ ] Error messages or outputs shown: Yes / No - Count: **\_**
- [ ] Real-world scenarios (not textbook): Yes / No - Count: **\_**

**Assessment**:

- 6+ specific details = ✅ Well-grounded
- 3-5 specific details = ⚠️ Somewhat abstract
- 0-2 specific details = ❌ Too generic

### Emotional Engagement

Check for emotional resonance markers:

- [ ] Expresses enthusiasm for interesting points
- [ ] Acknowledges reader challenges or frustrations
- [ ] Shows empathy for learning difficulties
- [ ] Celebrates reader progress
- [ ] Includes conversational asides or humor

**Count emotional engagement instances**: **\_**

**Assessment** (for full document):

- 4+ instances = ✅ Emotionally engaging
- 2-3 instances = ⚠️ Somewhat neutral
- 0-1 instances = ❌ Emotionally flat

---

## Section 5: Technical Content Depth

### Technical Depth Markers

**Positive Indicators** (count each):

- [ ] Specific version numbers - Count: **\_**
- [ ] Concrete error messages/outputs - Count: **\_**
- [ ] Trade-offs acknowledged - Count: **\_**
- [ ] Implementation details beyond basics - Count: **\_**
- [ ] Gotchas or edge cases mentioned - Count: **\_**
- [ ] "In practice..." or similar practitioner language - Count: **\_**

**Total positive markers**: **\_**

**Negative Indicators** (count each):

- [ ] Vague technical claims without specifics - Count: **\_**
- [ ] Surface-level coverage only - Count: **\_**
- [ ] Missing prerequisite information - Count: **\_**
- [ ] Generic code examples (foo/bar naming) - Count: **\_**

**Total negative markers**: **\_**

**Assessment**:

- More positive than negative by 3:1 ratio = ✅ Authentic expertise
- Balanced or slight positive advantage = ⚠️ Mixed signals
- More negative than positive = ❌ Shallow/generic

### Practitioner Signal Check

- [ ] References real tools/libraries (not hypothetical)
- [ ] Mentions practical workflows or commands
- [ ] Discusses when approach does/doesn't work
- [ ] Shows hands-on experience vs. documentation paraphrasing
- [ ] Includes lessons from mistakes or "learned the hard way"

**Boxes checked**: **\_**

**Assessment**:

- 4-5 boxes = ✅ Strong practitioner voice
- 2-3 boxes = ⚠️ Some expertise signals
- 0-1 boxes = ❌ Lacks authenticity

---

## Section 6: Coherence and Context

### Global Coherence Check

- [ ] Could sections be reordered without loss of meaning?
- [ ] Ideas build progressively throughout document
- [ ] Concepts reference previously introduced information
- [ ] Document has narrative arc or clear conceptual journey

**Assessment**:

- Strong progressive build = ✅ Good coherence
- Some connection but weak progression = ⚠️ Moderate coherence
- Standalone sections with little connection = ❌ Weak coherence

### Contextual Awareness

- [ ] Content re-explains previously defined terms
- [ ] Concepts are re-introduced in multiple sections
- [ ] Lacks forward/backward references within document
- [ ] Doesn't build on prior knowledge established earlier

**Boxes checked**: **\_**

**Assessment**:

- 0 boxes = ✅ Good contextual awareness
- 1-2 boxes = ⚠️ Some repetition
- 3-4 boxes = ❌ Poor context tracking

---

## Overall AI Pattern Score

### Dimension Summary

Transfer scores from each section:

| Dimension                      | Score    | Notes                                    |
| ------------------------------ | -------- | ---------------------------------------- |
| **Vocabulary** (Sec 1)         | ✅ ⚠️ ❌ | AI words: **\_**, Transitions: **\_**    |
| **Sentence Structure** (Sec 2) | ✅ ⚠️ ❌ | Burstiness: **\_**, Openings: **\_**     |
| **Organization** (Sec 3)       | ✅ ⚠️ ❌ | Lists: **\_**, Structure: **\_**         |
| **Voice/Authenticity** (Sec 4) | ✅ ⚠️ ❌ | Voice markers: **\_**, Specifics: **\_** |
| **Technical Depth** (Sec 5)    | ✅ ⚠️ ❌ | Pos markers: **\_**, Neg markers: **\_** |
| **Coherence** (Sec 6)          | ✅ ⚠️ ❌ | Global: **\_**, Context: **\_**          |

### Overall Assessment

**Interpretation** (using new positive dimension labels):

- **All or most ✅** = MINIMAL HUMANIZATION NEEDED (Quality ≥85, dimensions GOOD/EXCELLENT)
  - Content already reads naturally
  - Light polish recommended
  - Estimated effort: 15-30 min per 1000 words

- **Mix of ✅ and ⚠️** = LIGHT TO MODERATE HUMANIZATION NEEDED (Quality 70-84, some NEEDS WORK)
  - Systematic editing required
  - Focus on ⚠️ and ❌ areas (NEEDS WORK / POOR dimensions)
  - Estimated effort: 30-60 min per 1000 words

- **Multiple ⚠️ and some ❌** = SUBSTANTIAL HUMANIZATION NEEDED (Quality 50-69, multiple NEEDS WORK/POOR)
  - Comprehensive editing workflow required
  - Address all dimensions systematically
  - Estimated effort: 60-90 min per 1000 words

- **Multiple ❌** = EXTENSIVE HUMANIZATION NEEDED (Quality <50, many POOR dimensions)
  - Consider regeneration with humanization prompt
  - If editing: multi-pass workflow essential
  - Estimated effort: 90+ min per 1000 words

**Note**: Dimension scores now use positive labels (EXCELLENT/GOOD/NEEDS WORK/POOR) instead of confusing impact labels.

---

## Priority Action Plan

Based on your assessment, identify top 3 priorities:

**Priority 1** (Most Critical): **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

- Specific issue: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***
- Recommended technique: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

**Priority 2**: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

- Specific issue: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***
- Recommended technique: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

**Priority 3**: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

- Specific issue: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***
- Recommended technique: **\*\*\*\***\*\***\*\*\*\***\_**\*\*\*\***\*\***\*\*\*\***

---

## Quick Decision Guide

### Should I Edit or Regenerate?

**Edit the existing content if**:

- ✅ Technical accuracy is solid
- ✅ Overall structure is sound
- ✅ Issues are primarily vocabulary/style
- ✅ Word count is appropriate

**Regenerate with humanization prompt if**:

- ❌ Multiple critical issues across all dimensions
- ❌ Content is too generic/abstract throughout
- ❌ Would take longer to fix than to regenerate
- ❌ Structure needs complete rethinking

---

## Related Resources

- **Tasks**: analyze-ai-patterns.md, iterative-humanization-optimization.md, humanize-post-generation.md, humanize-pre-generation.md
- **Data**: ai-detection-patterns.md, humanization-techniques.md
- **Checklists**: humanization-quality-checklist.md

---

## Notes

- Complete this checklist BEFORE beginning humanization
- Use findings to create targeted improvement plan
- Re-run after humanization to measure improvement
- Keep record of patterns for future prompt engineering

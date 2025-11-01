# Task: Analyze AI Patterns in Content

<!-- Powered by BMAD™ Core -->

## Purpose

Systematically identify AI-characteristic patterns in content to diagnose humanization needs and prioritize editing efforts for maximum impact.

## When to Use This Task

- Before beginning post-generation humanization editing
- When assessing content quality and naturalness
- When troubleshooting why content "feels" AI-generated
- When training team members to recognize AI patterns
- When evaluating humanization effectiveness (before/after comparison)

## Prerequisites

- Content to analyze (AI-generated or suspected AI content)
- Text editor or analysis tool
- 10-15 minutes for thorough analysis

## Analysis Framework

This task produces a scored assessment across five key dimensions that distinguish AI from human writing.

---

## Dimension 1: Perplexity Analysis (Vocabulary Predictability)

### What to Analyze

Perplexity measures how predictable word choices are. AI systems favor statistically common words, creating low perplexity. Human writing includes unexpected vocabulary choices, creating higher perplexity.

### How to Assess

#### 1.1 AI-Characteristic Vocabulary Count

Search the content for these common AI words and count occurrences:

**Tier 1 (Most Obvious AI Markers)**:
- delve / delving / delves
- robust / robustness
- leverage / leveraging / leverages
- facilitate / facilitates / facilitating
- underscore / underscores / underscoring
- harness / harnesses / harnessing
- pivotal
- holistic

**Tier 2 (Overused by AI)**:
- seamless / seamlessly
- comprehensive / comprehensively
- optimize / optimization / optimizing
- streamline / streamlined
- paramount
- quintessential
- myriad
- plethora

**Tier 3 (Context-Dependent)**:
- innovative (unless discussing actual innovation)
- cutting-edge (unless it genuinely is)
- revolutionary (almost never appropriate)
- game-changing (marketing cliché)

#### 1.2 Scoring

| AI Words Found | Perplexity Score | Assessment |
|----------------|------------------|------------|
| 0-2 per 1000 words | HIGH (Good) | Minimal AI vocabulary |
| 3-5 per 1000 words | MEDIUM | Noticeable AI patterns |
| 6-10 per 1000 words | LOW | Significant AI vocabulary |
| 11+ per 1000 words | VERY LOW | Obviously AI-generated |

**Record**: `Perplexity Score: [HIGH/MEDIUM/LOW/VERY LOW]`

---

## Dimension 2: Burstiness Analysis (Sentence Variation)

### What to Analyze

Burstiness measures variation in sentence length and structure. Humans naturally vary between short and long sentences. AI tends toward uniform lengths.

### How to Assess

#### 2.1 Sample Selection

Choose 3 representative paragraphs (about 150-200 words each) from different sections.

#### 2.2 Measure Sentence Lengths

For each paragraph:
1. Count words in each sentence
2. Record: [Sentence 1: X words, Sentence 2: Y words, etc.]

#### 2.3 Calculate Statistics

For each paragraph:
- **Mean length**: Average words per sentence
- **Range**: Shortest to longest sentence
- **Variation**: How much lengths differ

#### 2.4 Pattern Analysis

**Red Flags (Low Burstiness - AI-typical)**:
- Most sentences within narrow range (e.g., 15-25 words)
- No sentences shorter than 10 words
- No sentences longer than 30 words
- Consistent pattern across multiple paragraphs

**Green Flags (High Burstiness - Human-like)**:
- Mix of short (5-10), medium (15-25), and long (30-45+) sentences
- Occasional fragments (1-4 words)
- Unpredictable variation
- Pattern differs between paragraphs

#### 2.5 Scoring

| Pattern | Burstiness Score | Assessment |
|---------|------------------|------------|
| Wide variation, unpredictable | HIGH (Good) | Human-like rhythm |
| Some variation, but patterns visible | MEDIUM | Moderate variation |
| Narrow range, most sentences similar | LOW | Uniform AI pattern |
| Nearly identical lengths | VERY LOW | Obviously algorithmic |

**Record**: `Burstiness Score: [HIGH/MEDIUM/LOW/VERY LOW]`

**Example Calculation**:
```
Paragraph Sample: 5 sentences
Lengths: 12, 18, 15, 19, 16 words
Mean: 16 words
Range: 12-19 (only 7-word spread)
Assessment: LOW burstiness (narrow range, no variety)
```

---

## Dimension 3: Structural Pattern Analysis

### What to Analyze

AI systems fall into predictable structural patterns: formulaic transitions, rigid paragraph structures, list overuse, and repetitive opening patterns.

### How to Assess

#### 3.1 Transition Word Analysis

Count occurrences of formulaic transitions:

**Primary Markers**:
- "Furthermore," → Count: ___
- "Moreover," → Count: ___
- "Additionally," → Count: ___
- "In addition," → Count: ___
- "It is important to note that" → Count: ___
- "It is worth mentioning that" → Count: ___
- "When it comes to" → Count: ___
- "One of the key aspects" → Count: ___

**Total formulaic transitions**: ___

#### 3.2 Paragraph Opening Analysis

Examine the first sentence of 10 paragraphs:

- How many start with "The [noun]..."? Count: ___
- How many start with identical subjects? Count: ___
- How many use topic sentence formula (direct fact statement)? Count: ___

#### 3.3 List Structure Analysis

Count instances where AI defaulted to list format:
- Numbered lists: ___
- Bulleted lists: ___
- Lists that could be prose: ___

#### 3.4 Scoring

| Issue | Count | Impact |
|-------|-------|--------|
| Formulaic transitions | 0-1 = Low, 2-4 = Medium, 5+ = High | |
| Repetitive openings | 0-2 = Low, 3-5 = Medium, 6+ = High | |
| Excessive lists | 0-1 = Low, 2-3 = Medium, 4+ = High | |

**Overall Structural Score**:
- All Low impacts = HIGH (Good)
- Mix of Low/Medium = MEDIUM
- Any High impact = LOW
- Multiple High impacts = VERY LOW

**Record**: `Structural Score: [HIGH/MEDIUM/LOW/VERY LOW]`

---

## Dimension 4: Voice and Authenticity Analysis

### What to Analyze

AI-generated content often lacks personal voice, authentic perspective, specific examples, and emotional connection.

### How to Assess

#### 4.1 Personal Voice Markers

Count presence of authentic voice indicators:

**Perspective Markers**:
- First person usage ("I," "we," "my," "our"): Yes/No, Count: ___
- Direct address ("you," "your"): Yes/No, Count: ___
- Personal insights ("In my experience," "I've found"): Count: ___

**Specificity Markers**:
- Specific examples with details (names, numbers, versions): Count: ___
- Real-world scenarios vs. generic examples: ___/___
- Concrete anecdotes vs. abstract statements: ___/___

**Emotional Engagement**:
- Expressions of enthusiasm, concern, or other appropriate emotions: Count: ___
- Acknowledgment of reader challenges: Count: ___
- Conversational asides or parenthetical thoughts: Count: ___

#### 4.2 Authenticity Red Flags

**Check for**:
- [ ] Content maintains uniform formality throughout (no tone variation)
- [ ] No acknowledgment of complexity or trade-offs
- [ ] Everything presented with absolute certainty (no hedging)
- [ ] Generic statements without supporting specifics
- [ ] No evidence of authorial expertise or perspective

#### 4.3 Scoring

| Authenticity Indicators | Count | Voice Score |
|-------------------------|-------|-------------|
| Multiple voice markers + specific examples + emotion | 10+ | HIGH (Good) |
| Some voice markers + occasional specifics | 5-9 | MEDIUM |
| Minimal voice markers + mostly generic | 2-4 | LOW |
| No voice markers + completely generic | 0-1 | VERY LOW |

**Record**: `Voice Score: [HIGH/MEDIUM/LOW/VERY LOW]`

---

## Dimension 5: Technical Content Analysis

### What to Analyze

For technical writing specifically, assess whether content demonstrates genuine expertise or relies on AI-typical abstractions.

### How to Assess

#### 5.1 Technical Depth Markers

**Positive Indicators** (count occurrences):
- Specific version numbers mentioned: ___
- Concrete error messages or outputs shown: ___
- Trade-offs or context-dependencies acknowledged: ___
- Implementation details beyond basic API usage: ___
- Gotchas or edge cases mentioned: ___

**Negative Indicators** (count occurrences):
- Vague technical claims without specifics: ___
- Surface-level coverage without depth: ___
- Missing prerequisite or version information: ___
- Code examples that are too generic (foo/bar naming): ___

#### 5.2 Practical Expertise Signals

**Check for**:
- [ ] References to real tools or libraries (not hypothetical)
- [ ] Mentions of practical workflows or commands
- [ ] Discussion of when approach does/doesn't work
- [ ] Evidence of hands-on experience vs. documentation paraphrasing

#### 5.3 Scoring

| Pattern | Technical Authenticity Score |
|---------|------------------------------|
| Multiple positive indicators, few negative | HIGH (Good) |
| Mix of positive and negative indicators | MEDIUM |
| More negative than positive indicators | LOW |
| Mostly vague abstractions, no specifics | VERY LOW |

**Record**: `Technical Score: [HIGH/MEDIUM/LOW/VERY LOW]`

---

## Comprehensive Assessment

### Overall AI Pattern Score

Combine all dimension scores:

| Dimension | Score | Weight |
|-----------|-------|--------|
| Perplexity | [HIGH/MEDIUM/LOW/VERY LOW] | 20% |
| Burstiness | [HIGH/MEDIUM/LOW/VERY LOW] | 25% |
| Structure | [HIGH/MEDIUM/LOW/VERY LOW] | 20% |
| Voice | [HIGH/MEDIUM/LOW/VERY LOW] | 20% |
| Technical | [HIGH/MEDIUM/LOW/VERY LOW] | 15% |

### Interpretation

**Overall Assessment**:
- All/Most HIGH scores = **MINIMAL HUMANIZATION NEEDED** (content is already natural)
- Mix of HIGH/MEDIUM scores = **LIGHT HUMANIZATION NEEDED** (polish and refine)
- Multiple MEDIUM/LOW scores = **SUBSTANTIAL HUMANIZATION NEEDED** (systematic editing required)
- Multiple LOW/VERY LOW scores = **EXTENSIVE HUMANIZATION NEEDED** (may need regeneration with better prompts)

### Priority Recommendations

Based on scores, recommend focus areas:

1. **If Perplexity is LOW**: Priority on vocabulary replacement
2. **If Burstiness is LOW**: Priority on sentence variation
3. **If Structure is LOW**: Priority on transition smoothing and pattern breaking
4. **If Voice is LOW**: Priority on adding authenticity and personal touches
5. **If Technical is LOW**: Priority on adding specific details and expertise markers

---

## Output Deliverable

**Create Analysis Report**:

```
AI PATTERN ANALYSIS REPORT
==========================

Content: [Title/Description]
Word Count: [approximate]
Analysis Date: [date]

DIMENSION SCORES:
-----------------
Perplexity:  [HIGH/MEDIUM/LOW/VERY LOW]
  - AI vocabulary count: X instances
  - Primary issues: [list top 3 AI words found]

Burstiness:  [HIGH/MEDIUM/LOW/VERY LOW]
  - Sample mean sentence length: X words
  - Range: X-Y words
  - Primary issue: [uniform/narrow variation/etc.]

Structure:   [HIGH/MEDIUM/LOW/VERY LOW]
  - Formulaic transitions: X instances
  - List overuse: X instances
  - Primary issue: [specific pattern]

Voice:       [HIGH/MEDIUM/LOW/VERY LOW]
  - Personal markers: X instances
  - Specific examples: X instances
  - Primary issue: [lacks voice/generic/etc.]

Technical:   [HIGH/MEDIUM/LOW/VERY LOW]
  - Expertise markers: X instances
  - Primary issue: [surface-level/vague/etc.]

OVERALL ASSESSMENT:
-------------------
[MINIMAL/LIGHT/SUBSTANTIAL/EXTENSIVE] HUMANIZATION NEEDED

PRIORITY ACTIONS:
-----------------
1. [Highest priority improvement]
2. [Second priority improvement]
3. [Third priority improvement]

ESTIMATED EFFORT:
-----------------
[15-30 / 30-60 / 60-90 / 90+] minutes per 1000 words

RECOMMENDATION:
---------------
[Specific recommendation: edit existing, regenerate with better prompt, etc.]
```

## Success Criteria

✅ All five dimensions systematically assessed
✅ Specific evidence documented for each score
✅ Clear priorities identified for humanization
✅ Realistic effort estimate provided
✅ Actionable recommendations given

## Tips for Effective Analysis

💡 **Be objective**: Score based on evidence, not gut feeling
💡 **Document examples**: Note specific instances that led to scores
💡 **Consider audience**: Some AI patterns matter more for certain audiences
💡 **Use for learning**: Track patterns across multiple analyses to improve prompt engineering
💡 **Compare before/after**: Re-analyze after humanization to measure improvement

## Related Tasks

- `humanize-post-generation.md` - Execute humanization based on this analysis
- `humanization-qa-check.md` - Verify humanization improvements
- `humanize-pre-generation.md` - Use insights to improve future prompts

## Example: Sample Analysis

```
AI PATTERN ANALYSIS REPORT
==========================

Content: "Introduction to Docker Containers"
Word Count: ~2,500 words
Analysis Date: 2025-10-31

DIMENSION SCORES:
-----------------
Perplexity:  LOW
  - AI vocabulary count: 18 instances
  - Primary issues: "robust" (6x), "leverage" (4x), "facilitate" (3x)

Burstiness:  VERY LOW
  - Sample mean sentence length: 17 words
  - Range: 14-21 words across 3 paragraphs
  - Primary issue: extreme uniformity, no short or long sentences

Structure:   LOW
  - Formulaic transitions: 12 instances ("Furthermore" 5x, "Moreover" 4x)
  - List overuse: 8 numbered/bulleted lists
  - Primary issue: rigid transitions and excessive lists

Voice:       VERY LOW
  - Personal markers: 0 instances
  - Specific examples: 2 instances (both generic)
  - Primary issue: completely impersonal, no authentic voice

Technical:   MEDIUM
  - Expertise markers: 5 instances (version numbers, specific commands)
  - Primary issue: surface-level but technically accurate

OVERALL ASSESSMENT:
-------------------
EXTENSIVE HUMANIZATION NEEDED

PRIORITY ACTIONS:
-----------------
1. URGENT: Introduce sentence variation (currently uniform)
2. HIGH: Replace 18 AI vocabulary instances
3. HIGH: Convert lists to prose, smooth transitions
4. MEDIUM: Add voice through examples and perspective

ESTIMATED EFFORT:
-----------------
60-90 minutes for full humanization

RECOMMENDATION:
---------------
Consider regenerating with humanization prompt to save editing time.
If editing: Focus first on burstiness (mechanical rhythm most obvious issue),
then vocabulary, then voice. Technical content is adequate and can stay.
```

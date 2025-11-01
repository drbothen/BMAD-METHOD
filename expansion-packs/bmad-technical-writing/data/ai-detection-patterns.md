# AI Detection Patterns Reference

<!-- Powered by BMAD™ Core -->

## Overview

This reference document catalogs the specific linguistic patterns, statistical markers, and structural characteristics that AI detection systems use to identify machine-generated content. Understanding these patterns enables effective humanization by addressing the actual detection mechanisms rather than guessing at improvements.

---

## Detection Methodologies Overview

### Statistical Analysis Methods

AI detectors primarily analyze three quantifiable dimensions:

1. **Perplexity** - Word-level predictability measurement
2. **Burstiness** - Sentence-level variation measurement
3. **N-gram Analysis** - Pattern repetition across word sequences

### Classifier-Based Methods

- **GPT-2 Output Detector** - OpenAI's original detection model
- **GPTZero** - Academic-focused detector emphasizing perplexity and burstiness
- **Originality.AI** - Commercial detector with multi-model analysis
- **Turnitin AI Detection** - Educational sector detector
- **Winston AI** - Enterprise detection system

### Ensemble Methods

Modern detectors combine multiple approaches:

- Statistical analysis + ML classification
- Multiple model agreement scoring
- Contextual semantic analysis
- Stylometric fingerprinting

---

## Category 1: Vocabulary Patterns

### 1.1 AI-Characteristic Words (High Detection Signal)

These words appear with statistically significant higher frequency in AI-generated content:

**Tier 1 - Extremely High AI Association**:

- **delve** / delving / delves - appears 15-20x more frequently in AI text
- **leverage** / leveraging / leverages - 12-18x higher frequency
- **robust** / robustness - 10-15x higher frequency
- **harness** / harnessing / harnesses - 8-12x higher frequency
- **underscore** / underscores / underscoring - 7-11x higher frequency
- **facilitate** / facilitates / facilitating - 9-14x higher frequency
- **pivotal** - 6-10x higher frequency
- **holistic** / holistically - 8-13x higher frequency

**Tier 2 - High AI Association**:

- seamless / seamlessly
- comprehensive / comprehensively
- optimize / optimization / optimizing
- streamline / streamlined
- paramount
- quintessential
- myriad
- plethora
- utilize / utilization (vs. simpler "use")
- commence (vs. "start")
- endeavor (vs. "try" or "attempt")

**Tier 3 - Context-Dependent Markers**:

- innovative (overused in marketing AI content)
- cutting-edge (cliché signal)
- revolutionary (hyperbole marker)
- game-changing (marketing cliché)
- transformative (abstract overuse)

### 1.2 Formulaic Phrase Patterns

**Transition Phrases** (Strong Detection Signal):

- "Furthermore," - classic AI transition
- "Moreover," - formal academic AI marker
- "Additionally," - frequent AI connector
- "In addition," - redundant AI pattern
- "It is important to note that" - verbose AI hedging
- "It is worth mentioning that" - unnecessary AI qualifier
- "One of the key aspects of" - generic AI framing
- "When it comes to" - vague AI introduction

**Meta-Commentary Phrases** (AI Tendency):

- "It should be noted that..."
- "It is crucial to understand that..."
- "One must consider that..."
- "It is essential to recognize that..."
- "As we delve deeper into..."
- "Let us explore the intricacies of..."

### 1.3 Adverb Overuse Pattern

AI systems frequently use weak verb + adverb combinations instead of stronger single verbs:

**Detection Patterns**:

- very + adjective (very important, very difficult)
- highly + adjective (highly effective, highly efficient)
- extremely + adjective (extremely useful, extremely complex)
- particularly + adjective
- remarkably + adjective
- exceptionally + adjective

**Human Alternative**: Single strong verb or adjective

- "runs quickly" → "sprints" or "races"
- "very important" → "critical" or "essential"
- "highly effective" → "powerful" or "potent"

---

## Category 2: Sentence Structure Patterns

### 2.1 Uniform Sentence Length (Primary Detection Signal)

**AI-Typical Pattern**:

- Mean sentence length: 15-22 words
- Standard deviation: < 5 words
- Range: Most sentences within 12-25 word band
- Distribution: Normal curve centered around mean

**Detection Threshold**:

- If 70%+ of sentences fall within 6-word range → High AI probability
- If standard deviation < 4 words → Strong AI signal
- If no sentences < 8 words or > 35 words → Detection flag

**Example AI Pattern**:

```
Sentence 1: 18 words
Sentence 2: 16 words
Sentence 3: 19 words
Sentence 4: 17 words
Sentence 5: 20 words
Sentence 6: 16 words
Mean: 17.7 words, StdDev: 1.5 words → DETECTED
```

### 2.2 Topic Sentence Formula

**AI Pattern**: Consistent paragraph opening structure

- 60-80% of paragraphs start with direct topic sentences
- Common opening: "The [subject] is/provides/enables..."
- Formulaic structure: Subject + linking verb + predicate nominative
- Rarely uses varied openings (questions, fragments, dependent clauses)

**Detection Signal**:

```
"The system provides three main benefits..."
"Docker is a containerization platform that..."
"Authentication serves as the foundation for..."
"The primary advantage of this approach is..."
```

### 2.3 Parallel Structure Overuse

**AI Tendency**: Excessive grammatical parallelism

- Lists with perfect parallel structure (100% consistent)
- Repeated sentence patterns within paragraphs
- Rhythmic uniformity that feels mechanical

**Example**:

```
AI generates content. AI analyzes data. AI provides insights.
(Perfect parallelism → Detection signal)

vs. Human variation:
AI generates content. It can analyze massive datasets.
The insights? Often surprising.
```

---

## Category 3: Structural Organization Patterns

### 3.1 List Overuse Pattern

**AI Default Behavior**:

- Defaults to numbered/bulleted lists for any multi-point content
- Lists appear with >50% higher frequency than human writing
- Rigid hierarchical structure (1, 2, 3 / a, b, c)
- Rarely converts lists to flowing prose

**Detection Threshold**:

- More than 3-4 lists per 1000 words → AI signal
- Lists where prose would be more natural → Strong signal
- Nested lists with perfect formatting → Detection flag

### 3.2 Section Heading Patterns

**AI-Characteristic Headings**:

- Generic descriptive: "Benefits," "Challenges," "Considerations"
- Formulaic: "Understanding [Topic]," "Exploring [Concept]"
- Question format overuse: "What is [X]?", "How does [Y] work?"
- Parallel structure in all headings

**Human Writing Variation**:

- Mix of styles: questions, statements, fragments
- Creative or unexpected phrasings
- Inconsistent grammatical structure
- Domain-specific terminology in headings

### 3.3 Introduction-Body-Conclusion Rigidity

**AI Pattern**:

- Strictly follows academic structure even for informal content
- Introduction always previews entire document
- Conclusion always summarizes all points
- Transitions are explicit and formulaic

**Detection Signal**:

```
Introduction: "In this article, we will explore..."
Body: Systematic point-by-point coverage
Conclusion: "In conclusion, we have examined..."
```

---

## Category 4: Tone and Voice Patterns

### 4.1 Emotional Neutrality

**AI Characteristic**: Consistently neutral emotional register

- Rarely expresses enthusiasm, frustration, or surprise
- Avoids subjective statements or opinions
- Maintains uniform formality throughout
- Lacks personality or authorial presence

**Detection Signals**:

- No first-person perspective ("I," "my experience")
- No acknowledgment of reader challenges or emotions
- No conversational asides or informal remarks
- Absence of humor, sarcasm, or irony

### 4.2 Hedge Word Patterns

**AI Overuse of Qualifiers**:

- "may potentially" (redundant hedging)
- "generally tends to" (double hedge)
- "often can be" (weak certainty)
- "might possibly" (excessive caution)
- "typically usually" (contradictory hedges)

**Detection Pattern**: 2+ hedge words in single sentence = strong AI signal

### 4.3 Absolute Certainty on Uncertain Topics

**AI Contradiction**: Paradoxically, AI sometimes presents uncertain information with false certainty

- States opinions as facts without attribution
- Lacks nuance on complex topics with multiple valid viewpoints
- Doesn't acknowledge trade-offs or context-dependencies
- Presents "best practices" as universal truths

---

## Category 5: Content Depth Patterns

### 5.1 Surface-Level Abstraction

**AI Tendency**: Stays at abstract conceptual level without grounding in specifics

**Detection Signals**:

- Generic examples: "user," "application," "system," "database"
- Absence of specific versions, tools, or products
- No error messages, output samples, or concrete details
- Theoretical explanations without practical grounding

**Example AI Pattern**:

```
"The database stores data efficiently and retriably."
(Generic, no specifics)

vs. Human:
"PostgreSQL 14's BRIN indexes reduced our storage by 40%
for time-series data, but rebuilding them after bulk
inserts became a bottleneck."
(Specific version, metric, trade-off)
```

### 5.2 Breadth Over Depth

**AI Pattern**: Covers many points superficially rather than few points deeply

- Lists 8-10 benefits without exploring any deeply
- Mentions concepts without explaining mechanisms
- Provides overview without diving into implementation
- Avoids edge cases, gotchas, or non-obvious details

### 5.3 Missing Practitioner Signals

**Human Expert Markers** (Often absent in AI text):

- "I learned this the hard way when..."
- "This confused me for weeks until..."
- "In production, you'll typically see..."
- "The documentation says X, but in practice Y..."
- References to specific error messages or behaviors
- Discussion of what doesn't work and why

---

## Category 6: Coherence and Context Patterns

### 6.1 Local Coherence, Weak Global Coherence

**AI Characteristic**:

- Sentences connect well locally (within paragraphs)
- Weak thematic connection across sections
- Ideas don't build progressively - each section feels standalone
- Lack of narrative arc or conceptual journey

**Detection Method**:

- Check if sections could be reordered without loss of meaning
- If yes → likely AI (human writing typically has intentional flow)

### 6.2 Contextual Repetition

**AI Pattern**: Unnecessary re-explanation of previously introduced concepts

- Redefines terms already defined
- Re-explains concepts in multiple sections
- Lacks forward references ("as we discussed earlier")
- Doesn't build on prior knowledge within document

### 6.3 Missing Domain Context

**AI Gap**: Lacks contextual awareness of domain conventions

- Explains basics that domain audience would know
- Misses domain-specific terminology or insider references
- Doesn't acknowledge current debates or trends in field
- Generic rather than domain-situated

---

## Category 7: Technical Content Specific Patterns

### 7.1 Code Example Characteristics

**AI-Generated Code Signals**:

- Generic variable names: foo, bar, baz, myVar, temp
- Minimal comments or overly verbose comments
- Perfect formatting (never messy or evolving)
- No debugging artifacts (console.logs, commented code)
- Examples that are "too clean" to be real

**Human Code Signals**:

- Domain-specific naming (userData, apiClient, orderProcessor)
- Practical comments addressing gotchas
- Realistic error handling
- Version-specific syntax choices

### 7.2 Technical Accuracy vs. Hallucination

**AI Risk Patterns**:

- Confident statements about non-existent features
- Mixing features from different versions
- Creating plausible-sounding but incorrect API names
- Stating best practices that aren't actually standard

**Detection**: Technical reviewers spot these, but automated detectors can't easily flag hallucinations

### 7.3 Missing Technical Nuance

**AI Simplification Pattern**:

- Presents complex topics without acknowledging complexity
- Omits important caveats or prerequisites
- Doesn't mention breaking changes or version differences
- Lacks discussion of trade-offs or alternative approaches

---

## Category 8: Stylometric Patterns

### 8.1 Lexical Diversity Metrics

**AI Tendency**: Lower lexical diversity (Type-Token Ratio)

- Repeats same words more frequently than humans
- Smaller vocabulary range for given text length
- Predictable synonym choices

**Measurement**:

- TTR = (Unique words / Total words)
- AI typical: 0.40-0.50 for 1000 words
- Human typical: 0.55-0.70 for 1000 words

### 8.2 Function Word Patterns

**AI Characteristic Distribution**:

- Higher frequency of articles (the, a, an)
- More frequent use of "that" as connector
- Overuse of "which" in relative clauses
- Specific preposition preferences (of, in, to)

### 8.3 Punctuation Patterns

**AI Tendencies**:

- Comma usage follows grammatical rules strictly
- Rare use of em-dashes, semicolons, or ellipses
- No stylistic punctuation variation
- Parenthetical asides rare or formulaic

**Human Variation**:

- Strategic punctuation for rhythm and emphasis
- Em-dashes for informal asides
- Semicolons for nuanced connections
- Ellipses for trailing thoughts...

---

## Detection Scoring Models

### GPTZero Methodology

**Primary Metrics**:

1. **Perplexity** - Measures at sentence level
   - High perplexity (unpredictable) → Human
   - Low perplexity (predictable) → AI

2. **Burstiness** - Measures sentence length variation
   - High burstiness (varied) → Human
   - Low burstiness (uniform) → AI

**Scoring**:

- Analyzes both metrics across entire document
- Flags sections with consistently low scores
- Reports per-paragraph probability scores

### Originality.AI Methodology

**Multi-Model Approach**:

- Checks against GPT-3, GPT-4, Claude, PaLM patterns
- Looks for model-specific fingerprints
- Assigns confidence score (0-100%)

**Thresholds**:

- 0-20%: Likely human
- 20-40%: Possibly AI-assisted
- 40-60%: Mixed/unclear
- 60-80%: Likely AI
- 80-100%: Highly likely AI

### Turnitin AI Detection

**Educational Focus**:

- Trained on academic writing patterns
- Flags whole-cloth AI generation
- Less sensitive to AI-assisted editing
- Reports AI probability percentage

**Known Limitations**:

- Higher false positive rate on non-native English speakers
- Struggles with heavily edited AI content
- Domain-specific writing can trigger false positives

---

## Evasion-Resistant Patterns

### Patterns That Remain Detectable

Even after humanization, these patterns may persist:

1. **Statistical Fingerprints**
   - Underlying probability distributions
   - Token selection patterns
   - N-gram frequencies

2. **Semantic Coherence Patterns**
   - Consistent logical structure
   - Absence of tangential thoughts
   - Predictable information architecture

3. **Consistency Patterns**
   - Uniform quality throughout
   - No typos or grammatical slips
   - Consistent voice/tone without drift

### Patterns Most Improved by Humanization

These respond well to humanization techniques:

1. **Vocabulary Patterns** - Highly responsive to replacement
2. **Sentence Variation** - Directly addressable through editing
3. **Voice/Authenticity** - Improved via personal touches
4. **Structural Patterns** - Fixed by converting lists, varying transitions

---

## Detection Confidence Factors

### High Confidence Detection Scenarios

Detectors are most confident when:

- Multiple pattern categories align (vocabulary + structure + tone)
- Patterns consistent across entire document
- Length > 500 words (more data for statistical analysis)
- Content type matches AI training data (explanatory, informational)

### Low Confidence Detection Scenarios

Detectors struggle with:

- Short texts < 200 words (insufficient data)
- Highly technical domain-specific content
- Creative or narrative writing
- Heavily humanized/edited AI content
- Mixed human-AI collaboration

---

## Implications for Humanization

### Priority 1: Address Statistical Patterns

**Why**: These are mathematically detectable and hard to mask
**Action**:

- Increase burstiness through sentence variation
- Boost perplexity through vocabulary diversification
- Break uniform patterns systematically

### Priority 2: Eliminate Vocabulary Markers

**Why**: Easiest for detectors to flag, easiest for humans to fix
**Action**:

- Remove all Tier 1 AI-characteristic words
- Minimize Tier 2 words
- Replace formulaic transitions

### Priority 3: Add Authenticity Signals

**Why**: AI lacks these; humans naturally include them
**Action**:

- Add personal perspective markers
- Include specific examples and details
- Acknowledge complexity and trade-offs
- Show domain expertise through practitioner signals

### Priority 4: Introduce Natural "Imperfections"

**Why**: Humans aren't perfectly consistent
**Action**:

- Vary voice/tone slightly across sections
- Mix contracted and expanded forms
- Allow some stylistic inconsistency
- Include conversational asides

---

## Testing for Detection Patterns

### Self-Assessment Checklist

Before publishing AI-assisted content, check:

**Vocabulary**:

- [ ] Search for all Tier 1 AI words (delve, leverage, robust, etc.)
- [ ] Count formulaic transitions (Furthermore, Moreover, Additionally)
- [ ] Check for hedge word stacking (may potentially, generally tends)

**Structure**:

- [ ] Measure sentence lengths in 3 sample paragraphs
- [ ] Calculate mean and standard deviation
- [ ] Count number of lists (should be < 3-4 per 1000 words)

**Voice**:

- [ ] Count personal perspective markers (I, we, you, in my experience)
- [ ] Check for specific examples vs. generic abstractions
- [ ] Verify emotional engagement appropriate to content

**Technical Depth**:

- [ ] Verify specific versions, tools, products mentioned
- [ ] Check for practitioner signals and trade-off discussions
- [ ] Ensure gotchas or edge cases addressed

### Automated Detection Tools (For Testing)

**Free Tools**:

- GPTZero (academic/educational)
- Copyleaks AI Content Detector
- Writer.com AI Content Detector

**Paid Tools**:

- Originality.AI (most comprehensive)
- Winston AI (enterprise-focused)
- Turnitin (educational sector)

**Note**: Use these to test your humanization effectiveness, not as primary quality measure

---

## Future Detection Evolution

### Emerging Detection Techniques

**Watermarking**:

- Some AI systems now embed statistical watermarks
- Subtle token selection patterns that persist through editing
- Currently limited deployment but growing

**Semantic Analysis**:

- Advanced NLP analyzing meaning structures
- Detecting AI-characteristic reasoning patterns
- Less focused on surface features

**Multi-Modal Analysis**:

- Analyzing consistency between text and claimed authorship
- Cross-referencing with author's prior writing
- Behavioral biometrics of writing process

### Humanization Implications

**Watermarks**: Difficult to remove without regeneration
**Semantic Analysis**: Addressable through voice customization and reasoning variation
**Multi-Modal**: Requires consistent authorial voice across works

---

## Ethical Considerations

### Detection vs. Quality

**Key Insight**: Detection patterns often correlate with quality issues

- AI vocabulary is often genuinely weaker writing
- Uniform sentences create boring rhythm
- Lack of voice reduces engagement
- Surface abstraction limits value

**Implication**: Humanization that improves quality is ethically sound; humanization purely for evasion is questionable

### Disclosure Norms

Different domains have different disclosure expectations:

- **Academic**: Full disclosure typically required
- **Technical writing**: Assistance acceptable, often not disclosed
- **Creative writing**: Varies by publisher/contest
- **Marketing**: AI assistance common, rarely disclosed
- **Journalism**: High disclosure expectations

---

## Related Resources

- **Tasks**: analyze-ai-patterns.md, humanize-post-generation.md
- **Data**: humanization-techniques.md
- **Checklists**: ai-pattern-detection-checklist.md

---

**Note**: This reference is based on research into detection systems as of 2025. Detection methodologies evolve continuously. The most sustainable approach is creating genuinely high-quality content that serves readers, not merely evading detection.

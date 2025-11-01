<!-- Powered by BMAD™ Core -->

# Extract Tone Patterns (Brownfield)

---

task:
id: extract-tone-patterns
name: Extract Tone Patterns from Existing Book
description: Analyze existing book chapters to extract voice, tone, and style patterns for maintaining consistency in new editions or added chapters
persona_default: technical-editor
inputs: - existing-chapters (multiple chapters for pattern accuracy) - book-context (title, edition, publisher)
steps: - Load multiple existing chapters (minimum 3-5 for accuracy) - Analyze voice characteristics (formal/casual, active/passive, perspective) - Extract common phrase patterns (transitions, introductions, conclusions) - Analyze code comment style and density - Identify formality indicators (contractions, vocabulary, sentence complexity) - Extract author personality markers (humor, encouragement, directness) - Document excluded patterns (what author avoids) - Generate extracted-tone-patterns.md document
output: extracted-tone-patterns.md
use_case: brownfield

---

## Purpose

Extract tone and voice patterns from existing published book chapters to ensure new content (2nd edition chapters, added sections, updated examples) matches the established style. This is the **brownfield equivalent** of define-book-tone.md—for books that already exist rather than starting from scratch.

## When to Use

**Use this task when:**

- Writing new chapters for 2nd/3rd edition of existing book
- Adding new content to existing technical book
- Multiple authors need to match original author's voice
- Updating book sections while preserving original tone
- Publisher requires consistency with previous edition
- Original tone-specification.md doesn't exist (older books)

**Do NOT use for:**

- New books (use define-book-tone.md instead)
- Books where you want to intentionally CHANGE tone for new edition
- Single-chapter updates (just read the chapter for style)

## Prerequisites

Before starting this task:

- **Multiple existing chapters available** (minimum 3-5 chapters for accurate pattern extraction)
- **Chapters represent book's typical style** (not preface, not highly technical appendix)
- **Access to published or final draft versions** (not early drafts)
- **Book context known** (edition, publisher, target audience)
- **Authority to analyze content** (you have the book, rights to reference it)

## Workflow Steps

**Note:** This task references config paths (e.g., {{config.manuscript.*}}). Load `.bmad-technical-writing/config.yaml` at the start to resolve these paths, or use defaults: `manuscript/{type}`, `code-examples`.

### 1. Select Representative Chapters

Choose chapters that best represent the book's typical voice:

**Selection Criteria:**

**Include (3-5 chapters minimum):**

- Middle chapters (not introduction, not appendix)
- Teaching chapters (explanations + code + exercises)
- Chapters you consider "well-written" examples of book's voice
- Chapters from different sections (early, middle, late) to detect any drift
- Chapters representing core book content (not edge cases)

**Avoid:**

- Preface or foreword (often different tone)
- Highly mathematical/formal sections (may not represent general tone)
- Appendices or reference sections (usually more terse)
- Guest-authored chapters (if different voice)
- Known problematic chapters (poorly edited, inconsistent)

**Example Selection:**

For "Kubernetes in Action, 2nd Edition":

- Chapter 3: "Deploying your first application" (practical teaching)
- Chapter 7: "Managing pod networking" (technical depth)
- Chapter 11: "Security best practices" (mixed practical + conceptual)
- Chapter 15: "Production troubleshooting" (real-world scenarios)

**Rationale:** 4 chapters covering range of topics, all teaching-focused, representing typical book voice.

### 2. Analyze Voice Characteristics

Examine how the author communicates:

**Perspective Analysis:**

Read through chapters and identify:

- **First person singular:** "I recommend", "In my experience", "I've found"
- **First person plural:** "We'll deploy", "Let's examine", "We can see"
- **Second person:** "You'll implement", "You can use", "Your application"
- **Third person:** "Developers implement", "The system performs", "One should consider"
- **Mixed:** Document when different perspectives are used and why

**Example Pattern:**

```markdown
**Extracted Perspective Pattern:**

- Primary: Second person ("You'll deploy the application")
- Secondary: First person plural in collaborative contexts ("Let's troubleshoot this together")
- Rare: Third person only for general statements ("Most teams prefer...")
- Never: First person singular (author avoids "I think", keeps focus on reader)
```

**Active vs. Passive Voice:**

Analyze sentence construction:

- Count active voice usage: "Deploy the application", "You configure the service"
- Count passive voice usage: "The application is deployed", "The service is configured"
- Calculate ratio: ~80% active, ~20% passive (example)
- Note when passive is used: Often for background processes, system actions

**Example Pattern:**

```markdown
**Voice Construction:**

- Active voice dominant: ~85% of sentences
- Passive voice for system actions: "The pod is scheduled by Kubernetes"
- Passive voice avoided for reader actions: NOT "The configuration file should be edited by you"
- Pattern: Reader actions always active, system actions may be passive
```

**Formality Level:**

Map to 1-5 scale:

- Count contractions per 1000 words
- Analyze vocabulary (simple/technical/academic)
- Examine sentence complexity (average words per sentence)
- Note formality indicators

**Example Analysis:**

```markdown
**Formality Level: 3 (Professional/Conversational)**

Evidence:

- Contractions: ~15 per 1000 words ("you'll", "we'll", "it's")
- Vocabulary: Technical but accessible (not overly academic)
- Average sentence length: 18 words (moderately complex)
- Formality indicators: Uses "Let's" frequently, explains jargon, occasional humor
```

### 3. Extract Common Phrase Patterns

Identify recurring language patterns:

**Chapter Introductions:**

Document how chapters typically open:

```markdown
**Introduction Patterns (extracted from 4 chapters):**

Pattern 1 (most common):
"In this chapter, you'll [learn/implement/explore] [topic]. By the end, you'll be able to [concrete outcome]."

Example: "In this chapter, you'll implement service networking. By the end, you'll be running a multi-service application with secure communication."

Pattern 2 (transitions from previous):
"Now that you've [previous chapter topic], it's time to [current chapter topic]."

Example: "Now that you've deployed your first pod, it's time to explore how Kubernetes schedules and manages multiple pods."

Pattern 3 (problem-solution):
"[Common problem/question]. In this chapter, you'll discover [solution/answer]."

Example: "How do multiple services discover and communicate with each other? In this chapter, you'll discover Kubernetes networking fundamentals."
```

**Section Transitions:**

Extract transition phrases used between sections:

```markdown
**Transition Patterns:**

Between related concepts:

- "Building on this..."
- "Now that you understand [X], let's explore [Y]"
- "This leads us to..."

From theory to practice:

- "Let's put this into practice"
- "Time to see this in action"
- "Let's implement this concept"

From explanation to code:

- "Here's how to implement this:"
- "The following example demonstrates:"
- "Let's write the code:"

From problem to solution:

- "Here's how to fix this:"
- "The solution is straightforward:"
- "You can resolve this by..."
```

**Chapter Conclusions:**

How chapters typically end:

```markdown
**Conclusion Patterns:**

Summary format:
"In this chapter, you [learned/implemented/explored] [topic 1], [topic 2], and [topic 3]. You're now ready to [next step/next chapter]."

Forward-looking:
"You now have [skill/knowledge]. In the next chapter, we'll [future topic] to [goal]."

Encouragement:
"You've made significant progress. [Specific achievement]. Keep going—[what's next] will build directly on this foundation."
```

**Common Technical Explanations:**

Identify how concepts are typically explained:

```markdown
**Explanation Pattern:**

1. State concept: "A Service is a Kubernetes abstraction for network access."
2. Explain why it matters: "Without Services, pods couldn't reliably communicate."
3. Provide concrete example: "Here's a Service definition for our web application:"
4. Show code/config
5. Explain key parts: "The `selector` field determines which pods receive traffic."
6. Common pitfall: "Don't confuse Services with Ingress—they serve different purposes."
```

### 4. Analyze Code Comment Style

Extract code commentary patterns:

**Comment Density Analysis:**

```markdown
**Code Comment Density:**

- Average: 1 comment per 3-4 lines of code
- Complex sections: 1 comment per 1-2 lines
- Simple configuration: 1 comment per 5-7 lines
- Never: Completely uncommented code blocks

**Pattern:** Comments for "why" not "what" unless syntax is non-obvious
```

**Comment Style Examples:**

Extract actual comment styles from existing code:

````markdown
**Comment Style Patterns:**

Style 1 - Explanation (most common):

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service # Service name used by other pods for discovery
spec:
  selector:
    app: web # Routes traffic to pods with this label
  ports:
    - port: 80 # External port clients connect to
      targetPort: 8080 # Internal port the app listens on
```

Style 2 - Warning/Caution:

```yaml
# IMPORTANT: Don't change this selector without updating pod labels
selector:
  app: web
```

Style 3 - Context/Rationale:

```yaml
# We use ClusterIP here because this service is internal-only
type: ClusterIP
```

Style 4 - Step-by-step for complex logic:

```python
# Step 1: Load configuration from environment
config = load_env_config()

# Step 2: Initialize database connection pool
db = connect_database(config)

# Step 3: Start background worker threads
start_workers(db, config.worker_count)
```
````

**Comment Tone:**

```markdown
**Comment Tone Characteristics:**

- Formality: Matches prose (Level 3, conversational)
- Contractions: Occasionally used ("Don't", "It's")
- Directness: Clear and instructive ("Change this", "Note that")
- Encouragement: Rare in comments (reserved for prose)
- Technical depth: Explains WHY, assumes reader knows WHAT
```

### 5. Identify Formality Indicators

Quantify formality decisions:

**Contraction Usage:**

```markdown
**Contractions Analysis (1000-word sample from each chapter):**

Chapter 3: 12 contractions (you'll, we'll, don't, it's)
Chapter 7: 15 contractions
Chapter 11: 10 contractions
Chapter 15: 14 contractions

Average: 12.75 per 1000 words = Moderate use

**Most common:**

- "you'll" (future actions)
- "we'll" (collaborative actions)
- "don't" (warnings/cautions)
- "it's" (explanations)

**Rarely used:**

- "shouldn't" (prefers "avoid" or "don't")
- "would've" (too casual)

**Never used:**

- "gonna", "wanna" (too informal)
```

**Vocabulary Complexity:**

```markdown
**Vocabulary Patterns:**

Technical terms:

- Used directly with brief explanation on first use
- Example: "Kubernetes uses etcd (a distributed key-value store) for cluster state."
- No dumbing down: "pod", "ingress", "daemonset" used throughout (not "container group", etc.)

Explanatory style:

- Prefers "Because [reason]" over "due to the fact that"
- Uses "use" not "utilize"
- Uses "help" not "facilitate"
- Practical vocabulary, not academic

Jargon approach:

- Kubernetes-specific terms: Used freely (assumes reader learning K8s)
- General tech terms: Defined briefly on first use
- Acronyms: Spelled out once, then abbreviated
```

**Sentence Structure:**

```markdown
**Sentence Complexity:**

Average sentence length: 16-18 words (moderately simple)
Average paragraph length: 3-4 sentences

Patterns:

- Short sentences for emphasis: "This is critical."
- Longer sentences for explanation: "The Service abstraction provides a stable IP address and DNS name for accessing a set of pods, even as individual pods are created and destroyed."
- Varies length deliberately for readability
- Avoids run-on sentences
```

### 6. Extract Author Personality Markers

Identify unique voice elements:

**Humor/Personality:**

```markdown
**Personality Characteristics:**

Humor frequency: Occasional (1-2 instances per chapter)
Humor style: Light technical humor, self-deprecating

Examples extracted:

- "If you're thinking this seems complicated, you're right. Kubernetes doesn't do simple."
- "After a 3am debugging session, you'll appreciate this logging configuration."
- "Yes, the acronym TLS actually makes sense. Rare for our industry."

Personality markers:

- Real-world war stories: References "production incidents", "debugging sessions"
- Empathy: Acknowledges difficulties ("This is confusing at first")
- Experience: "After deploying hundreds of applications..."
- Pragmatism: "In theory, X. In practice, Y. Use Y."
```

**Encouragement Approach:**

```markdown
**Encouragement Style:**

Frequency: Moderate (2-3 instances per chapter, usually at milestones)
Style: Confident and matter-of-fact, not cheerleading

Patterns:

- Progress acknowledgment: "You've now deployed a production-ready service."
- Capability building: "You can now troubleshoot networking issues independently."
- Forward-looking: "With this foundation, you're ready for advanced topics."

Avoids:

- ❌ "Great job!" or "Awesome!" (too cheerful)
- ❌ "This is easy!" (dismissive of legitimate difficulty)
- ❌ "Don't worry!" (patronizing)

Uses:

- ✓ "You've mastered [specific skill]"
- ✓ "This prepares you for [next challenge]"
- ✓ "You now understand [complex concept]"
```

**Directness/Authority:**

```markdown
**Authority Tone:**

Prescriptive language:

- Uses "Don't" frequently: "Don't hard-code credentials"
- Offers clear guidance: "Use environment variables for configuration"
- States best practices directly: "Always run security scanning before deployment"
- Explains rationale: "Use X because Y. Avoid Z because it causes W."

Avoids hedging:

- Rare: "might want to consider possibly"
- Common: "Use this approach"
- When uncertain: Explicit: "This depends on your use case. If [condition], choose [option]."

Authority without arrogance:

- Acknowledges complexity: "This is genuinely difficult"
- Admits limitations: "Kubernetes doesn't handle this well"
- Shares experience: "I've learned this through painful production issues"
```

### 7. Document Excluded Patterns

Identify what the author intentionally AVOIDS:

**Anti-Patterns Found:**

```markdown
**Excluded Tones/Patterns (What Author Doesn't Do):**

❌ **Overly Academic:**

- Never uses: "herein", "aforementioned", "utilize", "facilitate"
- Avoids passive academic construction: "It is recommended that..."
- Skips: "This paper presents", "We propose", "In conclusion"

❌ **Marketing Hype:**

- Never: "Revolutionary", "game-changing", "amazing", "incredible"
- Avoids: Exclamation points (except in warnings)
- Skips: Superlatives without evidence

❌ **Apologetic/Uncertain:**

- Never: "I think maybe you could possibly..."
- Avoids: "Sorry for the complexity"
- Skips: Unnecessary hedging

❌ **Condescending:**

- Never: "Obviously", "clearly", "simply", "just" (dismissive usage)
- Avoids: "Even beginners know"
- Skips: "This is trivial"

❌ **Overly Casual:**

- Never: "gonna", "wanna", "yeah"
- Avoids: Excessive exclamation points
- Skips: Internet slang or memes

❌ **Excessive Formality:**

- Never: "One must ensure", "It is imperative that"
- Avoids: Completely eliminating contractions
- Skips: Latin phrases (except common tech terms like "e.g.")
```

### 8. Generate extracted-tone-patterns.md Document

Compile analysis into structured document:

**Document Structure:**

```markdown
# Extracted Tone Patterns: [Book Title]

## Book Context

- **Title:** [Book title and edition]
- **Author:** [Author name]
- **Publisher:** [Publisher]
- **Edition:** [1st/2nd/3rd]
- **Publication Date:** [Year]
- **Chapters Analyzed:** [List chapters used for extraction]
- **Analysis Date:** [Date]
- **Extracted By:** [Your name]

## Voice Profile

### Perspective

[First/second/third person patterns]

### Active vs. Passive Voice

[Ratio, patterns, when each is used]

### Formality Level

**Level [1-5]: [Description]**
[Evidence, examples, metrics]

## Common Phrases and Patterns

### Chapter Introductions

[Patterns with examples]

### Section Transitions

[Transition phrases extracted]

### Chapter Conclusions

[Conclusion patterns]

### Technical Explanations

[Explanation structure patterns]

## Code Comment Style

### Comment Density

[Average comments per code lines]

### Comment Patterns

[Examples of actual comment styles]

### Comment Tone

[Formality, characteristics]

## Formality Indicators

### Contractions

[Frequency, which ones used, which avoided]

### Vocabulary

[Technical depth, complexity, style]

### Sentence Structure

[Length, complexity, variety]

## Author Personality Markers

### Humor and Personality

[Examples, frequency, style]

### Encouragement Approach

[How author motivates readers]

### Authority and Directness

[How author provides guidance]

## Excluded Patterns (Anti-Patterns)

### What Author Avoids

[List of excluded tones with examples]

## Usage Guidance for New Content

### When Writing New Chapters

[How to apply these patterns]

### Matching This Tone

[Specific guidance for consistency]

### Common Pitfalls to Avoid

[What would break tone consistency]

## Extracted Examples for Reference

### Example 1: Typical Chapter Introduction

[Full example]

### Example 2: Code with Comments

[Full example with commentary]

### Example 3: Technical Explanation

[Full example]

### Example 4: Chapter Conclusion

[Full example]

## Version History

| Date   | Analyst | Chapters Added | Notes              |
| ------ | ------- | -------------- | ------------------ |
| [Date] | [Name]  | [Chapters]     | Initial extraction |
```

**Save Location:**

Save as `extracted-tone-patterns.md` in project documentation directory (typically `docs/` or `{{config.manuscript.planning}}/`)

### 9. Validate Extraction Quality

Ensure patterns are actionable and accurate:

**Quality Checks:**

- [ ] Patterns based on minimum 3 chapters (preferably 5+)
- [ ] Patterns are specific, not generic ("uses 'Let's' frequently" not "friendly tone")
- [ ] Examples provided for each pattern (real excerpts from book)
- [ ] Formality level quantified with evidence (contraction count, sentence length)
- [ ] Voice characteristics clearly defined (not vague "conversational")
- [ ] Code comment examples included (minimum 3 different styles)
- [ ] Anti-patterns documented (what to avoid as important as what to include)
- [ ] Extracted passages can serve as "write like THIS" models

**Validation Test:**

Can you write a new paragraph on a technical topic using ONLY the guidance in extracted-tone-patterns.md? If not, patterns aren't specific enough.

## Success Criteria

✅ **Extraction is complete when:**

- Minimum 3-5 chapters analyzed (more is better)
- extracted-tone-patterns.md document generated
- Voice characteristics clearly defined (perspective, active/passive, formality)
- Minimum 10 phrase patterns extracted with examples
- Code comment style documented with examples
- Formality level quantified (contraction count, vocabulary analysis)
- Author personality markers identified (humor, encouragement, directness)
- Minimum 5 anti-patterns documented (excluded tones)
- Real book excerpts provided as reference examples
- Patterns are specific and actionable (not vague)

✅ **Quality indicators:**

- Another writer could match this tone using this document
- Patterns reflect book's actual voice, not analyst's interpretation
- Evidence supports each pattern (examples, metrics)
- Anti-patterns prevent common mismatches

## Integration Points

**Output To:**

- **apply-tone-patterns.md** - Uses extracted patterns to guide new chapter writing
- **copy-edit-chapter.md** - Validates new content against extracted patterns
- **tone-consistency-checklist.md** - Uses patterns as validation reference

**Complementary With:**

- **analyze-existing-book.md** - Extracts structure and technical patterns (not tone)
- Together provide complete brownfield book analysis

## Important Notes

**Accuracy Requires Multiple Chapters:**

- Single chapter may have anomalies or one-off experiments
- 3 chapters minimum, 5+ ideal for reliable patterns
- Include chapters from different book sections (early, middle, late)

**Avoid Over-Interpretation:**

- Extract what's actually there, not what you think should be there
- If author rarely uses humor, document that (don't force humor into patterns)
- Patterns should be descriptive, not prescriptive improvements

**Edition Updates:**

- Extract from CURRENT edition (not outdated versions)
- If tone has evolved across editions, note that explicitly
- New edition may intentionally refine tone (document changes)

**Publisher Context:**

- Publisher may have influenced original tone (O'Reilly, Manning, PacktPub)
- If staying with same publisher, extracted patterns likely align with expectations
- If changing publishers, may need to adjust some patterns

**Complementary to define-book-tone.md:**

- Brownfield (extract-tone-patterns.md): Analyze existing → maintain consistency
- Greenfield (define-book-tone.md): Define from scratch → establish new voice
- Both create guidance documents for consistent writing

## Related Tasks

- **apply-tone-patterns.md** - Apply extracted patterns to new content
- **define-book-tone.md** - Greenfield alternative (new books)
- **analyze-existing-book.md** - Extracts structure/technical patterns (complementary)
- **copy-edit-chapter.md** - Validates tone consistency

## Related Checklists

- **tone-consistency-checklist.md** - Validates extracted patterns applied correctly

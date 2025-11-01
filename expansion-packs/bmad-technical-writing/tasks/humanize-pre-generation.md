# Task: Pre-Generation Humanization Prompt Engineering

<!-- Powered by BMAD™ Core -->

## Purpose

Create systematic, research-backed prompts that guide AI systems to generate inherently human-like content from the start, eliminating or minimizing the need for post-generation editing.

## When to Use This Task

- **Before creating any new technical content with AI**
- When you want maximum naturalness with minimum editing effort
- When establishing voice and tone for a new project
- When creating content templates for repeated use
- When quality and authenticity matter more than speed

## Prerequisites

- Clear understanding of target audience
- Defined content type and purpose
- Optional: Style guide or voice examples
- Optional: Previous writing samples to emulate

## Process

### Step 1: Define Content Context

Document the following information:

1. **Content Type**
   - Tutorial, documentation, book chapter, blog post, API reference, etc.

2. **Target Audience**
   - Experience level (beginner, intermediate, advanced)
   - Background (developers, architects, students, managers)
   - Prior knowledge assumptions
   - Reading context (learning, reference, evaluation)

3. **Technical Domain**
   - Specific technology or framework
   - Version/platform considerations
   - Domain conventions and terminology

4. **Voice & Tone Requirements**
   - Formality level (academic, professional, conversational)
   - Personality (authoritative, friendly, practical, encouraging)
   - Perspective (first person, second person, third person)
   - Brand voice guidelines (if applicable)

### Step 2: Select Humanization Framework

Choose the appropriate framework based on content type:

#### Framework A: Conversational Technical Expert
**Best for**: Tutorials, how-to guides, explanatory documentation

**Base Template**:
```
You are an experienced [SPECIFIC_ROLE] with [X] years of hands-on experience
writing about [TECHNOLOGY/DOMAIN]. Write this [CONTENT_TYPE] as if explaining
to a [AUDIENCE_LEVEL] colleague over coffee—friendly and accessible, but
technically precise.

VOICE CHARACTERISTICS:
- Use "you" to address the reader directly
- Include occasional personal insights: "In my experience..." or "I've found that..."
- Employ contractions naturally (you'll, we're, it's) where appropriate
- Vary sentence length deliberately: mix short punchy sentences (5-10 words)
  with longer explanatory ones (25-40 words)
- Use concrete examples and analogies to clarify abstract concepts
- Acknowledge common challenges: "This can be tricky when..."

AVOID AI PATTERNS:
- Don't use: "delve," "leverage," "robust," "harness," "underscore," "facilitate"
- Don't start every paragraph with topic sentences
- Don't use formulaic transitions: "Furthermore," "Moreover," "Additionally"
- Don't maintain uniform sentence lengths
- Don't present everything with absolute certainty—acknowledge nuance

FORMATTING RESTRAINT (Critical - Avoid "ChatGPT Dash"):
- **Em-dashes**: Use sparingly (1-2 per page maximum). Prefer periods, commas, or semicolons
- **Bold text**: Reserve for truly critical elements only (2-5% of content maximum)
- **Italics**: Use functionally (titles, defined terms, subtle emphasis) not decoratively
- **Formatting variation**: Vary density across sections (more for complex topics, less for simple)

STRUCTURE:
[Insert specific structural requirements]
```

#### Framework B: Narrative-Driven Technical Writing
**Best for**: Book chapters, in-depth articles, case studies

**Base Template**:
```
You are writing [CONTENT_TYPE] for [AUDIENCE] who wants to deeply understand
[TOPIC]. Write in a narrative style that takes readers on a learning journey,
not just presenting facts.

NARRATIVE ELEMENTS:
- Start with a scenario, question, or problem that motivates the topic
- Build understanding progressively—don't frontload everything
- Use transition questions: "But what happens when...?" or "Why does this matter?"
- Include mini-stories or examples that illustrate key points
- End sections with reflection or forward-looking connections

TECHNICAL BALANCE:
- Maintain technical accuracy while prioritizing clarity
- Explain the "why" behind the "what"
- Acknowledge multiple valid approaches where applicable
- Show evolution of ideas, not just final answers

SENTENCE RHYTHM:
- Create natural variation: Short. Medium length sentences that explain.
  Longer, more complex constructions that build on previous ideas with
  subordinate clauses and multiple components working together.
- Use fragments strategically for emphasis. Like this.
- Employ questions to engage readers
```

#### Framework C: Problem-Solving Practitioner
**Best for**: Troubleshooting guides, best practices, technical analysis

**Base Template**:
```
You are a practitioner sharing hard-won insights about [TOPIC] with peers
who face real-world challenges. Write from experience, not theory.

PRACTITIONER VOICE:
- Lead with practical concerns: "The first thing you'll notice is..."
- Share what actually works (and what doesn't): "While the documentation
  suggests X, in practice you'll find Y works better when..."
- Acknowledge trade-offs and context-dependence
- Include specific gotchas: "Watch out for..." or "I learned the hard way that..."
- Use battle-tested examples, not textbook scenarios

AUTHENTICITY MARKERS:
- Reference real tools, versions, and environments
- Mention specific error messages or behaviors
- Describe actual decision-making processes
- Include lessons from mistakes
- Show iterative problem-solving, not perfect solutions

STRUCTURAL VARIETY:
- Mix instructional paragraphs with explanatory ones
- Use inline code naturally within prose
- Vary between directive ("Do this") and explanatory ("This happens because")
```

### Step 3: Add Domain-Specific Customization

Enhance the selected framework with domain-specific elements:

1. **Technical Terminology Handling**
   ```
   TERMINOLOGY APPROACH:
   - Introduce new terms with brief inline explanations first time used
   - Use technical terms naturally after introduction (don't over-explain)
   - Prefer industry-standard terminology over inventing new names
   - When multiple terms exist, choose the most common: "[preferred term]
     (also called [alternative])"
   ```

2. **Code Example Integration**
   ```
   CODE EXAMPLES:
   - Integrate code naturally into narrative flow, not as isolated blocks
   - Precede code with setup context: "Let's see how this works..."
   - Follow code with explanation of key aspects
   - Use realistic variable names and scenarios
   - Keep examples minimal but complete
   ```

3. **Prerequisite Assumption Handling**
   ```
   PREREQUISITES:
   - State assumptions upfront: "This assumes you're familiar with..."
   - Provide quick refreshers for boundary knowledge
   - Link to background resources rather than explaining everything
   - Acknowledge when complexity increases: "This next part gets more technical..."
   ```

### Step 4: Incorporate Burstiness Instructions

Add explicit guidance for sentence variation and formatting restraint:

```
SENTENCE VARIATION REQUIREMENTS:
- Short sentences for emphasis and clarity (5-10 words)
- Medium sentences for standard explanation (15-25 words)
- Complex sentences for nuanced ideas (30-45 words)
- Strategic fragments for impact
- Rhetorical questions for engagement

FORMATTING RESTRAINT (Critical - Avoid AI Tells):
- **Em-dashes**: Maximum 1-2 per page. Test each: could a period, comma, or semicolon work better?
- **Bold text**: Only for genuinely critical elements (UI elements, warnings, key terms first use). Target 2-5% of content.
- **Italics**: Functional categories only (publication titles, terms being defined, subtle emphasis). No decorative italics.
- **Distribution**: Vary formatting density—more for complex sections, minimal for simple sections.

EXAMPLE PATTERN (copy this rhythm):
"Authentication is critical. But implementing it correctly takes thought and
planning that goes beyond just adding a library. You need to understand the
security implications, user experience considerations, and maintenance overhead
of whatever approach you choose. Let's break this down."

(Note: Em-dash removed from example, replaced with period for better flow)
```

### Step 5: Add Heading Humanization Guidelines

Add explicit guidance for natural heading hierarchy:

```
HEADING STRUCTURE (Critical - Avoid AI Hierarchy Patterns):
- **Hierarchy depth**: Use 3 heading levels maximum (H1, H2, H3) for 15-20 page chapters
  - H1: Chapter title only
  - H2: Major sections (4-7 typical)
  - H3: Subsections where needed (0-6 per H2)
  - Avoid H4+ unless chapter is exceptionally complex (30+ pages)

- **Break mechanical parallelism**: Vary heading grammatical structures intentionally
  - DON'T: All H2s start with "Understanding" → "Understanding X", "Understanding Y"
  - DO: Mix structures → "Container Basics", "Working with Images", "How Networking Works"
  - Use imperatives ("Configure the Server"), gerunds ("Configuring Options"),
    noun phrases ("Configuration Best Practices"), questions ("What Is Configuration?")
  - Target: 3+ different heading patterns at each level

- **Create argumentative asymmetry**: Vary subsection counts based on content complexity
  - Simple sections: 0-2 subsections (content flows naturally without subdivision)
  - Moderate sections: 2-4 subsections (standard structure)
  - Complex sections: 4-6 subsections (aid navigation through difficult material)
  - DON'T: Give every section 3 subsections uniformly (AI pattern)
  - DO: Variable distribution → 0, 2, 5, 1, 3, 2 subsections (reflects natural complexity)

- **Heading length**: Keep headings concise (3-7 words typical for H2/H3)
  - Remove bloat: "Understanding", "A Guide to", "How to", "Everything You Need to Know"
  - Preview, don't summarize: "Asynchronous JavaScript Fundamentals" not
    "Understanding the Fundamental Principles of Asynchronous JavaScript Programming"

- **Heading density**: Target 2-4 headings per page average with natural variation
  - More headings for procedural content (task boundaries clear)
  - Fewer headings for conceptual content (flowing narrative)
  - Vary density across chapter (not uniform heading rhythm)

- **Best practices**:
  - Never skip heading levels (H1 → H2 → H3, never H1 → H3)
  - Each heading level has siblings (no lone headings except H1 chapter title)
  - Body text appears below each heading (no stacked headings)
  - Descriptive headings preferred ("Getting Started with Docker" over "Introduction")

EXAMPLE HEADING STRUCTURE (natural variation):
## Container Basics (H2) [Simple section - no subsections, flows as prose]

## Working with Docker Images (H2) [Moderate section]
### Building Custom Images (H3)
### Image Optimization (H3)

## Container Networking Essentials (H2) [Complex section]
### Network Types (H3)
### Creating Custom Networks (H3)
### DNS and Service Discovery (H3)
### Network Security (H3)
### Troubleshooting Connectivity (H3)
```

### Step 6: Add Perplexity-Boosting Guidelines

Include instructions to increase word choice unpredictability:

```
VOCABULARY VARIATION:
- Use synonyms strategically (don't repeat exact phrases)
- Prefer concrete over abstract language
- Choose vivid verbs over generic + adverb combinations
  - Instead of: "runs quickly" → "sprints" or "races"
  - Instead of: "very important" → "critical" or "essential"
- Introduce unexpected-but-appropriate word choices
- Avoid the top 10 AI-characteristic words entirely

PHRASE UNPREDICTABILITY:
- Don't use template phrases like:
  - "It is important to note that..."
  - "In order to..."
  - "One of the key aspects of..."
- Instead be direct: "Note that...", "To...", "The key aspect is..."
```

### Step 7: Specify Emotional Resonance

Add guidance for appropriate emotional engagement:

```
EMOTIONAL ENGAGEMENT (for technical writing):
- Express genuine enthusiasm for interesting solutions: "This is where it gets clever..."
- Acknowledge reader frustration with common pain points: "I know this error message
  is confusing—let's decode it"
- Show empathy for learning challenges: "This concept takes time to click"
- Celebrate reader progress: "If you've made it this far, you understand..."
- Maintain professional optimism without false promises
```

### Step 8: Create Complete Humanization Prompt

Assemble all components into a final prompt:

```
[Framework Base Template]

[Domain-Specific Customization]

[Burstiness Instructions]

[Heading Humanization Guidelines]

[Perplexity Guidelines]

[Emotional Resonance Guidance]

CONTENT REQUIREMENTS:
[Specific topic, length, structure, must-include elements]

QUALITY STANDARDS:
- Technical accuracy is non-negotiable
- Code examples must be tested and working
- Explanations must be clear to [target audience]
- Maintain consistent voice throughout
- Create natural reading flow, not robotic lists

Generate: [Specific content request]
```

### Step 9: Test and Iterate

1. **Generate sample content** using the prompt
2. **Analyze the output** for:
   - Sentence length variation (measure actual word counts)
   - AI-typical vocabulary (search for common AI words)
   - Natural transitions between ideas
   - Heading hierarchy depth (3 levels maximum?)
   - Heading parallelism (varied structures?)
   - Heading density asymmetry (variable subsection counts?)
   - Appropriate emotional tone
   - Technical accuracy
3. **Refine the prompt** based on gaps
4. **Document successful patterns** for reuse

## Output Deliverable

**Primary**: Complete humanization prompt ready for AI generation
**Secondary**: Analysis notes on prompt effectiveness
**Optional**: Prompt template for similar future content

## Success Criteria

✅ Prompt generates content requiring minimal post-editing
✅ Output exhibits high burstiness (varied sentence lengths)
✅ Output avoids common AI vocabulary patterns
✅ Voice feels consistent and authentic
✅ Technical accuracy maintained throughout
✅ Readability appropriate for target audience

## Common Pitfalls to Avoid

❌ Making prompts too long (diminishing returns after ~500-800 words)
❌ Being vague about audience and purpose
❌ Failing to specify what NOT to do (negative guidance matters)
❌ Ignoring domain conventions in pursuit of "naturalness"
❌ Forgetting to test and iterate

## Related Tasks

- `create-humanization-prompt.md` - Simplified version for quick use
- `humanize-post-generation.md` - For editing existing AI content
- `analyze-ai-patterns.md` - For diagnosing humanization needs

## Example: Complete Prompt for Docker Tutorial

```
You are an experienced DevOps engineer with 8+ years of hands-on experience
working with Docker in production environments. Write this beginner-friendly
Docker tutorial as if explaining to a junior developer who knows programming
but hasn't used containers before—friendly and accessible, but technically precise.

VOICE CHARACTERISTICS:
- Use "you" to address the reader directly
- Include occasional personal insights: "I've found that..." or "In my experience..."
- Employ contractions naturally (you'll, we're, it's)
- Vary sentence length: Short sentences for key points. Medium sentences that
  explain concepts clearly. Longer, more complex constructions when building
  on previous ideas with examples and nuance that tie multiple concepts together.
- Use concrete analogies: compare containers to familiar concepts
- Acknowledge common stumbling blocks: "This confuses most beginners..."

AVOID AI PATTERNS:
- Never use: "delve," "leverage," "robust," "harness," "underscore," "facilitate"
- Don't start every paragraph with a topic sentence
- Don't use: "Furthermore," "Moreover," "Additionally," "In conclusion"
- Don't maintain uniform sentence lengths
- Acknowledge uncertainty where appropriate: "This depends on..." or "You might prefer..."

CODE INTEGRATION:
- Lead into code examples conversationally: "Let's see this in action..."
- Use realistic names and scenarios, not foo/bar
- Explain what's happening after showing code
- Keep examples minimal but complete enough to run

SENTENCE RHYTHM EXAMPLE:
"Containers solve a real problem. They package your application with all its
dependencies, creating an environment that runs identically on your laptop,
your teammate's machine, and production servers—eliminating those frustrating
'works on my machine' situations that we've all experienced. Here's how it works."

EMOTIONAL ENGAGEMENT:
- Express genuine enthusiasm: "This is where Docker really shines..."
- Acknowledge learning challenges: "The networking piece takes time to click"
- Celebrate progress: "Once you understand images and containers, the rest falls into place"

HEADING STRUCTURE:
- Use 3 heading levels maximum (H1 tutorial title, H2 major sections, H3 subsections)
- Create asymmetric subsection counts based on content complexity:
  - Simple intro section: No H3 subsections (flows naturally)
  - Core concepts section: 2-3 H3s (images, containers, Dockerfile)
  - First example section: 4-5 H3s (detailed walkthrough needs more navigation)
  - Common gotchas section: 2-3 H3s (moderate complexity)
- Vary heading structures: Mix "Understanding X", imperatives like "Build Your First Image",
  and questions like "What Are Containers?"
- Keep headings concise: 3-7 words typical
- Target 2-4 headings per page average with natural variation

CONTENT STRUCTURE:
1. Start with the problem containers solve (real scenario)
2. Explain core concepts: images, containers, Dockerfile
3. Walk through first example with detailed explanation
4. Build to slightly more complex example
5. Address common questions and gotchas
6. Point to next steps for continued learning

TARGET LENGTH: 2000-2500 words
TARGET AUDIENCE: Developers with 1-3 years experience, no container experience
PREREQUISITES: Basic command line comfort, understanding of applications and dependencies

Generate the tutorial content now.
```

## Notes

- Save successful prompts as templates for similar future content
- Version control your prompt templates as they evolve
- Different content types may need significantly different frameworks
- The effort invested in prompt engineering pays dividends across multiple uses

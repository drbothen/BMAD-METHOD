# Task: Post-Generation Humanization Editing

<!-- Powered by BMAD™ Core -->

## Purpose

Transform AI-generated technical content into natural, human-sounding writing through systematic editing workflows that improve perplexity, burstiness, voice consistency, and emotional resonance while preserving technical accuracy.

## When to Use This Task

- **After AI has generated initial content** that needs humanization
- When content feels robotic, formulaic, or obviously AI-generated
- When preparing AI-assisted drafts for publication
- When quality assurance flags AI detection concerns
- When reader feedback indicates content lacks human authenticity

## Prerequisites

- AI-generated content that needs humanization
- Clear understanding of target audience and voice requirements
- Time budget for editing (15-60 minutes per 1,000 words depending on quality)
- Access to the content in editable format

## Process Overview

This task follows a **multi-pass editing workflow** where each pass addresses specific dimensions of humanization. Do NOT try to fix everything at once—systematic passes produce better results with less cognitive load.

---

## Pass 1: Structural Analysis and Pattern Detection (5-10 minutes)

### Step 1.1: Sentence Length Analysis

1. **Select a representative paragraph** (about 150-200 words)
2. **Count the word length of each sentence**
3. **Calculate statistics**:
   - Mean sentence length
   - Range (shortest to longest)
   - Standard deviation (if easily available)

**Red Flags**:

- Most sentences within 15-25 word range = Low burstiness (AI-typical)
- All sentences similar length = Needs variation
- No sentences under 10 words or over 30 words = Problematic uniformity

**Target Pattern for Human-Like Writing**:

- Mix of 5-10 word sentences (20-30% of total)
- 15-25 word sentences (40-50% of total)
- 30-45 word sentences (20-30% of total)
- Occasional strategic fragments or very long constructions

### Step 1.2: AI Vocabulary Detection

Search the document for common AI-characteristic words:

**High-Priority Removals**:

- delve / delving
- robust / robustness
- leverage / leveraging
- facilitate / facilitates
- underscore / underscores
- harness / harnessing
- pivotal
- seamless / seamlessly
- holistic / holistically
- optimize / optimization (overused)

**Document each occurrence** for systematic replacement in Pass 2.

### Step 1.3: Formulaic Pattern Detection

Search for these AI-typical patterns:

**Transition Phrases**:

- "Furthermore," "Moreover," "Additionally," "In addition,"
- "It is important to note that"
- "It is worth mentioning that"
- "One of the key aspects of"
- "When it comes to"

**Paragraph Openings**:

- Count how many paragraphs start with "The [noun]..."
- Count how many start with topic sentences stating facts

**List Structures**:

- Count numbered or bulleted lists
- Check if AI defaulted to list format where prose would be better

### Step 1.4: Document Findings

Create a quick assessment:

```
Humanization Assessment:
- Sentence variation: [Low/Medium/High]
- AI vocabulary count: [number] instances
- Formulaic transitions: [number] instances
- List overuse: [Yes/No]
- Priority level: [High/Medium/Low need for humanization]
```

---

## Pass 2: Vocabulary and Language Humanization (15-20 minutes)

### Step 2.1: Replace AI-Characteristic Vocabulary

For each flagged word, choose contextually appropriate replacements:

**Replacement Guide**:

| AI Word    | Better Alternatives                                 |
| ---------- | --------------------------------------------------- |
| delve into | explore, examine, investigate, look at, dig into    |
| robust     | reliable, powerful, solid, effective, well-designed |
| leverage   | use, apply, take advantage of, employ               |
| facilitate | enable, help, make easier, allow, support           |
| underscore | show, highlight, emphasize, demonstrate, reveal     |
| harness    | use, utilize, apply, employ                         |
| pivotal    | key, important, critical, essential, crucial        |
| seamlessly | smoothly, easily, without issues, naturally         |
| holistic   | complete, comprehensive, full, thorough             |
| optimize   | improve, enhance, fine-tune, make better            |

**Important**: Choose replacements based on context, not mechanically. Sometimes the AI word is actually appropriate—replace only when a more natural alternative exists.

### Step 2.2: Introduce Contractions

Search and replace (where appropriate for your tone):

- it is → it's
- you are → you're
- we are → we're
- that is → that's
- do not → don't
- cannot → can't
- will not → won't
- should not → shouldn't

**Guidelines**:

- More contractions = more conversational (good for tutorials, blogs)
- Fewer contractions = more formal (appropriate for some documentation)
- Never in code examples or technical specifications
- Inconsistency is OK (humans mix contracted and expanded forms)

### Step 2.3: Strengthen Verbs, Eliminate Adverbs

Find weak verb + adverb combinations and replace with stronger verbs:

- "runs quickly" → "sprints" or "races"
- "said loudly" → "shouted" or "exclaimed"
- "very important" → "critical" or "essential"
- "extremely difficult" → "challenging" or "formidable"
- "highly effective" → "powerful" or "potent"

**Search for**: "very," "really," "quite," "extremely," "highly," "ly" patterns

---

## Pass 3: Sentence Structure and Burstiness Enhancement (20-30 minutes)

### Step 3.1: Create Sentence Variation Deliberately

Work paragraph by paragraph:

**For paragraphs with uniform sentence lengths**:

1. **Identify 2-3 adjacent sentences** that could be combined or split
2. **Combine short sentences** into more complex constructions:
   - Before: "Docker uses containers. Containers isolate applications. This provides consistency."
   - After: "Docker uses containers to isolate applications, providing consistency across environments."

3. **Split long sentences** into shorter punchy statements:
   - Before: "The algorithm processes data in real-time, identifying patterns that humans might miss, and revealing important insights about customer behavior that lead to better business decisions."
   - After: "The algorithm processes data in real-time, identifying patterns humans might miss. These insights reveal critical customer behaviors. Better decisions follow."

4. **Introduce strategic fragments** for emphasis:
   - "Authentication is critical. But implementing it correctly takes careful planning. Very careful planning."
   - "The solution? Microservices."

### Step 3.2: Vary Sentence Openings

**Audit sentence starters in each paragraph**:

- If 3+ sentences start with "The [noun]..." → Vary them
- If 3+ sentences start with same subject → Rewrite for variety

**Variation Techniques**:

- Start with adverbs: "Typically, developers..."
- Start with transitions: "However, this approach..."
- Start with dependent clauses: "When working with React, you'll..."
- Start with -ing verbs: "Understanding this concept..."

### Step 3.3: Replace Formulaic Transitions

**Instead of** "Furthermore," → **Use** "What's more," "Beyond that," "And here's the thing,"
**Instead of** "Moreover," → **Use** "Plus," "On top of that," "Better yet,"
**Instead of** "Additionally," → **Use** "Also," "And," or often nothing at all
**Instead of** "In conclusion," → **Use** "So what does this mean?" "The bottom line?" "Here's the takeaway,"

**Pro Tip**: Often the best transition is no explicit transition—just let ideas flow naturally.

### Step 3.4: Break Up Lists Into Prose

**Convert rigid lists to flowing narrative** where appropriate:

Before (AI-typical):

```
Docker provides three main benefits:
1. Consistency across environments
2. Improved resource efficiency
3. Simplified deployment processes
```

After (humanized):

```
Docker solves several practical problems. Your application runs identically on your laptop, your colleague's machine, and production servers—no more "works on my machine" headaches. It uses system resources more efficiently than virtual machines, letting you run more applications on the same hardware. And deployment becomes dramatically simpler since you're shipping a complete, tested environment rather than hoping dependencies align.
```

---

## Pass 4: Voice and Tone Refinement (10-15 minutes)

### Step 4.1: Inject Appropriate Personal Perspective

**For conversational technical writing**, add strategic perspective markers:

- "In my experience..."
- "I've found that..."
- "Here's what typically happens..."
- "This is where things get interesting..."
- "Watch out for this gotcha..."

**For more formal writing**, use professional collective voice:

- "Our research shows..."
- "We observe that..."
- "The data suggests..."
- "Industry practice indicates..."

**Balance**: 1-2 perspective markers per 500 words (don't overdo it)

### Step 4.2: Add Conversational Connectors

**Replace formal connectors** with conversational equivalents:

| Formal (AI-typical)          | Conversational       |
| ---------------------------- | -------------------- |
| In order to                  | To                   |
| It is important to note that | Note that / Remember |
| One must consider            | You should consider  |
| This allows us to            | This lets us         |
| It is possible to            | You can              |

### Step 4.3: Introduce Appropriate Hedging or Confidence

**AI tends toward absolute certainty**. Humanize by acknowledging nuance:

- "This typically works well when..."
- "In most cases, you'll find..."
- "This depends on your specific requirements..."
- "While there's no universal answer, a good starting point is..."

**Conversely, when AI hedges too much**, be more direct:

- Replace "may potentially" with "might" or "can"
- Replace "generally tends to" with "usually" or "often"

---

## Pass 5: Formatting Humanization (10-20 minutes)

### Step 5.1: Em-Dash Reduction (Critical - Strongest AI Signal)

**The "ChatGPT Dash" problem**: AI systems (especially GPT-4) use em-dashes approximately **10x more frequently** than human writers.

**Count Em-Dashes**:

1. Use Find (Ctrl+F / Cmd+F) to search for "—" (em-dash)
2. Count total occurrences
3. Divide by page count
4. **Target**: 1-2 em-dashes per page maximum
5. **Red Flag**: 3+ per page indicates strong AI pattern

**The Substitution Test**:
For **each em-dash**, ask: "Could a period, semicolon, or comma work as well or better?"

- **Period**: Creates stronger separation, clearer boundary
- **Semicolon**: Connects related independent clauses
- **Comma**: Works for simpler connections

**Reduction Strategy**:

- Replace 80-90% of em-dashes with alternative punctuation
- Restructure sentences to eliminate need for em-dashes
- Break compound sentences into simpler ones
- Use colons for introducing examples/explanations

**Only retain em-dash if**:

- Marks abrupt change in thought
- Introduces crucial explanation/example
- Creates intentional emphasis through interruption

### Step 5.2: Bold Text Humanization

**AI Pattern**: Mechanical consistency, excessive bolding creating visual noise

**Count Bold Elements**:

1. Estimate percentage of content that is bolded
2. **Target**: 2-5% of content maximum
3. **Red Flag**: 10%+ indicates AI pattern

**The Purposefulness Test**:
For **each bolded element**, ask: "Does THIS need visual emphasis HERE?"

**Keep bolding for**:

- UI elements (button names, menu items)
- Critical warnings (safety, errors, important notices)
- Key terms (first use only when being defined)
- Essential information readers MUST notice

**Remove bolding for**:

- Decorative emphasis
- Repetitive patterns (e.g., every function name)
- Generic emphasis

**Action**: Remove 50-70% of current bolding, retain only genuinely critical elements

### Step 5.3: Italic Text Humanization

**AI Pattern**: Scattered italics appearing with predictable frequency

**Define 2-4 Functional Categories**:

- Publication titles (books, software names)
- Terms being defined (first use only)
- Subtle emphasis (specific words requiring attention)
- Foreign expressions

**Actions**:

- Remove casual/decorative italics
- Remove italics from extended passages (3+ sentences)
- Apply italics **only** to defined functional categories
- Ensure category consistency throughout

### Step 5.4: Formatting Distribution Check

**AI Pattern**: Uniform formatting density across all sections

**Human Pattern**: Natural variation (burstiness)

**Section Analysis**:

1. Identify complex sections (difficult concepts)
2. Identify simple sections (straightforward content)
3. **Complex sections**: Should have MORE formatting (emphasis where readers need guidance)
4. **Simple sections**: Should have LESS formatting (minimal where content is clear)

**Actions**:

- Create deliberate variation in formatting density
- More em-dashes/bold/italics for complex explanations
- Minimal formatting for straightforward content
- Avoid uniform patterns (e.g., formatting every 3rd paragraph)

### Step 5.5: Quick Formatting Assessment

**Red Flags to Remove** (AI patterns):

- [ ] 3+ em-dashes per page
- [ ] Uniform bolding pattern (every similar element bolded)
- [ ] Predictable formatting rhythm
- [ ] Scattered italics without clear purpose
- [ ] Consistent formatting depth across all sections

**Green Flags to Maintain** (human patterns):

- [ ] Em-dash restraint (1-2 per page or fewer)
- [ ] Purposeful bold inconsistency (similar elements treated differently based on context)
- [ ] Functional italic categories
- [ ] Formatting variation across sections
- [ ] Each formatting choice serves clear purpose

**Reference**: Use formatting-humanization-checklist.md for comprehensive formatting audit

---

## Pass 6: Heading Humanization (15-25 minutes)

### Step 6.1: Heading Hierarchy Depth Analysis

**The Deep Hierarchy Problem**: AI systems create 4-6 heading levels; human writers use 3-4 maximum.

**Count Heading Levels**:

1. Extract all headings (H1 through H6)
2. Identify deepest level used
3. **Target**: 3 levels maximum (H1, H2, H3) for 15-20 page chapters
4. **Red Flag**: 4+ levels indicates AI structure

**Flattening Strategy**:
For each H4+ heading:

- **Promote to H3**: If content is substantial
- **Convert to bold body text**: If content is minor detail
- **Merge with parent section**: If brief
- **Remove entirely**: If adds no navigation value

**Example Transformation**:

Before (5 levels - AI pattern):

```
## Authentication (H2)
### OAuth 2.0 Flow (H3)
#### Authorization Types (H4)
##### Authorization Code (H5)
```

After (3 levels - humanized):

```
## Authentication (H2)
### OAuth 2.0 Authorization Flow (H3)

OAuth 2.0 supports multiple grant types. The most common:

**Authorization Code Grant**: Best for server-side applications...
```

### Step 6.2: Break Mechanical Parallelism

**The Parallelism Problem**: AI uses identical grammatical structure for all headings at same level.

**Detect Parallelism**:

- Count how many H2 headings start with same word/structure
- Check if all H3s follow identical pattern
- **Red Flag**: 80%+ use same structure ("Understanding X", "Understanding Y")

**Breaking Strategy**:
Rewrite 50%+ of headings with varied structures:

- **Imperatives**: "Configure the Server"
- **Gerunds**: "Configuring Options"
- **Noun phrases**: "Configuration Best Practices"
- **Questions**: "What Is Configuration?"

**Example Transformation**:

Before (mechanical parallelism):

```
## Understanding Containers (H2)
## Understanding Images (H2)
## Understanding Volumes (H2)
## Understanding Networks (H2)
```

After (natural variation):

```
## Container Basics (H2)
## Working with Images (H2)
## Data Persistence with Volumes (H2)
## How Container Networking Works (H2)
```

### Step 6.3: Create Argumentative Asymmetry

**The Uniform Density Problem**: AI gives every section same number of subsections.

**Assess Current Density**:

1. Count H3 subsections under each H2 section
2. **Red Flag**: All sections have same count (e.g., all have 3 subsections)
3. **Red Flag**: Every H2 has subsections (none have 0)

**Asymmetry Strategy**:

- **Simple sections**: 0-2 subsections (let content flow)
- **Moderate sections**: 2-4 subsections (standard structure)
- **Complex sections**: 4-6 subsections (aid navigation)

**Example Distribution**:

Before (uniform - AI pattern):

```
Section A: 3 subsections
Section B: 3 subsections
Section C: 3 subsections
Section D: 3 subsections
```

After (asymmetric - human pattern):

```
Section A: 0 subsections (simple intro, flows naturally)
Section B: 2 subsections (moderate complexity)
Section C: 5 subsections (complex procedural content)
Section D: 1 subsection (brief reference)
```

### Step 6.4: Shorten Verbose Headings

**The Verbosity Problem**: AI creates 10+ word headings with complete thoughts.

**Identify Long Headings**:

1. Find headings with 8+ words
2. **Target**: 3-7 words for H2/H3
3. **Red Flag**: 30%+ of headings exceed 8 words

**Shortening Actions**:

- Remove: "Understanding", "A Guide to", "How to", "Everything You Need to Know"
- Focus on key concept, not complete summary
- Preview, don't summarize

**Example Transformations**:

| Before (Verbose)                                                      | After (Concise)                      |
| --------------------------------------------------------------------- | ------------------------------------ |
| Understanding the Fundamental Principles of Asynchronous JavaScript   | Asynchronous JavaScript Fundamentals |
| How to Configure Your Development Environment for Optimal Performance | Development Environment Setup        |
| A Comprehensive Guide to State Management in React Applications       | State Management in React            |

### Step 6.5: Validate Heading Best Practices

**Check Hierarchy Rules**:

- [ ] No skipped levels (H1 → H2 → H3, never H1 → H3)
- [ ] No lone headings (each level has sibling, except H1)
- [ ] No stacked headings (body text appears below each heading)
- [ ] Descriptive headings (not "Introduction", "Overview", "Summary")

**Content-Type Alignment**:

- [ ] Conceptual sections: Fewer headings (0-2 subsections)
- [ ] Procedural sections: More headings (3-6 subsections for task boundaries)
- [ ] Reference sections: Structured headings for lookup
- [ ] Mixed sections: Variable density based on content needs

**Heading Density Check**:

- [ ] Overall average: 2-4 headings per page
- [ ] Natural variation exists (not uniform across chapter)
- [ ] Density reflects content complexity

**Reference**: Use heading-humanization-checklist.md for comprehensive heading audit

---

## Pass 7: Emotional Depth and Authenticity (10-15 minutes)

### Step 7.1: Add Strategic Examples and Anecdotes

**Identify abstract statements** that would benefit from concrete grounding:

Before: "Regular testing improves code quality."

After: "I learned this lesson the hard way. After shipping a feature that crashed for 30% of users because I skipped testing, I became religious about test coverage. That outage taught me what 'code quality' really means."

**Guidelines**:

- 1-2 specific examples per major section
- Use realistic scenarios, not textbook cases
- Include actual numbers, tools, versions when possible
- Ground abstract concepts in concrete experience

### Step 7.2: Acknowledge Reader Challenges

**Show empathy for learning difficulties**:

- "This concept confused me for weeks when I first learned it..."
- "The error message doesn't help—let's decode what it actually means..."
- "I know this seems backwards, but here's why it works this way..."
- "This is the tricky part that trips up most beginners..."

### Step 7.3: Express Appropriate Enthusiasm

**For genuinely interesting technical points**:

- "This is where it gets clever..."
- "Here's the elegant part..."
- "I love this solution because..."
- "This blew my mind when I first discovered it..."

**Balance**: Authentic enthusiasm, not hyperbole. Only for truly noteworthy aspects.

---

## Pass 8: Quality Assurance Check (5-10 minutes)

### Step 8.1: Read Aloud Test

**Read 2-3 paragraphs aloud** (this is critical):

- Does it sound natural when spoken?
- Do you stumble over awkward phrasings?
- Does the rhythm feel human?

**Fix anything that sounds robotic when spoken.**

### Step 8.2: Verify Technical Accuracy

**Critical**: Ensure no technical errors were introduced:

- Verify code examples still work
- Check that technical terminology remains correct
- Confirm facts and statements are accurate
- Test any procedures or commands described

**If accuracy was compromised, revert and humanize more carefully.**

### Step 8.3: Final Metrics Check

**Quick assessment**:

- [ ] Sentence lengths vary significantly (measure 2-3 paragraphs)
- [ ] AI vocabulary removed or replaced
- [ ] Voice feels consistent and authentic
- [ ] At least some contractions present (if appropriate)
- [ ] Examples or personal touches included
- [ ] **Em-dashes: 1-2 per page maximum** (strongest AI signal removed)
- [ ] **Bold text: 2-5% of content** (purposeful, not mechanical)
- [ ] **Italics: Functional categories only** (consistent application)
- [ ] **Formatting variation** across sections (burstiness maintained)
- [ ] **Heading hierarchy: 3 levels maximum** (H1, H2, H3 for typical chapters)
- [ ] **Heading parallelism broken** (varied grammatical structures)
- [ ] **Heading density asymmetric** (0-6 subsections per section based on complexity)
- [ ] **Heading length concise** (3-7 words typical for H2/H3)
- [ ] Technical accuracy preserved 100%

---

## Time-Efficient Variant (15-Minute Quick Humanization)

When time is limited, focus on **highest-impact changes**:

**Priority 1 (5 minutes)**:

1. Replace the 10 most obvious AI words
2. Add 3-5 contractions
3. Vary sentence length in most problematic paragraphs

**Priority 2 (5 minutes)**: 4. Replace formulaic transitions (Furthermore, Moreover, etc.) 5. Add 1-2 specific examples or personal touches 6. Fix any robotic-sounding sentences you notice

**Priority 3 (5 minutes)**: 7. Read aloud test on key sections 8. Verify technical accuracy not compromised 9. Fix anything that sounds obviously wrong

**This achieves ~60-70% of full humanization impact in 20% of the time.**

---

## Output Deliverable

**Primary**: Humanized content with natural flow, varied structure, authentic voice
**Secondary**: Notes on what needed the most work (informs future prompt engineering)

## Success Criteria

✅ Content reads naturally when read aloud
✅ Sentence length variation creates natural rhythm
✅ AI-characteristic vocabulary eliminated or minimized
✅ Voice feels consistent and appropriately personal
✅ Technical accuracy completely preserved
✅ Examples and authenticity markers added where appropriate

## Common Pitfalls to Avoid

❌ Changing technical terminology in pursuit of "variety"
❌ Over-editing until content becomes convoluted
❌ Adding personal anecdotes that aren't genuine or relevant
❌ Sacrificing clarity for style
❌ Forgetting to verify code examples after editing

## Related Tasks

- `humanize-pre-generation.md` - Better to humanize during creation than after
- `analyze-ai-patterns.md` - For systematic diagnosis before editing
- `humanization-qa-check.md` - For verification after humanization

## Example: Before and After

### Before (AI-Generated)

```
Docker is a robust platform that facilitates the creation and deployment
of containerized applications. It leverages operating system-level
virtualization to deliver software in packages called containers.
Containers are lightweight and include everything needed to run an
application. Furthermore, Docker provides numerous benefits for modern
development workflows. Moreover, it enables developers to build, ship,
and run applications consistently across different environments.
Additionally, Docker containers start quickly and use system resources
efficiently.
```

**Analysis**: Low burstiness (all sentences 12-18 words), AI vocabulary (robust, facilitates, leverages), formulaic transitions (Furthermore, Moreover, Additionally)

### After (Humanized)

```
Docker solves a problem every developer faces: applications that work
perfectly on your machine but crash in production. The culprit? Different
environments with different dependencies, libraries, and configurations.

Here's how Docker addresses this. It packages your application with
everything it needs—code, runtime, libraries, dependencies—into a
standardized unit called a container. These containers are lightweight.
They share the host system's kernel rather than requiring separate
operating systems like traditional virtual machines. This means they
start in seconds instead of minutes and use a fraction of the memory.

The practical benefit? Your application runs identically everywhere—your
laptop, your colleague's machine, staging servers, production. No more
"works on my machine" excuses. You're deploying the exact environment
you tested, complete with specific library versions and configurations.
```

**Improvements**: Varied sentence lengths (4 words to 30+ words), personal language ("you," "your"), problem-focused framing, removed AI vocabulary, natural transitions, specific benefits with concrete details

---

## Notes

- Budget 70-80% of total content creation time for humanization, not generation
- The fastest humanization is good pre-generation prompting (prevents problems)
- Perfect is the enemy of done—aim for "noticeably human" not "perfectly undetectable"
- Different content types need different levels of humanization (tutorials > API docs)

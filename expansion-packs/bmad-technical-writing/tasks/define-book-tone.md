<!-- Powered by BMAD™ Core -->

# Define Book Tone

---

task:
  id: define-book-tone
  name: Define Book Tone
  description: Create comprehensive tone specification for technical book project to ensure consistent voice throughout
  persona_default: instructional-designer
  inputs:
    - book-proposal.md (recommended)
    - book-outline.md (recommended)
    - target-publisher
  steps:
    - Understand book context and audience
    - Elicit tone preferences from author
    - Define formality level with examples (1-5 scale)
    - Select tone characteristics (5 key adjectives)
    - Align with publisher requirements
    - Create example passages showing target tone
    - Document excluded tones and anti-patterns
    - Generate tone-specification.md using create-doc task with tone-specification-tmpl.yaml
  output: tone-specification.md

---

## Purpose

Define a comprehensive tone specification for a technical book project BEFORE writing begins, ensuring consistent voice, style, and personality throughout the entire manuscript. This prevents tone drift in long-form content and provides clear guidance for AI-assisted drafting.

## When to Use

**Use this task when:**

- Starting a new technical book project (greenfield)
- Beginning book planning phase after outline approval
- Multiple authors need shared tone guidance
- Publisher has specific tone expectations
- Planning AI-assisted chapter drafting

**Timing:** Execute AFTER book outline is complete, BEFORE writing any chapters.

## Prerequisites

- Book proposal completed (or clear understanding of book purpose)
- Book outline drafted with chapter structure
- Target publisher identified (or self-publishing confirmed)
- Author has considered desired voice/personality
- Access to tone-specification-tmpl.yaml template
- Access to publisher-guidelines.md knowledge base

## Workflow Steps

### 1. Understand Book Context

Load and review existing project materials:

**Required Context:**
- Book topic and technical domain
- Target audience (beginners/intermediate/advanced)
- Learning objectives and scope
- Publisher (PacktPub, O'Reilly, Manning, Self-Publishing)

**Actions:**
- Load book-proposal.md if available
- Load book-outline.md to understand chapter structure
- Review target audience definition
- Note any tone requirements from publisher

**Output:** Clear understanding of book purpose and audience.

### 2. Elicit Tone Preferences from Author

Ask strategic questions to understand desired tone:

**Target Audience Tone Expectations:**
- How does your target audience expect to be addressed?
- What tone would make them feel comfortable and engaged?
- Are they academic researchers, professional practitioners, or hobbyist learners?

**Author Personality vs. Book Personality:**
- Do you want your personal voice to come through, or prefer neutral professional tone?
- Should the book sound like you're speaking to a colleague, teaching a class, or presenting research?
- Do you use humor, encouragement, or directness in your communication style?

**Formality Assessment:**
- On a scale of 1-5 (1=very casual, 5=very formal), where should this book fall?
- Should you use contractions (don't, we'll) or avoid them (do not, we will)?
- How complex should sentence structures be?

**Tone Characteristics:**
- Which adjectives best describe your desired tone? (Select 5 from: encouraging, authoritative, friendly, technical, conversational, academic, professional, approachable, precise, warm, direct, patient, enthusiastic, pragmatic, etc.)

**Publisher-Specific Questions:**
- Are you aware of your publisher's tone expectations?
- PacktPub: "Conversational but professional" - does this fit your vision?
- O'Reilly: "Authoritative precision" - does this align?
- Manning: "Author voice with personality" - comfortable with this?

**Important:** These are elicitation questions, not rigid requirements. Author's authentic voice takes priority over generic formulas.

### 3. Define Formality Level with Examples

Establish specific formality level (1-5 scale):

**Formality Scale:**

**Level 1 (Very Casual):**
- Example: "Hey there! Let's dive into JavaScript. You're gonna love this stuff."
- Contractions frequent, exclamations common, very conversational

**Level 2 (Casual/Friendly):**
- Example: "Let's explore JavaScript together. You'll find these concepts intuitive once you try them."
- Contractions used, friendly but structured, approachable

**Level 3 (Professional/Conversational):**
- Example: "In this chapter, we'll examine JavaScript fundamentals. You'll apply these concepts through practical examples."
- Balanced contractions, professional yet warm, standard for most technical books

**Level 4 (Formal/Professional):**
- Example: "This chapter examines JavaScript fundamentals. Readers will apply these concepts through practical examples."
- Minimal contractions, structured tone, academic-adjacent

**Level 5 (Very Formal/Academic):**
- Example: "This chapter presents an examination of JavaScript fundamentals. The subsequent examples demonstrate practical application of these concepts."
- No contractions, passive voice acceptable, scholarly tone

**Action:** Based on elicitation, select formality level and document with specific examples for THIS book's content.

### 4. Select Tone Characteristics

Choose 5 key adjectives that define the book's tone personality:

**Selection Process:**
1. Review adjectives discussed during elicitation
2. Select the 5 most important characteristics
3. Define what each means in context of THIS book
4. Provide examples showing each characteristic

**Example Tone Profile:**

**For a beginner-friendly web development book:**
1. **Encouraging:** "You've got this! Every developer starts somewhere, and you're already making progress."
2. **Practical:** "Let's build a real login form, not just discuss theory. You'll deploy this by end of chapter."
3. **Conversational:** "Think of CSS like decorating a room. You're choosing colors, arranging furniture..."
4. **Patient:** "If this seems confusing, that's normal. We'll break it into smaller steps and try again."
5. **Direct:** "Don't use inline styles. They're harder to maintain. Use external stylesheets instead."

**Action:** Create similar profile with 5 adjectives + definitions + examples for your book.

### 5. Align with Publisher Requirements

Ensure tone meets publisher-specific expectations:

**PacktPub Requirements:**
- Tone: "Conversational but professional"
- Interpretation: Level 2-3 formality, encouraging + practical characteristics
- Code comments: Clear explanations, conversational style
- Avoid: Overly academic language, excessive formality
- Example: "Let's create a function that handles user authentication. We'll keep it simple for now."

**O'Reilly Requirements:**
- Tone: "Authoritative with technical precision"
- Interpretation: Level 3-4 formality, authoritative + precise characteristics
- Code comments: Technical accuracy prioritized, detailed explanations
- Avoid: Casual language, unverified claims, hand-waving
- Example: "The authentication function implements OAuth 2.0 protocol specification. Note the token validation in line 12."

**Manning Requirements:**
- Tone: "Author voice with personality"
- Interpretation: Level 2-3 formality, author's authentic voice preserved
- Code comments: Author's natural explanation style
- Avoid: Generic corporate voice, suppressing personality
- Example: "I learned this the hard way after a 3am production incident. Here's what actually works..."

**Self-Publishing:**
- Tone: Author's choice, no publisher constraints
- Interpretation: Any formality level, any characteristics
- Recommendation: Stay consistent with chosen tone throughout
- Flexibility: Can target niche audience with specialized tone

**Action:** Document how your tone aligns with publisher requirements, adjust if needed.

### 6. Create Example Passages

Write 3-5 sample passages (2-3 paragraphs each) demonstrating target tone:

**Coverage Requirements:**
- Example 1: Chapter introduction (how you'll open chapters)
- Example 2: Technical explanation (how you'll teach concepts)
- Example 3: Code example with commentary (how you'll present code)
- Example 4 (optional): Transition between topics
- Example 5 (optional): Chapter summary/conclusion

**Criteria:**
- Use ACTUAL content from your book outline
- Apply chosen formality level consistently
- Demonstrate all 5 tone characteristics
- Show code comment style in context
- Length: 2-3 paragraphs minimum per example

**Purpose:** These become reference materials when drafting chapters. "Write like THIS."

### 7. Document Excluded Tones and Anti-Patterns

Define what to AVOID (equally important as what to include):

**Excluded Tones:**
- List tone approaches explicitly rejected for this book
- Explain WHY each is excluded

**Example Exclusions:**

For a professional developer book:
- ❌ **Overly playful/childish:** "Wheee! Let's make our code go zoom zoom!" (Why: Undermines professional audience)
- ❌ **Condescending:** "Even a beginner should understand this obvious concept." (Why: Alienates learners)
- ❌ **Aggressive/preachy:** "You're doing it WRONG if you don't use X framework!" (Why: Discourages exploration)
- ❌ **Overly academic:** "Herein we shall explicate the algorithmic paradigm..." (Why: Too formal for practitioner audience)
- ❌ **Salesy/marketing:** "This amazing revolutionary technique will change your life!" (Why: Reduces credibility)

**Anti-Patterns to Avoid:**
- Tone inconsistency (formal intro, casual explanations)
- Shifting formality levels mid-chapter
- Mixing metaphors excessively
- Overuse of exclamation points (or complete absence)
- Inconsistent use of contractions

**Action:** Create 5-8 specific exclusions with explanations for YOUR book.

### 8. Generate tone-specification.md Document

Use create-doc task with tone-specification-tmpl.yaml template:

**Execution:**
1. Ensure all above steps completed with documented answers
2. Run: create-doc task with tone-specification-tmpl.yaml
3. Populate template sections with gathered information
4. Review generated document for completeness
5. Save as: tone-specification.md in project root or docs/

**Template Sections to Populate:**
- Book overview & audience
- Tone personality (5 key adjectives with definitions)
- Voice characteristics (formal/casual, perspective, active/passive)
- Formality level (1-5 scale with examples)
- Publisher alignment (specific guidance)
- Terminology preferences
- Code comment style in context of tone
- Example passages (3-5 samples)
- Tone consistency rules
- Excluded tones/approaches (anti-patterns)

**Validation Before Finalizing:**
- All 5 tone characteristics defined with examples
- Formality level specified with book-specific examples
- Publisher requirements addressed (or N/A for self-publishing)
- Minimum 3 example passages included
- Minimum 5 excluded tones/anti-patterns documented
- Code comment style examples present

**Output Location:** Save tone-specification.md where expand-outline-to-draft task can access it (typically project root or docs/).

## Success Criteria

✅ **Tone specification is complete when:**

- All 8 workflow steps executed
- tone-specification.md file generated using template
- 5 tone characteristics defined with clear examples
- Formality level (1-5) specified with book-specific passages
- Publisher alignment documented (specific adjustments made)
- 3-5 example passages demonstrate target tone consistently
- 5+ excluded tones documented with explanations
- Code comment style examples included
- Author confirms: "This feels like my book's voice"
- Document saved in accessible location for drafting tasks

✅ **Quality indicators:**

- Examples use actual book content (not generic samples)
- Tone characteristics are specific, not generic ("encouraging" with examples, not just "good")
- Formality level includes comparison examples showing consistency
- Publisher guidance includes specific language adjustments
- Excluded tones prevent common pitfalls for this book's audience

## Integration Points

**Input From:**
- book-proposal.md (book purpose, audience)
- book-outline.md (chapter structure, topic coverage)
- publisher-guidelines.md (publisher tone requirements)

**Output To:**
- expand-outline-to-draft.md (uses tone-specification.md when drafting chapters)
- copy-edit-chapter.md (validates tone consistency during editing)
- tone-consistency-checklist.md (references tone-specification.md for validation)

**Workflow Position:**
- Executed AFTER: book outline approved
- Executed BEFORE: any chapter drafting begins
- Part of: book-planning-workflow.yaml

## Important Notes

**Preserve Author Voice:**
- Tone specification should ENHANCE author's natural voice, not replace it
- If tone feels forced or unnatural, revisit and adjust
- Author authenticity > rigid formula compliance

**AI-Assisted Drafting Consideration:**
- Specific examples are crucial for AI to apply tone correctly
- The more detailed your tone-specification.md, the more consistent AI-generated drafts will be
- Generic descriptions ("friendly tone") produce generic results
- Specific examples ("Write like THIS passage") produce targeted results

**Flexibility:**
- Tone can evolve slightly as book develops
- Major tone shifts indicate specification needs update
- Consistency matters more than perfection

**Multi-Author Projects:**
- All authors must review and approve tone specification
- Use tone specification as shared reference during writing
- Appoint "tone guardian" to maintain consistency during editing

**Brownfield Projects:**
- For 2nd/3rd editions or book updates, use extract-tone-patterns.md instead
- This task is for NEW books defining tone from scratch

**Publisher Feedback:**
- Share tone-specification.md with publisher editor for early validation
- Adjust based on feedback BEFORE writing chapters
- Easier to adjust specification than rewrite chapters

## Common Pitfalls to Avoid

❌ **Over-specifying:** Don't create 50-page tone guidelines. Keep it actionable.

❌ **Under-specifying:** Don't just say "friendly tone." Provide examples showing what "friendly" means for THIS book.

❌ **Ignoring publisher:** If writing for PacktPub, O'Reilly, or Manning, their tone requirements matter. Don't ignore them.

❌ **Generic examples:** Don't use placeholder content. Use YOUR book's actual topics in example passages.

❌ **Tone-audience mismatch:** Casual playful tone doesn't work for enterprise architecture book. Match tone to audience.

❌ **Skipping this step:** "I'll just figure out tone as I write" leads to 500-page books with inconsistent voice. Define tone FIRST.

❌ **Analysis paralysis:** Don't spend weeks perfecting tone specification. 2-3 hours is sufficient for most books.

## Example Use Case

**Scenario:** Author planning "Practical Kubernetes for DevOps Engineers" (PacktPub, 450 pages, intermediate audience)

**Execution:**

1. **Context:** Book teaches Kubernetes to DevOps engineers with some Docker experience
2. **Elicitation:** Author wants practical, encouraging tone for busy professionals
3. **Formality:** Level 3 (Professional/Conversational) - "Let's deploy this to production"
4. **Characteristics:** Practical, Encouraging, Direct, Experienced, Professional
5. **Publisher:** PacktPub "conversational but professional" → good alignment
6. **Examples:** 5 passages showing Kubernetes deployments in target tone
7. **Exclusions:** No overly academic, no condescending "just deploy it" without explanation, no marketing hype
8. **Output:** tone-specification.md ready for chapter drafting

**Result:** All 18 chapters maintain consistent "experienced DevOps mentor" voice throughout 450 pages.

## Related Tasks

- **create-doc.md** - Document generation engine (required for Step 8)
- **expand-outline-to-draft.md** - Uses tone-specification.md when drafting chapters
- **copy-edit-chapter.md** - Validates tone consistency using this specification
- **extract-tone-patterns.md** - Brownfield alternative for existing books

## Related Templates

- **tone-specification-tmpl.yaml** - Template used in Step 8 to generate tone-specification.md

## Related Checklists

- **tone-consistency-checklist.md** - Validates tone alignment with specification during editing

## Related Knowledge Base

- **publisher-guidelines.md** - Publisher-specific tone requirements
- **technical-writing-standards.md** - General voice and tone principles
- **writing-voice-guides.md** - Tone profile examples and decision matrix

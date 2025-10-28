# Tone Consistency Checklist

Use this checklist to validate that chapter content maintains consistent tone and voice throughout, aligning with tone-specification.md or extracted-tone-patterns.md. Execute during copy editing or quality assurance phases.

## Prerequisites

Before using this checklist:

- [ ] tone-specification.md OR extracted-tone-patterns.md is available
- [ ] Chapter draft is complete
- [ ] You have read the tone specification/patterns document

## Voice Consistency

- [ ] Author voice is preserved throughout chapter (personality evident)
- [ ] Perspective (first/second/third person) is consistent across all sections
- [ ] Active vs. passive voice usage matches tone specification patterns
- [ ] Voice matches tone-specification.md personality characteristics
- [ ] No unintentional voice shifts between sections

**Common Violations:**
- Formal academic voice in introduction, then suddenly casual in examples
- Third person in explanations, switching to first person in conclusions
- Passive construction overuse contradicting "direct" tone characteristic

## Formality Level Consistency

- [ ] Formality level (1-5 scale) consistent with tone-specification.md
- [ ] Contractions usage matches specification (frequent/moderate/rare/never)
- [ ] Vocabulary appropriate for specified formality level
- [ ] Sentence structures match formality level (complex vs. simple)
- [ ] Formality level matches target audience expectations
- [ ] No formality drift mid-chapter or between sections

**Examples of Formality Inconsistency:**

**Violation (Level 3 spec, but drifts to Level 5):**
> "Let's deploy your application to AWS. (Level 3)
> Herein we shall explicate the deployment paradigm pursuant to infrastructure specifications. (Level 5 drift)"

**Correct (Consistent Level 3):**
> "Let's deploy your application to AWS. We'll use Terraform to define our infrastructure and automate the deployment process."

## Publisher Alignment

- [ ] Tone meets publisher-specific requirements (if applicable)
- [ ] **PacktPub:** Tone is "conversational but professional" (Level 2-3)
- [ ] **O'Reilly:** Tone demonstrates "authoritative technical precision" (Level 3-4)
- [ ] **Manning:** "Author voice with personality" is evident (Level 2-3)
- [ ] **Self-Publishing:** Tone matches author's chosen approach consistently
- [ ] No generic corporate voice replacing authentic author personality

**Publisher Misalignment Example:**

**Manning book using generic corporate voice (WRONG):**
> "The deployment process should be initiated according to established protocols."

**Manning book with author personality (CORRECT):**
> "I've deployed hundreds of apps this way, and here's what actually works in production..."

## Tone Characteristics Application

- [ ] All 5 tone characteristics from specification are demonstrated
- [ ] "Encouraging" characteristic (if specified) is evident without being patronizing
- [ ] "Authoritative" characteristic (if specified) is present without arrogance
- [ ] "Practical" characteristic (if specified) shows real-world application
- [ ] "Conversational" characteristic (if specified) maintains professionalism
- [ ] "Direct" characteristic (if specified) avoids unnecessary hedging
- [ ] Tone characteristics applied consistently across entire chapter

**Characteristic Application Examples:**

**Encouraging (when specified):**
> ✓ "You've tackled the basics. Now you're ready for production deployment."
> ✗ "Even a beginner could understand this simple concept." (condescending)

**Authoritative (when specified):**
> ✓ "Use environment variables for secrets. Hard-coding credentials is a security vulnerability."
> ✗ "I think maybe you should probably consider possibly using environment variables?" (weak)

## Code Comment Style Consistency

- [ ] Code comments match overall chapter tone
- [ ] Comment style matches tone-specification.md code examples
- [ ] Comment density consistent across all code blocks
- [ ] Comment formality matches prose formality
- [ ] Comments explain "why" or "what" as specified in tone specification
- [ ] No tone disconnect between prose and code comments

**Code Comment Tone Examples:**

**Formal Tone (Level 4) - Correct:**
```javascript
// Validate JWT signature to ensure token integrity
const isValid = verifySignature(token, secret);
```

**Formal Tone (Level 4) - WRONG (too casual):**
```javascript
// Let's check if this token is legit!
const isValid = verifySignature(token, secret);
```

**Conversational Tone (Level 2) - Correct:**
```javascript
// Check if the token's been tampered with
const isValid = verifySignature(token, secret);
```

## Transition and Flow Consistency

- [ ] Transitions between sections maintain tone
- [ ] Transition phrases match tone-specification.md patterns
- [ ] Chapter introductions follow specified opening style
- [ ] Chapter conclusions follow specified closing style
- [ ] Section-to-section handoffs maintain consistent voice

**Transition Tone Examples:**

**Professional/Conversational (Level 3):**
> "Now that you understand JWT structure, let's explore how to securely sign and verify tokens."

**Formal (Level 4):**
> "Having examined JWT structure, we now turn to signature creation and verification."

**Casual (Level 2):**
> "Okay, you've got JWT structure down. Time to tackle signing and verifying these tokens!"

## Learning Support Tone

- [ ] Explanations support learning objectives without talking down
- [ ] Encouragement appropriate for target audience skill level
- [ ] Warnings and cautions match overall tone
- [ ] Error handling explanations align with tone characteristics
- [ ] Troubleshooting guidance maintains specified voice

**Learning Support Examples:**

**Encouraging without patronizing:**
> ✓ "If you're seeing this error, don't worry—it's a common misconfiguration."
> ✗ "Don't feel bad if you made this silly mistake! It happens to everyone!"

**Direct but supportive:**
> ✓ "This won't work in production. Use environment variables instead."
> ✗ "Well, technically you could do this, but you probably shouldn't maybe..."

## Terminology and Language Consistency

- [ ] Technical terms used consistently (not alternating synonyms randomly)
- [ ] Terminology choices match tone-specification.md preferences
- [ ] Jargon level appropriate for target audience
- [ ] Acronyms handled consistently (defined on first use, or assumed knowledge)
- [ ] Industry-standard terms used per specification

**Terminology Consistency Examples:**

**Consistent:**
> "Function" used throughout chapter for JavaScript functions

**Inconsistent (WRONG):**
> Alternating "function", "method", "routine", "procedure" for same concept

## Metaphor and Analogy Usage

- [ ] Metaphor frequency matches tone specification
- [ ] Analogies appropriate for target audience
- [ ] Metaphors don't undermine technical credibility
- [ ] Analogy complexity matches formality level
- [ ] No forced or confusing metaphors

**Metaphor Tone Examples:**

**Appropriate for casual tone:**
> "Think of JWT like a concert wristband—it proves you paid to get in."

**Too playful for formal technical book:**
> "JWT is like a magical unicorn stamp of authentication wonderfulness!"

## Excluded Tone Avoidance

- [ ] No excluded tones from tone-specification.md present
- [ ] No condescending language ("even beginners know", "obviously")
- [ ] No overly aggressive prescriptiveness ("never", "always", "you must")
- [ ] No apologetic or uncertain language (if authority is specified)
- [ ] No marketing hype or exaggeration (if technical precision specified)
- [ ] No generic corporate-speak (if personal voice specified)

**Anti-Pattern Examples:**

**Condescending (AVOID):**
> "This should be obvious to anyone with basic programming knowledge."

**Overly aggressive (AVOID if not specified):**
> "You're doing it WRONG if you don't use framework X!"

**Marketing hype (AVOID in technical books):**
> "This AMAZING technique will REVOLUTIONIZE your coding!"

## Chapter-Level Consistency

- [ ] Introduction tone matches body tone
- [ ] Code examples maintain consistent commentary style
- [ ] Sidebars/callouts maintain tone
- [ ] Exercises or challenges match tone
- [ ] Summary/conclusion maintains tone
- [ ] No tone fatigue (starting strong, ending weak)

**Chapter Arc Consistency:**

Check that tone doesn't:
- Start formal, drift casual
- Start encouraging, become dismissive
- Start direct, become meandering
- Start conversational, become academic

## Multi-Author Projects (if applicable)

- [ ] All authors follow same tone-specification.md
- [ ] No detectable author switches based on tone changes
- [ ] Consistent formality level across author contributions
- [ ] Consistent voice characteristics across author sections
- [ ] Tone guardian has reviewed for consistency

## Tone Validation Against Specification

- [ ] Direct comparison: Does paragraph X match example passage Y from spec?
- [ ] Formality level spot-check: Sample 10 sentences—do they match Level N?
- [ ] Characteristic demonstration: Are all 5 adjectives evident in chapter?
- [ ] Code comment audit: Do 5 random code blocks match comment style spec?
- [ ] Transition pattern check: Do transitions match specification patterns?

## Before/After Examples (Tone Corrections)

**Example 1: Formality Level Correction**

**Original (Level 5, spec calls for Level 3):**
> "One must ensure that the authentication mechanism functions properly prior to deployment."

**Corrected (Level 3):**
> "You'll need to verify your authentication works before deploying to production."

---

**Example 2: Voice Consistency Correction**

**Original (Perspective shifts):**
> "Let's examine JWT structure. One should note the three components. You'll implement this in Chapter 5."

**Corrected (Consistent second person):**
> "Let's examine JWT structure. You'll notice three components. You'll implement this in Chapter 5."

---

**Example 3: Tone Characteristic Application**

**Original (Missing "practical" characteristic from spec):**
> "JWTs can be used for authentication in theoretical scenarios."

**Corrected (Demonstrates "practical"):**
> "You'll use JWTs to authenticate API requests in your production application."

---

**Example 4: Code Comment Tone Alignment**

**Original (Comment too formal for Level 2 prose):**
> ```javascript
> // Instantiate the authentication service object
> const auth = new AuthService();
> ```

**Corrected (Comment matches Level 2 conversational tone):**
> ```javascript
> // Set up the auth service
> const auth = new AuthService();
> ```

---

**Example 5: Publisher Alignment Correction**

**Original (Too formal for PacktPub "conversational but professional"):**
> "The subsequent section delineates the authentication methodology."

**Corrected (PacktPub-appropriate):**
> "Let's look at how authentication works in the next section."

## Red Flags (Immediate Attention Required)

**Critical tone violations:**

⚠️ **Multiple formality levels in same chapter** - Inconsistent reader experience
⚠️ **Code comments completely different tone than prose** - Jarring disconnect
⚠️ **Publisher misalignment** - May require rewrite before submission
⚠️ **Condescending language** - Alienates readers, damages credibility
⚠️ **No author personality** (when Manning or personality-driven tone specified) - Generic and unmemorable
⚠️ **Tone drift across chapter** - Professional intro → sloppy conclusion indicates fatigue

## Remediation Process

If checklist reveals tone violations:

1. **Identify violation category** (formality, voice, characteristics, etc.)
2. **Locate all instances** throughout chapter
3. **Review tone-specification.md** for correct approach
4. **Apply corrections systematically** (don't fix randomly)
5. **Verify corrections preserve author voice** (don't over-correct)
6. **Re-run this checklist** after corrections
7. **Document changes** in editorial notes

## Usage Notes

**When to use this checklist:**

- During copy editing phase (after technical review complete)
- Before submitting chapter to publisher
- When adding new sections to existing chapters
- For multi-author coordination reviews
- When author suspects tone drift

**How to use this checklist:**

1. Load tone-specification.md OR extracted-tone-patterns.md
2. Read chapter draft completely
3. Check each category systematically
4. Document violations with chapter section references
5. Apply corrections referencing tone specification examples
6. Verify corrections maintain author authenticity

**Integration with other tasks:**

- Use with **copy-edit-chapter.md** task (Step 9 enhancement)
- Reference **tone-specification.md** (greenfield projects)
- Reference **extracted-tone-patterns.md** (brownfield projects)
- Execute via **execute-checklist.md** task

## Acceptance Criteria

This checklist is complete when:

- [ ] All categories reviewed
- [ ] Violations documented with specific examples
- [ ] Corrections applied maintaining author voice
- [ ] Tone aligns with tone-specification.md
- [ ] No detectable tone inconsistencies remain
- [ ] Chapter reads with unified, consistent voice throughout

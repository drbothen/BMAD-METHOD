<!-- Powered by BMAD™ Core -->

# Expand Outline to Draft

---

task:
id: expand-outline-to-draft
name: Expand Outline to Draft
description: Convert bullet outline into initial prose draft for editing
persona_default: tutorial-architect
inputs:
  - outline (bullet-point format from research synthesis or chapter planning)
  - target-audience
  - tone-specification.md (REQUIRED - defines book's voice, formality, characteristics)
steps:
  - Review tone-specification.md to understand book's voice
  - Review complete outline and understand structure
  - Identify target audience and appropriate tone from specification
  - Expand bullet points into flowing prose using defined tone
  - Integrate code examples at appropriate points with tone-appropriate comments
  - Add section introductions and transitions matching tone style
  - Mark as DRAFT requiring human technical review
output: Draft prose document (marked for technical review)
ai_assistance: true
human_verification_required: true

---

## Purpose

This task converts structured bullet-point outlines into initial prose drafts, accelerating content creation by providing a starting point for editing. This is **AI-ASSISTED** content generation—the output requires human technical review and refinement.

## ⚠️ Critical Warnings

**AI-GENERATED CONTENT MAY CONTAIN INACCURACIES**

- ⚠️ **Always verify code examples work**
- ⚠️ **Check technical claims against authoritative sources**
- ⚠️ **This is a starting point, not final content**
- ⚠️ **Human technical review is MANDATORY**
- ⚠️ **Never publish AI-generated technical content without verification**

**Why Human Verification is Essential:**

- AI may hallucinate technical details
- AI may misunderstand nuanced concepts
- Pedagogical decisions require human judgment
- Code examples must be tested (not just generated)
- Technical accuracy is non-negotiable

## Prerequisites

Before starting this task:

- **Completed outline** - Bullet-point outline from synthesize-research-notes.md or chapter planning
- **Target audience identified** - Know who you're writing for
- **tone-specification.md** (REQUIRED) - Complete tone specification defining book's voice, formality level, characteristics, and example passages. If missing, run define-book-tone.md task first.
- **Code examples available** (if referenced in outline) - Have working code ready
- **Understanding of content domain** - Ability to verify technical accuracy

## Workflow Steps

### 1. Review Tone Specification (CRITICAL FIRST STEP)

**Before drafting any prose, load and review tone-specification.md:**

This step is MANDATORY. Tone must be applied from the first sentence, not added during editing.

**Load tone-specification.md:**

If file does not exist:
- ⚠️ **STOP** - Do not proceed with drafting
- Run define-book-tone.md task first
- Tone specification must be complete before any chapter drafting

**Review Key Sections:**

1. **Tone Personality (5 adjectives)** - Understand the characteristics that define this book's voice
2. **Formality Level (1-5 scale)** - Note whether writing should be casual, professional, or formal
3. **Example Passages** - Read all example passages carefully - these are your "write like THIS" models
4. **Code Comment Style** - Note how code comments should sound in this book
5. **Excluded Tones** - Review anti-patterns to avoid

**Internalize Writing Style:**

- Which of the 5 tone characteristics are most important?
- What formality level guides sentence structure and vocabulary?
- What does "encouraging" or "authoritative" mean for THIS book specifically?
- How should transitions sound? (Check example passages)
- Should I use contractions? (Check formality level)

**Tone Application Strategy:**

Based on tone-specification.md, determine:

- **Opening style:** How will chapter introductions sound?
- **Explanation style:** Formal definitions or conversational teaching?
- **Code commentary:** Detailed explanations or concise notes?
- **Encouragement approach:** Explicit support ("You've got this!") or implicit confidence?
- **Transition phrases:** Which transition words match the tone?

**Example Tone Review:**

```markdown
**From tone-specification.md:**

Tone Personality: Practical, Encouraging, Conversational, Direct, Experienced

Formality Level: 3 (Professional/Conversational)
- Use: "Let's deploy this application"
- Avoid: "We shall deploy the application"

Example Passage:
"Let's deploy your authentication service to AWS. You'll use production-ready Terraform configuration—no toy examples or 'works on my laptop' shortcuts. By the end of this chapter, you'll have a secure, scalable auth service running in the cloud."

**Application Strategy for This Chapter:**
- Open with "Let's [action]" pattern
- Use contractions moderately ("you'll", "we'll")
- Emphasize practical production readiness
- Encourage but don't coddle ("you'll have a secure service" - implies confidence)
- Be direct about what's happening (no hedging)
```

**Output of This Step:**
- Clear understanding of book's voice
- Specific tone application strategy for this chapter
- Reference examples loaded for comparison during drafting

### 2. Review Outline

Read and understand the complete outline before expansion:

**Read Complete Outline:**

- Read through all sections and bullet points
- Understand overall structure and flow
- Note hierarchical relationships
- Identify main topics and subtopics

**Understand Context:**

- What is the chapter/section about?
- What are the learning objectives?
- What prerequisite knowledge is assumed?
- What comes before and after this content?

**Note Code Examples:**

- Which bullet points reference code examples?
- Are code examples available and tested?
- Where should code be integrated?
- What do code examples demonstrate?

**Identify Target Audience:**

- Beginner, intermediate, or advanced?
- What can you assume they know?
- What needs detailed explanation?
- What tone is appropriate (formal, conversational, encouraging)?

**Example Outline Analysis:**

```markdown
## Original Outline

### Section 2: Understanding JWT Structure (4 pages)

- JWT has three parts: header, payload, signature
- Header contains algorithm (alg) and type (typ)
  - Example: {"alg": "HS256", "typ": "JWT"}
- Payload contains claims
  - Registered claims: iss, sub, aud, exp, iat, jti
  - Public claims (custom, namespaced)
  - Private claims (application-specific)
  - CRITICAL: Payload is encoded, NOT encrypted
- Signature prevents tampering
  - Computed: HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
  - Verification ensures integrity
- [CODE: Decoding JWT to see payload]
- [CODE: Creating JWT with custom claims]
- [CODE: Verifying JWT signature]
- Common misconception: "JWT is encrypted" → No, it's signed

**Analysis:**

- Audience: Intermediate developers (assumes basic auth knowledge)
- Tone: Technical but accessible
- 3 code examples to integrate
- Key teaching point: Encoding vs encryption distinction
```

### 3. Expand Bullet Points to Paragraphs (Applying Tone)

Convert each bullet point into flowing prose WHILE APPLYING TONE from Step 1:

**CRITICAL: Tone Application**

Every expansion must reflect the tone-specification.md:
- Use formality level from specification (contractions, sentence structure, vocabulary)
- Demonstrate tone characteristics (encouraging, authoritative, practical, etc.)
- Match example passage style
- Follow transition patterns from specification
- Apply code comment style consistently

**Expansion Guidelines:**

**For Concept Bullets (2-4 sentences):**

- Start with clear topic sentence
- Add context and explanation
- Use appropriate technical terminology
- Maintain active voice
- Keep audience in mind
- **APPLY TONE** from specification

**Example:**

```markdown
**Outline Bullet:**

- JWT has three parts: header, payload, signature

**Expanded Prose:**
A JSON Web Token consists of three distinct parts: the header, the payload, and the signature. These three components are concatenated with periods (.) to form the complete token string you see in practice. Understanding each part's role is essential for both implementing and securing JWT-based authentication in your applications.
```

**For Detail Bullets (1-3 sentences):**

- Provide specific information
- Explain significance
- Add examples if helpful

**Example:**

```markdown
**Outline Bullet:**

- Header contains algorithm (alg) and type (typ)

**Expanded Prose:**
The header specifies which algorithm is used to create the signature (alg) and declares the token type (typ), which is always "JWT". For example, a header might be `{"alg": "HS256", "typ": "JWT"}`, indicating the token uses HMAC with SHA-256 for signing.
```

**For Warning/Critical Bullets (2-5 sentences):**

- Emphasize importance
- Explain consequences
- Provide correct understanding

**Example:**

```markdown
**Outline Bullet:**

- CRITICAL: Payload is encoded, NOT encrypted

**Expanded Prose:**
It's crucial to understand that the JWT payload is base64url encoded, not encrypted. This means anyone who has the token can decode and read the payload—it's like sending a postcard instead of a sealed letter. Never include sensitive information like passwords, credit card numbers, or private keys in a JWT payload. The signature protects the token's integrity (detecting tampering), but it does not protect confidentiality (hiding contents).
```

**Connect Paragraphs with Transitions:**

```markdown
**Poor (No Transitions):**
The header specifies the algorithm. The payload contains claims. The signature prevents tampering.

**Good (With Transitions):**
The header specifies the algorithm used for signing. Building on this, the payload contains the claims—the actual data you want to transmit. Finally, the signature ties everything together by preventing tampering with either the header or payload.
```

**Tone Application Examples:**

Same content, different tones based on tone-specification.md:

```markdown
**Outline Bullet:**
- JWT has three parts: header, payload, signature

**Formal Tone (Level 4 - Authoritative):**
A JSON Web Token comprises three distinct components: the header, the payload, and the signature. Each component serves a specific cryptographic purpose. The three parts are base64url-encoded and concatenated with period separators to form the complete token.

**Professional/Conversational Tone (Level 3 - Practical + Encouraging):**
A JSON Web Token consists of three parts: the header, the payload, and the signature. You'll see these three components joined with periods (.) to form the complete token string. Understanding each part's role will help you implement and secure JWT-based authentication in your applications.

**Casual/Friendly Tone (Level 2 - Approachable + Conversational):**
Let's break down a JSON Web Token. It's got three parts: the header, payload, and signature. Think of them as three pieces that snap together with periods (.) to make the complete token you'll use in practice. Once you understand what each part does, JWT authentication will make a lot more sense.

**Key Differences:**
- Formality Level 4: "comprises", "cryptographic purpose", no contractions
- Formality Level 3: "consists of", "you'll see", moderate contractions, direct but professional
- Formality Level 2: "let's break down", "it's got", "you'll use", frequent contractions, conversational

**YOUR TASK:** Match the tone from YOUR tone-specification.md, not these examples.
```

### 4. Integrate Code Examples

Place code examples at appropriate points with proper framing:

**Before Code: Introduce It (1-2 sentences)**

```markdown
Let's see how to decode a JWT to inspect its payload. The following example uses the `jwt-decode` library to reveal the token's contents:
```

**The Code: Complete and Runnable**

````markdown
```javascript
const jwt = require('jwt-decode');

const token =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';

const decoded = jwt(token);
console.log(decoded);
// Output: { sub: "1234567890", name: "John Doe", iat: 1516239022 }
```
````

**After Code: Explain It (2-4 sentences)**

```markdown
When you run this code, you'll see the payload contents clearly displayed—including the subject (`sub`), name, and issued-at time (`iat`). Notice how easy it is to read the payload without any secret key or password. This demonstrates why sensitive data should never be stored in JWTs: the payload is publicly readable to anyone with the token.
```

**Document Expected Outputs:**

Always show what happens when code runs:

````markdown
**When you run this code:**

```bash
node decode-jwt.js
```

**You'll see:**

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```
````

**Code Integration Pattern:**

1. **Introduction** - What we're about to do
2. **Code** - Complete, runnable example
3. **Explanation** - What happened and why it matters
4. **Output** - Expected results

### 4. Add Structure Elements

Convert outline headings and add narrative elements:

**Convert Outline Headings to Prose Headings:**

```markdown
**Outline:**

### Section 2: Understanding JWT Structure (4 pages)

**Prose:**

## Understanding JWT Structure

Before we can implement JWT authentication, we need to understand how these tokens are constructed. In this section, you'll learn about the three components that make up a JWT and how they work together to create a secure, tamper-evident token.
```

**Add Section Introductions:**

```markdown
## Security Considerations

Now that you understand JWT structure and implementation, let's examine the security implications. Even a correctly implemented JWT system can be vulnerable if you don't follow security best practices. In this section, we'll cover the most common vulnerabilities and how to prevent them.
```

**Add Transitions Between Sections:**

```markdown
We've covered how to create and verify JWTs, but how do you handle token expiration gracefully? In the next section, we'll explore token lifecycle management, including refresh tokens and logout strategies.
```

**Add Summary/Conclusion (if appropriate):**

```markdown
## Summary

In this chapter, you've learned how JWT authentication works, from understanding token structure to implementing complete authentication flows. The key takeaways are:

- JWTs are signed (integrity) but not encrypted (confidentiality)
- Always verify signatures before trusting token contents
- Use HTTPS to protect tokens in transit
- Store tokens securely (httpOnly cookies preferred)
- Implement token expiration and refresh strategies

With this foundation, you're ready to build secure, stateless authentication systems for modern web applications.
```

### 5. Quality Check (HUMAN REQUIRED)

**⚠️ MANDATORY VERIFICATION STEPS:**

**Verify Technical Accuracy:**

- [ ] ⚠️ Check all technical claims against authoritative sources
- [ ] ⚠️ Verify code examples are correct (don't just assume)
- [ ] ⚠️ Confirm algorithms, syntax, and APIs are accurate
- [ ] ⚠️ Ensure no hallucinated libraries, functions, or features

**Check Tone is Appropriate:**

- [ ] Matches target audience level
- [ ] Consistent voice throughout
- [ ] Neither too formal nor too casual
- [ ] Encouraging and accessible

**Ensure Completeness:**

- [ ] All outline points addressed
- [ ] No sections skipped
- [ ] Transitions present
- [ ] Structure makes sense

**Verify Code Examples:**

- [ ] ⚠️ Code runs without errors
- [ ] Outputs match documentation
- [ ] Dependencies are correct
- [ ] Examples demonstrate intended concepts

**Mark as DRAFT:**

This is AI-expanded content requiring technical review. Do NOT treat as final.

### 6. Save as Draft

**Save with Clear Draft Status:**

```markdown
**File naming:**

- section-2-jwt-structure-DRAFT.md
- chapter-5-oauth-flow-DRAFT.md

**Add Metadata Note at Top:**

---

status: DRAFT - AI-Expanded from Outline
requires: Technical Review
source_outline: outlines/chapter-5-outline.md
expanded_date: 2024-01-15
reviewer: [PENDING]

---

⚠️ **AI-EXPANDED DRAFT - REQUIRES TECHNICAL REVIEW**

This document was AI-generated from a bullet-point outline. All technical
claims, code examples, and explanations must be verified by a subject matter
expert before publication.
```

**Track Source Outline:**

- Document which outline this came from
- Link to original outline file
- Note any deviations or additions
- Record expansion date

## Expansion Guidelines

### Do:

✅ **Expand bullets into flowing prose**

- Convert terse bullets into readable paragraphs
- Add natural language connectors
- Create smooth narrative flow

✅ **Use transitions between points**

- Connect ideas logically
- Show relationships between concepts
- Guide reader through progression

✅ **Add explanatory detail**

- Clarify technical concepts
- Provide context and motivation
- Explain significance

✅ **Maintain outline structure**

- Keep hierarchical organization
- Preserve section order
- Follow outline's teaching sequence

✅ **Frame code examples properly**

- Introduce before showing code
- Explain after showing code
- Document expected outputs

### Don't:

❌ **Add information not in outline**

- Stick to outline scope
- Don't invent new sections
- Don't add unsourced facts

❌ **Make technical claims without verification**

- Don't hallucinate APIs or features
- Don't assume code works
- Don't cite non-existent sources

❌ **Assume generated text is final**

- This is a DRAFT
- Technical review is mandatory
- Human judgment required

❌ **Skip human review step**

- Never publish AI-generated technical content without verification
- Code must be tested
- Claims must be verified

## Common Pitfalls to Avoid

**Over-Expansion:**

❌ Turning a concise outline into verbose text

✅ Add necessary detail but stay focused

**Under-Expansion:**

❌ Barely modifying bullet points ("JWT has three parts. The parts are...")

✅ Create genuine prose with explanation and context

**Inconsistent Tone:**

❌ Mixing formal academic language with casual slang

✅ Maintain consistent voice appropriate for audience

**Missing Code Context:**

❌ Dropping code blocks without explanation

✅ Always introduce, show, and explain code

**Ignoring Outline Structure:**

❌ Reorganizing or skipping outline sections

✅ Follow outline's structure and order

**Treating Draft as Final:**

❌ Publishing AI-generated content without review

✅ Always require human technical verification

## Quality Standards

A successful expansion produces:

✅ **Readable Prose:**

- Flowing paragraphs (not bullet-like sentences)
- Natural transitions between ideas
- Active voice predominates
- Clear, concise language

✅ **Well-Integrated Code:**

- Code introduced with context
- Code explained after showing
- Outputs documented
- Examples runnable and complete

✅ **Appropriate Detail:**

- Concept bullets → 2-4 sentences
- Detail bullets → 1-3 sentences
- Critical points emphasized
- Target audience level maintained

✅ **Structural Integrity:**

- Outline structure preserved
- Section headings clear
- Transitions present
- Introduction and summary included

✅ **Marked as DRAFT:**

- Clear draft status indicated
- Technical review required
- Source outline tracked
- Verification checklist included

## Example: Before and After

**Before (Outline):**

```markdown
### Section 3: Token Verification

- Signature verification is critical for security
- Use jsonwebtoken.verify() method
- Requires secret key that matches signing key
- Throws error if signature invalid
- [CODE: Verify token in Express middleware]
- Always verify before trusting payload claims
```

**After (Expanded Draft):**

````markdown
## Token Verification

The signature verification step is critical for JWT security—it's your application's guarantee that the token hasn't been tampered with. Without verification, an attacker could modify the payload (changing user IDs, permissions, or other claims) and your application would trust the altered data.

### Verifying Tokens in Practice

The `jsonwebtoken` library provides a `verify()` method that handles signature verification. This method requires the same secret key that was used to sign the token originally—if the keys don't match, or if the token has been modified in any way, verification will fail.

Let's see how to implement token verification in an Express middleware:

```javascript
const jwt = require('jsonwebtoken');
const SECRET_KEY = process.env.JWT_SECRET;

function authenticateToken(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const verified = jwt.verify(token, SECRET_KEY);
    req.user = verified;
    next();
  } catch (err) {
    return res.status(403).json({ error: 'Invalid token' });
  }
}
```
````

This middleware extracts the token from the Authorization header, then calls `jwt.verify()` with the secret key. If verification succeeds, the decoded payload is attached to the request object for downstream route handlers to use. If verification fails—whether due to signature tampering, expiration, or invalid format—an error is thrown and caught, returning a 403 Forbidden response.

**The critical principle:** Always verify the signature before trusting any claims from the payload. The payload is readable by anyone, but only a valid signature proves it came from your authentication server and hasn't been altered.

```

## AI-Assisted Drafting & Humanization

This section addresses AI-assisted content generation and the REQUIRED humanization workflow.

### Acknowledgment of AI Assistance

**If you use AI tools to assist with drafting** (including this task's AI execution via ChatGPT, Claude, Gemini, or similar), the resulting content **MUST be humanized before submission** to technical review.

**Why Humanization is Required:**

- Readers notice and complain about AI-generated patterns (documented in PacktPub reviews)
- Publishers require AI use declaration (PacktPub transparency requirement)
- AI patterns reduce content quality, credibility, and reader satisfaction
- Technical reviewers waste time on AI artifacts vs. substantive technical feedback
- Negative reviews specifically cite "AI-like" content

**PacktPub Official Requirement** (Generative_AI_Author_Guidelines.md):
> "Your editor can help you with this; we have many options to work on your writing to make it the best it can be... **to make it human**."

### AI Flag in Draft Metadata

**Output Metadata** (add to draft file header):

```markdown
---
status: DRAFT
ai_assisted: YES
created_date: {{date}}
outline_source: {{outline_file}}
tone_specification: {{tone_spec_file}}
requires_humanization: true
requires_technical_review: true
---
```

**If AI-Assisted = YES:**
- Humanization workflow is MANDATORY before technical review
- Next required step: humanize-ai-drafted-chapter.md
- Do not proceed to technical review without humanization

**If AI-Assisted = NO:**
- Humanization step can be skipped
- Proceed directly to technical review
- Note: Even human-written content may benefit from AI pattern checks if generic or formal

### Common AI Patterns to Avoid During Drafting

While humanization will systematically remove patterns, **try to avoid these during initial drafting** to reduce humanization effort:

#### Top 5 AI Patterns (will need removal during humanization):

1. **AI Vocabulary Overuse:**
   - sophisticated, delve, leverage, robust, seamless (use sparingly, ≤2 per chapter)
   - Polysyllabic words when simple ones work ("utilize" → "use", "facilitate" → "help")

2. **Metaphor Excess:**
   - Maximum 1-2 metaphors per section (not 4+ in single paragraph)
   - Avoid nonsense metaphors that confuse rather than clarify

3. **Generic Uncited Examples:**
   - NO: "a company", "financial institution", "company X"
   - YES: "Netflix's CDN architecture", "JPMorgan Chase fraud detection (cited)"

4. **Impersonal Voice:**
   - Encourage first-person perspective during drafting: "I've found that...", "In my experience..."
   - Include personal anecdotes, real projects, lessons learned

5. **Sentence Structure Uniformity:**
   - Vary sentence lengths (mix short 5-10, medium 10-20, long 20-30 words)
   - Avoid all sentences following same pattern (not all subject-verb-object)

**Note:** Full AI pattern list in ai-pattern-removal-guide.md (8 patterns with examples)

### Required Next Step: Humanization

**After drafting with AI assistance, you MUST execute:**

```
Draft Complete (AI-Assisted)
    ↓
humanize-ai-drafted-chapter.md ← MANDATORY NEXT STEP
    ↓
humanization-checklist.md (validation)
    ↓
Technical Review (only after humanization)
```

**Do NOT skip humanization:**
- Saves technical reviewer time (they review content, not AI artifacts)
- Prevents publisher rejection
- Avoids negative reader reviews
- Required for PacktPub compliance

### Humanization Workflow Summary

**Step 1: Baseline Detection**
- Execute generative-ai-compliance-checklist.md
- Document AI pattern score (baseline for improvement measurement)

**Step 2: Pattern Removal** (humanize-ai-drafted-chapter.md task executes 11 steps):
- Remove AI vocabulary (sophisticated, delve, leverage, etc.)
- Fix metaphor problems (overuse, nonsense)
- Introduce sentence rhythm variation
- Add personal voice and author perspective
- Replace generic examples with specific citations
- Remove filler, increase content depth
- Break rigid structural patterns
- Document all changes in change log

**Step 3: Validation**
- Execute humanization-checklist.md
- Target: ≥80% pass rate (≤20% AI patterns remaining)
- AI score improvement: ≥50% reduction from baseline

**Time Investment:** 2-4 hours per chapter for thorough humanization

**Quality Gate:** Do not proceed to technical review until humanization-checklist passes ≥80%

### PacktPub AI Declaration

**If using AI assistance for drafting:**

1. **Notify PacktPub editor immediately** - Transparency required
2. **Specify how AI was used** - "expand-outline-to-draft task with ChatGPT/Claude/Gemini"
3. **Confirm humanization executed** - Provide humanization-checklist results
4. **Acknowledge accountability** - Author remains accountable for accuracy, originality, integrity

**PacktPub Will:**
- Include AI use disclaimer in published book
- Work with you to ensure content quality meets standards
- Require humanization validation

### Integration with Tone Specification

**Relationship Between Tone & Humanization:**

| Concern | Tone Specification | Humanization |
|---------|-------------------|--------------|
| **Purpose** | Define consistent voice | Remove AI artifacts |
| **When** | Before writing (proactive) | After AI drafting (reactive) |
| **Question** | "Should we sound friendly or professional?" | "Does this sound AI-generated?" |
| **Focus** | Consistency, formality, style | Pattern removal, variation, authenticity |

**Workflow:**
```
Define Tone (before writing)
    ↓
AI Draft (using tone specification)
    ↓
Humanize (remove AI patterns while preserving tone)
    ↓
Copy-Edit (validate tone consistency + final AI pattern check)
    ↓
Publish
```

**Both are Required:**
- Tone specification ensures consistency
- Humanization ensures authenticity
- Together: consistent AND authentically human voice

### Cautionary Notes

**AI Content Risks:**
- **Accuracy:** AI may hallucinate facts, code, examples (always verify)
- **Quality:** Generic, superficial, lacks expert depth
- **Reputation:** Readers detect AI patterns, leave negative reviews
- **Publisher Trust:** Undisclosed AI use damages credibility
- **Legal/Ethical:** Author accountability for content integrity

**Author Responsibility:**
- YOU are accountable for every word in published book
- AI is tool for assistance, NOT replacement for expertise
- Humanization is NOT optional for AI-assisted content
- Technical verification MANDATORY before publication

**Best Practice:**
- Lead with your real expertise and experience
- Use AI for structural starting point, not final content
- Inject personal voice, insights, real-world examples during humanization
- Verify every technical claim
- Document AI use transparently

**Remember:** Your unique expertise, insights, and experience are what readers want—AI cannot replicate that value.

## Integration with Workflows

This task fits into content generation workflows:

**After Outline Creation:**

```

synthesize-research-notes.md
↓ (produces outline)
expand-outline-to-draft.md ← THIS TASK
↓ (produces prose draft with ai_assisted flag)
humanize-ai-drafted-chapter.md (if AI-assisted)
↓ (produces humanized draft)
Technical Review
↓
Editorial Polish + Final AI Pattern Check (Step 10)
↓
Final Content

```

**As Alternative to Manual Writing:**

```

Option A (Manual - No AI):
Outline → Write from scratch → Review → Polish

Option B (AI-Assisted - with Humanization):
Outline → expand-outline-to-draft.md → Humanize → Technical Review → Polish

Time Investment:
- Drafting: Save 2-4 hours (AI-assisted vs manual)
- Humanization: Invest 2-4 hours (AI pattern removal)
- Net: Similar time, but AI provides structural starting point
- Quality: Humanization ensures authentic expert voice

```

## Next Steps

After expanding outline to draft:

1. **Save draft with clear status** - Filename includes DRAFT, metadata indicates ai_assisted: YES/NO
2. **Execute humanization (if AI-assisted)** - MANDATORY: humanize-ai-drafted-chapter.md task
   - Execute generative-ai-compliance-checklist.md (baseline)
   - Remove AI patterns (vocabulary, metaphors, examples, voice, structure)
   - Validate with humanization-checklist.md (target: ≥80% pass)
   - Document changes in change log
3. **Test all code examples** - Run every code snippet in clean environment
4. **Technical review** - Subject matter expert verifies accuracy (AFTER humanization)
5. **Editorial polish** - Refine prose, improve clarity, final AI pattern check (Step 10)
6. **Final verification** - Check against outline completeness
7. **Remove DRAFT status** - Only after humanization + human verification complete

## Related Tasks

- **synthesize-research-notes.md** - Creates outlines (input to this task)
- **write-section-draft.md** - Manual section writing (alternative approach)
- **generate-explanation-variants.md** - Create multiple explanations for complex concepts
- **technical-review-section.md** - Review draft for technical accuracy
```

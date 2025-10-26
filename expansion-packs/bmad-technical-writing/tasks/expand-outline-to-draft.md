<!-- Powered by BMAD™ Core -->

# Expand Outline to Draft

---

task:
id: expand-outline-to-draft
name: Expand Outline to Draft
description: Convert bullet outline into initial prose draft for editing
persona_default: tutorial-architect
inputs: - outline (bullet-point format from research synthesis or chapter planning) - target-audience - tone-guidelines
steps: - Review complete outline and understand structure - Identify target audience and appropriate tone - Expand bullet points into flowing prose paragraphs - Integrate code examples at appropriate points - Add section introductions and transitions - Mark as DRAFT requiring human technical review
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
- **Tone guidelines** - Understand desired writing style
- **Code examples available** (if referenced in outline) - Have working code ready
- **Understanding of content domain** - Ability to verify technical accuracy

## Workflow Steps

### 1. Review Outline

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

### 2. Expand Bullet Points to Paragraphs

Convert each bullet point into flowing prose:

**Expansion Guidelines:**

**For Concept Bullets (2-4 sentences):**

- Start with clear topic sentence
- Add context and explanation
- Use appropriate technical terminology
- Maintain active voice
- Keep audience in mind

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

### 3. Integrate Code Examples

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

## Integration with Workflows

This task fits into content generation workflows:

**After Outline Creation:**

```

synthesize-research-notes.md
↓ (produces outline)
expand-outline-to-draft.md ← THIS TASK
↓ (produces prose draft)
Technical Review
↓
Editorial Polish
↓
Final Content

```

**As Alternative to Manual Writing:**

```

Option A (Manual):
Outline → Write from scratch → Review

Option B (AI-Assisted):
Outline → expand-outline-to-draft.md → Technical Review → Polish

Time Savings: 2-4 hours per chapter (depending on complexity)

```

## Next Steps

After expanding outline to draft:

1. **Save draft with clear status** - Filename includes DRAFT, metadata indicates AI-generated
2. **Test all code examples** - Run every code snippet in clean environment
3. **Technical review** - Subject matter expert verifies accuracy
4. **Editorial polish** - Refine prose, improve clarity
5. **Final verification** - Check against outline completeness
6. **Remove DRAFT status** - Only after human verification complete

## Related Tasks

- **synthesize-research-notes.md** - Creates outlines (input to this task)
- **write-section-draft.md** - Manual section writing (alternative approach)
- **generate-explanation-variants.md** - Create multiple explanations for complex concepts
- **technical-review-section.md** - Review draft for technical accuracy
```

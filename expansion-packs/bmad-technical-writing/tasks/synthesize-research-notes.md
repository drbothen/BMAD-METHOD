<!-- Powered by BMAD™ Core -->

# Synthesize Research into Content Outline

---

task:
id: synthesize-research-notes
name: Synthesize Research into Content Outline
description: Transform research notes into structured outline ready for chapter/section writing
persona_default: tutorial-architect
inputs: - research-notes - content-type (chapter, section, article)
steps: - Review all research notes and identify themes - Identify content structure based on teaching sequence - Extract key learning points and concepts - Create section-by-section content outline - Plan code examples from research - Apply content patterns (concept, tutorial, problem, comparison) - Add teaching guidance (analogies, visualizations) - Create citation list mapping sources to sections - Identify remaining gaps for follow-up
output: Structured content outline ready for writing (use with write-section-draft.md)

---

## Purpose

This task converts raw research notes into a structured content outline that's ready for writing. You'll organize findings into a logical teaching sequence with clear learning progression, code examples, and source attribution.

## Prerequisites

Before starting this task:

- Completed research notes (from research-technical-topic.md task)
- Clear content goal (chapter, section, or article)
- Target audience identified
- Learning objectives defined

## Workflow Steps

### 1. Review All Research Notes

Read through your research comprehensively:

**Initial review:**

- Read all research answers
- Read all key takeaways
- Review all code examples collected
- Note recurring themes/concepts

**Create research summary:**

```markdown
# Research Summary

**Total Questions Answered**: 30
**Key Sources**: 27
**Code Examples**: 15
**Research Time**: 4.5 hours

**Main Themes Identified**:

1. JWT structure and cryptography
2. Implementation patterns in Node.js
3. Security considerations
4. Token lifecycle management
5. Comparison with session-based auth
6. Production concerns

**Key Insights**:

- JWT is best for distributed/stateless systems
- Security requires HTTPS + careful secret management
- Multiple valid approaches for token storage
- Refresh tokens solve expiration UX problem
- RBAC can be implemented via JWT claims

**Conflicting Info to Resolve**:

- LocalStorage vs Cookie storage (context-dependent)
- Revocation strategies (multiple approaches)
```

**Identify what resonates:**

- Which concepts appeared repeatedly?
- What surprised you during research?
- What are the "aha!" moments?
- What are the practical takeaways?

### 2. Identify Content Structure

Determine how to organize the content:

**Consider target format:**

**For a book chapter (15-25 pages):**

- Introduction (1-2 pages)
- 3-5 main sections (3-6 pages each)
- Exercises (2-3 pages)
- Summary (1 page)

**For a section (2-5 pages):**

- Brief intro (0.5 page)
- Main content (1.5-4 pages)
- Brief wrap-up (0.5 page)

**For an article (1000-3000 words):**

- Hook/intro
- Problem statement
- Solution/implementation
- Example
- Conclusion

**Determine narrative flow:**

- **Simple to Complex**: Start with basics, build up
- **Problem to Solution**: Present challenge, then solve it
- **Comparison-driven**: Contrast approaches, then recommend
- **Tutorial-driven**: Step-by-step walkthrough
- **Concept-driven**: Explain ideas, then apply

**Map research to structure:**

```markdown
## Content Structure: JWT Authentication Chapter

**Teaching Approach**: Problem → Concept → Tutorial → Advanced

**Planned Structure**:

1. Introduction (2 pages)
   - Research: Q1 (What is JWT), Q7 (Problems it solves)

2. Understanding JWT (4 pages)
   - Research: Q4 (JWT components), Q8 (How signing works), Q9 (Algorithms)

3. Building Authentication Endpoints (5 pages)
   - Research: Q12 (Implementation), Q13 (Middleware), Q14 (Protected routes)

4. Token Lifecycle Management (4 pages)
   - Research: Q15 (Expiration), Q16 (Refresh tokens)

5. Security Best Practices (3 pages)
   - Research: Q17 (Vulnerabilities), Q18 (Best practices), Q19 (Storage)

6. Role-Based Access Control (3 pages)
   - Research: Q20 (RBAC implementation)

7. Testing and Troubleshooting (2 pages)
   - Research: Q26-Q29 (Errors, debugging, testing)

8. Summary and Exercises (2 pages)
   - Pull from all research

Total: 25 pages
```

### 3. Extract Key Learning Points

Identify the must-know takeaways:

**For each major section, answer:**

**What are the must-know concepts?**

- Core definitions
- Fundamental principles
- Critical facts

**What are common misconceptions?**

- What do people get wrong?
- What confusion did you encounter in research?
- What needs clarification?

**What are practical applications?**

- Real-world use cases
- When to apply this knowledge
- Concrete examples

**What are pitfalls to avoid?**

- Common mistakes from research
- Security vulnerabilities
- Performance issues
- Anti-patterns

**Example:**

```markdown
## Section: Understanding JWT Structure

**Must-Know Concepts**:

- JWT has three parts: header, payload, signature
- Payload is base64url encoded (readable, not encrypted)
- Signature prevents tampering but doesn't encrypt
- Standard claims: iss, sub, aud, exp, iat, jti

**Common Misconceptions**:

- "JWT is encrypted" → No, it's signed (integrity) not encrypted (confidentiality)
- "Put user password in JWT" → Never put sensitive data; payload is readable
- "JWT can't be tampered with" → True if signature verified; false if not checked

**Practical Applications**:

- User info in payload avoids database lookups
- Expiration claim (exp) enables time-limited access
- Custom claims support role-based access control

**Pitfalls to Avoid**:

- Storing sensitive data in payload
- Not validating signature
- Using weak signing secret
- Not handling expiration gracefully
```

### 4. Create Content Outline

Build detailed outline for each section:

**For each section, specify:**

```markdown
### Section 2: Understanding JWT Structure (4 pages, ~2000 words)

**Learning Objectives**:

- Explain the three components of a JWT
- Describe how JWT signing prevents tampering
- Identify standard JWT claims and their purposes
- Distinguish between encoding and encryption

**Content Flow**:

1. **Hook/Motivation** (0.5 pages)
   - "Have you ever wondered how a server validates tokens without a database lookup?"
   - Teaser: JWT's self-contained design

2. **JWT Structure Overview** (1 page)
   - Three parts: header.payload.signature
   - Visual diagram showing structure
   - Example token breakdown
   - Source: JWT.io introduction

3. **Header Component** (0.5 pages)
   - Contains algorithm (alg) and type (typ)
   - Example: `{"alg": "HS256", "typ": "JWT"}`
   - Why algorithm matters

4. **Payload Component** (1 page)
   - Registered claims (iss, sub, aud, exp, iat, jti)
   - Public claims (custom, namespaced)
   - Private claims (application-specific)
   - Example payload with user data
   - **Critical point**: Payload is encoded, NOT encrypted
   - Source: RFC 7519 Section 4

5. **Signature Component** (1 page)
   - How signature is computed: HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
   - Signature verification process
   - Why this prevents tampering
   - Code example: Creating and verifying signature
   - Source: JWT.io, Auth0 blog

**Key Concepts to Explain**:

- Base64url encoding vs encryption
- Signing vs encryption
- Claims and their purposes
- Token validation process

**Code Examples**:

1. Decoding JWT to see payload (jwt-decode library)
2. Creating JWT with custom claims (jsonwebtoken)
3. Verifying JWT signature (jsonwebtoken)

**Visuals Needed**:

1. Diagram: JWT structure (header.payload.signature)
2. Flowchart: How signature verification works
3. Screenshot: jwt.io debugger showing token parts

**Common Mistakes to Highlight**:

- Storing passwords or sensitive data in payload
- Assuming JWT is encrypted
- Not verifying signature before trusting payload

**Analogies/Explanations**:

- JWT like a sealed envelope: Contents visible (encoding), but seal (signature) proves authenticity
- Signature like wax seal on letter: Shows tampering, doesn't hide contents

**Exercises**:

1. Decode a JWT and identify claims
2. Explain why changing payload breaks signature
3. Create JWT with custom claims

**Sources to Cite**:

- JWT.io introduction
- RFC 7519 (JSON Web Token specification)
- Auth0 blog on JWT security
```

### 5. Plan Code Examples

Organize code from research:

**List all code examples needed:**

```markdown
## Code Examples Plan

### Example 1: Generating a JWT

- **Purpose**: Show basic token creation
- **Source**: JWT.io docs + Auth0 blog
- **File**: `examples/01-generate-token.js`
- **Dependencies**: jsonwebtoken
- **Teaching Point**: Token structure, payload claims, expiration
- **Page Estimate**: 0.5 pages

### Example 2: Verifying a JWT

- **Purpose**: Show signature validation
- **Source**: jsonwebtoken GitHub
- **File**: `examples/02-verify-token.js`
- **Dependencies**: jsonwebtoken
- **Teaching Point**: Security through verification
- **Page Estimate**: 0.5 pages

### Example 3: Express Auth Middleware

- **Purpose**: Real-world integration
- **Source**: Stack Overflow + own design
- **File**: `examples/03-auth-middleware.js`
- **Dependencies**: express, jsonwebtoken
- **Teaching Point**: Protecting routes, error handling
- **Page Estimate**: 1 page

[...continue for all examples...]
```

**Design progressive example sequence:**

1. **Basic example**: Minimal, focused on one concept
2. **Extended example**: Add realistic details
3. **Production example**: Full implementation with error handling
4. **Advanced example**: Optimization or advanced technique

**Document expected learning:**

- What does each example teach?
- What new concept does it introduce?
- How does it build on previous examples?

### 6. Apply Content Patterns

Use proven teaching patterns:

#### Concept Introduction Pattern

```markdown
**Pattern**: Definition → Motivation → Context → Example

**Application**:

1. What is [concept]? (Definition)
2. Why does [concept] matter? (Motivation)
3. Where does [concept] fit? (Context)
4. Show [concept] in action (Example)
```

#### Tutorial Pattern

```markdown
**Pattern**: Setup → Build → Verify → Extend

**Application**:

1. Prerequisites and setup
2. Step-by-step implementation
3. Test and verify it works
4. Discuss next steps/variations
```

#### Problem-Solution Pattern

```markdown
**Pattern**: Problem → Consequences → Solution → Implementation

**Application**:

1. Present the problem/challenge
2. Show why it matters (consequences of not solving)
3. Introduce the solution
4. Walk through implementation
```

#### Comparison Pattern

```markdown
**Pattern**: Option A → Option B → Trade-offs → Recommendation

**Application**:

1. Explain approach A
2. Explain approach B
3. Compare side-by-side
4. When to use each
```

#### Troubleshooting Pattern

```markdown
**Pattern**: Symptom → Cause → Solution → Prevention

**Application**:

1. Describe the error/problem
2. Explain root cause
3. Show how to fix
4. Discuss how to prevent
```

**Apply to each section:**

```markdown
### Section 3: Building Authentication Endpoints (Tutorial Pattern)

**Pattern Applied**: Setup → Build → Verify → Extend

**Setup** (0.5 pages):

- Install dependencies (express, jsonwebtoken)
- Create basic Express app
- Define routes structure

**Build** (3 pages):

- Step 1: Create login endpoint
- Step 2: Generate JWT on successful auth
- Step 3: Return token to client
- Step 4: Create protected route
- Step 5: Add auth middleware

**Verify** (0.5 pages):

- Test with curl/Postman
- Verify token format
- Test protected route with/without token

**Extend** (1 page):

- Add error handling
- Add token refresh
- Add logout (blacklist approach)
```

### 7. Identify Gaps

Note what's missing:

**Content gaps:**

- [ ] What concepts need more explanation?
- [ ] What examples are missing?
- [ ] What questions weren't fully answered?
- [ ] What transitions need smoothing?

**Research gaps:**

- [ ] What needs deeper investigation?
- [ ] What sources are needed for citation?
- [ ] What code examples need to be written/tested?
- [ ] What visuals need to be created?

**Example:**

```markdown
## Identified Gaps

**Need More Research**:

- [ ] JWT revocation strategies (only surface-level coverage)
- [ ] Production-scale performance data (no benchmarks found)
- [ ] Specific attack vectors and mitigation (need security-focused source)

**Need to Create**:

- [ ] Complete working example app (no source found, must build)
- [ ] Diagram showing token flow from login to protected route
- [ ] Comparison table: JWT vs Session (consolidate from multiple sources)

**Need to Clarify**:

- [ ] LocalStorage vs Cookie debate (present both sides clearly)
- [ ] When to use HS256 vs RS256 (needs decision framework)
```

### 8. Add Teaching Guidance

Enhance outline with pedagogical notes:

**For complex concepts:**

```markdown
### Teaching JWT Signature Verification

**Best Explanation Approach**:

- Use analogy: Wax seal on envelope
- Visual: Show signature computation step-by-step
- Code walkthrough: Line-by-line explanation
- Interactive: jwt.io debugger

**Analogies That Work** (from research):

- Signature = tamper-evident seal
- Payload = postcard (anyone can read)
- Secret key = royal seal stamp

**Visualizations Needed**:

- Flowchart: Signature creation process
- Diagram: Verification flow
- Screenshot: jwt.io showing signature change when payload modified

**Common Stumbling Blocks**:

- Confusion between encoding and encryption
- Not understanding why signature matters
- Thinking signature hides payload

**How to Address**:

- Explicitly contrast encoding vs encryption
- Demonstrate tampering detection
- Show base64 decoding to prove payload readable
```

**Exercises and challenges:**

```markdown
### Section Exercises

**Guided Exercise 1** (Reinforcement):

- Task: Create JWT with custom claims (name, role, permissions)
- Solution: Provided in full
- Estimated Time: 10 minutes
- Learning Goal: Understand claims and payload structure

**Guided Exercise 2** (Application):

- Task: Build middleware that checks user role from JWT
- Solution: Provided in full
- Estimated Time: 15 minutes
- Learning Goal: Apply JWT in authorization context

**Challenge Exercise** (Stretch Goal):

- Task: Implement token refresh logic
- Solution: Hints only, no full solution
- Estimated Time: 30 minutes
- Learning Goal: Design token lifecycle management

**Self-Assessment Questions**:

1. Why is the JWT payload not encrypted?
2. What happens if you change one character in the payload?
3. When should you use refresh tokens?
```

### 9. Create Citation List

Map sources to content sections:

```markdown
## Source Attribution Map

### Section 1: Introduction

- JWT.io Introduction (general overview)
- RFC 7519 (formal definition)

### Section 2: Understanding JWT Structure

- JWT.io Introduction (structure explanation, diagrams)
- RFC 7519 Section 4 (claims specification)
- Auth0 Blog "JWT Security Best Practices" (encoding vs encryption)

### Section 3: Building Authentication Endpoints

- jsonwebtoken GitHub repository (code examples)
- Express.js documentation (middleware patterns)
- Stack Overflow #43452896 (protected routes pattern)

### Section 4: Token Lifecycle

- Auth0 Blog "Refresh Tokens" (refresh token flow)
- JWT.io Introduction (expiration handling)

### Section 5: Security Best Practices

- Auth0 Blog "JWT Security" (vulnerabilities, mitigations)
- OWASP JWT Cheat Sheet (security guidance)
- RFC 7519 Section 8 (security considerations)

[...continue for all sections...]

---

## Bibliography (Full Citations)

1. **JWT.io Introduction**
   - URL: https://jwt.io/introduction
   - Accessed: January 15, 2024
   - Used in: Sections 1, 2, 4

2. **RFC 7519 - JSON Web Token (JWT)**
   - URL: https://tools.ietf.org/html/rfc7519
   - Date: May 2015
   - Used in: Sections 1, 2, 5

[...continue for all sources...]
```

### 10. Finalize Content Outline

Create polished outline document:

**Final outline format:**

```markdown
# Content Outline: JWT Authentication in Node.js

**Content Type**: Book Chapter (Chapter 8)
**Target Length**: 25 pages (~12,500 words)
**Target Audience**: Intermediate developers
**Prerequisites**: Node.js, Express.js, basic authentication concepts

**Learning Objectives**:

1. Explain JWT structure and how signing ensures integrity
2. Implement JWT authentication in Express.js application
3. Handle token lifecycle (generation, verification, refresh, expiration)
4. Apply security best practices for production JWT usage
5. Implement role-based access control using JWT claims

---

## Section-by-Section Outline

### Section 1: Introduction to JWT Authentication (2 pages)

[Complete outline as shown in step 4...]

### Section 2: Understanding JWT Structure (4 pages)

[Complete outline as shown in step 4...]

### Section 3: Building Authentication Endpoints (5 pages)

[Complete outline...]

[...continue for all sections...]

---

## Code Examples Summary

**Total Examples**: 8

1. Generate JWT with claims
2. Verify JWT signature
3. Express auth middleware
4. Protected route handler
5. Token refresh endpoint
6. RBAC middleware
7. Complete authentication flow
8. Unit tests for auth logic

**Code Repository Structure**:
```

chapter-08-jwt-auth/
├── examples/
│ ├── 01-generate-token.js
│ ├── 02-verify-token.js
│ ├── 03-auth-middleware.js
│ └── ...
├── complete-app/
│ ├── server.js
│ ├── routes/auth.js
│ ├── middleware/auth.js
│ └── tests/auth.test.js
└── package.json

```

---

## Visuals and Diagrams

1. **JWT Structure Diagram** (Section 2)
   - Shows header.payload.signature

2. **Signature Verification Flow** (Section 2)
   - Flowchart of verification steps

3. **Authentication Flow** (Section 3)
   - Sequence diagram: Login → Token → Protected Resource

4. **Refresh Token Flow** (Section 4)
   - Diagram showing token expiration and refresh

5. **JWT vs Session Comparison Table** (Section 1)
   - Side-by-side feature comparison

---

## Exercises and Assessments

**Guided Exercises**: 6
**Challenge Problems**: 2
**Self-Assessment Questions**: 12

[Details in each section outline...]

---

## Sources and Citations

**Total Sources**: 27
**Primary Sources**: 8
**Secondary Sources**: 15
**Tertiary Sources**: 4

[Full bibliography in Section 9 format...]

---

## Outstanding Tasks

**Research Follow-up**:
- [ ] Deep dive on JWT revocation (need better sources)
- [ ] Find production performance benchmarks

**Content Creation**:
- [ ] Build complete example application
- [ ] Create all diagrams
- [ ] Write all code examples
- [ ] Test all code in clean environment

**Review Needed**:
- [ ] Technical review of security section
- [ ] Code review of examples
- [ ] Verify all sources are current

---

**Outline Status**: Ready for Writing
**Next Step**: Begin drafting Section 1 with write-section-draft.md task
**Estimated Writing Time**: 12-15 hours
```

**Save outline:**

- `docs/outlines/chapter-08-jwt-outline.md` (or user-specified location)

## Success Criteria

A successful synthesized outline has:

- [ ] Clear structure with logical progression
- [ ] Each section has detailed content plan
- [ ] Learning objectives defined for chapter/sections
- [ ] Code examples planned and sourced
- [ ] Teaching patterns applied appropriately
- [ ] Visual/diagram needs identified
- [ ] Exercises and assessments planned
- [ ] Sources mapped to sections for citation
- [ ] Content gaps identified for follow-up
- [ ] Ready to begin writing immediately
- [ ] Realistic page/time estimates

## Common Pitfalls to Avoid

- **Too vague**: "Explain JWT" vs detailed section breakdown
- **No progression**: Random order instead of scaffolded learning
- **Missing code**: Tutorial content needs code examples
- **No sources**: Can't cite claims or verify accuracy
- **Poor balance**: All theory or all code, no mix
- **No exercises**: Readers need practice opportunities
- **Unrealistic scope**: 25-page outline that's really 50 pages
- **Gaps ignored**: Knowing you're missing content but not noting it
- **No teaching guidance**: Missing pedagogical notes for complex topics

## Example: Before and After Synthesis

**Before (Raw Research Notes)**:

- Q8: How does JWT signing work? Answer: Uses HMAC with secret key to create signature...
- Q9: What algorithms? Answer: HS256, RS256, ES256...
- Q14: How to protect routes? Answer: Use middleware to verify token...

**After (Synthesized Outline)**:

```markdown
### Section 2: Understanding JWT Security Model (3 pages)

**Teaching Approach**: Problem → Solution → Implementation

**Content**:

1. **Problem**: How does server trust unsigned data? (0.5 pages)
   - Motivation for signing
   - Attack vector: Tampered tokens

2. **Solution**: Cryptographic Signatures (1.5 pages)
   - How HMAC signing works
   - Algorithm comparison: HS256 vs RS256 vs ES256
   - When to use each algorithm
   - Sources: RFC 7519 Section 8, Auth0 algorithm comparison

3. **Implementation**: Protecting Routes (1 page)
   - Code example: Auth middleware
   - Signature verification process
   - Error handling for invalid tokens
   - Source: Express middleware pattern, jsonwebtoken docs

**Code**: Express middleware with verification (15 lines)
**Visual**: Signing algorithm comparison table
**Exercise**: Modify middleware to log failed attempts
```

## Next Steps

After synthesizing research into outline:

1. Review outline with technical expert or co-author
2. Validate that outline achieves learning objectives
3. Create code examples and test thoroughly
4. Create diagrams and visuals
5. Begin writing with write-section-draft.md task
6. Use outline as roadmap during writing

<!-- Powered by BMAD™ Core -->

# Research Technical Topic

---

task:
id: research-technical-topic
name: Research Technical Topic
description: Systematic research workflow with source tracking and comprehensive note-taking
persona_default: book-analyst
inputs: - research-questions-list - topic
steps: - Organize research questions by category and priority - Identify authoritative research sources (docs, papers, blogs, repos) - For each question systematically search, evaluate, and document answers - Take structured notes with source attribution - Track research progress (not started, in progress, complete) - Verify critical information across multiple sources - Test code examples when applicable - Organize research notes by category - Create source index for citations
output: Comprehensive research notes with tracked sources ready for synthesis

---

## Purpose

This task provides a systematic workflow for researching technical topics with proper source tracking. Instead of scattered research, you'll create organized, well-sourced notes that can be synthesized into high-quality content.

## Prerequisites

Before starting this task:

- Research questions list (from generate-research-questions.md task)
- Access to research tools (web browser, AI tools like Perplexity/ChatGPT, documentation)
- Clear research goal (chapter, section, article)
- Time allocation (estimate 2-4 hours for comprehensive research)

## Workflow Steps

**Note:** This task references config paths (e.g., {{config.manuscript.*}}). Load `.bmad-technical-writing/config.yaml` at the start to resolve these paths, or use defaults: `manuscript/{type}`, `code-examples`.

### 1. Organize Research Questions

Structure your research approach:

**Review question list:**

- Total questions to answer
- Categories (foundational, technical, practical, advanced, troubleshooting)
- Estimated effort per question

**Prioritize questions:**

**Critical (must answer):**

- Core to understanding topic
- Necessary for target content
- Foundational knowledge

**Important (should answer):**

- Enhances understanding significantly
- Best practices and patterns
- Common use cases

**Optional (nice to answer):**

- Advanced topics
- Edge cases
- Bonus content

**Identify dependencies:**

- Which questions should be answered first?
- Do some questions inform others?
- What's the logical research sequence?

**Create research plan:**

```markdown
## Research Plan: [Topic]

**Time Budget**: 3 hours
**Priority**: Critical questions first, then important, then optional

### Phase 1: Foundational (30 min, 7 questions)

- Question 1 (critical)
- Question 2 (critical)
  [...]

### Phase 2: Technical Deep-Dive (60 min, 8 questions)

[...]

### Phase 3: Practical Application (45 min, 9 questions)

[...]

### Phase 4: Advanced Topics (30 min, 4 questions)

[...]

### Phase 5: Troubleshooting (15 min, 4 questions)

[...]
```

### 2. Identify Research Sources

Know where to look:

**Primary Sources (Highest Trust):**

- **Official Documentation**
  - Language/framework official docs
  - API references
  - Official guides and tutorials
  - Trust: High, Currency: Varies, Use: Definitions, specs, official guidance

- **RFCs and Specifications**
  - IETF RFCs for protocols
  - W3C specifications
  - Industry standards
  - Trust: Authoritative, Currency: Varies, Use: Technical specifications

- **Source Code**
  - Official GitHub repositories
  - Reference implementations
  - Trust: Highest for "how it works", Use: Architecture understanding

**Secondary Sources (Medium Trust):**

- **Technical Blogs**
  - Engineering blogs (e.g., Netflix, Airbnb tech blogs)
  - Personal developer blogs
  - Medium, Dev.to articles
  - Trust: Medium (verify claims), Currency: Check dates, Use: Patterns, real-world usage

- **Stack Overflow / Forums**
  - Stack Overflow answers
  - GitHub Discussions
  - Reddit (r/programming, tech-specific subs)
  - Trust: Medium (community-validated), Use: Troubleshooting, common issues

- **Books and Courses**
  - Technical books (O'Reilly, Manning, Packt)
  - Online courses (Udemy, Pluralsight)
  - Trust: High for established publishers, Use: Comprehensive coverage

**Tertiary Sources (Verify First):**

- **Tutorials and How-Tos**
  - Random tutorials online
  - YouTube videos
  - Trust: Low to Medium (test everything), Use: Alternative explanations, examples

**Tools:**

- **AI Research Tools**
  - Perplexity AI (with source citations)
  - ChatGPT / Claude (verify outputs)
  - GitHub Copilot (for code examples)
  - Trust: Medium (always verify), Use: Quick answers, pattern discovery

### 3. Systematic Research Process (Per Question)

For each question, follow this workflow:

#### Step 1: State the Question Clearly

```markdown
## Question 1: What is JWT and how does it differ from session-based authentication?

**Category**: Foundational
**Priority**: Critical
**Estimated Time**: 15 minutes
**Status**: In Progress
```

#### Step 2: Search for Answers

**Search strategy:**

1. Start with official documentation
   - Google: "[topic] official documentation"
   - Visit official website/docs

2. Check authoritative sources
   - RFCs, specifications if applicable
   - Established technical resources (MDN, etc.)

3. Supplement with secondary sources
   - Technical blogs from reputable companies
   - Stack Overflow top answers
   - Relevant books/courses

4. Use AI tools for synthesis
   - Perplexity AI with "Find sources" mode
   - ChatGPT/Claude for explanations (verify with sources)

#### Step 3: Evaluate Sources

**For each source, assess:**

- **Authority**: Who wrote this? Are they credible?
- **Currency**: When was this published? Is it up-to-date?
- **Accuracy**: Does it match other sources? Any red flags?
- **Coverage**: Does it answer the question fully?
- **Clarity**: Is the explanation understandable?

**Red flags:**

- Very old content (pre-2020 for fast-moving tech)
- No author attribution
- Conflicts with official docs
- Poor English/obvious errors
- No sources cited for claims

#### Step 4: Take Structured Notes

Use this format for each question:

```markdown
## Question 1: What is JWT and how does it differ from session-based authentication?

**Answer**:

JWT (JSON Web Token) is a stateless authentication mechanism where the server generates a signed token containing user information and sends it to the client. The client includes this token in subsequent requests. Unlike session-based auth where server stores session data, JWT is self-contained and the server validates the token signature without needing to look up session storage.

**Key Differences**:

- JWT: Stateless, token stored client-side, server validates signature
- Session: Stateful, session stored server-side, cookie contains session ID
- JWT: Better for distributed systems/microservices (no shared session store needed)
- Session: Easier to revoke access (delete server-side session)

**Sources**:

1. **JWT.io Introduction** (https://jwt.io/introduction)
   - Official JWT website
   - Explains structure (header.payload.signature)
   - Diagrams showing flow
   - Trust: High | Date: 2024

2. **RFC 7519 - JSON Web Token** (https://tools.ietf.org/html/rfc7519)
   - Official specification
   - Technical definition of JWT structure
   - Trust: Authoritative | Date: 2015 (stable spec)

3. **Auth0 Blog: JWT vs Sessions** (https://auth0.com/blog/jwt-vs-sessions/)
   - Comparison table
   - Real-world trade-offs
   - Security considerations
   - Trust: High (Auth0 is authority on auth) | Date: 2023

4. **Stack Overflow: JWT vs Session Cookies** (https://stackoverflow.com/questions/43452896/)
   - Community discussion
   - Multiple perspectives
   - 450+ upvotes
   - Trust: Medium | Date: 2019 (check if still accurate)

**Key Takeaways**:

- JWT is stateless; session is stateful
- JWT better for distributed systems
- Sessions easier to revoke
- JWT requires careful security (HTTPS, secret management)
- Both have valid use cases

**Code Examples**:
(Will need to create example showing both approaches)

**Open Questions**:

- How do you handle JWT revocation? (Research in later question)
- What are specific security best practices? (Covered in security question)

**Confidence Level**: High (multiple authoritative sources agree)
```

#### Step 5: Document Code Examples

When you find code:

```markdown
**Code Example**: Basic JWT Generation (Node.js)

**Source**: JWT.io documentation

**Language**: JavaScript (Node.js)

**Dependencies**: jsonwebtoken package

**Code**:
\`\`\`javascript
const jwt = require('jsonwebtoken');

const token = jwt.sign(
{ userId: 123, email: 'user@example.com' },
'your-secret-key',
{ expiresIn: '1h' }
);

console.log(token);
// eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
\`\`\`

**Notes**:

- Never hardcode secrets in production
- Token expires in 1 hour (expiresIn)
- Payload should not contain sensitive data (it's base64 encoded, not encrypted)

**Testing Status**: Not yet tested (will test in code example creation phase)

**Attribution**: https://jwt.io/introduction
```

#### Step 6: Note Conflicting Information

When sources disagree:

```markdown
**Conflicting Information Noted**:

**Question**: Should JWTs be stored in localStorage or cookies?

**Position A** (Source: Auth0 Blog):

- Use httpOnly cookies for better XSS protection
- LocalStorage vulnerable to XSS attacks
- Cookies auto-sent by browser (secure if configured correctly)

**Position B** (Source: Some Medium articles):

- Use localStorage for easier mobile app integration
- Cookies subject to CSRF (require CSRF tokens)
- LocalStorage gives more control

**Resolution**:

- Security best practice: httpOnly cookies (prevents XSS access)
- Trade-off: Cookies require CSRF protection
- Context matters: SPA vs traditional web app
- Recommendation: httpOnly cookies + SameSite attribute + CSRF tokens

**Confidence**: Medium (context-dependent, both approaches have merit)
```

### 4. Track Research Progress

Maintain a progress tracker:

**Create status document:**

```markdown
# Research Progress: JWT Authentication

**Started**: 2024-01-15
**Last Updated**: 2024-01-15 14:30
**Total Questions**: 32
**Completed**: 8
**In Progress**: 2
**Not Started**: 22

## Status by Category

### Foundational Questions (7 total)

- [x] Q1: What is JWT? (Completed - 15 min)
- [x] Q2: Why use JWT? (Completed - 10 min)
- [x] Q3: When to use JWT? (Completed - 12 min)
- [ ] Q4: JWT components (In Progress)
- [ ] Q5: Where are JWTs used? (Not Started)
- [ ] Q6: Who created JWT? (Not Started)
- [ ] Q7: What problems does JWT solve? (Not Started)

### Technical Deep-Dive (9 total)

[...]

**Notes**:

- Q1-Q3 took longer than expected (quality sources found)
- Need to allocate more time for technical deep-dive questions
- Found excellent resource: Auth0 blog has comprehensive guides
```

**Update regularly:**

- Mark questions as you complete them
- Note time spent per question
- Identify blockers or difficult questions
- Adjust timeline as needed

### 5. Verify Critical Information

For important claims, cross-reference:

**Verification checklist:**

- [ ] **Check official documentation**
  - Does official source confirm this claim?

- [ ] **Cross-reference multiple sources**
  - Do 2+ independent sources agree?

- [ ] **Check publication date**
  - Is this information current?
  - Has the technology changed since?

- [ ] **Test code examples**
  - Does the code actually work?
  - Are there errors or outdated syntax?

- [ ] **Verify statistics/data**
  - What's the original source?
  - Is the data current?

**Mark confidence level for each answer:**

- **High**: 3+ authoritative sources agree, tested if code
- **Medium**: 2 sources agree, or single authoritative source
- **Low**: Single source, not verified, or conflicting information

### 6. Test Code Examples

When research includes code:

**Testing workflow:**

1. **Extract code snippet** from source
2. **Set up test environment**
   - Create test project/file
   - Install dependencies
   - Match versions if specified

3. **Run the code**
   - Does it execute without errors?
   - Does it produce expected output?

4. **Document results**

   ```markdown
   **Test Results**: JWT Generation Example

   - Environment: Node.js 18.12.0
   - Package: jsonwebtoken@9.0.0
   - Status: ✅ Works as documented
   - Notes: None
   ```

5. **Note modifications needed**
   - Did you need to change anything?
   - What wasn't included in the example?
   - What dependencies were missing?

**Save tested examples:**

- Organize in `research/{{config.codeExamples.root}}/` folder
- Include comments noting source
- Mark which examples to include in book

### 7. Organize Research Notes

Structure your findings:

**Create organized research document:**

```markdown
# Research Notes: JWT Authentication in Node.js

**Research Date**: January 15-16, 2024
**Total Questions Researched**: 32
**Time Spent**: 4.5 hours
**Sources Consulted**: 27

---

## Foundational Concepts

### What is JWT?

[Notes from Q1]

### Why Use JWT?

[Notes from Q2]

[...continue for all foundational questions...]

---

## Technical Deep-Dive

### JWT Structure and Signing

[Notes from technical questions]

[...continue...]

---

## Practical Application

### Implementation in Node.js

[Notes from practical questions]

[...continue...]

---

## Advanced Topics

### Security Considerations

[Notes from security questions]

[...continue...]

---

## Troubleshooting

### Common Errors

[Notes from troubleshooting questions]

[...continue...]

---

## Code Examples Collected

1. **JWT Generation** (jwt.io)
2. **JWT Verification** (Auth0 docs)
3. **Express Middleware** (Stack Overflow)
   [...list all examples with sources...]

---

## Open Questions / Need More Research

- [ ] JWT revocation strategies (need deeper dive)
- [ ] Performance at scale (need case studies)
- [ ] Specific security attack vectors (need security-focused research)

---

## Next Steps

1. Synthesize notes into content outline
2. Test all code examples in clean environment
3. Create diagrams for JWT flow
4. Identify which sections need which sources cited
```

**Save organized notes:**

- `docs/research/[topic]-research-notes.md`

### 8. Create Source Index

Build citation reference:

**Format:**

```markdown
# Source Index: JWT Authentication Research

## Official Documentation

1. **JWT.io Introduction**
   - URL: https://jwt.io/introduction
   - Type: Official Documentation
   - Authority: High
   - Date Accessed: 2024-01-15
   - Key Topics: JWT structure, basic concepts
   - Notes: Excellent diagrams, code examples in multiple languages

2. **RFC 7519 - JSON Web Token**
   - URL: https://tools.ietf.org/html/rfc7519
   - Type: Specification
   - Authority: Authoritative
   - Date: May 2015
   - Key Topics: Technical specification, formal definition
   - Notes: Dry but definitive

## Technical Articles

1. **Auth0: JWT vs Sessions**
   - URL: https://auth0.com/blog/jwt-vs-sessions/
   - Author: Auth0 Team
   - Authority: High (auth domain experts)
   - Published: 2023-03-15
   - Key Topics: Comparison, trade-offs, security
   - Notes: Best practical comparison found

[...continue for all sources...]

## Books Referenced

1. **"OAuth 2 in Action"** by Justin Richer
   - Publisher: Manning
   - Year: 2017
   - Pages Referenced: 45-67
   - Topics: JWT in OAuth context

## Code Examples

1. **jsonwebtoken GitHub Repository**
   - URL: https://github.com/auth0/node-jsonwebtoken
   - Stars: 15k+
   - Last Updated: 2024-01-10
   - Topics: Official library, examples, best practices

---

**Total Sources**: 27
**Primary Sources**: 8
**Secondary Sources**: 15
**Tertiary Sources**: 4
```

### 9. Document Research Session Metadata

Track your research effort:

```markdown
# Research Session Metadata

**Topic**: JWT Authentication in Node.js
**Research Goal**: Chapter 8 content
**Researcher**: [Your Name]
**Date**: January 15-16, 2024
**Time Spent**: 4.5 hours

## Time Breakdown

- Foundational research: 1 hour
- Technical deep-dive: 1.5 hours
- Practical implementation: 1 hour
- Code testing: 45 minutes
- Organization/note-taking: 15 minutes

## Questions Researched

- Total: 32
- Completed: 30
- Skipped: 2 (out of scope)

## Sources Consulted

- Official docs: 8
- Technical blogs: 12
- Stack Overflow: 4
- Books: 1
- RFCs/Specs: 2

## Code Examples

- Found: 15
- Tested: 8
- Will use in chapter: 6

## Key Findings

- JWT best suited for stateless, distributed systems
- Security requires careful implementation
- Multiple approaches exist for token storage (context-dependent)

## Confidence Assessment

- High confidence: 22 answers
- Medium confidence: 7 answers
- Low confidence: 1 answer (need more research)

## Follow-up Needed

- Deeper dive on JWT revocation strategies
- Find production-scale case studies
- Research specific attack vectors
```

## Success Criteria

Successful research produces:

- [ ] All critical questions answered with sources
- [ ] Structured notes for each question
- [ ] Source attribution for all claims
- [ ] Code examples collected and tested
- [ ] Conflicting information resolved or noted
- [ ] Confidence level assessed for each answer
- [ ] Research notes organized by category
- [ ] Source index created for citations
- [ ] Open questions identified for follow-up
- [ ] Research ready for synthesis into content

## Common Pitfalls to Avoid

- **No source tracking**: Can't cite or verify later
- **Relying on single source**: Lack of verification
- **Ignoring publication dates**: Using outdated info
- **Not testing code**: Examples may not work
- **Poor note organization**: Can't find information later
- **Too shallow**: Answering "what" but not "how" or "why"
- **Rabbit holes**: Spending 2 hours on one question
- **No confidence assessment**: Don't know what to trust
- **Copy-paste without understanding**: Notes are useless
- **Skipping conflicting info**: Missing important nuances

## Tips for Efficient Research

**Time management:**

- Set time limits per question (10-20 min typical)
- Use timer to avoid rabbit holes
- Mark complex questions for deeper dive later
- Don't perfect; iterate

**Source evaluation:**

- Start with official docs (saves time)
- Use CTRL+F to scan long documents
- Check dates immediately (skip old content)
- Trust GitHub stars/Stack Overflow votes as quality signals

**Note-taking:**

- Write notes in your own words (tests understanding)
- Include "why this matters" context
- Use bullet points for scannability
- Link related questions

**Tool usage:**

- Use Perplexity AI for quick answers with sources
- Use ChatGPT/Claude for explanation, but verify
- Use browser bookmarks/tabs for session management
- Use note-taking tools (Notion, Obsidian, etc.)

## Next Steps

After completing technical research:

1. Review research notes for completeness
2. Fill gaps with additional targeted research
3. Test all code examples in clean environment
4. Use synthesize-research-notes.md to create content outline
5. Begin writing with well-sourced material
6. Prepare citation list for book/article

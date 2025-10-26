<!-- Powered by BMAD™ Core -->

# Generate Research Questions

---

task:
id: generate-research-questions
name: Generate Research Questions
description: Create comprehensive research question list (20-30 questions) for deep technical topic exploration
persona_default: book-analyst
inputs: - topic - target-audience - research-depth
steps: - Understand research topic scope and depth goals - Generate foundational questions (What, Why, When, Where, Who) - Generate technical deep-dive questions (How, Architecture, Components) - Generate practical application questions (Use cases, Implementation, Best practices) - Generate advanced/edge case questions (Limitations, Scale, Advanced techniques) - Generate troubleshooting questions (Errors, Debugging, Tools) - Apply question templates (5W1H, Comparison, Implementation, Troubleshooting) - Organize questions by category (foundational, technical, practical, advanced) - Aim for 20-30 comprehensive, specific, answerable questions
output: List of 20-30 research questions ready for research-technical-topic.md task

---

## Purpose

This task generates Perplexity-style comprehensive research questions for deep technical topic exploration. Instead of manually wondering "what should I research?", you get a systematic list of 20-30 questions covering all aspects of the topic from basics to advanced techniques.

## Prerequisites

Before starting this task:

- Clear research topic identified
- Target audience skill level known (affects question depth)
- Understanding of research purpose (chapter, section, book, learning)

## Workflow Steps

### 1. Understand Research Topic

Define what you're researching:

**Ask the user:**

- What is the specific topic to research?
- What is the target audience (beginner/intermediate/advanced)?
- What is the current knowledge level about this topic?
- What is the research goal (chapter content, tutorial, reference)?
- How deep should the research go (overview vs comprehensive)?

**Document:**

- Topic scope clearly defined
- Audience skill level
- Research depth goal (overview / moderate / comprehensive)
- Time constraints (if any)

### 2. Generate Foundational Questions

Start with essential context questions:

#### What Questions (Definition & Description)

- What is [topic]?
- What problem does [topic] solve?
- What are the core components of [topic]?
- What are the key concepts in [topic]?
- What does [topic] look like in practice?

#### Why Questions (Motivation & Purpose)

- Why is [topic] important?
- Why was [topic] created?
- Why would you use [topic] instead of alternatives?
- Why do developers/engineers care about [topic]?
- Why is [topic] relevant in [year/context]?

#### When Questions (Applicability & Timing)

- When should you use [topic]?
- When should you NOT use [topic]?
- When was [topic] introduced?
- When is [topic] most beneficial?
- When do you need to consider [topic]?

#### Where Questions (Context & Architecture)

- Where does [topic] fit in the architecture?
- Where is [topic] used in production systems?
- Where are the main use cases for [topic]?
- Where does [topic] integrate with other technologies?

#### Who Questions (Users & Community)

- Who uses [topic]?
- Who created [topic]?
- Who maintains [topic]?
- Who is the target user for [topic]?

**Aim for 5-8 foundational questions**

### 3. Generate Technical Deep-Dive Questions

Explore how the technology works:

#### How Questions (Mechanics & Implementation)

- How does [topic] work internally?
- How is [topic] architected?
- How does [topic] achieve [key feature]?
- How does [topic] handle [specific scenario]?
- How is [topic] different from [alternative]?

#### Architecture Questions

- What is the internal architecture of [topic]?
- What are the key components and how do they interact?
- What design patterns does [topic] use?
- What are the data structures in [topic]?
- What is the request/processing flow in [topic]?

#### Component Questions

- What are the main modules/packages in [topic]?
- What APIs does [topic] provide?
- What configuration options exist?
- What extension points are available?
- What are the core abstractions in [topic]?

#### Performance Questions

- What are the performance characteristics of [topic]?
- How does [topic] scale?
- What are the resource requirements for [topic]?
- What are performance bottlenecks in [topic]?
- How do you optimize [topic] for performance?

#### Security Questions

- What are the security considerations for [topic]?
- How does [topic] handle authentication/authorization?
- What are common security vulnerabilities with [topic]?
- What are security best practices for [topic]?
- How do you secure [topic] in production?

**Aim for 6-10 technical questions**

### 4. Generate Practical Application Questions

Focus on real-world usage:

#### Use Case Questions

- What are real-world use cases for [topic]?
- What problems is [topic] commonly used to solve?
- What types of applications benefit from [topic]?
- What industry examples showcase [topic]?
- What successful projects use [topic]?

#### Implementation Questions

- How do you implement [topic] in [language/framework]?
- How do you get started with [topic]?
- How do you configure [topic] for [use case]?
- How do you integrate [topic] with [other technology]?
- How do you deploy [topic] to production?

#### Best Practices Questions

- What are best practices for using [topic]?
- What are anti-patterns to avoid with [topic]?
- What are code conventions for [topic]?
- What are recommended project structures?
- What are industry standards around [topic]?

#### Common Mistakes Questions

- What are common mistakes beginners make with [topic]?
- What are pitfalls to avoid?
- What are gotchas in [topic]?
- What do developers often get wrong about [topic]?
- What are misconceptions about [topic]?

#### Testing Questions

- How do you test [topic]?
- What testing strategies work for [topic]?
- What are common test scenarios?
- What tools help test [topic]?
- How do you verify [topic] works correctly?

**Aim for 6-10 practical questions**

### 5. Generate Advanced/Edge Case Questions

Explore boundaries and expertise:

#### Limitations Questions

- What are the limitations of [topic]?
- What doesn't [topic] handle well?
- What are the constraints of [topic]?
- What are known issues with [topic]?
- What trade-offs exist with [topic]?

#### Scaling Questions

- How does [topic] scale?
- What are scalability challenges with [topic]?
- How do you handle high load with [topic]?
- What are distributed system considerations?
- How do you optimize [topic] at scale?

#### Advanced Techniques Questions

- What advanced techniques exist for [topic]?
- What separates expert usage from intermediate?
- What are lesser-known features of [topic]?
- What are advanced configuration options?
- What are optimization strategies?

#### Integration Questions

- How does [topic] integrate with [ecosystem technology]?
- What tools/libraries complement [topic]?
- What are common technology stacks using [topic]?
- How does [topic] work with [database/framework/service]?
- What are integration patterns?

#### Future Questions

- What is the future of [topic]?
- What are upcoming features/changes?
- What are current trends around [topic]?
- What are the roadmap plans?
- How is [topic] evolving?

**Aim for 3-6 advanced questions**

### 6. Generate Troubleshooting Questions

Address practical problems:

#### Error Questions

- What errors commonly occur with [topic]?
- What do specific error messages mean?
- What causes [common error] in [topic]?
- What are warning signs of problems?
- What are failure modes?

#### Debugging Questions

- How do you debug [topic] issues?
- How do you diagnose [problem type] with [topic]?
- How do you troubleshoot [specific issue]?
- What logs/metrics help debug [topic]?
- What debugging tools exist for [topic]?

#### Tools Questions

- What tools help work with [topic]?
- What debugging utilities exist?
- What monitoring solutions work for [topic]?
- What profiling tools are available?
- What development tools enhance [topic] workflow?

#### Operations Questions

- What monitoring/observability for [topic]?
- How do you operate [topic] in production?
- What are maintenance requirements?
- How do you upgrade [topic]?
- What are backup/recovery strategies?

**Aim for 3-5 troubleshooting questions**

### 7. Apply Question Templates

Use these templates to generate additional questions:

#### 5W1H Template

- **What** is [topic]?
- **Why** use [topic]?
- **When** to use [topic]?
- **Where** does [topic] fit in architecture?
- **Who** uses [topic]?
- **How** does [topic] work?

#### Comparison Template

- How does [topic] compare to [alternative A]?
- How does [topic] compare to [alternative B]?
- What are pros/cons of [topic] vs [alternative]?
- When should you choose [topic] over [alternative]?
- What are the trade-offs between [topic] and [alternative]?

#### Implementation Template (Language/Framework Specific)

- How do you implement [topic] in [JavaScript]?
- How do you implement [topic] in [Python]?
- How do you implement [topic] in [Java]?
- How do you implement [topic] with [framework]?
- What libraries support [topic] in [language]?

#### Scenario Template

- How do you use [topic] for [specific use case]?
- How do you implement [feature] using [topic]?
- What's the best approach for [scenario] with [topic]?
- How do you solve [problem] using [topic]?

#### Troubleshooting Template

- What are common errors when using [topic]?
- How do you debug [specific error] in [topic]?
- What tools help troubleshoot [topic]?
- How do you fix [common problem] with [topic]?

### 8. Organize Questions

Group and sequence your questions:

**Create categories:**

```markdown
## Foundational Questions (5-8 questions)

[Definition, motivation, context, applicability questions]

## Technical Deep-Dive Questions (6-10 questions)

[Architecture, components, performance, security questions]

## Practical Application Questions (6-10 questions)

[Use cases, implementation, best practices, testing questions]

## Advanced Topics Questions (3-6 questions)

[Limitations, scaling, advanced techniques, integration questions]

## Troubleshooting Questions (3-5 questions)

[Errors, debugging, tools, operations questions]
```

**Sequence within categories:**

- Basic to advanced
- General to specific
- Common to edge cases

**Remove duplicates:**

- Check for similar questions
- Consolidate overlapping questions
- Ensure each question adds unique value

**Aim for 20-30 total questions**

### 9. Refine Questions

Make questions specific and answerable:

**Bad question (too vague):**

- "How does React work?"

**Good question (specific):**

- "How does React's virtual DOM reconciliation algorithm work?"

**Bad question (too broad):**

- "What are best practices?"

**Good question (specific):**

- "What are best practices for managing state in React applications?"

**Refinement checklist for each question:**

- [ ] Is it specific enough to research?
- [ ] Is it answerable (not purely opinion)?
- [ ] Is it relevant to the topic?
- [ ] Is it at appropriate depth for audience?
- [ ] Does it add unique value (not duplicate)?

### 10. Present Research Questions

Output final list:

**Format:**

```markdown
# Research Questions: [Topic]

**Research Goal**: [Chapter/Section/Book/etc.]
**Target Audience**: [Beginner/Intermediate/Advanced]
**Research Depth**: [Overview/Moderate/Comprehensive]

## Foundational Questions (7 questions)

1. What is [topic] and how does it work?
2. Why was [topic] created and what problems does it solve?
3. When should you use [topic] vs alternatives?
   [...continue...]

## Technical Deep-Dive Questions (8 questions)

1. How is [topic] architected internally?
2. What are the key components and how do they interact?
   [...continue...]

## Practical Application Questions (9 questions)

1. What are real-world use cases for [topic]?
2. How do you implement [topic] in [language/framework]?
   [...continue...]

## Advanced Topics Questions (4 questions)

1. What are the limitations and trade-offs of [topic]?
2. How does [topic] scale in production environments?
   [...continue...]

## Troubleshooting Questions (4 questions)

1. What are common errors when working with [topic]?
2. How do you debug [topic] issues?
   [...continue...]

---

**Total Questions**: 32
**Next Step**: Use research-technical-topic.md to answer these questions
```

**Save to:**

- User-specified location or `docs/research/[topic]-questions.md`

## Success Criteria

A successful research question list has:

- [ ] 20-30 comprehensive questions
- [ ] Questions organized by category (foundational, technical, practical, advanced, troubleshooting)
- [ ] All major aspects of topic covered
- [ ] Questions are specific and answerable
- [ ] Questions appropriate for target audience
- [ ] No significant duplicates
- [ ] Progression from basic to advanced
- [ ] Mix of "what/why/how/when" questions
- [ ] Practical and theoretical balance
- [ ] Ready to use with research-technical-topic.md task

## Common Pitfalls to Avoid

- **Too few questions**: Missing important aspects
- **Too many questions**: Overwhelming, redundant
- **Too vague**: "How does it work?" vs "How does [specific component] work?"
- **Too broad**: "Best practices?" vs "Best practices for [specific use case]?"
- **Only surface-level**: Need deep-dive questions too
- **Only advanced**: Need foundational questions
- **Unanswerable**: Opinion-based or too speculative
- **No organization**: Random list is hard to work with
- **Duplicates**: Same question asked multiple ways
- **Off-topic**: Questions not relevant to research goal

## Example: Research Questions for JWT Authentication

**Topic**: JWT Authentication in Node.js
**Target Audience**: Intermediate developers
**Research Goal**: Chapter content for technical book
**Depth**: Comprehensive

### Foundational Questions (7)

1. What is JWT (JSON Web Token) and how does it differ from session-based authentication?
2. Why use JWT for authentication instead of traditional session cookies?
3. When should you use JWT vs session-based authentication?
4. What are the three components of a JWT (header, payload, signature)?
5. Where are JWTs commonly used in modern web applications?
6. Who created JWT and what standards define it (RFC 7519)?
7. What problems does JWT solve in distributed/microservices architectures?

### Technical Deep-Dive Questions (9)

1. How does JWT signing and verification work cryptographically?
2. What signing algorithms are available (HS256, RS256, etc.) and when to use each?
3. How does the JWT signature prevent tampering?
4. What are standard JWT claims (iss, sub, aud, exp, iat) and their purposes?
5. How do you encode and decode JWTs in Node.js?
6. What libraries are most commonly used for JWT in Node.js?
7. How does token expiration work and how is it verified?
8. What is the structure of a JWT token (base64url encoding)?
9. How do refresh tokens work in JWT-based systems?

### Practical Application Questions (10)

1. How do you implement JWT authentication in an Express.js application?
2. What is the recommended way to store JWTs on the client (localStorage vs cookies)?
3. How do you create a JWT authentication middleware in Express?
4. What are best practices for JWT secret key management?
5. How do you implement protected API routes using JWT?
6. How do you handle token refresh logic in a Node.js backend?
7. What are common mistakes developers make when implementing JWT auth?
8. How do you test JWT authentication endpoints?
9. What HTTP headers should be used for transmitting JWTs?
10. How do you implement role-based access control (RBAC) with JWTs?

### Advanced Topics Questions (5)

1. What are the security vulnerabilities of JWT and how to mitigate them?
2. How do you implement JWT token revocation/blacklisting?
3. What are the performance implications of JWT vs session tokens at scale?
4. How do you handle JWT authentication in microservices architectures?
5. What are the trade-offs between short-lived tokens + refresh vs long-lived tokens?

### Troubleshooting Questions (4)

1. What are common JWT verification errors and their causes?
2. How do you debug "invalid signature" errors in JWT?
3. What tools exist for inspecting and debugging JWTs (jwt.io, etc.)?
4. How do you handle expired token scenarios gracefully in the UI?

**Total: 35 questions**

## Next Steps

After generating research questions:

1. Review questions with technical expert or co-author
2. Prioritize questions (critical vs nice-to-know)
3. Use research-technical-topic.md to systematically answer questions
4. Document sources and findings
5. Synthesize research into content outline

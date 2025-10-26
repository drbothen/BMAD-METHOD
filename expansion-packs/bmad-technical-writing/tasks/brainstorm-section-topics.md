<!-- Powered by BMAD™ Core -->

# Brainstorm Section Topics

---

task:
  id: brainstorm-section-topics
  name: Brainstorm Section Topics
  description: Break chapter into 8-12 manageable sections (2-5 pages each)
  persona_default: tutorial-architect
  inputs:
    - chapter-topic
    - learning-objectives
    - target-length
  steps:
    - Analyze chapter scope and learning objectives
    - Calculate target sections needed (chapter length ÷ section length)
    - Break down learning objectives into section-sized pieces
    - Identify natural content breakpoints
    - Apply section generation patterns (concept, tutorial, problem, comparison)
    - Generate 8-12 section topic ideas
    - Validate coverage and flow
    - Prioritize and sequence sections
  output: List of 8-12 section topics ready for section planning

---

## Purpose

This task helps you break a chapter into manageable, focused sections. Good section planning makes both writing and reading easier by creating clear knowledge chunks with logical progression.

## Prerequisites

Before starting this task:

- Chapter topic identified
- Chapter learning objectives defined (typically 3-5 objectives)
- Target chapter length known (15-25 pages typical)
- Understanding of target audience skill level

## Workflow Steps

### 1. Analyze Chapter Scope

Understand what you're working with:

**Review chapter information:**
- Chapter topic and title
- Learning objectives (what readers will accomplish)
- Target length (typical technical book chapter: 15-25 pages)
- Prerequisites (what readers already know)
- Position in book (early, middle, late)

**Identify chapter structure:**
- Introduction needs (hook, overview, prerequisites)
- Main content areas
- Exercises/practice needed
- Summary/conclusion

**Note constraints:**
- Page limit
- Code example count
- Diagram/screenshot needs
- Complexity level

### 2. Calculate Sections Needed

Determine how many sections to create:

**Typical section length:** 2-5 pages each

**Calculate target count:**
- 15-page chapter → 3-8 sections (average 4-5)
- 20-page chapter → 4-10 sections (average 6-8)
- 25-page chapter → 5-12 sections (average 8-10)

**Consider:**
- Shorter sections (2-3 pages): Focused, bite-sized, easier to write
- Longer sections (4-5 pages): Deeper coverage, fewer transitions
- Mix of lengths: Varies pacing, matches content naturally

**Account for fixed sections:**
- Introduction: ~1-2 pages
- Summary: ~1 page
- Remaining pages for content sections

### 3. Break Down Learning Objectives

Map objectives to sections:

**For each learning objective:**
- Can this be taught in one section? Or needs multiple?
- What's the teaching sequence (prerequisite order)?
- What examples demonstrate this objective?

**Example:**

**Chapter**: "JWT Authentication in Node.js"

**Learning Objectives:**
1. Understand JWT structure and security model
2. Implement JWT authentication middleware
3. Handle token refresh and expiration
4. Secure endpoints with role-based access control

**Mapped to sections:**
- LO 1 → Section 1 (Understanding JWTs), Section 2 (Security considerations)
- LO 2 → Section 3 (Creating auth middleware), Section 4 (Integration tutorial)
- LO 3 → Section 5 (Token expiration handling), Section 6 (Refresh token flow)
- LO 4 → Section 7 (RBAC implementation)
- Plus: Section 8 (Testing and troubleshooting)

### 4. Identify Natural Breakpoints

Find logical places to divide content:

**Concept boundaries:**
- Where topics naturally separate
- Transition between related ideas
- Shift from theory to practice

**Practical applications:**
- Each major hands-on tutorial is a section
- Code walkthroughs grouped by feature
- Implementation stages

**Code example groupings:**
- Related code files taught together
- Progressive iterations (v1, v2, v3)
- Before/after refactorings

**Tutorial stages:**
- Setup and prerequisites
- Basic implementation
- Adding features
- Optimization and polish

**Skill milestones:**
- Checkpoints where readers gain new capability
- "After this section, you can..."
- Natural stopping points

### 5. Apply Section Generation Patterns

Use these patterns to generate section ideas:

#### Concept-Driven Pattern

Focus on explaining ideas:

**Pattern:** "Understanding X", "How Y Works", "Z Fundamentals"

**Examples:**
- "Understanding JWT Structure and Claims"
- "How Token Signing and Verification Work"
- "Security Fundamentals for Token-Based Auth"

**Use when:** Teaching theory, background, or foundational concepts

#### Tutorial-Driven Pattern

Focus on building something:

**Pattern:** "Building X", "Implementing Y", "Creating Z"

**Examples:**
- "Building Your First JWT Authentication Endpoint"
- "Implementing Token Refresh Logic"
- "Creating a Protected API Route"

**Use when:** Hands-on practice, step-by-step implementation

#### Problem-Driven Pattern

Focus on solving challenges:

**Pattern:** "Solving X", "Debugging Y", "Optimizing Z", "Handling W"

**Examples:**
- "Handling Token Expiration Gracefully"
- "Debugging Authentication Failures"
- "Solving Token Storage Security Issues"

**Use when:** Addressing common pain points, troubleshooting

#### Comparison-Driven Pattern

Focus on evaluating options:

**Pattern:** "X vs Y", "Choosing Between Options", "Evaluating Trade-offs"

**Examples:**
- "JWT vs Session-Based Authentication"
- "Choosing Token Storage: LocalStorage vs Cookies"
- "Comparing Signing Algorithms: HS256 vs RS256"

**Use when:** Multiple approaches exist, decision frameworks needed

#### Integration-Driven Pattern

Focus on combining technologies:

**Pattern:** "Integrating X with Y", "Connecting Z", "Combining W"

**Examples:**
- "Integrating JWT with Express Middleware"
- "Connecting Frontend and Backend Auth"
- "Combining JWT with OAuth 2.0"

**Use when:** Multiple systems interact, ecosystem topics

### 6. Generate 8-12 Section Ideas

Create your section list:

**For each section, document:**

```markdown
**Section N**: [Descriptive title]
**Focus**: [Main point or learning outcome]
**Content**: [What will be covered]
**Type**: [Concept / Tutorial / Problem / Comparison / Integration]
**Estimated Length**: [2-5 pages]
**Code Examples**: [List any code files]
```

**Example:**

```markdown
**Section 3**: Implementing JWT Authentication Middleware
**Focus**: Create reusable Express middleware for token verification
**Content**: Design middleware function, verify tokens, handle errors, attach user to request
**Type**: Tutorial
**Estimated Length**: 4 pages
**Code Examples**: auth-middleware.js, error-handler.js
```

**Typical Chapter Structure:**

**Introduction Section (1-2 pages):**
- Hook and motivation
- Chapter overview
- Prerequisites check

**Foundational Sections (2-3 sections, 6-9 pages total):**
- Core concepts explained
- Background and theory
- Why this approach matters

**Implementation Sections (3-5 sections, 9-15 pages total):**
- Step-by-step tutorials
- Code walkthroughs
- Hands-on practice

**Advanced/Edge Case Sections (1-2 sections, 3-6 pages total):**
- Optimization techniques
- Error handling
- Security considerations
- Production concerns

**Practice Section (1 section, 2-3 pages):**
- Exercises
- Challenges
- Self-assessment

**Summary Section (1 page):**
- Key takeaways
- Skills checklist
- Next steps

### 7. Validate Section Plan

Check your section list:

**Coverage:**
- [ ] All learning objectives addressed
- [ ] No major gaps in content
- [ ] Appropriate depth for audience
- [ ] Examples for each concept

**Flow:**
- [ ] Logical progression (simple → complex)
- [ ] Prerequisites taught before usage
- [ ] Clear transitions possible between sections
- [ ] Natural reading experience

**Balance:**
- [ ] Mix of theory and practice
- [ ] Not too many concept-only sections
- [ ] Enough hands-on tutorials
- [ ] Appropriate difficulty curve

**Scope:**
- [ ] Sections fit within page estimates
- [ ] Total adds up to target chapter length
- [ ] No single section too large (>6 pages)
- [ ] No section too small (<2 pages unless intro/summary)

**Feasibility:**
- [ ] Code examples are realistic to create
- [ ] Time to write is reasonable
- [ ] Testing is manageable
- [ ] Diagram needs are clear

### 8. Prioritize Sections

Classify each section:

**Critical Sections (Must-Have):**
- Essential for learning objectives
- Cannot skip without knowledge gaps
- Core to chapter purpose

**Valuable Sections (Should-Have):**
- Enhance understanding significantly
- Best practices and patterns
- Common use cases

**Optional Sections (Nice-to-Have):**
- Advanced techniques
- Edge cases
- Bonus content
- Can be cut if space-limited

**Identify sections that could:**
- Be combined (if too granular)
- Be split (if too complex)
- Be expanded to full chapter (if rich enough)
- Be moved to appendix (if too specialized)

### 9. Sequence Sections

Determine final order:

**Scaffolding principles:**
- Teach simple before complex
- Prerequisites before dependents
- Theory before practice (but not too much theory upfront)
- General before specific
- Common before edge cases

**Flow considerations:**
- Vary pacing (concept → tutorial → concept → tutorial)
- Build momentum (quick wins early)
- Natural breaks (sections are stopping points)
- Motivation maintenance (why this matters)

**Example sequence:**

1. Introduction (motivation, overview)
2. Foundational concept (necessary theory)
3. First tutorial (hands-on win)
4. Supporting concept (more theory)
5. Second tutorial (building on first)
6. Advanced technique (stretch goal)
7. Troubleshooting (practical help)
8. Exercises (practice)
9. Summary (recap, next steps)

### 10. Document Section Plan

Create final output:

**Format:**

```markdown
# Section Plan: [Chapter Title]

## Chapter Info
- **Learning Objectives**: [List 3-5 objectives]
- **Target Length**: [15-25 pages]
- **Sections**: [8-12 sections]

## Section Breakdown

### Section 1: [Title] (Introduction, 2 pages)
- **Type**: Introduction
- **Focus**: [What this section accomplishes]
- **Content**: [Topics covered]
- **Code Examples**: [None for intro]

### Section 2: [Title] (Concept, 3 pages)
- **Type**: Concept
- **Focus**: [Learning outcome]
- **Content**: [Topics covered]
- **Code Examples**: [If any]

[... continue for all 8-12 sections ...]

## Total Estimation
- **Total Sections**: 10
- **Estimated Pages**: 22
- **Code Files**: 8
- **Diagrams**: 4
```

**Save to:**
- User-specified location or `docs/planning/[chapter-name]-sections.md`

## Success Criteria

A successful section plan has:

- [ ] 8-12 distinct section topics
- [ ] Each section 2-5 pages estimated
- [ ] All chapter learning objectives covered
- [ ] Clear focus for each section
- [ ] Logical progression (scaffolding)
- [ ] Mix of concepts and tutorials
- [ ] Realistic page estimates (total matches target)
- [ ] Natural breakpoints and transitions
- [ ] Code examples identified
- [ ] Prioritization clear (critical/valuable/optional)

## Common Pitfalls to Avoid

- **Too many sections**: Fragmented reading experience
- **Too few sections**: Overwhelming chunks of content
- **Unclear focus**: Sections try to cover too much
- **Poor progression**: Jumping between difficulty levels
- **All theory or all practice**: Need balance
- **No transitions**: Sections feel disconnected
- **Unrealistic length**: Section estimates don't match reality
- **Missing exercises**: No practice opportunities
- **Ignoring audience**: Difficulty not matched to skill level

## Example: Section Plan for JWT Chapter

**Chapter**: "JWT Authentication in Node.js"
**Target Length**: 20 pages
**Learning Objectives**: Understand JWT, implement auth middleware, handle refresh, secure with RBAC

**Section Breakdown (10 sections):**

1. **Introduction to JWT Authentication** (2 pages)
   - Type: Introduction
   - Why JWT over sessions, chapter roadmap

2. **Understanding JWT Structure and Claims** (3 pages)
   - Type: Concept
   - Header, payload, signature; standard claims

3. **Building Your First JWT Endpoint** (4 pages)
   - Type: Tutorial
   - Login endpoint, token generation, response

4. **Implementing Auth Middleware** (3 pages)
   - Type: Tutorial
   - Verify tokens, attach user, error handling

5. **Securing API Routes** (2 pages)
   - Type: Tutorial
   - Apply middleware, protect endpoints

6. **Handling Token Expiration and Refresh** (3 pages)
   - Type: Tutorial + Problem
   - Refresh token flow, graceful expiration

7. **Role-Based Access Control** (2 pages)
   - Type: Tutorial
   - Add roles to tokens, permission middleware

8. **Security Best Practices** (2 pages)
   - Type: Concept
   - HTTPS, secret management, token storage

9. **Testing and Troubleshooting** (2 pages)
   - Type: Problem
   - Unit tests, common errors, debugging

10. **Summary and Exercises** (2 pages)
    - Type: Practice + Summary
    - Skills checklist, challenge problems

**Total: 25 pages across 10 sections**

## Next Steps

After completing section brainstorming:

1. Review with technical expert or co-author
2. Validate against chapter learning objectives
3. Use sections to create detailed section outlines
4. Begin researching or writing individual sections
5. Create code examples for tutorial sections

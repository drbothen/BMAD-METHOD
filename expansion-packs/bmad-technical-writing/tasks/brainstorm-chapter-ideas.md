<!-- Powered by BMAD™ Core -->

# Brainstorm Chapter Topic Ideas

---

task:
  id: brainstorm-chapter-ideas
  name: Brainstorm Chapter Topic Ideas
  description: Generate comprehensive list of 15-25 potential chapter topics from book concept
  persona_default: instructional-designer
  inputs:
    - book-concept
    - target-audience
    - book-goals
  steps:
    - Analyze book concept, audience, and scope
    - Identify essential topics (must-have for this book)
    - Review similar/competing books for coverage gaps
    - Apply brainstorming techniques (mind mapping, SCAMPER, 5W1H)
    - Generate 15-25 chapter topic ideas with rationale
    - Organize by learning progression and priority
    - Tag difficulty level and estimated length
    - Identify gaps and opportunities
    - Present ideas grouped by category (Essential/Valuable/Optional)
  output: List of 15-25 chapter ideas ready for book outline design

---

## Purpose

This task helps you move from "I want to write a book about X" to a comprehensive list of potential chapters. By applying systematic brainstorming techniques, you'll generate more diverse, creative chapter ideas than manual ideation alone.

## Prerequisites

Before starting this task:

- Clear book concept or topic
- Target audience identified (skill level, background)
- General sense of book goals (what readers will accomplish)
- Understanding of book scope (approximate length, depth)

## Workflow Steps

### 1. Analyze Book Concept

Understand the foundation:

**Ask the user:**
- What is the book topic and core technology/framework?
- Who is the target audience (beginner/intermediate/advanced)?
- What will readers accomplish after reading this book?
- What is the estimated book length (pages or chapters)?
- What makes this book different from existing books?
- What publisher or format are you targeting?

**Document:**
- Book title or working title
- Target reader persona
- Book scope and constraints
- Success criteria for readers

### 2. Review Similar Books

Research competitive landscape:

**Identify 3-5 competing or similar books:**
- What topics do they cover?
- What topics do they miss?
- What's their approach (tutorial, reference, conceptual)?
- What page count and chapter count?

**Find opportunities:**
- Underserved topics in the space
- Better approaches to common topics
- New technologies or practices not yet covered
- Different audience segment (beginners vs experts)

### 3. Identify Core Topics

Determine essential content:

**Must-have topics** (essential for this book):
- What topics are absolutely required?
- What would make the book incomplete without them?
- What are foundational concepts?

**Foundation topics** (prerequisites):
- What background knowledge is needed?
- Should prerequisites be covered in the book?
- What can be assumed vs. taught?

**Advanced topics** (stretch goals):
- What advanced techniques separate experts from intermediates?
- What cutting-edge topics could be included?
- What bonus/optional chapters make sense?

**Topic dependencies:**
- What must be taught before other topics?
- What natural progression exists?
- Are there independent topics (can be read in any order)?

### 4. Apply Brainstorming Techniques

Generate diverse ideas using multiple approaches:

#### Mind Mapping Technique

Start with your core topic in the center, branch out:

**Example for "React Web Development":**
```
React Development
├── Fundamentals (Components, Props, State, Hooks)
├── Routing (React Router, Navigation, Protected Routes)
├── State Management (Context, Redux, Zustand)
├── Data Fetching (REST APIs, GraphQL, React Query)
├── Forms (Validation, File Uploads, Complex Forms)
├── Authentication (JWT, OAuth, Session Management)
├── Testing (Jest, React Testing Library, E2E)
├── Performance (Lazy Loading, Memoization, Code Splitting)
└── Deployment (Build Process, CI/CD, Hosting)
```

For each branch, ask: "What specific chapters could cover this?"

#### SCAMPER Technique

Apply each SCAMPER prompt to generate creative variations:

- **Substitute**: "What if we replaced X with Y approach?"
- **Combine**: "What if we combined X and Y in one chapter?"
- **Adapt**: "How can X be adapted for Y use case?"
- **Modify**: "How can we modify the standard X tutorial?"
- **Put to other uses**: "What other uses exist for X?"
- **Eliminate**: "What if we removed X complexity?"
- **Reverse**: "What if we approached X from the opposite angle?"

#### 5W1H Technique

Generate questions for each prompt:

- **Who**: "Who uses this technology?" → Chapter on enterprise vs startup usage
- **What**: "What are common mistakes?" → Chapter on anti-patterns and debugging
- **When**: "When should you use X vs Y?" → Chapter on decision frameworks
- **Where**: "Where does this fit in architecture?" → Chapter on integration patterns
- **Why**: "Why is this important?" → Chapter on motivation and real-world impact
- **How**: "How do you implement X?" → Tutorial chapter

#### Comparison & Contrast

Explore alternatives and trade-offs:

- "X vs Y: Choosing the Right Approach"
- "Comparing Implementation Patterns"
- "Migration from X to Y"
- "Evaluating Trade-offs in Z"

### 5. Use Ideation Prompts

Ask yourself these questions to generate specific ideas:

**Learning Path Prompts:**
- "What does the reader need to know to accomplish [book goal]?"
- "What's the logical progression from beginner to proficient?"
- "What milestones mark progress toward mastery?"

**Problem-Solving Prompts:**
- "What mistakes do beginners make with [technology]?"
- "What pain points does [technology] solve?"
- "What troubleshooting skills are essential?"
- "What errors and edge cases need coverage?"

**Practical Application Prompts:**
- "What real-world projects demonstrate [concepts]?"
- "What build tutorials would teach [skills]?"
- "What production concerns need addressing?"
- "What deployment scenarios are common?"

**Advanced Technique Prompts:**
- "What advanced techniques separate experts from intermediates?"
- "What performance optimization strategies exist?"
- "What security considerations are critical?"
- "What scalability patterns matter?"

**Ecosystem Prompts:**
- "What tools and libraries complement [technology]?"
- "What integrations are commonly needed?"
- "What testing strategies apply?"
- "What monitoring and debugging approaches work?"

### 6. Generate 15-25 Chapter Ideas

Create your brainstormed list:

**For each chapter idea, document:**

```markdown
**Chapter Idea**: [Descriptive title]
**Description**: [1-2 sentence overview]
**Rationale**: [Why include this? What problem does it solve?]
**Estimated Length**: [15-25 pages typical]
**Difficulty Level**: [Beginner / Intermediate / Advanced]
**Priority**: [Essential / Valuable / Optional]
**Dependencies**: [What chapters must come before this?]
```

**Example:**

```markdown
**Chapter Idea**: Building a Custom React Hook Library
**Description**: Design and implement reusable custom hooks for common patterns like data fetching, form handling, and authentication.
**Rationale**: Custom hooks are key to code reuse in React, but few books teach systematic hook design. This fills a gap.
**Estimated Length**: 20 pages
**Difficulty Level**: Intermediate
**Priority**: Valuable
**Dependencies**: Hooks fundamentals chapter
```

**Aim for diversity:**
- Mix of foundational and advanced topics
- Balance theory and hands-on tutorials
- Variety of chapter types (concept, tutorial, reference, troubleshooting)
- Different learning styles (visual, code-heavy, conceptual)

### 7. Organize and Prioritize

Group and sequence your ideas:

**Category 1: Essential Chapters**
- Topics required for book completeness
- Foundational concepts
- Core learning objectives

**Category 2: Valuable Chapters**
- Topics that enhance the book significantly
- Common use cases
- Best practices and patterns

**Category 3: Optional Chapters**
- Nice-to-have topics
- Advanced or specialized content
- Bonus material

**Sequence by learning progression:**
- Which topics are prerequisites for others?
- What's the natural teaching order?
- Where are the major skill milestones?

**Identify gaps:**
- Are there topic areas missing?
- Is coverage balanced across difficulty levels?
- Are there too many or too few chapters?
- What topics could be combined or split?

### 8. Review and Refine

Present ideas to the user:

**Present organized list:**
```markdown
## Essential Chapters (Must-Have)
1. [Chapter idea with description]
2. [Chapter idea with description]
...

## Valuable Chapters (Strongly Recommended)
1. [Chapter idea with description]
...

## Optional Chapters (Nice-to-Have)
1. [Chapter idea with description]
...
```

**Ask for feedback:**
- Which ideas resonate most?
- Are there topics to add or remove?
- Does the mix feel right for the target audience?
- Is anything missing from the competitive landscape?

**Iterate:**
- Add new ideas based on feedback
- Merge similar topics
- Remove low-priority items if scope is too large
- Adjust difficulty levels

### 9. Document Final List

Create final brainstormed chapter list:

**Output format:**
- List of 15-25 chapter ideas
- Organized by priority (Essential/Valuable/Optional)
- Each with description, rationale, difficulty, dependencies
- Ready for use in design-book-outline.md task

**Save to:**
- `docs/brainstorming/chapter-ideas.md` (or user-specified location)

## Success Criteria

A successful brainstorming session produces:

- [ ] 15-25 distinct chapter topic ideas
- [ ] Each idea has clear description and rationale
- [ ] Mix of foundational, intermediate, and advanced topics
- [ ] Variety of chapter types (tutorials, concepts, reference)
- [ ] Ideas organized by priority (Essential/Valuable/Optional)
- [ ] Difficulty levels and dependencies noted
- [ ] Coverage gaps identified
- [ ] Comparison with competing books done
- [ ] User feedback incorporated

## Common Pitfalls to Avoid

- **Not enough ideas**: Don't stop at obvious topics; push for creative angles
- **Too similar**: Ensure diversity in approach and difficulty
- **No rationale**: Every idea needs "why include this?"
- **Ignoring audience**: Keep target readers in mind
- **No prioritization**: Not all ideas are equal
- **Missing gaps**: Research what existing books don't cover
- **Too narrow**: Think beyond the obvious tutorials
- **No dependencies**: Consider what must be taught first

## Example: Brainstormed Chapter Ideas

**Book Concept**: "Full Stack TypeScript: Building Production Web Applications"
**Audience**: Intermediate developers with JavaScript experience
**Goal**: Build and deploy production-ready TypeScript applications

**Essential Chapters (10):**

1. **TypeScript Fundamentals for JavaScript Developers**
   - Rationale: Readers need solid foundation before advanced topics
   - Difficulty: Beginner-Intermediate
   - Length: 20 pages

2. **Building Type-Safe APIs with Express and TypeScript**
   - Rationale: Backend is critical for full-stack development
   - Difficulty: Intermediate
   - Length: 25 pages

3. **React with TypeScript: Components and Hooks**
   - Rationale: Frontend framework with type safety
   - Difficulty: Intermediate
   - Length: 22 pages

[...7 more essential chapters...]

**Valuable Chapters (8):**

1. **Advanced TypeScript: Generics and Utility Types**
   - Rationale: Differentiates intermediate from advanced developers
   - Difficulty: Advanced
   - Length: 18 pages

[...7 more valuable chapters...]

**Optional Chapters (4):**

1. **Migrating Legacy JavaScript to TypeScript**
   - Rationale: Practical for readers with existing codebases
   - Difficulty: Intermediate
   - Length: 15 pages

[...3 more optional chapters...]

## Next Steps

After completing chapter idea brainstorming:

1. Review list with technical experts or beta readers
2. Narrow to target chapter count (typically 12-20)
3. Use ideas with design-book-outline.md task
4. Create detailed chapter outlines for selected chapters
5. Begin content research for specific topics

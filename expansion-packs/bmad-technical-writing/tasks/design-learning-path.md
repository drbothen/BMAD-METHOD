<!-- Powered by BMAD™ Core -->

# Design Learning Path

---

task:
id: design-learning-path
name: Design Learning Path
description: Map prerequisite dependencies and design skill progression for optimal learning flow
persona_default: learning-path-designer
inputs:

- book-outline
- chapter-topics
- target-audience
  steps:
- Review book outline and chapter topics
- Identify foundational vs. advanced topics
- Map prerequisite dependencies between chapters
- Design skill scaffolding (simple → complex progression)
- Validate no knowledge gaps in progression
- Assess reader readiness at each chapter
- Identify optional vs. required chapters
- Create dependency diagram
- Verify alignment with learning objectives
- Document learning path in book outline
- Run execute-checklist.md with learning-objectives-checklist.md
- Run execute-checklist.md with prerequisite-clarity-checklist.md
  output: docs/learning-path/{{book-name}}-learning-path.md

---

## Purpose

This task guides you through designing a coherent learning progression that scaffolds reader knowledge from foundational concepts to advanced topics. A well-designed learning path ensures readers can successfully navigate the book without encountering unexplained prerequisites or knowledge gaps.

## Prerequisites

Before starting this task:

- Completed book outline with chapter topics
- Clear understanding of target audience skill level
- Access to learning-frameworks.md knowledge base
- Learning objectives defined for each chapter

## Workflow Steps

### 1. Review Book Outline and Chapter Topics

Analyze your book structure:

- List all chapters and their main topics
- Identify the core concepts in each chapter
- Note any technical skills required
- Review the chapter ordering

**Output:** Complete inventory of topics and skills covered

### 2. Identify Foundational vs. Advanced Topics

Categorize content by complexity:

- **Foundational topics**: Required basic knowledge (e.g., "What is an API?")
- **Intermediate topics**: Build on foundations (e.g., "RESTful API design")
- **Advanced topics**: Complex applications (e.g., "API rate limiting strategies")

**Example Categorization:**

```
Foundational:
- Chapter 1: Introduction to Web Development
- Chapter 2: HTML/CSS Basics
- Chapter 3: JavaScript Fundamentals

Intermediate:
- Chapter 4: DOM Manipulation
- Chapter 5: Async Programming
- Chapter 6: HTTP and APIs

Advanced:
- Chapter 7: State Management
- Chapter 8: Performance Optimization
- Chapter 9: Production Deployment
```

### 3. Map Prerequisite Dependencies

Create dependency mapping:

- Which chapters must be read before others?
- What external knowledge is assumed?
- Are there alternative learning paths?
- Can any chapters be read independently?

**Dependency Notation:**

- **Hard prerequisite**: Chapter 5 REQUIRES Chapter 3
- **Soft prerequisite**: Chapter 7 RECOMMENDS Chapter 4 (helpful but not essential)
- **No prerequisite**: Chapter can be read standalone

**Example Dependency Map:**

```
Chapter 1 → Chapter 2 (hard prerequisite)
Chapter 2 → Chapter 3 (hard prerequisite)
Chapter 3 → Chapter 4, Chapter 5 (hard prerequisite)
Chapter 4 → Chapter 7 (soft prerequisite)
Chapter 5 → Chapter 6 (hard prerequisite)
Chapter 6 → Chapter 8 (soft prerequisite)
```

### 4. Design Skill Scaffolding

Plan progression from simple to complex:

- Start with concrete, tangible concepts
- Build abstractions incrementally
- Introduce one new concept at a time
- Reinforce previous concepts in new contexts
- Increase cognitive load gradually

**Scaffolding Principles:**

- **Concrete before abstract**: Show examples before theory
- **Simple before complex**: One variable at a time
- **Familiar before unfamiliar**: Build on known concepts
- **Guided before independent**: Provide support initially

**Example Skill Progression:**

```
1. Use existing API (concrete, simple)
2. Understand API request/response (concrete, intermediate)
3. Design API endpoint (abstract, intermediate)
4. Implement full API (abstract, complex)
5. Optimize API architecture (abstract, advanced)
```

### 5. Validate No Knowledge Gaps

Check for missing prerequisites:

- Review each chapter's required knowledge
- Verify all prerequisites are taught earlier
- Identify any assumed knowledge not covered
- Check for circular dependencies
- Look for sudden difficulty jumps

**Gap Detection Questions:**

- Does the reader have the knowledge needed for this chapter?
- Was this concept explained in a previous chapter?
- Are we assuming prior knowledge that wasn't taught?
- Is there too large a jump from the previous chapter?

**Common Gaps:**

- Technical jargon used without definition
- Tools/frameworks used without introduction
- Concepts referenced but never explained
- Skipped intermediate steps

### 6. Assess Reader Readiness

Evaluate readiness at key transition points:

- Can readers handle the next chapter after completing this one?
- What skills should readers have at this point?
- How can readers self-assess their readiness?
- Should there be a checkpoint exercise?

**Readiness Assessment Template:**

```
After Chapter 3, readers should be able to:
✓ Write basic JavaScript functions
✓ Understand variables, loops, and conditionals
✓ Debug simple syntax errors
✓ Read and understand code examples

Before Chapter 4, readers should verify:
□ Can I write a function that takes parameters?
□ Do I understand how arrays work?
□ Can I follow code examples without confusion?
```

### 7. Identify Optional vs. Required Chapters

Mark chapter importance:

- **Required (Core)**: Essential for understanding later material
- **Recommended**: Enhances understanding but not essential
- **Optional**: Bonus content, alternative approaches, deep dives

**Labeling Example:**

```
✓ Chapter 1: Introduction (REQUIRED)
✓ Chapter 2: Setup (REQUIRED)
✓ Chapter 3: Basics (REQUIRED)
○ Chapter 4: Advanced Techniques (RECOMMENDED)
○ Chapter 5: Alternative Approaches (OPTIONAL)
✓ Chapter 6: Integration (REQUIRED)
```

### 8. Create Dependency Diagram

Visualize the learning path:

- Use flowchart or dependency graph
- Show prerequisite relationships
- Mark required vs. optional chapters
- Indicate alternative paths if applicable

**Simple Text Diagram:**

```
[Chapter 1] ──→ [Chapter 2] ──→ [Chapter 3] ──┬──→ [Chapter 4] ──→ [Chapter 7]
                                                │
                                                └──→ [Chapter 5] ──→ [Chapter 6] ──→ [Chapter 8]

Legend:
──→ Hard prerequisite
··→ Soft prerequisite (recommended)
[ ] Required chapter
( ) Optional chapter
```

### 9. Verify Alignment with Learning Objectives

Cross-check with stated objectives:

- Do chapter sequences support stated learning goals?
- Are learning objectives achievable with this progression?
- Does the path build the skills promised in the book description?
- Are there any objectives not covered by the learning path?

**Alignment Check:**

- Book objective: "Master API development"
- Learning path includes: API basics → design → implementation → optimization ✓
- Progression supports objective ✓

### 10. Document Learning Path

Create comprehensive learning path documentation:

**Include:**

- Visual dependency diagram
- Chapter-by-chapter prerequisite list
- Skill progression chart
- Reader readiness checkpoints
- Alternative reading paths (if applicable)
- Estimated difficulty curve
- Recommended pace (time per chapter)

**Example Documentation:**

```markdown
# Learning Path: Mastering Web APIs

## Reading Order

### Linear Path (Recommended for Beginners)

Chapters 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

### Fast Track (For Experienced Developers)

Chapters 1 → 3 → 5 → 6 → 8
(Skip chapters 2, 4, 7 if familiar with basics)

## Prerequisite Map

- Chapter 1: No prerequisites (start here)
- Chapter 2: Requires Chapter 1
- Chapter 3: Requires Chapter 2
- Chapter 4: Requires Chapter 3 (optional enhancement)
- Chapter 5: Requires Chapter 3
- Chapter 6: Requires Chapter 5
- Chapter 7: Requires Chapter 4 and 6
- Chapter 8: Requires Chapter 6

## Skill Progression

Chapters 1-3: Foundational (Beginner)
Chapters 4-6: Intermediate
Chapters 7-8: Advanced

## Reader Readiness Checkpoints

After Chapter 3: Can you create a basic API endpoint?
After Chapter 6: Can you handle authentication and errors?
After Chapter 8: Can you deploy and optimize an API?
```

### 11. Run Quality Checklists

Validate learning path quality:

- Run execute-checklist.md with learning-objectives-checklist.md
- Run execute-checklist.md with prerequisite-clarity-checklist.md

## Success Criteria

A completed learning path should have:

- [ ] Complete prerequisite dependency map
- [ ] Skill scaffolding from simple to complex
- [ ] No knowledge gaps or unexplained concepts
- [ ] Reader readiness checkpoints defined
- [ ] Optional vs. required chapters clearly marked
- [ ] Visual dependency diagram
- [ ] Alignment with stated learning objectives
- [ ] Alternative reading paths (if applicable)
- [ ] All checklists passed

## Common Pitfalls to Avoid

- **Circular dependencies**: Chapter A requires B, which requires A
- **Knowledge gaps**: Concepts used before being taught
- **Too steep progression**: Jumping from beginner to advanced without intermediate steps
- **Hidden prerequisites**: Assuming knowledge not covered in the book
- **No alternative paths**: Forcing linear reading when options exist
- **Unclear optional content**: Readers can't tell what they can skip

## Next Steps

After designing the learning path:

1. Update book outline with prerequisite information
2. Add reader readiness checkpoints to chapters
3. Include learning path diagram in book introduction or preface
4. Review with beta readers or instructional design expert
5. Update as chapter content evolves

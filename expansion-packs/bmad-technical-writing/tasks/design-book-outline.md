<!-- Powered by BMAD™ Core -->

# Design Book Outline

---

task:
id: design-book-outline
name: Design Book Outline
description: Create complete technical book structure with learning path and chapter breakdown
persona_default: instructional-designer
inputs:

- book-topic
- target-audience
- publisher-target (PacktPub, O'Reilly, Manning, Self-publish)
  steps:
- Elicit book concept, target audience, and technical scope
- Identify learning objectives for entire book (what readers will accomplish)
- Review publisher-specific structure requirements from book-structures.md
- Break into logical parts/sections based on learning progression
- Design chapter sequence ensuring proper scaffolding (simple to complex)
- For each chapter, define learning objectives and main topics
- Map prerequisites and dependencies between chapters
- Apply Bloom's Taxonomy to ensure progression (Remember→Understand→Apply→Analyze→Evaluate→Create)
- Plan code repository structure and testing approach
- Estimate page counts and timeline
- Use template book-outline-tmpl.yaml with create-doc.md task
- Run execute-checklist.md with learning-objectives-checklist.md
- Run execute-checklist.md with prerequisite-clarity-checklist.md
  output: docs/book-outline.md

---

## Purpose

This task guides you through creating a comprehensive book outline that balances publisher requirements, learning pedagogy, and technical accuracy. The result is a complete roadmap for the entire book.

## Prerequisites

Before starting this task:

- Have a clear book topic and target technology
- Know your target reader's skill level
- Understand which publisher you're targeting (or self-publishing)
- Access to book-structures.md and learning-frameworks.md knowledge bases

## Workflow Steps

### 1. Elicit Book Concept and Audience

Ask the user about:

- Book topic and core technology/framework
- Target reader's skill level (beginner, intermediate, advanced)
- Prerequisites readers should have
- What readers will accomplish after reading
- Estimated book length (200-400 pages typical)
- Publisher target (PacktPub, O'Reilly, Manning, self-publish)

### 2. Review Publisher Requirements

Consult book-structures.md for publisher-specific guidelines:

- **PacktPub**: Hands-on, project-based, practical tutorials
- **O'Reilly**: Learning path with exercises and examples
- **Manning**: Deep tutorial style with progressive complexity
- **Self-publish**: Flexible structure, but follow best practices

### 3. Define Book-Level Learning Objectives

Identify 5-10 major learning objectives for the entire book using action verbs:

- What will readers be able to CREATE after reading?
- What technologies will they IMPLEMENT?
- What concepts will they ANALYZE and EVALUATE?

Ensure objectives are:

- Measurable and specific
- Appropriate for target skill level
- Achievable within book scope

### 4. Design Part/Section Structure

Break the book into logical parts (typically 3-5 parts):

**Example Structure:**

- Part I: Foundations (Chapters 1-4)
- Part II: Core Concepts (Chapters 5-8)
- Part III: Advanced Topics (Chapters 9-12)
- Part IV: Real-World Applications (Chapters 13-15)

Each part should have:

- Clear learning arc
- Coherent theme
- Progressive difficulty

### 5. Create Chapter Sequence

For each chapter, define:

- Chapter number and title
- 3-5 learning objectives (using Bloom's taxonomy action verbs)
- Main topics covered
- Tutorials and exercises planned
- Code examples needed
- Estimated page count
- Prerequisites (which chapters must come before)
- Difficulty level

**Scaffolding Guidelines:**

- Start simple, add complexity gradually
- Each chapter builds on previous knowledge
- Introduce concepts before using them
- Provide practice before advancing

### 6. Map Dependencies

Create a dependency map:

- Which chapters must be completed before others?
- What external knowledge is assumed?
- Where are the major skill milestones?
- Are there any optional chapters?

### 7. Apply Bloom's Taxonomy

Ensure learning progression across the book:

- **Early chapters**: Remember, Understand (definitions, concepts)
- **Middle chapters**: Apply, Analyze (hands-on practice, debugging)
- **Later chapters**: Evaluate, Create (optimization, design decisions)

### 8. Plan Code Repository

Design companion code structure:

- Chapter folder organization
- Testing strategy (unit tests, integration tests)
- Version compatibility targets
- CI/CD pipeline for validation

### 9. Generate Book Outline

Use the create-doc.md task with book-outline-tmpl.yaml template to create the structured outline document.

### 10. Validate Outline

Run checklists:

- learning-objectives-checklist.md - Verify all objectives are measurable
- prerequisite-clarity-checklist.md - Ensure prerequisites are explicit

### 11. Review and Refine

Ask the user:

- Does the chapter progression feel natural?
- Are there any gaps in coverage?
- Is the scope appropriate for the target page count?
- Does this match publisher expectations?

## Success Criteria

A completed book outline should have:

- [ ] Clear target audience and prerequisites defined
- [ ] Book-level learning objectives (5-10 measurable outcomes)
- [ ] Part structure with 3-5 logical groupings
- [ ] Complete chapter list (typically 12-20 chapters)
- [ ] Each chapter has 3-5 learning objectives
- [ ] Dependencies and prerequisites mapped
- [ ] Scaffolding ensures proper progression
- [ ] Code repository structure planned
- [ ] Estimated page counts and timeline
- [ ] Publisher requirements incorporated
- [ ] All checklists passed

## Common Pitfalls to Avoid

- **Too much coverage**: Better to go deep on fewer topics
- **Poor scaffolding**: Don't use concepts before explaining them
- **Missing prerequisites**: Be explicit about what readers need
- **Inconsistent difficulty**: Avoid sudden jumps in complexity
- **No practice**: Include exercises and tutorials throughout
- **Ignoring publisher style**: Each publisher has specific expectations

## Next Steps

After completing the book outline:

1. Review with technical experts or potential readers
2. Create detailed chapter outlines (create-chapter-outline.md)
3. Begin drafting first chapter
4. Set up code repository structure

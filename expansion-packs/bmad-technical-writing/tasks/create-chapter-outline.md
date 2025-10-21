<!-- Powered by BMAD™ Core -->

# Create Chapter Outline

---

task:
id: create-chapter-outline
name: Create Chapter Outline
description: Structure detailed chapter plan with learning objectives and content breakdown
persona_default: tutorial-architect
inputs:

- chapter-number
- chapter-topic
- book-outline-reference
  steps:
- Review book outline context and learning path
- Define chapter number and title
- Identify 3-5 learning objectives using action verbs
- List prerequisites clearly (previous chapters, external knowledge)
- Plan introduction section (hook, overview, relevance)
- Break down main content sections with tutorials
- Design exercises and practice activities
- Create summary structure
- List code files needed
- Validate against book-level learning path
- Use template chapter-outline-tmpl.yaml with create-doc.md task
- Run execute-checklist.md with prerequisite-clarity-checklist.md
  output: manuscript/outlines/chapter-{{chapter_number}}-outline.md

---

## Purpose

This task guides you through creating a detailed chapter outline that balances theory, hands-on practice, and progressive skill building. A solid outline makes writing the chapter much easier.

## Prerequisites

Before starting this task:

- Book outline completed (provides context and learning path)
- Chapter topic and position in book determined
- Access to book-structures.md knowledge base
- Understanding of target audience

## Workflow Steps

### 1. Review Book Outline Context

Understand this chapter's role:

- Where does this chapter fit in the book?
- What chapters come before/after?
- What are the book-level learning objectives?
- What is the overall learning progression?

### 2. Define Chapter Metadata

Establish basic information:

- **Chapter number**: Position in book
- **Chapter title**: Clear, descriptive
- **Estimated page count**: Typical ranges 15-30 pages
- **Reading time**: Estimated time to complete (2-4 hours typical)
- **Difficulty level**: Beginner, Intermediate, Advanced

### 3. Identify Learning Objectives

Create 3-5 measurable objectives (see create-learning-objectives.md):

**Use action verbs:**

- "Implement user authentication using JWT tokens"
- "Debug async code using browser DevTools"
- "Optimize database queries for better performance"

**Ensure objectives:**

- Build on previous chapters
- Align with book learning path
- Are measurable and specific
- Match target difficulty level

### 4. List Prerequisites Explicitly

Define what readers need before starting:

**Previous Chapters:**

- "Chapter 3: Database Fundamentals"
- "Chapter 5: RESTful API Design"

**External Knowledge:**

- "Basic JavaScript ES6 syntax"
- "Understanding of HTTP request/response cycle"

**Software/Tools:**

- "Node.js 18+ installed"
- "PostgreSQL 14+ running locally"
- "VS Code or similar IDE"

**Setup Time:**

- "Approximately 30 minutes for environment setup"

### 5. Plan Introduction Section

Design the chapter opening (1-2 pages):

**Hook/Motivation:**

- Real-world problem this chapter solves
- Why this topic matters
- Common pain points addressed

**Overview:**

- What topics will be covered
- How sections connect
- What readers will build

**Relevance:**

- How this fits into larger application development
- Industry use cases
- Career relevance

### 6. Break Down Main Content Sections

For each major section of the chapter:

**Section Structure:**

1. **Section Title**: Descriptive and clear
2. **Concept Explanation**: Theory and background (2-4 pages)
3. **Tutorial/Walkthrough**: Hands-on implementation (3-6 pages)
4. **Code Examples**: List files and purpose
5. **Visuals**: Diagrams, screenshots needed
6. **Common Mistakes**: Pitfalls to highlight
7. **Troubleshooting**: Common issues and solutions

**Typical Chapter Structure:**

- **Introduction** (1-2 pages)
- **Section 1: Foundations** (5-7 pages)
- **Section 2: Implementation** (6-8 pages)
- **Section 3: Advanced Topics** (4-6 pages)
- **Exercises** (2-3 pages)
- **Summary** (1 page)

### 7. Design Exercises and Challenges

Create practice opportunities:

**Guided Practice (3-4 exercises):**

- Step-by-step instructions provided
- Builds confidence
- Reinforces key concepts

**Challenge Problems (1-2):**

- Requires independent problem-solving
- Tests deeper understanding
- Stretches skills

**For Each Exercise:**

- Clear instructions
- Expected outcome
- Difficulty level
- Estimated time
- Solution provided? (yes/no/hints only)

### 8. Plan Summary Section

Design chapter conclusion (1 page):

**Key Concepts Recap:**

- Bullet list of main takeaways
- Visual summary if helpful

**Skills Checklist:**

- "You can now..."
- Measurable accomplishments
- Links back to learning objectives

**Next Steps:**

- Preview of next chapter
- How skills will be built upon
- Optional advanced reading

### 9. List Code Files

Document all code examples:

**For Each File:**

- Filename (e.g., `auth-middleware.js`)
- Purpose (brief description)
- Language/version (e.g., "Node.js 18+")
- Dependencies (packages required)
- Testing requirements (unit tests needed?)

**Example:**

```
Code Files:
1. user-model.js - User database schema and validation
2. auth-controller.js - Authentication route handlers
3. jwt-utils.js - Token generation and verification utilities
4. auth.test.js - Unit tests for authentication logic
```

### 10. Validate Against Book Learning Path

Ensure chapter fits progression:

- Does this build on previous chapters naturally?
- Are prerequisites from earlier chapters met?
- Does this prepare readers for upcoming chapters?
- Is difficulty progression appropriate?
- Are there any gaps in coverage?

### 11. Generate Chapter Outline

Use the create-doc.md task with chapter-outline-tmpl.yaml template to create the structured outline document.

### 12. Run Quality Checklist

Execute prerequisite-clarity-checklist.md:

- [ ] Prerequisites explicitly listed
- [ ] External knowledge stated
- [ ] Required software documented
- [ ] Installation instructions provided
- [ ] Setup verification steps included

## Success Criteria

A completed chapter outline should have:

- [ ] Clear chapter number and title
- [ ] 3-5 measurable learning objectives
- [ ] Prerequisites explicitly documented
- [ ] Engaging introduction planned
- [ ] Main sections broken down with page estimates
- [ ] Tutorials and code examples identified
- [ ] Exercises and challenges designed
- [ ] Summary structure defined
- [ ] Code files list complete
- [ ] Validates against book learning path
- [ ] prerequisite-clarity-checklist.md passed

## Common Pitfalls to Avoid

- **Too much content**: Better to go deep on fewer topics
- **No hands-on practice**: Technical books need tutorials
- **Unclear prerequisites**: Be explicit about what readers need
- **Poor progression**: Concepts should build logically
- **Missing exercises**: Practice is essential for learning
- **Vague learning objectives**: Use specific, measurable outcomes
- **No troubleshooting**: Anticipate common issues
- **Inconsistent difficulty**: Avoid sudden complexity jumps

## Chapter Structure Patterns

**Tutorial-Heavy (PacktPub style):**

- Brief theory
- Extensive step-by-step walkthrough
- Multiple small exercises
- Project-based learning

**Concept-Heavy (O'Reilly style):**

- In-depth explanation
- Multiple examples
- Exercises after each concept
- Real-world applications

**Progressive Build (Manning style):**

- Introduce concept
- Simple implementation
- Iterate with improvements
- Advanced techniques
- Final polished version

## Next Steps

After completing chapter outline:

1. Review with technical expert or beta reader
2. Share with editor for feedback
3. Begin drafting chapter content
4. Create code examples (create-code-example.md)
5. Develop exercises and solutions
6. Test all code examples (test-code-examples.md)

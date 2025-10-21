<!-- Powered by BMAD™ Core -->

# Create Learning Objectives

---

task:
id: create-learning-objectives
name: Create Learning Objectives
description: Define measurable learning objectives for chapter or book section
persona_default: instructional-designer
inputs:

- chapter-or-section
- target-audience
  steps:
- Review chapter/section topic and content scope
- Define 3-5 learning objectives using action verbs from Bloom's Taxonomy
- Map objectives to Bloom's levels (Remember, Understand, Apply, Analyze, Evaluate, Create)
- Ensure objectives are measurable and specific
- Align objectives with book's overall learning path
- Define success criteria for each objective
- Identify assessment methods (exercises, projects, quizzes)
- Validate prerequisites are clear
- Run execute-checklist.md with learning-objectives-checklist.md
- Document estimated learning time
  output: Adds learning objectives section to chapter outline or book outline

---

## Purpose

This task helps you craft clear, measurable learning objectives that guide both the author (what to teach) and the reader (what they'll achieve). Well-defined objectives improve learning outcomes and book quality.

## Prerequisites

Before starting this task:

- Chapter or section topic identified
- Target audience skill level known
- Access to learning-frameworks.md knowledge base
- Understanding of Bloom's Taxonomy

## Bloom's Taxonomy Reference

Use action verbs appropriate to the learning level:

**Remember** (recall facts):

- Define, List, Name, Identify, Describe, Recognize

**Understand** (explain concepts):

- Explain, Summarize, Interpret, Compare, Classify

**Apply** (use knowledge):

- Implement, Execute, Use, Apply, Demonstrate, Build

**Analyze** (examine components):

- Analyze, Debug, Troubleshoot, Differentiate, Examine

**Evaluate** (make judgments):

- Evaluate, Assess, Critique, Optimize, Justify

**Create** (produce new work):

- Design, Create, Develop, Architect, Construct

## Workflow Steps

### 1. Review Content Scope

Understand what this chapter/section will cover:

- Main topics to be taught
- Depth of coverage
- Prerequisites assumed
- Where this fits in overall book

### 2. Draft Learning Objectives

Create 3-5 objectives following this formula:

**[Action Verb] + [Object] + [Context/Constraint]**

**Good Examples:**

- "Implement JWT authentication in an Express.js REST API"
- "Analyze database query performance using profiling tools"
- "Design a scalable microservices architecture using Docker"
- "Debug React component rendering issues using React DevTools"

**Bad Examples (too vague):**

- "Understand authentication" (no action, not measurable)
- "Learn about databases" (too broad, no specificity)
- "Know React" (not measurable, no context)

### 3. Map to Bloom's Taxonomy

Assign each objective to a Bloom's level:

- **Early chapters**: Focus on Remember, Understand, Apply
- **Middle chapters**: Focus on Apply, Analyze
- **Later chapters**: Focus on Analyze, Evaluate, Create

Ensure progression across book chapters.

### 4. Verify Measurability

Each objective should be testable:

**Ask:** "How will readers prove they've achieved this?"

**Assessment Methods:**

- Build a working project
- Complete coding exercises
- Answer quiz questions
- Debug sample problems
- Create something new

### 5. Define Success Criteria

For each objective, specify what "success" looks like:

**Example:**

- **Objective**: "Implement JWT authentication in Express.js REST API"
- **Success Criteria**:
  - User can register and receive JWT token
  - Protected routes verify token correctly
  - Invalid tokens are rejected with 401 error
  - Tokens expire after specified time

### 6. Check Alignment with Book Learning Path

Verify objectives fit the progression:

- Do they build on previous chapters?
- Do they prepare for future chapters?
- Are they appropriate for target audience skill level?
- Do they contribute to book-level objectives?

### 7. Identify Assessment Methods

Determine how readers will practice:

- **Exercises**: Step-by-step guided practice
- **Challenges**: Independent problem-solving
- **Projects**: Comprehensive application
- **Quizzes**: Knowledge checks
- **Debugging tasks**: Fix broken code

### 8. Validate Prerequisites

For each objective, ensure prerequisites are clear:

- What must readers know before starting?
- Which previous chapters must be completed?
- What external knowledge is assumed?
- Are prerequisites explicitly stated?

### 9. Estimate Learning Time

Provide realistic time estimates:

- Time to read/study content
- Time to complete exercises
- Time for practice and experimentation
- Total chapter completion time

### 10. Run Quality Checklist

Execute learning-objectives-checklist.md:

- [ ] Objectives use action verbs (Bloom's taxonomy)
- [ ] Objectives are measurable
- [ ] Objectives align with content
- [ ] Prerequisites clearly stated
- [ ] Difficulty level appropriate

## Success Criteria

Learning objectives are complete when:

- [ ] 3-5 objectives defined per chapter/section
- [ ] All objectives use measurable action verbs
- [ ] Mapped to Bloom's Taxonomy levels
- [ ] Success criteria defined for each
- [ ] Assessment methods identified
- [ ] Prerequisites validated
- [ ] Aligned with book learning path
- [ ] Time estimates provided
- [ ] learning-objectives-checklist.md passed

## Common Pitfalls to Avoid

- **Too vague**: "Understand databases" → "Design normalized relational database schemas"
- **Not measurable**: "Know about async" → "Implement asynchronous code using Promises and async/await"
- **Too many objectives**: Stick to 3-5 key objectives per chapter
- **Wrong Bloom's level**: Don't ask beginners to "Evaluate" or "Create" in early chapters
- **No assessment**: Always define how objectives will be verified
- **Misalignment**: Objectives don't match actual chapter content

## Examples by Bloom's Level

**Remember (Early chapters):**

- "List the main components of the React ecosystem"
- "Identify common SQL query types (SELECT, INSERT, UPDATE, DELETE)"

**Understand (Early-mid chapters):**

- "Explain how async/await improves code readability compared to callbacks"
- "Describe the request-response cycle in Express.js applications"

**Apply (Mid chapters):**

- "Implement user authentication using Passport.js and sessions"
- "Build a RESTful API with CRUD operations for a blog platform"

**Analyze (Mid-late chapters):**

- "Debug memory leaks in Node.js applications using Chrome DevTools"
- "Analyze API performance bottlenecks using profiling tools"

**Evaluate (Late chapters):**

- "Evaluate trade-offs between SQL and NoSQL databases for specific use cases"
- "Assess security vulnerabilities in web applications using OWASP guidelines"

**Create (Late chapters):**

- "Design a scalable microservices architecture for an e-commerce platform"
- "Develop a CI/CD pipeline for automated testing and deployment"

## Next Steps

After creating learning objectives:

1. Share with technical reviewers for feedback
2. Use objectives to guide chapter content creation
3. Design exercises that directly assess objectives
4. Create summary section that reviews objective completion
5. Test with beta readers to verify achievability

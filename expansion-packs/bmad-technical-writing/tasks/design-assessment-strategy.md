<!-- Powered by BMAD™ Core -->

# Design Assessment Strategy

---

task:
id: design-assessment-strategy
name: Design Assessment Strategy
description: Design aligned assessment strategy including exercises, quizzes, and projects based on learning objectives
persona_default: instructional-designer
inputs: - learning-objectives (path to objectives or chapter outline) - chapter-outline (path to chapter or book outline) - target-audience (beginner/intermediate/advanced)
steps: - Load learning objectives and chapter content - Map each objective to Bloom's Taxonomy level - Select appropriate assessment types per Bloom's level - Design difficulty progression for exercises - Specify formative vs summative assessment placement - Create exercise specification templates - Plan hands-on project requirements - Build assessment alignment matrix - Verify coverage of all learning objectives - Balance difficulty distribution - Run execute-checklist.md with assessment-strategy-checklist.md
output: Assessment strategy document with alignment matrix, exercise specs, and project plans

---

## Purpose

This task helps you design a comprehensive assessment strategy aligned with learning objectives and Bloom's Taxonomy levels. Effective assessments provide practice opportunities, verify learning, and build confidence through appropriate difficulty progression.

## Prerequisites

Before starting this task:

- Learning objectives defined (use create-learning-objectives.md if needed)
- Chapter outline exists
- Target audience level known
- Understanding of Bloom's Taxonomy (see learning-frameworks.md)
- Familiarity with formative vs summative assessment

## Assessment Types

### By Bloom's Level

| Bloom's Level | Assessment Types                   | Examples                                  |
| ------------- | ---------------------------------- | ----------------------------------------- |
| Remember      | Quiz, flashcards, matching         | "List the HTTP methods", "Define REST"    |
| Understand    | Short answer, concept mapping      | "Explain why async is important"          |
| Apply         | Coding exercises, tutorials        | "Build a REST endpoint"                   |
| Analyze       | Debugging, comparison tasks        | "Debug this code", "Compare SQL vs NoSQL" |
| Evaluate      | Code review, architecture critique | "Assess this API design"                  |
| Create        | Projects, system design            | "Design a microservices architecture"     |

### By Purpose

**Formative Assessments** (Practice & Feedback):

- In-chapter exercises
- Interactive tutorials
- Quick knowledge checks
- Debugging challenges
- Goal: Support learning, provide feedback, build skills

**Summative Assessments** (Mastery Verification):

- End-of-chapter projects
- Comprehensive exercises
- Chapter quizzes
- Capstone projects
- Goal: Verify mastery, gate progression, demonstrate competency

## Workflow Steps

### 1. Load Learning Objectives

Review objectives for chapter or section:

**Example Chapter:** "Express.js REST APIs"

**Learning Objectives:**

1. Explain the principles of RESTful API design (Understand)
2. Implement CRUD operations using Express.js (Apply)
3. Apply middleware for request processing (Apply)
4. Debug common Express.js routing issues (Analyze)
5. Evaluate API design choices for scalability (Evaluate)

### 2. Map Objectives to Bloom's Levels

Classify each objective (already shown above):

| Objective                 | Action Verb | Bloom's Level |
| ------------------------- | ----------- | ------------- |
| Explain REST principles   | Explain     | Understand    |
| Implement CRUD operations | Implement   | Apply         |
| Apply middleware          | Apply       | Apply         |
| Debug routing issues      | Debug       | Analyze       |
| Evaluate design choices   | Evaluate    | Evaluate      |

**Distribution:**

- Understand: 1 (20%)
- Apply: 2 (40%)
- Analyze: 1 (20%)
- Evaluate: 1 (20%)

### 3. Select Assessment Types per Level

Match each objective to appropriate assessment:

| Objective        | Bloom's Level | Assessment Type                         | Specific Assessment                              |
| ---------------- | ------------- | --------------------------------------- | ------------------------------------------------ |
| Explain REST     | Understand    | Short answer quiz                       | "Explain in 2-3 sentences why REST is stateless" |
| Implement CRUD   | Apply         | Guided exercise + Independent challenge | "Build a blog API with full CRUD"                |
| Apply middleware | Apply         | Coding exercise                         | "Add logging and error handling middleware"      |
| Debug routing    | Analyze       | Debugging challenge                     | "Fix 5 routing bugs in this code"                |
| Evaluate design  | Evaluate      | Case study analysis                     | "Critique this API design, suggest improvements" |

### 4. Design Difficulty Progression

Create exercises that progress from easy to challenging:

**Example: "Implement CRUD Operations" (Apply Level)**

**Exercise Progression:**

```markdown
Exercise 1: Simple GET (Easy)

- Difficulty: 3/10
- Time: 10 minutes
- Guidance: Full code template with TODOs
- Task: "Complete the GET /users endpoint to return user list"

Exercise 2: GET with Parameters (Easy-Medium)

- Difficulty: 4/10
- Time: 15 minutes
- Guidance: Partial template, hints provided
- Task: "Implement GET /users/:id with error handling"

Exercise 3: POST Endpoint (Medium)

- Difficulty: 5/10
- Time: 20 minutes
- Guidance: High-level steps only
- Task: "Create POST /users to add new user with validation"

Exercise 4: Full CRUD (Medium-Hard)

- Difficulty: 6/10
- Time: 30 minutes
- Guidance: Requirements only
- Task: "Implement PUT /users/:id and DELETE /users/:id"

Exercise 5: Complete API (Challenge)

- Difficulty: 7/10
- Time: 45 minutes
- Guidance: None (requirements only)
- Task: "Build a complete blog post API with CRUD + search"
```

### 5. Specify Formative vs Summative Placement

Plan where each assessment appears:

**Chapter Structure with Assessments:**

```markdown
## Chapter 5: Express.js REST APIs

### Section 5.1: REST Principles

Content: [Theory and examples]
✅ Formative: Knowledge check quiz (2 questions)

### Section 5.2: Basic Routing

Content: [Tutorial on GET endpoints]
✅ Formative: Exercise 1 - Simple GET
✅ Formative: Exercise 2 - GET with parameters

### Section 5.3: Handling Requests

Content: [POST, PUT, DELETE methods]
✅ Formative: Exercise 3 - POST endpoint
✅ Formative: Exercise 4 - Full CRUD

### Section 5.4: Middleware

Content: [Middleware concepts and examples]
✅ Formative: Exercise 5 - Add middleware

### Section 5.5: Debugging

Content: [Common issues and solutions]
✅ Formative: Debugging challenge

### Section 5.6: Chapter Summary

✅ Summative: Complete API project (combines all skills)
✅ Summative: Chapter quiz (10 questions covering all objectives)
```

**Assessment Distribution:**

- Formative: 6 assessments throughout chapter (practice & feedback)
- Summative: 2 assessments at end (verify mastery)

### 6. Create Exercise Specification Templates

Define detailed specifications for each exercise:

**Exercise Specification Template:**

````markdown
### Exercise [N]: [Title]

**Learning Objective:** [Which objective this assesses]
**Bloom's Level:** [Level]
**Difficulty:** [1-10]
**Estimated Time:** [Minutes]
**Type:** [Formative/Summative]

**Prerequisites:**

- [Concept or skill required]
- [Previous exercise completed]

**Task Description:**
[Clear description of what student must do]

**Starting Code:**

```javascript
[Code template or starter code, if applicable]
```
````

**Requirements:**

- [ ] [Specific requirement 1]
- [ ] [Specific requirement 2]
- [ ] [Specific requirement 3]

**Success Criteria:**

- [How to verify exercise is complete correctly]

**Hints:**

- [Optional hints for students who struggle]

**Solution:**
[Complete working solution - in solutions manual or online repo]

**Common Mistakes:**

- [Common error students make + how to fix]

**Extension Challenge:**
[Optional advanced variation for fast learners]

````

**Example Exercise Specification:**

```markdown
### Exercise 3: Create POST Endpoint

**Learning Objective:** Implement CRUD operations using Express.js
**Bloom's Level:** Apply
**Difficulty:** 5/10
**Estimated Time:** 20 minutes
**Type:** Formative

**Prerequisites:**
- Completed Exercises 1-2 (GET endpoints)
- Understanding of HTTP POST method
- Familiarity with JSON parsing

**Task Description:**
Create a POST /users endpoint that accepts user data and adds a new user to the in-memory database. The endpoint should validate required fields and return appropriate status codes.

**Starting Code:**
```javascript
const express = require('express');
const app = express();
app.use(express.json());

let users = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' }
];

// TODO: Implement POST /users endpoint

app.listen(3000, () => console.log('Server running on port 3000'));
````

**Requirements:**

- [ ] Accept POST requests to /users
- [ ] Validate required fields: name, email
- [ ] Generate unique ID for new user
- [ ] Add user to users array
- [ ] Return 201 status with created user
- [ ] Return 400 status if validation fails

**Success Criteria:**

- POST /users with valid data returns 201 and user object with ID
- POST /users with missing name returns 400 with error message
- POST /users with missing email returns 400 with error message
- User is added to users array and persists

**Hints:**

- Use `users.length + 1` for simple ID generation
- Check if `req.body.name` and `req.body.email` exist
- Use `res.status(201).json(...)` for success response

**Solution:**

```javascript
app.post('/users', (req, res) => {
  const { name, email } = req.body;

  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required' });
  }

  const newUser = {
    id: users.length + 1,
    name,
    email,
  };

  users.push(newUser);
  res.status(201).json(newUser);
});
```

**Common Mistakes:**

- Forgetting to use `express.json()` middleware → req.body undefined
- Using `res.send()` instead of `res.json()` → inconsistent response format
- Not returning after error response → code continues executing
- Using `users.length` instead of `users.length + 1` → duplicate IDs

**Extension Challenge:**
Add email format validation using regex and ensure email uniqueness before adding user.

````

### 7. Plan Hands-On Project Requirements

Design comprehensive projects that integrate multiple objectives:

**Project Specification Template:**

```markdown
# Project [N]: [Title]

## Overview
[Brief description of what students will build]

## Learning Objectives Covered
- [Objective 1]
- [Objective 2]
- ...

## Bloom's Levels Assessed
- Apply: [Specific skills]
- Analyze: [Specific skills]
- Create: [Specific skills]

## Project Requirements

### Core Features (Must Have)
1. [Feature 1 - with acceptance criteria]
2. [Feature 2 - with acceptance criteria]

### Optional Features (Nice to Have)
1. [Feature 1]
2. [Feature 2]

## Specifications

### API Endpoints
| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | /api/resource | ... | 200, 404 |

### Data Models
[Define data structures/schemas]

### Technical Constraints
- Must use Express.js
- Must include error handling
- Must validate inputs
- Must include at least 3 middleware functions

## Starter Code
[Link to starter repository or template]

## Deliverables
- [ ] Working application code
- [ ] README with setup instructions
- [ ] API documentation
- [ ] Test results (manual or automated)

## Rubric

| Criteria | Excellent (5) | Good (4) | Satisfactory (3) | Needs Improvement (2) | Incomplete (1) |
|----------|---------------|----------|------------------|-----------------------|----------------|
| Functionality | All features work | Most features work | Core features work | Some features work | Doesn't run |
| Code Quality | Clean, well-organized | Mostly clean | Functional but messy | Hard to follow | Poor quality |
| Error Handling | Comprehensive | Most errors handled | Basic handling | Minimal handling | None |
| Documentation | Complete & clear | Mostly complete | Basic docs | Minimal docs | None |

## Estimated Time
[Hours to complete]

## Resources
- [Link to relevant documentation]
- [Link to example implementations]
````

**Example Project:**

````markdown
# Project 1: Blog API with Authentication

## Overview

Build a RESTful API for a blog platform with user authentication, CRUD operations for posts, and comment functionality.

## Learning Objectives Covered

- Implement CRUD operations using Express.js
- Apply middleware for request processing
- Debug common Express.js routing issues
- Evaluate API design choices for scalability

## Bloom's Levels Assessed

- Apply: Implementing routes, middleware, authentication
- Analyze: Debugging issues, testing endpoints
- Evaluate: Making design decisions about architecture
- Create: Designing overall API structure

## Project Requirements

### Core Features (Must Have)

1. User registration and login (JWT authentication)
   - POST /auth/register - Create new user account
   - POST /auth/login - Login and receive JWT token
2. Blog post CRUD
   - GET /posts - List all posts
   - GET /posts/:id - Get single post
   - POST /posts - Create post (authenticated)
   - PUT /posts/:id - Update post (authenticated, owner only)
   - DELETE /posts/:id - Delete post (authenticated, owner only)
3. Comment functionality
   - POST /posts/:id/comments - Add comment (authenticated)
   - GET /posts/:id/comments - Get post comments

### Optional Features (Nice to Have)

1. Pagination for post listings
2. Search/filter posts by author or tags
3. Like/favorite posts

## Specifications

### Data Models

User:

```javascript
{
  id: number,
  username: string,
  email: string,
  password: string (hashed)
}
```
````

Post:

```javascript
{
  id: number,
  title: string,
  content: string,
  authorId: number,
  createdAt: date,
  updatedAt: date
}
```

Comment:

```javascript
{
  id: number,
  content: string,
  postId: number,
  authorId: number,
  createdAt: date
}
```

### Technical Constraints

- Use Express.js 4.x
- Use in-memory data storage (arrays) or JSON files
- Use JWT for authentication
- Include input validation middleware
- Include error handling middleware
- All endpoints must return JSON

## Starter Code

[Provide link to GitHub repo with basic Express setup]

## Deliverables

- [ ] Working Express.js application
- [ ] README.md with setup and API documentation
- [ ] Postman collection or API documentation
- [ ] Screenshot or video demonstrating functionality

## Rubric

| Criteria          | Excellent (5)                                              | Good (4)                         | Satisfactory (3)                   | Needs Improvement (2)   | Incomplete (1)        |
| ----------------- | ---------------------------------------------------------- | -------------------------------- | ---------------------------------- | ----------------------- | --------------------- |
| Functionality     | All core + optional features                               | All core features work perfectly | Core features work with minor bugs | Some core features work | Minimal functionality |
| Authentication    | Secure JWT implementation with proper verification         | JWT works, minor security issues | Basic JWT, some security gaps      | Broken authentication   | None                  |
| Error Handling    | Comprehensive error handling with appropriate status codes | Good error handling              | Basic error responses              | Minimal error handling  | No error handling     |
| Code Organization | Excellent structure, routes/middleware separated           | Good structure                   | Functional but messy               | Poor organization       | Very disorganized     |
| API Design        | RESTful, consistent, well-designed                         | Mostly RESTful                   | Functional but inconsistent        | Poor API design         | Non-RESTful           |
| Documentation     | Complete API docs + code comments                          | Good documentation               | Basic docs                         | Minimal docs            | No documentation      |

**Total Points:** 30
**Passing:** 18/30 (60%)

## Estimated Time

6-8 hours

## Resources

- Express.js documentation: https://expressjs.com
- JWT documentation: https://jwt.io
- Example blog API: [link]

````

### 8. Build Assessment Alignment Matrix

Create comprehensive matrix showing coverage:

**Assessment Alignment Matrix Template:**

| Learning Objective | Bloom's Level | Formative Assessments | Summative Assessments | Coverage |
|--------------------|---------------|----------------------|----------------------|----------|
| [Objective 1] | [Level] | [List of exercises] | [List of projects/quizzes] | ✅/⚠️/❌ |

**Example Matrix:**

| Learning Objective | Bloom's | Formative | Summative | Coverage |
|--------------------|---------|-----------|-----------|----------|
| Explain REST principles | Understand | Section 5.1 Quiz (2Q) | Chapter Quiz (Q1-3) | ✅ |
| Implement CRUD operations | Apply | Ex 1-4, Tutorial | Project 1 | ✅ |
| Apply middleware | Apply | Ex 5 | Project 1 | ✅ |
| Debug routing issues | Analyze | Debug Challenge | Project 1 (self-debugging) | ✅ |
| Evaluate design choices | Evaluate | Section 5.6 Discussion | Project 1 (design decisions doc) | ⚠️ |

**Coverage Status:**
- ✅ Well covered (multiple assessments)
- ⚠️ Minimal coverage (1-2 assessments)
- ❌ Not assessed

**Analysis:**
- "Evaluate design choices" has minimal coverage - add case study or architecture review exercise

### 9. Verify Coverage of All Objectives

Ensure every objective is assessed:

**Coverage Checklist:**

```markdown
## Coverage Verification

### Objective 1: Explain REST principles
- ✅ Formative: Section quiz
- ✅ Summative: Chapter quiz
- ✅ Adequate coverage

### Objective 2: Implement CRUD operations
- ✅ Formative: 4 exercises
- ✅ Summative: Project 1
- ✅ Adequate coverage

### Objective 3: Apply middleware
- ✅ Formative: 1 exercise
- ✅ Summative: Project 1
- ⚠️ Consider adding 1 more formative exercise

### Objective 4: Debug routing issues
- ✅ Formative: Debug challenge
- ⚠️ Summative: Only implicit in project
- ⚠️ Consider explicit debugging summative assessment

### Objective 5: Evaluate design choices
- ⚠️ Formative: Discussion only
- ⚠️ Summative: Design doc in project
- ❌ Needs explicit evaluation exercise (case study or critique)

## Action Items
1. Add formative middleware exercise
2. Add summative debugging assessment
3. Add architecture evaluation case study
````

### 10. Balance Difficulty Distribution

Verify appropriate spread of difficulty levels:

**Difficulty Distribution Analysis:**

```markdown
## Assessment Difficulty Distribution

### All Assessments (10 total)

Difficulty Breakdown:

- Easy (1-3): 3 assessments (30%)
- Medium (4-6): 5 assessments (50%)
- Hard (7-10): 2 assessments (20%)

Target for Intermediate Audience:

- Easy: 20-30% ✅
- Medium: 50-60% ✅
- Hard: 20-30% ✅

### By Assessment Type

**Formative (7 assessments):**

- Easy: 3 (43%)
- Medium: 3 (43%)
- Hard: 1 (14%)
  Analysis: Good progression - more easy/medium for practice

**Summative (3 assessments):**

- Easy: 0 (0%)
- Medium: 2 (67%)
- Hard: 1 (33%)
  Analysis: Good - summative should be moderate to challenging

### Progression Check

Assessments in order of appearance:

1. Quiz (Easy) ✅
2. Exercise 1 (Easy) ✅
3. Exercise 2 (Easy-Medium) ✅
4. Exercise 3 (Medium) ✅
5. Exercise 4 (Medium) ✅
6. Exercise 5 (Medium-Hard) ✅
7. Debug Challenge (Hard) ✅
8. Project (Hard) ✅
9. Chapter Quiz (Medium) ✅

✅ Clear progression from easy to hard
```

### 11. Run Quality Checklist

Execute assessment-strategy-checklist.md (if available):

- [ ] All learning objectives have aligned assessments
- [ ] Bloom's levels match assessment types
- [ ] Formative and summative assessments included
- [ ] Exercise specifications created
- [ ] Project requirements defined
- [ ] Assessment alignment matrix completed
- [ ] Coverage verified for all objectives
- [ ] Difficulty progression appropriate
- [ ] Assessment balance appropriate (formative > summative)

## Success Criteria

Assessment strategy is complete when:

- [ ] Every learning objective has 2+ aligned assessments
- [ ] Assessment types match Bloom's levels
- [ ] Difficulty progression from easy to hard
- [ ] Both formative and summative assessments included
- [ ] Exercise specifications created with success criteria
- [ ] Project plan includes rubric
- [ ] Assessment alignment matrix completed
- [ ] Coverage verified (no ❌ in matrix)
- [ ] Difficulty distribution balanced

## Output Format

```markdown
# Assessment Strategy: [Chapter Name]

## Learning Objectives Summary

[List with Bloom's levels]

## Assessment Overview

**Total Assessments:** [N]

- Formative: [N]
- Summative: [N]

**Difficulty Distribution:**

- Easy: [N] ([%])
- Medium: [N] ([%])
- Hard: [N] ([%])

## Assessment Alignment Matrix

[Full matrix table]

## Formative Assessments

### [Assessment 1]: [Title]

[Full specification]

### [Assessment 2]: [Title]

[Full specification]

## Summative Assessments

### [Assessment 1]: [Title]

[Full specification]

### Project: [Title]

[Full project requirements with rubric]

## Coverage Analysis

[Verification that all objectives assessed]

## Difficulty Progression

[Chart or analysis of difficulty curve]

## Implementation Notes

[Guidance for implementing assessments in chapter]
```

## Common Pitfalls to Avoid

**❌ Assessments don't match objectives:**

```
Objective: "Explain REST principles" (Understand)
Assessment: Build complete API (Create)
```

Fix: Match assessment type to Bloom's level

**❌ No formative practice before summative:**

```
Teach concept → Immediate project with no practice
```

Fix: Include formative exercises between teaching and summative

**❌ All assessments same difficulty:**

```
5 exercises all rated 5/10
```

Fix: Progress from easy to hard

**❌ Vague success criteria:**

```
"Build a good API"
```

Fix: Specific, measurable criteria with rubric

**❌ Too many summative assessments:**

```
10 projects, 0 practice exercises
```

Fix: 70-80% formative, 20-30% summative ratio

## Examples

### Example 1: Beginner Chapter Assessment Strategy

**Chapter:** "Variables and Data Types" (Python)

**Objectives:**

1. List basic Python data types (Remember)
2. Explain differences between mutable and immutable types (Understand)
3. Use variables in simple programs (Apply)

**Assessments:**

**Formative:**

- Quiz: "Name 5 Python data types" (Remember)
- Short answer: "Explain mutability" (Understand)
- Exercise 1: Variable declaration practice (Apply - Easy)
- Exercise 2: Type conversion (Apply - Medium)

**Summative:**

- Mini-project: "Build a calculator using variables" (Apply)

**Matrix:**

| Objective          | Bloom's    | Formative    | Summative          | Coverage |
| ------------------ | ---------- | ------------ | ------------------ | -------- |
| List data types    | Remember   | Quiz         | Chapter quiz       | ✅       |
| Explain mutability | Understand | Short answer | Chapter quiz       | ✅       |
| Use variables      | Apply      | Ex 1-2       | Calculator project | ✅       |

### Example 2: Advanced Chapter Assessment Strategy

**Chapter:** "Microservices Architecture" (Advanced)

**Objectives:**

1. Analyze trade-offs of microservices vs monoliths (Analyze)
2. Evaluate service decomposition strategies (Evaluate)
3. Design a microservices system (Create)

**Assessments:**

**Formative:**

- Case study analysis: "Analyze Uber's microservices migration" (Analyze)
- Discussion: "Evaluate different decomposition patterns" (Evaluate)
- Design exercise: "Decompose this monolith" (Create - guided)

**Summative:**

- Architecture project: "Design complete microservices system" (Create)
- Written analysis: "Justify your architectural decisions" (Evaluate)

**Matrix:**

| Objective           | Bloom's  | Formative       | Summative            | Coverage |
| ------------------- | -------- | --------------- | -------------------- | -------- |
| Analyze trade-offs  | Analyze  | Case study      | Written analysis     | ✅       |
| Evaluate strategies | Evaluate | Discussion      | Written analysis     | ✅       |
| Design system       | Create   | Design exercise | Architecture project | ✅       |

## Next Steps

After completing assessment strategy:

1. Share with content-developer for feedback
2. Implement exercise specifications (use design-exercises.md task)
3. Create exercise solutions and rubrics
4. Test exercises with sample audience
5. Integrate assessments into chapter outline
6. Update chapter structure to include assessment placement
7. Create instructor guide with grading rubrics
8. Build exercise repository or starter code templates

<!-- Powered by BMAD™ Core -->

# Develop Tutorial

---

task:
id: develop-tutorial
name: Develop Tutorial
description: Create hands-on step-by-step tutorial with tested code, clear instructions, and troubleshooting
persona_default: tutorial-architect
inputs:

- tutorial-topic
- learning-objective
- difficulty-level
  steps:
- Identify specific learning objective for tutorial
- Define prerequisite knowledge and setup requirements
- Design step-by-step progression (8-15 steps typical)
- Write clear, actionable instructions for each step
- Create and test code examples for each step
- Document expected outputs at each step
- Add troubleshooting section for common issues
- Test complete tutorial end-to-end
- Verify progressive difficulty and skill building
- Include summary and next steps
- Run execute-checklist.md with tutorial-effectiveness-checklist.md
- Use template tutorial-section-tmpl.yaml with create-doc.md
  output: tutorials/{{tutorial-slug}}.md

---

## Purpose

Create effective hands-on tutorials that guide learners through building something concrete while learning key concepts. Great tutorials balance clear instruction with learning depth.

## Prerequisites

- Learning objective clearly defined
- Subject matter expertise in tutorial topic
- Testing environment available
- Access to learning-frameworks.md knowledge base

## Workflow Steps

### 1. Identify Learning Objective

Define what students will accomplish:

**Specific and Measurable:**

- "Build a REST API with authentication" (good)
- "Learn about APIs" (too vague)

**Achievable Scope:**

- 30-45 minutes for basic tutorials
- 1-2 hours for intermediate
- 2-4 hours for advanced

**Clear Success Criteria:**

- What will work at the end?
- What skills will be demonstrated?
- What can student verify?

### 2. Define Prerequisites

Be explicit about requirements:

**Knowledge Prerequisites:**

- "Understanding of Python functions and classes"
- "Completed Tutorial 2: Flask Basics"
- "Familiarity with HTTP request/response cycle"

**Software Requirements:**

- "Python 3.11+"
- "PostgreSQL 15+ running locally"
- "VS Code or similar editor"

**Setup Steps:**

- "Clone starter repository"
- "Create virtual environment"
- "Install dependencies: `pip install -r requirements.txt`"

**Time Estimates:**

- Setup time: 10 minutes
- Tutorial time: 45 minutes
- Total: ~1 hour

### 3. Design Step-by-Step Progression

Plan the tutorial flow (typically 8-15 steps):

**Logical Progression:**

1. Setup and initialization
2. Core concept introduction
3. Basic implementation
4. Build on basics
5. Add complexity
6. Handle edge cases
7. Test/validate
8. Summary/reflection

**Each Step Should:**

- Build on previous steps
- Accomplish one clear goal
- Be testable/verifiable
- Take 3-8 minutes

**Progressive Difficulty:**

- Start simple (foundational)
- Add complexity gradually
- End with realistic scenario

### 4. Write Clear Instructions

Use consistent, actionable format:

**Step Format:**

````
**Step N: [Action-Oriented Title]**

[Brief explanation of what this step accomplishes]

**Instructions:**
1. [Specific action in imperative voice]
2. [Next action]
3. [Etc.]

**Code:**
```language
[Complete code to add/modify]
````

**Expected Output:**

```
[What student should see]
```

**Why This Matters:**
[Explain the concept or purpose]

**Verification:**
[How to confirm this step worked]

```

**Imperative Voice:**
- "Create a new file..." (good)
- "You should create..." (wordy)
- "We'll create..." (okay but less direct)

### 5. Create and Test Code Examples

Develop working code for every step:

**Code Quality:**
- Must run exactly as shown
- Include all necessary imports
- Show complete context
- Follow best practices
- Include comments explaining key lines

**Testing:**
- Run every code example
- Verify outputs match documentation
- Test in fresh environment
- Check for missing dependencies
- Validate error messages

**Incremental Development:**
- Each step adds to previous code
- Show only what changes (or full file if clearer)
- Maintain working state after each step
- Avoid breaking changes mid-tutorial

**Use:** create-code-example.md and test-code-examples.md tasks

### 6. Document Expected Outputs

Show what success looks like:

**After Key Steps:**
```

After Step 3, running `python app.py` should display:

- Running on http://127.0.0.1:5000
- Debug mode: on

Visiting http://localhost:5000/health should return:
{"status": "healthy", "timestamp": "2024-01-15T10:30:00Z"}

```

**Screenshots (where helpful):**
- UI results
- Browser developer tools
- Database state
- Terminal output

**File Structure:**
```

After Step 5, your project should look like:
tutorial-app/
├── app.py
├── models/
│ └── user.py
├── routes/
│ └── auth.py
└── tests/
└── test_auth.py

```

### 7. Add Troubleshooting Section

Anticipate and solve common problems:

**For Each Common Issue:**

**Problem:** [Error message or symptom]

**Likely Cause:** [What usually causes this]

**Diagnosis:** [How to check for this issue]

**Fix:** [Step-by-step solution]

**Verification:** [How to confirm it's fixed]

**Example:**
```

**Problem:** ImportError: No module named 'flask'

**Cause:** Flask not installed or wrong Python environment

**Diagnosis:**

1. Check virtual environment activated: `which python`
2. Check installed packages: `pip list | grep -i flask`

**Fix:**

1. Activate virtual environment: `source venv/bin/activate`
2. Install Flask: `pip install flask`
3. Verify: `python -c "import flask; print(flask.__version__)"`

**Verification:** Re-run your app - should start without import errors

```

**Include 3-5 most common issues** based on typical student mistakes.

### 8. Test Tutorial End-to-End

Validate the complete tutorial:

**Fresh Environment Test:**
- Start with clean environment
- Follow your own instructions exactly
- Don't skip any steps
- Note any assumptions you made
- Time how long it actually takes

**Someone Else Tests:**
- Have another person try the tutorial
- Watch for confusion points
- Note questions they ask
- Identify unclear instructions

**Validation Questions:**
- Does every step work as described?
- Are outputs accurate?
- Is prerequisite list complete?
- Is difficulty appropriate?
- Does learning objective get achieved?

**Use:** tutorial-effectiveness-checklist.md

### 9. Verify Progressive Difficulty

Ensure appropriate skill building:

**Check Progression:**
- Early steps are simple and foundational
- Complexity increases gradually
- No sudden jumps in difficulty
- Builds on prior knowledge systematically

**Cognitive Load:**
- Not too much new information at once
- One new concept per step when possible
- Reinforcement through repetition
- Clear explanations for complex topics

**Scaffolding:**
- More guidance early
- Gradually reduce hand-holding
- Final steps require more independence
- Prepares for next-level tutorials

### 10. Include Summary and Next Steps

Conclude effectively:

**What You Learned:**
- Recap key concepts covered
- Skills practiced in tutorial
- How this connects to broader topic

**What You Built:**
- Concrete deliverable description
- How it demonstrates learning
- Real-world applications

**Next Steps:**
- Related tutorials to try
- How to extend this project
- Resources for deeper learning

**Extension Challenges (Optional):**
- "Add password reset functionality"
- "Implement email verification"
- "Add OAuth2 social login"

## Output

Complete tutorial should include:

- Clear learning objective
- Explicit prerequisites
- 8-15 step-by-step instructions
- Tested, working code
- Expected outputs
- Troubleshooting guide
- Summary and next steps

**Use template:** tutorial-section-tmpl.yaml

## Quality Standards

Effective tutorial:

✓ Clear, specific learning objective
✓ Complete prerequisite list
✓ Actionable, numbered steps
✓ All code tested and works
✓ Expected outputs documented
✓ Troubleshooting for common issues
✓ Progressive difficulty
✓ Achievable in stated time
✓ Engaging and motivating

## Common Pitfalls

Avoid:

❌ Skipping setup steps (assumes too much)
❌ Code that doesn't actually run
❌ Unclear or vague instructions
❌ Jumping difficulty too quickly
❌ No verification steps
❌ Missing expected outputs
❌ Untested tutorial (always test!)
❌ Too long (break into multiple tutorials)

## Next Steps

After creating tutorial:

1. Include in relevant chapter
2. Add to tutorial repository
3. Test with target audience if possible
4. Gather feedback and iterate
5. Update based on common student questions
```

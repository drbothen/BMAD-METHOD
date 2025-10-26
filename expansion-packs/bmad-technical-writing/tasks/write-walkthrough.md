<!-- Powered by BMAD™ Core -->

# Write Walkthrough

---

task:
id: write-walkthrough
name: Write Walkthrough
description: Transform code examples and learning objectives into clear, step-by-step instructional walkthrough (8-15 steps)
persona_default: tutorial-architect
inputs: - code_examples_list (curated code demonstrating progression) - learning_objective (what reader will accomplish) - prerequisites (assumed knowledge) - target_audience (beginner/intermediate/advanced)
steps: - Analyze code examples for natural progression - Identify key concepts and breakpoints for steps - Plan step sequence (8-15 steps typical) - Write setup instructions - Write incremental steps with code inline - Document expected outputs at each step - Add troubleshooting section - Write completion summary - Run quality checklist
output: walkthrough-content.md

---

## Purpose

Create effective step-by-step walkthroughs that guide readers through building something concrete while learning key concepts. Walkthroughs are the instructional core of tutorials and sections—focused, actionable sequences that readers can follow successfully.

## Prerequisites

- Code examples curated and tested (from code-curator)
- Learning objective clearly defined
- Target audience identified
- Understanding of walkthrough vs tutorial vs section scope

## Context: What is a Walkthrough?

A **walkthrough** is a step-by-step instructional sequence (8-15 steps) that:

- Guides readers through building something concrete
- Demonstrates concepts through hands-on practice
- Provides clear instructions at each step
- Documents expected outputs for verification
- Can be embedded in sections or tutorials

**Scope Comparison:**

| Type            | Length          | Scope                        | Context                         |
| --------------- | --------------- | ---------------------------- | ------------------------------- |
| **Walkthrough** | 8-15 steps      | Single concept demonstration | Part of section or tutorial     |
| **Section**     | 2-5 pages       | 1-2 learning objectives      | Part of chapter                 |
| **Tutorial**    | Full standalone | Complete learning experience | Independent or chapter-embedded |

## Workflow Steps

### 1. Analyze Code Examples

Review all provided code examples thoroughly:

**Understand Progression:**

- Review each code file provided
- Understand what each example demonstrates
- Note how examples build from simple to complex
- Identify the "story arc" of the code

**Identify Natural Breakpoints:**

- Where does code introduce new concept?
- Where can reader verify progress?
- Where might reader need explanation?
- Where does complexity increase?

**Map Concepts to Code:**

For each example:

- What concept does this demonstrate?
- What makes this example necessary?
- How does it build on previous examples?
- What prerequisite knowledge does it require?

**Example Analysis:**

```
Code Example 1: basic-list-comp.py
  Concept: Basic list comprehension syntax
  Prerequisites: Python lists, for-loops
  Teaches: [expression for item in iterable]
  Verification: Print output matches expected

Code Example 2: filtering-list-comp.py
  Concept: Adding conditions to filter
  Prerequisites: Example 1, conditional expressions
  Teaches: if clause in comprehensions
  Verification: Filtered results match criteria

Code Example 3: nested-list-comp.py
  Concept: Nested comprehensions
  Prerequisites: Examples 1-2, nested loops
  Teaches: Complex transformations
  Verification: Matrix transformation correct
```

### 2. Plan Step Sequence

Design the walkthrough flow (8-15 steps):

**Determine Logical Order:**

1. **Setup** (Step 1-2): Environment, files, initial code
2. **Foundation** (Step 3-4): Simplest working example
3. **Build** (Step 5-8): Add complexity incrementally
4. **Advanced** (Step 9-12): Realistic usage patterns
5. **Verify** (Step 13-15): Testing and validation

**Each Step Should:**

- Accomplish one clear goal
- Build on previous steps
- Be testable/verifiable
- Take 2-5 minutes to complete
- Teach one specific concept

**Progressive Complexity:**

```
Step 1: Setup Python environment
  Complexity: Minimal
  New concepts: 0

Step 2: Create basic list
  Complexity: Very low
  New concepts: 1 (list creation)

Step 3: Transform with for-loop
  Complexity: Low
  New concepts: 1 (traditional approach)

Step 4: Transform with comprehension
  Complexity: Low-medium
  New concepts: 1 (comprehension syntax)

Step 5: Add filtering condition
  Complexity: Medium
  New concepts: 1 (if clause)

...and so on
```

**Avoid These Patterns:**

❌ Too granular (too many trivial steps):

```
Step 1: Open text editor
Step 2: Create new file
Step 3: Save file as script.py
Step 4: Add first line
Step 5: Add second line
```

❌ Too coarse (steps too large):

```
Step 1: Set up authentication system
Step 2: Test it
```

✅ Good granularity:

```
Step 1: Create User model with fields
Step 2: Add password hashing with bcrypt
Step 3: Create registration endpoint
Step 4: Test user registration
```

**Rule of Thumb:** Each step = 2-5 minutes + teaches one concept

### 3. Write Setup Instructions

Provide clear initialization (typically Step 1-2):

**Environment Setup:**

```markdown
**Step 1: Set Up Your Environment**

Create a project directory and set up your Python environment:

\`\`\`bash
mkdir list-comprehensions
cd list-comprehensions
python3 -m venv venv
source venv/bin/activate # On Windows: venv\\Scripts\\activate
\`\`\`

**What this does:** Creates an isolated Python environment for our examples.

**Verify:** Your terminal prompt should now show `(venv)` indicating the virtual environment is active.
```

**Initial File Structure:**

```markdown
**Step 2: Create Starter Files**

Create a file named `examples.py`:

\`\`\`python

# examples.py

# We'll build list comprehension examples here

# Sample data for our examples

numbers = [1, 2, 3, 4, 5]
names = ['Alice', 'Bob', 'Charlie', 'Diana']

print("Setup complete!")
\`\`\`

**What this does:** Creates our working file with sample data.

**Expected output:** Running `python examples.py` displays:
\`\`\`
Setup complete!
\`\`\`

**Verify:** File exists and runs without errors.
```

**Setup Essentials:**

- Required tools and versions
- Directory structure
- Initial files or starter code
- Dependencies to install
- Configuration if needed

### 4. Write Incremental Steps

Create the core walkthrough steps (typically Step 3-12):

**Standard Step Format:**

```markdown
**Step N: [Action-Oriented Title]**

[Brief introduction: What reader will do in this step]

[Instruction in imperative voice]

\`\`\`language
[Complete, runnable code]
\`\`\`

**What this does:** [Clear explanation of the code's function]

**Why it matters:** [Learning point or concept significance]

**Expected outcome:** [What reader should see when running this]

\`\`\`
[Example output]
\`\`\`

**Verify:** [How to confirm this step worked correctly]
```

**Example - Good Step:**

```markdown
**Step 3: Create Your First List Comprehension**

Let's transform a list using comprehension syntax. Add this code to `examples.py`:

\`\`\`python

# Traditional for-loop approach

doubled_loop = []
for num in numbers:
doubled_loop.append(num \* 2)

# List comprehension approach

doubled_comp = [num * 2 for num in numbers]

print("For-loop result:", doubled_loop)
print("Comprehension result:", doubled_comp)
\`\`\`

**What this does:** Both approaches create a new list with each number doubled. The comprehension version is more concise and expresses the transformation directly.

**Why it matters:** List comprehensions are the Pythonic way to transform data. They're more readable once you understand the syntax and often faster than equivalent for-loops.

**Expected outcome:** Running `python examples.py` displays:
\`\`\`
For-loop result: [2, 4, 6, 8, 10]
Comprehension result: [2, 4, 6, 8, 10]
\`\`\`

**Verify:** Both outputs are identical, showing the comprehension produces the same result as the traditional loop.
```

**Example - Bad Step (too vague):**

```markdown
**Step 3: Use list comprehensions**

Create a list comprehension to transform data.

[No code provided]

You should see the transformed list.
```

**Writing Clear Instructions:**

**Imperative Voice:**

- ✅ "Create a file named `auth.py`"
- ✅ "Add the following code to the User model"
- ✅ "Run the test suite with `pytest`"
- ❌ "You should create a file"
- ❌ "We'll add some code here"

**Specificity:**

- ✅ "Add line 12: `return hashedPassword`"
- ✅ "Create file `models/user.py`"
- ✅ "Set port to 3000"
- ❌ "Modify the code"
- ❌ "Update the configuration"
- ❌ "Add the necessary imports"

**Completeness:**

- Include ALL code needed (no "...")
- Show full context when necessary
- Explicitly state "save the file"
- Don't assume intermediate steps

**Code Integration:**

**Complete and Runnable:**

```python
# Include imports
from typing import List

# Show complete context
def filter_even_numbers(numbers: List[int]) -> List[int]:
    """Filter a list to return only even numbers."""
    return [n for n in numbers if n % 2 == 0]

# Demonstrate usage
if __name__ == "__main__":
    test_numbers = [1, 2, 3, 4, 5, 6]
    result = filter_even_numbers(test_numbers)
    print(f"Even numbers: {result}")
```

**Expected Outputs:**

Always show what happens when code runs:

```markdown
**Running this code:**

\`\`\`python
cities = ['New York', 'London', 'Tokyo', 'Paris']
lengths = [len(city) for city in cities]
print(lengths)
\`\`\`

**Produces:**

\`\`\`
[8, 6, 5, 5]
\`\`\`

Each number represents the character count of the corresponding city name.
```

**What to Explain vs. Assume:**

- **Explain:** New syntax, concepts, patterns being taught
- **Assume:** Prerequisites from your inputs
- **Briefly mention:** Related concepts not central to walkthrough
- **Link for depth:** Point to resources for tangential topics

### 5. Add Troubleshooting Section

Anticipate and address common problems:

**Troubleshooting Format:**

```markdown
## Troubleshooting

**Problem:** [Error message or symptom]

**Symptom:** [What reader sees or experiences]

**Cause:** [Why this happens]

**Solution:** [Step-by-step fix]

**Verification:** [How to confirm it's resolved]
```

**Example - Good Troubleshooting:**

```markdown
## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'bcrypt'`

**Symptom:** Server crashes when accessing `/register` route with error message about missing bcrypt module

**Cause:** The bcrypt package hasn't been installed in your virtual environment

**Solution:**

1. Ensure your virtual environment is activated (you should see `(venv)` in your terminal prompt)
2. Install bcrypt: `pip install bcrypt`
3. Verify installation: `pip list | grep bcrypt` should show bcrypt and its version
4. Restart your server: `python app.py`

**Verification:** The `/register` route should now be accessible without import errors

---

**Problem:** Password visible in database

**Symptom:** When querying the database, you can see the plain text password in the password column

**Cause:** Using `password` field instead of `hashedPassword` when creating the user record

**Solution:**

1. Open `routes/auth.js`
2. Find the `User.create()` call (around line 25)
3. Change `password: password` to `password: hashedPassword`
4. Delete any test users from database
5. Create a new test user through the registration endpoint

**Verification:** Query the database again—the password field should now contain a bcrypt hash (starts with `$2b$`) instead of plain text

---

**Problem:** `User.create is not a function` error

**Symptom:** Error when trying to create a user through the registration endpoint

**Cause:** User model not properly imported or exported

**Solution:**

1. Verify `models/user.js` exports the model:
   \`\`\`javascript
   module.exports = User;
   \`\`\`
2. Verify import in `routes/auth.js`:
   \`\`\`javascript
   const User = require('../models/user');
   \`\`\`
3. Check the path is correct (use `../models/user` not `./models/user` from routes directory)

**Verification:** The error should disappear and user creation should succeed
```

**How Many Issues to Include:**

- **Beginner walkthroughs:** 5-7 common issues
- **Intermediate walkthroughs:** 3-5 issues
- **Advanced walkthroughs:** 2-3 issues

**Focus on:**

- Setup and environment errors
- Common syntax mistakes
- Missing dependencies or imports
- Typos in critical code
- Platform-specific issues (Windows vs Mac/Linux)

### 6. Write Completion Summary

Conclude with accomplishments and next steps:

**What You Accomplished:**

```markdown
## What You Accomplished

Congratulations! You've successfully built a user authentication API with secure password handling. Let's recap what you've learned:

**Core Concepts:**

- Password hashing with bcrypt for security
- RESTful API endpoint design for authentication
- Express.js route handling and middleware
- Database integration with Sequelize ORM
- Environment variable management with dotenv

**Skills Practiced:**

- Creating user models with validation
- Implementing secure password storage
- Building registration and login endpoints
- JWT token generation and verification
- Error handling in Express routes
- Testing APIs with curl/Postman

**What You Built:**
You now have a working authentication system that:

- Accepts user registration with email/password
- Hashes passwords securely using bcrypt
- Stores user data in a database
- Generates JWT tokens for authenticated sessions
- Validates credentials on login
- Returns appropriate error messages

This foundation is production-ready and follows security best practices used in professional applications.
```

**Next Steps:**

```markdown
## Next Steps

**Immediate Extensions:**

- Add email verification for new accounts
- Implement password reset functionality
- Add rate limiting to prevent brute-force attacks
- Create refresh token mechanism for longer sessions

**Related Concepts to Explore:**

- OAuth2 integration for social login (Google, GitHub)
- Role-based access control (RBAC)
- Multi-factor authentication (MFA)
- Session management strategies

**Recommended Tutorials:**

- Tutorial 5: Implementing Password Reset Workflows
- Tutorial 7: Adding OAuth2 Social Authentication
- Tutorial 9: Role-Based Access Control

**Extension Challenges:**
Try implementing these features independently to reinforce your learning:

1. **Email Confirmation:** Send a confirmation email with a verification token when users register
2. **Account Lockout:** Lock accounts after 5 failed login attempts for security
3. **Password Strength Validation:** Require minimum complexity (uppercase, numbers, special chars)
4. **Remember Me:** Add optional long-lived tokens for "remember me" functionality
```

**Tone:**

- Celebratory (acknowledge accomplishment)
- Encouraging (build confidence)
- Forward-looking (what's next)
- Practical (how to apply learning)

### 7. Quality Checklist

Before finalizing, verify walkthrough quality:

**Content Quality:**

- [ ] Every step has clear action verb (Create, Add, Run, etc.)
- [ ] Code examples are complete (no `...` placeholders)
- [ ] All code has been tested and runs successfully
- [ ] Expected outputs documented for every code example
- [ ] Verification methods provided for each step
- [ ] Progressive difficulty (no sudden jumps)
- [ ] No assumed steps (all actions explicit)
- [ ] 8-15 steps (not too few, not too many)

**Instructional Quality:**

- [ ] Imperative voice used consistently
- [ ] Specific filenames, line numbers, values provided
- [ ] Clear explanations of what code does
- [ ] Clear explanations of why it matters
- [ ] Real-world context provided
- [ ] Common mistakes addressed
- [ ] Prerequisites stated explicitly

**Technical Quality:**

- [ ] All imports included
- [ ] Complete code context shown
- [ ] Platform-specific instructions noted (Windows vs Mac/Linux)
- [ ] Dependencies listed with versions
- [ ] Configuration requirements specified
- [ ] Error handling demonstrated

**Troubleshooting Quality:**

- [ ] 3-7 common issues documented
- [ ] Problem/Symptom/Cause/Solution format used
- [ ] Step-by-step solutions provided
- [ ] Verification methods for fixes
- [ ] Covers setup, environment, syntax errors

**Completion Quality:**

- [ ] Learning objectives summarized
- [ ] Skills practiced listed
- [ ] Concrete deliverable described
- [ ] Next steps provided
- [ ] Extension challenges offered
- [ ] Related resources linked

## Output

Complete walkthrough should include:

```markdown
# [Walkthrough Title]

## Prerequisites

- [List of assumed knowledge]
- [Software/tools required]
- [Estimated completion time]

## What You'll Build

[Brief description of the deliverable]

## Setup

**Step 1-2:** Environment and initial files

## Walkthrough

**Step 3-12:** Incremental build steps with:

- Action-oriented title
- Clear instructions (imperative voice)
- Complete, runnable code
- Explanation (what this does)
- Rationale (why it matters)
- Expected output
- Verification method

## Troubleshooting

**3-7 common issues** with:

- Problem/Symptom/Cause/Solution/Verification

## What You Accomplished

- Key concepts learned
- Skills practiced
- What you built

## Next Steps

- Immediate extensions
- Related concepts
- Recommended tutorials
- Extension challenges
```

## Quality Standards

An effective walkthrough:

✓ **Clear and Actionable:**

- Every step has specific, imperative instructions
- No ambiguity about what to do
- Complete code provided
- All necessary context included

✓ **Pedagogically Sound:**

- Progressive difficulty maintained
- One concept per step when possible
- Concepts explained before application
- Learning reinforced through practice

✓ **Technically Accurate:**

- All code tested and working
- Outputs match documentation
- Best practices demonstrated
- Common mistakes addressed

✓ **Reader-Friendly:**

- Encouraging, supportive tone
- Success verification at each step
- Troubleshooting readily available
- Clear accomplishment markers

## Common Pitfalls

Avoid:

❌ **Vague instructions** - "Modify the code" → "Add line 15: `const PORT = 3000;`"

❌ **Incomplete code** - Using `...` placeholders → Show complete, runnable code

❌ **Missing outputs** - Not showing what readers should see → Always document expected output

❌ **Assumed steps** - "Set up the database" → Explicit step-by-step database setup

❌ **No verification** - Readers can't tell if it worked → Provide verification method for each step

❌ **Difficulty jumps** - Going from simple to complex too quickly → Gradual progression

❌ **Too long** - More than 15 steps → Consider splitting into multiple walkthroughs

❌ **Too short** - Fewer than 8 steps → May lack necessary detail or be too simplistic

❌ **No troubleshooting** - Assuming everything will work → Anticipate and address common issues

❌ **No context** - Just code without explanation → Explain what, why, and how

## Example: Good Walkthrough Structure

```markdown
# Build a User Authentication API

## Prerequisites

- Node.js 18+ installed
- Basic understanding of Express.js
- Familiarity with REST API concepts
- 45-60 minutes

## What You'll Build

A secure user authentication system with registration, login, and JWT-based sessions using Express.js, bcrypt, and PostgreSQL.

**Step 1: Set Up Project Structure**

Create your project directory and initialize Node.js:

\`\`\`bash
mkdir auth-api
cd auth-api
npm init -y
npm install express bcrypt jsonwebtoken pg dotenv
\`\`\`

**What this does:** Initializes a Node.js project and installs necessary dependencies for authentication.

**Verify:** Check `package.json` includes express, bcrypt, jsonwebtoken, pg, and dotenv in dependencies.

---

**Step 2: Create Environment Configuration**

Create a `.env` file in your project root:

\`\`\`
DATABASE_URL=postgresql://localhost:5432/auth_db
JWT_SECRET=your-secret-key-change-this-in-production
PORT=3000
\`\`\`

**What this does:** Stores sensitive configuration outside your code for security.

**Why it matters:** Never hardcode secrets in source code. Environment variables keep configuration separate and secure.

**Verify:** File created with all three variables defined.

---

[Continue with steps 3-15...]

---

## Troubleshooting

**Problem:** `Error: connect ECONNREFUSED 127.0.0.1:5432`
**Symptom:** Application crashes when trying to connect to database
**Cause:** PostgreSQL is not running
**Solution:**

1. Start PostgreSQL: `brew services start postgresql` (Mac) or `sudo service postgresql start` (Linux)
2. Verify it's running: `psql --version`
3. Restart your application
   **Verification:** Application starts without connection errors

---

## What You Accomplished

You built a production-ready authentication API with secure password hashing, JWT tokens, and database persistence. You learned:

- Password hashing with bcrypt
- JWT token generation and validation
- Express.js route handling
- Database integration with PostgreSQL
- Environment variable management

## Next Steps

**Extensions:**

- Add email verification for new users
- Implement password reset workflow
- Add refresh token mechanism
- Create user profile endpoints

**Related Tutorials:**

- Tutorial 6: Adding OAuth2 Social Login
- Tutorial 8: Role-Based Access Control
```

## Integration with Tutorial-Architect

This task integrates with the tutorial-architect agent's `*write-walkthrough` command:

**Usage Pattern:**

```
User: *write-walkthrough

Tutorial-Architect loads this task and:
1. Requests code examples (from code-curator or user)
2. Asks for learning objective
3. Clarifies prerequisites
4. Identifies target audience
5. Executes walkthrough creation workflow
6. Outputs walkthrough-content.md
```

**Output Integration:**

The generated `walkthrough-content.md` can be:

- Embedded in a section (via write-section-draft.md)
- Included in a tutorial (via develop-tutorial.md)
- Used standalone as a quick-start guide
- Referenced in multiple chapters

## Related Resources

- **Task:** develop-tutorial.md - Full tutorial creation including walkthroughs
- **Task:** write-section-draft.md - Section writing that may embed walkthroughs
- **Template:** tutorial-section-tmpl.yaml - Structure for tutorial sections
- **Checklist:** tutorial-effectiveness-checklist.md - Quality validation
- **Data:** learning-frameworks.md - Pedagogical theory

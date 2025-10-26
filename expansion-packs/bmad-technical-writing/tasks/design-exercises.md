<!-- Powered by BMAD™ Core -->

# Design Exercises

---

task:
id: design-exercises
name: Design Exercises
description: Create practice exercises with progressive difficulty, hints, and solution approaches
persona_default: instructional-designer
inputs:

- chapter-number
- learning-objectives
- difficulty-range
  steps:
- Identify learning objectives to assess
- Determine appropriate difficulty levels (basic to advanced)
- Create 4-6 exercises per chapter with progressive difficulty
- Progress from basic application to challenging problems
- Write clear instructions for each exercise
- Develop solution approaches (not full solutions)
- Add progressive hints for learners
- Create extension challenges for advanced students
- Estimate completion time for each exercise
- Validate exercises are solvable and appropriate
- Run execute-checklist.md with exercise-difficulty-checklist.md
- Use template exercise-set-tmpl.yaml with create-doc.md
  output: exercises/chapter-{{chapter_number}}-exercises.md

---

## Purpose

Create practice exercises that reinforce learning, assess comprehension, and build confidence through progressive difficulty. Effective exercises bridge theory and independent application.

## Prerequisites

- Chapter learning objectives defined
- Chapter content drafted or outlined
- Understanding of target audience skill level
- Access to learning-frameworks.md knowledge base

## Workflow Steps

### 1. Identify Learning Objectives to Assess

Map exercises to specific learning goals:

**For Each Learning Objective:**

- Which exercises will assess this?
- What demonstrates mastery?
- How can students practice this skill?

**Example Mapping:**

```
Objective: "Implement JWT authentication"
→ Exercise 2: Build login endpoint (basic)
→ Exercise 4: Add token refresh (intermediate)
→ Exercise 6: Implement role-based access (advanced)
```

**Coverage:**

- Each objective addressed by at least one exercise
- Core objectives get multiple exercises
- Progressive difficulty across related exercises

### 2. Determine Difficulty Levels

Plan difficulty range appropriate for chapter:

**Basic (⭐):**

- Direct application of chapter examples
- Clear guidance and hints
- Builds confidence
- 2-3 exercises per chapter

**Intermediate (⭐⭐):**

- Combines multiple concepts
- Requires problem-solving
- Less hand-holding
- 1-2 exercises per chapter

**Advanced (⭐⭐⭐):**

- Creative application
- Minimal guidance
- Extension of concepts
- 1 exercise per chapter (optional)

**Balance:** Most students should complete basic and intermediate exercises successfully.

### 3. Create 4-6 Exercises with Progressive Difficulty

Design exercise sequence:

**Exercise Structure:**

**Exercise Header:**

- Number and title
- Difficulty indicator (⭐ ⭐⭐ ⭐⭐⭐)
- Estimated time
- Learning objective addressed

**Problem Description:**

- Clear problem statement
- Specific requirements (numbered list)
- Input/output examples
- Success criteria

**Example:**

````
### Exercise 3: User Input Validation ⭐⭐
**Estimated Time:** 20 minutes
**Learning Objective:** Apply regex for validation

**Problem:**
Create a `validate_user_input()` function that validates user registration data:

Requirements:
1. Username: 3-20 characters, alphanumeric only
2. Email: Valid email format
3. Password: Minimum 8 characters, must include number and special character
4. Return dict with validation results for each field

**Test Cases:**
```python
validate_user_input("user123", "user@example.com", "Pass123!")
# Returns: {"username": True, "email": True, "password": True, "valid": True}

validate_user_input("ab", "invalid", "weak")
# Returns: {"username": False, "email": False, "password": False, "valid": False}
````

**Success Criteria:**

- All test cases pass
- Clear error messages for invalid inputs
- Uses regex for email validation

````

### 4. Write Clear Instructions

Make requirements explicit and unambiguous:

**Good Exercise Instructions:**
- State exact functionality needed
- Provide function signature or class structure
- List all requirements as numbered points
- Include test cases with expected results
- Specify any constraints

**Avoid:**
- Vague requirements ("make it work better")
- Ambiguous success criteria
- Assuming implied requirements
- Unclear edge cases

**Starter Code (for basic exercises):**
```python
def validate_user_input(username, email, password):
    """
    Validate user registration inputs.

    Args:
        username (str): Username to validate
        email (str): Email address to validate
        password (str): Password to validate

    Returns:
        dict: Validation results for each field and overall validity
    """
    # Your code here
    pass
````

### 5. Develop Solution Approaches

Provide guidance without giving away the answer:

**Solution Approach (Not Full Code):**

- High-level algorithm
- Key concepts to apply
- Recommended data structures
- Common pitfalls to avoid

**Example:**

```
**Solution Approach:**
1. Create validation functions for each field type
2. Use regex pattern for email: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
3. For password, check length first, then regex for number and special char
4. Return dictionary with results for each field
5. Set `valid` to True only if all fields pass

**Key Concepts:**
- Python `re` module for regex matching
- `re.match()` vs `re.fullmatch()` - use fullmatch for exact pattern matching
- Combining multiple validation conditions

**Common Pitfalls:**
- Forgetting to anchor regex with ^ and $
- Not handling empty string inputs
- Allowing spaces in username
```

**Balance:** Enough guidance to unstick students, not so much they don't think.

### 6. Add Progressive Hints

Create hints that reveal information gradually:

**Hint Structure:**

- Hint 1: General approach or concept
- Hint 2: More specific technique
- Hint 3: Nearly complete solution approach

**Example:**

```
**Hints:**
1. Break the problem into three separate validation functions
2. Use Python's `re` module - import with `import re`
3. For password validation, you can use multiple regex patterns:
   - `re.search(r'\d', password)` to check for digit
   - `re.search(r'[!@#$%^&*]', password)` for special char
```

**Good Hints:**

- Guide thinking, don't solve the problem
- Progressive reveal (start general)
- Specific to common sticking points
- Teach concepts, not just answer

### 7. Create Extension Challenges

Add optional advanced problems:

**Extension Characteristics:**

- Builds on basic exercise
- Requires creative thinking
- No hints provided
- Tests deeper mastery

**Example Extensions:**

````
**Extension Challenges:**

**Challenge 1: Password Strength Meter**
Enhance the password validator to return a strength score (1-5) based on:
- Length (longer = stronger)
- Character variety (lowercase, uppercase, numbers, special chars)
- Common password detection

**Challenge 2: Custom Validation Rules**
Allow configuration of validation rules via a config object:
```python
rules = {
    "username": {"min": 3, "max": 20, "pattern": r"^[a-z0-9_]+$"},
    "password": {"min": 12, "require_special": True, "require_number": True}
}
validate_with_rules(data, rules)
````

```

**Purpose:** Challenges extend learning for students who want more practice.

### 8. Estimate Completion Time

Provide realistic time estimates:

**Factors:**
- Problem complexity
- Amount of code to write
- Testing and debugging time
- Student skill level

**Basic Exercise:** 10-20 minutes
**Intermediate:** 20-40 minutes
**Advanced:** 40-90 minutes

**Test Your Estimate:**
- Time yourself solving it
- Add 50-100% for students (you're expert)
- Test with actual students if possible

**State in Exercise:**
```

**Estimated Time:** 25 minutes

This includes:

- Understanding requirements: 5 min
- Implementation: 15 min
- Testing: 5 min

```

### 9. Validate Exercises Are Solvable

Quality check all exercises:

**Self-Solve:**
- Solve each exercise yourself without looking at hints
- Note any ambiguities or unclear requirements
- Verify time estimate is reasonable
- Ensure you only use concepts from the chapter

**Peer Review:**
- Have colleague attempt exercises
- Observe where they get stuck
- Note questions they ask
- Improve instructions based on feedback

**Verification:**
- All test cases provided are correct
- Multiple valid solutions exist (usually)
- Success criteria are measurable
- Difficulty matches rating

**Use:** exercise-difficulty-checklist.md

### 10. Run Quality Checklist

Final validation:

**Execute:** exercise-difficulty-checklist.md

**Check:**
- Progressive difficulty across exercises
- Each learning objective assessed
- Clear, unambiguous instructions
- Appropriate hints provided
- Time estimates realistic
- Exercises solvable with chapter knowledge
- No prerequisites beyond chapter scope

## Output

Exercise set should include:

- 4-6 exercises with progressive difficulty
- Clear problem statements
- Test cases and success criteria
- Progressive hints
- Solution approaches
- Extension challenges
- Estimated completion times
- Self-assessment checklist

**Use template:** exercise-set-tmpl.yaml

## Quality Standards

Effective exercise set:

✓ Maps to chapter learning objectives
✓ Progressive difficulty (⭐ to ⭐⭐⭐)
✓ Clear, specific requirements
✓ Realistic time estimates
✓ Helpful hints without giving away answers
✓ Solvable with chapter knowledge
✓ Engaging and relevant problems
✓ Extension challenges for advanced learners

## Common Pitfalls

Avoid:

❌ All exercises same difficulty
❌ Vague or ambiguous requirements
❌ Requiring knowledge beyond chapter
❌ Trivial exercises (too easy)
❌ Impossible exercises (too hard)
❌ No hints or scaffolding
❌ Unrealistic time estimates
❌ Boring or contrived problems

## Next Steps

After designing exercises:

1. Include in chapter draft
2. Create solution code (for answer key)
3. Test with beta readers if possible
4. Iterate based on feedback
5. Update hints if students commonly stuck
6. Consider creating video solutions for complex exercises
```

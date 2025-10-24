<!-- Powered by BMAD™ Core -->

# Check Code Best Practices

---

task:
id: check-best-practices
name: Check Code Best Practices
description: Comprehensive code quality and best practices review. Validates style guide compliance, design patterns, error handling, security, naming conventions, and educational value. Integrates automated linting with manual review.
persona_default: technical-reviewer
inputs: - code_path - language - style_guide
steps: - Identify all code examples and language(s) used - Set up linting tools for each language - Run automated linting and capture results - Review style guide compliance manually - Check naming conventions and code structure - Validate error handling completeness - Review design pattern usage - Check comments and documentation quality - Assess DRY principle adherence - Evaluate security best practices - Check educational value and clarity - Run execute-checklist.md with code-quality-checklist.md - Compile best practices review report - Use template best-practices-report-tmpl.yaml with create-doc.md
output: reviews/validation-results/best-practices-review-{{timestamp}}.md

---

## Purpose

This task performs comprehensive code quality review to ensure all code examples follow language-specific best practices, use appropriate design patterns, handle errors properly, and provide educational value. It combines automated linting with manual expert review.

## Prerequisites

- Code examples to review
- Language(s) and versions specified
- Style guide reference (PEP 8, Airbnb JS, Google Java, etc.)
- Linting tools installed for target languages
- Access to code-quality-checklist.md
- Understanding of language-specific best practices

## Workflow Steps

### 1. Identify Code Examples and Languages

Catalog all code to review:

**For Each Code Example:**

- Example number/identifier
- Location (chapter, section, page)
- Language and version
- Size (lines of code)
- Purpose (what concept it demonstrates)
- Applicable style guide

**Create Code Inventory:**

```
Example 3.1 (Chapter 3, Section 1)
Language: JavaScript (ES6+)
Size: 25 lines
Purpose: Demonstrate async/await with error handling
Style Guide: Airbnb JavaScript Style Guide
```

### 2. Set Up Linting Tools

Configure automated linting for each language:

**JavaScript/TypeScript:**

```bash
npm install eslint
npx eslint --init
# Configure for appropriate style guide (Airbnb, Standard, etc.)
```

**Python:**

```bash
pip install pylint black flake8
# Or use ruff for combined linting/formatting
```

**Java:**

```bash
# Use Checkstyle, PMD, or SpotBugs
```

**Go:**

```bash
# Use golint, go vet, staticcheck
```

**Configure Linters:**

- Set language version
- Enable style guide rules
- Configure ignore patterns (if teaching bad practices intentionally)
- Set severity levels

### 3. Run Automated Linting

Execute linters on all code:

**For Each Code Example:**

Run linting tool:

```bash
# JavaScript
eslint example3-1.js

# Python
pylint example5-2.py
flake8 example5-2.py

# Java
checkstyle example7-3.java
```

**Capture Results:**

- Errors (must fix)
- Warnings (should review)
- Info (suggestions)
- Style violations
- Complexity metrics

**Document Linting Results:**

```
Example 3.1: Async/Await Error Handling
Linter: ESLint (Airbnb config)
Errors: 0
Warnings: 2
  - Line 5: Unexpected console statement (no-console)
  - Line 12: 'error' is never reassigned. Use 'const' instead (prefer-const)
Info: 1
  - Line 8: Function has complexity of 6 (max 5)
```

### 4. Review Style Guide Compliance

Manual review beyond automated linting:

**Language-Specific Style Guides:**

**JavaScript:**

- Airbnb JavaScript Style Guide
- Google JavaScript Style Guide
- StandardJS

**Python:**

- PEP 8 (official style guide)
- Black (opinionated formatter)
- Google Python Style Guide

**Java:**

- Google Java Style Guide
- Oracle Java Code Conventions

**Go:**

- Effective Go (official)
- Go Code Review Comments

**Check:**

**Indentation and Formatting:**

- Consistent spacing (tabs vs spaces)
- Line length within limits
- Bracket placement consistent
- Blank lines used appropriately

**Naming Conventions:**

- camelCase vs snake_case per language
- Constants in UPPER_CASE
- Private members prefixed appropriately
- Descriptive names, not abbreviations

**Code Organization:**

- Logical grouping of related code
- Consistent ordering (imports, constants, functions)
- Appropriate file/module structure

**Document Style Violations:**

```
Example 5.3: Database Query
Severity: Minor
Issue: Line length exceeds 80 characters (PEP 8 guideline)
Line 15: query = "SELECT users.id, users.name, users.email, users.created_at, users.updated_at FROM users WHERE ..."
Recommendation: Break into multiple lines or use triple-quoted string
```

### 5. Check Naming Conventions

Evaluate variable, function, and class names:

**Good Naming Principles:**

**Variables:**

- Descriptive, not cryptic
- Appropriate length (not too short, not too verbose)
- Boolean variables suggest true/false (isValid, hasPermission)

❌ **Bad Examples:**

```python
x = get_data()  # What is x?
temp = process(temp)  # Ambiguous
flag = True  # Flag for what?
```

✓ **Good Examples:**

```python
user_profile = get_data()
sanitized_input = process(raw_input)
is_authenticated = True
```

**Functions/Methods:**

- Verb-based names (get, set, calculate, validate)
- Clear indication of what they do
- Consistent naming patterns

❌ **Bad Examples:**

```javascript
function data() {} // Ambiguous
function process() {} // Process what?
function doIt() {} // Do what?
```

✓ **Good Examples:**

```javascript
function fetchUserProfile() {}
function validateEmail() {}
function calculateTotalPrice() {}
```

**Classes:**

- Noun-based names
- PascalCase (most languages)
- Descriptive of what they represent

**Constants:**

- UPPER_SNAKE_CASE (most languages)
- Clear indication of purpose

**Check for Exceptions:**

- Loop counters (i, j, k acceptable)
- Lambda parameters (x, y acceptable for math)
- Very limited scope variables

**Document Naming Issues:**

```
Example 7.2: Data Processing
Severity: Major
Issue: Poor variable names throughout
Lines with issues:
  - Line 3: let d = new Date()  →  let currentDate = new Date()
  - Line 5: function proc(x)  →  function processTransaction(transaction)
  - Line 12: const tmp = ...  →  const normalizedData = ...
Impact: Code is harder to understand and teach
```

### 6. Validate Error Handling

Check error handling completeness:

**Error Handling Checklist:**

**Try-Catch Blocks:**

- Are potential errors caught?
- Are catch blocks meaningful (not empty)?
- Are errors logged or reported?
- Is cleanup performed (finally blocks)?

**Error Messages:**

- Are error messages descriptive?
- Do they help debug the issue?
- Do they avoid leaking sensitive info?

**Error Propagation:**

- Are errors re-thrown when appropriate?
- Are custom errors used where helpful?
- Is the call stack preserved?

**Defensive Programming:**

- Input validation present?
- Null/undefined checks where needed?
- Boundary conditions handled?

**Common Error Handling Issues:**

❌ **Empty Catch Block:**

```javascript
try {
  riskyOperation();
} catch (e) {
  // Silent failure - bad!
}
```

✓ **Proper Error Handling:**

```javascript
try {
  riskyOperation();
} catch (error) {
  console.error('Operation failed:', error.message);
  // Optionally re-throw or return error state
  throw error;
}
```

❌ **Generic Error Messages:**

```python
except Exception:
    print("Error")  # Uninformative
```

✓ **Descriptive Error Messages:**

```python
except FileNotFoundError as e:
    print(f"Could not find config file at {config_path}: {e}")
except PermissionError as e:
    print(f"Permission denied when reading {config_path}: {e}")
```

**Document Error Handling Issues:**

````
Example 4.5: File Processing
Severity: Major
Issue: No error handling for file operations
Lines 8-12: File open and read operations without try-catch
Risk: Code will crash with unhelpful error if file doesn't exist
Recommendation: Wrap file operations in try-catch with specific error handling:
```python
try:
    with open(file_path, 'r') as f:
        content = f.read()
except FileNotFoundError:
    print(f"File not found: {file_path}")
    return None
except PermissionError:
    print(f"Permission denied: {file_path}")
    return None
````

```

### 7. Review Design Pattern Usage

Assess appropriateness of patterns used:

**Common Design Patterns:**

**Creational:**
- Singleton
- Factory
- Builder

**Structural:**
- Adapter
- Decorator
- Facade

**Behavioral:**
- Observer
- Strategy
- Command

**Check:**

**Pattern Appropriateness:**
- Is the pattern suitable for the problem?
- Is it implemented correctly?
- Is it over-engineering for educational context?

**Anti-Patterns to Flag:**
- God objects (classes doing too much)
- Spaghetti code (tangled logic)
- Magic numbers (hardcoded values without explanation)
- Cargo cult programming (using patterns without understanding)

**Educational Consideration:**
- Is the pattern helping or hindering learning?
- Is it introduced at appropriate level?
- Is it explained adequately?

**Document Pattern Issues:**

```

Example 9.3: User Management
Severity: Minor
Issue: Overly complex Singleton pattern for simple use case
The example uses a full Singleton pattern (private constructor, getInstance method)
for a configuration object that could be a simple module export.

Recommendation: For teaching purposes, start with simpler module pattern:

```javascript
// Simple and clear for beginners
export const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
};
```

Reserve Singleton pattern for chapter on design patterns where complexity is justified.

````

### 8. Check Comments and Documentation

Evaluate comment quality and usefulness:

**Good Comments:**

**Explain WHY, not WHAT:**
```javascript
// Use exponential backoff to avoid overwhelming the API during retries
const delay = Math.pow(2, attemptNumber) * 1000
````

**Explain Complex Logic:**

```python
# Dijkstra's algorithm requires a priority queue
# We use heapq because it provides O(log n) operations
```

**Document Non-Obvious Decisions:**

```java
// Using StringBuilder instead of + operator
// for better performance in loop (avoids creating intermediate strings)
```

**Bad Comments:**

❌ **Obvious Comments:**

```javascript
// Increment i
i++;
```

❌ **Commented-Out Code:**

```python
# old_function()
# previous_approach()
new_function()
```

❌ **Misleading Comments:**

```javascript
// Calculate total price
const result = calculateTax(); // Comment doesn't match code
```

**Check:**

- Comments explain WHY, not WHAT
- Complex sections are explained
- No commented-out code
- Comments are current (not outdated)
- Appropriate level of detail for audience

**Document Comment Issues:**

```
Example 6.4: Algorithm Implementation
Severity: Minor
Issue: Insufficient comments for complex algorithm
Lines 15-30: Implements A* pathfinding without explanation
Recommendation: Add comments explaining:
  - What algorithm is being used
  - Why certain data structures are chosen (priority queue, set for visited)
  - Key steps in the algorithm
Educational note: Complex algorithms especially need good comments for teaching
```

### 9. Assess DRY Principle Adherence

Check for code duplication:

**DRY (Don't Repeat Yourself) Principle:**

**Look for:**

- Duplicated code blocks
- Similar logic in multiple places
- Copy-paste patterns

**Balance with Teaching:**

- Sometimes repetition aids learning
- Early examples may intentionally show duplication before refactoring
- Context matters

**Check:**

❌ **Unnecessary Duplication:**

```javascript
// Example shows same validation three times
if (email.includes('@')) { ... }
// Later...
if (email.includes('@')) { ... }
// Later again...
if (email.includes('@')) { ... }
```

✓ **Better Approach:**

```javascript
function isValidEmail(email) {
  return email.includes('@')
}

if (isValidEmail(email)) { ... }
```

✓ **Acceptable Duplication for Teaching:**

```javascript
// Chapter 2: Showing the problem (before refactoring)
calculatePriceWithTax(...)  // Duplicated logic
calculatePriceWithDiscount(...)  // Duplicated logic

// Chapter 3: Teaching the solution
calculatePrice(options)  // Refactored DRY version
```

**Document DRY Issues:**

````
Example 8.2: Form Validation
Severity: Major
Issue: Validation logic duplicated across 4 input handlers
Lines 10-15, 20-25, 30-35, 40-45: Nearly identical validation code
Recommendation: Extract to shared validation function:
```javascript
function validateInput(input, rules) {
  // Centralized validation logic
}

// Then use in all handlers
emailInput.addEventListener('input', () => validateInput(email, emailRules))
passwordInput.addEventListener('input', () => validateInput(password, passwordRules))
````

Educational value: Good opportunity to teach DRY principle

````

### 10. Evaluate Security Best Practices

Check for security issues in code:

**Common Security Issues in Technical Books:**

**Hardcoded Credentials:**
```javascript
// ❌ NEVER in production or teaching material:
const API_KEY = 'sk_live_51H...'
const DB_PASSWORD = 'mypassword123'

// ✓ Use environment variables or placeholders:
const API_KEY = process.env.API_KEY
const DB_PASSWORD = process.env.DB_PASSWORD
````

**SQL Injection:**

```python
# ❌ Vulnerable to SQL injection:
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✓ Use parameterized queries:
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

**XSS (Cross-Site Scripting):**

```javascript
// ❌ Vulnerable to XSS:
element.innerHTML = userInput;

// ✓ Use textContent or sanitize:
element.textContent = userInput;
// Or use a sanitization library
```

**Insecure Authentication:**

```python
# ❌ Storing passwords in plaintext:
user.password = password

# ✓ Hash passwords:
user.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**Check:**

- No hardcoded secrets
- Input validation present
- Parameterized queries for SQL
- Proper password hashing (bcrypt, Argon2)
- HTTPS/TLS mentioned for production
- Security warnings where needed

**Document Security Issues:**

````
Example 10.3: User Authentication
Severity: CRITICAL
Issue: Password stored in plaintext
Line 45: user.password = password
This is a severe security vulnerability that must never be done in production

Recommended Fix:
```python
import bcrypt

# Hash password before storing
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
user.password_hash = password_hash
````

Add Security Note: "IMPORTANT: Never store passwords in plaintext. Always use a
secure hashing algorithm like bcrypt or Argon2."

````

### 11. Check Educational Value

Evaluate if code serves its teaching purpose:

**Educational Code Qualities:**

**Clarity Over Cleverness:**
```javascript
// ❌ Clever but hard to understand for learners:
const result = arr.reduce((a, c) => ({...a, [c.id]: c}), {})

// ✓ Clear and educational:
const result = {}
for (const item of arr) {
  result[item.id] = item
}
// Later chapter can show reduce version as optimization
````

**Appropriate Complexity:**

- Not too simple (trivial examples waste time)
- Not too complex (overwhelming)
- Focused on one concept at a time

**Realistic but Simplified:**

- Resembles real-world code
- Simplified for learning (omit irrelevant details)
- Production-ready patterns when appropriate

**Progressive Enhancement:**

- Early chapters show simple approaches
- Later chapters show advanced techniques
- Clear progression of sophistication

**Check:**

- Code is readable by target audience
- Focuses on concept being taught
- Doesn't introduce too many concepts simultaneously
- Provides good foundation for building upon

**Document Educational Issues:**

```
Example 3.7: Array Manipulation
Severity: Major
Issue: Example too complex for introductory chapter
Combines map, filter, reduce, and destructuring in single example
This is Chapter 3 (JavaScript Basics) - readers don't know these concepts yet

Recommendation: Break into multiple examples:
  - Example 3.7a: Just map (transform array)
  - Example 3.7b: Just filter (select items)
  - Save reduce for Chapter 5 (Advanced Arrays)

Educational principle: One new concept per example at beginner level
```

### 12. Run Code Quality Checklist

Execute systematic checklist:

**Run:** `execute-checklist.md` with `code-quality-checklist.md`

**Verify:**

- Style guide compliance
- Naming conventions
- Comments appropriate
- Code structure logical
- Error handling complete
- Best practices followed
- Security considerations
- Educational value high

**Document** any checklist items that fail.

### 13. Compile Best Practices Review Report

Create structured review report:

**Report Structure:**

#### Executive Summary

- Overall code quality assessment (Pass/Fail/Needs Revision)
- Critical issues count (security, broken patterns)
- Major issues count (style violations, poor practices)
- Minor issues count (suggestions, optimizations)
- Overall recommendation

#### Automated Linting Results

- Linters used per language
- Total errors/warnings/info per example
- Common patterns in linting results

#### Style Guide Compliance

- Style guide(s) applied
- Compliance percentage
- Common violations found

#### Naming Conventions

- Quality of variable names
- Function naming patterns
- Consistency across examples

#### Error Handling Assessment

- Coverage of error handling
- Quality of error messages
- Missing error handling locations

#### Design Patterns Review

- Patterns identified
- Appropriateness assessment
- Anti-patterns found

#### Security Review

- Security issues found (critical priority)
- Best practices compliance
- Recommendations

#### Educational Value Assessment

- Clarity for target audience
- Complexity appropriateness
- Teaching effectiveness

#### Checklist Results

- Code quality checklist pass/fail items

#### Recommendations

- Prioritized by severity
- Specific code improvements
- Educational enhancements

**Severity Definitions:**

- **Critical:** Security vulnerabilities, dangerous practices
- **Major:** Best practice violations, significant quality issues
- **Minor:** Style improvements, optimizations, suggestions

**Pass/Fail Thresholds:**

- **Pass:** 0 critical, ≤ 3 major, minor acceptable
- **Needs Revision:** 0 critical, 4-7 major
- **Fail:** Any critical OR > 7 major

## Output

Best practices review report should include:

- Overall quality assessment
- Automated linting results
- Manual review findings
- Security issues (if any)
- Educational value assessment
- Checklist results
- Prioritized recommendations with examples

**Save to:** `reviews/validation-results/best-practices-review-{{timestamp}}.md`

## Quality Standards

Effective best practices review:

✓ Runs automated linting for all languages
✓ Reviews style guide compliance thoroughly
✓ Identifies all security issues
✓ Assesses educational value
✓ Provides specific, actionable fixes
✓ Includes corrected code examples
✓ Prioritizes by severity
✓ Balances production best practices with teaching clarity

## Next Steps

After review:

1. Deliver review report to author
2. Author addresses critical issues (must fix)
3. Author addresses major issues (should fix)
4. Re-lint code after fixes
5. Approve for next review phase

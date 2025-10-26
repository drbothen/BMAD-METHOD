<!-- Powered by BMAD™ Core -->

# Verify Technical Accuracy

---

task:
id: verify-accuracy
name: Verify Technical Accuracy
description: Comprehensive technical accuracy verification with fact-checking, code validation, API correctness, and source verification. Ensures all technical claims are correct, current, and verifiable.
persona_default: technical-reviewer
inputs:
  - content_path
  - code_examples_path
  - reference_docs
steps:
  - Read content completely for technical claims
  - Identify all technical statements requiring verification
  - Verify technical statements against authoritative sources
  - Test all code examples for correctness
  - Check API and library usage against current documentation
  - Validate diagrams match descriptions
  - Cross-check terminology consistency
  - Identify outdated or deprecated information
  - Run execute-checklist.md with technical-accuracy-checklist.md
  - Compile verification report with severity ratings
  - Use template accuracy-verification-report-tmpl.yaml with create-doc.md
output: reviews/validation-results/accuracy-verification-{{timestamp}}.md

---

## Purpose

This task performs rigorous technical accuracy verification to ensure all content is factually correct, uses current best practices, and can be verified against authoritative sources. It catches technical errors, outdated information, and incorrect API usage before publication.

## Prerequisites

- Chapter draft or content to review
- Access to official documentation for technologies covered
- Code testing environment
- Subject matter expertise in content domain
- Access to technical-accuracy-checklist.md
- Familiarity with version-specific features

## Workflow Steps

### 1. Read Content Completely

Gain full context before detailed review:

- Read entire content without stopping
- Understand the scope of technologies covered
- Note version numbers mentioned
- Identify all code examples
- List all technical claims to verify

**Purpose:** Understand context and identify verification targets.

### 2. Identify Technical Statements Requiring Verification

Create verification checklist:

**Technical Claims:**

- API behavior descriptions
- Language feature explanations
- Framework concepts
- Performance characteristics
- Security properties
- Compatibility statements
- Version-specific features

**For Each Statement:**

- Quote the exact statement
- Note the location (section, page)
- Identify authoritative source to check
- Mark verification status (pending/verified/incorrect)

**Example Verification List:**

```
Statement: "React's useEffect runs after every render by default"
Location: Chapter 4, Section 2, Page 47
Source: https://react.dev/reference/react/useEffect
Status: Pending verification
```

### 3. Verify Technical Statements Against Authoritative Sources

Check each statement for accuracy:

**Authoritative Sources (in priority order):**

1. **Official Documentation**
   - Language docs (Python.org, MDN, docs.oracle.com)
   - Framework official docs (reactjs.org, angular.io, vuejs.org)
   - Library documentation (official repos/sites)

2. **Standards and Specifications**
   - RFCs (IETF specifications)
   - PEPs (Python Enhancement Proposals)
   - ECMAScript specifications
   - W3C standards

3. **Official Release Notes**
   - Version-specific features
   - Deprecation notices
   - Breaking changes

4. **Reputable Technical Sources**
   - Official blogs (Mozilla Hacks, Go Blog, etc.)
   - Conference talks by maintainers
   - Authoritative technical books

**Verification Process:**

For each technical claim:

1. Locate authoritative source
2. Read relevant section carefully
3. Compare claim to source
4. Note any discrepancies
5. Check version applicability
6. Record verification result

**Document Findings:**

**For Correct Statements:**

```
Statement: "React's useEffect runs after every render by default"
Verification: CORRECT
Source: https://react.dev/reference/react/useEffect
Notes: Confirmed in official docs. True when no dependency array provided.
```

**For Incorrect Statements:**

```
Statement: "Python's len() returns 1-indexed length"
Verification: INCORRECT
Severity: Critical
Correct Info: len() returns 0-indexed count (number of items)
Source: https://docs.python.org/3/library/functions.html#len
Example: len([10, 20, 30]) returns 3, not 4
```

**For Imprecise Statements:**

```
Statement: "useEffect runs after render"
Verification: IMPRECISE
Severity: Minor
Correct Info: "useEffect runs after render is committed to the screen (after browser paint)"
Source: https://react.dev/reference/react/useEffect
Notes: Original statement is technically correct but lacks precision
```

### 4. Test All Code Examples for Correctness

Validate code execution and output:

**For Each Code Example:**

**Step 1: Extract Code**

- Copy complete code example
- Include all shown imports/dependencies
- Note any setup code mentioned

**Step 2: Set Up Test Environment**

- Install correct language/framework versions
- Install required dependencies
- Configure environment as specified

**Step 3: Run Code**

- Execute code exactly as shown
- Capture actual output
- Note any errors or warnings

**Step 4: Compare Results**

- Does output match claimed output?
- Does behavior match description?
- Are there any unexpected errors?

**Document Test Results:**

**Working Example:**

```
Location: Chapter 3, Example 3.2
Code: Array.map() example
Test Result: PASS
Output: Matches expected output exactly
Environment: Node.js 20.0.0
```

**Broken Example:**

```
Location: Chapter 5, Example 5.1
Code: Async database query
Test Result: FAIL
Severity: Critical
Error: TypeError: Cannot read property 'query' of undefined
Issue: Missing connection initialization code
Fix: Add `const connection = await createConnection()` before query
```

**Incomplete Example:**

```
Location: Chapter 7, Example 7.3
Code: Express middleware
Test Result: INCOMPLETE
Severity: Major
Issue: Missing import statements (express, body-parser)
Fix: Add required imports at top of example
```

### 5. Check API and Library Usage

Verify API calls are correct and current:

**For Each API/Library Call:**

**Check:**

- Function signature matches documentation
- Parameters in correct order
- Parameter types are correct
- Return type is accurate
- Method exists (not deprecated or renamed)
- Version compatibility

**Common API Issues:**

❌ **Incorrect Parameter Order:**

```javascript
// Content claims:
axios.get(headers, url);

// Actual correct usage:
axios.get(url, { headers });
```

❌ **Deprecated API:**

```javascript
// Content uses:
ReactDOM.render(<App />, container);

// Current API (React 18+):
const root = ReactDOM.createRoot(container);
root.render(<App />);
```

❌ **Wrong Return Type:**

```python
# Content claims map() returns a list
result = map(lambda x: x * 2, [1, 2, 3])
# Actually returns an iterator in Python 3

# Correct statement:
result = list(map(lambda x: x * 2, [1, 2, 3]))
```

**Document API Issues:**

```
Location: Chapter 6, Section 3
API: Array.prototype.sort()
Severity: Major
Issue: Claims sort() returns a new array
Correct: sort() mutates the original array in-place and returns reference to it
Source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
Impact: Readers may misunderstand side effects
```

### 6. Validate Diagrams Match Descriptions

Ensure visual representations are accurate:

**For Each Diagram:**

**Check:**

- Does diagram accurately represent the concept?
- Do labels match terminology in text?
- Are connections/flows correct?
- Are there any misleading elements?
- Does diagram match code/examples?

**Common Diagram Issues:**

- Arrows pointing wrong direction in data flow
- Components labeled differently than in code
- Missing important elements mentioned in text
- Oversimplification that creates misconceptions

**Document Diagram Issues:**

```
Location: Chapter 4, Figure 4.2
Diagram: React component lifecycle
Severity: Major
Issue: Shows componentWillMount as recommended lifecycle method
Correct: componentWillMount is deprecated (React 16.3+); show componentDidMount instead
Source: https://react.dev/reference/react/Component#componentwillmount
```

### 7. Cross-Check Terminology Consistency

Verify consistent and correct terminology:

**Check:**

- Terms used consistently throughout
- Technical terms spelled correctly
- Acronyms expanded on first use
- No conflating of distinct concepts

**Common Terminology Issues:**

❌ **Inconsistent Terms:**

- Uses "function," "method," and "procedure" interchangeably when discussing JavaScript
- Correct: Distinguish class methods from standalone functions

❌ **Incorrect Technical Terms:**

- Calls all errors "exceptions" in JavaScript
- Correct: JavaScript has errors; some languages have exceptions with different semantics

❌ **Conflated Concepts:**

- Uses "authentication" and "authorization" as synonyms
- Correct: Authentication = who you are, Authorization = what you can do

**Document Terminology Issues:**

```
Location: Throughout Chapter 8
Severity: Minor
Issue: Inconsistent terminology - alternates between "async function" and "asynchronous function"
Recommendation: Choose one term and use consistently (prefer "async function" as it matches the keyword)
```

### 8. Identify Outdated or Deprecated Information

Flag content that needs updating:

**Check For:**

**Deprecated Language Features:**

- Python 2 syntax in Python 3+ content
- var keyword in modern JavaScript guides
- Old-style React class components without hooks mention

**Deprecated APIs:**

- Removed or deprecated functions/methods
- Outdated library APIs
- Framework features replaced by newer approaches

**Outdated Best Practices:**

- Callback-based patterns when async/await is standard
- Older architectural patterns superseded
- Security practices now considered inadequate

**End-of-Life Software:**

- Libraries no longer maintained
- Language versions past EOL
- Frameworks without active support

**Document Outdated Content:**

```
Location: Chapter 9, Section 4
Severity: Major
Issue: Demonstrates Promise chaining with .then()
Current Standard: async/await is now the standard (Node 8+, released 2017)
Recommendation: Show .then() chaining briefly for understanding, then demonstrate async/await as the recommended approach
Source: Modern JavaScript best practices (MDN)
```

```
Location: Chapter 3, Examples
Severity: Critical
Issue: All examples use React class components
Current Standard: Functional components with Hooks (React 16.8+, 2019)
Recommendation: Rewrite examples using functional components with useState, useEffect
Source: https://react.dev/learn - official docs now teach hooks-first
```

### 9. Run Technical Accuracy Checklist

Execute systematic checklist:

**Run:** `execute-checklist.md` with `technical-accuracy-checklist.md`

**Verify:**

- All technical claims verified
- Version numbers correct
- API usage current
- Language features accurate
- Framework concepts correct
- No outdated information
- Sources verified
- Code correctness confirmed
- Best practices current
- Misconceptions avoided

**Document** any checklist items that fail.

### 10. Compile Verification Report

Create structured accuracy verification report:

**Report Structure:**

#### Executive Summary

- Overall verification status (Pass/Fail/Needs Revision)
- Critical errors count (factual errors, broken code)
- Major issues count (outdated info, API inaccuracies)
- Minor issues count (imprecision, terminology)
- Overall accuracy assessment

#### Technical Claims Verification

- Total claims verified: X
- Correct: Y
- Incorrect: Z
- List of incorrect claims with severity and corrections

#### Code Testing Results

- Total examples tested: X
- Working: Y
- Broken: Z
- Incomplete: W
- Details of broken/incomplete examples

#### API/Library Accuracy

- APIs checked: X
- Correct usage: Y
- Incorrect/deprecated: Z
- List of API issues with corrections

#### Diagram Validation

- Diagrams reviewed: X
- Accurate: Y
- Issues found: Z
- List of diagram issues

#### Terminology Consistency

- Key terms reviewed
- Consistency issues found
- Recommendations for standardization

#### Outdated Content

- Deprecated features identified
- Outdated practices found
- Recommended updates

#### Checklist Results

- Technical accuracy checklist pass/fail items

#### Recommendations

- Prioritized fixes by severity
- Specific corrections with sources
- Update recommendations

**Severity Definitions:**

- **Critical:** Factually incorrect information that would mislead readers or cause errors
  - Example: Wrong API signatures, broken code, security vulnerabilities
  - Action: Must fix before publication

- **Major:** Outdated or imprecise information that affects quality
  - Example: Deprecated APIs without warnings, outdated best practices
  - Action: Should fix before publication

- **Minor:** Small inaccuracies or inconsistencies
  - Example: Terminology inconsistencies, imprecise wording
  - Action: Consider fixing if time permits

**Pass/Fail Thresholds:**

- **Pass:** 0 critical, ≤ 2 major, minor acceptable
- **Needs Revision:** 0 critical, 3-5 major
- **Fail:** Any critical errors OR > 5 major

## Output

Technical accuracy verification report should include:

- Clear pass/fail status
- All verified claims (correct and incorrect)
- Code testing results
- API accuracy findings
- Diagram validation results
- Terminology consistency check
- Outdated content identification
- Checklist results
- Prioritized recommendations with sources

**Save to:** `reviews/validation-results/accuracy-verification-{{timestamp}}.md`

## Quality Standards

Effective accuracy verification:

✓ Verifies every technical claim against sources
✓ Tests all code examples in proper environment
✓ Checks API correctness against current docs
✓ Identifies all deprecated/outdated content
✓ Uses authoritative sources for verification
✓ Provides specific corrections with references
✓ Categorizes by appropriate severity
✓ Includes actionable recommendations

## Examples

### Example: Factual Error Found

**Finding:**

```
Location: Chapter 3, Section 2, Page 34
Statement: "JavaScript's Array.sort() always sorts alphabetically"
Verification: INCORRECT
Severity: Critical

Correct Information:
Array.sort() converts elements to strings and sorts in UTF-16 code unit order by default.
For numbers: [1, 10, 2].sort() returns [1, 10, 2] (NOT [1, 2, 10])
To sort numbers: array.sort((a, b) => a - b)

Source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort

Impact: Readers will incorrectly sort numeric arrays, causing bugs

Recommended Fix:
"JavaScript's Array.sort() converts elements to strings and sorts in UTF-16 code unit order.
For numeric arrays, provide a compare function: numbers.sort((a, b) => a - b)"
```

### Example: Code Example Failure

**Finding:**

```
Location: Chapter 5, Example 5.3
Code Example: Async database query
Test Result: FAIL
Severity: Critical

Error:
```

TypeError: Cannot read property 'query' of undefined
at example5-3.js:10:25

````

Issue: Missing database connection initialization
The example calls db.query() but never shows db connection setup

Fixed Code:
```javascript
// Add before the query:
const db = await createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'testdb'
})

// Then the query works:
const results = await db.query('SELECT * FROM users')
````

Recommendation: Either add connection setup to example, or add a note:
"Assuming db connection is already established (see Chapter 4)"

```

### Example: Deprecated API Usage

**Finding:**

```

Location: Chapter 7, Throughout
API: ReactDOM.render()
Severity: Major

Issue: All examples use ReactDOM.render(<App />, root)
This API is deprecated in React 18 (March 2022)

Current API:

```javascript
// Old (deprecated):
ReactDOM.render(<App />, document.getElementById('root'));

// Current (React 18+):
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
```

Source: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

Recommendation: Update all examples to use createRoot API, or add prominent warning that examples use React 17 API

```

## Next Steps

After verification:

1. Deliver verification report to author
2. Author addresses critical issues (must fix)
3. Author addresses major issues (should fix)
4. Re-verify code examples if critical fixes made
5. Approve for next review phase (editorial/QA)
```

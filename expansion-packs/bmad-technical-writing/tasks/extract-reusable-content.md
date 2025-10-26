<!-- Powered by BMAD™ Core -->

# Extract Reusable Content

---

task:
id: extract-reusable-content
name: Extract Reusable Content
description: Identify patterns and explanations reusable across chapters
persona_default: technical-editor
inputs: - completed-chapters (one or more finished chapters) - manuscript-directory
steps: - Analyze content for repeated patterns - Identify reusable concept explanations - Find common code patterns and templates - Extract troubleshooting content - Document each pattern with usage guidance - Create content library structure - Add reuse guidelines and customization points
output: Content library with categorized reusable patterns
ai_assistance: true
human_verification_required: false

---

## Purpose

This task identifies explanations, code patterns, and teaching content that appear repeatedly across chapters, then extracts them into a reusable content library. This enables consistency (same concepts explained the same way), efficiency (don't rewrite from scratch), and quality (polish patterns once, reuse everywhere).

## Benefits of Content Library

**Consistency:**

- Same concepts explained the same way throughout the book
- Consistent terminology and examples
- Uniform teaching approach

**Efficiency:**

- Don't rewrite similar explanations from scratch
- Faster chapter development
- Reduce redundant work

**Quality:**

- Polished explanations refined over time
- Tested and validated patterns
- Improved through reader feedback

**Maintenance:**

- Update pattern once, applies everywhere referenced
- Track where patterns are used
- Easier to fix errors or improve clarity

## Prerequisites

Before starting this task:

- **Completed chapters available** - At least 2-3 finished chapters
- **Content finalized** - Chapters have been reviewed and polished
- **Access to manuscript directory** - Can read all chapter files
- **Understanding of book structure** - Know overall organization and topics

## Workflow Steps

### 1. Analyze Content

Read through chapters looking for repetition and patterns:

**Read Through Chapters:**

- Read 2-3+ completed chapters thoroughly
- Note explanations that seem familiar
- Identify similar code structures
- Find repeated teaching approaches

**Look for Repetition:**

```markdown
## Pattern Detection

**Repeated Explanations:**

- "How async/await works" appears in Chapters 3, 5, 7
- "Why we use const over let" in Chapters 2, 4, 6, 8
- "Destructuring syntax" in Chapters 3, 4, 5

**Similar Code Patterns:**

- Try-catch error handling: Ch 3, 5, 7, 8
- API request with fetch: Ch 4, 6, 7
- Express route handlers: Ch 5, 6, 7, 8

**Common Teaching Approaches:**

- "Problem → Solution → Example" for new concepts
- "Before/After code comparison" for refactoring
- "Common Mistakes" sections
```

**Identify Themes:**

```markdown
## Theme Analysis

**Error Handling:**

- Appears in: 5 chapters
- Variations: Basic try-catch, async error handling, API errors, database errors
- Core pattern: Same structure, different context

**API Interactions:**

- Appears in: 4 chapters
- Variations: GET, POST, authentication, error handling
- Core pattern: fetch → parse → handle errors

**Best Practices:**

- Appears throughout
- Variations: Security, performance, code organization
- Core pattern: ❌ Don't... ✅ Do... pattern
```

### 2. Identify Reusable Patterns

Categorize content by reusability type:

#### Pattern Type 1: Concept Explanations

Explanations that appear multiple times in different contexts:

````markdown
### Example: Async/Await Explanation

**Used in:**

- Chapter 3, Section 2: "Handling Asynchronous Operations"
- Chapter 5, Section 4: "Making API Requests"
- Chapter 7, Section 1: "Database Queries"

**Core Explanation (Reusable):**

Async/await provides a cleaner syntax for working with Promises. Instead of chaining `.then()` calls, you can write asynchronous code that looks synchronous.

The `async` keyword before a function declaration means the function returns a Promise. The `await` keyword pauses execution until a Promise resolves, allowing you to assign the result directly to a variable.

```javascript
// Promise chaining (older style)
fetchUser()
  .then((user) => fetchOrders(user.id))
  .then((orders) => console.log(orders))
  .catch((err) => console.error(err));

// Async/await (modern style)
async function getUserOrders() {
  try {
    const user = await fetchUser();
    const orders = await fetchOrders(user.id);
    console.log(orders);
  } catch (err) {
    console.error(err);
  }
}
```
````

**Context-Specific Variations:**

- Chapter 3: Applied to file I/O
- Chapter 5: Applied to HTTP requests
- Chapter 7: Applied to database queries

**Customization Points:**

- Replace example domain (files, API, database)
- Adjust error handling detail level
- Add or remove complexity

````

#### Pattern Type 2: Code Patterns

Reusable code templates with variations:

```markdown
### Example: Express Route Handler with Error Handling

**Used in:**
- Chapter 5: User authentication routes
- Chapter 6: Product CRUD operations
- Chapter 7: Order processing
- Chapter 8: Admin dashboard

**Generic Template:**

```javascript
// [DESCRIPTION]: Brief description of what route does
router.[METHOD]('[PATH]', async (req, res) => {
  try {
    // 1. Extract and validate input
    const { [PARAMS] } = req.[body|params|query];

    // Validation
    if (![VALIDATION_CONDITION]) {
      return res.status(400).json({ error: '[ERROR_MESSAGE]' });
    }

    // 2. Perform operation
    const result = await [OPERATION];

    // 3. Return success response
    res.status([SUCCESS_CODE]).json({
      success: true,
      data: result
    });
  } catch (err) {
    console.error('[ERROR_PREFIX]:', err);
    res.status(500).json({ error: '[GENERIC_ERROR_MESSAGE]' });
  }
});
````

**Customization Points:**

- `[METHOD]`: get, post, put, delete
- `[PATH]`: Route path ('/users', '/products/:id', etc.)
- `[PARAMS]`: Parameter names to extract
- `[VALIDATION_CONDITION]`: Specific validation logic
- `[OPERATION]`: Core business logic
- `[SUCCESS_CODE]`: 200, 201, 204, etc.

**Usage Examples:**

_Chapter 5 - Create User:_

```javascript
router.post('/users', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }

    const user = await User.create({ email, password });

    res.status(201).json({
      success: true,
      data: user,
    });
  } catch (err) {
    console.error('Create user error:', err);
    res.status(500).json({ error: 'Failed to create user' });
  }
});
```

````

#### Pattern Type 3: Troubleshooting Content

Common errors explained repeatedly:

```markdown
### Example: "Cannot read property of undefined" Error

**Used in:**
- Chapter 2: Variable basics
- Chapter 4: Object manipulation
- Chapter 6: API responses
- Chapter 8: Database results

**Generic Explanation:**

**Error:**
````

TypeError: Cannot read property 'X' of undefined

````

**Cause:**
You're trying to access a property on an object that doesn't exist (it's `undefined`).

**Common Scenarios:**

1. **Optional chaining needed:**
```javascript
// ❌ Error if user is undefined
const name = user.name;

// ✅ Safe with optional chaining
const name = user?.name;
````

2. **Missing null check:**

```javascript
// ❌ Error if getUserById returns null
const user = getUserById(id);
console.log(user.email);

// ✅ Check before accessing
const user = getUserById(id);
if (user) {
  console.log(user.email);
}
```

3. **API response missing expected data:**

```javascript
// ❌ Error if response.data is undefined
const items = response.data.items;

// ✅ Provide default
const items = response.data?.items || [];
```

**Prevention:**

- Use optional chaining (`?.`) for potentially undefined values
- Validate data before accessing nested properties
- Provide default values with nullish coalescing (`??`)

**Variations by Chapter:**

- Chapter 2: Basic variable access
- Chapter 4: Object manipulation context
- Chapter 6: API response handling context
- Chapter 8: Database query results context

````

#### Pattern Type 4: Best Practices

Repeated advice given in multiple contexts:

```markdown
### Example: "Don't Store Sensitive Data in Client-Side Code"

**Used in:**
- Chapter 3: Environment variables
- Chapter 5: API keys
- Chapter 7: Database credentials
- Chapter 9: Authentication tokens

**Generic Guidance:**

**❌ Don't:**
```javascript
// NEVER hardcode sensitive data
const API_KEY = "sk_live_abc123..."; // ❌ Exposed in source code
const DB_PASSWORD = "mySecretPassword"; // ❌ Committed to Git
````

**✅ Do:**

```javascript
// Use environment variables
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;
```

**Why This Matters:**

- Source code is often public (GitHub, etc.)
- Attackers can find hardcoded secrets
- Secrets should be configurable per environment
- Leaked credentials create security vulnerabilities

**Implementation:**

1. Create `.env` file (add to `.gitignore`)
2. Store secrets in `.env`:
   ```
   API_KEY=sk_live_abc123...
   DB_PASSWORD=mySecretPassword
   ```
3. Load with `dotenv` package:
   ```javascript
   require('dotenv').config();
   const apiKey = process.env.API_KEY;
   ```

**Context-Specific Applications:**

- Chapter 3: Focus on environment setup
- Chapter 5: Focus on API key management
- Chapter 7: Focus on database connection strings
- Chapter 9: Focus on JWT secrets

````

### 3. Extract and Document

For each reusable pattern, create a comprehensive document:

**Pattern Documentation Template:**

```markdown
# Pattern: [Pattern Name]

## Summary

[One-sentence description of what this pattern is]

## Used In

- Chapter [X], Section [Y]: [Context]
- Chapter [X], Section [Y]: [Context]
- [Additional locations...]

## Generic Version

[Explanation/code that's context-independent]

### Code Template (if applicable)

```[language]
[Reusable code with [PLACEHOLDERS]]
````

## Customization Points

- **[PLACEHOLDER_1]**: [Description of what to replace and with what]
- **[PLACEHOLDER_2]**: [Description of what to replace and with what]

## Variations

### Variation 1: [Name]

[When to use this variation]

```[language]
[Code/explanation for this variation]
```

### Variation 2: [Name]

[When to use this variation]

```[language]
[Code/explanation for this variation]
```

## Usage Guidelines

**When to use this pattern:**

- [Scenario 1]
- [Scenario 2]

**When NOT to use this pattern:**

- [Scenario where alternative is better]

**Customization steps:**

1. [Step 1]
2. [Step 2]

## Examples

### Example 1: [Context]

[Full example showing pattern in specific context]

### Example 2: [Context]

[Full example showing pattern in different context]

## Related Patterns

- [Related Pattern 1]: [How they relate]
- [Related Pattern 2]: [How they relate]

## Notes

[Any additional considerations, gotchas, or tips]

```

### 4. Create Content Library

Organize extracted patterns into a structured library:

**Directory Structure:**

```

content-library/
├── README.md # Library overview and usage guide
├── explanations/ # Reusable concept explanations
│ ├── async-await-basics.md
│ ├── destructuring-syntax.md
│ ├── arrow-functions.md
│ ├── scope-and-closures.md
│ └── ...
├── code-patterns/ # Reusable code templates
│ ├── express-route-handler.md
│ ├── api-request-fetch.md
│ ├── error-handling-try-catch.md
│ ├── database-query-template.md
│ ├── authentication-middleware.md
│ └── ...
├── troubleshooting/ # Common errors and solutions
│ ├── cannot-read-property-undefined.md
│ ├── cors-errors.md
│ ├── async-function-returns-promise.md
│ ├── port-already-in-use.md
│ └── ...
├── best-practices/ # Repeated advice and guidelines
│ ├── dont-store-secrets-in-code.md
│ ├── use-const-over-let.md
│ ├── validate-user-input.md
│ ├── handle-errors-gracefully.md
│ └── ...
└── teaching-patterns/ # Pedagogical approaches
├── problem-solution-example.md
├── before-after-comparison.md
├── progressive-complexity.md
└── ...

````

**Library README:**

```markdown
# Content Library

This library contains reusable explanations, code patterns, troubleshooting guides, and best practices extracted from the book manuscript.

## Purpose

- **Consistency**: Use the same explanation for a concept throughout the book
- **Efficiency**: Don't rewrite common patterns from scratch
- **Quality**: Refined, polished content reused in multiple contexts
- **Maintenance**: Update once, benefit everywhere

## Usage

### Using an Explanation

1. Find the concept in `explanations/`
2. Read the generic version
3. Check customization points
4. Select appropriate variation for your context
5. Customize as needed
6. Reference in your chapter

### Using a Code Pattern

1. Find the pattern in `code-patterns/`
2. Copy the template code
3. Replace `[PLACEHOLDERS]` with your specific values
4. Test the customized code
5. Integrate into your chapter

### Using a Troubleshooting Guide

1. Find the error in `troubleshooting/`
2. Use the generic explanation
3. Adapt the context/examples to your chapter
4. Include relevant prevention tips

## Categories

- **explanations/**: Concept explanations (async/await, closures, etc.)
- **code-patterns/**: Reusable code templates (routes, error handling, etc.)
- **troubleshooting/**: Common errors and solutions
- **best-practices/**: Repeated advice and guidelines
- **teaching-patterns/**: Pedagogical approaches and structures

## Contributing

When you write a new chapter and encounter content that could be reusable:

1. Check if similar pattern already exists
2. If yes, use existing pattern (adapt if needed)
3. If no, consider extracting a new pattern
4. Document thoroughly with customization guidance

## Maintenance

- Update patterns based on reader feedback
- Refine explanations for clarity
- Add new variations as discovered
- Track usage to identify most valuable patterns
````

### 5. Add Usage Guidance

For each pattern, provide clear instructions:

**When to Use This Pattern:**

```markdown
## Usage Guidelines: Express Route Handler Template

**Use this pattern when:**

- Creating CRUD endpoints in Express
- Need consistent error handling across routes
- Want standard success/error response format
- Building RESTful API endpoints

**Don't use this pattern when:**

- Building GraphQL endpoints (different structure)
- Using different framework (adapt accordingly)
- Need streaming responses (different approach)
- Error handling is domain-specific (customize heavily)
```

**Customization Steps:**

```markdown
## How to Customize

1. **Identify the HTTP method**
   - GET for retrieving data
   - POST for creating resources
   - PUT/PATCH for updating
   - DELETE for removing

2. **Define the route path**
   - Static: `/users`, `/products`
   - Dynamic: `/users/:id`, `/products/:productId`

3. **Determine input source**
   - `req.body` for POST/PUT/PATCH
   - `req.params` for URL parameters
   - `req.query` for query strings

4. **Add validation logic**
   - Check required fields
   - Validate data types
   - Verify business rules

5. **Implement core operation**
   - Database query
   - External API call
   - Business logic processing

6. **Set appropriate status code**
   - 200 OK (successful GET/PUT/PATCH)
   - 201 Created (successful POST)
   - 204 No Content (successful DELETE)

7. **Test thoroughly**
   - Happy path
   - Validation errors
   - Server errors
```

**Examples in Context:**

````markdown
## Usage Examples

### Example 1: User Registration (Chapter 5)

**Context:** Creating a new user account

**Customization:**

- Method: POST
- Path: /users
- Input: req.body (email, password)
- Validation: Email format, password strength
- Operation: User.create()
- Success: 201 Created

**Result:**

```javascript
router.post('/users', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'Valid email required' });
    }

    const user = await User.create({ email, password });

    res.status(201).json({
      success: true,
      data: { id: user.id, email: user.email },
    });
  } catch (err) {
    console.error('Registration error:', err);
    res.status(500).json({ error: 'Registration failed' });
  }
});
```
````

### Example 2: Get Product Details (Chapter 6)

**Context:** Retrieving a single product by ID

**Customization:**

- Method: GET
- Path: /products/:id
- Input: req.params (id)
- Validation: ID exists, valid format
- Operation: Product.findById()
- Success: 200 OK

**Result:**

```javascript
router.get('/products/:id', async (req, res) => {
  try {
    const { id } = req.params;

    if (!id) {
      return res.status(400).json({ error: 'Product ID required' });
    }

    const product = await Product.findById(id);

    if (!product) {
      return res.status(404).json({ error: 'Product not found' });
    }

    res.status(200).json({
      success: true,
      data: product,
    });
  } catch (err) {
    console.error('Get product error:', err);
    res.status(500).json({ error: 'Failed to retrieve product' });
  }
});
```

````

### 6. Track Usage

Document where each pattern is used:

**Usage Tracking:**

```markdown
# Pattern Usage: Express Route Handler Template

## Chapters Using This Pattern

### Chapter 5: Building Authentication
- Section 3: User Registration (`POST /users`)
- Section 4: User Login (`POST /login`)
- Section 5: Get User Profile (`GET /users/:id`)
- Section 6: Update Profile (`PUT /users/:id`)

### Chapter 6: Product Management
- Section 2: List Products (`GET /products`)
- Section 3: Get Product (`GET /products/:id`)
- Section 4: Create Product (`POST /products`)
- Section 5: Update Product (`PUT /products/:id`)
- Section 6: Delete Product (`DELETE /products/:id`)

### Chapter 7: Order Processing
- Section 2: Create Order (`POST /orders`)
- Section 3: Get Order (`GET /orders/:id`)
- Section 4: Cancel Order (`PUT /orders/:id/cancel`)

## Total Uses: 12 instances across 3 chapters

## Update History
- 2024-01-15: Created pattern
- 2024-01-22: Added 404 handling variation (Chapter 6)
- 2024-02-01: Added async error handling note (reader feedback)
````

## Quality Standards

A well-extracted content library provides:

✅ **Comprehensive Coverage:**

- All repeated patterns identified
- Explanations, code, troubleshooting, best practices
- Organized into clear categories

✅ **Clear Documentation:**

- Each pattern thoroughly documented
- Generic version provided
- Customization points identified
- Usage examples included

✅ **Practical Usability:**

- Easy to find patterns
- Clear instructions for customization
- Multiple examples showing context adaptation
- Guidelines for when to use each pattern

✅ **Maintenance Tracking:**

- Usage documented (where patterns appear)
- Update history maintained
- Feedback incorporated

## Common Pitfalls

❌ **Extracting non-reusable content** - One-off explanations don't belong in library

✅ **Extract true patterns** - Must appear 2+ times with variations

---

❌ **Too specific** - Pattern is so specific it's not reusable

✅ **Appropriate generalization** - Generic enough for reuse, specific enough for clarity

---

❌ **Insufficient documentation** - Just the code/explanation without usage guidance

✅ **Complete documentation** - Generic version + customization points + examples + guidelines

---

❌ **Poor organization** - Random files with no structure

✅ **Clear categorization** - Explanations, code, troubleshooting, best practices

---

❌ **No usage tracking** - Don't know where patterns are used

✅ **Track usage** - Document all locations using each pattern

## Integration with Workflows

**When to Extract:**

```
Chapter Development:
  Write Chapter 1 → Complete
  Write Chapter 2 → Complete
  Write Chapter 3 → Complete ← "Hmm, explaining async/await again..."
    ↓
  Run extract-reusable-content.md
    ↓
  Content Library Created
    ↓
  Write Chapter 4+ → Reference library patterns
```

**Ongoing Maintenance:**

```
Reader Feedback:
  "Closure explanation in Ch 7 clearer than Ch 3"
    ↓
  Update content-library/explanations/closures.md
    ↓
  Revise Ch 3 using updated pattern
    ↓
  Consistency improved
```

## Next Steps

After creating content library:

1. **Integrate into workflow**
   - Reference library when writing new chapters
   - Use patterns instead of rewriting

2. **Share with collaborators**
   - Co-authors use same patterns
   - Consistency across contributors

3. **Maintain actively**
   - Update based on feedback
   - Refine patterns over time
   - Add new patterns as discovered

4. **Track effectiveness**
   - Note time saved
   - Monitor consistency improvements
   - Identify most valuable patterns

## Related Tasks

- **synthesize-research-notes.md** - May identify reusable research patterns
- **expand-outline-to-draft.md** - Can use library patterns when expanding
- **generate-explanation-variants.md** - Refined variants become library patterns
- **write-section-draft.md** - Reference library when writing sections
- **technical-review-section.md** - May suggest extracting patterns for reuse

# Technical Writing Standards

Comprehensive standards for creating clear, consistent, accessible, and well-structured technical content. These principles apply across all publishers and formats.

## Clarity Principles

### Use Simple, Direct Language

**Do:**

- "Click the Submit button" (clear, direct)
- "The function returns a boolean value" (precise)
- "Remove the file" (simple verb)

**Don't:**

- "Utilize the Submit functionality to initiate the process" (unnecessarily complex)
- "The function facilitates the return of a boolean-type value" (wordy)
- "Effect the removal of the file" (pretentious)

### Explain Technical Terms

**First Use Pattern:**

```
JSON (JavaScript Object Notation) is a lightweight data format...
[Later in text]
...parse the JSON data...
```

**Inline Explanation:**

```
The API returns a 401 status code, which indicates unauthorized access.
```

**Glossary Reference:**

```
The service uses OAuth2 for authentication (see Glossary).
```

### Provide Examples

**Abstract Concept:**

```
❌ "Functions should be idempotent."

✓ "Functions should be idempotent - producing the same result when called multiple times with the same input. For example, `getUserById(123)` should always return the same user data for ID 123."
```

**Show, Then Tell:**

```python
# Example first
def calculate_total(items):
    return sum(item.price for item in items)

# Then explain
The calculate_total function demonstrates list comprehension,
a Pythonic way to iterate and transform data in a single line.
```

### Break Down Complex Ideas

**Step-by-Step:**

```
To implement authentication:
1. Create a User model with password hashing
2. Build registration endpoint to create users
3. Implement login endpoint to verify credentials
4. Generate JWT token upon successful login
5. Create middleware to validate tokens
6. Protect routes using the middleware
```

**Progressive Disclosure:**

- Start with simplest case
- Add complexity incrementally
- Reference advanced topics for later

### Active Voice

**Prefer Active:**

- "The function returns an array" (active)
- "Pass the parameter to the function" (active)
- "The compiler throws an error" (active)

**Avoid Passive:**

- "An array is returned by the function" (passive)
- "The parameter should be passed to the function" (passive)
- "An error is thrown by the compiler" (passive)

**Exception:** Passive voice appropriate when actor is unknown or unimportant:

- "The file was corrupted" (we don't know who/what corrupted it)
- "Python was released in 1991" (focus on Python, not Guido)

### Sentence Clarity

**One Idea Per Sentence:**

```
❌ "The function validates the input and then transforms it to the required format and returns it to the caller or throws an error if validation fails."

✓ "The function first validates the input. If validation succeeds, it transforms the data to the required format and returns it. If validation fails, it throws an error."
```

**Specific vs Vague:**

```
❌ "The database might have some issues with performance."
✓ "Query response time increases from 50ms to 2 seconds when the users table exceeds 1 million rows."
```

---

## Consistency Requirements

### Terminology Consistency

**Choose One Term:**

```
✓ Consistent: "function" throughout
❌ Inconsistent: "function", "method", "routine", "procedure" interchangeably
```

**Create a Term List:**

```
Preferred Terms:
- "filesystem" (not "file system")
- "username" (not "user name")
- "backend" (not "back-end" or "back end")
- "email" (not "e-mail")
- "GitHub" (not "Github")
```

### Style Consistency

**Code Formatting:**

```
✓ Consistent:
Use `variable_name` for variables and `function_name()` for functions.

❌ Inconsistent:
Use variable_name for variables and function_name() for functions.
(Missing backticks, inconsistent formatting)
```

**Heading Capitalization:**

```
✓ Title Case Consistent:
## Chapter 1: Building Your First API
## Chapter 2: Adding Authentication
## Chapter 3: Deploying to Production

✓ Sentence Case Consistent:
## Chapter 1: Building your first API
## Chapter 2: Adding authentication
## Chapter 3: Deploying to production

❌ Inconsistent Mix:
## Chapter 1: Building your First API
## Chapter 2: Adding Authentication
```

### Voice and Tone

**Maintain Consistent Perspective:**

```
✓ Second Person Throughout:
"You create a function by using the def keyword. You then add parameters..."

❌ Mixed Perspectives:
"You create a function by using the def keyword. We then add parameters..."
"One creates a function by using the def keyword..."
```

**Consistent Formality Level:**

- Casual: "Let's dive in!", "Cool!", "Pretty neat, right?"
- Professional: "We'll begin", "Effective", "This demonstrates"
- Pick one and maintain throughout

### Formatting Patterns

**Code Blocks:**

```
✓ Consistent:
All code blocks use language tags and show complete context

❌ Inconsistent:
Some with language tags, some without; some show imports, some don't
```

**Lists:**

```
✓ Parallel Structure:
- Create the database
- Configure the connection
- Test the setup

❌ Non-Parallel:
- Create the database
- Configuring the connection
- You should test the setup
```

---

## Accessibility Standards

### Alt Text for Images

**Descriptive Alt Text:**

```
❌ <img alt="screenshot">
❌ <img alt="Figure 1">

✓ <img alt="Django admin interface showing user list with filter sidebar">
✓ <img alt="Error message: 'Connection refused on localhost:5432'">
```

**Complex Diagrams:**

```
<img alt="Authentication flow diagram" longdesc="auth-flow-description.html">

In text or linked file:
"The authentication flow begins with the client sending credentials to
the /login endpoint. The server validates these against the database.
If valid, a JWT token is generated and returned. The client includes
this token in subsequent requests via the Authorization header..."
```

### Color and Visual Information

**Don't Rely on Color Alone:**

```
❌ "The red items are errors, green items are successes."

✓ "Errors are marked with a red X icon (❌), while successes show a green checkmark (✓)."
```

**Code Syntax Highlighting:**

```
# Ensure code is understandable without color

❌ Relying only on color to show strings vs keywords

✓ Use descriptive comments:
# This string contains the API key:
api_key = "abc123xyz"
```

### Document Structure

**Proper Heading Hierarchy:**

```
✓ Correct:
# Chapter 1: Introduction (H1)
## Section 1.1: Prerequisites (H2)
### Installing Python (H3)
### Installing VS Code (H3)
## Section 1.2: Your First Program (H2)

❌ Incorrect:
# Chapter 1: Introduction (H1)
### Installing Python (H3) - skipped H2
## Your First Program (H2) - after H3
```

**Meaningful Headings:**

```
✓ Descriptive: "Installing PostgreSQL on macOS"
❌ Generic: "Installation" or "Next Steps"
```

### Screen Reader Considerations

**Link Text:**

```
❌ "Click [here] to download Python."
❌ "Learn more at [this link]."

✓ "[Download Python 3.11 for Windows]"
✓ "Read the [official Django tutorial]"
```

**Table Structure:**

```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1A  | Data 2A  | Data 3A  |

✓ Uses proper markdown table format with headers
✓ Screen readers can navigate by rows/columns
```

**Code Examples:**

```python
# Use descriptive variable names that make sense when read aloud
✓ user_email = "user@example.com"
❌ x = "user@example.com"

# Function names should be read able
✓ calculate_total_price()
❌ calc_tot()
```

### Plain Language

**Acronyms:**

```
✓ "REST (Representational State Transfer) is an architectural style..."
Later: "...using REST APIs..."

❌ Assuming knowledge: "Using REST..." (no definition)
```

**Define Jargon:**

```
✓ "Idempotent operations produce the same result when executed multiple times."
❌ "Operations should be idempotent." (no explanation)
```

---

## Structure Best Practices

### Logical Topic Progression

**Foundation First:**

```
Chapter Sequence:
1. Python Basics → 2. Functions → 3. Classes → 4. Advanced OOP
(Each builds on previous)

❌ Poor Sequence:
1. Advanced OOP → 2. Classes → 3. Python Basics
```

**Dependency Management:**

```
✓ "In Chapter 2, we learned about functions. Now we'll use functions to..."
✓ "This builds on the authentication system from Chapter 5..."

❌ Referencing concepts not yet covered without explanation
```

### Section Organization

**Consistent Chapter Structure:**

```
Chapter Template:
1. Introduction (hooks, context, objectives)
2. Prerequisites
3. Concept Explanation
4. Tutorial/Hands-On
5. Exercises
6. Summary
7. Further Reading

Use same structure for every chapter (readers know what to expect)
```

**Section Length:**

- Chapters: 15-30 pages typical
- Major sections: 3-8 pages
- Subsections: 1-3 pages
- Keep related content together

### Transitions

**Between Sections:**

```
✓ "Now that you understand basic routing, let's add authentication to protect routes."

✓ "With the database configured, we're ready to create our first model."

❌ Abrupt jump to new topic without connection
```

**Between Chapters:**

```
Chapter End: "In the next chapter, we'll deploy this application to production."

Next Chapter Start: "In Chapter 5, we built a REST API. Now we'll deploy it using Docker and AWS."
```

### Cross-References

**Specific References:**

```
✓ "See Chapter 3, Section 3.2: Database Setup"
✓ "As explained in the Authentication section on page 45..."

❌ "As mentioned earlier..."
❌ "See above..."
```

**Forward References:**

```
✓ "We'll cover error handling in depth in Chapter 8."
✓ "Advanced caching strategies are beyond this book's scope. See 'High Performance Python' by Gorelick and Ozsvald."

Manage expectations about what's covered where
```

### Visual Hierarchy

**Use Formatting:**

- **Bold** for emphasis or key terms
- `Code formatting` for inline code
- > Blockquotes for important callouts
- Lists for series of items
- Tables for structured data

**Consistent Callouts:**

```
**Note:** Additional information
**Warning:** Potential pitfall
**Tip:** Helpful suggestion
**Exercise:** Practice opportunity
```

---

## Code Documentation Standards

### Code Comments

**Explain Why, Not What:**

```python
❌ # Set x to 5
x = 5

✓ # Default timeout in seconds
timeout = 5

✓ # Use exponential backoff to avoid overwhelming the API
for attempt in range(max_retries):
    time.sleep(2 ** attempt)
```

**Document Intent:**

```python
✓ # Remove duplicates while preserving order
seen = set()
result = [x for x in items if not (x in seen or seen.add(x))]

❌ # Loop through items
for item in items:
    # Do something
    ...
```

### Function Documentation

**Docstring Standard:**

```python
def authenticate_user(username, password):
    """
    Authenticate user credentials against the database.

    Args:
        username (str): The user's username
        password (str): The user's plain-text password

    Returns:
        User: The authenticated user object

    Raises:
        AuthenticationError: If credentials are invalid
        DatabaseError: If database connection fails

    Example:
        >>> user = authenticate_user("john", "secret123")
        >>> print(user.email)
        john@example.com
    """
```

### API Documentation

**Endpoint Description:**

```
GET /api/users/:id

Description: Retrieve a single user by ID

Parameters:
- id (path): User ID (integer)

Headers:
- Authorization: Bearer token required

Response 200:
{
  "id": 123,
  "username": "john",
  "email": "john@example.com"
}

Response 404:
{
  "error": "User not found"
}
```

---

## References and Resources

### Style Guide Standards

- Microsoft Writing Style Guide
- Google Developer Documentation Style Guide
- Chicago Manual of Style (for publishers)
- AP Stylebook (for journalism-style technical writing)

### Accessibility Standards

- WCAG 2.1 Level AA (minimum)
- Section 508 (US government)
- Plain Language guidelines

### Technical Writing Communities

- Write the Docs: https://www.writethedocs.org/
- TC (Technical Communication) Stack Exchange
- Reddit: r/technicalwriting

### Tools

- Hemingway Editor (readability)
- Grammarly (grammar and style)
- Vale (style guide linter)
- alex (inclusive language linter)

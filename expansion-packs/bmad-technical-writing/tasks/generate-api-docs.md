<!-- Powered by BMAD™ Core -->

# Generate API Documentation

---

task:
id: generate-api-docs
name: Generate API Documentation
description: Create comprehensive API reference documentation with parameters, return values, and usage examples
persona_default: api-documenter
inputs:
  - api-component (function, class, module, or API endpoint)
  - source-code or API specification
  - target-audience (developers using this API)
steps:
  - Identify all API components that need documentation
  - Extract function/method signatures from source code or spec
  - Document all parameters with types, descriptions, and constraints
  - Document return values with types and descriptions
  - Document exceptions and error conditions
  - Create 2-3 realistic usage examples for each API
  - Add cross-references to related APIs
  - Create parameter and return value tables
  - Validate examples work correctly
  - Format per publisher requirements
  - Use template api-reference-tmpl.yaml with create-doc.md task
  - Run execute-checklist.md with glossary-accuracy-checklist.md
output: docs/api-reference/{{api_name}}-reference.md

---

## Purpose

This task guides you through creating complete, accurate API reference documentation that developers can trust. The result is comprehensive reference material structured for quick lookup.

## Prerequisites

Before starting this task:

- Have access to source code or API specifications
- Know the target audience's technical level
- Have working code examples to validate
- Access to code-style-guides.md knowledge base

## Workflow Steps

### 1. Identify API Components

Determine what needs documentation:

- Individual functions or methods
- Classes and their members
- Modules or packages
- RESTful API endpoints
- Configuration options
- Data structures

Create a comprehensive list of all components.

### 2. Extract Signatures

For each API component, extract:

- Full function/method signature
- Import path or package location
- Version introduced (if applicable)
- Deprecation status (if applicable)

**Example:**

```python
def authenticate_user(username: str, password: str, remember_me: bool = False) -> AuthToken
```

### 3. Document Parameters

Create a complete parameter table:

| Parameter   | Type | Required | Default | Description                        |
| ----------- | ---- | -------- | ------- | ---------------------------------- |
| username    | str  | Yes      | -       | User's login username (3-50 chars) |
| password    | str  | Yes      | -       | User's password (min 8 chars)      |
| remember_me | bool | No       | False   | Keep user logged in beyond session |

For each parameter:

- Exact name as it appears in code
- Type annotation (be precise)
- Required or Optional
- Default value if optional
- Clear, concise description
- Valid ranges or constraints
- Examples of valid values

### 4. Document Return Values

Specify what the API returns:

- Return type (include None/null if possible)
- Description of returned value
- Structure of complex return objects
- Examples of return values
- Conditions that affect return value

**Example:**

```
Returns: AuthToken object containing JWT token (str) and expiration timestamp (datetime)
Returns None if authentication fails
```

### 5. Document Exceptions and Errors

List all possible errors:

| Exception/Error     | Condition                                 | How to Handle                      |
| ------------------- | ----------------------------------------- | ---------------------------------- |
| ValueError          | Username/password empty or invalid format | Validate input before calling      |
| AuthenticationError | Invalid credentials                       | Show error to user, allow retry    |
| NetworkError        | Auth service unavailable                  | Implement retry logic with backoff |

For each exception:

- Exception class name or error code
- What triggers this exception
- How to prevent or handle it
- Impact on application state

### 6. Create Usage Examples

Provide 2-3 realistic code examples:

**Example 1: Basic usage (most common case)**

```python
# Authenticate with username and password
token = authenticate_user("john_doe", "secure_password")
if token:
    print(f"Login successful, token expires: {token.expires_at}")
```

**Example 2: Advanced usage (with optional parameters)**

```python
# Authenticate with persistent session
token = authenticate_user(
    username="john_doe",
    password="secure_password",
    remember_me=True
)
```

**Example 3: Error handling (production-ready)**

```python
# Proper error handling
try:
    token = authenticate_user(username, password)
    if token is None:
        print("Invalid credentials")
    else:
        # Proceed with authenticated session
        pass
except ValueError as e:
    print(f"Invalid input: {e}")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
```

Ensure:

- Examples are realistic and practical
- Code is tested and works correctly
- Examples demonstrate best practices
- Error handling is shown where appropriate

### 7. Add Cross-References

Link to related functionality:

- Functions that work together
- Alternative approaches
- Required setup functions (e.g., initialize_auth_service())
- Functions that consume this API's output
- Relevant chapter sections

**Example:**
"See also: `refresh_token()` for renewing expired tokens, `logout_user()` for ending sessions, Chapter 5: Authentication Architecture"

### 8. Create Reference Tables

For complex APIs, create summary tables:

**Authentication API Methods:**
| Method | Purpose | Returns |
|--------|---------|---------|
| authenticate_user() | Login with credentials | AuthToken |
| refresh_token() | Renew expired token | AuthToken |
| validate_token() | Check token validity | bool |
| logout_user() | End session | None |

### 9. Validate Examples

Ensure all code examples:

- [ ] Actually run without errors
- [ ] Use correct imports
- [ ] Follow project code style
- [ ] Demonstrate real-world usage
- [ ] Handle errors appropriately
- [ ] Work with current API version

Run examples in test environment to verify.

### 10. Format for Publisher

Apply publisher-specific formatting:

- **PacktPub**: Markdown with clear code blocks
- **O'Reilly**: AsciiDoc if required
- **Manning**: Code listings with callouts
- **Self-publish**: Clean markdown with syntax highlighting

### 11. Generate Documentation

Use the create-doc.md task with api-reference-tmpl.yaml template to create the structured API documentation.

### 12. Validate Terminology

Run checklist:

- glossary-accuracy-checklist.md - Ensure consistent terminology

## Success Criteria

Completed API documentation should have:

- [ ] All API components documented
- [ ] Complete parameter tables with types and descriptions
- [ ] Return values documented with types
- [ ] All exceptions and errors listed
- [ ] 2-3 working code examples per API
- [ ] Cross-references to related APIs
- [ ] Examples validated and tested
- [ ] Publisher formatting applied
- [ ] Terminology consistent with glossary
- [ ] Searchable structure (clear headings, tables)

## Common Pitfalls to Avoid

- **Incomplete parameter docs**: Every parameter needs type, description, constraints
- **Missing error cases**: Document all exceptions, not just happy path
- **Untested examples**: Always run examples to verify they work
- **Vague descriptions**: "Authenticates user" is too vague; be specific
- **No cross-references**: Link related APIs together
- **Inconsistent terminology**: Use same terms as glossary and main text
- **Missing edge cases**: Document behavior with null/None, empty strings, etc.

## Notes and Warnings

- **Type precision**: Use exact type annotations from code
- **Version compatibility**: Note if API changed between versions
- **Performance**: Document O(n) complexity if relevant
- **Thread safety**: Note if API is thread-safe or not
- **Platform differences**: Document platform-specific behavior
- **Security**: Warn about security implications (password handling, etc.)

## Next Steps

After generating API documentation:

1. Review with developers who use the API
2. Add to appendix or API reference chapter
3. Keep synchronized with code changes
4. Update glossary with new terms
5. Link from main chapter text to API reference

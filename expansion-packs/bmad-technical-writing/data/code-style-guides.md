# Code Style Guides for Technical Writing

This document summarizes language-specific coding standards for technical book code examples.

## Universal Code Example Standards

These apply to ALL code examples regardless of language:

### Readability First

- Use descriptive variable and function names
- Prefer clarity over cleverness
- Add inline comments for WHY, not WHAT
- Keep functions focused and small

### Educational Code vs Production Code

Technical book code should prioritize:

- **Clarity** over performance (unless teaching performance)
- **Explicitness** over brevity
- **Simplicity** over DRY (some repetition acceptable for clarity)
- **Readability** over advanced language features

### Comments

```
❌ Bad: Obvious comments
// increment counter
counter++;

✅ Good: Explain decisions
// Use exponential backoff to avoid overwhelming API during retry
await sleep(Math.pow(2, retryCount) * 1000);
```

### Error Handling

- Always demonstrate proper error handling
- Show common error scenarios
- Provide meaningful error messages
- Use language-appropriate patterns

### Magic Numbers

```
❌ Bad
if (age >= 18) { ... }

✅ Good
const MINIMUM_AGE = 18;
if (age >= MINIMUM_AGE) { ... }
```

---

## Python (PEP 8)

**Official Style Guide:** PEP 8 - Style Guide for Python Code

### Key Principles

**Indentation:**

- Use 4 spaces (not tabs)
- No mixing tabs and spaces

**Line Length:**

- Maximum 79 characters for code
- Maximum 72 for comments and docstrings

**Naming Conventions:**

```python
# Variables and functions: snake_case
user_name = "Alice"
def calculate_total(items): ...

# Constants: UPPER_CASE
MAX_CONNECTIONS = 100
API_TIMEOUT = 30

# Classes: PascalCase
class UserAccount: ...
class DatabaseConnection: ...

# Private: leading underscore
_internal_variable = 42
def _private_method(self): ...
```

**Imports:**

```python
# Standard library first
import os
import sys

# Then third-party
import requests
import numpy as np

# Then local imports
from myapp import models
from myapp.utils import helpers

# Avoid wildcard imports
from module import *  # ❌ Bad
from module import SpecificClass  # ✅ Good
```

**Docstrings:**

```python
def fetch_user(user_id: int) -> dict:
    """
    Fetch user data from the database.

    Args:
        user_id: The unique identifier for the user

    Returns:
        Dictionary containing user data

    Raises:
        UserNotFoundError: If user doesn't exist
    """
    ...
```

**Type Hints (Python 3.5+):**

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: list[dict]) -> None:
    ...
```

---

## JavaScript (Airbnb Style Guide)

**Official Style Guide:** Airbnb JavaScript Style Guide (github.com/airbnb/javascript)

### Key Principles

**Variables:**

```javascript
// Use const for values that won't be reassigned
const API_URL = 'https://api.example.com';
const user = { name: 'Alice' };

// Use let for values that will change
let counter = 0;

// Never use var
var oldStyle = 'bad'; // ❌
```

**Naming Conventions:**

```javascript
// Variables and functions: camelCase
const userName = "Alice";
function calculateTotal(items) { ... }

// Constants: UPPER_CASE (by convention)
const MAX_RETRY_COUNT = 3;
const API_TIMEOUT = 30000;

// Classes: PascalCase
class UserAccount { ... }
class DatabaseConnection { ... }

// Private (by convention): leading underscore
class Example {
  _privateMethod() { ... }
}
```

**Functions:**

```javascript
// Arrow functions for callbacks
const numbers = [1, 2, 3];
const doubled = numbers.map((n) => n * 2);

// Named functions for clarity
function processOrder(order) {
  // Implementation
}

// Avoid function hoisting confusion
// Declare before use
const helper = () => { ... };
helper();
```

**Strings:**

```javascript
// Use template literals for interpolation
const message = `Hello, ${userName}!`; // ✅ Good
const bad = 'Hello, ' + userName + '!'; // ❌ Avoid

// Use single quotes for simple strings
const apiKey = 'abc123';
```

**Objects and Arrays:**

```javascript
// Use shorthand
const name = 'Alice';
const user = { name }; // ✅ Good (shorthand)
const user2 = { name: name }; // ❌ Verbose

// Destructuring
const { id, email } = user;
const [first, second] = array;

// Spread operator
const newUser = { ...user, status: 'active' };
const newArray = [...oldArray, newItem];
```

---

## Java (Google Style Guide)

**Official Style Guide:** Google Java Style Guide

### Key Principles

**Indentation:**

- Use 2 spaces (not 4, not tabs)
- Continuation indent: 4 spaces

**Naming Conventions:**

```java
// Classes: PascalCase
public class UserAccount { }
public class DatabaseConnection { }

// Methods and variables: camelCase
public void calculateTotal() { }
private int userCount = 0;

// Constants: UPPER_CASE
private static final int MAX_CONNECTIONS = 100;
public static final String API_URL = "https://api.example.com";

// Packages: lowercase
package com.example.myapp;
```

**Braces:**

```java
// Braces on same line (K&R style)
if (condition) {
  // code
} else {
  // code
}

// Always use braces, even for single statements
if (condition) {
  doSomething();  // ✅ Good
}

if (condition)
  doSomething();  // ❌ Bad (no braces)
```

**Javadoc:**

```java
/**
 * Fetches user data from the database.
 *
 * @param userId the unique identifier for the user
 * @return User object containing user data
 * @throws UserNotFoundException if user doesn't exist
 */
public User fetchUser(int userId) throws UserNotFoundException {
  // Implementation
}
```

**Ordering:**

```java
public class Example {
  // 1. Static fields
  private static final int CONSTANT = 42;

  // 2. Instance fields
  private int count;

  // 3. Constructor
  public Example() { }

  // 4. Public methods
  public void doSomething() { }

  // 5. Private methods
  private void helper() { }
}
```

---

## Code Example Best Practices by Language

### Python

```python
# ✅ Good Example
def authenticate_user(username: str, password: str) -> dict:
    """
    Authenticate user and return JWT token.

    Args:
        username: User's login name
        password: User's password (will be hashed)

    Returns:
        Dictionary with 'token' and 'expires_at' keys

    Raises:
        AuthenticationError: If credentials are invalid
    """
    # Hash password for comparison
    password_hash = hash_password(password)

    # Query database
    user = User.query.filter_by(username=username).first()

    if not user or user.password_hash != password_hash:
        raise AuthenticationError("Invalid credentials")

    # Generate JWT token with 1-hour expiration
    token = jwt.encode(
        {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256",
    )

    return {"token": token, "expires_at": datetime.utcnow() + timedelta(hours=1)}
```

### JavaScript/Node.js

```javascript
// ✅ Good Example
async function authenticateUser(username, password) {
  // Hash password for comparison
  const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);

  // Query database
  const user = await User.findOne({ where: { username } });

  if (!user || !(await bcrypt.compare(password, user.passwordHash))) {
    throw new AuthenticationError('Invalid credentials');
  }

  // Generate JWT token with 1-hour expiration
  const token = jwt.sign({ userId: user.id }, SECRET_KEY, { expiresIn: '1h' });

  return {
    token,
    expiresAt: new Date(Date.now() + 3600000), // 1 hour from now
  };
}
```

### Java

```java
// ✅ Good Example
public class AuthService {
  private static final int TOKEN_EXPIRY_HOURS = 1;

  /**
   * Authenticates user and returns JWT token.
   *
   * @param username user's login name
   * @param password user's password (will be hashed)
   * @return AuthResponse containing token and expiration
   * @throws AuthenticationException if credentials are invalid
   */
  public AuthResponse authenticateUser(String username, String password)
      throws AuthenticationException {
    // Hash password for comparison
    String passwordHash = PasswordUtil.hash(password);

    // Query database
    User user = userRepository.findByUsername(username);

    if (user == null || !user.getPasswordHash().equals(passwordHash)) {
      throw new AuthenticationException("Invalid credentials");
    }

    // Generate JWT token with 1-hour expiration
    String token = Jwts.builder()
        .setSubject(String.valueOf(user.getId()))
        .setExpiration(new Date(System.currentTimeMillis() + TimeUnit.HOURS.toMillis(TOKEN_EXPIRY_HOURS)))
        .signWith(SignatureAlgorithm.HS256, SECRET_KEY)
        .compact();

    return new AuthResponse(token, new Date(System.currentTimeMillis() + TimeUnit.HOURS.toMillis(TOKEN_EXPIRY_HOURS)));
  }
}
```

---

## Testing Code Examples

For technical books, include test examples:

### Python (pytest)

```python
def test_authenticate_user_success():
    """Test successful authentication."""
    response = authenticate_user("alice", "correct_password")
    assert "token" in response
    assert response["expires_at"] > datetime.utcnow()


def test_authenticate_user_invalid_password():
    """Test authentication with wrong password."""
    with pytest.raises(AuthenticationError):
        authenticate_user("alice", "wrong_password")
```

### JavaScript (Jest)

```javascript
describe('authenticateUser', () => {
  it('returns token for valid credentials', async () => {
    const response = await authenticateUser('alice', 'correct_password');
    expect(response).toHaveProperty('token');
    expect(response.expiresAt).toBeInstanceOf(Date);
  });

  it('throws error for invalid password', async () => {
    await expect(authenticateUser('alice', 'wrong_password')).rejects.toThrow(AuthenticationError);
  });
});
```

---

## Official Style Guide Links

- **Python PEP 8**: https://peps.python.org/pep-0008/
- **JavaScript Airbnb**: https://github.com/airbnb/javascript
- **Java Google**: https://google.github.io/styleguide/javaguide.html
- **TypeScript**: https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html
- **Go**: https://go.dev/doc/effective_go
- **Rust**: https://doc.rust-lang.org/book/appendix-07-syntax-guide.html
- **C#**: https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions

Always check official documentation for your target language version.

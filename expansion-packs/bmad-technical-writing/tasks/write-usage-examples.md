<!-- Powered by BMAD™ Core -->

# Write Usage Examples

---

task:
id: write-usage-examples
name: Write Usage Examples
description: Create comprehensive usage examples for API functions including basic, advanced, and edge case scenarios
persona_default: api-documenter
inputs:
  - api-function (function name or API endpoint to demonstrate)
  - context (optional: book chapter, API section, tutorial level)
  - language (programming language for examples)
steps:
  - Identify function purpose and common use cases
  - Create basic usage example (simplest valid usage)
  - Create intermediate example (real-world scenario)
  - Create advanced example (complex configuration or chaining)
  - Add edge case examples (error handling, boundary conditions)
  - Include expected output for each example
  - Add explanatory comments to clarify non-obvious code
  - Ensure all examples are runnable and tested
output: Complete set of usage examples ready for documentation or book content

---

## Purpose

This task helps you create clear, comprehensive usage examples that demonstrate how to use an API function or library feature. Good examples accelerate learning, reduce support questions, and showcase best practices.

## Prerequisites

Before starting this task:

- Function or API is documented (or use `document-function.md` first)
- Understanding of function parameters and behavior
- Access to working environment for testing examples
- Knowledge of target audience skill level

## Example Categories

### 1. Basic Usage Example

**Purpose:** Show simplest possible valid usage

**Characteristics:**

- Minimal parameters
- Default options
- Clear, obvious use case
- No error handling (unless critical)
- 3-10 lines of code

**Template:**

```javascript
// Basic usage: [what this demonstrates]
const result = functionName(simpleArg);
console.log(result); // Expected output
```

### 2. Intermediate/Real-World Example

**Purpose:** Show practical, production-like usage

**Characteristics:**

- Realistic scenario
- Some configuration options
- Common patterns
- Basic error handling
- 10-25 lines of code

**Template:**

```javascript
// Real-world usage: [scenario description]
try {
  const result = functionName(arg1, {
    option1: value1,
    option2: value2,
  });

  // Do something with result
  processResult(result);
} catch (error) {
  console.error('Operation failed:', error.message);
}
```

### 3. Advanced Example

**Purpose:** Show complex or powerful usage patterns

**Characteristics:**

- Multiple features combined
- Advanced configuration
- Chaining or composition
- Performance optimizations
- 25-50 lines of code

**Template:**

```javascript
// Advanced usage: [complex scenario]
const config = {
  advanced_option_1: value,
  advanced_option_2: value,
  callbacks: {
    onProgress: (progress) => console.log(`${progress}%`),
    onComplete: (result) => handleCompletion(result),
  },
};

const pipeline = functionName(data, config).then(transform).then(validate).catch(handleError);
```

### 4. Edge Case Examples

**Purpose:** Show error handling and boundary conditions

**Characteristics:**

- Error scenarios
- Empty/null inputs
- Maximum/minimum values
- Timeout handling
- Concurrent usage

**Template:**

```javascript
// Edge case: [specific scenario]
try {
  const result = functionName(edgeCaseInput);
} catch (SpecificError) {
  // Handle expected error
} catch (UnexpectedError) {
  // Handle unexpected error
}
```

## Workflow Steps

### 1. Identify Function Purpose and Use Cases

Brainstorm common scenarios where function is used:

**Example: `fetchUser(userId, options)` function**

**Common use cases:**

- Fetch user by ID (basic)
- Fetch user with specific fields (optimization)
- Fetch deleted user (admin feature)
- Handle user not found (error case)
- Batch fetch multiple users (advanced)

### 2. Create Basic Usage Example

Write simplest valid usage:

**Example:**

```javascript
// Basic usage: Fetch a user by ID
const user = await fetchUser('507f1f77bcf86cd799439011');
console.log(user.email);
// Output: 'john.doe@example.com'
```

**Guidelines:**

- One clear purpose stated in comment
- Minimal code
- Show expected output
- No error handling (unless function requires it)

### 3. Create Intermediate Example

Write realistic production scenario:

**Example:**

```javascript
// Real-world usage: Display user profile with error handling
async function displayUserProfile(userId) {
  try {
    // Fetch only needed fields for performance
    const user = await fetchUser(userId, {
      fields: ['email', 'profile.name', 'profile.avatar'],
    });

    if (user) {
      console.log(`Name: ${user.profile.name}`);
      console.log(`Email: ${user.email}`);
      console.log(`Avatar: ${user.profile.avatar}`);
    } else {
      console.log('User not found');
    }
  } catch (error) {
    console.error('Failed to fetch user:', error.message);
  }
}

displayUserProfile('507f1f77bcf86cd799439011');
// Output:
// Name: John Doe
// Email: john.doe@example.com
// Avatar: https://example.com/avatars/john.jpg
```

**Guidelines:**

- Wrapped in function showing context
- Error handling included
- Comments explain key decisions
- Shows result processing

### 4. Create Advanced Example

Write complex scenario combining features:

**Example:**

```javascript
// Advanced usage: Batch fetch users with caching and retry logic
class UserService {
  constructor() {
    this.cache = new Map();
  }

  async fetchUsers(userIds, options = {}) {
    const { useCache = true, maxRetries = 3, onProgress = null } = options;

    const results = [];
    const uncachedIds = [];

    // Check cache first
    for (const userId of userIds) {
      if (useCache && this.cache.has(userId)) {
        results.push(this.cache.get(userId));
      } else {
        uncachedIds.push(userId);
      }
    }

    // Fetch uncached users with retry logic
    for (let i = 0; i < uncachedIds.length; i++) {
      const userId = uncachedIds[i];
      let retries = 0;
      let user = null;

      while (retries < maxRetries) {
        try {
          user = await fetchUser(userId, {
            fields: options.fields,
            includeDeleted: options.includeDeleted,
          });

          if (useCache && user) {
            this.cache.set(userId, user);
          }
          break;
        } catch (error) {
          retries++;
          if (retries === maxRetries) {
            console.error(`Failed to fetch user ${userId} after ${maxRetries} retries`);
          } else {
            await new Promise((resolve) => setTimeout(resolve, 1000 * retries));
          }
        }
      }

      if (user) results.push(user);

      if (onProgress) {
        onProgress({
          current: i + 1,
          total: uncachedIds.length,
          percentage: Math.round(((i + 1) / uncachedIds.length) * 100),
        });
      }
    }

    return results;
  }
}

// Usage
const service = new UserService();
const users = await service.fetchUsers(['id1', 'id2', 'id3', 'id4', 'id5'], {
  useCache: true,
  maxRetries: 3,
  fields: ['email', 'profile.name'],
  onProgress: (progress) => {
    console.log(`Fetching users: ${progress.percentage}% complete`);
  },
});

console.log(`Fetched ${users.length} users`);
// Output:
// Fetching users: 20% complete
// Fetching users: 40% complete
// Fetching users: 60% complete
// Fetching users: 80% complete
// Fetching users: 100% complete
// Fetched 5 users
```

**Guidelines:**

- Shows architectural pattern
- Combines multiple features
- Demonstrates best practices
- Includes performance considerations
- Well-commented

### 5. Add Edge Case Examples

Cover error scenarios and boundaries:

**Example 1: Handle user not found**

```javascript
// Edge case: User not found
try {
  const user = await fetchUser('nonexistent-id', { strict: true });
} catch (NotFoundError) {
  console.error('User does not exist');
  // Fallback to default user or show error message
}
```

**Example 2: Invalid input validation**

```javascript
// Edge case: Invalid user ID format
try {
  const user = await fetchUser('invalid-format');
} catch (ValidationError) {
  console.error('Invalid user ID format. Must be 24-character hex string.');
}
```

**Example 3: Handle empty results**

```javascript
// Edge case: Fetch user with no data
const user = await fetchUser('507f1f77bcf86cd799439011');
if (!user) {
  console.log('User not found or deleted');
  // Handle gracefully
}
```

**Example 4: Timeout handling**

```javascript
// Edge case: Request timeout
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

try {
  const user = await fetchUser('507f1f77bcf86cd799439011', {
    signal: controller.signal,
  });
  clearTimeout(timeoutId);
  console.log('User fetched:', user.email);
} catch (error) {
  if (error.name === 'AbortError') {
    console.error('Request timed out after 5 seconds');
  }
}
```

### 6. Include Expected Output

Show what each example produces:

**Good - Shows actual output:**

```javascript
const user = await fetchUser('507f...');
console.log(user.email);
// Output: 'john.doe@example.com'
```

**Better - Shows output structure:**

```javascript
const user = await fetchUser('507f...');
console.log(JSON.stringify(user, null, 2));
// Output:
// {
//   "id": "507f1f77bcf86cd799439011",
//   "email": "john.doe@example.com",
//   "profile": {
//     "name": "John Doe",
//     "avatar": "https://example.com/avatars/john.jpg"
//   }
// }
```

### 7. Add Explanatory Comments

Clarify non-obvious code:

**Example:**

```javascript
// Fetch user with field selection to minimize data transfer
const user = await fetchUser(userId, {
  fields: ['email', 'profile.name'], // Only fetch needed fields
});

// Cache result for 5 minutes to reduce database load
cache.set(userId, user, { ttl: 300 });

// Use optional chaining to safely access nested properties
const userName = user?.profile?.name ?? 'Unknown User';
```

**Guidelines:**

- Explain _why_, not _what_ (code shows what)
- Clarify performance implications
- Note security considerations
- Explain non-standard patterns

### 8. Ensure Examples Are Runnable

Test all examples:

**Checklist:**

- [ ] Example can run without modification
- [ ] All required imports/dependencies included
- [ ] No undefined variables
- [ ] Outputs match stated expectations
- [ ] Error cases actually trigger errors as shown

**Complete runnable example:**

```javascript
// Complete runnable example
import { fetchUser } from './api/users.js';

async function example() {
  try {
    // Basic usage
    const user = await fetchUser('507f1f77bcf86cd799439011');
    console.log('User email:', user.email);

    // With options
    const userWithFields = await fetchUser('507f1f77bcf86cd799439011', {
      fields: ['email', 'profile.name'],
    });
    console.log('User name:', userWithFields.profile.name);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

example();
```

## Success Criteria

Usage examples are complete when:

- [ ] Basic example shows simplest valid usage
- [ ] Intermediate example shows realistic scenario
- [ ] Advanced example demonstrates complex patterns
- [ ] Edge cases covered (errors, boundaries)
- [ ] All examples include expected output
- [ ] Non-obvious code is commented
- [ ] All examples are tested and runnable
- [ ] Examples progress from simple to complex
- [ ] Examples are relevant to target audience

## Output Format

Organize examples with clear headers and context:

```markdown
## Usage Examples

### Basic Usage

[Simple example with description]

### Common Use Cases

#### Fetching with Specific Fields

[Intermediate example]

#### Batch Operations

[Another intermediate example]

### Advanced Patterns

#### Custom Caching Strategy

[Advanced example]

#### Error Recovery with Retry Logic

[Advanced example]

### Error Handling

#### Handle User Not Found

[Edge case example]

#### Validate Input

[Edge case example]

#### Timeout Management

[Edge case example]
```

## Language-Specific Considerations

### JavaScript/TypeScript

**Include:**

- Async/await usage
- Promise chaining alternative
- Error handling (try/catch)
- Type annotations (TypeScript)

```javascript
// TypeScript example
const user: User = await fetchUser('507f...');

// Promise chaining alternative
fetchUser('507f...')
  .then(user => console.log(user.email))
  .catch(error => console.error(error));
```

### Python

**Include:**

- Type hints
- Context managers where relevant
- Exception handling
- List comprehensions for data processing

```python
# Type-annotated example
from typing import Optional
from models import User

user: Optional[User] = fetch_user('507f...')
if user:
    print(f"Email: {user.email}")
```

### Ruby

**Include:**

- Block syntax
- Symbol vs string keys
- Idiomatic Ruby patterns
- Exception handling

```ruby
# Idiomatic Ruby example
user = fetch_user('507f...') do |config|
  config.fields = [:email, :profile]
  config.cache_ttl = 300
end

puts user.email if user
```

### Go

**Include:**

- Error handling pattern
- Struct initialization
- Defer statements
- Context usage

```go
// Idiomatic Go example
ctx := context.Background()
user, err := fetchUser(ctx, "507f...")
if err != nil {
    log.Printf("Failed to fetch user: %v", err)
    return
}

fmt.Printf("Email: %s\n", user.Email)
```

## Common Pitfalls to Avoid

**❌ Examples that can't run:**

```javascript
const user = fetchUser(userId); // Where is userId defined?
```

✅ **Better:**

```javascript
const user = await fetchUser('507f1f77bcf86cd799439011');
```

**❌ No context or explanation:**

```javascript
const user = await fetchUser(id, { fields: ['a', 'b'], cache: true });
```

✅ **Better:**

```javascript
// Fetch only email and name fields to reduce data transfer
const user = await fetchUser('507f1f77bcf86cd799439011', {
  fields: ['email', 'profile.name'],
  cache: true, // Cache for 5 minutes
});
```

**❌ No expected output:**

```javascript
const user = await fetchUser('507f...');
console.log(user);
```

✅ **Better:**

```javascript
const user = await fetchUser('507f...');
console.log(user.email);
// Output: 'john.doe@example.com'
```

**❌ Mixing multiple concepts:**

```javascript
// Confusing example mixing validation, caching, and batch operations
```

✅ **Better:**

```javascript
// Example 1: Validation
// Example 2: Caching
// Example 3: Batch operations (combines previous concepts)
```

## Examples

### Example Set 1: REST API Client

**Function:** `apiClient.get(endpoint, options)`

**Basic:**

```javascript
// Basic usage: Fetch users list
const response = await apiClient.get('/users');
console.log(response.data);
// Output: [{ id: 1, name: 'John' }, { id: 2, name: 'Jane' }]
```

**Intermediate:**

```javascript
// Real-world usage: Fetch with query parameters and headers
const response = await apiClient.get('/users', {
  params: {
    page: 1,
    limit: 10,
    role: 'admin',
  },
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

console.log(`Fetched ${response.data.length} admin users`);
// Output: Fetched 3 admin users
```

**Advanced:**

```javascript
// Advanced usage: Pagination with automatic retry and caching
class UserFetcher {
  async fetchAllUsers(options = {}) {
    const users = [];
    let page = 1;
    let hasMore = true;

    const fetchOptions = {
      headers: { Authorization: `Bearer ${options.token}` },
      retry: {
        attempts: 3,
        delay: 1000,
      },
      cache: {
        enabled: true,
        ttl: 300,
      },
    };

    while (hasMore) {
      try {
        const response = await apiClient.get('/users', {
          ...fetchOptions,
          params: {
            page,
            limit: options.pageSize || 50,
            ...options.filters,
          },
        });

        users.push(...response.data);

        // Check if more pages exist
        hasMore = response.data.length === (options.pageSize || 50);
        page++;

        if (options.onProgress) {
          options.onProgress({ page, total: users.length });
        }
      } catch (error) {
        console.error(`Failed on page ${page}:`, error.message);

        if (options.continueOnError) {
          page++;
          continue;
        }

        throw error;
      }
    }

    return users;
  }
}

// Usage
const fetcher = new UserFetcher();
const allUsers = await fetcher.fetchAllUsers({
  token: process.env.API_TOKEN,
  pageSize: 100,
  filters: { role: 'admin', active: true },
  continueOnError: true,
  onProgress: ({ page, total }) => {
    console.log(`Fetched page ${page}, total users: ${total}`);
  },
});

console.log(`Total users fetched: ${allUsers.length}`);
```

**Edge Cases:**

```javascript
// Edge case: Handle 404 Not Found
try {
  const response = await apiClient.get('/users/nonexistent-id');
} catch (error) {
  if (error.status === 404) {
    console.log('User not found');
  }
}

// Edge case: Handle rate limiting
try {
  const response = await apiClient.get('/users');
} catch (error) {
  if (error.status === 429) {
    const retryAfter = error.headers['retry-after'];
    console.log(`Rate limited. Retry after ${retryAfter} seconds`);
  }
}

// Edge case: Timeout
const response = await apiClient.get('/users', {
  timeout: 5000, // 5 second timeout
});
```

## Next Steps

After creating usage examples:

1. Test all examples in isolated environment
2. Add examples to function documentation
3. Include examples in book chapter or tutorial
4. Create runnable sample code repository
5. Use `organize-code-repo.md` to structure examples
6. Add examples to API reference documentation
7. Consider creating video walkthrough for complex examples

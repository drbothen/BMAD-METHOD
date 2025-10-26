<!-- Powered by BMAD™ Core -->

# Optimize Code

---

task:
id: optimize-code
name: Optimize Code
description: Improve code clarity, readability, and efficiency for technical documentation
persona_default: code-curator
inputs:

- code_path (file or directory containing code to optimize)
- optimization_goals (clarity|performance|both)
- target_audience (beginner|intermediate|advanced)
  steps:
- Read and analyze existing code
- Identify optimization opportunities based on goals
- For clarity optimizations, improve naming, comments, structure, and readability
- For performance optimizations, improve algorithms, data structures, and efficiency
- Create before/after examples with annotations
- Explain rationale for each optimization
- Include performance benchmarks if applicable
- Run execute-checklist.md with code-quality-checklist.md
- Generate optimization recommendations report
  output: docs/optimization/{{code-name}}-optimization-report.md

---

## Purpose

This task improves code examples for technical books by optimizing for clarity (teaching effectiveness) and/or performance (demonstrating best practices). Code in technical documentation serves a different purpose than production code—it must be exceptionally clear, well-explained, and demonstrate best practices while remaining concise enough to include in a book.

## Prerequisites

Before starting this task:

- Code examples have been created
- Optimization goals defined (clarity, performance, or both)
- Target audience identified (affects complexity choices)
- code-quality-checklist.md available
- code-style-guides.md knowledge base accessible

## Workflow Steps

### 1. Analyze Existing Code

Read and understand the code thoroughly:

**Initial Analysis Checklist:**

- [ ] What does this code do? (purpose)
- [ ] What concepts does it teach? (learning objectives)
- [ ] Who is the audience? (skill level)
- [ ] What is the code's current complexity? (basic/intermediate/advanced)
- [ ] Are there obvious issues? (bugs, anti-patterns, inefficiencies)
- [ ] Does it follow language conventions? (style guide compliance)

**Code Quality Assessment:**

Rate current code on each dimension (1-5 scale):

- **Clarity**: Are variable/function names descriptive?
- **Readability**: Is the structure easy to follow?
- **Comments**: Do comments explain WHY, not WHAT?
- **Simplicity**: Is this the simplest approach?
- **Correctness**: Does it work correctly?
- **Efficiency**: Are there obvious performance issues?
- **Maintainability**: Could someone easily modify this?

### 2. Identify Optimization Opportunities

Based on optimization goals, find improvements:

#### Clarity Optimizations (Priority for Technical Books)

**A. Naming Improvements**

❌ **Poor Naming:**

```python
def calc(a, b, c):
    r = a + b * c
    return r
```

✅ **Clear Naming:**

```python
def calculate_total_price(base_price, quantity, tax_rate):
    total = base_price + (quantity * tax_rate)
    return total
```

**Naming Checklist:**

- [ ] Variables: Descriptive nouns (user_count, not uc)
- [ ] Functions: Verb phrases (calculate_total, not calc)
- [ ] Classes: Nouns (CustomerAccount, not CA)
- [ ] Constants: UPPER_SNAKE_CASE (MAX_CONNECTIONS)
- [ ] Booleans: is/has/can prefix (is_valid, has_permission)

**B. Comment Improvements**

❌ **Bad Comments (explain WHAT):**

```javascript
// Increment counter
counter++;

// Loop through array
for (let i = 0; i < items.length; i++) {
```

✅ **Good Comments (explain WHY):**

```javascript
// Track retry attempts for exponential backoff calculation
retryCount++;

// Process items sequentially to maintain insertion order
for (let i = 0; i < items.length; i++) {
```

**Comment Guidelines:**

- Explain design decisions and tradeoffs
- Highlight non-obvious logic
- Warn about gotchas or edge cases
- Link to relevant documentation
- Don't explain obvious syntax

**C. Simplify Complex Expressions**

❌ **Complex Expression:**

```python
result = data[0] if len(data) > 0 and data[0] is not None and data[0].value > 0 else default_value
```

✅ **Simplified with Explanatory Variables:**

```python
has_data = len(data) > 0
first_item_valid = data[0] is not None
has_positive_value = data[0].value > 0

result = data[0] if has_data and first_item_valid and has_positive_value else default_value
```

**D. Extract Magic Numbers to Constants**

❌ **Magic Numbers:**

```java
if (age >= 18 && score > 75) {
    timeout = 3600;
}
```

✅ **Named Constants:**

```java
private static final int ADULT_AGE = 18;
private static final int PASSING_SCORE = 75;
private static final int SESSION_TIMEOUT_SECONDS = 3600;

if (age >= ADULT_AGE && score > PASSING_SCORE) {
    timeout = SESSION_TIMEOUT_SECONDS;
}
```

**E. Break Long Functions into Smaller Pieces**

❌ **Long Function (hard to understand):**

```python
def process_order(order):
    # Validate order (20 lines)
    # Calculate prices (15 lines)
    # Apply discounts (25 lines)
    # Process payment (30 lines)
    # Send confirmation (10 lines)
    # Update inventory (15 lines)
```

✅ **Broken into Single-Responsibility Functions:**

```python
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    discounted_total = apply_discounts(order, total)
    payment_result = process_payment(order, discounted_total)
    send_confirmation_email(order, payment_result)
    update_inventory(order)
```

#### Performance Optimizations

**A. Improve Algorithm Efficiency**

❌ **Inefficient Algorithm (O(n²)):**

```javascript
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}
```

✅ **Optimized Algorithm (O(n)):**

```javascript
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();

  for (const item of arr) {
    if (seen.has(item)) {
      duplicates.add(item);
    } else {
      seen.add(item);
    }
  }

  return Array.from(duplicates);
}
```

**Performance Impact:** O(n²) → O(n), significant improvement for large arrays

**B. Optimize Data Structures**

❌ **Inefficient Data Structure:**

```python
# Checking membership in list is O(n)
allowed_users = ["alice", "bob", "charlie", ...]  # 10,000 users

if username in allowed_users:  # O(n) lookup
    grant_access()
```

✅ **Optimized Data Structure:**

```python
# Checking membership in set is O(1)
allowed_users = {"alice", "bob", "charlie", ...}  # 10,000 users

if username in allowed_users:  # O(1) lookup
    grant_access()
```

**Performance Impact:** O(n) → O(1) for lookups

**C. Cache Repeated Calculations**

❌ **Repeated Calculations:**

```python
def calculate_discount(items):
    total = sum(item.price for item in items)

    if sum(item.price for item in items) > 100:  # Calculated again
        discount = sum(item.price for item in items) * 0.1  # And again
        return sum(item.price for item in items) - discount  # And again
```

✅ **Cached Calculation:**

```python
def calculate_discount(items):
    total = sum(item.price for item in items)

    if total > 100:
        discount = total * 0.1
        return total - discount

    return total
```

**D. Reduce Unnecessary Operations**

❌ **Unnecessary Operations:**

```javascript
function processUsers(users) {
  // Creates intermediate arrays at each step
  return users
    .filter((user) => user.active)
    .map((user) => user.id)
    .filter((id) => id > 1000)
    .map((id) => ({ userId: id }));
}
```

✅ **Combined Operations:**

```javascript
function processUsers(users) {
  // Single pass through array
  return users.filter((user) => user.active && user.id > 1000).map((user) => ({ userId: user.id }));
}
```

### 3. Create Before/After Examples

Document each optimization with examples:

**Before/After Template:**

````markdown
## Optimization: [Name of Optimization]

### Before (Original Code)

```[language]
[original code with issues highlighted]
```
````

**Issues:**

- Issue 1: [description]
- Issue 2: [description]

### After (Optimized Code)

```[language]
[improved code with changes highlighted]
```

**Improvements:**

- Improvement 1: [description]
- Improvement 2: [description]

### Rationale

[Explain WHY this optimization was made, what tradeoffs were considered, and when this pattern should be used]

### Performance Impact (if applicable)

- **Before:** [benchmark results]
- **After:** [benchmark results]
- **Improvement:** [percentage or absolute improvement]

````

**Example:**

```markdown
## Optimization: Replace Nested Loops with Hash Set

### Before (Original Code)

```python
def find_common_elements(list1, list2):
    common = []
    for item1 in list1:  # O(n)
        for item2 in list2:  # O(m)
            if item1 == item2:
                common.append(item1)
    return common
````

**Issues:**

- Time complexity: O(n × m) - quadratic time
- Performance degrades significantly with large lists
- Duplicate handling not addressed

### After (Optimized Code)

```python
def find_common_elements(list1, list2):
    # Convert to set for O(1) lookups
    set2 = set(list2)

    # Single pass through list1
    common = []
    for item in list1:
        if item in set2:
            common.append(item)

    # Alternative: one-liner using set intersection
    # return list(set(list1) & set(list2))

    return common
```

**Improvements:**

- Time complexity: O(n + m) - linear time
- Scales well to large datasets
- Naturally handles duplicates via set

### Rationale

For finding common elements, set intersection is the optimal approach. We convert one list to a set (O(m)), then check membership for each element in the other list (O(n)). This is dramatically faster than nested loops for large datasets.

**Tradeoff:** Uses O(m) extra space for the set, but time savings justify space cost for most use cases.

**When to use:** Anytime you're checking if items from one collection exist in another collection.

### Performance Impact

**Benchmark:** 10,000 elements in each list

- **Before:** 2.47 seconds
- **After:** 0.003 seconds
- **Improvement:** 823x faster

````

### 4. Explain Rationale for Each Change

For every optimization, document:

**1. What Changed?**
- Specific lines/sections modified
- Nature of the change (algorithm, structure, naming, etc.)

**2. Why Was This Changed?**
- What problem did it solve?
- What was wrong with the original?
- What principle does this follow?

**3. When Should This Pattern Be Used?**
- In what situations is this optimization appropriate?
- When might the original approach be acceptable?
- Are there cases where this optimization would be wrong?

**4. What Are the Tradeoffs?**
- Does this use more memory?
- Is it more complex?
- Does it have edge cases?
- Is it less flexible?

### 5. Include Performance Benchmarks (If Applicable)

For performance optimizations, provide evidence:

**Benchmarking Approach:**

```python
import time

def benchmark(func, iterations=10000):
    start = time.time()
    for _ in range(iterations):
        func()
    end = time.time()
    return end - start

# Test both implementations
original_time = benchmark(original_function)
optimized_time = benchmark(optimized_function)

print(f"Original: {original_time:.4f}s")
print(f"Optimized: {optimized_time:.4f}s")
print(f"Improvement: {original_time / optimized_time:.2f}x faster")
````

**Benchmark Report Template:**

```markdown
### Performance Benchmarks

**Test Configuration:**

- Dataset Size: [size]
- Iterations: [count]
- Platform: [OS, CPU]
- Language Version: [version]

**Results:**

| Implementation | Time (ms) | Memory (MB) | Improvement |
| -------------- | --------- | ----------- | ----------- |
| Original       | 2,470     | 12.5        | Baseline    |
| Optimized      | 3         | 18.2        | 823x faster |

**Analysis:**
The optimized version is 823x faster despite using 45% more memory. For technical book examples, this demonstrates the classic time-space tradeoff and is worth the memory cost.
```

### 6. Run Code-Quality Checklist

Execute checklist validation:

```bash
# Using execute-checklist.md task
execute-checklist code-quality-checklist.md
```

Ensure optimized code:

- [ ] Follows language-specific style guide
- [ ] Uses descriptive naming
- [ ] Has appropriate comments
- [ ] Is DRY (no repetition)
- [ ] Has proper error handling
- [ ] Is testable
- [ ] Is maintainable
- [ ] Demonstrates best practices

### 7. Generate Optimization Report

Create comprehensive optimization documentation:

**Optimization Report Template:**

```markdown
# Code Optimization Report: [Code Name]

**Optimization Date:** [date]
**Optimization Goal:** [clarity|performance|both]
**Target Audience:** [beginner|intermediate|advanced]
**Optimized By:** code-curator agent

## Summary

**Total Optimizations:** [count]

- Clarity Improvements: [count]
- Performance Improvements: [count]

**Overall Impact:**

- Readability: [1-5] → [1-5] ([improvement]% improvement)
- Performance: [baseline] → [optimized] ([improvement]x faster)

## Optimizations Applied

### 1. [Optimization Name]

[Before/After with rationale - use template from Step 3]

### 2. [Optimization Name]

[Before/After with rationale]

[... continue for all optimizations]

## Code Quality Checklist Results

[Results from code-quality-checklist.md]

## Recommendations

### For This Code

1. [Specific recommendation]
2. [Specific recommendation]

### For Book/Documentation

1. [How to integrate these improvements]
2. [What to teach readers about these patterns]

## Next Steps

1. Review optimizations with technical reviewer
2. Update code repository
3. Integrate optimizations into chapter narrative
4. Add explanatory sidebars for key optimizations
5. Create exercises based on optimization patterns
```

## Success Criteria

Code optimization is complete when:

- [ ] All code analyzed for optimization opportunities
- [ ] Optimization goals (clarity/performance) achieved
- [ ] Before/after examples created for each optimization
- [ ] Rationale documented for every change
- [ ] Performance benchmarks included (if applicable)
- [ ] Tradeoffs clearly explained
- [ ] code-quality-checklist.md completed
- [ ] Optimization report generated
- [ ] Optimized code tested and working
- [ ] Code is more readable/efficient than original

## Common Pitfalls to Avoid

- **Over-optimization**: Don't sacrifice clarity for minor performance gains in teaching code
- **Premature optimization**: Focus on clarity first, performance second
- **Clever code**: Avoid "clever" tricks that confuse readers
- **Missing benchmarks**: Always measure before claiming performance improvements
- **Breaking functionality**: Ensure optimizations don't introduce bugs
- **Ignoring audience**: Beginner code should prioritize clarity over efficiency
- **No explanation**: Every optimization needs rationale documented
- **Incomplete testing**: Test optimized code thoroughly

## Optimization Priorities by Audience

### Beginner Audience

**Priority Order:**

1. **Clarity** (most important)
2. **Simplicity**
3. **Correctness**
4. **Performance** (least important, unless demonstrating concept)

**Guidelines:**

- Favor explicit over implicit
- Use longer, descriptive names
- Add more explanatory comments
- Prefer simple algorithms even if slower
- Break into smaller functions
- Avoid advanced language features

### Intermediate Audience

**Priority Order:**

1. **Clarity**
2. **Performance**
3. **Best Practices**
4. **Sophistication**

**Guidelines:**

- Balance clarity and efficiency
- Demonstrate idiomatic patterns
- Use appropriate language features
- Show common optimizations
- Explain tradeoffs

### Advanced Audience

**Priority Order:**

1. **Performance**
2. **Best Practices**
3. **Sophistication**
4. **Clarity** (still important, but audience can handle complexity)

**Guidelines:**

- Show production-quality code
- Demonstrate advanced patterns
- Include comprehensive error handling
- Use optimal algorithms and data structures
- Explain complex optimizations

## Optimization Pattern Catalog

Common optimization patterns for technical books:

### Pattern: Extract Method

**When:** Function > 20 lines or does multiple things

**Before:**

```python
def process_order(order):
    # 50 lines of validation, calculation, payment, email
```

**After:**

```python
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    charge_payment(order, total)
    send_confirmation(order)
```

### Pattern: Replace Loop with Built-in

**When:** Manual iteration can be replaced with language built-ins

**Before:**

```python
total = 0
for item in items:
    total += item.price
```

**After:**

```python
total = sum(item.price for item in items)
```

### Pattern: Early Return

**When:** Deep nesting can be flattened

**Before:**

```javascript
function processUser(user) {
  if (user) {
    if (user.active) {
      if (user.hasPermission) {
        // actual logic
      }
    }
  }
}
```

**After:**

```javascript
function processUser(user) {
  if (!user) return;
  if (!user.active) return;
  if (!user.hasPermission) return;

  // actual logic (not nested)
}
```

### Pattern: Use Descriptive Temporary Variables

**When:** Complex condition or calculation appears multiple times

**Before:**

```python
if user.age >= 18 and user.hasID and user.passedTest:
    # do something
elif user.age >= 18 and user.hasID:
    # do something else
```

**After:**

```python
is_adult = user.age >= 18
has_identification = user.hasID
passed_exam = user.passedTest
is_fully_qualified = is_adult and has_identification and passed_exam

if is_fully_qualified:
    # do something
elif is_adult and has_identification:
    # do something else
```

## Profiling Tools by Language

Use these tools to identify performance bottlenecks:

**Python:**

- cProfile (built-in profiler)
- line_profiler (line-by-line timing)
- memory_profiler (memory usage)

**JavaScript/Node:**

- Chrome DevTools Profiler
- Node.js --prof flag
- clinic.js (performance diagnostics)

**Java:**

- JProfiler
- VisualVM
- Java Flight Recorder

**Go:**

- pprof (built-in profiler)
- go tool trace

**Ruby:**

- ruby-prof
- stackprof

## Next Steps

After code optimization:

1. Review optimizations with technical expert
2. Update code repository with optimized versions
3. Integrate optimization explanations into chapter narrative
4. Create "Optimization Spotlight" sidebars for key patterns
5. Design exercises where readers apply optimization patterns
6. Add performance comparison diagrams if significant improvements
7. Update code examples in documentation

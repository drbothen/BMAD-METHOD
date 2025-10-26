# Section 3.1: List Basics - Creating and Accessing Lists

<!-- Agent: tutorial-architect -->
<!-- Task: write-section-draft.md -->
<!-- Status: Final (after review and revisions) -->
<!-- Sprint 7 Feature: ⭐ This section was written using write-section-draft.md task -->

## Learning Objectives

By the end of this section, you will be able to:

1. Create lists using various methods (literal notation, `list()` constructor)
2. Access list elements using positive and negative indexing
3. Use slicing to extract sublists from lists
4. Understand and avoid common indexing errors

## What Are Lists?

Lists are one of Python's most fundamental and versatile data structures. A **list** is an ordered, mutable collection that can store multiple items of any data type. Think of a list as a container that:

- **Holds multiple items** in a specific order
- **Can be changed** after creation (add, remove, or modify items)
- **Remembers the order** of items (first item stays first unless you change it)
- **Allows duplicates** (can have the same value multiple times)

Lists are perfect for storing collections like shopping items, student names, test scores, or any group of related data.

## Creating Lists

### List Literal Notation

The most common way to create a list is using square brackets `[]`:

```python
# List of numbers
numbers = [1, 2, 3, 4, 5]

# List of strings
fruits = ["apple", "banana", "cherry"]

# List with mixed data types
mixed = [1, "hello", 3.14, True]

# Empty list
empty_list = []
```

**Notice:** Lists can contain different types of data in the same list. Python doesn't require all elements to be the same type, though it's often clearer when they are.

### Using the list() Constructor

You can also create lists using the `list()` constructor function:

```python
# Create list from a string (each character becomes an element)
from_string = list("Python")
print(from_string)  # ['P', 'y', 't', 'h', 'o', 'n']

# Create list from another iterable
from_range = list(range(1, 6))
print(from_range)  # [1, 2, 3, 4, 5]
```

**When to use which:**
- Use `[]` for most cases - it's simpler and more readable
- Use `list()` when converting other data types to lists

## Accessing List Elements

### Positive Indexing (0-Based)

Python uses **zero-based indexing**, meaning the first element is at index 0:

```python
fruits = ["apple", "banana", "cherry"]

first_fruit = fruits[0]      # "apple"
second_fruit = fruits[1]     # "banana"
third_fruit = fruits[2]      # "cherry"
```

**Visual representation:**

```
Index:    0         1          2
        ┌─────────┬──────────┬────────┐
fruits  │ "apple" │ "banana" │ "cherry" │
        └─────────┴──────────┴────────┘
```

### Negative Indexing (From the End)

Python also supports negative indices, which count from the end of the list:

```python
fruits = ["apple", "banana", "cherry"]

last_fruit = fruits[-1]       # "cherry"
second_last = fruits[-2]      # "banana"
first_again = fruits[-3]      # "apple"
```

**Visual representation:**

```
Negative: -3        -2         -1
Positive:  0         1          2
        ┌─────────┬──────────┬────────┐
fruits  │ "apple" │ "banana" │ "cherry" │
        └─────────┴──────────┴────────┘
```

**Why use negative indexing?**
- Access the last element without knowing the list length
- More readable code when working from the end: `last = items[-1]` vs `last = items[len(items)-1]`

### Getting List Length

Use the `len()` function to find how many elements are in a list:

```python
fruits = ["apple", "banana", "cherry"]
count = len(fruits)  # 3
```

## Slicing Lists

**Slicing** lets you extract a portion of a list using the syntax `list[start:end]`:

```python
numbers = [1, 2, 3, 4, 5]

# Get elements from index 0 to 3 (3 is excluded!)
first_three = numbers[0:3]    # [1, 2, 3]

# Get elements from index 1 to 4
middle_three = numbers[1:4]   # [2, 3, 4]
```

**Key point:** The `end` index is **not included** in the slice. `numbers[0:3]` gets indices 0, 1, and 2.

### Omitting Start or End

You can omit the start or end index:

```python
numbers = [1, 2, 3, 4, 5]

# Omit start - goes from beginning
from_beginning = numbers[:3]  # [1, 2, 3]

# Omit end - goes to end of list
to_end = numbers[2:]          # [3, 4, 5]

# Omit both - copies entire list
copy = numbers[:]             # [1, 2, 3, 4, 5]
```

### Using Negative Indices in Slices

You can use negative indices in slices too:

```python
numbers = [1, 2, 3, 4, 5]

# Get last two elements
last_two = numbers[-2:]       # [4, 5]

# Get everything except last element
all_but_last = numbers[:-1]   # [1, 2, 3, 4]
```

### Slicing with Step

The full slice syntax is `list[start:end:step]`:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Get every other element
every_other = numbers[::2]    # [1, 3, 5, 7, 9]

# Get every third element
every_third = numbers[::3]    # [1, 4, 7, 10]

# Reverse a list (step of -1)
reversed_list = numbers[::-1] # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

## Common List Operations

### Checking Membership

Use the `in` operator to check if an element exists in a list:

```python
fruits = ["apple", "banana", "cherry"]

has_apple = "apple" in fruits        # True
has_orange = "orange" in fruits      # False
```

### Finding Element Position

Use the `index()` method to find where an element is located:

```python
fruits = ["apple", "banana", "cherry"]

position = fruits.index("banana")    # 1
```

**Warning:** `index()` raises a `ValueError` if the element isn't found. Always check with `in` first if unsure!

### Counting Occurrences

Use the `count()` method to count how many times an element appears:

```python
numbers = [1, 2, 2, 3, 2, 4, 2]
count_of_twos = numbers.count(2)     # 4
```

## Common Pitfalls to Avoid

### IndexError: List Index Out of Range

This happens when you try to access an index that doesn't exist:

```python
fruits = ["apple", "banana", "cherry"]

# This raises IndexError:
bad_access = fruits[10]  # Only indices 0-2 exist!
```

**Solution:** Always check the list length or use `in` operator to verify before accessing.

### Confusing Index with Element Value

Remember: the **index** is the position (0, 1, 2...), the **element** is the value stored ("apple", "banana"...).

```python
numbers = [10, 20, 30]

# numbers[0] returns 10 (element at index 0)
# NOT "get element numbered 0 from the list"
```

### Forgetting Slice End is Exclusive

```python
numbers = [1, 2, 3, 4, 5]

# numbers[0:3] gives [1, 2, 3]
# It does NOT include index 3!
```

**Memory aid:** Think `[start:end)` with the bracket facing away from `end` (not included).

## Practical Example

Let's put it all together with a practical example:

```python
# Student test scores
scores = [85, 92, 78, 95, 88, 76, 94, 89]

# Get first score
first_score = scores[0]  # 85

# Get last score
last_score = scores[-1]  # 89

# Get top 3 scores (after sorting - we'll learn this later!)
# For now, just slice the first 3
first_three_scores = scores[:3]  # [85, 92, 78]

# Check if perfect score exists
has_perfect = 100 in scores  # False

# Count how many 90+ scores (we'll learn better ways later)
count_90_plus = len([s for s in scores if s >= 90])  # 3

print(f"First score: {first_score}")
print(f"Last score: {last_score}")
print(f"Has perfect score: {has_perfect}")
```

## Transition to Next Section

Now that you know how to create lists and access their elements, you're ready to learn how to **modify** lists. In the next section, we'll explore list operations like adding, removing, and changing elements. The power of lists comes from their mutability - their ability to change - which we'll dive into next.

---

## Section Summary

**Key Concepts:**
- Lists are ordered, mutable collections
- Create lists with `[]` or `list()`
- Access elements with positive (0, 1, 2...) or negative (-1, -2, -3...) indices
- Slice lists with `[start:end:step]` syntax
- Use `in`, `index()`, and `count()` to work with list contents

**What's Next:**
In Section 3.2, you'll learn to modify lists by adding, removing, and changing elements.

---

<!-- Workflow metadata -->
<!-- Created: Section planning → Code examples → Draft → Review → Revisions → Final -->
<!-- Code examples: code/chapter-3/section-1/list_basics.py (tested ✅) -->
<!-- Review: reviews/section-1-review-notes.md -->
<!-- Checklist: checklists/section-1-checklist-results.md -->
<!-- Quality gate: Passed ✅ -->

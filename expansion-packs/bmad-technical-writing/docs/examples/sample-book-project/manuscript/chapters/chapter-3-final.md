# Chapter 3: Working with Lists and Tuples

<!-- Agent: tutorial-architect + technical-editor -->
<!-- Tasks: merge-sections.md → enhance-transitions.md → technical-review-chapter.md → copy-edit-chapter.md -->
<!-- Sprint 7 Features: ⭐ merge-sections.md, ⭐ enhance-transitions.md, ⭐ execute-checklist.md -->
<!-- Status: Final (ready for publication) -->

## Chapter Introduction

Welcome to Chapter 3! In this chapter, you'll master two of Python's fundamental sequence types: **lists** and **tuples**. These data structures are the foundation of almost every Python program you'll write.

**Why This Chapter Matters:**

Lists and tuples let you work with collections of data instead of individual values. Imagine trying to track 100 student scores using 100 separate variables - it would be a nightmare! Lists solve this problem elegantly. And when you need collections that can't be accidentally modified, tuples provide the safety of immutability.

**What You'll Learn:**

By the end of this chapter, you'll be able to:
- Create and access lists using various techniques
- Modify lists by adding, removing, and changing elements
- Understand when to use tuples instead of lists
- Choose the right sequence type for any programming task
- Apply lists and tuples to solve real-world problems

**Prerequisites:**

This chapter builds on concepts from Chapter 2 (Data Types), particularly the idea of mutability vs. immutability. You should be comfortable with:
- Variables and assignment
- Basic data types (int, str, bool)
- For loops and conditionals
- The difference between mutable and immutable types

**Chapter Structure:**

1. **Section 3.1**: List Basics - Learn to create and access lists
2. **Section 3.2**: List Operations - Modify lists by adding, removing, and changing elements
3. **Section 3.3**: Tuples and Immutability - Understand immutable sequences and when to use them

Let's begin your journey into Python's sequence types!

---

## Section 3.1: List Basics - Creating and Accessing Lists

### What Are Lists?

Lists are one of Python's most fundamental and versatile data structures. A **list** is an ordered, mutable collection that can store multiple items of any data type.

Think of a list as a container that:
- **Holds multiple items** in a specific order
- **Can be changed** after creation (add, remove, or modify items)
- **Remembers the order** of items
- **Allows duplicates** (can have the same value multiple times)

### Creating Lists

The most common way to create a list is using square brackets:

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

### Accessing List Elements

Python uses **zero-based indexing** - the first element is at index 0:

```python
fruits = ["apple", "banana", "cherry"]

first_fruit = fruits[0]      # "apple"
second_fruit = fruits[1]     # "banana"
third_fruit = fruits[2]      # "cherry"
```

Python also supports **negative indices** that count from the end:

```python
last_fruit = fruits[-1]       # "cherry"
second_last = fruits[-2]      # "banana"
```

### Slicing Lists

Slicing lets you extract a portion of a list using `list[start:end]` syntax:

```python
numbers = [1, 2, 3, 4, 5]

first_three = numbers[0:3]    # [1, 2, 3]
last_two = numbers[-2:]       # [4, 5]
every_other = numbers[::2]    # [1, 3, 5]
reversed_list = numbers[::-1] # [5, 4, 3, 2, 1]
```

**Key point:** The `end` index is not included in the slice.

### Common Operations

Check membership:
```python
has_apple = "apple" in fruits        # True
```

Find position:
```python
position = fruits.index("banana")    # 1
```

Count occurrences:
```python
numbers = [1, 2, 2, 3, 2, 4]
count = numbers.count(2)              # 3
```

**Transition:** Now that you understand how to create and access lists, let's explore how to modify them - the real power of lists comes from their mutability.

---

## Section 3.2: List Operations - Modify, Add, Remove

### Lists Are Mutable

Unlike strings or numbers, lists can be changed after creation. This **mutability** makes lists incredibly powerful for managing collections that evolve over time.

### Modifying Elements

Change elements by assigning to an index:

```python
fruits = ["apple", "banana", "cherry"]
fruits[0] = "orange"          # Replace "apple" with "orange"
# fruits is now: ["orange", "banana", "cherry"]
```

### Adding Elements

Python provides several ways to add elements to lists:

**append()** - add single element to end:
```python
fruits = ["apple", "banana"]
fruits.append("cherry")
# fruits is now: ["apple", "banana", "cherry"]
```

**insert()** - add element at specific position:
```python
fruits.insert(1, "mango")     # Insert "mango" at index 1
# fruits is now: ["apple", "mango", "banana", "cherry"]
```

**extend()** - add multiple elements:
```python
more_fruits = ["grape", "kiwi"]
fruits.extend(more_fruits)
# fruits is now: ["apple", "mango", "banana", "cherry", "grape", "kiwi"]
```

### Removing Elements

**remove()** - remove first occurrence by value:
```python
fruits.remove("banana")       # Removes first "banana"
```

**pop()** - remove and return element at index:
```python
last = fruits.pop()           # Removes and returns last element
first = fruits.pop(0)         # Removes and returns first element
```

**del** statement - remove by index:
```python
del fruits[0]                 # Remove first element
```

**clear()** - remove all elements:
```python
fruits.clear()                # Empty the list
```

### Method Comparison

| Method | What It Does | Returns | Example |
|--------|--------------|---------|---------|
| `append(x)` | Add x to end | None | `lst.append(4)` |
| `insert(i, x)` | Add x at index i | None | `lst.insert(0, 4)` |
| `extend(iter)` | Add all from iterable | None | `lst.extend([4,5])` |
| `remove(x)` | Remove first x | None | `lst.remove(4)` |
| `pop()` | Remove last, return it | Element | `x = lst.pop()` |
| `pop(i)` | Remove at i, return it | Element | `x = lst.pop(0)` |

**Important:** Methods like `append()` and `extend()` modify the list **in place** and return `None`, not the modified list.

**Transition:** Lists are mutable and powerful for changing data. But what if you need a sequence that *can't* be changed? That's where tuples come in.

---

## Section 3.3: Tuples and Immutability

### What Are Tuples?

**Tuples** are ordered, immutable sequences - like lists that can't be changed once created.

### Creating Tuples

Create tuples using parentheses:

```python
coordinates = (10, 20)
rgb_color = (255, 128, 0)

# Single-element tuple requires comma!
single = (42,)              # This is a tuple
not_tuple = (42)            # This is just an int!
```

### Accessing Tuples

Access tuple elements just like lists:

```python
point = (10, 20, 30)
x = point[0]         # 10
y = point[1]         # 20
z = point[-1]        # 30
```

### Tuples Are Immutable

You **cannot** modify tuple elements:

```python
coords = (10, 20, 30)

# This raises TypeError:
# coords[0] = 15

# No append, remove, or other modification methods
```

To "modify" a tuple, create a new one:

```python
old_coords = (10, 20)
new_coords = (old_coords[0], old_coords[1], 30)  # (10, 20, 30)
```

### When to Use Tuples vs Lists

**Use TUPLES for:**
- Fixed data that shouldn't change (coordinates, RGB colors, dates)
- Function return values (returning multiple values)
- Dictionary keys (tuples are hashable, lists aren't)
- Data integrity (prevent accidental modification)

```python
# Good tuple use cases
rgb_red = (255, 0, 0)                    # Color won't change
location = (37.7749, -122.4194)          # Coordinates are fixed

def get_min_max(numbers):
    return (min(numbers), max(numbers))  # Return multiple values

# Dictionary with tuple keys
city_locations = {
    (37.7749, -122.4194): "San Francisco",
    (40.7128, -74.0060): "New York"
}
```

**Use LISTS for:**
- Collections that will change (shopping cart, to-do list)
- Data that needs sorting or filtering
- Unknown or variable size collections

```python
# Good list use cases
shopping_cart = ["milk", "eggs"]
shopping_cart.append("bread")            # Can add items

scores = [85, 92, 78, 95]
scores.sort()                            # Can reorder
```

### Tuple Unpacking

One of tuples' most powerful features is **unpacking**:

```python
# Unpack into variables
point = (10, 20, 30)
x, y, z = point              # x=10, y=20, z=30

# Swap variables
a, b = 5, 10
a, b = b, a                  # a=10, b=5

# Unpack function returns
def get_name_age():
    return ("Alice", 25)

name, age = get_name_age()

# Extended unpacking
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers  # first=1, middle=[2,3,4], last=5
```

### Tuple Methods

Tuples have only 2 methods (compared to lists' many methods):

```python
numbers = (1, 2, 3, 2, 4, 2)

count = numbers.count(2)      # 3
index = numbers.index(3)      # 2
```

### Lists vs Tuples Summary

| Feature | Lists | Tuples |
|---------|-------|--------|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` |
| Mutable | ✅ Yes | ❌ No |
| Methods | Many (append, remove, sort...) | Two (count, index) |
| Dictionary keys | ❌ No | ✅ Yes |
| Use case | Changing collections | Fixed data |
| Performance | Slower | Faster |

---

## Chapter Summary

Congratulations! You've mastered Python's core sequence types. Let's review what you've learned:

**Lists:**
- Ordered, mutable collections created with `[]`
- Access elements with positive/negative indices
- Slice with `[start:end:step]` syntax
- Modify with `append()`, `insert()`, `extend()`, `remove()`, `pop()`
- Perfect for collections that change

**Tuples:**
- Ordered, immutable sequences created with `()`
- Access like lists but can't modify
- Use for fixed data and function returns
- Support powerful unpacking syntax
- Hashable (can be dictionary keys)

**Key Decision:**
- Need to change the collection? → Use a **list**
- Data is fixed and shouldn't change? → Use a **tuple**

### Practical Application

Here's how you might use both in a real program:

```python
# Tuple for fixed configuration
DEFAULT_WINDOW_SIZE = (1920, 1080)
RGB_COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255)
}

# List for dynamic data
shopping_cart = []
shopping_cart.append("laptop")
shopping_cart.append("mouse")
shopping_cart.extend(["keyboard", "monitor"])

# Function returning tuple
def get_screen_info():
    width, height = DEFAULT_WINDOW_SIZE
    return (width, height, width * height)

width, height, area = get_screen_info()

# Process items (list allows modification)
if "mouse" in shopping_cart:
    shopping_cart.remove("mouse")
    shopping_cart.append("wireless mouse")
```

### What's Next?

In **Chapter 4**, you'll learn about dictionaries and sets - Python's key-value and unique collection types. Dictionaries let you look up values by name rather than position, opening up powerful new programming patterns.

**Preview:**
```python
# Coming in Chapter 4: Dictionaries
student = {
    'name': 'Alice',
    'age': 20,
    'grades': [95, 88, 92]
}

print(student['name'])  # Much clearer than student[0]!
```

---

## Chapter Exercises

**Exercise 1:** Create a list of your 5 favorite movies. Print the first, last, and middle movie.

**Exercise 2:** Write a function that takes a list of numbers and returns a tuple of (minimum, maximum, average).

**Exercise 3:** Create a dictionary (you'll learn more in Ch 4!) where keys are tuples of (latitude, longitude) and values are city names.

**Challenge:** Implement a simple to-do list manager with functions to add, remove, and list tasks.

---

<!-- Workflow metadata -->
<!-- Assembly process:
  1. merge-sections.md: Combined section-1-final, section-2-final, section-3-final
  2. enhance-transitions.md: Improved flow between sections
  3. validate-learning-flow.md: Confirmed progressive complexity
  4. technical-review-chapter.md: Full chapter technical review
  5. copy-edit-chapter.md: Polish and consistency pass
  6. execute-checklist.md with chapter-completeness-checklist.md: Final quality gate
-->
<!-- Quality gates: All passed ✅ -->
<!-- Ready for: Publisher submission / Self-publishing -->
<!-- Total pages: ~11-12 pages -->

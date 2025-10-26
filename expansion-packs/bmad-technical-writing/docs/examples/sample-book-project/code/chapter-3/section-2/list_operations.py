"""
List Operations - Modify, Add, Remove
Chapter 3, Section 3.2
Python Essentials: Data Structures and Algorithms
"""

# Example 1: Modifying list elements
# -----------------------------------

# Lists are mutable - you can change their elements
fruits = ["apple", "banana", "cherry"]

# Modify an element by index
fruits[0] = "orange"          # Replace "apple" with "orange"
# fruits is now: ["orange", "banana", "cherry"]

# Modify multiple elements
numbers = [1, 2, 3, 4, 5]
numbers[1] = 20               # Replace 2 with 20
numbers[-1] = 50              # Replace last element (5) with 50
# numbers is now: [1, 20, 3, 4, 50]


# Example 2: Adding elements to lists
# ------------------------------------

# append() - add single element to end
fruits = ["apple", "banana"]
fruits.append("cherry")       # Add "cherry" to end
# fruits is now: ["apple", "banana", "cherry"]

# insert() - add element at specific position
fruits.insert(1, "mango")     # Insert "mango" at index 1
# fruits is now: ["apple", "mango", "banana", "cherry"]

# extend() - add multiple elements from another list
more_fruits = ["grape", "kiwi"]
fruits.extend(more_fruits)    # Add all elements from more_fruits
# fruits is now: ["apple", "mango", "banana", "cherry", "grape", "kiwi"]

# Alternative: use += operator (same as extend)
fruits += ["melon"]
# fruits is now: ["apple", "mango", "banana", "cherry", "grape", "kiwi", "melon"]


# Example 3: Removing elements from lists
# ----------------------------------------

# remove() - remove first occurrence of a value
fruits = ["apple", "banana", "cherry", "banana"]
fruits.remove("banana")       # Removes first "banana"
# fruits is now: ["apple", "cherry", "banana"]

# pop() - remove and return element at index (default: last)
last_fruit = fruits.pop()     # Removes and returns "banana"
# fruits is now: ["apple", "cherry"]

first_fruit = fruits.pop(0)   # Removes and returns element at index 0
# fruits is now: ["cherry"]

# del statement - remove element(s) by index or slice
numbers = [1, 2, 3, 4, 5]
del numbers[0]                # Remove first element
# numbers is now: [2, 3, 4, 5]

del numbers[1:3]              # Remove elements at indices 1-2
# numbers is now: [2, 5]

# clear() - remove all elements
numbers.clear()
# numbers is now: []


# Example 4: List concatenation and repetition
# ---------------------------------------------

# Concatenation with + operator
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = list1 + list2      # [1, 2, 3, 4, 5, 6]

# Repetition with * operator
repeated = [1, 2] * 3         # [1, 2, 1, 2, 1, 2]


# Example 5: Comparing modification methods
# ------------------------------------------

# append vs extend
numbers = [1, 2, 3]
numbers.append([4, 5])        # Adds list as single element
# numbers is now: [1, 2, 3, [4, 5]]

numbers = [1, 2, 3]
numbers.extend([4, 5])        # Adds each element individually
# numbers is now: [1, 2, 3, 4, 5]

# remove vs pop vs del
fruits = ["apple", "banana", "cherry"]

# remove: remove by value (raises ValueError if not found)
fruits_copy1 = fruits.copy()
fruits_copy1.remove("banana") # Removes "banana", no return value

# pop: remove by index, returns the removed value
fruits_copy2 = fruits.copy()
removed = fruits_copy2.pop(1) # Returns "banana"

# del: remove by index, no return value
fruits_copy3 = fruits.copy()
del fruits_copy3[1]           # Removes "banana", no return value


# Example 6: In-place vs creating new list
# -----------------------------------------

# In-place modification (changes original list)
numbers = [1, 2, 3]
numbers.append(4)             # Modifies numbers in-place
# numbers is now: [1, 2, 3, 4]

# Creating new list (original unchanged)
numbers = [1, 2, 3]
new_numbers = numbers + [4]   # Creates new list
# numbers is still: [1, 2, 3]
# new_numbers is: [1, 2, 3, 4]


# Common pitfalls
# ---------------

# 1. remove() raises ValueError if element not found
# This would raise ValueError:
# bad_remove = ["apple", "banana"]
# bad_remove.remove("cherry")  # ValueError!

# 2. Modifying list during iteration
# Bad:
# numbers = [1, 2, 3, 4, 5]
# for num in numbers:
#     if num % 2 == 0:
#         numbers.remove(num)  # Can skip elements!

# Good:
# numbers = [1, 2, 3, 4, 5]
# numbers = [num for num in numbers if num % 2 != 0]

# 3. append vs extend confusion
# append adds the whole argument as single element
# extend adds each element of the argument individually

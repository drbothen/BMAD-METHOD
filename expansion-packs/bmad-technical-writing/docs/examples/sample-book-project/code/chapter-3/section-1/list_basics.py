"""
List Basics - Creating and Accessing Lists
Chapter 3, Section 3.1
Python Essentials: Data Structures and Algorithms
"""

# Example 1: Creating lists
# --------------------------

# Create a list of numbers
numbers = [1, 2, 3, 4, 5]

# Create a list of strings
fruits = ["apple", "banana", "cherry"]

# Create a list with mixed data types
mixed = [1, "hello", 3.14, True]

# Create an empty list
empty_list = []

# Create a list using the list() constructor
from_string = list("Python")  # ['P', 'y', 't', 'h', 'o', 'n']


# Example 2: Accessing elements (indexing)
# -----------------------------------------

# Access elements using positive indexing (0-based)
first_fruit = fruits[0]      # "apple"
second_fruit = fruits[1]     # "banana"
third_fruit = fruits[2]      # "cherry"

# Access elements using negative indexing (from the end)
last_fruit = fruits[-1]      # "cherry"
second_last = fruits[-2]     # "banana"
first_again = fruits[-3]     # "apple"

# Get the length of a list
list_length = len(fruits)    # 3


# Example 3: Slicing lists
# -------------------------

# Basic slicing [start:end] - end is exclusive
first_three = numbers[0:3]    # [1, 2, 3]
middle_three = numbers[1:4]   # [2, 3, 4]

# Omit start (defaults to 0)
from_beginning = numbers[:3]  # [1, 2, 3]

# Omit end (goes to end of list)
to_end = numbers[2:]          # [3, 4, 5]

# Use negative indices in slices
last_two = numbers[-2:]       # [4, 5]

# Slicing with step [start:end:step]
every_other = numbers[::2]    # [1, 3, 5]
reversed_list = numbers[::-1] # [5, 4, 3, 2, 1]

# Copy a list using slicing
numbers_copy = numbers[:]     # [1, 2, 3, 4, 5]


# Example 4: Common list patterns
# --------------------------------

# Check if element exists in list
has_apple = "apple" in fruits        # True
has_orange = "orange" in fruits      # False

# Get the index of an element
apple_index = fruits.index("apple")  # 0

# Count occurrences of an element
duplicates = [1, 2, 2, 3, 2, 4]
count_of_twos = duplicates.count(2)  # 3


# Example 5: Nested lists (lists within lists)
# ---------------------------------------------

# Create a 2D list (matrix)
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access elements in nested lists
first_row = matrix[0]         # [1, 2, 3]
middle_element = matrix[1][1] # 5
bottom_right = matrix[2][2]   # 9


# Common pitfalls to avoid
# ------------------------

# 1. IndexError - trying to access index that doesn't exist
# This would raise IndexError: list index out of range
# bad_access = fruits[10]

# 2. Confusing index with element value
# Index is the position (0, 1, 2...)
# Element value is what's stored ("apple", "banana"...)

# 3. Forgetting that slicing doesn't include the end index
# numbers[0:3] gives you indices 0, 1, 2 (NOT 3)

"""
Tuples and Immutability
Chapter 3, Section 3.3
Python Essentials: Data Structures and Algorithms
"""

# Example 1: Creating tuples
# ---------------------------

# Create tuple using parentheses
coordinates = (10, 20)
rgb_color = (255, 128, 0)

# Create tuple without parentheses (tuple packing)
point = 5, 10

# Single-element tuple (note the comma!)
single = (42,)              # This is a tuple
not_tuple = (42)            # This is just an int in parentheses!

# Empty tuple
empty_tuple = ()

# Create tuple using tuple() constructor
from_list = tuple([1, 2, 3])    # (1, 2, 3)
from_string = tuple("hi")        # ('h', 'i')


# Example 2: Accessing tuple elements
# ------------------------------------

# Tuples use same indexing as lists
coordinates = (10, 20, 30)

x = coordinates[0]         # 10
y = coordinates[1]         # 20
z = coordinates[2]         # 30

# Negative indexing works too
last = coordinates[-1]     # 30

# Slicing works
middle_coords = coordinates[0:2]  # (10, 20)


# Example 3: Tuples are immutable
# --------------------------------

# You CANNOT modify tuple elements
coordinates = (10, 20, 30)

# This would raise TypeError: 'tuple' object does not support item assignment
# coordinates[0] = 15

# You CANNOT add elements to tuples
# coordinates.append(40)    # AttributeError: 'tuple' object has no attribute 'append'

# You CANNOT remove elements from tuples
# coordinates.remove(10)    # AttributeError: 'tuple' object has no attribute 'remove'

# To "modify" a tuple, you must create a new tuple
old_coords = (10, 20)
new_coords = (old_coords[0], old_coords[1], 30)  # (10, 20, 30)

# Or convert to list, modify, convert back
coords_list = list(coordinates)
coords_list[0] = 15
modified_coords = tuple(coords_list)  # (15, 20, 30)


# Example 4: When to use tuples vs lists
# ---------------------------------------

# Use TUPLES for:
# - Fixed data that shouldn't change
rgb_color = (255, 128, 0)     # RGB values are fixed
date = (2024, 10, 26)          # Date components are fixed
geographic_point = (37.7749, -122.4194)  # Latitude, longitude

# - Function return values (multiple values)
def get_min_max(numbers):
    return (min(numbers), max(numbers))  # Returns tuple

min_val, max_val = get_min_max([1, 5, 3, 9, 2])

# - Dictionary keys (lists can't be keys!)
locations = {
    (37.7749, -122.4194): "San Francisco",
    (40.7128, -74.0060): "New York"
}

# Use LISTS for:
# - Collections that will change
shopping_list = ["milk", "eggs", "bread"]  # Will add/remove items
shopping_list.append("butter")

# - Collections where order might change
scores = [95, 87, 92, 88]
scores.sort()  # Reorder in place

# - When you need list-specific methods
numbers = [1, 2, 3]
numbers.append(4)
numbers.extend([5, 6])


# Example 5: Tuple unpacking
# ---------------------------

# Unpack tuple into separate variables
coordinates = (10, 20, 30)
x, y, z = coordinates      # x=10, y=20, z=30

# Swap variables using tuple unpacking
a = 5
b = 10
a, b = b, a               # Now a=10, b=5

# Unpack function return value
def get_name_age():
    return ("Alice", 25)

name, age = get_name_age()

# Use underscore for values you don't need
coords_3d = (10, 20, 30)
x, y, _ = coords_3d       # Ignore z coordinate

# Extended unpacking (Python 3+)
numbers = (1, 2, 3, 4, 5)
first, *middle, last = numbers  # first=1, middle=[2,3,4], last=5


# Example 6: Tuple methods and operations
# ----------------------------------------

# Tuples have only 2 methods: count() and index()
numbers = (1, 2, 3, 2, 4, 2)

count_of_twos = numbers.count(2)  # 3
index_of_three = numbers.index(3)  # 2

# Concatenation (creates new tuple)
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
combined = tuple1 + tuple2  # (1, 2, 3, 4, 5, 6)

# Repetition (creates new tuple)
repeated = (1, 2) * 3       # (1, 2, 1, 2, 1, 2)

# Membership testing
has_element = 3 in (1, 2, 3)  # True

# Length
length = len((1, 2, 3, 4))  # 4


# Example 7: Nested tuples
# -------------------------

# Tuples can contain other tuples
matrix = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9)
)

# Access nested elements
first_row = matrix[0]       # (1, 2, 3)
middle_element = matrix[1][1]  # 5


# Example 8: Tuples with mutable elements
# ----------------------------------------

# Tuples themselves are immutable, but can contain mutable objects
tuple_with_list = (1, 2, [3, 4])

# You CAN'T reassign the list
# tuple_with_list[2] = [5, 6]  # TypeError!

# But you CAN modify the list's contents
tuple_with_list[2].append(5)  # This works!
# tuple_with_list is now (1, 2, [3, 4, 5])

# This means the tuple's "identity" doesn't change,
# but the mutable object inside can change


# Summary: Lists vs Tuples
# -------------------------
"""
LISTS:
- Mutable (can be changed)
- Use brackets []
- Many methods (append, remove, sort, etc.)
- Use when collection will change
- Can't be dictionary keys

TUPLES:
- Immutable (can't be changed)
- Use parentheses ()
- Only 2 methods (count, index)
- Use for fixed data
- Can be dictionary keys
- Slightly faster and more memory efficient
"""

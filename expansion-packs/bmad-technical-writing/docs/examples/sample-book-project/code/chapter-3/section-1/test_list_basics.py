"""
Unit tests for List Basics
Chapter 3, Section 3.1
Python Essentials: Data Structures and Algorithms
"""

import unittest
from list_basics import (
    numbers, fruits, mixed, empty_list, from_string,
    first_fruit, second_fruit, third_fruit,
    last_fruit, second_last, first_again,
    list_length,
    first_three, middle_three, from_beginning, to_end,
    last_two, every_other, reversed_list, numbers_copy,
    has_apple, has_orange, apple_index,
    duplicates, count_of_twos,
    matrix, first_row, middle_element, bottom_right
)


class TestListCreation(unittest.TestCase):
    """Test creating lists in various ways"""

    def test_number_list(self):
        """Test creating a list of numbers"""
        self.assertEqual(numbers, [1, 2, 3, 4, 5])
        self.assertEqual(len(numbers), 5)

    def test_string_list(self):
        """Test creating a list of strings"""
        self.assertEqual(fruits, ["apple", "banana", "cherry"])
        self.assertEqual(len(fruits), 3)

    def test_mixed_list(self):
        """Test creating a list with mixed types"""
        self.assertEqual(len(mixed), 4)
        self.assertIsInstance(mixed[0], int)
        self.assertIsInstance(mixed[1], str)
        self.assertIsInstance(mixed[2], float)
        self.assertIsInstance(mixed[3], bool)

    def test_empty_list(self):
        """Test creating an empty list"""
        self.assertEqual(empty_list, [])
        self.assertEqual(len(empty_list), 0)

    def test_list_from_string(self):
        """Test creating list from string using list()"""
        self.assertEqual(from_string, ['P', 'y', 't', 'h', 'o', 'n'])
        self.assertEqual(len(from_string), 6)


class TestIndexing(unittest.TestCase):
    """Test accessing list elements with positive and negative indices"""

    def test_positive_indexing(self):
        """Test accessing elements with positive indices"""
        self.assertEqual(first_fruit, "apple")
        self.assertEqual(second_fruit, "banana")
        self.assertEqual(third_fruit, "cherry")

    def test_negative_indexing(self):
        """Test accessing elements with negative indices"""
        self.assertEqual(last_fruit, "cherry")
        self.assertEqual(second_last, "banana")
        self.assertEqual(first_again, "apple")

    def test_list_length(self):
        """Test getting list length with len()"""
        self.assertEqual(list_length, 3)

    def test_index_bounds(self):
        """Test that accessing out of bounds raises IndexError"""
        with self.assertRaises(IndexError):
            _ = fruits[10]
        with self.assertRaises(IndexError):
            _ = fruits[-10]


class TestSlicing(unittest.TestCase):
    """Test list slicing operations"""

    def test_basic_slicing(self):
        """Test basic slice [start:end]"""
        self.assertEqual(first_three, [1, 2, 3])
        self.assertEqual(middle_three, [2, 3, 4])

    def test_omit_start(self):
        """Test slicing with omitted start"""
        self.assertEqual(from_beginning, [1, 2, 3])

    def test_omit_end(self):
        """Test slicing with omitted end"""
        self.assertEqual(to_end, [3, 4, 5])

    def test_negative_slice(self):
        """Test slicing with negative indices"""
        self.assertEqual(last_two, [4, 5])

    def test_step_slicing(self):
        """Test slicing with step parameter"""
        self.assertEqual(every_other, [1, 3, 5])
        self.assertEqual(reversed_list, [5, 4, 3, 2, 1])

    def test_copy_via_slice(self):
        """Test copying a list using [:]"""
        self.assertEqual(numbers_copy, numbers)
        self.assertIsNot(numbers_copy, numbers)  # Different objects


class TestListMembership(unittest.TestCase):
    """Test checking for element membership"""

    def test_in_operator(self):
        """Test 'in' operator for membership"""
        self.assertTrue(has_apple)
        self.assertFalse(has_orange)

    def test_index_method(self):
        """Test index() method to find element position"""
        self.assertEqual(apple_index, 0)

    def test_index_not_found(self):
        """Test index() raises ValueError when element not found"""
        with self.assertRaises(ValueError):
            fruits.index("orange")

    def test_count_method(self):
        """Test count() method"""
        self.assertEqual(count_of_twos, 3)
        self.assertEqual(duplicates.count(1), 1)
        self.assertEqual(duplicates.count(999), 0)  # Element not in list


class TestNestedLists(unittest.TestCase):
    """Test working with nested lists"""

    def test_matrix_structure(self):
        """Test 2D list structure"""
        self.assertEqual(len(matrix), 3)
        self.assertEqual(len(matrix[0]), 3)

    def test_accessing_rows(self):
        """Test accessing nested list rows"""
        self.assertEqual(first_row, [1, 2, 3])

    def test_accessing_elements(self):
        """Test accessing individual elements in nested lists"""
        self.assertEqual(middle_element, 5)
        self.assertEqual(bottom_right, 9)

    def test_nested_indexing(self):
        """Test various nested indexing patterns"""
        self.assertEqual(matrix[0][0], 1)  # Top-left
        self.assertEqual(matrix[0][-1], 3) # Top-right
        self.assertEqual(matrix[-1][0], 7) # Bottom-left


class TestListEquality(unittest.TestCase):
    """Test list comparison and equality"""

    def test_list_equality(self):
        """Test that lists with same elements are equal"""
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        self.assertEqual(list1, list2)

    def test_list_inequality(self):
        """Test that lists with different elements are not equal"""
        list1 = [1, 2, 3]
        list2 = [1, 2, 4]
        self.assertNotEqual(list1, list2)

    def test_identity_vs_equality(self):
        """Test difference between 'is' and '=='"""
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]
        list3 = list1

        self.assertEqual(list1, list2)      # Equal values
        self.assertIsNot(list1, list2)      # Different objects
        self.assertIs(list1, list3)         # Same object


if __name__ == '__main__':
    unittest.main()

"""
Unit tests for List Operations
Chapter 3, Section 3.2
Python Essentials: Data Structures and Algorithms
"""

import unittest


class TestModifyingElements(unittest.TestCase):
    """Test modifying list elements by index"""

    def test_modify_by_index(self):
        """Test changing elements using index assignment"""
        fruits = ["apple", "banana", "cherry"]
        fruits[0] = "orange"
        self.assertEqual(fruits, ["orange", "banana", "cherry"])

    def test_modify_negative_index(self):
        """Test modifying using negative indices"""
        numbers = [1, 2, 3, 4, 5]
        numbers[-1] = 50
        self.assertEqual(numbers[4], 50)
        self.assertEqual(numbers, [1, 2, 3, 4, 50])

    def test_modify_multiple(self):
        """Test modifying multiple elements"""
        numbers = [1, 2, 3, 4, 5]
        numbers[1] = 20
        numbers[3] = 40
        self.assertEqual(numbers, [1, 20, 3, 40, 5])


class TestAddingElements(unittest.TestCase):
    """Test adding elements to lists"""

    def test_append(self):
        """Test append() adds element to end"""
        fruits = ["apple", "banana"]
        fruits.append("cherry")
        self.assertEqual(fruits, ["apple", "banana", "cherry"])
        self.assertEqual(len(fruits), 3)

    def test_append_returns_none(self):
        """Test that append() returns None"""
        fruits = ["apple"]
        result = fruits.append("banana")
        self.assertIsNone(result)

    def test_insert(self):
        """Test insert() adds element at specific position"""
        fruits = ["apple", "cherry"]
        fruits.insert(1, "banana")
        self.assertEqual(fruits, ["apple", "banana", "cherry"])

    def test_insert_beginning(self):
        """Test inserting at beginning"""
        numbers = [2, 3]
        numbers.insert(0, 1)
        self.assertEqual(numbers, [1, 2, 3])

    def test_insert_end(self):
        """Test inserting at end (like append)"""
        numbers = [1, 2]
        numbers.insert(len(numbers), 3)
        self.assertEqual(numbers, [1, 2, 3])

    def test_extend(self):
        """Test extend() adds multiple elements"""
        fruits = ["apple", "banana"]
        fruits.extend(["cherry", "grape"])
        self.assertEqual(fruits, ["apple", "banana", "cherry", "grape"])

    def test_extend_vs_append(self):
        """Test difference between extend and append"""
        # append adds list as single element
        list1 = [1, 2, 3]
        list1.append([4, 5])
        self.assertEqual(list1, [1, 2, 3, [4, 5]])

        # extend adds each element
        list2 = [1, 2, 3]
        list2.extend([4, 5])
        self.assertEqual(list2, [1, 2, 3, 4, 5])

    def test_plus_operator(self):
        """Test += operator (same as extend)"""
        fruits = ["apple"]
        fruits += ["banana", "cherry"]
        self.assertEqual(fruits, ["apple", "banana", "cherry"])


class TestRemovingElements(unittest.TestCase):
    """Test removing elements from lists"""

    def test_remove_by_value(self):
        """Test remove() removes first occurrence"""
        fruits = ["apple", "banana", "cherry"]
        fruits.remove("banana")
        self.assertEqual(fruits, ["apple", "cherry"])

    def test_remove_first_occurrence(self):
        """Test remove() only removes first occurrence"""
        numbers = [1, 2, 3, 2, 4]
        numbers.remove(2)
        self.assertEqual(numbers, [1, 3, 2, 4])

    def test_remove_not_found(self):
        """Test remove() raises ValueError if element not found"""
        fruits = ["apple", "banana"]
        with self.assertRaises(ValueError):
            fruits.remove("cherry")

    def test_pop_last(self):
        """Test pop() removes and returns last element"""
        fruits = ["apple", "banana", "cherry"]
        removed = fruits.pop()
        self.assertEqual(removed, "cherry")
        self.assertEqual(fruits, ["apple", "banana"])

    def test_pop_by_index(self):
        """Test pop(index) removes and returns element at index"""
        fruits = ["apple", "banana", "cherry"]
        removed = fruits.pop(1)
        self.assertEqual(removed, "banana")
        self.assertEqual(fruits, ["apple", "cherry"])

    def test_pop_first(self):
        """Test popping first element"""
        numbers = [1, 2, 3]
        first = numbers.pop(0)
        self.assertEqual(first, 1)
        self.assertEqual(numbers, [2, 3])

    def test_pop_empty_raises(self):
        """Test pop() on empty list raises IndexError"""
        empty = []
        with self.assertRaises(IndexError):
            empty.pop()

    def test_del_by_index(self):
        """Test del statement removes element by index"""
        fruits = ["apple", "banana", "cherry"]
        del fruits[1]
        self.assertEqual(fruits, ["apple", "cherry"])

    def test_del_slice(self):
        """Test del statement with slice"""
        numbers = [1, 2, 3, 4, 5]
        del numbers[1:4]
        self.assertEqual(numbers, [1, 5])

    def test_clear(self):
        """Test clear() removes all elements"""
        fruits = ["apple", "banana", "cherry"]
        fruits.clear()
        self.assertEqual(fruits, [])
        self.assertEqual(len(fruits), 0)


class TestConcatenationRepetition(unittest.TestCase):
    """Test list concatenation and repetition"""

    def test_concatenation(self):
        """Test + operator creates new list"""
        list1 = [1, 2, 3]
        list2 = [4, 5, 6]
        combined = list1 + list2
        self.assertEqual(combined, [1, 2, 3, 4, 5, 6])

    def test_concatenation_preserves_originals(self):
        """Test + operator doesn't modify original lists"""
        list1 = [1, 2, 3]
        list2 = [4, 5, 6]
        combined = list1 + list2
        self.assertEqual(list1, [1, 2, 3])  # Unchanged
        self.assertEqual(list2, [4, 5, 6])  # Unchanged

    def test_repetition(self):
        """Test * operator repeats list"""
        repeated = [1, 2] * 3
        self.assertEqual(repeated, [1, 2, 1, 2, 1, 2])

    def test_repetition_empty(self):
        """Test repetition with 0"""
        empty = [1, 2, 3] * 0
        self.assertEqual(empty, [])


class TestInPlaceVsNew(unittest.TestCase):
    """Test in-place modification vs creating new lists"""

    def test_append_modifies_inplace(self):
        """Test append() modifies original list"""
        original = [1, 2, 3]
        reference = original
        original.append(4)
        self.assertEqual(original, [1, 2, 3, 4])
        self.assertIs(reference, original)  # Same object

    def test_plus_creates_new(self):
        """Test + operator creates new list"""
        original = [1, 2, 3]
        new_list = original + [4]
        self.assertEqual(original, [1, 2, 3])  # Unchanged
        self.assertEqual(new_list, [1, 2, 3, 4])
        self.assertIsNot(new_list, original)  # Different objects

    def test_extend_modifies_inplace(self):
        """Test extend() modifies original list"""
        original = [1, 2, 3]
        original.extend([4, 5])
        self.assertEqual(original, [1, 2, 3, 4, 5])

    def test_methods_return_none(self):
        """Test that mutating methods return None"""
        fruits = ["apple"]
        self.assertIsNone(fruits.append("banana"))
        self.assertIsNone(fruits.extend(["cherry"]))
        self.assertIsNone(fruits.remove("banana"))
        self.assertIsNone(fruits.clear())


class TestListCopy(unittest.TestCase):
    """Test copying lists"""

    def test_copy_method(self):
        """Test copy() creates shallow copy"""
        original = [1, 2, 3]
        copied = original.copy()
        self.assertEqual(original, copied)
        self.assertIsNot(original, copied)

    def test_copy_via_slice(self):
        """Test [:] creates copy"""
        original = [1, 2, 3]
        copied = original[:]
        self.assertEqual(original, copied)
        self.assertIsNot(original, copied)

    def test_modify_copy_doesnt_affect_original(self):
        """Test modifying copy doesn't affect original"""
        original = [1, 2, 3]
        copied = original.copy()
        copied.append(4)
        self.assertEqual(original, [1, 2, 3])  # Unchanged
        self.assertEqual(copied, [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()

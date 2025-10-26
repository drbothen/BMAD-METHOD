"""
Unit tests for Tuples and Immutability
Chapter 3, Section 3.3
Python Essentials: Data Structures and Algorithms
"""

import unittest


class TestTupleCreation(unittest.TestCase):
    """Test creating tuples in various ways"""

    def test_tuple_with_parentheses(self):
        """Test creating tuple with parentheses"""
        coordinates = (10, 20)
        self.assertIsInstance(coordinates, tuple)
        self.assertEqual(len(coordinates), 2)

    def test_tuple_without_parentheses(self):
        """Test tuple packing without parentheses"""
        point = 5, 10
        self.assertIsInstance(point, tuple)
        self.assertEqual(point, (5, 10))

    def test_single_element_tuple(self):
        """Test single-element tuple requires comma"""
        single = (42,)
        not_tuple = (42)
        self.assertIsInstance(single, tuple)
        self.assertIsInstance(not_tuple, int)  # Not a tuple!

    def test_empty_tuple(self):
        """Test creating empty tuple"""
        empty = ()
        self.assertIsInstance(empty, tuple)
        self.assertEqual(len(empty), 0)

    def test_tuple_constructor(self):
        """Test creating tuple with tuple() constructor"""
        from_list = tuple([1, 2, 3])
        self.assertEqual(from_list, (1, 2, 3))

        from_string = tuple("hi")
        self.assertEqual(from_string, ('h', 'i'))


class TestTupleAccess(unittest.TestCase):
    """Test accessing tuple elements"""

    def test_positive_indexing(self):
        """Test accessing elements with positive indices"""
        coordinates = (10, 20, 30)
        self.assertEqual(coordinates[0], 10)
        self.assertEqual(coordinates[1], 20)
        self.assertEqual(coordinates[2], 30)

    def test_negative_indexing(self):
        """Test accessing elements with negative indices"""
        coordinates = (10, 20, 30)
        self.assertEqual(coordinates[-1], 30)
        self.assertEqual(coordinates[-2], 20)
        self.assertEqual(coordinates[-3], 10)

    def test_slicing(self):
        """Test tuple slicing"""
        numbers = (1, 2, 3, 4, 5)
        self.assertEqual(numbers[0:3], (1, 2, 3))
        self.assertEqual(numbers[2:], (3, 4, 5))
        self.assertEqual(numbers[:2], (1, 2))

    def test_out_of_bounds(self):
        """Test that accessing out of bounds raises IndexError"""
        small = (1, 2)
        with self.assertRaises(IndexError):
            _ = small[5]


class TestTupleImmutability(unittest.TestCase):
    """Test that tuples are immutable"""

    def test_cannot_modify_element(self):
        """Test that attempting to modify element raises TypeError"""
        coords = (10, 20, 30)
        with self.assertRaises(TypeError):
            coords[0] = 15

    def test_no_append_method(self):
        """Test that tuples don't have append method"""
        coords = (10, 20)
        self.assertFalse(hasattr(coords, 'append'))

    def test_no_remove_method(self):
        """Test that tuples don't have remove method"""
        coords = (10, 20)
        self.assertFalse(hasattr(coords, 'remove'))

    def test_cannot_delete_element(self):
        """Test that deleting element raises TypeError"""
        coords = (10, 20, 30)
        with self.assertRaises(TypeError):
            del coords[0]

    def test_can_reassign_variable(self):
        """Test that you can reassign tuple variable (creates new tuple)"""
        coords = (10, 20)
        old_id = id(coords)
        coords = (15, 25)  # Creates new tuple
        new_id = id(coords)
        self.assertNotEqual(old_id, new_id)


class TestTupleUnpacking(unittest.TestCase):
    """Test tuple unpacking operations"""

    def test_basic_unpacking(self):
        """Test unpacking tuple into variables"""
        point = (10, 20, 30)
        x, y, z = point
        self.assertEqual(x, 10)
        self.assertEqual(y, 20)
        self.assertEqual(z, 30)

    def test_swap_variables(self):
        """Test swapping variables with tuple unpacking"""
        a = 5
        b = 10
        a, b = b, a
        self.assertEqual(a, 10)
        self.assertEqual(b, 5)

    def test_function_return_unpacking(self):
        """Test unpacking function return value"""
        def get_coords():
            return (100, 200)

        x, y = get_coords()
        self.assertEqual(x, 100)
        self.assertEqual(y, 200)

    def test_ignore_with_underscore(self):
        """Test ignoring values with underscore"""
        coords = (10, 20, 30)
        x, y, _ = coords  # Ignore z
        self.assertEqual(x, 10)
        self.assertEqual(y, 20)

    def test_extended_unpacking(self):
        """Test extended unpacking with *"""
        numbers = (1, 2, 3, 4, 5)
        first, *middle, last = numbers
        self.assertEqual(first, 1)
        self.assertEqual(middle, [2, 3, 4])  # Note: list, not tuple
        self.assertEqual(last, 5)

    def test_unpacking_wrong_count(self):
        """Test that unpacking wrong number of values raises ValueError"""
        coords = (10, 20)
        with self.assertRaises(ValueError):
            x, y, z = coords  # Too many variables


class TestTupleMethods(unittest.TestCase):
    """Test tuple methods"""

    def test_count_method(self):
        """Test count() method"""
        numbers = (1, 2, 3, 2, 4, 2)
        self.assertEqual(numbers.count(2), 3)
        self.assertEqual(numbers.count(1), 1)
        self.assertEqual(numbers.count(99), 0)

    def test_index_method(self):
        """Test index() method finds first occurrence"""
        numbers = (1, 2, 3, 2, 4)
        self.assertEqual(numbers.index(2), 1)  # First occurrence at index 1
        self.assertEqual(numbers.index(4), 4)

    def test_index_not_found(self):
        """Test index() raises ValueError when element not found"""
        numbers = (1, 2, 3)
        with self.assertRaises(ValueError):
            numbers.index(99)

    def test_only_two_methods(self):
        """Test that tuples have very few methods compared to lists"""
        t = (1, 2, 3)
        # Tuples don't have these list methods
        self.assertFalse(hasattr(t, 'append'))
        self.assertFalse(hasattr(t, 'extend'))
        self.assertFalse(hasattr(t, 'remove'))
        self.assertFalse(hasattr(t, 'pop'))
        self.assertFalse(hasattr(t, 'sort'))
        self.assertFalse(hasattr(t, 'reverse'))


class TestTupleOperations(unittest.TestCase):
    """Test tuple operations"""

    def test_concatenation(self):
        """Test + operator concatenates tuples"""
        tuple1 = (1, 2, 3)
        tuple2 = (4, 5, 6)
        combined = tuple1 + tuple2
        self.assertEqual(combined, (1, 2, 3, 4, 5, 6))

    def test_concatenation_creates_new(self):
        """Test concatenation doesn't modify originals"""
        tuple1 = (1, 2, 3)
        tuple2 = (4, 5, 6)
        combined = tuple1 + tuple2
        self.assertEqual(tuple1, (1, 2, 3))  # Unchanged
        self.assertEqual(tuple2, (4, 5, 6))  # Unchanged

    def test_repetition(self):
        """Test * operator repeats tuple"""
        repeated = (1, 2) * 3
        self.assertEqual(repeated, (1, 2, 1, 2, 1, 2))

    def test_membership(self):
        """Test 'in' operator"""
        numbers = (1, 2, 3, 4, 5)
        self.assertTrue(3 in numbers)
        self.assertFalse(99 in numbers)

    def test_length(self):
        """Test len() function"""
        self.assertEqual(len((1, 2, 3, 4)), 4)
        self.assertEqual(len(()), 0)


class TestNestedTuples(unittest.TestCase):
    """Test tuples containing other tuples"""

    def test_nested_access(self):
        """Test accessing elements in nested tuples"""
        matrix = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9)
        )
        self.assertEqual(matrix[0], (1, 2, 3))
        self.assertEqual(matrix[1][1], 5)
        self.assertEqual(matrix[2][2], 9)

    def test_nested_unpacking(self):
        """Test unpacking nested tuples"""
        point_3d = (10, (20, 30))
        x, (y, z) = point_3d
        self.assertEqual(x, 10)
        self.assertEqual(y, 20)
        self.assertEqual(z, 30)


class TestTupleWithMutableElements(unittest.TestCase):
    """Test tuples containing mutable objects"""

    def test_tuple_with_list(self):
        """Test tuple can contain list"""
        t = (1, 2, [3, 4])
        self.assertIsInstance(t[2], list)

    def test_cannot_replace_list(self):
        """Test can't replace the list element"""
        t = (1, 2, [3, 4])
        with self.assertRaises(TypeError):
            t[2] = [5, 6]

    def test_can_modify_list_contents(self):
        """Test can modify the list's contents"""
        t = (1, 2, [3, 4])
        t[2].append(5)
        self.assertEqual(t[2], [3, 4, 5])
        # The tuple identity didn't change
        self.assertIsInstance(t, tuple)


class TestTupleVsList(unittest.TestCase):
    """Test differences between tuples and lists"""

    def test_list_is_mutable(self):
        """Test that lists can be modified"""
        lst = [1, 2, 3]
        lst[0] = 10
        self.assertEqual(lst, [10, 2, 3])

    def test_tuple_is_immutable(self):
        """Test that tuples cannot be modified"""
        tpl = (1, 2, 3)
        with self.assertRaises(TypeError):
            tpl[0] = 10

    def test_list_has_many_methods(self):
        """Test that lists have modification methods"""
        lst = [1, 2, 3]
        self.assertTrue(hasattr(lst, 'append'))
        self.assertTrue(hasattr(lst, 'extend'))
        self.assertTrue(hasattr(lst, 'remove'))
        self.assertTrue(hasattr(lst, 'pop'))

    def test_tuple_has_few_methods(self):
        """Test that tuples have minimal methods"""
        tpl = (1, 2, 3)
        self.assertTrue(hasattr(tpl, 'count'))
        self.assertTrue(hasattr(tpl, 'index'))
        self.assertFalse(hasattr(tpl, 'append'))
        self.assertFalse(hasattr(tpl, 'remove'))

    def test_tuple_as_dict_key(self):
        """Test that tuples can be dictionary keys"""
        d = {(1, 2): "point"}
        self.assertEqual(d[(1, 2)], "point")

    def test_list_cannot_be_dict_key(self):
        """Test that lists cannot be dictionary keys"""
        with self.assertRaises(TypeError):
            d = {[1, 2]: "point"}  # Lists are unhashable


class TestTupleEquality(unittest.TestCase):
    """Test tuple comparison"""

    def test_equal_tuples(self):
        """Test that tuples with same elements are equal"""
        t1 = (1, 2, 3)
        t2 = (1, 2, 3)
        self.assertEqual(t1, t2)

    def test_unequal_tuples(self):
        """Test that tuples with different elements are unequal"""
        t1 = (1, 2, 3)
        t2 = (1, 2, 4)
        self.assertNotEqual(t1, t2)

    def test_identity_vs_equality(self):
        """Test difference between 'is' and '=='"""
        # Use larger tuples to avoid Python's interning optimization
        t1 = (1, 2, 3, 4, 5, 6)
        t2 = (1, 2, 3, 4, 5, 6)
        t3 = t1

        self.assertEqual(t1, t2)      # Equal values
        # Note: Small tuples may be interned by Python, so identity may match
        # Using variable assignment to test identity
        self.assertIs(t1, t3)         # Same object (t3 references t1)


if __name__ == '__main__':
    unittest.main()

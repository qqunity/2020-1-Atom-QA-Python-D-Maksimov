import pytest
import random
import sys


class TestSet:
    """Doc string..."""

    def test_operator_in_1(self, fun_random_char_set_gen):
        t_set = fun_random_char_set_gen
        val = 'D'
        t_set.add(val)
        assert val in t_set

    def test_add_1(self):  # Тестируем неднородное добавление элементов
        t_set = set()
        s_val = 'qwe'
        i_val = 10
        t_set.add(s_val)
        t_set.add(i_val)
        assert s_val in t_set and i_val in t_set

    def test_add_2(self): # Тестируем добавление однородных элементов в множество( int'ов)
        t_set = set()
        i_val = random.randint(sys.maxsize - 1, sys.maxsize) + random.randint(1, 10)
        t_set.add(i_val)
        assert i_val in t_set

    def test_copy_1(self, fun_random_char_set_gen):
        t_set1 = fun_random_char_set_gen
        t_set2 = t_set1.copy()
        assert t_set1 == t_set2

    def test_union_1(self, fun_random_char_set_gen):
        t_set1 = fun_random_char_set_gen
        t_set2 = fun_random_char_set_gen
        t_set3 = t_set1 | t_set2
        assert t_set1 == t_set3 and t_set2 == t_set3

    def test_intersection_1(self, fun_random_char_set_gen):
        t_set1 = fun_random_char_set_gen
        t_set2 = fun_random_char_set_gen
        t_set3 = t_set1 & t_set2
        assert t_set1 == t_set2 == t_set3

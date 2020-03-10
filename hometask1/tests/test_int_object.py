import pytest
import random
import sys


class ModifiedException(Exception):
    pass


class TestInt:
    """Doc string"""

    def test_div_1(self):
        with pytest.raises(ModifiedException):
            try:
                a = random.randint(0, sys.maxsize)
                b = 0
                c = a / b
            except ZeroDivisionError:
                raise ModifiedException('Divided by zero!')

    def test_div_2(self):
        a = random.randint(1, sys.maxsize)
        b = random.randint(-sys.maxsize, -1)
        assert a / b

    def test_append_1(self):
        with pytest.raises(ModifiedException):
            try:
                a = random.randint(0, sys.maxsize)
                a.append(0)
            except (AttributeError, SyntaxError):
                raise ModifiedException(r"Something went wrong! 'int' object has no attribute 'append'")

    def test_len_1(self):
        with pytest.raises(ModifiedException):
            try:
                a = random.randint(0, sys.maxsize)
                l = len(a)
            except TypeError:
                raise ModifiedException(r"Object of type 'int' has no len()")

    def test_iterable_1(self):
        with pytest.raises(ModifiedException):
            try:
                a = random.randint(0, sys.maxsize)
                buff = 3 in a
            except TypeError:
                raise ModifiedException(r"Argument of type 'int' is not iterable")

    def test_isdigit_1(self):
        with pytest.raises(ModifiedException):
            try:
                a = random.randint(0, sys.maxsize)
                buff = a.isdigit()
            except AttributeError:
                raise ModifiedException(r"'int' object has no attribute 'isdigit")

    def test_multip_1(self):
        a = random.randint(1, sys.maxsize)
        b = random.randint(-sys.maxsize, -1)
        assert a * b

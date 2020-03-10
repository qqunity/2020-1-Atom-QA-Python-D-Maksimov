import pytest
import random
import sys
from tools.tools import gen_random_str


@pytest.fixture(scope='class')
def class_random_int_gen():
    return random.randint(-sys.maxsize - 1, sys.maxsize)


@pytest.fixture(scope='function')
def fun_random_int_gen():
    return random.randint(-sys.maxsize - 1, sys.maxsize)


@pytest.fixture(scope='function')
def fun_random_int_list_gen():
    """Генерируем небольшой список"""
    return [buff + random.randint(1, 6) for buff in range(random.randint(5, 15))]


@pytest.fixture(scope='function')
def fun_random_char_set_gen():
    """Получаем рандомное множество состаящее из элементов букв латинского алфивита"""
    return set(gen_random_str())


@pytest.fixture(scope='function')
def fun_random_int_dict_gen():
    """Получаем словарь кубов чисел от 0 до 4"""
    return {buff: buff ** 3 for buff in range(5)}


@pytest.fixture(scope='function')
def fun_random_str_gen():
    """Получаем рандомную строку из букв латинского алфивита"""
    return gen_random_str()

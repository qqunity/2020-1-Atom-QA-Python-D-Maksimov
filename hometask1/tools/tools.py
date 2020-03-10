import random
import sys


def gen_random_int_range():
    """Генерирует рандомное значение int максимальной величины (почти граничное)"""
    return range(sys.maxsize - random.randint(5, 20), sys.maxsize)


def gen_random_int():
    """Генерирует рандомное значение int (небольшое по величине)"""
    return random.randint(6, 21)


def gen_random_str():
    """Генерирует рандомную строку из букв латинского алфивита"""
    rand_str = ''
    for i in range(random.randint(5, 10)):
        c = random.randint(65, 90)
        rand_str += chr(c)
    return rand_str

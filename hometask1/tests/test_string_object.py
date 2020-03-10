import pytest
import sys
from tools.tools import gen_random_str


class TestString:
    """Doc string..."""

    def test_concat_1(self, fun_random_str_gen):
        t_str1 = fun_random_str_gen  # Создаем рандомную строку и строку извесного содержания - 'qwe'
        t_str2 = 'qwe'
        t_str3 = t_str1 + t_str2
        l1 = len(t_str1)  # Длины данных строк
        l2 = len(t_str2)
        j = 0
        flag = True
        buff = ''
        n_buff = ''
        for i in range(
                l1 + l2):  # Проверяем успешно прошла ли конкатенация (поэлементно сравнивая результирующу строку и изначальные
            if i < l1:  # Ветка для сравнения первой строки, участвующей в конкатенации
                if t_str3[i] != t_str1[j]:  # j отвечает за индексацию элементов изначальных строк
                    flag = False
                    break
                buff += t_str1[j]
                j += 1
                if j == l1:
                    j = 0
            else:  # Ветка для второй строки
                if t_str3[i] != t_str2[j]:
                    flag = False
                    break
                n_buff += t_str2[j]
                j += 1
        assert flag

    @pytest.mark.parametrize('val', list(range(65, 90)))  # Данные параметры соответсвуют всем ASCII кодам заглавных латинских букв
    def test_slice_1(self, fun_random_str_gen, val):
        t_str = fun_random_str_gen
        l = len(t_str)
        t_str += chr(val)
        assert t_str[l:len(t_str)] == chr(val)

    def test_rfind_1(self, fun_random_str_gen):
        t_str = fun_random_str_gen
        pos = len(t_str)
        t_buff_str = gen_random_str()
        t_str += t_buff_str
        assert t_str.rfind(t_buff_str) == pos

    @pytest.mark.parametrize('val', list(range(sys.maxsize, sys.maxsize + 10)))
    def test_isdigit_1(self, val):
        assert str(val).isdigit()

    def test_isupper_1(self, fun_random_str_gen):
        t_str = fun_random_str_gen
        assert t_str.isupper()

    def test_isupper_2(self, fun_random_str_gen):
        t_str = fun_random_str_gen
        with pytest.raises(AssertionError):
            assert t_str.lower().isupper()

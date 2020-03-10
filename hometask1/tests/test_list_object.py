import pytest
from  tools.tools import gen_random_int_range, gen_random_int


class TestList:
    """Doc string ..."""

    @pytest.mark.parametrize('val', list(gen_random_int_range()))
    def test_append_1(self, val):  # Тест метода append с параметризацией
        t_list = []
        t_list.append(val)
        assert t_list[-1] == val

    @pytest.mark.parametrize('i', list(range(10)))
    def test_insert_1(self, fun_random_int_gen, i):  # Тест метода insert с параметризацией
        t_list = [0] * 10
        t_list.insert(i, fun_random_int_gen)
        assert t_list[i] == fun_random_int_gen

    def test_extend_1(self, fun_random_int_list_gen):
        t_list = [1] * 5
        b_list = fun_random_int_list_gen
        t_list.extend(b_list)
        flag = True
        j = 0
        for i in range(5, 5 + len(b_list)):  # Проходимся по тем элементам, которыми мы расширили список и сравниваем с исходным списком, при усливии несовпадения выбрасываем ошибку, счетчик j отвечает за индексацию массива b_list
            if t_list[i] != b_list[j]:
                flag = False
                break
            j += 1
        assert flag

    def test_count_1(self, fun_random_int_list_gen):
        t_list = fun_random_int_list_gen
        val = gen_random_int()
        cnt = 0
        for v_list in t_list:  # Считаем количесва элементов равных val ручками
            if v_list == val:
                cnt += 1
        assert cnt == t_list.count(val)

    def test_len_1(self, fun_random_int_list_gen):
        t_list = fun_random_int_list_gen
        l1 = len(t_list)
        l2 = 0
        for val in t_list:  # Считаем длину списка руками
            l2 += 1
        assert l1 == l2

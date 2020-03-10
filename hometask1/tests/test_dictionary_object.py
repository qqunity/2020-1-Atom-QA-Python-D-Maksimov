import pytest


class TestDict:
    """Doc string..."""

    @pytest.mark.parametrize('val', list(range(5)))
    def test_get_1(self, fun_random_int_dict_gen, val):
        t_dict = fun_random_int_dict_gen
        assert t_dict.get(val) == val ** 3

    def test_values_1(self, fun_random_int_dict_gen):
        t_dict = fun_random_int_dict_gen
        b_list = list(t_dict.values())
        flag = True
        for i, val in enumerate(b_list):
            flag = val == b_list[i]
            if not flag:
                break
        assert flag

    def test_update_1(self, fun_random_int_dict_gen):
        t_dict = fun_random_int_dict_gen
        t_dict.update({5: 5 ** 3})
        assert t_dict.get(5) == (5 ** 3)

    def test_keys_1(self, fun_random_int_dict_gen):
        t_dict = fun_random_int_dict_gen
        t_keys_val = [buff for buff in range(5)]
        keys_val = list(t_dict.keys())
        assert keys_val == t_keys_val

    def test_items_1(self, fun_random_int_dict_gen):
        t_dict = fun_random_int_dict_gen
        keys_val, val = ([buff for buff in range(5)], [buff ** 3 for buff in range(5)])
        flag = True
        i = 0
        for k, v in t_dict.items():
            if k != keys_val[i] or v != val[i]:
                flag = False
                break
            i += 1
        assert flag

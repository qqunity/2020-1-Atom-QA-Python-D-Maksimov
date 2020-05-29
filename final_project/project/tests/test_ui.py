import inspect

import pytest
import random
import allure

from tests.base_ui import BaseCase
from ui.utils.exceptions import InvalidLoginInfoException, InvalidRegInfoException


@pytest.mark.UI
class TestUI(BaseCase):

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_positive_1(self, create_fake_user, home_page_object):
        """Проверка валидного входа"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, password, _ = create_fake_user
        with allure.step('Входим на сайт'):
            home_page = self.login_page.sign_in(username, password, home_page_object)
        with allure.step('Проверяем успешность входа'):
            assert home_page.get_login_name_info() == f'Logged as {username}'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_positive_2(self):
        """Проверка нативной валидации"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Проверяем нативную валидацию'):
            assert self.login_page.check_native_validation()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_positive_3(self, create_fake_user, home_page_object):
        """Проверка валидности заполнения полей в БД при входе"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, password, _ = create_fake_user
        with allure.step('Получаем информацию о пользователе до входа'):
            user_info_before_login = self.db_interaction.get_user_info(username)
        with allure.step('Входим на сайт'):
            home_page = self.login_page.sign_in(username, password, home_page_object)
        with allure.step('Получаем информацию о пользователе после входа входа'):
            user_info_after_login = self.db_interaction.get_user_info(username)
        with allure.step('Проверям информацию о пользователе в БД'):
            assert user_info_before_login['active'] == 0 and user_info_after_login['active'] == 1 and user_info_before_login['access'] == user_info_before_login['access'] == 1 and user_info_before_login['start_active_time'] is None and user_info_after_login['start_active_time'] is not None
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_negative_1(self, get_fake_user_info, home_page_object):
        """Проверка невалидного входа"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, _ = get_fake_user_info
        with allure.step('Входим на сайт и проверяем валидное отбражение ошибки на странице входа'):
            try:
                self.login_page.sign_in(username, password, home_page_object)
            except InvalidLoginInfoException as exception:
                assert exception.args[0] == 'Invalid username or password'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    @pytest.mark.parametrize('len_username', [1, 2, 3, 4, 5])
    def test_sign_in_negative_2(self, get_fake_user_info, len_username, home_page_object):
        """Проверка валидации длины поля username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log_{len_username}.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, _ = get_fake_user_info
            if len(username) < len_username:
                username *= len_username
            username = username[:len_username]
        with allure.step('Входим на сайт и проверяем валидное отбражение ошибки на странице входа'):
            try:
                self.login_page.sign_in(username, password, home_page_object)
            except InvalidLoginInfoException as exception:
                assert exception.args[0] == 'Incorrect username length'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_negative_3(self, home_page_object):
        """Проверка граничных значений длины полей username и password"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Создаём невалидную информацию о пользователе'):
            username = 'qwe' * 20
            password = 'q' * 300
        with allure.step('Входим на сайт и проверяем валидное отбражение ошибки на странице входа'):
            try:
                self.login_page.sign_in(username, password, home_page_object)
            except InvalidLoginInfoException as exception:
                assert exception.args[0] == 'Incorrect username length'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_negative_4(self, home_page_object):
        """Проверка заполения пробелами поля username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Создаём невалидную информацию о пользователе'):
            username = ' ' * 4
            password = 'qweqweqwe'
        with allure.step('Входим на сайт и проверяем валидное отбражение ошибки на странице входа'):
            try:
                self.login_page.sign_in(username, password, home_page_object)
            except InvalidLoginInfoException as exception:
                assert exception.args[0] == 'Необходимо указать логин для авторизации'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_negative_5(self, home_page_object):
        """Проверка заполения пробелами поля password"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Создаём невалидную информацию о пользователе'):
            username = 'qweqweqwe'
            password = ' ' * 5
        with allure.step('Входим на сайт и проверяем валидное отбражение ошибки на странице входа'):
            try:
                self.login_page.sign_in(username, password, home_page_object)
            except InvalidLoginInfoException as exception:
                assert exception.args[0] == 'Необходимо указать пароль для авторизации'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_negative_6(self, home_page_object):
        """Проверка одновременного заполения пробелами полей username и password"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Создаём невалидную информацию о пользователе'):
            username = ' ' * 9
            password = ' ' * 5
        with allure.step('Входим на сайт и проверяем валидное отбражение ошибки на странице входа'):
            try:
                self.login_page.sign_in(username, password, home_page_object)
            except InvalidLoginInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                assert exception.args[0] == 'Необходимо указать логин и пароль для авторизации'

    @allure.feature('UI tests')
    @allure.story('Sign in page story')
    def test_sign_in_negative_7(self, home_page_object):
        """Проверка одновременного заполения пробелами поля password и некореектной длины поля username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Создаём невалидную информацию о пользователе'):
            username = 'q'
            password = ' ' * 5
        with allure.step('Входим на сайт и проверяем валидное отбражение ошибки на странице входа'):
            try:
                self.login_page.sign_in(username, password, home_page_object)
            except InvalidLoginInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                assert exception.args[0] == 'Необходимо указать пароль для авторизации и неверная длина логина'

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_positive_1(self, get_home_page):
        """Проверка валидной регистрации"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, username = get_home_page
        with allure.step('Проверяем успех регистрации и входа на домашнюю страницу'):
            assert home_page.get_login_name_info() == f'Logged as {username}'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    @pytest.mark.parametrize('len_username', [1, 2, 3, 4, 5])
    def test_sign_up_negative_1(self, get_fake_user_info, len_username, reg_page_object, home_page_object):
        """Проверка невалидной длины поля username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log_{len_username}.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
            if len(username) < len_username:
                username *= len_username
            username = username[:len_username]
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'Incorrect username length'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    @pytest.mark.parametrize('part_of_email', [0, 1])
    def test_sign_up_negative_2(self, get_fake_user_info, part_of_email, reg_page_object, home_page_object):
        """Проверка валидации поля email"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log_{part_of_email}.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
            if part_of_email == 1:
                email = '@' + email.split('@')[part_of_email]
            else:
                email = email.split('@')[part_of_email]
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'Invalid email address'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_3(self, get_fake_user_info, reg_page_object, home_page_object):
        """Проверка валидации поля email"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
            email = email.split('@')[0] + '@' + email.split('@')[1].split('.')[0]
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'Invalid email address'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_4(self, get_fake_user_info, reg_page_object, home_page_object):
        """Проверка валидации поля email"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
            email = email.split('@')[0] + '@.'
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'Invalid email address'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_5(self, get_fake_user_info, create_fake_user, reg_page_object, home_page_object):
        """Проверка регистрации пользователя с полем username, совпадающим с уже существующим в БД"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            _, password, email = get_fake_user_info
        with allure.step('Получаем информацию о существующим пользователе'):
            some_username, _, _ = create_fake_user
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(some_username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'User already exist'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_6(self, get_fake_user_info, reg_page_object, home_page_object):
        """Проверка регистрации пользователя с несовпадающими полями password и confirm_password"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object, wrong_password=password + 'qwe')
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'Passwords must match'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_7(self, get_fake_user_info, home_page_object, reg_page_object):
        """Проверка регистрации пользователя с одновременно несовпадающими полями password, confirm_password и невалидным полем email"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
            email = email.split('@')[0]
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object, wrong_password=password + 'qwe')
            except InvalidRegInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                assert exception.args[0] == 'Passwords must match and invalid email address'

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    @pytest.mark.parametrize('len_username', [1, 2, 3, 4, 5])
    def test_sign_up_negative_8(self, get_fake_user_info, len_username, home_page_object, reg_page_object):
        """Проверка регистрации пользователя с одновременно несовпадающими полями password, confirm_password и невалидным полем username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log_{len_username}.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
            if len(username) < len_username:
                username *= len_username
            username = username[:len_username]
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object, wrong_password=password + 'qwe')
            except InvalidRegInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                assert exception.args[0] == 'Incorrect username length and passwords must match'

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_9(self, get_fake_user_info, home_page_object, reg_page_object):
        """Проверка регистрации пользователя с одновременно несовпадающими полями password, confirm_password, и невалидным полем username, и невалидным полем email"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            _, password, _ = get_fake_user_info
            username = 'qwe'
            email = 'qwe@'
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
            except InvalidRegInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                assert exception.args[0] == 'Incorrect username length, passwords must match and invalid email address'

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_10(self, get_fake_user_info, home_page_object, reg_page_object):
        """Проверка граничной длины поля password"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, _, email = get_fake_user_info
            password = 'q' * 300
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_11(self, get_fake_user_info, home_page_object, reg_page_object):
        """Проверка граничного значения длины поля email"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, _ = get_fake_user_info
            email = 'q' * 100
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'Incorrect email length'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_12(self, get_fake_user_info, home_page_object, reg_page_object):
        """Проверка граничного значения длины поля username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            _, password, email = get_fake_user_info
            username = 'q' * 50
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username, email, password, home_page_object)
            except InvalidRegInfoException as exception:
                assert exception.args[0] == 'Incorrect username length'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_13(self, create_fake_user, home_page_object, reg_page_object):
        """Проверка допустимого регистра поля password"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о пользователях с разным ристром поля username'):
            username1, password1, email1 = create_fake_user
            username2 = username1.upper()
            password2 = password1
            email2 = email1 + 'q'
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Регистрируемся и проверяем валидное отбражение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username2, email2, password2, home_page_object)
            except InvalidRegInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception


    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_14(self, reg_page_object):
        """Проверка нативной валидации"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Проверяем нативную валидацию'):
            reg_page.check_native_validation()
            allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
            self.logger.stop_logging()
            allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
            assert reg_page.check_native_validation()

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_15(self, get_fake_user_info, reg_page_object, home_page_object):
        """Проверка допустимости различных символов в поле username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о пользователях с разными символами поля username'):
            username, password, email = get_fake_user_info
            username = '.' * random.randint(1, 4) + username + ' ' * random.randint(1, 3)
            if len(username) > 17:
                username = username[:15]
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Проверяем корректное отображение ошибки на странице регистрации'):
            with pytest.raises(InvalidRegInfoException):
                reg_page.sign_up(username, email, password, home_page_object)
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.db_interaction.del_user_info(username)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sing_up_negative_16(self, get_fake_user_info, home_page_object, reg_page_object):
        """Проверка допустимости русских букв в поле username"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о пользователях с русскими буквами в поле username'):
            username, password, email = get_fake_user_info
            username = 'приветмир' + username
            if len(username) > 17:
                username = username[:15]
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Проверяем корректное отображение ошибки на странице регистрации'):
            with pytest.raises(InvalidRegInfoException):
                reg_page.sign_up(username, email, password, home_page_object)
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.db_interaction.del_user_info(username)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_17(self, create_fake_user, reg_page_object, home_page_object):
        """Проверка регистрации пользователя при совпадении поля email с уже существующим в БД"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Получаем информацию о пользователях с совпадающими полями email'):
            username1, password1, email1 = create_fake_user
            username2 = username1[:6] + 'q'
        with allure.step('Получаем объект страницы регистрации'):
            reg_page = self.login_page.sign_up(reg_page_object)
        with allure.step('Проверяем корректное отображение ошибки на странице регистрации'):
            try:
                reg_page.sign_up(username2, email1, password1, home_page_object)
            except InvalidRegInfoException as exception:
                allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception

    @allure.feature('UI tests')
    @allure.story('Sign up page story')
    def test_sign_up_negative_18(self, get_home_page):
        """Проверка заполнения полей в БД при регистрации"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, username = get_home_page
            home_page.refresh()
        with allure.step('Проверяем заполнение полей в БД'):
            user_info = self.db_interaction.get_user_info(username)
            self.logger.stop_logging()
            allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
            assert user_info['access'] == 1 and user_info['active'] == 1 and user_info['start_active_time'] is not None


    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_1(self, get_home_page):
        """Проверка ссылки логотипа"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, username = get_home_page
        with allure.step('Переходим по ссылке логотипа'):
            home_page.click_logo_button()
        with allure.step('Проверяем корректность перехода по ссылке'):
            assert home_page.get_login_name_info() == f'Logged as {username}'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_2(self, get_home_page):
        """Проверка ссылки home"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, username = get_home_page
        with allure.step('Переходим по ссылке home'):
            home_page.go_to_home_page()
        with allure.step('Проверяем корректность перехода по ссылке'):
            assert home_page.get_login_name_info() == f'Logged as {username}'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_3(self, get_home_page, wiki_page_object):
        """Проверка ссылки python history"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы python history'):
            wiki_page = home_page.go_to_python_history_page(wiki_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            assert wiki_page.get_article_title() == 'History of Python'
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_4(self, get_home_page, flask_page_object, home_page_object):
        """Проверка сылки about flask"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы flask'):
            flask_page = home_page.go_to_about_flask(flask_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            assert 'Welcome to Flask’s documentation' in flask_page.get_welcome_text()
            flask_page.close_tab(home_page_object)
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_5(self, get_home_page, centos_download_page_object, home_page_object):
        """Проверка ссылки download Centos7"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы download Centos7'):
            download_centos_page = home_page.go_to_download_centos(centos_download_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            download_url = download_centos_page.get_current_url()
            allure.attach(self.driver.get_screenshot_as_png(), 'Error screen', allure.attachment_type.PNG)
            download_centos_page.close_tab(home_page_object)
            self.logger.stop_logging()
            allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
            assert 'https://www.centos.org/download/' in download_url

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_6(self, get_home_page, wireshark_news_page_object, home_page_object):
        """Проверка ссылки wireshark news"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы wireshark news'):
            wireshark_news_page = home_page.go_to_wireshark_news(wireshark_news_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            news_url = wireshark_news_page.get_current_url()
            wireshark_news_page.close_tab(home_page_object)
            assert 'wireshark' in news_url and 'news' in news_url
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_7(self, get_home_page, wireshark_download_page_object, home_page_object):
        """Проверка ссылки wireshark download"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы wireshark download'):
            wireshark_download_page = home_page.go_to_wireshark_download(wireshark_download_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            news_url = wireshark_download_page.get_current_url()
            wireshark_download_page.close_tab(home_page_object)
            assert 'wireshark' in news_url and 'download' in news_url
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_8(self, get_home_page, tcp_dump_examples_page_object, home_page_object):
        """Проверка ссылки tcp dump examples"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы tcp dump examples'):
            tcp_dump_examples_page = home_page.go_to_tcp_dump_examples(tcp_dump_examples_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            tcp_dump_examples_url = tcp_dump_examples_page.get_current_url()
            tcp_dump_examples_page.close_tab(home_page_object)
            assert 'tcpdump' in tcp_dump_examples_url and 'examples' in tcp_dump_examples_url
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_9(self, get_home_page, wiki_page_object, home_page_object):
        """Проверка ссылки про API"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы про API'):
            wiki_page = home_page.go_to_about_api(wiki_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            wiki_url = wiki_page.get_current_url()
            wiki_page.close_tab(home_page_object)
            assert 'Application_programming_interface' in wiki_url
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_10(self, get_home_page, future_of_internet_page_object, home_page_object):
        """Проверка ссылки future of internet"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы future of internet'):
            future_of_internet_page = home_page.go_to_future_of_internet(future_of_internet_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            future_of_internet_url = future_of_internet_page.get_current_url()
            future_of_internet_page.close_tab(home_page_object)
            assert 'future-of-the-internet' in future_of_internet_url
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_11(self, get_home_page, wiki_page_object, home_page_object):
        """Проверка ссылки about SMTP"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы about SMTP'):
            wiki_page = home_page.go_to_about_smtp(wiki_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            wiki_url = wiki_page.get_current_url()
            wiki_page.close_tab(home_page_object)
            assert 'SMTP' in wiki_url
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_12(self, get_home_page):
        """Проверка отображения vk id"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, username = get_home_page
        with allure.step('Получаем поле без vk id'):
            field_without_vk_id = home_page.get_user_vk_id_info()
        with allure.step('Устанавливаем пользователю vk id'):
            vk_id = self.vk_api_client.set_vk_id_by_username({username: str(random.randint(100000, 999999))})['body'].split(': ')[1].split('!')[0]
            home_page.refresh()
        with allure.step('Получаем поле с vk id'):
            field_with_vk_id = home_page.get_user_vk_id_info()
        with allure.step('Проверяем корректное отображение'):
            self.vk_api_client.delete_vk_id_by_username(username)
            assert field_without_vk_id == '' and field_with_vk_id.endswith(vk_id)
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)

    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_13(self, get_home_page, login_page_object):
        """Проверка кнопки logout"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, username = get_home_page
        with allure.step('Выходим со страницы'):
            login_page = home_page.logout(login_page_object)
        with allure.step('Проверяем изменённые данные о пользователе в БД'):
            user_info = self.db_interaction.get_user_info(username)
            access_info = user_info['access']
            active_info = user_info['active']
            login_page.refresh()
            self.logger.stop_logging()
            allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
            assert access_info == 1 and active_info == 0 and 'Welcome' in login_page.get_welcome_text()


    @allure.feature('UI tests')
    @allure.story('Home page story')
    def test_home_page_positive_14(self, python_page_object, get_home_page, home_page_object):
        """Проверка ссылки Python page"""
        self.logger.start_logging(
            f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_ui_log.txt')
        with allure.step('Регистрируемся на сайте и получаем объект домашней страницы'):
            home_page, _ = get_home_page
        with allure.step('Получаем объект страницы Python page'):
            python_page = home_page.go_to_python_org(python_page_object)
        with allure.step('Проверяем корректность перехода по ссылке'):
            python_url = python_page.get_current_url()
            assert 'python.org' in python_url
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
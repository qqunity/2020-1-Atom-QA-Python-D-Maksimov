import inspect
import pytest
import allure

from api.utils.exceptions import ResponseStatusCodeException
from database_code.utils.exceptions import UserNotFoundException
from tests.base_api import BaseCase


@pytest.mark.API
class TestApi(BaseCase):

    @allure.feature('API tests')
    @allure.story('Sign in api story')
    def test_sign_in_valid(self, create_fake_user):
        """Проверка кода ответа при валидном входе"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, password, _ = create_fake_user
        with allure.step('Входим на сайт'):
            response = self.api_client.login(username, password)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 302

    @allure.feature('API tests')
    @allure.story('Sign in api story')
    def test_sign_in_invalid(self, get_fake_user_info):
        """Проверка кода ответа при невалидном входе"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, _ = get_fake_user_info
        with allure.step('Входим на сайт'):
            response = self.api_client.login(username, password, status_code=401)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 401

    @allure.feature('API tests')
    @allure.story('Reg api story')
    def test_reg_user_1(self, get_fake_user_info):
        """Проверка кода ответа при валидной регистрации"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
        with allure.step('Регистрируем нового пользователя'):
            try:
                response = self.api_client.reg_user(username, password, password, email, autoremove=True)
            except ResponseStatusCodeException as exception:
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 201

    @allure.feature('API tests')
    @allure.story('Reg api story')
    def test_reg_user_2(self, get_fake_user_info):
        """Приверка кода ответа при невалидной регистрации"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Получаем информацию о невалидном пользователе'):
            username, password, email = get_fake_user_info
            username = username * 5
        with allure.step('Регистрируем невалидного пользователя'):
            resposne = self.api_client.reg_user(username, password, password, email, status_code=400)
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert resposne.status_code == 400

    @allure.feature('API tests')
    @allure.story('Reg api story')
    def test_reg_user_3(self, create_fake_user):
        """Проверка кода ответа при совпадении поля username с уже существующим в БД"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, password, email = create_fake_user
        with allure.step('Регистрируем пользователя при совпадении поля username с уже существующим в БД'):
            response = self.api_client.reg_user(username, password, password, email + 'q', status_code=409)
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 409

    @allure.feature('API tests')
    @allure.story('Reg api story')
    def test_reg_user_4(self, create_fake_user):
        """Проверка кода ответа при совпадении поля email с уже существующим в БД"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, password, email = create_fake_user
        with allure.step('Регистрируем пользователя при совпадении поля email с уже существующим в БД'):
            try:
                response = self.api_client.reg_user(username + 'q', password, password, email, status_code=409)
            except ResponseStatusCodeException as exception:
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 409

    @allure.feature('API tests')
    @allure.story('Add user api story')
    def test_add_user_1(self, get_fake_user_info):
        """Проверка кода ответа при валидном добавлении пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Получаем информацию о фейковом пользователе'):
            username, password, email = get_fake_user_info
        with allure.step('Добавляем нового пользователя'):
            try:
                response = self.api_client.add_user(username, password, email, autoremove=True)
            except ResponseStatusCodeException as exception:
                self.api_client.logout()
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 201

    @allure.feature('API tests')
    @allure.story('Add user api story')
    def test_add_user_2(self, add_fake_user):
        """Проверка валидного заполнения данных в БД при добавлении пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Добавляем данные о новом пользователе'):
            username = add_fake_user
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверка добавленных данных'):
            user_info = self.db_interaction.get_user_info(username)
            assert user_info['access'] == 1 and user_info['active'] == 0 and user_info['start_active_time'] is None

    @allure.feature('API tests')
    @allure.story('Add user api story')
    @pytest.mark.parametrize('len_username', [1, 2, 3, 4, 5, 6, 20])
    def test_add_user_3(self, len_username, get_fake_user_info):
        """Проверка валидации длины поля username"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log_{len_username}.txt')
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Создаём фейковые данные пользователя'):
            username, password, email = get_fake_user_info
            if len(username) < len_username:
                username *= 5
                username = username[:len_username]
            else:
                username = username[:len_username]
        with allure.step('Добавляем данные о пользователе'):
            try:
                response = self.api_client.add_user(username, password, email, autoremove=True)
            except ResponseStatusCodeException as exception:
                self.api_client.logout()
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 400

    @allure.feature('API tests')
    @allure.story('Add user api story')
    def test_add_user_4(self, create_fake_user):
        """Проверка создания пользователя при совпадении поля username с уже существующим в БД"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, password, email = create_fake_user
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Добавляем данные о пользователе'):
            response = self.api_client.add_user(username, password, email + 'q', status_code=304)
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 304

    @allure.feature('API tests')
    @allure.story('Add user api story')
    def test_add_user_5(self, create_fake_user):
        """Проверка создания пользователя при совпадении поля email с уже существующим в БД"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, password, email = create_fake_user
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Добавляем данные о пользователе'):
            try:
                response = self.api_client.add_user(username + 'q', password, email, status_code=409)
            except ResponseStatusCodeException as exception:
                self.api_client.logout()
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 409

    @allure.feature('API tests')
    @allure.story('Add user api story')
    @pytest.mark.parametrize('part_of_email', [0, 1])
    def test_add_user_6(self, get_fake_user_info, part_of_email):
        """Проверка создания пользователя с невалидным полем email"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log_{part_of_email}.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, password, email = get_fake_user_info
            if len(username) > 17:
                username = username[:10]
            if part_of_email == 1:
                email = '@' + email.split('@')[part_of_email]
            else:
                email = email.split('@')[part_of_email]
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Добавляем данные о пользователе'):
            try:
                response = self.api_client.add_user(username, password, email, autoremove=True, status_code=400)
            except ResponseStatusCodeException as exception:
                self.api_client.logout()
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 400

    @allure.feature('API tests')
    @allure.story('Add user api story')
    def test_add_user_7(self, get_fake_user_info):
        """Проверка создания пользователя с невалидной длиной поля email"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, password, email = get_fake_user_info
            if len(username) > 17:
                username = username[:10]
            email = email * 100
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Добавляем данные о пользователе'):
            try:
                response = self.api_client.add_user(username, password, email, status_code=400)
            except ResponseStatusCodeException as exception:
                self.api_client.logout()
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 400

    @allure.feature('API tests')
    @allure.story('Add user api story')
    def test_add_user_8(self, get_fake_user_info):
        """Проверка создания пользователя с некорректной длиной поля password"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, password, email = get_fake_user_info
            password = password * 200
            if len(username) > 17:
                username = username[:10]
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Добавляем данные о пользователе'):
            try:
                response = self.api_client.add_user(username, password, email, status_code=400)
            except ResponseStatusCodeException as exception:
                self.api_client.logout()
                self.logger.stop_logging()
                allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
                raise exception
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 400

    @allure.feature('API tests')
    @allure.story('Del user api story')
    def test_del_user_1(self, add_fake_user):
        """Проверка удаления данных о пользователе из БД"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Добавляем данные о новом пользователе'):
            username = add_fake_user
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Удаляем данные о пользователе'):
            response = self.api_client.del_user(username)
        with allure.step('Проверяем отсутствие данных в БД'):
            with pytest.raises(UserNotFoundException):
                user_info = self.db_interaction.get_user_info(username)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 204

    @allure.feature('API tests')
    @allure.story('Del user api story')
    def test_del_user_2(self, get_fake_user_info):
        """Проверка удаления данных о несуществующем пользователе"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, _, _ = get_fake_user_info
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Удаляем данные о несуществующем пользователе'):
            response = self.api_client.del_user(username, status_code=404)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 404

    @allure.feature('API tests')
    @allure.story('Block user api story')
    def test_block_user_1(self, create_fake_user):
        """Проверка блокировки существующего пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, _, _ = create_fake_user
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Блокируем существующего пользователя'):
            response = self.api_client.block_user(username)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем данные заблокированного пользователя'):
            user_info = self.db_interaction.get_user_info(username)
            assert response.status_code == 200 and user_info['access'] == 0 and user_info['active'] == 0

    @allure.feature('API tests')
    @allure.story('Block user api story')
    def test_block_user_2(self, get_fake_user_info):
        """Проверка блокировки несуществующего пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, _, _ = get_fake_user_info
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Блокируем несуществующего пользователя'):
            response = self.api_client.block_user(username, status_code=404)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 404

    @allure.feature('API tests')
    @allure.story('Block user api story')
    def test_block_user_3(self, create_fake_user):
        """Проверка блокировки активного пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, _, _ = create_fake_user
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Делаем пользователя активным'):
            self.db_interaction.edit_user_info(
                username=username,
                new_access=1,
                new_active=1
            )
        with allure.step('Блокируем активного пользователя'):
            response = self.api_client.block_user(username)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем данные заблокированного пользователя'):
            user_info = self.db_interaction.get_user_info(username)
            assert user_info['access'] == 0 and user_info['active'] == 0

    @allure.feature('API tests')
    @allure.story('Block user api story')
    def test_block_user_4(self, create_fake_user):
        """Проверка блокировки заблокированного пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, _, _ = create_fake_user
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Делаем пользователя заблокированным'):
            self.db_interaction.edit_user_info(
                username=username,
                new_access=0,
                new_active=0
            )
        with allure.step('Блокируем заблокированного пользователя'):
            response = self.api_client.block_user(username, status_code=304)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 304

    @allure.feature('API tests')
    @allure.story('Accept user api story')
    def test_accept_user_1(self, create_fake_user):
        """Проверка разблокировки пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, _, _ = create_fake_user
        with allure.step('Делаем пользователя заблокированным'):
            self.db_interaction.edit_user_info(
                username,
                new_access=0
            )
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Разблокируем пользователя'):
            response = self.api_client.accept_user(username)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем данные разблокированного пользователя'):
            user_info = self.db_interaction.get_user_info(username)
            assert response.status_code == 200 and user_info['access'] == 1

    @allure.feature('API tests')
    @allure.story('Accept user api story')
    def test_accept_user_2(self, get_fake_user_info):
        """Проверка разблокировки несуществующего пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём фейковые данные пользователя'):
            username, _, _ = get_fake_user_info
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Разблокируем несуществующего пользователя'):
            response = self.api_client.accept_user(username, status_code=404)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 404

    @allure.feature('API tests')
    @allure.story('Accept user api story')
    def test_accept_user_3(self, create_fake_user):
        """Проверка разблокировки разблокированного пользователя"""
        self.logger.start_logging(f'./project/app_logs/{inspect.getframeinfo(inspect.currentframe()).function}_api_log.txt')
        with allure.step('Создаём информацию о фейковом пользователе'):
            username, _, _ = create_fake_user
        with allure.step('Даём доступ пользователю'):
            self.db_interaction.edit_user_info(
                username,
                new_access=1
            )
        with allure.step('Входим на сайт'):
            self.api_client.login()
        with allure.step('Разблокируем разблокированного пользователя'):
            response = self.api_client.accept_user(username, status_code=304)
        with allure.step('Выходим с сайта'):
            self.api_client.logout()
        self.logger.stop_logging()
        allure.attach(self.logger.get_log_info(), 'App log', allure.attachment_type.TEXT)
        with allure.step('Проверяем код ответа'):
            assert response.status_code == 304

from ui.locators.locators import LoginPageLocators
from ui.pages.base import BaseActions
from ui.utils.additional_structures import wait
from ui.utils.exceptions import InvalidLoginInfoException, NoSuchElementException


class LoginPage(BaseActions):
    locators = LoginPageLocators()

    def paste_sign_in_info(self, username, password):
        self.paste_some_query_into_form(self.locators.USERNAME_LOGIN_FIELD, username)
        self.paste_some_query_into_form(self.locators.PASSWORD_LOGIN_FIELD, password)

    def click_sign_in_button(self):
        self.click(self.locators.SIGN_IN_BUTTON)

    def get_welcome_text(self):
        return self.find(self.locators.WELCOME_TEXT_FIELD).text

    def check_native_validation(self):
        return self.find(self.locators.USERNAME_LOGIN_FIELD).get_attribute('required') and self.find(self.locators.PASSWORD_LOGIN_FIELD).get_attribute('required')

    def sign_in(self, username, password, home_page_object):
        self.paste_sign_in_info(username, password)
        self.click_sign_in_button()
        try:
            if wait(func=self.check_available_of_element(self.locators.POP_UP_ERR_FIELD, auto_use=False), timeout=1):
                raise InvalidLoginInfoException(self.find(self.locators.POP_UP_ERR_FIELD).text)
        except NoSuchElementException:
            return home_page_object

    def sign_up(self, reg_page_object):
        self.click(self.locators.SIGN_UP_BUTTON)
        return reg_page_object

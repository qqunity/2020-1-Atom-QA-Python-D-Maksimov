from ui.locators.locators import RegPageLocators
from ui.pages.base import BaseActions
from ui.utils.additional_structures import wait
from ui.utils.exceptions import InvalidRegInfoException, NoSuchElementException


class RegPage(BaseActions):
    locators = RegPageLocators()

    def paste_sign_up_info(self, username, email, password, wrong_password=None):
        self.paste_some_query_into_form(self.locators.USERNAME_REG_FIELD, username)
        self.paste_some_query_into_form(self.locators.EMAIL_REG_FIELD, email)
        self.paste_some_query_into_form(self.locators.PASSWORD_REG_FIELD, password)
        self.paste_some_query_into_form(self.locators.PASSWORD_CONF_REG_FIELD, password if wrong_password is None else wrong_password)

    def click_accept_reg_button(self):
        self.click(self.locators.ACCEPT_REG_BUTTON)

    def click_submit_button(self):
        self.click(self.locators.SUBMIT_REG_BUTTON)

    def check_native_validation(self):
        return self.find(self.locators.USERNAME_REG_FIELD).get_attribute('required') and self.find(self.locators.EMAIL_REG_FIELD).get_attribute('required') and self.find(self.locators.PASSWORD_REG_FIELD).get_attribute('required') and self.find(self.locators.PASSWORD_CONF_REG_FIELD).get_attribute('required')

    def sign_up(self, username, email, password, home_page_object, wrong_password=None):
        self.paste_sign_up_info(username, email, password, wrong_password=wrong_password)
        self.click_accept_reg_button()
        self.click_submit_button()
        try:
            if wait(func=self.check_available_of_element(self.locators.POP_UP_ERR_FIELD, auto_use=False), timeout=1):
                raise InvalidRegInfoException(self.find(self.locators.POP_UP_ERR_FIELD).text)
        except NoSuchElementException:
            return home_page_object

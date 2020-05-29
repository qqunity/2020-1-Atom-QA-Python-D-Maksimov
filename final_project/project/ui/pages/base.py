import pytest
import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ui.locators.locators import BaseActionsLocators
from ui.utils.exceptions import NoSuchElementException


class BaseActions:
    base_locators = BaseActionsLocators()

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None) -> WebElement:
        try:
            return self.wait(timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise NoSuchElementException(f'No such element by locator "{locator}"')

    def alert(self, msg):
        script = f'alert("{msg}")'
        self.driver.execute_script(script)

    def click(self, locator, timeout=None):
        self.find(locator)
        element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def scroll_to_element(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def execute_script(self, script, element=None):
        self.driver.execute_script(script, element)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def wait_appear_quantity_elements(self, locator, count, timeout=1):
        self.wait(timeout).until(lambda browser: len(browser.find_elements(*locator)) == count)

    def paste_some_query_into_form(self, locator, query, timeout=None, clearing=True):
        form_field = self.find(locator, timeout)
        if clearing:
            form_field.clear()
        form_field.send_keys(query)

    def check_available_of_element(self, locator, auto_use=True):
        if auto_use:
            return self.find(locator).is_displayed()
        else:
            return self.find(locator).is_displayed

    def upload_file(self, upload_locator, submit_locator=None, file_path=None):
        upload_element = self.find(upload_locator)
        upload_element.send_keys(file_path)
        if submit_locator is not None:
            self.click(submit_locator)

    def refresh(self):
        self.driver.refresh()

    def move_to_element(self, locator):
        element = self.find(locator)
        ac = ActionChains(self.driver)
        ac.move_to_element(element).perform()

    def logout(self, login_page_object):
        self.click(self.base_locators.LOGOUT_BUTTON)
        return login_page_object
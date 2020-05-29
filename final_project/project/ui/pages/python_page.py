from ui.locators.locators import PythonPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class PythonPage(BaseThirdPartyPage):
    locators = PythonPageLocators()
    active_tab = False

    def get_current_url(self):
        return self.driver.current_url

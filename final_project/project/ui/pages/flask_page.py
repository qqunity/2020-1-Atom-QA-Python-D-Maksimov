from ui.locators.locators import FlaskPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class FlaskPage(BaseThirdPartyPage):
    locators = FlaskPageLocators()
    active_tab = False

    def get_welcome_text(self):
        if not self.active_tab:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.active_tab = True
        return self.find(self.locators.WELCOME_TEXT, timeout=20).text




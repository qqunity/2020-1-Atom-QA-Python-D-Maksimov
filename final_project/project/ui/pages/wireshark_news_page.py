from ui.locators.locators import WiresharkNewsPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class WiresharkNewsPage(BaseThirdPartyPage):
    locators = WiresharkNewsPageLocators()
    active_tab = False

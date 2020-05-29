from ui.locators.locators import FutureOfInternetPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class FutureOfInternetPage(BaseThirdPartyPage):
    locators = FutureOfInternetPageLocators()
    active_tab = False

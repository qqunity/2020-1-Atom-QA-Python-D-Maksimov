from ui.locators.locators import WiresharkDownloadPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class WiresharkDownloadPage(BaseThirdPartyPage):
    locators = WiresharkDownloadPageLocators()
    active_tab = False

from ui.locators.locators import CentosDownloadPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class CentosDownloadPage(BaseThirdPartyPage):
    locators = CentosDownloadPageLocators()
    active_tab = False

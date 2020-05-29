from ui.locators.locators import TcpDumpExamplesPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class TcpDumpExamplesPage(BaseThirdPartyPage):
    locators = TcpDumpExamplesPageLocators()
    active_tab = False

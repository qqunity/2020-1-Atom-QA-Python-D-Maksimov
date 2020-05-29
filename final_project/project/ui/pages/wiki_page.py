from ui.locators.locators import WikiPageLocators
from ui.pages.base_third_party_page import BaseThirdPartyPage


class WikiPage(BaseThirdPartyPage):
    locators = WikiPageLocators()
    active_tab = False

    def get_article_title(self):
        return self.find(self.locators.ARTICLE_TITLE).text

from ui.locators.locators import HomePageLocators
from ui.pages.base import BaseActions
from ui.utils.additional_structures import wait
from ui.utils.exceptions import InvalidLoginInfoException, NoSuchElementException


class HomePage(BaseActions):
    locators = HomePageLocators()

    def get_login_name_info(self):
        return self.find(self.locators.LOGIN_NAME_INFO).text

    def get_user_vk_id_info(self):
        return self.find(self.locators.USER_VK_IF_FIELD).text

    def click_logo_button(self):
        self.click(self.locators.LOGO_BUTTON)

    def go_to_home_page(self):
        self.click(self.locators.HOME_BUTTON)

    def go_to_python_history_page(self, wiki_page_object):
        self.move_to_element(self.locators.PYTHON_BUTTON)
        self.click(self.locators.PYTHON_HISTORY_BUTTON)
        return wiki_page_object

    def go_to_about_flask(self, flask_page_object):
        self.move_to_element(self.locators.PYTHON_BUTTON)
        self.click(self.locators.ABOUT_FLASK_BUTTON)
        return flask_page_object

    def go_to_download_centos(self, centos_download_page_object):
        self.move_to_element(self.locators.LINUX_BUTTON)
        self.click(self.locators.DOWNLOAD_CENTOS_BUTTON)
        return centos_download_page_object

    def go_to_wireshark_news(self, wireshark_news_page_object):
        self.move_to_element(self.locators.NETWORK_BUTTON)
        self.click(self.locators.WIRESHARK_NEWS_BUTTON)
        return wireshark_news_page_object

    def go_to_wireshark_download(self, wireshark_download_page_object):
        self.move_to_element(self.locators.NETWORK_BUTTON)
        self.click(self.locators.WIRESHARK_DOWNLOAD_BUTTON)
        return wireshark_download_page_object

    def go_to_tcp_dump_examples(self,tcp_dump_examples_page_object):
        self.move_to_element(self.locators.NETWORK_BUTTON)
        self.click(self.locators.TCP_DUMP_EXAMPLES_BUTTON)
        return tcp_dump_examples_page_object

    def go_to_about_api(self, wiki_page_object):
        self.click(self.locators.ABOUT_API_BUTTON)
        return wiki_page_object

    def go_to_future_of_internet(self, future_of_internet_page_object):
        self.click(self.locators.FUTURE_OF_INTERNET_BUTTON)
        return future_of_internet_page_object

    def go_to_about_smtp(self, wiki_page_object):
        self.click(self.locators.ABOUT_SMTP_BUTTON)
        return wiki_page_object

    def go_to_python_org(self, python_page_object):
        self.click(self.locators.PYTHON_BUTTON)
        return python_page_object

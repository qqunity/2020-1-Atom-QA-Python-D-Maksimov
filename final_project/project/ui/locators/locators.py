from selenium.webdriver.common.by import By


class BaseActionsLocators:
    LOGOUT_BUTTON = (By.XPATH, '//a[@class="uk-button uk-button-danger"]')


class LoginPageLocators(BaseActionsLocators):
    USERNAME_LOGIN_FIELD = (By.XPATH, '//input[@class="uk-input uk-form-large"]')
    PASSWORD_LOGIN_FIELD = (By.XPATH, '//input[@class="uk-input uk-form-large uk-icon-eye"]')
    SIGN_IN_BUTTON = (By.XPATH, '//input[@class="uk-button uk-button-primary uk-button-large uk-width-1-1"]')
    POP_UP_ERR_FIELD = (By.XPATH, '//div[@id="flash"]')
    SIGN_UP_BUTTON = (By.XPATH, '//a[@href="/reg"]')
    WELCOME_TEXT_FIELD = (By.XPATH, '//h3[@class="uk-card-title uk-text-center"]')


class RegPageLocators(BaseActionsLocators):
    USERNAME_REG_FIELD = (By.XPATH, '//input[@id="username"]')
    EMAIL_REG_FIELD = (By.XPATH, '//input[@id="email"]')
    PASSWORD_REG_FIELD = (By.XPATH, '//input[@id="password"]')
    PASSWORD_CONF_REG_FIELD = (By.XPATH, '//input[@id="confirm"]')
    ACCEPT_REG_BUTTON = (By.XPATH, '//input[@id="term"]')
    SUBMIT_REG_BUTTON = (By.XPATH, '//input[@id="submit"]')
    POP_UP_ERR_FIELD = (By.XPATH, '//div[@id="flash"]')


class HomePageLocators(BaseActionsLocators):
    LOGIN_NAME_INFO = (By.XPATH, '//div[@id="login-name"]//li[1]')
    LOGO_BUTTON = (By.XPATH, '//a[@class="uk-navbar-brand uk-hidden-small"]')
    HOME_BUTTON = (By.XPATH, '//li//a[@href="/"]')
    PYTHON_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[2]')
    PYTHON_HISTORY_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[2]//ul/li[1]')
    ABOUT_FLASK_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[2]//ul/li[2]')
    LINUX_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[3]')
    DOWNLOAD_CENTOS_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[3]//li')
    NETWORK_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[4]')
    WIRESHARK_NEWS_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[4]/div/ul/li[1]//li[1]')
    WIRESHARK_DOWNLOAD_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[4]/div/ul/li[1]//li[2]')
    TCP_DUMP_EXAMPLES_BUTTON = (By.XPATH, '//ul[@class="uk-navbar-nav uk-hidden-small"]/li[4]/div/ul/li[2]//li[1]')
    ABOUT_API_BUTTON = (By.XPATH, '//div[@class="uk-width-1-3 uk-text-center uk-row-first"]')
    FUTURE_OF_INTERNET_BUTTON = (By.XPATH, '//div[@class="uk-width-1-3 uk-text-center"][1]')
    ABOUT_SMTP_BUTTON = (By.XPATH, '//div[@class="uk-width-1-3 uk-text-center"][2]')
    USER_VK_IF_FIELD = (By.XPATH, '//div[@id="login-name"]//li[2]')


class WikiPageLocators(BaseActionsLocators):
    ARTICLE_TITLE = (By.XPATH, '//h1[@id="firstHeading"]')


class FlaskPageLocators(BaseActionsLocators):
    WELCOME_TEXT = (By.XPATH, '//div[@class="hide-header section"]/p[1]')


class CentosDownloadPageLocators(BaseActionsLocators):
    pass


class WiresharkDownloadPageLocators(BaseActionsLocators):
    pass


class WiresharkNewsPageLocators(BaseActionsLocators):
    pass


class TcpDumpExamplesPageLocators(BaseActionsLocators):
    pass


class FutureOfInternetPageLocators(BaseActionsLocators):
    pass


class PythonPageLocators(BaseActionsLocators):
    pass

import pytest

from database_code.db_interaction.interaction import DbInteraction
from faker import Faker
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ui.pages.centos_download_page import CentosDownloadPage
from ui.pages.flask_page import FlaskPage
from ui.pages.future_of_internet_page import FutureOfInternetPage
from ui.pages.home_page import HomePage
from ui.pages.login_page import LoginPage
from ui.pages.python_page import PythonPage
from ui.pages.reg_page import RegPage
from ui.pages.tcp_dump_examples_page import TcpDumpExamplesPage
from ui.pages.wiki_page import WikiPage
from ui.pages.wireshark_download_page import WiresharkDownloadPage
from ui.pages.wireshark_news_page import WiresharkNewsPage
from ui.utils.additional_structures import get_selenoid_host
from ui.utils.exceptions import UnsupportedBrowserException
from vk_api_client.client import VkApiClient


@pytest.fixture(scope='function')
def get_fake_user_info():
    fake = Faker(locale='ru_RU')
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    if len(username) < 6:
        username *= 2
    elif len(username) > 16:
        username = username[:15]
    return username, password, email


@pytest.fixture(scope='function')
def create_fake_user(get_fake_user_info, get_database_interaction):
    username, password, email = get_fake_user_info
    db_interaction = get_database_interaction
    db_interaction.add_user_info(
        username=username,
        email=email,
        password=password
    )
    # db_interaction.get_all_users_info()
    yield username, password, email
    db_interaction.del_user_info(username)


@pytest.fixture(scope='session')
def get_database_interaction():
    db_interaction = DbInteraction()
    return db_interaction


@pytest.fixture(scope='function')
def get_home_page(login_page_object, home_page_object, get_fake_user_info, get_database_interaction, reg_page_object):
    db_interaction = get_database_interaction
    reg_page = login_page_object.sign_up(reg_page_object)
    username, password, email = get_fake_user_info
    reg_page.sign_up(
        username=username,
        email=email,
        password=password,
        home_page_object=home_page_object
    )
    yield home_page_object, username
    db_interaction.del_user_info(username)


@pytest.fixture(scope='function')
def login_page_object(driver):
    return LoginPage(driver)


@pytest.fixture(scope='function')
def reg_page_object(driver):
    return RegPage(driver)


@pytest.fixture(scope='function')
def home_page_object(driver):
    return HomePage(driver)


@pytest.fixture(scope='function')
def wiki_page_object(driver):
    return WikiPage(driver)


@pytest.fixture(scope='function')
def flask_page_object(driver):
    return FlaskPage(driver)


@pytest.fixture(scope='function')
def centos_download_page_object(driver):
    return CentosDownloadPage(driver)


@pytest.fixture(scope='function')
def wireshark_download_page_object(driver):
    return WiresharkDownloadPage(driver)


@pytest.fixture(scope='function')
def wireshark_news_page_object(driver):
    return WiresharkNewsPage(driver)


@pytest.fixture(scope='function')
def tcp_dump_examples_page_object(driver):
    return TcpDumpExamplesPage(driver)


@pytest.fixture(scope='function')
def future_of_internet_page_object(driver):
    return FutureOfInternetPage(driver)


@pytest.fixture(scope='function')
def python_page_object(driver):
    return PythonPage(driver)


@pytest.fixture(scope='function')
def get_vk_api_client():
    return VkApiClient()


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url']
    download_dir = config['download_dir']
    selenoid_remote_ser = config['selenoid_remote_ser']

    if browser == 'chrome':
        if selenoid_remote_ser is None:
            options = ChromeOptions()

            prefs = {"download.default_directory": download_dir}
            options.add_experimental_option('prefs', prefs)

            capabilities = {'acceptInsecureCerts': True}

            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install(),
                                      options=options,
                                      desired_capabilities=capabilities
                                      )
        else:
            options = ChromeOptions()
            prefs = {"download.default_directory": download_dir}
            options.add_experimental_option('prefs', prefs)

            capabilities = {'acceptInsecureCerts': True,
                            'browserName': browser,
                            'version': '80',
                            }
            url = config['docker_url']

            driver = webdriver.Remote(command_executor='http://' + str(selenoid_remote_ser) + '/wd/hub/',
                                      options=options,
                                      desired_capabilities=capabilities
                                      )
    elif browser == 'firefox':
        manager = GeckoDriverManager(version=version)
        driver = webdriver.Firefox(executable_path=manager.install())

    else:
        raise UnsupportedBrowserException(f'Usupported browser: "{browser}"')

    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.close()

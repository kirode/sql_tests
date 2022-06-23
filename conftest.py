from pytest import fixture
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default=False)


@fixture()
def config(request):
    browser = request.config.getoption("--browser")
    headless = False
    if request.config.getoption("--headless"):
        headless = True

    return {"browser": browser,
            "headless": headless}


def get_chrome_options(config):
    options = ChromeOptions()
    options.headless = config["headless"]
    return options


def get_firefox_options(config):
    options = FirefoxOptions()
    options.headless = config["headless"]
    return options


def create_local_driver(config):
    driver = None
    if config["browser"] == "chrome":
        driver_manager = ChromeDriverManager()
        service = ChromeService
        options = get_chrome_options(config)
        driver = webdriver.Chrome(service=service(driver_manager.install()), options=options)

    elif config["browser"] == "firefox":
        driver_manager = GeckoDriverManager()
        service = FirefoxService
        options = get_firefox_options(config)
        driver = webdriver.Firefox(service=service(driver_manager.install()), options=options)

    return driver


@fixture()
def driver(config):
    driver = create_local_driver(config)
    driver.maximize_window()
    yield driver
    driver.quit()

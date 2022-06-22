from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement


class Widget:
    _url = 'https://www.w3schools.com'

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def _get_element(self, locator: tuple, timeout=10) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            expected.visibility_of_element_located(locator))

    def _get_elements(self, locator: tuple, timeout=10) -> list[WebElement]:
        return WebDriverWait(self.driver, timeout).until(
            expected.visibility_of_any_elements_located(locator))

    def _get_element_with_text(self, locator: tuple, text, timeout=10) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            expected.text_to_be_present_in_element(locator, text))

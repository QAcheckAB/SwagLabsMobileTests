import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class CheckoutCompletePage(DriverCommands):
    SELECTORS = {
        "CHECKOUT_COMPLETE_CONTEXT": {
        "android": (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT: COMPLETE!"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, "")
    }
    }

    def __init__(self, driver: WebDriver, platform: str) -> None:
        DriverCommands.__init__(self, driver)
        self.driver = driver
        self.platform = platform
        self.wait = WaitCommands(self.driver)
        self.swipe = Swipe(self.driver)

    @allure.step("Wait for page loaded")
    def wait_for_page_loaded(self) -> None:
        self.wait.wait_for_element_visibility(self.SELECTORS['CHECKOUT_COMPLETE_CONTEXT'][self.platform])

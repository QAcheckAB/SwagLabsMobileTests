import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from utils.driver_commands import DriverCommands


class NavBar(DriverCommands):
    SELECTORS = {
        "CART_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Cart"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CART_PRODUCT_COUNT": {
            "android": (AppiumBy.XPATH, "//android.widget.TextView"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
    }

    def __init__(self, driver: WebDriver, platform: str) -> None:
        DriverCommands.__init__(self, driver)
        self.driver = driver
        self.platform = platform

    @allure.step("Click cart button")
    def click_cart_button(self) -> None:
        self.click_element(self.SELECTORS["CART_BUTTON"][self.platform])

    @allure.step("Check cart button label")
    def check_cart_button_label(self, expected_label: str) -> None:
        add_cart_selector = self.SELECTORS["CART_BUTTON"][self.platform]
        add_cart_label_selector = self.SELECTORS["CART_PRODUCT_COUNT"][self.platform]
        add_cart_button_label = self.find_child_element_in_parent_element(
            add_cart_selector, add_cart_label_selector
        )
        add_cart_button_label_text = add_cart_button_label.text.rstrip()
        assert (
            add_cart_button_label_text == expected_label
        ), f"Cart label is incorrect. Expected {expected_label} but got {add_cart_button_label_text}"  # noqa E501

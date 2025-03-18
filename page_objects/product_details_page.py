import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class ProductDetailsPage(DriverCommands):
    SELECTORS = {
        "PRODUCT_CONTENT": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("test-Inventory item page")',
            ),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_TITLE": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("test-Description").childSelector(new UiSelector().className("android.widget.TextView").instance(0))',  # noqa E501
            ),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "ADD_TO_CART_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_PRICE": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Price"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
    }

    def __init__(self, driver: WebDriver, platform: str) -> None:
        DriverCommands.__init__(self, driver)
        self.driver = driver
        self.platform = platform
        self.wait = WaitCommands(self.driver)
        self.swipe = Swipe(self.driver)

    @allure.step("Wait for page loaded")
    def wait_for_page_loaded(self) -> None:
        self.wait.wait_for_element_visibility(self.SELECTORS["PRODUCT_CONTENT"][self.platform])

    @allure.step("Get product name")
    def get_product_name(self) -> str:
        return self.get_text_from_element(self.SELECTORS["PRODUCT_TITLE"][self.platform])

    @allure.step("Add to cart")
    def add_to_cart(self) -> None:
        add_to_cart_button_selector = self.SELECTORS["ADD_TO_CART_BUTTON"][self.platform]
        self.swipe.swipe_to_object_down(add_to_cart_button_selector)
        self.click_element(add_to_cart_button_selector)

    @allure.step("Get product price")
    def get_product_price(self) -> str:
        product_price_selector = self.SELECTORS["PRODUCT_PRICE"][self.platform]
        self.swipe.swipe_to_object_down(product_price_selector)
        return self.get_text_from_element(product_price_selector)

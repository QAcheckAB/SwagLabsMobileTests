from typing import List

import allure
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver

from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class CheckoutOverviewPage(DriverCommands):
    SELECTORS = {
        "CHECKOUT_OVERVIEW_LABEL": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("CHECKOUT: OVERVIEW")',
            ),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CART_ITEMS": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("test-Item")'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_TEXT": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("test-Description").childSelector(new UiSelector().className("android.widget.TextView").instance(0))',  # noqa E501
            ),
        },
        "PRODUCT_PRICE": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("test-Price").childSelector(new UiSelector().className("android.widget.TextView").instance(0))',  # noqa E501
            ),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_QUANTITY": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().description("test-Amount").childSelector(new UiSelector().className("android.widget.TextView").instance(0))',  # noqa E501
            ),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "ITEM_TOTAL": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Item total: $")',
            ),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "TAX": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Tax: $")'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "TOTAL": {
            "android": (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().textContains("Total: $%s")',
            ),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "FINISH_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-FINISH"),
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
        self.wait.wait_for_element_visibility(
            self.SELECTORS["CHECKOUT_OVERVIEW_LABEL"][self.platform]
        )

    @allure.step("Get all products on overview")
    def get_products_on_overview(self) -> List[WebElement]:
        return self.find_elements(self.SELECTORS["CART_ITEMS"][self.platform])

    @allure.step("Get amount of all products on overview")
    def get_amount_of_products_on_overview(self) -> int:
        return len(self.get_products_on_overview())

    @allure.step("Assert amount of products on overview")
    def assert_amount_of_products_on_overview(self, expected_amount: int) -> None:
        product_amounts = self.get_amount_of_products_on_overview()
        assert (
            product_amounts == expected_amount
        ), f"Amount of items on overview is incorrect, expected {expected_amount} but got {product_amounts}"  # noqa E501

    @allure.step("Get product based on index")
    def get_product(self, product_index: int) -> WebElement:
        return self.get_products_on_overview()[product_index]

    @allure.step("Get product name based on index")
    def get_product_name(self, product_index: int) -> str:
        product_text_selector = self.SELECTORS["PRODUCT_TEXT"][self.platform]
        return self.find_child_element_in_parent_element(
            self.get_product(product_index), product_text_selector
        ).text.rstrip()

    @allure.step("Assert product name")
    def assert_product_name(self, product_index: int, expected_name: str) -> None:
        product_name = self.get_product_name(product_index)
        assert (
            product_name == expected_name
        ), f"Product name is incorrect, expected {expected_name} but got {product_name}"

    @allure.step("Get product price based on index")
    def get_product_price(self, product_index: int) -> str:
        product_price_selector = self.SELECTORS["PRODUCT_PRICE"][self.platform]
        return self.find_child_element_in_parent_element(
            self.get_product(product_index), product_price_selector
        ).text.rstrip()

    @allure.step("Assert product price")
    def assert_product_price(self, product_index: int, expected_price: str) -> None:
        product_price = self.get_product_price(product_index)
        assert (
            product_price == expected_price
        ), f"Product price is incorrect, expected {expected_price} but got {product_price}"

    @allure.step("Get product quantity")
    def get_product_quantity(self, product_index: int) -> str:
        product_quantity_selector = self.SELECTORS["PRODUCT_QUANTITY"][self.platform]
        return self.find_child_element_in_parent_element(
            self.get_product(product_index), product_quantity_selector
        ).text.rstrip()

    @allure.step("Assert product quantity")
    def assert_product_quantity(self, product_index: int, expected_quantity: str) -> None:
        product_quantity = self.get_product_quantity(product_index)
        assert (
            product_quantity == expected_quantity
        ), f"Product quantity is incorrect, expected {expected_quantity} but got {product_quantity}"  # noqa E501

    @allure.step("Click finish button")
    def click_finish_button(self) -> None:
        self.click_element(self.SELECTORS["FINISH_BUTTON"][self.platform])

    @allure.step("Assert item total value")
    def assert_item_total_value(self, expected_value: str) -> None:
        item_total_selector = self.SELECTORS["ITEM_TOTAL"][self.platform]
        self.swipe.swipe_to_object_down(item_total_selector)
        item_total_value = self.get_text_from_element(item_total_selector)
        assert (
            item_total_value == f"Item total: {expected_value}"
        ), f"Item total value is incorrect, expected {expected_value} but got {item_total_value}"

    @allure.step("Assert tax value")
    def assert_tax_value(self, expected_value: str) -> None:
        tax_selector = self.SELECTORS["TAX"][self.platform]
        self.swipe.swipe_to_object_down(tax_selector)
        tax_value = self.get_text_from_element(tax_selector)
        assert (
            tax_value == f"Tax: ${expected_value}"
        ), f"Tax value is incorrect, expected {expected_value} but got {tax_value}"

    @allure.step("Assert total value")
    def assert_total_value(self, expected_value: str) -> None:
        total_selector = (
            self.SELECTORS["TOTAL"][self.platform][0],
            self.SELECTORS["TOTAL"][self.platform][1] % expected_value,
        )
        self.swipe.swipe_to_object_down(total_selector)
        total_value = self.get_text_from_element(total_selector)
        assert (
            total_value == f"Total: ${expected_value}"
        ), f"Total value is incorrect, expected {expected_value} but got {total_value}"

    @allure.step("Assert checkout overview page")
    def assert_checkout_overview_page(
        self,
        products_amount: int,
        product_index: int,
        product_name: str,
        product_price: str,
        product_quantity: str,
        tax_value: str,
        total_price: str,
    ):
        self.assert_amount_of_products_on_overview(products_amount)
        self.assert_product_name(product_index, product_name)
        self.assert_product_price(product_index, product_price)
        self.assert_product_quantity(product_index, product_quantity)
        self.assert_item_total_value(product_price)
        self.assert_tax_value(str(tax_value))
        self.assert_total_value(str(total_price))

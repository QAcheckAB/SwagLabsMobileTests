# -*- coding: UTF-8 -*-
import allure
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal, List

from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class CartDetailsPage(DriverCommands):
    SELECTORS = {
        "CART_CONTENT": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Cart Content"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CART_ITEMS": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"test-Item\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CONTINUE_SHOPPING_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE SHOPPING"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CHECKOUT_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_DESCRIPTION": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Description"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_TEXT": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_PRICE": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("test-Price").childSelector(new UiSelector().className("android.widget.TextView").instance(0))'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "REMOVE_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE"),
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
        self.wait.wait_for_element_visibility(self.SELECTORS['CART_CONTENT'][self.platform])

    @allure.step("Get all items in cart")
    def get_items_in_cart(self) -> List[WebElement]:
        cart_id = self.SELECTORS['CART_CONTENT'][self.platform]
        items_id = self.SELECTORS['CART_ITEMS'][self.platform]
        return self.find_all_child_elements_in_parent_element(cart_id, items_id)

    @allure.step("Get all items in cart")
    def get_amount_of_items_in_cart(self) -> int:
        return len(self.get_items_in_cart())

    @allure.step("Assert amount of items in cart")
    def assert_amount_of_items_in_cart(self, expected_amount: int) -> None:
        assert self.get_amount_of_items_in_cart() == expected_amount, f"Amount of items in cart is incorrect, expected {expected_amount} but got {self.get_items_in_cart()}"

    @allure.step("Get product")
    def get_product(self, product_index) -> WebElement:
        return self.get_items_in_cart()[product_index]

    @allure.step("Get product description")
    def get_product_description(self, product_index: int) -> str:
        product_description_selector = self.SELECTORS['PRODUCT_DESCRIPTION'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product(product_index), product_description_selector)

    @allure.step("Get product description")
    def get_first_text_from_product_description(self, product_index: int) -> str:
        product_text_selector = self.SELECTORS['PRODUCT_TEXT'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product_description(product_index),product_text_selector).text.rstrip()

    @allure.step("Assert product name")
    def assert_product_name(self, product_index:int, expected_name: str) -> None:
        assert self.get_first_text_from_product_description(product_index) == expected_name, f"Product description does not include product name, expected {expected_name} should be found in  {self.get_product_description(product_index)}"

    @allure.step("Get first product price")
    def get_product_price(self, product_index:int) -> str:
        product_price_selector = self.SELECTORS['PRODUCT_PRICE'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product(product_index), product_price_selector).text.rstrip()

    @allure.step("Assert product price")
    def assert_product_price(self, product_index:int, expected_price: str) -> None:
        assert self.get_product_price(product_index) == expected_price, f"Incorrect product price, expected {expected_price} but got {self.get_product_price(product_index)}"

    @allure.step("Check remove button visibility")
    def check_if_remove_button_visible_on_product_item(self, product_index:int) -> None:
        remove_button = self.SELECTORS['REMOVE_BUTTON'][self.platform]
        self.find_child_element_in_parent_element(self.get_product(product_index), remove_button)

    @allure.step("Click continue shopping button")
    def click_continue_shopping_button(self) -> None:
        continue_button_id = self.SELECTORS['CONTINUE_SHOPPING_BUTTON'][self.platform]
        self.swipe.swipe_to_object_down(continue_button_id)
        self.click_element(continue_button_id)

    @allure.step("Click checkout button")
    def click_checkout_button(self) -> None:
        checkout_button_id = self.SELECTORS['CHECKOUT_BUTTON'][self.platform]
        self.swipe.swipe_to_object_down(checkout_button_id)
        self.click_element(checkout_button_id)




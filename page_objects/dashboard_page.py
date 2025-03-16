# -*- coding: UTF-8 -*-
import allure
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal, List
from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class DashboardPage(DriverCommands):
    SELECTORS = {
        "MENU_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Menu"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CART_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Cart"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "DASHBOARD_LABEL": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Cart drop zone"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCTS_CONTENT": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_ITEM": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"test-Item\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_TEXT": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"test-Item title\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_PRICE": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"test-Price\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "ADD_TO_CARD_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "REMOVE_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE"),
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
        self.wait = WaitCommands(self.driver)
        self.swipe = Swipe(self.driver)

    @allure.step("Wait for page loaded")
    def wait_for_page_loaded(self) -> None:
        self.wait.wait_for_element_visibility(self.SELECTORS['MENU_BUTTON'][self.platform])
        self.wait.wait_for_element_visibility(self.SELECTORS['DASHBOARD_LABEL'][self.platform])

    @allure.step("Click login button")
    def click_cart_button(self) -> None:
        self.click_element(self.SELECTORS['CART_BUTTON'][self.platform])

    @allure.step("Get product items")
    def get_products_items(self) -> List[WebElement]:
        return self.find_elements(self.SELECTORS['PRODUCT_ITEM'][self.platform])

    @allure.step("Get first product items")
    def get_first_product_item(self) -> WebElement:
        return self.get_products_items()[0]

    @allure.step("Get first product name")
    def get_first_product_name(self) -> str:
        product_text_selector = self.SELECTORS['PRODUCT_TEXT'][self.platform]
        return self.find_child_element_in_parent_element(self.get_first_product_item(), product_text_selector).text.rstrip()

    @allure.step("Get first product price")
    def get_first_product_price(self) -> str:
        product_price_selector = self.SELECTORS['PRODUCT_PRICE'][self.platform]
        return self.find_child_element_in_parent_element(self.get_first_product_item(), product_price_selector).text.rstrip()

    @allure.step("Add first product to cart")
    def add_first_product_to_cart(self) -> None:
        add_cart_selector = self.SELECTORS['ADD_TO_CARD_BUTTON'][self.platform]
        add_button = self.find_child_element_in_parent_element(self.get_first_product_item(), add_cart_selector)
        self.click_element(add_button)

    @allure.step("Check remove button visibility")
    def check_if_remove_button_visible_on_first_product_item(self) -> None:
        remove_button = self.SELECTORS['REMOVE_BUTTON'][self.platform]
        self.find_child_element_in_parent_element(self.get_first_product_item(), remove_button)

    @allure.step("Check cart button label")
    def check_cart_button_label(self, expected_label: str) -> None:
        add_cart_selector = self.SELECTORS['CART_BUTTON'][self.platform]
        add_cart_label_selector = self.SELECTORS['CART_PRODUCT_COUNT'][self.platform]
        add_cart_button_label = self.find_child_element_in_parent_element(add_cart_selector, add_cart_label_selector)
        assert add_cart_button_label.text.rstrip() == expected_label, f"Expected {expected_label} but got {add_cart_button_label.text()}"





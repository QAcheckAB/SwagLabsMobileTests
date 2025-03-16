# -*- coding: UTF-8 -*-
import allure
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import List

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

    @allure.step("Get all items on overview")
    def get_items_on_overview(self) -> List[WebElement]:
        cart_id = self.SELECTORS['CART_CONTENT'][self.platform]
        items_id = self.SELECTORS['CART_ITEMS'][self.platform]
        return self.find_all_child_elements_in_parent_element(cart_id, items_id)

    @allure.step("Get amount of all items on overview")
    def get_amount_of_items_on_overview(self) -> int:
        return len(self.get_items_on_overview())

    @allure.step("Assert amount of items on overview")
    def assert_amount_of_items_on_overview(self, expected_amount: int) -> None:
        assert self.get_items_on_overview() == expected_amount, f"Amount of items on overview is incorrect, expected {expected_amount} but got {self.get_items_on_overview()}"

    @allure.step("Get product based on index")
    def get_product(self, product_index:int) -> WebElement:
        return self.get_items_on_overview()[product_index]

    @allure.step("Get product name based on index")
    def get_product_name(self, product_index:int) -> str:
        product_text_selector = self.SELECTORS['PRODUCT_TEXT'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product(product_index),
                                                         product_text_selector).text.rstrip()

    @allure.step("Assert product name")
    def assert_product_name(self, product_index:int, expected_name: str) -> None:
        assert self.get_product(product_index) == expected_name, f"Incorrect product name, expected {expected_name} but got {self.get_product_name(product_index)}"

    @allure.step("Get product price")
    def get_product_price(self, product_index:int) -> str:
        product_price_selector = self.SELECTORS['PRODUCT_PRICE'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product(product_index),
                                                         product_price_selector).text.rstrip()

    @allure.step("Assert product price")
    def assert_product_price(self, product_index:int, expected_price: str) -> None:
        assert self.get_product_price(product_index) == expected_price, f"Incorrect product price, expected {expected_price} but got {self.get_product_price(product_index)}"

    @allure.step("Click finish button")
    def click_finish_button(self) -> None:
        self.click_element(self.SELECTORS['FINISH_BUTTON'][self.platform])

    @allure.step("Assert item total value")
    def assert_item_total_value(self, expected_value: str) -> None:
        item_total_selector = self.SELECTORS['ITEM_TOTAL'][self.platform]
        self.swipe.swipe_to_object_down(item_total_selector)
        item_total_value = self.get_text_from_element(item_total_selector)
        assert item_total_value == f"Item total: ${expected_value}", f"Incorrect item total value, expected {expected_value} but got {item_total_value}"

    @allure.step("Assert tax value")
    def assert_tax_value(self, expected_value: str) -> None:
        tax_selector = self.SELECTORS['TAX'][self.platform]
        self.swipe.swipe_to_object_down(tax_selector)
        tax_value = self.get_text_from_element(tax_selector)
        assert tax_selector == f"Tax: ${expected_value}", f"Incorrect tax value, expected {expected_value} but got {tax_value}"

    @allure.step("Assert total value")
    def assert_total_value(self, expected_value: str) -> None:
        total_selector = self.SELECTORS['TAX'][self.platform][0]
        self.swipe.swipe_to_object_down(total_selector)
        total_value = self.get_text_from_element(total_selector)
        assert total_value == f"Total: ${expected_value}", f"Incorrect total value, expected {expected_value} but got {tax_value}"


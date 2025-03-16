# -*- coding: UTF-8 -*-
import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal
from faker import Faker

from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class CheckoutPage(DriverCommands):
    SELECTORS = {
        "CHECKOUT_CONTENT": {
        "android": (AppiumBy.ACCESSIBILITY_ID, "test-Checkout: Your Info"),
        "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
    },
        "FIRST_NAME_INPUT": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-First Name"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "LAST_NAME_INPUT": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Last Name"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "POSTAL_CODE_INPUT": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CONTINUE_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "TEST_ERROR_MESSAGE":{
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Error message"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        }
    }

    def __init__(self, driver: WebDriver, platform: str) -> None:
        DriverCommands.__init__(self, driver)
        self.driver = driver
        self.platform = platform
        self.wait = WaitCommands(self.driver)
        self.swipe = Swipe(self.driver)
        self.faker = Faker()  # Create a Faker instance


    @allure.step("Wait for page loaded")
    def wait_for_page_loaded(self) -> None:
        self.wait.wait_for_element_visibility(self.SELECTORS['CHECKOUT_CONTENT'][self.platform])

    @allure.step("Insert first name")
    def insert_first_name(self) -> None:
        first_name_value = self.faker.first_name()
        self.type_text(self.SELECTORS['FIRST_NAME_INPUT'][self.platform], first_name_value)

    @allure.step("Insert last name")
    def insert_last_name(self) -> None:
        last_name_value = self.faker.last_name()
        self.type_text(self.SELECTORS['LAST_NAME_INPUT'][self.platform], last_name_value)

    @allure.step("Insert postal code")
    def insert_postal_code(self) -> None:
        postal_code_value = self.faker.postalcode()
        self.type_text(self.SELECTORS['POSTAL_CODE_INPUT'][self.platform], postal_code_value)

    @allure.step("Click continue button")
    def click_continue_button(self) -> None:
        continue_button_id = self.SELECTORS['CONTINUE_BUTTON'][self.platform]
        self.swipe.swipe_to_object_down(continue_button_id)
        self.click_element(continue_button_id)



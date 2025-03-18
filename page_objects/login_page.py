# -*- coding: UTF-8 -*-
import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal
from utils import ELEMENT

from utils.driver_commands import DriverCommands
from utils.file_manager import load_config_from_json
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class LoginPage(DriverCommands):
    SELECTORS = {
        "LOGIN_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "USER": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"%s\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "USERNAME": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Username"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PASSWORD": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Password"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "ERROR_MESSAGE": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Error message"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "ERROR_MESSAGE_TEXT": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'),
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
        self.wait.wait_for_element_visibility(self.SELECTORS['USERNAME'][self.platform])
        self.wait.wait_for_element_visibility(self.SELECTORS['PASSWORD'][self.platform])

    @allure.step("Click login button")
    def click_login_button(self) -> None:
        login_button_id = self.SELECTORS['LOGIN_BUTTON'][self.platform]
        self.swipe.swipe_to_object_up(login_button_id)
        self.click_element(login_button_id)

    @allure.step("Select_user_type")
    def select_user_type(self, user:Literal["standard", "locked_out", "problem"]) -> None:
        user_id = f"{user}_user"
        selector = (
            self.SELECTORS['USER'][self.platform][0],
            self.SELECTORS['USER'][self.platform][1] % user_id
        )
        self.swipe.swipe_to_object_down(selector)
        self.click_element(selector)

    @allure.step("Get user data")
    def get_user_data(self) -> dict:
        return load_config_from_json("users.json")

    @allure.step("Insert username")
    def insert_username(self, user:Literal["standard", "locked_out", "problem", ""]) -> None:
        # user_data: dict = load_config_from_json("users.json")
        user_credential = self.get_user_data()[user]["login"] if user else ""
        self.type_text(self.SELECTORS['USERNAME'][self.platform], user_credential)

    @allure.step("Insert password")
    def insert_password(self, user:Literal["standard", "locked_out", "problem", ""]) -> None:
        # user_data: dict = load_config_from_json("users.json")
        password = self.get_user_data()[user]["password"] if user else ""
        self.type_text(self.SELECTORS['PASSWORD'][self.platform], password)

    @allure.step("Log in to the app")
    def log_in(self, user:Literal["standard", "locked_out", "problem"]) -> None:
        user_data: dict = load_config_from_json("users.json")
        self.type_text(self.SELECTORS['USERNAME'][self.platform], user_data[user]["login"])
        self.type_text(self.SELECTORS['PASSWORD'][self.platform], user_data[user]["password"])
        self.click_element( self.SELECTORS['LOGIN_BUTTON'][self.platform])

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        error_message = self.wait.wait_for_element_visibility(self.SELECTORS['ERROR_MESSAGE'][self.platform])
        error_message_text_selector = self.SELECTORS['ERROR_MESSAGE_TEXT'][self.platform]
        error_message_text = self.find_child_element_in_parent_element(error_message, error_message_text_selector)
        return self.get_text_from_element(error_message_text)

    @allure.step("Validate error message field")
    def validate_error_message(self, expected_error: str) -> None:
        assert self.get_error_message() == expected_error, f"Incorrect error message, expected {expected_error} but got {self.get_error_message()}"


# -*- coding: UTF-8 -*-
import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal
from utils import ELEMENT

from utils.driver_commands import DriverCommands
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



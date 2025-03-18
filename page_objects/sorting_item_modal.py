import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal

from utils.driver_commands import DriverCommands
from utils.wait_commands import WaitCommands


class SortingItemModal(DriverCommands):
    SELECTORS = {
        "SORT_ITEM_CONTAINER": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "Selector container"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "SORTING_RULE": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("%s")'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
    }
    def __init__(self, driver: WebDriver, platform: str) -> None:
        DriverCommands.__init__(self, driver)
        self.driver = driver
        self.platform = platform
        self.wait = WaitCommands(self.driver)

    SORTING_RULES = {
        "name_ascending": "Name (A to Z)",
        "name_descending": "Name (Z to A)",
        "price_ascending": "Price (low to high)",
        "price_descending": "Price (high to low)"
    }

    @allure.step("Check sort item modal visibility")
    def check_sorting_modal_visibility(self) -> None:
        self.wait.wait_for_element_visibility(self.SELECTORS['SORT_ITEM_CONTAINER'][self.platform])

    @allure.step("Select sorting rule")
    def select_sorting_rule(self, sorting_name: Literal["name_ascending", "name_descending", "price_ascending", "price_descending"]) -> None:
        sorting_selector = (
            self.SELECTORS['SORTING_RULE'][self.platform][0],
            self.SELECTORS['SORTING_RULE'][self.platform][1] % self.SORTING_RULES[sorting_name]
        )
        self.click_element(sorting_selector)
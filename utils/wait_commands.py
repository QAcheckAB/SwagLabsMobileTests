import logging as log
import time
import warnings
from typing import Any, Callable, Optional, Tuple, Union

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from . import is_webelement
class WaitCommands:

    def __init__(self, driver: webdriver) -> None:
        self.driver: webdriver = driver
        self.interval: float = 0.5
        self.wait_time: int = 5

    def wait_for_element_visibility(
        self, selector: Tuple[str, str], wait: float = None
    ) -> WebElement:
        """Wait some time until expected element
        will be visible on current page
        :param selector: selector
        :param wait: time to wait
        """
        wait = wait or self.wait_time
        log.debug(f"Waiting {wait} seconds for visibility of element {selector}")
        try:
            element = WebDriverWait(self.driver, wait, poll_frequency=1).until(
                EC.visibility_of_element_located(selector)
            )
            log.debug(f"Element by {selector} is visible. (ID: {element.id})")
            return element
        except (TimeoutException, NoSuchElementException):
            raise AssertionError(f"Could not find element {selector}")

# -*- coding: utf-8 -*-
import logging as log
from typing import Tuple, Dict, Optional, Union, List

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver

from utils import ELEMENT, is_webelement
from utils.wait_commands import WaitCommands


class DriverCommands:

    def __init__(self, driver: webdriver) -> None:
        self.driver: webdriver = driver
        self.wait = WaitCommands(self.driver)


    def find_element(self, selector: ELEMENT, wait: Optional[float] = None) -> WebElement:
        """
        Finds element on the application view.

        :param selector: tuple (eg. By.ID, 'element/id') or WebElement
        :param wait: float, wait time to element visibility
        :return: WebElement, the found element
        """
        if is_webelement(selector):
            return selector
        if isinstance(selector, str):
            selector = (AppiumBy.XPATH, selector)
        element = self.wait.wait_for_presence_of_element(selector, wait)
        log.info(f"Found element with by: {selector}. {self.__get_text_or_id(element)}")
        return element

    def find_elements(self, selector: Tuple[str, str]) -> List[WebElement]:
        """
        Finds all elements with selector.

        :param selector: tuple (eg. By.ID, 'element/id')
        :return: List[WebElement], list of found elements
        """
        elements = self.driver.find_elements(*selector)
        log.info(f"Found {len(elements)} elements by {selector}")
        return elements

    def click_element(self, element: ELEMENT) -> None:
        """
        Find the specified element and click on it.

        :param element: The element to be clicked. It can be a tuple (e.g., (By.ID, 'element/id')) or a WebElement.
        :type element: ELEMENT
        :return: None
        """
        element = self.find_element(element)
        text = self.__get_text_or_id(element)
        element.click()
        log.info(f"Element clicked. {text}")

    def type_text(self, selector: ELEMENT, value: str) -> None:
        """
        Finds element, clear and enter text to the field.

        :param selector: tuple (eg. By.ID, 'element/id') or WebElement
        :param value: str, text to enter; if value is an empty string '', the input will only be
            cleared
        """
        element = self.find_element(selector)
        element.clear()
        if len(value) > 0:
            element.send_keys(value)
        log.info(f'"{value}" text send to input field. (ID: {element.id})')

    def get_text_from_element(self, element: ELEMENT) -> str:
        """
        Find element and get text from it.

        :param element: touple (eg. By.ID, 'element/id') or WebElement
        :return: text from element
        """
        element = self.find_element(element)
        return element.text.rstrip()

    def check_elements_text(self, element: ELEMENT, expected_text: str) -> None:
        """
        Find element, get text from it and compare with your expectation.

        :param element: element to get text
        :param expected_text: text to compare with text from element
        """
        element_text = self.get_text_from_element(element)
        assert (
            element_text == expected_text
        ),   "Wrong text. Should be '%s' instead of '%s'" % (expected_text, element_text)
        log.info(f'Text: {expected_text} is correct!')

    def find_child_element_in_parent_element(
            self,
            parent: ELEMENT,
            child: Tuple[str, str],
            wait: Optional[float] = None,
    ) -> WebElement:
        """
        Finds child element in the parent WebElement.

        :param parent: tuple (eg. By.ID, 'element/id') or WebElement
        :param child: tuple (eg. By.ID, 'element/id')
        :param wait: float, wait time for child element, default 10
        :return: WebElement, the found child element
        """
        module = self.find_element(selector=parent)
        wait_time = wait or 10
        element = WebDriverWait(module, wait_time).until(
            EC.presence_of_element_located(locator=child)
        )
        log.info(f"Found child element by selector: {child}. {self.__get_text_or_id(element)}")
        return element

    def find_all_child_elements_in_parent_element(self, parent: ELEMENT, child: Tuple[str, str]
    ) -> List[WebElement]:
        """
        Finds all child elements located in the parent WebElement.

        :param parent: tuple (eg. By.ID, 'element/id') or WebElement
        :param child: tuple (eg. By.ID, 'element/id')
        :return: List[WebElement], list of found child elements
        """
        if not isinstance(parent, WebElement):
            parent = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(parent))
        elements = parent.find_elements(child[0], child[1])
        log.debug(f"Found {len(elements)} elements")
        return elements

    def platform_name(self) -> str:
        """
        Gets the platform name of the driver.

        :return: the platform name in lowercase
        """
        return self.driver.capabilities.get("platformName").lower()

    def driver_is_android(self) -> bool:
        """
        Checks if the driver is for an Android device.

        :return: True if the platform is Android, False otherwise
        """
        return self.platform_name() == "android"

    def driver_is_ios(self) -> bool:
        """
        Checks if the driver is for an iOS device.

        :return: True if the platform is iOS, False otherwise
        """
        return self.platform_name() == "ios"

    @staticmethod
    def convert_selector(
        my_object: Union[WebElement, str, tuple], by=AppiumBy.XPATH
    ) -> Union[WebElement, tuple]:
        """
        Converts a given object to a selector tuple, this method takes an object that can be
        a WebElement, a string, or a tuple, and converts it to a selector tuple.

        :param my_object: the object to be converted to a selector
        :param by: the method to locate elements, defaults to AppiumBy.XPATH
        :return: the selector tuple
        """
        if isinstance(my_object, tuple):
            return my_object
        elif isinstance(my_object, str):
            return by, my_object
        else:
            raise ValueError("my_object must be a string or tuple")

    @staticmethod
    def __get_text_or_id(element: WebElement) -> str:
        """
        Gets the text or ID of the element.

        :param element: WebElement
        :return: str, text or ID of the element
        """
        return f"Text: {element.text}" if element.text else f"ID: {element.id}"
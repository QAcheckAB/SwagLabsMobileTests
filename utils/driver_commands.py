# -*- coding: utf-8 -*-
import logging as log
from typing import Tuple, Dict, Optional, Union

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from utils import ELEMENT


class DriverCommands:

    def __init__(self, driver: webdriver) -> None:
        self.driver: webdriver = driver

    def find_element(self, selector: ELEMENT) -> WebElement:
        """Find element on application view.

            :param selector: touple (eg. By.ID, 'element/id')
            :return: elements handler
        """
        if self.is_webelement(selector):
            return selector
        else:
            element = self.find_elements(selector)
            if len(element) == 0:
                self.on_exception()
                raise AssertionError(
                    f'Could not locate elements by parameters: {selector}')
            log.debug(f'found element by: {selector}')
            return element[0]

    def find_elements(self, selector: tuple) -> list:
        """Find all elemement on visible view with selector

            :param selector: elements selector
        """
        elements = self.driver.find_elements(*selector)
        log.debug(f'found {len(elements)} elements')
        return elements

    def click_element(self, element: ELEMENT) -> None:
        """Find element and click on it.

            :param element: touple (eg. By.ID, 'element/id') or Webelement
        """
        element = self.find_element(element)
        element.click()
        log.debug('Element clicked')

    def fill_in(self, selector: ELEMENT, value: str) -> None:
        """Find element and enter text to the field

            :param selector: touple (eg. By.ID, 'element/id')
            :param value: text
        """
        element = self.find_element(selector)
        element.clear()
        if len(value) > 0:
            element.send_keys(value)
        log.debug('Input field filled')

    def get_text_from_element(self, element: ELEMENT) -> str:
        """Find element and get text from it.

            :param element: touple (eg. By.ID, 'element/id') or WebElement
            :return: text from element
        """
        element = self.find_element(element)
        return element.text

    def check_elements_text(
            self, element: ELEMENT, expected_text: str) -> None:
        """Find element, get text from it and compare with your expectation.

            :param element: element to get text
            :param expected_text: text to compare with text from element
        """
        element_text = self.get_text_from_element(element)
        assert element_text == expected_text, \
            "Wrong text. Should be '%s' instead of '%s'" % (
                expected_text, element_text)
        log.debug(f'Text: {expected_text} is correct!')

    def is_webelement(self, selector: Union[WebElement, Tuple[str, str], str]) -> bool:
        return selector.__class__.__name__ == 'WebElement'

    def find_child_element_in_parent_element(
            self, parent_element, child_element):
        module = self.find_element(selector=parent_element)
        wait_time = 10
        return WebDriverWait(module, wait_time).until(
            EC.presence_of_all_elements_located(locator=child_element))[0]

    def find_all_child_elements_in_parent_element(
            self, parent_element, child_element):
        module = self.find_element(selector=parent_element)
        wait_time = 10
        return WebDriverWait(module, wait_time).until(
            EC.presence_of_all_elements_located(locator=child_element))

    def get_element_attribute(self, element: ELEMENT, attribute: str) -> str:
        """Find element and get attribute of that element."""
        element = self.find_element(element)
        return element.get_attribute(attribute)

    def platform_name(self) -> str:
        """
        gets the platform name of the driver
        :return: the platform name in lowercase
        """
        return self.driver.capabilities.get("platformName").lower()

    def driver_is_android(self) -> bool:
        """
        checks if the driver is for an Android device
        :return: True if the platform is Android, False otherwise
        """
        return self.platform_name() == "android"

    def driver_is_ios(self) -> bool:
        """
        checks if the driver is for an iOS device
        :return: True if the platform is iOS, False otherwise
        """
        return self.platform_name() == "ios"

    @staticmethod
    def convert_selector(
        my_object: Union[WebElement, str, tuple], by=AppiumBy.XPATH
    ) -> Union[WebElement, tuple]:
        """
        converts a given object to a selector tuple, this method takes an object that can be
        a WebElement, a string, or a tuple, and converts it to a selector tuple
        :param my_object: the object to be converted to a selector
        :param by: the method to locate elements, defaults to AppiumBy.XPATH
        :return: the selector tuple
        """
        if isinstance(my_object, tuple):
            return my_object
        elif isinstance(my_object, str):
            return (by, my_object)
        else:
            raise ValueError("my_object must be a string or tuple")
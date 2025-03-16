from __future__ import annotations
from typing import Union, Tuple

from appium.webdriver.webelement import WebElement

ELEMENT = Union[WebElement, Tuple[str, str], str]


def is_webelement(selector: ELEMENT) -> bool:
    return selector.__class__.__name__ == "WebElement"

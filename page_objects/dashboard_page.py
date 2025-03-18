import allure
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal, List, Union

from helper_methods.value_formatting import format_price_value_to_float
from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class DashboardPage(DriverCommands):
    SELECTORS = {
        "MENU_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Menu"),
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
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"test-ADD TO CART\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "REMOVE_BUTTON": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"test-REMOVE\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "SWITCH_VIEW_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Toggle"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "SORTING_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Modal Selector Button"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "SORTING_CONTAINER": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "Selector container"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "SORTING_RULES": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"%s\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "NAMES": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("test-Item title")'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRICES": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("test-Price")'),
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

    @allure.step("Get product items")
    def get_products_items(self) -> List[WebElement]:
        return self.find_elements(self.SELECTORS['PRODUCT_ITEM'][self.platform])

    @allure.step("Get product items based on index")
    def get_product_item_based_on_index(self, product_index:int) -> WebElement:
        return self.get_products_items()[product_index]

    @allure.step("Open product details")
    def open_products_details(self, product_index:int) -> None:
        self.click_element(self.get_product_item_based_on_index(product_index))

    @allure.step("Get product name based on index")
    def get_product_name(self, product_index: int) -> str:
        product_text_selector = self.SELECTORS['PRODUCT_TEXT'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product_item_based_on_index(product_index), product_text_selector).text.rstrip()

    @allure.step("Get product price based on index")
    def get_product_price(self, product_index: int) -> str:
        product_price_selector = self.SELECTORS['PRODUCT_PRICE'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product_item_based_on_index(product_index), product_price_selector).text.rstrip()

    @allure.step("Add product to cart")
    def add_product_to_cart(self, product_index: int) -> None:
        add_cart_selector = self.SELECTORS['ADD_TO_CARD_BUTTON'][self.platform]
        self.swipe.swipe_to_object_down(add_cart_selector)
        add_button = self.find_child_element_in_parent_element(self.get_product_item_based_on_index(product_index), add_cart_selector)
        self.click_element(add_button)

    @allure.step("Check remove button visibility")
    def check_if_remove_button_visible_on_product_item(self, product_index:int) -> None:
        remove_button = self.SELECTORS['REMOVE_BUTTON'][self.platform]
        self.find_child_element_in_parent_element(self.get_product_item_based_on_index(product_index), remove_button)

    @allure.step("Check add cart button visibility")
    def check_if_add_cart_button_visible_on_product_item(self, product_index:int) -> None:
        add_to_cart_button = self.SELECTORS['ADD_TO_CARD_BUTTON'][self.platform]
        self.find_child_element_in_parent_element(self.get_product_item_based_on_index(product_index), add_to_cart_button)

    @allure.step("Remove product")
    def remove_product(self, product_index:int) -> None:
        remove_button_selector = self.SELECTORS['REMOVE_BUTTON'][self.platform]
        remove_button = self.find_child_element_in_parent_element(self.get_product_item_based_on_index(product_index), remove_button_selector)
        self.click_element(remove_button)

    @allure.step("Switch view")
    def switch_view(self) -> None:
        self.click_element(self.SELECTORS['SWITCH_VIEW_BUTTON'][self.platform])

    @allure.step("Click sorting button")
    def click_sorting_button(self) -> None:
        self.click_element(self.SELECTORS['SORTING_BUTTON'][self.platform])

    @allure.step("Get all products names")
    def get_all_names(self) -> List[str]:
        visible_products_names = self.find_elements(self.SELECTORS['NAMES'][self.platform])
        names = list(map(lambda x: x.text, visible_products_names))
        return names

    @allure.step("Get all products prices")
    def get_all_prices(self) -> List[float]:
        visible_products_prices = self.find_elements(self.SELECTORS['PRICES'][self.platform])
        prices = list(map(lambda x: x.text, visible_products_prices))
        prices_as_float = list(map(lambda x: format_price_value_to_float(x), prices))
        return prices_as_float

    @allure.step("Assert sorting order")
    def assert_sorting_order(self, sorting_order: Literal['asc', 'desc'], list_to_check: Union[List[str], List[float]]) -> None:
        reverse_sorting = False if sorting_order == 'asc' else True
        assert sorted(list_to_check, reverse=reverse_sorting) == list_to_check, f"Sorting order is not correct, expected {sorted(list_to_check, reverse=reverse_sorting)} but got {list_to_check}"




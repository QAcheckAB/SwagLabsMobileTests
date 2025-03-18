import allure
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from typing import Literal, List

from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class CartDetailsPage(DriverCommands):
    SELECTORS = {
        "CART_CONTENT": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Cart Content"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CART_ITEMS": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"test-Item\")"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CONTINUE_SHOPPING_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE SHOPPING"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "CHECKOUT_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_TEXT": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("test-Description").childSelector(new UiSelector().className("android.widget.TextView").instance(0))'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "PRODUCT_PRICE": {
            "android": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("test-Price").childSelector(new UiSelector().className("android.widget.TextView").instance(0))'),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
            "PRODUCT_QUANTITY": {
        "android": (AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().description("test-Amount").childSelector(new UiSelector().className("android.widget.TextView").instance(0))'),
        "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
    },
        "REMOVE_BUTTON": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE"),
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
        self.wait.wait_for_element_visibility(self.SELECTORS['CART_CONTENT'][self.platform])

    @allure.step("Get all products in cart")
    def get_products_in_cart(self) -> List[WebElement]:
        cart_id = self.SELECTORS['CART_CONTENT'][self.platform]
        items_id = self.SELECTORS['CART_ITEMS'][self.platform]
        return self.find_all_child_elements_in_parent_element(cart_id, items_id)

    @allure.step("Get amount of products in cart")
    def get_amount_of_products_in_cart(self) -> int:
        return len(self.get_products_in_cart())

    @allure.step("Assert amount of products in cart")
    def assert_amount_of_products_in_cart(self, expected_amount: int) -> None:
        products_amount = self.get_amount_of_products_in_cart()
        assert products_amount == expected_amount, f"Amount of products in cart is incorrect, expected {expected_amount} but got {products_amount}"

    @allure.step("Get product based on index")
    def get_product(self, product_index) -> WebElement:
        return self.get_products_in_cart()[product_index]

    @allure.step("Get product name based on index")
    def get_product_name(self, product_index: int) -> str:
        product_text_selector = self.SELECTORS['PRODUCT_TEXT'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product(product_index),
                                                         product_text_selector).text.rstrip()

    @allure.step("Assert product name")
    def assert_product_name(self, product_index: int, expected_name: str) -> None:
        product_name = self.get_product_name(product_index)
        assert product_name == expected_name, f"Product name is incorrect, expected {expected_name} but got {product_name}"

    @allure.step("Get product price based on index")
    def get_product_price(self, product_index:int) -> str:
        product_price_selector = self.SELECTORS['PRODUCT_PRICE'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product(product_index), product_price_selector).text.rstrip()

    @allure.step("Assert product price")
    def assert_product_price(self, product_index:int, expected_price: str) -> None:
        product_price = self.get_product_price(product_index)
        assert product_price == expected_price, f"Product price is incorrect, expected {expected_price} but got {product_price}"

    @allure.step("Check remove button visibility")
    def check_if_remove_button_visible_on_product_item(self, product_index:int) -> None:
        remove_button = self.SELECTORS['REMOVE_BUTTON'][self.platform]
        self.find_child_element_in_parent_element(self.get_product(product_index), remove_button)

    @allure.step("Remove product from cart")
    def remove_product_from_cart(self, product_index:int) -> None:
        remove_button = self.SELECTORS['REMOVE_BUTTON'][self.platform]
        self.find_child_element_in_parent_element(self.get_product(product_index), remove_button)
        self.click_element(remove_button)

    @allure.step("Click continue shopping button")
    def click_continue_shopping_button(self) -> None:
        continue_button_id = self.SELECTORS['CONTINUE_SHOPPING_BUTTON'][self.platform]
        self.swipe.swipe_to_object_down(continue_button_id)
        self.click_element(continue_button_id)

    @allure.step("Click checkout button")
    def click_checkout_button(self) -> None:
        checkout_button_id = self.SELECTORS['CHECKOUT_BUTTON'][self.platform]
        self.swipe.swipe_to_object_down(checkout_button_id)
        self.click_element(checkout_button_id)

    @allure.step("Get product quantity")
    def get_product_quantity(self, product_index:int) -> str:
        product_quantity_selector = self.SELECTORS['PRODUCT_QUANTITY'][self.platform]
        return self.find_child_element_in_parent_element(self.get_product(product_index), product_quantity_selector).text.rstrip()

    @allure.step("Assert product quantity")
    def assert_product_quantity(self, product_index:int, expected_quantity: str) -> None:
        product_quantity = self.get_product_quantity(product_index)
        assert product_quantity == expected_quantity, f"Product quantity is incorrect, expected {expected_quantity} but got {product_quantity}"

    @allure.step("Assert cart details page")
    def assert_cart_details_page(
            self,
            product_index:int,
            expected_name: str,
            expected_price: str,
            expected_quantity: str
    ) -> None:
        self.assert_product_name(product_index, expected_name)
        self.assert_product_price(product_index, expected_price)
        self.assert_product_quantity(product_index, expected_quantity)
        self.check_if_remove_button_visible_on_product_item(product_index)
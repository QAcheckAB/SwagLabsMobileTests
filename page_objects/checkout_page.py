import allure
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from faker import Faker

from utils.driver_commands import DriverCommands
from utils.swipe import Swipe
from utils.wait_commands import WaitCommands


class CheckoutPage(DriverCommands):
    faker = Faker()
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
        "ERROR_MESSAGE": {
            "android": (AppiumBy.ACCESSIBILITY_ID, "test-Error message"),
            "ios": (AppiumBy.ACCESSIBILITY_ID, ""),
        },
        "ERROR_MESSAGE_TEXT": {
            "android": (
            AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")'),
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
        self.wait.wait_for_element_visibility(self.SELECTORS['CHECKOUT_CONTENT'][self.platform])

    @allure.step("Insert first name")
    def insert_first_name(self,first_name_value: str = faker.first_name()) -> None:
        self.type_text(self.SELECTORS['FIRST_NAME_INPUT'][self.platform], first_name_value)

    @allure.step("Insert last name")
    def insert_last_name(self, last_name_value: str = faker.last_name()) -> None:
        self.type_text(self.SELECTORS['LAST_NAME_INPUT'][self.platform], last_name_value)

    @allure.step("Insert postal code")
    def insert_postal_code(self, postal_code_value = faker.postalcode()) -> None:
        self.type_text(self.SELECTORS['POSTAL_CODE_INPUT'][self.platform], postal_code_value)

    @allure.step("Click continue button")
    def click_continue_button(self) -> None:
        continue_button_id = self.SELECTORS['CONTINUE_BUTTON'][self.platform]
        self.swipe.swipe_to_object_down(continue_button_id)
        self.click_element(continue_button_id)

    @allure.step("Fill in checkout info and continue")
    def fill_in_checkout_info_and_continue(
        self,
        first_name_value: str = faker.first_name(),
        last_name_value: str = faker.last_name(),
        postal_code_value=faker.postalcode()
    ) -> None:
        self.insert_first_name(first_name_value)
        self.insert_last_name(last_name_value)
        self.insert_postal_code(postal_code_value)
        self.click_continue_button()

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        error_message = self.wait.wait_for_element_visibility(
            self.SELECTORS['ERROR_MESSAGE'][self.platform])
        error_message_text_selector = self.SELECTORS['ERROR_MESSAGE_TEXT'][self.platform]
        error_message_text = self.find_child_element_in_parent_element(error_message,
                                                                       error_message_text_selector)
        return self.get_text_from_element(error_message_text)

    @allure.step("Validate error message")
    def validate_error_message(self, expected_error: str) -> None:
        error_message = self.get_error_message()
        assert error_message == expected_error, f"Error message is incorrect, expected {expected_error} but got {error_message}"



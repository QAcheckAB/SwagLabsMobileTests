import allure
from page_objects.cart_details_page import CartDetailsPage
from page_objects.checkout_complete_page import CheckoutCompletePage
from page_objects.checkout_overview_page import CheckoutOverviewPage
from page_objects.checkout_page import CheckoutPage
from page_objects.dashboard_page import DashboardPage
from page_objects.login_page import LoginPage
from tests.baseTest import BaseTest, safe_run


class ValidateErrorsOnCheckoutPageTests(BaseTest):
    FIRST_NAME_ERROR_MESSAGE = "First Name is required"
    LAST_NAME_ERROR_MESSAGE = "Last Name is required"
    POSTAL_CODE_ERROR_MESSAGE = "Postal Code is required"


    @classmethod
    @safe_run
    def setUpClass(cls):
        BaseTest().setUpClass()
        cls.login_page = LoginPage(cls.driver, cls.PLATFORM)
        cls.dashboard_page = DashboardPage(cls.driver, cls.PLATFORM)
        cls.cart_details_page = CartDetailsPage(cls.driver, cls.PLATFORM)
        cls.checkout_page = CheckoutPage(cls.driver, cls.PLATFORM)
        cls.checkout_overview_page = CheckoutOverviewPage(cls.driver, cls.PLATFORM)
        cls.checkout_complete_page = CheckoutCompletePage(cls.driver, cls.PLATFORM)
        cls.login_page.wait_for_page_loaded()
        cls.login_page.select_user_type("standard")
        cls.login_page.click_login_button()
        cls.dashboard_page.wait_for_page_loaded()
        cls.dashboard_page.add_product_to_cart(0)
        cls.dashboard_page.click_cart_button()
        cls.cart_details_page.wait_for_page_loaded()
        cls.cart_details_page.click_checkout_button()
        cls.checkout_page.wait_for_page_loaded()


    def setUp(self):
        BaseTest().setUp()

    @allure.title("test 01 - Try to checkout without providing any data")
    def test_01_checkout_without_data(self):
        self.checkout_page.click_continue_button()
        self.checkout_page.validate_error_message(self.FIRST_NAME_ERROR_MESSAGE)

    @allure.title("test 02 - Try to checkout only with first name")
    def test_02_checkout_only_with_first_name(self):
        self.checkout_page.fill_in_checkout_info_and_continue(
            last_name_value="",
            postal_code_value=""
        )
        self.checkout_page.validate_error_message(self.LAST_NAME_ERROR_MESSAGE)

    @allure.title("test 03 - Try to checkout with first and last name")
    def test_03_checkout_with_first_and_last_name(self):
        self.checkout_page.fill_in_checkout_info_and_continue(postal_code_value="")
        self.checkout_page.validate_error_message(self.POSTAL_CODE_ERROR_MESSAGE)

    @allure.title("test 04 - Try to checkout with fist name and postal code")
    def test_04_checkout_with_first_name_and_postal_code(self):
        self.checkout_page.fill_in_checkout_info_and_continue(last_name_value="")
        self.checkout_page.validate_error_message(self.LAST_NAME_ERROR_MESSAGE)

    @allure.title("test 05 - Try to checkout only with last name")
    def test_05_checkout_only_with_last_name(self):
        self.checkout_page.fill_in_checkout_info_and_continue(
            first_name_value="",
            postal_code_value=""
        )
        self.checkout_page.validate_error_message(self.FIRST_NAME_ERROR_MESSAGE)

    @allure.title("test 06 - Try to checkout with last name and postal code")
    def test_06_checkout_with_last_name_and_postal_code(self):
        self.checkout_page.fill_in_checkout_info_and_continue(first_name_value="")
        self.checkout_page.validate_error_message(self.FIRST_NAME_ERROR_MESSAGE)

    @allure.title("test 07 - Try to checkout only with postal code")
    def test_07_checkout_only_with_postal_codee(self):
        self.checkout_page.fill_in_checkout_info_and_continue(
            first_name_value="",
            last_name_value=""
        )
        self.checkout_page.validate_error_message(self.FIRST_NAME_ERROR_MESSAGE)





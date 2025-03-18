import allure
from helper_methods.value_formatting import format_price_value_to_float, \
    format_value_to_two_decimal_places, round_value_to_two_decimal_places
from page_objects.cart_details_page import CartDetailsPage
from page_objects.checkout_complete_page import CheckoutCompletePage
from page_objects.checkout_overview_page import CheckoutOverviewPage
from page_objects.checkout_page import CheckoutPage
from page_objects.dashboard_page import DashboardPage
from page_objects.login_page import LoginPage
from page_objects.nav_bar import NavBar
from tests.baseTest import BaseTest, safe_run


class MakingOrderFromDashboardTests(BaseTest):

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
        cls.nav_bar = NavBar(cls.driver, cls.PLATFORM)

    def setUp(self):
        BaseTest().setUp()

    @allure.title("test 01 - Making order - adding product from dashboard to cart - happy path")
    def test_01_adding_product_from_dashboard_to_cart_and_making_order_happy_path(self):
        products_amount = 1
        product_quantity = "1"
        percentage = 0.08
        self.login_page.wait_for_page_loaded()
        self.login_page.select_user_type("standard")
        self.login_page.click_login_button()
        self.dashboard_page.wait_for_page_loaded()
        product_name= self.dashboard_page.get_product_name(0)
        product_price = self.dashboard_page.get_product_price(0)
        tax_value = round_value_to_two_decimal_places(format_price_value_to_float(
            product_price) * percentage
                                                      )
        tax_value_proper_format = str(format_value_to_two_decimal_places(tax_value))
        total_price = str(round_value_to_two_decimal_places(
            format_price_value_to_float(product_price) + float(tax_value))
        )
        self.dashboard_page.add_product_to_cart(0)
        self.nav_bar.check_cart_button_label(f"{products_amount}")
        self.dashboard_page.check_if_remove_button_visible_on_product_item(0)
        self.nav_bar.click_cart_button()
        self.cart_details_page.wait_for_page_loaded()
        self.cart_details_page.assert_amount_of_products_in_cart(products_amount)
        self.cart_details_page.assert_cart_details_page(
            0,
            product_name,
            product_price,
            product_quantity
        )
        self.cart_details_page.click_checkout_button()
        self.checkout_page.wait_for_page_loaded()
        self.checkout_page.fill_in_checkout_info_and_continue()
        self.checkout_overview_page.wait_for_page_loaded()
        self.checkout_overview_page.assert_checkout_overview_page(
            products_amount,
            0,
            product_name,
            product_price,
            product_quantity,
            tax_value_proper_format,
            total_price
        )
        self.checkout_overview_page.click_finish_button()
        self.checkout_complete_page.wait_for_page_loaded()






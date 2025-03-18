import allure
from page_objects.cart_details_page import CartDetailsPage
from page_objects.checkout_complete_page import CheckoutCompletePage
from page_objects.checkout_overview_page import CheckoutOverviewPage
from page_objects.checkout_page import CheckoutPage
from page_objects.dashboard_page import DashboardPage
from page_objects.login_page import LoginPage
from page_objects.sorting_item_modal import SortingItemModal
from tests.baseTest import BaseTest, safe_run


class SortingOnDashboardTests(BaseTest):

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
        cls.sorting_item_modal = SortingItemModal(cls.driver, cls.PLATFORM)
        cls.login_page.wait_for_page_loaded()
        cls.login_page.select_user_type("standard")
        cls.login_page.click_login_button()
        cls.dashboard_page.wait_for_page_loaded()
        cls.dashboard_page.switch_view()

    def setUp(self):
        BaseTest().setUp()

    @allure.title("test 01 - Check ascending sorting based on products names on dashboard page")
    def test_01_check_asc_name_sorting_on_dashboard_page(self):
        self.dashboard_page.click_sorting_button()
        self.sorting_item_modal.check_sorting_modal_visibility()
        self.sorting_item_modal.select_sorting_rule("name_ascending")
        product_names = self.dashboard_page.get_all_names()
        self.dashboard_page.assert_sorting_order('asc', product_names)

    @allure.title("test 02 - Check descending sorting based on products names on dashboard page")
    def test_02_check_desc_name_sorting_on_dashboard_page(self):
        self.dashboard_page.click_sorting_button()
        self.sorting_item_modal.check_sorting_modal_visibility()
        self.sorting_item_modal.select_sorting_rule("name_descending")
        product_names = self.dashboard_page.get_all_names()
        self.dashboard_page.assert_sorting_order('desc', product_names)


    @allure.title("test 03 - Check ascending sorting based on products price on dashboard page")
    def test_03_check_asc_price_sorting_on_dashboard_page(self):
        self.dashboard_page.click_sorting_button()
        self.sorting_item_modal.check_sorting_modal_visibility()
        self.sorting_item_modal.select_sorting_rule("price_ascending")
        product_prices = self.dashboard_page.get_all_prices()
        self.dashboard_page.assert_sorting_order('asc', product_prices)


    @allure.title("test 04 - Check descending sorting based on products price on dashboard page")
    def test_04_check_desc_price_sorting_on_dashboard_page(self):
        self.dashboard_page.click_sorting_button()
        self.sorting_item_modal.check_sorting_modal_visibility()
        self.sorting_item_modal.select_sorting_rule("price_descending")
        product_prices = self.dashboard_page.get_all_prices()
        self.dashboard_page.assert_sorting_order('desc', product_prices)






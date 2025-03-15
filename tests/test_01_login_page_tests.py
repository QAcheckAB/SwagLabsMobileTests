# -*- coding: utf-8 -*-
import allure

from page_objects.dashboard_page import DashboardPage
from page_objects.login_page import LoginPage
from tests.baseTest import BaseTest, safe_run


class LoginPageTests(BaseTest):

    @classmethod
    @safe_run
    def setUpClass(cls):
        BaseTest().setUpClass()
        cls.login_page = LoginPage(cls.driver, cls.PLATFORM)
        cls.dashboard_page = DashboardPage(cls.driver, cls.PLATFORM)

    def setUp(self):
        BaseTest().setUp()
        self.login_page.wait_for_page_loaded()

    @allure.title("test 01 - Making order - adding product from dashboard to cart - happy path")
    def test_01_login_in(self):
        products_amount = 1
        self.login_page.wait_for_page_loaded()
        self.login_page.select_user_type("standard")
        self.login_page.click_login_button()
        self.dashboard_page.wait_for_page_loaded()
        product_name= self.dashboard_page.get_first_product_name()
        product_price = self.dashboard_page.get_first_product_price()
        self.dashboard_page.add_first_product_to_cart()
        self.dashboard_page.check_cart_button_label(f"{products_amount}")
        self.dashboard_page.check_if_remove_button_visible_on_first_product_item()
        self.dashboard_page.click_cart_button()


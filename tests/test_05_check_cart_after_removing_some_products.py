# -*- coding: utf-8 -*-
import random
from typing import re

import allure

from helper_methods.value_formatting import format_price_value_to_float, \
    format_value_to_two_decimal_places, round_value_to_two_decimal_places
from page_objects.cart_details_page import CartDetailsPage
from page_objects.checkout_complete_page import CheckoutCompletePage
from page_objects.checkout_overview_page import CheckoutOverviewPage
from page_objects.checkout_page import CheckoutPage
from page_objects.dashboard_page import DashboardPage
from page_objects.login_page import LoginPage
from tests.baseTest import BaseTest, safe_run


class CheckCartAfterChangesTests(BaseTest):

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

    def setUp(self):
        BaseTest().setUp()

    @allure.title("test 01 - Making order - adding product from dashboard to cart - happy path")
    def test_01_check_cart_after_removing_some_products(self):
        products_amount = 3
        product_quantity = str(1)
        self.login_page.wait_for_page_loaded()
        self.login_page.select_user_type("standard")
        self.login_page.click_login_button()
        self.dashboard_page.wait_for_page_loaded()
        self.dashboard_page.switch_view()
        first_product_name= self.dashboard_page.get_product_name(0)
        first_product_price = self.dashboard_page.get_product_price(0)
        second_product_name= self.dashboard_page.get_product_name(1)
        second_product_price = self.dashboard_page.get_product_price(1)
        third_product_name= self.dashboard_page.get_product_name(2)
        third_product_price = self.dashboard_page.get_product_price(2)
        self.dashboard_page.add_product_to_cart(0)
        self.dashboard_page.add_product_to_cart(1)
        self.dashboard_page.add_product_to_cart(2)
        self.dashboard_page.check_cart_button_label(f"{products_amount}")
        self.dashboard_page.remove_product(2)
        self.dashboard_page.check_if_add_cart_button_visible_on_product_item(2)
        self.dashboard_page.check_if_remove_button_visible_on_product_item(0)
        self.dashboard_page.check_if_remove_button_visible_on_product_item(1)
        self.dashboard_page.check_cart_button_label(f"{2}")
        self.dashboard_page.click_cart_button()
        self.cart_details_page.wait_for_page_loaded()
        self.cart_details_page.assert_amount_of_items_in_cart(2)
        self.cart_details_page.assert_product_name(0, first_product_name)
        self.cart_details_page.assert_product_quantity(0, "1")
        self.cart_details_page.assert_product_name(1, second_product_name)
        self.cart_details_page.assert_product_quantity(1, "1")
        self.cart_details_page.remove_product_from_cart(0)
        self.dashboard_page.check_cart_button_label("1")
        self.cart_details_page.assert_amount_of_items_in_cart(1)
        self.cart_details_page.assert_cart_details_page( 0, second_product_name, second_product_price, "1")






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

    def setUp(self):
        BaseTest().setUp()
        # self.login_page.wait_for_page_loaded()

    @allure.title("test 01 - Making order - adding product from dashboard to cart - happy path")
    def test_01_adding_product_from_dashboard_to_cart_and_making_order_happy_path(self):
        products_amount = 1
        product_quantity = str(1)
        percentage = 0.08
        self.login_page.wait_for_page_loaded()
        self.login_page.select_user_type("standard")
        self.login_page.click_login_button()
        self.dashboard_page.wait_for_page_loaded()
        product_name= self.dashboard_page.get_product_name(0)
        product_price = self.dashboard_page.get_product_price(0)
        tax_value = round_value_to_two_decimal_places(format_price_value_to_float(product_price) * percentage)
        tax_value_proper_format = str(format_value_to_two_decimal_places(tax_value))
        total_price = str(round_value_to_two_decimal_places(format_price_value_to_float(product_price) + float(tax_value)))
        self.dashboard_page.add_product_to_cart(0)
        self.dashboard_page.check_cart_button_label(f"{products_amount}")
        self.dashboard_page.check_if_remove_button_visible_on_product_item(0)
        self.dashboard_page.click_cart_button()
        self.cart_details_page.wait_for_page_loaded()
        self.cart_details_page.assert_amount_of_items_in_cart(products_amount)
        self.cart_details_page.assert_cart_details_page(0, product_name, product_price, "1")
        # self.cart_details_page.assert_amount_of_items_in_cart(products_amount)
        # self.cart_details_page.assert_product_name(0, product_name)
        # self.cart_details_page.assert_product_price(0, product_price)
        # self.cart_details_page.check_if_remove_button_visible_on_product_item(0)
        self.cart_details_page.click_checkout_button()
        self.checkout_page.wait_for_page_loaded()
        self.checkout_page.fill_in_checkout_info_and_continue()
        # self.checkout_page.insert_first_name()
        # self.checkout_page.insert_last_name()
        # self.checkout_page.insert_postal_code()
        # self.checkout_page.click_continue_button()
        self.checkout_overview_page.wait_for_page_loaded()
        self.checkout_overview_page.assert_checkout_overview_page(products_amount, 0, product_name, product_price, product_quantity, tax_value_proper_format, total_price)
        # self.checkout_overview_page.assert_amount_of_items_on_overview(products_amount)
        # self.checkout_overview_page.assert_product_name(0, product_name)
        # self.checkout_overview_page.assert_product_price(0, product_price)
        # self.checkout_overview_page.assert_item_total_value(product_price)
        # self.checkout_overview_page.assert_tax_value(tax_value_proper_format)
        # self.checkout_overview_page.assert_total_value(total_price)
        self.checkout_overview_page.click_finish_button()
        self.checkout_complete_page.wait_for_page_loaded()






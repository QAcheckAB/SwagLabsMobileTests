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

    def setUp(self):
        BaseTest().setUp()

    @allure.title("test 01 - Check sorting based on products names on dashboard page")
    def test_01_check_name_sorting_on_dashboard_page(self):
        self.login_page.wait_for_page_loaded()
        self.login_page.select_user_type("standard")
        self.login_page.click_login_button()
        self.dashboard_page.wait_for_page_loaded()
        self.dashboard_page.switch_view()
        self.dashboard_page.get_all_names()
        self.dashboard_page.get_all_prices()







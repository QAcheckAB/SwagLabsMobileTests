# -*- coding: utf-8 -*-
import random
from typing import re

import allure

from helper_methods.value_formatting import format_price_value_to_float, round_value_to_two_decimal_places, format_value_to_two_decimal_places
from page_objects.cart_details_page import CartDetailsPage
from page_objects.checkout_complete_page import CheckoutCompletePage
from page_objects.checkout_overview_page import CheckoutOverviewPage
from page_objects.checkout_page import CheckoutPage
from page_objects.dashboard_page import DashboardPage
from page_objects.login_page import LoginPage
from tests.baseTest import BaseTest, safe_run


class ValidateErrorsOnLoginPageTests(BaseTest):
    USERNAME_ERROR_MESSAGE = "Username is required"
    PASSWORD_ERROR_MESSAGE = "Password is required"

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
        self.login_page.wait_for_page_loaded()

    @allure.title("test 01 - Try to login without providing any credentials")
    def test_01_login_without_credentials(self):
        self.login_page.click_login_button()
        self.login_page.validate_error_message(self.USERNAME_ERROR_MESSAGE)

    @allure.title("test 02 - Try to login without username")
    def test_02_login_without_username(self):
        self.login_page.insert_username("")
        self.login_page.insert_password("standard")
        self.login_page.click_login_button()
        self.login_page.validate_error_message(self.USERNAME_ERROR_MESSAGE)

    @allure.title("test 03 - Try to login without password")
    def test_03_login_without_password(self):
        self.login_page.insert_username("standard")
        self.login_page.insert_password("")
        self.login_page.click_login_button()
        self.login_page.validate_error_message(self.PASSWORD_ERROR_MESSAGE)






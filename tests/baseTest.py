# -*- coding: utf-8 -*-
import logging
import logging.config
import os
import unittest

import coloredlogs
from appium import webdriver

from utils.create_driver import create_driver
from utils.file_manager import load_config_from_json


def safe_run(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Tet scenario failed on setUpClass {e}")
            self = args[0]()
            self.set_up_failed = True
            self.tearDown()
            self.tearDownClass()
            raise e

    return func_wrapper


class BaseTest(unittest.TestCase):
    coloredlogs.install()
    ROOT_PATH: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    CONFIG: dict = load_config_from_json(os.getenv("CONFIG_FILE", "android_config.json"))
    APP_DIRECTORY: str = os.getenv("APP_DIRECTORY", os.path.join(ROOT_PATH, "test_apps"))
    PLATFORM: str = os.getenv("PLATFORM", CONFIG["platformName"].lower())
    driver: webdriver = None
    ANDROID = "android"
    IOS = "ios"
    set_up_failed = False
    recording = False

    @classmethod
    def setUpClass(cls):
        cls.driver = create_driver(cls.CONFIG, cls.APP_DIRECTORY)

    def setUp(self):
        self.test_name = self.__dict__["_testMethodName"]
        logging.info(f"RUNNING TEST: {self.test_name}")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()

    def is_failed(self):
        if self.set_up_failed:
            return self.set_up_failed
        elif self._outcome.errors:
            return True
        else:
            return False

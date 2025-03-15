# -*- coding: utf-8 -*-

import os
from appium import webdriver
import logging as log
import allure
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


@allure.step("create appium driver")
def create_driver(
        config_file: dict, app_dir: str) -> webdriver:
    """Create appium driver with specified desired capabilities
        :param config_file: dictionary with test configuration
        :param app_dir: path to directory with test applications
        :return: appium driver

    """
    desired_caps = {
        'appiumVersion': config_file['appiumVersion'],
        'deviceOrientation': config_file['deviceOrientation'],
        'app': os.path.join(app_dir, config_file['app']),
        'deviceName': config_file['deviceName'],
        'platformName': config_file['platformName'],
        'platformVersion': config_file['platformVersion'],
        'newCommandTimeout': 600
    }
    platform = config_file['platformName'].lower()
    if platform == 'ios':
        desired_caps['xcodeOrgId'] = config_file['xcodeOrgId']
        desired_caps['automationName'] = config_file['automationName']
        desired_caps['testFramework'] = config_file['automationName'].lower()
        desired_caps["noReset"] = False
        desired_caps["fullReset"] = True
        if config_file.get('udid'):
            desired_caps['updatedWDABundleId'] = config_file['updatedWDABundleId']
            desired_caps['udid'] = config_file['udid']
            desired_caps['xcodeSigningId'] = config_file['xcodeSigningId']
        automatorOptions = XCUITestOptions()
        automatorOptions.load_capabilities(desired_caps)
    elif platform == 'android':
        desired_caps['adbExecTimeout'] = 50000
        desired_caps['appPackage'] = config_file['appPackage']
        desired_caps['appWaitActivity'] = "com.swaglabsmobileapp.MainActivity" # TODO Zmiana do konfiga
        desired_caps['unicodeKeyboard'] = config_file['unicodeKeyboard']
        desired_caps['resetKeyboard'] = config_file['resetKeyboard']
        desired_caps['automationName'] = 'UiAutomator2'
        if config_file['platformVersion'] == '6.0':
            desired_caps['browserName'] = config_file['browserName']
        automatorOptions = UiAutomator2Options()
        automatorOptions.load_capabilities(desired_caps
        )
    environment = config_file["remote"]
    log.info(f'Starting appium driver with caps: \n{desired_caps}')

    return webdriver.Remote(command_executor= environment, options= automatorOptions)
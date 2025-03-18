import logging as log
import os

import allure
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def get_common_capabilities(config_file: dict, app_dir: str) -> dict:
    """
    Get common desired capabilities for both iOS and Android platforms.

    :param config_file: Dictionary with test configuration.
    :param app_dir: Path to directory with test applications.
    :return: Dictionary with common desired capabilities.
    """
    return {
        "appiumVersion": config_file["appiumVersion"],
        "deviceOrientation": config_file["deviceOrientation"],
        "app": os.path.join(app_dir, config_file["app"]),
        "deviceName": config_file["deviceName"],
        "platformName": config_file["platformName"],
        "platformVersion": config_file["platformVersion"],
        "newCommandTimeout": 600,
    }


def get_ios_capabilities(config_file: dict) -> dict:
    """
    Get iOS-specific desired capabilities.

    :param config_file: Dictionary with test configuration.
    :return: Dictionary with iOS-specific desired capabilities.
    """
    ios_caps = {
        "xcodeOrgId": config_file["xcodeOrgId"],
        "automationName": config_file["automationName"],
        "testFramework": config_file["automationName"].lower(),
        "noReset": False,
        "fullReset": True,
    }
    if config_file.get("udid"):
        ios_caps.update(
            {
                "updatedWDABundleId": config_file["updatedWDABundleId"],
                "udid": config_file["udid"],
                "xcodeSigningId": config_file["xcodeSigningId"],
            }
        )
    return ios_caps


def get_android_capabilities(config_file: dict) -> dict:
    """
    Get Android-specific desired capabilities.

    :param config_file: Dictionary with test configuration.
    :return: Dictionary with Android-specific desired capabilities.
    """
    android_caps = {
        "adbExecTimeout": 50000,
        "appPackage": config_file["appPackage"],
        "appWaitActivity": config_file["appWaitActivity"],
        "unicodeKeyboard": config_file["unicodeKeyboard"],
        "resetKeyboard": config_file["resetKeyboard"],
        "automationName": "UiAutomator2",
    }
    if config_file["platformVersion"] == "6.0":
        android_caps["browserName"] = config_file["browserName"]
    return android_caps


@allure.step("Create appium driver")
def create_driver(config_file: dict, app_dir: str) -> webdriver:
    """
    Create Appium driver with specified desired capabilities.

    :param config_file: Dictionary with test configuration.
    :param app_dir: Path to directory with test applications.
    :return: Appium driver.
    """
    desired_caps = get_common_capabilities(config_file, app_dir)
    platform = config_file["platformName"].lower()

    if platform == "ios":
        desired_caps.update(get_ios_capabilities(config_file))
        automator_options = XCUITestOptions()
    elif platform == "android":
        desired_caps.update(get_android_capabilities(config_file))
        automator_options = UiAutomator2Options()

    automator_options.load_capabilities(desired_caps)
    environment = config_file["remote"]
    log.info(f"Starting appium driver with caps: \n{desired_caps}")

    return webdriver.Remote(command_executor=environment, options=automator_options)

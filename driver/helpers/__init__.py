from sys import modules
from inspect import getmembers, isfunction

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Opera, Safari
from msedge.selenium_tools import Edge, EdgeOptions
from .web_driver_factory import WebDriverFactory


def _register_web_driver_chrome(factory):
    options = ChromeOptions
    driver = Chrome
    driver_type = 'GOOGLE CHROME'
    driver_type_alias = 'CHROME'

    factory.register_web_driver(driver_type, driver, options)
    factory.register_web_driver(driver_type_alias, driver, options)


def _register_web_driver_edge(factory):
    options = EdgeOptions
    driver = Edge
    driver_type = 'EDGE'
    driver_type_alias = 'EDGE CHROMIUM'

    factory.register_web_driver(driver_type, driver, options)
    factory.register_web_driver(driver_type_alias, driver, options)


def _register_web_driver_firefox(factory):
    options = FirefoxOptions
    driver = Firefox
    driver_type = 'FIREFOX'

    factory.register_web_driver(driver_type, driver, options)


def _register_web_driver_opera(factory):
    driver = Opera
    driver_type = 'OPERA'

    factory.register_web_driver(driver_type, driver, None)


def _register_web_driver_safari(factory):
    driver = Safari
    driver_type = 'SAFARI'

    factory.register_web_driver(driver_type, driver, None)


def get_web_driver_registries():
    """
    Dynamically gets all functions that start with _register_web_driver and append into the list
    """
    return [module[1] for module in getmembers(modules[__name__], isfunction) if
            module[0].startswith('_register_web_driver')]

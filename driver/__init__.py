from driver.helpers.web_driver_factory import WebDriverFactory
from driver.helpers import get_web_driver_registries


def initialize_web_driver_repository():
    repository = WebDriverFactory()

    for register_web_driver in get_web_driver_registries():
        register_web_driver(repository)

    return repository

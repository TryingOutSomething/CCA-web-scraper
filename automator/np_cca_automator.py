from automator import Automator
from util.file_util import get_user_defined_driver_info, setup_download_directory
from driver import initialize_web_driver_repository


def _validate_and_get_driver_information():
    driver_info = get_user_defined_driver_info()
    setup_download_directory(driver_info)

    return driver_info


class NpCcaAutomator(Automator):
    def __init__(self):
        self.driver = None
        self.cca_category_list = []
        self.driver_info = _validate_and_get_driver_information()
        self.available_web_drivers = initialize_web_driver_repository()

    def start_job(self, url, browser_options=None):
        print("Starting automation...")

        driver_path = self.driver_info['path']
        driver_type = self.driver_info['type']

        self.driver = self.available_web_drivers.get_web_driver(driver_type, driver_path, browser_options)
        self.driver.get(url)
        self._get_all_cca_categories()

    def _get_all_cca_categories(self):
        cca_menu_ul_element = self.driver.find_element_by_class_name('extend-menu')
        cca_li_elements = cca_menu_ul_element.find_elements_by_tag_name('li')

        for cca in cca_li_elements:
            cca_anchor_element = cca.find_element_by_tag_name('a')
            cca_name = cca_anchor_element.get_attribute('innerText')
            self.cca_category_list.append(cca_name)

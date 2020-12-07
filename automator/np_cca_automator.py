from automator import Automator
from util.file_util import get_user_defined_driver_info, setup_download_directory
from driver import initialize_web_driver_repository

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

_CLASS_NAMES = ['artandculture-container']


def _validate_and_get_driver_information():
    driver_info = get_user_defined_driver_info()
    setup_download_directory(driver_info)

    return driver_info


class NpCcaAutomator(Automator):
    def __init__(self):
        self.driver = None
        self.cca_list = []
        self.driver_info = _validate_and_get_driver_information()
        self.available_web_drivers = initialize_web_driver_repository()

    def start_job(self, url, browser_options=None):
        print("Starting automation...")

        driver_path = self.driver_info['path']
        driver_type = self.driver_info['type']

        self.driver = self.available_web_drivers.get_web_driver(driver_type, driver_path, browser_options)
        self.driver.get(url)
        self._get_cca_info_list_by_class_name(_CLASS_NAMES[0])

    def _get_cca_info_list_by_class_name(self, class_name):
        main_div_element = self.driver.find_element_by_class_name(class_name)
        child_div_elements = main_div_element.find_elements_by_class_name('col-xs-12')

        cca_category_h3_element = child_div_elements[0].find_element_by_tag_name('h3')
        cca_category = cca_category_h3_element.get_attribute('innerText')

        self._get_all_cca_under_category(cca_category, child_div_elements[1])

    def _get_all_cca_under_category(self, cca_category, cca_info_elements):
        cca_ul_elements = cca_info_elements.find_elements_by_class_name('ac-group')

        # for cca_column_element in cca_ul_elements:
        #     cca_row_element = cca_column_element.find_elements_by_css_selector('.ac-item')
        #     print(cca_row_element.get_attribute('class'))

        # loop done here
        # Get cca list from ul
        cca_row_elements = cca_ul_elements[0].find_elements_by_class_name('ac-item')

        # get p tag item from li list
        cca_value_element = cca_row_elements[0].find_element_by_class_name('open-modal')
        cca_value_element.click()

        modal_element = WebDriverWait(self.driver, 10) \
            .until(
            lambda on_modal_open: on_modal_open.find_element_by_css_selector('#modal-content > #md-main-content')
        )

        self._get_cca_info_from_modal(modal_element, cca_category)
        # close modal

    def _get_cca_info_from_modal(self, modal_element, cca_category):
        cca_title_element = modal_element.find_element_by_class_name('club-title')
        cca_title = cca_title_element.get_attribute('innerText')

        cca_content_elements = modal_element.find_elements_by_class_name('club-content')

        self._get_cca_image_info(modal_element)

        cca_bio = cca_content_elements[0].get_attribute('innerText')
        cca_contact = cca_content_elements[1].get_attribute('innerText')

        cca_info = {
            'name': cca_title,
            'category': cca_category,
            'bio': cca_bio,
            'contact': cca_contact.split(': ')[1]
        }

        print(cca_info)
        # self.cca_list.append(cca_info)

    def _get_cca_image_info(self, modal_element):
        try:
            cca_image = modal_element.find_element_by_class_name('img-responsive')
            print(cca_image.get_attribute('src'))
        except NoSuchElementException as e:
            print(e)

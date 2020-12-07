from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

from automator import Automator
from driver import initialize_web_driver_repository
from util.file_util import get_user_defined_driver_info, setup_download_directory

_CLASS_NAMES = ['ac', 'sp', 'cs', 'si']


def _validate_and_get_driver_information():
    driver_info = get_user_defined_driver_info()
    setup_download_directory(driver_info)

    return driver_info


class NpCcaAutomator(Automator):
    def __init__(self):
        self.driver = None
        self.cca_list = []
        self.current_cca_category = ''
        self.driver_info = _validate_and_get_driver_information()
        self.available_web_drivers = initialize_web_driver_repository()

    def start_job(self, url, browser_options=None):
        print("Starting automation...")

        driver_path = self.driver_info['path']
        driver_type = self.driver_info['type']

        self.driver = self.available_web_drivers.get_web_driver(driver_type, driver_path, browser_options)
        self.driver.get(url)

        # for name in _CLASS_NAMES:
        #     self._get_cca_info_list_by_id(name)
        self._get_cca_info_list_by_id(_CLASS_NAMES[0])

    def _get_cca_info_list_by_id(self, element_id):
        root_xpath = f'//*[@id="{element_id}"]/div'

        main_div_row = self.driver.find_element_by_id(element_id)
        div_elements = main_div_row.find_elements_by_xpath(root_xpath)

        for div in div_elements:
            current_div = div.get_attribute('class')

            if 'triangle' in current_div:
                continue

            child_div_xpath = f'{root_xpath}/div'
            child_div_elements = div.find_elements_by_xpath(child_div_xpath)

            cca_category_h3_element = child_div_elements[0].find_element_by_tag_name('h3')
            self.current_cca_category = cca_category_h3_element.get_attribute('innerText').strip()

            self._get_all_cca_under_category(child_div_xpath, child_div_elements[1])

    def _get_all_cca_under_category(self, parent_xpath, cca_info_elements):
        ul_xpath = f'{parent_xpath}/ul'
        cca_ul_elements = cca_info_elements.find_elements_by_xpath(ul_xpath)

        li_xpath = f'{ul_xpath}/li'

        for cca_column_element in cca_ul_elements:
            cca_li_elements = cca_column_element.find_elements_by_xpath(li_xpath)

            for cca_li_element in cca_li_elements:
                cca_value_element = cca_li_element.find_element_by_class_name('open-modal')
                print(cca_value_element.get_attribute('class'))
                print(cca_value_element.get_attribute('data-page'))
                cca_value_element.click()

                modal_element = WebDriverWait(self.driver, 10) \
                    .until(
                    lambda on_modal_open: on_modal_open.find_element_by_css_selector(
                        '#modal-content > #md-main-content'
                    )
                )

                self._get_cca_info_from_modal(modal_element)

                close_modal_element = self.driver.find_element_by_class_name('close-modal')
                close_modal_anchor_element = close_modal_element.find_element_by_tag_name('a')
                close_modal_anchor_element.click()

    def _get_cca_info_from_modal(self, modal_element):
        cca_title_element = modal_element.find_element_by_class_name('club-title')
        cca_title = cca_title_element.get_attribute('innerText')

        cca_content_elements = modal_element.find_elements_by_class_name('club-content')

        self._get_cca_image_info(modal_element)

        cca_bio = cca_content_elements[0].get_attribute('innerText')
        cca_contact = cca_content_elements[1].get_attribute('innerText')

        cca_info = {
            'name': cca_title,
            'category': self.current_cca_category,
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

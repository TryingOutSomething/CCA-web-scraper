from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
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
        self.driver_action = None
        self.cca_list = []
        self.current_cca_category = ''
        self.close_modal_util = None
        self.driver_info = _validate_and_get_driver_information()
        self.available_web_drivers = initialize_web_driver_repository()

    def start_job(self, url, browser_options=None):
        print("Starting automation...")

        driver_path = self.driver_info['path']
        driver_type = self.driver_info['type']

        self.driver = self.available_web_drivers.get_web_driver(driver_type, driver_path, browser_options)
        self.driver_action = ActionChains(self.driver)
        self.driver.maximize_window()
        self.driver.get(url)

        # for name in _CLASS_NAMES:
        #     self._get_cca_info_list_by_id(name)
        self._get_cca_info_list_by_id(_CLASS_NAMES[1])

    def _get_cca_info_list_by_id(self, element_id):
        root_xpath = f'//*[@id="{element_id}"]/div'

        div_elements = self.driver.find_elements_by_xpath(root_xpath)

        child_div_xpath = f'{root_xpath}/div'

        if len(div_elements) > 1:
            child_div_elements = div_elements[1].find_elements_by_xpath(child_div_xpath)
        else:
            child_div_elements = div_elements[0].find_elements_by_xpath(child_div_xpath)

        # for div in div_elements:
        #     current_div = div.get_attribute('class')
        #
        #     if 'triangle' in current_div:
        #         continue
        #
        #     child_div_elements = div.find_elements_by_xpath(child_div_xpath)

        cca_category_h3_element = child_div_elements[0].find_element_by_tag_name('h3')
        self.current_cca_category = cca_category_h3_element.get_attribute('innerText').strip()

        self._get_all_cca_under_category(child_div_xpath, child_div_elements[1])

    def _get_all_cca_under_category(self, x_path, cca_info_elements):
        ul_xpath = f'{x_path}/ul'
        cca_ul_elements = cca_info_elements.find_elements_by_xpath(ul_xpath)

        li_xpath = f'{ul_xpath}/li'

        for cca_column_element in cca_ul_elements:
            cca_li_elements = cca_column_element.find_elements_by_xpath(li_xpath)

            for cca_li_element in cca_li_elements:
                cca_value_element = cca_li_element.find_element_by_class_name('open-modal')
                self.driver.execute_script('arguments[0].click()', cca_value_element)

                modal_element = WebDriverWait(self.driver, 10) \
                    .until(lambda on_modal_open: on_modal_open.find_element_by_class_name('club-modal'))

                self._wait_till_loading_is_done()

                self._get_cca_info_from_modal(modal_element)
                self._close_modal(cca_li_element)

    def _get_cca_info_from_modal(self, modal_element):
        cca_title = self._get_cca_title(modal_element)

        cca_content_elements = modal_element.find_elements_by_tag_name('p')
        image_url = self._get_cca_image_info(modal_element)

        cca_bio = cca_content_elements[0].get_attribute('innerText')
        cca_contact = cca_content_elements[1].get_attribute('innerText')

        cca_info = {
            'name': cca_title,
            'category': self.current_cca_category,
            'bio': cca_bio,
            'email': cca_contact.split(': ')[1],
            'profileUrl': None,
            'coverUrl': None if not image_url else image_url
        }

        print(cca_info)
        # self.cca_list.append(cca_info)

    def _get_cca_title(self, modal_element):
        try:
            cca_title_element = modal_element.find_element_by_class_name('club-title')
            return cca_title_element.get_attribute('innerText')
        except NoSuchElementException as e:
            return ''

    def _get_cca_image_info(self, modal_element):
        try:
            cca_image = modal_element.find_element_by_class_name('img-responsive')
            return cca_image.get_attribute('src')
        except NoSuchElementException as e:
            return

    def _wait_till_loading_is_done(self):
        try:
            WebDriverWait(self.driver, 10).until(invisibility_of_element_located(
                self.driver.find_element_by_class_name('right-modal-content')
            ))
        except NoSuchElementException as e:
            return

    def _close_modal(self, cca_li_element):
        self.driver_action.move_to_element(cca_li_element)
        self.driver_action.perform()
        self.driver_action.click()
        self.driver_action.perform()

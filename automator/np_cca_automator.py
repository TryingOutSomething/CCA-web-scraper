from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from automator import Automator
from driver import initialize_web_driver_repository
from util.file_util import get_user_defined_driver_info, setup_download_directory, dump_records

_ID_NAMES = ['ac', 'sp', 'cs', 'si']


def _validate_and_get_driver_information():
    driver_info = get_user_defined_driver_info()
    setup_download_directory(driver_info)

    return driver_info


def _set_close_modal_element(driver, element_id):
    # Could be any element in the DOM. As long as it is always visible
    return driver.find_element_by_id(element_id)


def _get_cca_title(modal_element):
    try:
        cca_title_element = modal_element.find_element_by_class_name('club-title')
        return cca_title_element.get_attribute('innerText')
    except NoSuchElementException:
        return ''


def _get_cca_image_info(modal_element):
    try:
        cca_image = modal_element.find_element_by_class_name('img-responsive')
        return cca_image.get_attribute('src')
    except NoSuchElementException:
        return


def _get_email_from_cca_description(description):
    try:
        return description[1].split(': ')[1].rstrip('\n')
    except IndexError:
        return ''


class NpCcaAutomator(Automator):
    def __init__(self):
        self.driver = None
        self.driver_action = None
        self.cca_list = []
        self.current_cca_category = ''
        self.close_modal_element = None
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

        self.close_modal_element = _set_close_modal_element(self.driver, _ID_NAMES[0])

        # If you would like to scrape all at once
        for name in _ID_NAMES:
            self._scrape_cca_info(name)

        # Scrape one by one
        # self._get_cca_info_list_by_id(_ID_NAMES[0])

        print('Dumping records...')
        dump_records(self.cca_list, self.driver_info['download_directory'])

        self.driver.quit()

    def _scrape_cca_info(self, element_id):
        root_xpath = f'//div[@id="{element_id}"]/div'

        div_elements = self.driver.find_elements_by_xpath(root_xpath)

        child_div_xpath = './div'

        if len(div_elements) > 1:
            child_div_elements = div_elements[1].find_elements_by_xpath(child_div_xpath)
        else:
            child_div_elements = div_elements[0].find_elements_by_xpath(child_div_xpath)

        cca_category_h3_element = child_div_elements[0].find_element_by_tag_name('h3')
        self.current_cca_category = cca_category_h3_element.get_attribute('innerText').strip()

        for child_div in child_div_elements:
            self._get_all_cca_under_category(child_div)

    def _get_all_cca_under_category(self, cca_info_element):
        cca_ul_elements = cca_info_element.find_elements_by_xpath('./ul')

        for cca_column_element in cca_ul_elements:
            cca_li_elements = cca_column_element.find_elements_by_xpath('./li')

            for cca_li_element in cca_li_elements:
                cca_value_element = cca_li_element.find_element_by_class_name('open-modal')
                self.driver.execute_script('arguments[0].click()', cca_value_element)

                modal_element = WebDriverWait(self.driver, 10) \
                    .until(lambda on_modal_open: on_modal_open.find_element_by_class_name('club-modal'))

                self._get_cca_info_from_modal(modal_element)
                self._close_modal()

    def _get_cca_info_from_modal(self, modal_element):
        cca_title = _get_cca_title(modal_element)

        probable_html_tags_xpath = './p | ./h4'
        cca_content_elements = modal_element.find_elements_by_xpath(probable_html_tags_xpath)
        image_url = _get_cca_image_info(modal_element)

        raw_cca_content_list = [element.get_attribute('innerText') for element in cca_content_elements if
                                element.get_attribute('innerText') != '' and
                                '\xa0' not in element.get_attribute('innerText')]

        cca_info = {
            'name': cca_title.rstrip('\n'),
            'category': self.current_cca_category,
            'bio': raw_cca_content_list[0].rstrip('\n'),
            'email': _get_email_from_cca_description(raw_cca_content_list),
            'profileUrl': None,
            'coverUrl': None if not image_url else image_url
        }

        print(cca_info)
        self.cca_list.append(cca_info)

    def _close_modal(self):
        # The close button is not clickable with selenium as the click listener is using jQuery
        # The other method to close the modal is to click outside the modal region
        self.driver_action.move_to_element(self.close_modal_element)
        self.driver_action.perform()
        self.driver_action.click().perform()

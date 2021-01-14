from unicodedata import normalize

from automator import Automator

from driver import initialize_web_driver_repository
from util.file_util import get_user_defined_driver_info, setup_download_directory, dump_records


def _validate_and_get_driver_information():
    driver_info = get_user_defined_driver_info()
    setup_download_directory(driver_info, 'tp')

    return driver_info


def _is_cca_title(div_element):
    div_class = div_element.get_attribute('class')

    return 'text' in div_class


def _get_cca_description_and_email(cca_content_columns):
    common_x_path = './div/div/div/div'

    descriptions_container = cca_content_columns.find_element_by_xpath(common_x_path)

    cca_description = descriptions_container.find_element_by_xpath('p[1]').get_attribute('innerText')
    email = descriptions_container.find_element_by_css_selector('p > a').get_attribute('href')

    return cca_description, email


def _strip_mailto_links_from_email(email):
    return email.split(':')[1].rstrip('\n')


def _get_cca_category(cca_info_div):
    cca_category_css_selector_signature = 'div > div.tp--container > h3, h6'

    return cca_info_div.find_element_by_css_selector(
        cca_category_css_selector_signature).get_attribute('innerText')


class TpCcaAutomator(Automator):
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

        self.driver = self.available_web_drivers.get_web_driver(
            driver_type, driver_path, browser_options)
        self.driver.maximize_window()
        self.driver.get(url)

        main_element = self.driver.find_element_by_class_name('responsivegrid')

        self._scrape_cca_info(main_element)

        print('Dumping records...')
        dump_records(self.cca_list, self.driver_info['download_directory'])

        self.driver.quit()

    def _scrape_cca_info(self, main_element):
        child_element_x_path = './div/div'

        list_of_div_elements = main_element.find_elements_by_xpath(child_element_x_path)
        list_of_cca_info_elements = list_of_div_elements[4:]  # Get cca info only. Filter the rest

        for cca_info_div in list_of_cca_info_elements:
            if _is_cca_title(cca_info_div):  # if even, get cca category
                self.current_cca_category = _get_cca_category(cca_info_div)
            else:  # Else get content
                self._get_all_cca_under_category(cca_info_div)

    def _get_all_cca_under_category(self, cca_info_div):
        list_of_cca_elements = cca_info_div.find_elements_by_xpath('./div/div')

        for cca_element in list_of_cca_elements:
            cca_title = cca_element.find_element_by_xpath(f'./h3/button/span').get_attribute('innerText')

            cca_content_columns = cca_element.find_elements_by_xpath('./div/div/div/div/div')
            image_url = cca_content_columns[0].find_element_by_xpath('./div/div[2]/div/img').get_attribute('src')

            cca_description, email = _get_cca_description_and_email(cca_content_columns[1])

            cca_info = {
                'name': normalize('NFKD', cca_title),
                'category': normalize('NFKD', self.current_cca_category).strip(),
                'bio': normalize('NFKD', cca_description).rstrip('\n'),
                'email': _strip_mailto_links_from_email(email),
                'contact': None,
                'profileUrl': None,
                'coverUrl': None if not image_url else image_url
            }
            #
            print(cca_info)
            self.cca_list.append(cca_info)

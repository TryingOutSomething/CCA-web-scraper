from os import listdir
from os.path import dirname
from importlib import import_module

from util.file_util import get_school_cca_url


class Automator:
    def start_job(self, url, browser_options):
        raise NotImplemented

    def _login(self):
        raise NotImplemented

    def _get_all_assets_info(self):
        raise NotImplemented

    def _download(self, urls):
        raise NotImplemented


def get_automator_by_school_code(school_code):
    for module in listdir(dirname(__file__)):
        if _is_invalid_python_module(module) or school_code not in module:
            continue

        return _create_new_class_instance(module[:-3], school_code), get_school_cca_url(school_code)

    return None


def _is_invalid_python_module(module):
    return module == '__init__.py' or module[-3:] != '.py'


def _create_new_class_instance(module_name, school_code):
    importing_module = import_module(f'automator.{module_name}')
    selected_class = getattr(importing_module, _get_class_name(school_code))
    instance = selected_class()

    return instance


def _get_class_name(school_code):
    return f'{school_code[0].upper()}{school_code[1:]}CcaAutomator'


def get_valid_school_codes():
    valid_school_code_list = [f'{i + 1}. {module.split("_")[0]}'
                              for i, module in enumerate(listdir(dirname(__file__)))
                              if not _is_invalid_python_module(module)]

    return '\n'.join(valid_school_code_list)

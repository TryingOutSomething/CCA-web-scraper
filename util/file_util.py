from json import dump
from os import getcwd, makedirs, path
from os.path import isfile
from pathlib import Path
from platform import system

from yaml import safe_load

_default_directory_permission_mode = 777
_download_directory_name = 'cca_info'
_file_name = 'cca_list.json'
_driver_directory_name = 'driver'
_DRIVER_CONFIG_DIRECTORY = Path(getcwd() + '/driver_config.yaml')
_URL_DIRECTORY = Path(getcwd() + '/urls.yaml')


def get_user_defined_driver_info():
    driver_config_directory = _verify_driver_config_file_exists()
    driver_config = _get_driver_config_from_file(driver_config_directory)

    return driver_config


def _verify_driver_config_file_exists():
    driver_config_directory = _driver_config_file_is_present()

    if not driver_config_directory:
        raise FileNotFoundError(driver_config_directory)

    return driver_config_directory


def _driver_config_file_is_present():
    return _file_is_present_in_directory(_DRIVER_CONFIG_DIRECTORY)


def _file_is_present_in_directory(directory):
    # isFile checks if the file is a regular file and exists
    if not isfile(directory):
        return None
    return directory


def _get_driver_config_from_file(file_directory):
    with open(file_directory) as file:
        driver_config = safe_load(file)  # generates a dictionary from the config file

        if not driver_config:
            raise FileNotFoundError(file_directory)

        _validate_user_config_keys(driver_config)

        return driver_config


def _validate_user_config_keys(driver_config):
    if _has_missing_config_file_information(driver_config):
        raise KeyError(driver_config)

    driver_config['type'] = driver_config['type'].upper()


def _has_missing_config_file_information(driver_info):
    if not driver_info or \
            not driver_info['type'] or \
            not driver_info['name']:
        return True

    return False


def setup_download_directory(driver_config, school_name):
    driver_config['path'] = _check_if_driver_exists(driver_config['name'])
    driver_config['download_directory'] = _create_download_directory(school_name)


def _check_if_driver_exists(driver_file_name):
    if system() == 'Windows':
        driver_file_name += '.exe'

    driver_path = path.join(getcwd(), _driver_directory_name, driver_file_name)

    if not driver_path:
        raise FileNotFoundError(driver_path)

    return driver_path


def _create_download_directory(school_name):
    root_download_directory_path = path.join(getcwd(), _download_directory_name, school_name)

    makedirs(root_download_directory_path, mode=_default_directory_permission_mode, exist_ok=True)

    return root_download_directory_path


def get_school_cca_url(school_code):
    url_file_directory = _verify_url_file_exists()
    url_list = _get_school_cca_url_from_file(url_file_directory)

    return url_list[school_code]


def _verify_url_file_exists():
    url_file_directory = _url_file_is_present()

    if not url_file_directory:
        raise FileNotFoundError(url_file_directory)

    return url_file_directory


def _url_file_is_present():
    return _file_is_present_in_directory(_URL_DIRECTORY)


def _get_school_cca_url_from_file(url_file_directory):
    with open(url_file_directory) as file:
        url_list = safe_load(file)  # generates a dictionary from the config file

        if not url_list:
            raise FileNotFoundError(url_file_directory)

        return url_list


def dump_records(records, download_directory):
    file_path = path.join(download_directory, _file_name)

    with open(file_path, 'w') as f:
        # for record in records:
        dump(records, f)

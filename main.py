from util.arguments_constructor import get_arg_parser
from automator import get_automator_by_school_code, get_valid_school_codes


def main(browser_options=None, school_code='np'):
    if not school_code:
        print(f'Please provide a school code! \n\nAvailable school codes: \n{get_valid_school_codes()}')
        return

    scraper, url_to_scrape = get_automator_by_school_code(school_code.lower())

    if not scraper:
        print(f'Invalid school code! \n\nThe following school codes are available: \n{get_valid_school_codes()}')
        return

    if not browser_options:
        scraper.start_job(url=url_to_scrape)
    else:
        scraper.start_job(url=url_to_scrape, browser_options=browser_options)


if __name__ == '__main__':
    arguments = get_arg_parser()

    main(arguments.browser_options, arguments.school)

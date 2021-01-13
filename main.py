# from automator.np_cca_automator import NpCcaAutomator
from automator.tp_cca_automator import TpCcaAutomator
from util.arguments_constructor import get_arg_parser


def main(browser_options=None):
    automator = TpCcaAutomator()
    url_to_scrape = 'https://www.tp.edu.sg/life-at-tp/cca-events.html'

    if not browser_options:
        automator.start_job(url=url_to_scrape)
    else:
        automator.start_job(url=url_to_scrape, browser_options=browser_options)


if __name__ == '__main__':
    arguments = get_arg_parser()

    main(arguments.browser_options)

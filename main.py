from automator.np_cca_automator import NpCcaAutomator
from util.arguments_constructor import get_arg_parser


def main(browser_options=None):
    automator = NpCcaAutomator()

    if not browser_options:
        automator.start_job(url='https://www.np.edu.sg/studentlife/Pages/ccas.aspx')
    else:
        automator.start_job(url='https://www.np.edu.sg/studentlife/Pages/ccas.aspx', browser_options=browser_options)


if __name__ == '__main__':
    arguments = get_arg_parser()

    main(arguments.browser_options)

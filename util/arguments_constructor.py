from argparse import ArgumentParser

_parser = ArgumentParser(description='Browser options for the automator')
_parser.add_argument('-bo', '--browser-options', type=str,
                     help='Additional browser options for the webdriver utilised by the automator')


def get_arg_parser():
    return _parser.parse_args()

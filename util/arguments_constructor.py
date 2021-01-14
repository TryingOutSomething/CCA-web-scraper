from argparse import ArgumentParser

_parser = ArgumentParser(description='Additional options for the automator')
_parser.add_argument('-bo', '--browser-options', type=str,
                     help='Additional browser options for the webdriver utilised by the automator')
_parser.add_argument('--school', type=str,
                     help='School of choice: np (Ngee Ann Polytechnic) or tp (Temasek Polytechnic)')


def get_arg_parser():
    return _parser.parse_args()

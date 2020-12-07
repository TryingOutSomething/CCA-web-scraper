from automator.np_cca_automator import NpCcaAutomator


def main():
    # create download location
    automator = NpCcaAutomator()
    # automator.start_job(url='https://www.np.edu.sg/studentlife/Pages/ccas.aspx', browser_options='headless')
    automator.start_job(url='https://www.np.edu.sg/studentlife/Pages/ccas.aspx')
    # automate stuff lmao
    # store into json file
    pass


if __name__ == '__main__':
    main()

class WebDriverFactory:
    def __init__(self):
        self._drivers = {}
        self._driver_options = {}

    def register_web_driver(self, driver_type, web_driver, driver_options):
        self._drivers[driver_type] = web_driver
        self._driver_options[driver_type] = driver_options

    def get_registered_web_drivers(self):
        return self._drivers

    def get_web_driver(self, driver_type, driver_path, user_defined_options=None):
        driver_options_reference = self._driver_options[driver_type]
        web_driver = self._drivers[driver_type]

        if not web_driver:
            raise NotImplemented(f'Unsupported type for browser {driver_type}.')

        if not user_defined_options or not driver_options_reference:
            return web_driver(driver_path)

        driver_options = driver_options_reference()

        if driver_type == 'EDGE':
            driver_options.use_chromium = True

        driver_options.add_argument(user_defined_options)
        return web_driver(executable_path=driver_path, options=driver_options)

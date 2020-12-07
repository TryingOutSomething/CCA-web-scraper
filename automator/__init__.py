class Automator:
    def start_job(self, url, browser_options):
        raise NotImplemented

    def _login(self):
        raise NotImplemented

    def _get_all_assets_info(self):
        raise NotImplemented

    def _download(self, urls):
        raise NotImplemented

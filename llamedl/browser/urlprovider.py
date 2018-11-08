from llamedl.browser.basebrowser import BaseBrowser


class UrlProvider(BaseBrowser):
    def __init__(self, url):
        self.url = url

    def get_urls(self):
        return {'User url': self.url}

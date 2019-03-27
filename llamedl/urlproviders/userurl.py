from llamedl.urlproviders.baseurl import BaseUrl


class UserUrl(BaseUrl):
    def __init__(self, url):
        self.url = url

    def get_urls(self):
        return [self.url]

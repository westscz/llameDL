import unittest
from llamedl.browser.urlprovider import UrlProvider


class TestUrlProvider(unittest.TestCase):
    def test_get_urls(self):
        url = "http://foo.bar"
        obj = UrlProvider(url)
        self.assertDictEqual({'User url': url}, obj.get_urls())

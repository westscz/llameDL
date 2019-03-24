import unittest

from llamedl.urlproviders.userurl import UserUrl


class TestUserUrl(unittest.TestCase):
    def test_get_urls(self):
        url = 'http://foo.bar'
        obj = UserUrl(url)
        self.assertDictEqual({'User url': url}, obj.get_urls())

import unittest

from llamedl.urlproviders.chromeurls import ChromeUrl
from tests.utils import create_chrome_bookmarks_file


class TestChromeUrls(unittest.TestCase):
    def setUp(self):
        self.data = {
            "roots": {
                "bookmark_bar": {
                    "children": [
                        {
                            "children": [
                                {
                                    "name": "Infected Mushroom - Guitarmass - YouTube",
                                    "type": "url",
                                    "url": "https://www.youtube.com/watch?v=R_uS0aT0bG8",
                                },
                                {
                                    "name": "Infected Mushroom & Bliss - Bliss on Mushrooms (feat. Miyavi) [Monstercat Release] - YouTube",
                                    "type": "url",
                                    "url": "https://www.youtube.com/watch?v=ceYKKNXFpSE",
                                },
                                {
                                    "name": "MESZI live at Club Holidays, Orchowo (2019.02.23), Meszi",
                                    "type": "url",
                                    "url": "https://soundcloud.com/meszi/meszi1902",
                                },
                            ],
                            "name": "Music",
                            "type": "folder",
                        }
                    ],
                    "name": "Bookmarks bar",
                    "type": "folder",
                }
            }
        }
        filepath = create_chrome_bookmarks_file(self.data)
        self.obj = ChromeUrl(filepath)

    def test_get_folder__exist(self):
        result = self.obj.get_folder("Music")
        expected = self.data["roots"]["bookmark_bar"]["children"][0]["children"]
        self.assertListEqual(expected, result)

    def test_get_folder__not_exist(self):
        with self.assertRaises(IndexError):
            self.obj.get_folder("Music foo")

    def test_get_youtube_urls_from_folder__exist(self):
        result = self.obj.get_youtube_urls_from_folder("Music")
        expected = [
            "https://www.youtube.com/watch?v=R_uS0aT0bG8",
            "https://www.youtube.com/watch?v=ceYKKNXFpSE",
        ]
        self.assertListEqual(expected, result)

    def test_get_youtube_urls_from_folder__not_exist(self):
        with self.assertRaises(IndexError):
            self.obj.get_youtube_urls_from_folder("Music foo")

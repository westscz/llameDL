import unittest
from unittest import mock

from llamedl.tagsproviders.lastfmtags import LastFmTags


class TestLastFmTags(unittest.TestCase):
    def setUp(self):
        self.data = {
            "artist": {
                "name": "Infected Mushroom",
                "tags": {
                    "tag": [
                        {
                            "name": "psytrance",
                            "url": "https://www.last.fm/tag/psytrance",
                        },
                        {
                            "name": "electronic",
                            "url": "https://www.last.fm/tag/electronic",
                        },
                        {
                            "name": "psychedelic",
                            "url": "https://www.last.fm/tag/psychedelic",
                        },
                        {"name": "trance", "url": "https://www.last.fm/tag/trance"},
                        {"name": "goa", "url": "https://www.last.fm/tag/goa"},
                    ]
                },
            }
        }
        self.obj = LastFmTags()

    @mock.patch("llamedl.tagsproviders.lastfmtags.LastFmTags._retrieve_data")
    def test_get_tags__available(self, patch_retrieve_data):
        patch_retrieve_data.return_value = self.data
        expected = ["Psytrance", "Electronic", "Psychedelic", "Trance", "Goa"]
        result = self.obj.get_tags("Infected Mushroom")

        self.assertListEqual(expected, result)

    @mock.patch("llamedl.tagsproviders.lastfmtags.LastFmTags._retrieve_data")
    def test_get_tags__not_available(self, patch_retrieve_data):
        patch_retrieve_data.return_value = []
        expected = []
        result = self.obj.get_tags("Infected Mushroom")

        self.assertListEqual(expected, result)

import unittest
from unittest import mock

from llamedl.tagsproviders.musicbrainzngstags import MusicbrainzngsTags


class TestMusicbrainzngsTags(unittest.TestCase):
    def setUp(self):
        self.data = {
            "artist-list": [
                {
                    "id": "eab76c9f-ff91-4431-b6dd-3b976c598020",
                    "type": "Group",
                    "ext:score": "100",
                    "name": "Infected Mushroom",
                    "tag-list": [
                        {"count": "0", "name": "trance"},
                        {"count": "7", "name": "electronic"},
                        {"count": "1", "name": "dubstep"},
                        {"count": "2", "name": "electronica"},
                        {"count": "7", "name": "psytrance"},
                    ],
                }
            ],
            "artist-count": 1,
        }
        self.obj = MusicbrainzngsTags()

    @mock.patch(
        "llamedl.tagsproviders.musicbrainzngstags.MusicbrainzngsTags._retrieve_data"
    )
    def test_get_tags__available(self, patch_retrieve_data):
        patch_retrieve_data.return_value = self.data
        expected = ["Trance", "Electronic", "Dubstep", "Electronica", "Psytrance"]
        result = self.obj.get_tags("Infected Mushroom")

        self.assertListEqual(expected, result)

    @mock.patch(
        "llamedl.tagsproviders.musicbrainzngstags.MusicbrainzngsTags._retrieve_data"
    )
    def test_get_tags__not_available(self, patch_retrieve_data):
        patch_retrieve_data.return_value = {}
        expected = []
        result = self.obj.get_tags("Infected Mushroom")

        self.assertListEqual(expected, result)

from dataclasses import dataclass

import pytest

from llame.tag_providers.lastfm import LastFMProvider


@dataclass
class ResponseMock:
    def __init__(self, response):
        self.resp = response

    def json(self):
        return self.resp


@pytest.fixture
def response():

    data = {
        "artist": {
            "name": "Taylor Swift",
            "mbid": "20244d07-534f-4eff-b4d4-930878889970",
            "url": "https://www.last.fm/music/Taylor+Swift",
            "image": [
                {
                    "#text": "https://lastfm.freetls.fastly.net/i/u/34s/2a96cbd8b46e442fc41c2b86b821562f.png",
                    "size": "small",
                },
                {
                    "#text": "https://lastfm.freetls.fastly.net/i/u/64s/2a96cbd8b46e442fc41c2b86b821562f.png",
                    "size": "medium",
                },
                {
                    "#text": "https://lastfm.freetls.fastly.net/i/u/174s/2a96cbd8b46e442fc41c2b86b821562f.png",
                    "size": "large",
                },
                {
                    "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                    "size": "extralarge",
                },
                {
                    "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                    "size": "mega",
                },
                {
                    "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png",
                    "size": "",
                },
            ],
            "streamable": "0",
            "ontour": "1",
            "stats": {
                "listeners": "2379086",
                "playcount": "227645694",
                "userplaycount": "27",
            },
            "tags": {
                "tag": [
                    {"name": "country", "url": "https://www.last.fm/tag/country"},
                    {"name": "pop", "url": "https://www.last.fm/tag/pop"},
                    {
                        "name": "female vocalists",
                        "url": "https://www.last.fm/tag/female+vocalists",
                    },
                    {
                        "name": "singer-songwriter",
                        "url": "https://www.last.fm/tag/singer-songwriter",
                    },
                    {"name": "acoustic", "url": "https://www.last.fm/tag/acoustic"},
                ]
            },
            "bio": {
                "links": {
                    "link": {
                        "#text": "",
                        "rel": "original",
                        "href": "https://last.fm/music/Taylor+Swift/+wiki",
                    }
                },
                "published": "16 Aug 2006, 21:31",
            },
        }
    }
    return ResponseMock(data)


@pytest.fixture
def provider_result():
    return set(["Singer-Songwriter", "Female Vocalists", "Acoustic", "Country", "Pop"])


@pytest.fixture
def tag_provider() -> LastFMProvider:
    return LastFMProvider()


@pytest.fixture
def artist():
    return "Taylor Swift"


def test_get_tags(mocker, artist, tag_provider, response, provider_result):
    response_patch = mocker.patch("llame.tag_providers.lastfm.requests.get")
    response_patch.return_value = response
    result = tag_provider.get_tags_for(artist)
    assert set(result) == provider_result

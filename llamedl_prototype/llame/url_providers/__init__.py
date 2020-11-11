from collections import namedtuple

entry = namedtuple("entry", ["url", "artist", "title", "vendor"])


class BaseUrlProvider:
    def __init__(self, supported_vendors, path):
        self.supported_vendors = supported_vendors
        self.path = path

    def get_urls(self, **kwargs) -> []:
        """Return list of supported urls"""

    def _is_alive(self, url) -> bool:
        return False

    def _is_supported(self, url) -> bool:
        return any((vendor(url) for vendor in self.supported_vendors))


class SingleUrlProvider(BaseUrlProvider):
    def get_urls(self, **kwargs) -> []:
        return self.path


class PlaylistUrlProvider(BaseUrlProvider):
    def get_urls(self, **kwargs) -> []:
        return self._get_urls_from_playlist()

    def _get_urls_from_playlist(self) -> []:
        return []


class FirefoxBookmarksUrlProvider(BaseUrlProvider):
    def get_urls(self, **kwargs) -> []:
        return self._get_urls_from_file()

    def _get_urls_from_file(self) -> []:
        return []

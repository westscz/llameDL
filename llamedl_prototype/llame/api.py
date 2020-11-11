from .downloader import DownloadManager
from .tag_providers import get_tag_providers
from .tagger import Tagger
from .url_providers import BaseUrlProvider


class LlamedlAPI:
    def __init__(self, downloader):
        self.downloader = downloader  # Downloader(Tagger(get_tag_providers()))
        self.additional_tags = {}
        self.default_path = None

    def set_additional_static_tags(self, **additional_tags):
        self.additional_tags = additional_tags

    def set_default_path(self, path):
        self.default_path = path

    def get_urls(self, url_provider: BaseUrlProvider) -> []:
        return url_provider.get_urls()

    def download_file(self, url: str) -> str:
        """Download file and return path"""
        return self.downloader.download(self.default_path, url, self.additional_tags)

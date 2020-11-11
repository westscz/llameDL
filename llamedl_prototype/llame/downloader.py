from .tagger import Tagger


class DownloadManager:
    """Download files and properly change them"""

    def __init__(self, tagger: Tagger):
        self.tagger = tagger

    def download(self, path: str, url: str, additional_tags: {}) -> str:
        """Download file and return path to this file"""
        file_path = self._download_file(path, url)
        self._update_filename(file_path)
        self._update_tags(file_path, additional_tags)
        return file_path

    def _download_file(self, path: str, url: str) -> str:
        """Download file to audio format and return path to file"""
        return ""

    def _update_filename(self, path: str):
        """Update / fix filename of audio file"""

    def _update_tags(self, path: str, additional_tags: {}):
        """Update / add tags to file"""
        self.tagger.tag_files(path, additional_tags)

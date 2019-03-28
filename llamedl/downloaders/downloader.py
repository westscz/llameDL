import os

from tqdm import tqdm

from llamedl.downloaders.youtubedownloader import YouTubeDownloader
from llamedl.progress_logger import progresslogger


class Downloader:
    def __init__(self, download_directory):
        self._download_directory = download_directory
        self.downloaders_map = {"youtube": YouTubeDownloader(self.download_directory)}

    def download(self, provider):
        downloaded_urls = []
        urls = provider.get_urls()
        if not urls:
            return 1
        url_gen = tqdm(urls, desc="Download start")
        for url in url_gen:
            progresslogger.push_logger(url_gen)
            filename = self._download_song(url)
            print(filename)
            downloaded_urls.extend(filename)
        url_gen.set_description("Download end")
        return downloaded_urls

    def _download_song(self, url):
        for key, downloader in self.downloaders_map.items():
            if key in url:
                return downloader.download(url)

    @property
    def download_directory(self):
        if not self._download_directory:
            self._download_directory = "{}/Music".format(os.getenv("HOME"))
        return self._download_directory

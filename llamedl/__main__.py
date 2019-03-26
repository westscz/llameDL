import os

import fire

from llamedl.downloaders.downloader import Downloader
from llamedl.tagsproviders.tagger import Tagger
from llamedl.urlproviders.chromeurls import ChromeUrl
from llamedl.urlproviders.netscapefileurl import NetscapeFileUrl
from llamedl.urlproviders.userurl import UserUrl
from llamedl.utill import create_logger

LOGGER = create_logger("LlameDL")


class LlameDLFire:
    """
    LlameDL

    Download your music from URLs
    Use -- --help flag for more information

    """

    def __init__(self, tags_file="", download_directory=""):
        """
        :param tags_file: Path to YAML file with artist:tags variables
        :param download_directory: Directory where audio files will be saved
        """
        download_directory = (
            "{}/Music".format(os.getenv("HOME"))
            if not download_directory
            else download_directory
        )
        self._download_engine = Downloader(download_directory)
        self._tag_engine = Tagger(download_directory, tags_file)
        self._providers_map = {"chrome": ChromeUrl}

    def playlist(self, url):
        """
        Download music from url

        :param url: Playlist url
        """
        provider = UserUrl(url)
        self._download(provider)

    def browser(self, browser, folder_name="Music", user="Default", bookmarks_path=""):
        """
        Download music from urls based on browser bookmarks

        :param browser: Type of url provider, available: Chrome
        :param folder_name: Folder name in bookmarks
        :param user: Browser user
        """
        provider = self._providers_map.get(browser.lower(), None)
        if provider is None:
            LOGGER.error(
                "Your browser is not supported yet. "
                "Please add issue on github and use 'llamedl file' option instead"
            )
            return
        provider = provider(bookmarks_path, user, folder_name)
        self._download(provider)

    def bookmarks(self, path, folder_name="Music"):
        """
        Download music from urls based on bookmarks file in Netscape format.
        More information here: https://msdn.microsoft.com/en-us/ie/aa753582(v=vs.94)

        :param path: Path to bookmarks file in Netscape format
        :param folder_name: Folder name in bookmarks
        """
        provider = NetscapeFileUrl(path, folder_name)
        self._download(provider)

    def _download(self, provider):
        """
        Download and tag downloaded files
        :param provider: Url provider
        """
        LOGGER.info("Downloading start")
        downloaded_files = self._download_engine.download(provider)
        LOGGER.info("Downloading done, tagging start")
        self._tag_engine.add_tags_to_files(downloaded_files)
        LOGGER.info("Tagging done")

    def help(self):
        print(self.__doc__)


def llamedl_cli():
    fire.Fire(LlameDLFire)


if __name__ == "__main__":
    llamedl_cli()

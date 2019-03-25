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
     _     _                      ____  _
    | |   | | __ _ _ __ ___   ___|  _ \| |
    | |   | |/ _` | '_ ` _ \ / _ \ | | | |
    | |___| | (_| | | | | | |  __/ |_| | |___
    |_____|_|\__,_|_| |_| |_|\___|____/|_____|

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
        :return:
        """
        provider = UserUrl(url)
        downloaded_files = self._download_engine.download(provider)
        self._tag_engine.add_tags_to_files(downloaded_files)

    def browser(self, browser, folder_name="Music", user="Default"):
        """
        Download music from urls based on browser bookmarks

        :param browser: Type of url provider, available: Chrome
        :param folder_name: Folder name in bookmarks
        :param user: Browser user
        :return:
        """
        provider = self._providers_map.get(browser.lower(), None)
        if provider is None:
            LOGGER.error(
                "Your browser is not supported yet. "
                "Please add issue on github and use 'llamedl file' option instead"
            )
            return
        provider = provider("", user, folder_name)
        LOGGER.info("Downloading start")
        downloaded_files = self._download_engine.download(provider)
        LOGGER.info("Downloading done, tagging start")
        self._tag_engine.add_tags_to_files(downloaded_files)
        LOGGER.info("Tagging done")

    def bookmark(self, path, folder_name="Music"):
        """
        Download music from urls based on bookmark file in Netscape format.
        More information here: https://msdn.microsoft.com/en-us/ie/aa753582(v=vs.94)

        :param path: Path to bookmarks file in Netscape format
        :param folder_name: Folder name in bookmarks
        :return:
        """
        provider = NetscapeFileUrl(path, folder_name)
        downloaded_files = self._download_engine.download(provider)
        self._tag_engine.add_tags_to_files(downloaded_files)

    def help(self):
        print(self.__doc__)


def llamedl_cli():
    fire.Fire(LlameDLFire)


if __name__ == "__main__":
    llamedl_cli()

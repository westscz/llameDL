"""
llamedl.chrome.py
=========
"""
import json
import os
import subprocess

from llamedl.urlproviders.basebrowser import BaseBrowser
from llamedl.utill import create_logger

LOGGER = create_logger(__name__)


class ChromeUrl(BaseBrowser):
    """Class to retrieve bookmarks from google chrome urlproviders."""

    def __init__(self, bookmarks_path=None, user=None, bookmark_folder_name="Music"):
        super(ChromeUrl, self).__init__(bookmark_folder_name, url_title_name="name")
        self.__url_list = list()
        self.__bookmarks_json = None
        self.__bookmarks_path = bookmarks_path
        self.user = user if user is not None else "Default"

    @property
    def bookmarks(self):
        """TBD.

        :return:
        """
        LOGGER.debug(self.bookmarks_path)
        with open(self.bookmarks_path) as json_data:
            data = json.load(json_data)
            self.__bookmarks_json = (
                data.get("roots").get("bookmark_bar").get("children")
            )
        return self.__bookmarks_json

    @property
    def bookmarks_path(self):
        if not self.__bookmarks_path:
            self.__bookmarks_path = self._get_bookmarks_path()
        return self.__bookmarks_path

    def _get_bookmarks_path(self):
        output = subprocess.check_output(["which", "chromium"]).decode("utf-8")
        env_home_path = os.getenv("HOME")
        if "snap" in output:
            return f"{env_home_path}/snap/chromium/current/.config/chromium/{self.user}/Bookmarks"
        else:
            return f"{env_home_path}/.config/chromium/{self.user}/Bookmarks"

"""
llamedl.chrome.py
=========
"""
import json
import os
import subprocess

from llamedl.urlproviders.basebrowser import BaseBrowser
from llamedl.urlproviders.baseurl import BaseUrl
from llamedl.utill import create_logger

LOGGER = create_logger(__name__)


class ChromeUrl(BaseUrl, BaseBrowser):
    """Class to retrieve bookmarks from google chrome urlproviders."""

    def __init__(self, bookmarks_path=None, user=None, folder_name=None):
        self.__url_list = list()
        self.__bookmarks_json = None
        self.__bookmarks_path = bookmarks_path
        self.user = user if user is not None else 'Default'
        self.folder_name = folder_name

    @property
    def bookmarks_path(self):
        if not self.__bookmarks_path:
            self.__bookmarks_path = self._get_bookmarks_path()
        return self.__bookmarks_path

    @property
    def bookmarks(self):
        """TBD.

        :return:
        """
        LOGGER.debug(self.bookmarks_path)
        with open(self.bookmarks_path) as json_data:
            data = json.load(json_data)
            self.__bookmarks_json = data.get('roots').get('bookmark_bar').get('children')
        return self.__bookmarks_json

    def get_urls(self):
        return self.get_youtube_urls_from_folder(self.folder_name)

    def _get_bookmarks_path(self):
        output = subprocess.check_output(['which', 'chromium']).decode('utf-8')
        env_home_path = os.getenv('HOME')
        if 'snap' in output:
            return f'{env_home_path}/snap/chromium/current/.config/chromium/{self.user}/Bookmarks'
        else:
            return f'{env_home_path}/.config/chromium/{self.user}/Bookmarks'

    def get_youtube_urls_from_folder(self, folder_name):
        """TBD.

        :param folder_name: Folder name in chrome bookmarks
        :return:
        """
        urls_data = {}
        for node in self.get_folder(folder_name):
            url = node.get('url', '')
            if 'youtube' in url:
                name = node.get('name', '')
                urls_data[name] = url
        LOGGER.debug('I found %s urls', str(len(urls_data)))
        for name, url in urls_data.items():
            LOGGER.debug("Title: {} Url: {}".format(name, url))
        return list(urls_data.values())

    def get_folder(self, folder_name):
        """TBD.

        :param folder_name:
        :return:
        """
        folder_data = self.__find_folder_in_bookmarks(folder_name, self.bookmarks)
        if not folder_data:
            raise IndexError(f"Bookmarks does not have '{folder_name}' folder")
        return folder_data

    def __find_folder_in_bookmarks(self, folder_name, bookmarks):
        for bookmark in bookmarks:
            if bookmark.get('type') == 'folder' and bookmark.get('name') == folder_name:
                return bookmark.get('children')
            elif bookmark.get('type') == 'folder':
                result = self.__find_folder_in_bookmarks(folder_name, bookmark.get('children'))
                if result:
                    return result


if __name__ == '__main__':
    c = ChromeUrl(folder_name='Music')
    print(c.get_urls())

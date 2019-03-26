from bookmarks_parser import parse

from llamedl.urlproviders.baseurl import BaseUrl
from llamedl.utill import create_logger

LOGGER = create_logger(__name__)


class NetscapeFileUrl(BaseUrl):
    def __init__(self, bookmarks_path, bookmark_folder_name="Music"):
        self.last_urls = None
        self.__bookmarks_json = None
        self.bookmarks_path = bookmarks_path
        self.bookmark_folder_name = bookmark_folder_name

        self.url_title_name = "title"

    def get_urls(self) -> []:
        return self.get_youtube_urls_from_folder(self.bookmark_folder_name)

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
            if (
                bookmark.get("type") == "folder"
                and bookmark.get(self.url_title_name, None) == folder_name
            ):
                return bookmark.get("children")
            elif bookmark.get("type") == "folder":
                result = self.__find_folder_in_bookmarks(
                    folder_name, bookmark.get("children")
                )
                if result:
                    return result

    def get_youtube_urls_from_folder(self, folder_name):
        """TBD.

        :param folder_name: Folder name in chrome bookmarks
        :return:
        """
        return self.__get_urls_from_folder_from_given_source(folder_name, "youtube")

    def __get_urls_from_folder_from_given_source(self, folder_name, source):
        urls_data = {}
        for node in self.get_folder(folder_name):
            url = node.get("url", "")
            if source in url:
                name = node.get(self.url_title_name, "")
                urls_data[name] = url
        LOGGER.debug("I found %s urls", str(len(urls_data)))
        for name, url in urls_data.items():
            LOGGER.debug("Title: {} Url: {}".format(name, url))
        self.last_urls = urls_data
        return list(urls_data.values())

    @property
    def bookmarks(self):
        """TBD.

        :return:
        """
        LOGGER.debug(self.bookmarks_path)
        self.__bookmarks_json = parse(self.bookmarks_path)
        return self.__bookmarks_json

from llamedl.urlproviders.baseurl import BaseUrl
from llamedl.utill import create_logger

LOGGER = create_logger(__name__)


class BaseBrowser(BaseUrl):
    def __init__(self, bookmark_folder_name, url_title_name):
        self.bookmark_folder_name = bookmark_folder_name
        self.url_title_name = url_title_name

    @property
    def bookmarks(self):
        return []

    def get_urls(self) -> []:
        return self.get_youtube_urls_from_folder(self.bookmark_folder_name)

    def get_youtube_urls_from_folder(self, folder_name):
        """TBD.

        :param folder_name: Folder name in chrome bookmarks
        :return:
        """
        return self.__get_urls_from_folder_from_given_source(folder_name, "youtube")

    def get_folder(self, folder_name):
        """
        Get bookmarks from given folder name

        :param folder_name: Name of searched folder
        :return:
        """
        folder_data = self.__find_folder_in_bookmarks(folder_name, self.bookmarks)
        if not folder_data:
            raise IndexError(f"Bookmarks does not have '{folder_name}' folder")
        return folder_data

    def __get_urls_from_folder_from_given_source(self, folder_name, source):
        urls_data = {}
        for node in self.get_folder(folder_name):
            url = node.get("url", "")
            if source in url:
                name = node.get(self.url_title_name, "")
                urls_data[name] = url
        LOGGER.debug("Found %s urls", str(len(urls_data)))
        for name, url in urls_data.items():
            LOGGER.debug("Title: {} Url: {}".format(name, url))
        self.last_urls = urls_data
        return list(urls_data.values())

    def __find_folder_in_bookmarks(self, folder_name, bookmarks):
        for bookmark in bookmarks:
            if self._is_searched_folder(bookmark, folder_name):
                return bookmark.get("children")
            elif self._is_folder(bookmark):
                result = self.__find_folder_in_bookmarks(
                    folder_name, bookmark.get("children")
                )
                if result:
                    return result

    def _is_folder(self, bookmark):
        return bookmark.get("type") == "folder"

    def _is_searched_folder(self, bookmark, folder_name):
        return (
                self._is_folder(bookmark)
                and bookmark.get(self.url_title_name, None) == folder_name
        )

from bookmarks_parser import parse

from llamedl.urlproviders.basebrowser import BaseBrowser
from llamedl.utill import create_logger

LOGGER = create_logger(__name__)


class NetscapeFileUrl(BaseBrowser):
    def __init__(self, bookmarks_path, bookmark_folder_name="Music"):
        super(NetscapeFileUrl, self).__init__(
            bookmark_folder_name, url_title_name="title"
        )
        self.last_urls = None
        self.__bookmarks_json = None
        self.bookmarks_path = bookmarks_path

    @property
    def bookmarks(self):
        """
        Bookmarks data

        :return:
        """
        if not self.__bookmarks_json:
            LOGGER.debug(self.bookmarks_path)
            self.__bookmarks_json = parse(self.bookmarks_path)
        return self.__bookmarks_json

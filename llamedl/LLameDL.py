from llamedl.ichrome import IChrome
from llamedl.iyoutube import IYouTube
from llamedl.tagger import Tagger
import os


class LLameDL:
    def __init__(self):
        self.chrome = None
        self.youtube = None
        self.tagger = None

        self.__folder_name = None
        self.__download_directory = None

    def main(self, download_directory=None, bookmarks_path=None, folder_name='MM'):
        if not download_directory:
            self.__download_directory = "{}/Music".format(os.getenv("HOME"))

        self.chrome = IChrome(bookmarks_path)
        self.youtube = IYouTube(self.__download_directory)
        self.tagger = Tagger(whitelist_from_file=True)

        url_list = self.chrome.get_yt_urls(folder_name)
        for url in url_list:
            self.download_song(url)

    def download_song(self, url):
        self.youtube.url_info = url
        rc = self.youtube.download_mp3(url)
        if rc:
            title = self.youtube.get_title()
            self.tagger.add_tags_to_file(title, self.__download_directory)

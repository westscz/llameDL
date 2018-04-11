"""
    llamedl.LLameDL.py
    ~~~~~~~~~~~~~~~~~~~
"""
import os
import sys
import argparse
from tqdm import tqdm
from llamedl.ichrome import IChrome
from llamedl.iyoutube import IYouTube
from llamedl.tagger import Tagger


class LLameDL:
    def __init__(self):
        self.chrome = None
        self.youtube = None
        self.tagger = None

        self.directory_path = None
        self.bookmark_name = "Music"
        self.url = None
        self.whitelist_path = "../common/whitelist.cfg"

        self.__folder_name = None
        self.__download_directory = None

    def main(self, bookmarks_path=None):
        self.parse_args(sys.argv[1:])
        self.__download_directory = "{}/Music".format(os.getenv("HOME")) if not self.directory_path \
            else self.directory_path

        self.chrome = IChrome(bookmarks_path)
        self.youtube = IYouTube(self.__download_directory)
        self.tagger = Tagger()
        self.tagger.load_filters()

        url_list = self.chrome.get_yt_urls(self.bookmark_name) if not self.url else self.youtube.verify_url(self.url)
        for url in tqdm(url_list):
            self.download_song(url)

    def download_song(self, url):
        self.youtube.url_info = url
        rc = self.youtube.download_mp3(url)
        if rc:
            title = self.youtube.get_title()
            self.tagger.add_tags_to_file(title, self.__download_directory)

    def parse_args(self, args, namespace=None):
        parser = argparse.ArgumentParser(prog="LlameDL")
        parser.add_argument('-d', '--directory_path', help="Path to directory where audio should be saved, "
                                                           "default=~/Music")
        parser.add_argument('-n', '--bookmark_name', help="Name of folder in chrome bookmarks, "
                                                          "default=Music")
        parser.add_argument('-u', '--url', help="Url to Youtube video or playlist")
        parser.add_argument('-c', '--cover', help="Path to album cover, if album cover should be added")
        parser.add_argument('-w', '--whitelist_path', help="Path to txt file with whitelisted tags")
        return parser.parse_args(args, namespace=namespace)


if __name__ == '__main__':
    llamedl = LLameDL()
    llamedl.main()
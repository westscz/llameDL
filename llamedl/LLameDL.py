"""
    llamedl.LLameDL.py
    ~~~~~~~~~~~~~~~~~~~
"""
import os
import argparse
from llamedl.ichrome import IChrome
from llamedl.iyoutube import IYouTube
from llamedl.tagger import Tagger


class LLameDL:
    def __init__(self):
        self.chrome = None
        self.youtube = None
        self.tagger = None

        self.__folder_name = None
        self.__download_directory = None

    def main(self, download_directory=None, bookmarks_path=None, folder_name='M'):
        if not download_directory:
            self.__download_directory = "{}/Music".format(os.getenv("HOME"))

        self.chrome = IChrome(bookmarks_path)
        self.youtube = IYouTube(self.__download_directory)
        self.tagger = Tagger()

        url_list = self.chrome.get_yt_urls(folder_name)
        for url in url_list:
            self.download_song(url)

    def download_song(self, url):
        self.youtube.url_info = url
        rc = self.youtube.download_mp3(url)
        if rc:
            title = self.youtube.get_title()
            self.tagger.add_tags_to_file(title, self.__download_directory)

    def __create_args_parser(self):
        parser = argparse.ArgumentParser(prog="LlameDL")
        #bookmark name
        #save path
        #url
        parser.add_argument('-c', '--cover', help="Path to album cover, if album cover should be added")
        parser.add_argument('-w', '--whitelist', help="Path to txt file with whitelisted tags")
        parser.add_argument('-b', '--blacklist', help="Path to txt file with blacklisted tags")
        return parser

if __name__ == '__main__':
    l = LLameDL()
    l.main()
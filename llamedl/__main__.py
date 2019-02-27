import argparse
import os
import sys

import tqdm

from llamedl.browser.chromebrowser import ChromeBrowser
from llamedl.browser.urlprovider import UrlProvider
from llamedl.downloaders.youtubedownloader import YouTubeDownloader
from llamedl.tags.filetags import FileTags
from llamedl.tags.lastfmtags import LastFmTags
from llamedl.tags.musicbrainzgstags import MusicbrainzgsTags
from llamedl.tags.tagger import Tagger

providers_map = {
    'chrome': ChromeBrowser
}

downloaders_map = {
    'youtube': YouTubeDownloader
}

taggers_map = [LastFmTags(), MusicbrainzgsTags()]


def get_url_provider(provider, bookmark_folder_name, bookmarks_path, browser_user, url):
    provider = providers_map.get(provider.lower(), None)
    if not provider:
        return UrlProvider(url)
    return provider(bookmarks_path, browser_user, bookmark_folder_name)


def get_taggers(file_tags):
    if file_tags:
        return taggers_map + [FileTags(file_tags)]
    return taggers_map


class LlameDL:
    def __init__(self, arguments):
        self.args = arguments
        self._url_provider = None
        self._tagger = None
        self._download_directory = None

    @property
    def tagger(self):
        if not self._tagger:
            taggers_list = get_taggers(file_tags=self.args.file_tags)
            self._tagger = Tagger(taggers=taggers_list)
        return self._tagger

    @property
    def url_provider(self):
        if not self._url_provider:
            self._url_provider = get_url_provider(provider=self.args.url_provider,
                                                  bookmark_folder_name=self.args.bookmark_folder_name,
                                                  bookmarks_path=self.args.bookmarks_path,
                                                  browser_user=self.args.browser_user, url=self.args.url)
        return self._url_provider

    @property
    def download_directory(self):
        if not self._download_directory:
            self._download_directory = '{}/Music'.format(
                os.getenv('HOME')) if not arguments.download_directory else arguments.download_directory
        return self._download_directory

    def download(self):
        urls = tqdm.tqdm(self.url_provider.get_urls())
        for url in urls:
            urls.set_description("Downloading: {}".format(url))
            self.download_song(url)

    def download_song(self, url):
        for key, downloader in downloaders_map.items():
            if key in url:
                downloader(self.download_directory).download_mp3(url)


parser = argparse.ArgumentParser(prog='LlameDL')

parser.add_argument('--file_tags', help='Path to YAML file with artist:tags variables')
parser.add_argument('--url', help='Audio url', default=None)
parser.add_argument('--url_provider', help='Type of url provider, available: Chrome', default=None)
parser.add_argument('--bookmark_folder_name', default='Music')
parser.add_argument('--bookmarks_path', help='Only if you have bookmarks file', default=None)
parser.add_argument('--browser_user', default=None)
parser.add_argument('--download_directory', default=None, help='Directory where audio files will be saved')

arguments = parser.parse_args(sys.argv[1:])

if __name__ == '__main__':
    LlameDL(arguments).download()

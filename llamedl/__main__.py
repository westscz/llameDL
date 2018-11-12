import argparse
import os
import sys

from llamedl.browser.chromebrowser import ChromeBrowser
from llamedl.browser.urlprovider import UrlProvider
from llamedl.downloaders.youtubedownloader import YouTubeDownloader
from llamedl.tags.filetags import FileTags
from llamedl.tags.lastfmtags import LastFmTags
from llamedl.tags.musicbrainzgstags import MusicbrainzgsTags

# if __name__ == '__main__':
#     llamedl = LLameDL()
#     llamedl.main()

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
    return provider(browser_user, bookmark_folder_name, bookmarks_path)


def get_taggers(file_tags):
    if file_tags:
        return taggers_map + [FileTags(file_tags)]
    return taggers_map


parser = argparse.ArgumentParser(prog='LlameDL')

parser.add_argument('--file_tags', help='Path to YAML file with artist:tags variables')
parser.add_argument('--url', help='Audio url', default=None)
parser.add_argument('--url_provider', help='Type of url provider, available: Chrome', default=None)
parser.add_argument('--bookmark_folder_name', default='Music')
parser.add_argument('--bookmarks_path', help='Only if you have bookmarks file', default=None)
parser.add_argument('--browser_user', default=None)
parser.add_argument('--download_directory', default=None, help='Directory where audio files will be saved')

x = parser.parse_args(sys.argv[1:])
print(x)

url_provider = get_url_provider(provider=x.url_provider, bookmark_folder_name=x.bookmark_folder_name,
                                bookmarks_path=x.bookmarks_path, browser_user=x.browser_user, url=x.url)
print(url_provider)

taggers = get_taggers(file_tags=x.file_tags)
print(taggers)

download_directory = '{}/Music'.format(os.getenv('HOME')) if not x.download_directory else x.download_directory


class Tagger:
    def __init__(self, taggers, whitelist_flag=True):
        """taggers: List[BaseTags]"""
        self.taggers = taggers
        self.whitelist_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'whitelist.cfg')
        self.whitelist_flag = whitelist_flag
        self._whitelist = None

    def get_tags_for_artist(self, artist):
        tags = self.get_tags_from_tags_providers(artist)
        if self.whitelist_flag:
            return self.filter_tags(tags)
        else:
            return tags

    def get_tags_from_tags_providers(self, artist):
        tags = []
        for tagger in self.taggers:
            tags.extend(tagger.get_tags(artist))
        return list(set(tags))

    def filter_tags(self, tags_list):
        filtered_tags = [tag for tag in tags_list if tag.lower() in self.whitelist]
        return filtered_tags

    @property
    def whitelist(self):
        if not self._whitelist:
            self._whitelist = self.load_whitelist()
        return self._whitelist

    def load_whitelist(self):
        with open(self.whitelist_path) as file:
            return file.read().splitlines()


t = Tagger(taggers)
print(t.get_tags_for_artist('Skrillex'))

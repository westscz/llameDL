"""

"""
import os
import time
import musicbrainzngs
import requests
from llamedl.utill import create_logger, change_string_to_tags
from urllib.error import HTTPError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

LOGGER = create_logger("Tagger")
musicbrainzngs.set_useragent("LLameDL", "0.1", "http://github.com/music")


class Tagger:
    """
    # whitelist_sample = ["pop", "rock", "soul", "r&b", "trap rap", "electronic", "dubstep"]
    # blacklist_sample = ['owsla', 'seen live']
    """
    def __init__(self, whitelist=None, blacklist=None, whitelist_from_file = False):
        self.whitelist = [] if whitelist is None else whitelist
        self.blacklist = [] if blacklist is None else blacklist
        if whitelist_from_file:
            self.load_whitelist_from_file()
        self.__artist_data = {}

    def load_whitelist_from_file(self):
        with open("/home/jarek/Projects/LlameDL/common/whitelist.cfg") as f:
            self.whitelist = f.read().splitlines()

    def get_tags(self, artist_name):
        """
        Get tags for artist_name from last.fm and musicbrainzgs
        :param artist_name:
        :return:
        """
        if artist_name == 'Unknown':
            return []
        tag_list = self.get_tags_from_musicbrainzgs(artist_name)
        if not tag_list:
            tag_list = self.get_tags_from_last_fm(artist_name)
        tags_list = [tag.get('name').title() for tag in tag_list]
        if self.whitelist:
            tags_list = self.filter_tags_with_whitelist(tags_list)
        if self.blacklist:
            tags_list = self.filter_tags_with_blacklist(tags_list)
        LOGGER.debug("%s %s", artist_name, str(tags_list))
        return tags_list.sort()

    @staticmethod
    def get_tags_from_musicbrainzgs(artist_name):
        """
        Get tags for artist_name from musicbrainzgs
        :param artist_name:
        :return:
        """
        try:
            result = musicbrainzngs.search_artists(artist_name)
            if result.get('artist-count', 0):
                for artist_data in result.get('artist-list'):
                    if artist_data.get('name').lower() == artist_name.lower():
                        return artist_data.get('tag-list', {})
        except (HTTPError, musicbrainzngs.musicbrainz.ResponseError):
            pass
        return []

    @staticmethod
    def get_tags_from_last_fm(artist_name):
        """
        Get tags for artist_name from last_fm
        :param artist_name:
        :return:
        """
        artist_name = artist_name.replace(" ", "%20")
        api_key = "a7b8b15b54a347be1736dd0f77c7d048"
        response = requests.get(
            "http://ws.audioscrobbler.com/2.0/?"
            "method=artist.getInfo&artist={artist}&user=RJ&"
            "api_key={api_key}&format=json".format(
                artist=artist_name, api_key=api_key))
        if response.json().get('error'):
            return []
        tags = response.json().get('artist').get('tags').get('tag', [])
        return tags

    def filter_tags_with_whitelist(self, tags_list):
        """
        TBD
        :param tags_list:
        :return:
        """
        return [tag for tag in tags_list if tag.lower() in self.whitelist]

    def filter_tags_with_blacklist(self, tags_list):
        """
        TBD
        :param tags_list:
        :return:
        """
        return [tag for tag in tags_list if tag not in self.blacklist]

    def add_tags_to_file(self, filename, folder_path, cover=None):
        """

        :param filename:
        :param folder_path:
        :param cover:
        :return:
        """
        filename_suffix = 'mp3'
        LOGGER.info("Adding tags to {}".format(filename))
        filepath = os.path.join(folder_path, filename + '.' + filename_suffix)

        audio = EasyID3(filepath)
        LOGGER.debug(str(audio))

        tags = change_string_to_tags(filename)
        genres = "\\".join(self.get_tags(tags.get('artist')))
        year = str(time.gmtime()[0])
        tags.update({'genre': genres, 'date': year, 'album': year, 'albumartist': "VA", 'copyright': 'Jareczeg'})

        audio.update(tags)
        audio.save(v1=2)
        if cover:
            self.add_cover_art(filepath, cover)

    def add_cover_art(self, filepath, coverpath):
        """
        TBD
        :param filepath:
        :param coverpath:
        :return:
        """
        if not coverpath:
            return False
        print("Add cover")
        audio = ID3(filepath)
        with open(coverpath, 'rb') as albumart:
            audio['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=albumart.read()
            )
        audio.save()
        return True

    def main(self, folder_path="/home/jarek/Music/04"):
        """
        TBD
        :param folder_path:
        :return:
        """
        files_list = os.listdir(folder_path)
        for file in files_list:
            filename = os.path.splitext(file)[0]
            self.add_tags_to_file(filename, folder_path)

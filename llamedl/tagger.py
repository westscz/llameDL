"""
    llamedl.tagger.py
    ~~~~~~~~~~~~~~~~~~~
"""
import os
import time
import argparse
import musicbrainzngs
import requests
from tqdm import tqdm
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
    def __init__(self):
        self.whitelist_path = "../common/whitelist.cfg"
        self.whitelist = []
        self.cover_path = ""
        self.force = False
        self.path = ""
        self.__artist_data = {}

    def add_tags_to_file(self, filename, folder_path, cover=None, force=None):
        """

        :param filename:
        :param folder_path:
        :param cover:
        :param force:
        :return:
        """
        LOGGER.debug("Process %s", filename)
        filepath = os.path.join(folder_path, filename + '.mp3')
        audio = EasyID3(filepath)
        if audio.get('genre', False) and not force:
            return None
        tags = change_string_to_tags(filename)
        genres = "\\".join(self.get_tags(tags.get('artist')))
        year = str(time.gmtime()[0])
        tags.update({'genre': genres, 'date': year, 'album': year,
                     'albumartist': "VA", 'copyright': 'LlameDL'})
        audio.update(tags)
        audio.save(v1=2)
        if cover:
            self.add_cover_art(filepath, cover)

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
        tags_list = self.filter_tags(tag_list)
        LOGGER.info("%s %s", artist_name, str(tags_list))
        tags_list.sort()
        return tags_list

    @staticmethod
    def get_tags_from_musicbrainzgs(artist_name):
        """
        Get tags for artist_name from musicbrainzgs
        :param artist_name:
        :return:
        """
        try:
            result = musicbrainzngs.search_artists(artist_name)
            for artist_data in result.get('artist-list'):
                if artist_data.get('name').lower() == artist_name.lower():
                    return [tag.get('name').title() for tag in artist_data.get('tag-list', {})]
        except (HTTPError, musicbrainzngs.musicbrainz.ResponseError):
            pass
        except TypeError:
            return []
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
        return [tag.get('name').title() for tag in tags]

    def filter_tags(self, tags_list):
        """
        Filter tags_list with whitelist and/or blacklist
        :param tags_list:
        :return:
        """
        if self.whitelist:
            tags_list = self.filter_tags_with_whitelist(tags_list)
        return tags_list

    def filter_tags_with_whitelist(self, tags_list):
        """
        TBD            print(result.get('artist-count'))
        :param tags_list:
        :return:
        """
        return [tag for tag in tags_list if tag.lower() in self.whitelist]

    @staticmethod
    def add_cover_art(filepath, coverpath):
        """
        TBD
        :param filepath:
        :param coverpath:
        :return:
        """
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

    def main(self):
        """
        TBD
        :param folder_path:
        :return:
        """
        self.__create_args_parser().parse_args(namespace=self)
        self.load_filters()
        files_list = os.listdir(self.path)
        for file in tqdm(files_list):
            filename = os.path.splitext(file)[0]
            self.add_tags_to_file(filename, self.path, self.cover_path, self.force)

    @staticmethod
    def __create_args_parser():
        parser = argparse.ArgumentParser(prog="LlameTagger")
        parser.add_argument('path', help="Path to directory with mp3 files")
        parser.add_argument('-f', '--force', help="Force flag, add tags even if file contains tags")
        parser.add_argument('-c', '--cover_path', help="Path to album cover, if album cover should be added")
        parser.add_argument('-w', '--whitelist_path', help="Path to txt file with whitelisted tags")
        return parser

    def load_filters(self):
        if self.whitelist_path:
            with open(self.whitelist_path) as f:
                self.whitelist = f.read().splitlines()


if __name__ == '__main__':
    tagger = Tagger()
    tagger.main()

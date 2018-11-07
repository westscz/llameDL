"""
    llamedl.tagger.py
    ~~~~~~~~~~~~~~~~~~~
"""
import os
import time
import sys
import argparse

import requests
from tqdm import tqdm

from llamedl.tags.lastfmtags import LastFmTags
from llamedl.tags.musicbrainzgstags import MusicbrainzgsTags
from llamedl.utill import create_logger, change_string_to_tags
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC

LOGGER = create_logger("Tagger")


class Tagger:
    """
    # whitelist_sample = ["pop", "rock", "soul", "r&b", "trap rap", "electronic", "dubstep"]
    """

    def __init__(self):
        self.whitelist_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "whitelist.cfg")
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
        return MusicbrainzgsTags().get_tags(artist_name)

    @staticmethod
    def get_tags_from_last_fm(artist_name):
        """
        Get tags for artist_name from last_fm
        :param artist_name:
        :return:
        """
        return LastFmTags().get_tags(artist_name)

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
        self.parse_args(sys.argv[1:], self)
        self.load_filters()
        files_list = os.listdir(self.path)
        for file in tqdm(files_list):
            filename = os.path.splitext(file)[0]
            self.add_tags_to_file(filename, self.path, self.cover_path, self.force)

    @staticmethod
    def parse_args(args, namespace=None):
        parser = argparse.ArgumentParser(prog="LlameTagger")
        parser.add_argument('path',
                            help="Path to directory with mp3 files")
        parser.add_argument('-f', '--force',
                            help="Force flag, add tags even if file contains tags")
        parser.add_argument('-c', '--cover_path',
                            help="Path to album cover, if album cover should be added")
        parser.add_argument('-w', '--default_whitelist',
                            help="Use default whitelist, default=True")
        parser.add_argument('-p', '--whitelist_path',
                            help="Path to txt file with whitelisted tags")
        return parser.parse_args(args, namespace=namespace)

    def load_filters(self):
        if self.whitelist_path:
            with open(self.whitelist_path) as file:
                self.whitelist = file.read().splitlines()


def main():
    tagger = Tagger()
    tagger.main()


if __name__ == '__main__':
    main()

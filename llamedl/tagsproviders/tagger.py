"""
    llamedl.tagger.py
    ~~~~~~~~~~~~~~~~~~~
"""
import argparse
import os
import time

import fire
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3, ID3NoHeaderError
from tqdm import tqdm

from llamedl.tagsproviders.filetags import FileTags
from llamedl.tagsproviders.lastfmtags import LastFmTags
from llamedl.tagsproviders.musicbrainzngstags import MusicbrainzngsTags
from llamedl.utill import create_logger, change_string_to_tags

LOGGER = create_logger(__name__)


class Tagger:
    def __init__(self, download_directory, file_tags):
        self._file_tags = file_tags
        self.taggers_map = [LastFmTags(), MusicbrainzngsTags(), FileTags(file_tags)]
        self.whitelist_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "whitelist.cfg"
        )
        self.whitelist = []
        self.download_directory = download_directory

    def load_filters(self):
        if self.whitelist_path:
            with open(self.whitelist_path) as file:
                self.whitelist = file.read().splitlines()

    def add_tags_to_files(self, files_list):
        self.load_filters()
        tags_gen = tqdm(files_list, desc="Tagger start")
        for file in tags_gen:
            tags_gen.set_description(file)
            self.add_tags_to_file(self.download_directory, file)

    def add_tags_to_file(self, folder_path, filename, cover=None, force=None):
        """

        :param filename:
        :param folder_path:
        :param cover:
        :param force: If true, tags will be added even if they exist
        :return:
        """
        LOGGER.debug(f'Process "{filename}"')
        filepath = os.path.join(folder_path, filename + ".mp3")
        audio = self.get_id3_object(filepath)
        if audio.get("genre", False) and not force:
            return None
        tags = self.generate_new_id3_values(filename)
        audio.update(tags)
        audio.save(filepath, v1=2)
        # if cover:
        #     self.add_cover_art(filepath, cover)

    def get_id3_object(self, filepath):
        try:
            audio = EasyID3(filepath)
        except ID3NoHeaderError:
            audio = EasyID3()
        return audio

    def generate_new_id3_values(self, filename):
        tags = change_string_to_tags(filename)
        genres = self.get_tags(tags.get("artist"))
        year = str(time.gmtime()[0])
        tags.update(
            {
                "genre": genres,
                "date": year,
                "album": year,
                "albumartist": "VA",
                "copyright": "LlameDL",
            }
        )
        return tags

    def get_tags_from_tags_providers(self, artist):
        tags = []
        for tagger in self.taggers_map:
            tags.extend(tagger.get_tags(artist))
        if not tags:
            LOGGER.debug(
                f'Tags for "{artist}" are not available. Find more informations in help'
            )
        return list(set(tags))

    def get_tags(self, artist_name):
        """Get tagsproviders for artist_name from last.fm and musicbrainzgs.

        `\\` separator is used by most of audio players

        :param artist_name:
        :return:
        """
        if artist_name == "Unknown":
            return []

        tag_list = self.get_tags_from_tags_providers(artist_name)
        tags_list = self.filter_tags(tag_list)
        LOGGER.debug("%s %s", artist_name, str(tags_list))
        tags_list.sort()
        return "\\".join(tags_list)

    def filter_tags(self, tags_list):
        """Filter tags_list with whitelist and/or blacklist.

        :param tags_list:
        :return:
        """
        return [tag for tag in tags_list if tag.lower() in self.whitelist]

    @staticmethod
    def add_cover_art(filepath, coverpath):
        """TBD.

        :param filepath:
        :param coverpath:
        :return:
        """
        audio = ID3(filepath)
        with open(coverpath, "rb") as albumart:
            audio["APIC"] = APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,
                desc="Cover",
                data=albumart.read(),
            )
        audio.save()
        return True


class TaggerFire:
    def __init__(self):
        pass

    def main(self):
        """TBD.

        :param folder_path:
        :return:
        """
        # self.parse_args(sys.argv[1:], self)
        # self.load_filters()
        # files_list = os.listdir(self.path)
        # for file in tqdm(files_list):
        #     filename = os.path.splitext(file)[0]
        #     self.add_tags_to_file(filename, self.path, self.cover_path, self.force)

    @staticmethod
    def parse_args(args, namespace=None):
        parser = argparse.ArgumentParser(prog="LlameTagger")
        # parser.add_argument('path',
        #                     help='Path to directory with mp3 files')
        # parser.add_argument('-f', '--force',
        #                     help='Force flag, add tagsproviders even if file contains tagsproviders')
        # parser.add_argument('-c', '--cover_path',
        #                     help='Path to album cover, if album cover should be added')
        # parser.add_argument('-w', '--default_whitelist',
        #                     help='Use default whitelist, default=True')
        # parser.add_argument('-p', '--whitelist_path',
        #                     help='Path to txt file with whitelisted tagsproviders')
        # return parser.parse_args(args, namespace=namespace)


def tagger_cli():
    fire.Fire(TaggerFire)


if __name__ == "__main__":
    tagger_cli()

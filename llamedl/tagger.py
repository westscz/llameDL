"""

"""
import musicbrainzngs
import requests
from llamedl.utill import create_logger, change_string_to_tags
from urllib.error import HTTPError
import time
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3

LOGGER = create_logger("Tagger")


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
        musicbrainzngs.set_useragent("LLameDL", "0.1", "http://github.com/music")

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
        tag_list = self.get_tags_from_last_fm(artist_name)
        tag_list += self.get_tags_from_musicbrainzgs(artist_name)
        tags_list = set([tag.get('name').title() for tag in tag_list])
        if self.whitelist:
            tags_list = self.filter_tags_with_whitelist(tags_list)
        if self.blacklist:
            tags_list = self.filter_tags_with_blacklist(tags_list)
        LOGGER.debug(tags_list)
        return tags_list

    def get_tags_from_musicbrainzgs(self, artist_name):
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

    def get_tags_from_last_fm(self, artist_name):
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

    def add_tags_to_file(self, filename, folder_path):
        """

        :param filename:
        :param folder_path:
        :return:
        """
        LOGGER.info("Adding tags to {}".format(filename))
        filepath = "{}/{}.mp3".format(folder_path, filename)

        audio = EasyID3(filepath)
        LOGGER.debug(str(audio))

        tags = change_string_to_tags(filename)
        genres = "\\".join(self.get_tags(tags.get('artist')))
        year = str(time.gmtime()[0])
        tags.update({'genre': genres, 'date': year, 'album': year, 'albumartist': "VA", 'copyright': 'Jareczeg'})

        audio.update(tags)
        audio.save()
        self.__update_tag_type(filepath)

    def __update_tag_type(self, file_path):
        """

        :param filepath:
        :return:
        """
        audio = ID3(file_path, v2_version=3)
        audio.save(v2_version=3)

    # def add_cover_art(self, filepath):
    #     audio = ID3(filepath, v2_version=3)
    #     content = None
    #     with open(self.album_art, 'rb') as albumart:
    #         content = albumart.read()
    #     audio.add(APIC(encoding=3, mime="image/jpeg", type=3, desc=u"Cover", data=content))
    #     audio.save()

#
#
# if __name__ == '__main__':
#     x = Tagger()
#     BAND_LIST = ['Blade Rain', 'Red Hot Chili Peppers', 'Skrillex', 'asdsgfdasdfg',
#                  'Desiigner', "Taco Hemingway", 'Diplo and Friends', 'Razihel',
#                  'Bob Acri', 'Mrozu', 'Bracia Figo Fagot', 'Zbigniew Wodecki']
#
#     lfm = Tagger()
#     for x in BAND_LIST:
#         result = lfm.get_tags(x)
#         print(x, result)

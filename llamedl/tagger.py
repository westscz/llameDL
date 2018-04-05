"""

"""
import musicbrainzngs
import requests
from common.utill import create_logger

LOGGER = create_logger("LastFM")


class Tagger:
    """
    # whitelist_sample = ["pop", "rock", "soul", "r&b", "trap rap", "electronic", "dubstep"]
    # blacklist_sample = ['owsla', 'seen live']
    """
    def __init__(self, whitelist=None, blacklist=None):
        self.whitelist = [] if whitelist is None else whitelist
        self.blacklist = [] if blacklist is None else blacklist
        self.__artist_data = {}
        musicbrainzngs.set_useragent("LLameDL", "0.1", "http://github.com/music")

    def get_tags(self, artist_name):
        """
        Get tags for artist_name from last.fm and musicbrainzgs
        :param artist_name:
        :return:
        """
        tag_list = self.get_tags_from_last_fm(artist_name)
        tag_list += self.get_tags_from_musicbrainzgs(artist_name)
        tags_list = set([tag.get('name').lower() for tag in tag_list])
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
        result = musicbrainzngs.search_artists(artist_name)
        if result.get('artist-count', 0):
            for artist_data in result.get('artist-list'):
                if artist_data.get('name').lower() == artist_name.lower():
                    LOGGER.debug("MB - {}".format(artist_data.get('tag-list')))
                    return artist_data.get('tag-list', {})
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
        LOGGER.debug("LFM - {}".format(tags))
        return tags

    def filter_tags_with_whitelist(self, tags_list):
        """
        TBD
        :param tags_list:
        :return:
        """
        return [tag for tag in tags_list if tag in self.whitelist]

    def filter_tags_with_blacklist(self, tags_list):
        """
        TBD
        :param tags_list:
        :return:
        """
        return [tag for tag in tags_list if tag not in self.blacklist]
#
#
# if __name__ == '__main__':
#     x = Tagger()
#     BAND_LIST = ['Blade Rain', 'Red Hot Chili Peppers', 'Skrillex', 'asdsgfdasdfg',
#                  'Desiigner', "Taco Hemingway", 'Diplo and Friends', 'Razihel',
#                  'Bob Acri', 'Mrozu', 'Bracia Figo Fagot', 'Zbigniew Wodecki',
#                  'Marta Gałuszewska']
#
#     lfm = Tagger()
#     for x in BAND_LIST:
#         result = lfm.get_tags(x)
#         print(x, result)

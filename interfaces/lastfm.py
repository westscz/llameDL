import urllib3
from lxml import html
from common.utill import create_logger
import musicbrainzngs
Logger = create_logger("LastFM")

whitelist = ["pop", "rock", "soul", "r&b", "trap rap", "electronic", "dubstep"]

class ILastFM():
    def __init__(self):
        # self.http = urllib3.PoolManager()
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        musicbrainzngs.set_useragent("LLameDL", "0.1", "http://github.com/music")

    def get_artist_data(self, artist_name):
        result = musicbrainzngs.search_artists(artist_name)
        if result.get('artist-count', 0):
            for artist_data in result.get('artist-list'):
                if artist_data['name']==artist_name:
                    Logger.debug(artist_data)
                    return artist_data if artist_data else {}
        return {}

    def get_tags_for_artist(self, artist_name):
        artist_data = self.get_artist_data(artist_name)
        tags_list = artist_data.get('tag-list', [])
        if not tags_list:
            self.add_tag(artist_data.get('id', None))
        w=[tag.get('name') for tag in tags_list]
        Logger.debug(w)
        return self.whitelist_tags(w)

    def whitelist_tags(self, tags_list):
        return [tag for tag in tags_list if tag in whitelist]

    def add_tag(self, artist_id):
        if not artist_id:
            Logger.info("Artist is not visible in Music Brainz Database")
            Logger.info("https://musicbrainz.org/artist/create")
        else:
            Logger.info("Artist have not any tags in Music Brainz Database")
            Logger.info("https://musicbrainz.org/artist/{artist_id}".format(artist_id=artist_id))


if __name__ == '__main__':
    band_list = ['Blade Rain', 'Red Hot Chili Peppers', 'Skrillex', 'asdsgfdasdfg', 'Desiigner',
     'Diplo and Friends', 'Razihel', 'Bob Acri', 'Mrozu', 'Bracia Figo Fagot', 'Zbigniew Wodecki', 'Marta Gałuszewska']


    lfm = ILastFM()
    for x in band_list:
        result = lfm.get_tags_for_artist(x)
        print(x, result)

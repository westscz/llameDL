import urllib3
from lxml import html
from common.utill import create_logger
import musicbrainzngs
Logger = create_logger("LastFM")


class ILastFM():
    def __init__(self):
        # self.http = urllib3.PoolManager()
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        musicbrainzngs.set_useragent("LLameDL", "0.1", "http://github.com/music")

    # def remove_pl_chars(self, text):
    #     s = list(text)
    #     pl_dict = {261: 'a', 260: 'A', 263: 'c', 262: 'C', 281: 'e', 280: 'E', 322: 'l', 321: 'L', 243: 'o', 211: 'O',
    #                347: 's', 346: 'S', 380: 'z', 379: 'Z', 378: 'z', 377: 'Z', 235: 'e'}
    #     for idx, val in enumerate(s):
    #         char_ord = ord(val)
    #         if char_ord in pl_dict.keys():
    #             s[idx] = pl_dict[char_ord]
    #         elif char_ord > 600:
    #             s[idx] = "#"
    #     return "".join(s)

    # def get_tags_for_artist(self, artist):
    #     if artist == "Unknown":
    #         Logger.info(artist + ' nie posiada jeszcze tagow, dodaj je samodzielnie')
    #         return []
    #
    #     artist_mod = self.remove_pl_chars(artist)
    #     url = 'http://www.last.fm/pl/music/' + artist_mod.replace(' ', '+')
    #
    #     r = self.http.request('GET', url)
    #     html_content = r.data
    #     tree = html.fromstring(html_content)
    #
    #     x = tree.xpath('//section[@class="tag-section"]/ul//a')
    #     tags = []
    #     for f in x:
    #         tags.append(f.text.title())
    #     if tags:
    #         Logger.info(artist + ' - ' + ', '.join(tags))
    #         return tags
    #     else:
    #         Logger.info(artist + ' nie posiada jeszcze tagow, dodaj je samodzielnie: ' + url + '/+tags')
    #         return []

    def get_artist_data(self, artist_name):
        result = musicbrainzngs.search_artists(artist_name)
        if result.get('artist-count', 0):
            for artist_data in result.get('artist-list'):
                if artist_data['name']==artist_name:
                    print(artist_data)
                    return artist_data if artist_data else {}
        return {}

    def get_tags_for_artist(self, artist_name):
        artist_data = self.get_artist_data(artist_name)
        tags_list = artist_data.get('tag-list', [])
        return [tag.get('name') for tag in tags_list]

    def add_tag(self):
        pass
        #https://musicbrainz.org/artist/{artist_id}/tags/upvote?tags={tag%20list}
        #this can help to add tags


if __name__ == '__main__':
    band_list = ['Blade Rain', 'Red Hot Chili Peppers', 'Skrillex', 'asdsgfdasdfg', 'Desiigner',
     'Diplo and Friends', 'Razihel', 'Bob Acri', 'Mrozu', 'Bracia Figo Fagot', 'Zbigniew Wodecki', 'Marta Gałuszewska']


    lfm = ILastFM()
    for x in band_list:
        print(x)
        result = lfm.get_tags_for_artist(x)
        print(result)

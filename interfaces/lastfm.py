import urllib3
from lxml import html
from common.utill import create_logger

Logger = create_logger("LastFM")


class ILastFM():
    def __init__(self):
        self.http = urllib3.PoolManager()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def remove_pl_chars(self, text):
        s = list(text)
        pl_dict = {261: 'a', 260: 'A', 263: 'c', 262: 'C', 281: 'e', 280: 'E', 322: 'l', 321: 'L', 243: 'o', 211: 'O',
                   347: 's', 346: 'S', 380: 'z', 379: 'Z', 378: 'z', 377: 'Z', 235: 'e'}
        for idx, val in enumerate(s):
            char_ord = ord(val)
            if char_ord in pl_dict.keys():
                s[idx] = pl_dict[char_ord]
            elif char_ord > 600:
                s[idx] = "#"
        return "".join(s)

    def get_tags_for_artist(self, artist):
        if artist == "Unknown":
            Logger.info(artist + ' nie posiada jeszcze tagow, dodaj je samodzielnie')
            return []

        artist_mod = self.remove_pl_chars(artist)
        url = 'http://www.last.fm/pl/music/' + artist_mod.replace(' ', '+')

        r = self.http.request('GET', url)
        html_content = r.data
        tree = html.fromstring(html_content)

        x = tree.xpath('//section[@class="tag-section"]/ul//a')
        tags = []
        for f in x:
            tags.append(f.text.title())
        if tags:
            Logger.info(artist + ' - ' + ', '.join(tags))
            return tags
        else:
            Logger.info(artist + ' nie posiada jeszcze tagow, dodaj je samodzielnie: ' + url + '/+tags')
            return []


if __name__ == '__main__':
    lfm = ILastFM()
    lfm.get_tags_for_artist('Blade Rain')
    lfm.get_tags_for_artist('Red Hot Chili Peppers')
    lfm.get_tags_for_artist('Skrillex')
    lfm.get_tags_for_artist('asdsgfdasdfg')
    lfm.get_tags_for_artist('Desiigner')
    lfm.get_tags_for_artist('Diplo and Friends')
    lfm.get_tags_for_artist('Razihel')
    lfm.get_tags_for_artist('Bob Acri')
    lfm.get_tags_for_artist('Mrozu')
    lfm.get_tags_for_artist('Bracia Figo Fagot')
    lfm.get_tags_for_artist('')

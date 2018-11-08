from urllib.error import HTTPError

import musicbrainzngs
from llamedl.tags.basetags import BaseTags

musicbrainzngs.set_useragent('LLameDL', '0.1', 'http://github.com/music')


class MusicbrainzgsTags(BaseTags):
    def get_tags(self, artist_name):
        try:
            result = musicbrainzngs.search_artists(artist_name)
            for artist_data in result.get('artist-list'):
                if artist_data.get('name').lower() == artist_name.lower():
                    return [tag.get('name').title() for tag in artist_data.get('tag-list', {})]
        except (HTTPError, musicbrainzngs.musicbrainz.ResponseError, TypeError) as e:
            print(e)
            return []
        return []

from urllib.error import HTTPError

import musicbrainzngs

from llamedl.tagsproviders.basetags import BaseTags

musicbrainzngs.set_useragent('LLameDL', '0.1', 'http://github.com/music')


class MusicbrainzngsTags(BaseTags):
    def get_tags(self, artist_name) -> list:
        result = self._retrieve_data(artist_name)
        for artist_data in result.get('artist-list', []):
            if artist_data.get('name').lower() == artist_name.lower():
                return [tag.get('name').title() for tag in artist_data.get('tag-list', {})]
        else:
            return []

    def _retrieve_data(self, artist_name) -> dict:
        try:
            result = musicbrainzngs.search_artists(artist_name)
            return result
        except (HTTPError, musicbrainzngs.musicbrainz.ResponseError, TypeError) as e:
            print(e)
            return {}

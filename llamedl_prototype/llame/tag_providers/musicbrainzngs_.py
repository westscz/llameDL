import musicbrainzngs

from .base import BaseTagProvider

musicbrainzngs.set_useragent("LLameDL", "0.1", "http://github.com/music")


class MusicBrainzgsTagProvider(BaseTagProvider):
    def _get_tags_for(self, artist) -> list:
        result = self._retrieve_data(artist)
        if not result:
            return []
        artist_data = self._find_artist_data(result.get("artist-list", []), artist)
        return self._get_tags_from_data(artist_data)

    def _get_tags_from_data(self, artist_data):
        return [tag.get("name").title() for tag in artist_data.get("tag-list", {})]

    def _find_artist_data(self, artists_data, artist):
        for artist_data in artists_data:
            if artist_data.get("name").lower() == artist.lower():
                return artist_data

    def _retrieve_data(self, artist) -> dict:
        try:
            result = musicbrainzngs.search_artists(artist)
        except (HTTPError, musicbrainzngs.musicbrainz.ResponseError, TypeError) as e:
            result = {}
        return result


if __name__ == "__main__":
    l = MusicBrainzgsTagProvider()
    print(l.get_tags_for("Taylor Swift"))

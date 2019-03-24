import requests

from llamedl.tagsproviders.basetags import BaseTags


class LastFmTags(BaseTags):
    def __init__(self):
        self.api_key = 'a7b8b15b54a347be1736dd0f77c7d048'

    def get_tags(self, artist_name):
        artist = artist_name.replace(' ', '%20')
        url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getInfo&artist={artist}&user=RJ&api_key={self.api_key}&format=json'
        response = requests.get(url)
        if response.json().get('error'):
            return []
        tags = response.json().get('artist').get('tags').get('tag', [])
        return [tag.get('name').title() for tag in tags]


if __name__ == '__main__':
    o = LastFmTags()
    o.get_tags("Infected Mushroom")

import requests

from llamedl.tags.basetags import BaseTags


class LastFmTags(BaseTags):
    def get_tags(self, artist_name):
        artist_name = artist_name.replace(' ', '%20')
        api_key = 'a7b8b15b54a347be1736dd0f77c7d048'
        response = requests.get(
            'http://ws.audioscrobbler.com/2.0/?'
            'method=artist.getInfo&artist={artist}&user=RJ&'
            'api_key={api_key}&format=json'.format(
                artist=artist_name, api_key=api_key))
        if response.json().get('error'):
            return []
        tags = response.json().get('artist').get('tags').get('tag', [])
        return [tag.get('name').title() for tag in tags]

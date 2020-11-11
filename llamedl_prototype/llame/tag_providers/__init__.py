from .file_tag import FileTagProvider
from .lastfm import LastFMProvider
from .musicbrainzngs_ import MusicBrainzgsTagProvider


def get_tag_providers():
    return [FileTagProvider("")]

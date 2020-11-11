from functools import cached_property

from .base import BaseTagProvider


class FileTagProvider(BaseTagProvider):
    def __init__(self, path):
        self._path = path

    @cached_property
    def tags(self):
        return {}

    def get_tags_for(self, artist):
        return self.tags.get(artist, [])

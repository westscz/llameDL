from .base import BaseTagProvider


class MemoryTagsProvider(BaseTagProvider):
    def __init__(self, tags):
        self.tags = tags if tags else {}

    def _get_tags_for(artist):
        return self.tags.get(artist, [])

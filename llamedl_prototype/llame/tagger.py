class Tagger:
    def __init__(self, tag_providers):
        self.tag_providers = tag_providers

    def tag_files(self, path, additional_tags):
        """Tag file with additional_tags"""

    def _get_artist(self, path) -> str:
        """Return artist name from path filename"""

    def _get_tags_for_artist(self, artist) -> []:
        return [p.get_tags_for(artist) for p in self.tag_providers]

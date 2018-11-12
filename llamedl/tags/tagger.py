import os


class Tagger:
    def __init__(self, taggers, whitelist_flag=True):
        """taggers: List[BaseTags]"""
        self.taggers = taggers
        self.whitelist_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'whitelist.cfg')
        self.whitelist_flag = whitelist_flag
        self._whitelist = None

    def get_tags_for_artist(self, artist):
        tags = self.get_tags_from_tags_providers(artist)
        if self.whitelist_flag:
            return self.filter_tags(tags)
        else:
            return tags

    def get_tags_from_tags_providers(self, artist):
        tags = []
        for tagger in self.taggers:
            tags.extend(tagger.get_tags(artist))
        if not tags:
            print(f'Tags for "{artist}" are not available. Find more informations in help')
        return list(set(tags))

    def filter_tags(self, tags_list):
        filtered_tags = [tag for tag in tags_list if tag.lower() in self.whitelist]
        return filtered_tags

    @property
    def whitelist(self):
        if not self._whitelist:
            self._whitelist = self.load_whitelist()
        return self._whitelist

    def load_whitelist(self):
        with open(self.whitelist_path) as file:
            return file.read().splitlines()

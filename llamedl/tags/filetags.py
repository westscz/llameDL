from llamedl.tags.basetags import BaseTags
import yaml


class FileClass(BaseTags):
    def __init__(self, tags_file):
        """
        Add support for yaml file where key is artist, and value is tags list
        :param tags_file:
        """
        self.tags_file = tags_file
        self._file_content = None

    @property
    def tags_file_content(self):
        if not self._file_content:
            with open(self.tags_file, 'r') as stream:
                try:
                    self._file_content = yaml.load(stream)
                except yaml.YAMLError as e:
                    print(e)
        return self._file_content

    def get_tags(self, artist_name):
        return self.tags_file_content.get(artist_name, [])

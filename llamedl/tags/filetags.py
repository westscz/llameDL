from llamedl.tags.basetags import BaseTags
import yaml


class FileTags(BaseTags):
    def __init__(self, tags_file_path):
        """
        Add support for yaml file where key is artist, and value is tags list
        :param tags_file_path:
        """
        self.tags_file_path = tags_file_path
        self._file_content = {}

    @property
    def file_content(self):
        if not self._file_content:
            with open(self.tags_file_path, 'r') as stream:
                try:
                    self._file_content = yaml.load(stream)
                except yaml.YAMLError as e:
                    print(e)
        return self._file_content

    def get_tags(self, artist_name):
        return self.file_content.get(artist_name, [])

import yaml

from llamedl.tagsproviders.basetags import BaseTags


class FileTags(BaseTags):
    def __init__(self, tags_file_path):
        """Add support for yaml file where key is artist, and value is tagsproviders
        list.

        :param tags_file_path:
        """
        self.tags_file_path = tags_file_path
        self._file_content = {}

    @property
    def file_content(self) -> dict:
        if not self._file_content and self.tags_file_path:
            self._file_content = self._read_content_from_file()
        return self._file_content

    def _read_content_from_file(self) -> dict:
        with open(self.tags_file_path, "r") as stream:
            try:
                file_content = yaml.load(stream)
            except yaml.YAMLError as e:
                print(e)
                file_content = {}
        return file_content

    def get_tags(self, artist_name) -> list:
        return self.file_content.get(artist_name, [])

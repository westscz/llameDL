from os import listdir

import fire

from llamedl.tagsproviders.tagger import Tagger


class LlameTaggerFire:
    def __init__(self, tags_file=""):
        """
        :param tags_file: Path to YAML file with artist:tags variables
        :param download_directory: Directory where audio files will be saved
        """
        self._tags_file_path = tags_file
        self._tag_engine = None

    def directory(self, directory):
        """
        Tag all mp3 files in directory

        :param directory: Path to directory with mp3 files
        :return:
        """
        self._tag_engine = Tagger(directory, self._tags_file_path)

        files_list = listdir(directory)
        self._tag_engine.add_tags_to_files(files_list)


def tagger_cli():
    fire.Fire(LlameTaggerFire)


if __name__ == "__main__":
    tagger_cli()

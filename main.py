from interfaces.chrome import IChrome
from interfaces.youtube import IYouTube
from common.tageditor import TagEditor
from common.utill import create_logger

Logger = create_logger("Downloader")

import os

if __name__ == '__main__':
    env_home_path = os.getenv("HOME")
    music_folder_path = "{}/Music".format(env_home_path)

    c = IChrome()
    yt = IYouTube(music_folder_path)
    te = TagEditor(music_folder_path)

    Logger.info("{space}Start{space}".format(space='*' * 10))
    url_list = c.get_url_list()
    Logger.info("{space}Download{space}".format(space='*' * 10))
    for url in url_list:
        name = yt.download_mp3(url)
        if name:
            te.edit_tags(name)

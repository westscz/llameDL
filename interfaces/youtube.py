#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
xd
"""
from __future__ import unicode_literals
from common.utill import change_string_to_tags, remove_descriptions, \
    create_logger
import youtube_dl

LOGGER = create_logger("YouTube")





def create_file_name(title):
    """
    :param title:
    :return:
    """
    result_title = remove_descriptions(title)
    result_title = change_string_to_tags(result_title)
    return " - ".join([result_title['artist'],
                       result_title['title']]).rstrip(" ")


class IYouTube(object):
    """
    omaga
    """
    def __init__(self, music_folder_path):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': r"XD.%(ext)s",
            'logger': MyLogger()
        }
        self.music_folder_path = music_folder_path

    def download_mp3(self, video_url):
        """

        :param video_url:
        :return:
        """
        try:
            filename = self.get_url_info(video_url)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                out__tmpl = r"{}/{}.%(ext)s".format(
                    self.music_folder_path, filename)
                LOGGER.debug(out__tmpl)
                self.ydl_opts['outtmpl'] = out__tmpl
                ydl.params.update(self.ydl_opts)
                if not ydl.download([video_url]):
                    LOGGER.info('"{}" Downloaded correctly!'.format(filename))
            return filename
        except youtube_dl.utils.DownloadError:
            return ""

    def get_url_info(self, video_url=None):
        """

        :param video_url:
        :return:
        """
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            return create_file_name(info_dict['title'])

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from common.utill import change_string_to_tags, remove_descriptions, create_logger
import youtube_dl

Logger = create_logger("YouTube")


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class IYouTube(object):
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
        try:
            filename = self.get_url_info(video_url)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                out__tmpl = r"{}/{}.%(ext)s".format(self.music_folder_path, filename)
                Logger.debug(out__tmpl)
                self.ydl_opts['outtmpl'] = out__tmpl
                ydl.params.update(self.ydl_opts)
                if not ydl.download([video_url]):
                    Logger.info('"{}" Downloaded correctly!'.format(filename))
            return filename
        except youtube_dl.utils.DownloadError:
            return ""

    def get_url_info(self, video_url=None):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            return self.create_file_name(info_dict['title'])

    def create_file_name(self, title):
        result_title = remove_descriptions(title)
        result_title = change_string_to_tags(result_title)
        return " - ".join([result_title['artist'], result_title['title']]).rstrip(" ")

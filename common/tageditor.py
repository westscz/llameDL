#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from common.utill import create_logger
from interfaces.lastfm import ILastFM

Logger = create_logger("Tag Editor")


class TagEditor(object):
    def __init__(self, music_folder_path, album_art="folder.jpg"):
        self.album_art = album_art
        self.music_folder_path = music_folder_path

    def edit_tags(self, filename="Martin Garrix & Dua Lipa - Scared To Be Lonely "):
        Logger.info("Adding tags to {}".format(filename))
        filepath = "{}/{}.mp3".format(self.music_folder_path, filename)
        audio = EasyID3(filepath)
        Logger.debug(str(audio))
        clfm = ILastFM()
        try:
            artist, title = filename.split(" - ", 1)
        except:
            artist, title = filename.split(" – ", 1)
        genres = (clfm.get_tags_for_artist(artist))
        year = str(time.gmtime()[0])

        tags = {'artist': artist, 'title': title, 'genre': genres,
                'date': year, 'album': year, 'albumartist': "VA",
                'copyright': 'Jareczeg'}

        audio.update(tags)
        audio.save()
        self.update_tag_type(filepath)
        # self.add_cover_art(filepath)

    def update_tag_type(self, filepath):
        audio = ID3(filepath, v2_version=3)
        audio.save(v2_version=3)

    def add_cover_art(self, filepath):
        audio = ID3(filepath, v2_version=3)
        content = None
        with open(self.album_art, 'rb') as albumart:
            content = albumart.read()
        audio.add(APIC(encoding=3, mime="image/jpeg", type=3, desc=u"Cover", data=content))
        audio.save()

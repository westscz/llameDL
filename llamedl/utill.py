# !/usr/bin/python
# -*- coding: utf-8 -*-

import re
import logging


def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def create_filename(title):
    """
    :param title:
    :return:
    """
    result_title = remove_descriptions(title)
    result_title = change_string_to_tags(result_title)
    return " - ".join([result_title['artist'], result_title['title']]).rstrip(" ")


def remove_descriptions(filename):
    reg = r"[\[\(][^\[\(]*(oficjal|official|lyric|radio|video|audio|http|pl|hd)[^\[\(]*[\]\)]"
    while re.search(reg, filename, re.IGNORECASE):
        result = re.search(reg, filename, re.IGNORECASE)
        filename = filename.replace(result.group(), "")
    return filename.rstrip(" ")


def change_string_to_tags(string):
    string = string.replace("/", "")
    reg = r"(?P<artist>.*) [--–] (?P<title>.*)"
    result = re.search(reg, string)
    if result:
        artist, title = result.groups()
        return {'artist': capitalize_first_char(artist), 'title': capitalize_first_char(title)}
    else:
        return {'artist': 'Unknown', 'title': capitalize_first_char(string)}


def capitalize_first_char(string):
    return string[:1].upper()+string[1:]


class YTLogger:
    """
    Simple logger for IYouTube purpose
    """
    def debug(self, msg):
        """

        :param msg:
        :return:
        """
        pass

    def warning(self, msg):
        """

        :param msg:
        :return:
        """
        pass

    def error(self, msg):
        """

        :param msg:
        :return:
        """
        pass

# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
    llamedl.utill.py
    ~~~~~~~~~~~~~~~~~~~
"""
import logging
import re


def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(message)s (%(levelname)s)")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler = logging.FileHandler("llame.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def create_filename(string):
    """Get string and return fixed string.

    String should be in format 'artist - title'
    :param string:
    :return:
    """
    result_title = remove_descriptions(string)
    result_title = change_string_to_tags(result_title)
    return " - ".join([result_title["artist"], result_title["title"]]).rstrip(" ")


def remove_descriptions(string):
    """Get string and remove all regex matches.

    :param string:
    :return:
    """
    reg = r"[\[\(][^\[\(]*(prod|live|oficjal|free|hq|official|lyric|radio|video|audio|http|pl|hd|nowo)[^\[\(]*[\]\)]"
    while re.search(reg, string, re.IGNORECASE):
        result = re.search(reg, string, re.IGNORECASE)
        string = string.replace(result.group(), "")
    return string.rstrip(" ")


def change_string_to_tags(string):
    """
    Get string in format 'artist - title' and returns dictionary with 'artist' and 'title' as keys
    :param string:
    :return:
    """
    string = string.replace("/", " ").replace('"', "")
    reg = r"(?P<artist>.*) [---—–] (?P<title>.*)"
    result = re.search(reg, string)
    if result:
        artist, title = result.groups()
        return {
            "artist": capitalize_first_char(artist),
            "title": capitalize_first_char(title).title(),
        }
    return {"artist": "Unknown", "title": capitalize_first_char(string)}


def capitalize_first_char(string):
    """Get string and capitalize first char.

    :param string:
    :return:
    """
    return string[:1].upper() + string[1:]


class YTLogger:
    """Simple logger for IYouTube purpose."""

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

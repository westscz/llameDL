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


def remove_descriptions(filename):
    reg = r"[\[\(].*(ficjal|fficial|yric|adio|ideo|udio|rod).*[\]\)]"
    while re.search(reg, filename, re.IGNORECASE):
        X = re.search(reg, filename, re.IGNORECASE)
        filename = filename.replace(X.group(), "")
    return filename


def change_string_to_tags(string):
    reg = r"(?P<artist>.*) [-–] (?P<title>.*)"
    result = re.search(reg, string)
    if result:
        result = result.groupdict()
        return {'artist': result['artist'], 'title': result['title']}
    else:
        return {'artist': 'Unknown', 'title': string}

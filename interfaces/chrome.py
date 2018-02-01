#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from common.utill import create_logger

Logger = create_logger("Chrome")


class IChrome(object):
    def __init__(self, bookmark_name="M", bookmark_path=None):
        self.bookmark_name = bookmark_name
        if bookmark_path:
            self.bookmark_path = bookmark_path
        else:
            env_home_path = os.getenv("HOME")
            self.bookmark_path = "{}/.config/chromium/Default/Bookmarks".format(env_home_path)
        self.url_list = list()

    def get_url_list(self):
        with open(self.bookmark_path) as json_data:
            d = json.load(json_data)
            root = self.check_if_bookmark_exist(d)
            for kid in root:
                if "youtube" in kid["url"]:
                    self.url_list.append(kid["url"])
        Logger.info("I found {} urls".format(len(self.url_list)))
        return self.url_list

    def verify_yt_urls(self, urls_list):
        # TODO: Verify if url is not a playlist, or deleted video
        return True

    def check_if_bookmark_exist(self, json):
        for bookmark in json["roots"]["bookmark_bar"]["children"]:
            if bookmark["name"] == self.bookmark_name:
                print(bookmark["children"])
                return bookmark["children"]
        else:
            return None

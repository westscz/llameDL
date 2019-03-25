import json
import tempfile

import yaml


def create_chrome_bookmarks_file(data):
    file = tempfile.NamedTemporaryFile(mode="w", delete=False)
    with file as outfile:
        json.dump(data, outfile)
    return file.name


def create_netscape_bookmarks_file(data):
    file = tempfile.NamedTemporaryFile(mode="w", delete=False)
    with file as outfile:
        outfile.write(data)
    return file.name


def create_tags_file(data):
    file = tempfile.NamedTemporaryFile(mode="w", delete=False)
    with file as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
    return file.name

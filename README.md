# ![llameDL logo](logo.png) llameDL 
[![Build Status](https://travis-ci.org/westscz/llameDL.svg?branch=master)](https://travis-ci.org/westscz/llameDL)
![Python Version](https://img.shields.io/badge/python-3.5%2B-blue.svg)
[![Code Coverage](https://scrutinizer-ci.com/g/westscz/llameDL/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/westscz/llameDL/?branch=master)
[![Requirements Status](https://requires.io/github/westscz/llameDL/requirements.svg?branch=master)](https://requires.io/github/westscz/llameDL/requirements/?branch=master)
[![Scrutinize Status](https://scrutinizer-ci.com/g/westscz/llameDL/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/westscz/llameDL/)


**UNDER CONSTRUCTION**

YouTube to MP3 converter with adding tags

## Project structure

    ├── CHANGES.md
    ├── llamedl
    │   ├── browser
    │   │   ├── basebrowser.py
    │   │   ├── chromebrowser.py
    │   │   └── urlprovider.py
    │   ├── downloaders
    │   │   ├── basedownloader.py
    │   │   └── youtubedownloader.py
    │   ├── llame.py
    │   ├── __main__.py
    │   ├── tagger.py
    │   ├── tags
    │   │   ├── basetags.py
    │   │   ├── filetags.py
    │   │   ├── lastfmtags.py
    │   │   ├── musicbrainzgstags.py
    │   │   └── tagger.py
    │   ├── utill.py
    │   └── whitelist.cfg
    ├── logo.png
    ├── MANIFEST.in
    ├── README.md
    ├── requirements-dev.txt
    ├── requirements.txt
    ├── setup.cfg
    ├── setup.py
    └── tests
        ├── __init__.py
        ├── providers
        │   └── test_url_provider.py
        ├── tags
        │   └── test_file_tags.py
        ├── test_chromebrowser.py
        ├── test_iyoutube.py
        ├── test_tagger.py
        └── test_utill.py


## Install
- pip install -r requirements.txt
- ffprobe or avprobe


## Use
llameDL is provided with CLI, installed using entry-points in setup.py

- llamedl
- llametagger

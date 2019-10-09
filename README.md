# llameDL

<p align="center"><img src="/media/logo.png"/></p>
<p align="center">YouTube to MP3 converter with adding tags</p>

![LlameDL Version](https://img.shields.io/badge/llameDL-0.2.0-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)
[![Build Status](https://travis-ci.org/westscz/llameDL.svg?branch=master)](https://travis-ci.org/westscz/llameDL)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Code Coverage](https://scrutinizer-ci.com/g/westscz/llameDL/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/westscz/llameDL/?branch=master)
[![Requirements Status](https://requires.io/github/westscz/llameDL/requirements.svg?branch=master)](https://requires.io/github/westscz/llameDL/requirements/?branch=master)
[![Scrutinize Status](https://scrutinizer-ci.com/g/westscz/llameDL/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/westscz/llameDL/)
[![GitlabCI-pipe](https://gitlab.com/piszczala/llameDL/badges/master/pipeline.svg)](https://gitlab.com/piszczala/llameDL)
[![GitlabCI-cov](https://gitlab.com/piszczala/llameDL/badges/master/coverage.svg)](https://gitlab.com/piszczala/llameDL)


## Install
- pip install -r requirements.txt
- ffprobe or avprobe


## Use
llameDL is provided with CLI, installed using entry-points in setup.py

    llamedl

To download songs from browser bookmarks

    llamedl browser 
    
<p align="center"><img src="/media/browser-demo.gif?raw=true"/></p>
    
To download song from bookmarks file

    llamedl bookmarks
    
<p align="center"><img src="/media/bookmarks-demo.gif?raw=true"/></p>


To download one song or playlist

    llamedl playlist
    
<p align="center"><img src="/media/playlist-demo.gif?raw=true"/></p>

## Tagger

You can use llamedl tagger as standalone application with

    llametagger

## Thanks

- Ricardo Garcia (`youtube_dl` author)
- Mohammad Fares (`terminalizer` author)
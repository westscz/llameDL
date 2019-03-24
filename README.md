# llameDL

<p align="center"><img src="/media/logo.png"/></p>
<p align="center">YouTube to MP3 converter with adding tags</p>

![LlameDL Version](https://img.shields.io/badge/llameDL-0.2.0-blue.svg)
[![Build Status](https://travis-ci.org/westscz/llameDL.svg?branch=master)](https://travis-ci.org/westscz/llameDL)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
[![Code Coverage](https://scrutinizer-ci.com/g/westscz/llameDL/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/westscz/llameDL/?branch=master)
[![Requirements Status](https://requires.io/github/westscz/llameDL/requirements.svg?branch=master)](https://requires.io/github/westscz/llameDL/requirements/?branch=master)
[![Scrutinize Status](https://scrutinizer-ci.com/g/westscz/llameDL/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/westscz/llameDL/)



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
    
To download one song or playlist

    llamedl playlist

## Tagger

You can use llamedl tagger as standalone application with

    llametagger

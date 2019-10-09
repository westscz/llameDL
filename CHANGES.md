# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Filter new keywords from title
- Remove quotation mark from title
- Soundcloud downloader
- New architecture prototype

### Changed
- Path to whitelist
- Entry points path

## [0.2.0] - 2019-03-27
### Added
- New abstraction layer for URL providers
    - User provider URL
    - URL from Chrome
    - URL from Netscape formated file
- New abstraction layer for Downloaders
    - Download from YouTube
- New abstraction layer for Tag providers
    - Tags from musicbrainzgs
    - Tags from LastFM
    - Tags from file with artist-tags map
- CHANGES file with all changes between releases
- Missing tags from v0.0.1 to v0.1.0 created
- Integration tests
- Demo visualisation
- Integration with GitlabCI

### Changed
- CLI for llameDL and llameTagger
- Getting urls from Chrome is not default action anymore
- Structure of tests directory

## [0.1.0] - 2018-04-15
### Added
- CLI for llameDL and llameTagger
- Setup.py with entry points

### Changed
- Regex for youtube videos titles
- Scrutinizer setup

## [0.0.3] - 2018-04-09
### Added
- Docstring to class methods
- Whitelist file with whitelisted tags
- Setup.cfg for pytest and flake8
- Unit Tests for Tagger, IChrome and IYoutube
- Requirements-dev for TravisCI purpose
- Codecov, requires and scrutinizer support
- Tagger as stand-alone tool

### Changed
- Regex for youtube videos titles
- Tags from LastFM are supported again if MusicBrainzgs have missing tags

### Removed
- Support for python 2.7 (only python 3.5+ is supported)

## [0.0.2] - 2018-02-15
### Added
- Travis CI
- Tags whitelist

### Changed
- Tags searching from LastFM to MusicBrainz

## [0.0.1] - - 2018-02-02
### Added
- README with install informations
- Requirements file for Python requirements
- Functionality to get YouTube videos url from Chrome bookmarks
- Functionality to download YouTube video as mp3 file
- Functionality to add tags to mp3 files from LastFM

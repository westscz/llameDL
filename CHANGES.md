# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- CHANGES file with all changes between releases
- Old tags from v0.0.1 to v0.0.x

## v0.0.3 2018-04-09
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

## v0.0.2 2018-02-15
### Added
- Travis CI
- Tags whitelist

### Changed
- Tags searching from LastFM to MusicBrainz

## 0.0.1 - 2018-02-02
### Added
- README with install informations
- Requirements file for Python requirements
- Functionality to get YouTube videos url from Chrome bookmarks
- Functionality to download YouTube video as mp3 file
- Functionality to add tags to mp3 files from LastFM

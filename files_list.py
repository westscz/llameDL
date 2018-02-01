import os

from mutagen.easyid3 import EasyID3
from interfaces.lastfm import ILastFM as CheckLastFM


def add_genre(file):
    audio = EasyID3(files_path + file)
    x = str(audio['artist'][0])
    genre = CheckLastFM().do(x)
    genre_string = ';'.join(genre)
    audio['genre'] = genre_string
    audio['author'] = 'westscz LastFM genre tager'
    audio.save()


f = {}
files_path = 'mp3/'
for (dir, path, filename) in os.walk(files_path):
    f[dir] = filename

for dir in f:
    print(dir)
    for file in f[dir]:
        print('\n\tPrzetwarzam plik ' + file)
        add_genre(file)

# print(EasyID3.valid_keys.keys())

class UrlProvider()
    def __init__(self, url):
        self.urls = [url]

    def __iter__(self):
        return self.urls

class Tagger():
    ...

class DownloadManager():
    def __init__(self, urls_provider):
        self.urls_provider = urls_provider
        self.media = []

    def set_up(self):
        self.media = [
            self.create_media_object(url)
            for url
            in self.urls_provider
        ]

    def create_media_object(self, url):
        return Media(url)

    def download(self):
        for media in self.media:
            media.download()

class Media():
    def __init__(self, url, downloader):
        self.url = url
        self.downloader = downloader

    @property
    def name(self):
        return self.downloader.get_name(self.url)

    def download():
        self.fetch_audio()
        self.tag_audio()

    def fetch_audio(self):
        ...

    def tag_audio(self):
        ...
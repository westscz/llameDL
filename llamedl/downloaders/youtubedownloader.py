"""
    llamedl.youtubedownloader.py
    ~~~~~~~~~~~~~~~~~~~
"""
import youtube_dl
from llamedl.utill import create_logger, YTLogger, create_filename

LOGGER = create_logger("YouTube")


class YouTubeDownloader:
    """
    Module to get information about youtube url, and download audio
    """
    def __init__(self, download_directory):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': r"XD.%(ext)s",
            'logger': YTLogger()
        }
        self.__url_info = None
        self.__url = None
        self.download_directory = download_directory

    @property
    def url_info(self):
        """

        :return:
        """
        return self.__url_info

    @url_info.setter
    def url_info(self, video_url):
        print(video_url)
        self.__url = video_url
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                self.__url_info = ydl.extract_info(video_url, download=False)
        except youtube_dl.utils.DownloadError as error:
            LOGGER.debug(error.exc_info[1])
            self.__url_info = None

    def get_title(self):
        """
        Get title for video from url given to url_info.
        Original title will be fixed, and neccessary descriptions will be removed

        :return: Refactored title
        """
        return create_filename(self.url_info.get("title"))

    def verify_url(self, url):
        """

        :param url:
        :return:
        """
        self.url_info = url
        return self.get_playlist() if self.is_playlist() else [url]

    def is_playlist(self):
        """
        Check if url is a playlist

        :return:
        """
        return False if not self.url_info.get('_type') else True

    def get_playlist(self):
        """
        Get url of all videos in playlist

        :return: List of urls from playlist
        """
        try:
            return [entry.get('webpage_url') for entry in self.url_info.get('entries')]
        except TypeError:
            return []

    def download_mp3(self, video_url=None):
        """
        Download video from youtube and convert to mp3 format

        :param video_url: Url to youtube video
        :return: filename?
        """
        video_url = self.__url if not video_url else video_url
        try:
            filename = self.get_title()
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                self.__update_ydl_template(ydl, filename)
                if not ydl.download([video_url]):
                    LOGGER.info('"%s" Downloaded correctly!', filename)
                return True
        except youtube_dl.utils.DownloadError:
            return False

    def __update_ydl_template(self, ydl, filename):
        out_template = r"{}/{}.%(ext)s".format(self.download_directory, filename)
        LOGGER.debug(out_template)
        self.ydl_opts['outtmpl'] = out_template
        ydl.params.update(self.ydl_opts)

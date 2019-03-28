"""
    llamedl.youtubedownloader.py
    ~~~~~~~~~~~~~~~~~~~
"""
import youtube_dl

from llamedl.progress_logger import progresslogger
from llamedl.utill import YTLogger, create_filename, create_logger

LOGGER = create_logger(__name__)


class YouTubeDownloader:
    """Module to get information about youtube url, and download audio."""

    def __init__(self, download_directory):
        self.ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": r"XD.%(ext)s",
            "logger": YTLogger(),
        }
        self.__url_info = None
        self.__url = None
        self.download_directory = download_directory

    def get_url_info(self, video_url):
        if self.__url == video_url:
            return self.__url_info
        else:
            self.__url = video_url
            try:
                with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                    self.__url_info = ydl.extract_info(video_url, download=False)
            except youtube_dl.utils.DownloadError as error:
                LOGGER.error(error.exc_info[1])
                self.__url_info = {}
            return self.__url_info

    def is_url_available(self, url):
        url_info = self.get_url_info(url)
        return bool(url_info)

    def get_title(self, url):
        """Get title for video from url given to url_info. Original title will
        be fixed, and neccessary descriptions will be removed.

        :return: Refactored title
        """
        url_info = self.get_url_info(url)
        return create_filename(url_info.get("title"))

    def verify_url(self, url):
        """

        :param url:
        :return:
        """
        return self.get_playlist(url) if self.is_playlist(url) else [url]

    def is_playlist(self, url):
        """Check if url is a playlist.

        :return:
        """
        url_info = self.get_url_info(url)
        return False if not url_info.get("_type") else True

    def get_playlist(self, url):
        """Get url of all videos in playlist.

        :return: List of urls from playlist
        """
        url_info = self.get_url_info(url)
        try:
            return [entry.get("webpage_url") for entry in url_info.get("entries")]
        except TypeError:
            return []

    def download(self, video_url):
        downloaded = []
        if self.is_playlist(video_url):
            downloaded.extend(self.download_playlist(video_url))
        else:
            downloaded.append(self.download_song(video_url))
        return downloaded

    def download_playlist(self, playlist_url):
        downloaded = []
        progresslogger.info("Download playlist")
        playlist = self.get_playlist(playlist_url)
        progresslogger.change_size(len(playlist))
        for url in playlist:
            downloaded.append(self.download_song(url))
            progresslogger.__iadd__(1)
        return downloaded

    def download_song(self, video_url=None):
        """Download video from youtube and convert to mp3 format.

        :param video_url: Url to youtube video
        :return: filename?
        """
        if not self.is_url_available(video_url):
            return ""
        try:
            filename = self.get_title(video_url)
            progresslogger.info(filename)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                self.__update_ydl_template(ydl, filename)
                if not ydl.download([video_url]):
                    pass
                    LOGGER.debug('"%s" Downloaded correctly!', filename)
                return filename + ".mp3"
        except youtube_dl.utils.DownloadError as e:
            LOGGER.debug(f"Error on download {video_url}: {str(e)}")
            import traceback
            LOGGER.debug(traceback.format_exc())
            return ""

    def __update_ydl_template(self, ydl, filename, format="mp3"):
        out_template = r"{}/{}.{}".format(self.download_directory, filename, format)
        LOGGER.debug(out_template)
        self.ydl_opts["outtmpl"] = out_template
        ydl.params.update(self.ydl_opts)
        return out_template

import youtube_dl

from llamedl.downloaders.youtubedownloader import YouTubeDownloader
from llamedl.progress_logger import progresslogger
from llamedl.utill import YTLogger, create_filename, create_logger

LOGGER = create_logger(__name__)


class SoundcloudDownloader(YouTubeDownloader):
    """Module to get information about youtube url, and download audio."""

    def get_title(self, url):
        """Get title for video from url given to url_info. Original title will
        be fixed, and neccessary descriptions will be removed.

        :return: Refactored title
        """
        url_info = self.get_url_info(url)
        title = f"{url_info.get('uploader')} - {url_info.get('title')}"
        return create_filename(title)

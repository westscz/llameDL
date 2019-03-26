import os
import tempfile
import unittest

from llamedl.llamedl import LlameDLFire
from tests.utils import create_netscape_bookmarks_file, create_chrome_bookmarks_file


class TestLlameDL(unittest.TestCase):
    def setUp(self):
        self.dir_obj = tempfile.TemporaryDirectory()
        self.dir_path = self.dir_obj.name
        self.obj = LlameDLFire(download_directory=self.dir_path)

    def tearDown(self):
        self.dir_obj.cleanup()

    def test_bookmarks(self):
        self.data = """
        <!DOCTYPE NETSCAPE-Bookmark-file-1>
        <!-- This is an automatically generated file.
             It will be read and overwritten.
             DO NOT EDIT! -->
        <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
        <TITLE>Bookmarks</TITLE>
        <H1>Bookmarks</H1>
        <DL><p>
            <DT><H3 ADD_DATE="1537726948" LAST_MODIFIED="1553535633" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks bar</H3>
            <DL><p>
                <DT><H3 ADD_DATE="1547490253" LAST_MODIFIED="1553507973">Music</H3>
                <DL><p>
                    <DT><A HREF="https://soundcloud.com/meszi/meszi1902">MESZI live at Club Holidays, Orchowo (2019.02.23), Meszi</A>
                    <DT><A HREF="https://www.youtube.com/watch?v=R_uS0aT0bG8">Infected Mushroom - Guitarmass - YouTube</A>
                </DL><p>
            </DL><p>
        </DL><p>
        """
        file_path = create_netscape_bookmarks_file(self.data)
        self.obj.bookmarks(file_path, "Music")
        expected = ['Infected Mushroom - Guitarmass.mp3']
        result = os.listdir(self.dir_path)
        self.assertListEqual(expected, result)

    def test_playlist(self):
        pass

    def test_browser(self):
        self.data = {
            "roots": {
                "bookmark_bar": {
                    "children": [
                        {
                            "children": [
                                {
                                    "name": "Infected Mushroom - Guitarmass - YouTube",
                                    "type": "url",
                                    "url": "https://www.youtube.com/watch?v=R_uS0aT0bG8",
                                },
                                {
                                    "name": "MESZI live at Club Holidays, Orchowo (2019.02.23), Meszi",
                                    "type": "url",
                                    "url": "https://soundcloud.com/meszi/meszi1902",
                                },
                            ],
                            "name": "Music",
                            "type": "folder",
                        }
                    ],
                    "name": "Bookmarks bar",
                    "type": "folder",
                }
            }
        }
        file_path = create_chrome_bookmarks_file(self.data)
        self.obj.browser("Chrome", "Music", bookmarks_path=file_path)
        expected = ['Infected Mushroom - Guitarmass.mp3']
        result = os.listdir(self.dir_path)
        self.assertListEqual(expected, result)

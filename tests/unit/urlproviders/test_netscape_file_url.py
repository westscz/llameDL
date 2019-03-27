import unittest

from llamedl.urlproviders.netscapefileurl import NetscapeFileUrl
from tests.utils import create_netscape_bookmarks_file


class TestNetscapeFileUrl(unittest.TestCase):
    def setUp(self):
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
                    <DT><A HREF="https://www.youtube.com/watch?v=ceYKKNXFpSE">Infected Mushroom &amp; Bliss - Bliss on Mushrooms (feat. Miyavi)</A>
                </DL><p>
            </DL><p>
        </DL><p>
        """
        filepath = create_netscape_bookmarks_file(self.data)
        self.obj = NetscapeFileUrl(filepath)

    def test_get_folder__exist(self):
        result = self.obj.get_folder("Music")
        expected = [
            {
                "type": "bookmark",
                "url": "https://soundcloud.com/meszi/meszi1902",
                "title": "MESZI live at Club Holidays, Orchowo (2019.02.23), Meszi",
                "add_date": None,
                "icon": None,
            },
            {
                "add_date": None,
                "icon": None,
                "title": "Infected Mushroom - Guitarmass - YouTube",
                "type": "bookmark",
                "url": "https://www.youtube.com/watch?v=R_uS0aT0bG8",
            },
            {
                "add_date": None,
                "icon": None,
                "title": "Infected Mushroom & Bliss - Bliss on Mushrooms (feat. Miyavi)",
                "type": "bookmark",
                "url": "https://www.youtube.com/watch?v=ceYKKNXFpSE",
            },
        ]
        self.assertListEqual(expected, result)

    def test_get_folder__not_exist(self):
        with self.assertRaises(IndexError):
            self.obj.get_folder("Music foo")

    def test_get_youtube_urls_from_folder__exist(self):
        result = self.obj.get_youtube_urls_from_folder("Music")
        expected = [
            "https://www.youtube.com/watch?v=R_uS0aT0bG8",
            "https://www.youtube.com/watch?v=ceYKKNXFpSE",
        ]
        self.assertListEqual(expected, result)

    def test_get_youtube_urls_from_folder__not_exist(self):
        with self.assertRaises(IndexError):
            self.obj.get_youtube_urls_from_folder("Music foo")

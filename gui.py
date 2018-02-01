import wx
from interfaces.chrome import IChrome
from interfaces.youtube import IYouTube
from common.tageditor import TagEditor
from common.utill import create_logger

Logger = create_logger("Downloader")


def onButton(event):
    print("Button pressed.")


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, 'llameDownloader')
    frame.SetSize(100, 100, 800, 600)

    c = IChrome()
    yt = IYouTube()
    url_list = c.get_url_list()
    panel = wx.Panel(frame, wx.ID_ANY)


    def create_textfield(panel, url, name):
        pane = panel
        statictext = wx.StaticText(pane, wx.ID_ANY, label=name)
        statictext2 = wx.StaticText(pane, wx.ID_ANY, label=url)
        posPnlSzr = wx.BoxSizer(wx.HORIZONTAL)
        posPnlSzr.Add(statictext, 1, wx.GROW)
        posPnlSzr.Add(statictext2, 1, wx.GROW)
        # pane.SetSizer(posPnlSzr)


    def onButton(event):
        print("Button pressed.")
        statictext.SetLabelText("Wait a second...")
        # songs_list = [yt.get_url_info(url) for url in url_list]
        # statictext.SetLabelText("\n".join(songs_list))
        create_textfield(panel, "url", "song - song")
        create_textfield(panel, "url", "sog - song")
        create_textfield(panel, "ul", "song - song")
        create_textfield(panel, "url", "song - g")
        mainSzr = wx.BoxSizer(wx.VERTICAL)
        mainSzr.Add(panel, 1, wx.GROW)
        frame.SetSizerAndFit(mainSzr)


    statictext = wx.StaticText(panel, wx.ID_ANY, "foo", (10, 200))

    text_bookmark = wx.StaticText(panel, wx.ID_ANY, "Chrome bookmark folder name", (20, 80))
    textfield_bookmark = wx.TextCtrl(panel, wx.ID_ANY, "M", (200, 80))
    text_folder_path = wx.StaticText(panel, wx.ID_ANY, "Path to music folder", (20, 110))
    textfield_folder_path = wx.TextCtrl(panel, wx.ID_ANY, "/home/user/Music", (200, 110))

    button = wx.Button(panel, wx.ID_ANY, 'Load songs list', (10, 140))

    button.Bind(wx.EVT_BUTTON, onButton)

    frame.Centre()
    frame.Show()
    app.MainLoop()

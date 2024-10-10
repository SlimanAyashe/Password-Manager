import wx


class HoverButton(wx.Button):
    def __init__(self, parent, label, size=(120, 40)):
        super(HoverButton, self).__init__(parent, label=label, size=size)
        self.default_color = wx.Colour(30, 144, 255)
        self.hover_color = wx.Colour(72, 118, 255)
        self.SetBackgroundColour(self.default_color)
        self.SetForegroundColour(wx.Colour(255, 255, 255))

        self.Bind(wx.EVT_ENTER_WINDOW, self.on_hover)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)

    def on_hover(self, event):
        self.SetBackgroundColour(self.hover_color)
        self.Refresh()

    def on_leave(self, event):
        self.SetBackgroundColour(self.default_color)
        self.Refresh()

# Replace normal buttons with HoverButton

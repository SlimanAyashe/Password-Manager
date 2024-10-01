import wx
import os

class PasswordManager(wx.Frame):
    def __init__(self, *args, **kw):
        super(PasswordManager, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.SetTitle("Password Manager")

        # Create widgets
        self.name_label = wx.StaticText(self.panel, label="Account Name:")
        self.name_text = wx.TextCtrl(self.panel)

        self.password_label = wx.StaticText(self.panel, label="Password:")
        self.password_text = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)

        self.icon_label = wx.StaticText(self.panel, label="Select Icon:")
        self.icon_button = wx.Button(self.panel, label="Browse")
        self.icon_path = ""

        self.save_button = wx.Button(self.panel, label="Save Account")
        self.account_list = wx.ListBox(self.panel)

        # Bind events
        self.icon_button.Bind(wx.EVT_BUTTON, self.on_browse)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.name_label, 0, wx.ALL, 5)
        sizer.Add(self.name_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.password_label, 0, wx.ALL, 5)
        sizer.Add(self.password_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.icon_label, 0, wx.ALL, 5)
        sizer.Add(self.icon_button, 0, wx.ALL, 5)
        sizer.Add(self.save_button, 0, wx.ALL, 5)
        sizer.Add(self.account_list, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizer(sizer)
        self.SetSize((400, 300))

    def on_browse(self, event):
        """Open a file dialog to select an icon."""
        with wx.FileDialog(self, "Open Icon file", wildcard="Image files (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_OK:
                self.icon_path = file_dialog.GetPath()
                wx.MessageBox(f"Selected icon: {self.icon_path}", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_save(self, event):
        """Save the account information to the list."""
        name = self.name_text.GetValue()
        password = self.password_text.GetValue()

        if not name or not password:
            wx.MessageBox("Please enter both account name and password.", "Error", wx.OK | wx.ICON_ERROR)
            return

        account_info = f"Name: {name}, Password: {password}, Icon: {self.icon_path}"
        self.account_list.Append(account_info)

        # Clear input fields
        self.name_text.Clear()
        self.password_text.Clear()
        self.icon_path = ""

if __name__ == "__main__":
    app = wx.App(False)
    frame = PasswordManager(None)
    frame.Show()
    app.MainLoop()

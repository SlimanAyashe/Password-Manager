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
        self.copy_password_button = wx.Button(self.panel, label="Copy Selected Password")
        self.remove_password_button = wx.Button(self.panel, label="Remove Selected Account")  # New button to remove the account

        # Use wx.ListCtrl to display icons and account information
        self.account_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.account_list.InsertColumn(0, "Icon", width=50)
        self.account_list.InsertColumn(1, "Account Name", width=150)

        # Load image list for icons
        self.image_list = wx.ImageList(50, 50)
        self.account_list.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)

        # Bind events
        self.icon_button.Bind(wx.EVT_BUTTON, self.on_browse)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        self.copy_password_button.Bind(wx.EVT_BUTTON, self.on_copy_password)
        self.remove_password_button.Bind(wx.EVT_BUTTON, self.on_remove_account)  # Bind remove button event

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.name_label, 0, wx.ALL, 5)
        main_sizer.Add(self.name_text, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.password_label, 0, wx.ALL, 5)
        main_sizer.Add(self.password_text, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.icon_label, 0, wx.ALL, 5)
        main_sizer.Add(self.icon_button, 0, wx.ALL, 5)
        main_sizer.Add(self.save_button, 0, wx.ALL, 5)
        main_sizer.Add(wx.StaticText(self.panel, label="Saved Accounts:"), 0, wx.ALL, 5)
        main_sizer.Add(self.account_list, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(self.copy_password_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        main_sizer.Add(self.remove_password_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)  # Add the remove button to layout

        self.panel.SetSizer(main_sizer)
        self.SetSize((400, 550))  # Adjusted height to accommodate the new button

        # Dictionary to store account passwords
        self.passwords = {}

    def on_browse(self, event):
        """Open a file dialog to select an icon."""
        with wx.FileDialog(self, "Open Icon file", wildcard="Image files (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_OK:
                self.icon_path = file_dialog.GetPath()
                #wx.MessageBox(f"Selected icon: {self.icon_path}", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_save(self, event):
        """Save the account information to the list."""
        name = self.name_text.GetValue()
        password = self.password_text.GetValue()

        if not name or not password:
            wx.MessageBox("Please enter both account name and password.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Store the password in the dictionary
        self.passwords[name] = password

        # Load the icon, resize it, and convert it to a bitmap
        if self.icon_path:
            image = wx.Image(self.icon_path, wx.BITMAP_TYPE_ANY)
            image = image.Rescale(50, 50, wx.IMAGE_QUALITY_HIGH)  # Resize the image to 50x50 pixels
            icon_index = self.image_list.Add(image.ConvertToBitmap())
        else:
            icon_index = -1  # No icon selected

        # Add the account info to the list control
        index = self.account_list.InsertItem(0, "", icon_index)  # Set empty string for icon column
        self.account_list.SetItem(index, 1, name)  # Set the account name

        # Clear input fields
        self.name_text.Clear()
        self.password_text.Clear()
        self.icon_path = ""

    def on_copy_password(self, event):
        """Copy the password of the selected account to the clipboard."""
        selected_item_index = self.account_list.GetFirstSelected()
        if selected_item_index == -1:
            wx.MessageBox("Please select an account to copy the password.", "Error", wx.OK | wx.ICON_ERROR)
            return

        account_name = self.account_list.GetItemText(selected_item_index, col=1)
        if account_name in self.passwords:
            password = self.passwords[account_name]
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(password))
                wx.TheClipboard.Close()
                wx.MessageBox(f"Password for {account_name} copied to clipboard!", "Info", wx.OK | wx.ICON_INFORMATION)

    def on_remove_account(self, event):
        """Remove the selected account from the list."""
        selected_item_index = self.account_list.GetFirstSelected()
        if selected_item_index == -1:
            wx.MessageBox("Please select an account to remove.", "Error", wx.OK | wx.ICON_ERROR)
            return

        account_name = self.account_list.GetItemText(selected_item_index, col=1)

        # Remove from the list and the dictionary
        self.account_list.DeleteItem(selected_item_index)
        if account_name in self.passwords:
            del self.passwords[account_name]

        wx.MessageBox(f"Account {account_name} has been removed.", "Info", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App(False)
    frame = PasswordManager(None)
    frame.Show()
    app.MainLoop()

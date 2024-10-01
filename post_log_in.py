import wx
import os
import json


class PasswordManager(wx.Frame):
    def __init__(self, username, *args, **kw):
        super(PasswordManager, self).__init__(*args, **kw)

        self.username = username
        self.icon_folder = "icons"  # Folder to save icons
        os.makedirs(self.icon_folder, exist_ok=True)  # Create folder if it doesn't exist

        # Dictionary to store account passwords
        self.passwords = {}

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
        self.remove_password_button = wx.Button(self.panel, label="Remove Selected Account")

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
        self.remove_password_button.Bind(wx.EVT_BUTTON, self.on_remove_account)

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
        main_sizer.Add(self.remove_password_button, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.panel.SetSizer(main_sizer)
        self.SetSize((400, 550))

        # Load saved data
        self.load_data()

    def load_data(self):
        """Load passwords and icons for the current user."""
        try:
            user_file = f"{self.username}_passwords.json"
            if os.path.exists(user_file):
                with open(user_file, 'r') as file:
                    self.passwords = json.load(file)

                # Populate the ListCtrl with the saved data
                for account_name, details in self.passwords.items():
                    password = details['password']
                    icon_path = details['icon_path']

                    # Load the icon and add to the image list
                    image = wx.Image(icon_path, wx.BITMAP_TYPE_ANY)
                    image = image.Rescale(50, 50, wx.IMAGE_QUALITY_HIGH)
                    icon_index = self.image_list.Add(image.ConvertToBitmap())

                    # Add account name to the list
                    index = self.account_list.InsertItem(self.account_list.GetItemCount(), "", icon_index)
                    self.account_list.SetItem(index, 1, account_name)
        except Exception as e:
            wx.MessageBox(f"Error loading data: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_browse(self, event):
        """Open a file dialog to select an icon."""
        with wx.FileDialog(self, "Open Icon file", wildcard="Image files (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_OK:
                self.icon_path = file_dialog.GetPath()

    def on_save(self, event):
        """Save the account information to the list."""
        name = self.name_text.GetValue()
        password = self.password_text.GetValue()

        if not name or not password:
            wx.MessageBox("Please enter both account name and password.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # Save the account information in the dictionary
        self.passwords[name] = {
            'password': password,
            'icon_path': self.icon_path  # Store the icon path
        }

        # Save to the JSON file
        self.save_data()

        # Load the icon, resize it, and convert it to a bitmap
        if self.icon_path:
            image = wx.Image(self.icon_path, wx.BITMAP_TYPE_ANY)
            image = image.Rescale(50, 50, wx.IMAGE_QUALITY_HIGH)
            icon_index = self.image_list.Add(image.ConvertToBitmap())
        else:
            icon_index = -1  # No icon selected

        # Add the account info to the list control
        index = self.account_list.InsertItem(self.account_list.GetItemCount(), "", icon_index)
        self.account_list.SetItem(index, 1, name)

        # Clear input fields
        self.name_text.Clear()
        self.password_text.Clear()
        self.icon_path = ""

    def save_data(self):
        """Save passwords and icons for the current user to a JSON file."""
        user_file = f"{self.username}_passwords.json"
        with open(user_file, 'w') as file:
            json.dump(self.passwords, file)

    def on_copy_password(self, event):
        """Copy the password of the selected account to the clipboard."""
        selected_item_index = self.account_list.GetFirstSelected()
        if selected_item_index == -1:
            wx.MessageBox("Please select an account to copy the password.", "Error", wx.OK | wx.ICON_ERROR)
            return

        account_name = self.account_list.GetItemText(selected_item_index, col=1)
        if account_name in self.passwords:
            password = self.passwords[account_name]['password']
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
            self.save_data()  # Save changes to file

        wx.MessageBox(f"Account {account_name} has been removed.", "Info", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    app = wx.App(False)
    username = "default_user"  # Replace with actual username logic from your login
    frame = PasswordManager(username)
    frame.Show()
    app.MainLoop()

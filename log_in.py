import base64
import wx
import json
import os
<<<<<<< HEAD
from post_log_in import PasswordManager  # Import your PasswordManager class
=======
import base64
from post_log_in import PasswordManager
>>>>>>> Encryption
from Encryption import encrypt_message,decrypt_message

class LoginApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(LoginApp, self).__init__(*args, **kw)

        # Load existing users
        self.users_file = "users.json"
        self.users = self.load_users()

        # Setting up the frame
        self.SetTitle("Login Screen")
        self.SetSize((550, 450))
        self.Center()

        # Create panel and set background color
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(255, 223, 186))

        # Create a box sizer for vertical alignment
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create a login box
        login_box = wx.Panel(panel)
        login_box.SetBackgroundColour(wx.Colour(255, 223, 186))

        login_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(login_box, label="Login", style=wx.ALIGN_CENTER)
        font = title.GetFont()
        font.PointSize += 8
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(30, 144, 255))
        login_sizer.Add(title, 0, wx.ALL | wx.CENTER, 15)

        # Username input
        username_label = wx.StaticText(login_box, label="Username:")
        username_label.SetForegroundColour(wx.Colour(30, 144, 255))
        self.username_text = wx.TextCtrl(login_box, size=(300, 35))
        login_sizer.Add(username_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        login_sizer.Add(self.username_text, 0, wx.ALL | wx.CENTER, 5)

        # Password input
        password_label = wx.StaticText(login_box, label="Password:")
        password_label.SetForegroundColour(wx.Colour(30, 144, 255))
        self.password_text = wx.TextCtrl(login_box, size=(300, 35), style=wx.TE_PASSWORD)
        login_sizer.Add(password_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        login_sizer.Add(self.password_text, 0, wx.ALL | wx.CENTER, 5)

        # Login button
        login_button = wx.Button(login_box, label="Login", size=(120, 40))
        login_button.SetBackgroundColour(wx.Colour(30, 144, 255))
        login_button.SetForegroundColour(wx.Colour(255, 255, 255))
        login_sizer.Add(login_button, 0, wx.ALL | wx.CENTER, 10)
        login_button.Bind(wx.EVT_BUTTON, self.on_login)

        # Signup button
        signup_button = wx.Button(login_box, label="Sign Up", size=(120, 40))
        signup_button.SetBackgroundColour(wx.Colour(30, 144, 255))
        signup_button.SetForegroundColour(wx.Colour(255, 255, 255))
        login_sizer.Add(signup_button, 0, wx.ALL | wx.CENTER, 10)
        signup_button.Bind(wx.EVT_BUTTON, self.on_signup)

        # Apply the layout to the login box
        login_box.SetSizer(login_sizer)

        # Add login box to the vertical layout of the panel
        vbox.Add(login_box, 0, wx.ALL | wx.CENTER, 20)
        panel.SetSizer(vbox)

<<<<<<< HEAD

=======
    import base64
>>>>>>> Encryption

    def save_users(self):
        """Save users to the JSON file with Base64 encoded passwords."""
        users_to_save = {user: base64.b64encode(self.users[user]).decode('utf-8') for user in self.users}
        with open(self.users_file, 'w') as f:
            json.dump(users_to_save, f)

    def load_users(self):
        """Load users from the JSON file and decode Base64 passwords."""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users_loaded = json.load(f)
                return {user: base64.b64decode(users_loaded[user]) for user in users_loaded}
        return {}

    def on_login(self, event):
        """Check username and password when login button is clicked."""
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        if username in self.users and decrypt_message(self.users[username]) == (password):
            self.Hide()
            after_log_in_screen = PasswordManager(username=username, parent=self)
            after_log_in_screen.Show()
        else:
            wx.MessageBox("Invalid username or password.", "Error", wx.OK | wx.ICON_ERROR)

    def on_signup(self, event):
        """Open the signup window."""
        signup_window = SignupApp(self)  # Pass the current LoginApp instance
        signup_window.Show()


class SignupApp(wx.Frame):
    def __init__(self, parent):
        super(SignupApp, self).__init__(parent)
        self.parent = parent  # Store the parent reference

        # Setting up the frame
        self.SetTitle("Sign Up")
        self.SetSize((400, 300))
        self.Center()

        # Create panel
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(255, 223, 186))

        # Create a box sizer for vertical alignment
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label="Sign Up", style=wx.ALIGN_CENTER)
        font = title.GetFont()
        font.PointSize += 8
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(30, 144, 255))
        vbox.Add(title, 0, wx.ALL | wx.CENTER, 15)

        # Username input
        username_label = wx.StaticText(panel, label="Username:")
        username_label.SetForegroundColour(wx.Colour(30, 144, 255))
        self.username_text = wx.TextCtrl(panel, size=(300, 35))
        vbox.Add(username_label, 0, wx.ALL, 5)
        vbox.Add(self.username_text, 0, wx.ALL | wx.CENTER, 5)

        # Password input
        password_label = wx.StaticText(panel, label="Password:")
        password_label.SetForegroundColour(wx.Colour(30, 144, 255))
        self.password_text = wx.TextCtrl(panel, size=(300, 35), style=wx.TE_PASSWORD)
        vbox.Add(password_label, 0, wx.ALL, 5)
        vbox.Add(self.password_text, 0, wx.ALL | wx.CENTER, 5)

        # Sign Up button
        signup_button = wx.Button(panel, label="Sign Up", size=(120, 40))
        signup_button.SetBackgroundColour(wx.Colour(30, 144, 255))
        signup_button.SetForegroundColour(wx.Colour(255, 255, 255))
        vbox.Add(signup_button, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        signup_button.Bind(wx.EVT_BUTTON, self.on_signup)

        # Apply the layout to the panel
        panel.SetSizer(vbox)

    def on_signup(self, event):
        """Handle the signup process."""
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        if username in self.parent.users:
            wx.MessageBox("Username already exists. Please choose a different one.", "Error", wx.OK | wx.ICON_ERROR)
            return
        if len(password) < 8 or len(password) > 16:
            wx.MessageBox("Password length should be between 8 and 16", "Error", wx.OK | wx.ICON_ERROR)
            return
        # Save the new user
        self.parent.users[username] = (encrypt_message(password))
        self.parent.save_users()  # Save to JSON file

        wx.MessageBox("Signup successful! You can now log in.", "Success", wx.OK | wx.ICON_INFORMATION)
        self.Close()

# Initialize the wxPython app
if __name__ == '__main__':
    app = wx.App(False)
    frame = LoginApp(None)
    frame.Show()
    app.MainLoop()

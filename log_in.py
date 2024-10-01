import wx
from post_log_in import PasswordManager

class LoginApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(LoginApp, self).__init__(*args, **kw)

        # Predefined username and password for demo purposes
        self.correct_username = "admin"
        self.correct_password = "password123"

        # Setting up the frame
        self.SetTitle("Login Screen")
        self.SetSize((550, 450))  # Increased size for a larger window
        self.Center()

        # Create panel and set background color
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(255, 223, 186))  # Soft peach background

        # Create a box sizer for vertical alignment
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Create a login box with a colorful background
        login_box = wx.Panel(panel)
        login_box.SetBackgroundColour(wx.Colour(255, 223, 186))  # White background
        login_box.SetForegroundColour(wx.Colour(0, 0, 0))  # Black text color

        login_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title with larger font and centered alignment
        title = wx.StaticText(login_box, label="Login", style=wx.ALIGN_CENTER)
        font = title.GetFont()
        font.PointSize += 8
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title.SetFont(font)
        title.SetForegroundColour(wx.Colour(30, 144, 255))  # Bright blue color
        login_sizer.Add(title, 0, wx.ALL | wx.CENTER, 15)

        # Username input with vibrant styling
        username_label = wx.StaticText(login_box, label="Username:")
        username_label.SetForegroundColour(wx.Colour(30, 144, 255))  # Bright blue color
        self.username_text = wx.TextCtrl(login_box, size=(300, 35))
        self.username_text.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        login_sizer.Add(username_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        login_sizer.Add(self.username_text, 0, wx.ALL | wx.CENTER, 5)

        # Password input (masked) with vibrant styling
        password_label = wx.StaticText(login_box, label="Password:")
        password_label.SetForegroundColour(wx.Colour(30, 144, 255))  # Bright blue color
        self.password_text = wx.TextCtrl(login_box, size=(300, 35), style=wx.TE_PASSWORD)
        self.password_text.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        login_sizer.Add(password_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        login_sizer.Add(self.password_text, 0, wx.ALL | wx.CENTER, 5)

        # Login button with a modern style
        login_button = wx.Button(login_box, label="Login", size=(120, 40))
        login_button.SetBackgroundColour(wx.Colour(30, 144, 255))  # Blue background
        login_button.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        login_button.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        # Bind hover events for better visibility
        login_button.Bind(wx.EVT_ENTER_WINDOW, lambda event: login_button.SetBackgroundColour(wx.Colour(0, 0, 139)))  # Darker blue on hover
        login_button.Bind(wx.EVT_LEAVE_WINDOW, lambda event: login_button.SetBackgroundColour(wx.Colour(30, 144, 255)))  # Original blue when not hovered

        login_sizer.Add(login_button, 0, wx.ALL | wx.CENTER, 10)
        login_button.Bind(wx.EVT_BUTTON, self.on_login)

        # Apply the layout to the login box
        login_box.SetSizer(login_sizer)

        # Add login box to the vertical layout of the panel
        vbox.Add(login_box, 0, wx.ALL | wx.CENTER, 20)
        panel.SetSizer(vbox)

    def on_login(self, event):
        """Check username and password when login button is clicked."""
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        if username == self.correct_username and password == self.correct_password:
            self.Hide()
            after_log_in_screen= PasswordManager(None)
            after_log_in_screen.Show()
        else:
            wx.MessageBox("Invalid username or password.", "Error", wx.OK | wx.ICON_ERROR)


# Initialize the wxPython app
if __name__ == '__main__':
    app = wx.App(False)
    frame = LoginApp(None)
    frame.Show()
    app.MainLoop()

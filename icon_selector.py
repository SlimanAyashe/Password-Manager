import wx
import os


class IconSelectorDialog(wx.Dialog):
    def __init__(self, parent, icon_folder):
        super(IconSelectorDialog, self).__init__(parent, title="Select Icon", size=(400, 300))

        self.icon_folder = icon_folder
        self.selected_icon_path = None

        # Create a panel within the dialog to hold the controls
        panel = wx.Panel(self)

        # Sizer for the dialog
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Add a title label
        label = wx.StaticText(panel, label="Select an Icon:")
        sizer.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # FlexGridSizer to display the icons
        grid_sizer = wx.FlexGridSizer(cols=5, hgap=10, vgap=10)

        # Load all icon files from the icon folder
        for icon_file in os.listdir(self.icon_folder):
            if icon_file.endswith(('.png', '.jpg', '.jpeg')):
                icon_path = os.path.join(self.icon_folder, icon_file)

                # Create a bitmap button for each icon
                bitmap = wx.Image(icon_path, wx.BITMAP_TYPE_ANY).Rescale(50, 50).ConvertToBitmap()
                btn = wx.BitmapButton(panel, bitmap=bitmap, size=(50, 50))

                # Bind the button to a handler that stores the selected icon path
                btn.Bind(wx.EVT_BUTTON, lambda event, path=icon_path: self.on_icon_selected(path))

                # Add the button to the grid sizer
                grid_sizer.Add(btn, 0, wx.ALIGN_CENTER)

        # Add grid sizer to the main sizer
        sizer.Add(grid_sizer, 1, wx.ALIGN_CENTER | wx.ALL, 10)

        # Create OK and Cancel buttons manually
        ok_button = wx.Button(panel, wx.ID_OK, label="OK")
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label="Cancel")

        # Bind the button events if needed
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        # Add the buttons to a horizontal sizer
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(ok_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # Add the button sizer to the main sizer
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Set the sizer for the panel and the dialog
        panel.SetSizerAndFit(sizer)
        self.Fit()

    def on_icon_selected(self, icon_path):
        self.selected_icon_path = icon_path

    def on_ok(self, event):
        self.EndModal(wx.ID_OK)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)
    def get_selected_icon_path(self):
         return self.selected_icon_path

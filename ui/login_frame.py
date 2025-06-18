import wx

from ui.main_frame import MainFrame
from api.user_api import login

class LoginFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=wx.Size(640, 480))
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(30, 30, 30))

        self.create_widgets()
        self.Centre()

    def create_widgets(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(10, 10)

        # --- Title ---
        title_label = wx.StaticText(self.panel, label="欢迎登录")
        title_font = wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(title_font)
        title_label.SetForegroundColour(wx.WHITE)
        vbox.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 30)

        # Username Label and Text Control
        username_label = wx.StaticText(self.panel, label="用户名:")
        username_label.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        username_label.SetForegroundColour(wx.Colour(200, 200, 200))
        grid_sizer.Add(username_label, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=15)

        self.username_text = wx.TextCtrl(self.panel, size=wx.Size(300, 40), style=wx.BORDER_NONE | wx.TEXT_ALIGNMENT_CENTER)
        self.username_text.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.username_text.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.username_text.SetForegroundColour(wx.WHITE)
        self.username_text.SetInsertionPoint(0)
        # 垂直居中
        self.username_text.SetMargins(0, 20)
        grid_sizer.Add(self.username_text, pos=(0, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=10)

        # Password Label and Text Control
        password_label = wx.StaticText(self.panel, label="密 码:")
        password_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        password_label.SetForegroundColour(wx.Colour(200, 200, 200))
        grid_sizer.Add(password_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=15)

        self.password_text = wx.TextCtrl(self.panel, size=wx.Size(300, 40), style=wx.TE_PASSWORD | wx.BORDER_NONE)
        self.password_text.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.password_text.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.password_text.SetForegroundColour(wx.WHITE)
        self.password_text.SetInsertionPoint(0)
        # 垂直居中
        self.password_text.SetMargins(0, 20)
        grid_sizer.Add(self.password_text, pos=(1, 1), flag=wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=10)

        # Login Button
        login_button = wx.Button(self.panel, label="登录", size=wx.Size(250, 50))
        login_button.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        login_button.SetBackgroundColour(wx.Colour(255, 48, 114))
        login_button.SetForegroundColour(wx.WHITE)
        login_button.Bind(wx.EVT_BUTTON, self.on_login)
        login_button.Bind(wx.EVT_ENTER_WINDOW, self.on_button_hover)
        login_button.Bind(wx.EVT_LEAVE_WINDOW, self.on_button_leave)
        grid_sizer.Add(login_button, pos=(2, 0), span=(1, 2), flag=wx.ALIGN_CENTER | wx.TOP, border=30)

        # Set row and column proportions
        grid_sizer.AddGrowableCol(1, 1)
        grid_sizer.AddGrowableRow(0, 0)
        grid_sizer.AddGrowableRow(1, 0)

        vbox.Add(grid_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 50)
        self.panel.SetSizer(vbox)

        self.original_button_color = login_button.GetBackgroundColour()

    def on_button_hover(self, event):
        button = event.GetEventObject()
        button.SetBackgroundColour(wx.Colour(255, 80, 140))
        button.Refresh()

    def on_button_leave(self, event):
        button = event.GetEventObject()
        button.SetBackgroundColour(self.original_button_color)
        button.Refresh()

    def on_login(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        # 调用API封装的登录方法
        data = login(username, password)
        if data.get("success"):
            self.Hide()
            main_frame = MainFrame(None, title="主界面 - 任务管理")
            main_frame.Show()
        else:
            wx.MessageBox(data.get("msg", "用户名或密码错误！"), "登录失败", wx.OK | wx.ICON_ERROR)
            self.username_text.SetValue("")
            self.password_text.SetValue("")


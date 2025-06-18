import wx
import threading


from api.user_session import UserSession
from api.user_settings_api import create_or_update_user_settings, get_user_settings




class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="设置", size=wx.Size(450, 360))
        self.InitUI()
        self.CenterOnParent()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        # prefix_label和token_ctrl左对齐
        hbox_prefix = wx.BoxSizer(wx.HORIZONTAL)
        hbox_prefix.Add(wx.Size(105,20))  # 预留label宽度，保证和token_ctrl左对齐，y坐标下移10像素
        prefix_label = wx.StaticText(self, label="Token前面必须带前缀Bearer")
        prefix_label.SetForegroundColour(wx.Colour(255, 0, 0))
        hbox_prefix.Add(prefix_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL,8)
        vbox.Add(hbox_prefix, 0, wx.EXPAND | wx.ALL, 0)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label="Runway Token:")
        hbox1.Add(label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)
        self.token_ctrl = wx.TextCtrl(self, size=wx.Size(260, 120), style=wx.TE_MULTILINE)
        hbox1.Add(self.token_ctrl, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)
        vbox.Add(hbox1, 0, wx.EXPAND | wx.ALL, 5)

        # 视频路径输入框
        hbox_video = wx.BoxSizer(wx.HORIZONTAL)
        video_label = wx.StaticText(self, label="视频保存路径:")
        hbox_video.Add(video_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)
        self.video_path_ctrl = wx.TextCtrl(self, size=wx.Size(260, 35), style=wx.TE_READONLY)
        hbox_video.Add(self.video_path_ctrl, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)
        select_btn = wx.Button(self, label="选择路径", size=wx.Size(80, 35))
        select_btn.Bind(wx.EVT_BUTTON, self.on_select_video_path)
        hbox_video.Add(select_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 8)
        vbox.Add(hbox_video, 0, wx.EXPAND | wx.ALL, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(self, wx.ID_OK, label="确定")
        cancel_btn = wx.Button(self, wx.ID_CANCEL, label="取消")
        hbox2.AddStretchSpacer(1)
        hbox2.Add(ok_btn, 0, wx.ALL, 5)
        hbox2.Add(cancel_btn, 0, wx.ALL, 5)
        vbox.Add(hbox2, 0, wx.EXPAND | wx.BOTTOM, 10)
        self.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.on_ok, ok_btn)

        # 读取数据库token
        self.loading_dialog = None
        self.load_user_settings()

    def load_user_settings(self):
        def fetch():
            user_dict = get_user_settings(UserSession.get_user_id())
            wx.CallAfter(self.on_user_settings_loaded, user_dict.get("data", {}))

        self.loading = wx.BusyInfo("正在加载配置中，请稍候...", parent=self)
        wx.YieldIfNeeded()
        threading.Thread(target=fetch, daemon=True).start()

    def on_user_settings_loaded(self, user_dict):
        if hasattr(self, 'loading') and self.loading:
            del self.loading
            wx.YieldIfNeeded()
        if user_dict and user_dict.get("token"):
            self.token_ctrl.SetValue(user_dict.get("token") or "")
            self.video_path_ctrl.SetValue(user_dict.get("save_video_path") or "")

    def on_ok(self, event):
        token = self.token_ctrl.GetValue().strip()
        video_path = self.video_path_ctrl.GetValue().strip()
        if len(token) == 0:
            wx.MessageBox("输入Token不能为空！", "错误", wx.OK | wx.ICON_ERROR)
            return
        if len(video_path) == 0:
            wx.MessageBox("请选择视频保存路径！", "错误", wx.OK | wx.ICON_ERROR)
            return
        user_setting = {
            "token": token,
            "video_save_path": video_path
        }
        def save():
            result = create_or_update_user_settings(UserSession.get_user_id(), user_setting)
            wx.CallAfter(self.on_save_settings_result, result)
            # 显示loading对话框
            self.loading = wx.BusyInfo("正在提交中，请稍候...", parent=self)
            wx.YieldIfNeeded()
        threading.Thread(target=save, daemon=True).start()

    def on_save_settings_result(self, result):
        if hasattr(self, 'loading') and self.loading:
            del self.loading
            wx.YieldIfNeeded()
        if result.get("success") is False:
            wx.MessageBox(f"保存设置失败: {result.get('data', {}).get('message', '')}", "错误", wx.OK | wx.ICON_ERROR)
            return
        self.EndModal(wx.ID_OK)

    def on_select_video_path(self, event):
        dlg = wx.DirDialog(self, "选择视频保存文件夹")
        if dlg.ShowModal() == wx.ID_OK:
            self.video_path_ctrl.SetValue(dlg.GetPath())
        dlg.Destroy()

import wx
from api.task_execution_api import get_task_detail, update_task, run_task, create_task
from api.text_optimize_api import get_optimize_text
from api.user_session import UserSession
import threading



class AddTaskDialog(wx.Dialog):
    def __init__(self, parent, existing_task=None, task_id=None):
        super().__init__(parent, title="新增/编辑任务", size=wx.Size(540, 460))
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour("#FFFFFF"))  # 设置面板背景颜色
        self.task_id = task_id
        self.task_data = {}
        self.create_widgets()
        self.CentreOnParent()

        if self.task_id:
            self.load_existing_task_data()

    def create_widgets(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(5, 5)

        # Prompt
        prompt_label = wx.StaticText(self.panel, label="任务Prompt:")
        prompt_label.SetForegroundColour(wx.Colour("#000000"))  # 设置字体颜色
        grid_sizer.Add(prompt_label, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        self.prompt_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, size=wx.Size(350, 100))
        self.prompt_text.SetBackgroundColour(wx.Colour("#F7F7F7"))  # Light Gray
        grid_sizer.Add(self.prompt_text, pos=(0, 1), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        # Optimize Button
        optimize_btn = wx.Button(self.panel, label="提示词优化", size=wx.Size(120, 30))
        optimize_btn.Bind(wx.EVT_BUTTON, self.on_optimize_prompt)
        optimize_btn.SetBackgroundColour(wx.Colour("#007ACC"))  # 蓝色
        optimize_btn.SetForegroundColour(wx.Colour("#FFFFFF"))  # 白色
        grid_sizer.Add(optimize_btn, pos=(1, 2), flag=wx.ALIGN_RIGHT  | wx.ALL, border=5)
        # File Name
        file_name_label = wx.StaticText(self.panel, label="文件命名:")
        file_name_label.SetForegroundColour(wx.Colour("#000000"))
        grid_sizer.Add(file_name_label, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        self.file_name_text = wx.TextCtrl(self.panel, size=wx.Size(200, -1))
        self.file_name_text.SetBackgroundColour(wx.Colour("#F7F7F7"))
        grid_sizer.Add(self.file_name_text, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)
        # Ratio
        ratio_label = wx.StaticText(self.panel, label="Ratio:")
        grid_sizer.Add(ratio_label, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        self.ratio_choice = wx.Choice(self.panel, choices=["9:16", "16:9"], size=wx.Size(200, -1))
        grid_sizer.Add(self.ratio_choice, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Model Name
        model_label = wx.StaticText(self.panel, label="模型名称:")
        grid_sizer.Add(model_label, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        self.model_choice = wx.Choice(self.panel, choices=["gen3a_turbo"], size=wx.Size(200, -1))
        grid_sizer.Add(self.model_choice, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Duration
        duration_label = wx.StaticText(self.panel, label="时长(秒):")
        grid_sizer.Add(duration_label, pos=(4, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        self.duration_choice = wx.Choice(self.panel, choices=["5", "10"], size=wx.Size(200, -1))
        grid_sizer.Add(self.duration_choice, pos=(4, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Video Nums
        nums_label = wx.StaticText(self.panel, label="生成数量:")
        grid_sizer.Add(nums_label, pos=(5, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        self.nums_choice = wx.Choice(self.panel, choices=[str(i) for i in range(1, 5)], size=wx.Size(200, -1))
        self.nums_choice.SetSelection(0)
        grid_sizer.Add(self.nums_choice, pos=(5, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # 是否运行 Checkbox
        self.run_checkbox = wx.CheckBox(self.panel, label="添加后立即运行")
        self.run_checkbox.SetValue(True)
        grid_sizer.Add(self.run_checkbox, pos=(6, 0), flag=wx.ALIGN_LEFT | wx.ALL, border=5)

        # OK and Cancel buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(self.panel, wx.ID_OK, label="确定", size=wx.Size(80, 40))
        ok_btn.SetBackgroundColour(wx.Colour(40, 167, 69))  # 绿色
        ok_btn.SetForegroundColour(wx.Colour(255, 255, 255))   # 白色
        cancel_btn = wx.Button(self.panel, wx.ID_CANCEL, label="取消", size=wx.Size(80, 40))
        cancel_btn.SetBackgroundColour(wx.Colour(255, 59, 48))  # 红色
        cancel_btn.SetForegroundColour(wx.Colour(255, 255, 255))   # 白色
        btn_sizer.Add(ok_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        btn_sizer.Add(cancel_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        grid_sizer.Add(btn_sizer, pos=(6, 1), span=(1, 2), flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        main_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(main_sizer)

        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_cancel)

    def load_existing_task_data(self):
        if self.task_id:
            result = get_task_detail(UserSession.get_user_id(), self.task_id)
            if result.get('success') is False:
                wx.MessageBox(f"加载任务失败: {result.get('msg', '未知错误')}", "错误", wx.OK | wx.ICON_ERROR)
                return
            task = result.get('data', {})
            if task:
                self.prompt_text.SetValue(task.get('prompt', ''))
                self.ratio_choice.SetStringSelection(task.get('ratio', '9:16'))
                self.model_choice.SetStringSelection(task.get( 'model', 'gen3a_turbo'))
                self.duration_choice.SetStringSelection(str(task.get('video_duration', '5')))
                self.file_name_text.SetValue(task.get('video_name',''))
                self.nums_choice.SetStringSelection(str(task.get('video_nums', '1')))


    def on_optimize_prompt(self, event):
        user_prompt = self.prompt_text.GetValue()
        if not user_prompt.strip():
            wx.MessageBox('请输入需要优化的提示词', '提示', wx.OK | wx.ICON_INFORMATION)
            return

        # 显示loading对话框
        loading = wx.BusyInfo("正在优化提示词，请稍候...", parent=self)
        wx.YieldIfNeeded()
        try:
            result = get_optimize_text(user_prompt)
            if result.get('success') is False:
                wx.MessageBox(f"优化提示词失败: {result.get('msg', '未知错误')}", "错误", wx.OK | wx.ICON_ERROR)
                return
            optimized_prompt = result.get('data', {}).get('optimized_prompt', '')
            self.prompt_text.SetValue(optimized_prompt)
        except Exception as e:
            wx.MessageBox(f'优化失败: {e}', '错误', wx.OK | wx.ICON_ERROR)
        finally:
            del loading
            wx.YieldIfNeeded()

    def on_ok(self, event):
        prompt = self.prompt_text.GetValue()
        ratio = self.ratio_choice.GetStringSelection()
        model = self.model_choice.GetStringSelection()
        duration = int(self.duration_choice.GetStringSelection())
        video_nums = int(self.nums_choice.GetStringSelection())
        video_name = self.file_name_text.GetValue()
        run_after_add = self.run_checkbox.GetValue()
        if not prompt.strip():
            wx.MessageBox('提示词不能为空，请输入提示词', '提示', wx.OK | wx.ICON_INFORMATION)
            return
        if not video_name.strip():
            wx.MessageBox('文件名不能为空，请输入文件名', '提示', wx.OK | wx.ICON_INFORMATION)
            return
        self.loading = wx.BusyInfo("正在处理中，请稍候...", parent=self)
        wx.YieldIfNeeded()
        def do_request():
            if self.task_id:
                # 编辑模式，更新任务
                update_task_data = {
                    'task_id': self.task_id,
                    'prompt': prompt,
                    'model': model,
                    'ratio': ratio,
                    'video_name':video_name,
                    'seconds': duration,
                    'numbers': video_nums
                }
                result = update_task(UserSession.get_user_id(), self.task_id, update_task_data)
                if result.get('success') is True:
                    if run_after_add:
                        run_result = run_task(UserSession.get_user_id(), self.task_id)
                        wx.CallAfter(self.handle_run_result, run_result)
                    else:
                        wx.CallAfter(self.handle_update_result, True, None)
                else:
                    wx.CallAfter(self.handle_update_result, False, None)
            else:
                # 新增模式
                create_task_data = {
                    'prompt': prompt,
                    'model': model,
                    'ratio': ratio,
                    'seconds': duration,
                    'video_name':video_name,
                    'numbers': video_nums
                }
                result = create_task(UserSession.get_user_id(), create_task_data)
                if result.get('success') is True:
                    task_id = result.get('data')
                    if run_after_add:
                        run_result = run_task(UserSession.get_user_id(), task_id)
                        wx.CallAfter(self.handle_run_result, run_result)
                    else:
                        wx.CallAfter(self.handle_create_result, True, None)
                else:
                    wx.CallAfter(self.handle_create_result, False, None)
        threading.Thread(target=do_request, daemon=True).start()

    def handle_update_result(self, success, msg):
        if hasattr(self, 'loading') and self.loading:
            del self.loading
            wx.YieldIfNeeded()
        if success:
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox('任务更新失败', '错误', wx.OK | wx.ICON_ERROR)

    def handle_create_result(self, success, msg):
        if hasattr(self, 'loading') and self.loading:
            del self.loading
            wx.YieldIfNeeded()
        if success:
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox('任务提交失败', '错误', wx.OK | wx.ICON_ERROR)

    def handle_run_result(self, result):
        if hasattr(self, 'loading') and self.loading:
            del self.loading
            wx.YieldIfNeeded()
        if result.get('success') is False:
            wx.MessageBox(f'任务运行失败: {result.get("msg", "未知错误")}', '错误', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('任务运行成功！', '成功', wx.OK | wx.ICON_INFORMATION)
        self.EndModal(wx.ID_OK)

    def get_task_data(self):
        return self.task_data

    def EndModal(self, retCode):
        super().EndModal(retCode)
        if retCode == wx.ID_OK:
            parent = self.GetParent()
            if hasattr(parent, 'refresh_task_list'):
                parent.refresh_task_list(is_show_loading=False)

    def on_cancel(self, event):
        self.EndModal(wx.ID_CANCEL)

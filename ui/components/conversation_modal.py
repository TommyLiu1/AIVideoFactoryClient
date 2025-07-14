import uuid
from threading import Thread
import wx
import wx.html2
import markdown
import wx.lib.scrolledpanel as scrolled
from api.text_optimize_api import send_message
from ui.components.markdown_static_text import MarkdownStaticText


class LoadingPanel(wx.Panel):
    """加载中的动画气泡（优化版）"""

    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour(wx.Colour(245, 245, 245))

        # 使用更流畅的动画实现
        self.loading_text = wx.StaticText(self, label="思考中...")
        self.loading_text.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))

        # 使用wx.Timer实现动画（确保在主线程运行）
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_loading_text, self.timer)
        self.dot_count = 0
        self.timer.Start(300)  # 加快动画速度

        # 布局
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.loading_text, 1, wx.ALIGN_CENTER | wx.ALL, 15)
        self.SetSizer(sizer)

    def update_loading_text(self, event):
        """使用更流畅的动画逻辑"""
        self.dot_count = (self.dot_count + 1) % 4
        dots = "." * self.dot_count
        self.loading_text.SetLabel(f"思考中{dots}")
        self.loading_text.Refresh()  # 强制立即刷新

    def Destroy(self):
        self.timer.Stop()
        super().Destroy()


class RoundedMessagePanel(wx.Panel):
    """自定义圆角消息气泡（动态宽度 + 垂直居中）"""

    def __init__(self, parent, text, is_user, bg_color, text_color):
        super().__init__(parent)
        self.text = text
        self.is_user = is_user
        self.bg_color = bg_color
        self.text_color = text_color

        # 主滚动面板
        self.scroll_panel = wx.ScrolledWindow(self, style=wx.VSCROLL)
        self.scroll_panel.SetScrollRate(0, 10)
        self.scroll_panel.SetBackgroundColour(bg_color)

        # 文本控件
        self.text_ctrl = MarkdownStaticText(self.scroll_panel, label=text, style=wx.ALIGN_LEFT)
        self.text_ctrl.SetForegroundColour(text_color)
        self.text_ctrl.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        # self.webview = wx.html2.WebView.New(self)
        # self.webview.SetBackgroundColour(bg_color)
        # 转换Markdown为HTML
        # self.load_markdown(text)

        # 计算文本尺寸
        dc = wx.ClientDC(self.text_ctrl)
        dc.SetFont(self.text_ctrl.GetFont())
        text_width, text_height = dc.GetMultiLineTextExtent(text)

        # 设置气泡尺寸
        bubble_width = min(508, text_width + 40)  # 最大宽度380px
        self.text_ctrl.Wrap(bubble_width - 20)  # 换行宽度

        # 重新计算换行后的高度
        _, wrapped_height = dc.GetMultiLineTextExtent(self.text_ctrl.GetLabel())
        max_height = min(400, wrapped_height + 20)  # 最大高度400px

        # 设置滚动区域
        self.scroll_panel.SetVirtualSize(wx.Size(bubble_width, wrapped_height + 20))
        self.scroll_panel.SetMinSize(wx.Size(bubble_width, max_height))

        # 布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(self.webview, 0, wx.ALL, 10)
        sizer.Add(self.text_ctrl, 0, wx.ALL, 10)
        self.scroll_panel.SetSizer(sizer)

        # 主面板布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.scroll_panel, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

        # 绑定绘制事件
        # self.webview.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)
        self.text_ctrl.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def load_markdown(self, markdown_text):
        """加载Markdown内容并转换为HTML"""
        html = markdown.markdown(markdown_text)

        # 添加样式保持气泡外观
        styled_html = f"""
           <html>
               <style>
                   body {{
                       margin: 8px;
                       padding: 0;
                       background-color: {self.bg_color.GetAsString(wx.C2S_HTML_SYNTAX)};
                       color: {self.text_color.GetAsString(wx.C2S_HTML_SYNTAX)};
                       font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                       font-size: 14px;
                       line-height: 1.5;
                   }}
                   pre {{
                       background-color: rgba(0,0,0,0.05);
                       padding: 10px;
                       border-radius: 4px;
                       overflow-x: auto;
                   }}
                   code {{
                       font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
                       font-size: 90%;
                   }}
                   a {{
                       color: {self.text_color.GetAsString(wx.C2S_HTML_SYNTAX)};
                       text-decoration: underline;
                   }}
                   blockquote {{
                       border-left: 3px solid #ccc;
                       margin: 0;
                       padding-left: 15px;
                       color: #666;
                   }}
               </style>
               <body>{html}</body>
           </html>
           """

        self.webview.SetPage(styled_html, "")

    def on_context_menu(self, event):
        """右键菜单事件"""
        menu = wx.Menu()

        # 添加复制菜单项
        copy_item = menu.Append(wx.ID_COPY, "复制文本")
        self.Bind(wx.EVT_MENU, self.on_copy, copy_item)
        # 显示菜单
        self.PopupMenu(menu)
        menu.Destroy()

    def on_copy(self, event):
        """复制文本到剪贴板"""
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.text))
            wx.TheClipboard.Close()
            # 显示短暂提示
            wx.MessageBox("文本已复制到剪贴板", "提示", wx.OK | wx.ICON_INFORMATION, self)


    def on_paint(self, event):
        """绘制圆角气泡和箭头"""
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.bg_color))
        dc.SetPen(wx.Pen(self.bg_color))

        width, height = self.GetSize()
        radius = 12  # 圆角半径

        # 绘制圆角矩形
        dc.DrawRoundedRectangle(0, 0, width, height, radius)

        # 绘制箭头
        if self.is_user:
            points = [
                wx.Point(width, height // 2 - 8),
                wx.Point(width, height // 2 + 8),
                wx.Point(width - 10, height // 2)
            ]
        else:
            points = [
                wx.Point(0, height // 2 - 8),
                wx.Point(0, height // 2 + 8),
                wx.Point(10, height // 2)
            ]
        dc.DrawPolygon(points)

    def on_size(self, event):
        self.Refresh()
        event.Skip()

class ConversationModal(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title='会话：' + str(uuid.uuid4()), size=wx.Size(560, 680))
        self.Centre()
        self.SetBackgroundColour(wx.Colour(240, 242, 245))  # 类似 DeepSeek 的背景色
        self.messages = []
        self._is_sending = False  # 发送状态标志

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 顶部栏（可选）
        hbox_top = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, label="")
        title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        hbox_top.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(hbox_top, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        # 消息列表（使用 ScrolledPanel 支持更灵活的滚动）
        self.msg_panel = scrolled.ScrolledPanel(self)
        self.msg_panel.SetupScrolling()
        self.msg_panel.SetBackgroundColour(wx.Colour(240, 242, 245))
        self.msg_sizer = wx.BoxSizer(wx.VERTICAL)
        self.msg_panel.SetSizer(self.msg_sizer)
        vbox.Add(self.msg_panel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 8)

        # 输入区
        hbox_input = wx.BoxSizer(wx.HORIZONTAL)
        self.input_ctrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)
        self.input_ctrl.SetMinSize(wx.Size(-1, 60))
        self.input_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_send)
        hbox_input.Add(self.input_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        self.send_btn = wx.Button(self, label="发送", size=wx.Size(80, 60))
        self.send_btn.Bind(wx.EVT_BUTTON, self.on_send)
        hbox_input.Add(self.send_btn, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        vbox.Add(hbox_input, 0, wx.EXPAND | wx.ALL, 8)

        self.SetSizer(vbox)

    def on_send(self, event):
        if self._is_sending:
            return
        content = self.input_ctrl.GetValue().strip()
        if not content:
            return
        self._is_sending = True
        self.send_btn.Disable()  # 禁用发送按钮
        # 1. 先显示用户消息
        self.add_message('user', content)
        self.input_ctrl.SetValue("")
        # 2. 添加Loading占位符
        loading_panel = self.add_loading_message()
        Thread(
            target=self.do_send_message,
            args=(loading_panel, content),
            daemon=True
        ).start()

    def do_send_message(self, loading_panel, content):
        res = send_message(content)
        if not res.get('success'):
            reply_message = '请求失败，请稍后重试'
        else:
            reply_message = res.get('data').get('answer')
        wx.CallAfter(self.on_reply_received, loading_panel,reply_message)
    def on_reply_received(self, loading_panel, reply_content):
        """收到回复后的处理"""
        # 1. 删除Loading占位符
        if loading_panel:
            loading_panel.Destroy()
        # 2. 显示实际回复
        self.add_message('assistant', reply_content)
        self._is_sending = False
        self.send_btn.Enable()  # 重新启用发送按钮
        # 3. 滚动到底部
        wx.CallLater(200, self.scroll_to_bottom)


    def add_loading_message(self):
        """添加Loading占位符"""
        msg_container = wx.Panel(self.msg_panel)
        msg_container.SetBackgroundColour(wx.Colour(240, 242, 245))

        # 助手消息左对齐
        msg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        msg_sizer.AddStretchSpacer(0)  # 左对齐

        # 添加Loading动画
        loading_bubble = LoadingPanel(msg_container)
        msg_sizer.Add(loading_bubble, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        msg_container.SetSizer(msg_sizer)
        self.msg_sizer.Add(msg_container, 0, wx.EXPAND | wx.ALL, 5)

        # 更新布局并滚动
        self.msg_panel.Layout()
        self.msg_panel.ScrollChildIntoView(msg_container)

        return loading_bubble  # 返回引用以便后续删除

    def add_message(self, role, content):
        # 设置消息样式
        is_user = (role == 'user')
        bg_color =wx.Colour(100, 180, 255) if is_user else wx.Colour(255, 255, 255)
        text_color = wx.Colour(0, 0, 0)

        # 创建消息容器（Panel）
        msg_container = wx.Panel(self.msg_panel)
        msg_container.SetBackgroundColour(wx.Colour(240, 242, 245))  # 背景透明

        # 消息布局（用户消息右对齐，助手消息左对齐）
        msg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        if is_user:
            msg_sizer.AddStretchSpacer(1)  # 用户消息右对齐

        # 添加圆角消息气泡
        msg_bubble = RoundedMessagePanel(msg_container, content, is_user, bg_color, text_color)
        msg_sizer.Add(msg_bubble, 0, wx.TOP | wx.BOTTOM, 5)

        if not is_user:
            msg_sizer.AddStretchSpacer(1)  # 助手消息左对齐

        msg_container.SetSizer(msg_sizer)
        self.msg_sizer.Add(msg_container, 0, wx.EXPAND | wx.ALL, 5)
        self.messages.append((role, content))

        # 更新布局并滚动到底部
        self.msg_panel.Layout()
        self.msg_panel.SetupScrolling()
        self.msg_panel.ScrollChildIntoView(msg_container)

    def scroll_to_bottom(self):
        """最可靠的滚动到底部实现"""
        total_height = sum([c.GetSize().height for c in self.msg_panel.GetChildren()])

        # 设置虚拟大小（比实际内容稍大以确保可以滚动）
        self.msg_panel.SetVirtualSize(wx.Size(self.msg_panel.GetSize().width, total_height + 20))

        # 滚动到底部
        scroll_pos = self.msg_panel.GetScrollRange(wx.VERTICAL)
        self.msg_panel.Scroll(-1, scroll_pos)
        self.msg_panel.Refresh()
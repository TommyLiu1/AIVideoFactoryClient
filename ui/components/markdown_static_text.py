import re
import wx
import markdown
from bs4 import BeautifulSoup

class MarkdownStaticText(wx.StaticText):
    """支持基本Markdown的StaticText控件"""

    def __init__(self, parent, label="", style=wx.ALIGN_LEFT):
        super().__init__(parent, label=self._render_markdown(label), style=style)
        self._original_text = label
        self._font_normal = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self._font_bold = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self._font_italic = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)

    def _render_markdown(self, text):
        """简单Markdown渲染"""
        # 移除Markdown标记（实际显示时）
        html = markdown.markdown(text)
        # 移除HTML标签只保留文本
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()# 标题

    def DrawText(self, dc, text, x, y):
        """自定义文本绘制以支持简单Markdown格式"""
        current_x = x
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`.*?`)', text)  # 分割文本

        for part in parts:
            if not part:
                continue

            # 判断文本样式
            if part.startswith('**') and part.endswith('**'):
                dc.SetFont(self._font_bold)
                part = part[2:-2]
            elif part.startswith('*') and part.endswith('*'):
                dc.SetFont(self._font_italic)
                part = part[1:-1]
            elif part.startswith('`') and part.endswith('`'):
                dc.SetFont(self._font_normal)
                part = part[1:-1]
                # 可以添加背景色表示代码
                w, h = dc.GetTextExtent(part)
                dc.SetPen(wx.TRANSPARENT_PEN)
                dc.SetBrush(wx.Brush(wx.Colour(240, 240, 240)))
                dc.DrawRectangle(current_x, y, w, h)
            else:
                dc.SetFont(self._font_normal)

            dc.DrawText(part, current_x, y)
            current_x += dc.GetTextExtent(part)[0]

    def OnPaint(self, event):
        """自定义绘制"""
        dc = wx.PaintDC(self)
        # self.PrepareDC(dc)

        rect = self.GetClientRect()
        text = self._original_text

        # 设置文本颜色
        dc.SetTextForeground(self.GetForegroundColour())

        # 计算换行
        dc.SetFont(self._font_normal)
        wrapped_text = self._wrap_text(dc, text, rect.width - 20)  # 留出边距

        # 绘制文本
        y = 5
        for line in wrapped_text.split('\n'):
            self.DrawText(dc, line, 10, y)
            y += dc.GetCharHeight()

    def _wrap_text(self, dc, text, max_width):
        """文本换行处理"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            width = dc.GetTextExtent(test_line)[0]

            if width <= max_width or not current_line:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return '\n'.join(lines)
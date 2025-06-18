
from datetime import datetime
import wx
from loguru import logger
from ui.login_frame import LoginFrame
import os
import sys

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")
log_dir = os.path.join(base_path, "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
# 生成带时间戳的日志文件名
now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(log_dir, f"AI_Generate_video_factory_{now_str}.log")

# 初始化loguru日志配置
logger.add(log_path, level="DEBUG", rotation="10 MB", retention="10 days", encoding="utf-8", enqueue=True, backtrace=True, diagnose=True)


class AIVideoGenerateApp(wx.App):
    def OnInit(self):

        try:
            login_frame = LoginFrame(None, title="用户登录")
            login_frame.Show()
            return True
        except Exception as e:
            logger.error(f"应用启动失败: {e}")
            return False

    def OnExit(self):
        sys.exit(0)


if __name__ == '__main__':
    app = AIVideoGenerateApp()
    app.MainLoop()
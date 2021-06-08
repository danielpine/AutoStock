import ctypes
import logging
import os
import tkinter as tk

from cefpython3 import cefpython as cef

log = logging.getLogger()
# log.setLevel(logging.ERROR)


class Application(tk.Frame):
    navigation_bar = None

    def __init__(self, url='http://127.0.0.1:5000/'):
        root = tk.Tk()
        root.geometry("1366x640")
        tk.Frame.__init__(self, root)
        self.master.title("")
        self.bind("<Configure>", self.on_configure)
        self.browser_frame = BrowserFrame(
            self, self.navigation_bar, url=url)  # 浏览器框架
        self.browser_frame.grid(
            row=1, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        self.pack(fill=tk.BOTH, expand=tk.YES)  # 包装 Application

    def startup(self):
        cef.Initialize()
        self.mainloop()
        cef.Shutdown()
        os._exit(0)

    def on_configure(self, event):
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_Application_configure(width, height)


class BrowserFrame(tk.Frame):
    closing = False
    browser = None

    def __init__(self, master,   navigation_bar=None, url='http://127.0.0.1:5000/'):
        self.navigation_bar = navigation_bar
        tk.Frame.__init__(self, master)
        self.bind("<Configure>", self.on_configure)
        self.url = url

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=self.url)
        self.message_loop_work()

    def get_window_handle(self):  # 获取窗口句柄
        if self.winfo_id() > 0:
            return self.winfo_id()

    def message_loop_work(self):  # 消息循环工作
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):  # 判断是否有 cef 对象
        if not self.browser:
            self.embed_browser()

    def on_Application_configure(self, width, height):  # cef 窗口大小
        if self.browser:
            ctypes.windll.user32.SetWindowPos(self.browser.GetWindowHandle(),
                                              0, 0, 0, width, height, 0x0002)


if __name__ == '__main__':
    Application(url='chrome://version/').startup()

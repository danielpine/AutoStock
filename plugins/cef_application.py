import pywintypes
import ctypes
import logging
import os
import threading
import tkinter as tk

import win32api
import win32con
import win32gui
import win32gui_struct
from cefpython3 import cefpython as cef

log = logging.getLogger()
# log.setLevel(logging.ERROR)


class SysTrayIcon (object):
    '''SysTrayIcon类用于显示任务栏图标'''
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 5320

    def __init__(s, icon, hover_text, menu_options, on_quit, tk_window=None, default_menu_index=None, window_class_name=None):
        '''
        icon         需要显示的图标文件路径
        hover_text   鼠标停留在图标上方时显示的文字
        menu_options 右键菜单，格式: (('a', None, callback), ('b', None, (('b1', None, callback),)))
        on_quit      传递退出函数，在执行退出时一并运行
        tk_window    传递Tk窗口，s.root，用于单击图标显示窗口
        default_menu_index 不显示的右键菜单序号
        window_class_name  窗口类名
        '''
        s.icon = icon
        s.hover_text = hover_text
        s.on_quit = on_quit
        s.root = tk_window

        menu_options = menu_options + (('退出', None, s.QUIT),)
        s._next_action_id = s.FIRST_ID
        s.menu_actions_by_id = set()
        s.menu_options = s._add_ids_to_menu_options(list(menu_options))
        s.menu_actions_by_id = dict(s.menu_actions_by_id)
        del s._next_action_id

        s.default_menu_index = (default_menu_index or 0)
        s.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): s.restart,
                       win32con.WM_DESTROY: s.destroy,
                       win32con.WM_COMMAND: s.command,
                       win32con.WM_USER+20: s.notify, }
        # 注册窗口类。
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = s.window_class_name
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map  # 也可以指定wndproc.
        s.classAtom = win32gui.RegisterClass(wc)

    def activation(s):
        '''激活任务栏图标，不用每次都重新创建新的托盘图标'''
        hinst = win32gui.GetModuleHandle(None)  # 创建窗口。
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        s.hwnd = win32gui.CreateWindow(s.classAtom,
                                       s.window_class_name,
                                       style,
                                       0, 0,
                                       win32con.CW_USEDEFAULT,
                                       win32con.CW_USEDEFAULT,
                                       0, 0, hinst, None)
        win32gui.UpdateWindow(s.hwnd)
        s.notify_id = None
        # s.refresh(title='软件已后台！', msg='点击重新打开', time=500)
        s.refresh(title='软件已后台！', msg='', time=500)

        win32gui.PumpMessages()

    def refresh(s, title='', msg='111', time=500):
        '''刷新托盘图标
           title 标题
           msg   内容，为空的话就不显示提示
           time  提示显示时间'''
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(s.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, s.icon, win32con.IMAGE_ICON,
                                       0, 0, icon_flags)
        else:  # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if s.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD

        s.notify_id = (s.hwnd, 0,  # 句柄、托盘图标ID
                       # 托盘图标可以使用的功能的标识
                       win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO,
                       win32con.WM_USER + 20, hicon, s.hover_text,  # 回调消息ID、托盘图标句柄、图标字符串
                       msg, time, title,   # 提示内容、提示显示时间、提示标题
                       win32gui.NIIF_INFO  # 提示用到的图标
                       )
        win32gui.Shell_NotifyIcon(message, s.notify_id)

    def show_menu(s):
        '''显示右键菜单'''
        menu = win32gui.CreatePopupMenu()
        s.create_menu(menu, s.menu_options)

        pos = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(s.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                s.hwnd,
                                None)
        win32gui.PostMessage(s.hwnd, win32con.WM_NULL, 0, 0)

    def _add_ids_to_menu_options(s, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in s.SPECIAL_ACTIONS:
                s.menu_actions_by_id.add((s._next_action_id, option_action))
                result.append(menu_option + (s._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               s._add_ids_to_menu_options(option_action),
                               s._next_action_id))
            s._next_action_id += 1
        return result

    def restart(s, hwnd, msg, wparam, lparam):
        s.refresh()

    def destroy(s, hwnd=None, msg=None, wparam=None, lparam=None, exit=1):
        nid = (s.hwnd, 0)
        if exit and s.on_quit:
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            win32gui.PostQuitMessage(0)  # 终止应用程序。
            s.on_quit(s)  # 需要传递自身过去时用 s.on_quit(s)
        else:
            s.root.deiconify()  # 显示tk窗口

    def notify(s, hwnd, msg, wparam, lparam):
        '''鼠标事件'''
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            pass
        elif lparam == win32con.WM_RBUTTONUP:  # 右键弹起
            s.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 左键弹起
            s.destroy(exit=0)
        return True
        """
        可能的鼠标事件：
          WM_MOUSEMOVE      #光标经过图标
          WM_LBUTTONDOWN    #左键按下
          WM_LBUTTONUP      #左键弹起
          WM_LBUTTONDBLCLK  #双击左键
          WM_RBUTTONDOWN    #右键按下
          WM_RBUTTONUP      #右键弹起
          WM_RBUTTONDBLCLK  #双击右键
          WM_MBUTTONDOWN    #滚轮按下
          WM_MBUTTONUP      #滚轮弹起
          WM_MBUTTONDBLCLK  #双击滚轮
        """

    def create_menu(s, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = s.prep_menu_icon(option_icon)

            if option_id in s.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                s.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(s, icon):
        # 加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(
            0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x,
                            ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(s, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        s.execute_menu_option(id)

    def execute_menu_option(s, id):
        print(id)
        menu_action = s.menu_actions_by_id[id]
        if menu_action == s.QUIT:
            win32gui.DestroyWindow(s.hwnd)
        else:
            menu_action(s)


class Application(tk.Frame):
    navigation_bar = None
    icon = os.path.join(os.path.abspath('.'), 'static/image/favicon.ico')

    def __init__(self, url='http://127.0.0.1:5000/'):
        self.root = tk.Tk()
        self.root.iconbitmap(self.icon)
        self.root.geometry("1366x640")
        flask_thread = threading.Thread(
            target=self.create_SysTrayIcon, args=())
        flask_thread.setDaemon(True)
        flask_thread.start()
        self.root.protocol('WM_DELETE_WINDOW', self.root.withdraw)
        tk.Frame.__init__(self, self.root)
        self.master.title("Auto Stock")
        self.bind("<Configure>", self.on_configure)
        self.browser_frame = BrowserFrame(
            self, self.navigation_bar, url=url)  # 浏览器框架
        self.browser_frame.grid(
            row=1, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        self.pack(fill=tk.BOTH, expand=tk.YES)  # 包装 Application

    def switch_icon(s, _sysTrayIcon, icon='favicon.ico'):
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon
        # 只是一个改图标的例子，不需要的可以删除此函数
        _sysTrayIcon.icon = icon
        _sysTrayIcon.refresh()

        # 气泡提示的例子
        s.show_msg(title='图标更换', msg='图标更换成功！', time=500)

    def show_msg(s, title='标题', msg='内容', time=500):
        s.SysTrayIcon.refresh(title=title, msg=msg, time=time)
        pass

    def create_SysTrayIcon(s, hover_text="Auto Stock"):
        '''隐藏窗口至托盘区，调用SysTrayIcon的重要函数'''
        # 托盘图标右键菜单, 格式: ('name', None, callback),下面也是二级菜单的例子
        # 24行有自动添加‘退出’，不需要的可删除
        menu_options = (('一级 菜单', None, s.switch_icon),
                        ('二级 菜单', None, (('更改 图标', None, s.switch_icon), )))
        menu_options = ()
        icon = os.path.join(os.path.abspath('.'), s.icon)
        s.SysTrayIcon = SysTrayIcon(
            icon,  # 图标
            hover_text,  # 光标停留显示文字
            menu_options,  # 右键菜单
            on_quit=s.exit,  # 退出调用
            tk_window=s.root,  # Tk窗口
        )
        s.SysTrayIcon.activation()

    def exit(s, _sysTrayIcon=None):
        print('quit...')
        s.root.quit()

    def startup(self):
        cef.Initialize()
        self.root.mainloop()
        cef.Shutdown()
        print('Application ended')
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
        self.master = master

    def PyAlert(s, msg):
        print('calling PyAlert()')
        s.master.SysTrayIcon.refresh(title='Algo Trading', msg=msg, time=500)
        # hwnd = pywintypes.HANDLE(int(s.master.root.frame(), 16))
        # # win32gui.MessageBox(hwnd, msg,
        # #                     "PyAlert()", win32con.MB_ICONQUESTION)
        # message = win32gui.NIM_ADD
        # ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        # ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        # hicon = win32gui.LoadImage(
        #     0,  os.path.join(os.path.abspath('.'), 'favicon.ico'),
        #     win32con.IMAGE_ICON,
        #     ico_x,
        #     ico_y,
        #     win32con.LR_LOADFROMFILE)
        # s.notify_id = (hwnd, 0,  # 句柄、托盘图标ID
        #                # 托盘图标可以使用的功能的标识
        #                win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP | win32gui.NIF_INFO,
        #                win32con.WM_USER + 20, hicon, 'Auto Stock',  # 回调消息ID、托盘图标句柄、图标字符串
        #                msg, 500, 'Algo Trading',   # 提示内容、提示显示时间、提示标题
        #                win32gui.NIIF_INFO  # 提示用到的图标
        #                )
        # win32gui.Shell_NotifyIcon(message, s.notify_id)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url=self.url)

        bindings = cef.JavascriptBindings(
            bindToFrames=True, bindToPopups=True)
        bindings.SetFunction("alert", self.PyAlert)
        self.browser.SetJavascriptBindings(bindings)
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

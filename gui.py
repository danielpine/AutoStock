# -*- coding: utf-8 -*-
import os
import time
import win32gui
import win32con
import win32api
import win32ui
from imageDeal import identify
from nums.settings import pwd

# 从顶层窗口向下搜索主窗口，无法搜索子窗口
# FindWindow(lpClassName=None, lpWindowName=None)  窗口类名 窗口标题名
handle = win32gui.FindWindow("光大证券金阳光卓越版V7.02", None) 
#enter password
#获取某个句柄的类名和标题
#title = win32gui.GetWindowText(handle)     
#clsname = win32gui.GetClassName(handle)

# 打印句柄
# 十进制
#print(1,handle)
# 十六进制
#print(2,"%x" %(handle) )

#train Array
numarr=[[333, 370, 291, 312],
 [500, 111, 142, 571],
 [300, 225, 333, 200],
 [466, 250, 250, 375],
 4,
 [187, 562, 125, 333],
 [361, 222, 312, 281],
 [333, 111, 0, 257],
 [450, 531, 500, 428],
 [325, 366, 222, 333]]

os.remove("log.txt")

def demo_top_windows():
    '''
    演示如何列出所有的顶级窗口
    :return:
    '''
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    show_windows(hWndList)
 
    return hWndList

def show_windows(hWndList):
    for h in hWndList:
        # 获取窗口位置
        left, top, right, bottom = win32gui.GetWindowRect(h)
        if left!=0 or right!=0:
            #get 光大证券窗口：
            if show_window_attr(h):
                #show tag window
                
                win32gui.SetForegroundWindow (h)
                win32gui.SetWindowPos(h, win32con.HWND_TOPMOST, 500,500,right-left,bottom-top, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)   
                win32gui.ShowWindow(h, win32con.SW_SHOW)
             
                #print window's location
                print(left, top, right, bottom)
                #get password input location
                pwdLeft=left+484
                pwdTop=top+212
                ms=[]
                ms.append(pwdLeft)
                ms.append(pwdTop)
                #move mouse to the location just got above
                win32api.SetCursorPos(ms) 
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                key_input(pwd)
                #get check code
                #screen
                codeLeft=left+550
                codeTop=top+250
                ca=[codeLeft,codeTop]
                win32api.SetCursorPos(ca)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                file="cut.jpg"
                window_capture((589,238),(58,21),file,h)
                result=identify(file,numarr)
                win32api.SetCursorPos(ca)
                print("识别：",result)
                key_input(result)
                codeLeft=left+480
                codeTop=top+309
                ca=[codeLeft,codeTop]
                win32api.SetCursorPos(ca)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

def window_capture(strXY,endXY,filename,hwnd):
  #hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
  hwndDC = win32gui.GetWindowDC(hwnd)
  # 根据窗口的DC获取mfcDC
  mfcDC = win32ui.CreateDCFromHandle(hwndDC)
  # mfcDC创建可兼容的DC
  saveDC = mfcDC.CreateCompatibleDC()
  # 创建bigmap准备保存图片
  saveBitMap = win32ui.CreateBitmap()
  # 获取监控器信息
  MoniterDev = win32api.EnumDisplayMonitors(None, None)
  w = MoniterDev[0][2][2]
  h = MoniterDev[0][2][3]
  # print w,h　　　#图片大小
  # 为bitmap开辟空间
  saveBitMap.CreateCompatibleBitmap(mfcDC, endXY[0], endXY[1])#w,h
  # 高度saveDC，将截图保存到saveBitmap中
  saveDC.SelectObject(saveBitMap)
  # 截取从左上角（0，0）长宽为（w，h）的图片
  saveDC.BitBlt((0,0), endXY, mfcDC, strXY, win32con.SRCCOPY)
  saveBitMap.SaveBitmapFile(saveDC, filename)
                
    #print(len(hWndList))
VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
    '`': 0xC0}

def key_input(str=''):
    for c in str:
        win32api.keybd_event(VK_CODE[c], 0, 0, 0)
        win32api.keybd_event(VK_CODE[c], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.01)
def show_window_attr(hWnd):
    '''
    显示窗口的属性
    :return:
    '''
    if not hWnd:
        return
    
 
    #中文系统默认title是gb2312的编码
    title = win32gui.GetWindowText(hWnd)
    #title = gbk2utf8(title)
    clsname = win32gui.GetClassName(hWnd)
    '''
    print ('窗口句柄:%s ' % (hWnd))
    print ('窗口标题:%s' % (title))
    print ('窗口类名:%s' % (clsname))
    print ('')
    '''
    with open("log.txt",'a+') as ff:
        ff.write('窗口句柄:%s \n' % (hWnd))
        ff.write('窗口标题:%s \n' % (title))
        ff.write('窗口类名:%s \n' % (clsname))
        ff.write('----------------------\n')
    if title=="光大证券金阳光卓越版V7.02":
        print ('窗口句柄:%s ' % (hWnd))
        print ('窗口标题:%s' % (title))
        print ('窗口类名:%s' % (clsname))
        print ('')
        return True
    else :
        return False
def gbk2utf8(s):
    return s.decode('gbk').encode('utf-8')

#os.system("cd C:\zd_gdzq && TdxW.exe && exit")

demo_top_windows()
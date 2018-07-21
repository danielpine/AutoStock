# -*- coding: utf-8 -*-
import os
import time
import win32gui
import win32con
import win32api
import win32ui
from imageDeal import identify
from settings.settings import pwd
from settings.settings import numarr
from settings.settings import VK_CODE

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
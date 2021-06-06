from logging import log
from app.util.logger import log
import base64


def jpg_to_base64(path):
    f = open(path, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()
    log.info(ls_f)


def base64_to_jpg(bs):
    bs = 'iVBORw0KGgoAAAANSUhEUg....'  # 太长了省略
    imgdata = base64.b64decode(bs)
    file = open('2.jpg', 'wb')
    file.write(imgdata)
    file.close()


jpg_to_base64(r'C:\Users\danielpine\Pictures\1.png')

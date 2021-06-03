# -*- coding: UTF-8 -*- 
 
from aip import AipOcr 
import json 

 
# 定义常量 
APP_ID = '9851066' 
API_KEY = 'LUGBatgyRGoerR9FZbV4SQYk' 
SECRET_KEY = 'fB2MNz1c2UHLTximFlC4laXPg7CVfyjV' 
 
# 初始化AipFace对象 
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY) 
 
# 读取图片 
filePath = "cut.jpg" 
def get_file_content(filePath): 
  with open(filePath, 'rb') as fp: 
    return fp.read() 
 
# 定义参数变量 
options = { 
 'detect_direction': 'true', 
 'language_type': 'CHN_ENG', 
} 
 
# 调用通用文字识别接口 
result = aipOcr.basicGeneral(get_file_content(filePath), options) 
print(json.dumps(result).decode("unicode-escape")) 












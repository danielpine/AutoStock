import time
import urllib.request as urllib2
import http.cookiejar as cookielib
import re

title="ID,股票名字,今日开盘价,昨日收盘价,当前价格,今日最高价,今日最低价,竞买价,竞卖价,成交股票数,成交金额,买一数,买一价,买二数,买二价,买三数,买三价,买四数,买四价,买五数,买五价,卖一数,卖一价,卖二数,卖二价,卖三数,卖三价,卖四数,卖四价,卖五数,卖五价,日期,时间"
 
check_url = "http://hq.sinajs.cn/list=%s"
check_id_list = ["sh000001", "sz399001","sz399006", "sh600016", "sh601939", "sh601098", "sz300749","sz000068"]
 
def get_info_from_sina(ids):
    # use to store cookies
    cookie = cookielib.CookieJar()  
    # create an OpenerDirector instance,which can handle cookie automatically
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    # OpenerDirector automatically adds User-Agent and Connection header to every Request
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'),
                         ('Connection', 'keep-alive')]
    urllib2.install_opener(opener)
    url = check_url%ids
    request = urllib2.Request(url)
    response = opener.open(request)
    groups = re.findall(r'\"(.*)\"',response.read().decode('gbk')) 
    result=[title]
    titles=ids.split(',')
    for i,v in enumerate(groups):
        result.append(titles[i]+","+v)
    opener.close()
    cookie.clear()
    return '\n'.join(result)
 
def get_sys_time():
    return time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime(time.time()))
 
def get_info_form_feedback(basic_info):
    startIndex = basic_info.find(",") + 1
    endIndex = basic_info.rfind(",")
    info = basic_info[startIndex:endIndex]
    info_list = info.split(",")
    yesterday = info_list[1]
    now = round(float(info_list[2]),2)
    gap = round(float(now) - float(yesterday), 2)
    percent = round((gap / float(yesterday)) * 100, 2)
    if gap > 0:
        gap = "+" + str(gap)
        percent = "+" + str(percent)
    return "%s%s(%s%%)" % (str(now).ljust(10), str(gap), str(percent))

if __name__ == '__main__':
    print( ">>> %s <<<"%get_sys_time())
    infos = get_info_from_sina(','.join(check_id_list))
    print (infos)
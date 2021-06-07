import smtplib
from email.mime.text import MIMEText
# 设置服务器所需信息
# 163邮箱服务器地址
mail_host = 'smtp.163.com'
# 163用户名
mail_user = 'auto_stock'
# 密码(部分邮箱为授权码)
mail_pass = 'WEMCUXDRAEXVZSIJ'
# 邮件发送方邮箱地址
sender = 'auto_stock@163.com'
# 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receiver = 'danielpine@sina.com'


def send_plain_mail(title):
    # 设置email信息
    # 邮件内容设置
    message = MIMEText('content', 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receiver

    # 登录并发送邮件
    try:
        smtpObj = smtplib.SMTP()
        # 连接到服务器
        smtpObj.connect(mail_host, 25)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 发送
        smtpObj.sendmail(sender, receiver, message.as_string())
        # 退出
        smtpObj.quit()
        print('send_plain_mail success')
    except smtplib.SMTPException as e:
        print('send_plain_mail error', e)  # 打印错误

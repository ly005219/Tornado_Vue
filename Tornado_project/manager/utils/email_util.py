# import zmail

# def send_mail(from_mail:str,passwd:str,to_mail:str,subject:str,txt:str) -> None:
#     #server = zmail.server('2577265832@qq.com','oezalutdpbpjebec')
#     server = zmail.server(from_mail,passwd)
#     # 发邮件
#     #server.send_mail('hotelmail@126.com',{'subject':'这个测试邮件','content_text':'这个是内容'})
#     server.send_mail(to_mail,{'subject':subject,'content_text':txt})

# # if __name__ == '__main__':
# #     send_mail('2577265832@qq.com','oezalutdpbpjebec','ly2577265832@qq.com','测试邮件','这是测试邮件的内容')


import zmail
import smtplib

def send_mail(from_mail: str, passwd: str, to_mail: str, subject: str, txt: str) -> None:
    # 指定 SMTP 服务器地址和端口
    smtp_server = 'smtp.qq.com'  # 例如 QQ 邮箱的 SMTP 服务器地址
    smtp_port = 465  # 例如使用 SSL 端口 465

    # 打印调试信息
    print(f"Initializing server with: from_mail={from_mail}, passwd={passwd}, smtp_server={smtp_server}, smtp_port={smtp_port}")

    # 创建邮件服务器对象
    server = zmail.server(from_mail, passwd, smtp_host=smtp_server, smtp_port=smtp_port)

    # 创建邮件内容
    mail_content = {'subject': subject, 'content_text': txt}

    # 打印邮件内容
    print(f"Mail content: {mail_content}")

    # 发送邮件
    try:
        server.send_mail(to_mail, mail_content)
        print("邮件发送成功")
    except smtplib.SMTPResponseException as e:
        print(f"邮件发送失败: {e}")
    except Exception as e:
        print(f"邮件发送过程中发生错误: {e}")
    # 删除了 finally 中的 server.close()

if __name__ == '__main__':
    send_mail('2577265832@qq.com', 'oezalutdpbpjebec', 'ly2577265832@qq.com', '测试邮件', '这是测试邮件的内容')


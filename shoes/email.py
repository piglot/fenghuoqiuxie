from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    """
    Flask-Mail 中的 send() 函数使用 current_app，因此必须激活程序上下文
    """
    with app.app_context(): # 创建程序上下文
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    """
    异步发送电子邮件
    """
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread

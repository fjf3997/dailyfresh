from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

# 创建应用
app = Celery('task1', broker='redis://:6379/2')

# 创建任务函数
@app.task
def send_register_active_email(to_email, username, token):
    subject = '注册激活'
    message = ''
    from_email = settings.EMAIL_FROM
    recipient_list = [to_email]
    html_message = '<h1>%s,欢迎您!</h1><br>激活请点击<a href="http://127.0.0.1:8000/user/active/%s">' \
                   'http://127.0.0.1:8000/user/active/%s</a>' % (username, token, token)
    # subject, message, from_email, recipient_list,
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

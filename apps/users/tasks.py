from django.conf import settings
from django.core.mail import EmailMessage
from backGround.celery import app
from backGround.settings import EMAIL_FROM
from users.models import VerifyCode
from utils.email_send import random_str


@app.task
def send_mail():
    subject = 'test'
    text_content = '这是一封重要的报告邮件.'
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMessage(subject,
                       text_content,
                       from_email,
                       ['*******@qq.com', ])

    msg.send(fail_silently=False)


@app.task
def send_register_email(email, code):
    email_title = '激活链接'
    email_body = '同志您好，您的验证码是：{0}'.format(code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    return send_status


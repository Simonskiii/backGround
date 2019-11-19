from users.models import VerifyCode
from utils.asynchronous_send_mail import send_mail
from random import Random
from backGround.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# def send_register_email(email, send_type='register'):
#     email_record = VerifyCode()
#     code = random_str(6)
#     email_record.code = code
#     email_record.email = email
#     email_record.send_type = send_type
#
#     email_title = ''
#     email_body = ''
#     if send_type == 'register':
#         email_title = '激活链接'
#         email_body = '同志您好，您的验证码是：{0}'.format(code)
#         send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
#         if send_status:
#             email_record.save()
#         return send_status
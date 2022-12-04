from django.core.mail import send_mail
from django.utils import timezone

from application.celery import app
from application.settings import ADMINS, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from .models import Message


@app.task()
def send_admin_email(username, chat_title):
    send_mail(
        subject="New user added to chat",
        message=f'User {username} added to chat "{chat_title}"',
        from_email=EMAIL_HOST_USER,
        recipient_list=ADMINS,
    )


@app.task()
def log_number_of_messages():
    number_of_messages = len(Message.objects.values())
    logger = open('log_messages.txt', 'a')
    log_str = str(timezone.localtime(timezone.now())) + f' : {number_of_messages} messages sent' + '\n'
    logger.write(log_str)
    logger.close()

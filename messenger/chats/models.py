from django.db import models
from users.models import User


class Chat(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название чата')
    description = models.TextField(blank=True, verbose_name='Описание чата')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Чат, в котором находится сообщение')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Отправитель сообщения')
    message_text = models.TextField(verbose_name='Текст сообщения')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания сообщения')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

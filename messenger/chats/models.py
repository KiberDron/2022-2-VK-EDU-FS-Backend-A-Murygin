from django.db import models
from django.conf import settings


class Chat(models.Model):
    title = models.CharField('Название чата', max_length=200)
    description = models.TextField('Описание чата', blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats', verbose_name='Пользователи чата')

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
        related_name='messages',
        verbose_name='Чат, в котором находится сообщение')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='messages',
        verbose_name='Отправитель сообщения')
    message_text = models.TextField('Текст сообщения')
    creation_date = models.DateTimeField('Дата и время создания сообщения', auto_now_add=True)
    read_status = models.BooleanField('Статус прочтения сообщения', default=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

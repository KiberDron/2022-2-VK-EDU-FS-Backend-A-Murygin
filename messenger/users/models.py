from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения пользователя')
    chats = models.ManyToManyField('chats.Chat', verbose_name='Чаты пользователя')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user_name

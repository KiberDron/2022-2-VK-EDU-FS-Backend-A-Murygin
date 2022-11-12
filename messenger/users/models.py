from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    info = models.CharField('Информация о себе', max_length=1000, blank=True)
    status = models.CharField('Статус', max_length=200, blank=True)
    birthday = models.DateField('Дата рождения', null=True, blank=True)
    location = models.CharField('Город', max_length=30, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

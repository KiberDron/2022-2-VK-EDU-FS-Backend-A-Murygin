from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=200)
    birthday = models.DateField(null=True, blank=True)
    chats = models.ManyToManyField('chats.Chat')

    def __str__(self):
        return self.user_name

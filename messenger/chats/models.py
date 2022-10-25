from django.db import models
from users.models import User


class Chat(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    message_text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

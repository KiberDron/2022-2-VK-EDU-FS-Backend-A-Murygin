from rest_framework import serializers
from .models import Chat, Message, ChatMember


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'title', 'description']


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='chat.title')
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'text', 'creation_date', 'read_status']


class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['author', 'text']


class MessageReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = []


class UserInChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = ['chat', 'user']
